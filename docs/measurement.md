# Measuring Solodeveling

Solodeveling quality is not one number. Evaluate outcome quality before workflow
overhead, then keep controlled comparisons separate from observational field data.

## Evidence levels

1. Deterministic protocol and packaging tests show that specified routing and safety
   behavior exists.
2. Dogfood and field observations show whether behavior helps real work and how often
   it feels disproportionate.
3. Controlled paired pilots estimate whether one pinned version changes correctness
   or overhead under the same model, prompts, fixtures, and runtime.
4. A public comparative claim requires a broader preregistered confirmatory study.

Current evidence supports reduced internal workflow overhead and preserved release
controls. It does not establish that Solodeveling is faster than another methodology.

## Solodeveling 0.2.0 versus no skill

The preregistration in
`benchmarks/comparative/solodeveling-0.2.0-vs-no-skill.yaml` tests the narrower
claim behind the README comparison: whether a shared delivery protocol changes
correctness or observable workflow overhead compared with the same agent receiving
no project skill. It pins Solodeveling 0.2.0 to commit
`ca7c3b356c2e9444963a52e00e2e97198ad94e7d`. The no-skill arm has no source
checkout, installs no project skill, and receives no skill invocation.

Both arms otherwise receive the same Codex CLI, model, reasoning effort, permission
profile, network boundary, fixture, task text, neutral execution instructions,
timeout, and hidden check. Skill installation happens before timing. Every run uses
a fresh isolated Git worktree with user configuration and repository rules ignored.
The Windows preregistration pins the preferred `elevated` native sandbox. The runner
canonicalizes the standalone executable before launch so its signed package-relative
sandbox setup and command-runner resources remain paired with that CLI version.
The fixtures contain no `AGENTS.md` or alternate agent rules. Existing project
memory appears only in the bounded-continuation task because resuming that state is
the behavior being tested.

Five tasks cover Direct Read-Only inspection, a Quick change, a Standard repair,
bounded continuation, and Critical readiness review. Three paired repetitions over
two arms produce 30 calls. The two non-mutating tasks are checked using both the Git
diff and the saved final response; deterministic checks require the requested facts
or safety boundaries without using an AI judge. Mutation-required tasks retain the
zero-mutation circuit breaker.

These commands make no model calls:

    python scripts/comparative_benchmark.py --spec benchmarks/comparative/solodeveling-0.2.0-vs-no-skill.yaml plan
    python scripts/comparative_benchmark.py --spec benchmarks/comparative/solodeveling-0.2.0-vs-no-skill.yaml verify-fixtures
    python scripts/comparative_benchmark.py --spec benchmarks/comparative/solodeveling-0.2.0-vs-no-skill.yaml probe --source solodeveling-0.2.0=PINNED_V020_CHECKOUT

`probe` verifies the pinned runtime, local model catalog, sandbox and permission
capabilities, and a clean exact source checkout without inference. `run-live` is a
separate authorized action: it requires the exact confirmation printed by `plan`
and can consume up to 30 calls from the signed-in account. Preparing or validating
this preregistration does not authorize those calls.

The current offline probe passed on Codex CLI 0.144.6 with the signed standalone
Windows helper, the `elevated` `:workspace` write check, `gpt-5.6-sol` at medium
reasoning, and the clean pinned v0.2.0 commit. This establishes harness readiness,
not a comparative result.

Correctness remains primary. Timing, tokens, tool calls, questions, changed files,
and workflow artifacts are compared only where both paired runs pass. Any outcome
is pilot signal only: it cannot show that the model became smarter, cannot establish
universal superiority, and cannot support a public speed or quality claim without a
broader preregistered confirmatory study and independent review.

## Feedback pilot: 0.1.1 versus 0.1.2

The preregistration in benchmarks/comparative/feedback-0.1.1-vs-0.1.2.yaml compares
the exact 0.1.1 and 0.1.2 source commits. Five tasks cover Quick documentation, Quick
code, ordinary bug repair, a same-boundary follow-up, and a medium feature. Three
paired repetitions produce 30 calls.

Feedback pilot 1 is invalid: its first run completed without mutating the fixture,
failed the hidden check, and correctly stopped before run 2. Because that runner
version did not preserve a local failure transcript or final agent message, the
successor preregistration adds ignored, local-only diagnostics for unsuccessful runs.
The invalid run is evidence about the harness, not evidence for either skill version.

Feedback pilot 2 is also invalid: its first run was forced read-only by a mismatch
between the legacy sandbox flag and the active Codex permission-profile runtime. Its
diagnostic proved that patches and tests were policy-blocked, then the gate stopped
before run 2. Pilot 3 selects the built-in `:workspace` profile and runs a no-model
write probe before inference. Neither invalid run is comparative skill evidence.

Correctness is primary. Time, tokens, tool calls, questions, changed files, and
workflow artifacts are compared only for pairs where both versions pass visible
tests and the external hidden check. The study is pilot signal only.

These commands make no model calls:

    python scripts/comparative_benchmark.py --spec benchmarks/comparative/feedback-0.1.1-vs-0.1.2.yaml plan
    python scripts/comparative_benchmark.py --spec benchmarks/comparative/feedback-0.1.1-vs-0.1.2.yaml verify-fixtures
    python scripts/comparative_benchmark.py --spec benchmarks/comparative/feedback-0.1.1-vs-0.1.2.yaml probe --source solodeveling-0.1.1=PINNED_CHECKOUT --source solodeveling-0.1.2=PINNED_CHECKOUT

The live command requires the exact confirmation printed by plan, exact clean source
checkouts, the pinned Codex runtime and model, a working sandbox, and at most 30 calls.

Pilot interpretation uses these proposed decision thresholds:

- candidate correctness must not be lower than the baseline;
- Quick workflow-artifact median should be zero;
- questions and workflow artifacts should fall by at least 20 percent on Quick and
  bounded-follow-up pairs;
- elapsed-time or token improvements below 15 percent are inconclusive;
- any authorization, verification, or recovery regression rejects the improvement.

These thresholds guide whether a confirmatory study is worthwhile. They do not turn
the pilot into public proof.

## Twenty-task field scorecard

Copy benchmarks/field/scorecard.template.json to an ignored path under
benchmarks/field/results/ and add one sanitized observation after each real task. The
schema has no project name, repository path, prompt, free-text notes, source, secrets,
or raw model output.

Record observable values only. User annoyance and ceremony fit are optional and
should be entered only when the user supplies them. correctness_passed means real
acceptance checks passed; it must not be inferred from an agent completion message.

    python scripts/field_scorecard.py validate benchmarks/field/results/field-20.json
    python scripts/field_scorecard.py summary benchmarks/field/results/field-20.json

Review overall and per-tier correctness, verification, elapsed time, question count,
workflow artifacts, rework, resume accuracy, annoyance, and too-heavy ceremony rate.

Suggested field targets are:

- at least 20 completed observations across Quick, Standard, and Critical work;
- correctness and verification rates reported separately;
- Quick median workflow artifacts of zero;
- Standard median workflow artifacts no greater than two;
- Critical authorization and verification boundaries satisfied every time;
- median user annoyance no greater than two and too-heavy ceremony at or below ten
  percent.

Missing values stay missing. Never replace unavailable tokens, timing, resume, or user
ratings with zero. Field results remain observational and local.
