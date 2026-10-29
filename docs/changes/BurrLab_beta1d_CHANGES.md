# BurrLab beta 1d — changes from beta 1c (29 Oct 2026): the fast Explore redraw

Built from `parts/` (beta 1c's parts in `parts_beta1c/`); `BurrLab_beta1c.txt` untouched (md5
9571b7293751). Gate PASS vs beta 1c (`gate_BurrLab_beta1d_output.txt`); fleet_names 0/0/0;
case_scan clean over 33 files; `verify_BurrLab_beta1d.py` 3,165 checks, 0 failures (beta 1c's
plus Part H). Harness only. Everything outside the drawing is beta 1c's (same engine, fits, data).

Why: Roger, G2 (and G1): about 2 s per arrow press on Explore, and no faster on the G2 than the
G1 — so the time is in drawing calls / a pause, not arithmetic.

## Measured (PC harness, statements executed and drawing primitives per redraw)

| Page, event | beta 1c statements | primitives | beta 1d statements | primitives |
| --- | --- | --- | --- | --- |
| Explore, C/K/S arrow press | 9,497 | 561 (410 LINE_P, 120 PIXON_P, 23 TEXTOUT_P, 5 RECT_P, DIMGROB, BLIT) | 3,464 | 146 (121 LINE_P, 16 TEXTOUT_P, 3 RECT_P, 1 FILLPOLY_P, 2 DIMGROB, 3 BLIT) |
| Explore, x₀ move (+/−, tap, drag) | 2,241 | 556 | 474 | 16 (8 TEXTOUT_P, 3 RECT_P, 1 FILLPOLY_P, 1 LINE_P, 1 DIMGROB, 2 BLIT) |
| Explore, CDF view, parameter change | 9,482 | ~560 | 3,661 | ~150 |
| Family tree, C/K change | 5,077 | 194 (169 LINE_P) | 2,053 | ~110 (87 LINE_P) |
| How rare, x move | 11,507 | 417 (399 LINE_P) | 3,455 | 215 (199 LINE_P, 1 FILLPOLY_P) |
| Simulation, full frame (100 points) | 1,276 | | unchanged | |

Statements per arrow press 2.7× fewer, primitives 3.8× fewer (35× fewer on an x₀ move). The
curve pixels are IDENTICAL to beta 1c's (Part H: 12 shapes incl. C < 1, C = 30, the BJS and
Danish fits, both views; column by column from the LINE_P log); the y scale and the cached
pdf/CDF values equal to 1E-9; the page texts equal apart from the new timing readout.

## What changed

1. **Three layers** (`bu_ExFrame` → G3, `bu_ExBase` → G4, `bu_DrawExp` → G1): the frame (page,
   title band, plot box, grid, tick labels) is rebuilt only when the window changes (`buFrX`);
   the parameter layer (curve, markers, labels, cap note, short moment case, status rows B, C)
   only when C, K, S or the view change (`buBase`); every redraw makes a fresh G1 (DIMGROB_P,
   the house shape), blits G4 into it and adds the x₀ layer: the tail as ONE translucent
   `FILLPOLY_P` (alpha 128, its edge at every 2nd column under the curve), the x₀ line and dot,
   the four title pieces, status row A, the footer and the timing readout. No RECT_P clears of
   blitted regions; no `PIXON_P` at all (the dotted markers are thin solid `LINE_P` verticals).
2. **`bu_Curve`**: the curve as a run-merged polyline — a run of columns at the same pixel row
   is one horizontal `LINE_P`, a change of row one connecting segment: the same pixels as a
   segment per column, about a third of the calls (121 vs 410 at C = 2, K = 1.5).
3. **`bu_Cache`** in one pass per column: ln x = ln k + ln dx (ln k cached once in `buLnK`),
   ln z = C(ln x − ln S), ln(1 + z) (= ln z past 30, as bu_LnPdf/bu_LnSF), pdf = EXP(ln CK − ln x +
   ln z − (K + 1) ln(1 + z)); the CDF = 1 − EXP(−K ln(1 + z)) only in CDF view; the y scale as
   before (columns 4 on); then mode, median, mean, SD cached once per change (`buMd` …).
   `bu_DrawFam` and `bu_DrawRare` draw from the same cache (Rare computed the pdf three times
   per column before).
4. **Timing readout** (grey, inside the frame at the right, row PB−41): "c 12 d 180 w 0 ms" —
   c = window + cache + G4 layer, d = the x₀ layer and the blits, w = from the key event to this
   redraw (all TICKS). **No fixed pause** was found on the arrow path: the key drain is
   `UNTIL k == −1` (returns at once), `bu_Drain` (capped 1 s) runs only after a touch, no WAIT;
   Part H asserts the loop text has no WAIT and no TICKS-capped loop.
5. The stride machinery (`buStr`, `bu_ColC`) is in place but set to 1: a 2-column stride cut
   statements to 2,560 but moved the curve by up to 9 px at steep parts (measured), so the
   pixel-identical polyline was chosen instead.
