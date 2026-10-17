#!/usr/bin/env python3
"""verify_StudRange_beta15a.py -- checks for StudRange beta 15a (17 Oct 2026), built from
verify_StudRange.py (beta 15): every check is kept and now runs on beta 15a in harness v3c, which
models the emulator's WAIT(-1) answers (MenuTapProbe beta 1: a soft-key tap is ONLY {3, x, y}; a
tap above the strip is {0, x, y}, {2}, {3, x, y}).  Section 7 is new (15a):
  7a the plot's six soft keys fire on a type-3 strip click; 7b beta 15 in v3c: they do nothing (the
  emulator's FAIL); 7c no tap acts twice; 7d a press on the plot and on the q crit box still work,
  once; 7e a page closed by a footer tap leaves no stale click (also in the mouse_tail worst case);
  7f the Quit summary names the q crit's k and df and says "not computed" (SciPy for the numbers);
  7g beta 15a against beta 15: only the routines named in the CHANGES differ, the #PYTHON block is
  byte-identical.

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
SRC = HERE + 'StudRange_beta15a.txt'
OLD = HERE + 'StudRange_beta15.txt'
sys.path.insert(0, '/home/claude/work/out')

FAIL = []
def check(name, ok, detail=''):
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

def main():
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

    print('6. The real PPL source in the harness (v3c)')
    harness_checks(py)

    print('7. beta 15a: the plot soft keys under WAIT(-1), stale clicks, the Quit summary (v3c)')
    harness_checks_15a()

    print()
    print('FAILURES: %d %s' % (len(FAIL), FAIL))
    return 1 if FAIL else 0

# ---------------------------------------------------------------- harness
def harness_checks(py_unused):
    from ppl_run_v3c import Harness, ACCEPT
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
    from ppl_run_v3c import Harness, ACCEPT, CANCEL
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
    # 7b. beta 15 in v3c: nothing happens -- the emulator's "alpha+ does nothing"
    h = plot(OLD, lambda h: (h.tap(slot_x(2), 230), h.tap(slot_x(6), 230)))
    a = [alpha(t) for t in headers(h)]
    check('7b beta 15 in v3c: α+ and Menu do nothing (the emulator\'s FAIL)', set(a) == {0.05}
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
    want = 'StudRange: q crit (k = 4, ν = 28) = %.4f, p not computed, HSD = %.4f (engine: Python)' % (qc, hsd)
    check('7f after HSD only (the emulator\'s run): "%s"' % h.result, h.result == want, 'want ' + want)
    h = Bridge(OLD, idle_key=4)
    h.choose('Tukey HSD'); h.answer({'ta': 0.05, 'tk': 4, 'tm': 8, 'tmse': 1, 'tvo': 0}); h.press('Esc')
    h.choose('Quit'); h.execute('StudRange()')
    check('7f (beta 15 in the same run: "%s" -- the emulator\'s "p = 0.00000")' % h.result, 'p = 0.00000' in h.result)
    h = Bridge(SRC, idle_key=4)
    h.choose('P-value from q'); h.answer({'tq': 3.5, 'tk': 3, 'tv': 12}); h.press('Enter')
    h.choose('Critical value'); h.answer({'ta': 0.05, 'tk': 3, 'tv': 12}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    want = 'StudRange: q crit (k = 3, ν = 12) = %.4f, p = %.5f, HSD not computed (engine: Python)' % (
        sr.ppf(0.95, 3, 12), sr.sf(3.5, 3, 12))
    check('7f after P-value and Critical value: "%s"' % h.result, h.result == want, 'want ' + want)
    h = Bridge(SRC, idle_key=4); h.python_ok = False
    h.choose('Critical value'); h.answer({'ta': 0.05, 'tk': 3, 'tv': 2}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    check('7f the PPL fallback raised df 2 to 3: the summary names the df it used, ν = 3 ("%s")' % h.result,
          h.result.startswith('StudRange: q crit (k = 3, ν = 3) = ') and '(engine: PPL)' in h.result)
    h = Bridge(SRC, idle_key=4)
    h.choose('Critical value'); h.answer({'ta': 0.05, 'tk': 3, 'tv': 0}); h.press('Enter')
    h.choose('Quit'); h.execute('StudRange()')
    check('7f df 0 (infinity) is named with the infinity sign ("%s")' % h.result, 'ν = ' + chr(8734) + ')' in h.result)
    # 7g. beta 15a against beta 15
    def bodies(txt):
        c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', txt)
        c = re.sub(r'//[^\n]*', '', c)
        out = {}
        for m in re.finditer(r'(?m)^(?:EXPORT\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
            out[m.group(1)] = re.sub(r'[ \t]+\n', '\n', m.group(0))
        return out
    t0, t1 = open(OLD, encoding='utf-8').read(), open(SRC, encoding='utf-8').read()
    b0, b1 = bodies(t0), bodies(t1)
    diff = sorted(n for n in set(b0) | set(b1) if b0.get(n) != b1.get(n))
    want = ['StudRange', 'sr_CritMode', 'sr_HSDMode', 'sr_PlotMode', 'sr_PvMode', 'sr_WaitAny']
    check('7g routines that differ from beta 15: %s' % diff, diff == want, 'want %s' % want)
    py0 = re.findall(r'(?ms)^#PYTHON.*?^#END', t0); py1 = re.findall(r'(?ms)^#PYTHON.*?^#END', t1)
    check('7g the #PYTHON srq block is byte-identical to beta 15', py0 == py1 and len(py1) == 1)

if __name__ == '__main__':
    sys.exit(main())
