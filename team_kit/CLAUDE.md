# Project context for Claude Code (shared by all three students)

You are helping ONE student (the person in this terminal) on a team of three. Read this file fully, then read `MY_PART.md` (the student's own part). Talk to the student in Hebrew. Write code, comments, notebook text and commit messages in English unless the team decides otherwise (decision `g_lang` on the board).

## The assignment in one paragraph

Course: Neuroscience Data Analysis with Python. Mini-Project 1, due **3 December 2026**, one submission per team.
- **Q1 (50 pts) neural spikes**: simulate three neurons for 5 s (regular, irregular, bursting), analyse their firing patterns (raster, ISI, statistics), validate the models with at least three checks (temporal, statistical, edge case), study variability across realizations, and explain how to tell the patterns apart from observations alone.
- **Q2 (50 pts) laptop dataset EDA**: audit and clean `data/laptop_price_dataset.csv`, unify OS names, build a `Storage type` variable from `Memory`, answer at least three analytical questions (one must be RAM vs price, two different kinds of analysis), investigate outliers without automatically removing them, and write a short report separating what was observed, what the analysis supports, and what cannot be concluded.
- Grading: Q1 modeling 10, analysis and visualization 15, validation and interpretation 15, reproducibility 10. Q2 inspection and cleaning 10, questions and methods 15, visualization and interpretation 15, outliers 5, reproducibility/documentation/AI evaluation 5. Scientific reasoning and the ability to explain the work count as much as correct numbers.

## Required repository structure (and nothing else is pushed)

```
README.md  requirements.txt  Q1_neural_spikes.ipynb  Q2_laptop_analysis.ipynb  AI_USAGE.md  figures/  data/
```
`.gitignore` is a whitelist that enforces this. Never force-add other files (`git add -f`) and never add names to the whitelist without asking the student. The two notebooks must run top to bottom in a clean environment. The whole team's work ends up in these two notebooks.

## Rules you must follow

1. **The student decides.** All analytical decisions live on the team's decision board (private link, shared with the team): https://claude.ai/artifact/Pdz3QdkzTp1et1TFkgv374 . Each decision has options with scientific background and one recommended option. The board has one page per student (Shahar = Part 1, Tal = Part 2, Ohad = Part 3, names can be changed on the board) and one shared page. The student can press "העתק את ההחלטות שלי ל־Claude" on their page and paste the summary to you; that is the reliable way. If you can read the board's database, collection `dec` has one document per decision id (`choices`, `labels`, `q`, `note`, `owner`, `task`, `by`) and collection `tasks` has the task status and notes. Do not write code for a task until the decisions it depends on (listed in `MY_PART.md`) are made. Never silently choose the recommended option. If a decision is missing, ask the student, one decision at a time, with the options and their trade-offs.
2. **The student must be able to explain every line.** The assignment says submitting code you cannot explain or validate is not allowed, and any team member may be asked to explain or modify any part during the evaluation. Write short functions with docstrings, explain choices, and after each piece of code give the student two or three questions they should be able to answer. Do not generate large blocks of code in one go.
3. **Verify, do not assert.** Every number in a report or comment must come from code in the notebook. Several statements on the decision board are hand calculations that have not been verified (see "Unverified claims" in `AI_USAGE.md`). Check them in code before using them.
4. **Honest AI documentation.** `AI_USAGE.md` is graded. After each task, add a short entry under the student's name: what you did, what the student chose, how it was verified, and any mistake that was found. Never write section 9 (the example the student challenged or corrected) on the student's behalf. Never invent or embellish. Real problems and corrections belong in the log.
5. **Stay in your own part.** Edit only the notebook sections of your own part (headers are marked `[P1]`, `[P2]`, `[P3]`). Ask before touching anyone else's cells.
6. **Git workflow.** One branch per student (`p1-...`, `p2-...`, `p3-...`), small commits, a Pull Request that another student reviews before merging into `main`. Before every commit clear notebook outputs: `jupyter nbconvert --clear-output --inplace <notebook>.ipynb`. Do not push to `main` directly. Do not push unless the student asks you to.
7. **Reproducibility.** Use `numpy.random.default_rng` and `SeedSequence.spawn` (no global `np.random.seed`), relative paths only, figures saved to `figures/` from code, pinned versions in `requirements.txt` (Python 3.14 environment used so far).

## Interface contracts (DRAFT, confirm after the decisions are made)

All Q1/Q2 code lives inside the two notebooks. Keep these names so that the parts fit together.

Q1, section A (owner P1), spike times are 1-D float64 arrays in seconds, strictly increasing, inside `[0, T)`:
```python
make_rngs(seed: int, n: int = 3) -> list[np.random.Generator]      # SeedSequence.spawn
simulate_regular(T, rng, rate_hz=10.0, cv=0.05, ...)   -> np.ndarray
simulate_irregular(T, rng, rate_hz=10.0, ...)          -> np.ndarray
simulate_bursting(T, rng, rate_hz=10.0, ...)           -> np.ndarray
```
Q1, section B (owner P2), statistics; each returns `np.nan` (never raises) when it is undefined, for example with fewer than 2 or 3 spikes:
```python
isi(spikes), cv(spikes), lv(spikes), fano(spikes, T, window), burst_fraction(spikes, thr_s), isi_lag1_corr(spikes)
```
Q2, cleaning (owner P2): `load_raw()`, `clean(df)` (returns a new DataFrame, never changes the input), `load_clean()`. The new columns are fixed by the decisions `os_map`, `st_type`, `st_extra` (provisional names: `OpSys_clean`, `OS_family`, `Storage_type`, `Storage_GB_total`, `has_SSD`, `Screen_pixels`, `Touchscreen`, `CPU_tier`, `log_price`). P3 uses only these column names.

## Useful facts already computed (re-derive them in the notebook before citing)

- Dataset: 1275 rows, 15 columns, no empty cells, no fully duplicated rows, 48 rows identical except price. `OpSys` has `macOS` and `Mac OS X`. `Memory` has 39 text patterns (double spaces, `1.0TB`, Flash Storage, Hybrid, two drives). Price median 989 EUR, skew 1.51 raw and -0.18 after log. Tukey outliers: 28 on raw price, 1 on log price.
- Environment: `.venv` with numpy, pandas, scipy, matplotlib, seaborn, jupyter, nbconvert, ipykernel.
