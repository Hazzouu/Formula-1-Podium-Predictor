# %% [markdown]
# # Formula 1 Podium Prediction — Milestone 1
# Predict, for each driver in each race, whether they finish in the top 3, using only information available
# after qualifying and before the race starts.
#
# **Sections:** 01 Audit & EDA · 02 Cleaning · 03 Data-engineering questions · 04 Features · 05 Preprocessing ·
# 06 Models · 07 Ablation · 08 XAI · 09 Inference · 10 Summary

# %%
import os, random, warnings
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.max_columns", 60)
sns.set_theme(style="whitegrid")

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# --- Paths: Kaggle vs local -------------------------------------------------
ON_KAGGLE = Path("/kaggle/input").exists()
if ON_KAGGLE:
    RAW = next(Path("/kaggle/input").glob("*formula-1*"), Path("/kaggle/input/formula-1-world-championship-1950-2020"))
    WORK = Path("/kaggle/working")
else:
    ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "CLAUDE.md").exists())
    RAW = ROOT / "data" / "raw"
    WORK = ROOT

INTERIM = WORK / "data" / "interim"
FIGURES = WORK / "results" / "figures"
MODELS = WORK / "models"
EXPERIMENTS = WORK / "results" / "experiments.csv"
for d in (INTERIM, FIGURES, MODELS):
    d.mkdir(parents=True, exist_ok=True)

# --- Split boundaries (CLAUDE.md rule 4) -----------------------------------
TRAIN_MAX_YEAR, VAL_YEARS, TEST_MIN_YEAR = 2019, (2020, 2021), 2022

# --- Leakage guard (CLAUDE.md rule 1) --------------------------------------
BANNED_FEATURES = {
    "position", "positionText", "positionOrder", "points", "laps", "time", "milliseconds",
    "fastestLap", "rank", "fastestLapTime", "fastestLapSpeed", "statusId", "status",
    "podium",  # target
}

def assert_no_leakage(X: pd.DataFrame) -> None:
    bad = BANNED_FEATURES & set(X.columns)
    assert not bad, f"Leakage: banned columns in feature matrix: {sorted(bad)}"

# --- I/O helpers ------------------------------------------------------------
def read_raw(table: str) -> pd.DataFrame:
    """Read a raw CSV with '\\N' treated as missing. Raw files are never modified."""
    return pd.read_csv(RAW / f"{table}.csv", na_values=["\\N"], keep_default_na=True)

def write_interim(df: pd.DataFrame, name: str) -> Path:
    path = INTERIM / f"{name}.parquet"
    df.to_parquet(path, index=False)
    return path

def read_interim(name: str) -> pd.DataFrame:
    return pd.read_parquet(INTERIM / f"{name}.parquet")

def savefig(name: str, fig=None) -> None:
    (fig or plt.gcf()).savefig(FIGURES / f"{name}.png", dpi=120, bbox_inches="tight")

def log_result(section: str, trial: str, model: str, variant: str, split: str, **metrics) -> None:
    """Append one row of metrics to results/experiments.csv (the single source for report tables)."""
    row = dict(ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
               section=section, trial=trial, model=model, variant=variant, split=split, **metrics)
    pd.DataFrame([row]).to_csv(EXPERIMENTS, mode="a", header=not EXPERIMENTS.exists(), index=False)

def season_split(df: pd.DataFrame, year_col: str = "year"):
    """Return boolean masks (train, val, test) by season."""
    y = df[year_col]
    return y <= TRAIN_MAX_YEAR, y.between(*VAL_YEARS), y >= TEST_MIN_YEAR

print(f"Kaggle={ON_KAGGLE} | RAW={RAW} | INTERIM={INTERIM}")
