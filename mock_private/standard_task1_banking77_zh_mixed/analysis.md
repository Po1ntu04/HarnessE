# standard_task1_banking77_zh_mixed

Mode: standard
Group: task1_similar_label
Profile: classification_like
Languages: zh, en, mixed-zh-en
Scripts: Han, Latin
Label language: en
Labels: 8
Train/Test counts: 24/24
All-label token estimate: 24
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
Chinese and mixed Chinese-English Banking77-like texts with original English labels.

Hard slices:
- multilingual_text
- cross_lingual_label
- banking77_like
- unicode_text

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
