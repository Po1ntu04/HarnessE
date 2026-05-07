# task1_banking77_confusable_pairs

Group: `task1_similar_label`
Profile: `classification_like`
Labels: `['card_arrival', 'card_delivery_estimate', 'pending_transfer', 'transfer_not_received_by_recipient', 'pending_card_payment', 'card_payment_not_recognised', 'request_refund', 'Refund_not_showing_up', 'reverted_card_payment?', 'cash_withdrawal_card', 'cash_withdrawal_charge', 'wrong_amount_of_cash_received', 'verify_my_identity', 'why_verify_identity']`
Train/Test counts: 42 / 56
Train label counts: `{'Refund_not_showing_up': 3, 'card_arrival': 3, 'card_delivery_estimate': 3, 'card_payment_not_recognised': 3, 'cash_withdrawal_card': 3, 'cash_withdrawal_charge': 3, 'pending_card_payment': 3, 'pending_transfer': 3, 'request_refund': 3, 'reverted_card_payment?': 3, 'transfer_not_received_by_recipient': 3, 'verify_my_identity': 3, 'why_verify_identity': 3, 'wrong_amount_of_cash_received': 3}`
Test label counts: `{'Refund_not_showing_up': 4, 'card_arrival': 4, 'card_delivery_estimate': 4, 'card_payment_not_recognised': 4, 'cash_withdrawal_card': 4, 'cash_withdrawal_charge': 4, 'pending_card_payment': 4, 'pending_transfer': 4, 'request_refund': 4, 'reverted_card_payment?': 4, 'transfer_not_received_by_recipient': 4, 'verify_my_identity': 4, 'why_verify_identity': 4, 'wrong_amount_of_cash_received': 4}`

## Why this task exists

Banking77-style slice built around high-confusion label pairs and clusters.

## Hard slices

- `confusable_label_pair`
- `not_x_but_y`
- `temporal_shift`
- `multi_intent_but_primary_clear`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.

## Notes for audit

- card_arrival vs card_delivery_estimate separates missing shipped card from future estimate.
- pending_transfer vs transfer_not_received_by_recipient separates sender-side status from recipient-side absence.
- refund/reverted/request labels separate requested refund, issued missing refund, and card payment reversal.
