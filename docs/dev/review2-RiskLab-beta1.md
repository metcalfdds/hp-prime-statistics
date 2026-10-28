# Second review: RiskLab beta 1 (26 Oct 2026)

Independent reviewer; did not write the program; did not edit it. Own scripts (not the builder's verify) in
`/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/rv2risk/py/` (`rv2.py` presets vs
statsmodels/own DeLong/HL; `rv2_ui.py` awkward sets driven through the harness; `dec12.py` the fit in 12-digit
decimal arithmetic). ProPublica files fetched independently from GitHub (`.../rv2risk/dl/`, the two-year CSV is
byte-identical to the builder's copy).

## Findings, most serious first

### 1. `rl_HL` (routine, line 1054) and `RL_HL` (EXPORT variable, line 112) are one name ignoring case - CONFIRMED (rule), device effect PLAUSIBLE
Lessons v7r: "names differing only in case are one name" (ResampLab's `rsHa`/`rsHA`). This is the only case-only
pair in the file (scripted scan of every identifier). The gate passes because `fleet_names_v2` compares routine
names with routine names and built-ins, not with the file's own EXPORT variables, and the harness is
case-sensitive. **Failure scenario:** a syntax error on paste (name defined twice), or `RL_HL := {...}` (line 1132)
/ `rl_HL()` (lines 1105, 1113, 2039, 2099) binding to the wrong object at run time - either in front of a class.
**Fix:** rename the routine, e.g. `rl_HosLem`, at 1054 and the four calls; re-run the gate. Suggest adding an
"EXPORT variable vs routine, case-folded" check to `fleet_names`.

### 2. Help page 7 (lines 2859-2861) misstates where ProPublica's 44.9% / 23.5% come from - CONFIRMED
Screen: "Their article's FPRs 44.9% and 23.5% come from another file (their survival data)." Same claim in
`data/DATASETS_RISK.md` and the NOTES. What is true (notebook cells 70-77, `truth_tables.py`, article):
- The article's tables (FP 44.85 / 23.45, FN 27.99 / 47.72) total **3,696 black and 2,454 white defendants**.
- I reproduce all four rates exactly from `compas-scores-two-years.csv` itself, **all 7,214 rows, no filters**:
  African-American TN 990, FP 805, FN 532, TP 1,369; Caucasian 1,139, 349, 461, 505.
- The notebook reads `cox-parsed.csv`, but through `truth_tables.Person` with the same 730-day rule that
  `truth_tables.create_two_year_files()` used to *write* `compas-scores-two-years.csv`: the same 7,214 people.
- Same cut-off (score_text not "Low" = decile >= 5; verified decile 1-4 Low, 5-7 Medium, 8-10 High) and same
  outcome. The only difference is that the cell-4 filters (|days_b_screening_arrest| <= 30, is_recid != -1,
  c_charge_degree != "O") were not applied; with them (6,172; 3,175 / 2,103) the rates are 0.423 / 0.220 (FNR
  0.285 / 0.496), as RiskLab shows.
**Fix (lines 2859-2861, each under 300 px):**
`"Y = 1: a new arrest within two years.  Their"`, `"article's FPRs, 44.9% and 23.5%, count all"`,
`"7,214 people (no date or charge filters)."` If room allows a 14th line: `"After the filters: 42.3% and 22.0%."`
Correct DATASETS_RISK.md and the NOTES the same way ("different file ... survival framing" is wrong).

### 3. False "SEPARATION ... NOT valid" on a valid fit (rl_Fit line 828; text 1279-1281; Help 2766-2768) - CONFIRMED
`IF rlConv == 0 OR rlEta > 15 THEN rlSep := 1` flags any fit where one row's |eta| > 15. Example (101 rows,
x = 0..100, y ~ logistic((x - 50)/5), seed 3 in `rv2_ui.py`, case `wide`): statsmodels converges (b = -18.46,
0.321; SE 5.79, 0.100; max |eta| 18.5; AUC 0.994, not separated); RiskLab matches the numbers and then says
"b, SE, p, OR above are NOT valid". A wide-ranging x does this routinely. **Fix:** flag separation on
non-convergence in 25 steps or a singular I after >= 3 steps only; for |eta| > 15 with convergence, at most a
grey note ("some fitted P within 3E-7 of 0 or 1"). Reword Help page 2 to match.

### 4. "Rossi's 432 parolees" (rl_Open, line 2891) - CONFIRMED
Only 267 of the 432 were released on parole (`paro`, DATASETS_RISK.md; carData). **Fix:** "Rossi's 432 released
prisoners" (or "432 men released from prison"). Everything else said about Rossi (Maryland, 52 weeks, arrest,
age at release, prio = prior convictions, fin randomised, wexp = full-time work before) matches the codebook.

### 5. Zero-width AUC CI when DeLong SE = 0 (line 1769-1770) - CONFIRMED
All scores tied: "AUC = 0.500, 95% CI 0.500 to 0.500 (DeLong)"; perfect separation: "1.000 to 1.000". **Fix:**
if `rlM == 1` or `rlSEd == 0`, print "AUC = 0.500 (one score level: no CI)" / "(no SE at AUC = 1)". Related,
lower priority: the CI is plain Wald, cut at 0 and 1 (stated in Help, same as Stata `roctab`), so at n = 10 it
reads "0.459 to 1.000". A logit-scale CI, logit(A) +/- 1.96 SE/(A(1-A)), stays inside (0, 1) (0.353 to 0.958
here); or keep Wald and add "(rough at small n)" when a bound is cut.

### 6. COMPAS calibration page does not say whose P it is (rl_CalDraw) - PLAUSIBLE (teaching)
COMPAS gives deciles, not probabilities; "pred" is RiskLab's logistic in decile fitted to these same 5,278
people, so HL p = 0.161 tests that curve in-sample, not "COMPAS is calibrated". Add one grey line, e.g.
"pred: RiskLab's logistic of the decile (in-sample)".

### 7. Small wording items - CONFIRMED, cosmetic
- line 582: the progress page says "Rossi's fit takes 7 passes" also for your own data over 60 rows.
- line 1758 with `rlEvW = "Y = 1"` (2629, 2705): the ROC table prints "Y = 1: Y = 1".
- line 823: a constant predictor is reported as "collinear x (one a mix of others)"; say "an x is constant or
  a mix of others".
- footers "+/- = x10": the brief asks for the × glyph (`rlTIM`).
- Help page 6 "Kleinberg ... for calibration and balanced average scores": clearer as "calibration and equal
  average scores among Y = 1 and among Y = 0".
- Fairness page 1 (line 2172): add "(unless prediction is perfect)" as page 4 does, or "see Why" covers it.

### 8. G1 speed of the Rossi fit - PLAUSIBLE
The builder's count is about 163,000 statements for load + fit (7 passes x 432 rows). No G1 rate is measured
for this kind of loop; it may take tens of seconds. The progress bar and Esc (every 24 rows) are in place and
Help says so. Put the time on the device checklist.

## Checked and found correct
- **Rossi** (`arrest ~ age + prio + fin`, and `+ wexp`; columns match the carData codebook): b, SE, lnL, lnL0,
  LR chi-square and p equal statsmodels Logit to 2E-14 (k = 3: b = 0.6565, -0.0765, 0.1056, -0.4057; LR 27.56,
  p 4.5E-6). The same fit in 12-digit decimal arithmetic converges in 6 steps, b and SE within 1E-9 relative:
  no precision problem. Bootstrap optimism of the in-sample AUC (400 resamples): 0.654 -> 0.643 (k = 3),
  0.661 -> 0.644 (k = 4: wexp's gain vanishes). The ROC page says "in-sample: P fitted to these same people"
  and Help "A model's AUC on its own data is optimistic": stated. (Optional: "optimistic by about 0.01-0.02
  here" on the page.)
- **AUC and DeLong SE** equal my own DeLong (V10/V01, ties 1/2, n - 1 divisors) exactly: Rossi 0.6537/0.0300;
  COMPAS pooled 0.7113/0.00702, African-American 0.7043/0.00911, Caucasian 0.6928/0.01170.
- **Hosmer-Lemeshow**: COMPAS one group per decile, df 8, 11.79, p 0.1608 (mine identical); Rossi 10 groups
  ties kept, 14.82 p 0.063 (k = 3), recomputed from the same groups identically. Grouping convention differs by
  software (R `hoslem.test`-style 13.73, equal-size split ties 12.99): Help says so.
- **Cut-off table** at decile >= 5: pooled sens 0.645, spec 0.670, PPV 0.634; per group FPR 0.423 / 0.220,
  FNR 0.285 / 0.496, PPV 0.649 / 0.595; Chouldechova page arithmetic (1.097 x 0.540 x 0.715 = 0.423, 0.642 x
  0.681 x 0.504 = 0.220, swapped 0.248) all correct.
- **COMPAS counts**: my own filter of the fetched CSV gives N 6,172, 2,809 re-arrested, 3,175 / 2,103, and
  every per-decile n and event count in `rl_LoadCompas` and the CSV.
- **Statements**: ProPublica "marked scores other than low as higher risk" (article); Northpointe/Dieterich et
  al. argued accuracy equity (AUC) and predictive parity; Chouldechova's identity; all citations in the header
  (journals, volumes, pages) correct; group labels as in the file; no verdict on COMPAS; disclaimer on the
  opening page.
- **Device rules**: LOCAL lines <= 6, no list arithmetic in any path run, no comment in brackets (gate E12),
  MSGBOX texts <= 4 line breaks, drains after CHOOSE/MSGBOX/waits, Esc in the IRLS pass, `EXP` never sees a
  large positive argument (softplus form of lnL, `rl_Lgt`, `rl_ExpS` caps), lnL kept to its digits near
  P = 0 / 1, all chi-square tails as finite positive sums with integer df (`rl_ChiUp`), Wald p as a lower
  tail. Awkward sets (separation, constant x, n = 10, all scores tied, tied rows, x near 1E-6 and > 1E6)
  run with no runtime error and no `ᴇ`; n < 10 and |x| > 1E6 are refused with a message.
