"""verify_Burr3_v2.4a.py -- checks Burr3 v2.4a (17 Oct 2026, evening): no "=" before a relation (b3_Eq), and an
exact-0 P(X <= x0) (1 - (1 + u)^(-K) with u below the last digit) shown as "< 0.0001".
  A. harness_Burr3_v24.py, v2.4's harness run (ppl_run_v1), on v2.4a; only the file name changed, and check 10b's
     alternative form is written without the "=" (its case, Burr3(3,2,1,1), prints 0.0207 either way).
  B. verify_Burr3.py, v2.4's formula mirror (it reads no program file), run as it is.
  C. v2.4a, harness v3e: each fixed display before and after; the exact 0; a sweep identical to v2.4 once its
     "= <" is written the v2.4a way; b3_Eq; the code-line diff; the names; the version strings; comments; no new
     scientific fixed decimals.
Run:  python3 verify_Burr3_v2.4a.py     (needs /home/claude/work/harness/ppl_run_v1.py; exit 0 = all pass)

(harness_Burr3_v24.py's docstring follows.)
Harness run of Burr3 v2.4 (ppl_run_v1): every touch and key path, numbers vs SciPy.
Run:  python3 harness_Burr3_v24.py      (needs /home/claude/work/harness/ppl_run_v1.py)"""
print('A. harness_Burr3_v24.py on v2.4a (ppl_run_v1)')
import sys, re, math
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v1 import Harness, KEY, Tap, Drag, Key
from scipy.stats import burr12, norm

SRC = '/home/claude/work/out/Burr3_v2.4a.txt'
LFT, RGT, TOPy, BOT = 24, 302, 24, 190
W, H = RGT - LFT, BOT - TOPy
fails = []


def check(label, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + label + ('   ' + str(info) if info != '' else ''))
    if not cond:
        fails.append(label)


class Frame(object):
    """One composed frame: the items after the last full-screen clear (the harness keeps
    RECT_P(G1,0,0,319,239,c) as a shape, not a clear)."""
    def __init__(self, scr):
        cut = 0
        for i, it in enumerate(scr.items):
            if getattr(it, 'cmd', None) == 'RECT_P' and list(it.args[:4]) == [0, 0, 319, 239]:
                cut = i + 1
        self.items = scr.items[cut:]
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


def row(f, y):
    return ' | '.join(t.text for t in sorted(f.text_at(y), key=lambda t: t.x))


def num(f, prefix):
    t = f.find(prefix)
    if t is None:
        return None
    m = re.search(re.escape(prefix) + r'\s*(-?[0-9.]+)', t.text)
    return float(m.group(1)) if m else None


def lines(f, colour):
    return sum(1 for s in f.shapes if s.cmd == 'LINE_P' and s.args[-1] == colour)


def xl(f):
    return [t.text for t in f.text_at(BOT + 4)]


def run(events, call='Burr3(2,1,1,1)', choose=(), **kw):
    h = Harness(SRC, **kw)
    for c in choose:
        h.choose(c)
    h.event(*events)
    h.execute(call)
    return h


GREY_GHOST, GREY, MAG = 0xC8C8C8, 0x5A5A5A, 0xC800C8
SLOT = {1: 20, 2: 75, 3: 130, 4: 180, 5: 240, 6: 300}

# ---- 1. the first frame, Burr3(2,1,1,1) ----
h = run([Key(4)])
f = frames(h)[0]
d = burr12(c=2, d=1, scale=1)
print('rows:', row(f, 1), '/', row(f, 12), '/', row(f, BOT + 15))
check('1a title row', row(f, 1) == 'Burr | C = 2.00 | K = 1.00 | S = 1.00 | x₀ = 1.00', row(f, 1))
check('1b readout vs scipy', f.has('pdf = %.4f (a height), P(X ≤ x₀) = %.4f' % (d.pdf(1), d.cdf(1))), row(f, 12))
check('1c status: mean, no variance, K×C', f.has('μ = %.3f, no variance (K×C ≤ 2)' % d.mean()) and f.has('K×C = 2.00'), row(f, BOT + 15))
check('1d markers vs scipy', f.has('mode %.2f' % (math.sqrt(1 / 3))) and f.has('median %.2f' % d.median()) and f.has('mean %.2f' % d.mean()),
      [t.text for t in f.texts if t.text.startswith(('mode', 'median', 'mean'))])
