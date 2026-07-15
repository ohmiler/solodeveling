# Provenance and supply-chain claims

Use supply-chain evidence when release risk, policy, or user requirements justify it.

SLSA v1.2 was the current Approved specification when checked on 2026-07-15. Resolve
the current official specification again when an exact requirement affects a
decision.

- Bind provenance to the released artifact digest and expected source revision.
- Validate producer identity, build definition, inputs, authenticity, and verification
  method. Treat downloaded attestations and signatures as untrusted until verified.
- Record an SBOM format and generation point when required, then check it describes
  the candidate rather than a nearby build.
- Never infer a SLSA level, provenance authenticity, or supply-chain safety from the
  presence of a file, badge, signature, or CI job. State the exact requirement
  evaluated, evidence, result, scope, and limitations.
