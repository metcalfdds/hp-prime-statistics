#!/usr/bin/env python3
"""verify_ResampLab_beta1a.py -- checks for ResampLab beta 1a (21 Oct 2026): every beta 1 check, adapted
to beta 1a's wording, plus Part R, one section per finding of the independent second review
(REVIEW2_ResampLab_beta1.md): R1 key drain (stale-key mode, every action), R2 the one-pass jackknife,
R3 no COMB overflow (1,000 v 1,000), R4 no interval work in the progress redraw and an honest cap,
R5 relative tie tolerances (1E-10 and 1E10 scales), R6 Darwin's pots, R7 no "= <", R8 the lesser items.

(beta 1's description follows.)
verify_ResampLab_beta1.py -- checks for ResampLab beta 1 (21 Oct 2026).

Runs the real PPL source in the PC harness (ref/ppl_run_v3e.py) and checks it against SciPy 1.18,
exact enumeration (itertools, exact Fractions) and replays of its own random numbers.

  Part E  exact permutation p: every split (two groups, mean and median, all three alternatives)
          against itertools.combinations with exact Fractions, on the 5 v 5 preset and 28 more designs
          (ties, n = 2, decimals, negatives, a huge value, all-equal groups); scipy.stats.permutation_test
          (exact, one-sided) on the same; every sign pattern (paired: the counting-by-sums route and the
          Gray-code route) against itertools.product: Darwin (Fisher 1935) and 16 more.
  Part M  Monte Carlo: the program's RANDOM numbers are logged and the shuffles / sign flips replayed in
          Python, which must give EXACTLY the program's counts; the Monte Carlo p must agree with the
          exact p (5 v 5, Darwin) or with a 200,000-shuffle numpy run (MockJury, Rossi) within 3.3
          binomial standard errors.
  Part B  the bootstrap: the resample indices are rebuilt from the logged RANDOM numbers, the program's
          bootstrap values must equal numpy's on those indices, and its percentile, basic and BCa
          intervals must equal scipy.stats.bootstrap's when SciPy is handed THE SAME resamples (a
          numpy Generator whose integers() returns them); the jackknife acceleration against a direct
          computation and SciPy's _bca_interval; the t-interval against scipy.stats.t; the Welch
          interval against scipy.stats.ttest_ind; BCa refusals (a = 0/0, estimate outside the values);
          4 statistics x 22 data sets.
  Part H  every menu path in the harness: the five presets and the 5 v 5 set through every soft key,
          the Enter menu, the Info / Help / CIs / BCa pages, taps on dots, bins, the red line and the
          status lines; Use my data (D1, D2; missing D1; all equal; one value); Settings (seed, level,
          refusals, Cancel); the seed repeating a run; Esc during x1000 and during an exact count; the
          60-second cap (TICKS sped up); Quit's summary.  The numbers on the pages are checked against
          the values above.
  Part A  audits over EVERY harness run: no runtime error, no scientific-notation STRING (h.sci_strings),
          no text off the 320 x 240 screen (font 1 at 6.5 px a character, ChiTable's measure), no
          MSGBOX over 5 lines, every CHOOSE line at most 30 characters, the soft keys always six labels.
Prints "N checks, M failures".
"""
import sys, os, itertools, math, random, time, re, warnings
from fractions import Fraction as Fr
import numpy as np
from scipy import stats
from scipy.stats import _resampling as RS

os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
sys.path.insert(0, '/home/claude/new6/ref')
from ppl_run_v3e import Harness, KEY, Tap   # noqa: E402

PROG = '/home/claude/new6/ResampLab_beta1b.txt'
NCHK = [0]
FAILS = []
ALL = []          # (name, harness) of every run, for the audits


def check(name, ok, detail=''):
    NCHK[0] += 1
    print(('PASS ' if ok else 'FAIL ') + name + ('   ' + detail if detail else ''))
    if not ok:
        FAILS.append(name)


def say(s):
    print(s)


# ------------------------------------------------------------ harness set-up
def mk(name, seed=1, app_data=None, tick_ms=None):
    h = Harness(PROG, strict=False, idle_key=4, seed=seed, app_data=app_data)
    # RANDSEED is not in the harness: it reseeds the harness's RANDOM, as the calculator's RANDSEED
    # reseeds RANDOM (hp-prime-kit measured that on the emulator; not yet on our G1/G2)
    h._table['RANDSEED'] = lambda a, site: (h.rng.seed(int(a[0])), 0.0)[1]
    h.rlog = []
    orig = h._random

    def rnd(a):
        v = orig(a)
        h.rlog.append(v)
        return v
    h._random = rnd
    if tick_ms is not None:
        def tk():
            h.clock += tick_ms
            return h.clock
        h._ticks = tk
    ALL.append((name, h))
    return h


def run(h, entry='ResampLab', *args):
    err = None
    try:
        h.call(entry, *args)
    except Exception as e:      # a PPLError is a runtime error on the device
        err = e
    return err


def G(h, n):
    return h.globals_[n]


def engine(name, A, B, mode, st=1, ha=0, seed=1, diffs=None):
    """The engine of one mode on given data, without the menus."""
    h = mk(name, seed=seed)
    h.call('rs_Init')
    h.call('rs_SetTwo', [float(x) for x in A], [float(x) for x in B], 'A', 'B', name, '', 's1', 's2', 'n')
    if diffs is not None:
        h.globals_['rsDf'] = [float(x) for x in diffs]
        h.globals_['rsNd'] = float(len(diffs))
        h.globals_['rsPair'] = 1.0
        h.globals_['rsBoot1'] = 1.0
    h.globals_['rsExLim'] = 5000.0            # Part E lists designs up to C = 5,000 directly
    h.globals_['rsMode'] = float(mode)
    h.globals_['rsSt'] = float(st)
    h.globals_['rsHa'] = float(ha)
    ok = h.call('rs_Start')
    return h, ok


# ------------------------------------------------------------ Python references
def fr(x):
    return Fr(repr(float(x))) if not isinstance(x, Fr) else x


