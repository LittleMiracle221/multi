---
name: degate-multi-intel
description: 每日扫描加拿大、澳大利亚、法国加密货币与个人财经社区的合规焦虑与自托管讨论，为 DeGate 多链自托管钱包找软性营销切入点。触发场景：用户说"扫 CA 舆情"、"DeGate 日报"、"加拿大加密情报"、"Australian crypto sentiment"、"CARF/T1135/ATO/DAC8 用户讨论"、"法国加密日报"、"5A 战略情报"、"找软营销切入点"，或给出 date_range + market 的扫描请求时，都应调用本技能。即使用户只说"看看加拿大 crypto 论坛有啥"、"跑一下 FR 日报"，也应触发。产出 Markdown 日报 + 结构化 JSON，覆盖每个市场的 Reddit 子版、主流 KOL 候选、本地论坛；对 Twitter/X、Telegram、Discord 的覆盖缺口诚实披露。**market 参数强制必填**，目前支持 `CA` / `AU` / `FR`；扩展新市场时在 `references/markets/` 下新增 `{xx}.md` 即可。
---

# DeGate Multi-Market Intelligence Daily

这个 skill 把"每日扫某个市场的加密舆情、筛选与 DeGate 5A 战略匹配的软性营销切入点"这套工作流固化下来，方便每天快速复用。**支持加拿大 (CA)、澳大利亚 (AU)、法国 (FR) 三个主力市场**，未来可扩展德国、西班牙、新加坡等。

## 核心架构：通用框架 + 市场插件

**共享层**（本 SKILL.md + `references/` 下的非市场文件）：
- 5A 战略定义、人设红线、DeGate 产品优势、输出规范、Self-check 机制 —— **市场中性，三国通用**

**市场插件层**（`references/markets/{xx}.md`）：
- 每个市场专属的合规催化剂（税法）、Reddit 子版、本地论坛、KOL 候选、关键词、语言
- 运行时根据 `market` 参数加载对应文件

扩展新市场 = 新增一个 `markets/{xx}.md`，主 SKILL.md 不用改。

## 核心背景（不要跳过）

**DeGate 是什么**：多链自托管钱包，提供 Swap、基于 LP 区间的做市（范围做市）、稳定币理财。定位 = Rabby/Safe 类别但面向更主流用户。

**为什么盯这三个市场**：
- 都在 2025-2027 窗口进入**强制加密数据上报阶段**，但具体催化剂不同：
  - **CA**：CARF + T1135，自托管钱包明确豁免 T1135（关键钩子）
  - **AU**：ATO 数据匹配 + CARF 集成，DeFi 按 beneficial ownership change 判断 CGT
  - **FR**：DAC8 + Flat Tax 31.4%（2026-01-01 涨），swap 不触税（反差于 CA/AU）
- 都有清晰的合规焦虑 → 自托管叙事通路，**但具体切入话术和钩子每市场不同**，见各 market 插件

**6A 战略 = 锁定的 6 类人群/话题**（三市场通用，2026-04 起从 5A 扩 6A，加入两类 frontier 话题）：
1. **合规焦虑**（本地税法催化剂，见各 market 插件）
2. **自托管意识**（CEX 风险、FTX 阴影、"not your keys not your coins"、想从交易所撤出）
3. **DEX / Swap 需求**（多链 DEX、聚合器、跨链、滑点、MEV 焦虑）
4. **稳定币理财 / 被动收益**（USDC、USDT 存哪里、DeFi 利率；FR 用户也关心 EURC）
5. **做市 / LP 收益**（Uniswap v3 区间、IL、集中流动性）
6. **Frontier 话题**（2026-04 新增，分两子类）：
   - **6a · anon-on-off-ramp**：隐私出入金、no-KYC P2P、Bisq、Bitcoin ATM、cash-to-crypto、链上可追性焦虑。**注意红线** —— 命中此类的 lead 可以扫，但 reply 严格走"事实澄清 + 自托管反框架"，绝不教"具体绕监管步骤"，详见 `narrative-compliance.md`。
   - **6b · rwa**：链上美股 / 代币化股票 / xStocks / Backed Finance / Ondo / "买美股不开券商"叙事。命中此类落 `topic_tags_5a: ["rwa"]`（沿用 schema 字段名兼容历史）。

下文中"5A"提法和 `topic_tags_5a` 字段名为兼容历史保留，实际语义按 6A 处理。

**人设与红线**（不是词汇黑名单，是操作边界）：

