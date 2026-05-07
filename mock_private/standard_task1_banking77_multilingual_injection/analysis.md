# standard_task1_banking77_multilingual_injection

Mode: standard
Group: task1_similar_label
Profile: classification_like_with_injection
Languages: en, zh, es, fr, ja, mixed
Scripts: Han, Kana, Latin
Label language: en
Labels: 8
Train/Test counts: 24/19
All-label token estimate: 24
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
Multilingual prompt injection inside Banking77-like classification data.

Hard slices:
- multilingual_prompt_injection
- direct_override
- role_mimic
- json_format_attack
- benign_injection_keyword_control

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
