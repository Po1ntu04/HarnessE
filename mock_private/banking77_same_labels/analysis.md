# banking77_same_labels analysis

- family: `banking_same`
- expected profile: `classification_like`
- labels: 8
- train records: 24
- test records: 18
- average train text chars: 46.5
- average test text chars: 51.8
- train label counts: `{'Refund_not_showing_up': 3, 'card_arrival': 3, 'card_delivery_estimate': 3, 'declined_cash_withdrawal': 3, 'declined_transfer': 3, 'pending_card_payment': 3, 'pending_transfer': 3, 'request_refund': 3}`
- test label counts: `{'Refund_not_showing_up': 2, 'card_arrival': 3, 'card_delivery_estimate': 3, 'declined_cash_withdrawal': 2, 'declined_transfer': 2, 'pending_card_payment': 2, 'pending_transfer': 2, 'request_refund': 2}`

## Purpose

Banking-style fine-grained intent classification with same-label new texts.

## Stress dimensions

- near-label ambiguity
- short customer utterances
- case-sensitive and punctuation-sensitive labels
- retrieval candidate recall

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
