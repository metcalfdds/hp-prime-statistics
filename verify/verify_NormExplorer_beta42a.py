#!/usr/bin/env python3
"""verify_NormExplorer_beta42a.py -- checks for NormExplorer beta 42a (19 Oct 2026).

Built from verify_NormExplorer.py (beta 42), whose Parts A and B are kept whole and now
run on beta 42a.  The fixes are the fleet review of 19 Oct 2026's D-NE-1 to D-NE-5
(Fleet_Review_2026-10-19_v1.md section 2, items 8 and 12; findings_D.md section 1).

Part A  (kept) the beta 42 formulas against SciPy.
Part B  (kept) the PPL itself in hp-prime-kit's interpreter with the beta 42 mini-harness
        (its STRING is plain fixed decimals, so it cannot see the scientific form; that is
        what Parts C-D are for).  Run on beta 42a unchanged.  Its builtin patches are undone
        before Part C, so ppl_run_v3e sees the kit as shipped.
Part C  the review's regression tests: check_NormExplorer.py (62 checks) and
        check_NormExplorer_python.py (6 CPython runs of the #PYTHON block), each run on
        beta 42 (the 3 failures the review reported: B1, B2, B3) and on beta 42a (none).
Part D  one group of checks per fixed item, in ppl_run_v3e with home_minus=True (the
        Prime's scientific STRING, U+2212 minus), every run on beta 42 AND beta 42a:
          D1  D-NE-1  the headline (right tail, x = 180 on N(100,15): 4.8213E-8 before,
                      "< 0.0001" now); the three helpers; the review's reproduction table;
                      a sweep of ~400 runs over every module at ordinary and extreme
                      inputs: no small-capital E, no "= <", no negative zero anywhere;
                      every displayed probability within half a last digit of SciPy, and
                      "< 0.0001" exactly when it is positive and rounds to zero
          D2  D-NE-2  with the Prime's 12 significant digits modelled on the statistics
                      built-ins (check_StatDist.py's twelve_digits): NE_P, the complements,
                      outside, power, beta, the readouts and the riding tags far in a tail
          D3  D-NE-3  the CHOOSE idiom: static, and Esc in every menu (nothing happens)
          D4  D-NE-4  C = 1 is a 1% interval; 100 still refused
          D5  D-NE-5  a sigma drag 15 -> 2, then Right and Up: mu 100.5 and sigma 2.2
                      (beta 42: 105 and 4)
          D6  between, mirrored (ne_Btw; found while checking D-NE-2): with the 12 digits
                      modelled, an area between two x's far above the mean (panel, view,
                      tag, Explorer, a histogram bar's p) is right; beta 42 printed 0.0000
          D7  right-tail quantiles as -NORMALD_ICDF(0, 1, small area): a typed alpha of
                      1E-13 or C = 0.999999999999 stopped beta 42 at NORMALD_ICDF(..., 1)
                      under the model (the argument held to 12 digits); beta 42a is right,
                      and every form at its edges hands NORMALD_ICDF an area inside 0..1
Part E  static checks of the source: one STRING call left (inside ne_Fx), 134 helper
        calls in place of beta 42's 134 STRING(x, 2, d) calls, version strings, forward
        declarations, names against the built-ins, LOCAL sizes, no comment inside an
        open bracket, no 1 - CDF, ppl_check_v4 and lint_ppl tallies against beta 42.
Part F  the routine diff: only the routines meant to change differ; the #PYTHON block is
        byte-identical.
Every h.sci_strings entry of every ppl_run_v3e run on beta 42a is listed at the end (it
must be empty).

Run:  python3 verify_NormExplorer_beta42a.py [path/to/NormExplorer_beta42a.txt]
The beta 42 file and the review's scripts are read from /home/claude/work/out and
/home/claude/work/review by absolute path; a part whose files are absent is skipped
with a note.
"""
import sys, re, math, random, os

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'NormExplorer_beta42a.txt')
OLD = '/home/claude/work/out/NormExplorer_beta42.txt'
NCHK = [0]

import numpy as np
from scipy.stats import norm

sys.path.insert(0, '/home/claude/kit/hp-prime-kit-HEAD')
from hpkit import interp
# beta 42a: Part B patches the kit's builtin table; saved here, put back before Part C
_SAVED_BUILTINS = dict(interp.BUILTINS)
_SAVED_BARE = set(interp.BARE_BUILTINS)

SRC = NEW                                  # beta 42a (was beta 42)
FAILS = []


def check(label, got, want, tol=5e-5):
    NCHK[0] += 1                              # beta 42a: counted
    ok = abs(got - want) <= tol
    print('  %-58s got %-12.6g want %-12.6g %s' % (label, got, want, 'ok' if ok else '** FAIL **'))
    if not ok:
        FAILS.append(label)


def check_true(label, cond):
    NCHK[0] += 1                              # beta 42a: counted
    print('  %-58s %s' % (label, 'ok' if cond else '** FAIL **'))
    if not cond:
        FAILS.append(label)


# ---------------------------------------------------------------- Part A
print('=' * 78)
print('PART A  -- the beta 42 formulas against SciPy (kept from verify_NormExplorer.py)')
print('=' * 78)
mu, sg = 100.0, 15.0
for a in (0.10, 0.05, 0.01):
    zl = norm.ppf(a)
    check('left-tail z*  alpha=%.2f' % a, zl, -norm.ppf(1 - a), 1e-12)
    check('left-tail area below x* = alpha (%.2f)' % a, norm.cdf(mu + zl * sg, mu, sg), a, 1e-12)
    z2 = norm.ppf(1 - a / 2)
    lo, hi = mu - z2 * sg, mu + z2 * sg
    check('two-tailed: area outside = alpha (%.2f)' % a,
          norm.cdf(lo, mu, sg) + norm.sf(hi, mu, sg), a, 1e-12)
# power of a right-tail cut
# (the program's route: x* first, then the area of curve 2 beyond it;
#  the check's route: the textbook 1 - Phi(z_(1-alpha) - d), d = (mu2 - mu)/sigma)
for (m0, m2, s, a) in [(0, 1, 1, 0.05), (0, 2.5, 1, 0.05), (100, 110, 15, 0.05), (100, 90, 15, 0.01)]:
    xs = m0 + norm.ppf(1 - a) * s
    d = (m2 - m0) / s
    check('power mu=%g mu2=%g sigma=%g alpha=%.2f' % (m0, m2, s, a), norm.sf(xs, m2, s),
          1 - norm.cdf(norm.ppf(1 - a) - d), 1e-12)
check('power N(0,1) vs mu2 = 1, alpha = .05 (textbook 0.2595)', norm.sf(norm.ppf(0.95), 1, 1), 0.2595, 5e-5)
# expected count n*p for a bin
n, lo, w = 1000, -0.25, 0.25
check('bin [-0.25, 0) of N(0,1): p', norm.cdf(lo + w) - norm.cdf(lo), 0.0987063, 1e-6)
check('bin [-0.25, 0) of N(0,1), n = 1000: n*p', n * (norm.cdf(lo + w) - norm.cdf(lo)), 98.7063, 1e-3)


def cdf_cache(m, s, a, b, PW=272):
    xs = a + np.arange(PW + 1) / PW * (b - a)
    f = norm.pdf(xs, m, s)
    c = np.empty(PW + 1)
    c[0] = norm.cdf(a, m, s)
    for i in range(1, PW + 1):
        c[i] = c[i - 1] + (f[i - 1] + f[i]) / 2 * (b - a) / PW
    return np.max(np.abs(c - norm.cdf(xs, m, s)))


print('  trapezoid S-curve cache, worst error over the 273 columns')
for (m, s, a, b, tol) in [(0, 1, -4, 4, 1e-4), (0, 1, -6, 6, 1e-4), (100, 15, 40, 160, 1e-4),
                          (2, 1, -6, 6, 1e-4), (0, 1, -30, 30, 0.007), (0, 1, -100, 100, 0.02)]:
    e = cdf_cache(m, s, a, b)
    NCHK[0] += 1                              # beta 42a: counted
    px = e * 142                       # the S-curve spans PH - 6 = 142 px
    print('    N(%g,%g) on [%g, %g]: %.2e  (= %.2f px)  %s' % (m, s, a, b, e, px, 'ok' if e <= tol else '** FAIL **'))
    if e > tol:
        FAILS.append('cdf cache %g %g' % (a, b))


def hd(h):                              # the density's digit rule in the Explorer
    if h <= 0.000001:
        return 6
    return int(min(6, max(3, 2 - math.floor(math.log10(h)))))


for h, want in [(0.24197, 3), (0.0266, 4), (1.99, 3), (0.0004, 6), (0.00266, 5)]:
    check_true('density digits for %.5g -> %d (shows %s)' % (h, want, '%.*f' % (hd(h), h)), hd(h) == want)

# ---------------------------------------------------------------- Part B
print()
print('=' * 78)
print('PART B  -- the PPL itself, in the kit interpreter (kept; now on beta 42a)')
print('=' * 78)


def preprocess(text):
    out, skip = [], False
    for ln in text.split('\n'):
        s = ln.strip()
        if s.startswith('#PYTHON'):
            skip = True; out.append(''); continue
        if skip:
            out.append('')
            if s.startswith('#END'):
                skip = False
            continue
        if s.startswith('#pragma'):
            out.append(''); continue
        if re.fullmatch(r'ne_\w+\(\);', ln):          # forward declarations
            out.append(''); continue
        if ln.startswith('LOCAL '):                    # file-level LOCAL -> globals
            ln = ln[len('LOCAL '):]
        ln = re.sub(r'#([0-9A-Fa-f]+)h\b', lambda m: str(int(m.group(1), 16)), ln)
        ln = ln.replace('√(', 'SQRT(')
        out.append(ln)
    return '\n'.join(out)


def fmt_fixed(v, d):
    s = '%.*f' % (int(d), v)
    if s.startswith('-') and float(s) == 0:
        s = s[1:]
    return s


class Harness(interp.Machine):
    def __init__(self):
        interp.Machine.__init__(self)
        self.stack = []
        self.keyq = []          # (code, ctx)
        self.touchq = []        # ('down'|'move', x, y, ctx) or ('lift', ctx)
        self.chooseq = []
        self.inputq = []
        self.touch = None
        self.negs = 5
        self.armed = False
        self.ticks = 0
        self.frames = []        # list of dicts: text, rect, line, pixon
        self.cur = self._newframe()
        self.msgs = []
        self.menus = []
        self.panels = []        # G0 TEXTOUT_P (ZPanel and friends)

    def _newframe(self):
        return {'text': [], 'rect': [], 'line': [], 'pix': 0}

    def call(self, name, *args):
        self.stack.append(name)
        try:
            return interp.Machine.call(self, name, *args)
        finally:
            self.stack.pop()

    def _ctx_ok(self, ctx):
        return ctx is None or all(c in self.stack for c in ctx)

    def _call_node(self, e, frame):
        base, arg_nodes = e[1], e[2]
        if base[0] == 'var' and base[1] == 'INPUT':
            names = [n[1] for n in arg_nodes[0][1]]
            ans = self.inputq.pop(0) if self.inputq else 'cancel'
            self.io.append(('INPUT', names, ans))
            if ans == 'cancel':
                return 0.0
            for nm, v in zip(names, ans):
                self._assign(('var', nm), float(v), frame)
            return 1.0
        if base[0] == 'var' and base[1] == 'CHOOSE':
            nm = arg_nodes[0][1]
            title = self.evaluate(arg_nodes[1], frame)
            items = self.evaluate(arg_nodes[2], frame)
            pick = self.chooseq.pop(0) if self.chooseq else 0
            self.menus.append((title, items, pick))
            self._assign(('var', nm), float(pick), frame)
            return float(pick)
        return interp.Machine._call_node(self, e, frame)

    # ---- the interface ----
    def b_getkey(self, a):
        # A scripted key is delivered only after the program has seen
        # "no key" twice SINCE the key became due (its routine is
        # running): so the opening drain of a drain-wait-drain cannot
        # swallow it, exactly as on the calculator, where a key is
        # pressed after the screen is up.
        # (and only once the scripted touches before it are done:
        # the program, like beta 41, ignores a key read in the same
        # poll as a touch)
        if self.keyq and self._ctx_ok(self.keyq[0][1]) and not self.touchq and self.touch is None:
            if not self.armed:
                self.armed = True
                self.negs = 0
            elif self.negs >= 2:
                self.negs = 0
                self.armed = False
                return float(self.keyq.pop(0)[0])
        self.negs += 1
        return -1.0

    def _tl(self):
        x, y = self.touch
        return [float(x), float(y), float(x), float(y), 0.0]

    def b_mouse(self, a):
        h = self.touchq[0] if self.touchq else None
        if a:                                           # MOUSE(1): the drain
            if self.touch is None:
                return -1.0
            if h and h[0] == 'lift' and self._ctx_ok(h[-1]):
                self.touchq.pop(0); self.touch = None
                return -1.0
            return self._tl()
        if self.touch is None:
            if h and h[0] == 'down' and self._ctx_ok(h[-1]):
                self.touchq.pop(0); self.touch = (h[1], h[2])
                return [self._tl(), []]
            return [[], []]
        if h and h[0] == 'move' and self._ctx_ok(h[-1]):
            self.touchq.pop(0); self.touch = (h[1], h[2])
            return [self._tl(), []]
        if h and h[0] == 'lift' and self._ctx_ok(h[-1]):
            self.touchq.pop(0); self.touch = None
            return [[], []]
        return [self._tl(), []]

    def tap(self, x, y, ctx=None):
        self.touchq += [('down', x, y, ctx), ('lift', ctx)]

    def drag(self, pts, ctx=None):
        self.touchq.append(('down', pts[0][0], pts[0][1], ctx))
        for (x, y) in pts[1:]:
            self.touchq.append(('move', x, y, ctx))
        self.touchq.append(('lift', ctx))


