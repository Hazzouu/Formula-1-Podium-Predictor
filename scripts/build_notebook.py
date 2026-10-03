"""Assemble sections/common.py + sections/NN_*.py into one run-all notebook (podium.ipynb).

Usage:
    python scripts/build_notebook.py            # build only
    python scripts/build_notebook.py --execute  # build, then run top to bottom (must pass before a PR)
"""
import argparse
import subprocess
import sys
from pathlib import Path

import jupytext
import nbformat

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "sections"
OUT = ROOT / "podium.ipynb"


def load_cells(path: Path):
    nb = jupytext.read(path, fmt="py:percent")
    return [c for c in nb.cells if "dev-only" not in c.metadata.get("tags", [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args()

    files = [SECTIONS / "common.py", *sorted(SECTIONS.glob("[0-9][0-9]_*.py"))]
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    for f in files:
        nb.cells.extend(load_cells(f))
    nbformat.write(nb, OUT)
    print(f"Built {OUT.name}: {len(nb.cells)} cells from {len(files)} files")

    if args.execute:
        r = subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
                            "--inplace", "--ExecutePreprocessor.timeout=1800", str(OUT)], cwd=ROOT)
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
