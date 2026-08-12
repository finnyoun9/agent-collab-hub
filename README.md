# Agent Collab Hub

A lightweight control plane for coordinating heterogeneous coding agents across
multiple computers. It uses GitHub Issues as the task queue, branches and pull
requests as delivery boundaries, and Feishu as the human-facing notification
and command entry point.

This repository does not run or proxy models. Codex, Claude Code, WorkBuddy,
and API-backed agents keep using their native clients. The hub only standardizes
task routing, claims, handoffs, evidence, and review.

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
Router -> one owner -> isolated branch/worktree
        |
        v
PR + test evidence -> independent review -> integration
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

The example configuration models a practical four-agent fleet:

| Agent | Best use | Main constraint |
|---|---|---|
| bench Codex | coordinator, integration, hardware verification | premium capacity |
| bench WorkBuddy | local coding, repetitive work, quick checks | no image input |
| Mac Claude client | visual analysis, research, architecture review | may lack local workspace access |
| Mac Claude VS Code | local coding and review | no image input with current API |

Edit [config/agents.json](config/agents.json) as capabilities change.

## Design principles

- One task has one owner and one branch.
- Agents communicate through artifacts, not assumed shared chat memory.
- A claim is a lease, not permanent ownership.
- The author does not perform the final review for risky changes.
- Hardware claims require measurement evidence from a hardware-capable agent.
- Research is only complete when converted into code, a test, a decision, or a
  reproducible experiment.
- Secrets stay in environment variables or GitHub/Feishu secret stores.

## Related projects

See [docs/REFERENCES.md](docs/REFERENCES.md) for projects and patterns that
informed this implementation.
