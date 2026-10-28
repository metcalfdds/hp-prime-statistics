# AnovaLab beta 1a: notes (21 Oct 2026)

File: `/home/claude/new6/AnovaLab_beta1a.txt` (3,771 lines, pure ASCII, LF); beta 1 kept unchanged beside it.
Entry `EXPORT AnovaLab()`, zero arguments, menu-first. Tag `av_`; Home exports `AV_F, AV_P, AV_DF, AV_MSE, AV_ETA2, AV_TAB`
(from the last analysis: one-way F/p/eta²; two-way the A×B interaction; blocks the treatments; variances the statistic).
**Not run on hardware or the emulator**: PC harness (ppl_run_v3e) and the gate only.
Beta 1a applies every finding of the second review; one line per fix in `AnovaLab_beta1a_CHANGES.md`.

## What changed for the student (beta 1 → 1a)

- Post hoc pages open on **Holm** (instant). Tukey is computed only when picked, after a one-line warning with a G1
  estimate ("Compute it now" / "Not now"); Tukey p for all pairs (More > Tukey p) or for one pair (Menu), Esc stops
  inside the integration; the step bar counts honestly ("step n (q crit takes 6 to 23)").
- The Tukey engine tabulates the inner integral once per k (121 points, cubic interpolation): 3.4-4.9 × cheaper for q
  crit, 11.8 × for the draft's 66 p-values. Accuracy vs SciPy (k 2-12, df 3-1000, α .1-.001): q crit within 2.2E-4
  relative, tail within 6.7E-4 of α, pair p within 2.7E-6 (help page 3).
- Cells page fits 6 × 6 designs (tap a cell for x̄, n, s). Interaction wording never turns "no evidence" into "no
  interaction". Checks page: no unsourced s-ratio rule; its bottom line follows Levene. Large data: Working page with
  Esc above 500 values; the Dots page draws its dots once. Factor codes print as integers.

## What it does, menu by menu


Opening page: what it covers, the DISCLAIMER (red panel), copyright line. Then the main menu (CHOOSE, 9 items):

1. **One-way ANOVA** (default data: mock jury, Years by attractiveness). Five pages; soft keys
   `Table | Checks | Pairs | Dots | F | More`, and after More `Method | Tukey p | Help | Menu | Back | More`.
   The post hoc method starts as **Holm**.
   Enter = a CHOOSE of every action (the key twin of every soft key); Esc = main menu.
   - *Table*: SS, df, MS, F, p (between / within / total), eta², omega² (Hays), Welch's F with its fractional df and p,
     the verdict panel (red reject / green "no evidence ... not proof of none"), the source line of the data.
   - *Checks*: Levene (Brown-Forsythe, |y − median|) F and p, Bartlett χ² and p, largest/smallest s,
     every group's n, x̄, s, median (two columns when k > 7).
   - *Pairs*: every pair i < j, diff = mean_i − mean_j, the method's simultaneous CI, adjusted p, red `*` = differs.
     Tabs (tap) or +/- choose Tukey-Kramer, Bonferroni, Holm, Scheffe. Up/Down move the highlight; a tap on a row
     opens it on the Dots page. The default is Holm; Tukey is computed only after the student picks it and accepts
     a one-line warning with a G1 estimate (progress page, Esc stops inside the integration); Tukey p-values only on
     request (More > Tukey p for all pairs, Menu > Tukey p for this pair). Holm shows Bonferroni's CI
     (it says so). Before p is computed the Tukey column shows q and `*` = q > q crit (the same decision).
   - *Dots*: every value as a dot (5 lanes of jitter), each group's mean (green) and its (1 − α) CI from the
     POOLED s (magenta; the legend says "pooled s"). Tap two groups (or Left/Right through the pairs) for the
     pair's diff, method CI and adjusted p (or q vs q crit).
   - *F*: the F(k − 1, N − k) curve (density cached per pixel column), the p area shaded blue, the critical
     region pale red (purple where both), crit dotted magenta, the observed F a red line, or an arrow and
     "is off the plot, to the right" when F is far out (insect sprays, F = 34.7).
