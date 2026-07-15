from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from solodeveling_protocol.adapters import (
    AdapterError,
    AdapterReport,
    RUNTIME_PATHS,
    check_adapter,
    detect_install_runtimes,
    discover_managed_runtimes,
    install_adapter,
    uninstall_adapter,
)
from solodeveling_protocol.resources import resource_path


def _parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Install, verify, or remove Solodeveling skills."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    install = subparsers.add_parser(
        "install", help="Install or update managed skills automatically."
    )
    install.add_argument("--runtime", choices=sorted(RUNTIME_PATHS))
    install.add_argument("--source", type=Path)
    install.add_argument("--project-root", type=Path, default=Path("."))
    install.add_argument("--dry-run", action="store_true")

    check = subparsers.add_parser(
        "check", help="Check installed files and source drift."
    )
    check.add_argument("--runtime", choices=sorted(RUNTIME_PATHS))
    check.add_argument("--source", type=Path)
    check.add_argument("--project-root", type=Path, default=Path("."))

    uninstall = subparsers.add_parser(
        "uninstall", help="Remove only unchanged managed files."
    )
    uninstall.add_argument("--runtime", choices=sorted(RUNTIME_PATHS))
    uninstall.add_argument("--project-root", type=Path, default=Path("."))
    uninstall.add_argument("--dry-run", action="store_true")
    return parser


def _runtimes(arguments: argparse.Namespace) -> tuple[str, ...]:
    if arguments.runtime is not None:
        return (arguments.runtime,)
    if arguments.action == "install":
        return detect_install_runtimes(arguments.project_root)
    runtimes = discover_managed_runtimes(arguments.project_root)
    if not runtimes:
        raise AdapterError(
            "no managed Solodeveling installation found; run solodeveling install"
        )
    return runtimes


def _print_install_report(report: AdapterReport) -> None:
    verb = "would install" if report.dry_run else "installed"
    print(
        f"{verb} {report.file_count} files for {report.runtime} "
        f"at {report.adapter_root.as_posix()}"
    )


def _print_uninstall_report(report: AdapterReport) -> None:
    verb = "would uninstall" if report.dry_run else "uninstalled"
    print(
        f"{verb} {report.file_count} files for {report.runtime} "
        f"from {report.adapter_root.as_posix()}"
    )


def main(
    argv: Sequence[str] | None = None, *, prog: str | None = None
) -> int:
    arguments = _parser(prog).parse_args(argv)
    try:
        runtimes = _runtimes(arguments)
        if arguments.action == "uninstall":
            preflight = [
                uninstall_adapter(
                    arguments.project_root,
                    runtime,
                    dry_run=True,
                )
                for runtime in runtimes
            ]
            reports = (
                preflight
                if arguments.dry_run
                else [
                    uninstall_adapter(arguments.project_root, runtime)
                    for runtime in runtimes
                ]
            )
            for report in reports:
                _print_uninstall_report(report)
            return 0

        with resource_path("skills", arguments.source) as source:
            if arguments.action == "install":
                preflight = [
                    install_adapter(
                        source,
                        arguments.project_root,
                        runtime,
                        dry_run=True,
                    )
                    for runtime in runtimes
                ]
                reports = (
                    preflight
                    if arguments.dry_run
                    else [
                        install_adapter(source, arguments.project_root, runtime)
                        for runtime in runtimes
                    ]
                )
                for report in reports:
                    _print_install_report(report)
                return 0

            ok = True
            for runtime in runtimes:
                report = check_adapter(
                    source,
                    arguments.project_root,
                    runtime,
                )
                if report.ok:
                    print(
                        f"adapter is conformant for {report.runtime}: "
                        f"{report.file_count} managed files"
                    )
                    continue
                ok = False
                for issue in report.issues:
                    print(f"{issue.code}: {issue.path}: {issue.message}")
            return 0 if ok else 1
    except (AdapterError, FileNotFoundError, ValueError) as error:
        print(f"adapter-error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
