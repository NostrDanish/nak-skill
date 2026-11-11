import re
import unittest
from pathlib import Path

SKILL = Path(__file__).parents[1] / "SKILL.md"

class NAKSkillSafetyTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")

    def test_agent_skill_contains_no_secret_bearing_signing_options(self):
        forbidden = ("--sec", "--prompt-sec", "NOSTR_SECRET_KEY", "bunker://")
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, self.text)

    def test_event_examples_never_fall_back_to_machine_default_key(self):
        code_spans = re.findall(r"`([^`]+)`", self.text)
        fenced_blocks = re.findall(r"(?ms)^~~~[^\n]*\n(.*?)^~~~\s*$", self.text)
        fenced_commands = [
            line.strip() for block in fenced_blocks for line in block.splitlines()
            if "nak event" in line
        ]
        commands = [snippet for snippet in code_spans if "nak event" in snippet] + fenced_commands
        self.assertTrue(commands, "expected explicit safe event workflow examples")
        for command in commands:
            safe = (
                command.startswith("nak event --help")
                or command.startswith("nak event --no-sign --author")
                or "cat signed-event.json | nak event " in command
            )
            with self.subTest(command=command):
                self.assertTrue(safe, "NAK event example must be unsigned draft, help, or pre-signed input")

    def test_no_agent_key_generation_or_default_key_commands(self):
        for phrase in ("nak key generate", "nak key default", "nak key decrypt"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.text)

if __name__ == "__main__":
    unittest.main()
