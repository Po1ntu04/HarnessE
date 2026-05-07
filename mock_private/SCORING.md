# SCORING

Primary score follows the official mock weighting:

```text
task1_score = 0.50 * task1_banking77_clean_hard
            + 0.35 * task1_banking77_confusable_pairs
            + 0.15 * task1_banking77_injected_slice

task2_score = mean(all task2_ood_* subtask accuracies)

task3_score = mean(all task3_mcq_* subtask accuracies)

official_mock_score = 0.20 * task1_score
                    + 0.60 * task2_score
                    + 0.20 * task3_score
```

Interpretation:

- Task 1 is 20% of the final score. Prompt injection is only a small slice inside task 1.
- Task 2 is 60% of the final score. OOD subtasks are equal-weighted.
- Task 3 is 20% of the final score. MCQ subtasks are equal-weighted.
- `task_macro_average` and `record_micro_average` are diagnostics only.

Use:

```powershell
python scripts/score_mock_results.py mock_private predictions.jsonl
```

Supported prediction JSONL format:

```json
{"task": "task_name", "idx": 0, "prediction": "...", "label": "..."}
```
