from __future__ import annotations

import re

from solodeveling_protocol.models import SecurityProfile


PROFILE_TRIGGERS: tuple[tuple[SecurityProfile, re.Pattern[str]], ...] = (
    (
        SecurityProfile.WEB_APPLICATION,
        re.compile(r"\b(web(?:site|app)?|https?|browser|public api|api endpoint)\b", re.IGNORECASE),
    ),
    (
        SecurityProfile.MOBILE,
        re.compile(r"\b(android|ios|mobile app|react native|flutter)\b", re.IGNORECASE),
    ),
    (
        SecurityProfile.IDENTITY_ACCESS,
        re.compile(
            r"\b(auth(?:entication|orization)?|login|logout|session|permission|access control|rbac|oauth|oidc|sso)\b",
            re.IGNORECASE,
        ),
    ),
    (
        SecurityProfile.SENSITIVE_DATA,
        re.compile(
            r"\b(sensitive data|personal data|customer data|health data|pii|phi|privacy)\b",
            re.IGNORECASE,
        ),
    ),
    (
        SecurityProfile.DATA_MIGRATION,
        re.compile(
            r"\b(database|schema|data) (?:migration|backfill)|\b(drop table|delete data|destructive migration)\b",
            re.IGNORECASE,
        ),
    ),
    (
        SecurityProfile.SUPPLY_CHAIN,
        re.compile(
            r"\b(package|dependency|dependencies|build pipeline|artifact provenance|sbom|software bill of materials|code signing)\b",
            re.IGNORECASE,
        ),
    ),
    (
        SecurityProfile.INFRASTRUCTURE,
        re.compile(
            r"\b(cloud|infrastructure|terraform|kubernetes|container|docker|iam|firewall|serverless)\b",
            re.IGNORECASE,
        ),
    ),
    (
        SecurityProfile.AI_AGENTIC,
        re.compile(
            r"\b(ai|llm|rag|model|prompt|agentic|ai agent|tool access|tool calling)\b",
            re.IGNORECASE,
        ),
    ),
    (
        SecurityProfile.PAYMENTS,
        re.compile(
            r"\b(payment|billing|checkout|card data|transaction settlement)\b",
            re.IGNORECASE,
        ),
    ),
)


def classify_security_profiles(summary: str) -> tuple[SecurityProfile, ...]:
    """Return every security profile activated by observable text triggers."""
    return tuple(profile for profile, pattern in PROFILE_TRIGGERS if pattern.search(summary))