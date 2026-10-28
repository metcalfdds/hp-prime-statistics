# RankLab beta 1a — notes (21 Oct 2026)

beta 1a applies every finding of the second review (`REVIEW2_RankLab_beta1.md`); `RankLab_beta1a_CHANGES.md` lists them one by one. Below is beta 1's note, updated.

`/home/claude/new6/RankLab_beta1a.txt`: 3,722 lines, pure ASCII, LF. Entry `EXPORT RankLab()` (no arguments, menu first). Tag `rk_` on every helper; the file-level LOCALs start with `rk`. Home exports: `RK_STAT, RK_P, RK_PN, RK_EFF, RK_HL, RK_RANKS`. **No CAS and no Python**: pure PPL. Not run on hardware or the emulator; only the PC harness (ppl_run_v3e).

## What it does, menu by menu

The welcome page (with the DISCLAIMER) comes first. Any key opens the main menu (list-form CHOOSE, 10 items; the Prime shows Quit as **A**):

| Item | Test | Data it uses (loaded automatically with a message if none yet) |
|---|---|---|
| Sign test (1 sample/paired) | exact Binomial(n, 1/2) on S+ | paired / one-sample set (Darwin) |
| Wilcoxon signed-rank | T+, exact null by DP (ties allowed), n ≤ 50 | paired / one-sample set (Darwin) |
| Mann-Whitney (rank-sum) | U₁, exact by counting (no ties, n₁n₂ ≤ 400) | groups set (Rossi); with more than 2 groups it asks for X and Y |
| Kruskal-Wallis + Dunn | H, epsilon², Dunn z with Holm | groups set (draft by month) |
| Friedman + Kendall's W | Q, W, mean Spearman between blocks (pair by pair), caution b < 10, refuses b < 2 | blocks set (judges: 43 × 3) |
| Rank correlation (rs, tau-b) | Spearman: exact over all n! orders for n ≤ 7, else t (caution below 10); Kendall tau-b: exact without ties for n ≤ 30, else z | x-y set (draft day vs number) |
| Load a preset | seven presets (below); opens the matching test | |
| Use my data (D1..D9) | Groups / Paired D1 - D2 / One sample D1 vs m₀ (INPUT) / Correlation D1, D2 / Friedman rows = blocks | Statistics 1Var columns, read in IFERR |
| Help | 7 pages; any key = next, Left = back, Esc = leave | |
| Quit | returns a one-line summary to Home | |

