# AI log, Part 1

Temporary. At integration the content is merged into the shared `AI_USAGE.md`, under the same heading.

For every task add: date, task id, what the AI did, what the student decided, how it was verified, anything that went wrong. Keep it accurate. Section 9 of AI_USAGE.md (an example you challenged or corrected) is written by the student, never by the AI.

**Tool:** Claude Code (Claude Opus 5.5), desktop app. Work started in a local folder (no access to this repository yet) and was moved here on 28.11.

## Entries

| Date | Task | What the AI did | What the student decided / changed | How it was verified |
|---|---|---|---|---|
| 27.11 | `t_setup` | Local venv, pinned `requirements.txt`, folders | – | All packages import; a seeded random draw runs |
| 27.11 | `t_q1a` regular neuron | Gamma renewal process: ISI = 2 ms + Gamma(k = 400), mean 100 ms; `SeedSequence.spawn` seeds; `assert` validation | Asked for the first, dense version to be rewritten in short numbered sections with Decision / Why text and a comment on every line; then edited the comments herself | 50 spikes (≈50 expected), mean ISI 100.2 ms, CV 0.046 vs theory 0.049 |
| 27.11 | `t_q1a` irregular neuron | Same building blocks with k = 1 (exponential ISIs) | – | One run gave only 37 spikes. Checked it is not a bug: 5000 runs gave mean 50.7 spikes (SD 7.0), 2.7 % of runs had ≤ 37 |
| 27.11 | `t_q1a` bursting neuron | Burst-by-burst loop: n = 2 + Poisson(2) spikes, intra-burst ISI 2 ms + Gamma (mean 5 ms, CV 0.2), quiet period 50 ms + Gamma(k = 4), mean 385 ms so the rate stays 10 Hz | – | Tested on a copy first. Log-axis ISI histogram bimodal (~5 ms and ~400 ms, empty gap). 2000 runs: mean 50.3 spikes, mean CV 1.90 |
| 27.11 | `t_q1a` parameter table + combined raster | Table (deterministic / stochastic), raster of the 3 neurons with fixed colours, PNG 200 dpi | The first zoom panel (first 1 s) still showed each burst as one thick line; changed to a 100 ms window around the first burst | PNG written; the burst's individual spikes are visible |
| 28.11 | `t_q1c` temporal checks + reproducibility | 1000 realizations per neuron, criteria written before running, summary table | – | All pass. Checked that the checks can fail: the regularity test rejects the irregular neuron (85 % of ISIs outside 80–120 ms); a bursting model without the 50 ms minimum quiet period gives 21 ISIs in the 20–50 ms zone, so check C2.3 fails |
| 28.11 | `t_q1c` choice of checks | Proposed dropping the KS test and the zero/one-spike check to save time | Did not accept: kept KS (the only check of the distribution's shape, not just mean and CV) and folded zero/one spikes into the duration edge case. One redundant check removed | – |
| 28.11 | `t_q1c` statistical + edge-case checks | k scan (CV ∝ 1/√k), KS per realization, recording duration 10 ms – 500 s | Three main checks marked at the top of Q1 C (temporal C2.2, statistical C4.1, edge case C5) | k scan passes for all 5 k. Pooling all ISIs into one KS test fails (p = 7e-7) because the 5 s window shortens measured ISIs; KS per realization passes. The duration check **failed** at 5 s (10.16 Hz) – see next row |
| 28.11 | `t_q1a` burn-in fix (changes decision `a_start`) | Found the cause: a first spike uniform in [0, 100 ms) is right for the regular neuron but too early on average for the irregular one (+0.5 spike per recording: 10.10 Hz at 5 s, 10.99 Hz at 0.5 s, 20 000 runs). Proposed a 2 s burn-in | Chose to fix the model rather than only document it | With burn-in: 9.99 Hz (20 000 runs); all 20 checks pass, 10.01 Hz at 5 s |
| 28.11 | Move to this repository | Functions moved to `q1_models.py` with the contract signatures (`make_rngs(seed, n)`, `simulate_*(T, rng, rate_hz=...)`); the two local notebooks merged into `Q1_part1_models_validation.ipynb` | – | New module gives spike trains identical to the old notebook code (4 durations × 200 seeds × 3 neurons); the merged notebook runs from scratch, 20 / 20 checks pass with the same numbers |
| 28.11 | Contract test with Part 2 | Ran `Q1_part2_analysis.ipynb` on a copy of the repository | – | It switches to "Part 1's simulation" and runs, except one sanity check in Part 2's cell 16: `np.all(curves["Bursting"] > 2)`. Our bursting neuron's Fano factor falls from ~3.3 (50 ms window) to ~1.2–1.5 (1 s), because burst onsets are quasi-regular (decision `a_bo`, k = 4). The stand-in had Poisson onsets. Reported to Part 2; Part 2's file not edited |
| 28.11 | `t_q1int` Q1 interpretation (decision `d_report`) | Drafted the interpretation chapter (6 short parts: assumptions, rate alone, what distinguishes, variability, how to tell apart from observations, trustworthiness and limits) and a code cell that computes the numbers it quotes | – | Before writing, ran Part 2's notebook on the real models (on a copy): CV 0.05 / 0.95 / 1.89, its threshold rule 100 % correct on 3,000 new 5 s runs. Every number in the text matches the table computed in the notebook; notebook runs from scratch, 20 / 20 checks pass |
| 28.11 | `t_q2e` Q2 report (decisions `r_form`, `r_struct`, `r_lim`, `g_verify`) | First proposed typing the report as text with an `assert` to warn when numbers change | **Asked for the text to update itself instead.** The AI then wrote every paragraph with numbers as code that builds the text from Part 3's results (`IPython.display.Markdown`), with wording chosen by rules (e.g. "clear premium" only if the whole interval is above 1) and `assert`s for claims a rule cannot rephrase; an explanation of this choice is at the top of the report. Summary, 4 findings (observed / supported / cannot conclude, with figures), limitations, README draft | Ran Part 3's notebook on a copy and read its result tables before writing. Report runs from scratch with no errors. Helper functions tested on known inputs. One generated sentence was wrong at first: the "small groups" list showed only 2 GB, because it read the table where 24/32/64 GB were already merged; changed to the original RAM-level table |

## Section 9 draft (written by the student)

*Written by the student in Hebrew; translated to English with AI. To be moved into section 9 of `AI_USAGE.md` at integration.*

**Example 1: the report text**
- The AI suggested writing the report as fixed text, with a check that warns when a number changes; but when the data change, the text itself does not change.
- What bothered me: if something changes, nothing in the text changes and it stays exactly the same, so the text can become wrong after the data change.
- I suggested making the text change dynamically.
- The result is code that changes dynamically and prints the text according to the results of the analysis.
- The AI suggested a warning that pops up a note when the analysis changes, but that was not enough for me: I wanted the text to change dynamically and work by itself.

**Example 2: the number of checks**
- The AI suggested a long list of checks, 9 checks on the board, more than required, and a long implementation.
- What bothered me: it suggested things that might be unnecessary and add no value.
- I suggested sticking to the requirements of the assignment and not overloading the code.
- The result: three main checks marked at the top of the notebook, one of each type the assignment requires. All the others are defined as supporting checks, and one unnecessary check was deleted.
- The AI suggested dropping the KS test and the zero/single-spike check as well. Here I stopped it and asked whether these were important; that is, it wanted to cut important things too, so I kept the KS test.
