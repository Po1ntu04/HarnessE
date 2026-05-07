# Mock Private v3 Audit

Dataset root: `mock_private`
Manifest version: `mock_private_v3`
Task count: 39
Mode counts: {'standard': 30, 'stress': 9}
Standard group counts: {'task1_similar_label': 4, 'task2_ood_classification': 18, 'task3_mcq': 8}

Official proxy scoring for standard mode:

```text
task1_score = mean(standard task1_similar_label subtask accuracies)
task2_score = mean(standard task2_ood_classification subtask accuracies)
task3_score = mean(standard task3_mcq subtask accuracies)
standard_official_mock_score = 0.20 * task1_score + 0.60 * task2_score + 0.20 * task3_score
```

## Coverage Checks

- Standard languages: en, es, fr, ja, mixed, mixed-zh-en, zh
- Stress languages: am, ar, el, en, es, fr, he, hi, ja, ka, sw, th, zh
- Standard scripts: Greek, Han, Kana, Latin
- Stress scripts: Arabic, Devanagari, Ethiopic, Fullwidth, Georgian, Greek, Han, Hebrew, Kana, Latin, Thai
- Science-domain tasks: 9
- Unicode label count: 22
- High-cardinality token-pressure tasks: stress_task2_high_cardinality_long_labels
- Multilingual injection languages: ar, en, es, fr, ja, mixed, zh
- A/B/C/D non-MCQ negative control: PASS
- Full-width MCQ labels: PASS
- Chinese MCQ labels: PASS

## Per Task Checks

