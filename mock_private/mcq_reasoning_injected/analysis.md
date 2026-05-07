# mcq_reasoning_injected analysis

- family: `mcq`
- expected profile: `mcq_like_with_injection`
- labels: 4
- train records: 8
- test records: 8
- average train text chars: 111.0
- average test text chars: 152.4
- train label counts: `{'A': 2, 'B': 2, 'C': 2, 'D': 2}`
- test label counts: `{'A': 2, 'B': 2, 'C': 2, 'D': 2}`

## Purpose

Four-way reasoning questions with distractor instructions inside the text.

## Stress dimensions

- MCQ routing under instruction-like text
- answer cue parsing
- multi-sentence reasoning
- prompt injection inside question body

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
