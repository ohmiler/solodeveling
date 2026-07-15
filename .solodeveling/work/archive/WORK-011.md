---
solodeveling_schema: 1
id: WORK-011
title: Prepare guarded PyPI and npm publication workflow
status: done
level: critical
type: change
goal: Make public registry publication reproducible from one verified and attested GitHub Release while keeping every real publication behind explicit owner action and protected environments.
scope: Add deterministic publication-input preparation and verification, a manual GitHub Actions workflow for PyPI OIDC and existing-package npm OIDC stage/direct actions, policy regression tests, and owner setup/runbook documentation.
out_of_scope: Invoking either workflow, creating GitHub environments, configuring registry Trusted Publishers, bootstrapping or publishing the first npm version, creating a tag or GitHub Release, approving an npm staged package, signing native executables, or uploading any package.
acceptance:
- Publication preparation accepts only a complete verified release set for an exact source revision and emits exactly one wheel, one sdist, and one npm tarball with a deterministic plan that preserves their size and SHA-256.
- A manual-only workflow requires exact version, lowercase 40-character source revision, and an exact human confirmation string before downloading an existing non-draft v<version> GitHub Release.
- The workflow proves the tag resolves to the requested revision, verifies every downloaded release-set file and its GitHub attestation against the repository and signer workflow, and re-verifies inputs after job artifact transfer.
- PyPI publication uses a protected pypi environment and OIDC with a full-SHA-pinned official action; no PyPI token or secret is accepted.
- npm actions use a protected npm environment, OIDC, Node 24, npm 11.15.0, and separate guarded skip/stage/publish choices without shell-evaluating user input or accepting an npm token.
- Documentation states that PyPI can bootstrap through a pending publisher, npm 0.1.0 requires an owner-controlled first publish because the package does not yet exist, and no registry name is reserved before successful publication.
- Tests and static policy checks reject automatic triggers, mutable action refs, write permissions outside publisher jobs, missing environments, secret-token fallbacks, unverified release inputs, and unguarded publish commands.
- No workflow invocation, environment mutation, registry configuration, tag, release, attestation, stage, approval, or publication occurs in WORK-011.
risks:
- A publish workflow turns repository write access or workflow modification into a registry supply-chain boundary.
- A mutable, mismatched, draft, unattested, or incomplete GitHub Release could publish bytes that differ from the reviewed candidate.
- Shell interpolation of workflow inputs could allow command injection on privileged runners.
- npm first-package bootstrap cannot use staged publishing and must not silently introduce a long-lived automation token.
- Publishing npm before its exact native assets exist at releases/download/v<version> would produce an installable but unusable package.
decisions:
- Publish only from an already-created non-draft GitHub Release whose tag, manifest, source revision, hashes, and attestations all verify.
- Keep validation globally read-only and grant id-token write only to registry jobs that reference named protected environments.
- Use boolean/choice workflow conditions instead of interpolating registry actions into shell commands.
- Use PyPI pending Trusted Publisher for first creation; document npm first-release bootstrap as a separate owner-authorized interactive 2FA action from the verified tarball.
- Prefer npm stage publish for versions after bootstrap; retain direct publish as an explicit environment-gated choice for emergencies or deliberate releases.
verification:
- Begin with failing fixture tests for exact publication inventory, plan tampering, source/version drift, and output containment.
- Add static workflow tests for manual-only trigger, exact confirmation, release/tag/attestation checks, pinned actions, least permissions, protected environments, OIDC-only credentials, and guarded npm actions.
- Run focused tests, full Python and Node suites, official skill validators, protocol validation, compileall, dependency health, YAML parsing, and diff review.
next_action: Obtain explicit owner authorization before enabling immutable releases or configuring protected registry environments; all candidate, tag, release, and publication actions remain separate.
security_considerations:
- Treat GitHub Release files, manifests, attestations, workflow inputs, and downloaded job artifacts as untrusted until exact identity and digest verification succeeds.
- Do not expose or accept long-lived registry tokens; OIDC trust must bind repository, workflow filename, environment, and protected branch/tag policy.
- Do not run third-party code from the release set during validation; publishing jobs upload only the three selected package archives.
- Attestation verification must bind the expected repository and exact signer workflow, not only the artifact digest.
recovery:
- Before publication, cancel the workflow and discard temporary artifacts; rebuild the entire release set when any identity or digest differs.
- After an incorrect PyPI release, preserve evidence and yank the version where appropriate; after an incorrect npm release, deprecate the version and publish a corrected new version rather than replacing bytes.
- Remove or disable the relevant Trusted Publisher and environment authorization during a credential or workflow compromise investigation.
evidence:
- EVIDENCE-011
---

# Implementation plan

1. Create and activate the Critical publication-preparation checkpoint without granting publication authority.
2. Add regression tests for exact publication input selection, plan verification, tampering, and workflow permission/trigger guards.
3. Implement publication preparation/verification and a manual GitHub Release-to-registry workflow with separate PyPI and npm environments.
4. Document owner-only PyPI pending-publisher setup, npm first-release bootstrap, staged publishing, recovery, and post-publication smoke.
5. Run the complete verification gate, record limitations, and integrate through review without invoking the workflow.