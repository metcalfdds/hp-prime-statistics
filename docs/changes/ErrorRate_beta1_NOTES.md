# ErrorRate Lab beta 1: notes

*16 October 2026. A new program. It has not been run on hardware. 2,557 lines; tag `erl` (glued style: `erlBound`, `erlDrawMain` …); entry `EXPORT ErrorRate()`, no arguments. It is the fleet's first program to use all three engines: PPL draws and handles touch, MicroPython simulates, and the CAS writes exact answers.*

This is §5.1 of `CAS_Python_Ideas_2026-10-16_v1.md`, approved by Roger on 16 Oct 2026 at 21:15. Files:

- `ErrorRate_beta1.txt`: the program.
- `verify_ErrorRate.py`: the checks against SciPy, statsmodels, SymPy and desktop Giac, plus the harness runs. Its output is in `verify_ErrorRate_output.txt`: **161 PASS, 0 FAIL, 19 s**.
- `errorrate-guide_beta1.md`: the user's guide.

---

## 1 · The lesson, and what PCAST actually says (confirmed in the report)

"Zero errors in 30 proficiency tests: how good is the examiner?" Zero errors is not a zero error rate. An examiner whose true rate is 5 % also scores 0 of 30 with probability 0.95^30 = **21.5 %**. The honest number is the upper confidence bound: 1 − 0.05^(1/30) = **9.50 %**. The rule of three, 3/30 = 10 %, is that bound's large-n limit.

I downloaded PCAST (2016), *Forensic Science in Criminal Courts: Ensuring Scientific Validity of Feature-Comparison Methods*, and searched its text. The convention **is the one-sided 95 % Clopper–Pearson upper bound**:

- **§4.2 "Foundational Validity: Requirement for Empirical Studies", p. 51.** "When reporting a false positive rate to a jury, it is scientifically important to state the 'upper 95 percent one-sided confidence bound' to reflect the fact that the actual false positive rate could reasonably be as high as this value."
  - **Footnote 116:** no errors in 100 tests gives 3.0 % ("1 in 33"); no errors in 10 tests gives 26 %.
  - The same page says the false-positive rate should be calculated from **conclusive** examinations.
- **Appendix A "Statistical Issues", "Confidence Intervals", pp. 152–153.**
  - "Upper 95 percent one-sided confidence bounds should thus be used for assessing the error rates." Lower confidence levels "may rightly be viewed with suspicion as an attempt at obfuscation."
  - Zero false positives in 25 tests leaves "roughly 1 in 9".
  - Four methods are acceptable: Clopper–Pearson, Wilson, Agresti–Coull and Jeffreys. For 0 of 100 they give 0.030, 0.026, 0.032 and 0.019.
  - "(In this report, we used the Clopper-Pearson/Exact Binomial method.)"
- **§4.6 "Validity as Applied: Proficiency Testing", pp. 57–58.** This is the caveat:
  - testing should ideally be "test-blind";
  - non-blind tests "are likely to overestimate the accuracy because the examiners knew they were being tested";
  - that limitation should be reported "including to juries".

`verify_ErrorRate.py` reproduces every one of those numbers. The help pages cite §4.2 p. 51, App. A pp. 152–153 and §4.6 pp. 57–58, and so does the header.

## 2 · What it does

1. **Welcome page**, then the **main screen**, one G1 frame and one blit, followed by `DRAWMENU`.
   - **The curve (blue, 2 px):** P(k or fewer errors in n | true rate p). For k = 0 it is written out as (1 − p)^n. It is cached per pixel column, keyed on n, k, the window and the scale.
   - **The bands:** light green for rates the record allows, light red for rates it rules out at the one-sided level. The red band is labelled "ruled out at 95 %".
   - **The α line:** orange dashes, labelled "α = 0.05".
   - **The bound (red):** from the crossing down to the axis, with a square and its value just to the right of the crossing. The curve is always below α there, so the label never sits on it.
   - **The rule line (green dots):** labelled 3/n.
   - **The rate under the finger (magenta):** a line up to the curve, dots across to the y axis, and a dot on the curve.
   - **The n slider** at the right edge: log scale from 5 to 1000, ticks at 10, 30, 100, 300 and 1k, magenta knob.
   - **Header:** "0 errors in 30 tests, one-sided α = 0.05", then in red "95 % upper bound on the error rate: 9.50 %".
   - **Panel:**
     - "An examiner whose true rate is 5.0 % has / 0 errors in 30 tests 21.5 % of the time." This line turns red once the chance falls below α.
     - "3/n = 10.0 %, n × bound = 2.85 → 3.00".
   - **Window:** twice the larger of the bound and the rule line, rounded up to 1, 2 or 5 × 10^e (n = 30 gives 0 to 20 %). A drag of n freezes it; it refits on lift. The arrows refit only when the bound drifts far from the middle, so a run of key presses is seen on one window.
