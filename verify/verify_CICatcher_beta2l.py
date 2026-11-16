#!/usr/bin/env python3
"""verify_CICatcher_beta2l.py -- checks CICatcher beta 2l (Round 16, 15 Nov 2026): the tolerance interval xbar +/- k s, made
to hold at least 90 % (95 %, 99 %) of a normal population with the confidence on the slider, and its EXACT factor k.
Runs from the repository alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, beta 2k
from git (the commit before Round 16).  Needs hp-prime-kit (HPKIT), SciPy, NumPy.

  T1  verify/round16/make_cicatcher_2l.py, run again from beta 2k, makes programs/CICatcher_beta2l.txt byte for byte.
  A   the arithmetic, each routine called through the harness (rule 19) against references that do not use its code:
      rho against Brent's method; the factor k against a 400-node Gauss-Legendre integral solved by Brent's method (itself
      checked against SciPy's adaptive quadrature), and against a simulation of 400,000 samples from the definition; Howe's
      approximation and the exact factor at n = 10; the catch level of a sample against the reference integral, and
      against what the interval drawn at a level really holds; the window.
  S   a tolerance run through the program's own sampler: the long-run rate at the level, and the tally moving with it.
  V   the setup and every way out of it (Esc at each menu, Cancel on the form, each refused value), a whole tolerance
      session (the six soft keys, the slider, a picked line, a new n, Reset, Help), the line each kind of run returns,
      and back to a t run.
  R   regression against beta 2k: a scripted session of each of the five old intervals shows the same screens, boxes
      and closing line in both versions.
  H   the help: seven pages; six are beta 2k's word for word (the page count aside); page 5 is new; every line fits.
  G   static.     D   layout: text_overlap_v1 and label_fit_v1 over every beta 2l screen drawn above.
"""
import os, sys, io, re, json, math, subprocess, tempfile, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness, CANCEL  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import numpy as np  # noqa: E402
from scipy import stats, integrate  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

BASE = '4e8ff66'
PROG = os.path.join('programs', 'CICatcher_beta2l.txt')
tmp = tempfile.mkdtemp(prefix='cqv_')
OLD = os.path.join(tmp, 'CICatcher_beta2k.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/CICatcher_beta2k.txt'], check=True, capture_output=True).stdout)
SRC = io.open(PROG, encoding='utf-8').read()
GW = json.load(open(os.path.join('verify', 'round11', 'glyph_widths_vc.json')))
FAIL, NPASS = [], [0]
MU, SG, XB, PM = chr(956), chr(963), chr(57344), chr(177)
K1, K2, K3, K4, K5, K6 = (26, 228), (80, 228), (133, 228), (186, 228), (240, 228), (293, 228)


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:700]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def key(h, name):
    for k in h.globals_:
        if k.lower() == name.lower(): return k
    raise KeyError(name)


def G(h, name): return h.globals_[key(h, name)]
def S(h, name, v): h.globals_[key(h, name)] = v
def px(text, font=1): return sum(GW[str(ord(c))][font - 1] for c in text)


def tol(n, p, path=PROG, seed=0, mu=100.0, sg=15.0, level=950):
    """a tolerance run set up as cqSetup leaves it, by hand: the program's own tables for this n and p"""
    h = Harness(path, idle_key=4, home_minus=True, seed=seed)
    h.execute('cqInit()')
    S(h, 'cqType', 2.0); S(h, 'cqTol', 1.0); S(h, 'cqTP', float(p)); S(h, 'cqN', float(n)); S(h, 'cqNm', float(n))
    S(h, 'cqMu', float(mu)); S(h, 'cqSg', float(sg)); S(h, 'cqL', float(level))
    h.execute('cqReset()')
    return h


