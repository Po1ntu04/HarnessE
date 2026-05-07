# Mock Private v2 Audit

Dataset root: `mock_private`
Manifest version: `mock_private_v2`
Task count: 23
Group counts: task1=3, task2=14, task3=6

Official mock score:

```text
task1_score = 0.50 * task1_banking77_clean_hard + 0.35 * task1_banking77_confusable_pairs + 0.15 * task1_banking77_injected_slice
task2_score = mean(all task2_ood_* subtask accuracies)
task3_score = mean(all task3_mcq_* subtask accuracies)
official_mock_score = 0.20 * task1_score + 0.60 * task2_score + 0.20 * task3_score
```

## Per Task Checks

| Task | Group | Train | Test | Labels | Train min/max | Test min/max | Overlap | Empty | Option markers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `task1_banking77_clean_hard` | task1 | 72 | 72 | 24 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task1_banking77_confusable_pairs` | task1 | 42 | 56 | 14 | 3/3 | 4/4 | 0 | 0 | 0 |
| `task1_banking77_injected_slice` | task1 | 30 | 30 | 10 | 3/3 | 2/4 | 0 | 0 | 0 |
| `task2_ood_support_router_hard` | task2 | 24 | 24 | 8 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_news_topic_hard` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_research_sentence_role` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_sentiment_nuanced` | task2 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 0 |
| `task2_ood_question_type` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_email_action` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_software_issue_triage` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_product_review_aspect` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_policy_clause_type` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_long_text_topic` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_arbitrary_abcd_labels` | task2 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 0 |
| `task2_ood_opaque_label_mapping` | task2 | 20 | 20 | 5 | 4/4 | 4/4 | 0 | 0 | 0 |
| `task2_ood_event_intent` | task2 | 18 | 18 | 6 | 3/3 | 3/3 | 0 | 0 | 0 |
| `task2_ood_customer_review_stance` | task2 | 15 | 20 | 5 | 3/3 | 4/4 | 0 | 0 | 0 |
| `task3_mcq_science_fact` | task3 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 32 |
| `task3_mcq_commonsense_reasoning` | task3 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 32 |
| `task3_mcq_math_word_problem` | task3 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 32 |
| `task3_mcq_reading_comprehension` | task3 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 32 |
| `task3_mcq_logic_constraints` | task3 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 32 |
| `task3_mcq_injection_and_decoy` | task3 | 12 | 20 | 4 | 3/3 | 5/5 | 0 | 0 | 32 |

## Special Checks

- task1 injection-like test ratio: 24/30 = 80.0%
- `task2_ood_arbitrary_abcd_labels`: A/B/C/D are ordinary class IDs and option markers must be 0.
- MCQ tasks: labels must be exactly A/B/C/D and every record must contain an option structure.

## Long Text Stats

| Task | Test min words | Test median words | Test max words | Test min chars | Test median chars | Test max chars |
|---|---:|---:|---:|---:|---:|---:|
| `task2_ood_long_text_topic` | 41 | 46 | 52 | 278 | 320 | 359 |
| `task3_mcq_reading_comprehension` | 88 | 94 | 98 | 577 | 602 | 611 |

## PASS/FAIL

PASS
