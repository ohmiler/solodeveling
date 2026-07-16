from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from solodeveling_protocol.comparative_benchmark import (
    _load_checkpoint,
    _result_document,
    BenchmarkError,
    build_plan,
    load_spec,
    parse_codex_jsonl,
    plan_document,
    summarize_results,
    verify_fixtures,
    run_live,
)


SPEC = Path("benchmarks/comparative/pilot.yaml")


def test_plan_is_deterministic_and_exactly_eighteen_runs() -> None:
    spec = load_spec(SPEC)
    first = build_plan(spec)
    assert first == build_plan(spec)
    assert len(first) == 18
    pair_first = [first[index].methodology for index in range(0, len(first), 2)]
    assert abs(pair_first.count("solodeveling") - pair_first.count("superpowers")) == 1
    assert {(run.task_id, run.methodology, run.repetition) for run in first} == {
        (task["id"], method["id"], repetition)
        for task in spec["tasks"]
        for method in spec["methodologies"]
        for repetition in range(1, 4)
    }


def test_plan_is_non_live_and_discloses_runtime_boundary() -> None:
    document = plan_document(load_spec(SPEC))
    assert document["live"] is False
    assert document["runtime"]["model"] == "gpt-5.6"
    assert document["runtime"]["reasoning_effort"] == "medium"
    assert document["maximum_live_runs"] == 18
    assert document["maximum_agent_seconds"] == 21600
    assert document["confirmation_required"] == "RUN CONTROLLED PILOT 18"
    assert "run-live" in document["live_command_template"]


def test_fixture_baselines_pass_visible_and_fail_hidden_checks() -> None:
    reports = verify_fixtures(SPEC)
    assert len(reports) == 3
    assert all(report["visible_baseline_passed"] for report in reports)
    assert all(report["hidden_baseline_rejected"] for report in reports)


def test_jsonl_parser_extracts_usage_activity_and_questions() -> None:
    lines = [
        json.dumps({"type": "item.completed", "item": {"type": "command_execution"}}),
        json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "Need input?"}}),
        "not-json",
        json.dumps({"type": "turn.completed", "usage": {"input_tokens": 12, "cached_input_tokens": 3, "output_tokens": 4}}),
    ]
    assert parse_codex_jsonl(lines) == {"input_tokens": 12, "cached_input_tokens": 3, "output_tokens": 4, "tool_calls": 1, "agent_questions": 1}


def test_scoring_gates_speed_on_correct_pairs_and_forbids_claim() -> None:
    runs = [
        {"task_id": "a", "repetition": 1, "methodology": "solodeveling", "correct": True, "elapsed_seconds": 4},
        {"task_id": "a", "repetition": 1, "methodology": "superpowers", "correct": True, "elapsed_seconds": 8},
        {"task_id": "b", "repetition": 1, "methodology": "solodeveling", "correct": True, "elapsed_seconds": 2},
        {"task_id": "b", "repetition": 1, "methodology": "superpowers", "correct": False, "elapsed_seconds": 1},
    ]
    summary = summarize_results(runs)
    assert summary["correct_pairs"] == 1
    assert summary["paired_median_seconds"] == {"solodeveling": 4.0, "superpowers": 8.0}
    assert summary["public_faster_claim_allowed"] is False


def test_invalid_claim_policy_fails_closed(tmp_path: Path) -> None:
    document = SPEC.read_text(encoding="utf-8").replace("public_faster_claim_allowed: false", "public_faster_claim_allowed: true")
    path = tmp_path / "pilot.yaml"
    path.write_text(document, encoding="utf-8")
    with pytest.raises(BenchmarkError, match="public faster claim"):
        load_spec(path)


def test_live_runner_requires_exact_confirmation_before_any_runtime_call(tmp_path: Path) -> None:
    with pytest.raises(BenchmarkError, match="exact confirmation"):
        run_live(
            SPEC,
            confirmation="yes",
            solodeveling_source=tmp_path / "solodeveling",
            superpowers_source=tmp_path / "superpowers",
            output=tmp_path / "result.json",
        )


def test_sanitized_result_shape_matches_committed_schema() -> None:
    runs = [
        {
            "run_id": "run-01",
            "task_id": "quick-docs",
            "methodology": "solodeveling",
            "repetition": 1,
            "state": "completed",
            "correct": True,
            "elapsed_seconds": 1.0,
            "input_tokens": 1,
            "cached_input_tokens": 0,
            "output_tokens": 1,
            "tool_calls": 1,
            "agent_questions": 0,
            "changed_files": 1,
            "workflow_artifacts": 0,
            "human_interventions": 0,
        }
    ]
    document = {
        "schema": 1,
        "benchmark_id": "test",
        "classification": "pilot-signal-only",
        "spec_sha256": "0" * 64,
        "provenance": {
            "runtime": {},
            "methodology_pins": {},
            "expected_runs": 18,
        },
        "runs": runs,
        "summary": summarize_results(runs),
    }
    schema = json.loads(Path("benchmarks/comparative/result.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(document)


def test_checkpoint_resume_rejects_mismatched_preregistration(tmp_path: Path) -> None:
    spec = load_spec(SPEC)
    planned = build_plan(spec)
    expected = _result_document(spec, "0" * 64, [])
    checkpoint = tmp_path / "pilot.json"
    checkpoint.write_text(json.dumps({**expected, "spec_sha256": "1" * 64}), encoding="utf-8")
    with pytest.raises(BenchmarkError, match="spec_sha256"):
        _load_checkpoint(checkpoint, expected, planned)
