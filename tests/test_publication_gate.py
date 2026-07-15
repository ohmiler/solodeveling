from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts.publication_gate import PublicationGateError, validate_candidate_source


def _git(repo: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments),
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _commit(repo: Path, message: str, version: str) -> str:
    package = repo / "src/solodeveling_protocol"
    package.mkdir(parents=True, exist_ok=True)
    (package / "__init__.py").write_text(
        f'__version__ = "{version}"\n', encoding="utf-8"
    )
    (repo / ".history").write_text(message + "\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def revision_graph(tmp_path: Path) -> tuple[Path, str, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.name", "Solodeveling Test")
    _git(repo, "config", "user.email", "test@example.invalid")
    candidate = _commit(repo, "candidate", "0.1.0")
    workflow = _commit(repo, "evidence only", "0.1.0")
    tree = _git(repo, "write-tree")
    unrelated = _git(repo, "commit-tree", tree, "-m", "unrelated")
    return repo, candidate, workflow, unrelated


def test_publication_gate_accepts_versioned_candidate_ancestor(
    revision_graph: tuple[Path, str, str, str],
) -> None:
    repo, candidate, workflow, _ = revision_graph

    assert validate_candidate_source(
        repo,
        source_revision=candidate,
        workflow_revision=workflow,
        expected_version="0.1.0",
    ) == "0.1.0"


@pytest.mark.parametrize("case", ["descendant", "unrelated"])
def test_publication_gate_rejects_revision_outside_workflow_history(
    revision_graph: tuple[Path, str, str, str], case: str
) -> None:
    repo, candidate, workflow, unrelated = revision_graph
    source = workflow if case == "descendant" else unrelated
    current = candidate if case == "descendant" else workflow

    with pytest.raises(PublicationGateError, match="ancestor"):
        validate_candidate_source(
            repo,
            source_revision=source,
            workflow_revision=current,
            expected_version="0.1.0",
        )


@pytest.mark.parametrize("revision", ["main", "a" * 39, "; touch injected", "f" * 40])
def test_publication_gate_rejects_malformed_or_missing_revision_without_execution(
    revision_graph: tuple[Path, str, str, str], revision: str
) -> None:
    repo, _, workflow, _ = revision_graph

    with pytest.raises(PublicationGateError, match="revision"):
        validate_candidate_source(
            repo,
            source_revision=revision,
            workflow_revision=workflow,
            expected_version="0.1.0",
        )

    assert not (repo / "injected").exists()


def test_publication_gate_never_executes_candidate_version_code(
    revision_graph: tuple[Path, str, str, str],
) -> None:
    repo, _, _, _ = revision_graph
    version_file = repo / "src/solodeveling_protocol/__init__.py"
    version_file.write_text(
        'from pathlib import Path\n'
        '__version__ = (Path("executed").write_text("bad"), "0.1.0")[1]\n',
        encoding="utf-8",
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "nonliteral version")
    source = _git(repo, "rev-parse", "HEAD")
    (repo / ".history").write_text("later workflow\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "later workflow")
    workflow = _git(repo, "rev-parse", "HEAD")

    with pytest.raises(PublicationGateError, match="string literal"):
        validate_candidate_source(
            repo,
            source_revision=source,
            workflow_revision=workflow,
            expected_version="0.1.0",
        )

    assert not (repo / "executed").exists()


def test_publication_gate_rejects_requested_version_mismatch(
    revision_graph: tuple[Path, str, str, str],
) -> None:
    repo, candidate, workflow, _ = revision_graph

    with pytest.raises(PublicationGateError, match="version"):
        validate_candidate_source(
            repo,
            source_revision=candidate,
            workflow_revision=workflow,
            expected_version="0.2.0",
        )