发出去的内容是用**普通网友的账号**发的，不是 DeGate 官方声音。所以语气完全可以像一个被 2026 新规搞烦的当地真实用户 —— 带情绪、会吐槽税务机关、会用当地俚语、会自嘲、会承认自己没搞明白某些事。**如果读起来像博客首页那种四平八稳的官宣语气，就是人设不够真。**

仍然要避免的几条（有法律 / 声誉 / 人设风险）：
- ❌ 给**具体、可操作**的"如何规避申报"步骤（这种内容被截图传播会出事）
- ❌ 说错事实 —— **每个市场的事实底线不同**，见各 market 插件和 `narrative-compliance.md`。典型易错：
  - CA：说"T1135 自托管豁免 = 不用申报 capital gains"（错，两者独立）
  - AU：说"钱包间转账不记录也没事"（错，ATO 要求能证明 beneficial ownership 未变）
  - FR：说"non-custodial 不上 3916-bis 所以不用报 capital gains"（错，两者独立）
- ❌ 把 DeGate 这个名字直接绑定在"规避 / 绕开 / 逃避"的句子里（这是唯一 DeGate 法务会真头疼的 liability）
- ❌ 暗示自己是 DeGate 员工 / 顾问 / 合作方 —— 人设是用户

可以放开的：
- ✅ 吐槽税改、吐槽税务机关（CRA / ATO / DGFiP / Revenu Québec）、表达情绪
- ✅ 讨论灰色地带（自托管在现行法规下的位置、CEX 上报的事实）
- ✅ 承认自己没严格申报、参与"要不要补申报"的真实讨论
- ✅ 比较 Rabby / Safe / MetaMask / DeGate 等钱包的 UX
- ✅ 半开玩笑、FTX 梗、"not your keys not your coins"这些社区常用梗

完整尺度和语气校准见 `references/narrative-compliance.md`。**每次写 `reply_draft` 前都要过一遍那份文档的 6 题 Self-check**（真人味、具体操作、事实性、品牌绑定、身份、对用户是否真有帮助）。

## 输入参数

每次运行时确认：

| 参数 | 默认值 | 说明 |
|---|---|---|
| `market` | **无默认，强制必填** | `CA` / `AU` / `FR`。没有隐式默认 —— 三市场占比接近（CA 50% / FR 30% / AU 20%），避免跑错。 |
| `date_range_hours` | 72 | 回看时间窗（小时）。每日日报传 24，每周盘点传 168。 |
| `language` | 按 market 推导 | CA → `en`（Quebec 场景可切 `fr`），AU → `en`，FR → `fr`。可显式覆盖。 |
| `min_heat` | 无硬阈值 | 可选的最低热度门槛（upvote / 评论数），宁缺毋滥。 |
| `topic_whitelist` | 5A 全量 | 只看某几类话题时传子集，如 `["compliance", "self-custody"]`。 |
| `topic_blacklist` | 空 | 例如 `["meme", "airdrop-farming"]`。 |
| `output_dir` | `./reports/` | Markdown + JSON 输出目录（相对路径，运行时可覆盖）。 |

## 工作流

按顺序执行。每一步都要**诚实记录发现和空档**，宁缺毋滥。

### 0. 加载市场插件

运行前**先 view** `references/markets/{market}.md`。该文件包含：
- 本市场的法规催化剂清单（具体法条、生效时间、申报表单）
- Reddit 子版和关键词组合
- 本地论坛 / 死亡频道
- KOL 名单（按领域分）
- 每个 5A 话题在本市场的具体"钩子句"示例
- 本市场特有的叙事红线（和通用 compliance 的补充）

没有市场插件就**停止** —— 不要猜测平台、催化剂或关键词。

### 1. 平台扫描

按当前市场插件里的平台表逐一扫描。**三市场的主力通道**都是 Reddit JSON API（未登录可直连）：

扫描方式：用通用 HTTP fetch 工具打 Reddit JSON API（任何 web_fetch 类工具均可，不绑定特定 MCP）。

**时效窗内（72h / week）**：
```
https://www.reddit.com/r/{subreddit}/new.json?limit=100
https://www.reddit.com/r/{subreddit}/search.json?q={keywords}&restrict_sr=1&sort=new&t=week
```

**Evergreen 候选池（必扫，不要跳过）**：用 `sort=top&t=year` 捞长期排前的老帖，支持 §2 的 evergreen lead 机制：
```
https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&restrict_sr=1&sort=top&t=year&limit=15
```
从中选 1–2 条最接近 DeGate 5A 叙事的老帖作为 evergreen lead。这是提升日报质量的关键 —— 新鲜帖只覆盖 72h 视角，evergreen 提供长尾 SEO 占位机会。

