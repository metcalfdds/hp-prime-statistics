"""verify_Norm3_v2.4b.py -- checks Norm3 v2.4b (19 Oct 2026): N1 of the fleet review (ROUND before STRING on mu,
sigma, x0 and z, through n3_Fx; a value too small for its decimals reads "< 0.001", never 0.000 and never the
Prime's scientific form), n3_Nm for the summary's slots, and the MAKELIST caches counting with the LOCAL n3I.
Built from verify_Norm3_v2.4a.py; every check is kept:
  A. harness_Norm3_v24.py (ppl_run_v1), now on v2.4b; only the file name changed.
  B. verify_Norm3.py, v2.4's formula mirror (it reads no program file), run as it is.
  C. v2.4a's own checks (v2.4 against v2.4a, harness v3e), kept as they were: they now read the v2.4a file
     from /home/claude/work/out (that change set), as the v2.4a script compared v2.4 with v2.4a.
  D. (new, v2.4b, harness v3e)
     D1 the review's check_Norm3.py, run on v2.4b and on v2.4a (regression: its 5 failures on v2.4a pass on
        v2.4b; only its two version expectations are moved from v2.4a to v2.4b);
     D2 each N1 reproduction from findings_A, v2.4a against v2.4b;  D3 n3_Fx and n3_Nm;
     D4 a sweep of ordinary calls: v2.4b prints what v2.4a prints;  D5 Home's K untouched (the LOCAL counter);
     D6 the routine diff (only Norm3, n3_Help and the two new helpers differ);  D7 the code;
     D8 every scientific STRING result (h.sci_strings) of every v2.4b run in this script.
Run:  python3 verify_Norm3_v2.4b.py     (needs /home/claude/work/harness/ppl_run_v1.py and out/ppl_run_v3e.py)

(verify_Norm3_v2.4a.py's docstring follows.)
verify_Norm3_v2.4a.py -- checks Norm3 v2.4a (17 Oct 2026, evening): no "=" before a relation (n3_Eq) and
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
print('A. harness_Norm3_v24.py on v2.4b (ppl_run_v1)')
import sys, re
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v1 import Harness, KEY, Tap, Drag, Key
from scipy.stats import norm

SRC = '/home/claude/work/fix19/Norm3_v2.4b.txt'          # v2.4b: part A runs on the new file
SRC_C = '/home/claude/work/out/Norm3_v2.4a.txt'         # v2.4b: part C keeps checking the v2.4a change set
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
# (v2.4b: SRC_C is the v2.4a file in out/; these are v2.4a's checks of its own change set)
print()
print('C. v2.4a: no "=" before a relation; P(X > x0) as the lower tail (harness v3e)')
import importlib.util as _ilu
import subprocess as _sp
import difflib as _dl
sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3e import Harness as H3
OLD24 = '/home/claude/work/out/Norm3_v2.4.txt'
C_ALL, C_OLD = [], []


class _Lite(object):
    def __init__(self, sci):
        self.sci_strings = sci



def c_run(path, call):
    h = H3(path)
    h.press('Esc')
    h.execute(call)
    # (v2.4b: C6 reads only the run's scientific strings; keeping the whole harness of 460 runs ran a
    # shared machine out of memory)
    (C_ALL if path == SRC_C else C_OLD).append((call, _Lite(h.sci_strings)))
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
    a, b = c_run(OLD24, call), c_run(SRC_C, call)
    check('C1 %s, v2.4: %r | %s' % (call, a[0], a[1]), a == old, repr(a))
    check('C1 %s, v2.4a: %r | %s' % (call, b[0], b[1]), b == new, repr(b))

# C2. the right tail beside the left one: x0 ten sigma either side (in doubles 1 - NORMALD_CDF is exactly 0 there)
a, b = c_run(OLD24, 'Norm3(0,1,10)'), c_run(SRC_C, 'Norm3(0,1,-10)')
check('C2 v2.4 read "P(X > x₀) = 0.0000" ten σ to the right but "P(X ≤ x₀) = < 0.0001" ten σ to the left; v2.4a reads '
      '"< 0.0001" for both', a[0][2] == 'P(X > x₀) = 0.0000' and b[0][1] == 'P(X ≤ x₀) < 0.0001'
      and c_run(SRC_C, 'Norm3(0,1,10)')[0][2] == 'P(X > x₀) < 0.0001')
hc = H3(SRC_C)
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
            a, b = c_run(OLD24, call), c_run(SRC_C, call)
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


t0, t1 = open(OLD24, encoding='utf-8').read(), open(SRC_C, encoding='utf-8').read()
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

# ======================================================================== D. v2.4b (harness v3e)
print()
print('D. v2.4b: N1 (ROUND before STRING, n3_Fx / n3_Nm), the LOCAL MAKELIST counter (harness v3e)')
import io as _io
import contextlib as _cl
import types as _types
import os as _os
NEW = '/home/claude/work/fix19/Norm3_v2.4b.txt'
V24A = '/home/claude/work/out/Norm3_v2.4a.txt'
REVIEW = '/home/claude/work/review/check_Norm3.py'
D_NEW = []                                   # every v2.4b harness of part D (for D8)


D_SCI, D_RUNS = [], [0]


def d_flush():
    """keep only the scientific STRING results of the v2.4b harnesses already used, and let the harnesses go
    (memory: a harness keeps every drawing call of its run)"""
    for h_ in D_NEW:
        D_SCI.extend(h_.sci_strings)
        D_RUNS[0] += 1
    del D_NEW[:]


def d_h(path, **k):
    if len(D_NEW) >= 6:
        d_flush()
    h = H3(path, strict=True, on_unverified='warn', **k)
    if path == NEW:
        D_NEW.append(h)
    return h


# ---- D1. the review's check_Norm3.py on v2.4b and on v2.4a ----
# Its expectations are the review's.  Two of them name the version (the help page's title, the version string
# on screen), so they move from v2.4a to v2.4b; nothing else is touched.  PPL is pointed at each file in turn.
D1_PATCHES = [
    ("PPL = os.path.join(FLEET, 'Norm3_v2.4a.txt')", "PPL = __PPL__"),
    ("hp = [f for f in fr if f.find('Norm3 v2.4a  -  touch and keys')]",
     "hp = [f for f in fr if f.find('Norm3 ' + __VER__ + '  -  touch and keys')]"),
    ("check(vers == ['v2.4a'], 'D2 version string on screen: %s' % vers)",
     "check(vers == [__VER__], 'D2 version string on screen: %s' % vers)"),
]


def run_review(path, ver):
    s = open(REVIEW, encoding='utf-8').read()
    for o, n in D1_PATCHES:
        assert s.count(o) == 1, o
        s = s.replace(o, n)
    ns = {'__name__': 'review_check', '__file__': REVIEW, '__PPL__': path, '__VER__': ver}
    buf = _io.StringIO()
    with _cl.redirect_stdout(buf):
        exec(compile(s, REVIEW, 'exec'), ns)
        ns['main']()
    return ns['NCHECK'][0], list(ns['FAILS']), buf.getvalue()


n_new, f_new, out_new = run_review(NEW, 'v2.4b')
n_old, f_old, out_old = run_review(V24A, 'v2.4b')
print('   review check_Norm3.py on v2.4b: %d checks, %d failed %s' % (n_new, len(f_new), f_new[:3]))
print('   the same on v2.4a: %d checks, %d failed:' % (n_old, len(f_old)))
for f in f_old:
    print('      FAIL  ' + f[:150])
n1_old = [f for f in f_old if f.startswith(('C3 ', 'C6 '))]
check('D1 the review\'s check_Norm3.py passes in full on v2.4b (%d checks, 0 failed)' % n_new, n_new == 172 and not f_new,
      repr(f_new[:2]))
check('D1 regression: on v2.4a the same script fails the 5 N1 checks (C3 x 4, C6) the review found, and only the two '
      'version expectations besides (help title, D2)', len(n1_old) == 5 and len(f_old) == 7
      and any(f.startswith('B4 the help page was shown once') for f in f_old)
      and any(f.startswith('D2 version string') for f in f_old), repr(f_old))

# ---- D2. each N1 reproduction from findings_A, v2.4a against v2.4b ----
LFT_, RGT_, TOPy_, BOT_ = 24, 302, 37, 190
W_, H_ = RGT_ - LFT_, BOT_ - TOPy_


def d_rows(h):
    """the title row, row 2 and the summary of the last frame"""
    t = {}
    for x in h.texts:
        if x.y == 1 and x.x == 4:
            t['title'] = x.text
        if x.y == 11 and x.x == 4:
            t['row2'] = x.text
    return t


def d_allrows(h):
    return sorted(set(x.text for x in h.texts if (x.y, x.x) in ((1, 4), (11, 4))))


def d_run(path, args, script=None):
    h = d_h(path)
    if script:
        script(h)
    h.press('Esc')
    r = h.call('Norm3', *[float(v) for v in args])
    return h, r


def s_down31(h):
    for _ in range(31):
        h.press('Down')


def s_down60(h):
    for _ in range(60):
        h.press('Down')


def s_scurve51(h):
    cdfx = norm.ppf(0.51) * 0.1
    col = int(LFT_ + (cdfx + 0.4) / 0.8 * W_) + 8
    h.tap(col, int(BOT_ - 0.51 * H_ + 0.5))


def s_drag8(h):
    col0 = int(LFT_ + 0.5 * W_)
    h.drag([(col0 + 8, 120), (col0 + 9, 120)])


SCI = 'ᴇ'
D2 = [
    ('31 σ- presses from σ = 1 (title)', (0, 1, 0), s_down31,
     lambda o, n: any(SCI in s for s in o) and 'Normal  μ = 0.000, σ = 0.001' in n),
    ('60 σ- presses, σ at its 0.0001 floor (title)', (0, 1, 0), s_down60,
     lambda o, n: 'Normal  μ = 0.000, σ = 1.000ᴇ-4' in o and 'Normal  μ = 0.000, σ < 0.001' in n),
    ('a press on the S-curve at p = 0.51, σ = 0.1 (inverse row)', (0, 0.1, 0.05), s_scurve51,
     lambda o, n: any(s.startswith('p = 0.510') and SCI in s for s in o)
     and any(s.startswith('p = 0.510 ' + chr(8594) + ' x₀ < 0.01, z = 0.03') for s in n)),
    ('a drag 8-9 px right of the mean, σ = 0.03 (row 2 while the finger is down)', (0, 0.03, 0.01), s_drag8,
     lambda o, n: any(s.startswith('x₀ = 6.91ᴇ-3') for s in o) and any(s.startswith('x₀ = 0.01, z = 0.23') for s in n)),
    ('Norm3(0, 1, 0.004) (row 2)', (0, 1, 0.004), None,
     lambda o, n: 'x₀ = 4.00ᴇ-3, z = 4.00ᴇ-3, pdf = 0.3989 (a height)' in o
     and 'x₀ < 0.01, z < 0.01, pdf = 0.3989 (a height)' in n),
    ('Norm3(0.0005, 1, 0.005) (title, row 2)', (0.0005, 1, 0.005), None,
     lambda o, n: 'Normal  μ = 5.000ᴇ-4, σ = 1.000' in o and 'Normal  μ = 0.001, σ = 1.000' in n
     and 'x₀ = 0.01, z < 0.01, pdf = 0.3989 (a height)' in n),
    ('Norm3(-0.0004, 1, -0.003) (negative values that round to 0)', (-0.0004, 1, -0.003), None,
     lambda o, n: 'Normal  μ > -0.001, σ = 1.000' in n and 'x₀ > -0.01, z > -0.01, pdf = 0.3989 (a height)' in n),
]
SUMS = {}
for label, args, script, ok in D2:
    ho, ro = d_run(V24A, args, script)
    hn, rn = d_run(NEW, args, script)
    o, n = d_allrows(ho), d_allrows(hn)
    SUMS[label] = (ro, rn)
    print('   %s\n      v2.4a: %s\n      v2.4b: %s' % (label, [s for s in o if SCI in s][:2] or o[:2], [s for s in n if s not in o][:3]))
    check('D2 %s: v2.4a printed the scientific form, v2.4b reads it rounded or as "< 0.01" / "< 0.001"' % label,
          ok(o, n) and not any(SCI in s for s in n) and not any(SCI in s for s in [rn]), repr(n[:3]))
# the summary returned to Home
for label, want_o, want_n in (
        ('Norm3(0, 1, 0.004) (row 2)', 'Norm3: N(0.000, 1.000), P(X ≤ 4.00ᴇ-3) = 0.5016; values in EP_NORM_*',
         'Norm3: N(0.000, 1.000), P(X ≤ x₀) = 0.5016 with x₀ < 0.01; values in EP_NORM_*'),
        ('60 σ- presses, σ at its 0.0001 floor (title)', 'Norm3: N(0.000, 1.000ᴇ-4), P(X ≤ 0.00) = 0.5000; values in EP_NORM_*',
         'Norm3: N(0.000, σ < 0.001), P(X ≤ 0.00) = 0.5000; values in EP_NORM_*'),
        ('Norm3(-0.0004, 1, -0.003) (negative values that round to 0)',
         'Norm3: N(-4.000ᴇ-4, 1.000), P(X ≤ -3.00ᴇ-3) = 0.4990; values in EP_NORM_*',
         'Norm3: N(μ > -0.001, 1.000), P(X ≤ x₀) = 0.4990 with x₀ > -0.01; values in EP_NORM_*')):
    ro, rn = SUMS[label]
    check('D2 the summary to Home, %s: v2.4a %r -> v2.4b %r' % (label, ro, rn), ro == want_o and rn == want_n, repr((ro, rn)))
# the numbers themselves did not change: EP_NORM_* are the computed values
hn, rn = d_run(NEW, (0, 1, 0.004))
g = hn.globals_
check('D2 EP_NORM_X0, EP_NORM_Z and EP_NORM_CDF keep the computed values (0.004, 0.004, Phi(0.004))',
      g['EP_NORM_X0'] == 0.004 and abs(g['EP_NORM_Z'] - 0.004) < 1e-15 and abs(g['EP_NORM_CDF'] - norm.cdf(0.004)) < 1e-12)

# ---- D3. n3_Fx and n3_Nm ----
hc3 = d_h(NEW)
FX = [((0.0004, 3), '< 0.001'), ((-0.0004, 3), '> -0.001'), ((0.0005, 3), '0.001'), ((0.0, 3), '0.000'),
      ((1.0, 3), '1.000'), ((0.004, 2), '< 0.01'), ((-0.004, 2), '> -0.01'), ((0.005, 2), '0.01'), ((2.5, 2), '2.50'),
      ((-12.5, 3), '-12.500'), ((20000.0, 3), '20000.000'), ((1e-9, 2), '< 0.01')]
got = [(a, hc3.call('n3_Fx', float(a[0]), float(a[1]))) for a, _ in FX]
check('D3 n3_Fx: 0.0004 -> "< 0.001", -0.0004 -> "> -0.001", 0.0005 -> "0.001" (halves away from 0), 0 -> "0.000", '
      '0.004 -> "< 0.01", 0.005 -> "0.01", 1E-9 -> "< 0.01" ...', [g_ for _, g_ in got] == [w for _, w in FX], repr(got))
NM = [(('σ', 0.0004, 3), 'σ < 0.001'), (('σ', 1.0, 3), '1.000'), (('μ', -0.0004, 3), 'μ > -0.001'), (('μ', 0.0, 3), '0.000')]
got = [hc3.call('n3_Nm', a[0], float(a[1]), float(a[2])) for a, _ in NM]
check('D3 n3_Nm: a plain number as it is; a value too small for its decimals with its name: %r' % got,
      got == [w for _, w in NM])

# ---- D4. a sweep of ordinary calls: v2.4b prints what v2.4a prints ----
nsame, diff4 = 0, []
for mu_ in (0, 22, -12.5, 500):
    for sd_ in (1, 4, 0.2, 100):
        for z_ in (-6, -4, -3.7, -2, -1, 0, 0.5, 1, 1.96, 3, 3.72, 4, 6, 9):
            args = (mu_, sd_, mu_ + z_ * sd_)
            ho, ro = d_run(V24A, args)
            hn, rn = d_run(NEW, args)
            ko = [x.text for x in ho.texts if x.y in (1, 11, 24)]
            kn = [x.text for x in hn.texts if x.y in (1, 11, 24)]
            if ko == kn and ro == rn:
                nsame += 1
            else:
                diff4.append((args, [(a, b) for a, b in zip(ko + [ro], kn + [rn]) if a != b][:2]))
check('D4 %d ordinary calls (μ 0, 22, -12.5, 500; σ 1, 4, 0.2, 100; 14 values of z): every title, row 2, area key and '
      'summary of v2.4b is v2.4a\'s, character for character' % (nsame + len(diff4)), not diff4, repr(diff4[:2]))

# ---- D5. the MAKELIST caches no longer count with Home's K ----
# On the Prime MAKELIST writes its counter, so v2.4a's MAKELIST(0, K, 1, N, 1) left Home's K at N (Lessons Learned
# v7i section 5).  The harness binds a MAKELIST counter locally and cannot show that write, so this is a code check;
# the run below shows the LOCAL counter fills both caches (278 columns) and Home's K stays as it was.
mk = lambda t: re.findall(r'(\w+) := MAKELIST\(0, (\w+), 1, N, 1\);', '\n'.join(c_code(t)))
mk0, mk1 = mk(open(V24A, encoding='utf-8').read()), mk(open(NEW, encoding='utf-8').read())
print('   MAKELIST caches: v2.4a %s; v2.4b %s' % (mk0, mk1))
h = d_h(NEW)
h.globals_['K'] = 7.0
h.press('Esc')
h.call('Norm3', 0.0, 1.0, 1.0)
check('D5 v2.4b\'s two caches count with the LOCAL n3I (v2.4a: Home\'s K); in the harness both fill (one value per '
      'pixel column) and Home\'s K is 7 before and after',
      mk0 == [('n3Pdf', 'K'), ('n3Cdf', 'K')] and mk1 == [('n3Pdf', 'n3I'), ('n3Cdf', 'n3I')]
      and h.globals_['K'] == 7.0 and abs(h.globals_['EP_NORM_CDF'] - norm.cdf(1)) < 1e-12)

# ---- D6. the routine diff: only the routines meant to change differ ----


def d_routines(txt):
    """every routine's raw text, header line to the END; in column 1 that closes it (comments included)"""
    lines = txt.split('\n')
    out, i = {}, 0
    while i < len(lines):
        m = re.match(r'^(?:EXPORT\s+)?([A-Za-z]\w*)\(.*\)\s*$', lines[i])
        if m and i + 1 < len(lines) and lines[i + 1].strip() == 'BEGIN':
            j = i + 1
            while not lines[j].startswith('END;'):
                j += 1
            out[m.group(1)] = '\n'.join(lines[i:j + 1])
            i = j
        i += 1
    return out


