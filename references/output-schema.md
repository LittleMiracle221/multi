# Output JSON Schema —— 日报结构化字段完整定义

## 版本

当前 schema version：**`2.1`**

- `1.x`：原 IT 单市场版，硬编码 `reply_draft_it` 字段、无 `market` / `language` 字段
- `2.0`：多市场版，加 `schema_version` / `market` / `language` 字段，`reply_draft_{lang}` 按语言展开
- **`2.1`（当前）**：去掉 `kol_handoff` / `kol_candidates` 字段（KOL 工作流 2026-04 移除）；`platform` 字段支持 `"twitter"` 取值；`topic_tags_5a` 扩展 `"anon-on-off-ramp"` 和 `"rwa"`；Twitter lead 用 `heat: {likes, replies, reposts}` 替代 `heat: {score, comments, upvote_ratio}`；新增 `source_channel` / `source_query` / `source_area` 字段标识 xAI 来源。

JSON 文件根对象**必须**带 `schema_version` 字段，便于未来演进时做迁移。

## 顶层结构

```json
{
  "schema_version": "2.1",
  "report_meta": { ... },
  "tldr": [ ... ],
  "leads": [ ... ],
  "daily_themes": [ ... ],
  "action_guide": { ... },
  "narrative_compliance": { ... }
}
```

## `report_meta`

报告元数据。

```json
{
  "report_meta": {
    "generated_at_utc": "2026-04-24T09:30:00Z",
    "date_range_hours": 72,
    "market": "CA",
    "language": "en",
    "default_params": {
      "min_heat": null,
      "topic_whitelist": ["compliance", "self-custody", "dex-swap", "stablecoin-yield", "lp-market-making", "anon-on-off-ramp", "rwa"],
      "topic_blacklist": [],
      "output_dir": "./reports/"
    },
    "coverage_gaps": [
      "telegram",
      "discord"
    ],
    "coverage_newly_covered": [
      "twitter_x_ca_via_xai_agent_tools_api"
    ],
    "scan_stats": {
      "reddit": [
        {"channel": "r/PersonalFinanceCanada new", "method": "reddit_json_api", "posts_seen": 100, "keyword_matches_72h": 3}
      ],
      "xai_twitter": {
        "api_endpoint": "POST https://api.x.ai/v1/responses",
        "tools_used": [{"type": "x_search"}],
        "queries_run": ["Q1", "Q2"],
        "tweets_returned": {"Q1": 4, "Q2": 6}
      }
    },
    "time_window_note": null
  }
}
```

**字段说明**：
- `market`：必填，`"CA" | "AU" | "FR"`（或未来扩展的市场代码）
- `language`：必填，`"en" | "fr"`（主要回复语言）
- `topic_whitelist` 默认值含全部 6A 类别（5 个原始 + `anon-on-off-ramp` + `rwa`）
- `coverage_gaps`：数组，列出本次运行未覆盖的通道
- `coverage_newly_covered`：本期相对前几期新接入的通道（如 xAI Twitter 首次跑通时）
- `scan_stats`：每个 channel 的细节统计（看了多少帖、命中多少），便于审计和调优
- `time_window_note`：如需标注本次运行的特殊情况（如"Reddit 当前 429 扫描受限"、"72h 内无匹配帖"），在这里说明，否则 `null`。**不用于自动扩窗**（本 skill 不做自动扩窗，无匹配就写 null/无匹配）

**coverage_gaps 命名原则（2026-04 从 italy_intel 同步）**：
- 固定 gap：能力尚未接入，如当前的 `telegram`、`discord`
- 条件性 gap：能力已接入，但本期运行失败，如 `twitter_ca_xai_failed`
- 这两类不要混写。未来 Telegram 真接入 AU / CA / FR 后，应把固定 `telegram` 替换成对应市场的运行失败命名，而不是两者并存。

## `tldr`

今天最值得动手的机会（≤5 条）。

