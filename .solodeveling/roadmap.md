---
solodeveling_schema: 1
---
# Roadmap

1. Protocol foundation - implemented on `feat/protocol-foundation`.
2. Core router and onboarding - implemented on `feat/core-router-onboarding`.
3. Shaping, planning, execution, debugging, and verification workflows - implemented as WORK-002.
4. Secure SDLC baseline and security routing - implemented as WORK-003.
5. Release and maintenance workflows - implemented as WORK-004.
6. Runtime adapters - implemented as WORK-005.
7. Cross-agent behavioral evaluation - deterministic harness and bounded representative Codex/Claude live evidence implemented as WORK-006; full Tier 1 matrix remains unverified.
8. Public packaging, installation UX, and release readiness - implemented as WORK-007 and merged into `main`; later explicitly authorized work published versions 0.1.0 and 0.1.1.
9. Source-bound 0.1.0 candidate, CycloneDX SBOM, and manual provenance gate - implemented as WORK-008 and merged through pull request 8; first invoked and verified as WORK-016.
10. One public `solodeveling` name across Python, npm, native executables, and runtime installation - implemented as WORK-009 and merged through pull request 9.
11. Verified cross-ecosystem release-set assembly - implemented as WORK-010 and merged through pull request 10; the complete attested main release set was produced and verified as WORK-016.
12. Guarded PyPI and npm publication workflow - implemented as WORK-011 and merged through pull request 11; protected PyPI OIDC and stage-only npm Trusted Publishing are now verified in production.
13. Zero-config project installation, check, and uninstall - implemented as WORK-012 and merged through pull request 12.
14. Pre-release documentation reconciliation - implemented as WORK-013 and verified through pull request 13; no candidate, tag, GitHub Release, registry setup, or publication was authorized by this work.
15. Owner-controlled GitHub release prerequisites - implemented as WORK-014 and verified through pull request 14; immutable releases and protected pypi/npm environments are configured without invoking release workflows.
16. Owner release-setup verification - implemented as WORK-015; admin bypass is API-verified disabled and the PyPI pending publisher is owner-confirmed without invoking release workflows.
17. Non-publishing 0.1.0 release candidate - produced and independently verified as WORK-016 from exact main commit `700a9b9dafc877507232b84a94ff3d6eaf7afda4`; tag, GitHub Release, registry actions, and publication remain separately authorized work.
18. Publication candidate ancestry repair - implemented and verified as WORK-017; current protected `main` can validate the exact verified ancestor candidate without weakening tag, release, provenance, or registry gates.
19. Memory Workflow Simplification - implemented and locally verified as WORK-019 with progressive persistence, compact current state, validator enforcement, impact-based verification, and fail-safe memory-only CI; the 0.1.0 candidate and release set remain unchanged.
20. Immutable GitHub Release v0.1.0 - created and verified as WORK-020 with all 13 exact candidate assets; PyPI and npm actions remain separately authorized.
21. PyPI publication 0.1.0 - published and verified as WORK-021 through protected OIDC; clean pip, uvx, and pipx paths pass, while npm remains deferred and unpublished.
22. Narrow docs-only CI path - implemented and GitHub-verified as WORK-025; changes strictly under docs/** run one complete Python regression job with exact diff checking, while mixed and non-docs changes retain the full gate.
23. npm publication 0.1.0 - published and verified as WORK-026 from the exact immutable release tarball; clean install and npx paths pass, with later automation restricted to owner-reviewed staged Trusted Publishing and traditional publishing tokens disallowed.
24. README positioning and honest comparison - implemented and GitHub-verified as WORK-027 with live installation guidance, risk-scaled value, a documented-default comparison table, best-fit guidance, measured workflow-overhead evidence, and explicit competitive benchmark limits.
25. Registry landing pages and patch release 0.1.1 - implemented, published, and independently verified as WORK-028 from exact source commit `889e07a47a8cbdca15765d00348dbbd7f9849f03`; immutable GitHub, PyPI OIDC, npm staged Trusted Publishing, registry digests, provenance, and clean pip/npx paths pass.
26. Controlled comparison recovery - deterministic harness implemented as WORK-029; pilot-1 archived as invalid runtime evidence by WORK-030; pilot-2 archived as invalid methodology-activation evidence by WORK-031 after 18 inference processes found a project skill-path mismatch; corrected pilot-3 is preregistered but not run.
27. Comparative execution-sandbox recovery - Pilot-3 completed 18 inference processes but produced zero mutations while the local Codex Windows sandbox helper was unavailable; WORK-032 archives it as invalid evidence, adds a missing-helper preflight and zero-mutation circuit breaker, and preregisters blocked Pilot-4 without live execution.

The approved delivery sequence remains authoritative in
`docs/superpowers/specs/2026-07-15-solodeveling-design.md`.
