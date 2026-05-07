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


def load_jsonl_labels(path: Path) -> list[str]:
    return [row["label"] for row in load_jsonl(path)]


def build_gold(root: Path, tasks: list[dict]) -> dict[tuple[str, int], str]:
    gold: dict[tuple[str, int], str] = {}
    for task in tasks:
        task_id = task["task_id"]
        labels = load_jsonl_labels(root / task_id / "test.jsonl")
        for idx, label in enumerate(labels):
            gold[(task_id, idx)] = label
    return gold


def format_score(value: float) -> str:
    return f"{value:.4f}"


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
    malformed_count = 0

    for row in prediction_rows:
        try:
            task_id = str(row["task"])
            idx = int(row["idx"])
            prediction = str(row["prediction"]).strip()
        except (KeyError, TypeError, ValueError):
            malformed_count += 1
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

    per_task: dict[str, dict[str, int | float]] = {}
    total_correct = 0
    total_records = 0
    for task in tasks:
        task_id = task["task_id"]
        task_gold = [(key, label) for key, label in gold.items() if key[0] == task_id]
        correct = sum(1 for key, label in task_gold if predictions.get(key) == label)
        total = len(task_gold)
        missing = sum(1 for key, _ in task_gold if key not in predictions)
        accuracy = correct / total if total else 0.0
        per_task[task_id] = {
            "correct": correct,
            "total": total,
            "missing": missing,
            "accuracy": accuracy,
        }
        total_correct += correct
        total_records += total

    task1_weights = manifest["task1_internal_weights"]
    task1_score = sum(per_task[task_id]["accuracy"] * weight for task_id, weight in task1_weights.items())
    task2_tasks = [task["task_id"] for task in tasks if task["group"] == "task2_ood_classification"]
    task3_tasks = [task["task_id"] for task in tasks if task["group"] == "task3_mcq"]
    task2_score = mean(per_task[task_id]["accuracy"] for task_id in task2_tasks) if task2_tasks else 0.0
    task3_score = mean(per_task[task_id]["accuracy"] for task_id in task3_tasks) if task3_tasks else 0.0
    official_weights = manifest["official_weights"]
    official_mock_score = (
        official_weights["task1_similar_label"] * task1_score
        + official_weights["task2_ood_classification"] * task2_score
        + official_weights["task3_mcq"] * task3_score
    )
    task_macro_average = mean(values["accuracy"] for values in per_task.values()) if per_task else 0.0
    record_micro_average = total_correct / total_records if total_records else 0.0

    lines: list[str] = []
    lines.append("# Mock Private v2 Score")
    lines.append("")
    lines.append("| Task | Accuracy | Correct | Total | Missing |")
    lines.append("|---|---:|---:|---:|---:|")
    for task in tasks:
        task_id = task["task_id"]
        values = per_task[task_id]
        lines.append(
            f"| `{task_id}` | {format_score(values['accuracy'])} | {values['correct']} | {values['total']} | {values['missing']} |"
        )
    lines.append("")
    lines.append("## Aggregates")
    lines.append("")
    lines.append(f"- task1_score: {format_score(task1_score)}")
    lines.append(f"- task2_score: {format_score(task2_score)}")
    lines.append(f"- task3_score: {format_score(task3_score)}")
    lines.append(f"- official_mock_score: {format_score(official_mock_score)}")
    lines.append(f"- task_macro_average: {format_score(task_macro_average)}")
    lines.append(f"- record_micro_average: {format_score(record_micro_average)}")
    lines.append(f"- invalid_label_count: {invalid_label_count}")
    lines.append(f"- missing_prediction_count: {sum(values['missing'] for values in per_task.values())}")
    lines.append(f"- duplicate_prediction_count: {duplicate_prediction_count}")
    lines.append(f"- extra_prediction_count: {extra_prediction_count}")
    lines.append(f"- malformed_prediction_count: {malformed_count}")
    return "\n".join(lines) + "\n"


def gold_predictions(root: Path, tasks: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for task in tasks:
        task_id = task["task_id"]
        labels = load_jsonl_labels(root / task_id / "test.jsonl")
        for idx, label in enumerate(labels):
            rows.append({"task": task_id, "idx": idx, "prediction": label, "label": label})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Score HarnessE mock_private v2 predictions.")
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