2. **Two-way ANOVA (A × B)** (default: mock jury, Attractiveness × Crime). Soft keys `Table | Cells | Plot | F | Swap | Menu`.
   - *Table*: Type III SS (title says "Type III SS") for A, B, A×B, Error, Total; F, p, partial eta².
     Balanced designs: the classical SS are also computed and the page says whether they agree with Type III
     (checked: they agree to < 1E-9 of SST on every balanced test design). Unbalanced: "they need not add to the total".
   - *Cells*: cell means with n and s, unweighted margins (means of cell means: what Type III compares).
   - *Plot*: interaction plot, one coloured line per level of the trace factor; tap a point (or arrows) for its
     cell mean, n, s; Swap turns the plot.
   - *F*: the F curve of one effect; +/- or a tap on the title steps A, B, A×B.
3. **Randomized blocks** (default: 43 judges × INTG, DMNR, DILG). Soft keys `Table | Plot | F | | Help | Menu`.
   Treatments / Blocks / Error / Total with F and p, partial eta² (treatments), and the one-way F that ignores
   the blocks (F = 3.118, p = 0.0477 for the judges, against 21.349, p < 0.0001 blocked). Profile plot: one grey
   line per judge, treatment means green; tap a criterion for its mean, s, n.
4. **Variances: χ² and F** (Triola's S2TEST/S2INT, SDHYP/SDINT, STDTEST, STDEVCI, FINTRVAL reworked). One σ: χ² test
   and CI for σ² and σ; two σ: F test and CI for σ₁²/σ₂² and σ₁/σ₂. Data: typed s and n (labelled "illustrative
   numbers") or groups of the current one-way data. H₁ ≠ / < / > by CHOOSE; confidence level in the form.
   Soft keys `Result | Curve | 1 σ | 2 σ | Help | Menu`. The curve shades the observed tail and the other tail of
   EQUAL area (STDTEST's rule) in blue, both critical regions (α/2 each) in pale red.
5. **Load a preset**: Jury years by looks (one-way), Jury looks × crime (two-way), Draft 1970 by month (one-way, 12
   groups), Insect sprays (one-way, 6 groups), Judges × 3 criteria (blocks). Each page shows its source line.
6. **Use my data (D1-D9)**: one-way = each non-empty list a group; two-way = D1 y, D2 A codes, D3 B codes (any
   numbers, 2-6 levels each); blocks = each list a treatment, row i = block i (same lengths). First reads in IFERR.
   Caps: 3000 values; 6 × 6 levels.
7. **Set α** (0.001-0.2): every verdict, critical value, CI; Tukey's q crit is recomputed when next needed.
8. **Help**: 8 pages (one-way, Welch/checks, pairs, two-way, blocks, variances, your data/Home, credits).
9. **Quit**: returns "AnovaLab: <last analysis>", e.g. `AnovaLab: one-way F(2, 111) = 2.770, p = 0.0670 (...)`.

## Formulas and sources

| Quantity | Formula | Source |
|---|---|---|
| One-way F | (SSB/(k−1)) / (SSW/(N−k)); p = P(F(k−1,N−k) > F) as the mirror lower tail `FISHER_CDF(df2, df1, 1/F)` | any intro text; Triola |
| eta², omega² | SSB/SST; (SSB − (k−1)MSW)/(SST + MSW) | Hays (1963) |
| Welch's F | w = n/s², A = Σw(m−m_w)²/(k−1), Λ = Σ(1−w/W)²/(n−1), F = A/(1+2(k−2)Λ/(k²−1)), df2 = (k²−1)/(3Λ); p by own incomplete beta (fractional df) | Welch (1951) Biometrika 38:330 |
| Levene | one-way F on \|y − median\| | Levene (1960); Brown & Forsythe (1974) JASA 69:364 |
| Bartlett | [(N−k)ln s_p² − Σ(n−1)ln s²]/C, C = 1 + (Σ1/(n−1) − 1/(N−k))/(3(k−1)); χ²(k−1) upper tail by Q(a,x) | Bartlett (1937) |
| Tukey-Kramer | q = \|diff\|/√(MSW/2 (1/n_i+1/n_j)); p = 1 − F(q); CI diff ± q crit/√2 · SE | Kramer (1956); engine: StudRange beta 15d PPL (Dunlap, Powell & Konnerth 1977) |
| Bonferroni | raw two-sided t p (df N−k, pooled SE) × m, max 1; t crit at α/(2m) | |
| Holm | step-down: r-th smallest raw p × (m−r+1), running maximum | Holm (1979) |
| Scheffe | F = t²/(k−1) on F(k−1, N−k); CI diff ± √((k−1)F crit)·SE | Scheffe (1953) |
| Two-way Type III | effect-coded X; b = (X'X)⁻¹X'y; SS_E = b_E' [((X'X)⁻¹)_EE]⁻¹ b_E; X'X built cell by cell; own Gauss-Jordan inverse with partial pivoting | as statsmodels anova_lm(typ=3) with Sum contrasts |
| Blocks | SSTr = nb Σ(T−M)², SSBl = kt Σ(B−M)², SSE = Σ(y−T−B+M)² | |
| One σ | χ² = (n−1)s²/σ₀²; CI ((n−1)s²/χ²_upper, (n−1)s²/χ²_lower) | Triola S2TEST/S2INT |
| Two σ | F = s₁²/s₂²; CI (F·F_{c/2}(df2,df1), F/F_{c/2}(df1,df2)), F_{c/2} the LOWER quantile | (FINTRVAL swapped these) |

Every upper tail is a lower-tail form (Lessons §3): F by its mirror, χ² by 2Φ(−√x) / e^(−x/2) / own Q(a,x),
t by `STUDENT_CDF(df, −|t|)`. Right-tail quantiles: `−STUDENT_ICDF(df, a)`, `1/FISHER_ICDF(d2, d1, a)`; every
ICDF probability clamped into (1E-12, 1 − 1E-12). Special functions copied from StatDist v2.7f (incomplete
beta and gamma, Numerical Recipes 6.2/6.4) and StudRange (Lanczos log-gamma).

## Presets (data/DATASETS.md only; literals generated by script from the CSVs, none typed)

- Mock jury: Plaster 1989 thesis, via R heplots MockJury. 114 values, Attr and Crime codes in CSV row order.
- Draft lottery 1970: draft1970_triola.json (= vcdExtra CSV, checked identical); 366 numbers by month.
- Insect sprays: Beall 1942, R InsectSprays; 12 per spray.
- Judge ratings: New Haven Register 14 Jan 1977, R USJudgeRatings; blocks = all 43 judges, treatments = INTG,
  DMNR, DILG (integrity, demeanor, diligence), said on screen and in the header.

**Note for Roger (spec vs data):** the spec calls the mock-jury interaction "striking". The cell means are (7.0 for
unattractive swindlers, 3.5-4.8 elsewhere), but the Type III interaction test gives F(2, 108) = 2.085, p = 0.129
(statsmodels identical). The program says "No evidence of interaction" and help page 4 makes it the lesson:
"striking, yet the interaction's p is 0.13 (cells of 17 to 21)".

## What was checked (verify_AnovaLab_beta1a.py: 8,712 checks, 0 failures)

Part C (new in 1a) covers every review fix: the PPL engine equals its Python replica (table to 1E-11, F(q) and q crit
to 1E-10); the accuracy grid over k 2-12 × 16 df × 4 α against SciPy (worst q crit 2.2E-4 relative, tail 6.7E-4 of α,
pair p 2.7E-6 absolute; 6-23 evaluations per q crit, median 13); statement counts beta 1 vs 1a (table in the CHANGES
file); Holm default and no Tukey work on page entry; "Not now"; Esc inside the table build; the step count past 12;
one-pair Tukey p; Cells page on 6×6, 3×4, 4×6, 6×2 designs; the interaction wording (non-significant and significant);
the chi-square upper tail at df 1E4-1E6 and n up to 1E6; the Checks wording; 2,997 values (Working page, Esc, the
Dots cache drawing the dots once); the fallback group picker, integer factor labels, the header text. Every page of
every run is also held to a 6.4-px-per-character width model: 0 lines too wide.

Beta 1's checks, kept and adapted to the new defaults and wording:

- One-way on the 3 presets + 26 random sets (ties, zeros, negatives, a 1E6 offset, unequal spreads, k 2-9) +
  5 edge sets (two groups of 2, a group of 1, a group with s = 0, a degenerate Levene, k = 12) + α = 0.01:
  F, p vs f_oneway; SS, eta², omega²; Welch F/df/p vs statsmodels anova_oneway(use_var='unequal'); Levene vs
  levene(center='median'); Bartlett vs bartlett; every pair's diff, SE, raw p, Bonferroni, Holm (multipletests),
  Scheffe; t crits. Tukey q crit vs studentized_range (rel 2E-5) and Tukey p and CIs vs tukey_hsd on presets
  and 4 random sets (k = 12 draft included). Refusals (SSW = 0, N = k) give one message, no crash.
- Two-way: mock jury + 22 random designs (2-4 × 2-4, unbalanced and balanced) + a 6 × 6 unbalanced design:
  SS, df, F, p, partial eta² vs anova_lm typ=3 (Sum); balanced: classical SS = typ=2 = Type III; cell means, n;
  an empty cell refused. Matrix inverse vs numpy (sizes 1-16), singular flagged.
- Blocks: judges + 20 random designs: F, p vs AnovaRM; SS vs ols additive model; the one-way comparison F.
- Variances: 32 cases incl. n = 500 (SDINT failed above 75), a p near 1E-50, all three alternatives:
  statistic, both tails, p, CI ends and order, crit values, the equal-area points vs scipy chi2/f.
- Special functions: betainc, gammaincc, F/χ² tails, quantiles.
- Pages: every menu path driven in the harness (one-way all pages/methods/Tukey p/pair taps/Set α/Help; draft and
  insect presets with scrolling; two-way all pages, Swap, taps; blocks; variances typed and from groups; my data
  one-way, two-way with recoded factors, blocks, and three refusals), numbers read ON the pages against
  SciPy/statsmodels; no runtime error, no scientific `E`, no MSGBOX over 5 lines, no text clipped or off screen
  (harness width estimate), the source line on screen. Run again with `stale_keys=True`: no skipped page.
- Gate (`ppl_gate_v1c.py`): kit lint 0 errors; ppl_check clean; lint_ppl 5 problems, all known noise ("no function
  named AnovaLab_beta1", four EXPORT-discipline lines); full parse fails at the first file-level LOCAL (the known
  kit limit; ChiTable and TrendTest fail the same way); fleet_names 0 collisions, 0 untagged, 0 built-in matches.

## Triola / TI programs reworked, bugs not repeated

ANOVA (0 and negatives read as missing), the TI-82 suite's `/ABN` implied multiplication, TUKEY (n_J for the
second group, no q crit), LATINSQ (treatment p from SS), FINTRVAL (swapped bounds), SDINT (solve bracket at 100,
fails n > 75), ANCOVA1 (equal n; not carried), ALLREG-style best-R² (not offered). All listed in the header and on
help page 8.

