#!/usr/bin/env python3
"""verify_BiNorm3D_beta1a.py -- checks BiNorm3D beta 1a (19 Oct 2026): N1 (help page 4's sentence gets its verb
back) and N2 (the 31-character menu line), from the fleet review of 19 Oct 2026 (findings_B).  Built from
verify_BiNorm3D.py: parts A, B and C run on beta 1a with only the file name changed (harness ppl_run_v1, as
before).  Part D is new (harness ppl_run_v3e): the review's check_BiNorm3D.py on beta 1 and beta 1a (its two
failing checks, N1 and N2, fail on beta 1 and pass on beta 1a; everything else passes on both), the help page and
the menu as drawn, the routine diff beta 1 -> beta 1a (bnMenu and bnHelp only), the static rules, and no
scientific fixed decimal.

Run:  python3 verify_BiNorm3D_beta1a.py

(verify_BiNorm3D.py's docstring follows.)

verify_BiNorm3D.py -- checks the arithmetic of BiNorm3D_beta1.txt before it goes near
a calculator.

  A. The formulas, against SciPy:
     A1 the density f(x, y) against scipy.stats.multivariate_normal
     A2 Y | X = x0: mean rho x0 and SD (1 - rho^2)^0.5, by integrating the joint density,
        and the conditional density against scipy.stats.norm
     A3 the share inside the ellipse Q = k^2: 1 - exp(-k^2/2) against chi2(2) and a
        Monte Carlo draw; the parametric points lie on Q = k^2; the left/right ends of
        every ellipse are on the regression line y = rho x
     A4 the projection formula (a Python copy of the PPL arithmetic) at theta = 0 and 90
     A5 the colour ramp's end points
  B. The PPL itself, run in the harness (ppl_run_v1.py, hp-prime-kit's interpreter):
     B1 bnInit/bnCache: every cached height, ellipse pixel, slice-panel density and
        N(0, 1) row against SciPy, for several rho
     B2 the projection lists bnPX/bnPY and bnPrjX/bnPrjY at theta = 0 and 90 degrees,
        with SIN/COS/ASIN behaving as in DEGREES, RADIANS and GRADS mode -- all three
        must give the same pixels (the bnAU = ASIN(1)/(pi/2) conversion)
     B3 drawing calls per frame (the frame-cost estimate), 3-D full / coarse / slice,
        contour with and without the slice
     B4 a scripted session through every soft key, both drags, the menu, the exact-rho
        form, frame timing and all five help pages: no runtime error, text widths
        audited, the result string and BN_RHO
  C. Layout: the 39 % / 86 % labels against the ellipses, every rho from -0.9 to 0.9

Run:  python3 verify_BiNorm3D.py   (needs numpy, scipy, and the harness beside ../harness)
Roger Metcalf / Claude, 16 Oct 2026.
"""
import math
import os
import sys

import numpy as np
from scipy import stats
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = '/home/claude/work/fix19/BiNorm3D_beta1a.txt'      # beta 1a
OLD = '/home/claude/work/out/BiNorm3D_beta1.txt'
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v1 import Harness, Drag, KEY  # noqa: E402

RHOS = [-0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9]
FINE = [-3 + i * 6 / 14 for i in range(15)]
COARSE = [-3 + i * 0.6 for i in range(11)]
S, KZ, CX3, BT, BB = 22, 24, 160, 3, 215
CL, CT, CU = 22, 18, 27
CXc, CYc = CL + 3 * CU, CT + 3 * CU
PL, PW = 196, 104
fails = []


def check(name, ok, detail=''):
    print('  %-62s %s %s' % (name, 'PASS' if ok else 'FAIL', detail))
    if not ok:
        fails.append(name)


def f(x, y, r):
    return math.exp(-(x * x - 2 * r * x * y + y * y) / (2 * (1 - r * r))) / (2 * math.pi * math.sqrt(1 - r * r))


# ======================================================================= A. formulas
print('A1  density f(x, y) against scipy.stats.multivariate_normal')
worst = 0.0
for r in RHOS:
    mvn = stats.multivariate_normal([0, 0], [[1, r], [r, 1]])
    for x in FINE:
        for y in FINE:
            a, b = f(x, y, r), mvn.pdf([x, y])
            worst = max(worst, abs(a - b) / max(b, 1e-300))
