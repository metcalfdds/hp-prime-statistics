# StudRange beta 15a — User's Guide

The studentized range distribution (Tukey's q) on the HP Prime: p-values, critical values, the Tukey HSD, an interactive plot of the distribution, an H₀ simulation that shows why Tukey's test exists, and an HSD "yardstick" for your own group means. One program with **two engines**: a MicroPython engine (the fast path) and the PPL engine (the fallback, which needs no Python at all).

**Status: beta 15a has not yet been run on hardware.** Beta 15 ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026. The Python bridge, the P-value, the HSD (1.3652, as SciPy) and the plot with its drag all passed, but the plot's soft keys did nothing. Beta 15a fixes the soft keys and the Quit line (below); everything else, the Python block included, is unchanged. The PPL program was last run on an HP Prime G2 and G1 (2026-09-09 firmware) at beta 12, and its MicroPython twin StudRangePy at beta 14b (G2). Beta 15 merges the two, and the Python path in particular has to be tried on a calculator **with the Terminal open** — a Python failure on the Prime is silent (see *The two engines*), and the emulator cannot show one. The arithmetic of both engines was verified off-device against `scipy.stats.studentized_range` (see *Accuracy*); the screens were run through the PPL harness, with the Python block executed against the harness's variables, both with Python answering and with Python failing.

Run `StudRange()` from the Program Catalog. Install the `.txt` by pasting it into the Connectivity Kit editor — **paste, do not retype**: the Python block depends on its indentation. There is no separate `.py` file and nothing goes into the Python app. **StudRangePy is retired**: its features are all in this program, and the old file goes to `_superseded`. If StudRangePy is still on your calculator you may delete it.

## The menu

| Item | What it does |
|---|---|
| P-value from q | P(Q ≥ q) for k means and df error; stores `EP_QPVAL` |
| Critical value q(α) | the q with upper-tail area α; stores `EP_QCRIT` |
| Tukey HSD calculator | q crit and HSD = q·√(MSE/m); stores `EP_QCRIT`, `EP_HSD`; then the **HSD yardstick** (Enter or a tap) |
| Distribution plot | the density and CDF, live q and α, touch, soft keys, the simulation |
| Diagnostics (Python) | a live probe of the Python bridge, and which engine gave the last result |
| Help / About | four pages: the formulas, why q and not t, the two engines, the plot's gestures |
| Quit | returns a summary line to Home, e.g. `StudRange: q crit (k = 4, ν = 28) = 3.8612, p not computed, HSD = 1.3652 (engine: Python)`. It names the k and ν of the q crit it quotes, and says "not computed" for a value you never asked for |

df = 0 means ν = ∞ (the plain range distribution) in the P-value, Critical value and plot forms. In the HSD form, df below 1 means "work it out": k(m − 1).

**Degrees of freedom:** 1 and up when the Python engine answers; 3 and up with the PPL engine. If you ask for df 1 or 2 and Python does not answer, the program says *"df below 3 is not supported: using df = 3. (PPL engine: MicroPython did not answer)"* and carries on with df = 3.

## The two engines, and the badge

Every result is computed by the **MicroPython engine first** (native `erf` and `lgamma`, a secant solver; a critical value in about 1.5 s on a G2). If Python does not answer — no Python firmware, or the script failed — the **PPL engine** does the same calculation (beta 14's code; a critical value takes about a minute).

On this calculator a Python error does **not** stop the PPL program: the traceback goes to the Terminal and the program carries on as if nothing had happened. So StudRange guards every call three ways (Lessons Learned §9): it clears the output first, checks the answer by *using* it, and falls back to PPL. Then it **says which engine answered**:

- **engine badge** under the title of every result page and on the plot: a green panel *engine: MicroPython 1.9.4*, or a red panel *engine: PPL (Python unavailable)*;
- `SR_ENGINE` in Home holds `"Python"` or `"PPL"` for the last result.

If you see the red badge on a calculator that has Python, run **Diagnostics** and look in the Terminal for a traceback.

### Diagnostics

Runs a trivial Python call through the bridge — Python reads k = 3, df = 12, q = 3.5 from the program's variables, computes F(3.5) and writes it back — times it, and checks it against SciPy's 0.930005:

- **Python bridge OK (… ms)** with the value and SciPy's;
- **Python answered, but WRONGLY** — the value it gave (please report the page);
- **Python bridge NOT answering** — no Python firmware, or a Python error; the traceback, if any, is in the Terminal.

It also shows the **last Python mark**: the script writes how far it got into `SR_PZ` (`started`, `read mode 0`, `finished mode 0`), so a silent failure still leaves a trail — type `SR_PZ` in Home after any run to see it. And it names the engine of the last result.

## The result pages

Each page has an orange title bar, the engine badge, the result lines and a dodger-blue footer. A key **or a tap** closes it (it no longer times out after a minute). The HSD page's footer reads *Ent or tap = yardstick, Esc = menu*.

## The HSD yardstick

After the HSD result, Enter or a tap opens a form for up to six group means (the first six if k is larger; the default values are an example, and your own are remembered for the next visit). Then:

- the means sit on a number line (labelled x̄1 … x̄6, staggered so close means do not overprint), with their values listed at the top;
- an **orange bar exactly HSD long** lies under the line;
- **tap two means** (or move with ⇆ and press Enter twice): the program brackets them, starts the bar at the lower one, and prints *|x̄1 − x̄3| = 2.500 > HSD: significant* in **green** or *… ≤ HSD: not significant* in **red**. A third pick starts a new pair.
- Esc returns to the menu.

## The distribution plot

The form asks for k (2–20), df and an observed q (0 = none). The window runs from 0 to where the CDF reaches 0.998 (and far enough to show your q). The cache is built once per k and df — by Python with a red progress bar in roughly 5 to 20 seconds (estimates from StudRangePy's G2 timing, to be confirmed; df 1–3 and df above 50 use more nodes and are the slow end), or by PPL with the same bar (about a minute).

**What is drawn:** the density (blue), the CDF (green, scaled 0–1 on the right-hand axis), q crit (dotted orange) and q obs (dotted red). The tails are shaded in **two colours**: beyond q crit, the α region, light orange; beyond q obs, the p region, light red; where both overlap, darker. When q obs = q crit the two regions coincide and p = α. Above the plot, the **α ladder** — 0.10, 0.05, 0.025, 0.01, 0.005 — as five thin labelled ticks at their q crits (the current rung in orange). A dotted orange line runs from the CDF at q crit (height 1 − α) to the right-hand axis, where a small orange **handle** marks α.

**Header:** k and ν; q obs and p (red); the **q crit box** (α and q crit, orange); the engine badge.

### Gestures and keys

| Do this | It does | Keys |
|---|---|---|
| tap or drag in the plot | q obs follows the finger; p sweeps live | ⇆ step q on round numbers |
| drag up/down on the **right-hand edge** (the CDF axis strip) | sets **any α** — α is a height on the CDF, shown as *α = 0.037* | ⇅ walk the ladder; Menu → Set α |
| tap the **q crit box** | q obs = q crit, so p = α exactly | 0 |
| soft key **α−** / **α+** | next smaller / larger α on the ladder (from a free α: the nearest rung) | ⇅ |
| soft key **k−** / **k+** | k − 1 / k + 1, rebuilds the cache | − / + |
| soft key **df** | type a new df, rebuilds the cache | Menu → Change df |
| soft key **Menu** | the plot menu (below) | Enter |
| — | leave the plot | Esc |

The plot's actions fit in six soft keys (the Menu key opens the rest), so this screen does not use the house **"More"** page key; that convention is for screens with more than six soft-key actions.

The soft keys are drawn with `DRAWMENU` after each frame; a tap in the bottom strip (y ≥ 218) is read by its slot. On the Prime such a tap reaches the program only as a click (a WAIT(−1) type-3 event), with no press or lift: beta 15 listened for a press, which is why its soft keys did nothing on the emulator. Every soft key also has a hardware key.

### The plot menu

| Item | |
|---|---|
| Set α (any value) | 0.001 to 0.5 |
| q obs = q crit | |
| Change k / Change df | rebuild the cache |
| H₀ simulation (Python) | below |
| k = 2 curve on/off (Python) | a grey density for two means at the same df, for comparison |
| Clear the simulation | removes the histogram |
| Help for this plot | the gestures |
| Leave the plot | |

The two Python items are **hidden** when the cache was built by the PPL engine.

### The H₀ simulation (Python only)

Asks for a group size m. The simulation's df is k(m − 1), so if that differs from the plot's df the program says so and rebuilds the plot for it. It then draws **2,000 replicates** of k groups of m values, all from the **same** normal population (H₀ true; `urandom`, Marsaglia's polar method), and for each replicate computes Tukey's q — and checks whether **any** of the k(k − 1)/2 pairwise t tests would reject at α (t crit from `STUDENT_ICDF`, checked, or bisection on `STUDENT_CDF`).

A page reports, for example: *Of 2,000 replicates, 5.1 % exceeded q crit = 3.773 (α = 5.0 %)* — and *Any pairwise t > t crit = 2.179: 11.6 % (3 separate t tests)*. Tukey's q holds the whole family at α; separate t tests do not. The plot then overlays the 2,000 q values as a **40-bin magenta histogram** on the theoretical density, with the two percentages in a panel at the top right.

(Why the two numbers relate: a pair exceeds t crit exactly when the *largest* pair does, so "any t > t crit" is the same event as q > √2·t crit.)

## Why q and not t

For two means (k = 2), **q = t·√2** exactly, so q crit = √2·t crit (two-sided) — the k = 2 curve on the plot is that case. With k means there are k(k − 1)/2 pairs; a t test on each at α finds *some* difference far more often than α — the family-wise error rate. q is the range, the largest pair, so P(q > q crit) = α for the whole family. The H₀ simulation shows both numbers side by side.

## Formulas

q = (x̄max − x̄min)/√(MSE/m). Tukey HSD: n = all k means. Newman–Keuls: n = the span of the pair. Duncan: the N–K q with α* = 1 − (1 − α)^(n−1). Unequal n: use Tukey–Kramer. HSD = q crit · √(MSE/m).

F(q) = ∫ f_s(s) · P_k(q s) ds, s = √(χ²_ν/ν), P_k the CDF of the range of k standard normals (Dunlap, Powell & Konnerth 1977), Simpson's rule in both integrals.

## Accuracy (verify_StudRange.py, against SciPy)

- **MicroPython engine:** critical values within 5×10⁻⁶ (relative) for k 2–20, df 1–20,000, α 0.1–0.001. Beta 15 adds two integration grids at the ends of the df range — s = eᵗ for df below 4, and a window 1 ± 12/√(2ν) for df 51–25,000 — because StudRangePy's grid was off there (df 1, α 0.01: q crit 1–14 % low; df 1,000 and up: no answer). Its own code is unchanged and still does df 4–50 and ∞.
- **PPL engine:** within 0.008 of SciPy for df ≥ 3 (worst case k = 20, df = 3, α = 0.005), after two beta 15 fixes: a window for df above 100 (df 1,000 used to fail) and 48 inner intervals from k = 6.
- **Plot cache:** CDF within 3×10⁻⁴, density within 0.6 % of the peak — curve level. The plot's q crit and p come from this cache by interpolation; the menu modes compute at full precision, and the plot stores nothing.
- **H₀ simulation:** run on the PC with the same code: q > q crit 5.19 %, 5.17 %, 10.10 %, 1.00 % for α = 5 %, 5 %, 10 %, 1 % (10,000 replicates each); the family-wise rates matched P(Q > √2·t crit) within sampling error.

## Home variables

`EP_QPVAL`, `EP_QCRIT`, `EP_HSD` (full precision, from the menu modes); `SR_ENGINE`; the bridge variables `SR_K`, `SR_DF`, `SR_A`, `SR_Q`, `SR_MODE`, `SR_OUT`, `SR_M`, `SR_N`, `SR_TC`, `SR_PZ`; the lists `EP_SRCDF`, `EP_SRPDF` (the plot cache), `EP_SRCD2` (the k = 2 curve) and `EP_SRSIM` (40 bin counts, then q > q crit, any t > t crit, beyond the window, the exact q crit used, and the replicate count).

## First-run checks

In order, least risky first (the details are in `StudRange_beta15_CHANGES.md`):

1. Open the Terminal, then **Diagnostics**: "Python bridge OK" and F = 0.930005.
2. Critical value α = 0.05, k = 3, df = 12 → 3.7729 with the green badge; df = 2 → 8.3308.
3. The plot: the badge, the two-colour tails, the ladder ticks, the soft keys; drag q, drag the right edge, tap the q crit box.
4. The H₀ simulation and the k = 2 curve.
5. On a calculator or emulator without Python (or with the Python block made to fail): the red badge, the df 3 message, the PPL plot.

## Credit

Concept, direction, classroom judgement and all hardware testing: Roger Metcalf. Implementation, the numerical work and its verification against SciPy, and this guide: Claude (Anthropic).

The algorithm descends from **Dunlap, W. P., Powell, R. S. & Konnerth, T. K. (1977)**, "A FORTRAN IV function for calculating probabilities associated with the studentized range statistic," *Behavior Research Methods & Instrumentation* 9(4):373–375 — with native distribution functions in place of their polynomial approximations, a u² substitution (and, in beta 15, the two df-range grids) for degrees of freedom their paper excluded. Tables checked: Harter (1960).

Firmware: not yet run on hardware (written for the 2026-09-09 firmware, 2.4.2); beta 15 ran on the HP Prime Virtual Calculator on 17 Oct 2026.

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty.*
