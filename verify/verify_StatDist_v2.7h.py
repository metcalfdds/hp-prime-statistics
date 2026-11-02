#!/usr/bin/env python3
"""verify_StatDist_v2.7h.py -- checks StatDist v2.7h (1 Nov 2026, night): v2.7g's checks (against v2.7f, as there)
and section Y, the axis labels the Virtual Calculator showed clipped and over each other (against v2.7f, whose
labels v2.7g kept).  v2.7g's
were the fixes for what random use found in v2.7f (the
monkey test, 400 runs: 56 broken; and a sweep of every parameter of all 27 families over the decades 1E-300 .. 1E300):
  - "<>", not "!=" (on the Prime a factorial and a test), in st_fmtp and st_fmtv;
  - every form field takes a real number only ({name,[0]}, 56 forms);
  - what the plot cannot draw is refused with a sentence (st_LimP, asked first by st_AskAB): 50 digits or more, a shape
    outside the range where its family's formulas stay finite, a fitted window past 1E50 or too narrow for 12 digits;
  - four densities without overflow (Burr, Pareto, logistic, Frechet), the same numbers; Zoom- stops at 500 windows.

This is a new script in the repository's present layout.  It runs from verify/ as it is: the program from
../programs, v2.7f from ../programs or git history (Lessons Learned rule 18), the harness, the overlap recorder and
tools/prime_facts_v1.py (the device facts the harness does not model yet) from ../tools, hp-prime-kit from $HPKIT.

R  v2.7g against v2.7f, screen for screen: all 27 families with their default values, both tails and Between, every
   key of the plot, the Numbers and Formula pages, Edit, and Help.  Every text the same but Help's title.
M  the findings, one check each, each also run on v2.7f, where it fails.
A  the four rewritten densities (and the Frechet's CDF and right tail) against SciPy.
G  static: only the routines named below differ; no "!=".
D  layout: text_overlap_v1 over the same runs on both versions: nothing new.

Run:  python3 verify_StatDist_v2.7g.py [StatDist_v2.7g.txt]     (exit code 0 = all passed)
"""
import glob
import os
import re
import signal
import subprocess
import sys
import tempfile
import textwrap
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
_cands = [c for c in (os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
                      HERE) if c]
for cand in reversed(_cands):
    if os.path.exists(os.path.join(cand, 'ppl_run_v3e.py')):
        sys.path.insert(0, cand)
from ppl_run_v3e import Harness, CANCEL  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME = 'StatDist_v2.7h.txt'
PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, NAME)
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:700]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


OLD_FROM = ['']


def older(name):
    """the previous version: beside this script, in ../programs, in an _superseded_* folder, or from git history"""
    for pth in [os.path.join(HERE, name), os.path.join(HERE, '..', 'programs', name)] + \
            sorted(glob.glob(os.path.join(HERE, '_superseded_*', name)), reverse=True):
        if os.path.exists(pth):
            return pth
    root, rel_ = os.path.join(HERE, '..'), 'programs/' + name
    try:
        c = subprocess.run(['git', '-C', root, 'rev-list', '-n', '1', 'HEAD', '--', rel_],
                           capture_output=True, text=True, timeout=60).stdout.strip()
        for ref in ((c + ':' + rel_, c + '^:' + rel_) if c else ()):
            out = subprocess.run(['git', '-C', root, 'show', ref], capture_output=True, timeout=60)
            if out.returncode == 0:
                pth = os.path.join(tempfile.mkdtemp(), name)
                open(pth, 'wb').write(out.stdout)
                OLD_FROM[0] = 'git history'
                return pth
    except Exception:
        pass
    return None


