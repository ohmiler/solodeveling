from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml


class BenchmarkError(RuntimeError):
    pass


@dataclass(frozen=True)
class PlannedRun:
    run_id: str
    task_id: str
    methodology: str
    repetition: int
    order: int


def load_spec(path: Path) -> dict[str, Any]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("schema") != 1:
        raise BenchmarkError("pilot spec must be a schema-1 mapping")
    if document.get("classification") != "pilot-signal-only":
        raise BenchmarkError("pilot must remain classified as pilot-signal-only")
    if document.get("claim_policy", {}).get("public_faster_claim_allowed") is not False:
        raise BenchmarkError("pilot must not authorize a public faster claim")
    return document


def require_live_ready(spec: dict[str, Any]) -> None:
    if spec.get("status") != "preregistered-not-run":
        raise BenchmarkError(
            f"benchmark status {spec.get('status', 'missing')} is not eligible for live execution"
        )


def build_plan(spec: dict[str, Any]) -> list[PlannedRun]:
    tasks = [task["id"] for task in spec["tasks"]]
    methods = [method["id"] for method in spec["methodologies"]]
    repetitions = int(spec["repetitions"])
    if not tasks or len(methods) != 2 or repetitions < 1:
        raise BenchmarkError(
            "paired pilot design requires at least one task, exactly two methods, "
            "and at least one repetition"
        )
    if len(tasks) != len(set(tasks)) or len(methods) != len(set(methods)):
        raise BenchmarkError("task and methodology IDs must be unique")
    rng = random.Random(int(spec["seed"]))
    blocks = [(repetition, task) for repetition in range(1, repetitions + 1) for task in tasks]
    rng.shuffle(blocks)
    reverse_first = rng.randrange(2)
    planned: list[PlannedRun] = []
    for block_index, (repetition, task) in enumerate(blocks):
        ordered = list(methods)
        if (block_index + reverse_first) % 2:
            ordered.reverse()
        for methodology in ordered:
            order = len(planned) + 1
            planned.append(PlannedRun(f"run-{order:02d}", task, methodology, repetition, order))
    expected = int(spec["claim_policy"]["required_live_runs"])
    if len(planned) != expected:
        raise BenchmarkError(f"plan has {len(planned)} runs; expected {expected}")
    return planned


def plan_document(spec: dict[str, Any]) -> dict[str, Any]:
    runtime = spec["runtime"]
    result_path = f"benchmarks/results/{spec['benchmark_id']}.json"
    expected_runs = int(spec["claim_policy"]["required_live_runs"])
    source_arguments = "".join(
        f' --source "{method["id"]}=<PINNED_{method["id"].upper()}_CHECKOUT>"'
        for method in spec["methodologies"]
    )
    return {
        "schema": 1,
        "benchmark_id": spec["benchmark_id"],
        "classification": spec["classification"],
        "live": False,
        "runtime": runtime,
        "methodologies": spec["methodologies"],
        "confirmation_required": spec["claim_policy"]["confirmation"],
        "maximum_live_runs": expected_runs,
        "maximum_agent_seconds": int(runtime["timeout_seconds"]) * expected_runs,
        "account_boundary": (
            f"{expected_runs} Codex calls use the signed-in account's capacity or "
            "credits; no stable dollar maximum is available from the CLI"
        ),
        "mutation_boundary": "only fresh temporary fixture worktrees",
        "live_command_template": (
            'python scripts/comparative_benchmark.py run-live --confirm "'
            + spec["claim_policy"]["confirmation"]
            + '"'
            + source_arguments
            + f" --output {result_path}"
        ),
        "runs": [run.__dict__ for run in build_plan(spec)],
    }


def _run(command: list[str], cwd: Path, *, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, check=False, shell=False, env=environment)


