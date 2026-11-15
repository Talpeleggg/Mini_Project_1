# parts/ (temporary working area)

The two final notebooks are shared by several people, so until integration each person works only in their own files here. **Nobody edits another person's file.** Everyone pushes straight to `main` (run `git pull --rebase` first). This folder is deleted at integration.

| File | Owner | Goes into |
|---|---|---|
| `Q1_part1_models_validation.ipynb`, `q1_models.py` | Part 1 | `Q1_neural_spikes.ipynb` |
| `Q1_part2_analysis.ipynb`, `q1_stats.py` | Part 2 | `Q1_neural_spikes.ipynb` |
| `Q2_part2_cleaning.ipynb`, `q2_clean.py` | Part 2 | `Q2_laptop_analysis.ipynb` |
| `Q2_part3_analysis.ipynb` | Part 3 | `Q2_laptop_analysis.ipynb` |
| `Q2_part1_report.ipynb` | Part 1 | `Q2_laptop_analysis.ipynb` |
| `ai_log_part1.md`, `ai_log_part2.md`, `ai_log_part3.md` | Part 1 / 2 / 3 | `AI_USAGE.md` |

Notebooks import the helper modules of other parts with `from q1_models import ...` (run them from this folder). Before every commit clear notebook outputs: `jupyter nbconvert --clear-output --inplace parts/<name>.ipynb`.

Shared files (`README.md`, `AI_USAGE.md`, `requirements.txt`, and the two final notebooks) are not edited during the work phase. If you add a package, tell the group and add one line to `requirements.txt` after `git pull --rebase`.

Integration (planned 28.11, by the person who owns the final submission task): paste the part cells into the two final notebooks, run both from scratch in a fresh environment, merge the AI logs into `AI_USAGE.md`, then delete this folder.
