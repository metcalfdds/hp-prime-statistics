# BurrLab beta 1c — changes from beta 1b (28 Oct 2026): layout and soft-key visibility

Built from `parts/` (beta 1b's parts in `parts_beta1b/`); `BurrLab_beta1b.txt` untouched (md5
fb87757c6440). Gate PASS against beta 1b (`gate_BurrLab_beta1c_output.txt`); fleet_names 0/0/0;
case_scan clean over 32 files; `verify_BurrLab_beta1c.py` 3,089 checks, 0 failures (beta 1b's
3,059 plus Parts F and G). Harness only. The engine, the fits and the data are beta 1b's.

From Roger's Virtual Calculator screenshots of beta 1b (Q-Q and Explore pages):

1. **Text collisions on the plot pages.** Cause: tick labels at frame + 4 and axis titles at
   frame + 15 shared rows with the status lines at 180/192; the three marker labels sat 11 px
   apart (the font is 12 px); "mean iff …" and "heavy tail …" sat inside the plot where the
   marker labels can be. Fix: one layout table for every plot page — frame 36..153; tick-label
   row 156; status rows 168, 180, 192; footer 204 (12-px rows; font 1's ink is about 10 px in a
   12-px row, measured on the screenshots, so rows have 2 px of clearance); in-frame labels in
   14-px rows PT+2 / PT+16 / PT+30 (legends, axis titles right-aligned at PR−2) and PB−13 /
   PB−27 (the pdf/CDF label bottom-left, the cap note and the short moment case bottom-right);
   mode/median/mean labels in the three top rows; left axis labels right-aligned at PL−2; the
   right CDF axis "0" at PB−12; y-max and "h max" labels above the frame at PT−14; tick labels
   through `bu_TickLbl`, clamped to x 37..317 so they meet neither the left labels nor the edge.
   Explore and Family use the same frame (plot 117 px tall instead of 128). The A-D page,
   help page 4 and the CAS moments page were a line too long against the footer and were
   trimmed. **Verify Part F** (in `layout()`, so every page run is covered): every TEXTOUT_P on
   every screen (G1, the last text at a position wins, as RECT_P clears do on the device) is a
   box of 6.5 px/char (font 1; 8 for font 2) by 10 px of ink (13 for font 2); no two boxes may
   overlap with 2 px of vertical clearance, and on a screen with the plot frame no box may
   straddle the frame's bottom edge within the frame's x-range. The check found and the fix
   removed 20 collisions across the hist, hazard, family, A-D, help and moments pages.
2. **Soft keys C / K / S / x₀ "did nothing".** The harness shows the strip tap IS taken by the
   polling loop and not eaten by the drain (Part G: each of the four selects its parameter and
   the footer says so); the response in beta 1b was the label turning yellow on the orange band,
   invisible on the emulator. Now the chosen piece is drawn INVERTED (a white box, orange text,
   `bu_TPiece`, sized by TEXTOUT_P's own return) and the footer reads "K chosen: arrows/drag.
   +/- x₀, 0 next, Ent". The emulator can still miss a click shorter than a loop pass (Lessons
   §16: press about 0.3 s); the G1 takes a light tap (20 Oct).
3. **Other pages, same two faults.** Keys without a visible effect: the simulation's x1/x10/
   x100 changed nothing on screen mid-run; the status row now reads "n = 120 (x10): mean …".
   The hist +/−, Q-Q L/R, Rare x±, Family C±/K±, results soft keys all change the page (checked
   in Part B). Collisions: see 1 (Part F runs on every page of every B/D/E run).