OLD = older('StatDist_v2.7f.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()

# the menus: family id -> (main menu item, item in its sub-menu)
MENU = {1: (2, 1), 2: (2, 2), 3: (2, 3), 18: (2, 4), 4: (2, 5), 5: (2, 6), 19: (2, 7), 6: (2, 8),
        7: (3, 1), 8: (3, 2), 9: (3, 3), 24: (3, 4), 25: (3, 5), 10: (3, 6), 11: (3, 8), 20: (3, 9), 12: (3, 10),
        13: (3, 11), 21: (3, 12), 23: (3, 13), 22: (3, 14), 14: (3, 15),
        15: (4, 1), 16: (4, 2), 17: (4, 3), 26: (4, 4), 27: (4, 5)}
SOFT = lambda k: (int((k - 0.5) * 53.4), 230)  # noqa: E731


class _TO(Exception):
    pass


def _alarm(*a):
    raise _TO()


signal.signal(signal.SIGALRM, _alarm)


def run(script, path=PROG, secs=60):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail')
    script(h)
    signal.alarm(secs)
    try:
        res = h.execute('StatDist()')
        err = None
    except _TO:
        res, err = None, 'FREEZE: no end after %d s' % secs
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:160])
    finally:
        signal.alarm(0)
    return h, res, err


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


def fam(fid, tail, answer=None, keys=(), more=()):
    """family fid, tail 1/2/3, the form (None = as shown), then plot keys/taps, then the queued extra chooses"""
    def f(h):
        mn, ix = MENU[fid]
        h.choose(mn, ix, tail, *more)
        h.answer(answer if answer is not None else {})
        if tail == 3:
            h.answer({})
        for k in keys:
            if isinstance(k, tuple):
                h.tap(*k)
            else:
                h.press(k)
    return f


PLOTKEYS = ('Left', 'Right', 'Right', 'Up', 'Down', 'Plus', 'Minus', 'Minus', 'Zero', 'Enter', 'Enter', 'Enter',
            'Enter', 'Enter')   # ... Enter: options -> Numbers page (any key) -> options -> Formula page (any key)

