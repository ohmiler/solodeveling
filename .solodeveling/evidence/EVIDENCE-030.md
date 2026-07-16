---
solodeveling_schema: 1
id: EVIDENCE-030
work_item: WORK-030
claim: Pilot-1 is preserved as invalid runtime evidence, and successor pilot-2 now fails closed on exact Codex model and reasoning availability before any live call.
method: Inspect only sanitized pilot-1 metrics, Codex login status, executable help/version, current configuration, and local model catalog; archive the original preregistration; create a distinct successor benchmark; validate exact model/reasoning availability before source preparation or execution; reduce runtime output to fixed failure codes; exclude Python caches from mutation metrics; reject non-live-ready benchmark statuses; add regressions and complete non-live verification.
command: python scripts/comparative_benchmark.py plan; python scripts/comparative_benchmark.py probe with exact source checkouts; python -m pytest -q; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python -m compileall -q src scripts tests; python -m pip check; python -m build to a new temporary directory; git diff --check
result: passed
scope: Recovery from pilot-1 runtime failure, archived invalid preregistration, pilot-2 exact gpt-5.6-sol medium pin, model-catalog preflight, live status gate, bounded diagnostics, Python cache filtering, documentation, memory, packaging, and tests.
limitations:
- The pilot-1 runner did not retain sanitized failure codes, so the exact upstream error text is unavailable; the absent gpt-5.6 catalog slug, zero tokens, zero tool calls, uniform short failures, and working login establish a pre-inference runtime failure but not the service's verbatim reason.
- Pilot-1 made 18 process attempts. No token usage was emitted, but account-side request accounting is not exposed by the CLI and cannot be proven to be zero.
- Pilot-2 has not been run and still requires fresh authorization because gpt-5.6-sol is a materially different exact model identifier and the preregistration hash changed.
- The shared model cache may be written by adjacent Codex client versions; the executable version is authoritative while cache path, fetch time, writer version, exact slug, and reasoning support are recorded.
- No pilot outcome may support a public faster claim; confirmatory evidence remains required.
---

# Results

- Pilot-1 attempted nine Solodeveling and nine Superpowers processes. All 18 were
  `runtime-failure`, lasted 2.1-3.4 seconds, emitted no tokens or tool calls,
  preserved passing visible baselines, failed hidden checks, and yielded zero
  correct pairs. Neither methodology received an executable task opportunity.
- Codex login status was valid. Executable version remained `codex-cli 0.144.5`.
  The fresh local catalog contained `gpt-5.6-sol`, `gpt-5.6-terra`, and
  `gpt-5.6-luna`, but not pilot-1's `gpt-5.6` alias. Current config selected
  `gpt-5.6-sol` with medium reasoning.
- The original specification is archived with `invalid-runtime` status and the
  live gate rejects it. Its ignored sanitized checkpoint is not overwritten or
  interpreted as a benchmark result.
- Pilot-2 keeps the same 18-run order, task fixtures, source commits, isolation,
  timeout, correctness gates, checkpoint semantics, and permanent pilot-only
  claim policy. Only the exact model slug, benchmark identity, confirmation, hash,
  and result path change.
- Corrected offline probe verified `gpt-5.6-sol` and medium reasoning in the
  catalog before source/runtime execution. It also verified clean exact
  Solodeveling and Superpowers checkouts and printed the distinct pilot-2 command.
- Future nonzero exits record only a fixed diagnostic code and return code, never
  raw stderr, stdout, prompt, or session logs. Python bytecode caches are excluded
  from the environment and change metric.
- A pre-inference runtime failure now triggers a circuit breaker after one attempt;
  the checkpoint cannot resume under the same preregistration.
- Fourteen focused tests and the complete 236-test suite pass. Protocol/skill
  validators, compilation, dependency health, diff checks, and wheel/sdist build
  also pass. No model call occurred during recovery, and pilot-2 has no result.