Each test opens a **view** of 3 pages (4 for Kruskal-Wallis), polled with GETKEY + MOUSE (ChiTable's loop):

1. **Result**: the source line, n, ties, the statistic, the exact p (or why none) beside the normal approximation (continuity-corrected, tie-corrected), the effect size(s), Hodges-Lehmann, H₀, the verdict at α = 0.05 ("evidence against H₀" / "no evidence against H₀ (not proof)"), the assumption.
2. **Picture**: sign / signed-rank / Mann-Whitney: the **rank strip** (one dot per observation, colour = group or sign of d, stacked, midrank above each value when the labels fit, an orange mark under the axis for tied values, the picked dot framed red, the panel says value, group, midrank and "tied with k others: ranks a to b averaged"). Kruskal-Wallis: **group boxes** on the value or rank scale (+), dots, medians, mean rank over each column (green bar on the rank scale, H₀ level dotted). Friedman: the **rank grid** (blocks × treatments, shaded by rank, R and mean rows; + shows the values). Correlation: the **rank scatter** (More → Data shows the raw data).
3. **Null**: exact bars (sign, signed-rank, MW) with the p tail(s) magenta and marked under the axis, the observed statistic red; or the normal / χ² / t / standard-normal curve with the p region shaded. A tap (or Left/Right) reads P(= v), P(≤ v) off the bars or P(≥ x) off the curve.
4. **Dunn** (KW only): mean ranks as bars from the H₀ level, the picked pair framed red; the pair list (z, raw p, Holm p, green when Holm p < 0.05); opens on the smallest p.

Soft keys page 1: Result, Plot, Null, slot 4 (Exact/Normal; KW and Friedman: Ranks/Values; correlation: rs/tau-b for the Null page), Tails (2-side / Lower / Upper; KW and Friedman say "upper only"), More. Page 2: Help, Dunn (KW) or Data/Ranks (correlation), Menu, More. Keys: Up/Down = page, Left/Right = pick (on Result: turn pages), + = slot 4, − = Tails, 0 = Help, Enter = a CHOOSE of every action, Esc = back to the main menu. Every touch action has a key. A new test starts two-sided and exact.

## Formulas and sources (header has the full list)

- Midranks by SORT + lower-bound search (O(n log n)); tie sums Σ(t³ − t). Lehmann (1975); Hollander, Wolfe & Chicken (2014).
- Sign: zeros dropped; S+ ~ Binomial(n, ½); lower `BINOMIAL_CDF(n,0.5,s)`, upper `BINOMIAL_CDF(n,0.5,n−s)` (a lower tail), two-sided min(1, 2 × smaller). Normal z = (S+ − n/2 ± ½)/(√n/2).
- Signed-rank: zeros dropped (n = nonzero d); T+ = Σ ranks of d > 0; exact null = coefficients of Π(1 + q^{a_i}) with a_i the doubled midranks (the ranks themselves when all whole), counted in place, divided by 2^n; mean n(n+1)/4, var n(n+1)(2n+1)/24 − Σ(t³−t)/48, cc 0.5 (= SciPy `wilcoxon(method='approx', correction=True, zero_method='wilcox')`). r = (T+ − T−)/(n(n+1)/2) (Kerby 2014). HL = median of Walsh averages of the nonzero d (R's estimate), n ≤ 100.
- Mann-Whitney: U₁ = R₁ − n₁(n₁+1)/2; exact null = Gaussian binomial Π(1 − q^{n+i})/(1 − q^i) in whole numbers (≤ 2.8E11, exact in 12 digits for n₁n₂ ≤ 400); var n₁n₂/12((N+1) − Σ(t³−t)/(N(N−1))), cc 0.5 (= SciPy `mannwhitneyu(method='asymptotic', use_continuity=True)`). Rank-biserial (U₁ − U₂)/(n₁n₂); U₁/(n₁n₂) = P(X>Y) + ½P(X=Y). HL shift = median of x_i − y_j, n₁n₂ ≤ 5,000.
- Kruskal-Wallis: H/(1 − Σ(t³−t)/(N³−N)), p from χ²(k−1); ε² = H/(N−1) (Tomczak & Tomczak 2014). Dunn (1964) z with the tie-corrected variance; Holm (1979).
- Friedman (1937) with C = 1 − ΣΣ(t³−t)/(bk(k²−1)); W = Q/(b(k−1)); mean Spearman between blocks = the mean of Pearson's r of the within-block midranks over all pairs of blocks (beta 1a; (bW−1)/(b−1) only without ties).
- Exact Spearman (beta 1a): all n! orders of y, Heap's algorithm, T = Σ(2r_x)(2r_y) updated per swap, n ≤ 7; two-sided = min(1, 2 × smaller tail) (as `permutation_test`). Exact Kendall: inversion counts Π(1 − q^i)/(1 − q), n ≤ 30, no ties (as `kendalltau(method='exact')`).
- Spearman = Pearson on midranks; t on n−2 df (= SciPy `spearmanr`). Kendall tau-b by Knight's (1966) sort-and-merge (n log n); var as SciPy `kendalltau(method='asymptotic')`.
- χ² upper tails for whole df as sums of positive terms (A&S 26.4.4-5), never 1 − CDF; every other upper tail is a lower tail (`NORMALD_CDF(0,1,−z)`, `STUDENT_CDF(df,−t)`).

## Presets (data/DATASETS.md; the source line is on every page)

| Preset | Opens | Source line shown |
|---|---|---|
| Rossi: prior convictions (114 arrested vs 318 not) | Mann-Whitney | Rossi, Berk & Lenihan 1980 (via Allison 1995) |
| Draft 1970: number by month (12 groups, 366) | Kruskal-Wallis | Fienberg 1971 Science 171:255; Starr 1997 JSE |
| Draft 1970: day vs number | Rank correlation | Fienberg 1971 Science 171:255; Starr 1997 JSE |
| Darwin: Zea mays pairs (15, inches) | Signed-rank (Sign test from the menu) | Darwin 1876; Fisher 1935 Design of Experiments |
| US judges: 3 criteria — the 43 judges (blocks) × integrity, oral rulings, written rulings (treatments); each value = lawyers' mean rating | Friedman (a test) | New Haven Register 14 Jan 1977 (R datasets) |
| US judges: halo (W only) — 11 criteria (blocks) × the first 8 judges; W described, **no p** (criteria are not independent raters: same lawyers, halo effect); CONT left out | Friedman page, descriptive | New Haven Register 14 Jan 1977 (R datasets) |
| Mock jury: Years by attractiveness (39/38/37) | Kruskal-Wallis | Plaster 1989 M.A. thesis (R heplots, Friendly) |

Every preset value was compared with its CSV/JSON in the verify script (Rossi = rossi.csv; draft = draft1970_triola.json = vcdExtra_Draft1970.csv; judges = datasets_USJudgeRatings.csv; jury = heplots_MockJury.csv; Darwin from HistData_ZeaMays.csv, d × 8 = Fisher's 49, −67, …).

## What was checked

`verify_RankLab_beta1a.py` → `verify_RankLab_beta1a_output.txt`: **6064 checks, 0 failures**. It is beta 1's script with the expected values that beta 1a changes on purpose updated, plus:

- **Correlation:** Spearman's exact p (n ≤ 7) against brute-force enumeration of all n! orders and `scipy.stats.permutation_test` (exact, pairings). Kendall's exact p against `kendalltau(method='exact')` and enumeration (n ≤ 7).
  - The review's examples: (1,2,3; 2,4,9) gives 0.3333; (1..5; 1,2,3,5,4) gives 0.0833 for both, and the verdict no longer flips.
  - Also checked: 40 small random sets with ties, 12 tie-free sets up to n = 30, perfect orders, the exact nulls' bars (= the enumerated distributions), and the n < 10 caution.
- **Summary:** the Quit summary after 7 refusal kinds × 2 previous tests, after a cancelled group pick, after a tail change, and before any test.
- **Judges:** 43 × 3 = `friedmanchisquare`. The halo preset shows no p, says why, and sets `RK_P = -1`.
- **Esc:** every progress bar that says "Esc = stop" reads Esc (static check). Esc was run in the 366-value ranking, the Kendall merge, the Friedman blocks, the MW exact count, the Spearman orders, the Kendall count and the Walsh averages.
- **Cautions:** KW n < 5, Friedman b < 10, one block refused.
- **Glyphs:** every `CHAR()` is in the verified set.
- **Mean Spearman between blocks** with ties = the mean of pairwise `spearmanr`; "none" with a flat block.
- **Wording and colour:** "1 group", m₀/H₀ in the INPUT form, the HL wording, no magenta group colour.
- **The 12-item CHOOSE:** Mann-Whitney on Mar vs Dec.
- **Every screen of every run:** each font-1 line within its own TEXTOUT_P width at 6.5 px a character, no scientific-notation number, no MSGBOX over 5 lines.

Gate (`ppl_gate_v1c.py RankLab_beta1a.txt RankLab_beta1.txt`): **PASS**. Kit lint 0 errors; ppl_check clean (no hard errors); lint_ppl 5 known-noise lines; the full parse stops at the EXPORT list (line 214, the known tool limit, as beta 1 and ChiTable); fleet_names 0 collisions, 0 untagged, 0 built-in matches.

## The TI programs reworked, and their bugs not repeated

SRTEST, RSTEST, KWTEST, SRCORR and ZZRANK (Michael Lloyd, Triola's TI-83/84 CD) are the core; SRPVALUE/SRCV (the exact signed-rank recursion), SIGNTEST, WSIGNTST, FRIEDMAN, KENDALLT, CONCORW (mean Spearman from W), DIFFKWCV (pairwise KW, here Dunn + Holm) and COCHRANQ were read for ideas. Not repeated: RSTEST's S overwritten by the SD and its tie loop bounded by N; normal approximations without tie or continuity corrections and with no exact p; KWTEST's 0-as-missing; SRCORR's 1 − 6Σd²/(n(n²−1)) with ties; SIGNTEST's z passed into binomcdf; WSIGNTST's zeros counted in n; SRPVALUE's P(T > t) right tail; SRCV's nearest-α critical value (here p is computed, never looked up); the TI-82 implied-multiplication reliance.

## Left out, and why

- No CAS and no MicroPython.
- No exact null for Mann-Whitney with ties, nor for Kruskal-Wallis or Friedman (χ², now with cautions). Exact Spearman stops at n = 7: 8! orders would take roughly 90 s on a G1. Exact Kendall needs no ties and n ≤ 30.
- Hodges-Lehmann only for n ≤ 100 (one sample) or n₁n₂ ≤ 5,000 (two samples).
- Cochran's Q is not included.

## DEVICE CHECKLIST (G1 first; expected numbers from SciPy)

1. Paste into the Kit, save; Program Catalog → RankLab → Edit → **Check** (compile). Run `RankLab` from Home (no parentheses). Welcome page: the red DISCLAIMER box; glyphs render.
2. Main menu: 10 items, the last labelled **A** (Quit). Esc cancels → Home shows "RankLab: no test run".
3. **Wilcoxon signed-rank** → MSGBOX "Darwin's Zea mays loaded" → Result: `T+ = 96, T- = 24 (mean 60, SD 17.61)`, `Exact p = 0.0413 (two-sided)`, `Normal: z = +2.016, p = 0.0438`, `Rank-biserial r = +0.600`, `Hodges-Lehmann estimate = 3.125`. Time the opening (the exact count is n = 15: should be instant).
4. Down → rank strip: 13 blue, 2 magenta dots, midranks 1…15 above. Tap the right-most dot → "d = 9.375: |d| = 9.375, midrank 15, in T+". Left/Right move the red frame.
5. Down → Null: blue bars, magenta tails at both ends, red line at T+ = 96. Tap a bar: "T+ = v: P(=) …, P(≤) …"; Left/Right step it. Press − twice → "Upper", exact p = 0.0206; once more → 2-side. + → Normal: the curve, shaded, p = 0.0438.
6. Esc → **Sign test**: `S+ = 13 positive, 2 negative`, `Exact p = 0.0074`, `Normal: z = +2.582, p = 0.0098`, `Median of d = 3`.
7. **Mann-Whitney** (Rossi loads; **time it**, 432 values): `R₁ = 28174.5, U₁ = 21619.5, U₂ = 14632.5`, `Mean of U = 18126, SD = 1123.74 (tie-corrected)`, `Exact p: none with ties`, `z = +3.108, p = 0.0019`, `r = +0.193`, `P(X > Y) + half the ties = 0.596`, HL refused. Strip: tap a dot at 0 → "tied with 37 others: ranks 1 to 38 averaged".
8. **Kruskal-Wallis** (draft by month; **time it**): `H = 25.953`, `χ² approximation: p = 0.0066`, `epsilon² = 0.071`, `Dunn (Holm): 1 of 66`. Boxes: tap the last column → "Dec: n = 31, mean rank 121.55 (H₀ 183.5)"; + → rank scale with green mean bars. Up → Dunn page opens on **Mar v Dec, z = +3.88, Holm p = 0.0069** (green); tap rows.
9. **Friedman** (judges, 43 × 3): `Q = 69.547 (C = 0.9244)`, df 2, `p < 0.0001`, `Kendall's W = 0.809`, `Mean Spearman rs between blocks = 0.808`, mean ranks Integrity 2.9, Oral rulings 1.2, Written rulings 1.8. Grid: title "ranks within, blocks 1-9/43"; Right past the last cell of row 9 scrolls.
   Then Load a preset → **US judges: halo (W only)**: `W = 0.939`, the red "No p-value here, on purpose" lines, the Null page says why, `RK_P` = −1, Quit says "Kendall's W = 0.939 (descriptive, no p)".
10. **Rank correlation** (draft day vs number; **time it**; Esc on the Kendall merge bar must return to the menu with "Stopped by Esc"): `rs = -0.2257`, `t = -4.420 (364 df), p < 0.0001`, `tau-b = -0.1489`, `z = -4.251`. Scatter of ranks; More → Data shows the raw scatter. + → Null shows the standard normal for Kendall.
   **Small n:** D1 = 1..5, D2 = 1,2,3,5,4 → `Spearman rs = +0.9000`, `exact p = 0.0833 (two-sided, all n! orders)`, `tau-b = +0.8000`, `exact p = 0.0833`, verdict "no evidence". The Null page shows exact bars on the rs scale. D1 = 1..7, D2 = 2,1,4,3,7,5,6 → Spearman exact p = 0.0341, tau-b exact p = 0.0690: **time the 5,040 orders** (bar "Exact Spearman: … orders"). n = 8 (D2 = 2,1,4,3,5,7,6,8): the red "Caution: n < 10" lines, Kendall exact p = 0.0055.
11. Load a preset → Mock jury (KW): `H = 2.876 (divided by C = 0.9811)`, `p = 0.2374`. Esc → Mann-Whitney → choose Beautiful, then Unattractive: `U₁ = 592.5`, `z = -1.347, p = 0.1779`, `HL estimate of the shift X - Y = -1`.
11a. **The 12-item group CHOOSE** (review): Load a preset → Draft 1970: number by month, Esc, Mann-Whitney → pick **Mar** then **Dec** (items 3 and C): `X = Mar`, `U₁ = 753`, `normal p = 0.0001`. If the CHOOSE misbehaves (wrong names, an error), this is the `{cgN(1), …}` list form with no fleet precedent.
11b. **Summary after a refusal** (review): run Wilcoxon, Esc, Use my data → Groups with D1 = 2,2 and D2 = 2,2,2 (refused), then Quit: Home must still say "RankLab: Wilcoxon signed-rank, n = 15, T+ = 96, …".
11c. **Cautions:** Groups D1 = 1; D2 = 3; D3 = 2,4 → red "Caution: a group has n < 5"; Friedman with one row → refused.
12. Use my data: D1 = 10,12,9,15,11,13,8 and D2 = 9,12,10,11,10,9,9 → Paired: `n = 6 nonzero d (zeros dropped = 1)`, `T+ = 16`, exact p = 0.3438 (ties among |d|). One sample with m₀ = 10 (INPUT form shows 0 first). Correlation D1, D2. Groups (D1, D2) → Mann-Whitney, no ties → exact bars.
13. **Speed at the limit**: put 50 distinct values in D1, One sample, m₀ = their median → the progress bar "Exact null of T+: rank k of 50"; note the time. Repeat with heavy ties (values 1–12): about twice the steps (≈62,000). Press Esc during a long count → Result says "Exact p: stopped by Esc (normal used)".
14. Home after a run: `RK_STAT`, `RK_P` (Darwin signed-rank: 0.041259765625), `RK_PN`, `RK_EFF`, `RK_HL`, `RK_RANKS` (the 15 midranks). Quit's summary: "RankLab: Wilcoxon signed-rank, n = 15, T+ = 96, exact p = 0.0413 (two-sided)".
15. Glyphs to look at (no superscript 3 any more: "sum(t^3 - t)"); the INPUT form for One sample shows m₀ and H₀; ⇆ ⇅ (footers), ₀ ₁ ₂ (H₀, U₁, n₂), χ², ≤ ≥, ×, ±, √ (help page 5), α. Text near the right edge: the result pages' longest lines (font 1, 46 characters), the Friedman grid title, the KW panel lines.

Loop sizes for the G1 (interpreted steps, from the twin): exact signed-rank n = 30 ≈ 7,000; n = 50 ≈ 30,000 (no ties), ≈ 62,000 (ties); MW exact 20 × 20 ≈ 7,600; Kendall for 366 pairs ≈ 3,300 merge steps; ranking 432 values ≈ 4,000 search steps; the box page draws 366 dots per frame.
