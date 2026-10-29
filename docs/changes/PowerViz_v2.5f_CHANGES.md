# PowerViz v2.5f — layout only (28 Oct 2026)

Source: Overlap_Sweep_2026-10-28_v1.md (PowerViz v2.5e: 4 overlaps, 1 firm, in pv_PCDraw).
No number, formula, key handling or logic changed.

## Rows moved

| Routine | Element | old | new |
|---|---|---|---|
| file-level LOCALs (used by pv_PCDraw and the curve pages' touch handler) | power-curve plot top `PCT` | 30 | 35 |

Effect: the y-axis labels are drawn at `ticky - 4`, so the top one (`1.0`) moves from y 26 to y 31 and clears the caption row at y 19 (font 1, ink to 29, + 2 px). The grid, the 0.80 reference line, the n80 marker and the finger-to-n map all read PCT, so they move together; the plot is 5 px shorter (160 instead of 165 px).

## Overlap counts (tools/text_overlap_v1.py)

| Driver | v2.5e | v2.5f |
|---|---|---|
| --walk (10 runs): overlaps (firm) / tight / straddles (firm) / overruns (firm) | 4 (1) / 21 / 0 (0) / 5 (0) | 3 (0) / 21 / 0 (0) / 5 (0) |
| --run verify script: overlaps (firm) / tight / straddles (firm) / overruns (firm) | 13 (6) / 101 / 0 (0) / 30 (0) | 12 (5) / 101 / 0 (0) / 30 (0) |

The 5 firm overlaps left under the verify script are the `H₀` / `H₁` labels at the two curve means when the script sets μ₁ a few pixels from μ₀ (labels placed by the data, present in v2.5e; not a row-spacing matter). The 3 marginal walk overlaps (`d = 0.33, small` beside the big power figure; the SE₀ line beside `n₈₀ = …` on the footer row) are unchanged.

Verify script (verify_PowerViz_v2.5d.py with PROG pointed at v2.5f): 157 PASS, 17 FAIL, against 160 / 14 on v2.5e. The 14 shared failures are the v2.5d script expecting v2.5d's spelled-out text (v2.5e's glyph change); the 3 extra are its R5/U5 diff checks ("outside those routines only comments differ", "no new LOCAL line"), tripped by the one changed code line (PCT). Gate: ppl_gate_v1c PASS (the full-parse note is pre-existing); case_scan clean.

## Device checklist
1. Power vs sample size: the `1.0` label sits clear under the grey caption `… α = 0.050, 2-sided`; `0.0` still sits at the axis foot.
2. Drag along the curve: the n readout follows the finger over the slightly shorter plot.
3. Power vs effect size: same check; the 0.80 dotted line and its label are inside the plot.
