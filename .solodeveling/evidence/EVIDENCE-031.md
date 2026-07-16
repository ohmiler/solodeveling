---
solodeveling_schema: 1
id: EVIDENCE-031
work_item: WORK-031
claim: Pilot-2 is invalid methodology-activation evidence, and the successor harness now installs and verifies project-local workflow skills at Codex's canonical adapter path before timing.
method: Complete the exact authorized 18-run pilot-2; validate and score only its sanitized result; compare the shared zero-change outcome with the repository's Codex adapter contract; archive pilot-2; align installation and activation preflight; add regressions; preregister pilot-3 without live execution; run complete offline verification.
command: python scripts/comparative_benchmark.py score benchmarks/results/solodeveling-superpowers-pilot-2.json; python -m pytest tests/test_comparative_benchmark.py -q; python -m pytest -q; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python -m compileall -q src scripts tests; python -m pip check; git diff --check
result: passed
scope: Sanitized pilot-2 evidence, root-cause classification, Codex project skill path, activation preflight, successor preregistration, tests, documentation, and project memory.
limitations:
- Raw Codex JSONL, prompts, and temporary worktrees were intentionally not retained; causal diagnosis relies on the uniform zero-change result and the directly observable adapter-path mismatch.
- Pilot-2 consumed 18 signed-in account calls and substantial token capacity even though it produced no valid comparative evidence.
- Pilot-3 has not been run and requires fresh explicit authorization.
- No pilot result may support a public faster claim; confirmatory evidence remains required after any valid pilot.
---

# Results

Local verification passed; protected-main delivery remains pending.

- Pilot-2 completed 18/18 processes with exit code zero: nine Solodeveling and
  nine Superpowers runs. All visible baselines passed; every hidden check failed.
- Both methodologies scored 0/9 correct, with zero correct pairs, zero changed
  files, and no correctness-gated timing median.
- Descriptive failure-only medians were 108.38 seconds for Solodeveling and
  125.99 seconds for Superpowers. These values are not valid speed evidence.
- Sanitized usage totaled 1,902,441 input and 28,324 output tokens with 141 tool
  calls for Solodeveling, and 2,219,134 input and 29,672 output tokens with 139
  tool calls for Superpowers.
- The runner installed both skill suites under `.codex/skills`, while the
  product's Codex adapter contract is `.agents/skills`. The exact shared defect
  explains why neither named methodology was available in its worktree.
- The corrected runner copies to `.agents/skills` and verifies the named root
  `SKILL.md` before repository initialization and timing. A regression rejects
  the old path.
- Pilot-2 is archived with `invalid-methodology-activation` status and the
  live-ready gate rejects it. Pilot-3 preserves the fixed plan and is not run.
- Fifteen focused tests and the complete 237-test suite pass. Protocol and skill
  validation, compilation, dependency health, result-schema validation, and
  diff checks pass locally.
