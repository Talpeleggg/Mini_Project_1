# AI log, Part 2

Temporary. At integration the content is merged into the shared `AI_USAGE.md`, under the same heading.

For every task add: date, task id, what the AI did, what the student decided, how it was verified, anything that went wrong. Keep it accurate. Section 9 of AI_USAGE.md (an example you challenged or corrected) is written by the student, never by the AI.

## Entries

### 2026-11-20, task `t_q2a` (Q2 A, data audit), step 1

- **What the AI did:** wrote `load_raw()` in `q2_clean.py` and the first sections of `Q2_part2_cleaning.ipynb`: setup, the definition of a row, and the variables table.
- **Decisions applied (chosen on the board):** `q_data`, `q_dups`, `q_issues`, `q_audit`, `g_lang`, `g_nb`.
- **What the student decided:** all the Q2 A decisions on the board, before any code was written. The student reads each step before the next one is added.
- **How it was verified:** the notebook was executed from a temporary copy. The numbers in the variables table (1,275 rows, 15 columns, no missing values, number of different values per column) match the numbers computed earlier with a separate script (standard `csv` module and pandas).
- **What went wrong or was fixed:** the first version of the variables table sorted the columns alphabetically instead of keeping the file order. Fixed with `reindex(raw.columns)`.
- **Not verified yet:** a run of the whole notebook in a clean environment (planned for integration).
- **Hebrew helper comments (requested by the student):** every code cell and `q2_clean.py` now has comments in Hebrew on lines that start with `# HE:`, to help the team understand the code. They must be removed before submission: `parts/strip_he_comments.py` deletes them automatically. It was tested on a scratch copy (33 lines removed, 0 left, the stripped notebook still runs). Added as the final check `f_he` on the board.

### 2026-11-20, task `t_q2a` (Q2 A, data audit), step 2

- **What the AI did:** added sections 3 (data types) and 4 (missing values and duplicates) to `Q2_part2_cleaning.ipynb`, with Hebrew helper comments (`# HE:`).
- **Decisions applied:** `q_audit` (data types, missing values), `q_dups` (keep and document near-duplicates).
- **How it was verified:** executed a temporary copy. The count of near-duplicate rows (48) matches the independent check done earlier with a separate script. All numbers quoted in the markdown cells were copied from the executed output.
- **Observation to check by the student:** the 208 two-drive `Memory` strings are exactly the 208 strings with a double space; confirm this when writing the parser in Q2 B.
- **Not verified yet:** why the prices differ inside a near-duplicate pair (unknown, stated as such).

### 2026-11-20 and 2026-11-21, task `t_q2a` (Q2 A, data audit), step 3

- **What the AI did:** added sections 5 (ranges and units) and 6 (consistency between columns), with Hebrew helper comments (`# HE:`).
- **Decisions applied:** `q_audit` (ranges, units, consistency checks) and `q_issues` (implausible values or models are flagged and examined, not deleted).
- **How it was verified:** executed a temporary copy and copied every number in the markdown from the output. The claim from step 2 (the 208 strings with two drives are exactly the 208 strings with a double space) was checked separately: 208, 208, 208 in both, 0 different.
- **A first draft was wrong:** an exploratory version of the storage check used a faulty parser and reported that no model name matched the storage. It was caught because the result was implausible (0 of 151), and the parser was rewritten. The notebook contains only the corrected version.
- **Observation to check by the student:** the 3 Lenovo B51-80 rows ("1008GB" in the name, "1.0TB Hybrid" in `Memory`) are a unit convention, not a contradiction. Look at them in the data yourself.
- **Not verified:** the plausible ranges are our own assumptions about typical laptops, not taken from a source.

### 2026-11-21, task `t_q2a` (Q2 A, data audit), step 4 (audit complete)

- **What the AI did:** added section 7 (rare categories, the issues register, the audit summary) and fixed a cross-reference in the header table (the register is in section 7, not 6).
- **Decisions applied:** `q_issues` (what we fix and what we only document), `rare` (group rare categories in a helper column, never delete rows), `q_dups`, `q_audit`.
- **How it was verified:** executed a temporary copy; the issues register builds every number from code (f-strings), so no number in the register is typed by hand. The rare-category counts were read from the output (11 of 19 companies below 10 laptops, 51 rows).
- **Not verified:** the threshold of 10 laptops for "rare" is our choice for the audit; the board decision `g_n` uses a different minimum (20) for group comparisons. They answer different questions.
- **Status:** Q2 A is complete. The next task is Q2 B (cleaning), which produces `load_clean()` for Part 3.

### 2026-11-21, task `t_q2b` (Q2 B, cleaning), step B1: operating system

