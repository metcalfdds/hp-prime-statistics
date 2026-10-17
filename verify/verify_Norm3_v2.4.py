#!/usr/bin/env python3
"""verify_Norm3.py -- Norm3 v2.4's numbers against scipy.stats.norm (rewritten 16 Oct 2026).

The v2 checks (kept):
  A. NORMALD(mu,sd,mu) is the closed-form peak 1/(sd*sqrt(2*pi))
  B. the mu +/- 4 sd window covers 99.9937 %
  C. edge/peak density ratio is exp(-8) at every scale
  D. CDF(x0) equals Phi(z) for the z readout
  E. the tick ladder CEILING(xmin/stp)*stp puts every tick inside a negative range
New in v2.4:
  1. the pixel -> x0 map (x = xmin + (px - LFT)/W*(xmax - xmin)) round-trips with the drawing's
     x0 -> px map to within one column, and the snap grid NiceNum(width/100) gives round values
  2. the S-curve inverse: p from a pixel row (0.01 grid, 0.025/0.975 caught) -> NORMALD_ICDF
     equals norm.ppf; every 0.01 and 0.025/0.975 is reachable with H = 153 px
  3. P(X > x0) = 1 - CDF equals norm.sf to the 4 decimals shown
  4. the shifted-cache read used while mu is held: cache(k - m) at the old mu is exactly the pdf
     at column k for mu + m*dx, and the columns read fresh are exactly the |m| uncovered ones
  5. the z-ruler: column of mu + k*sd for k = -3..3 matches the x-axis map
  6. the sigma animation: the four sigma values, the y headroom (a step down peaks at 86 % of
     the held scale, no clipping), and area 1 at every frame (the conservation the picture shows)
Run: python3 verify_Norm3.py    (exit status 0 = all pass)
"""
import math
import sys
import numpy as np
from scipy.stats import norm

LFT, RGT, TOPy, BOT = 24, 302, 37, 190
W, H = RGT - LFT, BOT - TOPy
N = W
n_pass = n_fail = 0


def check(name, ok, detail=''):
    global n_pass, n_fail
    if ok:
        n_pass += 1
    else:
        n_fail += 1
        print('FAIL', name, detail)


def nicenum(v, roundf=1):
    if v <= 0:
        return 1
    e = math.floor(math.log10(v))
    f = v / 10 ** e
    if roundf:
        nf = 1 if f < 1.5 else 2 if f < 3 else 5 if f < 7 else 10
    else:
        nf = 1 if f <= 1 else 2 if f <= 2 else 5 if f <= 5 else 10
    return nf * 10 ** e