2. **Soft keys, two pages, with "More" in slot 6 on both** (the house convention):
   - page 1: `n, k | Rate | Why 3 | Bayes | Sim | More`;
   - page 2: `Trawl | Log y | Help | Eng | Quit | More`. "Log y" becomes "Lin y" while the log scale is on.
   - Hardware keys: ⇆ = rate, ⇅ = n ± 1, +/− = n up or down a step on a ladder (10, 15, 20, 25, 30, 40, 50, 75, 100 …), Enter = menu (the same ten actions, in a `CHOOSE`), Esc = quit.
3. **Two live drags:**
   - Along the plot: the true rate, snapped to 1/200 of the window. Each sample costs one CDF.
   - The right edge: n. Each new n reruns the bound and the curve. With k > 0 that is a 45-step bisection plus every third column, with straight lines between; the full curve is drawn on lift.
4. **Log y.** On a log scale the k = 0 curve is almost a straight line, ln P ≈ −np, which is the rule of three drawn. The scale runs from 1 down to 10^(⌊log α⌋ − 1).
5. **Why 3 (the CAS page).**
   - For **k = 0**:
     - "(1-p)^30 = 1/20";
     - "p = 1-(1/20)^(1/30)" (CAS);
     - "= 0.09503 = 9.50 %" (PPL);
     - "n × bound = 2.851";
     - "n(1-(1/20)^(1/n)) → ln(20)" (CAS limit) "= 2.9957";
     - "so 3/n is a large-n LIMIT, a little too high for small n".
   - For **k > 0** (k ≤ 6):
     - "(1-p)^28×(406×p^2+28×p+1) = 1/20" (the polynomial is the CAS's);
     - PPL's bisection value;
     - the Poisson limit "(μ^2+2×μ+2)×e^(-μ)/2 = 1/20" (CAS);
     - "μ = 6.296, so the rule is 6.30/n".
   - Every line comes from the CAS or, failing that, from PPL text, and the page carries the badge "exact (CAS)" or "decimal".
   - ⇅ or +/− change n on this page, and the CAS is asked again (an event).
6. **Bayes.**
   - The prior is Beta(a, b): soft keys Unif (1, 1), Jeff (½, ½), or "a, b" (an `INPUT`, in halves from 0.5 to 100).
   - The posterior Beta(a + k, b + n − k) is drawn in magenta. The area under it is light blue up to the true rate and pink beyond it, and that pink area **is** "P(true rate > 5.0 %) = 20.4 %". The prior is grey dots.
   - Marked: the upper credible bound (magenta), Clopper–Pearson (red dots), the mean (green dots) and the true rate (orange).
   - Panel: "mean (a+k)/(a+b+n) = 1/32 = 3.13 %", with the CAS's exact fraction; "95 % credible bound 9.21 % (CP 9.50 %)"; and the P(rate > p0) line. Dragging along the plot moves the rate live.
7. **Sim.**
   - MicroPython runs 10,000 proficiency programmes of n tests at the true rate.
   - The bars count errors: green = a record at least as good as this one; magenta squares = the binomial expectation.
   - "0 errors: 2,154 of 10,000 = 21.5 %", beside "exact chance (1 - p)^30 = 21.5 %".
   - The badge reads "engine: MicroPython, 10,000 in … ms", or "engine: PPL fallback, 1,000 in … ms".
   - Soft keys Again, Rate−, Rate+ (also Enter, ←, →).
8. **Trawl.**
   - The curve is P(at least one chance match) = 1 − (1 − RMP)^N against N, from 1 to 100 million on a log scale, with N × RMP as magenta dots while it is below 1.
   - Drag (or ⇆) to set N. RMP is a `CHOOSE` of seven values, 1 in 1,000 to 1 in 1 billion, labelled "illustrative RMP values, not casework". N can also be typed in.
   - **Exact** opens a CAS page:
     - the exact expression "1-(999999/1000000)^N";
     - the limit "P → -e^(-μ)+1";
     - the series "μ-1/2×μ^2+1/6×μ^3 - ...";
     - PPL's numbers at that N, and the half-way N (693,147 at 1 in a million).
9. **Help:** nine drawn pages.
   1. Zero errors is not a zero rate (with PCAST).
   2. Reading the plot.
   3. The rule of three (2.59 / 2.85 / 2.95 / 2.99; 4.74 / 6.30 / 7.75).
   4. Confidence or credibility (1/32, 9.21 %, 1/62, 6.15 %, and PCAST's four methods).
   5. Simulation.
   6. Database trawls.
   7. Honest caveats (PCAST §4.6, independence, conclusive answers only, one examiner on these tests, one-sided 95 % = the top of a two-sided 90 %).
   8. Keys and touch.
   9. Three engines.
10. **Eng (engines page):** what ran last, with a **live probe of each engine**: `erlCas("1/2+1/3")` must give "5/6", and Python is run with 50 programmes and must answer. It also shows the stage marker `ER_PYZ`.
11. **Quit** returns "ErrorRate: 0 errors in 30 tests -> 95 % upper bound 9.50 % (3/n = 10.0 %); see ER_UPPER". These stay in Home: `ER_UPPER, ER_N, ER_K, ER_ALPHA, ER_RATE, ER_PASS, ER_RULE, ER_BMEAN, ER_BUPPER, ER_SIM, ER_TRAWL`, and the bridge `ER_PYN, ER_PYP, ER_PYM, ER_PYK, ER_PYW, ER_PYO, ER_PYZ`.

## 3 · The maths, and which engine does it

| Quantity | Formula | Engine |
|---|---|---|
| Bound, k = 0 | (1 − p)^n = α, so p = 1 − α^(1/n) | PPL (the CAS shows the closed form) |
| Bound, k > 0 | `BINOMIAL_CDF(n, p, k)` = α, 45 halvings of [0, 1] | PPL (the CAS shows the equation) |
| Bound, k = n | 1: no rate is ruled out | PPL |
| Rule line | n × bound → μ with P(Poisson(μ) ≤ k) = α: −ln α for k = 0; `CHISQUARE_ICDF(2k+2, 1−α)/2` otherwise. The line uses exactly 3 at k = 0, α = 0.05 | PPL |
| Posterior | Beta(a + k, b + n − k), mean (a + k)/(a + b + n) | PPL; the CAS gives the fraction |
| Beta CDF | `FISHER_CDF(2a, 2b, b x / (a (1 − x)))`. The parameters are kept doubled, so the df are whole numbers even for Jeffreys | PPL |
| Credible bound | the Beta CDF solved by 50 halvings | PPL |
| Densities | exp((a−1) ln x + (b−1) ln(1−x) − ln B(a,b)), with ln Γ by Lanczos (Burr3's `b3_lngamma`, retagged) | PPL |
| Simulation | jumps from error to error: the clean run before an error is geometric, ⌊ln U / ln(1 − p)⌋ | Python, with a PPL fallback |
| Trawl | 1 − e^(N ln(1 − RMP)), with ln(1 − RMP) from four series terms, and 1 − e^(−x) as a series for x < 10⁻⁴ | PPL; the CAS gives the expression, limit and series |

**The CAS templates.** All of them are built by `erlIStr` from whole numbers. The symbolic names are `erlq` and `erll`. Every one goes through `erlCas`.

| Where | Template (n = 30, k = 2, α = 0.05) | Desktop Giac 1.9 answers |
|---|---|---|
| α | `50/1000` | `1/20` |
| k = 0 closed form | `1-(50/1000)^(1/30)` | `1-(1/20)^(1/30)` |
| k = 0 limit | `limit(erlq*(1-(50/1000)^(1/erlq)),erlq,inf)` | `ln(20)` |
| k > 0 polynomial | `normal(comb(30,0)*erlq^0*(1-erlq)^2+comb(30,1)*erlq^1*(1-erlq)^1+comb(30,2)*erlq^2*(1-erlq)^0)` | `406*erlq^2+28*erlq+1` |
| k > 0 Poisson limit | `factor(limit((1-erll/erlq)^erlq+erlq/1*(erll/erlq)^1*(1-erll/erlq)^(erlq-1)+erlq*(erlq-1)/2*(erll/erlq)^2*(1-erll/erlq)^(erlq-2),erlq,inf))` | `(erll^2+2*erll+2)*exp(-erll)/2` |
| Bayes mean | `(2)/(64)` | `1/32` |
| Trawl, exact | `1-(1-1/1000000)^erlq` | `1-(999999/1000000)^erlq` |
| Trawl, limit | `limit(1-(1-erll/erlq)^erlq,erlq,inf)` | `-exp(-erll)+1` |
| Trawl, series | `convert(series(1-exp(-erll),erll=0,3),polynom)` | `erll-1/2*erll^2+1/6*erll^3` |
| Engines probe | `1/2+1/3` | `5/6` |

Three of these templates were changed after desktop Giac showed problems:

1. **The k > 0 template used to factor the whole sum.** For n = 10,000 desktop Giac took **over 60 s**, because it expands (1 − p)^10000. On a calculator that would freeze the program. Every term of the sum has the factor (1 − p)^(n − k), so the program now writes that factor itself and asks the CAS only for the degree-k bracket. The bracket costs the same for any n and still carries the exact coefficients PPL cannot hold: C(1000, 5) has 13 digits.
2. **`expand` left non-canonical terms** (`405*erlq^2+(-erlq)^2+…`), so the bracket uses `normal`.
3. **A sum over a symbolic index makes Giac try to solve Gamma equations**, so every sum is written out with numeric j.

The exact trawl probability, (999999/1000000)^1000000, is never sent to the CAS: as a fraction it would have millions of digits.

**The display transform (`erlShow`).**

- `erlq` becomes p (or N on the trawl page), `erll` becomes μ, `exp(` becomes `e^(`, and `*` becomes ×.
- Giac writes the factor (1 − p)^m as `(p-1)^m` or `-(p-1)^m`, depending on whether m is even or odd. Both equal (1 − p)^m, so the leading factor is written as `(1-p)^m`.
- Long answers wrap at "+", "=" or "×", over at most three lines. Anything longer says how many characters it has, so an exact answer is never cut silently.

## 4 · Verification (verify_ErrorRate.py: 161 PASS, 0 FAIL, 19 s)

```
A. the program's own routines, in the harness, against SciPy / statsmodels
   erlBound = beta.ppf(1-a, k+1, n-k) = statsmodels proportion_confint(k, n, alpha=2a, 'beta')[1]
     276 cases (alpha .001-.5, n 1-10000, k 0-10), worst |diff| 1.4e-14
   PCAST examples: 0 in 10 -> 0.2589 (26 %), 0 in 25 -> 0.1129 (1 in 9), 0 in 100 -> 0.0295 (3.0 %)
   erlTail = binom.cdf 3.1e-16; erlRuleC: P(Poisson(mu) <= k) = alpha
     rules at 0.05: k=0 2.9957, 1 4.7439, 2 6.2958, 3 7.7537, 4 9.1535, 5 10.5130
   erlLnGam = gammaln 3.8e-13 (rel); erlBetaCdf = beta.cdf (FISHER_CDF route) 0.0; erlBetaQ = beta.ppf 3.1e-16
   uniform 0/30: mean 1/32, credible 0.09211; Jeffreys 0/30: mean 1/62, credible 0.06152; densities = beta.pdf
   uniform-prior bound for 0 of n = Clopper-Pearson for 0 of n+1; P(rate > 5 %) = 0.95^31 = 0.2039
   erlTrP = -expm1(N log1p(-RMP)), RMP 1E-3..1E-9, N 1..1E8, worst 2.4e-13 (rel); half-way N 693,147
   windows: 0/30 -> 0-20 %, 0/10 -> 0-100 %, 0/100 -> 0-10 %, 0/1000 -> 0-1 %, 2/30 -> 0-50 %
B. every quoted number (14), recomputed and found in the file: 21.5 %, 9.50 %, 2.59/2.85/2.95/2.99,
   4.74/6.30/7.75, 1/32 and 9.21 %, 1/62 and 6.15 %, PCAST's 3.0/2.6/3.2/1.9 %, ~2,150 of 10,000, 63.2 %
C. 25 k = 0 templates (n 1..10000 x alpha 1/20, 1/100, 1/1000, 1/2, 1/40), 8 k > 0 templates
   (k 1..6, n 2..10000), 5 Bayes fractions, 3 trawl RMPs: every Giac answer equal to SymPy's
   (polynomial identities by expand; limits and fractions symbolically); k = 7 and k = n make
   no CAS call they should not; erlCas strips one pair of quotes, rejects undef, returns "" on
   failure; erlShow display strings; Giac 33-141 ms a call on the PC
D. the #PYTHON block under CPython (stub hpprime, urandom): urandom only, no f-strings/format/
   join; 44 writes in index order, the total last; marks 1-2-3; bins fit Binomial(n, p) by chi-
   square for (30, .05), (30, .2), (1000, .003), (200, .3, bins of 3), (10, .5); p = 0 and p = 1
E. end to end: E1 CAS by Giac + Python (patched to run the block); E2 cas='fail' + Python absent
   ("decimal" badges, "PPL fallback, 1,000", no runtime error); E3 a half-written or bad-sum
   payload -> PPL fallback; E4 k = 2, alpha typed as "1" (1 %), n dragged to 750, log scale;
   E5 stale-key mode: no page skipped; E6 20 drag samples: 0 CAS calls (the fence);
   cost: k = 0 drags 0 BINOMIAL_CDF a frame; k = 2: 1,589 in 23 frames (an n frame is
   45 bisection + 87 curve columns; a rate frame is 1); no text below y 218 on a soft-key page;
   no text-page line over 46 characters; no MSGBOX over five lines
```

The harness is a test of logic and layout, not of the device.

- **Python:** it does not run Python. E1 patches `PYTHON()` to run the block in CPython, reading and writing the harness's PPL globals through the same `NAME(i):=v` strings the block sends to `hpprime.eval` (the GaltonBoard method).
- **CAS:** its answers come from desktop Giac 1.9, which is newer than the Prime's Giac.
- **Clock:** TICKS is virtual, so the ms figures in the badges mean nothing here.
- **Rounding:** 3.125 % prints as "3.12" here (IEEE rounds half to even). The Prime's decimal rounding should print 3.13, and the test accepts either.

## 5 · Gate

`bash check.sh ErrorRate_beta1.txt CICatcher_beta1.txt`

```
1. kit lint: 1 error -- "unbalanced: -1 openings too many" at the end of the file: the #PYTHON
   block's '#END' (GaltonBoard beta 2 gives the same).  With the block removed: 0 errors,
   2 warnings ("PYTHON is not a PPL name").
2. ppl_check_v3 tally: clean.  Hard errors E2/E3/E6/E8/E10/E11: none.
3. lint_ppl: 1,629 checks, 16 problems, all known noise:
     line 1605 "block depth went negative" + "final depth -1": the #PYTHON block's #END (as GaltonBoard)
     lines 395, 405, 484 (x2) "STRING() with 2 args": its regex matches the STRING( inside INSTRING(
     line 473 "STRING() with 1 args": STRING(CAS(ecQ)), the BRIEF_CAS kit's own line
     (the rest are the EXPORT-discipline lines the gate filters)
4. full parse: "expected a name after EXPORT" -- the kit cannot read the EXPORT list followed by
   file-level LOCAL; CICatcher_beta1 fails the same way (a tool limit).  The ppl_run_v3 harness
   parses and runs the whole file.
5. 2,557 lines, 96,572 bytes; no non-ASCII in code.
```

`python3 ppl_gate_v1.py ErrorRate_beta1.txt`: **RESULT: PASS**.

- 2. clean, no hard errors.
- 3. the noise above.
- 5. `fleet_names_v2` reported 725 collisions over the 72 files in out/, none of them involving ErrorRate. Old and new versions of the other programs sit side by side there.

Over the **newest version of each of the 27 programs**, including CASProbe beta 1 and the CAS versions written alongside this one (BayesTree beta 8, ChiTable beta 3, EpiStats v1.7 …): **0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches**. The tag `erl` is used by no other file.

Names changed by the gate: the parameter `caS` became `ecQ` (it is CAS when case is ignored), and the LOCAL `rpL` became `rpLn` (`rpl` is in the built-in list).

## 6 · Device test checklist (least to most risky)

0. **Run CASProbe beta 1 first**, on the G2 and then the G1.
   - If its summary names a different call form (T08's `EXPR("CAS(" + q + s + q + ")")` or T09's `CAS.eval`), change the one IFERR line in `erlCas` (line 473) to that form.
   - If T16 fails with `inf` but T16b passes with `infinity`, change line 2463 to `erlInf := "infinity";`.
   - Those two lines are the only places the probe's verdict touches.
1. **Paste and sync.** The only error should be none. If the Connectivity Kit appends stray CJK characters at the very end, delete them.
2. **Launch from the Catalog.** The orange welcome page appears; any key or tap goes on.
3. **The main screen, pure PPL.** What you should see:
   - "0 errors in 30 tests, one-sided α = 0.05";
   - red "95 % upper bound on the error rate: 9.50 %";
   - a blue curve falling from the top left;
   - green and red bands meeting at about 47 % of the plot width;
   - orange dashes 7 px above the axis labelled "α = 0.05";
   - the red marker labelled "9.50 %";
   - green dots labelled "3/n" just right of it;
   - a magenta marker at 5 %;
   - panel "An examiner whose true rate is 5.0 % has / 0 errors in 30 tests 21.5 % of the time." and "3/n = 10.0 %, n × bound = 2.85 → 3.00";
   - soft keys `n, k | Rate | Why 3 | Bayes | Sim | More`.

   Check that ⇅ ⇆ × α and **→** render: → is CHAR(8594), which §13 says renders and GfxProbe T14 re-checks.
4. **Keys.**
   - ⇆ moves the rate in 0.5 % steps.
   - ⇅ changes n by one. The window stays put, so the curve steepens and the red marker moves left.
   - +/− step n along 30 → 40 → 50 ….
   - Esc quits; Enter opens the menu (the 10th item shows as "A").
5. **Drag the rate along the plot.** The magenta marker follows and the panel updates live. Past the red marker, the second panel line turns red.
6. **Drag the right edge (n).** The knob follows and n changes live; the window refits when the finger lifts. **Time it on the G1.**
7. **More, then Log y.** The k = 0 curve becomes nearly straight, with axis labels 1, .1, .01, .001. Lin y returns. More on page 2 goes back to page 1.
8. **n, k: n = 30, k = 2, α = 0.05.** The bound is 19.5 % and the green line reads "6.30/n = 21.0 %".
   - **Drag n on the G1 with k = 2.** Each new n costs 45 + 87 BINOMIAL_CDF calls.
   - If it lags, raise the stride in `erlDragN` (line 1015, `dnS := 3`) to 6, or cut the bisection to 35 steps (line 539).
   - A one-line check of the argument order: `BINOMIAL_CDF(30, 0.2, 2)` in Home should give 0.04418.
9. **Trawl** (page 2). The P curve rises through 63.2 % at N = 1,000,000; drag N; RMP via the `CHOOSE`; N via `INPUT`.
10. **Help: the nine pages.** Every line fits inside the blue frame, and Esc leaves.
11. **Python: Sim, with the Terminal open (Shift-View after).**
    - You should see "Simulating 10,000 programmes ...", then bars with a tall green bar at 0 errors, magenta squares on or near the bar tops, "0 errors: about 2,150 of 10,000 = 21.x %", "exact chance (1 - p)^30 = 21.5 %", and **"engine: MicroPython, 10,000 in … ms"** in green. Note the ms on the G2 and the G1.
    - If the orange "PPL fallback" appears instead, read the Terminal traceback and type `ER_PYZ` in Home: 0 means it never started, 1 means it read its inputs, 2 means it finished the loop, 3 means it wrote everything.
    - Rate+ and Rate− rerun the simulation.
12. **The CAS steps, last** (each page asks the CAS on opening). Time each page on the G1.
    - **Why 3.** What you should see:
      - "a clean record only 1/20 likely:";
      - "(1-p)^30 = 1/20";
      - magenta "p = 1-(1/20)^(1/30)", which the Prime may write as `-(1/20)^(1/30)+1`, still correct;
      - red "= 0.09503 = 9.50 %";
      - "n(1-(1/20)^(1/n)) → ln(20)";
      - "= 2.9957";
      - the badge **"exact (CAS)"** top right.

      Press + and − and the CAS answers again for n = 40.
    - **Why 3 with k = 2**: "(1-p)^28×(406×p^2+28×p+1) = 1/20" and "(μ^2+2×μ+2)×e^(-μ)/2 = 1/20". With k = 6 the formula wraps onto two lines.
    - **Bayes**: "mean (a+k)/(a+b+n) = 1/32 = 3.13 %", the badge "exact (CAS)", "95 % credible bound 9.21 % (CP 9.50 %)" and "P(true rate > 5.0 %) = 20.4 %". Jeff gives 1/62 and 6.15 %. a, b = 1, 19 gives "Beta(1, 19), your prior". Drag the rate.
    - **Trawl → Exact**: "1-(999999/1000000)^N", "P → -e^(-μ)+1" and "μ-1/2×μ^2+1/6×μ^3 - ...", with the badge.
    - **Eng**: "live check: 1/2+1/3 = 5/6, as it should" and "live check: MicroPython answers".
    - **If any CAS line shows the formula in plain decimals with "decimal"**, the CAS call failed and the program carried on, as designed. Note which page it was.
13. **Quit** (page 2, Quit). Home shows the summary; then type `ER_UPPER` and expect 0.0950338528553.

## 7 · Not verified, stated plainly

- **No CAS call has run on a Prime.** The open points:
  - the call form;
  - `inf` against `infinity`;
  - whether a numerical-mode answer arrives in quotes (the kit strips one pair either way);
  - the Prime's output style (desktop Giac 1.9 is newer);
  - G1 timing.

  CASProbe tests the call form, `limit` with `inf`, `comb`, `exact`, `solve`, `fsolve`, `int`, `expand` and undef. It does **not** test `normal`, `factor`, `convert(…, polynom)`, `series`, or a `limit` over a falling-factorial sum. Those are checklist step 12, and each falls back to decimals if it fails.
- **The MicroPython block has never run on a calculator.** Unverified there:
  - `hpprime.eval` writing an EXPORTed list element by element (`ER_PYO(i):=v`, the GaltonBoard beta 2 method, also never run);
  - `int(float(ppl(...)))` reads;
  - the speed of 10,000 programmes;
  - MicroPython's float precision (it does not affect the counts).

  Against all of that: no `random`, no `time`, no f-strings, no `join`, and the three guards plus a PPL fallback are in place.
- **`DRAWMENU` with a list held in a variable** (`dmL := erlSKLab(); DRAWMENU(dmL);`). The device-verified uses pass a literal list. The More convention in TouchKit v2 uses a variable too, also unrun.
- **`INSTRING`** has run only on the emulator (PyProbe beta 2b). It is the CAS kit's own choice.
- **`BINOMIAL_CDF(n, p, k)`'s argument order** rests on HP's help, Lessons Learned §3 and the harness. The GaltonBoard beta 1a question was about `BINOMIAL`; checklist step 8 gives the one-line check.
- **`FISHER_CDF` with large df** (up to 2n + 1 = 20,001). The built-in is verified, but not at that size.
- **Text widths are estimates** (font 1 ≈ 6.5 px a character). Lines are kept to 46 characters and every `TEXTOUT_P` passes a width, but expect a pixel-nudge round, as §6 says.
- **The MAKELIST counter** stays Home's `K`, the house form pending GfxProbe T19.

## 8 · Decisions for Roger

1. **Default y scale: linear, with Log y on page 2.** On a log scale the rule of three is a straight line, which is very clear, but it is a second idea for an intro class. Should log be the default?
2. **The green "rule" line.** It shows exactly 3/n only in the classic case (k = 0, α = 0.05). Otherwise it shows the Poisson limit: 6.30/n for 2 errors, 4.61/n at α = 0.01. Keep that, or always show 3/n?
3. **The simulation jumps from error to error** (a geometric gap) instead of tossing a coin for every test. It is the same distribution, much faster for large n, and identical in Python and in PPL. A literal coin-per-test loop would be easier for students to read and slow for n ≥ 300. Which do you want?
4. **Simulation sizes:** 10,000 in Python, 1,000 in the PPL fallback.
5. **Trawl defaults:** RMP 1 in a million and N = 1 million (expected chance hits = 1, P = 63.2 %). The seven RMP values run from 1 in 1,000 to 1 in a billion and are labelled illustrative.
6. **The Bayes panel prints "P(true rate > 5.0 %) = 20.4 %"**, a direct Bayesian answer to "how good is the examiner?", next to the frequentist bound. Is that the framing you want in a criminal-justice course?
7. **CAS lines for k ≤ 6 only**, because the Poisson-limit template grows with k. Above that the page says "(k > 6: the CAS lines are skipped)". α runs from 0.001 to 0.5; n from 1 to 10,000 (the slider covers 5–1000).
8. **The examples are deliberately generic** ("examiner", "proficiency tests", "a 5 % examiner"), with no discipline named. Bitemark, latent-print or firearms framings would be easy to add to the help pages if you want them for a particular course or talk.
