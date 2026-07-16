---
solodeveling_schema: 1
id: WORK-029
title: Controlled Solodeveling versus Superpowers Pilot Benchmark
status: done
level: standard
type: explore
goal: Build a reproducible, non-live-first benchmark that can measure whether Solodeveling reduces coding-workflow overhead relative to pinned Superpowers without trading away task correctness.
scope: A preregistered three-task pilot, exact methodology and runtime pins, fresh isolated worktrees, equal explicit invocation, deterministic run ordering, hidden outcome checks, sanitized metrics, dry-run planning, offline scoring, documentation, regression tests, and a separate authorization boundary before any model calls.
out_of_scope: Running live model calls in this source-change phase, comparing more than two methodologies, publishing a faster claim from the pilot alone, changing either methodology to improve benchmark performance, benchmarking different models or harnesses against each other, and measuring subjective writing style.
acceptance:
- The pilot declares one documentation task, one bug repair, and one medium feature with common prompts, seed repositories, visible tests, and hidden deterministic checks.
- Solodeveling v0.1.1 and Superpowers v6.1.1 are pinned to exact source commits and installed project-locally through equivalent benchmark adapters.
- "The plan contains 18 fresh runs: three tasks, two methodologies, and three repetitions in deterministic counterbalanced order."
- Preparation and dry-run modes perform no model call and expose the exact live command, model, timeout, mutation boundary, and expected maximum run count.
- Live execution requires an exact typed confirmation and refuses dirty or mismatched methodology sources.
- Results record correctness, wall time, token usage when available, tool activity, agent questions, changed files, workflow artifacts, runtime identity, and failure state without retaining raw prompts or logs in committed evidence.
- Offline scoring reports success before speed, uses paired descriptive statistics, and marks the pilot ineligible for a public faster claim.
- Fixture, plan, parser, safety, hidden-check, and scoring regressions pass with protocol and skill validation.
- The exact live command and cost boundary are presented for separate user authorization after protected-main delivery.
risks:
- Synthetic tasks may not represent real repositories or all development work.
- Runtime caching, service load, nondeterminism, and methodology order can distort timing.
- A workflow can appear faster by skipping required work, so correctness and hidden checks must gate speed analysis.
- Superpowers bootstrap or invocation differences could create an unfair comparison.
- Live runs consume model-service capacity or credits and require separate explicit authorization.
decisions:
- Compare one model and harness under identical settings; do not compare model intelligence.
- Pin the pilot runtime to Codex CLI 0.144.5, gpt-5.6, and medium reasoning; record the observed runtime identity in every result and fail closed on a mismatch.
- Pin Solodeveling v0.1.1 at 889e07a47a8cbdca15765d00348dbbd7f9849f03 and Superpowers v6.1.1 at d884ae04edebef577e82ff7c4e143debd0bbec99.
- Install both skill suites project-locally and invoke their root workflow explicitly in the otherwise identical prompt.
- Start with an 18-run pilot. Treat its output as a signal for confirmatory design, never as sufficient evidence for a public superiority claim.
- Exclude common fixture, source preparation, and methodology installation time from task wall time while retaining their exact provenance.
verification:
- Validate the preregistration and exact 18-run deterministic plan.
- Run fixture baselines and prove hidden checks reject planted incomplete outcomes.
- Test JSONL usage parsing, failure classification, sanitization, and paired scoring offline.
- Run the full Python suite, protocol validation, canonical skill validation, compileall, dependency health, and diff checks.
next_action: Request separate owner authorization before running the exact 18-call pilot command printed by the verified offline probe.
evidence:
- EVIDENCE-029
---

# Authorization boundary

This work may design, implement, test, and merge the benchmark harness without
calling a model. It does not authorize any of the 18 live Codex runs. Live execution
requires a later approval naming the benchmark version, model, runtime command, run
count, timeout, methodology pins, and any known cost or account boundary.

# Verification

- The deterministic plan contains exactly 18 runs and counterbalances which
  methodology starts each paired block by 5 to 4.
- All three seed projects pass their visible baseline tests and fail their external
  hidden completion checks before an agent changes them.
- Offline probe verified Codex CLI 0.144.5, both clean exact source commits, both
  root skills, the no-network sandbox declaration, and the fully resolved command.
- Nine benchmark regressions and the complete 231-test Python suite pass.
- Protocol validation, canonical skill validation, compileall, pip check, diff
  check, and final wheel/source-distribution builds pass.
- No model call or comparative result was produced. The pilot remains permanently
  ineligible for a public faster claim.
