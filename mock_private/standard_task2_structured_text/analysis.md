# standard_task2_structured_text

Mode: standard
Group: task2_ood_classification
Profile: classification_like
Languages: en
Scripts: Han, Latin
Label language: en
Labels: 5
Train/Test counts: 15/20
All-label token estimate: 9
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
Structured key-value text classification.

Hard slices:
- structured_text
- format_variation
- ood_classification

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
