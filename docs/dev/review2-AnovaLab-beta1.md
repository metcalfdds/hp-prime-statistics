# AnovaLab beta 1: independent second review (21 Oct 2026)

Reviewer: second reviewer (did not write the program). Read in full first: `ref/HP_Prime_Lessons_Learned_v7n.md`, `BRIEF_NEW6_v1.md`, the builder's NOTES, then all 3,359 lines of `AnovaLab_beta1.txt`. `AnovaLab_beta1.txt` was NOT edited.

My own checks: `build/AnovaLab/review2_check_AnovaLab_beta1.py` (written from scratch, not from the builder's verify): **179 checks, 0 failures** against SciPy / statsmodels. Also a Python replica of the Tukey engine (it reproduces the program's q crit to 12 digits), sweeps of that engine and of cheaper ones, and harness runs of large and awkward inputs. The builder's `verify_AnovaLab_beta1.py` was re-run under the new kit interpreter (`interp.py` changed 13:38 and now refuses `+` with a list operand): **6770 checks, 0 failures**.

Ranked most serious first. CONFIRMED = reproduced here; PLAUSIBLE = reasoned, not reproducible off the device.

---

## 1. Tukey takes minutes on a G1, and opening Pairs or Dots starts it automatically. PLAUSIBLE (timing); call counts CONFIRMED

**Lines:** 2327 (`IF (avScr == 3 OR avScr == 4) AND avMeth == 1 AND avQc == -1 THEN av_TukeyCrit()`), 1156-1194 (`av_TukeyCrit`, `av_TukeyP`), 654-731 (engine), 218 (`avMeth := 1`, Tukey is the default).

**What is wrong.** Each CDF evaluation costs (64+1) outer × (32+1 or 48+1) inner iterations. Each inner iteration does one `NORMALD_CDF`, a power, a multiply and three list reads. I counted the calls in the harness and in a Python replica that matches the program's q crit to 12 digits:

| Case | Evaluations | NORMALD_CDF calls | Harness |
|---|---|---|---|
| Jury q crit (k 3, df 111, α .05) | 9 | 19,338 | 3.6 s |
| Jury q crit, α .001 | 16 | 34,353 | 6.1 s |
| Insect q crit (k 6, df 66) | 13 | 41,454 | 7.3 s |
| Insect Tukey p (15 pairs) | 15 | 47,775 | 8.6 s |
| Draft q crit (k 12, df 354) | 12 | 38,269 | 6.5 s |
| Draft q crit, α .001 | 19 | 60,564 | 9.5 s |
| **Draft Tukey p (66 pairs)** | 66 | **210,210** | **35.7 s** |

**G1 estimate.** Two independent estimates agree on about 5-15 ms per inner iteration on a G1:
- the brief's rule (G1 is 30-100 × the harness): 0.17 ms × 30-100;
- StudRange's own figures: this same PPL engine takes "about a minute" for a q crit on a G2. The Python path was 1.5 s on the G2 and 7 s on the G1, so the G1 is about 4.7 × slower.

That gives:
- jury q crit: **about 1.5-5 min**;
- insect or draft q crit: **3-10 min**;
- insect Tukey p: 4-12 min;
- **draft Tukey p: 20-50 min**.

The progress page promises "half a minute or more for each step". A step is 10-50 s, and Esc is seen only between steps.

**Failure scenario.** A student loads the mock jury and taps Pairs (or Dots, or `+/-` back to Tukey). The default method is Tukey, so the calculator freezes behind a progress bar for minutes. After Set α it happens again. With the draft data, "Tukey p" outlasts the class.

**Fix (checked against SciPy).** The inner integral P_k(x) depends only on k. Tabulate it once per k at x = 0, 0.1, …, 12: 121 points × the same 33/49 Simpson nodes, which is 4.0k / 5.9k NORMALD_CDF calls. Then read it in the outer loop by 4-point cubic Lagrange interpolation, with P_k(x) = 1 for x ≥ 12. Keep the table across Set α and Tukey p. Keep the outer 64-interval Simpson and the u² substitution.

Accuracy over k ∈ {2,3,4,6,8,12}, df ∈ {3,5,10,20,40,111,354,1000}, α ∈ {0.2,0.05,0.01,0.001}: worst relative error in P(Q > q crit) is **5.8E-4**. That is the same as the current engine (6.1E-4, worst at k 12, df 3, α .001). A coarser table (step 0.2, 61 points) gives 1.5E-3.

Fewer nodes do not work. Gauss-Legendre with 12-24 outer × 12-24 inner nodes oscillates above 1, so `1 − F` is wrong by up to 0.24 at α = 0.001 (sweep in the scratchpad). Do not take that route.

