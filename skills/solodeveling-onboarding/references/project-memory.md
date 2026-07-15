# Project memory creation

Create this minimum structure:

```text
.solodeveling/
|-- project.md
|-- state.md
|-- roadmap.md
|-- standards.md
|-- risks.md
|-- decisions/
|-- work/active/
|-- work/archive/
`-- evidence/
```

Every versioned artifact starts with YAML frontmatter containing
`solodeveling_schema: 1`.

## Deterministic initialization

When the optional package is installed, pass only discovered or user-approved facts:

```text
solodeveling-init <root> --name <name> --purpose <purpose> \
  --user <user> --architecture <summary> --stack <technology> \
  --source <authoritative-path> --goal <goal> --next-action <action>
```

Repeat `--user`, `--stack`, `--constraint`, and `--source` as needed. The command is
idempotent for valid memory and refuses to overwrite partial memory.

## Artifact responsibilities

- `project.md`: name, purpose, users, architecture, stack, durable constraints, and
  paths to authoritative sources.
- `state.md`: current goal, active work IDs, blockers, current risks, and next action.
- `roadmap.md`: milestones and priorities or a link to the established tracker.
- `standards.md`: Definition of Done and project conventions or authoritative links.
- `risks.md`: open product, technical, security, privacy, and operational risks.
- `decisions/`: durable approved decisions with rationale and consequences.
- `work/active/`: unfinished work items; `work/archive/`: closed work.
- `evidence/`: durable verification summaries referenced by work items.

Keep the body concise. Do not store secrets, local environment details, raw logs,
temporary scans, caches, or conversation transcripts.

## Brownfield preservation

Before writing, list existing sources for requirements, architecture, tasks,
standards, and decisions. Reference them from project memory. If equivalent project
memory already exists, stop and validate it; do not generate a parallel truth.