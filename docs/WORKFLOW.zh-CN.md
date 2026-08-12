# 协作流程

[English](WORKFLOW.md) | 简体中文

## 信息放在哪里

| 载体 | 唯一可信内容 |
|---|---|
| GitHub Issue | 目标、范围、负责人、依赖、验收标准 |
| Branch/worktree | 单个 Agent 的代码改动 |
| Pull Request | 审查讨论和合并门禁 |
| 飞书 | 通知、快捷指令、人工决定入口 |
| 项目文档 | 稳定架构和已验证知识 |
| [DECISIONS.md](../DECISIONS.md) | 已确定、无需反复讨论的结论 |

飞书聊天不是项目状态的唯一事实源。重要结论必须回写 Issue、PR、`DECISIONS.md` 或项目文档。

## 本地工作区隔离

即使 Agent 在同一台电脑上并发运行，也必须各用一个独立 clone。一个 checkout 中的不同分支仍会共享 `HEAD`、暂存区和工作目录文件，不能作为并发隔离边界。

常驻 coordinator 或其他服务再使用一个专用运行副本：

```text
agent-collab-hub-codex/        # Codex 开发
agent-collab-hub-workbuddy/    # WorkBuddy 开发
agent-collab-hub-coordinator/  # 只运行服务，Agent 不在这里开发
```

每个开发副本内部仍按“一项 Issue 一个任务分支”工作。Agent 之间只通过 commit、push、Pull Request 和 Issue 评论交换成果。仓库异常时，不得通过删除 `.git`、在原目录执行 `git init` 或手工写 Git refs 来原地修复；应保留现场用于诊断，并重新 clone 到新目录。

## 状态流转

```text
triage -> ready -> claimed -> in-progress -> review -> verify -> done
                         \-> blocked -----/
```

## 路由原则

1. 纯视觉任务优先给 `mac-claude-client`。
2. 低风险、边界清晰、可测试的本地编码默认给 `bench-workbuddy`。它可以在自己的独立 clone 中修改、测试、commit、push、创建 PR 并发布 `HANDOFF`。
3. 硬件烧录和测量给 `bench-codex`。
4. 架构和开放式调研给 `mac-claude-client`，主控再把结论转成可执行任务。
5. 高风险或跨模块工作交回 `bench-codex` 集成。
6. 条件允许时，作者和审查者使用不同模型或客户端。

WorkBuddy 不得合并 PR、直接提交 `main`、部署、发布、处理密钥、烧录硬件、破坏性操作设备、删除或重建 `.git`、手工写 Git refs，也不能超出已领取范围。这些操作必须交回主控或人工审批边界。

## 领取与租约

Agent 开工前必须发布结构化 `CLAIM`。长任务在 lease 到期前发布一次 `HEARTBEAT`。过期任务只能由主控发布 `RECLAIMED` 后重新分配。

任务分支必须在该 Agent 自己的 clone 中从最新 `origin/main` 创建。

协议关键字和字段名固定使用英文，内容可以使用中文或英文：

```text
CLAIM
Agent: mac-claude-vscode
Target: owner/project
Branch: agent/mac-claude-vscode/42-short-name
Files: src/foo.c, tests/test_foo.py
Lease until: 2026-08-13T20:00:00+08:00
```

## 交接

交接必须包含 branch、commit、PR、改动文件、验证结果、未验证内容和下一步：

```text
HANDOFF
Agent: mac-claude-vscode
Branch: agent/mac-claude-vscode/42-short-name
Commit: abc1234
PR: https://github.com/owner/project/pull/7
Changed: src/foo.c, tests/test_foo.py

VERIFIED
- `pytest tests/test_foo.py`: 8 passed

NOT VERIFIED
- 目标硬件时序

NEXT
- bench-codex：运行硬件验收测试并记录证据
```

## 学习任务

“学习 DMA”太虚，应该改成“在当前开发板实现 UART RX circular DMA，提交最小固件、接线说明和可复现丢包测试”。聊天总结不算完成，必须留下代码、测试、实验记录、图或决策记录。