## Left out, and why

- No MicroPython engine (spec): Tukey uses StudRange's PPL engine only. df error must be ≥ 3 for Tukey (the page
  says so and points to Bonferroni/Holm/Scheffe).
- No CAS (nothing here needs an exact form).
- No Latin square or ANCOVA (not on the spec's menu); no post hoc for two-way or blocks (beta 2 candidates).
- No sphericity correction for repeated measures (help page 5 names the assumption).
- Two-way limited to 6 × 6 levels; data limited to 3000 values (G1 speed).

## Most likely to go wrong on a real G1

1. **Speed of Tukey** (now smaller and on request). G1 estimates on the warning use 5-15 ms per inner step (the second
   review's figure from StudRange's timings): jury q crit about 33-100 s, draft q crit about 43-129 s, the draft's 66
   Tukey p a further 64-193 s. The stopwatch times below replace these.
2. **Untested call shapes:** `CHOOSE(var, title, listVariable)` in the variance group picker (now inside IFERR with a
   literal-menu fallback); σ in DRAWMENU labels (`1 σ`, `2 σ`); `BLIT_P(G2, 0, 0, G1)` and `BLIT_P(G1, 0, 0, G2)` for
   the Dots cache (the 4-argument form is verified only with G0 as target); `MAKELIST` reading its LOCAL counter.
3. **Widths:** every line fits a 6.4-px-per-character model (stricter than the harness), but proportional glyph widths
   on the device may still clip one or two lines; 12-digit arithmetic on data with a huge common offset.

## DEVICE CHECKLIST (in order; expected numbers from SciPy/statsmodels)

1. Paste, Check in the Program Catalog, run `AnovaLab` from Home. Opening page: "AnovaLab - beta 1a", the red
   DISCLAIMER panel (4 lines).
2. One-way ANOVA (mock jury). Band "One-way ANOVA: N = 114, k = 3". Table: SS 70.94 / 1421.3 / 1492.3, df 2 / 111 / 113,
   F = 2.770, p = 0.0670; eta² = 0.048, omega² = 0.030; "Welch: F = 2.340, df 2, 71.5, p = 0.1036"; green verdict.
3. Checks: Levene F = 4.029, df 2, 111, p = 0.0205 (red, "evidence the spreads differ"); Bartlett χ² = 6.920, p = 0.0314;
   "Largest s / smallest s = 1.55 (a description)"; bottom line "Levene: spreads differ, so read Welch's F."
4. Pairs: opens instantly on the **Holm** tab (no Working page). Holm p: Beaut-Avg 0.6601, Beaut-Unatt 0.1494,
   Avg-Unatt 0.0847 (Bonferroni: 1.0000 / 0.2241 / 0.0847).
5. Tap the Tukey tab: a menu titled "Tukey q crit: about 33-100 s on a G1" appears. Choose "Not now": the page says
   "q crit not computed". Then More > Tukey p > "Compute it now": **time q crit with a stopwatch from the tap to the
   pairs page (jury)**; watch the step label count ("step n (q crit takes 6 to 23)", 9 steps expected) and the thin
   inner bar move. q crit = 3.3596; Tukey p = 0.8985, 0.1746, 0.0717; CIs (-1.578, 2.297), (-3.428, 0.4734),
   (-3.800, 0.1262).
6. Esc test: Set α 0.01 (q crit is forgotten), pick Tukey, "Compute it now", press Esc after a second or two: it should
   stop within a moment (not after a whole step) and the page says q crit not computed. Set α back to 0.05.
7. Dots: tap two groups (orange frames, bracket, panel "Beaut-Unatt: diff -1.477, CI (...)"); Left/Right step pairs;
   Menu > "Tukey p for this pair" computes one pair only. Note how fast a redraw is after the first.
8. F page: red line at 2.770, shaded tail, dotted crit, "F < crit 3.078: do not reject H₀ (α = 0.05)".
9. Load a preset > Draft 1970: F = 2.463, p = 0.0056, Welch p = 0.0038; Checks bottom line "Welch's F (Table page) is
   safe either way."; Dots with 366 dots (time the first draw, then a tap). Pairs on Holm, scroll to row 66.
   **Time the draft's q crit with a stopwatch** (Tukey tab > Compute it now; k = 12, df = 354: q crit 4.6529, 13 steps),
   then More > Tukey p for the 66 pairs (time it; Esc partway, then run again: only the rest are computed).
10. Insect sprays: F = 34.702, p < 0.0001; Welch 36.065 (df 5, 30.0); Levene p = 0.0042; F page off-plot arrow.
11. Two-way: A 76.98 (F 3.042, p 0.0518), B 2.497 (0.197, 0.6577), A×B 52.76 (2.085, 0.1293), Error 1366.4 df 108;
    verdict "No evidence of interaction at α = 0.05 / (p = 0.1293). Main effects are averages over / a pattern that
    may still be there: see Plot." Cells: tap Unattract./Swindle → "x̄ = 7.000, n = 17", s = 4.899; arrows move the
    red cell. Plot: "Parallel = no interaction. These lines cross, / but p = 0.129 (n 17-21) cannot rule out chance."
12. Use my data, two-way with 6 levels in D2 and 6 in D3 (codes 1-6, y around 100): Cells page shows every cell
    without cut text; labels "A=1" ... "B=6".
13. Randomized blocks: Treatment F = 21.349, p < 0.0001; "One-way, blocks ignored: F 3.118, p = 0.0477".
14. Variances > Type s and n: s 2, n 12; σ₀ 3, conf 0.95; ≠: χ² = 4.889, p = 0.1271, crit lower 3.816 upper 21.920,
    95% CI for σ² (2.007, 11.531). Large n: s 1, n 1000000, σ₀ 1.001, H₁ σ > σ₀: p = 0.9211 (beta 1 showed 0.9381).
    Soft key `2 σ` > Two groups: **this is the CHOOSE with a list variable** — if a list of groups appears, it works;
    if instead a three-item menu "This one / Next group / Cancel" appears, the list form failed and the fallback ran
    (tell Claude). Beautiful, Unattractive, 0.9, ≠: F = 0.6089, p = 0.1344, 90% CI (0.3511, 1.0508). Check the σ
    glyphs on the soft keys.
15. Large data: fill D1-D9 with about 330 values each (e.g. `D1:=RANDNORM(50,10,330)` style entries in the Statistics
    app) → One-way: a Working page with a bar appears (time it; Esc stops with "Stopped (Esc)"); then Dots (time the
    first draw and a later tap).
16. With the Statistics app never opened: Use my data gives three clean messages. Help: 8 pages (page 3 states the
    Tukey accuracy). Quit: Home shows "AnovaLab: ..."; AV_F etc. hold the last analysis.
