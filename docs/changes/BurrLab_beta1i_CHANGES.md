# BurrLab beta 1i (29 Oct 2026)

Two changes from beta 1h, both asked for by Roger after running beta 1h on the G1 and G2 ("the redraw is better now, still slow on both G1 and G2, but manageable"; "instead of a progress bar maybe something like a flashing icon or something to at least let the user know the calculation is doing something"). No formula and no number on any page changed.

## 1. Instant feedback: the new value at once, and an hourglass

- **Explore.** When a key press or a drag needs a recompute (C, K, S, the view or the window changed), the title row is redrawn straight to the screen with the NEW value, and a small yellow hourglass appears at the top right (x 302-317). Then the page is recomputed, and the finished frame replaces both. An x₀ step needs no recompute and shows no hourglass. Nothing is drawn early on the first entry or right after a menu or help page, so the hourglass never lands on top of a menu (`buOnPg` says which page is on the screen).
- **Family and Rare.** The same: on Family the new title ("Family: C = 2.10, ...") and the hourglass at once; on Rare the hourglass when the window has to be refilled.
- **Fits blink.** Through a fit the hourglass blinks at the top right of the progress screen, on or off every 0.4 s or so. `bu_Blink` costs one `TICKS` reading per call unless 0.4 s have passed; it is called from the likelihood loops (`bu_ProfT`, `bu_GLL`, the Lomax objective), the Weibull rival's 42-pass bisection, every 50th term of the A-D sum and `bu_Prog`. Cost: +0.85 % statements on the Danish 300 PPL fit, +2.7 % on BJS (its evaluations are short); the fitted C, K, S and the number of evaluations are identical to beta 1h.
- **MicroPython fits.** PPL cannot draw while `PYTHON()` runs, so the hourglass is lit just before the call and stays lit until Python returns.
- Help page 1 says what the hourglass means. Help page 4's engine line now says Explore's curves are PPL in Auto (true since beta 1h).

Drawing: `bu_Busy` uses one-colour `TRIANGLE_P` (GfxProbe T04's form, there on G1; here on G0) and four `LINE_P`; `bu_Band0` a one-colour `RECT_P` and `TEXTOUT_P`. All straight to G0, as `bu_Prog` already does.

## 2. Fewer curve points (a faster redraw)

- The Explore, Family and Rare curve is computed at **every 3rd pixel column** (1, 4, 7, ..., 268), the last column, and the **two columns either side of the pdf's peak**: 90 to 92 points on Explore instead of 268, joined by straight lines. Including the peak's columns means the polyline reaches the same top as before and `buYmax` (the y scale) is exactly beta 1h's.
- The cache is now the polyline's points (`buPts`, 2 numbers a point; beta 1d-1h kept segments, 4 a segment, built by `bu_SegPPL`, which is gone). `bu_Curve`, `bu_Shade` and `bu_RowAt` read points; the x₀ dot and the shade's first vertex are read off the drawn line, so they sit on it.
- **Cost of one C step on Explore (PC harness): 1,586 statements, against beta 1h's 4,222 (38 %).** On the G1, beta 1h's readout was "c 757 d 137" ms; if time follows statements, beta 1i's c should be around 300 ms. To be measured: More > Timing.
- The Python curve mode (Python only / Both) computes the same points (`BU_IN(10)` = the stride; `BU_YP` holds points), so Both still compares like with like.

## Checks

- Gate (`ppl_gate_v1c.py`, against beta 1h): PASS, the same lint notes as beta 1h (the `#END` block depth and the CAS text formatting at the moments page); fleet_names 0 collisions over 29 files; case_scan clean.
- `verify_BurrLab_beta1i.py` (beta 1h's script, Parts H, I, K adjusted for points, Part L new): **3,518 checks, 0 failures.** Part H: on 14 shapes every point sits exactly on beta 1c's one-row-per-column curve, the line between points is within 2 px of it (worst 1.5 px, at C = K = 50), the point columns are as specified, `buYmax` identical. Part L: the early title and hourglass before the recompute on Explore and Family, none on first entry, after a menu or on an x₀ step, none left on the finished frame; the blink on a modelled G1 clock (4,000 statements/s): the Danish 300 fit about 65 s, hourglass toggled 114 times, never more than 0.48 s between checks; lit before the Python fit call; the title row ends by x = 260 even at C = K = 50, S = 1,000,000.
- Text overlap (`text_overlap_v1.py --walk`, 80 runs, 1,164 screens): 0 overlaps. The one marginal frame straddle ("Weibull(k = C, λ = ...)" by 2.5 px) is beta 1h's too.

## Device checklist (G1 first, then G2)

1. Explore: press Up on C. The title should show C = 2.10 **at once**, with the yellow hourglass at the top right, then the plot follows. Note how long until the plot appears (More > Timing: "c ... d ... w ... ms"). Beta 1h was c 757 d 137 on the G1, c 868 d 117 on the G2.
2. Drag C sideways in the plot: the title keeps up with the finger; the hourglass flickers while it computes.
3. Press + (x₀): no hourglass; the shade and the red dot move, and the dot sits on the curve.
4. Look at the curve at a sharp peak (C = 10 or more): smooth, no visible corners; the top touches the same height as before.
5. Family: C+ / K+: the new title and hourglass at once. The Weibull animation: the hourglass on each step.
6. Fit > Engine > PPL only > Danish 300: the hourglass **blinks** beside the progress bar for the whole fit (about 45 s on the G1). Esc still stops it.
7. Fit > Engine > Auto > Danish 300: the hourglass lit while MicroPython works, then the results page.
8. Help page 1: the hourglass sentence; page 4: "Explore's curves: PPL in Auto".
9. Nothing should hang; if anything does, note the screen and the last key.
