---
solodeveling_schema: 1
current_goal: Solodeveling 0.1.0 is complete on PyPI with one-command installation verified; npm and next-release workflow simplification remain deferred.
active_work:
- WORK-019
blockers: []
risks:
- PyPI 0.1.0 is public with matching immutable-release digests and public provenance; published bytes require an explicit yank-and-supersede recovery rather than replacement.
- The npm name remains unreserved, and npm Trusted Publishing cannot be configured before the first owner-controlled interactive publication.
- Immutable, non-draft GitHub Release v0.1.0 contains all 13 verified candidate assets and resolves through the tag to commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4; no publish run exists.
- npm first-package bootstrap requires a separate owner-controlled interactive publication with two-factor authentication.
- Native executables are not platform-signed, and Cursor plus complete Tier 1 behavior remain unverified.
next_action: Treat 0.1.0 as complete for PyPI installation; keep npm deferred and return to shaping WORK-019 only when opening the next release.
---
# State

WORK-015 and EVIDENCE-015 record that GitHub Release immutability remains enabled,
`pypi` and `npm` administrator bypass is disabled, reviewer `ohmiler` can self-review,
and exact `main`-only deployment policy remains configured.

The owner confirmed the PyPI pending publisher for project `solodeveling`, GitHub
owner `ohmiler`, repository `solodeveling`, workflow `publish.yml`, and environment
`pypi`. Public independent verification is unavailable until first authorized OIDC
use. WORK-016 and EVIDENCE-016 record the successful non-publishing 0.1.0 candidate
run, coordinated release set, local integrity verification, and strict provenance
verification for all 13 files. No tag, GitHub Release, staging action, approval, or
publication was invoked. Solodeveling remained the single-agent workflow;
Superpowers and subagents were not used.

WORK-017 and EVIDENCE-017 record the repaired publication gate: current protected
`main` may validate an older candidate only when it is an available ancestor, and
its canonical dynamic version is parsed without executing candidate code. Downstream
tag, immutable-release, asset, attestation, permission, and environment checks remain.
No tag, release, publish workflow, registry action, or publication was invoked.

WORK-018 and EVIDENCE-018 record that annotated tag v0.1.0 now resolves locally and
on origin to exact candidate commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
Tag-triggered CI run 29483670381 passed across tests, native targets, packaging, and
npm packaging. No GitHub Release or publish workflow run was created. WORK-019
records Memory Workflow Simplification as deferred work for the release after 0.1.0;
it is excluded from the candidate, tag target, release set, and publication inputs.

WORK-020 and EVIDENCE-020 record the non-draft immutable GitHub Release v0.1.0.
All 13 release assets passed release integrity and per-asset digest verification
after their candidate integrity and strict provenance checks passed. No publish
workflow, registry approval, token exchange, staging, bootstrap, or publication was
invoked. PyPI and npm actions remain separate authorization boundaries.

WORK-021 and EVIDENCE-021 record successful PyPI publication through protected OIDC
workflow run 29487808952. PyPI wheel and sdist digests match the immutable GitHub
Release, public provenance endpoints are available, and clean pip, uvx, pipx run,
and pipx install paths report solodeveling 0.1.0. npm was skipped and remains
unpublished. Version 0.1.0 is complete for the one-command Python installation path.
