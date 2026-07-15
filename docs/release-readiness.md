# Release readiness

WORK-007 prepares reviewable artifacts but does not publish them. Python packaging
guidance recommends distributing both a wheel and source distribution, while GitHub
recommends immutable full-SHA action pins and least-privilege workflow permissions.
See the [PyPA package formats guide](https://packaging.python.org/en/latest/discussions/package-formats/)
and [GitHub secure use reference](https://docs.github.com/en/actions/reference/security/secure-use).

## Local release gate

1. Run the full test, suite, official skill, protocol, compilation, dependency, and
   diff checks.
2. Build into a path that does not already exist:

       python scripts/build_release.py C:\tmp\solodeveling-release

3. Verify checksums, archive structure, canonical resource bytes, metadata, and entry
   points:

       python scripts/verify_release.py C:\tmp\solodeveling-release

4. Install the wheel in a fresh virtual environment outside the checkout and run all
   four console commands plus adapter install/check/uninstall for every runtime
   mapping.
5. Review `release-manifest.json` and `SHA256SUMS`. Checksums are integrity evidence,
   not a signature, attestation, or proof of publisher identity.

The builder refuses an existing output directory, builds in temporary staging, emits
exactly one wheel and one sdist, writes a deterministic manifest without timestamps,
and never uploads, tags, signs, merges, or creates a release.

## Evidence checked 2026-07-15

- Windows with Python 3.14: full installed-wheel smoke passed from a fresh virtual
  environment outside the checkout for Codex, Claude Code, Cursor, and generic adapter
  mappings. No agent was called.
- Dependency audit: `pip-audit` 2.10.1 reported no known vulnerabilities in installed
  dependencies. The unpublished `solodeveling-protocol` package itself was skipped
  because it was not found on PyPI.
- PyPI name lookup: `solodeveling-protocol` returned HTTP 404. This is not a reservation
  and can change before publication.
- GitHub repository: public, Apache-2.0, default branch `main`, no releases, no existing
  workflows before WORK-007, blank description, and no topics at the time checked.
- GitHub Actions: push run
  [29426760418](https://github.com/ohmiler/solodeveling/actions/runs/29426760418)
  and pull-request run
  [29426763270](https://github.com/ohmiler/solodeveling/actions/runs/29426763270)
  passed all six Windows, Ubuntu, and macOS test combinations for Python 3.10 and 3.14 plus the Ubuntu package job.
- Final local artifact hashes from commit `1d6a22d`: wheel
  `6055590863c021ac28839ea996703081e22fbaa445f6753519bb47a988c30a93`; source
  distribution `9672053da1559464b0131f075946267482397bb9cd900612826218f92fc89354`.
- Release integration: pull request
  [7](https://github.com/ohmiler/solodeveling/pull/7) remains open and the
  implementation history is not merged into `main`.

## Remaining gates before publication

- Review and merge pull request 7 into `main` through an explicitly authorized
  integration path. The cross-platform CI gate has passed on the reviewed branch.
- Recheck dependency vulnerabilities, package-name availability, runtime discovery
  documentation, metadata, artifact hashes, and support claims from the release commit.
- Decide whether to publish a GitHub Release, PyPI distribution, provenance
  attestation, and SBOM. Each is a separate external action and none is automatic.
- Do not claim Tier 1 until the full behavioral matrix passes on Codex, Claude Code,
  and Cursor. Current live evidence is one representative pass on Codex and Claude.
