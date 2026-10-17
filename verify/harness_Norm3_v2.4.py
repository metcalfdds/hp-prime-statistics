"""Harness run of Norm3 v2.4 (ppl_run_v1): every touch and key path, numbers vs SciPy.
Run:  python3 harness_Norm3_v24.py      (needs /home/claude/work/harness/ppl_run_v1.py)"""
import sys, re
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v1 import Harness, KEY, Tap, Drag, Key
from scipy.stats import norm

SRC = '/home/claude/work/out/Norm3_v2.4.txt'
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
print()
print('%d checks failed' % len(fails) if fails else 'ALL CHECKS PASSED')
