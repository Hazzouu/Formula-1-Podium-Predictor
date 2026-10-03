# %% [markdown]
# ## 10. Summary
# **Goal:** model comparison table (val + test), ablation table, preprocessing-order results — all built from
# `results/experiments.csv`, never typed by hand. Selected features and why each is valid at the cutoff.
# Known limitations (qualifying-coverage drift, era sensitivity, renames, early-F1 oddities).
# **Reads:** experiments.csv · **Brief:** Deliverables 4, 5, 8

# %% tags=["dev-only"]
from common import *

# %%
exp = pd.read_csv(EXPERIMENTS) if EXPERIMENTS.exists() else pd.DataFrame()
exp.tail()