def verify_fixtures(spec_path: Path) -> list[dict[str, Any]]:
    spec = load_spec(spec_path)
    root = spec_path.parent
    reports: list[dict[str, Any]] = []
    for task in spec["tasks"]:
        fixture = root / task["fixture"]
        checker = root / task["hidden_check"]
        with tempfile.TemporaryDirectory(prefix=f"benchmark-{task['id']}-") as temporary:
            project = Path(temporary) / "project"
            shutil.copytree(fixture, project)
            _initialize_repository(project)
            visible = _run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], project)
            hidden = _run([sys.executable, str(checker.resolve()), str(project), "HEAD"], project)
            report = {"task_id": task["id"], "visible_baseline_passed": visible.returncode == 0, "hidden_baseline_rejected": hidden.returncode != 0}
            if not all(report.values()):
                raise BenchmarkError(f"fixture verification failed: {report}")
            reports.append(report)
    return reports


def parse_codex_jsonl(lines: Iterable[str]) -> dict[str, int | None]:
    usage: dict[str, int | None] = {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None}
    tool_calls = 0
    questions = 0
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            for key in usage:
                value = event["usage"].get(key)
                if isinstance(value, int) and not isinstance(value, bool):
                    usage[key] = value
        if event.get("type") == "item.completed" and isinstance(event.get("item"), dict):
            item = event["item"]
            if item.get("type") in {"command_execution", "mcp_tool_call", "file_change", "web_search"}:
                tool_calls += 1
            if item.get("type") == "agent_message" and str(item.get("text", "")).rstrip().endswith("?"):
                questions += 1
    return {**usage, "tool_calls": tool_calls, "agent_questions": questions}


def classify_runtime_failure(stdout: str, stderr: str) -> str:
    lowered = (stdout + "\n" + stderr).lower()
    if "model" in lowered and any(marker in lowered for marker in ("not found", "not available", "unsupported", "does not exist", "unknown model")):
        return "model-unavailable"
    if any(marker in lowered for marker in ("not logged in", "unauthorized", "authentication failed", "invalid token")):
        return "auth-failure"
    if any(marker in lowered for marker in ("rate limit", "usage limit", "quota", "capacity")):
        return "capacity-failure"
    if any(marker in lowered for marker in ("invalid config", "configuration error", "config error")):
        return "configuration-failure"
    return "process-exit-nonzero"


def _median(values: list[float]) -> float | None:
    return round(statistics.median(values), 4) if values else None


def summarize_results(runs: list[dict[str, Any]]) -> dict[str, Any]:
    metric_names = (
        "elapsed_seconds",
        "input_tokens",
        "output_tokens",
        "tool_calls",
        "agent_questions",
        "changed_files",
        "workflow_artifacts",
    )
    methods = sorted({str(run["methodology"]) for run in runs})
    by_method: dict[str, Any] = {}
    for method in methods:
        selected = [run for run in runs if run["methodology"] == method]
        correct = [run for run in selected if run.get("correct") is True]
        correct_metrics = {
            metric: _median(
                [
                    float(run[metric])
                    for run in correct
                    if isinstance(run.get(metric), (int, float))
                    and not isinstance(run.get(metric), bool)
                ]
            )
            for metric in metric_names
        }
        by_method[method] = {
            "runs": len(selected),
            "correct": len(correct),
            "success_rate": round(len(correct) / len(selected), 4) if selected else None,
            "median_correct_seconds": _median([float(run["elapsed_seconds"]) for run in correct]),
            "median_correct_metrics": correct_metrics,
        }
    pairs: list[dict[str, Any]] = []
    paired_runs: list[dict[str, dict[str, Any]]] = []
    indexed = {(run["task_id"], run["repetition"], run["methodology"]): run for run in runs}
    if len(methods) == 2:
        keys = sorted({(run["task_id"], run["repetition"]) for run in runs})
        for task_id, repetition in keys:
            left = indexed.get((task_id, repetition, methods[0]))
            right = indexed.get((task_id, repetition, methods[1]))
            if left and right and left.get("correct") is True and right.get("correct") is True:
                pairs.append({"task_id": task_id, "repetition": repetition, f"{methods[0]}_seconds": left["elapsed_seconds"], f"{methods[1]}_seconds": right["elapsed_seconds"]})
                paired_runs.append({methods[0]: left, methods[1]: right})
    paired_medians = {method: _median([float(pair[f"{method}_seconds"]) for pair in pairs]) for method in methods}
    paired_metric_medians: dict[str, dict[str, float | None]] = {}
    paired_metric_pairs: dict[str, int] = {}
    for metric in metric_names:
        eligible_pairs = [
            pair
            for pair in paired_runs
            if all(
                isinstance(pair[method].get(metric), (int, float))
                and not isinstance(pair[method].get(metric), bool)
                for method in methods
            )
        ]
        paired_metric_pairs[metric] = len(eligible_pairs)
        paired_metric_medians[metric] = {
            method: _median(
                [float(pair[method][metric]) for pair in eligible_pairs]
            )
            for method in methods
        }
    return {
        "correctness_first": True,
        "by_methodology": by_method,
        "correct_pairs": len(pairs),
        "paired_median_seconds": paired_medians,
        "paired_median_metrics": paired_metric_medians,
        "paired_metric_pairs": paired_metric_pairs,
        "public_faster_claim_allowed": False,
        "interpretation": "pilot signal only; preregister a confirmatory benchmark before any public comparative claim",
    }