def fmed(v):
    v = sorted(v)
    n = len(v)
    return v[(n - 1) // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def fstat(v, st):
    if st == 1:
        return sum(v) / len(v)
    return fmed(v)


def exact_two(A, B, st):
    """Exact counts over every split, in exact Fractions: (C, n >= obs, n <= obs, n |d| >= |obs|)."""
    pool = [fr(x) for x in A] + [fr(x) for x in B]
    nA, N = len(A), len(A) + len(B)
    obs = fstat(pool[:nA], st) - fstat(pool[nA:], st)
    c = u = l = a = 0
    for comb in itertools.combinations(range(N), nA):
        s = set(comb)
        ga = [pool[i] for i in comb]
        gb = [pool[i] for i in range(N) if i not in s]
        t = fstat(ga, st) - fstat(gb, st)
        c += 1
        u += t >= obs
        l += t <= obs
        a += abs(t) >= abs(obs)
    return c, u, l, a


def exact_paired(D):
    d = [fr(x) for x in D]
    n = len(d)
    obs = sum(d)
    c = u = l = a = 0
    for sg in itertools.product((1, -1), repeat=n):
        s = sum(x * y for x, y in zip(sg, d))
        c += 1
        u += s >= obs
        l += s <= obs
        a += abs(s) >= abs(obs)
    return c, u, l, a


def pfr(c, n):
    s = 'p = %s/%s' % (intc(c), intc(n))
    if c == 0:
        return s
    if c / n < 0.0001:
        return s + ' (p < 0.0001)'
    return s + ' = %.4f' % round(c / n + 1e-15, 4)


def peq(p):
    return 'p < 0.0001' if p < 0.0001 else 'p = %.4f' % round(p + 1e-15, 4)


def pstr(p):
    if p < 0.0001:
        return '< 0.0001'
    return '%.4f' % round(p + 1e-15, 4)


def fmt(v, d):
    r = round(v, d)
    if r == 0:
        r = 0.0
    return '%.*f' % (d, r)


def fmts(v, d):
    r = round(v, d) + 0.0
    if r == 0:
        r = 0.0
    return ('+' if r > 0 else '') + '%.*f' % (d, r)


def intc(n):
    return '{:,}'.format(int(round(n)))


# ------------------------------------------------------------ the program's arithmetic, in numpy
# (sequential sums in the program's order, so the doubles are bit-for-bit the same)
def seq_mean(x, axis=-1):
    x = np.asarray(x)
    s = np.zeros(x.shape[:-1])
    for j in range(x.shape[-1]):
        s = s + x[..., j]
    return s / x.shape[-1]


def seq_med(x, axis=-1):
    x = np.sort(np.asarray(x), axis=-1)
    n = x.shape[-1]
    if n % 2:
        return x[..., (n - 1) // 2]
    return (x[..., n // 2 - 1] + x[..., n // 2]) / 2


def seq_sd(x, axis=-1):
    x = np.asarray(x)
    m = seq_mean(x)
    q = np.zeros(x.shape[:-1])
    for j in range(x.shape[-1]):
        q = q + (x[..., j] - m) ** 2
    return (q / (x.shape[-1] - 1)) ** 0.5


def seq_trim(x, axis=-1):
    x = np.sort(np.asarray(x), axis=-1)
    n = x.shape[-1]
    g = n // 10
    s = np.zeros(x.shape[:-1])
    for j in range(g, n - g):
        s = s + x[..., j]
    return s / (n - 2 * g)


STATF = {1: seq_mean, 2: seq_med, 3: seq_sd, 4: seq_trim}


class FakeRng(np.random.Generator):
    """A numpy Generator whose integers() hands back fixed index matrices, in order: SciPy's
    bootstrap then uses exactly the program's resamples."""
    def __init__(self, mats):
        super().__init__(np.random.PCG64(0))
        self.mats = list(mats)

    def integers(self, low, high=None, size=None, dtype=np.int64, endpoint=False):
        m = self.mats.pop(0)
        assert m.shape == tuple(size), (m.shape, size)
        return m


def boot_indices(rlog, sizes, B):
    """Rebuild the resample indices (0-based) from the logged RANDOM values: per resample, n_1
    indices for the first sample, then n_2 for the second; index = MIN(n, 1 + IP(u n)) - 1."""
    mats = [np.zeros((B, n), dtype=np.int64) for n in sizes]
    k = 0
    for b in range(B):
        for s, n in enumerate(sizes):
            for j in range(n):
                mats[s][b, j] = min(n, 1 + int(rlog[k] * n)) - 1
                k += 1
    return mats, k


def replay_two(rlog, N, k, V, nA, nB, kA, st, B):
    """Replay the program's partial Fisher-Yates shuffles; returns the list of d."""
    W = list(range(1, N + 1))
    Tot = 0.0
    for v in V:
        Tot += v
    out = []
    p = 0
    for b in range(B):
        U = 0.0
        for i in range(1, k + 1):
            u = rlog[p]; p += 1
            j = i + min(N - i, int(u * (N - i + 1)))
            W[j - 1], W[i - 1] = W[i - 1], W[j - 1]
            U = U + V[W[i - 1] - 1]
        if st == 1:
            SA = U if kA == 1 else Tot - U
            out.append(SA / nA - (Tot - SA) / nB)
        else:
            c = sorted(W[:k])
            a = [V[i - 1] for i in c]
            o = [V[i - 1] for i in range(1, N + 1) if i not in set(c)]
            ma, mo = float(fmed(a)), float(fmed(o))
            out.append(ma - mo if kA == 1 else mo - ma)
    return out, p


def tails(ts, obs, eps):
    u = sum(1 for t in ts if t >= obs - eps)
    l = sum(1 for t in ts if t <= obs + eps)
    a = sum(1 for t in ts if abs(t) >= abs(obs) - eps)
    return u, l, a


# ===================================================================== Part E: exact
say('\n===== Part E: exact permutation distributions =====')
ILL_A, ILL_B = [14, 18, 12, 16, 15], [10, 13, 9, 14, 11]
rng = random.Random(20261021)
designs = [('5 v 5 preset', ILL_A, ILL_B)]
designs += [('n=2 v 2', [3, 7], [1, 2]), ('2 v 3 ties', [5, 5], [5, 6, 5]), ('3 v 3 neg', [-2.5, -1, 0.5], [-4, -3.25, 1]),
            ('4 v 6 decimals', [1.25, 2.5, 3.75, 2.0], [0.5, 1.0, 1.5, 0.25, 2.25, 0.75]),
            ('6 v 6 ints ties', [3, 3, 4, 5, 5, 9], [1, 3, 3, 2, 4, 4]), ('7 v 7', [12, 15, 9, 18, 14, 11, 20], [8, 11, 7, 10, 13, 9, 12]),
            ('5 v 9', [2, 4, 4, 6, 8], [1, 1, 2, 3, 3, 4, 5, 5, 7]), ('3 v 12', [10, 11, 12], list(range(1, 13))),
            ('huge value', [1, 2, 3, 1000000], [2, 3, 4, 5, 6]), ('A all equal', [4, 4, 4, 4], [1, 2, 3, 5, 6, 7]),
            ('B larger', [1, 2, 3], [10, 20, 30, 40, 50, 60, 70, 80]), ('obs 0', [1, 2, 3], [3, 2, 1]),
            ('one big tie', [5, 5, 5, 6], [5, 5, 5, 5, 4])]
for i in range(15):
    nA = rng.randint(2, 7)
    nB = rng.randint(2, 7)
    while math.comb(nA + nB, min(nA, nB)) > 5000:
        nB -= 1
    kind = i % 3
    if kind == 0:
        A = [rng.randint(0, 9) for _ in range(nA)]; B = [rng.randint(0, 9) for _ in range(nB)]
    elif kind == 1:
        A = [round(rng.uniform(-5, 5), 2) for _ in range(nA)]; B = [round(rng.uniform(-5, 5), 2) for _ in range(nB)]
    else:
        A = [round(rng.gauss(50, 10), 1) for _ in range(nA)]; B = [round(rng.gauss(45, 10), 1) for _ in range(nB)]
    designs.append(('random %d (%d v %d)' % (i + 1, nA, nB), A, B))
for nm, A, B in designs:
    for st in (1, 2):
        h, ok = engine('E ' + nm, A, B, 1, st)
        if ok != 1:
            check('E %s st%d starts' % (nm, st), False, 'refused')
            continue
        err = run(h, 'rs_PmExact')
        want = exact_two(A, B, st)
        got = (G(h, 'rsXC'), G(h, 'rsXU'), G(h, 'rsXL'), G(h, 'rsXA'))
        check('E two-group %s, %s: exact counts (C, >=, <=, |>=|)' % (nm, 'mean' if st == 1 else 'median'),
              err is None and tuple(int(x) for x in got) == want and G(h, 'rsXOK') == 2,
              'program %s, itertools %s' % (tuple(int(x) for x in got), want))
        # the histogram of all splits adds up to C
        check('E %s st%d: exact histogram sums to C' % (nm, st), int(sum(G(h, 'rsEH'))) == want[0])
# scipy.stats.permutation_test (exact) for the one-sided p of the mean
for nm, A, B in designs[:8]:
    r = stats.permutation_test((np.array(A, float), np.array(B, float)),
                               lambda x, y, axis: np.mean(x, axis=axis) - np.mean(y, axis=axis),
                               permutation_type='independent', vectorized=True, n_resamples=np.inf,
                               alternative='greater')
    h, ok = engine('Es ' + nm, A, B, 1, 1)
    run(h, 'rs_PmExact')
    p = G(h, 'rsXU') / G(h, 'rsXC')
    check('E scipy.permutation_test exact, %s: p(greater) %.6f vs %.6f' % (nm, p, r.pvalue), abs(p - r.pvalue) < 1e-9)

# paired
DARWIN_C = [23.5, 12, 21, 22, 19.125, 21.5, 22.125, 20.375, 18.25, 21.625, 23.25, 21, 22.125, 23, 12]
DARWIN_S = [17.375, 20.375, 20, 20, 18.375, 18.625, 18.625, 15.25, 16.5, 18, 16.25, 18, 12.75, 15.5, 18]
DARWIN_D = [a - b for a, b in zip(DARWIN_C, DARWIN_S)]
check('E Darwin differences x 8 are Fisher\'s eighths (DATASETS.md)',
      [round(d * 8) for d in DARWIN_D] == [49, -67, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, -48])
pdes = [('Darwin', DARWIN_D)]
pdes += [('n=2', [1.5, -0.5]), ('n=3 zero', [2, 0, -1]), ('all positive', [1, 2, 3, 4, 5]), ('ints n=10', [3, -1, 4, 1, -5, 9, 2, 6, -5, 3]),
         ('decimals', [0.12, -0.05, 0.33, 0.21, -0.18, 0.07, 0.4]), ('floats Gray n=8', [0.1234567, -0.7654321, 0.3333333, 1.4142136, -0.5772157, 2.7182818, 0.6931472, -1.6180340]),
         ('floats Gray n=12', [math.sin(i) * 3 for i in range(1, 13)]), ('mixed zeros', [0, 0, 1, -1, 2]),
         ('ints n=15', [5, -3, 8, 1, 0, 7, -2, 4, 6, -1, 3, 9, -4, 2, 5])]
for i in range(7):
    n = rng.randint(3, 14)
    if i % 2 == 0:
        D = [rng.randint(-20, 20) for _ in range(n)]
    else:
        D = [round(rng.uniform(-3, 3), 2) for _ in range(n)]
    pdes.append(('random %d (n=%d)' % (i + 1, n), D))
for nm, D in pdes:
    h, ok = engine('Ep ' + nm, [1, 2], [1, 2], 2, 1, diffs=D)
    if ok != 1:
        check('E paired %s starts' % nm, False)
        continue
    knd = int(G(h, 'rsXKnd')); xok = int(G(h, 'rsXOK'))
    if xok == 0:
        check('E paired %s: exact refused only when n > 12 and off-grid' % nm, len(D) > 12)
        continue
    err = run(h, 'rs_PdExact')
    want = exact_paired(D)
    got = tuple(int(G(h, x)) for x in ('rsXC', 'rsXU', 'rsXL', 'rsXA'))
    check('E paired %s (%s): exact counts (2^n, >=, <=, |>=|)' % (nm, {2: 'counting by sums', 3: 'Gray code'}[knd]),
          err is None and got == want, 'program %s, itertools %s' % (got, want))
DW = exact_paired(DARWIN_D)
check('E Darwin (Python, itertools): %d of %d two-sided, %d one-sided (Fisher\'s own figure is in his book, not checked here)'
      % (DW[3], DW[0], DW[1]), DW[0] == 32768 and DW[3] == 1726 and DW[1] == 863)
h, ok = engine('Ep Gray route', [1], [1], 2, 1, diffs=[0.1234567, -0.7654321, 0.3333333])
check('E paired off-grid n=3 uses the Gray-code route', int(G(h, 'rsXKnd')) == 3)
h, ok = engine('Ep big n', [1], [1], 2, 1, diffs=[0.1234567 * (i + 1) for i in range(14)])
check('E paired off-grid n=14: exact refused, random flips used', int(G(h, 'rsXOK')) == 0 and 'random flips' in G(h, 'rsXWhy'))

# ===================================================================== Part M: Monte Carlo
say('\n===== Part M: Monte Carlo replays =====')


def mc_two(nm, A, B, st, nrun, seed):
    h, ok = engine('M ' + nm, A, B, 1, st, seed=seed)
    h.rlog.clear()
    run(h, 'rs_Run', float(nrun))
    Bn = int(G(h, 'rsB'))
    V = list(G(h, 'rsV'))
    ts, used = replay_two(h.rlog, int(G(h, 'rsN')), int(G(h, 'rsK')), V, len(A), len(B), int(G(h, 'rsKA')), st, Bn)
    u, l, a = tails(ts, G(h, 'rsObs'), G(h, 'rsEps'))
    got = (int(G(h, 'rsNU')), int(G(h, 'rsNL')), int(G(h, 'rsNAb')))
    check('M two-group replay %s %s: B = %d, counts %s = replay %s, %d random numbers used' %
          (nm, 'mean' if st == 1 else 'median', Bn, got, (u, l, a), used),
          got == (u, l, a) and used == len(h.rlog) and Bn == nrun)
    return h, ts


MJ_U = [1, 4, 3, 2, 8, 8, 1, 1, 5, 7, 1, 5, 2, 12, 10, 1, 6, 2, 5, 12, 6, 3, 8, 4, 10, 10, 15, 15, 3, 3, 3, 11, 12, 2, 1, 1, 12]
MJ_B = [10, 3, 5, 1, 7, 7, 3, 7, 2, 3, 5, 1, 1, 1, 2, 2, 10, 10, 3, 4, 7, 1, 1, 2, 2, 3, 15, 4, 6, 2, 10, 3, 2, 3, 5, 10, 2, 2, 2]
MJ_A = [5, 5, 4, 3, 6, 4, 9, 8, 3, 2, 10, 1, 1, 3, 1, 3, 5, 8, 3, 1, 1, 1, 2, 2, 1, 1, 2, 3, 4, 5, 3, 3, 3, 2, 7, 6, 12, 8]
RO_AID = [46, 24, 50, 20, 50, 22, 24, 49, 8, 8, 11, 9, 16, 15, 7, 46, 40, 37, 12, 14, 20, 32, 20, 42, 46, 36, 18, 34, 35, 9, 34, 35, 39, 19, 48, 37, 20, 36, 30, 42, 35, 49, 49, 45, 36, 8, 15, 12]
RO_NO = [20, 17, 25, 23, 37, 25, 28, 10, 6, 52, 49, 43, 5, 27, 18, 2, 26, 21, 48, 49, 8, 13, 33, 37, 44, 52, 17, 16, 3, 45, 28, 14, 43, 14, 8, 25, 17, 32, 18, 38, 24, 31, 40, 26, 47, 40, 21, 1, 43, 24, 11, 33, 50, 39, 44, 30, 43, 26, 40, 46, 35, 27, 52, 4, 52, 19]
BJS = [117, 188, 172, 145, 173, 159, 123, 136, 115, 190, 158, 147, 117, 196, 169, 160, 135, 163, 176, 155, 126, 133, 150, 146, 157, 137, 180, 134, 135, 128, 209, 144, 164, 185, 168, 121, 195, 149, 148, 216, 139]


def within(p_hat, p, B, z=3.3, B2=None):
    v = p * (1 - p) / B + (p * (1 - p) / B2 if B2 else 0)
    return abs(p_hat - p) <= z * math.sqrt(max(v, 1e-12)) + 1e-12


# 5 v 5: Monte Carlo against the exact p
h, ts = mc_two('5 v 5', ILL_A, ILL_B, 1, 2000, 11)
pe = 12 / 252
pm = G(h, 'rsNAb') / 2000
check('M 5 v 5 mean: random p %.4f within 3.3 SE of the exact 12/252 = %.4f' % (pm, pe), within(pm, pe, 2000))
h, ts = mc_two('5 v 5', ILL_A, ILL_B, 2, 2000, 12)
c, u, l, a = exact_two(ILL_A, ILL_B, 2)
pm = G(h, 'rsNAb') / 2000
check('M 5 v 5 median: random p %.4f within 3.3 SE of exact %d/%d' % (pm, a, c), within(pm, a / c, 2000))


def np_perm_p(A, B, st, R=200000, seed=5):
    g = np.random.default_rng(seed)
    pool = np.array(A + B, float)
    nA = len(A)
    obs = (np.mean(A) - np.mean(B)) if st == 1 else (np.median(A) - np.median(B))
    cnt = 0
    for chunk in range(R // 20000):
        P = np.argsort(g.random((20000, len(pool))), axis=1)
        X = pool[P]
        if st == 1:
            t = X[:, :nA].mean(1) - X[:, nA:].mean(1)
        else:
            t = np.median(X[:, :nA], 1) - np.median(X[:, nA:], 1)
        cnt += np.sum(np.abs(t) >= abs(obs) - 1e-9)
    return cnt / R


for nm, A, B, st, nrun in [('MockJury U v B', MJ_U, MJ_B, 1, 1000), ('MockJury U v B', MJ_U, MJ_B, 2, 600),
                           ('Rossi aid v no aid', RO_AID, RO_NO, 1, 600), ('MockJury U v Avg', MJ_U, MJ_A, 1, 600)]:
    h, ts = mc_two(nm, A, B, st, nrun, 7)
    pr = np_perm_p(A, B, st)
    pm = G(h, 'rsNAb') / nrun
    check('M %s %s: random p %.4f within 3.3 SE of numpy\'s 200,000-shuffle %.4f' % (nm, 'mean' if st == 1 else 'median', pm, pr),
          within(pm, pr, nrun, B2=200000))

# paired Monte Carlo replay and Darwin against the exact p
for nm, D, nrun, seed in [('Darwin', DARWIN_D, 3000, 3), ('ints n=10', [3, -1, 4, 1, -5, 9, 2, 6, -5, 3], 800, 4)]:
    h, ok = engine('Mp ' + nm, [1], [1], 2, 1, diffs=D, seed=seed)
    h.rlog.clear()
    run(h, 'rs_Run', float(nrun))
    n = len(D)
    ts = []
    p = 0
    for b in range(nrun):
        s = 0.0
        for i in range(n):
            if h.rlog[p] < 0.5:
                s = s - D[i]
            else:
                s = s + D[i]
            p += 1
        ts.append(s / n)
    u, l, a = tails(ts, G(h, 'rsObs'), G(h, 'rsEps'))
    got = (int(G(h, 'rsNU')), int(G(h, 'rsNL')), int(G(h, 'rsNAb')))
    check('M paired replay %s: counts %s = replay %s' % (nm, got, (u, l, a)), got == (u, l, a) and p == len(h.rlog))
    c, eu, el, ea = exact_paired(D)
    check('M paired %s: random p %.4f within 3.3 SE of exact %d/%d' % (nm, got[2] / nrun, ea, c), within(got[2] / nrun, ea / c, nrun))

# ===================================================================== Part B: bootstrap
say('\n===== Part B: the bootstrap against scipy.stats.bootstrap, same resamples =====')


def boot_check(nm, X, st, Bn, lev=0.95, seed=1, expect_bca=True):
    h, ok = engine('B ' + nm, X, [], 3, st, seed=seed)
    if ok != 1:
        check('B %s st%d starts' % (nm, st), False)
        return None
    h.globals_['rsLev'] = float(lev)
    h.rlog.clear()
    err = run(h, 'rs_Run', float(Bn))
    run(h, 'rs_BtCI')
    Xs = np.array(sorted(X), float)
    n = len(Xs)
    mats, used = boot_indices(h.rlog, [n], Bn)
    th_prog = np.array(G(h, 'rsTh')[:Bn])
    th_np = STATF[st](Xs[mats[0]])
    sname = {1: 'mean', 2: 'median', 3: 'SD', 4: 'trimmed'}[st]
    check('B %s %s: %d bootstrap values = numpy on the same indices' % (nm, sname, Bn),
          err is None and used == len(h.rlog) and np.allclose(th_prog, th_np, rtol=1e-12, atol=1e-12))
    CI = G(h, 'rsCI'); ok4 = G(h, 'rsCIok')
    res = {}
    for meth in ('percentile', 'basic', 'BCa'):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            r = stats.bootstrap((Xs,), STATF[st], n_resamples=Bn, method=meth, confidence_level=lev,
                                rng=FakeRng([mats[0].copy()]), batch=None, vectorized=True)
        res[meth] = (float(r.confidence_interval.low), float(r.confidence_interval.high))
    tol = 1e-9 * (np.max(np.abs(Xs)) + 1)
    check('B %s %s: percentile (%.6g, %.6g) = SciPy (%.6g, %.6g)' % (nm, sname, CI[0], CI[1], *res['percentile']),
          abs(CI[0] - res['percentile'][0]) < tol and abs(CI[1] - res['percentile'][1]) < tol)
    check('B %s %s: basic (%.6g, %.6g) = SciPy (%.6g, %.6g)' % (nm, sname, CI[2], CI[3], *res['basic']),
          abs(CI[2] - res['basic'][0]) < tol and abs(CI[3] - res['basic'][1]) < tol)
    # the acceleration, directly
    jk = np.array([STATF[st](np.delete(Xs, i)[None, :])[0] for i in range(n)])
    dd = jk.mean() - jk
    den = np.sum(dd ** 2)
    a_py = np.sum(dd ** 3) / (6 * den ** 1.5) if den > 0 else float('nan')
    alpha = (1 - lev) / 2
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        a1, a2, a_sp = RS._bca_interval((Xs,), lambda x, axis=-1: STATF[st](x), -1, alpha, th_np, None, np)
    if G(h, 'rsAcOK') == 1:
        check('B %s %s: jackknife a %.8f = direct %.8f = SciPy %.8f' % (nm, sname, G(h, 'rsAcc'), a_py, float(a_sp)),
              abs(G(h, 'rsAcc') - a_py) < 1e-9 and abs(a_py - float(a_sp)) < 1e-9)
    else:
        check('B %s %s: a refused when every jackknife value is equal (SciPy: %s)' % (nm, sname, a_sp), den == 0)
    bca_sp = res['BCa']
    if ok4[2] == 1:
        check('B %s %s: BCa (%.6g, %.6g) = SciPy (%.6g, %.6g), alpha1 %.6f alpha2 %.6f' %
              (nm, sname, CI[4], CI[5], bca_sp[0], bca_sp[1], G(h, 'rsAl1'), G(h, 'rsAl2')),
              abs(CI[4] - bca_sp[0]) < tol and abs(CI[5] - bca_sp[1]) < tol and
              abs(G(h, 'rsAl1') - float(a1)) < 1e-9 and abs(G(h, 'rsAl2') - float(a2)) < 1e-9)
    else:
        check('B %s %s: BCa refused (%s); SciPy gives %s' % (nm, sname, G(h, 'rsBcaW'), bca_sp),
              not (np.isfinite(bca_sp[0]) and np.isfinite(bca_sp[1])))
    if st == 1:
        m = float(np.mean(Xs)); s = float(np.std(Xs, ddof=1))
        lo, hi = stats.t.interval(lev, n - 1, loc=m, scale=s / math.sqrt(n))
        check('B %s mean: t-interval (%.6g, %.6g) = scipy.stats.t (%.6g, %.6g)' % (nm, CI[6], CI[7], lo, hi),
              ok4[3] == 1 and abs(CI[6] - lo) < tol and abs(CI[7] - hi) < tol)
    sd_b = float(np.std(th_np, ddof=1))
    check('B %s %s: SE* = SD of the B values %.6g = numpy %.6g' % (nm, sname, G(h, 'rsSEs'), sd_b), abs(G(h, 'rsSEs') - sd_b) < tol)
    return h


for st in (1, 2, 3, 4):
    boot_check('BJS', BJS, st, 1000, seed=21 + st)
boot_check('BJS 90%', BJS, 1, 400, lev=0.90, seed=5)
boot_check('BJS 99%', BJS, 2, 400, lev=0.99, seed=6)
boot_check('Darwin diffs', DARWIN_D, 1, 500, seed=8)
brng = random.Random(77)
bsets = [('n=3', [1.0, 2.0, 4.0]), ('ties', [2, 2, 2, 3, 3, 5, 5, 5, 8, 9]), ('negative', [-3.2, -1.5, -0.25, 0.5, 1.75, -2.0, 0.0]),
         ('huge', [1, 2, 3, 4, 5, 1000000]), ('skewed', [round(brng.expovariate(0.1), 1) for _ in range(25)]),
         ('decimals', [round(brng.uniform(0, 1), 3) for _ in range(12)]), ('large scale', [round(1e5 + brng.gauss(0, 50), 2) for _ in range(20)])]
for i in range(8):
    n = brng.randint(4, 30)
    bsets.append(('random %d (n=%d)' % (i + 1, n), [round(brng.gauss(10, 3), brng.choice([0, 1, 2])) for _ in range(n)]))
for nm, X in bsets:
    for st in (1, 2, 3, 4):
        boot_check(nm, X, st, 300, seed=brng.randint(1, 10 ** 6))
# BCa refusals
h = boot_check('median ties (a = 0/0)', [1, 2, 2, 2, 3], 2, 200, seed=3, expect_bca=False)
h = boot_check('SD of near-constant', [0, 0, 0, 0, 0, 0, 0, 10], 3, 200, seed=4, expect_bca=False)

# two-group bootstrap
say('\n----- two-group bootstrap -----')


def boot2_check(nm, A, B, st, Bn, lev=0.95, seed=1):
    h, ok = engine('B2 ' + nm, A, B, 4, st, seed=seed)
    h.globals_['rsLev'] = float(lev)
    h.rlog.clear()
    err = run(h, 'rs_Run', float(Bn))
    run(h, 'rs_BtCI')
    XA = np.array(sorted(A), float); XB = np.array(sorted(B), float)
    mats, used = boot_indices(h.rlog, [len(XA), len(XB)], Bn)
    f = STATF[st]
    th_np = f(XA[mats[0]]) - f(XB[mats[1]])
    th_prog = np.array(G(h, 'rsTh')[:Bn])
    check('B2 %s %s: %d values = numpy on the same indices' % (nm, 'mean' if st == 1 else 'median', Bn),
          err is None and used == len(h.rlog) and np.allclose(th_prog, th_np, rtol=1e-12, atol=1e-12))
    CI = G(h, 'rsCI')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        r = stats.bootstrap((XA, XB), lambda x, y, axis=-1: f(x) - f(y), n_resamples=Bn, method='percentile',
                            confidence_level=lev, rng=FakeRng([mats[0].copy(), mats[1].copy()]), batch=None,
                            vectorized=True)
    tol = 1e-9 * (max(np.max(np.abs(XA)), np.max(np.abs(XB))) + 1)
    lo, hi = float(r.confidence_interval.low), float(r.confidence_interval.high)
    check('B2 %s: percentile (%.6g, %.6g) = SciPy (%.6g, %.6g)' % (nm, CI[0], CI[1], lo, hi),
          abs(CI[0] - lo) < tol and abs(CI[1] - hi) < tol)
    if st == 1:
        w = stats.ttest_ind(XA, XB, equal_var=False).confidence_interval(lev)
        check('B2 %s: Welch t (%.6g, %.6g) = scipy ttest_ind (%.6g, %.6g)' % (nm, CI[6], CI[7], w.low, w.high),
              G(h, 'rsCIok')[3] == 1 and abs(CI[6] - w.low) < tol and abs(CI[7] - w.high) < tol)
    return h


boot2_check('MockJury U v B', MJ_U, MJ_B, 1, 600, seed=9)
boot2_check('MockJury U v B', MJ_U, MJ_B, 2, 400, seed=10)
boot2_check('Rossi', RO_AID, RO_NO, 1, 300, seed=11)
boot2_check('5 v 5', ILL_A, ILL_B, 1, 400, lev=0.9, seed=12)
boot2_check('decimals', [1.25, 2.5, 3.75, 2.0], [0.5, 1.0, 1.5, 0.25, 2.25, 0.75], 2, 300, seed=13)
boot2_check('negatives', [-3, -1, -4, -1, -5], [2, 7, 1, 8, 2, 8], 1, 300, seed=14)

# ===================================================================== Part H: the menus, in the harness
say('\n===== Part H: every menu path in the harness =====')


def SK(h, s):
    """Tap soft key s (1..6) on the strip."""
    h.tap(int(53.4 * (s - 1) + 26), 230)


def labpages(h):
    return [p for p in h.pages if p.func == 'rs_DrawLab']


def lastlab(h):
    lp = labpages(h)
    return lp[-1] if lp else None


def has_any(h, sub):
    return any(p.has(sub) for p in h.pages)


def texts_of(p):
    return [t.text for t in p.texts]


def start_main(h, preset=None):
    h.press('Enter')                                   # the opening page
    if preset:
        h.choose('Load a preset'); h.choose(preset)
        h.press('Enter')                               # the data page


def finish(h):
    h.press('Esc')                                     # leave the lab page
    h.choose('Quit')


# ---- H1: the 5 v 5 set: exact, Ha, Stat, Info, Help, runs
h = mk('H1 5v5', seed=31)
start_main(h, '5 v 5')
SK(h, 6); SK(h, 3)                 # More, Exact
SK(h, 1)                           # Ha: A > B
SK(h, 1)                           # Ha: A < B
SK(h, 1)                           # Ha: two-sided again
SK(h, 4); h.press('Enter'); h.press('Enter')       # Info, two pages
SK(h, 5)
for i in range(5):
    h.press('Enter')                                   # Help, five pages
SK(h, 6)                                               # page 1 of the soft keys
SK(h, 1); SK(h, 2); SK(h, 3); SK(h, 4)                 # Once, x10, x100, x1000
SK(h, 6); SK(h, 2)                                     # More, Stat -> median
SK(h, 3)                                               # Exact (median)
finish(h)
err = run(h)
check('H1 5 v 5: no runtime error', err is None, repr(err))
c, u, l, a = exact_two(ILL_A, ILL_B, 1)
check('H1 data page shows the illustrative label and the source line', has_any(h, '5 v 5: ILLUSTRATIVE NUMBERS (not data)') and any(t.startswith('Illustrative numbers made up for the exact') for p in h.pages for t in texts_of(p)))

check('H1 exact view: "exact p = 12/252 = 0.0476"', has_any(h, 'exact p = 12/252 = 0.0476'))
check('H1 exact, Ha A > B: "exact %s"' % pfr(u, 252), has_any(h, 'exact ' + pfr(u, 252)))
check('H1 exact, Ha A < B: "exact %s"' % pfr(l, 252), has_any(h, 'exact ' + pfr(l, 252)))
check('H1 exact line says "of all 252"', has_any(h, 'exact: 12 of all 252 with |d| ' + '≥' + ' 3.60'))
cm, um, lm, am = exact_two(ILL_A, ILL_B, 2)
check('H1 median exact ' + pfr(am, 252), has_any(h, 'exact ' + pfr(am, 252)))
check('H1 Info page names the null hypothesis and the plus-one rule', any(t.startswith('H\u2080: the labels do not matter') for p in h.pages for t in texts_of(p)) and any('Phipson & Smyth' in t for p in h.pages for t in texts_of(p)))

check('H1 Help has five pages (the last one the disclaimer)', has_any(h, 'Home, sources, disclaimer') and has_any(h, 'DISCLAIMER: a teaching and demonstration aid.'))
# the random shuffles on the page agree with a replay of the program's own random numbers (mean part)
check('H1 Quit returns the summary', isinstance(h.result, str) and h.result.startswith('ResampLab: Permutation test: medians'), repr(h.result))
check('H1 the opening page shows the disclaimer', any(p.has('DISCLAIMER: a teaching and demonstration aid.') and p.func == 'rs_PgEnd' for p in h.pages[:2]))

# ---- H2: MockJury, Once / x10 / x100 / x1000, taps, Enter menu, + key; numbers vs a replay
h = mk('H2 MockJury', seed=32)
start_main(h, 'Unattr. v Beaut')
SK(h, 1)                                               # Once
h.tap(150, 120)                                        # a bin
SK(h, 1)
h.press('Plus')                                        # + = Once
SK(h, 2); SK(h, 3); SK(h, 4)                           # x10, x100, x1000
h.tap(rs_x := 0, 0)                                    # the title band: nothing
h.tap(100, 30)                                         # a dot in row A
h.tap(100, 62)                                         # a dot in row B
h.press('Enter'); h.choose('Details'); h.press('Enter'); h.press('Enter')
h.tap(150, 190); h.press('Enter'); h.press('Enter')    # the status lines open Info
finish(h)
err = run(h)
check('H2 MockJury: no runtime error', err is None, repr(err))
Bn = int(G(h, 'rsB'))
check('H2 MockJury: B = 3 + 10 + 100 + 1000 = 1113', Bn == 1113, str(Bn))
V = list(G(h, 'rsV'))
ts, used = replay_two(h.rlog, 76, 37, V, 37, 39, 1, 1, Bn)
u, l, a = tails(ts, G(h, 'rsObs'), G(h, 'rsEps'))
check('H2 replay of every random number gives the program\'s counts', (u, l, a) == (G(h, 'rsNU'), G(h, 'rsNL'), G(h, 'rsNAb')) and used == len(h.rlog))
obs = np.mean(MJ_U) - np.mean(MJ_B)
wo = 'observed ' + '\ue000' + 'A - ' + '\ue000' + 'B = ' + fmts(obs, int(G(h, 'rsDec'))) + ',  Ha: A ' + '\u2260' + ' B'
check('H2 "%s" on the page' % wo, has_any(h, wo) and abs(G(h, 'rsObs') - obs) < 1e-12)
want = pfr(a, Bn) + ',  plus-one ' + peq((a + 1) / (Bn + 1))
check('H2 the p line: "%s"' % want, has_any(h, want))
check('H2 a tap on a bin tells what it holds', any('..' in t and ' in tail)' in t for p in h.pages for t in texts_of(p)))
check('H2 a tap on a dot names its value and both groups', any(('now in A, came from' in t) for p in h.pages for t in texts_of(p)) and
      any(('now in B, came from' in t) for p in h.pages for t in texts_of(p)))
check('H2 the Info page says C(76, 37) splits are too many: random shuffles', any(t.startswith('Exact: not here (') for p in h.pages for t in texts_of(p)))
check('H2 the Enter menu lists the actions', any(c.title == 'Actions' for c in h.chooses))
check('H2 a run shows the progress page', any(p.func == 'rs_Busy' for p in h.pages))

# ---- H3: Darwin, paired, exact by counting, Info with Fisher's note
h = mk('H3 Darwin', seed=33)
start_main(h, 'Darwin')
SK(h, 1); SK(h, 3)
SK(h, 6); SK(h, 3)                                     # Exact
SK(h, 4); h.press('Enter'); h.press('Enter')           # Info
h.tap(120, 30)                                         # a pair
finish(h)
err = run(h)
check('H3 Darwin: no runtime error', err is None, repr(err))
check('H3 Darwin exact p = 1,726/32,768 = 0.0527', has_any(h, 'exact p = 1,726/32,768 = 0.0527'))
check('H3 Darwin observed mean d = 314/120 in', has_any(h, 'observed mean d = +' + fmt(314 / 120, int(G(h, 'rsDec')))) and abs(G(h, 'rsObs') - 314 / 8 / 15) < 1e-12)
check('H3 the Info page gives the count and leaves Fisher\'s figure to his book', any('Fisher (1935, sec. 21) worked this test' in t for p in h.pages for t in texts_of(p)) and any('1,726 of 32,768' in t for p in h.pages for t in texts_of(p)) and any('checked here)' in t for p in h.pages for t in texts_of(p)))
check('H3 a tap on a lollipop names the pair', any(t.startswith('pair ') for p in h.pages for t in texts_of(p)))
check('H3 data page shows the source line', any(t.startswith('Darwin (1876); Fisher (1935) The Design of') for p in h.pages for t in texts_of(p)))

# ---- H4: BJS bootstrap: x1000, CIs, BCa, Level, Stat
h = mk('H4 BJS', seed=34)
start_main(h, 'BJS')
SK(h, 4)                                               # x1000
SK(h, 6); SK(h, 2); h.press('Enter')                   # CIs page
SK(h, 3); h.press('Enter')                             # BCa page
finish(h)
err = run(h)
check('H4 BJS: no runtime error', err is None, repr(err))
Bn = int(G(h, 'rsB'))
Xs = np.array(sorted(BJS), float)
mats, used = boot_indices(h.rlog, [41], Bn)
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    rp = stats.bootstrap((Xs,), seq_mean, n_resamples=Bn, method='percentile', rng=FakeRng([mats[0].copy()]), batch=None, vectorized=True)
    rb = stats.bootstrap((Xs,), seq_mean, n_resamples=Bn, method='BCa', rng=FakeRng([mats[0].copy()]), batch=None, vectorized=True)
d = int(G(h, 'rsDec'))
wp = '95% percentile (' + fmt(rp.confidence_interval.low, d) + ', ' + fmt(rp.confidence_interval.high, d) + ')'
wb = '95% BCa (' + fmt(rb.confidence_interval.low, d) + ', ' + fmt(rb.confidence_interval.high, d) + ')'
check('H4 status line "%s" (SciPy on the same 1,000 resamples)' % wp, has_any(h, wp))
check('H4 status line "%s"' % wb, has_any(h, wb))
lo, hi = stats.t.interval(0.95, 40, loc=np.mean(Xs), scale=np.std(Xs, ddof=1) / math.sqrt(41))
check('H4 CIs page: t line', any(t.startswith('t: (' + fmt(lo, d) + ', ' + fmt(hi, d) + ')') for p in h.pages for t in texts_of(p)))
check('H4 CIs page: basic line present', any(t.startswith('basic: (') for p in h.pages for t in texts_of(p)))
check('H4 BCa page shows z0 and a', any('z\u2080 = the normal quantile of the share' in t for p in h.pages for t in texts_of(p)) and any(t.startswith('a = sum (J. - Ji)^3') for p in h.pages for t in texts_of(p)))

check('H4 data page: the name and the source line', has_any(h, 'BJS: months served, 41 homicide prisoners') and any(t.startswith('BJS, Prison Sentences and Time Served for') for p in h.pages for t in texts_of(p)))

h = mk('H4b BJS level and stat', seed=35)
start_main(h, 'BJS')
SK(h, 3)                                               # x100
SK(h, 6); SK(h, 4)                                     # Level -> 0.99
SK(h, 4)                                               # Level -> 0.90
SK(h, 1); SK(h, 6); SK(h, 3)                           # Stat -> median, back to page 1, x100
SK(h, 6); SK(h, 1); SK(h, 6); SK(h, 3)                 # SD, x100
SK(h, 6); SK(h, 1); SK(h, 6); SK(h, 3)                 # trimmed, x100
SK(h, 6); SK(h, 2); h.press('Enter')                   # CIs page (trimmed mean)
finish(h)
err = run(h)
check('H4b BJS level/stat cycle: no runtime error', err is None, repr(err))
check('H4b level 99% then 90% shown', has_any(h, '99% percentile (') and has_any(h, '90% percentile ('))
check('H4b every statistic named', all(has_any(h, 'Bootstrap: the ' + s) for s in ('mean', 'median', 'SD', '10% trimmed mean')))
check('H4b CIs page for the trimmed mean says t is for the mean only', has_any(h, 't: for the mean only'))

# ---- H5: two-group bootstrap on MockJury; H6 Rossi
h = mk('H5 boot2', seed=36)
h.press('Enter')
h.choose('Load a preset'); h.choose('Unattr. v Beaut'); h.press('Enter')
h.press('Esc')                                          # leave the permutation page
h.choose('Bootstrap CI: two groups')
SK(h, 3); SK(h, 1)
SK(h, 6); SK(h, 2); h.press('Enter')
h.tap(100, 30)
finish(h)
err = run(h)
check('H5 two-group bootstrap: no runtime error', err is None, repr(err))
check('H5 the Welch line and the percentile line', has_any(h, '95% Welch t (') and has_any(h, '95% percentile ('))
check('H5 a tap on a sample dot (after Once) says how often it was picked', any(': picked ' in t for p in h.pages for t in texts_of(p)))
w = stats.ttest_ind(MJ_U, MJ_B, equal_var=False).confidence_interval(0.95)
d = int(G(h, 'rsDec'))
check('H5 Welch t line = scipy (%s, %s)' % (fmt(w.low, d), fmt(w.high, d)), has_any(h, '95% Welch t (' + fmt(w.low, d) + ', ' + fmt(w.high, d) + ')'))

h = mk('H6 Rossi', seed=37)
start_main(h, 'Rossi')
SK(h, 3)
SK(h, 6); SK(h, 4); h.press('Enter'); h.press('Enter')
finish(h)
err = run(h)
check('H6 Rossi: no runtime error', err is None, repr(err))
check('H6 Rossi caveat on the Info page', any('Only the 114 arrested' in t for p in h.pages for t in texts_of(p)))
check('H6 Rossi n = 48 v 66', int(G(h, 'rsNA')) == 48 and int(G(h, 'rsNB')) == 66)

# ---- H7: Use my data
DA = [4.1, 5.2, 6.0, 5.5, 4.8, 6.3]
DB = [3.9, 4.6, 5.1, 5.0, 4.2, 5.9]
h = mk('H7 my data', seed=38, app_data={'D1': DA, 'D2': DB})
h.press('Enter')
h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: 2 groups'); SK(h, 6); SK(h, 3); h.press('Esc')
h.choose('Permutation test: paired'); SK(h, 6); SK(h, 3); h.press('Esc')
h.choose('Bootstrap CI: one sample'); SK(h, 3); h.press('Esc')
h.choose('Quit')
err = run(h)
check('H7 Use my data (D1, D2): no runtime error', err is None, repr(err))
c, u, l, a = exact_two(DA, DB, 1)
check('H7 two groups from D1, D2: exact ' + pfr(a, c), has_any(h, 'exact ' + pfr(a, c)))
pc, pu, pl, pa = exact_paired([x - y for x, y in zip(DA, DB)])
check('H7 paired D1 - D2: exact ' + pfr(pa, pc), has_any(h, 'exact ' + pfr(pa, pc)))
check('H7 data page: "My data: D1 (A) and D2 (B)"', has_any(h, 'My data: D1 (A) and D2 (B)'))

h = mk('H7b no D1', seed=39)
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: 2 groups')
h.choose('Quit')
err = run(h)
check('H7b no D1: a message, no error', err is None and any('D1 of the Statistics 1Var app' in ' '.join(m.lines) for m in h.msgboxes) and
      any('No data yet' in ' '.join(m.lines) for m in h.msgboxes), repr(err))

h = mk('H7c all equal', seed=40, app_data={'D1': [5, 5, 5], 'D2': [5, 5, 5, 5]})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: 2 groups')
h.choose('Bootstrap CI: one sample')
h.choose('Permutation test: paired')
h.choose('Quit')
err = run(h)
msgs = [' '.join(m.lines) for m in h.msgboxes]
check('H7c all-equal data refused with messages', err is None and any('Every value is the same' in m for m in msgs), str(msgs))

h = mk('H7d one value', seed=41, app_data={'D1': [5]})
h.press('Enter'); h.choose('Use my data'); h.choose('Quit')
err = run(h)
check('H7d one value in D1 refused', err is None and any('D1 of the Statistics' in ' '.join(m.lines) for m in h.msgboxes))

# Gray-code route from D1 alone (the differences) and a 7 v 7 exact count stopped by Esc
GD = [0.1234567, -0.7654321, 0.3333333, 1.4142136, -0.5772157, 2.7182818, 0.6931472, -1.6180340, 0.5, 0.25]
h = mk('H8 Gray', seed=42, app_data={'D1': GD})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: paired'); SK(h, 6); SK(h, 3); h.press('Esc')
h.choose('Quit')
err = run(h)
pc, pu, pl, pa = exact_paired(GD)
check('H8 D1 alone as differences, Gray code: exact p = %d/%s' % (pa, intc(pc)), err is None and has_any(h, 'exact ' + pfr(pa, pc)))

A7 = [12, 15, 9, 18, 14, 11, 20]; B7 = [8, 11, 7, 10, 13, 9]
h = mk('H9 Esc in exact', seed=43, app_data={'D1': A7, 'D2': B7})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: 2 groups'); SK(h, 6); SK(h, 3)
h.press('Esc', anytime=True)
SK(h, 3)
h.press('Esc'); h.choose('Quit')
err = run(h)
check('H9 Esc during an exact count: marked unfinished, not used, then a fresh count works',
      err is None and has_any(h, 'exact count stopped by Esc: not used') and int(G(h, 'rsXOK')) == 2 and int(G(h, 'rsXC')) == 1716)
c, u, l, a = exact_two(A7, B7, 1)
check('H9 the second (full) count: %d of 1,716' % a, int(G(h, 'rsXA')) == a)

h = mk('H9b over the limit', seed=49, app_data={'D1': [12, 15, 9, 18, 14, 11, 20], 'D2': [8, 11, 7, 10, 13, 9, 12]})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: 2 groups'); SK(h, 6); SK(h, 3)
h.press('Esc'); h.choose('Quit')
err = run(h)
check('H9b 7 v 7 (C(14, 7) = 3,432 > 2,000): Exact refused with the reason', err is None and
      any('3,432' in ' '.join(m.lines) and 'too many' in ' '.join(m.lines) for m in h.msgboxes), str([m.lines for m in h.msgboxes]))

# ---- H10: Esc during x1000; the 60-second cap
h = mk('H10 Esc run', seed=44)
start_main(h, 'Unattr. v Beaut')
SK(h, 4); h.press('Esc', anytime=True)
finish(h)
err = run(h)
check('H10 Esc stops x1000 early and says so', err is None and 0 < G(h, 'rsB') < 1000 and has_any(h, 'stopped by Esc after ' + intc(G(h, 'rsB'))),
      'B = %d' % G(h, 'rsB'))
h = mk('H11 cap', seed=45, tick_ms=5000)
start_main(h, 'Unattr. v Beaut')
SK(h, 4)
finish(h)
err = run(h)
capmsg = [t for p in h.pages for t in texts_of(p) if t.startswith('capped at ')]
check('H11 a slow calculator (TICKS 5 s per reading here): x1000 capped, the page says so',
      err is None and capmsg and G(h, 'rsB') < 1000 and capmsg[-1] == 'capped at %s: about 60 s on this calculator' % intc(G(h, 'rsB')),
      str(capmsg[-1:]) + ' B = %d' % G(h, 'rsB'))

# ---- H12: Settings: seed repeats a run; level; refusals; Cancel
def seeded(seed_val, nm):
    h = mk(nm, seed=1000 + len(ALL))
    h.press('Enter')
    h.choose('Seed, confidence level'); h.answer({'seS': seed_val, 'seL': 0.9})
    h.choose('Load a preset'); h.choose('5 v 5'); h.press('Enter')
    SK(h, 3)
    finish(h)
    err = run(h)
    return h, err


h1, e1 = seeded(2026, 'H12 seed a')
h2, e2 = seeded(2026, 'H12 seed b')
h3, e3 = seeded(7, 'H12 seed c')
same = (G(h1, 'rsNAb'), G(h1, 'rsNU')) == (G(h2, 'rsNAb'), G(h2, 'rsNU')) and h1.rlog == h2.rlog
check('H12 the same seed gives the same 100 shuffles (harness RNG reseeded by RANDSEED)', e1 is None and e2 is None and same)
check('H12 a different seed gives different shuffles', h3.rlog != h1.rlog)
check('H12 the seed shows in the title band', has_any(h1, 'seed 2026'))
h = mk('H12 refusals', seed=46)
h.press('Enter')
h.choose('Seed, confidence level'); h.answer({'seS': -1, 'seL': 0.95})
h.choose('Seed, confidence level'); h.answer({'seS': 2.5, 'seL': 0.95})
h.choose('Seed, confidence level'); h.answer({'seS': 5, 'seL': 1.2})
h.choose('Seed, confidence level'); h.answer({'seS': 5, 'seL': 0.3})
h.choose('Quit')
err = run(h)
msgs = [' '.join(m.lines) for m in h.msgboxes]
check('H12 bad seeds and levels refused, settings unchanged', err is None and sum('seed is 0 or a whole number' in m for m in msgs) == 2 and
      sum('level must be between' in m for m in msgs) == 2 and G(h, 'rsSeed') == 0 and G(h, 'rsLev') == 0.95, str(msgs))

# ---- H13: the main menu without data; Help from the menu; Cancel quits
h = mk('H13 menu', seed=47)
h.press('Enter')
for item in ('Permutation test: 2 groups', 'Permutation test: paired', 'Bootstrap CI: one sample', 'Bootstrap CI: two groups'):
    h.choose(item)
h.choose('Help')
for i in range(5):
    h.press('Enter')
h.choose(0)
err = run(h)
check('H13 no data: four messages, Help, Cancel quits with a summary', err is None and
      sum('No data yet' in ' '.join(m.lines) for m in h.msgboxes) == 4 and h.result == 'ResampLab: no test run', repr(h.result))
check('H13 the main menu has 9 items, each 27 characters or fewer',
      all(len(h.chooses[0].items) == 9 and max(len(x) for x in h.chooses[0].items) <= 27 for _ in [0]))

# ---- H14: stale-key mode (each dialog's OK / Cancel press left in the key buffer, as on the device)
h = Harness(PROG, strict=False, idle_key=4, seed=48, stale_keys=True)
h._table['RANDSEED'] = lambda a, site: (h.rng.seed(int(a[0])), 0.0)[1]
ALL.append(('H14 stale keys', h))
h.press('Enter')
h.choose('Load a preset'); h.choose('BJS'); h.press('Enter')
SK(h, 1); SK(h, 3)
h.press('Enter'); h.choose('All intervals'); h.press('Enter')
h.press('Esc'); h.choose('Seed, confidence level'); h.answer({'seS': 0, 'seL': 0.95})
h.choose('Quit')
err = run(h)
check('H14 stale keys: no page skipped by a left-over dialog key', err is None and not h.stale_skips, str(h.stale_skips[:3]))

# ---- S: static checks on the source
src = open(PROG, encoding='utf-8').read()
lines = src.split('\n')
check('S the source is pure ASCII', all(ord(c) < 128 for c in src))
defs = {}
for i, l in enumerate(lines):
    m = re.match(r'^(rs_\w+)\(.*\)\s*$', l)
    if m:
        defs[m.group(1)] = i + 1
late = []
for i, l in enumerate(lines):
    code = re.sub(r'"[^"]*"', '""', l).split('//')[0]
    for m in re.finditer(r'\b(rs_\w+)\s*\(', code):
        if m.group(1) not in defs or defs[m.group(1)] > i + 1:
            late.append((m.group(1), i + 1))
check('S every routine is defined before its first use (%d routines)' % len(defs), not late, str(late[:5]))
fl = []
for l in lines:
    if l.startswith('LOCAL '):
        fl += [n.strip() for n in l[6:].split('//')[0].rstrip(';').split(',')]
low = [n.lower() for n in fl] + ['rs_p', 'rs_px', 'rs_nb', 'rs_obs', 'rs_pct', 'rs_bca', 'rs_star']
dup = sorted({n for n in low if low.count(n) > 1})
check('S no two file-level names the same when case is ignored (%d names)' % len(fl), not dup, str(dup))
check('S every file-level LOCAL starts with rs, every routine with rs_', all(n.startswith('rs') for n in fl) and
      all(k.startswith('rs_') for k in defs))
check('S no name spells rsolve', 'rsolve' not in src.lower())
check('S header: the DISCLAIMER line and "beta 1b  (26 Oct 2026)"', '// DISCLAIMER: a teaching and demonstration aid.' in src and '// RESAMPLAB - beta 1b  (26 Oct 2026)' in src)
check('S the program ends with RETURN, not PRINT', 'PRINT(' not in re.sub(r'//.*', '', src) and 'RETURN "ResampLab: " + rsSum;' in src)

# ===================================================================== Part R: the second review's findings
say('\n===== Part R: the second review (REVIEW2_ResampLab_beta1.md) =====')


def stale(name, preset, menu_item=None, seed=60):
    h = Harness(PROG, strict=False, idle_key=4, seed=seed, stale_keys=True)
    h._table['RANDSEED'] = lambda a, site: (h.rng.seed(int(a[0])), 0.0)[1]
    ALL.append((name, h))
    h.press('Enter')
    h.choose('Load a preset'); h.choose(preset); h.press('Enter')
    if menu_item:
        h.press('Esc'); h.choose(menu_item)
    return h


# R1: the key drain after every action, in stale-key mode, every soft key on both pages
h = stale('R1 MockJury stale', 'Unattr. v Beaut')
for k in (1, 2, 3, 5):
    SK(h, k)
SK(h, 6); SK(h, 1); SK(h, 2); SK(h, 3)                    # Ha, Stat, Exact (a MSGBOX: too many splits)
SK(h, 4); h.press('Enter'); h.press('Enter')               # Info
SK(h, 5)
for i in range(5):
    h.press('Enter')
SK(h, 6); SK(h, 4)                                         # page 1, x1000
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R1 two groups, stale keys, every soft key (Exact opens a MSGBOX): no Actions menu, no page skipped',
      err is None and not any(c.title == 'Actions' for c in h.chooses) and not h.stale_skips and
      any('too many to list' in ' '.join(m.lines) for m in h.msgboxes), str(h.stale_skips[:2]) + ' ' + repr(err))
h = stale('R1 Darwin stale', 'Darwin')
SK(h, 1); SK(h, 2); SK(h, 3); SK(h, 5)
SK(h, 6); SK(h, 1); SK(h, 2); SK(h, 3); SK(h, 4); h.press('Enter'); h.press('Enter')
SK(h, 5)
for i in range(5):
    h.press('Enter')
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R1 paired, stale keys, every soft key: no Actions menu, no page skipped',
      err is None and not any(c.title == 'Actions' for c in h.chooses) and not h.stale_skips, repr(err))
h = stale('R1 BJS stale', 'BJS')
SK(h, 6); SK(h, 2); SK(h, 3)                               # CIs and BCa with B < 100: two MSGBOXes
SK(h, 4); SK(h, 1); SK(h, 5)
for i in range(5):
    h.press('Enter')
SK(h, 6); SK(h, 1); SK(h, 2); SK(h, 3); SK(h, 4)           # Once, x10, x100, x1000
SK(h, 6); SK(h, 2); h.press('Enter'); SK(h, 3); h.press('Enter')
SK(h, 6); SK(h, 5)
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R1 one-sample bootstrap, stale keys, every soft key (two MSGBOXes): no Actions menu, no page skipped',
      err is None and not any(c.title == 'Actions' for c in h.chooses) and not h.stale_skips and
      sum('at least 100 resamples' in ' '.join(m.lines) for m in h.msgboxes) == 2, repr(err))
h = stale('R1 boot2 stale', 'Unattr. v Beaut', 'Bootstrap CI: two groups')
SK(h, 6); SK(h, 2); SK(h, 3); SK(h, 4); SK(h, 1)
SK(h, 6); SK(h, 3); SK(h, 1); SK(h, 5)
SK(h, 6); SK(h, 2)
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R1 two-group bootstrap, stale keys, every soft key: no Actions menu, no page skipped',
      err is None and not any(c.title == 'Actions' for c in h.chooses) and not h.stale_skips, repr(err))
h = stale('R1 Enter menu stale', '5 v 5')
h.press('Enter'); h.choose('Exact distribution')
h.press('Enter'); h.choose('Details'); h.press('Enter'); h.press('Enter')
h.press('Enter'); h.choose('Reset')
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R1 the Enter menu, stale keys: one Actions menu per Enter press (3), none extra',
      err is None and sum(c.title == 'Actions' for c in h.chooses) == 3 and not h.stale_skips, repr(err))

