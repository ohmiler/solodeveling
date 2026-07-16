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
- `state.md`: compact current goal, active resumable work IDs, blockers, current
  risks, and next action; never a completed-work history.
- `roadmap.md`: milestones and priorities or a link to the established tracker.
- `standards.md`: Definition of Done and project conventions or authoritative links.
- `risks.md`: open product, technical, security, privacy, and operational risks.
- `decisions/`: durable approved decisions with rationale and consequences.
- `work/active/`: unfinished resumable work items. Only actively resumed IDs belong
  in state `active_work`; deferred items are not loaded until resumed.
  `work/archive/`: closed work.
- `evidence/`: durable verification summaries referenced by work items.

Keep the body concise. Do not store secrets, local environment details, raw logs,
temporary scans, caches, or conversation transcripts.

Use an artifact budget:

- Ephemeral Quick: no memory artifacts.
- Tracked Standard: one WORK item and one cumulative EVIDENCE file.
- Audited: add artifacts only for distinct decisions, findings, recovery boundaries,
  or independently reviewable claims.

Append bounded follow-up verification to the existing evidence file. Update roadmap
only for milestone or priority changes. Keep final reports as summaries with links,
not copies of WORK, EVIDENCE, state, or roadmap content.

## Brownfield preservation

Before writing, list existing sources for requirements, architecture, tasks,
standards, and decisions. Reference them from project memory. If equivalent project
memory already exists, stop and validate it; do not generate a parallel truth.
