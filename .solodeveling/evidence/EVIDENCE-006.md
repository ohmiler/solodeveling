---
solodeveling_schema: 1
id: EVIDENCE-006
work_item: WORK-006
claim: Solodeveling provides a deterministic, isolated, budget-bounded cross-agent evaluation harness, and one representative Quick scenario passed live on both Codex and Claude Code without fixture mutation; Cursor was unavailable and Tier 1 remains unverified.
method: Versioned scenarios and strict response/result schemas, deterministic exact-field scoring, adversarial unit tests, safe argv and stdin construction, environment allowlisting, disposable native-adapter fixtures, before-and-after workspace hashing, secret-output rejection, record/replay, executable probing, bounded live runs, full regression, official skill validation, protocol validation, fresh package build and entry-point inspection, compilation, dependency health, and diff inspection.
command: python -m pytest -q; python scripts/validate_skill_suite.py; quick_validate.py for all ten skills; solodeveling protocol validation; solodeveling-eval probe and dry-run; bounded solodeveling-eval live runs for quick-local-documentation; uv build --wheel; inspect wheel and entry_points.txt; compileall; pip check; git diff --check
result: passed
scope: Nine shared behavioral scenarios, runtime-compatible schema materialization for Codex and Claude Code, deterministic semantic gates, distinct runtime result states, no-shell subprocess execution, isolated fixtures, integrity enforcement, sanitized local results, replay, contributor CLI, documentation, one live Codex pass, one live Claude pass after contract clarification, and an explicit Cursor unavailable result.
limitations:
- Only quick-local-documentation ran live. The other eight core scenarios, including the other two smoke scenarios, were not executed because the user approved a total Claude evaluation estimate near USD 0.25.
- Claude's first semantic result failed completion_allowed and need-verification. Clarifying those field descriptions without weakening the rubric produced a passing retry; this is one pass after one failure, not evidence of statistical stability.
- Claude reported estimated costs of USD 0.109709 and USD 0.111902, totaling USD 0.221611. The authenticated account was Claude Pro, so this estimate represents included plan usage rather than a separately verified API invoice.
- cursor-agent was unavailable locally. Cursor behavioral support and complete Tier 1 support are not verified.
- Live agent output is nondeterministic. One representative pass per available runtime does not establish full scenario, model-version, repetition, or cross-session coverage.
- Target runtimes were evaluation subjects only and were never used as implementation subagents.
---
# Verification summary

On 2026-07-15, 130 tests passed. The suite validator, all ten official skill
validations, protocol validation, compilation, dependency health, and diff checks
passed. A fresh wheel contained evaluation.py, evaluation_cli.py,
evaluation_runner.py, and the solodeveling-eval entry point; its SHA-256 was
965382fe28150cd755645f5727acda99a4489fe668e397fe8c44fb2cd6f103e0.

Codex CLI 0.144.4 and Claude Code 2.1.205 each passed the
quick-local-documentation scenario with score 1.0, all critical gates passing, and
unchanged fixture hashes. Cursor's three smoke probes recorded unavailable because
cursor-agent was not installed. Raw live results remained local under ignored
evals/results paths.

## Security and recovery evidence

Every live run used a disposable project populated only with canonical Solodeveling
skills and synthetic scenario data. Codex ran ephemeral and read-only; Claude ran in
plan mode with only Read, no session persistence, a timeout, and a budget ceiling.
The harness passed prompts through stdin with shell execution disabled, excluded API
key environment variables, rejected secret-like output before response retention,
and compared complete fixture hashes before accepting a result. All accepted Codex
and Claude fixtures were unchanged. Failed schema, authentication, and semantic
attempts also reported unchanged fixtures and were never copied back to the
repository.