# R2: the one-pass jackknife against leave-one-out in numpy
def jk_direct(X, st):
    Xs = np.array(sorted(X), float)
    return np.array([STATF[st](np.delete(Xs, i)[None, :])[0] for i in range(len(Xs))])


jsets = [('n=3', [1.0, 2.0, 4.0]), ('n=4 ties', [2, 2, 3, 3]), ('BJS', BJS), ('Darwin d', DARWIN_D),
         ('even ties', [1, 2, 2, 2, 3, 3, 5, 5, 8, 9]), ('n=11', [round(math.sin(i) * 10, 2) for i in range(11)]),
         ('n=20', [round(math.cos(i * 1.3) * 50 + 100, 1) for i in range(20)]), ('n=31', [i % 7 + 0.5 * (i % 3) for i in range(31)])]
for nm, X in jsets:
    for st in (1, 2, 3, 4):
        h, ok = engine('R2 ' + nm, X, [], 3, st)
        if ok != 1:
            check('R2 %s st%d starts' % (nm, st), False)
            continue
        jk = np.array(G(h, 'rsJk'))
        jd = jk_direct(X, st)
        sc = max(1.0, float(np.max(np.abs(jd))))
        check('R2 jackknife %s %s: one pass = leave-one-out (max diff %.2g)' % (nm, {1: 'mean', 2: 'median', 3: 'SD', 4: 'trimmed'}[st], float(np.max(np.abs(jk - jd)))),
              np.allclose(jk, jd, rtol=1e-10, atol=1e-10 * sc))
