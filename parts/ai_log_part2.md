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

