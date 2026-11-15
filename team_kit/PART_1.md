# MY_PART.md: Part 1 (about 36 points)

**Scope:** Q1 neuron models and validation, the Q1 wrap-up, the Q2 report, and the general setup.

| Task id | Task | Weight | Depends on decisions (board ids) | Needs from others |
|---|---|---|---|---|
| `t_setup` | environment, repo layout, general conventions | 3 | `g_lang g_nb g_figs g_out g_code s_env s_repo` | none |
| `t_q1a` | Q1 A: the three spike models | 10 | `a_rate a_reg a_irreg a_refr a_bn a_bi a_bo a_start a_valid a_seed` | none |
| `t_q1c` | Q1 C: validation checks | 8 | `c_checks c_reps c_crit` | P2's statistics functions (`t_q1b`) |
| `t_q1int` | Q1 wrap-up: assumptions table, interpretation, clean run | 7 | `d_report` | P2's results (`t_q1d`) |
| `t_q2e` | Q2 E: short report (observed / supported / cannot conclude) | 8 | `r_form r_struct` | P3's results (`t_q2c`, `t_q2d`) |

**You provide to others:** the three `simulate_*` functions and `make_rngs` (P2 needs them for the analysis and realizations). Agree the signatures with P2 first (see CLAUDE.md contracts), and publish a first working version early, even if the parameters are still provisional.

**Notebook sections:** mark your cells with `[P1]`, in `Q1_neural_spikes.ipynb` (A, C, wrap-up) and the final section of `Q2_laptop_analysis.ipynb` (E).

## What good looks like

- **A (models):** every parameter documented in a table (value, role, deterministic or stochastic). Spike times are built as a cumulative sum of positive intervals and cut to `[0, T)`; `assert` on ordering, positivity, bounds and the minimum interval. One independent random stream per neuron. The reasoning for each modeling assumption is written in the notebook, in the student's own words.
- **C (validation):** at least one temporal check, one statistical check and one edge case, each answering a question that can have a wrong answer (not "the code runs"). The acceptance criterion is fixed before looking at results (decision `c_crit`). Examples already on the board: does the regular neuron really have near-constant intervals; do p-values of a KS test on the irregular neuron's intervals come out uniform over many realizations; do 0 or 1 spikes return `nan` instead of crashing; is the result identical for the same seed and different for another.
- **Wrap-up:** a short scientific interpretation that answers "how would you tell the three patterns apart from observations alone, without knowing how they were generated?"
- **Q2 E (report):** each finding has three lines: observed, supported by the analysis, cannot be concluded. State limitations: confounding (CPU, type, brand), near-duplicate rows are not independent, the collection date is unknown, prices are list prices.

## Things to double check (unverified claims from the board, verify in code)

- The bursting neuron (4 spikes per burst, 5 ms inside, 10 Hz overall) has an ISI CV near 1.6, LV near 1.4 and lag-1 correlation near -0.3.
- A 2 ms floor changes the Poisson CV only slightly (about 0.98).
- With Poisson at 10 Hz about 9.5% of intervals are below 10 ms and 18% below 20 ms.
- A fixed-start versus a random-offset start changes spike counts for the regular neuron.

## Reading your decisions (do this before writing code)

On the board your page is "Part 1" (default name: Shahar). Your own decisions are on that page; the shared ones are on the "shared" page. Two ways to give them to Claude:
1. On your page press "העתק את ההחלטות שלי ל־Claude" and paste the result in the chat. It contains your tasks, what was decided, what is missing, and the related shared decisions.
2. If your Claude can read the shared board, read the database collection `dec` of the board artifact (one document per decision id; fields: `choices`, `labels`, `q`, `note`, `owner`, `task`, `by`) and `tasks` (one document per task id; fields: `status`, `part`, `notes`).
A decision marked "לא הוחלט" is not decided: ask the student, do not pick for them.

## Your AI log

After each task add an entry to `AI_USAGE.md` under "Part 1": what Claude did, what you decided, how you verified it, what went wrong. Section 9 (the example you challenged) must be yours.
