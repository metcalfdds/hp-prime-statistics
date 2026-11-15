# A book of tables checked against fresh calculations (15 November 2026)

**The book:** Zwillinger, D., & Kokoska, S. (2000). *CRC standard probability and statistics tables and formulae*. Chapman & Hall/CRC. The copy is the author's own PDF (538 pages). It is a digital PDF, so its text layer is the printed text and no character recognition was needed.

**Why:** Roger, 15 November 2026: "let's please use that book as another arbitrary reference to compare our calculations against--and note if there's an error in a table we're looking at", and later "please check all the tables in the 2000 CRC book that you can", "it would be interesting to see how many miscalculations/misprints are in the book", and "let's develop a distribution to model errors in stats and math books ... what's the 95% CI for number of errors per page?"

## The short answer

- **57 tables on 151 pages were checked: 39,164 printed values.**
- **2,834 values (7.2%) are wrong as printed**, by more than one unit in the last place. Another 2,006 (5.1%) are off by one unit in the last place.
- **22 of the 57 tables (39%) have at least one wrong number or wrong label.** 37 of the 151 pages (25%) have at least one wrong number.
- The wrong numbers are not spread evenly. **Six tables hold 2,598 of the 2,834.** In the other 51 tables the rate is 236 in 30,255, under 1%.
- The worst faults were **made in this book**, not inherited: its 1989 ancestor has the same tables right. At least one misprint from this book is **still in print**: 6336 for 6366 in the F table stands in the 2003 and 2018 editions of the *CRC Standard Mathematical Tables*.
- **Where one of our own routines disagreed with the book, the routine was right every time** (StudRange, RankLab, `hpstats.py`).

## How the check was done

Each table's numbers were read from the text layer and each was worked out afresh:

- distribution functions and quantiles with SciPy;
- rank tests by exact counting (every arrangement, or a recurrence that counts them);
- order statistics, the range, Dixon's ratios, Dunnett's values, tolerance factors and Cochran's test by numerical integration;
- Bartlett's test by inverting a characteristic function, confirmed against a direct integral, the exact two-sample case and simulation;
- simulation only where exact work was out of reach (Spearman at n = 20 and 30, with one and two billion permutations) or as a second opinion (Dixon, Cochran, Bartlett).

A printed value is **right** if it equals the true value rounded to the places printed, **off by one** if it misses by one unit in the last place, and **wrong** otherwise. A table whose label is wrong is counted as its reader would meet it: the label is taken at its word.

Fifteen of the flagged places were also looked at as images of the page. The image agreed with the text layer each time.

## The kinds of error, with examples

A printed number can be off for several different reasons. This book has all of them.

### 1. Misprints: a right number set wrong

| Page | Table | Printed | Should be |
| --- | --- | --- | --- |
| 144 | F, 1%, numerator ∞, denominator 1 | 6336 | 6366 |
| 166 | Student's t, 100 df, α = 0.1 | 0.290 | 1.290 |
| 166 | Student's t, 27 df, last column | 3.69o (a letter o) | 3.690 |
| 357 | Kolmogorov–Smirnov, two samples of 12 and 3 | 36/35 | 36/36 |
| 357 | the same table, two samples of 12 | 96/144 at 5%, 84/144 at 1% | the two exchanged |
| 251 | Dixon's r10, n = 4, 5% | .745 | .765 |
| 376–377 | Spearman, exact tails, n = 6 | 0.5000 three times running | twice; the 18 cells below it are one row low, and the column ends with a probability for S = 72, which cannot occur |
| 112 | Negative binomial, last column | a fifth digit, always 0 (0.04370) | four places (0.0437); the fifth digit is not real |
| 206 | Table 9.1, last row | 1074.6790 and four more values with a fourth decimal of 0 | three decimals; the zero is padding (1074.6794) |
| 373 | Sign test | 0 in 22 cells | no entry: no value satisfies the page's rule there (n = 1 to 7 at 1%, to 6 at 2.5%, to 5 at 5%, to 4 at 10%) |

### 2. Wrong labels: right numbers under the wrong heading

