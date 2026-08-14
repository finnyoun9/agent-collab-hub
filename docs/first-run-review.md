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
| `python scripts/collab.py doctor` | `GitHub API write credential: not set` (direct API token absent in that process; `gh` auth is separate) |
| `python scripts/collab.py route --needs local,research --prefer low-cost` | bench-workbuddy, mac-claude-vscode, bench-codex |
| `python -m unittest discover tests -v` | 10 tests, all passed |
| `gh issue create ... --label state:triage` | issue #1 created |
| `python scripts/collab.py claim 1 --agent bench-workbuddy ...` | CLAIM comment posted on issue #1 |
| `git fetch origin && git switch -c agent/bench-workbuddy/1-first-run-review` | branch created from origin/main |

## 3. Findings from inside the loop

These are observations from the perspective of the agent that the hub routes
bounded local work to. None of them blocks the loop; all of them cost time or
risk the next run.

### 3.1 `doctor` does not explain the difference between its API token and `gh` auth

`command_doctor` only checks `GH_TOKEN` / `GITHUB_TOKEN` environment variables.
This run authenticated with `gh auth` (the keyring) and the write command
(`collab.py claim`) worked fine, yet `doctor` printed:

```text
GitHub API write credential: not set
```

This is not a false negative for `collab.py`: its `GitHubClient` sends requests
with Python's `urllib` and requires `GH_TOKEN` or `GITHUB_TOKEN` for writes. A
credential stored by `gh auth login` can make `gh` commands work, but it is not
automatically available to that Python client. The successful CLAIM therefore
does not prove that `collab.py` read the `gh` keyring; the token may have been
provided for that invocation, or the comment may have been posted through a
different path.

Suggested fix: rename the diagnostic to `collab.py write token
(GH_TOKEN/GITHUB_TOKEN)` and, if useful, report `gh auth status` separately.
Do not merge the two authentication paths into one result.

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

1. **Clarify `doctor` auth scope** (3.1) — distinguish the direct API token
   used by `collab.py` from the separate `gh` CLI credential.
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
- Wrong assumption corrected by evidence: a working `gh` command does not
  prove that `git` or `collab.py` shares its authentication or proxy path;
  each path must be diagnosed separately.

## 7. Incident log (important)

The local Git metadata was deleted and rebuilt repeatedly during the first run
and the follow-up task. The command audit records explicit `rm -rf .git`
invocations, including commands proposed after branch or checkout failures.
There is no evidence that `git switch` or `git checkout` deleted `.git` by
itself, so the incident must not be documented as a Git or filesystem bug.

- **Root cause supported by evidence**: destructive recovery commands were run
  inside a checkout shared by multiple agents. Reinitializing the repository
  and manually writing refs then produced additional invalid or confusing Git
  states.
- **Safe recovery**: stop mutating the affected directory, preserve it for
  diagnosis, and clone the remote repository into a new directory. Verify the
  new clone with `git status`, `git rev-parse HEAD`, and `git fsck` before
  copying any uncommitted artifact deliberately.
- **Lesson**: never delete or recreate `.git` in place, run `git init` as a
  repair inside an existing checkout, or manually write `.git/refs`. Give each
  concurrently running agent its own clone; give long-running services a
  separate runtime clone that agents do not edit.
- **Improvement**: document isolated clones and fresh-clone recovery as the
  supported procedure. Keep GitHub as the durable exchange point, but do not
  assume every uncommitted local artifact is recoverable from the remote.
