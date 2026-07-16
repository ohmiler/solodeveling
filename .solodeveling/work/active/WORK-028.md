---
solodeveling_schema: 1
id: WORK-028
title: Registry Landing Pages and Patch Release 0.1.1
status: active
level: critical
type: release
goal: Correct the public npm and PyPI landing content through one exact, verified 0.1.1 patch release and prove the first-run installation paths from packaged artifacts.
scope: Version metadata, registry-facing README content, version-neutral installation links, current trusted-publishing documentation, release notes, packaging regressions, dynamic CI smoke paths, local candidate inspection, fresh-install dogfood, protected-main delivery, and separately authorized immutable publication.
out_of_scope: Mutating, replacing, unpublishing, or deprecating 0.1.0; cross-framework benchmarks; new skill behavior; breaking command or schema changes; and unrelated product features.
acceptance:
- Source, Python, npm, native filenames, artifact manifest, and release notes consistently identify version 0.1.1.
- The packed npm README and Python wheel metadata explain the live product and contain no pre-publication claims.
- CI derives package smoke paths from the canonical version instead of embedding 0.1.0.
- Complete regression, protocol, skill, package, and diff verification passes.
- Fresh temporary npm and Python installs from locally built artifacts pass version, install, and check smoke tests.
- A complete release set is bound to one exact protected-main SHA before any external publication.
- Candidate workflow, tag, immutable GitHub Release, PyPI, and npm actions occur only after exact action-specific authorization.
- Post-publication registry descriptions, integrity, provenance, and clean-install behavior are recorded as evidence.
risks:
- npm and PyPI version bytes and descriptions are immutable after upload.
- Native executables remain unsigned even though the release set binds hashes and provenance.
- A version mismatch can make the npm launcher request assets that do not exist.
- Publication changes external state and cannot be inferred from a general instruction to continue.
decisions:
- Use 0.1.1 as a patch release because behavior and public interfaces remain compatible.
- Keep 0.1.0 intact and publish corrected registry content only under a new version.
- Make registry-facing status text version-neutral to reduce future metadata drift.
- Defer controlled comparative benchmarking and unrelated skill changes.
verification:
- Add regressions for canonical version agreement, npm README content, Python long description, and dynamic CI paths.
- Run focused tests first, then the complete Python and Node suites plus protocol and canonical skill validation.
- Build and inspect local Python and npm artifacts, then dogfood them from clean temporary projects.
- After protected-main delivery, record the exact SHA and stop at the explicit publication boundary.
next_action: Commit the verified 0.1.1 source, deliver it through protected main, and record the exact source SHA before requesting candidate authorization.
evidence: []
---

# Release boundary

WORK-028 may prepare, review, merge, and verify source changes. It does not authorize
the candidate workflow, tag, GitHub Release, PyPI publication, npm staging, or npm
publication. Those actions require the exact version and source SHA named at the
boundary defined in docs/publishing.md.

# Verification so far

- Complete Python regression: 222 passed.
- Node launcher regression: 8 passed and 1 Windows symlink capability skip.
- Protocol validation, canonical skill validation, compileall, pip check, and diff
  check passed.
- Locally built wheel metadata reports 0.1.1, contains the current public positioning,
  and excludes the stale pre-publication claims.
- Locally packed npm tarball reports 0.1.1 and contains the corrected registry README.
- A temporary wheel installation reported 0.1.1, installed 31 managed files, and
  passed solodeveling check outside the checkout.
