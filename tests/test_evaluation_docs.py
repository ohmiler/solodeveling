import json
from pathlib import Path

import jsonschema

from solodeveling_protocol.evaluation import load_scenarios
from solodeveling_protocol.evaluation_runner import (
    replay_response,
    sanitized_result_document,
)


def test_cross_agent_documentation_covers_evidence_and_safety_boundaries() -> None:
    text = Path("docs/cross-agent-evaluation.md").read_text("utf-8")

    for phrase in (
        "not subagents",
        "No model judges another model",
        "shell disabled",
        "API-key environment",
        "fixture before and after",
        "without force",
        "Replay",
        "never fresh live evidence",
        "Tier 1 verified",
    ):
        assert phrase in text


def test_sanitized_result_matches_versioned_result_schema() -> None:
    scenario = load_scenarios(Path("evals/scenarios/core.yaml"))[0]
    expected = scenario.expected
    response = {
        "scenario_id": scenario.identifier,
        "level": expected.level,
        "workflow": expected.workflow,
        "action": expected.action,
        "requires_authority": expected.requires_authority,
        "requires_recovery": expected.requires_recovery,
        "completion_allowed": expected.completion_allowed,
        "signals": list(expected.signals),
        "acceptance_summary": ["Bound the work."],
        "limitations": ["Replay only."],
        "next_action": "Continue safely.",
    }
    result = replay_response(
        "codex",
        scenario,
        response,
        schema_path=Path("evals/evaluation-response.schema.json"),
    )
    document = sanitized_result_document([result])
    schema = json.loads(
        Path("evals/evaluation-result.schema.json").read_text("utf-8")
    )

    jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    ).validate(document)
