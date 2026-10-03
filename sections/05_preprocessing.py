# %% [markdown]
# ## 5. Splitting & preprocessing
# **Goal:** season-based split (train ≤ 2019, val 2020–21, test ≥ 2022) with justification; imputation, encoding,
# scaling fitted on train only; show effect on distributions; ≥2 preprocessing-order experiments.
# **Reads:** `model_table` · **Writes:** `preprocessor.joblib`, `splits.parquet` · **Brief:** §3, checklist

# %% tags=["dev-only"]
from common import *
