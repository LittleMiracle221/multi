# Market Plugin: 🇨🇦 Canada (CA)

**市场优先级**：约 50%（三市场最重）
**主语言**：`en`（默认）；`fr` 用于 Quebec 场景
**时区参考**：UTC-5（ET） / UTC-8（PT）
**税务机关**：CRA（Canada Revenue Agency）+ Revenu Québec（Quebec 特殊）

---

## 1. 法规催化剂（Compliance 话题的钩子清单）

### 核心催化剂（按紧迫度排序）

| 催化剂 | 生效时间 | 影响 | 用户焦虑点 |
|---|---|---|---|
| **CARF（Crypto-Asset Reporting Framework）** | **2026-01-01（CRA 文件）或 2027-01-01（部分 CPA 来源说推迟）** | 所有 Canadian CASP（Bitbuy、Coinsquare、NDAX、Newton、Shakepay 等）必须向 CRA 收集并上报用户身份 + 交易数据；CRA 再与其他 CARF 国家交换 | "我 2021 牛市没申报的那些小额 gain，现在 CRA 会不会知道？要不要 VDP？" |
| **T1135（Foreign Income Verification Statement）** | 长期有效 | 境外加密资产**总成本**（不是市值）在年内任何时点 > $100,000 CAD 需申报。**Canadian-situs CSA 注册平台 + 自托管钱包明确豁免 T1135**（CRA 2019 指引） | "我在 Binance / Kraken（非 CA 实体）的币算 specified foreign property 吗？" |
| **Capital Gains Inclusion Rate 改革** | 2026-01-01 生效 | 前 $250k capital gain 仍 50% 包含率，超过 $250k 部分 **66.67%** 包含率 | "我今年大 exit 是不是要在 $250k 以下分批做 disposition？" |
| **Schedule 3（Capital Gains/Losses）** | 每年 T1 申报 | 任何 disposition（卖、swap、买商品、赠与）都要报；**和 T1135 独立**，不因自托管豁免 | "crypto-to-crypto swap 要不要报？" 要 |
| **Form T2125（Business Income）** | 每年 | 若 CRA 认定你是 trader 而非 investor，按 100% 包含率征业务收入税 | "我日内交易频繁会不会被重分类？" |
| **VDP（Voluntary Disclosure Program）** | 长期开放 | 主动补报漏报可减免部分罚款和利息；但一旦 CRA 已启动 audit 就失效 | "2021-2022 漏报的现在补还来得及吗？" |
| **Superficial Loss Rule** | 长期 | 30 天内回购同一资产不能 claim loss（和美国 wash sale 类似但术语不同） | "止损后多久可以回购？" |
| **Quebec TP-1 加密问题** | **2024 税年起** | Quebec 居民 TP-1 表有单独加密资产问题（"Have you held, acquired, or used crypto-assets?"），独立于 federal T1 | "我住 QC，federal 报了还要在 TP-1 再答一次？" 要 |
| **CEX 历史数据命令** | Coinsquare 2021 / Dapper Labs 2025-09 | 联邦法院强制 CEX 交用户数据给 CRA | "CRA 已经有我过去的数据了吗？" |

### Compliance 话题下的核心钩子（DeGate 叙事切入点）

**最强钩子：T1135 自托管豁免**
- 真实事实：CRA 2019 指引明确，通过 CSA 注册的 Canadian 平台持有的加密，以及**用户自己控制私钥的自托管加密**，不视为 "specified foreign property"，不触发 T1135 申报。
- **但必须同时说清**：这不免除 Schedule 3 的 capital gains 申报义务（任何 disposition 还是要报）。
- 叙事转化：从"我怕 T1135 复杂"→"自托管 + Canadian-situs 简化 T1135 流程，但你该填的 Schedule 3 还是要填"

**次强钩子：CARF 让 CEX 可见性骤升 → 自托管是干净记录的选择**
- 不是"自托管让 CRA 看不到你"（这错），而是"CEX 今后会上报得更多，你自己维护的 self-custody 记录反而更可控 / 更可解释"

---

## 2. Reddit 平台表

### 主力子版（每日扫描）

