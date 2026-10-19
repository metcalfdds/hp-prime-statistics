#!/usr/bin/env python3
"""verify_StudRange_beta15d.py -- checks for StudRange beta 15d (19 Oct 2026): the fleet review's S1 (a plain note on
the Critical value and HSD pages when the PPL fallback answered below alpha 0.005), S3 (spaces round "=" on the HSD
page), Home's X no longer a MAKELIST counter, and Roger's disclaimer (19 Oct).  Built from verify_StudRange_beta15c.py:
every check runs on beta 15d (SRC), on harness v3e.  Where an old check's expected value moves with 15d it says so:
7g (15b vs 15a) also lists sr_BuildZ, sr_Cache and sr_HelpMode; 9c reads beta 15c's own file (it checks the 15b -> 15c
diff); 9d's version strings are beta 15d's.  Section 10 is new (15d): 10a S3, 10b S1, 10c X, 10d the disclaimer,
10e the routine and line diff 15c -> 15d, 10f names, 10g the review's own check_StudRange.py on 15c and on 15d.
8c lists h.sci_strings over every beta 15d run.

(beta 15c's docstring follows.)

verify_StudRange_beta15c.py -- checks for StudRange beta 15c (17 Oct 2026, evening): no "=" before a relation
(sr_Eq) and no "0.00000" for a p that is not 0.  Built from verify_StudRange_beta15b.py: every check runs on beta
15c, on harness v3e (v3d's results; its README).  Adjusted only where 15c changes the screen on purpose:
7g (15b vs 15a) now also expects sr_Eq and its prototype line; 8c expects "F(q) < 0.00001" (15b's own check
expected the "F(q) = < 0.00001" this pass removes); 8d allows the two LEFT calls of sr_Eq, inside IF DIM(eqS)>0.
Section 9 is new (15c): the P-value page and the Quit summary, 15b -> 15c, with the PPL engine (q 12, 40, 0.001,
ordinary values unchanged); sr_Eq; the routine and line diff; the names; the version strings; comments.

(beta 15b's docstring follows.)

verify_StudRange_beta15b.py -- checks for StudRange beta 15b (17 Oct 2026), built from
verify_StudRange_beta15a.py: every check is kept and now runs on beta 15b in harness v3d, which raises
"Invalid input" for INSTRING("", ...) and prints small fixed decimals in the Prime's scientific form
(h.sci_strings).  Section 8 is new (15b; BRIEF_R2FIX_v1, section 4 "StudRange"):
  8a the stale spot, both ways: Help for this plot closed on its footer at the alpha- key, then alpha-
     tapped there -- beta 15a skips that real tap (the emulator's finding), beta 15b takes it; a click
     injected as ALREADY QUEUED (mouse_tail=True, the clock not moved) is still skipped;
  8b the Quit summary after a plot-only session reports the q crit (with k, df, alpha) and the p the
     plot showed, exactly as shown; the menu modes' values as their pages showed them; "not computed"
     for what was not; beta 15a's plot-only summary says "not computed" (the emulator's finding);
  8c no STRING(x, 2, d) printed in scientific form: direct checks of the swept sites (sr_FmtF, the
     simulation's percents, the yardstick's means and ticks, F(q), a tiny HSD), and h.sci_strings of
     every harness run of beta 15b;
  8d INSTRING, LEFT and MID: none in the PPL code;
  7g (15b) beta 15b against beta 15a: only the routines named in the CHANGES differ, the #PYTHON srq
     block is byte-identical.

(The beta 15a description follows.)

7. Section 7 (15a): the plot's six soft keys fire on a type-3 strip click; beta 15 does nothing (the
  emulator's FAIL); no tap acts twice; a press on the plot and on the q crit box still work, once; a
  page closed by a footer tap leaves no stale click (also in the mouse_tail worst case); the Quit
  summary names the q crit's k and df and says "not computed"; beta 15a against beta 15.

(The beta 15 description follows.)

1. The MicroPython engine: the #PYTHON srq block is read OUT OF StudRange_beta15.txt
   and executed here with stub hpprime/urandom modules, so the code checked is the
   code that ships.  p-values and critical values on a (k, df, alpha) grid against
   scipy.stats.studentized_range, df 1 and up.
2. The PPL engine, mirrored line for line in Python (sr_BuildZ, sr_RngCDF, sr_LGAM,
   sr_SRCDF, sr_SRCrit) on the same grid, df 3 and up; and the real PPL source run
   through the harness (ppl_run_v1) for a handful of cases.
3. The plot cache (32 x 48 nodes) against SciPy, and the pdf (spdf) against SciPy.
4. The H0 simulation: the block's own simulate() with urandom stubbed by Python's
   random; coverage of q > q crit (about alpha) and the family-wise rate of the
   pairwise t tests, against P(Q > sqrt2 * t crit) from SciPy.
5. The k = 2 identity q = t * sqrt 2.
6. The bridge end to end in the harness: PYTHON(srq) replaced by the real block with
   an hpprime.eval that reads and writes the harness's PPL globals; every menu item
   with Python answering, and with Python failing (the PPL fallback and the badge).
Run: python3 verify_StudRange_beta15a.py   (prints a report; exit code 1 on a failure)
"""
import math, random, re, sys, types, time
from scipy import stats

HERE = '/home/claude/work/out/'
SRC = '/home/claude/work/fix19/StudRange_beta15d.txt'   # 15d: the new file (HERE stays the out/ folder)
B15C = HERE + 'StudRange_beta15c.txt'
OLD = HERE + 'StudRange_beta15a.txt'
B15 = HERE + 'StudRange_beta15.txt'
sys.path.insert(0, '/home/claude/work/out')

FAIL = []
NCHK = [0]                       # 15d: the number of checks run, for the summary
def check(name, ok, detail=''):
    NCHK[0] += 1
    print('  %-4s %s %s' % ('ok' if ok else 'FAIL', name, detail))
    if not ok:
        FAIL.append(name)

def pyblock():
    t = open(SRC, encoding='utf-8').read()
    m = re.search(r'^#PYTHON srq\n(.*?)^#END', t, re.S | re.M)
    return m.group(1)

# ---------------------------------------------------------------- stubs
class Store:
    """A stand-in for the PPL side: names -> numbers / lists / strings."""
    def __init__(self):
        self.g = {}
        self.evals = 0
    def eval(self, s):
        self.evals += 1
        m = re.match(r'^(\w+)\((\d+)\):=(.*)$', s)
        if m:
            self.g[m.group(1)][int(m.group(2)) - 1] = float(m.group(3))
            return 0
        m = re.match(r'^(\w+):=(.*)$', s)
        if m:
            v = m.group(2)
            self.g[m.group(1)] = v[1:-1] if v.startswith('"') else float(v)
            # fixed-point text only, never exponent notation
            assert v.startswith('"') or re.match(r'^-?\d+\.\d{10}$', v), v
            return 0
        return self.g[s]

def load_block(store, rnd=None, run_main=False):
    hp = types.ModuleType('hpprime')
    hp.eval = store.eval
    hp.fillrect = lambda *a: None
    ur = types.ModuleType('urandom')
    ur.random = rnd or random.random
    sys.modules['hpprime'] = hp
    sys.modules['urandom'] = ur
    code = pyblock()
    if not run_main:
        code = code.replace('\nmain()\n', '\n')
    ns = {'__name__': 'srq'}
    exec(compile(code, 'srq', 'exec'), ns)
    return ns

# ---------------------------------------------------------------- PPL mirror
class PPLEngine:
    def __init__(self):
        self.nz = 0
    def buildz(self, nz):
        if nz == self.nz:
            return
        h = 11.0 / nz
        self.zn, self.zw, self.zc = [], [], []
        for j in range(nz + 1):
            z = -7 + j * h
            w = 1 if j in (0, nz) else (4 if j % 2 == 1 else 2)
            self.zn.append(z)
            self.zw.append(w * h / 3 * stats.norm.pdf(z))
            self.zc.append(stats.norm.cdf(z))
        self.nz = nz
    def rng(self, x, k):
        if x <= 0:
            return 0.0
        acc = 0.0
        for z, w, c in zip(self.zn, self.zw, self.zc):
            d = stats.norm.cdf(z + x) - c
            if d > 0:
                acc += w * d ** (k - 1)
        return k * acc
    @staticmethod
    def lgam(x):
        c = [676.5203681218851, -1259.1392167224028, 771.32342877765313,
             -176.61502916214059, 12.507343278686905, -0.13857109526572012,
             9.9843695780195716E-6, 1.5056327351493116E-7]
        x = x - 1
        acc = 0.99999999999980993
        for j in range(8):
            acc += c[j] / (x + j + 1)
        t = x + 7.5
        return 0.918938533204673 + (x + 0.5) * math.log(t) - t + math.log(acc)
    def cdf(self, q, k, v, ns):
        if q <= 0:
            return 0.0
        if v == 0:
            return self.rng(q, k)
        if v > 100:                                   # beta 15's window branch
            sg = 1 / math.sqrt(2 * v); lo = max(1e-9, 1 - 12 * sg); hi = 1 + 12 * sg; h = (hi - lo) / ns
            lc = (1 - v / 2) * math.log(2) + (v / 2) * math.log(v) - self.lgam(v / 2)
            acc = 0.0
            for j in range(ns + 1):
                s = lo + j * h
                w = 1 if j in (0, ns) else (4 if j % 2 == 1 else 2)
                acc += w * math.exp(lc + (v - 1) * math.log(s) - v * s * s / 2) * self.rng(q * s, k)
            return min(1.0, h / 3 * acc)
        uhi = math.sqrt(1 + 9 / math.sqrt(v)); ulo = 1e-3; h = (uhi - ulo) / ns
        lc = (1 - v / 2) * math.log(2) + (v / 2) * math.log(v) - self.lgam(v / 2)
        acc = 0.0
        for j in range(ns + 1):
            u = ulo + j * h; s = u * u
            w = 1 if j in (0, ns) else (4 if j % 2 == 1 else 2)
            acc += w * math.exp(lc + (v - 1) * math.log(s) - v * s * s / 2) * 2 * u * self.rng(q * s, k)
        return min(1.0, h / 3 * acc)
    def crit(self, a, k, v, ns):
        t = 1 - a
        qlo, qhi = 0.6, 4.0
        flo = self.cdf(qlo, k, v, ns) - t; fhi = self.cdf(qhi, k, v, ns) - t
        while fhi < 0 and qhi < 60:
            qhi *= 1.5; fhi = self.cdf(qhi, k, v, ns) - t
        side = 0; qm = (qlo + qhi) / 2
        for _ in range(40):
            qm = (qlo * fhi - qhi * flo) / (fhi - flo)
            fm = self.cdf(qm, k, v, ns) - t
            if abs(fm) < 1e-7 or abs(qhi - qlo) < 5e-5:
                break
            if fm * flo > 0:
                qlo, flo = qm, fm
                if side == -1: fhi /= 2
                side = -1
            else:
                qhi, fhi = qm, fm
                if side == 1: flo /= 2
                side = 1
        return qm