- **What the AI did:** added `clean_opsys()` to `q2_clean.py` and the header and section 1 of Q2 B to `Q2_part2_cleaning.ipynb`, with Hebrew helper comments (`# HE:`).
- **Decision applied:** `os_map` (merge only true aliases, add `OS_family`), and `validate` (cross-tabulation, asserts).
- **How it was verified:** the cross-tabulation shows that exactly the 8 `Mac OS X` rows changed; the asserts check the row count, no new missing values, one clean name per raw name, and that the alias is gone. A small test checks the function on known input and that an unknown operating system is rejected.
- **Not verified yet:** the whole `clean()` and `load_clean()` (steps B2 to B5).

### 2026-11-21, task `t_q2b` (Q2 B, cleaning), step B2: storage

- **What the AI did:** added `parse_memory()` and `parse_memory_series()` to `q2_clean.py`, and section 2 of Q2 B to the notebook (mapping table of all 39 strings, counts, a capacity check in a second way, tests), with Hebrew helper comments.
- **Decisions applied:** `st_type` (canonical combination label), `st_extra` (`Storage_GB_total` with 1 TB = 1000 GB, `has_SSD`), `validate` (capacity in two ways).
- **How it was verified:** the two capacity computations agree for all 1,275 rows; the 39-row mapping table was inspected; the counts agree with the audit (10 Hybrid, 71 Flash Storage, 208 two-drive strings).
- **A mistake of the AI, found by a test:** the first test expected `Flash Storage + HDD`, but the fixed order of the label gives `HDD + Flash Storage`. The test failed, the AI checked, and fixed the test expectation (the function was right). This is a candidate example for section 9 of `AI_USAGE.md`, to be confirmed by the student.
- **Student's choices to confirm:** `Flash Storage` is not counted as an SSD (our reading, see the notebook); 1 TB = 1000 GB (the three Lenovo B51-80 rows show a 1,008 GB convention).
- **Not verified yet:** `clean()` and `load_clean()` (step B5).

### 2026-11-21, task `t_q2b` (Q2 B, cleaning), step B3: screen, CPU, price, GPU

- **What the AI did:** added `screen_pixels`, `has_touchscreen`, `cpu_tier`, `log_price` and `dedicated_gpu` to `q2_clean.py`, and section 3 of Q2 B to the notebook (new columns, counts, validation, tests), with Hebrew helper comments.
- **Decisions applied:** `st_extra` (the five variables), `tr` (log price), `validate`.
- **What the student decided:** before the code was written the student was told that `Dedicated_GPU` is an approximation by company (some AMD cards are integrated graphics) and chose to keep the decision and document the approximation as a limitation.
- **How it was verified:** all asserts pass (no new missing values, same number of rows, positive pixels, `exp(log_price)` equals the price); the counts agree with the audit (188 touchscreens); small tests on known inputs pass, including that an unknown GPU company is rejected; skewness 1.51 falls to -0.18, matching the value computed earlier with another library.
- **Limitations written to the report skeleton:** `Dedicated_GPU` by company; the mixed `Other` processor group; the 1 TB = 1000 GB convention.
- **Not verified yet:** `clean()` and `load_clean()` (step B5).

### 2026-11-21, task `t_q2b` (Q2 B, cleaning), step B4: rare categories and flags

- **What the AI did:** added `group_rare()`, `flag_near_duplicates()` and `flag_suspicious()` to `q2_clean.py`, and section 4 of Q2 B to the notebook, with Hebrew helper comments.
- **Decisions applied:** `rare` (helper columns, no row deleted), `st_type` (rare storage combinations grouped in the analysis only), `q_dups` and `q_issues` (flag, keep).
- **How it was verified:** no row was lost; every kept category in a helper column has at least 10 laptops; the number of rows in `Other` equals the number computed directly without the function; the flags are identical to the independent computations in the audit (`near_dup_mask`, `any_flag`). Tests on small inputs pass, including that a real category called `Other` is rejected.
- **Observation for the student to understand:** after merging `Mac OS X` into `macOS` the rare operating-system labels drop from 3 (18 rows) to 2 (10 rows), so the order of cleaning matters.
- **Not verified yet:** `clean()` and `load_clean()` (step B5).

### 2026-11-21, task `t_q2b` (Q2 B, cleaning), step B5: `clean()` and `load_clean()`

