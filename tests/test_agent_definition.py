from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
AGENT_FILE = ROOT / "src" / "project_nuwa" / "agents" / "nuwa.toml"


class AgentDefinitionTests(unittest.TestCase):
    def load_agent(self) -> dict[str, object]:
        with AGENT_FILE.open("rb") as stream:
            return tomllib.load(stream)

    def test_defines_only_the_portable_codex_agent_fields(self) -> None:
        agent = self.load_agent()

        self.assertEqual(
            set(agent), {"name", "description", "developer_instructions"}
        )
        self.assertEqual(agent["name"], "nuwa")
        self.assertIsInstance(agent["description"], str)
        self.assertIsInstance(agent["developer_instructions"], str)

    def test_enforces_one_bounded_job_and_one_created_agent(self) -> None:
        instructions = str(self.load_agent()["developer_instructions"]).lower()

        self.assertIn("one bounded job", instructions)
        self.assertIn("exactly one purpose-built agent", instructions)
        self.assertIn("more than one job", instructions)
        self.assertIn("ask for a single-job boundary", instructions)

    def test_uses_native_registration_and_direct_persona_name(self) -> None:
        instructions = str(self.load_agent()["developer_instructions"]).lower()

        self.assertIn("codex native agent interface", instructions)
        self.assertIn("real naming field", instructions)
        self.assertIn("direct persona name", instructions)
        self.assertIn("registered agent", instructions)

    def test_routes_coding_work_to_linus_without_role_play(self) -> None:
        instructions = str(self.load_agent()["developer_instructions"]).lower()

        self.assertIn("coding", instructions)
        self.assertIn("linus torvalds", instructions)
        self.assertIn("do not impersonate", instructions)

    def test_keeps_nuwa_out_of_domain_execution_and_orchestration(self) -> None:
        instructions = str(self.load_agent()["developer_instructions"]).lower()

        self.assertIn("do not perform the domain job", instructions)
        self.assertIn("do not orchestrate", instructions)
        self.assertIn("do not create a team", instructions)

    def test_contains_no_machine_local_or_secret_shaped_content(self) -> None:
        text = AGENT_FILE.read_text(encoding="utf-8")
        forbidden = (
            "/" + "Users" + "/",
            "/" + "home" + r"/[^$<{]",
            "plugins" + "/cache",
            r"\.clau" + "de/",
            r"gh[opsu]_[A-Za-z0-9]{20,}",
            r"AKIA[0-9A-Z]{16}",
            r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY",
        )

        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, text))


if __name__ == "__main__":
    unittest.main()