# ===================================================================== R
print('=== R. v2.7g against v2.7f, screen for screen, every family with its default values')
print('   v2.7f: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))
same, diff, errs, nscr = 0, [], [], 0
for fid in sorted(MENU):
    for tail in (1, 2, 3):
        sc = fam(fid, tail, None, PLOTKEYS, more=(1, 2))
        hn, rn, en = run(sc)
        ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no v2.7f')
        nscr += len(hn.screens)
        if en or eo:
            errs.append((fid, tail, en, eo))
        elif texts(hn) == texts(ho) and rn == ro and boxes(hn) == boxes(ho):
            same += 1
        else:
            k = next((i for i, (a, b) in enumerate(zip(texts(hn), texts(ho))) if a != b), None)
            diff.append((fid, tail, k, [(x, y) for x, y in zip(texts(hn)[k], texts(ho)[k]) if x != y][:3]
                         if k is not None else (boxes(hn), boxes(ho), rn, ro, len(texts(hn)), len(texts(ho)))))
check('R1 27 families x 3 tails (81 runs; the plot\'s every key, the Numbers page, the Formula page): %d screens, '
      'every text, box and the result identical to v2.7f\'s, no error' % nscr,
      OLD is not None and same == 81, (diff[:3], errs[:3]))

hn, rn, en = run(lambda h: h.choose(5))
ho, ro, eo = run(lambda h: h.choose(5), OLD) if OLD else (None, None, 'none')
dif = [(a, b) for a, b in zip(texts(hn), texts(ho)) if a != b]
only = [(sorted(set(a) - set(b)), sorted(set(b) - set(a))) for a, b in dif]
check('R2 Help (%d pages): identical to v2.7f\'s but for the title on each, "Statistical Distributions v2.7h": %s'
      % (len(dif), only[:1]), en is None and eo is None and len(texts(hn)) == len(texts(ho)) and len(dif) >= 1
      and all(o == (['Statistical Distributions v2.7h'], ['Statistical Distributions v2.7f']) for o in only),
      (en, eo, only))

# ===================================================================== M
print("=== M. the findings (1 Nov 2026; each check fails on v2.7f)")


def split_top(t):
    out, d, cur = [], 0, ''
    for ch in t:
        if ch in '([{':
            d += 1
        elif ch in ')]}':
            d -= 1
        if ch == ',' and d == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return out


def input_fields(src):
    code_ = '\n'.join(ln.split('//')[0] for ln in src.split('\n'))
    out = []
    for m in re.finditer(r'\bINPUT\(', code_):
        i = j = m.end()
        d = 0
        while True:
            ch = code_[j]
            if ch in '([{':
                d += 1
            elif ch in ')]}':
                d -= 1
                if d < 0:
                    break
            elif ch == ',' and d == 0:
                break
            j += 1
        a = code_[i:j].strip()
        out.append(split_top(a[1:-1]) if a.startswith('{') else [a])
    return out


ff, ffo = input_fields(SRC), input_fields(OSRC)
typed = all(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for f in ff for x in f)
typed_old = any(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for f in ffo for x in f)
check('M1 all %d forms take real numbers only: every field is {name,[0]} (%d fields); v2.7f\'s were bare names'
      % (len(ff), sum(len(f) for f in ff)), len(ff) == 56 and typed and not typed_old and OLD is not None,
      [f for f in ff if not all(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for x in f)][:3])

code = [ln.split('//')[0] for ln in SRC.split('\n')]
ocode = [ln.split('//')[0] for ln in OSRC.split('\n')]
neq_old = [c.strip() for c in ocode if '!=' in c]
check('M2 no "!=" in the code (on the Prime a factorial and a test: never true, and "Numerical overflow" from 254 '
      'on); v2.7f had %d: %s' % (len(neq_old), neq_old), not any('!=' in c for c in code) and len(neq_old) == 2,
      [c for c in code if '!=' in c])

BIG = 'A number you typed has more than 50 digits: too large to work with.'
REACH = 'These values spread the distribution past 1E50: too large to draw.'
NARROW = ("These values make the distribution too narrow for the calculator's 12 digits. Widen it, or move it "
          "nearer 0.")
cases = [
    ('Normal, mu = 1E300', 1, {'mu': 1E300}, BIG),
    ('Normal, sigma = 1E-300', 1, {'sg': 1E-300}, NARROW),
    ('Normal, x = 1E300', 1, {'x_val': 1E300}, BIG),
    ('Uniform, b = 1E300', 2, {'b_param': 1E300}, BIG),
    ('Exponential, lambda = 1E49', 3, {'lambda': 1E49}, NARROW),
    ('Exponential, lambda = 1E-300', 3, {'lambda': 1E-300}, REACH),
    ('Weibull, k = 0.001', 4, {'ksh': 0.001}, 'For the Weibull, k must be from 0.05 to 100 here.'),
    ('Weibull, scale = 1E-300', 4, {'stS': 1E-300}, NARROW),
    ('LogNormal, mu = 1000', 5, {'mu': 1000.0}, 'For the LogNormal, μ must be from -100 to 100 here.'),
    ('LogNormal, sigma = 1000', 5, {'sg': 1000.0}, 'For the LogNormal, σ can be at most 10 here.'),
    ('Laplace, b = 1E-300', 6, {'bb': 1E-300}, NARROW),
    ('F, df1 = 1E49', 9, {'df1': 1E49}, 'For the F, df1 can be at most 1000000 here.'),
    ('Burr, C = 0.001', 10, {'stC': 0.001}, 'For the Burr, C must be from 0.2 to 100 here.'),
    ('Burr, K = 1000', 10, {'stK': 1000.0}, 'For the Burr, K must be from 0.2 to 100 here.'),
    ('Gumbel, beta = 1E-300', 11, {'be': 1E-300}, NARROW),
    ('Pareto, alpha = 1000', 12, {'al': 1000.0}, 'For the Pareto, α must be from 0.05 to 100 here.'),
    ('Pareto, x_m = 1E-300', 12, {'xm': 1E-300, 'x_val': 2E-300}, NARROW),
    ('Rayleigh, sigma = 1E-300', 13, {'sg': 1E-300}, NARROW),
    ('Logistic, s = 1E-300', 14, {'sc': 1E-300}, NARROW),
    ('binomial, n = 1E49', 15, {'stN': 1E49}, 'For the binomial, n can be at most 100000 here.'),
    ('Poisson, lambda = 1E49', 16, {'lambda': 1E49}, 'For the Poisson, λ can be at most 100000 here.'),
    ('geometric, p = 1E-300', 17, {'stP': 1E-300}, 'For the geometric, p must be at least 0.000001 here.'),
    ('triangular, min = -1E300', 18, {'trA': -1E300}, BIG),
    ('Cauchy, location = 1E300', 19, {'cLoc': 1E300}, BIG),
    ('Frechet, alpha = 0.001', 20, {'frA': 0.001}, 'For the Frechet, α must be from 0.05 to 100 here.'),
    ('Erlang, lambda = 1E-300', 23, {'erL': 1E-300}, REACH),
    ('Poisson, k = 1E49', 16, {'k_val': 1E49}, 'k can be at most 1000000000 here.'),
    ('geometric, k = 1E49', 17, {'k_val': 1E49}, 'k can be at most 1000000000 here.'),
    ('negative binomial, r = 1E49', 26, {'nbR': 1E49}, 'For the negative binomial, r can be at most 1000 here.'),
    ('negative binomial, p = 1E-300', 26, {'nbP': 1E-300}, 'For the negative binomial, p must be at least 0.001 here.'),
]
M3KEYS = ('Minus', 'Plus', 'Plus', 'Left', 'Right', 'Up', 'Zero')     # the sweep's keys, without the menus
for name, fid, form, want in cases:
    sc = fam(fid, 1, form, M3KEYS)
    hn, rn, en = run(sc, secs=30)
    ho, ro, eo = run(sc, OLD, secs=30) if OLD else (None, None, 'no v2.7f')
    check('M3 %s: "%s", back to the menu; v2.7f: %s' % (name, want[:40] + '...', (eo or 'no box')[:100]),
          en is None and boxes(hn) == [want] and (rn or '').startswith('StatDist: ') and OLD is not None
          and eo is not None, (en, boxes(hn), rn, eo))

# mu = 1E40 with sigma = 1: the harness (16 digits) draws it, the Prime (12) cannot
from decimal import Decimal, Context, ROUND_HALF_UP  # noqa: E402
c12 = Context(prec=12, rounding=ROUND_HALF_UP)
lo12 = c12.subtract(Decimal('1E40'), Decimal('3.09023230617'))
hi12 = c12.add(Decimal('1E40'), Decimal('3.09023230617'))
stuck = c12.add(Decimal('1E40'), 1) == Decimal('1E40')
hn, rn, en = run(fam(1, 1, {'mu': 1E40, 'sg': 1.0}, M3KEYS), secs=30)
check('M3 Normal, mu = 1E40, sigma = 1: "%s", back to the menu; v2.7f drew it in the harness (16 digits), but in 12 '
      'its window, mu -/+ 3.09, is %s to %s (no width) and its tick counter n + 1 is n at 1E40 (%s): the tick loop '
      'never ends, as SampDist v2.3d\'s did on the Virtual Calculator' % (NARROW[:40] + '...', lo12, hi12, stuck),
      en is None and boxes(hn) == [NARROW] and lo12 == hi12 and stuck, (en, boxes(hn)))

# ===================================================================== A
print('=== A. the four rewritten densities (and the Frechet CDF and right tail) against SciPy and v2.7f')
from scipy import stats  # noqa: E402

ha = Harness(PROG, idle_key=4, home_minus=True, cas='fail')
ho_ = Harness(OLD, idle_key=4, home_minus=True, cas='fail') if OLD else None
for h_ in (ha, ho_):
    if h_ is not None:
        h_.execute('st_Init()')


def ppl(h_, fn, fid, pars, x):
    try:
        return h_.execute('%s(%d, {%r, %r, %r}, %r)' % (fn, fid, pars[0], pars[1], pars[2], x))
    except Exception as e:
        return 'ERR ' + type(e).__name__


A = []
for C, K, S in ((2, 2, 1), (0.2, 0.2, 1), (100, 100, 1), (3, 0.5, 1000), (0.5, 50, 0.001)):
    for x in (S * 1E-3, S * 0.5, S, S * 2, S * 50, S * 1E4):
        A.append(('st_pdf', 10, (C, K, S), x, stats.burr12(C, K, scale=S).pdf(x)))
for xm, al in ((1, 3), (10, 100), (0.001, 0.05), (1E6, 2.5)):
    for x in (xm, xm * 1.01, xm * 2, xm * 1E3):
        A.append(('st_pdf', 12, (xm, al, 0), x, stats.pareto(al, scale=xm).pdf(x)))
for mu, sc in ((0, 1), (1000, 1), (-5, 0.01)):
    for x in (mu - 700 * sc, mu - 20 * sc, mu - sc, mu, mu + 3 * sc, mu + 400 * sc):
        A.append(('st_pdf', 14, (mu, sc, 0), x, stats.logistic(mu, sc).pdf(x)))
for al, s_, m in ((3, 1, 0), (0.05, 1, 0), (100, 2, 5), (1.5, 0.001, -1)):
    for z in (1E-3, 0.5, 0.95, 1, 1.5, 10, 1E4):
        x = m + s_ * z
        d = stats.invweibull(al, loc=m, scale=s_)
        A.append(('st_pdf', 20, (al, s_, m), x, d.pdf(x)))
        A.append(('st_cdf', 20, (al, s_, m), x, d.cdf(x)))
        A.append(('st_sf', 20, (al, s_, m), x, d.sf(x)))
bad, vs_old, old_n = [], [], 0
for fn, fid, pars, x, want in A:
    got = ppl(ha, fn, fid, pars, x)
    if isinstance(got, str) or not (abs(got - want) <= 1E-9 * abs(want) + 1E-280):
        bad.append((fn, fid, pars, x, got, want))
    if ho_ is not None:
        go = ppl(ho_, fn, fid, pars, x)
        if not isinstance(go, str) and go == go and abs(go) < 1E300:
            old_n += 1
            if not isinstance(got, str) and abs(go - got) > 1E-12 * abs(go) + 1E-290:
                vs_old.append((fn, fid, pars, x, got, go))
check('A1 %d values of the Burr, Pareto and logistic densities and the Frechet density, CDF and right tail, inside '
      'the windows and far out: each within 1E-9 of SciPy (relative), no overflow' % len(A), not bad, bad[:4])
check('A2 where v2.7f gave a finite number (%d of them), v2.7g gives the same to 12 digits' % old_n,
      old_n > 0 and not vs_old, vs_old[:4])

# ===================================================================== G
print('=== G. static checks')


def bodies(txt):
    lns = txt.split('\n')
    heads = [i for i, ln in enumerate(lns) if re.match(r'^(EXPORT\s+)?[A-Za-z_]\w*\([^()]*\)\s*$', ln)]
    out = {}
    for k, i in enumerate(heads):
        nm = re.match(r'^(?:EXPORT\s+)?([A-Za-z_]\w*)', lns[i]).group(1)
        out[nm] = '\n'.join(lns[i:heads[k + 1] if k + 1 < len(heads) else len(lns)])
    return out


upto_end = lambda t: t[:t.index('\nEND;') + 5] if '\nEND;' in t else t  # noqa: E731
strip_c = lambda t: '\n'.join(ln.split('//')[0].rstrip() for ln in t.split('\n'))  # noqa: E731
untype = lambda t: re.sub(r'\{(\w+),\[0\]\}', r'\1', t)  # noqa: E731
bn, bo = bodies(SRC), bodies(OSRC)
changed = sorted(k for k in set(bn) | set(bo) if strip_c(upto_end(bn.get(k, ''))) != strip_c(upto_end(bo.get(k, ''))))
beyond = sorted(k for k in changed if untype(strip_c(upto_end(bn.get(k, '')))) != strip_c(upto_end(bo.get(k, ''))))
WANT = sorted(['st_AskAB', 'st_BigMsg', 'st_Fit', 'st_FitWin', 'st_Init', 'st_LimP', 'st_LimX', 'st_Rng', 'st_Zoom', 'st_cdf',
               'st_fmtp', 'st_fmtv', 'st_pdf', 'st_sf', 'st_show_help', 'st_Draw', 'st_LWd'])   # v2.7h: the labels
asks = [k for k in changed if k.startswith('st_ask_')]
check('G1 beyond the typed fields of the 27 st_ask_* forms (%d changed only there), only these routines differ from '
      'v2.7f, code for code: %s' % (len(asks), beyond), beyond == WANT and len(asks) == 27
      and all(k not in beyond for k in asks), (sorted(set(beyond) - set(WANT)), sorted(set(WANT) - set(beyond))))
routines = re.findall(r'^([A-Za-z_]\w*)\([^()]*\)\s*$', SRC, re.M)
check('G2 %d routines, every one tagged st_ (but the entry StatDist); at most six names on a LOCAL line' % len(routines),
      all(r.startswith('st_') for r in routines) and not [ln for ln in code if re.match(r'\s*LOCAL\b', ln)
                                                          and len(ln.split('LOCAL', 1)[1].split(',')) > 6],
      [r for r in routines if not r.startswith('st_')][:4])

# ===================================================================== D
print('=== D. layout (text_overlap_v1: the R runs and the ends of the new ranges, on both versions)')
OV.RECORDS.clear()
ends = [(4, {'ksh': 0.05}), (4, {'ksh': 100.0}), (5, {'mu': 100.0, 'sg': 0.1}), (5, {'mu': -20.0, 'sg': 10.0}),
        (10, {'stC': 0.2, 'stK': 0.2}), (10, {'stC': 100.0, 'stK': 100.0}), (12, {'al': 0.05}), (12, {'al': 100.0}),
        (20, {'frA': 0.05}), (20, {'frA': 100.0}), (15, {'stN': 100000.0, 'k_val': 50000.0}),
        (16, {'lambda': 100000.0, 'k_val': 100000.0}), (17, {'stP': 0.000001, 'k_val': 1.0}),
        (26, {'nbR': 1000.0, 'nbP': 0.001, 'k_val': 1.0}), (1, {'mu': 1E9, 'sg': 10.0, 'x_val': 1E9}),
        (1, {'mu': 0.0, 'sg': 1E-9, 'x_val': 0.0}), (14, {'mu': 1000.0}), (20, {'x_val': 1E-300})]
d_err = []
for fid, form in ends:
    sc = fam(fid, 1, form, ('Minus',) * 12 + ('Plus', 'Left', 'Right', 'Enter', 'Enter'), more=(1,))
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, None)
    d_err.append((fid, form, en, boxes(hn)[:1], eo))
