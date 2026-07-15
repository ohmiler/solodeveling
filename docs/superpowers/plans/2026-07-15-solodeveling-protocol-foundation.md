# Solodeveling Protocol Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task in one primary agent. Do not use subagents.

**Goal:** Build the versioned, human-readable protocol foundation that every Solodeveling workflow and runtime adapter will share.

**Architecture:** Implement the artifact contract as Markdown files with YAML frontmatter, JSON Schema Draft 2020-12 definitions, and a small Python validation package. The Python tooling is contributor and verification infrastructure; the artifacts remain readable and usable when Python is unavailable. Keep risk routing and lifecycle transitions in separate pure modules so later skills and adapters consume one semantic source of truth.

**Tech Stack:** Python 3.10+, PyYAML 6.0.3, jsonschema 4.26.0, pytest 9.1.1, JSON Schema Draft 2020-12, Markdown, YAML, Apache-2.0.

## Global Constraints

- The workflow must remain fully functional with one human and one primary agent; no correctness path may require subagents.
- Protocol artifacts must remain readable as ordinary Markdown or YAML without proprietary services.
- Python validation is optional at skill runtime; inability to run it must produce an explicit verification limitation rather than breaking the workflow.
- Support Windows, macOS, and Linux without shell-specific implementation logic.
- Use `solodeveling_schema: 1` in every versioned protocol artifact.
- Use observable risk triggers, not numeric risk scores.
- Never permit a work item to transition to `done` without evidence or an explicitly accepted verification gap.
- Critical work must include security and recovery consideration before completion.
- Do not add runtime adapters, lifecycle workflow skills, cloud services, subagent orchestration, or a full workflow engine in this plan.
- License all repository code and documentation under Apache-2.0.
- Follow the approved design at `docs/superpowers/specs/2026-07-15-solodeveling-design.md`.

## Delivery Plan Series

This plan is the first independently testable increment. Later plans will cover, in order:

1. Core router, onboarding, and project-memory creation.
2. Shaping, planning, execution, debugging, and verification skills.
3. Secure SDLC routing, findings, and initial project/security profiles.
4. Release and maintenance workflows.
5. Codex, Claude Code, and Cursor adapters.
6. Behavioral, adversarial, token-budget, and cross-agent evaluations.
7. Public packaging, installation, removal, and release verification.

## File Map

```text
LICENSE
.gitignore
pyproject.toml
src/solodeveling_protocol/
â”œâ”€â”€ __init__.py             Public package exports and protocol version
â”œâ”€â”€ frontmatter.py          Safe Markdown/YAML frontmatter loading
â”œâ”€â”€ models.py               Shared enums and immutable result types
â”œâ”€â”€ routing.py              Quick/Standard/Critical risk classification
â”œâ”€â”€ transitions.py          Work-item lifecycle transition guards
â”œâ”€â”€ validation.py           Schema and cross-artifact validation
â”œâ”€â”€ cli.py                  Thin validation command
â””â”€â”€ schemas/
    â”œâ”€â”€ work-item.schema.json
    â”œâ”€â”€ state.schema.json
    â””â”€â”€ evidence.schema.json
tests/
â”œâ”€â”€ test_package.py
â”œâ”€â”€ test_frontmatter.py
â”œâ”€â”€ test_routing.py
â”œâ”€â”€ test_transitions.py
â”œâ”€â”€ test_validation.py
â”œâ”€â”€ test_cli.py
â””â”€â”€ fixtures/
    â”œâ”€â”€ valid-project/.solodeveling/...
    â””â”€â”€ invalid-done-project/.solodeveling/...
docs/protocol-contract.md
```

---

### Task 1: Bootstrap the validation package

**Files:**

- Create: `LICENSE`
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `src/solodeveling_protocol/__init__.py`
- Test: `tests/test_package.py`

**Interfaces:**

- Consumes: The repository license and portability constraints from the approved design.
- Produces: Importable package `solodeveling_protocol`, `SCHEMA_VERSION`, and an executable `solodeveling-validate` entry point reserved for Task 6.

- [ ] **Step 1: Write the failing package test**

Create `tests/test_package.py`:

```python
from solodeveling_protocol import SCHEMA_VERSION, __version__


def test_package_exports_protocol_and_package_versions() -> None:
    assert SCHEMA_VERSION == 1
    assert __version__ == "0.1.0"
```

- [ ] **Step 2: Run the package test and verify the baseline failure**

Run:

```text
python -m pytest tests/test_package.py -q
```

Expected: collection fails with `ModuleNotFoundError: No module named 'solodeveling_protocol'`.

- [ ] **Step 3: Add packaging and repository metadata**

Create `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "solodeveling-protocol"
version = "0.1.0"
description = "Portable protocol validation for the Solodeveling agent skill suite"
requires-python = ">=3.10"
license = "Apache-2.0"
dependencies = [
  "PyYAML==6.0.3",
  "jsonschema==4.26.0",
]

[project.optional-dependencies]
dev = ["pytest==9.1.1"]

[project.scripts]
solodeveling-validate = "solodeveling_protocol.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/solodeveling_protocol"]

[tool.hatch.build.targets.wheel.force-include]
"src/solodeveling_protocol/schemas" = "solodeveling_protocol/schemas"

[tool.pytest.ini_options]
addopts = "--strict-markers --strict-config"
pythonpath = ["src"]
testpaths = ["tests"]
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
dist/
build/
*.egg-info/
.coverage
htmlcov/
```

