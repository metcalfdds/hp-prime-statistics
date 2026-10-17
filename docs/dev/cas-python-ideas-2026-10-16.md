# The CAS and MicroPython in the fleet: ideas, v1

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 16 October 2026.*

Roger asked (16 Oct, 21:07): ways to use the CAS in our programs, and new apps that use both MicroPython and the CAS.

**Short version.**
- The CAS gives a statistics course three things PPL and Python cannot:
  - **exact answers** (fractions, and integers of any size);
  - **the algebra behind a formula**, done live on the student's own numbers;
  - **limits and series**, so a student can watch a distribution turn into another one.
- **Nothing here has run on a calculator.** No program in the fleet calls the CAS yet. The first step is a short probe, CASProbe, like GfxProbe.
- Then a few quick additions to existing programs, and one new app. My pick for the first new app is **ErrorRate Lab**.

---

## 1 · What we know, and what we don't

| | Status | Source |
|---|---|---|
| The Python `cas` module exists, with `caseval`, `eval_expr`, `xcas` and `get_key` | **Present** (`dir()`), never called by us | PyProbe beta 2, emulator, 1 Oct 2026 |
| `cas.caseval("…")` takes a string and returns the CAS result | Documented (HP Help: "Acepta una expresión como una cadena"; `eval_expr` and `xcas` are synonyms) | HP Help (Spanish edition in the library); hp-prime-kit micropython.md |
| `cas.caseval` crashed for one author, who advises avoiding it | Community report, not reproduced | Tetravex `main.py` comments (Technique Catalog v2 §9.5) |
| PPL can call the CAS: `CAS.name(…)`, `CAS("…")`, and `#cas … #end` functions | Documented; 28 corpus programs use `#cas`, 36 use `CAS.` | HP user guide; library index |
| The safe pattern: CAS work in a separate `#CAS` program, called inside `IFERR`, the answer wrapped in `EVAL()`, stale CAS variables purged first, `HSeparator` read | Corpus precedent | Control Systems app (Taveirne, 2021), Technique Catalog v2 §9.1 |
| CAS numerical integration inside ordinary EXPORT functions | Corpus precedent, with one bug | salvomic's Statistic Distributions (§9.3) |
| A CAS exact integer stored from a PPL string, via `CAS.eval("…")` | Corpus precedent | PyReversi (§8.1) |
| Lessons Learned §1: "CAS only for genuinely symbolic work … keep each program on one side of the fence" | **House rule** | LL v7f §1 |

**So what this proposes is a change to the house rule.** The CAS would be allowed inside a fleet program, but only behind the same kind of fence we built for Python:
- in its own tagged routines;
- called only on an event, never once per frame;
- guarded, with a numeric fallback;
- shown with a badge.

---

## 2 · Ground rules (proposed; they become Lessons Learned v7g §1 if the probe passes)

1. **CASProbe first.** No program calls the CAS until the probe has run on the G2 and the G1. Its tests are listed in §6.
2. **The CAS answers events, not frames.** Call the CAS when a tap lands or a finger lifts, cache the answer, and draw from the cache. A drag never calls the CAS. G1 timing for `fsolve`, `int` and `limit` is unknown, and could be seconds.
3. **CAS routines return text, and PPL draws the text.**
   - A tagged `#cas` function, for example `ctFisherExact`, returns `string(…)` of its answer.
   - PPL never stores a CAS object in a Home real, which would turn it into a 12-digit decimal and lose the exactness.
4. **Three guards, as for Python:**
   - clear the CAS variables it uses (`purge`);
   - call it inside `IFERR` and check the result is usable;
   - fall back to the program's existing numeric answer.
   The footer badge reads "exact (CAS)" or "decimal".
5. **Save and restore the CAS settings the routine changes** (exact or approximate, digits), as the Stoichiometry guard does for `HSeparator`.
6. **Names:**
   - CAS functions are tagged like every other routine. We should assume they share the one name pool until the probe says otherwise.
   - Never use a bare `x`, `n`, `p` or `k` as a CAS variable a student could also own. Use tagged names, or `purge` them first.
7. **Python calls `cas.caseval` only if the probe shows it is stable.** Otherwise PPL does the CAS calls and hands the results to Python through `hpprime.eval`, the way the fleet already passes data.

