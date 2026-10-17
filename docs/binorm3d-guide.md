# BiNorm3D beta 1 — User's Guide

The bivariate normal surface on the HP Prime, turned with a finger, for teaching correlation and regression to the mean. Pure PPL: the work per frame is drawing, not computing. No MicroPython is needed.

**Status:** written for the 2026-09-09 firmware (2.4.2). **Not yet run on hardware.** The arithmetic was verified off-device against SciPy, and the PPL itself was run in the PC harness under degrees, radians and grads (`verify_BiNorm3D.py`, all checks passed). The checks to make on the first device run are listed in `BiNorm3D_beta1_NOTES.md`.

beta 1 (16 Oct 2026): first version.
- **Wireframe only.** The surface is drawn with `LINE_P` and the program's own rotation and projection. The 3-D `TRIANGLE_P` mesh, `FILLPOLY_P` and alpha are not device-verified yet. A shaded version can follow once GfxProbe T07 passes.
- **Angle setting.** The program works whatever the calculator's angle setting is, and never changes it.

Run `BiNorm3D()` from the Program Catalog. Install the `.txt` through the Connectivity Kit editor.

## What you see

**The 3-D view.** X and Y are each N(0, 1), with correlation ρ. The surface is their joint density f(x, y) over the square −3…3 by −3…3. Colour shows height: blue low, magenta in the middle, red at the top. The height scale never changes. Because the volume under the surface is always 1, a narrower bell has to be taller: the peak is 0.159 at ρ = 0, 0.199 at 0.6 and 0.365 at 0.9. The readouts give ρ, the peak, and the view angles θ (turn) and φ (eye height).

**The contour view (Cont).** The surface seen from straight above.
- The inner ellipse holds **39 %** of all (x, y) pairs and the outer one **86 %**, whatever ρ is.
- The **magenta line** is the regression line E[Y | X = x] = ρx.
- The **dotted line** is y = x, the ridge of the bell.
- The ellipses tilt along y = x when ρ > 0 and along y = −x when ρ < 0.

**The slice (Slice).** The surface cut along the line x = x₀.
- *From above:* a red line you drag. The panel on the right shows the distribution of Y among the cases with X = x₀, N(ρx₀, √(1 − ρ²)), shaded magenta, against N(0, 1) in grey. The panel's rows are the plot's rows, so y reads straight across.
- *The guides:* the red dotted guide marks y = x₀, where Y would sit if it kept pace with x₀. The magenta guide marks y = ρx₀, where it actually centres.
- *The bottom line* gives the numbers and the verdict: **REGRESSION TO THE MEAN: 1.20 is nearer 0**.
- *In 3-D:* the cut is drawn in red on the surface. The floor shows y = x (dotted) and y = ρx (magenta), and a magenta post marks the top of the cut. The cut peaks above the regression line, not under the ridge.

## Touch and keys

| Action | 3-D view | Contour view |
|---|---|---|
| Drag | sideways turns (0.6° per pixel); downward raises the eye (φ 10°–80°) | moves the slice to the finger |
| Tap | nothing | puts the slice there |
| Left / Right | turn 10° | move x₀ by 0.25 |
| Up / Down | raise / lower the eye 10° | — |
| + / − | ρ up / down 0.1 | ρ up / down 0.1 |
| Enter | Menu | Menu |
| Esc | quit | quit |

While a finger turns the surface, it is drawn on an 11 × 11 grid. It is redrawn at 15 × 15 when the finger lifts. A key press ends a drag.

## Soft keys

**ρ− · ρ+ · Cont (3-D) · Slice · Reset · Menu**

- **ρ− / ρ+** step ρ by 0.1 within −0.9…0.9. At the ends the screen says ρ stops there: at ±1 the bell would collapse onto a line.
- **Cont / 3-D** switches the view.
- **Slice** turns the cut on or off.
- **Reset** sets θ = 35°, φ = 30°, ρ = 0.60 and x₀ = 1.5.

## The menu

- **Set ρ exactly.** Two decimals are kept; the range is −0.9…0.9.
- **Contour view / 3-D view.**
- **Slice on / off.**
- **Reset the view.**
- **Grid while dragging.** 11 × 11 (the default) or the full 15 × 15.
- **Frame timing (G1 test).** Milliseconds per frame for the 3-D view at both grids and for the contour view with the slice.
- **Help.** Five pages: what ρ does, why the contours tilt, what a slice is, regression to the mean, keys and touch.
- **Quit.**

## Teaching notes

- **Correlation as shape.** Step ρ from 0 to 0.9 in 3-D. The round bell stretches along y = x and its peak climbs. Then go negative.
- **The regression line is not the ridge.** In Cont the magenta line ρx is flatter than y = x, and it runs through the left and right ends of every ellipse. Turn the slice on in 3-D and drag around: the cut's highest point always stands above the magenta line.
- **Regression to the mean.** In Cont with the slice on, drag x₀ out to 2. The cases with X = 2 have Y centred at ρ·2 = 1.2 at ρ = 0.6, nearer the mean, although nothing was done to them. The weaker ρ is, the stronger the pull.
- **Criminal justice example (help page 4).** Offenders chosen for a programme because their risk score was extreme will score closer to the average next time, programme or not. The drop is not the programme's effect; only a comparison group selected the same way shows what the programme added.

## The arithmetic

- f(x, y) = exp(−Q/2) / (2π√(1 − ρ²)), where Q = (x² − 2ρxy + y²) / (1 − ρ²).
- Y | X = x₀ ~ N(ρx₀, √(1 − ρ²)).
- The share inside Q = k² is 1 − e^(−k²/2), because Q is chi-square with 2 df: 39.3 % for k = 1 and 86.5 % for k = 2.
- Each ellipse is drawn from x = k(a cos t + b sin t)/√2, y = k(a cos t − b sin t)/√2, with a = √(1+ρ) and b = √(1−ρ).
- **Projection (orthographic):** screen x = 160 + s(x cosθ − y sinθ), screen y = cy − s((x sinθ + y cosθ) sinφ + k z cosφ), with s = 22 and k = 24.
- **Why 84 px.** The ρ = 0 peak is 84 px tall. That is the largest height that keeps the ρ = 0.9 peak (2.29 times taller) on screen at every tilt.
- **Caching.** Heights, colours, ellipses and the slice shape are computed once per change of ρ, never during a drag.
- **Angle unit.** `ASIN(1)` is a right angle in the calculator's own unit, so `ASIN(1)/(π/2)` converts radians at each SIN/COS call.

## Home exports (after a run)

`BN_RHO`: the last ρ. The program also returns a one-line summary to Home.

## Library check (D:\HP-Prime, 16 Oct 2026)

- **Angle setting.** `ASIN(1)` as the angle-unit probe appears in berthu's PrimeControls ("depends on angle setting").
- **Glyphs.** ρ, θ and φ appear in TEXTOUT_P strings in CoorConvUlt2, and ° in ELEMENTS. The program builds them with `CHAR()` in one line of `bnInit`. If any shows as a box, change that line to plain text.
- **3-D wireframes in the corpus.** Those found (3dparaplot, crystal) use matrix or `LINE_P`-mesh forms that are unverified, so this program uses plain `LINE_P` with its own arithmetic.

## Credit

Concept, direction, classroom judgement and all hardware testing: Roger Metcalf. Implementation, the numerics and their verification against SciPy, the harness runs and this guide: Claude (Anthropic).

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty.*
