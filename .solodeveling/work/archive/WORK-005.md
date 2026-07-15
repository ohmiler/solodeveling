---
solodeveling_schema: 1
id: WORK-005
title: Deliver safe portable runtime adapters
status: done
level: critical
type: build
goal: Materialize the canonical Solodeveling skill suite for Codex, Claude Code, Cursor, and generic Agent Skills clients without semantic forks or damage to user files.
scope: Versioned adapter manifest, runtime path mapping, deterministic install/check/uninstall CLI, collision and modification protection, path containment, structural conformance tests, packaging entry point, and runtime guidance.
out_of_scope: Live behavioral claims for all Tier 1 agents, marketplace or plugin publication, global installation, remote execution, and automatic edits to runtime settings.
acceptance:
- Codex maps to .agents/skills, Claude Code to .claude/skills, Cursor to .cursor/skills, and generic clients to .agents/skills without changing canonical skill content.
- Every installation copies the same canonical skill bytes and records relative paths, SHA-256 hashes, runtime, schema, and source identity in a managed manifest.
- Preflight rejects unmanaged collisions, symlink traversal, invalid skills, and paths outside the target project before any write.
- Check reports missing, modified, unexpected, or source-drifted managed files without altering the target.
- Uninstall removes only files whose current hash matches the managed manifest and preserves modified or unrelated user files with an actionable refusal.
- Failed installation rolls back files created by that attempt and never performs blind recursive deletion.
- CLI supports explicit install, check, and uninstall actions plus dry-run output and non-zero failure codes.
- Adapter and core protocol semantics remain separate; runtime adapters cannot alter lifecycle, risk, security, authority, evidence, or Definition of Done.
- Documentation reports evidence-based support tiers, native discovery paths, invocation differences, refresh behavior, and known limitations checked against current primary sources.
- Critical completion records security and recovery evidence and passes full regression, package, and structural validation.
risks:
- Copy-based adapters can drift from canonical skills if update and check semantics are weak.
- A careless uninstall could delete user-authored or modified skills.
- Runtime discovery behavior can change or differ across IDE, CLI, and SDK surfaces.
decisions:
- Materialize ordinary files rather than symlinks for Windows portability and predictable runtime discovery.
- Use Cursor native .cursor/skills instead of relying on currently inconsistent .agents/skills discovery.
- Keep runtime-specific metadata and paths outside canonical skill instructions.
- Defer live cross-agent behavioral Tier 1 claims to WORK-006; structural conformance alone is not behavioral proof.
verification:
- Start with failing mapping, byte-identity, collision, drift, traversal, rollback, dry-run, and safe-uninstall tests.
- Validate current skills before adapter installation and run official validation for every canonical skill.
- Run full tests, suite and protocol validators, fresh wheel build and inspection, compilation, dependency health, and diff checks.
next_action: Shape live cross-agent behavioral evaluation as WORK-006.
security_considerations:
- Treat source skills and existing target files as untrusted until validated and contained.
- Do not follow target symlinks, overwrite unmanaged files, grant tools, change settings, or execute installed skill scripts.
- Hashes provide change detection and identity evidence, not publisher authenticity or trust.
recovery:
- Complete preflight before writes, create files atomically where possible, and roll back only files created by the failed attempt.
- Preserve modified and unrelated target files on uninstall and report exact manual recovery actions.
- Keep canonical skills unchanged so deleting a generated adapter tree can be regenerated from source after authorized review.
evidence:
- EVIDENCE-005
---
# Implementation plan

1. Define adapter mapping and managed-manifest contracts with failing tests.
2. Implement pure planning, containment, hashing, install, check, dry-run, and safe-uninstall behavior.
3. Expose a package CLI and document runtime discovery and evidence tiers.
4. Add structural conformance checks that prevent adapter semantic forks.
5. Verify Critical completion, record evidence, reconcile memory, commit, and push.

## Runtime basis checked 2026-07-15

- Codex discovers repository skills from .agents/skills and invokes them explicitly with $name.
- Claude Code discovers project skills from .claude/skills and invokes them with /name.
- Cursor supports Agent Skills in editor and CLI; the adapter uses its native .cursor/skills path while current .agents/skills discovery inconsistencies remain a documented limitation.
- Agent Skills provides the shared SKILL.md structure; runtime-specific optional fields are not added to canonical frontmatter.

## Verification summary

On 2026-07-15, 94 tests, suite and protocol validators, all ten official skill
validations, Critical metadata inspection, canonical byte conformance for four runtime
mappings, a fresh wheel and entry-point inspection, compilation, dependency health,
and diff checks passed. Evidence and limitations are recorded in EVIDENCE-005.

## Dogfood observations

The protocol validator rejected infrastructure as a work type because work type
describes intent; WORK-005 was correctly classified as build. Pressure tests also
found that non-directory parents and dangling target symlinks needed explicit
preflight guards. Both cases now fail before the copy function is called. A command
transport failure caused by an escaped NUL was rejected before disk mutation and did
not affect product state.