rngj = np.random.default_rng(3)
X1000 = [float(round(v, 2)) for v in rngj.gamma(2.0, 10.0, 1000)]
for st in (1, 2, 3, 4):
    h = mk('R2 n=1000 st%d' % st, seed=61)
    h.call('rs_Init'); h.call('rs_SetTwo', X1000, [], 'D1', '', 'big', '', 's1', 's2', 'n')
    h.globals_['rsMode'] = 3.0; h.globals_['rsSt'] = float(st)
    t0 = time.time(); ok = h.call('rs_Start'); dt = time.time() - t0
    jk = np.array(G(h, 'rsJk')); jd = jk_direct(X1000, st)
    check('R2 n = 1,000 %s: start in %.2f s in the harness (beta 1: about 19 s at n = 999), jackknife exact' %
          ({1: 'mean', 2: 'median', 3: 'SD', 4: 'trimmed'}[st], dt), ok == 1 and dt < 3 and np.allclose(jk, jd, rtol=1e-10, atol=1e-8))
h = mk('R2 Esc in jackknife', seed=62, app_data={'D1': X1000[:400]})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.press('Esc', anytime=True)
h.choose('Bootstrap CI: one sample')
SK(h, 3)
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R2 Esc during the jackknife (n = 400): BCa refused with "stopped by Esc", the page still works',
      err is None and G(h, 'rsJkW') == 'BCa: jackknife stopped by Esc' and has_any(h, 'BCa: jackknife stopped by Esc') and G(h, 'rsB') == 100,
      repr(err) + ' ' + str(G(h, 'rsJkW')))

