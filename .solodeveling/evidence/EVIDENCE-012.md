---
solodeveling_schema: 1
id: EVIDENCE-012
work_item: WORK-012
claim: Ordinary project installation, verification, and removal use short flag-free commands while deterministic project-local runtime discovery preserves managed-file, containment, collision, symlink, and explicit-override protections.
method: Failing-first zero-config CLI regressions, runtime discovery and adversarial marker tests, packaged-resource integration, documentation contracts, full Python and Node regression, canonical and official skill validation, protocol validation, compilation, dependency health, and diff review.
command: python -m pytest -q; npm test --prefix packages/npm; python scripts/validate_skill_suite.py; official quick_validate.py for ten skills; python -m solodeveling_protocol.cli .; python -m compileall -q src tests scripts; python -m pip check; git diff --check; GitHub Actions runs 29441919964, 29441947219, and 29442167720.
result: passed
scope: Flag-free install/check/uninstall, marker-free default, project-local Codex/Agent Skills/Claude Code/Cursor detection, distinct-target deduplication, existing-manifest identity, multi-target preflight, no-managed failure, explicit flag compatibility, packaged skill resources, Quick Start, installation documentation, and safety boundaries.
limitations:
- Runtime detection is based on fixed project-local directories and managed manifests; it intentionally does not inspect global agent executables, accounts, or environment-provided paths.
- Several detected adapters are preflighted before writes, but an exceptional operating-system failure during later application can still leave earlier independently atomic targets installed.
- Local Windows could not create the Node test symlink fixture; simulated Python symlink rejection passed and cross-platform CI remains required.
- Agent UI refresh and duplicate-display behavior remain runtime-specific; Cursor and the complete Tier 1 behavior matrix remain unverified.
- No package was published and no release, environment, registry, or Trusted Publisher state changed.
---
# Evidence

## Claims and results

- `solodeveling install` with no options installs packaged canonical skills into `.agents/skills` for a marker-free project. `solodeveling check` and `solodeveling uninstall` rediscover the validated managed manifest without a runtime option. Unit and packaged-resource integration tests passed.
- New projects detect fixed `.codex`/`.agents`, `.claude`, and `.cursor` markers, operate on every distinct adapter path, and deduplicate Codex/generic's shared `.agents/skills` path. Multi-marker and existing-generic-manifest tests passed.
- Automatic install preflights every detected runtime before ordinary writes. An unmanaged Cursor collision prevented the otherwise valid Codex target from being created. Collision regression passed.
- Discovery validates runtime identity and manifest structure, rejects project-path symlinks, and check/uninstall fail clearly when no Solodeveling-managed installation exists. Security regressions passed.
- Explicit `--runtime`, `--project-root`, `--source`, and `--dry-run` paths remain supported for automation and recovery. Existing adapter tests passed.
- README, installation, release notes, and npm launcher documentation use `npx solodeveling install` or `solodeveling install` as the primary UX. Advanced flags are separated from Quick Start and described as optional.

## Verification performed

- `python -m pytest -q`: 203 passed.
- Focused zero-config behavior, packaged-resource, security, and documentation suites passed after the final relevant edits.
- `npm test --prefix packages/npm`: 8 passed and 1 skipped because file symlinks were unavailable on local Windows.
- `python scripts/validate_skill_suite.py`: canonical suite valid.
- Official skill-creator `quick_validate.py`: all ten skill directories valid.
- `python -m solodeveling_protocol.cli .`: protocol validation passed.
- `python -m compileall -q src tests scripts`: passed.
- `python -m pip check`: no broken requirements.
- `git diff --check`: passed.
- GitHub Actions push run 29441919964 and pull-request run 29441947219 passed the Python 3.10/3.14 matrix on Ubuntu, Windows, and macOS; package build/install smoke; all six native targets; and npm pack/npx smoke at commit b629d644f3a62757cf5a1ee8373f8fab76a03b25.
- Post-merge main run 29442167720 passed the same complete matrix at merge commit 4b0812f00c41260c4c66ec04e42d168a59323ac4.

## Security and recovery

- Runtime discovery uses only allowlisted relative paths and never executes agent binaries. Existing valid manifest identity wins for the Codex/generic shared target.
- Installation reuses the existing atomic per-target copy/manifest transaction and adds a complete collision/hash preflight before any detected target is applied.
- Automatic uninstall discovers only validated Solodeveling manifests and retains unchanged-hash, containment, symlink, and no-force-delete protections.
- Explicit runtime selection remains the recovery path for unusual workspaces. Reverting discovery does not require changing already installed bytes or manifests.

## Limitations

- Structural detection does not prove that a specific agent application will refresh or display exactly one skill entry.
- Cross-runtime application remains a sequence of independently atomic targets rather than one filesystem-wide transaction.
- Registry publication and public npx/uvx observation remain outside this work item.
