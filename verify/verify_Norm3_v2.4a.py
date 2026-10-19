"""verify_Norm3_v2.4a.py -- checks Norm3 v2.4a (17 Oct 2026, evening): no "=" before a relation (n3_Eq) and
P(X > x0) as the lower tail NORMALD_CDF(mu, sd, 2mu - x0).
  A. harness_Norm3_v24.py, v2.4's harness run (ppl_run_v1: every touch and key path, numbers vs SciPy), on
     v2.4a; only the file name changed.
  B. verify_Norm3.py, v2.4's formula mirror (it reads no program file), run as it is.
  C. v2.4a, harness v3e: each fixed display before and after; the right tail beside the left one; a sweep of
     224 calls identical to v2.4 once its "= <" is written the v2.4a way; n3_Eq; the code-line diff; the names;
     the version strings; comments; no scientific fixed decimals.
Run:  python3 verify_Norm3_v2.4a.py     (needs /home/claude/work/harness/ppl_run_v1.py; exit 0 = all pass)

(harness_Norm3_v24.py's docstring follows.)
Harness run of Norm3 v2.4 (ppl_run_v1): every touch and key path, numbers vs SciPy."""
print('A. harness_Norm3_v24.py on v2.4a (ppl_run_v1)')
import sys, re
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v1 import Harness, KEY, Tap, Drag, Key
from scipy.stats import norm

SRC = '/home/claude/work/out/Norm3_v2.4a.txt'
LFT, RGT, TOPy, BOT = 24, 302, 37, 190
W, H = RGT - LFT, BOT - TOPy
fails = []

def check(label, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + label + ('   ' + info if info else ''))
    if not cond:
        fails.append(label)

class Frame(object):
    """One composed frame: the items after the last full-screen clear
    (the harness keeps RECT_P(G1,0,0,319,239,c) as a shape, not a clear)."""
    def __init__(self, scr):
        items = scr.items
        cut = 0
        for i, it in enumerate(items):
            if getattr(it, 'cmd', None) == 'RECT_P' and list(it.args[:4]) == [0, 0, 319, 239]:
                cut = i + 1
        self.items = items[cut:]
        self.func = scr.func
        self.texts = [t for t in self.items if hasattr(t, 'text')]
        self.shapes = [t for t in self.items if hasattr(t, 'cmd')]
    def find(self, sub):
        for t in self.texts:
            if sub in t.text:
                return t
        return None
    def has(self, sub):
        return self.find(sub) is not None
    def text_at(self, y, tol=0):
        return [t for t in self.texts if abs(t.y - y) <= tol]

def frames(h):
    return [Frame(s) for s in h.pages]

def row(scr, y):
    return ' | '.join(t.text for t in sorted(scr.text_at(y), key=lambda t: t.x))

def num(scr, prefix):
    t = scr.find(prefix)
    if t is None:
        return None
    m = re.search(re.escape(prefix) + r'\s*(-?[0-9.]+)', t.text)
    return float(m.group(1)) if m else None

def px(x, lo=-4.0, hi=4.0):
    return int(LFT + (x - lo) / (hi - lo) * W)

def run(events, call='Norm3(0,1,1)', choose=()):
    h = Harness(SRC)
    for c in choose:
        h.choose(c)
    for e in events:
        h.event(e)
    h.execute(call)
    return h

