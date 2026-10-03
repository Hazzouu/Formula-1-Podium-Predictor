# %% [markdown]
# ## 4. Feature selection & engineering
# **Goal:** build the leakage-safe modeling table (one row per raceId, driverId) with EDA evidence for each
# feature group. **Reads:** clean tables · **Writes:** `model_table.parquet` · **Brief:** §3
#
# Feature groups (used again in 07 ablation): grid · qualifying · driver form · constructor form ·
# standings (previous race) · static (circuit, era, home race).
# Read `.claude/skills/f1-podium/references/leakage-checklist.md` before adding any feature.

# %% tags=["dev-only"]
from common import *

# %%
FEATURE_GROUPS: dict[str, list[str]] = {
    "grid": [],
    "qualifying": [],
    "driver_form": [],
    "constructor_form": [],
    "standings": [],
    "static": [],
}
