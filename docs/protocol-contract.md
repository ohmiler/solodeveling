# Solodeveling Protocol Contract

## Portability

Project memory is Markdown with YAML frontmatter. Humans and agents may use it without Python. The validator is optional verification tooling and never a workflow correctness dependency.

## Schema version

Every protocol artifact includes `solodeveling_schema: 1`. A future schema change requires validation, backup, migration, and safe failure without partial state changes.

## Artifact kinds

- `.solodeveling/state.md` uses `state.schema.json`.
- `.solodeveling/work/active/*.md` and `.solodeveling/work/archive/*.md` use `work-item.schema.json`.
- `.solodeveling/evidence/*.md` uses `evidence.schema.json`.

## Progressive persistence

Classify intent before reading project memory or choosing a level. Direct Read-Only
Q&A, explanation, review, status, diagnosis, and inline planning create no lifecycle
or evidence artifacts unless the user explicitly asks to preserve a result. General
Q&A reads no repository; status normally reads state plus Git, then adds WORK,
EVIDENCE, or archives only when the requested detail requires them.

- Ephemeral Quick work stays in one session, creates no project-memory artifacts, and
  still requires a focused verification result before a completion claim.
- Standard work uses one WORK item and one cumulative EVIDENCE file. Its plan and
  decisions stay in WORK; checks and limitations stay in EVIDENCE.
- Critical, security, release, migration, production, destructive, and sensitive
  work retain the full audited lifecycle, evidence, recovery, and authorization
  contract.

Ephemeral Quick takes precedence for a bounded same-session follow-up, even when the
surface previously had Standard work. Reuse the existing Standard pair only when the
continuation must survive a session, changes a durable decision, or remains part of
an active batch with unchanged goal, acceptance, authority, risk, release boundary,
and rollback. Create a new item only when one of those boundaries changes. Update
roadmap only when a milestone, priority, ordering, or deferred-work decision changes.

Classify backend work by the boundary changed and effect produced, not by the mere
presence of authentication, a database, or an API. Authenticated sorting or mapping
may remain Standard; changes to credentials, sessions, role/permission/ownership
decisions, sensitive-data exposure, payment fulfillment, or trust boundaries are
Critical. Additive reversible migrations without material backfill may be Standard;
data transformations and destructive migrations are Critical.

`state.md` is a compact current dashboard. Its `active_work` list must not reference
deferred or done work. Validate memory after relevant memory or schema changes, when
invalidity is suspected, before committing memory, and before tracked completion.

## Completion invariants

- Work passes through `verifying` before `done`.
- Done work references evidence or records an accepted verification gap.
- Critical done work records security and recovery consideration.
- Evidence reports claim, method, result, scope, and limitations.
- A cumulative evidence file keeps one Current acceptance matrix, marks replaced
  requirements `Superseded by ...`, and stores a short observation log. A latest
  `failed` or `unverified` result blocks `done`.
- Missing execution capability is recorded as unverified, not passed.

Focused verification runs per coherent slice. Affected broad gates run at commit,
handoff, changed boundary, or closure and remain valid until a later change crosses
their covered file, behavior, dependency, environment, or boundary. Do not rerun an
unchanged broad gate solely because a commit was requested.

## Validation

Run `solodeveling validate <project-root>`. Exit code 0 means the inspected artifacts satisfy the implemented structural and cross-reference checks. It does not prove that the software itself is correct or secure.

Installed users may apply common tracked-work updates without repetitive manual
edits:

~~~console
solodeveling work evidence <root> WORK-001 --claim "Tests pass" --method "Automated test" --result passed --scope "Changed behavior"
solodeveling work transition <root> WORK-001 verifying
solodeveling work archive <root> WORK-001 --next-action "Select the next priority"
~~~

These commands validate memory before and after mutation, update related artifacts
together, and roll back partial writes. They do not replace acceptance judgment or
software verification.

## Repository CI routing

- Changes entirely under `.solodeveling/` run project-memory validation and focused
  memory regressions.
- Changes entirely under `docs/` run the complete Python regression suite on one
  Ubuntu job and check the exact base-to-head diff.
- README, root Markdown, skills, source, tests, workflows, packages, tags, malformed
  paths, and mixed path sets use the full test, package, native, and npm gate.

Unknown or ambiguous classification always falls back to the full gate.