---

## 3 · What the CAS adds, in teaching terms

| CAS power | What a student sees | Example (checked in Python) |
|---|---|---|
| **Exact fractions** | Probabilities as fractions, the way the textbook writes them | 8 Galton rows, bin 4: **35/128**. A test with 95 % sensitivity and specificity at 1 % prevalence: PPV = **95/590 = 19/118 = 0.161** |
| **Huge exact integers** | Combinatorics without overflow | C(100, 50) = **100891344545564193334812497256** (30 digits) |
| **Exact tests** | Fisher's p as a fraction, with no rounding | The lady tasting tea, [[3, 1], [1, 3]]: two-sided **p = 17/35 = 0.4857** |
| **solve / fsolve** | "What value makes this true?" | The prevalence at which PPV = 50 % for a 95 %/95 % test: **5 %** |
| **diff / int** | Where a formula comes from | The delta method: d/dp ln(p/(1−p)) = 1/(p(1−p)), so SE(ln OR) = √(1/a + 1/b + 1/c + 1/d) |
| **limit / series** | One distribution becoming another | n·(1 − 0.05^(1/n)) → −ln 0.05 = **2.996**, the "rule of three". cosh(t/√n)^n → e^(t²/2): the CLT for coin flips |
| **expand (generating functions)** | Exact null distributions built from polynomials | The Mann–Whitney U counts for 6 vs 6 are coefficients of one polynomial and sum to C(12, 6) = **924** |

---

## 4 · Additions to existing programs

Effort is as in the fleet review: S = under an hour of code, M = an afternoon, L = a day or more, all before device testing. All of these wait for CASProbe.

