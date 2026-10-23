"""test_hpstats.py -- every function in hpstats against SciPy, statsmodels or brute force.

Run:  python3 test_hpstats.py        (or: pytest test_hpstats.py)
Needs numpy, scipy, statsmodels.
"""
import itertools
import math
import sys

import numpy as np
from scipy import stats
from scipy.special import gammaln
from statsmodels.stats.contingency_tables import mcnemar as sm_mcnemar
from statsmodels.stats.proportion import confint_proportions_2indep, proportion_confint

import hpstats as H


def close(a, b, rel=1e-9, abs_=1e-12):
    return abs(a - b) <= abs_ + rel * abs(b)


def test_chi2_sf():
    for df in range(1, 13):
        for x in [0.5, 2, 5, 10, 20, 40, 60, 100, 200, 400]:
            assert close(H.chi2_sf(x, df), stats.chi2.sf(x, df), 1e-9)
    assert H.chi2_sf(0, 3) == 1 and H.chi2_sf(-1, 2) == 1
    assert close(H.chi2_sf(5, 2.5), stats.chi2.sf(5, 2.5), 1e-12)       # non-integer df via SciPy
    assert H.chi2_sf(237.363, 2) > 1e-60                                 # the tail 1 - CDF loses


def test_wilson_and_clopper_pearson():
    for x, n in [(0, 10), (1, 10), (5, 20), (17, 20), (20, 20), (50, 200), (199, 200), (1, 1000)]:
        wl, wh = proportion_confint(x, n, 0.05, method='wilson')
        lo, hi = H.wilson_ci(x, n)
        assert close(lo, wl, 1e-6) and close(hi, wh, 1e-6)
        bl, bh = proportion_confint(x, n, 0.05, method='beta')
        lo, hi = H.clopper_pearson_ci(x, n)
        assert close(lo, bl, 1e-9) and close(hi, bh, 1e-9)
        lo, hi = H.clopper_pearson_ci(x, n, midp=True)
        if x > 0:
            assert close((1 - stats.binom.cdf(x, n, lo)) + 0.5 * stats.binom.pmf(x, n, lo), 0.025, 1e-7)
        if x < n:
            assert close(stats.binom.cdf(x - 1, n, hi) + 0.5 * stats.binom.pmf(x, n, hi), 0.025, 1e-7)


def test_binomial_upper_bound():
    for n, k, a in [(100, 0, 0.05), (100, 3, 0.05), (50, 2, 0.025), (300, 10, 0.05)]:
        assert close(H.binomial_upper_bound(n, k, a), stats.beta.ppf(1 - a, k + 1, n - k), 1e-9)
    assert close(H.binomial_upper_bound(100, 0, 0.05), 1 - 0.05 ** 0.01, 1e-12)


def test_newcombe():
    for a, n1, c, n2 in [(3, 4, 1, 4), (5, 5, 0, 5), (10, 30, 30, 45), (0, 10, 10, 10), (7, 50, 12, 60)]:
        lo, hi = confint_proportions_2indep(a, n1, c, n2, method='newcomb', compare='diff', alpha=0.05)
        got = H.newcombe_rd_ci(a, n1, c, n2)
        assert close(got[0], lo, 1e-5) and close(got[1], hi, 1e-5)
    assert -1 <= H.newcombe_rd_ci(0, 3, 3, 3)[0] <= 1


def test_chi_square_2x2():
    for a, b, c, d in [(10, 20, 30, 15), (3, 1, 1, 3), (5, 0, 0, 5), (50, 30, 20, 60), (12, 7, 9, 4)]:
        r = H.chi_square_2x2(a, b, c, d)
        x2, p, _, e = stats.chi2_contingency([[a, b], [c, d]], correction=False)
        y2, py, _, _ = stats.chi2_contingency([[a, b], [c, d]], correction=True)
        g2, pg, _, _ = stats.chi2_contingency([[a, b], [c, d]], correction=False, lambda_='log-likelihood')
        assert close(r['x2'], x2) and close(r['p'], p, 1e-9) and close(r['yates'], y2) and close(r['p_yates'], py, 1e-9)
        assert close(r['g2'], g2) and close(r['p_g2'], pg, 1e-9)
        assert np.allclose(r['expected'], e)
        o = np.array([[a, b], [c, d]], float); n = o.sum()
        rt, ct = o.sum(1, keepdims=True), o.sum(0, keepdims=True)
        assert np.allclose(r['adjusted_residuals'], (o - e) / np.sqrt(e * (1 - rt / n) * (1 - ct / n)))
        assert close(r['cramers_v'], math.sqrt(x2 / n))