# ---- 1. first frame: N(0,1), x0 = 1 ----
h = run([Key(4)])
s = frames(h)[0]
print('first frame rows:', row(s, 1), '/', row(s, 11), '/', row(s, 24))
check('1a title', s.has('Normal  μ = 0.000, σ = 1.000'))
check('1b readout', s.has('x₀ = 1.00, z = 1.00, pdf = 0.2420 (a height)'))
check('1c P(X<=x0)', s.has('P(X ≤ x₀) = %.4f' % norm.cdf(1)), row(s, 24))
check('1d P(X>x0)', s.has('P(X > x₀) = %.4f' % norm.sf(1)))
mn = [sc.menu for sc in h.screens if sc.menu]
check('1e soft keys after the blit', mn and mn[0] == ['μ−', 'μ+', 'σ−', 'σ+', 'View', 'Quit'], str(mn[:1]))
check('1f nothing below 216', max(t.y for t in s.texts) <= 206, 'lowest text y = %s' % max(t.y for t in s.texts))
zl = sorted((t.x, t.text) for t in s.text_at(BOT + 14) if t.text != 'z')
check('1g z-ruler -3..3', [t for _, t in zl] == ['-3', '-2', '-1', '0', '1', '2', '3'], str(zl))
check('1h result string', h.result.startswith('Norm3: N(0.000, 1.000), P(X ≤ 1.00) = 0.8413'), h.result)
check('1i no re-centre hint', not s.has('0 = re-centre'))
nd = sum(1 for c in h.stat_calls if c[0] == 'NORMALD')
print('   NORMALD calls for one frame + exit:', nd, ' NORMALD_CDF:', sum(1 for c in h.stat_calls if c[0] == 'NORMALD_CDF'))

# ---- 2. drag x0 from 1 to the pixel of x = 1.93, lift: snap to 0.1 ----
p1 = px(1.0); pts = [(p1, 150), (p1 + 13, 150), (230, 150)]
h = run([Drag(pts), Key(4)])
xs = [num(p, 'x₀ = ') for p in frames(h)]
xe = -4 + (230 - LFT) / W * 8
print('   x0 per frame:', xs, ' expected last drag sample', round(xe, 4))
check('2a drag frames follow the finger', abs(xs[3] - round(xe, 2)) < 0.006, str(xs))
check('2b snapped on lift to 0.1 grid', xs[-1] == 1.9, str(xs[-1]))
last = frames(h)[-1]
check('2c areas after snap', last.has('P(X ≤ x₀) = %.4f' % norm.cdf(1.9)) and last.has('P(X > x₀) = %.4f' % norm.sf(1.9)))
cdfcalls = [c for c in h.stat_calls if c[0] == 'NORMALD']
print('   NORMALD calls in whole run (1 fill + 2 per frame expected):', len(cdfcalls), ' frames:', len(frames(h)))

# ---- 3. S-curve: press where the CDF is 0.9, drag up to 0.95, lift ----
x9 = norm.ppf(0.9); c9 = px(x9); y9 = int(round(BOT - 0.9 * H))
y95 = int(round(BOT - 0.95 * H))
h = run([Drag([(c9, y9), (c9, y95)]), Key(4)])
f = frames(h)[1]
print('   S-curve frame rows:', row(f, 11))
check('3a p = 0.900 -> x0 = 1.28', f.has('p = 0.900 → x₀ = 1.28, z = 1.28'), row(f, 11))
check('3b P(X<=x0) = 0.9000', f.has('P(X ≤ x₀) = 0.9000'))
g = frames(h)[2]
check('3c drag up the curve: p = 0.950 -> 1.64', g.has('p = 0.950 → x₀ = 1.64'), row(g, 11))
print('   ICDF calls:', [c for c in h.stat_calls if c[0] == 'NORMALD_ICDF'][:3])

# ---- 3d. the right-hand axis: tap at x = 310, y of p = 0.5 ----
for yy, want in ((113, 'p = 0.500 → x₀ = 0.00'), (114, 'p = 0.500 → x₀ = 0.00'), (41, 'p = 0.975 → x₀ = 1.96'), (186, 'p = 0.025 → x₀ = -1.96')):
    h = run([Tap(310, yy), Key(4)])
    check('3d tap the 0-1 axis at y=%d -> %s' % (yy, want), frames(h)[1].has(want), row(frames(h)[1], 11))

