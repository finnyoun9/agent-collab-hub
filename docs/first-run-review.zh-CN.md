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
| `python scripts/collab.py doctor` | `GitHub API write credential: not set`（该进程缺少直接 API token；`gh` 认证是另一条路径） |
| `python scripts/collab.py route --needs local,research --prefer low-cost` | bench-workbuddy、mac-claude-vscode、bench-codex |
| `python -m unittest discover tests -v` | 10 个测试全部通过 |
| `gh issue create ... --label state:triage` | issue #1 创建成功 |
| `python scripts/collab.py claim 1 --agent bench-workbuddy ...` | CLAIM 评论已发布到 issue #1 |
| `git fetch origin && git switch -c agent/bench-workbuddy/1-first-run-review` | 从 origin/main 创建分支 |

## 3. 在链路内发现的问题

以下是从 hub 路由给"边界清晰的本地工作"的那个 agent 的视角观察到的。没有一条会阻断链路，但每条都在消耗时间或给下一次运行带来风险。

### 3.1 `doctor` 没有说明 API token 与 `gh` 认证的区别

`command_doctor` 只检查 `GH_TOKEN` / `GITHUB_TOKEN` 环境变量。本次运行通过 `gh auth`（keyring）认证，写操作（`collab.py claim`）实际成功，但 `doctor` 仍然输出：

```text
GitHub API write credential: not set
```

对 `collab.py` 来说，这并不是误报：它的 `GitHubClient` 使用 Python `urllib` 发请求，写操作必须有 `GH_TOKEN` 或 `GITHUB_TOKEN`。`gh auth login` 存下的凭据可以让 `gh` 命令工作，但不会自动提供给这个 Python 客户端。因此，CLAIM 成功不能证明 `collab.py` 读取了 `gh` keyring；当次调用可能单独提供了 token，也可能通过另一条路径发布了评论。

建议把诊断项改名为 `collab.py write token (GH_TOKEN/GITHUB_TOKEN)`；如果需要，再单独显示 `gh auth status`。两条认证路径不能合并成一个结果。

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

1. **明确 `doctor` 的认证范围**（3.1）——区分 `collab.py` 使用的直接 API token 和 `gh` CLI 的独立凭据。
2. **给 issue 表单加 `need:*` 标签多选**（3.4）——路由质量依赖结构化能力，而不是自由文本。
3. **在 `status` 中展示租期到期**（3.5）——回收过期租期目前完全不可见。
4. **在明显位置声明测试调用方式**（3.2）——将来的 agent 不应该靠读测试文件才知道怎么跑。
5. **把飞书通知限定到协议评论**（3.7）——保持人工通道的高信噪比。

建议负责人：`bench-codex`（协调/集成），其中边界清晰的实现部分可由 `bench-workbuddy` 或 `mac-claude-vscode` 承接。

## 6. 学习证据

- 新技术：以低成本 worker 的视角完整走一遍本 hub 的 claim-分支-PR-handoff 链路，并把发现沉淀为持久产物。
- 可复现产物：本文档、issue #1、分支和 PR。
- 被证据纠正的错误假设：`gh` 命令能工作，不代表 `git` 或 `collab.py` 共用它的认证或代理路径；三条路径必须分别诊断。

## 7. 运行事故记录（重要）

首次运行和后续修复任务中，本地 Git 元数据被多次删除并重建。命令审计记录明确包含 `rm -rf .git`，其中也包括分支或 checkout 失败后由 Agent 提出的命令。没有证据表明 `git switch` 或 `git checkout` 会自行删除 `.git`，因此不能把事故记录成 Git 或文件系统 bug。

- **证据支持的原因**：在多个 Agent 共用的 checkout 中执行了破坏性恢复命令；随后原地重新初始化仓库并手工写 ref，又制造了更多无效或混乱的 Git 状态。
- **安全恢复方式**：停止修改受影响目录，保留现场用于诊断，在新目录重新 clone 远端仓库。复制任何未提交产物前，先用 `git status`、`git rev-parse HEAD` 和 `git fsck` 验证新副本。
- **教训**：不得原地删除或重建 `.git`，不得把 `git init` 当作已有 checkout 的修复手段，也不得手工写 `.git/refs`。并发运行的每个 Agent 使用独立 clone；常驻服务使用 Agent 不编辑的专用运行副本。
- **改进建议**：把“独立 clone + 新目录重新 clone 恢复”写成唯一支持流程。GitHub 继续作为持久交换点，但不能假设远端能恢复所有未提交的本地产物。
