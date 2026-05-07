# short_label_sentiment analysis

- family: `ood_classification`
- expected profile: `classification_like`
- labels: 4
- train records: 12
- test records: 8
- average train text chars: 47.3
- average test text chars: 48.2
- train label counts: `{'mixed': 3, 'negative': 3, 'neutral': 3, 'positive': 3}`
- test label counts: `{'mixed': 2, 'negative': 2, 'neutral': 2, 'positive': 2}`

## Purpose

Sentiment classification with short labels and mixed statements.

## Stress dimensions

- short labels
- label-name reliance
- ambiguous sentiment
- mixed class handling

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
