# Market Plugin: 🇦🇺 Australia (AU)

**市场优先级**：约 20%
**主语言**：`en`
**时区参考**：UTC+10（AEST） / UTC+11（AEDT 夏令时）
**税务机关**：ATO（Australian Taxation Office）

---

## 1. 法规催化剂（Compliance 话题的钩子清单）

### 核心催化剂（按紧迫度排序）

| 催化剂 | 生效时间 | 影响 | 用户焦虑点 |
|---|---|---|---|
| **ATO Crypto Data-Matching Program** | 2014-15 ~ 2025-26（滚动更新） | ATO 从 CoinSpot、Swyftx、BTC Markets、Independent Reserve、Kraken AU 等主力本地所拉用户 + 交易数据；已覆盖 ~600,000 个人；已发 100,000+ warning letter | "ATO 是不是已经有我全部交易记录了？" |
| **CARF 集成 AU 数据匹配** | 2026（整合期） | ATO 数据匹配项目扩展到覆盖 OECD CARF 数据，国外交易所数据也进入 ATO 视野 | "我用海外所是不是就能绕过？" 不能 |
| **Crypto = CGT Asset（TD 2014/26）** | 长期 | 加密明确是 CGT asset，不是 foreign currency（2022 立法回溯 2021-07 确认）；每次 disposal 触发 CGT | "我换币 / 花 crypto 买东西都要记 CGT？" 要 |
| **DeFi Guidance（ATO 2023）** | 2023 至今 | 进入 DeFi 协议 = CGT 事件（"change in beneficial ownership"）；LP / staking / wrap/unwrap 都是 CGT；staking rewards 到手按 ordinary income | "我 stake ETH 到手就要交税？" 要 |
| **50% CGT Discount** | 长期 | **Investor**（非 trader）持有 >12 个月，capital gain 部分可享 50% discount；Super fund 33.33% | "怎么判定我是 investor 还是 trader？" 频率 + intent |
| **Super Fund Unrealised Gains Tax** | 2026 起 | Super 余额 > $3M AUD 部分，**未实现** gains 按 15% 征 | 仅影响高净值 super 持有者 |
| **Evasion Penalty 75%** | 长期 | 故意 evasion 罚款可达 shortfall 的 75% | 吓阻效应高 |
| **myTax Pre-fill** | 近年持续扩展 | ATO 在 myTax 里预填部分 CEX 数据，用户改不了就得解释 | "我看到 myTax 里有我不认的交易" |

### Compliance 话题下的核心钩子（DeGate 叙事切入点）

**最强钩子：ATO DeFi 指引复杂度 + self-custody 清晰记录**
- 真实事实：ATO 的 DeFi 指引复杂且在持续变化（LP 何时算 CGT、wrap 是否算 CGT 都有争议），普通投资者很难靠 CEX 数据导出搞清楚自己的实际税务仓位。
- 转化：自托管不改变你要申报的义务，但给你一份**链上可核对的交易历史**，反而比 CEX pre-fill 更可解释。

**次强钩子：钱包间转账不是 CGT 事件（但要记录）**
- 真实事实：自己名下多个钱包之间转账**不是** CGT 事件（ATO 明确），但 ATO 可能在 audit 时要求证明两个地址都是你的。
- 转化：自托管 + 钱包内清晰标签 = ATO-ready 证据链。

**风险叙事（FTX / CEX 风险）+ 50% CGT discount 组合**
- "Hold > 12 个月享 50% discount" 只对 CGT 适用；长期持有 + 自托管 = 清晰冷储 + 税务友好。

---

## 2. Reddit 平台表

### 主力子版（每日扫描）

| 子版 | 规模 | 内容特征 | DeGate 话题匹配度 |
|---|---|---|---|
| `r/AusFinance` | ~230k+ | 澳洲传统个人财经 sub；Big 4 banks / super / CGT / property 是主角；约 3-8% 帖涉及加密 | **极高**（合规向、税务向讨论密度最高） |
| `r/fiaustralia` | ~90k（估计） | 澳洲 FIRE 社区；crypto as part of portfolio | 高（长期投资 + 税务优化视角） |
| `r/CryptoCurrency` + `australia` / `ATO` 过滤 | 全球大 sub | 澳洲用户占少数 | 中低 |
| `r/BitcoinAUS` | 小 | 澳洲 BTC 专区，有税务讨论 | 中高（自托管意识强） |
| `r/CryptoAustralia` | 小-中 | 澳洲加密综合 | 中（信噪比中等） |
| `r/ausstocks` | 中 | 股票为主但 crypto-adjacent ETF 讨论偶有 | 中低 |

### 综合子版（弱信号，每周扫）

- `r/australia` ~700k —— 综合，用 `crypto OR bitcoin OR ATO` 过滤，仅抓全国级话题
- `r/ASX_Bets` ~230k —— 投机文化，crypto 讨论娱乐化为主

### Reddit JSON URL 模板

