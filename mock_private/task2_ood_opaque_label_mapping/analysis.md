# task2_ood_opaque_label_mapping

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['alpha', 'beta', 'gamma', 'delta', 'epsilon']`
Train/Test counts: 20 / 20
Train label counts: `{'alpha': 4, 'beta': 4, 'delta': 4, 'epsilon': 4, 'gamma': 4}`
Test label counts: `{'alpha': 4, 'beta': 4, 'delta': 4, 'epsilon': 4, 'gamma': 4}`

## Why this task exists

Opaque label mapping where labels reveal no semantics.

## Hard slices

- `opaque_label_names`
- `label_name_overlap_failure`
- `runtime_examples_required`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
