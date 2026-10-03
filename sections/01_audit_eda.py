# %% [markdown]
# ## 1. Audit & pre-cleaning EDA
# **Goal:** profile all 14 raw tables before any cleaning, so section 2 can show before/after.
# **Reads:** raw CSVs · **Writes:** `audit_report.parquet` · **Brief:** §1 Initial EDA (before cleaning)
#
# TODO (owner: see README): row counts, `\N` counts per column, dtypes, PK uniqueness, FK reconciliation,
# qualifying coverage per season, entrants per race per season, podium base rate per season.

# %% tags=["dev-only"]
from common import *

# %%
TABLES = ["circuits", "constructors", "constructor_results", "constructor_standings", "drivers",
          "driver_standings", "races", "results", "qualifying", "lap_times", "pit_stops",
          "sprint_results", "seasons", "status"]
