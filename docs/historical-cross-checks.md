# Historical Cross-Checks

*Worked examples from Hewlett-Packard's 1970s statistics programs, used as a second check on these programs*

## What this is

Most accuracy claims in this repository were checked against SciPy. Some were also checked against something much older: the worked examples HP printed in the manuals for its statistics programs, written for the HP-41, HP-55, HP-65 and HP-67/97 between 1974 and 1987.

Those manuals are useful test material:

- Each program came with its equations, its references, and a fully worked example: the inputs, the keystrokes, and the number the calculator showed.
- HP's engineers and the modern library worked independently, so where a fifty-year-old answer and SciPy agree, a program that matches both has been checked twice.

StudRange was already checked this way, against Harter's 1960 tables of the studentized range (see the [StudRange guide](studrange-guide.md)). This page adds the cases for NormExplorer and BayesTree. It also adds general reference cases anyone can use to test a program of their own.

**How the numbers were obtained.** Each HP value was transcribed by reading the scanned page, not from OCR. Each was then recomputed exactly in Python (SciPy, and statsmodels for power). The full set of 35 checks passes. Every HP answer agrees with the exact value at the precision HP printed, with one instructive exception, described under NormExplorer.

**Sources.** The scans are from the Museum of HP Calculators documentation collection. The manuals are © Hewlett-Packard. Only numbers and formulas are quoted here, with page references.

**Hardware status.** The values below are expected results, computed off-device. Runs on the G1 and G2 are pending.

---

## NormExplorer: normal and inverse normal

**Source:** *HP-41 Stat Pac*, "Normal and Inverse Normal Distribution", pp. 66–68.

Set μ = 0, σ = 1.

| HP printed | Exact | Where to check | NormExplorer should show |
|---|---|---|---|
| Q(1.18) = 0.12 | 0.119000 | 3 Probability from x → P(X > x) | **0.1190** |
| Q(−2.28) = 0.99 | 0.988696 | same | **0.9887** |
| f(1.18) = 0.20 | 0.198863 | Home: `NORMALD(1.18)` | 0.1989 |
| x for Q = 0.12: **1.18** | **1.174987** | 4 x from probability → Critical value, α = 0.12 | **1.1750** |
| x for Q = 0.95: **−1.65** | **−1.644854** | same, α = 0.95 | **−1.6449** |

**The exception: HP's two inverse answers are off by one in the last digit.** The exact values round to 1.17 and −1.64, but HP printed 1.18 and −1.65. The error is in HP's method, not the transcription. The manual prints the formula it used: Abramowitz & Stegun 26.2.23, a rational approximation accurate to about 4.5×10⁻⁴.

- That formula gives 1.175091 and −1.645211, which round to exactly what HP showed.
- The Prime's `NORMALD_ICDF` has no such error, so **a correct program should not reproduce HP's digits here.**

The forward direction used A&S 26.2.17, which is accurate to 7.5×10⁻⁸. HP's forward answers are fine.

For anyone who wants to show students how a 1979 calculator did this:

```
Q(x), x ≥ 0:  t = 1/(1 + 0.2316419 x)
              Q = f(x)·(b1 t + b2 t² + b3 t³ + b4 t⁴ + b5 t⁵)
              b = 0.319381530, −0.356563782, 1.781477937,
                  −1.821255978, 1.330274429         |error| < 7.5e-8

x(Q), 0 < Q ≤ 0.5:  t = √(−2 ln Q)
              x = t − (c0 + c1 t + c2 t²)/(1 + d1 t + d2 t² + d3 t³)
              c = 2.515517, 0.802853, 0.010328
              d = 1.432788, 0.189269, 0.001308      |error| < 4.5e-4
```

---

## BayesTree: Bayes' formula

**Source:** *HP-55 Statistics Programs*, "Bayes' Formula", pp. 10–11.

HP's example: P[E₁] = 0.95, P[A|E₁] = 0.005, P[E₂] = 0.05, P[A|E₂] = 0.995. HP printed **P[E₁|A] = .09**.

Read it as a screening test:

- E₂ is having the condition, with prevalence 0.05.
- A is a positive result.
- Sensitivity and specificity are both 0.995.
- HP's answer is the chance that a positive is a **false** positive: 1 − PPV.

In BayesTree: Enter values → prior 0.05, sens 0.995, spec 0.995, N 100000.