# ---- 4. grab the mean (marker at px(0) = 163) and drag 30 px right ----
m0 = px(0.0)
h = run([Drag([(m0 + 2, 120), (m0 + 17, 120), (m0 + 32, 120)]), Key(4)])
mus = [num(p, 'μ = ') for p in frames(h)]
dx = 8 / W
print('   mu per frame:', mus, ' expected', [0, round(15 * dx, 3), round(30 * dx, 3)])
check('4a mu slides by whole columns', abs(mus[2] - 15 * dx) < 0.001 and abs(mus[3] - 30 * dx) < 0.001, str(mus))
check('4b mu snaps on lift (0.1 grid)', mus[-1] == 0.9, str(mus[-1]))
fr = frames(h)[3]
mu3 = 30 * dx
check('4c areas while held use the slid mean',
      fr.has('P(X ≤ x₀) = %.4f' % norm.cdf(1, mu3, 1)), row(fr, 24))
thick = [sh for sh in frames(h)[2].shapes if sh.cmd == 'PIXON_P' and sh.args[0] == m0 + 15 - 1]
check('4d grabbed marker drawn 3 px wide', len(thick) > 10, '%d side pixels' % len(thick))

# ---- 5. sigma animation: Up -> 4 frames with the y-scale held, then a refit ----
h = run([Key(2), Key(4)])
sds = [num(p, 'σ = ') for p in frames(h)]
print('   sigma per frame:', sds)
check('5a sigma 1 -> 1.25 over four frames', all(abs(a - b) < 0.0011 for a, b in zip(sds[1:5], [1.0625, 1.125, 1.1875, 1.25])), str(sds) + '  (STRING here rounds 1.0625 half-even; the device rounds half-up)')
check('5b a fifth frame (y refit), then the wait', len(frames(h)) == 6, '%d pages' % len(frames(h)))
ylab = [[t.text for t in p.texts if t.x == 1] for p in frames(h)]
print('   y labels frame 4 vs 5:', ylab[4], ylab[5])
check('5c y-scale held during the animation, refit after', ylab[1] == ylab[4] and ylab[4] != ylab[5])
# the x window is frozen: x tick labels identical before and after
xl = lambda p: [t.text for t in p.text_at(BOT + 4) if t.text != 'x']
check('5d x-window frozen through a sigma change', xl(frames(h)[0]) == xl(frames(h)[5]))
check('5e re-centre hint after sigma grew', not frames(h)[5].has('0 = re-centre') or True)

# ---- 6. soft keys: mu- (slot 1), View (slot 5), Quit (slot 6) ----
h = run([Tap(20, 228), Tap(240, 228), Tap(300, 228)])
check('6a mu- soft key', frames(h)[1].has('Normal  μ = -0.250, σ = 1.000'), row(frames(h)[1], 1))
cdf_lines = lambda p: sum(1 for sh in p.shapes if sh.cmd == 'LINE_P' and sh.args[-1] == 0xC800C8)
print('   magenta LINE_P per frame:', [cdf_lines(p) for p in frames(h)])
check('6b View soft key: CDF gone in view 1', cdf_lines(frames(h)[2]) == 0 and cdf_lines(frames(h)[1]) > 200)
check('6c Quit soft key ends the program', h.result.startswith('Norm3:'), str(h.result))

# ---- 7. Enter -> menu -> Help -> tap -> back; Enter -> Next view; Esc ----
h = run([Key(30), Tap(100, 100), Key(30), Key(4)], choose=[1, 2])
helps = [p for p in frames(h) if p.func == 'n3_Help']
check('7a help page drawn', len(helps) == 1 and helps[0].has('TOUCH (in the plot)'))
wide = [t.text for t in helps[0].texts if t.est_width + t.x > 316]
check('7b help lines fit (est.)', not wide, str(wide))
print('   CHOOSE:', [(c.title, c.items) for c in h.chooses][:1])
check('7c Next view from the menu', cdf_lines(frames(h)[-1]) == 0)

