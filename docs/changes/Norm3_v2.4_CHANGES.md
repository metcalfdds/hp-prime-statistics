# Norm3 v2.4 — changes from v2.3 (the first touch version)

*16 October 2026. Source: `Norm3_v2.3.txt` (382 lines) → `Norm3_v2.4.txt` (816 lines). **Not yet run on hardware.** Written against Lessons Learned v7f, CLAUDE.md (16 Oct), BRIEF.md + BRIEF_TOUCH.md and Fleet Review §6 (Norm3/Burr3). Every v2.3 fix is kept (pdf cache, launch drain, LOCAL lines ≤ 6, tagged ASCII names, house orange, centred tick labels, "P(X ≤ x₀)" wording).*

Line references are **v2.3 → v2.4**.

## 1 · Changes

1. **Drag x₀ (showcase).** The single key wait (363) is replaced by a poll of GETKEY and MOUSE together (622-647). A finger inside the plot box sets x₀ from its pixel column with the drawing's own map, `x = xmin + (px − LFT)/W·(xmax − xmin)` (700-704; constants 328). The blue area, the light-red complement, both P values, row 2 and the magenta point on the S-curve all follow it. They are redrawn from the cached lists, so an x₀ drag costs 2 NORMALD-type calls a frame. A finger that rests redraws nothing: the poll waits for the position to change or for the lift (636-641, the NormExplorer beta 41 lesson). On lift, x₀ snaps to `n3_NiceNum(width/100)` (0.1 on N(0,1), 1 on N(100,15)) and stays inside the window (741-746). The lift goes through the capped `n3_Drain()` (236). A key pressed while a finger is down ends the hold, as a way out of a stuck touch.
2. **Tap the S-curve for the inverse.** In views 0 and 2, a press that is **on** the S-curve is the inverse. "On" means within 16 px vertically and nearer the S-curve than the pdf in that column, read from the caches (668-680). A press on the new right-hand 0-1 axis is the inverse too (683-686). p is the finger's height on that axis, rounded to 0.01, with 0.025 and 0.975 caught within 0.0035. p is clamped to the part of the curve on screen, then `x₀ := NORMALD_ICDF(mu, sd, p)` (705-728). A drag continues along the curve. Row 2 reads `p = 0.900 → x₀ = 1.28, z = 1.28`.
   - *Two deviations from the brief's literal wording, both found by the harness.* (a) The brief says only "nearer the CDF than the pdf". Near μ the S-curve crosses half height, so under that rule alone every press low in the middle of the plot became an inverse, and x₀ jumped to a quantile instead of the finger. The 16 px "on the curve" test fixes this. (b) The brief's example implies a 0.005 grid. With H = 153 px one pixel is 0.0065 of p, so a 0.005 grid cannot reach 0.500 or 46 other values (verify_Norm3.py 2c). A 0.01 grid reaches every value, and 0.025/0.975 are added specially.
