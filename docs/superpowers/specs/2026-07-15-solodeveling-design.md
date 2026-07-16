# Solodeveling Design Specification

**Date:** 2026-07-15
**Status:** Approved
**License:** Apache-2.0

## 1. Purpose

Solodeveling is a portable, solo-developer-first software development lifecycle (SDLC) skill suite for AI coding agents. It helps one human and one primary agent understand a project, shape and complete work, preserve context across sessions, apply professional quality controls, and integrate security throughout the lifecycle without requiring simulated team roles or subagents.

The suite must support greenfield and brownfield projects across frontend, backend, full-stack, mobile, desktop, CLI/library, data, infrastructure, and AI/agent systems. The universal core is technology-agnostic. Project and security profiles add only the concerns that differ by system type.

The central product principle is:

> Solodeveling must be fully functional with a single agent. Subagents are an optional future optimization, never a correctness dependency.

## 2. Goals

Solodeveling must:

- Give the user and agent a shared, durable understanding of the project.
- Preserve current state, decisions, unfinished work, risks, and verification evidence across sessions.
- Apply process in proportion to work-item risk, uncertainty, blast radius, and reversibility.
- Support multiple coding-agent runtimes from the first release.
- Use natural language as the primary interface.
- Continue autonomously within the authorized task and pause only for meaningful decisions or risk boundaries.
- Favor evidence over assertions and prevent unverified completion claims.
- Integrate security from requirements through maintenance using risk-based standards.
- Be fast and pleasant for small work while remaining rigorous for critical work.
- Minimize token consumption through progressive disclosure and compact project artifacts.
- Remain inspectable, portable, and useful without a proprietary service, cloud account, subagent system, or workflow engine.

## 3. Non-goals for Version 1

Version 1 will not:

- Implement a full CLI workflow engine.
- Model a virtual software team or require personas.
- Require subagents, parallel execution, worktrees, pull requests, or a specific Git provider.
- Include framework-specific tutorials for every supported ecosystem.
- Require an issue tracker or replace one already used by a project.
- Perform autonomous production deployment.
- Guarantee that software is secure or production-ready without scoped evidence.
- Depend on browser access, network access, MCP integrations, or runtime-specific task tools.

## 4. Product Principles

### 4.1 Solo-human first

One human owns product decisions. One primary agent maintains continuity from understanding through implementation and verification. The workflow must not create coordination overhead merely to imitate team ceremonies.

### 4.2 Risk-adaptive process

Process depth is selected per work item, not per repository. A large repository can contain a Quick change, while a small repository can contain a Critical authentication or migration change.

### 4.3 Durable, human-readable memory

Project memory lives in the repository as Markdown or YAML. It is understandable without Solodeveling and portable across agents and sessions.

### 4.4 Evidence-driven completion

Claims such as fixed, complete, passing, secure, or ready must map to recent evidence. Missing execution capability must be reported as a verification limitation, not silently converted into confidence.

### 4.5 Progressive disclosure

The core router stays small. It loads one primary workflow and only the project, system, security, or runtime references required for the current work.

### 4.6 Natural-language first

Users do not need to memorize commands. Runtime commands and hooks may improve convenience but must not be required for correct operation.

### 4.7 Existing-project respect

Solodeveling reads and follows existing project documentation, commands, conventions, and tracking systems before creating new structures. It avoids duplicate sources of truth.

### 4.8 Friction must earn its cost

Every checkpoint and artifact must prevent a concrete failure, preserve useful context, or improve auditability. Otherwise it should be removed.

## 5. Architecture

Version 1 uses a protocol-first skill-suite architecture.

```text
Portable skill suite
|-- core router
|-- lifecycle workflow skills
|-- project and security profiles
|-- human-readable artifact contracts
`-- lightweight deterministic validators

Optional runtime adapters
|-- Codex
|-- Claude Code
|-- Cursor
`-- generic Agent Skills clients
```

The protocol consists of work-item states, artifact schemas, routing rules, evidence semantics, risk triggers, and exit criteria. Runtime adapters may provide installation metadata, commands, hooks, permissions, or task UI, but may not change protocol semantics.

### 5.1 Skill suite

The initial suite contains:

- `solodeveling`: entry point, state reader, classifier, and router.
- `solodeveling-onboarding`: greenfield initialization and brownfield project discovery.
- `solodeveling-shaping-work`: intent, scope, acceptance criteria, and alternatives.
- `solodeveling-planning-work`: proportional implementation and verification planning.
- `solodeveling-executing-work`: sequential single-agent implementation and state tracking.
- `solodeveling-debugging`: root-cause diagnosis before fixes.
- `solodeveling-verifying`: evidence collection and Definition of Done enforcement.
- `solodeveling-securing`: security routing, threat analysis, findings, and verification.
- `solodeveling-releasing`: migration, deployment, rollback, and release readiness.
- `solodeveling-maintaining`: dependencies, vulnerabilities, incidents, debt, and operational work.

