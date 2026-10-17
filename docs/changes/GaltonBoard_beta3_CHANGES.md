# GaltonBoard beta 3: changes from beta 2

16 October 2026. This version is built on `GaltonBoard_beta2.txt` and keeps every beta 2 feature.

- **The pour mode** and the MicroPython **"Drop 100,000"** are untouched, byte for byte: the `#PYTHON` block, `gbPour`, `gbBigDrop`, `gbDropFast`, `gbBallStep` and `gbDropAnim`.
- **It has not been run on hardware.** Nothing in it about the CAS has run on any calculator, and its Python part has still never run anywhere.

Beta 3 adds **exact answers from the CAS** behind the fence in BRIEF_CAS.md and Lessons Learned v7g §9b:

- every CAS call goes through one routine, `gbCas`;
- CAS text is built from whole numbers only, by `gbIStr` (p = 0.37 goes in as 37/100);
- the CAS is asked on events only, a tap on a bar or a new k, and the answer is cached;
- every exact answer keeps the program's own decimal (BINOMIAL, POISSON) as its fallback;
- a badge, **exact (CAS)** or **decimal**, says which one is on screen.

Line references are `beta 2 → beta 3`. The file grows from 1,621 to 2,177 lines, and from 47 routines to 62.

## (a) Changes

### The three that matter most

1. **Tap a bar: P(k) as an exact fraction** (`gbBinInfo` 1276 → 1555, new `gbXBin` 513). The panel now shows:
   - **The formula with this bin's numbers:** "P(4) = C(8,4) × (1/2)^4 × (1/2)^4".
   - **Its value:** "= 35/128 = 0.2734" with a badge. For p = 1/2 that is C(R,k)/2^R.
   - **How p is written:** as whole numbers in lowest terms (`gbPFrac` 431, `gbGcd` 413). p × 100 must be a whole number (arrows and drag always give one), or p × 1000 for a typed p such as 0.123.
   - **A p that is not a simple ratio** (0.3333) sends nothing to the CAS. The line reads "= 0.2734 (p not a simple ratio)" with the decimal badge.
   - **A fraction too long for the line** is never cut: "= 0.2163 (exact: 47 digits)" at R = 12, p = 0.37, k = 5.
   - **Layout:** the panel runs from y 14 to 127 (was 16 to 122), and its lines are 13 px apart (17, 36, 49, 62, 75, 88, 101, 114; were 19, 40, 53, 66, 79, 92, 105). It still ends above the count labels (127) and the red frame (132).
2. **A new page, "Where Poisson comes from (CAS)"**: Menu item 14 (E), `gbPoisson` 1830. **What it shows:**
   - μ = Rp of the board is held fixed. The binomial bars for R, 4R and 16R rows (p = μ/R, in pale, mid and dark blue) stand beside the Poisson(μ) bars (green).
   - The bars come from PPL's BINOMIAL and POISSON, computed once as the page opens (`gbPsCalc` 1670), for k = 0 to about μ + 3 SD (5 to 24).
   - **The CAS's part:** for the k under the finger (a tap on a bar or its label) or the arrows, it takes `simplify(limit(comb(gbq,k)*((m/d)/gbq)^k*(1-(m/d)/gbq)^(gbq-k),gbq,inf))` with k a number. Desktop Giac fails with a symbolic k ("Limit: Max order reached"), so the page asks once per k, when k changes.
   - **The screen** then shows the answer beside μ^k e^(−μ)/k! with this k's numbers: "as R → infinity = 32/(3×exp(1)^4)" and "= μ^k e^(-μ)/k! = 4^3 e^(-4)/3! = 0.1954".
   - **How the answer is drawn:** `*` is shown as ×. A long answer wraps onto a second line, and one too long for both lines gives its digit count. While the CAS works on a new k, a frame says "asking the CAS ...".
   - **The Poisson mean is called μ** (CHAR(956), verified) rather than λ, which is not a verified glyph.
3. **The CAS kit and its fence** (new section, 342–562).
   - `gbIStr` (373) and `gbCas` (391) are BRIEF_CAS's shapes. `gbCas` uses the updated kit, which drops one surrounding pair of quotes.
   - **One change from the kit:** the parameter of `gbIStr` is `gbIv`, because `gbN` is already the ball count.
   - **The infinity word** is written in one place, `gbInf := "inf"` in `gbInit`. If CASProbe T16 says only "infinity" works, that one line changes. Desktop Giac gives the same answer for `+infinity`.
   - **The CAS is reachable only from** `gbBinInfo` (a tap) and `gbPoisson` (a new k). It is never reached from the drop, pour, ×10, ×100 or lattice animations, the p drag, the scene or a frame. The verify script checks this with a call graph and by counting calls.

### The rest

