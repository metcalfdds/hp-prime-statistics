#!/usr/bin/env python3
"""verify_ScatterLab_beta2k.py -- checks ScatterLab beta 2k (Round 14, 14 Nov 2026): inference for the slope, the two
95% bands, Anscombe's quartet.  Runs from the repository alone (Lessons Learned s14 rule 18): tools/, programs/ and
verify/ by relative path, beta 2j from git (the commit before Round 14).  Needs hp-prime-kit (HPKIT), SciPy, NumPy.

  T1  verify/round14/make_scatterlab_2k.py, run again from beta 2j, makes programs/ScatterLab_beta2k.txt byte for byte.
  A   the arithmetic (slInf, called through the harness on program state, rule 19) against SciPy's linregress and
      t.ppf: s, SE(b1), t, the two-tailed p, t crit and the 95% interval, on the example, on Anscombe's four sets and
      on 300 random sets of 3 to 40 points; Anscombe's values against R's data set anscombe.
  E   the edges: every point on the line (no t: the page says so, nothing divides by zero), fewer than 3 points and
      all x equal (the page and the bands are refused with a sentence, nothing changes), a p below 0.001 ("< 0.001",
      never 0.000), a p that rounds to 0.050 (its 4 significant digits beside the decision).
  P   the page's lines at the calculator's glyph widths (verify/round11/glyph_widths_vc.json): none past 296 px, for
      ordinary data and for values near 1E8 and 1E-8 (the long form of a line gives way to the short one).
  B   the bands: every pixel inside the plot box; at x-bar the inner band's half-width is t crit s / root(n) to the
      pixel; the outer band lies outside the inner one in every column; off, not drawn.
  M   the menus: every item of the new 12-item menu and the 8-item Data menu does its old job (the far point, fit,
      residuals, guess, the calculus page, data, type a point, delete, help, quit; the example, C1/C2 load and save,
      clear); Esc at each menu changes nothing; every menu item is at most 30 characters.
  R   regression: a tour that uses no new feature draws the same screens in beta 2j and beta 2k, apart from the help
      titles (n/6 -> n/7), help page 6's two Home lines and the menu's own text.
  H   the help: 7 pages; pages 1 to 6 are beta 2j's but for those lines; every page fits at the glyph widths.
  D   layout: text_overlap_v1 and label_fit_v1 over every beta 2k screen drawn above: no firm overlap, no cut number.
"""
import os, sys, io, json, math, random, subprocess, tempfile, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

BASE = '26912a9'
PROG = os.path.join('programs', 'ScatterLab_beta2k.txt')
tmp = tempfile.mkdtemp(prefix='slv_')
OLD = os.path.join(tmp, 'ScatterLab_beta2j.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/ScatterLab_beta2j.txt'], check=True, capture_output=True).stdout)
GW = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'round11', 'glyph_widths_vc.json'))).items()}
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def width(t, font=1):
    return sum(GW[ord(c)][font - 1] if ord(c) in GW else 8 for c in t)


def key(h, name):
    for k in h.globals_:
        if k.lower() == name.lower(): return k
    raise KeyError(name)


def G(h, name): return h.globals_[key(h, name)]


def setpts(h, xs, ys):
    X = [0.0] * 40; Y = [0.0] * 40
    X[:len(xs)] = [float(v) for v in xs]; Y[:len(ys)] = [float(v) for v in ys]
    h.globals_[key(h, 'slX')] = X; h.globals_[key(h, 'slY')] = Y; h.globals_[key(h, 'slN')] = float(len(xs))
    h.execute('slAutoWin()'); h.execute('slFit()')


def fresh(path=PROG):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail')
    h.execute('slInit()')
    return h


def ref(xs, ys):
    r = stats.linregress(xs, ys); n = len(xs); x = np.array(xs, float); y = np.array(ys, float)
    s = math.sqrt(max(0.0, float(np.sum((y - (r.intercept + r.slope * x)) ** 2))) / (n - 2))
    tc = stats.t.ppf(0.975, n - 2)
    return dict(s=s, seb=r.stderr, t=r.slope / r.stderr, p=r.pvalue, tc=tc, lo=r.slope - tc * r.stderr, hi=r.slope + tc * r.stderr)


