# CentralLimit beta 2: changes from beta 1b (an APP program)

16 October 2026. This is the touch and graphics version from the fleet review (`Fleet_Review_2026-10-16_v1.md` §6, CentralLimit). It is built on beta 1b and keeps every beta 1b fix: `cltX`/`cltFr`, the "(quick)" cap label, item (A) in Help, and Home's K as the MAKELIST counter. **It has not been run on hardware.** The install notes are unchanged word for word (beta 1b lines 52-60 are now lines 120-128). The app hooks keep their names exactly: `CentralLimit`, `START`, `Plot`, and the six existing VIEW entries. One VIEW entry is new. The file has no Symb, Num or Info hook, before or after this change.

Line references below are `beta 1b → beta 2`.

## (a) Changes

1. **Header** (1-50 → 1-118). Changes:
   - The version string is now beta 2, with a "beta 2 - what changed" paragraph that cites beta 1b line numbers.
   - The beta 1b and beta 1a paragraphs are kept.
   - The licence, AI-assistance and firmware ("NOT yet been run on hardware") lines are kept.
   - The VIEWS MENU list now includes Square-root law.
   - DASHBOARD CONTROLS has been rewritten to cover every button, gesture and key.
2. **Watching one sample: the showcase** (new `cltOneSample` 1202, `cltPause` 465). The "1 sample" button, the Up key, or a tap in the lower-left corner of the top panel (x ≤ 54, y ≥ 72) runs a four-step animation:
   - **Frame 1:** the n members of one sample, picked with replacement, appear as red 2×2 `RECT_P` dots on the population's axis. Each dot is raised 0-8 px at random so that repeated picks stay visible.
   - **Frame 2:** a short red bar (two `LINE_P`) and an x̄ glyph mark the members' mean.
   - **Frames 3-5:** the mean falls toward the top of its bar in the bottom panel, a quarter of the distance per frame.
   - **Final frame:** the bar is one taller, D2 has one more value (`CONCAT`), and a red square shows where the mean landed. The members stay on screen until the next action.

   The first single sample of each app start gets a caption box: "This is ONE sample's mean / - the pile is many of them." It is placed on the side away from the mean.

   Any key or tap during frames 1-5 skips to the end. `cltPause` waits on `TICKS` while polling both GETKEY and MOUSE, then drains, so the key that skips the animation does nothing else. No `WAIT(n)` is used.
3. **The "+1" button and the Down key** add one mean to the pile at once, with no animation, and mark where it landed.
4. **Dragging on the top panel to choose n** (new `cltTopPress` 1659, `cltKAt` 699). A press on the top panel starts a held loop that polls MOUSE until the finger lifts. The loop is capped at 15 s by `TICKS`.
   - **Drag (more than 8 px of movement):** x maps to √n = 1…10, snapped. A ruler (1 4 9 … 100) replaces the panel's label row, with the chosen n in red and a red line at the finger. The title shows "n = k²". In the bottom panel, the old means turn grey and the predicted N(μ, σ/√n) curve is redrawn for the new n with no resampling, under the label "n = 64: the curve first; lift to draw". The readouts show "If n = 64: standard error σ/√n = …". Redraws happen only when n changes. Lifting the finger runs `cltSample`.
   - **Tap without movement:** draws a fresh set, as in beta 1b (842).
   - **Keyboard equivalent:** Left and Right step √n down or up by one and draw samples.
   - **Curve with no means yet:** the preview is drawn as a density, scaled so that the n = 100 curve just fits. It therefore gets narrower and taller as n grows.
5. **Six drawn buttons, y 220-239** (new `cltButtons` 793, `cltButton` 1638). The buttons are 1 sample, +1, n−, n+, Curve and Menu. They are drawn as `RECT_P` with labels on G1, in the house colours. Curve is tinted while the curve is on. Any tap at y ≥ 218 is read as slot `MIN(6, IP(x/53.4)+1)` and handled after the finger lifts. There is no DRAWMENU, which is untested inside an app.
   - Hardware shortcuts: Up, Down, −, +, 0 and Enter, in button order.
   - The two-line footer (506-507) has been removed.
   - "Esc = quit" is now in the title row (x 256, dodger blue).
   - "n = …" in the title row moved to x 170, font 2.
   - Every y on the dashboard: title 1/3; top panel 14-89 with its label row at 16; ticks 90-92; bottom panel 94-167 with its label row at 96; axis labels 170; readouts 182 / 194 / 206; buttons 220-239 with labels at 224. Nothing is drawn at 207-219 apart from the descenders of the 206 row. The harness layout audit found 0 overlaps and 0 off-screen texts on 123 pages.
   - **"More" key convention (Roger, 16 Oct): not applied.** The dashboard has exactly six button actions. Everything else (Square-root law, Help, population, number of samples, Leave) is one tap away in the Menu button's CHOOSE list, so the whole dashboard works without a keyboard. Adding a More key would have pushed Menu off slot 6. This decision is noted in the header and in the `cltButtons` comment, and Help now says "Esc (or Menu, Leave) leaves the dashboard".
