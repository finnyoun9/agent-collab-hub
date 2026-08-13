# Collaboration workflow

English | [简体中文](WORKFLOW.zh-CN.md)

## Core rules

- Hermes is the always-on dispatcher; OpenCode is the default local coding worker.
- Codex handles complex integration, recovery, hardware, and high-risk work.
- Pi is for extension, RPC, and context-efficient experiments; WorkBuddy is an
  interactive fallback.
- Select one primary worker per task. Its internal subagents must not redispatch
  through the hub.
- Agents hand work off through results, Git diffs, commits, or issue comments;
  they do not assume shared chat memory.

## Fast mode

Use fast mode for routine low-risk local work:

```text
task -> primary worker -> change/result -> optional gap check -> done
```

Fast mode does not require a dedicated clone, PR, lease, full test suite, or
independent review. The worker reports what changed, any command failure, and
known gaps.

## Controlled mode

Use controlled mode for deployment, credentials, hardware flashing,
destructive actions, high-risk changes, or overlapping concurrent work:

- create a task branch or worktree;
- state the allowed scope;
- verify in proportion to risk;
- use a different agent for review when warranted;
- retain human approval for merge, release, and destructive operations.

Sequential workers may reuse a clean checkout. Two concurrent writers require
separate worktrees or clones. The coordinator runtime clone is not a development
workspace.

## Routing

1. Automation, scheduling, memory, and messaging: `bench-hermes`.
2. Ordinary local coding: `bench-opencode`.
3. Complex integration, repeated failure, hardware, or high risk: `bench-codex`.
4. Custom harness, extension, or RPC work: `bench-pi`.
5. Vision, architecture, and long-context work: Claude clients.
6. IDE interaction or OpenCode fallback: `bench-workbuddy`.

`config/agents.json` is the single source of truth for agent IDs and routing.
