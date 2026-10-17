# Burr3 v2.4 — changes from v2.3 (the first touch version)

*16 October 2026. Source: `Burr3_v2.3.txt` (455 lines) → `Burr3_v2.4.txt` (986 lines). **Not yet run on hardware.** Written against Lessons Learned v7f, CLAUDE.md, BRIEF.md + BRIEF_TOUCH.md and Fleet Review §6. Norm3 v2.4's frame work is ported first, then the Burr-specific features are added. Every v2.3 fix is kept: the pdf cache, the 50·S window cap, the K·C ≥ 0.5 floor and launch guard, the launch drain, LOCAL lines ≤ 6, tagged names, the named moment cases, the "0" at the origin, Home's X as the MAKELIST counter, and the √ left as is.*

Line references are **v2.3 → v2.4**.

## 1 · Changes

1. **Drag x₀ and tap the S-curve, as in Norm3 v2.4.** GETKEY and MOUSE are polled together (431 → 752-773). With x₀ selected, a finger in the plot box sets `x₀ = (px − LFT)/W·xmax` (819-830, 860-864). A press **on** the S-curve (within 16 px, and nearer it than the pdf) or on the new right-hand 0-1 axis is the inverse, `x₀ = S·((1−p)^(−1/K) − 1)^(1/C)` (866-874). p is rounded to 0.01, with 0.025 and 0.975 caught. Row 2 reads `p = 0.900 → x₀ = 3.00`.
   - **The window is held while a finger is down and refitted on the lift** (`b3Frz`, 409-428). The auto-fit to the 0.995 quantile, capped at 50·S, is unchanged at rest.
   - x₀ snaps to `b3_NiceNum(xmax/100)` on lift and stays above 0.
   - Every lift goes through the capped `b3_Drain()` (248). A key pressed during a hold ends it.
2. **Right-hand CDF axis** (613-622): a magenta line, ticks at 0, .5 and 1, and a 5×5 magenta point riding the S-curve with a dotted line across to the axis (690-697). It replaces the lone "1" (350). **RGT moved 314 → 302.**
3. **Soft keys `{"C","K","S","x₀","View","Quit"}`** after every blit (750). Tapping C, K, S or x₀ **selects** what the arrows and a horizontal drag adjust. The selected name is boxed in light orange on the title row (708-716). This finally gives S a control.
   - Keys (896-905, 932-967): **all four arrows adjust the selected quantity** — Right/Up up, Left/Down down. C and K step by 0.25 under the v2.3 floor, S by ×1.25, x₀ by 1/40 of the window.
   - **0** selects the next name, for keyboard-only use. +/- still slide x₀. **Enter opens a menu** (Help, Next view, Quit; 918-929).
   - *Change from v2.3:* Up/Down used to step K. Now you select K first (soft key or 0), then use the arrows. C is selected at the start, so Left/Right do what they always did.
4. **Drag a parameter.** With C, K or S selected:
   - A press is held as "tap or drag?" (`b3Drag = 4`). More than 8 px of sideways movement makes it a drag (876-891). C and K move by 0.01 a pixel and S by ×1.02 a pixel.
   - **The K·C ≥ 0.5 floor holds on every sample.** C or K stops at the smallest hundredth that keeps the product ≥ 0.5, `CEILING(50/K)/100`, checked in verify_Burr3.py §8.
   - During the drag the x-window is held, so the curve visibly changes shape in a fixed frame; the y-scale follows. The window is refitted on the lift.
   - A **tap** (under 8 px of movement) still sets x₀, or does the inverse when it lands on the S-curve. It acts on the lift (776-791 hand it to the press code).
5. **Three markers (showcase)** (625-662): **mode** (orange), `S·((C−1)/(K·C+1))^(1/C)` for C > 1, else 0; **median** (magenta), `S·(2^(1/K) − 1)^(1/C)`; **mean** (green, the existing Lanczos value).
   - Each is a dotted vertical with its name and value (`mode 0.58`, `median 1.00`, `mean 1.57`), on its own row so close markers do not overprint, via `b3_Label` (275).
   - A marker past the window is named at the right edge with →. Example: `mean 100.02 →` at C = 1.01.
   - **When K·C ≤ 1:** the right 20 % of the plot is hatched — a light-red band with a diagonal `PIXON_P` dot pattern, about 290 dots (527-540) — and **"heavy tail: no finite mean"** is shown in red in a white box on the plot (698-702).
   - As C is dragged down, the three markers slide apart; at K·C = 1 the mean disappears and the hatch appears.
