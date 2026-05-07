from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_no}: invalid JSONL row: {exc}") from exc
    return rows


def load_predictions(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return load_jsonl(path)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("predictions"), list):
            return data["predictions"]
        raise SystemExit("JSON predictions must be a list or an object with a predictions list")
    if suffix in {".tsv", ".txt"}:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return [dict(row) for row in csv.DictReader(fh, delimiter="\t")]
    raise SystemExit(f"unsupported prediction format: {path.suffix}")


def build_gold(root: Path, tasks: list[dict]) -> dict[tuple[str, int], str]:
    gold: dict[tuple[str, int], str] = {}
    for task in tasks:
        task_id = task["task_id"]
        for idx, row in enumerate(load_jsonl(root / task_id / "test.jsonl")):
            gold[(task_id, idx)] = row["label"]
    return gold


def fmt(value: float) -> str:
    return f"{value:.4f}"


def mode_group_score(per_task: dict[str, dict[str, float]], tasks: list[dict], mode: str, group: str) -> float:
    values = [per_task[task["task_id"]]["accuracy"] for task in tasks if task.get("mode") == mode and task["group"] == group]
    return mean(values) if values else 0.0


def score(root: Path, prediction_rows: list[dict]) -> str:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    tasks = manifest["tasks"]
    task_by_id = {task["task_id"]: task for task in tasks}
    labels_by_task = {task["task_id"]: set(task["labels"]) for task in tasks}
    gold = build_gold(root, tasks)

    predictions: dict[tuple[str, int], str] = {}
    invalid_label_count = 0
    duplicate_prediction_count = 0
    extra_prediction_count = 0
    malformed_prediction_count = 0

    for row in prediction_rows:
        try:
            task_id = str(row["task"])
            idx = int(row["idx"])
            prediction = str(row["prediction"]).strip()
        except (KeyError, TypeError, ValueError):
            malformed_prediction_count += 1
            continue
        key = (task_id, idx)
        if task_id not in task_by_id or key not in gold:
            extra_prediction_count += 1
            continue
        if prediction not in labels_by_task[task_id]:
            invalid_label_count += 1
        if key in predictions:
            duplicate_prediction_count += 1
        predictions[key] = prediction

    per_task: dict[str, dict[str, float]] = {}
    total_correct = 0
    total_records = 0
    for task in tasks:
        task_id = task["task_id"]
        keys = [(key, label) for key, label in gold.items() if key[0] == task_id]
        correct = sum(1 for key, label in keys if predictions.get(key) == label)
        total = len(keys)
        missing = sum(1 for key, _ in keys if key not in predictions)
        per_task[task_id] = {
            "accuracy": correct / total if total else 0.0,
            "correct": float(correct),
            "total": float(total),
            "missing": float(missing),
        }
        total_correct += correct
        total_records += total

    weights = manifest.get("official_weights", {
        "task1_similar_label": 0.20,
        "task2_ood_classification": 0.60,
        "task3_mcq": 0.20,
    })
    standard_task1 = mode_group_score(per_task, tasks, "standard", "task1_similar_label")
    standard_task2 = mode_group_score(per_task, tasks, "standard", "task2_ood_classification")
    standard_task3 = mode_group_score(per_task, tasks, "standard", "task3_mcq")
    standard_score = (
        weights["task1_similar_label"] * standard_task1
        + weights["task2_ood_classification"] * standard_task2
        + weights["task3_mcq"] * standard_task3
    )

    stress_values = [per_task[task["task_id"]]["accuracy"] for task in tasks if task.get("mode") == "stress"]
    stress_task_macro = mean(stress_values) if stress_values else 0.0
    task_macro_average = mean(value["accuracy"] for value in per_task.values()) if per_task else 0.0
    record_micro_average = total_correct / total_records if total_records else 0.0

    lines: list[str] = []
    lines.append("# Mock Private v3 Score")
    lines.append("")
    lines.append("| Task | Mode | Group | Accuracy | Correct | Total | Missing |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for task in tasks:
        values = per_task[task["task_id"]]
        lines.append(
            f"| `{task['task_id']}` | {task.get('mode', 'standard')} | {task['group']} | {fmt(values['accuracy'])} | "
            f"{int(values['correct'])} | {int(values['total'])} | {int(values['missing'])} |"
        )
    lines.append("")
    lines.append("## Aggregates")
    lines.append("")
    lines.append(f"- standard_task1_score: {fmt(standard_task1)}")
    lines.append(f"- standard_task2_score: {fmt(standard_task2)}")
    lines.append(f"- standard_task3_score: {fmt(standard_task3)}")
    lines.append(f"- standard_official_mock_score: {fmt(standard_score)}")
    lines.append(f"- stress_task_macro_average: {fmt(stress_task_macro)}")
    lines.append(f"- task_macro_average_all_modes: {fmt(task_macro_average)}")
    lines.append(f"- record_micro_average_all_modes: {fmt(record_micro_average)}")
    lines.append(f"- invalid_label_count: {invalid_label_count}")
    lines.append(f"- missing_prediction_count: {sum(int(value['missing']) for value in per_task.values())}")
    lines.append(f"- duplicate_prediction_count: {duplicate_prediction_count}")
    lines.append(f"- extra_prediction_count: {extra_prediction_count}")
    lines.append(f"- malformed_prediction_count: {malformed_prediction_count}")
    return "\n".join(lines) + "\n"


def gold_predictions(root: Path, tasks: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for task in tasks:
        for idx, row in enumerate(load_jsonl(root / task["task_id"] / "test.jsonl")):
            rows.append({"task": task["task_id"], "idx": idx, "prediction": row["label"], "label": row["label"]})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Score HarnessE mock_private v3 predictions.")
    parser.add_argument("root", help="mock_private dataset directory")
    parser.add_argument("predictions", nargs="?", help="JSONL/JSON/TSV predictions")
    parser.add_argument("--gold", action="store_true", help="score gold labels as a scorer self-check")
    args = parser.parse_args()
    root = Path(args.root)
    if args.gold:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        rows = gold_predictions(root, manifest["tasks"])
    elif args.predictions:
        rows = load_predictions(Path(args.predictions))
    else:
        raise SystemExit("provide a predictions file or pass --gold")
    print(score(root, rows))


if __name__ == "__main__":
    main()
