# PowerViz v2.4 — changes from v2.3

*16 October 2026 · the touch version, built on the v2.3 fix version. Every v2.3 fix is kept.*
*Source: `PowerViz_v2.3.txt` (898 lines) → `PowerViz_v2.4.txt` (1,823 lines, UTF-8, LF). Of the new lines, about 110 are the header and comment blocks.*
*Not yet run on hardware. "v2.3 nnn" is the old file and "v2.4 nnn" the new one.*
*Verification: `verify_PowerViz.py` (65 checks, all pass; output below).*

## (a) The changes, numbered as in the task list

**0. Groundwork (needed by every item below)**
- **One engine, `pv_Model(nv)`** (v2.4 470-519). This is the first half of v2.3's `pv_Setup` (v2.3 301-342), with n passed in. The formulas are byte-for-byte the same, with `NN` replaced by `nv`. The main view, the n₈₀ search and both curve views all compute power with it. `pv_Setup` (v2.4 551-587) now calls `pv_Model(NN)` and then runs the window logic.
- **Window hold, `WHLD`** (v2.4 230, 575-583). While a finger drags, `pv_Setup` never moves the x-window, even if a curve runs off the edge. It refits only the height, and only if the peak would clip (§6: freeze x, not y). The normal refit check runs after the finger lifts.
- **Per-frame clear**: `RECT_P(G1,0,0,319,239,cwht)` became `DIMGROB_P(G1,320,240,cwht)`, and `BLIT_P(G0,G1)` became `BLIT_P(G0,0,0,G1)`. This is the brief's verified idiom. It is used on the main view, the help pages and the curve views.
- **Plot moved up**: `PYT` 40→38 and `PYB` 162→146 (v2.4 199). The tick labels now sit at y 151-161, and the readout panel at y 162-217 (v2.3 178-225). The soft-key strip (218-239) therefore covers nothing.
- **Cache keys** `CK0`/`CK1` (v2.4 227, 833-843). A curve's column cache is reused when its centre, its SE and the window are unchanged:
  - while H₁ is dragged, H₀ is not recomputed, so a frame costs 297 `NORMALD` instead of 594 (measured in the harness);
  - while α is dragged, no curve is recomputed at all (0 calls after the first frame).
- New helpers: `pv_Same` (list equality with a flag), `pv_SinR` (sine in radians under any `HAngle`), `pv_NumS` (prints a number as it was typed, for the SE line) and `pv_GSave`.

**1. Showcase: drag H₁** (`pv_Touch` v2.4 1610-1732; live loop v2.4 1764-1800)
- The live loop polls `MOUSE` beside `GETKEY`. A touch goes to `pv_Touch`. Without a touch, the v2.3 key paths run as before, including `kk == 7 OR ISKEYDOWN(7)`.
- A press inside the plot box that is nearer the H₁ centre than the H₀ centre grabs H₁.
- Each drag sample sets the alternative to `XMN + (x − PXL)·span/(PXR − PXL)`, snapped to the `pv_EffStep` grid with `ROUND(ROUND(v/es,0)·es,6)`:
  - for the 2-sample tests the axis is the difference, so μ₂ = μ₁ + v and p₂ = p₁ + v;
  - proportions are clamped to 0.02-0.98.
- The frame is redrawn only when the snapped value changes (`pv_Setup` + `pv_Draw` from the caches).
- The status line reads "H₀ stays put; H₁ follows your finger".
- The POWER colour thresholds (0.5 and 0.8) are unchanged.
- After the lift there is a capped `pv_TDrain`, `WHLD` returns to 0, and the window refits only if a curve would leave the frame.
- **One deviation from the brief, on purpose**: a press within 6 px of the critical line grabs α *unless* it is nearer H₁'s dotted centre line than the dashed line. At the default scene the two lines are only 4.6 px apart, so a finger placed squarely on the H₁ peak would otherwise grab α (v2.4 1655-1661).

**2. Drag the dashed critical line**
- `pv_Draw` records each line's pixel x in `CLX` (v2.4 950-965). A press within ±6 px of a line grabs α.
- Upper line: `AL := 1 − NORMALD_CDF(M0v,SE0,x)`. Lower line: `NORMALD_CDF(M0v,SE0,x)`. When the test is 2-sided the result is doubled: the dragged side sets α/2 and the other side mirrors it. α is clamped to 0.001-0.5.
- While dragging, the status line shows `pv_ADrag()`: "α = 0.040 (off the ladder)", or "α = 0.048 (lift: snaps to 0.050)" when within 15 %.
- On lift, `pv_ASnap()` snaps to the nearest rung if it is within 15 % (relative to the rung) and says "snapped to the ladder". Otherwise it keeps the custom α and says "kept as a custom value (off the ladder)".
- `pv_AStep` (new; used by +/- and the soft keys) moves from a custom α to the next rung above or below. From a rung it behaves exactly like v2.3's `AIDX±1`.