6. **Bar tooltips** (new `cltTipDraw` 820, `cltHit` 751, `cltHitAdd` 739, `cltHitInit` 724). While the bars are drawn, their hit boxes are recorded in file-level lists (pre-sized to 100 entries).
   - **Bottom panel:** a tap on a bar of means shows a box drawn on G1 (not a MSGBOX) with the interval ("x̄ from 5.2 to 5.4"), the count, and the share ("13.5% of 200"). The bar is outlined in black.
   - **Top panel:** a plain tap must still resample, as the brief requires for the top panel. So a population bar shows its box when it is **held for 0.6 s**. This settles the brief's two top-panel rules, which conflict.
   - Geometric bars read "value = 3" or "values 3 to 4".
   - A bottom-panel tap on the curve label, or anywhere that is not a bar, still toggles the curve, as in beta 1b.
   - The box, the caption and the one-sample markers are cleared at the next key or tap.
7. **The square-root law** (new `cltLaw` 1449, menu item "Square-root law", and `VIEW "Square-root law", cltVLaw()` 1851, placed before Help).
   - The SD of the means for each √n tried is kept in `cltLawSD` and `cltLawM`, file-level lists of 10. They are written by `cltLawPut` after every `cltSample` and every single sample.
   - The page plots each point as a magenta square over σ/√n (blue), drawn one pixel column at a time, against n from 0 to 100.
   - A table on the right lists n, SD(x̄) and σ/√n. Grey notes underneath explain the page.
   - The record is cleared with each new population, because the old points belong to a different σ.
   - The CHOOSE list now has 10 items, so Leave shows as "A". Nothing on screen refers to it by number.
8. **Means bars coloured by standard-error distance.** Each bar is coloured by the distance of its centre from μ, measured in SE = σ/√n: green #008C3C/#A0DCB0 within 1, orange #FF4500/#FFC08C within 2, red #FF0000/#F5A0A0 beyond. While n is being previewed, the bars are grey. `cltMeanStats` now also counts the means within 1 and 2 SE, and row 206 shows "68% in 1 SE, 95% in 2 SE". The caption says "the pile", not "the magenta pile", because the bars are no longer magenta.
9. **Population density overlay** (new `cltDenCache` 497, called by `cltPopStats`). The overlay uses closed forms native to PPL:
   - uniform 1/(b−a);
   - `NORMALD(a,b,x)`;
   - exponential `EXP(-x/a)/a`;
   - bimodal ½N(a,1)+½N(b,1);
   - geometric pmf, as the expected count of each whole bar, N(q^(lo−1) − q^(lo+w−1)), with the tail included in the last bar.

   The overlay is computed once per population and cached as 301 pixel rows. The dashboard only reads it. It is drawn as a black line; the pmf is drawn as flat pieces that are not joined. Data supplied in D1 gets no overlay. Bars and curve share one scale (`cltPTop`).
10. **Faster early growth** (553 → 1182): the dashboard redraws after every sample for samples 1-20, then every reps/40 as before. With 200 samples that is 55 live frames; beta 1b drew 39.
11. **n = 1 first; + steps through 1, 4, 16, 64, 100.** `cltK` starts at 1 (106). `START` sets n = 1 when there is no pile, and `cltNewPop` sets it for every new population and for adopted D1 data.
    - + and the n+ button step to the next of √n 1, 2, 4, 8, 10. − and n− step back down (`cltKUp`/`cltKDn` 385-398, replacing 847-848).
    - Row 194 now reads "SD of x̄'s = …; σ/√n = … (standard error)", the one place the term is named.
    - At n = 1 the means panel reads "200 'means' of 1 member each". The empty panel's hint reads "n = 1 to start: each mean is one member".
12. **Help has two pages** (782-802 → 1565-1612): page 1 explains how to read the dashboard, and page 2 lists every button, tap, drag, hold and key, with item (A) kept. Esc on page 1 goes straight back. The "no samples yet" hint now mentions the 1 sample button.
13. **Cached normal table** (new `cltPhiInit` 712): φ(z) for z = 0…4.5 in steps of 0.02, 226 values, built once. Every predicted curve reads φ(z)/SE from the table, so the drag and the live frames call no NORMALD per pixel (beta 1b 445 did). The peak scale uses the table too (428).
14. **No MAX or MIN on a whole list** (277-278, 407, 424, 714, 720): these are replaced by loops in `cltLMax`/`cltLMin` (358-378). Whole-list MAX is on the TOUCH brief's not-verified list.
15. **`cltDrain`/`cltWaitAny` moved up into the helpers** (738-759 → 430-460) so that the animation can call them. `cltWaitAny` now matches the house kit: it returns the key code (−1 for a tap, with the position in `cltTX`/`cltTY`) and drains keys at the end.
16. **Integer labels in the code that was rewritten use `STRING(n, 2, 0)`** (403, 417, 455, 498, 502): ppl_check's E9 count drops from 5 to 0. The x position of each right-aligned label is now computed into a local before `TEXTOUT_P`, which clears lint_ppl's three "bare cWid" lines.
17. Code that did not change: `cltNice`, `cltF`, `cltDecFor`, `cltName`, `cltNorm`, `cltDraw1`, `cltCount`, `cltMakePop`, `cltMeanBins`, `cltChooseN`, `cltAskReps`, `cltBuiltin` (apart from MAX), `cltWelcome`, `Plot`, and the six existing VIEW bodies.

