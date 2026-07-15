from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

from solodeveling_protocol.adapters import install_adapter
from solodeveling_protocol.evaluation import (
    EvaluationError,
    EvaluationScenario,
    EvaluationScore,
    ResultState,
    RuntimeCommand,
    build_prompt,
    build_runtime_command,
    classify_process_failure,
    extract_runtime_response,
    score_response,
    runtime_response_schema,
    validate_safe_output,
    workspace_digest,
)


Executor = Callable[
    [RuntimeCommand, Path],
    subprocess.CompletedProcess[str],
]
ExecutableFinder = Callable[[str], str | None]
VersionReader = Callable[[str, str], str]


@dataclass(frozen=True)
class ScenarioResult:
    runtime: str
    scenario_id: str
    state: ResultState
    live: bool
    runtime_version: str | None
    score: EvaluationScore | None
    integrity_before: str | None
    integrity_after: str | None
    response: dict[str, object] | None
    diagnostic: str
    cost_usd: float | None = None


def _safe_environment() -> dict[str, str]:
    allowed = {
        "APPDATA",
        "CLAUDE_CONFIG_DIR",
        "CODEX_HOME",
        "COMSPEC",
        "HOMEDRIVE",
        "HOMEPATH",
        "LANG",
        "LC_ALL",
        "LOCALAPPDATA",
        "NO_COLOR",
        "PATH",
        "PATHEXT",
        "PROGRAMFILES",
        "PROGRAMFILES(X86)",
        "SSL_CERT_DIR",
        "SSL_CERT_FILE",
        "SYSTEMROOT",
        "TEMP",
        "TERM",
        "TMP",
        "USERPROFILE",
        "USERNAME",
        "WINDIR",
    }
    return {key: value for key, value in os.environ.items() if key.upper() in allowed}


def _default_executor(
    command: RuntimeCommand,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command.argv,
        input=command.stdin,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=command.timeout_seconds,
        check=False,
        shell=False,
        env=_safe_environment(),
    )


def _default_version_reader(runtime: str, executable: str) -> str:
    try:
        result = subprocess.run(
            (executable, "--version"),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
            shell=False,
            env=_safe_environment(),
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0][:200] if output else "unknown"


def _executable_name(runtime: str) -> str:
    return {
        "codex": "codex",
        "claude-code": "claude",
        "cursor": "cursor-agent",
    }.get(runtime) or ""


def _write_fixture(project_root: Path, scenario: EvaluationScenario) -> None:
    project_root.mkdir(parents=True)
    memory = project_root / ".solodeveling"
    memory.mkdir()
    state = (
        "---\n"
        "solodeveling_schema: 1\n"
        "current_goal: Evaluate one bounded scenario.\n"
        "active_work: []\n"
        "blockers: []\n"
        "risks: []\n"
        "next_action: Classify the scenario without changing files.\n"
        "---\n"
        "# State\n\n"
        f"Evaluation fixture for {scenario.identifier}. No software action is authorized.\n"
    )
    (memory / "state.md").write_text(state, encoding="utf-8")
    (project_root / "SCENARIO.md").write_text(
        f"# {scenario.title}\n\n{scenario.prompt}\n",
        encoding="utf-8",
    )


def _safe_diagnostic(error: EvaluationError) -> tuple[ResultState, str]:
    message = str(error)
    if message.startswith("secret-like output rejected:"):
        return ResultState.SAFETY_FAILURE, message
    return ResultState.INVALID_OUTPUT, message[:500]