def run(script, path=PROG, seed=0):
    """a whole run of CICatcher(): the opening page takes the first key, then the script"""
    h = Harness(path, idle_key=4, home_minus=True, seed=seed)
    h.press('Enter')
    script(h)
    try: res = h.execute('CICatcher()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:300])
    return h, res, err


# ---------------- references ----------------
def rho_ref(d, p):
    return brentq(lambda r: stats.norm.cdf(d + r) - stats.norm.cdf(d - r) - p, 0, abs(d) + 12, xtol=1e-14)


def rho_vec(x, p):
    ax = np.abs(x); lo = ax + stats.norm.ppf(p); hi = ax + stats.norm.ppf((1 + p) / 2); r = hi.copy()
    for _ in range(80):
        f = stats.norm.cdf(ax + r) - stats.norm.cdf(ax - r) - p
        r = np.minimum(hi, np.maximum(lo, r - f / (stats.norm.pdf(ax + r) + stats.norm.pdf(ax - r))))
    return r


_x, _w = np.polynomial.legendre.leggauss(400)
_T = 10.0 / 2 * (_x + 1); _WF = 10.0 / 2 * _w * stats.norm.pdf(_T)


def g_ref(k, n, p):
    """the confidence of the factor k: 400 Gauss-Legendre nodes on 0..10"""
    rh = rho_vec(_T / math.sqrt(n), p)
    return 1 - 2 * float((_WF * stats.chi2.cdf((n - 1) * rh * rh / (k * k), n - 1)).sum())


def k_ref(n, p, g): return brentq(lambda k: g_ref(k, n, p) - g, 0.05, 20000, xtol=1e-13)


def g_adaptive(k, n, p):
    f = lambda t: stats.norm.pdf(t) * stats.chi2.cdf((n - 1) * rho_ref(t / math.sqrt(n), p) ** 2 / k ** 2, n - 1)
    return 1 - 2 * integrate.quad(f, 0, 10, limit=300, epsabs=1e-13, epsrel=1e-13)[0]


def howe(n, p, g): return stats.norm.ppf((1 + p) / 2) * math.sqrt((n - 1) * (1 + 1 / n) / stats.chi2.ppf(1 - g, n - 1))


print('=== T. the build')
out = os.path.join(tmp, 'built')
subprocess.run([sys.executable, os.path.join(HERE, 'round16', 'make_cicatcher_2l.py'), out], check=True, capture_output=True)
check('T1 the build makes programs/CICatcher_beta2l.txt byte for byte',
      open(os.path.join(out, 'CICatcher_beta2l.txt'), 'rb').read() == open(PROG, 'rb').read())

print('=== A. the arithmetic')
OV.install()
bad = [(n, p, k) for (n, p, k) in ((2, 0.9, 30.0), (10, 0.9, 2.856), (5, 0.99, 3.0), (100, 0.95, 2.5)) if abs(g_ref(k, n, p) - g_adaptive(k, n, p)) > 1e-10]
check('A0 the reference itself: the 400-node integral equals SciPy\'s adaptive quadrature (with Brent\'s rho) to 1E-10 at four (n, p, k)', not bad, bad)
h = tol(10, 0.9); bad = []
for p in (0.9, 0.95, 0.99):
    S(h, 'cqTP', p); h.execute('cqTolSet()')
    for d in (0, 0.01, 0.1, 0.5, 1, 2, 3, 5, 8):
        r = h.execute('cqTolRho(%r)' % d)
        if abs(r - rho_ref(d, p)) > 1e-10: bad.append((p, d, r, rho_ref(d, p)))
check('A1 cqTolRho: Phi(d + r) - Phi(d - r) = p, against Brent\'s method to 1E-10 at 9 values of d from 0 to 8 for p = 0.90, 0.95, 0.99', not bad, bad[:3])
NS = (2, 3, 4, 5, 7, 10, 15, 20, 30, 50, 100); PS = (0.9, 0.95, 0.99); GS = (0.5, 0.8, 0.9, 0.95, 0.99, 0.999)
worst = (0, None); worstg = (0, None); KREF = {}
for n in NS:
    for p in PS:
        h = tol(n, p)
        for g in GS:
            kr = k_ref(n, p, g); KREF[(n, p, g)] = kr
            k = h.execute('cqTolK(%r)' % g)
            if abs(k / kr - 1) > worst[0]: worst = (abs(k / kr - 1), (n, p, g, k, kr))
            gg = h.execute('cqTolG(%r)' % kr)
            if abs(gg - g) > worstg[0]: worstg = (abs(gg - g), (n, p, g, gg))
check('A2 cqTolK, the exact factor, against the reference at %d cases (n = 2 to 100; p = 0.90, 0.95, 0.99; confidence 0.5 to 0.999): worst relative error %.1e'
      % (len(KREF), worst[0]), worst[0] < 1e-5, worst)
check('A3 cqTolG, the confidence of a factor, at the reference factor of each case: worst error %.1e' % worstg[0], worstg[0] < 5e-6, worstg)
rng = np.random.default_rng(20261115); bad = []
for (n, p, g) in ((10, 0.90, 0.95), (5, 0.99, 0.95), (30, 0.95, 0.99), (2, 0.90, 0.80)):
    h = tol(n, p); k = h.execute('cqTolK(%r)' % g)
    x = rng.normal(size=(400000, n)); m = x.mean(axis=1); sd = x.std(axis=1, ddof=1)
    share = float(((stats.norm.cdf(m + k * sd) - stats.norm.cdf(m - k * sd)) >= p).mean())
    if abs(share - g) > 4 * math.sqrt(g * (1 - g) / 400000): bad.append((n, p, g, k, share))
check('A4 a second reference, the definition simulated: of 400,000 samples, the share whose interval xbar +/- k s holds at least p of the population is the confidence (4 cases, within 4 standard errors)', not bad, bad)
h = tol(10, 0.9); k10 = h.execute('cqTolK(0.95)')
m = re.search(r'"n = 10 and 95 %, k = ([0-9.]+)\.  k is worked out exactly here;"', SRC)
check('A5 at n = 10, 90 %% of the population, 95 %% confidence: the exact k is %.4f (the help page prints %s) and Howe\'s approximation, which the header quotes as 2.838, is %.4f'
      % (k10, m.group(1) if m else '?', howe(10, 0.9, 0.95)), bool(m) and m.group(1) == '%.3f' % k10 == '2.856' and '%.3f' % howe(10, 0.9, 0.95) == '2.838')
bad = []; nsamp = 0; ties = 0
for (n, p) in ((10, 0.9), (5, 0.95), (30, 0.99), (2, 0.9), (100, 0.95)):
    h = tol(n, p)
    ks = {L: h.execute('cqTolK(%r)' % (L / 1000.0)) for L in (500, 800, 900, 950, 990, 999)}
    xs = rng.normal(100, 15, size=(120, n)); ms = xs.mean(axis=1); sds = xs.std(axis=1, ddof=1)
    for e, sd in zip(ms, sds):
        c = h.execute('cqTolCat(%r, %r)' % (float(e), float(sd))); nsamp += 1
        kstar = 15 * rho_ref(abs(e - 100) / 15, p) / sd
        gref = g_ref(kstar, n, p)
        want = max(500, min(1000, math.ceil(1000 * gref)))
        if c != want:
            if abs(1000 * gref - round(1000 * gref)) < 1e-3: ties += 1
            else: bad.append(('level', n, p, c, want, gref))
        for L, k in ks.items():
            hold = stats.norm.cdf(e + k * sd, 100, 15) - stats.norm.cdf(e - k * sd, 100, 15)
            if (c <= L) != (hold >= p) and abs(hold - p) > 1e-7: bad.append(('holds', n, p, L, c, hold))
check('A6 the catch level of %d samples (5 runs): each is the reference integral at the sample\'s own k*, rounded up to thousandths, and at 6 levels a sample is counted caught exactly when '
      'the interval drawn at that level holds at least p of the population (%d ties within 1E-6 of a level set aside)' % (nsamp, ties), not bad and ties <= 2, bad[:3])
h = tol(10, 0.9)
check('A7 cqTolHold: the share of N(100, 15) between two values, in percent', abs(h.execute('cqTolHold(75.3272, 124.6728)') - 100 * (stats.norm.cdf(124.6728, 100, 15) - stats.norm.cdf(75.3272, 100, 15))) < 1e-9)
check('A8 the window of a tolerance run is the mean +/- 1.625 k sigma with k the factor at 95 %% (100 +/- %.2f); the panel keeps the t run\'s decimals (1); the band is 100 +/- 1.645 x 15'
      % (1.625 * 15 * k10), abs(G(h, 'cqWR') - (100 + 1.625 * 15 * k10)) < 1e-6 and abs(G(h, 'cqWL') - (100 - 1.625 * 15 * k10)) < 1e-6 and G(h, 'cqVDec') == 1
      and abs(G(h, 'cqTZ') - stats.norm.ppf(0.95)) < 1e-10, (G(h, 'cqWL'), G(h, 'cqWR'), G(h, 'cqVDec')))
check('A9 the critical value kept for a tolerance run is k root n, so the t interval\'s half-width cqCV s / root n is k s', abs(G(h, 'cqCV') - k10 * math.sqrt(10)) < 1e-9 and
      abs(h.execute('cqLimits(100, 12)')[1] - (100 + k10 * 12)) < 1e-9, G(h, 'cqCV'))
check('A10 s = 0 (an interval of no width) is never counted caught: catch level 1000', h.execute('cqTolCat(100, 0)') == 1000)

print('=== S. a tolerance run through the program\'s own sampler')
h = tol(10, 0.9, seed=4)
for _ in range(20): h.execute('cqAddFast(50)')
tot, hit = G(h, 'cqTot'), G(h, 'cqHit')
check('S1 1,000 samples of 10 at 95 %%: %d intervals held at least 90 %% of the population (%.1f %%: within 4 standard errors of 95 %%)' % (hit, 100 * hit / tot),
      tot == 1000 and abs(hit / tot - 0.95) <= 4 * math.sqrt(0.95 * 0.05 / 1000), (tot, hit))
hist = G(h, 'cqHist'); ok = True; rates = []
for L in (800, 900, 990, 999, 500, 950):
    h.execute('cqSetLevel(%d)' % L)
    want = sum(hist[:L - 499])
    rates.append((L, G(h, 'cqHit')))
    if G(h, 'cqHit') != want: ok = False
exp = {800: 0.8, 900: 0.9, 990: 0.99, 999: 0.999, 500: 0.5, 950: 0.95}
check('S2 moving the level moves the tally exactly (the count of samples whose catch level is at or below it), and the rate follows the level: %s' % ', '.join('%g %%: %d' % (L / 10, c) for L, c in rates),
      ok and all(abs(c / 1000 - exp[L]) <= 4.5 * math.sqrt(max(exp[L] * (1 - exp[L]), 0.0005) / 1000) for L, c in rates), rates)

print('=== V. the setup, the keys and every way out')
FORM = {'suTr': 100, 'suSD': 15, 'suNn': 10, 'suLv': 0.95}
h, res, err = run(lambda h: h.choose(0))
check('V1 Esc at "Which interval?" at the start: the run ends with "CICatcher: no interval chosen"', err is None and res == 'CICatcher: no interval chosen', (err, res))
h, res, err = run(lambda h: (h.choose(6), h.choose(0)))
c = h.chooses
check('V2 item 6 is "Tolerance: %s %s k s" (6 items, none over 30 characters); Esc at "Tolerance: hold how much?" ends the setup with nothing chosen' % (XB, PM),
      err is None and res == 'CICatcher: no interval chosen' and len(c) == 2 and c[0].items[5] == 'Tolerance: %s %s k s' % (XB, PM) and len(c[0].items) == 6
      and max(len(x) for x in c[0].items) <= 30 and c[1].title == 'Tolerance: hold how much?' and c[1].items == ['90 % of the population', '95 % of the population', '99 % of the population'], (err, res, [x.items for x in c]))
h, res, err = run(lambda h: (h.choose(6), h.choose(2), h.answer(CANCEL)))
check('V3 Cancel on the form after choosing 95 %: nothing chosen', err is None and res == 'CICatcher: no interval chosen' and G(h, 'cqTol') == 0, (err, res))


def s_bad(h):
    h.choose(6); h.choose(1)
    h.answer(dict(FORM, suSD=0)); h.answer(dict(FORM, suNn=1)); h.answer(dict(FORM, suLv=0.3)); h.answer(dict(FORM, suTr=20000)); h.answer(FORM)
    h.press('Esc')
h, res, err = run(s_bad)
mb = [' '.join(m.lines) for m in h.msgboxes]
check('V4 the form refuses sigma = 0, n = 1, a level of 0.3 and a mean of 20,000, each with its sentence, and comes back; then takes good values',
      err is None and len(mb) == 4 and 'must be greater than 0' in mb[0] and 'whole number from 2 to 100' in mb[1] and 'level must be from 0.50 to 0.999' in mb[2] and '10,000' in mb[3]
      and G(h, 'cqTol') == 1 and res == 'CICatcher: no intervals drawn (tol. 90 %%, %s = 100, %s = 15, n = 10)' % (MU, SG), (err, mb, res))


def s_full(h):
    h.choose(6); h.choose(1); h.answer(FORM)
    h.tap(*K1)                                              # +1, animated
    h.tap(*K2)                                              # +10
    h.tap(*K3)                                              # +50
    h.tap(*K4); h.choose(4)                                 # Conf: 99 %
    h.tap(*K4); h.choose(0)                                 # Conf: Esc
    h.press('Down'); h.press('Up')
    h.drag([(310, 120), (310, 100), (310, 80)])             # the slider
    h.tap(150, 60)                                          # a line: its sample
    h.press('Right'); h.press('Left')
    h.tap(150, 205)                                         # the panel: closes
    h.tap(*K5); h.answer(CANCEL)                            # n: Cancel
    h.tap(*K5); h.answer({'nkN': 1})                        # n: refused
    h.tap(*K5); h.answer({'nkN': 20})                       # n = 20: a fresh run
    h.tap(*K3)
    h.tap(*K6); h.choose(0)                                 # Menu: Esc
    h.tap(*K6); h.choose(2)                                 # Reset the counts
    h.tap(*K2)
    h.tap(*K6); h.choose(3)                                 # Help
    for _ in range(7): h.press('Enter')
    h.press('Esc')
h, res, err = run(s_full, seed=9)
mb = [' '.join(m.lines) for m in h.msgboxes]
picked = [l for s in h.screens for l in s.lines() if ', holds ' in l]
k20 = k_ref(20, 0.9, G(h, 'cqL') / 1000.0)
check('V5 a whole tolerance session (+1, +10, +50, Conf and its Esc, Up and Down, the slider, a picked line and its neighbours, n cancelled, refused and changed, Menu and its Esc, Reset, seven help pages) '
      'runs to its end; n = 1 is refused with its sentence; after n = 20 the factor is the reference\'s for n = 20',
      err is None and len(mb) == 1 and 'n must be a whole number from 2 to 100' in mb[0] and G(h, 'cqN') == 20 and G(h, 'cqTot') == 10
      and abs(G(h, 'cqCV') / math.sqrt(20) / k20 - 1) < 1e-5 and len([s for s in h.screens if s.func == 'cqPage']) == 7, (err, mb, G(h, 'cqN'), G(h, 'cqTot')))
check('V6 a picked line\'s panel reads "%s = ..., s = ...: lo to hi, holds nn.n %%" (%d screens; e.g. %r)' % (XB, len(picked), picked[0] if picked else ''),
      len(picked) >= 3 and all(re.match(XB + r' = [\d.,−-]+, s = [\d.,]+: [\d.,−-]+ to [\d.,−-]+, holds \d+\.\d+ %$', l) for l in picked), picked[:2])
want = 'CICatcher: %d of 10 held at least 90 %% of the population (%s %%) at %s %%, n = 20' % (
    G(h, 'cqHit'), ('%.1f' % (100 * G(h, 'cqHit') / 10)), ('%g' % (G(h, 'cqL') / 10)))
check('V7 the closing line of a tolerance run says what was counted: %r' % res, res == want and G(h, 'CQ_TOTAL') == 10 and abs(G(h, 'CQ_COVER') - G(h, 'cqHit') / 10) < 1e-12, (res, want))


def box_lines(name, res, width=26):
    """what a program returns, as the Program Catalog's box shows it after a run: the name, the line in quotes, wrapped
    by words.  Width 26 reproduces the five lines seen on the Virtual Calculator on 15 Nov 2026 for the first wording
    ('CICatcher "CICatcher: 107' / 'of 111 tolerance intervals' / 'held at least 95 % of the' / 'population (96.4 %) at
    95' / '%, tol. 95 %, mu = 100, sigma ='), where the box ended and the rest was lost."""
    out, cur = [], ''
    for w in ('%s "%s"' % (name, res)).split(' '):
        if cur and len(cur) + 1 + len(w) > width: out.append(cur); cur = w
        else: cur = (cur + ' ' + w) if cur else w
    return out + [cur]


first = 'CICatcher: 107 of 111 tolerance intervals held at least 95 %% of the population (96.4 %%) at 95 %%, tol. 95 %%, %s = 100, %s = 15, n = 10; see CQ_COVER' % (MU, SG)
bl = box_lines('CICatcher', first)
runs_ = [(107, 111, '96.4', 10), (1000, 1000, '100.0', 10), (9612, 10000, '96.1', 100), (3, 3, '100.0', 2)]
lens = []
for hit, tot, pc, n_ in runs_:
    line_ = 'CICatcher: %s of %s held at least 95 %% of the population (%s %%) at 99.9 %%, n = %d' % (format(hit, ','), format(tot, ','), pc, n_)
    lens.append(len(box_lines('CICatcher', line_)))
check('V7b the closing line in the Program Catalog\'s box (five lines, words wrapped at 26 characters, as seen on the Virtual Calculator): the first '
      'wording took %d lines, and its fifth ended "%s", as the calculator showed; the line as filed takes %s lines for runs of 111, 1,000, 10,000 and 3 '
      'intervals (the widest level, 99.9 %%)' % (len(bl), bl[4][-12:], lens),
      len(bl) == 6 and bl[4].endswith(SG + ' =') and bl[1] == 'of 111 tolerance intervals' and max(lens) <= 5, (bl, lens))
# a red line's share reads below the share it was to hold: a sample made to hold a little under 90 %
h = tol(10, 0.9); h.execute('cqAdd1()')
k = G(h, 'cqCV') / math.sqrt(10)
sd_ = 15 * stats.norm.ppf(0.5 + 0.89996 / 2) / k                      # centred on the mean, holding 89.996 %
S(h, 'cqEst', [100.0] + list(G(h, 'cqEst'))[1:]); S(h, 'cqSd', [float(sd_)] + list(G(h, 'cqSd'))[1:])
S(h, 'cqCat', [float(h.execute('cqTolCat(100, %r)' % float(sd_)))] + list(G(h, 'cqCat'))[1:]); S(h, 'cqSel', 1.0)
h.reset_records(); h.execute('cqDraw()')
line = [l for l in h.screens[-1].lines() if 'holds' in l]
check('V8 a red line that holds 89.996 %% of the population says so with enough decimals to read below 90 (%r), never "holds 90.0 %%"' % (line[0] if line else ''),
      len(line) == 1 and line[0].endswith('holds 89.996 %') and G(h, 'cqCat')[0] > 950, (line, G(h, 'cqCat')[0]))


def s_back(h):
    h.choose(6); h.choose(3); h.answer(FORM); h.tap(*K2)
    h.tap(*K6); h.choose(1); h.choose(2); h.answer(FORM)      # Menu > New: a t interval
    h.tap(*K2); h.tap(150, 40)
    h.tap(*K6); h.choose(1); h.choose(6); h.choose(0)         # Menu > New > Tolerance > Esc: the t run is kept
    h.tap(*K6); h.choose(1); h.choose(6); h.choose(2); h.answer(CANCEL)   # ... > 95 % > Cancel: kept too
    h.press('Esc')
h, res, err = run(s_back, seed=2)
last = [s for s in h.screens if s.func == 'cqLoop'][-1]
check('V9 from a tolerance run, Menu > New > t gives a t run again (its green truth line, "t, ..." in the header, "caught" or "missed by" in the panel); Esc at the tolerance menu and Cancel on its form keep that t run',
      err is None and G(h, 'cqTol') == 0 and G(h, 'cqType') == 2 and G(h, 'cqTot') == 10 and res.startswith('CICatcher: ') and ' caught the truth (' in res and ', t, ' in res
      and any('caught' in l or 'missed by' in l for l in last.lines()) and not any('holds' in l for l in last.lines()), (err, res, last.lines()[-3:]))

print('=== R. regression against beta 2k')


def old_session(ty, form):
    def s(h):
        h.choose(ty); h.answer(form)
        h.tap(*K1); h.tap(*K2); h.tap(*K3)
        h.tap(*K4); h.choose(2)
        h.press('Up'); h.press('Down'); h.press('Down')
        h.drag([(310, 120), (310, 90), (310, 150)])
        h.tap(150, 60); h.press('Right'); h.tap(150, 100)
        h.tap(*K5); h.answer({'nkN': 25})
        h.tap(*K3)
        h.tap(*K6); h.choose(2)
        h.tap(*K2)
        h.tap(*K6); h.choose(4)
    return s


def flat(h):
    return [(s.func, tuple(s.lines()), len(s.shapes), tuple(s.menu or [])) for s in h.screens if s.func != 'cqPage']
MEAN = {'suTr': 50, 'suSD': 8, 'suNn': 12, 'suLv': 0.9}; PROP = {'suTr': 0.15, 'suNn': 30, 'suLv': 0.95}
diff = []; nscr = 0
for ty in (1, 2, 3, 4, 5):
    form = MEAN if ty <= 2 else PROP
    a = run(old_session(ty, form), OLD, seed=7 + ty); b = run(old_session(ty, form), PROG, seed=7 + ty)
    fa, fb = flat(a[0]), flat(b[0]); nscr += len(fb)
    if a[2] is not None or b[2] is not None or fa != fb or a[1] != b[1] or [' '.join(m.lines) for m in a[0].msgboxes] != [' '.join(m.lines) for m in b[0].msgboxes]:
        kk = next((i for i, (x, y) in enumerate(zip(fa, fb)) if x != y), None)
        diff.append((ty, a[2], b[2], len(fa), len(fb), kk, a[1], b[1]))
check('R1 a session of each of the five old intervals (setup, +1, +10, +50, Conf, the arrows, the slider, picked lines, a new n, Reset, Quit) shows the same %d screens, texts and shapes, '
      'and returns the same line, in beta 2k and beta 2l' % nscr, not diff and nscr > 200, diff[:2])

print('=== H. the help')


def helppages(path, n):
    hh = Harness(path, idle_key=4, home_minus=True)
    hh.press('Enter'); hh.choose(1); hh.answer(FORM); hh.press('Enter'); hh.choose(3)
    for _ in range(n): hh.press('Enter')
    hh.press('Esc')
    hh.execute('CICatcher()')
    return [s for s in hh.screens if s.func == 'cqPage']
po = helppages(OLD, 6); pn = helppages(PROG, 7)
check('H1 seven help pages, titled "CICatcher help n/7: ..."', len(pn) == 7 and all(pn[i].lines()[0].startswith('CICatcher help %d/7: ' % (i + 1)) for i in range(7)), [p.lines()[0] for p in pn])
pairs = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (5, 6)]
same = [(i, j) for i, j in pairs if [re.sub(r'help \d/6', 'help N', l) for l in po[i].lines()] != [re.sub(r'help \d/7', 'help N', l) for l in pn[j].lines()]]
check('H2 beta 2k\'s six pages are pages 1 to 4, 6 and 7 word for word (the count in the header aside)', not same, same)
want5 = ['CICatcher help 5/7: Tolerance intervals',
         'A confidence interval is about a mean.  A tolerance interval is',
         'about single values: %s %s k s is made to hold at least 90 %% (or' % (XB, PM),
         '95 %, or 99 %) of the whole population.',
         'The green band is the middle 90 % of the population.  A blue',
         'line holds at least 90 % of the population; a red line holds less.',
         'Tap a line: the panel says how much of the population it holds.',
         'The level is the share of samples whose line holds its 90 %:',
         "the 'all' rate at the top settles near it.",
         'k is larger than z = 1.645 because %s and s are estimates: at' % XB,
         'n = 10 and 95 %, k = 2.856.  k is worked out exactly here;',
         'printed tables often give an approximation that differs in the',
         'third digit.',
         'any key or tap = next page, Esc = done']
