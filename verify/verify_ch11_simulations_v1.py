#!/usr/bin/env python3
"""verify_ch11_simulations_v1.py -- the simulations behind four claims in Chapter 11 of Statisticles ("t-Tests: Two Samples").
5 November 2026.  Every number is the share of simulated studies in which a test at alpha = 0.05 said "different".

  A. Levene's test misses unequal spreads: groups of 40 and 20, normal data, one SD 30% larger than the other.
  B. The pooled t-test when the spreads differ: n = 40 and 20, SDs 10 and 20, equal means (a true null).
     The text says about 11% when the SMALLER group has the LARGER SD, and below 2% the other way round.
  C. Levene's test with equal spreads and skewed data: the means version (Levene, 1960; SPSS) against the medians
     version (Brown & Forsythe, 1974; R's car package).  The text says 10% to 19% against 4% to 5%.
  D. The F test of s1^2/s2^2 with equal spreads and skewed data.  The text says 17% to 51%.

Run:  python3 verify_ch11_simulations_v1.py            (about a minute; needs numpy and scipy)
The seed is fixed, so the same numbers come out every time.  Each setting uses REPS simulated studies."""
import numpy as np
from scipy import stats

REPS = 100_000
SEED = 20261105
rng = np.random.default_rng(SEED)
ALPHA = 0.05

def levene_p(a, b, center):
    """Levene's test for two groups, vectorized over rows: a is (REPS, n1), b is (REPS, n2).
    center 'mean' is Levene (1960), as SPSS; 'median' is Brown-Forsythe (1974), as R's car::leveneTest."""
    ca = a.mean(1, keepdims=True) if center == 'mean' else np.median(a, 1, keepdims=True)
    cb = b.mean(1, keepdims=True) if center == 'mean' else np.median(b, 1, keepdims=True)
    za, zb = np.abs(a - ca), np.abs(b - cb)
    n1, n2 = a.shape[1], b.shape[1]; N = n1 + n2
    ma, mb = za.mean(1), zb.mean(1); m = (za.sum(1) + zb.sum(1)) / N
    ssb = n1 * (ma - m) ** 2 + n2 * (mb - m) ** 2
    ssw = ((za - ma[:, None]) ** 2).sum(1) + ((zb - mb[:, None]) ** 2).sum(1)
    F = ssb / (ssw / (N - 2))
    return stats.f.sf(F, 1, N - 2)

def pooled_p(a, b):
    n1, n2 = a.shape[1], b.shape[1]
    sp2 = ((n1 - 1) * a.var(1, ddof=1) + (n2 - 1) * b.var(1, ddof=1)) / (n1 + n2 - 2)
    t = (a.mean(1) - b.mean(1)) / np.sqrt(sp2 * (1 / n1 + 1 / n2))
    return 2 * stats.t.sf(np.abs(t), n1 + n2 - 2)

def welch_p(a, b):
    n1, n2 = a.shape[1], b.shape[1]
    v1, v2 = a.var(1, ddof=1) / n1, b.var(1, ddof=1) / n2
    t = (a.mean(1) - b.mean(1)) / np.sqrt(v1 + v2)
    df = (v1 + v2) ** 2 / (v1 ** 2 / (n1 - 1) + v2 ** 2 / (n2 - 1))
    return 2 * stats.t.sf(np.abs(t), df)

def ftest_p(a, b):
    n1, n2 = a.shape[1], b.shape[1]
    F = a.var(1, ddof=1) / b.var(1, ddof=1)
    lo = stats.f.cdf(F, n1 - 1, n2 - 1)
    return 2 * np.minimum(lo, 1 - lo)

def rate(p): return 100 * np.mean(p < ALPHA)

# skewed populations, each with a known shape; every one is shifted and scaled later only by the same amount in both groups,
# so the two groups always have EQUAL spreads in part C and D
SKEWED = {
    'exponential': lambda size: rng.exponential(1.0, size),
    'chi-square, 3 df': lambda size: rng.chisquare(3, size),
    'lognormal, sigma 0.5': lambda size: rng.lognormal(0, 0.5, size),
    'lognormal, sigma 1': lambda size: rng.lognormal(0, 1.0, size),
}
SIZES = [(20, 20), (40, 20), (40, 40)]

print(f'Chapter 11 simulations: {REPS:,} studies per setting, seed {SEED}, alpha = {ALPHA}\n')

print('A. Levene\'s test, normal data, n = 40 and 20, one SD 1.3 times the other (power: % of studies saying "different")')
for big, label in ((1, 'larger SD in the group of 40'), (2, 'larger SD in the group of 20')):
    s1, s2 = (1.3, 1.0) if big == 1 else (1.0, 1.3)
    a = rng.normal(0, s1, (REPS, 40)); b = rng.normal(0, s2, (REPS, 20))
    print(f'   {label:32s} means version {rate(levene_p(a, b, "mean")):5.1f}%   medians version {rate(levene_p(a, b, "median")):5.1f}%')

print('\nB. Pooled and Welch t-tests, equal means, n = 40 and 20, SDs 10 and 20 (Type I error: should be 5%)')
for label, (s40, s20) in (('smaller group has the larger SD (40: 10, 20: 20)', (10, 20)),
                          ('larger group has the larger SD (40: 20, 20: 10)', (20, 10))):
    a = rng.normal(0, s40, (REPS, 40)); b = rng.normal(0, s20, (REPS, 20))
    print(f'   {label:50s} pooled {rate(pooled_p(a, b)):5.1f}%   Welch {rate(welch_p(a, b)):5.1f}%')

print('\nC and D. Equal spreads, skewed data (Type I error: should be 5%)')
print(f'   {"population":22s} {"n1, n2":8s} {"Levene, means":>14s} {"Levene, medians":>16s} {"F test":>8s}')
allc, allm, allf = [], [], []
for name, draw in SKEWED.items():
    for n1, n2 in SIZES:
        a = draw((REPS, n1)); b = draw((REPS, n2))
        lm, lmd, ft = rate(levene_p(a, b, 'mean')), rate(levene_p(a, b, 'median')), rate(ftest_p(a, b))
        allc.append(lm); allm.append(lmd); allf.append(ft)
        print(f'   {name:22s} {f"{n1}, {n2}":8s} {lm:13.1f}% {lmd:15.1f}% {ft:7.1f}%')
print(f'\n   ranges over the {len(allc)} settings: Levene means {min(allc):.1f}% to {max(allc):.1f}%;'
      f' Levene medians {min(allm):.1f}% to {max(allm):.1f}%; F test {min(allf):.1f}% to {max(allf):.1f}%')
print('\n   for comparison, normal data with equal spreads:')
for n1, n2 in SIZES:
    a = rng.normal(0, 1, (REPS, n1)); b = rng.normal(0, 1, (REPS, n2))
    print(f'   {"normal":22s} {f"{n1}, {n2}":8s} {rate(levene_p(a, b, "mean")):13.1f}% {rate(levene_p(a, b, "median")):15.1f}% {rate(ftest_p(a, b)):7.1f}%')