Create `LICENSE` with the unmodified Apache License 2.0 text from `https://www.apache.org/licenses/LICENSE-2.0.txt`.

Create `src/solodeveling_protocol/__init__.py`:

```python
"""Public protocol constants for Solodeveling."""

SCHEMA_VERSION = 1
__version__ = "0.1.0"

__all__ = ["SCHEMA_VERSION", "__version__"]
```

- [ ] **Step 4: Install contributor dependencies**

Run:

```text
python -m pip install -e ".[dev]"
```

Expected: editable installation completes successfully and installs the pinned package versions.

- [ ] **Step 5: Run the package test**

Run:

```text
python -m pytest tests/test_package.py -q
```

Expected: `1 passed`.

- [ ] **Step 6: Commit the package bootstrap**

```text
git add LICENSE .gitignore pyproject.toml src/solodeveling_protocol/__init__.py tests/test_package.py
git commit -m "build: bootstrap protocol validation package"
```

---

### Task 2: Parse versioned Markdown frontmatter safely

**Files:**

- Create: `src/solodeveling_protocol/models.py`
- Create: `src/solodeveling_protocol/frontmatter.py`
- Test: `tests/test_frontmatter.py`

**Interfaces:**

- Consumes: `SCHEMA_VERSION` from `solodeveling_protocol`.
- Produces: `ArtifactDocument`, `ArtifactReadError`, and `read_artifact(path: Path) -> ArtifactDocument` for schema validation and fixture loading.

- [ ] **Step 1: Write frontmatter behavior tests**

Create `tests/test_frontmatter.py`:

```python
from pathlib import Path

import pytest

from solodeveling_protocol.frontmatter import ArtifactReadError, read_artifact


def test_read_artifact_returns_metadata_and_body(tmp_path: Path) -> None:
    path = tmp_path / "work.md"
    path.write_text(
        "---\nsolodeveling_schema: 1\nid: WORK-001\n---\n# Notes\n",
        encoding="utf-8",
    )

    document = read_artifact(path)

    assert document.path == path
    assert document.metadata == {"solodeveling_schema": 1, "id": "WORK-001"}
    assert document.body == "# Notes\n"


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("# Missing frontmatter\n", "must start with YAML frontmatter"),
        ("---\n[invalid\n---\n", "contains invalid YAML"),
        ("---\n- not-a-mapping\n---\n", "frontmatter must be a mapping"),
        ("---\nid: WORK-001\n---\n", "solodeveling_schema must equal 1"),
    ],
)
def test_read_artifact_rejects_invalid_documents(
    tmp_path: Path, content: str, message: str
) -> None:
    path = tmp_path / "invalid.md"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ArtifactReadError, match=message):
        read_artifact(path)
```

- [ ] **Step 2: Run the tests and verify the missing-module failure**

Run:

```text
python -m pytest tests/test_frontmatter.py -q
```

Expected: collection fails because `solodeveling_protocol.frontmatter` does not exist.

- [ ] **Step 3: Add shared immutable models**

Create `src/solodeveling_protocol/models.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class WorkType(str, Enum):
    EXPLORE = "explore"
    BUILD = "build"
    CHANGE = "change"
    REPAIR = "repair"
    SECURE = "secure"
    RELEASE = "release"
    MAINTAIN = "maintain"


class WorkLevel(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    CRITICAL = "critical"


class WorkStatus(str, Enum):
    CAPTURED = "captured"
    SHAPED = "shaped"
    READY = "ready"
    ACTIVE = "active"
    VERIFYING = "verifying"
    DONE = "done"
    BLOCKED = "blocked"
    DEFERRED = "deferred"


@dataclass(frozen=True)
class ArtifactDocument:
    path: Path
    metadata: dict[str, Any]
    body: str


@dataclass(frozen=True)
class RoutingDecision:
    level: WorkLevel
    triggers: tuple[str, ...]
    downgrade_warning: str | None = None


@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    code: str
    message: str
```

- [ ] **Step 4: Implement strict frontmatter loading**

Create `src/solodeveling_protocol/frontmatter.py`:

```python
from __future__ import annotations

from pathlib import Path

import yaml

from solodeveling_protocol import SCHEMA_VERSION
from solodeveling_protocol.models import ArtifactDocument


class ArtifactReadError(ValueError):
    """Raised when a protocol artifact cannot be read safely."""


def read_artifact(path: Path) -> ArtifactDocument:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ArtifactReadError(f"{path} must start with YAML frontmatter")

    closing = text.find("\n---\n", 4)
    if closing == -1:
        raise ArtifactReadError(f"{path} must close YAML frontmatter with ---")

    raw_metadata = text[4:closing]
    body = text[closing + 5 :]
    try:
        metadata = yaml.safe_load(raw_metadata)
    except yaml.YAMLError as error:
        raise ArtifactReadError(f"{path} contains invalid YAML: {error}") from error

    if not isinstance(metadata, dict):
        raise ArtifactReadError(f"{path} frontmatter must be a mapping")
    if metadata.get("solodeveling_schema") != SCHEMA_VERSION:
        raise ArtifactReadError(
            f"{path} solodeveling_schema must equal {SCHEMA_VERSION}"
        )

    return ArtifactDocument(path=path, metadata=metadata, body=body)
```

