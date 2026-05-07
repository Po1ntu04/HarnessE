# stress_task1_multilingual_injection_flood

Mode: stress
Group: task1_similar_label
Profile: classification_like_with_injection
Languages: en, zh, es, fr, ja, ar
Scripts: Arabic, Han, Kana, Latin
Label language: en
Labels: 4
Train/Test counts: 12/16
All-label token estimate: 9
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
Dense multilingual prompt-injection flood.

Hard slices:
- multilingual_prompt_injection
- injection_flood
- direct_override

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