```json
{
  "tldr": [
    {
      "rank": 1,
      "opportunity_type": "lead",
      "one_liner": "L1: r/PersonalFinanceCanada OP 正在吵 CRA 审计通知 + CoinSquare 数据，评论区已有 3 个用户说要撤 CEX —— 自托管回复能自然嵌入",
      "related_lead_id": "L1"
    },
    {
      "rank": 2,
      "opportunity_type": "macro",
      "one_liner": "CARF 对 Canadian CASP 的 2026-01-01 数据收集已启动但 r/BitcoinCA 还没集中讨论 —— 抢占长尾关键词窗口",
      "related_lead_id": null
    }
  ]
}
```

**字段说明**：
- `rank`：1–5 整数
- `opportunity_type`：枚举 `"lead" | "macro" | "kol_window" | "evergreen"`
- `related_lead_id`：若 `opportunity_type="lead"` 或 `"evergreen"` 必填指向 `leads` 数组里的某个 id；否则 `null`

## `leads`

主市场高优先级 lead 列表。**2026-04 起两段式（reply + content_spinoff）**，已删除 KOL 接力字段。

```json
{
  "leads": [
    {
      "id": "L1",
      "priority_rank": 1,
      "platform": "reddit",
      "url": "https://www.reddit.com/r/PersonalFinanceCanada/comments/xxxxx/",
      "language": "en",
      "posted_at_utc": "2026-04-23T14:12:00Z",
      "author": "u/example_user",
      "heat": {
        "score": 87,
        "comments": 42,
        "upvote_ratio": 0.91
      },
      "summary_zh": "OP 被 CRA 发了关于 2021-2022 CEX 活动的审核信，问社区要不要主动补申报、以及之后应不应该继续把币放 CEX",
      "original_quote": "Got a letter from CRA asking about my Coinsquare activity from 2021. I didn't report any of the gains back then (was small, like $4k). Should I do a Voluntary Disclosure now or just wait? Also thinking I should move what's left off CEX entirely.",
      "topic_tags_5a": ["compliance", "self-custody"],
      "fit": "high",
      "fit_reason": "OP 主动说要撤出 CEX + 评论区已有讨论自托管选项，DeGate 回复可以非常自然嵌入。作者活跃在评论区。",
      "evergreen": false,
      "evergreen_reason": null,
      "source_channel": "reddit_json_api",
      "source_query": null,
      "source_area": null,
      "recommended_actions": {
        "reply_angle_zh": "先共情（被 CRA 通知谁都慌）+ 分享 Voluntary Disclosure Program 的事实性信息 + 自然带出'之后自托管 + 干净记录' 的视角，提 Rabby/Safe/DeGate 作为并列选项",
        "reply_draft_en": "That CRA letter feeling is awful, sorry you're dealing with it. VDP is usually the right move if you genuinely underreported — getting ahead of it vs waiting for a full audit almost always works out better. Accountant will know the timing cutoffs.\n\nOn moving off CEX — I made the same call last year. Been using a mix of Rabby, Safe, and DeGate for multi-chain stuff. What I'd say is: self-custody doesn't change your reporting obligation (Schedule 3 still applies to any disposal), but it DOES mean your records stay under your own control — no more CEX sending data to CRA that you forgot about. For the CARF stuff coming in, that CEX visibility is only going up.",
        "reply_draft_fr": null,
        "content_spinoff": {
          "title": "T1135 vs Schedule 3 vs VDP: Three Different Things Canadian Crypto Holders Keep Mixing Up",
          "value_point": "这三个概念每个月都在 r/PersonalFinanceCanada / r/BitcoinCA 被混淆，一篇清晰拆解的长文能吃长尾搜索流量 + 可作为未来 reply 里的引用资源。"
        }
      }
    },
    {
      "id": "L4",
      "priority_rank": 3,
      "platform": "twitter",
      "url": "https://x.com/someuser/status/1234567890",
      "language": "fr",
      "posted_at_utc": "2026-04-22T14:30:00Z",
      "author": "@someuser",
      "heat": {"likes": 187, "replies": 23, "reposts": 42},
      "summary_zh": "用户在质疑 ID numérique × wallet 联动后的资产主权",
      "original_quote": "Avec l'ID numérique européen lié au wallet, on parle vraiment de propriété privée encore?",
      "topic_tags_5a": ["self-custody", "compliance"],
      "fit": "high",
      "fit_reason": "本期 xAI Q1/area=2 engagement 冠军，自托管叙事最自然的接入点",
      "evergreen": false,
      "evergreen_reason": null,
      "source_channel": "xai_grok_x_search",
      "source_query": "Q1",
      "source_area": "2",
      "recommended_actions": {
        "reply_angle_zh": "认同问题严肃 + 区分 ID 链入和 wallet 主权两件事 + 提自托管多 wallet 是缓冲",
        "reply_draft_fr": "C'est une vraie question. ID numérique lié au wallet ≠ wallet custodié, mais la frontière devient floue dès que le KYC se branche en amont. Pour ceux qui veulent garder un buffer, Rabby, Safe, DeGate sont trois wallets non-custodial multi-chaînes que tu peux faire vivre en parallèle de tout système ID — ça change rien à tes obligations 2086 / 3916-bis, mais ça te garde la main.",
        "reply_draft_en": null,
        "content_spinoff": {
          "title": "ID numérique européen et auto-garde: ce qui change vraiment pour ton wallet en 2026",
          "value_point": "ID numérique × wallet 是法语圈未来 18 个月的高频焦虑话题，目前 IPF / vosfinances 的讨论密度都还低，DeGate 出一篇深度法语长文可以占长尾。"
        }
      }
    }
  ]
}
```

