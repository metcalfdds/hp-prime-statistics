# GaltonBoard beta 2: changes from beta 1b

16 October 2026. This is the showcase version from the fleet review (`Fleet_Review_2026-10-16_v1.md` §6, GaltonBoard). It is built on `GaltonBoard_beta1b.txt` and keeps every beta 1b fix, including the BINOMIAL(n, p, k) order from its addendum. **It has not been run on hardware.** Its MicroPython part has never run anywhere: test it with the Terminal open.

Line references are given as `beta 1b → beta 2`. The file grew from 688 to 1621 lines, and most of beta 2 is new routines.

## (a) Changes

1. **Header (1-81).** Banner "beta 2"; a dated "beta 2: what changed" paragraph. The beta 1b and 1a paragraphs are kept in short form, as are the licence, AI-assistance and firmware lines ("NOT yet been run on hardware", plus a line saying the Python part has never run). WHAT YOU SEE, KEYS AND TOUCH and HOME EXPORTS are rewritten for the new gestures and soft keys, and for GB_PEG, GB_PYN and GB_PYO.
2. **The scene now uses three layers** (gbScene 227-351 → 556-700; gbRefresh 438, gbFrame 712).
   - G3 is the static scene.
   - G2 is G3 plus the last five landed paths.
   - G1 is G2 plus whatever moves (balls, trails, the Bernoulli box, the bar-info panel, lattice paths), and the footer.
   - The screen gets one `BLIT_P(G0,0,0,G1)` and then `DRAWMENU`.
