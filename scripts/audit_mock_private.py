from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


STANDARD_EXPECTED = {
    "task1_similar_label": 4,
    "task2_ood_classification": 18,
    "task3_mcq": 8,
}


def normalize_text(text: str) -> str:
    return " ".join(re.findall(r"[\w]+", text.lower(), flags=re.UNICODE))


def has_option_structure(text: str, labels: list[str] | None = None) -> bool:
    labels = labels or ["A", "B", "C", "D"]
    escaped = [re.escape(label) for label in labels]
    if len(escaped) >= 4:
        joined = r".+".join([rf"{label}\s*[\.\):：、．]" for label in escaped[:4]])
        if re.search(joined, text, flags=re.IGNORECASE | re.DOTALL):
            return True
    patterns = [
        r"(?m)^\s*[A-D][\.\):：]\s+",
        r"(?m)^\s*\([A-D]\)\s+",
        r"(?m)^\s*[Ａ-Ｄ][\.\):：、．]\s+",
        r"(?m)^\s*[甲乙丙丁][\.\):：、．]\s+",
        r"Options?\s*:",
        r"选项\s*[:：]",
    ]
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns)


def script_name(text: str) -> set[str]:
    scripts: set[str] = set()
    checks = [
        ("Latin", r"[A-Za-z]"),
        ("Han", r"[\u3400-\u9fff]"),
        ("Kana", r"[\u3040-\u30ff]"),
        ("Arabic", r"[\u0600-\u06ff]"),
        ("Devanagari", r"[\u0900-\u097f]"),
        ("Thai", r"[\u0e00-\u0e7f]"),
        ("Hebrew", r"[\u0590-\u05ff]"),
        ("Greek", r"[\u0370-\u03ff]"),
        ("Georgian", r"[\u10a0-\u10ff]"),
        ("Ethiopic", r"[\u1200-\u137f]"),
        ("Fullwidth", r"[Ａ-Ｚａ-ｚ０-９]"),
    ]
    for name, pattern in checks:
        if re.search(pattern, text):
            scripts.add(name)
    return scripts


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


def text_stats(rows: list[dict[str, str]]) -> dict[str, int]:
    words = [len(re.findall(r"\S+", row["text"])) for row in rows]
    chars = [len(row["text"]) for row in rows]
    if not rows:
        return {"min_words": 0, "median_words": 0, "max_words": 0, "min_chars": 0, "median_chars": 0, "max_chars": 0}
    return {
        "min_words": min(words),
        "median_words": int(median(words)),
        "max_words": max(words),
        "min_chars": min(chars),
        "median_chars": int(median(chars)),
        "max_chars": max(chars),
    }


def min_test_required(task: dict) -> int:
    if task["mode"] == "stress":
        return 8
    if task["group"] == "task1_similar_label":
        return 16
    if task["group"] == "task2_ood_classification":
        return 18
    if task["group"] == "task3_mcq":
        return 16
    return 1


