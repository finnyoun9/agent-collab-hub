# First-run review: bench-workbuddy walks the full loop

English | [简体中文](first-run-review.zh-CN.md)

- **Run date**: 2026-08-13
- **Acting agent**: `bench-workbuddy`
- **Task**: [agent-collab-hub#1](https://github.com/finnyoun9/agent-collab-hub/issues/1)
- **Branch**: `agent/bench-workbuddy/1-first-run-review`
- **Related decision**: [D-001](https://github.com/finnyoun9/agent-collab-hub/blob/main/DECISIONS.md)

## 1. What was exercised

This run is the first complete pass over the coordination loop defined in
[docs/WORKFLOW.md](WORKFLOW.md):

```text
task issue -> CLAIM -> isolated branch -> evidence artifact -> PR -> HANDOFF
```

Every step was executed through the native `gh` CLI and the bundled
`scripts/collab.py`, with credentials injected only through the process
environment. The run produced this review document, its Chinese variant, one
pull request, and one structured handoff comment.

## 2. Evidence baseline

| Check | Result |
|---|---|
| `python scripts/collab.py agents` | 4 agents listed, matches `config/agents.json` |
| `python scripts/collab.py doctor` | repo/branch/remote/clean reported correctly |
| `python scripts/collab.py doctor` | `GitHub API write credential: not set` (false negative) |
| `python scripts/collab.py route --needs local,research --prefer low-cost` | bench-workbuddy, mac-claude-vscode, bench-codex |
| `python -m unittest discover tests -v` | 10 tests, all passed |
| `gh issue create ... --label state:triage` | issue #1 created |
| `python scripts/collab.py claim 1 --agent bench-workbuddy ...` | CLAIM comment posted on issue #1 |
| `git fetch origin && git switch -c agent/bench-workbuddy/1-first-run-review` | branch created from origin/main |

## 3. Findings from inside the loop

These are observations from the perspective of the agent that the hub routes
bounded local work to. None of them blocks the loop; all of them cost time or
risk the next run.

### 3.1 `doctor` misreports a working GitHub credential

`command_doctor` only checks `GH_TOKEN` / `GITHUB_TOKEN` environment variables.
This run authenticated with `gh auth` (the keyring) and the write command
(`collab.py claim`) worked fine, yet `doctor` printed:

```text
GitHub API write credential: not set
```

Suggested fix: also probe `gh auth status` / `gh api user` when the token
environment variables are absent, and print the effective auth source.

### 3.2 No declared Python dependency for the test suite

`tests/` is written in `unittest` style and runs with zero extra dependencies
(`python -m unittest discover tests -v`), which is good. But there is no
declared dependency metadata at all: no `requirements.txt`, no
`pyproject.toml`, no `setup.cfg`. `pytest` is not required, and that is fine;
what is missing is a single line that says how to run the tests. Suggest a
`pyproject.toml` with a `[project]` table and a `[tool.pytest]` hint, or at
minimum a note in the README.

### 3.3 Tool docs assume a `route` run but the first real need is `status`

The quick start shows `route`, `agents`, and `doctor`. In practice the first
question an agent or human asks is "what is open right now?", which is
`collab.py status`. Suggest moving `status` into the quick start and
documenting the expected label vocabulary (`state:*`, `agent:*`, `need:*`,
`risk:*`) next to it.

### 3.4 The issue template does not capture `need:*` capabilities

The template form has a single "Primary capability" dropdown and free-text
scope, but the routing protocol (`route --needs ...`) consumes capability
keywords (`need:vision`, `need:local`, ...). A task created through the form
therefore needs manual label normalization before it can be routed reliably.
Suggest a multi-select of `need:*` labels in the form and a note that
`state:triage` is the entry state.

### 3.5 CLAIM lease expiry is unverified on the tool side

`collab.py claim` writes the lease timestamp but nothing validates that the
lease is in the future, nor does `status` surface expiry. A stale lease is
supposed to be reclaimable after expiry (AGENTS.md), but no tool output helps a
coordinator see that an issue's lease has lapsed. Suggest surfacing `lease
until` in `status` output and warning when it is in the past.

### 3.6 Branch naming is underspecified for cross-device workers

`agent/<agent-id>/<issue>-<short-name>` works, but nothing prevents two agents
on different machines from colliding on the same branch name for the same
issue. The protocol already says "one owner per issue", so this is a soft risk,
but a small guard would help: document that branch creation must be
`git fetch origin && git switch -c <branch> origin/main` (the workflow doc says
this) and add an optional `git ls-remote --exit-code origin <branch>` check
before claiming.

### 3.7 Feishu webhook card preview is not scoped to protocol comments

`notify_feishu.py` previews the body of *every* new issue comment. During a
normal loop that includes CLAIM, HEARTBEAT, and HANDOFF comments, which is
fine; but off-protocol chatter also lands in Feishu. Suggest filtering the
preview to comments that start with a protocol keyword (`CLAIM`, `HEARTBEAT`,
`HANDOFF`, `BLOCKED`, `RECLAIMED`) and sending a generic "comment added" card
otherwise.

## 4. What worked well

- The `unittest`-style suite runs with zero dependencies on Windows, macOS,
  and Linux; CI would be a one-liner if it ever lands.
- The bilingual contract is consistently applied across README, workflow docs,
  issue template, PR template, CLI messages, and Feishu cards, and
  `tests/test_bilingual_docs.py` enforces it.
- `collab.py claim` and `collab.py handoff` produce exactly the parseable
  headings the protocol requires; copy-pasting from docs would have been
  slower and more error-prone.
- The CLAIM comment workflow forces the "one owner, one branch" discipline
  before any edit happens.

## 5. Suggestions for the next iteration

Prioritized by expected impact:

1. **Fix `doctor` auth detection** (3.1) — the first command every agent runs
   on a new machine currently lies about a working setup.
2. **Add `need:*` label multi-select to the issue form** (3.4) — routing
   quality depends on structured capabilities, not free text.
3. **Surface lease expiry in `status`** (3.5) — reclaiming a stale lease is
   currently invisible.
4. **Declare test invocation in one obvious place** (3.2) — a future agent
   should not have to read the test files to learn how to run them.
5. **Scope Feishu notifications to protocol comments** (3.7) — keeps the human
   channel high-signal.

Suggested owner: `bench-codex` (coordinator/integration), with `bench-workbuddy`
or `mac-claude-vscode` available for the bounded implementation pieces.

## 6. Learning evidence

- New technique: running the full claim-branch-PR-handoff loop of this hub
  from a low-cost worker's seat and recording findings as a durable artifact.
- Reproducible artifact: this document, issue #1, the branch, and the PR.
- Wrong assumption corrected by evidence: the environment proxy is required
  for `git` even though `gh api` succeeds without explicit configuration;
  network troubleshooting belongs in every agent's onboarding checklist.

## 7. Incident log (important)

Mid-run, the local git metadata was corrupted twice. The first incident
happened while recovering from an unborn HEAD state: a manual file-move
operation destroyed the `.git` directory contents and git stopped recognizing
the repository. The second incident recreated the same unborn-HEAD symptom
after a fresh `git init` + `fetch`, where the branch ref was not written. Both
times the recovery rebuilt the local repository from the remote.

- **Root cause**: manual working-tree moves and repeated `.git` rebuilds
  during HEAD repair; a fresh `git init` on a directory whose files are not yet
  committed can leave HEAD pointing at a ref that does not exist.
- **Recovery**: `rm -rf .git && git init -b main && git remote add origin <url>
  && git fetch origin main && git checkout -b <branch> origin/main`.
- **Lesson**: never move or delete working-tree files to fix git state; use
  `git switch -c <branch> origin/main` only. Verify `.git` integrity before any
  destructive git operation, and keep artifact files out of the way of git
  repair steps.
- **Improvement**: this incident validates D-001 — GitHub as the single source
  of truth makes a corrupted local clone fully recoverable. Suggest adding a
  "recovering a corrupted local clone" section to the WORKFLOW docs, and
  documenting that the very first branch creation on a fresh clone must happen
  before any local commit.
