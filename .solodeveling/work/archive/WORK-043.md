---
solodeveling_schema: 1
id: WORK-043
title: Gate and build the local Solodeveling 0.3.0 candidate
status: done
level: standard
type: release
goal: Run the authorized three-scenario Codex routing pilot and, only if it passes,
  advance all release surfaces to 0.3.0 and verify a local non-publishing candidate.
scope: Preregister one clear Standard frontend scenario, one clear Standard backend
  scenario, and one Critical backend readiness scenario; run them through the
  isolated read-only evaluation harness; review deterministic results; bump version
  metadata and release notes; build and verify local Python and current-platform
  native candidates from an exact committed revision.
out_of_scope: The separate 30-call comparative benchmark, Claude Code or Cursor live
  matrices, push, pull request, tag, GitHub Release, PyPI/npm publication, signing,
  attestation, production access, credentials, and production mutation.
acceptance:
- AC1 — A versioned three-scenario pilot pins expected level, primary workflow,
  action, authority, recovery, completion, and protocol signals.
- AC2 — All three Codex scenarios are live-pass with unchanged isolated fixtures;
  otherwise the version bump stops.
- AC3 — Python, npm, artifact metadata, current-version tests, docs, and 0.3.0 release
  notes agree after a passing pilot while the pinned 0.2.0 comparison stays unchanged.
- AC4 — Source gates, package checks, a clean Python candidate, and the current
  Windows native smoke test pass against exact recorded revisions.
- AC5 — Release evidence names candidate identity and limitations; no external
  release or production action occurs.
risks:
- The live runtime can fail for authentication, capacity, schema, or environment
  reasons unrelated to routing; classify those separately and do not weaken gates.
- A Standard result for the Critical scenario would be an under-classification and
  blocks the bump.
- Blanket version replacement would corrupt the intentionally pinned 0.2.0 benchmark.
decisions:
- Use the existing sanitized, read-only evaluation harness and Codex runtime only.
- Require all deterministic scalar and signal gates; do not use an AI judge.
- Build only local non-publishing artifacts and leave external actions unauthorized.
- On 2026-07-22 the owner explicitly accepted missing AC2 live evidence only for local
  candidate construction. This does not convert AC2 to passed and expires before any
  tag or publication decision.
verification:
- Validate the pilot corpus and dry-run plan, run exactly three live Codex scenarios,
  inspect sanitized results, then run focused/full source and candidate gates.
next_action: None; archived with a local-candidate-only accepted gap.
evidence:
- EVIDENCE-043
---
# Boundary record

| ID | Boundary | Authority | Invariant | Failure | Risk / Control | Verification | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | Live Codex evaluation | Owner authorized the named three-task pilot on 2026-07-22 | Read-only disposable fixtures; no network, credentials, repository mutation, or raw logs retained | Non-pass state or fixture digest change | Existing ephemeral harness, safe environment, JSON schema, deterministic scoring | Three sanitized results and before/after integrity | Stop before bump; retain bounded diagnostic only; temporary fixture is discarded |
| B2 | Local 0.3.0 candidate | Local preparation and build only | Version surfaces agree; artifact binds one exact committed source revision | Test, build, inventory, checksum, SBOM, or smoke mismatch | Clean source worktree, exact manifests, fresh output paths | Source suite, package verification, candidate verifier, native smoke | Discard disposable output and rebuild from reviewed commit |

## Observation log

- The offline preflight passed. The first live invocation was denied before execution
  because external transmission of private-workspace skill and scenario text requires
  explicit informed owner approval. No model call or sanitized result was produced.
- The owner then supplied the exact informed approval. Tenant policy still denied the
  invocation because this environment forbids that external transmission even with
  approval. No model call occurred; retry or indirect execution is prohibited.
- The owner explicitly accepted missing AC2 evidence for local candidate construction
  only. AC2 remains unverified and must be resolved or accepted again at the separate
  public-release decision.
- Source revision d0e9bcbaef88b301561fe4f6a530e0897378b2c9 passed exact-source
  gates. Its Python candidate, fresh-wheel installed smoke, and Windows x64 native
  smoke passed. Cross-platform release-set and public-release gates remain open.
