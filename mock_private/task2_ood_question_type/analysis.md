# task2_ood_question_type

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['definition', 'entity', 'location', 'number', 'procedure', 'comparison']`
Train/Test counts: 18 / 18
Train label counts: `{'comparison': 3, 'definition': 3, 'entity': 3, 'location': 3, 'number': 3, 'procedure': 3}`
Test label counts: `{'comparison': 3, 'definition': 3, 'entity': 3, 'location': 3, 'number': 3, 'procedure': 3}`

## Why this task exists

Natural-language question type classification.

## Hard slices

- `question_type`
- `multiple_entities`
- `short_labels`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
