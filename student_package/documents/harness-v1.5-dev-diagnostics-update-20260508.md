# HarnessE v1.5 DEV diagnostics update — 2026-05-08

## 1. Purpose

This update answers a late critical review question: whether the previous long-run work had diagnosed DEV failures deeply enough, and why the harness can score very high on `mock_private` while remaining around 78% on public DEV.

The answer is: the earlier v1.4 result was architecturally reasonable but the DEV failure analysis was incomplete. The missing evidence was per-example rank/route diagnostics. After adding those diagnostics, the main DEV bottleneck is no longer “can the harness recall the right label at all”, but “can Qwen3-8B-Instruct choose the right label from a dense set of semantically adjacent candidates under a bounded prompt”.

## 2. Reproducibility artifacts

| Artifact | Path |
|---|---|
| DEV diagnostic tool | `.omx/experiments/tools/run_dev_diagnostics.py` |
| v1.4 diagnostic summary | `.omx/experiments/results/v1.4-devdiag-9364e34d-w4-20260508-1005.summary.json` |
| v1.4 diagnostic predictions | `.omx/experiments/results/v1.4-devdiag-9364e34d-w4-20260508-1005.predictions.jsonl` |
| v1.5 final snapshot | `.omx/experiments/snapshots/solution-v1.5-final-87c3dde5.py` |
| v1.5 final diff | `.omx/experiments/diffs/v1.5-final-from-v1.4-9364e34d.diff` |
| v1.5 DEV diagnostic summary | `.omx/experiments/results/v1.5-exp-many16-87c3dde5-devdiag-w4-20260508-1007.summary.json` |
| v1.5 DEV diagnostic predictions | `.omx/experiments/results/v1.5-exp-many16-87c3dde5-devdiag-w4-20260508-1007.predictions.jsonl` |
| v1.5 public DEV log | `.omx/experiments/reports/v1.5-exp-many16-87c3dde5-public-dev-w4-r1-20260508-1009.log` |
| v1.5 mock v3 summary | `.omx/experiments/results/v1.5-exp-many16-87c3dde5-v3-all-w4-20260508-1008.summary.json` |
| v1.6 top20 ablation | `.omx/experiments/results/v1.6-exp-many20-f8ad34b1-devdiag-w4-20260508-1012.summary.json` |
| v1.7 top12 ablation | `.omx/experiments/results/v1.7-exp-many12-devdiag-w4-20260508-1014.summary.json` |

Current adopted code:

```text
student_package/solution.py
sha256 = 87c3dde5b25de56d1ecbaea114a1c9fd1a3d6ce6fd1aa6c93526a51c40804637
```

## 3. What changed in v1.5

Only one code-level factor was changed from v1.4:

```diff
- for candidate_count in (30, 25, 20, 16, 12, 8, 6, 4):
+ candidate_counts = (16, 12, 10, 8, 6, 4) if profile.get("many_labels") else (30, 25, 20, 16, 12, 8, 6, 4)
+ for candidate_count in candidate_counts:
```

Interpretation:

- For high-cardinality tasks such as Banking77 DEV, the first arbitration prompt now uses top16 candidates rather than top30.
- For smaller or non-many-label tasks, behavior remains unchanged.
- This is a context-budget/candidate-noise adjustment, not a Banking77 shortcut.
- No external dependencies, no file I/O, no label-specific phrase table were added.

## 4. DEV diagnostics: v1.4 failure structure

v1.4 public DEV diagnostic:

| Metric | Value |
|---|---:|
| Accuracy | 77.74% = 419/539 |
| Labels | 77 |
| Train / DEV | 231 / 539 |
| LLM calls | 356 |
| avg prompt/call | 1540.5 |
| p95 prompt/call | 1788.5 |
| local-return accuracy | 88.52% on 183 samples |
| LLM-route accuracy | 72.19% on 356 samples |

Retriever rank evidence:

| Rank bucket | Recall |
|---|---:|
| @1 | 56.40% |
| @3 | 78.29% |
| @5 | 85.16% |
| @10 | 92.02% |
| @20 | 96.85% |
| @30 | 98.14% |

Critical implication:

- The right label is almost always somewhere in the top30, so the retriever is not catastrophically missing labels.
- But top1 is only 56.40%; DEV is a dense 77-label same-domain intent task with many near-neighbor labels.
- The remaining gap is mostly candidate arbitration and fine-grained intent discrimination, not simple retrieval coverage.

Observed error patterns include:

- `why_verify_identity` vs `verify_my_identity`
- `atm_support` vs `card_acceptance`
- `card_payment_fee_charged` vs `extra_charge_on_statement`
- `balance_not_updated_after_bank_transfer` vs `transfer_timing`
- `exchange_via_app` vs `exchange_rate` / `fiat_currency_support`

These are semantically adjacent Banking77 intents. They are not the same type of problem as OOD topic classification or option extraction.

## 5. Candidate-budget ablation

The new diagnostic enabled a narrow ablation over the many-label arbitration candidate count:

