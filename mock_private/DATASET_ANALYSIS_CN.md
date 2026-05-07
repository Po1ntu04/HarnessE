# mock_private 数据集分析

这是一套本地开发期压力测试集，用来模拟私有评测可能出现的任务形状。它不是 `solution.py` 的运行时依赖，正式提交代码不应读取这些文件。

## 等权建议

私有评测各部分权重未知，因此主建议使用 family macro average：先计算每个 family 内任务平均准确率，再对 family 等权平均。

```text
score = mean(
  mean(banking_same),
  mean(prompt_injection),
  mean(ood_classification),
  mean(mcq)
)
```

task macro average 可作为次要指标：把 8 个任务直接等权平均。不要把 record-level micro average 作为主指标，因为样本数更多的任务会主导结论。

## 任务清单

| Task | Family | Expected profile | Labels | Train | Test | 主要压力点 |
|---|---|---|---:|---:|---:|---|
| `banking77_same_labels` | `banking_same` | `classification_like` | 8 | 24 | 18 | near-label ambiguity, short customer utterances |
| `banking77_injected` | `prompt_injection` | `classification_like_with_injection` | 6 | 12 | 12 | quoted-data boundary, label mention attack |
| `ood_support_router` | `ood_classification` | `classification_like` | 6 | 18 | 12 | OOD label inventory, support-domain overlap |
| `news_topic_ood` | `ood_classification` | `classification_like` | 4 | 12 | 8 | short labels, topic classification |
| `research_intent_ood` | `ood_classification` | `classification_like` | 5 | 15 | 10 | longer abstract-like text, labels are semantic but not customer support intents |
| `short_label_sentiment` | `ood_classification` | `classification_like` | 4 | 12 | 8 | short labels, label-name reliance |
| `mcq_science` | `mcq` | `mcq_like` | 4 | 8 | 8 | A/B/C/D short labels, option reasoning |
| `mcq_reasoning_injected` | `mcq` | `mcq_like_with_injection` | 4 | 8 | 8 | MCQ routing under instruction-like text, answer cue parsing |

## 每类任务的设计目的

- `banking_same`: 验证是否能处理 Banking77 风格同标签新文本和细粒度相近意图。
- `prompt_injection`: 验证输入边界，注入文本仍必须被分类到原任务 label。
- `ood_classification`: 验证 runtime label schema，不依赖银行标签或固定业务规则。
- `mcq`: 验证 `A/B/C/D` 选项推理、MCQ 路由和独立字母解析。

## 主要可暴露的问题

- Banking-only hardcoding: OOD 任务会失败。
- Missing prompt-injection boundary: injected banking / MCQ 任务会被文本中的假指令带偏。
- Router error: MCQ 和普通分类混淆。
- Invalid output: 输出不在当前 train label whitelist 中。
- Weak parser: `Answer: B`、解释文字、大小写/标点变体不能修复。
- Poor retrieval diversity: top-k 被同一 label 或相近强关键词垄断。
