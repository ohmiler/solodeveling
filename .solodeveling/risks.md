---
solodeveling_schema: 1
---
# Risks

- Released versions through 0.3.0 are immutable across GitHub, PyPI, and npm; corrections require a newly reviewed version and a complete rebuilt release set.
- Release 0.3.0 is bound to explicitly approved `main` commit `1bdfadd137c30f64b4d6308fe49975e81988644d`; later source commits do not alter its published bytes or provenance.
- Checksums, manifests, SBOM, and GitHub artifact attestation provide bounded integrity and provenance evidence only; they do not sign platform executables, prove safety, or establish a SLSA level by themselves.
- GitHub environments protect registry jobs; PyPI OIDC and npm stage-only Trusted Publishing have passed production releases, but owner proof-of-presence remains required to approve every staged npm version.
- Version 0.3.0 shipped with an owner-accepted missing live routing result after tenant policy blocked the three-call pilot; deterministic tests do not prove stable behavior across models, repetitions, or sessions.
- cursor-agent is unavailable locally, so Cursor behavior and complete Tier 1 support remain unverified.
- Co-installing native runtime adapters may surface duplicate skills in clients that scan compatibility paths.
- High-confidence secret detection is a bounded output and project-memory safeguard, not a complete repository scanner.
- Security standards, runtime CLIs, structured-output schema subsets, authentication, and billing behavior evolve; exact claims require current primary-source verification.
- Adjacent workflow projects change independently, and comparative speed or quality claims remain unsupported until a controlled repeated benchmark exists.
- A methodology benchmark can execute the model without activating the named workflow if project-local skills are installed outside the runtime adapter path; live evidence must verify the adapter path and reject zero-activation results.
- A Codex process may return zero even when sandboxed tool commands cannot mutate the workspace; Windows live evaluation must verify the sandbox helper before inference and stop after the first zero-mutation execution.
