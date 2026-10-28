# RiskLab beta 1a - notes (26 Oct 2026)

`/home/claude/new6/RiskLab_beta1a.txt`, 3,087 lines (beta 1 kept unchanged; what changed: `RiskLab_beta1a_CHANGES.md`), pure ASCII, LF. Entry `EXPORT RiskLab()`, tag
`rl_` (routines) / `rl` (file-level LOCALs) / `RL_` (Home exports). Harness only: NOT run on the
emulator, the G2 or the G1.

## What it does, menu by menu

Opens on a page with the DISCLAIMER; ProPublica's COMPAS counts are loaded at start (fast: 10
levels). Main menu: Logistic regression; ROC and cut-off; Calibration; Fairness by group; Load a
preset; Use my data (Stat 1Var); Help; Quit. Inside any view, Enter = "Go to" menu, Esc = back.

1. **Logistic regression** (view 1, table): per term b, SE, Wald z, p; under each predictor
   OR = e^b with its 95% CI e^(b +/- 1.96 SE); -2 lnL of the model and of the intercept-only model;
   LR chi-square, df k, p; McFadden R^2; Newton-Raphson steps. Tapping a row explains it ("prio:
   odds x 1.111 per +1 (others fixed)"; "fin: ... for 1 vs 0"). Red warnings: separation (no finite
   estimates; b, SE, p, OR not valid), collinearity (no SEs), fewer than 10 of the rarer outcome per
   predictor (Peduzzi et al. 1996). Separation (beta 1a) is judged from the fit only: no
   convergence in 25 steps, an information matrix turning singular after 3+ steps, or a linear
   predictor that orders Y perfectly; a converged fit with some fitted P near 0 or 1 gets only a grey
   note. Soft keys Curve / ROC / Calib / Fair / Back.
   **Fitted curve** (view 2): for one predictor, P(Y = 1) against x with the others at their means
   (magenta), each person as a dot (Y = 1 top, Y = 0 bottom, spread by a fixed pattern), and the
   share with Y = 1 in bins (green: one bin per value when x takes at most 8 values, else 8 equal
   widths). Cursor by arrows, tap or drag; readout of the fitted P and the bin's observed share.
   Prev x / Next x change the predictor.
2. **ROC and cut-off** (view 3): ROC as straight segments between the cut-off points (vertical /
   horizontal steps, diagonal where a score level holds both outcomes), area shaded, chance diagonal
   dotted. A red point marks the cut-off ("high risk = score >= c"); Left/Right move it one level,
   +/- ten, a finger drags it along the curve. Live 2 x 2 table (TP, FP, FN, TN) and sensitivity,
   specificity, PPV, NPV, FPR, share flagged. AUC with the DeLong 95% CI (stated on screen); a tap
   on the AUC line shows the DeLong and Hanley-McNeil SEs. "Groups" overlays each group's curve and
   puts a red point on each at the same cut-off. For a model's fitted P, a red "in-sample" line.
3. **Calibration** (view 4): mean predicted P vs observed share per group, 45-degree line, grey bars
   pred +/- 1.96 sqrt(pred(1-pred)/n) (labelled a rough guide in Help); table of groups (n, pred,
   obs); Hosmer-Lemeshow chi-square with df = groups - 2 and p. Groups: 10 by predicted risk (rows of
   data) or one per score level (a score with <= 12 levels); the soft key "Groups" switches to 5.
   Ties are never split. A red caution when a group expects < 5 events or non-events (Cochran 1954).
   For a score, the predicted P is a logistic fit of Y on the score (stated in the table page).