Each workflow skill defines:

- Inputs required before entry.
- Actions the agent performs.
- Artifacts it creates or updates.
- Exit criteria.
- Conditions that escalate risk or route to another skill.

Workflow skills reference one another rather than duplicating instructions.

### 5.2 Capability model

The baseline assumes the agent can read files, edit files, inspect the repository, and communicate results. Command execution, Git, network access, browser automation, external connectors, rendering, and subagents are optional.

Capability absence changes evidence strength, not workflow correctness:

- Without command execution, automated checks are recorded as unverified.
- Without Git, branch and commit operations are skipped.
- Without browser or emulator access, visual or platform verification limitations are recorded.
- Without network access, time-sensitive external facts are not asserted as current.
- Without subagents, all work proceeds sequentially in the primary agent.

## 6. Core Workflow

```text
User request
    v
Read project state
    v
Inspect relevant project evidence
    v
Classify work type and risk level
    v
Create or update a work item
    v
Shape -> Plan as needed -> Execute -> Verify
    v
Record evidence, decisions, risks, and limitations
    v
Close work item and update project state
```

### 6.1 Work types

- **Explore:** investigate an idea, technology, or codebase.
- **Build:** create a system or feature.
- **Change:** alter behavior, architecture, configuration, or structure.
- **Repair:** diagnose and fix unexpected behavior.
- **Secure:** assess or improve security and privacy.
- **Release:** deploy, publish, migrate, or roll back.
- **Maintain:** update dependencies, manage debt, improve performance, or perform operational work.

A work item has one primary type and may include additional concerns such as security, data migration, accessibility, or compatibility.

### 6.2 Process levels

#### Quick

Use only when impact is low, rollback is easy, requirements are clear, and no security-sensitive boundary is involved.

- Keep the work record compact.
- Shape, execute, and verify in one continuous pass when appropriate.
- Avoid long plans and unnecessary artifacts.
- Never skip verification.

#### Standard

Use by default for ordinary features, defects, and meaningful changes.

- Record goal, scope, acceptance criteria, risks, and verification strategy.
- Inspect the codebase before planning.
- Plan around contracts, dependencies, and outcomes rather than reproducing implementation code.
- Verify behavior, regression safety, and applicable security concerns.

#### Critical

Use when any critical trigger applies, including:

- Authentication or authorization.
- Payments or financial data.
- Sensitive or personal data.
- Destructive or difficult-to-reverse migration.
- Public APIs or production infrastructure with a large blast radius.
- Cryptography or secret management.
- Safety-critical behavior.
- A change with uncertain recovery or rollback.

Critical work adds a threat model, explicit security acceptance criteria, rollback or recovery planning, stronger verification, and a user checkpoint before material irreversible action.

Risk levels use observable triggers rather than a misleading numeric score. The user may request a different level. Lowering work that has a Critical trigger requires a concise risk warning and explicit user acceptance.

### 6.3 Work-item lifecycle

```text
captured -> shaped -> ready -> active -> verifying -> done
                    +-> blocked
                    `-> deferred
