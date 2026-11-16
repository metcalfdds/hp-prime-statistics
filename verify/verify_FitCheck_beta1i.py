#!/usr/bin/env python3
"""verify_FitCheck_beta1i.py -- checks FitCheck beta 1i (Round 16, 15 Nov 2026): Dixon's outlier test on the normality pages
(the Outlier soft key), the preset Darwin's differences, a mended fault of the loader, mended axis numbers, twelve help
pages.  Runs from the
repository alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, beta 1h from git (main at
4e8ff66).  Needs hp-prime-kit (HPKIT), SciPy, NumPy.  About five minutes.

  T1  verify/round16/make_fitcheck_1i.py, run again from beta 1h, makes programs/FitCheck_beta1i.txt byte for byte.
  A   the arithmetic.  fc_DxTail, called through the harness (rule 19), at every n from 3 to 30 with the ratio its n
      takes and 60 ratios from 0.01 to 0.999, against a reference written here: the same double integral on a
      360 x 600-point grid.  The reference against a grid twice as fine, against the closed form at n = 3, against
      1,000,000 simulated samples a case, and against the values McBane (2006) prints.  The printed Q table.  The
      ratios at both ends and the choice of ratio by n, against NumPy.  Darwin's differences.  "Either end = twice
      the one-end p" against simulation.
  P   the Outlier page, line for line: Darwin's differences; a high-end case; a ratio of 1 from tied values; the two
      ends equal; the other end smaller by less than the decimals show; the sentence follows the p as shown; a sample
      of more than 30 values and a sample in bins get sentences and no arithmetic; small and large scales; every n.
  V   every way in and out: the Outlier key from each normality page and back, Bins, Menu, Esc, Enter; taps and arrow
      keys on the page; the closing line; a new sample clears the test; the preset from both menus and Esc at each;
      the menus' other items at their new places; the mended fault (beta 1h stops with an error); Home's FC_R, FC_PR.
  R   regression against beta 1h.  R1: the monkey, 40 seeds, on beta 1h and on beta 1i with its three entrances shut
      (the soft key's action and the two menu items) and beta 1h's help text: the same verdict, boxes and closing
      line, and every screen the same text for text but the opening page.  R2: the menu items that moved, through the
      real menus.
  L   the axis numbers mended in passing: the last number of the ECDF's and the chi-square curve's axis ran off the
      screen in beta 1h, and a value wider than its 40 pixels was cut; where every number fitted, nothing moved.
  H   the help: 12 pages; the old pages word for word where they were not meant to change; the new pages as written;
      every line within 46 characters and 296 pixels, 14 lines a page.
  G   static.     D   layout: text_overlap_v1 and label_fit_v1 over every beta 1i screen drawn above (and what the
      same runs find on beta 1h's screens).
"""
import os, sys, io, re, json, math, random, signal, subprocess, tempfile, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

BASE = '4e8ff66'
PROG = os.path.join('programs', 'FitCheck_beta1i.txt')
tmp = tempfile.mkdtemp(prefix='fcv_')
OLD = os.path.join(tmp, 'FitCheck_beta1h.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/FitCheck_beta1h.txt'], check=True, capture_output=True).stdout)
SRC = io.open(PROG, encoding='utf-8').read()
OSRC = io.open(OLD, encoding='utf-8').read()
GW = json.load(open(os.path.join('verify', 'round11', 'glyph_widths_vc.json')))
FAIL, NPASS = [], [0]
MINUS, AL = chr(8722), chr(945)
SUB = {0: chr(8320), 1: chr(8321), 2: chr(8322)}
K1, K2, K3, K4, K5, K6 = (26, 228), (80, 228), (133, 228), (186, 228), (240, 228), (293, 228)
DARWIN = [6.125, -8.375, 1, 2, 0.75, 2.875, 3.5, 5.125, 1.75, 3.625, 7, 3, 9.375, 7.5, -6]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:900]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def key(h, name):
    for k in h.globals_:
        if k.lower() == name.lower(): return k
    raise KeyError(name)


def G(h, name): return h.globals_[key(h, name)]
def setg(h, name, v): h.globals_[key(h, name)] = v
def px(s, font=1): return sum((GW.get(str(ord(ch))) or [8, 9, 10])[font - 1] for ch in s)
def lst(xs): return '{' + ','.join(repr(float(v)) for v in xs) + '}'
def close(a, b, tol=1e-10): return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def fresh(path=PROG, d1=None):
    app = {'D1': [float(v) for v in d1]} if d1 is not None else None
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=app)
    h.execute('fc_Init()')
    return h


