# Experiment protocol

The brief grades *visible* before/after comparisons. Every trial follows this shape.

## One trial = three cells
```python
# %% [markdown]
# ### Trial 05-B: impute-then-scale vs scale-then-impute
# **Hypothesis:** ... (link the EDA cell that motivated it, or say "empirical")
# **Change vs baseline:** one thing only.

# %%
res = run_trial(...)                       # fit on train, select on validation
log_result(section="05", trial="05-B", model="logreg", variant="scale_then_impute",
           split="val", **res["val"])

# %% [markdown]
# **Result:** PR-AUC 0.61 → 0.63 on validation. **Why:** ... **Kept / rejected.**
```

## Rules
- One change per trial. Same rows, same feature set, same seed unless the trial *is* that change.
- Never delete a rejected trial. Rejected trials are evidence too.
- Choose thresholds and hyperparameters on **validation** only. Test is scored only for final models, in 06 and 10.
- Log every number with `log_result()`. Tables in 10_summary are built from `results/experiments.csv`,
  never typed by hand.
- Metrics for every model: ROC-AUC, PR-AUC, F1 (at the validation-chosen threshold), plus precision and recall.
- Report train, validation and test for final models (the brief wants all three for the comparison table).

## Required minimums (from the brief)
- Baseline: a statistical model or shallow FFNN.
- ≥3 distinct modeling attempts in total.
- ≥2 statistical models + 1 shallow NN on the same modeling table.
- ≥2 preprocessing-order experiments (05).
- Feature-group ablation: one group removed at a time (grid, qualifying, driver form, constructor form, standings, static).

## Trial IDs
`<section>-<letter>`: 05-A, 05-B, 06-A … so the report can cite them.