```

- `captured`: the request is recorded and initially understood.
- `shaped`: scope and acceptance criteria are clear.
- `ready`: enough information exists to execute safely.
- `active`: implementation or investigation is in progress.
- `verifying`: implementation is complete but completion is not yet established.
- `done`: applicable Definition of Done criteria have evidence.
- `blocked`: progress cannot continue and the blocking condition and next action are recorded.
- `deferred`: work is intentionally postponed with a reason and return condition.

Quick work may pass through multiple states in one session, but it cannot bypass `verifying`.

### 6.4 User checkpoints

The agent continues autonomously within scope. It pauses only when:

- Alternatives materially change product behavior, scope, or architecture.
- An action is irreversible, externally consequential, or production-impacting.
- A critical security assumption is unknown.
- Requirements conflict.
- Required authority exceeds the user's original request.
- Verification proves that the approved design cannot meet acceptance criteria.

A checkpoint states the decision, why it matters, the recommendation, and the principal alternative with its trade-off. The agent does not ask whether to continue after ordinary in-scope steps.

## 7. Project Memory Protocol

The default project structure is:

```text
.solodeveling/
|-- project.md
|-- state.md
|-- roadmap.md
|-- standards.md
|-- risks.md
|-- decisions/
|-- work/
|   |-- active/
|   `-- archive/
`-- evidence/
```

### 7.1 Artifact responsibilities

- `project.md`: purpose, users, architecture summary, technology stack, and durable constraints.
- `state.md`: current goal, active work, blockers, risks requiring attention, and next action.
- `roadmap.md`: milestones and priorities; it links to an existing tracker rather than duplicating it.
- `standards.md`: project Definition of Done and coding, testing, security, UX, and operational conventions.
- `risks.md`: open product, technical, security, privacy, and operational risks.
- `decisions/`: durable architecture or product decisions with context, rationale, and consequences.
- `work/active/`: unfinished work items.
- `work/archive/`: completed, cancelled, or superseded work items.
- `evidence/`: durable verification summaries worth retaining across sessions.

If a repository already has equivalent artifacts, Solodeveling references and updates the established source of truth instead of copying it.

### 7.2 Resume protocol

At the start of a new session, the agent reads:

1. `state.md`.
2. The active work item.
3. Relevant sections of project, standards, decisions, and risks.
4. The source files and evidence referenced by the work item.

It then establishes a compact resume packet containing the current goal, current state, known blocker, and next action. It does not load the full archive or ask the user to repeat discoverable history.

### 7.3 Work-item contract

A Standard or Critical work item includes at least:

```yaml
solodeveling_schema: 1
id: WORK-001
title: Add password reset
status: active
level: critical
type: build
goal: Provide a safe password reset flow.
scope: Application password reset request and completion flows.
out_of_scope: Account recovery through customer support.
acceptance:
  - Expired reset tokens are rejected.
risks:
  - Reset tokens could enable account takeover if leaked or replayed.
decisions: []
verification:
  - Automated integration test for expired and replayed tokens.
