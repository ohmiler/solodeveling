# Publishing Solodeveling

Publishing is a separate production-changing action. Preparation, CI success, a
release candidate, or the word “continue” does not grant publication authority.
Every release requires explicit authorization naming the version, source revision,
GitHub Release action, provenance action, and PyPI upload.

## Intended trusted identity

- Repository: `ohmiler/solodeveling`
- Package: `solodeveling-protocol`
- Workflow: `.github/workflows/release-candidate.yml`
- GitHub environment: `pypi`
- Identity mechanism: PyPI Trusted Publishing through GitHub Actions OIDC

Neither the PyPI project nor the `pypi` GitHub environment existed when WORK-008
started. An owner must create and protect them separately, require reviewer approval,
and configure the exact repository, workflow filename, environment, and package.
Do not substitute a long-lived PyPI token in repository or environment secrets.

## Authorized release sequence

1. Merge the reviewed release-readiness branch and bind candidate version 0.1.0 to
   the exact resulting commit SHA.
2. Rebuild wheel, source distribution, release notes, CycloneDX SBOM, manifest, and
   SHA-256 checksums from that commit in a clean environment.
3. Invoke `release-candidate.yml` manually only after explicit authorization. Verify
   the generated GitHub artifact attestation against the repository and exact
   subjects.
4. Re-run dependency and vulnerability checks, then compare every uploaded digest
   with the authorized candidate manifest.
5. Obtain separate explicit authorization before creating a tag, GitHub Release, or
   uploading to PyPI. Observe installation and critical commands after publication.

## Recovery

Before upload, recovery is deletion of only disposable candidate artifacts and
virtual environments. If identity, checksum, SBOM, attestation, or metadata differs,
stop and rebuild from the reviewed commit. After an incorrect publication, do not
silently replace files: preserve evidence, yank the affected PyPI release when
appropriate, publish a corrected version, and document impact and recovery.