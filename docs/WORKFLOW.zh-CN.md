# 协作流程

[English](WORKFLOW.md) | 简体中文

## 核心原则

- Hermes 是常驻调度器，OpenCode 是默认本地编码执行者。
- Codex 处理复杂集成、失败恢复、硬件和高风险任务。
- Pi 用于 extension、RPC 和低上下文实验；WorkBuddy 是交互式备用执行者。
- 一个任务只选一个主执行 Agent。其内部 subagent 不再回到 Hub 分派。
- Agent 之间通过结果、Git diff、commit 或 Issue 评论接力，不假设共享聊天记忆。

## 快速模式

适用于普通、低风险、本地任务：

```text
任务 -> 主执行 Agent -> 修改/结果 -> 可选快速补漏 -> 完成
```

不强制独立 clone、PR、lease、完整测试或独立审查。执行者应说明改了什么、
是否遇到错误和已知遗漏。

## 受控模式

部署、密钥、硬件烧录、破坏性操作、高风险或并发冲突任务使用受控模式：

- 建立任务分支或 worktree；
- 明确允许范围；
- 运行与风险匹配的验证；
- 必要时由不同 Agent 复核；
- 合并、发布和破坏性操作保留人工边界。

顺序执行的 Agent 可以复用干净 checkout。只有两个 Agent 同时写入时才必须
使用独立 worktree 或 clone。Coordinator 的运行副本不用于开发。

## 路由

1. 自动化、定时、记忆和消息入口：`bench-hermes`。
2. 普通本地编码：`bench-opencode`。
3. 复杂集成、重复失败、硬件或高风险：`bench-codex`。
4. 自定义 harness、extension 或 RPC：`bench-pi`。
5. 视觉、架构和长上下文：Claude 客户端。
6. OpenCode 不可用或需要 IDE 交互：`bench-workbuddy`。

Agent 配置的唯一真源是 `config/agents.json`。
