# hpstats: the fleet's arithmetic in Python

`hpstats.py` is one tested copy of what the HP Prime programs in this repository compute, written as plainly as the formulas in a textbook. It has no screens or menus. It is for three things: an oracle when a program gets a new version (its verify script can import these functions instead of carrying its own copy of the Wilson interval or the Fisher loop); a teaching aid, so a student can see how the calculator got its number; and a citable reference for course materials.

Needs Python 3.9 or later, numpy and scipy. The tests also need statsmodels. Free for educational and personal use.

```python
import hpstats as H

H.wilson_ci(17, 20)                              # (0.6396, 0.9476)
H.clopper_pearson_ci(3, 10, midp=True)
H.fisher_exact(3, 1, 1, 3)                       # 0.4857, the tea table
H.newcombe_rd_ci(5, 5, 0, 5)                     # (0.3855, 1.0)
H.chi_square_2x2(10, 20, 30, 15)['p']
H.conditional_odds_ratio(10, 2, 3, 15)           # (psi, lower, upper), exact
H.mcnemar(5, 10)
H.trend_test([0, 1, 2, 3], [2, 5, 9, 14], [20, 20, 20, 20])['p_trend']
H.mixture_probability([0.1, 0.2, 0.3], theta=0.03, unknowns=1, knowns=[0], typed=[0, 0])
H.studentized_range_crit(0.05, 3, 12)            # 3.7729
H.chi2_sf(237.363, 2)                            # 2.9e-52, where 1 - CDF gives 0
H.burr12_cdf(2, c=1.5, k=0.7, scale=1.2)
```

| Function | What it is | Calculator routine |
| --- | --- | --- |
| `chi2_sf(x, df)` | P(χ² > x) as a finite sum of positive terms | TrendTest `trUpper` |
| `wilson_ci(x, n)` | Wilson score interval | EpiStats `es_WilsonCI`, ChiTable `csWils` |
| `clopper_pearson_ci(x, n, midp=)` | exact or mid-p interval | EpiStats `es_CPInt` |
| `binomial_upper_bound(n, k, alpha)` | one-sided exact bound on an error rate; the rule of three at k = 0 | ErrorRate `erlBound` |
| `newcombe_rd_ci(a, n1, c, n2)` | Newcombe's hybrid score interval for a risk difference | ChiTable beta 3d |
| `chi_square_2x2(a, b, c, d)` | Pearson, Yates, G², φ, V, expected counts, adjusted residuals | ChiTable `csCompute` |
| `fisher_exact(a, b, c, d)` | two-sided exact p, R's convention | ChiTable `csFisher`, EpiStats `es_FisherExact` |
| `odds_ratio_ci`, `risk_ratio_ci` | Woolf intervals, 0.5 added at a zero cell | ChiTable, EpiStats, TrendTest |
| `conditional_odds_ratio(a, b, c, d)` | conditional MLE and exact limits | EpiStats `es_CondOR` |
| `mcnemar(b, c)` | continuity-corrected, R's convention at b = c | EpiStats `es_McNemar` |
| `trend_test(scores, cases, totals)` | Mantel's trend χ² (and Armitage's), Pearson, departure, the fitted line | TrendTest `trCompute` |
| `mixture_probability(freqs, theta, unknowns, knowns, typed)` | NRC II mixture probability with θ, positive terms only | DNAMixLR `dmProb` |
| `mixture_lr(freqs, theta, hp, hd)` | one locus's likelihood ratio | DNAMixLR |
| `studentized_range_cdf`, `studentized_range_crit` | Tukey's q | StudRange `sr_SRCDF`, `sr_SRCrit` |
| `burr12_pdf`, `burr12_cdf`, `burr12_ppf` | Burr type XII | Burr3 |

`python3 test_hpstats.py` runs every function against SciPy, statsmodels or a brute-force enumeration (the mixture probability is checked against every possible allele sequence). The conventions the calculator programs chose are kept and named in the docstrings: Mantel's N − 1 variance for the trend test, no continuity correction in McNemar when b = c, Haldane's 0.5 at a zero cell.
