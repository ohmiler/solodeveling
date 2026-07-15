---
solodeveling_schema: 1
id: WORK-010
title: Assemble one verified cross-ecosystem release set
status: done
level: critical
type: change
goal: Produce one non-publishing release set that binds Python distributions, six native executables, the npm tarball, evidence, version, and exact source revision before any external release action.
scope: Add fail-closed release-set assembly and verification, a manually dispatched least-privilege GitHub workflow, regression tests, documentation, and project evidence.
out_of_scope: Creating a tag or GitHub Release, configuring registry identities or protected environments, signing platform executables, publishing to npm or PyPI, or claiming complete Tier 1 runtime behavior.
acceptance:
- Assembly accepts exactly one verified Python candidate, six expected native executables, and one npm tarball whose embedded manifest matches every native filename, size, and SHA-256.
- One release-set manifest binds version, exact lowercase 40-character source revision, artifact roles, sizes, and SHA-256 values without timestamps or mutable URLs.
- Verification rejects missing, extra, symlinked, duplicated, path-traversing, version-drifted, revision-drifted, size-mismatched, or hash-mismatched inputs before any artifact is treated as releasable.
- A manual GitHub Actions workflow builds the complete set from one requested commit with pinned actions and least privilege, attests exact subjects, uploads only temporary artifacts, and contains no tag, GitHub Release, or registry publication command.
- Documentation distinguishes a verified non-publishing assembly from a signed, published, or behavior-complete release and defines recovery by rebuilding the whole set.
- Focused tests, the full suite, skill/protocol validation, package checks, workflow inspection, and clean diff review pass.
risks:
- Cross-job artifact mixing could bind binaries or packages from different source revisions.
- npm could reference a missing or different native executable and fail only after publication.
- Generated manifests, archive paths, symlinks, or duplicate filenames could cross a filesystem or execution trust boundary.
- Attestation presence could be overstated as proof of safety or a SLSA level.
decisions:
- Keep release assembly non-publishing and manually dispatched from an exact commit SHA.
- Copy verified inputs into a fresh output directory and describe only flat, version-bound filenames.
- Treat the complete release set as indivisible; rebuild all artifacts after any source, version, inventory, or digest change.
- Keep registry configuration, tag creation, GitHub Release creation, signing, and publication behind separate explicit authorization.
verification:
- Begin with regression tests for exact inventory, npm/native binding, source/version identity, path safety, symlink rejection, tampering, and deterministic manifests.
- Exercise assembly and verification using safe fixture artifacts, then run all Python and Node tests.
- Inspect the workflow for manual-only triggers, pinned action SHAs, bounded permissions, exact subject attestation, and absence of publishing commands.
- Run skill suite validation, protocol validation, compileall, dependency health, and diff/status review.
next_action: Review and integrate pull request 10; separately authorize any manual attestation, tag, release, registry configuration, or publication.
security_considerations:
- Inputs and downloaded CI artifacts are untrusted until inventory, containment, size, and SHA-256 checks pass.
- Do not execute artifacts during assembly; native smoke and npm execution remain isolated upstream gates.
- Do not grant contents write, packages write, registry tokens, or release mutation permissions to the assembly workflow.
- Record attestation as bounded provenance evidence, not categorical security or an inferred SLSA level.
recovery:
- Delete only disposable assembly output and rebuild the entire set from the reviewed exact commit.
- Never repair a release set by editing generated manifests, replacing individual files, or reusing artifacts from another run.
- Preserve the last known-good main commit and keep all external release actions unperformed in this work item.
evidence:
- EVIDENCE-010
---

# Implementation plan

1. Reconcile merged WORK-009 state and create the Critical WORK-010 checkpoint.
2. Add regression coverage for a deterministic, fail-closed complete release-set contract.
3. Implement assembly and verification scripts that bind Python, native, and npm artifacts to one version and source revision.
4. Add a manual least-privilege workflow that builds, verifies, attests, and temporarily uploads the complete set without publishing.
5. Update release documentation, run the full gate, record evidence, and integrate through review.