6. **Ghost** (555-571). After a C, K or S key step, the previous curve is drawn in light grey under the new one until the next action. It is mapped through the old window's dx, so it stays right when the window refits. During a parameter drag the ghost is the curve the drag started from, and it is still shown on the lift frame. A refused step draws no ghost.
7. **Fitted-normal overlay**, a fifth view (View cycle: grid+CDF, grid, CDF, plain, grid + normal; 581-604).
   - Draws in grey N(μ, σ) with the Burr's own mean and sd, cached in `b3Nrm` and filled once per parameter change.
   - The y-scale takes the taller of the two peaks (480-487; §6 "check both").
   - It prints **the normal's P(X < 0)**, the mass the symmetric model puts where the Burr has none.
   - When K·C ≤ 2 the sd does not exist, and the view says "normal fit needs K×C > 2 (now 2.00)" instead of drawing.
8. **Vertical room, as in Norm3:** BOT 194 → 190 and TOPy 22 → 24 (356). Nothing is drawn below y = 216; the harness's lowest row is 205.
   - Row 1 is the title with the C/K/S/x₀ values and the selection box. Row 2 is the readout, or the inverse, or "step refused".
   - x labels sit at BOT+4. The **status row** at BOT+15 carries the moments, or their absence in red when there is no mean, plus `K×C = …`, in orange with "(floor)" when K·C is at 0.5.
   - **Removed:** the legend line (420), and the moments panel (400-402), which covered the S-curve's plateau where the magenta point and the marker labels ride.
   - **Moved:** "window capped at 50×S" goes from the status line to an orange box on the plot (703-706).
9. **"CDF = …" → "P(X ≤ x₀) = …"**, with the pdf labelled "(a height)" (718-728), matching Norm3 v2.3/v2.4 as v2.3's CHANGES suggested.
10. **The cache refills only when C, K, S or the window changes** (458-495; v2.3 refilled every frame). Moving x₀ costs one pdf and one CDF evaluation a frame. The moments block moved ahead of the caches (430-456) because the fitted normal needs it. Mode and median are computed there too.
11. **Help page** `b3_Help()` (284) from Enter → Help, held with `b3_WaitAny()` (258).
12. **x₀ is copied to `b3X0`**, which the code uses (no new Unicode in code). The signature `Burr3(C, K, S, x₀)` is unchanged.
13. **Ends with `RETURN "Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 1.00) = 0.5000; values in EP_BURR_*"`.** EP_BURR_* are set as before; PDF and CDF are re-evaluated at the final state.
14. **Header:** v2.4, the dated "What changed" list, the v2.3 list kept, licence, AI and firmware lines, not yet run, the controls block rewritten, and the MATH VERIFIED note extended.

## 2 · Gate (final)

```
=================== Burr3_v2.4.txt ===================
--- 1. kit lint (errors) ---          kit lint: 0 errors   (warnings: textout-width only)
--- 2. ppl_check tally (NEW)  ---      4 E5   2 E7
--- 2. ppl_check tally (ORIG) ---     12 E5   2 E7
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11) --- none
--- 3. lint_ppl structural ---         498 checks, 4 problems  (the 4 known 'no function named <file>' / EXPORT noise lines)
--- 4. full parse ---                  PARSE FAIL line 445: unexpected character '√'   (ORIG: same, line 281)
--- 5. ---                            986 lines, 43315 bytes; E5 = ₀ at 311, 338, 345 and the existing √ at 445
```
- The parse failure is the kit's documented limit on `√`. The original fails the same way, and the rule is to leave existing `√` alone. A scratch copy with `(mvar)^.5` **parses OK (9 functions)**.
- E7 is `x₀` split by the checker, plus Home's `X` as the MAKELIST counter — both as in v2.3.
- `fleet_names_v2.py`: Burr3's only collisions are with its own v2.3. The new helpers `b3_Drain`, `b3_WaitAny`, `b3_Label` and `b3_Help` collide with nothing.

