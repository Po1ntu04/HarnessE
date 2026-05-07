# task2_ood_arbitrary_abcd_labels

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['A', 'B', 'C', 'D']`
Train/Test counts: 12 / 20
Train label counts: `{'A': 3, 'B': 3, 'C': 3, 'D': 3}`
Test label counts: `{'A': 5, 'B': 5, 'C': 5, 'D': 5}`

## Why this task exists

A/B/C/D are ordinary class IDs, not multiple-choice options.

## Hard slices

- `abcd_non_mcq_negative_control`
- `opaque_label_names`
- `router_false_positive`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.

## Special note

- A/B/C/D are ordinary class IDs, not MCQ options.
- Text intentionally does not contain option markers.
- This task catches routers that use label set alone to select MCQSolver.
