# Publishing Solodeveling

Publishing changes external production state. Preparation, passing CI, a release
candidate, or a general instruction to continue does not grant publication authority.
Each release requires explicit authorization naming the version, exact source commit,
tag, GitHub Release, provenance, PyPI publication, and npm publication. Approval for
one action does not imply the others.

## Trusted identities and owner setup

GitHub release immutability was enabled for this repository on 2026-07-16. It
protects only releases created after the setting was enabled.

Use these exact identities:

- repository: `ohmiler/solodeveling`;
- PyPI distribution: `solodeveling`;
- npm package: `solodeveling`;
- candidate workflow: `.github/workflows/release-candidate.yml`;
- publication workflow: `.github/workflows/publish.yml`;
- protected registry environments: `environment: pypi` and `environment: npm`.

Both GitHub environments exist, require reviewer `ohmiler`, permit the solo owner to
review a workflow they initiated, and allow deployment only from exact branch
`main`. They contain no secrets or variables, and GitHub reports administrator bypass
is disabled for both environments.

PyPI trusted publishing is configured for project `solodeveling`, GitHub owner
`ohmiler`, repository `solodeveling`, workflow `publish.yml`, and environment `pypi`.
The existing GitHub `pypi` environment provides required owner review and exact
`main` branch restriction. Version 0.1.0 was published through this OIDC path.

npm trusted publishing is configured for package `solodeveling`, repository
`ohmiler/solodeveling`, workflow `publish.yml`, and environment `npm`. Trusted
publishing is stage-only and the package publishing-access setting disallows
traditional write tokens. Version 0.1.0 completed its one-time interactive bootstrap;
later releases use the protected environment and staged npm action so the owner can
review and approve the exact release before it becomes public.

## Version-bound release set

One authorized release set contains all of the following from the same reviewed
source commit:

- Python wheel and source distribution;
- six native executables for Windows, macOS, and Linux on x64 and arm64;
- npm tarball with exact native filenames, sizes, and SHA-256 values;
- release notes, checksums, CycloneDX SBOM, source revision, and build inputs;
- artifact attestations and registry provenance where supported.

Do not publish the npm tarball until all native files it names exist in the same
versioned GitHub Release. Do not use a mutable latest URL or edit a generated
manifest after hashing.

## Complete release set boundary

The complete release set is an indivisible, non-publishing input. Preparing or
verifying it does not publish anything and does not grant registry authority.
Candidate invocation, tag creation, GitHub Release creation, PyPI publication, npm
staging, and npm publication each require separate explicit authorization.
## Guarded publication workflow

`publish.yml` is manual-only and accepts an exact version, the exact 40-character
candidate commit, an exact typed confirmation, a PyPI boolean, and an npm action of
`skip`, `stage`, or `publish`. The workflow itself must run from current protected
`main`; it accepts an older candidate only when Git proves that commit is an ancestor
of the current workflow revision and the canonical dynamic source version matches.
It refuses a candidate outside that history, a mismatched tag, a draft, mutable, or
missing GitHub Release, a changed release-set inventory, a failed hash, or an
attestation not issued by `release-candidate.yml` for that candidate commit.

The validation job has no write permission. The two registry jobs receive
`id-token: write` only behind their matching protected environment. There is no
registry token or password in the workflow. The workflow never creates a tag or
GitHub Release and never repairs or replaces release files.

## Authorized release sequence

1. Merge the reviewed release branch and record the exact resulting `main` SHA.
2. With explicit authority, run `release-candidate.yml` from that exact `main` SHA.
3. Download and independently inspect the complete candidate, checksums, SBOM,
   manifests, smoke evidence, and attestations.
4. With separate authority, create tag `v<version>` at that SHA and an immutable,
   non-draft immutable GitHub Release containing the complete verified release set.
5. Confirm the protected registry environments and trusted-publisher identities
   described above still match the release workflow.
6. With explicit authority naming the registry targets, run the current `publish.yml`
   from protected `main` while naming the exact verified candidate SHA. Enter exactly
   `CONFIRM publish solodeveling <version> from <source_revision>`.
7. Prefer PyPI alone and npm `stage` as independently reviewable choices. Use direct
   npm `publish` only when that exact action was explicitly authorized.
8. Complete the post-publication smoke checks before announcing availability.

## Post-publication smoke

Use clean temporary environments and do not rely on a developer checkout or cache:

    python -m pip install --no-cache-dir "solodeveling==<version>"
    solodeveling version
    uvx --from "solodeveling==<version>" solodeveling version
    pipx run --spec "solodeveling==<version>" solodeveling version
    npm view "solodeveling@<version>" version dist.integrity
    npx --yes --package "solodeveling@<version>" solodeveling version

Confirm that the reported version is exact, the npm launcher downloads only the
matching versioned native asset, and registry provenance refers to the authorized
repository, workflow, and source revision.

## Recovery

Before publication, discard only disposable outputs and rebuild the entire set if
any source, version, inventory, checksum, SBOM, build input, tag, release asset, or
attestation differs. Never edit a generated manifest or replace one artifact.

After an incorrect publication, preserve evidence and do not silently replace
registry bytes. Stop further publication, yank the affected PyPI release or
deprecate the npm version where appropriate, make an authorized decision about
unsafe GitHub Release visibility, publish a corrected new version, and document the
impact and recovery.