def run(script, path=PROG, d1=None):
    app = {'D1': [float(v) for v in d1]} if d1 is not None else None
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=app)
    h.press('Enter')                     # the title page takes the first key
    script(h)
    try: res = h.execute('FitCheck()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
    return h, res, err


# ---------------- the reference: the double integral on a fine grid ----------------
def gl_panels(a, b, npan, n):
    x, w = np.polynomial.legendre.leggauss(n)
    e = np.linspace(a, b, npan + 1); xs = []; ws = []
    for i in range(npan):
        xs.append((e[i + 1] - e[i]) / 2 * x + (e[i + 1] + e[i]) / 2); ws.append((e[i + 1] - e[i]) / 2 * w)
    return np.concatenate(xs), np.concatenate(ws)


GRID = {}


def tail(R, n, i, j, pa=36, pw=60, lim=9.0):
    """P(ratio > R) at one end: n!/((j-1)! m!) INT INT F(a)^(j-1) f(a) f(b) [G^m + (i-1) m G^(m-1) (H - G)] da dw, b = a + w,
    m = n - j - 1, G = F(b - R w) - F(a), H = F(b) - F(a), on pa x pw panels of 10 Gauss-Legendre points."""
    if (pa, pw, lim) not in GRID: GRID[(pa, pw, lim)] = gl_panels(-lim, lim, pa, 10) + gl_panels(0, 2 * lim, pw, 10)
    AX, AW, WX, WW = GRID[(pa, pw, lim)]
    m = n - j - 1
    a = AX[:, None]; w = WX[None, :]; b = a + w
    Fa = stats.norm.cdf(a); Gm = np.maximum(stats.norm.cdf(b - R * w) - Fa, 0); H = np.maximum(stats.norm.cdf(b) - Fa, 0)
    core = Gm ** m
    if i == 2 and m >= 1: core = core + m * Gm ** (m - 1) * (H - Gm)
    lc = math.lgamma(n + 1) - math.lgamma(j) - math.lgamma(m + 1)
    return float(np.exp(lc) * (Fa ** (j - 1) * stats.norm.pdf(a) * stats.norm.pdf(b) * core * AW[:, None] * WW[None, :]).sum())


def kind(n): return (1, 1) if n <= 7 else (1, 2) if n <= 10 else (2, 2) if n <= 13 else (2, 3)
def name_of(n): i, j = kind(n); return 'r' + SUB[i] + SUB[j - 1]
def crit(alpha, n, i, j): return brentq(lambda R: tail(R, n, i, j) - alpha, 1e-4, 0.99999, xtol=1e-11)


def ratios(xs, n=None):
    """the two ends' ratios of a sample by Dixon's scheme: (low, high)"""
    x = sorted(float(v) for v in xs); n = len(x); i, j = kind(n)
    gl, wl = x[i] - x[0], x[n - j] - x[0]; gh, wh = x[n - 1] - x[n - 1 - i], x[n - 1] - x[j - 1]
    return (gl / wl if gl > 0 and wl > 0 else 0.0), (gh / wh if gh > 0 and wh > 0 else 0.0)


print('=== T. the build')
out = os.path.join(tmp, 'built')
subprocess.run([sys.executable, os.path.join(HERE, 'round16', 'make_fitcheck_1i.py'), out], check=True, capture_output=True)
check('T1 the build makes programs/FitCheck_beta1i.txt byte for byte',
      open(os.path.join(out, 'FitCheck_beta1i.txt'), 'rb').read() == open(PROG, 'rb').read())

print('=== A. the arithmetic')
OV.install()
hA = fresh()
def tailP(R, n, i, j):
    setg(hA, 'fcNX', float(n)); setg(hA, 'fcDxI', float(i)); setg(hA, 'fcDxJ', float(j))
    return hA.execute('fc_DxTail(%r)' % float(R))
Rs = [round(float(v), 4) for v in np.linspace(0.01, 0.999, 60)]
wa = (0.0, None); w3 = (0.0, None); w4 = (0.0, None); npts = 0
for n in range(3, 31):
    i, j = kind(n)
    for R in Rs:
        r = tail(R, n, i, j)
        if r < 1e-6: continue
        v = tailP(R, n, i, j); npts += 1
        if abs(v - r) > wa[0]: wa = (abs(v - r), (n, R, r, v))
        if r > 1e-3 and abs(v / r - 1) > w3[0]: w3 = (abs(v / r - 1), (n, R, r, v))
        if r > 1e-4 and abs(v / r - 1) > w4[0]: w4 = (abs(v / r - 1), (n, R, r, v))
check('A1 fc_DxTail at every n from 3 to 30, %s ratios: against the reference the worst error is %.1e; relative, %.3f %% for a p above 0.001 (limit 0.05 %%) and %.2f %% above 0.0001 (limit 0.2 %%)'
      % (format(npts, ','), wa[0], 100 * w3[0], 100 * w4[0]), wa[0] < 1e-4 and w3[0] < 5e-4 and w4[0] < 2e-3, (wa, w3, w4))
check('A2 at the edges: a ratio of 0 or less has p = 1, a ratio of 1 or more has p = 0, and no p is above 1',
      tailP(0, 5, 1, 1) == 1 and tailP(-0.2, 5, 1, 1) == 1 and tailP(1, 5, 1, 1) == 0 and tailP(1.5, 12, 2, 2) == 0
      and all(tailP(0.001, n, *kind(n)) <= 1 for n in (3, 8, 11, 14, 30)))
worst = 0.0
for n in (3, 4, 7, 8, 10, 11, 13, 14, 20, 30):
    i, j = kind(n)
    for R in (0.02, 0.2, 0.5, 0.7, 0.9, 0.98):
        a = tail(R, n, i, j); b = tail(R, n, i, j, pa=72, pw=120, lim=10.0)
        if a > 1e-12: worst = max(worst, abs(a / b - 1))
check('A3 the reference has converged: a grid twice as fine and wider gives the same 60 values to %.0e (relative)' % worst, worst < 1e-10 and tail(0.3, 9, 1, 2) == tail(0.3, 9, 1, 2), worst)
bad = [(R, tail(R, 3, 1, 1), 1 - (3 / math.pi) * (math.atan((2 * R - 1) / math.sqrt(3)) + math.pi / 6)) for R in (0.05, 0.2, 0.5, 0.8, 0.95, 0.99)]
check('A4 the closed form at n = 3, P(r10 > R) = 1 - (3/pi)(atan((2R - 1)/root 3) + pi/6): the reference to 10 digits, and fc_DxTail within 0.05 %% (P(r10 > 0.5) = %.4f)' % tailP(0.5, 3, 1, 1),
      all(abs(a - b) < 1e-10 for _, a, b in bad) and all(abs(tailP(R, 3, 1, 1) / b - 1) < 5e-4 for R, _, b in bad), bad)
rng = np.random.default_rng(16); rows = []; okS = True
for n in (3, 5, 7, 8, 10, 11, 13, 14, 20, 30):
    i, j = kind(n); x = np.sort(rng.standard_normal((1000000, n)), axis=1)
    r = (x[:, -1] - x[:, -1 - i]) / (x[:, -1] - x[:, j - 1])
    for al in (0.25, 0.05, 0.01):
        R = crit(al, n, i, j); sim = float((r > R).mean()); se = math.sqrt(al * (1 - al) / 1e6)
        rows.append((n, al, round(R, 4), sim)); okS = okS and abs(sim - al) < 4 * se
check('A5 simulation: 1,000,000 normal samples at each of 10 sizes; the share of ratios above the reference\'s 25 %, 5 % and 1 % points is within 4 standard errors of each (30 cases)', okS, [x for x in rows if abs(x[3] - x[1]) > 3 * math.sqrt(x[1] * (1 - x[1]) / 1e6)])
MCB = {4: 0.910, 6: 0.610, 8: 0.480, 22: 0.269, 24: 0.259, 26: 0.251, 28: 0.243, 30: 0.237}     # McBane (2006), its test3 output: r11, alpha = 0.1, one-tailed
mine = {n: crit(0.1, n, 1, 2) for n in MCB}
viaP = {n: tailP(mine[n], n, 1, 2) for n in MCB}
check('A6 McBane\'s (2006) eight printed values of r11 at alpha = 0.1 (n = 4 to 30) are the reference\'s to 3 decimals, and fc_DxTail at those points is 0.1 within 0.05 %',
      all(abs(round(mine[n], 3) - MCB[n]) < 5e-4 for n in MCB) and all(abs(viaP[n] / 0.1 - 1) < 5e-4 for n in MCB), (mine, viaP))
# the printed Q table (Rorabacher 1991 by way of Harvey, Analytical Chemistry 2.1, the appendix "Critical Values for Dixon's Q-Test"):
# two-sided alpha .10, .05, .01 for n = 3..10, the plain ratio r10 at every n
QTAB = {0.10: [.941, .765, .642, .560, .507, .468, .437, .412], 0.05: [.970, .829, .710, .625, .568, .526, .493, .466], 0.01: [.994, .926, .821, .740, .680, .634, .598, .568]}
dq = {(a2, n): QTAB[a2][n - 3] - crit(a2 / 2, n, 1, 1) for a2 in QTAB for n in range(3, 11)}
big = max(abs(v) for v in dq.values())
check('A7 the printed two-sided Q table (n = 3 to 10) is the one-sided point at alpha/2 to within %.4f; its two largest gaps are the two McBane names: n = 4 and 6 at 99 %% (%+.4f and %+.4f)'
      % (big, dq[(0.01, 4)], dq[(0.01, 6)]), big < 0.006 and abs(dq[(0.01, 4)] - 0.005) < 0.0006 and abs(dq[(0.01, 6)] + 0.003) < 0.0006
      and sorted(dq, key=lambda k: -abs(dq[k]))[:2] == [(0.01, 4), (0.01, 6)], sorted(((round(v, 4), k) for k, v in dq.items()), key=lambda t: -abs(t[0]))[:4])
rr = random.Random(16); bad = []; nsm = 0
for n in list(range(3, 31)) * 6:
    sc = 10 ** rr.uniform(-4, 5); xs = [round(rr.gauss(0, 1) * sc + 3 * sc, 9) for _ in range(n)]
    if rr.random() < 0.3: xs[rr.randrange(n)] += rr.choice((-1, 1)) * 6 * sc
    if len(set(xs)) < 2: continue
    hh = fresh()
    if hh.execute('fc_NormSet(%s, "t", "src")' % lst(xs)) != 1: bad.append((n, 'refused')); continue
    hh.execute('fc_DxCalc()'); nsm += 1
    lo, hi = ratios(xs); i, j = kind(n); pxl = [float(v) for v in G(hh, 'fcDxPx')]
    ok = (close(G(hh, 'fcDxRL'), lo, 1e-9) and close(G(hh, 'fcDxRH'), hi, 1e-9) and (G(hh, 'fcDxI'), G(hh, 'fcDxJ')) == (i, j)
          and G(hh, 'fcDxE') == (1 if lo > hi else 2) and G(hh, 'fcDxOK') == 1 and close(G(hh, 'FC_R'), max(lo, hi), 1e-9)
          and close(G(hh, 'FC_PR'), min(1.0, 2 * G(hh, 'fcDxP')), 1e-12) and abs(G(hh, 'fcDxP') - tail(max(lo, hi), n, i, j)) < 1e-4
          and len(pxl) == n and pxl[0] == 24 and pxl[-1] == 296 and pxl == sorted(pxl) and len(G(hh, 'fcDxLv')) == n)
    if not ok: bad.append((n, lo, hi, G(hh, 'fcDxRL'), G(hh, 'fcDxRH'), G(hh, 'fcDxE'), G(hh, 'fcDxP')))
check('A8 %d random samples of 3 to 30 values: the ratio at each end and the ratio\'s kind are as NumPy has them (r10 to 7, r11 to 10, r21 to 13, r22 to 30), the bigger end is the one tested, its p is the reference\'s to 0.0001, FC_R and FC_PR hold the ratio and twice the p, and the strip runs from pixel 24 to 296' % nsm, not bad and nsm > 150, bad[:2])
rk = io.open([os.path.join('programs', f) for f in sorted(os.listdir('programs')) if f.startswith('RankLab_')][-1], encoding='utf-8').read()
xa = [float(v) for v in re.search(r'rkXA := \{([^}]*)\};\s*\n\s*rkXB', rk).group(1).split(',')]; xb = [float(v) for v in re.search(r'rkXB := \{([^}]*)\};', rk).group(1).split(',')]
hD0 = Harness(PROG, idle_key=4, home_minus=True, cas='fail'); hD0.execute('fc_Init()'); hD0.press('Enter'); hD0.execute('fc_PreDarwin()')      # the preset as the menu loads it
hD = fresh(); hD.execute('fc_NormSet(%s, "d", "src")' % lst(DARWIN)); hD.execute('fc_DxCalc()')                                        # the same values, and the test
dx = sorted(DARWIN); lo, hi = ratios(DARWIN)
check('A9 Darwin\'s differences: the 15 values are RankLab\'s pairs, crossed minus self-fertilized, and times 8 they are Fisher\'s 49, -67, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, -48',
      [a - b for a, b in zip(xa, xb)] == DARWIN and [8 * v for v in DARWIN] == [49, -67, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, -48] and [float(v) for v in G(hD0, 'fcX')] == dx and G(hD0, 'fcNPre') == 9
      and [float(v) for v in G(hD, 'fcX')] == dx)
p22 = tail(lo, 15, 2, 3); p10 = tail((dx[1] - dx[0]) / (dx[14] - dx[0]), 15, 1, 1)
check('A10 Darwin\'s differences, n = 15: r22 at the low end = 9.125/15.375 = %.4f, one-end p %.4f (reference %.5f), either end %.4f; the high end %.4f; the plain r10 would be %.3f with a one-end p of %.2f: the second low value hides the first'
      % (G(hD, 'fcDxRL'), G(hD, 'fcDxP'), p22, G(hD, 'FC_PR'), G(hD, 'fcDxRH'), (dx[1] - dx[0]) / (dx[14] - dx[0]), p10),
      close(G(hD, 'fcDxRL'), 9.125 / 15.375) and close(lo, 9.125 / 15.375) and abs(G(hD, 'fcDxP') / p22 - 1) < 5e-4 and round(G(hD, 'FC_PR'), 4) == 0.0321 and round(G(hD, 'fcDxRH'), 4) == 0.2754
      and G(hD, 'fcDxE') == 1 and round((dx[1] - dx[0]) / (dx[14] - dx[0]), 3) == 0.134 and 0.40 < p10 < 0.45, (G(hD, 'fcDxRL'), G(hD, 'fcDxP'), p22, p10))
rng = np.random.default_rng(1616); rows = []; okE = True
for n in (5, 7, 9, 12, 15, 30):
    i, j = kind(n); R = crit(0.025, n, i, j); x = np.sort(rng.standard_normal((2000000, n)), axis=1)
    rh = (x[:, -1] - x[:, -1 - i]) / (x[:, -1] - x[:, j - 1]); rl = (x[:, i] - x[:, 0]) / (x[:, n - j] - x[:, 0])
    either = float(((rh > R) | (rl > R)).mean()); both = float(((rh > R) & (rl > R)).mean()); se = math.sqrt(0.05 * 0.95 / 2e6)
    rows.append((n, round(R, 4), either, both)); okE = okE and either < 0.05 + 4 * se and either > 0.05 * 0.92 and ((i, j) != (1, 1) or (R > 0.5 and both == 0 and abs(either - 0.05) < 4 * se))
check('A11 "either end = twice the one-end p" is an upper limit: at the two-sided 5 %% point, 2,000,000 samples at each of 6 sizes (n = 5, 7, 9, 12, 15, 30), the share with EITHER end\'s ratio above it is %s: 5 %% for r10 (above 0.5 both ends never count at once), 4.6 to 4.9 %% for the other ratios, never above 5 %% (but for chance)'
      % ', '.join('%.4f' % r[2] for r in rows), okE and all(0.046 <= r[2] <= 0.049 for r in rows[2:]), rows)
wD, pD = stats.shapiro(DARWIN)
check('A12 the engine beside it is untouched: Shapiro-Wilk on Darwin\'s differences, W = %.4f and p = %.4f as SciPy has them (%.4f, %.4f)' % (G(hD, 'fcW'), G(hD, 'fcPW'), wD, pD),
      abs(G(hD, 'fcW') - wD) < 5e-5 and abs(G(hD, 'fcPW') - pD) < 5e-4, (G(hD, 'fcW'), wD, G(hD, 'fcPW'), pD))


# ---------------- the Outlier page, modelled here line for line ----------------
from decimal import Decimal, ROUND_HALF_UP  # noqa: E402
RED, GRN = 0xFF0000, 0x008C3C
KEYS = '{"Q-Q", "ECDF", "Tests", "Bins", "Outlier", "Menu"}'


def fx(v, d):
    """a number with d decimals as the program writes it: rounded half up, a rounded -0 shown as 0, the Prime's minus"""
    q = Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if q == 0: q = abs(q)
    t = format(q, 'f')
    return t.replace('-', MINUS)


def commas(t):
    def grp(m):
        g = m.group(0)
        return g if len(g) < 4 else format(int(g), ',')
    return re.sub(r'(?<![\.\d])\d+', grp, t)


def val(v, T):
    """fc_DxFmt: as few decimals as the value needs, judged against the sample's range T, up to MAX(4, 3 - FLOOR(LOG T)), 12 at most"""
    dm = min(12, max(4, 3 - math.floor(math.log10(T))))
    for d in range(dm + 1):
        if abs(v - float(Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))) <= 1e-7 * T: return commas(fx(v, d))
    return commas(fx(v, dm))