3. **Right-hand CDF axis.** In the CDF views there is a magenta line at RGT, ticks at 0, .5 and 1, and labels "1", ".5" and "0" (504-513). The magenta point (5×5) rides the S-curve at x₀, with a dotted line across to the axis (577-586). This replaces the lone "1" (292). **RGT moved 314 → 302** (328) to make room for the labels, so W = N = 278.
4. **Soft keys.** `DRAWMENU({"μ−","μ+","σ−","σ+","View","Quit"})` is called after the blit on every frame (618-620). A press at y ≥ 218 is drained, then acts as slot `MIN(6, IP(x/53.4)+1)` (654-657, ChiTable's shape). The hardware keys stay as shortcuts (759-769). **Enter now opens a menu** (771-784): Help, Next view, Re-centre, Quit. View has its own soft key, and keyboard-only users reach it through the menu.
5. **Vertical room.** BOT moved 194 → 190 and TOPy 22 → 37 (328). Nothing is drawn below y = 216: the harness's lowest text row is y = 204.
   - Rows above the plot: title at y 1, row 2 (x₀ / z / pdf, or the inverse) at 11, the two area keys at 22-34.
   - Rows below the plot: x labels at BOT+4, z-ruler at BOT+14.
   - **Removed:** the green legend line (355), whose job the strip and the help page now do; the μ/σ panel (339-341), because μ and σ are in the title row and the panel would cover the S-curve exactly where the magenta point rides at high percentiles. The mean marker, x₀ line and pdf dotted line are unchanged.
6. **Grab the mean.** A press within ±6 px of the green dotted μ line, and nearer it than the x₀ line, grabs μ (661-665). If the two lines are the same distance away, x₀ wins (harness 11a). The drag slides the bell inside the frozen window by whole pixel columns (729-735). The grabbed line is drawn 3 px wide (516-527). μ snaps to the grid on lift and the cache is refilled for the true μ (747-751). While μ is held, column k reads cache entry k − n3Sh, and only the |n3Sh| columns the cache does not cover are computed (469-503). verify_Norm3.py §4 checks that this is exact, and that the number of fresh columns is |m|.
7. **Complement shading.** Right of x₀ is shaded light red `RGB(255,235,235)`, in the same column loop as the blue (480-484). Row 3 prints `P(X ≤ x₀) = 0.8413` on a key filled with the blue shade and `P(X > x₀) = 0.1587` on a key filled with the light red (612-616).
8. **z-ruler.** Grey z labels −3…3 sit at μ + kσ under the x labels (552-568), with captions "x" and "z". They are thinned to −3, 0, 3 below 14 px per σ, and to 0 alone below 5 px per σ.
9. **Frozen window and the re-centre key.** v2.3 refitted μ ± 4σ on every frame (202-205), so the bell never moved; Lessons Learned §6 calls that the anti-pattern.
   - The window is now set on entry and on **0** (or the menu's Re-centre), and held otherwise (384-396). The arrows move the bell inside it.
   - x₀ still pushes the window when it passes an edge, as in v2.3.
   - Row 1 shows **"0 = re-centre"** in orange whenever pressing 0 would move the window by more than a tenth of its width (588-602). Example: x₀ pushed the window and then came back. The hint does not show while x₀ is still outside, because 0 would change nothing then (harness 8a-8c).
   - **This changes what Left/Right look like from v2.3:** the bell slides, and the window no longer follows it. The fleet review asked for exactly this.
10. **σ animation.** Up/Down and the σ soft keys move σ over 4 frames with the window and the y-scale held, so the peak visibly falls and spreads, or rises and narrows (369-382, 791-797). A 5th frame refits the y-scale. The y headroom is 1.45 × the peak (was 1.15, 210), so a step down peaks at 86 % of the held scale and is not clipped. The x-window stays frozen afterwards (§6: freeze x, not y), so the width change persists.
11. **The cache refills only when μ, σ or the window changes** (410-426; v2.3 refilled on every frame). Moving x₀ by keys, finger or S-curve needs no refill. Shading and curve are one column loop (460-487). Column k is drawn at exactly LFT + k: v2.3 recomputed `IP(LFT + …)`, which could land one pixel off.
12. **Help page** `n3_Help()` (264-289), from Enter → Help. It is a drawn page listing every gesture and key in 16 lines of font 1 that fit at 6 px a character, and is held with `n3_WaitAny()` (247, the house drain-wait-drain).
13. **x₀ is copied to `n3X0`** (316) and the code uses the copy. This follows the rule against new Unicode in executable code. The Home signature `Norm3(mu, sd, x₀)` is unchanged.
14. **Ends with `RETURN "Norm3: N(0.000, 1.000), P(X ≤ 1.00) = 0.8413; values in EP_NORM_*"`** (814). The EP_NORM_* globals are set as before.
15. **Header** updated: v2.4, the dated "What changed in v2.4" list, the v2.3 list kept, licence, AI and firmware lines kept, marked not yet run, and the controls block rewritten.

## 2 · Gate (final)

```
=================== Norm3_v2.4.txt ===================
--- 1. kit lint (errors) ---          kit lint: 0 errors   (warnings: textout-width only, the pre-existing kind)
--- 2. ppl_check tally (NEW)  ---      2 E5   1 E7
--- 2. ppl_check tally (ORIG) ---     13 E5   1 E7
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11) --- none
--- 3. lint_ppl structural ---         396 checks, 4 problems  (the 4 known 'no function named <file>' / EXPORT noise lines)
--- 4. full parse ---                  Norm3_v2.4.txt PARSE OK (6 functions);  ORIG PARSE OK (3 functions)
--- 5. ---                            816 lines, 36966 bytes;  E5 = the ₀ of x₀ in the signature (291) and the copy (316)
```
E7 is the checker splitting `x₀` into `x` + `₀` on the signature line, as in v2.3. `fleet_names_v2.py out/*.txt` reports Norm3's only collisions as those with its own v2.3. The new helpers `n3_Drain`, `n3_WaitAny` and `n3_Help` collide with nothing.

## 3 · Verification

**verify_Norm3.py** (rewritten; keeps the v2 checks A-E): **276 checks passed, 0 failed.** It covers:
- the pixel ↔ x₀ round trip (≤ 1 column) and the 1-2-5 snap grid;
- `NORMALD_ICDF` against `norm.ppf`, and `1 − CDF` against `norm.sf` at 4 decimals;
- the shifted-cache read, exact, with exactly |m| fresh columns;
- the z-ruler columns;
- p-grid reachability with H = 153: every 0.01 plus 0.025 and 0.975 reachable, while a 0.005 grid misses 47 values including 0.500;
- the σ frames 1.0625 / 1.125 / 1.1875 / 1.25; a step down peaks at 86.2 % and a step up at 55.2 % of the held scale; the area inside the held window stays ≥ 0.9985.

**harness_Norm3_v24.py** (ppl_run_v1, scripted keys, taps and drags; numbers against SciPy): **all 45 checks pass.** In summary:
- First frame: `x₀ = 1.00, z = 1.00, pdf = 0.2420 (a height)`, `P(X ≤ x₀) = 0.8413`, `P(X > x₀) = 0.1587`. The soft-key labels are drawn after the blit, the z-ruler reads −3…3, and nothing is drawn below 216.
- x₀ drag frames read 1.00 → 0.98 → 1.35 → 1.93, then 1.9 after the snap. The whole run made 285 NORMALD calls over 5 frames (one fill plus 2 a frame).
- S-curve: `p = 0.900 → x₀ = 1.28`, then dragged to `p = 0.950 → x₀ = 1.64`. Right-axis taps at y 113 and 114 both give `p = 0.500`; 41 gives `p = 0.975 → x₀ = 1.96`; 186 gives `p = 0.025 → x₀ = −1.96`.
- μ grab: 0 → 0.432 → 0.863, snapped to 0.9, with the 3 px line. The held-μ frame computed about 30 + 30 fresh values, not 556.
- σ animation: σ steps through the 4 values with the y labels held, then a 5th frame refits y; the x window stays frozen.
- Soft keys μ−, View and Quit each act. Menu → Help is drawn and closed by a tap; Menu → Next view works.
- Stale-key mode: the menu's left-over OK does not skip the help page.
- N(−12.5, 4) and N(500, 100) readouts match SciPy and fit at 6 px a character.
- A press outside the plot changes nothing.

The interpreter cannot model a key pressed while a finger is down, so the "key ends a hold" path was traced by hand (740).

## 4 · Device test checklist (in this order)

1. **Paste and compile.** Run `Norm3(0, 1, 1)`. The first frame appears without a key press. Check four things:
   - the soft-key strip reads μ− μ+ σ− σ+ View Quit;
   - the rows above the plot (title, magenta readout, the blue and light-red area keys) do not overlap each other or the plot;
   - the x labels and the z-ruler sit under the axis and **above the strip**;
   - right of x₀ is shaded light red.
2. **Drag x₀:** put a finger on the red line and slide it. The red line, both shadings, both P values and the magenta point on the S-curve should follow smoothly on the **G1**. If the G1 lags, note how much: each frame is one cached column loop plus about 40 text and line calls. Hold the finger still: nothing should flicker. Lift: x₀ jumps to a round value (1.3, 1.9 …) and the program does not hang.
3. **Tap the S-curve:** put a finger on the magenta curve at its upper right and slide it up. Row 2 should read `p = 0.900 → x₀ = 1.28` when you pass 0.90, then 0.95 (1.64) and 0.975 (1.96). Tap the right-hand axis at its ".5" tick: `p = 0.500 → x₀ = 0.00`. Then press low in the middle of the plot, in the shaded area under the bell. **That must move x₀ to the finger, not do the inverse** (the 16 px rule).
4. **Grab the mean:** press on the green dotted line, away from the red one, and drag right. The green line turns thick, the bell slides, μ in the title changes, and on lift μ snaps to a round value.
5. **Soft keys and keys:** tap μ+ and σ+ on the strip, then press ← → ↑ ↓. Each σ press shows four in-between frames, with the peak visibly falling (↑) or rising (↓), then one rescale. Tap View four times: the CDF, the right axis and the magenta point appear only in the two CDF views.
6. **Re-centre:** press + about twenty times (x₀ pushes the window right), then − twenty times. The orange **"0 = re-centre"** appears at the top right. Press 0: the window returns to μ ± 4σ and the hint disappears. The hint should also appear after several ← presses.
7. **Enter → menu:** check Help (the drawn page; a tap or any key returns), Next view, Re-centre and Quit. The menu items carry no numbers.
8. **Glyphs in font 1:** ≤ in "P(X ≤ x₀)", → in the inverse row, and μ− σ+ on the strip labels. If any shows as a box, the fallbacks are `<=`, `->`, and "mu-" style labels.
9. **Large and negative means:** `Norm3(500, 100, 600)` and `Norm3(-12.5, 4, -10)`. Every row must end before the right edge.
10. **Esc** returns `Norm3: N(…), P(X ≤ …) = …; values in EP_NORM_*`, and `EP_NORM_CDF` matches the last value shown. Home's K reads 278 afterwards (the MAKELIST counter), which is expected.

## 5 · Not confirmed, left as it was

- **The G1's frame rate during drags is unknown.** The x₀ and S-curve drags make no per-column calls. The μ drag computes |shift| columns fresh, and the σ animation refills the cache on each of its 4 frames.
- **Font-1 widths** are the fleet's 6 px a character estimate. The rows were sized for it, and checklist steps 1 and 9 cover them.
- **The 16 px "on the curve" tolerance and the ±6 px μ grab** are first guesses; tune them on the device.
- **MOUSE while a finger rests** is assumed to keep reporting the same position, as in NormExplorer's Explorer on hardware. If it reports nothing instead, a resting finger would count as a lift: x₀ snaps early, which is harmless.
- `!=` in `n3_fmtp` is unchanged.
- Arrow glyph convention: `CHAR(8594)` is used, ChiTable's form; the fleet decision is still open.