mn = [s.menu for s in h.screens if s.menu]
check('1e soft keys', mn and mn[0] == ['C', 'K', 'S', 'x₀', 'View', 'Quit'], mn[:1])
box = [s for s in f.shapes if s.cmd == 'RECT_P' and s.args[1] == 0 and s.args[3] == 11]
check('1f C highlighted (box at x 31..99)', box and box[0].args[0] == 31, [b.args for b in box])
check('1g nothing below 216', max(t.y for t in f.texts) <= 206, max(t.y for t in f.texts))
wide = [t.text for t in f.texts if t.x + 6 * len(t.text) > 320]
check('1h rows fit at 6 px/char', not wide, wide)
check('1i result string', h.result.startswith('Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 1.00) = 0.5000'), h.result)

# ---- 2. Right (C up): the ghost for one action, then gone ----
h = run([Key(8), Key(50), Key(4)])
F = frames(h)
print('   ghost LINE_Ps per frame:', [lines(x, GREY_GHOST) for x in F])
check('2a C 2.00 -> 2.25', F[1].has('C = 2.25'))
check('2b ghost drawn after the step', lines(F[1], GREY_GHOST) > 100)
check('2c ghost gone after the next action', lines(F[2], GREY_GHOST) == 0)
d = burr12(c=2.25, d=1, scale=1)
check('2d markers follow C', F[1].has('median %.2f' % d.median()) and F[1].has('mean %.2f' % d.mean()))

# ---- 3. Left x7 from C = 2, K = 1: down to the floor, refusal, hatch, cap ----
h = run([Key(7)] * 7 + [Key(4)])
F = frames(h)
cs = [num(x, 'C = ') for x in F]
print('   C per frame:', cs)
check('3a C stops at 0.50 (K×C = 0.5)', cs[-1] == 0.5 and cs[-2] == 0.5, cs)
check('3b refused step said on row 2', F[-1].has('step refused: K×C must stay ≥ 0.5'), row(F[-1], 12))
check('3c status shows the floor', F[-1].has('K×C = 0.50 (floor)') and F[-1].has('no mean (K×C ≤ 1)'), row(F[-1], BOT + 15))
dots = [s for s in F[-1].shapes if s.cmd == 'PIXON_P' and s.args[-1] == 0xFF0000 and s.args[0] >= LFT + int(0.8 * W)]
check('3d heavy-tail hatch (PIXON_P pattern) and its message', len(dots) > 150 and F[-1].has('heavy tail: no finite mean'), len(dots))
check('3e cap said on the plot', F[-1].has('window capped at 50×S'))
check('3f no mean marker when K×C <= 1', not any(t.text.startswith('mean ') for t in F[-1].texts))
check('3g ghost not drawn after a refused step', lines(F[-1], GREY_GHOST) == 0)
check('3h K×C = 1.5 (C = 1.5): mean, no hatch', F[2].has('C = 1.50') and not F[2].has('heavy tail'))

# ---- 4. choose S (soft key 3), Right: S x1.25 ----
h = run([Tap(SLOT[3], 228), Key(8), Key(4)])
F = frames(h)
box = [s for s in F[1].shapes if s.cmd == 'RECT_P' and s.args[1] == 0 and s.args[3] == 11]
check('4a S highlighted', box and box[0].args[0] == 167, [b.args for b in box])
check('4b S = 1.25 and the median scales', F[2].has('S = 1.25') and F[2].has('median %.2f' % burr12(c=2, d=1, scale=1.25).median()), row(F[2], 1))

# ---- 5. choose x0, drag in the plot: x0 follows, window held, snap on lift ----
xmax = math.sqrt(199)
px = lambda x: int(LFT + x / xmax * W)
h = run([Tap(SLOT[4], 228), Drag([(px(1), 150), (px(2), 150), (px(4.37), 150)]), Key(4)])
F = frames(h)
xs = [num(x, 'x₀ = ') for x in F]
print('   x0 per frame:', xs, ' x labels during / after:', xl(F[3])[-2:], xl(F[-1])[-2:])
check('5a x0 follows the finger', abs(xs[4] - (px(4.37) - LFT) / W * xmax) < 0.006, xs)
check('5b snapped on lift (grid 0.1)', abs(xs[-1] - round(xs[4], 1)) < 1e-9, xs[-1])
check('5c readout vs scipy after the drag', F[-1].has('P(X ≤ x₀) = %.4f' % burr12(c=2, d=1, scale=1).cdf(xs[-1])))