3. **Pour mode** (new gbPour 929, gbBallStep 794, gbNewBall 781).
   - **How to start it:** hold a finger still on the funnel for 0.35 s. The funnel zone is x 132-188, y from gbTop−14 down to half a row below gbTop. Or use the Pour soft key, or the 0 key. A ball launches every third frame, at most 8 in the air.
   - **Per-ball state:** parallel file-level lists gbQR (segment), gbQK (rights so far), gbQG (this row's choice), gbQF (frame in segment) and gbQM (the path so far, as binary digits).
   - **Each frame:** one G2→G1 blit, the discs and trails, one blit to the screen, DRAWMENU.
   - **When it stops:** lifting the finger (hold mode). In soft-key/0 mode, a tap anywhere, 0 or Esc. Esc in every mode. Balls already in the air finish their fall.
   - **Pacing:** each frame lasts at least 25 ms, timed with `TICKS` rather than `WAIT`, so keys are read during the pour (GfxProbe T15 is still open).
   - **×10** uses the same engine with exactly ten launches (mode 3).
4. **A landed ball redraws only its bar** (new gbLand 725, gbCol 516, gbBar 480).
   - gbCol wipes the column on G3 from y 127 to the baseline. It then redraws in the scene's own order: normal area, bar, count, the magenta segments to both neighbours and the square, the green outline over three columns, and the dotted lines.
   - When the red x̄ line moves, its old column is redrawn as well. The left readouts are wiped and redrawn (gbReadL 453).
   - **The whole scene is rebuilt only when** a bar exceeds the y-scale, or (with overlays on) the expected counts n·P(k) would rise 3 px or more.
   - A count label that has no room above its bar goes inside it.
5. **Ball trails** (gbTrPush 756, gbTrDraw 768). Each ball keeps a ring of its last 6 positions, drawn as 3×3 dots that fade from #FF4040 to #FFE0E0, oldest first.
   - **The last five landed paths** are thin light-red (#F5A0A0) polylines on G2 (gbPathDraw 412).
   - They stop at the lowest peg level (y 126), so they never touch the bars. They are cleared with the counts (gbClear 289).
   - They are hidden while Pascal's numbers are shown, and during a p-drag.
6. **The Bernoulli string** (gbBBox 864, gbDropAnim 366-415 → 889-926).
   - While a single animated ball falls, a light-red box at top left (x 0-99, y 17-71, over the readouts, which are stale then) prints its choices one letter per row, six to a line.
   - After the last row it adds "→ k rights" and "→ bin k".
   - On landing, the footer keeps the whole line, e.g. `R L L R L L R L → 3 rights → bin 3`, in red until the next action.
   - gbDropAnim now runs the same gbBallStep as pour mode, so the single ball has a trail too. Its geometry and frame counts are unchanged: 2 + R×speed + 4 frames, `WAIT(0.02)`.
7. **Drag p** (new gbPress 1439; the main loop's peg-field branch 661-663 → 1590-1593).
   - **A press on the peg field or the funnel is watched until the finger lifts.**
   - **Movement of more than 8 px sideways is a drag.** p becomes the finger's position across the board: (x − gbX0) / ((R+1)·bw), rounded to 0.01 and clamped to 0.05-0.95.
   - Each new p calls gbScene and gbFrame. The old bars are hidden while dragging (gbPrev); the magenta squares, the normal curve and the Rp line follow the finger.
   - On lift the counts clear (gbClear) and the footer says "p = 0.77 now: the counts were cleared (new board)".
   - A held press on the funnel pours. Any other press with no movement drops one ball.
   - The arrow keys stay as the keyboard equivalent, and now also print the "counts cleared" line.
8. **Soft keys and a one-line legend** (346-350, 586-591 → gbMenuKeys 278, gbFoot 702).
   - The soft keys are `DRAWMENU({"Drop", CHAR(215)+"10", CHAR(215)+"100", "Pour", "Rows", "Menu"})`, drawn after every blit to G0, the animation frames included.
   - The three legend lines are now ONE dodger-blue line at y 206 (house form): `⇆ = p, ⇅ = rows (clear), tap bar = info, Esc = quit`.
   - The same line carries status messages when there are any.
   - gbHB moves from 187 to 191, so the bars are 57 px tall instead of 53. The bin labels sit at y 194 and the footer at 206, which ends at 217, below the strip's 218.
   - Rows opens the existing gbSetRows. Menu (or Enter) opens the menu. p stays on the arrows and the drag.
9. **"More" soft-key pages (Roger's new convention): deliberately not applied.**
   - Every action on this screen fits in six keys: Drop, ×10, ×100, Pour, Rows and Menu.
   - The rest (p by touch is the drag; overlays, SD colours, Pascal, 100,000, speed, D1/D2, help) sit in the Menu soft key's CHOOSE list, which is itself tappable.
   - CLAUDE.md's rule says "a screen whose actions fit in six gets no More". The help page lists the soft keys as they are.
10. **Tap a bar: a drawn panel instead of a MSGBOX** (gbBinInfo 506-522 → 1276-1336).
    - The panel sits over the pegs, with the bar framed in red. It shows the bin, the observed share, binomial P(k), the expected count n·P(k), C(R,k), and the **normal area from k−0.5 to k+0.5** (two `NORMALD_CDF(μ, σ, x)` calls; the continuity correction, item 9 of the task).
    - The panel says when the approximation is poor.
    - **Tap the same bar again:** gbLattice (1233) draws every lattice path to that bin, one by one, in light blue on G1, with "C(8,4) = 70 paths" and a running count. This is limited to R ≤ 8; for larger R it says "too many paths to draw (C(12,6) = 924)".
    - A tap on another bar shows that bar. Anything else goes back.
11. **Empirical Pascal's triangle** (gbPass 397, gbPegLbl 379; Menu "Pascal's triangle: off / counts / C(r,k)").
    - **Pass counters:** `GB_PEG := MAKEMAT(0, R, R)` (an EXPORTed matrix, as in ChiTable's verified case). It is incremented in every drop routine: the animated ball (gbBallStep), gbDropFast, and both engines of the 100,000 drop.
    - **Display:** shown as font-1 numbers just left of each peg when bw ≥ 28 (R ≤ 9). Blue for counts (compact: 987, 1.2k, 27k), magenta for C(r−1, j) in theory mode.
    - A count updates in place on G3 as a ball passes. For R > 9 the footer explains why nothing shows.
12. **The normal curve as a filled area; SD-coloured bars** (gbScene's overlay 2; Menu "Colour bars by distance from Rp (SD)").
    - The normal is drawn as light-green (#E8F6EB) vertical lines per pixel column, UNDER the bars, with the green outline on top.
    - When Rp < 5 or R(1−p) < 5, the curve and area turn grey (#A0A0A0 / #EBEBEB) and the title line reads e.g. "normal approximation poor (Rp = 4.00 < 5)" in grey (gbTheory 343 sets gbPoor). This includes the default board, R = 8 and p = 0.5, when the normal overlay is on.
    - SD option: |k − Rp|/SD ≤ 1 gives a solid green bar, ≤ 2 orange, otherwise red.
13. **The density is cached** (gbTheory 343). NORMALD is evaluated once per pixel column, (R+1)·bw + 1 ≈ 300 calls, only when R or p change. Pixel heights are cached per scene (gbNy, gbEy) and reused by gbCol. Harness costs are in (d).
14. **Drop 100,000** (new #PYTHON gbPyDrop 1029-1080; gbBigDrop 1088; Menu item 5).
    - **Route A.** Python reads `GB_R`, `GB_P` and `GB_PYN` with `hpprime.eval`, never argv. It imports `from urandom import random, getrandbits` (not `random`).
    - **The simulation:** each ball's R choices form one number m (at p = ½, one `getrandbits(R)` per ball; otherwise one `random() < p` per peg). Pegs and bins are counted from the histogram of m.
    - **The return trip:** it writes R(R+1)/2 peg counts and then the R+1 bins back ONE value per `eval`, the last bin last. The payload is fixed in size and does not depend on N.
    - **The PPL side follows §9:**
      - GB_PYO is cleared to −1 first.
      - It is validated by reading the last element inside IFERR (it must be ≥ 0), and the bins must add up to N.
      - The PPL fallback (gbDropFast) is capped at 5,000 balls.
    - **The badge:** the footer shows "engine: MicroPython, 100000 balls in … ms" (green) or "engine: PPL (5,000 cap), 5000 balls in … ms" (orange), with the elapsed TICKS.
15. **Menu** (549-580 → 1388-1436). The list grows to 15 unnumbered items: Drop 100,000, Colour bars by SD, and Pascal's triangle are added. Leave is item 15, which the Prime labels F.
16. **Help is two drawn pages** (525-546 → 1342-1385).
    - **Page 1:** the BELL comes from the number of ROWS (each bin is a sum of R steps: de Moivre-Laplace; sweep rows 3 to 12). More BALLS only make the bars match the squares, and x̄ and s settle. The normal turns grey when Rp or R(1−p) < 5.
    - **Page 2:** every soft key and gesture, the keys, and the menu's new items.
    - **Welcome:** updated for the new gestures and soft keys (1529).
17. **House rules applied to the rewritten code.** These lines had not run on hardware anyway.
    - MAX on a list (beta 1b 263-264) is replaced by loops.
    - String lengths use DIM (confirmed) instead of SIZE.
    - gbWaitAny returns the key or −1, with the tap in gbTapX/gbTapY (TouchKit shape).
    - G1 and G2 are dimensioned in gbInit.
    - The MAKELIST counter stays Home's K throughout (pending GfxProbe T19).
18. **The summary line** now ends "; bins in GB_CNT, pegs in GB_PEG".

## (b) Gate (check.sh, final)

```
--- 1. kit lint ---  1 error: "unbalanced ... -1" at EOF.  Cause: the kit counts the
    #END line that closes the #PYTHON block as an END (checked: with the Python block
    removed the file gives 0 errors).  This is the 'unbalanced' the brief allows.
--- 2. ppl_check tally NEW: (none)      ORIG (beta 1b): (none)
--- 2b. hard errors E2 E3 E6 E8 E10 E11: none
--- 3. lint_ppl: 987 checks, 15 problems; all are known noise: block depth -1 at #END
    (Python block, as NormExplorer beta 42), 'STRING() with 4 args' at 385
    (STRING(COMB(a, b), 2, 0): the lint counts COMB's comma), 'targets pdG/dcG/ftG, not
    a GROB' (grob parameters, as beta 1b's dcG), file-name and EXPORT discipline.
--- 4. full parse: PARSE FAIL at the file-level LOCAL after the EXPORT list (129), as
    beta 1b (93): the tool's limit.  With the EXPORT GB_ / LOCAL gb lines masked:
    beta 2 PARSE OK (47 functions), beta 1b PARSE OK (25 functions).
fleet_names_v2 over out/*.txt (45 files): 0 untagged, 0 mixed-tag, 0 built-in matches;
    every gb* collision is beta 1b <-> beta 2 of this program (no other program).
```
During the work the checker caught `LOCAL poS` (= POS, a built-in), which was renamed `poSl`, and a legend line ppl_check estimated at 336 px, which was shortened ("(both clear)" became "(clear)").

## (c) Harness and SciPy results

`verify_GaltonBoard.py` (in `out/`) runs 83 checks and **ALL PASS**; the full output is in `verify_GaltonBoard_output.txt`. The harness needed one test-side shim: bare `RANDOM` (the fleet idiom `RANDOM < p`, used by beta 1b and CentralLimit too) is covered by ppl_run_v1 only as a call.

**Statistics, against SciPy**

| | program | SciPy |
|---|---|---|
| P(k), R = 8/0.5, 8/0.3, 12/0.5, 10/0.37, 3/0.05 | gbE | `binom.pmf`, < 1e-12 |
| bar info, bin 4, R = 8, p = .5 | `binomial P(4) = 0.2734` | 0.273437 |
| continuity-corrected area 3.5 to 4.5 | `normal area 3.5 to 4.5 = 0.2763` (2 NORMALD_CDF calls) | 0.276326 |
| C(8,4) | 70 (panel, and 70 paths drawn) | 70 |
| Pascal, theory row 8 | 1 7 21 35 35 21 7 1 | C(7, j) |
| SD bands, R = 8, p = .5 | R R O G G G O R R | same |
| "poor" rule | R = 8, p = .5: Rp = 4.00 < 5 (grey, title); R = 12: green | |

**The Python block under CPython** (stub `hpprime.eval` and `urandom`), with R, p, N of 8/0.5/100,000, 8/0.3/20,000, 12/0.5/100,000 and 5/0.73/20,000:
- It wrote 45 / 45 / 91 / 21 single values, indices in order, the last bin last.
- The bins and every peg row add up to N.
- The bins fit Binomial(R, p) (χ² p = 0.66, 0.37, 0.77, 0.26).
- The last row's pass counts fit N·C(r−1, j)p^j(1−p)^(r−1−j).

**The program in the harness**
- **Scene:** a single legend line at y 206, the soft keys after the blit, the lowest text ending at y 217, bin labels at 194.
- **Single drop:** 22 frames for R = 8. The Bernoulli box grows "R L L R R R" / "L L", then "→ 4 rights" / "→ bin 4" (seed 1); with seed 11 the footer keeps `R L L R L L R L → 3 rights → bin 3`. GB_PEG has one pass per row.
- **Bar info and lattice:** the second tap on the same bar drew 70 paths in 71 frames. At R = 12, "too many paths to draw (C(12,6) = 924)".
- **Drag p:** a 7-sample drag ended at p = 0.77, the counts were cleared and both footer messages appeared. A 6-px wobble is a tap: one ball, p unchanged.
- **Pour, finger held 900 readings:**
  - 184 balls, 571 frames, never more than 8 in the air.
  - Every ball was counted once per row and once in a bin; five paths were kept.
  - 50 full rebuilds, mostly in the first balls while n is small; the rest were one-column updates.
- **Pour by soft key, stopped by a tap:** 41 balls. **×10:** exactly 10.
- **Drop 100,000, PPL fallback** (PYTHON does nothing in the harness, as when Python fails):
  - `gbBigDrop(300)` gave "engine: PPL (5,000 cap), 300 balls in … ms" and updated GB_PEG.
  - `gbBigDrop(7000)` was capped at 5,000.
- **Drop 100,000, Python path,** with PYTHON() patched to run the real block in CPython and write GB_PYO(i) one value at a time:
  - It was accepted and folded in: "engine: MicroPython, 100000 balls", GB_PEG rows = N.
  - A Python that stops after 10 of 45 values falls back to PPL. This shows the last-element validation works.
- **Geometry:** the closest light-red path pixel to a peg centre is 2.0 px at R = 3 and ≥ 2.83 px for R ≥ 4. Paths never cross a peg; at R = 3 one pixel may touch a peg's radius-2 ring.

**Costs (harness counts of drawing calls; no device timing):**
- **gbScene rebuild at an unchanged R, p:** 0 NORMALD. 163 draw calls with the binomial overlay, 710 with the normal area and curve (two ~300-column passes).
- **A drag sample:** about 298 NORMALD (one per column, because p changes), plus the 710 draws. On a G1 that may be a few redraws per second; see checklist item 12.
- **Pour:** a median 113 draw calls per frame (up to 8 balls with trails), and a maximum of 320 in a frame that rebuilt the scene.
- **One gbCol update:** 44 calls (binomial overlay), 176 (normal area + curve).

## (d) DEVICE TEST CHECKLIST (least to most risky)

1. Paste and Check: no syntax error. The `#PYTHON gbPyDrop … #END` block must paste intact, with its indentation kept.
2. Run `GaltonBoard()`, then any key past the welcome page (new text; no line should overrun).
   - **The board:** the title, R = 8, p = 0.50 on the right, 9 bin labels at y 194, and ONE footer line at 206.
   - **Soft keys** Drop, ×10, ×100, Pour, Rows, Menu (the × glyph from CHAR(215)), with nothing overlapping the strip. The bars should be slightly taller than in beta 1b.
3. **BINOMIAL order (beta 1b addendum):** at R = 8, p = 0.5 the magenta squares follow 1, 8, 28, 56, 70, 56, 28, 8, 1.
4. **Drop soft key / − key:** one ball falls.
   - **The disc:** a solid red disc (ARC_P r 1-3, as in beta 1b's test) with a fading trail behind it.
   - **The top-left box:** one letter per row (six to a line), then "→ k rights" and "→ bin k". The "→" is CHAR(8594).
   - **The footer after landing:** the whole string in red. Then press a key: the legend returns.
5. **Tap a bar:**
   - **The panel:** P(4) = 0.2734 at R = 8, p = 0.5. The normal area 3.5 to 4.5 = 0.2763 must not be 0.2734: it is the continuity-corrected normal, not the exact binomial.
   - **The red frame** round the bar.
   - **Tap the same bar again:** 70 light-blue paths appear one by one and "C(8,4) = 70 paths" is printed. Note how long that takes on the G1.
   - **R = 12:** the "too many paths" line.
   - **Tap another bar instead:** that bar's panel.
6. **×100 and + :** the "Dropping 100 balls" panel, then the board.
7. **Menu → Pascal's triangle** (once: counts; twice: C(r,k)).
   - **The numbers:** sit just left of each peg, with no digit over a peg or the readouts.
   - **Counts:** then drop single balls: the numbers along the ball's path tick up.
   - **R = 10:** the footer says the numbers need R ≤ 9.
8. **Menu → Overlays** (to "binomial+normal") and **Colour bars by SD:**
   - the light-green area sits under the bars with the green outline on top;
   - at R = 8, p = 0.5 everything turns grey and the title reads "normal approximation poor (Rp = 4.00 < 5)";
   - Up to R = 10 or more: green again;
   - the bar colours run red/orange/green symmetrically.
9. **×10 soft key:** ten balls cascade, several in the air at once.
   - Watch the soft-key strip: it is repainted after every frame blit. Note any flicker.
   - Bars grow without the whole board redrawing, except an occasional rebuild that may show as a small pause.
10. **Pour by holding the funnel** (just under the title, centre):
    - after about 0.35 s a stream starts; lift the finger and it stops, the last balls landing;
    - check MOUSE keeps reporting a still finger (the hold is read from it);
    - the last five paths remain as thin light-red lines;
    - Esc during a held pour also stops it.
11. **Pour by the Pour soft key, then by 0:** a stream with "tap, 0 or Esc = stop"; each of the three stops it. Note the frame rate on the G1 (frames are paced to at least 25 ms).
12. **Drag p:** put a finger on the pegs and slide sideways.
    - p in the right readout, the squares, the Rp line and (with the normal on) the curve and area follow. The bars are hidden while dragging.
    - Lift: the counts clear and the footer says so.
    - Note the redraw rate on the G1 (about 300 NORMALD and 700 draws per new p with the normal on). If it is sluggish, turn the normal overlay off for drags in class.
    - A press with no movement still drops one ball.
13. **Drop 100,000 (Menu item 5), Terminal open, on the G2 first:**
    - (a) "engine: MicroPython, 100000 balls in N ms" in green, with n += 100000. Record N ms (expect seconds at p = 0.5 with `getrandbits`, and longer at other p: one `random()` per peg).
    - (b) Pascal counts consistent with n (top peg = n).
    - (c) If the badge says "engine: PPL (5,000 cap)" instead, read the Terminal for the traceback. The fallback takes tens of seconds for 5,000 balls.
    - (d) Repeat at p = 0.3 and on the G1.
    - (e) Type `GB_PYO` in Home: R(R+1)/2 + R + 1 non-negative numbers.
14. Esc: Home shows "Galton Board: N balls, R = …, p = …; bins in GB_CNT, pegs in GB_PEG". GB_PEG is readable in Home. Home's K has been overwritten (MAKELIST).

## (e) Not confirmed / left as is

- **The whole Python path is not yet run on hardware.** These are unverified:
  - writing a list element through `hpprime.eval("GB_PYO(3):=17")`;
  - `urandom.getrandbits(R)` behaviour;
  - the timing.
  The PPL fallback and the validation make a failure harmless, but only a Terminal-open run tells which engine actually works.
- **DRAWMENU after every animation frame** follows the rulebook (soft keys after every blit). Whether the strip flickers during pour is unknown.
- **The pour hold relies on MOUSE reporting a finger held still.** This is documented, not yet seen in this fleet.
- **WAIT(0.02) in the single drop is kept from beta 1b** (GfxProbe T15 is still open). Pour mode uses TICKS pacing instead.
- **No "More" soft-key page:** this screen fits in six (item 9).
- **Kept as before:** `CHAR(8730)` (√) in readouts and help, the bare `RANDOM` idiom, and Home's K as the MAKELIST counter.
- **R = 3:** a light-red path can touch one pixel of a peg ring (2.0 px from the centre); cosmetic.
- **Not in scope:** the review's "tilted board for p ≠ 0.5" and readout taps.