def pstr(p): return 'p < 0.0001' if p < 0.0001 else 'p > 0.9999' if p > 0.9999 else 'p = ' + fx(p, 4)


def page(xs, title='t'):
    hh = fresh()
    if hh.execute('fc_NormSet(%s, "%s", "src")' % (lst(xs), title)) != 1: return hh, None
    hh.execute('fc_DxCalc()'); hh.execute('fc_DrawDx()'); hh.execute('fc_Show(%s)' % KEYS)
    return hh, hh.screens[-1]


def expect(hh, xs, title='t'):
    """the page's lines for a sample, from the sample and from the p the program holds (A8 checks that p)"""
    x = sorted(float(v) for v in xs); n = len(x); i, j = kind(n); lo, hi = ratios(xs); T = x[-1] - x[0]
    E = 1 if lo > hi else 2; R = max(lo, hi); p1 = G(hh, 'fcDxP'); p2 = min(1.0, 2 * p1)
    flag = float(Decimal(repr(p2)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)) < 0.05
    O, Gp, Rg = (1, 1 + i, n + 1 - j) if E == 1 else (n, n - i, j)
    oth = hi if E == 1 else lo
    r3 = lambda v: float(Decimal(repr(float(v))).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
    tail_ = ', the smaller (not tested).' if r3(oth) < r3(R) else ', a little smaller (not tested).' if oth < R else ', the same.'
    L = ['Outlier? ' + title,
         "Dixon's %s = %s,  %s (either end)" % (name_of(n), fx(R, 3), pstr(p2)),
         'Red dot: the value tested.  Its ratio = gap / range.',
         'range ' + val(abs(x[O - 1] - x[Rg - 1]), T), 'gap ' + val(abs(x[O - 1] - x[Gp - 1]), T),
         ('Low end: (x(%d) - x(1)) / (x(%d) - x(1))' % (Gp, Rg) if E == 1 else 'High end: (x(%d) - x(%d)) / (x(%d) - x(%d))' % (O, Gp, O, Rg)) + ' = ' + fx(R, 3),
         'This end alone: ' + pstr(p1) + ('.  Either end: twice that, at most.' if 2 * p1 <= 1 else '.  Either end: no more than 1.'),
         ('High end: ratio ' if E == 1 else 'Low end: ratio ') + fx(oth, 3) + tail_,
         'x(%d) = %s' % (O, val(x[O - 1], T)) + (': flagged as an outlier at ' + AL + ' = 0.05.' if flag else ': not flagged at ' + AL + ' = 0.05.'),
         "%s: Dixon's ratio for n from %s.  Normal data assumed." % (name_of(n), '3 to 7' if n <= 7 else '8 to 10' if n <= 10 else '11 to 13' if n <= 13 else '14 to 30'),
         'A ratio of 1 here means tied values: p means little.' if R >= 1 else 'A flagged value is one to check, not to delete.']
    return L, flag


def body(scr):
    """the page's lines without the axis numbers (y = 116), in the order the model lists them"""
    return [t.text for t in sorted(scr.texts, key=lambda t: (t.y, t.x)) if t.y != 116]


def colors(scr):
    t = {tt.y: int(tt.color) for tt in scr.texts}
    return t.get(21), t.get(170)


print('=== P. the Outlier page')
hP, sP = page(DARWIN, "Darwin's differences")
wantD = ["Outlier? Darwin's differences", "Dixon's r" + SUB[2] + SUB[2] + ' = 0.593,  p = 0.0321 (either end)', 'Red dot: the value tested.  Its ratio = gap / range.',
         'range 15.375', 'gap 9.125', 'Low end: (x(3) - x(1)) / (x(13) - x(1)) = 0.593', 'This end alone: p = 0.0161.  Either end: twice that, at most.',
         'High end: ratio 0.275, the smaller (not tested).', 'x(1) = ' + MINUS + '8.375: flagged as an outlier at ' + AL + ' = 0.05.',
         'r' + SUB[2] + SUB[2] + ": Dixon's ratio for n from 14 to 30.  Normal data assumed.", 'A flagged value is one to check, not to delete.']
axis = [t.text for t in sorted(sP.texts, key=lambda t: t.x) if t.y == 116]
check('P1 Darwin\'s differences: the page reads, line for line, %r ... and its axis is numbered %s' % (wantD[1], ', '.join(axis)),
      body(sP) == wantD and expect(hP, DARWIN, "Darwin's differences")[0] == wantD and axis == [MINUS + '5', '0', '5'] and colors(sP) == (RED, RED), [l for l in body(sP) if l not in wantD])
def has_line(scr, x1, y1, x2, y2, col):
    return any(s.cmd == 'LINE_P' and [int(round(float(v))) for v in s.args[0:4]] == [x1, y1, x2, y2] and int(s.args[4]) == col for s in scr.shapes)
pxD = [int(v) for v in G(hP, 'fcDxPx')]
check('P2 the picture: the range bracket (blue, y 61) runs from the tested value\'s pixel to x(13)\'s, the gap bracket (red, y 80 and 81) to x(3)\'s; the tested dot is red and drawn last',
      has_line(sP, pxD[0], 61, pxD[12], 61, 0x003CC8) and has_line(sP, pxD[0], 80, pxD[2], 80, RED) and has_line(sP, pxD[0], 81, pxD[2], 81, RED)
      and [s for s in sP.shapes if s.cmd == 'RECT_P'][-1].args[-1] == RED and pxD[0] == 24 and pxD[14] == 296, pxD)
HIGH = [12.1, 11.8, 12.4, 12.0, 15.9]
hH, sH = page(HIGH, 'high'); LH, flH = expect(hH, HIGH, 'high')
check('P3 a high-end case, n = 5 ({12.1, 11.8, 12.4, 12.0, 15.9}): %r, %r, %r; red' % (LH[1], LH[5], LH[8]),
      body(sH) == LH and LH[5] == 'High end: (x(5) - x(4)) / (x(5) - x(1)) = 0.854' and flH and colors(sH) == (RED, RED) and LH[7].startswith('Low end: ratio 0.049, the smaller'), [l for l in body(sH) if l not in LH])
TIE = [10.1, 10.1, 10.3]
hT, sT = page(TIE, 'tie'); LT, flT = expect(hT, TIE, 'tie')
check('P4 two of three values the same ({10.1, 10.1, 10.3}): the ratio is 1.000, p < 0.0001, and the last line says "%s"' % LT[-1],
      body(sT) == LT and LT[1] == "Dixon's r" + SUB[1] + SUB[0] + ' = 1.000,  p < 0.0001 (either end)' and LT[-1] == 'A ratio of 1 here means tied values: p means little.' and G(hT, 'fcDxP') == 0
      and LT[7] == 'Low end: ratio 0.000, the smaller (not tested).', body(sT))
SYM = [1, 2, 3]
hS, sS = page(SYM, 'sym'); LS, flS = expect(hS, SYM, 'sym')
check('P5 the two ends equal ({1, 2, 3}): both ratios 0.500, the high end is shown, "%s", p for either end %s, green' % (LS[7], LS[1].split(',  ')[1]),
      body(sS) == LS and LS[7] == 'Low end: ratio 0.500, the same.' and G(hS, 'fcDxE') == 2 and abs(G(hS, 'fcDxP') - 0.5) < 3e-4 and not flS and colors(sS) == (GRN, GRN)
      and LS[1].endswith('p > 0.9999 (either end)'), body(sS))
NEAR = [0, 1.0004, 2]
hN, sN = page(NEAR, 'near'); LN, flN = expect(hN, NEAR, 'near')
check('P6 the other end smaller by less than the decimals show ({0, 1.0004, 2}): "%s"' % LN[7], body(sN) == LN and LN[7] == 'High end: ratio 0.500, a little smaller (not tested).' and LN[5].startswith('Low end: (x(2) - x(1)) / (x(3) - x(1)) = 0.500'), body(sN))
res = []
for p1, want_flag in ((0.024996, False), (0.02497, True), (0.025, False), (0.0249749, True), (0.03, False), (0.0001, True)):
    hh, _ = page(HIGH, 'edge'); setg(hh, 'fcDxP', p1); hh.execute('fc_DrawDx()'); hh.execute('fc_Show(%s)' % KEYS); sc = hh.screens[-1]; L, fl = expect(hh, HIGH, 'edge')
    res.append((p1, body(sc) == L, fl == want_flag, colors(sc) == ((RED, RED) if want_flag else (GRN, GRN)), L[1].split(',  ')[1], L[8].split(': ')[1]))
check('P7 the sentence follows the p AS SHOWN: a one-end p of 0.024996 shows "p = 0.0500" and "not flagged" (green); 0.02497 shows "p = 0.0499" and "flagged" (red); six cases',
      all(r[1] and r[2] and r[3] for r in res) and res[0][4] == 'p = 0.0500 (either end)' and res[1][4] == 'p = 0.0499 (either end)', res)
def s_rossi_out(h): h.choose(5); h.choose(1); h.press('Enter'); h.tap(*K5); h.press('Esc'); h.choose(11)
def s_crim_out(h): h.choose(5); h.choose(2); h.press('Enter'); h.tap(*K5); h.press('Esc'); h.choose(11)
hR, resR, errR = run(s_rossi_out); hC, resC, errC = run(s_crim_out)
def outl(h): return [s for s in h.screens if s.lines() and s.lines()[0].startswith('Outlier? ')]
def allt(h): return ' '.join(t.text for s in h.screens for t in s.texts)
def nbusy(h): return sum(1 for t in h.texts if t.text.startswith("Dixon's ratio and its p"))
LR_ = [l.rstrip() for l in outl(hR)[-1].lines()]; LC_ = [l.rstrip() for l in outl(hC)[-1].lines()]
check('P8 the Rossi ages (n = 432): the Outlier key gives sentences ("%s ... %s"), nothing is worked out, and the closing line has no Dixon in it' % (LR_[1], LR_[4]),
      errR is None and LR_[:7] == ['Outlier? Rossi ages', "Dixon's outlier test is for a small sample: 3", 'to 30 values.', '', 'This sample has 432 values.', '', 'With a larger sample, look at the two ends of']
      and G(hR, 'fcDxOK') == 0 and nbusy(hR) == 0 and 'Dixon' not in resR and ' W = ' in resR, (errR, resR, LR_))
check('P9 the crimtab heights (in bins): "%s %s", nothing is worked out' % (LC_[4], LC_[5]),
      errC is None and LC_[0] == 'Outlier? crimtab heights' and ' '.join(LC_[4:6]) == 'This sample is in bins (3,000 values in 22 bins), so it has no single values to test.' and G(hC, 'fcDxOK') == 0 and 'Dixon' not in resC, (errC, resC, LC_))
TINY = [0.00000012, 0.00000015, 0.00000016, 0.00000017, 0.00000031]
BIG = [1234567.5, 1234570.25, 1234571, 1234571.5, 1234572, 1234590.75, 1234572.5, 1234573]
hTi, sTi = page(TINY, 'tiny'); LTi, _ = expect(hTi, TINY, 'tiny'); hB, sB = page(BIG, 'big'); LB, _ = expect(hB, BIG, 'big')
axB = [t.text for t in sorted(sB.texts, key=lambda t: t.x) if t.y == 116]; axT = [t.text for t in sorted(sTi.texts, key=lambda t: t.x) if t.y == 116]
check('P10 the numbers keep the decimals the sample\'s scale needs: values near 0.0000002 read %r and %r; values near 1,234,570 read %r with commas, and the axis %s' % (LTi[3], LTi[8].split(':')[0], LB[8].split(':')[0], ', '.join(axB)),
      body(sTi) == LTi and LTi[3] == 'range 0.00000019' and LTi[4] == 'gap 0.00000014' and LTi[8].startswith('x(5) = 0.00000031:') and axT == ['0.00000015', '0.00000020', '0.00000025', '0.00000030']
      and body(sB) == LB and LB[3] == 'range 20.5' and LB[4] == 'gap 17.75' and LB[8].startswith('x(8) = 1,234,590.75:') and axB == ['1,234,570', '1,234,580', '1,234,590'], (body(sTi), axT, body(sB), axB))
rr = random.Random(1616); bad = []; npg = 0; nfl = 0; kinds = set()
for n in list(range(3, 31)) * 3:
    kind_ = rr.randrange(4)
    if kind_ == 0: xs = [round(rr.gauss(50, 10), 1) for _ in range(n)]                      # rounded: ties now and then
    elif kind_ == 1: xs = [float(rr.randint(1, 6)) for _ in range(n)]                       # heavy ties: towers of dots
    elif kind_ == 2: xs = [round(rr.gauss(0, 1), 4) for _ in range(n - 1)] + [rr.choice((-1, 1)) * rr.uniform(4, 9)]   # one value far out
    else: xs = [round(rr.lognormvariate(8, 1.5), 2) for _ in range(n)]                      # thousands, skewed
    if len(set(xs)) < 2: continue
    hh, sc = page(xs, 'r')
    if sc is None: bad.append((n, 'refused', xs[:4])); continue
    L, fl = expect(hh, xs, 'r'); npg += 1; nfl += fl; kinds.add((kind(n), fl))
    okc = colors(sc) == ((RED, RED) if fl else (GRN, GRN)); ax = [t for t in sc.texts if t.y == 116]
    lab = [t for t in sc.texts if t.y in (46, 65)]
    inside = all(t.x >= 2 and t.x + px(t.text) <= 318 for t in sc.texts)
    if not (body(sc) == L and okc and len(ax) >= 1 and len(lab) == 2 and inside and int(G(hh, 'fcDxMx')) <= n - 1):
        bad.append((n, kind_, [a for a, b in zip(body(sc), L) if a != b][:2], [b for a, b in zip(body(sc), L) if a != b][:2], okc, len(ax), inside))
check('P11 %d random samples, three at every n from 3 to 30 (rounded, heavily tied, one value far out, thousands): every page is the model\'s line for line, red where flagged (%d) and green where not, its axis numbered, every text inside the screen' % (npg, nfl),
      not bad and npg >= 80 and nfl >= 10 and len(set(k for k, _ in kinds)) == 4, bad[:2])

print('=== V. every way in and out')
def s_darwin(*steps):
    def s(h):
        h.choose(5); h.choose(3); h.press('Enter')
        for st in steps:
            if isinstance(st, tuple): h.tap(*st)
            else: h.press(st)
        h.choose(11)
    return s
def firsts(h): return [s.lines()[0] for s in h.screens if s.lines() and s.menu]
h1, r1, e1 = run(s_darwin(K5, K1, K5, K2, K5, K3, K5, K6))
f1 = [x.split(':')[0].split('?')[0] for x in firsts(h1)]
check('V1 Darwin\'s differences, then Outlier from the Q-Q page, from the ECDF page and from the Tests page, and back by each of those keys; Menu leaves: the pages come in that order, and the test is worked out once',
      e1 is None and f1 == ['Q-Q', 'Outlier', 'Q-Q', 'Outlier', 'ECDF vs normal', 'Outlier', 'Normality', 'Outlier'] and nbusy(h1) == 1, (e1, f1, nbusy(h1)))
WANT = 'FitCheck: W = 0.9008, p = 0.0978; Dixon r22 = 0.593, p = 0.0321 (either end);'
check('V2 the closing line then reads %r' % r1, r1 == WANT, r1)
h2, r2, e2 = run(s_darwin(K5, 'Esc')); h3, r3, e3 = run(s_darwin(K5, 'Enter')); h4, r4, e4 = run(s_darwin('Esc'))
check('V3 Esc and Enter leave the Outlier page for the menu like Menu does (the same closing line); without the Outlier key the line has no Dixon in it (%r)' % r4,
      e2 is None and e3 is None and e4 is None and r2 == WANT and r3 == WANT and r4 == 'FitCheck: W = 0.9008, p = 0.0978;' and G(h4, 'fcDxOK') == 0, (r2, r3, r4))
h5, r5, e5 = run(s_darwin(K5, (160, 100), (30, 60), (300, 200), 'Left', 'Right', 'Up', 'Down', 'Plus', 'Esc'))
n5 = [s.lines() for s in h5.screens if s.lines() and s.menu and s.lines()[0].startswith('Outlier')]
check('V4 on the Outlier page three taps on the picture and the text, the four arrows and + change nothing: the page is drawn again the same (%d times), and the closing line is the same' % len(n5),
      e5 is None and len(n5) >= 9 and all(x == n5[0] for x in n5) and r5 == WANT, (e5, len(n5), r5))
h6, r6, e6 = run(s_darwin(K5, K4, 'Esc'))
check('V5 Bins from the Outlier page opens the chi-square fit on bins as before, and both results are in the closing line (%r)' % r6,
      e6 is None and isinstance(r6, str) and r6.startswith('FitCheck: ' + chr(967) + chr(178) + '(') and 'Dixon r22 = 0.593' in r6 and ' W = 0.9008' in r6, (e6, r6))
def s_new(h): h.choose(5); h.choose(3); h.press('Enter'); h.tap(*K5); h.press('Esc'); h.choose(5); h.choose(5); h.press('Esc'); h.choose(11)
h7, r7, e7 = run(s_new, d1=HIGH)
def s_new2(h): h.choose(5); h.choose(3); h.press('Enter'); h.tap(*K5); h.press('Esc'); h.choose(5); h.choose(5); h.tap(*K5); h.press('Esc'); h.choose(11)
h8, r8, e8 = run(s_new2, d1=HIGH)
check('V6 a new sample clears the test: Darwin and its Outlier page, then My values in D1 (5 values) without the Outlier key: no Dixon in the closing line (%r); with the key, the new sample\'s (%r)' % (r7, r8),
      e7 is None and e8 is None and 'Dixon' not in r7 and G(h7, 'fcDxOK') == 0 and 'Dixon r10 = 0.854' in r8 and G(h8, 'fcNX') == 5, (e7, r7, e8, r8))
def s_last(h): h.choose(5); h.choose(3); h.press('Enter'); h.tap(*K5); h.press('Esc'); h.choose(5); h.choose(1); h.tap(*K5); h.press('Esc'); h.choose(11)
h9, r9, e9 = run(s_last)
check('V7 "The last sample again" keeps the test: the Outlier page comes back without being worked out again (the "working" box is drawn once in the session)', e9 is None and r9 == WANT and nbusy(h9) == 1, (e9, r9, nbusy(h9)))
m1 = [c for c in h9.chooses if c.title == 'Normality']
check('V8 the Normality menu: 4 items before a sample is loaded, 5 after ("Preset: Darwin\'s differences" above "My values in D1"), none over 30 characters',
      [list(c.items) for c in m1] == [['Preset: Rossi ages', 'Preset: crimtab heights', "Preset: Darwin's differences", 'My values in D1'],
                                      ['The last sample again', 'Preset: Rossi ages', 'Preset: crimtab heights', "Preset: Darwin's differences", 'My values in D1']]
      and all(len(i) <= 30 for c in m1 for i in c.items), [list(c.items) for c in m1])
def s_pre(h): h.choose(8); h.choose(7); h.press('Enter'); h.tap(*K5); h.press('Esc'); h.choose(11)
h10, r10, e10 = run(s_pre); pm = [c for c in h10.chooses if c.title == 'Load a preset'][0]
check('V9 Load a preset: 9 items, the seventh "Darwin\'s differences: outlier"; it loads the same sample and the Outlier page gives the same line',
      e10 is None and r10 == WANT and len(pm.items) == 9 and pm.items[6] == "Darwin's differences: outlier" and pm.items[7] == 'Draft lottery 1970' and pm.items[8] == 'Binomial (illustrative)' and all(len(i) <= 30 for i in pm.items), (e10, r10, list(pm.items)))
def s_esc_n(h): h.choose(5); h.choose(0); h.choose(8); h.choose(0); h.choose(0)
h11, r11, e11 = run(s_esc_n)
check('V10 Esc at the Normality menu, at the preset menu and at the main menu: nothing loaded, "FitCheck: nothing computed"', e11 is None and r11 == 'FitCheck: nothing computed' and G(h11, 'fcHasN') == 0 and G(h11, 'fcDxOK') == 0, (e11, r11))
# the mended fault: a refused sample used to replace the loaded sample's sorted values
def s_fault(first):
    def s(h):
        h.choose(5); h.choose(first); h.press('Enter'); h.press('Esc')          # a preset, its source page, its Q-Q page, back
        h.choose(5); h.choose(h.myv)                                             # My values in D1: every value the same, refused
        h.choose(5); h.choose(1); h.tap(*K2); h.tap(*K3); h.press('Esc'); h.choose(11)   # The last sample again: Q-Q, ECDF, Tests
    return s
def with_myv(path, first, myv, d1):
    app = {'D1': [float(v) for v in d1]}
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=app); h.myv = myv
    h.press('Enter'); s_fault(first)(h)
    try: res = h.execute('FitCheck()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:120])
    return h, res, err
ho, ro, eo = with_myv(OLD, 1, 4, [5, 5, 5, 5]); hn, rn, en = with_myv(PROG, 1, 5, [5, 5, 5, 5])
boxo = [' '.join(m.lines) for m in ho.msgboxes]; boxn = [' '.join(m.lines) for m in hn.msgboxes]
check('V11 the mended fault: the Rossi ages loaded, then D1 = {5, 5, 5, 5} refused ("%s"), then The last sample again.  beta 1h stopped with %r; beta 1i shows the Rossi ages again and ends %r' % (boxn[0][:23], eo, rn),
      eo is not None and 'out of range' in eo and en is None and boxo == boxn and boxn == ['Every value is the same: s = 0, so there is no shape to test.'] and G(hn, 'fcNX') == 432 and len(G(hn, 'fcX')) == 432 and ' W = 0.8499' in rn, (eo, en, rn, boxn))
hn2, rn2, en2 = with_myv(PROG, 2, 5, [7, 7, 7])
check('V12 the same after the sample in bins: the refused D1 leaves the crimtab heights as they were (%r)' % rn2, en2 is None and G(hn2, 'fcBin') == 1 and G(hn2, 'fcNX') == 3000 and 'binned sample' in rn2, (en2, rn2))
h12, r12, e12 = run(lambda h: (h.choose(5), h.choose(4), h.choose(11)), d1=[1, 2])
check('V13 My values in D1 at its new place (item 4 before a sample is loaded) with two values: refused with "need at least 3 values", nothing loaded',
      e12 is None and 'need at least 3 values' in ' '.join(' '.join(m.lines) for m in h12.msgboxes) and G(h12, 'fcHasN') == 0, (e12, r12))
check('V14 Home: after Darwin\'s Outlier page FC_R = %.6f and FC_PR = %.6f; a session that never opens the page leaves them as they were' % (G(h1, 'FC_R'), G(h1, 'FC_PR')),
      close(G(h1, 'FC_R'), 9.125 / 15.375) and close(G(h1, 'FC_PR'), 2 * G(h1, 'fcDxP')) and G(h4, 'FC_R') == 0 and G(h4, 'FC_PR') == 0, (G(h1, 'FC_R'), G(h1, 'FC_PR'), G(h4, 'FC_R'), G(h4, 'FC_PR')))

print('=== R. regression against beta 1h')
# beta 1i with its three entrances shut: the soft key does nothing again, and the two menus are beta 1h's
SHUT = SRC
def shut(a, b):
    global SHUT
    assert SHUT.count(a) == 1, (SHUT.count(a), a[:70])
    SHUT = SHUT.replace(a, b)
shut('''        IF nlSl == 5 THEN
          nlScr := 4;
          IF fcBin == 0 AND fcNX <= 30 AND fcDxOK == 0 THEN fc_DxCalc(); END;
        END;
''', '')
shut('''"Preset: crimtab heights", "Preset: Darwin's differences", "My values in D1"});
  ELSE''', '''"Preset: crimtab heights", "My values in D1"});
  ELSE''')
shut('''{"Preset: Rossi ages", "Preset: crimtab heights", "Preset: Darwin's differences", "My values in D1"});
    IF mnI > 0''', '''{"Preset: Rossi ages", "Preset: crimtab heights", "My values in D1"});
    IF mnI > 0''')
shut('''    IF mnI == 4 THEN fc_PreDarwin(); IF fcHasN == 1 THEN fc_NorLoop(1); END; END;
    IF mnI == 5 THEN fc_MyD(1); END;
''', '''    IF mnI == 4 THEN fc_MyD(1); END;
''')
shut('''    "Darwin's differences: outlier",
''', '')
shut('''    IF prsI == 7 THEN fc_PreDarwin(); IF fcHasN == 1 THEN fc_NorLoop(1); END; END;
    IF prsI == 8 THEN fc_PreDraft(); fc_GofLoop(1); END;
    IF prsI == 9 THEN fc_PreBinIll(); fc_GofLoop(1); END;
''', '''    IF prsI == 7 THEN fc_PreDraft(); fc_GofLoop(1); END;
    IF prsI == 8 THEN fc_PreBinIll(); fc_GofLoop(1); END;
''')
def help_of(src): return src[src.index('fc_Help()\nBEGIN\n'):src.index('\n// The title page, with the disclaimer on screen.')]
shut(help_of(SRC), help_of(OSRC))
SHUTP = os.path.join(tmp, 'FitCheck_beta1i_shut.txt'); io.open(SHUTP, 'w', encoding='utf-8', newline='').write(SHUT)
argv = sys.argv; sys.argv = ['monkey_v1b.py']
import monkey_v1b as MK  # noqa: E402
sys.argv = argv
def skip(lines):
    return bool(lines) and lines[0].startswith('FitCheck - beta')
def one(path, seed):
    rng = random.Random(seed)
    app, kind_ = MK.random_lists(rng)
    hh = MK.Monkey(path, rng, app, 150)
    for q in range(10): hh.globals_.setdefault('M%d' % q, MK.R.interp.Matrix([[0.0]]))
    m1_, mk = MK.random_matrix(seed)
    if m1_ is not None: hh.globals_['M1'] = m1_
    verdict = 'OK'
    signal.signal(signal.SIGALRM, MK._alarm); signal.alarm(60)
    try: hh.execute('FitCheck()')
    except MK.TimeUp: verdict = 'FREEZE'
    except Exception as e: verdict = 'END ' + type(e).__name__
    finally: signal.alarm(0)
    scr = [tuple(t.text for t in s.texts) for s in hh.screens]
    boxes = [' '.join(m.lines) for m in hh.msgboxes]
    return verdict, [('<skipped>',) if skip(list(s)) else s for s in scr], boxes, str(hh.result), sum(1 for s in scr if skip(list(s)))
diffs = []; nscr = 0; nskip = 0; verd = {}; mended = []; nhelp = 0
for sd in range(1600, 1640):
    a = one(OLD, sd); b = one(SHUTP, sd)
    nscr += len(b[1]); nskip += b[4]; verd[b[0]] = verd.get(b[0], 0) + 1; nhelp += sum(1 for x in b[1] if x and x[0].startswith('FitCheck help'))
    if a[0] != b[0] or a[2] != b[2] or a[3] != b[3] or a[1] != b[1]:
        if any('Every value is the same' in x for x in a[2]) and b[0] == 'OK': mended.append((sd, a[0], b[0])); continue      # the mended fault (V11): beta 1h goes on with a spoiled sample
        k = next((i for i, (x, y) in enumerate(zip(a[1], b[1])) if x != y), None)
        diffs.append((sd, a[0], b[0], a[3] == b[3], len(a[1]), len(b[1]), k, (a[1][k][:3], b[1][k][:3]) if k is not None else None))
check('R1 the monkey, 40 seeds, on beta 1h and on beta 1i with its three entrances shut and beta 1h\'s help text: the same verdict, boxes and closing line, and all %s screens the same text for text (%d help pages among them) but the %d opening pages (%s; %d runs set aside where beta 1h went on after a refused sample: the mended fault)'
      % (format(nscr, ','), nhelp, nskip, verd, len(mended)), not diffs and nscr > 400 and len(mended) <= 4, (diffs[:2], mended))
# R2: the items that moved, through the real menus: the old menu's item on beta 1h against its new place on beta 1i
def texts_after(h, title_start):
    out = []
    for s in h.screens:
        L = [t.text for t in s.texts]
        if L and not L[0].startswith('FitCheck - beta'): out.append(tuple(L))
    return out
pairs = []
for nm, so, sn, d1 in (('Load a preset > Draft lottery 1970', lambda h: (h.choose(8), h.choose(7), h.press('Enter'), h.tap(*K2), h.tap(*K3), h.tap(*K4), h.press('Esc'), h.choose(11)),
                        lambda h: (h.choose(8), h.choose(8), h.press('Enter'), h.tap(*K2), h.tap(*K3), h.tap(*K4), h.press('Esc'), h.choose(11)), None),
                       ('Load a preset > Binomial (illustrative)', lambda h: (h.choose(8), h.choose(8), h.press('Enter'), h.tap(*K2), h.tap(*K3), h.tap(*K4), h.press('Esc'), h.choose(11)),
                        lambda h: (h.choose(8), h.choose(9), h.press('Enter'), h.tap(*K2), h.tap(*K3), h.tap(*K4), h.press('Esc'), h.choose(11)), None),
                       ('Normality > My values in D1, no sample yet', lambda h: (h.choose(5), h.choose(3), h.tap(*K2), h.tap(*K3), h.press('Esc'), h.choose(11)),
                        lambda h: (h.choose(5), h.choose(4), h.tap(*K2), h.tap(*K3), h.press('Esc'), h.choose(11)), [3.1, 4.7, 5.2, 5.9, 6.3, 7.7, 8.1, 9.6, 12.4]),
                       ('Normality > My values in D1, after a sample', lambda h: (h.choose(5), h.choose(1), h.press('Enter'), h.press('Esc'), h.choose(5), h.choose(4), h.tap(*K2), h.tap(*K3), h.press('Esc'), h.choose(11)),
                        lambda h: (h.choose(5), h.choose(1), h.press('Enter'), h.press('Esc'), h.choose(5), h.choose(5), h.tap(*K2), h.tap(*K3), h.press('Esc'), h.choose(11)), [3.1, 4.7, 5.2, 5.9, 6.3, 7.7, 8.1, 9.6, 12.4]),
                       ('Normality > Rossi ages and crimtab heights (not moved)', lambda h: (h.choose(5), h.choose(1), h.press('Enter'), h.tap(*K2), h.tap(*K3), h.press('Esc'), h.choose(5), h.choose(3), h.press('Enter'), h.tap(*K3), h.press('Esc'), h.choose(11)),
                        lambda h: (h.choose(5), h.choose(1), h.press('Enter'), h.tap(*K2), h.tap(*K3), h.press('Esc'), h.choose(5), h.choose(3), h.press('Enter'), h.tap(*K3), h.press('Esc'), h.choose(11)), None)):
    ho_, ro_, eo_ = run(so, path=OLD, d1=d1); hn_, rn_, en_ = run(sn, d1=d1)
    pairs.append((nm, eo_ is None and en_ is None and ro_ == rn_ and texts_after(ho_, '') == texts_after(hn_, '') and len(texts_after(hn_, '')) >= 4, eo_, en_, ro_, rn_, len(texts_after(hn_, ''))))
check('R2 the menu items that moved, through the real menus, beta 1h\'s place against beta 1i\'s: the draft lottery and the illustrative binomial (presets 7, 8 -> 8, 9), My values in D1 (3 -> 4, 4 -> 5), and Rossi and crimtab where they were: the same screens and closing lines (%s screens)'
      % ', '.join(str(p_[6]) for p_ in pairs), all(p_[1] for p_ in pairs), [p_ for p_ in pairs if not p_[1]][:1])

print('=== L. the axis numbers mended in passing')
EE = chr(7431)
def pxw(t): return sum((GW.get(str(ord(ch))) or [6, 7, 8])[0] for ch in t)       # font 1; a glyph not in the table (the small capital E) counts as a digit
def norm_pages(path, d1, myv):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data={'D1': [float(v) for v in d1]})
    h.press('Enter'); h.choose(5); h.choose(myv); h.tap(*K2); h.press('Esc'); h.choose(11)
    h.execute('FitCheck()')
    return {s.lines()[0].split(':')[0]: [(t.text, int(t.x), int(t.y), None if t.width is None else float(t.width)) for t in s.texts] for s in h.screens if s.menu and s.lines()}