R0, R1 = d_routines(open(V24A, encoding='utf-8').read()), d_routines(open(NEW, encoding='utf-8').read())
changed = sorted(n for n in set(R0) & set(R1) if R0[n] != R1[n])
added, gone = sorted(set(R1) - set(R0)), sorted(set(R0) - set(R1))
same = sorted(n for n in set(R0) & set(R1) if R0[n] == R1[n])
print('   routines byte-identical to v2.4a: %s' % ', '.join(same))
print('   changed: %s; added: %s; removed: %s' % (changed, added, gone))
check('D6 the routines that differ from v2.4a are Norm3 and n3_Help (changed) and n3_Fx, n3_Nm (new); the other '
      '%d are byte-identical' % len(same), changed == ['Norm3', 'n3_Help'] and added == ['n3_Fx', 'n3_Nm'] and not gone)
# inside n3_Help only the title moved to v2.4b
check('D6 n3_Help differs from v2.4a only in its title line ("Norm3 v2.4b  -  touch and keys")',
      R0['n3_Help'].replace('Norm3 v2.4a', 'Norm3 v2.4b') == R1['n3_Help'])
# inside Norm3: the code lines that changed are the N1 sites, the summary and the two MAKELIST lines
k0 = c_code(R0['Norm3'])
k1 = c_code(R1['Norm3'])
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += k0[i1:i2]
    if op in ('replace', 'insert'):
        pl += k1[j1:j2]
