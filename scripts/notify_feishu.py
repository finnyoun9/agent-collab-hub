#!/usr/bin/env python3
"""Send a compact GitHub issue event to a Feishu custom-bot webhook."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any


def build_card(event: dict[str, Any], event_name: str) -> dict[str, Any]:
    issue = event.get("issue", {})
    comment = event.get("comment", {})
    title = issue.get("title", "Agent collaboration update")
    number = issue.get("number", "?")
    url = comment.get("html_url") or issue.get("html_url") or "https://github.com"
    action = event.get("action", "updated")
    body = comment.get("body", "")
    preview = body.strip().replace("\n", " ")[:300]
    lines = [f"**Event:** {event_name}/{action}", f"**Task:** #{number} {title}"]
    if preview:
        lines.append(f"**Update:** {preview}")
    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "Agent Collab Hub"},
                "template": "blue",
            },
            "elements": [
                {"tag": "markdown", "content": "\n".join(lines)},
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "Open GitHub"},
                            "url": url,
                            "type": "primary",
                        }
                    ],
                },
            ],
        },
    }


def main() -> int:
    webhook = os.environ.get("FEISHU_WEBHOOK_URL")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not webhook or not event_path:
        raise SystemExit("FEISHU_WEBHOOK_URL and GITHUB_EVENT_PATH are required")
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    payload = build_card(event, os.environ.get("GITHUB_EVENT_NAME", "github"))
    request = urllib.request.Request(
        webhook,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        response.read()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
