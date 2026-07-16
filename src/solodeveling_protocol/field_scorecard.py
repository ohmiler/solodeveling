from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class ScorecardError(RuntimeError):
    pass


def _schema_path() -> Path:
    source = Path(__file__).resolve().parents[2] / 'benchmarks' / 'field' / 'scorecard.schema.json'
    if source.is_file():
        return source
    return (
        Path(__file__).resolve().parent
        / 'resources'
        / 'benchmarks'
        / 'field'
        / 'scorecard.schema.json'
    )


def load_scorecard(path: Path, *, schema_path: Path | None = None) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding='utf-8'))
        schema = json.loads((schema_path or _schema_path()).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise ScorecardError(f'scorecard or schema is unreadable: {error}') from error
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        details = '; '.join(error.message for error in errors[:3])
        raise ScorecardError(f'scorecard validation failed: {details}')
    identifiers = [item['id'] for item in document['observations']]
    if len(identifiers) != len(set(identifiers)):
        raise ScorecardError('scorecard observation IDs must be unique')
    return document


def _median(observations: list[dict[str, Any]], key: str) -> float | None:
    values = [
        float(item[key])
        for item in observations
        if isinstance(item.get(key), (int, float))
        and not isinstance(item.get(key), bool)
    ]
    return round(statistics.median(values), 4) if values else None


def _rate(values: list[bool]) -> float | None:
    return round(sum(values) / len(values), 4) if values else None


def _tier_summary(observations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        'observations': len(observations),
        'correctness_rate': _rate(
            [item['correctness_passed'] for item in observations]
        ),
        'verification_rate': _rate(
            [item['verification_passed'] for item in observations]
        ),
        'median_elapsed_seconds': _median(observations, 'elapsed_seconds'),
        'median_agent_questions': _median(observations, 'agent_questions'),
        'median_workflow_artifacts': _median(observations, 'workflow_artifacts'),
        'median_rework_count': _median(observations, 'rework_count'),
        'median_user_annoyance': _median(observations, 'user_annoyance'),
        'too_heavy_rate': _rate(
            [
                item['ceremony_fit'] == 'too-heavy'
                for item in observations
                if 'ceremony_fit' in item
            ]
        ),
    }


def summarize_scorecard(document: dict[str, Any]) -> dict[str, Any]:
    observations = document['observations']
    resumed = [item for item in observations if item['resume_required']]
    resume_results = [
        item['resume_correct']
        for item in resumed
        if isinstance(item.get('resume_correct'), bool)
    ]
    tiers = sorted({item['tier'] for item in observations})
    return {
        'schema': 1,
        'study_id': document['study_id'],
        'observations': len(observations),
        'target_observations': document['target_observations'],
        'collection_complete': len(observations) >= document['target_observations'],
        'correctness_rate': _rate(
            [item['correctness_passed'] for item in observations]
        ),
        'verification_rate': _rate(
            [item['verification_passed'] for item in observations]
        ),
        'median_elapsed_seconds': _median(observations, 'elapsed_seconds'),
        'median_time_to_first_edit_seconds': _median(
            observations, 'time_to_first_edit_seconds'
        ),
        'median_agent_questions': _median(observations, 'agent_questions'),
        'median_workflow_artifacts': _median(observations, 'workflow_artifacts'),
        'median_rework_count': _median(observations, 'rework_count'),
        'resume_accuracy': _rate(resume_results),
        'median_user_annoyance': _median(observations, 'user_annoyance'),
        'too_heavy_rate': _rate(
            [
                item['ceremony_fit'] == 'too-heavy'
                for item in observations
                if 'ceremony_fit' in item
            ]
        ),
        'by_tier': {
            tier: _tier_summary(
                [item for item in observations if item['tier'] == tier]
            )
            for tier in tiers
        },
        'public_comparative_claim_allowed': False,
        'interpretation': (
            'field evidence is observational; use a preregistered controlled study '
            'for comparative claims'
        ),
    }
