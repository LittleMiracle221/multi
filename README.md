# DeGate Multi-Market Intel

这个仓库用于持续扫描加拿大、澳大利亚、法国的加密与个人财经社区，并把对 DeGate 有价值的讨论转成可执行的调研与内容动作。

## 现在多了一层什么

除了原有的 Reddit / xAI 扫描脚本，这个仓库现在增加了一层“上游方法学习”流程，用来跟踪并吸收意大利市场任务仓库的更新：

- 上游来源：`https://github.com/RickyShiJs/italy_intel.git`
- 关注重点：方法、技能、渠道、提示词、工作流、输出结构
- 忽略重点：只对意大利本地成立、无法迁移到 AU / CA / FR 的纯本地细节

## 新增目录

- `scripts/sync_italy_intel_upstream.py`
  - 拉取/更新上游 GitHub 仓库
  - 检测是否有新 commit
  - 生成本地 diff 存档和更新记录
- `references/upstream-learning.md`
  - 作为长期维护的“迁移学习 playbook”
  - 记录哪些方法可复用到 AU / CA / FR
- `upstream_sync/runs/`
  - 每次检测到更新后生成一份运行记录

## 推荐使用方式

### 1. 首次准备

复制环境变量模板：

```bash
cp .env.example .env
```

填好 `.env` 中的 Reddit 和 xAI key。

如果上游仓库是私有的，建议同时设置：

```bash
ITALY_INTEL_REPO_URL=git@github.com:RickyShiJs/italy_intel.git
```

这样同步脚本会优先走你本机已有的 SSH 凭证，而不是卡在 HTTPS 用户名/密码流程。

### 2. 初始化为 Git 仓库并推到 GitHub

如果这是第一次上传：

```bash
git init -b main
git add .
git commit -m "Initial import: degate multi-market intel"
git remote add origin <你的 GitHub 仓库地址>
git push -u origin main
```

### 3. 手动检测上游是否更新

```bash
python3 scripts/sync_italy_intel_upstream.py
```

前提条件：

- 你的机器对上游仓库有读取权限
- 如果是私有仓库，优先用 SSH remote
- 本地 `git` 能直接访问该仓库而不弹交互式登录

返回值说明：

- `NO_CHANGE::<commit>`：上游没有新变化
- `UPDATED::<summary_path>::<patch_path>`：发现更新，并已生成本地记录
- `BOOTSTRAPPED::<commit>`：首次建立上游基线

### 4. 检测到更新后怎么处理

建议按这个顺序：

1. 打开 `references/upstream-learning.md`
2. 查看最新的 `upstream_sync/runs/*.md`
3. 根据变更，把可迁移的方法整理到 AU / CA / FR 三个市场
4. 如有必要，更新 `references/markets/*.md` 或你的执行脚本
5. 提交并推送到你的 GitHub 仓库

## 适合自动化的任务

这个仓库很适合配一个定时任务，每天或每个工作日运行一次：

1. 执行 `python3 scripts/sync_italy_intel_upstream.py`
2. 若检测到更新：
3. 阅读最新 diff
4. 更新 `references/upstream-learning.md`
5. 如果确认对 AU / CA / FR 有帮助，再提交并 push

这样可以避免把“意大利本地变化”机械同步进来，而是只同步可迁移的方法论。