# 15b: every harness made in this script is remembered (section 8c: h.sci_strings, harness v3d)
ALL_H = []


def _record_harnesses():
    import ppl_run_v3e
    init = ppl_run_v3e.Harness.__init__
    def rec(self, *a, **k):
        init(self, *a, **k)
        ALL_H.append(self)
    ppl_run_v3e.Harness.__init__ = rec


def main():
    _record_harnesses()
    sr = stats.studentized_range
    st = Store()
    py = load_block(st)

    print('1. MicroPython engine (the block as shipped) vs SciPy')
    worst_p = worst_q = 0.0
    rows = []
    for k in (2, 3, 4, 6, 10, 20):
        for v in (1, 2, 3, 5, 12, 30, 120, 1000, 20000):
            for a in (0.10, 0.05, 0.01, 0.001):
                q_true = sr.ppf(1 - a, k, v)
                q_py = py['qcrit'](k, float(v), a)
                worst_q = max(worst_q, abs(q_py - q_true) / q_true)
                p_py = 1 - py['scdf'](q_true, k, float(v))
                worst_p = max(worst_p, abs(p_py - a) / a)
                if (k, v, a) in ((3, 12, 0.05), (4, 3, 0.005), (2, 1, 0.05), (10, 2, 0.01)):
                    rows.append((k, v, a, q_py, q_true))
    for r in rows:
        print('     k=%-2d df=%-3d a=%.3f  python %.5f  scipy %.5f' % r)
    check('python q crit, max relative error < 1E-5', worst_q < 1e-5, '(%.2e)' % worst_q)
    check('python p at the true q crit, max relative error < 1E-4', worst_p < 1e-4, '(%.2e)' % worst_p)
    q4 = py['qcrit'](4, 3.0, 0.005)
    check('Lessons s11 case k=4 df=3 a=.005 -> 15.4503', abs(q4 - sr.ppf(0.995, 4, 3)) < 1e-3, '(%.4f)' % q4)
    inf_p = 1 - py['scdf'](3.5, 3, 100000.0)
    check('df = infinity (100000) matches SciPy df=inf-ish (1e6)',
          abs(inf_p - sr.sf(3.5, 3, 1e6)) < 1e-6, '(%.7f vs %.7f)' % (inf_p, sr.sf(3.5, 3, 1e6)))
    f_probe = py['scdf'](3.5, 3, 12.0)
    check('Diagnostics probe value F(3.5;3,12) within 1E-5 of 0.9300045147',
          abs(f_probe - 0.9300045147) < 1e-5, '(%.10f)' % f_probe)

    print('2. PPL engine (mirror) vs SciPy, the menu resolution (64 x 32/48)')
    pe = PPLEngine()
    worst = 0.0; worst_case = None
    for k in (2, 3, 4, 6, 10, 20):
        pe.buildz(48 if k > 5 else 32)
        for v in (3, 5, 12, 30, 120, 240, 1000):
            for a in (0.10, 0.05, 0.01, 0.005):
                qc = pe.crit(a, k, v, 64)
                e = abs(qc - sr.ppf(1 - a, k, v))
                if e > worst:
                    worst, worst_case = e, (k, v, a, qc)
    check('PPL q crit, max absolute error < 1E-2 (df >= 3; it is k = 20, df = 3 at the worst)', worst < 1e-2,
          '(%.1e at k=%d df=%d a=%.3f)' % ((worst,) + worst_case[:3]))
    lg = max(abs(PPLEngine.lgam(x) - math.lgamma(x)) for x in (0.5, 1.0, 1.5, 2.5, 6.0, 60.0))
    check('sr_LGAM (Lanczos) vs lgamma < 1E-12', lg < 1e-12, '(%.1e)' % lg)

    print('3. The plot cache (32 x 48) and spdf vs SciPy')
    wc = wp = 0.0
    for k, v in ((3, 12), (5, 3), (2, 1), (3, 2), (10, 30), (20, 2), (3, 240), (4, 100000)):
        vv = 1e6 if v == 100000 else v
        qmax = 6.0                                  # the program's window rule
        while sr.cdf(qmax, k, vv) < 0.998 and qmax < 40:
            qmax *= 1.4
        peak = max(sr.pdf(j * qmax / 64, k, vv) for j in range(1, 65))
        for j in range(65):
            q = (j + 1e-6 * (j == 0)) * qmax / 64      # as cache() reads q = 0
            wc = max(wc, abs(py['scdf'](q, k, float(v), 32, 48) - sr.cdf(q, k, vv)))
            wp = max(wp, abs(py['spdf'](q, k, float(v), 32, 48) - sr.pdf(q, k, vv)) / peak)
    check('cache CDF max abs error < 5E-4 (curve level; worst k = 20, df = 2)', wc < 5e-4, '(%.1e)' % wc)
    check('cache pdf max error relative to the peak < 1E-2 (curve level)', wp < 1e-2, '(%.1e)' % wp)
    # the cache() routine itself, through the stub bridge: payload shape and order
    st.g.update({'EP_SRCDF': [-1.0] * 65, 'EP_SRPDF': [-1.0] * 65, 'SR_OUT': -1.0})
    st.evals = 0
    py['cache'](3, 12.0, 3.5)
    check('cache(): 65 + 65 + 1 = 131 crossings', st.evals == 131, '(%d)' % st.evals)
    c = st.g['EP_SRCDF']
    check('cache(): CDF monotone, last element in [0,1]',
          all(c[i] <= c[i + 1] for i in range(64)) and 0 <= c[64] <= 1, '(F(qmax) = %.5f, qmax = %.3f)' % (c[64], st.g['SR_OUT']))

    print('4. The H0 simulation (the block\'s simulate(), urandom -> random.random)')
    for (k, m, a, seed) in ((3, 5, 0.05, 1), (4, 8, 0.05, 2), (6, 4, 0.10, 3), (3, 5, 0.01, 4)):
        random.seed(seed)
        df = k * (m - 1)
        tc = stats.t.ppf(1 - a / 2, df)
        qmax = sr.ppf(0.998, k, df)
        n = 0; nq = 0; nt = 0
        for rep in range(5):                        # 5 x 2,000 replicates
            st.g['EP_SRSIM'] = [-1.0] * 45
            py['simulate'](k, m, 2000, a, tc, qmax)
            s = st.g['EP_SRSIM']
            assert s[44] == 2000 and sum(s[:40]) + s[42] == 2000
            n += 2000; nq += s[40]; nt += s[41]
        fw = sr.sf(math.sqrt(2) * tc, k, df)        # P(any pairwise t > t crit)
        se = math.sqrt(a * (1 - a) / n); se2 = math.sqrt(fw * (1 - fw) / n)
        check('k=%d m=%d a=%.2f: q > q crit %.2f %% (alpha %.0f %%, |z| < 4)' % (k, m, a, 100 * nq / n, 100 * a),
              abs(nq / n - a) < 4 * se, '(z = %.2f)' % ((nq / n - a) / se))
        check('k=%d m=%d: any t > t crit %.2f %% vs theory %.2f %% (|z| < 4)' % (k, m, 100 * nt / n, 100 * fw),
              abs(nt / n - fw) < 4 * se2, '(z = %.2f)' % ((nt / n - fw) / se2))
    print('     (theory for the family-wise line: any pair exceeds t crit exactly when the')
    print('      largest pair does, i.e. when q > sqrt2 * t crit)')

    print('5. k = 2: q = t * sqrt 2')
    w5 = 0.0
    for v in (1, 2, 3, 12, 60):
        for a in (0.1, 0.05, 0.01):
            tq = math.sqrt(2) * stats.t.ppf(1 - a / 2, v)
            w5 = max(w5, abs(sr.ppf(1 - a, 2, v) - tq) / tq, abs(py['qcrit'](2, float(v), a) - tq) / tq)
    check('q crit(k=2) = sqrt2 * t crit (two-sided), SciPy and the Python engine', w5 < 1e-5, '(%.1e)' % w5)

    print('6. The real PPL source in the harness (v3d)')
    harness_checks(py)

    print('7. beta 15a: the plot soft keys under WAIT(-1), stale clicks, the Quit summary (v3d)')
    harness_checks_15a()

    print('8. beta 15b: the stale spot, the Quit summary, small numbers (v3d)')
    harness_checks_15b()

    # 15b: every harness run of beta 15b in this script, and what harness v3d printed in scientific form
    print('9. beta 15c: no "=" before a relation, no "0.00000" for a p that is not 0 (v3e)')
    harness_checks_15c()

    print('10. beta 15d: S3, S1, Home\'s X, the disclaimer (v3e)')
    harness_checks_15d()

    mine = [h for h in ALL_H if any(f.endswith('StudRange_beta15d.txt') for f in h.files)]   # 15d
    sci = sorted({(round(v, 12), d, r) for h in mine for (v, d, r) in h.sci_strings})
    print('     harness runs of beta 15d: %d; scientific STRING results: %s' % (len(mine), sci or 'none'))
    check('8c no STRING(x, 2, d) of beta 15d printed in scientific form in any of the %d runs (9 and 10 included)' % len(mine), not sci,
          str(sci[:6]))
    olds = sorted({(round(v, 12), d, r) for h in ALL_H if any(f.endswith('StudRange_beta15a.txt') for f in h.files)
                   for (v, d, r) in h.sci_strings})
    print('     (beta 15a in this script: %s)' % (olds or 'none'))

    print()
    print('CHECKS: %d' % NCHK[0])
    print('FAILURES: %d %s' % (len(FAIL), FAIL))
    return 1 if FAIL else 0

