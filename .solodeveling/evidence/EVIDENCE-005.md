---
solodeveling_schema: 1
id: EVIDENCE-005
work_item: WORK-005
claim: Solodeveling can safely materialize one byte-identical canonical skill suite into native Codex, Claude Code, Cursor, and generic Agent Skills paths, detect drift, and remove only unchanged managed files.
method: Focused safety and conformance tests, full automated regression, canonical byte comparison across four adapter mappings, CLI tests, official skill validation, protocol and Critical metadata validation, fresh package build and entry-point inspection, compilation, dependency checks, and diff inspection.
command: python -m pytest -q; python scripts/validate_skill_suite.py .; quick_validate.py for all ten skills; solodeveling protocol validation; inspect Critical security and recovery fields; python -m pip wheel . --no-deps; inspect fresh wheel and entry_points.txt; compileall; pip check; git diff --check
result: passed
scope: Runtime mapping, managed SHA-256 manifest, source validation, containment and symlink preflight, unmanaged collision refusal, atomic copy, managed update, drift check, dry-run, rollback, safe uninstall, packaged CLI, documentation, and canonical byte conformance on feat/runtime-adapters.
limitations:
- No live Codex, Claude Code, or Cursor behavioral scenario was executed; structural conformance does not establish Tier 1 behavioral support.
- Codex and Claude executables were available, but cursor-agent was unavailable; live and cross-session evaluation is deferred to WORK-006.
- Co-installing several native adapter roots may surface duplicate skills in runtimes that scan compatibility paths; that UX remains unverified.
- Hash equality detects changes but does not establish publisher authenticity, trust, or behavioral safety.
- No global skill installation, real user project installation, runtime setting change, marketplace publication, or remote action was performed.
---
# Verification summary

On 2026-07-15, 94 tests passed. The suite validator and all ten official skill
validations passed. Protocol and Critical metadata validation, compilation,
dependency health, and diff checks passed. A fresh wheel contained adapter_cli.py,
adapters.py, and the solodeveling-adapt entry point; its SHA-256 was
89be2acc2f84a62ca013922775fdad97d4ae4037f07e09d3cdcc960b7d8f39d9.
