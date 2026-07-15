from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from solodeveling_protocol.validation import validate_project


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="solodeveling-validate",
        description="Validate Solodeveling project-memory artifacts.",
    )
    parser.add_argument("project_root", nargs="?", default=".")
    args = parser.parse_args(argv)

    issues = validate_project(Path(args.project_root))
    if not issues:
        print("Protocol validation passed")
        return 0

    for issue in issues:
        print(f"{issue.path}: [{issue.code}] {issue.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
