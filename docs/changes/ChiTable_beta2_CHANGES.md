# ChiTable beta 2: changes from beta 1l

*16 October 2026. **Not yet run on hardware.** Beta 1j is the version both calculators ran (G2 and G1, 2026-09-09 firmware, 10 Oct 2026). Beta 1l's fixes (help names items, the last page stays put, cached curve density, the df > 2 comment) are all kept.*

Beta 2 is built on beta 1l and adds to it rather than rewriting it. Every new feature lives in a new routine. An old routine was touched only where a feature needed it.

- **Untouched, checked byte for byte against beta 1l:** `csCompute`, `csFisher`, `csCheck`, `csTotals`, `csAskAll`, `csNewTable`, `csSetAlpha`, `csDrain`, `csWaitAny`.
- `csPageTest`, `csPageInterp` and `csPage2x2` changed one line each: the footer line.

The file grows from 1,438 to 2,716 lines, from 34 routines to 62.

## 1 · Changes

Line numbers are beta 1l's, then beta 2's.

### Existing routines touched

1. **`csAStr` (260 → 353)** shows a custom α with the decimals it needs: 0.037 (not 0.04), 0.0037. The ladder values print exactly as before.
2. **`csGrid` (553 → 876)**, results page 1:
   - **Tapped cell, 2-row table:** the cell gets a magenta frame. The two lines under the table become "R1 C1:  E = 515 × 68 / 674 = 51.96" and "what it would hold if the variables were unrelated".
   - **Tapped cell, 3-row table:** the same two lines replace the title instead, since there is no room under the table.
   - **The page-1 note** now reads "Tap a cell: how its E is made.  Red frame: E < 5." (was "E = row total x col total / N.  Red frame: E < 5.").
   - **The footer** (`csFoot`) is drawn in the empty top-left corner cell. It now holds only the page number, "1/6".
3. **`csEntry` (807 → 1155):** a successful Run saves the counts in `csKeep`. Restore uses this copy.
4. **Text pages, one footer line each** (`csPageTest` 861, `csPageInterp` 907, `csPage2x2` 937): `TEXTOUT_P(csFoot, …, 12, 222, …)` → the page number at (282, 11), top right.
5. **`csResults` (945 → 1303):**
   - The soft-key strip; Menu opens `csResMenu`.
   - On page 1, a tap on a cell sets `csTapC`; a tap elsewhere turns the page as before.
   - Returns the next screen. The footer string is now just "3/6".
   - Arrows, Enter, Esc and the half-screen taps behave as in beta 1l.
6. **`csBars` (991 → 1370):**
   - The y-scale is frozen while `csYF > 0` and saved in `csYT`/`csYS`. `csBW` is recorded for the drag hit box.
   - A bar is clipped to the box (a frozen scale can be outgrown). With the scale not frozen, this never takes effect.
   - The readout moves from y 206 to 192.
   - The footer (y 222) becomes a verdict line at y 204: "χ² = 13.16, p = 0.0003: REJECT H₀" in red, or "…: keep H₀" in green, plus "drag bars" in grey when there is room. During a drag that would empty a row: "A row or column would add to 0: lift = refused".
7. **`csMosaic` (1072 → 1541):**
   - **Morph, via `csMT`:** with `csMT = 0` the tile height expression is beta 1l's, unchanged. With `csMT > 0`, heights are interpolated, colours fade through `csMFill`/`csMEdge`, there is no selection frame, and the tile label shows the count on its way to E.
   - **Bottom text:** the legend and readout move from 198/210 to 190/202, and the footer (224) is dropped. During the morph two caption lines replace them.
8. **`csPlotLoop` (1140 → 1763):**
   - **Plots:** handles the residual plot as `plWhich` 3.
   - **Strip:** the soft-key strip on every frame.
   - **Bars:** a press on an observed bar goes to `csBarDrag`; with no movement it selects the cell, as before. Up/Down change the selected count, and `csCheck` refuses a row or column at 0. Restore is slot 3.
   - **Mosaic:** Morph is slot 4, or the + key.
   - **Navigation:** Prev/Next go to the screen before or after. Returns the next screen.
9. **`csCurve` (1176-1249 → 1867-2120)** was split into four routines plus `csCurve` itself. Beta 1l's drawing arithmetic is unchanged; the cache now holds pixel rows.
   - `csCvFit`: the window and the cached pixel row per column, once per window.
   - `csCvDraw`: one frame from the cache. The readout moves from 204/216 to 192/204 and the footer (228) is dropped. The line's labels flip to its left near the right edge. Under the crit label is "← drag →", or the live α while dragging. An off-ladder α is worded "custom α = 0.037".
   - `csSnapA`, `csStepA`, `csOnLad`: the ladder.
   - `csCurve`: the loop.
   - The window stays fixed while the curve is open. It refits only when the line would leave the plot (crit > 0.97 × x-max) or after a Menu action.
