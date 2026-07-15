---
solodeveling_schema: 1
id: EVIDENCE-015
work_item: WORK-015
claim: GitHub environment administrator bypass is disabled while immutable releases, owner review, solo-owner self-review, and exact main-only policies remain enabled; the matching PyPI pending publisher is owner-confirmed with public verification explicitly unavailable before first use.
method: Fresh GitHub REST API inspection, main/CI/release-activity checks, public PyPI project lookup, owner statement, official PyPI pending-publisher behavior review, and focused project verification.
command: gh api immutable-releases and environments/{pypi,npm}; gh api deployment-branch-policies; gh run list for main, release-candidate.yml, and publish.yml; git tag --list; gh release list; PyPI JSON project lookup; project-memory and focused release/publication/documentation tests.
result: passed
scope: GitHub immutable-release and registry-environment controls; absence of candidate, publication, tag, and release activity; bounded recording of the pending PyPI publisher identity.
limitations:
- PyPI exposes no public account endpoint for independently reading a pending publisher; its configuration is owner-confirmed and OIDC matching remains unverified until a separately authorized first use.
- A pending publisher does not create or reserve the PyPI project name; the public project endpoint still returned 404.
- No candidate, OIDC token exchange, tag, GitHub Release, registry staging, approval, or publication was invoked.
---
# Evidence

## API-verified GitHub state

- Repository immutable releases reports `enabled: true`.
- Environments `pypi` and `npm` both report `can_admins_bypass: false`.
- Each environment retains required reviewer `ohmiler`, permits solo-owner self-review,
  and contains only the exact `main` branch deployment policy.
- `main` commit `8565887fc1494720259456b5ccc8b8780252afda` matched
  `origin/main`; post-merge CI run 29449189972 passed.
- Candidate and publish workflow run lists, tag list, and GitHub Release list were
  empty.

## Owner-confirmed PyPI state

The owner reported creating this pending publisher:

- project: `solodeveling`;
- GitHub owner: `ohmiler`;
- repository: `solodeveling`;
- workflow: `publish.yml`;
- environment: `pypi`.

The public PyPI project endpoint returned 404. This is expected because a pending
publisher does not create or reserve the project until first successful use; it is
not independent evidence of the authenticated pending-publisher settings.

## Local verification

- Focused release, publication, candidate, release-set, and installation-documentation
  tests: 39 passed.
- Project-memory validation, canonical skill-suite validation, and diff whitespace
  review passed.

## Security and recovery

- Admin bypass removal makes the configured reviewer action mandatory for environment
  jobs while self-review remains available to the solo owner.
- No long-lived PyPI token or GitHub environment secret is required or inspected.
- If first authorized OIDC use reports `invalid-pending-publisher`, compare the exact
  owner, repository, workflow filename, environment, and project name in the PyPI UI
  before retrying; do not weaken the GitHub gate or add a long-lived token fallback.