## Gate (check.sh NEW = beta 2, ORIG = beta 1b)

```
kit lint: 0 errors
ppl_check tally NEW: 7 E1, 21 E7         ORIG: 6 E1, 20 E7, 5 E9
  E1/E7: app settings H1, H2, Xmin ... and #RRGGBB:24h read as names, plus one
  E1 + one E7 per VIEW entry (the checker cannot read VIEW). The single +1 in each is
  the new VIEW "Square-root law". The total falls from 31 to 28: E9 drops 5 -> 0.
hard errors (E2 E3 E6 E8 E10 E11) in NEW: none
lint_ppl: 1104 checks, 4 problems, all known noise (file name, EXPORT discipline);
  beta 1b's three "bare cWid" lines are gone
full parse: PARSE FAIL at `#003CC8:24h` (1414). Beta 1b fails the same way (704); this
  is the tool's limit. The harness, which converts :24h, loads and runs the whole
  file: 51 routines plus 7 VIEW entries.
fleet_names_v2 (newest version of each of 26 programs in out/): 0 collisions,
  0 untagged, 0 mixed, 0 built-in
```

## Harness and SciPy runs (`verify_CentralLimit.py`; full output in `verify_CentralLimit_output.txt`)

The harness does not read a bare `RANDOM`, so the script handles it with a 6-line subclass that reads `RANDOM` as `RANDOM()`. The app settings (H1, Xmin …) are plain globals in the harness.

```
cltPhi table: max |error| 0.00242 of peak 0.39894 (0.61%) -> 0.36 px on a 59 px curve
densities vs scipy: uniform 0, normal 0, exponential 1.4e-17, bimodal 0; geometric bars 1.7e-16
Uniform(0,10), N = 500, sigma 2.9285 (D1 numpy: same), 400 samples each, seed 7:
  sqrt n  n    SD(xbar)  sigma/sqrt n  ratio   in 1 SE  in 2 SE
   1      1    3.0050    2.9285        1.026   53.0%   100.0%   (uniform n=1 theory 57.7/100)
   2      4    1.4671    1.4642        1.002   71.0%    94.2%
   4     16    0.7565    0.7321        1.033   68.5%    95.5%
   8     64    0.3662    0.3661        1.000   67.8%    96.5%
  10    100    0.2808    0.2928        0.959   69.5%    96.5%
  worst |ratio - 1| 0.054 (SD-of-400 sampling error ~0.035); cltMS == numpy std(D2, ddof=1)
square-root law page, Exponential(mean 5), seed 5: rows n 1/4/16/64/100, SD 5.003/2.484/1.341/
  0.617/0.494 vs sigma/sqrt n 5.098/2.549/1.275/0.637/0.510 (python agrees); 5 squares; curve
  of 164 one-column segments; "No n tried yet:" before any samples
live frames, n = 1, 200 samples: 55 (1-20 each, then every 5th)
one sample watched (n = 16): 5 frames (16 red dots; + red bar and x-bar; + falling square x3);
  its mean = mean of its members; exactly one bar +1; D2 200 -> 201; caption on the next frame
  key during frame 1: 1 frame, then straight to the pile, and the key leaves nothing behind
  +1: 0 frames, D2 +1, mark only
drag 60 -> 300 px: 4 preview frames n = 9, 16, 49, 100; red ruler label; 16 grey old bars;
  D2 untouched until the lift; then cltK = 10 and 200 new means
plain tap on top: resample; hold 0.7 s on a top bar: "x from 4.5 to 5.0 / count = 21 /
  share = 4.2% of 500" (checked against cltPCnt)
bottom-bar tap: "x-bar from 5.2 to 5.4 / count = 27 / share = 13.5% of 200" (numpy count 27)
curve-label tap: curve off; + x5, - x2 from n=1: n = 1, 4, 16, 64, 100, 64, 16
Menu button: CHOOSE "Central Limit", 10 items; Help: 2 pages, Esc on page 1 returns
density overlays: uniform flat, exponential and geometric scale up past the tallest bar
  (100 vs 85; 150 vs 142), so the curve never clips; the exponential's first bar is 85
  observed against 90.6 expected
