# task2_ood_event_intent

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['registration', 'speaker_request', 'venue_logistics', 'sponsorship', 'agenda_change', 'attendee_support']`
Train/Test counts: 18 / 18
Train label counts: `{'agenda_change': 3, 'attendee_support': 3, 'registration': 3, 'speaker_request': 3, 'sponsorship': 3, 'venue_logistics': 3}`
Test label counts: `{'agenda_change': 3, 'attendee_support': 3, 'registration': 3, 'speaker_request': 3, 'sponsorship': 3, 'venue_logistics': 3}`

## Why this task exists

Event and conference request intent classification.

## Hard slices

- `event_domain`
- `multi_intent`
- `label_semantics`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
