---
solodeveling_schema: 1
---
# Risks

- Candidate 0.1.0 is bound to explicitly approved `main` commit `700a9b9dafc877507232b84a94ff3d6eaf7afda4`; any replacement candidate must rebuild the entire set from a newly reviewed and explicitly approved commit.
- Candidate workflow artifacts expire on 2026-10-13 and are not a durable GitHub Release.
- Checksums, manifests, SBOM, and GitHub artifact attestation provide bounded integrity and provenance evidence only; they do not sign platform executables, prove safety, or establish a SLSA level by themselves.
- npm and PyPI names are not reserved and availability can change before publication. GitHub environments are protected; the PyPI pending publisher is owner-confirmed but public verification and first-use OIDC matching remain unavailable, while npm Trusted Publishing awaits the first npm publication.
- One representative live scenario does not prove stable behavior across the full core matrix, model versions, repetitions, or sessions.
- cursor-agent is unavailable locally, so Cursor behavior and complete Tier 1 support remain unverified.
- Co-installing native runtime adapters may surface duplicate skills in clients that scan compatibility paths.
- High-confidence secret detection is a bounded output and project-memory safeguard, not a complete repository scanner.
- Security standards, runtime CLIs, structured-output schema subsets, authentication, and billing behavior evolve; exact claims require current primary-source verification.
