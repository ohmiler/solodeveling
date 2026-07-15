# Publishing Solodeveling

Publishing changes external production state. Preparation, passing CI, a release
candidate, or a general instruction to continue does not grant publication authority.
Each release requires explicit authorization naming the version, exact source commit,
tag, GitHub Release, provenance, PyPI publication, and npm publication. Approval for
one action does not imply the others.

## Intended trusted identities

- Repository: `ohmiler/solodeveling`
- PyPI distribution: `solodeveling`
- npm package: `solodeveling`
- Candidate workflow: `.github/workflows/release-candidate.yml`
- Future protected environments: `pypi` and `npm`
- Identity mechanism: registry Trusted Publishing through GitHub Actions OIDC

Neither registry project, protected environment, nor registry trusted-publisher
relationship is configured at this source revision. An owner must create and protect
them separately, require reviewer approval, bind the exact repository and workflow,
and disallow long-lived write tokens after OIDC is verified.

npm Trusted Publishing should use stage-only permission where available so CI can
prepare a publication that still requires maintainer review and 2FA approval. Public
packages published from this public repository through npm Trusted Publishing receive
automatic provenance, but provenance links source and build identity; it does not
prove the code is safe.

## Version-bound release set

One authorized release set contains all of the following from the same reviewed
source commit:

- Python wheel and source distribution;
- six native executables for Windows, macOS, and Linux on x64 and arm64;
- npm tarball with a manifest containing exact native filenames, sizes, and SHA-256;
- release notes, checksums, CycloneDX SBOM, source revision, and build inputs;
- artifact attestations and registry provenance where supported.

Do not publish the npm tarball until all native files it names exist in the same
versioned GitHub Release. Do not use a mutable latest URL or edit a generated manifest
after hashing.

## Authorized release sequence

1. Merge the reviewed release branch and name the exact resulting commit SHA.
2. Rebuild every artifact from that commit in protected, clean environments.
3. Verify regression tests, skill validation, protocol validation, installed wheel
   smoke, six native smoke tests, Node launcher tests, local npm pack/npx smoke,
   SBOM, vulnerability results, inventories, and checksums.
4. Invoke the candidate provenance workflow only after explicit authorization and
   verify attestations against `ohmiler/solodeveling` and exact subjects.
5. Obtain separate authorization before creating the version tag and immutable GitHub
   Release containing the six native assets.
6. Confirm the GitHub assets match the npm manifest, then obtain separate authorization
   for PyPI and npm staged publication.
7. Observe clean-machine `uvx`, `pipx`, `npx`, and
   global npm installation after publication.

The current workflows build and upload only temporary CI artifacts. They contain no
registry publish command and no registry identity-token permission.

## Recovery

Before publication, remove only disposable build outputs and rebuild the complete set
when any version, source revision, inventory, checksum, SBOM, or attestation differs.
After an incorrect publication, preserve evidence and never replace registry bytes
silently. Yank or deprecate the affected version where appropriate, remove unsafe
GitHub assets or release visibility only through an authorized incident decision,
publish a corrected new version, and document impact and recovery.
