---
solodeveling_schema: 1
id: EVIDENCE-038
work_item: WORK-038
claim: The Solodeveling 0.2.0 versus no-skill harness and 30-call preregistration
  are offline-verified without making or authorizing a live comparative call.
method: Failing-first regressions, deterministic plan inspection, negative and positive
  hidden-check controls, exact detached-source verification, fail-closed runtime probe,
  documentation review, and full repository gates.
command: python -m pytest -q; validate_skill_suite.py; protocol CLI validation; comparative
  plan and verify-fixtures; exact verify_sources; comparative probe; git diff --check.
result: passed
scope: WORK-038 implementation and offline verification only.
limitations:
- No live model calls ran, so the pilot has no comparative outcome and supports no
  speed, quality, or superiority claim.
- The initial combined probe stopped before permission/model/source stages because
  the harness did not recognize the standalone resource layout. WORK-039 later
  repaired that false negative and completed the offline probe; the original failed
  attempt remains part of this evidence history.
- Deterministic response checks intentionally trade semantic breadth for auditable,
  offline scoring and may reject correct answers with substantially different wording.
---
# Evidence

## Current acceptance matrix

| Acceptance criterion | Method | Result |
| --- | --- | --- |
| Existing benchmark compatibility | Focused and full regression suites | Passed: 26 comparative tests and 273 total tests, including archived pilot protections |
| Explicit no-skill arm | Runner unit, plan inspection, and exact source verification | Passed: only the pinned skill arm requires a source, install, and invocation |
| Non-mutating response-aware tasks | Negative fixture baselines and positive response controls | Passed for Direct Read-Only and Critical readiness checks |
| Neutral 30-call preregistration | Static inspection, deterministic plan, and fixture verification | Passed: five tasks, two arms, three repetitions, and 30 counterbalanced runs |
| Fairness and claim-boundary documentation | English/Thai README and measurement documentation review | Passed; the unrun and pilot-only boundaries are explicit |
| Broad project gates | Tests, validators, source pin, probe, and diff integrity | Passed with the recorded local sandbox-helper limitation |

## Observation log

- The first focused run failed at import because `_build_task_prompt` and
  `_prepare_methodology` did not exist, demonstrating the planned regression boundary.
- The first repair exposed two compatibility failures: completeness validation was
  coupled to kind detection and rejected abbreviated archived specs. Separating live
  completeness validation restored the archive protections; 23 focused tests passed.
- The new preregistration initially failed because its file did not exist. After adding
  the spec and fixtures, all five visible baselines passed and all five empty-response
  hidden checks failed as intended. Positive controls passed for both response-aware
  checks; the final comparative suite passed 26 tests.
- Offline `plan` produced exactly 30 counterbalanced runs and disclosed the exact
  confirmation and account boundary. Offline `verify-fixtures` passed all five tasks.
- The first probe found a stale preregistered runtime pin (`0.144.5` versus installed
  `0.144.6`) before inference. The unrun spec was corrected and locked by regression.
- The second probe passed the exact runtime version then failed closed because the
  Windows sandbox helper is unavailable. No model call occurred. A separate
  `verify_sources` check passed for clean detached commit
  `ca7c3b356c2e9444963a52e00e2e97198ad94e7d`; both temporary worktrees were removed.
- Final verification: 273 tests passed in 18.94 seconds; the skill suite and protocol
  validators passed; `git diff --check` reported no whitespace errors.
