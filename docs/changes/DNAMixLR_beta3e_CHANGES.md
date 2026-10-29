# DNAMixLR beta 3e — layout only (28 Oct 2026)

Source: Overlap_Sweep_2026-10-28_v1.md (DNAMixLR beta3d: 2 overlaps, 1 firm, theta plot).
No number, formula, key handling or logic changed; the code stays pure ASCII (glyphs built with CHAR()).

## Rows moved

| Routine | Element | old | new |
|---|---|---|---|
| dmInit (the plot box constants; dmThStatic draws the frame and labels, dmThFrame the readout) | theta plot top `dmP2T` | 34 | 37 |

Effect: the top y-axis label is drawn at `dmP2T - 5`, so it moves from y 29 to y 32 and clears the theta readout row at y 20 (font 1, ink to 30, + 2 px). The "up to θ 0.25" note (`dmP2T + 12`) and the green finger line move with the frame; the touch handler reads the same constant. The plot is 3 px shorter (129 instead of 132 px).

## Overlap counts (tools/text_overlap_v1.py)

| Driver | beta3d | beta3e |
|---|---|---|
| --walk (80 runs): overlaps (firm) / tight / straddles (firm) / overruns (firm) | 2 (1) / 63 / 3 (0) / 2 (0) | 1 (0) / 63 / 3 (0) / 2 (0) |
| --run verify script: overlaps (firm) / tight / straddles (firm) / overruns (firm) | 5 (2) / 170 / 4 (0) / 1 (0) | 3 (0) / 170 / 4 (0) / 1 (0) |

The marginal overlap left (`excluded (LR = 0)` beside `dropped`, same row of the results table) is unchanged. The 63 / 170 tight rows are the program's 11 px font-1 pitch (cosmetic, as the sweep notes for AnovaLab and SurvLab).

Verify script (verify_DNAMixLR_beta3c.py with PROG pointed at beta3e): 167 PASS, 21 failures — the identical 21 fail on beta3d, because the beta3c script looks for the spelled-out "theta" that beta3d replaced with CHAR(952). Gate: ppl_gate_v1c PASS; case_scan clean.

## Device checklist
1. Theta plot: the top y-axis label sits below the `θ 0.0100  log10 LR …  LR …` readout row with a visible gap.
2. Drag across the theta plot: the green line and dot follow the finger; the readout updates.
3. The "up to θ 0.25" note (when shown) still sits inside the frame at its top right.
