#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_TTestLabG_beta1h.py -- checks TTestLabG beta 1h (14 Nov 2026, round 14), the general version, built from
TTestLab beta 1k by tools/make_tlg1_v3.py.  This script is verify_TTestLab_beta1k.py with the program's names changed
(verify/round14/make_verify_tlg_1h.py); "beta 1j" below reads beta 1g, the general version before.  Three more tests in the same five
steps, the one-sample t-test, the one-proportion z-test and the two-proportion z-test.

  A  static: the header; the routines of beta 1j that were not meant to change are unchanged, word for word; the new
     routines are the ones the header names; every INPUT field is {name,[0]}; no "!="; no menu item over 30 characters.
  B  the three older tests are beta 1j's: scripted sessions on both versions (each older example through its five
     pages, the "Pooled or separate?" page, the flowchart with typed numbers and with D1/D2, a refusal) draw the same
     screens, show the same forms and boxes, and return the same text.
  C  the arithmetic of the new tests against SciPy and statsmodels, through tt_Calc: random cases, every tail and
     alpha the menus offer; scores in a list against scipy.stats.ttest_1samp; z critical against the normal quantile.
  E  the three new examples show the book's numbers (Chapter 9: t(9) = 4.06, p = .003; Chapters 5 and 12: z = -29.1;
     Chapter 11: z = -1.965, p = .049), and two of the book's practice problems come out as its answers do.
  F  every cancel and refusal path of the new code: Esc at each menu, Cancel on each form, each refused read of D1,
     each refused number (its sentence, word for word), the family rule of "Choose the test", "Pooled or separate?" on
     a test that has no such choice.  After a cancel, nothing has changed.
  P  the pages' notes: the count check of step 2 (yes and no, each test), the table-row note and the "just below
     alpha" note of step 5, the soft keys of a z-test, the tails menu in each test's symbols; no menu of more than eight
     items (a ninth is cut off at the bottom of the calculator's screen).
  H  help: three pages with the one header; pages 1 and 2 are beta 1j's but for the page count and one footer; every
     line of page 3 within the screen at the calculator's own glyph widths.
  D  layout over every beta 1k screen drawn above, with the largest numbers the forms allow: text_overlap_v1 (no firm
     overlap, nothing off the screen), label_fit_v1 (no number cut short), every text's right edge at the glyph
     widths, and commas in every number of 1,000 or more (never in a year).
Run from anywhere:   python3 verify/verify_TTestLabG_beta1h.py        (the older version comes from git)
"""
import os, sys, re, json, math, random, subprocess, tempfile, warnings
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
from scipy import stats  # noqa: E402
from statsmodels.stats.proportion import proportions_ztest  # noqa: E402

# ---------------------------------------------------------------- what differs between the advanced and general versions
BASE = '1001032'                                   # the commit that holds the version before
NAME, OLDNAME = 'TTestLabG_beta1h.txt', 'TTestLabG_beta1g.txt'
VER, PROGNAME, ENTRY, TAG = 'beta 1h', 'TTestLabG', 'TTESTLABG()', 'tz'
NOLD = 4                                           # the older examples: start-menu items 2 to NOLD + 1
# (then the start menu's list of the three newer examples, MORE, and its Help, HELP: set below from NOLD)
EX_POOLED, PAIRS = 3, (1, 4)                       # which older example is pooled, and which are dependent samples
HAS_TABLE = False                                  # the general version gives the exact t critical only
YEARS = ('Student 1908', 'Darwin 1876', 'Selective Service, 1970', 'Delacre 2017')    # numbers the program writes as text: no comma
# ----------------------------------------------------------------
T_ = TAG + '_'
MORE, HELP = NOLD + 2, NOLD + 3
PROG = os.path.join('programs', NAME)
tmp = tempfile.mkdtemp(prefix='tlv_')
OLD = os.path.join(tmp, OLDNAME)
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/' + OLDNAME], check=True, capture_output=True).stdout)
SRC = open(PROG, encoding='utf-8').read(); OSRC = open(OLD, encoding='utf-8').read()
GW = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'round11', 'glyph_widths_vc.json'))).items()}
XB, PH = '', ''                        # x-bar and p-hat, HP's private-use glyphs
FAIL, NPASS = [], [0]
OV.install()


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:700]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def width(t, font=1):
    return sum(GW[ord(c)][font - 1] if ord(c) in GW else 8 for c in t)


def g(h, name): return h.globals_[TAG + name]


def U(s):
    """Screen text with the Prime's minus sign (U+2212) read as a hyphen."""
    return s.replace('\u2212', '-') if isinstance(s, str) else s


def sig4(v):
    """A value to 4 significant digits in fixed form, as the program's own routine prints it."""
    if v == 0: return '0'
    d = min(10, max(0, 3 - math.floor(math.log10(abs(v)))))
    return '%.*f' % (d, round(v, d))


def run(script, path=PROG, app=None):
    """One session from the program's start: -> (harness, result text, error)."""
    h = Harness(path, idle_key=4, home_minus=True, app_data=app)
    script(h)
    res = err = None
    try: res = U(h.execute(ENTRY))
    except Exception as e: err = e
    return h, res, err


def clean(h, err):
    q, c, a = h.leftover()
    return err is None and not h.warnings and not q and not c and not a


def page(h, n):
    """The text of step n's page as last drawn, one line per text."""
    for s in reversed(h.screens):
        ls = s.lines()
        if ls and ls[0].startswith('Step %d.' % n): return U('\n'.join(ls))
    return ''


def boxes(h): return [U(m.text) for m in h.msgboxes]


def sig(h, res, err):
    """What a session showed: every screen (texts with their places and colours, shapes, soft keys), every box and
    form, and the result."""
    scr = [([(t.text, t.x, t.y, t.font, t.color) for t in s.texts], [repr(x) for x in s.shapes], s.menu) for s in h.screens]
    frm = [(d.title, d.labels, d.helps, d.after, d.accepted) for d in h.inputs]
    return scr, boxes(h), frm, res, repr(err)


def routines(t):
    """{name: text} of every routine, from its first line to the line before the next routine's comments."""
    out, cur, buf = {}, None, []
    for ln in t.split('\n'):
        m = re.match(r'^(?:LOCAL |EXPORT )?(\w+)\([\w, ]*\)\s*$', ln)
        if m:
            if cur: out[cur] = '\n'.join(buf)
            cur, buf = m.group(1), []
        if cur: buf.append(ln)
    if cur: out[cur] = '\n'.join(buf)
    return dict((k, re.sub(r'(?m)^\s*//.*\n?', '', v).rstrip()) for k, v in out.items())


# ================================================================ A. static
print('=== A. static')
check('A1 the header names %s' % VER, ('// %s - %s' % (PROGNAME.upper(), VER)) in SRC and ('// %s (14 Nov 2026):' % VER) in SRC)
ro, rn = routines(OSRC), routines(SRC)
MEANT = {T_ + x for x in ('Calc', 'TName', 'TDf', 'ShowSteps', 'Curve', 'Step5', 'Compare', 'AskTails', 'AskData', 'Example',
                          'Help', 'Menu', 'Page')} | {ENTRY[:-2]}
NEWR = {T_ + x for x in ('SL', 'Dens', 'ZCrit', 'ZP', 'HS', 'DS', 'One', 'Whole', 'CalcN', 'VN', 'Par', 'Step1N', 'Step2N', 'Step3Z',
                         'Step4N', 'Step5N', 'Fam', 'Pick', 'AskDataN')}
changed = {k for k in ro if k in rn and ro[k] != rn[k]}
check('A2 of the %d routines of the version before, only the %d meant to change did' % (len(ro), len(MEANT)),
      changed == MEANT and not (set(ro) - set(rn)), (sorted(changed ^ MEANT), sorted(set(ro) - set(rn))))
check('A3 the %d new routines are the ones the header names' % len(NEWR), set(rn) - set(ro) == NEWR,
      sorted((set(rn) - set(ro)) ^ NEWR))
hdr = SRC[:SRC.index('// ---------------- shared state')]
check('A3b the header lists each new routine', all(k in hdr for k in NEWR), [k for k in NEWR if k not in hdr])
code = re.sub(r'"[^"\n]*"', '""', re.sub(r'(?m)//.*$', '', SRC))
check('A4 no "!=" in the code, and the code is ASCII outside its strings and comments', '!=' not in code and all(ord(c) < 128 for c in code),
      sorted(set(c for c in code if ord(c) >= 128))[:8])
fields = re.findall(r'INPUT\(\{(.*?)\},"', SRC)
check('A5 every field of the %d forms is {name,[0]}' % len(fields),
      len(fields) >= 5 and all(re.fullmatch(r'(\{\w+,\[0\]\},?)+', f) for f in fields), fields)
lits = [it for m in re.finditer(r'CHOOSE\(\w+,"[^"]*",\{(.*?)\}\);', SRC) for it in re.findall(r'"([^"]*)"', m.group(1))]
check('A6 no written menu item over 30 characters (%d items)' % len(lits), max(len(x) for x in lits) <= 30,
      [x for x in lits if len(x) > 30])

# ================================================================ B. the older tests are the version before's
print('=== B. the three older tests against %s' % OLDNAME)
YES1, NO1, YES2, NO2, RUN = (90, 71), (230, 71), (40, 133), (140, 133), (290, 230)   # the flowchart's boxes


def b_example(k, extra=()):
    def s(h, new):
        h.choose(1 + k)
        h.press('Right', 'Right', 'Right', 'Right', 'Left', 'Left', 'Left', 'Left')
        for e in extra: e(h)
        h.press('Esc')
    return s


def b_compare(h):          # Menu > Pooled or separate?  (a page for independent samples, a box for dependent ones)
    h.press('Enter'); h.choose(3)


def b_flow(taps, data, tails, alpha):
    def s(h, new):
        h.choose(1)
        if new: h.choose(1)                              # Which test? -> two means: the flowchart
        for xy in taps: h.tap(*xy)
        data(h)
        h.choose(tails); h.choose(alpha)
        h.press('Right', 'Right', 'Right', 'Right', 'Esc')
    return s


def typed6(m1, s1, n1, m2, s2, n2):
    return lambda h: (h.choose(1), h.answer({TAG + 'M1': m1, TAG + 'S1': s1, TAG + 'N1': n1, TAG + 'M2': m2, TAG + 'S2': s2, TAG + 'N2': n2}))


def TINY(h):               # a pooled test with SDs typed far too small: t and d are huge
    b_flow((YES1, YES2, RUN), typed6(10000, 0.0001, 9, -10000, 0.0002, 7), 1, 3)(h, True)


def b_refused(h, new):     # N 1 = 1: the box, then the menu, then Quit
    h.choose(1)
    if new: h.choose(1)
    for xy in (YES1, YES2, RUN): h.tap(*xy)
    typed6(10, 2, 1, 11, 2, 9)(h)
    h.choose(1); h.choose(3)
    h.choose(7)


D12 = {'D1': [12, 15, 11, 18, 14, 16, 13], 'D2': [10, 9, 14, 11, 12, 8, 13]}
BS = [('example %d, its five pages forward and back' % k, b_example(k), None) for k in range(1, NOLD + 1)]
BS += [('example %d, then Menu > Pooled or separate?' % k, b_example(k, (b_compare, lambda h: h.press('Enter'))), None)
       for k in range(1, NOLD + 1) if k not in PAIRS]
BS += [('example %d (pairs), then Pooled or separate? (a box)' % k, b_example(k, (b_compare,)), None) for k in PAIRS]
BS += [('flowchart > pooled, typed numbers, two-tailed .05', b_flow((YES1, YES2, RUN), typed6(15.89, 1.45, 44, 16.57, 1.11, 31), 1, 3), None),
       ('flowchart > separate, typed numbers, one-tailed .01', b_flow((YES1, NO2, RUN), typed6(4.8185, 3.28798, 270, 6.4247, 3.74872, 146), 2, 4), None),
       ('flowchart > pooled, raw scores in D1 and D2', b_flow((YES1, YES2, RUN), lambda h: h.choose(2), 3, 2), D12),
       ('flowchart > dependent, pairs in D1 and D2', b_flow((NO1, RUN), lambda h: h.choose(1), 1, 3), D12),
       ('flowchart > dependent, typed mean and SD of the differences', b_flow((NO1, RUN), lambda h: (h.choose(2), h.answer({'dm': 0.182, 'dsd': 0.31, 'dn': 5})), 2, 2), None),
       ('a refused N (1): the box, the menu, Quit', b_refused, None)]
bad = []
for label, s, app in BS:
    ho, r0, e0 = run(lambda h: s(h, False), OLD, app); hn, r1, e1 = run(lambda h: s(h, True), PROG, app)
    if not (sig(ho, r0, e0) == sig(hn, r1, e1) and clean(hn, e1) and len(hn.screens) > 2): bad.append((label, r0, r1, repr(e1), hn.leftover()))
check('B1 %d sessions of the older tests: the same screens, forms, boxes and results as %s' % (len(BS), OLDNAME), not bad, bad[:3])

# ================================================================ C. arithmetic of the new tests
print('=== C. arithmetic against SciPy and statsmodels (through %sCalc)' % T_)
TAILS = [(0, a) for a in (0.20, 0.10, 0.05, 0.02, 0.01, 0.001)] + [(d, a) for d in (-1, 1) for a in (0.10, 0.05, 0.025, 0.01, 0.005, 0.0005)]
ALT = {0: 'two-sided', -1: 'less', 1: 'greater'}; ALTZ = {0: 'two-sided', -1: 'smaller', 1: 'larger'}
hc = Harness(PROG, idle_key=4, home_minus=True)
rng = random.Random(14)


def close(a, b, tol=1e-9): return abs(a - b) <= tol * max(1.0, abs(a), abs(b)) + 1e-13


def calc(**kv):
    for k, v in kv.items(): hc.globals_[TAG + k] = v
    return hc.execute(T_ + 'Calc()')


def beyond(t, c, tl): return (abs(t) > c) if tl == 0 else (t < -c if tl < 0 else t > c)


worst = []
n_cases = 0
for i in range(120):                                   # one sample, from the mean, SD and N
    m = round(rng.uniform(-500, 500), rng.randint(0, 3)); sd = round(10 ** rng.uniform(-2, 2.9), 4); n = int(10 ** rng.uniform(0.31, 4))
    mu = round(m + rng.uniform(-3, 3) * sd / math.sqrt(n), 4)
    for tl, al in TAILS:
        ok = calc(TY=4, SRC=1, MO=m, SO=sd, NO=n, MU=mu, TL=tl, AL=al)
        se = sd / math.sqrt(n); t = (m - mu) / se; df = n - 1; a = al / 2 if tl == 0 else al
        p = min(1, 2 * stats.t.sf(abs(t), df)) if tl == 0 else (stats.t.cdf(t, df) if tl < 0 else stats.t.sf(t, df))
        tc = stats.t.isf(a, df)
        good = (ok == 1 and g(hc, 'OK') == 1 and close(g(hc, 'SE'), se) and close(g(hc, 'T'), t) and g(hc, 'DF') == df and
                close(g(hc, 'P'), p, 1e-8) and close(g(hc, 'TC'), tc, 1e-8) and close(g(hc, 'D'), (m - mu) / sd) and
                bool(g(hc, 'REJ')) == beyond(t, tc, tl))
        n_cases += 1
        if not good: worst.append((m, sd, n, mu, tl, al, g(hc, 'T'), t, g(hc, 'P'), p))
check('C1 one-sample t from the mean, SD and N: %d cases (t, df, SE, p, t critical, d, the decision)' % n_cases, not worst, worst[:2])
worst, n_cases = [], 0
for i in range(60):                                    # one sample, from scores in a list
    n = rng.randint(2, 60); xs = [round(rng.gauss(50, 12), rng.randint(0, 2)) for _ in range(n)]
    if len(set(xs)) == 1: xs[0] += 1
    mu = round(50 + rng.uniform(-8, 8), 1)
    for tl, al in TAILS[::3]:
        ok = calc(TY=4, SRC=2, XO=[float(x) for x in xs], MU=mu, TL=tl, AL=al)
        r = stats.ttest_1samp(xs, mu, alternative=ALT[tl])
        n_cases += 1
        if not (ok == 1 and close(g(hc, 'T'), r.statistic, 1e-8) and close(g(hc, 'P'), r.pvalue, 1e-8) and g(hc, 'DF') == n - 1 and g(hc, 'NO') == n):
            worst.append((xs, mu, tl, g(hc, 'T'), r.statistic))
check('C2 one-sample t from scores (scipy.stats.ttest_1samp): %d cases' % n_cases, not worst, worst[:1])
worst, n_cases = [], 0
for i in range(120):                                   # one proportion
    n = int(10 ** rng.uniform(0, 6)); x = rng.randint(0, n); p0 = round(rng.uniform(0.00001, 0.99999), rng.randint(1, 5))
    p0 = min(0.99999, max(0.00001, p0))
    for tl, al in TAILS:
        ok = calc(TY=5, SRC=1, KA=x, NA=n, P0=p0, TL=tl, AL=al)
        z, p = proportions_ztest(x, n, value=p0, alternative=ALTZ[tl], prop_var=p0)
        zc = stats.norm.isf(al / 2 if tl == 0 else al)
        n_cases += 1
        if not (ok == 1 and close(g(hc, 'T'), z, 1e-8) and close(g(hc, 'P'), min(1, p), 1e-8) and close(g(hc, 'TC'), zc, 1e-8) and
                close(g(hc, 'PA'), x / n) and close(g(hc, 'D'), x / n - p0) and bool(g(hc, 'REJ')) == beyond(z, zc, tl)):
            worst.append((x, n, p0, tl, al, g(hc, 'T'), z, g(hc, 'P'), p))
check('C3 one-proportion z (statsmodels proportions_ztest, SE from p0): %d cases' % n_cases, not worst, worst[:2])
worst, n_cases = [], 0
for i in range(120):                                   # two proportions
    n1 = int(10 ** rng.uniform(0, 6)); n2 = int(10 ** rng.uniform(0, 6)); x1 = rng.randint(0, n1); x2 = rng.randint(0, n2)
    if x1 + x2 in (0, n1 + n2): x1 = 1 if n1 > 1 else 0; x2 = 0 if x1 else 1; n2 = max(n2, 2)
    for tl, al in TAILS:
        ok = calc(TY=6, SRC=1, KA=x1, NA=n1, KB=x2, NB=n2, TL=tl, AL=al)
        z, p = proportions_ztest([x1, x2], [n1, n2], value=0, alternative=ALTZ[tl])
        zc = stats.norm.isf(al / 2 if tl == 0 else al)
        n_cases += 1
        if not (ok == 1 and close(g(hc, 'T'), z, 1e-8) and close(g(hc, 'P'), min(1, p), 1e-8) and close(g(hc, 'TC'), zc, 1e-8) and
                close(g(hc, 'PP'), (x1 + x2) / (n1 + n2)) and close(g(hc, 'D'), x1 / n1 - x2 / n2) and bool(g(hc, 'REJ')) == beyond(z, zc, tl)):
            worst.append((x1, n1, x2, n2, tl, al, g(hc, 'T'), z, g(hc, 'P'), p))
check('C4 two-proportion z (statsmodels, pooled): %d cases' % n_cases, not worst, worst[:2])
calc(TY=5, SRC=1, KA=5, NA=10, P0=0.5, TL=0, AL=0.05)
check('C5 a sample exactly on H0 (5 of 10 against 0.5): z = 0 and the two-tailed p is 1, not above it', g(hc, 'T') == 0 and g(hc, 'P') == 1)
calc(TY=1, SRC=1, M1=15.89, S1=1.45, N1=44, M2=16.57, S2=1.11, N2=31, TL=0, AL=0.05)
check('C6 back on a t-test, the curve is Student\'s again (the height at 0 on 73 df)',
      close(hc.execute(T_ + 'Dens(0)'), stats.t.pdf(0, 73), 1e-9) and hc.execute(T_ + 'SL()') == 't' and hc.execute(T_ + 'TDf()') == 't(73)')
calc(TY=6, SRC=1, KA=48, NA=216, KB=66, NB=216, TL=0, AL=0.05)
check('C7 on a z-test, the curve is the standard normal curve', close(hc.execute(T_ + 'Dens(1.5)'), stats.norm.pdf(1.5), 1e-9) and
      hc.execute(T_ + 'SL()') == 'z' and hc.execute(T_ + 'TDf()') == 'z')

# ================================================================ E. the examples and the book
print('=== E. the new examples show the book\'s numbers')
WALK = ('Right', 'Right', 'Right', 'Right', 'Esc')
h4, r4, e4 = run(lambda h: (h.choose(MORE), h.choose(1), h.press(*WALK)))
check('E1 Student\'s sleep data (Chapter 9): t(9) = 4.06, p = 0.003; SE 0.3890; t critical 2.262; d = 1.28',
      clean(h4, e4) and r4 == PROGNAME + ': t(9) = 4.06, p = 0.003, two-tailed' and 'SE = s/√N = 1.230/√10 = 0.3890' in page(h4, 4) and
      XB + ' = 1.580,   s = 1.230' in page(h4, 1) and 't crit = ±2.262' in page(h4, 3) and 'REJECT H₀.' in page(h4, 5) and
      "Cohen's d = 1.28" in page(h4, 5) and 'One sample:  df = N - 1' in page(h4, 2) and '= 10 - 1 = 9' in page(h4, 2),
      (r4, repr(e4), page(h4, 4)))
h5, r5, e5 = run(lambda h: (h.choose(MORE), h.choose(2), h.press(*WALK)))
check('E2 Castaneda v. Partida (Chapters 5 and 12): z = -29.11; n p0 = 688.2 and n(1 - p0) = 181.8; SE 0.01378',
      clean(h5, e5) and r5 == PROGNAME + ': z = -29.11, p < 0.001, two-tailed' and 'n p₀ = 870 × 0.791 = 688.2' in page(h5, 2) and
      'n(1 - p₀) = 870 × 0.209 = 181.8' in page(h5, 2) and 'Yes: the normal curve fits.' in page(h5, 2) and
      '= √(0.791 × 0.209/870) = 0.01378' in page(h5, 4) and 'z crit = ±1.960' in page(h5, 3) and
      'z obt = -29.115 is beyond z crit = ±1.960:' in page(h5, 5) and 'x = 339 successes in n = 870 cases' in page(h5, 1),
      (r5, repr(e5), page(h5, 5)))
h6, r6, e6 = run(lambda h: (h.choose(MORE), h.choose(3), h.press(*WALK)))
check('E3 the Rossi experiment (Chapter 11): z = -1.965, p = 0.049; pooled p 0.2639; SE 0.04241',
      clean(h6, e6) and r6 == PROGNAME + ': z = -1.96, p = 0.049, two-tailed' and '= 114/432 = 0.2639' in page(h6, 4) and
      '   = 0.04241' in page(h6, 4) and 'z obt = -1.965 is beyond z crit = ±1.960:' in page(h6, 5) and
      'sample 1 (Financial aid) has the lower proportion.' in page(h6, 5) and 'sample 1:  48 and 168' in page(h6, 2) and
      'sample 2:  66 and 150' in page(h6, 2), (r6, repr(e6), page(h6, 4)))
check('E4 the examples\' sources are on step 1', 'Student 1908' in page(h4, 1) and 'Castaneda v. Partida' in page(h5, 1) and '(Rossi)' in page(h6, 1))


def s_new(kind, vals, tails, alpha, d1=False, after=WALK):
    def s(h):
        h.choose(1); h.choose(kind)                      # Choose the test > Which test?
        if kind == 2: h.choose(2 if d1 else 1)
        h.answer(vals)
        h.choose(tails); h.choose(alpha)
        if after: h.press(*after)
    return s


hb, rb, eb = run(s_new(2, {'da': 27.5, 'db': 2, 'dc': 16, 'dd': 28}, 2, 2))
check('E5 Chapter 9, problem 2 (16 bags, mean 27.5, SD 2.0, against 28, one-tailed): t(15) = -1.00, t critical -1.753, retain',
      clean(hb, eb) and rb == PROGNAME + ': t(15) = -1.00, p = 0.167, one-tailed' and 't obt < -1.753' in page(hb, 3) and
      'RETAIN H₀.' in page(hb, 5) and '(27.5 - 28)/0.5000' in page(hb, 4), (rb, repr(eb), page(hb, 3)))
hv, rv, ev = run(s_new(3, {'da': 220, 'db': 400, 'dc': 0.5}, 3, 2))
check('E6 Chapter 9, problem 3 (220 of 400 voters against one half, one-tailed): z = 2.00, p = 0.023, z critical 1.645, reject',
      clean(hv, ev) and rv == PROGNAME + ': z = 2.00, p = 0.023, one-tailed' and 'z crit = 1.645' in page(hv, 3) and
      'REJECT H₀.' in page(hv, 5) and 'The proportion differs from p₀ the way H₁ predicted:' in page(hv, 5), (rv, repr(ev), page(hv, 5)))
SLEEP = [1.2, 2.4, 1.3, 1.3, 0.0, 1.0, 1.8, 0.8, 4.6, 1.4]
hd, rd, ed = run(s_new(2, {'dd': 0}, 1, 3, d1=True), app={'D1': SLEEP})
same = [a == b for a, b in zip([page(hd, k) for k in (2, 3, 4, 5)], [page(h4, k) for k in (2, 3, 4, 5)])]
check('E7 the sleep data typed into D1 give the example\'s steps 2 to 5, and step 1 names D1',
      clean(hd, ed) and rd == r4 and all(same) and 'The sample (D1):  N = 10 scores' in page(hd, 1), (rd, same))
ht, rt, et = run(s_new(4, {'da': 48, 'db': 216, 'dc': 66, 'dd': 216}, 1, 3))
check('E8 the Rossi counts typed give the example\'s steps 2 to 5 (with "Group 1" for the example\'s name)', clean(ht, et) and rt == r6 and
      all(page(ht, k).replace('Group 1', 'Financial aid') == page(h6, k) for k in (2, 3, 4, 5)) and 'Group 1' in page(ht, 1), rt)

# ================================================================ F. cancels and refusals
print('=== F. every cancel and refusal path of the new code')
CAN = PROGNAME + ': cancelled'
F = [('Esc at Which test?', lambda h: (h.choose(1), h.choose(0)), None, 0),
     ('Esc at the list of newer examples (back to the start menu), then Esc there', lambda h: (h.choose(MORE), h.choose(0), h.choose(0)), None, 0),
     ('two means, then Esc on the flowchart', lambda h: (h.choose(1), h.choose(1), h.press('Esc')), None, 0),
     ('one mean, Esc at The sample', lambda h: (h.choose(1), h.choose(2), h.choose(0)), None, 0),
     ('one mean, Cancel on the form', lambda h: (h.choose(1), h.choose(2), h.choose(1), h.answer(CANCEL)), None, 0),
     ('one mean, numbers in, Esc at Tails', lambda h: (h.choose(1), h.choose(2), h.choose(1), h.answer({'da': 5, 'db': 2, 'dc': 9, 'dd': 4}), h.choose(0)), None, 0),
     ('one mean, numbers in, tails chosen, Esc at alpha', lambda h: (h.choose(1), h.choose(2), h.choose(1), h.answer({'da': 5, 'db': 2, 'dc': 9, 'dd': 4}), h.choose(2), h.choose(0)), None, 0),
     ('one mean from D1, no D1', lambda h: (h.choose(1), h.choose(2), h.choose(2)), None, 1),
     ('one mean from D1, one score in D1', lambda h: (h.choose(1), h.choose(2), h.choose(2)), {'D1': [3]}, 1),
     ('one mean from D1, a score of 50 digits', lambda h: (h.choose(1), h.choose(2), h.choose(2)), {'D1': [3, 1e50, 5]}, 1),
     ('one mean from D1, Cancel on the form for mu0', lambda h: (h.choose(1), h.choose(2), h.choose(2), h.answer(CANCEL)), {'D1': SLEEP}, 0),
     ('one proportion, Cancel on the form', lambda h: (h.choose(1), h.choose(3), h.answer(CANCEL)), None, 0),
     ('one proportion, numbers in, Esc at Tails', lambda h: (h.choose(1), h.choose(3), h.answer({'da': 3, 'db': 9, 'dc': 0.5}), h.choose(0)), None, 0),
     ('two proportions, Cancel on the form', lambda h: (h.choose(1), h.choose(4), h.answer(CANCEL)), None, 0),
     ('two proportions, numbers in, Esc at alpha', lambda h: (h.choose(1), h.choose(4), h.answer({'da': 3, 'db': 9, 'dc': 4, 'dd': 9}), h.choose(1), h.choose(0)), None, 0)]
BOX = {7: 'Put the sample in D1 of the Statistics 1Var app: at least 2 scores.', 8: 'Put the sample in D1 of the Statistics 1Var app: at least 2 scores.',
       9: 'Value 2 in D1 has more than 50 digits: too large to work with. Check D1 in the Statistics 1Var app.'}
bad = []
for i, (label, s, app, nbox) in enumerate(F):
    h, r, e = run(s, app=app)
    steps = [x for x in h.screens if x.lines() and x.lines()[0].startswith('Step')]
    if not (clean(h, e) and r == CAN and not steps and len(boxes(h)) == nbox and (i not in BOX or boxes(h) == [BOX[i]])):
        bad.append((label, r, repr(e), boxes(h), h.leftover()))
check('F1 %d ways out before the first page: each returns "%s", draws no page, and shows a box only where one is due' % (len(F), CAN),
      not bad, bad[:3])


def in_session(start, acts):
    """An example on screen, then the menu actions; -> the harness and the pages before and after."""
    def s(h):
        for c in start: h.choose(c)
        acts(h)
        h.press('Esc')
    return run(s)


def first_last(h):
    ps = [x.lines() for x in h.screens if x.menu and x.lines() and x.lines()[0].startswith('Step 1.')]
    return ps[0], ps[-1]


hs, rs, es = in_session((MORE, 3), lambda h: (h.press('Enter'), h.choose(1), h.answer(CANCEL)))
a, b = first_last(hs)
check('F2 Menu > Edit the numbers, Cancel: the numbers, the example\'s names and the pages stay', clean(hs, es) and a == b and rs == r6 and g(hs, 'EX') == NOLD + 3, (rs, repr(es)))
hs, rs, es = in_session((MORE, 3), lambda h: (h.press('Enter'), h.choose(4), h.choose(3), h.answer(CANCEL)))
a, b = first_last(hs)
check('F3 Menu > Choose the test > one proportion, Cancel on its form: the two-proportion test stays', clean(hs, es) and a == b and rs == r6 and g(hs, 'TY') == 6, (rs, repr(es)))
hs, rs, es = in_session((MORE, 3), lambda h: (h.press('Enter'), h.choose(4), h.choose(0)))
a, b = first_last(hs)
check('F4 Menu > Choose the test, Esc at Which test?: nothing changes', clean(hs, es) and a == b and rs == r6, (rs, repr(es)))
hs, rs, es = in_session((MORE, 3), lambda h: (h.press('Enter'), h.choose(4), h.choose(3), h.answer({'da': 220, 'db': 400, 'dc': 0.5}), h.choose(0)))
check('F5 ... a new test with its numbers in, Esc at Tails: the new test runs with the tails and alpha that were on screen',
      clean(hs, es) and rs == PROGNAME + ': z = 2.00, p = 0.046, two-tailed' and g(hs, 'TY') == 5 and g(hs, 'EX') == 0, (rs, repr(es)))
hs, rs, es = in_session((1 + EX_POOLED,), lambda h: (h.press('Enter'), h.choose(4), h.choose(1), [h.tap(*xy) for xy in (YES1, NO2, RUN)], h.choose(1), h.choose(3)))
check('F6 pooled > Choose the test > two means > separate: no form (the two independent tests share their numbers)',
      clean(hs, es) and not hs.inputs and g(hs, 'TY') == 2 and rs.startswith(PROGNAME + ': t(') and g(hs, 'EX') == EX_POOLED, (rs, repr(es), len(hs.inputs)))
hs, rs, es = in_session((1 + EX_POOLED,), lambda h: (h.press('Enter'), h.choose(4), h.choose(4), h.answer({'da': 48, 'db': 216, 'dc': 66, 'dd': 216}), h.choose(1), h.choose(3)))
check('F7 pooled > Choose the test > two proportions: its form, then the Rossi result', clean(hs, es) and rs == r6 and len(hs.inputs) == 1 and
      hs.inputs[0].title == 'Two proportions' and hs.inputs[0].labels == ['x 1:', 'n 1:', 'x 2:', 'n 2:'] and len(hs.inputs[0].helps) == 4, (rs, repr(es)))
for st, nm in (((MORE, 1), 'one-sample t'), ((MORE, 2), 'one proportion'), ((MORE, 3), 'two proportions')):
    hs, rs, es = in_session(st, lambda h: (h.press('Enter'), h.choose(3)))
    a, b = first_last(hs)
    check('F8 Pooled or separate? on the %s example: a box that says the test has no such choice, and the pages stay' % nm,
          clean(hs, es) and a == b and boxes(hs) == ['Pooled or separate variances is a question for a test of TWO independent means. The test on screen has no such choice.'],
          (boxes(hs), repr(es)))
EDIT = ' Choose Edit the numbers to change it.'
BIG = 'A number you typed has more than 50 digits: too large to work with.' + EDIT
REF = [  # (which test, the form's answers, the sentence)
    (2, {'da': 5, 'db': 2, 'dc': 1, 'dd': 4}, 'A one-sample t-test needs N of at least 2.'),
    (2, {'da': 5, 'db': -2, 'dc': 9, 'dd': 4}, 'An SD cannot be negative.'),
    (2, {'da': 5, 'db': 0, 'dc': 9, 'dd': 4}, 'The SD is 0: every score is the same, so there is no t.'),
    (2, {'da': 10001, 'db': 2, 'dc': 9, 'dd': 4}, 'The mean and μ₀ must be from -10,000 to 10,000 and the SD at most 1,000.' + EDIT),
    (2, {'da': 5, 'db': 2, 'dc': 9, 'dd': -10000.5}, 'The mean and μ₀ must be from -10,000 to 10,000 and the SD at most 1,000.' + EDIT),
    (2, {'da': 5, 'db': 1000.01, 'dc': 9, 'dd': 4}, 'The mean and μ₀ must be from -10,000 to 10,000 and the SD at most 1,000.' + EDIT),
    (2, {'da': 5, 'db': 2, 'dc': 10001, 'dd': 4}, 'N can be at most 10,000.' + EDIT),
    (2, {'da': 1e50, 'db': 2, 'dc': 9, 'dd': 4}, BIG), (2, {'da': 5, 'db': 2, 'dc': 9, 'dd': -1e50}, BIG),
    (3, {'da': 3, 'db': 0, 'dc': 0.5}, 'n must be a whole number from 1 to 1,000,000.' + EDIT),
    (3, {'da': 3, 'db': 9.5, 'dc': 0.5}, 'n must be a whole number from 1 to 1,000,000.' + EDIT),
    (3, {'da': 3, 'db': 1000001, 'dc': 0.5}, 'n must be a whole number from 1 to 1,000,000.' + EDIT),
    (3, {'da': 10, 'db': 9, 'dc': 0.5}, 'x, the number of successes, must be a whole number from 0 to n.' + EDIT),
    (3, {'da': -1, 'db': 9, 'dc': 0.5}, 'x, the number of successes, must be a whole number from 0 to n.' + EDIT),
    (3, {'da': 2.5, 'db': 9, 'dc': 0.5}, 'x, the number of successes, must be a whole number from 0 to n.' + EDIT),
    (3, {'da': 3, 'db': 9, 'dc': 0}, 'p₀ must be from 0.00001 to 0.99999.' + EDIT),
    (3, {'da': 3, 'db': 9, 'dc': 1}, 'p₀ must be from 0.00001 to 0.99999.' + EDIT),
    (3, {'da': 3, 'db': 9, 'dc': 0.000001}, 'p₀ must be from 0.00001 to 0.99999.' + EDIT),
    (3, {'da': 3, 'db': 1e50, 'dc': 0.5}, 'n must be a whole number from 1 to 1,000,000.' + EDIT),
    (4, {'da': 3, 'db': 0, 'dc': 4, 'dd': 9}, 'Each n must be a whole number from 1 to 1,000,000.' + EDIT),
    (4, {'da': 3, 'db': 9, 'dc': 4, 'dd': 1000001}, 'Each n must be a whole number from 1 to 1,000,000.' + EDIT),
    (4, {'da': 10, 'db': 9, 'dc': 4, 'dd': 9}, 'Each x, a number of successes, must be a whole number from 0 to its n.' + EDIT),
    (4, {'da': 3, 'db': 9, 'dc': 4.5, 'dd': 9}, 'Each x, a number of successes, must be a whole number from 0 to its n.' + EDIT),
    (4, {'da': 0, 'db': 9, 'dc': 0, 'dd': 7}, 'Every case is a success, or none is: the two samples cannot differ, so there is no z.'),
    (4, {'da': 9, 'db': 9, 'dc': 7, 'dd': 7}, 'Every case is a success, or none is: the two samples cannot differ, so there is no z.')]
bad = []
for kind, vals, sentence in REF:
    h, r, e = run(lambda hh: (s_new(kind, vals, 1, 3, after=None)(hh), hh.choose(7)))
    steps = [x for x in h.screens if x.lines() and x.lines()[0].startswith('Step')]
    if not (clean(h, e) and r == PROGNAME and boxes(h) == [sentence] and not steps and g(h, 'OK') == 0): bad.append((kind, vals, boxes(h), r, repr(e)))
check('F9 %d refused numbers: each its sentence in a box, once, then the menu; no page is drawn' % len(REF), not bad, bad[:3])
h, r, e = run(lambda hh: (s_new(3, {'da': 3, 'db': 0, 'dc': 0.5}, 1, 3, after=None)(hh), hh.choose(1), hh.answer({'da': 220, 'db': 400, 'dc': 0.5}), hh.press('Esc')))
check('F10 after a refusal, Edit the numbers puts the test right', clean(h, e) and r == PROGNAME + ': z = 2.00, p = 0.046, two-tailed', (r, repr(e)))
h, r, e = run(lambda hh: (s_new(2, {'dd': 1e50}, 1, 3, d1=True, after=None)(hh), hh.choose(7)), app={'D1': SLEEP})
check('F11 scores in D1 and a mu0 of 50 digits: refused', clean(h, e) and boxes(h) == [BIG], (boxes(h), repr(e)))
h, r, e = run(s_new(2, {'da': 5.5, 'db': 2, 'dc': 9.9, 'dd': 4}, 1, 3))
check('F12 a typed N of 9.9 is taken as 9 (as the other forms take it)', clean(h, e) and g(h, 'NO') == 9 and r.startswith(PROGNAME + ': t(8)'), r)
forms = {}
for hh in (hb, hv, hd, ht):
    for d in hh.inputs: forms[d.title] = (d.labels, len(d.helps))
check('F13 the four new forms: plain labels, a help line for every field',
      forms == {'One sample': (['Mean:', 'SD:', 'N:', 'μ₀:'], 4), 'One proportion': (['x:', 'n:', 'p₀:'], 3),
                'One sample: scores in D1': (['μ₀:'], 1), 'Two proportions': (['x 1:', 'n 1:', 'x 2:', 'n 2:'], 4)}, forms)

# ================================================================ P. the pages' notes
print('=== P. the pages\' notes')
h, r, e = run(s_new(3, {'da': 1, 'db': 10, 'dc': 0.4}, 1, 3))
check('P1 one proportion with n p0 = 4: step 2 says the curve fits poorly and names the exact binomial test',
      clean(h, e) and 'No: the curve fits poorly, so p is only rough.' in page(h, 2) and 'Use an exact binomial test (FitCheck).' in page(h, 2), page(h, 2))
h, r, e = run(s_new(3, {'da': 1, 'db': 10, 'dc': 0.5}, 1, 3))
check('P2 ... with n p0 = n(1 - p0) = 5 exactly: the curve fits', clean(h, e) and 'Yes: the normal curve fits.' in page(h, 2), page(h, 2))
h, r, e = run(s_new(4, {'da': 4, 'db': 30, 'dc': 12, 'dd': 30}, 1, 3))
check('P3 two proportions with 4 successes in sample 1: step 2 says so and names Fisher\'s exact test',
      clean(h, e) and 'sample 1:  4 and 26' in page(h, 2) and 'No: the curve fits poorly, so p is only rough.' in page(h, 2) and
      "Use Fisher's exact test (ChiTable)." in page(h, 2), page(h, 2))
h, r, e = run(s_new(3, {'da': 531, 'db': 1000, 'dc': 0.5}, 1, 3))
p_lo = 2 * stats.norm.sf(62 / math.sqrt(1000))
check('P4 a p that rounds to alpha (531 of 1,000: p = %.5f): step 5 gives its 4 digits, "just below", beside REJECT' % p_lo,
      clean(h, e) and ('(p = %s: just below α = 0.050.)' % sig4(p_lo)) in page(h, 5) and 'REJECT H₀.' in page(h, 5) and 'p = 0.050, two-tailed' in page(h, 5), page(h, 5))
h, r, e = run(s_new(3, {'da': 1355, 'db': 2610, 'dc': 0.5}, 1, 3))
p_hi = 2 * stats.norm.sf(100 / math.sqrt(2610))
check('P5 ... and from the other side (1,355 of 2,610: p = %.5f): "just above", beside RETAIN' % p_hi,
      clean(h, e) and ('(p = %s: just above α = 0.050.)' % sig4(p_hi)) in page(h, 5) and 'RETAIN H₀.' in page(h, 5), page(h, 5))
h, r, e = run(s_new(2, {'da': 0.23203, 'db': 1, 'dc': 74, 'dd': 0}, 1, 3))
note = '(Table row 60, ±2.000, decides the other way.)'
check('P6 one-sample t = 1.996 on 73 df (exact t critical 1.993): REJECT' + (', and the note that the table\'s row 60 decides the other way' if HAS_TABLE else '; no table-row note in this version'),
      clean(h, e) and 't obt = 1.996 is beyond t crit = ±1.993:' in page(h, 5) and ((note in page(h, 5)) == HAS_TABLE), page(h, 5))
h, r, e = run(s_new(2, {'da': 3, 'db': 2, 'dc': 9, 'dd': 4}, 3, 2))
check('P7 one-tailed, and the sample lies the other way: RETAIN, and the page says so',
      clean(h, e) and 'RETAIN H₀.' in page(h, 5) and 'The sample even differs the other way from H₁.' in page(h, 5), page(h, 5))
h, r, e = run(s_new(2, {'da': 3, 'db': 2, 'dc': 9, 'dd': -4}, 1, 3))
hq, rq, eq = run(s_new(2, {'da': 10000, 'db': 0.0001, 'dc': 9, 'dd': -10000}, 1, 3))
check('P7a an SD typed far too small (d = 200,000,000): step 5 prints "Cohen\'s d > 999.99", clear of the label beside it',
      clean(hq, eq) and "Cohen's d > 999.99  ((" in page(hq, 5) and '200,000,000' not in page(hq, 5), page(hq, 5))
hq, rq, eq = run(TINY)
check('P7b ... and so does the older tests\' step 5 ("Cohen\'s d > 999.99  (pooled s)")', clean(hq, eq) and "Cohen's d > 999.99  (pooled s)" in page(hq, 5), page(hq, 5))
check('P8 a negative mu0 is bracketed in the arithmetic: "(3 - (-4))"', clean(h, e) and '(3 - (-4))/0.6667' in page(h, 4), page(h, 4))
zmenu = [s.menu for s in h6.screens if s.menu][-1]; tmenu = [s.menu for s in h4.screens if s.menu][-1]
check('P9 the soft keys: "2 dist" and "4 z" for a z-test, "2 df" and "4 t" for the one-sample t',
      zmenu == ['1 H', '2 dist', '3 crit', '4 z', '5 end', 'Menu'] and tmenu == ['1 H', '2 df', '3 crit', '4 t', '5 end', 'Menu'], (zmenu, tmenu))
tails = {}
for hh, k in ((hb, 'one mean'), (hv, 'one proportion'), (ht, 'two proportions')):
    tails[k] = [d.items[0] for d in hh.chooses if d.title == 'Tails'][0]
ho, r0, e0 = run(lambda h: b_flow((YES1, YES2, RUN), typed6(15.89, 1.45, 44, 16.57, 1.11, 31), 1, 3)(h, True))
tails['two means'] = [d.items[0] for d in ho.chooses if d.title == 'Tails'][0]
check('P10 the tails menu speaks each test\'s symbols', tails == {'one mean': 'Two-tailed: μ ≠ μ₀', 'one proportion': 'Two-tailed: p ≠ p₀',
                                                               'two proportions': 'Two-tailed: p₁ ≠ p₂', 'two means': 'Two-tailed: μ₁ ≠ μ₂'}, tails)
longest = max((len(it), it) for hh in (h4, hb, hv, hd, ht, ho, hs) for d in hh.chooses for it in d.items)
check('P11 no menu item as shown is over 30 characters (the longest: %d)' % longest[0], longest[0] <= 30, longest)
hx, rx, ex = in_session((2,), lambda h: (h.press('Enter'), h.choose(5), h.choose(NOLD + 3)))
check('P11a Menu > Examples lists the older examples and the three new ones, and its last item runs the Rossi example',
      clean(hx, ex) and rx == r6 and len(hx.chooses[-1].items) == NOLD + 3 and hx.chooses[-1].title == 'Examples', (rx, repr(ex)))
most = max((len(d.items), d.title) for hh in (h4, hb, hv, hd, ht, ho, hs, hx) for d in hh.chooses)
check('P11b no menu has more than eight items, so none is cut off at the bottom of the screen (the most: %d, in "%s")' % most, most[0] <= 8, most)
many = [round(100 + 0.37 * i, 2) for i in range(37)]
h, r, e = run(s_new(2, {'dd': 105}, 1, 3, d1=True), app={'D1': many})
check('P12 37 scores in D1: step 1 shows the first ten and says "... and 27 more"', clean(h, e) and '... and 27 more' in page(h, 1) and
      '100.00' in page(h, 1) and 'N = 37 scores' in page(h, 1), page(h, 1))

# ================================================================ H. help
print('=== H. help')


def helppages(path, item, n):
    h, r, e = run(lambda hh: (hh.choose(item), hh.press(*(['Enter'] * n)), hh.choose(0)), path)
    out = []
    for s in h.screens:
        ls = s.lines()
        if ls and ' help ' in ls[0] and (not out or out[-1].lines() != ls): out.append(s)
    return out, r, clean(h, e)


pn, rh, okh = helppages(PROG, HELP, 3); po, _, _ = helppages(OLD, NOLD + 2, 2)
heads = [p.lines()[0] for p in pn]
check('H1 three help pages with the one header, and Help returns to the start menu', okh and rh == CAN and
      heads == [PROGNAME + ' help 1/3: Keys', PROGNAME + ' help 2/3: The numbers', PROGNAME + ' help 3/3: One sample, proportions'], heads)
diff = []
for i in range(2):
    a = [l.replace('/2:', '/3:') for l in po[i].lines()]; b = pn[i].lines()
    diff += [(i + 1, x, y) for x, y in zip(a, b) if x != y]
check('H2 pages 1 and 2 are the version before\'s but for the page count and page 2\'s footer',
      diff == [(2, 'any key or tap = back', 'any key or tap = next page')], diff)
over = []
for p in pn:
    for t in p.texts:
        if t.x + width(t.text, int(t.font or 1)) > 318: over.append((t.x + width(t.text, int(t.font or 1)), t.text))
check('H3 every help line ends inside the screen at the calculator\'s glyph widths', not over, over)
p3 = '\n'.join(pn[2].lines())
check('H4 page 3 gives the three tests\' formulas and the Inference app\'s names for them',
      all(x in p3 for x in ('t obt = (' + XB + ' - μ₀)/(s/√N), df = N - 1', 'z obt = (' + PH + ' - p₀)/√(p₀(1 - p₀)/n)', 'T-Test: 1 μ', 'Z-Test: 1 π and Z-Test: π₁ - π₂')), p3)

# ================================================================ D. layout
print('=== D. layout over every %s screen drawn above, and with the largest numbers the forms allow' % VER)
BIGS = [TINY, s_new(2, {'da': 10000, 'db': 0.0001, 'dc': 9, 'dd': -10000}, 1, 3), s_new(2, {'da': -10000, 'db': 0.00002, 'dc': 5000, 'dd': 10000}, 2, 2),
        s_new(2, {'da': -10000, 'db': 1000, 'dc': 10000, 'dd': 10000}, 1, 3), s_new(2, {'da': 9999.5, 'db': 999.75, 'dc': 10000, 'dd': -9999.25}, 2, 6),
        s_new(3, {'da': 999999, 'db': 1000000, 'dc': 0.99999}, 1, 6), s_new(3, {'da': 0, 'db': 1000000, 'dc': 0.00001}, 3, 6),
        s_new(4, {'da': 123456, 'db': 1000000, 'dc': 987654, 'dd': 1000000}, 1, 3), s_new(4, {'da': 1, 'db': 1000000, 'dc': 999999, 'dd': 1000000}, 2, 1)]
bad = []
for s in BIGS:
    h, r, e = run(s)
    if not (clean(h, e) and page(h, 5)): bad.append((r, repr(e)))
for d1 in ([123456.789, -98765.4321, 0.00012, 55555.5, 1e7, -2.5e6], [1e49, -1e49, 3, 4], [1234.5 + i for i in range(12)]):
    h, r, e = run(s_new(2, {'dd': 1000}, 1, 3, d1=True), app={'D1': d1})
    # a score of 49 digits gives an SD that the Prime prints in scientific form (the harness notes it): no fault
    q = h.leftover()
    if not (e is None and not any(q) and page(h, 5) and all(w.startswith('STRING(') for w in h.warnings)): bad.append((d1[:2], r, repr(e), h.warnings[:2], q))
check('D0 %d sessions with the largest numbers the forms allow, and wide scores in D1, run to step 5' % (len(BIGS) + 3), not bad, bad[:3])
firm, wide, ungrouped = [], [], []
for tag, f in OV.report().items():
    if NAME[:-4] not in tag: continue
    firm += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
recs = {t: v for t, v in OV.RECORDS.items() if NAME[:-4] in t}
cut = sorted(set(x[0] for v in LF.clipped(recs).values() for x in v))
nscr = 0
for t, rec in recs.items():
    for dg, (cnt, first, d) in rec['screens'].items():
        nscr += 1
        for it in d['items']:
            if 'text' not in it: continue
            tx, x = it['text'], it['x']
            wide.append((x + width(tx, int(it.get('font') or 1) or 1), tx))
            body = tx
            for y in YEARS: body = body.replace(y, '')
            if re.search(r'(?<![\d,.])\d{4,}', body): ungrouped.append(tx)
check('D1 no firm overlap of two texts (text_overlap_v1, %d distinct screens)' % nscr, not firm and nscr > 100, (nscr, firm[:4]))
check('D2 no number cut short by its width argument (label_fit_v1)', not cut, cut[:4])
edge = max(wide)
check('D3 every text ends inside the screen at the calculator\'s glyph widths (the widest ends at x = %d)' % edge[0], edge[0] <= 319, sorted(set(wide))[-4:])
check('D4 every number of 1,000 or more drawn has its commas (years apart)', not ungrouped, sorted(set(ungrouped))[:5])

print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
