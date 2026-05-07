# standard_task2_arbitrary_abcd_non_mcq

Mode: standard
Group: task2_ood_classification
Profile: classification_like
Languages: en
Scripts: Han, Latin
Label language: opaque
Labels: 4
Train/Test counts: 12/20
All-label token estimate: 4
Expected solver: classification_retrieval_llm_verifier

Why this task exists:
A/B/C/D are ordinary class IDs, not options.

Hard slices:
- abcd_non_mcq_negative_control
- router_false_positive
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

A/B/C/D are ordinary class IDs, not MCQ options. Text intentionally has no option markers.
