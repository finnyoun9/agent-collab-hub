# macOS Agent 协作流程

这是一个适合个人在 Codex Chat、VS Code 编码 Agent 和 GitHub 之间切换的小流程。GitHub 保存可持续的任务状态；不同 Agent 不假设彼此共享聊天上下文。

## 默认分工

| 角色 | 职责 |
| --- | --- |
| Codex Chat | 澄清目标、定义验收、整合结果、复核高风险修改。 |
| VS Code 编码 Agent | 在分配到的 worktree 或分支内实现一个边界明确的改动。 |
| 第二 Agent | 调研、测试或审查；返回证据或 patch，不悄悄修改负责人正在使用的文件。 |
| GitHub | Issue、分支/PR、commit 和简短 handoff 是跨会话记录。 |

一个任务只能有一个负责人。顺序工作可复用干净 checkout；只有并发写入时才建立独立 worktree。

## 任务循环

1. 任务跨会话、涉及多 Agent 或需要长期决策时，创建 GitHub Issue；小型单人改动可留在本地。
2. 负责人写清目标、精确文件/范围、验收条件、基线 commit，以及哪个 Agent 有写入权。
3. 给执行 Agent 一个边界明确的任务；不要只说“把机器人做完”。
4. 执行 Agent 在分支提交、运行相关验证并写 handoff；只有风险或不确定性需要时才引入第二 Agent 审查。
5. 负责人整合结果，记录已经验证的事实和仍属于假设的内容。

## 并发 worktree

```bash
git fetch origin
git worktree add ../mecanum-robot-motor-bringup -b agent/motor-bringup origin/main
```

把新目录交给第二个 Agent。不要让两个编码 Agent 同时修改同一个 checkout 或同一批文件。合并完成且确认不再需要后，再移除对应 worktree。

## Handoff 模板

```text
Goal:
Branch + commit:
Files changed:
Verified: command / hardware setup / observed result
Not verified:
Next smallest step:
```

硬件任务的 `Verified` 必须包含板卡、固件 commit、接线或仪器，以及测量观察。仿真或 AI 推演在复现之前一律写入 `Not verified`。

## 推荐的第一次实践

针对麦克纳姆轮机器人：一个 Agent 负责 P0 文档与接线审查，另一个 Agent 只审查 PWM/编码器代码，首次真实上板仍由一个人负责。交付物是一条单轮测量证据，不是一轮多 Agent 讨论。