def faults(pg):
    return sorted((nm, t, 'cut' if (w is not None and pxw(t) > w) else 'off') for nm, L_ in pg.items() for (t, x, y, w) in L_ if (w is not None and pxw(t) > w) or x + pxw(t) > 320)
THOU = [1210, 1340, 1385, 1420, 1466, 1502, 1533, 1590, 1622, 1700, 1745, 1810, 2950]
SMALL = [3.1, 4.7, 5.2, 5.9, 6.3, 7.7, 8.1, 9.6, 12.4]
MILL = [1200000, 1450000, 1500000, 1620000, 1800000, 2100000, 2500000, 3900000]
po_, pn_ = norm_pages(OLD, THOU, 3), norm_pages(PROG, THOU, 4)
dif = [(a, b) for nm in po_ for a, b in zip(po_[nm], pn_[nm]) if a[:3] != b[:3]]
check('L1 values in the thousands: in beta 1h the ECDF\'s last axis number, "3,000", began at x = 299 and ran off the screen; in beta 1i it begins at x = %d and ends on it; nothing else on the two pages moved'
      % [x for (t, x, y, w) in pn_['ECDF vs normal'] if t == '3,000'][0],
      faults(po_) == [('ECDF vs normal', '3,000', 'off')] and not faults(pn_) and [(a[:3], b[:3]) for a, b in dif] == [(('3,000', 299, 161), ('3,000', 289, 161))], (faults(po_), faults(pn_), dif[:4]))
