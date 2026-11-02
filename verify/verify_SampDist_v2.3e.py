#!/usr/bin/env python3
"""verify_SampDist_v2.3e.py -- checks SampDist v2.3e (1 Nov 2026), the fixes for what the monkey test found in v2.3d
(400 random runs: 20 crashed with a division by zero, 127 more broke):
  - every form field takes a real number only ({name,[0]});
  - a number with more than 50 digits is refused, and so is a sigma/sqrt(n) below 1E-9 or below |mu| x 1E-8
    (sd_Big, sd_Narrow, sd_BadMsg): the window mu +- 4 sigma-x-bar had zero width in 12 digits and the grid divided
    by it, and a little above that the tick loop never ended (the Virtual Calculator, 1 Nov 2026); in the live
    graph n+, n- and nx4 stop before that;
  - a sigma above 1E10 is refused: the density labels then need 13 or more decimals, and STRING(x, 2, d) is
    "Invalid input" for those on the Prime (the Virtual Calculator, 1 Nov 2026; v2.3d stopped so at sigma = 1E12).
    The harness printed any number of decimals; tools/prime_facts_v1.py now makes it refuse them as the Prime does,
    for every run in this script;
  - the upper-tail critical values are -NORMALD_ICDF(0, 1, alpha), not NORMALD_ICDF(0, 1, 1 - alpha).

This is a new script in the repository's present layout (the 19 October scripts read the author's folders). It runs
from verify/ as it is: the program from ../programs, v2.3d from ../programs or git history (Lessons Learned rule 18),
the harness and the overlap recorder from ../tools, hp-prime-kit from $HPKIT.

A  the arithmetic against SciPy: sd_prob for the four regions and sd_crit for the three tails over a grid, the four
   modes end to end (the exported EP_SD_* values), and alpha = 1E-300 now giving finite critical values.
B  every mode and Help run from the menu with ordinary numbers, with no error.
M  the monkey test's findings, one check each, each also run on v2.3d, where it fails: the typed fields; the crash
   inputs refused with a sentence and the program back at its menu; the line (sd_Big, sd_Narrow); the live graph's n
   stopping; the live form refusing; a bound too large; the largest numbers accepted drawing in every mode; every
   new message within 4 lines at 32 characters a line (the Virtual Calculator wrapped 112 characters into 4 lines).
G  static: every routine tagged sd_, only verified glyphs in strings, no "!=".
D  layout: text_overlap_v1 over every screen drawn: no firm overlap, straddle or overrun.

Run:  python3 verify_SampDist_v2.3e.py [SampDist_v2.3e.txt]     (exit code 0 = all passed)
"""
import glob
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import warnings

from scipy.stats import norm

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
_cands = [c for c in (os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
                      HERE) if c]
for cand in reversed(_cands):
    if any(os.path.exists(os.path.join(cand, f)) for f in ('ppl_run_v3e.py', 'text_overlap_v1.py')):
        sys.path.insert(0, cand)
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()      # the device facts the harness does not model yet: STRING(x, 2, d) refuses d >= 13

PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'SampDist_v2.3e.txt')
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', 'SampDist_v2.3e.txt')
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:400]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


OLD_FROM = ['']


def older(name):
    """the previous version: beside this script, in ../programs, in an _superseded_* folder beside it (the author's
    D:\\HP-Prime), or from git history (Lessons Learned rule 18)"""
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


OLD = older('SampDist_v2.3d.txt')


def H(path=PROG):
    return Harness(path, idle_key=4, home_minus=True)


def run(script, path=PROG):
    """the whole program from its menu: script queues the answers; Esc (idle) ends every graph, Cancel the menu"""
    h = H(path)
    script(h)
    h.choose(0)                                          # the menu after the last mode: Cancel
    try:
        res = h.execute('SampDist()')
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:120])
    return h, res, err


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def g(h, k):
    return h.globals_[k]


OV.install()

