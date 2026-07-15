# Release readiness

Build the smallest project-specific gate that can disprove readiness.

## Candidate and change

- Bind artifact or digest, version, source revision, build inputs, target environment,
  compatibility window, and intended change.
- Review user-facing notes, operational instructions, API or data compatibility, and
  feature-flag defaults where relevant.
- Confirm dependencies and lockfiles resolve from expected sources. Treat build
  output, SBOMs, signatures, and provenance as evidence requiring validation.

## Environment and risk

- Validate production configuration separately from development defaults.
- Verify secret references and least-privilege permissions without revealing values.
- Reconcile open defects, security findings, accepted risk, and expiry conditions.
- Confirm monitoring, alert ownership, support communication, capacity, and external
  dependency health needed for the observation window.

## Proof and decision

Run focused checks for changed behavior, then the broadest practical regression,
security, build, package, and compatibility checks. Record skipped or unavailable
checks as unverified.

Before execution, name the last known-good artifact, recovery owner, rollback trigger,
data implications, and maximum tolerable observation time. A release candidate is
not ready when a critical acceptance criterion or credible recovery path is missing.

After execution, observe critical user journeys, error and latency signals, security
events, queues or jobs, and data integrity. Compare with a known baseline. Record the
window and limitations; silence or a successful deploy command is not evidence that
the release is healthy.
