from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import TextIO

from solodeveling_protocol import __version__
from solodeveling_protocol.adapter_cli import main as adapter_main
from solodeveling_protocol.cli import main as validate_main
from solodeveling_protocol.evaluation_cli import main as evaluation_main
from solodeveling_protocol.lifecycle_cli import main as lifecycle_main
from solodeveling_protocol.memory_cli import main as memory_main


_COMMAND_HELP = (
    ("install", "Install or update Solodeveling skills for an agent runtime."),
    ("check", "Verify installed skills and report drift."),
    ("uninstall", "Safely remove unchanged managed skills."),
    ("init", "Create Solodeveling project memory."),
    ("validate", "Validate Solodeveling project memory."),
    ("work", "Record evidence, transition status, or archive tracked work."),
    ("eval", "Run or inspect cross-agent evaluations."),
    ("version", "Print the installed Solodeveling version."),
)


def _print_help(stream: TextIO) -> None:
    print("usage: solodeveling <command> [options]", file=stream)
    print(file=stream)
    print("Single-agent-first software delivery for solo developers.", file=stream)
    print(file=stream)
    print("commands:", file=stream)
    for command, description in _COMMAND_HELP:
        print(f"  {command:<11} {description}", file=stream)
    print(file=stream)
    print("Run 'solodeveling <command> --help' for command options.", file=stream)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments or arguments[0] in {"-h", "--help"}:
        _print_help(sys.stdout)
        return 0

    command = arguments[0]
    if command in {"version", "--version"}:
        if len(arguments) != 1:
            print(f"solodeveling {command}: unexpected arguments", file=sys.stderr)
            return 2
        print(f"solodeveling {__version__}")
        return 0

    if command in {"install", "check", "uninstall"}:
        return adapter_main(arguments, prog=f"solodeveling {command}")
    if command == "init":
        return memory_main(arguments[1:], prog="solodeveling init")
    if command == "validate":
        return validate_main(arguments[1:], prog="solodeveling validate")
    if command == "work":
        return lifecycle_main(arguments[1:], prog="solodeveling work")
    if command == "eval":
        return evaluation_main(arguments[1:], prog="solodeveling eval")

    print(f"solodeveling: unknown command: {command}", file=sys.stderr)
    _print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
