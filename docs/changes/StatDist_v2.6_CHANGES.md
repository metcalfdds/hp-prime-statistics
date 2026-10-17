# StatDist v2.5 -> v2.6: what changed, and what to test on the calculator

*16 October 2026. The touch/graphics expansion from Fleet Review 2026-10-16 v1 section 6 ("StatDist v2.4 -- the biggest rebuild"), built ON TOP OF the v2.5 fix version with every v2.5 fix kept. v2.6 has NOT been run on hardware.*

Files (all in ``):

- `StatDist_v2.6.txt`: 3,176 lines (v2.5 was 1,380).
- `verify_StatDist.py` and its output `verify_StatDist_output.txt`: the PPL dispatch against SciPy.
- `run_StatDist_v2.6.py` and its output `run_StatDist_v2.6_output.txt`: the scripted UI runs.
- `statdist_harness_v1.py`: the runner (see note H).
- This note.

Line numbers: "v2.5 n" refers to the fix version, "v2.6 n" to the new file.

**Note H: the harness.** `tools/ppl_run_v1.py` did not exist in this session (searched the whole filesystem), so I wrote `statdist_harness_v1.py` to do the same job on hp-prime-kit's interpreter. It provides:

- scripted CHOOSE and INPUT answers that write the variables;
- a GETKEY/MOUSE scheduler that only delivers an event after the program has drained and is polling (a touch is a list of finger samples, one per `MOUSE` call, then the lift);
- TICKS;
- SciPy-backed NORMALD*/STUDENT*/CHISQUARE*/FISHER*/BINOMIAL*/POISSON*/COMB;
- ATAN/TAN in radians, degrees or grads;
- STRING modes 1 and 2;
- a record of every TEXTOUT_P/DRAWMENU/MSGBOX per frame.

It also flags any `POISSON_CDF(λ, k<0)` call and any CHISQUARE_* call with a non-integer df.

## (a) The changes