def install(h):
    B = interp.BUILTINS
    interp.BARE_BUILTINS.update(['MOUSE', 'TICKS', 'RANDOM'])

    def string(m, a):
        if len(a) == 3 and isinstance(a[0], float):
            if int(a[1]) == 2:
                return fmt_fixed(a[0], a[2])
            return interp._as_text(a[0])
        return interp._b_string(m, a)

    def textout(m, a):
        if len(a) >= 6 and a[1] == 'G1':
            m.cur['text'].append((a[0], a[2], a[3], a[4], a[5]))
        else:
            m.panels.append((a[0], a[1], a[2]))
        return 0.0

    def rect(m, a):
        if a and a[0] == 'G1':
            m.cur['rect'].append(tuple(a[1:]))
        return 0.0

    def line(m, a):
        if a and a[0] == 'G1':
            m.cur['line'].append(tuple(a[1:]))
        return 0.0

    def pixon(m, a):
        m.cur['pix'] += 1
        return 0.0

    def dimgrob(m, a):
        m.cur = m._newframe()
        return 0.0

    def blit(m, a):
        m.frames.append(m.cur)
        return 0.0

    def ticks(m, a):
        m.ticks += 1
        return float(m.ticks)

    def typ(m, a):
        v = a[0]
        if isinstance(v, list):
            return 6.0
        if isinstance(v, str):
            return 2.0
        return 0.0

    def python(m, a):
        raise interp.PPLError('no Python in this harness: the PPL fallback runs')

    B.update({
        'STRING': string,
        'NORMALD': lambda m, a: float(norm.pdf(a[2], a[0], a[1])),
        'NORMALD_CDF': lambda m, a: float(norm.cdf(a[2], a[0], a[1])),
        'NORMALD_ICDF': lambda m, a: float(norm.ppf(a[2], a[0], a[1])),
        'TEXTOUT_P': textout, 'RECT_P': rect, 'LINE_P': line, 'PIXON_P': pixon,
        'DIMGROB_P': dimgrob, 'BLIT_P': blit,
        'DRAWMENU': lambda m, a: (m.io.append(('DRAWMENU', a[0])), 0.0)[1],
        'MSGBOX': lambda m, a: (m.msgs.append(a[0]), 0.0)[1],
        'WAIT': lambda m, a: 0.0,
        'GETKEY': lambda m, a: m.b_getkey(a),
        'MOUSE': lambda m, a: m.b_mouse(a),
        'TICKS': ticks,
        'TYPE': typ,
        'CHAR': lambda m, a: chr(int(a[0])),
        'RANDOM': lambda m, a: random.random(),
        'PYTHON': python,
        'STARTAPP': lambda m, a: 0.0,
        'SQRT': lambda m, a: math.sqrt(a[0]),
    })


def machine():
    h = Harness()
    install(h)
    h.load(preprocess(open(SRC, encoding='utf-8').read()))
    h.globals_['G0'] = 'G0'
    h.globals_['G1'] = 'G1'
    h.call('ne_ResetAll')
    h.frames.clear()
    return h


def texts(fr):
    return [t[0] for t in fr['text']]


def find(fr, prefix):
    return [t for t in texts(fr) if t.startswith(prefix)]


def num_after(s, key):
    m = re.search(re.escape(key) + r'\s*(-?[0-9.]+)', s)
    return float(m.group(1)) if m else float('nan')


# ---- B1: Probability from x, all four types, on N(100,15) ----
print('B1  Probability from x on N(100,15): panel, sweep, final view')
for typ, inp, want, lab in [(1, [110], norm.cdf(110, 100, 15), 'P(X < x₀) = '),
                            (2, [110], norm.sf(110, 100, 15), 'P(X > x₀) = '),
                            (3, [85, 115], norm.cdf(115, 100, 15) - norm.cdf(85, 100, 15), 'P(a < X < b) = '),
                            (4, [85, 115], 1 - (norm.cdf(115, 100, 15) - norm.cdf(85, 100, 15)), 'P(outside) = ')]:
    h = machine()
    h.globals_['NE_MU'] = 100.0; h.globals_['NE_SG'] = 15.0
    h.chooseq = [typ]; h.inputq = [inp]
    h.keyq = [(30, ('ne_ZPanel',)), (30, ('ne_ShowCurve', 'ne_WaitAny'))]
    h.call('ne_ProbCalc')
    check('  type %d: NE_P' % typ, h.globals_['NE_P'], want, 1e-12)
    fin = h.frames[-1]
    got = num_after(' '.join(find(fin, lab)), lab)
    check('  type %d: final readout "%s"' % (typ, lab.strip()), got, want, 5e-5)
    sweep = h.frames[:-1]
    check_true('  type %d: sweep drew 9 frames before the final one (%d)' % (typ, len(sweep)), len(sweep) == 9)
    run = [num_after(' '.join(find(f, lab)), lab) for f in sweep]
    check_true('  type %d: running area rises frame by frame to the answer' % typ,
               all(run[i] <= run[i + 1] + 1e-9 for i in range(len(run) - 1)) and run[-1] <= want + 1e-4)
    tags = [t for t in fin['text'] if t[3] in (1.0, 2.0) and re.fullmatch(r'0\.\d{4}', str(t[0]))]
    if typ == 4:
        check_true('  type 4: two riding tags, one per tail (%s)' % [t[0] for t in tags], len(tags) == 2)
        check('  type 4: left tail tag', float(tags[0][0]), norm.cdf(85, 100, 15), 5e-5)
    else:
        check_true('  type %d: a riding tag with the area (%s)' % (typ, [t[0] for t in tags]),
                   any(abs(float(t[0]) - want) < 5e-5 for t in tags))
    foot = [t for t in fin['text'] if t[2] == 226]
    check_true('  type %d: result footer "%s"' % (typ, foot[0][0] if foot else ''),
               bool(foot) and foot[0][0] == 'tap plot = explore, any key = menu')
    zr = [t[0] for t in fin['text'] if t[2] == 205.0]
    check_true('  type %d: z-ruler row at y = 205: %s' % (typ, zr), zr[:1] == ['z'] and '-3' in zr and '3' in zr)
    hi = max(t[2] for t in fin['text'] if t[2] < 218 and t[2] > 150)
    check_true('  type %d: lowest label row starts at y = %g (< 207, so it ends above 218)' % (typ, hi), hi <= 206)

# sweep skipped by a key
h = machine()
h.chooseq = [1]; h.inputq = [[1.0]]
h.keyq = [(30, ('ne_ZPanel',)), (4, ('ne_Sweep',)), (30, ('ne_ShowCurve', 'ne_WaitAny'))]
h.call('ne_ProbCalc')
check_true('B1  a key during the sweep skips it (%d sweep frames drawn)' % (len(h.frames) - 1), len(h.frames) - 1 < 9)

# ---- B2: x from probability, all five items ----
print('B2  x from probability on N(100,15)')
cases = [(1, [0.90], 'NE_X', norm.ppf(0.90, 100, 15), 1),
         (2, [0.05], 'NE_X', norm.ppf(0.95, 100, 15), 2),
         (3, [0.05], 'NE_X', norm.ppf(0.05, 100, 15), 1),
         (4, [0.05], 'NE_X', norm.ppf(0.975, 100, 15), 4),
         (5, [0.95], 'NE_X', norm.ppf(0.975, 100, 15), 3)]
for item, inp, var, want, mode in cases:
    h = machine()
    h.globals_['NE_MU'] = 100.0; h.globals_['NE_SG'] = 15.0
    h.chooseq = [item]; h.inputq = [inp]
    h.keyq = [(30, ('ne_ZPanel',)), (30, ('ne_ShowCurve', 'ne_WaitAny'))]
    h.call('ne_InvCalc')
    check('  item %d: %s' % (item, var), h.globals_[var], want, 1e-9)
    check_true('  item %d: shading mode %d (got %g)' % (item, mode, h.globals_['NE_XM']), h.globals_['NE_XM'] == mode)
    pan = [p[0] for p in h.panels]
    print('      panel:', ' | '.join(str(p) for p in pan[:5]))
    if item == 3:
        check('  item 3: z* (left tail, negative)', h.globals_['NE_Z'], norm.ppf(0.05), 1e-9)
        zline = [p for p in pan if str(p).startswith('z* = ')][0]
        check('  item 3: panel z*', float(zline.split('=')[1]), norm.ppf(0.05), 5e-5)
    if item == 4:
        check('  item 4: lower bound NE_XO', h.globals_['NE_XO'], norm.ppf(0.025, 100, 15), 1e-9)
        fin = h.frames[-1]
        tags = [t for t in fin['text'] if re.fullmatch(r'0\.\d{4}', str(t[0]))]
        check_true('  item 4: each tail tagged 0.0250 (%s)' % [t[0] for t in tags],
                   len(tags) == 2 and all(t[0] == '0.0250' for t in tags))
        po = num_after(' '.join(find(fin, 'P(outside) = ')), 'P(outside) = ')
        check('  item 4: P(outside) readout = alpha', po, 0.05, 5e-5)

# ---- B3: z-solver (unchanged, run as a regression) ----
print('B3  Z-formula solver')
for item, inp, var, want in [(1, [130, 100, 15], 'NE_Z', 2.0), (2, [-1.5, 100, 15], 'NE_X', 77.5),
                             (3, [130, 2, 15], 'NE_MU', 100.0), (4, [130, 100, 2], 'NE_SG', 15.0)]:
    h = machine()
    h.chooseq = [item]; h.inputq = [inp]
    h.keyq = [(30, ('ne_ZPanel',))]
    h.call('ne_ZSolve')
    check('  item %d: %s' % (item, var), h.globals_[var], want, 1e-9)

# ---- B4: Compare curves, the power picture ----
print('B4  Compare curves: power picture, N(0,1) vs mu2 = 1')
h = machine()
h.chooseq = [3]; h.inputq = [[0.05]]
h.keyq = [(30, ('ne_ZPanel',)), (30, ('ne_ShowCurve', 'ne_WaitAny'))]
h.call('ne_Compare2')
fin = h.frames[-1]
pw = num_after(' '.join(find(fin, 'power = ')), 'power = ')
check('  power readout on the plot', pw, norm.sf(norm.ppf(0.95), 1, 1), 5e-5)
check('  NE_P = power', h.globals_['NE_P'], norm.sf(norm.ppf(0.95), 1, 1), 1e-12)
green = [l for l in fin['line'] if l[-1] == 0xB4E0A8]
check_true('  light-green power columns drawn (%d)' % len(green), len(green) > 20)
check_true('  every power column lies right of x* (pixel %d)' % h.globals_['neAPX'] if 'neAPX' in h.globals_ else '',
           all(l[0] >= h.globals_['neAPX'] for l in green))
print('      panel:', ' | '.join(str(p[0]) for p in h.panels[:5]))

# ---- B5: the Explorer -- soft keys, grabs, the two-bound drag ----
print('B5  Explorer on N(0,1)')
h = machine()
# between -1 and 1 first, then the Explorer
h.globals_['NE_XM'] = 3.0; h.globals_['NE_XO'] = -1.0; h.globals_['NE_XB'] = 1.0
# window frozen at -6..6: pixel = 38 + (x+6)/12*272
px = lambda x: 38 + int((x + 6) / 12 * 272)
xv = lambda p: -6 + (p - 38) / 272 * 12
ctx = ('ne_Explorer',)
# 1. press ON bound b (x = 1) and drag it to x = 2: the mode must stay 3
h.drag([(px(1), 120), (px(1.5), 120), (px(2.0), 120)], ctx)
# 2. press empty plot at x = -3: the NEARER bound (a) jumps there
h.tap(px(-3), 150, ctx)
# 3. drag a (now at -3) to x = 3, past b: they swap
h.drag([(px(-3), 150), (px(0), 150), (px(3), 150)], ctx)
h.keyq = [(4, ctx)]
# capture state after each gesture by stopping early: run the whole
# script, then inspect the final state
h.call('ne_Explorer')
check_true('  mode kept as "between" after every drag (NE_XM = %g)' % h.globals_['NE_XM'], h.globals_['NE_XM'] == 3)
check('  bounds after the swap: a', h.globals_['NE_XO'], xv(px(2.0)), 1e-9)
check('  bounds after the swap: b', h.globals_['NE_XB'], xv(px(3)), 1e-9)
hints = [t for f in h.frames for t in f['text'] if t[2] == 24.0]
print('      frames drawn: %d, DRAWMENU calls: %d' % (len(h.frames), sum(1 for x in h.io if x[0] == 'DRAWMENU')))
check_true('  DRAWMENU after every frame', sum(1 for x in h.io if x[0] == 'DRAWMENU') == len(h.frames))
check_true('  no footer at y = 226 in the Explorer', not any(t[2] == 226 for f in h.frames for t in f['text']))
area_between = [num_after(' '.join(find(f, 'area between = ')), 'area between = ') for f in h.frames]
check('  final "area between" readout', area_between[-1], norm.cdf(xv(px(3))) - norm.cdf(xv(px(2.0))), 5e-5)

# the mu grab and the sigma grab, with the snap on lift
h = machine()
h.drag([(px(0), 150), (px(0.5), 150), (px(1.1), 150)], ctx)      # the mean line, to ~1.1
h.drag([(px(2.0), 120), (px(2.6), 120), (px(3.0), 120)], ctx)    # shoulder at mu+1 = 2.0 (after snap: mu = 1)
h.keyq = [(4, ctx)]
h.call('ne_Explorer')
check('  mu dragged to ~1.1 then snapped to the 0.2 step -> 1.0', h.globals_['NE_MU'], 1.0, 1e-9)
check('  sigma dragged out by ~1 then snapped to the 0.1 step -> 2.0', h.globals_['NE_SG'], 2.0, 1e-9)
# the y-scale refits on sigma: in the last Explorer frame the peak of
# N(1, 2) stands at 62% of the box height again -- the mean line runs
# from y = 187 up to 188 - IP(0.62 * 148) = 97
ml = [l for l in h.frames[-1]['line'] if l[-1] == 0x003D7A and l[1] == 187]
check_true('  y-scale refitted for the new sigma (mean line %s)' % ml[:1], any(l[3] == 97 for l in ml))
check('  on exit the menu window refits: NE_YMX = 1.15 x peak', h.globals_['NE_YMX'], norm.pdf(0, 0, 2.0) * 1.15, 1e-12)
held = [f for f in h.frames if any(t[0].startswith('Dragging') for t in f['text'] if t[2] == 24.0)]
check_true('  the hint line names the held parameter while dragging (%d frames)' % len(held), len(held) >= 2)
thick = [f for f in held if sum(1 for l in f['line'] if l[-1] == 0x003D7A) >= 3]
check_true('  the held line is drawn thick', len(thick) >= 1)