- [ ] **Step 5: Run frontmatter and package tests**

Run:

```text
python -m pytest tests/test_package.py tests/test_frontmatter.py -q
```

Expected: `6 passed`.

- [ ] **Step 6: Commit frontmatter parsing**

```text
git add src/solodeveling_protocol/models.py src/solodeveling_protocol/frontmatter.py tests/test_frontmatter.py
git commit -m "feat: parse versioned protocol artifacts"
```

---

### Task 3: Define work, state, and evidence schemas

**Files:**

- Create: `src/solodeveling_protocol/schemas/work-item.schema.json`
- Create: `src/solodeveling_protocol/schemas/state.schema.json`
- Create: `src/solodeveling_protocol/schemas/evidence.schema.json`
- Create: `src/solodeveling_protocol/validation.py`
- Test: `tests/test_validation.py`

**Interfaces:**

- Consumes: `ArtifactDocument` and `ValidationIssue` from Task 2.
- Produces: `validate_document(document, kind) -> list[ValidationIssue]` and schemas named `work-item`, `state`, and `evidence`.

- [ ] **Step 1: Write schema validation tests**

Create `tests/test_validation.py`:

```python
from pathlib import Path

from solodeveling_protocol.models import ArtifactDocument
from solodeveling_protocol.validation import validate_document


def document(metadata: dict) -> ArtifactDocument:
    return ArtifactDocument(Path("artifact.md"), metadata, "")


def test_valid_work_item_has_no_issues() -> None:
    metadata = {
        "solodeveling_schema": 1,
        "id": "WORK-001",
        "title": "Add password reset",
        "status": "active",
        "level": "critical",
        "type": "build",
        "goal": "Provide a safe password reset flow.",
        "scope": "Request and completion flows.",
        "out_of_scope": "Manual support recovery.",
        "acceptance": ["Expired tokens are rejected."],
        "risks": ["Leaked tokens could enable account takeover."],
        "decisions": [],
        "verification": ["Integration test expired and replayed tokens."],
        "next_action": "Write the failing expired-token test.",
        "security_considerations": ["Tokens are single-use and short-lived."],
        "recovery": ["Disable reset issuance and invalidate outstanding tokens."],
    }

    assert validate_document(document(metadata), "work-item") == []


def test_quick_work_item_accepts_compact_contract() -> None:
    metadata = {
        "solodeveling_schema": 1,
        "id": "WORK-002",
        "title": "Fix documentation typo",
        "status": "active",
        "level": "quick",
        "type": "change",
        "goal": "Correct a reversible documentation typo.",
        "next_action": "Correct and inspect the rendered sentence.",
    }

    assert validate_document(document(metadata), "work-item") == []


def test_work_item_reports_all_schema_failures() -> None:
    metadata = {"solodeveling_schema": 1, "id": "bad id", "status": "unknown"}

    issues = validate_document(document(metadata), "work-item")

    assert len(issues) > 1
    assert {issue.code for issue in issues} == {"schema"}


def test_unknown_artifact_kind_is_reported() -> None:
    issues = validate_document(document({"solodeveling_schema": 1}), "unknown")

    assert [(issue.code, issue.message) for issue in issues] == [
        ("unknown-kind", "Unknown artifact kind: unknown")
    ]
```

- [ ] **Step 2: Run the tests and verify the missing validator failure**

Run:

```text
python -m pytest tests/test_validation.py -q
```

Expected: collection fails because `solodeveling_protocol.validation` does not exist.

- [ ] **Step 3: Create the work-item schema**

Create `src/solodeveling_protocol/schemas/work-item.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://solodeveling.dev/schemas/v1/work-item.schema.json",
  "type": "object",
  "required": ["solodeveling_schema", "id", "title", "status", "level", "type", "goal", "next_action"],
  "properties": {
    "solodeveling_schema": {"const": 1},
    "id": {"type": "string", "pattern": "^WORK-[0-9]{3,}$"},
    "title": {"type": "string", "minLength": 1},
    "status": {
      "enum": ["captured", "shaped", "ready", "active", "verifying", "done", "blocked", "deferred"]
    },
    "level": {"enum": ["quick", "standard", "critical"]},
    "type": {"enum": ["explore", "build", "change", "repair", "secure", "release", "maintain"]},
    "goal": {"type": "string", "minLength": 1},
    "scope": {"type": "string", "minLength": 1},
    "out_of_scope": {"type": "string"},
    "acceptance": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
    "risks": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "decisions": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "verification": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "next_action": {"type": "string", "minLength": 1},
    "security_considerations": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "recovery": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "accepted_verification_gaps": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "evidence": {"type": "array", "items": {"type": "string", "minLength": 1}}
  },
  "additionalProperties": false,
  "allOf": [
    {
      "if": {"properties": {"level": {"enum": ["standard", "critical"]}}},
      "then": {
        "required": ["scope", "out_of_scope", "acceptance", "risks", "decisions", "verification"]
      }
    }
  ]
}
```

