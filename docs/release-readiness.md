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
- Release integration: the implementation history is stacked on feature branches and
  not merged into `main`.

## Remaining gates before publication

- GitHub CI must pass on Windows, Linux, and macOS for Python 3.10 and 3.14 after this
  branch is pushed. Local execution cannot substitute for those platform results.
- Review and merge the stacked changes into `main` through an explicitly authorized
  integration path.
- Recheck dependency vulnerabilities, package-name availability, runtime discovery
  documentation, metadata, artifact hashes, and support claims from the release commit.
- Decide whether to publish a GitHub Release, PyPI distribution, provenance
  attestation, and SBOM. Each is a separate external action and none is automatic.
- Do not claim Tier 1 until the full behavioral matrix passes on Codex, Claude Code,
  and Cursor. Current live evidence is one representative pass on Codex and Claude.