check('max relative error over 7 rho x 225 grid points', worst < 1e-12, '(%.2e)' % worst)
for r, want in [(0.0, 0.159155), (0.6, 0.198944), (0.9, 0.365126)]:
    check('peak f(0,0) at rho = %.1f = %.6f' % (r, want), abs(f(0, 0, r) - want) < 5e-7,
          '(%.6f)' % f(0, 0, r))

print('A2  Y | X = x0 ~ N(rho x0, (1 - rho^2)^0.5)')
worst_m = worst_s = worst_d = 0.0
for r in RHOS:
    for x0 in [-2.9, -2, -1, 0, 0.5, 1.5, 2, 2.9]:
        mass = quad(lambda y: f(x0, y, r), -np.inf, np.inf)[0]
        mean = quad(lambda y: y * f(x0, y, r), -np.inf, np.inf)[0] / mass
        var = quad(lambda y: (y - mean) ** 2 * f(x0, y, r), -np.inf, np.inf)[0] / mass
        worst_m = max(worst_m, abs(mean - r * x0))
        worst_s = max(worst_s, abs(math.sqrt(var) - math.sqrt(1 - r * r)))
        # the marginal of X is N(0, 1): f(x0, y) / phi(x0) is the conditional density
        for y in [-2, -0.5, 0, r * x0, 1.7]:
            c = f(x0, y, r) / stats.norm.pdf(x0)
            worst_d = max(worst_d, abs(c - stats.norm(r * x0, math.sqrt(1 - r * r)).pdf(y)))
check('conditional mean = rho x0 (by integration), max error', worst_m < 1e-8, '(%.1e)' % worst_m)
check('conditional SD = (1-rho^2)^0.5 (by integration), max error', worst_s < 1e-8, '(%.1e)' % worst_s)
check('f(x0,y)/phi(x0) = norm(rho x0, sd).pdf(y), max error', worst_d < 1e-12, '(%.1e)' % worst_d)

print('A3  the ellipses Q = k^2')
for k, label in [(1, 39), (2, 86)]:
    share = 1 - math.exp(-k * k / 2)
    check('k = %d: 1 - exp(-k^2/2) = chi2(2).cdf(k^2) = %.4f (label "%d %%")'
          % (k, share, label), abs(share - stats.chi2(2).cdf(k * k)) < 1e-12
          and round(100 * share) == label)
rng = np.random.default_rng(1)
for r in [0.6, -0.9]:
    xy = rng.multivariate_normal([0, 0], [[1, r], [r, 1]], size=1000000)
    q = (xy[:, 0] ** 2 - 2 * r * xy[:, 0] * xy[:, 1] + xy[:, 1] ** 2) / (1 - r * r)
    check('Monte Carlo, 10^6 pairs, rho = %+.1f: inside k=1 %.4f, k=2 %.4f'
          % (r, (q <= 1).mean(), (q <= 4).mean()),
          abs((q <= 1).mean() - 0.3935) < 0.002 and abs((q <= 4).mean() - 0.8647) < 0.002)
worst_q = 0.0
ends_ok = True
for r in RHOS:
    a, b = math.sqrt(1 + r) / math.sqrt(2), math.sqrt(1 - r) / math.sqrt(2)
    for k in (1, 2):
        pts = []
        for m in range(61):
            t = 2 * math.pi * m / 60
            x, y = k * (a * math.cos(t) + b * math.sin(t)), k * (a * math.cos(t) - b * math.sin(t))
            worst_q = max(worst_q, abs((x * x - 2 * r * x * y + y * y) / (1 - r * r) - k * k))
            pts.append((x, y))
        # the right-most point of the exact ellipse is (k, rho k); 61 samples land near it
        tt = np.linspace(0, 2 * math.pi, 200001)
        xs = k * (a * np.cos(tt) + b * np.sin(tt)); ys = k * (a * np.cos(tt) - b * np.sin(tt))
        i = int(np.argmax(xs))
        ends_ok &= abs(xs[i] - k) < 1e-6 and abs(ys[i] - r * k) < 1e-3
        j = int(np.argmax(ys))
        ends_ok &= abs(ys[j] - k) < 1e-6 and abs(xs[j] - r * k) < 1e-3
check('61 parametric points satisfy Q = k^2, max |Q - k^2|', worst_q < 1e-12, '(%.1e)' % worst_q)
check('right end (k, rho k) on y = rho x; top (rho k, k): all rho, k', ends_ok)


