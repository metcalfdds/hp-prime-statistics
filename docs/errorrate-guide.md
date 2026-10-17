# ErrorRate Lab beta 1a: User's Guide

Proficiency tests and error rates on the HP Prime: **"Zero errors in 30 tests: how good is the examiner?"** It uses PPL, MicroPython and the CAS.

**Status:** written for the 2026-09-09 firmware (2.4.2), and **not yet run on hardware**. It was the fleet's first program to call the CAS.
- **On the HP Prime Virtual Calculator** (2.4.2, build 2026-09-09, 17 Oct 2026), beta 1's welcome page and main plot passed (0 errors in 30 tests: 95 % upper bound 9.50 %), but its Why 3 page showed its own question under "exact (CAS)". Beta 1a fixes that. On the same page it now reads **ln(20) = 2.9957**, a real CAS answer that matches the program's own decimal: the first CAS answer from a fleet program on the Prime's firmware.
- Every formula and every number on the help pages was checked against SciPy and statsmodels.
- Every CAS answer was checked against desktop Giac 1.9 and SymPy.
- The whole program was run off-device in the fleet's run harness (`verify_ErrorRate.py`; for beta 1a, `verify_ErrorRate_beta1a.py`).

The device-test checklist is in `ErrorRate_beta1_NOTES.md`; `ErrorRate_beta1a_CHANGES.md` adds what changed. On a G1, run CASProbe beta 1b once to time the CAS there.

beta 1a (17 Oct 2026): the CAS call form. CASProbe beta 1b showed that `CAS(s)` hands back the text of `s` unevaluated. `erlCas` now sends the text through `EXPR` and asks the CAS for a string; an answer with ∞ in it is refused, like one with `undef` or an error. The Eng page's grey CAS lines now name the form CASProbe beta 1b found. Nothing else changed.

beta 1 (16 Oct 2026): first version, from *The CAS and MicroPython in the fleet: ideas, v1*, §5.1.

Run `ErrorRate()` from the Program Catalog. Install as `.txt` through the Connectivity Kit editor; there is no separate `.py` file.

## The idea

An examiner takes **n = 30** proficiency tests and makes **0 errors**. That is not a zero error rate.

- An examiner whose true error rate is 5 % would also make no errors in 30 tests 0.95^30 = **21.5 %** of the time, about one time in five.
- The honest summary is the **upper 95 % confidence bound**: the highest error rate that still produces a record this good at least 5 % of the time. For 0 errors in n tests it is 1 − 0.05^(1/n), so **9.50 %** for n = 30.
- Rates above the bound are ruled out; rates below it are not.
- The **rule of three**, 3/n (10 % here), is what that bound tends to as n grows. It is a limit, not the bound itself.

This is the number PCAST asked forensic disciplines to report from black-box studies. *Forensic Science in Criminal Courts* (2016):
- **§4.2, p. 51:** "it is scientifically important to state the 'upper 95 percent one-sided confidence bound' to reflect the fact that the actual false positive rate could reasonably be as high as this value". Footnote 116 adds: no errors in 100 tests means "as high as 3.0 percent"; no errors in 10 tests, 26 percent.
- **Appendix A, pp. 152–153:** "Upper 95 percent one-sided confidence bounds should thus be used for assessing the error rates", and "In this report, we used the Clopper-Pearson/Exact Binomial method." That is the bound this program computes.

## The main screen

| What | Meaning |
|---|---|
| **Blue curve** | the chance of a record this good (k or fewer errors in n tests) at each true error rate; for 0 errors it is (1 − p)^n |
| **Orange dashes** | α = 0.05, one-sided |
| **Red marker** | where the curve crosses α: the **upper bound**, with its value |
| **Green / red bands** | rates the record allows / rates it rules out at 95 % |
| **Green dots** | the rule-of-three line, 3/n (for 1 or more errors, its version: 4.74/n, 6.30/n …) |
| **Magenta marker** | the true rate under your finger, and the chance of the record at that rate |
| Right edge | the **n slider**, 5 to 1000 on a log scale, magenta knob |
| Header | the record ("0 errors in 30 tests, one-sided α = 0.05") and, in red, the bound |
| Panel | "An examiner whose true rate is 5.0 % has 0 errors in 30 tests 21.5 % of the time." This line turns red once that chance is below α, so that rate is ruled out. Below it: "3/n = 10.0 %, n × bound = 2.85 → 3.00" |

The window is fitted to n (0 to 20 % for n = 30). It stays frozen while you drag n, so the curve visibly steepens and the red marker slides toward the axis; it refits when you lift your finger.

## Keys, soft keys and touch

| Action | Touch | Keys |
|---|---|---|
| true rate | drag along the plot | ⇆ |
| n | drag the right edge | ⇅ (n ± 1); + / − (10, 15, 20, 25, 30, 40, 50, 75, 100 …) |
| set n, k and α | soft key **n, k** | menu |
| type a true rate | soft key **Rate** | menu |
| the algebra (CAS) | soft key **Why 3** | menu |
| Bayesian view | soft key **Bayes** | menu |
| simulation (Python) | soft key **Sim** | menu |
| database trawl | **More**, then **Trawl** | menu |
| log / linear y | **More**, then **Log y** / **Lin y** | menu |
| help, engines, quit | **More**, then **Help**, **Eng**, **Quit** | menu; Esc = quit |

