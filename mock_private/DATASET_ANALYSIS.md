# mock_private v3 dataset analysis

v3 adds multilingual, cross-lingual, science-domain, Unicode exact-match, high-cardinality, and multilingual prompt-injection pressure.

## Task table

| Task | Mode | Group | Languages | Scripts | Labels | Train | Test | Token est | Risk tags |
|---|---|---|---|---|---:|---:|---:|---:|---|
| `standard_task1_banking77_en` | standard | task1_similar_label | en | Latin | 12 | 36 | 36 | 38 | similar_label, banking77_like, paraphrase_without_label_keywords |
| `standard_task1_banking77_zh_mixed` | standard | task1_similar_label | zh, en, mixed-zh-en | Han, Latin | 8 | 24 | 24 | 24 | multilingual_text, cross_lingual_label, banking77_like, unicode_text |
| `standard_task1_banking77_confusable_pairs` | standard | task1_similar_label | en, zh, mixed-zh-en | Han, Latin | 10 | 30 | 30 | 31 | confusable_label_pair, temporal_shift, not_x_but_y, multilingual_text |
| `standard_task1_banking77_multilingual_injection` | standard | task1_similar_label | en, zh, es, fr, ja, mixed | Han, Kana, Latin | 8 | 24 | 19 | 24 | multilingual_prompt_injection, direct_override, role_mimic, json_format_attack |
| `standard_task2_zh_customer_support` | standard | task2_ood_classification | zh | Han, Latin | 6 | 18 | 18 | 24 | zh_support, non_banking, runtime_label_schema, ood_classification |
| `standard_task2_en_saas_router` | standard | task2_ood_classification | en | Han, Latin | 6 | 18 | 18 | 12 | en_saas, service_outage_vs_bug, ood_classification |
| `standard_task2_multilingual_assistant_intent` | standard | task2_ood_classification | en, zh, es, fr, ja | Han, Kana, Latin | 5 | 15 | 20 | 5 | multilingual_text, assistant_intent, ood_classification |
| `standard_task2_crosslingual_news_topic` | standard | task2_ood_classification | en, zh, es, fr, ja | Han, Kana, Latin | 6 | 18 | 18 | 12 | cross_lingual_news, topic_overlap, ood_classification |
| `standard_task2_science_sentence_role` | standard | task2_ood_classification | en, zh | Han, Latin | 6 | 18 | 18 | 7 | science_domain, research_role, method_result_confusion, ood_classification |
| `standard_task2_citation_intent_style` | standard | task2_ood_classification | en | Han, Latin | 5 | 15 | 20 | 11 | science_domain, citation_intent, ood_classification |
| `standard_task2_lab_safety` | standard | task2_ood_classification | en, zh | Han, Latin | 5 | 15 | 20 | 10 | science_domain, lab_safety, unicode_text, ood_classification |
| `standard_task2_policy_clause_type` | standard | task2_ood_classification | en, zh | Han, Latin | 6 | 18 | 18 | 6 | policy_clause, keyword_variation, ood_classification |
| `standard_task2_software_issue_triage` | standard | task2_ood_classification | en | Han, Latin | 6 | 18 | 18 | 11 | software_issue, bug_vs_usability, ood_classification |
| `standard_task2_email_action` | standard | task2_ood_classification | en | Han, Latin | 6 | 18 | 18 | 15 | email_action, legal_terms_without_label, ood_classification |
| `standard_task2_product_review_aspect` | standard | task2_ood_classification | en, zh | Han, Latin | 6 | 18 | 18 | 11 | product_aspect, mixed_reviews, ood_classification |
| `standard_task2_sentiment_nuanced` | standard | task2_ood_classification | en, zh | Han, Latin | 4 | 12 | 20 | 4 | sentiment_reversal, short_labels, ood_classification |
| `standard_task2_question_type` | standard | task2_ood_classification | en, zh | Han, Latin | 6 | 18 | 18 | 6 | question_type, multiple_entities, ood_classification |
| `standard_task2_arbitrary_abcd_non_mcq` | standard | task2_ood_classification | en | Han, Latin | 4 | 12 | 20 | 4 | abcd_non_mcq_negative_control, router_false_positive, ood_classification |
| `standard_task2_opaque_label_mapping` | standard | task2_ood_classification | en | Han, Latin | 5 | 15 | 20 | 5 | opaque_label_names, label_name_overlap_failure, ood_classification |
| `standard_task2_unicode_label_exact_match` | standard | task2_ood_classification | en, zh, fr, ja, es | Greek, Han, Kana, Latin | 5 | 15 | 20 | 17 | unicode_label, unicode_exact_match, diacritics, ood_classification |
| `standard_task2_structured_text` | standard | task2_ood_classification | en | Han, Latin | 5 | 15 | 20 | 9 | structured_text, format_variation, ood_classification |
| `standard_task2_long_text_topic` | standard | task2_ood_classification | en, zh, es | Han, Latin | 6 | 18 | 18 | 7 | long_text_with_distractors, budget_pressure, ood_classification |
| `standard_task3_mcq_science_en` | standard | task3_mcq | en | Latin | 4 | 12 | 16 | 4 | science_domain, option_format_variation, mcq, answer_distribution_balanced |
| `standard_task3_mcq_science_zh` | standard | task3_mcq | zh | Han, Latin | 4 | 12 | 16 | 4 | science_domain, chinese_text, mcq, answer_distribution_balanced |
| `standard_task3_mcq_bilingual_science_terms` | standard | task3_mcq | en, zh, mixed-zh-en | Han, Latin | 4 | 12 | 16 | 4 | science_domain, cross_lingual_terms, mcq, answer_distribution_balanced |
| `standard_task3_mcq_multilingual_commonsense` | standard | task3_mcq | en, zh, es, fr | Han, Latin | 4 | 12 | 16 | 4 | multilingual_text, commonsense_reasoning, mcq, answer_distribution_balanced |
| `standard_task3_mcq_math_zh_en` | standard | task3_mcq | en, zh | Han, Latin | 4 | 12 | 16 | 4 | math_word_problem, multilingual_text, mcq, answer_distribution_balanced |
| `standard_task3_mcq_multilingual_reading` | standard | task3_mcq | en, zh, es | Han, Latin | 4 | 12 | 16 | 4 | passage_based, multilingual_text, budget_pressure, mcq |
| `standard_task3_mcq_logic_constraints` | standard | task3_mcq | en, zh | Han, Latin | 4 | 12 | 16 | 4 | logic_constraints, multi_step_reasoning, mcq, answer_distribution_balanced |
| `standard_task3_mcq_injection_fake_key` | standard | task3_mcq | en, zh, es, ja | Han, Latin | 4 | 12 | 16 | 4 | misleading_instruction_inside_text, multilingual_prompt_injection, mcq, answer_distribution_balanced |
| `stress_task2_high_cardinality_long_labels` | stress | task2_ood_classification | en | Latin | 120 | 120 | 48 | 2280 | high_cardinality, all_labels_token_pressure, science_domain |
| `stress_task2_opaque_ids_300` | stress | task2_ood_classification | en | Latin | 300 | 300 | 60 | 300 | opaque_label_names, high_cardinality, label_name_overlap_failure |
| `stress_task2_multilingual_small_language` | stress | task2_ood_classification | sw, ka, he, hi, th, el, am, ar | Devanagari, Ethiopic, Georgian, Greek, Hebrew, Latin, Thai | 4 | 12 | 12 | 4 | low_resource_language, non_latin_scripts, multilingual_text |
| `stress_task2_label_language_mismatch` | stress | task2_ood_classification | en, zh, fr, ar, es, ja | Arabic, Han, Latin | 4 | 12 | 12 | 12 | label_language_mismatch, unicode_label, cross_lingual_label |
| `stress_task2_hierarchical_prefix_collision` | stress | task2_ood_classification | en | Latin | 5 | 15 | 20 | 19 | hierarchical_prefix_collision, science_domain, label_name_overlap_trap |
| `stress_task1_multilingual_injection_flood` | stress | task1_similar_label | en, zh, es, fr, ja, ar | Arabic, Han, Kana, Latin | 4 | 12 | 16 | 9 | multilingual_prompt_injection, injection_flood, direct_override |
| `stress_task3_fullwidth_option_labels` | stress | task3_mcq | zh, en | Fullwidth, Han, Latin | 4 | 12 | 16 | 4 | full_width_option_labels, unicode_label, mcq |
| `stress_task3_chinese_option_labels` | stress | task3_mcq | zh, en | Han, Latin | 4 | 12 | 16 | 4 | chinese_option_labels, unicode_label, mcq |
| `stress_task3_long_science_passage_fake_instruction` | stress | task3_mcq | en | Latin | 4 | 12 | 16 | 4 | science_domain, long_science_passage, misleading_instruction_inside_text |
