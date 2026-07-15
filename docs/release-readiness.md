# Release readiness

WORK-009 extends the non-publishing release gate to one public name and two install
ecosystems. Ordinary CI builds Python distributions, six platform executables, and an
npm tarball for verification; it does not publish, tag, create a GitHub Release, or
configure a registry.

## Local gate

1. Run the full test suite, ten official skill validations, protocol validation,
   compilation, dependency checks, Node launcher tests, and diff review.
2. Build the current-platform executable into a new path:

       python scripts/build_native.py C:/tmp/solodeveling-native

3. Exercise embedded templates, schemas, skills, evaluations, and all unified
   subcommands:

       python scripts/smoke_native.py C:/tmp/solodeveling-native C:/tmp/native-smoke

4. Build the source-bound Python candidate from a clean exact revision and verify its
   checksums, contents, SBOM, release notes, and manifest.
5. Collect all six CI-native artifacts, prepare the version-bound npm package, inspect
   `npm pack` contents, and run the local tarball through `npx`
   with a verified cached artifact.
6. Review manifests and SHA-256 values. Integrity hashes are not a signature,
   attestation, or proof of publisher identity.

The builders refuse unsafe or existing destinations, require exact inventories, use
temporary staging, and never upload to a registry.

## Evidence checked 2026-07-15

- Python 3.10 and 3.14 remain the supported Python bounds in cross-platform CI.
- The unified Python CLI regression and full suite passed locally after removing the
  four split console entry points.
- A Windows x64 PyInstaller 6.21.0 executable embedded schemas, templates, skills,
  evaluations, and required dependency grammar data; full installed smoke passed.
- A dependency-free npm tarball was prepared locally without lifecycle install scripts
  and `npx` executed the verified cached Windows binary successfully.
- Node tests rejected unsafe names, invalid versions, unsupported platforms, corrupt
  downloads, tampered cache files, wrong sizes, and wrong hashes before execution.
- npm and PyPI name lookups returned not found earlier on this date. That is not a
  reservation and can change before publication.
- No npm project, PyPI project, trusted publisher, protected registry environment,
  tag, GitHub Release, or registry publication exists from this work.

Tier 1 remains unverified because the full behavioral scenario matrix has not passed
on Codex, Claude Code, and Cursor.

## Remaining gates

- Push WORK-009 and require the new six-target native and npm-package CI jobs to pass.
- Review CI cost, public-preview runner stability, artifact inventories, and every
  current dependency vulnerability result.
- Merge through an authorized review path, then rebuild the release candidate from
  the resulting exact main commit.
- Recheck both registry names and configure protected OIDC trusted publishers only
  after explicit owner authority.
- Treat tag creation, GitHub Release, attestation, PyPI publication, and npm staged
  publication as each a separate external action.
