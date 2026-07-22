---
solodeveling_schema: 1
id: EVIDENCE-043
work_item: WORK-043
claim: The 0.3.0 routing pilot is deterministically preregistered and passed local
  corpus, schema, harness, executable-availability, dry-run, memory, and diff checks;
  live routing evidence remains unverified.
method: Load and schema-check exactly three scenarios, exercise the evaluation unit
  tests, probe Codex without a model call, preview the read-only execution plan, and
  attempt the authorized live command through the policy gate.
command: python -m pytest -q tests/test_evaluation.py tests/test_evaluation_cli.py
  tests/test_evaluation_runner.py; python -m solodeveling_protocol.main_cli eval probe
  --runtime codex; python -m solodeveling_protocol.main_cli eval run --runtime codex
  --smoke --scenarios evals/release-pilots/0.3.0 --source skills --dry-run; python -m
  solodeveling_protocol.cli .; git diff --check.
result: unverified
scope: Release 0.3.0 routing-pilot preregistration and offline preflight only.
limitations:
- The owner supplied informed approval, but tenant policy still forbids sending
  private-workspace skill and scenario text externally from this environment.
- No live-pass, runtime semantic result, fixture integrity result, version bump, or
  candidate evidence exists yet.
---
# Evidence

| AC | Result | Evidence | Limitation |
| --- | --- | --- | --- |
| AC1 | Passed | Three versioned scenarios; deterministic route expectations; 35 evaluation tests | Scenarios are self-authored |
| AC2 | Unverified | Codex CLI 0.145.0 available; exactly three read-only calls in dry-run; owner gave informed approval | Tenant policy still stopped the command before any call |
| AC3 | Not started | Version remains 0.2.0 by gate design | Requires AC2 |
| AC4 | Not started | Prior source revision passed 280 tests | Exact 0.3.0 candidate does not exist |
| AC5 | In progress | WORK boundary excludes all external release actions | Candidate identity is not available |

## Observation log

- A second live invocation after exact informed approval was denied by tenant policy.
  The policy explicitly forbids this external transmission from the current
  environment even with user approval. No runtime output or result file was created.