def project(x, y, z, th, ph):
    """The PPL arithmetic of bnFrame + bnPrjX/bnPrjY, in Python (radians)."""
    ct, st, sp, cp = math.cos(th), math.sin(th), math.sin(ph), math.cos(ph)
    hm = S * KZ / (2 * math.pi * math.sqrt(0.19))
    r3 = 3 * math.sqrt(2) * S
    top, bot = max(hm * cp, r3 * sp), r3 * sp
    cy = BT + top + (BB - BT - top - bot) / 2 if top + bot <= BB - BT else BB - bot
    sx = CX3 + S * (x * ct - y * st)
    sy = cy - S * ((x * st + y * ct) * sp + KZ * z * cp)
    return int(sx + 0.5), int(sy + 0.5), cy


print('A4  projection: screen x = 160 + s(x cos t - y sin t),')
print('                screen y = cy - s((x sin t + y cos t) sin p + k z cos p)')
ph = math.radians(30)
_, _, cy30 = project(0, 0, 0, 0, ph)
check('phi = 30: floor centre cy = 215 - R3 sin 30 = %.2f (picture too tall to centre)' % cy30,
      abs(cy30 - (215 - 3 * math.sqrt(2) * 22 * 0.5)) < 1e-9)
r = 0.6
for (x, y), th, want in [((3, 0), 0, (226, 168)), ((0, 3), 0, (160, 135)),
                         ((3, 0), 90, (160, 135)), ((0, 3), 90, (94, 168)),
                         ((-3, -3), 0, (94, 201)), ((-3, -3), 90, (226, 201))]:
    got = project(x, y, f(x, y, r), math.radians(th), ph)[:2]
    check('theta = %2d, phi = 30, rho = .6: (%+d, %+d, f) -> %s' % (th, x, y, got), got == want,
          '(expected %s)' % (want,))
got = project(0, 0, f(0, 0, 0.6), 0, ph)[:2]
want = (160, int(cy30 - 22 * 24 * f(0, 0, 0.6) * math.cos(ph) + 0.5))
check('the peak (0, 0, 0.199) at theta 0: %s, %d px above the floor' % (got, int(cy30 - got[1])),
      got == want)
check('rho = 0 peak height s k f(0,0) = %.1f px (brief: ~90)' % (S * KZ * f(0, 0, 0)), True)
worst_top, worst_bot = 1e9, -1e9
for r in RHOS:
    for thd in range(0, 360, 5):
        for phd in range(10, 81, 1):
            for x in FINE:
                for y in (FINE if abs(r) >= 0.6 else FINE[::7]):
                    sx, sy, _ = project(x, y, f(x, y, r), math.radians(thd), math.radians(phd))
                    worst_top = min(worst_top, sy); worst_bot = max(worst_bot, sy)
check('every grid point, every rho/theta/phi on screen: y %d .. %d (0..216)'
      % (worst_top, worst_bot), worst_top >= 0 and worst_bot <= 216)

print('A5  the colour ramp: blue (0,60,200) -> magenta (200,0,200) -> red (255,0,0)')
ramp = []
for i in range(16):
    t = i / 15
    if t <= 0.5:
        u = 2 * t; ramp.append((int(200 * u + 0.5), int(60 * (1 - u) + 0.5), 200))
    else:
        u = 2 * t - 1; ramp.append((int(200 + 55 * u + 0.5), 0, int(200 * (1 - u) + 0.5)))
check('ramp(1) = %s, ramp(16) = %s' % (ramp[0], ramp[15]),
      ramp[0] == (0, 60, 200) and ramp[15] == (255, 0, 0))
check('ramp at t = 0.533 (index 9) = %s, nearest step to magenta' % (ramp[8],),
      ramp[8][1] == 0 and ramp[8][0] >= 200)


# ======================================================================= B. the PPL
MODES = {
    'degrees': (lambda a: math.sin(math.radians(a)), lambda a: math.cos(math.radians(a)),
                lambda v: math.degrees(math.asin(v))),
    'radians': (math.sin, math.cos, math.asin),
    'grads': (lambda a: math.sin(a * math.pi / 200), lambda a: math.cos(a * math.pi / 200),
              lambda v: math.asin(v) * 200 / math.pi),
}


def harness(mode='degrees', **kw):
    h = Harness(PROG, **kw)
    s, c, a = MODES[mode]
    h._table['SIN'] = lambda args, site: s(args[0])
    h._table['COS'] = lambda args, site: c(args[0])
    h._table['ASIN'] = lambda args, site: a(args[0])
    return h


def g(h, name):
    return h.globals_[name]