**More** (slot 6) is on both pages of soft keys and switches between them. **Enter** opens a menu with all ten actions.

- **n, k:** n from 1 to 10,000; k from 0 to n; α from 0.001 to 0.5. α can be typed as a percent: 5 means 0.05.
- **Rate:** a value from 0 to 1, or a percent (5 means 5 %); the window widens to show it.

### Log y

On a log scale the 0-error curve is almost a **straight line**, because ln P ≈ −n p. It reaches ln 0.05 at p ≈ 3/n. That is the rule of three, drawn.

## Why 3 (the CAS page)

**For 0 errors** the CAS writes the algebra exactly:
- (1 − p)^30 = 1/20;
- p = 1 − (1/20)^(1/30), which PPL evaluates as 0.09503 = 9.50 %;
- the limit n(1 − (1/20)^(1/n)) → ln(20) = 2.9957.

So 3/n is a large-n **limit**. For small n it is a little too high: n × bound is 2.59 at n = 10, 2.85 at 30, 2.95 at 100 and 2.99 at 1000.

**For k errors (1 to 6)** there is no closed form.
- The CAS shows the exact equation, for example (1 − p)^28 × (406 p² + 28 p + 1) = 1/20 for 2 errors in 30.
- PPL solves it by halving an interval 45 times: 19.5 %.
- The CAS then lets n grow with n × p = μ fixed. The binomial becomes a Poisson, (μ² + 2μ + 2) e^(−μ)/2 = 1/20, which gives μ = 6.30: the "rule of 6.3" for 2 errors (4.74 for 1 error, 7.75 for 3).

⇅ or +/− change n on this page, and the CAS answers again. The badge at the top right reads:
- **exact (CAS)** when the CAS answered;
- **decimal** when it did not. The same formulas are then written out by the program, with the same decimals.

## Bayes

A different question: given the record, what should we believe about this examiner's rate?
- Start from a prior **Beta(a, b)**. Soft keys:
  - **Unif** (1, 1): every rate equally likely;
  - **Jeff** (½, ½): Jeffreys;
  - **a, b**: your own prior, in steps of 0.5. For example, Beta(1, 19) says "about 5 % before any tests".
- Add k errors and n − k passes, and the posterior is **Beta(a + k, b + n − k)**, drawn in magenta.

| 0 errors in 30 | Posterior mean (a + k)/(a + b + n) | Upper 95 % credible bound |
|---|---|---|
| Uniform prior | **1/32** = 3.13 % | 9.21 % |
| Jeffreys prior | **1/62** = 1.61 % | 6.15 % |
| Clopper–Pearson (no prior) | — | 9.50 % |

The fractions come from the CAS. The Jeffreys bound is the **Jeffreys interval**, one of PCAST's four acceptable methods (App. A, p. 153). For 0 errors in 100 tests, PCAST gives Clopper–Pearson 3.0 %, Wilson 2.6 %, Agresti–Coull 3.2 % and Jeffreys 1.9 %.

Drag along the plot to move the true rate. The **pink area** under the posterior is the chance the true rate exceeds it: "P(true rate > 5.0 %) = 20.4 %" with the uniform prior. Lines mark the credible bound (magenta), Clopper–Pearson (red dots), the mean (green dots) and the rate (orange).

## Sim (MicroPython)

**10,000 examiners**, every one with the SAME true rate (the one under your finger), each take n tests.
- The bars count their errors. Green bars are records at least as good as this one; magenta squares are what the binomial predicts.
- At 5 %, about **2,150 of 10,000** finish 30 tests without a single error, beside the exact chance (1 − p)^30 = 21.5 %. A clean record from a small n is weak evidence of a low rate.
- **Again** reruns; **Rate−** and **Rate+** (or ⇆) move the rate and rerun.

The badge says which engine did the work:
- **engine: MicroPython, 10,000 in … ms** when Python ran;
- **engine: PPL fallback, 1,000 in … ms** if Python failed. The answers are still correct, just from fewer programmes.

Each simulated programme jumps from one error to the next. The run of clean tests before an error has a geometric length, ⌊ln U / ln(1 − p)⌋, which gives the same distribution as tossing a coin for every test and is far quicker when errors are rare.

## Database trawl

A crime-scene profile with random match probability **RMP** is searched against a database of **N** profiles. If the source is not in the database, each profile still matches by chance with probability RMP, so

  **P(at least one chance match) = 1 − (1 − RMP)^N**, and the expected number of chance matches is **N × RMP**.

When N × RMP = 1, P is 63.2 %, not 100 %.

