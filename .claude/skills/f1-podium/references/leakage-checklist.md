# Leakage checklist

Prediction moment: grid is fixed, lights not yet out. Ask of every feature: *"Would I know this value at that moment?"*

## Allowed
- `results.grid` for the current race (0 = pit-lane start: verify in EDA, then encode explicitly, not as "P0").
- `qualifying.position`, `q1`, `q2`, `q3` for the current race (coverage is patchy before the mid-1990s).
- Static info: driver DOB/nationality, constructor nationality, circuit location/country, race date/round, season.
- Anything aggregated from **strictly earlier** races (form, rolling podium rate, previous-race standings).

## Banned (current race)
| Source | Columns / tables |
|---|---|
| results | position, positionText, positionOrder (target only), points, laps, time, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId |
| lap_times, pit_stops | everything |
| driver_standings, constructor_standings, constructor_results | rows with the current raceId |
| status | anything joined via the current result's statusId |
| sprint_results | pending decision (see decisions.md) |

## Traps that look safe but leak
1. **Standings at this raceId** are *after* the race. Join standings of the previous race in the same season.
2. **Rolling means without `shift(1)`** include the current race. Always `groupby(...).shift(1)` *then* roll.
3. **Sorting by raceId** is not chronological. Sort by `date` (then `round`).
4. **Season-level aggregates** (e.g. champion, season podium count) use the future of the same season.
5. **Fitting scalers/imputers/encoders on the full table** leaks validation/test distributions. Fit on train.
6. **Target encoding** of driver/constructor/circuit must be out-of-fold or past-only.
7. **Number of finishers / classified count** for the race is post-race.
8. **DSQ / post-race penalties** affect positionOrder only: fine as target, never as feature.
9. **Sprint (2021–22)** set the Sunday grid; grid already captures it. Using sprint result as an extra feature
   is defensible (it happens before the race) but must be a documented team decision.

## Automated guard
`assert_no_leakage(df)` in `common.py` fails if any banned column name is present in the feature matrix.
Also add a sanity test in 04_features: a form feature for a driver's first-ever race must be NaN / default.