def audit(root: Path) -> tuple[str, bool]:
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    tasks = manifest.get("tasks", [])
    failures: list[str] = []
    warnings: list[str] = []
    per_task_rows: list[dict[str, object]] = []
    long_stats: list[tuple[str, dict[str, int]]] = []
    all_languages: dict[str, set[str]] = defaultdict(set)
    all_scripts: dict[str, set[str]] = defaultdict(set)
    science_tasks: list[str] = []
    unicode_label_count = 0
    injection_languages: set[str] = set()
    high_card_tasks: list[str] = []
    abcd_non_mcq_ok = False
    fullwidth_mq = False
    chinese_mq = False
    jsonl_problems: list[str] = []

    if manifest.get("version") != "mock_private_v3":
        failures.append(f"manifest version is {manifest.get('version')}, expected mock_private_v3")
    by_id = {task["task_id"]: task for task in tasks}
    actual_dirs = sorted(path.name for path in root.iterdir() if path.is_dir() and path.name.startswith(("standard_", "stress_")))
    if set(actual_dirs) != set(by_id):
        failures.append("top-level task directories do not exactly match manifest v3 tasks")

    standard_counts = Counter(task["group"] for task in tasks if task["mode"] == "standard")
    for group, expected in STANDARD_EXPECTED.items():
        if standard_counts[group] != expected:
            failures.append(f"standard {group} count is {standard_counts[group]}, expected {expected}")
    if sum(1 for task in tasks if task["mode"] == "stress") < 9:
        failures.append("stress mode has fewer than 9 tasks")

    for doc_name in ["README.md", "SCORING.md", "DATASET_ANALYSIS_CN.md"]:
        doc = root / doc_name
        if not doc.exists():
            failures.append(f"missing {doc_name}")
            continue
        content = doc.read_text(encoding="utf-8").lower()
        if "english-only" in content and "not" not in content:
            warnings.append(f"{doc_name} may contain an English-only assumption")
        has_unknown_weights = re.search(r"weights\s+unknown", content) or re.search(
            r"private\s+test\s+weights\s+are\s+unknown", content
        )
        if has_unknown_weights:
            failures.append(f"{doc_name} still contains obsolete unknown-weight wording")

    for task in tasks:
        task_id = task["task_id"]
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
        if observed_labels != set(labels):
            failures.append(f"{task_id}: manifest labels do not match train/test union")
        missing_test_from_train = sorted(set(test_labels) - set(train_labels))
        if missing_test_from_train:
            failures.append(f"{task_id}: test labels absent from train {missing_test_from_train}")
        if len(test) < min_test_required(task):
            failures.append(f"{task_id}: test count {len(test)} below minimum {min_test_required(task)}")
        if task.get("label_count") != len(labels):
            failures.append(f"{task_id}: label_count mismatch")
        if "languages" not in task or "scripts" not in task or "label_language" not in task:
            failures.append(f"{task_id}: missing v3 language/script metadata")

        train_norm = {normalize_text(row["text"]) for row in train}
        test_norm = {normalize_text(row["text"]) for row in test}
        overlap = train_norm & test_norm
        if overlap:
            failures.append(f"{task_id}: normalized train/test overlap count {len(overlap)}")

        empty_text = sum(1 for row in train + test if not row["text"].strip())
        empty_label = sum(1 for row in train + test if not row["label"].strip())
        if empty_text or empty_label:
            failures.append(f"{task_id}: empty text={empty_text}, empty label={empty_label}")

        for lang in task.get("languages", []):
            all_languages[task["mode"]].add(lang)
        for script in task.get("scripts", []):
            all_scripts[task["mode"]].add(script)
        unicode_label_count += sum(1 for label in labels if any(ord(ch) > 127 for ch in label))
        if "science_domain" in task.get("risk_tags", []):
            science_tasks.append(task_id)
        if "multilingual_prompt_injection" in task.get("risk_tags", []):
            injection_languages.update(task.get("languages", []))
        if task["label_count"] >= 120 and task.get("all_labels_token_est", 0) > 2048:
            high_card_tasks.append(task_id)

        option_count = sum(1 for row in train + test if has_option_structure(row["text"], labels))
        if task["group"] == "task3_mcq":
            if len(labels) != 4:
                failures.append(f"{task_id}: MCQ task must have 4 labels")
            if set(train_labels) != set(labels):
                failures.append(f"{task_id}: MCQ train split lacks at least one option label")
            if set(test_labels) != set(labels):
                failures.append(f"{task_id}: MCQ test split lacks at least one option label")
            if option_count != len(train) + len(test):
                failures.append(f"{task_id}: {len(train) + len(test) - option_count} MCQ records lack option structure")
            if set(labels) == {"Ａ", "Ｂ", "Ｃ", "Ｄ"}:
                fullwidth_mq = True
            if set(labels) == {"甲", "乙", "丙", "丁"}:
                chinese_mq = True
        if "abcd_non_mcq_negative_control" in task.get("risk_tags", []) or task_id.endswith("arbitrary_abcd_non_mcq"):
            if option_count:
                failures.append(f"{task_id}: detected option structure in A/B/C/D non-MCQ negative control")
            else:
                abcd_non_mcq_ok = True

        if task["task_id"].endswith("long_text_topic") or "long_science_passage" in task.get("risk_tags", []):
            long_stats.append((task_id, text_stats(test)))

        train_counts = [train_labels[label] for label in labels]
        test_counts = [test_labels[label] for label in labels]
        per_task_rows.append(
            {
                "task_id": task_id,
                "mode": task["mode"],
                "group": task["group"],
                "languages": ",".join(task.get("languages", [])),
                "scripts": ",".join(task.get("scripts", [])),
                "labels": len(labels),
                "train": len(train),
                "test": len(test),
                "train_minmax": f"{min(train_counts)}/{max(train_counts)}" if train_counts else "0/0",
                "test_minmax": f"{min(test_counts)}/{max(test_counts)}" if test_counts else "0/0",
                "label_token_est": task.get("all_labels_token_est", 0),
                "overlap": len(overlap),
                "options": option_count,
            }
        )

    if len(all_languages["standard"]) < 6 or "zh" not in all_languages["standard"] or "en" not in all_languages["standard"]:
        failures.append(f"standard multilingual coverage too small: {sorted(all_languages['standard'])}")
    if len(all_languages["stress"]) < 8:
        failures.append(f"stress language coverage below 8 languages/scripts: {sorted(all_languages['stress'])}")
    if len(all_scripts["stress"]) < 6:
        failures.append(f"stress script coverage below 6 scripts: {sorted(all_scripts['stress'])}")
    if len(science_tasks) < 6:
        failures.append(f"science-domain task coverage too small: {len(science_tasks)}")
    if unicode_label_count < 8:
        failures.append(f"Unicode label count too small: {unicode_label_count}")
    if not high_card_tasks:
        failures.append("missing high-cardinality task with label_count >= 120 and all_labels_token_est > 2048")
    if not any(task["task_id"] == "stress_task2_opaque_ids_300" and task["label_count"] >= 300 for task in tasks):
        failures.append("missing opaque L0001...L0300 stress task")
    if not abcd_non_mcq_ok:
        failures.append("A/B/C/D non-MCQ negative control missing or invalid")
    if not fullwidth_mq:
        failures.append("full-width Ａ/Ｂ/Ｃ/Ｄ MCQ task missing")
    if not chinese_mq:
        failures.append("Chinese 甲/乙/丙/丁 MCQ task missing")
    if len(injection_languages) < 5:
        failures.append(f"multilingual injection language coverage too small: {sorted(injection_languages)}")
    if jsonl_problems:
        failures.extend(jsonl_problems)

    lines: list[str] = []
    lines.append("# Mock Private v3 Audit")
    lines.append("")
    lines.append(f"Dataset root: `{root}`")
    lines.append(f"Manifest version: `{manifest.get('version')}`")
    lines.append(f"Task count: {len(tasks)}")
    lines.append(f"Mode counts: {dict(Counter(task['mode'] for task in tasks))}")
    lines.append(f"Standard group counts: {dict(standard_counts)}")
    lines.append("")
    lines.append("Official proxy scoring for standard mode:")
    lines.append("")
    lines.append("```text")
    lines.append("task1_score = mean(standard task1_similar_label subtask accuracies)")
    lines.append("task2_score = mean(standard task2_ood_classification subtask accuracies)")
    lines.append("task3_score = mean(standard task3_mcq subtask accuracies)")
    lines.append("standard_official_mock_score = 0.20 * task1_score + 0.60 * task2_score + 0.20 * task3_score")
    lines.append("```")
    lines.append("")
    lines.append("## Coverage Checks")
    lines.append("")
    lines.append(f"- Standard languages: {', '.join(sorted(all_languages['standard']))}")
    lines.append(f"- Stress languages: {', '.join(sorted(all_languages['stress']))}")
    lines.append(f"- Standard scripts: {', '.join(sorted(all_scripts['standard']))}")
    lines.append(f"- Stress scripts: {', '.join(sorted(all_scripts['stress']))}")
    lines.append(f"- Science-domain tasks: {len(science_tasks)}")
    lines.append(f"- Unicode label count: {unicode_label_count}")
    lines.append(f"- High-cardinality token-pressure tasks: {', '.join(high_card_tasks) if high_card_tasks else 'none'}")
    lines.append(f"- Multilingual injection languages: {', '.join(sorted(injection_languages))}")
    lines.append(f"- A/B/C/D non-MCQ negative control: {'PASS' if abcd_non_mcq_ok else 'FAIL'}")
    lines.append(f"- Full-width MCQ labels: {'PASS' if fullwidth_mq else 'FAIL'}")
    lines.append(f"- Chinese MCQ labels: {'PASS' if chinese_mq else 'FAIL'}")
    lines.append("")
    lines.append("## Per Task Checks")
    lines.append("")
    lines.append("| Task | Mode | Group | Languages | Scripts | Labels | Train | Test | Train min/max | Test min/max | Label token est | Overlap | Option markers |")
    lines.append("|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in per_task_rows:
        lines.append(
            f"| `{row['task_id']}` | {row['mode']} | {row['group']} | {row['languages']} | {row['scripts']} | "
            f"{row['labels']} | {row['train']} | {row['test']} | {row['train_minmax']} | {row['test_minmax']} | "
            f"{row['label_token_est']} | {row['overlap']} | {row['options']} |"
        )
    lines.append("")
    lines.append("## Long Text Stats")
    lines.append("")
    lines.append("| Task | Min words | Median words | Max words | Min chars | Median chars | Max chars |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for task_id, stats in long_stats:
        lines.append(f"| `{task_id}` | {stats['min_words']} | {stats['median_words']} | {stats['max_words']} | {stats['min_chars']} | {stats['median_chars']} | {stats['max_chars']} |")
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
    parser = argparse.ArgumentParser(description="Audit a HarnessE mock_private v3 dataset.")
    parser.add_argument("root", nargs="?", default="mock_private")
    args = parser.parse_args()
    content, ok = audit(Path(args.root))
    print(content)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
