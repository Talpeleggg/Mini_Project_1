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