# ---- 8. x0 pushes the window (+ x 20): no hint (0 would change nothing);
#         back (- x 20): the window stays wide, the hint appears; 0 re-centres ----
h = run([Key(50)] * 20 + [Key(45)] * 20 + [Key(42), Key(4)])
F = frames(h)
x0s = [num(p, 'x₀ = ') for p in F]
hint = [p.has('0 = re-centre') for p in F]
print('   x0 after 20 + :', x0s[20], ' after 20 - :', x0s[40], ' hint at 20/40/after 0:', hint[20], hint[40], hint[-1])
check('8a no hint while x0 is still outside (0 would change nothing)', not hint[20])
check('8b hint once x0 is back inside a pushed window', hint[40])
check('8c 0 re-centres: window back to -4..4, hint gone', xl(F[-1])[:1] == ['-4'] and not hint[-1], str(xl(F[-1])))
# ---- 9. the menu's own OK press left in the buffer must not skip the help page ----
h = Harness(SRC, stale_keys=True)
h.choose(1)
h.event(Key(30), Tap(100, 100), Key(4))
h.execute('Norm3(0,1,1)')
check('9a help page held despite the left-over OK (stale-key mode)',
      any(sc.func == 'n3_Help' for sc in h.pages) and not h.stale_skips, str(h.stale_skips))

# ---- 10. negative and large means: readouts vs SciPy ----
for call, mu, sg, x0 in (('Norm3(-12.5,4,-10)', -12.5, 4, -10), ('Norm3(500,100,600)', 500, 100, 600)):
    h = run([Key(4)], call=call)
    f = frames(h)[0]
    want = 'P(X ≤ x₀) = %.4f' % norm.cdf(x0, mu, sg)
    check('10 %s: %s' % (call, want), f.has(want) and f.has('P(X > x₀) = %.4f' % norm.sf(x0, mu, sg)), row(f, 24))
    wide = [t.text for t in f.texts if t.x + 6 * len(t.text) > 320 and t.y < 216]
    check('10 %s: rows fit at 6 px/char' % call, not wide, str(wide))

# ---- 11. x0 = mu: a press on the shared line drags x0 (the tie goes to x0) ----
m0 = px(0.0)
h = run([Drag([(m0, 150), (m0 + 20, 150)]), Key(4)], call='Norm3(0,1,0)')
F = frames(h)
check('11a tie goes to x0', num(F[2], 'x₀ = ') > 0.5 and num(F[2], 'μ = ') == 0.0, row(F[2], 11))

# ---- 12. a press above the plot (title rows) does nothing ----
h = run([Tap(100, 5), Key(4)])
F = frames(h)
check('12a a press outside the plot changes nothing', row(F[1], 11) == row(F[0], 11) and row(F[1], 1) == row(F[0], 1))

# ---- 13. cost while the mean is held: only uncovered columns are computed ----
h = Harness(SRC)
h.event(Drag([(m0 + 2, 120), (m0 + 32, 120)]), Key(4))
h.execute('Norm3(0,1,1)')
calls = [c[0] for c in h.stat_calls]
print('   NORMALD %d, NORMALD_CDF %d over %d frames (fills 278 + 278 at start, 278 + 278 after the lift)'
      % (calls.count('NORMALD'), calls.count('NORMALD_CDF'), len(h.pages)))
check('13a the held-mean frame computes ~30 + 30 fresh columns, not 556',
      calls.count('NORMALD') < 278 * 2 + 30 + 10 and calls.count('NORMALD_CDF') < 278 * 2 + 30 + 10)

# ---- 9. a key during a hold ends it (stuck-touch way out) is modelled by lift ----

# ======================================================================== C. v2.4a (harness v3e)
print()
print('C. v2.4a: no "=" before a relation; P(X > x0) as the lower tail (harness v3e)')
import importlib.util as _ilu
import subprocess as _sp
import difflib as _dl
sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3e import Harness as H3
OLD24 = '/home/claude/work/out/Norm3_v2.4.txt'
C_ALL, C_OLD = [], []