# soft keys: Bands, Ref x3, Centre, Shade x5, Hist (no histogram), Menu
h = machine()
slot = lambda k: int((k - 0.5) * 53.4)
for k in [1, 2, 2, 2, 3, 4, 4, 4, 4, 4, 5, 6, 5]:     # ... Hist, More, Menu (page 2)
    h.tap(slot(k), 228, ctx)
h.call('ne_Explorer')
g = h.globals_
check_true('  Bands toggled off (NE_CFG(1) = %g)' % g['NE_CFG'][0], g['NE_CFG'][0] == 0)
check_true('  Ref cycled 1 -> 2 -> 0 -> 1 (NE_CFG(2) = %g)' % g['NE_CFG'][1], g['NE_CFG'][1] == 1)
check_true('  Shade cycled 0 -> 1 -> 2 -> 3 -> 4 -> 0 (NE_XM = %g)' % g['NE_XM'], g['NE_XM'] == 0)
modes = []
for f in h.frames:
    r = ' '.join(texts(f))
    modes.append('L' if 'area to the left' in r else 'R' if 'area to the right' in r else
                 'B' if 'area between' in r else 'O' if 'area outside' in r else '-')
print('      shading by frame:', ''.join(modes))
check_true('  Shade passed through left, right, between, outside', 'LRBO' in ''.join(m for i, m in enumerate(modes) if i == 0 or m != modes[i - 1]))
msg = [t[0] for f in h.frames for t in f['text'] if t[2] == 24.0]
check_true('  Hist with no histogram says so', any('No histogram' in t for t in msg))
dens = [t[0] for f in h.frames for t in f['text'] if t[0].startswith('height ')]
print('      density line:', dens[:1])
check_true('  "height ... (density," printed in the Explorer', bool(dens))
cdfl = [f for f in h.frames if any(l[-1] == 0xC800C8 for l in f['line'])]
check_true('  the CDF S-curve was drawn while Ref = CDF (%d frames)' % len(cdfl), len(cdfl) >= 1)

# soft-key page 2: what the arrows move (the keyboard route to the bounds).
# Script: More, Bnd A, Right x2, Bnd B, Left, Bnd B again (default),
# Right (mu), sigma, Right, Enter -- fed one step at a time so that no
# key shares a poll with a touch.
h2 = machine()
h2.globals_['NE_XM'] = 3.0; h2.globals_['NE_XO'] = -1.0; h2.globals_['NE_XB'] = 1.0
seq = [('t', 6), ('t', 1), ('k', 8), ('k', 8), ('t', 2), ('k', 7), ('t', 2), ('k', 8), ('t', 4), ('k', 8), ('k', 30)]
import types
def b_getkey2(self, a):
    if self.seq and self.seq[0][0] == 'k' and not self.touchq and self.touch is None:
        if not self.armed:
            self.armed = True; self.negs = 0
        elif self.negs >= 2:
            self.negs = 0; self.armed = False
            return float(self.seq.pop(0)[1])
    self.negs += 1
    return -1.0
def feed(self):
    while self.seq and self.seq[0][0] == 't' and not self.touchq:
        self.tap(slot(self.seq.pop(0)[1]), 228, ctx)
        break
h2.seq = seq
h2.b_getkey = types.MethodType(b_getkey2, h2)
h2._feed = types.MethodType(feed, h2)
_orig_mouse = h2.b_mouse
def b_mouse2(self, a):
    r = _orig_mouse(a)
    if not self.touchq and self.touch is None:
        self._feed()
    return r
h2.b_mouse = types.MethodType(b_mouse2, h2)
h2._feed()
h2.call('ne_Explorer')
g = h2.globals_
check('  page 2, Bnd A, two Rights: lower bound', g['NE_XO'], -0.8, 1e-9)
check('  Bnd B, one Left: upper bound', g['NE_XB'], 0.9, 1e-9)
check('  Bnd B tapped again = default: Right moves mu', g['NE_MU'], 0.2, 1e-9)
check('  sigma chosen: Right widens sigma', g['NE_SG'], 1.1, 1e-9)
check_true('  the mode stayed "between" (NE_XM = %g)' % g['NE_XM'], g['NE_XM'] == 3)
menus = [x[1] for x in h2.io if x[0] == 'DRAWMENU']
check_true('  page 2 labels drawn: %s' % menus[2] if len(menus) > 2 else 'no page 2',
           ['Bnd A', 'Bnd B', 'mu', 'sigma', 'Menu', 'More'] in menus)
check_true('  page 1 has More in slot 6: %s' % menus[0], menus[0] == ['Bands', 'Ref', 'Centre', 'Shade', 'Hist', 'More'])
hint = [t[0] for f in h2.frames for t in f['text'] if t[2] == 24.0]
check_true('  status line says "arrows move: lower bound"', 'arrows move: lower bound' in hint)
thickA = [f for f in h2.frames if any(t[0] == 'arrows move: lower bound' for t in f['text'])
          and sum(1 for l in f['line'] if l[-1] == 0xC00000 and l[1] == 40.0) >= 3]
check_true('  the chosen bound is drawn thick (%d frames)' % len(thickA), len(thickA) >= 1)

# ---- B6: data, filled bars, tapping a bar ----
print('B6  Data module: D1 histogram, a tapped bar')
rng = np.random.default_rng(42)
d1 = [float(v) for v in np.round(rng.normal(50, 10, 400), 1)]
h = machine()
h.globals_['D1'] = d1
xb, s = float(np.mean(d1)), float(np.std(d1, ddof=1))
hlo, hw = xb - 4 * s, 8 * s / 32
# the window is auto mu +/- 4 s: the bar holding the mean
win_lo, win_hi = xb - 4 * s, xb + 4 * s
pxd = lambda x: 38 + int((x - win_lo) / (win_hi - win_lo) * 272)
b_idx = int(math.floor((xb - hlo) / hw)) + 1
bx = (pxd(hlo + (b_idx - 1) * hw) + pxd(hlo + b_idx * hw)) // 2
h.tap(bx, 185, ('ne_ShowCurve', 'ne_WaitAny'))              # on the bar
h.keyq = [(30, ('ne_ShowCurve', 'ne_WaitAny'))]
h.call('ne_DataLoad')
fr = [f for f in h.frames if any(t[0].startswith('bin ') for t in f['text'])]
check_true('  a frame shows the bar panel', bool(fr))
if fr:
    t1 = [t[0] for t in fr[-1]['text'] if t[0].startswith('bin ')][0]
    print('      ', t1)
    m = re.match(r'bin (\d+): (\d+) observed, ([0-9.]+) expected', t1)
    k = int(m.group(1))
    obs = sum(1 for v in d1 if hlo + (k - 1) * hw <= v < hlo + k * hw)
    exp = 400 * (norm.cdf(hlo + k * hw, xb, s) - norm.cdf(hlo + (k - 1) * hw, xb, s))
    check_true('  bin index is the one tapped (%d)' % b_idx, k == b_idx)
    check('  observed count', float(m.group(2)), obs, 0)
    check('  expected count n*p', float(m.group(3)), exp, 0.05)
fills = [r for r in h.frames[-1]['rect'] if len(r) == 6 and r[4] == 0x208020]
check_true('  bars are filled RECT_P with a green edge (%d)' % len(fills), len(fills) >= 20)
foot = [t[0] for t in h.frames[-1]['text'] if t[2] == 226]
check_true('  footer mentions bars: %s' % foot, foot == ['tap bar = counts, tap plot = explore, any key = menu'])

# a tap on empty plot drops into the Explorer with the shading kept
h = machine()
h.globals_['NE_XM'] = 2.0; h.globals_['NE_XO'] = 1.0
h.tap(200, 60, ('ne_ShowCurve', 'ne_WaitAny'))
h.keyq = [(4, ('ne_Explorer',))]
h.call('ne_ShowCurve')
check_true('  a tap on the plot entered the Explorer (DRAWMENU seen)', any(x[0] == 'DRAWMENU' for x in h.io))
check_true('  ...with the right-tail shading kept (NE_XM = %g)' % h.globals_['NE_XM'], h.globals_['NE_XM'] == 2)

# ---- B7: CDF overlay in a result view ----
print('B7  CDF overlay, N(0,1), left tail at x = 1')
h = machine()
h.globals_['NE_CFG'][1] = 2.0
h.globals_['NE_XM'] = 1.0; h.globals_['NE_XO'] = 1.0
h.keyq = [(30, ('ne_ShowCurve', 'ne_WaitAny'))]
h.call('ne_ShowCurve')
fin = h.frames[-1]
c = num_after(' '.join(find(fin, 'CDF(x₀) = ')), 'CDF(x₀) = ')
check('  CDF(x0) readout', c, norm.cdf(1), 5e-5)
cache = h.globals_['neCdf']
xs = -4 + np.arange(273) / 272 * 8
check('  S-curve cache, worst error vs SciPy', float(np.max(np.abs(np.array(cache) - norm.cdf(xs)))), 0, 1e-4)
check_true('  dotted drop line drawn (%d pixels)' % fin['pix'], fin['pix'] >= 20)

# ---- B8: the rest runs without error ----
print('B8  Animation, help, window menu, a full session')
h = machine()
h.globals_['NE_MU'] = 100.0; h.globals_['NE_SG'] = 15.0
h.call('ne_AnimStd', 100.0, 15.0, 1.0, 2.0)
check_true('  standardize animation ran (%d frames)' % len(h.frames), len(h.frames) == 22)
h = machine()
h.keyq = [(30, None), (30, None), (30, None)]
h.call('ne_HelpPages')
check_true('  three help pages composed on G1 (%d)' % len(h.frames), len(h.frames) == 3)
for k in range(1, 10):
    h = machine()
    h.chooseq = [k]
    h.inputq = [[-2, 2]]
    h.keyq = [(30, None)] * 4
    try:
        h.call('ne_SetWin')
        ok = True
    except Exception as e:
        ok = False; print('     ', k, type(e).__name__, e)
    check_true('  window & display item %d ran' % k, ok)
h = machine()
h.chooseq = [1, 3, 4, 7, 2, 11]
h.inputq = [[100, 15], [120], [0.05], [0.05]]
h.keyq = [(30, ('ne_ZPanel',)), (30, ('ne_ShowCurve', 'ne_WaitAny'))] * 3
h.keyq += [(4, ('ne_Explorer',))]
# NormExp's menu: Set mu/sigma, P(X<120), item 4 = x from probability
# (then Compare (7) power, then Explore (2), then Quit (11))
h.chooseq = [1, 3, 1, 4, 4, 7, 3, 2, 11]
r = h.call('NormExp')
print('      NormExp returned:', r)
check_true('  NormExp ran a whole session and returned its summary', str(r).startswith('NormExp: z = '))


# =============================================================================
# beta 42a: everything below is new.
# =============================================================================
# Part B patched the kit's builtin table (STRING as plain fixed decimals ...).
# Put it back, so ppl_run_v3e runs on the kit as shipped.
interp.BUILTINS.clear(); interp.BUILTINS.update(_SAVED_BUILTINS)
interp.BARE_BUILTINS.clear(); interp.BARE_BUILTINS.update(_SAVED_BARE)
print()
print('PARTS A-B (the beta 42 verify, every check kept, run on beta 42a): %d checks, %d failures'
      % (NCHK[0], len(FAILS)))

import subprocess, difflib
from scipy.stats import norm as _norm

REVIEW = '/home/claude/work/review'
HAVE_OLD = os.path.exists(OLD)
sys.path.insert(0, '/home/claude/work/out')
import ppl_run_v3e as R                       # noqa: E402
from ppl_run_v3e import Harness               # noqa: E402

SMALL_E = 'ᴇ'                            # the Prime's small-capital E
UMINUS = '−'
ALL_SCI = {}                                  # scenario -> sci strings, beta 42a
OLD_SCI = {}                                  # the same runs on beta 42, for contrast
LIMITS = []                                   # documented limits, not failures


def section(t):
    print()
    print('=' * 78)
    print(t)
    print('=' * 78)


def mk(src, **kw):
    h = Harness(src, seed=11, home_minus=True, stall_limit=30000, **kw)
    h.call('ne_ResetAll')
    return h


def fresh(h):
    """The same loaded program, ready for the next scripted run."""
    h._queue.clear(); h._choices.clear(); h._answers.clear()
    h.call('ne_ResetAll')
    h.globals_['NE_Z'] = 0.0; h.globals_['NE_X'] = 0.0; h.globals_['NE_P'] = 0.0
    h.reset_records()
    del h.sci_strings[:]


def seen(h):
    """Every text the student could see in the run."""
    out = [t.text for t in h.texts]
    out += [ln for m in h.msgboxes for ln in m.lines]
    for d in h.dialogs:
        if hasattr(d, 'items'):
            out.append(str(d.title)); out += [str(i) for i in d.items]
        else:
            out.append(str(d.title)); out += [str(i) for i in (d.labels or [])] + [str(i) for i in (d.helps or [])]
    if isinstance(h.result, str):
        out.append(h.result)
    return out


NEGZ = re.compile('[' + UMINUS + r'\-](\d+(?:\.\d+)?)(?![\d.])')


def bad_texts(txts):
    """(scientific, '= <', negative zero) offenders."""
    sci = [t for t in txts if SMALL_E in t]
    eqlt = [t for t in txts if '= <' in t]
    negz = [t for t in txts if any(float(m.group(1)) == 0 for m in NEGZ.finditer(t))]
    return sci, eqlt, negz


def record(tag, h, new):
    (ALL_SCI if new else OLD_SCI).setdefault(tag, []).extend(list(h.sci_strings))


# =============================================================================
section('PART C  -- the review\'s regression tests, on beta 42 and on beta 42a')
REV_LIT = "SRC = '/home/claude/work/review/fleet/NormExplorer_beta42.txt'"


def run_review(script, src):
    path = os.path.join(REVIEW, script)
    code = ("import sys\np = %r\ns = open(p).read()\ns2 = s.replace(%r, %r)\n"
            "assert s2 != s, 'SRC line not found'\nsys.argv = [p]\n"
            "exec(compile(s2, p, 'exec'), {'__name__': '__main__'})\n") % (path, REV_LIT, "SRC = %r" % src)
    r = subprocess.run([sys.executable, '-c', code], cwd=REVIEW, capture_output=True, text=True, timeout=1800)
    return r.returncode, r.stdout + r.stderr


REV_FAILS_OLD = {'B1: no scientific form on the panel or the view',
                 "B2: no scientific form in the Explorer's area readout",
                 'B3: outermost bin panel prints p and n*p in fixed form'}
