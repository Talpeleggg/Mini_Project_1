# MY_PART.md: Part 3 (about 35 points)

**Scope:** the Q2 analysis, outliers, and the final integration and submission.

| Task id | Task | Weight | Depends on decisions (board ids) | Needs from others |
|---|---|---|---|---|
| `t_q2c` | Q2 C: analytical questions (RAM vs price is required) | 22 | `qs tr ram_rep ram_m viz g_test g_n q_tpl` | P2's `load_clean()` (`t_q2b`) |
| `t_q2d` | Q2 D: outliers | 5 | `o_def o_other o_treat` | P2's cleaned data |
| `t_final` | README, merged AI_USAGE, clean-environment run, structure check | 8 | `s_ai s_dec s_readme s_final` | everyone's parts |

**You provide to others:** your results to P1, who writes the Q2 report (E) from them. Put key numbers in clearly labelled variables or a small results table so they are easy to quote.

**Your files (temporary, in `parts/`):** `Q2_part3_analysis.ipynb` and `ai_log_part3.md`. Mark your cells with `[P3]`. Push straight to `main` (`git pull --rebase` first); never edit other people's files. At integration your cells go into `Q2_laptop_analysis.ipynb` (C and D come after P2's cleaning cells). In the final stage you also run the integration (planned 28.11): paste every part's cells into the two final notebooks, run both from scratch in a fresh environment, merge the AI logs into `AI_USAGE.md`, write the README, and delete `parts/`.

## What good looks like

- **C (questions):** at least three questions and at least two different kinds of analysis (the board proposes RAM vs price, SSD vs HDD, and brand premium). For each: why it is interesting, which variables and rows, which method, one figure, an interpretation. Use log price (decision `tr`), RAM as log2 for correlation and regression (decision `ram_rep`), Spearman plus Pearson on the log scale plus an adjusted regression (decision `ram_m`). Show how much of the raw RAM-price association remains after adjusting for CPU tier, laptop type, SSD, screen resolution and brand; this separates correlation from causation. For group comparisons use a rank-based test with an effect size and a confidence interval, Holm correction for several comparisons, and a minimum group size (decisions `g_test`, `g_n`). With about 1275 rows every difference is "significant", so emphasize effect sizes. The near-duplicate rows are not independent: run a sensitivity check without them.
- **D (outliers):** define what an outlier is and which method finds it (decision `o_def`); the count depends on the scale (28 on raw price, 1 on log price by the 1.5 IQR rule, from the first look). Decide whether each unusual value is an error or a real extreme (high-end gaming and workstation laptops are real). Do not remove them automatically: compare Spearman, the regression slope and medians before and after, and report the difference (decision `o_treat`).
- **Final:** README with install and run instructions, repo layout, key findings and design decisions (decision `s_readme`, `s_dec`); `AI_USAGE.md` merged from everyone's entries, accurate to what was really done; both notebooks run from scratch in a fresh virtual environment from `requirements.txt` (decision `s_final`); the repository tree matches the required structure exactly; every figure the notebooks mention exists in `figures/`.

## Things to double check (unverified claims, verify in code)

- Spearman about 0.76 and Pearson about 0.74 between RAM and price (computed once; recompute in the notebook).
- RAM levels with few laptops (2 GB: 16, 24 GB: 3, 64 GB: 1) need special handling in plots and tests.
- Brand comparisons: only brands with enough laptops (decision `g_n`).

## Reading your decisions (do this before writing code)

On the board your page is "Part 3" (default name: Ohad). Your own decisions are on that page; the shared ones are on the "shared" page. Two ways to give them to Claude:
1. On your page press "העתק את ההחלטות שלי ל־Claude" and paste the result in the chat. It contains your tasks, what was decided, what is missing, and the related shared decisions.
2. If your Claude can read the shared board, read the database collection `dec` of the board artifact (one document per decision id; fields: `choices`, `labels`, `q`, `note`, `owner`, `task`, `by`) and `tasks` (one document per task id; fields: `status`, `part`, `notes`).
A decision marked "לא הוחלט" is not decided: ask the student, do not pick for them.

## Your AI log

After each task add an entry to `parts/ai_log_part3.md` (merged into `AI_USAGE.md` at integration): what Claude did, what you decided, how you verified it, what went wrong. Section 9 (the example you challenged) must be yours. As integrator, do not remove or soften other people's honest entries.
