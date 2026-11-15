#!/usr/bin/env python3
"""verify_FitCheck_beta1h.py -- checks FitCheck beta 1h (Round 15, 15 Nov 2026): a standard error beside the skewness g1 and
beside the excess kurtosis g2 on the normality Tests page, a sentence on them on help page 5, and the credits (help page 8
and the header) in the words of what was done.  Runs from the repository alone (Lessons Learned s14 rule 18): tools/,
programs/ and verify/ by relative path, beta 1g from git (the commit before Round 15).  Needs hp-prime-kit (HPKIT), SciPy,
NumPy.

  T1  verify/round15/make_fitcheck_1h.py, run again from beta 1g, makes programs/FitCheck_beta1h.txt byte for byte.
  A   the arithmetic.  fc_ShapeSE, called through the harness (rule 19), against the two formulas written out here, and
      against a second reference that does not use them: the standard deviations of g1 and g2 over 200,000 simulated normal
      samples (a fixed seed, so the reference gives the same answer twice).  g1 and g2 themselves, and the n the standard
      errors are taken at, against SciPy's skew and kurtosis on 60 random samples of 3 to 300 values, on the Rossi ages
      preset (n = 432) and on the binned crimtab preset (n = 3,000).
  P   the Tests page, line for line: beta 1g's list of lines with its one shape line taken out equals beta 1h's with its
      three taken out, and the three are the expected text, for a random sample, both presets, and 3 values; no line of
      the page is longer than its 46 characters.
  E   the edges: 3 values (SE(g2) is 0.000, and nothing fails); fewer than 3 values, every value the same, and more than
      5,000 are refused with their sentences BEFORE the standard errors are worked out (nothing divides by zero).
  M   the menus and their ways out: Esc at the main menu and at the Normality menu; the soft keys Q-Q, ECDF, Tests and
      Menu; turning the Tests page with a key and a tap; a refused read of D1; Help paged to its end.
  R   regression against beta 1g: 30 seeds of the monkey on both versions.  The same verdict, boxes and Quit summary, and
      every screen the same text for text, apart from the version on the opening screen, the normality Tests pages (their
      lines moved down by two) and help pages 5 and 8.
  H   the help: 8 pages still; pages 1 to 4, 6 and 7 are beta 1g's word for word; page 5 is beta 1g's with two lines more;
      page 8 has the new credits; the word "rework" is nowhere in the program.
  D   layout: text_overlap_v1 and label_fit_v1 over every beta 1h screen drawn above: no firm overlap, no cut number.
"""
import os, sys, io, re, json, math, random, signal, subprocess, tempfile, warnings
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

BASE = 'a7df6e7'
PROG = os.path.join('programs', 'FitCheck_beta1h.txt')
tmp = tempfile.mkdtemp(prefix='fcv_')
OLD = os.path.join(tmp, 'FitCheck_beta1g.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/FitCheck_beta1g.txt'], check=True, capture_output=True).stdout)
SRC = io.open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]
MINUS = chr(8722)


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:700]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def key(h, name):
    for k in h.globals_:
        if k.lower() == name.lower(): return k
    raise KeyError(name)


def G(h, name): return h.globals_[key(h, name)]


def fresh(path=PROG, d1=None):
    app = {'D1': [float(v) for v in d1]} if d1 is not None else None
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=app)
    h.execute('fc_Init()')
    return h


def lst(xs): return '{' + ','.join(repr(float(v)) for v in xs) + '}'
def se1(n): return math.sqrt(6.0 * (n - 2) / ((n + 1) * (n + 3)))
def se2(n): return math.sqrt(24.0 * n * (n - 2) * (n - 3) / ((n + 1) ** 2 * (n + 3) * (n + 5)))
def close(a, b, tol=1e-10): return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
def sgn(v, d=3):
    r = round(v, d) + 0.0
    t = ('%.' + str(d) + 'f') % abs(r)
    return ('+' if r >= 0 else MINUS) + t


print('=== T. the build')
out = os.path.join(tmp, 'built')
subprocess.run([sys.executable, os.path.join(HERE, 'round15', 'make_fitcheck_1h.py'), out], check=True, capture_output=True)
check('T1 the build makes programs/FitCheck_beta1h.txt byte for byte',
      open(os.path.join(out, 'FitCheck_beta1h.txt'), 'rb').read() == open(PROG, 'rb').read())

