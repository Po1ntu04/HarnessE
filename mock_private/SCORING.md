# mock_private v3 scoring

The primary score is computed on `mode == "standard"` tasks only, because the `stress` mode is an adversarial diagnostic extension.

```text
task1_score = mean(standard task1_similar_label subtask accuracies)
task2_score = mean(standard task2_ood_classification subtask accuracies)
task3_score = mean(standard task3_mcq subtask accuracies)

standard_official_mock_score = 0.20 * task1_score
                             + 0.60 * task2_score
                             + 0.20 * task3_score
```

Stress tasks should be reported as `stress_task_macro_average`, plus per-risk diagnostics for high-cardinality, Unicode exact match, multilingual injection, full-width options, and Chinese option labels.

`task_macro_average` and `record_micro_average` are diagnostics. They are not the primary metric.

Use:

```powershell
python scripts/score_mock_results.py mock_private predictions.jsonl
```
