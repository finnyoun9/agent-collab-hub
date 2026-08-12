# Agent Collab Hub

[English](README.md) | 简体中文

一个轻量的跨电脑异构编码 Agent 协作控制层。它用 GitHub Issues 做任务队列，独立分支和 Pull Request 做交付边界，飞书负责通知和人工指令入口。

这个仓库不运行或代理模型。Codex、Claude Code、WorkBuddy 和 API Agent 继续使用各自原生客户端；本项目只统一任务路由、领取、交接、证据和审查协议。

## 工作流

```text
飞书 / 人工需求
      |
      v
GitHub Issue（任务 + 验收标准）
      |
      v
路由器 -> 单一负责人 -> 独立分支/worktree
      |
      v
PR + 测试证据 -> 独立审查 -> 集成
      |
      v
飞书通知 + 长期决策/学习记录
```

## 快速开始

```bash
python scripts/collab.py --lang zh agents
python scripts/collab.py --lang zh route --needs local,code --prefer low-cost
python scripts/collab.py --lang zh doctor
```

也可以设置默认语言：

```bash
export COLLAB_LANG=zh
```

PowerShell：

```powershell
$env:COLLAB_LANG = "zh"
```

读写 GitHub Issue 时，凭据只能通过进程环境传入，不能提交到仓库：

```bash
export GH_TOKEN="..."
python scripts/collab.py --lang zh status --repo finnyoun9/agent-collab-hub
```

通过 GitHub 的 `Agent task / Agent 任务` 表单创建任务。协作协议见 [docs/WORKFLOW.zh-CN.md](docs/WORKFLOW.zh-CN.md)，飞书接入见 [docs/FEISHU.zh-CN.md](docs/FEISHU.zh-CN.md)。

## 当前 Agent 分工

| Agent | 最适合 | 主要限制 |
|---|---|---|
| bench Codex | 主控、集成、硬件验证 | 高价值额度 |
| bench WorkBuddy | 本地编码、重复工作、快速检查 | 不能识图 |
| Mac Claude client | 视觉分析、调研、架构审查 | 可能不能访问本地工作区 |
| Mac Claude VS Code | 本地编码和审查 | 当前 API 不能识图 |

能力变化时修改 [config/agents.json](config/agents.json)。

## 核心约定

- 一个任务只有一个负责人和一个分支。
- Agent 通过可审查产物协作，不假设共享聊天记忆。
- `CLAIM` 是有期限的 lease，不是永久占有。
- 高风险改动的作者不能做最终审查。
- 硬件结论必须带实测证据。
- 调研只有转化成代码、测试、决策或可复现实验才算完成。
- 协议关键字保持英文，保证不同语言和模型都能稳定解析。
- 密钥只放环境变量或 GitHub/飞书 secret store。

所有文本文件和 CLI 输出统一使用 UTF-8，保证 Windows、macOS 和 Linux 上的中英文内容一致。

bench 上的飞书长连接协调器见 [coordinator/README.zh-CN.md](coordinator/README.zh-CN.md)。
