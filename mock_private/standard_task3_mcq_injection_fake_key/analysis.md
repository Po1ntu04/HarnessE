# standard_task3_mcq_injection_fake_key

Mode: standard
Group: task3_mcq
Profile: mcq_like
Languages: en, zh, es, ja
Scripts: Han, Latin
Label language: option-label
Labels: 4
Train/Test counts: 12/16
All-label token estimate: 4
Expected solver: mcq_reasoning_verifier

Why this task exists:
MCQ with fake answer keys and multilingual injection.

Hard slices:
- misleading_instruction_inside_text
- multilingual_prompt_injection
- mcq
- answer_distribution_balanced

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
