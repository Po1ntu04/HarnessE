# task2_ood_sentiment_nuanced

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['positive', 'negative', 'mixed', 'neutral']`
Train/Test counts: 12 / 20
Train label counts: `{'mixed': 3, 'negative': 3, 'neutral': 3, 'positive': 3}`
Test label counts: `{'mixed': 5, 'negative': 5, 'neutral': 5, 'positive': 5}`

## Why this task exists

Nuanced sentiment classification with mixed and neutral statements.

## Hard slices

- `sentiment_reversal`
- `mixed_boundary`
- `short_labels`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
