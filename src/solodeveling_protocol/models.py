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

class SecurityProfile(str, Enum):
    WEB_APPLICATION = "web-application"
    MOBILE = "mobile"
    IDENTITY_ACCESS = "identity-access"
    SENSITIVE_DATA = "sensitive-data"
    DATA_MIGRATION = "data-migration"
    SUPPLY_CHAIN = "supply-chain"
    INFRASTRUCTURE = "infrastructure"
    AI_AGENTIC = "ai-agentic"
    PAYMENTS = "payments"


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
