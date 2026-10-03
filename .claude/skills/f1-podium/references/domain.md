# F1 domain notes (condensed from "Intro to F1" + Milestone 1 brief)

## Data facts that affect code
- 14 Kaggle/Ergast CSVs; missing values are the literal string `\N`.
- `results.csv`: one row per entrant per race. Three position columns:
  - `position`: official, `\N` if not classified
  - `positionText`: number or letter code R retired, D disqualified, E excluded, W withdrawn, F failed to qualify, N not classified
  - `positionOrder`: always filled, final post-appeal order → **target source**
- A retired driver can still be *classified* (≥90% of winner's laps) and get a number.
- `grid` = actual starting slot after penalties; differs from qualifying position. `0` likely = pit-lane start (verify).
- `qualifying.csv` believed to start mid-1990s (confirm). q2/q3 `\N` for drivers knocked out early.
- `status`: "Finished", "+N Lap(s)" = reached the flag. 100+ other values = reasons for stopping.
  Question 3 needs a documented mechanical vs non-mechanical mapping
  (mechanical: Engine, Gearbox, Hydraulics, Brakes, Power Unit, Transmission, Electrical, Suspension, …;
  non-mechanical: Accident, Collision, Spun off, Disqualified, Withdrew, …).
- Constructor renames create new `constructorId`s; team history resets.
- Base rate: ~15% podium per row in modern era; much lower in eras with 30+ entrants and DNQ rows.

## Early-F1 oddities
- **Shared drives (≤1957):** duplicate (raceId, driverId) rows. Candidate rules: keep the row with non-zero grid
  (the car he started in) or best positionOrder. Pick, justify, document.
- **Indianapolis 500 (1950–1960)** counted for the championship; regulars rarely entered. Distorts home-race and
  race-count stats. Excluding it is defensible.
- **DNQ / DNPQ rows** (late 1980s–early 1990s): entries with no race start. Decide whether they stay.
- Very high retirement rates early on.

## Eras (for splits, stratified plots, Q1/Q3)
| Seasons | Era |
|---|---|
| 2022–2024 | Ground-effect; budget cap since 2021 |
| 2014–2021 | Turbo-hybrid (Mercedes dominance; 2020 = 17 races) |
| 2009–2013 | Late V8; DRS from 2011 |
| 1995–2008 | V10 / early V8, refuelling |
| 1989–1994 | Post-turbo |
| 1977–1988 | Turbo + ground effect |
| 1966–1976 | 3-litre + wings |
| 1958–1965 | Rear-engine |
| 1950–1957 | Front-engine |

## Qualifying formats
2006+ three-part knockout (q1/q2/q3) · 1996–2005 mostly single session → q1 only · ≤1995 little/no data.

## Sprint
2021–2022: sprint result set the Sunday grid. 2023+: separate sprint qualifying; Friday qualifying sets Sunday grid.

## Data-engineering questions (brief §2)
1. Circuits converting a front-row start (grid 1–2 vs quali 1–2: distinguish!) into a podium; pre vs post 2014.
2. Home-race podium effect controlling for starting position (map driver nationality → circuit country).
3. Constructor mechanical-retirement rate, 2014–2021 vs 2022–2024 (denominator = race starts).