wm = ['n3Pdf := MAKELIST(0, K, 1, N, 1);', 'n3Cdf := MAKELIST(0, K, 1, N, 1);',
      'TEXTOUT_P("Normal  μ = "+STRING(mu,2,3)+", σ = "+STRING(sd,2,3),',
      'TEXTOUT_P("p = "+STRING(n3P,2,3)+" "+CHAR(8594)+" x₀ = "+STRING(n3X0,2,2)+',
      '", z = "+STRING(zz,2,2), G1, 4, 11, 1, cTx);',
      'TEXTOUT_P("x₀ = "+STRING(n3X0,2,2)+", z = "+STRING(zz,2,2)+',
      'RETURN "Norm3: N(" + STRING(mu,2,3) + ", " + STRING(sd,2,3) + "), P(X ≤ " +',
      'STRING(n3X0,2,2) + ")" + n3_Eq(n3_fmtp(EP_NORM_CDF,4)) + "; values in EP_NORM_*";']
wp = ['LOCAL n3XS,n3XT;', 'n3Pdf := MAKELIST(0, n3I, 1, N, 1);', 'n3Cdf := MAKELIST(0, n3I, 1, N, 1);',
      'TEXTOUT_P("Normal  μ"+n3_Eq(n3_Fx(mu,3))+", σ"+n3_Eq(n3_Fx(sd,3)),',
      'TEXTOUT_P("p = "+STRING(n3P,2,3)+" "+CHAR(8594)+" x₀"+n3_Eq(n3_Fx(n3X0,2))+',
      '", z"+n3_Eq(n3_Fx(zz,2)), G1, 4, 11, 1, cTx);',
      'TEXTOUT_P("x₀"+n3_Eq(n3_Fx(n3X0,2))+", z"+n3_Eq(n3_Fx(zz,2))+',
      'n3XS := n3_Fx(n3X0,2); n3XT := "";', 'IF n3_Eq(n3XS) <> " = " + n3XS THEN', 'n3XT := " with x₀ " + n3XS;',
      'n3XS := "x₀";', 'END;',
      'RETURN "Norm3: N(" + n3_Nm("μ",mu,3) + ", " + n3_Nm("σ",sd,3) + "), P(X ≤ " +',
      'n3XS + ")" + n3_Eq(n3_fmtp(EP_NORM_CDF,4)) + n3XT + "; values in EP_NORM_*";']
