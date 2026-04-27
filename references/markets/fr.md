# Market Plugin: 🇫🇷 France (FR)

**市场优先级**：约 30%
**主语言**：`fr`
**时区参考**：UTC+1（CET） / UTC+2（CEST 夏令时）
**税务机关**：DGFiP（Direction générale des Finances publiques）
**监管机关**：AMF（Autorité des Marchés Financiers）+ ACPR

---

## 1. 法规催化剂（Compliance 话题的钩子清单）

### 核心催化剂（按紧迫度排序）

| 催化剂 | 生效时间 | 影响 | 用户焦虑点 |
|---|---|---|---|
| **Flat Tax (PFU) 从 30% 涨到 31.4%** | **2026-01-01 生效** | capital gains 的 flat rate 涨了：12.8% IR + 18.6% prélèvements sociaux（原 17.2%） | "我的 PnL 税突然多了 1.4%" |
| **DAC8（EU 指令 2023/2226）** | **2026-01-01 生效**（法国 2025 Finance Act 第 54 条转置）；首次自动数据交换 **2027-09-30**（覆盖 2026 年活动） | 所有 EU CASP 向各国税务机关上报用户交易数据 + 提现目的地址 | "我在 Binance / Coinbase / Kraken 的历史数据明年 9 月就会到 DGFiP 手里" |
| **Formulaire 3916-bis**（境外加密账户申报） | 长期，DAC8 没替代它 | 每个境外 custodial 账户单独填（Binance、Coinbase 各一张）；**自托管钱包不是 3916-bis 意义上的"账户"** | "我有 5 个 CEX 账户要填 5 张 3916-bis？" 要 |
| **Formulaire 2086**（capital gains 明细） | 每年 | 每次 crypto→euro 或买商品触税的 disposition 单独列；**crypto-to-crypto swap 不触税**（法国特殊规则） | "我只换币没出法币要不要申报？" 不用（但要追踪） |
| **Formulaire 2042-C**（汇总） | 每年 | 填入当年总 plus-value / moins-value | 和 2086 配套 |
| **305 欧元门槛** | 长期 | 年度**总处置金额** ≤ €305 免税（注意是 cessions 总额不是 gain） | "小额到底要不要报？" |
| **PCVT 方法（Plus-Values de Cessions）** | 长期 | 法国强制成本基础算法：`sale price - (total acquisition cost × sale price / total portfolio value)`。需要**整个 portfolio 价值**不只是卖出的那部分 | "这个公式怎么算？"（复杂到一般用加密税软件） |
| **BNC（Bénéfices Non-Commerciaux）职业 trader** | 长期 | 若被认定专业 trader，progressive rate 最高 45% + BNC 制度 | "我频繁交易会不会被重分类？" |
| **Mining / Staking = BNC income** | 长期 | 挖矿 / staking 收益按 BNC 申报，不走 PFU | "staking 收益怎么报？" |
| **Evasion Penalty 80%** | 长期 | 逃税罚款最高 80% + 最高 €500,000 罚款 + 最高 5 年刑期 | 吓阻效应高 |
| **MiCA（EU Markets in Crypto-Assets）** | 2024-12 全面生效 | 框架法规，监管 CASP（发币 / 做市） | 用户层面感受较间接 |

### Compliance 话题下的核心钩子（DeGate 叙事切入点）

**最强钩子（法国专属）：crypto-to-crypto swap 不触税 + 自托管对 3916-bis 中性**
- 真实事实 1：法国唯一在 EU 里明确 crypto→crypto swap **不是** taxable event（2019 Pacte Act 确立）；只有 crypto→EUR 或 crypto→商品触税。
- 真实事实 2：Non-custodial 钱包**不是 3916-bis 意义上的"compte"**，所以不填 3916-bis。但这**不等于免除 2086 capital gains 申报**。
- 转化：法国用户做 DeFi swap 的**税务摩擦**比加/澳/意天然低；DeGate 多链 swap + 自托管的组合对法国用户双重合规友好（减少 3916-bis 账户数量 + swap 不计税）。

**次强钩子：DAC8 2026-01-01 生效 + 2027-09-30 首次交换**
- CEX 可见性在 2027 年底骤升；**现在开始做干净记录 + 部分资产自托管**的用户，明年被回看时姿态更好。
- 叙事 reframe：自托管不是"躲 DAC8"，是"在 DAC8 面前把我自己的账搞清楚"。

