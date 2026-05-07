# task1_banking77_injected_slice

Group: `task1_similar_label`
Profile: `classification_like_with_injection`
Labels: `['card_arrival', 'pending_transfer', 'declined_card_payment', 'verify_my_identity', 'pending_top_up_by_bank_card', 'lost_or_stolen_card', 'Refund_not_showing_up', 'request_refund', 'card_payment_not_recognised', 'cash_withdrawal_not_recognised']`
Train/Test counts: 30 / 30
Train label counts: `{'Refund_not_showing_up': 3, 'card_arrival': 3, 'card_payment_not_recognised': 3, 'cash_withdrawal_not_recognised': 3, 'declined_card_payment': 3, 'lost_or_stolen_card': 3, 'pending_top_up_by_bank_card': 3, 'pending_transfer': 3, 'request_refund': 3, 'verify_my_identity': 3}`
Test label counts: `{'Refund_not_showing_up': 2, 'card_arrival': 4, 'card_payment_not_recognised': 3, 'cash_withdrawal_not_recognised': 4, 'declined_card_payment': 3, 'lost_or_stolen_card': 2, 'pending_top_up_by_bank_card': 3, 'pending_transfer': 3, 'request_refund': 3, 'verify_my_identity': 3}`

## Why this task exists

Small injected slice inside task1: injected text remains data and must still map to a banking label.

## Hard slices

- `direct_override`
- `role_mimic`
- `delimiter_escape`
- `false_label_attack`
- `json_format_attack`
- `choice_answer_attack`
- `benign_injection_keyword_control`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
