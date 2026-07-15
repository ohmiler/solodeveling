# Cross-agent behavioral evaluation

Solodeveling evaluates protocol behavior, not writing style or model preference. Codex,
Claude Code, and Cursor run as isolated runtimes under test. They are not subagents
that implement the repository, and ordinary Solodeveling correctness never depends on
calling another agent.

## Contracts

The versioned corpus is evals/scenarios/core.yaml. Each scenario declares the expected:

- Quick, Standard, or Critical level.
- One primary Solodeveling workflow.
- Proceed, clarify, diagnose, verify, pause, or refuse action.
- Explicit-authority and recovery requirements.
- Whether completion may be claimed now.
- Enumerated protocol signals.

Every runtime returns evals/evaluation-response.schema.json. Deterministic scoring
checks six critical scalar gates plus the required signal set. All seven criteria must
pass; prose in acceptance_summary, limitations, and next_action remains free to vary.
No model judges another model.

The sanitized result format is evals/evaluation-result.schema.json. Result states keep
live-pass, semantic-failure, safety-failure, invalid-output, auth-failure,
network-failure, timeout, runtime-failure, unavailable, and replay outcomes distinct.

## Safety boundary

Each live scenario receives a fresh temporary project containing the canonical skills
through its native adapter and minimal Solodeveling state. The harness:

- Sends prompts through stdin and subprocess argument arrays with shell disabled.
- Passes an allowlist of operating-system path variables, not API-key environment
  variables or conversation history.
- Uses Codex ephemeral read-only mode, Claude plan mode with only Read and no session
  persistence, and Cursor print mode without force.
- Hashes the entire fixture before and after execution. Any mutation is a safety
  failure even when semantic fields are correct.
- Rejects high-confidence secret-like output before retaining a structured response.
- Deletes disposable fixtures and writes only sanitized local result documents.

Codex uses skip-git-repo-check only because the generated directory is a controlled
disposable fixture. Do not copy that flag into evaluation of an untrusted workspace.

## Commands

Inspect availability without an agent call:

    solodeveling eval probe

Preview the representative matrix without an agent call:

    solodeveling eval run --runtime codex --runtime claude-code --smoke --dry-run

Run three smoke scenarios on Codex and Claude Code:

    solodeveling eval run --runtime codex --runtime claude-code --smoke --claude-budget-usd 0.25

The Claude ceiling applies per fresh scenario, so three smoke scenarios have a maximum
configured ceiling of USD 0.75. Actual cost is recorded when Claude returns it. Codex
usage follows the authenticated CLI account and currently has no harness cost flag.

Validate one scenario before expanding a live matrix:

    solodeveling eval run --runtime codex --smoke --scenario quick-local-documentation


Run Cursor only when cursor-agent is installed and authenticated:

    solodeveling eval run --runtime cursor --smoke

Cursor print mode is deliberately used without force. Cursor result JSON wraps the
assistant text, so the harness parses and validates the inner JSON locally.

Local results default to evals/results/latest.json and are ignored by Git. Do not
commit raw runtime logs, credentials, session identifiers, or sensitive prompts.

## Replay

Replay scores a saved structured response without calling an agent:

    solodeveling eval replay --input evals/results/replay-input.json

Replay input contains a runtime and a responses mapping keyed by scenario ID. A replay
pass proves only that those saved fields satisfy the current deterministic rubric. It
is never fresh live evidence and cannot upgrade a runtime support tier.

## Evidence tiers

- Structural conformance: canonical bytes and adapter contracts pass locally.
- Live pass: a named runtime version passed named scenarios with fixture integrity.
- Live failure: the runtime ran but a semantic, safety, output, or process gate failed.
- Unavailable: the required executable or environment was absent.
- Tier 1 verified: all required core scenarios pass live on Codex, Claude Code, and
  Cursor under the declared versions and limits.

Current claims must come from recorded evidence, not this guide.

## Primary runtime sources

Checked 2026-07-15:

- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)
  documents exec, ephemeral sessions, read-only sandboxing, JSONL, and JSON Schema
  output.
- [Claude Code programmatic mode](https://code.claude.com/docs/en/headless) documents
  print mode, JSON Schema output, no-session persistence, and cost metadata.
- [Cursor CLI parameters](https://docs.cursor.com/en/cli/reference/parameters) and
  [output format](https://docs.cursor.com/en/cli/reference/output-format) document
  print mode and JSON result envelopes. Cursor print mode can access tools; never add
  force to this evaluation.