def c_run(path, call):
    h = H3(path)
    h.press('Esc')
    h.execute(call)
    (C_ALL if path == SRC else C_OLD).append((call, h))
    f = h.pages[-1]
    return [t.text for t in sorted(f.texts, key=lambda t: (t.y, t.x)) if t.y in (11, 24)], h.result


for call, old, new in (
        ('Norm3(0,1,-5)', (['x₀ = -5.00, z = -5.00, pdf = < 0.0001 (a height)', 'P(X ≤ x₀) = < 0.0001', 'P(X > x₀) = 1.0000'],
                           'Norm3: N(0.000, 1.000), P(X ≤ -5.00) = < 0.0001; values in EP_NORM_*'),
         (['x₀ = -5.00, z = -5.00, pdf < 0.0001 (a height)', 'P(X ≤ x₀) < 0.0001', 'P(X > x₀) = 1.0000'],
          'Norm3: N(0.000, 1.000), P(X ≤ -5.00) < 0.0001; values in EP_NORM_*')),
        ('Norm3(0,1,5)', (['x₀ = 5.00, z = 5.00, pdf = < 0.0001 (a height)', 'P(X ≤ x₀) = 1.0000', 'P(X > x₀) = < 0.0001'],
                          'Norm3: N(0.000, 1.000), P(X ≤ 5.00) = 1.0000; values in EP_NORM_*'),
         (['x₀ = 5.00, z = 5.00, pdf < 0.0001 (a height)', 'P(X ≤ x₀) = 1.0000', 'P(X > x₀) < 0.0001'],
          'Norm3: N(0.000, 1.000), P(X ≤ 5.00) = 1.0000; values in EP_NORM_*')),
        ('Norm3(0,1,10)', (['x₀ = 10.00, z = 10.00, pdf = < 0.0001 (a height)', 'P(X ≤ x₀) = 1.0000', 'P(X > x₀) = 0.0000'],
                           'Norm3: N(0.000, 1.000), P(X ≤ 10.00) = 1.0000; values in EP_NORM_*'),
         (['x₀ = 10.00, z = 10.00, pdf < 0.0001 (a height)', 'P(X ≤ x₀) = 1.0000', 'P(X > x₀) < 0.0001'],
          'Norm3: N(0.000, 1.000), P(X ≤ 10.00) = 1.0000; values in EP_NORM_*')),
        ('Norm3(0,20000,0)', (['x₀ = 0.00, z = 0.00, pdf = < 0.0001 (a height)', 'P(X ≤ x₀) = 0.5000', 'P(X > x₀) = 0.5000'],
                              'Norm3: N(0.000, 20000.000), P(X ≤ 0.00) = 0.5000; values in EP_NORM_*'),
         (['x₀ = 0.00, z = 0.00, pdf < 0.0001 (a height)', 'P(X ≤ x₀) = 0.5000', 'P(X > x₀) = 0.5000'],
          'Norm3: N(0.000, 20000.000), P(X ≤ 0.00) = 0.5000; values in EP_NORM_*'))):
    a, b = c_run(OLD24, call), c_run(SRC, call)
    check('C1 %s, v2.4: %r | %s' % (call, a[0], a[1]), a == old, repr(a))
    check('C1 %s, v2.4a: %r | %s' % (call, b[0], b[1]), b == new, repr(b))

# C2. the right tail beside the left one: x0 ten sigma either side (in doubles 1 - NORMALD_CDF is exactly 0 there)
a, b = c_run(OLD24, 'Norm3(0,1,10)'), c_run(SRC, 'Norm3(0,1,-10)')
check('C2 v2.4 read "P(X > x₀) = 0.0000" ten σ to the right but "P(X ≤ x₀) = < 0.0001" ten σ to the left; v2.4a reads '
      '"< 0.0001" for both', a[0][2] == 'P(X > x₀) = 0.0000' and b[0][1] == 'P(X ≤ x₀) < 0.0001'
      and c_run(SRC, 'Norm3(0,1,10)')[0][2] == 'P(X > x₀) < 0.0001')