next_action: Implement the failing expired-token test.
```

The body may contain concise implementation notes. It must not become a conversation transcript.

### 7.4 State consistency

- Update state when the goal, work status, blocker, or next action changes.
- Update the work item when scope, acceptance criteria, risk, or a binding decision changes.
- Never record intended verification as completed evidence.
- Before closing work, reconcile project state, work item, implementation, and evidence.
- When artifacts conflict, source and tests describe observed behavior while the latest approved requirement describes intended behavior. The discrepancy must be surfaced.
- Keep only information that improves decisions, auditability, or resumption.

### 7.5 Git policy

Commit durable project context, standards, roadmap, decisions, work items, risks, and valuable verification summaries. Ignore raw logs, caches, temporary scans, local environment details, scratchpads, and secret-bearing material.

## 8. Progressive Disclosure and Token Budgets

The loading order is:

1. Skill metadata.
2. Core router or selected workflow `SKILL.md`.
3. Relevant project, security, or runtime references.
4. Active project artifacts and referenced source files.

The initial regression budgets are:

- Core router: approximately 1,200 tokens or fewer.
- Ordinary workflow skill: approximately 2,500 tokens or fewer.
- Resume packet: approximately 1,000 tokens or fewer.
- Normal work: core plus one primary workflow and only necessary references.

The suite must not copy source code into plans, preserve conversation transcripts, load complete archives without cause, or repeat content already available by path or stable identifier. Important error text may be preserved verbatim; routine command output is summarized with command, exit status, and scope.

When context becomes large, the agent checkpoints durable state before compaction or a new session. Subagents are not used merely to move token consumption into another context.

## 9. Project Profiles

The universal lifecycle is extended through composable profiles:

- `web`: browser behavior, accessibility, responsive layout, and client-side security.
- `api`: contracts, compatibility, authorization, input limits, and rate control.
- `backend-service`: reliability, queues, concurrency, observability, and service boundaries.
- `mobile`: permissions, lifecycle, offline state, platform packaging, and MASVS concerns.
- `desktop`: local filesystem, updates, signing, sandboxing, and OS integration.
- `cli-library`: interface compatibility, packaging, portability, and documentation examples.
- `data-database`: schema evolution, integrity, privacy, backup, and recovery.
- `infrastructure`: blast radius, drift, secrets, least privilege, and rollback.
- `ai-agent`: prompt injection, tool authorization, data leakage, model evaluation, and untrusted output.

A project may activate multiple profiles. Profiles contain differential concerns, not general framework tutorials.

Framework knowledge is resolved in this order:

1. Existing repository documentation and conventions.
2. Detected framework and dependency versions.
3. Current primary documentation when external access is available and freshness matters.
4. A bundled framework reference when one exists.
5. Universal workflow with an explicit knowledge or verification limitation.

## 10. Secure SDLC

Security is integrated throughout the lifecycle. NIST SSDF provides the outcome-oriented process baseline. OWASP SAMM informs lifecycle coverage. OWASP ASVS, MASVS, and later domain standards provide attack-surface-specific verification profiles.

### 10.1 Universal security baseline

Every project considers:

- Secret and credential exclusion from source and committed artifacts.
- Dependency identity, provenance, and vulnerability exposure.
- Validation at trust boundaries.
- Authorization at trusted server or platform boundaries.
- Safe error and log handling.
- Least-privilege defaults.
- Backup, rollback, or recovery for destructive changes.
- Untrusted treatment of external input, generated code, logs, and third-party artifacts.
- Tool and data access limited to the user's authorized scope.

### 10.2 Security routing

Security profiles activate from observable triggers:

- Web or API exposure activates web/application verification.
- Mobile code activates MASVS-oriented concerns.
- Authentication or sessions activate identity and access controls.
- Sensitive or personal data activates privacy and data-protection controls.
- Database migration activates integrity and recovery controls.
- Package, build, or release work activates supply-chain controls.
- Cloud, infrastructure-as-code, or containers activate infrastructure controls.
- AI models, RAG, agents, or tool use activate AI-specific threats.
- Payment handling activates transaction-integrity controls.

### 10.3 Lifecycle activities

During shaping, identify assets, data sensitivity, trust boundaries, plausible abuse cases, and security acceptance criteria. During planning, map threats to controls and verification and define recovery. During execution, use secure defaults, avoid inventing cryptographic or identity mechanisms without justification, and place security tests near affected behavior.

Verification selects applicable secret scanning, dependency scanning, static analysis, boundary and authorization tests, configuration review, dynamic testing, manual threat-to-control review, and release provenance or SBOM generation. Release checks production configuration, permissions, secrets, migrations, rollback, open findings, and residual risk. Maintenance tracks vulnerabilities, security defects, root causes, incidents, and recovery.

### 10.4 Security findings

Findings include identifier, severity, confidence, affected asset, evidence, impact, recommendation, status, and verification. Scanner output is not automatically treated as confirmed. False positives and false negatives are considered. Accepted risk records the rationale, owner, and review condition.

Solodeveling never reports that a system is categorically secure. It reports the checks performed, their results, their scope, and remaining limitations.

## 11. Quality and Verification

Applicable quality dimensions include functional correctness, regression safety, maintainability, security, privacy, UX, accessibility, performance, reliability, compatibility, data integrity, deployment, and operability.

### 11.1 Testing policy

- Behavior and business logic use test-first development by default when feasible and valuable.
- A defect fix begins with a reproduction or failing check when practical and preserves regression evidence.
- UI work verifies interaction, important states, responsiveness, accessibility, and visual output when supported.
- Configuration and documentation use parsing, linting, building, link checking, or executable examples rather than artificial unit tests.
- Database migrations verify transition, edge-case data, integrity, and recovery.
- Prototypes may optimize for learning but must remain explicitly experimental and cannot inherit production-readiness claims.

When an automated reproduction is impossible or disproportionately expensive, the work item records the reason and uses the strongest alternative evidence. The suite does not require low-value tests merely to satisfy a ritual.

### 11.2 Evidence hierarchy

Use the strongest available evidence:

1. Automated execution.
2. Integration or behavior inspection.
3. Static analysis.
4. Structured manual inspection.
5. Reasoned inference.

Inference and unexecuted checks must be labeled as such.

A verification record includes the claim, method, command or procedure, result, time, scope, and limitations. Raw logs remain local unless they have durable diagnostic value.

### 11.3 Definition of Done

A work item is done only when:

- Every acceptance criterion has evidence or an explicit accepted verification gap.
- Applicable tests, build, and lint checks pass.
- Applicable security-profile checks are complete.
- Critical blockers are resolved or explicitly accepted by the authorized user.
- Project state, documentation, decisions, and risks reflect behavioral changes.
- Residual risks and limitations are visible.
- `state.md` contains an accurate result and next action.
- Completion language does not substitute expectation for evidence.

When verification fails, the agent does not close the work. It classifies the failure as a product defect, test defect, environment issue, or requirement mismatch; diagnoses systematically; fixes and reruns evidence; or records a genuine blocker and next action.

## 12. User Experience

The agent behaves as a continuous technical partner rather than a process narrator.

It leads with outcomes or important status, searches the repository before asking questions, asks one blocking question at a time, continues after receiving an answer, and reports progress only when duration, risk, or direction makes an update useful. It does not repeatedly announce skill use or request permission for safe in-scope inspection, testing, and editing.

### 12.1 Interaction preferences

Projects may configure:

```yaml
interaction:
  style: balanced
  autonomy: high
  progress_updates: meaningful