print('=== A. the arithmetic')
OV.install()
h = fresh(); bad = []
for n in (3, 4, 5, 10, 30, 100, 432, 3000, 5000):
    h.execute('fc_ShapeSE(%d)' % n)
    if not (close(G(h, 'fcSeS'), se1(n)) and close(G(h, 'fcSeK'), se2(n))): bad.append((n, G(h, 'fcSeS'), se1(n), G(h, 'fcSeK'), se2(n)))
check('A1 fc_ShapeSE at n = 3 to 5,000: root(6(n-2)/((n+1)(n+3))) and root(24n(n-2)(n-3)/((n+1)^2(n+3)(n+5))) to 10 digits', not bad, bad)
rng = np.random.default_rng(15); worst = 0.0; rows = []
for n in (4, 10, 30, 100):
    x = rng.standard_normal((200000, n))
    s1 = float(stats.skew(x, axis=1, bias=True).std()); s2 = float(stats.kurtosis(x, axis=1, fisher=True, bias=True).std())
    h.execute('fc_ShapeSE(%d)' % n)
    e1 = abs(G(h, 'fcSeS') / s1 - 1); e2 = abs(G(h, 'fcSeK') / s2 - 1); worst = max(worst, e1, e2); rows.append((n, round(s1, 4), round(G(h, 'fcSeS'), 4), round(s2, 4), round(G(h, 'fcSeK'), 4)))
check('A2 a second reference: the SDs of g1 and g2 over 200,000 simulated normal samples at n = 4, 10, 30, 100 (worst gap %.2f%%)' % (100 * worst), worst < 0.01, rows)
h.execute('fc_ShapeSE(3)')
check('A3 at n = 3 the kurtosis has no spread at all: SE(g2) is exactly 0 and SE(g1) is 0.5', G(h, 'fcSeK') == 0 and close(G(h, 'fcSeS'), 0.5))
rr = random.Random(15); bad = []
for i in range(60):
    n = rr.randint(3, 300); sc = 10 ** rr.uniform(-3, 5); xs = [round(rr.gauss(0, 1) ** (3 if i % 3 == 0 else 1) * sc + 7 * sc, 6) for _ in range(n)]
    if len(set(xs)) < 2: continue
    hh = fresh()
    if hh.execute('fc_NormSet(%s, "t", "src")' % lst(xs)) != 1: bad.append((i, 'refused')); continue
    g1 = float(stats.skew(xs, bias=True)); g2 = float(stats.kurtosis(xs, fisher=True, bias=True))
    if not (close(G(hh, 'fcSkw'), g1, 1e-8) and close(G(hh, 'fcKur'), g2, 1e-8) and close(G(hh, 'fcSeS'), se1(n)) and close(G(hh, 'fcSeK'), se2(n))):
        bad.append((i, n, G(hh, 'fcSkw'), g1, G(hh, 'fcKur'), g2, G(hh, 'fcSeS'), se1(n)))
check('A4 60 random samples of 3 to 300 values: g1 and g2 equal SciPy\'s, and the two SEs are taken at the sample\'s own n', not bad, bad[:2])