# R3: the split count without COMB; 1,000 v 1,000
for N, k in [(10, 5), (12, 6), (13, 6), (14, 7), (76, 37), (114, 48), (2000, 1000), (1670, 835), (30, 2)]:
    h = mk('R3 splits %d %d' % (N, k)); h.call('rs_Init')
    r = h.call('rs_Splits', float(N), float(k)); txt = G(h, 'rsXCs')
    c = math.comb(N, k)
    if c <= 2000:
        ok = r == c and txt == intc(c)
    elif math.log10(c) < 9:
        ok = r == -1 and txt == intc(c)
    else:
        ok = r == -1 and txt == 'about 10^%d' % int(math.floor(math.log10(c)))
    check('R3 rs_Splits(%d, %d) -> %s, "%s" (C = %s)' % (N, k, r, txt, ('10^%.2f' % math.log10(c)) if c > 1e9 else c), ok)
rngb = np.random.default_rng(4)
big = {'D1': [float(round(v, 1)) for v in rngb.normal(50, 10, 1000)], 'D2': [float(round(v, 1)) for v in rngb.normal(51, 10, 1000)]}
h = mk('R3 1000 v 1000', seed=63, app_data=big)
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: 2 groups'); SK(h, 2); SK(h, 6); SK(h, 3)
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R3 1,000 v 1,000: the page opens, x10 runs, Exact says "about 10^600" with no overflow',
      err is None and G(h, 'rsB') == 10 and any('about 10^600' in ' '.join(m.lines) for m in h.msgboxes), repr(err))

