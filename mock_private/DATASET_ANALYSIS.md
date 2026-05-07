# mock_private dataset analysis

| Task | Family | Expected profile | Labels | Train | Test | Main stress |
|---|---|---|---:|---:|---:|---|
| `banking77_same_labels` | `banking_same` | `classification_like` | 8 | 24 | 18 | near-label ambiguity, short customer utterances |
| `banking77_injected` | `prompt_injection` | `classification_like_with_injection` | 6 | 12 | 12 | quoted-data boundary, label mention attack |
| `ood_support_router` | `ood_classification` | `classification_like` | 6 | 18 | 12 | OOD label inventory, support-domain overlap |
| `news_topic_ood` | `ood_classification` | `classification_like` | 4 | 12 | 8 | short labels, topic classification |
| `research_intent_ood` | `ood_classification` | `classification_like` | 5 | 15 | 10 | longer abstract-like text, labels are semantic but not customer support intents |
| `short_label_sentiment` | `ood_classification` | `classification_like` | 4 | 12 | 8 | short labels, label-name reliance |
| `mcq_science` | `mcq` | `mcq_like` | 4 | 8 | 8 | A/B/C/D short labels, option reasoning |
| `mcq_reasoning_injected` | `mcq` | `mcq_like_with_injection` | 4 | 8 | 8 | MCQ routing under instruction-like text, answer cue parsing |

## Recommended averaging

- Primary: family macro average, because hidden private weights are unknown.
- Secondary: task macro average, useful for debugging individual task failures.
- Do not use record-level micro average as the main score; it lets larger tasks dominate.

## What this suite is designed to catch

- Banking-only hardcoding.
- Missing prompt-injection boundary.
- Router mistakes between MCQ and normal classification.
- Illegal label outputs and weak parser behavior.
- Retrieval that fails to preserve label diversity.
