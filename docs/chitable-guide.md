# ChiTable beta 3d: User's Guide

ChiTable runs a chi-square test for a 2 × 2, 2 × 3 or 3 × 2 table on the HP Prime. The engine is pure PPL, with no MicroPython: the arithmetic is light, and the live touch screens belong in PPL. Beta 3 adds a few **exact answers from the calculator's CAS** (its computer algebra system), shown beside the decimals the program has always computed.

**Status: beta 3d (19 Oct 2026) has run in the PC test harness only; beta 3c passed the emulator retest on 17 Oct 2026. Betas 2 to 3d have not yet been run on hardware.** Beta 2 passed every item of its checklist on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026, with every number matching SciPy. Beta 3b's CAS lines have run only in the off-device harness. They use the CAS call form that CASProbe beta 1b found on the emulator, the one ErrorRate beta 1a has already shown working there. Beta 1j ran on an HP Prime G2 and a G1, both on the 2026-09-09 firmware (2.4.2), on 10 Oct 2026. That run covered the entry grid and its soft keys, the Values form, the results pages and all three plots.

- **What has been checked off-device:**
  - The arithmetic was verified against scipy and statsmodels on 4,900 random tables. It has not changed since.
  - Beta 2's formulas (the Fisher distribution, ×10 N, the α drag and snap, the morph geometry, the Simpson figures) are checked against SciPy in `verify_ChiTable.py`.
  - Beta 3's exact answers are checked in `verify_ChiTable_beta3.py`. Every CAS text the program builds was run through desktop Giac (the engine inside the Prime's CAS, a newer build) for 18 chosen and 450 random tables. Each answer was compared with Python's exact fractions and with SciPy's `fisher_exact` and `chi2_contingency`. Every screen was also run in the off-device harness twice: once with Giac answering, and once with every CAS call failing.
  - Beta 3b's checks are in `verify_ChiTable_beta3b.py` (5,969 checks, 0 failures), in the harness that follows the Prime's CAS (`ppl_run_v3c`).
- **What to try first on the calculator:** `ChiTable_beta3_CHANGES.md` has a device checklist, ordered from least to most risky; `ChiTable_beta3a_CHANGES.md` and `ChiTable_beta3b_CHANGES.md` add what changed since.

**beta 3d (19 Oct 2026): fixes from the fleet review.**
- **Newcombe's interval for the risk difference.** It is built from the two rows' Wilson intervals. It never leaves [−1, 1] and never shrinks to width 0 at the extremes. The Wald interval it replaces did both: it left [−1, 1] in 17.8 % of the 2 × 2 tables with row totals up to 12. For the tea table, Wald gave (−0.10, 1.10) and Newcombe gives (−0.14, 0.79).
- **Every chi-square p, and the `CS_P` export, is computed as a lower tail**: 2Φ(−√χ²) for 1 df, e^(−χ²/2) for 2 df. The Prime's 12-digit arithmetic made 1 − CDF exactly 0 past χ² ≈ 52; these forms keep their digits.
- **The help now states the expected-count rule the program applies.**

**beta 3c (17 Oct 2026): the compile fix.** Two comment lines moved out of a `CHOOSE` list. A comment inside an open bracket is a syntax error on the Prime.

**beta 3b (17 Oct 2026): two menu lines shortened.** The emulator cut two CHOOSE lines at the edge of the box. The Results menu now reads "N / 10: counts divided by 10", and the Examples list reads "Death penalty × defendant" and "Death penalty × victim". Each results page still names the variable in full.

**beta 3a (17 Oct 2026): the CAS call form.** CASProbe beta 1b showed that `CAS(s)` hands back the text of `s` unevaluated, so beta 3's exact lines would always have fallen back to the decimal. `csCas` now sends the text through `EXPR` and asks the CAS for a string. Nothing else changed.

