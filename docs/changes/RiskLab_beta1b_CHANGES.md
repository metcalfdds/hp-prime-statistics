# RiskLab beta 1b -- changes from beta 1a (28 Oct 2026)

**Layout only.** No number, formula, key handling or logic changed; verify_RiskLab_beta1b.py (the beta 1a
script with the file name and the old-version path updated) passes 611 checks, 0 failures, the same numbers
as beta 1a.  Gate: PASS.  Pure ASCII, LF.

## Rows moved (routine: old y -> new y)

| Routine | What | Old | New |
|---|---|---|---|
| rl_Grid | y tick labels (every box) | tick - 5 | clamped to [box top + 2, box bottom - 10]: the `1.0` label no longer sits on the cut-off line above the ROC box or on the group names above the fairness box; the `0.0` label no longer meets the x labels in the corner |
| rl_Grid | last x tick label | centred on the tick | at most 4 px past the box's right edge (the ROC `1.0` was touching the "flagged high" panel row) |
| rl_CalDraw | Hosmer-Lemeshow line / groups line / Cochran note | 174 / 185 / 196 | 176 / 187 / 197 |
| rl_FairTab | the "Differences" block | 160, 172, 186, 198 | 157, 169, 181, 193 (the last line was on the footer at 205) |
| rl_FairCal | "decile score k:" caption and the two group lines | 168, 180, 192 | 171, 182, 193 (the caption was on the x tick labels at 159) |
| rl_FairErr | bar value label | bar top - 11 | the same, but a bar whose label would rise above 44 (onto the group names) gets it just inside the bar's top |
| rl_FairErr | FPR/PPV explanation lines | 180, 192 | 181, 193 |
| rl_Open | the four "Loaded: ..." lines | 75, 86, 97, 108 | 73, 85, 97, 109 |
| rl_Open | version line | beta 1a, 26 Oct 2026 | beta 1b, 28 Oct 2026 |

## Overlap counts (tools/text_overlap_v1.py --run the verify script)

| | Overlaps (firm) | Tight rows | Frame straddles (firm) | Overruns |
|---|---|---|---|---|
| beta 1a | 19 (18) | 13 | 0 (0) | 0 |
| beta 1b | 0 (0) | 18 | 0 (0) | 0 |

What remains (build/RiskLab/overlap_RiskLab_beta1b.txt): tight rows only -- 11-px (one 10-px) pitch under
the calibration box, where four rows share the 42 px between the x tick labels (165) and the footer (207),
the three 11-px rows under the fairness calibration box, and the ROC's `0.0` corner label 1 px short of
clearance from the AUC row.  The count rose from 13 because rows that overlapped are now merely tight.

## Device checklist
1. ROC page: `1.0` sits just inside the top-left of the box, under the red cut-off line; `0.0` clears the x labels and the AUC row.
2. Calibration page (COMPAS): the Hosmer-Lemeshow, groups and (with Rossi) Cochran lines are readable, none on the x labels.
3. Fairness pages 1-3: the Differences block clears the footer; the "decile score k:" caption clears the x labels; a full-height error bar carries its value inside the bar; `1.00` on the y axis is below the group names.
