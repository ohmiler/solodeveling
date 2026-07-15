from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from solodeveling_protocol.memory import (
    MemoryInitializationError,
    ProjectFacts,
    initialize_memory,
)


def _parser(prog: str = "solodeveling init") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Create validated Solodeveling project memory without overwriting it.",
    )
    parser.add_argument("root", type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--user", action="append", required=True, dest="users")
    parser.add_argument("--architecture", required=True)
    parser.add_argument("--stack", action="append", required=True)
    parser.add_argument("--constraint", action="append", default=[], dest="constraints")
    parser.add_argument("--source", action="append", default=[], dest="sources")
    parser.add_argument("--goal", required=True)
    parser.add_argument("--next-action", required=True)
    return parser


def main(
    argv: Sequence[str] | None = None, *, prog: str = "solodeveling init"
) -> int:
    arguments = _parser(prog).parse_args(argv)
    try:
        result = initialize_memory(
            arguments.root,
            ProjectFacts(
                name=arguments.name,
                purpose=arguments.purpose,
                users=tuple(arguments.users),
                architecture=arguments.architecture,
                stack=tuple(arguments.stack),
                constraints=tuple(arguments.constraints),
                sources=tuple(arguments.sources),
            ),
            current_goal=arguments.goal,
            next_action=arguments.next_action,
        )
    except (MemoryInitializationError, OSError, ValueError) as error:
        print(f"Project memory was not changed: {error}")
        return 2

    if result.created:
        print(f"Project memory created: {result.memory_root}")
    else:
        print(f"Project memory already initialized: {result.memory_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())