**字段说明**：
- `id`：`L1`, `L2`, ...（全报告唯一）
- `platform`：枚举 `"reddit" | "twitter" | "forum" | "other"`
- `language`：原帖语言
- `heat`：
  - Reddit：`{score, comments, upvote_ratio}`
  - Twitter：`{likes, replies, reposts}` —— 字段名不同
  - 其他来源可省略字段
- `topic_tags_5a`：枚举数组，子集来自 7 个值：`["compliance", "self-custody", "dex-swap", "stablecoin-yield", "lp-market-making", "anon-on-off-ramp", "rwa"]`（字段名为兼容历史保留 `_5a` 后缀，实际是 6A）
- `fit`：枚举 `"high" | "medium" | "medium_low"`（`"low"` 不应出现在输出里 —— 在第 2 步过滤时就丢掉了）
- `evergreen`：布尔值。若 `true`，`evergreen_reason` 必填
- `source_channel`：枚举 `"reddit_json_api" | "xai_grok_x_search" | "websearch_forum" | "other"`
- `source_query`：xAI 来源时填 `"Q1"` / `"Q2"`，其他来源填 `null`
- `source_area`：xAI 来源时填 `"1"` / `"2"`，其他来源填 `null`
- `reply_draft_en` / `reply_draft_fr`：按 `language` 字段填，不相关的填 `null`（**不要删字段**，保持 schema 稳定）
- `content_spinoff`：对象，含 `title` + `value_point`
- **已移除字段**：`kol_handoff`、`kol_candidates`（v2.1 起删除，KOL 工作流不再作为日报固定输出）

**未来 Telegram 接入规则（文档先行，当前尚未启用）**：
- Telegram 一旦接入，不应新增一套平行 schema，而应沿用 `leads` 的同一对象结构。
- 建议的 `heat` 子字段为：`{views, forwards, replies, reactions_total}`。
- `platform` 届时扩展为 `"telegram"`，并要求 `url` 必须为真实可打开链接。
- Telegram 和 Twitter 同属流式平台，默认 `evergreen=false`。

## `secondary_market` （可选）

某些情况下会扫次级市场对照（如 CA 主扫时顺带看 r/CryptoTax EN 层）。结构和 `leads` 一致，再加：

```json
{
  "secondary_market": {
    "market_code": "EN_global",
    "leads": [ ... ],
    "scanned_scope": ["r/CryptoTax", "r/CryptoCurrency"],
    "scanned_keywords": ["CRA", "canadian", "CARF"],
    "future_timing_note": "等 CARF 对 G20 全面生效（2027 窗口）再重扫"
  }
}
```

若本次没扫次级市场，整个 `secondary_market` 键可省略。

## `daily_themes`

"持币者正在焦虑什么"的主题聚类（3–5 条）。