**3. Vertical drag for n**
- After more than 8 px of movement, a drag with |dy| > 2|dx| becomes an n-drag, whatever was pressed.
- n moves one `pv_StepN` step per 12 px, measured from the press: finger up means larger n, so 50 px up takes n from 30 to 50.

**4. Soft keys**
- `DRAWMENU({"Edit","Tails","α−","α+","Pow-n","Menu"})` is called after every main-view blit (v2.4 1043). A tap with y ≥ 218 is slot `MIN(6, IP(x/53.4)+1)` and goes to `pv_Soft` (v2.4 1584).
- The footer legend (v2.3 543) is dropped from the main view while the strip shows, as ChiTable does. Every label's y was checked in the harness for all four tests: each ends above y 218 and inside its column.
- **The "More" convention** (BRIEF_TOUCH, last section) was considered and **not applied**. The main view has exactly six actions, and every other feature already has a route: the Menu covers the effect-size view, change test and help; 0 refits the window; the arrows step. CLAUDE.md says the same: "a screen whose actions fit in six gets no More".

**5. Tap a readout cell**
- `pv_Draw` records five hit boxes in `HX1/HY1/HX2/HY2/HACT` (v2.4 1027-1031), using the same numbers as the text.
- **n** opens `pv_EditN`, a one-field INPUT into a LOCAL, with the v2.3 clamp message.
- **μ₁/p₁** and **d/h** open `pv_EditEff`, a one-field form; a proportion gets the clamp box.
- **α** and **zcrit** open `pv_AChoose`, the v2.3 alpha CHOOSE, now shared with the menu.
- The β, SE and POWER cells are not tappable.

**6. n₈₀**
- `pv_N80` (v2.4 522-549) finds the smallest whole n from 2 to 5000 with power ≥ 0.80, using `pv_Model`.
  - It bisects (about 13 engine calls) instead of stepping n one at a time, because it reruns on every drag sample that changes the effect or α.
  - It returns 0 for "no effect" and −1 when n = 5000 falls short.
  - `pv_Setup` reruns it only when one of TT, TL, AL, MM0, MM1, SG, PP0 or PP1 changed (key `N8K`).
- It is printed in green in the panel at (228, 206): "n₈₀ = 56", "n₈₀ > 5000" or "n₈₀: no effect".
- The power-vs-n sweep records the first column at 0.80, then steps n down with the same engine to the first whole n (`PN80`). The view draws a green dotted vertical there, labelled "n₈₀ = 56".
- Sweep, panel and brute-force SciPy agree for all four tests (56 / 112 / 153 / 305 at the defaults).

**7. Power-vs-n view: drag to choose n** (`pv_PowNView` v2.4 1204-1286; `pv_PCDraw` v2.4 1064-1202)
- The 250 powers are cached in `PWC`, one *whole* n per column: `pv_NofC(c) = ROUND(2 + c/250·(PNMX−2))`.
- The range is now max(200, 1.25 n, 1.25 n₈₀), capped at 5000, so n₈₀ is always on screen.
- A touch in the plot box follows the finger and redraws from the cache only. A red marker rides the curve, the current-n marker turns grey, and the footer reads "at n = 114: power = 0.972, lift = use this n". On lift that n is adopted and the program returns to the main view.
- A key returns unchanged. Esc while the finger is down lets go without choosing.
- The x ticks now use the curve's own n→pixel map. v2.3 placed them with `i2/nmax`, a pixel or two off.
- The subtitle (v2.3 568-569) ran to about 338 px. It is now "μ₁ = 105, d = 0.33, small, α = 0.050, 1-sided" at x 4, with the test name on the title line.

**8. Power-vs-effect-size view (new, Menu item "Power vs effect size")** (`pv_PowEView` v2.4 1288-1321)
- Effects d (or h) from 0 to 1.5 are swept in the direction of the current effect, at the current n and α:
  - means: μ₁ = μ₀ + d·σ;
  - proportions: p₁ = sin²(asin√p₀ + h/2), and the curve stops where p₁ would pass 0.98 (214 of 250 columns at p₀ = 0.5).
- Cohen's 0.2/0.5/0.8 are dotted grey with the words small/medium/large, and a red marker shows the current effect.
- The effect is restored afterwards. The view uses the same `pv_PCDraw` layout as the power-vs-n view.
- Menu items: Edit values, Toggle 1/2-sided, Set α, Power vs n curve, **Power vs effect size**, Change test, Help, Return to plot. No numbers; the dispatch indexes were shifted to match.