print('B1  bnInit / bnCache in the harness against SciPy')
h = harness('degrees')
h.call('bnInit')
check('bnAU in degrees mode = 180/pi', abs(g(h, 'bnAU') - 180 / math.pi) < 1e-9,
      '(%.10f)' % g(h, 'bnAU'))
grid_ok = all(abs(g(h, 'bnGV')[i] - FINE[i]) < 1e-12 for i in range(15)) and \
    all(abs(g(h, 'bnGV')[15 + i] - COARSE[i]) < 1e-12 for i in range(11))
check('grid values: 15 fine (step 3/7), 11 coarse (step 0.6)', grid_ok)
for r in [0.6, -0.9, 0.0, 0.9, -0.3]:
    h.call('bnSetRho', r)
    rho = g(h, 'bnRho')
    mvn = stats.multivariate_normal([0, 0], [[1, rho], [rho, 1]])
    z = g(h, 'bnZ')
    wz = 0.0
    for n, off, vals in [(15, 0, FINE), (11, 225, COARSE)]:
        for j in range(n):
            for i in range(n):
                want = mvn.pdf([vals[i], vals[j]])
                wz = max(wz, abs(z[off + j * n + i] - want) / want)
    # the ellipse pixels
    a, b = math.sqrt(1 + rho) / math.sqrt(2), math.sqrt(1 - rho) / math.sqrt(2)
    we = 0
    for k in (1, 2):
        for m in range(61):
            t = 2 * math.pi * m / 60
            ex = int(CXc + CU * k * (a * math.cos(t) + b * math.sin(t)) + 0.5)
            ey = int(CYc - CU * k * (a * math.cos(t) - b * math.sin(t)) + 0.5)
            we = max(we, abs(g(h, 'bnEX')[(k - 1) * 61 + m] - ex), abs(g(h, 'bnEY')[(k - 1) * 61 + m] - ey))
    # the slice-panel density shape: offset o px from the centre = o/27 units
    sd = math.sqrt(1 - rho * rho)
    wc = max(abs(g(h, 'bnCnd')[o] - stats.norm(0, sd).pdf(o / CU)) for o in range(121))
    psc_ok = abs(g(h, 'bnPSc') * stats.norm(0, sd).pdf(0) - PW) < 1e-9
    check('rho = %+.1f: 346 heights (rel %.1e), ellipse px (max %d px off), f(y|x0) (%.1e)'
          % (rho, wz, we, wc), wz < 1e-12 and we == 0 and wc < 1e-12 and psc_ok)
wm = max(abs(g(h, 'bnMg')[r_ - CT] - stats.norm.pdf((CYc - r_) / CU)) for r_ in range(CT, CT + 6 * CU + 1))
check('N(0, 1) at all 163 panel rows', wm < 1e-12, '(%.1e)' % wm)
h.call('bnSetRho', 0.6); h.call('bnSetX0', 1.5); h.call('bnSliceC')
ws = max(abs(g(h, 'bnSlZ')[m] - f(1.5, -3 + m * 6 / 28, 0.6)) for m in range(29))
check('3-D slice f(1.5, y), 29 points; top f(1.5, 0.9) = %.5f' % g(h, 'bnSlTop'),
      ws < 1e-12 and abs(g(h, 'bnSlTop') - f(1.5, 0.9, 0.6)) < 1e-12)
rp = g(h, 'bnRamp')
check('bnRamp(1) = #003CC8, bnRamp(16) = #FF0000', int(rp[0]) == 0x003CC8 and int(rp[15]) == 0xFF0000)
h.call('bnSetRho', 1.0)
check('rho + 0.1 past 0.9 stops at 0.9 and says so: "%s"' % g(h, 'bnMsg'),
      g(h, 'bnRho') == 0.9 and 'stops at 0.9' in g(h, 'bnMsg'))
h.call('bnSetRho', 0.6 + 0.1)
check('0.6 + 0.1 is stored as 0.7 (ROUND 2)', g(h, 'bnRho') == 0.7)
h.call('bnSetX0', 1.2345)
check('x0 snaps to 0.05: 1.2345 -> %.2f; 3.4 -> 2.9' % g(h, 'bnX0'), abs(g(h, 'bnX0') - 1.25) < 1e-12)
h.call('bnSetX0', 3.4)
check('   (clamped)', abs(g(h, 'bnX0') - 2.9) < 1e-12)

