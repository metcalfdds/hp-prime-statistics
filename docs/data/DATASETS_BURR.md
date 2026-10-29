# Data sets added for BurrLab (28 Oct 2026)

The same two-source rule as `DATASETS_2026-10-21.md`: every set below was taken from two sources that agree,
or from one source plus an internal check. BurrLab shows the source on screen when a preset is
loaded (the data page) and names it in its header. Nothing here changes `DATASETS_2026-10-21.md`.

| Preset in BurrLab | What | Source to show | Check done |
| --- | --- | --- | --- |
| BJS: months served, 41 homicide offenders | `crimedatasets_Sentence_tbl_df.csv` (already in `DATASETS_2026-10-21.md`): months served by 41 prisoners convicted of a homicide offence | BJS, *Prison Sentences and Time Served for Violence*, NCJ-153858 (1995), via R crimedatasets | 41 values, sum 6358, min 115, max 216 (read from the CSV by the build script, not retyped) |
| Rossi: weeks to re-arrest, the 114 re-arrested | `rossi.csv` (already in `DATASETS_2026-10-21.md`), the rows with `arrest = 1`: `week` is the week of first re-arrest | Rossi, Berk & Lenihan (1980) via Allison (1995) / R carData | 114 rows, sum 3273, min 1, max 52; the 318 censored men (arrest = 0, week = 52) are EXCLUDED, and the program says so on screen |
| Danish fire losses, 300-value subsample | `evir::danish` (R package evir, via Rdatasets: `csv/evir/danish.csv`, fetched 27 Oct 2026 from the Rdatasets GitHub mirror): 2,167 Danish fire insurance losses, 3 Jan 1980 to 31 Dec 1990, in millions of DKK (inflation-adjusted to 1985 values), supplied by Mette Rytgaard of Copenhagen Re. BurrLab uses the EXCESS over the 1 million DKK threshold (loss - 1) for the 2,156 losses strictly above 1 million; a random 300 of them (numpy `default_rng(1980).choice(2156, 300, replace=False)`, rounded to 3 decimals) are carried in the program | McNeil (1997) *ASTIN Bulletin* 27(1):117-137 and R evir `danish` (Rdatasets) | Two sources reconciled: the evir vector has 2,167 values, 11 of them exactly 1.0; McNeil's paper counts "the 2156 losses exceeding one million" = 2,167 - 11. Exceedance counts above 3, 4, 5, 10, 20 million from the file (532, 362, 254, 109, 36) equal McNeil's Table I; the largest loss 263.25 equals his "263". File summaries: mean 3.385, median 1.778, SD 8.51 (n = 2,167). Subsample: n = 300, min 0.005, max 151.413, mean 2.668, median 0.741 |
| Danish fire losses, all 2,156 in 60 bins | The same 2,156 excesses counted in 60 log-spaced bins: bin 1 is (0, 0.001], bin j (j = 2..59) is (10^(-3+0.1(j-2)), 10^(-3+0.1(j-1))], bin 60 is everything above 10^2.8 = 631 (empty; the largest excess is 262.25). Counts: 0, 0, 0, 0, 0, 2, 2, 3, 2, 6, 1, 5, 4, 12, 17, 7, 4, 23, 24, 32, 25, 64, 58, 44, 79, 103, 113, 140, 138, 184, 161, 136, 124, 110, 102, 97, 79, 70, 36, 32, 22, 24, 19, 20, 10, 10, 2, 4, 2, 1, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0 (sum 2,156) | as above | the counts sum to 2,156; `verify_BurrLab_beta1.py` A7 checks the edges and the total through the program's own lists |

Why the excess over 1 million, and not the loss itself: the evir series is left-truncated at 1
million DKK (11 values sit exactly on the threshold), so a Burr XII on the raw losses runs to
its Pareto limit (C to infinity, S to 1) and the fit degenerates; on the excesses the maximum
likelihood estimate is interior (C about 1.13, K about 1.23, S about 1.03 on all 2,156; K C
about 1.40, so the mean exists and the variance does not). McNeil (1997) also works with
excesses over a threshold. BurrLab's data page says "excess over 1M DKK".

Not added: a second BJS table with raw values. The other crimedatasets tables in `data/` are
counts or ratings, not durations, and no further BJS raw-value table was verified against a
second source, so none was added (the spec said "otherwise not").