| Page | Table | The fault | Cells wrong as labelled |
| --- | --- | --- | --- |
| 194 | Circular normal probabilities | every row label is one row too low: the row marked d/σ = 0.2 holds the values for 0.1. With the labels moved up one row all 198 cells are exact | 183 of 198 |
| 186 | Tolerance factors | the book defines α by the confidence and P as the share of the population, but the table's "P = .90" is the confidence and its "α = .10, .05, .01, .001" are the shares left out (n = 2: printed 18.800 under α = .05, where the value for 95% confidence is about 32). The 1989 book labels the same numbers γ and 1 − α | 162 of 216 |
| 248 | Cochran's test, second table | headed α = .05; it is the 1% table (headed rightly in 1989) | 221 of 252 |
| 166 | Student's t | the last two columns are headed 0.0025 and 0.001 and hold the values for 0.001 and 0.0005 | 72 of 72 |
| 209 | "z(α/2)/√n" | the numbers are t(α/2, n − 1)/√n: 8.99 at n = 2, where z gives 1.39 | 36 of 36 |
| 385 | Mann–Whitney, 0.10 | the row for 18 is labelled 8 (its numbers are right) | — |
| 77 | Covariances of normal order statistics | the heading says E[X(i)X(j)] is shown; the entries are the covariances (the numbers are right) | — |

### 3. Miscalculations: a number worked out wrong, then printed faithfully

- **2 × 2 contingency tables, pp. 254–267 (14 pages, 5,057 entries).** The text says the small number beside each critical value is the one-tail probability. In every entry it is the probability of that one table alone. So **305 critical values are one too large** (the real tail probability is above the level), **886 probabilities are wrong by more than a unit in the third decimal**, and 807 by one unit. Example: A = 7, B = 7, a = 6 at 5% prints 2 with .049; the tail probability at 2 is .0513, and the right entry is 1 with .015. The book's own example on p. 253 quotes "1.035" for A = 9, B = 6, a = 7; its table prints 1.034. The example is the right one.
- **Studentized range, pp. 87–89.** 505 of 1,463 values are wrong: 231 of 475 at 1%, 252 of 494 at 5%, 22 of 494 at 10%; 203 of them by more than 1% of the value. At 5% and 20 df the book prints 3.60, 3.99, 4.26 for 3.58, 3.96, 4.23. At 1% and 1 df it prints 77.75 for 90.02. Kokoska and Nevison's 1989 table gives 3.578, 3.958, 4.232.

### 4. Old values carried along

- **Dunnett's two-sided comparisons, pp. 297–298.** The book prints the values of Dunnett's 1955 paper. For three or more treatments they are too large: 303 of 384 cells. At 5 df and 5%: 3.39 for 3.29 with three treatments, 4.49 for 3.97 with nine. Dunnett published new tables in 1964 (*Biometrics*, 20, 482–491). The one-sided tables (396 cells) are right.
- **Dixon's ratios, p. 251.** 60 of 272 values are off by more than rounding; with the printed r11 at n = 6 the 0.5% point really cuts off 0.69%. The table is from Dixon (1951), whose errors are documented (McBane, 2006, *Journal of Statistical Software*, 16(3)).
- **Cochran's test, pp. 247–248.** Read at the right levels, 71 of 504 values are off by 2 to 8 units in the fourth decimal, as in the 1947 source.
- **Tolerance factors, p. 186.** The numbers are the Wald–Wolfowitz approximation; 171 of 216 differ from the exact factor (15.978 for 15.512 at n = 2).
- **Control chart factors, p. 392.** D1 and D2 at n = 12, 14, 15 are off by 2 to 4 in the third decimal.

### 5. Single wrong values of unknown cause

| Page | Table | Printed | Should be |
| --- | --- | --- | --- |
| 134 | χ²/df, 500 df, 0.05% and 95% | 0.810, 1.111 | 0.805, 1.106 |
| 245 | Bartlett, 1%, n = 3, k = 3 | .1672 | .1670 |
| 249 | R for the variance test, 150 df, β = 0.5 | 1.297, 1.206 | 1.294, 1.203 |
| 357 | K–S two-sample, 8 and 3, 1% | 24/24 | no entry (the probability of D = 1 is .0121) |
| 357 | K–S two-sample, 9 and 4, 1% | 32/36 | 36/36 |
| 357 | K–S two-sample, 7 and 5, 5% | 30/35 | 28/35 |
| 357 | K–S two-sample, 5 and 5, both levels | no entry | 25/25 (probability .0079) |
| 357 | K–S two-sample, 10 and 9, 1% | 70/90 | 63/90 |
| 375 | Spearman critical values, n = 12 and 13, 0.001 | .8182, .7912 | .8112, .7857 by the rule the table's other exact cells follow |

