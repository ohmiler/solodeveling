---
solodeveling_schema: 1
id: WORK-036
title: Publish and fresh-install verify Solodeveling 0.1.2
status: done
level: critical
type: release
goal: Publish the exact verified 0.1.2 candidate to PyPI and npm and prove clean installation.
scope: Protected PyPI publication, npm staging and owner approval, public digest and provenance checks, and clean pip and npx smoke tests.
out_of_scope: Candidate rebuild or change, immutable-byte replacement, another version, policy weakening, or credential handling.
acceptance:
- PyPI and npm publish only 0.1.2 from SHA 00efc22a01daad1cddb544b4d97ffb6a45b283fc and candidate run 29521649767.
- Public wheel, sdist, and npm tarball match the immutable release.
- npm is staged and byte-verified before approval and latest then resolves to 0.1.2.
- Clean pip and npx version, install, and check paths pass without a source checkout.
risks:
- Registry bytes are immutable after publication.
- Native executables remain unsigned.
decisions:
- Use only the immutable 13-file v0.1.2 release set.
- Use protected OIDC and npm staged owner review.
- Approve stage e02400e1-a1c1-41b2-b325-ec609d88d36d only after exact digest comparison.
verification:
- Preflighted tag, release, assets, attestations, registries, and workflow inputs.
- Observed run 29524805137 and compared public registry files.
- Ran clean pip and npx version, install, and check paths.
security_considerations:
- Bound version, source, workflow, assets, checksums, attestations, stage, and registry bytes.
- Recorded no token, OTP, session data, or recovery code.
recovery:
- Yank or deprecate a bad version where appropriate and issue a corrected version.
next_action: None; archived.
evidence:
- EVIDENCE-036
---
# Authorization

The user authorized PyPI and npm publication plus fresh-install verification from
candidate SHA 00efc22a01daad1cddb544b4d97ffb6a45b283fc. npm was staged and
byte-verified before owner approval.