见 `scripts/reddit_scan.py` 的模板。**脚本里的 User-Agent 已改成常见浏览器字符串 + 指数退避**，降低被 Reddit 限流的风险。

**Twitter / X（通过 xAI Grok Agent Tools API，2026-04 接入）**

从 2026-04 起，三个市场都通过 xAI 的 Agent Tools API（POST `/v1/responses` + `tools: [{"type": "x_search"}]`）拉本地语推文。这取代了原来的 "Twitter coverage gap"。具体规则：

- API key 从 skill 根目录的 `.env` 读（`XAI_API_KEY=...`）。`.env` 不入库，模板见 `.env.example`。
- 默认每市场每天跑 2 条合并 query：
  - **Q1（主流）**：合规焦虑（area 1）+ 自托管 / CEX 抵触（area 2）
  - **Q2（长尾 frontier）**：anon-on-off-ramp（area 1）+ rwa（area 2）
- query prompt 用**当前 market 的语言**写（CA/AU=英语；FR=法语），具体模板放在 `markets/{market}.md` 的"xAI Twitter prompts"段
- 调用方式：`python scripts/xai_twitter_scan.py --market {CA|AU|FR} --hours 72 --out scans/`
- 脚本输出 `scans/{YYYY-MM-DD}_{HHMM}_xai_twitter_{market}.json`，含每条 tweet 的 `handle / posted_at / likes / replies / reposts / text / url / area / source_query`
- **红线**：Grok 偶尔会总结而不给原 URL —— **没有真 URL 的推文不入 lead**。URL 优先从 response 的 `output[].content[]` 文本里 regex 抽 `https://x.com/{handle}/status/{id}` 格式，仍缺就直接丢弃。
- 5A 标签映射：
  - Q1/area=1 → `compliance`
  - Q1/area=2 → `self-custody`
  - Q2/area=1 → `["compliance", "self-custody"]`（隐私出入金跨两类）
  - Q2/area=2 → `rwa`
- 失败降级：xAI 调用失败（key 失效 / 限流 / 超时）**不要让日报整体失败**：在 `coverage_gaps` 里加 `twitter_{market}_xai_failed`，§0 平台表的 X 行写具体原因，按"无 X 数据"行为继续跑
- 完整指南见 `references/xai-twitter-search.md`（含 prompt 模板细节、字段规则、合并去重策略、成本预估）

**本地论坛 / 垂类**：见当前 market 插件的"本地论坛"段。

**Telegram / Discord**：当前无 MCP 连接。记为 `coverage_gap`，不要编造内容。

**空结果 & 故障处理**（重要 —— 不自动扩窗）：
- 若目标子版在 `date_range_hours` 内无匹配帖 → **如实在报告里写"72h 内无匹配"**，**不要自动扩到 7 天凑数**。用户设的时间窗就是用户想看的时间窗，诚实 > 数据量。Evergreen 候选池是独立扫的（`sort=top&t=year`），本来就可以单独产出，不用作为"扩窗"的借口。
- 若 Reddit JSON 整体不可用（429 / blocked）→ 暂停扫描，向用户报告"Reddit 当前不可达，建议稍后重试或传入已抓取的 dump"，**不要伪造 lead**
- 若当期 72h 内无 lead 且 evergreen 也无合适老帖 → 交"空 leads 章节 + ambient themes"的日报（见 §4），ambient 本就是"没 lead 也能产出的结构性价值"。不是每一份日报都必须有 lead，空就是空。

### 2. 过滤与打分

对每条抓到的帖子，过一遍：
1. **去重**：按 post id 全局去重（同一帖子多关键词搜索会命中多次）。
2. **时间窗**：是否在 `date_range_hours` 内。**少数"常青帖"可以破例**入选，但在 lead 里标注 `evergreen: true` + 写 `evergreen_reason`（比如"该 sub 搜 'crypto tax CRA' 长期排前 5"、"这条是当前语境下最接近 DeGate 叙事的老帖，补一条深度回帖能吃长尾 SEO"）。
3. **5A 标签**：打 1～N 个标签（`compliance` / `self-custody` / `dex-swap` / `stablecoin-yield` / `lp-market-making`）。没有任何匹配则丢弃。
4. **热度**：抓 `score`（upvote）、评论数、时间；不足 `min_heat` 阈值丢弃（若有设）。
5. **soft-marketing fit**：
   - **高**：帖子正在讨论 5A 话题、评论区有提到"撤出 CEX / 找 DEX / 怎么做税务合规" + 作者有互动 → DeGate 回复能自然嵌入
   - **中**：话题相关但作者/评论区对工具推荐抵触（如"不要回复广告"），可观察不可硬推
   - **中低**：不是 5A 核心但**用户画像干净**（高净值 / 多账户管理痛点 / 多链持仓），适合轻度出现
   - **低**：只擦边，没有嵌入空间 → 丢弃

