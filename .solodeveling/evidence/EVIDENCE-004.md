---
solodeveling_schema: 1
id: EVIDENCE-004
work_item: WORK-004
claim: Solodeveling provides portable, single-agent release and maintenance workflows that bind readiness, migrations, recovery, dependency and vulnerability triage, incidents, and operational work to authority and recent evidence.
method: Focused and full automated tests, adversarial skill scenarios, official skill validation, protocol and Critical metadata validation, fresh package build and inspection, compilation, dependency checks, and diff inspection.
command: python -m pytest -q; python scripts/validate_skill_suite.py .; quick_validate.py for all ten skills; solodeveling protocol validation; inspect Critical security and recovery fields; python -m pip wheel . --no-deps; inspect fresh wheel; compileall; pip check; git diff --check
result: passed
scope: Releasing and maintaining skills, five progressive release references, two progressive maintenance references, router vocabulary, scenario discovery, nine adversarial release and maintenance scenarios, and WORK-004 lifecycle evidence on feat/release-maintenance-workflows.
limitations:
- No real deployment, migration, rollback, dependency upgrade, vulnerability response, production access, incident containment, credential access, or external-system mutation was performed.
- Scenario validation proves required portable protocol content is present; live behavioral comparison on Codex, Claude Code, Cursor, and other agents remains deferred to the adapter evaluation increment.
- SLSA, CISA KEV, OSV, and NIST incident-response status was checked on 2026-07-15 and living or current requirements must be refreshed when applied.
- The local environment lacked the optional python-build frontend; a fresh isolated wheel was built with pip instead and inspected at C:/tmp/solodeveling-work004.
---
# Verification summary

On 2026-07-15, 73 tests passed. The suite validator and all ten official skill
validations passed. Protocol and Critical metadata validation, compilation,
dependency health, and diff checks passed. A fresh wheel was built and inspected;
its SHA-256 was e7d6636471985aee4923c6a3707990898a799a503eab3eb2dfb3ecf544f6b71f.
