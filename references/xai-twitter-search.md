# xAI Grok Agent Tools API — Twitter/X 多市场覆盖指南

## 为什么接这个

DeGate 多市场日报里 **Twitter/X 在 CA / AU / FR 三市场**都曾经是结构性盲区 —— WebSearch 对法语 / 本地英语推文覆盖差，没有 X API 没法直接抓真实讨论。xAI 的 **Agent Tools API**（POST `/v1/responses` + `tools: [{"type": "x_search"}]`）等效于给 Claude 配了一个能读 X 的工具：模型自主跑 `x_keyword_search` + `x_semantic_search`，把目标语种推文拉回来。

接上之后，每市场的日报 `coverage_gaps` 里就可以把 `twitter_{market}` 划掉，§2 leads 里会多出 Twitter 来源的 lead。

## API 基础

- **Endpoint**：`POST https://api.x.ai/v1/responses`（**这是 Agent Tools API，不是旧的 Live Search**；2026-01 起 `/v1/chat/completions + search_parameters` 已 deprecated）
- **Auth**：`Authorization: Bearer <XAI_API_KEY>`
- **模型**：`grok-3-latest`（默认推荐，便宜）/ `grok-4-latest`（更强推理，贵）
- **Tools**：在 body 里 `tools: [{"type": "x_search"}]`，Grok 服务端自主多轮调用 `x_keyword_search` + `x_semantic_search`
- **不再是 API 字段的**：`from_date` / `to_date` / `max_search_results` / `return_citations` —— 全都写进 prompt 里让模型解释执行

## API Key 放哪

skill 根目录的 `.env` 里：

```
XAI_API_KEY=xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
XAI_MODEL=grok-3-latest             # 可选
XAI_MAX_SEARCH_RESULTS=25           # 可选
```

`.env.example` 是占位模板，复制成 `.env` 填 key 即用。`.env` 不入库（`.gitignore` 已挡）。脚本通过相对路径 `Path(__file__).resolve().parent.parent / ".env"` 找到 key —— **不依赖任何绝对路径**，把 skill 放任何机器都能跑。

## 请求模板（Python / HTTP）

```python
import datetime as dt, requests
import os
from pathlib import Path
from dotenv import load_dotenv

# 相对于本 skill 根目录，跨机器可移植
SKILL_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(SKILL_ROOT / ".env")

resp = requests.post(
    "https://api.x.ai/v1/responses",
    headers={
        "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "grok-3-latest",
        "tools": [{"type": "x_search"}],
        "input": "Sei un analista... Trova tweet ... Finestra: dal 2026-04-21 al 2026-04-24. ...",
    },
    timeout=120,
)
data = resp.json()

# Grok 服务端自主跑了多轮 x_keyword_search / x_semantic_search
# 返回里 output[] 包含 tool_calls 日志 + 最终 message
for item in data.get("output", []):
    if item.get("type") in ("tool_call", "custom_tool_call"):
        print("tool:", item.get("name"), item.get("input"))
    elif "content" in item:
        for blk in item["content"]:
            if blk.get("type") in ("output_text", "text"):
                print(blk["text"])
```

## 每市场的 prompt 怎么写

每个市场都跑 **2 条合并 query**，每条覆盖 2 个 area：

- **Q1（主流）** — AREA 1 = 合规焦虑 / AREA 2 = 自托管 / CEX 抵触
- **Q2（长尾 frontier）** — AREA 1 = anon-on-off-ramp / AREA 2 = rwa（链上美股 / 代币化股票）

为什么合并成 2 条而不是 4 条：单条 query 塞 4 个话题会让长尾话题（隐私 / RWA）被高音量主流话题（合规）挤死；拆成"主流一对 + 长尾一对"既省调用又给长尾独立预算。

**具体语种和关键词每市场不同**，prompt 模板放在各 market 插件里：
- CA → `markets/ca.md` 的 "xAI Twitter prompts" 段（英语 + Quebec 法语关键词混入）
- AU → `markets/au.md` 同段（英语 + ATO 本地化术语）
- FR → `markets/fr.md` 同段（法语，DAC8 / 3916-bis / PFU 等本地术语）

**所有 prompt 共同的结尾约定**：

```
Per ogni tweet dammi JSON lines (un oggetto per riga, NO sintesi aggregata):
{"area":"1"|"2","handle":"@...","posted_at":"YYYY-MM-DDTHH:MM:SSZ","likes":N,"replies":N,"reposts":N,"text":"...","url":"https://x.com/.../status/..."}
Max {M} tweet totali, ordine per rilevanza.
Finestra temporale: dal {from_date} al {to_date}.
```

（上面是法/意语示意；CA/AU 用英语对应的写法见 `markets/ca.md` / `markets/au.md`。）

## 5A 标签映射（统一规则）

| query | area | 5A 标签 |
|---|---|---|
| Q1 | 1 | `compliance` |
| Q1 | 2 | `self-custody` |
| Q2 | 1 | `["compliance", "self-custody"]`（隐私出入金跨两类） |
| Q2 | 2 | `rwa` |

## 把 Grok 输出塞进日报的规则

1. **每条候选必须带 URL**：Grok 偶尔会总结而不给原 URL，**没有真链接的不入 lead**。从 `output[]` 里所有文本块用 regex 抽 `https://(x|twitter)\.com/\w+/status/\d+` 收齐 citations，再和 JSON line 里的 url 字段交叉匹配。仍缺就直接丢弃。