po_, pn_ = norm_pages(OLD, BIG, 3), norm_pages(PROG, BIG, 4)
axn = sorted(set(t for nm in pn_ for (t, x, y, w) in pn_[nm] if EE in t))
check('L2 seven-digit values: beta 1h cut %d axis numbers by their 40 pixels ("1,234,570" needs %d); beta 1i cuts none, runs none off the screen, and writes both axes in scientific form (%s)'
      % (len([f for f in faults(po_) if f[2] == 'cut']), pxw('1,234,570'), ', '.join(axn)), len([f for f in faults(po_) if f[2] == 'cut']) >= 5 and not faults(pn_) and axn == ['1.2' + EE + '6'], (faults(po_), faults(pn_), axn))
pm_ = norm_pages(PROG, MILL, 4); axm = [t for (t, x, y, w) in pm_['ECDF vs normal'] if EE in t]; axq = [t for (t, x, y, w) in pm_['Q-Q'] if EE in t]
check('L3 values in the millions read %s along the ECDF and %s up the Q-Q plot; nothing cut, nothing off the screen' % (', '.join(axm), ', '.join(axq)),
      axm == ['2' + EE + '6', '3' + EE + '6', '4' + EE + '6'] and sorted(axq) == ['2' + EE + '6', '3' + EE + '6', '4' + EE + '6'] and not faults(pm_), (axm, axq, faults(pm_)))
