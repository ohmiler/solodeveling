# Dependencies and vulnerabilities

## Dependency change

- Identify package, expected source or registry, current or affected version, target
  version, direct or transitive path, runtime use, and supported platform range.
- Read current ecosystem or vendor release notes and advisories when freshness
  matters. Validate identity and integrity; do not trust a package name or generated
  update command alone.
- Review compatibility, removed behavior, configuration, permissions, license or
  policy constraints when applicable. Update the lockfile with the manifest.
- Run focused behavior and security regressions, then the broadest practical build,
  test, package, and platform checks. Define rollback or pinning before release.

## Vulnerability triage

First establish whether the installed artifact and affected version range match.
Then assess reachability, runtime exposure, privilege and data impact, compensating
controls, exploit evidence, and confidence. A scanner match is a lead, not proof.

Use current native ecosystem and vendor advisories. OSV supplies a machine-readable
cross-ecosystem format; schema 1.8.0 was current when checked on 2026-07-15. CISA KEV
is an authoritative living catalog of vulnerabilities known to be exploited in the
wild and a strong prioritization input. Recheck living sources when making a current
decision.

Prioritize from affected evidence, exposure, exploitability, impact, and remediation
risk—not a score alone or CISA KEV absence. Record advisory identifiers, timestamps,
source links, uncertainty, mitigation, target version, owner, due or review condition,
verification, and rollback. Never claim absence of vulnerability from one database.