def close(a, b, tol=1e-9): return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def cmp(h, xs, ys):
    q = ref(xs, ys)
    got = dict(s=G(h, 'slSe'), seb=G(h, 'slSeB'), t=G(h, 'slTv'), p=G(h, 'slPv'), tc=G(h, 'slTc'), lo=G(h, 'slCiL'), hi=G(h, 'slCiH'))
    return [k for k in q if not close(got[k], q[k])], got, q


def page(h):
    h.screens[:] = []
    h.execute('slInfPage()')
    return h.screens[-1] if h.screens else None


EXX = [10.4, 14.9, 7.1, 18.6, 23.0, 25.0, 12.5, 7.5, 14.2, 18.6, 10.8, 19.8, 25.8, 14.0, 16.0, 22.6]
EXY = [34.4, 43.5, 22.3, 36.1, 45.2, 35.3, 31.5, 20.2, 26.8, 27.8, 26.2, 41.8, 43.1, 26.0, 30.6, 41.3]
ANS = {1: ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
       2: ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
       3: ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
       4: ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])}   # R: anscombe

print('=== T. the build')
out = os.path.join(tmp, 'built')
subprocess.run([sys.executable, os.path.join(HERE, 'round14', 'make_scatterlab_2k.py'), out], check=True, capture_output=True)
check('T1 the build makes programs/ScatterLab_beta2k.txt byte for byte',
      open(os.path.join(out, 'ScatterLab_beta2k.txt'), 'rb').read() == open(PROG, 'rb').read())

print('=== A. the arithmetic against SciPy')
OV.install()
h = fresh(); h.execute('slExample()')
bad, got, q = cmp(h, EXX, EXY)
check('A1 the example: s, SE(b1), t, p, t crit and the interval equal linregress and t.ppf (t = %.4f, p = %.6f)' % (got['t'], got['p']), not bad, (bad, got, q))
check('A2 Home: SL_SEB, SL_T, SL_P hold the same numbers', close(G(h, 'SL_SEB'), q['seb']) and close(G(h, 'SL_T'), q['t']) and close(G(h, 'SL_P'), q['p']))
okA, okV, summ = True, True, []
for k in (1, 2, 3, 4):
    h.execute('slAnsc(%d)' % k)
    xs, ys = ANS[k]
    okV = okV and G(h, 'slN') == 11 and [G(h, 'slX')[i] for i in range(11)] == [float(v) for v in xs] and [G(h, 'slY')[i] for i in range(11)] == [float(v) for v in ys]
    bad, got, q = cmp(h, xs, ys); okA = okA and not bad
    summ.append('%.2f + %.3fx, r = %.2f (%.3f)' % (G(h, 'slB0'), G(h, 'slB1'), G(h, 'slR'), G(h, 'slR')))
check('A3 Anscombe\'s four sets hold the values of R\'s anscombe', okV)
check('A4 on each of them the slope test equals SciPy\'s', okA)
check('A5 all four give 3.00 + 0.500x and r = 0.82; to three decimals r is 0.816, 0.816, 0.816 and 0.817',
      [x.split(' (')[0] for x in summ] == ['3.00 + 0.500x, r = 0.82'] * 4 and [x[-6:-1] for x in summ] == ['0.816', '0.816', '0.816', '0.817'], summ)
check('A6 all four share one window, x 2 to 20 and y 2 to 14', (G(h, 'slXlo'), G(h, 'slXhi'), G(h, 'slYlo'), G(h, 'slYhi')) == (2, 20, 2, 14))
rng = random.Random(14); nbad = []; near = None
for i in range(300):
    n = rng.randint(3, 40); sc = 10 ** rng.uniform(-2, 3)
    xs = [round(rng.uniform(0, 100) * sc, 4) for _ in range(n)]
    b = rng.uniform(-2, 2); ys = [round(5 + b * x + rng.gauss(0, 30 * sc), 4) for x in xs]
    if len(set(xs)) < 3: continue
    setpts(h, xs, ys)
    if G(h, 'slOK') != 1: nbad.append((i, 'no line')); continue
    bad, got, q = cmp(h, xs, ys)
    if bad: nbad.append((i, bad))
check('A7 300 random sets of 3 to 40 points: every number equals SciPy\'s to 9 digits', not nbad, nbad[:3])

