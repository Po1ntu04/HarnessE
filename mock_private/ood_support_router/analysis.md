# ood_support_router analysis

- family: `ood_classification`
- expected profile: `classification_like`
- labels: 6
- train records: 18
- test records: 12
- average train text chars: 46.8
- average test text chars: 51.2
- train label counts: `{'billing_question': 3, 'feature_request': 3, 'login_problem': 3, 'product_return': 3, 'shipping_status': 3, 'technical_bug': 3}`
- test label counts: `{'billing_question': 2, 'feature_request': 2, 'login_problem': 2, 'product_return': 2, 'shipping_status': 2, 'technical_bug': 2}`

## Purpose

Non-banking customer support routing with runtime labels.

## Stress dimensions

- OOD label inventory
- support-domain overlap
- label name semantics
- few-shot adaptation

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
