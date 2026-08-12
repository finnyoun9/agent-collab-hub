# Workflow

English | [简体中文](WORKFLOW.zh-CN.md)

## Control surfaces

| Surface | Canonical content |
|---|---|
| GitHub Issue | goal, scope, owner, dependencies, acceptance criteria |
| Branch/worktree | one agent's code changes |
| Pull request | review discussion and merge gate |
| Feishu | notification, quick commands, human decisions |
| Project docs | stable architecture and verified knowledge |
| Decision log ([DECISIONS.md](../DECISIONS.md)) | settled conclusions, not re-litigated |

Feishu chat is not canonical project state. Important decisions made there must
be copied to the issue, PR, or project documentation.

## Task states

```text
triage -> ready -> claimed -> in-progress -> review -> verify -> done
                         \-> blocked -----/
```

Suggested labels:

- `state:triage`, `state:ready`, `state:claimed`, `state:review`,
  `state:verify`, `state:blocked`, `state:done`
- `agent:bench-codex`, `agent:bench-workbuddy`, `agent:mac-claude-client`,
  `agent:mac-claude-vscode`
- `need:vision`, `need:local`, `need:hardware`, `need:research`, `need:review`
- `risk:low`, `risk:medium`, `risk:high`

## Routing rules

1. Vision input routes to `mac-claude-client` unless local/hardware access is
   also required. It returns observations as an issue comment or artifact.
2. Bounded local coding routes first to a low-cost local worker.
3. Hardware flashing and measurement route to `bench-codex`.
4. Architecture and ambiguous research route to `mac-claude-client`; the
   coordinator converts conclusions into an executable task.
5. High-risk or cross-module work returns to `bench-codex` for integration.
6. Review should use a different model/client from the author when possible.

## Claim

Before editing, post:

```text
CLAIM
Agent: mac-claude-vscode
Target: owner/project
Branch: agent/mac-claude-vscode/42-short-name
Files: src/foo.c, tests/test_foo.py
Lease until: 2026-08-13T20:00:00+08:00
```

Then create the branch from current `origin/main`:

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c agent/mac-claude-vscode/42-short-name
```

## Heartbeat and lease

Long tasks post a short heartbeat before the lease expires:

```text
HEARTBEAT
Agent: mac-claude-vscode
Progress: parser implemented; tests in progress
Lease until: 2026-08-14T04:00:00+08:00
```

Do not use minute-by-minute heartbeats. One update at a meaningful checkpoint is
enough. An expired task can be reassigned by the coordinator after a visible
`RECLAIMED` comment.

## Handoff

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
- target hardware timing

NEXT
- bench-codex: run the hardware acceptance test and record evidence
```

## Learning tasks

Learning work uses the same delivery discipline. A task such as “learn DMA” is
too vague; route it as:

```text
Goal: explain and implement UART RX circular DMA on the current board.
Artifact: minimal firmware + wiring note + captured UART evidence.
Acceptance: no byte loss in a reproducible burst test.
Reflection: record one wrong assumption and how the evidence corrected it.
```

The output must be reusable: code, test, experiment log, diagram, or decision
record. A chat summary alone is not complete.