**beta 3 (16 Oct 2026): exact answers from the CAS.** Everything in beta 2 is kept. The decimals still come from the same device-tested routines (`csCompute`, `csFisher`).

- **Fisher's p as a fraction.** On results page 6 and on the Fisher plot: **p = 17/35 = 0.4857** for the lady tasting tea, [[3, 1], [1, 3]]. The CAS adds exactly the tables the program's Fisher test adds. When a fraction is too long for its line it is never cut short: the line gives the decimal and says how many digits the fraction has.
- **A new last results page, "Where the numbers come from."** For a 2 × 2 it shows two things:
  - χ² by the shortcut N(ad − bc)² / (r₁ r₂ c₁ c₂), with your counts put in and simplified to one fraction;
  - Fisher's p as counting: "34 of the 70 equally likely ways, p = 34/70 = 17/35".
  
  For a 2 × 3 or 3 × 2 it shows χ² as one exact fraction of Σ (O − E)²/E.
- **The badge.** Every exact answer carries one, in blue: **exact (CAS)** when the CAS produced it, **decimal** when it could not and you see the program's own decimal.
- **Help page 5** explains the exact answers and the badge.

beta 2 (16 Oct 2026): touch and graphics. New features were added; the device-tested screens were kept.

- **Drag a bar.** Drag a solid (observed) bar in the bars plot. Every expected bar moves with it, and χ², p and the verdict colour update as you drag.
- **Drag the critical line.** Drag the dotted red line on the χ² curve to set α. It snaps to the usual values.
- **Soft keys.** A soft-key strip runs along the bottom of the results pages and every plot.
- **Tap a cell.** On results page 1, a tap on a cell shows how its expected count is made.
- **×10 N and N / 10.** Both are on the Menu soft key: V is the effect size; p depends on N.
- **Independence morph.** On the mosaic plot, it turns the observed table into what independence predicts.
- **Two new plots.** The adjusted residuals, and Fisher's exact distribution for a 2 × 2.
- **New help page.** It shows why df = (r − 1)(c − 1).
- **Simpson's paradox page.** A new item under Examples.
- **Layout.** The plots are 12 px shorter so their text clears the soft keys, and the results pages' page number moved to a corner.

beta 1l (16 Oct 2026): four small fixes from the fleet review.
- The help names menu items instead of numbering them.
- On the last results page a right-half tap or Right stays put, where it used to leave for the menu.
- The curve plot computes its density once per column.
- A comment marks the df > 2 branch as kept for later.

beta 1k (10 Oct 2026): clean exits.
- The finger-lift drains go through `csDrain()`, which gives up after one second, so a phantom touch can no longer freeze the program.
- Quit returns the summary line instead of printing it, so no Terminal screen is left open.
- No change to the arithmetic or the screens.

beta 1j (10 Oct 2026): header only. It records the G1 run; there is no code change.

beta 1i (10 Oct 2026): the verdict in Roger's words. It reads "REJECT H₀ because the data show evidence of an association between the variables" or "DO NOT REJECT H₀ because the data do not show an association between the variables". The interpretation page's sentence matches.

beta 1h (10 Oct 2026): the verdict is two lines and names both hypotheses. It reads either "REJECT H₀ because there is an association / and ACCEPT H₁: the variables are related" or "DO NOT REJECT H₀ because there is not enough / evidence of an association; do not accept H₁". The interpretation page says the same, and the effect-size block moves down 6 px.

beta 1g (10 Oct 2026): header only. It records the first run on a G2; there is no code change.

beta 1f (10 Oct 2026): the decision line reads "REJECT H₀: there is evidence of an association" or "DO NOT REJECT H₀: there is not enough evidence". H₀ and H₁ carry subscript digits, and α its Greek letter, everywhere on screen. The program uses H₁ rather than Hₐ because the subscript 1 is a verified glyph and a subscript a is not.

beta 1e (10 Oct 2026): CHOOSE labels items 10–12 as A, B and C on the Prime, so the "no table yet" message points at example (A). The results footer says "scroll output" rather than "pages".

