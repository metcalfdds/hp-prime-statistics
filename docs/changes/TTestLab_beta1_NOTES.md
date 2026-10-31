# TTestLab beta 1: notes

*Beta 1a followed the same evening: each example's source named on screen, for the public repository (`TTestLab_beta1a_CHANGES.md`, 59 checks). Everything below still holds for 1a.*

*31 October 2026, late afternoon. A new program: 1,215 lines (926 of code, 241 of comments). Harness only; nothing has run on a calculator yet.*

## Why

Roger attached his lecture note, *Hypothesis Testing: t-Test (with two population means)*, and asked: "I also would like to be sure we can do these sorts of analyses...." The fleet had no program that works a t test the way the lecture does.

- **His choice:** a new program, TTestLab.
- **His addition:** "and t tests with any combination of equal or unequal variances and equal or unequal n".

## What it does

**1. Which t test? (Figure 11.2)**
- The lecture's two questions as a tappable flowchart: are the samples independent? are the population variances equal?
- The answers lead to the pooled-variances, separate-variances or dependent-samples t.
- Tap the Yes and No boxes, or use the soft keys Yes, No, Back and OK.
- A hint under the chart: equal variances come from the problem, or from Levene's test on the raw scores (SPSS).

**2. The numbers**
- **Independent samples:** each group's mean, SD and N in a form ("Mean 1:", "SD 1:", "N 1:" …), or the raw scores in D1 and D2 (Statistics 1Var).
- **Dependent samples:** the pairs in D1 and D2, or the mean and SD of the differences and the number of pairs.
- **Tails:** two-tailed, or one-tailed either way.
- **α:** the t table's columns (.20 … .001 two-tailed; .10 … .0005 one-tailed).
- **Any mix** of equal or unequal SD and equal or unequal N.

**3. The five steps, a screen each** (soft keys 1-5, ← →; Enter or Menu for the menu; Esc quits)
1. **The hypotheses, and the data:** Table 11.1's layout with the groups' names, or Table 11.3's pairs.
2. **The distribution and df:**
   - pooled N₁ + N₂ − 2;
   - separate: the Welch–Satterthwaite df, worked with a and b;
   - dependent: N pairs − 1.
3. **The critical value and the decision rule:**
   - the printed table's row (df 73 → row 60, as the lecture says) and the exact value for the df;
   - the rule in words;
   - a t curve with the rejection region shaded red and t critical dashed.
4. **The standard error and t obtained, with the numbers put in:**
   - 4 significant digits all the way through;
   - for pairs, Table 11.4's columns (xD, xD − x̄D, its square, their sum).
5. **The decision and the conclusion:**
   - reject or retain, which way the samples differ, in the groups' own names;
   - "Report t(73) = −2.20, p = 0.031, two-tailed";
   - Cohen's d;
   - the curve with t obtained in magenta and the p value's area shaded magenta.

**4. "Pooled or separate?" (menu)**
- Both tests side by side: SE, t, df, t critical, p, decision.
- Then the reason they agree or differ:
  - N₁ = N₂ or s₁ = s₂: the same t, only df differs;
  - the smaller group has the larger SD: the pooled test rejects a true H₀ more often than α says;
  - the larger group has the larger SD: the pooled test is too cautious.
- The lecture's rule, and the case for using the separate test every time (Delacre et al. 2017).