4. **Helpers:**
   - `gbIsFr` (449): a fraction or whole number only, so a decimal handed back as a Home real means "no exact answer";
   - `gbFrDig` (471): digits;
   - `gbShow` (483): * → ×;
   - `gbBadge` (498);
   - `gbPsKey` (532) and `gbPsLim` (545): the limit, with a one-entry cache keyed on k and μ. A limit answer must contain `exp` and no `limit` or `inf`;
   - `gbMuS` (1655): μ with only the decimals it needs;
   - `gbPsDraw` (1701): one frame from the caches, with no CAS call in it.
5. **Menu** (`gbMenu` 1388 → 1936): 16 items. "Where Poisson comes from (CAS)" is 14 (E), Help 15 (F), Leave 16 (G); it was 15 (F). The list form of CHOOSE has no 14-item cap.
6. **Help** (`gbHelp` 1342 → 1868): page 2's footer now reads "Any key or tap: exact answers (page 3)". **New page 3, "Exact answers (CAS)":** 35/128 = 70/256, p = 0.3 as 3/10, the Poisson page and its limit, and the badge.
7. **New file-level state** (232–247), all checked case-insensitively against the built-ins:
   - `gbCasOK`, `gbInf`, `gbXKey`, `gbXTxt`;
   - `gbPsMN`, `gbPsMD` (μ as a fraction), `gbPsK`, `gbPsKm`, `gbPsB` (the bars), `gbPsR` ({R, 4R, 16R});
   - `gbPsCK`, `gbPsTx`.
   
   All are initialised in `gbInit` (2033).
8. **Header:** "beta 3", a dated "What changed" paragraph, the firmware line (the CAS has never run either), and the KEYS AND TOUCH lines for the exact panel and the new menu item.
9. **Two lint-visibility tweaks:** `biE := "" + gbXBin(biK)` and `pwMu := "" + gbMuS(…)`. The lint can only tell a variable holds text when the assignment shows it, and both lines carry a comment saying so.

**CAS variable:** `gbq`, a tagged name. No `#cas` block, `CAS.name()` call, purge or Python `cas` is used.

## (b) Gate (check.sh and ppl_gate_v1.py, final, after the kit's quote-stripping update)

```
--- 1. kit lint ---  1 error: "unbalanced ... -1" at EOF (line 2178).  As in beta 2: the kit
    counts the #END that closes the #PYTHON block as an END.  This is the 'unbalanced' the brief allows.
--- 2. ppl_check tally NEW: (none)      ORIG (beta 2): (none)
--- 2b. hard errors E2 E3 E6 E8 E10 E11: none
--- 3. lint_ppl: 1352 checks, 23 problems = beta 2's 15 (block depth -1 at #END, STRING(COMB(a,b),2,0)
    read as 4 arguments, 'pdG/dcG/ftG not a GROB', file-name and EXPORT discipline) plus 8 false
    alarms, all in the CAS kit and its helpers:
      396  cR := STRING(CAS(gbS));                        the kit's 1-argument STRING
      407  IF INSTRING(cR, "undef") > 0 OR ...           x2: INSTRING contains the letters "STRING"
      457  IF INSTRING("0123456789", fsC) == 0 THEN         (lint_ppl matches STRING( inside INSTRING())
      476  IF INSTRING("0123456789", MID(...)) > 0
      555  IF INSTRING(gbPsTx, "exp") == 0 OR ...         x3
    (line 664, STRING(COMB(...), 2, 0) read as 4 arguments, is beta 2's)
--- 4. full parse: PARSE FAIL at the file-level LOCAL after the EXPORT list, as beta 2: the tool's
    limit.  With the file-level EXPORT and LOCAL lines masked: beta 2 PARSE OK (47 functions),
    beta 3 PARSE OK (62 functions).
--- 5. 2177 lines, 86129 bytes
fleet_names_v2 over the latest version of every program in out/ (27 files):
    1233 routine names, 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches
```

## (c) Verification (`verify_GaltonBoard_beta3.py`; full output in `verify_GaltonBoard_beta3_output.txt`)

**4,016 checks, 0 failed.** Desktop Giac 1.9 (`icas`), Python `fractions`, SymPy 1.14, SciPy 1.18 and the run harness `ppl_run_v3.py`.

**A. Giac.**
- A symbolic k: `limit(comb(gbq,gbk)*(2/gbq)^gbk*…, gbq, inf)` → "Limit: Max order reached or unable to make series expansion Error: Bad Argument Value".
- k = 3, μ = 4 → `32/(3*exp(1)^4)`; μ = 37/10 → `50653*exp(-37/10)/6000`. `+infinity` gives the same answer as `inf`.
- `comb(8,4)*(1/2)^4*(1/2)^4` → `35/128`.