```
# 主力
https://www.reddit.com/r/AusFinance/new.json?limit=100
https://www.reddit.com/r/AusFinance/search.json?q=crypto+OR+bitcoin+OR+ATO+OR+CGT+OR+DeFi&restrict_sr=1&sort=new&t=week

# Evergreen
https://www.reddit.com/r/AusFinance/search.json?q=%22crypto+tax%22+OR+%22ATO+data+matching%22+OR+%22CGT+crypto%22&restrict_sr=1&sort=top&t=year&limit=20

# FI & BitcoinAUS
https://www.reddit.com/r/fiaustralia/search.json?q=crypto+OR+bitcoin&restrict_sr=1&sort=new&t=week
https://www.reddit.com/r/BitcoinAUS/new.json?limit=50
```

### 关键词组合

- **合规焦虑**：`ATO`, `CGT`, `data matching`, `CARF`, `myTax pre-fill`, `TD 2014/26`, `DeFi ruling`, `staking tax`, `wrapped token`, `beneficial ownership`, `CGT discount`
- **自托管**：`self-custody`, `hardware wallet`, `cold wallet`, `ledger trezor`, `not your keys`, `CoinSpot risk`
- **DEX**：`DEX swap CGT`, `Uniswap Australia`, `bridge`, `aggregator`
- **稳定币**：`USDC AUD`, `stablecoin yield`, `AUD stablecoin`
- **LP**：`liquidity pool tax`, `Uniswap v3 ATO`, `impermanent loss`, `yield farming Australia`

---

## 3. 确认死亡 / 不存在的子版（不要再扫）

- `r/AustraliaCrypto` → 小众或空版
- `r/CryptoAU` → 不存在
- `r/AusCrypto` → 已合并或不活跃

（扫前建议再 head 一次，活跃度会变化。）

---

## 4. 本地论坛 / 垂类媒体

| 平台 | URL | 覆盖方式 | 状态 |
|---|---|---|---|
| **Whirlpool** | `forums.whirlpool.net.au` | 澳洲最大综合网络论坛之一，有 Finance & Business 区，偶有加密税讨论 | 部分可用；`site:forums.whirlpool.net.au crypto tax` |
| Finder Community | `finder.com.au/community` | Finder.com.au 附属社区，crypto 话题活跃 | 部分可用 |
| ATO Community | `community.ato.gov.au` | ATO 官方问答社区 —— 用户直接问 ATO 员工 crypto 问题 | **高价值**，搜 `crypto` + `DeFi` / `staking` |
| HotCopper | `hotcopper.com.au` | ASX 散户股票论坛，crypto-adjacent ETF 讨论偶见 | 低价值 |
| CoinSpot / Swyftx / Independent Reserve 博客评论 | 各自域名 | 手动 | 部分可用 |

**特别指出**：`community.ato.gov.au` 是澳洲独有的高价值金矿 —— 用户在 ATO 官方社区公开问合规问题，ATO 员工回答，是**事实核对**的一手来源（比 reddit 二手讨论更可靠）。

---

## 5. KOL / 意见领袖参考名单（非每日动作 —— 仅供需要时人工接触参考）

> **重要**：自 2026-04 起，KOL 接力**不再是日报固定输出**（实际运行下来 ROI 远低于直接软回帖 + 长内容 SEO）。下面这些是**人工启动专项 outreach 时**的参考名单，不是每天要联系的对象。

### 加密 / 财经媒体 & KOL

| Handle / Name | 渠道 & 粉丝量 | 备注 / 适用话题 |
|---|---|---|
| **Fred Schebesta** | Finder.com.au 创始人，Twitter / YouTube 活跃 | 澳洲最大加密意见领袖之一，投资 / 宏观 / 合规都有覆盖 |
| **Kylie Purcell** | Finder.com.au 加密投资分析师，AFR / Yahoo Finance / SBS / News.com.au 常客 | **合规 / 税务领域最匹配的接触候选** —— 如果做 ATO 数据匹配 / CARF 主题内容，她是首选 op-ed 对接 |
| **Stephan Livera** | Podcast "Stephan Livera Podcast"，Bitcoin / 奥地利经济学派 | 偏 BTC Maximalist，适合 self-custody / sound money 叙事而不是 DeFi |
| **Equity Mates Media**（Tracey Plowman / Blake Cassidy / Craig Jackson） | "Crypto Curious" podcast，Apple rating 4.7 | 大众向加密科普，适合 CARF / ATO 变化科普合作 |
| **Sheldon Evans** | YouTube | 生活方式 + 加密视角 |

### 加密媒体 / 内容平台

| 实体 | 类型 | 适用切入 |
|---|---|---|
| **Finder.com.au** | 澳洲最大财经比价 + 加密媒体 | op-ed 投稿（Kylie Purcell 编辑线） |
| **AFR（Australian Financial Review）** | 主流财经日报 | 宏观合规稿的投稿路径（门槛高） |
| **Cointracker / Koinly / Kryptos / CoinTracking** AU 页面 | 加密税软件 | 反向 SEO 参考 + 可能的合作机会 |
| **Digi Tax Advisors** / **National Accounts** | CPA 事务所，crypto 专题内容多 | 合规深度稿的引用源 / 合作 |
| **Cointelegraph Australia** | 加密媒体 | 新闻稿发布 |

### Twitter / X 覆盖（2026-04 接入 xAI Grok Agent Tools API）

