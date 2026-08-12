# Feishu bridge

English | [简体中文](FEISHU.zh-CN.md)

Feishu should be the front door and notification channel, while GitHub remains
the source of truth.

## MVP data flow

```text
Feishu command/card
    -> existing bot or metabot
    -> GitHub Issue API
    -> agent claims and works in its native client
    -> handoff/PR event
    -> GitHub Action or bot
    -> Feishu card notification
```

This avoids forcing Codex, Claude Code, and DeepSeek-backed clients into one
runtime. Each agent only needs GitHub access and this repository's protocol.

## Suggested Feishu commands

```text
/task <goal>                 create a triage issue
/queue                       list ready, claimed, and blocked tasks
/assign <issue> <agent-id>   set owner and capability label
/handoff <issue>             show the latest handoff
/decision <issue> <text>     record a human decision in GitHub
```

## Task creation contract

The Feishu bot should create an Issue body containing:

```json
{
  "goal": "string",
  "target_repo": "owner/repository",
  "required_capabilities": ["code", "local"],
  "allowed_scope": ["src/ota/**", "tests/**"],
  "acceptance": ["tests pass", "CRC error is rejected"],
  "learning_goal": "optional string",
  "risk": "low|medium|high"
}
```

The bot must not insert Feishu app secrets, user tokens, private chat history,
or full local paths into the issue.

## Outbound webhook

`scripts/notify_feishu.py` converts a GitHub event into a small interactive
card. Configure a Feishu custom-bot webhook as the GitHub Actions secret
`FEISHU_WEBHOOK_URL`. The script reads the secret only from the environment.

For a production Feishu app, replace the custom webhook transport with app
authentication inside the existing bot. Keep the event payload and GitHub state
model unchanged.

## Recommended automation boundary

Automate:

- new task notification;
- task claimed/blocked/handoff notification;
- review requested and CI failed notification;
- stale lease reminder.

Keep human approval for:

- high-risk scope changes;
- merging to protected branches;
- publishing releases;
- flashing hardware or destructive device actions.
