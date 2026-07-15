---
solodeveling_schema: 1
id: WORK-016
title: Produce and verify release candidate 0.1.0
status: done
level: critical
type: change
goal: Produce one non-publishing release candidate for version 0.1.0 from the exact owner-authorized main commit and verify its integrity and provenance.
scope: Preflight the authorized version and source revision; invoke release-candidate.yml once; observe all jobs; download and independently verify the complete release set and every GitHub artifact attestation; reconcile release memory.
out_of_scope: Creating or pushing a tag, creating a GitHub Release, publishing to PyPI or npm, configuring or weakening registry environments, approving a deployment, or claiming platform code signing, complete Tier 1 behavior, or categorical security.
acceptance:
- Exactly one release-candidate workflow run succeeds for version 0.1.0 from source revision 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
- The coordinated release set contains the expected Python distributions, six native executables, npm tarball, SBOM, release notes, checksums, and manifest.
- Independent local verification confirms the release-set manifest, sizes, hashes, version, and source revision.
- GitHub provenance verification succeeds for every release-set subject with the expected repository, signer workflow, main ref, source revision, and GitHub-hosted runner policy.
- No tag, GitHub Release, registry staging, approval, or publication occurs.
risks:
- Artifact retention is finite and a workflow artifact is not a durable public release.
- Attestation and checksums prove bounded provenance and integrity, not software safety or platform code signing.
- The public package names remain unreserved until first publication.
decisions:
- Treat workflow run 29452526223 as the only authorized 0.1.0 release candidate for source revision 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
- Keep tag creation, immutable GitHub Release creation, registry actions, and publication behind separate explicit authorization checkpoints.
verification:
- Inspect workflow and artifact metadata through GitHub APIs.
- Download the complete release-set artifact and run verify_release_set.py against the authorized source revision.
- Verify all 13 artifact attestations with repository, signer workflow, source ref, source digest, and hosted-runner constraints.
next_action: Obtain separate explicit owner authorization before creating tag v0.1.0 at source revision 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
security_considerations:
- The candidate workflow used read-only repository permission except scoped id-token and attestations write permission in the assemble job.
- Verification required the expected GitHub repository and signer workflow, refs/heads/main, the exact source digest, and denial of self-hosted runners.
recovery:
- Before publication, discard an invalid or expired workflow artifact and rebuild the entire set from a newly reviewed and explicitly authorized commit; never replace individual files or edit manifests.
- If an externally visible tag or release is later created incorrectly, stop before publication and use the separately approved recovery procedure for that external action.
evidence:
- EVIDENCE-016
---
# Execution plan

1. Confirm version 0.1.0, clean main, exact source revision, and successful post-merge CI.
2. Dispatch the authorized non-publishing workflow exactly once and observe every job.
3. Independently verify the downloaded complete release set and all provenance subjects.
4. Reconcile memory and stop at the next external authorization boundary.
