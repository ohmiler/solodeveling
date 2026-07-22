---
solodeveling_schema: 1
id: WORK-039
title: Repair standalone Codex sandbox preflight discovery
status: done
level: standard
type: maintain
goal: Make the comparative benchmark recognize the signed Windows sandbox helper shipped
  in the Codex standalone `codex-resources` layout.
scope: Add failing-first coverage for standalone resource discovery, update the fail-closed
  helper locator, rerun the no-model benchmark probe, and reconcile documentation
  and evidence only if observable behavior changes.
out_of_scope: Copying executables between Codex versions, modifying the Codex app
  or user PATH, live benchmark calls, publication, commit, and push.
acceptance:
- Windows preflight accepts a helper beside the executable, on PATH, or in the exact
  sibling `codex-resources` directory used by the standalone package.
- Windows preflight still rejects installations where none of the supported helper
  locations contains a regular file.
- The real Codex 0.144.6 runtime passes sandbox, permission, model-catalog, and exact
  v0.2.0 source checks without inference.
- Focused and full tests, skill validation, protocol validation, and diff checks pass.
risks:
- Broad helper discovery could accept an unrelated or attacker-controlled executable.
- A preflight pass does not prove a later live model call will complete successfully.
- Runtime packaging may change again and require a new explicitly tested layout.
decisions:
- Treat the observed signed `codex-resources` helper as the supported standalone layout.
- Resolve only deterministic package-relative paths plus the existing PATH fallback.
- Do not repair the installation by copying versioned binaries.
- Keep all live calls behind the separate exact 30-call authorization boundary.
verification:
- Reproduce the current false negative with a resource-layout regression test.
- Run the focused comparative suite and the offline real-runtime probe.
- Run full repository checks and record remaining limitations.
next_action: Request explicit authorization for the pinned 30-call live pilot, or
  commit the verified harness changes separately.
evidence:
- EVIDENCE-039
---
# Plan

1. Model the observed standalone directory layout in a focused regression.
2. Extend helper discovery to the exact package-relative resource directory.
3. Run the real no-model probe with a clean pinned v0.2.0 checkout.
4. Reconcile evidence and stop before any live benchmark call.