10. **`csExamples` (1263 → 2419):**
    - New fifth item, "Simpson (examples 1 + 2)".
    - A loaded example saves `csKeep` and opens `csView(1)` instead of `csResults()`.
11. **`csHelp` (1314 → 2549):**
    - Page 2's footer reads "Any key = page 3".
    - New page 3, "Touch, soft keys and the new plots": 14 lines naming every new gesture, soft key and plot.
    - New page 4: `csDfPage`.
12. **`csInit` (1361 → 2622):**
    - **`csPB` = 174 (was 186).** The plot box is 12 px shorter, so every plot's text ends above the soft-key strip at y 218. This is the one change that moves all three device-tested plots.
    - The new state is initialised.
13. **Main menu (1393 → 2663):** 14 items. New are "Plot: adjusted residuals" and "Plot: Fisher exact (2 × 2)"; CHOOSE shows items 10-14 as A-E. Quit is item 14. Results and every plot open through `csView`. The index variable is tested, never the return value.
14. **Header:** "beta 2", a dated "What changed" paragraph, "WHAT IT DOES" items 4-6, and a "HOW THE SCREENS FIT TOGETHER" note. The tested-on line says beta 2 has not run.

### New file-level state (line 275)

| Variable | Holds |
|---|---|
| `csKeep` | the counts that Restore puts back |
| `csYF`, `csYS`, `csYT` | the bars plot's y-top and tick step: frozen during a drag, and those of the last frame |
| `csBW` | the width of one bar |
| `csMT` | how far the morph has gone |
| `csTapC` | the cell tapped on results page 1 |
| `csDgBad` | 1 while a drag holds a row or column at 0 |
| `csFW`, `csFLo`, `csFHi`, `csFSel`, `csFDL`, `csFDH` | the Fisher plot: probabilities, the range of a, the selected table, the range drawn |
| `csCvX`, `csCvY`, `csCvS`, `csCvDc`, `csCvP`, `csCvW` | the curve's window and its cached pixel rows |

All names were checked case-insensitively against the built-in list. The gate caught `dfC` (DFC) and `dfX` (DFX) in the first draft; they are now `dpC` and `dpX`.

### New routines (all tagged `cs`)

| Routine | What it does |
|---|---|
| `csDotH` | dotted horizontal line on G1 |
| `csCopy` | a fresh element-by-element copy of a list, so `csKeep` cannot alias `csO` |
| `csRecalc` | runs `csCompute` and keeps `csSel`, since `csCompute` ends by selecting cell 1 |
| `csCellAt` | the cell under a tap, using the entry grid's arithmetic |
| `csEStr` | "R1 C1:  E = R × C / N = …" with the real numbers |
| `csStrip` | `DRAWMENU` for each screen: `{"Prev","Next","Bars","Mosaic","Curve","Menu"}`. The current plot's own slot does its own job instead: Restore on the bars, Morph on the mosaic, Reset (α = 0.05) on the curve |
| `csPlotStep` | the ring results → bars → mosaic → curve → residuals → Fisher (2 × 2 only) → results |
| `csRestore` | puts back the saved counts |
| `csScaleN` | ×10 or ÷10, the refusals, then the "before / after" page (N, χ², p, V, the decision) with "V is the effect size; p depends on N." |
| `csResMenu` | the Menu soft key: Main menu / ×10 N / N / 10 / Restore; Cancel stays |
| `csFade`, `csMFill`, `csMEdge` | the morph's colour fade to the grey of the "all" bar |
| `csBarDrag` | the bar drag (details below) |
| `csMorph` | the independence morph (details below) |
| `csResBars` | the adjusted-residual chart: blue up, red down, solid beyond ±2, dotted magenta lines at ±2, a tap shows the cell's O, E and residual |
| `csCvFit`, `csCvDraw`, `csOnLad`, `csSnapA`, `csStepA`, `csCurve` | the interactive curve |
| `csFishW` | Fisher weights by csFisher's own ratios, normalised; returns 0 when there are more than 3,000 tables, csFisher's guard |
| `csFishDraw` | one bar per a: observed red, no-more-probable magenta, rest pale grey. A 3-px strip under the axis shows each bar's class even when it is too short to see. The corner panel shows the selected 2 × 2. The window drawn keeps every table at least 1/100000 as probable as the mode, plus the observed one |
| `csFishPlot` | the Fisher screen loop |
| `csView` | the screen dispatcher |
| `csSmBar` | one row of the Simpson page |
| `csSimpson` | the Simpson's paradox page |
| `csDfPage` | why df = (r − 1)(c − 1) |

