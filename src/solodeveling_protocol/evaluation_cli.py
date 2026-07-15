from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from contextlib import ExitStack
from pathlib import Path
from typing import Sequence

from solodeveling_protocol.evaluation import (
    EvaluationError,
    ResultState,
    SUPPORTED_RUNTIMES,
    build_prompt,
    build_runtime_command,
    load_scenarios,
)
from solodeveling_protocol.evaluation_runner import (
    replay_response,
    run_live_scenario,
    sanitized_result_document,
)
from solodeveling_protocol.resources import resource_path


DEFAULT_SCENARIOS = Path("evals/scenarios/core.yaml")
DEFAULT_SCHEMA = Path("evals/evaluation-response.schema.json")
DEFAULT_OUTPUT = Path("evals/results/latest.json")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run deterministic Solodeveling cross-agent evaluations."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    run = subparsers.add_parser("run", help="Run fresh isolated live scenarios.")
    run.add_argument(
        "--runtime",
        action="append",
        choices=SUPPORTED_RUNTIMES,
        required=True,
    )
    run.add_argument("--source", type=Path)
    run.add_argument("--scenarios", type=Path)
    run.add_argument("--schema", type=Path)
    run.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    run.add_argument("--temp-parent", type=Path, default=None)
    run.add_argument("--claude-budget-usd", type=float, default=0.25)
    run.add_argument("--smoke", action="store_true")
    run.add_argument(
        "--scenario",
        action="append",
        dest="scenario_ids",
        help="Run only the named scenario; repeat to select more than one.",
    )
    run.add_argument("--dry-run", action="store_true")

    replay = subparsers.add_parser(
        "replay", help="Score saved structured responses without an agent call."
    )
    replay.add_argument("--input", type=Path, required=True)
    replay.add_argument("--scenarios", type=Path)
    replay.add_argument("--schema", type=Path)
    replay.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)

    probe = subparsers.add_parser(
        "probe", help="Report executable availability without an agent call."
    )
    probe.add_argument(
        "--runtime",
        action="append",
        choices=SUPPORTED_RUNTIMES,
    )
    return parser


def _write_document(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _selected_scenarios(
    path: Path,
    smoke: bool,
    scenario_ids: Sequence[str] | None = None,
):
    scenarios = load_scenarios(path)
    selected = tuple(
        scenario for scenario in scenarios if not smoke or scenario.smoke
    )
    if not scenario_ids:
        return selected
    requested = set(scenario_ids)
    known = {scenario.identifier for scenario in scenarios}
    unknown = sorted(requested - known)
    if unknown:
        raise EvaluationError(
            "unknown scenario selection: " + ", ".join(unknown)
        )
    filtered = tuple(
        scenario for scenario in selected if scenario.identifier in requested
    )
    if not filtered:
        raise EvaluationError(
            "selected scenarios are excluded by the active smoke filter"
        )
    return filtered


def _dry_run(arguments, scenarios) -> int:
    schema = json.loads(arguments.schema.read_text(encoding="utf-8"))
    plan = []
    for runtime in arguments.runtime:
        for scenario in scenarios:
            prompt = build_prompt(runtime, scenario, schema)
            command = build_runtime_command(
                runtime,
                project_root=Path("<isolated-project>"),
                schema_path=arguments.schema,
                output_path=Path("<local-result>"),
                prompt=prompt,
                claude_budget_usd=arguments.claude_budget_usd,
            )
            plan.append(
                {
                    "runtime": runtime,
                    "scenario_id": scenario.identifier,
                    "executable": command.argv[0],
                    "timeout_seconds": command.timeout_seconds,
                    "prompt_transport": "stdin",
                    "mutation_mode": (
                        "read-only"
                        if runtime == "codex"
                        else "plan-read-only"
                        if runtime == "claude-code"
                        else "no-force"
                    ),
                }
            )
    print(json.dumps({"live": False, "dry_run": True, "plan": plan}, indent=2))
    return 0


def _run_live(arguments) -> int:
    scenarios = _selected_scenarios(
        arguments.scenarios,
        arguments.smoke,
        arguments.scenario_ids,
    )
    if arguments.dry_run:
        return _dry_run(arguments, scenarios)
    parent = arguments.temp_parent or Path(tempfile.gettempdir())
    results = []
    for runtime in arguments.runtime:
        for scenario in scenarios:
            result = run_live_scenario(
                runtime,
                scenario,
                source_skills=arguments.source,
                schema_path=arguments.schema,
                temp_parent=parent,
                claude_budget_usd=arguments.claude_budget_usd,
            )
            results.append(result)
            print(f"{runtime}/{scenario.identifier}: {result.state.value}")
    document = sanitized_result_document(results)
    _write_document(arguments.output, document)
    passing = all(result.state is ResultState.LIVE_PASS for result in results)
    return 0 if passing else 1


def _run_replay(arguments) -> int:
    try:
        record = json.loads(arguments.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EvaluationError(f"cannot load replay input: {error}") from error
    if not isinstance(record, dict):
        raise EvaluationError("replay input must be an object")
    runtime = record.get("runtime")
    responses = record.get("responses")
    if runtime not in SUPPORTED_RUNTIMES:
        raise EvaluationError("replay runtime is unsupported")
    if not isinstance(responses, dict) or not responses:
        raise EvaluationError("replay responses must be a non-empty object")
    scenarios = {
        scenario.identifier: scenario
        for scenario in load_scenarios(arguments.scenarios)
    }
    results = []
    for identifier, response in responses.items():
        scenario = scenarios.get(identifier)
        if scenario is None:
            raise EvaluationError(f"unknown replay scenario: {identifier}")
        if not isinstance(response, dict):
            raise EvaluationError(
                f"replay response for {identifier} must be an object"
            )
        results.append(
            replay_response(
                runtime,
                scenario,
                response,
                schema_path=arguments.schema,
            )
        )
    document = sanitized_result_document(results)
    _write_document(arguments.output, document)
    passing = all(result.state is ResultState.REPLAY_PASS for result in results)
    return 0 if passing else 1


def _run_probe(arguments) -> int:
    runtimes = arguments.runtime or list(SUPPORTED_RUNTIMES)
    document = {
        "live": False,
        "probe": [
            {
                "runtime": runtime,
                "executable": {
                    "codex": "codex",
                    "claude-code": "claude",
                    "cursor": "cursor-agent",
                }[runtime],
                "available": shutil.which(
                    {
                        "codex": "codex",
                        "claude-code": "claude",
                        "cursor": "cursor-agent",
                    }[runtime]
                )
                is not None,
            }
            for runtime in runtimes
        ],
    }
    print(json.dumps(document, indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        with ExitStack() as resources:
            if arguments.action == "run":
                arguments.source = resources.enter_context(
                    resource_path("skills", arguments.source)
                )
                arguments.scenarios = resources.enter_context(
                    resource_path("evals/scenarios", arguments.scenarios)
                ) / "core.yaml"
                arguments.schema = resources.enter_context(
                    resource_path(
                        "evals/evaluation-response.schema.json",
                        arguments.schema,
                    )
                )
                return _run_live(arguments)
            if arguments.action == "replay":
                arguments.scenarios = resources.enter_context(
                    resource_path("evals/scenarios", arguments.scenarios)
                ) / "core.yaml"
                arguments.schema = resources.enter_context(
                    resource_path(
                        "evals/evaluation-response.schema.json",
                        arguments.schema,
                    )
                )
                return _run_replay(arguments)
            return _run_probe(arguments)
    except (EvaluationError, FileNotFoundError, ValueError) as error:
        print(f"evaluation-error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
