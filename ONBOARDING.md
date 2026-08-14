# Agent 快速上手指南

> 给新加入的 agent（bench 上的 hermes / opencode / codex / pi / workbuddy，Mac 上的 Claude）看的。
> 目标：**5 分钟内理解协作机制，认领任务开干。**

## 你是谁，你该干什么

先看 [config/agents.json](config/agents.json) 里自己的 `id` 和 `capabilities`，确认哪些任务适合你。
也读 [docs/LOCAL-AGENTS.md](docs/LOCAL-AGENTS.md) 了解 bench 的 CLI 适配和派单模型。

## 第一步：读这三个文件（必读）

1. [README.md](README.md) — 整体设计
2. [docs/WORKFLOW.md](docs/WORKFLOW.md) — fast / controlled 两档模式、路由规则
3. [AGENTS.md](AGENTS.md) — 跨 agent 操作契约（开工/所有权/交接/证据/安全）

## 第二步：按任务风险选模式

### Fast mode（默认，低风险本地活）

```text
task -> primary worker -> change/result -> optional gap check -> done
```

- 不需要分支、PR、租约或独立 review
- 干完报告：改了什么、命令是否失败、已知缺口
- 选 worker：普通编码 → `bench-opencode`；自动化/调度/记忆 → `bench-hermes`

### Controlled mode（部署、凭据、烧录硬件、破坏性操作、高风险、并发写）

1. 在 Issue 下评论 `CLAIM`（agent id、目标仓库、分支、涉及文件、租约到期）
2. 建独立分支/worktree，只动 `allowed scope`
3. 按风险配比做验证，高风险换不同 agent review
4. 合入/发布/破坏性操作保留人工批准

## 第三步：交付

- 普通任务：在 Issue 评论里按 `HANDOFF / VERIFIED / NOT VERIFIED / NEXT` 格式总结
- 硬件/测量任务：必须有日志、CSV、波形或照片证据
- 认领了 Issue 的任务，完成后把标签置为 `state:done`

## 红线（违反会被打回）

- 不编造验证结果（真机结果必须有日志/CSV/波形/照片证据）
- 不把未实机验证的东西写成"已验证"
- 不碰 `do not touch` 范围
- 不直接 commit 到 main（受控模式必守；fast mode 的普通结果走 Issue 汇报）
- 不把密钥/路径泄露进 Issue 或 PR
- hub 不递归派发 worker 的 subagent：选定的主 worker 拥有全部子工作，只返回一个结果

## 常见环境坑

- bench 上非交互 SSH 不 source `.bashrc`，用 `export PATH="$HOME/.local/bin:$PATH"` 或全路径
- 平台过滤的 skills（`platforms: [macos]`）在 Linux 上不可见
- 仓库都是独立 git repo，认领哪个仓库的任务就去哪个仓库建分支，PR 提交到**目标仓库**，不是 hub
- 不维护每个 agent 一个常驻 clone；顺序任务可复用干净 checkout，并发写才开独立 worktree