| 子版 | 规模 | 内容特征 | DeGate 话题匹配度 |
|---|---|---|---|
| `r/PersonalFinanceCanada`（PFC） | ~1.8M | 加拿大最大个人财经 sub，CRA / 税务 / 投资讨论的主场；约 5-10% 帖子涉及加密 | **极高**（合规焦虑 + 自托管讨论的核心战场） |
| `r/BitcoinCA` | ~20-50k（活跃） | 加拿大 Bitcoin 专区，有税务讨论置顶帖（2020/21/22 Megathread） | **高**（自托管意识最强，hardware wallet 讨论多） |
| `r/CanadianInvestor` | ~100k+ | 投资综合，偶有加密 ETF / crypto-adjacent 讨论 | 中（合规话题偶尔相关） |
| `r/CryptoCurrency` | ~7M+ 全球 | 综合，加拿大用户占少数但存在；需关键词过滤 `CRA OR canadian OR T1135` | 中低（信噪比差） |
| `r/CanadaTaxes` | 小 | 纯税务 | 中（税务合规向帖偶见） |

### Quebec 法语子版（每周扫描）

| 子版 | 规模 | 说明 |
|---|---|---|
| `r/Quebec` | ~220k | 综合，用 `crypto OR bitcoin OR Revenu Québec OR TP-1` 过滤 |
| `r/QuebecFinance` | 小但活跃 | 魁北克个人财经 |
| `r/QuebecLibre` | 综合 | 偶有相关讨论 |

### 综合子版（弱信号，每周扫）

`r/Canada`（2M+）、`r/Canada_sub`、`r/ontario`、`r/alberta` —— 仅在 CARF / CRA / 全国性加密事件时抓头条；常规扫描价值有限。

### Reddit JSON URL 模板（关键词）

```
# 主力 sub 时间窗扫描
https://www.reddit.com/r/PersonalFinanceCanada/new.json?limit=100
https://www.reddit.com/r/PersonalFinanceCanada/search.json?q=crypto+OR+bitcoin+OR+CARF+OR+T1135+OR+%22voluntary+disclosure%22&restrict_sr=1&sort=new&t=week

# Evergreen 老帖
https://www.reddit.com/r/PersonalFinanceCanada/search.json?q=%22crypto+tax%22+OR+%22CRA+audit%22+OR+%22T1135%22&restrict_sr=1&sort=top&t=year&limit=20

# BitcoinCA
https://www.reddit.com/r/BitcoinCA/search.json?q=tax+OR+CRA+OR+CARF+OR+self-custody&restrict_sr=1&sort=new&t=week

# Quebec FR
https://www.reddit.com/r/Quebec/search.json?q=crypto+OR+bitcoin+OR+%22Revenu+Qu%C3%A9bec%22&restrict_sr=1&sort=new&t=week
```

### 关键词组合（英语）

- **合规焦虑**：`CRA`, `T1135`, `Schedule 3`, `CARF`, `voluntary disclosure`, `VDP`, `superficial loss`, `crypto audit`, `capital gains inclusion`, `Coinsquare data`
- **自托管**：`self-custody`, `hardware wallet`, `not your keys`, `cold storage`, `ledger trezor`, `FTX lesson`
- **DEX / Swap**：`DEX`, `Uniswap`, `multi-chain`, `bridge`, `MEV`, `slippage`
- **稳定币**：`USDC yield`, `stablecoin interest`, `DeFi APY`, `USDT Canada`
- **LP**：`liquidity pool`, `Uniswap v3`, `impermanent loss`, `range orders`

### 关键词组合（法语，Quebec 用）

- **合规**：`déclaration crypto`, `Revenu Québec crypto`, `TP-1`, `ARC`, `Agence du revenu du Canada`
- **自托管**：`auto-garde`, `portefeuille matériel`, `clé privée`, `garde personnelle`
- **DEX**：`échange décentralisé`, `DEX`, `multi-chaîne`

---

## 3. 确认死亡 / 不存在的子版（不要再扫）

- `r/CanadaCrypto` → 存在但近乎死版（最后活跃 2022）
- `r/CryptoCanada` → 不存在 / 空版
- `r/BitCoinCanada` → 已合并进 r/BitcoinCA

（每次扫描前可再快速 head 一下，死版会定期变化。）

---

## 4. 本地论坛 / 垂类媒体