| Readout | Expected |
|---|---|
| PPV | **0.913** (exact 0.9128; 1 − PPV = 0.0872, HP's .09) |
| NPV | 1.000 (exact 0.99974) |
| LR+ / LR− | 199.000 / 0.005 |
| Tree | D+ 5000 → TP 4975, FN 25; D− 95000 → FP 475, TN 94525 |

A test that is 99.5% sensitive and 99.5% specific, and still one positive in eleven is false. HP picked this example in 1975 for the same reason BayesTree exists.

---

## General reference cases

These come from the same manuals and are verified the same way. They are offered for checking any program that does these calculations.

### Fisher's exact test, 2×2

**Source:** *HP-65 Stat Pac 2*, program Stat 2-24A, pp. 92–94.

HP's table is 7 10 / 8 5. HP's program needed the smallest count top-left, so the example rearranges it to 5 8 / 10 7, then reports one tail.

| Quantity | HP printed | Exact |
|---|---|---|
| Probability of the observed table | 0.16 | 0.161359 |
| Next two more-extreme tables | 0.06, 0.01 | 0.057046, 0.011409 |
| One-tailed p | 0.23 | 0.231069 |
| Two-sided p (sum of tables no more probable than observed) | none | 0.462137 |

- Both column totals are 15, so the distribution is symmetric and the two-sided p is exactly twice the one-tailed.
- Pearson X² = 1.2217 (p = 0.26902).
- Yates X² = 0.5430 (p = 0.46120), close to Fisher's two-sided p, which is what the continuity correction is for.

### Chi-square test of independence, 2×2

**Source:** *HP-67/97 Stat Pac 1*, "Contingency Table", Example 1, pp. 17-04 to 17-05. A poll of 250 men and 250 women on wanting a television set: 80 120 / 170 130.

| Quantity | HP printed | Exact |
|---|---|---|
| Pearson χ² | 13.33 | 13.3333 (p = 0.00026) |
| χ²₀.₉₉ critical value, df 1 | 6.63 | 6.6349 |

Also: Yates χ² = 12.6750 (p = 0.00037), Fisher two-sided p = 0.000359, φ = −0.1633, odds ratio 0.5098.

### Larger tables and goodness of fit

**Source:** *HP-41 Stat Pac*, pp. 56–61.

| Case | HP printed | Exact |
|---|---|---|
| Goodness of fit. O = 8, 50, 47, 56, 5, 14; E = 9.6, 46.75, 51.85, 54.4, 8.25, 9.15 | χ² = 4.84 | 4.8444 |
| 2×3 table: 2 5 4 / 3 8 7 | χ² = 0.02, C = 0.03 | 0.0221, 0.0281 |
| 3×4 table: 36 67 49 58 / 31 60 49 54 / 58 87 80 68 | χ² = 3.36, C = 0.07 | 3.3574, 0.0692 |

C is Pearson's contingency coefficient, √(χ²/(N + χ²)).

### Acceptance sampling (operating characteristic curves)

**Source:** *HP-67/97 Stat Pac 1*, pp. 20-01 to 20-06. The table gives the probability of accepting a lot, by fraction defective p.

| Plan | p → HP (exact) |
|---|---|
| Finite lot (hypergeometric): N 200, n 20, accept on 0 defectives | 0.02 → 0.65 (0.6539); 0.06 → 0.27 (0.2718); 0.10 → 0.11 (0.1085); 0.14 → 0.04 (0.0415) |
| Infinite lot (binomial): n 200, accept on ≤ 1 defective | 0.01 → 0.40 (0.4046); 0.02 → 0.09 (0.0894); 0.04 → 2.656338303×10⁻³ (exact to all ten digits) |

### No shared birthday

**Source:** *HP-55 Statistics Programs*, "Probability of No Repetitions in a Sample", pp. 12–13. The probability that n people, with 365 possible birthdays, share none:

| n | HP printed | Exact |
|---|---|---|
| 4 | .98 | 0.9836 |
| 23 | .49 | 0.4927 |
| 48 | .04 | 0.0394 |

---

## Credit and terms

The idea of checking against HP's historical programs, the source material, and the hardware testing are Roger Metcalf's. Claude did the transcription, the recomputation and this page. The worked examples are Hewlett-Packard's, from the manuals cited above. The normal approximations are from Abramowitz & Stegun, *Handbook of Mathematical Functions* (National Bureau of Standards; the HP-41 manual cites the 1970 printing).

**Free for educational and personal use.** Share it, teach with it, quote it with attribution. Not for sale or commercial redistribution. Provided as is, with no warranty.