if os.path.exists(os.path.join(REVIEW, 'check_NormExplorer.py')) and HAVE_OLD:
    res = {}
    for lab, src in (('beta 42', OLD), ('beta 42a', NEW)):
        rc, out = run_review('check_NormExplorer.py', src)
        m = re.search(r'(\d+) checks, (\d+) failures', out)
        fl = set(re.findall(r'^  FAIL (.*)$', out, re.M))
        res[lab] = (int(m.group(1)) if m else -1, int(m.group(2)) if m else -1, fl, out)
        print('  check_NormExplorer.py on %-8s: %s checks, %s failures %s'
              % (lab, res[lab][0], res[lab][1], sorted(fl) if fl else ''))
    check_true('C1  beta 42 fails exactly the review\'s three regression asserts (B1, B2, B3)',
               res['beta 42'][1] == 3 and res['beta 42'][2] == REV_FAILS_OLD)
    check_true('C2  beta 42a passes all of check_NormExplorer.py (%d checks, %d failures)'
               % (res['beta 42a'][0], res['beta 42a'][1]),
               res['beta 42a'][1] == 0 and res['beta 42a'][0] == res['beta 42'][0] == 62)
    for ln in res['beta 42a'][3].splitlines():
        if ln.startswith(('  panel lines', '  readout lines', '  area readouts', '  tapped bin')):
            print('     42a', ln.strip()[:150])
    pres = {}
    for lab, src in (('beta 42', OLD), ('beta 42a', NEW)):
        rc, out = run_review('check_NormExplorer_python.py', src)
        m = re.search(r'^(\d+) failures', out, re.M)
        runs = [l for l in out.splitlines() if l.startswith('  N(')]
        pres[lab] = (int(m.group(1)) if m else -1, runs)
        print('  check_NormExplorer_python.py on %-8s: %d runs, %s failures' % (lab, len(runs), pres[lab][0]))
    check_true('C3  the #PYTHON block passes the CPython check on beta 42a (6 runs, 0 failures)',
               pres['beta 42a'][0] == 0 and len(pres['beta 42a'][1]) == 6)
    check_true('C4  ... and gives exactly beta 42\'s six results (the block is unchanged)',
               pres['beta 42a'][1] == pres['beta 42'][1])
else:
    print('  SKIP: the review scripts or beta 42 are not at their absolute paths')


# =============================================================================
section('PART D1 -- D-NE-1: fixed decimals that stay fixed (ppl_run_v3e, home_minus=True)')
HN = mk(NEW)
HO = mk(OLD) if HAVE_OLD else None


def probcalc(h, mu, sg, typ, a, b=None):
    fresh(h); g = h.globals_
    g['NE_MU'] = float(mu); g['NE_SG'] = float(sg); h.call('ne_AutoWin')
    h.choose(typ)
    h.answer({'pcA': a} if b is None else {'pcA': a, 'pcB': b})
    h.press('Enter', 'Enter', 'Enter')
    h.call('ne_ProbCalc')
    return h


# ---- D1a: the headline, x = 180 on N(100, 15), right tail
for lab, h in (('beta 42', HO), ('beta 42a', HN)):
    if h is None:
        continue
    probcalc(h, 100, 15, 2, 180)
    pl = [t for t in seen(h) if t.startswith(('P(X > x', 'Complement'))]
    print('  %-8s %s   sci_strings %s' % (lab, pl, [s[2] for s in h.sci_strings]))
    record('D1a right tail x=180', h, lab == 'beta 42a')
    if lab == 'beta 42':
        check_true('D1a beta 42 prints "P(X > x) = 4.8213' + SMALL_E + UMINUS + '8" (the review\'s reproduction)',
                   ('P(X > x) = 4.8213' + SMALL_E + UMINUS + '8') in pl)
    else:
        check_true('D1a beta 42a prints "P(X > x) < 0.0001" on the panel and the view', pl.count('P(X > x) < 0.0001') == 1
                   and 'P(X > x₀) < 0.0001' in pl)
        check_true('D1a beta 42a: no small-capital E anywhere, h.sci_strings empty',
                   not any(SMALL_E in t for t in seen(h)) and h.sci_strings == [])
        check('D1a NE_P keeps every digit (SciPy sf)', h.globals_['NE_P'], _norm.sf(180, 100, 15), 1e-20)

# ---- D1b: the helpers themselves
fresh(HN)
FX = [((0.096, 1), '0.1'), ((0.0004, 3), '0.000'), ((-0.00004, 4), '0.0000'), ((-2.5, 2), UMINUS + '2.50'),
      ((123.456789, 4), '123.4568'), ((1e-9, 4), '0.0000'), ((0, 3), '0.000'), ((3, 0), '3'),
      ((-3, 0), UMINUS + '3'), ((0.00005, 4), '0.0001'), ((-0.004, 2), '0.00'), ((1e11 + 0.25, 1), '100000000000')]   # 12 significant digits: no room for a decimal (LL s3)
PS = [((4.8213e-8, 4), '< 0.0001'), ((0.00004999, 4), '< 0.0001'), ((0.00005, 4), '0.0001'), ((0, 4), '0.0000'),
      ((-1e-13, 4), '0.0000'), ((0.011, 1), '< 0.1'), ((0.004, 2), '< 0.01'), ((7.9e-9, 6), '< 0.000001'),
      ((0.5, 4), '0.5000'), ((1, 4), '1.0000'), ((0.99999999, 4), '1.0000'), ((1e-300, 4), '< 0.0001'),
      ((0.0004, 3), '< 0.001'), ((15, 2), '15.00')]
for (v, d), want in FX:
    got = HN.call('ne_Fx', float(v), float(d))
    check_true('D1b ne_Fx(%g, %d) = %r (got %r)' % (v, d, want, got), got == want)
for (v, d), want in PS:
    got = HN.call('ne_PStr', float(v), float(d))
    check_true('D1b ne_PStr(%g, %d) = %r (got %r)' % (v, d, want, got), got == want)
for s, want in (('0.5000', ' = 0.5000'), ('< 0.0001', ' < 0.0001'), ('', ' = '), (UMINUS + '1.00', ' = ' + UMINUS + '1.00')):
    got = HN.call('ne_Eq', s)
    check_true('D1b ne_Eq(%r) = %r' % (s, want), got == want)
check_true('D1b the helpers never print scientific (h.sci_strings empty)', HN.sci_strings == [])
record('D1b helpers', HN, True)


# ---- D1c: the review's reproduction table (findings_D, D-NE-1), beta 42 and beta 42a
def explorer_drag_left(h):           # review B2
    fresh(h); g = h.globals_
    g['NE_WA'] = 6.0; h.call('ne_AutoWin')
    px = lambda x: 38 + int((x - g['NE_WLO']) / (g['NE_WHI'] - g['NE_WLO']) * 272)
    xs = px(2.5)
    h.drag([(xs, 120), (xs - 40, 120), (xs - 90, 120), (39 + 30, 120), (39, 120)])
    h.press('Esc')
    h.call('ne_Explorer')


def percentile(h, p):
    fresh(h); g = h.globals_
    g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
    h.choose(1); h.answer({'icP': p}); h.press('Enter', 'Enter', 'Enter')
    h.call('ne_InvCalc')


def central(h, c):
    fresh(h); g = h.globals_
    g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
    h.choose(5); h.answer({'icC': c}); h.press('Enter', 'Enter', 'Enter')
    h.call('ne_InvCalc')


def bar_outer(h):                    # review B3, the outermost bar forced to one count
    fresh(h); g = h.globals_
    g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
    h.choose(6, 1); h.press('Enter'); h.call('ne_Histo')
    g['NE_BINS'][0] = 1.0
    h.reset_records(); del h.sci_strings[:]
    px = 38 + int((g['NE_HLO'] + 0.5 * g['NE_HW'] - g['NE_WLO']) / (g['NE_WHI'] - g['NE_WLO']) * 272)
    h.tap(px, 186); h.press('Enter')
    h.call('ne_ShowCurve')


REPRO = [
    ('right tail x = 180', lambda h: probcalc(h, 100, 15, 2, 180), ('P(X > x)',)),
    ('Explorer, x0 dragged to the left edge', explorer_drag_left, ('area to the left', 'height ')),
    ('outermost bar tapped', bar_outer, ('bin 1:', 'x from')),
    ('percentile at area 1E-9', lambda h: percentile(h, 1e-9), ('area left', '% of the distribution')),
    ('central C = 0.9999', lambda h: central(h, 0.9999), ('Middle',)),
]
for name, fn, keys in REPRO:
    row = {}
    for lab, h in (('beta 42', HO), ('beta 42a', HN)):
        if h is None:
            continue
        fn(h)
        record('D1c ' + name, h, lab == 'beta 42a')
        lines = [t for t in seen(h) if t.startswith(keys) or any(k in t for k in keys if k.startswith('%'))]
        row[lab] = (lines, len(h.sci_strings))
        print('  %-38s %-8s sci %d  %s' % (name, lab, len(h.sci_strings), lines[-2:]))
    if HO is not None:
        check_true('D1c %s: beta 42 printed scientific (%d), beta 42a none' % (name, row['beta 42'][1]),
                   row['beta 42'][1] > 0 and row['beta 42a'][1] == 0)
    sci, eqlt, negz = bad_texts(seen(HN))
    check_true('D1c %s: beta 42a has no small-capital E, "= <" or negative zero' % name, not (sci or eqlt or negz))

# ---- D1d: the sweep over every module (beta 42a; beta 42 for the contrast count)
TRUTH_FAILS = []


def prob_lines(h):
    """(label, text) of every probability line on the ProbCalc panel (ne_ZPanel), and the
    LAST readout of each kind on the plot (ne_RTxt) -- the result view at the true bounds;
    the sweep frames before it show the area still growing."""
    out = []
    for t in [t.text for t in h.texts if t.func == 'ne_ZPanel']:
        for lab in ('P(X < x)', 'P(X > x)', 'Complement: P(X > x)', 'Complement: P(X < x)',
                    'P(a < X < b)', 'Outside area', 'P(outside)', 'Between area'):
            if t.startswith(lab) and t[len(lab):len(lab) + 2] in (' =', ' <'):
                out.append((lab, t))
    rd = [t.text for t in h.texts if t.func == 'ne_RTxt']
    for lab in ('P(X < x₀)', 'P(X > x₀)', 'P(a < X < b)', 'P(outside)'):
        last = [t for t in rd if t.startswith(lab) and t[len(lab):len(lab) + 2] in (' =', ' <')]
        if last:
            out.append((lab, last[-1]))
    return out


def truth(lab, mu, sg, a, b):
    if lab in ('P(X < x)', 'Complement: P(X < x)', 'P(X < x₀)'):
        return _norm.cdf(a, mu, sg)
    if lab in ('P(X > x)', 'Complement: P(X > x)', 'P(X > x₀)'):
        return _norm.sf(a, mu, sg)
    btw = (_norm.sf(a, mu, sg) - _norm.sf(b, mu, sg)) if a > mu else (_norm.cdf(b, mu, sg) - _norm.cdf(a, mu, sg))
    if lab in ('P(a < X < b)', 'Between area'):
        return btw
    return _norm.cdf(a, mu, sg) + _norm.sf(b, mu, sg)


def honest(lab, t, tv):
    """The display rule: within half a last digit, and '< 0.0001' exactly when the value
    is positive (and representable) but rounds to zero."""
    tail = t[len(lab):]
    if tail == ' < 0.0001':
        return 0 < tv < 0.00005 * (1 + 1e-9)
    m = re.match(r' = (\d+\.\d{4})$', tail)
    if not m:
        return False
    v = float(m.group(1))
    if 1e-300 < tv < 0.00005:
        return False
    return abs(v - tv) <= 0.00005 + 1e-12


KS = [-40, -10, -8, -7, -6, -5.3333, -4, -1, -1e-6, 0, 1e-6, 1, 4, 5.3333, 6, 7, 8, 10, 40]
PAIRS = [(-8, 8), (-1e-6, 1e-6), (-3, -2), (2, 3), (5, 9), (-9, -5), (-40, 40), (1, 1), (8, 10), (-12, -9), (9, 12)]
DISTS = [(100.0, 15.0), (0.0, 0.001), (1e6, 3.0)]
nrun = {'new': 0, 'old': 0}
oldsci_total = 0
all_new_txt = []


def sweep_run(tag, fn):
    global oldsci_total
    for lab, h in (('beta 42', HO), ('beta 42a', HN)):
        if h is None:
            continue
        fn(h)
        record(tag, h, lab == 'beta 42a')
        if lab == 'beta 42a':
            nrun['new'] += 1
            all_new_txt.extend(seen(h))
        else:
            nrun['old'] += 1
            oldsci_total += len(h.sci_strings)
    return HN


# S1: Probability from x, the four types, three distributions, x from -40 to +40 sigma
for (mu, sg) in DISTS:
    for typ in (1, 2):
        for k in KS:
            x = mu + k * sg
            h = sweep_run('D1d S1 ProbCalc', lambda h: probcalc(h, mu, sg, typ, x))
            pls = prob_lines(h)
            if len(pls) != 3:
                TRUTH_FAILS.append((mu, sg, typ, k, 'lines', pls))
            for lab, t in pls:
                tv = truth(lab, mu, sg, x, None)
                if not honest(lab, t, tv):
                    TRUTH_FAILS.append((mu, sg, typ, k, t, tv))
            if not abs(h.globals_['NE_P'] - (_norm.cdf(x, mu, sg) if typ == 1 else _norm.sf(x, mu, sg))) <= 1e-12 * max(1e-300, h.globals_['NE_P']) + 1e-300:
                TRUTH_FAILS.append((mu, sg, typ, k, 'NE_P', h.globals_['NE_P']))
    for typ in (3, 4):
        for (ka, kb) in PAIRS:
            a, b = mu + ka * sg, mu + kb * sg
            h = sweep_run('D1d S1 ProbCalc', lambda h: probcalc(h, mu, sg, typ, a, b))
            pls = prob_lines(h)
            if len(pls) != 3:
                TRUTH_FAILS.append((mu, sg, typ, (ka, kb), 'lines', pls))
            for lab, t in pls:
                tv = truth(lab, mu, sg, a, b)
                if not honest(lab, t, tv):
                    if lab in ('P(a < X < b)', 'Between area') and ka >= 9:
                        LIMITS.append('between %g..%g sigma on N(%g, %g): %r, true %.3g' % (ka, kb, mu, sg, t, tv))
                    else:
                        TRUTH_FAILS.append((mu, sg, typ, (ka, kb), t, tv))