# ---- 6. the S-curve: tap (C chosen: a tap) at p = 0.9 -> x0 = 3 ----
y9 = int(round(BOT - 0.9 * H))
h = run([Tap(px(3.0), y9), Key(4)])
F = frames(h)
check('6a tap on the S-curve with C chosen (acts on the lift): p = 0.900 -> x0 = 3.00', F[2].has('p = 0.900 → x₀ = 3.00') and not F[1].has('p = '), row(F[2], 12))
check('6b P(X ≤ x0) after it', True)
h = run([Tap(SLOT[4], 228), Drag([(px(3.0), y9), (px(3.0), int(round(BOT - 0.975 * H)))]), Key(4)])
F = frames(h)
want = 'p = 0.975 → x₀ = %.2f' % burr12(c=2, d=1, scale=1).ppf(0.975)
check('6c drag up the S-curve to 0.975: ' + want, F[3].has(want), row(F[3], 12))
h = run([Tap(310, int(round(BOT - 0.5 * H))), Key(4)])
check('6d tap the right-hand axis at 0.5 -> the median', frames(h)[1].has('p = 0.500 → x₀ = 1.00'), row(frames(h)[1], 12))

# ---- 7. drag C (chosen) 50 px right: C = 2.50, window held, ghost, refit on lift ----
h = run([Drag([(150, 150), (155, 150), (200, 150)]), Key(4)])
F = frames(h)
cs = [num(x, 'C = ') for x in F]
print('   C per frame:', cs, ' x labels before / during / after:', xl(F[0])[-2:], xl(F[3])[-2:], xl(F[-1])[-2:])
check('7a under 8 px it is still a tap-in-waiting (C unchanged)', cs[2] == 2.0, cs)
check('7b past 8 px: C = 2 + 0.01*50', cs[3] == 2.5, cs)
check('7c window held during the drag', xl(F[3]) == xl(F[0]))
check('7d ghost during the drag and on the lift frame', lines(F[3], GREY_GHOST) > 100 and lines(F[-1], GREY_GHOST) > 50)
check('7e window refitted on the lift', xl(F[-1]) != xl(F[3]))
d = burr12(c=2.5, d=1, scale=1)
check('7f markers vs scipy at C = 2.5', F[-1].has('median %.2f' % d.median()) and F[-1].has('mode %.2f' % ((1.5 / 3.5) ** 0.4)))

# ---- 8. drag K (soft key 2) 100 px left: the K×C floor stops it at 0.25 ----
h = run([Tap(SLOT[2], 228), Drag([(200, 150), (150, 150), (100, 150)]), Key(4)])
F = frames(h)
ks = [num(x, 'K = ') for x in F]
print('   K per frame:', ks)
check('8a K stops at 0.25 (K×C = 0.50)', ks[-1] == 0.25 and ks[3] == 0.5, ks)

# ---- 9. drag S (soft key 3) 35 px right: S = 1.02^35 ----
h = run([Tap(SLOT[3], 228), Drag([(100, 150), (135, 150)]), Key(4)])
F = frames(h)
check('9a S = 1.02^35 = %.2f' % 1.02 ** 35, F[-1].has('S = %.2f' % 1.02 ** 35), row(F[-1], 1))

# ---- 10. View x4: the fitted normal, Burr3(3,2,1,1) ----
h = run([Tap(SLOT[5], 228)] * 4 + [Key(4)], call='Burr3(3,2,1,1)')
F = frames(h)
d = burr12(c=3, d=2, scale=1)
m, s = d.mean(), d.std()
cap = 'its P(X < 0) = %.4f' % norm.cdf(0, m, s)
print('   view 4:', [t.text for t in F[4].texts if 'normal' in t.text or 'P(X < 0)' in t.text])
check('10a fitted normal drawn in grey', lines(F[4], GREY) > 200 and F[4].has('grey = normal, same μ and σ'))
check('10b ' + cap, F[4].has(cap) or F[4].has('its P(X < 0) < 0.0001'), cap)
check('10c status: both moments vs scipy', F[4].has('μ = %.3f, σ = %.3f' % (m, s)), row(F[4], BOT + 15))
nd = [c for c in h.stat_calls if c[0] == 'NORMALD']
ymax_ok = max(c[2] for c in nd) <= max(d.pdf(x) for x in [i * 0.001 for i in range(1, 4000)]) * 10
check('10d the normal is cached (one fill: ~N NORMALD calls)', 278 <= len(nd) <= 278 + 5, len(nd))
h = run([Tap(SLOT[5], 228)] * 4 + [Key(4)])
check('10e K×C <= 2: the view says so instead', frames(h)[4].has('normal fit needs K×C > 2 (now 2.00)'))