## 3 · Verification against SciPy

**verify_Burr3.py** (`scipy.stats.burr12`, c = C, d = K, scale = S; 184 parameter sets with K·C ≥ 0.5): **4,972 checks passed, 0 failed.**

| check | worst relative error |
| --- | --- |
| pdf | 1.9e-15 |
| CDF | 6.3e-15 |
| 0.995 quantile | 2.8e-15 |
| mean (Lanczos) | 6.2e-14 |
| variance (Lanczos) | 1.6e-13 |
| **median** | 8.6e-16 |
| **inverse CDF** (p 0.005-0.995) | 6.8e-14 |
| **mode vs argmax of scipy's pdf** | 3.5e-8 (the optimiser's tolerance) |

For C ≤ 1 the script confirms the pdf is decreasing, so the mode is 0. The drag floor `CEILING(50/K)/100` equals the smallest valid hundredth for 11 values of K. Every p in 0.01 … 0.99, plus 0.025 and 0.975, is reachable with H = 166.

```
C, K, S                mode     argmax     median      scipy     x(0.9)   ppf(0.9)
2, 1, 1             0.57735    0.57735    1.00000    1.00000    3.00000    3.00000
3, 2, 1             0.65863    0.65863    0.74543    0.74543    1.29312    1.29312
1.5, 0.75, 1        0.38113    0.38113    1.32190    1.32190    7.50116    7.50116
0.5, 2, 1           0.00000        (0)    0.17157    0.17157    4.67544    4.67544
5, 0.5, 3           3.08120    3.08120    3.73719    3.73719    7.52053    7.52053
10, 4, 100         85.93021   85.93021   84.66302   84.66302   97.52446   97.52446
1, 1, 1             0.00000        (0)    1.00000    1.00000    9.00000    9.00000
```
At C = 10 the mode lies right of the median: the skew reverses for large C, and the markers show it.

**harness_Burr3_v24.py** (ppl_run_v1): **all 50 checks pass.**
- **First frame.** Title `Burr | C = 2.00 | K = 1.00 | S = 1.00 | x₀ = 1.00` with C boxed; `pdf = 0.5000 (a height), P(X ≤ x₀) = 0.5000`; `μ = 1.571, no variance (K×C ≤ 2)`; `mode 0.58`, `median 1.00`, `mean 1.57`, all matching SciPy. The soft keys are drawn after the blit and nothing below 216.
- **Steps, ghost and floor.** A C step shows the ghost (206 grey segments), which is gone after the next action. Seven Left presses stop C at 0.50 with "step refused…", "K×C = 0.50 (floor)", the hatch (287 dots), the heavy-tail message and the cap notice; no mean marker is drawn and no ghost on the refused step.
- **S.** The S soft key, then Right, gives S = 1.25.
- **x₀ drag.** 0.96 → 1.98 → 4.36, then 4.4 after the snap, with the window held during the drag.
- **S-curve.** A tap on it with C selected gives `p = 0.900 → x₀ = 3.00`, acting on the lift. A drag up the curve gives `p = 0.975 → x₀ = 6.24`. A tap on the right axis at .5 gives the median, 1.00.
- **Parameter drags.**
  - C: under 8 px nothing happens; at +50 px, C = 2.50. The window is held during the drag and refitted on lift (the last x label goes from 14 to 8), and the markers match SciPy at C = 2.5.
  - K: dragging left stops at 0.25.
  - S: +35 px gives 2.00 = 1.02³⁵.
- **View 5 at Burr3(3,2,1,1).** The grey normal is drawn, `its P(X < 0) = 0.0207`, and `μ = 0.806, σ = 0.395` match SciPy; the normal is filled once (279 NORMALD calls). At K·C = 2 the view gives its message instead.
- **Menu and help.** Help is drawn and its lines fit; 0 pressed twice selects S; menu Quit returns the summary. Stale-key mode does not skip the help.
- **Edge cases.** `mean 100.02 →` at C = 1.01, and `mode 0.00` at C = 1.