**5. Three examples**
- **Age at arrest** (the lecture; pooled, two-tailed, .05). Exact t = −2.20. Step 4's gray note: the lecture rounds √0.05499 to √.05 and SE to .29, so it prints −2.34.
- **Matched jails** (the lecture; dependent, one-tailed μ₁ < μ₂, .05). Exact t = 1.33. The note: the lecture rounds x̄D to .18 and .38/4 to .10, so it prints 1.29. Step 5: retain, and the samples even differ the other way from H₁.
- **Drug use by sex** (Roger's SPSS output; separate). t = −4.351, df = 265.924, SE .36918, as SPSS printed. Switched to pooled, step 4 says it is SPSS's "Equal variances assumed" row and that its Levene p = .009 points to the other.

## The lecture's numbers

**Its rounding** (Roger: "this instructor is sort of liberal with rounding"):

| | the lecture | exact |
|---|---|---|
| Example 1 SE | √1.74 × √.05 = .29 | √1.7448 × √0.054985 = 0.3097 |
| Example 1 t | −.68/.29 = −2.34 | −2.20 |
| Example 2 sD | √(.38/4) = √.10 = .32 | √(0.37508/4) = 0.3062 |
| Example 2 SE | .32/2.24 = .14 | 0.1369 |
| Example 2 t | .18/.14 = 1.29 | 1.33 |

The decisions at α .05 are the same.

**Its t table (appendix 1).** 193 of its 198 cells equal the exact value rounded to 3 decimals. The other five are all in the last column (one-tailed .0005, two-tailed .001):

| row | printed | exact |
|---|---|---|
| 2 | 31.598 | 31.599 |
| 3 | 12.941 | 12.924 |
| 5 | 6.859 | 6.869 |
| 7 | 5.405 | 5.408 |
| 23 | 3.767 | 3.768 |

TTestLab shows the table's own figure as "the table's" (so it matches what a student reads) and, in those five cells only, step 3 adds "(Row 3 exact: 12.924; lecture's table: 12.941.)".

## The formulas

Group 1 minus group 2, as the lecture and SPSS do.
- **Pooled:** sp = √[((N₁−1)s₁² + (N₂−1)s₂²)/(N₁+N₂−2)], SE = sp √[(N₁+N₂)/(N₁N₂)], df = N₁+N₂−2.
- **Separate:** SE = √(s₁²/N₁ + s₂²/N₂); df = (a+b)²/(a²/(N₁−1) + b²/(N₂−1)), a = s₁²/N₁, b = s₂²/N₂. This is Welch's test, SPSS's "Equal variances not assumed" row. If Roger's textbook gives a different separate-variances df (some older books use N₁ + N₂ − 2, or the smaller N − 1), say so and TTestLab can show it beside Welch's.
- **Dependent:** xD = x₁ − x₂ per pair, sD with N − 1, SE = sD/√N pairs, df = N pairs − 1.
- **t critical:** −STUDENT_ICDF(df, a), a = α (one-tailed) or α/2 (two-tailed); a lower tail, mirrored.
- **p:** lower tails only. Two-tailed MIN(1, 2·STUDENT_CDF(df, −|t|)).
- **Cohen's d:** (x̄₁ − x̄₂)/sp, or x̄D/sD.
- **Scaling:** the SDs are divided by the larger before squaring.

## From the library

The search came after the first draft; Roger asked whether it had been done. It was then run with `libsearch_v1.py` over the index (1,658 Prime programs, the hpcalc.org zips, the Community_Library, the PDFs). The index then dated from 13 Oct, so the current fleet was grepped directly. It was rebuilt at 16:17 the same afternoon (13,093 text files, 1,003 PDFs), and every search was rerun on it. The new hits were the fleet's own files and the TI sweep: a TI-83 `DEGFREED` that gives a "conservative" df (smaller N − 1) beside the formula df, and a matched-pairs program that takes lists or summary numbers. Nothing changed TTestLab. Lessons Learned v7z records the lesson: search first.

**Nothing in the Prime corpus works a t test in steps.** Schrausser's HP_Prime_MATH has three CAS one-liners (one-sample, paired, pooled; no Welch); nothing was taken.

**Taken from the fleet:**
- **PowerViz:** the key and finger drains, the D1/D2 reader, the number formats, the palette.
- **CICatcher (`cqTCrit`):** STUDENT_ICDF tried inside IFERR and checked with STUDENT_CDF, with a bisection fallback. STUDENT_ICDF matched SciPy on the emulator but is not on the device-verified list.
- **AnovaLab:** the two-tailed p capped at 1.
- **RankLab:** the wording of the D1/D2 pairs message.
- **TestChooser:** the Prime's Inference app (Hyp. test, T-Test: μ₁−μ₂, with its Pooled box; pairs: T-Test: 1 μ on the differences). Help page 2 names it as a check.

**Bears on TTestLab but was not changed:** TestChooser's open decision D12, "Welch's t by default". TTestLab follows the lecture (pooled when the variances are equal) and shows both tests on its compare page.

**Also found:** HP's Technology Corner 24 (two-sample t tests on the Prime) in D:\HP-Prime, which says to leave Pooled unchecked. The Prime's user guide does not say which df the unpooled test uses (checklist item 10).

## Verification

`verify_TTestLab_beta1.py`, output `verify_TTestLab_beta1_output.txt`: **57 PASS, 0 FAIL**.

- **A, against SciPy:**
  - pooled and separate SE, t and df in 288 cases (8 N pairs × 6 SD pairs × 3 mean pairs × 2 tests), worst relative difference below 1E-15;
  - SDs of 1E-200 and 1E200;
  - paired t from raw pairs (N 2 to 200, all three tails) and from summary numbers;
  - p in all three tails;
  - t critical for every column, df 1 to 1000 and fractional, 162 values, and the bisection fallback;
  - the table's row rule (17 cases);
  - the lecture's table cell by cell.
- **B:** the three examples, the lecture's rounded paths reproduced, the step-4 notes.
- **C:**
  - every step of every example by soft keys and arrows;
  - step 3's shading, pixel column by column;
  - the flowchart (boxes, soft keys, Back, OK too early, Esc);
  - the forms, D1/D2 for groups and pairs;
  - the refusals: no data, one score, unequal pairs, N < 2, SD < 0, both SDs 0, sD = 0; no box over 5 lines;
  - the menu, including a cancelled switch to dependent samples keeping the old test;
  - help.
- **E:** the compare page for each mix of N and SD, and its claims simulated. With 20,000 pairs of samples each and H₀ true:
  - smaller group with the larger SD (10 at SD 4, 40 at SD 1): pooled rejects 29 %, separate 4.8 %;
  - the reverse: pooled 0.1 %, separate 5.2 %.
- **F:** a finger left on a form's OK is waited out. A copy without the finger drain reopens the menu, as PowerViz v2.5h did on Roger's calculator.
- **G:** no `!=`; 45 routines, all tagged `tt_`; 51 file-level variables, all tagged `tt`; one EXPORT; only verified glyphs (± ² × α μ ₁ ₂ √ ≠, and x̄); every routine defined before use.
- **D:** text_overlap_v1 over 67 distinct screens: no overlap, straddle or overrun, firm or marginal.

## Gate

`ppl_gate_v1c.py TTestLab_beta1.txt`: **RESULT: PASS**.
- The kit lint gives 0 errors and the hard checks find nothing.
- The full parse stops at the first file-level `LOCAL`, the kit's known limit (Lessons Learned §14 rule 14).
- lint_ppl's four "problems" are the version number in the file name.
- The gate's first runs caught `ci` and `si` (the built-ins Ci and Si) and a `\"` the parser rejects; all three are fixed.

## Device checklist (G2 first, then G1)

Load `TTestLab.txt` from `_to_calcs_2026-10-31f_ttestlab` with the Connectivity Kit; run `TTESTLAB` from Home (no parentheses) or the Catalog.

1. **Example: age at arrest.**
   - Step 1: two columns, "Non-Hispanic white" whole.
   - Step 3: "t table, row df = 60: t crit = ±2.000", "exact, df = 73: t crit = ±1.993", red tails beyond the dashed lines.
   - Step 4: "√1.745 × √0.05499 = 1.321 × 0.2345", "= 0.3097", t obt −2.20, and the gray note.
   - Step 5: REJECT, "sample 1 (Hispanic) is lower on average.", "Report t(73) = −2.20, p = 0.031, two-tailed", d −0.51, magenta t obt line and p area.
2. **Example: matched jails.**
   - Step 1: the five pairs.
   - Step 3: "t crit = −2.132", the red tail on the left only.
   - Step 4: the three columns, "sum = 0.3751", sD 0.3062, SE 0.1369, t obt 1.33, the note.
   - Step 5: RETAIN and "The samples even differ the other way from H₁."
3. **Example: drug use by sex.**
   - Step 2: a, b and df 265.92.
   - Step 4: SE 0.3692, t obt −4.35, and SPSS's row quoted.
   - Menu → Pooled or separate?: pooled t −4.524 on 414 df beside separate −4.351.
4. **The flowchart:** tap Yes / No in the boxes and on the soft keys; Back; OK before an answer does nothing; Esc leaves.
5. **A finger on OK:** Menu → Edit the numbers → type the numbers → tap OK and hold a moment. The menu must not open again.
6. **D1 and D2:** a few scores in each (Statistics 1Var), then Choose the test → independent → raw scores; and pairs, the same number in each. Then D2 one shorter: the box says what to do.
7. **Glyphs:** x̄ in "t obt = (x̄₁ − x̄₂)/SE" and "x̄D"; ±, √, ², ×, ≠, μ₁, μ₂, H₀, H₁; the tick labels' minus.
8. **Help:** both pages fit, the Inference app lines on page 2.
9. **Row 3 at α .001 two-tailed** (dependent, typed: mean 1, SD 1, N pairs 4): step 3 reads "±12.941" and "(Row 3 exact: 12.924; lecture's table: 12.941.)", whole.
10. **A check against the Prime itself:** Inference app, Hypothesis test, T-Test: μ₁−μ₂, with Roger's numbers (x̄₁ 4.8185, s₁ 3.28798, n₁ 270; x̄₂ 6.4247, s₂ 3.74872, n₂ 146), Pooled unchecked. Write down the t and the df it shows; TTestLab says −4.351 and 265.92. Then with Pooled checked: −4.524 and 414.
11. **Timing (G1):** how long steps 3 and 5 take to draw (each draws the curve column by column, 297 columns).

## Open

- **The public repository:** does TTestLab go into hp-prime-statistics (27 programs → 28)? If it does, may the drug-use example (Roger's SPSS summary numbers) be public?
- **The separate-variances formulas in Roger's textbook.** The lecture note names the test but does not print its formulas. TTestLab uses Welch's (SPSS's). Some criminal-justice texts may use s²/(N − 1) in the SE and a df with N + 1 and a final − 2 (from memory, not verified: Roger to check his book). If so, TTestLab can show the book's version beside Welch's. AP-style books also use a "conservative" df, the smaller N − 1 (the TI-83 `DEGFREED`).
- **TestChooser:** its t-test cells could point to TTestLab in its next version ("Fleet: TTestLab").
- **The Inference app's unpooled df** (checklist 10).
- **Σ** prints as "sum" until a probe shows it renders.