def _result_document(
    spec: dict[str, Any],
    spec_sha256: str,
    runs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema": 1,
        "benchmark_id": spec["benchmark_id"],
        "classification": "pilot-signal-only",
        "spec_sha256": spec_sha256,
        "provenance": {
            "runtime": spec["runtime"],
            "methodology_pins": {
                method["id"]: method["commit"] for method in spec["methodologies"]
            },
            "expected_runs": spec["claim_policy"]["required_live_runs"],
        },
        "runs": runs,
        "summary": summarize_results(runs),
    }


def _write_checkpoint(output: Path, document: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)


def _write_failure_diagnostic(
    output: Path,
    *,
    run_id: str,
    process_stdout: str,
    process_stderr: str,
    last_agent_message: str,
    visible_stdout: str,
    visible_stderr: str,
    hidden_stdout: str,
    hidden_stderr: str,
    changed_paths: list[str],
) -> Path:
    """Write ignored, local-only raw diagnostics for an unsuccessful live run."""
    path = output.with_name(f"{output.stem}.{run_id}.diagnostic.json")
    document = {
        "schema": 1,
        "run_id": run_id,
        "notice": "local-only unsanitized diagnostic; do not publish",
        "process_stdout": process_stdout,
        "process_stderr": process_stderr,
        "last_agent_message": last_agent_message,
        "visible_tests_stdout": visible_stdout,
        "visible_tests_stderr": visible_stderr,
        "hidden_check_stdout": hidden_stdout,
        "hidden_check_stderr": hidden_stderr,
        "changed_paths": changed_paths,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def _load_checkpoint(
    output: Path,
    expected_document: dict[str, Any],
    planned_runs: list[PlannedRun],
) -> list[dict[str, Any]]:
    if not output.exists():
        return []
    try:
        existing = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise BenchmarkError("existing checkpoint is unreadable") from error
    if not isinstance(existing, dict):
        raise BenchmarkError("existing checkpoint must be a JSON object")
    for key in ("schema", "benchmark_id", "classification", "spec_sha256", "provenance"):
        if existing.get(key) != expected_document[key]:
            raise BenchmarkError(f"existing checkpoint has mismatched {key}")
    if not isinstance(existing.get("runs"), list):
        raise BenchmarkError("existing checkpoint runs must be a list")
    results = existing["runs"]
    expected_runs = {run.run_id: run for run in planned_runs}
    seen: set[str] = set()
    for result in results:
        if not isinstance(result, dict):
            raise BenchmarkError("existing checkpoint run must be an object")
        run_id = result.get("run_id")
        if run_id in seen or run_id not in expected_runs:
            raise BenchmarkError("existing checkpoint contains duplicate or unknown run IDs")
        planned = expected_runs[run_id]
        identity = (result.get("task_id"), result.get("methodology"), result.get("repetition"))
        if identity != (planned.task_id, planned.methodology, planned.repetition):
            raise BenchmarkError(f"existing checkpoint identity mismatch for {run_id}")
        if (
            result.get("state") == "runtime-failure"
            and result.get("input_tokens") is None
            and result.get("output_tokens") is None
            and result.get("tool_calls") == 0
        ):
            raise BenchmarkError(
                f"checkpoint contains pre-inference failure at {run_id}; "
                "create a successor preregistration instead of resuming"
            )
        if result.get("failure_code") == "zero-mutation":
            raise BenchmarkError(
                f"checkpoint contains zero-mutation execution failure at {run_id}; "
                "create a successor preregistration instead of resuming"
            )
        seen.add(run_id)
    return results


def _safe_environment() -> dict[str, str]:
    allowed = {"APPDATA", "CODEX_HOME", "COMSPEC", "HOMEDRIVE", "HOMEPATH", "LOCALAPPDATA", "PATH", "PATHEXT", "PROGRAMFILES", "PROGRAMFILES(X86)", "SYSTEMROOT", "TEMP", "TMP", "USERPROFILE", "USERNAME", "WINDIR"}
    environment = {key: value for key, value in os.environ.items() if key.upper() in allowed}
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def _default_model_catalog_path() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    return (Path(codex_home) if codex_home else Path.home() / ".codex") / "models_cache.json"


def verify_model_catalog(spec: dict[str, Any], catalog_path: Path | None = None) -> dict[str, str]:
    path = (catalog_path or _default_model_catalog_path()).resolve()
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise BenchmarkError(f"Codex model catalog is unavailable: {path}") from error
    models = document.get("models") if isinstance(document, dict) else None
    if not isinstance(models, list):
        raise BenchmarkError("Codex model catalog has no models list")
    requested_model = spec["runtime"]["model"]
    selected = next(
        (model for model in models if isinstance(model, dict) and model.get("slug") == requested_model),
        None,
    )
    if selected is None:
        raise BenchmarkError(f"model {requested_model} is absent from the local Codex catalog")
    requested_effort = spec["runtime"]["reasoning_effort"]
    levels = selected.get("supported_reasoning_levels", [])
    supported = {
        level.get("effort") if isinstance(level, dict) else level
        for level in levels
    }
    if requested_effort not in supported:
        raise BenchmarkError(
            f"reasoning effort {requested_effort} is unavailable for {requested_model}"
        )
    catalog_version = document.get("client_version")
    return {
        "path": str(path),
        "fetched_at": str(document.get("fetched_at", "unknown")),
        "client_version": str(catalog_version or "unknown"),
        "model": requested_model,
        "reasoning_effort": requested_effort,
    }


def verify_sandbox_runtime(
    executable: str,
    *,
    platform: str = sys.platform,
    helper_finder: Callable[[str], str | None] = shutil.which,
) -> dict[str, str]:
    if platform != "win32":
        return {"platform": platform, "status": "not-windows"}
    helper_name = "codex-windows-sandbox-setup.exe"
    sibling = Path(executable).resolve().with_name(helper_name)
    discovered = helper_finder(helper_name)
    if not sibling.is_file() and discovered is None:
        raise BenchmarkError(
            "Codex Windows sandbox helper is unavailable; "
            "repair the Codex installation before any live call"
        )
    return {
        "platform": platform,
        "status": "available",
        "helper": str(sibling if sibling.is_file() else Path(discovered).resolve()),
    }


def verify_permission_runtime(executable: str, spec: dict[str, Any]) -> dict[str, str]:
    profile = spec["runtime"].get("permission_profile")
    if profile != ":workspace":
        raise BenchmarkError("live benchmark requires the built-in :workspace permission profile")
    with tempfile.TemporaryDirectory(prefix="solodeveling-permission-probe-") as temporary:
        root = Path(temporary)
        marker = root / "permission-probe.txt"
        command = [
            executable,
            "sandbox",
            "--permission-profile",
            profile,
            "--cd",
            str(root),
            sys.executable,
            "-c",
            "from pathlib import Path; Path('permission-probe.txt').write_text('ok', encoding='utf-8')",
        ]
        process = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
            shell=False,
            env=_safe_environment(),
        )
        if process.returncode or not marker.is_file():
            raise BenchmarkError(
                "Codex :workspace permission profile cannot write to its workspace; "
                "repair runtime permissions before any live call"
            )
    return {"profile": profile, "status": "write-verified"}


