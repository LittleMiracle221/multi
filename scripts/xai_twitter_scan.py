#!/usr/bin/env python3
"""
xai_twitter_scan.py — 多市场（CA / AU / FR）xAI Grok Agent Tools API 扫推工具

调用 POST https://api.x.ai/v1/responses + tools=[{"type":"x_search"}]，
让 Grok 服务端自主跑多轮 x_keyword_search + x_semantic_search 把目标
语种的推文拉回来，给日报 workflow 消费。

用法:
    # 跑 CA 默认 Q1+Q2，72h 窗，输出到 scans/
    python scripts/xai_twitter_scan.py --market CA --hours 72 --out scans/

    # 只跑 FR 的 Q1
    python scripts/xai_twitter_scan.py --market FR --queries Q1 --hours 72

    # smoke test：验证 API key 是否可用
    python scripts/xai_twitter_scan.py --market AU --smoke-test

环境变量（从 skill 根目录 `.env` 加载，相对路径）：
    XAI_API_KEY               必填，以 xai- 开头
    XAI_MODEL                 可选，默认 grok-3-latest
    XAI_MAX_SEARCH_RESULTS    可选，默认 25

5A 标签映射:
    Q1/area=1 → compliance
    Q1/area=2 → self-custody
    Q2/area=1 → ["compliance", "self-custody"]   # anon-on-off-ramp 跨两类
    Q2/area=2 → rwa

失败降级: API 调用失败时打印错误到 stderr，返回码 1，不破坏 outputs 目录的其他文件。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    sys.stderr.write("需要 requests 库：pip install requests python-dotenv\n")
    sys.exit(2)

try:
    from dotenv import load_dotenv
except ImportError:
    # dotenv 缺失不致命，退化为简单 KV 解析
    def load_dotenv(path):  # type: ignore
        p = Path(path)
        if not p.exists():
            return
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


# ===== 路径相对化（关键：跨机器可移植）=====
SKILL_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = SKILL_ROOT / ".env"

# JSON line 形状（所有市场共用）
_JSON_LINE_SHAPE = (
    '{{"area":"1"|"2","handle":"@...",'
    '"posted_at":"YYYY-MM-DDTHH:MM:SSZ",'
    '"likes":N,"replies":N,"reposts":N,"text":"...",'
    '"url":"https://x.com/<handle>/status/<id>"}}'
)


# ===== 三市场 prompt 模板 =====
# 每市场 Q1（合规 + 自托管） + Q2（隐私出入金 + RWA）
# 关键词列表来自各 markets/{market}.md，此处保持同步

QUERIES = {
    # ---------- 加拿大 ----------
    "CA": {
        "Q1": {
            "tag": "tax-and-selfcustody",
            "system": (
                "You are a Canadian crypto sentiment analyst. You return real "
                "tweets with canonical URLs (https://x.com/<handle>/status/<id>). "
                "DO NOT invent tweets. If you can't find enough say so explicitly "
                "instead of filling. Follow the JSON-lines format exactly."
            ),
            "prompt": (
                "Find tweets in English (with some French Canadian / Québécois) "
                "from the last {N} days. Collect from TWO distinct AREAs, "
                "balanced ~half and half:\n\n"
                "AREA 1 — Crypto tax / compliance anxiety in Canada:\n"
                "CRA, T1135, Schedule 3, CARF, voluntary disclosure program, VDP, "
                "superficial loss rule, capital gains inclusion rate, Coinsquare "
                "data CRA, Bitbuy NDAX KYC, crypto audit Canada, 2026 capital "
                "gains, Quebec TP-1 crypto, Revenu Québec crypto, déclaration "
                "crypto Canada, ARC crypto.\n\n"
                "AREA 2 — Self-custody / leaving CEX:\n"
                "self-custody, hardware wallet, not your keys, Ledger Trezor, "
                "leave Binance Coinbase Kraken, FTX lesson, Celsius bankruptcy, "
                "Canadian exchange risk, MetaMask vs hardware, Quadrigacx, "
                "auto-garde Quebec, portefeuille matériel.\n\n"
                "Exclude retweets, shills, and 'earn with crypto' spam. For "
                "each tweet give JSON lines (one object per line, NO summary): "
                + _JSON_LINE_SHAPE +
                ". Max {M} tweets total, ordered by relevance."
            ),
        },
        "Q2": {
            "tag": "privacy-and-rwa",
            "system": (
                "You are a Canadian crypto sentiment analyst. AREA 2 has lower "
                "volume than AREA 1 — if AREA 2 has few tweets say so explicitly "
                "instead of padding with AREA 1. Real tweets only, real URLs only."
            ),
            "prompt": (
                "Find tweets in English (with some French Canadian) from the "
                "last {N} days. TWO distinct AREAs.\n\n"
                "AREA 1 — Privacy on/off-ramp / no-KYC crypto:\n"
                "buy bitcoin anonymously Canada, no-KYC crypto, P2P crypto "
                "Canada, Bisq, Bitcoin ATM Canada, Robosats, Hodl Hodl, cash to "
                "crypto, gift card crypto, Monero privacy Canada, untraceable "
                "crypto, no-KYC bridge, off-ramp privacy, convert crypto to "
                "CAD without CEX. Exclude clear shills of illegal services or "
                "mixing tutorials — only real users with privacy or tax anxiety.\n\n"
                "AREA 2 — RWA / tokenized stocks:\n"
                "RWA crypto, real world assets, tokenized stocks, on-chain "
                "stocks, xStocks, bTSLA, bAAPL, Backed Finance, Ondo Finance, "
                "USDY, tokenized ETF, S&P 500 on-chain, Tesla tokenized "
                "Kraken, 'buy US stocks without broker' from Canada, BCSC "
                "tokenized.\n\n"
                "JSON lines per tweet: " + _JSON_LINE_SHAPE +
                ". Max {M} total."
            ),
        },
    },

    # ---------- 澳大利亚 ----------
    "AU": {
        "Q1": {
            "tag": "tax-and-selfcustody",
            "system": (
                "You are an Australian crypto sentiment analyst. Real tweets "
                "only, real URLs only (https://x.com/<handle>/status/<id>). "
                "If you can't find enough, say so explicitly. Follow JSON lines."
            ),
            "prompt": (
                "Find tweets in English from the last {N} days, focus on "
                "Australian users / context. TWO distinct AREAs, balanced.\n\n"
                "AREA 1 — Crypto tax / compliance anxiety in Australia:\n"
                "ATO crypto, ATO data matching, CGT crypto, crypto capital "
                "gains tax, myTax pre-fill crypto, TD 2014/26, ATO DeFi "
                "ruling, staking tax Australia, wrap unwrap CGT, beneficial "
                "ownership crypto, 50% CGT discount, Super fund crypto $3M, "
                "CARF Australia, CoinSpot Swyftx Independent Reserve audit, "
                "crypto investor vs trader Australia.\n\n"
                "AREA 2 — Self-custody / leaving CEX (AU context):\n"
                "self-custody, hardware wallet, not your keys, Ledger Trezor, "
                "leave CoinSpot Swyftx Binance Australia, FTX Australia, "
                "Celsius bankruptcy, exchange counterparty risk, MetaMask vs "
                "hardware, AU exchange withdrawal limits, cold wallet "
                "Australia.\n\n"
                "Exclude retweets, shills, 'earn with crypto' spam. JSON "
                "lines (one object per line, no summary): "
                + _JSON_LINE_SHAPE +
                ". Max {M} tweets, ordered by relevance."
            ),
        },
        "Q2": {
            "tag": "privacy-and-rwa",
            "system": (
                "Australian crypto analyst. AREA 2 is lower volume — if few "
                "say so, don't pad. Real tweets only."
            ),
            "prompt": (
                "Find tweets in English from the last {N} days, AU focus. "
                "TWO distinct AREAs.\n\n"
                "AREA 1 — Privacy on/off-ramp in Australia:\n"
                "buy bitcoin anonymously Australia, no-KYC crypto AU, P2P "
                "crypto Australia, Bisq, Bitcoin ATM Australia, cash to "
                "crypto AU, Monero Australia, off-ramp privacy AUD, convert "
                "crypto to AUD without CEX, AUSTRAC crypto, AML crypto AU. "
                "Exclude shills of illegal services or mixers — real users "
                "with privacy or tax anxiety only.\n\n"
                "AREA 2 — RWA / tokenized stocks (AU lens):\n"
                "RWA crypto, tokenized stocks Australia, on-chain ASX, "
                "xStocks, bTSLA, bAAPL, Backed Finance, Ondo Finance, USDY, "
                "tokenized ETF Australia, S&P 500 on-chain, 'buy US stocks "
                "without broker' Australia, ASIC tokenized assets.\n\n"
                "JSON lines: " + _JSON_LINE_SHAPE + ". Max {M}."
            ),
        },
    },

    # ---------- 法国 ----------
    "FR": {
        "Q1": {
            "tag": "tax-and-selfcustody",
            "system": (
                "Tu es un analyste français de sentiment crypto. Tu retournes "
                "des tweets réels avec URLs canoniques "
                "(https://x.com/<handle>/status/<id>). N'invente PAS de "
                "tweets. Si tu n'en trouves pas assez, dis-le explicitement "
                "au lieu de remplir. Format JSON lines obligatoire."
            ),
            "prompt": (
                "Trouve des tweets en français des {N} derniers jours. "
                "Récolte depuis DEUX zones distinctes, équilibrées (~moitié "
                "moitié):\n\n"
                "ZONE 1 — Fiscalité / compliance crypto en France:\n"
                "DAC8, fiscalité crypto, impôt crypto, PFU 31,4%, flat tax "
                "crypto 2026, formulaire 3916-bis, formulaire 2086, DGFiP "
                "crypto, déclaration crypto, plus-value crypto France, "
                "PCVT, BNC crypto, cession crypto, Agence du Trésor, "
                "régularisation crypto, ravvedimento crypto, "
                "transfert résidence fiscale Portugal Malte Dubai, "
                "commercialista crypto, Waltio Koinly France, MiCA France.\n\n"
                "ZONE 2 — Auto-garde / sortir des CEX:\n"
                "auto-garde, wallet non-custodial, clé privée, portefeuille "
                "matériel, Ledger Trezor, 'pas tes clés pas tes cryptos', "
                "quitter Binance Coinbase Kraken Bitpanda Coinhouse, FTX "
                "leçon, Celsius faillite, multi-sig, MetaMask vs hardware, "
                "risque contrepartie CEX.\n\n"
                "Exclure retweets, shills, spam 'gagner avec la crypto'. "
                "Pour chaque tweet donne JSON lines (un objet par ligne, "
                "PAS de synthèse aggrégée): " + _JSON_LINE_SHAPE +
                ". Max {M} tweets totaux, ordre par pertinence."
            ),
        },
        "Q2": {
            "tag": "privacy-and-rwa",
            "system": (
                "Analyste crypto FR. ZONE 2 a moins de volume — si peu de "
                "tweets dis-le explicitement, ne remplis pas avec ZONE 1. "
                "Tweets réels uniquement."
            ),
            "prompt": (
                "Trouve des tweets en français des {N} derniers jours. "
                "DEUX zones distinctes.\n\n"
                "ZONE 1 — On-ramp/off-ramp privacy / crypto sans KYC:\n"
                "acheter bitcoin anonymement, crypto sans KYC, P2P crypto "
                "France, Bisq, Bitcoin ATM France, retrait crypto privacy, "
                "cash to crypto, carte cadeau crypto, Monero privacy, 'non "
                "traçable' crypto, bridge sans KYC, on-ramp/off-ramp privacy, "
                "convertir crypto en euros sans CEX, TRACFIN crypto. "
                "Exclure shills de services illégaux ou tutoriels de mixing/"
                "washing — seulement utilisateurs avec angoisse privacy ou "
                "doutes fiscaux réels.\n\n"
                "ZONE 2 — RWA / actions tokenisées:\n"
                "RWA crypto, real world assets, actions tokenisées, stock "
                "on-chain, xStocks, bTSLA, bAAPL, Backed Finance, Ondo "
                "Finance, USDY, ETF tokenisé, S&P 500 on-chain, Tesla "
                "tokenisé Kraken, 'acheter actions US sans courtier'.\n\n"
                "JSON lines: " + _JSON_LINE_SHAPE + ". Max {M} totaux."
            ),
        },
    },
}


# ===== API call =====

def call_grok(api_key: str, model: str, system_prompt: str, user_prompt: str,
              hours: int, max_results: int) -> dict:
    """
    POST /v1/responses + tools=[{"type":"x_search"}].
    时间窗 / 上限 / handle 白名单全部写进 prompt（Agent Tools API 不再有这些字段）。
    """
    now = dt.datetime.now(dt.timezone.utc)
    from_date = (now - dt.timedelta(hours=hours)).strftime("%Y-%m-%d")
    to_date = now.strftime("%Y-%m-%d")

    body = (
        user_prompt
        .replace("{N}", str(max(1, hours // 24)))
        .replace("{M}", str(max_results))
    )
    full_prompt = (
        system_prompt + "\n\n" + body
        + f"\n\nFinestra temporale / Time window / Fenêtre temporelle: "
        + f"{from_date} → {to_date} UTC. "
        + f"Max {max_results} tweets total."
    )

    payload = {
        "model": model,
        "tools": [{"type": "x_search"}],
        "input": full_prompt,
    }

    resp = requests.post(
        "https://api.x.ai/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def extract_answer(data: dict) -> tuple[str, list[str], list[dict]]:
    """从 /v1/responses 抽 final text + url citations + tool_call 日志."""
    final_text = ""
    tool_calls: list[dict] = []
    for item in data.get("output", []):
        t = item.get("type")
        if t in ("custom_tool_call", "tool_call"):
            tool_calls.append({
                "name": item.get("name"),
                "input": item.get("input"),
                "id": item.get("call_id") or item.get("id"),
            })
        elif "content" in item:
            for blk in item.get("content", []):
                if blk.get("type") in ("output_text", "text"):
                    final_text += blk.get("text", "")
    citations = re.findall(
        r"https?://(?:x|twitter)\.com/[^\s)\]\"]+/status/\d+", final_text
    )
    citations = list(dict.fromkeys(citations))   # dedup, keep order
    return final_text, citations, tool_calls


def parse_jsonlines(final_text: str, citations: list[str]) -> list[dict]:
    """
    Grok 应该输出 JSON lines。容错处理：
    - 抽出每一行能 json.loads 的对象
    - 缺 url 字段的尝试从 citations 回填
    - 仍缺 url 的丢弃（红线：没 URL 不入 lead）
    """
    tweets = []
    candidates_url_iter = iter(citations)
    for line in final_text.splitlines():
        line = line.strip().rstrip(",")
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        # 必填字段筛
        if not isinstance(obj, dict) or "handle" not in obj:
            continue
        # URL 回填
        url = obj.get("url") or ""
        if not url.startswith("http"):
            try:
                url = next(candidates_url_iter)
                obj["url"] = url
            except StopIteration:
                # 没 URL 直接丢
                continue
        tweets.append(obj)
    return tweets


# ===== Main =====

def main():
    parser = argparse.ArgumentParser(
        description="DeGate Multi-Market xAI Twitter scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--market", required=True, choices=["CA", "AU", "FR"],
        help="目标市场",
    )
    parser.add_argument(
        "--queries", default="Q1,Q2",
        help="跑哪些 query，逗号分隔，默认 Q1,Q2",
    )
    parser.add_argument(
        "--hours", type=int, default=72,
        help="回看时间窗（小时），默认 72",
    )
    parser.add_argument(
        "--out", default="scans/",
        help="输出目录，相对 skill 根，默认 scans/",
    )
    parser.add_argument(
        "--smoke-test", action="store_true",
        help="只发一个最小查询验证 API key 是否可用",
    )
    args = parser.parse_args()

    load_dotenv(ENV_PATH)
    api_key = os.environ.get("XAI_API_KEY", "").strip()
    if not api_key:
        sys.stderr.write(
            f"❌ XAI_API_KEY 未设置（在 {ENV_PATH} 或环境变量里设置）\n"
        )
        sys.exit(1)
    model = os.environ.get("XAI_MODEL", "grok-3-latest")
    max_results = int(os.environ.get("XAI_MAX_SEARCH_RESULTS", "25"))

    if args.smoke_test:
        try:
            data = call_grok(
                api_key, model,
                "You are a test agent.",
                "Give me 1 sample tweet about Bitcoin from the last 24 hours, "
                "JSON line format with url.",
                hours=24, max_results=1,
            )
            text, urls, _ = extract_answer(data)
            tweets = parse_jsonlines(text, urls)
            print(f"✓ xAI OK, {len(tweets)} tweet(s) returned (model={model})")
            sys.exit(0)
        except Exception as e:
            sys.stderr.write(f"❌ smoke test failed: {e}\n")
            sys.exit(1)

    market = args.market
    if market not in QUERIES:
        sys.stderr.write(f"❌ 未支持的 market: {market}\n")
        sys.exit(2)

    query_ids = [q.strip() for q in args.queries.split(",") if q.strip()]
    for qid in query_ids:
        if qid not in QUERIES[market]:
            sys.stderr.write(f"❌ 未知 query id {qid}（市场 {market}）\n")
            sys.exit(2)

    # 输出准备
    out_dir = SKILL_ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    stamp = now.strftime("%Y-%m-%d_%H%M")
    qid_suffix = "".join(query_ids)
    out_path = out_dir / (
        f"{stamp}_xai_twitter_{market.lower()}_{qid_suffix}.json"
    )

    result = {
        "schema_version": "1.0",
        "generated_at_utc": now.isoformat(),
        "market": market,
        "model": model,
        "hours": args.hours,
        "max_search_results": max_results,
        "queries": {},
    }

    any_success = False
    for qid in query_ids:
        q = QUERIES[market][qid]
        print(f"[run] market={market} query={qid} ({q['tag']})", file=sys.stderr)
        try:
            data = call_grok(
                api_key, model, q["system"], q["prompt"],
                args.hours, max_results,
            )
            text, urls, tool_calls = extract_answer(data)
            tweets = parse_jsonlines(text, urls)
            result["queries"][qid] = {
                "tag": q["tag"],
                "raw_text": text,
                "tool_calls": tool_calls,
                "citations": urls,
                "tweets": tweets,
                "tweet_count": len(tweets),
                "status": "ok",
            }
            any_success = True
            print(
                f"[ok] {qid}: {len(tweets)} tweets, "
                f"{len(urls)} URL citations, {len(tool_calls)} tool calls",
                file=sys.stderr,
            )
        except Exception as e:
            result["queries"][qid] = {
                "tag": q["tag"],
                "status": "failed",
                "error": str(e),
            }
            print(f"[fail] {qid}: {e}", file=sys.stderr)

    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[done] wrote {out_path}", file=sys.stderr)

    sys.exit(0 if any_success else 1)


if __name__ == "__main__":
    main()
