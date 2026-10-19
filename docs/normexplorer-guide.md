# NormExplorer beta 42a — User's Guide

A normal-distribution workbench for the HP Prime: set any N(μ, σ), find areas and the x-values behind them, solve the z-formula, look at your own data against a fitted curve, compare two curves, and — the heart of it — **explore the curve with your finger**: drag a cut point and watch the area change, drag the mean, stretch σ, and see the probability travel with the shaded region. PPL, with an optional MicroPython sampler for simulated histograms.

**Status:** beta 42a (19 Oct 2026) fixes what the fleet review found; it has run in the PC test harness only. Beta 42 (16 Oct 2026) is the touch and graphics version. It has **not yet been run on hardware**. Builds up to beta 39 were tested on an HP Prime G2 and G1 (2026-09-09 firmware) and the Virtual Calculator; beta 40, 41 and 42 have not been. The arithmetic was checked against SciPy and the program's own code was run, path by path, in an off-device interpreter (see *How it was checked*). The device checklist is in `NormExplorer_beta42_CHANGES.md`.

Install: paste `NormExplorer_beta42.txt` into the Connectivity Kit editor and send it to the calculator. Run **NormExp** from the Program Catalog (Shift-1).

---

## The main menu

The Prime numbers the items itself: 1 to 9, then **A** and **B**.

| Item | What it does |
|---|---|
| 1 Set μ and σ | The session distribution. Any μ, any σ > 0: N(100,15), N(2.4,0.6), N(847,220) all plot. Changing it clears the shading, the histogram and the second curve, which all belonged to the old one. |
| 2 Explore the curve | The live plot: touch, soft keys and arrow keys (below). |
| 3 Probability from x | P(X < x), P(X > x), P(a < X < b), P(outside a, b). |
| 4 x from probability | Percentile; critical value for a right-tail, left-tail or two-tailed α; central C% interval. |
| 5 Z-formula solver | z = (x − μ)/σ: enter any three of z, x, μ, σ and get the fourth. |
| 6 Data & histogram | Your own data from the Statistics apps, regression residuals, z-scores into D2, or a simulated sample. |
| 7 Compare curves (d, power) | A second curve N(μ₂, σ), Cohen's d, and the power picture. |
| 8 Standardize animation | Watch N(μ, σ) slide and squeeze into N(0, 1). |
| 9 Plot window & display | Window, bands, N(0,1) reference or CDF overlay, diagnostics, reset. |
| A Help | Three pages: the modules, the Explorer's two pages of soft keys, touch. |
| B Quit | Leaves the program. Esc on the menu does the same. |

Every calculation shows a **result panel** first (any key or a tap continues), then the result **shaded on the curve** — and the shaded area grows into place over about a second, with the running area printed, so you see the number as an accumulation of area. A key or a tap skips the growing.

---

## What is on the plot

- **The curve** N(μ, σ) in blue, with a dark line at the mean (labelled μ) running up to the peak: the mean is also the highest point.
- **68-95-99.7 bands** (on unless you turn them off): μ ± σ, ± 2σ, ± 3σ in three blues, with the exact areas and ranges in the top-right corner — 68.27 %, 95.45 %, 99.73 %, not the rounded headline.
- **Shading** in orange for the area you asked about, with red lines at the bounds. The area is printed in a **small white box riding on the shaded region** (each tail gets its own box when you shade outside two bounds); when the region is narrower than 40 pixels the box is left out and the corner readout carries the number alone.
- **Two rows of labels under the axis.** The black row is x. The grey row, marked **z** at the far left, is the z-score: −3 to 3, printed exactly at x = μ + kσ. Read down from an x-label to the z beneath it and you have z = (x − μ)/σ without arithmetic. (On a very narrow σ the z-row thins to every other label, or disappears.)
- **Readouts:** μ and σ at the top left (and μ₂ and d with a second curve; n, x̄ and s with a histogram); x₀, its z and the probability at the top right.
- **Optional:** the N(0,1) reference curve in grey (when it fits — otherwise a grey note says so), or the **CDF** S-curve in magenta (see below), a second curve in green, a histogram.

---

## Explore the curve (item 2)

On entry the window is **frozen** at μ ± 6σ of the distribution you start with. That is deliberate: if the window followed μ, the bell would sit dead centre for ever and moving the mean would look like nothing happening. With the window held, μ visibly slides and σ visibly reshapes. **Centre** (or the 0 key) re-centres it.

### Soft keys (the bottom row)

There are two pages of soft keys. **More**, always in the last slot, turns the page.

**Page 1** (shown when you enter):