check('M4 the ends of every new range, and the values v2.7f could not draw, draw with Zoom- twelve times and the '
      'Numbers page: no error, no box: %s' % [(x[0], x[2], x[3]) for x in d_err if x[2] or x[3]][:4],
      not any(x[2] or x[3] for x in d_err), [x for x in d_err if x[2] or x[3]][:4])
for fid in sorted(MENU):
    for tail in (1, 3):
        sc = fam(fid, tail, None, PLOTKEYS, more=(1, 2))
        run(sc)
        if OLD:
            run(sc, OLD)
rep = OV.report()


def firm_of(tag0):
    """the firm findings, each as its layout spot: kind, routine and row(s) -- the same spot with other numbers
    in it (another distribution's labels) counts once"""
    t = [t for t in rep if t.startswith(tag0)]
    f = rep[t[0]] if t else None
    out, ex = set(), {}
    if f:
        for c in f['collisions']:
            if c['severity'] == 'overlap' and c['firm']:
                k = ('overlap', c['func'], c['ay'], c['by'])
                out.add(k)
                ex[k] = (c['a'], c['b'])
        for x in f['straddles'] + f['overruns']:
            if x['firm']:
                k = ('straddle' if 'edge' in x else 'overrun', x['func'], x['y'])
                out.add(k)
                ex[k] = x['text']
        print('   %s: %d distinct screens of %d' % (t[0], f['screens_distinct'], f['screens_total']))
    return bool(t), out, ex