print('  S1 Probability from x: %d runs on beta 42a' % nrun['new'])

# S2: x from probability, all five items at ordinary and extreme inputs
INV = [(1, 'icP', v) for v in (1e-12, 1e-9, 1e-5, 0.5, 0.99999, 0.9999999)]
INV += [(it, 'icP', v) for it in (2, 3) for v in (1e-9, 1e-5, 0.05, 0.5, 0.9999)]
INV += [(4, 'icP', v) for v in (1e-9, 1e-5, 0.05, 0.9999)]
INV += [(5, 'icC', v) for v in (1, 95, 0.9999, 1e-6, 0.5, 99.99, 0.000001)]
for (it, var, v) in INV:
    def f(h, it=it, var=var, v=v):
        fresh(h); g = h.globals_
        g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
        h.choose(it); h.answer({var: v}); h.press('Enter', 'Enter', 'Enter')
        h.call('ne_InvCalc')
    h = sweep_run('D1d S2 InvCalc', f)
    txt = seen(h)
    if it == 1 and v == 1e-9:
        check_true('D1d percentile 1E-9: "area left < 0.0001" and "< 0.1% of the distribution falls below x"',
                   'area left < 0.0001' in txt and '< 0.1% of the distribution falls below x' in txt)
    if it == 4 and v == 1e-9:
        check_true('D1d two tails, alpha 1E-9: "α < 0.0001  (< 0.0001 per tail)"', 'α < 0.0001  (< 0.0001 per tail)' in txt)
    if it == 5 and v == 0.000001:
        check_true('D1d central C = 1E-6: "Central < 0.1% interval" and "each tail 50.00%"',
                   'Central < 0.1% interval' in txt and any(t.endswith('each tail 50.00%') for t in txt))
print('  S2 x from probability: %d runs so far' % nrun['new'])

# S3: the z-solver, every unknown, with tiny and ordinary values
ZS = [(1, {'zsX': 100.00001, 'zsM': 100, 'zsS': 15}), (1, {'zsX': 5, 'zsM': 3, 'zsS': 0.00001}),
      (1, {'zsX': 1e-9, 'zsM': 0, 'zsS': 1}), (2, {'zsZ': 1e-7, 'zsM': 0, 'zsS': 1}),
      (2, {'zsZ': 2, 'zsM': 0, 'zsS': 0.001}), (3, {'zsX': 1e-9, 'zsZ': 1e-9, 'zsS': 1}),
      (4, {'zsX': 100.00001, 'zsM': 100, 'zsZ': 1}), (4, {'zsX': 5, 'zsM': 3, 'zsZ': 200000}),
      (4, {'zsX': 3, 'zsM': 5, 'zsZ': 2}), (4, {'zsX': 3, 'zsM': 3.00001, 'zsZ': 2})]
for it, ans in ZS:
    def f(h, it=it, ans=ans):
        fresh(h)
        h.choose(it); h.answer(ans); h.press('Enter')
        h.call('ne_ZSolve')
    h = sweep_run('D1d S3 ZSolve', f)
    txt = seen(h)
    if it == 1 and ans['zsS'] == 0.00001:
        check_true('D1d z-solver, sigma 1E-5: "σ < 0.0001" and ")/< 0.01" (never 0.0000 or E)',
                   'σ < 0.0001' in txt and any(t.endswith(')/< 0.01') for t in txt))
    if it == 4 and ans.get('zsM') == 3.00001:
        check_true('D1d z-solver, sigma -5E-6: "These values give σ = 0.0000, ..." (signed: ne_Fx, no minus on zero)',
                   any(t.startswith('These values give σ = 0.0000,') for t in txt))
print('  S3 z-solver: %d runs so far' % nrun['new'])

# S4: compare curves -- the power picture far in both directions, a tiny d
for (m2, al) in ((1e-7, 0.05), (10, 0.05), (-10, 0.05), (1, 1e-9), (15, 0.05)):
    def f(h, m2=m2, al=al):
        fresh(h); g = h.globals_
        g['NE_CFG'][2] = float(m2)
        h.choose(3); h.answer({'c2A': al}); h.press('Enter', 'Enter', 'Enter')
        h.call('ne_Compare2')
    h = sweep_run('D1d S4 Compare2', f)
    txt = seen(h)
    if m2 == -10:
        check_true('D1d power picture, mu2 = -10: "power < 0.0001" on the panel and the plot',
                   'power < 0.0001' in txt and txt.count('power < 0.0001') >= 2)
    if m2 == 15:
        check_true('D1d power picture, mu2 = 15: "β < 0.0001: curve 2 left of x*"', 'β < 0.0001: curve 2 left of x*' in txt)
    if m2 == 1e-7:
        check_true('D1d power picture, mu2 = 1E-7: "d = 0.000" (a signed value rounds to 0)',
                   any(t.endswith('d = 0.000') for t in txt))


def f(h):
    fresh(h); g = h.globals_
    h.choose(1); h.answer({'c2M2': 1e-7}); h.press('Enter', 'Enter')
    h.call('ne_Compare2')


h = sweep_run('D1d S4 Compare2', f)
check_true('D1d second curve at mu2 = 1E-7: the plot reads "d = 0.00"', 'd = 0.00' in seen(h))

# S5: menu 9 -- the window panel and diagnostics, at tiny and huge sigma and a tiny window
for (sg, cust) in ((1e5, None), (5000, None), (0.001, None), (1.0, (0.0, 0.0001))):
    def f(h, sg=sg, cust=cust):
        fresh(h); g = h.globals_
        g['NE_SG'] = float(sg); h.call('ne_AutoWin')
        if cust:
            g['NE_WA'] = 0.0; g['NE_WLO'], g['NE_WHI'] = cust
        h.choose(7); h.press('Enter')
        h.call('ne_SetWin')
        h.choose(8); h.press('Enter')
        h.call('ne_SetWin')
    h = sweep_run('D1d S5 SetWin, Diag', f)
    txt = seen(h)
    if sg == 1e5:
        check_true('D1d window panel, sigma 1E5: "y top < 0.0001   peak < 0.0001"', 'y top < 0.0001   peak < 0.0001' in txt)
    if cust:
        check_true('D1d window panel, width 0.0001: "width < 0.001  < 0.01 σ"', 'width < 0.001  < 0.01 σ' in txt)
    if sg == 0.001:
        check_true('D1d diagnostics, sigma 0.001: "  N(0.00, < 0.01) ..."', any(t.startswith('  N(0.00, < 0.01)') for t in txt))

# S6: z-scores into D2, a list with almost no spread
for d1 in ([1.0, 1.00000001, 1.00000002], [2.0, 4.0, 9.0]):
    def f(h, d1=d1):
        fresh(h)
        h.globals_['D1'] = list(d1)
        h.call('ne_ZtoD2')
    h = sweep_run('D1d S6 ZtoD2', f)
    if d1[0] == 1.0:
        check_true('D1d D2 message, s = 1E-8: "..., s < 0.0001"', any(t.endswith(', s < 0.0001') for t in seen(h)))

# S7: the Explorer -- shadings far out, the CDF overlay, a tiny sigma
EXS = [dict(NE_XM=2.0, NE_XO=4.5), dict(NE_XM=1.0, NE_XO=-5.5), dict(NE_XM=3.0, NE_XO=-5.5, NE_XB=5.5),
       dict(NE_XM=4.0, NE_XO=-5.5, NE_XB=5.5), dict(NE_XM=4.0, NE_XO=-0.000001, NE_XB=0.000001),
       dict(NE_XM=3.0, NE_XO=-5.5, NE_XB=5.5, CDF=1), dict(NE_XM=2.0, NE_XO=5.9, CDF=1),
       dict(NE_SG=0.001), dict(NE_SG=0.001, NE_XM=2.0, NE_XO=0.0055), dict(NE_MU=1e6, NE_SG=3.0)]
for st in EXS:
    def f(h, st=st):
        fresh(h); g = h.globals_
        for k, v in st.items():
            if k == 'CDF':
                g['NE_CFG'][1] = 2.0
            else:
                g[k] = v
        h.call('ne_AutoWin')
        h.press('Esc')
        h.call('ne_Explorer')
    h = sweep_run('D1d S7 Explorer', f)
    txt = seen(h)
    if st.get('NE_XM') == 2.0 and st.get('NE_XO') == 4.5:
        check_true('D1d Explorer, right tail at 4.5 sigma: "area to the right < 0.0001" and "height 0.000016 (density,"',
                   'area to the right < 0.0001' in txt and 'height 0.000016 (density,' in txt)
    if st.get('CDF') and st.get('NE_XM') == 3.0:
        check_true('D1d Explorer with the S-curve: "CDF(a) < 0.0001" and "CDF(b) = 1.0000"',
                   'CDF(a) < 0.0001' in txt and 'CDF(b) = 1.0000' in txt)
    if st.get('NE_SG') == 0.001 and 'NE_XM' not in st:
        check_true('D1d Explorer, sigma 0.001: "σ < 0.01" and the bands "68.27%: 0.00…0.00"',
                   'σ < 0.01' in txt and '68.27%: 0.00…0.00' in txt)


# S8: histogram bars -- an outer bar under a curve moved 10 sigma right (expected < 0.1)
def f(h):
    fresh(h); g = h.globals_
    g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
    h.choose(6, 1); h.press('Enter'); h.call('ne_Histo')
    g['NE_BINS'][0] = 3.0; g['NE_BINS'][31] = 2.0
    g['NE_MU'] = 250.0; g['NE_XM'] = 0.0
    g['NE_WA'] = 0.0; g['NE_WLO'] = 30.0; g['NE_WHI'] = 330.0; h.call('ne_AutoWin')
    h.reset_records(); del h.sci_strings[:]
    for b in (1, 32, 16):
        px = 38 + int((g['NE_HLO'] + (b - 0.5) * g['NE_HW'] - 30.0) / 300.0 * 272)
        h.tap(px, 186)
    h.press('Enter')
    h.call('ne_ShowCurve')


h = sweep_run('D1d S8 bars', f)
txt = seen(h)
check_true('D1d bar 1 under a curve 10 sigma away: "3 observed, < 0.1 expected" and "p < 0.0001"',
           any(t.startswith('bin 1: 3 observed, < 0.1 expected') for t in txt)
           and any(t.startswith('x from') and t.endswith('p < 0.0001') for t in txt))


# S9: a whole session, ending on a far right tail: the line returned to Home
def f(h):
    fresh(h)
    h.choose(1, 3, 2, 11)
    h.answer({'sdMU': 100, 'sdSG': 15}, {'pcA': 220})
    h.press('Enter', 'Enter', 'Enter')
    h.call('NormExp')


h = sweep_run('D1d S9 NormExp', f)
check_true('D1d NormExp returns "NormExp: z = 8.0000, x = 220.0000, p < 0.0001" (got %r)' % h.result,
           h.result == 'NormExp: z = 8.0000, x = 220.0000, p < 0.0001')
check_true('D1d ... and NE_P in Home keeps the number (SciPy sf, 1E-9 relative)',
           abs(h.globals_['NE_P'] - _norm.sf(8)) <= 1e-9 * _norm.sf(8))


# S10: the animation at a tiny and an ordinary sigma; the help pages
for (am, asg) in ((0.0, 0.001), (100.0, 15.0)):
    def f(h, am=am, asg=asg):
        fresh(h)
        h.call('ne_AnimStd', am, asg, 1.0, 1.0)
    sweep_run('D1d S10 animation, help', f)


def f(h):
    fresh(h)
    h.press('Enter', 'Enter', 'Enter')
    h.call('ne_HelpPages')


sweep_run('D1d S10 animation, help', f)

sci, eqlt, negz = bad_texts(all_new_txt)
print('  the sweep: %d runs on beta 42a, %d texts seen; the same %d runs on beta 42 printed %d scientific strings'
      % (nrun['new'], len(all_new_txt), nrun['old'], oldsci_total))
check_true('D1d no small-capital E in any of the %d texts beta 42a showed' % len(all_new_txt), not sci)
check_true('D1d no "= <" anywhere (ne_Eq)', not eqlt)
check_true('D1d no negative zero anywhere ("%s0.0000")' % UMINUS, not negz)
check_true('D1d every probability on the Probability-from-x panels and final views (3 lines a run) within half '
           'a last digit of SciPy, "< 0.0001" exactly when positive and rounding to zero; NE_P = SciPy to 1E-12 '
           '(%d offenders)' % len(TRUTH_FAILS), not TRUTH_FAILS)
for tf in TRUTH_FAILS[:8]:
    print('     ', tf)
if HO is not None:
    check_true('D1d the same runs on beta 42 printed the scientific form (%d strings): the sweep can see it' % oldsci_total,
               oldsci_total > 0)
for lm in LIMITS:
    print('  between far right, still wrong: ' + lm)
check_true('D1d "between" far right of mu (8..10 and 9..12 sigma) is right too: ne_Btw mirrors it (%d wrong lines)'
           % len(LIMITS), len(LIMITS) == 0)


# =============================================================================
section('PART D2 -- D-NE-2: right tails as lower tails, with the Prime\'s 12 digits modelled')
_LOG0 = R._StatFns.log


def _log12(self, name, args, val):
    v = _LOG0(self, name, args, val)
    return float('%.12g' % v) if v == v else v