| 平台 | URL | 覆盖方式 | 状态 |
|---|---|---|---|
| Financial Wisdom Forum | `financialwisdomforum.org` | `site:` WebSearch；偏传统投资、偶见加密 | 部分可用 |
| RedFlagDeals Finance | `forums.redflagdeals.com/personal-finance` | Google 索引良好 | 部分可用 |
| Canadian Money Forum | `canadianmoneyforum.com` | WebSearch | 部分可用 |
| Bitbuy 博客评论 | `bitbuy.ca/en/blog` | 手动 | 部分可用 |
| NDAX 博客评论 | `ndax.io/blog` | 手动 | 部分可用 |
| Coinsquare Learn | `coinsquare.com/learn` | 手动 | 部分可用 |

---

## 5. KOL / 意见领袖参考名单（非每日动作 —— 仅供需要时人工接触参考）

> **重要**：自 2026-04 起，KOL 接力**不再是日报固定输出**（实际运行下来 ROI 远低于直接软回帖 + 长内容 SEO）。下面这些是**人工启动专项 outreach 时**的参考名单，不是每天要联系的对象。
>
> **粉丝量为截至 2025 年底快照**，用之前先核对近期活跃度。**不要在 JSON 里凭空声称他们发了什么** —— 要么有真实链接要么不写。

### 加密 YouTuber / 广义 KOL

| Handle / Name | 渠道 & 粉丝量 | 备注 / 适用话题 |
|---|---|---|
| **VirtualBacon (Dennis Liu)** | YT 775k / Twitter 179k | 加拿大 crypto 教育 + 投资，适合 CARF / 自托管科普 |
| **Mason Versluis (@MasonVersluis)** | ~1.5M 多平台 | 加密交易 / 项目深度，适合 multi-chain 话题 |
| **Vitalik Buterin** | 巨型 | 加拿大籍（不常驻），适合宏观引用，不会接触合作 |

### 加密媒体 / 事务所

| 实体 | 类型 | 适用切入 |
|---|---|---|
| **Insight CPA** | CPA 事务所，crypto 专题 | op-ed 合作（CARF / T1135 主题） |
| **Marcil Lavallée** | CPA 事务所，发过 T1135 加密专题 | 合规深度稿的引用源 |
| **Segal GCSE LLP** | 多伦多税务事务所 | CARF 合规内容 |
| **Koinly / CoinLedger / TokenTax** | 加密税软件，加拿大页面 | 反向 SEO 参考（看他们写什么） |
| **NDAX** | Canadian CEX，博客活跃 | 内容合作可能性低（竞品向），但素材价值高 |

### Quebec 法语媒体（次级优先）

| 实体 | 说明 |
|---|---|
| **Les Affaires**（lesaffaires.com） | Quebec 主流商业媒体，偶有 crypto 合规稿 |
| **La Presse** | 魁北克主流报，crypto 报道有限 |
| **Journal de Québec** / **Journal de Montréal** | Quebecor 系，大众向，有时带税务角度 |

**重要**：Quebec 法语加密 KOL 生态较弱，需 DeGate 团队补充名单后记录。目前搜索中未找到单个超过 50k 粉丝的 Quebec 法语加密专职 YouTuber。

### Twitter / X 覆盖（2026-04 接入 xAI Grok Agent Tools API）

`twitter_ca` 已不再是覆盖缺口。每日通过 `scripts/xai_twitter_scan.py --market CA` 跑 Q1/Q2 拉真实推文。

**Q1（主流：合规 + 自托管）关键词**（脚本里已硬编码，下面是文档备份）：

英语：CRA, T1135, Schedule 3, CARF, voluntary disclosure, VDP, superficial loss, capital gains inclusion, Coinsquare data CRA, Bitbuy NDAX KYC, crypto audit Canada, Quebec TP-1 crypto, Revenu Québec crypto, self-custody, hardware wallet, leave Binance/Coinbase/Kraken, FTX lesson, Quadrigacx, Ledger Trezor

法语补丁（Quebec）：déclaration crypto Canada, ARC crypto, auto-garde, portefeuille matériel

**Q2（长尾 frontier：anon-on-off-ramp + rwa）关键词**：

