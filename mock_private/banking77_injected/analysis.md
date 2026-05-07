# banking77_injected analysis

- family: `prompt_injection`
- expected profile: `classification_like_with_injection`
- labels: 6
- train records: 12
- test records: 12
- average train text chars: 37.2
- average test text chars: 80.7
- train label counts: `{'card_arrival': 2, 'declined_card_payment': 2, 'lost_or_stolen_card': 2, 'pending_transfer': 2, 'top_up_failed': 2, 'verify_my_identity': 2}`
- test label counts: `{'card_arrival': 2, 'declined_card_payment': 2, 'lost_or_stolen_card': 2, 'pending_transfer': 2, 'top_up_failed': 2, 'verify_my_identity': 2}`

## Purpose

Banking-style labels with injected instructions inside test text.

## Stress dimensions

- quoted-data boundary
- label mention attack
- instruction-like user text
- whitelist verifier

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
