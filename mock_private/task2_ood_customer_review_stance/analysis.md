# task2_ood_customer_review_stance

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['supportive', 'opposed', 'uncertain', 'request_more_info', 'off_topic']`
Train/Test counts: 15 / 20
Train label counts: `{'off_topic': 3, 'opposed': 3, 'request_more_info': 3, 'supportive': 3, 'uncertain': 3}`
Test label counts: `{'off_topic': 4, 'opposed': 4, 'request_more_info': 4, 'supportive': 4, 'uncertain': 4}`

## Why this task exists

Stance classification toward a product or policy.

## Hard slices

- `stance_not_sentiment`
- `off_topic`
- `request_more_info`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