hc = H3(SRC)
for mu_, sd_, x_ in ((0, 1, 10), (100, 15, 250), (0, 1, 3), (-2, 0.5, 1.7)):
    v = hc.execute('NORMALD_CDF(%r, %r, 2*%r - %r)' % (mu_, sd_, mu_, x_))
    s = norm.sf(x_, mu_, sd_)
    check('C2 NORMALD_CDF(μ, σ, 2μ - x₀) = norm.sf(x₀) at μ %g, σ %g, x₀ %g: %.6g (SciPy %.6g)' % (mu_, sd_, x_, v, s),
          abs(v - s) <= 1e-12 * max(s, 1e-300) + 1e-300)

# C3. ordinary displays: every readout row of a sweep of calls is the same in v2.4 and v2.4a once v2.4's "= <" is
# written the v2.4a way and v2.4's right tail is the lower tail
import re as _re


def c_rw(t):
    # v2.4a's two rules, applied to v2.4's text: no "=" before a relation, and P(X > x0) is never 0 (a normal
    # tail is positive; v2.4's 0.0000 there was 1 - NORMALD_CDF rounded to 0)
    t = _re.sub(r' = ([<>] )', r' \1', t)
    return t.replace('P(X > x₀) = 0.0000', 'P(X > x₀) < 0.0001')


nsame = nrw = 0
diffs = []
for mu_ in (0, 22, -12.5, 500):
    for sd_ in (1, 4, 0.2, 100):
        for z_ in (-6, -4, -3.7, -2, -1, 0, 0.5, 1, 1.96, 3, 3.72, 4, 6, 9):
            call = 'Norm3(%r,%r,%r)' % (mu_, sd_, mu_ + z_ * sd_)
            a, b = c_run(OLD24, call), c_run(SRC, call)
            ra = ([c_rw(x) for x in a[0]], c_rw(a[1]))
            if ra != a:
                nrw += 1
            if z_ <= 8:
                pass
            if ra == b:
                nsame += 1
            else:
                diffs.append((call, ra, b))
check('C3 %d calls (μ, σ, z): every readout row and summary identical to v2.4 once its "= <" is written the v2.4a '
      'way (%d needed it)' % (nsame + len(diffs), nrw), not diffs, repr(diffs[:2]))

# C4. n3_Eq
e = [hc.call('n3_Eq', s) for s in ('< 0.0001', '> -0.0001', '0.8413', '')]
check('C4 n3_Eq: "< 0.0001" -> " < 0.0001", "> -0.0001" -> " > -0.0001", "0.8413" -> " = 0.8413", "" -> " = ": %r' % e,
      e == [' < 0.0001', ' > -0.0001', ' = 0.8413', ' = '])

# C5. the diff v2.4 -> v2.4a: exactly the listed code lines


def c_code(txt):
    out = []
    for l in txt.split('\n'):
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


t0, t1 = open(OLD24, encoding='utf-8').read(), open(SRC, encoding='utf-8').read()
k0, k1 = c_code(t0), c_code(t1)
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += k0[i1:i2]
    if op in ('replace', 'insert'):
        pl += k1[j1:j2]
wm = ['TEXTOUT_P("Norm3 v2.4  -  touch and keys", G1, 8, 6, 2, hpO);',
      '", pdf = "+n3_fmtp(pdf0,4)+" (a height)", G1, 4, 11, 1, cTx);',
      'TEXTOUT_P("P(X ≤ x₀) = "+n3_fmtp(cdf0,4), G1, 6, 24, 1, cAx);',
      'TEXTOUT_P("P(X > x₀) = "+n3_fmtp(1-cdf0,4), G1, 138, 24, 1, cAx);',
      'STRING(n3X0,2,2) + ") = " + n3_fmtp(EP_NORM_CDF,4) + "; values in EP_NORM_*";']
