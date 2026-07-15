---
solodeveling_schema: 1
current_goal: Evaluate Solodeveling behavior across Tier 1 coding agents.
active_work: []
blockers: []
risks:
- cursor-agent is unavailable in the current environment, so a complete Tier 1 live matrix cannot yet run locally.
- Live agent evaluation uses external services, may incur usage, and produces nondeterministic outputs requiring bounded scoring.
- Multi-runtime co-installation may surface duplicate skills when a runtime scans compatibility paths.
next_action: Shape WORK-006 for shared behavioral scenarios, bounded scoring, live Codex and Claude runs, and an explicit Cursor execution path.
---
# State

Safe runtime adapters are implemented as WORK-005. They materialize one canonical
skill suite without changing protocol semantics and refuse unsafe overwrite or
removal. Live Tier 1 behavioral support remains unverified and is the next increment.
Solodeveling remains the active workflow; Superpowers is not used.
