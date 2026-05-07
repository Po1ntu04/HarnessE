# task2_ood_long_text_topic

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['education', 'environment', 'technology', 'public_health', 'finance', 'culture']`
Train/Test counts: 18 / 18
Train label counts: `{'culture': 3, 'education': 3, 'environment': 3, 'finance': 3, 'public_health': 3, 'technology': 3}`
Test label counts: `{'culture': 3, 'education': 3, 'environment': 3, 'finance': 3, 'public_health': 3, 'technology': 3}`

## Why this task exists

Long paragraph topic classification with distractors.

## Hard slices

- `long_text_with_distractors`
- `budget_pressure`
- `topic_primary`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