| Soft key | Does | Key shortcut |
|---|---|---|
| **Bands** | 68-95-99.7 bands on or off | + |
| **Ref** | cycles: N(0,1) reference curve → CDF S-curve → neither | − |
| **Centre** | re-centre the window on the curve as it is now (the arrow steps re-fit too) | 0 |
| **Shade** | cycles the shading: left of x₀ → right of x₀ → between → outside → none. "Between" starts symmetric about the mean, at μ ∓ \|x₀ − μ\| | — |
| **Hist** | with a histogram on the plot: taps now read the bars (see *Reading a bar*); Hist again to go back. Without one, a note says where to make one | — |
| **More** | page 2 | — |

**Page 2 — what the arrow keys move:**

| Soft key | Then ← → move … |
|---|---|
| **Bnd A** | the lower bound (x₀ when there is only one); with no shading yet, a left tail starts at x₀ |
| **Bnd B** | the upper bound (needs between or outside shading — otherwise a note says so) |
| **mu** | the mean |
| **sigma** | σ: ← narrower, → wider |
| **Menu** | back to the menu (Esc or Enter also work, from either page) |
| **More** | back to page 1 |

The chosen handle is drawn thick and the line under the title says, for example, *arrows move: lower bound*. Bounds move in round steps (σ/10 pushed to 1, 2 or 5 × a power of ten); stepping one bound past the other swaps them. Tap the chosen key again to go back to the usual arrows. ↑ ↓ always change σ. This is the way to set a bound without touching the plot — and the way to nudge it exactly.

The arrow keys still do what they always did: **← →** move μ and **↑ ↓** change σ, in round steps (σ/4 and σ/10 pushed to 1, 2 or 5 × a power of ten: on N(100,15), μ moves by 5 and σ by 2). Each press moves to the next round value, so an odd start such as 847 snaps to 850 and stays round.

### Touch

What a finger does depends on **where it first lands**; while it stays down it drags that same thing; lifting it ends the drag.

| Press on … | and drag … | Notes |
|---|---|---|
| a red bound line (within about 8 pixels) | that bound follows your finger | with two bounds (between, outside) the shading **stays two-bounded**; drag one past the other and they swap |
| the dark **mean line** | sideways: μ moves with your finger | the line thickens while held; on lifting, μ snaps to the arrow step |
| a **small square** on the curve — the shoulders, μ − σ and μ + σ | outward to widen σ, inward to narrow it | both shoulders thicken; the peak stays at the same height on screen while the y-axis labels change (σ changes the peak height); on lifting, σ snaps to the arrow step |
| anywhere else in the plot | — | the **nearer bound jumps** to your finger and you drag it from there; with no shading yet, a left tail starts at your finger |
| the bottom strip | — | a soft key, acted on when you lift |

When two handles are within 8 pixels of your finger, the nearest wins. While you hold μ or σ, a grey line under the title says so. The window never moves during a drag; only σ re-fits the vertical scale.

A finger that wanders off the plot keeps dragging, pinned to the edge. Lift and press again to start something new.

To move a bound from the keyboard, choose it on soft-key page 2 (above) and use ← →. To type an exact bound, use menu 3 or 4, then tap the plot on the result view to carry on exploring from there.

### Height is not probability

In the Explorer the top-right corner reads, for a one-sided cut:

> x₀ = 1.00  z = 1.00
> area to the left = 0.8413
> height 0.242 (density,
> not a probability)

The **area** under the curve to the left of x₀ is the probability. The **height** of the curve at x₀ is a *density* — probability per unit of x. It is not the probability of anything: P(X = 1) is 0 for a continuous variable. Make σ small (menu 1, σ = 0.2) and tap at the mean: the height is 1.995, bigger than 1, which no probability can be.

(With two bounds the corner reads "area between" or "area outside". With a second curve on, the corner shows the power instead of the height. In the result views after a calculation the corner keeps the P(X < x₀) notation of the panel you just read.)

### The CDF overlay

Cycle **Ref** (or −) to the CDF, or choose it in menu 9. The cumulative curve F(x) = P(X < x) appears in magenta on its own 0-to-1 scale up the **right-hand edge** ("1" at the top, a tick at ½). From the point where each bound meets the S-curve, a dotted magenta line runs across to that edge, and the corner adds "CDF(x₀) = …". The height of the S-curve at x₀ **is** the area to the left of x₀ — drag x₀ and watch both. With two bounds, the gap between the two dotted lines is the area between them. Where the bell is tallest the S-curve is steepest: they are one distribution, seen as a rate and as an accumulation.

---

## The result views

