from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import install  # noqa: E402


class AnswerStyleSkillTests(unittest.TestCase):
    def test_skill_frontmatter_and_encoding(self) -> None:
        skill_text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("\ufffd", skill_text)
        self.assertNotIn("博宸", skill_text)
        match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", skill_text, flags=re.DOTALL)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertIn("name: bochen-answer-style", match.group(1))
        self.assertIn("description:", match.group(1))
        self.assertLessEqual(len(skill_text.splitlines()), 200)

    def test_openai_yaml_and_rule_file(self) -> None:
        yaml_text = (REPO_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "博晨回答风格"', yaml_text)
        self.assertIn("$bochen-answer-style", yaml_text)

        rule_text = (REPO_ROOT / "rules" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("结论前置", rule_text)
        self.assertIn("低 AI 腔", rule_text)

    def test_eval_suite_structure(self) -> None:
        payload = json.loads(
            (REPO_ROOT / "evals" / "bochen-answer-style.json").read_text(encoding="utf-8")
        )
        self.assertEqual(payload["skill_name"], "bochen-answer-style")
        cases = payload["evals"]
        self.assertGreaterEqual(len(cases), 6)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))

    def test_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"\]\((?!https?://|mailto:|#)([^)]+)\)")
        for md_file in REPO_ROOT.rglob("*.md"):
            if ".git" in md_file.parts:
                continue
            text = md_file.read_text(encoding="utf-8")
            for target in link_pattern.findall(text):
                clean = target.split("#", 1)[0].strip()
                if clean:
                    self.assertTrue(
                        (md_file.parent / clean).resolve().exists(),
                        f"Broken link '{target}' in {md_file.relative_to(REPO_ROOT)}",
                    )

    def test_installer_skill_and_idempotent_rule_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            skill_dest = install.install_skill(tmp_path / "skills")
            self.assertTrue((skill_dest / "SKILL.md").is_file())
            self.assertTrue((skill_dest / "agents" / "openai.yaml").is_file())
            self.assertTrue((skill_dest / "examples" / "before-after.md").is_file())

            rule_file = tmp_path / "GEMINI.md"
            rule_file.write_text("# Existing Rule\nKeep code clean.\n", encoding="utf-8")
            install.install_rule(rule_file)
            install.install_rule(rule_file)  # idempotent second run
            merged = rule_file.read_text(encoding="utf-8")
            self.assertEqual(merged.count(install.RULE_MARKER), 1)
            self.assertIn("# Existing Rule", merged)


if __name__ == "__main__":
    unittest.main()
