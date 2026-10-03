# %% [markdown]
# ## 2. Cleaning
# **Goal:** sentinels → NaN, semantic typing (dates, lap-time strings → seconds), PK/FK checks,
# grain fixed to one row per (raceId, driverId) with a documented duplicate rule, post-cleaning EDA.
# **Reads:** raw CSVs · **Writes:** `clean_<table>.parquet`, `results_dedup.parquet` · **Brief:** §1
#
# Open decisions (record in decisions.md): duplicate rule for shared drives, Indy 500 (1950–60), DNQ rows.

# %% tags=["dev-only"]
from common import *
