# TrendTest beta 2: changes from beta 1b

16 October 2026. This is the touch and graphics version from the fleet review (Fleet_Review_2026-10-16_v1.md, §6, TrendTest entry). It is built on `TrendTest_beta1b.txt`, and every beta 1b fix is kept: `trTot`, `doTk`, `trPTop`, `trHiMx`, unnumbered menus, house footers, and taps limited to the plot box. **It has not been run on hardware.** The file has 1436 lines (beta 1b had 806).

Line references are `beta 1b → beta 2`.

## (a) Changes

1. **Header** (4, 19-42 → 4, 19-98). The banner reads "beta 2". A new "beta 2 (16 Oct 2026) - what changed" paragraph comes first, and the beta 1b and 1a paragraphs are kept below it. The licence, AI-assistance and firmware lines are unchanged ("NOT yet been run on hardware").
   - THE ARITHMETIC now also covers the band, the residual SE and midranks.
   - EXAMPLES lists all three data sets with their expected statistics, from `verify_TrendTest.py`.
   - SCREENS describes the three results pages, the plots and the soft keys.
2. **Drag a dot.** This is the new routine `trPlotTouch` (1124-1194), called from the view loop.
   - **Grabbing a dot.** On the proportions plot, a press within 10 px of a dot's centre grabs that dot. The centres are recorded in `trDX`/`trDY` while drawing, so the drawing and the hit test cannot disagree.
   - **Drag or tap.** Movement of more than 8 px makes the press a drag. A press that lifts without moving is a tap and selects the level.
   - **Setting the count.** Each MOUSE sample maps the finger's y through the **frozen** y-scale to p, then sets `trA(sel) := ROUND(p·n)`.
   - **Limits.** The count stays between 0 and n. It is also kept so that the table holds at least one case and one non-case overall; otherwise V = 0 and the program would divide by zero.
   - **Redraws.** A sample that changes the count runs `trCompute`, `trDrawProp(1)` and `trShow`. A finger resting still costs nothing.
   - **Freeze and refit.** `trFrz := 1` freezes the y-scale while the finger is down, and it is refitted on lift.
   - **Stuck readings.** A reading off the screen (x outside 0-319, or y outside 0-239) counts as a lift, so a phantom reading cannot hold the loop.
   - **Keyboard.** Up/Down do the same from the keys, moving the dot about 1/40 of the y-scale per press and never less than 1 case (`trView`).
3. **Originals and Restore.**
   - **Where the originals live.** The new file-level `trOX` and `trOA` hold the entered scores and cases. `trEnter`, `trExamples` and Restore copy them through `trCopy` (261-270), because the PC test bench aliases lists on `:=` (the Prime copies).
   - **What Restore does.** The Restore soft key (or `0`) puts back the cases and the as-entered scores.
   - **Edited flag.** `trEdit` marks a dragged table. While it is set, results page 1 shows "Counts changed by dragging; Restore = original" in red, and the Home summary ends "; counts edited".
4. **One view loop with soft keys.** `trView` (1208-1306) replaces `trResults` (416-486) and `trPlotLoop` (669-706).
   - **The views.** Results pages 1-3 and the two plots share one loop. `trDrawView` composes the current view, and `trShow` (363-367) blits it and then calls `DRAWMENU({"Prop","OR","Scores","Data","Restore","Menu"})`.
   - **Soft-key taps.** A tap with y ≥ 218 is slot `MIN(6, IP(x/53.4)+1)`.
   - **Hardware keys.** The keys stay as shortcuts:
     - `+` = Scores, `0` = Restore, `-` = the other plot, Esc = menu.
     - Results pages: Left/Right turn pages, and Enter turns to the next page (the menu after page 3).
     - Plots: Left/Right choose the level, Up/Down change its cases (plot 1), and Enter returns to the menu.
   - **Taps on a results page.** A tap on the left half goes back a page and a tap on the right half goes on (as in ChiTable).
   - **Data.** It reopens `trEnter`. When the level count matches, the dialogs open filled with the data on screen: entered scores, current cases and totals (536-544; beta 1b always started at 1,2,3 and zeros). Keys and touch are drained after the dialogs.
   - **Footers above the strip.** All footer text now sits above y 218. The plot box is 28..152 (was 30..186), the four footer lines are at y 170/182/194/206, and the results frames end at y 217.