def test_fisher_exact():
    for t in [(3, 1, 1, 3), (10, 2, 3, 15), (0, 5, 5, 0), (8, 2, 1, 5), (2, 3, 6, 4), (20, 30, 25, 10),
              (1, 0, 0, 1), (0, 0, 3, 4), (5, 5, 5, 5), (100, 50, 40, 110), (0, 10, 10, 0), (7, 0, 3, 9)]:
        assert close(H.fisher_exact(*t), stats.fisher_exact([[t[0], t[1]], [t[2], t[3]]])[1], 1e-7)


def test_odds_and_risk_ratios():
    for a, b, c, d in [(10, 20, 30, 15), (3, 1, 1, 3), (50, 30, 20, 60)]:
        orr, lo, hi = H.odds_ratio_ci(a, b, c, d)
        assert close(orr, a * d / (b * c))
        se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        assert close(lo, orr * math.exp(-1.959964 * se)) and close(hi, orr * math.exp(1.959964 * se))
        rr, lo, hi = H.risk_ratio_ci(a, b, c, d)
        assert close(rr, (a / (a + b)) / (c / (c + d)))
    orr, lo, hi = H.odds_ratio_ci(5, 0, 2, 7)          # Haldane: every cell + 0.5
    assert close(orr, 5.5 * 7.5 / (0.5 * 2.5))


def test_conditional_odds_ratio():
    for t in [(10, 2, 3, 15), (8, 2, 1, 5), (2, 3, 6, 4), (20, 30, 25, 10), (5, 5, 5, 5), (0, 5, 5, 3), (7, 0, 3, 9)]:
        r = stats.contingency.odds_ratio([[t[0], t[1]], [t[2], t[3]]], kind='conditional')
        ci = r.confidence_interval(0.95)
        m, lo, hi = H.conditional_odds_ratio(*t)
        assert close(m, r.statistic, 1e-6) or (math.isinf(m) and math.isinf(r.statistic))
        assert close(lo, ci.low, 1e-6) and (close(hi, ci.high, 1e-6) or (math.isinf(hi) and math.isinf(ci.high)))


def test_mcnemar():
    for b, c in [(5, 10), (10, 5), (0, 8), (25, 40), (200, 0)]:
        r = sm_mcnemar([[0, b], [c, 0]], exact=False, correction=True)
        x, p = H.mcnemar(b, c)
        assert close(x, r.statistic) and close(p, r.pvalue, 1e-7)
    assert H.mcnemar(3, 3) == (0.0, 1.0)                    # R's convention: no correction at b = c
    assert H.mcnemar(200, 0)[1] > 0                          # 5.7E-45, not 0


def test_trend_test():
    for X, A, Nn in [([0, 1, 2, 3], [2, 5, 9, 14], [20] * 4), ([1, 2, 4], [3, 8, 12], [30, 25, 20]),
                     ([0, 1, 2], [5, 95, 5], [100] * 3), ([0, 10, 20, 30, 40], [1, 2, 6, 9, 15], [50] * 5)]:
        r = H.trend_test(X, A, Nn)
        x, a, n = map(np.asarray, (X, A, Nn)); N, At = n.sum(), a.sum()
        s = (x * a).sum() - At * (x * n).sum() / N
        v = At * (N - At) / (N ** 2 * (N - 1)) * (N * (x * x * n).sum() - (x * n).sum() ** 2)
        assert close(r['x2_trend'], s * s / v) and close(r['p_trend'], stats.chi2.sf(s * s / v, 1), 1e-9)
        # Armitage's form is what R's prop.trend.test computes: weighted regression chi-square
        p = a / n; pbar = At / N; xbar = (x * n).sum() / N
        armitage = ((n * (x - xbar) * (p - pbar)).sum()) ** 2 / (pbar * (1 - pbar) * (n * (x - xbar) ** 2).sum())
        assert close(r['x2_armitage'], armitage, 1e-9)
        x2p, pp, _, _ = stats.chi2_contingency([list(A), [m - q for q, m in zip(A, Nn)]], correction=False)
        assert close(r['x2_pearson'], x2p) and close(r['p_pearson'], pp, 1e-9)
        assert r['p_departure'] > 0 or len(X) == 2


