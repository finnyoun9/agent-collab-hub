#!/usr/bin/env python3
"""Small, dependency-free CLI for the Agent Collab Hub."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO = "finnyoun9/agent-collab-hub"


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or ROOT / "config" / "agents.json"
    return json.loads(config_path.read_text(encoding="utf-8"))


def split_capabilities(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def route_agents(
    config: dict[str, Any], needs: set[str], prefer: str | None = None
) -> list[dict[str, Any]]:
    ranked: list[tuple[int, str, dict[str, Any]]] = []
    for agent in config["agents"]:
        capabilities = set(agent["capabilities"])
        if not needs.issubset(capabilities):
            continue
        score = len(needs) * 10
        if prefer == "low-cost" and (
            agent["cost"] == "low" or "low-cost" in capabilities
        ):
            score += 5
        if prefer == "vision" and "vision" in capabilities:
            score += 5
            if agent["role"] == "specialist":
                score += 2
        if prefer == "coordinator" and agent["role"] == "coordinator":
            score += 5
        ranked.append((score, agent["id"], agent))
    return [item[2] for item in sorted(ranked, key=lambda item: (-item[0], item[1]))]


class GitHubClient:
    def __init__(self, token: str | None = None) -> None:
        self.token = token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")

    def request(
        self, method: str, path: str, payload: dict[str, Any] | None = None
    ) -> Any:
        url = f"https://api.github.com{path}"
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "agent-collab-hub",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc
        return json.loads(body) if body else None

    def list_tasks(self, repo: str, state: str) -> list[dict[str, Any]]:
        query = urllib.parse.urlencode({"state": state, "per_page": 100})
        issues = self.request("GET", f"/repos/{repo}/issues?{query}")
        return [issue for issue in issues if "pull_request" not in issue]

    def comment(self, repo: str, issue: int, body: str) -> None:
        if not self.token:
            raise RuntimeError("GH_TOKEN or GITHUB_TOKEN is required for writes")
        self.request(
            "POST", f"/repos/{repo}/issues/{issue}/comments", {"body": body}
        )


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=Path.cwd(), text=True, capture_output=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else f"ERROR: {result.stderr.strip()}"


def claim_body(agent: str, target: str, branch: str, files: str, lease: str) -> str:
    return "\n".join(
        [
            "CLAIM",
            f"Agent: {agent}",
            f"Target: {target}",
            f"Branch: {branch}",
            f"Files: {files}",
            f"Lease until: {lease}",
        ]
    )


def handoff_body(args: argparse.Namespace) -> str:
    return "\n".join(
        [
            "HANDOFF",
            f"Agent: {args.agent}",
            f"Branch: {args.branch}",
            f"Commit: {args.commit}",
            f"PR: {args.pr}",
            f"Changed: {args.changed}",
            "",
            "VERIFIED",
            args.verified,
            "",
            "NOT VERIFIED",
            args.not_verified,
            "",
            "NEXT",
            args.next,
        ]
    )


def command_agents(_: argparse.Namespace) -> int:
    for agent in load_config()["agents"]:
        caps = ", ".join(agent["capabilities"])
        print(f"{agent['id']}: {agent['role']} [{caps}]")
    return 0


def command_route(args: argparse.Namespace) -> int:
    matches = route_agents(load_config(), split_capabilities(args.needs), args.prefer)
    if not matches:
        print("No agent satisfies every required capability.", file=sys.stderr)
        return 1
    for index, agent in enumerate(matches, start=1):
        print(f"{index}. {agent['id']} - {agent['notes']}")
    return 0


def command_doctor(_: argparse.Namespace) -> int:
    token_present = bool(os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN"))
    print(f"repository: {git_output('rev-parse', '--show-toplevel')}")
    print(f"branch: {git_output('branch', '--show-current')}")
    print(f"remote: {git_output('remote', 'get-url', 'origin')}")
    print(f"working tree: {git_output('status', '--short') or 'clean'}")
    print(f"GitHub API write credential: {'available' if token_present else 'not set'}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    tasks = GitHubClient().list_tasks(args.repo, args.state)
    for issue in tasks:
        labels = ",".join(label["name"] for label in issue.get("labels", []))
        print(f"#{issue['number']} [{labels}] {issue['title']} {issue['html_url']}")
    return 0


def command_claim(args: argparse.Namespace) -> int:
    body = claim_body(args.agent, args.target, args.branch, args.files, args.lease)
    GitHubClient().comment(args.repo, args.issue, body)
    print(body)
    return 0


def command_handoff(args: argparse.Namespace) -> int:
    body = handoff_body(args)
    GitHubClient().comment(args.repo, args.issue, body)
    print(body)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    agents = subparsers.add_parser("agents", help="list configured agents")
    agents.set_defaults(func=command_agents)

    route = subparsers.add_parser("route", help="rank agents by capability")
    route.add_argument("--needs", required=True, help="comma-separated capabilities")
    route.add_argument(
        "--prefer", choices=["low-cost", "vision", "coordinator"], default=None
    )
    route.set_defaults(func=command_route)

    doctor = subparsers.add_parser("doctor", help="inspect local collaboration setup")
    doctor.set_defaults(func=command_doctor)

    status = subparsers.add_parser("status", help="list hub tasks")
    status.add_argument("--repo", default=DEFAULT_REPO)
    status.add_argument("--state", choices=["open", "closed", "all"], default="open")
    status.set_defaults(func=command_status)

    claim = subparsers.add_parser("claim", help="post a structured claim")
    claim.add_argument("issue", type=int)
    claim.add_argument("--repo", default=DEFAULT_REPO)
    claim.add_argument("--agent", required=True)
    claim.add_argument("--target", required=True)
    claim.add_argument("--branch", required=True)
    claim.add_argument("--files", required=True)
    claim.add_argument("--lease", required=True, help="ISO 8601 timestamp")
    claim.set_defaults(func=command_claim)

    handoff = subparsers.add_parser("handoff", help="post a structured handoff")
    handoff.add_argument("issue", type=int)
    handoff.add_argument("--repo", default=DEFAULT_REPO)
    handoff.add_argument("--agent", required=True)
    handoff.add_argument("--branch", required=True)
    handoff.add_argument("--commit", required=True)
    handoff.add_argument("--pr", required=True)
    handoff.add_argument("--changed", required=True)
    handoff.add_argument("--verified", required=True)
    handoff.add_argument("--not-verified", required=True)
    handoff.add_argument("--next", required=True)
    handoff.set_defaults(func=command_handoff)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.func(args))
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
