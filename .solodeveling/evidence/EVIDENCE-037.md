---
solodeveling_schema: 1
id: EVIDENCE-037
work_item: WORK-037
claim: The feedback measurement system is offline-verified, exact-source-bound, correctness-gated,
  packaged, and collecting sanitized field evidence without a comparative outcome
  claim.
method: Failing-first regressions; deterministic plan and hidden fixture checks; exact
  detached source identity checks; fail-closed non-live probe; full Python and Node
  gates; packaged-wheel smoke; local scorecard validation.
command: pytest 259; npm test; validate_skill_suite.py; protocol validate; compileall;
  pip check; build and installed-wheel smoke; comparative plan/verify-fixtures/probe;
  field_scorecard validate/summary.
result: passed
scope: Generic paired benchmark harness, five-task 0.1.1-versus-0.1.2 preregistration,
  30-call authorization boundary, overhead scoring, field scorecard schema/CLI/docs,
  and first sanitized local observation.
limitations:
- Feedback pilot 1 used one model call, produced a zero-mutation failure, and stopped
  before run 2; it is invalid and provides no 0.1.1-versus-0.1.2 comparison.
- Feedback pilot 2 used one model call and proved that the legacy workspace-write
  flag was forced read-only by the active permission-profile runtime; it is invalid.
- The Windows sandbox is repaired and successor pilot 3 passes an explicit no-model
  `:workspace` write probe, but requires a new exact authorization before execution.
- Field collection is 1 of 20 observations; elapsed time, tokens, resume accuracy,
  ceremony fit, and user annoyance remain unavailable rather than zero.
---
# Evidence

Verified observations are recorded below.

## The feedback measurement system is offline-verified, exact-source-bound, correctness-gated, packaged, and collecting sanitized field evidence without a comparative outcome claim.

- Method: Failing-first regressions; deterministic plan and hidden fixture checks; exact detached source identity checks; fail-closed non-live probe; full Python and Node gates; packaged-wheel smoke; local scorecard validation.
- Result: passed
- Scope: Generic paired benchmark harness, five-task 0.1.1-versus-0.1.2 preregistration, 30-call authorization boundary, overhead scoring, field scorecard schema/CLI/docs, and first sanitized local observation.
- Command: pytest 259; npm test; validate_skill_suite.py; protocol validate; compileall; pip check; build and installed-wheel smoke; comparative plan/verify-fixtures/probe; field_scorecard validate/summary.
- Limitations:
  - Feedback pilot 1 used one model call, produced a zero-mutation failure, and stopped before run 2; it is invalid and provides no 0.1.1-versus-0.1.2 comparison.
  - Feedback pilot 2 used one model call and proved that the legacy workspace-write flag was forced read-only by the active permission-profile runtime; it is invalid.
  - The Windows sandbox is repaired and successor pilot 3 passes an explicit no-model `:workspace` write probe, but requires a new exact authorization before execution.
  - Field collection is 1 of 20 observations; elapsed time, tokens, resume accuracy, ceremony fit, and user annoyance remain unavailable rather than zero.