# ---- 11. Enter -> Help -> tap -> back; 0 cycles the choice; Enter -> Quit ----
h = run([Key(30), Tap(100, 100), Key(42), Key(42), Key(30)], choose=[1, 3])
F = frames(h)
helps = [x for x in F if x.func == 'b3_Help']
check('11a help page', len(helps) == 1 and helps[0].has('CHOOSE (soft keys C K S x₀, or 0)'))
wide = [t.text for t in helps[0].texts if t.x + 6 * len(t.text) > 316]
check('11b help lines fit at 6 px/char', not wide, wide)
box = [s for s in F[-1].shapes if s.cmd == 'RECT_P' and s.args[1] == 0 and s.args[3] == 11]
check('11c 0 twice: S chosen', box and box[0].args[0] == 167, [b.args for b in box])
check('11d menu Quit returns the summary', h.result.startswith('Burr3:'), h.result)
h = Harness(SRC, stale_keys=True)
h.choose(1)
h.event(Key(30), Tap(100, 100), Key(4))
h.execute('Burr3(2,1,1,1)')
check('11e help held despite the menu\'s left-over OK (stale-key mode)',
      any(sc.func == 'b3_Help' for sc in h.pages) and not h.stale_skips, h.stale_skips)

# ---- 12. a mean beyond the capped window is named at the edge; C <= 1 mode is 0 ----
h = run([Key(4)], call='Burr3(1.01,1,1,1)')
f = frames(h)[0]
d = burr12(c=1.01, d=1, scale=1)
t = f.find('mean ')
print('   mean label:', t.text if t else None, ' scipy mean %.2f' % d.mean())
check('12a mean past the window: named at the right edge with an arrow', t and t.text.endswith('→') and abs(float(t.text.split()[1]) - d.mean()) < 0.01)
h = run([Key(4)], call='Burr3(1,1,1,1)')
check('12b mode 0 for C <= 1', frames(h)[0].has('mode 0.00'))

# ---- 13. cost: moving x0 does not refill the cache ----
h = Harness(SRC)
h.event(Key(50), Key(50), Key(50), Key(4))
h.execute('Burr3(2,1,1,1)')
print('   b3_bpdf-free check: pages %d' % len(h.pages))


# ======================================================================== C. v2.4a (harness v3e)
print()
print('C. v2.4a: no "=" before a relation; no "0.0000" for a P that is not 0 (harness v3e)')
import subprocess as _sp
import difflib as _dl
import re as _re
sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3e import Harness as H3
OLD24 = '/home/claude/work/out/Burr3_v2.4.txt'
C_ALL, C_OLD = [], []


def c_run(path, call, views=0):
    h = H3(path)
    for _ in range(views):
        h.tap(240, 230)                        # View (soft key 5)
    h.press('Esc')
    h.execute(call)
    (C_ALL if path == SRC else C_OLD).append((call, h))
    f = h.pages[-1]
    return [t.text for t in sorted(f.texts, key=lambda t: (t.y, t.x)) if 'pdf' in t.text or 'P(X' in t.text], h.result, h


for (call, views), old, new in (
        (('Burr3(2,1,1,0.005)', 0), (['pdf = 0.0100 (a height), P(X ≤ x₀) = < 0.0001'],
                                     'Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 5.00ᴇ-3) = < 0.0001; values in EP_BURR_*'),
         (['pdf = 0.0100 (a height), P(X ≤ x₀) < 0.0001'],
          'Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 5.00ᴇ-3) < 0.0001; values in EP_BURR_*')),
        (('Burr3(2,1,1,30)', 0), (['pdf = < 0.0001 (a height), P(X ≤ x₀) = 0.9989'],
                                  'Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 30.00) = 0.9989; values in EP_BURR_*'),
         (['pdf < 0.0001 (a height), P(X ≤ x₀) = 0.9989'],
          'Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 30.00) = 0.9989; values in EP_BURR_*')),
        (('Burr3(25,1,1,0.3)', 0), (['pdf = < 0.0001 (a height), P(X ≤ x₀) = < 0.0001'],
                                    'Burr3: C = 25.00, K = 1.00, S = 1.00, P(X ≤ 0.30) = < 0.0001; values in EP_BURR_*'),
         (['pdf < 0.0001 (a height), P(X ≤ x₀) < 0.0001'],
          'Burr3: C = 25.00, K = 1.00, S = 1.00, P(X ≤ 0.30) < 0.0001; values in EP_BURR_*')),
        (('Burr3(25,1,1,0.2)', 0), (['pdf = < 0.0001 (a height), P(X ≤ x₀) = 0.0000'],
                                    'Burr3: C = 25.00, K = 1.00, S = 1.00, P(X ≤ 0.20) = 0.0000; values in EP_BURR_*'),
         (['pdf < 0.0001 (a height), P(X ≤ x₀) < 0.0001'],
          'Burr3: C = 25.00, K = 1.00, S = 1.00, P(X ≤ 0.20) < 0.0001; values in EP_BURR_*')),
        (('Burr3(2,1,1,1)', 0), (['pdf = 0.5000 (a height), P(X ≤ x₀) = 0.5000'],
                                 'Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 1.00) = 0.5000; values in EP_BURR_*'), None)):
    a, b = c_run(OLD24, call, views), c_run(SRC, call, views)
    check('C1 %s, v2.4: %r | %s' % (call, a[0], a[1]), (a[0], a[1]) == old, repr(a[:2]))
    if new is None:
        check('C1 %s, v2.4a: an ordinary readout and summary are unchanged' % call, a[:2] == b[:2], repr(b[:2]))
    else:
        check('C1 %s, v2.4a: %r | %s' % (call, b[0], b[1]), (b[0], b[1]) == new, repr(b[:2]))
