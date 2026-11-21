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

