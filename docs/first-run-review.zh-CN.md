# 首轮运行审查：bench-workbuddy 走完完整链路

[English](first-run-review.md) | 简体中文

- **运行日期**：2026-08-13
- **执行 Agent**：`bench-workbuddy`
- **任务**：[agent-collab-hub#1](https://github.com/finnyoun9/agent-collab-hub/issues/1)
- **分支**：`agent/bench-workbuddy/1-first-run-review`
- **相关决策**：[D-001](https://github.com/finnyoun9/agent-collab-hub/blob/main/DECISIONS.md)

## 1. 本次跑通了什么

这是对 [docs/WORKFLOW.md](WORKFLOW.md) 定义的协作链路的第一次完整走通：

```text
任务 issue -> CLAIM -> 独立分支 -> 证据产物 -> PR -> HANDOFF
```

每一步都通过原生 `gh` CLI 和仓库自带的 `scripts/collab.py` 执行，凭据只通过进程环境注入。本次运行产出了这份审查文档、中文版、一个 PR 和一条结构化 HANDOFF 评论。

## 2. 证据基线

| 检查项 | 结果 |
|---|---|
| `python scripts/collab.py agents` | 4 个 agent，与 `config/agents.json` 一致 |
| `python scripts/collab.py doctor` | repo/branch/remote/clean 报告正确 |
| `python scripts/collab.py doctor` | `GitHub API write credential: not set`（误报） |
| `python scripts/collab.py route --needs local,research --prefer low-cost` | bench-workbuddy、mac-claude-vscode、bench-codex |
| `python -m unittest discover tests -v` | 10 个测试全部通过 |
| `gh issue create ... --label state:triage` | issue #1 创建成功 |
| `python scripts/collab.py claim 1 --agent bench-workbuddy ...` | CLAIM 评论已发布到 issue #1 |
| `git fetch origin && git switch -c agent/bench-workbuddy/1-first-run-review` | 从 origin/main 创建分支 |

## 3. 在链路内发现的问题

以下是从 hub 路由给"边界清晰的本地工作"的那个 agent 的视角观察到的。没有一条会阻断链路，但每条都在消耗时间或给下一次运行带来风险。

### 3.1 `doctor` 对可用的 GitHub 凭据误报

`command_doctor` 只检查 `GH_TOKEN` / `GITHUB_TOKEN` 环境变量。本次运行通过 `gh auth`（keyring）认证，写操作（`collab.py claim`）实际成功，但 `doctor` 仍然输出：

```text
GitHub API write credential: not set
```

建议修复：当 token 环境变量缺失时，改用 `gh auth status` / `gh api user` 探测，并打印实际生效的认证来源。

### 3.2 测试套件缺少依赖声明

`tests/` 是 `unittest` 风格，零额外依赖即可运行（`python -m unittest discover tests -v`），这点很好。但仓库完全没有依赖元数据：没有 `requirements.txt`、没有 `pyproject.toml`、没有 `setup.cfg`。`pytest` 不是必需的，缺的只是"怎么跑测试"这一行说明。建议加一个带 `[project]` 表和 `[tool.pytest]` 提示的 `pyproject.toml`，或至少在 README 里写一句。

### 3.3 工具文档把 `route` 放在最前，但第一个真实需求是 `status`

快速开始展示的是 `route`、`agents`、`doctor`。实际上 agent 或人问的第一个问题是"现在有哪些任务开着？"，也就是 `collab.py status`。建议把 `status` 挪进快速开始，并在旁边写清楚标签词表（`state:*`、`agent:*`、`need:*`、`risk:*`）。

### 3.4 issue 表单没有采集 `need:*` 能力标签

表单只有一个"Primary capability"下拉和自由文本 scope，但路由协议（`route --needs ...`）消费的是能力关键字（`need:vision`、`need:local`……）。从表单创建的任务因此需要人工规范化标签才能可靠路由。建议在表单里加一个 `need:*` 多选，并注明 `state:triage` 是入口状态。

### 3.5 CLAIM 租期在工具侧没有校验和展示

`collab.py claim` 只写入租期时间戳，不校验租期是否在未来，`status` 也不展示到期时间。协议规定过期租期可以被回收（AGENTS.md），但没有任何工具输出帮助协调者看到某个 issue 的租期已过期。建议在 `status` 输出中展示 `lease until`，并在过期时告警。

### 3.6 分支命名对跨设备 worker 约束不足

`agent/<agent-id>/<issue>-<short-name>` 本身没问题，但没有任何机制防止两台机器上的不同 agent 为同一 issue 撞到同名分支。协议已有"一个 issue 只有一个负责人"，所以这是软风险，但加一道小防线更好：明确分支创建必须是 `git fetch origin && git switch -c <branch> origin/main`（workflow 文档已写），并在 CLAIM 前可选执行 `git ls-remote --exit-code origin <branch>` 检查。

### 3.7 飞书卡片预览没有按协议评论做过滤

`notify_feishu.py` 预览每一条新 issue 评论的正文。正常链路的 CLAIM、HEARTBEAT、HANDOFF 评论没问题，但协议外的闲聊也会进飞书。建议把预览过滤到以协议关键字开头的评论（`CLAIM`、`HEARTBEAT`、`HANDOFF`、`BLOCKED`、`RECLAIMED`），其余评论只发一条泛化的"新评论"卡片。

## 4. 做得好的地方

- `unittest` 风格的测试套件在 Windows、macOS、Linux 上零依赖可跑；将来加 CI 只需一行。
- 双语约定在 README、workflow 文档、issue 模板、PR 模板、CLI 消息和飞书卡片中贯彻一致，且由 `tests/test_bilingual_docs.py` 强制。
- `collab.py claim` 和 `collab.py handoff` 产出的正是协议要求的可解析标题；从文档复制粘贴更慢更容易出错。
- CLAIM 评论流程在任何编辑发生之前就强制了"一个负责人、一个分支"的纪律。

## 5. 下一轮迭代建议

按预期影响排序：

1. **修复 `doctor` 的认证检测**（3.1）——每个 agent 在新机器上跑的第一条命令，目前会对一个可用环境撒谎。
2. **给 issue 表单加 `need:*` 标签多选**（3.4）——路由质量依赖结构化能力，而不是自由文本。
3. **在 `status` 中展示租期到期**（3.5）——回收过期租期目前完全不可见。
4. **在明显位置声明测试调用方式**（3.2）——将来的 agent 不应该靠读测试文件才知道怎么跑。
5. **把飞书通知限定到协议评论**（3.7）——保持人工通道的高信噪比。

建议负责人：`bench-codex`（协调/集成），其中边界清晰的实现部分可由 `bench-workbuddy` 或 `mac-claude-vscode` 承接。

## 6. 学习证据

- 新技术：以低成本 worker 的视角完整走一遍本 hub 的 claim-分支-PR-handoff 链路，并把发现沉淀为持久产物。
- 可复现产物：本文档、issue #1、分支和 PR。
- 被证据纠正的错误假设：`git` 必须走环境代理，而 `gh api` 不做显式配置也能通；网络排障应写进每个 agent 的上手清单。

## 7. 运行事故记录（重要）

本次运行中途本地 git 元数据损坏了两次。第一次发生在修复 unborn HEAD 状态时：手动移动工作区文件的操作破坏了 `.git` 目录内容，git 不再识别仓库。第二次在 `git init` + `fetch` 重建后再次出现同样的 unborn-HEAD 症状——分支 ref 没有写入。两次都通过从远端重建本地仓库恢复。

- **事故原因**：修复 HEAD 期间手动移动/删除工作区文件、反复重建 `.git`；在文件尚未提交的目录上执行 `git init` 会让 HEAD 指向不存在的 ref。
- **恢复方式**：`rm -rf .git && git init -b main && git remote add origin <url> && git fetch origin main && git checkout -b <branch> origin/main`。
- **教训**：修复 git 状态时绝不要移动或删除工作区文件，只用 `git switch -c <branch> origin/main`；任何破坏性 git 操作前先验证 `.git` 完整性；产物文件要放在 git 修复步骤够不到的地方。
- **改进建议**：这次事故正好验证了 D-001——GitHub 作为唯一事实来源，本地仓库损坏可以无损恢复。建议在 WORKFLOW 文档补充"本地仓库损坏恢复"一节，并写明：全新克隆上第一次建分支必须发生在任何本地提交之前。
