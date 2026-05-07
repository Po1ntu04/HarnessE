# task2_ood_policy_clause_type

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['permission', 'prohibition', 'obligation', 'exception', 'definition', 'penalty']`
Train/Test counts: 18 / 18
Train label counts: `{'definition': 3, 'exception': 3, 'obligation': 3, 'penalty': 3, 'permission': 3, 'prohibition': 3}`
Test label counts: `{'definition': 3, 'exception': 3, 'obligation': 3, 'penalty': 3, 'permission': 3, 'prohibition': 3}`

## Why this task exists

Policy and contract clause type classification.

## Hard slices

- `legal_language`
- `keyword_variation`
- `clause_type`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