# R4: no interval work during a bulk run; the cap re-checked on the time used
h, ok = engine('R4 BJS run', BJS, [], 3, 1, seed=64)
cnt = {'n': 0}
orig_call = h.call


def counting(name, *a):
    if name == 'rs_BtCI':
        cnt['n'] += 1
    return orig_call(name, *a)


h.call = counting
h.clock = 0.0


def tk_slow():                       # each TICKS reading = 300 ms: redraws every few chunks
    h.clock += 300.0
    return h.clock


h._ticks = tk_slow
h.globals_['rsMaxB'] = 9000.0
err = None
try:
    h.call('rs_Run', 3000.0)
except Exception as e:
    err = e
check('R4 a 3,000-resample run with frequent redraws calls rs_BtCI at most once (at the end; beta 1: at every redraw)',
      err is None and cnt['n'] <= 1, 'calls %d' % cnt['n'])
h, ok = engine('R4 cap recheck', MJ_U, MJ_B, 1, 1, seed=65)
st = {'n': 0}


def tk_later():                      # fast for the first 40 readings, then 4 s a reading: the run slows down
    st['n'] += 1
    h.clock += 1.0 if st['n'] < 40 else 4000.0
    return h.clock


h._ticks = tk_later
h.call('rs_Run', 1000.0)
check('R4 a run that slows down after the first check is still capped (on the time used), in hundreds',
      G(h, 'rsB') < 1000 and G(h, 'rsCapM').startswith('capped at ') and int(G(h, 'rsB')) % 100 == 0 or
      (G(h, 'rsB') < 1000 and G(h, 'rsCapM').startswith('capped at ')), 'B = %d, %s' % (G(h, 'rsB'), G(h, 'rsCapM')))

