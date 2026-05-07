# task3_mcq_logic_constraints

Group: `task3_mcq`
Profile: `mcq_like`
Labels: `['A', 'B', 'C', 'D']`
Train/Test counts: 12 / 20
Train label counts: `{'A': 3, 'B': 3, 'C': 3, 'D': 3}`
Test label counts: `{'A': 5, 'B': 5, 'C': 5, 'D': 5}`

## Why this task exists

Logic and ordering MCQ.

## Hard slices

- `logic_constraints`
- `multi_step_reasoning`
- `answer_distribution_balanced`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