| Task | Mode | Group | Languages | Scripts | Labels | Train | Test | Train min/max | Test min/max | Label token est | Overlap | Option markers |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `standard_task1_banking77_en` | standard | task1_similar_label | en | Latin | 12 | 36 | 36 | 3/3 | 3/3 | 38 | 0 | 0 |
| `standard_task1_banking77_zh_mixed` | standard | task1_similar_label | zh,en,mixed-zh-en | Han,Latin | 8 | 24 | 24 | 3/3 | 3/3 | 24 | 0 | 0 |
| `standard_task1_banking77_confusable_pairs` | standard | task1_similar_label | en,zh,mixed-zh-en | Han,Latin | 10 | 30 | 30 | 3/3 | 3/3 | 31 | 0 | 0 |
| `standard_task1_banking77_multilingual_injection` | standard | task1_similar_label | en,zh,es,fr,ja,mixed | Han,Kana,Latin | 8 | 24 | 19 | 3/3 | 2/3 | 24 | 0 | 0 |
| `standard_task2_zh_customer_support` | standard | task2_ood_classification | zh | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 24 | 0 | 0 |
| `standard_task2_en_saas_router` | standard | task2_ood_classification | en | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 12 | 0 | 0 |
| `standard_task2_multilingual_assistant_intent` | standard | task2_ood_classification | en,zh,es,fr,ja | Han,Kana,Latin | 5 | 15 | 20 | 3/3 | 4/4 | 5 | 0 | 0 |
| `standard_task2_crosslingual_news_topic` | standard | task2_ood_classification | en,zh,es,fr,ja | Han,Kana,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 12 | 0 | 0 |
| `standard_task2_science_sentence_role` | standard | task2_ood_classification | en,zh | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 7 | 0 | 0 |
| `standard_task2_citation_intent_style` | standard | task2_ood_classification | en | Han,Latin | 5 | 15 | 20 | 3/3 | 4/4 | 11 | 0 | 0 |
| `standard_task2_lab_safety` | standard | task2_ood_classification | en,zh | Han,Latin | 5 | 15 | 20 | 3/3 | 4/4 | 10 | 0 | 0 |
| `standard_task2_policy_clause_type` | standard | task2_ood_classification | en,zh | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 6 | 0 | 0 |
| `standard_task2_software_issue_triage` | standard | task2_ood_classification | en | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 11 | 0 | 0 |
| `standard_task2_email_action` | standard | task2_ood_classification | en | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 15 | 0 | 0 |
| `standard_task2_product_review_aspect` | standard | task2_ood_classification | en,zh | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 11 | 0 | 0 |
| `standard_task2_sentiment_nuanced` | standard | task2_ood_classification | en,zh | Han,Latin | 4 | 12 | 20 | 3/3 | 5/5 | 4 | 0 | 0 |
| `standard_task2_question_type` | standard | task2_ood_classification | en,zh | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 6 | 0 | 0 |
| `standard_task2_arbitrary_abcd_non_mcq` | standard | task2_ood_classification | en | Han,Latin | 4 | 12 | 20 | 3/3 | 5/5 | 4 | 0 | 0 |
| `standard_task2_opaque_label_mapping` | standard | task2_ood_classification | en | Han,Latin | 5 | 15 | 20 | 3/3 | 4/4 | 5 | 0 | 0 |
| `standard_task2_unicode_label_exact_match` | standard | task2_ood_classification | en,zh,fr,ja,es | Greek,Han,Kana,Latin | 5 | 15 | 20 | 3/3 | 4/4 | 17 | 0 | 0 |
| `standard_task2_structured_text` | standard | task2_ood_classification | en | Han,Latin | 5 | 15 | 20 | 3/3 | 4/4 | 9 | 0 | 0 |
| `standard_task2_long_text_topic` | standard | task2_ood_classification | en,zh,es | Han,Latin | 6 | 18 | 18 | 3/3 | 3/3 | 7 | 0 | 0 |
| `standard_task3_mcq_science_en` | standard | task3_mcq | en | Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `standard_task3_mcq_science_zh` | standard | task3_mcq | zh | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `standard_task3_mcq_bilingual_science_terms` | standard | task3_mcq | en,zh,mixed-zh-en | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `standard_task3_mcq_multilingual_commonsense` | standard | task3_mcq | en,zh,es,fr | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `standard_task3_mcq_math_zh_en` | standard | task3_mcq | en,zh | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `standard_task3_mcq_multilingual_reading` | standard | task3_mcq | en,zh,es | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `standard_task3_mcq_logic_constraints` | standard | task3_mcq | en,zh | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `standard_task3_mcq_injection_fake_key` | standard | task3_mcq | en,zh,es,ja | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `stress_task2_high_cardinality_long_labels` | stress | task2_ood_classification | en | Latin | 120 | 120 | 48 | 1/1 | 0/1 | 2280 | 0 | 0 |
| `stress_task2_opaque_ids_300` | stress | task2_ood_classification | en | Latin | 300 | 300 | 60 | 1/1 | 0/1 | 300 | 0 | 0 |
| `stress_task2_multilingual_small_language` | stress | task2_ood_classification | sw,ka,he,hi,th,el,am,ar | Devanagari,Ethiopic,Georgian,Greek,Hebrew,Latin,Thai | 4 | 12 | 12 | 3/3 | 3/3 | 4 | 0 | 0 |
| `stress_task2_label_language_mismatch` | stress | task2_ood_classification | en,zh,fr,ar,es,ja | Arabic,Han,Latin | 4 | 12 | 12 | 3/3 | 3/3 | 12 | 0 | 0 |
| `stress_task2_hierarchical_prefix_collision` | stress | task2_ood_classification | en | Latin | 5 | 15 | 20 | 3/3 | 4/4 | 19 | 0 | 0 |
| `stress_task1_multilingual_injection_flood` | stress | task1_similar_label | en,zh,es,fr,ja,ar | Arabic,Han,Kana,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 9 | 0 | 0 |
| `stress_task3_fullwidth_option_labels` | stress | task3_mcq | zh,en | Fullwidth,Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `stress_task3_chinese_option_labels` | stress | task3_mcq | zh,en | Han,Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |
| `stress_task3_long_science_passage_fake_instruction` | stress | task3_mcq | en | Latin | 4 | 12 | 16 | 3/3 | 4/4 | 4 | 0 | 28 |

## Long Text Stats

| Task | Min words | Median words | Max words | Min chars | Median chars | Max chars |
|---|---:|---:|---:|---:|---:|---:|
| `standard_task2_long_text_topic` | 33 | 53 | 66 | 244 | 339 | 440 |
| `stress_task3_long_science_passage_fake_instruction` | 62 | 73 | 98 | 421 | 458 | 617 |

## PASS/FAIL

PASS
