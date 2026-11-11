import re
import unittest
from pathlib import Path

SKILL = Path(__file__).parents[1] / "SKILL.md"

class NAKSkillSafetyTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")

    def test_runnable_examples_contain_no_secret_bearing_options(self):
        forbidden = ("--sec", "--prompt-sec", "NOSTR_SECRET_KEY", "bunker://")
        fenced_blocks = re.findall(r"(?ms)^~~~[^\\n]*\\n(.*?)^~~~\\s*$", self.text)
        runnable = "\\n".join(fenced_blocks)
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, runnable)

    def test_agent_skill_never_invokes_nak_event(self):
        # v0.22.3 initializes its default signer before checking --no-sign.
        fenced_blocks = re.findall(r"(?ms)^~~~[^\\n]*\\n(.*?)^~~~\\s*$", self.text)
        runnable_lines = [line.strip() for block in fenced_blocks for line in block.splitlines()]
        commands = [line for line in runnable_lines if line.startswith("nak event")]
        self.assertEqual(commands, [])
        self.assertIn("even with `--no-sign`", self.text)
        self.assertIn("machine-specific key", self.text)

    def test_no_agent_key_generation_or_default_key_commands(self):
        for phrase in ("nak key generate", "nak key default", "nak key decrypt"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.text)

if __name__ == "__main__":
    unittest.main()