for call, old, new in (('Burr3(10,1,1,1)', 'its P(X < 0) = < 0.0001', 'its P(X < 0) < 0.0001'),
                       ('Burr3(3,2,1,1)', 'its P(X < 0) = 0.0207', 'its P(X < 0) = 0.0207')):
    a, b = c_run(OLD24, call, 4), c_run(SRC, call, 4)
    oa = [t for t in a[0] if t.startswith('its')]
    ob = [t for t in b[0] if t.startswith('its')]
    check('C1 view 4 %s: v2.4 %r -> v2.4a %r' % (call, oa, ob), oa == [old] and ob == [new])

# C2. the exact 0: computed 0, true value positive
b = c_run(SRC, 'Burr3(25,1,1,0.2)')
check('C2 C 25, x₀ 0.2: EP_BURR_CDF holds the computed value, 0 (1 + 0.2^25 is 1 in the last digit; SciPy %.2g); the '
      'screen says "< 0.0001"' % burr12(c=25, d=1, scale=1).cdf(0.2),
      b[2].globals_['EP_BURR_CDF'] == 0 and burr12(c=25, d=1, scale=1).cdf(0.2) > 0)


# C3. a sweep: every readout row and summary identical to v2.4 once its "= <" and its exact-0 CDF are written the
# v2.4a way
def c_rw(t):
    t = _re.sub(r' = ([<>] )', r' \1', t)
    t = t.replace('P(X ≤ x₀) = 0.0000', 'P(X ≤ x₀) < 0.0001')
    t = _re.sub(r'(P\(X ≤ [^)]*\)) = 0\.0000;', r'\1 < 0.0001;', t)
    return t


nrw, diffs, n = 0, [], 0
for C_ in (0.5, 1, 2, 4.5, 12, 25):
    for K_ in (1, 2, 0.25):
        if C_ * K_ < 0.5:
            continue
        for S_ in (1, 3.5):
            for x_ in (0.05, 0.2, 0.7, 1, 2.5, 9, 40):
                call = 'Burr3(%r,%r,%r,%r)' % (C_, K_, S_, x_)
                a, b = c_run(OLD24, call), c_run(SRC, call)
                ra = ([c_rw(x) for x in a[0]], c_rw(a[1]))
                n += 1
                if ra != (a[0], a[1]):
                    nrw += 1
                if ra != (b[0], b[1]):
                    diffs.append((call, ra, b[:2]))
check('C3 %d calls (C, K, S, x₀): every readout row and summary identical to v2.4 once its "= <" and exact-0 CDF '
      'are written the v2.4a way (%d needed it)' % (n, nrw), not diffs, repr(diffs[:2]))

# C4. b3_Eq
hc = H3(SRC)
e = [hc.call('b3_Eq', s) for s in ('< 0.0001', '> -0.0001', '0.5000', '')]
check('C4 b3_Eq: "< 0.0001" -> " < 0.0001", "> -0.0001" -> " > -0.0001", "0.5000" -> " = 0.5000", "" -> " = ": %r' % e,
      e == [' < 0.0001', ' > -0.0001', ' = 0.5000', ' = '])


