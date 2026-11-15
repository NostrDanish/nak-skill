import re
import unittest
from pathlib import Path

SKILL = Path(__file__).parents[1] / "SKILL.md"
FENCED_BLOCK_PATTERN = re.compile(r"(?ms)^~~~[^\n]*\n(.*?)^~~~\s*$")


def extract_fenced_blocks(text: str) -> list[str]:
    """Return only Markdown triple-tilde fenced code blocks."""
    return FENCED_BLOCK_PATTERN.findall(text)


class NAKSkillSafetyTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")

    def test_fence_extractor_captures_runnable_examples(self):
        sample = (
            "Prose mentioning --sec is not a command.\n"
            "~~~bash\n"
            "nak req -k 1 wss://relay.example\n"
            "~~~\n"
            "More prose.\n"
            "~~~sh\n"
            "nak event --no-sign\n"
            "~~~\n"
        )
        blocks = extract_fenced_blocks(sample)
        self.assertEqual(len(blocks), 2)
        runnable = "\n".join(blocks)
        self.assertIn("nak req -k 1", runnable)
        self.assertIn("nak event --no-sign", runnable)
        self.assertNotIn("Prose mentioning --sec", runnable)

    def test_runnable_examples_contain_no_secret_bearing_options(self):
        forbidden = ("--sec", "--prompt-sec", "NOSTR_SECRET_KEY", "bunker://")
        runnable = "\n".join(extract_fenced_blocks(self.text))
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, runnable)

    def test_agent_skill_never_invokes_nak_event(self):
        # v0.22.3 initializes its default signer before checking --no-sign.
        runnable_lines = [
            line.strip()
            for block in extract_fenced_blocks(self.text)
            for line in block.splitlines()
        ]
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