print('=== E. the edges')
h = fresh(); setpts(h, [1, 2, 3, 4, 5], [3, 5, 7, 9, 11])
sc = page(h); L = sc.lines() if sc else []
check('E1 every point on the line: no test (slIok 0), and the page says the slope has no t-test', G(h, 'slIok') == 0 and any('no t-test' in l for l in L) and not any(l.startswith('t =') for l in L), L)
h = fresh(); setpts(h, [1, 2], [3, 5]); sc = page(h)
check('E2 two points: the page is refused with a sentence, no page drawn', sc is None and 'needs 3 points' in G(h, 'slMsg1'), G(h, 'slMsg1'))
h = fresh(); setpts(h, [4, 4, 4, 4], [1, 2, 3, 5]); sc = page(h)
check('E3 every x the same: the page is refused the same way', sc is None and 'needs 3 points' in G(h, 'slMsg1'))
h = fresh(); h.execute('slExample()'); L = page(h).lines()
check('E4 the example\'s p (0.0008) prints "p < 0.001", never 0.000', any(l.startswith('p < 0.001') for l in L) and not any('0.000 ' in l for l in L), L)
rng = random.Random(5); found = None
for i in range(60000):
    xs = list(range(1, 11)); ys = [round(rng.gauss(0, 1) + 0.25 * x, 2) for x in xs]
    p = stats.linregress(xs, ys).pvalue
    if 0.0495 <= p < 0.0505: found = (xs, ys, p); break
if found:
    setpts(h, found[0], found[1]); L = page(h).lines()
    want = 'just below' if found[2] < 0.05 else 'just above'
    check('E5 a p of %.5f: the decision line carries "(p = %.5f: %s α = 0.050.)"' % (found[2], found[2], want),
          any(('(p = %.5f: %s' % (found[2], want)) in l for l in L), L)
else:
    check('E5 a p that rounds to 0.050 was found to test with', False)

print('=== P. the page at the calculator\'s glyph widths')
worst = (0, '')
def pagefit(h, label):
    global worst
    sc = page(h); over = []
    for t in [it for it in sc.items if hasattr(it, 'text') and it.text.strip()]:
        w = width(t.text, int(t.font or 1))
        if w > worst[0]: worst = (w, t.text)
        if w > 296 or t.x + w > 318: over.append((w, t.text))
    return over
h = fresh(); h.execute('slExample()')
check('P1 the example: every line of the page within 296 px', not pagefit(h, 'example'))
ov = []
for k in (1, 2, 3, 4):
    h.execute('slAnsc(%d)' % k); ov += pagefit(h, 'anscombe')
check('P2 Anscombe\'s four sets: the same', not ov, ov)
rng = random.Random(8); ov = []; shortseen = 0
for sx, sy in ((1e8, 1e8), (1e-8, 1), (1, 1e-8), (1e6, 1e-6), (1e-6, 1e6), (1e8, 1e-8), (12345.678, 98765.4321)):
    for rep_ in range(6):
        n = rng.randint(3, 40)
        xs = [rng.uniform(1, 9) * sx for _ in range(n)]; ys = [rng.uniform(1, 9) * sy for _ in range(n)]
        setpts(h, xs, ys)
        if G(h, 'slOK') != 1: continue
        ov += pagefit(h, 'big')
        if any(l.startswith('s = ') and '(' not in l for l in h.screens[-1].lines()): shortseen += 1
check('P3 42 sets with values near 1E8 and 1E-8: no line past 296 px (widest %d px: %r)' % (worst[0], worst[1][:40]), not ov, ov[:3])
check('P4 slIL hands back the short form when the long one is past 294 px (never needed on those pages: %d)' % shortseen,
      h.execute('slIL("' + 'a' * 60 + '", "short")') == 'short' and h.execute('slIL("fits", "short")') == 'fits')

print('=== B. the bands')
def bandpix(h):
    h.screens[:] = []; h.execute('slDraw()')
    sc = h.screens[-1]
    return [(int(it.args[0]), int(it.args[1]), it.args[2]) for it in sc.items if getattr(it, 'cmd', '') == 'PIXON_P']
