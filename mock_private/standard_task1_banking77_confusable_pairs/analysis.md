# standard_task1_banking77_confusable_pairs

Mode: standard
Group: task1_similar_label
Profile: classification_like
Languages: en, zh, mixed-zh-en
Scripts: Han, Latin
Label language: en
Labels: 10
Train/Test counts: 30/30
All-label token estimate: 31
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
Confusable Banking77-like pairs across English and Chinese phrasing.

Hard slices:
- confusable_label_pair
- temporal_shift
- not_x_but_y
- multilingual_text

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
