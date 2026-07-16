from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

import yaml

from solodeveling_protocol.frontmatter import ArtifactReadError, read_artifact
from solodeveling_protocol.models import ArtifactDocument, WorkStatus
from solodeveling_protocol.transitions import TransitionError, validate_transition
from solodeveling_protocol.validation import validate_document, validate_project


class LifecycleError(RuntimeError):
    """Raised when lifecycle automation cannot mutate project memory safely."""


@dataclass(frozen=True)
class LifecycleResult:
    action: str
    work_path: Path
    evidence_path: Path | None = None


WORK_ID_PATTERN = re.compile(r"^WORK-[0-9]{3,}$")
EVIDENCE_ID_PATTERN = re.compile(r"^EVIDENCE-[0-9]{3,}$")


def _require_identifier(value: str, pattern: re.Pattern[str], label: str) -> str:
    if not pattern.fullmatch(value):
        raise LifecycleError(f"invalid {label}: {value}")
    return value


def _render(document: ArtifactDocument) -> str:
    frontmatter = yaml.safe_dump(
        document.metadata,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    return f"---\n{frontmatter}---\n{document.body}"


def _validated_text(document: ArtifactDocument, kind: str) -> str:
    issues = validate_document(document, kind)
    if issues:
        details = "; ".join(issue.message for issue in issues)
        raise LifecycleError(f"{document.path.name} is invalid: {details}")
    return _render(document)


def _require_valid_project(root: Path) -> Path:
    root = root.resolve()
    issues = validate_project(root)
    if issues:
        details = "; ".join(f"{issue.code}: {issue.message}" for issue in issues)
        raise LifecycleError(f"project memory is invalid: {details}")
    return root


def _work_path(root: Path, work_id: str, *, include_archive: bool = False) -> Path:
    _require_identifier(work_id, WORK_ID_PATTERN, "work ID")
    memory = root / ".solodeveling"
    candidates = [
        memory / "work" / "active" / f"{work_id}.md",
        memory / "work" / f"{work_id}.md",
    ]
    if include_archive:
        candidates.append(memory / "work" / "archive" / f"{work_id}.md")
    matches = [path for path in candidates if path.is_file()]
    if len(matches) != 1:
        raise LifecycleError(
            f"expected exactly one {'tracked' if include_archive else 'active'} "
            f"work item for {work_id}"
        )
    return matches[0]


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as stream:
        stream.write(content)
        temporary = Path(stream.name)
    try:
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _commit_updates(root: Path, updates: dict[Path, str]) -> None:
    originals = {
        path: path.read_text(encoding="utf-8") if path.exists() else None
        for path in updates
    }
    try:
        for path, content in updates.items():
            _atomic_write(path, content)
        issues = validate_project(root)
        if issues:
            details = "; ".join(f"{issue.code}: {issue.message}" for issue in issues)
            raise LifecycleError(f"updated project memory is invalid: {details}")
    except Exception:
        for path, content in originals.items():
            if content is None:
                path.unlink(missing_ok=True)
            else:
                _atomic_write(path, content)
        raise


def transition_work(
    root: Path,
    work_id: str,
    target: WorkStatus,
    *,
    next_action: str | None = None,
) -> LifecycleResult:
    root = _require_valid_project(root)
    work_path = _work_path(root, work_id)
    state_path = root / ".solodeveling" / "state.md"
    try:
        work = read_artifact(work_path)
        state = read_artifact(state_path)
        current = WorkStatus(str(work.metadata["status"]))
        validate_transition(current, target, work.metadata)
        if target is WorkStatus.DONE:
            for evidence_id in work.metadata.get("evidence", []):
                _require_identifier(evidence_id, EVIDENCE_ID_PATTERN, "evidence ID")
                evidence = read_artifact(
                    root / ".solodeveling" / "evidence" / f"{evidence_id}.md"
                )
                if evidence.metadata.get("work_item") != work_id:
                    raise LifecycleError(
                        f"{evidence_id} belongs to another work item"
                    )
                if evidence.metadata.get("result") in {"failed", "unverified"}:
                    raise LifecycleError(
                        f"{evidence_id} has result {evidence.metadata['result']}"
                    )
    except (ArtifactReadError, KeyError, ValueError, TransitionError) as error:
        raise LifecycleError(str(error)) from error

    work_metadata = dict(work.metadata)
    work_metadata["status"] = target.value
    state_metadata = dict(state.metadata)
    active = list(state_metadata.get("active_work", []))
    if target in {WorkStatus.ACTIVE, WorkStatus.VERIFYING, WorkStatus.BLOCKED}:
        if work_id not in active:
            active.append(work_id)
    if target in {WorkStatus.DONE, WorkStatus.DEFERRED}:
        active = [item for item in active if item != work_id]
    state_metadata["active_work"] = active
    if next_action is not None:
        if not next_action.strip():
            raise LifecycleError("next action must not be blank")
        work_metadata["next_action"] = next_action
        state_metadata["next_action"] = next_action

    updated_work = ArtifactDocument(work_path, work_metadata, work.body)
    updated_state = ArtifactDocument(state_path, state_metadata, state.body)
    _commit_updates(
        root,
        {
            work_path: _validated_text(updated_work, "work-item"),
            state_path: _validated_text(updated_state, "state"),
        },
    )
    return LifecycleResult(f"transitioned to {target.value}", work_path)


def record_evidence(
    root: Path,
    work_id: str,
    *,
    claim: str,
    method: str,
    result: str,
    scope: str,
    command: str | None = None,
    limitations: tuple[str, ...] = (),
    evidence_id: str | None = None,
) -> LifecycleResult:
    root = _require_valid_project(root)
    work_path = _work_path(root, work_id, include_archive=True)
    work = read_artifact(work_path)
    existing_ids = list(work.metadata.get("evidence", []))
    if evidence_id is None:
        if len(existing_ids) > 1:
            raise LifecycleError(
                "work has multiple evidence files; pass an explicit evidence ID"
            )
        evidence_id = (
            existing_ids[0]
            if existing_ids
            else work_id.replace("WORK-", "EVIDENCE-", 1)
        )
    _require_identifier(evidence_id, EVIDENCE_ID_PATTERN, "evidence ID")
    if (
        work.metadata.get("level") == "standard"
        and existing_ids
        and evidence_id not in existing_ids
    ):
        raise LifecycleError("Standard work reuses its existing evidence file")
    evidence_path = root / ".solodeveling" / "evidence" / f"{evidence_id}.md"

    values = (claim, method, scope, *limitations)
    if any(not value.strip() for value in values):
        raise LifecycleError("evidence fields must not be blank")
    if command is not None and not command.strip():
        raise LifecycleError("evidence command must not be blank")
    if result not in {"passed", "failed", "unverified", "accepted-gap"}:
        raise LifecycleError(f"unsupported evidence result: {result}")
    if work.metadata.get("status") == WorkStatus.DONE.value and result != "passed":
        raise LifecycleError(
            "non-passing follow-up evidence requires new or reopened work"
        )

    observation = [
        f"## {claim}",
        "",
        f"- Method: {method}",
        f"- Result: {result}",
        f"- Scope: {scope}",
    ]
    if command is not None:
        observation.append(f"- Command: {command}")
    if limitations:
        observation.extend(["- Limitations:", *[f"  - {item}" for item in limitations]])
    observation_text = "\n".join(observation) + "\n"

    if evidence_path.exists():
        evidence = read_artifact(evidence_path)
        if evidence.metadata.get("work_item") != work_id:
            raise LifecycleError(f"{evidence_id} belongs to another work item")
        body = evidence.body.rstrip() + "\n\n" + observation_text
        evidence_metadata = dict(evidence.metadata)
        evidence_metadata.update(
            {
                "claim": claim,
                "method": method,
                "command": command,
                "result": result,
                "scope": scope,
                "limitations": list(limitations),
            }
        )
        updated_evidence = ArtifactDocument(evidence_path, evidence_metadata, body)
        action = "appended evidence"
    else:
        metadata = {
            "solodeveling_schema": 1,
            "id": evidence_id,
            "work_item": work_id,
            "claim": claim,
            "method": method,
            "command": command,
            "result": result,
            "scope": scope,
            "limitations": list(limitations),
        }
        body = "# Evidence\n\n" + observation_text
        updated_evidence = ArtifactDocument(evidence_path, metadata, body)
        action = "created evidence"

    work_metadata = dict(work.metadata)
    work_metadata["evidence"] = list(dict.fromkeys([*existing_ids, evidence_id]))
    updated_work = ArtifactDocument(work_path, work_metadata, work.body)
    _commit_updates(
        root,
        {
            evidence_path: _validated_text(updated_evidence, "evidence"),
            work_path: _validated_text(updated_work, "work-item"),
        },
    )
    return LifecycleResult(action, work_path, evidence_path)


def archive_work(
    root: Path,
    work_id: str,
    *,
    next_action: str | None = None,
    current_goal: str | None = None,
    state_summary: str | None = None,
) -> LifecycleResult:
    root = _require_valid_project(root)
    source = _work_path(root, work_id)
    work = read_artifact(source)
    if work.metadata.get("status") != WorkStatus.DONE.value:
        raise LifecycleError("only done work can be archived")
    destination = root / ".solodeveling" / "work" / "archive" / source.name
    if destination.exists():
        raise LifecycleError(f"archive destination already exists: {destination}")
    work_metadata = dict(work.metadata)
    work_metadata["next_action"] = "None; archived."
    archived_work = ArtifactDocument(destination, work_metadata, work.body)

    state_path = root / ".solodeveling" / "state.md"
    state = read_artifact(state_path)
    state_metadata = dict(state.metadata)
    state_metadata["active_work"] = [
        item for item in state_metadata.get("active_work", []) if item != work_id
    ]
    if next_action is not None:
        if not next_action.strip():
            raise LifecycleError("next action must not be blank")
        state_metadata["next_action"] = next_action
    if current_goal is not None:
        if not current_goal.strip():
            raise LifecycleError("current goal must not be blank")
        state_metadata["current_goal"] = current_goal
    state_body = state.body
    if state_summary is not None:
        if not state_summary.strip():
            raise LifecycleError("state summary must not be blank")
        state_body = f"# State\n\n{state_summary.strip()}\n"
    updated_state = ArtifactDocument(state_path, state_metadata, state_body)

    source_text = source.read_text(encoding="utf-8")
    state_text = state_path.read_text(encoding="utf-8")
    try:
        _atomic_write(destination, _validated_text(archived_work, "work-item"))
        _atomic_write(state_path, _validated_text(updated_state, "state"))
        source.unlink()
        issues = validate_project(root)
        if issues:
            details = "; ".join(f"{issue.code}: {issue.message}" for issue in issues)
            raise LifecycleError(f"archived project memory is invalid: {details}")
    except Exception:
        destination.unlink(missing_ok=True)
        _atomic_write(source, source_text)
        _atomic_write(state_path, state_text)
        raise
    return LifecycleResult("archived", destination)
