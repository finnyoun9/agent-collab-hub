# Agent Collab Hub

[English](README.md) | 简体中文

这是一个轻量的异构 Agent 协作控制层。Hermes 作为常驻入口和调度器，
OpenCode、Codex、Pi、WorkBuddy 和 Claude 客户端继续使用各自原生能力。
Hub 只负责选择主执行 Agent、隔离并发写入，并记录简短结果。

## 推荐架构

```text
你 / 飞书
  -> Hermes（接收、定时、记忆、分派）
  -> OpenCode（默认本地编码）
  -> Codex（复杂集成、恢复、高风险任务）
  -> Pi（extension / RPC 实验）
  -> WorkBuddy（交互式备用执行者）
  -> Claude（视觉、架构、长上下文）
```

各 Agent 可以使用自己的 subagent，但内部 subagent 不得再次通过 Hub 分派。
主执行 Agent 负责汇总所有子任务并返回一个最终结果。

## 快速开始

```powershell
python scripts/collab.py --lang zh agents
python scripts/collab.py --lang zh route --needs local,code --prefer low-cost
python scripts/collab.py --lang zh doctor
```

Agent 名单和默认路由只在 [config/agents.json](config/agents.json) 中维护。
新增 Agent 后不需要再修改 Coordinator 源码。

## 工作模式

- 普通低风险任务使用快速模式：一个主 Agent 直接完成，简短汇报即可。
- 模糊或跨模块任务可以由第二个 Agent 做快速查漏补缺。
- 部署、密钥、硬件、破坏性操作和高风险改动使用受控模式，要求独立工作区、适当验证和复核。
- 顺序执行的 Agent 可以复用干净 checkout；只有并发写入时才创建独立 worktree 或 clone。

详细 CLI 接入和路由见 [docs/LOCAL-AGENTS.md](docs/LOCAL-AGENTS.md)，协作协议见
[docs/WORKFLOW.zh-CN.md](docs/WORKFLOW.zh-CN.md)，飞书接入见
[docs/FEISHU.zh-CN.md](docs/FEISHU.zh-CN.md)。

密钥只放环境变量或密钥存储，不写入 Issue、日志或仓库文件。
