# mock_private v2

This is a local HarnessE private-test simulation stress suite. It preserves the official interface:

```json
{"text": "...", "label": "..."}
```

Each top-level task directory contains `train.jsonl`, `test.jsonl`, and `analysis.md`.
The final submitted `solution.py` must not read or depend on this directory.

## Official mock weighting

task1_score = 0.50 * task1_banking77_clean_hard
            + 0.35 * task1_banking77_confusable_pairs
            + 0.15 * task1_banking77_injected_slice

task2_score = mean(all task2_ood_* subtask accuracies)

task3_score = mean(all task3_mcq_* subtask accuracies)

official_mock_score = 0.20 * task1_score
                    + 0.60 * task2_score
                    + 0.20 * task3_score

Prompt injection is a slice inside task 1, not an independent main family.
Task 2 is the main pressure source: 14 OOD subtasks, equal-weighted.
Task 3 contains 6 MCQ subtasks, equal-weighted.

## Task groups

- Task 1 similar-label Banking-style tasks: 3 subtasks.
- Task 2 OOD closed-set classification: 14 subtasks.
- Task 3 MCQ natural-language choice tasks: 6 subtasks.

## Run

```powershell
python scripts/generate_mock_private_v2.py
python scripts/audit_mock_private.py mock_private
python scripts/score_mock_results.py mock_private predictions.jsonl
```

## Expected failure modes

- Banking77 hardcoding fails on task2 and task3.
- Label-name-only methods fail on opaque label tasks.
- Routers that treat every A/B/C/D label set as MCQ fail on `task2_ood_arbitrary_abcd_labels`.
- Missing prompt-injection boundaries fail on `task1_banking77_injected_slice` and `task3_mcq_injection_and_decoy`.
- Traditional classifiers without reasoning fail on MCQ.
- Weak budget handling fails on long text and reading-comprehension tasks.

## Tasks

- `task1_banking77_clean_hard`: task1_similar_label, 24 labels, 72 train / 72 test.
- `task1_banking77_confusable_pairs`: task1_similar_label, 14 labels, 42 train / 56 test.
- `task1_banking77_injected_slice`: task1_similar_label, 10 labels, 30 train / 30 test.
- `task2_ood_support_router_hard`: task2_ood_classification, 8 labels, 24 train / 24 test.
- `task2_ood_news_topic_hard`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_research_sentence_role`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_sentiment_nuanced`: task2_ood_classification, 4 labels, 12 train / 20 test.
- `task2_ood_question_type`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_email_action`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_software_issue_triage`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_product_review_aspect`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_policy_clause_type`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_long_text_topic`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_arbitrary_abcd_labels`: task2_ood_classification, 4 labels, 12 train / 20 test.
- `task2_ood_opaque_label_mapping`: task2_ood_classification, 5 labels, 20 train / 20 test.
- `task2_ood_event_intent`: task2_ood_classification, 6 labels, 18 train / 18 test.
- `task2_ood_customer_review_stance`: task2_ood_classification, 5 labels, 15 train / 20 test.
- `task3_mcq_science_fact`: task3_mcq, 4 labels, 12 train / 20 test.
- `task3_mcq_commonsense_reasoning`: task3_mcq, 4 labels, 12 train / 20 test.
- `task3_mcq_math_word_problem`: task3_mcq, 4 labels, 12 train / 20 test.
- `task3_mcq_reading_comprehension`: task3_mcq, 4 labels, 12 train / 20 test.
- `task3_mcq_logic_constraints`: task3_mcq, 4 labels, 12 train / 20 test.
- `task3_mcq_injection_and_decoy`: task3_mcq, 4 labels, 12 train / 20 test.