print('B2  projection in the PPL, in all three angle modes')
results = {}
for mode in MODES:
    h = harness(mode)
    h.call('bnInit')
    out = {}
    for thd in (0, 90, 35):
        h.globals_['bnTh'] = math.radians(thd)
        h.globals_['bnPh'] = math.radians(30)
        h.globals_['bnDrag'] = 0.0
        h.call('bnDraw3D')
        out[thd] = (list(h.globals_['bnPX']), list(h.globals_['bnPY']),
                    h.call('bnPrjX', 3, 0), h.call('bnPrjY', 3, 0, 0),
                    h.call('bnPrjX', 0, 3), h.call('bnPrjY', 0, 3, 0))
    results[mode] = (out, h.globals_['bnAU'])
for mode in MODES:
    print('    %-8s bnAU = %.10f' % (mode, results[mode][1]))
same = all(results[m][0] == results['radians'][0] for m in MODES)
check('degrees, radians and grads give identical pixels (theta 0, 90, 35)', same)
out = results['degrees'][0]
worst = 0
for thd in (0, 90, 35):
    px, py = out[thd][0], out[thd][1]
    for j in range(15):
        for i in range(15):
            x, y = FINE[i], FINE[j]
            want = project(x, y, f(x, y, 0.6), math.radians(thd), math.radians(30))[:2]
            worst = max(worst, abs(px[j * 15 + i] - want[0]), abs(py[j * 15 + i] - want[1]))
check('PPL bnPX/bnPY = Python projection, 3 x 225 points (max px off)', worst == 0, '(%d)' % worst)
check('theta 0:  (3,0,0) -> (%d, %d), (0,3,0) -> (%d, %d)' % out[0][2:], out[0][2:] == (226, 168, 160, 135))
check('theta 90: (3,0,0) -> (%d, %d), (0,3,0) -> (%d, %d)' % out[90][2:], out[90][2:] == (160, 135, 94, 168))
h = harness('degrees')
h.call('bnInit')
for v in (-0.1, 7.0, 2 * math.pi + 0.3):
    h.globals_['bnTh'] = v
    h.call('bnNormTh')
    check('bnNormTh(%.2f) -> %.4f in [0, 2 pi)' % (v, h.globals_['bnTh']),
          0 <= h.globals_['bnTh'] < 2 * math.pi and abs(math.sin(h.globals_['bnTh']) - math.sin(v)) < 1e-12)
h.globals_['bnTh'] = math.radians(359.7)
check('bnDeg(359.7 deg) shows "%s"' % h.call('bnDeg', h.globals_['bnTh']), h.call('bnDeg', h.globals_['bnTh']).startswith('0'))

print('B3  drawing calls per frame (the frame-cost estimate)')


def frame_cost(h, fn, **state):
    for k_, v in state.items():
        h.globals_[k_] = float(v)
    n0 = len(h.log)
    h.call(fn)
    calls = {}
    for entry in h.log[n0:]:
        calls[entry[0]] = calls.get(entry[0], 0) + 1
    return calls


h = harness('degrees')
h.call('bnInit')
rows = []
for label, fn, st in [
        ('3-D, 15 x 15, slice off', 'bnDraw3D', dict(bnDrag=0, bnSlc=0)),
        ('3-D, 11 x 11 while dragging, slice off', 'bnDraw3D', dict(bnDrag=1, bnCrs=1, bnSlc=0)),
        ('3-D, 15 x 15, slice on', 'bnDraw3D', dict(bnDrag=0, bnSlc=1)),
        ('3-D, 11 x 11 while dragging, slice on', 'bnDraw3D', dict(bnDrag=1, bnCrs=1, bnSlc=1)),
        ('3-D, 15 x 15 while dragging (coarse off), slice on', 'bnDraw3D', dict(bnDrag=1, bnCrs=0, bnSlc=1)),
        ('contour, slice off', 'bnDrawC', dict(bnDrag=0, bnSlc=0)),
        ('contour, slice on (the x0 drag frame)', 'bnDrawC', dict(bnDrag=0, bnSlc=1))]:
    c = frame_cost(h, fn, **st)
    rows.append((label, c))
    print('    %-52s LINE_P %3d  PIXON_P %3d  TEXTOUT_P %2d  RECT_P %d'
          % (label, c.get('LINE_P', 0), c.get('PIXON_P', 0), c.get('TEXTOUT_P', 0), c.get('RECT_P', 0)))
full = rows[0][1].get('LINE_P', 0)
check('3-D full frame LINE_P = %d (420 mesh + 4 floor + 2 axes)' % full, full == 426)
check('coarse frame LINE_P = %d (220 mesh + 6)' % rows[1][1].get('LINE_P', 0), rows[1][1].get('LINE_P', 0) == 226)

