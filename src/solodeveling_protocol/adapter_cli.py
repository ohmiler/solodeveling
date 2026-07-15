from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from solodeveling_protocol.adapters import (
    AdapterError,
    RUNTIME_PATHS,
    check_adapter,
    install_adapter,
    uninstall_adapter,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Materialize and verify Solodeveling runtime adapters safely."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    install = subparsers.add_parser("install", help="Install or update managed skills.")
    install.add_argument("--runtime", choices=sorted(RUNTIME_PATHS), required=True)
    install.add_argument("--source", type=Path, required=True)
    install.add_argument("--project-root", type=Path, default=Path("."))
    install.add_argument("--dry-run", action="store_true")

    check = subparsers.add_parser("check", help="Check installed files and source drift.")
    check.add_argument("--runtime", choices=sorted(RUNTIME_PATHS), required=True)
    check.add_argument("--source", type=Path, required=True)
    check.add_argument("--project-root", type=Path, default=Path("."))

    uninstall = subparsers.add_parser(
        "uninstall", help="Remove only unchanged managed files."
    )
    uninstall.add_argument("--runtime", choices=sorted(RUNTIME_PATHS), required=True)
    uninstall.add_argument("--project-root", type=Path, default=Path("."))
    uninstall.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.action == "install":
            report = install_adapter(
                arguments.source,
                arguments.project_root,
                arguments.runtime,
                dry_run=arguments.dry_run,
            )
            verb = "would install" if report.dry_run else "installed"
            print(
                f"{verb} {report.file_count} files for {report.runtime} "
                f"at {report.adapter_root.as_posix()}"
            )
            return 0

        if arguments.action == "check":
            report = check_adapter(
                arguments.source,
                arguments.project_root,
                arguments.runtime,
            )
            if report.ok:
                print(
                    f"adapter is conformant for {report.runtime}: "
                    f"{report.file_count} managed files"
                )
                return 0
            for issue in report.issues:
                print(f"{issue.code}: {issue.path}: {issue.message}")
            return 1

        report = uninstall_adapter(
            arguments.project_root,
            arguments.runtime,
            dry_run=arguments.dry_run,
        )
        verb = "would uninstall" if report.dry_run else "uninstalled"
        print(
            f"{verb} {report.file_count} files for {report.runtime} "
            f"from {report.adapter_root.as_posix()}"
        )
        return 0
    except AdapterError as error:
        print(f"adapter-error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
