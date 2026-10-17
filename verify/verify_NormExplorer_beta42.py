#!/usr/bin/env python3
"""verify_NormExplorer.py -- checks for NormExplorer beta 42 (16 Oct 2026).

Part A checks every NEW formula of beta 42 against SciPy:
  left-tail and two-tailed critical values, the power of a right-tail cut,
  a histogram bin's expected count n*p, the trapezoid CDF cache that draws
  the S-curve, the density digits rule, the sweep's start and end points.

Part B RUNS the PPL itself in hp-prime-kit's interpreter (the same source
that ships), with a small harness:
  * pre-processing the kit cannot read: the #PYTHON block, forward
    declarations, file-level LOCAL lines (read as globals), #RRGGBBh
    literals and the square-root sign (-> SQRT);
  * SciPy for NORMALD / NORMALD_CDF / NORMALD_ICDF;
  * STRING(v, 2, d) as fixed decimals;
  * scripted CHOOSE and INPUT answers (written into the named variables),
    scripted keys and touches (each optionally tied to the routine that
    must be running to receive it), TICKS as a counter;
  * every TEXTOUT_P, RECT_P, LINE_P, PIXON_P, DRAWMENU and MSGBOX recorded,
    frame by frame (a frame ends at BLIT_P).
It then compares the numbers PRINTED by the program with SciPy.

Run:  python3 verify_NormExplorer.py [path/to/NormExplorer_beta42.txt]
"""
import sys, re, math, random
import numpy as np
from scipy.stats import norm

sys.path.insert(0, '/home/claude/kit/hp-prime-kit-HEAD')
from hpkit import interp

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/out/NormExplorer_beta42.txt'
FAILS = []


def check(label, got, want, tol=5e-5):
    ok = abs(got - want) <= tol
    print('  %-58s got %-12.6g want %-12.6g %s' % (label, got, want, 'ok' if ok else '** FAIL **'))
    if not ok:
        FAILS.append(label)


def check_true(label, cond):
    print('  %-58s %s' % (label, 'ok' if cond else '** FAIL **'))
    if not cond:
        FAILS.append(label)


# ---------------------------------------------------------------- Part A
print('=' * 78)
print('PART A  -- the new formulas against SciPy')
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
print('PART B  -- the PPL itself, in the kit interpreter')
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

print()
print('FAILURES: %d %s' % (len(FAILS), FAILS))
sys.exit(1 if FAILS else 0)