- **What the AI did:** added `clean()`, `load_clean()` and `COLUMN_DICTIONARY` to `q2_clean.py`, and section 5 of Q2 B to the notebook (final validation, 15-row spot check, data dictionary, fresh-process test), with Hebrew helper comments.
- **Decisions applied:** `validate` (all four kinds of check), `st_extra`, `rare`, `q_dups`, `q_issues`.
- **How it was verified:** the function returns exactly the table built step by step (`assert_frame_equal`), the 15 original columns equal the source, the raw table is unchanged, no missing values in the new columns, and `load_clean()` returns (1275, 32) in a fresh Python process. The 15-row spot check was read by the AI and looks consistent.
- **To be done by the student:** repeat the spot check by hand on 2 or 3 of the 15 rows against the file `data/laptop_price_dataset.csv` (the row number in the notebook plus 2 is the line number in the file). This is the main manual check and it is not done by the AI.
- **Status:** Q2 A and Q2 B are complete, and Part 3 can use `load_clean()` from `parts/q2_clean.py`.

### 2026-11-21, task `t_q1b` (Q1 B, analysis), step 1: statistics functions

- **What the AI did:** wrote `isi`, `mean_rate`, `mean_isi`, `cv`, `lv`, `cv2`, `isi_lag1_corr`, `burst_fraction`, `burst_curve`, `window_counts`, `fano`, `fano_curve`, `rate_over_time` in `q1_stats.py`, and tests in `Q1_part2_analysis.ipynb`.
- **Decisions applied (student chose the recommended option for all):** `b_figs`, `b_axis` (log), `b_bin` (100 ms), `b_stats` (all seven), `b_thr` (curve), `b_fano` (curve).
- **How it was verified:** cases computed by hand, a perfectly regular neuron, a random neuron (CV, LV, Fano about 1), and edge cases returning `nan`.
- **What went wrong:** the first test failed because a regular spike train built with `np.arange(0, 10, 0.1)` has rounding noise, so its standard deviation is not exactly 0 and the serial correlation was a number instead of `nan`. The function was changed to treat a tiny variance as zero.
- **Not done yet:** the figures (need the simulation of Part 1) and the comparison of the three neurons.

### 2026-11-21, task `t_q1b` (Q1 B, analysis), step 2: stand-in neurons, raster, ISI histograms

- **What the AI did:** wrote three temporary stand-in generators (regular, random, bursting; 10 Hz) inside the part notebook, marked `STAND-IN`, because Part 1's simulation is not delivered yet; built the raster and the log-axis ISI histograms.
- **Decisions applied:** `b_figs` (raster, histogram), `b_axis` (log), `a_rate` (10 Hz).
- **How it was verified:** the stand-ins give strictly increasing times inside the recording and mean rates between 9.7 and 10.8 Hz (the bursting one is a little above 10: it is only a stand-in); the AI looked at both figures.
- **To replace:** the `STAND-IN` cell with `q1_models.simulate_*` when Part 1 delivers them.

### 2026-11-21, task `t_q1b` (Q1 B, analysis), step 3: rate, return map, threshold curve, Fano curve

- **What the AI did:** added four figures to the part notebook (rate in 100 ms bins, return map, short-interval threshold curve 2 to 30 ms, Fano curve over window sizes 10 ms to 10 s), still on the stand-in neurons.
- **Decisions applied:** `b_bin`, `b_figs`, `b_thr` (curve), `b_fano` (curve).
- **How it was verified:** assertions on the data (regular neuron has 0 short intervals at 10 ms, bursting more than 0.5, random close to the theoretical 0.095; Fano at 1 s below 0.3 for regular, near 1 for random, above 2 for bursting); the AI looked at all four figures.
- **What was changed after looking:** the first return map had axes stretched down to 1e-6 by a few extreme stand-in intervals, so the axes were limited to 1 ms to 3 s.
- **Not done yet:** a comparison figure on shared axes, the diagram of how each neuron is built, the numbers table, and re-running everything on Part 1's simulation.

### 2026-11-25, task `t_q1b` (Q1 B, analysis), step 4: comparison figure and numbers table

