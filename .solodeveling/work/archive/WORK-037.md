---
solodeveling_schema: 1
id: WORK-037
title: Measure feedback-driven workflow improvement
status: done
level: standard
type: change
goal: Make Solodeveling improvement claims testable by comparing 0.1.1 with 0.1.2
  on feedback-sensitive tasks and collecting bounded field evidence.
scope: Generalized paired benchmark planning and scoring, five deterministic fixtures,
  exact 0.1.1 and 0.1.2 pins, a non-live 30-run preregistration, local field scorecard
  validation and summaries, documentation, tests, and offline probes.
out_of_scope: Live model calls, Pilot-4 execution, public faster claims, telemetry,
  external data upload, changing published releases, and repairing the external Codex
  Windows sandbox installation.
acceptance:
- One preregistered study compares exact Solodeveling 0.1.1 and 0.1.2 sources on five
  feedback-sensitive tasks with three paired repetitions and a 30-call maximum.
- Correctness gates every efficiency comparison; summaries include time, tokens, tool
  calls, questions, changed files, and workflow artifacts.
- Fixture checks detect Quick zero-artifact behavior, same-boundary follow-up reuse,
  ordinary correctness, and no hidden baseline success.
- A local-only field scorecard validates and summarizes the next 20 real tasks without
  collecting project names, prompts, source, secrets, or raw model output.
- Existing Pilot-4 behavior, archived results, fail-closed sandbox checks, and public-claim
  prohibition remain intact.
- Focused and full regressions, fixture verification, source probes, protocol validation,
  and diff checks pass without a live call.
risks:
- A synthetic task set may reward benchmark-specific behavior and fail to represent
  real projects.
- Generalizing the harness could weaken the exact source or live-authorization boundary.
- Small samples and nondeterministic model behavior can produce misleading timing
  differences.
decisions:
- Compare 0.1.1 directly with 0.1.2 before interpreting any cross-framework result.
- Use five task families and three repetitions as pilot signal only; require later
  confirmatory evidence for public claims.
- Keep observations local and sanitized; record user annoyance only when voluntarily
  supplied.
- Do not run live while the Windows sandbox helper preflight fails.
verification:
- Add failing-focused tests before implementation and preserve all Pilot-4 regressions.
- Verify each fixture passes visible tests and fails its hidden completion check at
  baseline.
- Probe exact detached source checkouts and confirm the sandbox failure occurs before
  any model call.
next_action: None; archived.
evidence:
- EVIDENCE-037
---
# Plan

1. Generalize planning, source mapping, and paired overhead scoring without changing
   the existing Pilot-4 specification.
2. Add five feedback-sensitive tasks and preregister exact 0.1.1 versus 0.1.2 inputs.
3. Add a privacy-preserving local field scorecard for 20 real tasks.
4. Run only offline validation and probes in this work; live calls require a repaired
   sandbox and the exact confirmation printed by the finished plan.