**B. The exact bin probability, 680 bins.** That is R = 3 to 12 (the program's maximum), every k, and p = 1/2, 3/10, 37/100, 1/20, 19/20, 1/4, 3/4, 0.123.
- **Against Python:** the program's CAS text, answered by Giac, equals the Fraction C(R,k) p^k (1−p)^(R−k) every time. Its float equals `scipy.stats.binom.pmf` to 1e-12.
- **Calls:** one CAS call per new bar, and none for the same bar again. p = 0.3333 and 1/7 send nothing.

The panel's two lines:

| Board | formula line | value line |
|---|---|---|
| R 8, p 0.5, k 4 | P(4) = C(8,4) × (1/2)^4 × (1/2)^4 | = **35/128** = 0.2734 |
| R 10, p 0.3, k 3 | P(3) = C(10,3) × (3/10)^3 × (7/10)^7 | = 66706983/250000000 = 0.2668 |
| R 12, p 0.37, k 5 | P(5) = C(12,5) × (37/100)^5 × (63/100)^7 | = 0.2163 (exact: 47 digits) |
| R 12, p 0.123, k 6 | P(6) = C(12,6) × (123/1000)^6 × (877/1000)^6 | = 0.0015 (exact: 69 digits) |

**C. The Poisson page.** Each limit text from the program was parsed with SymPy and compared exactly with μ^k e^(−μ)/k!: `simplify(difference) == 0` for every k drawn. Its float matches `poisson.pmf` to 1e-12. The PPL bars match `binom.pmf(k, R, μ/R)` and `poisson.pmf` for R, 4R and 16R to within 2e-15.

| Board | μ | k drawn | exact limits | Σ\|binomial − Poisson\| for R, 4R, 16R |
|---|---|---|---|---|
| R 8, p 0.5 | 4 | 0–11 | 12 | 0.337 > 0.066 > 0.016 |
| R 10, p 0.37 | 37/10 | 0–11 | 12 | 0.228 > 0.047 > 0.011 |
| R 3, p 0.05 | 3/20 | 0–5 | 6 | 0.013 > 0.003 > 0.001 |
| R 12, p 0.95 | 57/5 | 0–23 | 24 | 1.300 > 0.131 > 0.030 |
| R 8, p 0.3 | 12/5 | 0–9 | 10 | 0.182 > 0.039 > 0.010 |
| R 12, p 0.5 | 6 | 0–15 | 16 | 0.341 > 0.064 > 0.015 |
| R 10, p 0.05 | 1/2 | 0–5 | 6 | 0.024 > 0.006 > 0.001 |

**D. End to end in the harness.** The run: welcome, tap bar 4, Esc, the Menu soft key, item 14, a tap on k = 2, Right, Esc, Esc.

| | cas = 'giac' | cas = 'fail' |
|---|---|---|
| panel | "= 35/128 = 0.2734" + exact (CAS) | "= 0.2734" + decimal, no "/128" |
| Poisson page | k went 4 → 2 → 3. "as R → infinity = 32/(3×exp(1)^4)" and "= μ^k e^(-μ)/k! = 4^3 e^(-4)/3! = 0.1954" + exact (CAS). The "asking the CAS ..." frame appeared before each new k | "(the CAS did not answer)", the Poisson decimal still shown, decimal badge |
| CAS calls | 4 (the panel, k = 4, 2, 3) | 4 attempts, no runtime error |
| quoted answers (Giac's answer given an extra pair of quotes) | `gbCas` dropped them: "= 35/128 = 0.2734", no quote mark on screen | — |

**The animations ask nothing.** A held pour, ×10, Drop, ×100 and a peg tap (296 balls) made **0 CAS calls**. So did `gbBigDrop(300)` (its PPL fallback).

**E. The fence.**
- **Call graph:** only `gbXBin` and `gbPsLim` call `gbCas`; `gbXBin` is called only by `gbBinInfo`, and `gbPsLim` only by `gbPoisson`. `gbCas` is the one `CAS(` in the code.
- **Nothing in a loop reaches `gbCas`:** not `gbPour`, `gbDropAnim`, `gbBallStep`, `gbLattice`, `gbPress`, `gbDropFast`, `gbBigDrop`, `gbScene`, `gbFrame`, `gbLand`, `gbCol`, `gbBar`, `gbTheory`, `gbRefresh`, `gbPsDraw`, `gbPsCalc` or `gbHelp`.
- **Byte-identical to beta 2:** the `#PYTHON gbPyDrop` block, `gbPour`, `gbBigDrop`, `gbDropFast`, `gbBallStep`, `gbDropAnim`, `gbNewBall`, `gbPress`, `gbScene`, `gbTheory`, `gbLattice`, `gbLand`, `gbCol`, `gbFrame`, `gbDrain`, `gbWaitAny`.

**F. Layout.** The bar panel on 5 boards and the Poisson page on 7 boards: every line inside its frame by the harness's width estimate. The Poisson page has no soft keys, and its footer is at y 224.

Desktop Giac took about 30 ms per call, process start included. That says nothing about a G1.

## (d) DEVICE TEST CHECKLIST (least to most risky)

1. **Run CASProbe beta 1 first, on the G2 and the G1.**
   - **Call form:** if it reports a form other than `STRING(CAS(s))` (T04–T10), change the one IFERR line in `gbCas` (line 396).
   - **Infinity:** if T16 needed "infinity" instead of "inf", change `gbInf := "inf"` in `gbInit` (line 2061).
   - **Gate:** if T07 or T11 fail, expect every beta 3 line to show **decimal**. That is the designed fallback.
2. **Paste and Check.** No syntax error, and the `#PYTHON gbPyDrop … #END` block pastes intact.
3. **Beta 2's checklist, items 2–14** (`GaltonBoard_beta2_CHANGES.md` (d)): the pour, drops, drag, Pascal, SD colours and Drop 100,000 are byte-identical, so they should pass as before.
4. **Menu:** 16 items, with "Where Poisson comes from (CAS)" as E, Help as F and Leave as G. Help has 3 pages, and page 3 shows 13 lines with none clipped.
5. **Tap a bar (R = 8, p = 0.5, bin 4). Layout:**
   - the panel is a little taller than in beta 2;
   - its 8 lines are evenly spaced, and nothing overlaps the bars' count labels or the red frame.
6. **The CAS steps:**
   - (a) **The same panel. What you should see:**
     - "P(4) = C(8,4) × (1/2)^4 × (1/2)^4" in magenta;
     - "= 35/128 = 0.2734" with **exact (CAS)** at the right.
     - **If it says "= 0.2734" and decimal:** note CASProbe's T07/T11.
   - (b) **Right arrow** (p = 0.55), then tap bin 4. **What you should see:** "= 672417207/2560000000 = 0.2627", which just fits. Then **Up, Up** (R = 10) and tap bin 5: the fraction is too long, so the line reads "= 0.2340 (exact: 25 digits)".
   - (c) **Up to 12 rows, p back to 0.50**, tap bin 6. **What you should see:** "= 231/1024 = 0.2256".
   - (d) **Menu → Where Poisson comes from** (R = 8, p = 0.5: μ = 4, k starts at 4). **What you should see:**
     - first "asking the CAS ...", then "as R → infinity = 32/(3×exp(1)^4)" in magenta, and "= μ^k e^(-μ)/k! = 4^4 e^(-4)/4! = 0.1954" in green;
     - four values under the legend: 0.2734, 0.2088, 0.1985, 0.1954;
     - the light, mid and dark blue bars closing in on the green ones.
     - On a G1, time the "asking" frame.
   - (e) **Tap the bar group at k = 2, then Right.** k changes, with one "asking" frame each time. Esc returns to the board.
   - (f) **The board at p = 0.95, R = 12** (μ = 11.4), then the Poisson page and Right up to k = 23. Long answers wrap onto a second line, or say "(exact: N digits, too long to show)". Nothing runs off the right edge.
   - (g) **A p typed as 0.3333:** the panel says "(p not a simple ratio)", and the Poisson page says "p is not a simple ratio, so there is no exact limit". Both show the decimal badge.
   - (h) **The fence on the device:** pour, ×10 and the p drag must feel exactly as in beta 2 (no CAS pauses).
7. **Esc:** Home shows the summary line as before.

## (e) Not confirmed / left as is

- **Everything about the CAS on the calculator:**
  - the call form;
  - whether `limit` with `inf` works on the Prime's older Giac (CASProbe T16 tests one limit);
  - whether `simplify(limit(comb(…)…))` comes back in the same form as on the desktop. The screen shows whatever text the CAS gives, so another form only looks different;
  - G1 timing for the limit (k up to 24, μ = 57/5).
- **The quotes.** The kit's quote-stripping is harness-tested only.
- **The exact-mode setting** of the CAS is not read or set. An answer that comes back as a decimal fails `gbIsFr` (panel) or the "exp" test (Poisson), and the decimal is shown.
- **One-entry caches.** Each holds one answer (the last bar, the last k). Going back to an earlier k asks again. That is cheap on the desktop; whether it is cheap on a G1 is unknown.
- **The CAS answer on the Poisson page** is the CAS's own form ("32/(3×exp(1)^4)"), not rewritten as e^(−4)·32/3. Rewriting it would mean parsing the CAS's text in PPL. The line under it shows the textbook form with the same numbers.
- **λ (CHAR(955)) is not a verified glyph**, so the page uses μ. Roger may prefer λ once GfxProbe's glyph test (T14) or the Chars menu confirms it.
- **Kept from beta 2:** `CHAR(8730)` (√) in readouts and help, `WAIT(0.02)` in the single drop, the bare `RANDOM` idiom, and Home's K as the MAKELIST counter.
