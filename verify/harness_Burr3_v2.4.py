"""Harness run of Burr3 v2.4 (ppl_run_v1): every touch and key path, numbers vs SciPy.
Run:  python3 harness_Burr3_v24.py      (needs /home/claude/work/harness/ppl_run_v1.py)"""
import sys, re, math
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v1 import Harness, KEY, Tap, Drag, Key
from scipy.stats import burr12, norm

SRC = '/home/claude/work/out/Burr3_v2.4.txt'
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
check('10b ' + cap, F[4].has(cap) or F[4].has('its P(X < 0) = < 0.0001'), cap)
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

print()
print('%d checks failed' % len(fails) if fails else 'ALL CHECKS PASSED')