def _initialize_repository(project: Path) -> None:
    commands = [
        ["git", "init", "--quiet"],
        ["git", "config", "user.name", "Benchmark Fixture"],
        ["git", "config", "user.email", "benchmark@example.invalid"],
        ["git", "add", "."],
        ["git", "commit", "--quiet", "-m", "benchmark seed"],
    ]
    for command in commands:
        result = _run(command, project)
        if result.returncode:
            raise BenchmarkError(f"fixture git preparation failed: {command[1]}: {result.stderr.strip()}")


def _source_commit(source: Path) -> str:
    result = _run(["git", "rev-parse", "HEAD"], source)
    if result.returncode:
        raise BenchmarkError(f"methodology source is not a git checkout: {source}")
    return result.stdout.strip()


def verify_sources(spec: dict[str, Any], sources: dict[str, Path]) -> None:
    expected_identifiers = {
        str(methodology["id"]) for methodology in spec["methodologies"]
    }
    if set(sources) != expected_identifiers:
        missing = sorted(expected_identifiers - set(sources))
        unexpected = sorted(set(sources) - expected_identifiers)
        raise BenchmarkError(
            f"source assignments must exactly match the spec; "
            f"missing={missing}, unexpected={unexpected}"
        )
    for methodology in spec["methodologies"]:
        identifier = methodology["id"]
        source = sources.get(identifier)
        if source is None:
            raise BenchmarkError(f"missing --{identifier}-source")
        actual = _source_commit(source)
        if actual != methodology["commit"]:
            raise BenchmarkError(f"{identifier} source is {actual}; expected {methodology['commit']}")
        status = _run(["git", "status", "--porcelain", "--untracked-files=all"], source)
        if status.returncode or status.stdout.strip():
            raise BenchmarkError(f"{identifier} source checkout must be clean")
        skill = source / "skills" / methodology["skill"] / "SKILL.md"
        if not skill.is_file():
            raise BenchmarkError(f"missing pinned root skill: {skill}")


