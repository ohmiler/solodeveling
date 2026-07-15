---
solodeveling_schema: 1
id: EVIDENCE-009
work_item: WORK-009
claim: Solodeveling exposes one public package and command name across Python and Node.js, provides documented npm, npx, uvx, uv tool, and pipx installation UX, builds and smoke-tests one canonical implementation on six native targets, and prepares a dependency-free npm launcher that fails closed before executing unverified code.
method: Unified command and metadata regression tests, legacy-name documentation guards, exact wheel entry-point inspection, isolated wheel installation, full installed command and runtime smoke, PyInstaller resource-inventory regression and native smoke, Node launcher boundary tests, complete native manifest generation, local npm pack and npx execution, exact source-bound candidate and CycloneDX verification, full Python suite, ten-skill validation, protocol validation, compilation, dependency health, pip-audit, pinned least-privilege CI, and six-target GitHub Actions native plus npm aggregation.
command: python -m pytest -q; npm test --prefix packages/npm; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python -m compileall -q src tests scripts; python -m pip check; python scripts/build_release.py and scripts/verify_release.py in C:/tmp; isolated installed wheel smoke; python scripts/build_native.py and scripts/smoke_native.py on Windows x64; local npm prepare, pack, and npx tarball smoke; python scripts/build_candidate.py and scripts/verify_candidate.py for f1f98b3a6ca44d17c6cfba29600f66577d4e724d; pip-audit 2.10.1 --local --skip-editable; GitHub Actions run 29434106046.
result: passed
scope: Public naming and command dispatch, Python metadata and distributions, Node launcher and package contents, native Windows/macOS/Linux x64 and arm64 artifacts, embedded schemas/templates/skills/evaluations, npm manifest binding, cache and download verification, documentation, ordinary CI, local non-publishing candidate, and recovery boundaries.
limitations:
- No npm package, PyPI distribution, version tag, GitHub Release, protected registry environment, trusted publisher, OIDC publication, signature, or release attestation was created.
- The source-tree npm artifact manifest remains intentionally empty. A publishable npm tarball must be regenerated from the six exact native assets of the authorized release commit.
- CI artifacts are temporary workflow artifacts, not an immutable GitHub Release. Native executables are not code-signed or release-attested.
- Local file-symlink creation was unavailable on Windows, so that Node regression skipped locally; it passed in the successful Ubuntu npm-package CI job.
- pip-audit found no known vulnerabilities in installed dependencies but skipped the editable solodeveling distribution and a stale editable solodeveling-protocol installation because neither represents an auditable registry release.
- npm and PyPI name availability is time-sensitive and was not reserved.
- One-file executables extract to an operating-system temporary directory on each invocation and may start slower than the Python tool path.
- Cursor live behavior and the complete Tier 1 cross-agent matrix remain unverified.
---
# Verification summary

On 2026-07-15, 178 Python tests and nine Node tests passed in the applicable
environments. The local Windows Node run skipped only file-symlink creation because
the host disallowed it; the Ubuntu npm-package job executed the same test successfully.
The official skill-suite validator, protocol validator, compilation, dependency
health, workflow parsing, archive verification, installed wheel smoke, native smoke,
npm pack/npx smoke, and pip-audit gate passed.

GitHub Actions run
[29434106046](https://github.com/ohmiler/solodeveling/actions/runs/29434106046)
passed Python 3.10 and 3.14 on Windows, Ubuntu, and macOS; the source-bound Python
candidate job; native build and complete embedded-resource smoke on Windows x64,
Windows arm64, macOS x64, macOS arm64, Linux x64, and Linux arm64; and the final npm
job that combined all six assets, tested the dependency-free launcher, prepared the
exact manifest, packed a local tarball, and ran it through npx without a network
binary download.

The final non-publishing Python candidate from commit
`f1f98b3a6ca44d17c6cfba29600f66577d4e724d` passed distribution,
candidate, checksum, inventory, SBOM, and source-revision verification. Its SHA-256
identities were:

- wheel: `5dc08db8f4938623b1c02d5bf796e4cf2cb9953297b9b46a09804e089136fe8a`
- source distribution: `99d4e2c3903462ca705e578a17d270e6242c99ae74e1e0081a4cbb313d309ff8`
- release notes: `b763e6a900e625af379f89b681c4576c29b3f8f1dfd1d23d61c438e18605fe2f`
- CycloneDX SBOM: `5a8b2e7c06155ca91da1e2c849211efb851edb4f1b99474a881d52e1a2cd7bc5`
- candidate manifest: `ca4e8ecf4d6ba0ded38eff63b08e6d481200c2e29d03e6b3057b5162f70d8f3c`

## Security and recovery evidence

The npm package has no runtime dependencies and no preinstall, install, or postinstall
lifecycle script. The launcher accepts only fixed platform mappings and an exact
version-bound filename, size, and lowercase SHA-256; uses a hard-coded versioned
GitHub Release path over HTTPS; limits redirects and download size; stages with
exclusive creation; rejects unsafe names, unsupported targets, symlinked cache
entries, tampering, and hash or size mismatch; verifies again after atomic promotion;
restores executable permission on non-Windows; and spawns with shell disabled.

Native and npm build jobs have only contents-read workflow permission and all external
actions are pinned to full commit SHAs. Failed build and verification work is isolated
to disposable output/cache paths. Project installation retains collision, containment,
atomic update, drift, symlink, dry-run, and safe-uninstall controls. No release or
registry state changed.
