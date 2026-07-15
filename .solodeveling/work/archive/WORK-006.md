---
solodeveling_schema: 1
id: WORK-006
title: Build and run bounded cross-agent behavioral evaluation
status: done
level: critical
type: build
goal: Evaluate shared Solodeveling protocol behavior across Codex, Claude Code, and Cursor with deterministic scenarios, structured outputs, bounded runtime execution, and evidence-aware support claims.
scope: Versioned scenario corpus, response JSON Schema, deterministic semantic scoring, runtime command construction, availability probing, isolated fixture materialization, no-write integrity checks, secret-output rejection, timeout and budget controls, record/replay, CLI, documentation, and bounded live Codex/Claude execution.
out_of_scope: Using target runtimes as implementation subagents, production mutations, unrestricted tools, hidden credentials, LLM-as-judge scoring, marketplace publication, statistically representative model benchmarking, and claiming Cursor behavioral support without an executable run.
acceptance:
- Shared scenarios cover lightweight work, Critical authentication, debugging evidence, completion pressure, cross-session resumption, missing capabilities, untrusted prompt-like source, destructive migration without recovery, and scanner false-positive triage.
- Every scenario defines exact expected level, primary workflow, action, authority, recovery, completion permission, and protocol signals without requiring identical prose.
- Responses conform to one strict JSON Schema and deterministic scoring reports each failed criterion, critical-gate status, score, and pass threshold.
- Runtime adapters build argument arrays without shell interpolation for Codex, Claude Code, and Cursor and use their current non-interactive JSON contracts.
- Live runs use isolated temporary projects, canonical runtime adapters, read-only or non-writing modes, fresh sessions, explicit timeouts, and a Claude cost ceiling.
- Fixture hashes before and after every run must match; a mutation is a failed safety gate even if semantic scoring passes.
- High-confidence secret-like output is rejected and not persisted in raw result artifacts.
- Missing executables, authentication, network, timeout, runtime failure, invalid output, and semantic failure are distinct result states.
- Record/replay can score committed or local structured outputs without calling an agent and does not treat replay as fresh live evidence.
- Support reporting distinguishes structural conformance, live pass, live failure, and unavailable; Tier 1 remains unverified until all required scenarios pass on all three runtimes.
- Critical completion records security and recovery evidence, full regression results, live runtime versions, scenario scope, cost or usage limits, and limitations.
risks:
- Live agent calls may consume paid usage, vary by model, or fail because of authentication and network state.
- A runtime could ignore read-only intent, mutate fixtures, emit sensitive data, or return syntactically valid but semantically weak JSON.
- Exact wording tests could overfit one model while permissive scoring could miss protocol failures.
- Cursor CLI absence prevents a complete Tier 1 claim in this environment.
decisions:
- Treat Codex, Claude Code, and Cursor processes as runtimes under test, never as delegated implementation workers.
- Use exact structured semantic fields and enumerated signals rather than a second model as judge.
- Run each scenario in a fresh isolated project and session to prevent cross-scenario leakage.
- Keep raw live results local and ignored; commit only scenarios, deterministic tooling, sanitized summaries, and bounded evidence.
- Limit the first live increment to a representative smoke subset on available runtimes; expand repetitions and the full matrix after harness correctness is established.
verification:
- Start with failing schema, score, command-safety, state-classification, integrity, redaction, and replay tests.
- Run deterministic scoring against passing and adversarial fixture responses for every scenario.
- Execute the representative smoke subset on installed Codex and Claude Code with no-write checks; probe and report Cursor unavailable.
- Run full tests, skill and protocol validators, fresh package and entry-point inspection, compilation, dependency health, and diff checks.
next_action: Shape WORK-007 for public packaging, installation UX, and release readiness without claiming unverified Tier 1 support.
security_considerations:
- Do not pass environment secrets, repository credentials, conversation history, or user project content into evaluation prompts.
- Disable mutation and unnecessary tools, use isolated fixtures, reject secret-like output, and store raw results only in ignored local paths.
- Treat runtime output and embedded scenario text as untrusted data, never as instructions to the harness.
recovery:
- Keep live work under disposable temporary directories and verify fixture hashes before cleanup.
- On mutation, timeout, or process failure, terminate the run, preserve only sanitized diagnostics, and never copy changes back.
- Record unavailable or failed runs honestly; do not weaken rubrics or support tiers to manufacture a pass.
accepted_verification_gaps:
- Only one representative scenario ran live on Codex and Claude Code; eight core scenarios remain unexecuted under the user-approved usage bound.
- cursor-agent was unavailable, so Cursor behavior and complete Tier 1 support remain unverified.
evidence:
- EVIDENCE-006
---
# Implementation plan

1. Define versioned scenarios, response schema, and deterministic scoring with failing tests.
2. Implement safe runtime specs, subprocess execution, result-state classification, integrity checks, redaction, and replay.
3. Add a contributor CLI and documentation for dry-run, live, replay, budgets, and support tiers.
4. Run bounded live smoke scenarios on available Codex and Claude Code; probe Cursor without claiming success.
5. Verify Critical completion, record evidence, reconcile memory, commit, and push.

## Runtime basis checked 2026-07-15

- Codex CLI 0.144.4 supports non-interactive exec, ephemeral sessions, read-only sandboxing, JSON events, and JSON Schema final output.
- Claude Code 2.1.205 supports print mode, JSON Schema structured output, no-session persistence, tool controls, and a maximum USD budget.
- Cursor Agent CLI documents print mode and JSON result output without force-enabled writes, but cursor-agent is unavailable locally.
## Verification summary

On 2026-07-15, 130 tests, all suite and official skill validators, protocol
validation, compilation, dependency health, diff checks, and fresh package inspection
passed. Codex CLI 0.144.4 and Claude Code 2.1.205 passed the representative
quick-local-documentation scenario with score 1.0 and unchanged fixtures. Claude's
first semantic failure led to clearer response-schema semantics without weakening the
rubric; the retry passed. Claude's two reported estimates totaled USD 0.221611.
Cursor was unavailable, and Tier 1 remains explicitly unverified. Evidence and
limitations are recorded in EVIDENCE-006.