- **What the AI did:** before the step, read the student's choices directly from the decision board (collection `dec`) and found three differences from the code: `b_stats` on the board has no CV2 (the AI's chat summary had wrongly said the recommendation included it), `b_axis` bins are 1 ms to 1 s (code had up to 3 s), `b_fano` windows are 50 to 1000 ms (code had 10 ms to 10 s). The student chose to follow the board; the code was corrected. Then added one comparison figure (three ISI distributions on shared axes) and a numbers table for a 5 s and a 200 s recording.
- **Decisions applied:** `b_figs` (comparison figure, table; the construction diagram is postponed because Part 1's model decisions are not made), `b_stats` (six measures, no CV2), `b_axis`, `b_fano`.
- **How it was verified:** table checks (rates within 1 Hz of 10 on 200 s; CV and LV increase from regular to random to bursting; no CV2 column); the AI looked at the figures.
- **What went wrong:** the first comparison figure used `density=True` with log-spaced bins, which inflated the narrow short-interval bins and made the bursting peak look huge; changed to the fraction of intervals per bin. The count of intervals outside 1 ms to 1 s showed that 18% of the stand-in bursting intervals are below 1 ms (no refractory period in the stand-in).
- **Not done yet:** the construction diagram, and re-running on Part 1's simulation.

### 2026-11-25, task `t_q1d` (Q1 D, realizations), step 1: variability between realizations

- **What the AI did:** added a raster of 5 realizations per neuron, 1,000 realizations of 5 s with four properties each, a box plot with all points, and a table of median and 5th to 95th percentile per neuron and property, with a check of whether the three ranges overlap. Still on the stand-in neurons.
- **Decisions applied (read from the board):** `d_n` (5 + 1,000), `d_props` (spike count, CV, LV, short-interval fraction), `d_plot` (box plot with all points).
- **How it was verified:** exactly 1,000 runs per neuron and no `nan`; medians agree with the long-recording table of Q1 B step 4 (CV about 0.2, 1, 2.8); the AI looked at both figures.
- **Not done yet:** classification rule on new simulations (`d_cls`) and accuracy by recording length (`d_dur`).

### 2026-11-25, task `t_q1d` (Q1 D, realizations), step 2: classification rule and recording length

- **What the AI did:** set two thresholds (CV and short-interval fraction) from the 1,000 training runs of step 1, wrote a three-way rule, tested it on 3,000 new runs with other seeds (confusion matrix), and measured accuracy for 1, 2, 5, 10 and 30 s recordings (500 new runs per neuron per length). Still on the stand-in neurons.
- **Decisions applied:** `d_cls` (2-D view + simple threshold rule, evaluated on new simulations), `d_dur` (accuracy by length, one figure).
- **How it was verified:** small tests of the rule on obvious values; test seeds differ from training seeds; 3,000 test rows; the AI looked at both figures.
- **What went wrong:** the 1 s runs crashed the stand-in bursting generator when no burst started (`np.concatenate` of an empty list); the stand-in now returns an empty spike train. The first accuracy figure had its legend over the lines; moved.
- **Caveat recorded in the notebook:** 100% accuracy at 5 s reflects how different the stand-ins are; thresholds and accuracy must be recomputed on Part 1's simulation.

### 2026-11-25, tasks `t_q1b` and `t_q1d`: automatic switch to Part 1's simulation, figure saving

- **What the AI did:** the stand-in cell now checks whether `q1_models.py` contains the four contract functions (`make_rngs`, `simulate_regular`, `simulate_irregular`, `simulate_bursting`). If it does, every cell runs on Part 1's simulation through one function `make_trains(T, seed)`; if not, the stand-ins are used. Added `save_fig()` (decision `g_figs`: PNG, 200 dpi, to `figures/`), called for all 11 figures, which saves only when the data are real, never the stand-ins.
- **How it was verified:** the notebook runs unchanged on the stand-ins (prints the data source, saves nothing). In a separate temporary folder, outside the repository, with a FAKE `q1_models.py` that follows the contract (written by the AI only for this test and then deleted), the whole notebook ran without errors, printed "Part 1's simulation", and saved the 11 PNG files.
- **For Part 1:** the signatures must match the contract in `team_kit/CLAUDE.md` (`make_rngs(seed, n)`, `simulate_*(T, rng, rate_hz=...)`), and `simulate_bursting` must return an empty array when no burst starts in a short recording.
- **Still needed after Part 1 delivers:** re-read every interpretation cell, because all numbers in them come from the stand-ins.


### 2026-11-28, task `t_q1b`: CV2 removed from `q1_stats.py`

- **What the AI did:** at the student's decision, deleted `cv2` from `q1_stats.py` and from the notebook (import, hand-computed test, regular and Poisson tests, edge-case loop, interpretation text, and the "no CV2 column" check). LV stays as the single neighbouring-interval measure.
- **Why:** CV2 and LV both compare neighbouring intervals and give almost the same answer on our constant-rate neurons (Poisson: 1.001 for both). CV2 was never in the numbers table (the board's `b_stats` did not include it), so it was only used in tests.
- **How it was verified:** all code cells of `Q1_part2_analysis.ipynb` run from start to end on the stand-in neurons with every assert passing; no mention of `cv2` remains in the code or notebook.
- **What is not done:** the Hebrew explanation files outside git (`explain_decisions_he.md`, the Claude Docs knowledge doc) may still mention CV2.

- **Rename (2026-11-28):** `isi_lag1_corr` was renamed `next_interval_corr` (the name was unclear to the student) in `q1_stats.py` and the notebook; behaviour unchanged.
- **Rename (2026-11-28):** `burst_fraction` was renamed `short_isi_fraction` (it measures short intervals, not proven bursts); behaviour unchanged.
- **Rename (2026-11-28):** `burst_curve` renamed `short_isi_curve` to match `short_isi_fraction`; behaviour unchanged.
