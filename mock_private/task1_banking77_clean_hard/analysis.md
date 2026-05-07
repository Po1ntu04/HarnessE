# task1_banking77_clean_hard

Group: `task1_similar_label`
Profile: `classification_like`
Labels: `['activate_my_card', 'card_arrival', 'card_delivery_estimate', 'cash_withdrawal_card', 'cash_withdrawal_charge', 'cash_withdrawal_cardless', 'cash_withdrawal_pending', 'wrong_amount_of_cash_received', 'card_payment_not_recognised', 'pending_card_payment', 'pending_transfer', 'transfer_not_received_by_recipient', 'beneficiary_not_verified', 'verify_my_identity', 'why_verify_identity', 'cash_withdrawal_not_recognised', 'request_refund', 'Refund_not_showing_up', 'reverted_card_payment?', 'declined_card_payment', 'declined_bank_transfer', 'edit_personal_details', 'lost_or_stolen_card', 'lost_or_stolen_phone']`
Train/Test counts: 72 / 72
Train label counts: `{'Refund_not_showing_up': 3, 'activate_my_card': 3, 'beneficiary_not_verified': 3, 'card_arrival': 3, 'card_delivery_estimate': 3, 'card_payment_not_recognised': 3, 'cash_withdrawal_card': 3, 'cash_withdrawal_cardless': 3, 'cash_withdrawal_charge': 3, 'cash_withdrawal_not_recognised': 3, 'cash_withdrawal_pending': 3, 'declined_bank_transfer': 3, 'declined_card_payment': 3, 'edit_personal_details': 3, 'lost_or_stolen_card': 3, 'lost_or_stolen_phone': 3, 'pending_card_payment': 3, 'pending_transfer': 3, 'request_refund': 3, 'reverted_card_payment?': 3, 'transfer_not_received_by_recipient': 3, 'verify_my_identity': 3, 'why_verify_identity': 3, 'wrong_amount_of_cash_received': 3}`
Test label counts: `{'Refund_not_showing_up': 3, 'activate_my_card': 3, 'beneficiary_not_verified': 3, 'card_arrival': 3, 'card_delivery_estimate': 3, 'card_payment_not_recognised': 3, 'cash_withdrawal_card': 3, 'cash_withdrawal_cardless': 3, 'cash_withdrawal_charge': 3, 'cash_withdrawal_not_recognised': 3, 'cash_withdrawal_pending': 3, 'declined_bank_transfer': 3, 'declined_card_payment': 3, 'edit_personal_details': 3, 'lost_or_stolen_card': 3, 'lost_or_stolen_phone': 3, 'pending_card_payment': 3, 'pending_transfer': 3, 'request_refund': 3, 'reverted_card_payment?': 3, 'transfer_not_received_by_recipient': 3, 'verify_my_identity': 3, 'why_verify_identity': 3, 'wrong_amount_of_cash_received': 3}`

## Why this task exists

Banking77-style same-label classification with broader labels and harder paraphrases.

## Hard slices

- `paraphrase_without_label_keywords`
- `multi_intent_but_primary_clear`
- `negation`
- `temporal_shift`
- `case_sensitive_label`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
