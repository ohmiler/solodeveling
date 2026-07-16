---
solodeveling_schema: 1
id: EVIDENCE-018
work_item: WORK-018
claim: Annotated tag v0.1.0 was created and pushed at the exact verified 0.1.0 candidate commit without changing the candidate or crossing the GitHub Release or registry publication boundaries.
method: Candidate and artifact preflight, explicit local tag targeting, local and remote peeled-reference comparison, GitHub ref inspection, tag-triggered CI observation, and negative release/publication-state checks.
command: git tag -a v0.1.0 700a9b9dafc877507232b84a94ff3d6eaf7afda4; git push origin refs/tags/v0.1.0; git ls-remote origin refs/tags/v0.1.0 and its peeled ref; gh api git/ref; gh release list; gh run list for publish.yml; gh run watch 29483670381.
result: passed
scope: Local and origin tag v0.1.0, candidate commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4, candidate workflow artifact availability, and tag-triggered CI run 29483670381.
limitations:
- No immutable GitHub Release was created and no release asset was promoted from the expiring workflow artifact.
- No publish workflow, protected-environment approval, PyPI action, npm bootstrap, staging, or publication was invoked.
---

# Evidence

## Candidate and tag identity

- Candidate run 29452526223 remained successful and its complete coordinated
  release-set artifact remained available, unexpired, and scheduled to expire on
  2026-10-13.
- Before creation, origin had no v0.1.0 tag and GitHub had no release or publish run.
- The annotated tag object is 581c5e2ce7cfd3ba22a3862961ff880d13ae46cc.
- The local tag, origin peeled ref, and GitHub tag object all resolve to candidate
  commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4.

## Post-tag verification

- Tag-triggered CI run 29483670381 executed with head branch v0.1.0 and exact head
  SHA 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
- All test, native Windows/macOS/Linux x64/arm64, package, and npm-package jobs passed.
- GitHub Release listing and publish workflow listing remained empty after the tag
  push. No downstream release or registry boundary was crossed.