okn, fn, exn = firm_of(os.path.splitext(os.path.basename(PROG))[0])
oko, fo, exo = firm_of('StatDist_v2.7f')
check('D1 the same runs on both versions: no layout spot (kind, routine, row) with a firm overlap, straddle or overrun '
      'on a v2.7g screen that v2.7f\'s screens do not also have (v2.7g: %d spots, v2.7f: %d)' % (len(fn), len(fo)),
      okn and not (fn - fo), [(k, exn[k]) for k in sorted(fn - fo)][:6])

msgs = sorted(set([BIG, REACH, NARROW] + [c[3] for c in cases]))
nl = [len(textwrap.wrap(m, 32)) for m in msgs]
check('M5 every new box within 4 lines at 32 characters a line: %s' % nl, max(nl) <= 4, nl)

def yw(s):
    """a label's width as the programs estimate it: 5.5 px a character, 3 px for the point (n3_YWd, ne_YWd, st_LWd;
    "0.03" is 20 px wide on the Virtual Calculator)"""
    return 5.5 * (len(s) - 1) + 3 if '.' in s else 5.5 * len(s)


def yval(s):
    return float(s.replace('ᴇ', 'e').replace('−', '-').replace('×', '').replace(',', ''))


def close(a, b):
    return abs(a - b) <= 1E-9 * max(abs(a), abs(b), 1E-300)

