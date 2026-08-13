# Agent Collab Hub

English | [简体中文](README.zh-CN.md)

A lightweight control plane for coordinating heterogeneous coding agents across
multiple computers. It uses GitHub Issues as the task queue, branches and pull
requests as delivery boundaries, and Feishu as the human-facing notification
and command entry point.

Hermes can act as an always-on dispatcher and invoke native CLIs such as
OpenCode and Pi. Each agent keeps its own tools, sessions, and subagents; the
hub chooses a primary worker and records a concise outcome.

## Why this shape

Cross-device agents cannot safely share a checkout or chat history. They can,
however, share durable state through GitHub. The minimum reliable protocol is:

```text
Feishu / human request
        |
        v
GitHub Issue (task + acceptance criteria)
        |
        v
Hermes/router -> one primary worker -> clean checkout or task worktree
        |
        v
result -> optional gap check -> integration
        |
        v
Feishu notification + durable decision/learning note
```

## Quick start

```bash
python scripts/collab.py agents
python scripts/collab.py route --needs local,code --prefer low-cost
python scripts/collab.py doctor
```

Use Chinese output with `--lang zh` or `COLLAB_LANG=zh`:

```bash
python scripts/collab.py --lang zh route --needs vision,research --prefer vision
```

All text files and CLI output use UTF-8 across Windows, macOS, and Linux.

See [coordinator/README.zh-CN.md](coordinator/README.zh-CN.md) for the current
bench-hosted Feishu coordinator MVP.

To read or update GitHub Issues, provide credentials only through the process
environment. Never commit them:

```bash
export GH_TOKEN="..."
python scripts/collab.py status --repo finnyoun9/agent-collab-hub
```

On PowerShell:

```powershell
$env:GH_TOKEN = "..."
python scripts/collab.py status --repo finnyoun9/agent-collab-hub
```

Create tasks through the GitHub `Agent task` issue form. See
[docs/WORKFLOW.md](docs/WORKFLOW.md) for the operating protocol and
[docs/FEISHU.md](docs/FEISHU.md) for the Feishu bridge.

## Included agent profile

The configuration models a mixed local and remote fleet. The core local roles are:

| Agent | Best use | Main constraint |
|---|---|---|
| bench Hermes | always-on dispatch, memory, scheduling, Feishu | delegates coding |
| bench OpenCode | default local coding and fast edits | permissions must be configured |
| bench Codex | complex integration, recovery, hardware verification | premium capacity |
| bench Pi | extensions and RPC experiments | intentionally minimal defaults |
| bench WorkBuddy | interactive fallback implementation | no image input |
| Mac Claude client | visual analysis, research, architecture review | may lack local workspace access |
| Mac Claude VS Code | local coding and review | no image input with current API |

Edit [config/agents.json](config/agents.json) as capabilities change.

## Design principles

- One task has one owner and one branch.
- Low-risk local implementation defaults to `bench-opencode`.
- Sequential workers may reuse a clean checkout. Concurrent writers use
  separate task worktrees or clones.
- Runtime services use a dedicated clone that coding agents do not edit.
- Agents communicate through artifacts, not assumed shared chat memory.
- A claim is a lease, not permanent ownership.
- Independent review is risk-based, not mandatory for routine work.
- Hardware claims require measurement evidence from a hardware-capable agent.
- Research is only complete when converted into code, a test, a decision, or a
  reproducible experiment.
- Secrets stay in environment variables or GitHub/Feishu secret stores.

## Related projects

See [docs/REFERENCES.md](docs/REFERENCES.md) for projects and patterns that
informed this implementation.

See [docs/LOCAL-AGENTS.md](docs/LOCAL-AGENTS.md) for CLI adapters, routing, and
the recommended Hermes-to-worker execution model.
