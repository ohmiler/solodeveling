---
solodeveling_schema: 1
id: EVIDENCE-032
work_item: WORK-032
claim: Pilot-3 is invalid execution-sandbox evidence, and the successor harness now rejects a missing Windows sandbox helper before inference and stops after one zero-mutation execution.
method: Complete the exact authorized Pilot-3; validate and score only sanitized output; inspect the installed Codex binaries and bounded sandbox error lines; archive Pilot-3; add helper and mutation fail-closed gates; add regressions; preregister Pilot-4 without live execution; run offline verification.
command: python scripts/comparative_benchmark.py score benchmarks/results/solodeveling-superpowers-pilot-3.json; python -m pytest tests/test_comparative_benchmark.py -q; python -m pytest -q; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python -m compileall -q src scripts tests; python -m pip check; git diff --check
result: passed
scope: Sanitized Pilot-3 evidence, local sandbox capability diagnosis, pre-call helper gate, zero-mutation circuit breaker, successor preregistration, tests, docs, and memory.
limitations:
- Raw per-run prompts, JSONL, stderr, and temporary worktrees were intentionally not retained, so the sandbox helper diagnosis is strong corroborating evidence rather than verbatim proof for each run.
- Pilot-3 consumed 18 signed-in account calls and substantial token capacity without valid comparative evidence.
- Helper presence alone cannot prove all sandbox operations work; the zero-mutation circuit breaker provides a second boundary.
- Pilot-4 is not run and no pilot supports a public faster claim.
---

# Results

- Pilot-3 completed 18/18 processes with return code zero, nine per methodology.
  Visible baselines passed, hidden checks failed, and every worktree remained
  unchanged. Both methodologies scored 0/9 with zero correct pairs.
- Sanitized totals were 1,918,694 input tokens, 30,922 output tokens, and 149
  tool calls for Solodeveling; 1,903,215 input tokens, 24,112 output tokens, and
  110 tool calls for Superpowers.
- Failure-only medians were 121.41 and 94.32 seconds respectively. These are not
  correctness-gated speed evidence.
- `codex-windows-sandbox-setup.exe` is absent from PATH and the installed Codex
  binary directory. The local sandbox log repeatedly records helper launch
  failure with `program not found`.
- Pilot-4 probe and live execution now reject this state before a model call.
  Any zero-mutation execution that still occurs is checkpointed with
  `failure_code: zero-mutation`, stops the sequence, and cannot resume.
- Eighteen focused recovery tests and the complete 240-test suite pass. Protocol
  and skill validators, compilation, dependency health, package build, and diff
  checks pass. Pilot-4 remains not run.
