# Agent 快速上手指南

> 给新加入的 agent（bench 上的 hermes / opencode / codex，Mac 上的 Claude）看的。
> 目标：**5 分钟内理解协作机制，认领任务开干。**

## 你是谁，你该干什么

先看 [config/agents.json](config/agents.json) 里自己的 `id` 和 `capabilities`，确认哪些任务适合你。

## 第一步：读这三个文件（必读）

1. [README.md](README.md) — 整体设计
2. [docs/WORKFLOW.md](docs/WORKFLOW.md) — 任务状态机、路由规则、CLAIM/HANDOFF 协议
3. [AGENTS.md](AGENTS.md) — 跨 agent 操作契约（开工/所有权/交接/证据/安全）

## 第二步：认领任务

1. 在 [Issues](https://github.com/finnyoun9/agent-collab-hub/issues) 列表找带 `state:ready` 标签、且能力匹配你（看 `agent:*` 标签）的任务
2. 在 Issue 下评论 `CLAIM`（格式见 WORKFLOW.md），声明分支、文件、租约到期时间
3. `git fetch origin && git switch main && git pull --ff-only && git switch -c agent/<你的id>/<issue号>-短名`

## 第三步：干活并交付

1. 只改你 CLAIM 里声明的文件，只动 `allowed scope`
2. 完成后开 PR，PR 描述用 `HANDOFF / VERIFIED / NOT VERIFIED / NEXT` 格式
3. PR 请求独立 review（尽量让不同 agent 审）
4. 合入后把 Issue 打上 `state:done`

## 红线（违反会被打回）

- 不编造验证结果（真机结果必须有日志/CSV/波形/照片证据）
- 不把未实机验证的东西写成"已验证"
- 不碰 `do not touch` 范围
- 不直接 commit 到 main
- 不把密钥/路径泄露进 Issue 或 PR

## 常见环境坑

- bench 上非交互 SSH 不 source `.bashrc`，用 `export PATH="$HOME/.local/bin:$PATH"` 或全路径
- 平台过滤的 skills（`platforms: [macos]`）在 Linux 上不可见
- 仓库都是独立 git repo，认领哪个仓库的任务就去哪个仓库建分支，PR 提交到**目标仓库**，不是 hub
