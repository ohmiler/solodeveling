# Standards status and use

Status checked 2026-07-15. Verify the official source again when current control text
or version affects a decision.

- **NIST SSDF:** SP 800-218 / SSDF 1.1 is Final and is the outcome-oriented baseline.
  SP 800-218 Rev. 1 / SSDF 1.2 is Draft; do not present draft content as final.
  For generative AI and dual-use foundation models, SP 800-218A is a Final community
  profile. Source: https://csrc.nist.gov/Projects/ssdf/publications
- **OWASP SAMM:** version 2 is a living, development-model-neutral maturity model
  spanning Governance, Design, Implementation, Verification, and Operations. Use it
  for lifecycle coverage, not as a claim of certification.
  Source: https://owaspsamm.org/model/
- **OWASP ASVS:** 5.0.0 is the stable application verification release at this check.
  Version requirement identifiers as `v<version>-<identifier>` because identifiers
  can change. Source:
  https://owasp.org/www-project-application-security-verification-standard/
- **OWASP MASVS:** use the current online control groups with MASTG/MASWE evidence.
  MASVS 2.0.0 and later no longer contain the legacy verification levels; select
  testing profiles from current official guidance. Source: https://mas.owasp.org/MASVS/
- **OWASP SCVS:** use its inventory, SBOM, build environment, package management,
  component analysis, and provenance families for supply-chain work.
  Source: https://scvs.owasp.org/
- **OWASP Agentic Security:** use current threat guidance for AI-agentic systems,
  including goal manipulation, tool misuse, identity and privilege, supply chain,
  unexpected code execution, and memory/context poisoning. Source:
  https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/

Standards inform requirements and evidence. They do not replace project-specific
threat analysis, authorization, legal advice, or verified behavior.