**9. Area labels inside the fills** (v2.4 971-1004)
- The fill pass sums the centroid of the yellow region (β; columns in the acceptance region, height PYB − y₁).
- It also sums the *visible* green: H₁'s band above H₀, on H₁'s side only.
- "β = 0.43" (grey) and "power = 0.99" (green) are drawn at the centroids, kept inside the region at that column.
- A label is suppressed when fewer columns of its region are at least 11 px tall than the label's estimated width (5 px a character).
- At the defaults (n = 30, μ₁ = 105, power 0.57) both labels are suppressed: the tall part of the yellow is about 30 px wide. Low-power scenes show β and high-power scenes show power (harness survey of 16 scenes).

**10. Ghost of the previous H₁**
- `pv_GSave` (before an arrow step, and when an H₁ or n drag begins) asks the next frame that recomputes H₁ to copy the old column values into `CYG` while it overwrites `CY1` (v2.4 860-866). That costs no extra NORMALD and no extra loop.
- The ghost is drawn in pale magenta RGB(235,160,235) under the outlines, only while the window matches the one the ghost was drawn in.
- It shows on every frame of a drag and on the lift frame, then is cleared. For key steps it lasts one frame.
- The copy is element-by-element on purpose: the harness aliases lists on `:=`, and an element copy is unambiguous on the device too.

**11. Teaching lines**
- The SE₀ cell became a full-width line at y 206, built by `pv_SELine` (v2.4 632-655):
  - "SE₀ = σ/√n = 15/√30 = 2.74"
  - "SE₀ = σ√(2/n) = 15√(2/30) = 3.87"
  - "SE₀ = √(0.5×0.5/100) = 0.0500"
  - "SE₀ = √(2×0.55×0.45/100) = 0.0704" (pooled p̄)
- `pv_DLbl` prints "d = 0.33, small" using `pv_EffWord`. The thresholds are 0.2/0.5/0.8, and "tiny" below 0.2. The word is taken from the value rounded as shown.
- `pv_Tails` (soft key or menu) sets a one-frame callout over the plot top, for example:
  - "2-sided: α = 0.050 is split, 0.025 in each tail," / "so the critical z is 1.960 instead of 1.645."
  - "1-sided: all of α = 0.050 sits in one tail,"

**12. Help** (`pv_ShowHelp` v2.4 1461-1505)
- Page 1 has the soft keys, the keys, the Cohen benchmarks and the meaning of SE₀.
- Page 2 has the three drags, the readout taps, the colours (ghost included) and n₈₀.
- Any key or a tap moves on (`pv_WaitAny`). Every v2.3 help line is kept, some reworded to fit.

**Header**: v2.4 banner; the "v2.4 — what changed" list above the kept v2.3 list; the firmware line says v2.2-v2.4 have not run; the LIVE CONTROLS / SOFT KEYS / TOUCH / DISPLAY comment block updated.

**Left as instructed:** every routine head stays `LOCAL pv_Name()`. The 24 new routines use the same form, so if LocalHeadProbe rejects it, one mechanical edit (remove "LOCAL " from the 49 routine heads) fixes the whole file. A copy edited that way **parses OK with 49 functions** in the kit interpreter.

## Verification (verify_PowerViz.py, harness ppl_run_v1)

