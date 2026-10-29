# SampDist v2.3d — layout only (28 Oct 2026)

Source of the finding: Overlap_Sweep_2026-10-28_v1.md (SampDist v2.3c, 7 overlaps, 6 firm, all in sd_drawCmp screen 9).
No number, formula, key handling or logic changed; only y positions in sd_drawCmp and the header block.

## Rows moved (sd_drawCmp, Compare sample sizes)

| Element | old y | new y |
|---|---|---|
| summary panel RECT_P (G2) | 182..220 | 188..222 |
| `n = n1: σx̄ = …` (red) and `n = n3: …` (green) | 186 | 192 |
| `n = n2: …` (blue) and `4× n halves σx̄` | 197 | 203 |
| `touch the plot: P(x̄ < x) for each n` | 208 | 214 |
| cursor readout clear RECT_P (G1) | 207..218 | 213..224 |
| `P(x̄ < x):` and the three probabilities | 208 | 214 |

The x-axis tick labels sit at BOT+5 = 177 (font 1, ink to 187) and are untouched; the panel's first row is now 192 (187 + 2 px clearance = 189 ≤ 192). The footer at 226 keeps 12 px from the 214 row.

## Overlap counts (tools/text_overlap_v1.py)

| Driver | v2.3c | v2.3d |
|---|---|---|
| --walk (80 runs): overlaps (firm) / tight / straddles (firm) / overruns (firm) | 7 (6) / 30 / 6 (0) / 6 (0) | 0 (0) / 30 / 6 (0) / 6 (0) |
| --run verify script: overlaps (firm) | 25 (10) | 20 (6) |

The 6 firm overlaps left under the verify script are same-row x-tick labels in sd_compose (y 154) under the script's stress parameters (σ = 0.000045, μ = 1e9: `-0.00020` beside `-0.00015`, `800000000` beside `1000000000`); they are in v2.3c too, were not in the sweep (the walk's defaults never produce them) and would need a number-format change, which is out of scope here.

Verify script (verify_SampDist_v2.3b.py with NEW pointed at v2.3d): 345 checks, 3 failures — J5 and J6, the v2.3b-specific "only S1/S2 changed" diff and version-string checks; the same 3 fail on v2.3c. Gate: ppl_gate_v1c PASS; case_scan clean.

## Device checklist
1. Menu 3 (Compare sample sizes), let the animation finish: the tick labels under the axis must clear the orange panel's top edge and its first row.
2. Drag across the plot: the `P(x̄ < x)` readout and its three values appear on the panel's third row, above the blue footer, with no clipping.
3. Tap a curve: the picked-curve label at the top left and the panel rows are unchanged in content.