5. **Scores key.** `trScM` cycles through 0 as entered, 1 equal steps 1,2,3..., and 2 midranks (`trSetX`, 399-419). The program recomputes after each step.
   - **Footer.** Plot 1's footer prints χ²trend with its p and the score set, and on the next line Pearson χ² and the departure statistic.
   - **What it shows.** Help page 1's warning becomes something students can see. On the snoring data, χ²trend goes 72.66 → 72.01 → 68.19 while Pearson stays at 72.78.
   - **Score labels.** `trXStr` (297-302) prints each score with 0, 1 or 2 decimals as needed. It replaces the single `trXDec` setting (338-342), so a midrank like 2357.5 and an integer like 2124 do not both get two decimals.
6. **95% confidence band** round the WLS line (`trDrawProp`, 897-910). It is shaded column by column in light magenta #FAEBFA: fit(x) ± 1.96·√(P(1−P)·(1/N + (x−x̄)²/Sxx)).
   - **Where it comes from.** This is the weighted regression of p_i on x_i with weights n_i/(P(1−P)), the null variance the trend statistic itself uses.
   - **Verified.** It matches statsmodels `WLS(p, X, weights=n).fit(cov_type='fixed scale', scale=P(1−P))` to 1e-10 on all three examples.
   - **The alternatives differ, and were not used.** The default statsmodels WLS (scale estimated from the residuals) gives a different band: 4.6× narrower for snoring and 4.2× wider for the U example. The binomial GLM with an identity link (variance at the fitted values) is also different.
   - **Why this form.** I used the fixed-scale form because it matches the statistic the program reports: (b/SE_b)² = N r² (Armitage) = N/(N−1)·X²trend (Mantel).
   - **New state.** `trCompute` now also sets `trSxx`, `trPQ` and the x-window `trXlo`/`trXhi`. Beta 1b computed the window separately in three routines.
7. **Dots coloured by their residual.** The residual is the dot's distance from the line drawn in that frame. A dot more than 1 SE above the line is blue, more than 1 SE below is red, and anything within 1 SE is grey, with SE_i = √(P(1−P)/n_i). The squared z-residuals add up to Pearson − Armitage, the departure statistic; this was verified.
   - The Wilson bar takes the dot's colour.
   - The selected level is now ringed in black, because red now means "below the line". The red readout became black.
   - The readout gives the residual: "L3: x = 4, 21/213 = 0.099, line 0.097 (+0.1 SE)".
   - The legend in the plot reads above / below / within 1 SE / WLS line, 95% band.
8. **The WLS line is one clipped LINE_P** (2 px thick) instead of 520 PIXON_P per frame (541-549). It is clipped analytically to the window 0..y-top. This keeps each drag frame to one 260-column band plus about 40 calls.
9. **Animated fit** (`trAnimate`, 1005-1022). It runs when the proportions plot is entered from the menu or from another view.
   - **The motion.** Over 15 frames the slope goes from 0 to trB, pivoting on (x̄, P), the point every weighted line passes through.
   - **The counter.** The footer shows "fitting: slope × 0.47, χ²trend = 16.0". The value is X²·f², the statistic for the slope being drawn.
   - **Skipping.** Any key or tap skips the rest. The band appears only on the fitted line.
   - **Changing scores.** Pressing Scores while on the plot does not re-animate.
10. **"fit" column on results page 1.** This is n_i·(a + b·x_i), the cases the line predicts at each level. A note line says the column sums to A. The page is re-spaced at 12 px: rows from y 60, tests at 146/158/170, the WLS line at 182, a "Scores: …" line at 194, and the page legend at 205.
11. **New results page 2, "Where the two statistics fall"** (`trChiPanel` 699-770, `trPageChi` 772-797). Two 140-px panels show χ²(1) with X²trend and χ²(k−2) with the departure statistic.
   - **Each panel.** The tail beyond the statistic is shaded (that area is the p-value). The 5% cut-off is a dotted red line, and the statistic is a solid line in its colour (magenta for trend, green for departure).
   - **Statistics far out.** A statistic more than 4 cut-offs out is marked at the right edge with "further →".
   - **Density cache.** Each density is cached per pixel column (one CHISQUARE call per column, shared by the tail and the curve).
   - **Below the panels.**
     - "Pearson χ² 72.78 = trend 72.66 + departure 0.12".
     - "1 df concentrates the evidence: its 5% cut-off is 3.84, against 7.81 for Pearson's 3 df."
     - For k = 2, a note that the two tests coincide.
   - **Page order.** The OR/formulas page is now page 3. Its "Home: TR_…" line moved there from page 1.
