# EpiStats v1.6: changes from v1.5

*16 October 2026. v1.6 is built on v1.5 and keeps every v1.5 and v1.4 fix and feature. It folds in ConTable2 v1.3 and FEP v1.4, gives module 5 the touch grid, the Mantel-Haenszel CIs and tests, and a forest plot, and adds two module 2 pages. **It has not been run on hardware yet** (nor have v1.5 and v1.4).*

File: `EpiStats_v1.6.txt`: 4627 lines, 205,780 bytes, UTF-8, LF. Base: `EpiStats_v1.5.txt` (3518 lines). The file has 99 routines (v1.5 had 75). In this document, "before" line numbers are **v1.5's** and "after" line numbers are **v1.6's**.

**Staging:** move `ConTable2_v1.3.txt` and `FEP_v1.4.txt` (with their `_CHANGES.md`) to `_superseded`. `EpiStats2x2(a, b, c, d)` replaces both one-line Home calls. Also delete the `ConTable2` and `FEP` programs from the calculator.

---

## (a) Every change

| # | Item | Before (v1.5) | After (v1.6) | What changed |
| --- | --- | --- | --- | --- |
| 1 | Header | 3, 14-17, 126 | 3, 14-66, 175 | v1.6 banner. A "What changed in v1.6" paragraph lists everything that moved from ConTable2 v1.3 and FEP v1.4. Licence, AI-assistance and firmware lines kept; marked "not yet run on hardware". |
| 2 | **New results** | — | 247-254 | `EP_ORMH_CI`, `EP_RRMH_CI`, `EP_IRRMH_CI`, `EP_MH_CHI`, `EP_MH_P`, `EP_BD_P`, `EP_MCN_P`. All 39 v1.5 `EP_*` are kept with their meanings. `EP_IRRMH_CI` was not on the brief's list; I added it because the IRR_MH CI now exists. `EP_MH_CHI`/`EP_MH_P` hold the **uncorrected** statistic (statsmodels' default) from the most recent case-control or cohort run. `-1` means undefined. |
| 3 | File-level state | 205-238 | 298-311, init 341-347 | Three new `LOCAL` lines (≤ 6 names, all `es`-tagged): `esStr`, `esMS` (24-number stratum memory), `esSC`, `esDrp`, `esFMsg`, `esRd`, `esDir`, and the Fisher-bar cache `esQP … esQCut`. `es_Init` sets every one of them. |
| 4 | **`EXPORT EpiStats2x2(eA, eB, eC, eD)`** | — | 401-424 | The one-line Home call. It loads the counts into module 1, skips the grid, opens the results at page 1, and on Esc returns the two-sided Fisher p (as ConTable2/FEP did). It returns `-1` above N = 2000, or with a message for negative, fractional or all-zero counts. ppl_check_v3 E11/E4 report no clash for the parameter names. This is the only new catalog entry. |
| 5 | Helpers | — | 546-614 | `es_FisherPt` (point probability, log space), `es_McNemar`, `es_KapTxt`, `es_Nice` (1-2-5 steps), `es_PTxt` ("p < 0.0001" instead of "p = < 0.0001"), `es_EqTxt`, `es_RateTx` (849). |
| 6 | **Module 1 page 1: THE THREE READINGS** | — | 1513-1650 | Three tabs (Cohort / Diagnostic / Paired) across the top, as hit boxes. A tap on a tab, or Up/Down, switches the reading. The four counts are relabelled (Exposed/Outcome; Test/Disease with TP FP FN TN; A/B with agree/differ), and the page shows only that reading's statistics. **Cohort:** both risks, RR, OR and RD with CIs, AF exposed and AF population. **Diagnostic:** sens and spec (with Wilson CIs), PPV, NPV, LR+, LR−, Youden, accuracy and **error rate**, prevalence. **Paired:** po, pe, kappa (Landis-Koch words), **McNemar** with continuity correction and p, "only the pairs that differ: b, c", **Yule's Q and Y**, disagreement rate. The default is Cohort, each time module 1 opens. |
| 7 | Module 1 page 3: tests | 1450-1497 | 2083-2135 | **Fisher's point probability** now sits on its own line under the two-sided p. Spacing is 2 px tighter below it, so the N line still ends at y 214. |
| 8 | **Module 1 page 4: the Fisher bars** | — | 1660-1814 | `es_HyperFill` computes P(a′ \| margins) for every a′ from amin to amax in log space with `es_lngamma`, using the same rule as `es_FisherExact`, so the magenta bars sum to page 3's p exactly. It is computed once per table (N ≤ 2000 cap; above that the page says so). It trims tails below 1E-7 of the tallest bar but always keeps your bar, and says how many it trimmed. `es_HyperPage` draws your bar red, bars no more likely than yours magenta, and the rest pale grey, with a colour strip under the axis so even bars too short to see show whether they count. A tap on the plot, or Up/Down, picks a bar; an orange corner panel (in the corner away from the peak) shows that 2×2, its P, and "counted in p" or "not counted". **Above 60 bars**, the note reads "N bars: too narrow to label; a tap picks one". Bars become 1 px or thinner (269 bars at N = 1980) and are not grouped. |
| 9 | Module 1 page order | loop 1346-1398 | 1816-2032 | Six pages: 1 readings, 2 table (v1.5 p1), 3 tests, 4 Fisher bars, 5 association with tap-for-arithmetic (v1.5 p3), 6 mosaic (v1.5 p4). Page indicators are now n/6. `esDir` skips the grid for EpiStats2x2. `EP_MCN_P` is set here. |
| 10 | **Module 2 page 4: risk bars** | — | 2469-2565 | Two bars (Exposed+, Exposed−) with 95 % Wilson CIs (`es_WilsonCI`) drawn as whiskers. The RD is a magenta bracket joining the two bar tops, with dotted guides, labelled "RD = …". The y axis uses 1-2-5 ticks. Below the plot, "OR = 2.67 overstates RR = 2.00 by 33 % here / because the outcome is common (Ru = 20.0 %)." is worked out from the data (OR/RR = (1−Ru)/(1−Re)). The page also has a rare-outcome wording ("by only 3 %: the outcome is rare here"), an RR < 1 wording ("exaggerates"), a version for RR = 1, and one for a zero risk. It names Re instead of Ru when only Re is common. |
| 11 | **Module 2 page 5: NNT icon array** | — | 2570-2620 | A 10 × 10 grid of 12-px cells. CEILING(NNT) cells are blue (the exposed/treated group). One cell is **red** for the one extra case (RD > 0) or **green** for the one prevented case (RD < 0). The rest are grey. NNT > 100 and RD = 0 are explained on screen. Module 2's loop goes to 5 pages; headers are n/5. |
| 12 | **Module 5 entry: the touch grid** | 2652-2702, 2821-2846, 2965-2990 (eight INPUTs) | `es_StratGrids` 3458-3486; grid modes 5-7 in `es_CellName` 895, `es_AskAll` 917-1039, `es_GridDraw` 1041-1128, `es_Grid` 1130-1236 | Two grid entries, stratum 1 then 2, in the **module-1 cell layout** (b = Exposed+/Outcome−, c = Exposed−/Outcome+) for all three designs. The rates grid holds cases and person-time: its Total column shows each row's rate, and person-time keeps its decimals. **Values** opens the v1.4 four-field form for that stratum, with labels a₁…/Cases(exp)₁…. The cohort form still asks for cases and *totals*, converts them to cells, and refuses a total smaller than its cases. Each design remembers its two strata (`esMS`). |
| 13 | **Module 5 engine** | 2704-2725, 2857-2880, 3000-3023 | `es_StratEst` 3490, `es_BDFit` 3533, `es_MHCalc` 3581-3685 | One routine for OR, RR and IRR, with an optional drop mask. **RBG** variance of ln OR_MH; **Greenland-Robins** variances of ln RR_MH and ln IRR_MH; CI = exp(ln ± 1.959964 SE); the **M-H chi-square**, uncorrected and corrected, 1 df, for OR and RR; **Breslow-Day** (per-stratum quadratic in its cancellation-free form, a linear root when OR_MH = 1, k−1 df, strata with an empty margin skipped). The point estimates are the v1.5 formulas, unchanged. |
| 14 | **Module 5 pages** | 2727-2806, 2882-2950, 3025-3060 | `es_StratTables` 3711, `es_MHSummary` 3817, `es_RuleTxt` 3765, `es_Strat_Run` 4065 | Three pages for each design. **1:** the two strata, with each stratum's own estimate and 95 % CI (Woolf / Katz / Poisson; "+0.5" marked). **2:** crude vs M-H with CIs, the CI method named, the tests, and "Reading it". **3:** the forest plot. The v1.5 red "Confounding likely present" verdicts (2797-2800, 2916-2919, 3048-3049) are gone. In their place, in black, is "Crude and M-H differ by 23 % (of the M-H). / By the usual 10 % rule of thumb: adjust. / Strata ORs homogeneous (Breslow-Day p = 0.67): / one adjusted OR is a fair summary." When BD p < 0.05, orange text says to report the strata separately. RR and IRR have no homogeneity test, so the page states the v1.4 "differ by more than half" heuristic as a heuristic. The rates design was one page and is now three. |
| 15 | **Forest plot** | — | `es_ForestDraw` 3895-4063, `es_Toggle` 3870, `es_FX` 3862 | Rows: Stratum 1, Stratum 2, Crude, M-H, on a log10 axis with 1-2-5 ticks (TrendTest's trDrawOR scheme). Labels are thinned to 24 px apart, and the axis covers at least 0.6 decades and is capped at 10^±3. **Squares** have area ∝ the M-H weight (b c/n; c n₁/n; c T₁/T), with the weight % printed. Each stratum has its own CI bar with caps. Crude is a black square with its CI. **M-H is a magenta diamond** (four LINE_P plus a centre line) with its tips on the RBG/GR CI. The **dotted line at 1** is a `PIXON_P … STEP 3` loop. **Tap a stratum row (or Up = 1, Down = 2) to drop it.** The row turns grey with a hollow square, "dropped" appears, and M-H and crude are recomputed from what is left. With one stratum left the page reads "M-H OR = 4.000 (2.00-8.00), stratum 2 only / One stratum left: M-H = that stratum's OR." A tap on the last remaining stratum is refused ("At least one stratum must stay in the pool."). Tap again to restore. The `EP_*` results always keep the full two-stratum analysis. |
| 16 | Help | 3309-3518 | 4370-4627 | The menu has 14 items, the most the simple CHOOSE form takes; items 10-14 show as A-E. Two new pages: **C "Readings & Fisher Bars"** and **D "Forest, Risk Bars, NNT"**. Updated: About (v1.6, EpiStats2x2, "Touch: Help 9 to D"), Mantel-Haenszel (RBG/GR, M-H χ², Breslow-Day, the 10 % rule as a rule of thumb, the forest-plot tap), Variables (the seven new names), Grid ("Modules 1-3 and 5"), Result pages (pages 5 and 6). |
| 17 | Footers | — | new pages | House form, dodger blue: `tap a tab = reading, ←/→ = page, Esc = menu`; `tap a bar = its table, …`; `tap row = drop/restore, …`; the module 2 pages use the standard paged footer. |

**Not added: the "More" soft key.** No v1.6 screen needs more than six soft-key actions. The grid keeps its five (Edit, Values, Clear, —, Cancel, Run), and every new tap action already has a keyboard route (Up/Down on the tabs, the bars and the forest rows; arrows for pages). So by the convention's own rule ("a screen whose actions fit in six gets no More") there is no "More" key, and the help pages do not mention it.

**What was not copied from ConTable2/FEP:** their Pearson, Yates and COMB-based Fisher code, which module 1 already had, now in log space with no COMB overflow, so the old N ≤ 1500 cap is gone. Also their MSGBOX output, and ConTable2's degenerate-table refusal (module 1 handles zero margins).

---

## Gate output (final run)

```
=================== EpiStats_v1.6.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
     66 E4      36 E9
--- 2. ppl_check_v2 tally (ORIG) ---          (ORIG = EpiStats_v1.5.txt)
     69 E4      44 E9
--- 2b. ppl_check_v2 HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
3775 checks, 18 problems   (v1.5: 16. The same 12 'a'/denom/center lines and file-name
  noise, plus 2 lines about the deliberate EXPORT EpiStats2x2: "neither the entry point
  nor an EP_* result" / "helper is EXPORTed - it will show in the catalog". Nothing else new.)
--- 4. full parse (kit interpreter) ---
EpiStats_v1.6.txt   PARSE FAIL PPLError: <ppl>:263: expected a name after EXPORT
   ORIG: EpiStats_v1.5.txt   PARSE FAIL PPLError: <ppl>:205: expected a name after EXPORT
--- 5. line count, size, non-ASCII in code (E5 list) ---
4627 lines, 205780 bytes     (no E5 lines, no W3 lines)
```
Line 263 is the first file-level `LOCAL`, which is the kit parser's known limit (same as v1.5 and ChiTable). A copy with the file-level `LOCAL` lines turned into plain globals parses: **PARSE OK (99 functions)**. `fleet_names_v2.py` over the newest version of every program in `out/` (23 files; ConTable2 and FEP left out as superseded): **0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches.**

---

## Verification: `verify_EpiStats.py` (output in `verify_EpiStats_output.txt`)

The v1.5 script is preserved unchanged as `verify_EpiStats_v1.5.py`; its Part B mini-harness was built around v1.5's page numbers. The new script has two parts:

- **Part C**: the v1.6 formulas, written out the way the PPL computes them, against statsmodels and SciPy. This was done before the PPL was written. **120 checks.**
- **Part D**: the PPL run in the shared harness `harness/ppl_run_v1.py`, covering modules 1, 2 and 5 plus EpiStats2x2. Each run is scripted the way a student would use it: grid taps, soft keys, tabs, bar taps, forest taps, Up/Down. **83 checks, 28 scripted runs.**

**Result: ALL CHECKS PASSED (203). There were no runtime errors, no stalls, no leftover script, and no page skipped in stale-key mode. Nothing draws on G0 except `BLIT_P(G0, …)`. The layout audit found 0 warnings over 262 pages** (that audit uses estimated glyph widths; see (c)).

### Part C: what statsmodels reports and what v1.6 matches

| Statistic | Reference | Result |
| --- | --- | --- |
| OR_MH, RBG SE of ln OR_MH, 95 % CI | `StratifiedTable.oddsratio_pooled`, `logodds_pooled_se`, `oddsratio_pooled_confint` | equal (1e-12 / 1e-6), 5 strata sets incl. 3 strata and a zero cell. One stratum: RBG var = Woolf var. |
| M-H χ², uncorrected | `test_null_odds(correction=False)`, **statsmodels' default** | equal (1e-10). This is what `EP_MH_CHI`/`EP_MH_P` hold. |
| M-H χ², continuity corrected | `test_null_odds(correction=True)` | equal whenever \|Σ(a − E a)\| ≥ 0.5. Below 0.5, statsmodels subtracts 0.5 anyway and squares a negative number (for example 0.0255 instead of 0.0211). v1.6 follows R's `mantelhaen.test` and does not correct below 0.5; the page then shows the same value twice. |
| Breslow-Day | `test_equal_odds(adjust=False)`, **statsmodels' default (no Tarone)** | equal (1e-8). Tarone's version is also checked in Python (`adjust=True`, equal) but not shown on the calculator, because statsmodels does not apply it by default. When OR_MH = 1 exactly, statsmodels divides by 1 − OR_MH = 0 and returns nan; v1.6 takes the linear root and matches the hand formula (p = 4E-6 for opposite ORs). |
| RR_MH | `riskratio_pooled` | equal (1e-12) |
| Var ln RR_MH (Greenland-Robins 1985) | no statsmodels routine | One stratum: equals Katz 1/a − 1/n₁ + 1/c − 1/n₀ exactly, and its CI equals `Table2x2.riskratio_confint`. |
| IRR_MH and its variance (Greenland & Robins 1985, *Biometrics* 41:55-68) | no statsmodels routine; **cited source** | One stratum: equals 1/a + 1/c exactly. Simulated coverage of the 95 % CI is 0.956 over 4000 runs (true IRR 2). So IRR_MH **has** a CI in v1.6. |
| McNemar (continuity corrected) | `mcnemar(exact=False, correction=True)` | equal when b ≠ c. When b = c, statsmodels gives (−1)²/(b+c); v1.6 gives 0, p = 1 (R's `mcnemar.test` rule). |
| Yule Q, Y; error rate | identities (OR−1)/(OR+1), (√OR−1)/(√OR+1); 1 − accuracy | equal |
| Point probability; Fisher bars | `scipy.stats.hypergeom.pmf`, `fisher_exact` | Every bar equals the pmf (to 1e-9); the magenta sum equals `fisher_exact`'s p; 6 tables. |
| Wilson CIs; OR/RR | `proportion_confint(method='wilson')`; OR/RR = (1−Ru)/(1−Re) | equal |

### Part D: the device-test tables, as the harness ran them

- **Module 1, 12 5 8 30 (typed by taps).**
  - Cohort tab: RR 3.353 (1.69-6.67), OR 9.000 (2.45-33.11), RD 49.5 %, AF exposed 70.2 %, AF population 42.1 %.
  - Diagnostic tab: sens 60.0 % (38.7-78.1 %), spec 85.7 %, LR+ 4.20, error rate 23.6 %.
  - Paired tab: kappa 0.472 (statsmodels `cohens_kappa` 0.4723), McNemar χ² 0.308, p = 0.5791, Yule Q 0.800, Y 0.500, `EP_MCN_P` = 0.5791.
  - Page 3: Fisher 0.000729, point probability 0.000599.
  - Page 4: 16 bars (1 red, 4 magenta, 11 grey; 2 trimmed); the legend says "they sum to p = 0.000729". A tap at x 150 picks a′ = 6, and the panel shows "6 11 | 17 / 14 24 | 38, P = 0.236954, not counted". Down then picks a′ = 7.
  - v1.5 features intact: OR box "OR = (a×d)/(b×c) = (12×30)/(5×8) = 9.00", mosaic tile a adjusted residual +3.53, pages 1/6 to 6/6.
- **EpiStats2x2.**
  - (12, 5, 8, 30) returns 0.000729 and opens at 1/6 with no grid.
  - (3.5, 1, 2, 4) shows a message and returns −1.
  - N = 2070 returns −1, and page 4 says it is not computed.
  - N = 1980 returns 5.3E-78 = scipy; 269 bars with the "too narrow" note.
  - (3,1,1,3), (1,9,11,3), (0,0,5,20) and (10,4,4,10) each return scipy's p.
- **Module 2.**
  - 40 60 20 80: "OR = 2.67 overstates RR = 2.00 by 33 % here / because the outcome is common (Ru = 20.0 %)."; icon array: 4 blue + 1 red of 100.
  - 5 95 2 98: "by only 3 %: the outcome is rare here (Ru = 2.0 %)"; 33 blue + 1 red.
  - 10 90 20 80: "OR = 0.44 exaggerates RR = 0.50 by 11 % here"; 9 blue + 1 green.
  - 1 299 0 300 and 10 10 10 10 both end cleanly with their explanations.
- **Module 5, case-control, strata 15 5 30 30 and 40 30 20 60.**
  - Page 1: OR₁ = 3.000 (0.97-9.30), OR₂ = 4.000 (2.00-8.00).
  - Page 2: Crude OR = 2.829 (1.64-4.89); M-H OR = 3.681 (2.04-6.66); M-H χ² 19.443, p < 0.0001, corrected 18.228; Breslow-Day 0.181, p = 0.670; "Crude and M-H differ by 23 % … adjust … Strata ORs homogeneous (Breslow-Day p = 0.67): one adjusted OR is a fair summary."
  - Forest plot: dropping stratum 1 gives 4.000 (2.00-8.00), "stratum 2 only"; a second drop is refused; restore works; Down drops stratum 2, giving 3.000.
  - `EP_ORMH_CI` = {2.035829, 6.655110}, `EP_BD_P` = 0.670438.
- **Cohort, 12 88 4 96 and 25 75 10 90:** RR_MH 2.643 (1.48-4.71) = Python GR; M-H χ² 12.074. The same strata typed through the **Values** form (cases and totals) give the same RR_MH.
- **Rates, 15/1200 8/1500 and 30/900 20/1100:** IRR_MH 1.978 (1.23-3.17). Person-time 1200.5 entered through Values is kept as typed.
- **Edge runs (all clean):** a zero cell (Haldane "+0.5" in the stratum), an empty row (no BD, said so), \|Δ\| < 0.5, opposite ORs (BD p < 0.001, orange advice), a cohort stratum and a rate stratum with no exposed cases ("RR = 0.000 (no CI)"), a total smaller than its cases (refused), and Cancel.

---

## (b) DEVICE TEST CHECKLIST, least to most risky

Paste `EpiStats_v1.6.txt` into the Connectivity Kit and sync. Delete `ConTable2` and `FEP` from the calculator. Steps 1-2 check the paste; 3-8 the parts built only from verified idioms; 9-15 the new drawing and taps; 16-19 the riskier constructs. Have the G1 ready for 17.

1. **Paste and compile.** If it stops, note the line. Likely spots, most likely first:
   - the new file-level `LOCAL` lines 298-300;
   - `EXPORT EpiStats2x2(eA, eB, eC, eD)` at 401 (the first EXPORT with parameters in this file);
   - the 14-item `CHOOSE` at 4378 (at the simple-form cap).
2. **Catalog.** It shows **EpiStats** and **EpiStats2x2** (no `es_` helpers). Run EpiStats: the menu says "EpiStats v1.6"; Esc returns the summary string.
3. **Help, item 6 (Mantel-Haenszel), then C and D.** Twelve lines each, nothing cut at the right edge. Item 1 says "Touch: Help 9 to D". The menu letters run A…E, with E = Back.
4. **Module 1 grid, 12 5 8 30 → Run → page "THREE READINGS 1/6".**
   - Cohort is filled blue.
   - Check RR = 3.353 (1.69-6.67), OR = 9.000 (2.45-33.11), RD 49.5 %, AF exposed 70.2 %, AF population 42.1 %.
   - The last two lines are grey and none touches the footer.
5. **Tap "Diagnostic".** The table relabels as Test+/Test− by Disease+/Disease− with "a = 12 TP … d = 30 TN". Check sensitivity 60.0 % (38.7-78.1 %), specificity 85.7 % (70.6-93.7 %), LR+ 4.20, LR− 0.467, Youden 0.457, "Accuracy = 76.4%, error rate (b+c)/N = 23.6%".
6. **Tap "Paired".** The cells read "agree"/"differ". Check kappa 0.472 (Moderate) and **"McNemar χ² (cont. corr.) = 0.308, p = 0.5791"**. Up/Down cycle the tabs. A tap below the tabs on the right half turns to page 2.
7. **Page 3/6.** "Point prob. (this table): 0.000599 (page 4)" sits under "Two-sided exact p: 0.000729 *". The N = 55 line is above the footer.
8. **Pages 5/6 and 6/6 (v1.5 features).** The OR row's worked box still opens on tap; the mosaic tile a reads adj. residual +3.53. A right tap on 6/6 stays put.
9. **Module 1 page 4/6, the Fisher bars.**
   - 16 bars; a = 12 is red at the right; a = 13-15 and 0-1 are magenta; the middle bars are grey; a coloured strip runs under the axis.
   - The legend reads "they sum to p = 0.000729", the same as page 3.
   - The orange panel (top right) shows your table.
   - **Tap the tallest bar** (about x 150): the panel reads "a = 6 / 6 11 | 17 / 14 24 | 38 / P = 0.236954 / not counted", and a small black arrow sits over the bar. Down/Up step the bars.
   - Check that the panel does not cover the tallest bars. If it does, it is on the wrong side, so note it.
10. **EpiStats2x2 from Home.** Type `EpiStats2x2(12,5,8,30)`. The results open at 1/6 with no grid; Esc returns **0.000729…** to Home. `EpiStats2x2(3.5,1,2,4)` shows a message and returns −1. The catalog's argument form shows the fields eA, eB, eC, eD.
11. **Module 2 grid, 40 60 20 80 → pages 4/5 and 5/5.**
    - Page 4: two blue bars at 40 % and 20 % with black whiskers, and a magenta bracket at the right labelled "RD = 20.0%". Below: "OR = 2.67 overstates RR = 2.00 by 33 % here / because the outcome is common (Ru = 20.0 %)."
    - Page 5: 4 blue cells and 1 red cell, then grey; "Expose 5 (blue): about 1 extra case (red)."
    - Then try 10 90 20 80: one green cell, "Treat 10 …".
12. **Module 5 > Case-Control.**
    - The grid title reads "STRATUM 1 OF 2: CASE-CONTROL", columns Case/Control. Type 15 5 30 30 → Run → "STRATUM 2 OF 2" → 40 30 20 60 → Run.
    - Page 1/3: OR₁ = 3.000 (0.97-9.30), OR₂ = 4.000 (2.00-8.00).
    - Page 2/3: Crude OR = 2.829 (1.64-4.89), M-H OR = 3.681 (2.04-6.66); "M-H χ² (1 df) = 19.443, p < 0.0001", corrected 18.228; "Breslow-Day χ² (1 df) = 0.181, p = 0.670"; the four reading lines in black, no red verdict.
13. **Page 3/3, the forest plot.**
    - Two blue squares (stratum 2's bigger, w = 68 %), a black crude square, and a magenta diamond spanning about 2.0-6.7.
    - A dotted vertical line at 1, and ticks 1, 2, 5, 10.
    - **Tap stratum 1's row:** it turns grey with a hollow square and "dropped"; the readout becomes "M-H OR = 4.000 (2.00-8.00), stratum 2 only" and "One stratum left …".
    - Tap stratum 2: "At least one stratum must stay in the pool."
    - Tap stratum 1 again to restore it. Down drops stratum 2.
    - In Home, `EP_ORMH_CI` is still {2.036…, 6.655…}.
14. **Cohort and rates.**
    - Cohort: type 12 88 4 96 / 25 75 10 90; M-H RR = 2.643 (1.48-4.71) with "Greenland-Robins (1985)".
    - Then the same strata through **Values** (cases 12, 4; totals 100, 100): the same RR. A total of 10 with 12 cases is refused.
    - Rates: 15 1200 8 1500 / 30 900 20 1100; the grid's Total column shows the rates; IRR_MH = 1.978 (1.23-3.17).
    - Type person-time 1200.5: it stays 1200.5.
15. **Footer and soft-key strip.** On every new page the dodger-blue footer is a single line, and nothing new runs into it. The stratum grids show the soft keys Edit | Values | Clear | (blank) | Cancel | Run.
16. **Large N, Fisher page.**
    - `EpiStats2x2(700,300,280,700)` (N = 1980): page 4 takes a moment (about 4000 `es_lngamma` calls, the same work es_FisherExact already does at entry; note the seconds on each calculator). It shows about 269 thin bars and "269 bars: too narrow to label; a tap picks one". A tap anywhere on the plot picks a bar.
    - `EpiStats2x2(600,500,450,520)`: page 4 says N > 2000.
17. **G1 speed.** Repeat step 16's timing on the G1. Also check that forest-plot taps redraw promptly (one frame, about 60 drawing calls).
18. **`MAKELIST(…, K, …)`.** Module 1 page 4 uses Home's K as its counter (three new calls, the verified form). After it, K in Home holds the last count, as v1.5's prevalence page already does.
19. **Glyphs in strings:** χ², ₁, ₂ (by CHAR(8321)/CHAR(8322)), ←/→ (as v1.5), "─── … ───" (as v1.5). If any shows as a box, note where.

---

## (c) Not confirmed, or left as it was

- **Hardware.** None of this has run on a calculator. In particular, these are copied or estimated rather than observed:
  - an `EXPORT` routine with four parameters in this file;
  - a 14-item simple `CHOOSE`;
  - `LEFT(s, 1)` in `es_EqTxt` (verified on strings, §3);
  - lists of strings indexed by a variable (`sgT(sgK)`);
  - `RETURN` inside `FOR` (es_StratGrids);
  - every new pixel position.
- **Font widths** are estimates (6.5 px per character in font 1). The longest new lines are 44-47 characters: the readings lines, "Strata ORs homogeneous (Breslow-Day p = 0.67):", and the OR-vs-RR sentence.
- **z = 1.96 vs 1.959964.** The per-stratum and crude CIs reuse `es_CalcORCI` and `es_CalcRRCI` (1.96, unchanged from v1.5), while the M-H CIs use 1.959964 to match statsmodels. With one stratum left, the M-H CI therefore equals that stratum's own CI to the 2 printed decimals, but not to the 4th significant figure.
- **No homogeneity test for RR or IRR.** statsmodels has none, and none was asked for. The page says "no formal test here" and keeps v1.4's "more than half" heuristic, labelled as a heuristic.
- **No M-H χ² for rates.** Not requested; the rates summary skips the Tests block.
- **Tarone's correction** is checked in Python but not shown, because statsmodels does not apply it by default.
- **The Fisher bars are not grouped above 60.** They get thinner (down to shared pixel columns past 272 bars), and the page says so.
- **`EP_MH_CHI`/`EP_MH_P`** come from whichever case-control or cohort run was last.
- **Not changed:** modules 3, 4 and 6, the sample-size screens, and all v1.5 computations.
- **ConTable2/FEP features dropped deliberately:** the MSGBOX output, and ConTable2's refusal of tables with a zero margin.
- The kit's full parse stops at the file-level `LOCAL` (tool limit); the translated copy parses.
