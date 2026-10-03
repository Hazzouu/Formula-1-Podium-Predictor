# F1 Podium Prediction — CSEN 903 Milestone 1

Predict whether each driver finishes on the podium, using only pre-race information.
Deliverables: Kaggle notebook link · this repo · PDF report. **Deadline: 18 Oct 2026, 23:59.**

## Setup (each teammate, once)
```bash
git clone <repo-url> && cd f1-podium
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Data: download the Kaggle dataset and unzip the 14 CSVs into data/raw/
kaggle datasets download -d rohanrao/formula-1-world-championship-1950-2020 -p data/raw --unzip
```

### Claude Code skills
The project skill `f1-podium` is committed under `.claude/skills/` and loads automatically.
Install the two third-party skills **project-scoped** once (one person), then commit what they add:
```bash
# graphify (needs Python 3.10+)
pip install graphifyy
graphify claude install --project
# then in Claude Code:  /graphify .     (rebuild later with /graphify . --update)

# ponytail — project-scoped skills
npx -y skills add DietrichGebert/ponytail --skill ponytail --agent claude-code
npx -y skills add DietrichGebert/ponytail --skill ponytail-review --agent claude-code
```
Optional per person: the ponytail *plugin* (injects its rules every turn, stronger than the skill alone):
`/plugin marketplace add DietrichGebert/ponytail` then `/plugin install ponytail@ponytail`.
Either way, CLAUDE.md rule 7 limits it: it never removes trial or justification cells.

## Daily workflow
0. Write the brief in `briefs/NN_*.md` (planned in the claude.ai Project chat), then tell Claude Code:
   *"Implement briefs/04_features.md"*. Claude Code writes the code; the team makes the decisions.
1. `git checkout -b sec/04-features`
2. Edit `sections/04_features.py` (open it as a notebook in VS Code/Jupyter via jupytext, or edit as text).
3. `python scripts/build_notebook.py --execute` — must pass.
4. Open a PR; the section owner reviews.

No brief? Prompt Claude Code however you like. CLAUDE.md makes it check `decisions.md` before any design choice,
ask you instead of deciding silently, and update `findings/` when it finishes. Read `decisions.md` and `findings/`
before the evaluation: anyone can be asked about any step.

**Never commit `podium.ipynb` edits by hand** — it is generated. Upload the built notebook to Kaggle.

## Ownership (edit names)
| Owner | Sections | Also owns |
|---|---|---|
| Member A | 01 Audit/EDA, 02 Cleaning | `common.py`, build script |
| Member B | 03 DE questions | Report: DE answers |
| Member C | 04 Features, 05 Preprocessing, 07 Ablation | Report: features & limitations |
| Member D | 06 Models, 08 XAI, 09 Inference, 10 Summary | Report: results |

Critical path: 02 → 04 → 05 → 06 → (07, 08, 09). Members B and D can start on 03 and model code
against a dummy `model_table` while 02/04 land.

## Timeline
| Dates | Milestone |
|---|---|
| Oct 3–5 | Repo, data, 01 audit, decisions on duplicates/Indy 500/DNQ |
| Oct 6–8 | 02 cleaning done, `model_table` v1 from 04 |
| Oct 9–12 | 03 answers, 05 experiments, 06 models |
| Oct 13–15 | 07 ablation, 08 XAI, 09 inference |
| Oct 16–17 | 10 summary, report PDF, full run-all on Kaggle |
| Oct 18 | Submit |
