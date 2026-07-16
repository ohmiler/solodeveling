from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from solodeveling_protocol.lifecycle import (
    LifecycleError,
    archive_work,
    record_evidence,
    transition_work,
)
from solodeveling_protocol.models import WorkStatus


def _parser(prog: str = "solodeveling work") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Apply validated Solodeveling work, evidence, and archive updates.",
    )
    commands = parser.add_subparsers(dest="action", required=True)

    transition = commands.add_parser("transition")
    transition.add_argument("root", type=Path)
    transition.add_argument("work_id")
    transition.add_argument("status", choices=[status.value for status in WorkStatus])
    transition.add_argument("--next-action")

    evidence = commands.add_parser("evidence")
    evidence.add_argument("root", type=Path)
    evidence.add_argument("work_id")
    evidence.add_argument("--claim", required=True)
    evidence.add_argument("--method", required=True)
    evidence.add_argument(
        "--result",
        required=True,
        choices=["passed", "failed", "unverified", "accepted-gap"],
    )
    evidence.add_argument("--scope", required=True)
    evidence.add_argument("--command")
    evidence.add_argument("--limitation", action="append", default=[])
    evidence.add_argument(
        "--evidence-id",
        help="Select an existing or distinct audited evidence file.",
    )

    archive = commands.add_parser("archive")
    archive.add_argument("root", type=Path)
    archive.add_argument("work_id")
    archive.add_argument("--next-action")
    archive.add_argument("--current-goal")
    archive.add_argument("--state-summary")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    prog: str = "solodeveling work",
) -> int:
    arguments = _parser(prog).parse_args(argv)
    try:
        if arguments.action == "transition":
            result = transition_work(
                arguments.root,
                arguments.work_id,
                WorkStatus(arguments.status),
                next_action=arguments.next_action,
            )
        elif arguments.action == "evidence":
            result = record_evidence(
                arguments.root,
                arguments.work_id,
                claim=arguments.claim,
                method=arguments.method,
                result=arguments.result,
                scope=arguments.scope,
                command=arguments.command,
                limitations=tuple(arguments.limitation),
                evidence_id=arguments.evidence_id,
            )
        else:
            result = archive_work(
                arguments.root,
                arguments.work_id,
                next_action=arguments.next_action,
                current_goal=arguments.current_goal,
                state_summary=arguments.state_summary,
            )
    except (LifecycleError, OSError, ValueError) as error:
        print(f"Project memory was not changed: {error}")
        return 2

    details = f"; evidence: {result.evidence_path}" if result.evidence_path else ""
    print(f"{result.action}: {result.work_path}{details}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