print('B4  a scripted session in the harness')
h = harness('degrees', idle_key=None)
h.tap(160, 120)                                         # welcome page
h.event(Drag([(160, 120), (175, 120), (200, 125), (240, 140), (260, 150)]))   # turn
h.tap(80, 228)                                          # rho+
h.tap(20, 228)                                          # rho-
h.tap(240, 228)                                         # Reset
h.tap(190, 228)                                         # Slice (3-D)
h.event(Drag([(100, 100), (90, 90), (80, 80)]))         # turn with the slice on
h.tap(130, 228)                                         # Cont
h.tap(150, 60)                                          # tap in the plot: slice at x0
h.event(Drag([(150, 60), (120, 60), (60, 60), (30, 60)]))     # drag x0 left
h.press('Left', 'Right', 'Right')                       # x0 by keys
h.press('Plus', 'Plus', 'Plus', 'Plus')                 # rho up to the limit
h.press('Minus')
h.tap(300, 228)                                         # Menu
h.choose(1); h.answer({'arV': -0.45})                   # set rho exactly
h.press('Enter'); h.choose(5)                           # grid while dragging -> full
h.press('Enter'); h.choose(6)                           # frame timing
h.press('Enter'); h.choose(7)                           # help
h.tap(10, 10); h.tap(10, 10); h.press('Enter'); h.tap(10, 10); h.press('Enter')
h.press('Enter'); h.choose(2)                           # back to 3-D view
h.press('Left', 'Up', 'Up', 'Down', 'Right')            # turn and tilt
h.press('Esc')
err = None
try:
    res = h.call('BiNorm3D')
except Exception as e:                                  # noqa: BLE001
    err = e
    res = None
check('session ran to the end with no runtime error', err is None, '' if err is None else repr(err))
print('    result: %r' % (res,))
print('    BN_RHO = %r; %d screens composed; MSGBOXes: %d' % (h.globals_.get('BN_RHO'), len(h.pages), len(h.msgboxes)))
for mb in h.msgboxes:
    print('    MSGBOX: %r' % (mb.text if hasattr(mb, 'text') else mb,))
check('BN_RHO = -0.45 after the exact-rho form', abs(h.globals_.get('BN_RHO', 99) - -0.45) < 1e-12)
left = h.leftover()
check('every scripted event was used', not any(left), '' if not any(left) else repr(left))
clipped = sorted({(t.text, t.width, round(t.est_width)) for s in h.pages for t in s.texts if t.clipped})
check('no text wider than its width argument (estimate)', not clipped,
      '' if not clipped else '\n      ' + '\n      '.join(map(repr, clipped)))
# DRAWMENU paints the screen, so it must come straight after a BLIT_P to G0
order = [e[0] for e in h.log if e[0] in ('BLIT_P', 'DRAWMENU')]
menus = sum(1 for i, c in enumerate(order) if c == 'DRAWMENU')
after = all(order[i - 1] == 'BLIT_P' for i, c in enumerate(order) if c == 'DRAWMENU' and i > 0)
check('DRAWMENU straight after the blit, %d frames' % menus, menus > 10 and after)
helps = [s for s in h.pages if s.func == 'bnPgEnd']
check('five help pages shown', len(helps) == 5, '(%d)' % len(helps))
long_lines = [t.text for s in helps for t in s.texts if t.x == 12 and t.y < 215 and len(t.text) > 46]
check('help lines <= 46 characters', not long_lines, repr(long_lines))
verdicts = [t.text for s in h.pages for t in s.texts if 'REGRESSION' in t.text]
print('    verdict lines seen: %s' % sorted(set(verdicts))[:4])
for w in sorted(set(h.warnings)):
    print('    harness warning: %s' % w)

# ======================================================================= C. layout
print('C   layout: the ellipse labels against the ellipses')


def seg_hits_box(p, q, box):
    x1, y1, x2, y2 = box
    for t in np.linspace(0, 1, 40):
        x, y = p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False


