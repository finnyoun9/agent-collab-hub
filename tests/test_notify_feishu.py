from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "notify_feishu.py"
SPEC = importlib.util.spec_from_file_location("notify_feishu", SCRIPT)
assert SPEC and SPEC.loader
notify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(notify)


class CardTests(unittest.TestCase):
    def test_issue_comment_card_links_to_comment(self) -> None:
        card = notify.build_card(
            {
                "action": "created",
                "issue": {
                    "number": 3,
                    "title": "Run hardware test",
                    "html_url": "https://example.test/issues/3",
                },
                "comment": {
                    "body": "HANDOFF\nTests passed",
                    "html_url": "https://example.test/issues/3#comment-1",
                },
            },
            "issue_comment",
        )
        action = card["card"]["elements"][1]["actions"][0]
        self.assertEqual(action["url"], "https://example.test/issues/3#comment-1")
        markdown = card["card"]["elements"][0]["content"]
        self.assertIn("#3 Run hardware test", markdown)
        self.assertIn("HANDOFF Tests passed", markdown)


if __name__ == "__main__":
    unittest.main()