**PFU 31.4% 涨价后的心态撬动**
- 真实情绪：2026 初涨价是个可以吐槽的新催化剂 —— 法国用户对税负敏感度高。合规 reply 可以自然带入 "既然税率都涨了，至少要把成本基础算清楚"，DeGate 的多链视图帮忙聚合成本基础。

---

## 2. Reddit 平台表

### 主力子版（每日扫描）

| 子版 | 规模 | 内容特征 | DeGate 话题匹配度 |
|---|---|---|---|
| **`r/vosfinances`** | ~414k | 法国最大个人财经 sub；税务 / 投资 / 退休主题；约 5-8% 涉及加密 | **极高**（法国合规焦虑 + 税务讨论主场） |
| `r/CryptoFR` | 中 | 法国加密综合 sub | 高（信噪比中等） |
| `r/CryptoMonnaie` | 中小 | 法语加密讨论 | 中高 |
| `r/france` | ~1M+ | 综合大 sub；用 `crypto OR bitcoin OR DAC8 OR "flat tax"` 过滤 | 中（话题广但加密比例低） |
| `r/AskFrance` | 中 | Q&A 型，偶有税务 crypto 问题 | 中低 |

### 综合子版（弱信号，每周扫）

- `r/frenchrap` 等文化 sub —— 忽略
- `r/FIREFrance` 或对等 FIRE sub —— 若存在且活跃可加入

### Reddit JSON URL 模板

```
# 主力
https://www.reddit.com/r/vosfinances/new.json?limit=100
https://www.reddit.com/r/vosfinances/search.json?q=crypto+OR+bitcoin+OR+DAC8+OR+%22flat+tax%22+OR+%223916-bis%22&restrict_sr=1&sort=new&t=week

# Evergreen
https://www.reddit.com/r/vosfinances/search.json?q=%22fiscalit%C3%A9+crypto%22+OR+%22imp%C3%B4t+crypto%22+OR+%22PFU+crypto%22&restrict_sr=1&sort=top&t=year&limit=20

# CryptoFR
https://www.reddit.com/r/CryptoFR/search.json?q=fiscalit%C3%A9+OR+imp%C3%B4t+OR+DAC8+OR+3916&restrict_sr=1&sort=new&t=week
https://www.reddit.com/r/CryptoMonnaie/new.json?limit=50
```

### 关键词组合（法语，核心）

- **合规焦虑**：`fiscalité crypto`, `impôt crypto`, `PFU`, `flat tax`, `DAC8`, `3916-bis`, `formulaire 2086`, `DGFiP`, `déclaration crypto`, `ravvedimento` 对应概念是 `régularisation`, `plus-value crypto`, `PCVT`, `BNC crypto`, `cession crypto`
- **自托管**：`auto-garde`, `wallet non-custodial`, `clé privée`, `portefeuille matériel`, `Ledger`, `pas tes clés pas tes cryptos`
- **DEX**：`échange décentralisé`, `DEX`, `multi-chaîne`, `cross-chain`, `slippage`
- **稳定币**：`rendement USDC`, `rendement EURC`, `stablecoin France`, `yield DeFi`
- **LP**：`pool de liquidité`, `Uniswap v3 France`, `perte impermanente`, `market making crypto`

### 关键词组合（英语，辅助）

当法语结果稀疏时可用英语 `France OR French` + 核心术语扩大捞取范围，但主要 reply 仍用法语。

---

## 3. 确认死亡 / 不存在的子版（不要再扫）

- `r/FranceBitcoin` → 近乎空版
- `r/BitcoinFrance` → 小众活跃度低

（扫前再 head 一次确认。）

---

## 4. 本地论坛 / 垂类媒体

| 平台 | URL | 覆盖方式 | 状态 |
|---|---|---|---|
| **Journal du Coin** | `journalducoin.com` | RSS / WebSearch | 部分可用 |
| **Cryptoast** | `cryptoast.fr` | RSS / WebSearch | 部分可用 |
| **CoinAcademy** | `coinacademy.fr` | WebSearch | 部分可用 |
| **Cointelegraph France** | `cointelegraph.com/fr` | RSS | 部分可用 |
| **CryptonewsFR** | `cryptonews.com/fr/` | RSS | 部分可用 |
| **BFM Crypto** | BFM TV 加密栏目 | YouTube + 文章 | 部分可用 |
| **Forum BoursoBank / Boursorama** | `forum.boursorama.com` | `site:` WebSearch | 部分可用，Google 索引 OK |
| **FinancesMag / Les Echos crypto** | 主流财经媒体加密板块 | WebSearch | 部分可用 |
| **Waltio 博客** | `waltio.com/fr` | 法国加密税软件博客 | 高质量合规参考 |
| **Coinhouse 博客** | `coinhouse.com` | 法国本地 CASP，博客 + 社区 | 部分可用 |

