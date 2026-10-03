# Brief 01 — Audit & pre-cleaning EDA

**Owner:** Hazzou · **Section file:** `sections/01_audit_eda.py` · **Branch:** `sec/01-audit`
**Findings:** `findings/01_audit_eda.md`
**Brief requirement:** Milestone 1 §1 — initial EDA *before* cleaning, PK/FK verification, grain check, sentinels.

## Purpose
Describe the raw data as it is, with no cleaning. This section produces the evidence the team needs to make
decisions 4–8 in `decisions.md` (duplicate rule, Indy 500, DNQ rows, sprint, training window).
**Do not make any of those decisions here.** Measure and report only.

## Rules for this section
- Read raw CSVs only. Never write to `data/raw/`.
- For sentinel counting, read with `dtype=str, keep_default_na=False` so `\N` is counted literally.
  Everywhere else use `read_raw()` from `common.py`.
- Every plot: saved with `savefig("01_<name>")`, followed by a markdown cell interpreting it in 1–3 sentences.
- Use the Milestone's season range as data allows; report the actual min/max season found.

## Tasks

### 1.1 Table inventory
For all 14 tables: rows, columns, inferred dtypes (as read with defaults), memory.
Output: one summary DataFrame, displayed.

### 1.2 Sentinels and missingness
- Count literal `\N` per column per table. Also check for other placeholders: empty strings, whitespace-only,
  `"NULL"`, `"nan"`. Report any found.
- Columns that should be numeric/date but are strings because of sentinels (e.g. `results.position`,
  `results.milliseconds`, `qualifying.q1–q3`, `races.date/time`, lap-time strings). List them; this is the
  to-do list for typing in section 02.
- **Plot:** heatmap or bar chart of % missing per column for `results`, `qualifying`, `races`, `drivers`.

### 1.3 Primary keys
Check uniqueness and non-null for:

| Table | PK |
|---|---|
| circuits | circuitId |
| constructors | constructorId |
| drivers | driverId |
| races | raceId |
| seasons | year |
| status | statusId |
| results | resultId |
| sprint_results | resultId |
| qualifying | qualifyId |
| driver_standings | driverStandingsId |
| constructor_standings | constructorStandingsId |
| constructor_results | constructorResultsId |
| lap_times | (raceId, driverId, lap) |
| pit_stops | (raceId, driverId, stop) |

Output: table with PK, n_rows, n_unique, n_null, pass/fail.

### 1.4 Foreign keys
For every FK, count orphan values (present in child, missing in parent):
- results, qualifying, sprint_results → races.raceId, drivers.driverId, constructors.constructorId
- results, sprint_results → status.statusId
- races → circuits.circuitId, seasons.year
- driver_standings → races, drivers · constructor_standings, constructor_results → races, constructors
- lap_times, pit_stops → races, drivers

Output: table FK, n_orphans, example orphan values. Also report races with **no** results rows (future or
cancelled races in the calendar).

### 1.5 Grain check — (raceId, driverId) in `results`
- Number of duplicated (raceId, driverId) pairs and rows involved.
- **Plot:** duplicates per season.
- Show 3 full example groups (all columns, joined with race name and year, driver name).
- For each duplicate group, report: how many rows have `grid > 0`, whether they share `constructorId`,
  and their `positionOrder` values. This is the evidence for choosing the duplicate rule.
- Same check on `qualifying` and `sprint_results`.

### 1.6 Era and coverage profile (per season)
One DataFrame indexed by season, plus plots:
- races per season; entrants per race (mean, max) — **plot**
- qualifying coverage: % of results rows with a matching qualifying row — **plot** (key for decision 8)
- podium base rate: share of results rows with `positionOrder <= 3` — **plot**
- share of rows with `grid == 0` — **plot**; also show their `positionText` distribution
- `positionText` letter-code counts (R, D, E, W, F, N) by decade — **plot**
- DNQ-like rows: `positionText == "F"` per season, and rows with `grid == 0` *and* no laps

### 1.7 Special cases
- **Indy 500:** identify its raceIds (race name contains "Indianapolis"), count rows and seasons,
  count drivers who appear only in Indy 500 races.
- **Sprint:** seasons covered by `sprint_results`, races per season, rows.
- **Status:** top 30 status values by count, and the total number of distinct values (input to Q3 mapping later).
- **Qualifying vs grid:** for races with qualifying data, share of rows where `qualifying.position != results.grid`
  — **plot** by season. (Evidence for DE Q1 and features.)

### 1.8 Save
`write_interim(audit_df, "audit_report")`, where `audit_df` is the per-season profile from 1.6.

## Acceptance checks
- [ ] `python scripts/build_notebook.py --execute` passes.
- [ ] Section runs standalone (only needs `data/raw/`).
- [ ] No cell modifies raw files; no rows dropped or values changed anywhere in this section.
- [ ] Every plot has a markdown interpretation directly after it.
- [ ] `findings/01_audit_eda.md` filled from the template, with at least:
  - min/max season in the data, total rows per table
  - PK and FK failures (or "none")
  - duplicate (raceId, driverId) count, seasons affected, and the grid/constructor pattern from 1.5
  - first season where qualifying coverage exceeds 90%
  - Indy 500 row count and seasons
  - number of DNQ-like rows and peak seasons
  - sprint coverage
  - share of qualifying position ≠ grid
  - **Open questions:** anything surprising, and any row that breaks an assumption in
    `.claude/skills/f1-podium/references/domain.md`

## Out of scope
Cleaning, type conversion, dropping rows, choosing rules. Those are section 02, after the team decides.
