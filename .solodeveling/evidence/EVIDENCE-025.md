---
solodeveling_schema: 1
id: EVIDENCE-025
work_item: WORK-025
claim: Changes strictly under docs/** use one verified Ubuntu docs job while memory, mixed, product, workflow, package, tag, malformed, and root-document paths retain their intended fail-safe routing.
method: Failing-first classifier and workflow regressions, full local gate, full GitHub implementation PR and main runs, and docs-only dogfood PR and main runs with job-level routing inspection.
command: python -m pytest -q; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python -m compileall -q src tests scripts; python -m pip check; parse ci.yml with PyYAML; git diff --check; GitHub runs 29492218994, 29492404797, 29492612885, and 29492666899
result: passed
scope: WORK-025 classifier outputs, CI job conditions, exact diff checking, complete Python regression coverage, fail-safe exclusions, and one docs-only documentation change.
limitations:
- No new tag was created; v* full-gate preservation is covered by workflow policy regression and unchanged trigger configuration rather than a fresh tag run.
- README, mixed, malformed, and other negative cases are automated classifier regressions rather than separate live pull requests.
---

# Results

- The local gate passed 219 tests plus skill validation, protocol validation, source
  compilation, dependency health, CI YAML parsing, classifier smoke cases, and diff
  checks.
- Implementation PR run 29492218994 and main run 29492404797 selected the full gate;
  memory-only and docs-only were skipped while all broad jobs passed.
- Dogfood PR run 29492612885 selected `changes` in 4 seconds and `docs-only` in
  23 seconds. Memory, test matrix, package, native, and npm jobs were skipped.
- Dogfood main run 29492666899 selected `changes` in 5 seconds and `docs-only` in
  33 seconds. The exact range diff check and complete 219-test Python suite passed;
  all broad jobs were skipped.
- The dogfood change touched only `docs/protocol-contract.md`, asked zero user
  questions, and created no Quick-task project-memory artifacts.
- `v0.1.0^{}` remains candidate commit
  `700a9b9dafc877507232b84a94ff3d6eaf7afda4`. No release, registry, npm, tag,
  schema, branch-protection, or publication action was performed.