英语：buy bitcoin anonymously Canada, no-KYC crypto, P2P crypto Canada, Bisq Robosats Hodl Hodl, Bitcoin ATM Canada, cash to crypto, Monero Canada, untraceable crypto, off-ramp privacy CAD, RWA crypto, tokenized stocks, xStocks, bTSLA bAAPL, Backed Finance, Ondo Finance, USDY, S&P 500 on-chain, BCSC tokenized

**调用示例**：
```bash
python scripts/xai_twitter_scan.py --market CA --hours 72
# 输出：scans/2026-04-24_0930_xai_twitter_ca_Q1Q2.json
```

具体 prompt 模板在 `scripts/xai_twitter_scan.py` 的 `QUERIES["CA"]` 字典里，要修改请直接改脚本（避免文档和代码不同步）。

### 仍然存在的覆盖缺口

- `twitter_ca_xai_failed`（仅当本期 xAI 调用失败时记入）
- `coverage_gap_twitter_ca_fr_low_volume`：xAI 对 Quebec 法语推文召回偶尔较少（Q1 prompt 已混入法语关键词，但 Quebec 加密 X 用户基数小）
- 不要凭空列未验证账号

---

## 6. 5A 钩子句示例（CA 本地口语，用来对齐 reply_draft 风格）

### Compliance
> "Honestly the CARF thing has me looking at self-custody more seriously. Not because it changes what I have to report — Schedule 3 still applies to every disposal — but because I want my records under my own control instead of CEX deciding what to hand over. Been trying Rabby, Safe, DeGate lately. DeGate has swap and LP built in which is nice for someone who'd rather not chase 5 dApps."

### Self-custody / FTX
> "Look, after FTX I really don't want any material amount sitting on a CEX longer than a week. Main self-custody now. When picking I care about multi-chain support and whether I can do yield in the same app — DeGate covers that better than most. Ledger for deep cold, DeGate for active. That's been working."

### DEX / Swap
> "Bridging manually between chains is exhausting. I tried DeGate recently because USDC between BASE and Solana is instant in-wallet — no separate bridge UI. Saved me a bunch of time last week."

### Stablecoin Yield
> "I keep a USDC chunk self-custodied earning yield. DeGate has built-in products so I don't have to eval every DeFi protocol — good enough for someone who doesn't want to go down that rabbit hole."

### LP / Range Vault
> "Managing Uniswap v3 ranges myself was a headache — constantly rebalancing. DeGate's range vault basically productized it."

---

## 7. CA 特有的额外叙事红线（补充 `narrative-compliance.md`）

除了通用红线，在 CA 市场 reply 时额外警惕：

1. **CARF 日期不要写死**。目前 CRA 官方文件和部分 CPA 来源对 2026-01-01 vs 2027-01-01 有分歧。用 "likely 2026 or 2027 depending on how CRA phases it in" 比单一日期安全。

2. **Quebec TP-1 只对 QC 居民说**。回 ROC（Rest of Canada）用户时不要提 TP-1，会误导。

3. **T1135 阈值是成本不是市值**。$100,000 CAD 指总**成本基础**，不是当前市值。说错会让事实性自查崩。

4. **Superficial Loss ≠ Wash Sale**。不要用美国术语 "wash sale"。加拿大叫 superficial loss，30 天窗口。

5. **Capital gains inclusion rate 变化是分层的**。不要说 "Canada is doubling capital gains"。准确说法是 "inclusion rate goes from 50% to 66.67% for gains over $250k per year, starting 2026"。

6. **VDP 的前提条件**。VDP 只对**尚未被 CRA 通知 audit**的纳税人有效。已经收到 audit letter 的不能用 VDP。不要笼统说 "just do VDP" 给已经收到信的用户。

---

## 8. 覆盖缺口清单（本市场固定 gap，2026-04 起更新）

写 report 的 `coverage_gaps` 时必含：
- `telegram` —— 无 MCP 接入
- `discord` —— 无 MCP 接入
- `bitbuy_blog_comments` / `ndax_blog_comments` —— 未自动化抓取

**已不再是 gap**（2026-04 起接入）：
- ~~`twitter_ca_en`~~ / ~~`twitter_ca_fr`~~ —— 通过 xAI Grok Agent Tools API 接入

**条件性 gap**（只在本期触发时记入）：
- `twitter_ca_xai_failed` —— 仅当本期 xAI 调用失败时

未来补 MCP 或直接抓取能力时从 gap 列表里划掉。
