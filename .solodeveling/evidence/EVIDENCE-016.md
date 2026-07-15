---
solodeveling_schema: 1
id: EVIDENCE-016
work_item: WORK-016
claim: Release candidate 0.1.0 was built once from the exact authorized main commit, passed every workflow gate, and produced an independently verified and attested complete release set without creating a tag, GitHub Release, registry action, or publication.
method: GitHub Actions observation and API inspection, release-set artifact download, local manifest and checksum verification, and per-file GitHub provenance verification with strict identity constraints.
command: gh workflow run release-candidate.yml --ref main -f source_revision=700a9b9dafc877507232b84a94ff3d6eaf7afda4; gh run watch/view; gh run download; python scripts/verify_release_set.py; gh attestation verify for every release-set file with repository, signer workflow, source digest, source ref, and hosted-runner constraints.
result: passed
scope: Version 0.1.0 candidate run 29452526223, its nine uploaded workflow artifacts, and the 13 subjects in the coordinated release set.
limitations:
- GitHub Actions artifacts expire on 2026-10-13 and have not been promoted to a durable GitHub Release.
- Native executables are not platform-signed, full Tier 1 runtime behavior remains unverified, and provenance does not prove categorical safety.
- No tag, GitHub Release, PyPI or npm registry action, environment approval, or publication was performed.
---
# Evidence

## Authorized identity

- Owner authority named version `0.1.0` and source revision
  `700a9b9dafc877507232b84a94ff3d6eaf7afda4`.
- Preflight confirmed local `main` and `origin/main` matched that revision, the worktree
  was clean, and post-merge CI run 29452201289 had passed for the same revision.
- Python and npm package metadata both resolved to version `0.1.0`.

## Candidate workflow

- Exactly one new workflow dispatch was observed: run 29452526223, event
  `workflow_dispatch`, ref `main`, source revision
  `700a9b9dafc877507232b84a94ff3d6eaf7afda4`.
- `validate-source`, `python-candidate`, all six native matrix jobs, `npm-package`, and
  `assemble` completed successfully.
- The workflow produced nine non-expired artifacts: one Python candidate, six native
  platform artifacts, one npm package, and one coordinated release set.
- The coordinated artifact digest reported by GitHub was
  `sha256:f9a7d408a0527a224570204bde62369fb906c5940798dae39d42a8350881e53b`.

## Independent release-set verification

- `python scripts/verify_release_set.py C:/tmp/solodeveling-rc-29452526223
  --source-revision 700a9b9dafc877507232b84a94ff3d6eaf7afda4` passed.
- The verified set contained 13 files: release notes, manifest, checksums, CycloneDX
  SBOM, Python sdist and wheel, npm tarball, and Linux, macOS, and Windows executables
  for x64 and arm64.
- The verifier reported: `Solodeveling 0.1.0 release set is internally consistent
  and not published`.

## Provenance and authorization boundary

- GitHub attestation verification passed separately for all 13 files while enforcing
  repository `ohmiler/solodeveling`, signer workflow
  `.github/workflows/release-candidate.yml`, `refs/heads/main`, the exact source
  digest, and denial of self-hosted runners.
- No version tag points to the candidate, no GitHub Release exists, and no PyPI or npm
  staging, approval, token exchange, or publication was authorized or performed.