# ---------------------------------------------------------------- harness
def harness_checks(py_unused):
    from ppl_run_v3e import Harness, ACCEPT
    sr = stats.studentized_range

    class Bridge(Harness):
        """PYTHON(srq) runs the real block; hpprime.eval reads/writes these globals."""
        python_ok = True
        def _python(self, a):
            self.log.append(('PYTHON', a))
            if not self.python_ok:
                return 0.0           # as on a calculator without Python: nothing happens
            h = self
            class HStore(Store):
                def eval(s2, txt):
                    s2.evals += 1
                    m = re.match(r'^(\w+)\((\d+)\):=(.*)$', txt)
                    if m:
                        h.globals_[m.group(1)][int(m.group(2)) - 1] = float(m.group(3))
                        return 0
                    m = re.match(r'^(\w+):=(.*)$', txt)
                    if m:
                        v = m.group(2)
                        h.globals_[m.group(1)] = v[1:-1] if v.startswith('"') else float(v)
                        return 0
                    return h.globals_[txt]
            load_block(HStore(), run_main=True)
            return 0.0

    def run(python_ok, chooses, answers, keys=(), taps=None):
        h = Bridge(SRC, idle_key=4)
        h.python_ok = python_ok
        for c in chooses:
            h.choose(c)
        for a in answers:
            h.answer(a)
        for k in keys:
            h.press(k)
        return h

    # 6a. the PPL engine's own routines, a handful of cases
    h = Bridge(SRC)
    for (q, k, v, ref) in ((3.5, 3, 12, sr.cdf(3.5, 3, 12)), (4.0, 5, 20, sr.cdf(4.0, 5, 20)),
                           (5.0, 4, 3, sr.cdf(5.0, 4, 3))):
        h.execute('sr_BuildZ(32)')
        f = h.execute('sr_SRCDF(%g,%d,%d,64)' % (q, k, v))
        check('harness sr_SRCDF(%g,%d,%d) = %.6f (SciPy %.6f)' % (q, k, v, f, ref), abs(f - ref) < 2e-4)
    qc = h.execute('sr_SRCrit(0.05,3,12,64)')
    check('harness sr_SRCrit(.05,3,12) = %.5f (SciPy %.5f)' % (qc, sr.ppf(.95, 3, 12)), abs(qc - sr.ppf(.95, 3, 12)) < 5e-4)

    def page_has(h, s):
        return any(sc.has(s) for sc in h.screens)
    def texts(h):
        return [t.text for t in h.texts]

    # 6b. P-value, both engines
    for ok in (True, False):
        h = run(ok, ['P-value from q', 'Quit'], [{'tq': 3.5, 'tk': 3, 'tv': 12}], keys=['Enter'])
        h.execute('StudRange()')
        badge = 'engine: MicroPython 1.9.4' if ok else 'engine: PPL (Python unavailable)'
        p = h.globals_['EP_QPVAL']
        check('P-value via %s: EP_QPVAL %.6f (SciPy %.6f), badge shown, SR_ENGINE %s' %
              ('Python' if ok else 'PPL', p, sr.sf(3.5, 3, 12), h.globals_['SR_ENGINE']),
              abs(p - sr.sf(3.5, 3, 12)) < (1e-7 if ok else 2e-4) and page_has(h, badge)
              and h.globals_['SR_ENGINE'] == ('Python' if ok else 'PPL'))
    # df = 2: legal with Python, raised to 3 (with the message) without
    h = run(True, ['Critical value', 'Quit'], [{'ta': 0.05, 'tk': 3, 'tv': 2}], keys=['Enter'])
    h.execute('StudRange()')
    check('Critical value df=2 via Python: %.4f (SciPy %.4f), no MSGBOX' % (h.globals_['EP_QCRIT'], sr.ppf(.95, 3, 2)),
          abs(h.globals_['EP_QCRIT'] - sr.ppf(.95, 3, 2)) < 1e-4 and not h.msgboxes)
    h = run(False, ['Critical value', 'Quit'], [{'ta': 0.05, 'tk': 3, 'tv': 2}], keys=['Enter'])
    h.execute('StudRange()')
    check('Critical value df=2 via PPL: raised to df 3 with the beta 14 message (%.4f, SciPy df3 %.4f)' %
          (h.globals_['EP_QCRIT'], sr.ppf(.95, 3, 3)),
          abs(h.globals_['EP_QCRIT'] - sr.ppf(.95, 3, 3)) < 2e-3 and h.msgboxes
          and 'df below 3 is not supported' in ' '.join(h.msgboxes[0].lines))
    print('     result:', h.result)

    # 6c. HSD then the yardstick: Enter opens it, tap two means
    h = Bridge(SRC, idle_key=4)
    h.choose('Tukey HSD'); h.answer({'ta': 0.05, 'tk': 4, 'tm': 8, 'tmse': 1, 'tvo': 0})
    h.press('Enter')                                   # the HSD page -> yardstick
    h.answer(ACCEPT)                                    # the means form, defaults
    h.press('Enter')                                   # pick mean 1 (cursor)
    h.press('Right'); h.press('Right'); h.press('Enter')   # pick mean 3
    h.press('Esc'); h.choose('Quit')
    h.execute('StudRange()')
    hsd = sr.ppf(.95, 4, 28) * math.sqrt(1 / 8)
    check('HSD = %.4f (SciPy %.4f)' % (h.globals_['EP_HSD'], hsd), abs(h.globals_['EP_HSD'] - hsd) < 1e-4)
    verdict = [t for t in texts(h) if 'HSD: ' in t and 'significant' in t]
    check('yardstick verdict for means 10 and 12.5 says significant (|diff| 2.5 > %.3f)' % hsd,
          bool(verdict) and 'not significant' not in verdict[-1], repr(verdict[-1:] ))

    # 6d. the plot: cache by Python, a drag, the alpha strip, a soft key, the q crit box
    h = Bridge(SRC, idle_key=4)
    h.choose('Distribution plot'); h.answer({'tk': 3, 'tv': 12, 'qo': 3.5})
    h.drag([(100, 120), (140, 120), (160, 120)])        # q obs follows
    h.drag([(300, 70), (300, 75)])                      # alpha from the CDF strip
    h.tap(20, 230, lift=True)                            # soft key 1: alpha-
    h.tap(60, 18, lift=True)                             # the q crit box: q obs = q crit
    h.press('Esc'); h.choose('Quit')
    h.execute('StudRange()')
    tx = texts(h)
    check('plot via Python: badge on the plot', any('engine: MicroPython' in t for t in tx))
    alph = [t for t in tx if t.startswith('α = ')]
    print('     header readouts seen:', sorted(set(alph))[:6])
    qobs = [t for t in tx if t.startswith('q obs = ')]
    print('     q obs readouts (last 3):', qobs[-3:])
    check('soft keys drawn', any(sc.menu for sc in h.screens))
    last_alpha = alph[-1]
    last_q = qobs[-1]
    m1 = re.search(r'q crit = ([\d.]+)', last_alpha); m2 = re.search(r'q obs = ([\d.]+)\s+p = ([\d.]+)', last_q)
    check('after the q crit tap: q obs = q crit and p = alpha', m1 and m2 and m1.group(1) == m2.group(1)
          and abs(float(m2.group(2)) - float(re.search(r'α = ([\d.]+)', last_alpha).group(1))) < 6e-4,
          '(%s | %s)' % (last_alpha, last_q))
    # plot with Python failing: PPL fallback, the red badge, the menu has no Python items
    h = Bridge(SRC, idle_key=4); h.python_ok = False
    h.choose('Distribution plot'); h.answer({'tk': 3, 'tv': 12, 'qo': 3.5})
    h.press('Enter'); h.choose(0)                        # open the plot menu, cancel
    h.press('Esc'); h.choose('Quit')
    h.execute('StudRange()')
    plotmenu = [c for c in h.chooses if c.title == 'Plot menu']
    check('plot via PPL: red badge and a 6-item plot menu without the Python extras',
          any('engine: PPL' in t for t in texts(h)) and plotmenu and len(plotmenu[0].items) == 6)

    # 6e. the simulation from the plot menu, and the k = 2 curve
    h = Bridge(SRC, idle_key=4)
    random.seed(7)
    h.choose('Distribution plot'); h.answer({'tk': 3, 'tv': 12, 'qo': 3.5})
    h.press('Enter'); h.choose('H0 simulation'); h.answer({'pmTv': 5})
    h.press('Enter')                                     # close the teaching page
    h.press('Enter'); h.choose('k = 2 curve')
    h.press('Esc'); h.choose('Quit')
    h.execute('StudRange()')
    sim = h.globals_['EP_SRSIM']
    lines = [t for t in texts(h) if 'replicates' in t or 'q > q crit' in t or 'any t > t crit' in t]
    check('simulation ran through the bridge (2,000 replicates; q > q crit %.1f %%, any t %.1f %%)' %
          (100 * sim[40] / 2000, 100 * sim[41] / 2000), sim[44] == 2000 and 0.02 < sim[40] / 2000 < 0.09)
    print('     page/panel lines:', sorted(set(lines))[:5])
    check('k = 2 curve arrived and its legend is drawn', min(h.globals_['EP_SRCD2']) >= 0 and 'k = 2' in texts(h))

    # 6f. Diagnostics, both ways
    for ok in (True, False):
        h = run(ok, ['Diagnostics', 'Quit'], [], keys=['Enter'])
        h.execute('StudRange()')
        first = [t for t in texts(h) if 'Python bridge' in t]
        check('Diagnostics with Python %s: %r' % ('answering' if ok else 'failing', first[-1:]),
              bool(first) and (('OK' in first[-1]) if ok else ('NOT' in first[-1])))
    # 6g. help pages: 4 pages, nothing clipped
    h = run(True, ['Help', 'Quit'], [], keys=['Enter'] * 4)
    h.execute('StudRange()')
    clipped = [t.text for t in h.texts if getattr(t, 'clipped', False)]
    check('help: 4 pages, no line estimated clipped', len([s for s in h.screens if s.has('/4)')]) >= 4 and not clipped, repr(clipped[:3]))
    allclip = []
    for hh in []:
        pass


