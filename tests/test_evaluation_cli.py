from __future__ import annotations

import json
from pathlib import Path

from solodeveling_protocol.evaluation import load_scenarios
from solodeveling_protocol.evaluation_cli import main


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
        "acceptance_summary": ["Respect the bounded acceptance criteria."],
        "limitations": ["This is replay evidence, not a live run."],
        "next_action": "Continue with the selected workflow.",
    }


def test_dry_run_plans_smoke_matrix_without_live_claim(
    tmp_path: Path, capsys
) -> None:
    output = tmp_path / "must-not-exist.json"

    exit_code = main(
        [
            "run",
            "--runtime",
            "codex",
            "--runtime",
            "claude-code",
            "--smoke",
            "--dry-run",
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    document = json.loads(capsys.readouterr().out)
    assert document["live"] is False
    assert document["dry_run"] is True
    assert len(document["plan"]) == 6
    assert not output.exists()


def test_dry_run_can_select_one_scenario(capsys) -> None:
    result = main(
        [
            "run",
            "--runtime",
            "codex",
            "--smoke",
            "--scenario",
            "quick-local-documentation",
            "--dry-run",
        ]
    )

    document = json.loads(capsys.readouterr().out)
    assert result == 0
    assert [item["scenario_id"] for item in document["plan"]] == [
        "quick-local-documentation"
    ]


def test_unknown_scenario_selection_is_rejected(capsys) -> None:
    result = main(
        [
            "run",
            "--runtime",
            "codex",
            "--scenario",
            "not-present",
            "--dry-run",
        ]
    )

    assert result == 1
    assert "unknown scenario selection" in capsys.readouterr().out



def test_replay_scores_structured_records_without_live_label(
    tmp_path: Path,
) -> None:
    scenario = load_scenarios(SCENARIOS)[0]
    record = tmp_path / "record.json"
    output = tmp_path / "result.json"
    record.write_text(
        json.dumps(
            {
                "runtime": "cursor",
                "responses": {
                    scenario.identifier: passing_response(scenario)
                },
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "replay",
            "--input",
            str(record),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    document = json.loads(output.read_text("utf-8"))
    assert document["live"] is False
    assert document["results"][0]["state"] == "replay-pass"


def test_replay_rejects_unknown_scenario(
    tmp_path: Path, capsys
) -> None:
    record = tmp_path / "record.json"
    output = tmp_path / "result.json"
    record.write_text(
        json.dumps(
            {
                "runtime": "codex",
                "responses": {"unknown": {"scenario_id": "unknown"}},
            }
        ),
        encoding="utf-8",
    )

    assert main(
        [
            "replay",
            "--input",
            str(record),
            "--output",
            str(output),
        ]
    ) == 1
    assert "unknown replay scenario" in capsys.readouterr().out
    assert not output.exists()


def test_evaluation_cli_is_packaged() -> None:
    text = Path("pyproject.toml").read_text("utf-8")

    assert (
        'solodeveling-eval = "solodeveling_protocol.evaluation_cli:main"'
        in text
    )
