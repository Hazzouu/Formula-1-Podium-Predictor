# %% [markdown]
# ## 7. Feature-group ablation
# **Goal:** remove one feature group at a time (groups defined in 04), retrain, report the drop on validation.
# **Reads:** `model_table` · **Writes:** experiments.csv · **Brief:** §5

# %% tags=["dev-only"]
from common import *
