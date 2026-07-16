---
solodeveling_schema: 1
id: EVIDENCE-029
work_item: WORK-029
claim: A reproducible, correctness-gated, non-live-first Solodeveling-versus-Superpowers pilot harness is ready for a separately authorized 18-run execution, but no comparative speed result or public faster claim exists yet.
method: Preregister three task classes and exact runtime/methodology pins; generate a deterministic counterbalanced plan; isolate every attempt in a fresh linked worktree; keep hidden checks outside agent-visible fixtures; parse sanitized Codex activity and usage; gate timing on visible and hidden correctness; add exact confirmation, clean-source/runtime probes, atomic checkpoints, resume validation, and a permanent pilot-only claim boundary.
command: python scripts/comparative_benchmark.py plan; python scripts/comparative_benchmark.py verify-fixtures; python scripts/comparative_benchmark.py probe with exact temporary source checkouts; python -m pytest -q; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python -m compileall -q src scripts tests; python -m pip check; python -m build to a new temporary output directory; git diff --check
result: passed
scope: Offline benchmark design and harness only, covering Solodeveling 0.1.1 at 889e07a47a8cbdca15765d00348dbbd7f9849f03, Superpowers 6.1.1 at d884ae04edebef577e82ff7c4e143debd0bbec99, Codex CLI 0.144.5, gpt-5.6 with medium reasoning, three deterministic fixtures, 18 planned runs, sanitized metrics, hidden correctness checks, offline scoring, and live authorization controls.
limitations:
- At harness delivery no live call had occurred. A later authorized pilot-1 execution made 18 process attempts, but all failed before inference with zero observed tokens and tool calls; it provides no evidence that either methodology is faster.
- The pilot has only three synthetic tasks and three repetitions; regardless of outcome it is signal for confirmatory design, not sufficient evidence for a public superiority claim.
- Service load, caching, model nondeterminism, account capacity, and synthetic fixture representativeness can affect observed time and token use.
- The CLI cannot provide a stable dollar maximum for signed-in ChatGPT capacity or credits; the disclosed boundary is 18 calls with a 1,200-second timeout each.
- The runtime pin will fail closed if Codex CLI changes before authorization; changing the pin would require reviewing and updating the preregistration rather than silently accepting drift.
---

# Results

- The fixed-seed plan contains three documentation, three bug-repair, and three
  medium-feature pairs, one run per methodology in each pair, for exactly 18 runs.
  Starting order is alternated and balanced 5 to 4.
- Each seed passes its visible unittest baseline and is rejected by the external
  hidden checker until the required outcome exists. Speed statistics include only
  pairs where both methodologies pass both correctness layers.
- Offline probe verified the exact clean source commits and root skills
  `solodeveling` and `using-superpowers`, plus Codex CLI 0.144.5. It printed the
  resolved command without invoking Codex exec.
- Live execution requires the exact phrase `RUN CONTROLLED PILOT 18`, refuses
  source or runtime drift, disables network access, pins `gpt-5.6` with medium
  reasoning, and mutates only temporary linked worktrees.
- Sanitized results record elapsed time, correctness, visible/hidden outcomes,
  token usage when emitted, tool calls, agent questions, human interventions,
  changed files, workflow artifacts, runtime identity, and failure state.
- Atomic checkpoints preserve attempted run IDs. Resume refuses a different
  preregistration hash, provenance, run identity, duplicate ID, or unknown ID, so
  an interruption does not silently repeat completed calls.
- Nine focused benchmark tests and the complete 231-test suite pass. Protocol and
  canonical skill validation, compilation, dependency health, diff checks, and
  final wheel/source-distribution builds also pass.
- README describes the prepared pilot and explicitly says it has not been run.
  Release 0.1.1 artifacts, tags, registries, and immutable release bytes were not
  changed.

# Subsequent invalid execution

Pilot-1 later attempted all 18 planned processes using the preregistered
`gpt-5.6` alias. Every process returned a runtime failure in 2.1-3.4 seconds with
no token usage, no tool activity, no correct run, and no correct pair. The alias
was absent from the fresh local Codex model catalog. EVIDENCE-030 records the
recovery and successor preregistration. Pilot-1 is invalid runtime evidence, not a
comparative result.
