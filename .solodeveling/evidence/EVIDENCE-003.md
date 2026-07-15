---
solodeveling_schema: 1
id: EVIDENCE-003
work_item: WORK-003
claim: Solodeveling provides a version-aware Secure SDLC baseline with deterministic attack-surface routing, strict finding semantics, non-echoing project-memory secret detection, and bounded security verification guidance.
method: Unit and integration tests, adversarial skill scenarios, official skill validation, protocol and secret validation, Critical metadata inspection, package inspection, compilation, dependency checks, and clean-tree verification.
command: python -m pytest -q; python scripts/validate_skill_suite.py .; quick_validate.py for all eight skills; solodeveling protocol validation; inspect Critical security and recovery fields; build and inspect wheel; compileall; pip check
result: passed
scope: Security profile routing, security finding schema, project-memory high-confidence secret patterns, securing skill and references, router integration, and execution checkpoint hardening on feat/secure-sdlc-baseline.
limitations:
- Secret detection intentionally covers selected high-confidence formats in `.solodeveling` memory; it is not a repository-wide secret scanner and absence of findings is not proof of absence.
- Standards status was checked on 2026-07-15 and must be refreshed when exact current controls affect a decision.
- Live comparative behavior on Codex, Claude Code, and Cursor remains deferred to the adapter evaluation increment.
- No intrusive scan, penetration test, production change, credential access, or compliance certification was performed.
---
# Verification summary

On 2026-07-15, 72 tests passed. The suite validator and all eight official skill
validations passed. Critical security and recovery fields were present. Project
memory contained no reported secret-like material or invalid finding. The built
wheel contained security routing, non-echoing secret detection, and finding schema
resources. Compilation, dependency health, diff, and clean-tree checks passed.