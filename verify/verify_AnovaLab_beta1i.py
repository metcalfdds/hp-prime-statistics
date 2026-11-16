#!/usr/bin/env python3
"""verify_AnovaLab_beta1i.py -- checks AnovaLab beta 1i (Round 16, 15 Nov 2026): Dunnett's test of every group against
one control (its engine, its two pages, every way in and out), ten help pages, and everything else as beta 1h had it.
Runs from the repository alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, beta 1h
from git (main at 4e8ff66).  Needs hp-prime-kit (HPKIT), SciPy, NumPy.  About seven minutes.

  T1  verify/round16/make_anovalab_1i.py, run again from beta 1h, makes programs/AnovaLab_beta1i.txt byte for byte.
  A   the arithmetic, every routine called through the harness (rule 19).  The setup for a control (distinct sizes,
      intervals, key); the table of G against a Python replica of the engine and against a fine Gauss-Legendre
      reference; the tail P(max |t| > c) and d crit against both, over 18 sets of group sizes and df 3 to 2,990 (the
      numbers the header and help page 5 print are asserted here); one comparison = the t-test; Dunnett's 1964 table;
      SciPy's dunnett on the presets.
  P   the two pages for three presets, line for line against numbers computed here from the same data; the plot's
      bars, marks, zero line and axis numbers pixel for pixel; the pick by tap and by Up/Down; the state without d crit.
  V   every way in and out: the menu's twelve items, Esc at each menu, "Not now", Esc during the table, during the
      p-values and during d crit, the two refusals with their sentences and nothing changed, the same control again,
      another control, Set alpha (computed again or not), new data, the Left/Right round, Help from the new pages,
      the estimate's wording, numbers too wide or too small for their places.
  R   regression against beta 1h: the monkey, 40 seeds, on beta 1h and on beta 1i with its new entrance shut and beta
      1h's help and opening page; every old one-way page through beta 1i's own menu.
  H   the help: 10 pages; the old pages word for word but their numbers and page 4's new line; every line within its
      pixels; each view's Help key opens its own page.
  G   static.     D   layout: text_overlap_v1 and label_fit_v1 over every beta 1i screen drawn above.

  --save   writes the ten help pages to verify/round16/help_AnovaLab_beta1i.txt
"""
import os, sys, io, re, json, math, random, signal, subprocess, tempfile, warnings, collections, time
from decimal import Decimal, ROUND_HALF_UP
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
if not os.path.isdir(os.path.join(REPO, 'programs')): REPO = os.getcwd()
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness, CANCEL  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import numpy as np  # noqa: E402
from scipy import stats, special  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

T00 = time.time()
BASE = '4e8ff66'
PROG = os.path.join('programs', 'AnovaLab_beta1i.txt')
tmp = tempfile.mkdtemp(prefix='avv_')
OLD = os.path.join(tmp, 'AnovaLab_beta1h.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/AnovaLab_beta1h.txt'], check=True, capture_output=True).stdout)
SRC = io.open(PROG, encoding='utf-8').read()
OSRC = io.open(OLD, encoding='utf-8').read()
GW = json.load(open(os.path.join('verify', 'round11', 'glyph_widths_vc.json')))
FAIL, NPASS = [], [0]
MINUS, AL, H0, GE, TX, PM = chr(8722), chr(945), 'H' + chr(8320), chr(8805), chr(215), chr(177)
UD, LR, SCI = chr(8645), chr(8592) + chr(8594), chr(7431)
OV.install()


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
def px(s, font=1): return sum((GW.get(str(ord(ch))) or [8, 9, 10])[int(font) - 1] for ch in s)
def rel(a, b): return abs(a - b) / max(abs(b), 1e-300)


def fx(v, d):
    """a number as the Prime writes it with d decimals: rounded half away from zero, the Prime's minus, commas"""
    q = Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if q == 0: q = abs(q)
    return '{:,f}'.format(q).replace('-', MINUS)


def gn(v):
    """av_Gn: about 5 digits"""
    a = abs(v); d = 4
    if a >= 1: d = 3
    if a >= 10: d = 2
    if a >= 1000: d = 1
    if a >= 100000: d = 0
    return fx(v, d)


def axw(t): return 6 * len(t) - 3 * sum(1 for ch in t if ch in '.,')


def sci(v, d):
    """STRING(v, 3, d) as the Prime writes it: mantissa with d decimals, the small capital E, the exponent"""
    if v == 0: return fx(0, d) + SCI + '0'
    e = int(math.floor(math.log10(abs(v)))); m = Decimal(repr(float(v))) / (Decimal(10) ** e)
    q = m.quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if abs(q) >= 10: q = (q / 10).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP); e += 1
    return ('{:f}'.format(q) + SCI + str(e)).replace('-', MINUS)


def fitn(v, w):
    """av_FitN"""
    a = abs(v)
    if 0.001 <= a < 1e12 or a == 0:
        d = 4
        if a >= 1: d = 3
        if a >= 10: d = 2
        if a >= 1000: d = 1
        if a >= 100000: d = 0
        t = fx(v, d)
        if axw(t) <= w: return t
        while a >= 10 and d > 0:
            d -= 1; t = fx(v, d)
            if axw(t) <= w: return t
    for d in (2, 1, 0):
        t = sci(v, d)
        if axw(t) <= w: return t
    return t


def fits(v, w): return '+' + fitn(v, w - 6) if v > 0 else fitn(v, w)


def ts(v):
    t = fx(v, 3)
    return t if axw(t) <= 40 else fitn(v, 40)


def pt(p): return '< 0.0001' if p < 0.0001 else fx(p, 4)
def pe(p): return 'p < 0.0001' if p < 0.0001 else 'p = ' + fx(p, 4)
def al_s(a): return fx(a, 2) if abs(a - round(a, 2)) < 1e-9 else fx(a, 3)
def cs(c): return (fx(100 * c, 0) if abs(100 * c - round(100 * c)) < 1e-6 else fx(100 * c, 1)) + '%'
def comma(n): return '{:,d}'.format(int(n))


def fresh(path=PROG, d=None):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=d)
    h.execute('av_Init()')
    return h


