# %% [markdown]
# ## 6. Predictive modeling
# **Goal:** baseline + ≥2 statistical models + shallow NN on the same table. ROC-AUC, PR-AUC, F1 (threshold chosen
# on validation) on train/val/test. Primary/secondary metric justified. Limitations of each model.
# **Reads:** `model_table`, preprocessor · **Writes:** `models/*.joblib`, experiments.csv · **Brief:** §4

# %% tags=["dev-only"]
from common import *