**`csBarDrag`.** The press must move more than 8 px before it counts as a drag. After that the count comes from the finger's y on the frozen scale, rounded and clamped to 0 … the frozen top. `csRecalc` runs on every changed sample.

A sample that would make a row or column 0 is drawn but not computed (0/0), with a warning line. On lift:
1. The scale refits.
2. `csCheck` runs. If it refuses, its own MSGBOX explains, the count goes back and the table is recomputed.

Any key ends the drag, which is a way out if a touch reading ever sticks.

**`csMorph`.** Ten frames of about 150 ms, timed with a `TICKS` loop that also polls `GETKEY` and `MOUSE` so it can be interrupted. Any key or tap stops it at once. After a full run the H₀ picture is held until a key or tap.

**Simpson page data.** The page adds the four counts of the three-way table that examples 1 and 2 are the margins of: white victim 53/414 and 11/37, black victim 0/16 and 4/139 (Radelet & Pierce 1991 via Agresti). The verify script checks that they add up to both examples exactly. The joint shares and the 22.9 % and 0 % rates match a published vignette (CRAN asbio `simpson.pdf`).

## 2 · Gate (final run)

```
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check tally (NEW)  ---   1 W3
--- 2. ppl_check tally (ORIG) ---   1 W3          (the same beta-1l line, csPageTest's df line)
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11) ---   none
--- 3. lint_ppl ---   1962 checks, 8 problems: the same 8 as beta 1l, diffed line by line
    (STRING() with 4 args = a known false alarm; PIXON_P targets 'dvG'; the
     file-name / EXPORT-discipline noise)
--- 4. full parse (kit interpreter) ---   PARSE FAIL at the file-level LOCAL after the
    EXPORT list, the kit's limit, the same as beta 1l (the harness parser reads it, below)
--- 5. ---   2716 lines, 118787 bytes; no non-ASCII in code
fleet_names_v2 (all *.txt in out/, old versions of the same programs left out):
    no ChiTable name collides with any other program; 0 untagged, 0 built-in matches
```

## 3 · Harness runs (`ppl_run_v1.py`, the kit interpreter with SciPy built-ins)

| Run | What it checked |
|---|---|
| Example 2, tap R1 C1 on page 1 | "R1 C1:  E = 515 × 68 / 674 = 51.96" and the "unrelated" line at y 184 / 200; "1/6" in the corner |
| Bars soft key, drag R1 C1 from y 160 to 100 | count 64 → 97 → 178 → 300. E(R1 C1) 51.96 → 78.29 → 145.28 → 250.88. χ² 13.16 → 23.21 → 47.50 → 82.64; the scale stays 600. After lift `csKeep` is still {64, 451, 4, 155} (copy not aliased) |
| New 2 × 2 {5, 0, 3, 7}, drag R1 C1 to 0 | the verdict goes from REJECT (p = 0.0104) to keep (p = 0.1653 at O = 1), as the colour should. At 0 the line reads "A row or column would add to 0: lift = refused". On lift csCheck's message appears and the count returns to 5. Then Up gives 6 (χ² 7.47) and Restore gives 5 |
| Example 1 curve | drag 3.84 → 3.31 (custom α 0.069) → 2.41 (0.121) → 1.59 (0.207). On lift it snaps to 0.20 (crit 1.64). Left stays at 0.20; Right goes to 0.10. Dragging to 0.245 turns the verdict red, "Past crit (custom α = 0.245): REJECT H₀" (X² = 1.47 > 1.35). Reset gives 0.05; Right gives 0.02 |
| Morph frames t = 0, 0.5, 1 | at t = 0 the tiles are identical to beta 1l. At t = 1 every bar's tiles have exactly the "all" bar's edges (26-41, 45-174), with fill F0F0F0 and edge 5A5A5A; labels C1 52, C2 463, C1 16, C2 143 = the E's |
| Morph via soft key, stopped by a tap | `csMT` is back to 0 and the mosaic redraws |
| Residuals (example 2) | ±3.63 bars, scale ±4, the selected cell's readout |
| Fisher (example 2) | a = 64 observed, P < 0.0001; red + magenta = p 0.0001; a tap shows a = 47, P = 0.0387 "likelier than yours"; Right shows a = 48 |
| Menu → ×10 N | N 674 → 6740, χ² 13.16 → 131.57, p 0.0003 → < 0.0001, V 0.140 → 0.140; the Fisher plot redraws over a = 500-650 |
| Menu → N / 10, then N / 10 again | the first gives back 674. The second is refused ("a count would round to 0"; 4 → 0) |
| Help with no table, Simpson page, 3 × 2 example | all four help pages, then the df page ("free / forced / fixed"). Simpson: 11.0 / 7.9 / 12.4 / 2.5 / 11.3 / 22.9 / 0.0 / 2.8 %. A tap on R3 C2 of the 3 × 2 puts "R3 C2:  E = 945 × 1200 / 2757 = 411.32" in the title area |
| **Randomized stress run** | 400 sessions of 10-80 random keys, taps, strip taps and drags, with random menu answers. **0 runtime errors, 0 stalls, 0 harness warnings.** Frames drawn: csGrid 7058, csBars 2685, csMosaic 2210, csCvDraw 1440, csHelp 1152, csResBars 774, csFishDraw 701, csPageTest 573, csDfPage 384, csScaleN 114, csSimpson 56 |