# C5. the diff v2.4 -> v2.4a
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
wm = ['TEXTOUT_P("Burr3 v2.4  -  touch and keys", G1, 8, 6, 2, hpO);',
      'TEXTOUT_P("its P(X < 0) = "+b3_fmtp(NORMALD_CDF(mmean, msd, 0),4),',
      'TEXTOUT_P("pdf = "+b3_fmtp(pdf0,4)+" (a height), P(X ≤ x₀) = "+',
      'b3_fmtp(cdf0,4), G1, 4, 12, 1, cTx);',
      'STRING(S,2,2) + ", P(X ≤ " + STRING(b3X0,2,2) + ") = " +',
      'b3_fmtp(EP_BURR_CDF,4) + "; values in EP_BURR_*";']
wp = ['b3_Eq(eqS)', 'BEGIN', 'IF DIM(eqS) > 0 THEN', 'IF LEFT(eqS, 1) == "<" OR LEFT(eqS, 1) == ">" THEN RETURN " " + eqS; END;',
      'END;', 'RETURN " = " + eqS;', 'END;',
      'TEXTOUT_P("Burr3 v2.4a  -  touch and keys", G1, 8, 6, 2, hpO);',
      'TEXTOUT_P("its P(X < 0)"+b3_Eq(b3_fmtp(NORMALD_CDF(mmean, msd, 0),4)),',
      'TEXTOUT_P("pdf"+b3_Eq(b3_fmtp(pdf0,4))+" (a height), P(X ≤ x₀)"+',
      'b3_Eq(IFTE(cdf0 > 0, b3_fmtp(cdf0,4), "< 0.0001")), G1, 4, 12, 1, cTx);',
      'STRING(S,2,2) + ", P(X ≤ " + STRING(b3X0,2,2) + ")" +',
      'b3_Eq(IFTE(EP_BURR_CDF > 0, b3_fmtp(EP_BURR_CDF,4), "< 0.0001")) + "; values in EP_BURR_*";']
check('C5 the code lines that changed are exactly the 6 listed (and b3_Eq\'s 7): -%r +%r'
      % ([x for x in mi if x not in wm], [x for x in pl if x not in wp]), sorted(mi) == sorted(wm) and sorted(pl) == sorted(wp))
BI = set(l.strip().lower() for l in open('/home/claude/work/gate_r2/HP_Prime_Builtin_Names.txt', encoding='utf-8')
         if l.strip() and not l.startswith('#'))
check('C5 the new names b3_Eq and eqS are not built-ins (case ignored); b3_Eq carries the b3_ tag',
      not any(n.lower() in BI for n in ('b3_Eq', 'eqS')))
check('C5 version strings: the banner, the help page title, the "What changed in v2.4a" paragraph',
      t1.split('\n')[3] == '// BURR3 - v2.4a' and '"Burr3 v2.4a  -  touch and keys"' in t1
      and '// What changed in v2.4a (17 Oct 2026, evening' in t1 and '"Burr3 v2.4  -' not in t1)
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
check('C5 no INSTRING in v2.4a\'s code; b3_Eq reads LEFT(eqS, 1) only inside IF DIM(eqS) > 0',
      not any('INSTRING(' in l for l in k1))
sci = sorted(set((c, round(v, 12), d, r) for c, h in C_ALL for v, d, r in h.sci_strings))
sco = sorted(set((c, round(v, 12), d, r) for c, h in C_OLD for v, d, r in h.sci_strings))
print('   scientific fixed decimals: %d in the v2.4a runs of part C, %d in v2.4\'s; e.g. %r' % (len(sci), len(sco), sci[:2]))
check('C6 no NEW scientific fixed decimal: the %d v2.4a runs print exactly those v2.4 prints for the same calls (%d: x₀ '
      'below 0.01 in the summary, STRING(x₀, 2, 2), outside this pass)' % (len(C_ALL), len(sci)), sci == sco, repr(sci[:2]))

# B. verify_Burr3.py, v2.4's formula mirror (it reads no program file), run as it is
r = _sp.run([sys.executable, '/home/claude/work/out/verify_Burr3.py'], capture_output=True, text=True)
last = [l for l in r.stdout.split('\n') if l.strip()][-1:]
print('B. verify_Burr3.py (v2.4\'s formula mirror, unchanged): %s' % last)
check('B verify_Burr3.py passes: %s' % last, r.returncode == 0 and last == ['4972 checks passed, 0 failed'])

print()
print('%d checks failed' % len(fails) if fails else 'ALL CHECKS PASSED')
sys.exit(1 if fails else 0)