beta 1d (10 Oct 2026): screen labels and glyphs.
- The soft key reads **Run** (was Done).
- The menu items are unnumbered, since CHOOSE numbers them, and short enough for the choose box (item 4 was being cut off).
- χ² is written with its own glyphs everywhere on screen: `CHAR(967) + CHAR(178)`, chi and a superscript two, the same pair EpiStats v1.2 draws literally. ² is used for G² and the squares in formulas, and × for the table shapes.
- The code stays ASCII, and the Home export names (`CS_X2` …) are unchanged.

beta 1c (10 Oct 2026): soft keys on the entry grid.
- **Edit · Values · Clear · Cancel · Done** run along the bottom, drawn with `DRAWMENU` and read as taps in the bottom strip: six 53-px slots, the geometry CHOOSE_R, LibMenu and PrimeFX use.
- The keys remain as shortcuts: Enter = Edit, + = Values, Esc = Cancel.
- Done runs the checks and computes. Cancel keeps the counts but marks any old results stale.

beta 1b (10 Oct 2026): the first paste on the G2 stopped at the first file-level `LOCAL` line, with the cursor after `csC`. The Prime matches built-in names **case-insensitively**: `csC` is `CSC` (cosecant), and the program's own name, `ChiSquare`, is `CHISQUARE`, the density function the curve plot calls. Renamed `csC → csNC`, `csR → csNR`, and the program to **ChiTable**. Nothing else changed.

beta 1a (10 Oct 2026): readouts and footers brought to house style after the library search. No change to the arithmetic.

Run `ChiTable()` from the Program Catalog. The program was called ChiSquare until beta 1b. Install it as `.txt` through the Connectivity Kit editor.

## The menu

The calculator numbers the items itself: 1–9, then A–E for items 10–14.

| Item | What it does |
|---|---|
| New table 2 × 2 / 2 × 3 / 3 × 2 | Draws the empty table and opens the touch grid with its soft keys |
| Edit the counts | Reopens the grid for the current table (your own or an example) |
| Results | Seven pages (six for a 2 × 3 or 3 × 2); see below |
| Plot: observed vs expected | Observed bars (solid) beside expected bars (pale), one pair per cell, coloured by column. **Drag a solid bar** to change its count; see below |
| Plot: mosaic | Bar width = the row's share of N; tile height = row %. Tiles are coloured by adjusted residual: blue = more than expected, red = fewer, darker beyond \|4\|. The grey "all" bar on the right is what every bar would look like under independence. **Morph** plays that change |
| Plot: χ² curve and p | The χ² curve for df, with the p-value shaded beyond X² and the critical value as a dotted red line. **Drag the red line** to set α |
| Plot: adjusted residuals | One bar per cell: blue up (more than expected), red down (fewer), solid beyond the dotted ±2 lines. Tap a bar for its O, E and residual |
| Plot: Fisher exact (2 × 2) | Every 2 × 2 table with these margins, one bar each. Tap a bar to see that table. **Beta 3:** the two-sided p as an exact fraction |
| Set α | Default 0.05. A custom α shows its own decimals (0.037) |
| Examples | Four built-in tables and the Simpson's paradox page (below) |
| Help | Five pages; the fourth shows why df = (r − 1)(c − 1), the fifth explains the exact answers |
| Quit | Returns the summary line to Home |

The results pages and the plots are one set of screens. Their soft keys move between them without going back to this menu.

## Typing the table

Tap a cell (or move the red frame with the arrows and tap **Edit**) and type its **observed count**. Row and column totals and N update as you go. The soft keys along the bottom:

| Soft key | Does | Key shortcut |
|---|---|---|
| Edit | type the count of the framed cell | Enter |
| Values | type every count in one form | + |
| Clear | zero the whole table | — |
| Cancel | back to the menu, counts kept, results marked stale | Esc |
| Run | run the checks and compute | — |

