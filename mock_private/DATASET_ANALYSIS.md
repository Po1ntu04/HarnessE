# mock_private v2 dataset analysis

The v1 suite was closer to a smoke test. v2 targets runtime-schema, routing, injection boundary, budget, and verifier behavior.

## Official mock weighting

- Task 1 similar-label classification: 20%; clean/confusable/injection slice use 0.50/0.35/0.15 internal weights.
- Task 2 OOD classification: 60%; all 14 OOD subtasks are equal-weighted.
- Task 3 MCQ: 20%; all 6 MCQ subtasks are equal-weighted.
- `task_macro_average` and `record_micro_average` are diagnostics, not the primary metric.

| Task | Group | Profile | Labels | Train | Test | Risk tags |
|---|---|---|---:|---:|---:|---|
| `task1_banking77_clean_hard` | `task1_similar_label` | `classification_like` | 24 | 72 | 72 | paraphrase_without_label_keywords, multi_intent_but_primary_clear, negation, temporal_shift |
| `task1_banking77_confusable_pairs` | `task1_similar_label` | `classification_like` | 14 | 42 | 56 | confusable_label_pair, not_x_but_y, temporal_shift, multi_intent_but_primary_clear |
| `task1_banking77_injected_slice` | `task1_similar_label` | `classification_like_with_injection` | 10 | 30 | 30 | direct_override, role_mimic, delimiter_escape, false_label_attack |
| `task2_ood_support_router_hard` | `task2_ood_classification` | `classification_like` | 8 | 24 | 24 | runtime_label_schema, multi_intent_but_primary_clear, service_outage_vs_bug |
| `task2_ood_news_topic_hard` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | short_labels, topic_overlap, non_support_domain |
| `task2_ood_research_sentence_role` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | research_role, method_result_confusion, longer_text |
| `task2_ood_sentiment_nuanced` | `task2_ood_classification` | `classification_like` | 4 | 12 | 20 | sentiment_reversal, mixed_boundary, short_labels |
| `task2_ood_question_type` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | question_type, multiple_entities, short_labels |
| `task2_ood_email_action` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | action_routing, legal_terms_without_label, archive_no_action |
| `task2_ood_software_issue_triage` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | bug_vs_usability, performance_regression, installation_help |
| `task2_ood_product_review_aspect` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | mixed_reviews, aspect_focus, return_vs_service |
| `task2_ood_policy_clause_type` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | legal_language, keyword_variation, clause_type |
| `task2_ood_long_text_topic` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | long_text_with_distractors, budget_pressure, topic_primary |
| `task2_ood_arbitrary_abcd_labels` | `task2_ood_classification` | `classification_like` | 4 | 12 | 20 | abcd_non_mcq_negative_control, opaque_label_names, router_false_positive |
| `task2_ood_opaque_label_mapping` | `task2_ood_classification` | `classification_like` | 5 | 20 | 20 | opaque_label_names, label_name_overlap_failure, runtime_examples_required |
| `task2_ood_event_intent` | `task2_ood_classification` | `classification_like` | 6 | 18 | 18 | event_domain, multi_intent, label_semantics |
| `task2_ood_customer_review_stance` | `task2_ood_classification` | `classification_like` | 5 | 15 | 20 | stance_not_sentiment, off_topic, request_more_info |
| `task3_mcq_science_fact` | `task3_mcq` | `mcq_like` | 4 | 12 | 20 | option_format_variation, plausible_distractors, answer_distribution_balanced |
| `task3_mcq_commonsense_reasoning` | `task3_mcq` | `mcq_like` | 4 | 12 | 20 | multi_step_reasoning, plausible_distractors, answer_distribution_balanced |
| `task3_mcq_math_word_problem` | `task3_mcq` | `mcq_like` | 4 | 12 | 20 | multi_step_reasoning, math_word_problem, answer_distribution_balanced |
| `task3_mcq_reading_comprehension` | `task3_mcq` | `mcq_like` | 4 | 12 | 20 | passage_based, budget_pressure, plausible_distractors |
| `task3_mcq_logic_constraints` | `task3_mcq` | `mcq_like` | 4 | 12 | 20 | logic_constraints, multi_step_reasoning, answer_distribution_balanced |
| `task3_mcq_injection_and_decoy` | `task3_mcq` | `mcq_like` | 4 | 12 | 20 | misleading_instruction_inside_text, option_format_variation, answer_distribution_balanced |

## Expected failure modes

1. Banking77 hardcoding fails on task2/task3.
2. Label-name-only methods fail on opaque label tasks.
3. Routers that treat A/B/C/D as sufficient MCQ evidence fail on `task2_ood_arbitrary_abcd_labels`.
4. Missing injection boundaries fail on task1 and task3 injection slices.
5. Traditional classifiers without reasoning fail on MCQ tasks.
6. Weak budget management fails on long-text and reading-comprehension tasks.