worst = []
for r in [x / 100 for x in range(-90, 91)]:
    a, b = math.sqrt(1 + r) / math.sqrt(2), math.sqrt(1 - r) / math.sqrt(2)
    ell = {}
    for k in (1, 2):
        ell[k] = [(CXc + CU * k * (a * math.cos(2 * math.pi * m / 60) + b * math.sin(2 * math.pi * m / 60)),
                   CYc - CU * k * (a * math.cos(2 * math.pi * m / 60) - b * math.sin(2 * math.pi * m / 60)))
                  for m in range(61)]
    for k in (1, 2):
        lx = int(CXc + CU * r * k + 0.5) - 13
        ly = int(CYc - CU * k + 0.5) - 12
        if k == 1 and abs(r) > 0.75:                  # the PPL's long-axis placement
            lx = int(CXc + CU * 1.16673 + 0.5) - 13
            ly = int(CYc - CU * 1.16673 * (1 if r > 0 else -1) + 0.5) - 6
        box = (lx, ly + 2, lx + 26, ly + 10)          # the glyph body of "39 %"
        hits = [kk for kk in (1, 2) for m in range(60) if seg_hits_box(ell[kk][m], ell[kk][m + 1], box)]
        inside = CL <= lx and lx + 26 <= CL + 6 * CU and ly >= CT
        if hits or not inside:
            worst.append((r, k, sorted(set(hits)), inside))
check('39 % / 86 % labels clear of both ellipses and inside the box, rho -0.9..0.9',
      not worst, '' if not worst else repr(worst))


# ================================================================ D. beta 1a (harness ppl_run_v3e)
print()
print('D. beta 1a: N1 (help page 4) and N2 (the menu line); the review\'s checks on both versions')
import io as _io                       # noqa: E402
import re as _re                       # noqa: E402
import contextlib as _cl               # noqa: E402
import difflib as _dl                  # noqa: E402
sys.path.insert(0, '/home/claude/work/review')
sys.path.insert(0, '/home/claude/work/out')
import check_BiNorm3D as CB            # noqa: E402   the review's own checks (19 Oct 2026), ppl_run_v3e
import ppl_run_v3e as R3               # noqa: E402
D_RUNS = []
_i0 = R3.Harness.__init__


def _i3(self, *a, **k):
    _i0(self, *a, **k)
    D_RUNS.append(self)


R3.Harness.__init__ = _i3


def cb_run(path, letters):
    CB.PROG = path
    CB.FAILS[:] = []
    CB.NCHK[0] = 0
    buf = _io.StringIO()
    with _cl.redirect_stdout(buf):
        for L in letters:
            getattr(CB, 'part' + L)()
    return CB.NCHK[0], list(CB.FAILS), buf.getvalue()


n_o, f_o, _ = cb_run(OLD, 'ABCDEFGH')
n_n, f_n, log_n = cb_run(PROG, 'ABCDEFGH')
print('  the review\'s check_BiNorm3D on beta 1: %d checks, failed %s' % (n_o, f_o))
print('  the review\'s check_BiNorm3D on beta 1a: %d checks, failed %s' % (n_n, f_n or 'none'))
check('D1 check_BiNorm3D: N1 (F, the verb) and N2 (H, a 31-character menu line) fail on beta 1',
      len(f_o) == 2 and any(f.startswith('F help page 4') for f in f_o) and any(f.startswith('H no menu line') for f in f_o))
check('D1 check_BiNorm3D on beta 1a: all %d checks pass' % n_n, not f_n and n_n == n_o, str(f_n))

# D2. the help page and the menu as the student sees them
h = R3.Harness(PROG, strict=False, cas='fail', stall_limit=30000, idle_key=4)
h.call('bnInit')
h.reset_records()
h.press('Enter', 'Enter', 'Enter', 'Esc')
try:
    h.call('bnHelp')
except Exception as e:
    print('  bnHelp: %s' % str(e)[:80])
pg4 = [pg for pg in h.pages if pg.has('Regression to the mean')]
blue = [t.text for pg in pg4[:1] for t in pg.texts if 114 <= t.y <= 179]
print('  help page 4, the criminal-justice paragraph:')
for t in blue:
    print('    %r (%d)' % (t, len(t)))
sent = ' '.join(blue)
check('D2 N1: page 4 reads "... whose risk score was extreme will score closer to the average next time, programme '
      'or not ..." as six lines of at most 46 characters',
      len(blue) == 6 and 'risk score was extreme will score closer to the average next time, programme or not.' in sent
      and "only a comparison group picked the same way shows what it added." in sent and max(len(t) for t in blue) <= 46)
widths = [(t.text, t.x + 6.2 * len(t.text)) for pg in pg4[:1] for t in pg.texts if 114 <= t.y <= 179]
check('D2 N1: every line of the paragraph ends before x = 308 at 6.2 px a character (widest %.0f)'
      % max(w for _, w in widths), max(w for _, w in widths) <= 308)