- [ ] **Step 4: Create the state and evidence schemas**

Create `src/solodeveling_protocol/schemas/state.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://solodeveling.dev/schemas/v1/state.schema.json",
  "type": "object",
  "required": ["solodeveling_schema", "current_goal", "active_work", "blockers", "risks", "next_action"],
  "properties": {
    "solodeveling_schema": {"const": 1},
    "current_goal": {"type": "string", "minLength": 1},
    "active_work": {"type": "array", "uniqueItems": true, "items": {"type": "string", "pattern": "^WORK-[0-9]{3,}$"}},
    "blockers": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "risks": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "next_action": {"type": "string", "minLength": 1}
  },
  "additionalProperties": false
}
```

Create `src/solodeveling_protocol/schemas/evidence.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://solodeveling.dev/schemas/v1/evidence.schema.json",
  "type": "object",
  "required": ["solodeveling_schema", "id", "work_item", "claim", "method", "result", "scope", "limitations"],
  "properties": {
    "solodeveling_schema": {"const": 1},
    "id": {"type": "string", "pattern": "^EVIDENCE-[0-9]{3,}$"},
    "work_item": {"type": "string", "pattern": "^WORK-[0-9]{3,}$"},
    "claim": {"type": "string", "minLength": 1},
    "method": {"type": "string", "minLength": 1},
    "command": {"type": ["string", "null"]},
    "result": {"enum": ["passed", "failed", "unverified", "accepted-gap"]},
    "scope": {"type": "string", "minLength": 1},
    "limitations": {"type": "array", "items": {"type": "string", "minLength": 1}}
  },
  "additionalProperties": false
}
```

- [ ] **Step 5: Implement schema validation**

Create `src/solodeveling_protocol/validation.py`:

```python
from __future__ import annotations

import json
from importlib.resources import files

from jsonschema import Draft202012Validator

from solodeveling_protocol.models import ArtifactDocument, ValidationIssue


SCHEMA_FILES = {
    "work-item": "work-item.schema.json",
    "state": "state.schema.json",
    "evidence": "evidence.schema.json",
}


def _load_schema(kind: str) -> dict:
    resource = files("solodeveling_protocol").joinpath("schemas", SCHEMA_FILES[kind])
    return json.loads(resource.read_text(encoding="utf-8"))


def validate_document(
    document: ArtifactDocument, kind: str
) -> list[ValidationIssue]:
    if kind not in SCHEMA_FILES:
        return [
            ValidationIssue(
                path=document.path,
                code="unknown-kind",
                message=f"Unknown artifact kind: {kind}",
            )
        ]

    validator = Draft202012Validator(_load_schema(kind))
    errors = sorted(validator.iter_errors(document.metadata), key=lambda error: list(error.path))
    return [
        ValidationIssue(
            path=document.path,
            code="schema",
            message=f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}",
        )
        for error in errors
    ]
```

- [ ] **Step 6: Run schema validation tests**

Run:

```text
python -m pytest tests/test_validation.py -q
```

Expected: `4 passed`.

- [ ] **Step 7: Run the full suite and commit schemas**

Run:

```text
python -m pytest -q
```

Expected: `10 passed`.

Commit:

```text
git add src/solodeveling_protocol/schemas src/solodeveling_protocol/validation.py tests/test_validation.py
git commit -m "feat: define versioned artifact schemas"
```

---

### Task 4: Implement observable risk routing

**Files:**

- Create: `src/solodeveling_protocol/routing.py`
- Test: `tests/test_routing.py`

**Interfaces:**

- Consumes: `RoutingDecision` and `WorkLevel` from Task 2.
- Produces: `classify_level(summary, requested_level=None, downgrade_accepted=False) -> RoutingDecision`.

- [ ] **Step 1: Write routing tests**

Create `tests/test_routing.py`:

```python
import pytest

from solodeveling_protocol.models import WorkLevel
from solodeveling_protocol.routing import classify_level


def test_low_impact_reversible_work_can_be_quick() -> None:
    decision = classify_level("Fix a typo in local documentation", WorkLevel.QUICK)

    assert decision.level is WorkLevel.QUICK
    assert decision.triggers == ()


def test_unspecified_ordinary_feature_defaults_to_standard() -> None:
    decision = classify_level("Add filtering to the product list")

    assert decision.level is WorkLevel.STANDARD


@pytest.mark.parametrize(
    ("summary", "trigger"),
    [
        ("Change authorization checks for admin accounts", "identity-access"),
        ("Migrate sensitive customer data", "sensitive-data"),
        ("Rotate production encryption secrets", "cryptography-secrets"),
        ("Deploy a destructive database migration", "destructive-migration"),
        ("Change payment transaction settlement", "payments"),
    ],
)
def test_critical_trigger_forces_critical_level(summary: str, trigger: str) -> None:
    decision = classify_level(summary)

    assert decision.level is WorkLevel.CRITICAL
    assert trigger in decision.triggers


def test_critical_work_cannot_be_silently_downgraded() -> None:
    decision = classify_level(
        "Change login authentication", requested_level=WorkLevel.STANDARD
    )

    assert decision.level is WorkLevel.CRITICAL
    assert decision.downgrade_warning is not None


def test_explicit_risk_acceptance_allows_downgrade() -> None:
    decision = classify_level(
        "Change login authentication",
        requested_level=WorkLevel.STANDARD,
        downgrade_accepted=True,
    )

    assert decision.level is WorkLevel.STANDARD
    assert decision.downgrade_warning is not None
```

