# task2_ood_product_review_aspect

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['shipping_delivery', 'product_quality', 'price_value', 'usability', 'customer_service', 'return_refund']`
Train/Test counts: 18 / 18
Train label counts: `{'customer_service': 3, 'price_value': 3, 'product_quality': 3, 'return_refund': 3, 'shipping_delivery': 3, 'usability': 3}`
Test label counts: `{'customer_service': 3, 'price_value': 3, 'product_quality': 3, 'return_refund': 3, 'shipping_delivery': 3, 'usability': 3}`

## Why this task exists

Product review aspect classification.

## Hard slices

- `mixed_reviews`
- `aspect_focus`
- `return_vs_service`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
