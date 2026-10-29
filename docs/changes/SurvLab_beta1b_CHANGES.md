# SurvLab beta 1b -- changes from beta 1a (28 Oct 2026)

**Layout only.** No number, formula, key handling or logic changed; verify_SurvLab_beta1b.py (the beta 1a
script with the file name, one hard-coded at-risk row y, and the old-version path updated) passes 5619 checks,
0 failures, the same numbers as beta 1a.  Gate: PASS.  Pure ASCII, LF.

## Rows moved (routine: old y -> new y)

| Routine | What | Old | New |
|---|---|---|---|
| sv_Grid | bottom y tick label (every box) | tick - 5 | min(tick - 5, box bottom - 10) when the labelled ticks are >= 17 px apart; else unchanged |
| sv_Grid | y tick labels closer than 12 px (KM zoomed with y from 0.0; test page 3) | every tick | every 2nd (3rd ...) tick labelled; grid lines and tick marks unchanged |
| sv_XLab | x label thinning rule | 6 px/char + 6 | 7 px/char + 6 (no change for the shipped data) |
| sv_KMBase | at-risk rows | 160, 171 | 160, 172 |
| sv_KMFrame | readout rows | 183, 195 | 184, 196 |
| sv_KMFrame | footer / info row | 207 | 208 |
| sv_LPlot | "q = P(event in the interval ...)" caption | 124 | 128 |
| sv_LPlot | q-max label (left of the bar panel) | 134 | 140 |
| sv_QDraw | "Median: first time S(t) < ..." caption | 118 | 119 |
| sv_QDraw | the 2-px gap before the red "n.r." block | +2 | removed (rows 11 px apart from 119: 130/141/152/163/174/185, then 196, 207) |
| sv_TPage1 | "solid O, pale E" | 93 | 94 |
| sv_TPage2 | "Shaded tail = ..." / H0 line / "No test" line | 160 / 172 / 160 | 162 / 174 / 162 |
| sv_TPage3 | "weight: G-B ..." caption | 101 | 102 |
| sv_TPage3 | the two red rule-of-thumb lines | 178, 190 | 179, 191 |

## Overlap counts (tools/text_overlap_v1.py --run the verify script)

| | Overlaps (firm) | Tight rows | Frame straddles (firm) | Overruns |
|---|---|---|---|---|
| beta 1a | 35 (31) | 89 | 3 (3) | 0 |
| beta 1b | 2 (0) | 25 | 3 (3) | 0 |

What remains (build/SurvLab/overlap_SurvLab_beta1b.txt): the 25 tight rows are the quantile page's 11-px
pitch (nine rows between the x tick labels at 108 and the footer at 207 with a 104-px plot box: no room for
12) plus a few 11-px rows elsewhere; the 2 marginal overlaps are the right-edge-clamped x label `1000000` on
stress data (times to 1e6); the 3 "straddles" are the red `t = ...` cursor label at the top of the KM plot
crossing the top edge of the CI band FILL on a 5-point stress data set (the tool counts any RECT_P of at
least 120 x 80 px as a frame) -- the label is inside the plot box, so nothing to fix.

## Device checklist
1. Kaplan-Meier page (Rossi, aid vs no aid): the `0.0` y label sits above the `at risk` header; at-risk rows, readouts and footer evenly spaced; Zoom on: y labels 0.0, 0.2, ... only when the ticks are dense.
2. Quantile page (Median) and the life-table Plot page: the caption rows clear the x tick labels; the q label sits beside the bar panel.
3. Test pages 2/3 and 3/3: the caption under each box clears its x tick labels; page 3's y labels are not on top of each other.
