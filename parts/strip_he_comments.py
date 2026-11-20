"""TEMPORARY tool: remove the Hebrew helper comments before submission.

Helper comments are code lines that start with `# HE:`. They help us understand the code and
must not stay in the submitted notebooks (the submission language is English).

Usage (from the repository root):
    python parts/strip_he_comments.py Q1_neural_spikes.ipynb Q2_laptop_analysis.ipynb

It works on .ipynb files (code cells only) and on .py files, and prints how many lines it removed.
"""
import json
import sys


def keep(line):
    return not line.lstrip().startswith("# HE:")


def strip_notebook(path):
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    removed = 0
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            kept = [line for line in cell["source"] if keep(line)]
            removed += len(cell["source"]) - len(kept)
            cell["source"] = kept
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return removed


def strip_python(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    kept = [line for line in lines if keep(line)]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(kept)
    return len(lines) - len(kept)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        n = strip_notebook(p) if p.endswith(".ipynb") else strip_python(p)
        print(f"{p}: removed {n} helper comment lines")
