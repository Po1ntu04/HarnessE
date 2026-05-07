# mock_private v2 数据集分析

旧版压力集更接近 smoke test：任务少、样本少、标签语义过于直接、MCQ 格式过于标准。v2 的目标不是故意压低分数，而是暴露错误的 harness 假设。

## 官方 mock 权重

- Task 1 同标签分类：20%，其中 clean/confusable/injection slice 按 0.50/0.35/0.15 加权。
- Task 2 OOD 分类：60%，14 个 OOD 子任务内部等权。
- Task 3 MCQ：20%，6 个 MCQ 子任务内部等权。
- `task_macro_average` 和 `record_micro_average` 只用于辅助诊断，不是主分。

## v2 hard slices

- `paraphrase_without_label_keywords`
- `confusable_label_pair`
- `negation` / `temporal_shift`
- `multi_intent_but_primary_clear`
- `long_text_with_distractors`
- `opaque_label_names`
- `abcd_non_mcq_negative_control`
- `misleading_instruction_inside_text`
- `answer_distribution_balanced`

## 任务表

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

1. Banking77 hardcode 会在 task2/task3 崩。
2. 只看 label name 会在 opaque label 任务崩。
3. 看到 A/B/C/D 就走 MCQ 会在 `task2_ood_arbitrary_abcd_labels` 崩。
4. 不做 injection boundary 会在 task1 injection 和 task3 injection 崩。
5. 只做 traditional classifier 会在 MCQ 崩。
6. 不做 budget 管理会在 long_text 和 reading_comprehension 崩。