- [ ] **Step 2: Run the routing tests and verify failure**

Run:

```text
python -m pytest tests/test_routing.py -q
```

Expected: collection fails because `solodeveling_protocol.routing` does not exist.

- [ ] **Step 3: Implement deterministic critical-trigger routing**

Create `src/solodeveling_protocol/routing.py`:

```python
from __future__ import annotations

import re

from solodeveling_protocol.models import RoutingDecision, WorkLevel


CRITICAL_TRIGGERS: dict[str, re.Pattern[str]] = {
    "identity-access": re.compile(
        r"\b(auth(?:entication|orization)?|login|session|permission|admin account)\b",
        re.IGNORECASE,
    ),
    "payments": re.compile(
        r"\b(payment|billing|financial|transaction settlement)\b", re.IGNORECASE
    ),
    "sensitive-data": re.compile(
        r"\b(sensitive|personal|private|customer data|health data)\b", re.IGNORECASE
    ),
    "destructive-migration": re.compile(
        r"\b(destructive|drop table|delete data|irreversible)\b",
        re.IGNORECASE,
    ),
    "production-infrastructure": re.compile(
        r"\b(production|public api|infrastructure|iam|firewall)\b", re.IGNORECASE
    ),
    "cryptography-secrets": re.compile(
        r"\b(cryptograph|encryption|secret|credential|private key)\w*\b",
        re.IGNORECASE,
    ),
    "safety-critical": re.compile(
        r"\b(safety-critical|medical device|life safety)\b", re.IGNORECASE
    ),
}


def classify_level(
    summary: str,
    requested_level: WorkLevel | None = None,
    downgrade_accepted: bool = False,
) -> RoutingDecision:
    triggers = tuple(
        name for name, pattern in CRITICAL_TRIGGERS.items() if pattern.search(summary)
    )
    warning = None

    if triggers:
        if requested_level in {WorkLevel.QUICK, WorkLevel.STANDARD}:
            warning = (
                "Critical triggers detected: "
                + ", ".join(triggers)
                + ". Lowering the level requires explicit risk acceptance."
            )
            if downgrade_accepted:
                return RoutingDecision(requested_level, triggers, warning)
        return RoutingDecision(WorkLevel.CRITICAL, triggers, warning)

    return RoutingDecision(requested_level or WorkLevel.STANDARD, ())
```

- [ ] **Step 4: Run routing tests**

Run:

```text
python -m pytest tests/test_routing.py -q
```

Expected: `9 passed`.

- [ ] **Step 5: Run the full suite and commit routing**

Run:

```text
python -m pytest -q
```

Expected: `19 passed`.

Commit:

```text
git add src/solodeveling_protocol/routing.py tests/test_routing.py
git commit -m "feat: classify work by observable risk triggers"
```

---

### Task 5: Enforce lifecycle completion guards

**Files:**

- Create: `src/solodeveling_protocol/transitions.py`
- Test: `tests/test_transitions.py`

**Interfaces:**

- Consumes: `WorkLevel` and `WorkStatus` from Task 2 plus validated work-item metadata from Task 3.
- Produces: `TransitionError` and `validate_transition(current, target, metadata) -> None`.

- [ ] **Step 1: Write lifecycle tests**

Create `tests/test_transitions.py`:

```python
import pytest

from solodeveling_protocol.models import WorkStatus
from solodeveling_protocol.transitions import TransitionError, validate_transition


def metadata(**overrides: object) -> dict:
    value = {
        "level": "standard",
        "evidence": ["EVIDENCE-001"],
        "accepted_verification_gaps": [],
        "security_considerations": [],
        "recovery": [],
    }
    value.update(overrides)
    return value


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (WorkStatus.CAPTURED, WorkStatus.SHAPED),
        (WorkStatus.SHAPED, WorkStatus.READY),
        (WorkStatus.READY, WorkStatus.ACTIVE),
        (WorkStatus.ACTIVE, WorkStatus.VERIFYING),
        (WorkStatus.VERIFYING, WorkStatus.DONE),
        (WorkStatus.ACTIVE, WorkStatus.BLOCKED),
        (WorkStatus.BLOCKED, WorkStatus.ACTIVE),
        (WorkStatus.ACTIVE, WorkStatus.DEFERRED),
    ],
)
def test_allowed_transition(current: WorkStatus, target: WorkStatus) -> None:
    validate_transition(current, target, metadata())


def test_cannot_skip_verifying() -> None:
    with pytest.raises(TransitionError, match="not allowed"):
        validate_transition(WorkStatus.ACTIVE, WorkStatus.DONE, metadata())


def test_done_requires_evidence_or_accepted_gap() -> None:
    with pytest.raises(TransitionError, match="evidence or an accepted verification gap"):
        validate_transition(
            WorkStatus.VERIFYING,
            WorkStatus.DONE,
            metadata(evidence=[], accepted_verification_gaps=[]),
        )


def test_critical_done_requires_security_and_recovery() -> None:
    with pytest.raises(TransitionError, match="security and recovery"):
        validate_transition(
            WorkStatus.VERIFYING,
            WorkStatus.DONE,
            metadata(level="critical"),
        )


def test_critical_done_accepts_security_and_recovery() -> None:
    validate_transition(
        WorkStatus.VERIFYING,
        WorkStatus.DONE,
        metadata(
            level="critical",
            security_considerations=["Threat model reviewed."],
            recovery=["Rollback procedure verified."],
        ),
    )
```