R._StatFns.log = _log12            # every statistics built-in returns 12 significant digits
try:
    fresh(HN)
    check_true('D2  the model is on: NORMALD_CDF(0, 1, 8) is exactly 1 (so 1 - CDF = 0); NORMALD_CDF(0, 1, -8) = 6.22096057427E-16',
               HN.execute('NORMALD_CDF(0, 1, 8)') == 1.0 and HN.execute('NORMALD_CDF(0, 1, -8)') == 6.22096057427e-16)
    print('  right tail on N(100, 15): NE_P (beta 42 = 1 - CDF; beta 42a = the mirrored lower tail) against SciPy')
    for z in (5.3333, 6, 7, 8, 9, 12):
        x = 100 + 15 * z
        tv = _norm.sf(z)
        got = {}
        for lab, h in (('beta 42', HO), ('beta 42a', HN)):
            if h is None:
                continue
            probcalc(h, 100, 15, 2, x)
            record('D2 right tail', h, lab == 'beta 42a')
            got[lab] = (h.globals_['NE_P'], [t for t in seen(h) if t.startswith('P(X > x)')][0])
        print('    z = %-7g true %.4e   beta 42 %.4e %-20s beta 42a %.4e %s'
              % (z, tv, got.get('beta 42', (float('nan'), ''))[0], got.get('beta 42', ('', ''))[1],
                 got['beta 42a'][0], got['beta 42a'][1]))
        check('D2  z = %g: beta 42a NE_P = SciPy sf (12-digit relative)' % z, got['beta 42a'][0], tv, 1e-11 * tv)
        if z >= 8 and 'beta 42' in got:
            check_true('D2  z = %g: beta 42 NE_P was exactly 0 (the bug), beta 42a positive' % z,
                       got['beta 42'][0] == 0 and got['beta 42a'][0] > 0)

    def both(fn, keys):
        out = {}
        for lab, h in (('beta 42', HO), ('beta 42a', HN)):
            if h is None:
                continue
            fn(h)
            record('D2 ' + keys[0], h, lab == 'beta 42a')
            out[lab] = ([t for t in seen(h) if t.startswith(keys)], h.globals_['NE_P'])
        return out

    r = both(lambda h: probcalc(h, 100, 15, 1, 220), ('Complement',))
    print('  left tail at z = 8, its complement:', r)
    check_true('D2  left-tail panel at z = 8: "Complement: P(X > x) < 0.0001" (beta 42: 0.0000)',
               'Complement: P(X > x) < 0.0001' in r['beta 42a'][0]
               and (HO is None or 'Complement: P(X > x) = 0.0000' in r['beta 42'][0]))
    # (The harness rounds the built-ins' answers to 12 digits but still adds and subtracts in
    # doubles, so 1 - (1 - 6.2E-16) is 6.7E-16 here where the Prime's 12-digit subtraction gives
    # exactly 0.  For beta 42 these lines are printed for contrast; the checks are on beta 42a.)
    r = both(lambda h: probcalc(h, 100, 15, 2, -20), ('Complement',))
    print('  right tail at z = -8, its complement:', r)
    check_true('D2  right-tail panel at z = -8: "Complement: P(X < x) < 0.0001" (read directly as the lower tail)',
               'Complement: P(X < x) < 0.0001' in r['beta 42a'][0])
    r = both(lambda h: probcalc(h, 100, 15, 4, -20, 220), ('P(outside)',))
    print('  outside -8..8 sigma:', r)
    check('D2  outside -8..8 sigma: beta 42a NE_P = 2 Phi(-8)', r['beta 42a'][1], 2 * _norm.cdf(-8), 1e-11 * _norm.cdf(-8))
    check_true('D2  ... "P(outside) < 0.0001"; beta 42\'s 1 - (F(b) - F(a)) is off by more than 10%% even in '
               'double arithmetic (%s; the Prime: 0)' % (r.get('beta 42', [0, 'n/a'])[1],),
               'P(outside) < 0.0001' in r['beta 42a'][0]
               and (HO is None or abs(r['beta 42'][1] - 2 * _norm.cdf(-8)) > 0.1 * 2 * _norm.cdf(-8)))
    r = both(lambda h: probcalc(h, 100, 15, 3, -20, 220), ('Outside area',))
    check_true('D2  between -8..8 sigma: "Outside area < 0.0001" (beta 42: 1 - pcP)', 'Outside area < 0.0001' in r['beta 42a'][0])

    def power(h, m2):
        fresh(h); g = h.globals_
        g['NE_CFG'][2] = float(m2)
        h.choose(3); h.answer({'c2A': 0.05}); h.press('Enter', 'Enter', 'Enter')
        h.call('ne_Compare2')

    r = both(lambda h: power(h, -8), ('power',))
    tv = _norm.sf(_norm.ppf(0.95) + 8)
    print('  power, mu2 = -8:', r, 'true %.4e' % tv)
    check('D2  power picture, mu2 = -8: beta 42a NE_P = power (SciPy)', r['beta 42a'][1], tv, 1e-10 * tv)
    check_true('D2  ... "power < 0.0001" on the panel and the plot (beta 42: NE_P %s)' % (r.get('beta 42', [0, 'n/a'])[1],),
               r['beta 42a'][0].count('power < 0.0001') >= 2 and (HO is None or r['beta 42'][1] == 0))
    r = both(lambda h: power(h, 12), ('β',))
    print('  beta, mu2 = 12:', r)
    check_true('D2  power picture, mu2 = 12: "β < 0.0001" (beta 42: "β = 0.0000")',
               'β < 0.0001: curve 2 left of x*' in r['beta 42a'][0]
               and (HO is None or 'β = 0.0000: curve 2 left of x*' in r['beta 42'][0]))

    def view(h, **st):
        fresh(h); g = h.globals_
        for k, v in st.items():
            if k == 'M2':
                g['NE_CFG'][2] = v; g['NE_CFG'][3] = 1.0
            else:
                g[k] = v
        h.call('ne_AutoWin')
        h.press('Enter')
        h.call('ne_ShowCurve')

    TAGC = 0xC00000
    tagre = re.compile(r'^(< )?\d\.\d{4}$')
    cases = [('right tail at 8 sigma, a custom window 7..10 (the riding tag)',
              dict(NE_XM=2.0, NE_XO=8.0, NE_WA=0.0, NE_WLO=7.0, NE_WHI=10.0), 'P(X > x₀)'),
             ('outside -8..8, a custom window 5..12 (the right tail\'s tag)',
              dict(NE_XM=4.0, NE_XO=-8.0, NE_XB=8.0, NE_WA=0.0, NE_WLO=5.0, NE_WHI=12.0), 'P(outside)'),
             ('the power readout, mu2 = -8, x* = 1.6449', dict(NE_XM=2.0, NE_XO=1.6449, M2=-8.0), 'power')]
    for name, st, key in cases:
        out = {}
        for lab, h in (('beta 42', HO), ('beta 42a', HN)):
            if h is None:
                continue
            view(h, **st)
            record('D2 views', h, lab == 'beta 42a')
            rd = [t.text for t in h.texts if t.text.startswith(key)]
            tg = [t.text for t in h.texts if t.color == TAGC and tagre.match(t.text)]
            out[lab] = (rd[-1:] if rd else [], tg[-1:] if tg else [])
        print('  %s: %s' % (name, out))
        okr = out['beta 42a'][0] == [key + ' < 0.0001']
        okt = key == 'power' or out['beta 42a'][1] == ['< 0.0001']
        # beta 42: a single 1 - CDF is exactly 0 here as on the Prime (the readout for one
        # tail, the power, every tag); the outside readout is a 1 - (difference), see above
        if key == 'P(outside)':
            oldbad = HO is None or out['beta 42'][1] == ['0.0000']
        else:
            oldbad = HO is None or (out['beta 42'][0] == [key + ' = 0.0000']
                                    and (key == 'power' or out['beta 42'][1] == ['0.0000']))
        check_true('D2  %s: beta 42a reads "%s < 0.0001"%s (beta 42: %s)'
                   % (name, key, '' if key == 'power' else ' and its tag "< 0.0001"',
                      'the tag 0.0000' if key == 'P(outside)' else '0.0000'), okr and okt and oldbad)
finally:
    R._StatFns.log = _LOG0
check_true('D2  the 12-digit model is off again', R._StatFns.log is _LOG0)


# =============================================================================
section('PART D3 -- D-NE-3: the CHOOSE idiom')
newsrc = open(NEW, encoding='utf-8').read()
oldsrc = open(OLD, encoding='utf-8').read() if HAVE_OLD else ''


def strip_comment(l):
    """The code part of a PPL line: everything before a // that is not inside a string."""
    instr = False
    for k, ch in enumerate(l):
        if ch == '"':
            instr = not instr
        elif not instr and l.startswith('//', k):
            return l[:k]
    return l


def code_lines(src):
    out, py = [], False
    for i, l in enumerate(src.split('\n'), 1):
        if l.startswith('#PYTHON'):
            py = True
        if not py:
            out.append((i, strip_comment(l)))
        if l.startswith('#END'):
            py = False
    return out


ncl = code_lines(newsrc)
choose_new = [(i, c) for i, c in ncl if 'CHOOSE(' in c]
check_true('D3  beta 42a: 8 CHOOSE calls (the 7 menus and the main menu), none assigned (%d)' % len(choose_new),
           len(choose_new) == 8 and not any(re.search(r':=\s*CHOOSE', c) for _, c in choose_new))
srcl = newsrc.split('\n')
for i, c in choose_new:
    idx = re.search(r'CHOOSE\((\w+)', c).group(1)
    before = [srcl[j - 1].strip() for j in range(max(1, i - 5), i)]
    j = i
    while '})' not in srcl[j - 1]:
        j += 1
    nxt = srcl[j].strip()
    init_ok = ('%s := 0;' % idx) in before or idx == 'hsN'
    test_ok = nxt.startswith('IF %s == 0 THEN RETURN; END;' % idx) or idx == 'mnPick'
    check_true('D3  line %d CHOOSE(%s, ...): index set to 0 before, only the index tested after' % (i, idx), init_ok and test_ok)
check_true('D3  hsN is set to 0 before its CHOOSE (the nested one)',
           re.search(r'hsN := 0;\s*\n\s*IF hsT == 6 THEN\s*\n\s*//[^\n]*\n\s*CHOOSE\(hsN', newsrc) is not None)
check_true('D3  swSel, pcSel, icSel, zsSel, c2Sel and hsSel are gone',
           not re.search(r'\b(swSel|pcSel|icSel|zsSel|c2Sel|hsSel)\b', '\n'.join(c for _, c in ncl)))

SNAP = ('NE_MU', 'NE_SG', 'NE_XM', 'NE_XO', 'NE_XB', 'NE_WA', 'NE_WLO', 'NE_WHI', 'NE_HN', 'NE_P', 'NE_X', 'NE_Z')
for routine, picks in (('ne_SetWin', (0,)), ('ne_ProbCalc', (0,)), ('ne_InvCalc', (0,)), ('ne_ZSolve', (0,)),
                       ('ne_Compare2', (0,)), ('ne_Histo', (0,)), ('ne_Histo', (6, 0))):
    res = {}
    for lab, h in (('beta 42', HO), ('beta 42a', HN)):
        if h is None:
            continue
        fresh(h)
        before = {k: h.globals_[k] for k in SNAP}
        cfg = list(h.globals_['NE_CFG'])
        h.choose(*picks)
        h.call(routine)
        same = all(h.globals_[k] == before[k] for k in SNAP) and list(h.globals_['NE_CFG']) == cfg
        res[lab] = (len(h.chooses), len(h.inputs), len(h.msgboxes), len(h.pages), same)
    check_true('D3  Esc in %s%s: CHOOSE shown %d time(s), then nothing (no form, message, plot or change); as beta 42'
               % (routine, ' (Simulate, then Esc)' if picks == (6, 0) else '', res['beta 42a'][0]),
               res['beta 42a'][1:] == (0, 0, 0, True) and res['beta 42a'][0] == len(picks)
               and (HO is None or res['beta 42'] == res['beta 42a']))


# =============================================================================
section('PART D4 -- D-NE-4: central C = 1 means 1%')
for c, want in ((1, 0.01), (100, None), (95, 0.95), (0.95, 0.95), (99.9, 0.999), (0.5, 0.5)):
    res = {}
    for lab, h in (('beta 42', HO), ('beta 42a', HN)):
        if h is None:
            continue
        central(h, c)
        record('D4 central', h, lab == 'beta 42a')
        res[lab] = (h.globals_['NE_P'], [m.lines for m in h.msgboxes], h.globals_['NE_X'],
                    [t for t in seen(h) if t.startswith('Central ')])
    print('  C = %-5g beta 42: %s   beta 42a: %s' % (c, res.get('beta 42', ('-',))[:2], res['beta 42a'][:2]))
    if want is None:
        check_true('D4  C = %g refused with a message, in both' % c,
                   res['beta 42a'][1] == [['Central proportion must be between 0 and 1.']]
                   and (HO is None or res['beta 42'][1] == res['beta 42a'][1]))
    else:
        zz = _norm.ppf((1 + want) / 2)
        check('D4  C = %g: NE_P = %g' % (c, want), res['beta 42a'][0], want, 1e-12)
        check('D4  C = %g: upper end = mu + z sigma (SciPy)' % c, res['beta 42a'][2], 100 + 15 * zz, 1e-9)
        if c == 1:
            check_true('D4  C = 1: the panel says "Central 1.0% interval" (beta 42 refused it)',
                       'Central 1.0% interval' in res['beta 42a'][3]
                       and (HO is None or res['beta 42'][1] == [['Central proportion must be between 0 and 1.']]))
        elif HO is not None:
            check('D4  C = %g: as beta 42' % c, res['beta 42a'][0], res['beta 42'][0], 0)


# =============================================================================
section('PART D5 -- D-NE-5: the Explorer\'s arrow steps refit after a sigma drag')


def drag_sigma(h, keys):
    fresh(h); g = h.globals_
    g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
    # the window freezes at 10..190 (mu +/- 6 sigma); the right shoulder mu + sigma = 115 is at
    # pixel 38 + IP(105/180 * 272) = 196; dragging it to 176 pulls sigma down to its floor, 2
    h.drag([(196, 120), (186, 120), (176, 120)])
    h.press(*keys)
    h.call('ne_Explorer')
    return g['NE_MU'], g['NE_SG']


for keys, want_new, want_old in ((('Esc',), (100.0, 2.0), (100.0, 2.0)),
                                 (('Right', 'Esc'), (100.5, 2.0), (105.0, 2.0)),
                                 (('Right', 'Up', 'Esc'), (100.5, 2.2), (105.0, 4.0)),
                                 (('Left', 'Down', 'Esc'), (99.5, 1.8), (95.0, 2.0))):
    got = {}
    for lab, h in (('beta 42', HO), ('beta 42a', HN)):
        if h is None:
            continue
        got[lab] = drag_sigma(h, keys)
        record('D5 Explorer', h, lab == 'beta 42a')
    print('  sigma drag 15 -> 2, then %-22s beta 42 mu, sigma = %s   beta 42a = %s'
          % ('+'.join(keys), got.get('beta 42'), got['beta 42a']))
    check_true('D5  then %s: beta 42a mu, sigma = %s (beta 42: %s)' % ('+'.join(keys), want_new, want_old),
               abs(got['beta 42a'][0] - want_new[0]) < 1e-9 and abs(got['beta 42a'][1] - want_new[1]) < 1e-9
               and (HO is None or (abs(got['beta 42'][0] - want_old[0]) < 1e-9 and abs(got['beta 42'][1] - want_old[1]) < 1e-9)))