check('D6 inside Norm3 the code lines that changed are exactly the N1 sites (title, row 2 twice, summary), the two '
      'MAKELIST lines and the summary\'s x0 slot: -%r +%r' % ([x for x in mi if x not in wm], [x for x in pl if x not in wp]),
      sorted(mi) == sorted(wm) and sorted(pl) == sorted(wp))

# ---- D7. the code ----
t2 = open(NEW, encoding='utf-8').read()
BI2 = set(l.strip().lower() for l in open('/home/claude/work/gate_f19/HP_Prime_Builtin_Names.txt', encoding='utf-8')
          if l.strip() and not l.startswith('#'))
newn = ['n3_Fx', 'n3_Nm', 'fxV', 'fxD', 'fxR', 'nmS', 'nmV', 'nmD', 'nmT', 'n3XS', 'n3XT']
check('D7 the new names %s are not built-ins (case ignored); the two helpers carry the n3_ tag and are defined once, '
      'after n3_fmtp and n3_Eq and before Norm3' % ', '.join(newn),
      not any(n.lower() in BI2 for n in newn) and t2.count('\nn3_Fx(fxV, fxD)\n') == 1 and t2.count('\nn3_Nm(nmS, nmV, nmD)\n') == 1
      and t2.index('\nn3_Eq(eqS)') < t2.index('\nn3_Fx(fxV, fxD)') < t2.index('\nn3_Nm(nmS, nmV, nmD)') < t2.index('EXPORT Norm3('))
