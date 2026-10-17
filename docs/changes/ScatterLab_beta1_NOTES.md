# ScatterLab beta 1 — notes

*16 October 2026. NEW program, not yet run on hardware. Pure PPL (the regression is a few O(n) passes; nothing here would gain from MicroPython).*

Files: `ScatterLab_beta1.txt` (the program, 1,525 lines, ASCII, LF), `scatterlab-guide_beta1.md` (student/instructor guide), `verify_ScatterLab.py` (SciPy comparison + harness runs), this file.

## 1 · What it does

A scatterplot built with the finger. Tap empty plot area to add a point (40 at most); press a point and drag it, and the least-squares line, r, r², SSE and the orange residual segments are recomputed and redrawn on every drag sample while the window stays frozen. Everything is composed in G1 and shown with one blit; `DRAWMENU({"Add","Del","Resid","Guess","Data","Menu"})` is painted after every blit.

| Part | What it is |
| --- | --- |
| Plot | box x 30–222, y 20–176; nice ticks (1/2/5 × 10^k), grid, labels thinned when they crowd; default window 0–10 × 0–10 |
| Points | 5 × 5 blue `RECT_P`; selected point framed red, the far-out point framed orange |
| Lines | least-squares line magenta (2 px, clipped to the box); Guess line red; mean point a green cross |
| Panel | n, r, r², y-hat = b₀ + b₁x with its numbers, SSE, x̄, y-bar, mode, residuals on/off; in Guess the student's line, its SSE, the least-squares SSE and a Reveal button |
| Notes | two lines under the plot: the last action's message, else the selected point's coordinates, residual and leverage h, else the mode's hint; line 2 the key legend in house form, or the leverage sentence while a far-out point exists |
| Guards | n < 3 or every x equal → "need at least 3 points with different x" instead of r and the line; every y equal → flat line, "r undefined" |
| Soft keys | Add / Del set the tap mode; Resid toggles residuals; Guess toggles Guess mode; Data and Menu open CHOOSE lists |
| Guess | handles at 20 % / 80 % of the window width (x = 2 and 8 in 0–10), starting level with y-bar so "your SSE" starts at SST; dragged up/down; Enter or the panel button reveals/hides the LS line |
| Far-out point | Menu item 1: a point ON the LS line at x̄ + 3 SD (at least one tick past the last point); the window widens if needed. Its note says dragging it swings the slope and a point near x̄ barely moves the line; the live line 2 says "High leverage (h > 4/n)" or "Near x̄ … no tilt" for whichever point is selected |
| Data | SYNTHETIC example (16 made-up counties, poverty % vs property crimes per 1,000; label and note say so), load from C1/C2 (IFERR; the message says the columns exist only after Statistics 2Var has been opened once), save to C1/C2 (then "open Statistics 2Var yourself"; no `STARTAPP`), clear |
| Help | six drawn pages: r, r² as share explained, residuals and least squares, leverage, correlation is not causation (ice cream and assaults follow temperature; county poverty and crime; ecological fallacy; the example is synthetic), touch/keys/2Var |
| Home | `SL_N SL_B0 SL_B1 SL_R SL_R2 SL_SSE`, updated on every fit; `RETURN "ScatterLab: n = 16, y-hat = 16.64 + 1.020 x, r = 0.7512, SSE = 422.7"` |

Keys (all verified codes): +/− select the next/previous point; arrows move it one tick (Guess: ←/→ pick a handle, ↑/↓ move it a fifth of a tick); 0 fits the window; Enter = menu (Guess: reveal/hide); Esc leaves Del or Guess, and quits from Add; **any key ends a drag**.

**Tag `sl`** (glued style: `slFit`, `slDraw` …); 48 routines, all tagged.

## 2 · Decisions you may want to change