# ===================================================================== A. arithmetic
print('=== A. the arithmetic against SciPy')
h = H()
worst, n = 0.0, 0
for mu in (0.0, 100.0, -50.0):
    for sg in (1.0, 15.0):
        for nn in (1, 4, 30):
            se = sg / nn ** 0.5
            for lo, hi in ((mu - se, mu + se), (mu - 2.5 * se, mu + 0.3 * se), (mu + 1.1 * se, mu + 3 * se)):
                want = {1: norm.cdf(lo, mu, se), 2: norm.sf(lo, mu, se),
                        3: norm.cdf(hi, mu, se) - norm.cdf(lo, mu, se),
                        4: norm.cdf(lo, mu, se) + norm.sf(hi, mu, se)}
                for t in (1, 2, 3, 4):
                    got = h.execute('sd_prob(%r, %r, %r, %r, %d)' % (mu, se, lo, hi, t))
                    worst = max(worst, abs(got - want[t]))
                    n += 1
check('A1 sd_prob, the four regions, %d cases: SciPy to %.1e' % (n, worst), worst < 1e-12)
worst, n = 0.0, 0
for alp in (0.2, 0.1, 0.05, 0.01, 0.001, 1e-7):
    for t in (1, 2, 3):
        got = h.execute('sd_crit(5.0, 2.0, %r, %d)' % (alp, t))
        if t == 1:
            want = [5 + 2 * norm.ppf(alp)] * 2
        elif t == 2:
            want = [5 + 2 * norm.isf(alp)] * 2
        else:
            want = [5 + 2 * norm.ppf(alp / 2), 5 + 2 * norm.isf(alp / 2)]
        worst = max(worst, max(rel(a, b) for a, b in zip(got, want)))
        n += 1
check('A2 sd_crit, the three tails at six alphas: SciPy to %.1e (relative)' % worst, worst < 1e-12)
c2 = h.execute('sd_crit(0.0, 1.0, 1E-300, 2)')
c3 = h.execute('sd_crit(0.0, 1.0, 1E-300, 3)')
check('A2 alpha = 1E-300: the upper critical value is finite (%.4f, SciPy %.4f) and the two-tailed pair symmetric '
      '(v2.3d took ICDF(1 - alpha) = ICDF(1), infinity)' % (c2[0], norm.isf(1e-300)),
      abs(c2[0] - norm.isf(1e-300)) < 1e-9 and abs(c3[0] + c3[1]) < 1e-9 and abs(c3[1] - norm.isf(5e-301)) < 1e-9,
      (c2, c3))


def s_prob(tail, lo, hi=None, mu=100.0, sg=15.0, nn=30.0):
    def f(h):
        h.choose(1)
        h.answer({'mu': mu, 'sg': sg, 'nn': nn})
        h.choose(tail)
        h.answer({'lo': lo} if hi is None else {'lo': lo, 'hi': hi})
    return f


eps = []
for tail, lo, hi in ((1, 95.0, None), (2, 104.0, None), (3, 97.0, 103.0), (4, 97.0, 103.0)):
    hh, res, err = run(s_prob(tail, lo, hi))
    se = 15 / 30 ** 0.5
    b = lo if hi is None else hi
    want = {1: norm.cdf(lo, 100, se), 2: norm.sf(lo, 100, se), 3: norm.cdf(b, 100, se) - norm.cdf(lo, 100, se),
            4: norm.cdf(lo, 100, se) + norm.sf(b, 100, se)}[tail]
    eps.append((tail, err, round(g(hh, 'EP_SD_P'), 9), round(want, 9)))
check('A3 Find probability from the menu, the four regions (N(100, 15), n = 30): EP_SD_P = SciPy: %s' % eps,
      all(e[1] is None and abs(e[2] - e[3]) < 1e-9 for e in eps), eps)


def s_crit(tail, alp, mu=100.0, sg=15.0, nn=30.0):
    def f(h):
        h.choose(2)
        h.answer({'mu': mu, 'sg': sg, 'nn': nn, 'alp': alp})
        h.choose(tail)
    return f


cv = []
for tail in (1, 2, 3):
    hh, res, err = run(s_crit(tail, 0.05))
    se = 15 / 30 ** 0.5
    want = {1: (100 + se * norm.ppf(0.05),) * 2, 2: (100 + se * norm.isf(0.05),) * 2,
            3: (100 + se * norm.ppf(0.025), 100 + se * norm.isf(0.025))}[tail]
    cv.append((tail, err, round(g(hh, 'EP_SD_LO'), 6), round(g(hh, 'EP_SD_HI'), 6), [round(w, 6) for w in want]))
