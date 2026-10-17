# BiNorm3D beta 1 — notes

*16 Oct 2026. New program; not yet run on hardware. Files: `BiNorm3D_beta1.txt` (1,175 lines, pure ASCII), `verify_BiNorm3D.py`, `verify_BiNorm3D_output.txt`, `binorm3d-guide_beta1.md`.*

## What it does

The standard bivariate normal density f(x, y) with correlation ρ, drawn as a **wireframe** a student turns with a finger, plus a contour view and a slice that shows regression to the mean.

- **3-D view.** A 15 × 15 grid over [−3, 3]², drawn with `LINE_P` only (`TRIANGLE_P`/`FILLPOLY_P`/alpha are not device-verified; the header says a shaded version can follow once GfxProbe T07 passes). Each segment is coloured by its mean height on a 16-step ramp: blue (0,60,200) → magenta (200,0,200) → red (255,0,0). The program does its own orthographic projection: screen x = 160 + s(x cosθ − y sinθ), screen y = cy − s((x sinθ + y cosθ) sinφ + k z cosφ), with s = 22 and k = 24. The z scale is fixed, so the peak visibly rises as ρ grows. The floor square and the x/y axes are grey and labelled. Lines are drawn back to front by row order.
- **Touch.** A horizontal drag turns θ at 0.6° per pixel; a vertical drag tilts φ, clamped to 10–80° (dragging down looks from higher up). The view redraws on each drag sample, from the cache. Movement under 8 px counts as a tap. Any key ends a drag. The finger-lift drain is capped. The arrows turn and tilt in 10° steps.
- **Soft keys** `ρ− ρ+ Cont Slice Reset Menu`, drawn after every blit. `+`, `−` and Enter are hardware shortcuts. In the contour view the third key reads `3-D`.
- **Contour view.** The ellipses Q = 1 and Q = 4 come from the parametric form, 60 segments each, labelled 39 % and 86 %. When |ρ| > 0.75 the 39 % label moves onto the long axis so it clears both ellipses. The view also shows y = x dotted and the regression line y = ρx in magenta.
- **Slice.**
  - *Contour view:* a red line at x = x₀ that you drag (or tap, or move with Left/Right in 0.25 steps; x₀ snaps to 0.05). A side panel shares the plot's pixel rows, so y reads straight across. It shows f(y | x₀) = N(ρx₀, √(1−ρ²)), shaded magenta, against N(0, 1) in grey. A red dotted guide marks y = x₀ and a magenta guide marks y = ρx₀. The verdict line reads "REGRESSION TO THE MEAN: 1.20 is nearer 0". Special wording covers x₀ = 0 and ρ = 0.
  - *3-D view:* the surface cut at x₀ is drawn in red. The floor carries the ridge y = x (dotted) and the regression line y = ρx (magenta), with a magenta post from the floor to the top of the cut. This shows that the slices peak above the regression line, not under the ridge.
- **Reset** sets θ = 35°, φ = 30° and ρ = 0.60 (and puts x₀ back to 1.5).
- **Menu** (a CHOOSE with unnumbered items): set ρ exactly (INPUT, range −0.9…0.9, kept to two decimals), the view, slice on/off, reset, the grid while dragging, frame timing, help, quit.
- **Help**: five drawn pages:
  1. what ρ does to the surface
  2. why the contours tilt
  3. what a slice is
  4. regression to the mean, with the criminal-justice programme example
  5. keys and touch
- **Home:** `BN_RHO`. The program returns a summary string.
- **Structure:** follows ChiTable beta 1k and GaltonBoard beta 1a.
  - File-level `LOCAL` state and palette constants, set in `bnInit`.
  - `bnDrain` / `bnWaitAny` copied from the TOUCH brief.
  - Every helper carries the `bn` tag.
  - Lists are built with `MAKELIST(0, K, 1, n, 1)`, so Home's K is overwritten, as in the rest of the fleet.
- **Angle mode** is never changed. Angles are kept in radians, and `bnAU := ASIN(1) / 1.5707963267949` converts them at each SIN/COS call. The same idea is used in berthu's PrimeControls (found in the library index).
- **Glyphs:** ρ, θ, φ and ° are `CHAR(961/952/966/176)`. None is on the verified list, but all four appear in corpus TEXTOUT_P strings (CoorConvUlt2, ELEMENTS). They are set in one line of `bnInit` with an ASCII fallback noted there. The verified glyphs ², −, ₀ and × are used as well.

