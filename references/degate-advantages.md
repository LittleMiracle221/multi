# DeGate 产品优势 —— 供 reply / 内容策划时参考

## 用法说明

这份文档不是"回复时必须复述的卖点列表" —— 作为普通网友人设发言，**绝大多数时候不需要主动推销 DeGate**，即使提到也只是"我在试的几个钱包之一"这种顺带口吻（参考 `narrative-compliance.md`）。

这份文档的用处是：
- 让你**心里清楚** DeGate 到底在哪些点上和 CEX 钱包 / 其他自托管钱包不同
- 当对话自然走到"你用啥钱包"、"多链用户体验"、"稳定币放哪"这类问题时，可以真实说出产品特性
- 作为长文 / 推文 / KOL brief 的素材池（官方内容里可以更直接地谈这些优势）

**这是个活文档**，随 DeGate 产品更新持续补充。发现新卖点或对手比较点，直接往下追加。

---

## 核心定位

DeGate 是**多链自托管钱包**，把通常需要多个工具才能完成的事情装在一个钱包里：

- **交易**：多链 Swap
- **做市 / 赚费**：基于 LP 区间的做市工具（"区间宝"）
- **生息**：稳定币理财
- **多链资产管理**：一个钱包统一看 / 统一操作所有链上的资产

## 对比 CEX 钱包

| 维度 | CEX 钱包（Binance / Coinbase / Kraken / CoinSpot 等） | DeGate |
|---|---|---|
| 私钥归属 | 交易所托管 | **你自己持有**（助记词 / 私钥只在你本地） |
| KYC | 必须 | 不需要 |
| 资产主权 | 交易所可冻结 / 限制提现 | 链上你的，谁都动不了 |
| 多链支持 | 通常受限或体验割裂 | **一个钱包统一管多链** |
| 收益归属 | 平台先抽一刀 | 做市 / 生息的收益**直接进你钱包** |
| 监管风险 | CARF / DAC8 下 CEX 需上报持仓 + 提现地址 | 作为自托管工具本身不是 CASP |

> 注：自托管**不等于免除用户申报义务**，申报义务始终在用户本人（CA 的 Schedule 3、AU 的 CGT 报告、FR 的 Cerfa 2086 都照填）。这一点在 `narrative-compliance.md` 的市场事实底线里有详细讨论。

## 对比其他自托管钱包（Rabby / MetaMask / Safe 等）

DeGate 的差异点在于**把 DeFi 玩法装进去**，不只是一个签名和转账工具：

- **内置 LP 做市（区间宝）**：传统自托管钱包只能转账 / Swap，想做市得自己打开 Uniswap / Orca 前端去设置区间、跟踪价格、手动再平衡。DeGate 把这套流程产品化，降低普通用户门槛。
- **内置稳定币理财**：一般钱包你得自己选协议、看 APY、自己评估风险。DeGate 集成了稳定币生息产品，钱包内一键参与。
- **Swap 聚合**：内置跨链 / 多 DEX 聚合，不用跳来跳去。

## USDC 跨链 —— 丝滑体验（重点卖点）

**场景**：你只持有 BASE 上的 USDC，但你想参加 SOLANA 上的某个机会（比如打新、参与某个 pool、抢某个 launch）。

**传统做法**（麻烦）：BASE 上的 USDC → 通过跨链桥（Wormhole / Stargate 等）→ 等桥接确认 → 到 SOLANA → 可能还要 Swap 成目标代币 → 才能参与。过程中要切网络、要付多次 gas、要等分钟到数十分钟。

**DeGate 做法**：**任意链的 USDC 之间秒级互转，无缝跨链**。钱包内一键完成，不需要理解桥接 / 不需要等确认块 / 不需要担心桥安全性细节。

**这解锁了什么**：
- 你的**资金可以留在你最熟悉 / gas 最便宜 / 最安全的链**（比如 BASE）
- 哪条链上出机会，资金秒到哪条链
- 普通用户第一次可以像用 CEX 内部转账那样**无摩擦在多链之间移动 USDC**
- 不再需要"这条链上预留点 USDC 以防万一"的习惯

对目标用户（合规焦虑 + 想自托管 + 但怕操作复杂的人）来说，这是一个**"自托管不用牺牲 CEX 的便利"**的最直观证据。

## 在 5A 话题下各自怎么自然带入（三市场通用范例）

这是"当话题走到这个方向时"的切入思路，**不是模板**。每个市场的具体钩子句见对应 `markets/{xx}.md`。

