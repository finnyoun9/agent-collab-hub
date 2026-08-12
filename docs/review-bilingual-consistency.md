# Bilingual consistency review: README and WORKFLOW

English | [简体中文](review-bilingual-consistency.zh-CN.md)

- **Review date**: 2026-08-13
- **Reviewer**: `bench-workbuddy`
- **Task**: [agent-collab-hub#10](https://github.com/finnyoun9/agent-collab-hub/issues/10)
- **Branch**: `agent/bench-workbuddy/10-bilingual-doc-review`
- **Reviewed commit**: `0a70f8b`
- **Scope reviewed**:
  - `README.md` vs `README.zh-CN.md`
  - `docs/WORKFLOW.md` vs `docs/WORKFLOW.zh-CN.md`

## 1. Method

Each English document was read side by side with its Chinese variant. Every
section heading, paragraph, code block, table, and link was compared for:

- semantic equivalence (does the Chinese say the same thing as the English?);
- structural equivalence (are all sections present in both languages?);
- protocol-keyword stability (are machine-readable keywords like `CLAIM`,
  `HANDOFF`, `VERIFIED` kept in English in both variants?).

The reviewed README/WORKFLOW files were not modified. This report is the only
deliverable.

## 2. Verdict

**The bilingual pair is directionally consistent and the protocol keywords are
correctly kept in English in both variants. However, the Chinese WORKFLOW
document has four substantial content gaps relative to the English original,
and there are several smaller wording/layout discrepancies across both pairs.**

Severity key: **M** = missing content (Chinese is incomplete), **D** = wording
or layout difference that does not change meaning, **P** = protocol-relevant
(affects how agents/humans operate).

## 3. Findings — docs/WORKFLOW.md vs docs/WORKFLOW.zh-CN.md

### F1 [M, P] Chinese WORKFLOW omits the "Suggested labels" section

The English document lists the full label vocabulary under "Suggested labels":

```text
- state:triage, state:ready, state:claimed, state:review, state:verify,
  state:blocked, state:done
- agent:bench-codex, agent:bench-workbuddy, agent:mac-claude-client,
  agent:mac-claude-vscode
- need:vision, need:local, need:hardware, need:research, need:review
- risk:low, risk:medium, risk:high
```

The Chinese variant has the "状态流转" (task states) diagram but **no label
vocabulary at all**. The label vocabulary is referenced by the issue template
as suggested labels; a Chinese-reading agent that needs to label or filter
tasks cannot learn the label contract from the Chinese doc.

### F2 [M, P] Chinese WORKFLOW omits the branch-creation commands

The English Claim section includes the exact commands to create the branch:

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c agent/mac-claude-vscode/42-short-name
```

The Chinese variant only shows the `CLAIM` comment format and says "Agent 开工
前必须发布结构化 CLAIM", without the branch-creation commands. An agent that
reads only the Chinese doc must guess the branch workflow.

### F3 [M] Chinese WORKFLOW compresses the Heartbeat section

English has a full "Heartbeat and lease" section with the `HEARTBEAT` comment
template and the guidance "Do not use minute-by-minute heartbeats. One update
at a meaningful checkpoint is enough." Chinese compresses this into one
sentence: "长任务在 lease 到期前发布一次 `HEARTBEAT`。" The explicit
anti-noise guidance is lost.

### F4 [M] Chinese WORKFLOW compresses the Learning tasks section

English defines the full routeable learning-task shape:

```text
Goal: ...
Artifact: ...
Acceptance: ...
Reflection: ...
```

Chinese replaces it with a single compressed paragraph. The four-field
template that makes learning tasks verifiable is not present in Chinese.

### F5 [D] Section title localization

English "Control surfaces" / "Task states" / "Routing rules" / "Claim" /
"Heartbeat and lease" / "Handoff" / "Learning tasks" map to Chinese
"信息放在哪里" / "状态流转" / "路由原则" / "领取与租约" / "交接" / "学习任务".
This is fine for humans, but note that "Claim" → "领取与租约" merges the
English "Claim" and "Heartbeat and lease" sections into one, which is part of
why F2/F3 content was dropped.

### F6 [D] NEXT line localization in Handoff example

English: `- bench-codex: run the hardware acceptance test and record evidence`
Chinese: `- bench-codex：运行硬件验收测试并记录证据` — semantically
equivalent; the protocol keywords stay English. No action needed.

## 4. Findings — README.md vs README.zh-CN.md

### F7 [D] `--lang zh` placement

English Quick start shows bare commands (`agents`, `route --needs ...`,
`doctor`) then a separate "Use Chinese output with `--lang zh`" block. Chinese
Quick start inlines `--lang zh` into every command. Semantically consistent;
layout differs. No action needed.

### F8 [D] UTF-8 statement position

English states "All text files and CLI output use UTF-8..." inside Quick start.
Chinese places the equivalent sentence at the very end of the document.
Same content, different position. No action needed.

### F9 [D] COLLAB_LANG example

English shows both `--lang zh` and `COLLAB_LANG=zh` in the quick start. Chinese
shows `COLLAB_LANG=zh` with export and a PowerShell variant
(`$env:COLLAB_LANG = "zh"`) that the English version lacks for `COLLAB_LANG`
(the English PowerShell example covers `GH_TOKEN` only). Minor asymmetry; both
documents are self-consistent. No action needed.

### F10 [D] Agent table wording

"premium capacity" → "高价值额度", "may lack local workspace access" →
"可能不能访问本地工作区", "no image input with current API" → "当前 API 不能识图".
All faithful. No action needed.

## 5. Impact and recommendation

| Finding | Severity | Suggested action |
|---|---|---|
| F1 labels missing in ZH | M, P | Add the label vocabulary to WORKFLOW.zh-CN.md |
| F2 branch commands missing in ZH | M, P | Add the branch-creation commands to WORKFLOW.zh-CN.md |
| F3 heartbeat guidance compressed | M | Expand the Heartbeat section in ZH |
| F4 learning-task template compressed | M | Restore the four-field template in ZH |
| F5–F10 | D | No change required; note for future localizers |

**Recommendation**: the English WORKFLOW should be treated as canonical and the
Chinese variant brought up to parity (F1–F4). The README pair needs no
correction. Because this task is review-only, the fixes are proposed as a
follow-up task for a worker agent.

## 6. Evidence

- All four files read in full: `README.md` (97 lines), `README.zh-CN.md`
  (78 lines), `docs/WORKFLOW.md` (116 lines), `docs/WORKFLOW.zh-CN.md`
  (73 lines).
- Protocol keywords (`CLAIM`, `HANDOFF`, `VERIFIED`, `NOT VERIFIED`, `NEXT`,
  `HEARTBEAT`, `RECLAIMED`) verified to stay English in both language variants.
- This report is committed on branch
  `agent/bench-workbuddy/10-bilingual-doc-review`; the reviewed
  README/WORKFLOW files were not modified.