- Drag along the plot (or ⇆) to set N, from 1 to 100 million on a log scale.
- **RMP** picks one of seven values, 1 in 1,000 to 1 in a billion. **They are illustrative, not from casework.**
- **N** lets you type N in.
- **Exact** opens a CAS page:
  - the exact expression, 1 − (999999/1000000)^N;
  - its limit, 1 − e^(−μ) with μ = N × RMP;
  - its series, μ − μ²/2 + μ³/6 − …, which is why P ≈ μ only while μ is small;
  - the half-way database size, ln 2 / RMP (693,147 at 1 in a million).

A cold hit from a big database needs more support than the RMP alone.

## The help pages

1. Zero errors is not a zero rate, with the PCAST citations.
2. Reading the main plot.
3. The rule of three: the limit, and the 4.74 / 6.30 / 7.75 versions for 1–3 errors.
4. Confidence or credibility?: Clopper–Pearson, Bayes, Jeffreys, PCAST's four methods.
5. Simulation: absence of evidence.
6. Database trawls.
7. **Honest caveats**:
   - Proficiency tests are not blind casework. Examiners who know they are being tested do better (PCAST §4.6, pp. 57–58).
   - The bound assumes independent tests of equal difficulty. Easy or similar items make it too optimistic.
   - Count only conclusive answers (PCAST p. 51).
   - It describes this examiner on these tests, not a discipline and not one case.
   - A false-positive rate needs different-source tests; a miss rate needs same-source ones.
   - One-sided 95 % is the top of a two-sided **90 %** interval.
8. Keys and touch.
9. Three engines.

## Three engines: who does what

| Engine | Its job here | If it fails |
|---|---|---|
| **PPL** | draws every screen, reads every touch, computes every number that is drawn (the bound, the curves, the posterior, the trawl) | — |
| **CAS** | exact text: the fraction 1/20, the closed form 1 − (1/20)^(1/30), the limit ln(20), exact polynomials, the Poisson limit, the Bayes fraction 1/32, the trawl's expression, limit and series | the page shows the same formula with PPL's decimals and says "decimal" |
| **MicroPython** | 10,000 simulated proficiency programmes | PPL simulates 1,000 and the badge says "PPL fallback" |

The CAS is asked only when a page opens or n changes, never during a drag, and its answers are cached. **Eng** (page 2) checks both engines live: `1/2+1/3` must come back as `5/6`, and Python must answer a 50-programme run. It also names which engine produced the last result.

## Home exports

After you quit:

| Variable | Contents |
|---|---|
| `ER_UPPER` | the upper bound |
| `ER_N`, `ER_K`, `ER_ALPHA` | the record |
| `ER_RATE`, `ER_PASS` | the last true rate, and the chance of the record at that rate |
| `ER_RULE` | the rule line (3/n) |
| `ER_BMEAN`, `ER_BUPPER` | the posterior mean and credible bound |
| `ER_SIM` | the simulated share of records at least this good |
| `ER_TRAWL` | the last trawl probability |
| `ER_PY…` | the MicroPython bridge. `ER_PYZ` shows how far the script got: 1 read its inputs, 2 simulated, 3 wrote back |

## Classroom suggestions

1. **Before the program:** "An examiner passed 30 proficiency tests with no errors. What is the error rate?" Collect answers; many will say 0. Then open the program and drag the rate to 5 %: 21.5 %.
2. **Drag n** from 5 to 1000 and watch n × bound climb from 2.25 toward 3. The rule of three is where it is heading, not where it is.
3. **Set k = 1 or 2:** one error makes the bound much larger than one more test would shrink it. Compare 0 of 30 (9.5 %), 1 of 30 (14.9 %) and 2 of 30 (19.5 %).
4. **Sim** at the bound itself (9.5 %): about 5 % of examiners still finish 30 tests clean. That is what "95 % one-sided" means.
5. **Bayes** with a sceptical prior Beta(1, 19), and again with the uniform prior. How much does the prior matter at n = 30? At n = 300?
6. **Trawl:** at 1 in a million, a database of a million profiles is expected to give one chance match. How should a cold hit be presented?

## Credit

Concept, direction, classroom judgement and all hardware testing: Roger Metcalf.

Implementation, the numerics and their verification against SciPy, statsmodels, SymPy and desktop Giac, and this guide: Claude (Anthropic). The numerics are the bisected Clopper–Pearson bound, the Poisson rule constants, the Beta functions through `FISHER_CDF`, the geometric-gap simulation in MicroPython and PPL, the trawl series, and the CAS templates.

The touch and drawing idioms are the house kit (ChiTable, CICatcher, TouchKit v2). The Python bridge is GaltonBoard beta 2's and NormExplorer beta 42's. The CAS call routine is the fleet's BRIEF_CAS kit. The Lanczos log-gamma is Burr3's.

The statistical convention follows PCAST (2016), *Forensic Science in Criminal Courts: Ensuring Scientific Validity of Feature-Comparison Methods*: §4.2 p. 51, §4.6 pp. 57–58, and Appendix A pp. 152–153.

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty. Firmware: not yet run on hardware (written for 2.4.2, 2026-09-09); beta 1a's Why 3 page passed on the HP Prime Virtual Calculator on 17 Oct 2026.*