- [ ] **Step 2: Run lifecycle tests and verify failure**

Run:

```text
python -m pytest tests/test_transitions.py -q
```

Expected: collection fails because `solodeveling_protocol.transitions` does not exist.

- [ ] **Step 3: Implement the transition graph and completion guards**

Create `src/solodeveling_protocol/transitions.py`:

```python
from __future__ import annotations

from collections.abc import Mapping

from solodeveling_protocol.models import WorkStatus


class TransitionError(ValueError):
    """Raised when a work-item state transition violates the protocol."""


ALLOWED_TRANSITIONS: dict[WorkStatus, frozenset[WorkStatus]] = {
    WorkStatus.CAPTURED: frozenset({WorkStatus.SHAPED, WorkStatus.DEFERRED}),
    WorkStatus.SHAPED: frozenset({WorkStatus.READY, WorkStatus.DEFERRED}),
    WorkStatus.READY: frozenset({WorkStatus.ACTIVE, WorkStatus.BLOCKED, WorkStatus.DEFERRED}),
    WorkStatus.ACTIVE: frozenset({WorkStatus.VERIFYING, WorkStatus.BLOCKED, WorkStatus.DEFERRED}),
    WorkStatus.VERIFYING: frozenset({WorkStatus.ACTIVE, WorkStatus.DONE, WorkStatus.BLOCKED}),
    WorkStatus.BLOCKED: frozenset({WorkStatus.ACTIVE, WorkStatus.DEFERRED}),
    WorkStatus.DEFERRED: frozenset({WorkStatus.ACTIVE}),
    WorkStatus.DONE: frozenset(),
}


def validate_transition(
    current: WorkStatus, target: WorkStatus, metadata: Mapping[str, object]
) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise TransitionError(f"Transition {current} -> {target} is not allowed")

    if target is not WorkStatus.DONE:
        return

    evidence = metadata.get("evidence") or []
    gaps = metadata.get("accepted_verification_gaps") or []
    if not evidence and not gaps:
        raise TransitionError(
            "done requires evidence or an accepted verification gap"
        )

    if metadata.get("level") == "critical":
        security = metadata.get("security_considerations") or []
        recovery = metadata.get("recovery") or []
        if not security or not recovery:
            raise TransitionError(
                "critical done requires security and recovery consideration"
            )
```

- [ ] **Step 4: Run lifecycle tests**

Run:

```text
python -m pytest tests/test_transitions.py -q
```

Expected: `12 passed`.

- [ ] **Step 5: Run the full suite and commit transitions**

Run:

```text
python -m pytest -q
```

Expected: `31 passed`.

Commit:

```text
git add src/solodeveling_protocol/transitions.py tests/test_transitions.py
git commit -m "feat: guard work-item lifecycle transitions"
```

---

### Task 6: Validate complete project-memory fixtures

**Files:**

- Modify: `src/solodeveling_protocol/validation.py`
- Create: `src/solodeveling_protocol/cli.py`
- Create: `tests/fixtures/valid-project/.solodeveling/state.md`
- Create: `tests/fixtures/valid-project/.solodeveling/work/active/WORK-001.md`
- Create: `tests/fixtures/valid-project/.solodeveling/evidence/EVIDENCE-001.md`
- Create: `tests/fixtures/invalid-done-project/.solodeveling/state.md`
- Create: `tests/fixtures/invalid-done-project/.solodeveling/work/archive/WORK-002.md`
- Test: `tests/test_cli.py`
- Test: `tests/test_validation.py`
- Create: `docs/protocol-contract.md`

**Interfaces:**

- Consumes: frontmatter reader, schemas, and completion rules from Tasks 2-5.
- Produces: `validate_project(root: Path) -> list[ValidationIssue]` and CLI `solodeveling-validate [PROJECT_ROOT]` with exit code 0 for valid state and 1 for invalid state.

- [ ] **Step 1: Add project-level validation tests**

Append to `tests/test_validation.py`:

```python
def test_valid_project_fixture_has_no_issues() -> None:
    from solodeveling_protocol.validation import validate_project

    root = Path("tests/fixtures/valid-project")
    assert validate_project(root) == []


def test_done_project_without_evidence_is_rejected() -> None:
    from solodeveling_protocol.validation import validate_project

    root = Path("tests/fixtures/invalid-done-project")
    issues = validate_project(root)

    assert any(issue.code == "done-without-evidence" for issue in issues)
```

Add `from pathlib import Path` to the existing imports in `tests/test_validation.py` if it is not already present.

Create `tests/test_cli.py`:

