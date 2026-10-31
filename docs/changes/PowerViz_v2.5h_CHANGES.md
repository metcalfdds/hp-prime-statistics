# PowerViz v2.5h: changes

*Superseded the same day by v2.5i, v2.5j and v2.5k (fixes and a new readout box from Roger's first run of v2.5h on the calculator; see `PowerViz_v2.5i_CHANGES.md` and `PowerViz_v2.5j_CHANGES.md`). v2.5h was not committed on its own. Its verify script, `verify_PowerViz_v2.5h.py`, is in the author's folder; `verify_PowerViz_v2.5k.py` runs its checks on v2.5k.*

*31 October 2026. Built from v2.5g by `make_v25h.py` (18 exact replacements, each required to match once). 3,612 lines: 2,299 of code and 1,149 of comments. v2.5g, the fifth test, was not committed on its own; this version carries it, and `PowerViz_v2.5g_CHANGES.md` describes that part.*

## Why

Roger, 31 Oct 2026, after v2.5g:
- "we need to add Levene's F test and Cohen's d unless I missed those". Cohen's d was already on v2.5g's panel.
- Asked which Levene he wanted: **both**, a power page and a page for real data.
- For d: "make d more prominent".
- "and how to interpret those for students".

## What changed (line numbers are v2.5h's)

### Levene's test: power (Menu, test 5; `pv_LvPage`, 2692)

**What it asks:** how often Levene's test would say "spreads differ" when σ₁ and σ₂ really are as typed, at the n on screen and the α on screen (two-sided).

**Which Levene:** the absolute deviations from the group **means**. That is the form SPSS prints in its Independent Samples Test table ([spss-tutorials.com](https://www.spss-tutorials.com/levenes-test-in-spss): "the absolute differences between all scores and their (group) means").

**How the power is found:**
- **Simulated** when n₁ + n₂ ≤ 240 (`pv_LvSim`, 2645): 100 to 400 pairs of normal samples, about 24,000 values in all.
  - A progress bar is drawn straight to the screen, and Esc stops early.
  - The result shows ±2 SE.
  - Levene's F for two groups is t² on the deviations, so the critical value is `(-STUDENT_ICDF(N-2, α/2))²` and no F quantile is needed.
  - Normal values come from `pv_RNorm` (2585), Marsaglia's polar method.
- **A large-sample formula** past 240 (`pv_LvApx`, 2622). It is within 0.01–0.02 of a 40,000-pair simulation there (verify E2).
- The result is cached: reopening the page with nothing changed does not simulate again.

**Beside it, the exact F test of s₁²/s₂² for normal data** (`pv_FPow`, 2605), from `FISHER_CDF`. Both tails are computed as lower tails, the upper critical value as 1/(a lower quantile), so the formula never uses 1 − α. The page plots that test's power against σ ratios (the larger σ over the smaller) from 1 to 3–10, with Levene's simulated point (red, ±2 SE) and the F test's point (magenta) at the ratio on screen, and a dotted 0.80 line.

**Page 2, "Levene's test: what it means"**, at the defaults (σ 10/20, n 40/20, 400 simulated pairs):
- "test flags it in about 87 of 100 such studies";
- "In the other 13, a 'Levene first' rule keeps 'equal spreads' and picks the pooled t test, whose α can be far off (Cohen 1988, p. 44)". With n₁ = n₂ the line reads instead "which with n₁ = n₂ stays close to α"; with σ₁ = σ₂, "Levene's test still says 'spreads differ' in about 5 of 100 studies: that is α";
- "A non-significant Levene does NOT show that the spreads are equal: it may just lack power";
- "The F test … is stronger with normal data, but skewed data fool it badly. Levene's test (means, as SPSS) is fooled less; its median form (Brown-Forsythe) hardly at all";
- "Simplest rule: use Welch's t test every time (Delacre, Lakens & Leys 2017)".

**The sources for page 2:**
- Cohen (1988), *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed., p. 44: with σ_A ≠ σ_B and n_A ≠ n_B, the nominal values "may differ greatly from the true values".
- Delacre, M., Lakens, D., & Leys, C. (2017), "Why psychologists should by default use Welch's t-test instead of Student's t-test", *International Review of Social Psychology* 30(1):92–101, doi:10.5334/irsp.82.

**The page's claims, each simulated in the verify script (E6):**
- **The pooled t test with n₁ = n₂:** at a σ ratio of 2–3 its true α is 5.1–5.9% at a nominal 5%.
- **Skewed data with equal spreads:** at a nominal 5%, the true α is 17–52% for the F test, 10–19% for Levene's mean form, and 4–5% for Brown-Forsythe (lognormal, exponential and χ²(4) data).
- **The first wording was wrong.** It said "Levene (1960) built his test to cope with that". That was too strong for the mean form, and the check caught it before filing.

### Two samples: data (Menu; `pv_DataPage`, 2999)

**Sources:**
- **The 1970 draft lottery**, January–June against July–December birthdays (`pv_Draft`, 2853). These are AnovaLab's 366 numbers, checked number for number. They also match published facts: 1 on September 14 (day 258), 2 on April 24, and only December 2, 12, 15, 17 and 19 above 195 ([Wikipedia, Draft lottery (1969)](https://en.wikipedia.org/wiki/Draft_lottery_(1969))). Source: Fienberg (1971), *Science* 171:255.
- **Insect sprays C and F**, AnovaLab's lists (Beall 1942).
- **The student's own D1 and D2** from the Statistics 1Var app (`pv_ReadD`, AnovaLab's IFERR pattern). A box explains what to do when they are missing or hold fewer than 2 values, and another box appears when neither group has any spread.

**Page 1:**
- A strip plot of both samples: dots, each mean a red bar, ±1 s in green. A tick label is kept inside the screen and left out if it would run into the one before it (long labels such as 1.5205 on a narrow range; the layout check found the overrun).
- n, mean and s for each group.
- Levene's F and p, means form, labelled "as SPSS".
- Brown-Forsythe's p, medians form, as R's car and AnovaLab use.
- The pooled t test, and Welch's t test with Satterthwaite df.
- **Cohen's d in large magenta type** (font 4), pooled s, with Cohen's word for its size and the σ' form beside it.

**`pv_TwoS` (2947)** returns all 18 numbers as one list, so the verify script checks it against SciPy directly.
- **Very large or very small data** (beyond 1E50 or under 1E-50) is first divided by a power of 10, so no square of a square runs out of range. A power of 10 divides exactly on the Prime, whose numbers are decimal. t, F, p, df and d do not change; the means and SDs are multiplied back. Everyday data is left exactly as it is. The verify script's final run found the problem: data near 1E100 or 1E-100 made the Welch df overflow or divide by zero in the PC harness. (The Prime's own range, to 1E499, would have carried those two cases, but not data near 1E200.)
- **The means and SDs get enough decimals for 3 significant digits of the larger s**, 2 at least and 8 at most. Glass refractive indices (s about 0.0001) print as "mean 1.518188, s 0.000088", not "mean 1.52, s 0.00"; blood alcohol levels get 4 decimals. The presets keep 2.

**Page 2, "Two samples: what it means":**
- **SPREADS:**
  - Levene's p against α: "the spreads look different. Read Welch's t."
  - or "no clear sign they differ. That is not proof they are equal".
- **MEANS:**
  - Welch's p, read as "If the population means were equal, a gap at least this big (either way) would turn up about x % / less than 0.1 % of the time".
  - Whether the pooled and Welch tests agree about p < α, or "DISAGREE: go with Welch's".
- **SIZE:** "d = −0.44. Jul-Dec's mean is 0.44 SDs below Jan-Jun's: a small difference (Cohen: 0.2 small, 0.5 medium, 0.8 large)".
- **The closing line:** "p says whether a gap is likely to be real; d says how big it is. Report both."

### d on the plot (`pv_Draw`, 1691)

- A magenta arrow runs between the H₀ and H₁ centres, 6 px below the plot top, labelled "d = 0.32" (or "h = …" for the proportion tests). The label sits under the arrow, or beside it when the arrow is too short; there is no arrow when the centres are under 6 px apart.
- The panel's d cell is magenta to match.
- Help page 2 has a line for it, and page 5 another.

### Help page 5, "Levene, data" (3257)

It explains the two new menu items and where to put your own data (Apps, Statistics 1Var, Num: D1 and D2). The help pages are now numbered 1/5 to 5/5.

### The menu (3280)

There are 11 items: "Levene's test: power" (7) and "Two samples: data" (8) are new. Change test, Help and Return move to 9, A and B.

## Not changed

- The engine and every number of tests 1–5.
- Tests 1–4's screens, except the d label under the new arrow, the d cell's colour, the help titles, help page 2's new line and page 3's footer (verify A1–A3).

## Verification

`verify_PowerViz_v2.5h.py`, output `verify_PowerViz_v2.5h_output.txt`: **82 PASS, 0 FAIL**.

- **A, against v2.5f:**
  - Tests 1–4's main view in 512 states, the curve views and the formula page, and help pages 1–3. The allowed differences are each checked.
  - The engine's numbers, the tiny-α critical z and the menus.
- **B and C, test 5:** every check of v2.5g's script, rerun on v2.5h.
- **E, Levene's power page:**
  - `pv_FPow` equals SciPy in 144 cases.
  - `pv_LvApx` is within 0.02 of a 40,000-pair simulation wherever it is used.
  - `pv_LvSim`'s 400 pairs are within 3.5 SE of a 40,000-pair simulation in four settings.
  - `pv_RNorm`: 20,000 draws are N(0, 1) (KS test).
  - The page texts in five cases, the cache, and page 2's claims, simulated.
- **F, the data page:**
  - `pv_TwoS` equals SciPy (Levene with means and with medians, pooled and Welch t, Welch df, both d's) on the three presets and 200 random pairs of samples.
  - The same samples times 1E100, 1E-100, 1E60, 1E-60, 1E200 and 1E-200 give the same t, F, p, df and d, with the means and SDs times the factor.
  - The means and SDs print with 6, 4 and 2 decimals for spreads near 0.0001, 0.01 and 5.
  - The presets match AnovaLab's lists, and the draft data matches the published facts.
  - The page texts.
  - D1/D2, the boxes, and a pair where the pooled and Welch tests disagree.
  - A robustness sweep: 8 odd data sets and 8 odd Levene settings give a page or a box, never an error.
- **G, d on the plot:** the label and arrow in all five tests, and no arrow when there is no effect.
- **D, layout:** no firm overlap, straddle or overrun that v2.5f lacks.

## Gate

`ppl_gate_v1c.py PowerViz_v2.5h.txt PowerViz_v2.5g.txt`: **RESULT: PASS**.
- The gate caught a local named `lsq`, which is the built-in LSQ with case ignored; it is now `lsBt`.
- The twelve new E1 notes (18 against v2.5g's 6) are list indexing, which the checker reads as calls.
- Its full-parse step stops at the bare `EXPORT EP_…;` declarations, as it does on v2.5g; the harness reads the whole file.
- lint_ppl's four problems are the version number in the file name, as on v2.5g (the calculator's copy is named PowerViz).
- No new name differs from another only by case. The two older pairs (`dV`/`dv`, `dD`/`dd`) are in different routines, as in v2.5f.

## Device checklist (G2 first, then G1)

Replace PowerViz by opening it in the Connectivity Kit and pasting over it, then Check. Items 1–12 of `PowerViz_v2.5g_CHANGES.md` still apply. Then:

13. **The arrow:** at the defaults of any test, a magenta arrow joins the H₀ and H₁ centres near the plot top, with "d = 0.32" under it (test 5). Drag H₁: the arrow and label follow.
14. **Menu → Levene's test: power** (test 5, defaults):
    - a progress bar fills, and Esc stops it early;
    - **write down the time it takes on each calculator**;
    - page 1 shows the magenta curve, the red point near 0.87 with its ± bar, and the two numbers;
    - page 2 is readable, with nothing off the right edge.
15. **The same, with n = 200/100** (Edit): no simulation, "Levene (large-sample formula)".
16. **Menu → Two samples: data → 1970 draft lottery:**
    - the strip plot: two bands, red mean bars, green ±1 s lines;
    - the readouts "Levene (means, as SPSS): F = 0.96, p = 0.329", "Welch t(362.6) = −4.20, p < 0.001", and d = −0.44 in large magenta type;
    - page 2 reads sensibly.
17. **Insect sprays C and F:** Levene p < 0.001, Brown-Forsythe p = 0.011, d = 3.16.
18. **Your data:**
    - Put a few numbers in D1 and D2 (Apps → Statistics 1Var → Num), then choose "Your data". The page should show D1/D2.
    - Numbers with a tiny spread (say 1.51812, 1.51825, 1.51809 in D1 and 1.52031, 1.52044, 1.52027 in D2) should show the means and SDs with 6 decimals.
    - Clear D2 and try again: the box should explain where the data goes.

## Unresolved

- Levene's simulation speed on the G1 and G2 (checklist 14). In the harness, 400 pairs of 40 + 20 values take under a second. On the G1 roughly 24,000 values × ~9 statements is about 35 s by SpeedProbe's 0.17 ms a statement, and about 10 s on a G2. **Those are estimates, not measurements.** If the G1 is too slow, MicroPython is the next step (Lessons Learned §1).
- Data whose spread is below about 1E-8 prints its means, SDs and tick labels as rows of zeros (8 decimals at most); its t, p and d are still right. No classroom data comes near that, so it is left as it is.
- The tick labels' right-edge limit uses about 6 px a character in font 1, as the d arrow's label does. It is checked in the harness only (checklist 18, the tiny-spread numbers).
- Glyphs: the new pages use only characters already seen to render on the Prime (± is the only one new to PowerViz). A first draft had ÷, the prime ′ and the en dash –, none of them on GfxProbe's list; they became /, ' and -, as v2.5g's help page already writes σ'.