```json
{
  "daily_themes": [
    {
      "theme_id": "T1",
      "title_zh": "VDP 要不要做 —— 加拿大散户的 CRA 通知恐慌",
      "type": "lead_anchored",
      "related_lead_ids": ["L1", "L3"],
      "anchor_source": null,
      "one_liner": "2021 牛市期间的未申报收益，现在正被 CRA 精准通知；散户在纠结主动补申报 vs 赌不被抽中"
    },
    {
      "theme_id": "T2",
      "title_zh": "Quebec TP-1 加密问题的空白地带",
      "type": "ambient",
      "related_lead_ids": [],
      "anchor_source": "Quebec 自 2024 税年起在 TP-1 加了单独加密问题；r/Quebec 和 r/PersonalFinanceCanada 过去 30 天无专题帖讨论，但 Revenu Québec 指引链接 3 月刚更新过",
      "one_liner": "Quebec 法语用户对 federal + provincial 双重加密申报的困惑是结构性空位，DeGate 可以抢占法语长尾"
    }
  ]
}
```

**字段说明**：
- `type`：枚举 `"lead_anchored" | "ambient"`
- `related_lead_ids`：`lead_anchored` 必填，`ambient` 必须为 `[]` 或 `null`
- `anchor_source`：`ambient` 必填（法规节点 / broader sub 观察 / 上月深帖等），**不能凭空**
- **每份日报至少 1 条 `ambient`**（除非宏观层真无新变化）

## `action_guide`

DeGate 行动指南。**2026-04 起去掉 `kol_outreach` 块**，KOL 不再作为日报固定输出。

```json
{
  "action_guide": {
    "publish": [
      {
        "format": "long_form",
        "title": "T1135 vs Schedule 3 vs VDP: ...",
        "related_ids": ["L1", "T1"],
        "one_liner_zh": "拆解三个被混淆的加拿大加密税概念，面向 CA 散户，吃长尾 SEO"
      }
    ],
    "reply": [
      {
        "lead_id": "L1",
        "assigned_to": "social_team_member_A",
        "deadline_utc": "2026-04-25T00:00:00Z",
        "note": "主力回复；作者还在评论区活跃"
      },
      {
        "lead_id": "L4",
        "assigned_to": "social_team_member_B",
        "deadline_utc": "2026-04-27T00:00:00Z",
        "note": "evergreen 长尾占位，优先级较低但务必补一条高质量深度回帖"
      }
    ],
    "watch_list": [
      {
        "topic": "CARF 生效日期的官方确认（2026 vs 2027）",
        "why": "目前来源有分歧，一旦 CRA 发布明确时间表会引爆一轮 Reddit 讨论",
        "trigger_to_watch_for": "CRA 官网 CARF 专题页更新、Finance Canada 公告、CRA commissioner 媒体发言"
      },
      {
        "topic": "r/PersonalFinanceCanada 所有 'crypto/CRA/T1135/CARF' 关键词",
        "why": "主力 sub，应做成每日定时抓取",
        "trigger_to_watch_for": "建议运营层每天 UTC 09:00 自动跑 reddit_scan.py，输出 JSONL 给本 skill"
      }
    ]
  }
}
```

**字段说明**：
- `publish[].format`：枚举 `"long_form" | "tweet_thread" | "short_video" | "op_ed"`
- `reply[].deadline_utc`：ISO 8601 UTC
- `watch_list[]`：3–5 条；每条必带 `why` + `trigger_to_watch_for`
- **已移除字段**：`kol_outreach[]`（v2.1 起删除）

## `narrative_compliance`

Self-check 的结构化自评结果。