# ===================================================================== Y
print('=== Y. v2.7h: axis labels never clipped, never over each other; wide density labels in the scientific form')
PREV = OLD     # v2.7f: v2.7g drew its axis labels exactly as v2.7f did (st_Draw unchanged)


def sd_labs(h):
    """the last plot's density labels (x 1, inside the plot) and x labels (the row at y 142)"""
    scr = [s_ for s_ in h.screens if any(t.y == 142 for t in s_.texts)]
    if not scr:
        return [], []
    ys = [t.text for t in scr[-1].texts if t.x == 1 and 12 < t.y < 138]
    xs = sorted((t.x, t.text) for t in scr[-1].texts if t.y == 142)
    return ys, xs


CASES = [('normal sigma %g' % sg, 1, {'mu': 0.0, 'sg': sg, 'x_val': 0.0}) for sg in
         [10.0 ** k for k in (-9, -8, -7, -6, -5, -3, 0, 3, 5, 6, 10, 20, 40)]] + \
        [('exponential lambda 1E-6', 3, {'lambda': 1E-6}), ('exponential lambda 1E6', 3, {'lambda': 1E6}),
         ('Poisson lambda 100000', 16, {'lambda': 100000.0, 'k_val': 100000.0}),
         ('normal mu 1E9 sigma 10', 1, {'mu': 1E9, 'sg': 10.0, 'x_val': 1E9})]
