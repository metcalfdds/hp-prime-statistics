# SeizureLab beta 1b -- changes from beta 1a (28 Oct 2026)

**Layout only.** No number, formula, key handling or logic changed; verify_SeizureLab_beta1b.py (the beta
1a script with the file name, the table row pitch and the version-specific Part G/C expectations updated:
it now diffs beta 1b against beta 1a and expects exactly the nine drawing routines below to differ) passes
with 0 failures and the same numbers.  The check count is 17977 against beta 1a's 17991 because B11 checks
every text on every page and the thinned x labels are fewer texts.  Gate: PASS.  Pure ASCII, LF.  The
header's file map was rebuilt for the new line numbers.

## Rows moved (routine: old y -> new y)

| Routine | What | Old | New |
|---|---|---|---|
| sz_YAxis | bottom y tick label (every box) | tick - 5 | min(tick - 5, box bottom - 10): `0.00` no longer meets the x label `0` in the corner of the binomial plot |
| sz_XAxis | x tick labels | every tick; the last clamped to the screen edge | every k-th tick when the labels would touch (7 px per character + 4), and a last label pushed onto the one before is left out (`1250000` `1260000` on stress weights) |
| sz_HypDraw | grey k labels under the bars | left out within 18 px of the red observed label | left out within 7 px per character + 4 of it (`5668` `5669`) |
| sz_TabPlot | plot box bottom | 170 (x labels 173 under the "0.90: magenta = hyper ..." row at 180) | 164 (x labels 167; the two legend rows 180 and 192 unchanged) |
| sz_TabDraw | table rows / rule / notes | 47 + 11 per row (to 124); rule 134; notes 137, 149, 161, 173 | 47 + 12 per row (to 131); rule 141; notes 144, 156, 168, 180 |
| sz_OCDraw | the red `p0` label at the vertical line | box top + 12 (1 px under the "Worst false claim" row) | box top + 13 |
| sz_BayDraw | the red `p0` label | box top + 2, beside the "grey = prior, magenta = posterior" row | box top + 13, under it |
| sz_WtDraw | the red `>= ->` label of the lower box | box top - 8 (1 px under the upper box's x labels) | box top - 7 |
| sz_Open | "N = ...: the red units ..." and the four disclaimer rows | 145; 158, 169, 180, 191 | 144; 156, 168, 180, 192 |

The sz_TabPlot change moves a frame edge by 6 px (the only way to fit the x labels and two legend rows
above the disclaimer line without dropping text); the plotted values are unchanged.

## Overlap counts (tools/text_overlap_v1.py on the verify script)

| | Overlaps (firm) | Tight rows | Frame straddles (firm) | Overruns |
|---|---|---|---|---|
| beta 1a | 11 (7) | 47 | 0 (0) | 0 |
| beta 1b | 0 (0) | 0 | 0 (0) | 0 |

Nothing remains (build/SeizureLab/overlap_SeizureLab_beta1b.txt; the run is recorded in-process because
this script's 3400 screens make the tool's JSON 690 MB).

## Device checklist
1. Tables page and its Plot: the eight rows and the three green notes are evenly spaced; on the plot the x labels (10 ... 1000, infinity) sit between the box and the black "0.90: ..." legend row.
2. Binomial page: `0.00` at the bottom of the y axis clears the `0` under it; hypergeometric page with a large N (e.g. 10000, c = 0.9999): no grey k label touches the red one.
3. OC curve and Bayes pages: the red `p0` label sits just under the caption row inside the box; weight page (typed summary with weights near 1.25 kg): the lower box's x labels do not run into each other.
