# mcq_science analysis

- family: `mcq`
- expected profile: `mcq_like`
- labels: 4
- train records: 8
- test records: 8
- average train text chars: 101.1
- average test text chars: 113.8
- train label counts: `{'A': 2, 'B': 2, 'C': 2, 'D': 2}`
- test label counts: `{'A': 2, 'B': 2, 'C': 2, 'D': 2}`

## Purpose

Four-way science multiple-choice questions.

## Stress dimensions

- A/B/C/D short labels
- option reasoning
- independent letter parsing
- avoid label-name semantic assumptions

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
