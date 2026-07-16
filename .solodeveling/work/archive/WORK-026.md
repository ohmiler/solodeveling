---
solodeveling_schema: 1
id: WORK-026
title: npm Publication 0.1.0
status: done
level: critical
type: release
goal: Publish exact verified package solodeveling@0.1.0 to the public npm registry, verify clean npx installation, and configure secure trusted publishing for later releases.
scope: npm account/name/2FA preflight, exact immutable release tarball verification, owner-controlled interactive first publication, registry digest and ownership verification, clean npx smoke, stage-only GitHub Actions trusted publisher for publish.yml environment npm, token restriction where available, and durable evidence.
out_of_scope: Any rebuild or replacement of candidate artifacts, PyPI changes, version changes, npm tokens, direct CI bootstrap, source/package modifications, a new tag or GitHub Release, and publication of any version other than 0.1.0.
acceptance:
- The operator is authenticated as the intended npm owner with 2FA capable of interactive publication, and the unscoped name is still unpublished immediately before execution.
- The sole publication input is the npm tarball from immutable GitHub Release v0.1.0, with release digest, candidate manifest, checksum, inventory, and strict attestation verification passing for source commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
- Dry-run inspection reports exact name solodeveling, version 0.1.0, public access intent, expected launcher files, and no unexpected or secret material.
- Explicitly authorized owner-controlled npm publish with 2FA creates public solodeveling@0.1.0 exactly once; no token or CI bootstrap is used.
- Registry metadata, tarball integrity and digest match the verified publication input, and package ownership includes the intended owner.
- Clean npm install and npx execution outside the checkout report solodeveling 0.1.0 and retrieve the matching versioned native asset.
- A GitHub Actions trusted publisher is configured for ohmiler/solodeveling, publish.yml, environment npm, with stage-only permission for later releases; traditional publishing tokens are disallowed when the registry permits that setting.
- Project memory records exact actions, results, limitations, recovery, and the unchanged v0.1.0 source boundary.
risks:
- npm package name and version publication are externally visible and cannot be replaced with different bytes.
- Interactive authentication or 2FA failure could leave the name unpublished or the post-publication configuration incomplete.
- A wrong tarball, registry, account, access mode, trust claim, or permission could create a supply-chain ownership or distribution incident.
- Native executables remain unsigned and the npm launcher downloads platform assets from the immutable GitHub Release.
decisions:
- User authorized public npm publication of solodeveling@0.1.0 in this conversation.
- Bootstrap interactively from the verified GitHub Release tarball; never rebuild or use a token.
- Configure later automation for npm stage publish only, preserving owner proof-of-presence before public availability.
- Stop before publication on any identity, digest, inventory, attestation, 2FA, or registry mismatch.
verification:
- Verify npm CLI/account/name state without exposing credentials.
- Verify the exact GitHub Release tarball and full release set before dry-run or publication.
- Compare npm registry integrity/digest to local bytes after publication and run clean install/npx smoke tests.
- Inspect trusted publisher and publishing-access configuration after setup.
next_action: Preserve the immutable 0.1.0 evidence and use the stage-only Trusted Publisher flow for a separately authorized later release.
security_considerations:
- Use interactive 2FA and no automation token for bootstrap.
- Do not display npm credentials, OTP values, recovery codes, or private account fields.
- Prefer stage-only OIDC trust and disallow traditional publishing tokens after configuration.
- Preserve immutable release, attestations, least-privilege GitHub environment, and exact repository/workflow/environment claims.
recovery:
- Before publication, stop and discard only temporary verified downloads if any check fails.
- After an incorrect publication, preserve evidence, immediately deprecate the affected version, stop further release actions, and publish a corrected new version only after separate authorization.
- If trusted publishing setup fails after correct publication, leave 0.1.0 public, retain interactive owner control, and complete trust configuration before any later npm release.
evidence:
- EVIDENCE-026
---

# Execution plan

1. Confirm npm CLI capability, intended owner authentication, 2FA readiness, public
   name absence, registry health, and exact release identity.
2. Download the immutable release set into a disposable directory and re-run release,
   digest, inventory, attestation, and npm dry-run checks.
3. Publish only the verified `.tgz` interactively with owner 2FA, then observe registry
   metadata and clean user journeys.
4. Configure stage-only trusted publishing for `publish.yml` and environment `npm`,
   restrict token publishing where supported, and inspect the saved claims.
5. Record evidence, reconcile state, and close only when all acceptance criteria pass
   or an explicit limitation remains.
