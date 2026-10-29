# BurrLab beta 1i NOTES (beta 1h's notes; the beta 1i changes are in BurrLab_beta1i_CHANGES.md: the new value and a yellow hourglass at once on a key press, the hourglass blinking through a fit, and the curve at every 3rd column plus the peak's two)

beta 1i = beta 1h with instant feedback and fewer curve points (`BurrLab_beta1i_CHANGES.md`). File:
`/home/claude/new6/BurrLab_beta1i.txt` (4,380 lines, pure ASCII, LF), built from beta 1h by
`make_beta1i.py` (exact replacements; `parts/` is beta 1f's and is no longer the source). Gate: PASS vs
beta 1h (`gate_BurrLab_beta1i_output.txt`). Verify: 3,518 checks, 0 failures
(`verify_BurrLab_beta1i_output.txt`, built by `make_verify_beta1i.py`). Harness only; beta 1h ran on the
G1 and G2 (Explore redraw about 0.9 s; "slow but manageable").
beta 1h = beta 1f with the Explore curves back to PPL in Auto and the Terminal messages pointing to BU_PZ
(`BurrLab_beta1h_CHANGES.md`).

beta 1f = beta 1e with the Python curve bridge fixed after two device faults
(`BurrLab_beta1f_CHANGES.md`): (1) every Up/Down on Explore flashed a Python ValueError traceback,
then PPL drew the plot; (2) on the G2 BurrLab HUNG at the menu and **the On key did not break it**
(paperclip reset). On breaks a PPL loop, so the hang was outside PPL: in the PYTHON() call or the
firmware's Python/Terminal handling after the uncaught errors.
beta 1e = beta 1d with the Explore (Family, Rare) curves computed by the MicroPython engine when the
engine setting allows (`BurrLab_beta1e_CHANGES.md`, with the G1/G2 finding: both run PPL at about
4,500 statements/s).
beta 1d = beta 1c with the Explore (and Family, Rare) redraw rebuilt in layers for speed and a
timing readout (`BurrLab_beta1d_CHANGES.md`, with the before/after counts).
beta 1c = beta 1b with the plot pages relaid out (no two texts may overlap: verify Part F) and the
Explore selection made visible (inverted title piece, footer line; `BurrLab_beta1c_CHANGES.md`).
beta 1b = beta 1a plus a MicroPython engine for the Burr fit, an engine selector (Auto / PPL only /
Python only / Both), timing and an engine badge (`BurrLab_beta1b_CHANGES.md`). Nothing else changed.
beta 1a = beta 1 with the second review's five findings applied (`BurrLab_beta1a_CHANGES.md`).

File: `/home/claude/new6/BurrLab_beta1f.txt` (4,267 lines, pure ASCII, LF). Entry `BurrLab()`, tag
`bu_`, Home exports `BU_C`, `BU_K`, `BU_S`, `BU_LL`, `BU_AIC`, and the fitted summary line is the
RETURN value. It replaces Burr3 v2.4c (tag `b3_`, which can stay on a calculator beside it:
fleet_names 0 collisions over 29 files). Built from `parts/` by `assemble.sh`. Gate: PASS vs beta 1e
(`gate_BurrLab_beta1f_output.txt`). Verify: 3,468 checks, 0 failures under the STRICT hpprime stub
(`verify_BurrLab_beta1f_output.txt`); beta 1e under the same stub: 112 failures
(`verify_BurrLab_beta1e_under_strict_stub.txt`). PPL with a MicroPython engine for the Burr fit (Auto by default,
PPL fallback); exports also BU_JOB, BU_IN, BU_X, BU_GE, BU_GC, BU_OUT, BU_YP, BU_PZ, BU_ENGINE. beta 1e
ran on the G1 and G2 (the two faults above); beta 1f has run only in the PC harness.

## The bridge names (beta 1f; grep of the #PYTHON block, checked by verify Part J)

The block hands hpprime.eval only these names: **BU_JOB, BU_IN, BU_X, BU_GE, BU_GC** (read;
`SIZE(BU_IN)`, `SIZE(BU_X)`, `SIZE(BU_GE)`, `SIZE(BU_GC)` too), **BU_OUT, BU_YP, BU_PZ** (written).
All are EXPORTed. No file-level LOCAL (buXxx) is named anywhere in the block. Mode 5's BU_IN is
{C, K, S, x max, columns, view, frame bottom, frame top, frame left} (9 values; beta 1e read
buPB, buPT, buPL from Python -- file-level LOCALs, invisible to hpprime.eval -- the ValueError).

## Lessons Learned notes (for v7t)

* **Test stubs for hpprime.eval must expose only EXPORTed names.** A stub that resolves any
  harness global (file-level LOCALs included) hides exactly the bug the calculator shows first.
  The beta 1f stub reads the program's `EXPORT NAME;` lines; any other name comes back as its own
  text (float() then fails as on the device) and an assignment to one raises.
* **A Python block catches its own errors.** main() runs inside try/except; an error writes
  BU_PZ = "error: <message>" and the failure sentinel -2, and nothing is printed. An uncaught
  error prints a traceback on the screen every call.
* **Validate before looping.** Every Python loop is bounded by a checked input (columns 1..320,
  frame height 1..240, list sizes 0..20,000, mode 0..5, finite positive C, K, S, x max; NaN fails
  every check).
* **Fail once.** After one Python failure (no sentinel, or an answer the guard refuses) PYTHON()
  is not called again in the session (buPyBad) until the engine setting is chosen again.
* **The On key does not break a stuck PYTHON() call** (beta 1e, G2): only a PPL loop is
  breakable. No PPL loop may wait or poll for a Python result; PYTHON() is one call and the answer
  is read once afterwards (verify Part K checks no WHILE/UNTIL condition reads BU_OUT/BU_PZ/BU_YP).

## What it does, menu by menu

1. **Explore the Burr XII** — pdf (blue) or CDF (magenta, soft key 5 toggles; a right-hand 0–1
   axis in CDF view) over 0 to the 0.995 quantile (capped at 50 S, said on screen). Soft keys
   C, K, S, x₀ choose what the arrows and a sideways drag change (C, K by 0.1 per arrow and
   0.01 per pixel; S by ×1.1 and ×1.02 per pixel; x₀ by a 1-2-5 step); +/− slide x₀; 0 cycles
   the choice; a tap puts x₀ there; Enter is a CHOOSE of every action; Esc back. The window is
   held while a finger is down and refitted on the lift (Burr3's idiom); x₀ snaps to a 1-2-5
   grid on the lift. Dotted markers: mode (orange), median (magenta), mean (green); past the
   window they are named at the right edge with an arrow. The tail beyond x₀ is shaded under
   the pdf by pixel column; a red line and dot mark x₀. Status rows: x₀, pdf, P(X > x₀); mode,
   median, mean, SD (when they exist); the moment case ("K×C = 3.00: mean and variance exist" /
   "mean exists, variance infinite" / "NO mean (heavy tail)", the last in red, with "heavy
   tail: no finite mean" on the plot). Floors: C, K ≥ 0.2 (K×C may be as small as 0.04), S in
   [0.01, 1E6]. pdf and CDF caches per pixel column, refilled only when C, K, S or the window
   change.
2. **Family tree** — the pdf on the left (a 164-px-wide plot), a (C, K) "shape map" on the
   right: log₂ axes from 1/4 to 16, three bands coloured by the moment case (red: no mean;
   orange: mean only; green: mean and variance), the Lomax line C = 1 (orange) and the Fisk
   line K = 1 (magenta), drawn once into G2 and blitted each frame; the current (C, K) is a
   red dot. Tap or drag in the map to set C, K (snapped to 0.05 in log₂, and to exactly 1
   within 6 %); drag in the plot (sideways = C, up = K, 0.01 a pixel); soft keys C−, C+, K−,
   K+, Weibl, More / Lomax, Fisk, Reset, Help, Menu; keys L/R = C, U/D = K, +/− = S, 0 = the
   Weibull animation. Names on screen when reached: "C = 1: Pareto II (Lomax), shape K = …",
   "K = 1: log-logistic (Fisk), shape C = …", "C = K = 1: Lomax and log-logistic at once",
   otherwise "Burr XII = Singh-Maddala (income economics)". The Weibull limit animates K = 1,
   2, 4 … 128 with S = Sw K^(1/C) (Sw = the Weibull scale the current Burr implies, S K^(−1/C)),
   the target Weibull(k = C, λ = Sw) drawn in green dots under the blue Burr, about 0.5 s a
   frame (TICKS-paced; Esc stops it).
3. **Fit my data / a preset** — CHOOSE: BJS, Rossi, Danish 300, Danish 2,156 binned, My data
   (D1 of Statistics 1Var: ≥ 5 positive values, ≤ 1,000, not all equal; first read inside
   IFERR), Results of the last fit. A data page shows the source lines, n, min, max, mean,
   median, max/median and a note (small n; censoring excluded; the heavy-tail facts; "binned:
   grouped likelihood"). Enter runs the fit with a progress bar (Esc abandons it: nothing is
   kept, a MSGBOX says so). Results page: C, K, S with SEs, ln L, AIC, BIC, the moment case,
   median/mode/mean/SD, the SE caveat ("with n = 41 they are rough (and wide)"), boundary
   flags in red (a Weibull-limit fit says the explorer shows its Weibull-equivalent at
   K = 50; a Pareto/box-limit fit says the explorer keeps its own shape), A². Soft keys: Table, Hist, Q-Q, Surv, Hazrd, More / A-D, Data, Rare, Explr,
   Menu; Enter = a CHOOSE of the same.
   - **AIC table**: Burr XII and the five rivals: k, ln L, AIC, AIC − best, "best" in green,
     "exp" beside a Lomax that ran to its exponential limit, "not fitted on bins" for the
     gamma on grouped data; Burnham & Anderson's reading of differences; a verdict line
     ("Here Lognormal beats the Burr XII by 4.4." / "within 2: about equal" / the Weibull-limit
     explanation).
   - **Histogram**: density bars (1-2-5 width from 0, or a 1-2-5 fraction of a decade on a
     log₁₀ axis with density per log unit; +/− toggles; the grouped preset uses its own 60
     bins) with the fitted Burr (blue) and the best rival by AIC (its colour).
   - **Q-Q**: sorted data against the Burr quantiles at (i − 0.5)/n, log-log when
     max/median > 30; tap a point or Left/Right to read "#i/n: x, model, p"; refused for bins.
   - **Survival, log-log**: empirical P(X > x) = 1 − (i − 0.5)/n (bins: from the cumulative
     counts), the Burr, the best rival, and the Pareto asymptote log₁₀ SF = −K C (log₁₀ x −
     log₁₀ S) in red dots with "slope −K×C = …" (omitted at the Weibull limit).
   - **Hazard**: f/SF for the Burr and the best rival over the data's range, with the C > 1 /
     C ≤ 1 reading and the exponential's flat hazard named.
   - **A-D statistic**: A² = −n − (1/n) Σ (2i − 1)[ln F(x₍ᵢ₎) + ln(1 − F(x₍ₙ₊₁₋ᵢ₎))] from ln SF
     (no cancellation in a far tail); the page says plainly that NO p is printed (no table
     for the fitted-parameter case; a parametric bootstrap is too slow on a G1) and gives
     D'Agostino & Stephens's fully-specified 10/5/1 % points 1.933/2.492/3.857 with the
     warning that fitted parameters make the true points smaller.
4. **The mean that never settles** — draws from the current Burr by the inverse CDF (RANDOM;
   Seed soft key → INPUT → RANDSEED inside IFERR, ResampLab's shape), 1, 10 or 100 draws a
   frame (x1/x10/x100 soft keys or +/−), the running mean (blue) and running median (magenta)
   traced across 0..2,000 draws, the true mean as a green line when it exists and the true
   median as magenta dots; the y-window doubles and the trace is redrawn when the mean leaves
   it; the moment case in words, red when K×C ≤ 1 ("NO mean. The law of large numbers has
   nothing to aim at; the median settles at …"). Each frame appends a segment and blits (no
   full redraw), with GETKEY/MOUSE polled between frames; the median is a SORT of the draws so
   far. Esc stops.
5. **How rare is this?** — the fitted model's pdf (or the explorer's if no data) with the tail
   beyond x shaded, the data as a red rug; P(X ≤ x) and P(X > x) with their relation (never
   "= <"), "1 in N" to two significant figures, the model percentile, and the empirical count
   and percentile ("Data: 2 of 41 above x (4.9 %), pctile 95.1"; bins: "about … to the bin
   edge"). x−/x+ soft keys and arrows, Type (INPUT), a tap on the plot sets x.
6. **Exact moments (CAS)** — E[X^r] = S^r K B(K − r/C, 1 + r/C) for r = 1, 2, 3 with C, K, S
   rounded to 3 decimals (said on screen; the decimal uses the same rounding so the two are
   comparable). One `bu_Cas` (ChiTable's fence); `simplify(S^r*K*Beta(K-r/C,1+r/C))` with the
   numbers as integer fractions /1000 for the display, `evalf(...)` for the check by value
   (1E-6 relative against the Lanczos value); badge "exact (CAS)" or "decimal"; a closed form
   over 60 characters is not printed ("its 87-character Gamma form not shown"). A live probe
   (`evalf(Beta(1,3/2))` = 2/3) runs once before the page. For C = 2, K = 1.5, S = 10 the CAS
   gives E[X] = 10 and E[X²] = 200 exactly; for C = K = 2, S = 10 it gives 5π/2.
7. **Help** (3 pages), **Quit** (RETURN the summary; BU_* set).

## Formulas and sources

Parameterisation = scipy.stats.burr12(c = C, d = K, scale = S): f = (C K/S)(x/S)^(C−1)(1 + z)^(−K−1),
F = 1 − (1 + z)^(−K), z = (x/S)^C (Burr 1942; Tadikamalla 1980; Kleiber & Kotz 2003 ch. 6).
Everything in logs (Burr3 v2.4b's lesson): ln SF = −K ln(1 + z) with ln(1 + z) = ln z past
ln z = 30 and log1p below; CDF = −expm1(ln SF); quantile x = S exp(ln((1−p)^(−1/K) − 1)/C) with
the inner term as expm1(−log1p(−p)/K), the exponent capped at 500 (the Prime's EXP overflows
to ∞ without an error). E[X^r] = S^r K B(K − r/C, 1 + r/C) via the Lanczos log-gamma, finite
iff K C > r; mode S((C−1)/(KC+1))^(1/C); median S(2^(1/K) − 1)^(1/C); hazard
(CK/S)(x/S)^(C−1)/(1+z). MLE: the profile over K (K̂ = n/Σ ln(1 + zᵢ)) leaves a 2-D Nelder-Mead
(1965) over (ln C, ln S) from the best of an 18-point grid, tolerance 1E-10 relative on ln L
and 1E-6 on the simplex, cap 400 iterations, a box ln C ∈ [−4, 7], ln S ∈ [ln min − 6, ln max
+ 6] (outside = penalty). Boundaries are named: the Weibull limit = S at the top of its box OR (beta 1a) a Burr ln L
within 1E-4 (1 + |ln L|) of the Weibull rival's MLE with K > 100 (grouped: S within 1 of the
box top or K > 1E4); K, S → ∞ with S K^(−1/C) fixed and the Weibull(k = C, λ) is printed; the
explorer then holds the equivalent at K = 50; C at its top with S at the
smallest value = the Pareto limit ("the data start at a floor"); anything else at the edge =
"treat with suspicion". The rivals are fitted before the SEs (the limit test needs the Weibull's ln L). SEs: the
observed information −H from central differences of ln L in (C, K, S) with relative step 1 %,
inverted by cofactors (a 9-element list); skipped at a boundary. Rivals on raw
data: exponential (x̄), lognormal (μ̂ = mean ln x, σ̂ with divisor n), Weibull (shape by 42
bisections on ln k of the profile equation, x^k formed as exp(k(ln x − ln x_max))), gamma
(Newton on ln a − ψ(a) = ln x̄ − mean ln x from Minka's start, ψ and ψ' by shift-and-series),
Lomax (K profiled, a 1-D simplex over ln S; at the top of the box it IS the exponential and
its row takes the exponential's ln L, flagged "exp"). Grouped data: Σ nⱼ ln(SF(eⱼ₋₁) − SF(eⱼ)),
bin 1 from 0, the last open; a 3-D simplex for the Burr from a 48-point grid, 2-D simplices
for lognormal, Weibull, Lomax, 1-D for the exponential, the gamma skipped (an incomplete
gamma per edge per step: too slow on a G1) and said so. AIC = 2k − 2 ln L, BIC = k ln n − 2 ln L
(Burnham & Anderson 2002 §2.6 for the differences). A²: Anderson & Darling 1952; the critical
points D'Agostino & Stephens 1986 Table 4.2 (case 0). Danish data: McNeil 1997 ASTIN Bull
27(1):117 and evir (`data/DATASETS_BURR.md`).

## What was checked (verify_BurrLab_beta1a.py: 2,667 checks, 0 failures)

A1 Lanczos, digamma, trigamma, log1p, expm1, the incomplete gamma (both tails) against SciPy.
A2 pdf, ln pdf, ln SF, CDF, hazard, quantile, mean, SD, median, mode, moment case against
scipy.stats.burr12 on 12 shapes (C, K up to 400; S from 0.01 to 20,978) × 11 x-values from
1E-6 S to 1E6 S and 9 probabilities (the capped quantile checked as capped). A3 E[X^r],
r = 1..3, against mpmath's Beta. A4 the MLE on BJS, Rossi, Danish 300 and 20 random samples
(n = 8..150 from Burr, lognormal, Pareto, gamma) against a SciPy Nelder-Mead on the same ln L:
every interior fit agrees to 1E-6 in ln L and 1E-3 in the parameters, and the program's ln L is
never below SciPy's; every boundary fit is within 2E-3 of the free optimum, and the Weibull-limit
fits reproduce scipy's weibull_min fit (k, λ). A5 SEs against a 30-digit mpmath Hessian, 1 %
(raw and grouped). A6 the five rivals against scipy.stats fits (ln L to 1E-5, parameters), AIC
rows, the best rival, the Lomax limit. A7 the grouped likelihood against NumPy at 12 Burr and 5
rival parameter sets; the grouped Burr and three grouped rivals against SciPy minimisations.
A8 A² against the hand formula (and the formula's shape against scipy.stats.anderson). A9 300
draws and the simulation page replayed from the same seeded RANDOM: every draw, running mean
and running median equal; the heavy-tail page says NO mean. A10 seven CAS templates through
desktop Giac (10, 200, 5π/2, 40π√3/9, …) checked by evalf against SciPy's Beta; the page badge
with cas = giac and cas = fail. A11 n = 5, ties, a huge value, tiny values, n = 1,000 (fit
and every page); negative, short, empty and all-equal D1 refused with a message. Part B: every
menu path with cas = giac and fail and once in stale-key mode; Part D (beta 1a): the Weibull-limit
detection on the reviewer's 16 samples and 20 fresh ones (no flag-0 fit with K > 1E4, no missing
SEs, no absurd slope; every flag-1 fit equals the Weibull MLE and the explorer holds K = 50 with λ
kept; flags 2/3 leave the explorer alone; no ∞ or scientific number on any page), bu_Median and
bu_Num caps, the list simplex reproducing the BJS optimum, the A-D and Danish wording: the numbers on the pages
(explore readouts on 20+ frames, the family names and S = Sw K^(1/C) on the animation frames,
C/K/S/SE/ln L/AIC/BIC/A² on the results pages, every AIC-table row, the Q-Q readouts, the rare
page's probabilities and counts), layout (6.5/8/9.5 px per character, nothing off screen or
under the soft keys), no scientific strings, MSGBOX ≤ 5 lines, no runtime error, no stale
skips, Esc out of a fit.

## G1 cost and the first G1 timing (calibration)

Objective evaluations (each a loop over n with about 3 statements per value, plus the Hessian's
19 full evaluations, the Weibull's 42 × n and the Lomax's ~60 × n): BJS 160 evaluations
(~20k loop statements), Rossi 229 (~78k), Danish 300 138 (~124k; with the rivals and Hessian
about 290k in all), the binned set 501 evaluations × 60 survival values (~90k), n = 1,000
128 (~384k for the Burr alone). At the 10–30k statements/s a G1 has shown (StudRange's
60-step bisection in about a minute) that is roughly 2 s (BJS), 5 s (Rossi), 10–30 s (Danish
300 and the bins), and 1–3 minutes for 1,000 values. The brief's threshold for a Python engine
was 60 s at n = 300; the estimate was under it, so beta 1 was pure PPL. **Measured (Roger, G1,
beta 1a): the Danish 300 fit took 45 s**, so this G1 runs this loop at about 6,500 statements/s,
about 2× slower than the 30–100× rule gave: use 5,000–7,000 statements/s for loops of this kind
(LN, EXP, list reads) when estimating G1 time. beta 1b therefore carries the MicroPython engine as
a trial; the PPL rivals (about a third of the PPL time) remain, so the whole Danish 300 fit should
drop to roughly 15–20 s with Python answering, the Burr part itself to a second or two.

## Left out, and why

- A p-value for A² (no table for the fitted-Burr case; a bootstrap is too slow): the page says
  so. The gamma rival on binned data (too slow): said on the table. A second BJS table (no
  raw-value table verified against a second source). The Burr3 S-curve "inverse" drag (p from
  the finger's height) is not carried over: the Explore page's CDF view shows the CDF point at
  x₀ instead, and How rare gives the inverse by typing.
- The grouped SEs and AICs treat the bins as the data (standard for grouped likelihood).

## Three things most likely to go wrong on a real G1 (beta 1b)

00. (beta 1f) The hang. Its cause on the G2 is not known: the audit found no PPL loop waiting on
   Python (so a TICKS cap or Esc check has nothing to guard) and every Python loop is now bounded
   by validated inputs. Remaining suspects, none reproducible in the harness: the firmware's
   handling of repeated uncaught tracebacks (now none: the block catches its own errors), and the
   MicroPython heap after many PYTHON() calls (one per redraw, the 500-line script compiled each
   time). If it hangs again, note how many presses it took and whether the Terminal had text.

0. The bridge itself: `hpprime.eval` reading a list element by element (`BU_X(i)`), the
   `BU_OUT(j):=` writes, `hpprime.fillrect`; a silent Python death shows as the PPL badge (Auto)
   or the failure message (Python only), with BU_PZ saying how far the script got.

1. Speed of the fit on the Danish 300 and binned presets (estimate above): the progress bar
   and Esc are there; the checklist times it.
2. The simplex and Hessian are now plain LOCAL lists (beta 1a), the proven shape; the
   remaining untested shape is the `bu_SxRow` list copy inside `bu_NM`'s insertion sort.
3. The simulation's per-frame SORT of up to 2,000 values and CONCAT growth at x1 speed
   (2,000 frames); x10 is the default. RANDSEED has not run on our calculators (inside IFERR).

## DEVICE CHECKLIST (in order; expected numbers from the harness)

1. Program Catalog → BurrLab → Check: compiles. Run `BurrLab` from Home: the opening page shows
   the DISCLAIMER; any key → the 8-item menu.
2. Explore — FIRST the beta 1f fixes, on BOTH calculators (save work first: the beta 1e hang
   needed a paperclip reset). Engine Auto, Explore, press Up/Down 20 times: no traceback may flash
   and the readout must say ", py". Esc to the menu, Explore again, 20 more presses, Esc, Quit:
   no hang. In Home, BU_PZ reads "finished mode 5". If a traceback or ", py FAIL, PPL" appears,
   read BU_PZ (it now holds "error: <message>") and report it. If it hangs, try On once
   (beta 1e: On did not break it) and report how many presses it took.
   THEN READ THE READOUT (beta 1e): More > Timing turns on the grey readout at the
   right of the footer, "c 25 d 120 w 2 ms, py". With the engine at Auto (Fit menu > Engine)
   press Up: expect c well under beta 1d's 757/868 ms and ", py" (the Python engine made the
   curve; BU_PZ in Home reads "finished mode 5"). If it reads ", py FAIL, PPL" the bridge
   failed: read the Terminal and BU_PZ. Then Engine > PPL only: ", PPL" and c about
   1 s (the fallback path). Then Engine > Both: ", py = PPL" (every segment equal) and c
   about the sum. Report the three numbers from the G2 and the G1 for each engine after an
   arrow press (C chosen), after a + press (x₀ move) and after a tap in the plot. If d dominates, the primitives are the cost (TEXTOUT_P, the blits, FILLPOLY_P); if
   w is large, something waits between the key and the redraw. The tail shade is now a
   translucent polygon over the curve (FILLPOLY_P, alpha 128: first hardware use in this
   program; GfxProbe showed it on the emulator); the markers are thin solid lines.
   LAYOUT (beta 1c): the title row reads C = 2.00 K = 1.50 S = 10.00
   x₀ = 15.00 with "C = 2.00" in a WHITE box (orange text); the plot ends at y 153 with its
   tick labels 0, 10, 20 … in their own row under it; "mode", "median", "mean" labels in
   three separate rows beside their dotted lines; "pdf" bottom-left and "K×C = 3.00: mean and
   variance" bottom-right inside the frame; then "x₀ = 15.00, pdf 0.0236, P(X > x₀) = 0.1707",
   "mode 5.000, median 7.664, mean 10.000, SD 10.00", "K×C = 3.00: mean and variance exist"
   and the footer "C chosen: arrows/drag. +/- x₀, 0 next, Ent". Tap soft key K: the white box
   moves to "K = 1.50" and the footer reads "K chosen …" (press the key about 0.3 s on the
   emulator). Set C = 1.18, K = 1.08, S = 0.8254 (the Danish fit) and check the three marker
   labels no longer pile up. Right twice: C = 2.20. Soft key K, Up: K = 1.60.
   Soft key S, Left: S = 9.091. + : x₀ = 18.00 (the step is 1/40 of the window, 1-2-5). Soft
   key CDF: magenta S-curve, right axis 0/.5/1, a dot at x₀. Drag sideways with S chosen: S
   changes 2 % a pixel, the window frozen until the lift. Soft key x₀ then tap: x₀ jumps there
   (snapped). More → Reset → C, K, S back to 2, 1.5, 10. Drag C and K down until K×C ≤ 1: the
   red "heavy tail: no finite mean" and "mean none". Enter: the 8-item CHOOSE. Esc: menu.
3. Family tree: tap the map near its centre-left column (C = 1): "C = 1: Pareto II (Lomax),
   shape K = …" appears in purple. Soft key Fisk (page 2): "C = K = 1: Lomax and log-logistic
   at once", "K×C = 1.00: NO mean (heavy tail)" in red. Reset, then Weibl: eight frames,
   K = 1 … 128, S from 8.165 up to 92.38 (C = 2, Sw = 8.165), the blue curve settling onto the
   green dots; last line "K = 128, S = 92.38: near Weibull(2.00, 8.165)". Time the animation
   (expected about 4–8 s on a G1).
4. Fit → BJS: the data page says n = 41, min 115, max 216, mean 155.1, median 150, "n = 41 is
   SMALL". Enter: a progress bar (time it; expected a few seconds). Results: C = 10.84 (SE
   3.596), K = 0.8981 (SE 0.7267), S = 150.1 (SE 18.13), ln L = −191.14, AIC = 388.27, BIC =
   393.42, "K×C = 9.74: mean and variance exist", median 152.3, mode 148.9, mean 155.0, SD
   27.86, A² = 0.233. Table: Lognormal best (ln L −189.95, AIC 383.89), Gamma +0.46, Burr XII
   +4.38, Weibull +6.05, Exponential +113.71, Lomax +113.71 with "exp"; verdict "Here Lognormal
   beats the Burr XII by 4.4." Hist: 11 bars, blue Burr, magenta lognormal; +: the log
   version (14 bars of 0.02 dex). Q-Q: tap the top point: "#41/41: x 216.0, model 235.9,
   p 0.988". Surv: "Pareto line, slope −K×C = −9.74". Hazrd: the Burr rises then falls. A-D:
   the honesty page. Rare: x = 216 at first ("Data: 0 of 41 above x"); Type 200: "P(X ≤ x) =
   0.9410, P(X > x) = 0.0590", "pctile 94.1; how unusual: 1 in 17", "Data: 2 of 41 above x
   (4.9 %), pctile 95.1".
5. Fit → Rossi: results "C = 2.047   K → ∞", "S → ∞", ln L = −465.39, the red WEIBULL LIMIT
   paragraph with Weibull(k = 2.05, λ = 32.24), "not a power law", "Explore, Rare and the CAS
   page show its Weibull-equivalent at K = 50", A² = 1.630. Explr (page 2): the title reads
   C = 2.05 K = 50.00 S = 218.1 (λ 32.24 × 50^(1/2.047)). Rare: "model: Weibull-equivalent,
   K = 50" on the plot. Table: Weibull best (−465.39),
   Burr XII +2.00, Gamma +13.41, the green "exactly 2" line. Surv: "Weibull limit: no Pareto
   line".
6. Fit → Danish 300: time the fit (the brief's 60-s line). Results: C = 1.183 (SE 0.1004),
   K = 1.079 (SE 0.2236), S = 0.8254 (SE 0.2250), ln L = −453.28, AIC = 912.56, "K×C = 1.28:
   mean exists, variance infinite", "mean 3.161, SD: none (infinite variance)", A² = 0.323.
   Table: Burr XII best, Lomax +1.94 ("within 2: about equal"), Lognormal +10.45, Weibull +72.41,
   Gamma +146.87, Exponential +278.26. Hist opens on the log axis. Surv: slope −1.28, the
   points near the red dots in the far tail. Rare at x = 151.4: "pctile 99.9; how unusual: 1 in
   780", "Data: 0 of 300 above x". The data page says "1980-1990, in 1985 prices
   (inflation-adjusted DKK); excess over 1M DKK".
7. Fit → Danish 2,156 in 60 bins: time the fit. Results: "Grouped maximum likelihood, n = 2156
   in 60 bins", C = 1.138 (SE 0.0363), K = 1.228 (SE 0.1046), S = 1.023 (SE 0.1182), ln L =
   −7060.90, "K×C = 1.40". Table: Burr best, Lomax +14.34, Lognormal +62.09, Weibull +379.98,
   Gamma "not fitted on bins", Exponential +1365.68. Q-Q: the MSGBOX refusal. A-D: "No A² here".
8. The mean that never settles (LAYOUT: "draws" top-right inside the frame, the y-max label
   above the frame at the left, "true mean"/"true median" labels beside their lines never on
   the legend rows; the status row shows the speed, "n = 120 (x10): mean …", and changes when
   x1/x100 is pressed mid-run) (from the menu, with the explorer at C = 2, K = 1.5, S = 10 or
   the last fit): the green "true mean" line and magenta dotted "true median"; x10 runs 200
   frames (time it); x100 is near-instant; x1 is slow (2,000 frames) — note the time per
   frame. Seed 5, Reset: the same trace twice (RANDSEED has not run on our calculators: if the
   two runs differ, say so). With the Danish fit loaded (K×C = 1.28) the mean trace jumps on
   every big draw; set C = 0.75, K = 0.8 in Explore first and run again: the red "NO mean"
   lines, the mean wandering, the median settling at 7.66.
9. Exact moments with the explorer's 2, 1.5, 10: "E[X^1] … = 10.000 [exact (CAS)]" and
   "= 10"; "E[X^2] … = 200.0 [exact (CAS)]", "= 200"; E[X^3] does not exist (K×C = 3). Note
   the time of the page (six CAS calls). Set C = K = 2: "= 5*pi/2". After a BJS fit: the
   badge reads "exact (CAS), its 87-character Gamma form not shown" (or thereabouts).
10. Help: four pages by Right; Esc. Quit: Home shows "BurrLab: BJS: … Burr XII C = 10.84, K =
    0.8981, S = 150.1, ln L = −191.14, AIC = 388.27" (or the last fit); `BU_C`, `BU_AIC` hold
    the numbers.
11. ENGINE TRIAL (beta 1b). Open the Terminal first (Lessons Learned section 9: a Python
    traceback prints there and PPL carries on). Fit → BJS with the engine at Auto: the badge
    must read "engine: MicroPython 1.9.4, x.x s" (green); if it reads "engine: PPL (Python
    unavailable)" (red) the Python side failed silently: type BU_PZ in Home (expected
    "finished mode 3" after a raw fit with SEs, "finished mode 1" when the Hessian was skipped)
    to see how far the script got, read the Terminal, and report the traceback; the numbers are
    still right (the PPL engine answered). Then Fit → Engine → Python only and fit BJS: same
    badge, or the plain message "Python engine failed: see the Terminal". Then Engine → PPL
    only: badge "engine: PPL (chosen), x.x s" (the beta 1a numbers, unchanged).
12. THE DEMO: Engine → Both (compare), Fit → Danish 300 (the harness says 45 s for PPL on this
    G1): the progress bar runs twice; the results page shows "Py x.x s, PPL 45.x s: same C, K, S
    to 6 digits" (on the device the two engines round differently — 12-digit BCD against
    doubles — so a difference of about 1E-6 is possible: the line then prints the largest
    relative difference, and anything below 1E-5 is agreement) and the badge "engine:
    MicroPython 1.9.4 (compared)". Time the whole fit; note it beside the beta 1a 45 s. Then
    Both on the Danish bins (the grouped path, 3-D simplex). Home after Quit: the summary ends
    "engine: MicroPython 1.9.4 (xx.x s)"; BU_ENGINE holds the text.
13. My data: put 30 Weibull-shaped values in D1 (e.g. the cubes of 30 uniform numbers × 10):
    the fit must report the WEIBULL LIMIT, not a huge K with "not positive definite".
14. A-D page: the Stephens (1986) sentence and "only ranks fits"; no "reassuring".
15. Help page 4 (Engines) reads and the Fit menu shows "Engine (now: Auto)".
16. Stale keys: close the fit menu's data page with Enter held a moment: the results page must
    not be skipped. A light tap on each soft key registers (as on 20 Oct).