```
A. power = statsmodels NormalIndPower (z tests, 108 cases)         max diff 1.8e-15
   power = statsmodels power_proportions_2indep (36 cases)          max diff 3.9e-16
   n80 = ceil(statsmodels solve_power) = brute force: 56, 71, 112, 142
B. program engine in the harness, 216 scenarios (4 tests x tails x alpha x n x effect):
   power max diff 1.7e-16; n80 = brute force in every scenario
C. H1 drag: mu1 snapped to the finger (112), power = SciPy, H0 label fixed in every frame,
   POWER orange -> green, ghost 296 segments per drag frame, 297 NORMALD per drag frame
   POWER colours red/orange/green at < .5 / .5-.8 / >= .8 across a drag
   alpha drag: AL = 1 - Phi((x-mu0)/SE0) = 0.03975 = SciPy; "α = 0.040 (off the ladder)";
     custom kept on lift; power at custom alpha = SciPy; 0 NORMALD after frame 1
   alpha drag near 0.05: "α = 0.048 (lift: snaps to 0.050)" -> snapped
   2-sided lower line: 2 Phi(...) = 0.01097 shown "α = 0.011 ...", snapped to 0.01 (9.7 %),
     upper line mirrors; Tails callout "so the critical z is 1.960 instead of 1.645."
   vertical drag 50 px up: n 30 -> 50, power = SciPy; down: n decreases
   plain tap in plot: nothing moves, gesture hint shown
   soft keys α+, α−, α−: .05 -> .10 -> .05 -> .02; DRAWMENU labels; Tails; Edit; Menu -> Help (2 pages)
   readout taps: n -> 64 (one-field form); d cell -> mu1 108; α -> 0.01; p1 0.99 -> 0.98 + box
   Pow-n drag: adopts the column's n (114); footer power 0.972 = SciPy; 250 cached values = SciPy;
     n80 label "n₈₀ = 56" green = panel = brute force; tests 2-4: 112 / 153 / 305 agree
   effect view tests 1 and 4: 250 cached powers = SciPy (214 drawn for proportions), effect restored
   two proportions H1 drag: p2 = p1 + axis value on the 0.01 grid; power = statsmodels
   area labels: "power = 0.99" in the green (n 60, mu1 108); "β = 0.84" (n 10, mu1 103)
   SE lines for all 4 tests and Cohen words (small, large) as listed above
   layout, 4 tests: every main-view label ends above y 218 and inside its column
0 failure(s)        (65 PASS)
```
Stale-key mode (each dialog's OK/Cancel left in the key buffer) was also run on menu → Pow-n, menu → effect view, menu → Help, the n-cell tap and Pow-n tap-to-pick: no page skipped, no script left over.

## Gate (final run)

```
=================== PowerViz_v2.4.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
      3 E1     132 E7      14 E9
--- 2. ppl_check_v2 tally (ORIG) ---
     71 E7       5 E9
--- 2b. ppl_check_v2 HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
836 checks, 5 problems
  PROBLEM line 189: file-level LOCAL declares 7 names (max 6)
--- 4. full parse (kit interpreter) ---
PowerViz_v2.4.txt                PARSE FAIL PPLError: <ppl>:185: expected a name after EXPORT
   ORIG: PowerViz_v2.2.txt                PARSE FAIL PPLError: <ppl>:74: expected a name after EXPORT
--- 5. line count, size ---
1823 lines, 64822 bytes
```
- **The E1/E7 tally grew. Every one of those lines is the routine-head form**, not a defect. `ppl_check` does not read `LOCAL pv_Name()` as a routine head, so every LOCAL inside one shows as undeclared (E7), and an indexed list LOCAL (`waM(1)`, `tm(1)`, `tm1(1)`) shows as a call (E1). On the bare-head copy the tally is **0 E1, 0 E7, 14 E9**, the parse is **OK (49 functions)** and there is **0 W**.
- The 14 E9 are all `STRING(n,1,0)` on integers, the documented form.
- The lint "7 names" at 189 is `ALAD:={…7 values…}`, a single name. The same false positive appeared in v2.2 and v2.3.
- The parse failure is the kit's known limit: it cannot read file-level LOCAL after an EXPORT list. The v2.2 original fails the same way.
- Other lint lines are the known EXPORT-discipline noise.
- `fleet_names_v2.py` over `out/*.txt` reports 0 untagged, 0 mixed-tag files and 0 built-in matches. Every new `pv_` name collides only with PowerViz v2.3, the same program. All names are defined before use (scripted check).

## (b) DEVICE TEST CHECKLIST (G2 first, then G1), least → most risky

1. **Paste.**
   - If the editor stops on a `LOCAL pv_…(` line, the routine-head form is the problem: run LocalHeadProbe, then strip "LOCAL " from the 49 heads.
   - A stop anywhere else is new: tell Claude the line.
2. **Run `POWERVIZ`, One-Sample Mean, OK.** Check the first frame:
   - title; a blue status line "Drag H₁, the dashed line (α), or up/down (n)" in place of the colour chips;
   - plot down to y ~146 with tick labels under it; orange panel ending just above the strip;
   - the strip reads Edit, Tails, α−, α+, Pow-n, Menu.
   - **Check the glyphs:** α and the minus in the strip; **√** in "SE₀ = σ/√n = 15/√30 = 2.74"; **₈** in "n₈₀ = 56".
   - If √ or ₈ shows as a box, change only `SQG` / `N80L` in `pv_Init` (comment there).
3. **Panel numbers** (SciPy): POWER **0.572** orange; β = 0.428; zcrit = 1.645; "d = 0.33, small"; "n₈₀ = 56" green. Check that nothing overlaps: the d cell's right edge against the big number, and the SE line against n₈₀.
4. **Keys unchanged.**
   - Right/Left step μ₁ by 1, and a pale magenta ghost of the old H₁ shows for one frame.
   - Up/Down step n (30 → 35); hold an arrow and it repeats.
   - +/- step α; 0 refits; Enter opens the menu; Esc ends with the 5-line box.
5. **Soft keys (taps).**
   - α+ → 0.10, α− → 0.05.
   - Tails → 2-sided, with a one-frame orange-framed callout "2-sided: α = 0.050 is split, 0.025 in each tail, / so the critical z is 1.960 instead of 1.645." Its two lines must fit the box.
   - Edit → the full form; Menu → the 8-item menu; Help → two pages (tap or key moves on).
   - **Confirm a soft-key tap does not also act on the plot.**
6. **Readout taps.**
   - Tap "n = 30/grp" → a one-field form; enter 64.
   - Tap "μ₁ = 105" or "d = …" → the μ₁ form.
   - Tap "α =" or "zcrit =" → the alpha list.
   - After each, the plot redraws and Enter does not reopen the menu.
7. **Power vs n** (soft key Pow-n).
   - The curve, a green dotted line at **n₈₀ = 56**, and the footer "at n = 30: power = 0.572, touch = pick n, key = back".
   - A key returns.
   - Open it again, **touch the curve and slide**: a red marker rides it, the old marker turns grey, and the footer reads "at n = …: power = …, lift = use this n". Lift → the main view shows that n.
8. **Power vs effect size** (Menu → item 5). Curve from d = 0 to 1.5, small/medium/large dotted, red marker at 0.33, power 0.572. Any key or tap returns. Try Two Proportions too: the curve stops early near h ≈ 1.29.
9. **Vertical drag.** Put a finger mid-plot and slide up about 50 px: n goes 30 → 50 in steps, with "n = … per group: drag up = larger n" on the status line. Slide down: n falls. H₀ must not move sideways.
10. **Drag H₁** (the showcase).
    - Press **on the magenta H₁ peak**, which must grab H₁, not α (the tie-break), and slide right: H₁ follows, red/yellow/green re-shade, POWER turns green past 0.80, and H₀ stays put.
    - The pale ghost shows where H₁ started. On lift the window may refit if H₁ went near the edge.
    - **Watch the G1's frame rate**: each frame is 297 NORMALD plus about 900 LINE_P.
11. **Drag the critical line.**
    - Press on the dashed red line (a little right of H₁'s centre) and slide right: "α = 0.040 (off the ladder)"; red shrinks, yellow grows, green shrinks. Lift → "kept as a custom value".
    - +/- from there → the next rung.
    - Repeat ending near 0.05: "lift: snaps to 0.050" → "snapped to the ladder".
    - With 2-sided on, drag the left line: both lines move symmetrically.
12. **Area labels.** Edit to n = 10, μ₁ = 103: "β = 0.84" sits inside the yellow. Edit to n = 60, μ₁ = 108: "power = 0.99" sits inside the green. The defaults show neither (too narrow). **Font-1 widths are estimated at 5 px a character**: look for a label spilling over its region's edge. If one does, the fix is `lw:=6*DIM(lbs)` (two places).
13. **Stuck-touch escape.** During a drag, press Esc: the drag ends (the program does not quit).
14. **Exit** with Esc: the summary box, then `RETURN PW` to Home. Home's K is overwritten by the MAKELIST counter, which is expected.
15. Repeat 2-11 on the G1.

## (c) Not confirmed / left as it was

- **`LOCAL pv_Name()` routine heads**: kept, per instruction (LocalHeadProbe decides).
- **Glyphs not on the verified list**: √ (CHAR 8730, GfxProbe T14 e) and subscript 8 (CHAR 8328, not probed). Both live in one line each in `pv_Init`. The `α−` label uses U+2212 (listed as verified in CLAUDE.md); its rendering inside DRAWMENU is not separately confirmed.
- **Text widths** are estimates (the harness uses ~5.5 px a character for font 1). The status hints are at most 52 characters, and the help page lines at most 52.
- **MOUSE during a drag** is modelled in the harness as one reading per call. The real sample rate, and what MOUSE returns while a finger rests still, are untested. The drag loop redraws only on a changed value, and treats an off-screen reading as a lift.
- **The tie-break in item 1** goes beyond the brief's "±6 px grabs α". It is easy to remove (v2.4 1655-1661) if Roger prefers the literal rule.
- **The "More" soft-key page** was not used: all six actions fit (see item 4).
- **`!=` in `pv_FMTP`**, **`pwv`** removal, and the exit MSGBOX + `RETURN PW` are untouched from v2.3. `pwv` disappeared with the rewritten `pv_PowNView`.
- No user guide exists for PowerViz in the repo, so none was written.