1. **Keyboard parity.** The soft keys produce no key code, so the Enter menu also carries Residuals, Guess, Data, **Type a point (x, y)** and **Delete the selected point** — nine items in all. Without them a keyboard-only user could not add, delete, guess or load.
2. **Two refits besides Fit.** The window refits when the far-out point or a typed point would land outside it (both are deliberate requests, and the alternative is a point off screen). Never during a drag, never on a tap.
3. **y-hat and y-bar are spelled out.** No ŷ / ȳ glyph is verified. `ŷ` appears in the corpus (`regress10.zip::Regress.hpprgm`, Schrausser's `CIXY.pas`) but not in our confirmed list, so both strings live in `slYHAT`, `slYBAR` in `slInit` — one line each to change after GfxProbe T14.
4. **Arrows move one whole tick** (as specified). In the example window a tick is 5 units, which is coarse; the handles use a fifth of a tick. One expression in `slNudge` changes it.
5. **Handles move vertically only**, x fixed at 20 % / 80 %. Any non-vertical line is reachable that way, and the handles can never meet or make a vertical line.
6. **In Guess mode the residuals go to the student's line** (that is what "your SSE" adds up). Outside Guess they go to the LS line.
7. **Tapped and dragged points snap** to one decade below the tick step (0.1 in the default window and the example), so C1/C2 receive 12.3, not 12.2947. A drag moves the point by the finger's displacement in data units, so an axis the finger did not move along is left exactly as it was (a pure vertical drag keeps x).
8. **Hit radius** `slHit := 7` px (as specified) and `slHitH := 10` for handles, both in `slInit`. 7 px is about 1.6 mm on the Prime's screen — fine with a stylus, tight with a finger; widen it if the first run says so.

## 3 · Gate (final)

```
=================== ScatterLab_beta1.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
                                   (empty: no E or W codes at all)
--- 2b. HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
910 checks, 6 problems  -- all six are the known noise: 'no function named
   ScatterLab_beta1', 'entry point ScatterLab_beta1 not EXPORTed', and four
   EXPORT-discipline lines about SL_N / SL_R / ScatterLab
--- 4. full parse (kit interpreter) ---
PARSE FAIL <ppl>:124: expected a name after EXPORT   -- the kit's known limit
   (file-level LOCAL after an EXPORT list); ChiTable beta 1k and GaltonBoard
   beta 1b fail the same way.  The harness's own parser reads the whole file
   and runs it (section 4).
--- 5. ---
1525 lines, 55853 bytes; no non-ASCII in code
```

`ppl_gate_v1.py`: ppl_check_v3 clean, lint 910/6 (noise), **RESULT: PASS** (its kit steps skip here: the zip is not beside it).

**Fleet names** (`fleet_names_v2.py`): over the newest version of every program in `out/` (23 files including ScatterLab): **0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches**. Over every `out/*.txt` at the time of writing (31 files): 121 collisions, every one between two versions of the same program (e.g. NormExplorer beta 41 / 42) and none involving an `sl` name. One E11 was caught and fixed on the way: `LOCAL lcM` is `LCM`.

## 4 · Verification (`python3 verify_ScatterLab.py` — ALL CHECKS PASSED)

```
Part A: the PPL formulas, written out in Python, against scipy.stats.linregress
   234 data sets; worst |error|: slope 4.8e-15 (rel), intercept 1.2e-15 (scaled),
   r 5.6e-16, SSE 1.5e-15 (/SST), leverage 4.5e-14
   guard  vertical: every x equal                   -> no line (scipy slope nan, r nan)
   guard  vertical, x = 0.1 (mean not exact)        -> no line (scipy slope 10.67, r 1.2e-16 !)
   guard  n = 2 / n = 1 / n = 0                     -> no line
   flat   every y equal (5 and 0.1)                 -> b1 = 0, b0 = y, r undefined (scipy r nan / 0.0)
   centring: x = 1,000,000.1 .. .5: Sxx centred 0.100000000023,
             naive sum x^2 - (sum x)^2/n 0.0996 (true 0.1)
   SYNTHETIC example: n = 16, x-bar = 16.30, y-bar = 33.25625, b0 = 16.636242,
             b1 = 1.019632, r = 0.751215, r^2 = 0.564324, SSE = 422.7364, SST = 970.2994
Part B: the PPL routine slFit itself, run on the harness (ppl_run_v1)
   234 data sets through the PPL: worst relative difference from SciPy 5.3e-15
   guards and flat sets: as Part A; slGuessFit matches; flat starting guess SSE = SST;
   slSnap, slNice right on known cases; example window x 5-30, y 15-50, ticks 5, snap 0.1
Part C: scripted sessions through the whole program (no runtime error anywhere)
   taps, drag, keys              23 frames            -> n = 3, r = 0.9922 (= SciPy)
   example, Guess, far point     19 frames, 3 dialogs -> far point x = 34.1, h = 0.399 (4/n = 0.235)
   leverage demonstration        far point (h = 0.40) down 15: b1 1.0195 -> 0.7149;
                                 point at x = 16.0 (h = 0.06) down 15: b1 0.7149 -> 0.7394
   guards, Del, C1/C2, help      30 frames, 10 dialogs; all 6 help pages; MSGBOXes <= 5 lines
   40 points, cancels            87 frames; the 41st tap refused with a note
   load before 2Var opened       the IFERR message
   routines reached: 48 of 48
```

Data sets: random n = 3–40 at three scales and offsets, integer x with ties, n = 3 exactly, crime-count-sized y (≈ 3,000–6,000), x as years (2000–2024), two distinct x values, perfect ±1 lines, the example. The vertical x = 0.1 case is the reason the guard tests the **range** of x rather than Sxx: SciPy happily returns a slope of 10.67 from rounding dust there. The harness runs the PPL with Python doubles, so Parts B and C check the program's logic and flow, not the Prime's own 12-digit arithmetic.

## 5 · Device test checklist — least risky first

1. **Paste and compile** in the Connectivity Kit; run `ScatterLab()`. Expect the empty 0–10 plot, "n = 0" and the red "need at least / 3 points with / different x" in the panel, the green hint "Tap the plot to add points, or Data = example.", and the six soft keys. Esc quits; Home shows "ScatterLab: n = 0, no line (…)".
2. **Glyphs.** Data → Poverty vs crime (SYNTHETIC). Check x̄ (CHAR 57344), r² (CHAR 178), the subscripts in help page 3 (b₀, b₁) and ⇆⇅ in the legend all render. Top label in orange: "SYNTHETIC: x poverty %, y property crime /1000".
3. **Numbers** on the example: n = 16, r = 0.751, r² = 0.564, y-hat = 16.64 / + 1.020 x, SSE = 422.7, x̄ = 16.30, y-bar = 33.26; window 5–30 × 15–50 with ticks every 5. Then compare with the Prime's own Statistics 2Var on the same data (step 10).
4. **Keys only** (no touch): + selects point 1 (red frame, note line "Pt 1 (10.4, 34.4): resid …, h = …"); arrows move it one tick (5 units here) and the line follows; − selects backwards; 0 refits; Enter opens the nine-item menu; Esc quits.
5. **Soft keys**: Resid draws orange segments and the note explains them; Del then a tap on a point removes it ("Point deleted: n = 15"), a tap on empty plot says "No point there"; Add returns. Esc in Del returns to Add (does not quit).
6. **Tap to add** on an empty 0–10 plot (Data → Clear first): three taps make three points that land under the finger, and the line appears with the third. Watch whether 7 px is a comfortable grab radius for a finger (`slHit`).
7. **Drag a point** — the main event. Press a point and slide: the point, line, r, r², SSE and residuals should follow on every sample. Note the smoothness **on the G1** (≈ 70–90 drawing calls per frame with residuals on; the soft-key strip is repainted per frame — watch for strip flicker). A tap without movement only selects. Press, slide, and press any key mid-drag: the drag ends.
8. **Guess**: handles appear at x = 10 and 25 in the example window, level with y-bar; "your SSE" = 970.3 (= SST); drag each handle; Enter reveals the magenta line and "No line has a smaller SSE than least squares."; tap the panel button to hide/reveal; ←/→ pick a handle, ↑/↓ move it; Esc leaves Guess.
9. **Far-out point**: Enter → Add a far-out point. Window widens to 0–40 × 15–55; orange-framed point at (34.1, 51.4); the two orange note lines. Drag it straight down ~15 units: b₁ ≈ 1.02 → 0.71 and line 2 reads "High leverage (h > 4/n): it swings the slope."; drag the point at x = 16.0 down: b₁ barely moves and line 2 reads "Near x̄: the line barely moves (no tilt)."
10. **Save to C1/C2**: Data → Save. Message (4 lines). Quit, open Statistics 2Var yourself: C1/C2 hold the points (16 or 17 rows). Fit Linear there and compare r, b₀, b₁ with step 3.
11. **Load from C1/C2**: edit a value in the 2Var Num view, run ScatterLab, Data → Load: the edited data appear, window fitted, label "From Statistics 2Var: x = C1, y = C2". More than 40 rows: only the first 40, with a red note.
12. **Help**: six pages; check no line is clipped on the right (the longest lines are 46 characters), the footer "1/6 ←→ or tap = page, Esc = plot", tap left/right halves, Esc returns to the plot.
13. **Edge cases**: Type a point (Menu) outside the window → the window refits and says so; Cancel on the form changes nothing; 40 points then a tap → "40 points is the limit"; three points stacked on one x → the guard; all y equal → "r undefined: every y equal" and a flat line.
14. **Home after Quit**: `SL_N`, `SL_B0`, `SL_B1`, `SL_R`, `SL_R2`, `SL_SSE` match the last screen; `K` holds 40 (the `MAKELIST` counter, as in every fleet program until GfxProbe T19).
15. *(Only if a calculator is available where Statistics 2Var has never been opened, or after a full reset)* Data → Load: the "C1 and C2 hold no data yet" message, no error; Data → Save: "Could not write C1 and C2", no error.

## 6 · Not confirmed — stated plainly

- **Nothing here has run on a Prime.** Every construct is copied from device-run fleet code (ChiTable beta 1k's drain/wait/soft keys/palette/file-level LOCAL; NormExplorer's MOUSE-drag polling and its `IFERR … SIZE(C1)` read), but the combination is new.
- **Drag frame rate on the G1** is unmeasured. If it lags: draw the static grid and labels once per window into G2 and start each frame with `BLIT_P(G1, 0, 0, G2)` (GaltonBoard's pattern — itself not yet device-run), or skip the residual segments during a drag.
- **Writing C1/C2** from a standalone program: Lessons Learned §10 says data columns are reachable and writable (D1/D2 seen); C1/C2 writes appear in corpus programs (`sir.hpprgm.txt`, `RKF1`, `AASHTO T-180`), but ScatterLab's own write is untested. It is inside `IFERR`.
- **The IFERR path when C1/C2 do not yet exist** has never been observed by us on this firmware (step 15).
- **DRAWMENU repainted on every drag sample** — ChiTable repaints it every frame of its grid, but never at drag rate.
- **Text widths** are estimates (font 1 ≈ 6.5 px/char): the panel lines are ≤ 13 characters in 86 px, the longest note and help lines 46 characters (ChiTable shows 48 on the device).
- **Statistics 2Var wording** in the save message ("Symb picks the fit, Plot draws it, Stats shows r") is general on purpose; it has not been checked against the 2026-09-09 app screens.
- The harness runs the arithmetic in IEEE doubles; the Prime's Home arithmetic is not reproduced. The centred two-pass sums are what keep it safe at classroom scales.

## 7 · Library check (D:\HP-Prime index, 16 Oct 2026)

- `ŷ` (U+0177): two hits (Regress.hpprgm, Schrausser CIXY.pas) — corpus-used, not verified; not used.
- `C1:=` from a program: sir.hpprgm.txt, RKF1, AASHTO T-180, Bode Plot — corpus-used; used inside IFERR.
- `IFERR … MIN(SIZE(C1), SIZE(C2))`: NormExplorer beta 40 (device-run program), copied exactly.
