# AI log, Part 3

Temporary. At integration the content is merged into the shared `AI_USAGE.md`, under the same heading.

For every task add: date, task id, what the AI did, what the student decided, how it was verified, anything that went wrong. Keep it accurate. Section 9 of AI_USAGE.md (an example you challenged or corrected) is written by the student, never by the AI.

## Entries

### 2026-11-25, task `t_q2c`, step C0 (setup and variable check)

- **What the AI did:** read the decision board and Part 2's cleaning code, then wrote the setup cells of `Q2_part3_analysis.ipynb`: loading `load_clean()`, an `assert` check that the columns we rely on exist and have no missing values, the new column `RAM_log2`, and a table of RAM levels with counts. Also created the virtual environment from `requirements.txt`.
- **What the student decided:** the Part 3 decisions on the board (`qs`, `tr`, `ram_rep`, `ram_m`, `viz`, `g_test`, `g_n`, `q_tpl`, `o_def`, `o_other`, `o_treat`), all choosing the board's recommended option. The student asked for a Hebrew explanation of the reason behind each choice. The student also noticed that `g_style` and `g_verify` have Q1-style examples but apply to Q2 too.
- **How it was verified:** the notebook was run from top to bottom in a copy; the checks passed (1275 rows, 32 columns, no missing values, `RAM_log2` equals 1, 3 and 6 for 2, 8 and 64 GB). The RAM level counts match Part 2's audit (2 GB: 16, 24 GB: 3, 32 GB: 17, 64 GB: 1).
- **What went wrong:** nothing yet. Open point: the board says RAM levels with fewer than 20 laptops are "flagged or merged"; the AI did not choose, and only flagged them. The merge decision is left for the box plot step.

### 2026-11-25, task `t_q2c`, step C1 (RAM and price, raw association)

- **What the AI did:** wrote the question 1 headings (why interesting, variables and observations, method) and one code cell computing Pearson on raw values, Pearson on the log-log scale, and Spearman.
- **What the student decided:** the method (`ram_m`: Spearman and Pearson on log-log, then OLS with controls); the student also chose to push directly to `main`, as the team agreed, after asking the AI to check how Tal pushes.
- **How it was verified:** every coefficient is computed in the notebook, not typed by hand. Two checks in the code: Spearman is the same on the raw and on the log scale (the log keeps the order), and Pearson matches an independent `numpy.corrcoef`. The results (raw Pearson 0.740, log-log Pearson 0.771, Spearman 0.764) agree with the unverified numbers in the team notes (about 0.74, 0.77 and 0.76), which are now confirmed in code.
- **What went wrong:** nothing in this step. Side note: the student expected that Tal pushed through branches; the AI checked the git history and found that all her commits are directly on `main`, which is the team rule, so no change in method was needed.

### 2026-11-25, task `t_q2c`, step C2 (RAM and price, regression with controls)

- **What the AI did:** wrote small OLS helper functions with `numpy` (design matrix, least squares fit, bootstrap confidence interval) and six models that add controls one group at a time (CPU tier, laptop type, SSD, resolution, brand). `statsmodels` is not in `requirements.txt`, so no new package was added.
- **What the student decided:** the method (`ram_m`) and the list of controls. The student did not choose the details below; they are AI choices to confirm or change: resolution enters as megapixels in a straight line, the baseline brand is Acer (first alphabetically), the bootstrap uses 1,000 resamples and a fixed seed, and the models are added in the order CPU tier, laptop type, SSD, resolution, brand.
- **How it was verified:** the helpers were tested on data with a known answer (y = 1 + 2x gives coefficients 1 and 2 and R2 of 1) and on the real data (the one-variable slope equals the Pearson correlation times the ratio of standard deviations). Model 0 agrees with that check. All numbers are computed in the notebook.
- **Result (to be interpreted later, not yet in the report):** the RAM coefficient per doubling falls from 0.641 (about +90% in price) with no controls to 0.301 (about +35%, 95% bootstrap interval about 30% to 40%) with all controls.
- **What went wrong:** nothing in this step.

