# news_topic_ood analysis

- family: `ood_classification`
- expected profile: `classification_like`
- labels: 4
- train records: 12
- test records: 8
- average train text chars: 59.3
- average test text chars: 58.5
- train label counts: `{'business': 3, 'sports': 3, 'technology': 3, 'world': 3}`
- test label counts: `{'business': 2, 'sports': 2, 'technology': 2, 'world': 2}`

## Purpose

Short news-topic classification with compact labels.

## Stress dimensions

- short labels
- topic classification
- non-support domain
- lexical overlap across economy and technology

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
