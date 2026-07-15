from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_nuwa.installer import (  # noqa: E402
    InstallConflict,
    agent_bytes,
    agent_destination,
    install,
    main,
    resolve_codex_home,
)


class DestinationTests(unittest.TestCase):
    def test_explicit_home_takes_precedence_over_environment(self) -> None:
        with patch.dict(os.environ, {"CODEX_HOME": "/ignored"}):
            actual = resolve_codex_home(Path("relative-codex-home"))

        self.assertEqual(actual, Path("relative-codex-home").absolute())

    def test_environment_home_is_used_when_no_explicit_path_is_given(self) -> None:
        with TemporaryDirectory() as temporary_home:
            with patch.dict(os.environ, {"CODEX_HOME": temporary_home}):
                actual = resolve_codex_home()

        self.assertEqual(actual, Path(temporary_home).resolve())

    def test_default_home_uses_current_users_home_directory(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with patch("project_nuwa.installer.Path.home", return_value=Path("/portable")):
                actual = resolve_codex_home()

        self.assertEqual(actual, Path("/portable/.codex"))


class InstallTests(unittest.TestCase):
    def test_fresh_install_creates_the_native_agent_file(self) -> None:
        with TemporaryDirectory() as temporary_home:
            home = Path(temporary_home)
            result = install(home)

            self.assertTrue(result.changed)
            self.assertEqual(
                result.destination, home.resolve() / "agents" / "nuwa.toml"
            )
            self.assertEqual(result.destination.read_bytes(), agent_bytes())

    def test_identical_install_is_idempotent(self) -> None:
        with TemporaryDirectory() as temporary_home:
            home = Path(temporary_home)
            install(home)

            result = install(home)

        self.assertFalse(result.changed)

    def test_different_existing_agent_is_not_overwritten_by_default(self) -> None:
        with TemporaryDirectory() as temporary_home:
            destination = agent_destination(Path(temporary_home))
            destination.parent.mkdir(parents=True)
            destination.write_text("private local version", encoding="utf-8")

            with self.assertRaises(InstallConflict):
                install(Path(temporary_home))

            self.assertEqual(
                destination.read_text(encoding="utf-8"), "private local version"
            )

    def test_force_replaces_a_different_existing_agent(self) -> None:
        with TemporaryDirectory() as temporary_home:
            destination = agent_destination(Path(temporary_home))
            destination.parent.mkdir(parents=True)
            destination.write_text("older version", encoding="utf-8")

            result = install(Path(temporary_home), force=True)

            self.assertTrue(result.changed)
            self.assertEqual(destination.read_bytes(), agent_bytes())


class CommandLineTests(unittest.TestCase):
    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(list(arguments))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_install_then_check_reports_the_resolved_destination(self) -> None:
        with TemporaryDirectory() as temporary_home:
            install_code, install_output, install_error = self.invoke(
                "install", "--codex-home", temporary_home
            )
            check_code, check_output, check_error = self.invoke(
                "check", "--codex-home", temporary_home
            )

        self.assertEqual(install_code, 0)
        self.assertIn("Installed NÜWA", install_output)
        self.assertEqual(install_error, "")
        self.assertEqual(check_code, 0)
        self.assertIn("NÜWA is installed", check_output)
        self.assertEqual(check_error, "")

    def test_check_fails_cleanly_when_agent_is_missing(self) -> None:
        with TemporaryDirectory() as temporary_home:
            code, output, error = self.invoke(
                "check", "--codex-home", temporary_home
            )

        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("NÜWA is not installed", error)

    def test_install_conflict_is_an_explicit_cli_error(self) -> None:
        with TemporaryDirectory() as temporary_home:
            destination = agent_destination(Path(temporary_home))
            destination.parent.mkdir(parents=True)
            destination.write_text("local custom agent", encoding="utf-8")

            code, output, error = self.invoke(
                "install", "--codex-home", temporary_home
            )

        self.assertEqual(code, 2)
        self.assertEqual(output, "")
        self.assertIn("already exists with different content", error)
        self.assertIn("--force", error)


if __name__ == "__main__":
    unittest.main()
