# TDist3D beta 1 — User's Guide

Student's t distribution as one surface on the HP Prime, turned with a finger: every t curve at once, from the heavy tails of one degree of freedom to the normal curve. It is the calculator's version of the Maple surface drawn for *Statisticles*, Figure 9.3. Pure PPL: the work per frame is drawing, not computing, so no MicroPython is needed.

**Status:** written for the 2026-09-09 firmware (2.4.2). Run in the PC harness (`verify_TDist3D_beta1.py`, 85 checks, all passed; the monkey test, 1,000 runs of random keys, taps, drags, menu picks, and typed values) and on the HP Prime Virtual Calculator (Check: "No errors in the program"; the surface, the drag, both views, the form, the help pages, and the timing readout were all seen). **Not yet run on a G1 or a G2.** The first things to look at on the hardware are listed at the end.

beta 1 (8 Nov 2026): first version.

Run `TDist3D()` from the Program Catalog. Install the `.txt` through the Connectivity Kit editor, or copy `TDist3D.hpprgm` into the calculator's folder.

## What you see

**The 3-D view.** The height is f(t; ν), Student's t density. Across the floor runs t, from −6 to 6; away from you runs ν, the degrees of freedom, from 0.5 at the front to 10 at the back. Each row across is one t curve, and every row has area 1. Colour is height: blue low, magenta in the middle, red at the top (0.4 is the top of the scale). The front rows are low in the middle and lifted in the tails, which is what a heavy tail looks like; the back rows climb toward the normal curve, drawn in gray dots just beyond the back edge and labelled N(0,1), ν = ∞. The readouts give ν for the slice, its peak, its critical value, and its tail chance; the angles θ (turn) and φ (eye height) sit at the bottom left.

**The slice (Slice).** One row, ν = ν₀, drawn in red on the surface with its numbers in the corner:
- **peak:** f(0; ν₀), the height at t = 0 — 0.318 at ν = 1, 0.368 at ν = 3, 0.399 for the normal curve.
- **t crit:** the t with 2.5 % beyond it, the number that replaces 1.960 in a 95 % confidence interval or a two-sided test at α = 0.05 — 12.706 at ν = 1, 3.182 at ν = 3, 2.042 at ν = 30.
- **beyond ±2:** P(|t| > 2), the chance of a value past 2 in either direction — 0.295 at ν = 1, 0.139 at ν = 3, 0.046 for the normal curve.

Red posts stand at ±t crit when they fall inside t = ±6 (at ν = 1 they do not: 12.7 is off the floor). A red square marks the peak. When ν₀ is set above 10 the slice is past the back edge of the surface; the corner says so and points to the Curves view.

**The Curves view (Curves).** The family seen end on, the way a textbook draws it: the eleven rows stacked, coloured from blue (ν = 0.5) to red (ν = 10); N(0,1) in black dots; ±1.960 in gray dots; the slice in bold red with red ticks at ±t crit on the t axis. The same readouts are at the top.

## Touch and keys

| Action | 3-D view | Curves view |
|---|---|---|
| Drag | sideways turns (0.6° per pixel); downward raises the eye (φ 10°–80°) | — |
| Tap on the plot | nothing (a movement under 8 px is a tap, not a drag) | picks the curve nearest the finger |
| Left / Right | turn 10° | — |
| Up / Down | raise / lower the eye 10° | move the slice up / down the ladder |
| + / − | ν up / down the ladder | ν up / down the ladder |
| Enter | Menu | Menu |
| Esc | quit | quit |

While a finger turns the surface it is drawn on a 13 × 6 grid (137 line segments) and the screen says "13×6 while dragging"; it is redrawn at 25 × 11 (514 segments) when the finger lifts. A key press ends a drag.

## Soft keys

**ν− · ν+ · Curves (3-D) · Slice · Reset · Menu**

- **ν− / ν+** move the slice along a ladder: 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 100, 1,000. At the ends the screen says ν stops there. Either key turns the slice on.
- **Curves / 3-D** switches the view.
- **Slice** turns the slice on or off. With it off, the corner names the surface instead.
- **Reset** sets θ = 35°, φ = 30°, and ν = 3, with the slice on.

## The menu

- **Set ν exactly.** Any value from 0.5 to 1,000; two decimals are kept (7.126 becomes 7.13). A value outside the range is refused with a sentence and nothing changes. Below 0.5 the curve is all tail; past 1,000 it is the normal curve to three decimals.
- **Curves view / 3-D view.**
- **Slice on / off.**
- **Reset the view.**
- **Grid while dragging.** 13 × 6 (the default) or the full 25 × 11.
- **Frame timing (G1 test).** Milliseconds per frame for the 3-D view at both grids and for the Curves view. On the Virtual Calculator on a PC: 9 ms at 25 × 11, 5 ms at 13 × 6, 12 ms for Curves. A G1 is many times slower; this item is how to find out by how much.
- **Help.** Four pages: what the surface is, what ν does (a table), the slice and its numbers, keys and touch.
- **Quit.**

