# Local agent integration

The bench uses one lightweight dispatch layer over native agent CLIs. Agents
keep their own prompts, tools, sessions, and subagents; the hub only chooses a
primary worker and records the outcome.

## Roles

| Agent | Role |
|---|---|
| `bench-hermes` | always-on intake, Feishu, scheduling, memory, and dispatch |
| `bench-opencode` | default local coding worker |
| `bench-codex` | complex implementation, integration, recovery, and risk review |
| `bench-pi` | experimental extensions and RPC workflows |
| `bench-workbuddy` | interactive fallback worker |
| Claude clients | vision, architecture, and long-context specialist work |

All may use DeepSeek V4. The harness still matters: each client supplies
different tools, context management, permissions, UI, and subagent behavior.

## CLI adapters

```powershell
hermes -z "<task>"
opencode run --auto "<task>"
pi -p "<task>"
```

Use configured provider/model names rather than placing API keys in commands or
repository files. Hermes may spawn these commands and collect stdout, exit code,
and Git diff. The hub must never recursively dispatch a worker's subagent: the
selected primary worker owns all child work and returns one result.

## Routing

- Automation, scheduled work, memory, or messaging: Hermes.
- Ordinary local coding: OpenCode.
- Complex integration, repeated failure, hardware, or high risk: Codex.
- Custom harness/RPC experiments: Pi.
- Vision or long-context architecture: Claude client.

Fast mode is the default. A second agent performs a quick gap check only for
ambiguous or cross-module tasks. Controlled mode is reserved for high-risk work.

## Workspace policy

Do not maintain a permanent clone per agent. Keep one runtime clone for the
coordinator and create task worktrees only when agents write concurrently.
Sequential workers may reuse a clean checkout. Archive obsolete recovery and
review directories after confirming they contain no unique uncommitted work.