Cost with the table, counting one interpolation as one or two inner iterations:
- jury q crit: about 6k instead of 19k, roughly 3 × faster;
- draft q crit plus all 66 Tukey p: about 22k instead of 248k, roughly 11 × faster.

On a G1 that is about 0.5-1.5 min for the jury and 2-5 min for the whole draft, instead of 20-50 min.

**Also:**
- Do not start Tukey automatically on entry to Pairs or Dots. Show Bonferroni or Holm by default and draw a "Compute Tukey (about N s on a G1)" button.
- Put the measured G1 time on the progress page once Roger has timed it.

## 2. The Cells page cuts off every cell mean when B has 4 or more levels. CONFIRMED

**Lines:** 2428 (`tcW := MIN(80, IP(236/(avTNB + 1)))`), 2433, 2436, 2444, 2455, 2462 (`tcW - 6`).

**Reproduction.** Use my data → Two-way with D2 holding 6 codes, D3 holding 6 codes and y around 120. The harness flags **49 clipped strings** on the Cells page:
- `x̄ 118.42` in a 27-px field;
- `B=10.00` in 29 px;
- `A margin` in 33 px.

A 3 × 4 design still clips (41 px for `x̄ 118.42`). The builder's "no text clipped" check never drove a design with this many levels on the Cells page.

**Fix:**
- Drop the "x̄ " prefix inside cells; the header already says "Cell means".
- Print means with `av_Gn` limited to about 4 significant digits.
- From 4 levels of B, use a smaller font or transpose so the longer factor runs down the page. Or, from 5 levels, show "n" lines only on tap.

## 3. Two-way wording when the interaction is not significant (mock jury, p = 0.129): partly overclaims. CONFIRMED (screen text)

**Line 2417-2418** (Table verdict, green): "No evidence of interaction (p = 0.1293): / the main effects A and B can be read on their own."

The first line is honest. The second treats "no evidence" as "no interaction", which the brief forbids. The cell means are 7.0 for unattractive swindlers against 3.5-4.8 elsewhere, and each cell has only 17-21 people.

Suggested text: "No evidence of interaction (p = 0.129); not proof of none. / Main effects are averages over the other factor: see Plot."

**Line 2576** (Plot page): "Parallel lines = no interaction (p = 0.1293)". Under visibly crossing lines, this reads as a claim that the lines are parallel. Suggested text: "Parallel lines would mean no interaction; test: p = 0.129".

Help page 4 (lines 2116-2118) handles the case well. The figures it quotes are correct: cell means 3.5-4.8 and 7.0, n from 17 to 21, p = 0.13.

Side note for Roger: `data/DATASETS.md` says the MockJury cells hold 18-21. They hold 17-21 (Unattractive/Swindle has 17). The program is right.

## 4. The one-σ upper tail is wrong for very large n. CONFIRMED

**Lines:** 526-540 (`av_GamP`, 500-term cap), 545-567 (`av_GamQ`), 596, 1509.

For x < a + 1, `av_GamQ` returns 1 − P(a, x) from a series capped at 500 terms. With a = df/2 in the tens of thousands, the series needs about √(54a) terms. The form allows n up to 1,000,000.

| n | σ₀ | Program upper tail | SciPy upper tail |
|---|---|---|---|
| 50,000 | 1.005 | 0.942079 | 0.942078 |
| 100,000 | 1.0005 | **0.5948** | **0.5879** |
| 1,000,000 | 1.001 | **0.9381** | **0.9211** |

So with H₁: σ > σ₀ the screen prints a wrong p in the second decimal, and the two tails do not add to 1. The two-sided p uses the smaller tail, which is right, so it is unaffected.

**Fix:** in `av_ChiUp`, when x ≤ df (the upper tail is then at least about 0.5, so nothing cancels), return `1 − CHISQUARE_CDF(df, x)`. The df is always whole here. Alternatively, cap typed n at 10,000.

## 5. The Checks page gives contradictory advice, with an unsourced rule of thumb. CONFIRMED (jury preset)

**Lines 1744-1747.** For the mock jury, Levene shows red, "→ evidence the spreads differ" (p = 0.0205). Directly below, in magenta: "Largest s / smallest s = 1.55 (under 2: usually fine)". The "under 2 / use Welch" rule has no source on the page or in the header.

Fix: name it as a rule of thumb with its source, or drop "usually fine". For example: "s ratio 1.55 (a rule of thumb: under 2); Levene above is the test; Welch is safe either way."

## 6. Large data sets run with no progress indicator and no Esc. PLAUSIBLE

