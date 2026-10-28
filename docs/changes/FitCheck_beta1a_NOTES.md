# FitCheck beta 1a — notes (21 Oct 2026)

**beta 1a** applies every item of `REVIEW2_FitCheck_beta1.md` (see `FitCheck_beta1a_CHANGES.md`).
The file is `/home/claude/new6/FitCheck_beta1a.txt`, 3,231 lines; the longest source line is 229 characters.
`verify_FitCheck_beta1a.py` gives **3976 checks, 0 failures**. The gate (`gate_FitCheck_beta1a_output.txt`) passes.
The beta 1 notes follow. Where beta 1a changed something, the text below has been updated: the draft lottery, Lilliefors for small n, the Benford two-digit rule, Castaneda, and the checklist.

`/home/claude/new6/FitCheck_beta1a.txt` (beta 1 was 2,987 lines), pure ASCII, LF. Entry `EXPORT FitCheck()`, which takes no arguments and opens on its menu. Tag `fc_`: every helper is `fc_Name`, every file-level LOCAL is `fcName`, and the Home exports are `FC_…`. The source is assembled from `build/FitCheck/parts/*.txt` by `build/FitCheck/assemble.sh`. The parts are the working copy; the assembled file is the deliverable.

It has run only in the PC harness (ppl_run_v3e). It has not run on the emulator or on a calculator.

## What it does, menu by menu

The program opens on a title page that shows the DISCLAIMER on screen. The menu has 11 items (CHOOSE list form):

1. **χ² goodness of fit**: the last fit again; my counts in D1 with equal shares; my counts in D1 with shares in D2; preset draft lottery 1970; preset Castaneda as 2 cells.
2. **Benford's law**: preset Arizona v. Nelson; my values in D1, first digit; my values in D1, first two digits.
3. **Poisson fit**: preset Richmond homicides; preset horse kicks; my counts of 0, 1, 2 … in D1.
4. **Binomial fit**: illustrative numbers, labelled on screen as made up; my counts of 0..n in D1. For your own data, p is estimated or typed as p₀.
5. **Normality: Q-Q, W, A², D**: the last sample again; preset Rossi ages; preset crimtab heights; my values in D1.
6. **Normality: χ² on bins**: the χ² normal fit on the loaded sample. The sparse tails are merged automatically, and Unmrg shows every bin.
7. **Exact binomial test**: the last test again; preset Castaneda v. Partida; typed x, n, p₀.
8. **Load a preset**: all 8 presets. Each preset opens with a page showing its source line, then its pictures.
9. **Use my data (D1, D2)**: 7 routes, plus a help page on how to fill D1 and D2.
10. **Help**: 7 pages. Esc leaves from any page.
11. **Quit**: returns a summary line, e.g. `FitCheck: χ²(1) = 7.082, p = 0.0078;`.

**Screens of a χ² fit.** Soft keys: Bars | Table | Curve | Test | Merge/Unmrg | Menu.

