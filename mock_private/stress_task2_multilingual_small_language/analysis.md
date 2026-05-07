# stress_task2_multilingual_small_language

Mode: stress
Group: task2_ood_classification
Profile: classification_like
Languages: sw, ka, he, hi, th, el, am, ar
Scripts: Devanagari, Ethiopic, Georgian, Greek, Hebrew, Latin, Thai
Label language: en
Labels: 4
Train/Test counts: 12/12
All-label token estimate: 4
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
Small-language and non-Latin script classification.

Hard slices:
- low_resource_language
- non_latin_scripts
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
