# mock_private v3

v3 is a dual-mode HarnessE private-test simulation suite.

- `standard_*` tasks are the official-proxy multilingual set and use the 20/60/20 primary score.
- `stress_*` tasks are adversarial diagnostics for high-cardinality, low-resource languages, Unicode labels, non-ASCII MCQ options, and multilingual prompt injection.

Every task still uses only `train.jsonl` and `test.jsonl`. Every record is exactly:

```json
{"text": "...", "label": "..."}
```

Do not make `solution.py` read or depend on `mock_private`.

## Core v3 assumptions

1. Text is not guaranteed to be English.
2. Labels are not guaranteed to be English.
3. All-label prompts do not scale to high-cardinality or long-label tasks.
4. Prompt injection is not guaranteed to be English.
5. MCQ option labels are not guaranteed to be ASCII A/B/C/D.
6. Science OOD may be text classification, not only MCQ.
7. The verifier must preserve original Unicode labels for exact match.
8. Task 2 OOD is 60%, so multilingual/OOD generalization is the main design goal.

## Scoring

```text
standard_official_mock_score = 0.20 * task1_score + 0.60 * task2_score + 0.20 * task3_score
```

Task scores are equal-subtask macro averages within standard mode. Stress mode is reported separately.

## Run

```powershell
python scripts/generate_mock_private_v3.py
python scripts/audit_mock_private.py mock_private
python scripts/score_mock_results.py mock_private predictions.jsonl
```

Standard tasks: 30. Stress tasks: 9. Total tasks: 39.

## Task list

- `standard_task1_banking77_en`: standard / task1_similar_label, 12 labels, 36 train / 36 test.
- `standard_task1_banking77_zh_mixed`: standard / task1_similar_label, 8 labels, 24 train / 24 test.
- `standard_task1_banking77_confusable_pairs`: standard / task1_similar_label, 10 labels, 30 train / 30 test.
- `standard_task1_banking77_multilingual_injection`: standard / task1_similar_label, 8 labels, 24 train / 19 test.
- `standard_task2_zh_customer_support`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_en_saas_router`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_multilingual_assistant_intent`: standard / task2_ood_classification, 5 labels, 15 train / 20 test.
- `standard_task2_crosslingual_news_topic`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_science_sentence_role`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_citation_intent_style`: standard / task2_ood_classification, 5 labels, 15 train / 20 test.
- `standard_task2_lab_safety`: standard / task2_ood_classification, 5 labels, 15 train / 20 test.
- `standard_task2_policy_clause_type`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_software_issue_triage`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_email_action`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_product_review_aspect`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_sentiment_nuanced`: standard / task2_ood_classification, 4 labels, 12 train / 20 test.
- `standard_task2_question_type`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task2_arbitrary_abcd_non_mcq`: standard / task2_ood_classification, 4 labels, 12 train / 20 test.
- `standard_task2_opaque_label_mapping`: standard / task2_ood_classification, 5 labels, 15 train / 20 test.
- `standard_task2_unicode_label_exact_match`: standard / task2_ood_classification, 5 labels, 15 train / 20 test.
- `standard_task2_structured_text`: standard / task2_ood_classification, 5 labels, 15 train / 20 test.
- `standard_task2_long_text_topic`: standard / task2_ood_classification, 6 labels, 18 train / 18 test.
- `standard_task3_mcq_science_en`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `standard_task3_mcq_science_zh`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `standard_task3_mcq_bilingual_science_terms`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `standard_task3_mcq_multilingual_commonsense`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `standard_task3_mcq_math_zh_en`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `standard_task3_mcq_multilingual_reading`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `standard_task3_mcq_logic_constraints`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `standard_task3_mcq_injection_fake_key`: standard / task3_mcq, 4 labels, 12 train / 16 test.
- `stress_task2_high_cardinality_long_labels`: stress / task2_ood_classification, 120 labels, 120 train / 48 test.
- `stress_task2_opaque_ids_300`: stress / task2_ood_classification, 300 labels, 300 train / 60 test.
- `stress_task2_multilingual_small_language`: stress / task2_ood_classification, 4 labels, 12 train / 12 test.
- `stress_task2_label_language_mismatch`: stress / task2_ood_classification, 4 labels, 12 train / 12 test.
- `stress_task2_hierarchical_prefix_collision`: stress / task2_ood_classification, 5 labels, 15 train / 20 test.
- `stress_task1_multilingual_injection_flood`: stress / task1_similar_label, 4 labels, 12 train / 16 test.
- `stress_task3_fullwidth_option_labels`: stress / task3_mcq, 4 labels, 12 train / 16 test.
- `stress_task3_chinese_option_labels`: stress / task3_mcq, 4 labels, 12 train / 16 test.
- `stress_task3_long_science_passage_fake_instruction`: stress / task3_mcq, 4 labels, 12 train / 16 test.