```python
from solodeveling_protocol.cli import main


def test_cli_returns_zero_for_valid_project(capsys) -> None:
    exit_code = main(["tests/fixtures/valid-project"])

    assert exit_code == 0
    assert "Protocol validation passed" in capsys.readouterr().out


def test_cli_returns_one_and_prints_issues_for_invalid_project(capsys) -> None:
    exit_code = main(["tests/fixtures/invalid-done-project"])

    assert exit_code == 1
    assert "done-without-evidence" in capsys.readouterr().out
```

- [ ] **Step 2: Run project and CLI tests and verify failure**

Run:

```text
python -m pytest tests/test_validation.py tests/test_cli.py -q
```

Expected: collection fails because `solodeveling_protocol.cli` and `validate_project` do not exist.

- [ ] **Step 3: Create the valid fixture**

Create `tests/fixtures/valid-project/.solodeveling/state.md`:

```markdown
---
solodeveling_schema: 1
current_goal: Validate the protocol foundation.
active_work:
  - WORK-001
blockers: []
risks: []
next_action: Close the validated foundation work item.
---
# State
```

Create `tests/fixtures/valid-project/.solodeveling/work/active/WORK-001.md`:

```markdown
---
solodeveling_schema: 1
id: WORK-001
title: Validate protocol foundation
status: verifying
level: standard
type: build
goal: Prove that versioned project artifacts validate consistently.
scope: State, active work item, and evidence fixtures.
out_of_scope: Runtime adapters.
acceptance:
  - The project validator returns no issues.
risks: []
decisions: []
verification:
  - Run solodeveling-validate against the fixture.
next_action: Run the project validator.
evidence:
  - EVIDENCE-001
---
# Work notes
```

Create `tests/fixtures/valid-project/.solodeveling/evidence/EVIDENCE-001.md`:

```markdown
---
solodeveling_schema: 1
id: EVIDENCE-001
work_item: WORK-001
claim: The valid fixture satisfies the version 1 protocol.
method: Automated schema and cross-reference validation.
command: solodeveling-validate tests/fixtures/valid-project
result: passed
scope: State, active work item, and evidence artifacts.
limitations: []
---
# Evidence
```

- [ ] **Step 4: Create the invalid completion fixture**

Create `tests/fixtures/invalid-done-project/.solodeveling/state.md`:

```markdown
---
solodeveling_schema: 1
current_goal: Demonstrate invalid completion detection.
active_work: []
blockers: []
risks: []
next_action: Restore missing completion evidence.
---
# State
```

Create `tests/fixtures/invalid-done-project/.solodeveling/work/archive/WORK-002.md`:

```markdown
---
solodeveling_schema: 1
id: WORK-002
title: Invalid completed work
status: done
level: standard
type: build
goal: Demonstrate that completion requires evidence.
scope: Invalid archived work fixture.
out_of_scope: Runtime behavior.
acceptance:
  - Missing evidence is reported.
risks: []
decisions: []
verification:
  - Validate the fixture.
next_action: Add evidence before closing the work item.
evidence: []
accepted_verification_gaps: []
---
# Invalid work
```

- [ ] **Step 5: Implement project-level validation**

Append to `src/solodeveling_protocol/validation.py`:

```python
from pathlib import Path

from solodeveling_protocol.frontmatter import ArtifactReadError, read_artifact


def _artifact_kind(path: Path) -> str | None:
    normalized = path.as_posix()
    if normalized.endswith("/.solodeveling/state.md"):
        return "state"
    if "/.solodeveling/work/" in normalized:
        return "work-item"
    if "/.solodeveling/evidence/" in normalized:
        return "evidence"
    return None


def validate_project(root: Path) -> list[ValidationIssue]:
    memory_root = root / ".solodeveling"
    if not memory_root.is_dir():
        return [
            ValidationIssue(memory_root, "missing-memory", ".solodeveling directory is missing")
        ]

    issues: list[ValidationIssue] = []
    work_items: dict[str, ArtifactDocument] = {}
    evidence_ids: set[str] = set()

    for path in sorted(memory_root.rglob("*.md")):
        kind = _artifact_kind(path)
        if kind is None:
            continue
        try:
            document = read_artifact(path)
        except (ArtifactReadError, OSError) as error:
            issues.append(ValidationIssue(path, "read-error", str(error)))
            continue

        issues.extend(validate_document(document, kind))
        if kind == "work-item" and isinstance(document.metadata.get("id"), str):
            work_items[document.metadata["id"]] = document
        if kind == "evidence" and isinstance(document.metadata.get("id"), str):
            evidence_ids.add(document.metadata["id"])

    for document in work_items.values():
        metadata = document.metadata
        references = set(metadata.get("evidence", []))
        missing = sorted(references - evidence_ids)
        for evidence_id in missing:
            issues.append(
                ValidationIssue(
                    document.path,
                    "missing-evidence",
                    f"Referenced evidence does not exist: {evidence_id}",
                )
            )
        if metadata.get("status") == "done":
            gaps = metadata.get("accepted_verification_gaps", [])
            if not references and not gaps:
                issues.append(
                    ValidationIssue(
                        document.path,
                        "done-without-evidence",
                        "Done work requires evidence or an accepted verification gap",
                    )
                )
            if metadata.get("level") == "critical" and (
                not metadata.get("security_considerations")
                or not metadata.get("recovery")
            ):
                issues.append(
                    ValidationIssue(
                        document.path,
                        "critical-completion-gap",
                        "Critical done work requires security and recovery consideration",
                    )
                )

    return issues
```