4. **Fairness by group** (view 5; two groups needed): Table (n, base rate, AUC, flagged, FPR, FNR,
   PPV, NPV, and their differences), Calib (share with Y = 1 at each score level, a line per group;
   45-degree line for a probability score), Errors (bars: flagged, FPR, FNR, PPV per group at the
   cut-off; arrows move the cut-off live), Why (Chouldechova's identity FPR = p/(1-p) (1-PPV)/PPV
   (1-FNR) worked with the data's own numbers for both groups, then "give group 2 group 1's PPV and
   FNR: its FPR must be ...", then the conclusion). Help page 6 states the definitions and who used
   which (Northpointe: AUC and PPV; ProPublica: FPR and FNR) without a verdict.
5. **Load a preset**: COMPAS; Rossi: age, prio, fin; Rossi: age, prio, fin, wexp. A load page shows
   what the data are and the source line. **Use my data**: (a) D1 = Y 0/1, D2-D5 = 1 to 4 predictors
   (10-500 rows); (b) D1 = Y, D2 = a score (higher = riskier), D3 = group 1/2 optional (10-2000
   rows). **Help**: 8 pages. **Quit** returns e.g. "RiskLab: COMPAS, AUC = 0.711, >= 5: sens
   0.645, spec 0.670".

Home exports: RL_B, RL_SE (lists), RL_OR (odds ratios of the predictors), RL_P (LR p), RL_AUC
{AUC, DeLong SE}, RL_HL {HL, df, p}, RL_CUT {cut-off, sensitivity, specificity, PPV}; -1 when not
computed.

## Formulas and sources

| What | Formula | Source |
| --- | --- | --- |
| Fit | Newton-Raphson b <- b + I^-1 U, U = X'(y - m mu), I = X'WX, W = m mu(1-mu); start at the null model; converged when every step < 1E-9 (1 + abs b); 25 steps max; one more pass at the final b for lnL, SE, fitted P | Hosmer & Lemeshow 2000 ch. 1-2; Agresti 2013 5.1 (pages not checked) |
| Null model | lnL0 = Y ln(Y/M) + (M-Y) ln(1 - Y/M) | closed form |
| Tests | Wald z = b/SE, p = 2 Phi(-abs z) (a lower tail); LR = 2(lnL - lnL0), df k; McFadden 1 - lnL/lnL0 | McFadden 1974 |
| Separation | not converged in 25 steps, or I singular after >= 3 steps, or the linear predictor orders Y perfectly (rl_Order); max abs eta > 15 alone = a note | Albert & Anderson 1984 |
| Collinearity | a Gauss-Jordan pivot (no row exchange; I is positive semi-definite) below 1E-10 of its column's diagonal | - |
| AUC | (pairs where Y=1 scores higher + 1/2 ties) / (n1 n0) = Mann-Whitney U/(n1 n0) | Bamber 1975; Hanley & McNeil 1982 |
| DeLong SE | Var = S10/n1 + S01/n0, structural components with ties 1/2, n-1 divisors; CI AUC +/- 1.96 SE cut at 0 and 1 | DeLong et al. 1988 |
| Hanley-McNeil SE | Q1 = A/(2-A), Q2 = 2A^2/(1+A) | Hanley & McNeil 1982 |
| HL | sum (O-E)^2/(E(1-E/n)), df = groups - 2 | Hosmer & Lemeshow 1980; Hosmer et al. 1997 (weaknesses) |
| Chi-square tails | finite sums of positive terms, any whole df (rl_ChiUp) | Lessons Learned 11 |
| Fairness identity | FPR = p/(1-p) (1-PPV)/PPV (1-FNR) (an identity of the 2 x 2 table) | Chouldechova 2017; Kleinberg et al. 2016 for calibration vs balance |

## Presets and sources

- **COMPAS**: counts by decile and group from ProPublica's `compas-scores-two-years.csv` with their
  notebook's filter; N = 6,172, 2,809 re-arrested, 3,175 / 2,103 and every n per decile equal
  ProPublica's printed numbers; re-arrest counts by two routes (csv module, pandas) and a third in
  the verify script. Recorded in `data/DATASETS_RISK.md` and `data/compas_two_year_counts.csv`. The
  methodology article's 44.85% / 23.45% FPRs (FNR 27.99% / 47.72%) come from this same file, all 7,214
  rows, without the date and charge filters (3,696 black, 2,454 white defendants); with ProPublica's
  analysis filters (N = 6,172), as RiskLab uses, they are 42.3% / 22.0%. Help page 7 says both.
- **Rossi** (`data/rossi.csv`, DATASETS.md): arrest within 52 weeks on age, prio, fin (and wexp).
  Codebook checked against `carData_Rossi.csv` and the carData documentation (fin assigned at
  random; wexp = full-time work before prison). race, mar and paro were not used: the spec's
  predictors are age, prio, fin; the fairness lesson uses COMPAS.

## What was checked (verify_RiskLab_beta1a.py: 611 checks, 0 failures)

Beta 1a adds Part D, one or more checks per review item: the case-insensitive name scan (below), the
reviewer's wide-x case (statsmodels converges, max |eta| > 15: no warning, a grey note), complete and
quasi-complete separation still flagged on the page, all 7,214 rows reproducing 44.85 / 23.45 and
27.99 / 47.72, the opening page, AUC with one score level / AUC = 1 / small n, the COMPAS calibration
note, and the wording items.

**Name scan (beta 1a):** `name_scan()` in the verify script reads every routine head (98), EXPORT name (7, entry point included) and file-level LOCAL (145) of RiskLab_beta1a.txt and folds case: **0 pairs equal ignoring case**, and no routine LOCAL folds onto any of them. Run on beta 1 the same scan finds exactly one pair, `rl_HL` (routine) / `RL_HL` (EXPORT), now `rl_HosLem`. (fleet_names_v2 compares routines with routines and built-ins only, so the gate could not see it.)

Beta 1 checks, carried over:

- Logistic fits vs statsmodels Logit (b, SE, lnL, lnL0, LR, its p, McFadden; fitted P to 1E-9) on
  Rossi k = 3 and 4, COMPAS (grouped counts = 5,278 people one by one), and 30 random sets (n 10-300,
  k 1-4, normal, binary, integer, 1E4-1E5 and negative predictors; at least 20 compared, the rest
  flagged as unstable by both); complete and quasi-complete separation flagged; collinear x refused
  with "no SEs"; constant outcome refused; n = 2 and 3 run without an error.
- AUC vs pairwise counting and scipy mannwhitneyu; DeLong vs a pairwise implementation, a 2,000-
  resample bootstrap (within 10%) and **Stata's published example** (Hanley & McNeil 1982 data:
  0.8932, SE 0.0307, CI 0.83295-0.95339: equal; RiskLab's Hanley-McNeil SE is 0.0325, Stata's
  `hanley` option prints 0.0320 - Stata's variant, not checked further); every cut-off's counts;
  HL vs an independent grouping and chi2.sf; rl_ChiUp vs chi2.sf (df 1-14, x to 400, worst relative
  error < 1E-9); levels with groups; COMPAS counts and error rates from the raw CSV.
- Every menu path in the harness with the numbers on the pages: tables, taps, curve readouts, ROC
  2 x 2 tables at several cut-offs (arrows, +/-, drag), overlay AUCs, calibration tables and HL for
  both groupings, all four fairness pages including the Why page's arithmetic, your-data paths
  (valid and 8 refusals), Esc during the Rossi fit and the re-fit, Help (8 pages, Esc), Quit.
- Every run: no runtime error, no scientific number, no text off screen, MSGBOX <= 5 lines of <= 38
  characters, every text within its width at 6.5 px per character, source ASCII.
- Gate (ppl_gate_v1c): PASS; kit lint 0 errors; ppl_check clean; lint_ppl 6 known-noise items (no
  function named after the file; EXPORT-discipline lines); full parse stops at the file-level LOCAL
  after the EXPORT lines (the tool's known limit); fleet names: 0 collisions, 0 untagged.

## G1 speed (estimate, not measured)

`tools/count_statements.py`: one Rossi fit (432 rows, 4 predictors, 7 passes) executes about
137,000 PPL statements (19,600 per pass, about 45 per row, no inner loops) plus about 30,000 for the
levels, AUC and HL; 0.6 s in the harness. At the brief's 30-100 x, **about 20-60 s on a G1**; a
progress page per pass with a bar every 24 rows, and Esc stops it (the menu re-fits later). COMPAS
needs about 4,000 statements (instant). Your data: up to 500 rows x 4 (about 25-70 s on a G1).

## Left out (and why)

- No Firth / penalised fit for separation (only detected and explained).
- Rossi's race, mar, paro not offered (see above). No other COMPAS groups.
- The ROC drag searches every cut-off point per frame: fine for COMPAS (11) and Rossi (up to 272),
  slow for a 2,000-level score of your own.
- No CAS, no Python. No Triola program is replaced; TI LOGIT (grouped WLS) is credited for the idea.

## DEVICE CHECKLIST (in order; expected values from the harness)

0. Delete RiskLab beta 1 from the calculator first (it shares the routine names).
1. Paste, Check in the Program Catalog (Shift + Program -> Edit -> Check): no syntax error.
2. Run `RiskLab` from Home (no parentheses). Opening page shows the 4-line DISCLAIMER box and "432 men
   released from Maryland state prisons". Any key.
3. Logistic regression (COMPAS): const -1.433, SE 0.059, z -24.16, p <.0001; decile +0.283, SE
   0.011, z 25.52, OR = 1.327, 95% CI 1.299 to 1.356; -2 lnL = 6553.13
   (no predictors: 7298.41); LR chi-square = 745.28, df 1, p < 0.0001; McFadden 0.102; 5 steps.
   Tap the decile row: "decile: odds x 1.327 per +1 (others fixed)". Check the chi-square, R^2,
   subscript-0, x and +/- glyphs render.
4. Curve: the magenta S-curve, green squares at deciles 1-10; Right moves 1 decile; readout at 5:
   "fitted P = 0.495", "249 of 523 re-arrested = 0.476". Prev x: "One predictor only".
5. ROC: cut "decile score >= 5" (the >= glyph); table 1602 / 923 / 881 / 1872; sensitivity 0.645,
   specificity 0.670, PPV 0.634, NPV 0.680, FPR 0.330, flagged 47.8%; AUC = 0.711, 95% CI 0.698 to
   0.725 (DeLong). Left -> ">= 6"; drag a finger along the curve: the red point follows (note how
   smooth on the G1). Groups: blue and magenta curves, "AUC: African-Am. 0.704, Caucasian 0.693".
   Tap the AUC line: "SE: DeLong 0.0070, Hanley-McNeil 0.0071".
6. Calibration (COMPAS): title "Calibration: COMPAS (RiskLab's fit)", grey line "pred: RiskLab's
   logistic of Y on the score"; HL chi-square = 11.79, df 8, p = 0.1608, "10 groups: one per score
   level"; Groups -> 3.36, df 3, p = 0.3389. Tap a dot: its row turns red.
7. Fairness at >= 5: base rates 0.523 / 0.391, AUC 0.704 / 0.693, FPR 0.423 / 0.220, FNR 0.285 /
   0.496, PPV 0.650 / 0.595. Errors: bars move with Left/Right. Why: the two identity lines end in
   0.423 and 0.220 at >= 5. Calib: at decile 5, 158 of 323 = 0.489 and 91 of 200 = 0.455.
8. Load a preset -> Rossi: age, prio, fin. **Time the fit with a watch** (estimate 20-60 s): 7
   progress pages, the bar moves. Then: LR 27.56, df 3; AUC 0.654. Table: age -0.076 (OR 0.926, CI
   0.885 to 0.969), prio +0.106 (1.111), fin -0.406 (0.667, CI 0.427 to 1.039), McFadden 0.055,
   6 steps. ROC: "high risk = fitted P >= 0.3194", 47 / 65 / 67 / 253, red "in-sample" line.
   Calibration: HL 14.82, df 8, p = 0.0628 and the red Cochran caution. No "SEPARATION" anywhere.
9. Rossi with wexp: press Esc during the fit -> load page says "No fit: stopped with Esc"; then
   Logistic regression re-fits (LR 28.46, df 4).
10. Fairness on Rossi: a MSGBOX "Fairness needs two groups"; one key closes it and nothing is
    skipped.
11. Use my data (score): D1 = 0 x 58 then 1 x 51; D2 = Hanley & McNeil's ratings (1 x 33, 2 x 6,
    3 x 6, 4 x 11, 5 x 2, then 1 x 3, 2 x 2, 3 x 2, 4 x 11, 5 x 33): ROC AUC 0.893, CI 0.833 to
    0.953, DeLong SE 0.0307 (Stata's numbers). D2 all equal: "AUC = 0.500 (one score level: no
    interval)". D2 = 1..20 with D1 = ten 0s then ten 1s: "AUC = 1.000 (SE = 0: no interval)". With D1
    emptied: the "D1 needs at least 10 rows" message.
11a. Help page 7 ends "count all 7,214 people (no date or charge filters). After the filters: 42.3%
    and 22.0%."; Help pages 5 and 6 have 14 lines: check the last line is above the footer.
12. Help: 8 pages; Esc on page 1 leaves. Quit: the summary line in Home; RL_AUC, RL_CUT, RL_B in
    Home hold numbers.