## Verification (verify_BiNorm3D.py — ALL CHECKS PASSED)

- **A — formulas against SciPy.**
  - Density vs `multivariate_normal`: worst relative error 3.1e-14 over 7 values of ρ × 225 points. Peak = 0.159155 / 0.198944 / 0.365126 at ρ = 0 / 0.6 / 0.9.
  - Conditional mean ρx₀ and SD √(1−ρ²) by numerical integration: errors 4e-13 and 5e-14. f(x₀, y)/φ(x₀) matches `norm(ρx₀, sd)`.
  - Share inside Q = k²: 1 − e^(−k²/2) = chi2(2) = 0.3935 / 0.8647, confirmed by a Monte Carlo run of 10⁶ draws at ρ = 0.6 and −0.9.
  - The parametric points satisfy Q = k² to 5e-15. The left/right ends of each ellipse lie on y = ρx, and its top is at (ρk, k).
  - Projection at θ = 0° and 90° (φ = 30°): (3, 0) → (226, 168) and (160, 135); (0, 3) → (160, 135) and (94, 168); (−3, −3) → (94, 201) and (226, 201).
  - Every grid point at every ρ, θ (5° steps) and φ (1° steps) stays on screen, y 1…215.
- **B — the PPL itself in `ppl_run_v1.py`.** SIN, COS and ASIN were added to the harness so it can mimic degrees, radians and grads.
  - All 346 cached heights match SciPy (rel. ≤ 5e-14), the ellipse pixels match exactly, and the slice-panel shape and N(0, 1) rows match.
  - bnAU = 57.2958 / 1 / 63.662, and **all three angle modes give identical pixels**.
  - The PPL's `bnPX`/`bnPY` equal the Python projection for all 3 × 225 points (0 px off).
  - ρ stops at ±0.9 with a message; 0.6 + 0.1 is stored as 0.7; x₀ snaps and clamps.
  - A scripted session used both drags, every soft key, the arrows, the menu, the exact-ρ form, frame timing and all five help pages: no runtime error, every scripted event used, no text past its width, `DRAWMENU` straight after the blit on all 49 frames, help lines ≤ 46 characters, `BN_RHO` = −0.45 as typed.
- **C — layout.** Both ellipse labels clear both ellipses and stay inside the box for every ρ from −0.9 to 0.9 in 0.01 steps.

**Gate** (`check.sh`): kit lint 0 errors; ppl_check_v3 0 errors and 0 warnings (E2, E3, E6, E8, E10 and E11 all zero); lint_ppl shows only its 5 known-noise lines (versioned filename, EXPORT discipline); the kit parse fails at the file-level `LOCAL` after `EXPORT BN_RHO;`, its documented limit (ChiTable beta 1k fails the same way; the harness parser reads it); no non-ASCII characters.

**Fleet names** (`fleet_names_v2.py` on the latest version of each program in out/, 26 files): 0 collisions, 0 untagged, 0 mixed tags, 0 built-in matches. Run over every `*.txt`, the only collisions are between two versions of the same program from other sessions (ChiTable 1l/2, EpiStats 1.4/1.5, and so on). None involves `bn`.

## Frame cost (counted in the harness; no time measured)

| Frame | LINE_P | PIXON_P | TEXTOUT_P | RECT_P |
|---|---|---|---|---|
| 3-D 15×15, slice off | 426 | 0 | 6 | 0 |
| 3-D 11×11 (drag), slice off | 226 | 0 | 7 | 0 |
| 3-D 15×15, slice on | 485 | 49 | 8 | 1 |
| 3-D 11×11 (drag), slice on | 285 | 49 | 9 | 1 |
| Contour, slice off | 141 | 55 | 31 | 0 |
| Contour, slice on (the x₀-drag frame) | 435 | 113 | 25 | 2 |

Each 3-D frame also projects 225 points (121 at 11×11): two list stores and about six arithmetic operations each, with 4 SIN/COS calls per frame. No density is evaluated in any frame, because everything comes from the cache, which is rebuilt once per ρ change (346 EXP plus 121 for the panel).

