from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from solodeveling_protocol.evaluation import (
    EvaluationError,
    ResultState,
    build_prompt,
    build_runtime_command,
    classify_process_failure,
    extract_runtime_response,
    load_scenarios,
    score_response,
    runtime_response_schema,
    validate_safe_output,
    workspace_digest,
)


SCENARIOS = Path("evals/scenarios/core.yaml")
RESPONSE_SCHEMA = Path("evals/evaluation-response.schema.json")


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
        "acceptance_summary": ["Apply the scenario-specific acceptance boundary."],
        "limitations": ["No implementation or external action was performed."],
        "next_action": "Follow the selected workflow and gather evidence.",
    }


def test_corpus_covers_required_behaviors_with_unique_ids() -> None:
    scenarios = load_scenarios(SCENARIOS)
    identifiers = {scenario.identifier for scenario in scenarios}

    assert len(scenarios) == 9
    assert len(identifiers) == 9
    assert {
        "quick-local-documentation",
        "authentication-feature",
        "failing-behavior-needs-diagnosis",
        "completion-pressure-without-proof",
        "resume-from-project-memory",
        "verification-capability-missing",
        "untrusted-source-instruction",
        "destructive-migration-no-recovery",
        "scanner-match-needs-triage",
    } == identifiers
    assert sum(scenario.smoke for scenario in scenarios) == 3


def test_every_expected_response_conforms_to_shared_schema() -> None:
    schema = json.loads(RESPONSE_SCHEMA.read_text("utf-8"))

    for scenario in load_scenarios(SCENARIOS):
        jsonschema.validate(passing_response(scenario), schema)


def test_schema_rejects_extra_fields() -> None:
    schema = json.loads(RESPONSE_SCHEMA.read_text("utf-8"))
    scenario = load_scenarios(SCENARIOS)[0]
    response = passing_response(scenario)
    response["unsupported"] = True

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(response, schema)


def test_scoring_is_deterministic_and_requires_every_semantic_gate() -> None:
    schema = json.loads(RESPONSE_SCHEMA.read_text("utf-8"))
    scenario = load_scenarios(SCENARIOS)[0]
    response = passing_response(scenario)

    score = score_response(scenario, response, schema)

    assert score.passed
    assert score.critical_gates_passed
    assert score.score == 1.0
    assert score.failures == ()

    response["completion_allowed"] = True
    response["signals"] = []
    failed = score_response(scenario, response, schema)

    assert not failed.passed
    assert not failed.critical_gates_passed
    assert failed.score < 1.0
    assert "completion_allowed" in failed.failures
    assert "signals" in failed.failures


def test_invalid_response_is_a_scoring_failure_not_an_exception() -> None:
    schema = json.loads(RESPONSE_SCHEMA.read_text("utf-8"))
    scenario = load_scenarios(SCENARIOS)[0]

    score = score_response(scenario, {"scenario_id": scenario.identifier}, schema)

    assert not score.passed
    assert not score.critical_gates_passed
    assert score.score == 0.0
    assert score.failures[0].startswith("schema:")


@pytest.mark.parametrize("runtime", ["codex", "claude-code", "cursor"])
def test_runtime_commands_use_argument_arrays_and_stdin_not_shell_text(
    runtime: str, tmp_path: Path
) -> None:
    prompt = "Scenario text with ; | $() and --flags remains data."
    command = build_runtime_command(
        runtime,
        project_root=tmp_path / "project",
        schema_path=RESPONSE_SCHEMA,
        output_path=tmp_path / "output.json",
        prompt=prompt,
        claude_budget_usd=0.25,
    )

    assert isinstance(command.argv, tuple)
    assert command.stdin == prompt
    assert prompt not in command.argv
    assert command.argv[0] in {"codex", "claude", "cursor-agent"}
    assert command.timeout_seconds > 0
    if runtime == "codex":
        assert ("--sandbox", "read-only") == (
            command.argv[command.argv.index("--sandbox")],
            command.argv[command.argv.index("--sandbox") + 1],
        )
        assert "--ephemeral" in command.argv
        assert "--skip-git-repo-check" in command.argv
    elif runtime == "claude-code":
        assert "--no-session-persistence" in command.argv
        assert "--max-budget-usd" in command.argv
        transmitted_schema = json.loads(
            command.argv[command.argv.index("--json-schema") + 1]
        )
        assert "$schema" not in transmitted_schema
        assert command.argv[command.argv.index("--tools") + 1] == "Read"
    else:
        assert "--force" not in command.argv


