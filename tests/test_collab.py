from __future__ import annotations

import argparse
import importlib.util
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "collab.py"
SPEC = importlib.util.spec_from_file_location("collab", SCRIPT)
assert SPEC and SPEC.loader
collab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collab)


class RoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = collab.load_config()

    def test_visual_research_prefers_visual_agent(self) -> None:
        matches = collab.route_agents(
            self.config, {"vision", "research"}, prefer="vision"
        )
        self.assertEqual(matches[0]["id"], "mac-claude-client")

    def test_local_low_cost_excludes_online_visual_specialist(self) -> None:
        matches = collab.route_agents(
            self.config, {"code", "local"}, prefer="low-cost"
        )
        ids = [agent["id"] for agent in matches]
        self.assertIn("bench-workbuddy", ids[:2])
        self.assertIn("mac-claude-vscode", ids[:2])
        self.assertNotIn("mac-claude-client", ids)

    def test_hardware_routes_only_to_capable_agent(self) -> None:
        matches = collab.route_agents(self.config, {"hardware"})
        self.assertEqual([agent["id"] for agent in matches], ["bench-codex"])

    def test_chinese_route_output(self) -> None:
        args = argparse.Namespace(needs="vision,research", prefer="vision", lang="zh")
        output = io.StringIO()
        with redirect_stdout(output):
            result = collab.command_route(args)
        self.assertEqual(result, 0)
        self.assertIn("适合截图、数据手册", output.getvalue())


class MessageTests(unittest.TestCase):
    def test_claim_has_parseable_headings(self) -> None:
        body = collab.claim_body(
            "agent-a", "owner/repo", "agent/a/1-task", "src/a.py", "tomorrow"
        )
        self.assertTrue(body.startswith("CLAIM\n"))
        self.assertIn("Agent: agent-a", body)
        self.assertIn("Branch: agent/a/1-task", body)

    def test_handoff_has_required_sections(self) -> None:
        args = argparse.Namespace(
            agent="agent-a",
            branch="agent/a/1-task",
            commit="abc1234",
            pr="https://example.test/pr/1",
            changed="src/a.py",
            verified="tests passed",
            not_verified="hardware",
            next="run hardware test",
        )
        body = collab.handoff_body(args)
        for heading in ("HANDOFF", "VERIFIED", "NOT VERIFIED", "NEXT"):
            self.assertIn(heading, body)


if __name__ == "__main__":
    unittest.main()
