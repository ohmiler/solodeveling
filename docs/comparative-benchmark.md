# Controlled comparative benchmark

This repository contains a preregistered successor pilot for measuring workflow overhead
between Solodeveling 0.1.1 and Superpowers 6.1.1. It does not support a public
claim that either methodology is faster.

Pilot 1 attempted 18 processes with the `gpt-5.6` alias, but every process failed
before inference with zero tokens and zero tool calls. The alias was absent from
the fresh local Codex model catalog. That execution is archived as invalid runtime
evidence. Pilot 2 used the exact account-visible `gpt-5.6-sol` slug and completed
18 inference processes, but the harness had copied both methodology suites to
`.codex/skills` instead of Codex's project adapter path `.agents/skills`. Both
sides produced zero changed files and zero correct runs. Pilot 2 is therefore
archived as invalid methodology-activation evidence, not comparative evidence.
Pilot 3 then completed 18 inference processes with the corrected skill path, but
again produced zero changed files and zero correct runs. The local Codex Windows
sandbox log records repeated failures to launch
`codex-windows-sandbox-setup.exe` because the helper is absent. Raw per-run logs
were intentionally not retained, so this is the strongest supported shared
execution diagnosis rather than verbatim per-run proof. Pilot 3 is archived as
invalid execution-sandbox evidence. Pilot 4 adds a fail-closed helper preflight
and has not been run.

The feedback-specific Solodeveling 0.1.1-versus-0.1.2 study and local twenty-task
field scorecard are documented in [Measuring Solodeveling](measurement.md). They
do not alter Pilot 4 or the archived Solodeveling-versus-Superpowers boundary.
That document also contains a separate preregistered 30-call pilot comparing pinned
Solodeveling 0.2.0 with a true no-skill arm. It has not been run and is not evidence
that Solodeveling is faster or better.

## Fairness boundary

The successor pilot uses the same Codex CLI, `gpt-5.6-sol` model, medium reasoning effort,
offline workspace sandbox, prompts, seed projects, timeouts, and hidden outcome
checks. Both methodologies are checked out at exact commits, copied into the
project-local `.agents/skills` directory before timing, verified at their named
root skill, and explicitly invoked in
the otherwise identical prompt. Every run receives a fresh linked Git worktree.
Fixture preparation and skill installation are outside task wall time.
On Windows, the live gate also requires the Codex sandbox setup helper before
the first model call. A completed process that produces zero mutations for these
mutation-required fixtures is checkpointed as an execution failure and stops
the sequence before the next call.

The 18-run plan covers three repetitions of a small documentation task, a bug
repair, and a medium feature for each methodology. A fixed seed determines the
counterbalanced order. Correctness is reported before speed; timing comparisons
only include pairs where both runs pass visible tests and the external hidden
check.

## Safe commands

These commands perform no model calls:

```text
python scripts/comparative_benchmark.py plan
python scripts/comparative_benchmark.py verify-fixtures
python scripts/comparative_benchmark.py probe --solodeveling-source PINNED_SOLODEVELING_CHECKOUT --superpowers-source PINNED_SUPERPOWERS_CHECKOUT
python scripts/comparative_benchmark.py score benchmarks/results/solodeveling-superpowers-pilot-4.json
```

`plan` prints the exact model, runtime, timeout, pins, mutation boundary, run
order, and required confirmation. `verify-fixtures` proves each seed passes its
visible baseline while failing its hidden completion check. `score` analyzes an
existing sanitized result without contacting a model. `probe` verifies the exact
CLI version, source commits, clean checkouts, and root skills, then prints the
fully resolved live command without contacting a model. On Windows it also
rejects a missing Codex sandbox helper without contacting a model.

## Live authorization boundary

`run-live` is deliberately separate. It requires the exact confirmation printed
by `plan`, exact pinned Git checkouts supplied as source paths, the preregistered
Codex CLI version, an exact model slug and reasoning level present in the local
Codex model catalog, and all 18 runs. It fails closed on a source or runtime
mismatch. Raw prompts and JSONL are held only in the temporary run process;
committed evidence may contain only the sanitized result schema.
After every attempted run, the sanitized result is written through an atomic
checkpoint. Re-running the exact command resumes only missing run IDs and refuses
a checkpoint whose preregistration hash, provenance, or run identity differs.
If a process fails before inference with no tokens or tool calls, a circuit breaker
checkpoints that attempt, stops before the next call, and makes the checkpoint
non-resumable. Recovery then requires a distinct successor preregistration.
The same non-resumable boundary applies when a process returns successfully but
produces zero mutations and fails the hidden completion check.

Model calls consume the signed-in account's capacity or credits. Therefore the
live command must not be run until the owner separately authorizes the named
model, 18-call maximum, 1,200-second per-run timeout, source pins, and account
boundary.

## Interpretation

This pilot is designed to find measurement problems and estimate whether a
larger confirmatory study is worthwhile. Service load, caching, model
nondeterminism, and synthetic fixtures remain important limitations. Regardless
of the observed difference, the pilot is permanently marked
`pilot-signal-only`; a public comparative claim requires a separately
preregistered confirmatory benchmark with broader tasks and independent review.