## Teaching notes

- **Why t is wider than z.** When σ is unknown, s takes its place in t = (x̄ − μ)/(s/√n), and s is a different number in every sample. So t varies more than z does, and the extra variation goes into the tails. Help page 1 says this in four lines.
- **What ν buys.** Step the slice from 0.5 up the ladder and watch the corner: t crit falls from 164 (ν = 0.5) through 12.7 (ν = 1), 4.30 (2), 2.57 (5), 2.23 (10), 2.04 (30), and 1.98 (100) toward 1.96. By ν = 30 the price of estimating σ is small; that is where the old "use z above 30" rule came from.
- **The chance beyond ±2.** For z it is 4.6 %. With one degree of freedom it is 29.5 %: nearly a third of the time. A value past 2 is nothing special in a sample of two.
- **The family at a glance.** Switch to Curves. The lowest, widest curve is ν = 0.5; the curves rise and tighten with ν, and the black dots (the normal curve) sit just above the red ν = 10 curve. In the tails the order reverses: the heaviest tail belongs to the smallest ν.
- **A value typed, not stepped.** Menu > Set ν exactly takes the degrees of freedom of a real problem (a two-sample t-test's (n₁ + n₂ − 2), or Welch's fractional ν) and shows that row's critical value at once.

## The arithmetic

- f(t; ν) = `STUDENT(ν, t)` = Γ((ν+1)/2) / (√(νπ) Γ(ν/2)) · (1 + t²/ν)^(−(ν+1)/2). The Prime's `STUDENT` takes any ν, fractions included.
- t crit = `−STUDENT_ICDF(ν, 0.025)`, the mirrored form (never ICDF at 0.975, where the upper tail loses its digits).
- P(|T| > 2) = `2·STUDENT_CDF(ν, −2)`, a doubled lower tail (never 1 − CDF).
- **Projection (orthographic):** with X = 14·t pixels across and Y = 14·(ν − 5) pixels away, screen x = 160 + X cos θ − Y sin θ and screen y = c − (X sin θ + Y cos θ) sin φ − k·f·cos φ, with k = 250 px per unit of density. The floor's centre c depends on φ alone, so the picture does not jump while θ changes.
- **Caching.** The surface never changes (ν is an axis, not a setting), so the 275 fine and 78 coarse heights, every segment's colour, the normal ghost row, and the Curves view's eleven curves (about 1,500 `STUDENT` calls) are computed once at the start; a drag only projects and draws. The slice's 49 heights and three numbers are recomputed when ν changes.
- **Angle unit.** `ASIN(1)` is a right angle in the calculator's own unit, so `ASIN(1)/(π/2)` converts radians at each SIN/COS call, and the program works whatever the angle setting is and never changes it.
- **Wireframe only,** drawn with `LINE_P`, as BiNorm3D: the 3-D `TRIANGLE_P` mesh drew nothing on the emulator (GfxProbe T07).

## Home exports (after a run)

`TD_NU`: the last ν of the slice. The program also returns a one-line summary (ν, t crit, and P(|t| > 2)) to Home.

## Checks on the first hardware run

1. Menu > Frame timing: the three times on a G1 and a G2, for the Lessons Learned table. If a 25 × 11 frame is over about 250 ms, keep the coarse grid while dragging (the default).
2. A drag across the surface: does it feel continuous, and does the full grid come back when the finger lifts?
3. The glyphs ν, θ, φ, °, ∞, ±, x̄, and ν₀ on the readouts and the help pages (all on the verified list except ν₀'s subscript next to ν, which is new).
4. The light tints of the help pages' panels on the G1's screen.

## Library check (D:\HP-Prime, 7 Nov 2026)

- **The only 3-D surface in the routine pool** is BiNorm3D's (bnFrame, bnDraw3D, bnDrag3D); TDist3D's projection, drag, wait, drain, page, and comma routines are re-tagged copies of those, reworked for a rectangular floor and a surface whose peak moves with ν.
- **`STUDENT(ν, t)` is the built-in density** and takes a fractional ν (Lessons Learned s3); `STUDENT_CDF` and `STUDENT_ICDF` likewise.
- **The Graph 3D app** (User Guide ch. 9) would draw FZ1(X,Y) = STUDENT(Y, X) with its own drag-rotation; it has no slice, no readouts, and no help, and setting its variables from a program is unverified, so the program draws its own surface.

## Credit

Concept, direction, classroom judgement, and all hardware testing: Roger D. Metcalf. Implementation, the numerics and their verification against SciPy, the harness and Virtual Calculator runs, and this guide: Claude (Anthropic).

*Free for educational and personal use. © 2026 Roger D. Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty.*