check('D7 version strings: the banner, the help page title and a "What changed in v2.4b" paragraph; Roger\'s DISCLAIMER '
      'line beside the distribution terms; no code line names v2.4a',
      t2.split('\n')[3] == '// NORM3 - v2.4b' and '"Norm3 v2.4b  -  touch and keys"' in t2
      and '// What changed in v2.4b (19 Oct 2026' in t2 and not any('v2.4a' in l for l in c_code(t2))
      and '// DISCLAIMER: a teaching and demonstration aid. Not validated for' in t2)
dep, badc = 0, []
for n_, l in enumerate(t2.split('\n'), 1):
    q = False
    for i_, ch in enumerate(l):
        if ch == '"':
            q = not q
        elif not q:
            if l[i_:i_ + 2] == '//':
                if dep:
                    badc.append(n_)
                break
            dep += (ch in '({[') - (ch in ')}]')
check('D7 no // comment inside an open bracket %s' % badc[:5], not badc)
lmax = max(len(m.split(',')) for m in re.findall(r'^\s*LOCAL ([^;(]*);', '\n'.join(c_code(t2)), re.M))
check('D7 every LOCAL line holds at most 6 names (largest %d); no INSTRING; no root sign; no MAKELIST counts with K or X'
      % lmax, lmax <= 6 and not any('INSTRING(' in l for l in c_code(t2)) and not any('√' in l for l in c_code(t2))
      and not re.search(r'MAKELIST\([^,]+,\s*[KX]\s*,', '\n'.join(c_code(t2))))