Move the new imports to the existing import blocks so `validation.py` has one `pathlib` import and one models import containing both `ArtifactDocument` and `ValidationIssue`.

- [ ] **Step 6: Implement the thin CLI**

Create `src/solodeveling_protocol/cli.py`:

```python
from __future__ import annotations

import argparse
from pathlib import Path
from collections.abc import Sequence

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
```

- [ ] **Step 7: Run fixture and CLI tests**

Run:

```text
python -m pytest tests/test_validation.py tests/test_cli.py -q
```

Expected: `8 passed`.

- [ ] **Step 8: Document the protocol contract**

Create `docs/protocol-contract.md` with these exact sections and rules:

```markdown
# Solodeveling Protocol Contract

## Portability

Project memory is Markdown with YAML frontmatter. Humans and agents may use it without Python. The validator is optional verification tooling and never a workflow correctness dependency.

## Schema version

Every protocol artifact includes `solodeveling_schema: 1`. A future schema change requires validation, backup, migration, and safe failure without partial state changes.

## Artifact kinds

- `.solodeveling/state.md` uses `state.schema.json`.
- `.solodeveling/work/active/*.md` and `.solodeveling/work/archive/*.md` use `work-item.schema.json`.
- `.solodeveling/evidence/*.md` uses `evidence.schema.json`.

## Completion invariants

- Work passes through `verifying` before `done`.
- Done work references evidence or records an accepted verification gap.
- Critical done work records security and recovery consideration.
- Evidence reports claim, method, result, scope, and limitations.
- Missing execution capability is recorded as unverified, not passed.

## Validation

Run `solodeveling-validate <project-root>`. Exit code 0 means the inspected artifacts satisfy the implemented structural and cross-reference checks. It does not prove that the software itself is correct or secure.
```

- [ ] **Step 9: Run full verification**

Run:

```text
python -m pytest -q
solodeveling-validate tests/fixtures/valid-project
python -m solodeveling_protocol.cli tests/fixtures/invalid-done-project
```

Expected:

- Pytest reports `35 passed`.
- Valid fixture prints `Protocol validation passed` and exits 0.
- Invalid fixture prints at least one `[done-without-evidence]` issue and exits 1.

- [ ] **Step 10: Commit end-to-end validation**

```text
git add src/solodeveling_protocol/validation.py src/solodeveling_protocol/cli.py tests/fixtures tests/test_cli.py tests/test_validation.py docs/protocol-contract.md
git commit -m "feat: validate project memory end to end"
```

---

### Task 7: Perform foundation release-gate verification

**Files:**

- Modify only if verification finds a defect in files created by Tasks 1-6.

**Interfaces:**

- Consumes: The complete protocol foundation.
- Produces: Fresh verification evidence that the foundation is internally consistent and ready for the next implementation plan.

- [ ] **Step 1: Verify all tests from a clean invocation**

Run:

```text
python -m pytest -q
```

Expected: `35 passed` with zero failures and zero collection errors.

- [ ] **Step 2: Verify both CLI entry paths**

Run:

```text
solodeveling-validate tests/fixtures/valid-project
python -m solodeveling_protocol.cli tests/fixtures/valid-project
```

Expected: both invocations print `Protocol validation passed` and exit 0.

- [ ] **Step 3: Verify invalid completion remains rejected**

Run:

```text
python -m solodeveling_protocol.cli tests/fixtures/invalid-done-project
```

Expected: exits 1 and prints `[done-without-evidence]`.

- [ ] **Step 4: Verify packaging metadata and wheel contents**

Run:

```text
python -m pip wheel . --no-deps --wheel-dir dist
python -c "from importlib.resources import files; print(files('solodeveling_protocol').joinpath('schemas', 'work-item.schema.json').is_file())"
```

Expected: wheel build exits 0 and the resource check prints `True`.

- [ ] **Step 5: Verify repository hygiene**

Run:

```text
git diff --check
git status --short
```

Expected: `git diff --check` exits 0. `git status --short` shows only an untracked `dist/` directory if the ignore rule has not already hidden it; no source or test file remains uncommitted.

- [ ] **Step 6: Commit verification corrections only if required**

If Steps 1-5 required a correction, stage only the corrected foundation files and commit:

```text
git commit -m "fix: satisfy protocol foundation release gate"
```

If no correction was required, do not create an empty commit.

## Plan Self-Review Checklist

- Design coverage: this plan implements delivery sequence item 1 and deliberately defers items 2-8 to the named plan series.
- Portability: artifacts remain Markdown/YAML; Python is optional validation tooling.
- Single-agent operation: the plan requires inline execution and contains no subagent task.
- Type consistency: Tasks 2-6 use the same `ArtifactDocument`, `RoutingDecision`, `ValidationIssue`, `WorkLevel`, and `WorkStatus` names.
- Completion integrity: lifecycle and project validation both require evidence or accepted gaps; Critical completion also requires security and recovery consideration.
- Security: YAML uses `safe_load`, schemas reject undeclared properties, and validation does not execute artifact content.
- Scope: no runtime adapter, workflow skill suite, cloud service, or production deployment is introduced.
