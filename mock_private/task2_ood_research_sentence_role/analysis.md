# task2_ood_research_sentence_role

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['background', 'objective', 'method', 'result', 'limitation', 'future_work']`
Train/Test counts: 18 / 18
Train label counts: `{'background': 3, 'future_work': 3, 'limitation': 3, 'method': 3, 'objective': 3, 'result': 3}`
Test label counts: `{'background': 3, 'future_work': 3, 'limitation': 3, 'method': 3, 'objective': 3, 'result': 3}`

## Why this task exists

Research sentence role classification with close method/result/background boundaries.

## Hard slices

- `research_role`
- `method_result_confusion`
- `longer_text`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
