from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from statistics import median


GROUP_NAMES = {
    "task1_similar_label": "task1",
    "task2_ood_classification": "task2",
    "task3_mcq": "task3",
}


def normalize_text(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def has_option_structure(text: str) -> bool:
    patterns = [
        r"(?m)^\s*A[\.\):]\s+",
        r"(?m)^\s*\(A\)\s+",
        r"Options?\s*:",
        r"\bA[\.\):]\s+.+\bB[\.\):]\s+.+\bC[\.\):]\s+.+\bD[\.\):]\s+",
        r"\(A\)\s+.+\(B\)\s+.+\(C\)\s+.+\(D\)\s+",
    ]
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns)


def load_jsonl(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    problems: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            problems.append(f"{path}:{line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            problems.append(f"{path}:{line_no}: row is not an object")
            continue
        if set(row) != {"text", "label"}:
            problems.append(f"{path}:{line_no}: keys must be exactly text,label; got {sorted(row)}")
        text = row.get("text", "")
        label = row.get("label", "")
        if not isinstance(text, str) or not isinstance(label, str):
            problems.append(f"{path}:{line_no}: text and label must be strings")
            text = str(text)
            label = str(label)
        rows.append({"text": text, "label": label})
    return rows, problems


def min_test_required(task_id: str, group: str) -> int:
    if task_id == "task1_banking77_clean_hard":
        return 45
    if task_id == "task1_banking77_confusable_pairs":
        return 40
    if task_id == "task1_banking77_injected_slice":
        return 24
    if group == "task2_ood_classification":
        return 18
    if group == "task3_mcq":
        return 16
    return 1


def injection_like_ratio(rows: list[dict[str, str]]) -> tuple[int, float]:
    patterns = [
        r"ignore all previous",
        r"\bSYSTEM\b",
        r"```",
        r"new instruction",
        r"return json",
        r"account_closed",
        r"correct answer is [ABCD]",
        r"\boutput\s+[a-z_?]+",
    ]
    count = 0
    for row in rows:
        text = row["text"].lower()
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            count += 1
    ratio = count / len(rows) if rows else 0.0
    return count, ratio


def text_stats(rows: list[dict[str, str]]) -> dict[str, int | float]:
    chars = [len(row["text"]) for row in rows]
    words = [len(re.findall(r"\S+", row["text"])) for row in rows]
    if not rows:
        return {"min_chars": 0, "median_chars": 0, "max_chars": 0, "min_words": 0, "median_words": 0, "max_words": 0}
    return {
        "min_chars": min(chars),
        "median_chars": int(median(chars)),
        "max_chars": max(chars),
        "min_words": min(words),
        "median_words": int(median(words)),
        "max_words": max(words),
    }


def audit(root: Path) -> tuple[str, bool]:
    manifest_path = root / "manifest.json"
    failures: list[str] = []
    warnings: list[str] = []
    if not manifest_path.exists():
        raise SystemExit(f"missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    tasks = manifest.get("tasks", [])
    by_id = {task.get("task_id"): task for task in tasks}
    group_counts = Counter(task.get("group") for task in tasks)
    if len(tasks) != 23:
        failures.append(f"manifest task count is {len(tasks)}, expected 23")
    expected_group_counts = {
        "task1_similar_label": 3,
        "task2_ood_classification": 14,
        "task3_mcq": 6,
    }
    for group, expected in expected_group_counts.items():
        if group_counts[group] != expected:
            failures.append(f"{group} task count is {group_counts[group]}, expected {expected}")

    actual_task_dirs = sorted(path.name for path in root.iterdir() if path.is_dir() and path.name.startswith("task"))
    if set(actual_task_dirs) != set(by_id):
        failures.append("top-level task directories do not exactly match manifest tasks")

    for doc_name in ["README.md", "SCORING.md"]:
        doc = root / doc_name
        if not doc.exists():
            failures.append(f"missing {doc_name}")
            continue
        content = doc.read_text(encoding="utf-8").lower()
        if re.search(r"weights\s+unknown", content) or re.search(r"unknown\s+weights", content):
            failures.append(f"{doc_name} still contains obsolete unknown-weight wording")

    rows_for_table: list[dict[str, object]] = []
    long_stats: list[tuple[str, dict[str, int | float]]] = []
    task1_test_total = 0
    injection_summary = "not checked"
    jsonl_problems: list[str] = []

    for task in tasks:
        task_id = task["task_id"]
        group = task["group"]
        labels = list(task["labels"])
        task_dir = root / task_id
        train_path = task_dir / "train.jsonl"
        test_path = task_dir / "test.jsonl"
        if not train_path.exists() or not test_path.exists():
            failures.append(f"{task_id}: missing train.jsonl or test.jsonl")
            continue
        train, train_problems = load_jsonl(train_path)
        test, test_problems = load_jsonl(test_path)
        jsonl_problems.extend(train_problems)
        jsonl_problems.extend(test_problems)

        train_labels = Counter(row["label"] for row in train)
        test_labels = Counter(row["label"] for row in test)
        observed_labels = set(train_labels) | set(test_labels)
        manifest_labels = set(labels)
        if observed_labels != manifest_labels:
            failures.append(f"{task_id}: manifest labels do not match train/test union")
        missing_train_labels = sorted(manifest_labels - set(train_labels))
        if missing_train_labels:
            failures.append(f"{task_id}: train missing labels {missing_train_labels}")
        missing_test_from_train = sorted(set(test_labels) - set(train_labels))
        if missing_test_from_train:
            failures.append(f"{task_id}: test labels absent from train {missing_test_from_train}")

        train_norm = {normalize_text(row["text"]) for row in train}
        test_norm = {normalize_text(row["text"]) for row in test}
        overlap = sorted(train_norm & test_norm)
        if overlap:
            failures.append(f"{task_id}: normalized train/test overlap count {len(overlap)}")

        empty_text = sum(1 for row in train + test if not row["text"].strip())
        empty_label = sum(1 for row in train + test if not row["label"].strip())
        if empty_text or empty_label:
            failures.append(f"{task_id}: empty text={empty_text}, empty label={empty_label}")

        minimum = min_test_required(task_id, group)
        if len(test) < minimum:
            failures.append(f"{task_id}: test count {len(test)} below minimum {minimum}")
        if group == "task1_similar_label":
            task1_test_total += len(test)

        train_counts = [train_labels[label] for label in labels]
        test_counts = [test_labels[label] for label in labels]
        if train_counts and min(train_counts) < 2:
            failures.append(f"{task_id}: some label has fewer than 2 train examples")
        if test_counts and min(test_counts) < 2:
            failures.append(f"{task_id}: some label has fewer than 2 test examples")

        option_count = sum(1 for row in train + test if has_option_structure(row["text"]))
        if group == "task3_mcq":
            if labels != ["A", "B", "C", "D"]:
                failures.append(f"{task_id}: MCQ labels are {labels}, expected A/B/C/D")
            if set(train_labels) != {"A", "B", "C", "D"}:
                failures.append(f"{task_id}: MCQ train split does not contain all A/B/C/D")
            if set(test_labels) != {"A", "B", "C", "D"}:
                failures.append(f"{task_id}: MCQ test split does not contain all A/B/C/D")
            if option_count != len(train) + len(test):
                failures.append(f"{task_id}: {len(train) + len(test) - option_count} MCQ records lack option structure")
        if task_id == "task2_ood_arbitrary_abcd_labels" and option_count:
            failures.append(f"{task_id}: detected option structure in non-MCQ A/B/C/D negative control")
        if task_id == "task1_banking77_injected_slice":
            count, ratio = injection_like_ratio(test)
            injection_summary = f"{count}/{len(test)} = {ratio:.1%}"

        if task_id in {"task2_ood_long_text_topic", "task3_mcq_reading_comprehension"}:
            long_stats.append((task_id, text_stats(test)))

        rows_for_table.append(
            {
                "task_id": task_id,
                "group": GROUP_NAMES.get(group, group),
                "train": len(train),
                "test": len(test),
                "labels": len(labels),
                "train_minmax": f"{min(train_counts)}/{max(train_counts)}" if train_counts else "0/0",
                "test_minmax": f"{min(test_counts)}/{max(test_counts)}" if test_counts else "0/0",
                "overlap": len(overlap),
                "empty": empty_text + empty_label,
                "options": option_count,
            }
        )

    if task1_test_total < 100:
        failures.append(f"task1 total test count is {task1_test_total}, expected at least 100")
    if jsonl_problems:
        failures.extend(jsonl_problems)

    lines: list[str] = []
    lines.append("# Mock Private v2 Audit")
    lines.append("")
    lines.append(f"Dataset root: `{root}`")
    lines.append(f"Manifest version: `{manifest.get('version', 'unknown')}`")
    lines.append(f"Task count: {len(tasks)}")
    lines.append(f"Group counts: task1={group_counts['task1_similar_label']}, task2={group_counts['task2_ood_classification']}, task3={group_counts['task3_mcq']}")
    lines.append("")
    lines.append("Official mock score:")
    lines.append("")
    lines.append("```text")
    lines.append("task1_score = 0.50 * task1_banking77_clean_hard + 0.35 * task1_banking77_confusable_pairs + 0.15 * task1_banking77_injected_slice")
    lines.append("task2_score = mean(all task2_ood_* subtask accuracies)")
    lines.append("task3_score = mean(all task3_mcq_* subtask accuracies)")
    lines.append("official_mock_score = 0.20 * task1_score + 0.60 * task2_score + 0.20 * task3_score")
    lines.append("```")
    lines.append("")
    lines.append("## Per Task Checks")
    lines.append("")
    lines.append("| Task | Group | Train | Test | Labels | Train min/max | Test min/max | Overlap | Empty | Option markers |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in rows_for_table:
        lines.append(
            f"| `{row['task_id']}` | {row['group']} | {row['train']} | {row['test']} | {row['labels']} | "
            f"{row['train_minmax']} | {row['test_minmax']} | {row['overlap']} | {row['empty']} | {row['options']} |"
        )
    lines.append("")
    lines.append("## Special Checks")
    lines.append("")
    lines.append(f"- task1 injection-like test ratio: {injection_summary}")
    lines.append("- `task2_ood_arbitrary_abcd_labels`: A/B/C/D are ordinary class IDs and option markers must be 0.")
    lines.append("- MCQ tasks: labels must be exactly A/B/C/D and every record must contain an option structure.")
    lines.append("")
    lines.append("## Long Text Stats")
    lines.append("")
    lines.append("| Task | Test min words | Test median words | Test max words | Test min chars | Test median chars | Test max chars |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for task_id, stats in long_stats:
        lines.append(
            f"| `{task_id}` | {stats['min_words']} | {stats['median_words']} | {stats['max_words']} | "
            f"{stats['min_chars']} | {stats['median_chars']} | {stats['max_chars']} |"
        )
    if not long_stats:
        lines.append("| none | 0 | 0 | 0 | 0 | 0 | 0 |")
    lines.append("")
    lines.append("## PASS/FAIL")
    lines.append("")
    if failures:
        lines.append("FAIL")
        lines.append("")
        for failure in failures:
            lines.append(f"- {failure}")
    else:
        lines.append("PASS")
    if warnings:
        lines.append("")
        lines.append("Warnings:")
        for warning in warnings:
            lines.append(f"- {warning}")
    content = "\n".join(lines) + "\n"
    (root / "AUDIT.md").write_text(content, encoding="utf-8")
    return content, not failures


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a HarnessE mock_private v2 dataset.")
    parser.add_argument("root", nargs="?", default="mock_private", help="mock_private dataset directory")
    args = parser.parse_args()
    content, ok = audit(Path(args.root))
    print(content)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