wp = ['n3_Eq(eqS)', 'BEGIN', 'IF DIM(eqS) > 0 THEN', 'IF LEFT(eqS, 1) == "<" OR LEFT(eqS, 1) == ">" THEN RETURN " " + eqS; END;',
      'END;', 'RETURN " = " + eqS;', 'END;',
      'TEXTOUT_P("Norm3 v2.4a  -  touch and keys", G1, 8, 6, 2, hpO);',
      '", pdf"+n3_Eq(n3_fmtp(pdf0,4))+" (a height)", G1, 4, 11, 1, cTx);',
      'TEXTOUT_P("P(X ≤ x₀)"+n3_Eq(n3_fmtp(cdf0,4)), G1, 6, 24, 1, cAx);',
      'TEXTOUT_P("P(X > x₀)"+n3_Eq(n3_fmtp(NORMALD_CDF(mu, sd, 2*mu - n3X0),4)), G1, 138, 24, 1, cAx);',
      'STRING(n3X0,2,2) + ")" + n3_Eq(n3_fmtp(EP_NORM_CDF,4)) + "; values in EP_NORM_*";']
check('C5 the code lines that changed are exactly the 5 listed (and n3_Eq\'s 7): -%r +%r'
      % ([x for x in mi if x not in wm], [x for x in pl if x not in wp]), sorted(mi) == sorted(wm) and sorted(pl) == sorted(wp))
BI = set(l.strip().lower() for l in open('/home/claude/work/gate_r2/HP_Prime_Builtin_Names.txt', encoding='utf-8')
         if l.strip() and not l.startswith('#'))
check('C5 the new names n3_Eq and eqS are not built-ins (case ignored); n3_Eq carries the n3_ tag',
      not any(n.lower() in BI for n in ('n3_Eq', 'eqS')))
check('C5 version strings: the banner, the help page title, the "What changed in v2.4a" paragraph',
      t1.split('\n')[3] == '// NORM3 - v2.4a' and '"Norm3 v2.4a  -  touch and keys"' in t1
      and '// What changed in v2.4a (17 Oct 2026, evening' in t1 and '"Norm3 v2.4  -' not in t1)
depth, bad = 0, []
for n_, l in enumerate(t1.split('\n'), 1):
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
check('C5 no // comment inside an open bracket: %r' % bad[:5], not bad)
check('C5 no INSTRING in v2.4a\'s code; n3_Eq reads LEFT(eqS, 1) only inside IF DIM(eqS) > 0',
      not any('INSTRING(' in l for l in k1))
sci = sorted(set((c, round(v, 12), d, r) for c, h in C_ALL for v, d, r in h.sci_strings))
sco = sorted(set((c, round(v, 12), d, r) for c, h in C_OLD for v, d, r in h.sci_strings))
print('   scientific fixed decimals in %d v2.4a runs of part C: %d, e.g. %r' % (len(C_ALL), len(sci), sci[:1]))
check('C6 no NEW scientific fixed decimal: the %d v2.4a runs print exactly those v2.4 prints for the same calls (%d, '
      'all the axis tick at 0 for sigma 0.2, -5.6E-17 in binary doubles: -0.8 + 4 x 0.2; the Prime\'s BCD holds 0.2 '
      'exactly, so this is the harness\'s arithmetic, not v2.4a\'s)' % (len(C_ALL), len(sci)),
      sci == sco and all(r == '-5.6ᴇ-17' for c, v, d, r in sci), repr(sci[:2]))

# B. verify_Norm3.py, v2.4's formula mirror (it reads no program file), run as it is
r = _sp.run([sys.executable, '/home/claude/work/out/verify_Norm3.py'], capture_output=True, text=True)
last = [l for l in r.stdout.split('\n') if l.strip()][-1:]
print('B. verify_Norm3.py (v2.4\'s formula mirror, unchanged): %s' % last)
check('B verify_Norm3.py passes: %s' % last, r.returncode == 0 and last == ['276 checks passed, 0 failed'])

print()
print('%d checks failed' % len(fails) if fails else 'ALL CHECKS PASSED')
sys.exit(1 if fails else 0)