**Lines:** 1073-1079 (medians: k passes over all N values with a growing `CONCAT`), 3212-3215 (`av_LevOf` per value), 1964-1971 (Dots draws every value on every redraw).

Harness timings and G1 estimates:

| Step | Harness | G1 (× 30-100) |
|---|---|---|
| 9 lists × 333 values: read + `av_OCompute` | 2.0 s | 1-3 min, blank screen |
| Two-way 6 × 6, N = 3000: `av_MyTwo` | 3.1 s | 1.5-5 min |
| Dots page redraw, 3000 dots | 0.4 s | 12-40 s per tap |

Fix:
- Build each group once into a pre-sized list (MAKELIST, then fill in place, the idiom already used at 3176-3180), then `SORT` it.
- Show a "Working…" page before any pass over N > 500.
- Lower the cap to about 1000 values, or say on screen how long it may take.

## 7. `CHOOSE(pgI, pgT, pgL)` with a list variable. PLAUSIBLE (untested call shape)

**Line 2950.** The Lessons Learned and the brief document only the literal list form `CHOOSE(var, "title", {...})`. No fleet program passes a list variable; the only other hit, FitCheck line 2924, uses a literal. hp-prime-kit's CHOOSE entry gives only the multi-string form. I could not reach the HP manuals: there are no PDFs in this container.

A list is a value, so it will very likely work. If it does not, it fails at run time (the Program Editor opens), and it is the only way into "groups of the one-way data" in Variances.

Keep it early on the device checklist; the builder's item 13 has it. Fallback if it fails: a literal 12-entry `{avON(1)…}` list cannot shrink to k items, so instead page through groups with a 3-item CHOOSE ("this group / next / cancel").

## 8. The progress bar fills after 12 steps, but q crit takes 9-19. CONFIRMED (counts)

**Lines 769-781** (`av_PrgStep(crE, 12)`). Jury at α .001 takes 16 evaluations; draft at α .001 takes 19. The bar sits full for 4-7 more steps, which is minutes on a G1, and looks hung.

Fix: pass 20 and label it "step n (usually 9-19)", or move the bar by |F − (1 − α)| on a log scale.

## 9. User-data factor labels print as decimals. CONFIRMED

**Lines 3219-3220** (`"A=" + av_Gn(...)`). Codes 1, 2 show as "A=1.000"; 10, 20 as "B=10.00". This also feeds finding 2. Use `av_I` when `FP(v) == 0`.

## 10. Smaller items

1. **Header line 43** says AV_ETA2 is "partial eta^2 of the last effect shown". After a two-way it is always A × B (line 1405), and after blocks always treatments (1465). AV_F and AV_P are likewise always the interaction. Reword the header and help page 7. CONFIRMED.
2. **Line 1861.** "PPL engine below α 0.005: may be a few % off" over-warns for this program's range (k ≤ 12, α ≥ 0.001). My sweep's worst relative p error is 6E-4 and q crit agrees with SciPy to about 1E-6. Say "slightly less accurate" or drop it. CONFIRMED.
3. **Line 1488.** `CHISQUARE_ICDF(df, 1 − av_Clp(p))` is the right-tail-quantile form the Lessons (§3) say never to use. The clamp stops it reaching ∞, so it only blurs the equal-area shading when p < 1E-10. Mirror it the way `av_FQ` does if convenient. CONFIRMED (cosmetic).
4. **Line 3082.** σ inside the DRAWMENU labels ("1 σ", "2 σ") has not been seen on a calculator (the builder flagged this). PLAUSIBLE, low.
5. **Lines 1330 / 1361.** `tcR` holds a list (`av_TRow`) and later a real. This is legal, but rename one of them for readers.

## List arithmetic (the lead's added item): no finding

- **Static scan:** I found 95 list-valued names (assigned from `{}`, MAKELIST, CONCAT, SORT, `av_ReadD`, `av_Levels`, `av_TRow`, `av_TRange`, MOUSE, plus copies). None is an operand of `+ − * / ^` without an index. The two hits the scan reported are scalars at that point: `tcR` at line 1364, reset to 0 at line 1361, and `tcY` in `av_TDrawCells`, a different routine's real.
- **Literals:** there is no `{…} +` or `+ {…}` anywhere.
- **Appends:** all use `CONCAT(list, {x})` (lines 1076, 2947, 3145, 3169-3172, 3219-3220, 3242, 3258).
- **Dynamic check:** the builder's full verify, which drives every menu path, passes 6770/0 under the interpreter that refuses list `+`. The scan script is in my scratchpad (`listarith/scan.py`).

