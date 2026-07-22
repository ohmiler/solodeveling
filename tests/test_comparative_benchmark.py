from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from solodeveling_protocol.comparative_benchmark import (
    _build_task_prompt,
    _load_checkpoint,
    _result_document,
    _changed_paths,
    _build_live_command,
    _initialize_repository,
    _install_methodology,
    _is_zero_mutation_failure,
    _prepare_methodology,
    _runtime_executable,
    _safe_environment,
    _write_failure_diagnostic,
    _verify_installed_methodology,
    BenchmarkError,
    build_plan,
    classify_runtime_failure,
    load_spec,
    parse_codex_jsonl,
    plan_document,
    require_live_ready,
    summarize_results,
    verify_fixtures,
    verify_model_catalog,
    verify_permission_runtime,
    verify_sandbox_runtime,
    run_live,
)


SPEC = Path("benchmarks/comparative/pilot.yaml")
NO_SKILL_SPEC = Path("benchmarks/comparative/solodeveling-0.2.0-vs-no-skill.yaml")


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
    assert document["runtime"]["model"] == "gpt-5.6-sol"
    assert document["runtime"]["reasoning_effort"] == "medium"
    assert document["maximum_live_runs"] == 18
    assert document["maximum_agent_seconds"] == 21600
    assert document["confirmation_required"] == "RUN CONTROLLED PILOT 4 18"
    assert "run-live" in document["live_command_template"]


def test_fixture_baselines_pass_visible_and_fail_hidden_checks() -> None:
    reports = verify_fixtures(SPEC)
    assert len(reports) == 3
    assert all(report["visible_baseline_passed"] for report in reports)
    assert all(report["hidden_baseline_rejected"] for report in reports)


def test_no_skill_preregistration_is_balanced_and_fixture_gated() -> None:
    spec = load_spec(NO_SKILL_SPEC)
    planned = build_plan(spec)

    assert len(spec["tasks"]) == 5
    assert len(planned) == 30
    assert [method.get("kind", "skill") for method in spec["methodologies"]] == [
        "skill",
        "none",
    ]
    assert spec["methodologies"][0]["version"] == "0.2.0"
    assert spec["methodologies"][0]["commit"] == "ca7c3b356c2e9444963a52e00e2e97198ad94e7d"
    assert spec["runtime"]["cli_version"] == "codex-cli 0.144.6"
    assert {task["class"] for task in spec["tasks"]} == {
        "direct-read-only",
        "quick",
        "standard",
        "follow-up",
        "critical-readiness",
    }

    reports = verify_fixtures(NO_SKILL_SPEC)
    assert len(reports) == 5
    assert all(report["visible_baseline_passed"] for report in reports)
    assert all(report["hidden_baseline_rejected"] for report in reports)


@pytest.mark.parametrize(
    ("fixture_name", "checker_name", "response"),
    [
        (
            "read-only-review",
            "check_read_only_review.py",
            "Version 2.4.0 is alpha and requires Python 3.11 or newer.",
        ),
        (
            "critical-readiness",
            "check_critical_readiness.py",
            "No-go: this destructive drop risks data loss. Require explicit approval, "
            "a backup, staging validation, and a tested rollback before proceeding.",
        ),
    ],
)
def test_response_aware_hidden_checks_accept_complete_read_only_answers(
    tmp_path: Path,
    fixture_name: str,
    checker_name: str,
    response: str,
) -> None:
    root = tmp_path / "project"
    shutil.copytree(
        Path("benchmarks/comparative/fixtures") / fixture_name,
        root,
    )
    _initialize_repository(root)
    last_message = tmp_path / "last-message.txt"
    last_message.write_text(response, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str((Path("benchmarks/comparative/checks") / checker_name).resolve()),
            str(root),
            "HEAD",
            str(last_message),
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_jsonl_parser_extracts_usage_activity_and_questions() -> None:
    lines = [
        json.dumps({"type": "item.completed", "item": {"type": "command_execution"}}),
        json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "Need input?"}}),
        "not-json",
        json.dumps({"type": "turn.completed", "usage": {"input_tokens": 12, "cached_input_tokens": 3, "output_tokens": 4}}),
    ]
    assert parse_codex_jsonl(lines) == {"input_tokens": 12, "cached_input_tokens": 3, "output_tokens": 4, "tool_calls": 1, "agent_questions": 1}


