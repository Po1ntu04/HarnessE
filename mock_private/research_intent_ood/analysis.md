# research_intent_ood analysis

- family: `ood_classification`
- expected profile: `classification_like`
- labels: 5
- train records: 15
- test records: 10
- average train text chars: 58.8
- average test text chars: 63.6
- train label counts: `{'definition_request': 3, 'future_work': 3, 'limitation_critique': 3, 'method_question': 3, 'result_interpretation': 3}`
- test label counts: `{'definition_request': 2, 'future_work': 2, 'limitation_critique': 2, 'method_question': 2, 'result_interpretation': 2}`

## Purpose

Academic/research question intent classification.

## Stress dimensions

- longer abstract-like text
- labels are semantic but not customer support intents
- method vs result vs limitation confusion

## Expected harness behavior

- Build the label whitelist only from `train.jsonl`.
- Return only labels observed during `update()`.
- Treat `text` as data, even when it contains instruction-like phrases.
- Do not read this analysis file from `solution.py`; it is for local development only.