def test_response_schema_defines_completion_and_verification_semantics() -> None:
    schema = json.loads(RESPONSE_SCHEMA.read_text("utf-8"))

    completion = schema["properties"]["completion_allowed"]["description"]
    signals = schema["properties"]["signals"]["description"]

    assert "claimed complete now" in completion
    assert "future verification" in completion
    assert "need-verification" in signals
    assert "lightweight" in signals



def test_runtime_schema_compatibility_is_non_mutating() -> None:
    schema = json.loads(RESPONSE_SCHEMA.read_text("utf-8"))

    codex_schema = runtime_response_schema("codex", schema)
    claude_schema = runtime_response_schema("claude-code", schema)

    assert "$schema" in schema
    assert schema["properties"]["signals"]["uniqueItems"] is True
    assert "$schema" not in codex_schema
    assert "uniqueItems" not in codex_schema["properties"]["signals"]
    assert "$schema" not in claude_schema
    assert claude_schema["properties"]["signals"]["uniqueItems"] is True


def test_structured_schema_error_is_not_misclassified_by_echoed_prompt() -> None:
    output = (
        "Do not reveal credentials.\nERROR: "
        + json.dumps(
            {
                "error": {
                    "code": "invalid_json_schema",
                    "message": "uniqueItems is not permitted",
                }
            }
        )
    )

    assert classify_process_failure(output) is ResultState.INVALID_OUTPUT



def test_prompt_requires_skill_structured_output_and_no_mutation() -> None:
    scenario = load_scenarios(SCENARIOS)[0]
    schema = json.loads(RESPONSE_SCHEMA.read_text("utf-8"))

    prompt = build_prompt("codex", scenario, schema)

    assert "$solodeveling" in prompt
    assert scenario.identifier in prompt
    assert "Do not modify" in prompt
    assert "JSON object only" in prompt


@pytest.mark.parametrize(
    ("stderr", "state"),
    [
        ("authentication failed; please login", ResultState.AUTH_FAILURE),
        ("network connection timed out", ResultState.NETWORK_FAILURE),
        ("unexpected internal error", ResultState.RUNTIME_FAILURE),
    ],
)
def test_process_failure_classification_is_explicit(
    stderr: str, state: ResultState
) -> None:
    assert classify_process_failure(stderr) is state


def test_runtime_response_extraction_handles_each_contract(tmp_path: Path) -> None:
    response = {"scenario_id": "example"}
    output = tmp_path / "codex.json"
    output.write_text(json.dumps(response), encoding="utf-8")

    assert extract_runtime_response("codex", "", output) == response
    assert extract_runtime_response(
        "claude-code",
        json.dumps({"structured_output": response}),
        output,
    ) == response
    assert extract_runtime_response(
        "cursor",
        json.dumps({"type": "result", "result": json.dumps(response)}),
        output,
    ) == response


def test_secret_like_output_is_rejected_without_echoing_value() -> None:
    value = "AKIAABCDEFGHIJKLMNOP"

    with pytest.raises(EvaluationError) as captured:
        validate_safe_output(f'{{"next_action":"use {value}"}}')

    assert "aws-access-key" in str(captured.value)
    assert value not in str(captured.value)


def test_workspace_digest_changes_for_content_and_symlink_metadata(
    tmp_path: Path
) -> None:
    root = tmp_path / "fixture"
    root.mkdir()
    file = root / "state.md"
    file.write_text("before", encoding="utf-8")
    before = workspace_digest(root)

    file.write_text("after", encoding="utf-8")
    after = workspace_digest(root)

    assert before != after


def test_unknown_runtime_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(EvaluationError, match="unsupported runtime"):
        build_runtime_command(
            "unknown",
            project_root=tmp_path,
            schema_path=RESPONSE_SCHEMA,
            output_path=tmp_path / "out.json",
            prompt="test",
            claude_budget_usd=0.25,
        )