- **Bars.** Observed counts are blue. Expected counts are orange: pale bars beside the observed for up to 12 cells, or an orange curve over the bars for Benford and for many cells. Each cell's (O−E)²/E is a magenta bar in a strip below. The headline shows χ², df and p, coloured red when p < 0.05 and green otherwise. A second line gives the expected-count check. Tapping a cell, or pressing Left/Right, shows O, E, (O−E)²/E and (O−E)/√E.
- **Table.** 12 cells per page; Up/Down pages; tap a row to select it. A residual with |(O−E)/√E| ≥ 2 is red.
- **Curve.** The χ² density for df, cached per column. The tail beyond χ² is shaded and the 5% critical value is a dotted red line. When χ² is far out (Castaneda's 847.7), the page says "far off the chart" rather than squashing the curve.
- **Test.** Wrapped text with paging. It shows H₀, the source, the arithmetic, df = k−1−m, p (a tiny p is printed from its log, e.g. `p = 2.32 × 10^-186`), the decision ("no evidence of a departure … which does not prove …"), the expected-count check, exactly which cells were merged, and the notes for the kind of fit (MAD, λ̂, p̂, x̄ and s, Chernoff–Lehmann). It also carries each preset's talking point.

**Normality screens.** Soft keys: Q-Q | ECDF | Tests | Bins | – | Menu.

- **Q-Q.** Each value plotted against its Blom normal score, with the line x̄ + s·z. Tap a point, or use Left/Right (or Up/Down to jump n/20 points), to see x(i), its rank and z. Binned data (crimtab) shows one point per bin: the bin's midpoint against the Blom score of the bin's middle rank, and the page says so.
- **ECDF.** The empirical CDF, the fitted normal CDF, and the largest gap D marked in red at the point where it occurs. Tapping a column, or pressing Left/Right, reads both curves there.
- **Tests.** W, A², A*², D with their p-values, a verdict across the three tests, skewness and kurtosis, a sentence on the Q-Q shape (e.g. "right-skewed … the points bend upward"), median versus mean, and warnings for large and small n.

**Exact binomial test screens.** Soft keys: Plot | Why | χ² | – | – | Menu.

- **Plot.** The binomial pmf over E ± 4.5 SD plus x. x is red; every k no more likely than x is magenta (these make up the two-sided p); the rest are blue. A second axis counts SDs from E. Tapping a bar shows P(X = k) and z; tiny probabilities are printed from logs.
- **Why.** E, SD and z written out. For Castaneda, it adds the Court's SD reasoning and describes footnote 17 without quoting it.
- **χ².** Runs the same question as a two-category χ², which equals z².

## Formulas and sources (each is also cited in the code)

- **χ² goodness of fit.** E = N·p_i; χ² = Σ(O−E)²/E; df = k−1−m (Fisher 1924). Check: every E ≥ 5, or Cochran (1954), at most 20% of the E below 5 and none below 1. **Every cell is checked.**
- **Upper tail.** df 1: 2Φ(−√x). df 2: e^(−x/2). Otherwise ln Q(df/2, x/2) by series or Lentz continued fraction (Numerical Recipes 2nd ed. §6.2). The tail is never computed as 1 − CDF. ln Γ uses Lanczos (g = 7, 9 coefficients, written to 12 digits).
- **Merge** (on request; automatic only for the normal fit on bins). While some E < 5 and k > m + 2, the cell with the smallest E joins its neighbour with the smaller E (left on a tie). Only adjacent cells are merged, so ordered scales stay ordered. The Test page lists each group, e.g. `{6, 7, 8, 9} → 6-9`. For the Nelson preset, Merge uses Triola's fixed grouping 1 / 2-5 / 6-9 instead.
- **Benford.** P(d) = log₁₀(1 + 1/d); P(ab) = log₁₀(1 + 1/(10a + b)), using the significand, with zeros skipped and counted. In the two-digit test, numbers below 10 are left out and counted (beta 1a), and a MSGBOX says how many. MAD = (1/K)Σ|actual − Benford| over all K cells (Nigrini, *Forensic Analytics*, 2011/2020). **Nigrini's conformity ranges are not shown.** No file readable here contains them (data/, ref/, the fleet, Community_Library and the Python packages were searched for "Nigrini"), so the Test page says so and shows only the MAD.
- **Poisson.** λ̂ = Σxf/N. The cells are 0..K−1 plus a tail cell "≥K" with E = N·P(X ≥ K), summed from positive terms, so the expected counts add to N. df = k − 2.
- **Binomial fit.** p̂ = Σxf/(nN) with df = k − 2, or a typed p₀ with df = k − 1. E uses `BINOMIAL(n, p, k)`.
- **Normal on bins.** End cells are open. Each middle cell's proportion is Φ(z_hi) − Φ(z_lo), or its mirror above the mean. df = k − 3. For raw data the bins are (a, a + w]: Sturges' count, with w the nearest 1/2/5 × 10^e, and x̄ and s from the raw values. The Test page notes Chernoff & Lehmann (1954): the true reference lies between χ²(k−3) and χ²(k−1).
- **Q-Q.** Blom positions (i − 3/8)/(n + 1/4). Half the scores are computed and half mirrored, and the middle of an odd n is exactly 0 (the NMLPROB bug avoided).
- **Shapiro–Wilk.** Royston (1995), AS R94, as in R's and SciPy's swilk; valid for 3 ≤ n ≤ 5000. For n = 3, p = 3·ASIN(√W)/ASIN(1) − 2, which is the same in any angle mode.
- **Anderson–Darling.** A² with ln(1 − Φ(z)) taken as ln Φ(−z), and an asymptotic ln Φ below z = −30. A*² = A²(1 + 0.75/n + 2.25/n²). p comes from the four D'Agostino & Stephens (1986) formulas, with A*² > 13 reported as p < 0.0001, exactly as statsmodels' normal_ad does.
- **Lilliefors D** (K–S with x̄ and s). p comes from the Dallal & Wilkinson (1986) formula, given only for n ≥ 5 (beta 1a) and only when it is ≤ 0.10. Otherwise the page says "p > 0.10" (`FC_PD = -1`), or for n < 5 "p not available for n < 5" in grey (`FC_PD = -2`, left out of the verdict). This is statsmodels' `pvalmethod='approx'` below 0.10; above 0.10 statsmodels switches to its own table, which FitCheck does not carry.
- **Exact binomial test.** Two-sided p = the sum of P(X = k) over every k with P(X = k) ≤ P(X = x)(1 + 1E−7). This is SciPy's binomtest "minlike" rule, with the far side found by bisection. Tails are summed away from the mode, all in logs.

## Presets (only data/DATASETS.md; the source line shows on screen when loaded)

| Preset | Data | Result (harness = SciPy) |
|---|---|---|
| Arizona v. Nelson | 23 cheque amounts (DATASETS row; Triola p. 653): first digits 1,1,0,0,0,0,3,9,9 | 9 cells: χ² = 129.95, df 8, p = 2.89×10⁻²⁴, 8 of 9 E < 5 (rule fails). Triola merge 1 / 2-5 / 6-9: O 1, 1, 21; E 6.92, 10.97, 5.10; χ² = 63.66, df 2, p = 1.5×10⁻¹⁴. MAD = 0.1685 |
| Castaneda v. Partida | 339 of 870, p₀ = 0.791 | E = 688.17, SD = 11.993, z = −29.11. Exact two-sided p = 4.18×10⁻¹⁴⁵ (= P(X ≤ 339)). Two-category χ² = 847.68, p = 2.32×10⁻¹⁸⁶ |
| Richmond 1991 | 268, 79, 17, 1 | λ̂ = 0.3178. 4 cells: χ² = 1.518, df 2, p = 0.468, rule fails (E≥3 = 1.6). Merged {2, ≥3}: χ² = 0.989, df 1, p = 0.320 |
| Horse kicks | 144, 91, 32, 11, 2 | λ̂ = 0.700. χ² = 1.979, df 3, p = 0.577 (Cochran OK). Merged {3, ≥4}: χ² = 1.952, df 2, p = 0.377 |
| crimtab | 22 height bins summed over finger length (= the CSV; 3000) | x̄, s from midpoints. Tails merged into 16 cells: χ² = 9.769, df 13, p = 0.713 |
| Rossi ages | 432 ages, rebuilt from their frequency table (identical to the CSV) | W = 0.8499, p = 7.09×10⁻²⁰. A² = 20.940, A*² = 20.977, p < 0.0001. D = 0.1824 at x = 24, p = 1.66×10⁻³⁹. g₁ = 1.39. Bins (width 2): χ² = 246.3, df 9 |
| Draft lottery 1970 | all 366 numbers by month | **beta 1a: a 2 × 2 table.** Jan–Jun 73 low / 109 high; Jul–Dec 110 low / 74 high (E 91, 91, 92, 92). Pearson χ² = 14.164, df 1, p = 0.000168. Fisher exact (hypergeometric) p = 0.000243. The fixed-share GOF (χ² = 7.082, p = 0.0078) is shown only as the teaching point: it understates the evidence because the numbers were drawn without replacement. Monthly counts 12, 12, 10, 11, 14, 14, 14, 19, 17, 13, 21, 26 |
| Binomial (illustrative) | 6, 27, 42, 20, 5 groups of 4, labelled made up | p̂ = 0.4775, χ² = 1.206, df 3, p = 0.752 |

**Talking points.**

- **Nelson.** The Test page asks Triola's question, what argument the defendant's attorney might make. It then gives teaching points, labelled as not from the trial record: only 23 cheques; 21 of the 23 lie between 71,552.16 and 97,473.96, just under 100,000, while Benford needs amounts spread over several powers of ten; and a poor fit shows the amounts are unusual, not who wrote them or why. The actual defence argument is not in any source here, so none is claimed.
- **Castaneda.** The Why page describes footnote 17's "two or three standard deviations" rule of thumb and says it does not quote it.
- **Draft lottery.** The usual explanation, that the capsules were poorly mixed, is attributed to Fienberg (1971) and marked "not checked against the paper here".

## What was checked (beta 1: verify_FitCheck_beta1.py, 3810 checks, 0 failures; beta 1a: verify_FitCheck_beta1a.py, **3976 checks, 0 failures**; both outputs saved beside the scripts)

- **A1–A3.** ln Γ against gammaln, to 1e-10. ln Φ against log_ndtr, z from −60 to 10. The χ² upper tail against chi2.logsf/sf for df 1–150 and x up to 5000, compared in logs down to e^−2500.
- **A4.** Shapiro–Wilk on 306 samples: n = 3..50 × 6 kinds (normal, exponential, uniform, lognormal, t₃, rounded with ties), plus n = 100, 200, 500, 1000, 2000 and 5000. The largest difference from scipy.stats.shapiro in W or p was **7.6e-12**. n = 3 was also run in degrees and grads.
- **A5/A6.** 75 samples, n = 5..3000. A² matches scipy.anderson and statsmodels normal_ad; A*² and p match normal_ad. For one t₃ sample (n = 1000) statsmodels' A² overflows to ∞, while SciPy's and FitCheck's agree (13.738408). D matches statsmodels lilliefors, and p matches pval_lf (Dallal–Wilkinson) whenever that is ≤ 0.10; otherwise the page shows "p > 0.10".
- **A7.** 60 random fits: χ², df, p, E, residuals and the expected-count rule against scipy.stats.chisquare(ddof = m). Merging against an independent Python version of the documented rule, the merged test, and unmerging.
- **A8.** First digit and first two digits (including 0.3, 0.0299, 2000, negatives, 1.5e300) against a string reading. Counts, the Benford proportions (sum = 1), χ² and MAD on 12 random sets.
- **A9–A11.** Poisson (8 data sets, including only zeros/ones and trailing zeros), binomial (estimated and given p, degenerate cases) and normal-on-bins (crimtab, all 22 bins and merged) against scipy.stats.
- **A12.** Exact binomial test, 165 cases (Castaneda, edges x = 0, x = n, x = np, n = 1, n = 100000, and 150 random), against binomtest two-sided and binom.cdf/sf. The magenta region was checked k by k.
- **A13.** Edge inputs: n = 1, 2 and all-equal values refused with a message; ties; negatives; 1e9 + small; a value of 1000 among 1–4; zero counts.
- **B1–B13.** Every menu path through FitCheck() in the harness, including all 7 D1/D2 routes, 11 refusals and the typed test (5 cases plus 4 refusals). The numbers on the pages were checked against SciPy. Also checked: help (Esc leaves), the title-page disclaimer, the Quit summary, the Home exports, the menu-line lengths (≤ 30), and a degrees-mode run.
- **Every run:** no runtime error, no scientific STRING (`h.sci_strings` empty), no `ᴇ`, no text estimated wider than its box at 6.5 px per character or off the 320×240 screen, nothing under the soft keys, and no MSGBOX over 5 lines.
- **Gate** (`gate_FitCheck_beta1_output.txt`): kit lint 0 errors; ppl_check clean; fleet_names 0 collisions, 0 untagged, 0 built-in matches; RESULT PASS.
  - lint_ppl's 7 "problems" are the known noise (no function named after the file; EXPORT-discipline lines).
  - The full parse fails at line 132 ("expected a name after EXPORT"). This is the kit's known limit with file-level LOCALs after an EXPORT list; ChiTable fails the same way.
- The pages were also rendered from the harness's drawing log to PNG and inspected by eye. No CAS is used.

## Triola / TI programs reworked, and the bugs not repeated

- **X2GOF, ZSTCHISQ, GOFARB, GOFUNIFM, CHITESTS** (the GOF part): χ² goodness of fit with every cell checked.
- **GOFBIN, GOFPOISS:** binomial and Poisson fits.
- **GOFNORML, X2NORM2, ZSTCHINO:** the normal fit on bins.
- **KOLSMIR, CVMTEST1:** replaced by Lilliefors and Anderson–Darling.
- **NMLPROB, NRMLPRPL, ZSTNORMP:** the Q-Q plot.
- **BENFORD:** Benford's law.
- **Erdeky's CHISQ:** its wording.

Bugs avoided:
- X2NORM2 divided by the observed counts.
- GOFPOISS kept df = k − 1 after estimating λ and had no tail cell.
- GOFBIN, GOFARB and GOFNORML checked E < 1 for the first cell only (they reused the loop variable).
- CHITESTS applied the 20% rule to R + C cells.
- KOLSMIR used the plain K–S p with estimated parameters.
- CVMTEST1 ignored Stephens' correction, and one of its Ifs guards a single line.
- NMLPROB/ZSKNPROB left the middle point untransformed for odd n.
- Erdeky's CHISQ printed "INDEPENDENT".

## Left out, and why

- **Nigrini's MAD ranges:** no readable source, as explained above.
- **Lilliefors p above 0.10:** statsmodels uses its own simulated table there. FitCheck shows "p > 0.10" and does not carry a table it cannot cite.
- **W, A² and D on binned data (crimtab):** heavy ties break them. The page says so and points to the χ² fit on the bins.
- **Cramér–von Mises:** not in the spec; Anderson–Darling covers the EDF family with its correction.
- **The CAS:** nothing here needs an exact fraction. Huge and tiny numbers are handled in logs instead.
- **Typed data lists:** INPUT cannot take a list reliably, so data comes through D1/D2. The binomial test's x, n and p₀ are typed.
- **Normality data is capped at 5000 values**, Royston's limit. D1 counts are capped at 120 cells. The typed binomial n is capped at 100,000.

## The three things most likely to go wrong on a real G1

1. **Speed.** fc_NormSet on a large sample: Rossi's n = 432 costs about 216 NORMALD_ICDF, 864 LN(NORMALD_CDF) and 432 NORMALD_CDF calls. A Q-Q redraw costs 432 dots. n = 5000 from D1 could take a minute, and each Q-Q redraw several seconds. A busy box shows for n > 200. Castaneda's plot needs 278 fc_LPmf calls (Lanczos) when it opens.
2. **The list and string idioms** used here more than elsewhere in the fleet: nested list indexing `pdL(pdI)` then `pdR(pdN)`; `CONCAT` of strings into lists; IFTE with string results; INPUT labels built by expressions; `MAKELIST(0, var, 1, n, 1)` with a LOCAL counter. All are in fleet use or the brief, but this many in one program has not been run on a device.
3. **Layout.** Text widths were estimated at 6.5 px per character for font 1. The bin labels under crowded bars, and the merged labels such as "142.24-147.32" in the bars readout, may still touch on the real font. Also: the ≈ glyph is never used; ⇅ (8645) and ⇆ (8646) are used on the footers and help, and Lessons §13 lists them as rendering.

## DEVICE CHECKLIST (beta 1a; in order; expected numbers from SciPy)

0. **In Home, before anything else** (review 7, the ln Φ far tail): `NORMALD_CDF(0,1,-29.115)` should be about 1.161E-186, and `NORMALD_CDF(0,1,-37.5)` about 4.6E-308. If either shows 0 or an error, the tiny Castaneda χ² p and the tiny W/A² p-values will be wrong; report it.
1. Paste, then use Check in the Program Catalog. Run `FitCheck`. The title page should read "FitCheck - beta 1a" with the red DISCLAIMER. Any key opens the menu, which has 11 items (A, B last).
2. **Load a preset → Arizona v. Nelson.**
   - Bars: `χ² = 129.95, df = 8, p < 0.0001` and `8 of 9 E < 5: tap Merge`. Tap digit 9: `O = 9, E = 1.05`, `(O-E)²/E = 60.018, (O-E)/√E = +7.75`.
   - Merge: `χ² = 63.66, df = 2`, `every E ≥ 5`.
   - Test page: `MAD … = 0.1685`, the Nigrini sentence, and "Triola's question (p. 653, paraphrased)".
3. **Curve** (Nelson, before Merge): the shaded tail, the dotted red line at 15.51, "far off the chart", `p = 2.89 × 10^-24`.
4. **Load a preset → Castaneda.**
   - The source page ends "n. 17 at 496-497". Plot: `x = 339 of 870: two-sided p = 4.18 × 10^-145`, with "0" under E.
   - Why: `= 688.17`, `= 11.993`, `= -29.11 SDs`, "430 U.S. at 496-497 n.17", the quoted words "approximately 29 standard deviations", "less than 1 in 10^140".
   - χ² key: `χ² = 847.68, df = 1`, Curve `p = 2.32 × 10^-186` (this needs item 0 to pass).
   - Also reach Castaneda through "χ² goodness of fit → Preset: Castaneda, 2 cells": the source page now appears there too.
5. **Poisson → Richmond:** `χ² = 1.52, df = 2, p = 0.4682`. After Merge: `χ² = 0.99, df = 1, p = 0.3201`, with the last label `≥2`. **Horse kicks:** `χ² = 1.98, df = 3, p = 0.5768`, `1 of 5 E < 5: Cochran OK`.
6. **crimtab** (the beta 1 crash path):
   - Q-Q: 20 dots, the first reading `bin 142.24: 1 value, z = -3.529`.
   - Bins: `χ² = 9.77, df = 13, p = 0.7127`.
   - **Unmrg, then Bars:** all 22 bins drawn (labels 142 … 196) with no error. Then Table, Test, and "χ² goodness of fit → The last fit again" → Bars.
7. **Rossi.**
   - The busy box shows "A²: 250 of 432", then "D: 250 of 432" (the score count only appears from n = 500). Time it.
   - Press Esc during a second load from D1 with 1000+ values: "Stopped (Esc): no sample is loaded".
   - Q-Q: `W = 0.8499, p = 7.09 × 10^-20`. ECDF: `D = 0.1824` at x = 24.
   - Tests: `A*² … = 20.9771, p < 0.0001`, `Lilliefors D = 0.1824, p = 1.66 × 10^-39`, "all 3 tests with a p give evidence against normality".
   - Bins: `χ² = 246.28, df = 9`. Unmrg → Bars: no error.
8. **Draft lottery (new).**
   - Bars, title "Draft lottery 1970: 2 × 2": `χ² = 14.16, df = 1, p = 0.0002`, then `Fisher exact p = 0.0002` in red. Four cells: Jan-Jun lo 73 / hi 109, Jul-Dec lo 110 / hi 74. Check that the labels fit under the bars.
   - Table: E = 91.00, 91.00, 92.00, 92.00.
   - Test: `P(χ²(1) ≥ 14.164) : p = 0.000168`, `Two-sided p = 0.000243`, the "Why not a goodness-of-fit test …" paragraph with `χ² = 7.08, p = 0.0078`, and the monthly counts.
   - Curve: `df = (2-1)(2-1) = 1, Fisher exact p = 0.000243`. Merge says "A 2 × 2 table has nothing to merge."
9. **Exact test → Type** 7, 20, 0.5: `two-sided p = 0.2632`. The INPUT form shows the labels x:, n:, p₀:, and the p₀ help line with H₀ and p₀ glyphs.
10. **Use my data.**
    - D1 = 1, 2, 4: `W = 0.9643`, p = 0.6369. ECDF and Tests show `D = …, p not available for n < 5` in grey. Repeat in Degrees mode: same W and p.
    - D1 = 5, 5, 7: the Tests page has no green "p > 0.10".
    - D1 = 5, 7, 3, 12, 15, 1.5, 0.3, 99, 250, 8, 8, 8 → "Benford, 2 digits": the MSGBOX says "8 of the values are below 10", and the Test page repeats the count.
    - D1 = 12, 30, 8, 50 with D2 = 1, 2, 1, 4: the shares are rescaled (sum 8).
11. **Binomial fit → My counts → Type p₀:** the INPUT label is built from a variable (the verified form); check that it reads "p₀:".
12. **Glyphs:** χ² ² √ ≥ ≤ × → ± α λ μ σ x̄ p̂ ₀ ₁ ₂ ⇅ ⇆ all render. Footers read "page 1 of 3, ⇅ or tap = page".
13. **Touch:** check bars, rows, Q-Q points, ECDF columns and binomial bars; check that light taps on every soft key respond; check that Esc and Enter leave every screen.
14. **Quit:** Home should show `FitCheck: χ²(1) = 14.164, p = 0.0002; …` when the draft preset was the last fit. Check `FC_P`, `FC_PD` and `FC_BP`.
