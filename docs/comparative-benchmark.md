# Controlled comparative benchmark

This repository contains a preregistered pilot for measuring workflow overhead
between Solodeveling 0.1.1 and Superpowers 6.1.1. It does not contain benchmark
results and does not support a public claim that either methodology is faster.

## Fairness boundary

The pilot uses the same Codex CLI, `gpt-5.6` model, medium reasoning effort,
offline workspace sandbox, prompts, seed projects, timeouts, and hidden outcome
checks. Both methodologies are checked out at exact commits, copied into the
project-local `.codex/skills` directory before timing, and explicitly invoked in
the otherwise identical prompt. Every run receives a fresh linked Git worktree.
Fixture preparation and skill installation are outside task wall time.

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
python scripts/comparative_benchmark.py score benchmarks/results/pilot.json
```

`plan` prints the exact model, runtime, timeout, pins, mutation boundary, run
order, and required confirmation. `verify-fixtures` proves each seed passes its
visible baseline while failing its hidden completion check. `score` analyzes an
existing sanitized result without contacting a model. `probe` verifies the exact
CLI version, source commits, clean checkouts, and root skills, then prints the
fully resolved live command without contacting a model.

## Live authorization boundary

`run-live` is deliberately separate. It requires the exact confirmation printed
by `plan`, exact pinned Git checkouts supplied as source paths, the preregistered
Codex CLI version, and all 18 runs. It fails closed on a source or runtime
mismatch. Raw prompts and JSONL are held only in the temporary run process;
committed evidence may contain only the sanitized result schema.
After every attempted run, the sanitized result is written through an atomic
checkpoint. Re-running the exact command resumes only missing run IDs and refuses
a checkpoint whose preregistration hash, provenance, or run identity differs.

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