check('A4 Find critical value from the menu, the three tails at alpha .05: EP_SD_LO/HI = SciPy: %s' % cv,
      all(c[1] is None and abs(c[2] - c[4][0]) < 1e-9 and abs(c[3] - c[4][1]) < 1e-9 for c in cv), cv)

# ===================================================================== B. every mode
print('=== B. every mode and Help from the menu')
flows = []
for name, sc in (('probability', s_prob(3, 97.0, 103.0)), ('critical', s_crit(3, 0.05)),
                 ('compare', lambda h: (h.choose(3), h.answer({'mu': 100.0, 'sg': 15.0, 'n1': 10.0, 'n2': 40.0, 'n3': 160.0}))),
                 ('watch', lambda h: (h.choose(4), h.answer({'mu': 100.0, 'sg': 15.0, 'nn': 30.0}))),
                 ('help', lambda h: h.choose(5))):
    hh, res, err = run(sc)
    flows.append((name, err, len(hh.screens)))
check('B1 each mode and Help, from the menu and back to it, with no error: %s' % flows,
      all(f[1] is None and f[2] > 0 for f in flows), flows)

# ===================================================================== M. the monkey test's findings
print("=== M. the monkey test's findings (1 Nov 2026; each check fails on v2.3d)")
print('   v2.3d for the controls: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))


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


ff = input_fields(SRC)
ffo = input_fields(open(OLD, encoding='utf-8').read()) if OLD else []
typed = all(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for f in ff for x in f)
typed_old = all(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for f in ffo for x in f) if ffo else True
check('M1 all %d forms take real numbers only: every field is {name,[0]} (%d fields), so the form refuses a typed '
      'list; v2.3d\'s were bare names' % (len(ff), sum(len(f) for f in ff)), len(ff) == 10 and typed and not typed_old,
      ff)

NARROW = "σ/√n is too small next to μ for the calculator's 12 digits. Use a larger σ, a smaller n or a μ nearer 0."
WIDE = 'σ can be at most 1E10: a larger σ needs density labels with more decimals than the calculator prints.'
BIG = 'A number you typed has more than 50 digits: too large to work with.'
# each case: the new version's script (it stops at the form: the box comes at once and the program is back at its
# menu), and v2.3d's, which goes on through the tail choice and the bounds to the graph, where v2.3d fails
cases = (
    ('probability, mu = 1E300', lambda h: (h.choose(1), h.answer({'mu': 1E300})),
     lambda h: (h.choose(1), h.answer({'mu': 1E300}), h.choose(1), h.answer({'lo': 1E300})), BIG),
    ('probability, mu = -1E300, sigma = 0.05', lambda h: (h.choose(1), h.answer({'mu': -1E300, 'sg': 0.05})),
     lambda h: (h.choose(1), h.answer({'mu': -1E300, 'sg': 0.05}), h.choose(1), h.answer({'lo': -1E300})), BIG),
    ('critical value, mu = 100, n = 1E300', lambda h: (h.choose(2), h.answer({'mu': 100.0, 'nn': 1E300})),
     lambda h: (h.choose(2), h.answer({'mu': 100.0, 'nn': 1E300}), h.choose(1)), BIG),
    ('critical value, mu = 1E40, sigma = 1', lambda h: (h.choose(2), h.answer({'mu': 1E40, 'sg': 1.0})),
     lambda h: (h.choose(2), h.answer({'mu': 1E40, 'sg': 1.0}), h.choose(1)), NARROW),
    ('compare, sigma = 1E-300', lambda h: (h.choose(3), h.answer({'sg': 1E-300})), None, NARROW),
    ('compare, mu = 1E300', lambda h: (h.choose(3), h.answer({'mu': 1E300, 'n1': 30.0})), None, BIG),
    ('watch, mu = 25, sigma = 1E-300', lambda h: (h.choose(4), h.answer({'mu': 25.0, 'sg': 1E-300, 'nn': 25.0})), None,
     NARROW),
    ('watch, mu = 0.01, sigma = 30, n = 1E300', lambda h: (h.choose(4), h.answer({'mu': 0.01, 'sg': 30.0, 'nn': 1E300})),
     None, BIG),
    ('probability, mu = 1E9, sigma = 0.001', lambda h: (h.choose(1), h.answer({'mu': 1E9, 'sg': 0.001, 'nn': 1.0})),
     lambda h: (h.choose(1), h.answer({'mu': 1E9, 'sg': 0.001, 'nn': 1.0}), h.choose(1), h.answer({'lo': 1E9})),
     NARROW),
)
for name, sc, sco, want in cases[:-1]:
    hn, rn, en = run(sc)
    ho, ro, eo = run(sco or sc, OLD) if OLD else (None, None, 'no v2.3d')
    check('M2 %s: the box "%s", the program back at its menu; v2.3d: %s' % (name, want[:40] + '...', eo or 'no error'),
          en is None and boxes(hn) == [want] and OLD is not None and eo is not None, (en, boxes(hn), eo))
# the last case is the 12-digit one.  The harness counts in Python's 16 digits, so v2.3d draws there without an error.
# The Prime keeps 12 digits: the x axis runs from 999999999.996 to 1000000000.00, the tick step is 0.0005, and
# xv := xv + stp stops moving once xv + 0.0005 rounds back to xv (at 1E9 at the latest), so v2.3d's tick loop
# (WHILE xv <= xhi ...) would never end.  The model below runs that loop in 12-digit decimals, both ways of rounding a
# half; what the Prime does is the Virtual Calculator's to say (docs/changes/SampDist_v2.3e_CHANGES.md).
from decimal import Decimal, Context, ROUND_HALF_UP, ROUND_HALF_EVEN


def tick_loop_12(rnd):
    c = Context(prec=12, rounding=rnd)
    mu, se = Decimal('1E9'), Decimal('0.001')
    ww = max(c.multiply(4, se), min(c.multiply(Decimal('3.5'), se), c.multiply(16, se)))
    xlo, xhi = c.subtract(mu, ww), c.add(mu, ww)
    stp = Decimal('0.0005')                              # sd_NiceNum(0.004/6, 1): f = 6.67 -> 5, times 1E-4
    xv = c.multiply(c.divide(xlo, stp).to_integral_value(rounding='ROUND_CEILING'), stp)
    for k in range(200):
        if xv > c.add(xhi, c.divide(stp, 1000)):
            return 'ends after %d steps' % k
        nxt = c.add(xv, stp)
        if nxt == xv:
            return 'stuck at %s after %d steps' % (xv, k)
        xv = nxt
    return 'still going after 200 steps'


name, sc, sco, want = cases[-1]
hn, rn, en = run(sc)
ho, ro, eo = run(sco, OLD) if OLD else (None, None, 'no v2.3d')
m12 = (tick_loop_12(ROUND_HALF_UP), tick_loop_12(ROUND_HALF_EVEN))
check('M2 %s: the box "%s", the program back at its menu; v2.3d gave no box and drew (%s: the harness has 16 digits); '
      'its tick loop in 12 digits: %s (half up), %s (half even); on the Virtual Calculator v2.3d drew nothing for two '
      'minutes, until On: "Program interrupted" (1 Nov 2026)' % (name, want[:40] + '...', eo or 'no error', m12[0],
                                                                m12[1]),
      en is None and boxes(hn) == [want] and OLD is not None and not boxes(ho) and len(ho.screens) > 0
      and all(t.startswith('stuck') for t in m12), (en, boxes(hn), eo, boxes(ho) if ho else None, m12))

h = H()
line = [(h.execute('sd_Narrow(0, 0.000000001)'), 0), (h.execute('sd_Narrow(0, 0.00000000099)'), 1),
        (h.execute('sd_Narrow(1E9, 10)'), 0), (h.execute('sd_Narrow(1E9, 9.99)'), 1),
        (h.execute('sd_Narrow(-1E9, 9.99)'), 1), (h.execute('sd_Big(9.99E49)'), 0), (h.execute('sd_Big(-1E50)'), 1)]
check('M3 the lines: sigma-x-bar of 1E-9 accepted, 9.9E-10 refused; at mu = +-1E9, 10 accepted and 9.99 refused; '
      '9.99E49 accepted, -1E50 refused: %s' % line, all(a == b for a, b in line), line)


def s_live_x4(h):
    h.choose(1)
    h.answer({'mu': 1E9, 'sg': 100.0, 'nn': 1.0})
    h.choose(1)
    h.answer({'lo': 1E9})
    for _ in range(5):
        h.tap(int(2.5 * 53.4), 230)                      # n x 4, five times


hn, rn, en = run(s_live_x4)
nlast = g(hn, 'EP_SD_SE')
notes = [t for s in hn.screens for t in s.lines() if 'n stops here' in t]
check('M4 the live graph at mu = 1E9, sigma = 100: n x 4 goes 1, 4, 16, 64 and stops before 256 (sigma-x-bar 6.25 < '
      '10), saying "n stops here: ..." (sigma-x-bar left at %.4g)' % nlast,
      en is None and abs(nlast - 12.5) < 1e-9 and notes and 'n stops here: σ/√n would be too small to draw' in notes[0],
      (en, nlast, notes[:1]))
ho, ro, eo = run(s_live_x4, OLD) if OLD else (None, None, 'no v2.3d')
check('M4 control: v2.3d went on to n = 1024 (sigma-x-bar %s) with no note' % (g(ho, 'EP_SD_SE') if ho else '-'),
      OLD is not None and (eo is not None or abs(g(ho, 'EP_SD_SE') - 100 / 1024 ** 0.5) < 1e-9), (eo,))


def s_live_form(h):
    h.choose(1)
    h.answer({'mu': 100.0, 'sg': 15.0, 'nn': 30.0})
    h.choose(1)
    h.answer({'lo': 95.0})
    h.tap(int(3.5 * 53.4), 230)                          # mu, sigma: the form
    h.answer({'mu2': 1E40, 'sg2': 1.0})


hn, rn, en = run(s_live_form)
check('M5 the live graph\'s mu, sigma form with mu = 1E40, sigma = 1: "%s Nothing changed.", and sigma-x-bar stays '
      '%.4f' % (NARROW[:30] + '...', 15 / 30 ** 0.5),
      en is None and boxes(hn) == [NARROW + ' Nothing changed.'] and abs(g(hn, 'EP_SD_SE') - 15 / 30 ** 0.5) < 1e-12,
      (en, boxes(hn)))


def s_bound(h):
    h.choose(1)
    h.answer({'mu': 100.0, 'sg': 15.0, 'nn': 30.0})
    h.choose(3)
    h.answer({'lo': -1E60, 'hi': 103.0})


hn, rn, en = run(s_bound)
check('M6 a bound of -1E60: "A bound you typed has more than 50 digits ...", and the program is back at its menu',
      en is None and boxes(hn) == ['A bound you typed has more than 50 digits: too large to work with.'],
      (en, boxes(hn)))

big = []
for name, sc in (('probability, mu = 1E18, sigma = 1E10', lambda h: (h.choose(1), h.answer({'mu': 1E18, 'sg': 1E10, 'nn': 1.0}), h.choose(3), h.answer({}))),
                 ('probability, mu = 1E18, sigma = 1E10, n = 1, a bound of 9.9E49', lambda h: (h.choose(1), h.answer({'mu': 1E18, 'sg': 1E10, 'nn': 1.0}), h.choose(1), h.answer({'lo': 9.9E49}))),
                 ('critical, mu = 0, sigma = 1E-9', lambda h: (h.choose(2), h.answer({'mu': 0.0, 'sg': 1E-9, 'nn': 1.0}), h.choose(3))),
                 ('critical, mu = 1E18, sigma = 1E10, n = 1', lambda h: (h.choose(2), h.answer({'mu': 1E18, 'sg': 1E10, 'nn': 1.0}), h.choose(3))),
                 ('compare, mu = 1E9, sigma = 1000', lambda h: h.choose(3) or h.answer({'mu': 1E9, 'sg': 1000.0})),
                 ('compare, mu = 0, sigma = 1E10, n = 1, 2, 3', lambda h: h.choose(3) or h.answer({'mu': 0.0, 'sg': 1E10, 'n1': 1.0, 'n2': 2.0, 'n3': 3.0})),
                 ('watch, mu = 1E12, sigma = 1E10, n = 1E12', lambda h: (h.choose(4), h.answer({'mu': 1E12, 'sg': 1E10, 'nn': 1E12}))),
                 ('watch, mu = 0, sigma = 1E10, n = 1', lambda h: (h.choose(4), h.answer({'mu': 0.0, 'sg': 1E10, 'nn': 1.0})))):
    hn, rn, en = run(sc)
    big.append((name, en, boxes(hn)))
check('M7 the largest and smallest numbers accepted draw in every mode with no error and no box (STRING refusing 13 '
      'decimals, as on the Prime): %s' % [(b[0], b[1]) for b in big], all(b[1] is None and not b[2] for b in big), big)

# M9: sigma above 1E10.  v2.3d on the Virtual Calculator, 1 Nov 2026: mu 0, sigma 10^12, n 1, left tail, OK ->
# "SampDist  Error: Invalid input"; in this script's harness (prime_facts_v1) the same STRING(x, 2, 13) error.
w9 = []
for name, sc, sco in (
        ('probability, sigma = 1E12, n = 1', lambda h: (h.choose(1), h.answer({'mu': 0.0, 'sg': 1E12, 'nn': 1.0})),
         lambda h: (h.choose(1), h.answer({'mu': 0.0, 'sg': 1E12, 'nn': 1.0}), h.choose(1), h.answer({}))),
        ('critical value, sigma = 1.0000001E10', lambda h: (h.choose(2), h.answer({'mu': 0.0, 'sg': 1.0000001E10, 'nn': 1.0})),
         None),
        ('compare, sigma = 1E12, n = 1E6, 4E6, 1.6E7 (every sigma/sqrt(n) at most 1E9: sigma itself is the line)',
         lambda h: (h.choose(3), h.answer({'mu': 0.0, 'sg': 1E12, 'n1': 1E6, 'n2': 4E6, 'n3': 1.6E7})), None),
        ('watch, sigma = 5E11', lambda h: (h.choose(4), h.answer({'mu': 0.0, 'sg': 5E11, 'nn': 1.0})), 'same')):
    hn, rn, en = run(sc)
    w9.append((name, en, boxes(hn)))
    ok = en is None and boxes(hn) == [WIDE]
    if sco:
        ho, ro, eo = run(sc if sco == 'same' else sco, OLD) if OLD else (None, None, 'no v2.3d')
        ok = ok and OLD is not None and eo is not None and 'Invalid input' in eo
        check('M9 %s: "%s"; v2.3d: %s' % (name, WIDE[:36] + '...', eo), ok, (en, boxes(hn), eo))
    else:
        check('M9 %s: "%s"' % (name, WIDE[:36] + '...'), ok, (en, boxes(hn)))


def s_live_wide(h):
    h.choose(1)
    h.answer({'mu': 100.0, 'sg': 15.0, 'nn': 30.0})
    h.choose(1)
    h.answer({'lo': 95.0})
    h.tap(int(3.5 * 53.4), 230)                          # mu, sigma: the form
    h.answer({'sg2': 1E11})


hn, rn, en = run(s_live_wide)
check('M9 the live graph\'s mu, sigma form with sigma = 1E11: "%s Nothing changed.", sigma-x-bar stays %.4f'
      % (WIDE[:30] + '...', 15 / 30 ** 0.5),
      en is None and boxes(hn) == [WIDE + ' Nothing changed.'] and abs(g(hn, 'EP_SD_SE') - 15 / 30 ** 0.5) < 1e-12,
      (en, boxes(hn)))



# M10: the density labels left of the axis and the panel's sigma line at the ends of what is accepted.  On the Virtual
# Calculator v2.3e's predecessor wrote "0.00015" at sigma = 15,000 against the axis, and cut the sigma line at
# sigma = 1E10 at the panel's edge.
def ylabels(h):
    """the density labels of the last graph: text left of the axis (x 40), between the header and the axis"""
    return [(t.text, t.x) for t in h.screens[-1].texts if t.x < 40 and 15 < t.y < 150 and t.font in (1, 1.0)]


def sigline(h):
    return [ln for s_ in h.screens for ln in s_.lines() if ln.startswith('σ = ') or ln.startswith('one draw: σ')
            or (ln.startswith('σ = ') and 'σ' in ln[3:])]


m10 = []
for name, sc in (('probability, sigma = 15,000, n = 30', lambda h: (h.choose(1), h.answer({'mu': 0.0, 'sg': 15000.0, 'nn': 30.0}), h.choose(1), h.answer({}))),
                 ('probability, sigma = 1E10, n = 1', lambda h: (h.choose(1), h.answer({'mu': 0.0, 'sg': 1E10, 'nn': 1.0}), h.choose(1), h.answer({}))),
                 ('probability, sigma = 1E-9, n = 1', lambda h: (h.choose(1), h.answer({'mu': 0.0, 'sg': 1E-9, 'nn': 1.0}), h.choose(1), h.answer({}))),
                 ('watch, sigma = 1E10, n = 1', lambda h: (h.choose(4), h.answer({'mu': 0.0, 'sg': 1E10, 'nn': 1.0})))):
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no v2.3d')
    yl, ylo = ylabels(hn), (ylabels(ho) if ho and not eo else [])
    fit = [x + 6 * len(t) <= 40 for t, x in yl]
    fito = [x + 6 * len(t) <= 40 for t, x in ylo]
    sl = [len(x) for x in sigline(hn)]
    slo = [len(x) for x in sigline(ho)] if ho and not eo else []
    m10.append((name, en, yl[:4], all(fit) and yl != [], max(sl or [0]), ylo[:2], all(fito), max(slo or [0]), eo))
check('M10 every density label ends left of the axis (6 px a character, the program\'s own estimate) and the panel\'s '
      'sigma line is at most 50 characters, at sigma = 15,000, 1E10 and 1E-9: %s' % [(m[0][:34], m[2][:2], m[4])
                                                                                   for m in m10],
      all(m[1] is None and m[3] and m[4] <= 50 for m in m10), m10)
check('M10 control: v2.3d\'s labels at sigma = 15,000 ran into the axis (%s) and its sigma line at 1E10 was %s characters'
      % (m10[0][5], m10[1][7]), OLD is not None and not m10[0][6] and m10[1][7] > 50, m10)

msgs = [NARROW, NARROW + ' Nothing changed.', BIG, WIDE, WIDE + ' Nothing changed.',
        'A bound you typed has more than 50 digits: too large to work with.',
        'A bound you typed has more than 50 digits: too large to work with. The bounds did not change.']
lines = [len(textwrap.wrap(m, 32)) for m in msgs]
check('M8 every new box within 4 lines at 32 characters a line: %s' % lines, max(lines) <= 4, lines)

# ===================================================================== G. static
print('=== G. static checks')
code = [ln.split('//')[0] for ln in SRC.split('\n')]
routines = re.findall(r'^([A-Za-z_]\w*)\([^()]*\)\s*$', SRC, re.M)
check('G1 %d routines; every one but the EXPORT is tagged sd_; no "!="' % len(routines),
      all(r.startswith('sd_') or r == 'SampDist' for r in routines) and not any('!=' in c for c in code), routines)
VERIFIED = set('χ²√≥≤≠±×→∞αβμσφθρλ⇆⇅') | {chr(8320), chr(8321), chr(8322), chr(8323), chr(57344), chr(8722), '—', '…', '·'}
glyphs = sorted(set(c for ln in code for c in ln if ord(c) > 126))
check('G1 the glyphs in the code\'s strings are the program\'s own set: %s' % ''.join(glyphs),
      set(glyphs) <= VERIFIED, sorted(set(glyphs) - VERIFIED))

# ===================================================================== D. layout
print('=== D. layout (text_overlap_v1 over every screen above)')
rep = OV.report()
tag = [t for t in rep if t.startswith(os.path.splitext(os.path.basename(PROG))[0])]
f = rep[tag[0]] if tag else None
firm = []
if f:
    firm += [('overlap', c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [('straddle', x['text'], x['edge']) for x in f['straddles'] if x['firm']]
    firm += [('overrun', x['text'], x.get('right')) for x in f['overruns'] if x['firm']]
    print('   screens: %d distinct of %d' % (f['screens_distinct'], f['screens_total']))
check('D1 no firm overlap, frame straddle or overrun on any SampDist screen drawn (%s)' % tag[:1], bool(tag) and not firm,
      firm[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for x in FAIL:
    print('  FAILED: ' + x)
sys.exit(1 if FAIL else 0)
