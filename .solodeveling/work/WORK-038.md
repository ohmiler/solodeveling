---
solodeveling_schema: 1
id: WORK-038
title: Benchmark Solodeveling 0.2.0 against a no-skill baseline
status: done
level: standard
type: change
goal: Make the value of Solodeveling 0.2.0 testable against an otherwise identical
  Codex run with no installed methodology skill.
scope: Extend the paired benchmark harness with an explicit no-skill methodology,
  optional mutation requirements, response-aware hidden checks, a neutral five-task
  30-call preregistration, safe fixtures, documentation, and offline validation.
out_of_scope: Live model calls, public superiority or speed claims, external telemetry,
  changing published 0.2.0 artifacts, production actions, and comparing other frameworks.
acceptance:
- Existing skill-versus-skill benchmark specs and archived-result protections remain
  compatible.
- A no-skill methodology requires no source checkout, installs no project skill, and
  receives no skill invocation while the Solodeveling arm remains pinned to v0.2.0.
- Tasks may explicitly allow zero mutations without triggering the mutation-required
  circuit breaker, and hidden checks may inspect a local final-message file.
- One neutral preregistered pilot covers Direct Read-Only, Quick, Standard repair,
  bounded continuation, and Critical readiness with three paired repetitions and a
  maximum of 30 live calls.
- Fixture baselines pass visible tests and fail hidden completion checks; no fixture
  contains repository-level instructions that activate Solodeveling for the baseline.
- Documentation explains fairness, interpretation, exact authorization, and the boundary
  between internal pilot signal and public claims.
- Focused tests, fixture verification, plan generation, source/runtime probe where
  available, full regressions, skill validation, protocol validation, and diff checks
  pass without making a live model call.
risks:
- Synthetic fixtures may reward benchmark-specific behavior and not generalize to
  real repositories.
- An accidental skill, AGENTS.md, or prompt instruction could contaminate the no-skill
  baseline.
- Response keyword checks may overfit wording rather than measure the intended safety
  decision.
- Generalizing source handling or zero-mutation behavior could weaken existing fail-closed
  pilots.
- Thirty nondeterministic model calls can provide pilot signal only and consume signed-in
  account capacity.
decisions:
- Preserve current specs by treating methodologies without kind as installed skills.
- Model the baseline explicitly as kind none and require sources only for installed-skill
  arms.
- Keep five tasks and three repetitions so the live authorization boundary remains
  30 calls.
- Use hidden deterministic checks as primary evidence and never use an AI judge as
  the correctness gate.
- Keep live execution out of this work; a later exact user confirmation must name
  the 30-call boundary.
verification:
- Add failing regressions before runner behavior changes and retain all existing comparative
  tests.
- Verify neutral fixture baselines offline and inspect their initial trees for skill
  or agent-rule contamination.
- Generate the deterministic plan and attempt the fail-closed source/runtime probe
  without model calls.
- Run the full Python suite, skill-suite validator, protocol validator, and diff integrity
  checks.
next_action: Repair or reinstall the Codex Windows sandbox helper, then request a
  separate exact 30-call authorization before any live pilot.
evidence:
- EVIDENCE-038
---
# Plan

1. Add fail-closed methodology-kind validation and source mapping that omits no-skill arms.
2. Prepare each run according to its methodology, build neutral prompts, pass the local
   final message to hidden checks, and scope zero-mutation failure to mutation-required tasks.
3. Add two non-mutating fixtures and reuse three existing deterministic fixtures in a
   pinned v0.2.0-versus-no-skill preregistration.
4. Document the pilot, run offline gates, and record limitations without authorizing live calls.