def _brute_mixture(freqs, theta, x, knowns, typed):
    M = len(freqs); cats = list(range(M)) + ['other']; pf = list(freqs) + [1 - sum(freqs)]
    U = set(range(M)) - set(knowns); tot = 0.0
    for seq in itertools.product(cats, repeat=2 * x):
        if 'other' in seq or not U <= set(seq):
            continue
        cnt = {}; nT = len(typed); pr = 1.0
        for t in typed:
            cnt[t] = cnt.get(t, 0) + 1
        for s_ in seq:
            pr *= (cnt.get(s_, 0) * theta + (1 - theta) * pf[s_]) / (1 + (nT - 1) * theta)
            cnt[s_] = cnt.get(s_, 0) + 1; nT += 1
        tot += pr
    return tot


def test_mixture_probability():
    cases = [(3, [0.1, 0.2, 0.3], 0.0, 1, [], []), (3, [0.1, 0.2, 0.3], 0.0, 2, [], []),
             (2, [0.15, 0.25], 0.0, 1, [], []), (3, [0.1, 0.2, 0.3], 0.03, 1, [], []),
             (3, [0.1, 0.2, 0.3], 0.03, 2, [], []), (3, [0.1, 0.2, 0.3], 0.03, 1, [0, 1], [0, 1]),
             (4, [0.1, 0.2, 0.3, 0.15], 0.01, 2, [0], [0, 0]), (3, [0.1, 0.2, 0.3], 0.03, 1, [0], [0, 0, 2]),
             (2, [0.3, 0.4], 0.05, 2, [0, 1], [0, 1]), (3, [0.1, 0.2, 0.3], 0.02, 1, [0], [0, 0, None])]
    for M, fq, th, x, kn, ty in cases:
        got = H.mixture_probability(fq, th, x, kn, ty)
        assert close(got, _brute_mixture(fq, th, x, kn, ty), 1e-9), (M, fq, th, x, kn, ty)
    assert H.mixture_probability([0.1, 0.2], 0.0, 1, knowns=[None]) == 0.0
    assert H.mixture_probability([0.1, 0.2], 0.0, 0, knowns=[0, 1]) == 1.0
    assert H.mixture_probability([0.1, 0.2, 0.3], 0.0, 1) == 0.0          # 3 alleles need 2 unknowns
    # the textbook two-person mixture with theta = 0: P = 2 p1 p2 for an unknown with alleles {1, 2}
    assert close(H.mixture_probability([0.1, 0.2], 0.0, 1), 2 * 0.1 * 0.2)
    lr = H.mixture_lr([0.1, 0.2], 0.0, {'unknowns': 0, 'knowns': [0, 1]}, {'unknowns': 1})
    assert close(lr, 1 / (2 * 0.1 * 0.2))


def test_studentized_range():
    for q, k, df in [(3.5, 3, 10), (4.0, 5, 20), (2.5, 2, 5), (5.0, 10, 60), (3.8, 6, 240), (4.5, 8, 1000), (3.0, 4, math.inf)]:
        want = stats.studentized_range.cdf(q, k, 1e9 if math.isinf(df) else df)
        assert close(H.studentized_range_cdf(q, k, df), want, 1e-5), (q, k, df)
    for a, k, df in [(0.05, 3, 10), (0.05, 10, 60), (0.01, 4, 30), (0.05, 6, 90)]:
        assert close(H.studentized_range_crit(a, k, df), stats.studentized_range.ppf(1 - a, k, df), 1e-4)
    assert close(H.studentized_range_crit(0.05, 3, 12), 3.7729, 2e-4)     # Harter's table


def test_burr12():
    for x, c, k, s in [(1, 2, 1, 1), (0.5, 3, 2, 1), (2, 1.5, 0.7, 1.2), (1e5, 2, 3, 1), (50, 4, 2, 0.5)]:
        d = stats.burr12(c, k, scale=s)
        assert close(H.burr12_cdf(x, c, k, s), d.cdf(x), 1e-9) and close(H.burr12_pdf(x, c, k, s), d.pdf(x), 1e-9)
    for p in [0.1, 0.5, 0.9]:
        assert close(H.burr12_ppf(p, 2, 3, 1.5), stats.burr12(2, 3, scale=1.5).ppf(p), 1e-9)


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    failed = 0
    for t in tests:
        try:
            t(); print('ok   ', t.__name__)
        except AssertionError as e:
            failed += 1; print('FAIL ', t.__name__, e)
    print('%d tests, %d failed' % (len(tests), failed))
    sys.exit(1 if failed else 0)