Counts are rounded to whole numbers. Run refuses a negative count, an empty table, or a row or column that adds to 0, with a message that says why, and the grid stays open so the table can be fixed. The counts that Run accepts are the ones **Restore** puts back later.

## The results pages

1. **Observed and expected:** O in black, E = (row total × column total) / N in blue. A cell with E < 5 gets a red frame. Tap a cell: it gets a magenta frame, and a line under the table (in the title area for a 3-row table) shows how its E is made: "R1 C1:  E = 483 × 68 / 674 = 48.73 — what it would hold if the variables were unrelated".
2. **Percentages:** row %, column % and % of N in every cell, with the marginal percentages in the totals.
3. **The test:** χ², df, p (right tail), the critical value at α, the decision, Cramér's V with Cohen's label, the contingency coefficient C, the likelihood-ratio G², the smallest expected count and how many cells fall below 5.
4. **Contributions:** (O − E)²/E per cell on top (they add to χ², shown in the corner), and the adjusted residual, blue when ≥ 2, red when ≤ −2.
5. **What it means:** an APA-style line (`χ²(1, N = 674) = 13.16, p < .001, V = .14`), the decision in words, the effect size, the cell that drives the result, and the expected-count check.
6. **2 × 2 only:** p₁ and p₂, the two-proportion z (z² = χ²), Yates' corrected χ², Fisher's exact two-sided p, risk difference (Newcombe's interval since beta 3d), relative risk and odds ratio (log method) with 95% intervals, and phi. **Beta 3:** Fisher's p has its own line, as an exact fraction from the CAS when it fits ("p = 17/35 = 0.4857"), with its badge. The lines below it moved down a few pixels to make room.
7. **Where the numbers come from** (new; it is page 6 for a 2 × 3 or 3 × 2). See *Exact answers* below.

The page number ("3/7") sits in a corner: the top-left cell of the table pages, the top right of the text pages. You can move between pages several ways:

- ← → or a tap on the left or right half of the screen.
- The **Prev** / **Next** soft keys.
- Enter steps forward, and past the last page returns to the menu.
- Esc returns to the menu from any page.

## Exact answers (CAS, new in beta 3)

The CAS can do two things the rest of the program cannot: exact fractions, and whole numbers of any size. ChiTable uses it for two lessons.

**χ² is one exact number made from your counts.** For a 2 × 2 the last page writes:

```
χ² = N(ad - bc)² / (r₁ r₂ c₁ c₂)
   = 674 × (64 × 155 - 451 × 4)²
       / (515 × 159 × 68 × 606)
   = 674 × 8116² / 3374317080
   = 5549501668/421789635 = 13.157
```

These are example 2's numbers. They give the same χ² as the sum of (O − E)²/E on page 3. Note that ad − bc = 0 would make χ² = 0. For a 2 × 3 or 3 × 2 the page writes out the first cell's (O − E)²/E with E = R × C / N, then the whole sum as one fraction. Example 3 gives 3668733438511/122005828000 = 30.070. Every E is itself a fraction, so χ² is one too.

**Fisher's test is counting, not approximating.** With the totals fixed, the table whose top-left count is a happens in C(r₁, a) × C(r₂, c₁ − a) of the C(N, c₁) equally likely ways. The two-sided p adds the tables that are no likelier than yours (the red and magenta bars of the Fisher plot). For the lady tasting tea, [[3, 1], [1, 3]]:

```
P(a) = C(4, a) × C(4, 4 - a) / C(8, 4)
Tables no likelier than yours (red + magenta):
  34 of the 70 equally likely ways
p = 34/70 = 17/35 = 0.4857
```

The CAS uses exactly the tables `csFisher` adds: every table whose probability is at most the observed one's times 1.0000001. That is the hair of tolerance R and SciPy also use, so a tie always counts. In the tea example, a = 1 ties with your a = 3.

**When an answer cannot be shown in full.**
- **Too long for its line:** the line keeps the decimal and counts the digits instead. Example 2 shows "p = 0.0001 (140-digit fraction)".
- **Too big to be worth asking:** when C(N, c₁) has more than 100 digits, the program does not ask the CAS at all, and the page says so. Example 2 after ×10 N shows "C(6740, 680) has about 956 digits: too big".
- **More than 3,000 tables:** Fisher's test is not computed (as before), so there is no fraction either.

**The badge.** **exact (CAS)** means the CAS produced the line. **decimal** means it did not: the CAS failed, its answer was not a clean fraction, or the answer was too big to ask for. The program's own decimal is shown either way, so the numbers on screen never depend on the CAS.

**When the CAS is asked.** Only when a page opens (results page 6, the last page, the Fisher plot) and only when the table has changed since the last time. The answers are kept, so turning pages back and forth asks nothing new. The CAS is never asked while you drag a bar or the critical line, or while the morph plays.

## Soft keys on the results pages and plots

The strip reads **Prev · Next · Bars · Mosaic · Curve · Menu**.

| Soft key | On the results pages | On a plot |
|---|---|---|
| Prev / Next | the page before or after | the screen before or after, in the ring results → bars → mosaic → curve → residuals → Fisher (2 × 2) → results |
| Bars / Mosaic / Curve | jump to that plot | jump to that plot; on the plot itself this key does the plot's own job (below) |
| Menu | the Results menu | the Results menu |

On its own plot, the key that would jump there does something else:

- **Bars plot:** **Restore** puts back the original counts (as last run or loaded).
- **Mosaic plot:** **Morph** plays the independence morph.
- **Curve plot:** **Reset** sets α back to 0.05.

**The Results menu** offers:

- **Main menu.**
- **×10 N:** every count times 10.
- **N / 10:** every count divided by 10 and rounded. It is refused if any count would round to 0.
- **Restore the original counts.**
- Cancel stays where you are.

×10 and N / 10 show a page with N, χ², p, V and the decision before and after. Ten times the data keeps every percentage and V, multiplies χ² by ten exactly, and collapses p: **V is the effect size; p depends on N.** Example 2 gives χ² 13.16 → 131.57, p 0.0003 → < 0.0001, V 0.140 → 0.140.

The hardware keys still work everywhere: Esc and Enter leave a plot, and ← → move the highlighted cell.

There is no "More" key. The fleet's convention pages the soft keys only when a screen needs more than six; every ChiTable screen fits in six, and the rarer actions are in the Results menu.

## Touch on the plots

**Bars plot: drag a solid bar.**
- **To drag:** press a solid (observed) bar and slide up or down. The count follows your finger.
- **What updates:** every pale expected bar moves too, because E depends on the whole table. The line above the soft keys shows χ² and p, red when p < α and green when not, so you can watch the decision flip.
- **The scale:** held still while your finger is down, refitted when you lift.
- **Refused drags:** if your drag leaves a row or column adding to 0, the line warns you. When you lift, the program explains and puts the count back.
- **Keys:** Up / Down change the selected count by a step of 1, 2, 5, 10 … (about 1% of the scale). **Restore** undoes everything.
- **A tap** without dragging selects the cell, as before.

**Mosaic plot: Morph** (or the + key).
- Ten frames carry every tile from its row % to the column shares of the grey "all" bar, while the blue and red residual colours fade to grey.
- The counts in the tiles turn into the expected counts. This is H₀, independence, made visible.
- Any key or tap stops it at once. At the end the picture stays until a key or tap.

**Curve plot: drag the critical line.**
- **To drag:** press within 6 px of the dotted red line and slide sideways. α becomes the area to the right of your finger, 1 − CDF(df, x), shown under "crit".
- **The verdict** turns red the moment the line crosses X² to its left.
- **On lift** α snaps to 0.001, 0.005, 0.01, 0.02, 0.05, 0.10 or 0.20 if it is within 10% of one. Otherwise it stays as "custom α = 0.037", and the menu item and the results pages use it too.
- **Keys:** ← → step along that ladder, and **Reset** returns to 0.05.
- **Taps:** a tap outside the plot returns to the menu; a tap inside it, away from the line, does nothing.
- **The window** stays fixed while the curve is open, so the line really moves. It refits only if the line would leave the plot.

**Residual plot:** tap a bar (or use ← →) for its cell's O, E and adjusted residual.

**Fisher plot (2 × 2):**
- **What it shows:** with the margins fixed, a table is set by its top-left count *a*, and every possible *a* gets a bar with its probability.
  - **Red** is your table.
  - **Magenta** marks the tables no more probable than yours. Red plus magenta adds up to Fisher's two-sided p, the same value as on results page 6.
  - **Pale grey** is the rest.
  - A thin strip under the axis keeps the colours visible where a bar is too short to see.
- **Beta 3:** the line under the plot reads "red + magenta: p = 17/35 = 0.4857". The badge sits at the top right, beside the title, which is now "Tables with these margins" (shorter, so the badge fits).
- **Tap a bar** (or ← →) to show that table in the orange corner panel.
- **Large tables:** with more than 3,000 possible tables the plot is not drawn, and a message says the χ² approximation is excellent there.

## Conventions

- Rows are the groups (the explanatory variable); columns are the outcome. Row % compares the groups and is the percentage to report.
- The 2 × 2 measures take **column 1 as the outcome of interest**: p₁ = O(1,1)/row 1 total, p₂ = O(2,1)/row 2 total, RR = p₁/p₂, OR = ad/bc. If a cell is 0, 0.5 is added to every cell for RR and OR (Haldane–Anscombe), and the page says so.
- Fisher's exact p is two-sided in the R / scipy sense: every table no more probable than the observed one. It is skipped, with a note, when there are more than 3,000 possible tables with these margins.
- Cohen's benchmarks for V are 0.10 small, 0.30 medium and 0.50 large. These are the df* = 1 benchmarks. They apply to all three shapes because min(rows, columns) = 2, so V = phi = Cohen's w here.
- The expected-count rule on screen: when every E ≥ 5 the page says "fine". Otherwise it says the approximation is shaky and points to Fisher (2 × 2) or merging categories.

## The arithmetic

E = R·C/N; X² = Σ (O − E)²/E; df = (r − 1)(c − 1); p = 1 − CHISQUARE_CDF(df, X²) (note that `CHISQUARE` alone is the density); critical value = CHISQUARE_ICDF(df, 1 − α); G² = 2 Σ O ln(O/E); adjusted residual = (O − E)/√(E(1 − R/N)(1 − C/N)); V = √(X²/(N(min(r,c) − 1))); C = √(X²/(X² + N)); Yates X² = Σ (|O − E| − 0.5)²/E with the shrink floored at 0; z = (p₁ − p₂)/√(p̄(1 − p̄)(1/n₁ + 1/n₂)); RD with a Wald interval; RR and OR with log (Woolf) intervals.

Beta 2 (none of it changes the test's arithmetic):

- **Fisher distribution:** the hypergeometric probability of each *a*, built outward from the most probable table by the same ratios the Fisher p uses.
- **Dragged α:** α = 1 − CHISQUARE_CDF(df, x).
- **Morph:** each tile's height goes from O/R to (1 − t)·O/R + t·C/N. At t = 1 that is E/R, so every tile holds its expected count.

Beta 3, exact (the CAS; text for display only, the decimals are unchanged):

- **χ² for a 2 × 2:** N(ad − bc)²/(r₁ r₂ c₁ c₂), the same number as Σ (O − E)²/E.
- **χ² for a 2 × 3 or 3 × 2:** Σ (O − R·C/N)²/(R·C/N), summed as fractions.
- **Fisher's p:** Σ C(r₁, a) C(r₂, c₁ − a) / C(N, c₁) over the tables no more probable than the observed one. The CAS sums the one or two runs of a that count (the two tails).

## The examples

| | Table | Expected result |
|---|---|---|
| 1 | Death penalty × defendant's race, Florida murder cases 1976–87 (Radelet & Pierce 1991, as tabulated by Agresti): white 53/430, black 15/176 | X² = 1.47 (exactly 697832977/475195203), df 1, p = 0.226: no evidence of association |
| 2 | Death penalty × victim's race, same cases: white victim 64/451, black victim 4/155 | X² = 13.16 (exactly 5549501668/421789635), p = 0.0003, V = 0.14; RR 4.94 (1.83–13.35), OR 5.50 (1.97–15.35), Fisher p = 0.0001 (a 140-digit fraction) |
| 3 | Gender × party identification, 1991 GSS (Agresti, *Introduction to Categorical Data Analysis*, Table 2.5): female 762/327/468, male 484/239/477 | X² = 30.07 (exactly 3668733438511/122005828000), df 2, p < 0.0001, G² = 30.02 |
| 4 | The same table transposed (3 × 2) | identical X² (the same fraction), df and p: a transposed table is the same test |
| Simpson (examples 1 + 2) | A page, not a table | see below |

For a table of your own, type the lady tasting tea, [[3, 1], [1, 3]]. Fisher's p = 17/35 = 0.4857: 34 of the 70 ways to choose the four "milk first" cups are no likelier than the observed table. χ² = 2 exactly.

**Simpson (examples 1 + 2)** draws the two tables side by side as death-sentence percentages.

- **By defendant:** white 11.0%, black 7.9%.
- **By victim:** white 12.4%, black 2.5%.
- **Both races at once:** the same 674 cases split by both, from the three-way table that examples 1 and 2 are the margins of.
  - White victims: white defendant 11.3% (53/467), black defendant 22.9% (11/48).
  - Black victims: white defendant 0.0% (0/16), black defendant 2.8% (4/143).
- **The reversal:** overall, white defendants were sentenced to death more often. Within each victim's race, black defendants were.
- **Why:** a white victim made a death sentence far likelier, and most victims were of the defendant's own race.

Example 2 also shows RR and OR on the same data.

## Help

1. **Basics:** typing a table, E, χ², df, the assumptions, the pages.
2. **Conventions, plots and Home.**
3. **Touch, soft keys and the new plots:** every gesture and soft key in this guide, by name.
4. **Why df = (r − 1)(c − 1):** the current table's shape, with the margins fixed (orange). The (r − 1)(c − 1) white cells are free, and every grey cell is forced as its row or column total minus the cells beside it: "fill these and the rest follow". With a computed table it shows the counts.
5. **Exact answers (CAS)** (new): what the CAS adds, Fisher's test as counting (the tea example), and what the two badges mean.

## Home exports (after a run)

`CS_X2`, `CS_DF`, `CS_P`, `CS_V`, `CS_N`, and the matrices `CS_OBS`, `CS_EXP` (expected counts) and `CS_RES` (adjusted residuals). They follow the current counts, including any you dragged or scaled; use Restore first if you want the original table's values. The exact fractions are display text and are not exported.

On quitting, the program returns the summary line (`ChiTable: χ²(1, N = 674) = 13.16, p < .001, V = 0.14`) as its value, so it appears in the Home history and nothing is left open.

## First-run checks for beta 3b

The full list is in `ChiTable_beta3_CHANGES.md`, ordered from least to most risky so that the first failure tells you which features are still good. In brief:

1. **On a G1, run CASProbe beta 1b first.** The emulator settled the call form, which `csCas` now uses. The probe on the G1 times the CAS and confirms the same form on that calculator.
2. Paste and compile. The menu has 14 items, Quit is E, and the old grid and results pages behave as in beta 2.
3. The beta 2 checks (soft keys, plots, drags, the morph): unchanged code, so they should pass as before.
4. Results page 6: the lines under the Fisher p sit 4 to 7 px lower and still clear the soft keys.
5. The tea table: page 6 shows "p = 17/35 = 0.4857" with **exact (CAS)**. Page 7 shows "= 2 = 2.000" and "34 of the 70 equally likely ways". The Fisher plot shows the same fraction.
6. Example 2: the digit counts on page 6 and 7. After ×10 N, page 7 says "C(6740, 680) has about 956 digits: too big".
7. Example 3: the 2 × 3 fraction on page 6.
8. G1: how long page 7 takes to appear for example 2 (six CAS calls).

The beta 1k checks are kept for the record. All four were seen working on 10 Oct 2026 with beta 1j:

1. The entry grid redraws after a typed count, and the dialog's closing tap does not reopen it.
2. The Values form puts counts in the right cells.
3. `CS_EXP` and `CS_RES` are filled in Home.
4. Example 2's mosaic and curve look right.

## Library check (D:\HP-Prime, 10 Oct 2026; CAS notes 16 Oct 2026)

Searched the fleet, the hpcalc zips and `Community_Library` for every construct that is new to the fleet:

- **File-level `LOCAL` state** (the `cs…` variables above the first routine) is documented in the command reference ("local to the program") and used by about 1,100 corpus programs, PrimeFX and the 2048 app among them. It was first relied on in a fleet hardware run by beta 1j.
- **Element assignment into an EXPORTed matrix** (`CS_EXP(r, c) := …` after `MAKEMAT`): 13 corpus programs do exactly this.
- **`INPUT` label lists built from a variable or by concatenation:** Fingerspelling, Foundation, CostsReturn, Framework and Control Systems.
- **`CHISQUARE_ICDF`:** RANDO in the Community Library. **`CHISQUARE`** (the density): StatDist.
- **FEP and ConTable2** use the same conventions as this program: two-sided Fisher, Yates with the `MAX(0, …)` clamp, Haldane +0.5, Woolf intervals.

Beta 2 adds no construct beyond those the fleet has already used on hardware: `MOUSE` polled while a finger is down, the capped `csDrain`, `DRAWMENU` after the blit, `RGB()`, `TICKS`, and `MAKELIST` with Home's `K`.

Beta 3 adds two, both behind the fleet's CAS fence (Lessons Learned v7h §9b):

- **The CAS call**, inside IFERR in the one routine `csCas`. Beta 3 used `STRING(CAS(s))`, as spect.hpprgm in the corpus does. CASProbe beta 1b showed that this hands back the text of `s` unevaluated. Beta 3a uses the form the probe found working: `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))`, with the surrounding quotes dropped.
- **`INSTRING`**, which ran in PyProbe beta 2b (emulator).

The CAS text uses only `comb`, `sum(seq(...))` with whole-number bounds, and the four operations. A `sum` over a symbolic index makes Giac try to solve Gamma equations, so it is avoided.

It deliberately avoids the unverified graphics: translucent `FILLPOLY_P`/`TRIANGLE_P`, the 10-argument `BLIT_P`, a second finger, `WAIT(-1)` gestures, and the ± and ÷ glyphs.

## Credit

Concept, direction, classroom judgement and all hardware testing: Roger Metcalf. Implementation, the arithmetic and its verification against scipy/statsmodels and desktop Giac, the off-device screen renderer and harness runs, and this guide: Claude (Anthropic). The example data are Radelet & Pierce (1991) via Agresti, and the 1991 General Social Survey via Agresti.

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty.*

*Firmware: betas 2 and 3b have not yet been run on hardware; beta 2 passed on the HP Prime Virtual Calculator (2.4.2) on 17 Oct 2026; beta 3b's CAS lines have run only in the harness; beta 1j ran on the G2 and G1 (2026-09-09 firmware, 2.4.2).*
