# stress_task2_high_cardinality_long_labels

Mode: stress
Group: task2_ood_classification
Profile: classification_like_high_cardinality
Languages: en
Scripts: Latin
Label language: en-long
Labels: 120
Train/Test counts: 120/48
All-label token estimate: 2280
Expected solver: retrieval_required_no_all_label_prompt

Why this task exists:
High-cardinality long labels; all-label prompt is intentionally too large.

Hard slices:
- high_cardinality
- all_labels_token_pressure
- science_domain

Expected failure modes:
- English-only prompts miss non-English semantics.
- Label normalization that lowercases, removes accents, or half-width-normalizes labels can break exact match.
- All-label prompts fail on high-cardinality or long-label tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls and Unicode option labels.
- Prompt-injection text must be treated as data in every language.

Notes for audit:
- Records contain only text and label.
- Test labels appear in train.
- Train/test exact normalized overlap is not allowed.