layout audit (6 px/char, 11 px rows), 123 pages: 0 problems; harness warnings: none
```

## (b) DEVICE TEST CHECKLIST (least risky first)

1. **Install it as an app, exactly as the header says.** In Apps, highlight Statistics 1Var, tap Save, and name the copy CentralLimit. Open its program, replace everything with this file, and press Check. Expected: no syntax error. Beta 1b has never been pasted either, so this is the first paste of the app.
2. Start the app from the Application Library. The welcome page should appear, then `STARTVIEW(7,1)` should open the View menu, which is untested. Square-root law should appear before Help.
3. View → CLT dashboard → Uniform, with the defaults. Check:
   - the title reads **n = 1**, with "Esc = quit" complete at the right;
   - a **flat black line** lies across the blue bars;
   - three hint lines sit inside the magenta panel;
   - **six buttons** fill y 220-239 with labels centred, and "1 sample" fits its 51-px button;
   - "n−" shows the minus glyph.
4. Tap the top panel. Samples are drawn, and the first 20 land one at a time. The means are coloured green, orange and red. Row 206 reads "68% in 1 SE, 95% in 2 SE"; at n = 1 on a uniform population expect about 58% / 100%. The title reads "200 'means' of 1 member each".
5. Press n+ (or +) four times: n should go 1 → 4 → 16 → 64 → 100. n− goes back down. Left and Right step √n by one. Every step resamples.
6. **Watch one sample**, the main new feature. At n = 16, tap 1 sample:
   - red dots appear on the top axis;
   - a red bar with x̄ appears above them;
   - a red square falls in three steps;
   - one bar grows, with a red square on top;
   - the caption box appears.

   Tap 1 sample again: there should be no caption this time. Tap it once more and press a key during the animation: the animation should skip, and the key should not leave the dashboard. Also try +1, Down, and the lower-left corner of the top panel.
7. Tap a bar of means. The orange-edged box should give its interval, count and share, and the bar should be outlined in black. Tap the curve label to turn the curve off and on, then try the Curve button and the 0 key.
8. **Hold a population bar for about a second.** Its box should appear, and a quick tap should still resample. If holds feel unreliable, raise 600 ms in `cltTopPress` (line ~1695).
9. **Drag along the top panel**, the riskiest touch feature:
   - the ruler appears, n follows the finger, and the old means turn grey;
   - the blue curve narrows and rises before any data arrives;
   - lifting the finger resamples at the new n.

   Watch the G1 redraw speed during the drag; it redraws only when n changes. Drag with no means (pick a new population first): the curve alone should preview.
10. Menu → Square-root law, and View → Square-root law. Squares should sit on the σ/√n curve, and the table should list each n tried. Then New population → the law page should say "No n tried yet", and n should reset to 1.
11. Try every shape for the density line: Exponential (decaying), Normal, Bimodal (two humps), Geometric (flat pieces per bar), and data in D1 (no line).
12. Run Enter → Help through both pages and check the line spacing at 13 px. Esc on page 1 should go straight back.
13. Run Enter → Number of samples 2000 → n = 100 (menu item A). The title should read "600 of 2000 samples (quick)". The live frames take longer at large n.
14. **Plot key / Plot population / Plot sample means** are untested app features carried over from beta 1a: `H1`/`H2` with the `:24h` colours, `CHECK`/`UNCHECK` and `STARTVIEW(1,1)`. Also check that Num shows D2, including the means added one at a time.
15. Leave the app and look at Home's K: MAKELIST overwrote it, as before.

## (c) Not confirmed, or left as it was

- **What "+1" should do is not stated anywhere.** The brief names the button but not its action. It was taken to mean "add one mean at once", next to "1 sample", which is the animated version. If you meant something else, the change is in `cltButton`, one line.
- **The top panel's tooltip needs a 0.6 s hold, not a tap,** because the brief also requires a plain tap there to resample (item 6 above).
- The caption reads "the pile", not "the magenta pile", because the bars are now coloured by SE. It is two lines because one line would not fit at font 1.
- These constructs are not device-verified for this file: `CONCAT` onto the app column D2, a held MOUSE loop of up to 15 s inside an app, `EXP`, and font-1 text widths. The 6 px/char layout is an estimate, so the button labels and row 194 at 4 decimals (~300 px) need checking on the device.
- No MSGBOX was added, and nothing from the not-verified list is used: no FILLPOLY_P, TRIANGLE_P, WAIT(-1), second finger, 10-argument BLIT_P, DRAWMENU, Python, or whole-list MAX/MIN.
- MAKELIST still uses Home's K as its counter (house rule, pending GfxProbe T19).
- Sampling is unchanged; `PYTHON()` was not added.
