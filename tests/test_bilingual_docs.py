from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BilingualDocumentationTests(unittest.TestCase):
    def test_core_documents_have_chinese_variants(self) -> None:
        pairs = [
            ("README.md", "README.zh-CN.md"),
            ("docs/WORKFLOW.md", "docs/WORKFLOW.zh-CN.md"),
            ("docs/FEISHU.md", "docs/FEISHU.zh-CN.md"),
        ]
        for english, chinese in pairs:
            with self.subTest(english=english):
                self.assertTrue((ROOT / english).is_file())
                self.assertTrue((ROOT / chinese).is_file())
                self.assertIn(chinese.split("/")[-1], (ROOT / english).read_text("utf-8"))
                self.assertIn(english.split("/")[-1], (ROOT / chinese).read_text("utf-8"))

    def test_issue_form_contains_both_languages(self) -> None:
        issue_form = (ROOT / ".github/ISSUE_TEMPLATE/agent-task.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("Goal / 目标", issue_form)
        self.assertIn("Acceptance criteria / 验收标准", issue_form)


if __name__ == "__main__":
    unittest.main()