cases = [(0, 1), (100, 15), (-12.5, 4), (500, 100), (0.001, 0.0003), (-50, 10)]
for mu, sd in cases:
    # A-D (v2)
    check('A peak %s' % ((mu, sd),), abs(norm.pdf(mu, mu, sd) - 1 / (sd * math.sqrt(2 * math.pi))) < 1e-12 / sd)
    check('B coverage %s' % ((mu, sd),), abs(norm.cdf(mu + 4 * sd, mu, sd) - norm.cdf(mu - 4 * sd, mu, sd) - 0.999936657516) < 1e-10)
    check('C edge ratio %s' % ((mu, sd),), abs(norm.pdf(mu + 4 * sd, mu, sd) / norm.pdf(mu, mu, sd) - math.exp(-8)) < 1e-12)
    for x0 in (mu - 2 * sd, mu, mu + 1.3 * sd):
        check('D CDF=Phi(z) %s' % ((mu, sd, x0),), abs(norm.cdf(x0, mu, sd) - norm.cdf((x0 - mu) / sd)) < 1e-12)
    xmin, xmax = mu - 4 * sd, mu + 4 * sd
    stp = nicenum((xmax - xmin) / 6)
    ticks = [math.ceil(xmin / stp) * stp + i * stp for i in range(20)]
    ticks = [t for t in ticks if t <= xmax + stp / 1000]
    check('E ticks inside %s' % ((mu, sd),), all(xmin <= t <= xmax + stp / 1000 for t in ticks) and len(ticks) >= 4, ticks)

    # 1. pixel <-> x0, and the snap grid
    worst = 0
    for px in range(LFT + 1, RGT + 1):
        x0 = xmin + (px - LFT) / W * (xmax - xmin)          # the touch map
        back = int(LFT + (x0 - xmin) / (xmax - xmin) * W)    # the drawing's IP(...) map
        worst = max(worst, abs(back - px))
    check('1 pixel round trip %s' % ((mu, sd),), worst <= 1, worst)
    g = nicenum((xmax - xmin) / 100)
    m = g / 10 ** math.floor(math.log10(g))
    check('1 snap grid is 1-2-5 %s' % ((mu, sd),), any(abs(m - v) < 1e-9 for v in (1, 2, 5, 10)), g)
    check('1 snap grid 1/200..1/50 of the window %s' % ((mu, sd),), (xmax - xmin) / 200 <= g <= (xmax - xmin) / 50, g)

    # 2. the inverse
    for p in (0.01, 0.025, 0.1, 0.5, 0.9, 0.95, 0.975, 0.99):
        check('2 icdf %s' % ((mu, sd, p),), abs(norm.ppf(p, mu, sd) - (mu + sd * norm.ppf(p))) < 1e-9 * max(1, abs(mu)))

    # 3. the complement, to the 4 decimals shown
    for x0 in (mu - 3 * sd, mu - 0.5 * sd, mu, mu + 1 * sd, mu + 2.7 * sd):
        check('3 sf %s' % ((mu, sd, x0),), '%.4f' % (1 - norm.cdf(x0, mu, sd)) == '%.4f' % norm.sf(x0, mu, sd))

    # 4. the shifted cache
    dx = (xmax - xmin) / N
    cache = [norm.pdf(xmin + k * dx, mu, sd) for k in range(1, N + 1)]
    for msh in (-200, -37, -1, 1, 15, 140, 277):
        mu2 = mu + msh * dx
        err, fresh = 0.0, 0
        for k in range(1, N + 1):
            j = k - msh
            if 1 <= j <= N:
                v = cache[j - 1]
            else:
                v = norm.pdf(xmin + k * dx, mu2, sd)
                fresh += 1
            err = max(err, abs(v - norm.pdf(xmin + k * dx, mu2, sd)) / norm.pdf(mu, mu, sd))
        check('4 shifted cache exact %s' % ((mu, sd, msh),), err < 1e-9, err)
        check('4 fresh columns = |m| %s' % ((mu, sd, msh),), fresh == min(abs(msh), N), fresh)

    # 5. z-ruler columns
    for kz in range(-3, 4):
        col = int(LFT + (mu + kz * sd - xmin) / (xmax - xmin) * W)
        check('5 z column %s' % ((mu, sd, kz),), col == int(LFT + (kz + 4) / 8 * W))

# 2b. reachability of the p grid with H = 153
def snap(p):
    if abs(p - 0.975) < 0.0035:
        return 0.975
    if abs(p - 0.025) < 0.0035:
        return 0.025
    return round(p * 100) / 100


reach = {round(snap((BOT - y) / H), 3) for y in range(TOPy, BOT + 1)}
want = {round(k / 100, 2) for k in range(1, 100)} | {0.025, 0.975}
missing = sorted(want - reach)
check('2b every p 0.01..0.99, 0.025, 0.975 reachable (H=153)', not missing, missing)
# and the old 0.005 grid would have missed some -- the reason for the change
reach005 = {round(round((BOT - y) / H * 200) / 200, 3) for y in range(TOPy, BOT + 1)}
missed005 = sorted({round(k / 200, 3) for k in range(1, 200)} - reach005)
print('a 0.005 grid would miss %d values, e.g. %s' % (len(missed005), missed005[:8]))
check('2c 0.500 is missed by a 0.005 grid (why 0.01 is used)', 0.5 in missed005)

# 6. the sigma animation
A, B = 1.0, 1.25
frames = [B + (A - B) * (n - 2) / 4 for n in (5, 4, 3, 2)]
check('6 sigma frames', np.allclose(frames, [1.0625, 1.125, 1.1875, 1.25]), frames)
A, B = 1.0, 1 / 1.25
held = norm.pdf(0, 0, A) * 1.45
check('6 a step down peaks under the held scale', norm.pdf(0, 0, B) / held < 0.87, norm.pdf(0, 0, B) / held)
print('step down: new peak at %.1f %% of the held y-scale; step up: %.1f %%'
      % (100 * norm.pdf(0, 0, B) / held, 100 * norm.pdf(0, 0, 1.25) / held))
for s in frames + [0.8, 0.85, 0.9, 0.95]:
    area = norm.cdf(4 * 1.0, 0, s) - norm.cdf(-4 * 1.0, 0, s)     # inside the held window
    check('6 area inside the held window ~1 at sigma %.4f' % s, area > 0.9985, area)

print()
print('%d checks passed, %d failed' % (n_pass, n_fail))
sys.exit(1 if n_fail else 0)
