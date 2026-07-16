# Solodeveling

> **One agent. The right amount of process. From a tiny fix to a verified release.**

Solodeveling is a single-agent-first software delivery protocol for solo developers.
It keeps a single primary agent oriented across discovery, planning,
implementation, verification, security, release, and maintenance. Small, safe work
can stay ephemeral. Resumable or risky work gains durable memory and stronger gates
only when the risk justifies them.

Use the same canonical skill suite with Codex, Claude Code, Cursor, and generic Agent
Skills clients. Subagents may still be used when useful, but Solodeveling does not
require a multi-agent team to complete the ordinary workflow.

**Status:** 0.1.0 alpha is published on
[npm](https://www.npmjs.com/package/solodeveling),
[PyPI](https://pypi.org/project/solodeveling/), and as an
[immutable GitHub Release](https://github.com/ohmiler/solodeveling/releases/tag/v0.1.0).
Codex and Claude Code have each passed one bounded representative live scenario.
Cursor has structural adapter evidence only because `cursor-agent` was unavailable.
Tier 1 remains unverified until the full core scenario matrix passes.

## Quick start

Node.js users need one command:

~~~console
npx solodeveling install
~~~

For a permanent command:

~~~console
npm install -g solodeveling
solodeveling install
~~~

Python users can run it without a permanent install or install it as a tool:

~~~console
uvx solodeveling install
uv tool install solodeveling
pipx install solodeveling
~~~

All channels expose one public command: `solodeveling`. See
[Installation](docs/installation.md) for prerequisites, platform support, upgrades,
and integrity controls.

## Why Solodeveling

- **Single-agent-first:** keep one accountable primary agent instead of requiring
  delegation, role hand-offs, or parallel workers for ordinary delivery.
- **Quiet for small work:** a safe Quick task can use zero required questions, zero
  project-memory writes, and verification proportional to its impact.
- **Durable when it matters:** resumable work records current state; Critical work
  adds explicit security, recovery, evidence, and release boundaries.
- **Complete delivery lifecycle:** use one vocabulary from discovery and coding
  through debugging, verification, release, and maintenance.
- **Project-local and portable:** install the same skills into the runtimes detected
  in the repository without searching for or modifying global agent installations.

| Work level | Default behavior | Persistent overhead |
| --- | --- | --- |
| Quick | Act immediately when intent is clear; escalate if risk appears | None required for safe ephemeral work |
| Standard | Shape, plan, implement, and verify with resumable state | Compact current state and one active work item |
| Critical | Add security, recovery, provenance, and explicit authorization gates | Auditable work and evidence records |

## How it compares

These projects have different defaults rather than a universal winner. The table
summarizes their public documentation as of July 2026; it is not a controlled speed
or quality benchmark.

| Project | Documented default | Strongest fit | Main contrast with Solodeveling |
| --- | --- | --- | --- |
| **Solodeveling** | One primary agent with risk-scaled workflow and memory | Solo maintainers balancing tiny fixes with security, release, and maintenance work | Quick work may stay ephemeral; compact state expands into auditable evidence only when needed |
| [Superpowers](https://github.com/obra/superpowers) | Complete development methodology built from composable skills | Developers who want modular engineering skills, planning, review, and subagent-oriented paths where supported | Solodeveling keeps one accountable primary agent as the ordinary default and does not require delegation |
| [GSD](https://github.com/gsd-build/get-shit-done) | Lightweight meta-prompting, context engineering, and spec-driven execution | Longer builds where countering context degradation is the main concern | Solodeveling organizes persistence and verification around task risk and the full delivery lifecycle |
| [GitHub Spec Kit](https://github.github.com/spec-kit/) | Specification-centered flow: Spec, Plan, Tasks, Implement | Work where the specification should remain the primary source of truth across many agent integrations | Solodeveling allows safe Quick work to skip a persistent spec while retaining escalation paths |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | Scale-adaptive agile workflows with 12+ specialist roles and 34+ workflows | Users who want guided agile personas, modules, and a broad workflow ecosystem | Solodeveling favors one primary agent and a smaller common vocabulary across the lifecycle |

### What faster means here

Solodeveling optimizes **workflow overhead**, not unmeasured model intelligence. It
does not yet claim to complete coding tasks faster than the alternatives above. A
fair claim requires the same repository, model, prompt, task set, and repeated runs.

| Evidence from this repository | Observed result | What it supports |
| --- | --- | --- |
| Ephemeral documentation dogfood | Zero user questions and no Quick-task memory artifacts | Small clear work can avoid coordination and persistence ceremony |
| Memory-only GitHub CI | Focused validation jobs completed in 18-20 seconds | Memory updates do not trigger package, native, or full test jobs |
| Docs-only GitHub CI | Complete Python regression job completed in 23-33 seconds | Documentation retains meaningful verification without the cross-platform package matrix |
| Bounded live portability scenario | Codex and Claude Code each scored 1.0 on one Quick scenario | The canonical behavior can transfer across two available runtimes; it does not establish full Tier 1 support |

See [EVIDENCE-006](.solodeveling/evidence/EVIDENCE-006.md),
[EVIDENCE-019](.solodeveling/evidence/EVIDENCE-019.md), and
[EVIDENCE-025](.solodeveling/evidence/EVIDENCE-025.md) for methods and limitations.

## Who it is for

Choose Solodeveling when you:

- maintain a project alone or with one primary coding agent;
- want tiny fixes to stay lightweight without losing discipline on risky work;
- need continuity across sessions without accumulating a document for every action;
- own both implementation and release or maintenance responsibilities; or
- switch between Codex, Claude Code, Cursor, or another Agent Skills client.

Another approach may fit better when you want specialized personas and multi-agent
coordination as the default, require a formal specification artifact for every
change, or need a mature ecosystem with a much larger behavioral evidence base.

## Automatic project installation

The ordinary workflow has no required options:

~~~console
solodeveling install
solodeveling check
solodeveling uninstall
~~~

Solodeveling first reuses any installation it already manages. Otherwise it detects
project-local Codex/Agent Skills, Claude Code, and Cursor directories. It installs
every distinct runtime found, and defaults to the standard `.agents/skills` path when
the project has no runtime marker. It never searches global executables or writes
outside the current project.

Installation validates the skill suite, preflights every detected target, rejects
symlinks and path traversal, refuses unmanaged collisions, copies files atomically,
and records managed hashes. Check detects missing, changed, or unexpected managed
files. Uninstall removes only unchanged managed files and has no force-delete mode.

Start a fresh agent session after first installation, then invoke `$solodeveling` in
Codex, `/solodeveling` in Claude Code or Cursor, or the client-defined invocation in
another Agent Skills runtime.

### Advanced overrides

Automation and unusual workspaces may still select an exact runtime or another
project. `--dry-run` remains available as an optional preview, not a required step:

~~~console
solodeveling install --runtime claude-code --project-root PATH
solodeveling install --runtime cursor --dry-run
~~~

## Other commands

The install flow stays short; project memory and evaluation remain explicit:

~~~console
solodeveling init
solodeveling validate .
solodeveling eval probe
solodeveling version
~~~

Live evaluation can consume model-service usage or API credits, so review
[Cross-agent evaluation](docs/cross-agent-evaluation.md) before authorizing a live
run.

## Security and support boundaries

The npm launcher has no runtime dependencies and no install lifecycle script. On an
explicit invocation it selects an exact-version native artifact, downloads only from
the versioned GitHub Release, verifies its bundled size and SHA-256, caches it, and
executes it without a shell. Windows, macOS, and Linux on x64 and arm64 are release
targets only after their CI builds and native smoke tests pass. Unsupported targets
fail closed and show the Python-tool fallback.

Solodeveling applies risk-scaled verification and Secure SDLC guidance, but installing
it does not make a project categorically secure or compliant. Hashes detect byte
changes; they do not by themselves prove publisher identity. No telemetry is
collected and no publishing credentials are included.

No tag, GitHub Release, npm package, or PyPI package is created by ordinary CI.
External publication requires a reviewed source revision and separate explicit
authorization.

## License

Apache-2.0. See [LICENSE](LICENSE).