---

## 5. KOL / 意见领袖参考名单（非每日动作 —— 仅供需要时人工接触参考）

> **重要**：自 2026-04 起，KOL 接力**不再是日报固定输出**（实际运行下来 ROI 远低于直接软回帖 + 长内容 SEO）。下面这些是**人工启动专项 outreach 时**的参考名单，不是每天要联系的对象。

### 加密 YouTuber / 头部 KOL

| Handle / Name | 渠道 & 粉丝量 | 备注 / 适用话题 |
|---|---|---|
| **Hasheur** | YT 巨量（法国加密最大 YouTuber） | 企业化运作，难接触；引用源价值 |
| **Cryptoast**（官方频道） | YT 188k | 主流加密媒体 YouTube，合作窗口最实际的之一 |
| **Journal du Coin（Sami）** | YT 155k / Twitter 271k | **媒介合作首选** —— 采访访谈强项，op-ed 投稿通路 |
| **Crypto Le Trône** | YT 中大型 | 分析向 |
| **Enter The Crypto Matrix** | YT 中大型 | 教育向 |
| **Coin Academy** | 教育平台 | 入门内容强，合作可能性中 |
| **Vincent Ganne** | 技术分析向 | 偏 trading，合规话题匹配度中 |
| **Crypto Pour Tous** | YT 教育向 | 大众科普 |

### 加密媒体 / 内容平台

| 实体 | 类型 | 适用切入 |
|---|---|---|
| **Journal du Coin** | 法国头部加密媒体，271k Twitter | **op-ed 投稿首选** —— DAC8 / Flat Tax 主题内容对口 |
| **Cryptoast** | 法国头部加密媒体，188k YT | op-ed 次选 + 合作内容 |
| **Les Echos Crypto** | 主流财经媒体加密栏目 | 宏观稿投稿（门槛高） |
| **BFM Crypto** | BFM TV 加密栏目 | 电视曝光（门槛最高） |
| **Waltio** | 加密税 SaaS + 博客 | 合规内容协作（可能竞合） |
| **Coinhouse** | 法国本地 CASP + 博客 | 竞品向但素材价值高 |

### 税务 / 合规专业博主

| 实体 | 说明 |
|---|---|
| **ADAN**（Association pour le Développement des Actifs Numériques） | 法国加密行业协会，政策/监管发声权威 |
| **Fibo-Crypto** 等合规教育博客 | 细节查证源 |
| 法国 fiscalistes / expert-comptables crypto 专题博主 | 通过 LinkedIn 搜索补充 |

### Twitter / X 覆盖（2026-04 接入 xAI Grok Agent Tools API）

`twitter_fr` 已不再是覆盖缺口。每日通过 `scripts/xai_twitter_scan.py --market FR` 跑 Q1/Q2 拉法语推文。

**Q1（主流：合规 + 自托管）法语关键词**：

DAC8, fiscalité crypto, impôt crypto, PFU 31,4%, flat tax crypto 2026, formulaire 3916-bis, formulaire 2086, DGFiP crypto, déclaration crypto, plus-value crypto France, PCVT, BNC crypto, cession crypto, régularisation crypto, transfert résidence fiscale (Portugal/Malte/Dubai), Waltio Koinly France, MiCA France, auto-garde, wallet non-custodial, Ledger Trezor, "pas tes clés pas tes cryptos", quitter Binance/Coinbase/Kraken/Bitpanda/Coinhouse, FTX leçon, multi-sig, MetaMask vs hardware

**Q2（长尾 frontier：anon-on-off-ramp + rwa）法语关键词**：

acheter bitcoin anonymement, crypto sans KYC, P2P crypto France, Bisq, Bitcoin ATM France, cash to crypto, Monero privacy, "non traçable" crypto, bridge sans KYC, convertir crypto en euros sans CEX, TRACFIN crypto, RWA crypto, actions tokenisées, xStocks, bTSLA bAAPL, Backed Finance, Ondo Finance, USDY, ETF tokenisé, Tesla tokenisé Kraken, "acheter actions US sans courtier"

**调用示例**：
```bash
python scripts/xai_twitter_scan.py --market FR --hours 72
# 输出：scans/2026-04-24_0930_xai_twitter_fr_Q1Q2.json
```