1. **The drawn result screen `st_Plot`** (new, v2.6 2834; drawing in `st_Draw` 2418, `st_DrawCurve` 2243, `st_DrawBars` 2282, `st_Panel` 2340). It replaces the v2.5 `st_Page(...)` call at the end of each `st_calc_*` (v2.5 370, 431, 484, ... 1379).
   - Continuous distributions:
     - the pdf in blue `#003CC8` over a grid at nice values (`st_Nice` = Norm3's rounding NiceNum);
     - the requested area shaded column by column in `#AACDFF`;
     - x as a red line (a and b for Between; the bound the arrows move is drawn 2 px wide);
     - the mean as a green dotted line, `PIXON_P ... STEP 4`, drawn only when the mean exists.
   - Discrete distributions draw pmf bars with `RECT_P`:
     - counted bars are filled; uncounted bars are outlined;
     - the chosen k is red: filled when it is counted, outline-only when it is not, so P(X > 3) shows bar 3 empty;
     - a red tick under the axis marks the chosen k even when its bar is too short to see.
   - The orange-framed panel `RECT_P(G1,0,152,319,217,orange,light orange)` holds five lines:
     - the parameters (`st_ParStr`);
     - mean and sd, in green, or "undef ...";
     - "f(x) = 0.2420: a density, not a probability" (for discrete, "P(X = 3) = ...: the red bar");
     - the probability in magenta, font 2; discrete P>k reads "P(X > 3) = P(X >= 4) = ...";
     - one note line (see item 3).
   - Window (`st_Fit`, 2096):
     - continuous: from the 0.1 % to the 99.9 % quantile. Each side is cut at 8 IQRs beyond its quartile, which catches Cauchy, Pareto, t(1-2), LogNormal(0,1) and Fréchet. The plot then prints "1.9% beyond >>" / "<< 1.9% beyond" in grey for the mass outside the window, so a cut tail is never silent.
     - A finite support end close to the window becomes its edge (Exponential starts at 0). A support finite at both ends (Uniform, Triangular, Beta) is shown whole, plus 5 %.
     - Discrete: the whole support up to 41 values, otherwise the 0.1-99.9 % k's, at least 9 bars and at most 251.
     - The window stretches to show a typed x (Norm3's idiom).
   - Cache (`st_Cache`, 2162): the pdf, the CDF and the pixel height for every column (or bar) are built once per parameter or window change. Every frame, including each drag sample, evaluates nothing.
   - The y top ignores the two end columns, so a density that is unbounded at 0 (chi-square(1), Gamma k < 1) does not flatten the curve. It is clipped instead, and the note says "curve clipped at the top of the plot".
   - The dispatch `st_pdf(id, plist, x)` (662) and `st_cdf(id, plist, x)` (804), plus `st_icdf` (971), `st_Mom` (1023), `st_ParStr`, `st_DefAB`, `st_ABHelp`, `st_Sup`, `st_Name`, `st_Use` and `st_Def`, form one section: section 4, "THE DISPATCH". Each takes the parameters packed in one list {p1, p2, p3}, which keeps every call under the 16-argument limit.
2. **Touch** (`st_Drag` 2658, `st_Plot` loop):
   - A tap or drag in or just around the plot box moves x (or k).
   - The shading and the panel follow the finger, reading `stPd`/`stCd` at the finger's column; that value is exact, because the finger always sits on a cached column.
   - On lift, x snaps to the grid `stGs = st_Nice(width/60)`, for example 0.1 on N(0,1), and P is recomputed exactly.
   - The window is frozen during a drag. Esc, or a reading off the screen, also ends the drag.
   - Soft keys (DRAWMENU after the blit, every frame; slot `MIN(6, IP(x/53.4)+1)`):
     - Page 1 is **{P<=x, P>x, a<X<b, Zoom−, Zoom+, More}**; P<=k / P>k on discrete plots.
     - P<=x and P>x change the tail in place.
     - a<X<b starts a two-tap set-up: the panel says "tap the plot to set a", then "... b". After that, a drag moves the nearer line.
     - Zoom± halves or doubles the window about x (about the middle of a..b) and rebuilds the cache.
   - Keys:
     - Left/Right step to the next grid line (typed 1.96 -> 2.0 -> 2.1, NormExplorer's idiom); x walking off the plot pans the window.
     - Up = upper tail and Down = lower tail. In a<X<b, Up/Down choose which bound the arrows move (b/a).
     - + and − zoom; 0 refits; Enter = options; Esc = back to the menu.
   - The capped `st_Drain` and `st_WaitAny` are the house shapes.
3. **The "More" soft-key page** (house convention, Roger 16 Oct 2026; BRIEF_TOUCH last section).
   - Slot 6 is "More" on every page and flips between the two pages (`stSKP`, file-level).
   - Page 2 is **{Edit, Numbers, CDF, Approx | N(0,1) | Refit, Menu, More}**. Slot 4 is the overlay this distribution has (Binomial/Poisson: Approx; t: N(0,1)), else Refit.
   - So everything the Enter menu offers also works by touch alone.
   - **Deviation from the task text:** the task listed Edit in slot 6; under the convention it moves to page 2, slot 1.
   - DRAWMENU is called with literal lists inside IF branches, the shape ChiTable verified, rather than `DRAWMENU(xxSK(page))` with a list variable. The two are equivalent; the literal form is the one known to have run.
   - The gallery's strip {Open, , , , Help, Back} fits in six, so it gets no "More".
4. **Overlays** (Enter -> "Plot options" CHOOSE, `st_Options` 2791, or page 2):
   - The **normal approximation** N(np, √(np(1−p))) / N(λ, √λ) is drawn in magenta across the Binomial/Poisson bars. The note line gives the continuity-corrected area, either:
     - "normal approx. = 0.5885 (continuity corr.)", or
     - in red, "approx. 0.2512: approximation poor here, λ < 10" (Binomial: np or n(1−p) < 10).
   - **N(0,1) in pale grey behind Student t**, with "grey = N(0,1): t has heavier tails". The y axis makes room for N(0,1)'s taller peak (Lessons Learned s6: check both curves).
   - **The CDF as a magenta S-curve** on a right-hand 0..1 axis labelled "1" and ".5", with F(x) read across to it as a dotted magenta line. For discrete distributions it is a staircase.
   - The options menu also holds: Numbers page, Between, Edit, Refit, Help, and Back to the menu.
5. **The ten stubs implemented** (v2.5 1045-1093; now sections in `st_pdf`/`st_cdf`/`st_icdf`/`st_Mom` plus `st_ask_triangular` 1650 ... `st_ask_hypergeom` 1869). Each gets the same tail-first flow, the numbers page, the plot and a typical-use line.
   - Triangular(a,c,b): closed form.
   - Cauchy(x0,γ): CDF 1/2 + atan(z)/π. `st_atan` (394) = `ATAN(z)·(π/4)/ATAN(1)`, so it is right in radians, degrees **and** grads; `st_tanr` likewise for the quantile.
   - Fréchet(α,s,m): closed form; moments by Lanczos Γ, "undef" for α ≤ 1 and α ≤ 2.
   - Gompertz(η,b): closed form; mean and variance by 400-step Simpson on S(x) (`st_gompMom` 529). There is no elementary closed form.
   - Maxwell(a): the erf form with `2·NORMALD_CDF(0,1,x/a) − 1`; the quantile is `a·√CHISQUARE_ICDF(3,p)` (whole df).
   - Erlang(k,λ): CDF `CHISQUARE_CDF(2k, 2λx)`; pdf `2λ·CHISQUARE(2k, 2λx)`; k is rounded down with a box.
   - Gamma(k,θ), any k > 0: our own regularized lower incomplete gamma, `st_gammaP` 417. It uses the series for x < k+1, else a Lentz continued fraction, with `st_lngamma`. **It never calls CHISQUARE_CDF with a non-integer df**, and the harness confirms no such call happens anywhere.
   - Beta(α,β): our own incomplete beta (`st_betaI` 492, `st_betacf` 458), Lentz with the symmetry swap at x ≥ (a+1)/(a+b+2).
   - Negative binomial(r,p), Y = failures before the r-th success: P(Y ≤ k) = `1 − BINOMIAL_CDF(k+r, p, r−1)`, using the file's existing (n, p, k) order (v2.5 783). pmf = `r/(k+r)·BINOMIAL(k+r, p, r)`.
   - Hypergeometric(N,K,n): `COMB` in a loop (`st_hyp` 510). N is capped at 1000, so C(N,n) ≤ 2.7E299.
6. **Typical use, for CJ/forensic students** (`st_Use` 574; the INPUT titles; the plot title in grey; numbers page line 1). Examples:
   - Poisson: calls per shift. Binomial: convictions in n cases. Exponential: time to the next incident.
   - Student t: small-sample means. Chi-square: goodness of fit. LogNormal: sentence lengths.
   - Weibull: time to re-offence. Rayleigh: shot distance from aim. Laplace: age-estimate errors.
   - Pareto: a few offenders, most crime. Gompertz: years lived past age 20. Beta: clearance rates.
   - Triangular: an expert's min/likeliest/max guess. Hypergeometric: sampling seized packets (default N = 50, K = 40, n = 6: P(all 6 positive) = P(X > 5) = 0.2415).
7. **Gallery**, the new first main-menu item (`st_GalBuild` 2929, `st_GalDraw` 2959, `st_Gallery` 3028).
   - A 2×3 grid of 98×90 cells with 96×64-px thumbnails: Normal(0,1), Exponential(1), Chi-square(4), t(3) over N(0,1), Binomial(10,0.3), Poisson(3).
   - Each thumbnail has a shaded curve or bars, a green dotted mean and a label.
   - The heights are computed once into one flat list `stGH`, so a redraw does no maths.
   - Tap boxes are recorded while drawing (ChiTable idiom).
   - Tapping a thumbnail runs that distribution's tail menu and form with the thumbnail's parameters as the defaults; t(3) opens with N(0,1) already behind it.
   - Keyboard: arrows move a red frame and Enter opens. Soft keys: {Open, , , , Help, Back}.
8. **Numbers page** (`st_Numbers` 2715): the v2.5 result text is now built from the live plot state. It follows a dragged x, a changed tail and edited parameters. Its lines are:
   - the typical use, the parameters, mean and sd, variance;
   - for x: PDF/PMF and CDF; for Between: "CDF(b) = ..., CDF(a) = ..., P = CDF(b) − CDF(a)" (discrete: CDF(a−1));
   - the magenta P line last.
   It is reached by Enter -> Numbers page, or page 2 -> Numbers.
9. **Forms** (`st_ask_*`, one per distribution, section 5; dispatch `st_Ask` 1896; the Between form generic in `st_AskAB` 1250):
   - The v2.5 labels, help strings, reset values, error boxes and the "n rounded down to 20" boxes are kept (`st_Int`).
   - Between bounds are clamped to a discrete support (v2.5's `MAX(0, ...)`) and swapped if typed backwards (new).
   - Every INPUT is now `okI := INPUT(...); IF okI == 0 THEN RETURN 0; END;` (the ChiTable shape; lint_ppl's rule).
   - Edit re-opens the form with the plot's values in it. In a<X<b it then resets a and b to the default rule, and the help says so.
10. **Help** (`st_show_help` 1936): 31 lines on three pages. It covers every gesture, both soft-key pages, the keys, the options and the colours.
    - `st_Page` now waits with `st_WaitAny`, so a key **or a tap** turns a page, and the finger lift that opened a page cannot close it.
    - Footers are in the house form: "any key or tap = next page" / "any key or tap = back".
    - The plot's note line falls back to "Ent = options, +/- = zoom, 0 = refit, Esc = menu" in dodger blue.
11. **Structure and hygiene**:
    - EXPORT StatDist() moved to the end, so every routine is defined before it is used.
    - File-level LOCAL state is set in `st_Init` (ChiTable's model).
    - New code writes `^0.5` and number literals, so the √ and π in code are gone: E5 drops from 24 to 0. E9 drops from 17 to 0 (integers use `STRING(v,2,0)`, ChiTable's verified form), and the 34 W2 unused `params, bounds` go too.
    - The lint_ppl PROBLEM `LOCAL 'mean' shadows a builtin` is gone.
    - The program returns "StatDist: <last P line>" to Home.
12. **Bugs found and fixed while testing**:
    - Student t's mean is now "undef (df<=1)" for df ≤ 1; v2.5 always printed 0.
    - The harness's all-27 sweep found that while the FIRST a<X<b tap was being dragged, a could cross the default b and the panel showed P = −0.19. Now the first tap places a and b together (P = 0), the second stretches the interval, and the bounds are kept ordered on every drag sample.

Not changed, on purpose: the v2.5 labels, error texts and form defaults. "Back" items and Weibull on both menus also stay. The λ glyph in display strings is kept where v2.5 used it, and reused for the new Erlang rate. New strings avoid unverified glyphs: γ, η and θ are written "gamma", "eta" and "theta"; "≤" is written "<=", because CHAR(8804) is still unverified (GfxProbe T14).

## The gate

```
=================== StatDist_v2.6.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
(empty: no errors, no warnings)
--- 2. ppl_check_v2 tally (ORIG = v2.5) ---
     24 E5      17 E9      34 W2
--- 2b. ppl_check_v2 HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
2059 checks, 4 problems -- all four are the known file-name/EXPORT noise
  ("no function named StatDist_v2.6", "EXPORT StatDist is neither the entry point ...")
--- 4. full parse (kit interpreter) ---
StatDist_v2.6.txt   PARSE FAIL <ppl>:155: expected a name after EXPORT   <- file-level LOCAL, the kit's documented limit
   ORIG: StatDist_v2.5.txt  PARSE FAIL line 412: unexpected character '√'
  With file-level LOCAL turned into plain declarations (the harness does this),
  the whole file parses: 102 functions, and runs (below).
--- 5. line count, size, non-ASCII in code ---
3176 lines, 126657 bytes; no non-ASCII in executable code
fleet_names_v2.py over the newest version of every fleet program in out/ + uploads
(27 files, including the versions other sessions wrote today):
  673 routine names, 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches
```

## Verification against SciPy (verify_StatDist.py, pasted)

This is the program's own PPL `st_pdf`, `st_cdf`, `st_icdf` and `st_Mom`, run in the interpreter.

- Each point set is 9 quantiles plus two points outside the support (all k for discrete distributions).
- Parameters include hard corners: Gamma k = 0.15 and 60.5; Beta(0.5,0.5), (0.3,4) and (200,300); t(1); chi-square(1); Hypergeometric N = 1000.

```
id  distribution    sets   pts   pdf(rel)   CDF(abs)   quantile    moments
1   Normal             2    22    0.0e+00    0.0e+00    0.0e+00    0.0e+00
2   Uniform            2    22    0.0e+00    0.0e+00    0.0e+00    2.1e-16
3   Exponential        2    22    1.1e-16    5.5e-17    3.5e-18    0.0e+00
4   Weibull            2    22    1.5e-16    5.6e-17    1.4e-17    6.7e-15
5   LogNormal          2    22    1.1e-16    1.1e-16    1.4e-16    2.4e-16
6   Laplace            2    22    0.0e+00    0.0e+00    0.0e+00    0.0e+00
7   Student t          3    33    0.0e+00    0.0e+00    5.8e-11    0.0e+00
8   Chi-square         3    33    0.0e+00    0.0e+00    0.0e+00    0.0e+00
9   Fisher F           2    22    0.0e+00    0.0e+00    3.1e-11    0.0e+00
10  Burr XII           2    22    2.2e-16    1.7e-16    3.1e-15    1.4e-14
11  Gumbel             2    22    0.0e+00    1.1e-16    0.0e+00    2.2e-15
12  Pareto             2    22    1.7e-16    2.2e-16    0.0e+00    0.0e+00
13  Rayleigh           1    11    1.1e-16    1.1e-16    2.8e-17    1.0e-15
14  Logistic           2    22    2.8e-17    0.0e+00    0.0e+00    8.1e-16
15  Binomial           2    42    0.0e+00    0.0e+00    0.0e+00    1.2e-16
16  Poisson            2    65    0.0e+00    0.0e+00    0.0e+00    0.0e+00
17  Geometric          2   179    1.4e-17    3.3e-16    0.0e+00    1.1e-16
18  Triangular         3    33    2.8e-17    2.2e-16    1.9e-16    1.4e-16
19  Cauchy             2    22    6.7e-16    3.6e-16    3.2e-13    0.0e+00
20  Frechet            3    33    2.8e-17    1.1e-16    2.8e-16    1.2e-13
21  Gompertz           4    44    1.6e-15    6.7e-16    4.0e-16    3.5e-09
22  Maxwell            2    22    3.3e-16    3.9e-16    0.0e+00    1.3e-15
23  Erlang             3    33    1.8e-15    0.0e+00    1.3e-16    1.4e-16
24  Gamma              5    55    3.6e-12    3.6e-11    1.5e-10    1.9e-16
25  Beta               6    66    1.3e-10    6.3e-11    3.0e-11    0.0e+00
26  Neg.binomial       3    86    2.2e-16    5.6e-17    0.0e+00    0.0e+00
27  Hypergeometric     3    53    1.0e-13    6.5e-13    0.0e+00    1.1e-16
st_gammaP vs scipy.special.gammainc, 63 points incl. a = 0.05..150: max abs err 6.6e-11
st_betaI  vs scipy.special.betainc, 252 points incl. a, b = 0.1..400:  max abs err 7.6e-11
Cauchy(3, 0.5) in rad  mode: F(4.2) = 0.8743340836  Q(0.9) = 4.5388417686
Cauchy(3, 0.5) in deg  mode: F(4.2) = 0.8743340836  Q(0.9) = 4.5388417686
Cauchy(3, 0.5) in grad mode: F(4.2) = 0.8743340836  Q(0.9) = 4.5388417686
                    SciPy: F(4.2) = 0.8743340836  Q(0.9) = 4.5388417686
flags raised by the built-ins (non-integer df, POISSON_CDF k<0): none
RESULT: ALL PASS
```

- SciPy's `invweibull` returns a *negative* variance (−44.96) for Fréchet α = 1.5, where the true variance is infinite. StatDist's "undef (α<=2)" is right, and the script treats it so.
- The interpreter's statistics built-ins are SciPy. For the 17 v2.5 distributions this checks the PPL formulas and argument orders, not HP's built-in algorithms.

## Harness runs (run_StatDist_v2.6.py, summary pasted)

**Part A**: every distribution × every tail through the real menus (main -> submenu -> tail -> forms as shown -> plot -> Enter -> Numbers page -> key -> Esc). The numbers-page P **and** the plot-panel P were both compared with SciPy, computed independently in the script. **81 runs, 0 failures**; the largest |P − SciPy| is 4.9e-7, the 6-decimal rounding.

```
  1 Normal       P(X <= 0) = 0.500000 | P(X > 0) = 0.500000 | P(-1 < X < 1) = 0.682689
  8 Chi-square   0.108822 | 0.891178 | P(5 < X < 20) = 0.861925
 15 Binomial     P(X <= 10) = 0.588099 | P(X > 10) = 0.411901 | P(7 <= X <= 12) = 0.810753
 16 Poisson      0.265026 | 0.734974 | P(0 <= X <= 9) = 0.968172
 18 Triangular   P(X <= 5) = 0.300000 | 0.700000 | P(2 < X < 5) = 0.300000
 19 Cauchy       0.750000 | 0.250000 | P(-1 < X < 1) = 0.500000
 20 Frechet      0.367879 | 0.632121 | P(0 < X < 2) = 0.882497
 21 Gompertz     P(X <= 50) = 0.498952 | 0.501048 | P(34.0896 < X < 61.8754) = 0.695023
 22 Maxwell      P(X <= 1.5) = 0.477833 | 0.522167 | P(0 < X < 1.5958) = 0.533050
 23 Erlang       P(X <= 2) = 0.323324 | 0.676676 | P(0 < X < 3) = 0.576810
 24 Gamma        P(X <= 4) = 0.450584 | 0.549416 | P(0 < X < 5) = 0.584120
 25 Beta         P(X <= 0.3) = 0.579825 | 0.420175 | P(0.1260 < X < 0.4454) = 0.662012
 26 Neg.binomial P(X <= 4) = 0.580096 | 0.419904 | P(0 <= X <= 4) = 0.580096
 27 Hypergeom.   P(X <= 5) = 0.758451 | P(X > 5) = 0.241549 | P(0 <= X <= 4) = 0.344367
 (all 27 rows are in run_StatDist_v2.6_output.txt; the v2.5 values for the first 17 are unchanged)
```

**Part B**: 58 interaction checks, **0 failed**. They cover:

- **Drag**: one frame per new column; the mid-drag readout equals Φ(column x); on lift x snaps to 0.1 and P = Φ(x).
- **a<X<b**: the two taps set a and b; the prompts appear; a later drag moves the nearer line only.
- **Discrete**: Poisson P>k reads "P(X > 3) = P(X >= 4) = 0.734974"; a drag across Binomial bars lands on the bar under the finger.
- **Keys**: arrows 1.96 -> 2.0 -> 2.1; Up/Down change the tail; Left past 0 pans the window.
- **Zoom**: Zoom+ halves the window about x; Zoom−, −, 0 refit restores it; the "zoomed" note appears.
- **Edit**: re-opens the form and refits.
- **The More page**: Numbers, CDF, Approx and Menu work with no Esc pressed; page 1 keeps More.
- **Overlays**: the Binomial approximation area is 0.5885; Poisson shows "poor here, λ < 10"; t shows the N(0,1) legend and the y-axis room; the CDF axis labels are drawn.
- **Heavy tails**: Cauchy is cut at ±17 with "1.9% beyond" both sides; Pareto shows "0.6% beyond"; chi-square(1) is clipped and says so.
- **Gallery**: all six taps open the right form with the right values; t opens with N(0,1); keys Right, Down, Enter open Binomial; the soft keys are right.
- **Help**: three pages; every key and soft key named; a tap turns the page.
- **v2.5 checklist values**: 0.968172, 0.588099 with both rounding boxes, 0.847717, 0.875000, Burr 0.7854/0.3831.
- **Error boxes and Cancel at each stage**.
- **A sweep of all 27 distributions** through drag, two-tap Between, Zoom−/+, arrows, the CDF overlay, More -> Edit and the slot-4 overlay: no runtime error, 0 ≤ P ≤ 1, no flagged built-in call.

**Cost** (counted in the harness):

- One continuous frame is 429 LINE_P, 31 PIXON_P, 1 RECT_P and 19 TEXTOUT_P, with no density evaluations. That is the brief's "one shaded 272-column curve from a cache plus ~40 calls".
- A refit costs 278 st_cdf calls for the Normal (all built-ins), but **424 incomplete-gamma evaluations for Gamma** (4 bisected quantiles plus 275 cache columns). That is the one place the G1 may feel slow; see checklist item 14.

## (b) DEVICE TEST CHECKLIST (G2 first, in this order)

1. **Paste and compile.** Paste v2.6 with the Connectivity Kit and run `fleet_names_v2.py *.txt` in D:\HP-Prime first. If the editor stops, note the line. The constructs here that the fleet has not yet run are:
   - file-level `LOCAL` lines *before* any EXPORT (ChiTable has them after its EXPORT variables);
   - `RETURN` inside `CASE` clauses;
   - list literals indexed through a LOCAL (`nmL := {...}; RETURN nmL(dId)`);
   - `1E300` / `1E-300` literals;
   - `TYPE(dbMo(2))`;
   - a CASE `DEFAULT` inside an IF inside an IF (st_Plot).
2. Main menu: **Gallery** is item 1.
   - Six thumbnails, with t(3) showing a pale grey N(0,1) behind it. Check the labels are not clipped ("Binomial(10,0.3)" is the widest).
   - Tap Chi-square(4): the tail menu appears, then the form shows df = 4, x = 5.
   - Accept. The plot opens with the window starting at 0. P(X ≤ 5) is 0.712703 (not checked in the harness; SciPy value).
3. **Normal, Lower tail, defaults.** Check that:
   - the blue bell sits over a grey grid with ticks −3..3;
   - the red x line is at 0, with the left half shaded pale blue and a green dotted line at 0;
   - the panel reads "μ = 0, σ = 1", "mean = 0, sd = 1", "f(x) = 0.3989: a density, not a probability", and in magenta "P(X <= 0) = 0.500000";
   - the soft keys read P<=x, P>x, a<X<b, Zoom−, Zoom+, More. **Does "Zoom−" with U+2212 render?** If not, use "Zoom-".
4. **Drag** a finger slowly across the plot. The shading and the magenta P must follow without lag on the G2. Lift: x snaps to a multiple of 0.1. Repeat the drag on the G1 and note whether it keeps up.
5. **Arrows.** Right/Left step 0.1. Up turns the shading to the right tail ("P(X > ...)"); Down turns it back.
6. **Between.**
   - Tap a<X<b: the note turns red, "tap the plot to set a". Tap left of centre: a appears, P = 0, and the note says "... set b". Tap right: P(a < X < b).
   - Then drag near b: only b moves. Use Up/Down plus the arrows to move b or a from the keys.
7. **Zoom.** Zoom+ halves the window about x and the note says "zoomed, 0 = refit the window". Zoom− and the −/+ keys work the same way. 0 refits.
8. **More.**
   - Tap slot 6: the strip changes to Edit, Numbers, CDF, Refit, Menu, More.
   - Numbers shows the page; a tap or key returns to the plot.
   - CDF draws the magenta S-curve, the right-hand "1"/".5" labels and the dotted line across from x.
   - More again returns to page 1.
   - Edit: the form shows the plot's μ, σ, x. Type 100, 15, 130 -> P(X <= 130) = 0.977250.
   - Menu leaves the plot.
9. **Enter on the plot**: the "Plot options" CHOOSE has 7 items (8 for t, Binomial and Poisson). Check that its Enter press does not leak back to the plot: the plot must not reopen the menu by itself.
10. **Binomial (20, 0.5)**:
    - bars 0..20; bars ≤ 10 filled, bar 10 solid red.
    - P>k: bar 10 turns to a red OUTLINE, and the panel reads "P(X > 10) = P(X >= 11) = 0.411901".
    - More -> Approx: a magenta normal curve over the bars and "normal approx. = 0.5885 (continuity corr.)".
    - Edit n = 10, p = 0.3: the note turns red, "approximation poor here, np or n(1-p) < 10".
11. **Poisson (5)**, Between with the default bounds 0 and 9: "P(0 <= X <= 9) = 0.968172" (the v2.5 POISSON_CDF(λ,−1) case; v2.6 never calls it).
12. **Heavy tails.**
    - Cauchy defaults: grey "<< 1.9% beyond" at the top left and "1.9% beyond >>" at the top right. The panel says "mean = undef (no mean)" and there is no green line.
    - Pareto(1,3): "0.6% beyond >>".
13. **Angle mode.** Set Home to **Degrees**. Cauchy, x = 1: P(X <= 1) = 0.750000, the same as in Radians. (This tests `st_atan`'s ATAN(1) trick on the device.)
14. **Speed of the new maths on the G1**:
    - Gamma (2.5, 2) Lower tail x = 4 should show 0.450584. **Time the wait from accepting the form to the plot**, and the wait after a Zoom+. A refit is 424 incomplete-gamma evaluations.
    - Beta (2, 5) x = 0.3: 0.579825.
    - If either takes more than ~3 s, say so: the next version can build the CDF cache by quadrature of the pdf cache instead.
15. **The other new ones, defaults, Lower tail**:
    - Triangular 0.300000; Frechet 0.367879; Gompertz 0.498952 (mean ≈ 47.98); Maxwell 0.477833;
    - Erlang 0.323324; Negative binomial 0.580096;
    - Hypergeometric: P>k for k = 5 should give 0.241549 (all 6 sampled packets positive).
16. **v2.5 items, unchanged**:
    - Binomial n = 20.7, k = 10.4: two boxes, then 0.588099.
    - Bounds 6.5/12.9: two boxes, then P(6 <= X <= 12) = 0.847717.
    - Pareto x_m = 5, α = 3, Between: 0.875000.
    - Burr: mean 0.7854, variance 0.3831 on the numbers page.
17. **Help**: 3 pages. A key and a tap each turn a page; the last page returns.
18. **Exit** from the main menu: Home shows "StatDist: P(...) = ..." (the last probability shown).
19. Repeat 3, 4, 10 and 14 on the **G1**.

## (c) Not confirmed, left as it is

- **Nothing here has run on a calculator.** The interpreter runs IEEE doubles, not the Prime's 12-digit decimals: the 6th decimal of a probability can differ in a tie, and the loop tolerances (1E-11) are chosen to be reachable in 12 digits.
- The kit cannot parse file-level LOCAL, so the gate's parse step fails on line 155 (its documented limit). The harness's preprocessed copy parses and runs. ChiTable's file-level LOCALs have run on the device, but there they sit *after* EXPORT variable lines; StatDist has none.
- The **G1 cost of the Gamma/Beta refit** is untested (checklist 14).
- `STUDENT_CDF` / `CHISQUARE_CDF` with a non-integer df: v2.5 allowed a real df for t and chi-square, and v2.6 keeps that (unverified, GfxProbe T11). The chi-square *quantile* falls back to bisection for a non-integer df, so CHISQUARE_ICDF is only ever asked with a whole df.
- Glyphs: v2.6 uses only glyphs v2.5 already displayed (μ σ λ α β) plus "−" in "Zoom−" (on the verified list). "≤" is spelled "<=" until GfxProbe T14 passes.
- The **"More" convention** is applied with literal DRAWMENU lists in IF branches, the ChiTable-verified call. The brief's `DRAWMENU(xxSK(page))` with a list variable is equivalent, but no fleet program has used that form on the device.
- Tick and title text widths are estimated (font 1 ≈ 6.5 px, font 2 ≈ 8 px per character); a 12-digit typed parameter can clip a panel line at 308 px.
- Plot and page geometry come from this design, not a device photograph. Expect one pixel-nudge round, especially the panel's font-2 P line at y = 191 against the note at y = 205.
