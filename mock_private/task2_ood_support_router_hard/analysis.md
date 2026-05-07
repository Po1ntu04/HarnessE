# task2_ood_support_router_hard

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['account_access', 'billing_dispute', 'technical_bug', 'feature_request', 'security_risk', 'cancellation', 'data_export', 'service_outage']`
Train/Test counts: 24 / 24
Train label counts: `{'account_access': 3, 'billing_dispute': 3, 'cancellation': 3, 'data_export': 3, 'feature_request': 3, 'security_risk': 3, 'service_outage': 3, 'technical_bug': 3}`
Test label counts: `{'account_access': 3, 'billing_dispute': 3, 'cancellation': 3, 'data_export': 3, 'feature_request': 3, 'security_risk': 3, 'service_outage': 3, 'technical_bug': 3}`

## Why this task exists

Non-banking SaaS and IT support routing with overlapping support language.

## Hard slices

- `runtime_label_schema`
- `multi_intent_but_primary_clear`
- `service_outage_vs_bug`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