2. **去重 with Reddit leads**：合并时按 `url` 去重；同一事件 Reddit 和 Twitter 都有时**保留 Reddit 那条**（因为有评论语料更深），在 metadata 里记 `also_on_twitter: [url]`。

3. **Twitter lead 的字段差异**：
   - `platform: "twitter"`
   - `author` 格式 `@handle`
   - `heat` 用 `{likes, replies, reposts}` 替代 `{score, comments, upvote_ratio}`
   - 加 `source_query: "Q1" | "Q2"` 和 `source_area: "1" | "2"`
   - 加 `source_channel: "xai_grok_x_search"`

4. **TL;DR 里的 Twitter 准入门槛**：Twitter lead 只在 `likes >= 30 OR replies >= 10` 时进 §1 TL;DR，低于这个只放 §2。原因：X 上低互动推文软投放 ROI 不值回复时间。

5. **Q2/area=1（anon-on-off-ramp）的特殊处理**：
   - `topic_tags_5a: ["compliance", "self-custody"]`
   - `fit_reason` 必须说明"用户在问隐私 / 去追溯 — 我们的回帖是**澄清事实 + 自托管反框架**，不教绕监管"
   - 若帖子本身是 shill 非 KYC 服务 / mixer 教程 / 洗币技巧 → **直接丢弃，不入 lead**
   - 若帖子是用户自己困惑（"DAC8 之后该怎么办"、"Bitcoin ATM 还能用吗"） → 入 lead，reply 走澄清事实路线

## 成本预估

按默认每市场每天跑一次 Q1 + Q2，每条 max_search_results = 25：
- Grok 3 tokens：2 × (~2500 input + ~2000 output) ≈ 9000 tokens/天/市场 ≈ $0.015/天/市场
- Live search results：2 × 25 = 50 results/天/市场 × $0.025/result = $1.25/天/市场
- **每市场月成本约 $38**
- **三市场全开月成本约 $114**

可以在 `.env` 里调 `XAI_MAX_SEARCH_RESULTS` 平衡：20 → ~$30/月/市场，30 → ~$45/月/市场。

## 失败降级

如果 xAI API 调用失败（key 失效 / 限流 / 超时）：
- 脚本捕获异常**不要中断整个日报**
- 在 `coverage_gaps` 里加 `twitter_{market}_xai_failed`（如 `twitter_ca_xai_failed`），并在 §0 平台表的 X 行写具体原因（HTTP 状态码 + 时间）
- 日报 §4 / §5 按"无 X 数据"行为继续跑

## 验证 API key 可用

```bash
cd <skill_root>
python scripts/xai_twitter_scan.py --market CA --smoke-test
```

smoke-test 发一个最小查询，打印返回的 tweet 数量。返回 `✓ xAI OK, N tweets` 表示接好了。

## 输出文件名约定

脚本输出到 `<skill_root>/scans/`，文件名 pattern：

```
{YYYY-MM-DD}_{HHMM}_xai_twitter_{market}_{query_ids}.json
```

其中 `{market}` 是 `ca` / `au` / `fr` 小写，`{query_ids}` 是本次跑的 query 列表按字典序拼接。例：
- 默认跑 Q1+Q2 → `2026-04-24_0930_xai_twitter_ca_Q1Q2.json`
- 只跑 Q1 → `2026-04-24_0930_xai_twitter_ca_Q1.json`

下游消费时按 glob + mtime 找最新：

```python
import glob, json, os
candidates = glob.glob(f"scans/*_xai_twitter_{market.lower()}_*.json")
latest = max(candidates, key=os.path.getmtime)
data = json.load(open(latest))
all_queries = data["queries"]   # 已合并 Q1+Q2 后的完整数据
```

## Twitter lead 字段示例（output-schema.md 兼容）

```json
{
  "id": "L4",
  "platform": "twitter",
  "url": "https://x.com/someuser/status/1234567890",
  "language": "fr",
  "posted_at_utc": "2026-04-22T14:30:00Z",
  "author": "@someuser",
  "heat": {"likes": 187, "replies": 23, "reposts": 42},
  "source_channel": "xai_grok_x_search",
  "source_query": "Q1",
  "source_area": "1",
  "summary_zh": "...",
  "original_quote": "...",
  "topic_tags_5a": ["compliance"],
  "fit": "high",
  "fit_reason": "...",
  "evergreen": false,
  "evergreen_reason": null,
  "recommended_actions": {
    "reply_angle_zh": "...",
    "reply_draft_fr": "...",
    "reply_draft_en": null,
    "content_spinoff": {"title": "...", "value_point": "..."}
  }
}
```

## 注意事项

- xAI X 数据**有时间延迟**（通常几分钟到十几分钟），不适合秒级实时监控，但"日报级 72h 窗口"完全够用
- Grok 默认会做**总结 + 聚合**，必须在 prompt 里明确说 "dammi ogni tweet separatamente, non una sintesi" / "give each tweet separately, not a summary" / "donne-moi chaque tweet séparément, pas un résumé"
- 控制台可以看每条请求消耗了几次 x_search，**建议开 rate limit 告警在 500 result/天**
- Agent Tools API 内部多轮自主调用，单次 call 可能超 60s timeout —— 脚本已设 120s timeout
