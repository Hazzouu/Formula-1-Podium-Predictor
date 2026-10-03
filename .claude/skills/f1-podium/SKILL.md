---
name: f1-podium
description: Workflow, domain knowledge and leakage rules for the F1 podium-prediction project (CSEN 903 Milestone 1). Use for any work on sections/*.py, features, cleaning, modeling, experiments, XAI or the report.
---

# F1 Podium Prediction — working skill

CLAUDE.md holds the rules that are never broken. This skill holds the *how*.

## Before touching a section
1. Read the section contract in CLAUDE.md (what it reads and writes).
2. If the task touches features, standings, form, sprint or anything from `results`, read
   `references/leakage-checklist.md` first.
3. If the task involves F1 terms, eras or data oddities you are unsure of, read `references/domain.md`.
4. If the task is an experiment, comparison, ablation or "try X", follow `references/experiment-protocol.md`.

## Decision format (team convention)
Before any non-trivial choice (rule, feature, model, encoding, imputation), present:
1. **Options:** 2–3 viable approaches.
2. **Reasoning:** trade-offs for *this* data (era drift, class imbalance ~15% or lower, qualifying coverage gaps).
3. **Recommendation:** one choice, and why.

Wait for the person's choice — never pick for them. Then record it in `decisions.md`: decision, date,
who decided, evidence cell. When the section's work is done, update `findings/NN_<section>.md`
(template: `findings/_template.md`).

## Writing a section file
- Jupytext percent format. Markdown cells: `# %% [markdown]`, code cells: `# %%`.
- Start every section with a markdown cell: goal, inputs, outputs, brief requirement it satisfies.
- The first code cell is the dev-only bootstrap (the build strips it, because `common.py` is already cell 1):
  ```python
  # %% tags=["dev-only"]
  from common import *
  ```
- Load inputs with `read_interim(name)` / `read_raw(table)`, save outputs with `write_interim(df, name)`.
- After each transformation, show its effect (shape, nulls, distribution before vs after). The brief grades this.
- Plots: one idea per figure, titled, axes labelled, saved with `savefig(name)`, then a markdown cell
  interpreting it in 1–3 sentences.
- End with `assert` checks on the outputs (grain, dtypes, no banned columns: `assert_no_leakage(df)`).
- Run a section alone: `cd sections && python -m jupytext --to notebook --execute 04_features.py` or open it in
  VS Code / Jupyter as a notebook (jupytext pairs it).

## Code style
- pandas + scikit-learn; Keras or PyTorch for the shallow NN (1–2 hidden layers).
- Prefer pandas/sklearn built-ins over hand-written loops (ponytail applies here).
- No abstraction used by only one section. Shared helpers go in `common.py` only if 2+ sections use them.

## Checklist mapping (brief → section)
| Brief item | Section |
|---|---|
| EDA before/after cleaning | 01, 02 |
| Sentinels `\N`, semantic typing, PK/FK checks, grain + duplicate rule | 02 |
| DE questions 1–3, with plots and markdown answers | 03 |
| Feature evidence, leakage-safe form feature | 04 |
| Preprocessing effect + ≥2 preprocessing-order experiments | 05 |
| Baseline + ≥3 modeling attempts, all metrics on train/val/test | 06 |
| Feature-group ablation | 07 |
| Permutation importance, SHAP, LIME / local SHAP | 08 |
| Inference function on complete + partially missing record | 09 |
| Comparison tables and limitations for the report | 10 |

## Evaluation readiness
Any teammate can be asked about any step. When you finish a section, add a short
"Defend this" markdown cell at the end: the 2–3 questions a grader is most likely to ask, with one-line answers
pointing at the evidence cell.
