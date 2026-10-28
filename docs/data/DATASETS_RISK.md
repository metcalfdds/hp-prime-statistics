# Data sets for RiskLab (26 Oct 2026)

A companion to `DATASETS.md` (not edited). Same rule: two independent sources for every number,
the source line shown on screen, no invented data.

| File / where | What | Source to show | Check done |
| --- | --- | --- | --- |
| `compas_two_year_counts.csv` (typed into `rl_LoadCompas`) | Counts by COMPAS decile score (1-10) for the two largest groups in the file, as the file labels them: `African-American` (n 3,175; 1,661 re-arrested) and `Caucasian` (n 2,103; 822 re-arrested). `n` = defendants at that decile, `two_year_recid` = of them, a new arrest within two years | "ProPublica (Angwin et al. 2016), Broward, FL". Angwin J, Larson J, Mattu S, Kirchner L (2016) Machine Bias, ProPublica, 23 May 2016; data: github.com/propublica/compas-analysis, `compas-scores-two-years.csv` | See below: two routes agree cell by cell; N and the n-per-decile table equal ProPublica's printed numbers |
| `rossi.csv` (already in `DATASETS.md`): extra columns used | `wexp` 1 = full-time work experience before incarceration; `fin` was assigned at random ("Half the released convicts were assigned at random to an experimental treatment in which they were given financial aid"); `race`, `mar`, `paro` NOT used by RiskLab | R carData documentation of `Rossi` (Fox), citing Rossi, Berk & Lenihan (1980) and Allison (1995) | `rossi.csv` vs `carData_Rossi.csv`: fin 0/no 216, 1/yes 216; wexp 1/yes 247, 0/no 185; race 1/black 379; mar 1/married 53; paro 1/yes 267 (identical coding) |

## COMPAS: the filter and the checks

Filter (ProPublica's notebook `Compas Analysis.ipynb`, cell 4, applied to the 7,214 rows of
`compas-scores-two-years.csv`): `days_b_screening_arrest` between -30 and 30 (missing values dropped,
as R's `filter` drops NA), `is_recid != -1`, `c_charge_degree != "O"`, `score_text != "N/A"`.

| Count | Recomputed | ProPublica printed |
| --- | --- | --- |
| rows kept | 6,172 | 6,172 (notebook cell 4) |
| two_year_recid = 1 | 2,809 | 2,809 (cell 15; methodology article: "There were 2,809 defendants who recidivated within two years in this sample") |
| African-American / Caucasian | 3,175 / 2,103 | 3,175 / 2,103 (cell 9; article: "there were 3,175 black defendants and 2,103 white defendants") |
| n per decile, African-American | 365, 346, 298, 337, 323, 318, 343, 301, 317, 227 | identical (cell 19, `xtabs(~ decile_score + race)`) |
| n per decile, Caucasian | 605, 321, 238, 243, 200, 160, 113, 96, 77, 50 | identical (cell 19) |
| re-arrested per decile, African-American | 85, 105, 125, 158, 158, 187, 209, 215, 229, 190 | not printed by ProPublica |
| re-arrested per decile, Caucasian | 128, 100, 82, 98, 91, 93, 68, 72, 55, 35 | not printed by ProPublica |

The re-arrest counts were computed by two independent routes from the raw CSV, Python's `csv` module
row by row and pandas `groupby` (`build/RiskLab/tools/compas_counts.py`), which agree in every cell;
`verify_RiskLab_beta1.py` (Part A6) recomputes them a third time.

At ProPublica's cut-off (decile 5 and up = "medium" or "high"), this filtered file gives: FPR 0.423
(African-American) and 0.220 (Caucasian); FNR 0.285 and 0.496. **ProPublica's article's 44.85% /
23.45% FPRs and 27.99% / 47.72% FNRs come from the same `compas-scores-two-years.csv`, all 7,214 rows,
without the date and charge filters** (3,696 black and 2,454 white defendants; TN 990, FP 805, FN 532,
TP 1,369 and 1,139, 349, 461, 505; recomputed here, and by the second review). The notebook reaches
them through `cox-parsed.csv` and `truth_tables.py` with the same 730-day rule that wrote the
two-year file, so it is the same 7,214 people. Same cut-off, same outcome; the only difference is
the filters of notebook cell 4. RiskLab uses the filtered 6,172 (ProPublica's own analysis N); Help
page 7 states both. (Corrected 26 Oct 2026, beta 1a: an earlier version of this note wrongly put the
article's rates in ProPublica's survival file.)

Group labels are used exactly as in the file ("African-American", "Caucasian"); "African-Am." is
the only abbreviation, used in narrow table columns, with the full label on the same page.

Not used: the other groups in the file (Hispanic 509, Other 343, Asian 31, Native American 11), the
violent-recidivism score, and ProPublica's survival data.

## Dieterich et al. (2016)

Title checked by web search (26 Oct 2026): Dieterich W, Mendoza C, Brennan T (2016) *COMPAS Risk
Scales: Demonstrating Accuracy Equity and Predictive Parity*, Northpointe Inc. RiskLab states only
which fairness definitions each side used (Northpointe: AUC and PPV by group; ProPublica: FPR and
FNR by group) and quotes no number from the Northpointe report.

## Stata's published worked example (used in the verify script only)

Hanley & McNeil (1982) ratings, 58 normal / 51 abnormal patients on a 1-5 scale (counts 33, 6, 6,
11, 2 and 3, 2, 2, 11, 33). Stata `roctab` manual, `roctab disease rating`: ROC area 0.8932,
Std. err. 0.0307 (DeLong), asymptotic normal 95% CI 0.83295 to 0.95339. RiskLab gives the same
(read on the Stata manual, `stata.com/manuals/rroctab.pdf`, 26 Oct 2026).