### 6. Rounding

2,006 values (5.1%) are off by one unit in the last place. The share is highest in tables copied from old sources: 35% in Dixon's, 19% in the order statistics, 18% in Duncan's.

### Slips in the text, seen in passing and not counted

- p. 102: a worked sum has 0.656 for 0.0656 (its total is right).
- p. 250: formula (10.11) for r20 has x(2) in the denominator where x(1) belongs.
- p. 246: Cochran's n is called the sample size; the table's n is the degrees of freedom.
- p. 75: the example quotes 1.1630 from the table of order statistics, which prints 1.1629 (1.1630 is right).

## Every table

| Table | Pages | Values read | Off by one in the last place | Wrong by more | What was found |
| --- | --- | ---: | ---: | ---: | --- |
| Expected values of normal order statistics | 75–76 | 399 | 77 | 0 | 77 of 399 cells off by one in the fourth decimal; the example on p.75 quotes 1.1630 where the table prints 1.1629 |
| Variances and covariances of normal order statistics | 77 | 125 | 0 | 0 | The numbers are right; the heading says E[X(i)X(j)] is shown, but the entries are the covariances |
| Probability integral of the range | 79–86 | 2,379 | 1 | 0 | Nothing |
| Studentized range, upper 1%, 5%, 10% points | 87–89 | 1,463 | 198 | 505 | Half the cells at 1% and 5% differ from the true values; Kokoska and Nevison (1989) print the right values |
| Cumulative binomial probabilities | 96–100 | 1,672 | 35 | 0 | Nothing |
| Geometric distribution, probability and cumulative | 102 | 225 | 0 | 0 | The worked example above the table has 0.656 for 0.0656 in a sum |
| Hypergeometric probability and distribution functions | 105–109 | 1,000 | 23 | 0 | Nothing |
| Negative binomial probabilities | 112 | 126 | 1 | 5 | The last column carries a fifth digit, always 0, that is not a real digit: seven cells, five of them wrong as printed |
| Cumulative Poisson probabilities | 114–118 | 989 | 44 | 0 | Nothing |
| Chi-square critical values | 130–133 | 1,304 | 0 | 0 | Nothing |
| Chi-square over degrees of freedom | 134 | 264 | 1 | 2 | 500 df: 0.810 for 0.805 and 1.111 for 1.106 |
| F critical values, six levels | 141–146 | 1,586 | 1 | 1 | 6336 for 6366 (1%, numerator infinity, denominator 1); still printed in the 31st (2003) and 33rd (2018) editions of the CRC Standard Mathematical Tables |
| Student's t critical values | 166 | 252 | 0 | 73 | The last two columns are headed 0.0025 and 0.001 but hold the values for 0.001 and 0.0005 (72 cells); 0.290 for 1.290 at 100 df; "3.69o" at 27 df |
| Normal distribution: f(z), F(z), 1 - F(z) | 176–184 | 2,448 | 132 | 0 | Nothing |
| Table 7.1, critical values of the normal distribution | 184 | 23 | 0 | 0 | Nothing |
| Tolerance factors for normal distributions | 186 | 216 | 1 | 162 | The headings P and alpha are exchanged against the book's own definitions (162 of 216 cells wrong as headed; 1989 has them as gamma and 1 - alpha); the numbers are the Wald-Wolfowitz approximation (171 differ from the exact factors, by 3% at n = 2) |
| Percentage points of the correlation coefficient | 193 | 186 | 0 | 0 | The six cells of the first row, printed in a short form, were checked by hand |
| Circular normal probabilities | 194 | 198 | 12 | 183 | Every row label is one row too low: the row marked 0.2 holds the values for 0.1, and so on; with the labels moved up one row all 198 cells are exact |
| Circular error probabilities | 195 | 150 | 1 | 0 | Nothing |
| Estimators of the mean and of sigma (variances, efficiencies) | 202 | 87 | 0 | 0 | The best-linear-estimate part was not checked |
| Table 9.1, common critical values | 206 | 50 | 4 | 1 | The last row is printed with a fourth decimal that is a padding zero (1074.6790 for 1074.6794) |
| Table of t over root n (p.209) | 209 | 36 | 1 | 36 | The columns are headed z(alpha/2)/sqrt(n); the numbers are t(alpha/2, n-1)/sqrt(n) (8.99 at n = 2, where z gives 1.39) |
| Table 9.6, k1 and k2 for the median interval | 211 | 50 | 0 | 0 | Checked against the formula the book gives |
| Table 9.7, order statistics for the median interval | 212 | 210 | 0 | 0 | Nothing |
| Confidence limits for a Poisson mean | 213 | 204 | 0 | 0 | Nothing |
| Confidence limits of proportions, 95% and 99% | 215–230 | 4,224 | 146 | 0 | Nothing |
| Bartlett's test critical values | 244–245 | 579 | 6 | 1 | .1672 for .1670 (1%, n = 3, k = 3) |
| Cochran's test critical values | 247–248 | 504 | 72 | 254 | The second table is headed alpha = .05 but is the 1% table (headed rightly in 1989), so 221 of its 252 cells are wrong as headed; read at the right level, 71 cells of the two tables are off by 2 or 3 in the fourth decimal, as in the 1947 source |
| Values of R for the variance test | 249 | 152 | 0 | 2 | 150 df, beta = 0.5: 1.297 for 1.294 and 1.206 for 1.203 |
| Dixon's ratios r10, r11, r20 | 251 | 272 | 94 | 60 | Dixon's 1951 tables are known to hold errors (McBane 2006); .745 for .765 (r10, n = 4, 5%) is not among those and looks like a misprint |
| 2 x 2 contingency tables (critical b and its probability) | 254–267 | 6,144 | 807 | 1,191 | The probability printed is that of the single table, not the one-tail probability the text describes: 305 critical values are one too large, 886 probabilities are wrong by more than a unit in the third decimal and 807 by one unit; the example on p.253 quotes 1.035 where the table prints 1.034 |
| Orthogonal polynomials | 286–288 | 1,052 | 0 | 0 | The blocks for 3, 4 and 5 points were not read |
| Duncan's multiple range test | 294–296 | 1,713 | 300 | 0 | 300 of 1,713 cells off by one in the last place |
| Dunnett's two-sided critical values, 5% and 1% | 297–298 | 384 | 7 | 303 | The 1955 values, too large for three or more treatments (3.39 for 3.29 at 5 df, k = 3); Dunnett gave new two-sided tables in 1964 |
| Dunnett's one-sided critical values, 5% and 1% | 298–299 | 396 | 22 | 0 | Nothing |
| Kendall's rank correlation, distribution of S | 352 | 82 | 0 | 0 | Nothing |
| Kolmogorov-Smirnov one-sample critical values | 355–356 | 200 | 0 | 0 | Nothing |
| Kolmogorov-Smirnov two-sample critical values | 357 | 150 | 0 | 8 | 8 of 150 cells wrong (the two values for 12 and 12 stand in each other's places; 5 and 5 has asterisks where 25/25 belongs); 36/35 for 36/36 |
| Kruskal-Wallis exact probability levels | 359–360 | 108 | 0 | 0 | Nothing |
| Distribution of the total number of runs | 362–371 | 2,178 | 0 | 0 | Nothing |
| Critical values for the sign test | 373 | 200 | 0 | 22 | 22 cells print 0 where no value satisfies the rule the page gives (n = 1 at every level, for instance) |
| Spearman's rank correlation, critical values | 375 | 56 | 0 | 2 | N = 12 and 13 at 0.001 are one step off the rule the other 42 exact cells follow; n = 20 agrees by simulation; two of the four cells for n = 30 are too close to call |
| Spearman's rank correlation, exact tail probabilities | 376–377 | 380 | 0 | 18 | In the n = 6 column 0.5000 stands three times instead of twice and the rest of the column is one row low (18 cells), ending with a probability for S = 72, which cannot occur |
| Wilcoxon signed-ranks critical values | 379 | 114 | 0 | 0 | Nothing |
| Mann-Whitney U, probabilities | 380–384 | 385 | 0 | 0 | 12 cells on p.381, where two blocks stand side by side, were not read |
| Mann-Whitney U, critical values at seven levels | 385–388 | 2,251 | 0 | 0 | In the 0.10 table the row for 18 is labelled 8 (its 19 numbers are right) |
| Factors for control chart lines | 392 | 182 | 19 | 5 | D1 and D2 at n = 12, 14, 15 are off by 2 to 4 in the third decimal (they follow from d3 kept to three places) |
| Permutations | 506 | 133 | 0 | 0 | Nothing |
| Combinations | 507–509 | 764 | 0 | 0 | Nothing |
| Bessel functions J, Y, I, K | 513–515 | 204 | 1 | 0 | Nothing |
| Beta function | 517 | 200 | 0 | 0 | Nothing |
| Factorials, double factorials and their logarithms | 521 | 140 | 0 | 0 | Nothing |
| Gamma function | 524 | 104 | 0 | 0 | Nothing |
| Partitions | 528 | 38 | 0 | 0 | Nothing |
| Stirling numbers of the first kind | 529 | 49 | 0 | 0 | Nothing |
| Stirling numbers of the second kind | 530 | 84 | 0 | 0 | Nothing |
| Sums of powers of integers | 531 | 100 | 0 | 0 | Nothing |
| **All 57 tables** | **151 pages** | **39,164** | **2,006** | **2,834** | |

## Where the errors came from

Other books on the author's drive were opened to see how far back, and how far forward, the errors go.

| Book | What it shows |
| --- | --- |
| *Standard Mathematical Tables*, 13th ed. (Weast, 1964) | Only normal, t, F, binomial and Poisson tables. It is a scan; it was not compared cell by cell. |
| Kokoska & Nevison, *Statistical Tables and Formulae* (Springer, 1989) | The ancestor of the 2000 book. Its studentized range is right, its second Cochran table is headed α = .01, and its tolerance table is labelled γ and 1 − α. Those three faults were made in 2000. |
| *CRC Standard Mathematical Tables and Formulae*, 31st ed. (2003) and 33rd ed. (2018) | Both still print 6336 in the F table. |
| *CRC Handbook of Chemistry and Physics*, 97th ed. | Has t, χ² and F tables; the cells looked at are right. |
| Beyer's *Handbook of Tables for Probability and Statistics* (1968) | Not on the drive; not checked. |

So some errors are old (Dixon 1951, Dunnett 1955, the 1940s approximations), but the largest ones are new. They look like the work of a computer program: one wrong formula spoils 14 pages (the 2 × 2 tables), and one weak numerical method spoils three (the studentized range).

Table makers have always known this. The preface of the 1945 Dover edition of Jahnke and Emde's *Tables of Functions* says that "nearly 400 corrections of errors, and other changes, have been made."

## A model for the errors

**Is there a distribution for the number of errors on a page?** The first thought is Poisson's, the law of rare, independent events. Student used it in 1907 for counts of yeast cells (*Biometrika*, 5(3), 351–360). It does not fit here.

Two counts were made for each of the 151 pages:

- **separate slips**: one cell, one label or one heading set wrong. There are 28, on 17 pages: the misprints, wrong labels and single wrong values listed above, leaving out the sign test's zeros and the faults that run through a whole table;
- **wrong numbers**: every value wrong as printed (2,834).

| Pages with | 0 slips | 1 | 2 | 3 or more |
| --- | ---: | ---: | ---: | ---: |
| Counted | 134 | 12 | 3 | 2 |
| Poisson expects | 125.4 | 23.3 | 2.2 | 0.1 |
| Negative binomial expects | 134.1 | 10.8 | 3.5 | 2.6 |

The variance of the slips is 2.76 times their mean (Poisson says 1; the test gives p below 10⁻²⁵). There are too many clean pages and too many bad ones: **errors come in clumps**, because a table is made in one sitting, from one source or one program. The negative binomial, which allows clumps, fits closely. For the wrong numbers the clumping is far stronger (variance 124 times the mean) and the negative binomial again fits: it expects 112.7, 5.5, 2.9 and 29.8 pages with 0, 1, 2 and 3 or more, against 114, 3, 3 and 31 counted.

**How much can a table be trusted?** For this book:

| Question | Estimate | 95% interval |
| --- | --- | --- |
| Share of tables with a wrong number or label | 22 of 57 = 39% | 27% to 52% |
| Share of pages with a wrong number | 37 of 151 = 25% | 18% to 32% |
| Separate slips per page | 0.19 (one in five pages) | 0.11 to 0.34 |
| Wrong numbers per page | 18.8 | 9.8 to 43 |
| Share of all printed values that are wrong | 7.2% | 2.2% to 12.8% |
| The same, outside the six worst tables | 0.8% | |

The intervals for the two per-page means are from the negative binomial (profile likelihood); the Poisson interval for slips, 0.12 to 0.27, is too narrow because it ignores the clumping. The interval for the share of wrong values resamples whole tables. The two shares of tables and pages use Wilson's interval.

These are figures for one book, as found by the checks made here. Another book would give others.

## Our own arithmetic against the book

| Routine | Table | Cells | Ours rounds to the printed value | Where it does not |
| --- | --- | ---: | ---: | --- |
| StudRange `sr_SRCrit` (PPL, through the PC harness), 3 df and up | Studentized range | 1,349 | 742 | ours equals SciPy to two places in 1,345 of 1,349 (largest difference 0.008%) |
| RankLab `rk_SRNull` | Signed ranks | 114 | 114 | |
| RankLab `rk_KdNull` | Kendall | 82 | 82 | |
| RankLab `rk_MWNull` | Mann–Whitney probabilities and critical values | 2,636 | 2,636 | |
| RankLab `rk_SpPerm` | Spearman exact tails, n = 3 to 7 | 132 | 114 | the 18 cells of the book's faulty n = 6 column |
| `hpstats.clopper_pearson_ci` | Confidence limits of proportions | 4,224 | 4,078 | 146 cells, the number in which the book's last place is off |

The harness is a PC model of the calculator. Nothing here was run on a calculator. The Prime's built-in functions (`STUDENT_ICDF` and the like) were not compared with the book; that would take a run on the Virtual Calculator.

## Not checked

- Tables that cannot be recomputed: block designs (pp. 334–345), sampling plans (p. 395), random digits and normal deviates (pp. 504–505).
- Spearman's critical values above n = 15, except by simulation at 20 (all four agree) and 30 (two agree; two are too close to call with two billion permutations).
- Small parts of tables: best linear estimates (p. 202); the orthogonal-polynomial blocks for 3 to 5 points; 12 Mann–Whitney probabilities on p. 381; Duncan's cells past p = 12 in the rows for 40 df and up; the first column of twelve rows of Dunnett's two-sided 5% table.
- The worked examples and formulas in the text, apart from the four slips listed.
- Kokoska and Nevison (1989) and the 1964 edition beyond the cells named above.
- `hpstats.studentized_range_crit` on the book's grid: it takes over a minute a value on this machine, so the PPL routine was run instead.

## What the book suggests for our programs

Suggestions only; nothing was built.

1. **Dunnett's comparisons with a control**, computed exactly, in AnovaLab. The printed two-sided table is wrong for three or more treatments, so a program that integrates is better than the table.
2. **Page's L test** in RankLab. It is the test in Chapter 9's story. Its exact null distribution is a short convolution; for 3 treatments and 4 blocks the 5% point is 54 (probability .0255), by listing all 1,296 arrangements.
3. **A runs test for randomness** in RankLab. Triola teaches it and the fleet has none.
4. **An outlier test** (Dixon's ratios with exact p-values) in FitCheck.
5. **Tolerance intervals** with exact factors, in CICatcher.
6. **Circular error probability** in BiNorm3D: the chance a shot lands inside a circle.

## Files

Scripts (in `verify/crc2000/tools/`; they read the PDF's text and hold none of it): `crc_lib.py`, `crc_check_v1.py` to `v8.py`, `crc_bartlett_v1.py`, `crc_dunnett2_v1.py`, `crc_finney_v1.py`, `crc_orthpoly_v1.py`, `crc_spearman_v1.py`, `crc_spearman_mc.py`, `crc_ours_v2.py`, `crc_studrange_ours.py`, `crc_summary_v1.py`, `crc_model_v1.py`. To rerun: `pdftotext -layout BOOK.pdf work/all.txt`, then the scripts in that order.
