# mock_private

This directory is a local stress suite for HarnessE. It is not a runtime dependency for `solution.py`.

The private test weights are unknown, so the recommended primary summary is `family_macro_average`:

```text
score = mean(
  mean(tasks in banking_same),
  mean(tasks in prompt_injection),
  mean(tasks in ood_classification),
  mean(tasks in mcq)
)
```

A secondary `task_macro_average` treats all tasks equally.

## Families

- `banking_same`: Banking-style same-label new texts.
- `prompt_injection`: Same closed-set task, but test text contains instruction-like attacks.
- `ood_classification`: Non-banking closed-set classification with runtime labels.
- `mcq`: A/B/C/D option reasoning tasks.

## Tasks

- `banking77_same_labels`: family `banking_same`, profile `classification_like`, 24 train / 18 test / 8 labels.
- `banking77_injected`: family `prompt_injection`, profile `classification_like_with_injection`, 12 train / 12 test / 6 labels.
- `ood_support_router`: family `ood_classification`, profile `classification_like`, 18 train / 12 test / 6 labels.
- `news_topic_ood`: family `ood_classification`, profile `classification_like`, 12 train / 8 test / 4 labels.
- `research_intent_ood`: family `ood_classification`, profile `classification_like`, 15 train / 10 test / 5 labels.
- `short_label_sentiment`: family `ood_classification`, profile `classification_like`, 12 train / 8 test / 4 labels.
- `mcq_science`: family `mcq`, profile `mcq_like`, 8 train / 8 test / 4 labels.
- `mcq_reasoning_injected`: family `mcq`, profile `mcq_like_with_injection`, 8 train / 8 test / 4 labels.

## Use

Use these files to check whether a harness generalizes beyond the visible Banking77 DEV subset.
Do not load this directory inside the final submitted `solution.py`.