**数量节奏**：主力 sub 活跃周 4–7 条 lead 是正常的（高/中/中低/evergreen 混合），**不要为了"宁缺毋滥"把 fit=中 或 evergreen 的合理 lead 砍掉**。宁缺毋滥的真正含义是"不硬塞 fit=低 的"，不是"只保留 fit=高 的"。

### 3. 生成回复草稿 & 动作

对高 / 中 / 中低 fit 的每条 lead，产出**两件套**：

**(a) `reply_angle_zh` + `reply_draft_{lang}`**
- `reply_angle_zh`：中文说清楚这条帖子要怎么切入（回答用户问题 → 再自然带出自托管视角 → 不硬推 DeGate）
- `reply_draft_{lang}`：**按 market 的 language 参数**输出回复草稿（社区口语，不带官方腔；先回答用户具体问题，再层层带到自托管）
  - CA → `reply_draft_en`（Quebec 场景下可出 `reply_draft_fr`，在 lead 里明标）
  - AU → `reply_draft_en`
  - FR → `reply_draft_fr`
- **品牌名策略**：允许（而且鼓励）在 reply_draft 里把 DeGate 和 Rabby/Safe/MetaMask 以**并列竞品**的形式一起提（如 "Rabby, Safe, DeGate are three no-KYC options I've been trying"），这比完全不提品牌更真实。真红线是"DeGate + 避税动词直接绑定"，不是"不能出现 DeGate 三个字"。详见 `references/narrative-compliance.md`。
- **叙事 reframe**：合规帖里**正面说清"自托管 ≠ 隐藏 = 知道第三方报什么"**，这是 DeGate 的核心叙事钩子，不要绕着走。每个市场的具体钩子句见对应 market 插件。

**(b) `content_spinoff`**
- 这条 lead 能衍生出的长文 / 推文串 / 视频选题，**带标题草稿**。价值点要说清楚为什么这个选题有复用性（不只对当前 lead，对整个市场都长期有用）。

> **2026-04 起 KOL 工作流已移除**：lead 不再产 `kol_handoff` / `kol_candidates` 字段，§5 行动指南也不再有"该联系谁"板块。原因：实际运行下来，KOL 接力的 ROI 远低于直接软回帖 + 长内容 SEO 占位；KOL 名单作为"需要时人工联系的资源"留在各 market 插件的"参考名单"段里，但**不作为日报每天产出的固定动作**。

### 4. 每日主题聚类 —— "本市场持币者正在焦虑什么"

抽 **3–5 个** daily_themes。视角写成"**用户在焦虑什么**"（主体是用户、带情绪、带画像），不是"哪些叙事被讨论"（主体是内容、冷冰冰归纳）。

每个主题必须标注来源类型：
- **`lead_anchored`**：和当期 lead 直接相关，写 `related_lead_ids: ["L1", "L2"]`
- **`ambient`**：**当期没 lead 但属于结构性 / 宏观焦虑**。比如"CARF 2026-01-01 已对 CASP 生效但 r/BitcoinCA 还没炸"、"broader sub 里反复出现 Quebec 单独申报叙事（出时间窗）"、"ATO DeFi ruling 对 LP 解释模糊是垂直空位"。这类必须写 `anchor_source`（"法规 YYYY-MM-DD 生效"、"broader sub 7–14 天窗口出现 3 次"、"上月有一条 20 评论深帖"等），**不能凭空编**。

ambient themes **是这份日报最有长期价值的部分** —— 它们标记的是"论坛还没反应过来但已经发生"的市场窗口，是 DeGate 可以**抢先占位**的地方。每份日报**至少要有 1 个 ambient**，除非当期宏观层真的没新变化。

### 5. DeGate 行动指南

给出当天三个维度（**2026-04 起去掉"该联系谁"板块**，KOL 不再作为日报固定输出）：