def run(script, path=PROG, d1=None):
    app = {'D1': [float(v) for v in d1]} if d1 is not None else None
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=app)
    h.press('Enter')                     # the title page takes the first key
    script(h)
    try: res = h.execute('FitCheck()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
    return h, res, err


def s_rossi(h):     # Normality > Preset: Rossi ages; a key passes the page about the data; the Tests soft key; a key and a tap turn the page; Esc; Quit
    h.choose(5); h.choose(1); h.press('Enter'); h.tap(133, 228); h.press('Down'); h.tap(160, 120); h.press('Esc'); h.choose(11)
def s_crim(h):
    h.choose(5); h.choose(2); h.press('Enter'); h.tap(133, 228); h.press('Esc'); h.choose(11)
hR, resR, errR = run(s_rossi); hC, resC, errC = run(s_crim)
ages = [float(v) for v in G(hR, 'fcX')]
check('A5 the Rossi ages preset: n = 432, g1 = %.3f and g2 = %.3f as SciPy has them, SE(g1) = %.3f, SE(g2) = %.3f' % (G(hR, 'fcSkw'), G(hR, 'fcKur'), G(hR, 'fcSeS'), G(hR, 'fcSeK')),
      errR is None and G(hR, 'fcNX') == 432 and close(G(hR, 'fcSkw'), float(stats.skew(ages, bias=True)), 1e-8) and close(G(hR, 'fcKur'), float(stats.kurtosis(ages, bias=True)), 1e-8)
      and close(G(hR, 'fcSeS'), se1(432)) and close(G(hR, 'fcSeK'), se2(432)), (errR, G(hR, 'fcNX')))
nC = int(G(hC, 'fcNX'))
check('A6 the binned crimtab preset (n = %s): the SEs are taken at n too (%.4f and %.4f)' % (format(nC, ','), G(hC, 'fcSeS'), G(hC, 'fcSeK')),
      errC is None and G(hC, 'fcBin') == 1 and nC == 3000 and close(G(hC, 'fcSeS'), se1(nC)) and close(G(hC, 'fcSeK'), se2(nC)), (errC, nC))

print('=== P. the Tests page, line for line')
def testlines(path, loader):
    hh = Harness(path, idle_key=4, home_minus=True, cas='fail'); hh.execute('fc_Init()')
    loader(hh); hh.execute('fc_NTestLines()')
    return hh, [str(l) for l in G(hh, 'fcTL')]
def shape_split(L):
    """the page's lines without its shape lines, and the shape lines: in beta 1g one paragraph ("Skewness ..., excess kurtosis
    ...") that fc_Wrap may cut in two; in beta 1h three paragraphs of one line each"""
    idx = [i for i, l in enumerate(L) if l.startswith('Skewness g') or l.startswith('Excess kurtosis g') or l.startswith('SE: the standard error')]
    for i in list(idx):
        if L[i].startswith('Skewness g') and 'kurtosis' in L[i] and not re.search(r'\d\s*$', L[i]): idx.append(i + 1)      # the wrapped rest of beta 1g's line
    return [l for i, l in enumerate(L) if i not in idx], [l for i, l in enumerate(L) if i in sorted(idx)]
rr = random.Random(4); xs40 = [round(rr.gauss(50, 10), 1) for _ in range(40)]
CASES = [('a random sample of 40', lambda hh: hh.execute('fc_NormSet(%s, "t", "src")' % lst(xs40))),
         ('3 values', lambda hh: hh.execute('fc_NormSet({1,2,4}, "t", "src")')),
         ('the Rossi ages', lambda hh: hh.execute('fc_PreRossi()') if any(k.lower() == 'fc_prerossi' for k in hh.routines) else None)]
okP = True; detP = []; longest = 0
for nm, ld in CASES[:2]:
    ho_, Lo = testlines(OLD, ld); hn_, Ln = testlines(PROG, ld)
    ro, so = shape_split(Lo); rn, sn = shape_split(Ln)
    want = ['Skewness g' + chr(8321) + ' = ' + sgn(G(hn_, 'fcSkw')) + '  (SE %.3f)' % G(hn_, 'fcSeS'),
            'Excess kurtosis g' + chr(8322) + ' = ' + sgn(G(hn_, 'fcKur')) + '  (SE %.3f)' % G(hn_, 'fcSeK'),
            'SE: the standard error in normal samples.']
    good = ro == rn and sn == want and len(so) in (1, 2) and ''.join(so).replace(' ', '') == ('Skewness g' + chr(8321) + ' = ' + sgn(G(ho_, 'fcSkw')) + ',  excess kurtosis g' + chr(8322) + ' = ' + sgn(G(ho_, 'fcKur'))).replace(' ', '')
    okP = okP and good; detP.append((nm, good, so, sn)); longest = max([longest] + [len(l.rstrip()) for l in Ln])
check('P1 a random sample of 40 and 3 values: every other line of the page is beta 1g\'s, and the shape lines are the three expected', okP, detP)
def pagelines(h):
    return [l for s in h.screens if s.lines() and s.lines()[0].startswith('Normality: ') and any(re.match(r'page \d+ of \d+', x) for x in s.lines()) for l in s.lines()]
LR = pagelines(hR); LC = pagelines(hC)
wantR = ['Skewness g' + chr(8321) + ' = ' + sgn(G(hR, 'fcSkw')) + '  (SE %.3f)' % se1(432), 'Excess kurtosis g' + chr(8322) + ' = ' + sgn(G(hR, 'fcKur')) + '  (SE %.3f)' % se2(432), 'SE: the standard error in normal samples.']
wantC = ['Skewness g' + chr(8321) + ' = ' + sgn(G(hC, 'fcSkw')) + '  (SE %.3f)' % se1(nC), 'Excess kurtosis g' + chr(8322) + ' = ' + sgn(G(hC, 'fcKur')) + '  (SE %.3f)' % se2(nC), 'SE: the standard error in normal samples.']
check('P2 on screen, the Rossi ages: "%s", "%s" and the line that says what SE is' % (wantR[0], wantR[1]), all(w in LR for w in wantR), [l for l in LR if 'g' + chr(8321) in l or 'SE' in l])
check('P3 on screen, the binned crimtab heights: "%s" and "%s"' % (wantC[0], wantC[1]), all(w in LC for w in wantC), [l for l in LC if 'g' + chr(8321) in l or 'SE' in l])
check('P4 no line of the Tests page is longer than 46 characters (longest %d)' % longest, longest <= 46)

print('=== E. the edges')
hh = fresh(); r3 = hh.execute('fc_NormSet({1,2,4}, "t", "src")'); hh.execute('fc_NTestLines()'); L3 = [str(l) for l in G(hh, 'fcTL')]
check('E1 three values: loaded, g2 = -1.5 with "(SE 0.000)" beside it, g1 with "(SE 0.500)"', r3 == 1 and close(G(hh, 'fcKur'), -1.5) and any(l.endswith('(SE 0.000)') and l.startswith('Excess') for l in L3) and any(l.endswith('(SE 0.500)') and l.startswith('Skewness') for l in L3), L3[-8:])
ref = []
for nm, data, frag in (('two values', '{1,2}', 'need at least 3 values'), ('every value the same', '{5,5,5,5}', 'Every value is the same'), ('5,001 values', 'MAKELIST(K_,K_,1,5001,1)', 'At most 5,000 values')):
    hh = fresh(); hh.execute('fc_ShapeSE(10)'); a0, b0 = G(hh, 'fcSeS'), G(hh, 'fcSeK')
    try:
        if 'MAKELIST' in data: hh.globals_['FCVBIG'] = [float(v) for v in range(1, 5002)]; r_ = hh.execute('fc_NormSet(FCVBIG, "t", "src")')
        else: r_ = hh.execute('fc_NormSet(%s, "t", "src")' % data)
        e_ = None
    except Exception as ex: r_, e_ = None, '%s: %s' % (type(ex).__name__, str(ex)[:120])
    box = ' '.join(' '.join(m.lines) for m in hh.msgboxes)
    ref.append((nm, e_ is None and r_ == 0 and frag in box and G(hh, 'fcSeS') == a0 and G(hh, 'fcSeK') == b0, e_, r_, box[:80]))
check('E2 two values, every value the same, and 5,001 values: each refused with its sentence, and the SEs are not touched', all(x[1] for x in ref), ref)

print('=== M. the menus and their ways out')
allR = [l for s in hR.screens for l in s.lines()]
check('M1 Normality > Rossi ages > Tests, a key and a tap turn the page, Esc, Quit: no error, and the Quit summary has W', errR is None and isinstance(resR, str) and resR.startswith('FitCheck:') and ' W = ' in resR, (errR, resR))
pg = sorted(set(m.group(0) for l in allR for m in [re.match(r'page \d+ of \d+', l)] if m))
check('M2 the Tests page showed its pages in turn (%s)' % ', '.join(pg), len(pg) >= 2, pg)
def s_esc(h): h.choose(0)
h1, r1, e1 = run(s_esc)
check('M3 Esc at the main menu: "FitCheck: nothing computed", no error', e1 is None and r1 == 'FitCheck: nothing computed', (e1, r1))
def s_esc2(h): h.choose(5); h.choose(0); h.choose(11)
h2, r2, e2 = run(s_esc2)
check('M4 Esc at the Normality menu: back to the main menu with no sample loaded', e2 is None and r2 == 'FitCheck: nothing computed' and G(h2, 'fcHasN') == 0, (e2, r2))
def s_keys(h): h.choose(5); h.choose(1); h.press('Enter'); h.tap(80, 228); h.tap(133, 228); h.tap(26, 228); h.tap(293, 228); h.choose(11)
h3, r3_, e3 = run(s_keys); t3 = [s.lines()[0] for s in h3.screens if s.lines()]
check('M5 the soft keys ECDF, Tests, Q-Q and Menu each do their job (%d screens)' % len(h3.screens), e3 is None and isinstance(r3_, str) and ' W = ' in r3_ and len(h3.screens) >= 4, (e3, r3_, t3[:6]))
def s_my(h): h.choose(5); h.choose(3); h.choose(11)
h4, r4, e4 = run(s_my, d1=[1, 2]); box4 = ' '.join(' '.join(m.lines) for m in h4.msgboxes)
check('M6 My values in D1 with two values: refused with "need at least 3 values", nothing loaded', e4 is None and 'need at least 3 values' in box4 and G(h4, 'fcHasN') == 0, (e4, box4[:120]))
def s_help(h):
    h.choose(10); [h.press('Down') for _ in range(9)]; h.press('Esc'); h.choose(11)
h5, r5, e5 = run(s_help); helpt = sorted(set(s.lines()[0] for s in h5.screens if s.lines() and s.lines()[0].startswith('FitCheck help')))
check('M7 Help paged to its end and left with Esc: 8 pages seen, no error', e5 is None and len(helpt) == 8, (e5, helpt))
# the closing summary after a sample in bins (found on the Virtual Calculator, 15 Nov 2026): beta 1g returned "nothing computed"
hCo, resCo, errCo = run(s_crim, path=OLD)
want = 'FitCheck: binned sample, skewness %s, excess kurtosis %s;' % ('%+.3f' % G(hC, 'fcSkw'), '%+.3f' % G(hC, 'fcKur'))
check('M8 crimtab, Tests, Esc, Quit: the summary names the sample\'s skewness and kurtosis (%r); beta 1g said %r' % (resC, resCo),
      errC is None and resC == want and resCo == 'FitCheck: nothing computed' and want == 'FitCheck: binned sample, skewness +0.050, excess kurtosis +0.170;', (errC, resC, want, resCo))
def s_crim_bins(h): h.choose(5); h.choose(2); h.press('Enter'); h.tap(186, 228); h.press('Esc'); h.choose(11)
h6, r6, e6 = run(s_crim_bins); h6o, r6o, e6o = run(s_crim_bins, path=OLD)
check('M9 crimtab, the Bins key, Esc, Quit: beta 1g\'s summary (%r) with the binned sample\'s two numbers after it' % r6o,
      e6 is None and e6o is None and isinstance(r6o, str) and r6o.startswith('FitCheck: ') and r6 == r6o + want[len('FitCheck:'):], (e6, r6, r6o))
def s_two(h): h.choose(5); h.choose(2); h.press('Enter'); h.press('Esc'); h.choose(5); h.choose(2); h.press('Enter'); h.press('Esc'); h.choose(11)
h7, r7, e7 = run(s_two); h7o, r7o, e7o = run(s_two, path=OLD)
check('M10 crimtab and then the Rossi ages: the summary is the raw sample\'s W alone, as in beta 1g (%r)' % r7, e7 is None and r7 == r7o and ' W = ' in r7 and 'binned' not in r7, (e7, r7, r7o))

print('=== R. regression against beta 1g: the monkey, 30 seeds on both versions')
argv = sys.argv; sys.argv = ['monkey_v1b.py']
import monkey_v1b as MK  # noqa: E402
sys.argv = argv
def skip(lines):
    if not lines: return False
    if lines[0].startswith('Normality: ') and any(re.match(r'page \d+ of \d+', x) for x in lines): return True
    return lines[0].startswith('FitCheck help 5/8') or lines[0].startswith('FitCheck help 8/8')
def one(path, seed):
    rng = random.Random(seed)
    app, kind = MK.random_lists(rng)
    hh = MK.Monkey(path, rng, app, 150)
    for q in range(10): hh.globals_.setdefault('M%d' % q, MK.R.interp.Matrix([[0.0]]))
    m1, mk = MK.random_matrix(seed)
    if m1 is not None: hh.globals_['M1'] = m1
    verdict = 'OK'
    signal.signal(signal.SIGALRM, MK._alarm); signal.alarm(60)
    try: hh.execute('FitCheck()')
    except MK.TimeUp: verdict = 'FREEZE'
    except Exception as e: verdict = 'END ' + type(e).__name__
    finally: signal.alarm(0)
    scr = [tuple(t.text.replace('beta 1h', 'beta 1g') for t in s.texts) for s in hh.screens]
    res = str(hh.result); nb = int(' binned sample, skewness ' in res)
    res = re.sub(r' binned sample, skewness [^;]*;', '', res)          # beta 1h's addition to the summary (M8 to M10 check it)
    if res == 'FitCheck:': res = 'FitCheck: nothing computed'
    return verdict, [('<skipped>',) if skip(list(s)) else s for s in scr], [' '.join(m.lines) for m in hh.msgboxes], res, sum(1 for s in scr if skip(list(s))), nb
diffs = []; nscr = 0; nskip = 0; verd = {}; nbin = 0
for sd in range(1500, 1530):
    a = one(OLD, sd); b = one(PROG, sd)
    nscr += len(b[1]); nskip += b[4]; verd[b[0]] = verd.get(b[0], 0) + 1; nbin += b[5]
    if a[0] != b[0] or a[2] != b[2] or a[3] != b[3] or a[1] != b[1]:
        k = next((i for i, (x, y) in enumerate(zip(a[1], b[1])) if x != y), None)
        diffs.append((sd, a[0], b[0], a[3] == b[3], len(a[1]), len(b[1]), k, (a[1][k][:3], b[1][k][:3]) if k is not None else None))
check('R1 30 seeds: the same verdict, boxes and Quit summary (but for the binned sample\'s two numbers, in %d runs), and all %d screens the same text for text but the %d Tests and help-5/8 pages (%s)' % (nbin, nscr, nskip, verd), not diffs and nscr > 300, diffs[:2])

print('=== H. the help')
def helppages(path):
    hh = Harness(path, idle_key=4, home_minus=True, cas='fail')
    hh.press('Enter'); hh.choose(10); [hh.press('Down') for _ in range(9)]; hh.press('Esc'); hh.choose(11)
    hh.execute('FitCheck()')
    seen, pages = set(), []
    for s in hh.screens:
        L = s.lines()
        if L and L[0].startswith('FitCheck help') and L[0] not in seen: seen.add(L[0]); pages.append(s)
    return pages
po, pn = helppages(OLD), helppages(PROG)
check('H1 eight help pages, titled n/8', len(pn) == 8 and all(pn[i].lines()[0].startswith('FitCheck help %d/8:' % (i + 1)) for i in range(8)), [p.lines()[0] for p in pn])
same = all(po[i].lines() == pn[i].lines() for i in (0, 1, 2, 3, 5, 6))
a5, b5 = [l.rstrip() for l in po[4].lines()], [l.rstrip() for l in pn[4].lines()]; new5 = [l for l in b5 if l not in a5]
check('H2 pages 1 to 4, 6 and 7 are beta 1g\'s word for word; page 5 is beta 1g\'s with two lines more: %r' % (new5,),
      same and [l for l in b5 if l and l not in new5] == [l for l in a5 if l] and len(new5) == 2 and ' '.join(x.strip() for x in new5) == 'Tests page: skewness g' + chr(8321) + ' and excess kurtosis g' + chr(8322) + ', each with its SE if the data are normal.', (same, new5))
t8 = ' '.join(x.strip() for x in pn[7].lines())
check('H3 page 8: "FitCheck does on the Prime what Triola\'s TI-83/84 ... programs do ... written new for the Prime, with none of their code"; the disclaimer as before',
      'FitCheck does on the Prime what Triola\'s TI-83/84 goodness-of-fit and normality programs do' in t8 and 'It was written new for the Prime, with none of their code and without their bugs: the header lists them.' in t8
      and [l for l in po[7].lines() if l.startswith('DISCLAIMER') or 'legal' in l] == [l for l in pn[7].lines() if l.startswith('DISCLAIMER') or 'legal' in l], t8[:300])
check('H4 the word "rework" is nowhere in the program (beta 1g had it %d times)' % len(re.findall('(?i)rework', io.open(OLD, encoding='utf-8').read())), not re.search('(?i)rework', SRC))
longest = max(len(l.rstrip()) for p in pn for l in p.lines()[1:-1])
check('H5 no help line is longer than its 46 characters (longest %d), and every page has at most 14 lines of text' % longest, longest <= 46 and all(len(p.lines()) <= 16 for p in pn), [len(p.lines()) for p in pn])

print('=== D. layout over every beta 1h screen above')
firm = []
for t, f in OV.report().items():
    firm += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
cut = sorted(set(x[0] for v in LF.clipped(OV.RECORDS).values() for x in v))
check('D1 no firm overlap and no text off the screen (text_overlap_v1)', not firm, firm[:4])
check('D2 no number cut short by its width argument (label_fit_v1)', not cut, cut[:4])

print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
