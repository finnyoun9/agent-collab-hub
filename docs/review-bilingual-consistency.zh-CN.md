# 中英文一致性审查：README 与 WORKFLOW

[English](review-bilingual-consistency.md) | 简体中文

- **审查日期**：2026-08-13
- **审查者**：`bench-workbuddy`
- **任务**：[agent-collab-hub#10](https://github.com/finnyoun9/agent-collab-hub/issues/10)
- **分支**：`agent/bench-workbuddy/10-bilingual-doc-review`
- **被审查提交**：`0a70f8b`
- **审查范围**：
  - `README.md` 与 `README.zh-CN.md`
  - `docs/WORKFLOW.md` 与 `docs/WORKFLOW.zh-CN.md`

## 1. 方法

将每份英文文档与其中文版并排通读，逐一比较章节标题、段落、代码块、表格和链接，检查：

- 语义等价（中文是否表达了与英文相同的意思）；
- 结构等价（两份语言版本是否都有全部章节）；
- 协议关键字稳定性（`CLAIM`、`HANDOFF`、`VERIFIED` 等机器可读关键字是否在两个版本中都保持英文）。

未修改被审查的 README/WORKFLOW。本报告是唯一交付物。

## 2. 结论

**中英文对整体方向一致，协议关键字在两个版本中都正确保持英文。但是中文 WORKFLOW 文档相对英文原版存在四处实质内容缺口，且两对文档还有若干小的措辞/排版差异。**

严重级别：**M** = 内容缺失（中文不完整）、**D** = 措辞或排版差异（不影响含义）、**P** = 与协议相关（影响 Agent 或人的实际操作）。

## 3. 发现——docs/WORKFLOW.md 与 docs/WORKFLOW.zh-CN.md

### F1 [M, P] 中文 WORKFLOW 缺失 "Suggested labels" 章节

英文文档在 "Suggested labels" 下列出了完整标签词表：

```text
- state:triage, state:ready, state:claimed, state:review, state:verify,
  state:blocked, state:done
- agent:bench-codex, agent:bench-workbuddy, agent:mac-claude-client,
  agent:mac-claude-vscode
- need:vision, need:local, need:hardware, need:research, need:review
- risk:low, risk:medium, risk:high
```

中文版有"状态流转"图，但**完全没有标签词表**。issue 模板把该词表作为建议标签引用；需要给任务打标签或按标签筛选的、只读中文文档的 Agent，无法从中文版学到标签约定。

### F2 [M, P] 中文 WORKFLOW 缺失建分支命令

英文 Claim 章节包含创建分支的确切命令：

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c agent/mac-claude-vscode/42-short-name
```

中文版只展示 `CLAIM` 评论格式，说"Agent 开工前必须发布结构化 CLAIM"，但没有建分支命令。只读中文文档的 Agent 必须自己猜测分支工作流。

### F3 [M] 中文 WORKFLOW 压缩了 Heartbeat 章节

英文有完整的 "Heartbeat and lease" 章节，含 `HEARTBEAT` 评论模板和指导"不要按分钟发心跳，在一个有意义的检查点发一次即可"。中文压缩成一句："长任务在 lease 到期前发布一次 `HEARTBEAT`。"明确的防噪音指导丢失了。

### F4 [M] 中文 WORKFLOW 压缩了学习任务章节

英文定义了可路由的学习任务完整形态：

```text
Goal: ...
Artifact: ...
Acceptance: ...
Reflection: ...
```

中文用一段压缩文字替代。让学习任务可验证的四字段模板在中文版中不存在。

### F5 [D] 章节标题本地化

英文 "Control surfaces" / "Task states" / "Routing rules" / "Claim" / "Heartbeat and lease" / "Handoff" / "Learning tasks" 对应中文 "信息放在哪里" / "状态流转" / "路由原则" / "领取与租约" / "交接" / "学习任务"。对人没问题，但注意 "Claim" → "领取与租约" 把英文的 "Claim" 和 "Heartbeat and lease" 两个章节合并了，这正是 F2/F3 内容丢失的部分原因。

### F6 [D] Handoff 示例中的 NEXT 行本地化

英文：`- bench-codex: run the hardware acceptance test and record evidence`
中文：`- bench-codex：运行硬件验收测试并记录证据` —— 语义等价；协议关键字保持英文。无需处理。

## 4. 发现——README.md 与 README.zh-CN.md

### F7 [D] `--lang zh` 的位置

英文 Quick start 先展示裸命令（`agents`、`route --needs ...`、`doctor`），再用单独的 "Use Chinese output with `--lang zh`" 块演示。中文 Quick start 把 `--lang zh` 内联进每条命令。语义一致；排版不同。无需处理。

### F8 [D] UTF-8 说明的位置

英文在 Quick start 中说明 "All text files and CLI output use UTF-8..."。中文把等价句子放在文档末尾。内容相同，位置不同。无需处理。

### F9 [D] COLLAB_LANG 示例

英文 Quick start 同时展示 `--lang zh` 和 `COLLAB_LANG=zh`。中文展示 `COLLAB_LANG=zh` 的 export 和 PowerShell 变体（`$env:COLLAB_LANG = "zh"`），而英文版对 `COLLAB_LANG` 没有 PowerShell 示例（英文的 PowerShell 示例只覆盖 `GH_TOKEN`）。轻微不对称；两份文档各自自洽。无需处理。

### F10 [D] Agent 表格措辞

"premium capacity" → "高价值额度"、"may lack local workspace access" → "可能不能访问本地工作区"、"no image input with current API" → "当前 API 不能识图"。翻译忠实。无需处理。

## 5. 影响与建议

| 发现 | 严重级别 | 建议动作 |
|---|---|---|
| F1 中文缺标签词表 | M, P | 在 WORKFLOW.zh-CN.md 补充标签词表 |
| F2 中文缺建分支命令 | M, P | 在 WORKFLOW.zh-CN.md 补充建分支命令 |
| F3 心跳指导被压缩 | M | 在中文版展开 Heartbeat 章节 |
| F4 学习任务模板被压缩 | M | 在中文版恢复四字段模板 |
| F5–F10 | D | 无需修改；供未来本地化参考 |

**建议**：以英文 WORKFLOW 为基准，把中文版补齐到对等（F1–F4）。README 这对无需修正。由于本任务是纯审查，修复项建议作为后续任务派给 worker Agent。

## 6. 证据

- 完整通读四份文件：`README.md`（97 行）、`README.zh-CN.md`（78 行）、`docs/WORKFLOW.md`（116 行）、`docs/WORKFLOW.zh-CN.md`（73 行）。
- 协议关键字（`CLAIM`、`HANDOFF`、`VERIFIED`、`NOT VERIFIED`、`NEXT`、`HEARTBEAT`、`RECLAIMED`）已验证在两个语言版本中都保持英文。
- 本报告提交在分支 `agent/bench-workbuddy/10-bilingual-doc-review` 上；未修改被审查的 README/WORKFLOW。
