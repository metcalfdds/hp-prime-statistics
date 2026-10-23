"""hpstats.py -- the arithmetic of the HP Prime statistics fleet, in plain Python.

One tested copy of what the calculator programs compute: proportions and their intervals,
2 x 2 tables, the chi-square trend test, the DNA mixture probability with theta, the
studentized range, Burr XII, and the chi-square upper tail as a sum of positive terms.
Each function reads like the formula in the textbook and is checked against SciPy and
statsmodels in test_hpstats.py.  Where the calculator program does something a particular
way for a reason (Newcombe's hybrid score interval, Mantel's N - 1 variance, the finite
positive sums), this module does it the same way and the docstring says so.

Needs numpy and scipy.  Free for educational and personal use.
Roger Metcalf, 2026.  Written with AI assistance (Anthropic Claude), 23 October 2026.
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence

import numpy as np
from scipy import integrate, optimize, special, stats

__all__ = [
    'chi2_sf', 'wilson_ci', 'clopper_pearson_ci', 'newcombe_rd_ci', 'binomial_upper_bound',
    'chi_square_2x2', 'fisher_exact', 'odds_ratio_ci', 'risk_ratio_ci', 'conditional_odds_ratio',
    'mcnemar', 'trend_test', 'mixture_probability', 'mixture_lr',
    'studentized_range_cdf', 'studentized_range_crit', 'burr12_pdf', 'burr12_cdf', 'burr12_ppf',
]

_Z = {0.95: 1.959964}


def _z(conf: float) -> float:
    """The two-sided normal quantile for a confidence level, e.g. 1.959964 for 0.95."""
    return _Z.get(conf) or float(stats.norm.ppf(0.5 + conf / 2))


# ----------------------------------------------------------------- chi-square tails

def chi2_sf(x: float, df: int) -> float:
    """P(chi-square(df) > x) as a finite sum of positive terms (TrendTest beta 3f, trUpper).

    1 - CDF is exactly 0 on a 12-digit calculator once the tail is below about 5E-13; these
    closed forms keep every digit.  Even df: e^(-x/2) (1 + h + h^2/2! + ... + h^(m-1)/(m-1)!)
    with h = x/2, m = df/2.  Odd df, m = (df-1)/2: 2 Phi(-sqrt x) + sqrt(2x/pi) e^(-x/2)
    (1 + x/3 + x^2/15 + ...), m terms.  A non-integer df falls back to SciPy's regularized gamma.
    """
    if x <= 0:
        return 1.0
    if df != int(df) or df < 1:
        return float(special.gammaincc(df / 2, x / 2))
    df = int(df)
    h = x / 2
    if df % 2 == 0:
        m = df // 2
        t = math.exp(-h)
        s = t
        for j in range(1, m):
            t *= h / j
            s += t
        return min(1.0, s)
    m = (df - 1) // 2
    s = 2 * stats.norm.cdf(-math.sqrt(x))
    if m >= 1:
        t = math.sqrt(2 * x / math.pi) * math.exp(-h)
        s += t
        for j in range(2, m + 1):
            t *= x / (2 * j - 1)
            s += t
    return min(1.0, float(s))


# ----------------------------------------------------------------- one proportion

def wilson_ci(x: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """Wilson score interval for a proportion x/n (EpiStats es_WilsonCI, ChiTable csWils)."""
    if n == 0:
        return (0.0, 1.0)
    z = _z(conf)
    p = x / n
    q = z * z / n
    centre = (p + q / 2) / (1 + q)
    half = z * math.sqrt(p * (1 - p) / n + q / (4 * n)) / (1 + q)
    return (max(0.0, centre - half), min(1.0, centre + half))


def clopper_pearson_ci(x: int, n: int, conf: float = 0.95, midp: bool = False) -> tuple[float, float]:
    """Exact (Clopper-Pearson) interval for x/n, or the mid-p interval (EpiStats es_CPInt).

    Exact: the lower end is the p at which P(X >= x) = alpha/2, the upper the p at which
    P(X <= x) = alpha/2.  Mid-p: half the probability of x itself is counted on each side.
    """
    a = (1 - conf) / 2
    if n == 0:
        return (0.0, 1.0)
    if not midp:
        lo = float(stats.beta.ppf(a, x, n - x + 1)) if x > 0 else 0.0
        hi = float(stats.beta.ppf(1 - a, x + 1, n - x)) if x < n else 1.0
        return (lo, hi)

    def upper_tail(p):      # P(X > x) + P(X = x)/2 - alpha/2
        return (1 - stats.binom.cdf(x, n, p)) + 0.5 * stats.binom.pmf(x, n, p) - a

    def lower_tail(p):      # P(X < x) + P(X = x)/2 - alpha/2
        return stats.binom.cdf(x - 1, n, p) + 0.5 * stats.binom.pmf(x, n, p) - a

    lo = float(optimize.brentq(upper_tail, 1e-12, 1 - 1e-12)) if x > 0 else 0.0
    hi = float(optimize.brentq(lower_tail, 1e-12, 1 - 1e-12)) if x < n else 1.0
    return (lo, hi)


def binomial_upper_bound(n: int, k: int, alpha: float = 0.05) -> float:
    """The largest error rate consistent with k errors in n trials (ErrorRate erlBound).

    The one-sided exact upper bound: the p at which P(X <= k) = alpha.  With k = 0 it is
    1 - alpha^(1/n), the "rule of three" (about 3/n at alpha = 0.05).
    """
    if k >= n:
        return 1.0
    if k == 0:
        return 1 - alpha ** (1 / n)
    return float(stats.beta.ppf(1 - alpha, k + 1, n - k))


# ----------------------------------------------------------------- two proportions, 2 x 2 tables

def newcombe_rd_ci(a: int, n1: int, c: int, n2: int, conf: float = 0.95) -> tuple[float, float]:
    """Newcombe's hybrid score interval for the risk difference a/n1 - c/n2 (ChiTable beta 3d).

    Each proportion's Wilson limits (l1, u1), (l2, u2) are combined as independent errors:
    lower = rd - sqrt((p1 - l1)^2 + (u2 - p2)^2), upper = rd + sqrt((u1 - p1)^2 + (p2 - l2)^2).
    Never leaves [-1, 1] and never has width 0, which the Wald interval does at small n.
    """
    p1, p2 = a / n1, c / n2
    l1, u1 = wilson_ci(a, n1, conf)
    l2, u2 = wilson_ci(c, n2, conf)
    rd = p1 - p2
    return (rd - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), rd + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def chi_square_2x2(a: int, b: int, c: int, d: int) -> dict:
    """Pearson, Yates and likelihood-ratio chi-square for the table [[a, b], [c, d]] (ChiTable csCompute).

    Returns a dict with x2, p, yates, p_yates, g2, p_g2, phi, cramers_v, expected (2 x 2 list)
    and adjusted (Haberman) residuals.  p-values use chi2_sf, so a tiny p keeps its digits.
    """
    o = np.array([[a, b], [c, d]], dtype=float)
    n = o.sum()
    rt = o.sum(axis=1, keepdims=True)
    ct = o.sum(axis=0, keepdims=True)
    e = rt * ct / n
    x2 = float(((o - e) ** 2 / e).sum())
    yates = float((np.maximum(0, np.abs(o - e) - 0.5) ** 2 / e).sum())
    with np.errstate(divide='ignore', invalid='ignore'):
        g2 = float(2 * np.where(o > 0, o * np.log(o / e), 0).sum())
    adj = (o - e) / np.sqrt(e * (1 - rt / n) * (1 - ct / n))
    phi = (a * d - b * c) / math.sqrt(float(rt[0, 0] * rt[1, 0] * ct[0, 0] * ct[0, 1]))
    return {
        'x2': x2, 'p': chi2_sf(x2, 1), 'yates': yates, 'p_yates': chi2_sf(yates, 1),
        'g2': g2, 'p_g2': chi2_sf(g2, 1), 'phi': phi, 'cramers_v': math.sqrt(x2 / n),
        'expected': e.tolist(), 'adjusted_residuals': adj.tolist(),
    }


def fisher_exact(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact p for [[a, b], [c, d]]: the sum of every table at most as probable
    as the observed one (R's convention; ChiTable csFisher, EpiStats es_FisherExact).

    Table weights are built as ratios from the modal table outward, so nothing overflows.
    """
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2
    lo, hi = max(0, c1 - r2), min(r1, c1)
    mode = min(max((r1 + 1) * (c1 + 1) // (n + 2), lo), hi)
    w = {mode: 1.0}
    for k in range(mode, hi):               # upward
        w[k + 1] = w[k] * (r1 - k) * (c1 - k) / ((k + 1) * (r2 - c1 + k + 1))
    for k in range(mode, lo, -1):           # downward
        w[k - 1] = w[k] * k * (r2 - c1 + k) / ((r1 - k + 1) * (c1 - k + 1))
    total = sum(w.values())
    limit = w[a] * (1 + 1e-7)
    return min(1.0, sum(v for v in w.values() if v <= limit) / total)


def odds_ratio_ci(a: int, b: int, c: int, d: int, conf: float = 0.95) -> tuple[float, float, float]:
    """Sample odds ratio ad/bc with Woolf's log-scale interval.  A zero cell adds 0.5 to every
    cell (Haldane-Anscombe), as the calculator programs do.  Returns (or, lower, upper)."""
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    orr = a * d / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    z = _z(conf)
    return (orr, orr * math.exp(-z * se), orr * math.exp(z * se))


def risk_ratio_ci(a: int, b: int, c: int, d: int, conf: float = 0.95) -> tuple[float, float, float]:
    """Risk ratio (a/(a+b)) / (c/(c+d)) with its log-scale interval; 0.5 added to every cell
    when one is zero.  Returns (rr, lower, upper)."""
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    rr = (a / (a + b)) / (c / (c + d))
    se = math.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
    z = _z(conf)
    return (rr, rr * math.exp(-z * se), rr * math.exp(z * se))


def conditional_odds_ratio(a: int, b: int, c: int, d: int, conf: float = 0.95) -> tuple[float, float, float]:
    """The conditional maximum-likelihood odds ratio and its exact interval (EpiStats es_CondOR).

    With the margins fixed, a follows Fisher's noncentral hypergeometric distribution with
    weights C(r1, a) C(r2, c1 - a) psi^a.  The estimate is the psi at which E[A] equals the
    observed a; the limits are the psi at which P(A >= a) and P(A <= a) equal alpha/2.
    Returns (psi, lower, upper); lower is 0 and upper inf at the ends of the support.
    """
    r1, r2, c1 = a + b, c + d, a + c
    lo, hi = max(0, c1 - r2), min(r1, c1)
    ks = np.arange(lo, hi + 1)
    logw = special.gammaln(r1 + 1) - special.gammaln(ks + 1) - special.gammaln(r1 - ks + 1) \
        + special.gammaln(r2 + 1) - special.gammaln(c1 - ks + 1) - special.gammaln(r2 - c1 + ks + 1)

    def probs(logpsi):
        lp = logw + ks * logpsi
        lp -= lp.max()
        p = np.exp(lp)
        return p / p.sum()

    alpha = (1 - conf) / 2
    lim = 50.0
    mle = 0.0 if a == lo else (math.inf if a == hi else math.exp(
        optimize.brentq(lambda t: float((ks * probs(t)).sum()) - a, -lim, lim)))
    lower = 0.0 if a == lo else math.exp(optimize.brentq(lambda t: float(probs(t)[ks >= a].sum()) - alpha, -lim, lim))
    upper = math.inf if a == hi else math.exp(optimize.brentq(lambda t: float(probs(t)[ks <= a].sum()) - alpha, -lim, lim))
    return (mle, lower, upper)


def mcnemar(b: int, c: int) -> tuple[float, float]:
    """McNemar's test on the discordant cells b and c, with the continuity correction
    (|b - c| - 1)^2 / (b + c), 1 df.  As in R, the correction is not applied when b = c, where
    the statistic is 0 and p = 1.  Returns (statistic, p)."""
    if b + c == 0:
        return (math.nan, math.nan)
    x = 0.0 if b == c else (abs(b - c) - 1) ** 2 / (b + c)
    return (x, chi2_sf(x, 1))


# ----------------------------------------------------------------- the trend test

def trend_test(scores: Sequence[float], cases: Sequence[int], totals: Sequence[int]) -> dict:
    """Chi-square for linear trend in proportions across k ordered groups (TrendTest trCompute).

    The headline statistic is Mantel's (1963) form, whose variance carries an N - 1 and is the
    larger, so the statistic is the smaller; Armitage's form, which R's prop.trend.test and SAS
    print, is Mantel's times N/(N - 1) and is returned as x2_armitage.  Also the Pearson chi-square for the 2 x k table (k - 1 df), the departure from
    linearity (k - 2 df), and the weighted least-squares line through the proportions.
    """
    x = np.asarray(scores, float)
    a = np.asarray(cases, float)
    n = np.asarray(totals, float)
    k = len(x)
    N, A = n.sum(), a.sum()
    sxa, sxn, sxxn = (x * a).sum(), (x * n).sum(), (x * x * n).sum()
    s = sxa - A * sxn / N
    v = A * (N - A) / (N ** 2 * (N - 1)) * (N * sxxn - sxn ** 2)
    x2t = s * s / v
    ea = n * A / N
    x2p = float((((a - ea) ** 2) / ea).sum() + (((n - a) - (n - ea)) ** 2 / (n - ea)).sum())
    x2d = max(0.0, x2p - x2t)
    xbar = sxn / N
    sxx = sxxn - N * xbar ** 2
    slope = s / sxx
    return {
        'x2_trend': float(x2t), 'p_trend': chi2_sf(x2t, 1),
        'x2_armitage': float(x2t * N / (N - 1)), 'p_armitage': chi2_sf(x2t * N / (N - 1), 1),
        'x2_pearson': x2p, 'df_pearson': k - 1, 'p_pearson': chi2_sf(x2p, k - 1),
        'x2_departure': float(x2d), 'df_departure': k - 2,
        'p_departure': chi2_sf(x2d, k - 2) if k > 2 else math.nan,
        'slope': float(slope), 'intercept': float(A / N - slope * xbar),
    }


# ----------------------------------------------------------------- DNA mixtures

def mixture_probability(freqs: Sequence[float], theta: float, unknowns: int,
                        knowns: Iterable[int] = (), typed: Iterable[int | None] = ()) -> float:
    """P(the mixture's alleles at one locus | x unknown contributors, the knowns, theta)
    (DNAMixLR dmProb, NRC II recommendation 4.1 with the Balding-Nichols sampling formula).

    freqs: the population frequencies of the mixture's M alleles, indexed 0 .. M-1.
    unknowns: x, the number of unknown contributors; they bring 2x alleles, every one of which
      must be in the mixture, and together they must cover every mixture allele no known carries.
    knowns: the allele indices carried by the known contributors (a known with an allele outside
      the mixture makes the probability 0; pass None for such an allele).
    typed: the alleles already typed (the knowns' and the suspect's), as indices, or None for an
      allele outside the mixture; they condition the theta correction and count in its denominators.
    Every term is positive: the sum is over the ways the 2x draws are split among the alleles,
    weighted by the sequential sampling products, so nothing cancels.
    """
    f = list(freqs)
    M = len(f)
    knowns = list(knowns)
    typed = list(typed)
    if any(k is None for k in knowns):
        return 0.0
    needed = [1] * M
    for k in knowns:
        needed[k] = 0
    n_needed = sum(needed)
    if n_needed > 2 * unknowns:
        return 0.0
    if unknowns == 0:
        return 1.0
    N = 2 * unknowns
    nT = len(typed)
    t = [0] * M
    for al in typed:
        if al is not None:
            t[al] += 1
    W = [0.0] * (N + 1)
    W[0] = 1.0
    for i in range(M):
        G = [1.0] * (N + 1)                     # g_i(c) / c!
        for c in range(1, N + 1):
            G[c] = G[c - 1] * ((t[i] + c - 1) * theta + (1 - theta) * f[i]) / c
        low = 1 if needed[i] else 0
        V = [0.0] * (N + 1)
        for s_ in range(N + 1):
            if W[s_] > 0 and low <= N - s_:
                for c in range(low, N - s_ + 1):
                    V[s_ + c] += W[s_] * G[c]
        W = V
    total = W[N]
    for j in range(1, N + 1):
        total *= j / (1 + (nT + j - 2) * theta)
    return total


def mixture_lr(freqs: Sequence[float], theta: float, hp: dict, hd: dict) -> float:
    """Likelihood ratio P(E | Hp) / P(E | Hd) for one locus.  hp and hd are dicts with the keys
    unknowns, knowns and typed as for mixture_probability.  Multiply the loci's ratios for the
    profile's LR; a 0 denominator gives inf."""
    num = mixture_probability(freqs, theta, hp['unknowns'], hp.get('knowns', ()), hp.get('typed', ()))
    den = mixture_probability(freqs, theta, hd['unknowns'], hd.get('knowns', ()), hd.get('typed', ()))
    return math.inf if den == 0 else num / den


# ----------------------------------------------------------------- the studentized range

def _range_cdf(r: float, k: int) -> float:
    """P(range of k standard normals <= r) = k * int phi(z) [Phi(z + r) - Phi(z)]^(k-1) dz."""
    if r <= 0:
        return 0.0
    f = lambda z: stats.norm.pdf(z) * (stats.norm.cdf(z + r) - stats.norm.cdf(z)) ** (k - 1)
    v, _ = integrate.quad(f, -12, 12, limit=200)
    return min(1.0, k * v)


def studentized_range_cdf(q: float, k: int, df: float) -> float:
    """P(Q <= q) for the studentized range with k groups and df error degrees of freedom
    (Tukey's q; StudRange sr_SRCDF).  df = inf gives the plain range distribution.

    The outer integral is over s = sqrt(chi-square(df) / df), the density of which narrows as
    1/sqrt(2 df): the integration window follows it, which is the lesson of StudRange beta 15e.
    """
    if q <= 0:
        return 0.0
    if df is None or math.isinf(df):
        return _range_cdf(q, k)
    lc = (1 - df / 2) * math.log(2) + (df / 2) * math.log(df) - special.gammaln(df / 2)

    def dens(s):
        return math.exp(lc + (df - 1) * math.log(s) - df * s * s / 2)

    sig = 1 / math.sqrt(2 * df)
    lo, hi = max(1e-9, 1 - 12 * sig), 1 + 12 * sig
    if df < 100:                       # the density is wide and skewed: use the whole support
        lo, hi = 1e-9, 1 + 12 * sig + 6 / math.sqrt(df)
    v, _ = integrate.quad(lambda s: dens(s) * _range_cdf(q * s, k), lo, hi, limit=200, points=[1.0])
    return min(1.0, v)


def studentized_range_crit(alpha: float, k: int, df: float) -> float:
    """The critical value q such that P(Q > q) = alpha (StudRange sr_SRCrit)."""
    return float(optimize.brentq(lambda q: studentized_range_cdf(q, k, df) - (1 - alpha), 0.3, 120))


# ----------------------------------------------------------------- Burr XII

def burr12_pdf(x: float, c: float, k: float, scale: float = 1.0) -> float:
    """Burr type XII density with shapes c, k and a scale (Burr3 b3_bpdf), computed in logs so
    large shapes do not overflow."""
    if x <= 0:
        return 0.0
    L = c * math.log(x / scale)
    if L > 100:
        return math.exp(math.log(k * c) - math.log(x) - k * L)
    return math.exp(math.log(k * c) - math.log(x) + L - (k + 1) * math.log1p(math.exp(L)))


def burr12_cdf(x: float, c: float, k: float, scale: float = 1.0) -> float:
    """Burr type XII distribution function 1 - (1 + (x/scale)^c)^(-k) (Burr3 b3_bcdf)."""
    if x <= 0:
        return 0.0
    L = c * math.log(x / scale)
    if L > 100:
        return 1 - math.exp(-k * L)
    return 1 - (1 + math.exp(L)) ** (-k)


def burr12_ppf(p: float, c: float, k: float, scale: float = 1.0) -> float:
    """The Burr XII quantile scale * ((1 - p)^(-1/k) - 1)^(1/c)."""
    return scale * ((1 - p) ** (-1 / k) - 1) ** (1 / c)
