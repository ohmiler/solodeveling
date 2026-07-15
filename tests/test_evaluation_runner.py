from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from solodeveling_protocol.evaluation import ResultState, load_scenarios
from solodeveling_protocol.evaluation_runner import (
    replay_response,
    run_live_scenario,
    sanitized_result_document,
)


SCENARIOS = Path("evals/scenarios/core.yaml")
SCHEMA = Path("evals/evaluation-response.schema.json")


def passing_response(scenario) -> dict[str, object]:
    expected = scenario.expected
    return {
        "scenario_id": scenario.identifier,
        "level": expected.level,
        "workflow": expected.workflow,
        "action": expected.action,
        "requires_authority": expected.requires_authority,
        "requires_recovery": expected.requires_recovery,
        "completion_allowed": expected.completion_allowed,
        "signals": list(expected.signals),
        "acceptance_summary": ["Use the selected bounded workflow."],
        "limitations": ["No software action was performed."],
        "next_action": "Gather the required evidence.",
    }


def codex_executor(response, *, mutate: bool = False):
    def execute(command, cwd):
        if mutate:
            (cwd / "mutated.txt").write_text("unsafe", encoding="utf-8")
        output_index = command.argv.index("--output-last-message") + 1
        Path(command.argv[output_index]).write_text(
            json.dumps(response), encoding="utf-8"
        )
        return subprocess.CompletedProcess(command.argv, 0, "", "")

    return execute


def test_live_pass_requires_semantics_and_unchanged_fixture(tmp_path: Path) -> None:
    scenario = load_scenarios(SCENARIOS)[0]

    result = run_live_scenario(
        "codex",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: f"/fake/{name}",
        executor=codex_executor(passing_response(scenario)),
        version_reader=lambda runtime, executable: "test-version",
    )

    assert result.state is ResultState.LIVE_PASS
    assert result.score is not None and result.score.passed
    assert result.integrity_before == result.integrity_after
    assert result.response == passing_response(scenario)
    assert result.runtime_version == "test-version"


def test_codex_receives_compatible_schema_copy(tmp_path: Path) -> None:
    scenario = load_scenarios(SCENARIOS)[0]

    def inspect_schema(command, cwd):
        schema_index = command.argv.index("--output-schema") + 1
        schema = json.loads(Path(command.argv[schema_index]).read_text("utf-8"))
        assert "$schema" not in schema
        assert "uniqueItems" not in schema["properties"]["signals"]
        return codex_executor(passing_response(scenario))(command, cwd)

    result = run_live_scenario(
        "codex",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: f"/fake/{name}",
        executor=inspect_schema,
        version_reader=lambda runtime, executable: "test-version",
    )

    assert result.state is ResultState.LIVE_PASS


def test_failure_state_reads_claude_json_stdout(tmp_path: Path) -> None:
    scenario = load_scenarios(SCENARIOS)[0]

    def not_logged_in(command, cwd):
        stdout = json.dumps(
            {"is_error": True, "result": "Not logged in · Please run /login"}
        )
        return subprocess.CompletedProcess(command.argv, 1, stdout, "")

    result = run_live_scenario(
        "claude-code",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: f"/fake/{name}",
        executor=not_logged_in,
        version_reader=lambda runtime, executable: "test-version",
    )

    assert result.state is ResultState.AUTH_FAILURE



def test_fixture_mutation_is_safety_failure_even_with_correct_response(
    tmp_path: Path,
) -> None:
    scenario = load_scenarios(SCENARIOS)[0]

    result = run_live_scenario(
        "codex",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: f"/fake/{name}",
        executor=codex_executor(passing_response(scenario), mutate=True),
        version_reader=lambda runtime, executable: "test-version",
    )

    assert result.state is ResultState.SAFETY_FAILURE
    assert result.integrity_before != result.integrity_after
    assert result.response is None


def test_missing_executable_is_unavailable_without_executor_call(
    tmp_path: Path,
) -> None:
    scenario = load_scenarios(SCENARIOS)[0]
    called = False

    def execute(command, cwd):
        nonlocal called
        called = True
        raise AssertionError("executor must not run")

    result = run_live_scenario(
        "cursor",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: None,
        executor=execute,
        version_reader=lambda runtime, executable: "unreachable",
    )

    assert result.state is ResultState.UNAVAILABLE
    assert not called
    assert result.response is None


def test_timeout_is_distinct_and_does_not_leak_raw_prompt(tmp_path: Path) -> None:
    scenario = load_scenarios(SCENARIOS)[0]

    def timeout(command, cwd):
        raise subprocess.TimeoutExpired(command.argv, command.timeout_seconds)

    result = run_live_scenario(
        "claude-code",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: f"/fake/{name}",
        executor=timeout,
        version_reader=lambda runtime, executable: "test-version",
    )

    assert result.state is ResultState.TIMEOUT
    assert scenario.prompt not in result.diagnostic


def test_secret_output_becomes_safety_failure_and_is_not_retained(
    tmp_path: Path,
) -> None:
    scenario = load_scenarios(SCENARIOS)[0]
    unsafe = passing_response(scenario)
    unsafe["next_action"] = "Use AKIAABCDEFGHIJKLMNOP"

    result = run_live_scenario(
        "codex",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: f"/fake/{name}",
        executor=codex_executor(unsafe),
        version_reader=lambda runtime, executable: "test-version",
    )

    assert result.state is ResultState.SAFETY_FAILURE
    assert result.response is None
    assert "aws-access-key" in result.diagnostic
    assert "AKIAABCDEFGHIJKLMNOP" not in result.diagnostic


def test_replay_is_scored_but_never_labeled_live() -> None:
    scenario = load_scenarios(SCENARIOS)[0]

    passed = replay_response(
        "codex",
        scenario,
        passing_response(scenario),
        schema_path=SCHEMA,
    )
    failed_response = passing_response(scenario)
    failed_response["completion_allowed"] = True
    failed = replay_response(
        "codex",
        scenario,
        failed_response,
        schema_path=SCHEMA,
    )

    assert passed.state is ResultState.REPLAY_PASS
    assert failed.state is ResultState.REPLAY_FAILURE
    assert passed.live is False
    assert failed.live is False


def test_sanitized_document_excludes_process_output_and_prompts(
    tmp_path: Path,
) -> None:
    scenario = load_scenarios(SCENARIOS)[0]
    result = run_live_scenario(
        "codex",
        scenario,
        source_skills=Path("skills"),
        schema_path=SCHEMA,
        temp_parent=tmp_path,
        claude_budget_usd=0.25,
        executable_finder=lambda name: f"/fake/{name}",
        executor=codex_executor(passing_response(scenario)),
        version_reader=lambda runtime, executable: "test-version",
    )

    document = sanitized_result_document([result])
    encoded = json.dumps(document)

    assert scenario.prompt not in encoded
    assert "stdout" not in encoded
    assert "stderr" not in encoded
    assert document["live"] is True
    assert document["results"][0]["state"] == "live-pass"