## 4 · Formula checks (`verify_ChiTable.py`, SciPy 1.x and statsmodels): ALL OK

```
csFishW == hypergeom pmf on 306 tables            max |diff| = 1.1e-16
red + magenta sum == fisher_exact == csFisher     max |diff| = 6.7e-16
  example 2: a = 0..68 (69 tables), P(a = 64) = 4.48e-05, two-sided p = 0.000118
corner-panel tables keep the margins
x10: chi2 x 10 exactly and V unchanged, all four examples (ex 2: 13.16 -> 131.57, V 0.140)
N / 10 refused for example 2, allowed for example 3; x10 then /10 returns the counts
E = R x C / N == chi2_contingency expected, every cell (ex 1 R1 C1: 483 x 68 / 674 = 48.73)
alpha = 1 - CDF(crit) inverts ICDF; snap windows disjoint; snap cases; csAStr decimals
verdict: p < alpha <=> X2 > crit at 200 alphas
bar drag: finger on a bar top gives back its count (within one pixel), scales 8 .. 5000
morph: shares add to 1 every frame, heights == the O->E labels, t = 1 is E
Simpson: the three-way table adds to examples 1 and 2; printed %; the reversal holds
df page: free cells = (r-1)(c-1)
csAdj == statsmodels standardized_resids          max |diff| = 1.7e-14
```

## 5 · Device test checklist: from least to most risky

Stop at the first failure. Everything above it is known good.