- **该发什么长文 / 推文 / 短视频**（2–3 个主题，含标题草稿 + 对应哪条 lead 或哪个 ambient theme）
- **该去回什么帖**（列出 lead id + 建议负责人 + deadline；evergreen lead 也要列，标注"补长尾"）
- **该持续追踪什么话题**（未来 7 天 watch list，3–5 条）：
  - 每条带"为什么要追 + 可能的触发事件"
  - 可以包括**运营层动作**（如"主力 sub 所有 `crypto/tax/CARF/DAC8` 关键词新帖建议做成每日定时抓取"）

## 输出规范

**两个文件，同目录**：

1. **Markdown 日报**：`<output_dir>/<YYYY-MM-DD>_<HHMM>_<MARKET>_daily_intel.md`
2. **结构化 JSON**：`<output_dir>/<YYYY-MM-DD>_<HHMM>_<MARKET>_daily_intel.json`

时间戳用**运行时的 UTC 时间**，格式 `HHMM`（零填充，如 `0930` / `1745`）。这样同一天多次运行不会互相覆盖，排序也天然按时间。示例：`2026-04-24_0930_CA_daily_intel.md`。

Markdown 日报结构固定：

```
# 标题行（含日期 + UTC HHMM + market）

## 报告头元数据块（4–5 行）
- **时间窗口**：具体 UTC 起止
- **市场**：CA / AU / FR 之一
- **语言**：en / fr（按 market 推导或显式覆盖）
- **分析师视角**：DeGate 5A 战略（自托管叙事 + 当地合规催化剂）
- **抓取方式**：Reddit JSON 直连 + 本地关键词 WebSearch + ...

§0 平台覆盖盘点
    → 3 列表格：平台 | **画像（谁在混，带年龄层 / 讨论类型 / 焦虑度）** | 扫描结果
    → 诚实披露死频道、未连接通道（Twitter/X 本地、Telegram、Discord、本地论坛等）

§1 TL;DR — 今天最值得动手的机会（≤5 条，用 🥇🥈🥉 排序）
    允许 4 类机会混排，不只是 lead：
    - **lead**：当期高优先级帖
    - **macro**：宏观话题空窗（如 "CARF 2026 对 CA CASP 已生效但论坛还没炸"）
    - **kol_window**：KOL / 编辑的接触时机（如 "垂媒 X 刚发对口稿，本周就是窗口"）
    - **evergreen**：非 72h 但长期占搜索位的老帖，补深度回帖

§2 主市场高优先级 leads
    每条 lead 内部用两段式（**2026-04 起从三段式简化为两段式**，去掉 KOL 接力子段）：
    (a) 回帖切入角 + reply_angle_zh + reply_draft_{lang}（允许品牌并列）
    (b) 长内容选题（content_spinoff，带标题草稿）
    可以有 evergreen 标注（破时间窗的老帖，写 evergreen_reason）
    Twitter 来源的 lead `platform: "twitter"`，`heat` 字段用 `likes/replies/reposts`

§3 本市场持币者正在焦虑什么（3–5 个焦虑点）
    每条标注 type: lead_anchored | ambient
    ambient 必须写 anchor_source（法规节点 / broader sub 观察 / 上月深帖等）
    至少 1 条 ambient

§4 DeGate 行动指南
    - 该发什么（长文 / 推文 / 短视频，2–3 个选题含标题）
    - 该回什么（lead id + 负责人 + deadline，含 evergreen 占长尾）
    - 该追踪什么（3–5 条 watch list，含运营动作建议）
    （**2026-04 起去掉"该联系谁 / KOL"板块**，KOL 不再作为日报固定输出）

§5 Self-check（6 题，**每题写具体回答，不要只打 ✅**）

结尾一行：附：结构化 JSON（同目录 <...>.json）
```

JSON schema 见 `references/output-schema.md`。核心字段（关键变化：`market` 必填，`reply_draft_{lang}` 替代硬编码 `reply_draft_it`，加了 `schema_version` 字段，**去掉 `kol_handoff` / `kol_candidates` 字段**，platform 支持 `"reddit" | "twitter" | "forum"`）：
```json
{
  "schema_version": "2.1",
  "report_meta": {
    "generated_at_utc": "...",
    "date_range_hours": 72,
    "market": "CA",
    "language": "en",
    "default_params": {...},
    "coverage_gaps": ["telegram", "discord", "..."]
  },
  "tldr": [...],
  "leads": [
    {
      "id": "L1",
      "platform": "reddit",
      "language": "en",
      "reply_draft_en": "...",
      "reply_draft_fr": null,
      "content_spinoff": {...}
    }
  ],
  "daily_themes": [...],
  "action_guide": {
    "publish": [...],
    "reply": [...],
    "watch_list": [...]
  }
}
```

