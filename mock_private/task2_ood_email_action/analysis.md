# task2_ood_email_action

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['reply_with_info', 'schedule_meeting', 'request_approval', 'forward_to_legal', 'archive_no_action', 'escalate_manager']`
Train/Test counts: 18 / 18
Train label counts: `{'archive_no_action': 3, 'escalate_manager': 3, 'forward_to_legal': 3, 'reply_with_info': 3, 'request_approval': 3, 'schedule_meeting': 3}`
Test label counts: `{'archive_no_action': 3, 'escalate_manager': 3, 'forward_to_legal': 3, 'reply_with_info': 3, 'request_approval': 3, 'schedule_meeting': 3}`

## Why this task exists

Work-email action routing from summaries and short messages.

## Hard slices

- `action_routing`
- `legal_terms_without_label`
- `archive_no_action`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