bad, fixed, old_bad = [], [], []
for nm_, fid, ans in CASES:
    hn_, _, en_ = run(fam(fid, 1, ans))
    ho_, _, eo_ = run(fam(fid, 1, ans), PREV) if PREV else (None, None, 'no v2.7f')
    yn, xn = sd_labs(hn_)
    yo, xo = sd_labs(ho_) if ho_ else ([], [])
    over = lambda xs: [(a, b) for a, b in zip(xs, xs[1:]) if a[0] + yw(a[1]) + 3 > b[0]]  # noqa: E731
    ob = [y for y in yo if yw(y) > 35] + over(xo)
    if ob:
        old_bad.append((nm_, ob[0]))
    ok = not en_ and not eo_ and all(yw(y) <= 35 for y in yn) and not over(xn) \
        and all(x + yw(t) <= 322 for x, t in xn) and set(xn) <= set(xo)
    # the density labels: v2.7g's values where it drew them, else a step and its multiples
    if yo and all(yw(y) <= 35 for y in yo):
        ok = ok and yn == yo
    elif yn:
        v = [yval(y) for y in yn]
        ok = ok and all('ᴇ' in y for y in yn) and all(close(v[i], v[0] * (i + 1)) for i in range(len(v)))
        fixed.append((nm_, yn[-1]))
    if not ok:
        bad.append((nm_, yn, yo, xn, en_, eo_))
check('Y1 %d plots at the far scales (normal sigma 1E-9 .. 1E40 and others): density labels at most 35 px wide, '
      'x labels not over each other and inside the screen, every x label one v2.7f drew; density labels v2.7f\'s '
      'where they fitted, else the scientific form (%d plots, e.g. %s)' % (len(CASES), len(fixed), fixed[:3]),
      PREV is not None and not bad and len(fixed) > 0, bad[:2])
check('Y2 v2.7f (and v2.7g, the same) had a density label wider than the margin (clipped by TEXTOUT_P\'s width '
      'limit: "4000000" showed as "400000" on the Virtual Calculator) or x labels over each other in %d of those '
      'plots, normal sigma 1E-7 among them: %s' % (len(old_bad), old_bad[:3]), any(n.startswith('normal sigma 1e-07') for n, _ in old_bad), old_bad)
dr = upto_end(bn.get('st_Draw', ''))
check('Y3 st_Draw clips no label (no width limit on its TEXTOUT_P calls for labels) and asks STRING(x, 2, d) for a '
      'density label only with d at most 12 (the Prime refuses 13)',
      ', 60);' not in dr and 'stPL - 4);' not in dr and 'IF dwD > 12 THEN dwSc := 1; END;' in dr
      and 'WHILE dwV < stYmx AND dwSc == 0 DO' in dr, None)

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
