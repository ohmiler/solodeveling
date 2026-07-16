---
solodeveling_schema: 1
id: EVIDENCE-027
work_item: WORK-027
claim: The public README now explains Solodeveling's single-agent-first value, live installation, workflow-overhead model, intended users, and documented contrasts with adjacent frameworks without claiming unmeasured cross-framework superiority.
method: Review current project evidence and official adjacent-project documentation; rewrite the public README and linked installation status; add stale-claim and positioning regressions; run focused and complete local gates; and verify full protected-main pull-request and post-merge CI matrices.
command: python -m pytest -q tests/test_installation_docs.py; python -m pytest -q; npm test --prefix packages/npm; python scripts/validate_skill_suite.py; official quick_validate.py for all ten skills; python -m solodeveling_protocol.cli .; python -m compileall -q src tests scripts; python -m pip check; parse workflow YAML; git diff --check; GitHub runs 29496447066 and 29496613211
result: passed
scope: Root README positioning, live npm/PyPI/GitHub installation links, risk-level explanation, four-project comparison table, speed-evidence boundary, best-fit guidance, linked installation publication status, regression coverage, and unchanged release boundary.
limitations:
- No controlled cross-framework completion-time, token, question-count, correctness, or repair benchmark was run; the README explicitly rejects conclusions that would require one.
- Superpowers, GSD, GitHub Spec Kit, and BMAD Method descriptions reflect their official public documentation observed in July 2026 and may change independently.
- Codex and Claude Code still have only one bounded representative live scenario each; Cursor remains structurally verified only and Tier 1 remains unverified.
---

# Results

- README now leads with one agent and right-sized process, links the live 0.1.0 npm,
  PyPI, and immutable GitHub Release channels, and removes the obsolete unpublished
  instructions.
- Quick, Standard, and Critical behavior is summarized in one compact table. A
  separate four-column comparison covers Solodeveling, Superpowers, GSD, GitHub Spec
  Kit, and BMAD Method by documented default, strongest fit, and main contrast.
- The speed section defines the supported claim as reduced workflow overhead. It
  cites zero-question ephemeral dogfood, focused memory/docs CI durations, and the
  bounded cross-runtime scenario while explicitly deferring competitive conclusions.
- Best-fit guidance identifies solo maintenance, one-primary-agent work, mixed task
  sizes, lifecycle ownership, and runtime portability; it also states when another
  approach may fit better.
- Linked installation guidance now records the published 0.1.0 registries, immutable
  release, verified bytes, and staged future npm publication. Regression tests fail
  on stale unpublished wording or removal of positioning and evidence boundaries.
- Final local verification passed 220 Python tests; npm passed 8 tests with one local
  Windows symlink skip; all ten canonical and official skill validations, protocol
  validation, compilation, dependency health, workflow YAML parsing, and diff checks
  passed.
- Pull-request full run 29496447066 and post-merge main full run 29496613211 passed
  Python 3.10/3.14 across Windows, Ubuntu, and macOS; package verification; six native
  builds and smokes; and npm pack/npx smoke.
- No skill behavior, package version, registry object, tag, release asset, or
  candidate content changed. `v0.1.0^{}` remains
  `700a9b9dafc877507232b84a94ff3d6eaf7afda4`.