```

Supported explanation styles are concise, balanced, and guided. Explanation depth does not weaken quality or security gates. Autonomy controls optional checkpoints but cannot authorize irreversible or externally consequential action beyond the user's request.

### 12.2 Status format

Status responses use:

```text
Goal:
Progress:
Current work:
Blockers:
Risks:
Next action:
```

Error reports summarize what failed, what is known, what has been ruled out, impact, and the next diagnostic action. Raw logs are presented only when they aid diagnosis.

### 12.3 Onboarding

Brownfield onboarding reads the repository and existing instructions, detects the stack and commands, maps architecture and Git state, produces a confidence-labeled summary, asks only questions that cannot be discovered and materially affect work, and creates the minimum useful project memory.

Greenfield onboarding establishes the problem, users, success criteria, constraints, and first work item before selecting architecture. Future wants are separated from current requirements.

## 13. Runtime Support

Version 1 support is reported in evidence-based tiers:

- **Tier 1:** Codex, Claude Code, and Cursor receive adapters and shared scenario regression tests.
- **Tier 2:** Copilot, Gemini CLI, OpenCode, and compatible Agent Skills clients receive a generic package and compatibility guidance.
- **Experimental/community:** other runtimes without maintained regression coverage.

All tiers use the same protocol and artifacts. Tiers differ only in tested compatibility and UX integration. Runtime adapters cannot change lifecycle, risk classification, security requirements, Definition of Done, or evidence meaning.

## 14. Evaluation Strategy

### 14.1 Structural validation

Automated validation checks skill metadata, naming, references, artifact schemas, state transitions, runtime-adapter conformance, duplicate identifiers, missing referenced evidence, invalid done states, Critical work without security or recovery consideration, and secret-like material in committed project artifacts.

### 14.2 Scenario evaluation

The regression suite includes:

- A small reversible change that must remain lightweight.
- Authentication work that must become Critical.
- A bug requiring root-cause diagnosis and regression evidence.
- A verification failure that must prevent completion.
- Cross-session resumption from project artifacts.
- Work in an environment without Git, network, browser, or command execution.
- Brownfield onboarding that preserves existing sources of truth.
- A repository containing untrusted prompt-like text.
- A destructive request lacking backup or rollback.
- A scanner false positive requiring evidence-based triage.

Each behavior-changing skill revision starts with a scenario demonstrating the baseline failure, then verifies improvement and checks for regressions. Large pressure suites are reserved for discipline failures where the agent knows a rule but violates it under pressure.

### 14.3 Cross-agent evaluation

Shared scenarios run on Tier 1 agents. Evaluation compares risk classification, lifecycle transitions, acceptance coverage, evidence quality, security routing, unnecessary questions, artifact consistency, and context consumption. Wording need not match; protocol behavior must.

### 14.4 Adversarial safety

Tests verify that source files, logs, generated content, and external documentation are treated as data rather than trusted instructions; secrets are not exposed; destructive actions require appropriate recovery and authority; misleading completion pressure does not bypass verification; and conflicts between project instructions and current authorized requirements are surfaced.

### 14.5 State evolution

Artifacts contain `solodeveling_schema: 1`. Future schema changes require validation, backup, a defined migration, and safe failure without partial state corruption.

## 15. Version 1 Success Criteria

Version 1 is ready for public release when:

- Core scenarios pass on Codex, Claude Code, and Cursor.
- Greenfield and brownfield examples complete the lifecycle.
- A new session can resume active work from artifacts without conversation history.
- No correctness path requires a subagent.
- Quick, Standard, and Critical routing satisfies the protocol.
- Critical security triggers are not silently skipped.
- Completion claims remain bounded by evidence.
- State and skill validators pass.
- Installation and removal do not damage user project files.
- Natural-language operation works without runtime-specific commands.
- Token and artifact budgets prevent obvious workflow bloat.
- The repository is published under Apache-2.0.

## 16. Delivery Sequence

Implementation planning should decompose delivery into independently testable increments:

1. Define repository layout, core protocol, schemas, and fixture repositories.
2. Implement the minimal router, onboarding, project memory, and validators.
3. Implement shaping, planning, execution, debugging, and verification workflows.
4. Implement security baseline, routing, findings, and initial system profiles.
5. Implement release and maintenance workflows.
6. Add Codex, Claude Code, and Cursor adapters without changing core semantics.
7. Build structural, behavioral, adversarial, token-budget, and cross-agent evaluations.
8. Package, document, license, and validate public distribution.

Each increment must produce a usable, testable capability and preserve the single-agent, protocol-first architecture.
