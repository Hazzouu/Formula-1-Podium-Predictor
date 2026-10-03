# F1 Podium Prediction — CSEN 903 Milestone 1

Binary classifier: for each (raceId, driverId), will the driver finish on the podium?
Target: `podium = positionOrder <= 3`. Deadline: 2026-10-18 23:59.
For domain detail, workflow and checklists, load the `f1-podium` skill.

## Roles: you implement, the team decides
- **You (Claude Code) write all code.** The team gives instructions, usually as a brief in `briefs/NN_*.md`.
  Read the brief for the section before starting, and do exactly its scope.
  Teammates may also prompt you directly with no brief. These rules apply either way.
- **You do not make project decisions.** Before any design choice (cleaning rule, row filter, feature, imputation,
  encoding, split, model, metric, threshold strategy), check `decisions.md`:
  - Already decided → follow it.
  - `_pending_` or not listed → present Options → Reasoning → Recommendation, then **stop and wait**.
    Implement only after the person prompting you picks. Then write the row in `decisions.md` with their name as
    "who decided". Never fill a row on your own judgment.
  - Request contradicts a logged decision → say so and quote the row. Change it only on an explicit override,
    keeping the old choice in the "why" column.
- If a brief is ambiguous or the data contradicts it, stop and write the question under "Open questions" in the
  section's findings file instead of choosing.
- Pure implementation details (variable names, helper structure, plot styling) are yours: take the simplest
  choice consistent with these rules.
- Every team member must be able to defend any step at evaluation. After finishing a task:
  - update `findings/NN_<section>.md` (template: `findings/_template.md`): key numbers, one line per plot,
    decisions made, open questions. Numbers come from running the code, never estimated.
  - reply with what changed (files, cells), the evidence produced, and 2–3 likely grader questions with answers.

## Repo layout (read before editing anything)
- `sections/NN_*.py` — the notebook, one file per section, jupytext percent format (`# %%`, `# %% [markdown]`).
  Edit these, never the `.ipynb`.
- `sections/common.py` — imports, paths, seeds, shared helpers. Becomes the notebook's first cell.
- `scripts/build_notebook.py` — joins `common.py` + sections in order into `podium.ipynb` (the Kaggle deliverable).
- `data/raw/` — the 14 Kaggle CSVs. **Immutable. Never write here.** Clean copies only.
- `data/interim/` — parquet handoffs between sections (gitignored).
- `results/experiments.csv` — every metric from every trial, written via `log_result()`.
- `briefs/NN_*.md` — task briefs written by the team (planning happens outside Claude Code). Optional input.
- `findings/NN_*.md` — what each section found: numbers, plot takeaways, open questions. Always updated.
- `decisions.md` — every team decision. Overrides briefs and prompts; only CLAUDE.md rules rank higher.

## Section contracts
Sections talk only through files in `INTERIM`, never through shared variables.
A section must run standalone after the sections it reads from.

| Section | Reads | Writes |
|---|---|---|
| 01_audit_eda | raw CSVs | `audit_report.parquet` |
| 02_cleaning | raw CSVs | `clean_<table>.parquet`, `results_dedup.parquet` |
| 03_de_questions | clean tables | figures only |
| 04_features | clean tables | `model_table.parquet` |
| 05_preprocessing | model_table | `preprocessor.joblib`, `splits.parquet` |
| 06_models | model_table, preprocessor | `models/*.joblib`, experiments.csv |
| 07_ablation | model_table | experiments.csv |
| 08_xai | models, model_table | figures |
| 09_inference | models, preprocessor | — |
| 10_summary | experiments.csv | final tables |

If you change a contract (file name, column name, dtype), update this table in the same commit.

## Non-negotiables
1. **Prediction cutoff = after qualifying, before lights out.** Allowed: grid, qualifying (q1–q3, quali position),
   anything from *earlier* races, static driver/constructor/circuit info.
   Banned as features (current race): `position, positionText, positionOrder, points, laps, time, milliseconds,
   fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId`, all of `lap_times`, `pit_stops`,
   and current-race rows of `driver_standings`, `constructor_standings`, `constructor_results`.
2. **Standings and form use only strictly earlier races.** Sort by race date, then `shift(1)` within the group.
   Standings join to the *previous* race of the same season; first race of a season → 0 / missing, documented.
3. **Grain:** model table has exactly one row per `(raceId, driverId)`. Assert it.
4. **Split by season:** train ≤ 2019, validation 2020–2021, test ≥ 2022. Never random-split rows.
5. **Fit on train only:** imputers, scalers, encoders, resampling. Thresholds and hyperparameters are chosen on validation.
   Test is scored once per final model, never used to choose anything.
6. **Sprint results:** pending team decision. Do not use until it is recorded in `decisions.md`.
7. **Keep every trial.** The brief grades visible before/after cells. Never delete, merge or "clean up" experiment,
   ablation, trial, or justification-markdown cells, even if they look redundant.
8. **Every claim gets evidence:** a plot, a statistic, or an experiment in the notebook. Explanations (SHAP, LIME,
   permutation importance) are described as model reliance, **never** as causal effects.
9. Seeds: use `SEED` from `common.py` everywhere.

## Skills
- `f1-podium` (project) — domain, leakage checklist, experiment protocol. Load it for any section work.
- `ponytail` — use for pipeline code in `sections/*.py` and `common.py` (invoke `/ponytail` if it isn't active).
  **Scope limit:** ponytail must not remove trial cells, ablation variants, or markdown justification (rule 7).
  Minimal code ≠ minimal evidence.
- `graphify` — query the project graph for joins and contracts before grepping.
  Rebuild after structural changes: `/graphify . --update`.

## Workflow
- Branch per section: `sec/04-features`. Small PRs. The owner of a section reviews changes to it.
- Before a PR: `python scripts/build_notebook.py --execute` must run clean end to end, and the section's findings
  file is updated.
