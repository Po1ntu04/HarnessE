# standard_task1_banking77_en

Mode: standard
Group: task1_similar_label
Profile: classification_like
Languages: en
Scripts: Latin
Label language: en
Labels: 12
Train/Test counts: 36/36
All-label token estimate: 38
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
English Banking77-like same-label classification with hard paraphrases.

Hard slices:
- similar_label
- banking77_like
- paraphrase_without_label_keywords

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
