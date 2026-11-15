# MY_PART.md: Part 2 (about 32 points)

**Scope:** Q1 analysis and realizations, and the Q2 audit and cleaning.

| Task id | Task | Weight | Depends on decisions (board ids) | Needs from others |
|---|---|---|---|---|
| `t_q1b` | Q1 B: analysis and comparison (raster, ISI, statistics) | 15 | `b_figs b_axis b_bin b_stats b_thr b_fano` | P1's `simulate_*` functions (`t_q1a`) |
| `t_q1d` | Q1 D: new realizations, stability, how to tell patterns apart | 7 | `d_n d_props d_plot d_cls d_dur` | your own Q1 B |
| `t_q2a` | Q2 A: data audit | 5 | `q_data q_dups q_issues` | none |
| `t_q2b` | Q2 B: cleaning and new variables, with validation | 5 | `os_map st_type st_extra rare validate` | `t_q2a` |

**You provide to others:** the statistics functions (`isi`, `cv`, `lv`, `fano`, `burst_fraction`, `isi_lag1_corr`; P1 needs them for the validation checks) and `load_raw()`, `clean(df)`, `load_clean()` (P3 builds the whole analysis on them). Publish these first with the agreed names, even before they are polished.

**Notebook sections:** mark your cells with `[P2]`: Q1 sections B and D in `Q1_neural_spikes.ipynb`, and Q2 sections A and B in `Q2_laptop_analysis.ipynb` (they come first, before P3's analysis).

## What good looks like

- **B (analysis):** the figures and numbers answer the questions in the assignment: how each neuron distributes spikes over time, what a raster shows, what the ISI holds, how the ISI distributions differ, whether mean rate alone separates the neurons (use the same mean rate for all three), and which additional statistics help. Explain why each plot and statistic was chosen. ISI histograms on a log axis (decision `b_axis`). Every statistic returns `np.nan` when undefined, never an exception.
- **D (realizations):** many realizations (decision `d_n`) per neuron; show which properties are stable and which vary. Any threshold or rule for telling patterns apart must be fitted on one set of simulations and evaluated on fresh ones. Conclude with a plain explanation of how to distinguish the patterns from observations.
- **Q2 A (audit):** what a row means, the variables and types, missing values, duplicates (48 rows differ only by price, decision `q_dups`), units and plausibility of price, weight, size, RAM. Document each problem and say which ones you fix.
- **Q2 B (cleaning):** `macOS` and `Mac OS X` are the same system (decision `os_map`); build `Storage type` from `Memory` (handle double spaces, `1.0TB`, Flash Storage, Hybrid, and two-drive strings); add the extra columns chosen in `st_extra`. Keep the raw file untouched (`data/laptop_price_dataset.csv`); `clean()` returns a new table. **Validate the transformations, do not assume they worked:** a raw-to-clean cross-tabulation, assertions for no new NaN and no unmapped values, a second independent computation of capacity, and a spot-check of about 15 random rows (decision `validate`).

## Things to double check (unverified claims, verify in code)

- Sampling error of CV from N intervals is about `1/sqrt(2N)`.
- The 10 ms burst threshold captures almost every within-burst interval of the bursting model but about 9% of Poisson intervals.
- `Memory`: 39 distinct strings; TB to GB conversion (1000 vs 1024) must be stated and applied consistently.

## Your AI log

After each task add an entry to `AI_USAGE.md` under "Part 2": what Claude did, what you decided, how you verified it, what went wrong. Section 9 (the example you challenged) must be yours.
