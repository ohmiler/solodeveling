from __future__ import annotations

import hashlib
import json
import os
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


ADAPTER_SCHEMA = 1
MANIFEST_NAME = ".solodeveling-adapter.json"
RUNTIME_PATHS = {
    "codex": Path(".agents/skills"),
    "claude-code": Path(".claude/skills"),
    "cursor": Path(".cursor/skills"),
    "generic": Path(".agents/skills"),
}


class AdapterError(ValueError):
    """Raised when an adapter operation cannot proceed without risking user files."""


@dataclass(frozen=True)
class AdapterIssue:
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class AdapterReport:
    action: str
    runtime: str
    adapter_root: Path
    file_count: int
    dry_run: bool = False
    issues: tuple[AdapterIssue, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues


@dataclass(frozen=True)
class _SourcePlan:
    files: dict[str, Path]
    hashes: dict[str, str]
    source_digest: str


def _sha256_bytes(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _source_identity(hashes: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, file_hash in sorted(hashes.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    return f"sha256:{digest.hexdigest()}"


def _safe_relative(value: str) -> Path:
    if not value or "\\" in value:
        raise AdapterError(f"unsafe manifest path: {value!r}")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise AdapterError(f"unsafe manifest path: {value!r}")
    if ":" in pure.parts[0]:
        raise AdapterError(f"unsafe manifest path: {value!r}")
    return Path(*pure.parts)


def _runtime_path(runtime: str) -> Path:
    try:
        return RUNTIME_PATHS[runtime]
    except KeyError as error:
        supported = ", ".join(sorted(RUNTIME_PATHS))
        raise AdapterError(
            f"unsupported runtime {runtime!r}; choose one of: {supported}"
        ) from error


def _contained(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return False
    return True


def _ensure_target_path(project_root: Path, candidate: Path) -> None:
    project = project_root.resolve(strict=False)
    if not _contained(project, candidate):
        raise AdapterError(f"target path escapes project root: {candidate}")

    current = project_root
    if current.exists() and current.is_symlink():
        raise AdapterError(f"target symlink is not allowed: {current}")
    relative = candidate.relative_to(project_root)
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise AdapterError(f"target symlink is not allowed: {current}")
        if not current.exists():
            continue
        if current != candidate and not current.is_dir():
            raise AdapterError(f"target parent is not a directory: {current}")


def _parse_skill(skill_file: Path, expected_name: str) -> None:
    try:
        text = skill_file.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise AdapterError(f"cannot read skill {skill_file}: {error}") from error
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise AdapterError(f"{skill_file}: missing YAML frontmatter")
    try:
        boundary = lines.index("---", 1)
    except ValueError as error:
        raise AdapterError(f"{skill_file}: unterminated YAML frontmatter") from error
    try:
        metadata = yaml.safe_load("\n".join(lines[1:boundary]))
    except yaml.YAMLError as error:
        raise AdapterError(f"{skill_file}: invalid YAML frontmatter: {error}") from error
    if not isinstance(metadata, dict):
        raise AdapterError(f"{skill_file}: frontmatter must be a mapping")
    if set(metadata) != {"name", "description"}:
        raise AdapterError(
            f"{skill_file}: canonical frontmatter must contain only name and description"
        )
    if metadata.get("name") != expected_name:
        raise AdapterError(
            f"{skill_file}: name must match skill directory {expected_name}"
        )
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        raise AdapterError(f"{skill_file}: description must be non-empty")


def _build_source_plan(source_root: Path) -> _SourcePlan:
    if not source_root.is_dir():
        raise AdapterError(f"source skills directory does not exist: {source_root}")
    if source_root.is_symlink():
        raise AdapterError(f"source symlink is not allowed: {source_root}")

    files: dict[str, Path] = {}
    hashes: dict[str, str] = {}
    skills = sorted(
        path
        for path in source_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    if not skills:
        raise AdapterError(f"source contains no skill directories: {source_root}")

    for skill in skills:
        if skill.is_symlink():
            raise AdapterError(f"source symlink is not allowed: {skill}")
        _parse_skill(skill / "SKILL.md", skill.name)
        for path in sorted(skill.rglob("*")):
            if path.is_symlink():
                raise AdapterError(f"source symlink is not allowed: {path}")
            if not path.is_file():
                continue
            relative = path.relative_to(source_root).as_posix()
            safe = _safe_relative(relative)
            if safe.parts[0] != skill.name:
                raise AdapterError(f"source path escaped skill directory: {path}")
            files[relative] = path
            hashes[relative] = _sha256_file(path)

    return _SourcePlan(
        files=files,
        hashes=hashes,
        source_digest=_source_identity(hashes),
    )


def manifest_path(project_root: Path, runtime: str) -> Path:
    return project_root / _runtime_path(runtime) / MANIFEST_NAME


def _manifest_document(runtime: str, plan: _SourcePlan) -> dict[str, Any]:
    return {
        "solodeveling_adapter_schema": ADAPTER_SCHEMA,
        "runtime": runtime,
        "adapter_root": _runtime_path(runtime).as_posix(),
        "source_digest": plan.source_digest,
        "files": dict(sorted(plan.hashes.items())),
    }


def _load_manifest(project_root: Path, runtime: str) -> dict[str, Any]:
    path = manifest_path(project_root, runtime)
    _ensure_target_path(project_root, path)
    if not path.is_file():
        raise AdapterError(f"managed adapter manifest is missing: {path}")
    if path.is_symlink():
        raise AdapterError(f"target symlink is not allowed: {path}")
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise AdapterError(f"managed adapter manifest is invalid: {error}") from error
    if not isinstance(document, dict):
        raise AdapterError("managed adapter manifest must be an object")
    if document.get("solodeveling_adapter_schema") != ADAPTER_SCHEMA:
        raise AdapterError(f"managed adapter schema must equal {ADAPTER_SCHEMA}")
    if document.get("runtime") != runtime:
        raise AdapterError("managed adapter runtime does not match requested runtime")
    if document.get("adapter_root") != _runtime_path(runtime).as_posix():
        raise AdapterError("managed adapter root does not match requested runtime")
    files = document.get("files")
    if not isinstance(files, dict) or not files:
        raise AdapterError("managed adapter manifest files must be a non-empty object")
    for relative, file_hash in files.items():
        if not isinstance(relative, str):
            raise AdapterError("unsafe manifest path: non-string key")
        _safe_relative(relative)
        if not isinstance(file_hash, str) or not file_hash.startswith("sha256:"):
            raise AdapterError(f"invalid managed hash for {relative}")
    return document


def _atomic_write(content: bytes, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(
        f".{destination.name}.solodeveling-{uuid.uuid4().hex}.tmp"
    )
    try:
        temporary.write_bytes(content)
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def _atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(
        f".{destination.name}.solodeveling-{uuid.uuid4().hex}.tmp"
    )
    try:
        shutil.copyfile(source, temporary)
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def _remove_empty_parents(paths: list[Path], stop: Path) -> None:
    candidates: set[Path] = set()
    for path in paths:
        current = path.parent
        while current != stop and _contained(stop, current):
            candidates.add(current)
            current = current.parent
    for directory in sorted(candidates, key=lambda item: len(item.parts), reverse=True):
        try:
            directory.rmdir()
        except (FileNotFoundError, OSError):
            pass


def _existing_manifest(
    project_root: Path, runtime: str
) -> dict[str, Any] | None:
    path = manifest_path(project_root, runtime)
    if not path.exists():
        return None
    return _load_manifest(project_root, runtime)


def install_adapter(
    source_root: Path,
    project_root: Path,
    runtime: str,
    *,
    dry_run: bool = False,
) -> AdapterReport:
    source_root = Path(source_root)
    project_root = Path(project_root)
    adapter_root = project_root / _runtime_path(runtime)
    plan = _build_source_plan(source_root)
    manifest = _existing_manifest(project_root, runtime)
    old_hashes = manifest["files"] if manifest is not None else {}

    targets: dict[str, Path] = {
        relative: adapter_root / _safe_relative(relative)
        for relative in plan.files
    }
    for target in targets.values():
        _ensure_target_path(project_root, target)

    old_targets: dict[str, Path] = {}
    for relative, expected_hash in old_hashes.items():
        target = adapter_root / _safe_relative(relative)
        _ensure_target_path(project_root, target)
        old_targets[relative] = target
        if not target.is_file():
            raise AdapterError(f"missing managed file blocks update: {relative}")
        if target.is_symlink():
            raise AdapterError(f"target symlink is not allowed: {target}")
        if _sha256_file(target) != expected_hash:
            raise AdapterError(f"modified managed file blocks update: {relative}")

    for relative, target in targets.items():
        if not target.exists():
            continue
        if target.is_symlink():
            raise AdapterError(f"target symlink is not allowed: {target}")
        if relative not in old_hashes or not target.is_file():
            raise AdapterError(f"unmanaged collision at {target}")

    report = AdapterReport(
        action="install",
        runtime=runtime,
        adapter_root=_runtime_path(runtime),
        file_count=len(plan.files),
        dry_run=dry_run,
    )
    if dry_run:
        return report

    old_manifest_path = manifest_path(project_root, runtime)
    old_manifest_bytes = (
        old_manifest_path.read_bytes() if old_manifest_path.exists() else None
    )
    snapshots = {
        relative: target.read_bytes() for relative, target in old_targets.items()
    }
    new_paths = [
        target for relative, target in targets.items() if relative not in old_hashes
    ]
    obsolete_paths = [
        target for relative, target in old_targets.items() if relative not in plan.files
    ]

    try:
        for relative, source in plan.files.items():
            _atomic_copy(source, targets[relative])
        for target in obsolete_paths:
            target.unlink()
        document = (
            json.dumps(
                _manifest_document(runtime, plan),
                indent=2,
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )
        _atomic_write(document, old_manifest_path)
        _remove_empty_parents(obsolete_paths, adapter_root)
    except Exception as error:
        for path in new_paths:
            try:
                if path.exists() and path.is_file() and not path.is_symlink():
                    path.unlink()
            except OSError:
                pass
        for relative, content in snapshots.items():
            try:
                _atomic_write(content, old_targets[relative])
            except OSError:
                pass
        try:
            if old_manifest_bytes is None:
                if old_manifest_path.exists() and not old_manifest_path.is_symlink():
                    old_manifest_path.unlink()
            else:
                _atomic_write(old_manifest_bytes, old_manifest_path)
        except OSError:
            pass
        _remove_empty_parents(new_paths, adapter_root)
        raise AdapterError(
            f"installation failed and was rolled back: {error}"
        ) from error

    return report


def check_adapter(
    source_root: Path,
    project_root: Path,
    runtime: str,
) -> AdapterReport:
    source_root = Path(source_root)
    project_root = Path(project_root)
    adapter_root = project_root / _runtime_path(runtime)
    manifest = _load_manifest(project_root, runtime)
    managed: dict[str, str] = manifest["files"]
    issues: list[AdapterIssue] = []

    for relative, expected_hash in sorted(managed.items()):
        target = adapter_root / _safe_relative(relative)
        _ensure_target_path(project_root, target)
        if not target.exists():
            issues.append(AdapterIssue("missing", relative, "managed file is missing"))
        elif target.is_symlink() or not target.is_file():
            issues.append(AdapterIssue("modified", relative, "managed path changed type"))
        elif _sha256_file(target) != expected_hash:
            issues.append(AdapterIssue("modified", relative, "managed file hash changed"))

    managed_skills = {_safe_relative(relative).parts[0] for relative in managed}
    for skill_name in sorted(managed_skills):
        skill_root = adapter_root / skill_name
        if not skill_root.is_dir() or skill_root.is_symlink():
            continue
        for path in sorted(skill_root.rglob("*")):
            if path.is_symlink():
                relative = path.relative_to(adapter_root).as_posix()
                if relative not in managed:
                    issues.append(
                        AdapterIssue("unexpected", relative, "unexpected symlink")
                    )
            elif path.is_file():
                relative = path.relative_to(adapter_root).as_posix()
                if relative not in managed:
                    issues.append(
                        AdapterIssue("unexpected", relative, "unexpected file")
                    )

    current = _build_source_plan(source_root)
    if current.source_digest != manifest.get("source_digest"):
        issues.append(
            AdapterIssue(
                "source-drift",
                ".",
                "canonical source digest differs from installed manifest",
            )
        )

    return AdapterReport(
        action="check",
        runtime=runtime,
        adapter_root=_runtime_path(runtime),
        file_count=len(managed),
        issues=tuple(issues),
    )


def uninstall_adapter(
    project_root: Path,
    runtime: str,
    *,
    dry_run: bool = False,
) -> AdapterReport:
    project_root = Path(project_root)
    adapter_root = project_root / _runtime_path(runtime)
    manifest = _load_manifest(project_root, runtime)
    managed: dict[str, str] = manifest["files"]
    targets: dict[str, Path] = {}

    for relative, expected_hash in sorted(managed.items()):
        target = adapter_root / _safe_relative(relative)
        _ensure_target_path(project_root, target)
        targets[relative] = target
        if not target.exists():
            raise AdapterError(f"missing managed file blocks uninstall: {relative}")
        if target.is_symlink() or not target.is_file():
            raise AdapterError(f"modified managed file blocks uninstall: {relative}")
        if _sha256_file(target) != expected_hash:
            raise AdapterError(f"modified managed file blocks uninstall: {relative}")

    report = AdapterReport(
        action="uninstall",
        runtime=runtime,
        adapter_root=_runtime_path(runtime),
        file_count=len(targets),
        dry_run=dry_run,
    )
    if dry_run:
        return report

    snapshots = {relative: target.read_bytes() for relative, target in targets.items()}
    path = manifest_path(project_root, runtime)
    manifest_bytes = path.read_bytes()
    removed: list[Path] = []
    try:
        for target in targets.values():
            target.unlink()
            removed.append(target)
        path.unlink()
        _remove_empty_parents(removed + [path], adapter_root.parent)
    except Exception as error:
        for relative, content in snapshots.items():
            try:
                _atomic_write(content, targets[relative])
            except OSError:
                pass
        try:
            _atomic_write(manifest_bytes, path)
        except OSError:
            pass
        raise AdapterError(
            f"uninstall failed and managed files were restored: {error}"
        ) from error

    return report
