# StudRange beta 15f — layout only (28 Oct 2026)

Source: Overlap_Sweep_2026-10-28_v1.md (StudRange beta15e: 6 overlaps, 4 firm, in sr_PlotMode and sr_Yard).
No number, formula, key handling or logic changed; the `#PYTHON srq` block is byte-identical (checked line-anchored, 13146 bytes both).

## Rows moved

| Routine | Element | old | new |
|---|---|---|---|
| sr_PlotMode | alpha ladder labels `.10 .05 .025 .01 .005` (font 1) | y 39 | y 43 |
| sr_PlotMode | ladder tick lines, top end | y 49 | y 54 |
| sr_PlotMode | plot box top `py1` (drawing and touch handler read it) | 54 | 58 |
| sr_Yard | `HSD = … (the orange bar)` | (160, 30) | (8, 74) |

Why: the engine badge (sr_Badge at y 29, text at 31, ink to 41) sat under the ladder labels at 39; the labels now start at 43 (41 + 2 px clearance), their ticks run 54..57 and the plot frame starts at 58, so no label straddles the frame. In sr_Yard the HSD line shared the badge's row and ran to x 348; the band 72..102 between the two rows of means (48, 60) and the staggered mean labels (104..128) is empty, so it goes there.

## Overlap counts (tools/text_overlap_v1.py, --walk, 30 runs x 15 s as in the sweep)

| | beta15e | beta15f |
|---|---|---|
| overlaps (firm) | 6 (4) | 3 (0) |
| tight rows | 2 | 2 |
| frame straddles (firm) | 2 (0) | 2 (0) |
| overruns (firm) | 18 (0) | 17 (0) |

The three marginal overlaps left are same-row ladder labels `.025`/`.01` (22 px apart, estimate-sensitive) and the q-crit box text against `tap box: q to q crit`, both unchanged from beta15e.

Verify script (verify_StudRange_beta15e.py with NEW pointed at beta15f): failures 0, same numbers as the beta15e run (p = 0.00012 at q = 1.837 for k 4, df 5). Gate: ppl_gate_v1c PASS (the full-parse note is pre-existing, same spot in beta15e); case_scan clean.

## Device checklist
1. Plot mode: the five alpha ladder labels sit between the red/green engine badge and the plot's top edge, with their short ticks just below them.
2. Plot mode: drag the orange alpha handle on the right axis; it still tracks the finger over the (4 px shorter) plot.
3. HSD yardstick: `HSD = … (the orange bar)` appears on its own row under the two rows of means, fully on screen.