def _claude_cost(stdout: str) -> float | None:
    try:
        validate_safe_output(stdout)
        wrapper = json.loads(stdout)
    except (EvaluationError, json.JSONDecodeError):
        return None
    if not isinstance(wrapper, dict):
        return None
    value = wrapper.get("total_cost_usd")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def run_live_scenario(
    runtime: str,
    scenario: EvaluationScenario,
    *,
    source_skills: Path,
    schema_path: Path,
    temp_parent: Path,
    claude_budget_usd: float,
    executable_finder: ExecutableFinder = shutil.which,
    executor: Executor = _default_executor,
    version_reader: VersionReader = _default_version_reader,
) -> ScenarioResult:
    executable_name = _executable_name(runtime)
    if not executable_name:
        raise EvaluationError(f"unsupported runtime: {runtime}")
    executable = executable_finder(executable_name)
    if executable is None:
        return ScenarioResult(
            runtime=runtime,
            scenario_id=scenario.identifier,
            state=ResultState.UNAVAILABLE,
            live=True,
            runtime_version=None,
            score=None,
            integrity_before=None,
            integrity_after=None,
            response=None,
            diagnostic=f"{executable_name} executable is unavailable",
        )
    version = version_reader(runtime, executable)
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    compatible_schema = runtime_response_schema(runtime, schema)
    prompt = build_prompt(runtime, scenario, compatible_schema)

    Path(temp_parent).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f"solodeveling-evaluation-{runtime}-",
        dir=temp_parent,
    ) as temporary:
        root = Path(temporary)
        project = root / "project"
        output = root / "response.json"
        runtime_schema_path = Path(schema_path).resolve()
        if runtime == "codex":
            runtime_schema_path = root / "runtime-response.schema.json"
            runtime_schema_path.write_text(
                json.dumps(compatible_schema, separators=(",", ":")),
                encoding="utf-8",
            )
        _write_fixture(project, scenario)
        install_adapter(Path(source_skills), project, runtime)
        before = workspace_digest(project)
        command = build_runtime_command(
            runtime,
            project_root=project,
            schema_path=runtime_schema_path,
            output_path=output,
            prompt=prompt,
            claude_budget_usd=claude_budget_usd,
        )
        command = replace(
            command,
            argv=(executable, *command.argv[1:]),
        )
        try:
            process = executor(command, project)
        except subprocess.TimeoutExpired:
            after = workspace_digest(project)
            state = (
                ResultState.SAFETY_FAILURE
                if before != after
                else ResultState.TIMEOUT
            )
            return ScenarioResult(
                runtime=runtime,
                scenario_id=scenario.identifier,
                state=state,
                live=True,
                runtime_version=version,
                score=None,
                integrity_before=before,
                integrity_after=after,
                response=None,
                diagnostic=(
                    "fixture changed before timeout"
                    if state is ResultState.SAFETY_FAILURE
                    else f"runtime exceeded {command.timeout_seconds}s timeout"
                ),
            )
        except OSError:
            after = workspace_digest(project)
            return ScenarioResult(
                runtime=runtime,
                scenario_id=scenario.identifier,
                state=ResultState.RUNTIME_FAILURE,
                live=True,
                runtime_version=version,
                score=None,
                integrity_before=before,
                integrity_after=after,
                response=None,
                diagnostic="runtime process could not be started",
            )

        after = workspace_digest(project)
        if before != after:
            return ScenarioResult(
                runtime=runtime,
                scenario_id=scenario.identifier,
                state=ResultState.SAFETY_FAILURE,
                live=True,
                runtime_version=version,
                score=None,
                integrity_before=before,
                integrity_after=after,
                response=None,
                diagnostic="runtime modified the isolated evaluation fixture",
            )
        if process.returncode != 0:
            failure_output = process.stdout + "\n" + process.stderr
            state = classify_process_failure(failure_output)
            try:
                validate_safe_output(failure_output)
                diagnostic = f"{state.value}: process exited {process.returncode}"
            except EvaluationError as error:
                state, diagnostic = _safe_diagnostic(error)
            return ScenarioResult(
                runtime=runtime,
                scenario_id=scenario.identifier,
                state=state,
                live=True,
                runtime_version=version,
                score=None,
                integrity_before=before,
                integrity_after=after,
                response=None,
                diagnostic=diagnostic,
            )
        try:
            response = extract_runtime_response(runtime, process.stdout, output)
        except EvaluationError as error:
            state, diagnostic = _safe_diagnostic(error)
            return ScenarioResult(
                runtime=runtime,
                scenario_id=scenario.identifier,
                state=state,
                live=True,
                runtime_version=version,
                score=None,
                integrity_before=before,
                integrity_after=after,
                response=None,
                diagnostic=diagnostic,
                cost_usd=_claude_cost(process.stdout)
                if runtime == "claude-code"
                else None,
            )

        score = score_response(scenario, response, schema)
        state = (
            ResultState.LIVE_PASS
            if score.passed
            else ResultState.SEMANTIC_FAILURE
        )
        return ScenarioResult(
            runtime=runtime,
            scenario_id=scenario.identifier,
            state=state,
            live=True,
            runtime_version=version,
            score=score,
            integrity_before=before,
            integrity_after=after,
            response=response,
            diagnostic=(
                "all deterministic semantic gates passed"
                if score.passed
                else "semantic gates failed: " + ", ".join(score.failures)
            ),
            cost_usd=_claude_cost(process.stdout)
            if runtime == "claude-code"
            else None,
        )


def replay_response(
    runtime: str,
    scenario: EvaluationScenario,
    response: dict[str, object],
    *,
    schema_path: Path,
) -> ScenarioResult:
    serialized = json.dumps(response, ensure_ascii=False)
    try:
        validate_safe_output(serialized)
    except EvaluationError as error:
        state, diagnostic = _safe_diagnostic(error)
        return ScenarioResult(
            runtime=runtime,
            scenario_id=scenario.identifier,
            state=state,
            live=False,
            runtime_version=None,
            score=None,
            integrity_before=None,
            integrity_after=None,
            response=None,
            diagnostic=diagnostic,
        )
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    score = score_response(scenario, response, schema)
    return ScenarioResult(
        runtime=runtime,
        scenario_id=scenario.identifier,
        state=(
            ResultState.REPLAY_PASS
            if score.passed
            else ResultState.REPLAY_FAILURE
        ),
        live=False,
        runtime_version=None,
        score=score,
        integrity_before=None,
        integrity_after=None,
        response=response,
        diagnostic=(
            "replay semantic gates passed"
            if score.passed
            else "replay semantic gates failed: " + ", ".join(score.failures)
        ),
    )


def sanitized_result_document(
    results: Iterable[ScenarioResult],
) -> dict[str, object]:
    items = list(results)
    return {
        "solodeveling_eval_result_schema": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "live": any(result.live for result in items),
        "results": [
            {
                "runtime": result.runtime,
                "runtime_version": result.runtime_version,
                "scenario_id": result.scenario_id,
                "state": result.state.value,
                "live": result.live,
                "score": result.score.score if result.score else None,
                "critical_gates_passed": (
                    result.score.critical_gates_passed
                    if result.score
                    else None
                ),
                "failures": list(result.score.failures) if result.score else [],
                "integrity_unchanged": (
                    result.integrity_before == result.integrity_after
                    if result.integrity_before is not None
                    else None
                ),
                "cost_usd": result.cost_usd,
                "diagnostic": result.diagnostic,
                "response": result.response,
            }
            for result in items
        ],
    }
