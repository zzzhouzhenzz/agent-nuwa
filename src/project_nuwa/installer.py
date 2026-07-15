from __future__ import annotations

import argparse
from dataclasses import dataclass
from importlib import resources
import os
from pathlib import Path
import sys
import tempfile
from typing import Sequence


class InstallConflict(RuntimeError):
    """Raised when installation would overwrite a different local agent."""


@dataclass(frozen=True)
class InstallResult:
    destination: Path
    changed: bool


def resolve_codex_home(explicit: Path | None = None) -> Path:
    """Resolve the Codex home without embedding a machine-specific path."""
    candidate = explicit
    if candidate is None:
        configured = os.environ.get("CODEX_HOME")
        candidate = Path(configured) if configured else Path.home() / ".codex"
    return candidate.expanduser().resolve()


def agent_destination(codex_home: Path | None = None) -> Path:
    return resolve_codex_home(codex_home) / "agents" / "nuwa.toml"


def agent_bytes() -> bytes:
    source = resources.files("project_nuwa.agents").joinpath("nuwa.toml")
    return source.read_bytes()


def install(codex_home: Path | None = None, *, force: bool = False) -> InstallResult:
    destination = agent_destination(codex_home)
    content = agent_bytes()

    if destination.exists():
        if destination.read_bytes() == content:
            return InstallResult(destination=destination, changed=False)
        if not force:
            raise InstallConflict(
                f"{destination} already exists with different content; "
                "re-run with --force to replace it"
            )

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=destination.parent,
            prefix=".nuwa-",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        temporary_path.replace(destination)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    return InstallResult(destination=destination, changed=True)


def check(codex_home: Path | None = None) -> tuple[bool, Path, str]:
    destination = agent_destination(codex_home)
    if not destination.exists():
        return False, destination, "NÜWA is not installed"
    if destination.read_bytes() != agent_bytes():
        return False, destination, "A different NÜWA agent is installed"
    return True, destination, "NÜWA is installed"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project-nuwa",
        description="Install the NÜWA custom agent into Codex.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    install_parser = commands.add_parser("install", help="install the agent")
    install_parser.add_argument("--codex-home", type=Path)
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing agent with different content",
    )

    check_parser = commands.add_parser("check", help="check installed content")
    check_parser.add_argument("--codex-home", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.command == "check":
        current, destination, message = check(arguments.codex_home)
        stream = sys.stdout if current else sys.stderr
        print(f"{message}: {destination}", file=stream)
        return 0 if current else 1

    try:
        result = install(arguments.codex_home, force=arguments.force)
    except InstallConflict as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: could not install NÜWA: {error}", file=sys.stderr)
        return 1

    action = "Installed NÜWA" if result.changed else "NÜWA is already current"
    print(f"{action}: {result.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