## Checked and found correct

**One-way** (presets and seven awkward sets: a group of 1; groups of 2; a zero-variance group; zeros and negatives; k = 2 with df = 3; a 1E6 offset; all values equal):
- F, p, SS, η², ω² (Hays' (SSB − (k−1)MSW)/(SST + MSW)) match `f_oneway`.
- Welch's F, its fractional df and p match `anova_oneway(use_var='unequal')`. The fractional df goes only to the program's own incomplete beta, never to FISHER_CDF.
- Levene (median) matches `levene(center='median')`; Bartlett matches `bartlett`.
- Welch and Bartlett are hidden for n = 1 or s = 0 and Levene still runs. The all-equal set is refused with one MSGBOX.
- Every value counts: 0 and negatives are kept (the TI ANOVA bug is not repeated).
- Bonferroni, Holm and Scheffé: the formulas are standard; the Scheffé multiplier is √((k−1)F crit) and Scheffé p comes from t²/(k−1) on F(k−1, N−k). The builder's verify checks the values and still passes (above); my own script did not re-check them.
- **Tukey-Kramer:** q crit matches SciPy (jury 3.35955 vs 3.35955, insect 4.15085, draft 4.65294). The jury p-values are 0.89849 / 0.17459 / 0.07173, matching `studentized_range`. CIs are diff ± q crit/√2·SE with each pair's own n. The awkward sets agree within 5E-4.

**Two-way:** the Type III SS and p match statsmodels `anova_lm(typ=3)` with Sum contrasts on:
- the jury (A 76.98, B 2.497, A × B 52.76, error 1366.4, interaction p = 0.1293);
- an unbalanced 3 × 3 with one-value cells and zeros/negatives;
- a 6 × 6 unbalanced design.

The effect-coding column layout is right (A in 2..a, B in a+1..a+b−1, A × B from a+b). An empty cell is refused by name.

**Blocks:** the judges give F = 21.349 and p = 3.19E-8 (`AnovaRM`), and F = 3.118, p = 0.0477 when the blocks are ignored (`f_oneway`).

**Variances:**
- The χ² and F statistics, the tails and the two-sided p (2 × the smaller tail) are right for all three alternatives, and also for n = 2 each and 99.9 %.
- The CI for σ² is ((n−1)s²/χ²_upper, (n−1)s²/χ²_lower).
- The CI for σ₁²/σ₂² is (F·F_{c/2}(df2, df1), F/F_{c/2}(df1, df2)), which equals the textbook (F/F_{1−c/2}(df1, df2), F/F_{c/2}(df1, df2)). FINTRVAL's swap is not repeated.

**12-digit and ICDF safety:**
- Every upper tail is a lower-tail form.
- Every `_ICDF` probability is clamped into [1E-12, 1 − 1E-12].
- The F critical value is `1/FISHER_ICDF(d, n, α)`.
- The engine's normalising constant is computed in logs.
- No ∞ path was found from typed input, since α is limited to 0.001-0.2 and the confidence level to 0.5-0.999.

**Device rules:**
- At most 6 names on every LOCAL line, all at the top of their blocks.
- No `//` comment inside an open bracket; capital-E exponents.
- `CHOOSE` index set to 0 first and tested; no numbers in menu strings.
- `INPUT` targets are LOCALs, never parameters.
- MSGBOXes stay within 5 lines (harness check).
- Drain / wait / drain, with the finger-lift drain capped by TICKS; soft keys read with y ≥ 218 and `MIN(6, IP(x/53.4)+1)`.
- `RETURN "AnovaLab: …"` at the end.
- The `D1`..`D9` reads are inside IFERR.
- Esc is honoured between Tukey steps, and a stopped q crit is not restarted automatically.

**Data:** every preset literal equals its CSV: MockJury Years/Attr/Crime in row order, the 366 draft numbers, InsectSprays, and the judges' INTG/DMNR/DILG row-major.

**Style:**
- The header matches the brief: copyright, DISCLAIMER, AI credit, sources, data lines, the reworked programs, and a file map whose line ranges are exact.
- The DISCLAIMER is shown on the opening page.
- Pure ASCII, LF, no CR. Glyphs are built with CHAR(); η and ω are spelled out, as the brief requires.
- Every helper is tagged `av_`.
- The palette is the house palette; footers use the canonical form.
- The source citations (Welch 1951, Brown & Forsythe 1974, Bartlett 1937, Kramer 1956, Holm 1979, Scheffé 1953, Levene 1960) carry the right volume and pages. Triola's TI ANOVA does print "HAY'S W² STAT", as the header says.