def test_model_catalog_requires_exact_slug_and_reasoning(tmp_path: Path) -> None:
    catalog = tmp_path / "models_cache.json"
    catalog.write_text(
        json.dumps(
            {
                "client_version": "0.144.5",
                "fetched_at": "2026-07-16T00:00:00Z",
                "models": [
                    {
                        "slug": "gpt-5.6-sol",
                        "supported_reasoning_levels": [
                            {"effort": "low"},
                            {"effort": "medium"},
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    spec = load_spec(SPEC)
    verified = verify_model_catalog(spec, catalog)
    assert verified["model"] == "gpt-5.6-sol"
    invalid = deepcopy(spec)
    invalid["runtime"]["model"] = "gpt-5.6"
    with pytest.raises(BenchmarkError, match="absent"):
        verify_model_catalog(invalid, catalog)


def test_runtime_failure_is_reduced_to_fixed_diagnostic_code() -> None:
    assert classify_runtime_failure("", "requested model is not available") == "model-unavailable"
    assert classify_runtime_failure("", "401 unauthorized") == "auth-failure"
    assert classify_runtime_failure("opaque provider failure", "") == "process-exit-nonzero"


def test_runtime_executable_is_canonicalized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    executable = tmp_path / "release" / "bin" / "codex.exe"
    executable.parent.mkdir(parents=True)
    executable.write_bytes(b"codex")
    alias = executable.parent / ".." / "bin" / "codex.exe"
    monkeypatch.setattr(shutil, "which", lambda name: str(alias))

    assert Path(_runtime_executable("codex")) == executable.resolve()


def test_windows_sandbox_helper_is_required_before_live_calls(tmp_path: Path) -> None:
    executable = tmp_path / "codex.exe"
    executable.write_bytes(b"codex")
    with pytest.raises(BenchmarkError, match="sandbox helper is unavailable"):
        verify_sandbox_runtime(
            str(executable),
            platform="win32",
            helper_finder=lambda name: None,
        )
    helper = tmp_path / "codex-windows-sandbox-setup.exe"
    helper.write_bytes(b"helper")
    report = verify_sandbox_runtime(
        str(executable),
        platform="win32",
        helper_finder=lambda name: None,
    )
    assert report["status"] == "available"
    assert Path(report["helper"]) == helper.resolve()


def test_windows_sandbox_helper_is_discovered_in_standalone_resources(
    tmp_path: Path,
) -> None:
    release = tmp_path / "release"
    executable = release / "bin" / "codex.exe"
    executable.parent.mkdir(parents=True)
    executable.write_bytes(b"codex")
    helper = release / "codex-resources" / "codex-windows-sandbox-setup.exe"
    helper.parent.mkdir()
    helper.write_bytes(b"helper")

    report = verify_sandbox_runtime(
        str(executable),
        platform="win32",
        helper_finder=lambda name: None,
    )

    assert report["status"] == "available"
    assert Path(report["helper"]) == helper.resolve()


def test_safe_environment_exposes_packaged_sandbox_helper_to_codex(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    release = tmp_path / "release"
    executable = release / "bin" / "codex.exe"
    executable.parent.mkdir(parents=True)
    executable.write_bytes(b"codex")
    helper = release / "codex-resources" / "codex-windows-sandbox-setup.exe"
    helper.parent.mkdir()
    helper.write_bytes(b"helper")
    monkeypatch.setenv("PATH", str(tmp_path / "existing-path"))

    environment = _safe_environment(
        str(executable),
        platform="win32",
        helper_finder=lambda name: None,
    )

    assert environment["PATH"].split(os.pathsep)[0] == str(helper.parent.resolve())


def test_python_cache_does_not_count_as_agent_change(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    readme = project / "README.md"
    readme.write_text("before\n", encoding="utf-8")
    _initialize_repository(project)
    baseline = "HEAD"
    readme.write_text("after\n", encoding="utf-8")
    cache = project / "__pycache__"
    cache.mkdir()
    (cache / "fixture.pyc").write_bytes(b"cache")
    assert _changed_paths(project, baseline) == ["README.md"]


def test_methodology_is_installed_at_codex_adapter_path(tmp_path: Path) -> None:
    source = tmp_path / "source"
    root_skill = source / "skills" / "example" / "SKILL.md"
    root_skill.parent.mkdir(parents=True)
    root_skill.write_text("# Example\n", encoding="utf-8")
    project = tmp_path / "project"
    project.mkdir()

    _install_methodology(source, project)
    _verify_installed_methodology(project, "example")

    assert (project / ".agents" / "skills" / "example" / "SKILL.md").is_file()
    assert not (project / ".codex" / "skills").exists()


def test_no_skill_methodology_installs_nothing(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()

    _prepare_methodology(
        {"id": "no-skill", "kind": "none", "version": "none"},
        {},
        project,
    )

    assert not (project / ".agents").exists()


def test_task_prompt_omits_invocation_for_no_skill() -> None:
    task = {"prompt": "Inspect the repository and report its status."}
    candidate = _build_task_prompt(
        {"id": "solodeveling", "kind": "skill", "invocation": "$solodeveling"},
        task,
    )
    baseline = _build_task_prompt(
        {"id": "no-skill", "kind": "none"},
        task,
    )

    assert candidate.startswith("$solodeveling\n\n")
    assert "$solodeveling" not in baseline
    assert candidate.split("\n\n", 1)[1] == baseline
    assert baseline.endswith(task["prompt"])


def test_no_skill_plan_requires_only_installed_methodology_sources() -> None:
    spec = deepcopy(load_spec(SPEC))
    spec["methodologies"][1] = {
        "id": "no-skill",
        "kind": "none",
        "version": "none",
    }

    document = plan_document(spec)

    assert '--source "solodeveling=<PINNED_SOLODEVELING_CHECKOUT>"' in document["live_command_template"]
    assert "no-skill-source" not in document["live_command_template"]


def test_zero_mutation_failure_requires_successful_but_incorrect_process() -> None:
    assert _is_zero_mutation_failure(0, False, [])
    assert not _is_zero_mutation_failure(1, False, [])
    assert not _is_zero_mutation_failure(0, True, [])
    assert not _is_zero_mutation_failure(0, False, ["README.md"])
    assert not _is_zero_mutation_failure(0, False, [], mutation_required=False)


def test_failure_diagnostic_is_local_raw_sidecar(tmp_path: Path) -> None:
    output = tmp_path / "pilot.json"
    path = _write_failure_diagnostic(
        output,
        run_id="run-01",
        process_stdout='{"type":"turn.completed"}\n',
        process_stderr="stderr",
        last_agent_message="Could not edit the fixture.",
        visible_stdout="visible",
        visible_stderr="",
        hidden_stdout="",
        hidden_stderr="hidden",
        changed_paths=[],
    )
    assert path == tmp_path / "pilot.run-01.diagnostic.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["notice"] == "local-only unsanitized diagnostic; do not publish"
    assert document["last_agent_message"] == "Could not edit the fixture."
    assert document["changed_paths"] == []


def test_live_command_uses_workspace_permission_profile_not_legacy_sandbox(tmp_path: Path) -> None:
    spec = load_spec(Path("benchmarks/comparative/feedback-0.1.1-vs-0.1.2.yaml"))
    command = _build_live_command(
        "codex",
        spec,
        tmp_path / "worktree",
        tmp_path / "last-message.txt",
    )
    assert "--sandbox" not in command
    assert 'default_permissions=":workspace"' in command
    assert "sandbox_workspace_write.network_access=false" not in command


def test_no_skill_live_command_pins_the_verified_windows_sandbox(tmp_path: Path) -> None:
    spec = load_spec(NO_SKILL_SPEC)
    command = _build_live_command(
        "codex",
        spec,
        tmp_path / "worktree",
        tmp_path / "last-message.txt",
    )

    assert 'windows.sandbox="elevated"' in command


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


def test_archived_invalid_pilot_is_not_live_eligible() -> None:
    for path in (
        Path("benchmarks/comparative/archive/pilot-1-invalid.yaml"),
        Path("benchmarks/comparative/archive/pilot-2-invalid.yaml"),
        Path("benchmarks/comparative/archive/pilot-3-invalid.yaml"),
        Path("benchmarks/comparative/archive/feedback-0.1.1-vs-0.1.2-pilot-1-invalid.yaml"),
        Path("benchmarks/comparative/archive/feedback-0.1.1-vs-0.1.2-pilot-2-invalid.yaml"),
    ):
        archived = load_spec(path)
        with pytest.raises(BenchmarkError, match="not eligible"):
            require_live_ready(archived)


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
            "failure_code": None,
            "process_returncode": 0,
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


def test_checkpoint_with_pre_inference_failure_cannot_resume(tmp_path: Path) -> None:
    spec = load_spec(SPEC)
    planned = build_plan(spec)
    expected = _result_document(spec, "0" * 64, [])
    failed = {
        "run_id": planned[0].run_id,
        "task_id": planned[0].task_id,
        "methodology": planned[0].methodology,
        "repetition": planned[0].repetition,
        "state": "runtime-failure",
        "input_tokens": None,
        "output_tokens": None,
        "tool_calls": 0,
    }
    checkpoint = tmp_path / "pilot.json"
    checkpoint.write_text(
        json.dumps({**expected, "runs": [failed]}),
        encoding="utf-8",
    )
    with pytest.raises(BenchmarkError, match="successor preregistration"):
        _load_checkpoint(checkpoint, expected, planned)


def test_checkpoint_with_zero_mutation_failure_cannot_resume(tmp_path: Path) -> None:
    spec = load_spec(SPEC)
    planned = build_plan(spec)
    expected = _result_document(spec, "0" * 64, [])
    failed = {
        "run_id": planned[0].run_id,
        "task_id": planned[0].task_id,
        "methodology": planned[0].methodology,
        "repetition": planned[0].repetition,
        "state": "execution-failure",
        "failure_code": "zero-mutation",
    }
    checkpoint = tmp_path / "pilot.json"
    checkpoint.write_text(json.dumps({**expected, "runs": [failed]}), encoding="utf-8")
    with pytest.raises(BenchmarkError, match="zero-mutation"):
        _load_checkpoint(checkpoint, expected, planned)
