from __future__ import annotations

import re

from solodeveling_protocol.models import RoutingDecision, WorkLevel


CRITICAL_TRIGGERS: dict[str, re.Pattern[str]] = {
    "identity-access": re.compile(
        r"\b(password|credential|account recovery|login (?:authentication|flow)|"
        r"session (?:creation|rotation|revocation|handling|lifecycle)|"
        r"(?:role|permission|ownership|authorization|access) "
        r"(?:check|checks|decision|policy|enforcement)|privilege escalation)\b",
        re.IGNORECASE,
    ),
    "payments": re.compile(
        r"\b(payment fulfillment|billing authorization|financial effect|"
        r"transaction settlement|webhook (?:signature|fulfillment)|charge|refund|"
        r"payout|money movement)\b",
        re.IGNORECASE,
    ),
    "sensitive-data": re.compile(
        r"\b(?:migrate|expose|export|transform|delete|encrypt|redact|retain)\w* "
        r"(?:sensitive(?: customer)?|personal|private|customer|health) data\b|"
        r"\bsensitive-data exposure\b",
        re.IGNORECASE,
    ),
    "destructive-migration": re.compile(
        r"\b(destructive|drop table|delete data|irreversible|data transformation|"
        r"backfill|non-null constraint)\b",
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