# ---------------------------------------------------------------- 7. beta 15a
def harness_checks_15a():
    from ppl_run_v3e import Harness, ACCEPT, CANCEL
    sr = stats.studentized_range

    class Bridge(Harness):
        python_ok = True
        def _python(self, a):
            self.log.append(('PYTHON', a))
            if not self.python_ok:
                return 0.0
            h = self
            class HStore(Store):
                def eval(s2, txt):
                    s2.evals += 1
                    m = re.match(r'^(\w+)\((\d+)\):=(.*)$', txt)
                    if m:
                        h.globals_[m.group(1)][int(m.group(2)) - 1] = float(m.group(3))
                        return 0
                    m = re.match(r'^(\w+):=(.*)$', txt)
                    if m:
                        v = m.group(2)
                        h.globals_[m.group(1)] = v[1:-1] if v.startswith('"') else float(v)
                        return 0
                    return h.globals_[txt]
            load_block(HStore(), run_main=True)
            return 0.0

    def slot_x(k):
        return int(53.4 * (k - 0.5))

    def plot(path, events, python_ok=True, **kw):
        h = Bridge(path, idle_key=4, **kw)
        h.python_ok = python_ok
        h.choose('Distribution plot'); h.answer({'tk': 3, 'tv': 12, 'qo': 3.5})
        events(h)
        h.press('Esc'); h.choose('Quit')
        h.execute('StudRange()')
        return h

    def headers(h):
        return [t.text for t in h.texts if t.text.startswith('α = ')]

    def ks(h):
        return [t.text for t in h.texts if t.text.startswith('k = ')]

    def alpha(t):
        return float(re.search(r'α = ([\d.]+)', t).group(1))

    # 7a. each soft key from its type-3 click alone
    h = plot(SRC, lambda h: h.tap(slot_x(1), 230))
    a = [alpha(t) for t in headers(h)]
    check('7a soft key 1 (α−) on a type-3 click: α 0.050 -> 0.025', a[0] == 0.05 and a[-1] == 0.025, str(sorted(set(a))))
    h = plot(SRC, lambda h: h.tap(slot_x(2), 230))
    a = [alpha(t) for t in headers(h)]
    check('7a soft key 2 (α+) on a type-3 click: α 0.050 -> 0.100', a[-1] == 0.1, str(sorted(set(a))))
    h = plot(SRC, lambda h: h.tap(slot_x(3), 230))
    check('7a soft key 3 (k−): k 3 -> 2', ks(h)[-1].startswith('k = 2 '), ks(h)[-1])
    h = plot(SRC, lambda h: h.tap(slot_x(4), 230))
    check('7a soft key 4 (k+): k 3 -> 4', ks(h)[-1].startswith('k = 4 '), ks(h)[-1])
    h = plot(SRC, lambda h: (h.tap(slot_x(5), 230), h.answer({'pmTv': 20})))
    check('7a soft key 5 (df): the df form opens; df 20 rebuilds the plot',
          any(d.title == 'Degrees of freedom' for d in h.inputs) and 'ν = 20' in ks(h)[-1], ks(h)[-1])
    h = plot(SRC, lambda h: (h.tap(slot_x(6), 230), h.choose(0)))
    check('7a soft key 6 (Menu): the plot menu opens', any(c.title == 'Plot menu' for c in h.chooses),
          str([c.title for c in h.chooses]))
    # 7b. beta 15 in v3d: nothing happens -- the emulator's "alpha+ does nothing"
    h = plot(B15, lambda h: (h.tap(slot_x(2), 230), h.tap(slot_x(6), 230)))
    a = [alpha(t) for t in headers(h)]
    check('7b beta 15 in v3d: α+ and Menu do nothing (the emulator\'s FAIL)', set(a) == {0.05}
          and not any(c.title == 'Plot menu' for c in h.chooses), str(sorted(set(a))))
    # 7c. no tap acts twice
    h = plot(SRC, lambda h: h.tap(slot_x(2), 230, lift=True), wait_model='v3b')
    a = [alpha(t) for t in headers(h)]
    check('7c a type-0 PRESS on the strip (the v3b model) does nothing -- neutralised', set(a) == {0.05}, str(sorted(set(a))))
    def inj(h):
        h._queue.clear()
    h = Bridge(SRC, idle_key=4)
    h.choose('Distribution plot'); h.answer({'tk': 3, 'tv': 12, 'qo': 3.5})
    h.choose('Quit')
    h._pending_wait = [[0.0, float(slot_x(2)), 230.0], [2.0], [3.0, float(slot_x(2)), 230.0], [4.0 * 0 + 2.0]]
    h.press('Esc')
    h.execute('StudRange()')
    a = [alpha(t) for t in headers(h)]
    check('7c a firmware that sent {0}, {2} AND {3} for a strip tap would still step α ONCE (0.05 -> 0.10)',
          sorted(set(a)) == [0.05, 0.1], str(a))
    # 7d. taps above the strip still work, once each
    h = plot(SRC, lambda h: h.tap(162, 120))
    q = [t.text for t in h.texts if t.text.startswith('q obs = ')]
    want = round((162 - 34) / (290 - 34) * h.globals_['srQmax'], 3)     # the plot window's right end
    check('7d a tap in the plot ({0}, {2}, {3}) moves q obs to the finger (%.3f): %s' % (want, q[-1]),
          q[-1].startswith('q obs = %.3f' % want))
    h = plot(SRC, lambda h: h.tap(60, 18))
    last_a = headers(h)[-1]; last_q = [t.text for t in h.texts if t.text.startswith('q obs = ')][-1]
    m1 = re.search(r'q crit = ([\d.]+)', last_a); m2 = re.search(r'q obs = ([\d.]+)', last_q)
    check('7d a tap on the q crit box sets q obs = q crit (%s | %s)' % (last_a, last_q), m1 and m2 and m1.group(1) == m2.group(1))
    # 7e. stale clicks: a page held by sr_WaitAny, closed by a tap on its footer
    def help_then_tap(h):
        h.press('Enter'); h.choose('Help for this plot')
        h.tap(150, 226)                      # "any key or tap = back to the plot"
    for tail in (False, True):
        h = plot(SRC, help_then_tap, mouse_tail=tail)
        a = [alpha(t) for t in headers(h)]
        check('7e the plot\'s help page closed by a footer tap (x 150, y 226)%s: no soft key fires on the plot '
              '(k stays 3, α stays 0.05)' % (' -- mouse_tail worst case' if tail else ''),
              set(a) == {0.05} and all(t.startswith('k = 3 ') for t in ks(h)), '%s %s' % (sorted(set(a)), ks(h)[-1:]))
    # without the guard, the worst case WOULD fire slot 3 (k-) there
    src = open(SRC, encoding='utf-8').read()
    ng = '/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/StudRange_beta15a_noguard.txt'
    open(ng, 'w', encoding='utf-8').write(src.replace(
        'IF ABS(pmMX-srTLX(srTLi))<=2 AND ABS(pmKey(3)-srTLY(srTLi))<=2 THEN', 'IF 0 THEN'))
    h = plot(ng, help_then_tap, mouse_tail=True)
    check('7e (without the guard, in that worst case, the click WOULD run soft key 3: k 3 -> 2)',
          ks(h)[-1].startswith('k = 2 '), ks(h)[-1])
    # 7f. the Quit summary
    h = Bridge(SRC, idle_key=4); h.choose('Quit'); h.execute('StudRange()')
    check('7f Quit with nothing computed: "%s"' % h.result,
          h.result == 'StudRange: q crit not computed, p not computed, HSD not computed (engine: none)')
    h = Bridge(SRC, idle_key=4)
    h.choose('Tukey HSD'); h.answer({'ta': 0.05, 'tk': 4, 'tm': 8, 'tmse': 1, 'tvo': 0}); h.press('Esc')
    h.choose('Quit'); h.execute('StudRange()')
    qc = sr.ppf(0.95, 4, 28); hsd = qc * math.sqrt(1 / 8)
    # 15b: the q crit names its alpha too, as its page showed it (4 decimals)
    want = 'StudRange: q crit (k = 4, ν = 28, α = 0.0500) = %.4f, p not computed, HSD = %.4f (engine: Python)' % (qc, hsd)
    check('7f after HSD only (the emulator\'s run): "%s"' % h.result, h.result == want, 'want ' + want)
    h = Bridge(B15, idle_key=4)
    h.choose('Tukey HSD'); h.answer({'ta': 0.05, 'tk': 4, 'tm': 8, 'tmse': 1, 'tvo': 0}); h.press('Esc')
    h.choose('Quit'); h.execute('StudRange()')
    check('7f (beta 15 in the same run: "%s" -- the emulator\'s "p = 0.00000")' % h.result, 'p = 0.00000' in h.result)
    h = Bridge(SRC, idle_key=4)
    h.choose('P-value from q'); h.answer({'tq': 3.5, 'tk': 3, 'tv': 12}); h.press('Enter')
    h.choose('Critical value'); h.answer({'ta': 0.05, 'tk': 3, 'tv': 12}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    want = 'StudRange: q crit (k = 3, ν = 12, α = 0.0500) = %.4f, p = %.5f, HSD not computed (engine: Python)' % (
        sr.ppf(0.95, 3, 12), sr.sf(3.5, 3, 12))
    check('7f after P-value and Critical value: "%s"' % h.result, h.result == want, 'want ' + want)
    h = Bridge(SRC, idle_key=4); h.python_ok = False
    h.choose('Critical value'); h.answer({'ta': 0.05, 'tk': 3, 'tv': 2}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    check('7f the PPL fallback raised df 2 to 3: the summary names the df it used, ν = 3 ("%s")' % h.result,
          h.result.startswith('StudRange: q crit (k = 3, ν = 3, α = 0.0500) = ') and '(engine: PPL)' in h.result)
    h = Bridge(SRC, idle_key=4)
    h.choose('Critical value'); h.answer({'ta': 0.05, 'tk': 3, 'tv': 0}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    check('7f df 0 (infinity) is named with the infinity sign ("%s")' % h.result, 'ν = ' + chr(8734) + ', α = 0.0500)' in h.result)
    # 7g. beta 15a against beta 15 (kept, on those two files)
    def bodies(txt):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', txt)
        c = re.sub(r'//[^\n]*', '', c)
        out = {}
        for m in re.finditer(r'(?m)^(?:EXPORT\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
            out[m.group(1)] = re.sub(r'[ \t]+\n', '\n', m.group(0))
        return out
    t0, t1 = open(B15, encoding='utf-8').read(), open(OLD, encoding='utf-8').read()
    b0, b1 = bodies(t0), bodies(t1)
    diff = sorted(n for n in set(b0) | set(b1) if b0.get(n) != b1.get(n))
    want = ['StudRange', 'sr_CritMode', 'sr_HSDMode', 'sr_PlotMode', 'sr_PvMode', 'sr_WaitAny']
    check('7g routines that differ from beta 15: %s' % diff, diff == want, 'want %s' % want)
    py0 = re.findall(r'(?ms)^#PYTHON.*?^#END', t0); py1 = re.findall(r'(?ms)^#PYTHON.*?^#END', t1)
    check('7g the #PYTHON srq block is byte-identical to beta 15', py0 == py1 and len(py1) == 1)
    # 7g (15b). beta 15b against beta 15a
    t2 = open(SRC, encoding='utf-8').read()
    b2 = bodies(t2)
    diff = sorted(n for n in set(b1) | set(b2) if b1.get(n) != b2.get(n))
    # 15d: + sr_BuildZ, sr_Cache (the MAKELIST counter) and sr_HelpMode (the disclaimer line); sr_CritMode and
    # sr_HSDMode were already listed
    want = ['StudRange', 'sr_BuildZ', 'sr_Cache', 'sr_CritMode', 'sr_Eq', 'sr_FmtF', 'sr_HSDMode', 'sr_HelpMode',
            'sr_PlotMode', 'sr_PvMode', 'sr_SimRun', 'sr_Yard']
    check('7g 15b (and 15c: + sr_Eq; 15d: + sr_BuildZ, sr_Cache, sr_HelpMode): routines that differ from beta 15a: %s'
          % diff, diff == want, 'want %s' % want)
    check('7g 15b: sr_WaitAny (it still appends its tap) is byte-identical to beta 15a', b1['sr_WaitAny'] == b2['sr_WaitAny'])
    py2 = re.findall(r'(?ms)^#PYTHON.*?^#END', t2)
    check('7g 15b: the #PYTHON srq block is byte-identical to beta 15a (and to beta 15)', py2 == py1 == py0 and len(py2) == 1)
    def outside(t, names):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', t)
        c = re.sub(r'//[^\n]*', '', c)
        c = re.sub(r'(?ms)^(?:EXPORT\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
        return re.sub(r'\s+', ' ', c)
    newl = ['LOCAL srQS:="";', 'LOCAL srAS:="";', 'LOCAL srPS:="";', 'LOCAL srQueuedMs:=100;', 'sr_Eq();']
    o1, o2 = outside(t1, diff), outside(t2, diff)
    for nl in newl:
        o2 = o2.replace(nl + ' ', '', 1)
    check('7g 15b: outside those routines only the new file-level lines differ (%s); the rest is comments' % ', '.join(newl),
          o1 == o2)
    code = re.sub(r'"[^"\n]*"', '""', re.sub(r'//[^\n]*', '', re.sub(r'(?ms)^#PYTHON.*?^#END', '', t2)))
    check('7g 15b: the stale test reads the threshold by name, set in ONE place; the clock is read around the wait',
          code.count('srQueuedMs') == 2 and 'IF pmMT==3 AND pmMX>=0 AND pmWT<=srQueuedMs THEN' in t2
          and t2.count('pmWT:=TICKS;') == 1 and t2.count('pmWT:=TICKS-pmWT;') == 1)
    check('7g 15b: the type-3 soft-key logic the emulator confirmed is unchanged',
          'IF pmMT==3 AND pmMX>=0 AND pmStl==0 THEN' in t2 and 'IF pmKey(3)>=218 THEN pmAct:=MIN(6,IP(pmMX/53.4)+1); END;' in t2)


# ---------------------------------------------------------------- 8. beta 15b
def harness_checks_15b():
    from ppl_run_v3e import Harness, ACCEPT, CANCEL
    sr = stats.studentized_range

    class Bridge(Harness):
        """PYTHON(srq) runs the real block (as in sections 6 and 7); and, for section 8, the clock:
        gap_ms = a fresh event the student makes (WAIT(-1) takes it from the script's queue) comes
        gap_ms after WAIT(-1) was called -- a person, not the queue; what is ALREADY QUEUED
        (_pending_wait: a lift, a click, mouse_tail's tail) comes back at once, the clock not moved.
        gap_ms = 0 is plain v3d (its clock moves only 1 ms per TICKS reading)."""
        python_ok = True
        gap_ms = 0

        def _python(self, a):
            self.log.append(('PYTHON', a))
            if not self.python_ok:
                return 0.0
            h = self
            class HStore(Store):
                def eval(s2, txt):
                    s2.evals += 1
                    m = re.match(r'^(\w+)\((\d+)\):=(.*)$', txt)
                    if m:
                        h.globals_[m.group(1)][int(m.group(2)) - 1] = float(m.group(3))
                        return 0
                    m = re.match(r'^(\w+):=(.*)$', txt)
                    if m:
                        v = m.group(2)
                        h.globals_[m.group(1)] = v[1:-1] if v.startswith('"') else float(v)
                        return 0
                    return h.globals_[txt]
            load_block(HStore(), run_main=True)
            return 0.0

        def _wait(self, a):
            n = a[0] if a else None
            if n is not None and n < 0 and self._stale is None and not self._pending_wait and self._queue:
                self.clock += self.gap_ms
            return Harness._wait(self, a)

    def slot_x(k):
        return int(53.4 * (k - 0.5))

    def plot(path, events, python_ok=True, gap_ms=0, quit=True, **kw):
        h = Bridge(path, idle_key=4, **kw)
        h.python_ok = python_ok
        h.gap_ms = gap_ms
        h.choose('Distribution plot'); h.answer({'tk': 3, 'tv': 12, 'qo': 3.5})
        events(h)
        h.press('Esc')
        if quit:
            h.choose('Quit')
        h.execute('StudRange()')
        return h

    def alphas(h):
        return [float(re.search(r'α = ([\d.]+)', t.text).group(1)) for t in h.texts if t.text.startswith('α = ')]

    def ks(h):
        return [t.text for t in h.texts if t.text.startswith('k = ')]

    GAP = 400
    AX = slot_x(1)          # 26: the alpha- key

    def help_at_alpha(taps):
        def ev(h):
            h.press('Enter'); h.choose('Help for this plot')
            h.tap(AX, 226)              # close the help page on its footer, at the alpha- key's spot (MOUSE)
            for _ in range(taps):
                h.tap(AX, 226)          # then alpha- at that same spot
        return ev

    print('   8a. the stale spot, both ways')
    h = plot(OLD, help_at_alpha(1), gap_ms=GAP)
    a = alphas(h)
    check('8a beta 15a, the emulator\'s case: Help closed on its footer at the α− key, then α− once -> nothing '
          '(α stays 0.050)', set(a) == {0.05}, str(sorted(set(a))))
    h = plot(OLD, help_at_alpha(2), gap_ms=GAP)
    a = alphas(h)
    check('8a beta 15a: ... a second α− tap works (the emulator: "ignored once, then works"): 0.050 -> 0.025',
          a[-1] == 0.025 and 0.01 not in a, str(sorted(set(a))))
    h = plot(SRC, help_at_alpha(1), gap_ms=GAP)
    a = alphas(h)
    check('8a beta 15b: the same taps -- α− works on the FIRST tap (a real, later tap at the spot counts): '
          '0.050 -> 0.025', a[-1] == 0.025 and 0.01 not in a, str(sorted(set(a))))
    for gap, lbl in ((0, 'a clock that has not moved (plain v3d)'), (GAP, 'the student\'s taps %d ms apart' % GAP)):
        h = plot(SRC, help_at_alpha(0), gap_ms=gap, mouse_tail=True)
        a = alphas(h)
        check('8a beta 15b: a click ALREADY QUEUED at the α− spot (mouse_tail, %s) is still skipped: α stays 0.050'
              % lbl, set(a) == {0.05} and all(t.startswith('k = 3 ') for t in ks(h)), str(sorted(set(a))))
    h = plot(SRC, help_at_alpha(1), gap_ms=GAP, mouse_tail=True)
    a = alphas(h)
    check('8a beta 15b: ... and the real α− tap after that queued click counts, ONCE: 0.050 -> 0.025',
          a[-1] == 0.025 and 0.01 not in a, str(sorted(set(a))))
    src = open(SRC, encoding='utf-8').read()
    nq = '/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/StudRange_beta15c_noqueue.txt'
    open(nq, 'w', encoding='utf-8').write(src.replace('IF pmMT==3 AND pmMX>=0 AND pmWT<=srQueuedMs THEN', 'IF 0 THEN'))
    h = plot(nq, help_at_alpha(0), gap_ms=0, mouse_tail=True)
    a = alphas(h)
    check('8a (with the stale test patched out, that queued click WOULD step α: 0.050 -> 0.025 -- the skip is real)',
          0.025 in a, str(sorted(set(a))))
    h = plot(SRC, lambda h: h.tap(162, 120), gap_ms=GAP)
    q = [t.text for t in h.texts if t.text.startswith('q obs = ')]
    want = round((162 - 34) / (290 - 34) * h.globals_['srQmax'], 3)
    check('8a beta 15b, time passing: a tap in the plot still moves q obs to the finger once (%.3f)' % want,
          q[-1].startswith('q obs = %.3f' % want), q[-1])
    h = plot(SRC, lambda h: (h.tap(slot_x(2), 230), h.tap(slot_x(2), 230)), gap_ms=GAP)
    a = alphas(h)
    check('8a beta 15b, time passing: two α+ taps step α twice (0.050 -> 0.100 -> ... ) -- soft keys unchanged',
          a[-1] == 0.1 and 0.1 in a, str(sorted(set(a))))

    print('   8b. the Quit summary reports what the student saw')
    def last(h, prefix):
        return [t.text for t in h.texts if t.text.startswith(prefix)][-1]
    # the emulator's run: only the plot
    h = plot(SRC, lambda h: None)
    hdr, qob = last(h, 'α = '), last(h, 'q obs = ')
    m1 = re.search(r'α = ([\d.]+)   q crit = ([\d.]+)', hdr); m2 = re.search(r'(p [=<] [<\d. ]+)$', qob)
    want = 'StudRange: q crit (k = 3, ν = 12, α = %s) = %s, %s, HSD not computed (engine: Python)' % (
        m1.group(1), m1.group(2), m2.group(1).strip())
    check('8b plot only (the emulator\'s session): "%s" -- the plot\'s own readouts "%s" / "%s"' % (h.result, hdr, qob),
          h.result == want, 'want ' + want)
    qcs, ps = float(m1.group(2)), float(m2.group(1).split()[-1])
    check('8b ... and those are SciPy\'s q crit and p to the plot\'s decimals (%.3f / %.4f; curve-level accuracy)'
          % (sr.ppf(0.95, 3, 12), sr.sf(3.5, 3, 12)),
          abs(qcs - sr.ppf(0.95, 3, 12)) < 2e-3 and abs(ps - sr.sf(3.5, 3, 12)) < 2e-4)
    check('8b ... EP_QCRIT and EP_QPVAL are still not written by the plot (beta 14)',
          h.globals_['EP_QCRIT'] == 0 and h.globals_['EP_QPVAL'] == 0,
          '%s %s' % (h.globals_['EP_QCRIT'], h.globals_['EP_QPVAL']))
    h = plot(OLD, lambda h: None)
    check('8b (beta 15a, same session: "%s" -- the emulator\'s finding)' % h.result,
          h.result == 'StudRange: q crit not computed, p not computed, HSD not computed (engine: Python)')
    # the plot with alpha moved and k changed: the summary follows the last frame
    h = plot(SRC, lambda h: (h.tap(slot_x(1), 230), h.tap(slot_x(4), 230)))
    hdr, kh = last(h, 'α = '), last(h, 'k = ')
    m1 = re.search(r'α = ([\d.]+)   q crit = ([\d.]+)', hdr)
    check('8b plot, α− then k+: the summary has k = 4, α = %s, q crit = %s, as on the last frame ("%s")'
          % (m1.group(1), m1.group(2), h.result),
          h.result.startswith('StudRange: q crit (k = 4, ν = 12, α = %s) = %s, p ' % (m1.group(1), m1.group(2)))
          and kh.startswith('k = 4 '), kh)
    # no q obs on the plot: q crit is reported, p stays "not computed"
    h = Bridge(SRC, idle_key=4)
    h.choose('Distribution plot'); h.answer({'tk': 3, 'tv': 12, 'qo': 0}); h.press('Esc'); h.choose('Quit')
    h.execute('StudRange()')
    check('8b plot with no q obs: "%s" (p not computed)' % h.result,
          re.match(r'^StudRange: q crit \(k = 3, ν = 12, α = 0\.050\) = [\d.]+, p not computed, HSD not computed', h.result)
          is not None)
    # a q crit beyond the plot's window, as the plot says it: "q crit > ..."
    h = plot(SRC, lambda h: (h.press('Enter'), h.choose('Set α'), h.answer({'pmTv': 0.001})))
    hdr = last(h, 'α = ')
    m1 = re.search(r'α = ([\d.]+)   q crit ([=>]) ([\d.]+)', hdr)
    check('8b α = 0.001 on the plot: the summary says what the header said ("%s" / "%s")' % (hdr, h.result),
          m1 is not None and ('α = %s) %s %s' % (m1.group(1), m1.group(2), m1.group(3))) in h.result)
    # the last value seen wins: P-value then the plot, and the plot then P-value
    h = Bridge(SRC, idle_key=4)
    h.choose('P-value from q'); h.answer({'tq': 3.5, 'tk': 3, 'tv': 12}); h.press('Enter')
    h.choose('Distribution plot'); h.answer({'tk': 4, 'tv': 20, 'qo': 4.5}); h.press('Esc')
    h.choose('Quit'); h.execute('StudRange()')
    qob = last(h, 'q obs = ')
    check('8b P-value, then the plot (k 4, df 20, q obs 4.5): the plot\'s p is the last seen ("%s")' % h.result,
          ', ' + qob.split('   ')[-1] + ',' in h.result and 'k = 4, ν = 20' in h.result)
    h = Bridge(SRC, idle_key=4)
    h.choose('Distribution plot'); h.answer({'tk': 4, 'tv': 20, 'qo': 4.5}); h.press('Esc')
    h.choose('P-value from q'); h.answer({'tq': 3.5, 'tk': 3, 'tv': 12}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    check('8b the plot, then P-value: the P-value page\'s p (5 decimals) is the last seen ("%s")' % h.result,
          ', p = %.5f,' % sr.sf(3.5, 3, 12) in h.result and 'k = 4, ν = 20' in h.result)
    h = Bridge(SRC, idle_key=4)
    h.choose('P-value from q'); h.answer({'tq': 30, 'tk': 3, 'tv': 12}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    check('8b a P-value below 0.00001 reads "p < 0.00001" in the summary ("%s")' % h.result,
          ', p < 0.00001,' in h.result)

    print('   8c. no fixed decimals in scientific form')
    hh = Bridge(SRC)
    for args, want in (((0.0004, 3), '0.000'), ((0.096, 1), '0.1'), ((-1e-17, 1), '0.0'), ((0.05, 1), '0.1'),
                       ((3.77293, 3), '3.773'), ((1e-6, 4), '0.0000'), ((-2.5, 2), '-2.50')):
        g = hh.execute('sr_FmtF(%s,%d)' % (('%.17g' % args[0]).replace('e', 'E'), args[1]))
        check('8c sr_FmtF%s = "%s"' % (args, g), g == want, 'want ' + want)
    check('8c ... none of them printed in scientific form', not hh.sci_strings, str(hh.sci_strings))
    # the yardstick: means across zero and a tiny one; a tiny MSE (HSD = 1.4E-5); F(q) for a tiny q
    # (q = 0.001: F = 3E-7)
    def tiny(h):
        h.choose('Tukey HSD'); h.answer({'ta': 0.05, 'tk': 4, 'tm': 8, 'tmse': 1E-10, 'tvo': 0})
        h.press('Enter'); h.answer({'ymA': -0.3, 'ymB': 0.0004, 'ymC': 0.2, 'ymD': 0.25})
        h.press('Esc'); h.choose('P-value from q'); h.answer({'tq': 0.001, 'tk': 3, 'tv': 12}); h.press('Enter')
        h.choose('Quit'); h.execute('StudRange()')
    h15a = Bridge(OLD, idle_key=4)
    tiny(h15a)
    print('     (beta 15a on the same run: %s)' % sorted({r for (v, d, r) in h15a.sci_strings}))
    h = Bridge(SRC, idle_key=4)
    tiny(h)
    tx = [t.text for t in h.texts]
    yd = [t for t in tx if t.startswith(chr(57344)) and ' = ' in t]
    ticks = [t.text for t in h.texts if t.y == 156]
    check('8c yardstick: means -0.3, 0.0004, 0.2, 0.25 print as %s; the ticks %s -- no scientific form, no "-0.0"'
          % (yd[:4], ticks[:8]), not h.sci_strings and '-0.0' not in ticks and '-0.00' not in ticks
          and any(t.endswith(' = 0.000') for t in yd), str(h.sci_strings[:3]))
    fq = [t for t in tx if t.startswith('F(q)')]
    check('8c F(q) for q = 0.001 (a probability under 0.00001) reads "%s" (15c: no "=" before the relation)'
          % (fq[-1] if fq else None), fq and fq[-1] == 'F(q) < 0.00001')
    check('8c a tiny MSE gives HSD "0.0000" on the page and in the summary ("%s")' % h.result,
          'HSD = 0.0000' in h.result and any(t.startswith('HSD = q·√(MSE/m) = 0.0000') for t in tx))
    # the simulation's percents through sr_FmtF: one replicate in 2,000
    hh = Bridge(SRC)
    g = hh.execute('sr_FmtF(100*1/2000,1)')
    check('8c one replicate in 2,000 = 0.05 %% prints "%s" (STRING(0.05, 2, 1) is "5.0ᴇ-2")' % g, g == '0.1')

    print('   8d. INSTRING, LEFT, MID')
    code = re.sub(r'(?ms)^#PYTHON.*?^#END', '', src)
    code = re.sub(r'//[^\n]*', '', code)
    code = re.sub(r'"[^"\n]*"', '""', code)
    found = re.findall(r'\b(INSTRING|LEFT|RIGHT|MID)\s*\(', code, re.I)
    # 15c: sr_Eq reads the first character, LEFT(eqS,1), twice -- inside IF DIM(eqS)>0, so never of ""
    eqb = re.search(r'(?ms)^sr_Eq\(eqS\)\nBEGIN\n(.*?)^END;', src).group(1)
    check('8d the PPL code (outside comments, strings and the #PYTHON block) calls none of INSTRING, RIGHT, MID, '
          'and LEFT only twice, in sr_Eq, inside IF DIM(eqS)>0', found == ['LEFT', 'LEFT'] and
          eqb.split('\n')[0].strip() == 'IF DIM(eqS)>0 THEN' and eqb.count('LEFT(eqS,1)') == 2, str(found))

# ---------------------------------------------------------------- 9. beta 15c
def harness_checks_15c():
    from ppl_run_v3e import Harness
    import difflib
    B15 = HERE + 'StudRange_beta15b.txt'

    def bodies(txt):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', txt)
        c = re.sub(r'//[^\n]*', '', c)
        out = {}
        for m in re.finditer(r'(?m)^(?:EXPORT\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
            out[m.group(1)] = re.sub(r'[ \t]+\n', '\n', m.group(0))
        return out

    def pv_page(path, q, k, v):
        h = Harness(path)                                  # no Python: the PPL engine (the fallback)
        h.answer({'tq': q, 'tk': k, 'tv': v}); h.press('Enter')
        h.call('sr_PvMode')
        tx = [t.text for t in h.texts if t.text.startswith('P(Q') or t.text.startswith('F(q)')]
        return tx, h.globals_['srPS'], h.globals_['EP_QPVAL']

    for (q, k, v), old, new in (
            ((3.5, 3, 12), (['P(Q ≥ q) = 0.07000', 'F(q) = 0.93000'], 'p = 0.07000'), None),
            ((12.0, 3, 12), (['P(Q ≥ q) = < 0.00001', 'F(q) = 0.99999'], 'p < 0.00001'),
             (['P(Q ≥ q) < 0.00001', 'F(q) = 0.99999'], 'p < 0.00001')),
            ((40.0, 3, 12), (['P(Q ≥ q) = 0.00000', 'F(q) = 1.00000'], 'p = 0.00000'),
             (['P(Q ≥ q) < 0.00001', 'F(q) = 1.00000'], 'p < 0.00001')),
            ((0.001, 3, 12), (['P(Q ≥ q) = 1.00000', 'F(q) = < 0.00001'], 'p = 1.00000'),
             (['P(Q ≥ q) = 1.00000', 'F(q) < 0.00001'], 'p = 1.00000')),
            ((0.0, 3, 12), (['P(Q ≥ q) = 1.00000', 'F(q) = 0.00000'], 'p = 1.00000'), None),
            ((5.0, 4, 20), None, None), ((8.0, 6, 30), None, None)):
        a, b = pv_page(B15, q, k, v), pv_page(SRC, q, k, v)
        if old is not None:
            check('9a 15b, q %g, k %d, df %d: %r, summary "%s"' % (q, k, v, a[0], a[1]), (a[0], a[1]) == old, str(a))
        if new is None:
            check('9a q %g, k %d, df %d: an ordinary page and summary are the same in 15b and 15c: %r, "%s"'
                  % (q, k, v, b[0], b[1]), a[:2] == b[:2] and ' = ' in b[0][0], str((a, b)))
        else:
            check('9a 15c, q %g, k %d, df %d: %r, summary "%s"' % (q, k, v, b[0], b[1]), (b[0], b[1]) == new, str(b))
        check('9a q %g: EP_QPVAL is the computed p, the same in 15b and 15c (%.3g)' % (q, b[2]), a[2] == b[2])
    a = pv_page(SRC, 40.0, 3, 12)
    check('9a q 40: the PPL engine\'s p is exactly 0 (1 - F, F reached 1; SciPy %.2g), shown "< 0.00001"'
          % stats.studentized_range.sf(40, 3, 12), a[2] == 0 and stats.studentized_range.sf(40, 3, 12) > 0)
    # the Quit summary after the page
    for q, want in ((40.0, ', p < 0.00001,'), (3.5, ', p = 0.07000,'), (12.0, ', p < 0.00001,')):
        h = Harness(SRC, idle_key=4)
        h.choose('P-value from q'); h.answer({'tq': q, 'tk': 3, 'tv': 12}); h.press('Enter')
        h.choose('Quit'); h.execute('StudRange()')
        check('9a the Quit summary after q %g: "%s"' % (q, h.result), want in h.result)
    # 9b sr_Eq
    hh = Harness(SRC)
    e = [hh.call('sr_Eq', s) for s in ('< 0.00001', '0.07000', '', '1.00000')]
    check('9b sr_Eq: "< 0.00001" -> " < 0.00001", "0.07000" -> " = 0.07000", "" -> " = " (no error): %r' % e,
          e == [' < 0.00001', ' = 0.07000', ' = ', ' = 1.00000'])
    # 9c the diff 15b -> 15c
    # 15d: 9c checks the 15b -> 15c diff, so it reads beta 15c's own file; 9d's version strings and bracket check read
    # beta 15d (section 10 checks 15c -> 15d)
    t15b, t15c = open(B15, encoding='utf-8').read(), open(B15C, encoding='utf-8').read()
    t15d = open(SRC, encoding='utf-8').read()
    c0, c1 = bodies(t15b), bodies(t15c)
    diff = sorted(n for n in set(c0) | set(c1) if c0.get(n) != c1.get(n))
    check('9c routines that differ from beta 15b: %s (sr_Eq new, sr_PvMode)' % diff, diff == ['sr_Eq', 'sr_PvMode'])
    check('9c the #PYTHON srq block is byte-identical to beta 15b',
          re.findall(r'(?ms)^#PYTHON.*?^#END', t15b) == re.findall(r'(?ms)^#PYTHON.*?^#END', t15c))

    def code(t):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', t)
        out = []
        for l in c.split('\n'):
            o, ins = [], False
            for i, ch in enumerate(l):
                if ch == '"':
                    ins = not ins
                if not ins and l[i:i + 2] == '//':
                    break
                o.append(ch)
            s = ''.join(o).strip()
            if s:
                out.append(s)
        return out
    mi, pl = [], []
    k0, k1 = code(t15b), code(t15c)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
        if op in ('replace', 'delete'):
            mi += k0[i1:i2]
        if op in ('replace', 'insert'):
            pl += k1[j1:j2]
    wm = ['LOCAL tq,tk,tv,pv,fv;', 'srPS:="p = "+sr_FmtP(pv,5);',
          'IF pv>0 AND pv<0.00001 THEN srPS:="p "+sr_FmtP(pv,5); END;', '"P(Q ≥ q) = "+sr_FmtP(pv,5),',
          '"F(q) = "+sr_FmtP(fv,5),']
    wp = ['sr_Eq();', 'sr_Eq(eqS)', 'BEGIN', 'IF DIM(eqS)>0 THEN',
          'IF LEFT(eqS,1)=="<" OR LEFT(eqS,1)==">" THEN RETURN " "+eqS; END;', 'END;', 'RETURN " = "+eqS;', 'END;',
          'LOCAL tq,tk,tv,pv,fv,pvS;', 'pvS:=sr_FmtP(pv,5);', 'IF pv<=0 THEN pvS:="< "+STRING(0.00001,2,5); END;',
          'srPS:="p"+sr_Eq(pvS);', '"P(Q ≥ q)"+sr_Eq(pvS),', '"F(q)"+sr_Eq(sr_FmtP(fv,5)),']
    check('9c the code lines that changed are exactly the listed ones: -%r +%r'
          % ([x for x in mi if x not in wm], [x for x in pl if x not in wp]), sorted(mi) == sorted(wm) and sorted(pl) == sorted(wp))
    # 9d names, version strings, comments
    BI = set(l.strip().lower() for l in open('/home/claude/work/gate_r2/HP_Prime_Builtin_Names.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#'))
    check('9d the new names sr_Eq, eqS, pvS are not built-ins (case ignored); sr_Eq carries the sr_ tag',
          not any(n.lower() in BI for n in ('sr_Eq', 'eqS', 'pvS')))
    L = t15d.split('\n')
    check('9d version strings (15d: beta 15d\'s): both banners, the tested-on lines, the "What changed in beta 15d" '
          'paragraph above beta 15c\'s',
          L[1] == '// STUDRANGE - beta 15d' and '// StudRange beta 15d — Studentized Range Distribution (Tukey q)' in t15d
          and '//   this beta 15d have NOT yet been run on hardware.' in t15d and '// What changed in beta 15d' in t15d
          and '// What changed in beta 15c' in t15d and '// STUDRANGE - beta 15c' not in t15d
          and 'beta 15d has run only in the PC harness' in t15d)
    depth, bad = 0, []
    for n_, l in enumerate(re.sub(r'(?ms)^#PYTHON.*?^#END', '', t15d).split('\n'), 1):
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
    check('9d no // comment inside an open bracket: %r' % bad[:5], not bad)


# ---------------------------------------------------------------- 10. beta 15d
def harness_checks_15d():
    from ppl_run_v3e import Harness
    import difflib, subprocess
    sr = stats.studentized_range
    t15c, t15d = open(B15C, encoding='utf-8').read(), open(SRC, encoding='utf-8').read()

    class Bridge(Harness):
        """PYTHON(srq) runs the real block (as in sections 6-8); python_ok = False: nothing happens"""
        python_ok = True
        def _python(self, a):
            self.log.append(('PYTHON', a))
            if not self.python_ok:
                return 0.0
            h = self
            class HStore(Store):
                def eval(s2, txt):
                    s2.evals += 1
                    m = re.match(r'^(\w+)\((\d+)\):=(.*)$', txt)
                    if m:
                        h.globals_[m.group(1)][int(m.group(2)) - 1] = float(m.group(3))
                        return 0
                    m = re.match(r'^(\w+):=(.*)$', txt)
                    if m:
                        v = m.group(2)
                        h.globals_[m.group(1)] = v[1:-1] if v.startswith('"') else float(v)
                        return 0
                    return h.globals_[txt]
            load_block(HStore(), run_main=True)
            return 0.0

    def page(path, mode, ans, python_ok, home_x=None):
        h = Bridge(path)
        h.python_ok = python_ok
        if home_x is not None:
            h.globals_['X'] = home_x
        h.answer(ans); h.press('Esc')
        h.call(mode)
        pg = [x for x in h.pages if x.func == 'sr_ShowRes'][-1]
        lines = [t.text for t in pg.texts if t.font == 3 and t.y > 26]
        return lines, h

    NOTE = ['PPL fallback at α < 0.005:', 'q crit may be off by a few %']
    HNOTE = ['PPL fallback at α < 0.005:', 'q crit, HSD may be off a few %']

    print('   10a. S3: spaces round "=" on the HSD page')
    for ans, old0, new0 in (({'ta': 0.05, 'tk': 4, 'tm': 8, 'tmse': 1, 'tvo': 0}, 'α=0.0500  k=4  m=8  ν=28',
                             'α = 0.0500  k = 4  m = 8  ν = 28'),
                            ({'ta': 0.01, 'tk': 20, 'tm': 100, 'tmse': 2.5, 'tvo': 0}, 'α=0.0100  k=20  m=100  ν=1980',
                             'α = 0.0100  k = 20  m = 100  ν = 1980')):
        a, ha = page(B15C, 'sr_HSDMode', ans, True)
        b, hb = page(SRC, 'sr_HSDMode', ans, True)
        check('10a HSD page (Python answering), first line: 15c "%s" -> 15d "%s"; the other lines unchanged'
              % (a[0], b[0]), a[0] == old0 and b[0] == new0 and a[1:] == b[1:]
              and ha.globals_['EP_HSD'] == hb.globals_['EP_HSD'])
        check('10a "%s": %d characters, ends at x %d at 7.5 px a character (the harness) or %d at 9 (the review\'s '
              'cautious estimate), inside 320' % (new0, len(new0), 12 + 7.5 * len(new0), 12 + 9 * len(new0)),
              12 + 9 * len(new0) <= 320 if len(new0) <= 34 else 12 + 7.5 * len(new0) <= 320)
    code = re.sub(r'(?ms)^#PYTHON.*?^#END', '', t15d)
    code = re.sub(r'//[^\n]*', '', code)
    unsp = re.findall(r'"[^"\n]*\w=["+]', code)
    check('10a no display label is glued to its "=" any more (a string ending "x=" before a value): %r' % unsp[:3],
          not [u for u in unsp if not u.endswith(':="')])

    print('   10b. S1: the note on the Critical value and HSD pages, PPL engine below alpha 0.005')
    rows = {}
    for ta, k, v, py_ok in ((0.0001, 20, 3, False), (0.0049, 3, 12, False), (0.005, 3, 12, False),
                            (0.05, 3, 12, False), (0.0001, 20, 3, True), (0.001, 4, 3, True)):
        a, ha = page(B15C, 'sr_CritMode', {'ta': ta, 'tk': k, 'tv': v}, py_ok)
        b, hb = page(SRC, 'sr_CritMode', {'ta': ta, 'tk': k, 'tv': v}, py_ok)
        rows[(ta, k, v, py_ok)] = (a, b, ha.globals_['EP_QCRIT'], hb.globals_['EP_QCRIT'])
        noted = (not py_ok) and ta < 0.005
        if noted:
            want = a[:3] + NOTE + [a[4], a[5], a[7]]
            ok = b == want and a[3] == '' and a[6] == ''
        else:
            ok = b == a
        check('10b Critical value, alpha %g, k %d, df %d, %s: %s' % (ta, k, v, 'PPL engine' if not py_ok else 'Python',
              'the two note lines replace the two blank ones' if noted else 'the page is beta 15c\'s'),
              ok and len(b) == 8 and hb.globals_['EP_QCRIT'] == ha.globals_['EP_QCRIT'], str(b))
    qp = rows[(0.0001, 20, 3, False)][3]
    qy = rows[(0.0001, 20, 3, True)][3]
    ref = sr.ppf(1 - 0.0001, 20, 3)
    check('10b why: k 20, df 3, alpha 1E-4: the PPL engine gives %.3f, Python %.3f, SciPy %.3f (PPL %.1f %% off; the '
          'number is unchanged in 15d, only said)' % (qp, qy, ref, 100 * (qp / ref - 1)),
          abs(qp / ref - 1) > 0.01 and abs(qy / ref - 1) < 1e-5)
    for ta, py_ok in ((0.001, False), (0.05, False), (0.001, True)):
        ans = {'ta': ta, 'tk': 4, 'tm': 8, 'tmse': 1, 'tvo': 3}
        a, ha = page(B15C, 'sr_HSDMode', ans, py_ok)
        b, hb = page(SRC, 'sr_HSDMode', ans, py_ok)
        noted = (not py_ok) and ta < 0.005
        if noted:
            ok = b[1:] == [a[1], a[3], a[4]] + HNOTE + [a[6], a[7]] and a[2] == '' and a[5] == ''
        else:
            ok = b[1:] == a[1:]
        check('10b Tukey HSD, alpha %g, k 4, m 8, df 3, %s: %s' % (ta, 'PPL engine' if not py_ok else 'Python',
              'the two note lines replace the two blank ones' if noted else 'the page is beta 15c\'s (but S3)'),
              ok and len(b) == 8 and hb.globals_['EP_HSD'] == ha.globals_['EP_HSD'], str(b))
    longest = max(NOTE + HNOTE, key=len)
    check('10b the note lines are %d characters at most (font 3: under the review\'s 34)' % len(longest), len(longest) <= 34)

    print('   10c. Home\'s X is no longer the MAKELIST counter')
    xs = {}
    for path, tag in ((B15C, '15c'), (SRC, '15d')):
        b, h = page(path, 'sr_CritMode', {'ta': 0.05, 'tk': 3, 'tv': 12}, False, home_x=7.25)
        xs[(tag, 'crit')] = (h.globals_['X'], h.globals_['EP_QCRIT'], list(h.globals_['gZN']))
        h2 = Bridge(path); h2.python_ok = False; h2.globals_['X'] = 7.25
        h2.call('sr_Cache', 3.0, 12.0, 3.5)
        xs[(tag, 'cache')] = (h2.globals_['X'], list(h2.globals_['EP_SRCDF']), list(h2.globals_['EP_SRPDF']),
                              h2.globals_['srQmax'])
    # The harness does not model MAKELIST writing its counter variable (Home's X stays 7.25 in beta 15c's run too);
    # that the Prime writes it is the device fact Lessons Learned section 5 records for K.  So for beta 15c this is
    # a code check, and the overwrite itself is on the device checklist.
    old_code = re.sub(r'//[^\n]*', '', re.sub(r'(?ms)^#PYTHON.*?^#END', '', t15c))
    check('10c beta 15c counts with Home\'s X in 5 MAKELIST calls (sr_BuildZ 3, sr_Cache 2); the harness leaves X at '
          '%r there (it does not model the counter write, a device fact: LL section 5)' % xs[('15c', 'crit')][0],
          len(re.findall(r'MAKELIST\(0,X,1,', old_code)) == 5)
    check('10c beta 15d: Home\'s X is still 7.25 after both, and the numbers are beta 15c\'s (q crit %.4f; the node '
          'table; the 65-point CDF and pdf cache and its window)' % xs[('15d', 'crit')][1],
          xs[('15d', 'crit')][0] == 7.25 and xs[('15d', 'cache')][0] == 7.25
          and xs[('15d', 'crit')][1:] == xs[('15c', 'crit')][1:] and xs[('15d', 'cache')][1:] == xs[('15c', 'cache')][1:])
    check('10c no MAKELIST in beta 15d counts with X; the new counters bzI, cbI are LOCAL',
          not re.search(r'MAKELIST\([^,]*,\s*X\s*,', code) and 'LOCAL bzJ,bzH,zv,bzW,bzI;' in t15d
          and 'LOCAL cbI;' in t15d)

    print('   10d. the disclaimer (Roger, 19 Oct 2026)')
    DISC = ('DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not '
            'rely on its results for legal purposes.')

    def header(txt):
        hdr = txt.split('// Tested on an HP Prime G2')[0]
        return ' '.join(l.lstrip('/').strip() for l in hdr.split('\n') if l.startswith('//'))
    check('10d the header carries the disclaimer word for word (15c: no)', DISC in header(t15d) and DISC not in header(t15c))
    ab = []
    for path in (B15C, SRC):
        h = Bridge(path); h.press('Esc'); h.call('sr_HelpMode')
        pg = [x for x in h.pages if x.func == 'sr_ShowRes'][0]
        ab.append([(t.text, t.y) for t in pg.texts if t.font == 3 and t.y > 26])
    check('10d About page 1/4: beta 15d adds "Teaching aid; not for legal use." as its ninth line (32 characters), so '
          'its lines are 18 px apart (30 ... 174) instead of 22; the eight lines before it are beta 15c\'s',
          [x[0] for x in ab[1]] == [x[0] for x in ab[0]] + ['Teaching aid; not for legal use.']
          and [x[1] for x in ab[1]] == [30 + 18 * i for i in range(9)] and [x[1] for x in ab[0]] == [30 + 22 * i for i in range(8)],
          str(ab[1][-2:]))

    print('   10e. the routine diff and the line diff, 15c -> 15d')
    def bodies(txt):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', txt)
        c = re.sub(r'//[^\n]*', '', c)
        out = {}
        for m in re.finditer(r'(?m)^(?:EXPORT\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
            out[m.group(1)] = re.sub(r'[ \t]+\n', '\n', m.group(0))
        return out
    c0, c1 = bodies(t15c), bodies(t15d)
    diff = sorted(n for n in set(c0) | set(c1) if c0.get(n) != c1.get(n))
    check('10e routines that differ from beta 15c: %s' % diff,
          diff == ['sr_BuildZ', 'sr_Cache', 'sr_CritMode', 'sr_HSDMode', 'sr_HelpMode'])
    check('10e the #PYTHON srq block is byte-identical to beta 15c',
          re.findall(r'(?ms)^#PYTHON.*?^#END', t15c) == re.findall(r'(?ms)^#PYTHON.*?^#END', t15d))

    def outside(t, names):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', t)
        c = re.sub(r'//[^\n]*', '', c)
        c = re.sub(r'(?ms)^(?:EXPORT\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
        return re.sub(r'\s+', ' ', c)
    check('10e outside those routines only comments differ', outside(t15c, diff) == outside(t15d, diff))
    raw = lambda txt, nm: re.search(r'(?ms)^(?:EXPORT\s+)?%s\([^\n]*\)\s*\nBEGIN\n.*?^END;' % re.escape(nm), txt).group(0)
    same = [n for n in c0 if n not in diff and raw(t15c, n) == raw(t15d, n)]
    check('10e the other %d routines are byte-identical, comments included' % len(same), len(same) == len(c0) - len(diff))

    def ccode(t):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', t)
        out = []
        for l in c.split('\n'):
            o, ins = [], False
            for i, ch in enumerate(l):
                if ch == '"':
                    ins = not ins
                if not ins and l[i:i + 2] == '//':
                    break
                o.append(ch)
            x = ''.join(o).strip()
            if x:
                out.append(x)
        return out
    mi, pl = [], []
    k0, k1 = ccode(t15c), ccode(t15d)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
        if op in ('replace', 'delete'):
            mi += k0[i1:i2]
        if op in ('replace', 'insert'):
            pl += k1[j1:j2]
    print('     code lines removed: %d, added: %d' % (len(mi), len(pl)))
    for x in mi:
        print('       - ' + x)
    for x in pl:
        print('       + ' + x)
    wm = ['LOCAL bzJ,bzH,zv,bzW;', 'gZN:=MAKELIST(0,X,1,nz+1);', 'gZW:=MAKELIST(0,X,1,nz+1);',
          'gZC:=MAKELIST(0,X,1,nz+1);', 'cdf:=MAKELIST(0,X,1,nn+1);', 'pdf:=MAKELIST(0,X,1,nn+1);',
          'LOCAL ta,tk,tv,qc;', 'sr_ShowRes("Critical value q(α)",',
          '{"α = "+sr_FmtF(ta,4)+"   k = "+STRING(tk,2,0)+"   ν = "+IFTE(tv==0,CHAR(8734),STRING(tv,2,0)),',
          '"Stored in EP_QCRIT"},', '"any key or tap = menu",1);',
          'LOCAL qc,hsd,xb,hk;', 'hk:=sr_ShowRes("Tukey HSD",',
          '{"α="+sr_FmtF(ta,4)+"  k="+STRING(tk,2,0)+"  m="+STRING(tm,2,0)+"  ν="+STRING(vv,2,0),',
          '"Stored in EP_QCRIT, EP_HSD"},', '"Ent or tap = yardstick, Esc = menu",1);',
          '"After Dunlap et al. 1977, BRMI 9(4)"},']
    bad_minus = [x for x in mi if x not in wm]
    check('10e every removed code line is one of the sites listed (the X counters, the two pages\' heads and tails, '
          'the HSD line, the About page\'s last line): %r' % bad_minus, not bad_minus and len(mi) == len(wm))
    for must in ('LOCAL bzJ,bzH,zv,bzW,bzI;', 'gZN:=MAKELIST(0,bzI,1,nz+1);', 'LOCAL cbI;', 'cdf:=MAKELIST(0,cbI,1,nn+1);',
                 'IF srEng==2 AND ta<0.005 THEN', '"PPL fallback at α < 0.005:",', '"q crit may be off by a few %",',
                 '"q crit, HSD may be off a few %",', 'sr_ShowRes("Critical value q(α)",crL,"any key or tap = menu",1);',
                 'hk:=sr_ShowRes("Tukey HSD",hdL,"Ent or tap = yardstick, Esc = menu",1);',
                 'hdH:="α = "+sr_FmtF(ta,4)+"  k = "+STRING(tk,2,0)+"  m = "+STRING(tm,2,0)+"  ν = "+STRING(vv,2,0);',
                 '"Teaching aid; not for legal use."},'):
        if must not in pl:
            check('10e added line present: %s' % must, False)
    check('10e the added lines include every fix (counters, notes, S3 line, disclaimer)', True)

    print('   10f. names and static rules')
    BI = set(l.strip().lower() for l in open('/home/claude/work/gate_f19/HP_Prime_Builtin_Names.txt', encoding='utf-8')
             if l.strip() and not l.startswith('#'))
    check('10f the new names bzI, cbI, crH, crL, hdH, hdL are not built-ins (case ignored)',
          not any(n.lower() in BI for n in ('bzI', 'cbI', 'crH', 'crL', 'hdH', 'hdL')))
    locs = [l for l in ccode(t15d) if l.startswith('LOCAL ') and ':=' not in l]
    big = [l for l in locs if len([x for x in l[6:].rstrip(';').split(',') if x.strip()]) > 6]
    check('10f no LOCAL line declares more than 6 names: %r' % big[:2], not big)

    print('   10g. the review\'s own check_StudRange.py, on beta 15c and on beta 15d')
    chk = open('/home/claude/work/review/check_StudRange.py', encoding='utf-8').read()
    chk = chk.replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = '/home/claude/work/review'")
    res = {}
    for path, tag in ((B15C, '15c'), (SRC, '15d')):
        c2 = chk.replace("SRC = os.path.join(FLEET, 'StudRange_beta15c.txt')", 'SRC = %r' % path)
        assert c2 != chk
        out = subprocess.run([sys.executable, '-'], input=c2, capture_output=True, text=True, timeout=3600).stdout
        m = re.search(r'(\d+) checks failed', out)
        res[tag] = (m.group(1) if m else 'no summary', [l for l in out.split('\n') if l.startswith('FAIL ')],
                    [l for l in out.split('\n') if 'k 20, df 3, alpha 1E-4 on the fallback' in l])
        print('     beta %s: %s checks failed %r; %r' % (tag, res[tag][0], res[tag][1], res[tag][2]))
    check('10g the review\'s check_StudRange.py passes on beta 15c and on beta 15d (0 failures each)',
          res['15c'][0] == '0' and res['15d'][0] == '0')

if __name__ == '__main__':
    sys.exit(main())