| Program | What the CAS adds | Teaching payoff | Effort |
|---|---|---|---|
| **ChiTable** | **Exact Fisher p as a fraction** on the Fisher plot ("p = 17/35 = 0.4857"), from `comb` with no decimals. Also χ² = N(ad − bc)² / (row and column totals) shown with the student's numbers and simplified to a fraction | Students see that Fisher's test is counting, not approximating | S–M |
| **BayesTree** | **Exact PPV and NPV as fractions** from the natural frequencies (19/118). **"Break-even prevalence":** `solve` for the prior where PPV = 50 % ("this test is wrong more often than right below 5 %"), drawn as a mark on the slider | The base-rate lesson in one number; good for court | S |
| **GaltonBoard** | **Exact bin probability** on the bar tap (35/128 beside 0.2734). A **"Where Poisson comes from"** page: `limit(comb(n,k)(λ/n)^k(1−λ/n)^(n−k), n, ∞)` = λ^k e^(−λ)/k!, as rows grow and p shrinks | The binomial-to-Poisson limit done live, not quoted | S–M |
| **EpiStats** | **Clopper–Pearson exact CI** (and mid-P) for a proportion, using `fsolve` on the exact binomial tail. **Conditional MLE odds ratio** (the one R's `fisher.test` reports), from `fsolve` on the noncentral hypergeometric mean. A **"Where the SE comes from"** page using the delta method with `diff` | Matches what students will see in R and JMP; shows that the √(1/a+…) formula is derived, not magic | M |
| **CICatcher** | **A third proportion interval, "Exact" (Clopper–Pearson)**, beside Wald and Wilson. Its coverage never falls below the nominal level, and the plot shows that conservativeness | Completes the Wald / Wilson / exact comparison every methods text makes | M |
| **CentralLimit** | **The exact curve for a uniform population.** The density of the mean of n uniforms (Irwin–Hall) is computed by the CAS once per n as a piecewise polynomial, cached, and drawn beside the normal curve. Plus an **MGF page**: cosh(t/√n)^n → e^(t²/2) | Shows how fast the CLT really works, with no simulation noise | M |
| **StatDist** | A **"Formula" page** per distribution: the CAS integrates x·f(x) for the mean and confirms the variance; it derives the CDF for the exponential, Weibull and Pareto; hypergeometric probabilities as exact fractions | "Where does E[X] come from?", answered for the distribution on screen | M |
| **PowerViz** | **The closed-form n**, n = ((z₁₋α/₂ + z₁₋β)·σ/δ)², obtained by `solve` from the power equation and shown beside the brute-force n₈₀ | Students see the sample-size formula is just the power curve solved backwards | S |
| **DNAMixLR** | **The LR as a formula** in the allele frequencies and θ (CAS `simplify`), shown on the locus page. **"θ at the ladder edge":** `fsolve` for the θ where log₁₀ LR crosses the next ENFSI band | Turns "a number from a black box" into an expression an expert can explain on the stand | M |
| **TrendTest / ScatterLab** | **The normal equations solved symbolically** for the student's data: ∂SSE/∂a = 0 and ∂SSE/∂b = 0, with the slope as an exact fraction | Least squares as calculus, on the class's own points | S–M |

**Not worth the CAS:** NormExplorer, Norm3, SampDist and StudRange. They already have fast, verified numeric engines, so the CAS would add risk and no lesson. FDAES and TestChooser have no symbolic step. Burr3's moments in Beta functions are possible but minor.

---

## 5 · New apps that use all three: PPL draws, Python crunches, the CAS is exact

Each app below has one showcase gesture, a clear job for each engine, and a criminal-justice or forensic hook.

### 5.1 ErrorRate Lab: "zero errors in 30 tests: how good is the examiner?" (first pick)

- **The lesson:**
  - Zero errors does not mean a zero error rate.
  - The upper 95 % confidence bound is what PCAST (2016) asked forensic disciplines to report from black-box studies.
  - The rule of three, 3/n, is a limit.
- **Showcase gesture:** drag the true error rate along an axis.
  - A curve of P(0 errors in n tests) falls as the rate rises.
  - The α = 0.05 line cuts it at the upper bound, marked in red.
  - Drag n and the bound slides toward 3/n.
- **CAS:**
  - The exact Clopper–Pearson bound: for 0 errors, the closed form 1 − 20^(−1/n) (n = 30 gives 0.0950, against 3/30 = 0.1000); for k errors, `fsolve`.
  - The limit n·(1 − 0.05^(1/n)) → −ln 0.05 = 2.996, shown as the reason for "3".
  - The Bayesian alternative: Beta(a + k, b + n − k) posterior, with its mean as an exact fraction.
- **Python:**
  - Simulates 10,000 proficiency programmes at the dragged true rate, showing how often a fallible examiner still scores 0 for 30. That is "absence of evidence" as a histogram.
  - **Database-trawl page:** P(at least one adventitious match) = 1 − (1 − p)^N for N up to millions, with Monte Carlo beside the exact CAS value.
- **PPL:** the curves, the drag, the posterior plot with a prior slider, soft keys with "More".
- **Why first:** it is the most Roger-specific program possible (ABFO, proficiency testing, PCAST). Every engine has an honest job, and the CAS part is small (closed forms plus one `fsolve`), so it is a good first CAS program. Effort: M–L.

### 5.2 RankLab: exact nonparametric tests for small samples

- **The lesson:** with 6 vs 7 sentences, the t-test's assumptions are shaky. The Mann–Whitney test's exact null distribution comes from counting arrangements.
- **Showcase:** tap the ranks of two groups on a number line (or load an example) and the bars of the exact null distribution of U appear. The observed U is red, its tail is shaded and the normal approximation is overlaid. Drag a point across another and watch U and the exact p jump.
- **CAS:** the generating function. The counts are the coefficients of a q-binomial polynomial, expanded exactly, and the p-value comes out as a fraction. For example, with 6 vs 6 and U = 3, one-sided p = 7/924 = 1/132 = 0.0076, which matches SciPy's exact Mann–Whitney test.
- **Python:** a dynamic-programming count for larger m and n (in seconds), and a 10,000-shuffle permutation test on the raw data for comparison.
- **PPL:** the number line, the bars, the drag.
- Extends to the Wilcoxon signed-rank and sign tests. Effort: M–L.

### 5.3 MLE Lab: where estimators come from

- **The lesson:** the likelihood is a curve. Its peak is the estimate, its slope is the score and its curvature gives the SE.
- **Showcase:** drag θ along the log-likelihood curve. A tangent line rides the finger, with its slope (the score) shown live, and it flattens to zero at the peak. The likelihood-ratio interval is drawn as the band within 1.92 of the top.
- **CAS:**
  - Builds the log-likelihood for the student's data (Poisson arrests per week, exponential time to re-arrest, binomial).
  - Differentiates it, solves score = 0 and prints the estimator ("λ̂ = Σx/n = x̄").
  - Takes −ℓ″ for the SE formula.
- **Python:** simulates 2,000 samples and histograms the λ̂'s against N(λ, SE²), showing why MLEs are approximately normal.
- **PPL:** the curve, the tangent, the drag, the histogram. Effort: L.

### 5.4 MarkovLab: recidivism as a Markov chain

- **The lesson:** with three states (free, probation, prison) and a transition matrix, where does a cohort end up, and how fast?
- **Showcase:** a state diagram with animated tokens flowing along the arrows, beside bars converging to the steady state. Tap an arrow to change its probability; the row total is kept at 1.
- **CAS:** the steady state as exact fractions (solving πP = π) and Pⁿ symbolically.
- **Python:** simulates 1,000 individual life-courses with `urandom` (`linalg` can do the matrix powers too, numerically).
- **PPL:** the diagram, the animation, the bars. The example matrix would be labelled illustrative, not real data. Effort: L.

### 5.5 BenfordLab: first digits and fraud

- **The lesson:** many real-world amounts have leading digit 1 about 30.1 % of the time (log₁₀ 2), and forensic accountants test for that.
- **Showcase:** bars of observed against Benford first digits. Pick a data source (a multiplicative process, uniform amounts, or "invented" numbers) and the bars settle or refuse to. χ² and MAD appear with a verdict band.
- **CAS:** the exact law log₁₀(1 + 1/d), and the second-digit law as a sum.
- **Python:** generates and counts 50,000 numbers in seconds.
- **PPL:** bars and verdict. Effort: M.

---

## 6 · CASProbe beta 1: what it must settle (before any of the above)

It would be one program on the GfxProbe pattern: tests T01–T16, a results pager, a log in a Home variable, and a run on the G2 and the G1.

1. `CAS.comb(100,50)`: what does PPL get back? An exact integer, a decimal, or an error?
2. A `#cas` function that returns `string(comb(100,50))`: does all of the 30-digit text reach `TEXTOUT_P`?
3. `CAS("17/35")` and `string(exact(0.4857142857))`: is a fraction kept as text?
4. `CAS.fsolve` on a binomial tail, `CAS.int` of a normal pdf and `CAS.limit` of n·(1 − 0.05^(1/n)): the values, and **TICKS timing on the G1**.
5. `IFERR` around a CAS call that fails (a division by zero inside `solve`): is it caught, or does it crash?
6. Does a CAS call change the CAS settings or variables? Read before and after, and check `purge`.
7. Do `#cas` function names share the routine-name pool? Two programs, one name.
8. `expand` of a degree-36 q-binomial polynomial, and reading its coefficients back as a list: the size and the time.
9. From Python: `cas.caseval("comb(100,50)")`. What type comes back, a `str` or an `int`? Does it crash (the Tetravex report)? How long does it take?
10. From Python: is `2**100` exact? If MicroPython on the Prime has arbitrary-size integers, Python could do exact counting itself.
11. A CAS result handed from PPL to Python through `hpprime.eval`.
12. Does `HSeparator` change a CAS string, comma against dot?

---

## 7 · Suggested order

1. **CASProbe beta 1** (S–M). Run it after GfxProbe; it is about 10 minutes on each calculator.
2. **Quick wins:** BayesTree break-even prevalence and exact PPV, ChiTable exact Fisher fraction, GaltonBoard exact bin and Poisson limit (S each). Each shows the CAS in one tap with almost no risk.
3. **ErrorRate Lab beta 1** (M–L), the first program written to use all three engines.
4. The EpiStats exact intervals and conditional MLE OR, plus CICatcher's "Exact" interval, which share one Clopper–Pearson routine.
5. RankLab, MLE Lab, MarkovLab and BenfordLab, as Roger chooses.

## 8 · Questions for Roger

1. Is the house-rule change in §2 acceptable: the CAS allowed in fleet programs behind the fence?
2. Is ErrorRate Lab the right first new app, or would RankLab or MLE Lab serve the spring courses better?
3. Which of the §4 additions do you want first?
