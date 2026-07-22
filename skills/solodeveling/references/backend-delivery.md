# Backend delivery contract

Use this contract for queries, API handlers, database mutations, webhooks, provider
integrations, and additive migrations. Classify from observable effects, not the mere
presence of a server, database, authentication middleware, or provider SDK.

## Allow Quick only when the backend boundary stays bounded

A query or API handler remains Standard unless every applicable condition below is
demonstrably true:

- The path is read-only, produces no stored-data mutation or external effect, and
  does not select or expose new sensitive data.
- Authentication, authorization, ownership, tenant scoping, and negative-access
  behavior remain unchanged.
- Request validation, response fields and types, nullability, status and error
  behavior, caching, pagination, and compatibility guarantees remain unchanged.
- The only intended behavior change is a bounded deterministic mapping, sorting, or
  copy adjustment with known local consumers; no shared serializer, query primitive,
  generated contract, or cross-route behavior changes.
- A focused contract test proves the exact response plus relevant empty/error paths
  and, for a protected endpoint, unchanged unauthorized behavior.

An observationally equivalent pure refactor may also be Quick with a focused test.
Any uncertainty about consumers, sensitivity, access, validation, compatibility, or
shared behavior keeps the change Standard. Quick is not a waiver for server-side
validation, access checks, or evidence.

## Keep one boundary record

WORK owns one record for each changed effect boundary. Treat the security
attack-surface matrix, transaction plan, recovery plan, and verification mapping as
views of this record rather than separate artifacts.

| Field | Record |
| --- | --- |
| ID | Stable short name referenced by acceptance and evidence |
| Boundary | Query, mutation, webhook, provider effect, or migration being changed |
| Authority | Who or what may invoke the effect and under which verified condition |
| Invariant | State or outcome that must remain true, including duplicate behavior |
| Failure | Partial, concurrent, retry, invalid, or unavailable behavior to contain |
| Risk / Control | Material risk and the control that prevents or detects it |
| Verification | Focused checks that prove authority, invariant, and failure handling |
| Recovery | Rollback, roll-forward, retry, reconciliation, or explicit none needed |

Shaping, planning, securing, execution, and verification update or reference the
same record by ID. EVIDENCE records `boundary ID -> result -> limitation`; it does not
copy the record. Add project-specific fields only when they change a decision.

## Select gates by effect

These are focused minimums, not a command checklist:

| Effect | Focused minimum |
| --- | --- |
| Query | Authority when protected; request validation; mapping; empty and error paths |
| Local mutation | Authority; validation; transaction commit and rollback; duplicate/retry behavior |
| Webhook | Signature and freshness; replay; idempotency; duplicate/out-of-order delivery; partial failure and retry |
| Additive migration | Schema diff; generated migration review; fresh and existing-schema apply; compatibility; recovery |
| Critical migration | Representative data; integrity invariants; compatibility window; rehearsed recovery and exact authority |

`Applicable` means a gate can detect a regression in a changed file, behavior,
dependency, generated artifact, environment, or boundary:

- Run neighboring tests when shared query, serializer, transaction, provider, or data
  primitives change.
- Run affected lint or type checks when changed code crosses their configured scope.
- Run a build when generated types, packaging, bundling, runtime integration, or
  deployable output can change.
- Run the full suite once at the checkpoint when shared data/security behavior,
  schema compatibility, or project policy makes its coverage relevant.

Do not run a broad gate merely because the stack contains a database, login,
payment provider, or webhook. Add a stricter project gate when an observable invariant
requires it, and record why.

## Triage backend verification failures

Classify the failure before changing production source or weakening an assertion:

1. A reproducible source or contract failure routes to debugging.
2. A fixture or mock may be repaired only after evidence shows it disagrees with the
   real library, schema, or provider contract. Preserve the original assertion and
   rerun the same focused check once.
3. For an unavailable local database, queue, emulator, or migration tool, restore the
   expected controlled environment and rerun once. If unavailable, mark the affected
   criterion unverified instead of calling the product fixed or broken.
4. Missing credentials, provider network access, or a sandbox capability does not
   invalidate code-level fixture evidence and does not prove the target environment.
   Keep the owner-controlled smoke check as separate unverified release evidence.
5. If a migration target, environment, schema version, or connection identity is
   uncertain, fail closed. Do not probe by mutating an unknown database.

Never use real credentials in ordinary tests, replace a failing contract with a
weaker mock, or treat one passing retry as proof when the first failure remains
unexplained.

## Use the additive migration template

Keep an additive, reversible migration with no material backfill Standard unless a
new constraint, data transformation, access change, or production effect escalates
the boundary.

1. Inspect the current schema, migration history, generated-client workflow, and
   supported application-version window.
2. Generate the migration with the repository tool and review the exact schema diff
   and generated statements. Do not hand-edit generated output unless project policy
   requires it.
3. Apply it to a fresh schema and an existing representative pre-migration schema.
4. Verify focused reads/writes, null/default behavior, and old/new application compatibility
   when rolling deployment can overlap versions.
5. Regenerate types and run the affected build only when those outputs or runtime
   boundaries change.
6. Define the smallest credible rollback or roll-forward and state why existing data
   remains safe. Production execution still requires separate authority.