## Self-check（交付前必过）

在写完报告、交付前，**每题写具体回答**（不是打 ✅，而是点出这份报告里具体是怎么做到的 / 哪里有妥协）。任何一题过不去都回头改。**6 题**：

1. **真 72h 吗？** → 回答时列具体 lead id，明说哪些是 72h 内，哪些是 evergreen 破例并解释原因。例："L1/L2 严格在 72h 内；L3–L5 明确标注 evergreen 并给出长尾 SEO 价值理由。"
2. **匹配牵强吗？** → 回答时点名 fit=中低 或 evergreen 的那几条为什么仍然列出，而不是一句"没牵强"搪塞。
3. **事实性检查（market-specific）** → 针对本市场的 3 个易错事实做自查（见 `narrative-compliance.md` 的市场分节），例如："reply 里没有把 T1135 自托管豁免等同于免除 capital gains 申报义务；没有说 AU 钱包间转账完全无需记录；没有说 FR non-custodial 可以跳过 capital gains。"
4. **回帖会不会像广告？** → 回答时说明这批 reply_draft 的具体反广告手法（先共情 / 先回答问题 / 把 DeGate 放进竞品并列 / 引用竞品 Rabby/Safe 做参照）。
5. **有没有漏大平台？** → 回答时列具体盲区和原因，不是"已披露"三个字。例："Twitter/X 通过 xAI Q1+Q2 已扫，本期 ✅ N 条；Telegram/Discord 仍无 MCP；本地论坛 X 搜索引擎不吐具体帖路径。"
6. **行动指南够具体吗？** → 回答时数一下：几条回帖 + 几个内容选题 + 几条 watch list，全部带链接或草稿。

模板化的 ✅✓ 打勾视为没过。

## 参数化建议 & 未来接入

当前实现支持 `market=CA | AU | FR`；扩展其他市场（DE / ES / SG 等）时，只需在 `references/markets/` 下新增对应 `{xx}.md` 文件（按现有三个的模板结构写），主 SKILL.md 和 schema 都无需改。

计划中但未接入的能力，遇到时记 `coverage_gap`：
- Telegram MCP
- Discord MCP
- 本地封闭论坛（如 Whirlpool AU、FinanzaOnline IT 等）直接抓取
- Twitter/X 区域语种精准聚合器

## 参考文件

- `references/narrative-compliance.md` —— 人设口径、真红线（vs 语气问题）、**三市场各自的事实底线**、发布前 6 题 Self-check。**每次写 reply_draft 前都要过一遍。**
- `references/degate-advantages.md` —— DeGate 产品优势（自托管定位、内置 Swap/LP/理财、USDC 丝滑跨链等），6A 各话题下怎么自然带入。活文档，随产品迭代持续补充。
- `references/output-schema.md` —— JSON 字段完整定义 + 示例 + 校验要点。schema v2.1：含 schema_version、market/language 字段，去掉 kol 字段，platform 支持 twitter。
- `references/xai-twitter-search.md` —— **xAI Grok Agent Tools API 接入指南**（2026-04 全市场启用）：API 模板、三市场 Q1/Q2 prompt 思路、字段规则、合并去重、成本预估、失败降级。
- `references/markets/ca.md` —— **加拿大市场插件**：CARF/T1135 催化剂、r/PersonalFinanceCanada 等平台、Q1/Q2 英语 prompt、KOL 参考名单。
- `references/markets/au.md` —— **澳大利亚市场插件**：ATO 数据匹配 + CARF、r/AusFinance 等平台、Q1/Q2 英语 prompt、KOL 参考名单。
- `references/markets/fr.md` —— **法国市场插件**：DAC8 + Flat Tax 31.4%、r/vosfinances 等平台、Q1/Q2 法语 prompt、KOL 参考名单。
- `scripts/reddit_scan.py` —— Reddit JSON API 扫描模板（通用 UA + rate limit + 指数退避）。
- `scripts/xai_twitter_scan.py` —— xAI Grok Agent Tools API 调用脚本（多市场参数化，`--smoke-test` 验证 key）。
- `.env.example` —— `XAI_API_KEY` 模板。复制成 `.env` 填上 key 即用。`.env` 不入库（`.gitignore` 已挡）。