def run(script, path=PROG, d=None, cls=Harness):
    h = cls(path, idle_key=4, home_minus=True, cas='fail', app_data=d)
    h.press('Enter')                     # the opening page takes the first key
    script(h)
    try: res = h.execute('AnovaLab()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
    return h, res, err


def views(h):
    """the pages the views showed (the screens with soft keys), each as its lines of text, in order, repeats dropped"""
    out = []
    for s in h.screens:
        if s.menu:
            L = [t.text for t in s.texts]
            if not out or out[-1][0] != L or out[-1][1] != s.menu: out.append((L, s.menu, s))
    return out


def call(h, expr):
    """one routine through the harness; what it drew is dropped (thousands of such calls would fill the memory)"""
    r = h.execute(expr)
    del h.screens[:]
    for nm in ('log', 'stat_calls'):
        v = getattr(h, nm, None)
        if isinstance(v, list): del v[:]
    for g in h.grobs.values():
        if isinstance(getattr(g, 'items', None), list): del g.items[:]
    return r


def boxes(h): return [' '.join(m.lines) for m in h.msgboxes]
def titles(h): return [c.title for c in h.chooses]


# ---------------- the references, written here ----------------
def gl(a, b, npan, n=10):
    x, w = np.polynomial.legendre.leggauss(n)
    e = np.linspace(a, b, npan + 1); xs = []; ws = []
    for i in range(npan):
        xs.append((e[i + 1] - e[i]) / 2 * x + (e[i + 1] + e[i]) / 2); ws.append((e[i + 1] - e[i]) / 2 * w)
    return np.concatenate(xs), np.concatenate(ws)


ZN = {}
def z_nodes(bmax, fine=1):
    """Gauss-Legendre points over z in [-9, 9]: 450, twice that for a size ratio over 6.25, four times over 25"""
    k = (1 if bmax <= 2.5 else (2 if bmax <= 5 else 4)) * fine
    if k not in ZN: ZN[k] = gl(-9, 9, 45 * k, 10)
    return ZN[k]


def distinct(n0, ns):
    c = collections.Counter(ns)
    return [(math.sqrt(n / n0), m) for n, m in sorted(c.items())]


def G_ref(y, n0, ns, fine=1):
    """G(y) = INT phi(z) PROD [Phi(b z + y a) - Phi(b z - y a)] dz, for a vector y (fine Gauss-Legendre over z)"""
    dd = distinct(n0, ns); zx, zw = z_nodes(max(b for b, m in dd), fine)
    y = np.atleast_1d(np.asarray(y, float)); out = np.empty(y.size)
    for k in range(0, y.size, 2000):                      # in pieces, to keep the arrays small
        yy = y[k:k + 2000, None]; z = zx[None, :]
        prod = np.ones((yy.shape[0], zx.size))
        for b, m in dd:
            a = math.sqrt(1 + b * b)
            prod *= np.clip(stats.norm.cdf(b * z + yy * a) - stats.norm.cdf(b * z - yy * a), 0, 1) ** m
        out[k:k + 2000] = (stats.norm.pdf(z) * prod * zw[None, :]).sum(axis=1)
    return out


def s_nodes(v, fine=1):
    """points and weights (the density of S folded in) over s: Gauss-Legendre in u = sqrt(s), which puts points
    thickly near 0, where G(c s) turns fastest for a small df; over the spike 1 -/+ 14/sqrt(2 v) for a large one"""
    lo = 1e-12; hi = max(8.0, 1 + 40 / math.sqrt(v))
    if v >= 400: lo = max(1e-12, 1 - 14 / math.sqrt(2 * v)); hi = 1 + 14 / math.sqrt(2 * v)
    ux, uw = gl(math.sqrt(lo), math.sqrt(hi), 80 * fine, 10)
    sx = ux * ux; sw = 2 * ux * uw
    lc = (1 - v / 2) * math.log(2) + (v / 2) * math.log(v) - special.gammaln(v / 2)
    return sx, sw * np.exp(lc + (v - 1) * np.log(sx) - v * sx * sx / 2)


def P_ref(cs_, v, n0, ns, fine=1):
    """the upper tail P(max |t| > c) for each c in cs_: INT f_S(s) (1 - G(c s)) ds, 800 Gauss-Legendre points over s"""
    sx, wd = s_nodes(v, fine); cs_ = np.atleast_1d(np.asarray(cs_, float))
    g = G_ref(np.outer(cs_, sx).ravel(), n0, ns, fine).reshape(len(cs_), len(sx))
    return ((1 - g) * wd[None, :]).sum(axis=1)


def crit_ref(alpha, v, n0, ns, near=None):
    """the c with P_ref(c) = alpha.  With a value near it (the program's own), three tails around that value and
    the straight line through their logs; else Brent's method."""
    if near is not None:
        cc = np.array([near * 0.999, near, near * 1.001]); lp = np.log(P_ref(cc, v, n0, ns))
        if lp[0] > lp[2]:
            c1 = float(np.interp(math.log(alpha), lp[::-1], cc[::-1]))
            if cc[0] < c1 < cc[2]: return c1
    return brentq(lambda c: float(P_ref([c], v, n0, ns)[0]) - alpha, 0.3, 80, xtol=1e-10)


def nz_of(N, n0): return max(16, 2 * int(math.ceil(round(5 * math.sqrt(N / n0), 6))))


class Rep:
    """the engine of section 3b in Python, step for step (a replica; the PPL itself is called through the harness)"""
    def __init__(self, n0, ns):
        self.d = distinct(n0, ns); N = n0 + sum(ns); self.nz = nz_of(N, n0)
        h = 6.0 / self.nz; zs = np.arange(self.nz + 1) * h
        w = np.ones(self.nz + 1); w[1:-1:2] = 4; w[2:-1:2] = 2
        ww = 2 * w * h / 3 * stats.norm.pdf(zs)
        self.tab = np.zeros(71)
        for i in range(1, 71):
            y = i / 10; prod = ww.copy()
            for b, m in self.d:
                a = math.sqrt(1 + b * b); u = b * zs; q = y * a
                dd = np.where(u > q, stats.norm.cdf(q - u) - stats.norm.cdf(-u - q), 1 - stats.norm.cdf(-u - q) - stats.norm.cdf(u - q))
                prod = np.where(dd > 0, prod * dd ** m, 0)
            self.tab[i] = min(1.0, float(prod.sum()))

    def G(self, y):
        if y <= 0: return 0.0
        if y >= 7: return 1.0
        i = min(max(int(y * 10) - 1, 0), 67); t = y * 10 - i
        A, B, C, D = self.tab[i:i + 4]
        r = -A * (t - 1) * (t - 2) * (t - 3) / 6 + B * t * (t - 2) * (t - 3) / 2 - C * t * (t - 1) * (t - 3) / 2 + D * t * (t - 1) * (t - 2) / 6
        return min(1.0, max(0.0, r))

    def tail(self, c, v, ns=64):
        if c <= 0: return 1.0
        w = 8 / math.sqrt(2 * v)
        ulo = math.sqrt(max(0.0, 1 - w)); h = (math.sqrt(1 + w) - ulo) / ns
        e0 = (v - 1) * math.log((v - 1) / v) / 2 - (v - 1) / 2
        num = den = 0.0
        for j in range(ns + 1):
            u = ulo + j * h; s = u * u
            if s <= 0: continue
            f = (1 if j in (0, ns) else (4 if j % 2 else 2)) * u * math.exp((v - 1) * math.log(s) - v * s * s / 2 - e0)
            den += f; num += f * (1 - self.G(c * s))
        return num / den

    def crit(self, alpha, v, ns=64):
        ev = 0
        ql = 0.6; fl = alpha - self.tail(ql, v, ns); ev += 1
        qh = 4.0; fh = alpha - self.tail(qh, v, ns); ev += 1
        while fh < 0 and qh < 60:
            qh *= 1.5; fh = alpha - self.tail(qh, v, ns); ev += 1
        qm = (ql + qh) / 2; sd = 0
        for it in range(40):
            qm = (ql * fh - qh * fl) / (fh - fl)
            fm = alpha - self.tail(qm, v, ns); ev += 1
            if abs(fm) < 1e-7 or abs(qh - ql) < 5e-5: break
            if fm * fl > 0:
                ql, fl = qm, fm
                if sd == -1: fh /= 2
                sd = -1
            else:
                qh, fh = qm, fm
                if sd == 1: fl /= 2
                sd = 1
        self.ev = ev
        return qm


print('=== T. the build')
bd = tempfile.mkdtemp(prefix='avb_')
rb = subprocess.run([sys.executable, os.path.join('verify', 'round16', 'make_anovalab_1i.py'), bd], capture_output=True, text=True)
check('T1 the build makes programs/AnovaLab_beta1i.txt byte for byte', rb.returncode == 0 and open(os.path.join(bd, 'AnovaLab_beta1i.txt'), 'rb').read() == open(PROG, 'rb').read(), rb.stdout[-300:] + rb.stderr[-300:])

print('=== A. the arithmetic')
hA = fresh()
# A0: the reference against itself with twice the points each way, and its straight-line d crit against Brent's method
w0 = 0; w0c = 0
for n0, ns in ((10, [10] * 3), (3, [30, 3, 12, 6]), (1, [99]), (2, [20] * 9), (31, [29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])):
    for v in (3, 33, 2990):
        a_ = P_ref([1.0, 2.5, 4.0, 8.0], v, n0, ns); b_ = P_ref([1.0, 2.5, 4.0, 8.0], v, n0, ns, fine=2)
        w0 = max(w0, max(abs(x - y) / y for x, y in zip(a_, b_) if y > 1e-9))
    c_ = crit_ref(0.05, 12, n0, ns); w0c = max(w0c, rel(crit_ref(0.05, 12, n0, ns, near=c_ * 1.0004), c_))
check('A0 the fine reference (Gauss-Legendre: 450 points and more over z, 800 over s) against itself with twice the points each way: the tails (0.000000001 and more) agree within %.1e of their value; its d crit by a straight line through three tails agrees with Brent\'s method within %.1e'
      % (w0, w0c), w0 < 1e-7 and w0c < 1e-7, (w0, w0c))
def sizes(h, n0, ns):
    setg(h, 'avOK', float(len(ns) + 1)); setg(h, 'avRn', [float(n0)] + [float(x) for x in ns]); setg(h, 'avNN', float(n0 + sum(ns))); setg(h, 'avStop', 0.0)
CONF = [(10, [10] * 2), (10, [10] * 3), (12, [12] * 5), (30, [30] * 11), (38, [39, 37]), (5, [5, 8, 12]), (20, [5, 5, 5]), (4, [16, 25, 9]), (3, [30, 3, 12, 6]),
        (2, [2, 2]), (8, [100, 150]), (2, [50]), (1, [25, 25, 25]), (3, [99, 99, 99]), (1, [99]), (31, [29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]), (50, [2, 3]), (2, [20] * 9)]
# A1: the setup
bad = []; nzs = []
for n0, ns in CONF + [(25, [11]), (4, [4, 4, 4]), (9, [36, 36]), (100, [100] * 8), (7, [1, 1, 1])]:
    sizes(hA, n0, ns); k = call(hA, 'av_DnSetup(1)')
    dd = distinct(n0, ns); B, A_, M = [float(x) for x in G(hA, 'avDnB')], [float(x) for x in G(hA, 'avDnA')], [float(x) for x in G(hA, 'avDnM')]
    got = sorted(zip(B, A_, M)); want = sorted((b, math.sqrt(1 + b * b), float(m)) for b, m in dd)
    N = n0 + sum(ns); nz = int(G(hA, 'avDnNz')); nzs.append(nz)
    if (k != '%d|' % n0 + ''.join('%d,' % x for x in ns) or len(got) != len(want) or any(abs(a - b) > 1e-12 for g, w in zip(got, want) for a, b in zip(g, w))
            or nz != nz_of(N, n0) or nz % 2 or nz < 16 or nz < 10 * math.sqrt(N / n0) - 1e-9 or nz > 10 * math.sqrt(N / n0) + 2 and nz != 16):
        bad.append((n0, ns, k, got, nz))
# the control second, and a control that is not the first group
sizes(hA, 10, [4, 10, 4]); k2 = call(hA, 'av_DnSetup(2)')
check('A1 av_DnSetup over %d sets of sizes: the key is the control\'s size and the others\' in order ("%s" for a control of 4 among 10, 10, 4); the distinct sizes with b = sqrt(n/n0), a = sqrt(1 + b^2) and how many groups share each; the intervals 2 x ceiling(5 sqrt(N/n0)), 16 at least (%d to %d here; 20 for N/n0 = 4 exactly, 30 for 9)'
      % (len(CONF) + 5, k2, min(nzs), max(nzs)),
      not bad and k2 == '4|10,10,4,' and sorted(float(x) for x in G(hA, 'avDnM')) == [1.0, 2.0] and nz_of(16, 4) == 20 and nz_of(81, 9) == 30 and nzs[len(CONF) + 1] == 20 and nzs[len(CONF) + 2] == 30 and max(nzs) == 100, bad[:2])

# A2-A6: the table, the tail and d crit over the 18 sets of sizes
DFS = [3, 4, 6, 12, 30, 33, 100, 101, 400, 2990]
CS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.5, 8.0, 12.0, 25.0]
ALS = [0.2, 0.05, 0.001]
tabP = tabR = 0; giP = 0; tlP = 0; tlAbs = tlRel = tlSm = 0; crP = crR = 0; evs = []; ntail = ncrit = 0; stops = 0; tabs = {}
worstat = None; t0 = time.time()
for n0, ns in CONF:
    sizes(hA, n0, ns); N = n0 + sum(ns)
    ok = call(hA, 'av_DnBuild(1)'); T = [float(x) for x in G(hA, 'avDnT')]
    R = Rep(n0, ns); tabs[(n0, tuple(ns))] = (T, R)
    if ok != 1 or len(T) != 71 or T[0] != 0: stops += 1
    tabP = max(tabP, max(abs(a - b) for a, b in zip(T, R.tab)))
    tabR = max(tabR, float(np.abs(np.array(T[1:]) - G_ref(np.arange(1, 71) / 10, n0, ns)).max()))
    for y in (0.03, 0.17, 0.44, 1.234, 2.5, 3.99, 6.87, 6.95, 7.0, 9.0, 0.0, -1.0):
        giP = max(giP, abs(call(hA, 'av_DnGI(%r)' % y) - R.G(y)))
    for v in sorted(set(DFS + [max(3, N - len(ns) - 1)])):
        ref = P_ref(CS, v, n0, ns)
        for c, pr in zip(CS, ref):
            p = call(hA, 'av_DnTail(%r, %r, 64)' % (c, float(v))); pp = R.tail(c, v); ntail += 1
            if G(hA, 'avStop') != 0: stops += 1; setg(hA, 'avStop', 0.0)
            tlP = max(tlP, abs(p - pp))
            tlAbs = max(tlAbs, abs(p - pr))
            if pr >= 1e-4 and rel(p, pr) > tlRel: tlRel = rel(p, pr); worstat = (n0, ns, v, c, pr)
            if pr < 1e-4: tlSm = max(tlSm, abs(p - pr))
        if v in (3, 30, 2990) or v == N - len(ns) - 1:
            for al in ALS:
                d = call(hA, 'av_DnCrit(%r, %r, 64, 0)' % (al, float(v))); dp = R.crit(al, v); evs.append(R.ev); ncrit += 1
                if G(hA, 'avStop') != 0: stops += 1; setg(hA, 'avStop', 0.0)
                crP = max(crP, rel(d, dp)); crR = max(crR, rel(d, crit_ref(al, v, n0, ns, near=d)))
tA = time.time() - t0
check('A2 the table of G for 18 sets of group sizes (2 to 12 groups, equal and unequal, a control from 1/100 of the values up): the PPL\'s 71 values are the replica\'s (largest difference %.1e), and within %.1e of the fine reference at every table point (the header: within 0.000001)'
      % (tabP, tabR), stops == 0 and tabP < 1e-12 and tabR < 1e-6, (stops, tabP, tabR))
check('A3 av_DnGI: the cubic interpolation at 12 arguments a table, from below 0 to above 7, is the replica\'s (largest difference %.1e); 0 at and below 0, 1 from 7 on' % giP, giP < 1e-12, giP)
check('A4 the tail P(max |t| > c): %s values (18 sets of sizes x df %s and each set\'s own df x c from 0.5 to 25): the PPL is the replica (largest difference %.1e), within %.3f %% of the fine reference wherever the p is 0.0001 or more (the header and help page 5: 0.05 %%; the largest difference, %.5f, is at a p near 0.9), and a p under 0.0001 is never off by more than %.1e, so it prints as "< 0.0001"'
      % (comma(ntail), ', '.join(str(v) for v in DFS), tlP, 100 * tlRel, tlAbs, tlSm), stops == 0 and tlP < 1e-12 and tlRel < 5e-4 and tlAbs < 5e-4 and tlSm < 1e-7, (stops, tlP, tlRel, tlAbs, tlSm, worstat))
