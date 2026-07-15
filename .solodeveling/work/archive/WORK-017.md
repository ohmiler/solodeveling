---
solodeveling_schema: 1
id: WORK-017
title: Repair publication candidate ancestry gate
status: done
level: critical
type: repair
goal: Allow the current protected main publication workflow to publish the already verified 0.1.0 candidate while preserving exact candidate identity and rejecting untrusted source revisions.
scope: Reproduce and repair the source-revision equality defect and dynamic-version lookup defect in publish.yml; add executable or focused regression coverage; update release guidance and project evidence.
out_of_scope: Creating or pushing v0.1.0, creating a GitHub Release, invoking publish.yml, changing registry environments, staging or publishing either package, rebuilding or replacing the verified candidate.
acceptance:
- The publication workflow continues to require execution from refs/heads/main and validates inputs before any registry job.
- A candidate source revision is accepted only when it is a valid commit reachable as an ancestor of the current main workflow revision.
- An unrelated, descendant, malformed, or missing source revision is rejected before tag, release, or registry work.
- Package version validation reads the canonical dynamic version source and matches the requested version.
- Existing tag, immutable release, release-set hash, inventory, attestation, environment, and least-privilege gates remain intact.
- Focused regressions, the full suite, protocol validation, skill validation, and CI pass without creating a tag, release, or publication run.
risks:
- Relaxing equality without proving ancestry could allow a candidate outside reviewed main history.
- A text-only workflow assertion could miss shell behavior or quoting defects.
- Advancing main changes the workflow revision but must not alter the verified candidate bytes or identity.
decisions:
- Run the current publication workflow from protected main and accept an older candidate only when Git proves it is an ancestor of that exact workflow revision.
- Preserve the verified candidate revision and artifact attestations; do not rebuild solely because evidence documentation advanced main.
- Read version from src/solodeveling_protocol/__init__.py through the package module instead of nonexistent static project.version metadata.
verification:
- Add failing regressions for ancestry enforcement and dynamic-version lookup before implementation.
- Exercise accepted ancestor and rejected unrelated, descendant, malformed, and missing revision cases.
- Confirm all prior publication security assertions and the full project gate pass.
next_action: Obtain fresh explicit owner authorization before creating tag v0.1.0 at the verified candidate commit; GitHub Release creation and publication remain separate.
security_considerations:
- The current workflow revision remains bound to refs/heads/main; only candidate identity is decoupled from current HEAD.
- Existing exact tag, immutable GitHub Release, verified assets, provenance signer, source digest, source ref, hosted-runner, and protected-environment checks must remain unchanged.
recovery:
- Revert the workflow repair before any tag or release if ancestry or version regressions fail.
- If a later authorized dry validation exposes a new mismatch, stop before protected environment approval and keep registries untouched.
evidence:
- EVIDENCE-017
---
# Execution plan

1. Capture failing regressions for the two observed defects.
2. Implement the smallest ancestry and dynamic-version repair.
3. Run focused adversarial cases and the complete project gate.
4. Record evidence and merge through reviewed CI, then request fresh tag authority.
