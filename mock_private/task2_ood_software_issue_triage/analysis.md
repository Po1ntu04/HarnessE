# task2_ood_software_issue_triage

Group: `task2_ood_classification`
Profile: `classification_like`
Labels: `['bug_report', 'feature_request', 'documentation', 'installation_help', 'performance_regression', 'usability_feedback']`
Train/Test counts: 18 / 18
Train label counts: `{'bug_report': 3, 'documentation': 3, 'feature_request': 3, 'installation_help': 3, 'performance_regression': 3, 'usability_feedback': 3}`
Test label counts: `{'bug_report': 3, 'documentation': 3, 'feature_request': 3, 'installation_help': 3, 'performance_regression': 3, 'usability_feedback': 3}`

## Why this task exists

Software issue triage for repository-style reports.

## Hard slices

- `bug_vs_usability`
- `performance_regression`
- `installation_help`

## Expected failure modes

- Hard-coded Banking77 rules fail on non-banking tasks.
- Routers that use label set alone fail on A/B/C/D non-MCQ controls.
- Weak prompt boundaries follow instruction-like text inside `text`.
- Weak verifiers return explanations or labels not present in the current train label set.