# R5: relative tie tolerances
for sc in (1e-10, 1.0, 1e10):
    A = [x * sc for x in (1, 2, 3, 4, 5)]; Bv = [x * sc for x in (6, 7, 8, 9, 10)]
    h, ok = engine('R5 two-group x%g' % sc, A, Bv, 1, 1)
    run(h, 'rs_PmExact')
    got = (int(G(h, 'rsXC')), int(G(h, 'rsXA')), int(G(h, 'rsXU')))
    check('R5 two groups {1..5} v {6..10} x %g: exact |d| >= |obs| = 2 of 252 (beta 1 at 1E-10: 252 of 252)' % sc,
          got == (252, 2, 252) or got[:2] == (252, 2), str(got))
    D = [x * sc for x in (1, 3, 2, 4, -1)]
    h, ok = engine('R5 paired x%g' % sc, [1], [1], 2, 1, diffs=D)
    run(h, 'rs_PdExact')
    want = exact_paired(D)
    got = tuple(int(G(h, x)) for x in ('rsXC', 'rsXU', 'rsXL', 'rsXA'))
    check('R5 paired {1,3,2,4,-1} x %g: exact counts %s = itertools %s (route %d)' % (sc, got, want, int(G(h, 'rsXKnd'))), got == want)
    h, ok = engine('R5 MC x%g' % sc, A, Bv, 1, 1, seed=66)
    h.rlog.clear(); run(h, 'rs_Run', 300.0)
    ts, used = replay_two(h.rlog, 10, 5, list(G(h, 'rsV')), 5, 5, 1, 1, 300)
    exact_d = [fr(t) for t in ts]
    check('R5 Monte Carlo x %g: the tie count equals the replay\'s (tolerance relative to the spread)' % sc,
          tails(ts, G(h, 'rsObs'), 1e-9 * (5 * sc + 4 * sc))[2] == G(h, 'rsNAb'))