## 4 · Device test checklist (in this order)

1. **Paste and compile, `Burr3(2, 1, 1, 1)`.** Check:
   - the strip reads C K S x₀ View Quit;
   - "C = 2.00" is boxed in light orange in the title row;
   - row 2, the x labels and the status row do not overlap, and all sit above the strip;
   - three dotted markers with labels: orange mode 0.58, magenta median 1.00, green mean 1.57.
   
   Then `Burr3(0.25, 0.25, 1, 1)` from Home must still be refused.
2. **Keys.** Press → (C 2.25): a light-grey ghost of the old curve should show under the new one. Press + : the ghost goes. Press ← seven times: C stops at 0.50, row 2 says "step refused…", the status row turns orange "(floor)", and the right fifth of the plot is hatched light red. "heavy tail: no finite mean" and "window capped at 50×S" both show, in boxes, and the mean marker is gone. **Check the hatch is visible but not garish.** The fallback is a lighter dot colour on line 536.
3. **Drag C (C selected).** With `Burr3(3, 2, 1, 1)`, drag sideways across the plot. C changes by about 0.01 a pixel, the three markers slide apart or together, the grey ghost of the starting curve stays, and the x-axis labels **do not change during the drag**. On lift the window refits. **Note the G1 frame rate:** each sample refills 278 pdf values, plus 278 CDF values in the CDF views. If it is sluggish, the fallback is to skip the S-curve during a parameter drag.
4. **Tap versus drag.** With C selected, a short tap in the plot moves x₀ there, on the lift. A tap on the magenta S-curve gives the inverse.
5. **K and S.** Tap K on the strip (the box moves) and drag left: K stops where K×C = 0.50. Tap S and drag right: S grows about 2× per 35 px, and the whole curve stretches in the held window.
6. **x₀.** Tap x₀ on the strip, then drag in the plot: x₀ follows, and on lift it snaps to a round value. Slide up the S-curve until row 2 reads `p = 0.900 → x₀ = 3.00`, then 0.975.
7. **View × 4 with `Burr3(3, 2, 1, 1)`.** The fifth view draws the grey normal, `grey = normal, same μ and σ`, and `its P(X < 0) = 0.0207`. With `Burr3(2, 1, 1, 1)` the fifth view says "normal fit needs K×C > 2 (now 2.00)".
8. **The 0 key** moves the box C → K → S → x₀ → C. **Enter** opens the menu: Help is a drawn page that a tap or any key closes; Next view; Quit.
9. **`Burr3(1.01, 1, 1, 1)`:** the mean label reads `mean 100.02 →` at the right edge. **`Burr3(1, 1, 1, 1)`:** `mode 0.00` is drawn next to the y-axis.
10. **Glyphs in font 1:** ≤ and × on the status row, → in the labels, x₀ on the strip. If a box shows, use the `<=` / `->` / `x0` fallbacks.
11. **Esc** returns `Burr3: C = …, P(X ≤ …) = …; values in EP_BURR_*`. Home's X reads 278 afterwards (the MAKELIST counter), and Home's K is untouched.

## 5 · Not confirmed, left as it was

- **G1 speed of parameter drags** (checklist 3). This is the one drag that must recompute the curve.
- **Font-1 widths:** the title-row segments are spaced 68 px apart for up to 11 characters (an S over 1000 would crowd), and the marker labels are clamped to the plot. Both rest on the fleet's 6 px a character estimate.
- **The selection model** is an interpretation of the brief: all arrows adjust, 0 cycles the selection, and a tap still sets x₀ when C/K/S is selected. If Roger prefers Up/Down = K as in v2.3, the change is two lines (897-898).
- **The 50·S cap, the 8 px tap threshold and the 16 px on-curve tolerance** are judgement values.
- **√(mvar)** is kept (it ran on hardware); it is why the kit's parser stops.
- **Complement shading** (Norm3's item 5) was not ported. The light-red fill is reserved for the heavy-tail hatch, so the two would read the same.
