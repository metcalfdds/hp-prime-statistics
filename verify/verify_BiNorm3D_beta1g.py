#!/usr/bin/env python3
"""verify_BiNorm3D_beta1g.py -- checks BiNorm3D beta 1g (Round 16, 15 Nov 2026): the target view and the CEP, the circular
error probable: the radius of the circle round the mean that holds half of all (x, y) pairs.  Runs from the repository
alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, beta 1f from git (the commit before
Round 16).  Needs hp-prime-kit (HPKIT), SciPy, NumPy.

  T1  verify/round16/make_binorm3d_1g.py, run again from beta 1f, makes programs/BiNorm3D_beta1g.txt byte for byte.
  A   the arithmetic.  bnCepC, called through the harness (rule 19), against a reference that does not use its formula:
      X^2 + Y^2 = A Z1^2 + B Z2^2 integrated over Z1 by adaptive quadrature with the normal CDF, and the R that holds half
      found by Brent's method; then a simulation of 2,000,000 pairs (a fixed seed).  The ellipse that holds half; the two
      numbers the help page prints; the Home export.
  S   the shots: 50 at a time and 500 at most; the count inside the circle; their correlation; what clears them.
  V   the views, the keys and every way out: key 3 and the menu's item 2 through the three views; what keys 4 and 5 and
      the arrows do in each view; a tap on the plot and beside it; rho at its ends; a cancelled menu; Set rho cancelled,
      refused and accepted; Esc from each view and the line each kind of run returns; Frame timing from the target view.
  R   regression against beta 1f: the 3-D view and the contour view draw the same shapes and texts over a grid of rho,
      angles and slices, and a scripted session of the old features shows the same screens in both versions once the
      target view's screens are taken out.
  H   the help: six pages; pages 1 to 4 are beta 1f's word for word (the page count in the header and footer aside); page
      6 is beta 1f's page 5 with the listed changes; page 5 is new; every line fits its 296 px at the glyph widths
      GlyphProbe_v1 measured; the opening page.
  G   static: no "!="; code ASCII; the menu has 8 items of at most 30 characters; LOCAL lines of at most 6 names.
  D   layout: text_overlap_v1 and label_fit_v1 over every beta 1g screen drawn above: no firm overlap, no cut number.
"""
import os, sys, io, re, json, math, subprocess, tempfile, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness, CANCEL  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import numpy as np  # noqa: E402
from scipy import stats, integrate  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

BASE = '4e8ff66'
PROG = os.path.join('programs', 'BiNorm3D_beta1g.txt')
tmp = tempfile.mkdtemp(prefix='bnv_')
OLD = os.path.join(tmp, 'BiNorm3D_beta1f.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/BiNorm3D_beta1f.txt'], check=True, capture_output=True).stdout)
SRC = io.open(PROG, encoding='utf-8').read()
GW = json.load(open(os.path.join('verify', 'round11', 'glyph_widths_vc.json')))
FAIL, NPASS = [], [0]
RHO, MINUS, X0 = chr(961), chr(8722), 'x' + chr(8320)
K3, K4, K5, K6 = (133, 228), (186, 228), (240, 228), (293, 228)      # soft keys 3 to 6
KM, KP = (26, 228), (80, 228)                                        # rho-, rho+


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:700]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def key(h, name):
    for k in h.globals_:
        if k.lower() == name.lower(): return k
    raise KeyError(name)


def G(h, name): return h.globals_[key(h, name)]
def S(h, name, v): h.globals_[key(h, name)] = v


def fresh(path=PROG, seed=0):
    h = Harness(path, idle_key=4, home_minus=True, seed=seed)
    h.execute('bnInit()')
    return h


