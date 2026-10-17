# Round-1 tests on the HP Prime Virtual Calculator (17 October 2026)

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). Run by Claude through computer use on Rogers-HP, 16–17 October 2026.*

**The emulator:** HP Prime Virtual Calculator 2.4.2, software build 2026-09-09, revision 15751, CAS 1.5.0, MicroPython 1.9.4. This is the same build as the fleet's target firmware (2026-09-09).

**What an emulator run can and can't settle.** Commands, error behaviour, drawing, glyphs and maths behave as on the calculator, because the emulator runs the same firmware. Timing (G1 speed), a held key, and anything needing two fingers can't be tested with a mouse; those stay on Roger's list for the real G1 and G2.

**How the logs were captured:** after each run, `GP_LOG` (or the program's log) was evaluated in Home, selected, and copied out with the emulator's Edit ▸ Copy. The text below is the calculator's own output.

---

## GfxProbe beta 1 — run 1

| Test | Result | Notes |
|---|---|---|
| T01 FILLPOLY_P opaque, `{{x,y},…}` | **yes** | |
| T02 FILLPOLY_P alpha 110 | **yes** | Bars clearly visible through the shape |
| T03 FILLPOLY_P flat list | **yes** | |
| T04 TRIANGLE_P one colour | **yes** | |
| T05 TRIANGLE_P three-colour blend | **yes** | Smooth RGB gradient |
| T06 TRIANGLE_P blend + alpha 128 | **yes** | |
| T07 TRIANGLE_P 3-D mesh form | **no** | Ran without error but drew nothing. The control list or the matrices are probably wrong; no fleet program depends on it |
| T08 BLIT_P 10-argument scaled copy | **yes** | Exactly 2× |
| T09 ARC_P r = 3, 2, 1 + pixel as a solid dot | **no** | Each dot shows a white **X**: concentric circles leave holes on the diagonals. **GaltonBoard draws its balls this way** (fix below) |
| T10 MAX / SORT on a list | yes | |
| T11 non-integer df | **ERROR** | See the Home checks below |
| T12 POISSON_CDF(2, −1) | **ERROR** | "Invalid input". StatDist v2.5+ already avoids it |
| T13 MSGBOX lines | **5 lines** shown (line 1–line 5). No scroll bar; the PC Down key closed the box, so whether it scrolls on the calculator is still open |
| T14 nine glyph lines | **yes** | x₃, arrows, ⇆ ⇅, ①②, √ ∞, χ², x̄ p̂, ≥ ≤ ≠, θ ρ λ all render |
| T15 held key across WAIT(0.02) | not settled | GETKEY 0, ISKEYDOWN 0, but the PC key was held after the counting loop had begun. **Hardware test** |
| T16 second finger in MOUSE | not testable | MOUSE returns **2 lists**. A mouse can't make two touches. **Hardware test** |
| T17 WAIT(−1) event types | **0, 1, 2, 3, 7 seen** | 0 down, 1 move, 2 up, 3 click, 7 long click (pinch/rotate need two fingers). Matches the manual's table. **New:** the values come back as *integers* (`#3C:-16h`), so STRING() prints them in hex; arithmetic is unaffected. Type 2 (up) is a list of size 1, with no x, y |
| T18 TICKS across WAIT(0.1) | 107 ms | |
| T19 MAKELIST with a LOCAL counter | **yes** | Constant form yes; Home K untouched |
| T20a BINOMIAL(10, 0.3, 2) | **0.233474** | = SciPy. The order is **(n, p, k)** |
| T20b BINOMIAL(10, 2, 0.3) | ERROR | Only (n, p, k) works. The fleet uses (n, p, k) everywhere (checked) |
| T20c BINOMIAL(8, 0, 0.5) | ERROR | Consistent with (n, p, k) only |

### Home checks after T11 (typed by hand, compared with SciPy)

| Expression | Emulator | SciPy |
|---|---|---|
| CHISQUARE_CDF(3, 3) | 0.608374823729 | 0.6083748 |
| CHISQUARE_CDF(2.5, 3) | **Invalid input** | 0.69415 |
| CHISQUARE_ICDF(2.5, 0.5) | **Invalid input** | |
| CHISQUARE(2.5, 1) (density) | 0.281348225763 | 0.2813482258 ✓ |
| FISHER_CDF(2.5, 7.5, 2) | **Invalid input** | 0.80043 |
| FISHER_ICDF(2.5, 7.5, 0.5) | **Invalid input** | |
| STUDENT_CDF(2.5, 1) | 0.797969486361 | 0.7979694864 ✓ |
| STUDENT_ICDF(2.5, 0.9) | 1.7302509288 | 1.7302509288 ✓ |
| STUDENT(2.5, 1) (density) | 0.200795960671 | 0.2007959607 ✓ |
| POISSON_CDF(2, −1), POISSON_CDF(2, −0.5) | **Invalid input** | 0 |

**The rule this gives (for Lessons Learned v7h):** the chi-square and F **CDF and ICDF** take **whole-number df only**; their densities take any df. Student t takes any df in all three (Welch's df is safe).

### What these findings mean for the fleet

1. **StatDist v2.6 (and v2.7): bug.** The chi-square and F prompts accept any df > 0, but the CDF calls CHISQUARE_CDF / FISHER_CDF directly, so df = 2.5 stops with "Invalid input". The chi-square ICDF already checks `FP(df) == 0`, but its bisection fallback calls the same CDF. **Fix:** for a fractional df, chi-square goes through StatDist's own `st_gammaP(df/2, x/2)`; F either gets an incomplete-beta routine or the prompt asks for whole numbers.
2. **GaltonBoard beta 2 (and beta 3): visual bug.** The balls have diagonal holes. **Fix:** draw each ball as a small filled octagon (FILLPOLY_P, confirmed by T01/T03) or three overlapping RECT_P bars.
3. **ErrorRate beta 1: safe.** Its Beta CDF uses FISHER_CDF with doubled parameters. The uniform and Jeffreys priors double to 2 and 1, and a custom prior is held to multiples of 0.5, so the df are always whole.
4. **WAIT(−1) integers:** any program that prints a touch coordinate with STRING() will show hex. None of the fleet does today; worth a line in Lessons Learned.

---

## LocalHeadProbe beta 1

**PASS.** `LocalHeadProbe()` returned "LocalHeadProbe: LOCAL routine head works, 2 + 3 = 5". The form `LOCAL name(args)` for a routine head pastes and runs, so PowerViz's `LOCAL pv_Name()` helpers are fine.

---

## CASProbe beta 1a, then beta 1b

### Beta 1a: "CAS available: no" (the probe's yardstick was wrong, not the CAS)

| Test | Result |
|---|---|
| T01 STRING(real) | FAIL: `STRING(-2.5)` gives **U+2212 (−)**, not a hyphen. Positive integers are plain |
| T02 cxIStr | PASS |
| T03 | HSeparator 0 (decimal dot), HFormat 0 (Standard) |
| T04 `CAS(comb(100,50))` written in the program | Evaluated, but crossed into Home as the real 1.00891344546E29 |
| T06 / T07 `CAS(s)`, s a string variable (**the fleet's xxCas as written**) | **The text came back unevaluated** |
| T08 / T09 `EXPR("CAS(" + q + s + q + ")")`, `CAS.eval` | Evaluated, but crossed back as the 12-digit real |
| T42 BINOMIAL_CDF(30, 0.2, 2) | 0.044179, the (n, p, k) order |
| T33 Python ints | exact |
| T34 Python `cas.caseval` | No crash; returns a str; comb(100,50) comes back as a decimal |

By hand in Home: `STRING(EXPR("CAS(\"comb(8,4)/2^8\")"))` = `35/128`; `EXPR("CAS(\"string(comb(100,50))\")")` = all 30 digits; `factor(6*cft^2+7*cft+2)` = `(2*cft+1)*(3*cft+2)`.

**So CASProbe beta 1b** asks the CAS for `string(...)` of each answer, through EXPR. It is in D:\HP-Prime and FIXED_FOR_DEVICE (1a archived to `_superseded_2026-10-17`).

### Beta 1b: CAS available, yes. 42 pass, 8 fail, 19 values, 0 errors

**The call form that works** (T08):

```
cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + xxS + ")" + CHAR(34) + ")"));
```

then drop the surrounding quotes. The answer is a PPL string (TYPE 2): `STRING()` of it adds the quotes, `"" + it` does not (T12).

**How the Prime prints CAS answers. This differs from desktop Giac, which the harness uses:**

| What | Prime (emulator) | Desktop Giac 1.9 |
|---|---|---|
| exp | `e^(cxt^2/2)`, `1/2*cxl^2*e^(-cxl)` | `exp(cxt^2/2)` |
| sqrt | `√2`, `erf(49*√2/50)/2+1/2` (U+221A) | `sqrt(2)` |
| solve, one unknown | `{1/20}`, `{-2,2}` (braces) | `list[1/20]` |
| solve, a system | `{[2,1]}`, `{[23/10,4/5]}` | `list[[2,1]]` |
| fsolve | `[0.0950338528553]` | |
| seq, matrices | `[1,4,9,16]`, `[[2,4],[6,8]]` | same |
| limit to infinity | `∞` (U+221E) | `+infinity` |
| 1/0 | `±∞` | `infinity` |
| 0/0 | `undef` | `undef` |
| an unknown function | handed back unevaluated: `cxnosuch(3)` | |
| a syntax error | a run-time error, caught by IFERR | |
| series | `…+cxt^4*order_size(cxt)`; `convert(…,polynom)` drops it | same |
| evalf(17/35) | `0.485714285714` (12 significant digits) | |
| products | `*` | `*` |

**Other findings:**
- **CAS variables persist** (T25): `cxq:=7` survives into the next call, and so into the student's CAS view, until `purge(cxq)`. Fleet programs must not assign CAS variables, or must purge them.
- **Long text** is fine: 6,005 characters in one call (T35).
- **Big numbers** are fine as strings: comb(1000,500), all 300 digits (T22).
- **Speed** on the PC: the slowest call took 8 ms. This says nothing about the G1.
- **The U+2212 minus is read by the CAS:** `STRING(-2.5)+1/2` gave −2.0 (T31b). Even so, CAS text still comes only from xxIStr.
- **Python `cas.caseval`:** no crash, but it returns decimals for big integers ("wrong text"). The fence keeps it out of the fleet.

### What this means

1. **Every CAS program's `xxCas` must change** to the form above. That is all eleven round-2 programs **and ErrorRate beta 1 (round 1, current)**. As written, xxCas hands back its own input text.
2. **Every parser of a CAS answer must accept the Prime's printing:** braces from solve, `e^(` for exp, `√` for sqrt, and `∞`. A check that looks for `exp(` or `list[` will never match on the calculator.
3. **xxCas should also reject `∞`** (CHAR(8734)), as it already rejects `undef` and `rror`.
4. **The harness must model the calculator:** CAS(variable) unevaluated; Prime-style printing; big integers becoming reals unless they are strings. Until it does, a harness pass on CAS code proves less than it seems.

---

## ChiTable beta 2: PASS (two cosmetic items)

Run through the CHANGES checklist (§5).

| Item | Result |
|---|---|
| 1 Paste, menu | PASS: 14 items, A–E lettered, Quit last; Quit returns "ChiTable: χ²(1, N = 674) = 13.1570, p = 0.0003, …" |
| 2 Entry grid | PASS: tap a cell → INPUT → the count and totals update |
| 3 Results pages (death penalty × victim's race) | PASS: "1/6"…"6/6"; soft keys Prev · Next · Bars · Mosaic · Curve · Menu; page 3's last line sits above the strip. **Every number matches SciPy:** χ² 13.157, p 0.0003, E 51.96 / 463.04 / 16.04 / 142.96, Yates 12.087 (p 0.0005), Fisher p 0.0001, G² 16.872, V 0.140, C 0.138, OR 5.499 |
| 4 Tap a cell | PASS: magenta frame, "R1 C1: E = 515 × 68 / 674 = 51.96" |
| 5 Help | PASS: four pages; page 3 (14 lines) not clipped; page 4 the df page |
| 6 Simpson | PASS |
| 7 Plots | PASS: bars, mosaic (colours right), curve ("← drag →"), residuals (dotted ±2), Fisher (class strip, orange panel) |
| 8 Soft keys on plots | PASS: Next walks the plots; "Restore" fits its key |
| 9 ×10 N, N / 10 | PASS: 6740 / 131.57 / p < 0.0001 / V 0.140; N / 10 back to 674; a second N / 10 refused with the message |
| 11 Tap a Fisher bar | PASS: a = 52, P = 0.1196 |
| 12 Morph | PASS: ends on the grey "all" shape with the E values |
| 14 Drag a bar | PASS: the count follows the finger (64 → 268), the pale bars move, χ² updates live; Restore puts it back |
| 15 Drag the critical line | PASS: α follows, the verdict changes, "custom α = 0.0002" on lift |
| 10, 13 Arrow keys | not tested: one click on the emulator's arrow pad moves the selection two steps, so arrow counts can't be trusted here |

**Cosmetic (fix in the next version):** two CHOOSE items are clipped at the right edge of the box: "Death penalty × defendant's rac[e]" in the Examples list and "N / 10: every count divided by [10]" in the Results menu. Shorten them to about 30 characters.

---

## BayesTree beta 7: works, except **the soft keys** (a real bug), plus one rounding slip

| Item | Result |
|---|---|
| 1 Paste | PASS |
| 2 First frame | PASS: slider "prior 0.100", mosaic, leaves 90 / 10 / 45 / 855 with bars, PPV 0.667, NPV 0.988, LR+ 18.000, LR− 0.105, soft keys "Values Counts ROC PPV 2×2 More". *Cosmetic:* the first-level numbers (0.100 / 0.900) sit on top of the branch lines |
| 6 Slider drag | PASS: the knob follows; at prior 0.001: D+ 1, PPV 0.018 |
| 8 Branch number: tap and drag | PASS: a tap opens "Branch: P(T+ \| D+) = sens" after the lift; a drag down moves sens to 0.835 and everything follows (PPV 0.650, LR+ 16.7, LR− 0.174, all correct) |
| 9 ROC view | PASS: d′ = 2.619, AUC = 0.968 (both correct); a tap on the curve moves the point (sens 0.960, spec 0.808, PPV 0.357, correct) |
| 9 Fagan | PASS: grey line for test 1, dotted carry line, magenta and blue for test 2; readouts correct |
| 11 Second test (0.9 / 0.95) | PASS: breadcrumb 0.10 → 0.36 → 0.91; root T+ 269; leaves 86 / 10 / 9 / 164 (all correct for the first test's sens 0.960 / spec 0.808) |
| A Icon array | PASS: TP 321, FP 32, FN 36, TN 611, white gaps |
| 13 Exit | PASS: "BayesTree: PPV = 0.909, NPV = 0.945 (prior …" |
| **12 Soft keys under WAIT(−1)** | **FAIL: tapping Values or ROC does nothing** (the Enter menu still works) |

**Why the soft keys fail (MenuTapProbe beta 1, a 40-line probe written for this).** It records every WAIT(−1) result with DRAWMENU on screen:

| What was touched | What WAIT(−1) returned |
|---|---|
| A tap on soft key 2 | only `{3, 78, 230}`: **type 3 (click), no type 0, no lift** |
| A tap on the screen above the keys | `{0, 161, 115}`, then `{2}`, then `{3, 161, 115}` |

BayesTree acts on type 0 with y ≥ 218, which never arrives on the menu strip. **Fix (BayesTree beta 7a / 8b):** read a soft key from a **type 3 event with y ≥ 218**, and keep ignoring type 3 above the strip (a screen tap sends 0, 2 and 3, so acting on both would double-fire). StudRange beta 15 also waits with WAIT(−1) and needs the same check (tested below). Every other program polls GETKEY + MOUSE, which sees soft-key presses (ChiTable's work).

**Rounding slip:** after the sens drag to 0.835, the D+ 100 branch shows T+ 84 and T− 17, which adds to 101. **Fix:** draw T− as D+ minus the rounded T+ (and likewise for D−), so every pair adds up.

---

## GaltonBoard beta 2: works; **the pegs and balls show the ARC_P holes**

| Item | Result |
|---|---|
| Paste, welcome page, board | PASS: R = 8, p = 0.50, Rp, √(Rp(1−p)), magenta binomial squares in the 1-8-28-56-70 shape, soft keys Drop ×10 ×100 Pour Rows Menu |
| ×10, ×100 | PASS: the paths and bars; n = 110, x̄ 4.15, s 1.35 |
| Drop | PASS: footer "R L L L L R R R → 4 rights → bin 4" in red. On the PC the ball lands within half a second, too fast to see the disc |
| Tap a bar | PASS: Bin 4: observed 37 of 111, binomial P(4) = 0.2734, normal area 3.5–4.5 = 0.2763, "C(8,4) = 70 paths"; a second tap draws all 70 paths |
| **MicroPython: drop 100,000** | **PASS:** "engine: MicroPython, 100000 balls in 7 ms"; x̄ 4.00, s 1.41 |
| Overlays → binomial+normal | PASS: "normal approximation poor (Rp = 4.00 < 5)" |
| Drag sideways for p | PASS: p 0.50 → 0.72, counts cleared, the flag switches to "R(1−p) = 2.24 < 5" |
| Exit | PASS: "Galton Board: 0 balls, R = 8, p = 0.72; bins in GB…" |

**Visual bug:** every peg shows the diagonal-hole pattern GfxProbe T09 found (each looks like ⊕), and so would the falling balls. **Fix (GaltonBoard beta 2a / 3b):** draw pegs and balls as solid shapes, e.g. a filled octagon with FILLPOLY_P (confirmed by GfxProbe T01 and T03), or a plus of two RECT_Ps plus a corner square.

*Cosmetic:* the bin-count labels sit on the magenta binomial line, so "9" was half hidden.

---

## NormExplorer (NormExp) beta 42: PASS

| Item | Result |
|---|---|
| 1 Paste | PASS: the new file-level LOCAL lines paste |
| 3 P(X < 1) on N(0,1) | PASS: orange left tail, boxed 0.8413 |
| 6 Tap the plot | PASS: the Explorer opens with the tail still shaded and soft keys Bands · Ref · Centre · Shade · Hist · More |
| 7 Soft keys | PASS: Shade cycles left → right (0.0046) → between (0.9908); More shows page 2 (Bnd A · Bnd B · mu · sigma · Menu · More) |
| 8 Height vs area | PASS: "area to the left = 0.8413", "height 0.242 (density, not a probability)" |
| 9 Drag x₀ | PASS: the box rides along (x₀ 2.60 → 0.9954) |
| 11 Grab μ | PASS: "Dragging μ: lift to snap", the bell slides with a ghost of N(0,1), μ snaps to 1.00 |
| 4 Two-tailed critical values, α 0.05 on N(1,1) | PASS: z* = ±1.9600, x* = −0.96 and 2.96, both tails 0.0250 on the curve |
| Exit | PASS: "NormExp: z = 1.9600, x = 2.9600, p = 0.0500" |

Not tried here: Help, data and bars (D1), the power picture, the animation, timing (G1).

---

## StudRange beta 15: works; **plot soft keys fail** (same cause as BayesTree)

| Item | Result |
|---|---|
| 1 Paste (2,228 lines, with the Python block) | PASS |
| 2 Diagnostics | PASS: "Python bridge OK (6 ms)", F(3.5; k = 3, ν = 12) = 0.930005 = SciPy, "Last Python mark: finished mode 0" |
| 5 Tukey HSD (α .05, k 4, m 8, MSE 1) | PASS: q crit 3.8612, HSD 1.3652, green "engine: MicroPython 1.9.4" badge |
| 6 Plot (k 3, df 12, q obs 3.5) | PASS: q crit 3.773, p 0.0700, pdf + cdf, the shaded tail |
| 7 Drag across the plot | PASS: q obs follows (5.677, p 0.0045) |
| **8 Soft keys on the plot** | **FAIL: α+ does nothing**, as the checklist warned. Same cause and fix as BayesTree: read soft keys from a WAIT(−1) **type 3** event with y ≥ 218 |
| 13 Quit | Works: "StudRange: q crit = 3.8612, p = 0.00000, HSD = …". *Small:* p reads 0.00000 when no P-value was asked for, and q crit is the HSD run's (k = 4), not the plot's. Say "p not computed" instead |

---

## StatDist v2.6: works; **the fractional-df bug is confirmed**

| Check | Result |
|---|---|
| Paste (3,177 lines), main menu | PASS |
| Gallery | PASS: six tiles (Normal, Exponential, Chi-square(4), t(3) with N(0,1), Binomial(10, 0.3), Poisson(3)). A **very quick** mouse click on a tile is missed, a normal press opens it. The gallery polls MOUSE, so a finger tap should be fine; recheck on the calculator |
| Chi-square(4), P(X ≤ 5) | PASS: 0.712703, f(5) = 0.1026 (both = SciPy); the shaded plot |
| Soft keys | PASS: P>x gives 0.287297 |
| **Advanced Continuous → ChiSquare, df = 2.5** | **FAIL: the program stops with "Error: Invalid input"** (the CHISQUARE_CDF limit from GfxProbe T11). The F distribution with a fractional df will do the same. Fix as listed above |
| Exit | PASS: "StatDist: P(X > 5) = 0.287297" |

*Cosmetic:* the INPUT label "Degrees of freedom:" is cut to "Degrees of fr…". Shorten it to "df:" (the help line already says "df > 0").

---

## Norm3 v2.4: PASS

`Norm3(0,1,1)`: the plot with both tails, the CDF overlay and "pdf = 0.2420 (a height)"; P(X ≤ 1) = 0.8413. μ+ gives N(0.25, 1) with 0.7734; dragging x₀ to 2.80 gives 0.9946 (all correct). Quit returns "Norm3: N(0.250, 1.000), P(X ≤ 2.80) = 0.9946; …".

**Not a program bug:** typing a call with **empty parentheses** in Home (`Norm3()`, `SampDist()`) gives "Syntax Error". The program is fine: the editor's Check says "No errors in the program", and the program runs from the Program Catalog or as `SampDist` without the parentheses. Norm3 and Burr3 take arguments, `Norm3(μ, σ, x₀)`, and the Catalog asks for them.

**About emulator keystrokes:** letters typed from the PC keyboard leave the emulator in ALPHA lock, so digits typed afterwards come out as letters (2 → Z, 3 → #). Pasting from the clipboard avoids this. This affects only the test method, not the programs.

---

## Burr3 v2.4: PASS

`Burr3(2,3,1,1)`: the density with the mode 0.38, median 0.51 and mean 0.59 markers, the CDF overlay, pdf 0.3750, P(X ≤ 1) = 0.8750, μ 0.589, σ 0.391. All match the closed forms. The soft keys select a parameter (the orange box moves to K), and Quit returns the summary.

---

## SampDist v2.3: PASS (smoke test)

Run from the Program Catalog: the menu (Find probability, Find critical value, Compare sample sizes, Watch sample means, Help). Watch sample means at N(100, 15), n = 30: 40 means as a histogram under the population curve; mean of the 40 x̄ 98.986, SD 2.536 against σx̄ = 2.7386. Exit returns the EP_SD_* list. The editor's Check reports no errors.

---

## PowerViz v2.4: PASS (smoke test)

`POWERVIZ` → One-Sample Mean (z), μ₀ 100, μ₁ 105, σ 15, n 30, α .05: power **0.572**, zcrit 1.645, d 0.33, n₈₀ = 56 (all correct). Dragging H₁ to 110 gives 0.978 ("H₀ stays put; H₁ follows your finger"). α+ gives α 0.100, zcrit 1.282, power 0.991. Esc shows the summary box. The `LOCAL pv_Name()` routine heads compile (LocalHeadProbe agrees).

*Note:* a very quick mouse click on α+ was missed; a press of about 0.3 s worked (the StatDist gallery did the same). A finger tap is longer than a mouse click, but check on the calculator that a light tap on a soft key registers.

---

## EpiStats v1.6: PASS (smoke test, the 2×2 path)

The 2×2 grid; Values (a 30, b 70, c 10, d 90), then Run, gives six pages, **all matching SciPy**:
- Expected counts 20 / 80;
- Pearson χ² 12.5000 (p 0.00041) and Yates 11.2813 (p 0.00078);
- Fisher two-sided p 0.000650, with the point probability of this table 0.000248;
- the Fisher every-table plot;
- OR 3.857 (1.77–8.42), RR 3.000 (1.55–5.80), RD 20.0 % (9.3–30.7 %), φ 0.2500;
- the mosaic.

Exit returns "EpiStats – Results stored in EP_* variables". Not tried: the other menu items (Risk, Sens/Spec, Incidence, M-H, Sample size).

---

## ErrorRate beta 1: the PPL works; **the CAS page shows its own question as the answer**

- **Welcome page and main plot: PASS.** 0 errors in 30 tests gives a one-sided 95 % upper bound of **9.50 %**, correct (1 − 0.05^(1/30)). The rule of 3 gives 10.0 %, and n × bound = 2.85 → 3.00.
- **"Why 3" page: BUG.** The page is badged "exact (CAS)". The "CAS finds the limit" line prints the **input text**, `limit(p ×(1 −(50/1000)^(1/p)), p, inf)`, and then the program's own decimal "= 2.9957". This is CASProbe's T07 failure in a real program: xxCas returns its input, the text has no "undef" or "rror" to reject, and the badge says exact. **ErrorRate beta 1a** (being built with the new call form) fixes this.
- Exit: PASS ("ErrorRate: 0 errors in 30 tests -> 95 % upper bo…").

---

## TrendTest beta 2: PASS (smoke test)

Examples → Snoring and heart disease:
- trend χ² **72.659** (Mantel's (N−1)/N form; the Cochran–Armitage value is 72.688), Pearson **72.782**, departure 0.123 (p 0.94) — all match Python;
- the WLS line and the per-level 95 % CIs;
- the OR soft key draws the log-scale odds-ratio plot with Woolf CIs.

Exit returns "TrendTest: X2 trend = 72.6588 (1 df), p < 0.0001".

*Cosmetic:* the Examples list cuts "(made up)" to "(made up".

---

## CentralLimit beta 2: not run (it is an app)

A Statistics 1Var copy named CentralLimit was saved on the emulator, and the file was pasted into the app's Program tab in the Connectivity Kit. Starting the app gave the plain Numeric view and the stock View menu, so the program never reached the emulator: saving from the Kit's app editor did not send it. Installing it through the calculator's own editor (step 2 of the header) is the next try. **Not tested.**

---

## TestChooser beta 2: PASS (smoke test)

Guide me: the Q1 flowchart (Interval / Ordinal / Nominal / Survival boxes). Tapping Nominal leads to Q2 with six boxes. The Quit soft key works ("TestChooser: no test looked at").

---

## DNAMixLR beta 2: PASS (smoke test)

"Load the worked example" (victim + suspect vs victim + 1 unknown, 3 loci, θ 0.010) gives the LR-by-locus table: 56.793, 19.083 and 3.674; combined LR 3981.5 (log10 3.600, "strong support for Hp"). The page also says "The LR is NOT the probability that the suspect contributed". The Ladder soft key draws the ENFSI verbal-scale ladder with the running log10. Exit returns "DNAMixLR: combined LR = 3981.5, log10 = 3.60…".

*Cosmetic:* the menu item "Results table (tap a row to drop)" is cut to "…to dro".

---

## ScatterLab beta 1: PASS (smoke test)

Tapping the empty grid adds points. With 3 points: r 0.997, r² 0.994, ŷ = −0.02974 + 0.7111x, SSE 0.06876, x̄ 4.167, ȳ 2.933; the line and a mean cross are drawn, and the last point is reported ("Pt 3 (7.5, 5.2): resid −0.1038, h = 0.84"). Resid toggles "resid: on". Exit returns the fit.

---

## BiNorm3D beta 1: PASS (smoke test)

The 3-D wireframe bell for ρ = 0.60, peak 0.199 (= 1/(2π√(1−ρ²))). Dragging turns it (θ 35° → 63°). Cont shows the view from above: ellipses holding **39 %** and **86 %** (1 − e^(−1/2) and 1 − e^(−2)), the magenta regression line E[Y | x] = ρx and the dotted y = x. Exit returns "BiNorm3D: ρ = 0.60, E[Y | X = x] = 0.60 x; …". (The wireframe uses LINE_P, so GfxProbe T07's failed 3-D TRIANGLE_P mesh does not affect it.)

---

## CICatcher beta 1: PASS (smoke test)

Welcome page, then Enter (a very quick mouse click on that page was missed, like the gallery case). Mean with σ known, μ 100, σ 15, n 10, 95 %. +50 gives 50 intervals with 48 caught (96.0 %) and the misses in red. Dragging the right edge to 84.1 % shrinks every interval live: 43 of 50 caught. Exit returns "CICatcher: 43 of 50 caught the truth (86.0 %) at …".

---


## Not run on the emulator

- **CentralLimit** (an app; see above).
- **TouchKit template** (a template, not a teaching program; it is being checked in code for the soft-key fix).
- **G1 timing, held keys, two fingers:** hardware only.

---

## ErrorRate beta 1a (the new CAS call form): PASS on the emulator

The new xxCas (BRIEF_CAS_v2: `STRING(EXPR("CAS(" + q + "string(" + s + ")" + q + ")"))`, quotes dropped, ∞ refused) on the same "Why 3" page now reads:

> (1−p)^30 = 1/20 … n(1−(1/20)^(1/n)) → **ln(20)** = 2.9957, badge "exact (CAS)".

The CAS answer is real and matches the program's own decimal. This is the first fleet program to show a CAS answer on the Prime's firmware. ErrorRate beta 1a is delivered to D:\HP-Prime and FIXED_FOR_DEVICE (beta 1 archived).