def xy(pg): return {k: [t[:3] for t in v] for k, v in pg.items()}
same_small = xy(norm_pages(OLD, SMALL, 3)) == xy(norm_pages(PROG, SMALL, 4))
def preset_pages(path, item):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail'); h.press('Enter'); h.choose(5); h.choose(item); h.press('Enter'); h.tap(*K2); h.press('Esc'); h.choose(11); h.execute('FitCheck()')
    return [[(t.text, int(t.x), int(t.y)) for t in s.texts] for s in h.screens if s.menu and s.lines()]
check('L4 where every number fitted nothing moved: nine small values, the Rossi ages and the crimtab heights give the same Q-Q and ECDF pages in both versions, text for text and pixel for pixel',
      same_small and preset_pages(OLD, 1) == preset_pages(PROG, 1) and preset_pages(OLD, 2) == preset_pages(PROG, 2))
rr = random.Random(89); TWO = [float(rr.randint(10, 99)) for _ in range(400)]
def curve_page(path):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data={'D1': TWO}); h.press('Enter'); h.choose(2); h.choose(3); h.tap(*K3); h.press('Esc'); h.choose(11); h.execute('FitCheck()')
    return [[(t.text, int(t.x), int(t.y)) for t in s.texts] for s in h.screens if s.menu and s.lines() and 'curve' in s.lines()[0]][-1]