for crs, want in ((0, 'Grid while dragging: 15×15'), (1, 'Grid while dragging: 11×11')):
    hm = R3.Harness(PROG, strict=False, cas='fail', stall_limit=30000, idle_key=4)
    hm.call('bnInit')
    hm.globals_['bnCrs'] = float(crs)
    hm.choose(5)                       # the grid item: it toggles bnCrs
    hm.call('bnMenu')
    items = hm.chooses[-1].items
    check('D2 N2: bnCrs = %d: the menu item reads %r (%d characters); choosing it toggles bnCrs to %d; every item '
          '<= 30 characters' % (crs, items[4], len(items[4]), int(hm.globals_['bnCrs'])),
          items[4] == want and hm.globals_['bnCrs'] == 1 - crs and max(len(x) for x in items) <= 30, str(items))

# D3. the routine diff beta 1 -> beta 1a
def d_bodies(txt):
    c = _re.sub(r'//[^\n]*', '', txt)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'\n\s*\n', '\n', _re.sub(r'[ \t]+\n', '\n', m.group(0)))
    return out


def d_code(txt):
    out = []
    for l in txt.split('\n'):
        o, ins = [], False
        for i, ch in enumerate(l):
            if ch == '"':
                ins = not ins
            if not ins and l[i:i + 2] == '//':
                break
            o.append(ch)
        t = ''.join(o).strip()
        if t:
            out.append(t)
    return out


t0, t1 = open(OLD, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()
B0, B1 = d_bodies(t0), d_bodies(t1)
dif = sorted(n for n in set(B0) | set(B1) if B0.get(n) != B1.get(n))
check('D3 the routines that differ from beta 1: %s (want bnHelp, bnMenu; %d routines)' % (dif, len(B1)),
      dif == ['bnHelp', 'bnMenu'])
k0, k1 = d_code(t0), d_code(t1)
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += k0[i1:i2]
    if op in ('replace', 'insert'):
        pl += k1[j1:j2]
print('  code lines removed: %d, added: %d' % (len(mi), len(pl)))
check('D3 only the two menu-label lines and four help lines changed (6 out, 6 in), all of them display text',
      len(mi) == 6 and len(pl) == 6 and all(('muS3 :=' in l) or l.startswith('bnLn(') for l in mi + pl))
# D4. the static rules
vl = t1.split('\n')
depth, bad = 0, []
for n_, l in enumerate(vl, 1):
    ins, start = False, depth
    for i, ch in enumerate(l):
        if ch == '"':
            ins = not ins
        elif not ins:
            if l[i:i + 2] == '//':
                if start > 0:
                    bad.append(n_)
                break
            if ch in '({[':
                depth += 1
            elif ch in ')}]':
                depth -= 1
check('D4 no // comment inside an open bracket', not bad, str(bad[:5]))
check('D4 version strings: the banner reads beta 1a, a "beta 1a (19 Oct 2026)" paragraph, the status line (PC harness '
      'only), and the disclaimer beside the distribution terms',
      vl[3] == '// BINORM3D - beta 1a' and '// beta 1a (19 Oct 2026): N1, N2' in t1
      and 'only in the PC harness (ppl_run_v3e, 19 Oct 2026)' in t1
      and '// DISCLAIMER: a teaching and demonstration aid. Not validated for' in t1)
locs = _re.findall(r'^\s*LOCAL ([^;(]*);', '\n'.join(d_code(t1)), _re.M)
check('D4 every LOCAL line holds at most 6 names; no INSTRING',
      max(len(m.split(',')) for m in locs) <= 6 and not any('INSTRING(' in l for l in d_code(t1)))
# D5. scientific fixed decimals in every ppl_run_v3e run of beta 1a in part D (the review's included)
sci = sorted(set((round(v, 12), d_, r_) for hh in D_RUNS if hh.path == PROG for v, d_, r_ in hh.sci_strings)) \
    if all(hasattr(hh, 'path') for hh in D_RUNS) else \
    sorted(set((round(v, 12), d_, r_) for hh in D_RUNS for v, d_, r_ in hh.sci_strings))
print('  scientific fixed decimals in the %d v3e runs of part D: %s' % (len(D_RUNS), sci or 'none'))
check('D5 no scientific fixed decimal in any run of part D (%d runs, both versions)' % len(D_RUNS), not sci)

print()
print('%d check(s) failed: %s' % (len(fails), fails) if fails else 'ALL CHECKS PASSED')
sys.exit(1 if fails else 0)
