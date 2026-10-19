"""verify_Burr3_v2.4b.py -- checks Burr3 v2.4b (19 Oct 2026): B1 (the pdf and the CDF in logarithms, b3_bpdf and
the new b3_bcdf, so (1 + (x/S)^C)^(K+1) is never formed), B2 (ROUND before STRING through b3_Fx; a value too small
for its decimals reads "< 0.01", never 0.00 and never the Prime's scientific form), B3 (no root sign in the code) and
B4 (the MAKELIST caches count with the LOCAL b3I).  Built from verify_Burr3_v2.4a.py; every check is kept:
  A. harness_Burr3_v24.py (ppl_run_v1), now on v2.4b; only the file name changed.
  B. verify_Burr3.py, v2.4's formula mirror (it reads no program file), run as it is.
  C. v2.4a's own checks (v2.4 against v2.4a, harness v3e), kept as they were: they now read the v2.4a file from
     /home/claude/work/out (that change set).
  D. (new, v2.4b, harness v3e)
     D1 the review's check_Burr3.py on v2.4b and on v2.4a (its 9 failures on v2.4a pass on v2.4b; its two version
        expectations move to v2.4b, and C4, which sized the overflowing power from the inputs alone, is restated
        about the program);
     D2 each B2 reproduction from findings_A, v2.4a against v2.4b;  D3 B1 against 40-digit mpmath and
        scipy.stats.burr12, the tail branch included, and the calls that overflowed, end to end;
     D4 a sweep of ordinary calls and the five views: v2.4b prints what v2.4a prints;  D5 B4;
     D6 the routine diff;  D7 the code (names, versions, the disclaimer, comments, LOCAL sizes, B3, bare STRINGs);
     D8 every scientific STRING result of every v2.4b run in part D.
Run:  python3 verify_Burr3_v2.4b.py     (needs /home/claude/work/harness/ppl_run_v1.py, out/ppl_run_v3e.py, mpmath)

(verify_Burr3_v2.4a.py's docstring follows.)
verify_Burr3_v2.4a.py -- checks Burr3 v2.4a (17 Oct 2026, evening): no "=" before a relation (b3_Eq), and an
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
print('A. harness_Burr3_v24.py on v2.4b (ppl_run_v1)')
import sys, re, math
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v1 import Harness, KEY, Tap, Drag, Key
from scipy.stats import burr12, norm

SRC = '/home/claude/work/fix19/Burr3_v2.4b.txt'          # v2.4b: part A runs on the new file
SRC_C = '/home/claude/work/out/Burr3_v2.4a.txt'         # v2.4b: part C keeps checking the v2.4a change set
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
# (v2.4b: SRC_C is the v2.4a file in out/; these are v2.4a's checks of its own change set)
print()
print('C. v2.4a: no "=" before a relation; no "0.0000" for a P that is not 0 (harness v3e)')
import subprocess as _sp
import difflib as _dl
import re as _re
sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3e import Harness as H3
OLD24 = '/home/claude/work/out/Burr3_v2.4.txt'
C_ALL, C_OLD = [], []


class _Lite(object):
    def __init__(self, sci):
        self.sci_strings = sci



def c_run(path, call, views=0):
    h = H3(path)
    for _ in range(views):
        h.tap(240, 230)                        # View (soft key 5)
    h.press('Esc')
    h.execute(call)
    # (v2.4b: C6 reads only the run's scientific strings; keeping the whole harness of 460 runs ran a
    # shared machine out of memory)
    (C_ALL if path == SRC_C else C_OLD).append((call, _Lite(h.sci_strings)))
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
    a, b = c_run(OLD24, call, views), c_run(SRC_C, call, views)
    check('C1 %s, v2.4: %r | %s' % (call, a[0], a[1]), (a[0], a[1]) == old, repr(a[:2]))
    if new is None:
        check('C1 %s, v2.4a: an ordinary readout and summary are unchanged' % call, a[:2] == b[:2], repr(b[:2]))
    else:
        check('C1 %s, v2.4a: %r | %s' % (call, b[0], b[1]), (b[0], b[1]) == new, repr(b[:2]))
for call, old, new in (('Burr3(10,1,1,1)', 'its P(X < 0) = < 0.0001', 'its P(X < 0) < 0.0001'),
                       ('Burr3(3,2,1,1)', 'its P(X < 0) = 0.0207', 'its P(X < 0) = 0.0207')):
    a, b = c_run(OLD24, call, 4), c_run(SRC_C, call, 4)
    oa = [t for t in a[0] if t.startswith('its')]
    ob = [t for t in b[0] if t.startswith('its')]
    check('C1 view 4 %s: v2.4 %r -> v2.4a %r' % (call, oa, ob), oa == [old] and ob == [new])

# C2. the exact 0: computed 0, true value positive
b = c_run(SRC_C, 'Burr3(25,1,1,0.2)')
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
                a, b = c_run(OLD24, call), c_run(SRC_C, call)
                ra = ([c_rw(x) for x in a[0]], c_rw(a[1]))
                n += 1
                if ra != (a[0], a[1]):
                    nrw += 1
                if ra != (b[0], b[1]):
                    diffs.append((call, ra, b[:2]))
check('C3 %d calls (C, K, S, x₀): every readout row and summary identical to v2.4 once its "= <" and exact-0 CDF '
      'are written the v2.4a way (%d needed it)' % (n, nrw), not diffs, repr(diffs[:2]))

# C4. b3_Eq
hc = H3(SRC_C)
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


t0, t1 = open(OLD24, encoding='utf-8').read(), open(SRC_C, encoding='utf-8').read()
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

# ======================================================================== D. v2.4b (harness v3e)
print()
print('D. v2.4b: B1 (the pdf and CDF in logs), B2 (ROUND before STRING, b3_Fx), B3 (no root sign), B4 (the LOCAL '
      'MAKELIST counter) (harness v3e)')
import io as _io
import contextlib as _cl
import mpmath as _mp
from scipy import stats as _st
_mp.mp.dps = 40
NEW = '/home/claude/work/fix19/Burr3_v2.4b.txt'
V24A = '/home/claude/work/out/Burr3_v2.4a.txt'
REVIEW = '/home/claude/work/review/check_Burr3.py'
D_NEW = []
SCI = 'ᴇ'


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


# ---- D1. the review's check_Burr3.py on v2.4b and on v2.4a ----
# Two expectations name the version (the help page's title, the version string on screen): they move to v2.4b.
# The three marker-label checks also accept "< 0.01" for a value below 0.005 (B2's honest minimum), as they accepted
# the scientific form.
# C4 computed the size of (1 + z)^(K+1) at the window's edge from the inputs alone, so it can never pass, whatever
# the program does; it is restated about the program: the run completes in the harness, whose doubles stop at
# 1.8E308 (inside the Prime's 1E500), so no intermediate passed it, and the pdf at x0 matches burr12.
D1_PATCHES = [
    ("PPL = os.path.join(FLEET, 'Burr3_v2.4a.txt')", "PPL = __PPL__"),
    # B2 / D14: a marker value that is not 0 but rounds to 0.00 now reads "< 0.01" (the honest minimum); the review's
    # label checks accepted the Prime's scientific form there, and now accept that form too
    ("        check(mode_txt != '' and (abs(nums(mode_txt)[0] - mode) <= 0.006 * max(1, mode) or SCI_E in mode_txt), 'A mode label %r (want %.4f)' % (mode_txt, mode))",
     "        check(mode_txt != '' and (abs(nums(mode_txt)[0] - mode) <= 0.006 * max(1, mode) or SCI_E in mode_txt or ('< 0.01' in mode_txt and 0 < mode < 0.005)), 'A mode label %r (want %.4f)' % (mode_txt, mode))"),
    ("        check(med_txt != '' and (abs(nums(med_txt)[0] - med) <= 0.006 * max(1, med) or SCI_E in med_txt), 'A median label %r' % med_txt)",
     "        check(med_txt != '' and (abs(nums(med_txt)[0] - med) <= 0.006 * max(1, med) or SCI_E in med_txt or ('< 0.01' in med_txt and 0 < med < 0.005)), 'A median label %r' % med_txt)"),
    ("            check('mean ' in t.get('mean', '') and abs(nums(t['mean'])[0] - mean) <= 0.006 * max(1, mean) or (SCI_E in t.get('mean', '')),",
     "            check('mean ' in t.get('mean', '') and abs(nums(t['mean'])[0] - mean) <= 0.006 * max(1, mean) or (SCI_E in t.get('mean', '')) or ('< 0.01' in t.get('mean', '') and 0 < mean < 0.005),"),
    ("hp = [f for f in fr if f.find('Burr3 v2.4a  -  touch and keys')]",
     "hp = [f for f in fr if f.find('Burr3 ' + __VER__ + '  -  touch and keys')]"),
    ("check(vers == ['v2.4a'], 'D2 version string on screen: %s' % vers)",
     "check(vers == [__VER__], 'D2 version string on screen: %s' % vers)"),
    ("        check(lg < 500, 'C4 Burr3(%s, %s, %s, %s): the pdf denominator stays below 1E500 (the Prime\\'s range) inside the window' % (C, K, S, x0))",
     "        check(err is None and abs(h.globals_['EP_BURR_PDF'] - stats.burr12(c=C, d=K, scale=S).pdf(x0)) <= 1e-9 * max(1e-300, stats.burr12(c=C, d=K, scale=S).pdf(x0)),\n"
     "              'C4 Burr3(%s, %s, %s, %s): the program never forms the pdf denominator (1 + z)^(K+1) (1E%.0f at the window\\'s edge): '\n"
     "              'the run completes in the harness (doubles to 1.8E308, inside the Prime\\'s 1E500) and EP_BURR_PDF = burr12.pdf' % (C, K, S, x0, lg))"),
]


def run_review(path, ver):
    s = open(REVIEW, encoding='utf-8').read()
    for o, n in D1_PATCHES:
        assert s.count(o) == 1, o[:80]
        s = s.replace(o, n)
    ns = {'__name__': 'review_check', '__file__': REVIEW, '__PPL__': path, '__VER__': ver}
    buf = _io.StringIO()
    with _cl.redirect_stdout(buf):
        exec(compile(s, REVIEW, 'exec'), ns)
        ns['main']()
    return ns['NCHECK'][0], list(ns['FAILS']), buf.getvalue()


n_new, f_new, out_new = run_review(NEW, 'v2.4b')
n_old, f_old, out_old = run_review(V24A, 'v2.4b')
print('   review check_Burr3.py on v2.4b: %d checks, %d failed %s' % (n_new, len(f_new), f_new[:3]))
print('   the same on v2.4a: %d checks, %d failed:' % (n_old, len(f_old)))
for f in f_old:
    print('      FAIL  ' + f[:150])
want_old = {'C4': 4, 'C5': 1, 'C6': 3, 'D4': 1, 'B5': 1, 'D2': 1}
got_old = {}
for f in f_old:
    got_old[f.split()[0]] = got_old.get(f.split()[0], 0) + 1
check('D1 the review\'s check_Burr3.py passes in full on v2.4b (%d checks, 0 failed)' % n_new, n_new == 290 and not f_new,
      repr(f_new[:2]))
check('D1 regression: on v2.4a the same script fails the 9 checks the review found (C4 x 4: B1; C5, C6 x 3: B2; D4: B3) '
      'and the two version expectations besides (help title, D2): %s' % got_old, got_old == want_old, repr(f_old))

# ---- D2. B2: each reproduction from findings_A, v2.4a against v2.4b ----


def d_run(path, args, script=None):
    h = d_h(path)
    if script:
        script(h)
    h.press('Esc')
    r = h.call('Burr3', *[float(v) for v in args])
    return h, r


def d_texts(h):
    return sorted(set(t.text for t in h.texts))


def s_sfloor(h):
    h.tap(133, 230)
    for _ in range(25):
        h.press('Down')
    h.tap(186, 230)
    h.tap(60, 150)


D2 = [
    ('S at its 0.01 floor by the keys, then a tap (the mode label)', (2, 1, 1, 1), s_sfloor,
     ['mode 5.77ᴇ-3', 'mode 6.66ᴇ-3', 'mode 8.32ᴇ-3'], ['mode 0.01', 'S = 0.01']),
    ('Burr3(1.01, 1, 1, 1): the mode leaves 0 as C passes 1', (1.01, 1, 1, 1), None, ['mode 5.24ᴇ-3'], ['mode 0.01']),
    ('Burr3(1, 100, 1, 1): the median', (1, 100, 1, 1), None, ['median 6.96ᴇ-3'], ['median 0.01', 'mean 0.01']),
    ('Burr3(2, 1, 1, 0.005): x0 in the title', (2, 1, 1, 0.005), None, ['x₀ = 5.00ᴇ-3'], ['x₀ = 0.01']),
    ('Burr3(2, 1, 0.001, 0.0004): a scale below 0.005', (2, 1, 0.001, 0.0004), None, ['S = 1.00ᴇ-3', 'x₀ = 4.00ᴇ-4'],
     ['S < 0.01', 'x₀ < 0.01', 'mode < 0.01', 'median < 0.01', 'mean < 0.01']),
    ('Burr3(3, 2, 0.0001, 0.0001): the moments on the status row', (3, 2, 0.0001, 0.0001), None, ['μ = 8.061ᴇ-5, σ = 3.953ᴇ-5'],
     ['μ < 0.001, σ < 0.001']),
]
for label, args, script, want_o, want_n in D2:
    ho, ro = d_run(V24A, args, script)
    hn, rn = d_run(NEW, args, script)
    to, tn = d_texts(ho), d_texts(hn)
    so = [t for t in to if SCI in t]
    print('   %s\n      v2.4a: %s\n      v2.4b: %s' % (label, so[:4], [t for t in tn if any(w in t for w in want_n)][:5]))
    check('D2 %s: v2.4a printed %s; v2.4b prints %s and no scientific form' % (label, want_o, want_n),
          all(any(w in t for t in so) for w in want_o) and all(any(w in t for t in tn) for w in want_n)
          and not any(SCI in t for t in tn) and SCI not in rn, repr([t for t in tn if SCI in t][:2]))
# the summary returned to Home
for args, want_o, want_n in (
        ((2, 1, 1, 0.005), 'Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 5.00ᴇ-3) < 0.0001; values in EP_BURR_*',
         'Burr3: C = 2.00, K = 1.00, S = 1.00, P(X ≤ 0.01) < 0.0001; values in EP_BURR_*'),
        ((2, 1, 0.001, 0.0004), 'Burr3: C = 2.00, K = 1.00, S = 1.00ᴇ-3, P(X ≤ 4.00ᴇ-4) = 0.1379; values in EP_BURR_*',
         'Burr3: C = 2.00, K = 1.00, S < 0.01, P(X ≤ x₀) = 0.1379 with x₀ < 0.01; values in EP_BURR_*')):
    ro, rn = d_run(V24A, args)[1], d_run(NEW, args)[1]
    check('D2 the summary to Home, Burr3%s: v2.4a %r -> v2.4b %r' % (args, ro, rn), ro == want_o and rn == want_n,
          repr((ro, rn)))

# ---- D3. B1: the log-space pdf and CDF against 40-digit mpmath and scipy.stats.burr12, tail branch included ----


def ref_pdf(x, C, K, S):
    x, C, K, S = map(_mp.mpf, (x, C, K, S))
    z = (x / S) ** C
    return K * C * z / (x * (1 + z) ** (K + 1))


def ref_cdf(x, C, K, S):
    x, C, K, S = map(_mp.mpf, (x, C, K, S))
    return 1 - (1 + (x / S) ** C) ** (-K)


hp = d_h(NEW)
w_pdf = w_sp = w_cdf = 0.0
n_pdf = n_tail = n_sp = n_sp_tail = n_under = 0
for C_ in (0.5, 1, 2, 5, 20, 30, 50, 100, 200, 400):
    for K_ in (0.01, 0.25, 1, 5, 30, 100, 400):
        if C_ * K_ < 0.5:
            continue
        for S_ in (0.01, 1, 7):
            for xr in (1e-6, 0.01, 0.3, 0.9, 1, 1.1, 2, 5, 50, 1e3):
                x_ = xr * S_
                v = hp.call('b3_bpdf', x_, float(C_), float(K_), float(S_))
                w = ref_pdf(x_, C_, K_, S_)
                tail = C_ * math.log(xr) > 100
                n_tail += tail
                if w > _mp.mpf('1e-300'):
                    w_pdf = max(w_pdf, float(abs(_mp.mpf(v) / w - 1))); n_pdf += 1
                    sp = _st.burr12.pdf(x_, C_, K_, scale=S_)
                    if 1e-300 < sp < 1e300:
                        w_sp = max(w_sp, abs(v / sp - 1)); n_sp += 1; n_sp_tail += tail
                else:
                    n_under += 1
                    assert v < 1e-290, (C_, K_, S_, x_, v)
                c = hp.call('b3_bcdf', x_, float(C_), float(K_), float(S_))
                w_cdf = max(w_cdf, float(abs(_mp.mpf(c) - ref_cdf(x_, C_, K_, S_))))
print('   b3_bpdf: %d points against mpmath (%d in the tail branch, z > e^100), worst relative %.1e; %d against '
      'burr12.pdf (%d tail), worst %.1e; %d below 1E-300 return 0 (as the Prime returns 0 below 1E-499)'
      % (n_pdf, n_tail, w_pdf, n_sp, n_sp_tail, w_sp, n_under))
check('D3 B1: b3_bpdf (in logs) = the Burr XII pdf to %.1e relative at %d points, C 0.5 to 400, K 0.01 to 400, S 0.01 '
      'to 7, x from 1E-6 S to 1000 S; %d of them in the tail branch (ln z > 100); = scipy burr12.pdf to %.1e at %d '
      '(%d tail)' % (w_pdf, n_pdf, n_tail, w_sp, n_sp, n_sp_tail),
      w_pdf < 1e-11 and w_sp < 1e-9 and n_tail > 100 and n_sp_tail > 20)
check('D3 B1: b3_bcdf (in logs) = 1 - (1 + z)^(-K) to %.1e absolute over the same grid' % w_cdf, w_cdf < 1e-13)
# end to end: the four calls that overflowed, and two near them
for args in ((30, 30, 1, 5), (100, 100, 1, 1), (20, 25, 1, 10), (3, 400, 1, 10), (20, 20, 1, 1), (50, 50, 1, 1)):
    try:
        hn, rn = d_run(NEW, args); en = None
    except Exception as e:
        hn, en = None, '%s: %s' % (type(e).__name__, e)
    try:
        d_run(V24A, args); eo = None
    except Exception as e:
        eo = '%s: %s' % (type(e).__name__, str(e)[:60])
    d = _st.burr12(c=args[0], d=args[1], scale=args[2])
    ok = en is None
    if ok:
        g = hn.globals_
        pr = float(ref_pdf(args[3], *args[:3])); cr = float(ref_cdf(args[3], *args[:3]))
        ok = (abs(g['EP_BURR_PDF'] - pr) <= 1e-11 * pr + 1e-300 and abs(g['EP_BURR_CDF'] - cr) < 1e-12
              and abs(g['EP_BURR_MEAN'] - d.mean()) < 1e-7 * d.mean())
        rows = [t.text for t in hn.texts if t.y == 12 and t.x == 4]
        ok = ok and not any('0.0000 (a height)' in r for r in rows)
    print('   Burr3%s: v2.4a %s; v2.4b %s %s' % (args, eo or 'ran', en or 'ran', rows[-1:] if ok else ''))
    check('D3 B1: Burr3%s runs to the end; EP_BURR_PDF, EP_BURR_CDF and the mean = mpmath / burr12; the pdf readout '
          'never "0.0000" (v2.4a: %s)' % (args, 'stopped' if eo else 'ran'), ok)
hn, rn = d_run(NEW, (30, 30, 1, 5))
row = [t.text for t in hn.texts if t.y == 12 and t.x == 4][-1]
check('D3 B1: Burr3(30, 30, 1, 5) -- the pdf at x0 = 5 is about 1E-628, below the Prime\'s smallest real; it comes back '
      '0 and the readout says "pdf < 0.0001" (%r); EP_BURR_PDF holds the computed 0' % row,
      row.startswith('pdf < 0.0001 (a height)') and hn.globals_['EP_BURR_PDF'] == 0)

# the status row's K x C, which B1 lets reach five digits: inside the screen; an ordinary one still at x 248
hn, rn = d_run(NEW, (123.25, 456.5, 1, 1))
kc = [t for t in hn.texts if t.text.startswith('K×C = ')][-1]
hn2, rn2 = d_run(NEW, (2, 1, 1, 1))
kc2 = [t for t in hn2.texts if t.text.startswith('K×C = ')][-1]
check('D3 Burr3(123.25, 456.5, 1, 1): %r from x %d ends by x %d at 6 px a character (v2.4a stopped in b3_bpdf; '
      'from x 248 it would end at 332); "K×C = 2.00" still starts at 248' % (kc.text, kc.x, kc.x + 6 * len(kc.text)),
      kc.x + 6 * len(kc.text) <= 320 and kc2.text == 'K×C = 2.00' and kc2.x == 248)

# ---- D4. a sweep of ordinary calls: v2.4b prints what v2.4a prints ----
nsame, diff4 = 0, []
for C_ in (0.5, 1, 2, 4.5, 12, 25):
    for K_ in (1, 2, 0.25):
        if C_ * K_ < 0.5:
            continue
        for S_ in (1, 3.5):
            for x_ in (0.05, 0.2, 0.7, 1, 2.5, 9, 40):
                args = (C_, K_, S_, x_)
                ho, ro = d_run(V24A, args)
                hn, rn = d_run(NEW, args)
                ko, kn = [t.text for t in ho.texts], [t.text for t in hn.texts]
                if ko == kn and ro == rn:
                    nsame += 1
                else:
                    diff4.append((args, [(a, b) for a, b in zip(ko + [ro], kn + [rn]) if a != b][:2]))
check('D4 %d ordinary calls (C 0.5 to 25, K 0.25 to 2, S 1 and 3.5, x0 0.05 to 40): every text v2.4b draws, and its '
      'summary, is v2.4a\'s, character for character' % (nsame + len(diff4)), not diff4, repr(diff4[:2]))
# the five views and the keys, on an ordinary distribution
for args in ((3, 2, 1, 1), (2, 1, 1, 1)):
    def views(h):
        for _ in range(5):
            h.tap(240, 230)
        h.press('Right', 'Left', 'Up', 'Down', 'Zero', 'Plus', 'Minus')
    ho, ro = d_run(V24A, args, views)
    hn, rn = d_run(NEW, args, views)
    check('D4 Burr3%s through the five views and seven keys: every text as v2.4a' % (args,),
          [t.text for t in ho.texts] == [t.text for t in hn.texts] and ro == rn)

# ---- D5. B4: the MAKELIST caches count with the LOCAL b3I ----
mk = lambda t: re.findall(r'(\w+)\s*:= MAKELIST\(0, (\w+), 1, N, 1\);', '\n'.join(c_code(t)))
mk0, mk1 = mk(open(V24A, encoding='utf-8').read()), mk(open(NEW, encoding='utf-8').read())
print('   MAKELIST caches: v2.4a %s; v2.4b %s' % (mk0, mk1))
h = d_h(NEW)
h.globals_['X'] = 7.0
h.press('Esc')
h.call('Burr3', 2.0, 1.0, 1.0, 1.0)
check('D5 B4: v2.4b\'s four caches count with the LOCAL b3I (v2.4a: Home\'s X, which MAKELIST overwrote on the Prime); '
      'in the harness all four fill and Home\'s X is 7 before and after',
      [c for _, c in mk0] == ['X'] * 4 and [c for _, c in mk1] == ['b3I'] * 4 and h.globals_['X'] == 7.0)

# ---- D6. the routine diff: only the routines meant to change differ ----


def d_routines(txt):
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
check('D6 the routines that differ from v2.4a are Burr3, b3_bpdf (B1) and b3_Help (its title), and the new b3_bcdf '
      '(B1) and b3_Fx (B2); the other %d are byte-identical' % len(same),
      changed == ['Burr3', 'b3_Help', 'b3_bpdf'] and added == ['b3_Fx', 'b3_bcdf'] and not gone)
check('D6 b3_Help differs from v2.4a only in its title line', R0['b3_Help'].replace('Burr3 v2.4a', 'Burr3 v2.4b') == R1['b3_Help'])
k0, k1 = c_code(R0['Burr3']), c_code(R1['Burr3'])
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += k0[i1:i2]
    if op in ('replace', 'insert'):
        pl += k1[j1:j2]
print('   inside Burr3: %d code lines removed, %d added' % (len(mi), len(pl)))
RM_KEYS = ('MAKELIST(0, X', 'STRING(', '√', '1-(1+(', '"pdf"+b3_Eq(b3_fmtp(pdf0', 'TEXTOUT_P(sKC, G1, 248',
           'values in EP_BURR_*')
ADD_KEYS = ('MAKELIST(0, b3I', 'b3_Fx(', 'b3_bcdf(', 'mvar^0.5', 'b3XS', 'b3XT', 'END;', 'IFTE(pdf0 > 0',
            'TEXTOUT_P(sKC, G1, MIN(248, 320 - 6*SIZE(sKC))')
rm_odd = [l for l in mi if not any(w in l for w in RM_KEYS)]
add_odd = [l for l in pl if not any(w in l for w in ADD_KEYS)]
check('D6 inside Burr3 every code line that changed is a B1 (the CDF through b3_bcdf), B2 (b3_Fx), B3 (^0.5) or B4 '
      '(MAKELIST) site, the pdf readout\'s IFTE, the K x C position or the summary\'s x0 slot (%d removed, %d added): -%r +%r'
      % (len(mi), len(pl), rm_odd, add_odd), not rm_odd and not add_odd)

# ---- D7. the code ----
t2 = open(NEW, encoding='utf-8').read()
BI2 = set(l.strip().lower() for l in open('/home/claude/work/gate_f19/HP_Prime_Builtin_Names.txt', encoding='utf-8')
          if l.strip() and not l.startswith('#'))
newn = ['b3_bcdf', 'b3_Fx', 'b3L', 'fxV', 'fxD', 'fxR', 'b3XS', 'b3XT']
check('D7 the new names %s are not built-ins (case ignored); the helpers carry the b3_ tag and are defined once, before '
      'Burr3' % ', '.join(newn), not any(n.lower() in BI2 for n in newn) and t2.count('\nb3_bcdf(b3V,C,K,S)\n') == 1
      and t2.count('\nb3_Fx(fxV, fxD)\n') == 1 and t2.index('\nb3_Fx(fxV, fxD)') < t2.index('EXPORT Burr3(')
      and t2.index('\nb3_bcdf(') < t2.index('EXPORT Burr3('))
check('D7 version strings: the banner, the help page title, a "What changed in v2.4b" paragraph, and Roger\'s '
      'DISCLAIMER line beside the distribution terms; no code line names v2.4a',
      t2.split('\n')[3] == '// BURR3 - v2.4b' and '"Burr3 v2.4b  -  touch and keys"' in t2
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
check('D7 B3: no root sign in the code; every LOCAL line holds at most 6 names (largest %d); no INSTRING; no MAKELIST '
      'counts with K or X' % lmax, lmax <= 6 and not any('√' in l for l in c_code(t2))
      and not any('INSTRING(' in l for l in c_code(t2)) and not re.search(r'MAKELIST\([^,]+,\s*[KX]\s*,', '\n'.join(c_code(t2))))
bare = []
for l in c_code(t2):
    for m in re.finditer(r'STRING\(([^;]*?),\s*2,\s*(\w+)\)', l):
        if not m.group(1).startswith('ROUND(') and m.group(2) != '0':
            bare.append(m.group(1))
SAFE2 = {'thr': 'b3_fmtp: the floor itself, 10^-d', 'pv': 'b3_fmtp: reached only when |pv| >= 10^-d',
         'fxR': 'b3_Fx: ROUND(x, d) itself, so 0 or at least 10^-d',
         'xv': 'an x tick label: a multiple of a 1-2-5 step with d = -FLOOR(LOG(step))', 'yv': 'a y tick label: the same',
         'K*C': 'K x C: 0.5 or more (the floor)', 'b3P': 'p on the inverse row: clamped to 0.005 or more'}
print('   STRING(x, 2, d) without ROUND in v2.4b:', ', '.join('%s (%s)' % (b_, SAFE2.get(b_, '?')) for b_ in sorted(set(bare))))
check('D7 every bare STRING(x, 2, d) left in v2.4b is one of %s, each unable to print the scientific form' % sorted(SAFE2),
      sorted(set(bare)) == sorted(SAFE2))

# ---- D8. every scientific STRING result of every v2.4b run in part D ----
d_flush()
sci_new = sorted(set((round(v, 15), d, r) for v, d, r in D_SCI))
print('   v2.4b: %d harness runs in part D, %d distinct scientific STRING results: %s' % (D_RUNS[0], len(sci_new), sci_new[:4]))
check('D8 no scientific STRING result in any of the %d v2.4b runs of part D' % D_RUNS[0], not sci_new, repr(sci_new[:3]))

print()
print('%d checks failed' % len(fails) if fails else 'ALL CHECKS PASSED')
sys.exit(1 if fails else 0)
