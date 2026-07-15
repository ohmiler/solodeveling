from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path


SHA_PATTERN = re.compile(r"[0-9a-f]{40}")
SEMVER_PATTERN = re.compile(
    r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?"
)
VERSION_PATH = "src/solodeveling_protocol/__init__.py"


class PublicationGateError(ValueError):
    """Raised when a publication candidate fails the source identity gate."""


def _git(repo: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("git", *arguments),
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )


def _require_revision(repo: Path, value: str, label: str) -> None:
    if SHA_PATTERN.fullmatch(value) is None:
        raise PublicationGateError(
            f"{label} revision must be a lowercase 40-character Git SHA"
        )
    if _git(repo, "cat-file", "-e", f"{value}^{{commit}}").returncode != 0:
        raise PublicationGateError(f"{label} revision is not an available commit")


def _version_from_source(repo: Path, source_revision: str) -> str:
    completed = _git(repo, "show", f"{source_revision}:{VERSION_PATH}")
    if completed.returncode != 0:
        raise PublicationGateError("source revision lacks the canonical version file")
    try:
        module = ast.parse(completed.stdout, filename=VERSION_PATH)
    except SyntaxError as error:
        raise PublicationGateError("canonical version file is invalid Python") from error
    values: list[str] = []
    for statement in module.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__version__"
            for target in statement.targets
        ):
            continue
        if not isinstance(statement.value, ast.Constant) or not isinstance(
            statement.value.value, str
        ):
            raise PublicationGateError("canonical version must be a string literal")
        values.append(statement.value.value)
    if len(values) != 1 or SEMVER_PATTERN.fullmatch(values[0]) is None:
        raise PublicationGateError("canonical version is missing, duplicated, or invalid")
    return values[0]


def validate_candidate_source(
    repo: Path,
    *,
    source_revision: str,
    workflow_revision: str,
    expected_version: str,
) -> str:
    repo = repo.resolve()
    if not repo.is_dir():
        raise PublicationGateError("repository path is not a directory")
    if SEMVER_PATTERN.fullmatch(expected_version) is None:
        raise PublicationGateError("requested version must be an exact supported SemVer")
    _require_revision(repo, source_revision, "source")
    _require_revision(repo, workflow_revision, "workflow")
    ancestry = _git(
        repo, "merge-base", "--is-ancestor", source_revision, workflow_revision
    )
    if ancestry.returncode == 1:
        raise PublicationGateError(
            "source revision must be an ancestor of the current main workflow revision"
        )
    if ancestry.returncode != 0:
        raise PublicationGateError("could not verify source revision ancestry")
    actual_version = _version_from_source(repo, source_revision)
    if actual_version != expected_version:
        raise PublicationGateError(
            "requested version does not match the candidate source version"
        )
    return actual_version


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a source-bound candidate for the current publication workflow."
    )
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--workflow-revision", required=True)
    parser.add_argument("--expected-version", required=True)
    arguments = parser.parse_args(argv)
    try:
        version = validate_candidate_source(
            arguments.repo,
            source_revision=arguments.source_revision,
            workflow_revision=arguments.workflow_revision,
            expected_version=arguments.expected_version,
        )
    except (OSError, PublicationGateError) as error:
        print(f"publication-gate-error: {error}", file=sys.stderr)
        return 1
    print(
        f"publication candidate {version} is reachable from the current main workflow revision"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