After every calculation (and after menu 9's display items) the plot stays up until you answer it:

| You | It |
|---|---|
| press any key | back to the menu |
| tap inside the plot | opens the **Explorer** on this picture, shading kept — drag the bound you just computed |
| tap a histogram bar | shows that bar's numbers (below) and stays |
| tap outside the plot | back to the menu |

The footer says which: *tap plot = explore, any key = menu*, or with a histogram *tap bar = counts, tap plot = explore, any key = menu*.

### Reading a bar

Tap a bar (on a result view) or, in the Explorer, press **Hist** and touch or slide along the bars. The bar is outlined in red and a small orange-framed panel reads, for example:

> bin 12: 148 observed, 151.3 expected (n×p)
> x from −0.25 to 0.00,  p = 0.0987

*Observed* is how many values fell in that bin. *Expected* is n × p, where p = F(right edge) − F(left edge) is the curve's probability for that bin — under the curve **as drawn now**. Move μ in the Explorer and the expected counts move with it, so a curve that fits badly shows it bar by bar.

---

## Probability from x (item 3)

| Choice | You enter | Shaded |
|---|---|---|
| P(X < x) left tail | x | left of x |
| P(X > x) right tail | x | right of x |
| P(a < X < b) between | a, b (either order) | between |
| P(outside a, b) two tails | a, b | both tails |

The panel shows x (or a and b), z, the probability in red and its complement. `NE_X`, `NE_Z` and `NE_P` keep the last answer.

## x from probability (item 4)

| Choice | You enter | Gives | Shaded |
|---|---|---|---|
| x at a percentile (area left) | area to the left (default .90) | z* and x | left tail |
| Critical value: right tail (α) | α (default .05) | z* = Φ⁻¹(1 − α), x* | right of x* |
| Critical value: left tail (α) | α | z* = Φ⁻¹(α) — negative — and x* | left of x* |
| Critical values: two tails (α) | α, the total in both tails | z* = ± Φ⁻¹(1 − α/2), lower and upper x* | **both tails**, each boxed with α/2 |
| Central C% interval | C (.95 or 95 both work) | z* = Φ⁻¹((1 + C)/2), the interval | between |

The two-tailed picture and the central 95 % picture are the same two lines with complementary shading — worth showing side by side. (Item 5 was item 3 before beta 42.)

## Z-formula solver (item 5)

Pick the unknown — z, x, μ or σ — and enter the other three. The answer is shown with the formula filled in, e.g. *z = (x − μ)/σ = (130 − 100)/15*. The solver remembers its x and z between visits, and its μ and σ are the session's: solve for μ or σ and the plotted distribution follows. Solving for σ refuses a z whose sign disagrees with x − μ, and says so.

## Data & histogram (item 6)

| Choice | What it does |
|---|---|
| My data from D1 (Statistics 1Var) | Fits N(x̄, s) to the list D1 (s with the n − 1 divisor), makes it the session curve and draws your data as a histogram of 32 bins over x̄ ± 4s, on the density scale |
| Two groups from C1, C2 (2Var) | A curve for each group, both drawn with the pooled s; Cohen's d in the corner |
| Regression residuals from C1, C2 | Least-squares line of C2 on C1, then the residuals through the same view — the normality assumption behind slope inference, shown rather than told |
| Write z-scores of D1 into D2 | So the next step can be done with the calculator's own apps |
| Normal probability plot of D1 | Opens Statistics 1Var (set Plot1 to Normal Probability, then Plot, Autoscale) |
| Simulate a sample | n = 200, 1000 or 5000 from the session N(μ, σ); the sample's own x̄ and s appear beside μ and σ — they differ on every draw, which is the lesson |
| Clear histogram | |

The bars are filled pale green under the curve. Where a bar stands inside the shaded region it is filled deep orange instead, so the shading still reads as one region; a bar that a bound crosses is split at the line.

## Compare curves (item 7)

| Choice | What it does |
|---|---|
| Set μ₂ and show (same σ) | A second curve in green with its own mean line (μ₂). The gap between the two mean lines, measured in σ, is **Cohen's d = (μ₂ − μ)/σ**; the overlap of the two curves is shaded light green |
| Turn second curve off | |
| Power picture: right-tail α | Enter α; the cut x* = μ + z₁₋α σ is set, curve 2 turned on at the current μ₂, and a panel shows α, x*, μ₂, d, the **power** and β = 1 − power |

**The power picture** appears whenever the second curve is on and the shading is a right-tail cut x*. Curve 1 is the null hypothesis; its orange tail past x* is α. Curve 2 is the alternative; *all* of its area past x* is the power, and the light green shows the part of it above curve 1. The corner reads "power = …". Tap the plot to explore: drag x* left and α grows while power grows with it; drag right and both shrink. Move μ (the null) with the mean line or the arrows and d changes under your finger.

## Standardize animation (item 8)

Two phases on a window wide enough for the whole journey: the mean slides to 0 (*shift x − μ*), a pause, then the spread squeezes or stretches to 1 (*rescale (x − μ)/σ*), ending on N(0,1) with the formula over it. The session μ and σ are not changed. The z-row under the axis travels with the curve and, at the end, sits exactly under the x-row.

## Plot window & display (item 9)

| Choice | |
|---|---|
| Auto: μ ± 4σ (default) | widened automatically to include the shading and a second curve |
| Wide: μ ± 6σ | |
| Custom: enter xmin, xmax | kept until μ or σ changes, then auto again — the program says so when it drops it |
| Bands 68-95-99.7: ON / off | the menu line shows the current state |
| N(0,1) reference curve: ON / off | the reference and the CDF share one setting, so turning one on turns the other off |
| CDF overlay (S-curve): ON / off | |
| Show current window | the x-range, its width in σ, the y-top and the peak |
| Diagnostics | whether the MicroPython bridge answers, and which sampler drew the last histogram |
| Reset everything to N(0,1) | a clean start without quitting |

---

## Home exports

`NE_Z`, `NE_X` and `NE_P` hold the last z, x and probability (power, after the power picture) and are still there after Quit. NormExp also returns them as its result line, e.g. `NormExp: z = 1.6449, x = 124.6728, p = 0.2595`, so it appears in the Home history.

## The arithmetic

- Areas: `NORMALD_CDF(μ, σ, x)`; P(a < X < b) = F(b) − F(a); outside = 1 − that.
- Inverses: `NORMALD_ICDF`. Right-tail z* = Φ⁻¹(1 − α); left-tail z* = Φ⁻¹(α); two-tailed z* = Φ⁻¹(1 − α/2); central C: z* = Φ⁻¹((1 + C)/2); x = μ + z σ.
- d = (μ₂ − μ)/σ. Power = P(X₂ > x*) = 1 − Φ((x* − μ₂)/σ), which is the textbook 1 − Φ(z₁₋α − d).
- A bin's expected count = n [F(right) − F(left)].
- Sample statistics use the n − 1 divisor; two groups use the pooled s_p = √(((n₁−1)s₁² + (n₂−1)s₂²)/(n₁+n₂−2)).
- The density is `NORMALD(μ, σ, x)`, cached once per pixel column and kept across frames; the CDF S-curve is drawn from that cache by adding trapezoids (within 0.0001 of the exact curve at the usual windows). **Every number printed on screen comes from `NORMALD_CDF` / `NORMALD_ICDF` themselves**, never from the drawing caches.

## How it was checked

Every new formula was checked against SciPy in `verify_NormExplorer.py`, and the program itself was run in hp-prime-kit's PPL interpreter with scripted menu choices, keys and touches: all four probability types, all five inverse items, the solver, the power picture, the Explorer's drags, grabs and soft keys, a histogram bar tap, the CDF overlay, the animation, the help pages, the window menu and a whole session — 135 checks, none failed. None of that is a substitute for the calculator: the device checklist in `NormExplorer_beta42_CHANGES.md` lists what to try, least risky first.

## What changed in beta 42a

The fleet review of 19 Oct 2026 found that the 17 Oct display clean-up had never reached NormExplorer. Details, line by line, are in `NormExplorer_beta42a_CHANGES.md`.
- **No number on screen turns scientific any more** (`4.8213ᴇ−8` for a far right tail). Every value is rounded before it is printed, in 134 places. A probability too small to show reads "< 0.0001".
- **Right tails keep their digits on the Prime:**
  - the area between two bounds far out on one side;
  - the right-tail and two-tailed critical values.
  Before, they printed 0.0000 past about z = 7, and a tiny α could ask for Φ⁻¹(1), which is an error.
- A typed confidence level of 1 now means 1 %.
- After a σ drag, the arrow steps refit to the new σ.
- Every menu follows the house rule for reading `CHOOSE`.

## What changed in beta 42

The touch and graphics version (on top of beta 41's fixes): drag either bound of between/outside shading with the area riding the region; two pages of soft keys (More turns the page; page 2 chooses what the arrow keys move); grab μ and σ; live result views (tap to explore, tap a bar); filled histogram bars and bar counts; the shading sweep; the CDF overlay; the z-ruler; "height is not probability"; left-tail and two-tailed critical values; the power picture; three help pages. Details, with line numbers, in `NormExplorer_beta42_CHANGES.md`.

Beta 41 (16 Oct 2026) was a fix version: unnumbered menus, the MicroPython sampler importing from `urandom`, Home exports kept after Quit, the N(0,1) reference cached, flicker-free animation captions, the custom window kept, the Explorer redrawing only on change.

## Credit

Concept, source material, direction, classroom judgement and all hardware testing: Roger Metcalf. Implementation, the numerical work and its verification, and this guide: Claude (Anthropic).

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty.*

*Firmware: builds through beta 39 tested on HP Prime G2 and G1, 2026-09-09 firmware. Betas 42 and 42a have not yet been run on hardware.*