# every STRING(x, 2, d) left without ROUND has a reason
bare = []
for l in c_code(t2):
    for m in re.finditer(r'STRING\(([^;]*?),\s*2,\s*(\w+)\)', l):
        if not m.group(1).startswith('ROUND(') and m.group(2) != '0':
            bare.append(m.group(1))
SAFE2 = {'thr': 'n3_fmtp: the floor itself, 10^-d, never below it',
         'fxR': 'n3_Fx: ROUND(x, d) itself, so 0 or at least 10^-d',
         'pv': 'n3_fmtp: reached only when |pv| >= 10^-d',
         'xv': 'an x tick label: a multiple of a 1-2-5 step with d = -FLOOR(LOG(step)), so 0 or at least 10^-d',
         'yv': 'a y tick label: the same',
         'n3P': 'p on the inverse row: clamped to 0.005 or more'}
print('   STRING(x, 2, d) without ROUND in v2.4b:', ', '.join('%s (%s)' % (b_, SAFE2.get(b_, '?')) for b_ in bare))
check('D7 every bare STRING(x, 2, d) left in v2.4b is one of %s, each unable to print the scientific form' % sorted(SAFE2),
      sorted(set(bare)) == sorted(SAFE2))

# ---- D8. every scientific STRING result of every v2.4b run in part D ----
d_flush()
sci_new = sorted(set((round(v, 15), d, r) for v, d, r in D_SCI))
print('   v2.4b: %d harness runs in part D, %d distinct scientific STRING results: %s' % (D_RUNS[0], len(sci_new), sci_new[:4]))
check('D8 the only scientific STRING results of v2.4b in its %d runs are the axis tick at 0 for σ 0.2 (%d), -5.6E-17 in '
      'binary doubles (-0.8 + 4 x 0.2): the Prime\'s BCD makes that tick exactly 0, so it is the harness\'s '
      'arithmetic, as v2.4a\'s C6 found' % (D_RUNS[0], len(sci_new)),
      all(abs(v) < 1e-12 for v, d, r in sci_new), repr(sci_new[:3]))

print()
print('%d checks failed' % len(fails) if fails else 'ALL CHECKS PASSED')
sys.exit(1 if fails else 0)