h = fresh(); h.execute('slExample()')
check('B1 off at the start: no band pixel drawn', len(bandpix(h)) == 0)
h.globals_[key(h, 'slBand')] = 1.0
px = bandpix(h); PL, PR, PT, PB = (int(G(h, n)) for n in ('slPL', 'slPR', 'slPT', 'slPB'))
check('B2 on: %d band pixels, every one inside the plot box' % len(px), len(px) > 200 and all(PL <= x <= PR and PT <= y <= PB for x, y, c in px))
blue = G(h, 'slBLUE'); orng = G(h, 'slORNG')
inner = {}; outer = {}
for x, y, c in px: (inner if c == blue else outer).setdefault(x, []).append(y)
q = ref(EXX, EXY); n = len(EXX); xb = sum(EXX) / n
def ypix(v): return PB - (v - G(h, 'slYlo')) / (G(h, 'slYhi') - G(h, 'slYlo')) * (PB - PT)
def xpix(v): return PL + (v - G(h, 'slXlo')) / (G(h, 'slXhi') - G(h, 'slXlo')) * (PR - PL)
cx = int(round(xpix(xb))); r = stats.linregress(EXX, EXY)
xd = G(h, 'slXlo') + (cx - PL) / (PR - PL) * (G(h, 'slXhi') - G(h, 'slXlo'))
hw = q['tc'] * q['s'] * math.sqrt(1 / n + (xd - xb) ** 2 / float(np.sum((np.array(EXX) - xb) ** 2)))
yc = r.intercept + r.slope * xd
want = sorted([int(ypix(yc + hw) + 0.5), int(ypix(yc - hw) + 0.5)])
check('B3 at x-bar the inner band stands t crit s root(1/n) = %.3f above and below the line, to the pixel' % hw, sorted(inner.get(cx, [])) == want, (sorted(inner.get(cx, [])), want))
okO = all(min(outer[x]) <= min(inner[x]) and max(outer[x]) >= max(inner[x]) for x in outer if x in inner and len(inner[x]) == 2 and len(outer[x]) == 2)
check('B4 the outer band (one new case) lies outside the inner one (the mean of y) in every column that shows both', okO and len(outer) > 40)
check('B5 the outer band is dotted: two columns in every four', all(x % 4 < 2 for x in outer))