**Decision.** The full 3-D frame is under the ~450 threshold with the slice off (426) but over it with the slice on (485 + 49). So **coarse-while-dragging is implemented and on by default**: an 11 × 11 grid (226 LINE_P) while the finger is down, redrawn at 15 × 15 on lift. It can be turned off in Menu. The house reference point is that one 272-column curve from a cache plus about 40 calls is fine on a G1. On that basis I estimate the full frame is about at the G1's comfortable limit and the coarse frame about half of it. That is an estimate only. **Menu → Frame timing** measures the 3-D frame at both grids and the contour+slice frame with `TICKS` on the device. The contour+slice frame (x₀ drag) has no coarse fallback, and it is the one to watch on the G1.

## Device test checklist (least to most risky)

1. **Paste and launch on the G2.** No syntax error. The welcome page draws. ρ, θ, φ and ° render (not boxes). If any is a box, edit the one `bnRS := …` line in `bnInit`.
2. **Static 3-D view.** The coloured wireframe sits between the corner readouts. The peak is red and the floor grey, with "x" and "y" labels. Readouts show ρ = 0.60, peak 0.199, θ = 35°, φ = 30°. The soft-key strip shows ρ− ρ+ Cont Slice Reset Menu.
3. **Angle mode.** Repeat step 2 with the calculator in Radians, then in Degrees. The picture must be identical. Your angle setting must be unchanged after quitting.
4. **Keys.** The arrows turn and tilt in 10° steps (φ stops at 10° and 80°); + and − step ρ; ρ+ at 0.9 says "ρ stops at 0.9 here"; Enter opens the menu; Esc quits and Home shows the summary with `BN_RHO` set.
5. **Soft keys by tap.** ρ−, ρ+, Cont/3-D, Slice and Reset. Menu: set ρ exactly (try 0.75, then 0.95, which should be refused with a message), help (5 pages; Esc leaves), quit.
6. **Contour view.** The two ellipses tilt with ρ, with 39 % and 86 % labels readable at ρ = 0.6, 0.8, 0.9 and −0.9. The magenta regression line passes through the ellipses' left and right ends, and y = x is dotted.
7. **Slice in the contour view.** Tap the plot, then drag left and right. Check that the red line follows the finger, the shaded panel moves, and the verdict line updates. Check that Left/Right move x₀ by 0.25 and the panel rows line up with the plot's y.
8. **Slice in 3-D.** The red cut, the magenta post and the floor lines appear. The post's top sits on the cut's highest point.
9. **3-D drag on the G2.** Smooth turning; "11×11 while dragging" shows during the drag and the view refines to 15 × 15 on lift. Hold a finger still with no move: nothing should happen. Press a key mid-drag: the drag ends.
10. **Frame timing on the G2, then the G1**, with the slice off and then on. Note the three numbers. If the 15 × 15 frame is under ~150 ms on the G1, the coarse grid could be switched off by default. If the contour+slice frame is over ~250 ms, the panel outlines need thinning in beta 2.
11. **Drags on the G1.** The 3-D drag with the slice on, and the x₀ drag. These are the riskiest items for feel, not for correctness.

## Not verified / known limits

- **Off-screen drawing.** Whether `LINE_P` clips cleanly off the grob is unverified (kit docs: unmeasured). The geometry keeps every grid point on screen (y 1…215), so it should not arise.
- **The MOUSE drag loop** (`REPEAT … UNTIL SIZE(MOUSE(1)) == 0`) matches NormExplorer's device-run drag and the new TouchKit template. A continuous redraw inside the loop has not been run by this program.
- **Unverified constructs.** `RGB()` with computed arguments, `ASIN`, `SIN`/`COS`, and a `DRAWMENU` list built from concatenated strings are standard but are not on the §3 confirmed list.
- **Frame times are not measured**; see the section above.
- **The 84 px peak.** The ρ = 0 peak is 84 px, not ~90. That is the largest value that keeps the ρ = 0.9 peak, which is 2.29 times taller, on screen at every tilt with a fixed z scale.
- **Wording.** The criminal-justice wording on help page 4 is Claude's draft and needs Roger's classroom judgement.
