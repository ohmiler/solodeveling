---
solodeveling_schema: 1
id: WORK-012
title: Make runtime installation zero-config
status: done
level: standard
type: change
goal: Let ordinary users install, check, and uninstall Solodeveling with short commands that do not require runtime or dry-run flags.
scope: Add deterministic project-local runtime discovery, default to the standard agents skill path when no runtime marker exists, auto-discover managed installations for check and uninstall, retain explicit flags as advanced backward-compatible overrides, and simplify public documentation.
out_of_scope: Removing advanced flags, changing agent-native skill discovery rules, installing outside the selected project root, interactive prompts, global agent configuration, or publishing a package.
acceptance:
- solodeveling install works with no options and installs into .agents/skills when no supported runtime marker exists.
- Project markers select Claude Code, Cursor, or the standard agents path automatically; multiple distinct detected runtimes are handled deterministically without duplicate writes to the shared codex/generic path.
- solodeveling check and solodeveling uninstall work without runtime options by discovering Solodeveling-managed manifests and fail clearly when nothing is managed.
- Explicit --runtime, --project-root, --source, and --dry-run behavior remains backward compatible for automation and advanced recovery.
- Quick-start and primary installation documentation show only short commands; advanced flags are documented separately and do not appear necessary for ordinary installation.
- Focused regressions, full Python and Node tests, skill/protocol validation, package checks, and diff review pass.
risks:
- Incorrect detection could write skills into an unrelated agent directory or omit a runtime the developer expects.
- Multiple detected runtimes could create partial installation if one target fails after another succeeds.
- Codex and generic share .agents/skills and must not be treated as two independent targets.
- Automatic uninstall must never infer unmanaged directories or remove files without a valid Solodeveling manifest and unchanged hashes.
decisions:
- Prefer project-local directory markers and existing managed manifests over global executable or environment detection.
- Default a marker-free project to codex-compatible .agents/skills so the shortest command always has a deterministic useful result.
- Detect and operate on every distinct project-local runtime marker, deduplicated by target path; existing manifest identity wins for a shared path.
- Keep explicit flags as advanced overrides but remove dry-run from the normal two-step installation story.
- Preflight every detected install target before applying any target to prevent ordinary collision-driven partial installs.
verification:
- Begin with failing CLI regressions for marker-free default, Claude/Cursor detection, multiple markers, existing-manifest discovery, no-install check/uninstall failure, and explicit override compatibility.
- Run focused adapter and documentation tests after each slice.
- Run full Python and Node suites, canonical and official skill validators, protocol validation, compileall, dependency health, package build checks, and diff review.
next_action: Use the short installation commands in the next release; owner-controlled release prerequisites and publication remain separately authorized.
security_considerations:
- Detection reads only fixed project-relative marker and manifest paths and must not execute agent binaries or trust environment-provided paths.
- Check and uninstall may act only on validated manifests; unchanged-hash and containment protections remain mandatory.
- Runtime input remains constrained to the existing allowlist.
recovery:
- Explicit --runtime remains available when automatic detection is not desired.
- Installation retains per-target rollback and performs all collision/hash preflights before writes; uninstall refuses changed managed files rather than forcing deletion.
- Revert the CLI discovery change without modifying already managed skill bytes or manifests if detection proves confusing.
evidence:
- EVIDENCE-012
---

# Implementation plan

1. Record the Standard zero-config UX boundary and failing behavior/documentation tests.
2. Add deterministic runtime discovery from validated manifests and fixed project markers.
3. Route install, check, and uninstall across discovered unique targets with preflight protection and explicit-flag compatibility.
4. Rewrite Quick Start and primary installation examples around `solodeveling install`, `check`, and `uninstall`.
5. Run the complete gate, record evidence, and integrate through review without publishing.