co, cn = curve_page(OLD), curve_page(PROG); lasto = max((x, t) for (t, x, y) in co if y == 155); lastn = max((x, t) for (t, x, y) in cn if y == 155)
check('L5 the chi-square curve of a first-two-digits Benford fit (df = 89): its last axis number, "%s", began at x = %d in beta 1h (%d pixels past the edge) and begins at x = %d now; the rest of the page did not move'
      % (lasto[1], lasto[0], lasto[0] + pxw(lasto[1]) - 320, lastn[0]), lasto[0] + pxw(lasto[1]) > 320 and lastn[0] + pxw(lastn[1]) <= 320 and lasto[1] == lastn[1]
      and [a for a, b in zip(co, cn) if a != b] == [(lasto[1], lasto[0], 155)], (lasto, lastn, [a for a, b in zip(co, cn) if a != b]))
hL = fresh()
forms = [hL.execute(c) for c in ('fc_AxLb(1500000, 0, 1)', 'fc_AxLb(2000000, 0, 1)', 'fc_AxLb(-3000000, 0, 1)', 'fc_AxLb(0, 0, 1)', 'fc_AxLb(0.00000015, 8, 1)', 'fc_AxLb(1234.5, 1, 0)', 'fc_AxLb(-0.0000001, 3, 0)', 'fc_AxLb(0.5, 15, 0)')]
check('L6 fc_AxLb: %s' % ', '.join(forms), forms == ['1.5' + EE + '6', '2' + EE + '6', MINUS + '3' + EE + '6', '0', '1.5' + EE + MINUS + '7', '1,234.5', '0.000', '0.500000000000'], forms)
wid = [hL.execute(c) for c in ('fc_AxWide(100000, 250000, 50000, 0, 40)', 'fc_AxWide(500000, 1000000, 250000, 0, 40)', 'fc_AxWide(0.0000001, 0.0000003, 0.00000005, 8, 40)', 'fc_AxWide(-1, 1, 0.5, 1, 40)', 'fc_AxWide(-99999, 99999, 50000, 0, 40)')]
check('L7 fc_AxWide: numbers up to "250,000" (39 px) fit 40 pixels, "1,000,000" and "0.00000015" do not', wid == [0, 1, 1, 0, 0], wid)

print('=== H. the help')
def helppages(path):
    hh = Harness(path, idle_key=4, home_minus=True, cas='fail')
    hh.press('Enter'); hh.choose(10); [hh.press('Down') for _ in range(14)]; hh.press('Esc'); hh.choose(11)
    hh.execute('FitCheck()')
    seen, pages = set(), []
    for s in hh.screens:
        L = s.lines()
        if L and L[0].startswith('FitCheck help') and L[0] not in seen: seen.add(L[0]); pages.append(s)
    return pages
po, pn = helppages(OLD), helppages(PROG)
TOP = ['Two questions', 'Goodness of fit', 'Small counts and Merge', 'Benford, Poisson, binomial', 'Normality', 'Reading p; the exact test', "Outliers: Dixon's test", 'Outliers: which ratio',
       'Outliers: the p and its limits', 'Keys and presets', 'Home variables', 'Credits']
check('H1 twelve help pages (eight before), titled n/12: %s' % '; '.join(TOP[6:11]), len(po) == 8 and len(pn) == 12 and [p.lines()[0] for p in pn] == ['FitCheck help %d/12: %s' % (k + 1, t) for k, t in enumerate(TOP)], [p.lines()[0] for p in pn])
def bodyl(p): return [l.rstrip() for l in p.lines()[1:-1]]
def words(p): return ' '.join(' '.join(bodyl(p)).split())
same = all(bodyl(po[k]) == bodyl(pn[k]) for k in (1, 2, 3, 4, 5)) and bodyl(po[7]) == bodyl(pn[11])
check('H2 pages 2 to 6 are beta 1h\'s word for word and line for line, and page 12, Credits, is beta 1h\'s page 8', same, [k for k in (1, 2, 3, 4, 5) if bodyl(po[k]) != bodyl(pn[k])])
check('H3 page 1 is beta 1h\'s with one clause more ("... for one proportion, and Dixon\'s test for one outlier in a small sample.")',
      words(pn[0]) == words(po[0])[:-1] + ", and Dixon's test for one outlier in a small sample.", words(pn[0])[-120:])
old7 = words(po[6]); k_home = old7.index('HOME, after a run')
check('H4 page 10, Keys and presets, is the first two paragraphs of beta 1h\'s page 7 with "Outlier" among the soft keys',
      words(pn[9]) == old7[:k_home].strip().replace('Tests, Bins; Plot', 'Tests, Bins, Outlier; Plot') and 'Tests, Bins, Outlier; Plot' in words(pn[9]), words(pn[9])[:200])
exports = re.findall(r'\bFC_[A-Z0-9]+\b', ' '.join(l.split('//')[0] for l in SRC.split('\n') if l.startswith('EXPORT ')))
w11 = words(pn[10])
check('H5 page 11, Home variables, names every exported variable (%d: %s) and ends "FC_R, FC_PR: Dixon\'s ratio and its either-end p."' % (len(exports), ', '.join(exports)),
      len(exports) == 14 and all(re.search(r'\b%s\b' % e, w11) for e in exports) and w11.endswith("FC_R, FC_PR: Dixon's ratio and its either-end p.") and all(e in old7 for e in exports[:12]), w11)
r10_, r11_, r21_, r22_ = 'r' + SUB[1] + SUB[0], 'r' + SUB[1] + SUB[1], 'r' + SUB[2] + SUB[1], 'r' + SUB[2] + SUB[2]
W7 = ("DIXON'S OUTLIER TEST (the Outlier key; 3 to 30 values). Is the lowest or the highest value too far from the rest to come from the same normal population? Sort the values: x(1) is the lowest, x(n) the highest. "
      "The ratio is a gap over a range: how far the value stands from its neighbor, as a share of the spread. 0 = no gap; 1 = it stands alone. "
      "The page draws every value as a dot, the tested one in red, with its gap (red) and its range (blue) above the dots. It tests the end with the bigger ratio.")
W8 = ("The ratio changes with n (Dixon 1953). First digit: the gap ends at the nearest value (1) or the second-nearest (2). Second digit: how many values the range leaves off its far end. "
      "3 to 7 values: " + r10_ + ". The gap to the nearest value, over the whole range. 8 to 10: " + r11_ + ". The range leaves off 1 value. 11 to 13: " + r21_ + ". The gap to the second-nearest value; the range leaves off 1. "
      "14 to 30: " + r22_ + ". The range leaves off 2 values. Why: a second outlier, beside the first or at the far end, would hide the first. The later ratios guard against that.")
