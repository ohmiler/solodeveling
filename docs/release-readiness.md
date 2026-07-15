# Release readiness

WORK-011 extends the guarded release and publication gate to one public name and two install
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

## Status reconciled 2026-07-16

- Pull requests 8 through 12 and WORK-008 through WORK-012 are merged. The reviewed
  pre-release base is `main` commit
  `cda0f4854359384f79ea45c50a8ad06f9eba6baf`; GitHub Actions run 29442409991
  passed the full Python/package, six-native-target, and npm pack/npx matrix.
- The npm and PyPI registry endpoints for `solodeveling` returned not found. The
  repository has no version tag or GitHub Release, so public `npx`, `uvx`, `pipx`,
  and registry installation remain unavailable.
- GitHub Release immutability is enabled. The `pypi` and `npm` environments require
  reviewer `ohmiler`, permit solo-owner self-review, contain exact `main`-only branch
  policy, and contain no secrets or variables. Administrator bypass remains enabled
  as an explicit residual recovery path.
- Source and guarded workflows are ready for owner-controlled release preparation.
  No candidate workflow, registry, tag, release, attestation, staging action,
  approval, or publication has been invoked.

## Remaining gates

- Decide whether to disable administrator bypass for `pypi` and `npm` through the
  GitHub environment UI before first publication.
- Recheck both registry names immediately before first publication.
- With separate explicit authority, invoke the candidate workflow from an exact
  reviewed `main` commit, inspect the complete attested set, then create its tag and
  immutable GitHub Release.
- Configure the PyPI pending publisher. Bootstrap npm 0.1.0 separately with
  interactive two-factor authentication, then configure npm Trusted Publishing with
  stage-only permission where practical.
- Treat each candidate invocation, tag, GitHub Release, environment or registry
  setup, PyPI publication, npm staging, npm approval, and direct npm publication as a
  separate external action and authorization checkpoint.
- Complete Tier 1 agent-runtime evaluation and decide whether native platform signing
  is required before a stable release.
## Complete release-set gate

After all upstream checks pass, assemble the coordinated non-publishing input from one
exact source revision:

    python scripts/assemble_release_set.py <candidate> <native> <npm-tarball> <release-set> --source-revision <sha>
    python scripts/verify_release_set.py <release-set> --source-revision <sha>

`release-set-manifest.json` must describe exactly two Python distributions, six native
executables, one npm tarball, one CycloneDX SBOM, and release notes. The verifier
recomputes size and SHA-256, checks the flat inventory, validates the npm archive
without extraction, and requires its platform manifest to match all six native bytes.
The gate provides bounded integrity and provenance input; it is not publication,
platform code signing, categorical security assurance, or Tier 1 behavior proof.

Recovery before publication is to remove only disposable output and rebuild the
entire set from the reviewed commit. Do not edit manifests or replace an individual
artifact. External tag, release, signing, registry configuration, and publication
actions remain separate authorization checkpoints.
