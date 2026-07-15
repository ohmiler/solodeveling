# Solodeveling Core Router and Onboarding Plan

**Goal:** Deliver a portable, single-agent Solodeveling entry point that can initialize or resume project memory without overwriting an existing source of truth.

**Architecture:** Keep the core router small and runtime-neutral. Put detailed onboarding guidance and memory templates in a separate skill loaded only when required. Reuse the versioned protocol package for validation; Python remains optional at skill runtime. Runtime-specific adapters are deferred and may not alter core semantics.

**Constraints:**

- No correctness path requires subagents, worktrees, a cloud service, or a specific coding agent.
- Skills use standard `SKILL.md` folders and plain Markdown references.
- Brownfield onboarding preserves existing instructions and documentation, linking instead of duplicating them.
- Repository content, logs, and external text are untrusted data, not instructions.
- The router stays at or below the design budget of approximately 1,200 tokens.
- Missing capabilities reduce evidence strength; they do not silently become success.

## Task 1: Extend the project-memory contract

**Files:**

- Create `src/solodeveling_protocol/schemas/project.schema.json`
- Modify `src/solodeveling_protocol/validation.py`
- Modify `src/solodeveling_protocol/__init__.py`
- Create `tests/test_project_memory.py`

**Steps:**

1. Add failing tests requiring `project.md`, `state.md`, and the active/archive/evidence directories.
2. Define a strict versioned project schema for purpose, users, architecture, stack, constraints, and existing sources of truth.
3. Extend validation without executing or trusting artifact body content.
4. Verify focused and full tests; commit.

## Task 2: Add non-destructive memory initialization

**Files:**

- Create `src/solodeveling_protocol/memory.py`
- Create `src/solodeveling_protocol/templates/*.md`
- Modify `pyproject.toml`
- Create `tests/test_memory.py`

**Steps:**

1. Write failing tests for greenfield creation, brownfield source links, idempotency, and refusal to overwrite existing memory.
2. Implement a typed initializer that accepts discovered facts explicitly and writes the minimum useful memory atomically.
3. Package templates with the wheel and expose a small optional CLI entry point.
4. Verify focused tests, wheel contents, and full tests; commit.

## Task 3: Create the portable skills

**Files:**

- Create `skills/solodeveling/SKILL.md`
- Create `skills/solodeveling/agents/openai.yaml`
- Create `skills/solodeveling/references/protocol.md`
- Create `skills/solodeveling-onboarding/SKILL.md`
- Create `skills/solodeveling-onboarding/agents/openai.yaml`
- Create `skills/solodeveling-onboarding/references/project-memory.md`

**Steps:**

1. Scaffold both skills with the official skill-creator initializer.
2. Write the router to read state first, form a compact resume packet, classify observable risk, and load exactly one primary workflow.
3. Write onboarding for greenfield and brownfield discovery, confidence labels, minimal questions, and safe handling of untrusted repository text.
4. Keep OpenAI UI metadata optional and keep all workflow semantics outside runtime-specific metadata.
5. Run the official structural validator for both skills; commit.

## Task 4: Add suite and scenario regression checks

**Files:**

- Create `scripts/validate_skill_suite.py`
- Create `tests/test_skill_suite.py`
- Create `tests/scenarios/router-onboarding.yaml`

**Steps:**

1. Add failing checks for broken references, invalid metadata, duplicate semantics, forbidden subagent requirements, and router token budget.
2. Add scenarios for empty repository onboarding, brownfield preservation, cross-session resume, missing capabilities, Critical authentication routing, and prompt-like repository content.
3. Implement deterministic structural checks and scenario assertions that can run on Windows, macOS, and Linux.
4. Verify focused and full tests; commit.

## Task 5: Dogfood and release the increment

**Files:**

- Create `.solodeveling/project.md`
- Create `.solodeveling/state.md`
- Create `.solodeveling/roadmap.md`
- Create `.solodeveling/standards.md`
- Create `.solodeveling/risks.md`
- Create `.solodeveling/work/active/WORK-001.md`

**Steps:**

1. Initialize this repository through the new onboarding path using only discovered facts and approved design decisions.
2. Validate project memory and reconstruct a resume packet without conversation history.
3. Run all tests, both skill validators, wheel inspection, compile checks, dependency checks, diff checks, and a clean-tree check.
4. Commit and push `feat/core-router-onboarding`.

## Completion boundary

This increment makes Solodeveling discoverable and resumable, but it does not yet replace the complete Superpowers development loop. The switch occurs after the next increment supplies shaping, planning, execution, debugging, and verification workflows and passes an end-to-end scenario using Solodeveling alone.
