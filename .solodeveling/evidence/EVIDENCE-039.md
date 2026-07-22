---
solodeveling_schema: 1
id: EVIDENCE-039
work_item: WORK-039
claim: The comparative runner correctly pairs Codex standalone sandbox resources with
  the canonical CLI executable and passes the complete no-model Windows readiness probe.
method: Failing-first resource-layout, child-environment, runtime-canonicalization,
  and sandbox-pin regressions; signed binary inspection; manual differential probes;
  real offline benchmark probe; and full repository gates.
command: comparative pytest 30; full pytest 277; validate_skill_suite.py; protocol
  validation; comparative probe; git diff --check.
result: passed
scope: WORK-039 maintenance boundary only.
limitations:
- No live benchmark call ran, so this proves harness readiness only and provides no
  comparative performance or quality result.
- A successful preflight cannot guarantee that all later model calls will complete;
  the checkpoint and circuit-breaker protections remain necessary.
- Native Windows packaging may change again and requires a new explicit regression
  before accepting another resource layout.
---
# Evidence

## Observation log

- Codex CLI 0.144.6 resolves through the standalone package.
- The signed helper exists at `codex-resources/codex-windows-sandbox-setup.exe`, not
  beside `bin/codex.exe` and not on PATH.
- The existing preflight checks only the executable sibling and PATH, producing a
  reproducible false negative before inference.
- The first resource-layout regression failed with the expected unavailable-helper
  error. Exact `codex-resources` discovery repaired it while preserving the missing,
  sibling, and PATH boundaries.
- Setup then succeeded but the junction-launched CLI could not find its versioned
  command runner. A manual differential probe showed that the exact release executable
  passes the preferred `elevated` sandbox in the normal user temp directory.
- The runner now resolves the executable before probe/live launch and exposes the
  paired resource directory only to the sanitized child PATH. The preregistration
  explicitly pins `windows.sandbox="elevated"`.
- The real offline probe passed Codex CLI 0.144.6, signed helper discovery,
  `:workspace` write verification, the cached `gpt-5.6-sol` medium model entry, and
  clean source commit `ca7c3b356c2e9444963a52e00e2e97198ad94e7d` without inference.
- Final verification passed 30 comparative tests, 277 full tests, skill validation,
  protocol validation, and diff integrity. All WORK-039 temporary directories and
  its detached worktree were removed.