1. **Paste and compile.** Run ChiTable. The main menu should have 14 items, items 10-14 lettered A-E, and Quit last (E). Quit at once: Home shows "ChiTable: no table".
2. **Old paths, unchanged code.** New table 2 × 2 → tap cells, Edit, Values, Clear, Run: exactly as beta 1j.
3. **Results pages** (Examples → Death penalty × victim's race):
   - **Page number:** "1/6" in the top-left corner of the table pages and at the top right of pages 3, 5 and 6.
   - **Soft keys:** Prev · Next · Bars · Mosaic · Curve · Menu along the bottom.
   - **Paging:** Left/Right, Enter and the half-screen taps work as before, and the last page stays put on Right.
   - **Bottom text:** page 3's last line (y 207) and the 3 × 2 example's totals row (to y 214) must both be fully visible above the strip.
4. **Tap a cell on page 1** (R1 C1): a magenta frame and "R1 C1:  E = 515 × 68 / 674 = 51.96" / "what it would hold if the variables were unrelated". Then load the 3 × 2 example and tap a cell: the two lines appear in place of the title. A tap outside the cells still turns the page.
5. **Help:** four pages. Page 3 is "Touch, soft keys and the new plots"; check that none of its 14 lines is clipped at the right. Page 4 is the df page, "free / forced / fixed" with no table, numbers with one.
6. **Examples → Simpson (examples 1 + 2):** the bars, the percentages listed under the harness runs, the four sentences, and a key or tap returns to the menu.
7. **Plots open from the main menu**, all now 12 px shorter:
   - Bars and mosaic: the readout lines sit above the strip.
   - Curve: "← drag →" under the crit label, and both readout lines above the strip.
   - Residuals: blue and red bars, dotted magenta ±2 lines.
   - Fisher: bars, the 3-px class strip under the axis, the orange corner panel.
   Esc and Enter return to the menu.
8. **Soft keys on plots:**
   - Next walks bars → mosaic → curve → residuals → Fisher → results; Prev goes back.
   - Bars, Mosaic and Curve jump to that plot.
   - Menu opens "Results menu", and Cancel stays on the plot.
   - Check that the label "Restore" fits its key; it is 7 characters, the longest label used.
9. **Menu → ×10 N** on example 2: the before/after page (6740, 131.57, p < 0.0001, V 0.140 twice). Then **N / 10** returns to 674; a second N / 10 is refused with a message. Restore also returns the original counts.
10. **Curve: the arrows.** Left/Right step α along .001 … .20; the line moves and the menu item reads "Set α (now 0.10)". Reset returns to 0.05.
11. **Tap a bar** in the residual and Fisher plots; Left/Right move the Fisher selection.
12. **Morph** (mosaic → Morph, or +): ten frames glide to the grey "all" shape, then hold until a key. Run it again and tap mid-way: it stops at once and the normal mosaic returns. On a G1, note whether ten frames feel smooth (each redraws about 15 tiles).
13. **Bars: Up/Down** change the selected count by a step (10 on example 2's scale). Press Down on a 2 × 2 whose other cell in that row is 0, so the row empties: csCheck's message appears and the count stays.
14. **Bars: drag a solid bar.**
    - The count follows the finger, the pale bars move and χ²/p update on the line above the strip. The scale stays put until you lift.
    - Drag example 1's R1 C1 up until the line turns red (p < 0.05).
    - On a G1, judge the lag: each sample runs csCompute, including the Fisher loop over about 70 tables.
    - Drag a bar to 0 in a row whose other count is 0: the line reads "…would add to 0: lift = refused", and lifting gives csCheck's message and restores the count.
    - Restore puts everything back.
15. **Curve: drag the red line** (press within 6 px of it):
    - α follows the finger, shown under "crit", and the verdict turns red as the line passes X².
    - Lift near 0.05: it snaps to 0.05. Lift elsewhere: "custom α = 0.037" appears, and the main menu says "(now 0.037)".
    - A tap inside the plot away from the line does nothing; a tap outside the plot returns to the menu.
16. **Home after Quit:** CS_X2 etc. hold the last table, including any dragged or scaled counts. K holds the last MAKELIST count, as before.

## 6 · Not confirmed / left as it was

- **The "More" soft-key convention** (Roger, 16 Oct 2026; BRIEF_TOUCH's last section) is **not used here, on purpose.**
  - Every screen's strip fits in six keys.
  - Every feature already has both a touch route and a key route: the bar drag has Up/Down, the line drag ←/→, the morph +, the Fisher and residual taps ←/→, and ×10 / N / 10 / Restore sit in the Menu list.
  - The convention says to apply it only where it helps. Adding a page would have moved labels students meet first.
  - `csStrip` carries a comment saying so. The help pages are unchanged on this point, since there is no "More" key for a student to learn.
  - If Roger wants ×10 N one tap away, the natural form is page 2 = {"x10 N", "N/10", "Restore", "", "Main", "More"}, with Menu becoming More. That is a small change in `csStrip` plus the four slot handlers.

- **Not run on hardware.** Nothing in beta 2 has been. The constructs it relies on are all the fleet's verified ones: `MOUSE` polling, the capped drain, `DRAWMENU` after the blit, `RGB()` (used by StudRange, SampDist, EpiStats and BayesTree on hardware), `TICKS`, `MAKELIST` with Home's `K`, and `CHISQUARE` / `CHISQUARE_CDF` / `CHISQUARE_ICDF`. The drag loops read `MOUSE` repeatedly while the finger is down; NormExplorer's device-run explorer does the same. A key always ends a drag.
- **Avoided glyphs.** `CHAR(177)` (±) and `÷` are not on the verified-glyph list, so the program writes "+/-2", "+2 and -2" and "N / 10".
- **Text widths** were checked with the gate's 6-px estimate and the harness's estimate, not on the screen. Beta 2's longest new lines are 50 characters of font 1, against 51 for beta 1j's longest device-seen line. Checklist items 3, 5 and 7 cover them.
- **G1 timing** for the bar drag (csCompute per sample) and the morph is unmeasured. If the drag lags on a G1, one option is a flag that skips the Fisher loop during the drag and runs the full csCompute on lift. That needs Roger's approval to touch csCompute.
- **Not done** (in the review, not in this brief): drag on an entry cell to nudge ±1, a ghost χ² curve for the other df, row-% stacked bars, live χ² in the entry grid.
- **`MAKELIST`** still uses Home's `K` (GfxProbe T19 pending).