W9 = ("THE P is the chance, in a normal sample of this size, of a ratio this big or bigger at that end. FitCheck computes it; a printed table of critical values can differ from it in the third decimal (McBane 2006). "
      "The test takes the end with the bigger ratio, so the p it reports is for either end: twice the one-end p, as in the printed tables. That is an upper limit. "
      "A small p is a reason to check the value: was it misread, mistyped, or from another population? It is no license to delete it. "
      "The p assumes normal data (see the Q-Q plot). Values tied by rounding can make the ratio 1.")
check('H6 pages 7, 8 and 9 read as written (Dixon\'s test; which ratio; the p and its limits)', words(pn[6]) == W7 and words(pn[7]) == W8 and words(pn[8]) == W9,
      [w for w, p_ in ((W7, pn[6]), (W8, pn[7]), (W9, pn[8])) if words(p_) != w][:1] + [words(pn[6])[:150], words(pn[7])[:150]])
starts8 = [l for l in bodyl(pn[7]) if re.match(r'(3 to 7 values|8 to 10|11 to 13|14 to 30|Why): ', l)]
check('H7 on page 8 each of the four ratios, and the "Why", begins a line of its own', len(starts8) == 5, bodyl(pn[7]))
longest = max(len(l) for p in pn for l in bodyl(p)); wide = [(l, px(l)) for p in pn for l in p.lines()[1:] if px(l.rstrip()) > 296]
check('H8 no help line is longer than 46 characters (longest %d) or wider than 296 px at the measured glyph widths (widest %d px), and no page has more than 14 lines of text'
      % (longest, max(px(l.rstrip()) for p in pn for l in p.lines()[1:])), longest <= 46 and not wide and all(len(bodyl(p)) <= 14 for p in pn), (wide[:2], [len(bodyl(p)) for p in pn]))

print('=== G. static')
code = '\n'.join(re.sub(r'"[^"\n]*"', '""', l.split('//')[0]) for l in SRC.split('\n'))
check('G1 no "!=" in the code, and the code outside strings and comments is ASCII', '!=' not in code and all(ord(c) < 128 for c in code))
loc = [l for l in SRC.split('\n') if re.match(r'\s*LOCAL\s', l)]
check('G2 every LOCAL line names at most 6 variables (%d lines)' % len(loc), all(len(l.split('//')[0].replace('LOCAL', '').split(',')) <= 6 for l in loc))
long_o = [len(l) for l in OSRC.split('\n') if len(l) > 250]; long_n = [len(l) for l in SRC.split('\n') if len(l) > 250]
check('G3 the header names beta 1i and its date; no source line is over 250 characters (beta 1h had two, of %s)' % ' and '.join(str(v) for v in long_o),
      '// FITCHECK - beta 1i  (15 Nov 2026)' in SRC and '// beta 1i (15 Nov 2026): Round 16' in SRC and 'fc_Frame("FitCheck - beta 1i");' in SRC and not long_n and long_o == [336, 311], (long_o, long_n))
gx, gw = np.polynomial.legendre.leggauss(20)
mx = re.search(r'fcDxGX := \{([^}]*)\};', SRC); mw = re.search(r'fcDxGW := \{([^}]*)\};', SRC)
nx = [float(v) for v in mx.group(1).split(',')] if mx else []; nw = [float(v) for v in mw.group(1).split(',')] if mw else []
check('G4 the 20 nodes and 20 weights written in fc_Init are NumPy\'s 20-point Gauss-Legendre rule to 12 decimals (the weights add up to %.12f)' % sum(nw),
      len(nx) == 20 and len(nw) == 20 and np.allclose(nx, gx, atol=6e-13, rtol=0) and np.allclose(nw, gw, atol=6e-13, rtol=0) and abs(sum(nw) - 2) < 1e-11)
items = []
for m in re.finditer(r'CHOOSE\(\w+,\s*("[^"]*"|[^,]+(?:\+[^,]+)*),\s*\{(.*?)\}\);', SRC, re.S):
    for it in re.split(r',\s*(?=")|,\s*\n\s*', m.group(2)):
        t = re.sub(r'"\s*\+\s*fcX2S\s*\+\s*"|fcX2S\s*\+\s*"|"\s*\+\s*fcX2S', chr(967) + chr(178), it.strip())
        t = re.sub(r'"\s*\+\s*fcSq\s*\+\s*"', chr(178), t); t = re.sub(r'"\s*\+\s*CHAR\(8320\)', chr(8320) + '"', t)
        items.append(t.strip().strip('"'))
check('G5 every item of every menu is at most 30 characters (%d items in the source; the longest is %r, %d)' % (len(items), max(items, key=len), max(len(i) for i in items)),
      len(items) >= 60 and max(len(i) for i in items) <= 30, sorted(items, key=len)[-3:])
L_ = SRC.split('\n'); mp = {}
for m in re.finditer(r'(\d+)-(\d+|end)', '\n'.join(l for l in L_[:260] if l.startswith('//   ') and re.search(r'\d+-(\d+|end)', l) and 'File map' not in l and L_.index(l) > L_.index(next(x for x in L_ if x.startswith('// File map:'))))):
    mp[int(m.group(1))] = m.group(2)
first_ok = all(L_[a - 1].startswith('// ====') or L_[a - 1].startswith('EXPORT FC_X2') for a in mp)
ends_ok = all(b == 'end' or L_[int(b)].strip() == '' for b in mp.values())
check('G6 the file map in the header is true: each of its %d sections begins where the map says (a bar of = signs, or the first EXPORT), and ends on the line before a blank one' % len(mp), len(mp) == 17 and first_ok and ends_ok, sorted(mp.items())[:20])
check('G7 the nine new routines carry the program\'s tag, and beta 1h\'s routines are all still there (%d before, %d now)'
      % (len(re.findall(r'(?m)^(?:EXPORT )?(fc_\w+|FitCheck)\(', OSRC)), len(re.findall(r'(?m)^(?:EXPORT )?(fc_\w+|FitCheck)\(', SRC))),
      set(re.findall(r'(?m)^(?:EXPORT )?(fc_\w+|FitCheck)\(', OSRC)) <= set(re.findall(r'(?m)^(?:EXPORT )?(fc_\w+|FitCheck)\(', SRC))
      and set(re.findall(r'(?m)^(?:EXPORT )?(fc_\w+|FitCheck)\(', SRC)) - set(re.findall(r'(?m)^(?:EXPORT )?(fc_\w+|FitCheck)\(', OSRC)) == {'fc_DxRat', 'fc_DxFmt', 'fc_DxNm', 'fc_DxTail', 'fc_DxCalc', 'fc_DrawDx', 'fc_PreDarwin', 'fc_AxLb', 'fc_AxWide'})
big_un = sorted(set((m.group(0), it['text'][:40]) for rec in OV.RECORDS.values() for e in rec['screens'].values() for it in e[2]['items'] if 'text' in it
                    for m in re.finditer(r'(?<![\d.,])\d{4,}(?![\d,])', it['text']) if not re.fullmatch(r'(18|19|20)\d\d', m.group(0)) and '10^' not in it['text']))
check('G8 commas: no number of four or more digits is drawn without them on any screen above (years in citations aside)', not big_un, big_un[:8])

print('=== D. layout over every beta 1i screen above')
NEWTAGS = [t for t in OV.RECORDS if t.startswith('FitCheck_beta1i')]; OLDTAGS = [t for t in OV.RECORDS if t.startswith('FitCheck_beta1h')]
firm = []; firm_old = []
for t, f in OV.report().items():
    dst = firm if t in NEWTAGS else firm_old
    dst += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    dst += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
recs_new = dict((t, OV.RECORDS[t]) for t in NEWTAGS)
rep_ = sorted(set((x[0], x[3], x[4]) for v in LF.clipped(recs_new).values() for x in v))
cut = [(t, pxw(t) if int(f) == 1 else px(t, int(f)), w) for t, f, w in rep_ if (pxw(t) if int(f) == 1 else px(t, int(f))) > w]
nsc = sum(len(OV.RECORDS[t]['screens']) for t in NEWTAGS)
check('D1 no firm overlap and no text off the screen on any beta 1i screen above (text_overlap_v1 over %s different screens; on beta 1h\'s screens of the same runs it finds %s)'
      % (format(nsc, ','), ', '.join('"%s" %s' % x for x in sorted(set(firm_old))) or 'nothing'), not firm and len(NEWTAGS) == 2 and nsc > 250, firm[:4])
check('D2 no number cut short by its width argument (label_fit_v1 reports %d texts at its estimate; none is wider than its width argument at the measured glyph widths)' % len(rep_), not cut, cut[:4])

# D3: a CHOOSE title shows 31 characters on the calculator (tools/prime_facts_v1.py, fact 4); the harness keeps every
# title a program showed in any run above, and each one longer than that.
_new = os.path.basename(PROG); _cut = sorted(set(t for t, sh_, fn_, f_ in Harness.cut_titles if f_ == _new))
check('D3 no menu title of this version is longer than the 31 characters a CHOOSE box shows (%d different titles in the runs above)'
      % len(Harness.shown_titles.get(_new, ())), not _cut and len(Harness.shown_titles.get(_new, ())) >= 1, _cut[:4])
print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
