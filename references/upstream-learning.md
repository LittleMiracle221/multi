# Upstream Learning Playbook

上游来源：[`RickyShiJs/italy_intel`](https://github.com/RickyShiJs/italy_intel)

这个文件只记录“可迁移的方法”，不机械复制意大利本地结论。

## 使用原则

- 只吸收对 `AU` / `CA` / `FR` 都有帮助，或至少对其中一个市场有帮助的方法
- 优先关注：渠道扩展、查询词设计、去重策略、输出 schema、叙事框架、自动化方法
- 不直接迁移：只对意大利法规、税表、论坛生态成立的本地细节
- 每次更新都要回答一个问题：这会不会让我们更快找到更好的本地线索？

## 最近一次人工结论

- 2026-04-27（Asia/Shanghai）首次建立同步基线，并人工吸收上游最新提交 `cadbf89`（提交时间：2026-04-27 16:51:42 +08:00，标题：`thread telegram into daily report pipeline`）。
- 这次真正可迁移的不是“意大利 Telegram 群名单”，而是接入方法：
- Telegram 一旦接入，不应被当成旁路补充，而应作为和 Reddit / X 平行的正式 lead 来源。
- Telegram 消息进入日报前，应走和 Reddit / X 相同的 §2 过滤打分与 §4 `daily_themes` 聚类管线，而不是单独写一套规则。
- `coverage_gaps` 的最佳实践是区分“固定未接入”和“已接入但本期运行失败”。当前 AU / CA / FR 仍未接入 Telegram，所以 `telegram` 仍是固定 gap；未来一旦接入，应改成运行失败时才出现的 `telegram_{market}_..._failed`。
- 多渠道统一规则要继续坚持：没有真实可打开 URL 的内容不入 lead；流式平台（Twitter / Telegram）默认不做 evergreen。

## 可迁移方法池

### 渠道与信号源

- Telegram 值得作为下一个正式接入渠道，前提不是“能抓到消息”，而是“抓到的消息能无缝进入现有 lead schema 和 scoring pipeline”。
- Telegram 的价值更接近高噪声实时讨论流，不应像论坛老帖那样承担 evergreen SEO 角色。
- 真正的渠道接入完成标准应写成三件套：
- 有稳定抓取方法
- 有可映射到统一 lead schema 的字段
- 有失败降级约定，不让单渠道故障拖垮整份日报

### 查询词与提示词

- 待补充

### 数据清洗与去重

- Telegram / X / Reddit 应继续共享“无真实 URL 不入 lead”的底线。
- 新渠道接入后先做字段映射，再进入统一去重与 fit 评分流程，避免下游逻辑分叉。

### 输出结构与评分

- `platform` 字段的演进应以统一下游消费为目标，而不是按渠道散写。
- `coverage_gaps` 应分两类：
- 固定 gap：能力尚未接入
- 条件性 gap：能力已接入，但本期因 session、限流、私有群、权限等原因失败
- 流式平台默认 `evergreen=false`，不要把 Telegram / X 的短消息错误塞进长尾 SEO 逻辑。

### 合规叙事与软营销

- 待补充

## 市场映射

### AU

- 后续若接入 Telegram，优先考虑本地交易 / 税务焦虑讨论群，而不是只盯项目官方群。
- 接入时应直接沿用 Reddit / X 的 fit 评分，不为 Telegram 单独发明“群热度”逻辑。

### CA

- 加拿大市场尤其适合把 Telegram 当成补充性的“实时焦虑流”，用于补 Reddit 节奏偏慢的问题。
- Quebec 相关法语讨论若来自 Telegram，也应按现有 `reply_draft_fr` 逻辑进入同一 schema。

### FR

- 法国市场天然更适合试 Telegram，因为散户加密讨论常更偏聊天群而不完全在 Reddit 上。
- 但仍应坚持“可打开 URL + 可审计字段 + 同一评分管线”，避免把 Telegram 变成不可复核的黑盒来源。

## 待实验项

- 评估 AU / CA / FR 各自最值得接入的 1-3 个 Telegram 公共或可加入群。
- 设计多市场版 Telegram 字段映射：`channel / posted_at / sender / url / views / forwards / replies / reactions_total / text`。
- 接入时同步更新 `references/output-schema.md` 与 `SKILL.md`，并把 `coverage_gaps` 从固定 `telegram` 迁移到条件性失败命名。
