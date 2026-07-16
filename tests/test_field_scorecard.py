from __future__ import annotations

import json
from pathlib import Path

import pytest

from solodeveling_protocol.field_scorecard import (
    ScorecardError,
    load_scorecard,
    summarize_scorecard,
)


def test_empty_template_is_valid_and_incomplete() -> None:
    document = load_scorecard(Path('benchmarks/field/scorecard.template.json'))
    summary = summarize_scorecard(document)
    assert summary['observations'] == 0
    assert summary['target_observations'] == 20
    assert summary['collection_complete'] is False
    assert summary['public_comparative_claim_allowed'] is False


def test_summary_reports_quality_overhead_resume_and_annoyance(tmp_path: Path) -> None:
    document = {
        'schema': 1,
        'study_id': 'field-test',
        'target_observations': 2,
        'observations': [
            {
                'id': 'task-001',
                'version': '0.1.2',
                'tier': 'quick',
                'task_class': 'documentation',
                'correctness_passed': True,
                'verification_passed': True,
                'elapsed_seconds': 10,
                'agent_questions': 0,
                'workflow_artifacts': 0,
                'rework_count': 0,
                'resume_required': False,
                'user_annoyance': 1,
                'ceremony_fit': 'right',
            },
            {
                'id': 'task-002',
                'version': '0.1.2',
                'tier': 'standard',
                'task_class': 'repair',
                'correctness_passed': True,
                'verification_passed': True,
                'elapsed_seconds': 30,
                'agent_questions': 1,
                'workflow_artifacts': 2,
                'rework_count': 1,
                'resume_required': True,
                'resume_correct': True,
                'user_annoyance': 2,
                'ceremony_fit': 'too-heavy',
            },
        ],
    }
    path = tmp_path / 'scorecard.json'
    path.write_text(json.dumps(document), encoding='utf-8')
    summary = summarize_scorecard(load_scorecard(path))
    assert summary['collection_complete'] is True
    assert summary['correctness_rate'] == 1.0
    assert summary['median_elapsed_seconds'] == 20.0
    assert summary['resume_accuracy'] == 1.0
    assert summary['median_user_annoyance'] == 1.5
    assert summary['too_heavy_rate'] == 0.5
    assert summary['by_tier']['quick']['median_workflow_artifacts'] == 0


def test_scorecard_rejects_project_identifiers(tmp_path: Path) -> None:
    template = json.loads(
        Path('benchmarks/field/scorecard.template.json').read_text(encoding='utf-8')
    )
    template['observations'] = [{'id': 'task-001', 'project_name': 'secret'}]
    path = tmp_path / 'invalid.json'
    path.write_text(json.dumps(template), encoding='utf-8')
    with pytest.raises(ScorecardError):
        load_scorecard(path)
