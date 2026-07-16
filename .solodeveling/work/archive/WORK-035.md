---
solodeveling_schema: 1
id: WORK-035
title: Create immutable GitHub Release v0.1.2
status: done
level: critical
type: release
goal: Create and independently verify tag v0.1.2 and its immutable GitHub Release
  from the exact verified candidate.
scope: Annotated tag at candidate SHA, non-draft non-prerelease GitHub Release, exact
  13 candidate assets, release notes, immutability, asset byte comparison, and GitHub
  release verification.
out_of_scope: PyPI publication, npm staging or publication, candidate rebuild, asset
  replacement, Pilot-4, and changes to releases 0.1.0 or 0.1.1.
acceptance:
- Annotated tag v0.1.2 peels to SHA 00efc22a01daad1cddb544b4d97ffb6a45b283fc.
- GitHub Release v0.1.2 is non-draft, non-prerelease, immutable, and contains exactly
  the verified 13 candidate assets.
- Every remote asset is byte-identical to candidate run 29521649767 and passes GitHub
  release verification.
- Release notes match the exact candidate source.
- No PyPI, npm staging, or npm publication action occurs.
risks:
- The tag and immutable release cannot be silently replaced after creation.
- A wrong or incomplete asset upload would require stopping rather than repairing
  the release in place.
- Native executables remain unsigned.
decisions:
- Use only the already verified release set downloaded from candidate run 29521649767.
- Create the annotated tag before the GitHub Release and require exact peeled SHA
  verification.
- Keep registry actions as separate future authorization boundaries.
verification:
- Reverify candidate set and repository immutability immediately before creation.
- Verify the remote tag object and peeled commit.
- Verify release state, exact asset inventory, per-asset bytes, and GitHub release
  integrity.
security_considerations:
- Bind tag, release, assets, source SHA, workflow run, checksums, and attestations
  exactly.
- Treat release API output and downloaded remote assets as untrusted until independently
  compared.
- Do not request or expose registry credentials, OTP values, or recovery codes.
recovery:
- Stop before release creation if tag identity or candidate bytes differ.
- If release creation fails before publication, preserve evidence and do not substitute
  assets from another build.
- If an immutable incorrect release is created, stop registry actions and make a new
  authorized corrective version rather than replacing bytes.
next_action: None; archived.
evidence:
- EVIDENCE-035
---
# Authorization boundary

The user authorized annotated tag `v0.1.2` at candidate SHA
`00efc22a01daad1cddb544b4d97ffb6a45b283fc` and an immutable GitHub Release
containing the verified 13-file set from run `29521649767`. This work does not
authorize PyPI or npm actions.