| Version | many-label first candidates | DEV accuracy | Correct | avg prompt/call | p95 prompt/call | Adopt? |
|---|---:|---:|---:|---:|---:|---|
| v1.4 | 30 | 77.74% | 419/539 | 1540.5 | 1788.5 | no |
| v1.7 exp | 12 | 77.74% | 419/539 | 790.4 | 912.2 | no |
| v1.5 | 16 | **78.11%** | **421/539** | 1016.0 | 1146.0 | yes |
| v1.6 exp | 20 | 77.55% | 418/539 | 1243.4 | 1384.0 | no |

Interpretation:

1. `top30` gives high coverage but too much distractor context for Qwen3-8B, creating arbitration noise.
2. `top12` is very cheap but starts to lose useful candidates; it matches v1.4 accuracy but does not improve it.
3. `top20` was a useful negative control: adding candidates back did not recover accuracy and increased prompt cost.
4. `top16` is the best observed balance on public DEV and reduces prompt cost substantially.

This does not prove 16 is globally optimal. It proves that “all relevant labels/examples in prompt” is not automatically better, and that context noise is a real failure mode for this small non-thinking model.

## 6. v1.5 validation results

### 6.1 Public DEV diagnostic

| Metric | Value |
|---|---:|
| Accuracy | 78.11% = 421/539 |
| LLM calls | 356 |
| avg prompt/call | 1016.0 |
| p95 prompt/call | 1146.0 |
| max prompt/call | 1280 |
| local-return accuracy | 88.52% |
| LLM-route accuracy | 72.75% |

### 6.2 Public DEV normal runner

| Metric | Value |
|---|---:|
| Accuracy | 78.1% |
| prompt/条 | 671 |
| completion/条 | 2.6 |
| elapsed | 45.3s |
| workers / runs | 4 / 1 |

### 6.3 mock_private v3 all-mode

| Metric | Value |
|---|---:|
| standard official score | 99.53% |
| standard Task1 | 97.64% |
| standard Task2 | 100.00% |
| standard Task3 | 100.00% |
| stress macro | 88.89% |
| LLM calls | 152 |
| truncations | 0 |

v1.5 does not regress mock relative to v1.4. Therefore it is a strict practical improvement in the current evidence set: slightly better DEV, much lower DEV arbitration prompt budget, unchanged mock.

## 7. Why mock is much higher than DEV

The answer is not “mock is a dataset so it should behave like DEV”. They are datasets, but they stress different dimensions.

### 7.1 DEV stresses high-cardinality near-intent arbitration

Public DEV is 77 labels, roughly 3 train examples per label, all in one banking/customer-service domain. Many labels are intentionally adjacent:

- identity action vs identity reason;
- card payment failure vs card not working vs virtual card not working;
- exchange rate vs exchange operation vs cash-withdrawal exchange-rate problem;
- pending transfer vs transfer timing vs bank-transfer balance delay.

The retriever finds the right neighborhood, but the model must choose among near-synonyms with limited examples. That is difficult for Qwen3-8B-Instruct non-thinking mode.

### 7.2 mock standard stresses task-shape robustness

The current `mock_private` standard set deliberately includes multilingual labels, OOD routing, injection-like text, and MCQ. The final harness handles these well because its architecture has:

- runtime label schema;
- task profiler;
- memory index and candidate recall;
- data/instruction boundary;
- MCQ option-structure detection;
- exact-label verifier.

Those are exactly the structural Harness Engineering requirements. Many mock subtasks have smaller or clearer label spaces than Banking77 DEV, so once routing and verifier are correct, accuracy becomes high.

### 7.3 This is not a reason to ignore DEV

DEV still exposes a real weakness: fine-grained semantic arbitration within a dense label set. The right future fix is not to add Banking77 shortcuts, but to improve generic contrastive arbitration: for example, pairwise label contrast pages, hard-negative examples, or a verifier that asks whether the predicted label and the nearest confusable alternative differ on the query’s decisive clue.

## 8. Honest assessment of previous effort

The previous v1.4 long-run effort was partially sufficient:

- It correctly moved away from metric-only shortcut code.
- It reached the requested DEV threshold and very strong mock results.
- It preserved the core architecture: memory index, candidate recall, context budget, code-level verifier.

But it was not deep enough on DEV failure attribution:

- It had aggregate DEV accuracy but lacked per-example rank/route evidence.
- It could not distinguish retrieval misses from LLM arbitration errors.
- It therefore risked misreading the 78% DEV ceiling as a generic architecture limit.

The new diagnostic fixes that gap. It shows the next meaningful research direction is contrastive high-cardinality arbitration, not more all-label prompting and not more mock-specific rules.

## 9. Decision

Adopt v1.5 as the current final candidate:

```text
version: v1.5 lean many-label top16 arbitration
sha256: 87c3dde5b25de56d1ecbaea114a1c9fd1a3d6ce6fd1aa6c93526a51c40804637
```

Rejected alternatives:

- v1.4 top30: same architecture but noisier, larger prompt, lower DEV by 2 examples.
- v1.6 top20: negative control; lower DEV and higher prompt than v1.5.
- v1.7 top12: cheaper but no accuracy gain and likely too narrow for hidden high-cardinality tasks.

Next non-slop direction:

- Implement a generic contrastive memory page for high-cardinality tasks: after top-k recall, identify the top confusable label pairs and present decisive positive/negative examples rather than only flat candidate lists.
- Keep it domain-agnostic and factorized so it can be ablated against v1.5.
