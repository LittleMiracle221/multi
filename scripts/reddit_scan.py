#!/usr/bin/env python3
"""
Reddit OAuth API 扫描脚本 —— DeGate Multi-Market Intel Skill 专用

核心改进:
- 改走 OAuth + oauth.reddit.com，避免匿名 .json 被 403 Blocked
- 使用 Reddit 风格的唯一 User-Agent，而非伪装浏览器
- 内置 rate limit：默认请求间 sleep 2s
- 429 / 5xx 指数退避重试（最多 5 次）
- 按 post id 去重（支持多次 search 合并）
- 支持 --market 参数作为元数据标注
- 支持 --subreddits 一次传多个子版（逗号分隔），合并输出

用法:
    # 扫单个 sub 的 new
    python reddit_scan.py --subreddits PersonalFinanceCanada --mode new --market CA --out /tmp/ca.jsonl

    # 扫多个 sub + 关键词搜索（CA 合规焦虑）
    python reddit_scan.py --subreddits PersonalFinanceCanada,BitcoinCA \\
        --mode search --market CA \\
        --query 'crypto OR bitcoin OR CARF OR T1135 OR "voluntary disclosure"' \\
        --time week --out /tmp/ca.jsonl

    # 扫 FR evergreen 老帖
    python reddit_scan.py --subreddits vosfinances --mode search --market FR \\
        --query 'fiscalité crypto OR "PFU crypto" OR "3916-bis"' \\
        --time year --sort top --limit 20 --out /tmp/fr_evergreen.jsonl
"""
import argparse
import base64
import html
import json
import email.utils
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from dotenv import load_dotenv
except ImportError:
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


SKILL_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = SKILL_ROOT / ".env"

DEFAULT_SLEEP_BETWEEN_REQUESTS = 2.0  # 秒，Reddit 友好节流
MAX_RETRIES = 5
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API_BASE = "https://oauth.reddit.com"
SEARCH_BASE = "https://www.bing.com/search"
SEARCH_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

TIME_WINDOW_TO_HOURS = {
    "hour": 1,
    "day": 24,
    "week": 24 * 7,
    "month": 24 * 30,
    "year": 24 * 365,
    "all": None,
}


def get_user_agent() -> str:
    reddit_username = os.environ.get("REDDIT_USERNAME", "your_reddit_username")
    app_name = os.environ.get("REDDIT_APP_NAME", "degate-multi-intel")
    app_version = os.environ.get("REDDIT_APP_VERSION", "2.1")
    return f"python:{app_name}:{app_version} (by /u/{reddit_username})"


def build_request(url: str, *, data=None, headers=None, method=None):
    req_headers = {"User-Agent": get_user_agent()}
    if headers:
        req_headers.update(headers)
    return urllib.request.Request(
        url,
        data=data,
        headers=req_headers,
        method=method,
    )


def build_search_request(url: str):
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": SEARCH_USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )


def get_access_token() -> str:
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "缺少 REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET，请先在 .env 中配置"
        )

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8"))
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
    req = build_request(
        TOKEN_URL,
        data=body,
        headers={
            "Authorization": f"Basic {basic.decode('ascii')}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"获取 access token 失败: {payload}")
    return token


def fetch(url: str, token: str) -> dict:
    """带指数退避的 GET。遇到 429 / 5xx 自动 retry。"""
    for attempt in range(MAX_RETRIES):
        try:
            req = build_request(
                url,
                headers={
                    "Authorization": f"bearer {token}",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503, 504) and attempt < MAX_RETRIES - 1:
                # 指数退避 + 抖动
                backoff = (2 ** attempt) + random.uniform(0, 1)
                print(
                    f"[retry] HTTP {e.code} on attempt {attempt+1}, "
                    f"sleeping {backoff:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(backoff)
                continue
            raise
        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES - 1:
                backoff = (2 ** attempt) + random.uniform(0, 1)
                print(
                    f"[retry] URL error {e} on attempt {attempt+1}, "
                    f"sleeping {backoff:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(backoff)
                continue
            raise
    raise RuntimeError(f"Failed after {MAX_RETRIES} attempts: {url}")


def fetch_text(url: str) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            req = build_search_request(url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503, 504) and attempt < MAX_RETRIES - 1:
                backoff = (2 ** attempt) + random.uniform(0, 1)
                print(
                    f"[retry] search HTTP {e.code} on attempt {attempt+1}, "
                    f"sleeping {backoff:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(backoff)
                continue
            raise
        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES - 1:
                backoff = (2 ** attempt) + random.uniform(0, 1)
                print(
                    f"[retry] search URL error {e} on attempt {attempt+1}, "
                    f"sleeping {backoff:.1f}s",
                    file=sys.stderr,
                )
                time.sleep(backoff)
                continue
            raise
    raise RuntimeError(f"Failed after {MAX_RETRIES} attempts: {url}")


def extract_post(child: dict, market: str) -> dict:
    """裁剪到 skill 关心的字段，加 market 元数据。"""
    d = child.get("data", {})
    created = d.get("created_utc")
    posted_iso = (
        datetime.fromtimestamp(created, tz=timezone.utc).isoformat()
        if created else None
    )
    return {
        "id": d.get("id"),
        "market": market,
        "subreddit": d.get("subreddit_name_prefixed"),
        "title": d.get("title"),
        "author": "u/" + (d.get("author") or "[unknown]"),
        "url": "https://www.reddit.com" + (d.get("permalink") or ""),
        "posted_at_utc": posted_iso,
        "score": d.get("score"),
        "num_comments": d.get("num_comments"),
        "upvote_ratio": d.get("upvote_ratio"),
        "selftext": (d.get("selftext") or "")[:2000],
        "link_flair_text": d.get("link_flair_text"),
        "over_18": d.get("over_18"),
    }


def strip_tags(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text or "")).strip()


def normalise_reddit_url(url: str) -> Optional[str]:
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc:
        return None
    if "reddit.com" not in parsed.netloc and "redd.it" not in parsed.netloc:
        return None
    clean = parsed._replace(query="", fragment="")
    return urllib.parse.urlunparse(clean)


def parse_freshness(snippet: str, now: datetime) -> Tuple[Optional[str], Optional[str]]:
    text = " ".join(snippet.split())
    if not text:
        return None, None

    relative_patterns = [
        (r"(\d+)\s+(minute|minutes|min|mins)\s+ago", "minutes"),
        (r"(\d+)\s+(hour|hours|hr|hrs)\s+ago", "hours"),
        (r"(\d+)\s+(day|days)\s+ago", "days"),
    ]
    for pattern, unit in relative_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if not m:
            continue
        qty = int(m.group(1))
        if unit == "minutes":
            dt = now - timedelta(minutes=qty)
        elif unit == "hours":
            dt = now - timedelta(hours=qty)
        else:
            dt = now - timedelta(days=qty)
        return dt.replace(microsecond=0).isoformat(), m.group(0)

    month_pattern = (
        r"\b("
        r"Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|"
        r"Aug|August|Sep|Sept|September|Oct|October|Nov|November|Dec|December"
        r")\s+\d{1,2},\s+\d{4}\b"
    )
    m = re.search(month_pattern, text, re.IGNORECASE)
    if m:
        raw = m.group(0)
        for fmt in ("%b %d, %Y", "%B %d, %Y"):
            try:
                dt = datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc)
                return dt.isoformat(), raw
            except ValueError:
                continue

    iso_match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", text)
    if iso_match:
        raw = iso_match.group(0)
        dt = datetime.strptime(raw, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return dt.isoformat(), raw

    return None, None


def within_time_window(
    posted_iso: Optional[str],
    time_window: str,
    now: datetime,
    hours_override: Optional[int] = None,
) -> bool:
    max_hours = hours_override if hours_override is not None else TIME_WINDOW_TO_HOURS[time_window]
    if max_hours is None:
        return True
    if not posted_iso:
        return False
    try:
        posted = datetime.fromisoformat(posted_iso)
    except ValueError:
        return False
    if posted.tzinfo is None:
        posted = posted.replace(tzinfo=timezone.utc)
    age = now - posted.astimezone(timezone.utc)
    return age <= timedelta(hours=max_hours)


def extract_subreddit_from_url(url: str) -> Optional[str]:
    match = re.search(r"reddit\.com/r/([^/]+)/", url or "")
    if not match:
        return None
    return f"r/{match.group(1)}"


def extract_post_id(url: str) -> Optional[str]:
    match = re.search(r"/comments/([a-z0-9]+)/", url or "", re.IGNORECASE)
    if not match:
        return None
    return match.group(1)


def parse_bing_results(html_text: str) -> List[dict]:
    results: List[dict] = []
    for block in re.findall(r'<li class="b_algo".*?</li>', html_text, re.DOTALL):
        href_match = re.search(r'<h2><a href="([^"]+)"', block)
        title_match = re.search(r"<h2><a [^>]*>(.*?)</a>", block, re.DOTALL)
        snippet_match = re.search(r"<p>(.*?)</p>", block, re.DOTALL)
        if not href_match or not title_match:
            continue
        url = normalise_reddit_url(html.unescape(href_match.group(1)))
        if not url:
            continue
        title = strip_tags(title_match.group(1))
        snippet = strip_tags(snippet_match.group(1) if snippet_match else "")
        results.append({
            "url": url,
            "title": title,
            "snippet": snippet,
        })
    return results


def build_public_search_query(subreddit: str, user_query: str) -> str:
    return f'site:reddit.com/r/{subreddit} {user_query}'


def split_search_terms(query: str) -> List[str]:
    parts = re.split(r"\s+OR\s+", query, flags=re.IGNORECASE)
    terms: List[str] = []
    for part in parts:
        cleaned = part.strip()
        if not cleaned:
            continue
        # Keep quoted phrases intact, and avoid huge broad terms dominating results.
        if cleaned.lower() in {"crypto", "bitcoin"}:
            terms.append(f'"{cleaned}"')
        else:
            terms.append(cleaned)
    return terms or [query]


def parse_rss_items(xml_text: str) -> List[dict]:
    items: List[dict] = []
    for block in re.findall(r"<item>(.*?)</item>", xml_text, re.DOTALL):
        def grab(tag: str) -> str:
            match = re.search(rf"<{tag}>(.*?)</{tag}>", block, re.DOTALL)
            return html.unescape(match.group(1).strip()) if match else ""

        items.append({
            "title": grab("title"),
            "url": normalise_reddit_url(grab("link")),
            "snippet": grab("description"),
            "pub_date": grab("pubDate"),
        })
    return [item for item in items if item["url"]]


def scan_public_search(
    subreddit: str,
    query: str,
    time_window: str,
    limit: int,
    market: str,
    hours_override: Optional[int] = None,
) -> list:
    now = datetime.now(timezone.utc)
    fetch_count = min(max(limit * 2, 10), 25)
    terms = split_search_terms(query)

    posts = []
    seen_ids = set()
    for term in terms:
        q = build_public_search_query(subreddit, term)
        search_url = (
            f"{SEARCH_BASE}?format=rss&q={urllib.parse.quote(q)}"
            f"&count={fetch_count}&setlang=en-US&ensearch=1"
        )
        rss_text = fetch_text(search_url)
        parsed_results = parse_rss_items(rss_text)

        for item in parsed_results:
            post_url = item["url"]
            post_id = extract_post_id(post_url)
            if not post_id or post_id in seen_ids:
                continue

            posted_iso = None
            freshness_hint = None
            if item.get("pub_date"):
                try:
                    dt = email.utils.parsedate_to_datetime(item["pub_date"])
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    posted_iso = dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()
                    freshness_hint = item["pub_date"]
                except (TypeError, ValueError):
                    posted_iso = None
            if not posted_iso:
                posted_iso, freshness_hint = parse_freshness(item["snippet"], now)

            if not within_time_window(posted_iso, time_window, now, hours_override):
                continue

            seen_ids.add(post_id)
            posts.append({
                "id": post_id,
                "market": market,
                "subreddit": extract_subreddit_from_url(post_url) or f"r/{subreddit}",
                "title": item["title"],
                "author": "u/[unknown]",
                "url": post_url,
                "posted_at_utc": posted_iso,
                "score": None,
                "num_comments": None,
                "upvote_ratio": None,
                "selftext": item["snippet"][:2000],
                "link_flair_text": None,
                "over_18": None,
                "source": "public_search",
                "freshness_hint": freshness_hint,
                "source_query": term,
            })
            if len(posts) >= limit:
                return posts

    return posts


def scan_new(subreddit: str, limit: int, market: str, token: str) -> list:
    url = f"{API_BASE}/r/{subreddit}/new?limit={limit}&raw_json=1"
    data = fetch(url, token)
    return [extract_post(c, market) for c in data.get("data", {}).get("children", [])]


def scan_search(
    subreddit: str,
    query: str,
    time_window: str,
    sort: str,
    limit: int,
    market: str,
    token: str,
) -> list:
    q = urllib.parse.quote(query)
    url = (
        f"{API_BASE}/r/{subreddit}/search"
        f"?q={q}&restrict_sr=1&sort={sort}&t={time_window}&limit={limit}&raw_json=1"
    )
    data = fetch(url, token)
    return [extract_post(c, market) for c in data.get("data", {}).get("children", [])]


def main():
    load_dotenv(ENV_PATH)
    ap = argparse.ArgumentParser(
        description="DeGate Multi-Market Intel Reddit scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--subreddits",
        required=True,
        help=(
            "Subreddit 名（无 r/ 前缀）；逗号分隔可传多个，"
            "例 `PersonalFinanceCanada,BitcoinCA`"
        ),
    )
    ap.add_argument(
        "--market",
        required=True,
        choices=["CA", "AU", "FR"],
        help="市场代码（将作为元数据写入每条 post）",
    )
    ap.add_argument(
        "--mode", choices=["new", "search"], default="new",
        help="new=按时间倒序；search=按关键词",
    )
    ap.add_argument(
        "--query", default="",
        help="mode=search 时的关键词，支持 OR / 引号（例 'crypto OR bitcoin OR CARF'）",
    )
    ap.add_argument(
        "--time", dest="time_window",
        choices=["hour", "day", "week", "month", "year", "all"],
        default="week",
    )
    ap.add_argument(
        "--sort", choices=["new", "top", "hot", "relevance"], default="new",
        help="search 模式的排序；evergreen 捞老帖建议用 top",
    )
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument(
        "--sleep", type=float, default=DEFAULT_SLEEP_BETWEEN_REQUESTS,
        help=f"请求间隔秒数（默认 {DEFAULT_SLEEP_BETWEEN_REQUESTS}，Reddit 友好）",
    )
    ap.add_argument(
        "--out", default="-",
        help="JSONL 输出路径；- 表示 stdout",
    )
    ap.add_argument(
        "--transport",
        choices=["auto", "oauth", "public-search"],
        default="auto",
        help="抓取通道：oauth / public-search / auto（默认）",
    )
    ap.add_argument(
        "--date-range-hours",
        type=int,
        default=None,
        help="可选：按小时精确过滤时间窗，适合 public-search 的 72h 模式",
    )
    args = ap.parse_args()

    subs = [s.strip() for s in args.subreddits.split(",") if s.strip()]
    if not subs:
        print("--subreddits 解析为空", file=sys.stderr)
        sys.exit(2)

    if args.mode == "search" and not args.query:
        print("mode=search 时必须传 --query", file=sys.stderr)
        sys.exit(2)

    token = None
    if args.transport in ("auto", "oauth"):
        try:
            token = get_access_token()
        except Exception as e:
            if args.transport == "oauth":
                print(f"[auth error] {e}", file=sys.stderr)
                sys.exit(1)
            print(f"[auth warn] OAuth 不可用，准备回退 public-search: {e}", file=sys.stderr)

    all_posts: list = []
    seen_ids: set = set()

    for i, sub in enumerate(subs):
        try:
            if args.transport == "public-search" or (args.transport == "auto" and token is None):
                if args.mode != "search":
                    raise RuntimeError("public-search 仅支持 mode=search")
                posts = scan_public_search(
                    sub, args.query, args.time_window, args.limit, args.market, args.date_range_hours,
                )
            elif args.mode == "new":
                posts = scan_new(sub, args.limit, args.market, token)
            else:
                posts = scan_search(
                    sub, args.query, args.time_window,
                    args.sort, args.limit, args.market, token,
                )
        except Exception as e:
            if args.transport == "auto" and token is not None and args.mode == "search":
                err_text = str(e)
                if "HTTP Error 403" in err_text or "HTTP Error 429" in err_text:
                    print(
                        f"[scan warn] r/{sub}: OAuth/Reddit blocked, fallback public-search",
                        file=sys.stderr,
                    )
                    try:
                        posts = scan_public_search(
                            sub, args.query, args.time_window, args.limit, args.market, args.date_range_hours,
                        )
                    except Exception as fallback_err:
                        print(f"[scan error] r/{sub}: {fallback_err}", file=sys.stderr)
                        continue
                else:
                    print(f"[scan error] r/{sub}: {e}", file=sys.stderr)
                    continue
            else:
                print(f"[scan error] r/{sub}: {e}", file=sys.stderr)
                continue

        new_count = 0
        for p in posts:
            pid = p.get("id")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)
            all_posts.append(p)
            new_count += 1

        print(
            f"[scan ok] r/{sub}: {len(posts)} posts, {new_count} new after dedup",
            file=sys.stderr,
        )

        # Rate limit（最后一个不用 sleep）
        if i < len(subs) - 1:
            time.sleep(args.sleep)

    # 输出
    out = sys.stdout if args.out == "-" else open(args.out, "w", encoding="utf-8")
    try:
        for p in all_posts:
            out.write(json.dumps(p, ensure_ascii=False) + "\n")
    finally:
        if out is not sys.stdout:
            out.close()

    print(
        f"[done] market={args.market} total={len(all_posts)} "
        f"unique posts across {len(subs)} subreddit(s)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