`twitter_au` 已不再是覆盖缺口。每日通过 `scripts/xai_twitter_scan.py --market AU` 跑 Q1/Q2。

**Q1（主流：合规 + 自托管）关键词**：

ATO crypto, ATO data matching, CGT crypto, myTax pre-fill, TD 2014/26, ATO DeFi ruling, staking tax Australia, wrap unwrap CGT, beneficial ownership crypto, 50% CGT discount, Super fund crypto $3M, CARF Australia, CoinSpot Swyftx Independent Reserve audit, crypto investor vs trader Australia, self-custody, hardware wallet, leave CoinSpot/Swyftx/Binance Australia, FTX Australia, MetaMask vs hardware

**Q2（长尾 frontier：anon-on-off-ramp + rwa）关键词**：

buy bitcoin anonymously Australia, no-KYC crypto AU, P2P crypto Australia, Bisq, Bitcoin ATM Australia, cash to crypto AU, Monero Australia, off-ramp privacy AUD, AUSTRAC crypto, AML crypto AU, RWA crypto, tokenized stocks Australia, on-chain ASX, xStocks, bTSLA bAAPL, Backed Finance, Ondo Finance, USDY, ASIC tokenized assets

**调用示例**：
```bash
python scripts/xai_twitter_scan.py --market AU --hours 72
# 输出：scans/2026-04-24_0930_xai_twitter_au_Q1Q2.json
```

具体 prompt 模板在 `scripts/xai_twitter_scan.py` 的 `QUERIES["AU"]` 字典里。

### 仍然存在的覆盖缺口

- `twitter_au_xai_failed`（仅当本期 xAI 调用失败时记入）
- 不要凭空列未验证 tweet

---

## 6. 5A 钩子句示例（AU 本地口语，reply_draft 风格对齐）

### Compliance
> "The ATO guidance on DeFi has been a moving target — wrap/unwrap, LP entry, all CGT events supposedly. Honestly the cleanest way for me has been to do more in self-custody so I have one consistent history to reconcile, instead of piecing together CEX exports. Tried Rabby, Safe, DeGate — DeGate has swap and LP in one app so my records don't fragment across 5 dApps."

### Self-custody / FTX
> "Learned my lesson post-FTX. Anything I'm not actively trading goes to cold / self-custody. Wallet-to-wallet between my own addresses isn't a CGT event but keep records anyway — ATO can ask you to prove it's your address."

### DEX / Swap
> "Every swap being a CGT event is painful in Australia, not gonna lie. At least with DeGate's aggregator I'm doing fewer swaps to get where I want — USDC between BASE and Solana is in-wallet, no bridge hop. Fewer taxable events, same outcome."

### Stablecoin Yield
> "USDC in self-custody earning something is better than sitting on a CEX doing nothing. DeGate has built-in products — remember the yield is ordinary income per ATO, not CGT."

### LP / Range Vault
> "LP entry is a CGT event per ATO guidance so I'm picky about it. DeGate's range vault makes the actual management less of a headache — doesn't change the tax treatment but the operational side is a lot cleaner."

---

## 7. AU 特有的额外叙事红线（补充 `narrative-compliance.md`）

除了通用红线，在 AU 市场 reply 时额外警惕：

1. **DeFi = CGT 事件的 beneficial ownership 逻辑一定要说清**。不能暗示 "DEX swap 是自己钱包换自己的币所以不算 CGT"。ATO 明确说是。

2. **wrap/unwrap 是有争议的，但 ATO 现行立场是 CGT 事件**。可以吐槽 "这规定有点奇怪"，但不要断言 "wrap 不触税"。

3. **50% CGT discount 不适用 trader 和 income**。
   - 只 investor（非 trader）享有
   - 只对 capital gain，不对 staking rewards 等 ordinary income
   - 必须持有 >12 个月

4. **Super Fund $3M 未实现税只影响 super，不影响个人持仓**。不要在回普通用户帖时错说 "2026 起所有 crypto 都要交未实现税"。

5. **ATO data matching 覆盖的是 AU-based CEX**。如果用户说 "我用的是海外所"，不要直接说 "你安全了" —— CARF 正在填这个缺口，而且海外所若与 ATO 有信息交换协议也会上报。

6. **Evasion 75% penalty 只针对故意 evasion**，不是所有补报。主动 amendment 通常罚款轻很多。不要吓唬用户 "不报就 75%"。

---

## 8. 覆盖缺口清单（本市场固定 gap，2026-04 起更新）

写 report 的 `coverage_gaps` 时必含：
- `telegram` —— 无 MCP 接入
- `discord` —— 无 MCP 接入
- `whirlpool_forums` —— Whirlpool 未自动化抓取
- `ato_community` —— ATO 官方社区高价值但未自动抓取（**应尽快补入抓取能力**）

**已不再是 gap**（2026-04 起接入）：
- ~~`twitter_au`~~ —— 通过 xAI Grok Agent Tools API 接入

**条件性 gap**（只在本期触发时记入）：
- `twitter_au_xai_failed` —— 仅当本期 xAI 调用失败时

未来补能力时从 gap 列表里划掉。