### 2026-11-25, task `t_q2c`, step C3 (RAM and price, scatter figure)

- **What the AI did:** wrote the section "Figure: RAM against price": the merge of RAM levels 24, 32 and 64 GB into a "24+" group, a table of the groups, and the scatter figure (jitter, median line per group, log price axis), saved to `figures/` at 200 dpi, with a caption under it.
- **What the student decided:** the figure rules (`g_style`: axis names with units, same limits when comparing, a caption, a readable font) and how to treat the rare RAM levels. The student first asked which option is statistically better and what each loses; the AI explained that no data is lost either way (the choice is detail against reliability of the summary), recommended the merge, and the student accepted the recommendation.
- **How it was verified:** the notebook checks that no laptop is lost in the grouping (the counts add up to 1,275) and that the "24+" group has exactly 21 laptops. The caption numbers (498, 1,895 and 3,073 euro) come from the group table printed in the notebook.
- **What went wrong:** the first version of the figure had overlapping tick labels (the `n=` counts under the RAM levels), clutter from small tick labels on the log axis (such as 6x10^3), and a text note placed far from the line it described. We looked at the figure, found these and fixed them. A first run also failed on a broken string in a notebook cell (a line break inserted by the AI's own script in an f-string); fixed, and the notebook now runs.

### 2026-11-25, task `t_q2c`, step C3 follow-up (price labels on the figure)

- **What the AI did:** at the student's request, added the price in euro above each median line of the RAM scatter figure (only the specific values, no extra grid lines), and added the group mean to the printed group table for comparison.
- **What the student decided:** to label the lines with their price in euro. The student wrote "average price"; the lines in the figure are medians (decision `viz`), so the AI labelled the median and pointed out that the mean is slightly different (for example 4 GB: median 498, mean 576 euro). Whether to show the mean instead, or both, was left to the student.
- **How it was verified:** the labels come from the same table that draws the lines (printed in the notebook), and the figure was inspected by eye after the change.
- **What went wrong:** nothing.

### 2026-11-25, task `t_q2c`, step C4 (RAM and price, box plot)

- **What the AI did:** wrote the "box plot by RAM level" section: the quartiles table per RAM group, the box plot (same groups, same price range and ticks as the scatter figure, median price written next to each box, the 2 GB group dashed in red), the median ratios for doubling RAM, and a caption. Saved to `figures/q2_ram_vs_price_boxplot.png` at 200 dpi.
- **What the student decided:** to keep the median price written next to the lines (the AI had compared this with putting the values on the price axis and recommended the labels next to the lines); the student also made clear that the intended statistic was the median, not the mean.
- **How it was verified:** the figure was inspected by eye. The caption's numbers (the quartiles of the 4, 6, 8 and 12 GB groups and the ratios 2.2 and 1.7) come from the tables printed in the notebook, not from memory.
- **What went wrong:** nothing in this step. Note for the final merge: the figure code reuses variables from the scatter section (`groups`, `order`, `FIG_DIR`, `PRICE_YLIM`, `NullFormatter`), so the two sections must stay in this order.

### 2026-11-25, task `t_q2c`, step C5 (SSD vs HDD, test and effect size)

- **What the AI did:** wrote the headings of question 2 (why interesting, variables and observations, method) and the code for the comparison of SSD-only and HDD-only laptops: a function for the rank-biserial effect size with three checks, the Mann-Whitney test, bootstrap intervals (2,000 resamples, fixed seed) for the effect size and for the ratio of the median prices, and a descriptive table of every storage type.
- **What the student decided:** the method (`g_test`, `g_n`); and which groups to compare. The board did not say. The student asked for an explanation of the Holm correction and of what is best; the AI explained and recommended SSD-only against HDD-only as the tested comparison, with the mixed `SSD + HDD` and `Flash Storage` groups shown for context but not tested; the student chose that.
- **How it was verified:** the effect size function passes three checks: a toy example with a known answer (8/9), a direct count over all pairs of laptops, and `scipy`'s Mann-Whitney U statistic. Every number is computed in the notebook.
- **Result (to be interpreted later):** SSD-only median 1,197 euro and HDD-only median 598 euro; ratio about 2.0 (interval about 1.87 to 2.18); rank-biserial 0.674 (interval 0.625 to 0.722).
- **What went wrong:** nothing in this step. The Holm correction is not applied here, because there is a single comparison; it will be used in the brand question.

### 2026-11-25, task `t_q2c`, step C6 (SSD vs HDD, figure)

- **What the AI did:** wrote the section "Figure: price by storage type": a box plot of all five storage groups with the same price range and ticks as the RAM figures, the tested groups (SSD-only, HDD-only) in blue, the context groups in grey, the group under 20 laptops dashed and red, the median in euro next to each box, and a caption. Saved to `figures/q2_ssd_vs_hdd_boxplot.png` at 200 dpi. The title quotes the result table computed earlier.
- **What the student decided:** to show the mixed `SSD + HDD` and `Flash Storage` groups for context only, without a test (decided in the previous step); the figure rules from `g_style`.
- **How it was verified:** the figure was inspected by eye. The medians and quartiles in the caption come from the storage table printed in the notebook.
- **What went wrong:** nothing in this step. The caption says that the reason for the low price of Flash Storage laptops was not checked; it is not claimed.

### 2026-11-25, task `t_q2c`, step C6 follow-up (figure split in two panels)

- **What the AI did:** at the student's suggestion, split the SSD vs HDD figure into two panels with a shared price axis: the main finding (SSD-only against HDD-only) on the left, drawn larger and in blue, and the supplementary groups (`SSD + HDD`, `Flash Storage`, `Other storage`) on the right, in grey and not tested. The notebook text and the caption were updated to describe the two panels.
- **What the student decided:** the split and the emphasis; the design idea was the student's.
- **How it was verified:** the figure was inspected by eye after the change; both panels use exactly the same price range because they share the axis (decision `g_style`).
- **What went wrong:** nothing in this step.

### 2026-11-25, task `t_q2c`, step C7 (brand premium, raw comparisons)

- **What the AI did:** wrote the headings of question 3 (why interesting, variables and observations, method), a table of the brands, a Holm correction function, a function that compares two groups (medians, ratio of medians, rank-biserial effect size, bootstrap intervals, Mann-Whitney p-value), and the four comparisons: Apple and MSI, each against Acer and Lenovo.
- **What the student decided:** the method (`g_test`, `g_n`); and which comparisons to make. The board did not say. The AI offered three designs (four pairs, all eight brands against Acer, or two pooled comparisons) and the student chose the four pairs.
- **How it was verified:** the Holm function was checked against a hand calculation (p-values 0.01, 0.04, 0.03 give 0.03, 0.06, 0.06), and the comparison function on two groups with a known answer (effect size 1 and ratio 10). Every number is computed in the notebook.
- **Result (to be interpreted later):** raw median ratios against Acer are 2.34 (Apple) and 2.80 (MSI), and against Lenovo 1.49 (Apple) and 1.78 (MSI); the rank-biserial values are 0.92, 0.48, 0.93 and 0.58. All four Holm-corrected p-values are below 0.001. Apple has only 21 laptops, so its intervals are wide. MSI has the highest median of all brands (1,599 euro), above Apple (1,340 euro).
- **What went wrong:** the first version of the Holm test had a wrong expected value that I (the AI) wrote by hand: for p-values 0.5 and 0.9 I expected 1.0 and 0.9, but Holm never lets the corrected values go down, so the right answer is 1.0 and 1.0. The test failed, I checked the function against the definition, found that the function was right and the test expectation was wrong, and corrected the test.

### 2026-11-25, task `t_q2c`, steps C8 and C9 (brand after controls, figure, sensitivity, interpretations)

- **What the AI did:** wrote the regression of `log_price` with brand as a control and turned the brand coefficients into four adjusted price ratios (Apple and MSI against Acer and Lenovo) with bootstrap intervals; a two-panel figure (raw against adjusted ratios, and the price of the four brands) with a caption; a sensitivity table that recomputes the key numbers of the three questions without the 48 near-duplicate rows; and the interpretation text of the three questions, in three parts: what we observed, what the analysis supports, and what we cannot conclude.
- **What the student decided:** the method of the question (`g_test`, `g_n`) and the four pairs (previous step); the figure layout (main finding emphasised, as in the SSD figure). The student must read the interpretation texts and change anything they do not agree with: they are drafts written by the AI, and the student is responsible for being able to explain them.
- **How it was verified:** the contrasts between brands were checked against a refit that uses Lenovo as the baseline (the coefficients agree to 1e-9). Every number in the interpretation texts was compared by hand with the tables printed in the notebook. The sensitivity table shows that no key number changes materially when the near-duplicate rows are removed (largest change: the RAM effect per doubling, 35.1 percent against 35.8 percent).
- **What went wrong:** the first version of the brand figure drew no intervals for the raw ratios. My code used a wrong column name inside a condition that silently skipped the intervals instead of failing. The figure was inspected by eye, the missing intervals were noticed, and the code now uses the right names. The legend also covered one label, and the axis cut another; both were fixed.

### 2026-11-26, task `t_q2d`, steps D1 and D2 (outliers: Tukey fences and residuals)

- **What the AI did:** wrote the opening of the outlier section (the decisions, the definition of an outlier, conditional against unconditional); the Tukey fences on the log price; and the diagnostics of the specification model: leverage, standardized residuals and Cook's distance, written with `numpy` and tested.
- **What the student decided:** the methods (`o_def`: Tukey on log price and residuals from a specification model); and which variables the specification model uses: the specification only, without the brand (RAM as log2, SSD, resolution, CPU tier, laptop type). The board did not say this, so the AI explained the options in Hebrew and the student chose. The student had first pointed out that the AI had not explained the question and how to approach it.
- **AI choices to confirm or change:** the standardized residual is the internally studentized version (it divides by the leverage too); the threshold for a large Cook's distance is `4 / n`; the resolution enters as megapixels in a straight line.
- **How it was verified:** the Tukey function on a toy example with a known answer, and against `pandas.quantile`; the leverage on a toy regression with known values (0.6, 0.3, 0.2, 0.3, 0.6), the fact that the leverages add up to the number of parameters, and a direct calculation with the pseudo-inverse on the real model. All numbers are computed in the notebook.
- **Result (to be interpreted later):** Tukey on log price flags one laptop (Razer Blade Pro, 6,099 euro). The residual rule flags seven laptops (six more expensive than expected, one cheaper), none of them flagged by Tukey. Six are HP, Dell or Lenovo laptops with names that suggest business or workstation lines; we have not checked this, so it is only a guess. 68 laptops are above the `4 / n` rule of thumb for Cook's distance.
- **What went wrong:** nothing in these steps.

### 2026-11-26, task `t_q2d`, step D3 (outliers that are not about price)

- **What the AI did:** wrote the three checks of decision `o_other`: physical fit (a regression of weight on screen size and laptop type, flagging a standardized residual above 3 in absolute value), rare configurations and their leverage (RAM of 24 GB or more, or a CPU or GPU model that appears in no other laptop), and the price spread within the same configuration (the near-duplicate rows).
- **What the student decided:** to do these three checks (`o_other`), after asking the AI to explain the absolute value and the threshold 3 of the residual rule; the AI explained that the absolute value catches both sides and that 3 is a rule of thumb (about 3.4 laptops in 1,275 by chance if the residuals were normal).
- **AI choices to confirm or change:** the weight model is linear in screen size plus laptop type, and uses the same threshold 3 (the board did not set a rule for weight); what counts as a rare configuration; the leverage threshold `2 * k / n`.
- **How it was verified:** the weight model reuses the diagnostics already tested in the previous step; the near-duplicate groups are checked against Part 2's flag (the same 48 laptops). All numbers are computed in the notebook.
- **Result (to be interpreted later):** 31 laptops are flagged by weight, almost all 17-inch gaming laptops of 4.2 to 4.7 kg, many of them repeated listings of the same model (for example Alienware 17). That is about ten times more than the 3.4 expected by chance, so the residuals are not normal and the weight model is simple; these laptops are heavy for real, not errors. Two Alienware 17 rows have a screen of 15.6 inches or the type Notebook, which does not fit the model name; we have not checked this. Laptops with 24 GB or more RAM have a higher leverage than the others (a third of them above the threshold), but the five highest-leverage laptops are workstations and business laptops that fit the model well. The price spread inside the same configuration is small (median ratio 1.09, the largest 1.72, Yoga Book 319 against 549 euro): the spread of the log price is 0.124 inside a configuration against 0.282 left unexplained by the specification model.
- **What went wrong:** nothing in this step.

### 2026-11-26, task `t_q2d`, step D4 (before and after removing the unusual observations)

- **What the AI did:** answered the student's question about two suspicious Alienware 17 rows (a screen of 15.6 inches and the type Notebook, against 17.3 inches and Gaming in the other rows of the same model): the values are in the raw file unchanged, `clean()` keeps the original columns and removes no rows, and Part 2's audit did not compare the screen size or the type with the model name, so this is a gap in the checks and not a cleaning mistake. Then wrote the before-and-after comparison of decision `o_treat`: for six scenarios, the mean and median price, Pearson (raw and log-log), Spearman and the regression coefficient of RAM.
- **What the student decided:** to keep the unusual observations in the main analysis and compare (`o_treat`). The student asked whether the two rows come from a mistake of Part 2's cleaning; the answer is no.
- **AI choices to confirm or change:** the six scenarios (all laptops; without the Tukey outlier; without the residual outliers; without both; without the 64 GB laptop; without all 24+ GB laptops) and the choice to show Pearson on both the raw and the log-log scale.
- **How it was verified:** the row counts of the scenarios are asserted (1,275, 1,274, 1,268, 1,267, 1,274, 1,254), and the "all laptops" column is asserted to match the Spearman and the RAM effect computed in question 1. All numbers are computed in the notebook.
- **Result (to be interpreted later):** the key numbers hardly change. Removing the Tukey and residual outliers changes the median price by at most 9 euro, Spearman by 0.001 and the RAM effect from 35.1 to 32.6 percent per doubling. The largest change is when the 21 laptops with 24 GB or more are removed: Pearson on raw values drops from 0.740 to 0.711, and the RAM effect to 32.1 percent. The mean price moves more (from 1,135 to 1,121 euro without the outliers) than the median (from 989 to 980).
- **What went wrong:** nothing in this step. We have not verified with an external source that the two Alienware rows are errors; this is a hypothesis.

### 2026-11-26, task `t_q2d`, step D5 (interpretation of the outlier section)

- **What the AI did:** wrote the interpretation of Q2 D in three parts: what we observed, what the analysis supports, and what we cannot conclude.
- **What the student decided:** to keep the unusual observations in the analysis (`o_treat`). The student must read the text, change anything they do not agree with, and be able to explain it: it is a draft written by the AI.
- **How it was verified:** every number in the text was compared by hand with the tables printed in the notebook (the fences, the counts of flagged laptops, the before-and-after table, the leverage shares, the price ratios and the two spreads of the log price).
- **What went wrong:** nothing in this step. The statement about the two Alienware rows is a hypothesis (comparison with other rows of the same model) and is written as one.
