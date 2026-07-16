from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from solodeveling_protocol.comparative_benchmark import (
    _result_document,
    build_plan,
    load_spec,
    plan_document,
    summarize_results,
    verify_fixtures,
)


SPEC = Path('benchmarks/comparative/feedback-0.1.1-vs-0.1.2.yaml')


def test_feedback_plan_is_five_tasks_two_versions_three_repetitions() -> None:
    spec = load_spec(SPEC)
    planned = build_plan(spec)
    assert len(planned) == 30
    assert {run.methodology for run in planned} == {
        'solodeveling-0.1.1',
        'solodeveling-0.1.2',
    }
    assert len({run.task_id for run in planned}) == 5
    document = plan_document(spec)
    assert document['maximum_live_runs'] == 30
    assert document['confirmation_required'] == 'RUN CONTROLLED FEEDBACK PILOT 3 30'
    assert document['runtime']['permission_profile'] == ':workspace'
    assert 'sandbox' not in document['runtime']
    assert document['account_boundary'].startswith('30 Codex calls')


def test_feedback_fixture_baselines_pass_visible_and_fail_hidden_checks() -> None:
    reports = verify_fixtures(SPEC)
    assert len(reports) == 5
    assert all(report['visible_baseline_passed'] for report in reports)
    assert all(report['hidden_baseline_rejected'] for report in reports)


def test_scoring_reports_overhead_only_for_correct_pairs() -> None:
    runs = [
        {'task_id': 'quick', 'repetition': 1, 'methodology': 'old', 'correct': True, 'elapsed_seconds': 12, 'input_tokens': 120, 'output_tokens': 20, 'tool_calls': 5, 'agent_questions': 1, 'changed_files': 3, 'workflow_artifacts': 2},
        {'task_id': 'quick', 'repetition': 1, 'methodology': 'new', 'correct': True, 'elapsed_seconds': 8, 'input_tokens': 90, 'output_tokens': 15, 'tool_calls': 3, 'agent_questions': 0, 'changed_files': 2, 'workflow_artifacts': 0},
        {'task_id': 'broken', 'repetition': 1, 'methodology': 'old', 'correct': False, 'elapsed_seconds': 1, 'workflow_artifacts': 0},
        {'task_id': 'broken', 'repetition': 1, 'methodology': 'new', 'correct': True, 'elapsed_seconds': 1, 'workflow_artifacts': 0},
    ]
    summary = summarize_results(runs)
    assert summary['correct_pairs'] == 1
    assert summary['paired_median_metrics']['elapsed_seconds'] == {
        'new': 8.0,
        'old': 12.0,
    }
    assert summary['paired_median_metrics']['workflow_artifacts'] == {
        'new': 0.0,
        'old': 2.0,
    }
    assert summary['paired_median_metrics']['input_tokens'] == {
        'new': 90.0,
        'old': 120.0,
    }


def test_feedback_result_shape_accepts_generic_ids_and_thirty_runs() -> None:
    spec = load_spec(SPEC)
    document = _result_document(spec, '0' * 64, [])
    schema = json.loads(
        Path('benchmarks/comparative/result.schema.json').read_text(encoding='utf-8')
    )
    Draft202012Validator(schema).validate(document)
    assert document['provenance']['expected_runs'] == 30


def test_paired_metric_excludes_both_sides_when_one_value_is_missing() -> None:
    runs = [
        {'task_id': 'a', 'repetition': 1, 'methodology': 'old', 'correct': True, 'elapsed_seconds': 2, 'input_tokens': 10},
        {'task_id': 'a', 'repetition': 1, 'methodology': 'new', 'correct': True, 'elapsed_seconds': 1, 'input_tokens': None},
    ]
    summary = summarize_results(runs)
    assert summary['paired_metric_pairs']['elapsed_seconds'] == 1
    assert summary['paired_metric_pairs']['input_tokens'] == 0
    assert summary['paired_median_metrics']['input_tokens'] == {
        'new': None,
        'old': None,
    }