def _install_methodology(source: Path, project: Path) -> None:
    destination = project / ".agents" / "skills"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source / "skills", destination)


def _verify_installed_methodology(project: Path, skill: str) -> None:
    installed = project / ".agents" / "skills" / skill / "SKILL.md"
    if not installed.is_file():
        raise BenchmarkError(f"installed Codex root skill is unavailable: {installed}")


def _changed_paths(project: Path, baseline: str) -> list[str]:
    status = _run(["git", "status", "--porcelain", "--untracked-files=all"], project)
    committed = _run(["git", "diff", "--name-only", baseline, "HEAD"], project)
    if status.returncode or committed.returncode:
        raise BenchmarkError("could not inspect benchmark worktree")
    paths = {line[3:].replace(chr(92), "/") for line in status.stdout.splitlines() if len(line) > 3}
    paths.update(line.replace(chr(92), "/") for line in committed.stdout.splitlines() if line)
    return sorted(
        path for path in paths
        if "/__pycache__/" not in f"/{path}" and not path.endswith((".pyc", ".pyo"))
    )


def _is_zero_mutation_failure(
    process_returncode: int | None,
    correct: bool,
    changed: list[str],
) -> bool:
    return process_returncode == 0 and not correct and not changed


def _runtime_version(executable: str) -> str:
    process = subprocess.run([executable, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15, check=False, shell=False)
    return (process.stdout or process.stderr).strip().splitlines()[0]


def _build_live_command(
    executable: str,
    spec: dict[str, Any],
    worktree: Path,
    last_message_path: Path,
) -> list[str]:
    runtime = spec["runtime"]
    profile = runtime.get("permission_profile")
    if profile != ":workspace":
        raise BenchmarkError("live benchmark requires the built-in :workspace permission profile")
    return [
        executable,
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--model",
        runtime["model"],
        "--config",
        f"model_reasoning_effort={json.dumps(runtime['reasoning_effort'])}",
        "--config",
        f"default_permissions={json.dumps(profile)}",
        "--config",
        'approval_policy="never"',
        "--output-last-message",
        str(last_message_path),
        "-C",
        str(worktree),
        "-",
    ]


def probe(spec: dict[str, Any], sources: dict[str, Path]) -> dict[str, Any]:
    require_live_ready(spec)
    executable = shutil.which(spec["runtime"]["executable"])
    if executable is None:
        raise BenchmarkError("codex executable is unavailable")
    version = _runtime_version(executable)
    if version != spec["runtime"]["cli_version"]:
        raise BenchmarkError(f"runtime is {version}; expected {spec['runtime']['cli_version']}")
    sandbox = verify_sandbox_runtime(executable)
    permissions = verify_permission_runtime(executable, spec)
    catalog = verify_model_catalog(spec)
    resolved = {key: value.resolve() for key, value in sources.items()}
    verify_sources(spec, resolved)
    document = plan_document(spec)
    document["source_checkouts"] = {key: str(value) for key, value in resolved.items()}
    document["runtime_verified"] = True
    document["sandbox_runtime_verified"] = sandbox
    document["permission_runtime_verified"] = permissions
    document["model_catalog_verified"] = catalog
    document["sources_verified"] = True
    source_arguments = "".join(
        f' --source "{identifier}={path}"'
        for identifier, path in resolved.items()
    )
    document["live_command"] = (
        "python scripts/comparative_benchmark.py run-live"
        f' --confirm "{spec["claim_policy"]["confirmation"]}"'
        + source_arguments
        + f" --output benchmarks/results/{spec['benchmark_id']}.json"
    )
    return document


def run_live(
    spec_path: Path,
    *,
    confirmation: str,
    output: Path,
    sources: dict[str, Path] | None = None,
    solodeveling_source: Path | None = None,
    superpowers_source: Path | None = None,
) -> dict[str, Any]:
    spec = load_spec(spec_path)
    require_live_ready(spec)
    spec_sha256 = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    expected_confirmation = spec["claim_policy"]["confirmation"]
    if confirmation != expected_confirmation:
        raise BenchmarkError(f"live execution requires exact confirmation: {expected_confirmation}")
    executable = shutil.which(spec["runtime"]["executable"])
    if executable is None:
        raise BenchmarkError("codex executable is unavailable")
    version = _runtime_version(executable)
    if version != spec["runtime"]["cli_version"]:
        raise BenchmarkError(f"runtime is {version}; expected {spec['runtime']['cli_version']}")
    verify_sandbox_runtime(executable)
    verify_permission_runtime(executable, spec)
    verify_model_catalog(spec)
    if sources is None:
        sources = {}
        if solodeveling_source is not None:
            sources["solodeveling"] = solodeveling_source
        if superpowers_source is not None:
            sources["superpowers"] = superpowers_source
    sources = {identifier: path.resolve() for identifier, path in sources.items()}
    verify_sources(spec, sources)
    tasks = {task["id"]: task for task in spec["tasks"]}
    methods = {method["id"]: method for method in spec["methodologies"]}
    planned_runs = build_plan(spec)
    expected_document = _result_document(spec, spec_sha256, [])
    results = _load_checkpoint(output, expected_document, planned_runs)
    with tempfile.TemporaryDirectory(prefix="solodeveling-comparative-live-") as temporary:
        temp_root = Path(temporary)
        completed_ids = {result["run_id"] for result in results}
        for planned in planned_runs:
            if planned.run_id in completed_ids:
                continue
            task = tasks[planned.task_id]
            method = methods[planned.methodology]
            repository = temp_root / f"{planned.run_id}-repo"
            worktree = temp_root / f"{planned.run_id}-worktree"
            shutil.copytree(spec_path.parent / task["fixture"], repository)
            _install_methodology(sources[planned.methodology], repository)
            _verify_installed_methodology(repository, method["skill"])
            _initialize_repository(repository)
            baseline = _run(["git", "rev-parse", "HEAD"], repository).stdout.strip()
            added = _run(["git", "worktree", "add", "--quiet", "--detach", str(worktree), "HEAD"], repository)
            if added.returncode:
                raise BenchmarkError(f"could not create fresh worktree for {planned.run_id}: {added.stderr.strip()}")
            prompt = f"{method['invocation']}\n\nThe requirements below are final and approved. Work autonomously in this already-isolated git worktree. Do not use the network or ask for approval. Run the tests and report completion.\n\n{task['prompt']}"
            last_message_path = temp_root / f"{planned.run_id}-last-message.txt"
            command = _build_live_command(executable, spec, worktree, last_message_path)
            started = time.perf_counter()
            try:
                process = subprocess.run(command, input=prompt, cwd=worktree, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=int(spec["runtime"]["timeout_seconds"]), check=False, shell=False, env=_safe_environment())
                state = "completed" if process.returncode == 0 else "runtime-failure"
                failure_code = None if process.returncode == 0 else classify_runtime_failure(process.stdout, process.stderr)
                process_returncode = process.returncode
                stdout = process.stdout
                stderr = process.stderr
                lines = stdout.splitlines()
            except subprocess.TimeoutExpired as error:
                process = None
                state = "timeout"
                failure_code = "timeout"
                process_returncode = None
                stdout = error.stdout.decode("utf-8", "replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
                stderr = error.stderr.decode("utf-8", "replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
                lines = stdout.splitlines()
            elapsed = round(time.perf_counter() - started, 4)
            visible = _run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], worktree)
            hidden = _run([sys.executable, str((spec_path.parent / task["hidden_check"]).resolve()), str(worktree), baseline], worktree)
            correct = state == "completed" and visible.returncode == 0 and hidden.returncode == 0
            if not correct and state == "completed":
                state = "correctness-failure"
            activity = parse_codex_jsonl(lines)
            changed = _changed_paths(worktree, baseline)
            if _is_zero_mutation_failure(process_returncode, correct, changed):
                state = "execution-failure"
                failure_code = "zero-mutation"
            if not correct:
                _write_failure_diagnostic(
                    output,
                    run_id=planned.run_id,
                    process_stdout=stdout,
                    process_stderr=stderr,
                    last_agent_message=(
                        last_message_path.read_text(encoding="utf-8", errors="replace")
                        if last_message_path.is_file()
                        else ""
                    ),
                    visible_stdout=visible.stdout,
                    visible_stderr=visible.stderr,
                    hidden_stdout=hidden.stdout,
                    hidden_stderr=hidden.stderr,
                    changed_paths=changed,
                )
            workflow = [path for path in changed if path.startswith((".solodeveling/", "docs/superpowers/"))]
            results.append({
                "run_id": planned.run_id, "task_id": planned.task_id, "methodology": planned.methodology,
                "repetition": planned.repetition, "order": planned.order, "state": state, "correct": correct,
                "elapsed_seconds": elapsed, **activity, "changed_files": len(changed), "workflow_artifacts": len(workflow),
                "human_interventions": 0,
                "failure_code": failure_code, "process_returncode": process_returncode,
                "runtime_version": version, "model": spec["runtime"]["model"], "reasoning_effort": spec["runtime"]["reasoning_effort"],
                "visible_tests_passed": visible.returncode == 0, "hidden_check_passed": hidden.returncode == 0,
            })
            _write_checkpoint(output, _result_document(spec, spec_sha256, results))
            if (
                state == "runtime-failure"
                and activity["input_tokens"] is None
                and activity["output_tokens"] is None
                and activity["tool_calls"] == 0
            ):
                raise BenchmarkError(
                    f"pre-inference failure at {planned.run_id} "
                    f"({failure_code}); stopped before the next call"
                )
            if failure_code == "zero-mutation":
                raise BenchmarkError(
                    f"zero-mutation execution failure at {planned.run_id}; "
                    "stopped before the next call"
                )
    document = _result_document(spec, spec_sha256, results)
    _write_checkpoint(output, document)
    return document


def score_file(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("classification") != "pilot-signal-only" or not isinstance(document.get("runs"), list):
        raise BenchmarkError("not a sanitized pilot result document")
    return summarize_results(document["runs"])


def _source_mapping(
    assignments: list[str],
    *,
    solodeveling_source: Path | None = None,
    superpowers_source: Path | None = None,
) -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for assignment in assignments:
        identifier, separator, raw_path = assignment.partition("=")
        if not separator or not identifier or not raw_path:
            raise BenchmarkError("--source must use METHODOLOGY_ID=CHECKOUT_PATH")
        if identifier in sources:
            raise BenchmarkError(f"duplicate source assignment for {identifier}")
        sources[identifier] = Path(raw_path)
    if solodeveling_source is not None:
        sources.setdefault("solodeveling", solodeveling_source)
    if superpowers_source is not None:
        sources.setdefault("superpowers", superpowers_source)
    return sources


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Controlled Solodeveling/Superpowers pilot benchmark")
    parser.add_argument("--spec", type=Path, default=Path("benchmarks/comparative/pilot.yaml"))
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("plan")
    subparsers.add_parser("verify-fixtures")
    source_probe = subparsers.add_parser("probe")
    source_probe.add_argument("--source", action="append", default=[])
    source_probe.add_argument("--solodeveling-source", type=Path)
    source_probe.add_argument("--superpowers-source", type=Path)
    score = subparsers.add_parser("score")
    score.add_argument("result", type=Path)
    live = subparsers.add_parser("run-live")
    live.add_argument("--confirm", required=True)
    live.add_argument("--source", action="append", default=[])
    live.add_argument("--solodeveling-source", type=Path)
    live.add_argument("--superpowers-source", type=Path)
    live.add_argument("--output", type=Path, default=Path("benchmarks/results/pilot-2.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "plan":
            result = plan_document(load_spec(args.spec))
        elif args.command == "verify-fixtures":
            result = {"fixtures": verify_fixtures(args.spec), "live": False}
        elif args.command == "probe":
            result = probe(
                load_spec(args.spec),
                _source_mapping(
                    args.source,
                    solodeveling_source=args.solodeveling_source,
                    superpowers_source=args.superpowers_source,
                ),
            )
        elif args.command == "score":
            result = score_file(args.result)
        else:
            result = run_live(
                args.spec,
                confirmation=args.confirm,
                sources=_source_mapping(
                    args.source,
                    solodeveling_source=args.solodeveling_source,
                    superpowers_source=args.superpowers_source,
                ),
                output=args.output,
            )
    except BenchmarkError as error:
        print(f"benchmark error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
