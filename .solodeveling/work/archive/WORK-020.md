---
solodeveling_schema: 1
id: WORK-020
title: Create immutable GitHub Release v0.1.0
status: done
level: critical
type: release
goal: Promote the exact verified 0.1.0 candidate into a non-draft immutable GitHub Release with all 13 coordinated release-set files.
scope: Download candidate artifact 8358101583 from run 29452526223; independently verify inventory, hashes, version, source revision, and attestations; create GitHub Release v0.1.0 from the existing exact tag; verify immutability and every uploaded asset.
out_of_scope: Rebuilding or changing the candidate, invoking publish.yml, approving environments, or publishing to PyPI or npm.
acceptance:
- The downloaded 13-file release set passes exact source, inventory, size, hash, and version verification.
- Provenance verification passes for every file against the expected repository, workflow, source ref, source digest, and GitHub-hosted runner policy.
- GitHub Release v0.1.0 is non-draft, immutable, targets tag v0.1.0, and contains exactly the verified 13 assets.
- No registry workflow, approval, token exchange, staging, or publication occurs.
risks:
- An incorrect immutable release cannot be edited after publication and would require an explicitly authorized recovery decision.
- Candidate workflow artifacts expire on 2026-10-13 and must not be replaced file-by-file.
decisions:
- Use only the coordinated release-set artifact from authorized run 29452526223.
- Stop after GitHub Release verification; registry publication remains separately authorized.
verification:
- Run verify_release_set.py against exact candidate commit.
- Run strict gh attestation verify for each of the 13 subjects.
- Verify release immutability, tag identity, asset count, names, sizes, digests, and GitHub release integrity.
next_action: Obtain separate explicit owner authorization for each registry action; PyPI publication and npm first-package bootstrap remain distinct boundaries.
security_considerations:
- Treat every downloaded file and manifest as untrusted until hashes and attestations pass.
- Do not expose tokens or grant registry permissions.
recovery:
- Before release creation, discard the temporary download on any mismatch.
- After creation, stop and preserve evidence on any unexpected identity or asset result; do not replace immutable assets or proceed to publication.
evidence:
- EVIDENCE-020
---

# Execution plan

1. Reconfirm tag, candidate run, artifact identity, and absent release state.
2. Download and verify the complete release set and all attestations.
3. Create the non-draft GitHub Release once from the existing tag and exact files.
4. Verify immutability, release integrity, asset inventory, and unchanged registry state.
5. Reconcile project memory and stop at the registry-publication boundary.