check('A5 d crit: %d values (the same sizes; df 3, 30, 2,990 and each set\'s own; alpha 0.2, 0.05, 0.001): the PPL is the replica (%.1e), within %.4f %% of the fine reference (the header: 0.005 %%); the search took %d to %d tails, %d as a rule (the bar says 8 to 22)'
      % (ncrit, crP, 100 * crR, min(evs), max(evs), sorted(evs)[len(evs) // 2]), stops == 0 and crP < 1e-9 and crR < 5e-5 and min(evs) >= 8 and max(evs) <= 22, (crP, crR, min(evs), max(evs)))
print('    (A2-A5: %.0f s)' % tA, flush=True)

# A6: one comparison is the t-test
sizes(hA, 10, [10]); call(hA, 'av_DnBuild(1)'); w6 = w6b = 0
for v in (3, 4, 5, 8, 12, 20, 33, 60, 100, 101, 200, 1000, 2990):
    for c in (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6.5, 8, 12, 20, 40):
        pr = 2 * stats.t.sf(c, v); p = call(hA, 'av_DnTail(%r, %r, 64)' % (float(c), float(v)))
        if pr >= 1e-4: w6 = max(w6, rel(p, pr))
        if pr >= 1e-6: w6b = max(w6b, rel(p, pr))
d6 = [(v, a_, call(hA, 'av_DnCrit(%r, %r, 64, 0)' % (a_, float(v))), stats.t.isf(a_ / 2, v)) for v in (3, 9, 30, 120, 2990) for a_ in (0.2, 0.05, 0.01, 0.001)]
check('A6 with one group beside the control the test is the two-sided t-test: 182 tails against Student\'s t (df 3 to 2,990, c 0.5 to 40) within %.3f %% for a p of 0.0001 or more (%.2f %% down to 0.000001), and d crit is t crit (20 values, alpha 0.2 to 0.001) within %.4f %%'
      % (100 * w6, 100 * w6b, 100 * max(rel(d, t_) for v, a_, d, t_ in d6)), w6 < 5e-4 and w6b < 2e-3 and max(rel(d, t_) for v, a_, d, t_ in d6) < 5e-5, (w6, w6b))

# A7: Dunnett's 1964 table, two-sided 5 %: groups counted with the control, df 10, 20, 60
D64 = {3: (2.57, 2.38, 2.27), 4: (2.76, 2.54, 2.41), 5: (2.89, 2.65, 2.51), 6: (2.99, 2.73, 2.58), 10: (3.24, 2.95, 2.77)}
got7 = {}
for kk, row in D64.items():
    sizes(hA, 8, [8] * (kk - 1)); call(hA, 'av_DnBuild(1)')
    got7[kk] = tuple(call(hA, 'av_DnCrit(0.05, %r, 64, 0)' % float(v)) for v in (10, 20, 60))
check('A7 Dunnett\'s 1964 two-sided 5 %% points, 15 of them (3, 4, 5, 6 and 10 groups with the control; df 10, 20, 60): d crit rounds to every one (3 groups: %s; 10 groups: %s)'
      % (', '.join('%.4f' % x for x in got7[3]), ', '.join('%.4f' % x for x in got7[10])),
      all(abs(round(g, 2) - t_) < 1e-9 for kk in D64 for g, t_ in zip(got7[kk], D64[kk])), got7)

print('=== P. the pages')
BLUE, RED, GRAY, LORN, ORNG = 0x003CC8, 0xFF0000, 0x5A5A5A, 0xFFF0DC, 0xFF4500
def rnd(x): return math.floor(x + 0.5) if x >= 0 else -math.floor(-x + 0.5)       # ROUND(x, 0), half away from zero


def data_of(loader, d=None):
    h = fresh(d=d); call(h, loader)
    return ([float(x) for x in G(h, 'avOY')], [int(x) for x in G(h, 'avOG')], int(G(h, 'avOK')), list(G(h, 'avON')), list(G(h, 'avOSh')))


def dunnett(Y, Gp, k, c, alpha):
    """every group against group c (1 = the first): the sums as the program adds them, the test from the replica"""
    n = [0] * k; m = [0.0] * k; v = [0.0] * k
    for y, g in zip(Y, Gp): n[g - 1] += 1; m[g - 1] += y
    m = [a / b for a, b in zip(m, n)]
    for y, g in zip(Y, Gp): v[g - 1] += (y - m[g - 1]) * (y - m[g - 1])
    ssw = 0.0
    for x in v: ssw += x
    N = len(Y); df = N - k; msw = ssw / df
    oth = [j for j in range(k) if j != c - 1]
    R = Rep(n[c - 1], [n[j] for j in oth]); rows = []
    for j in oth:
        diff = m[j] - m[c - 1]; se = math.sqrt(msw * (1 / n[j] + 1 / n[c - 1])); t = diff / se
        rows.append(dict(j=j, diff=diff, se=se, t=t, p=R.tail(abs(t), df)))
    return dict(rows=rows, d=R.crit(alpha, df), df=df, n=n, m=m, msw=msw, N=N, R=R, c=c, alpha=alpha, n0=n[c - 1], ns=[n[j] for j in oth])


def page6(D, names, sh, d_ok=True, alpha=None):
    a = D['alpha'] if alpha is None else alpha; c = D['c']; mm = len(D['rows'])
    L = ['Dunnett: each group vs a control', 'Control: %s  (n = %s, mean %s)' % (names[c - 1], comma(D['n0']), fitn(D['m'][c - 1], 72))]
    if d_ok:
        L += ['d crit = %s  (%d comparison%s, df = %s, %s = %s)' % (fx(D['d'], 3), mm, '' if mm == 1 else 's', comma(D['df']), AL, al_s(a)),
              'CI = diff %s d crit %s SE;  p = P(largest |t| %s this |t|)' % (PM, TX, GE)]
    else:
        L += ['d crit not computed for %s = %s (not asked for, or Esc).' % (AL, al_s(a)), 'Menu > Dunnett computes it.  The p-values stand.']
    L += ['Group', 'diff', 't', cs(1 - a) + ' CI (family)', 'adj. p']
    for r in D['rows']:
        hw = D['d'] * r['se']
        L += [sh[r['j']], fits(r['diff'], 48), ts(r['t']), '(%s, %s)' % (fitn(r['diff'] - hw, 49), fitn(r['diff'] + hw, 49)) if d_ok else '--', pt(r['p']), '*' if r['p'] < a else '']
    return L + ["diff = its mean - the control's;  red * = differs at %s = %s" % (AL, al_s(a)), '%s = page, %s = a group, Ent = menu, Esc = main menu' % (LR, UD)]


def nice(v):
    if v <= 0: return 1
    e = math.floor(math.log10(v)); f = v / 10 ** e
    return 10 ** e if f <= 1 else (2 * 10 ** e if f <= 2 else (5 * 10 ** e if f <= 5 else 10 ** (e + 1)))


def tk(v, d, st):
    if abs(v) < st / 1000: return '0'
    if d <= 6 and abs(v) < 10000000: return fx(v, d)
    return sci(v, 1).replace('.0' + SCI, SCI)


def page7(D, names, sh, sel=None, d_ok=True, alpha=None):
    """-> (the texts in the order they are drawn, as (text, x, y); the shapes in order, as (cmd, args))"""
    a = D['alpha'] if alpha is None else alpha; c = D['c']; rows = D['rows']; mm = len(rows)
    P = min(40, 122 // mm); H2 = P // 2
    hw = [D['d'] * r['se'] if d_ok else 0 for r in rows]
    lo = min([0] + [r['diff'] - w for r, w in zip(rows, hw)]); hi = max([0] + [r['diff'] + w for r, w in zip(rows, hw)])
    if hi - lo <= 0: lo, hi = -1, 1
    w = (hi - lo) * 0.04; lo -= w; hi += w; sc = 256 / (hi - lo); ya = 36 + mm * P + 2
    X = lambda v: 52 + rnd((v - lo) * sc)
    T = [('Dunnett plot: group minus control', 4, 2)]; S = [('RECT_P', [0, 0, 319, 18, ORNG, ORNG])]
    T.append((('Control: %s.  Bars: %s family CIs (d crit %s).' % (sh[c - 1], cs(1 - a), fx(D['d'], 3))) if d_ok else 'Control: %s.  No bars: d crit is not computed.' % sh[c - 1], 4, 22))
    for i, r in enumerate(rows):
        y = 36 + i * P + H2; col = RED if r['p'] < a else BLUE
        if sel is not None and r['j'] == sel: S.append(('RECT_P', [2, y - H2, 317, y - H2 + P - 1, LORN, LORN]))
        T.append((sh[r['j']], 4, y - 5))
        if d_ok:
            x1 = X(r['diff'] - hw[i]); x2 = X(r['diff'] + hw[i])
            S += [('RECT_P', [x1, y - 1, x2, y + 1, col, col]), ('LINE_P', [x1, y - 3, x1, y + 3, col]), ('LINE_P', [x2, y - 3, x2, y + 3, col])]
        xd = X(r['diff'])
        S += [('RECT_P', [xd - 1, y - 2, xd + 1, y + 2, 0]), ('RECT_P', [xd - 2, y - 1, xd + 2, y + 1, 0])]
        if r['p'] < a: T.append(('*', 311, y - 5))
    S += [('PIXON_P', [X(0), yy, GRAY]) for yy in range(34, ya + 1, 3)]
    S.append(('LINE_P', [52, ya, 308, ya, 0]))
    st = nice((hi - lo) / 8); d = max(0, -math.floor(math.log10(st))); v0 = math.ceil(lo / st) * st; lx = -100; i = 0; ticks = []
    while v0 + i * st <= hi and i < 12:
        x1 = X(v0 + i * st); S.append(('LINE_P', [x1, ya, x1, ya + 2, 0]))
        t = tk(v0 + i * st, d, st); wt = axw(t); x2 = max(2, min(317 - wt, x1 - wt // 2))
        if x2 > lx + 4: T.append((t, x2, ya + 3)); lx = x2 + wt; ticks.append((t, x2, wt))
        i += 1
    T.append((('red = the CI misses 0 (differs at %s = %s);  dotted line = 0' % (AL, al_s(a))) if d_ok else 'red = p < %s = %s (differs);  dotted line = 0' % (AL, al_s(a)), 4, 173))
    if sel is not None:
        r = [q for q in rows if q['j'] == sel][0]; h_ = D['d'] * r['se']
        T.append(('%s - %s = %s;  t = %s;  %s' % (sh[sel], sh[c - 1], fits(r['diff'], 52), ts(r['t']), pe(r['p'])), 4, 184))
        T.append((('%s family CI: %s to %s;  SE %s' % (cs(1 - a), fitn(r['diff'] - h_, 60), fitn(r['diff'] + h_, 60), fitn(r['se'], 52))) if d_ok
                  else 'SE %s;  no CI without d crit (Menu > Dunnett)' % fitn(r['se'], 52), 4, 195))
    else:
        T.append(("Tap a row, or %s, to read a group's numbers." % UD, 4, 184))
    T.append(('%s = page, %s or a tap = a group, Ent = menu' % (LR, UD), 4, 206))
    return T, S, dict(P=P, ya=ya, x0=X(0), ticks=ticks, lo=lo, hi=hi, sc=sc)


def got7(s): return [(t.text, int(t.x), int(t.y)) for t in s.texts], [(q.cmd, [int(x) for x in q.args]) for q in s.shapes]
def norm7(S): return [(c_, [int(x) for x in a_]) for c_, a_ in S]
def dpages(h):
    """Dunnett's pages as the view showed them, in order: a page whose pick alone changed (a band, no text) counts"""
    out = []
    for s in h.screens:
        if s.menu and s.texts and s.texts[0].text.startswith('Dunnett'):
            kk = got7(s)
            if not out or out[-1][3] != kk: out.append(([t.text for t in s.texts], s.menu, s, kk))
    return out
def colors(s): return [int(t.color) for t in s.texts]

PRE = {'ins': ('av_LdInsect()', 4, 1), 'jury': ('av_LdJury1()', 1, 2), 'draft': ('av_LdDraft()', 3, 12)}
DAT = {}; EXP = {}; RUNS = {}
for nm, (ld, item, ctl) in PRE.items():
    DAT[nm] = data_of(ld); Y, Gp, k, names, sh = DAT[nm]
    EXP[nm] = dunnett(Y, Gp, k, ctl, 0.05)
    # the menu, Dunnett, the control, "Compute it now"; then the plot, Down twice, back to the table
    RUNS[nm] = run(lambda h, item=item, ctl=ctl: (h.choose(5), h.choose(item), h.press('Enter'), h.choose(6), h.choose(ctl), h.choose(1), h.press('Right'), h.press('Down'), h.press('Down'), h.press('Left')))
res = []
for nm in PRE:
    Y, Gp, k, names, sh = DAT[nm]; D = EXP[nm]; h, r_, e_ = RUNS[nm]; dp = dpages(h)
    ok6 = e_ is None and len(dp) == 5 and dp[0][0] == page6(D, names, sh) and dp[4][0] == page6(D, names, sh)
    rows6 = [(int(t.x), int(t.y)) for t in dp[0][2].texts][9:9 + 6 * len(D['rows'])]
    okpos = rows6 == [(x, 72 + 11 * i) for i in range(len(D['rows'])) for x in (4, 44, 96, 138, 250, 308)]
    cl = colors(dp[0][2])[9:9 + 6 * len(D['rows'])]
    okcol = all(cl[6 * i:6 * i + 6] == ([RED] * 6 if r['p'] < 0.05 else [0] * 3 + [0, 0, 0]) for i, r in enumerate(D['rows']))
    # the p-values and d crit against the fine reference
    pr = P_ref([abs(r['t']) for r in D['rows']], D['df'], D['n0'], D['ns']); worst = max(rel(r['p'], q) for r, q in zip(D['rows'], pr) if q >= 1e-4) if any(q >= 1e-4 for q in pr) else 0
    dref = crit_ref(0.05, D['df'], D['n0'], D['ns'], near=D['d'])
    res.append((nm, ok6, okpos, okcol, worst, rel(D['d'], dref), len(D['rows']), dp[0][0][1], dp[0][0][2]))
check('P1 page 6, the table, for three presets through the menu (insect sprays against Spray A, 5 rows; the mock jury against Average, 2 rows, unequal n; the draft lottery against December, 11 rows): every line as computed here from the same data (%s | %s | %s ...), the rows 11 pixels apart from y = 72 at x = 4, 44, 96, 138, 250, 308, red with a star exactly where p < 0.05; the p-values within %.3f %% of the fine reference and d crit within %.4f %%'
      % (res[0][7], res[0][8], ' '.join(page6(EXP['ins'], DAT['ins'][3], DAT['ins'][4])[9:15]), 100 * max(r[4] for r in res), 100 * max(r[5] for r in res)),
      all(r[1] and r[2] and r[3] for r in res) and max(r[4] for r in res) < 5e-4 and max(r[5] for r in res) < 5e-5 and [r[6] for r in res] == [5, 2, 11], [(r[0], r[1], r[2], r[3]) for r in res])

# P2: SciPy's dunnett on the same samples (randomized quasi-Monte Carlo: about three decimals)
w2 = 0; n2 = 0
for nm in PRE:
    Y, Gp, k, names, sh = DAT[nm]; D = EXP[nm]
    smp = [[y for y, g in zip(Y, Gp) if g == j + 1] for j in range(k)]
    sp = stats.dunnett(*[smp[r['j']] for r in D['rows']], control=smp[D['c'] - 1], random_state=np.random.default_rng(5))
    for r, q, st_ in zip(D['rows'], sp.pvalue, sp.statistic):
        w2 = max(w2, abs(r['p'] - q)); n2 += 1
        if abs(st_ - r['t']) > 1e-9 * max(1, abs(st_)): w2 = 9
check('P2 SciPy\'s stats.dunnett on the same three sets of samples: the %d t statistics are the program\'s and its p-values (from a randomized integration, good to about three decimals) are within %.4f of ours' % (n2, w2), n2 == 18 and w2 < 0.002, w2)

# P3: page 7, the plot: every text and every shape where the arithmetic puts it
res = []
for nm in PRE:
    Y, Gp, k, names, sh = DAT[nm]; D = EXP[nm]; h, r_, e_ = RUNS[nm]; dp = dpages(h)
    j1 = D['rows'][0]['j']; j2 = D['rows'][1]['j']
    okall = True; info = None
    for pg, sel in ((dp[1], None), (dp[2], j1), (dp[3], j2)):
        T, S, info = page7(D, names, sh, sel=sel)
        gt, gs = got7(pg[2])
        if gt != T or gs != norm7(S): okall = False; res.append((nm, sel, [x for x in zip(gt, T) if x[0] != x[1]][:2], [x for x in zip(gs, norm7(S)) if x[0] != x[1]][:2], len(gs), len(S)))
    tks = info['ticks']
    oktk = all(2 <= x and x + w <= 317 for t, x, w in tks) and all(b[1] > a[1] + a[2] + 4 for a, b in zip(tks, tks[1:])) and len(tks) >= 3
    res.append((nm, 'ok' if okall and oktk else 'BAD', info['P'], info['ya'], info['x0'], [t for t, x, w in tks]))
good = [r for r in res if r[1] == 'ok']
check('P3 page 7, the plot, for the same three (before a pick and with the first and the second row picked): every text at its place and every shape as the scale puts it: the band of the picked row, a 3-pixel bar from one end of each CI to the other with its two caps, red where p < 0.05 and blue otherwise, the black mark at the difference, the dotted line at 0, the axis under the last row, its ticks at a round step and their numbers (sprays: %s; jury: %s; draft: %s), none touching the next and all on the screen; rows of %s pixels for 5, 2 and 11 groups'
      % (', '.join(good[0][5]) if good else '', ', '.join(good[1][5]) if len(good) > 1 else '', ', '.join(good[2][5]) if len(good) > 2 else '', ', '.join(str(r[2]) for r in good)),
      len(good) == 3 and len(res) == 3 and [r[2] for r in good] == [24, 40, 11], [r for r in res if r[1] != 'ok'][:2])

# P4: the pick, by Up/Down and by a tap, on both pages
def sel_of(pg, k):
    """the picked group's row on a Dunnett page, from its light band (None when there is none)"""
    b = [q.args for q in pg[2].shapes if q.cmd == 'RECT_P' and len(q.args) == 6 and int(q.args[4]) == LORN and int(q.args[0]) == 2]
    return None if not b else int(b[0][1])
hk, rk_, ek = run(lambda h: (h.choose(5), h.choose(4), h.press('Enter'), h.choose(6), h.choose(3), h.choose(1),
                             h.press('Down'), h.press('Down'), h.press('Down'), h.press('Down'), h.press('Down'), h.press('Down'), h.press('Up'), h.press('Up'), h.press('Up'), h.press('Up'), h.press('Up'),
                             h.press('Right'), h.tap(160, 36 + 24 * 3 + 5), h.tap(20, 36), h.tap(300, 36 + 24 * 5 - 1), h.tap(160, 36 + 24 * 5), h.tap(160, 30), h.press('Left'), h.tap(100, 71 + 11 * 2 + 3), h.tap(100, 71 + 11 * 5), h.tap(100, 70)))
dk = dpages(hk); D3 = dunnett(*DAT['ins'][:3], 3, 0.05)
seq = [sel_of(p, 6) for p in dk]
# control = Spray C (group 3): the rows are A, B, D, E, F.  Table rows at 72 + 11 i - 1; plot rows at 36 + 24 i
want = [None, 71, 82, 93, 104, 115, 104, 93, 82, 71] + [36 + 24 * 0] + [36 + 24 * 3, 36, 36 + 24 * 4] + [71 + 11 * 4, 71 + 11 * 2]
hu, ru, eu = run(lambda h: (h.choose(5), h.choose(4), h.press('Enter'), h.choose(6), h.choose(3), h.choose(1), h.press('Up'), h.press('Right'), h.press('Up'), h.press('Up')))
du = dpages(hu)
check('P4 the pick (insect sprays, control Spray C, so the rows are A, B, D, E, F): Down goes from no pick to the first row and on to the last, where it stays; Up goes back to the first and stays; the pick is kept from the table to the plot; a tap on a row of the plot or of the table picks that row, and a tap above the rows or under them picks nothing; Up from no pick takes the last row; the picked row\'s numbers are under the plot ("%s" / "%s")'
      % (dk[12][0][-3] if len(dk) > 12 else '', dk[12][0][-2] if len(dk) > 12 else ''),
      ek is None and seq == want and dk[10][0][0].startswith('Dunnett plot') and dk[14][0][0].startswith('Dunnett: each')
      and got7(dk[11][2]) == tuple(x if i else x for i, x in enumerate((page7(D3, DAT['ins'][3], DAT['ins'][4], sel=4)[0], norm7(page7(D3, DAT['ins'][3], DAT['ins'][4], sel=4)[1]))))
      and eu is None and [sel_of(p, 6) for p in du] == [None, 115, 36 + 24 * 4, 36 + 24 * 3, 36 + 24 * 2], (seq, want, [sel_of(p, 6) for p in du]))

# P5: without d crit (Set alpha to 0.01 from the menu, then "Not now"): the p-values stand, no CI, no bars
hn, rn, en = run(lambda h: (h.choose(5), h.choose(1), h.press('Enter'), h.choose(6), h.choose(2), h.choose(1), h.press('Down'), h.press('Enter'), h.choose(10), h.answer({'saV': 0.01}), h.choose(2), h.press('Right')))
dn = dpages(hn); Dj = EXP['jury']; nmj, shj = DAT['jury'][3], DAT['jury'][4]
T5, S5, i5 = page7(Dj, nmj, shj, sel=Dj['rows'][0]['j'], d_ok=False, alpha=0.01)
check('P5 Set %s = 0.01 on page 6 and "Not now" at the question ("%s"): the table keeps its p-values, says "%s" in red and "--" for each CI under "99%% CI (family)", and stars by p < 0.01; the plot has the marks and no bars, "%s", and "%s" for the picked row'
      % (AL, titles(hn)[-2] if len(titles(hn)) > 1 else '', dn[2][0][2] if len(dn) > 2 else '', T5[1][0], T5[-2][0]),
      en is None and len(dn) == 4 and dn[2][0] == page6(Dj, nmj, shj, d_ok=False, alpha=0.01) and got7(dn[3][2]) == (T5, norm7(S5)) and titles(hn)[-2].startswith('Dunnett d crit: about ') and hn.chooses[-2].items == ['Compute it now', 'Not now']
      and int(dn[2][2].texts[2].color) == RED and G(hn, 'avDnD') == -2 and G(hn, 'avAlpha') == 0.01, (len(dn), dn[2][0][:4] if len(dn) > 2 else None))

print('=== V. every way in and out')
K1, K2, K3, K4, K5, K6 = (26, 228), (80, 228), (133, 228), (186, 228), (240, 228), (293, 228)
MENU = ['Table: F, p, effect sizes', 'Checks: equal spreads?', 'Pairs: post hoc tests', 'Dots: groups and CIs', 'F curve and p', 'Dunnett: all vs a control', 'Next method (now Holm)',
        'Tukey p for every pair', 'Tukey p for this pair', 'Set %s (now 0.05)' % AL, 'Help', 'Back to the main menu']
def firsts(h): return [v[0][0] for v in views(h)]
def dts(h): return [t for t in titles(h) if t not in ('AnovaLab: analysis of variance', 'Load a preset', 'Use my data (Statistics 1Var)')]
def state(h): return (G(h, 'avDnC'), G(h, 'avDnD'), G(h, 'avDnKey'), list(G(h, 'avDnP')), G(h, 'avDnSel'))
INS = lambda h: (h.choose(5), h.choose(4))

# V1: the menu's twelve items, each against beta 1h's item that did the same
pairs = []
for old in range(0, 12):
    new = old if old <= 5 else old + 1
    def sc(h, it):
        INS(h); h.press('Right'); h.press('Right'); h.press('Enter'); h.choose(it)
        if old in (7, 8): h.choose(2)                       # Tukey: "Not now"
        if old == 9: h.answer({'saV': 0.1})
        h.press('Right')
    ho, ro, eo = run(lambda h: sc(h, old), path=OLD); hn_, rn_, en_ = run(lambda h: sc(h, new))
    same = (eo is None and en_ is None and ro == rn_ and boxes(ho) == boxes(hn_) and [t for t in titles(ho)] == [t for t in titles(hn_)]
            and [(v[0], v[1]) for v in views(ho)] == [(v[0], v[1]) for v in views(hn_)] and len(ho.inputs) == len(hn_.inputs))
    pairs.append((old, new, same, len(views(hn_))))
hm, rm, em = run(lambda h: (INS(h), h.press('Enter'), h.choose(0), h.tap(*K6), h.tap(*K4), h.choose(12)))
mi = [c.items for c in hm.chooses if c.title == 'One-way ANOVA']
check('V1 the one-way menu (Enter, or More then Menu) has 12 items, "Dunnett: all vs a control" the sixth, so that items 1 to 6 are the six kinds of page; none is over 30 characters; every item of beta 1h does in beta 1i what it did, at its new number (Esc and the 11 old items, each on the Pairs page of the insect sprays: the same pages, boxes, forms and closing line); item 12 leaves for the main menu',
      all(p_[2] for p_ in pairs) and len(pairs) == 12 and em is None and len(mi) == 2 and mi[0] == MENU == mi[1] and max(len(x) for x in MENU) <= 30 and firsts(hm)[-1].startswith('One-way ANOVA'), ([p_ for p_ in pairs if not p_[2]], mi[:1]))

# V2: Esc at the group menu; "Not now" and Esc at the estimate: nothing is computed and the page stays
out = []
for nm, picks in (('Esc at the group menu', [6, 0]), ('"Not now"', [6, 1, 2]), ('Esc at the estimate', [6, 1, 0])):
    h, r_, e_ = run(lambda h: (INS(h), h.press('Right'), h.press('Enter'), [h.choose(x) for x in picks], h.press('Right')))
    f_ = firsts(h)
    out.append((nm, e_ is None and state(h) == (0, -1, '', [], 0) and not boxes(h) and len(f_) == 3 and f_[0].startswith('One-way ANOVA') and f_[1].startswith('Checks') and f_[2].startswith('Pairs') and r_ == RUNS['ins'][1], f_, dts(h)))
check('V2 Esc at the menu of groups ("%s": %s ...), "Not now" at the estimate ("%s"), or Esc there: nothing is computed, no box, the page is the one it was, and Right then goes on as before (no Dunnett page in the round)'
      % (out[0][3][-1], ', '.join(RUNS['ins'][0].chooses[3].items[:2]), out[1][3][-1]),
      all(o[1] for o in out) and out[0][3] == ['One-way ANOVA', 'Dunnett: which is the control?'] and out[1][3] == out[2][3] == ['One-way ANOVA', 'Dunnett: which is the control?', 'Dunnett: about 37-112 s on a G1']
      and RUNS['ins'][0].chooses[3].items[0] == 'Spray A (n 12, s 4.719)' and max(len(x) for x in RUNS['ins'][0].chooses[3].items) <= 30, out)

# V3: Esc while it computes: during the table, during the p-values, during d crit
def esc_at(npoll):
    def sc(h):
        INS(h); h.press('Enter'); h.choose(6); h.choose(1); h.choose(1)
        for _ in range(npoll - 1): h.press('Up', anytime=True)
        h.press('Esc', anytime=True)
    return run(sc)
h31, r31, e31 = esc_at(10); h32, r32, e32 = esc_at(45); h33, r33, e33 = esc_at(75)
D1 = EXP['ins']; d33 = dpages(h33)
check('V3 Esc while Dunnett\'s test computes (insect sprays, 5 groups against Spray A; the keyboard is read at each of the table\'s 70 values and 9 times a tail, and the harness hands over a pressed key at every second reading; Esc as the 10th, the 45th and the 75th key).  During the table: the box "%s", nothing kept, no table.  During the third p-value: the same box, no result, but the table is kept under its key "%s".  During d crit: no box; the five p-values stand and the table page opens with "%s" and "--" for each CI'
      % (boxes(h31)[0] if boxes(h31) else '', state(h32)[2], d33[0][0][2] if d33 else ''),
      e31 is None and e32 is None and e33 is None and boxes(h31) == boxes(h32) == ["Stopped (Esc): Dunnett's test was not computed."] and not boxes(h33)
      and state(h31) == (0, -1, '', [], 0) and state(h32)[:2] == (0, -1) and state(h32)[2] == '12|12,12,12,12,12,' and state(h32)[3] == [] and not dpages(h31) and not dpages(h32)
      and state(h33)[:3] == (1, -2, '12|12,12,12,12,12,') and len(d33) >= 1 and d33[0][0] == page6(D1, DAT['ins'][3], DAT['ins'][4], d_ok=False)
      and [round(x, 12) for x in state(h33)[3][1:]] == [round(r['p'], 12) for r in D1['rows']], (boxes(h31), boxes(h32), boxes(h33), state(h32)[:3], state(h33)[:3]))

# V4: after an Esc during d crit, the menu's Dunnett with the same control asks for d crit alone and finishes the page
h4, r4, e4 = run(lambda h: (INS(h), h.press('Enter'), h.choose(6), h.choose(1), h.choose(1), [h.press('Up', anytime=True) for _ in range(74)], h.press('Esc', anytime=True),
                            h.press('Enter'), h.choose(6), h.choose(1), h.choose(1)))
d4 = dpages(h4)
check('V4 after that Esc, Menu > Dunnett with the same control asks "%s" (d crit alone: the table and the p-values are kept), and "Compute it now" completes the page: d crit = %s as the reference' % (dts(h4)[-1], fx(D1['d'], 3)),
      e4 is None and dts(h4)[-3:] == ['One-way ANOVA', 'Dunnett: which is the control?', 'Dunnett d crit: about 14-41 s on a G1'] and len(d4) == 2 and d4[0][0] == page6(D1, DAT['ins'][3], DAT['ins'][4], d_ok=False)
      and d4[1][0] == page6(D1, DAT['ins'][3], DAT['ins'][4]) and abs(G(h4, 'avDnD') - D1['d']) < 1e-9, (dts(h4), [p_[0][2] for p_ in d4]))

# V5: the two refusals
h51, r51, e51 = run(lambda h: (h.choose(6), h.choose(1), h.press('Enter'), h.choose(6), h.press('Right')), d={'D1': [1.0, 2.0], 'D2': [3.0, 5.0]})
big = {'D1': [5.0, 7.0], 'D2': [float(10 + (i * 7) % 13) for i in range(250)], 'D3': [float(20 + (i * 5) % 11) for i in range(60)]}
h52, r52, e52 = run(lambda h: (h.choose(6), h.choose(1), h.press('Enter'), h.choose(6), h.choose(1), h.press('Right')), d=big)
h53, r53, e53 = run(lambda h: (h.choose(6), h.choose(1), h.press('Enter'), h.choose(6), h.choose(2), h.choose(1)), d=big)
lim = {'D1': [5.0, 7.0, 6.0], 'D2': [float(10 + (i * 7) % 13) for i in range(297)]}
h54, r54, e54 = run(lambda h: (h.choose(6), h.choose(1), h.press('Enter'), h.choose(6), h.choose(1), h.choose(2)), d=lim)
check('V5 what the engine cannot do is refused with a sentence and nothing changes.  Two lists of 2 values (N - k = 2): "%s", with no menu of groups.  A control of 2 values among 312: "%s"; D2 as the control is taken (%s).  A control of 3 among 300, exactly 1/100, is taken too (the estimate: "%s")'
      % (boxes(h51)[0] if boxes(h51) else '', boxes(h52)[0] if boxes(h52) else '', dpages(h53)[0][0][1] if dpages(h53) else '', dts(h54)[-1]),
      e51 is None and e52 is None and e53 is None and e54 is None
      and boxes(h51) == ["Dunnett's test needs df within %s 3 here (the PPL engine): N - k is 2." % GE] and dts(h51) == ['One-way ANOVA'] and state(h51) == (0, -1, '', [], 0) and firsts(h51)[-1].startswith('Checks')
      and boxes(h52) == ["Dunnett's test here needs a control group with at least 1/100 of all the values: D1 has 2 of 312."] and state(h52) == (0, -1, '', [], 0) and firsts(h52)[-1].startswith('Checks')
      and not any('about' in t for t in titles(h52)) and not boxes(h53) and len(dpages(h53)) == 1 and dpages(h53)[0][0][1].startswith('Control: D2  (n = 250')
      and not boxes(h54) and dts(h54)[-1].startswith('Dunnett: about ') and G(h54, 'avDnNz') == 100, (boxes(h51), boxes(h52), dts(h54)))

# V6: the same control again (no question); another control (a question, and the table kept when the sizes are the same)
h6, r6, e6 = run(lambda h: (INS(h), h.press('Enter'), h.choose(6), h.choose(1), h.choose(1), h.press('Left'), h.press('Enter'), h.choose(6), h.choose(1), h.press('Left'), h.press('Enter'), h.choose(6), h.choose(6), h.choose(1)))
t6 = dts(h6); D6 = dunnett(*DAT['ins'][:3], 6, 0.05); d6_ = dpages(h6); f6 = [x[:9] for x in firsts(h6)]
check('V6 Menu > Dunnett again with the same control: no question, the table page at once.  With another control (Spray F): the question again, "%s" (less than the first, "%s": the groups are all of 12, so the table already there is the one needed), and the page is the reference\'s for Spray F (%s | %s)'
      % (t6[-1], t6[2], d6_[-1][0][1], ' '.join(d6_[-1][0][9:15])),
      e6 is None and t6 == ['One-way ANOVA', 'Dunnett: which is the control?', 'Dunnett: about 37-112 s on a G1', 'One-way ANOVA', 'Dunnett: which is the control?', 'One-way ANOVA', 'Dunnett: which is the control?', 'Dunnett: about 19-56 s on a G1']
      and f6 == ['One-way A', 'Dunnett: ', 'F(5, 66):', 'Dunnett: ', 'F(5, 66):', 'Dunnett: '] and len(d6_) == 2 and d6_[0][0] == page6(EXP['ins'], DAT['ins'][3], DAT['ins'][4]) and d6_[1][0] == page6(D6, DAT['ins'][3], DAT['ins'][4]), (t6, f6, len(d6_)))

# V7: Set alpha, computed again: on page 6 from the menu; from the main menu, where the question waits for page 6
D01 = dunnett(*DAT['ins'][:3], 1, 0.01)
h71, r71, e71 = run(lambda h: (INS(h), h.press('Enter'), h.choose(6), h.choose(1), h.choose(1), h.press('Enter'), h.choose(10), h.answer({'saV': 0.01}), h.choose(1), h.press('Right')))
h72, r72, e72 = run(lambda h: (INS(h), h.press('Enter'), h.choose(6), h.choose(1), h.choose(1), h.press('Esc'), h.choose(7), h.answer({'saV': 0.01}), h.choose(1), h.press('Left'), h.press('Left'), h.choose(1), h.press('Left')))
d71 = dpages(h71); d72 = dpages(h72); t72 = titles(h72)
check('V7 Set %s = 0.01 with Dunnett\'s results there.  On page 6, from the menu: the question "%s", then d crit = %s (the reference\'s %s), "99%% CI (family)" and stars by p < 0.01, the p-values as they were; the plot follows.  From the main menu: nothing is asked there; the question comes when page 6 is reached (Left from the Table page to the plot, Left again), and both pages are the reference\'s'
      % (AL, dts(h71)[-1], d71[1][0][2][9:14] if len(d71) > 1 else '', fx(D01['d'], 3)),
      e71 is None and e72 is None and len(d71) == 3 and d71[0][0] == page6(EXP['ins'], DAT['ins'][3], DAT['ins'][4]) and d71[1][0] == page6(D01, DAT['ins'][3], DAT['ins'][4])
      and d71[2][3] == (page7(D01, DAT['ins'][3], DAT['ins'][4])[0], norm7(page7(D01, DAT['ins'][3], DAT['ins'][4])[1])) and dts(h71)[-1] == 'Dunnett d crit: about 14-41 s on a G1'
      and [round(a, 12) for a in G(h71, 'avDnP')[1:]] == [round(r['p'], 12) for r in EXP['ins']['rows']]
      and t72[5] == 'AnovaLab: analysis of variance' and t72[6] == 'AnovaLab: analysis of variance' and t72[7] == 'Dunnett d crit: about 14-41 s on a G1'
      and [p[0][0] for p in d72] == ['Dunnett: each group vs a control', 'Dunnett plot: group minus control', 'Dunnett: each group vs a control'] and d72[2][0] == page6(D01, DAT['ins'][3], DAT['ins'][4])
      and d72[1][3] == (page7(D01, DAT['ins'][3], DAT['ins'][4])[0], norm7(page7(D01, DAT['ins'][3], DAT['ins'][4])[1])), (t72, [p[0][0] for p in d72], len(d71)))

# V8: the arrows: without Dunnett's results as in beta 1h; with them its two pages stand between F and Table
h81, r81, e81 = run(lambda h: (INS(h), h.press('Left'), h.press('Right'), h.press('Right'), h.press('Right'), h.press('Right'), h.press('Right'), h.tap(*K5), h.press('Left')))
h82, r82, e82 = run(lambda h: (INS(h), h.press('Enter'), h.choose(6), h.choose(1), h.choose(1), h.press('Right'), h.press('Right'), h.press('Left'), h.press('Left'), h.press('Left'), h.press('Right'), h.press('Left'), h.press('Left')))
h83, r83, e83 = run(lambda h: (INS(h), h.press('Enter'), h.choose(6), h.choose(1), h.choose(1), h.press('Esc'), h.choose(5), h.choose(4), h.press('Left'), h.press('Right'), h.press('Enter'), h.choose(6), h.choose(2), h.choose(2)))
def short(h): return [{'One': 'T', 'Che': 'C', 'Pai': 'P', 'Dot': 'D', 'F(5': 'F', 'Dun': 'U'}[f[:3]] + ('p' if f.startswith('Dunnett plot') else '') for f in firsts(h)]
check('V8 the arrows.  Without Dunnett\'s results, as in beta 1h: Left from Table is F, Right from F is Table, then Checks, Pairs, Dots, where Left and Right pick the pair (%s).  With them, Dunnett\'s table and plot stand between F and Table: Right from the table is the plot, then Table; Left from Table the plot, the table, F, and Right from F the table again (%s).  After the same preset is loaded again the results are gone and Left from Table is F again, but the table of G is still there (the question then: "%s")'
      % (' '.join(short(h81)), ' '.join(short(h82)), dts(h83)[-1]),
      e81 is None and e82 is None and e83 is None and short(h81) == list('TFTCPDDFD')
      and short(h82) == ['T', 'U', 'Up', 'T', 'Up', 'U', 'F', 'U', 'F', 'D']
      and short(h83) == ['T', 'U', 'T', 'F', 'T'] and state(h83)[0] == 0 and state(h83)[2] == '12|12,12,12,12,12,' and dts(h83)[-1] == 'Dunnett: about 19-56 s on a G1', (short(h81), short(h82), short(h83)))

# V9: Help, + and -, and the soft keys on Dunnett's pages
h9, r9, e9 = run(lambda h: (INS(h), h.press('Enter'), h.choose(6), h.choose(1), h.choose(1), h.tap(*K6), h.tap(*K3), h.press('Esc'), h.press('Right'), h.press('Enter'), h.choose(11), h.press('Esc'),
                            h.press('Plus'), h.press('Minus'), h.press('Minus'), h.tap(*K6), h.tap(*K1)))
hp9 = [s.texts[0].text for s in h9.screens if s.texts and s.texts[0].text.startswith('AnovaLab help')]
check('V9 on Dunnett\'s pages the Help key (More, Help) and the menu\'s Help open help page 5 ("%s"); + and - change the method of the Pairs page as they do on the Table page and leave this page as it is (Holm, then Scheffe after +, -, -: avMeth = %d); the soft keys are the one-way pages\' (Table goes to the Table page)'
      % (hp9[0] if hp9 else '', int(G(h9, 'avMeth'))),
      e9 is None and len(hp9) == 2 and hp9[0] == hp9[1] == "AnovaLab help 5/10: Dunnett's test" and G(h9, 'avMeth') == 2 and firsts(h9)[-1].startswith('One-way ANOVA')
      and [m for v in views(h9) for m in [tuple(v[1])]][0] == ('Table', 'Checks', 'Pairs', 'Dots', 'F', 'More') and len(dpages(h9)) == 2, (hp9, G(h9, 'avMeth'), firsts(h9)))

# V10: the estimate: its arithmetic, seconds and minutes
def est(n0, ns, ev, have=False):
    u = ev * 65 * 3 + (0 if have else 70 * (nz_of(n0 + sum(ns), n0) + 1) * len(set(ns)) * 2)
    r = lambda x: int(Decimal(repr(x)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    if u * 0.015 >= 120: return 'about %s-%s min on a G1' % (comma(max(1, r(u * 0.005 / 60))), comma(max(2, r(u * 0.015 / 60))))
    return 'about %s-%s s on a G1' % (comma(max(1, r(u * 0.005))), comma(max(2, r(u * 0.015))))
he = fresh(); e10 = []
for n0, ns in CONF:
    sizes(he, n0, ns); setg(he, 'avDnKey', '')
    for ev in (len(ns) + 14, 14):
        e10.append((call(he, 'av_DnEst(1, %d)' % ev), est(n0, ns, ev)))
sizes(he, 12, [12] * 5); call(he, 'av_DnBuild(1)'); e10.append((call(he, 'av_DnEst(1, 19)'), est(12, [12] * 5, 19, have=True)))
kinds10 = collections.Counter('min' if ' min ' in a else 's' for a, b in e10)
check('V10 the estimate shown before a computation, for the 18 sets of sizes with and without the p-values and once with the table already built: units = 195 a tail + 70 x (intervals + 1) x distinct sizes x 2 for a table, at 5 to 15 ms each, in seconds below two minutes (%d of them, as "%s") and in minutes from there (%d, as "%s"); the same wording as Tukey\'s'
      % (kinds10['s'], [a for a, b in e10 if ' s ' in a][0], kinds10['min'], [a for a, b in e10 if ' min ' in a][0]),
      all(a == b for a, b in e10) and len(e10) == 37 and kinds10['s'] > 5 and kinds10['min'] > 5, [x for x in e10 if x[0] != x[1]][:3])

# V11: numbers too wide or too small for their places; one comparison only
rngv = random.Random(11); bigd = {}
for g_ in range(9):
    bigd['D%d' % (g_ + 1)] = [float(round(2500000 + 400000 * (g_ % 4) + rngv.gauss(0, 600000))) for _ in range([8, 5, 12, 7, 20, 6, 9, 15, 4][g_])]
tiny = {'D1': [3.1e-7, 3.4e-7, 2.9e-7, 3.37e-7], 'D2': [4.1e-7, 4.4e-7, 3.9e-7, 4.6e-7], 'D3': [3.0e-7, 3.6e-7, 3.2e-7, 2.7e-7]}
two = {'D1': [12.1, 13.4, 11.8, 14.2, 12.9, 13.3], 'D2': [14.0, 15.2, 13.9, 16.1, 15.5]}
huge = {'D1': [1e40, 3e40, 2e40, 2.6e40], 'D2': [5e40, 9e40, 7e40, 6e40], 'D3': [-4e40, -1e40, -2e40]}
o11 = []
for nm, dd_, ctl in (('millions', bigd, 5), ('ten-millionths', tiny, 1), ('two groups', two, 1), ('1E40', huge, 2)):
    h, r_, e_ = run(lambda h, ctl=ctl: (h.choose(6), h.choose(1), h.press('Enter'), h.choose(6), h.choose(ctl), h.choose(1), h.press('Down'), h.press('Right')), d=dd_)
    Yd, Gd, kd, nmd, shd = data_of('av_MyOne()', d=dd_); Dd = dunnett(Yd, Gd, kd, ctl, 0.05); dp = dpages(h)
    T, S, inf = page7(Dd, nmd, shd, sel=Dd['rows'][0]['j'])
    clip = [t.text for p_ in dp for t in p_[2].texts if px(t.text.replace(SCI, 'E')) > t.width]
    o11.append((nm, e_ is None and len(dp) == 3 and dp[1][0] == page6(Dd, nmd, shd) and dp[2][3] == (T, norm7(S)) and not clip, dp[1][0][9:15] if len(dp) > 1 else None, [t for t, x, w in inf['ticks']], dp[1][0][2] if len(dp) > 1 else None, clip))
check('V11 numbers that do not fit their places as usual.  Nine unequal groups with values in the millions (%s; axis %s); values of a few ten-millionths (%s; axis %s); 1E40 (%s); two groups only ("%s", d crit = t crit %.3f).  Every line and shape is the reference\'s and nothing is cut'
      % (' '.join(o11[0][2]), ', '.join(o11[0][3]), ' '.join(o11[1][2]), ', '.join(o11[1][3]), ' '.join(o11[3][2]), o11[2][4], stats.t.isf(0.025, 9)),
      all(o[1] for o in o11) and o11[2][4] == 'd crit = %s  (1 comparison, df = 9, %s = 0.05)' % (fx(stats.t.isf(0.025, 9), 3), AL), [(o[0], o[1], o[5]) for o in o11])

# V12: what Dunnett's test leaves alone: the closing line and Home's variables
hb, rb_, eb = run(lambda h: (INS(h), h.press('Right')))
ha, ra, ea = RUNS['ins']
homes = ['AV_F', 'AV_P', 'AV_DF', 'AV_MSE', 'AV_ETA2', 'AV_TAB']
check('V12 Dunnett\'s test changes nothing else: the closing line ("%s") and Home\'s AV_F, AV_P, AV_DF, AV_MSE, AV_ETA2 and AV_TAB are the same with and without it' % ra,
      ra == rb_ and all(str(G(ha, v)) == str(G(hb, v)) for v in homes) and ra.startswith('AnovaLab: one-way F(5, 66) = 34.702, p < 0.0001'), (ra, rb_))

print('=== R. regression against beta 1h')
def routine(src, head):
    a = src.index('\n' + head) + 1
    return src[a:src.index('\nEND;\n', a) + 6]
# beta 1i with its new entrance shut: the one-way menu, the help, its three callers elsewhere and the opening page are beta 1h's
SHUT = SRC
for head in ('av_OMenu()\nBEGIN', 'av_HelpPage(hpN)\nBEGIN', 'av_Help(hsN)\nBEGIN', 'av_TView(tvS)\nBEGIN', 'av_BView(bvS)\nBEGIN', 'av_VView()\nBEGIN', 'av_Hello()\nBEGIN'):
    assert SHUT.count(routine(SRC, head)) == 1 and routine(SRC, head) != routine(OSRC, head)
    SHUT = SHUT.replace(routine(SRC, head), routine(OSRC, head))
SHUTP = os.path.join(tmp, 'AnovaLab_beta1i_shut.txt'); io.open(SHUTP, 'w', encoding='utf-8', newline='').write(SHUT)
argv = sys.argv; sys.argv = ['monkey_v1b.py']
import monkey_v1b as MK  # noqa: E402
sys.argv = argv
def one(path, seed):
    rng_ = random.Random(seed)
    app, kind_ = MK.random_lists(rng_)
    hh_ = MK.Monkey(path, rng_, app, 150)
    for q in range(10): hh_.globals_.setdefault('M%d' % q, MK.R.interp.Matrix([[0.0]]))
    m1_, mk = MK.random_matrix(seed)
    if m1_ is not None: hh_.globals_['M1'] = m1_
    verdict = 'OK'
    signal.signal(signal.SIGALRM, MK._alarm); signal.alarm(90)
    try: hh_.execute('AnovaLab()')
    except MK.TimeUp: verdict = 'FREEZE'
    except Exception as e: verdict = 'END ' + type(e).__name__
    finally: signal.alarm(0)
    scr = [tuple((t.text, t.x, t.y) for t in s.texts) for s in hh_.screens]
    return verdict, scr, [' '.join(m_.lines) for m_ in hh_.msgboxes], str(hh_.result), [c.title for c in hh_.chooses]
diffs = []; nscr = 0; verd = {}; kinds = collections.Counter()
for sd in range(1800, 1840):
    a = one(OLD, sd); b = one(SHUTP, sd)
    nscr += len(b[1]); verd[b[0]] = verd.get(b[0], 0) + 1
    for x in b[1]:
        if x: kinds[re.split(r'[:(]', x[0][0])[0].strip()[:22]] += 1
    if a != b:
        k_ = next((i for i, (x, y) in enumerate(zip(a[1], b[1])) if x != y), None)
        diffs.append((sd, a[0], b[0], a[3] == b[3], len(a[1]), len(b[1]), k_))
check('R1 the monkey, 40 seeds, on beta 1h and on beta 1i with its new entrance shut (beta 1h\'s one-way menu, help and opening page): the same verdict (%s), boxes, menus and closing line, and all %s screens the same, every text at its place (%s ...)'
      % (verd, format(nscr, ','), ', '.join('%s %d' % kv for kv in kinds.most_common(7))), not diffs and nscr > 400, diffs[:3])

# R2: every other way in, through beta 1i's own menus, against beta 1h (no menu of the one-way pages and no Help: V1 and H have those)
DD = {'D1': [3.1, 4.7, 5.2, 5.9, 6.3, 7.7, 8.1, 9.6, 12.4], 'D2': [2.9, 5.1, 4.4, 6.6, 6.0, 7.1, 9.3, 9.9, 11.0], 'D3': [3.5, 4.0, 5.9, 5.5, 7.0, 6.9, 8.8, 10.4, 12.0]}
D3w = {'D1': [3.1, 4.7, 5.2, 5.9, 6.3, 7.7, 8.1, 9.6, 12.4, 5.5, 6.1, 7.2], 'D2': [1.0, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2], 'D3': [1.0, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]}
def walk(h, k5=True): return (h.press('Right'), h.press('Right'), h.tap(*K4), h.press('Right'), h.tap(*K3), h.press('Down'), h.press('Plus'), h.press('Minus'), h.tap(150, 100), h.tap(*K2), h.tap(*K1), h.press('Left'),
                              h.tap(*K5) if k5 else h.tap(*K2), h.press('Up'))
def texts(h): return [(tuple((t.text, t.x, t.y) for t in s.texts), tuple(s.menu or ())) for s in h.screens]
# (the fifth soft key is Help on the blocks and variances pages: not pressed there)
ways = [('preset %d' % i, [5, i], None, i != 5) for i in range(1, 6)] + [('your data, one-way', [6, 1], DD, True), ('your data, two-way', [6, 2], D3w, True), ('your data, blocks', [6, 3], DD, False),
                                                                        ('variances', [4, 1, 1], None, False), ('one-way', [1], None, True), ('two-way', [2], None, True), ('blocks', [3], None, False)]
pairs = []
for nm, pick, dd_, k5 in ways:
    sc = lambda h: ([h.choose(p_) for p_ in pick], walk(h, k5))
    ho_, ro_, eo_ = run(sc, path=OLD, d=dd_); hn_, rn_, en_ = run(sc, d=dd_)
    pairs.append((nm, eo_ is None and en_ is None and ro_ == rn_ and texts(ho_)[1:] == texts(hn_)[1:] and boxes(ho_) == boxes(hn_) and titles(ho_) == titles(hn_) and len(texts(hn_)) >= 6, len(texts(hn_)), ro_ == rn_))
check('R2 every other way in, through beta 1i\'s own main menu against beta 1h\'s: the five presets, three kinds of Your data, the variances, and the three analyses of the data loaded at the start, each walked with the arrows, taps, + and - and the soft keys (%d ways, %s screens): the same screens, every text at its place, the same boxes, menus and closing lines (the opening page, which names the version, aside)'
      % (len(pairs), format(sum(p_[1] for p_ in pairs), ',')), all(p_[1] for p_ in pairs) and len(pairs) == 12, [p_ for p_ in pairs if not p_[1]][:3])

print('=== H. the help')
def help_pages(path, n):
    hh_ = Harness(path, idle_key=4, home_minus=True, cas='fail'); hh_.press('Enter'); hh_.choose(8)
    for _ in range(n): hh_.press('Enter')
    hh_.execute('AnovaLab()')
    out_ = []
    for s in hh_.screens:
        L = [t.text for t in s.texts]
        if L and L[0].startswith('AnovaLab help') and (not out_ or out_[-1][0] != L): out_.append((L, s))
    return out_, hh_
HN, hhn = help_pages(PROG, 10); HO, hho = help_pages(OLD, 9)
TOPICS = ['What one-way ANOVA asks', 'Welch and the checks', 'Which pairs differ?', 'Which pairs differ? (continued)', "Dunnett's test", 'Two-way ANOVA', 'Randomized blocks', 'One and two variances', 'Your data, and Home', 'Credits']
FOOT = 'Any key or tap = next, %s = back, Esc = leave' % chr(8592)
check('H1 the help has 10 pages (beta 1h: %d), each headed "AnovaLab help n/10: <Topic>" and footed "%s"; a key on page 10 leaves' % (len(HO), FOOT),
      len(HN) == 10 and len(HO) == 9 and [p[0][0] for p in HN] == ['AnovaLab help %d/10: %s' % (i + 1, t) for i, t in enumerate(TOPICS)] and all(p[0][-1] == FOOT for p in HN)
      and [p[0][0] for p in HO] == ['AnovaLab help %d/9: %s' % (i + 1, t) for i, t in enumerate(TOPICS[:4] + TOPICS[5:])], [p[0][0] for p in HN])
body = lambda p: p[0][1:-1]
pos = lambda p: [(int(t.x), int(t.y)) for t in p[1].texts]
same = [body(HN[i]) == body(HO[j]) and pos(HN[i]) == pos(HO[j]) for i, j in ((0, 0), (1, 1), (2, 2), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8))]
check('H2 pages 1, 2, 3 and 6 to 10 are beta 1h\'s pages 1, 2, 3 and 5 to 9 word for word, every line at its place; page 4 is its page 4 with one line more, at y = 130: "%s"' % body(HN[3])[-1],
      all(same) and body(HN[3])[:-1] == body(HO[3]) and pos(HN[3])[:-2] == pos(HO[3])[:-1] and body(HN[3])[-1] == "One group is the control?  Dunnett's test: the next page." and pos(HN[3])[-2] == (10, 130), same)
P5 = ["Dunnett's test compares every group with ONE control", 'group (a placebo, the usual method): k - 1 comparisons,', 'not all the pairs.  With fewer comparisons, it finds a', "real difference more often than Tukey's test does.",
      't = (group mean - control mean)/SE, SE from MS within', 'and both n.  A group differs when |t| > d crit, and d crit', 'keeps the chance of ANY false alarm in the family at %s.' % AL,
      'Adjusted p: the chance that the LARGEST |t| of the', 'family is this big when no group differs from the control.',
      'Enter > Dunnett: pick the control.  It asks before it runs', '(slow on a G1).  Two pages: the table, then the CIs drawn.',
      'Two-sided; unequal n allowed.  Choose the control before', 'you see the data.  Dunnett (1955); p within 0.05 %.']
check('H3 page 5 is new: 13 lines in five paragraphs (what the test is; t and d crit; the adjusted p; how to run it; its limits and source), at x = 10 and y = 30 to 198, a new paragraph 16 pixels down and a new line 13',
      body(HN[4]) == P5 and pos(HN[4])[1:-1] == [(10, y_) for y_ in (30, 43, 56, 69, 85, 98, 111, 127, 140, 156, 169, 185, 198)], body(HN[4]))
oldl = set(t for p in HO for t in body(p))
wide = [(i + 1, px(t), t) for i, p in enumerate(HN) for t in body(p) if px(t) > (300 if t in oldl else 296)] + [(i + 1, px(p[0][0], 2), p[0][0]) for i, p in enumerate(HN) if px(p[0][0], 2) > 300]
check('H4 every help line is within the 300 pixels the page gives it at the measured glyph widths (the widest is %d; the widest new line is %d, within 296) and every header too (the widest is %d); no page has more than 13 lines'
      % (max(px(t) for p in HN for t in body(p)), max(px(t) for p in HN for t in body(p) if t not in oldl), max(px(p[0][0], 2) for p in HN)), not wide and max(len(body(p)) for p in HN) <= 13, wide[:3])
# H5: each view's Help opens its own page
def first_help(script, path=PROG, d=None):
    hh_, r_, e_ = run(script, path=path, d=d)
    hp = [s.texts[0].text for s in hh_.screens if s.texts and s.texts[0].text.startswith('AnovaLab help')]
    return hp[0] if hp else None
H5 = [('the main menu', lambda h: h.choose(8), 1, 1), ('one-way, Table', lambda h: (h.choose(1), h.tap(*K6), h.tap(*K3)), 1, 1), ('one-way, Pairs', lambda h: (h.choose(1), h.tap(*K3), h.tap(*K6), h.tap(*K3)), 3, 3),
      ('one-way, Dots', lambda h: (h.choose(1), h.tap(*K4), h.tap(*K6), h.tap(*K3)), 3, 3), ('two-way', lambda h: (h.choose(2), h.press('Enter'), h.choose(7)), 6, 5),
      ('blocks', lambda h: (h.choose(3), h.tap(*K5)), 7, 6), ('variances', lambda h: (h.choose(4), h.choose(1), h.choose(1), h.tap(*K5)), 8, 7)]
got5 = [(nm, first_help(sc), first_help(sc, path=OLD), n_, o_) for nm, sc, n_, o_ in H5]
check('H5 the Help key of each view opens its own page: the main menu and the one-way Table page 1, Pairs and Dots page 3, Dunnett\'s pages page 5 (V9), two-way page 6, blocks page 7, variances page 8: the same topics as in beta 1h, where the last three were pages 5, 6 and 7',
      all(a is not None and b is not None and a.startswith('AnovaLab help %d/10: ' % n_) and b.startswith('AnovaLab help %d/9: ' % o_) and a.split(': ', 1)[1] == b.split(': ', 1)[1] for nm, a, b, n_, o_ in got5), got5)
if '--save' in sys.argv:
    with io.open(os.path.join('verify', 'round16', 'help_AnovaLab_beta1i.txt'), 'w', encoding='utf-8') as f:
        for p in HN: f.write('\n'.join(p[0]) + '\n\n')
    print('    (help pages written to verify/round16/help_AnovaLab_beta1i.txt)')

print('=== G. static')
code = '\n'.join(re.sub(r'"[^"\n]*"', '""', l.split('//')[0]) for l in SRC.split('\n'))
check('G1 no "!=" in the code, and the code outside strings and comments is ASCII', '!=' not in code and all(ord(c) < 128 for c in code))
loc = [l for l in SRC.split('\n') if re.match(r'\s*LOCAL\s', l)]
check('G2 every LOCAL line names at most 6 variables (%d lines)' % len(loc), all(len(l.split('//')[0].replace('LOCAL', '').split(',')) <= 6 for l in loc))
check('G3 the header names beta 1i and its date, the note of beta 1i is there, the opening page shows the version and names the test ("%s")' % [l for l in SRC.split('\n') if 'post hoc, Dunnett' in l][0].split('"')[1],
      '// ANOVALAB - beta 1i  (15 Nov 2026)' in SRC and '// beta 1i (15 Nov 2026): Round 16' in SRC and 'av_Band("AnovaLab - beta 1i");' in SRC and SRC.count('beta 1h"') == 0
      and 'av_Tx("one-way ANOVA (Welch, checks, post hoc, Dunnett),", 10, 40, avBLUE);' in SRC)
ALLH = [RUNS['ins'][0], RUNS['jury'][0], RUNS['draft'][0], hk, hn, hm, h4, h52, h53, h54, h6, h71, h72, h83, h9, hhn]
items = sorted(set(i for hh_ in ALLH for c in hh_.chooses for i in c.items)); ttl = sorted(set(c.title for hh_ in ALLH for c in hh_.chooses))
lit = re.findall(r'"([^"\n]*)"', '\n'.join(m_.group(1) for m_ in re.finditer(r'CHOOSE\([^{;]*\{(.*?)\}\);', SRC, re.S)))
check('G4 every item of every menu is at most 30 characters: the %d different items the runs above were shown (the longest is %r, %d) and the %d quoted pieces of the menus\' items in the source; the longest menu title shown is %r (%d)'
      % (len(items), max(items, key=len), max(len(i) for i in items), len(lit), max(ttl, key=len), max(len(t) for t in ttl)), len(items) >= 40 and max(len(i) for i in items) <= 30 and max(len(i) for i in lit) <= 30, sorted(items, key=len)[-3:])
L_ = SRC.split('\n'); a_ = next(i for i, l in enumerate(L_) if l.startswith('// File map')); mp = []
for l in L_[a_:a_ + 30]:
    m_ = re.match(r'//\s+(\d+)-(\d+|end)\s+(\S.*)$', l)
    if m_: mp.append((int(m_.group(1)), len(L_) - 1 if m_.group(2) == 'end' else int(m_.group(2)), m_.group(3)))
first_ok = all(L_[a - 1].startswith('// ====') or L_[a - 1].startswith('// ---- palette') for a, b, t in mp)
ends_ok = all(b == len(L_) - 1 or L_[b].startswith('// ====') or L_[b].startswith('// ---- palette') or (L_[b - 1].strip() == '' and True) for a, b, t in mp) and all(mp[i][1] + 1 == mp[i + 1][0] for i in range(len(mp) - 1))
check('G5 the file map in the header is true: each of its %d parts begins where the map says (a bar of = signs; the state at its first comment) and ends on the line before the next, the last on the file\'s last line (%d); section 3b, Dunnett\'s engine, is lines %d to %d'
      % (len(mp), mp[-1][1] if mp else 0, mp[4][0] if len(mp) > 4 else 0, mp[4][1] if len(mp) > 4 else 0), len(mp) == 16 and first_ok and ends_ok and mp[-1][1] == len(L_) - 1 and L_[mp[4][0]].startswith("// 3b. DUNNETT'S TEST"), mp)
rn_old = set(re.findall(r'(?m)^(?:EXPORT )?(av_\w+|AnovaLab)\(', OSRC)); rn_new = set(re.findall(r'(?m)^(?:EXPORT )?(av_\w+|AnovaLab)\(', SRC))
NEWR = {'av_DnSetup', 'av_DnBuild', 'av_DnGI', 'av_DnTail', 'av_DnCrit', 'av_DnEst', 'av_DnPage', 'av_DnAsk', 'av_DnAll', 'av_DnCritRun', 'av_AxW', 'av_FitN', 'av_FitS', 'av_DnRowG', 'av_DnPitch', 'av_DnTS', 'av_DnMove', 'av_DnRun',
        'av_ODrawDunn', 'av_DnTk', 'av_ODrawDnPl'}
CHG = {'av_Init', 'av_OCrit', 'av_PostHoc', 'av_ODraw', 'av_HelpPage', 'av_Help', 'av_OArrow', 'av_OTap', 'av_OMenu', 'av_OView', 'av_TView', 'av_BView', 'av_VView', 'av_Hello'}
chg = set(n_ for n_ in rn_old if n_ != 'AnovaLab' and routine(OSRC, n_ + '(') != routine(SRC, n_ + '('))
main_same = OSRC[OSRC.index('EXPORT AnovaLab()'):] == SRC[SRC.index('EXPORT AnovaLab()'):]
check('G6 the %d new routines carry the program\'s tag, and beta 1h\'s %d routines are all still there; %d of them are untouched, character for character (the Tukey engine, every analysis and every other page among them, the group picker that moved up, and the main routine); the %d that changed are the ones meant: %s'
      % (len(NEWR), len(rn_old), len(rn_old) - len(chg), len(chg), ', '.join(sorted(chg))), rn_old <= rn_new and rn_new - rn_old == NEWR and chg == CHG and main_same
      and all(n_ not in chg for n_ in ('av_BuildZ', 'av_RngCDF', 'av_BuildT', 'av_PkI', 'av_SRCDF', 'av_SRCrit', 'av_TEst', 'av_OCompute', 'av_TukeyCrit', 'av_TukeyP', 'av_TukeyP1', 'av_PickG', 'av_PickG2', 'av_ODrawPairs', 'av_ODrawDots', 'av_TCompute', 'av_BCompute', 'av_VCompute')),
      (sorted(rn_new - rn_old - NEWR), sorted(NEWR - rn_new), sorted(chg ^ CHG)))
big_un = sorted(set((m_.group(0), it['text'][:40]) for rec in OV.RECORDS.values() for e in rec['screens'].values() for it in e[2]['items'] if 'text' in it
                    for m_ in re.finditer(r'(?<![\d.,])\d{4,}(?![\d,])', it['text']) if not re.fullmatch(r'(18|19|20)\d\d', m_.group(0))))
check('G7 commas: no number of four or more digits is drawn without them on any screen above (years aside)', not big_un, big_un[:8])
verbs = lambda t: re.findall(r'\b(reworks?|reworked|ports?|ported|replaces)\b', t)
check('G8 the credits say what was done: no "reworks", "ports" or "replaces" in the file (beta 1h: %d); the header says which program was read for Dunnett\'s test, what it does, and that none of its code is here; the sources name Dunnett (1955) and (1964)'
      % len(verbs(OSRC)), verbs(SRC) == verbs(OSRC) == [] and 'program STAT.08, was read: after an ANOVA it gives each group\'s t' in SRC and 'None of its code is in' in SRC
      and 'Dunnett (1955) JASA 50:1096-1121' in SRC and 'Dunnett (1964) Biometrics' in SRC)
m9 = re.search(r'the p is within (\S+) %\s*\n?//\s*of its value wherever it is 0\.0001 or more', SRC); m9b = re.search(r'and d crit within (\S+) % for alpha', SRC)
check('G9 the accuracy the header, section 3b and help page 5 state is the one measured in A4 and A5: p within %s %% (measured %.3f %%), d crit within %s %% (measured %.4f %%)'
      % (m9.group(1) if m9 else '?', 100 * tlRel, m9b.group(1) if m9b else '?', 100 * crR),
      m9 is not None and m9b is not None and float(m9.group(1)) / 100 > tlRel and float(m9b.group(1)) / 100 > crR and SRC.count('0.05 %') >= 3 and 'p within 0.05 %.' in SRC, (m9, m9b))
fn = subprocess.run([sys.executable, os.path.join('tools', 'fleet_names_v2.py')] + sorted(os.path.join('programs', f) for f in os.listdir('programs') if f.endswith('.txt')), capture_output=True, text=True)
check('G10 fleet names: %s' % fn.stdout.strip().split('\n')[-1][:160], fn.returncode == 0 and ' 0 collisions' in fn.stdout and '31 files' in fn.stdout, fn.stdout[-400:] + fn.stderr[-200:])

print('=== D. layout over every beta 1i screen above')
def pxw(t): return sum((GW.get(str(ord(ch))) or [6, 7, 8])[0] for ch in t)       # font 1; a glyph not in the table counts as a digit
NEWTAGS = [t for t in OV.RECORDS if t.startswith('AnovaLab_beta1i')]; OLDTAGS = [t for t in OV.RECORDS if t.startswith('AnovaLab_beta1h')]
firm = []; firm_old = []
for t, f in OV.report().items():
    dst = firm if t in NEWTAGS else firm_old
    dst += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    dst += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
recs_new = dict((t, OV.RECORDS[t]) for t in NEWTAGS)
rep_ = sorted(set((x[0], x[3], x[4]) for v in LF.clipped(recs_new).values() for x in v))
cut = [(t, pxw(t) if int(f) == 1 else px(t, int(f)), w) for t, f, w in rep_ if (pxw(t) if int(f) == 1 else px(t, int(f))) > w]
nsc = sum(len(OV.RECORDS[t]['screens']) for t in NEWTAGS)
ndun = sum(1 for t in NEWTAGS for e in OV.RECORDS[t]['screens'].values() if any(it.get('text', '').startswith('Dunnett') for it in e[2]['items'][:2]))
newfirm = sorted(set(firm) - set(firm_old))
check('D1 no firm overlap and no text off the screen on any beta 1i screen above that beta 1h does not have too (text_overlap_v1 over %s different screens, %d of them Dunnett\'s pages; on both versions it finds %s)'
      % (format(nsc, ','), ndun, ', '.join('"%s" on "%s"' % (str(x[0])[:24], str(x[1])[:24]) for x in sorted(set(firm) & set(firm_old))[:4]) or 'nothing'), not newfirm and nsc > 250 and ndun > 40, newfirm[:6])
check('D2 no number cut short by its width argument (label_fit_v1 reports %d texts at its estimate; none is wider than its width argument at the measured glyph widths)' % len(rep_), not cut, cut[:4])

print('\n%d checks, %d failed   (%.0f s)' % (NPASS[0] + len(FAIL), len(FAIL), time.time() - T00))
sys.exit(1 if FAIL else 0)
