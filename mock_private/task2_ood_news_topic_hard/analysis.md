# task2_ood_news_topic_hard

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['world_affairs', 'business_markets', 'science_technology', 'health_medicine', 'climate_energy', 'sports_competition']`
Train/Test counts: 18 / 18
Train label counts: `{'business_markets': 3, 'climate_energy': 3, 'health_medicine': 3, 'science_technology': 3, 'sports_competition': 3, 'world_affairs': 3}`
Test label counts: `{'business_markets': 3, 'climate_energy': 3, 'health_medicine': 3, 'science_technology': 3, 'sports_competition': 3, 'world_affairs': 3}`

## Why this task exists

News summary topic classification with cross-topic distractors.

## Hard slices

- `short_labels`
- `topic_overlap`
- `non_support_domain`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