def run(script, path=PROG, seed=0):
    """a whole run of BiNorm3D(): the opening page takes the first key, then the script's keys, taps and answers"""
    h = Harness(path, idle_key=4, home_minus=True, seed=seed)
    h.press('Enter')
    script(h)
    try: res = h.execute('BiNorm3D()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
    return h, res, err


def px(text, font=1):
    return sum(GW[str(ord(c))][font - 1] for c in text)


# ---- the reference: a different integral from the program's ----
def p_ref(R, A, B):
    s1, s2 = math.sqrt(A), math.sqrt(B)
    f = lambda z: stats.norm.pdf(z) * (2 * stats.norm.cdf(math.sqrt(max(R * R - A * z * z, 0.0)) / s2) - 1)
    return integrate.quad(f, -R / s1, R / s1, limit=400, epsabs=1e-13, epsrel=1e-13)[0]


def cep_ref(rho):
    A, B = 1 + abs(rho), 1 - abs(rho)
    return brentq(lambda R: p_ref(R, A, B) - 0.5, 0.2, 3, xtol=1e-13)


print('=== T. the build')
out = os.path.join(tmp, 'built')
subprocess.run([sys.executable, os.path.join(HERE, 'round16', 'make_binorm3d_1g.py'), out], check=True, capture_output=True)
check('T1 the build makes programs/BiNorm3D_beta1g.txt byte for byte',
      open(os.path.join(out, 'BiNorm3D_beta1g.txt'), 'rb').read() == open(PROG, 'rb').read())

print('=== A. the arithmetic')
OV.install()
h = fresh(); bad = []; steps = []; REF = {}
rhos = [-0.9, -0.75, -0.5, -0.33, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.47, -0.01]
for r in rhos:
    h.execute('bnSetRho(%r)' % r); h.execute('bnCepC()')
    REF[r] = cep_ref(r); steps.append(G(h, 'bnCpK'))
    if abs(G(h, 'bnCpR') - REF[r]) > 1e-9 or G(h, 'bnCpD') != 0 or abs(G(h, 'BN_CEP') - G(h, 'bnCpR')) > 0: bad.append((r, G(h, 'bnCpR'), REF[r]))
check('A1 bnCepC equals the reference (an integral over Z1 with the normal CDF, Brent\'s method) to 1E-9 at %d values of %s from %s0.9 to 0.9; Newton took %d to %d steps; BN_CEP holds it'
      % (len(rhos), RHO, MINUS, min(steps), max(steps)), not bad and max(steps) <= 8, bad[:3])
h.execute('bnSetRho(0)'); h.execute('bnCepC()')
check('A2 at %s = 0 the CEP is root(2 ln 2) = 1.17741002252 to 12 digits' % RHO, abs(G(h, 'bnCpR') - math.sqrt(2 * math.log(2))) < 1e-12, G(h, 'bnCpR'))
rng = np.random.default_rng(20261115); bad = []
for r in (0.6, -0.9, 0.0):
    z = rng.normal(size=(2000000, 2)); x = z[:, 0]; y = r * z[:, 0] + math.sqrt(1 - r * r) * z[:, 1]
    h.execute('bnSetRho(%r)' % r); h.execute('bnCepC()')
    share = float((x * x + y * y <= G(h, 'bnCpR') ** 2).mean())
    if abs(share - 0.5) > 4 * 0.5 / math.sqrt(2000000): bad.append((r, share))
check('A3 a second reference, a simulation: of 2,000,000 pairs at %s = 0.6, %s0.9 and 0, half land inside the circle (within 4 standard errors)' % (RHO, MINUS), not bad, bad)
bad = []
for r in (0.6, -0.9, 0.0, 0.33):
    h.execute('bnSetRho(%r)' % r); h.execute('bnCepC()')
    ex, ey = G(h, 'bnTEX'), G(h, 'bnTEY')
    for i in range(61):
        xx = (ex[i] - G(h, 'bnCXc')) / G(h, 'bnCU'); yy = (G(h, 'bnCYc') - ey[i]) / G(h, 'bnCU')
        q = (xx * xx - 2 * r * xx * yy + yy * yy) / (1 - r * r)
        # one pixel is 1/27 of a unit: the point may sit half a pixel from the true ellipse in x and in y
        t = 2 * math.pi * i / 60; a, b = math.sqrt(1 + r), math.sqrt(1 - r); k = math.sqrt(2 * math.log(2))
        tx = k * (a * math.cos(t) + b * math.sin(t)) / math.sqrt(2); ty = k * (a * math.cos(t) - b * math.sin(t)) / math.sqrt(2)
        if abs(xx - tx) > 0.51 / 27 or abs(yy - ty) > 0.51 / 27: bad.append((r, i, xx, tx, yy, ty, q))
check('A4 the ellipse that holds half: its 61 points are the pixels of Q = 2 ln 2 (1 - exp(-Q/2) = 1/2) at four values of %s' % RHO,
      not bad and abs(1 - math.exp(-math.log(2)) - 0.5) < 1e-15, bad[:2])
m = re.search(r'bnLn\("([0-9.]+) at " \+ bnRS \+ " = 0.6 and ([0-9.]+) at " \+ bnRS \+ " = 0.9."', SRC)
check('A5 help page 5 prints the CEP at %s = 0.6 and 0.9 as the reference gives them to 3 decimals (%.3f, %.3f)' % (RHO, REF[0.6], REF[0.9]),
      bool(m) and m.group(1) == '%.3f' % REF[0.6] and m.group(2) == '%.3f' % REF[0.9], m and m.groups())
h = fresh()
check('A6 a fresh run: BN_CEP is 0, no CEP worked out yet (bnCpD = 1), no shots', G(h, 'BN_CEP') == 0 and G(h, 'bnCpD') == 1 and G(h, 'bnShN') == 0)

print('=== S. the shots')
h = fresh(seed=11); h.execute('bnCepC()')
rets = [h.execute('bnShots(50)') for _ in range(10)]
n500, in500 = G(h, 'bnShN'), G(h, 'bnShIn')
r11 = h.execute('bnShots(50)')
check('S1 ten volleys of 50 make 500 shots; an eleventh fires none and says "500 shots is the most: Clear starts again"',
      rets == [1] * 10 and n500 == 500 and r11 == 0 and G(h, 'bnShN') == 500 and G(h, 'bnShIn') == in500 and G(h, 'bnMsg') == '500 shots is the most: Clear starts again', (rets, n500, r11, G(h, 'bnMsg')))
sx, sy, si = G(h, 'bnShX'), G(h, 'bnShY'), G(h, 'bnShI')
drawn = [(sx[i], sy[i]) for i in range(500) if sx[i] > 0]
inside_frame = all(22 < x and x + 1 < 184 and 18 < y and y + 1 < 180 for x, y in drawn)
check('S2 the count inside the circle is the number of shots flagged inside (%d of 500, near half), and every shot drawn is a 2 x 2 dot inside the frame (%d drawn)' % (in500, len(drawn)),
      in500 == sum(si[:500]) and abs(in500 - 250) <= 4 * math.sqrt(125) and inside_frame, (in500, sum(si[:500])))
xs = np.array([x for x, y in drawn], float); ys = -np.array([y for x, y in drawn], float)
rr = float(np.corrcoef(xs, ys)[0, 1])
check('S3 the 500 shots have the correlation they were fired with (%s = 0.60; the pixels give r = %.3f, within 4 standard errors)' % (RHO, rr), abs(rr - 0.6) <= 4 * (1 - 0.36) / math.sqrt(len(drawn)), rr)
# inside means x^2 + y^2 <= R^2: every flagged shot's pixel is within the circle (to a pixel), every unflagged one outside it
R27 = G(h, 'bnCpR') * 27; cx, cy = G(h, 'bnCXc'), G(h, 'bnCYc')
wrong = [(sx[i], sy[i], si[i]) for i in range(500) if sx[i] > 0 and ((si[i] == 1 and math.hypot(sx[i] - cx, sy[i] - cy) > R27 + 0.8) or (si[i] == 0 and math.hypot(sx[i] - cx, sy[i] - cy) < R27 - 0.8))]
check('S4 a shot is flagged inside exactly when it lies inside the circle (checked on its pixel, to a pixel)', not wrong, wrong[:3])
h.execute('bnSetRho(0.3)')
stale = (G(h, 'bnCpD'), G(h, 'bnShN'))
h.execute('bnDrawT()')
check('S5 a new %s marks the CEP stale; the next drawing of the target works it out again (R = %.4f) and removes the shots fired at the old %s' % (RHO, REF[0.3], RHO),
      stale == (1, 500) and G(h, 'bnShN') == 0 and G(h, 'bnShIn') == 0 and abs(G(h, 'bnCpR') - REF[0.3]) < 1e-9, (stale, G(h, 'bnShN'), G(h, 'bnCpR')))

print('=== V. the views, the keys and every way out')


def view_of(s):
    """which view a screen shows, from its first line"""
    L = s.lines()
    if L and L[0].startswith('Target: CEP'): return 'target'
    if L and L[0].startswith('From above'): return 'contour'
    return '3-D'


def waits(h): return [s for s in h.screens if s.menu]      # the screens the main loop waits on: they carry the soft keys


def s_cycle(h): h.tap(*K3); h.tap(*K3); h.tap(*K3); h.press('Esc')
h, res, err = run(s_cycle)
mn = [s.menu[2] for s in waits(h)]
fn = [view_of(s) for s in waits(h)]
check('V1 soft key 3 goes 3-D, Cont, CEP, 3-D, and names the next view each time ("Cont", "CEP", "3-D", "Cont"); in the target view keys 4 and 5 read Shots and Clear',
      err is None and mn == ['Cont', 'CEP', '3-D', 'Cont'] and fn == ['3-D', 'contour', 'target', '3-D']
      and [s.menu for s in waits(h) if view_of(s) == 'target'][0] == [RHO + MINUS, RHO + '+', '3-D', 'Shots', 'Clear', 'Menu'], (err, mn, fn))


def s_menu2(h):
    for _ in range(3): h.press('Enter'); h.choose(2)
    h.press('Enter'); h.choose(0)
    h.press('Esc')
h, res, err = run(s_menu2)
items = [c.items for c in h.chooses]
check('V2 the menu has 8 items of at most 30 characters; its item 2 names the next view ("Contour view (from above)", "Target view (CEP circle)", "3-D view") and goes there; Esc at the menu changes nothing',
      err is None and [it[1] for it in items] == ['Contour view (from above)', 'Target view (CEP circle)', '3-D view', 'Contour view (from above)']
      and all(len(it) == 8 and max(len(x) for x in it) <= 30 for it in items)
      and [view_of(s) for s in waits(h)] == ['3-D', 'contour', 'target', '3-D', '3-D'], (err, [it[1] for it in items], [view_of(s) for s in waits(h)]))


def state(h): return tuple(round(float(G(h, n)), 9) for n in ('bnRho', 'bnTh', 'bnPh', 'bnSlc', 'bnX0', 'bnView', 'bnShN', 'bnShIn'))


def at_target(seed=5):
    """a run brought to the target view by hand: the state the main loop would be in"""
    h = fresh(seed=seed); S(h, 'bnView', 3); S(h, 'bnTgt', 1); h.execute('bnDrawT()')
    return h


def s_arrows(h):
    h.tap(*K3); h.tap(*K3)
    for k in ('Left', 'Right', 'Up', 'Down'): h.press(k)
    h.press('Esc')
h, res, err = run(s_arrows)
tg = [s for s in h.screens if s.func == 'bnDrawT']
check('V3 in the target view the four arrows change nothing: five target screens, each with the same shapes and texts, and the slice stays off',
      err is None and len(tg) == 5 and all(t.lines() == tg[0].lines() and len(t.shapes) == len(tg[0].shapes) for t in tg) and G(h, 'bnSlc') == 0 and G(h, 'bnX0') == 1.5, (err, len(tg)))


def s_left2(h): h.tap(*K3); h.press('Left'); h.press('Esc')
h, res, err = run(s_left2)
check('V3b in the contour view Left still switches the slice on and moves it (x0 1.50 to 1.25), as in beta 1f', err is None and G(h, 'bnSlc') == 1 and G(h, 'bnX0') == 1.25, (err, G(h, 'bnSlc'), G(h, 'bnX0')))


def s_k45(h):
    h.tap(*K4)                                  # 3-D: Slice on
    h.tap(*KP)                                  # rho 0.7
    h.tap(*K5)                                  # 3-D: Reset (rho 0.6)
    h.tap(*K3); h.tap(*K3)                      # the target
    h.tap(*K4); h.tap(*K4)                      # Shots twice
    h.tap(*K5)                                  # Clear
    h.tap(*K4)
    h.press('Esc')
h, res, err = run(s_k45)
tg = [s for s in h.screens if s.func == 'bnDrawT']
counts = [next((l for l in s.lines() if l.startswith('Shots: ') or l.startswith('No shots')), None) for s in tg]
check('V4 keys 4 and 5: Slice and Reset in the 3-D view (the slice comes on; %s back to 0.60); Shots and Clear in the target view (0, 50, 100, 0, 50 shots; %s and the angles untouched)' % (RHO, RHO),
      err is None and G(h, 'bnSlc') == 1 and G(h, 'bnRho') == 0.6 and counts == ['No shots yet.', 'Shots: 50', 'Shots: 100', 'No shots yet.', 'Shots: 50'], (err, counts, G(h, 'bnSlc'), G(h, 'bnRho')))
ins = [l for l in tg[-1].lines() if l.startswith('inside: ')]
check('V4b the count line reads "inside: n (p %%)" with p = 100 n / 50 rounded (%s)' % ins,
      len(ins) == 1 and re.match(r'inside: (\d+) \((\d+) %\)$', ins[0]) and int(re.match(r'inside: (\d+) \((\d+) %\)$', ins[0]).group(2)) == round(100 * G(h, 'bnShIn') / 50), ins)


def s_taps(h):
    h.tap(*K3); h.tap(*K3)
    h.tap(100, 100)                             # on the plot
    h.tap(250, 100)                             # beside it, on the words
    h.tap(100, 200)                             # under it
    h.press('Esc')
h, res, err = run(s_taps)
check('V5 a tap on the plot fires 50 shots; a tap on the words beside it or under it fires none', err is None and G(h, 'bnShN') == 50, (err, G(h, 'bnShN')))


def s_rho(h):
    h.tap(*K3); h.tap(*K3); h.tap(*K4)          # 50 shots at 0.6
    h.tap(*KP)                                  # 0.7: shots gone
    h.press('Plus'); h.press('Plus')            # 0.8, 0.9
    h.tap(*KP)                                  # stops at 0.9
    h.press('Minus')                            # 0.8
    h.press('Esc')
h, res, err = run(s_rho)
tg = [s for s in h.screens if s.func == 'bnDrawT']
titles = [s.lines()[0] for s in tg]
rline = [next(l for l in s.lines() if l.startswith('R = ')) for s in tg]
want = ['R = %.3f' % REF[r] for r in (0.6, 0.6, 0.7, 0.8, 0.9, 0.9, 0.8)]
check('V6 %s%s, %s+ and the %s and + keys in the target view: a new %s, a new R (%s) and the shots gone; at 0.9 the page says "%s stops at 0.9 here"'
      % (RHO, MINUS, RHO, MINUS, RHO, ', '.join(want[2:]), RHO),
      err is None and rline == want and titles[-1] == 'Target: CEP, %s = 0.80' % RHO and (RHO + ' stops at 0.9 here') in tg[5].lines()
      and 'Shots: 50' in tg[1].lines() and 'No shots yet.' in tg[2].lines(), (err, rline, titles[-1], tg[5].lines()[-3:]))


def s_ask(h):
    h.tap(*K3); h.tap(*K3)
    h.press('Enter'); h.choose(1); h.answer(CANCEL)                        # Set rho: Cancel
    h.press('Enter'); h.choose(1); h.answer({'arV': 0.95})                 # refused
    h.press('Enter'); h.choose(1); h.answer({'arV': -0.45})                # accepted
    h.press('Esc')
h, res, err = run(s_ask)
tg = [s for s in h.screens if s.func == 'bnDrawT']
rline = [next(l for l in s.lines() if l.startswith('R = ')) for s in tg]
mb = [' '.join(m.lines) for m in h.msgboxes]
check('V7 Menu > Set %s in the target view: Cancel changes nothing; 0.95 is refused with its sentence and changes nothing; %s0.45 is taken (R = %.3f)' % (RHO, MINUS, cep_ref(-0.45)),
      err is None and rline == ['R = %.3f' % REF[0.6]] * 3 + ['R = %.3f' % cep_ref(-0.45)] and len(mb) == 1 and 'must be between' in mb[0] and G(h, 'bnRho') == -0.45, (err, rline, mb))

OLDLINE = 'BiNorm3D: %s = 0.60, E[Y | X = x] = 0.60 x; %s in BN_RHO' % (RHO, RHO)
h, res, err = run(lambda h: h.press('Esc'))
check('V8a Esc in the 3-D view ends the run with beta 1f\'s line, and BN_CEP is 0: the target view was never opened', err is None and res == OLDLINE and G(h, 'BN_CEP') == 0, (err, res))
h, res, err = run(lambda h: (h.tap(*K3), h.press('Esc')))
check('V8b Esc in the contour view: the same line', err is None and res == OLDLINE and G(h, 'BN_CEP') == 0, (err, res))
h, res, err = run(lambda h: (h.tap(*K3), h.tap(*K3), h.press('Esc')))
NEWLINE = 'BiNorm3D: %s = 0.60, E[Y | X = x] = 0.60 x, CEP = %.3f; %s in BN_RHO, the CEP in BN_CEP' % (RHO, REF[0.6], RHO)
check('V8c Esc in the target view: the line also names the CEP ("%s"), and BN_CEP holds it' % NEWLINE, err is None and res == NEWLINE and abs(G(h, 'BN_CEP') - REF[0.6]) < 1e-9, (err, res))
h, res, err = run(lambda h: (h.tap(*K3), h.tap(*K3), h.tap(*K3), h.tap(*KP), h.tap(*KP), h.press('Esc')))
check('V8d the target view opened, then %s changed in the 3-D view: the line and BN_CEP give the CEP for the LAST %s (0.80: %.3f), worked out at the end' % (RHO, RHO, REF[0.8]),
      err is None and res == 'BiNorm3D: %s = 0.80, E[Y | X = x] = 0.80 x, CEP = %.3f; %s in BN_RHO, the CEP in BN_CEP' % (RHO, REF[0.8], RHO) and abs(G(h, 'BN_CEP') - REF[0.8]) < 1e-9, (err, res))
h, res, err = run(lambda h: (h.tap(*K3), h.tap(*K3), h.tap(*K6), h.choose(8)))
check('V8e Menu > Quit from the target view ends the run with the same line as Esc there', err is None and res == NEWLINE, (err, res))
h, res, err = run(lambda h: (h.tap(*K3), h.tap(*K3), h.tap(*K4), h.press('Enter'), h.choose(6), h.press('Esc')))
last = waits(h)[-1]
check('V9 Menu > Frame timing from the target view shows its box and comes back to the target view with its shots', err is None and view_of(last) == 'target' and 'Shots: 50' in last.lines() and len(h.msgboxes) == 1, (err, view_of(last)))
h, res, err = run(lambda h: (h.tap(*K3), h.tap(*K3), h.press('Enter'), h.choose(4), h.press('Esc')))
check('V10 Menu > Reset the view from the target view leaves %s at 0.60 and the target on the screen' % RHO, err is None and G(h, 'bnRho') == 0.6 and view_of(waits(h)[-1]) == 'target', err)

print('=== R. regression against beta 1f')


def drawn(path, routine, rho, th, ph, slc, x0):
    hh = fresh(path)
    hh.execute('bnSetRho(%r)' % rho)
    S(hh, 'bnTh', th * math.pi / 180); S(hh, 'bnPh', ph * math.pi / 180); S(hh, 'bnSlc', slc)
    hh.execute('bnSetX0(%r)' % x0)
    S(hh, 'bnView', 1 if routine == 'bnDraw3D' else 2)
    hh.reset_records()
    hh.execute(routine + '()')
    s = hh.screens[-1]
    return [(t.text, t.x, t.y, t.font, t.color) for t in s.texts], [repr(x) for x in s.shapes], list(s.menu or [])
diff = []; n = 0
for rho in (-0.9, -0.4, 0, 0.6, 0.9):
    for th, ph in ((35, 30), (120, 60), (300, 15)):
        for slc, x0 in ((0, 1.5), (1, -2), (1, 0), (1, 1.5)):
            for routine in ('bnDraw3D', 'bnDrawC'):
                a = drawn(OLD, routine, rho, th, ph, slc, x0); b = drawn(PROG, routine, rho, th, ph, slc, x0); n += 1
                ma, mb_ = a[2], b[2]
                if routine == 'bnDrawC': mb_ = [('3-D' if x == 'CEP' else x) for x in mb_]
                if a[0] != b[0] or a[1] != b[1] or ma != mb_: diff.append((routine, rho, th, ph, slc, x0))
check('R1 the 3-D view and the contour view draw exactly beta 1f\'s shapes and texts in %d states (5 values of %s, 3 pairs of angles, the slice off and at 3 places); only soft key 3 of the contour view differs ("CEP" for "3-D")' % (n, RHO),
      not diff, diff[:3])


def session(h, new):
    def k3_from_contour():
        h.tap(*K3)
        if new: h.tap(*K3)                     # past the target view
    h.tap(*KP)                                 # rho 0.7
    h.press('Right'); h.press('Up')            # turn, raise
    h.tap(*K4)                                 # slice on
    h.tap(*K3)                                 # Cont
    h.tap(60, 100)                             # slice by tap
    h.press('Left'); h.press('Right')
    h.tap(*K4)                                 # slice off
    h.tap(*KM); h.tap(*KM)
    k3_from_contour()                          # back to 3-D
    h.tap(*K5)                                 # Reset
    h.press('Enter'); h.choose(5)              # grid while dragging
    h.press('Enter'); h.choose(3)              # slice on by the menu
    h.press('Enter'); h.choose(1); h.answer({'arV': -0.3})
    h.press('Enter'); h.choose(7)              # help
    for _ in range(6 if new else 5): h.press('Enter')
    h.press('Esc')


def norm(s):
    L = [re.sub(r'(BiNorm3D help \d)/\d', r'\1/N', re.sub(r'^(\d)/\d,', r'\1/N,', l)) for l in s.lines()]
    return (s.func, tuple(L), len(s.shapes), tuple(('3-D' if x == 'CEP' else x) for x in (s.menu or [])))
ho, ro, eo = run(lambda h: session(h, False), OLD)
hn, rn, en = run(lambda h: session(h, True))
so = [norm(s) for s in ho.screens if s.func != 'bnPgEnd' and s.func != 'bnWelcome']
sn = [norm(s) for s in hn.screens if s.func not in ('bnPgEnd', 'bnWelcome') and view_of(s) != 'target']
check('R2 a session of the old features (rho keys, arrows, slice by key, tap and menu, Reset, the grid item, Set %s, both views) shows the same %d screens in both versions once the target view\'s are taken out; '
      'beta 1g returns beta 1f\'s line with the CEP added' % (RHO, len(so)),
      eo is None and en is None and so == sn and len(so) > 15 and rn.startswith(ro.split(';')[0]) and rn.endswith('the CEP in BN_CEP'), (eo, en, len(so), len(sn), ro, rn))

print('=== H. the help')


def helppages(path, n):
    hh = Harness(path, idle_key=4, home_minus=True)
    hh.press('Enter'); hh.press('Enter'); hh.choose(7)
    for _ in range(n): hh.press('Enter')
    hh.press('Esc')
    hh.execute('BiNorm3D()')
    return [s for s in hh.screens if s.func == 'bnPgEnd'], [s for s in hh.screens if s.func == 'bnWelcome'][0]
po, wo = helppages(OLD, 5); pn, wn = helppages(PROG, 6)
check('H1 six help pages, titled "BiNorm3D help n/6: ..."', len(pn) == 6 and all(pn[i].lines()[0].startswith('BiNorm3D help %d/6: ' % (i + 1)) for i in range(6)), [p.lines()[0] for p in pn])
same = all([l.replace('/5', '/6') for l in po[i].lines()] == pn[i].lines() for i in range(4))
check('H2 pages 1 to 4 are beta 1f\'s word for word, with 6 for 5 in the header and the footer', same)
a, b = po[4].lines(), pn[5].lines()
gone = [l for l in a if l not in b]; came = [l for l in b if l not in a]
check('H3 page 6 is beta 1f\'s page 5 with four lines changed (the header, the views, BN_CEP, the footer) and one more (the target\'s keys): %r' % (came,),
      gone == ['BiNorm3D help 5/5: Keys and touch', 'Cont: the view from above; 3-D goes back.', 'Home after a run: BN_RHO holds %s.' % RHO, '5/5, tap or key = back to the surface']
      and came == ['BiNorm3D help 6/6: Keys and touch', 'Cont: the view from above; CEP: the target; 3-D: the surface.', 'Target: Shots (or a tap) fires 50 shots; Clear removes them.',
                   'Home after a run: BN_RHO holds %s; BN_CEP the CEP if shown.' % RHO, '6/6, tap or key = back to the surface'], (gone, came))
want5 = ['BiNorm3D help 5/6: The target and the CEP',
         'CEP shows the pattern from above as a target.  Think of each',
         '(x, y) pair as a shot aimed at the center.',
         'The green circle holds half of all the shots.  Its radius R is the',
         'CEP, the circular error probable: a shot is as likely to land',
         'inside the circle as outside it.  R is in SDs of X (or of Y).',
         RHO + ' = 0: the pattern is round and R = 1.177.  As ' + RHO + ' moves away',
         'from 0 the pattern grows longer and narrower, and R shrinks:',
         '%.3f at %s = 0.6 and %.3f at %s = 0.9.' % (REF[0.6], RHO, REF[0.9], RHO),
         'The blue ellipse holds half of the shots too.  It has the',
         "pattern's own shape, so it covers less area than the circle.",
         'Shots, or a tap on the plot, fires 50 shots and counts those',
         'inside the circle: about half.  Clear removes the shots.',
         '5/6, tap or key = next page, Esc = back']
check('H4 page 5, The target and the CEP, reads as written (14 lines)', pn[4].lines() == want5, [x for x in pn[4].lines() if x not in want5])
wide = [(l, px(l)) for p in pn for l in p.lines()[1:] if px(l) > 296]
low = max(t.y for p in pn for t in p.texts if t.y < 215)
check('H5 every help line fits its 296 px at the measured glyph widths (widest %d px), and no line of text sits below y = %d' % (max(px(l) for p in pn for l in p.lines()[1:]), low),
      not wide and low <= 201, wide[:3])
a, b = wo.lines(), wn.lines()
check('H6 the opening page: beta 1f\'s lines, with two more on the target view and "six pages of help"',
      [l for l in b if l not in a] == ['CEP: the pattern as a target, with the circle', 'that holds half of the shots.', 'Enter: menu, with six pages of help.']
      and [l for l in a if l not in b] == ['Enter: menu, with five pages of help.'], ([l for l in b if l not in a], [l for l in a if l not in b]))

print('=== G. static')
code = '\n'.join(re.sub(r'"[^"\n]*"', '""', l.split('//')[0]) for l in SRC.split('\n'))
check('G1 no "!=" in the code, and the code outside strings and comments is ASCII', '!=' not in code and all(ord(c) < 128 for c in code), [c for c in code if ord(c) >= 128][:5])
loc = [l for l in SRC.split('\n') if re.match(r'\s*LOCAL\s', l)]
check('G2 every LOCAL line names at most 6 variables (%d lines)' % len(loc), all(len(l.split('//')[0].replace('LOCAL', '').split(',')) <= 6 for l in loc))
check('G3 the header names beta 1g and its date', '// BINORM3D - beta 1g' in SRC and '// beta 1g (15 Nov 2026): Round 16' in SRC)
wide = []
for s_ in set((s.func, tuple((t.text, t.x, t.font, t.width) for t in s.texts)) for s in tg):
    for text, x, font, width in s_[1]:
        if px(text, int(font)) > width or x + px(text, int(font)) > 319: wide.append((text, x, px(text, int(font)), width))
check('G4 every text of the target view fits its width argument and the screen at the measured glyph widths', not wide, wide[:3])

print('=== D. layout over every beta 1g screen above')
firm = []
for t, f in OV.report().items():
    firm += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
# label_fit_v1 measures at an estimate (5.5 px a character in font 1).  Each text it reports is measured again here at the
# glyph widths GlyphProbe_v1 measured on the Virtual Calculator: it is cut only if it is wider than its width argument there.
rep_ = sorted(set((x[0], x[3], x[4]) for v in LF.clipped(OV.RECORDS).values() for x in v))
cut = [(t, px(t, int(f)), w) for t, f, w in rep_ if px(t, int(f)) > w]
check('D1 no firm overlap and no text off the screen (text_overlap_v1)', not firm, firm[:4])
check('D2 no number cut short by its width argument (label_fit_v1 reports %d texts at its estimate; none is wider than its width argument at the measured glyph widths)' % len(rep_), not cut, cut[:4])

print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