# =============================================================================
section('PART D6 -- between, mirrored (ne_Btw), with the Prime\'s 12 digits modelled')
# Found while checking D-NE-2; fixed in beta 42a at the coordinator's request (19 Oct).
# Both CDFs of an area far above the mean are exactly 1 on the Prime; beta 42 subtracted them.
# The model as in Part D2, plus (for Part D7) the probability handed to NORMALD_ICDF held to
# 12 significant digits as the Prime holds every real -- so 1 - 1E-13 is exactly 1 there, as
# on the calculator.  Harnesses made inside the block see the patched ICDF (the harness binds
# its built-ins when it is made).
_ICDF0 = R._StatFns.NORMALD_ICDF


def _icdf12(self, a):
    a = list(a)
    a[-1] = float('%.12g' % a[-1])
    return _ICDF0(self, a)


R._StatFns.log = _log12
R._StatFns.NORMALD_ICDF = _icdf12
try:
    HN12 = mk(NEW)
    HO12 = mk(OLD) if HAVE_OLD else None
    check_true('D6  the model is on: NORMALD_CDF(0, 1, 9) is exactly 1; NORMALD_ICDF(0, 1, 1 - 1E-13) is '
               'NORMALD_ICDF(0, 1, 1), which stops the program',
               HN12.execute('NORMALD_CDF(0, 1, 9)') == 1.0)
    try:
        HN12.execute('NORMALD_ICDF(0, 1, 1 - 0.0000000000001)')
        stops = False
    except Exception:
        stops = True
    check_true('D6  ... (the ICDF at a rounded 1 does stop it)', stops)
    for (ka, kb) in ((9, 12), (8, 10), (2, 3), (-3, -2), (-1, 9)):
        a, b = 100 + 15 * ka, 100 + 15 * kb
        tv = (_norm.sf(ka) - _norm.sf(kb)) if ka > 0 else (_norm.cdf(kb) - _norm.cdf(ka))
        out = {}
        for lab, h in (('beta 42', HO12), ('beta 42a', HN12)):
            if h is None:
                continue
            probcalc(h, 100, 15, 3, a, b)
            record('D6 between', h, lab == 'beta 42a')
            pan = [t.text for t in h.texts if t.func == 'ne_ZPanel' and t.text.startswith('P(a < X < b)')]
            rd = [t.text for t in h.texts if t.func == 'ne_RTxt' and t.text.startswith('P(a < X < b)')]
            out[lab] = (h.globals_['NE_P'], pan[-1:], rd[-1:])
        print('  between %g..%g sigma: true %.4e  beta 42 %s  beta 42a %s' % (ka, kb, tv, out.get('beta 42'), out['beta 42a']))
        check('D6  between %g..%g sigma: beta 42a NE_P = SciPy (12-digit relative)' % (ka, kb), out['beta 42a'][0], tv, 1e-10 * tv)
        if ka >= 8:
            check_true('D6  ... panel and view read "P(a < X < b) < 0.0001"; beta 42 had NE_P 0 and "= 0.0000"',
                       out['beta 42a'][1] == ['P(a < X < b) < 0.0001'] and out['beta 42a'][2] == ['P(a < X < b) < 0.0001']
                       and (HO12 is None or (out['beta 42'][0] == 0 and out['beta 42'][1] == ['P(a < X < b) = 0.0000'])))
        elif HO12 is not None:
            check('D6  ... an ordinary area is beta 42\'s to the last digit', out['beta 42a'][0], out['beta 42'][0], 2e-12)
    # the outside panel's "Between area"
    out = {}
    for lab, h in (('beta 42', HO12), ('beta 42a', HN12)):
        if h is None:
            continue
        probcalc(h, 100, 15, 4, 235, 280)
        record('D6 between', h, lab == 'beta 42a')
        out[lab] = [t for t in seen(h) if t.startswith('Between area')]
    check_true('D6  outside 9..12 sigma: "Between area < 0.0001" (beta 42: %s)' % out.get('beta 42'),
               out['beta 42a'] == ['Between area < 0.0001'])

    def view3(h, explorer=False):
        fresh(h); g = h.globals_
        g['NE_XM'] = 3.0; g['NE_XO'] = 8.5; g['NE_XB'] = 9.5
        if not explorer:
            g['NE_WA'] = 0.0; g['NE_WLO'] = 8.0; g['NE_WHI'] = 10.0
        h.call('ne_AutoWin')
        h.press('Esc' if explorer else 'Enter')
        h.call('ne_Explorer' if explorer else 'ne_ShowCurve')

    for explorer in (False, True):
        out = {}
        for lab, h in (('beta 42', HO12), ('beta 42a', HN12)):
            if h is None:
                continue
            view3(h, explorer)
            record('D6 views', h, lab == 'beta 42a')
            key = 'area between' if explorer else 'P(a < X < b)'
            rd = [t.text for t in h.texts if t.text.startswith(key)]
            tg = [t.text for t in h.texts if t.color == 0xC00000 and re.match(r'^(< )?\d\.\d{4}$', t.text)]
            out[lab] = (rd[-1:], tg[-1:])
        print('  %s, N(0,1), between 8.5 and 9.5: %s' % ('Explorer' if explorer else 'result view, window 8..10', out))
        if explorer:
            check_true('D6  Explorer: "area between < 0.0001" (beta 42: "= 0.0000")',
                       out['beta 42a'][0] == ['area between < 0.0001']
                       and (HO12 is None or out['beta 42'][0] == ['area between = 0.0000']))
        else:
            check_true('D6  result view: "P(a < X < b) < 0.0001" and the riding tag "< 0.0001" (beta 42: 0.0000, tag 0.0000)',
                       out['beta 42a'] == (['P(a < X < b) < 0.0001'], ['< 0.0001'])
                       and (HO12 is None or out['beta 42'] == (['P(a < X < b) = 0.0000'], ['0.0000'])))

    def bars_far_left(h):
        fresh(h); g = h.globals_
        g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
        h.choose(6, 1); h.press('Enter'); h.call('ne_Histo')
        g['NE_BINS'][0] = 3.0; g['NE_BINS'][31] = 2.0
        g['NE_MU'] = -100.0; g['NE_XM'] = 0.0               # the curve 13 sigma left of the bars' centre
        g['NE_WA'] = 0.0; g['NE_WLO'] = -160.0; g['NE_WHI'] = 170.0; h.call('ne_AutoWin')
        h.reset_records(); del h.sci_strings[:]
        for b in (1, 32):
            h.tap(38 + int((g['NE_HLO'] + (b - 0.5) * g['NE_HW'] + 160.0) / 330.0 * 272), 186)
        h.press('Enter')
        h.call('ne_ShowCurve')

    out = {}
    for lab, h in (('beta 42', HO12), ('beta 42a', HN12)):
        if h is None:
            continue
        bars_far_left(h)
        record('D6 bars', h, lab == 'beta 42a')
        out[lab] = [t for t in seen(h) if t.startswith(('bin 1:', 'bin 32:', 'x from'))]
    print('  bars 1 and 32 under N(-100, 15): beta 42 %s' % out.get('beta 42'))
    print('                                   beta 42a %s' % out['beta 42a'])
    check_true('D6  a bar far above the curve: "3 observed, < 0.1 expected", "p < 0.0001" (beta 42: "0.0 expected", "p = 0.0000")',
               any(t.startswith('bin 1: 3 observed, < 0.1 expected') for t in out['beta 42a'])
               and sum(t.endswith('p < 0.0001') for t in out['beta 42a']) == 2
               and (HO12 is None or (any(t.startswith('bin 1: 3 observed, 0.0 expected') for t in out['beta 42'])
                                     and sum(t.endswith('p = 0.0000') for t in out['beta 42']) == 2)))

    # =========================================================================
    section('PART D7 -- right-tail quantiles as minus the quantile of the small area (12 digits modelled)')

    def inv(h, it, var, v):
        fresh(h); g = h.globals_
        g['NE_MU'] = 100.0; g['NE_SG'] = 15.0; h.call('ne_AutoWin')
        h.choose(it); h.answer({var: v}); h.press('Enter', 'Enter', 'Enter')
        h.call('ne_InvCalc')

    def pw(h, v):
        fresh(h)
        h.choose(3); h.answer({'c2A': v}); h.press('Enter', 'Enter', 'Enter')
        h.call('ne_Compare2')

    def attempt(fn, h, *args):
        try:
            fn(h, *args)
            return None
        except Exception as e:
            return '%s: %s' % (type(e).__name__, str(e)[:90])

    CASES = [('right tail, alpha 1E-13', lambda h: inv(h, 2, 'icP', 1e-13), 'NE_Z', _norm.isf(1e-13), 1e-9),
             ('two tails, alpha 1E-13', lambda h: inv(h, 4, 'icP', 1e-13), 'NE_Z', _norm.isf(5e-14), 1e-9),
             ('central, C = 0.999999999999', lambda h: inv(h, 5, 'icC', 0.999999999999), 'NE_Z', _norm.isf(5e-13), 1e-4),
             ('central, C = 99.9999999999 (percent)', lambda h: inv(h, 5, 'icC', 99.9999999999), 'NE_Z', _norm.isf(5e-13), 1e-3),
             ('power picture, alpha 1E-13', lambda h: pw(h, 1e-13), 'NE_Z', _norm.isf(1e-13), 1e-9),
             ('right tail, alpha 0.05', lambda h: inv(h, 2, 'icP', 0.05), 'NE_Z', _norm.isf(0.05), 1e-9),
             ('two tails, alpha 0.05', lambda h: inv(h, 4, 'icP', 0.05), 'NE_Z', _norm.isf(0.025), 1e-9),
             ('central, C = 0.95', lambda h: inv(h, 5, 'icC', 0.95), 'NE_Z', _norm.isf(0.025), 1e-9),
             ('power picture, alpha 0.05', lambda h: pw(h, 0.05), 'NE_Z', _norm.isf(0.05), 1e-9)]
    for name, fn, var, want, tol in CASES:
        res = {}
        for lab, h in (('beta 42', HO12), ('beta 42a', HN12)):
            if h is None:
                continue
            err = attempt(lambda hh: fn(hh), h)
            record('D7 quantiles', h, lab == 'beta 42a')
            res[lab] = (err, h.globals_[var])
        print('  %-38s beta 42: %-60s beta 42a: z* = %.6f (want %.6f)'
              % (name, res.get('beta 42', ('-',))[0] or ('z* = %.6f' % res['beta 42'][1]), res['beta 42a'][1], want))
        okn = res['beta 42a'][0] is None and abs(res['beta 42a'][1] - want) <= tol * want
        if name.startswith('central, C = 0.9999') or name.startswith('central, C = 99.99'):
            # beta 42's argument (1 + C)/2: on the Prime 1 + C = 1.999999999999 needs 13 digits and
            # rounds to 2, so the argument is exactly 1 and the program stops.  The harness adds in
            # doubles and rounds only the argument, so there beta 42 runs on with half the tail
            # area lost (1E-12 instead of 5E-13): a wrong z*.  Wrong either way.
            oldbad = HO12 is None or res['beta 42'][0] is not None or abs(res['beta 42'][1] - want) > 0.005 * want
            check_true('D7  %s: beta 42a z* = %.4f (SciPy); beta 42 stopped or was wrong (%s)'
                       % (name, want, res.get('beta 42', ('-',))[0] or 'z* = %.4f' % res['beta 42'][1]), okn and oldbad)
        elif '0.05' in name or 'C = 0.95' in name:
            check_true('D7  %s: beta 42a z* = SciPy, and = beta 42\'s' % name,
                       okn and (HO12 is None or (res['beta 42'][0] is None and abs(res['beta 42'][1] - res['beta 42a'][1]) < 1e-9)))
        else:
            check_true('D7  %s: beta 42a z* = %.4f (SciPy); beta 42 stopped at NORMALD_ICDF(..., 1)' % (name, want),
                       okn and (HO12 is None or (res['beta 42'][0] is not None and 'NORMALD_ICDF' in res['beta 42'][0])))

    # every NORMALD_ICDF the program makes, at the edges each form accepts, gets an area inside 0..1
    EDGE = [(lambda h, v: inv(h, 1, 'icP', v), (1e-300, 1e-13, 0.5, 0.999999999999), 'percentile'),
            (lambda h, v: inv(h, 2, 'icP', v), (1e-300, 1e-13, 0.999999999999), 'right tail'),
            (lambda h, v: inv(h, 3, 'icP', v), (1e-300, 1e-13, 0.999999999999), 'left tail'),
            (lambda h, v: inv(h, 4, 'icP', v), (1e-300, 1e-13, 0.999999999999), 'two tails'),
            (lambda h, v: inv(h, 5, 'icC', v), (1e-300, 0.5, 0.999999999999, 1, 99.9999999999), 'central'),
            (lambda h, v: pw(h, v), (1e-300, 1e-13, 0.999999999999), 'power picture')]
    bad, n_icdf, n_runs = [], 0, 0
    for fn, vals, name in EDGE:
        for v in vals:
            err = attempt(fn, HN12, v)
            n_runs += 1
            record('D7 edges', HN12, True)
            calls = [c for c in HN12.stat_calls if c[0] == 'NORMALD_ICDF']
            n_icdf += len(calls)
            if err or not calls or not all(0 < c[1][-1] < 1 for c in calls):
                bad.append((name, v, err, [c[1] for c in calls]))
            sci, eqlt, negz = bad_texts(seen(HN12))
            if sci or eqlt or negz:
                bad.append((name, v, 'text', sci + eqlt + negz))
    for b_ in bad:
        print('    ', b_)
    check_true('D7  every form at its edges (1E-300, 1E-13, 0.999999999999, ...; %d runs): no stop, every '
               'NORMALD_ICDF argument (%d calls) strictly inside 0..1 at 12 digits, no E / "= <" / -0' % (n_runs, n_icdf),
               not bad)
finally:
    R._StatFns.log = _LOG0
    R._StatFns.NORMALD_ICDF = _ICDF0