### 合规焦虑
- 不要直接说 "用 DeGate 就不用担心 CARF/DAC8/ATO"（错且违规）
- CA 示例："Now that CARF is coming, CEX reporting is a lot more comprehensive. I've been slowly moving some to self-custody — been trying MetaMask, Safe, and DeGate. DeGate has swap and market making built in which is nice for someone lazy like me. Still have to do Schedule 3 either way though."
- AU 示例："With ATO's data matching getting tighter every year, I'd rather have a clean record of my own activity. Been testing a few wallets — MetaMask, Safe, DeGate. DeGate's the most all-in-one. Doesn't change what I need to report to ATO but makes MY records cleaner."
- FR 示例："Avec DAC8 qui arrive, autant avoir la main sur mes données moi-même. J'essaie quelques wallets — Rabby, Safe, DeGate. DeGate intègre swap et market making ce qui est pratique pour un flemmard comme moi. Ça change rien à ma déclaration 2086 évidemment."
- **核心转化点**：从"CEX 焦虑"→"我想更多自托管"→"自托管其实不麻烦"

### 自托管意识 / FTX 教训
- "Post-FTX I really don't want to keep coins on exchanges long-term. Mainly on self-custody now — when picking I care about multi-chain support and whether I can do LP / yield in the same place. DeGate covers both."

### DEX / Swap 需求
- "Bouncing between chains and bridges is exhausting. Been trying DeGate lately because of the built-in aggregator — USDC between BASE and Solana is instant, saves a ton of hassle."

### 稳定币理财
- "Keep a chunk of USDC / EURC in self-custody earning yield. DeGate has built-in products so I don't have to research every DeFi protocol myself — good enough for someone who doesn't want to go down that rabbit hole."

### LP 做市 / 区间宝
- "Managing Uniswap v3 ranges manually is exhausting — constantly watching price, rebalancing. DeGate's range vault productizes the flow, a lot less headache."

### 6a · anon-on-off-ramp（隐私出入金）—— 严格走"事实澄清 + 自托管反框架"
- **不要**给绕监管步骤、不要推 mixer / 非 KYC 服务
- 真实事实：链上交易**公开可追**，CEX 在 DAC8 / CARF 下自动上报提现目的地址。"自托管 + KYC 出金"是合规可行的姿态，"自托管 + 完全匿名"通常会撞上 P2P 风险或 AML 红旗
- 切入示例（CA/AU/FR 通用思路）：
  > "I get the privacy concern but worth knowing — the chain is public, and CEX withdrawals get reported to the tax authority either way under CARF/DAC8. Self-custody helps you control YOUR records, not avoid reporting. If you're worried about audit, the cleaner path is keep coins in self-custody (Rabby/Safe/DeGate are three options I've been trying) + file properly when you cash out, rather than trying to break the on-chain trail."
- **关键**：哪怕用户帖子在问"怎么完全匿名"，回帖也要把话题拉回到"清晰记录 + 合规出金 = 长期最省事"，否则人设崩

### 6b · rwa（链上美股 / 代币化股票）
- 切入示例：
  > "I've been watching xStocks and Backed Finance too. Honestly the interesting part isn't 'buy US stocks without a broker' (that's still grey area in most countries — your local securities regulator may have something to say), it's that the wrapper is on-chain so you can use it in DeFi. DeGate's swap aggregator handles xStocks pairs which is convenient if you're moving in and out."
- 这类 lead 通常 fit=medium —— 用户对话题感兴趣但对监管风险敏感，回帖姿态 = **兴趣而非 hype**
- 法律红线：不要正面给"绕开本地证券监管买美股"的步骤，每个市场的证券法不同（CA = CSA / 各省 securities commission；AU = ASIC；FR = AMF）

## 待补充（后续优化方向）

以下维度 DeGate 团队补数据 / 卖点后，可以追加进这份文档：

- 支持的链列表（截至目前）
- Swap 聚合覆盖的 DEX 数量 + 实际滑点 / 费率 benchmark
- USDC 跨链的底层机制简述（CCTP / 内部流动性池 / 其他？）
- 区间宝的再平衡策略、历史回测收益
- 稳定币理财产品清单 + APY 范围 + 底层协议
- 安全审计、bug bounty、历史事件记录
- UI / UX 的独特点（如果有 —— 例如一键操作流、Gas 估算等）
- 移动端 / 浏览器插件 / 硬件钱包兼容情况
- 社区 / 文档 / 客服质量

补充时请注明数据来源或更新日期，方便下次复核是否过时。
