from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


class SmokeError(RuntimeError):
    pass


def _command(name: str) -> str:
    executable = shutil.which(name)
    if executable is None:
        raise SmokeError(f"installed command is unavailable: {name}")
    return executable


def _run(argv: tuple[str, ...], cwd: Path) -> None:
    process = subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        shell=False,
    )
    if process.returncode != 0:
        raise SmokeError(
            f"command failed with exit code {process.returncode}: {argv[0]}"
        )


def installed_smoke(workspace: Path) -> None:
    workspace = workspace.resolve()
    if workspace.exists():
        raise SmokeError(f"smoke workspace already exists: {workspace}")
    workspace.mkdir(parents=True)
    init = _command("solodeveling-init")
    validate = _command("solodeveling-validate")
    adapt = _command("solodeveling-adapt")
    evaluate = _command("solodeveling-eval")

    memory = workspace / "memory-project"
    _run(
        (
            init,
            str(memory),
            "--name",
            "installed-smoke",
            "--purpose",
            "Verify installed package",
            "--user",
            "solo developer",
            "--architecture",
            "modular",
            "--stack",
            "Python",
            "--goal",
            "Validate installed commands",
            "--next-action",
            "Run protocol validation",
        ),
        workspace,
    )
    _run((validate, str(memory)), workspace)

    for runtime in ("codex", "claude-code", "cursor", "generic"):
        project = workspace / f"adapter-{runtime}"
        project.mkdir()
        unrelated = project / "unrelated.txt"
        unrelated.write_text("preserve", encoding="utf-8")
        base = (adapt, "--runtime", runtime, "--project-root", str(project))
        _run((adapt, "install", *base[1:]), workspace)
        _run((adapt, "check", *base[1:]), workspace)
        _run((adapt, "uninstall", *base[1:], "--dry-run"), workspace)
        _run((adapt, "uninstall", *base[1:]), workspace)
        if unrelated.read_text("utf-8") != "preserve":
            raise SmokeError(f"unrelated file changed for runtime: {runtime}")

    _run(
        (
            evaluate,
            "run",
            "--runtime",
            "codex",
            "--smoke",
            "--scenario",
            "quick-local-documentation",
            "--dry-run",
        ),
        workspace,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke-test installed Solodeveling commands outside a checkout."
    )
    parser.add_argument("workspace", type=Path)
    arguments = parser.parse_args()
    try:
        installed_smoke(arguments.workspace)
    except (OSError, SmokeError) as error:
        print(f"installed-smoke-error: {error}")
        return 1
    print("Installed Solodeveling distribution smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