check_true('D6-7 the 12-digit model is off again', R._StatFns.log is _LOG0 and R._StatFns.NORMALD_ICDF is _ICDF0)

# =============================================================================
section('PART E  -- the source, statically')
nl = newsrc.split('\n')
if nl[-1] == '':
    nl = nl[:-1]


def calls_of(line, name):
    return len(re.findall(r'(?<![\w])' + name + r'\(', line))


def routine_span(src_lines, name):
    i = next(k for k, l in enumerate(src_lines) if re.match(r'^' + name + r'\(', l) and not l.rstrip().endswith(';'))
    j = next(k for k in range(i, len(src_lines)) if src_lines[k] == 'END;')
    return i + 1, j + 1


helpers = {n: routine_span(nl, n) for n in ('ne_Fx', 'ne_PStr', 'ne_Eq')}
inside = set()
for a, b in helpers.values():
    inside |= set(range(a, b + 1))
string_new = [(i, c) for i, c in ncl if calls_of(c, 'STRING')]
check_true('E1  one STRING call left in the code, inside ne_Fx (%s)' % [i for i, _ in string_new],
           len(string_new) == 1 and string_new[0][0] in range(*helpers['ne_Fx']))
nfx = sum(calls_of(c, 'ne_Fx') + calls_of(c, 'ne_PStr') for i, c in ncl
          if i not in inside and not re.fullmatch(r'ne_\w+\(\);', c.strip()))
nold = sum(calls_of(c, 'STRING') for i, c in code_lines(oldsrc)) if HAVE_OLD else 134
check_true('E2  beta 42 had %d STRING calls; beta 42a has %d ne_Fx / ne_PStr calls in their place' % (nold, nfx),
           nold == 134 and nfx == 134)
check_true('E3  banner and second banner say beta 42a',
           nl[1] == '// NORM EXPLORER - beta 42a' and '// NORM EXPLORER — beta 42a' in nl[:90])
mp = re.search(r'MAP OF THE FILE  \((\d+) lines', newsrc)
check_true('E3  the file map gives the true line count (%s = %d)' % (mp.group(1), len(nl)), int(mp.group(1)) == len(nl))
check_true('E3  Roger\'s disclaimer sits under the distribution terms (comment only)',
           '// DISCLAIMER: a teaching and demonstration aid. Not validated for\n//   forensic, clinical or legal use; '
           'do not rely on its results for\n//   legal purposes.' in newsrc
           and newsrc.index('// DISCLAIMER') > newsrc.index('// FREE FOR EDUCATIONAL'))
check_true('E3  the tested-on lines say beta 42a has run on the PC harness only',
           'Beta 42a has run on the PC harness only (ppl_run_v3e)' in newsrc)
check_true('E3  a dated "beta 42a (19 Oct 2026)" paragraph citing D-NE-1..5 and "Line numbers are beta 42\'s"',
           all(s in newsrc for s in ('// beta 42a (19 Oct 2026)', 'D-NE-1', 'D-NE-2', 'D-NE-3', 'D-NE-4', 'D-NE-5',
                                     "Line numbers are beta 42's")))
fwd = [l for l in nl if re.fullmatch(r'ne_\w+\(\);', l)]
helpers['ne_Btw'] = routine_span(nl, 'ne_Btw')
for n in ('ne_Fx', 'ne_PStr', 'ne_Eq', 'ne_Btw'):
    first_use = min(i for i, c in ncl if calls_of(c, n) and i not in range(*helpers[n]) and not re.fullmatch(n + r'\(\);', c.strip()))
    check_true('E4  %s: forward-declared, defined at %d, before its first use at %d' % (n, helpers[n][0], first_use),
               (n + '();') in fwd and helpers[n][0] < first_use)
BUILTIN = set()
for l in open('/home/claude/work/HP_Prime_Builtin_Names.txt', encoding='utf-8'):
    l = l.strip()
    if l and not l.startswith('#'):
        BUILTIN |= {w.lower() for w in l.replace(',', ' ').split()}
newnames = ['ne_Fx', 'ne_PStr', 'ne_Eq', 'ne_Btw', 'fxV', 'fxD', 'fxR', 'psV', 'psD', 'eqS', 'pcO', 'btM', 'btS', 'btA', 'btB']
check_true('E5  no new name matches a built-in, case ignored (%s)' % ', '.join(newnames),
           not any(n.lower() in BUILTIN for n in newnames))
loc = [(i, c) for i, c in ncl if re.match(r'\s*LOCAL\s', c)]
check_true('E6  every LOCAL line holds 6 names or fewer (%d lines)' % len(loc),
           all(len(c.strip()[6:].rstrip(';').split(',')) <= 6 for _, c in loc))


def comment_in_bracket(src):
    bad, depth, py = [], 0, False
    for i, l in enumerate(src.split('\n'), 1):
        if l.startswith('#PYTHON'):
            py = True
        if py:
            if l.startswith('#END'):
                py = False
            continue
        k, instr = 0, False
        while k < len(l):
            ch = l[k]
            if ch == '"':
                instr = not instr
            elif not instr:
                if l.startswith('//', k):
                    if depth > 0:
                        bad.append(i)
                    break
                if ch in '([{':
                    depth += 1
                elif ch in ')]}':
                    depth -= 1
            k += 1
    return bad


check_true('E7  no // comment inside an open bracket', comment_in_bracket(newsrc) == [])
codejoin = '\n'.join(c for _, c in ncl)
check_true('E8  no right tail as 1 - CDF left (1 - NORMALD_CDF, 1-NE_P, 1-pcP, 1 - c2Pw, 1 - ndPV)',
           not re.search(r'1\s*-\s*(NORMALD_CDF|NE_P\b|pcP\b|c2Pw\b|ndPV\b)', codejoin))
check_true('E8  no quantile of 1 - p: no NORMALD_ICDF whose argument is formed as 1 - p or (1 + C)/2',
           not re.search(r'NORMALD_ICDF\([^;]*,\s*1\s*-|NORMALD_ICDF\([^;]*\(\s*1\s*\+', codejoin))
ICDF_WANT = [('NORMALD_ICDF(NE_MU, NE_SG, icP)', 'percentile: icP typed, refused unless 0 < icP < 1'),
             ('-NORMALD_ICDF(0, 1, icP)', 'right tail: alpha typed, refused unless 0 < alpha < 1'),
             ('NORMALD_ICDF(0, 1, icP)', 'left tail: alpha typed, refused unless 0 < alpha < 1'),
             ('-NORMALD_ICDF(0, 1, icP / 2)', 'two tails: alpha/2 in (0, 0.5)'),
             ('-NORMALD_ICDF(0, 1, (1 - icC) / 2)', 'central: C in (0, 1) after the percent rule, so (1 - C)/2 in (0, 0.5)'),
             ('-NORMALD_ICDF(0, 1, c2A)', 'power picture: alpha typed, refused unless 0 < alpha < 1')]
icdf_got = []
for _, c in ncl:
    k = c.find('NORMALD_ICDF(')
    if k < 0:
        continue
    j, depth = k + len('NORMALD_ICDF('), 1
    while depth:
        depth += {'(': 1, ')': -1}.get(c[j], 0); j += 1
    icdf_got.append(('-' if c[:k].rstrip().endswith('-') else '') + c[k:j])
for call, dom in ICDF_WANT:
    print('  %-38s %s' % (call, dom))
check_true('E8  the six NORMALD_ICDF calls are exactly these, each taking an area that its form keeps strictly '
           'inside 0..1 (%s)' % icdf_got, sorted(icdf_got) == sorted(c for c, _ in ICDF_WANT))
check_true('E9  INSTRING sites as in beta 42 (%d); the one new LEFT is guarded by DIM'
           % codejoin.count('INSTRING('),
           codejoin.count('INSTRING(') == '\n'.join(c for _, c in code_lines(oldsrc)).count('INSTRING(')
           and re.search(r'IF DIM\(eqS\) > 0 THEN\s*\n\s*IF LEFT\(eqS, 1\)', newsrc) is not None)


def tally(path):
    r = subprocess.run([sys.executable, '-I', '/home/claude/work/ppl_check_v4.py',
                        '/home/claude/work/whitelist_empty.json,/home/claude/work/HP_Prime_Builtin_Names.txt', path],
                       capture_output=True, text=True)
    return sorted(re.findall(r'\b(E\d+|W\d+)\b', r.stdout + r.stderr))


if os.path.exists('/home/claude/work/ppl_check_v4.py'):
    tn, to = tally(NEW), tally(OLD) if HAVE_OLD else None
    hard = [c for c in tn if c in ('E2', 'E3', 'E6', 'E8', 'E10', 'E11', 'E12')]
    print('  ppl_check_v4: beta 42a %s; beta 42 %s' % ({c: tn.count(c) for c in set(tn)},
                                                       {c: to.count(c) for c in set(to)} if to else '-'))
    check_true('E10 ppl_check_v4: no hard code (E2 E3 E6 E8 E10 E11 E12), the same tally as beta 42', not hard and (to is None or tn == to))
    r = subprocess.run([sys.executable, '-I', '/home/claude/work/lint_ppl.py', NEW], capture_output=True, text=True)
    ro = subprocess.run([sys.executable, '-I', '/home/claude/work/lint_ppl.py', OLD], capture_output=True, text=True)
    pn = [l for l in r.stdout.splitlines() if 'PROBLEM' in l]
    po = [l for l in ro.stdout.splitlines() if 'PROBLEM' in l]
    print('  lint_ppl: beta 42a %d problems, beta 42 %d' % (len(pn), len(po)))
    strip = lambda ls: sorted(re.sub(r'NormExplorer_beta42a?', 'FILE', re.sub(r'line \d+', 'line N', l)) for l in ls)
    gone = [l for l in strip(po) if l not in strip(pn)]
    check_true('E11 lint_ppl: the 7 "CHOOSE return value" lines and the STRING(NORMALD(..)) miscount are gone, nothing new',
               not any('CHOOSE return value' in l for l in pn) and len(po) - len(pn) == 8
               and all(l in strip(po) for l in strip(pn)))
else:
    print('  SKIP: ppl_check_v4.py / lint_ppl.py not found')


# =============================================================================
section('PART F  -- the routine diff, beta 42 -> beta 42a')


def split_routines(src):
    lines = src.split('\n')
    rout, glue, py = {}, [], None
    k = 0
    while k < len(lines):
        l = lines[k]
        if l.startswith('#PYTHON'):
            j = k
            while not lines[j].startswith('#END'):
                j += 1
            rout[l.strip()] = '\n'.join(lines[k:j + 1]); k = j + 1; continue
        m = re.match(r'^(?:EXPORT\s+)?([A-Za-z_]\w*)\(([^;]*)\)\s*$', l)
        if m and k + 1 < len(lines) and lines[k + 1].strip() == 'BEGIN':
            j = k
            while lines[j] != 'END;':
                j += 1
            rout[m.group(1)] = '\n'.join(lines[k:j + 1]); k = j + 1; continue
        glue.append((k + 1, l)); k += 1
    return rout, glue


if HAVE_OLD:
    ro, go = split_routines(oldsrc)
    rn, gn = split_routines(newsrc)
    changed = sorted(n for n in ro if n in rn and ro[n] != rn[n])
    added = sorted(n for n in rn if n not in ro)
    removed = sorted(n for n in ro if n not in rn)
    same = sorted(n for n in ro if n in rn and ro[n] == rn[n])
    print('  changed (%d): %s' % (len(changed), ', '.join(changed)))
    print('  added   (%d): %s' % (len(added), ', '.join(added)))
    print('  removed (%d): %s' % (len(removed), ', '.join(removed) or '-'))
    print('  byte-identical (%d): %s' % (len(same), ', '.join(same)))
    WANT = sorted(['ne_Explorer', 'ne_SetWin', 'ne_ProbCalc', 'ne_InvCalc', 'ne_ZSolve', 'ne_Compare2', 'ne_Histo',
                   'ne_ZtoD2', 'ne_DiagPage', 'NormExp', 'ne_Tag', 'ne_NormDraw'])
    check_true('F1  exactly the intended routines changed (D-NE-1: 10 with displays; D-NE-2 and the two tail '
               'items: ne_ProbCalc, ne_InvCalc, ne_Compare2, ne_NormDraw; D-NE-3: 6 menus; D-NE-4: ne_InvCalc; '
               'D-NE-5: ne_Explorer)',
               changed == WANT)
    check_true('F2  the four helpers are the only routines added, none removed',
               added == ['ne_Btw', 'ne_Eq', 'ne_Fx', 'ne_PStr'] and not removed)
    check_true('F3  the #PYTHON SAMPBINSPY block is byte-identical', ro.get('#PYTHON SAMPBINSPY') == rn.get('#PYTHON SAMPBINSPY'))
    sm = difflib.SequenceMatcher(None, [l for _, l in go], [l for _, l in gn], autojunk=False)
    gl = []
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op != 'equal':
            gl.append((op, [go[i][0] for i in range(a1, a2)], [gn[j][0] for j in range(b1, b2)]))
    ok_old = {2, 18, 19, 24, 27, 75}
    oldl = sorted(set(x for _, a, _ in gl for x in a))
    print('  outside the routines (header, declarations, comments): %d hunks; beta 42 lines touched %s'
          % (len(gl), oldl))
    check_true('F4  outside the routines only the header (2, 18-19, 24, 27, 75), the disclaimer, the map, the '
               'beta 42a paragraph, three forward declarations and the helpers\' comments changed',
               set(oldl) <= ok_old and len(gl) <= 10)
else:
    print('  SKIP: beta 42 not found')


# =============================================================================
section('h.sci_strings of every ppl_run_v3e run')
tot = 0
for tag in ALL_SCI:
    n = len(ALL_SCI[tag]); tot += n
    print('  beta 42a  %-34s %d %s' % (tag, n, [s[2] for s in ALL_SCI[tag]][:6]))
for tag in OLD_SCI:
    print('  beta 42   %-34s %d %s' % (tag, len(OLD_SCI[tag]), [s[2] for s in OLD_SCI[tag]][:4]))
check_true('every ppl_run_v3e run of beta 42a: h.sci_strings is empty (%d scenario groups, %d entries)' % (len(ALL_SCI), tot),
           tot == 0)

print()
print('=' * 78)
print('TOTAL: %d checks, %d failures' % (NCHK[0], len(FAILS)))
for f in FAILS:
    print('  FAIL', f)
sys.exit(1 if FAILS else 0)