具体 prompt 模板（含法语 system prompt）在 `scripts/xai_twitter_scan.py` 的 `QUERIES["FR"]` 字典里。

### 仍然存在的覆盖缺口

- `twitter_fr_xai_failed`（仅当本期 xAI 调用失败时记入）
- 核心人工跟踪 handles（不在 xAI 之外凭空列举他们发了什么）：@JournalDuCoin、@Cryptoast、@Hasheur、@VincentGanne、@CoinAcademy

---

## 6. 5A 钩子句示例（FR 本地口语，reply_draft 风格对齐）

### Compliance
> "Avec DAC8 qui arrive et la flat tax qui passe à 31,4%, autant remettre à plat ses comptes. Ce qui m'a fait passer plus en auto-garde c'est pas d'éviter quoi que ce soit — la 2086 faut la faire de toute façon si tu sors en euros — c'est juste que j'ai la main sur mon historique au lieu de dépendre de ce que le CEX va remonter. J'teste Rabby, Safe, DeGate. DeGate a le swap et le market making intégré, pratique pour un flemmard."

### Self-custody / FTX
> "Post-FTX franchement je garde plus rien de sérieux sur un CEX. Tout en auto-garde. Entre wallets à moi c'est pas une cession donc pas d'impact 2086 — mais garde quand même tes traces, le fisc peut demander de prouver que les deux adresses sont bien à toi."

### DEX / Swap
> "Truc cool en France : les swap crypto→crypto sont pas imposables (c'est que la sortie en euros). Donc bouger du BTC vers ETH via un DEX = 0 PFU. DeGate agrégateur m'évite les bridges manuels entre chaînes, USDC entre BASE et Solana direct dans le wallet."

### Stablecoin Yield
> "Je garde un bout de USDC en auto-garde qui rend un peu. DeGate a des produits intégrés. Attention le rendement c'est du BNC pas du PFU, donc à déclarer différemment."

### LP / Range Vault
> "Uniswap v3 à gérer soi-même c'est chronophage. DeGate a un truc de range vault qui automatise. Ça change rien au traitement fiscal mais opérationnellement c'est beaucoup plus simple."

---

## 7. FR 特有的额外叙事红线（补充 `narrative-compliance.md`）

除了通用红线，在 FR 市场 reply 时额外警惕：

1. **DAC8 vs 3916-bis vs Flat Tax 是三件不同的事**。绝对不能说 "DAC8 remplace la 3916-bis" 或者 "la 3916-bis c'est fini avec DAC8"。三者并存。

2. **Crypto-to-crypto swap 不触税不等于不追踪**。PCVT 方法需要整个 portfolio 价值来算每次 crypto→EUR 的 plus-value。不要暗示"swap 随便玩，反正不报"。

3. **Non-custodial 不是 3916-bis 账户 ≠ 不用报 capital gains**。这是和 CA 的 T1135 类似的陷阱。

4. **PFU 是 31.4% 不是 30%**（2026-01-01 起）。写 reply 时如果提到税率要用最新值。可选 progressive scale 若边际税率 < 12.8%（对低收入者友好的细节）。

5. **305 欧元门槛是 cessions 总额不是 gain**。"Si tu fais moins de 305€ de plus-value" 是错的；正确："Si tu fais moins de 305€ de cessions totales dans l'année"。

6. **BNC vs PFU 的触发判定不要给用户下定论**。Professional trader 认定涉及主观要素（intent / frequency），回 reply 不要轻易说 "tu es forcément BNC"。建议是 "check avec un fiscaliste"。

7. **MiCA 不直接影响个人用户申报**。不要把 MiCA 和 DAC8 / 3916-bis 混为一谈，两者目的不同（MiCA 规范 CASP 运营，DAC8 规范数据上报）。

---

## 8. 覆盖缺口清单（本市场固定 gap，2026-04 起更新）

写 report 的 `coverage_gaps` 时必含：
- `telegram` —— 无 MCP 接入
- `discord` —— 无 MCP 接入
- `boursorama_forum` —— Boursorama 论坛未自动化抓取
- `cryptoast_comments` / `journal_du_coin_comments` —— 媒体博客评论区未自动化
- `coinhouse_community` —— Coinhouse 社区未自动化

**已不再是 gap**（2026-04 起接入）：
- ~~`twitter_fr`~~ —— 通过 xAI Grok Agent Tools API 接入

**条件性 gap**（只在本期触发时记入）：
- `twitter_fr_xai_failed` —— 仅当本期 xAI 调用失败时

未来补能力时从 gap 列表里划掉。