```json
{
  "narrative_compliance": {
    "self_check_results": [
      {
        "question": "真 72h 吗？",
        "pass": true,
        "answer": "L1/L2/L3 严格 72h 内；L4/L5 明确标注 evergreen 并给出长尾 SEO 价值理由"
      },
      {
        "question": "匹配牵强吗？",
        "pass": true,
        "answer": "L5 evergreen 明确是因为 sub 里搜 'voluntary disclosure crypto' 长期排前 3，不是凑数"
      },
      {
        "question": "事实性检查（market-specific）",
        "pass": true,
        "answer": "reply 里区分了 T1135 豁免 vs Schedule 3 申报义务；CARF 日期用的 'likely 2026 or 2027' 而非武断单日期；Quebec TP-1 只对 Quebec 用户提"
      },
      {
        "question": "回帖会不会像广告？",
        "pass": true,
        "answer": "4 条 reply 都先共情 / 先回答 OP 的具体问题再带出视角；品牌并列提法（Rabby/Safe/DeGate）而非单推 DeGate"
      },
      {
        "question": "有没有漏大平台？",
        "pass": false,
        "answer": "Twitter/X 加拿大英语和法语内容因 WebSearch 区域限制未覆盖；Telegram/Discord 无 MCP；Bitbuy/NDAX 官方博客评论区未手动查"
      },
      {
        "question": "行动指南够具体吗？",
        "pass": true,
        "answer": "4 条回帖（带 deadline + 负责人）+ 2 个长内容选题（带标题草稿）+ 2 位 KOL（带接触方式）+ 3 条 watch list"
      }
    ]
  }
}
```

**字段说明**：
- `self_check_results`：**6 项数组**，和 SKILL.md §5 的 6 题对齐
- 每项 `pass` 可以是 `false`（诚实披露没过的地方，比下次改进）
- 所有 `answer` **不能是模板化 ✅/✓ 或一句话**，必须点到具体做法 / 具体妥协

## 校验要点

运行时建议在写文件前做一遍 schema 校验，检查：

1. `schema_version` 字段存在且值为 `"2.1"`
2. `report_meta.market` 是已知市场代码
3. 每条 `lead` 的 `language` 和 `reply_draft_{lang}` 的填充一致（language="en" → reply_draft_en 非空、reply_draft_fr=null）
4. 每条 `evergreen=true` 的 lead 有非空 `evergreen_reason`
5. 每条 `type="ambient"` 的 theme 有非空 `anchor_source`
6. `daily_themes` 至少 1 条 `ambient`（除非宏观层真无新）
7. `narrative_compliance.self_check_results` 长度 == 6
8. 所有 `tldr[].related_lead_id` 指向存在的 lead id
9. **不应再出现** `kol_handoff` / `kol_candidates` / `action_guide.kol_outreach` 字段（v2.1 已删）
10. Twitter 来源 lead（platform="twitter"）必须有 `source_query` ∈ `["Q1","Q2"]` 和 `source_area` ∈ `["1","2"]`

简单的 Python 校验 snippet：

```python
import json, sys

def validate(path):
    with open(path) as f:
        d = json.load(f)
    assert d.get("schema_version") == "2.1", "schema_version must be 2.1"
    assert d["report_meta"]["market"] in ("CA", "AU", "FR"), "unknown market"
    lead_ids = {L["id"] for L in d.get("leads", [])}
    for t in d.get("tldr", []):
        if t["opportunity_type"] in ("lead", "evergreen"):
            assert t["related_lead_id"] in lead_ids
    for L in d.get("leads", []):
        assert "kol_handoff" not in L["recommended_actions"], \
            f"{L['id']} still has deprecated kol_handoff field"
        if L["evergreen"]:
            assert L.get("evergreen_reason"), f"{L['id']} evergreen but no reason"
        lang = L["language"]
        assert L["recommended_actions"].get(f"reply_draft_{lang}"), \
            f"{L['id']} missing reply_draft_{lang}"
        if L["platform"] == "twitter":
            assert L.get("source_query") in ("Q1", "Q2"), \
                f"{L['id']} twitter lead missing source_query"
            assert L.get("source_area") in ("1", "2"), \
                f"{L['id']} twitter lead missing source_area"
    ambient = [t for t in d.get("daily_themes", []) if t["type"] == "ambient"]
    assert len(ambient) >= 1 or d["report_meta"].get("ambient_waived_reason"), \
        "need at least 1 ambient theme"
    assert "kol_outreach" not in d["action_guide"], \
        "action_guide.kol_outreach is deprecated in v2.1"
    assert len(d["narrative_compliance"]["self_check_results"]) == 6
    print(f"[ok] {path}")

if __name__ == "__main__":
    validate(sys.argv[1])
```

运行：`python -m scripts.validate <report.json>`（待后续补入 `scripts/` 目录）。
