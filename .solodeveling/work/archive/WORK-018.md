---
solodeveling_schema: 1
id: WORK-018
title: Establish the 0.1.0 tag boundary
status: done
level: critical
type: release
goal: Create and push tag v0.1.0 at the exact verified candidate commit without changing the candidate or crossing the GitHub Release or registry publication boundaries.
scope: Reconfirm candidate identity and artifact availability; create annotated tag v0.1.0 at 700a9b9dafc877507232b84a94ff3d6eaf7afda4; push the tag; verify the remote tag target; record bounded evidence and the next authorization checkpoint.
out_of_scope: Rebuilding or modifying the candidate, creating a GitHub Release, invoking publish.yml, approving a protected environment, or publishing to PyPI or npm.
acceptance:
- Local and remote tag v0.1.0 resolve to candidate commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
- The verified release-set artifact from run 29452526223 remains available and unchanged.
- No GitHub Release, publish workflow run, environment approval, or registry publication is created.
- Project memory records the tag evidence and preserves separate authorization for the next release boundary.
risks:
- An incorrect public tag would expose the wrong source identity and require an explicitly authorized recovery action.
- Advancing release state without preserving candidate identity could detach later publication from verified artifacts.
decisions:
- Target the exact candidate SHA explicitly; do not tag the current main revision or working tree.
- Stop after remote tag verification because GitHub Release creation and publication remain separate authority checkpoints.
verification:
- Resolve the peeled local and remote tag target and compare it with the exact candidate SHA.
- Re-read GitHub Releases and publish workflow runs after the push.
- Validate project memory after recording the result.
next_action: Obtain separate explicit owner authorization before creating the immutable, non-draft GitHub Release from the exact verified release set.
security_considerations:
- Tag creation uses the reviewed candidate identity and does not grant registry permissions or execute candidate code.
recovery:
- Stop before GitHub Release creation or publication if the remote tag identity differs; preserve evidence and request explicit authority before changing an externally visible tag.
evidence:
- EVIDENCE-018
---

# Execution plan

1. Reconfirm the exact candidate, artifact availability, and absent tag/release state.
2. Create and verify the annotated tag against the candidate SHA.
3. Push the tag and independently verify the remote target and unchanged downstream state.
4. Record evidence, archive the completed tag work, and stop at the GitHub Release boundary.