print('=== M. the menus')
import re
SRC = io.open(PROG, encoding='utf-8').read()
items = re.findall(r'^\s+"([^"\n]*)"[,}]', SRC[SRC.index('CHOOSE(muI, "ScatterLab", {'):SRC.index('IF muI == 1 THEN slFarPt')], re.M)
ditems = re.findall(r'^\s+"([^"\n]*)"[,}]', SRC[SRC.index('CHOOSE(daI, "Data", {'):SRC.index('IF daI == 1 THEN slExample')], re.M)
check('M1 the menu has 12 items and the Data menu 8, each at most 30 characters', len(items) == 12 and len(ditems) == 8 and max(map(len, items + ditems)) <= 30, (items, ditems))
def run(script, path=PROG, c1=None, c2=None):
    app = {'C1': [float(v) for v in c1], 'C2': [float(v) for v in c2]} if c1 is not None else None
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=app)
    script(h)
    try: res = h.execute('ScatterLab()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
    return h, res, err
def menu(h, k, sub=None):
    h.press('Enter')
    if sub is None: h.choose(k)
    else: h.choose(k, sub)
def s_all(h):
    menu(h, 8, 1)                 # Data > the example
    menu(h, 6); h.press('Enter')  # the inference page, a key closes it
    menu(h, 7)                    # bands on
    menu(h, 1)                    # the far point (the bands follow)
    menu(h, 2); menu(h, 3); menu(h, 4); h.press('Enter'); h.press('Esc')   # fit, residuals, guess, reveal, back
    menu(h, 5); h.press('Enter')  # least squares as calculus
    menu(h, 9); h.answer({'tpX': 12.0, 'tpY': 30.0})
    h.press(50); menu(h, 10)     # delete the selected point
    menu(h, 7)                    # bands off
    for k in (2, 3, 4, 5): menu(h, 8, k)   # Anscombe 1 to 4
    menu(h, 6); h.press('Enter')
    menu(h, 11); [h.press('Right') for _ in range(7)]   # help, 7 pages
    menu(h, 12)                   # quit
h, res, err = run(s_all)
allL = [l for s in h.screens for l in s.lines()]
check('M2 a tour of every menu item ends with the Quit summary and no error', err is None and isinstance(res, str) and res.startswith('ScatterLab: n = 11'), (err, res))
check('M3 it showed the inference page twice, the bands\' two notes, the calculus page and help 7/7',
      sum(1 for s in h.screens if s.lines() and s.lines()[0] == 'Inference for the slope') >= 2 and any('Solid blue: where the MEAN of y lies' in l for l in allL)
      and any('Dotted orange: where ONE new case falls' in l for l in allL) and any('help 7/7' in l for l in allL) and any('Anscombe (1973), set 4 of 4' in l for l in allL))
def s_cancel(h):
    menu(h, 8, 1); h.press('Enter'); h.choose(0); h.press('Enter'); h.choose(8, 0); menu(h, 12)
h2, res2, err2 = run(s_cancel)
check('M4 Esc at the menu and at the Data menu changes nothing: the example\'s 16 points and line at Quit', err2 is None and res2.startswith('ScatterLab: n = 16'), (err2, res2))
def s_refuse(h):
    menu(h, 7); menu(h, 6); menu(h, 12)
h3, res3, err3 = run(s_refuse); L3 = [l for s in h3.screens for l in s.lines()]
check('M5 with no points, Bands and Inference are refused with their sentences and nothing is drawn',
      err3 is None and any('Bands need a line: 3 points with different x.' in l for l in L3) and any('A slope needs 3 points with different x.' in l for l in L3)
      and not any(l == 'Inference for the slope' for l in L3) and G(h3, 'slBand') == 0)
def s_c(h):
    menu(h, 8, 6); menu(h, 8, 7); menu(h, 8, 8); menu(h, 12)
h4, res4, err4 = run(s_c, c1=[1, 2, 3, 4, 5], c2=[2, 4, 5, 4, 5])
check('M6 Data items 6, 7, 8 are still Load from C1/C2, Save and Clear (5 points loaded, then none)', err4 is None and res4.startswith('ScatterLab: n = 0'), (err4, res4))

print('=== R. regression against beta 2j')
def s_old(newmenu):
    D, T, DEL, HELP, Q = (8, 9, 10, 11, 12) if newmenu else (6, 7, 8, 9, 10)
    def s(h):
        menu(h, D, 1); menu(h, 1); menu(h, 2); menu(h, 3); menu(h, 4); h.press('Up'); h.press('Right'); h.press('Down'); h.press('Enter'); h.press('Esc')
        menu(h, 5); h.press('Enter'); menu(h, T); h.answer({'tpX': 12.0, 'tpY': 30.0}); h.press(50); h.press('Left'); menu(h, DEL)
        h.tap(100, 100); h.tap(150, 80); h.press(42); menu(h, Q)
    return s
ho, ro, eo = run(s_old(False), OLD); hn, rn, en = run(s_old(True), PROG)
def scr(h): return [tuple(l for l in s.lines()) for s in h.screens]
so, sn = scr(ho), scr(hn)
check('R1 a tour with no new feature: the same %d screens, text for text, and the same Quit summary' % len(so), eo is None and en is None and so == sn and ro == rn, (len(so), len(sn), eo, en, [i for i, (a, b) in enumerate(zip(so, sn)) if a != b][:3]))

print('=== H. the help')
def helppages(path):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail'); h.execute('slInit()'); h.screens[:] = []
    for i in range(12): h.press('Right')
    h.execute('slHelp()')
    seen, pages = set(), []
    for s in h.screens:
        k = '\n'.join(s.lines())
        if s.lines() and k not in seen: seen.add(k); pages.append(s)
    return pages
po, pn = helppages(OLD), helppages(PROG)
check('H1 seven help pages, titled n/7', len(pn) == 7 and all(('ScatterLab help %d/7:' % (i + 1)) in pn[i].lines()[0] for i in range(7)), [p.lines()[0] for p in pn])
diff = []
for i in range(6):
    a = [l.replace('/6', '/7') for l in po[i].lines()]; b = pn[i].lines()
    diff += [(i + 1, x, y) for x, y in zip(a, b) if x != y]
check('H2 pages 1 to 6 are beta 2j\'s but for the page count and page 6\'s two lines on Home\'s results', len(diff) == 2 and all(d[0] == 6 and 'SL_' in d[2] for d in diff), diff)
over = []
for p in pn:
    for t in [it for it in p.items if hasattr(it, 'text') and it.text.strip()]:
        w = width(t.text, int(t.font or 1))
        if w > min(318 - t.x, t.width or 999): over.append((w, t.text))
check('H3 every help line within its width at the glyph widths', not over, over)

print('=== D. layout over every beta 2k screen above')
firm = []
for t, f in OV.report().items():
    firm += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
cut = sorted(set(x[0] for v in LF.clipped(OV.RECORDS).values() for x in v))
check('D1 no firm overlap and no text off the screen (text_overlap_v1)', not firm, firm[:4])
check('D2 no number cut short by its width argument (label_fit_v1)', not cut, cut[:4])

print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
