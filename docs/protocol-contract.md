# Solodeveling Protocol Contract

## Portability

Project memory is Markdown with YAML frontmatter. Humans and agents may use it without Python. The validator is optional verification tooling and never a workflow correctness dependency.

## Schema version

Every protocol artifact includes `solodeveling_schema: 1`. A future schema change requires validation, backup, migration, and safe failure without partial state changes.

## Artifact kinds

- `.solodeveling/state.md` uses `state.schema.json`.
- `.solodeveling/work/active/*.md` and `.solodeveling/work/archive/*.md` use `work-item.schema.json`.
- `.solodeveling/evidence/*.md` uses `evidence.schema.json`.

## Completion invariants

- Work passes through `verifying` before `done`.
- Done work references evidence or records an accepted verification gap.
- Critical done work records security and recovery consideration.
- Evidence reports claim, method, result, scope, and limitations.
- Missing execution capability is recorded as unverified, not passed.

## Validation

Run `solodeveling validate <project-root>`. Exit code 0 means the inspected artifacts satisfy the implemented structural and cross-reference checks. It does not prove that the software itself is correct or secure.