12. **Examples menu** (`trExamples`, 594-642). "Example: snoring & heart disease" becomes "Examples", a CHOOSE with three items:
    - **Snoring and heart disease** (unchanged).
    - **"Sleep hours: a U shape (made up)".** Hours 5-9; cases 38, 40, 36, 44, 44 of 160, 320, 480, 320, 160. Trend 1.105 (p = 0.293), departure 53.115 on 3 df (p < 0.0001).
    - **"Convictions, re-arrest (made up)".** Prior convictions 0/1/2/3+, with 3+ scored 3; re-arrested 72, 66, 51, 88 of 400, 240, 150, 200. Trend 47.719, departure 0.248 (p = 0.883).
    - **Labelling of made-up data.** Results page 1 shows "ILLUSTRATIVE (made-up counts)…" in red, both plot titles become "Made-up data: …" in red, and the header says the counts are invented.
    - **Second label line.** Every example now has a second label line (`trLbl2`): snoring's categories, the sleep hours, and "3+ scored 3".
13. **OR plot footer** (`trDrawOR`) has four lines: the readout (170), the Woolf/Haldane note (182), **"Log scale: OR 0.5 and 2 are equally far from 1."** (194), and the legend "⇆ or tap = level, Esc = menu" (206).
14. **Help is now three pages** (`trHelp`). They cover "1 df concentrates the evidence", the Scores key, the residual colours and SE, dragging and Restore, the band formula, why the axis is logarithmic, every soft key and hardware shortcut, and the animation skip. The "elsewhere" references are kept.
15. **`trCompute` no longer sets `trSel := 1`** (348), so a dragged dot stays selected. `trEnter` and `trExamples` set it instead.
16. **Main menu** (769-806 → 1394-1436). Item 5 is "Examples". Items 1-4 open `trView` at page 1, page 1, plot 1 and plot 2. The "no data" box names "one of the Examples". The Home summary appends "; scores midranks" or "; counts edited" when either applies.
17. **New file-level state**, at six names per line at most: `trOX trOA trScM trEdit trLbl2 trIllu`, `trSxx trPQ trXlo trXhi`, `trYhi trYStp trYDec trFrz trDX trDY`, and `trChi` (= CHAR(967)+CHAR(178), as in ChiTable). `trXDec` is gone.
18. **χ² glyph** in the results lines, the footers and the formulas page, instead of "X2". It is the ChiTable-verified `CHAR(967)+CHAR(178)`. The Home summary keeps "X2".

## Gate (check.sh, final file)

```
kit lint: 0 errors
ppl_check tally NEW: (none)      ORIG (beta 1b): (none)
hard errors (E2 E3 E6 E8 E10 E11) in NEW: none
lint_ppl: 1067 checks, 8 problems -- the same 8 as beta 1b: "no function named
  TrendTest_beta2", EXPORT discipline (3 lines), PIXON_P on dtG/dlG (2), and the known
  false "STRING() with 4 args" (MAX inside STRING, now line 1059, was 610)
full parse: PARSE FAIL at the file-level LOCAL after the EXPORT list (191), as beta 1b
  (109) -- the tool's limit.  With the LOCAL/EXPORT-variable lines masked: beta 2 PARSE OK
  (34 functions), beta 1b PARSE OK (21 functions).
fleet_names_v2 over the latest version of every program (25 files, incl. ChiTable_beta2,
  CentralLimit_beta2, NormExplorer_beta42, EpiStats_v1.5 ...): 787 routine names,
  0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.
```

## Verification (verify_TrendTest.py: SciPy and statsmodels, then the harness)

