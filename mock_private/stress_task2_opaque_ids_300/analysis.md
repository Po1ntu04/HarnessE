# stress_task2_opaque_ids_300

Mode: stress
Group: task2_ood_classification
Profile: classification_like_high_cardinality
Languages: en
Scripts: Latin
Label language: opaque-id
Labels: 300
Train/Test counts: 300/60
All-label token estimate: 300
Expected solver: retrieval_required_no_label_semantics

Why this task exists:
300 opaque IDs L0001...L0300.

Hard slices:
- opaque_label_names
- high_cardinality
- label_name_overlap_failure

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