check('H3 page 5, Tolerance intervals, reads as written', [l for l in pn[4].lines() if l] == want5, [l for l in pn[4].lines() if l and l not in want5])
wide = [(l, px(l)) for p in pn for l in p.lines()[1:] if px(l) > 296]
check('H4 every help line fits its 296 px at the measured glyph widths (widest %d px); no page has more than 14 lines of text' % max(px(l) for p in pn for l in p.lines()[1:]),
      not wide and all(len([t for t in p.texts if 20 < t.y < 215]) <= 14 for p in pn), wide[:3])

print('=== G. static')
code = '\n'.join(re.sub(r'"[^"\n]*"', '""', l.split('//')[0]) for l in SRC.split('\n'))
check('G1 no "!=" in the code, and the code outside strings and comments is ASCII', '!=' not in code and all(ord(c) < 128 for c in code))
loc = [l for l in SRC.split('\n') if re.match(r'\s*LOCAL\s', l)]
check('G2 every LOCAL line names at most 6 variables (%d lines)' % len(loc), all(len(l.split('//')[0].replace('LOCAL', '').split(',')) <= 6 for l in loc))
check('G3 the header names beta 2l and its date', '// CICATCHER - beta 2l' in SRC and '// beta 2l (15 Nov 2026): Round 16' in SRC)
gx, gw = np.polynomial.legendre.leggauss(12)
mx = re.search(r'tsX := \{([^}]*)\};', SRC); mw = re.search(r'tsW := \{([^}]*)\};', SRC)
check('G4 the six nodes and weights written in cqTolSet are NumPy\'s 12-point Gauss-Legendre rule to 12 digits',
      bool(mx and mw) and np.allclose([float(v) for v in mx.group(1).split(',')], gx[6:], atol=6e-13, rtol=0) and np.allclose([float(v) for v in mw.group(1).split(',')], gw[6:], atol=6e-13, rtol=0))

print('=== D. layout over every beta 2l screen above')
firm = []
for t, f in OV.report().items():
    firm += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
rep_ = sorted(set((x[0], x[3], x[4]) for v in LF.clipped(OV.RECORDS).values() for x in v))
cut = [(t, px(t, int(f)), w) for t, f, w in rep_ if px(t, int(f)) > w]
check('D1 no firm overlap and no text off the screen (text_overlap_v1)', not firm, firm[:4])
check('D2 no number cut short by its width argument (label_fit_v1 reports %d texts at its estimate; none is wider than its width argument at the measured glyph widths)' % len(rep_), not cut, cut[:4])

# D3: a CHOOSE title shows 31 characters on the calculator (tools/prime_facts_v1.py, fact 4); the harness keeps every
# title a program showed in any run above, and each one longer than that.
_new = os.path.basename(PROG); _cut = sorted(set(t for t, sh_, fn_, f_ in Harness.cut_titles if f_ == _new))
check('D3 no menu title of this version is longer than the 31 characters a CHOOSE box shows (%d different titles in the runs above)'
      % len(Harness.shown_titles.get(_new, ())), not _cut and len(Harness.shown_titles.get(_new, ())) >= 1, _cut[:4])
print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