Part 2 runs the program in `ppl_run_v1` and compares `trCompute`'s globals with the Python reference. It checks X²trend and p, Pearson and p, the departure and p, the slope and intercept, Sxx, P(1−P), all Wilson limits, all ORs and their Woolf limits, and the scores in use. **Every value matches to 1e-6.**

| Run | X²trend | Pearson | departure | values compared |
|---|---|---|---|---|
| Snoring, scores as entered / 1,2,3 / midranks / back to entered (`+` ×3) | 72.6588 / 72.0083 / 68.1898 / 72.6588 | 72.7821 each time | 0.1232 / 0.7738 / 4.5923 / 0.1232 | 34 each, MATCH |
| Sleep U shape, same cycle | 1.1048 / 1.1048 / 1.0503 / 1.1048 | 54.2197 | 53.1149 / 53.1149 / 53.1694 / 53.1149 | 40 each, MATCH |
| Convictions, same cycle | 47.7191 / 47.7191 / 47.0216 / 47.7191 | 47.9674 | 0.2483 / 0.2483 / 0.9458 / 0.2483 | 34 each, MATCH |
| Snoring, level 3 dragged from y 91 to y 127 | 51.1921 (cases 21 → 9, as predicted from the finger's y) | 63.1993 | 12.0072 | MATCH |
| ... then the Restore soft key | 72.6588 | 72.7821 | 0.1232 | MATCH |
| Zero-cell table (0, 5, 10 of 20 each), Haldane flag | 13.1111 | 13.3333 | 0.2222 | MATCH |
| Two levels (12/100, 30/100) | 9.7161 | 9.7649 | (k-2 = 0) | MATCH |

Python-only cross-checks: X²trend = (N−1)r² over all N individuals; Pearson = `scipy.stats.chi2_contingency`; Σ expected = A; Σz² = Pearson − Armitage. The band agrees with statsmodels WLS with the scale fixed at P(1−P) to 1e-10.

Behaviour in the harness (`ppl_run_v1`, scripted keys, taps and drags):

- **Animation.** 15 frames run on entering plot 1, from "fitting: slope × 0.00, χ²trend = 0.00" to "× 0.93, χ²trend = 63.29".
- **Freeze and refit.** Level 3 was dragged up past the top. The y-scale stayed at 0.20 for all 20 frames while the finger was down, with the count held at ROUND(0.20·213) = 42, then refitted to 0.3 on lift.
- **Keys.** The script on the convictions data was Right, Up×3, Down, `+`, `-`, `0`, Enter. The level moved, the counts changed, the scores cycled, the view switched to the OR plot, Restore brought the original counts back, and Enter returned to the menu.
- **Data soft key.** It opened the three dialogs prefilled with the U example's data. Accepting them reset the score set to "as entered".
- **Soft-key strip.** It is drawn after every frame. No text is drawn at y > 206 on any results page or plot.
- **No overlapping text** was found by width estimate, after moving page 1's score column (36 → 42) and cases column (76 → 80).
- **Stale-key mode** (each dialog's OK left in the buffer): no skipped pages for any example, results pages 1-3 and help pages 1-3.
- **Page 2, U example.** The departure panel's statistic of 53.11 is past the 40 maximum and shows "further →". The cut-offs read 3.84 against 9.49 for Pearson's 4 df.
- **k = 2.** Page 2 shows the "needs 3 or more levels" note and the line saying the two tests ask the same question.

## (b) DEVICE TEST CHECKLIST (least to most risky)

1. Paste into the Connectivity Kit and Check. There should be no syntax error. The new names are `trCopy trXStr trScName trShow trSetX trFitY trPyOf trPage1 trChiPanel trPageChi trPage3 trAnimate trPlotTouch trDrawView trView trExamples`.
2. Run `TrendTest()`. The menu has seven items, item 5 is "Examples". Help shows three pages, each line inside the blue frame. Check that ⇆ and ⇅ draw as single glyphs on page 3.
3. Results before loading data: the box names "one of the Examples".
4. Examples → Snoring.
   - **Page 1.** Check that the score, cases/n, fit, p and CI columns do not touch (fit 23.3, 36.3, 20.7, 29.7) and that the χ² glyph renders. The "1/3 …" legend at y 205 must sit fully above the soft-key strip, and the orange frame must end at y 217.
5. Soft-key strip on the results pages. It should show Prop | OR | Scores | Data | Restore | Menu, redrawn after every page turn.
   - Left/Right and taps on the left/right half turn pages 1 ↔ 2 ↔ 3.
   - Enter on page 3 returns to the menu.
6. **Page 2 (the curves).**
   - **Left panel.** χ²(1) with "further →" at the right edge (72.66 is off the scale).
   - **Right panel.** χ²(2), with almost the whole curve shaded beyond 0.12 and a dotted red line labelled "5%".
   - **Text below.** Read the two sentences below the panels.
   - **Timing.** Note how long the page takes to draw (280 CHISQUARE calls).
7. **Scores soft key (or `+`)** on page 1. The trend line should read 72.659 → 72.008 → 68.190 → 72.659 while Pearson stays at 72.782. On midranks the score column shows 690, 1698.5, 2124, 2357.5.
8. **OR soft key.** Plot 2 has four footer lines at 170/182/194/206, including "Log scale: OR 0.5 and 2 are equally far from 1." Left/Right and taps select levels, and `-` switches plots.
9. **Prop soft key (the animation).** The line swings from flat to fitted in about 15 frames, and the footer counts "fitting: … χ²trend" up. Time it on the G2 and on the G1. Press a key mid-way: it should jump to the fitted frame, and that key should do nothing else.
10. **Plot 1, static.**
    - The pale magenta band is narrowest near x̄ (about 1.4) and wider at the ends.
    - Dots are grey for snoring (all within 1 SE), with a black ring on the selected level.
    - The footer has four lines with nothing under the strip, and the legend at the top of the plot box reads.
    - Then load the U example. Dots 1 and 5 should be blue, dot 3 red, and dots 2 and 4 grey.
11. **Up/Down** on plot 1 change the selected level's cases. Pearson and departure should change in the footer, and the y-scale refits after each press.
12. **The drag.**
    - **Grab and drag down.** Put a finger on level 3's dot and drag it slowly down. The count should change smoothly, the line tilt and the departure rise, while the y-axis labels stay fixed during the drag.
    - **Drag up.** Drag a dot up past the top. It stops at the top (0.20), then on lift the scale refits.
    - **Tap without moving.** A tap on a dot without moving only selects it.
    - **Frame rate.** Watch the frame rate on the G1. If it lags, the band (260 LINE_P and 260 `^0.5` per frame) is the first thing to thin.
13. **Restore** (soft key or `0`) brings back 24/35/21/30 and the scores as entered. Results page 1 loses the red "Counts changed by dragging" line.
14. **Data soft key.** The three dialogs open filled with the current data. Cancel leaves everything unchanged. A table with every case dragged to one level is still refused by the drag limits, so V never reaches 0.
15. **Quit after a drag.** Home shows "…; counts edited". Note Home's K, which MAKELIST still writes.

## (c) Not confirmed / left as is

- **Drag frame rate on the G1 is unknown.** Each frame draws the 260-column band, about 87 PIXON_P for the dotted overall line, and about 40 text and line calls. NormExplorer's device-tested drag is similar in cost, but the G1 is the slower machine. Redraws happen only when the count changes.
- **Whether a moving finger reports through `MOUSE` as continuous samples** is the same idiom NormExplorer's explorer drag uses on hardware. The press-vs-drag threshold (8 px) and grab radius (10 px) are untested on the device.
- **The DRAWMENU strip is repainted after every drag frame.** If the strip flickers during a drag, the fix is to blit only rows 0-217 of G1. That is not done, because the verified idiom is the full blit followed by DRAWMENU.
- **MAKELIST still uses Home's K** in `trEnter` (pending GfxProbe T19), as in beta 1b.
- **lint_ppl's "STRING() with 4 args" at 1059** is the known false positive (MAX inside STRING), unchanged from beta 1a/1b.
- **The harness cannot render.** Text widths are estimates (5.5 px/char for font 1), so layout tightness needs the device. The tightest spots are page 1's columns (cases/n at 80-130, fit at 134), the plot-1 readout (up to about 49 characters in 310 px), and the "1 df concentrates…" line (46 characters).
- **The U-shaped and convictions examples use made-up counts.** They are labelled so in the CHOOSE item, results page 1, both plot titles and the header.