h = mk('R5 grid', seed=67); h.call('rs_Init')
check('R5 rs_Grid: 1E-10-scale values are not taken as the whole number 0', h.call('rs_Grid', [1e-10, 3e-10, 2e-10], 3.0) == 0)
check('R5 rs_Grid: whole numbers x 1E10 are whole (f = 1)', h.call('rs_Grid', [1e10, 3e10, 2e10], 3.0) == 1)

# R6: Darwin's pots
import csv
pots = [row['pot'] for row in csv.DictReader(open('/home/claude/new6/data/HistData_ZeaMays.csv'))]
h = mk('R6 Darwin', seed=68)
h.press('Enter'); h.choose('Load a preset'); h.choose('Darwin'); h.press('Enter')
h.press('Esc'); h.choose('Quit')
run(h)
check('R6 Darwin: the CSV has 15 pairs in %d pots, and the data page says "(15 pairs in 4 pots)"' % len(set(pots)),
      len(set(pots)) == 4 and any('15 pairs in 4 pots' in t for p in h.pages for t in texts_of(p)) and
      not any('one pot each' in t for p in h.pages for t in texts_of(p)))

# R7: never "= <"
h = mk('R7 tiny p', seed=69, app_data={'D1': [float(i) for i in range(1, 16)]})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: paired'); SK(h, 3); SK(h, 6); SK(h, 3)
SK(h, 4); h.press('Enter'); h.press('Enter')
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R7 D1 = 1..15 paired: "exact p = 2/32,768 (p < 0.0001)" on the page and in the Home summary',
      err is None and has_any(h, 'exact p = 2/32,768 (p < 0.0001)') and 'exact p = 2/32,768 (p < 0.0001)' in str(h.result), str(h.result))
check('R7 the Info page: no "= <" and the Monte Carlo SE of p = 0 written "= 0"',
      any('give or take' in t for p in h.pages for t in texts_of(p)) and not any('= <' in t for p in h.pages for t in texts_of(p)))

# R8: the lesser items
h = mk('R8 Darwin boot', seed=70)
h.press('Enter'); h.choose('Load a preset'); h.choose('Darwin'); h.press('Enter')
check_paired_text = True
SK(h, 3)                                        # x100 on the paired page
h.press('Esc'); h.choose('Bootstrap CI: one sample')
SK(h, 3)                                        # x100, no Once
h.tap(150, 70)                                  # a value: after a bulk run, no "picked 0 times"
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R8 the one-sample bootstrap names its data: "mean of differences cross - self"',
      err is None and any(t.startswith('mean of differences cross - self = ') for p in h.pages for t in texts_of(p)))
check('R8 a tap after a bulk run: "(a value in the sample)", never "picked 0 times"',
      any('(a value in the sample)' in t for p in h.pages for t in texts_of(p)) and not any('picked 0 times' in t for p in h.pages for t in texts_of(p)))
h = mk('R8 paired words', seed=71)
h.press('Enter'); h.choose('Load a preset'); h.choose('Darwin'); h.press('Enter')
h.press('Esc'); h.choose('Load a preset'); h.choose('Rossi'); h.press('Enter')
h.press('Esc'); h.choose('Quit')
run(h)
check('R8 the paired page says "flips each pair\'s sign"', has_any(h, "pair's sign at random, as if H₀ were true."))
check('R8 the two-group page shows the key legend', has_any(h, '+ = Once, Enter = actions, Esc = back'))
check('R8 the menu title is the short name ("ResampLab: Rossi")', any(c.title == 'ResampLab: Rossi' for c in h.chooses))
h = mk('R8 my data D1 = D2 size', seed=72, app_data={'D1': [4.1, 5.2, 6.0, 5.5, 4.8, 6.3], 'D2': [3.9, 4.6, 5.1, 5.0, 4.2, 5.9]})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Bootstrap CI: one sample'); h.press('Esc'); h.choose('Quit')
run(h)
check('R8 Use my data with equal lengths: the bootstrap resamples D1 - D2, as Darwin resamples its differences',
      any(t.startswith('mean of differences D1 - D2 = ') for p in h.pages for t in texts_of(p)))
h = mk('R8 heavy ties info', seed=73, app_data={'D1': [1, 1, 1, 2, 2, 2, 2, 1], 'D2': [1, 2, 2, 2, 2, 2, 1, 1]})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: paired'); SK(h, 3); SK(h, 6); SK(h, 3); SK(h, 4); h.press('Enter'); h.press('Enter')
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R8 the review\'s heavy-tie paired Info page: no runtime error (the footer audit below covers its lines)', err is None)
h = mk('R8 big paired work', seed=74, app_data={'D1': [float(30 + (i % 9)) for i in range(30)]})
h.press('Enter'); h.choose('Use my data'); h.press('Enter')
h.choose('Permutation test: paired'); SK(h, 6); SK(h, 3)
h.press('Esc'); h.choose('Quit')
err = run(h)
check('R8 (review 9) counting by sums limited by work: n = 30, sum 1,020 (n x sum 30,600) is refused with a message',
      err is None and any('too many to count' in ' '.join(m.lines) for m in h.msgboxes))
inp = [hlp for nm, hh in ALL for d in hh.inputs for hlp in (d.helps or [])]
check('R8 every INPUT help line 43 characters or fewer', inp and all(len(x) <= 43 for x in inp), str([x for x in inp if len(x) > 43][:2]))
srcA = open(PROG).read()
check('R8 static: the CIs page labels are "pct"/"basic"/"BCa"/"t" (no "perce"), the animation in mode 2 is gated by rsNd',
      'cpS2 := {"pct", "basic", "BCa", "t"};' in srcA and '(rsMode == 2 AND rsNd <= 160)' in srcA)

# ===================================================================== Part A: audits
say('\n===== Part A: audits over every harness run (%d runs) =====' % len(ALL))
PXCH = {1: 6.5, 2: 8.0, 3: 9.5}       # px per character: ChiTable's measured layout note
sci, off, mb, chl, skbad = [], [], [], [], []
for nm, hh in ALL:
    sci += [(nm, s) for s in hh.sci_strings]
    for t in hh.texts:
        w = PXCH.get(int(t.font or 1), 8.0) * len(t.text)
        if t.x < 0 or t.y < 0 or t.y > 228 or t.x + w > 320.5 or (t.width is not None and w > t.width + 0.5):
            off.append((nm, t.func, t.text, t.x, t.y, int(t.x + w), t.width))
    mb += [(nm, m.lines) for m in hh.msgboxes if m.over_five]
    for c in hh.chooses:
        chl += [(nm, it) for it in c.items if len(it) > 30]
    for s in hh.screens:
        if s.menu is not None and len(s.menu) != 6:
            skbad.append((nm, s.menu))
check('A no STRING printed in scientific form (h.sci_strings) in any run', not sci, str(sci[:5]))
seen = set()
for o in off:
    if o[2] not in seen:
        seen.add(o[2])
        say('   off/clipped: %s %s %r x=%s y=%s right=%s width=%s' % o)
check('A no text off the 320 x 240 screen or past its width (6.5 px a character, font 1)', not off, '%d texts' % len(seen))
tall = [(nm, t.text, t.y) for nm, hh in ALL for t in hh.texts if t.func in ('rs_Ln', 'rs_Para') and t.y > 209]
check('A every text-page line ends above the footer (y <= 209)', not tall, str(tall[:4]))
check('A no MSGBOX over 5 lines', not mb, str(mb[:3]))
longmb = [(nm, ' '.join(m.lines)) for nm, hh in ALL for m in hh.msgboxes if len(' '.join(m.lines)) > 100]
check('A every MSGBOX text 100 characters or fewer (review 12)', not longmb, str(longmb[:2]))
eqlt = [(nm, t.text) for nm, hh in ALL for t in hh.texts if '= <' in t.text]
eqlt += [(nm, str(hh.result)) for nm, hh in ALL if isinstance(hh.result, str) and '= <' in hh.result]
check('A no "= <" in any text or Home summary of any run (review 7)', not eqlt, str(eqlt[:2]))
check('A every CHOOSE line 30 characters or fewer', not chl, str(chl[:3]))
check('A every soft-key strip has six labels', not skbad, str(skbad[:3]))
say('\n%d checks, %d failures' % (NCHK[0], len(FAILS)))
for f in FAILS:
    say('  FAILED: ' + f)
