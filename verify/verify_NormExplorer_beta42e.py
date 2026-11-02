#!/usr/bin/env python3
"""verify_NormExplorer_beta42e.py -- checks NormExplorer beta 42e (1 Nov 2026, night): beta 42d's checks (against
beta 42c, as there) and section Y, the density labels that ran over the axis on the Virtual Calculator (against
beta 42c, whose labels beta 42d kept).  Beta 42d's were the fixes for what the monkey test
found in beta 42c (400 random runs under tools/monkey_v1b.py: 47 broken):
  - every form field takes a real number only ({name,[0]}; 30 runs had a typed list crash later);
  - a mu or sigma the 12 digits cannot draw is refused with a sentence before anything changes: 50 digits or more
    (mu = 1E300 left the window with no width: division by zero, 3 runs), sigma above 1E10 (density labels of 13
    decimals, which STRING refuses on the Prime: 5 runs), sigma too small next to mu (a tick loop that never ends);
    in menu 1, the Z-formula solver, the bounds, mu2, the custom window and every data route;
  - the Explorer stays inside those lines (sigma keys and drag, the mu drag), and its steps round to the step's own
    decimals (a sigma below 0.000001 rounded to 0);
  - the Diagnostics page takes a tap (9 runs waited for a key that never came).

This is a new script in the repository's present layout.  It runs from verify/ as it is: the program from
../programs, beta 42c from ../programs or git history (Lessons Learned rule 18), the harness, the overlap recorder and
tools/prime_facts_v1.py (the device facts the harness does not model yet) from ../tools, hp-prime-kit from $HPKIT.

R  beta 42d against beta 42c, screen for screen, every menu item with ordinary numbers (the Explorer with every key,
   soft key and a drag; all probability, quantile, solver, comparison, data and window items; the animation; Help).
   Every text, box and the result the same, but for the Diagnostics footer, which now says "or tap".
M  the findings, one check each, each also run on beta 42c, where it fails.
G  static: only the routines named below differ; no "!="; no new glyph in the code outside strings.
D  layout: text_overlap_v1 over every beta 42d screen drawn: no firm overlap, straddle or overrun that beta 42c's same
   runs do not also have, and none on the screens only beta 42d can draw.

Run:  python3 verify_NormExplorer_beta42d.py [NormExplorer_beta42d.txt]     (exit code 0 = all passed)
"""
import glob
import os
import re
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

NAME = 'NormExplorer_beta42e.txt'
PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, NAME)
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:600]) if (detail != '' and not ok) else ''))
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


OLD = older('NormExplorer_beta42c.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()

D1 = [12.1, 9.8, 11.4, 10.2, 8.7, 10.9, 11.8, 9.5, 10.4, 10.0, 12.6, 9.1, 10.7, 11.1, 9.9]
C1 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
C2 = [2.3, 4.1, 5.8, 8.4, 9.9, 12.2, 13.8, 16.5]
APP = {'D1': D1, 'C1': C1, 'C2': C2}


def run(script, path=PROG, app=None, call='NormExp()'):
    """NormExp() with script's answers and events queued; Esc whenever it waits with nothing queued; an empty CHOOSE
    queue is Esc too, so the menu ends the run"""
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=APP if app is None else app)
    script(h)
    try:
        res = h.execute(call)
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:160])
    return h, res, err


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


def titles(h):
    return [c.title for c in h.chooses]


def g(h, k):
    return h.globals_.get(k)


SOFT = lambda k: (int((k - 0.5) * 53.4), 230)  # noqa: E731   soft key k (1..6) on the Explorer's strip

# ===================================================================== R
print('=== R. beta 42d against beta 42c, screen for screen, every menu item with ordinary numbers')
print('   beta 42c: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))


def s_explore(h):
    h.choose(1)
    h.answer({'sdMU': 100.0, 'sdSG': 15.0})
    h.choose(2)                                     # the Explorer
    h.press('Left', 'Right', 'Right', 'Up', 'Up', 'Down', 'Plus', 'Minus', 'Minus', 'Minus', 'Zero')
    h.tap(*SOFT(4))                                 # Shade: left
    h.tap(*SOFT(4))                                 # right
    h.tap(*SOFT(4))                                 # between
    h.drag([(150, 120), (170, 120), (190, 120)])    # the nearer bound
    h.tap(*SOFT(1))                                 # Bands
    h.tap(*SOFT(2))                                 # Ref
    h.tap(*SOFT(5))                                 # Hist (none yet: the note)
    h.tap(*SOFT(6))                                 # More: page 2
    h.tap(*SOFT(1))                                 # Bnd A
    h.press('Left', 'Right', 'Right')
    h.tap(*SOFT(2))                                 # Bnd B
    h.press('Right', 'Left')
    h.tap(*SOFT(3))                                 # mu
    h.press('Left', 'Left')
    h.tap(*SOFT(4))                                 # sigma
    h.press('Right', 'Left', 'Left')
    h.tap(*SOFT(4))                                 # back to the default
    h.drag([(174, 100), (200, 100), (220, 100)])    # mu, or a bound near it
    h.tap(*SOFT(6))                                 # More: page 1
    h.press('Enter')                                # Menu


def s_prob(h):
    h.choose(1)
    h.answer({'sdMU': 100.0, 'sdSG': 15.0})
    h.choose(3, 1)
    h.answer({'pcA': 120.0})
    h.choose(3, 2)
    h.answer({'pcA': 180.0})
    h.choose(3, 3)
    h.answer({'pcA': 85.0, 'pcB': 130.0})
    h.choose(3, 4)
    h.answer({'pcA': 130.0, 'pcB': 70.0})
    h.choose(4, 1)
    h.answer({'icP': 0.9})
    h.choose(4, 2)
    h.answer({'icP': 0.05})
    h.choose(4, 3)
    h.answer({'icP': 0.01})
    h.choose(4, 4)
    h.answer({'icP': 0.05})
    h.choose(4, 5)
    h.answer({'icC': 95.0})


def s_solve(h):
    h.choose(5, 1)
    h.answer({'zsX': 130.0, 'zsM': 100.0, 'zsS': 15.0})
    h.choose(5, 2)
    h.answer({'zsZ': -1.5, 'zsM': 500.0, 'zsS': 100.0})
    h.choose(5, 3)
    h.answer({'zsX': 70.0, 'zsZ': 2.0, 'zsS': 5.0})
    h.choose(5, 4)
    h.answer({'zsX': 84.0, 'zsM': 60.0, 'zsZ': 1.2})
    h.choose(5, 4)
    h.answer({'zsX': 50.0, 'zsM': 60.0, 'zsZ': 1.2})         # sigma not positive: the box
    h.choose(5, 1)
    h.answer({'zsX': 1.0, 'zsM': 0.0, 'zsS': 0.0})           # sigma 0: the box


def s_compare(h):
    h.choose(7, 1)
    h.answer({'c2M2': 1.0})
    h.choose(7, 3)
    h.answer({'c2A': 0.05})
    h.choose(7, 2)
    h.choose(7, 3)
    h.answer({'c2A': 1.5})                                   # refused: the box


def s_data(h):
    h.choose(6, 6, 1)                                        # simulate n = 200
    h.choose(6, 1)                                           # D1
    h.choose(6, 2)                                           # C1, C2
    h.choose(6, 3)                                           # residuals
    h.choose(6, 4)                                           # z-scores into D2
    h.choose(6, 7)                                           # clear


def s_window(h):
    h.choose(9, 2)                                           # wide
    h.choose(9, 1)                                           # auto
    h.choose(9, 3)
    h.answer({'swLO': -5.0, 'swHI': 5.0})                    # custom
    h.choose(9, 4)                                           # bands
    h.choose(9, 5)                                           # reference
    h.choose(9, 6)                                           # CDF
    h.choose(9, 7)                                           # show the window
    h.choose(1)
    h.answer({'sdMU': 3.0, 'sdSG': 2.0})                     # custom window cleared: the box
    h.choose(8)                                              # the animation
    h.choose(10)                                             # Help
    h.choose(9, 9)                                           # reset


sessions = [('Explorer', s_explore), ('probability and quantiles', s_prob), ('Z solver', s_solve),
            ('compare curves', s_compare), ('data', s_data), ('window, animation, Help, reset', s_window)]
same, diff, errs, nscr = 0, [], [], 0
for nm, sc in sessions:
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no beta 42c')
    nscr += len(hn.screens)
    if en or eo:
        errs.append((nm, en, eo))
    elif texts(hn) == texts(ho) and rn == ro and boxes(hn) == boxes(ho) and titles(hn) == titles(ho):
        same += 1
    else:
        k = next((i for i, (a, b) in enumerate(zip(texts(hn), texts(ho))) if a != b), None)
        diff.append((nm, k, (texts(hn)[k], texts(ho)[k]) if k is not None else (boxes(hn), boxes(ho), rn, ro)))
check('R1 %d sessions over every menu item (the Explorer with every key, soft key and drags; 4 areas, 5 quantiles, '
      '4 solves, compare and power, simulate, D1, C1/C2, residuals, z-scores, every window item, the animation, Help, '
      'reset): %d screens, every text, box, menu title and the result identical to beta 42c\'s, no error'
      % (len(sessions), nscr), OLD is not None and same == len(sessions), (diff[:1], errs[:2]))


def s_diag(h):
    h.choose(6, 6, 1)
    h.choose(9, 8)                                           # Diagnostics; Esc (a key) leaves it


hn, rn, en = run(s_diag)
ho, ro, eo = run(s_diag, OLD) if OLD else (None, None, 'no beta 42c')
tn, to = texts(hn), texts(ho) if ho else []
dif = [(a, b) for a, b in zip(tn, to) if a != b]
only = [(sorted(set(a) - set(b)), sorted(set(b) - set(a))) for a, b in dif]
check('R2 the Diagnostics page, left with a key: identical to beta 42c\'s but for its footer, "Any key or tap: back to '
      'the menu" (was "Any key: ..."): %s' % (only[:1],),
      en is None and eo is None and len(tn) == len(to) and len(dif) == 1 and only[0] == (
          ['Any key or tap: back to the menu'], ['Any key: back to the menu']) and rn == ro, (en, eo, only[:2]))

# ===================================================================== M
print("=== M. the monkey test's findings (1 Nov 2026; each check fails on beta 42c)")


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
check('M1 all %d forms take real numbers only: every field is {name,[0]} (%d fields); beta 42c\'s were bare names'
      % (len(ff), sum(len(f) for f in ff)), len(ff) == 15 and sum(len(f) for f in ff) == 26 and typed and not typed_old
      and OLD is not None, ff)

BIG = 'A number you typed has more than 50 digits: too large to work with.'
WIDE = 'σ can be at most 1E10: a larger σ needs density labels with more decimals than the calculator prints.'
NARROW = 'σ is too small next to μ for the calculator\'s 12 digits. Use a larger σ or a μ nearer 0.'
GIVES = 'These values give a μ or σ of 1E50 or more: too large to work with.'
ZBIG = 'These values give z beyond 1E50: too large to work with.'
XBIG = 'These values give x beyond 1E50: too large to work with.'
SBIG = 'These values give σ beyond 1E50: too large to work with.'
WNAR = 'This window is too narrow for the calculator\'s 12 digits. Make it wider.'
DBIG = 'A value in the data has more than 50 digits: too large to work with.'
DWIDE = ('The data\'s s is above 1E10: a larger s needs density labels with more decimals than the calculator '
         'prints.')
DNAR = ('The data\'s s is too small next to their mean for the calculator\'s 12 digits. Subtract one number from every '
        'value.')
CBIG = 'A value in C1 or C2 has more than 50 digits: too large to work with.'
ZDBIG = 'A value in D1 has more than 50 digits: too large to work with.'
START = 'NormExp — N(0.00, 1.00)'


def then_draw(h):
    """after the refusal: the probability item on whatever the session is, so a bad session would be drawn"""
    h.choose(3, 1)
    h.answer({'pcA': 0.5})


cases = [
    ('menu 1, mu = 1E300', lambda h: (h.choose(1), h.answer({'sdMU': 1E300, 'sdSG': 1.0})), BIG, None),
    ('menu 1, mu = -1E300', lambda h: (h.choose(1), h.answer({'sdMU': -1E300, 'sdSG': 1.0})), BIG, None),
    ('menu 1, sigma = 1E300', lambda h: (h.choose(1), h.answer({'sdMU': 0.0, 'sdSG': 1E300})), BIG, None),
    ('menu 1, sigma = 1.23E12', lambda h: (h.choose(1), h.answer({'sdMU': 0.0, 'sdSG': 1234567890123.0})), WIDE, None),
    ('menu 1, sigma = 1E-300', lambda h: (h.choose(1), h.answer({'sdMU': 0.0, 'sdSG': 1E-300})), NARROW, None),
    ('menu 1, mu = 1E9, sigma = 0.001', lambda h: (h.choose(1), h.answer({'sdMU': 1E9, 'sdSG': 0.001})), NARROW, None),
    ('solve mu: z = -1E300, sigma = 1', lambda h: (h.choose(5, 3), h.answer({'zsX': 0.0, 'zsZ': -1E300, 'zsS': 1.0})),
     BIG, None),
    ('solve x: mu = 1E300', lambda h: (h.choose(5, 2), h.answer({'zsZ': 1.0, 'zsM': 1E300, 'zsS': 1.0})), BIG, None),
    ('solve z: sigma = 1E12', lambda h: (h.choose(5, 1), h.answer({'zsX': 1.0, 'zsM': 3.0, 'zsS': 1E12})), WIDE,
     None),
    ('solve z: x = 1E49, sigma = 1E-9', lambda h: (h.choose(5, 1), h.answer({'zsX': 1E49, 'zsM': 0.0, 'zsS': 1E-9})),
     ZBIG, None),
    ('solve x: z = 1E49, sigma = 1E10', lambda h: (h.choose(5, 2), h.answer({'zsZ': 1E49, 'zsM': 0.0, 'zsS': 1E10})),
     XBIG, None),
    ('solve mu: z = 1E49, sigma = 1E10', lambda h: (h.choose(5, 3), h.answer({'zsX': 0.0, 'zsZ': 1E49, 'zsS': 1E10})),
     GIVES, None),
    ('solve sigma: x = 1E49, z = 1E-49', lambda h: (h.choose(5, 4), h.answer({'zsX': 1E49, 'zsM': 0.0, 'zsZ': 1E-49})),
     SBIG, None),
    ('solve sigma: x = 1, z = 1E12', lambda h: (h.choose(5, 4), h.answer({'zsX': 1.0, 'zsM': 0.0, 'zsZ': 1E12})),
     NARROW, None),
    ('menu 3, x = 1E300', lambda h: (h.choose(3, 1), h.answer({'pcA': 1E300})), BIG, None),
    ('menu 3, a = -1E300', lambda h: (h.choose(3, 3), h.answer({'pcA': -1E300, 'pcB': 1.0})), BIG, None),
    ('menu 7, mu2 = 1E300', lambda h: (h.choose(7, 1), h.answer({'c2M2': 1E300})), BIG, None),
    ('custom window 0 .. 1E-300', lambda h: (h.choose(9, 3), h.answer({'swLO': 0.0, 'swHI': 1E-300})), WNAR, None),
    ('custom window 1E9 .. 1E9 + 0.001', lambda h: (h.choose(9, 3), h.answer({'swLO': 1E9, 'swHI': 1E9 + 0.001})),
     WNAR, None),
    ('custom window -1E300 .. 0', lambda h: (h.choose(9, 3), h.answer({'swLO': -1E300, 'swHI': 0.0})), BIG, None),
    ('D1 with 1E300', lambda h: h.choose(6, 1), DBIG, {'D1': [1.0, 2.0, 1E300]}),
    ('D1 with s = 1E11', lambda h: h.choose(6, 1), DWIDE, {'D1': [0.0, 1E11, 2E11]}),
    ('D1 at 1E9, s = 0.01 (12 digits each)', lambda h: h.choose(6, 1), DNAR, {'D1': [1E9, 1E9 + 0.01, 1E9 + 0.02]}),
    ('C1 with -1E300 (two groups)', lambda h: h.choose(6, 2), CBIG, {'C1': [1.0, -1E300], 'C2': [1.0, 2.0]}),
    ('C2 with 1E300 (residuals)', lambda h: h.choose(6, 3), CBIG, {'C1': [1.0, 2.0, 3.0], 'C2': [1.0, 1E300, 2.0]}),
    ('D1 with 1E300 (z-scores)', lambda h: h.choose(6, 4), ZDBIG, {'D1': [1.0, 1E300]}),
]
for name, sc, want, app in cases:
    full = lambda h, sc=sc: (sc(h), then_draw(h))  # noqa: E731
    hn, rn, en = run(full, app=app)
    ho, ro, eo = run(full, OLD, app=app) if OLD else (None, None, 'no beta 42c')
    menu_after = [t for t in titles(hn) if t.startswith('NormExp')]
    old_ok = ho is not None and eo is None and want in boxes(ho)
    check('M2 %s: "%s", the session unchanged (%s), and drawing goes on; beta 42c: %s' % (
        name, want[:34] + '...', menu_after[1] if len(menu_after) > 1 else '?',
        (eo or ('no box' if not boxes(ho) else boxes(ho)[0][:30])) if ho else '-'),
        en is None and want in boxes(hn) and len(menu_after) >= 2 and menu_after[1] == START and OLD is not None
        and not old_ok, (en, boxes(hn), menu_after[:3], eo, boxes(ho)[:2] if ho else None))

# the lines themselves (ne_BadDist, ne_BigMsg)
h = Harness(PROG, idle_key=4, home_minus=True, cas='fail')
h.execute('ne_ResetAll()')
lines_ = [('ne_BadDist(0, 0.000000001, 0)', ''), ('ne_BadDist(0, 0.00000000099, 0)', 'N'),
          ('ne_BadDist(1E9, 10, 0)', ''), ('ne_BadDist(-1E9, 9.99, 0)', 'N'),
          ('ne_BadDist(1E18, 10000000000, 0)', ''), ('ne_BadDist(0, 10000000001, 0)', 'W'),
          ('ne_BadDist(9.9E49, 1, 0)', 'N'), ('ne_BadDist(1E50, 1E45, 0)', 'G'),
          ('ne_BigMsg(-9.99E49)', ''), ('ne_BigMsg(1E50)', 'B')]
code_of = {'': '', BIG: 'B', WIDE: 'W', NARROW: 'N', GIVES: 'G'}
got = [code_of.get(h.execute(e), '?') for e, _ in lines_]
check('M3 the lines: sigma 1E-9 accepted, 9.9E-10 refused; at mu = +-1E9 sigma 10 accepted, 9.99 refused; sigma 1E10 '
      'accepted at mu = 1E18, 1E10 + 1 refused; 50 digits refused, 9.99E49 not: %s' % got,
      got == [b for _, b in lines_], (got, [b for _, b in lines_]))


def explorer(path, setup, events, after=None):
    """the Explorer on its own, from a set-up session; returns the harness, mu and sigma after it, the error"""
    hh = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=APP)
    try:
        hh.execute('ne_ResetAll()')
        for k, v in setup.items():
            hh.globals_[k] = v
        hh.execute('ne_AutoWin()')
        events(hh)
        hh.execute('ne_Explorer()')
        if after:
            after(hh)
        err = None
    except Exception as e:
        err = '%s: %s' % (type(e).__name__, str(e)[:160])
    return hh, g(hh, 'NE_MU'), g(hh, 'NE_SG'), err


def ups(n, key='Up'):
    return lambda hh: hh.press(*([key] * n))


hn, mn, sn, en = explorer(PROG, {'NE_MU': 0.0, 'NE_SG': 1E10}, ups(20))
ho, mo, so, eo = explorer(OLD, {'NE_MU': 0.0, 'NE_SG': 1E10}, ups(20)) if OLD else (None, None, None, 'none')
check('M4 sigma up twenty times from 1E10 in the Explorer: sigma stays 1E10 (%s), no error; beta 42c: %s' % (
    sn, eo or 'sigma %s' % so), en is None and sn == 1E10 and OLD is not None and (eo is not None or so > 1E10),
    (en, sn, eo, so))


def down_centre(hh):
    for _ in range(5):
        hh.press(*(['Down'] * 12))
        hh.press('Zero')                                     # Centre: the steps refit to the new sigma


hn, mn, sn, en = explorer(PROG, {'NE_MU': 1E9, 'NE_SG': 10.0}, down_centre)
ho, mo, so, eo = explorer(OLD, {'NE_MU': 1E9, 'NE_SG': 10.0}, down_centre) if OLD else (None, None, None, 'none')
check('M4 sigma down, Centre, five times at mu = 1E9, sigma = 10: sigma stays 10, the narrowest 12 digits draw there '
      '(%s); beta 42c went to %s' % (sn, so), en is None and sn == 10.0 and OLD is not None and so is not None
      and so < 10, (en, sn, eo, so))

hn, mn, sn, en = explorer(PROG, {'NE_MU': 0.0, 'NE_SG': 1E-8}, ups(1), lambda hh: hh.execute('ne_DrawFrame()'))
ho, mo, so, eo = explorer(OLD, {'NE_MU': 0.0, 'NE_SG': 1E-8}, ups(1),
                          lambda hh: hh.execute('ne_DrawFrame()')) if OLD else (None, None, None, 'none')
check('M4 sigma up once from 1E-8: sigma 1.1E-8 (%s), drawn with no error; beta 42c rounded it to 6 decimals: %s, %s'
      % (sn, so, eo), en is None and abs(sn - 1.1E-8) < 1E-20 and OLD is not None and (so == 0 or eo is not None),
      (en, sn, eo, so))

hn, mn, sn, en = explorer(PROG, {'NE_MU': 0.0, 'NE_SG': 1E-9}, ups(3, 'Down'))
check('M4 sigma down three times from 1E-9: sigma stays 1E-9 (%s), no error' % sn, en is None and sn == 1E-9,
      (en, sn))


def far_drag(hh):
    hh.drag([(38, 100), (120, 100), (300, 100)])             # mu, from its line at the left edge
    for _ in range(4):
        hh.tap(*SOFT(4))                                     # Shade: left -> right -> between -> outside -> none


def auto_draw(hh):
    hh.globals_['NE_WA'] = 4.0
    hh.execute('ne_DrawFrame()')


far = {'NE_MU': 0.0, 'NE_SG': 1.0, 'NE_XM': 1.0, 'NE_XO': 1E40}
hn, mn, sn, en = explorer(PROG, far, far_drag, auto_draw)
ho, mo, so, eo = explorer(OLD, far, far_drag, auto_draw) if OLD else (None, None, None, 'none')
check('M4 a shading bound at 1E40 (N(0,1)): mu dragged to the far right stops at 100,000,000 sigma (%s); with the '
      'shading off the auto window draws; beta 42c: mu %s, %s' % (mn, mo, eo), en is None and mn is not None
      and abs(mn) <= 1E8 and OLD is not None and eo is not None, (en, mn, eo, mo))


def s_diag_tap(h):
    h.choose(9, 8)
    h.tap(150, 120)                                          # a tap on the Diagnostics page


hn, rn, en = run(s_diag_tap)
ho, ro, eo = run(s_diag_tap, OLD) if OLD else (None, None, 'no beta 42c')
check('M5 Diagnostics, then a tap: back to the menu, the run ends normally (%s); beta 42c: %s' % (
    (rn or '')[:30], (eo or ro or '')[:90]), en is None and (rn or '').startswith('NormExp: ')
    and [c.title for c in hn.chooses][-1].startswith('NormExp') and OLD is not None and eo is not None,
    (en, rn, eo))


def ends(mu, sg):
    def f(h):
        h.choose(1)
        h.answer({'sdMU': mu, 'sdSG': sg})
        h.choose(2)
        h.press('Up', 'Up', 'Down', 'Left', 'Right', 'Zero', 'Down', 'Down', 'Down')
        h.tap(*SOFT(4))
        h.tap(*SOFT(4))
        h.tap(*SOFT(4))
        h.drag([(150, 120), (190, 120)])
        h.press('Enter')
        h.choose(3, 1)
        h.answer({'pcA': mu + sg})
        h.choose(3, 4)
        h.answer({'pcA': mu - sg, 'pcB': mu + 2 * sg})
        for k, fld, v in ((1, 'icP', 0.9), (2, 'icP', 0.05), (3, 'icP', 0.05), (4, 'icP', 0.01), (5, 'icC', 0.95)):
            h.choose(4, k)
            h.answer({fld: v})
        h.choose(7, 1)
        h.answer({'c2M2': mu + sg})
        h.choose(7, 3)
        h.answer({'c2A': 0.05})
        h.choose(7, 2)
        h.choose(6, 6, 1)
        h.choose(8)
        h.choose(9, 2)
        h.choose(9, 3)
        h.answer({'swLO': mu - 5 * sg, 'swHI': mu + 5 * sg})
        h.choose(9, 7)
        h.choose(9, 8)
        h.choose(5, 1)
        h.answer({'zsX': mu + sg, 'zsM': mu, 'zsS': sg})
    return f


big = []
for mu, sg in ((0.0, 1E-9), (0.0, 1E10), (1E18, 1E10), (-1E18, 1E10), (1E9, 10.0), (-1E9, 10.0), (0.001, 1E-9)):
    hn, rn, en = run(ends(mu, sg))
    big.append(('N(%g, %g)' % (mu, sg), en, boxes(hn), (rn or '')[:20]))
check('M6 the ends of what is accepted, through the Explorer, both areas, the five quantiles, compare and power, a '
      'sample, the animation, the wide and custom windows, Diagnostics and the solver: no error, no box (STRING '
      'refusing 13 decimals as on the Prime): %s' % [(b[0], b[1], b[2][:1]) for b in big],
      all(b[1] is None and not b[2] and b[3].startswith('NormExp: ') for b in big), big)


def far_bounds(h):
    h.choose(3, 1)
    h.answer({'pcA': 9.9E49})
    h.choose(3, 4)
    h.answer({'pcA': -9.9E49, 'pcB': 9.9E49})
    h.choose(7, 1)
    h.answer({'c2M2': -9.9E49})
    h.choose(9, 3)
    h.answer({'swLO': -9.9E49, 'swHI': 9.9E49})


hn, rn, en = run(far_bounds)
check('M6 N(0,1) with bounds, mu2 and a custom window at +-9.9E49: drawn, no error, no box (%s)' % (en or 'ok'),
      en is None and not boxes(hn), (en, boxes(hn)))

def readout(h):
    """the last screen's mean, sigma, xbar, s and d lines"""
    out = []
    for sc in h.screens:
        r = [x for x in sc.lines() if re.match(r'^(\ue000|s|σ|μ|d) = ', x)]
        if r:
            out = r
    return out


big1e8 = [1E8 + k for k in range(1, 11)]                     # s = 3.0277
hn, rn, en = run(lambda h: h.choose(6, 1), app={'D1': big1e8})
ho, ro, eo = run(lambda h: h.choose(6, 1), OLD, app={'D1': big1e8}) if OLD else (None, None, 'none')
check('M8 D1 = 100,000,001 ... 100,000,010 (s = 3.0277): the fitted curve and readout say s = 3.03 (%s); beta 42c, '
      'from the sum of squares: %s' % (readout(hn)[-1:], readout(ho)[-1:] if ho else '-'),
      en is None and 's = 3.03' in readout(hn) and 'σ = 3.03' in readout(hn) and OLD is not None
      and 's = 3.03' not in readout(ho), (en, readout(hn), eo, readout(ho) if ho else None))
tg = {'C1': [1E8 + k for k in (1, 2, 3, 4, 5)], 'C2': [1E8 + k for k in (3, 4, 5, 6, 8)]}
hn, rn, en = run(lambda h: h.choose(6, 2), app=tg)
ho, ro, eo = run(lambda h: h.choose(6, 2), OLD, app=tg) if OLD else (None, None, 'none')
check('M8 two groups near 100,000,000 (s1 = 1.58, s2 = 1.92): pooled sigma 1.76 and d = 1.25 (%s); beta 42c: %s' % (
    readout(hn), readout(ho) if ho else '-'), en is None and 'σ = 1.76' in readout(hn) and 'd = 1.25' in readout(hn)
    and OLD is not None and 'd = 1.25' not in readout(ho), (en, readout(hn), eo, readout(ho) if ho else None))
sims = []
for k, nn in ((1, 200), (2, 1000)):
    sc = lambda h, k=k: (h.choose(1), h.answer({'sdMU': 1E9, 'sdSG': 10.0}), h.choose(6, 6, k))  # noqa: E731
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'none')
    sv = [float(x[4:]) for x in readout(hn) if x.startswith('s = ')]
    so = [x for x in readout(ho) if x.startswith('s = ')] if ho else []
    sims.append((nn, en, sv, so))
check('M8 a simulated sample from N(1E9, 10), n = 200 and 1000 (the PPL sampler): s within 1.5 of 10 (%s); beta 42c, '
      'from sums of the values: %s' % ([x[2] for x in sims], [x[3] for x in sims]),
      all(x[1] is None and len(x[2]) == 1 and abs(x[2][0] - 10) < 1.5 and x[3] == ['s = 0.00'] for x in sims), sims)

msgs = [BIG, WIDE, NARROW, GIVES, ZBIG, XBIG, SBIG, WNAR, DBIG, DWIDE, DNAR, CBIG, ZDBIG]
nl = [len(textwrap.wrap(m, 32)) for m in msgs]
check('M7 every new box within 4 lines at 32 characters a line: %s' % nl, max(nl) <= 4, nl)

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
bn, bo = bodies(SRC), bodies(OSRC)
changed = sorted(k for k in set(bn) | set(bo) if strip_c(upto_end(bn.get(k, ''))) != strip_c(upto_end(bo.get(k, ''))))
WANT = sorted(['ne_BadDist', 'ne_BigMsg', 'ne_BinData', 'ne_Compare2', 'ne_DataLoad', 'ne_DiagPage', 'ne_Explorer',
               'ne_Histo', 'ne_InvCalc', 'ne_NormDraw', 'ne_ProbCalc', 'ne_ResidLoad', 'ne_SampBins', 'ne_SetDist',
               'ne_SetWin', 'ne_SgMin', 'ne_Snap', 'ne_TwoGroups', 'ne_YWd', 'ne_ZSolve', 'ne_ZtoD2'])
check('G1 only these routines differ from beta 42c, code for code (comments aside): %s' % changed, changed == WANT,
      (sorted(set(changed) - set(WANT)), sorted(set(WANT) - set(changed))))
code = [ln.split('//')[0] for ln in SRC.split('\n')]
fwd = re.findall(r'^(ne_\w+)\(\);', SRC, re.M)
check('G2 no "!=" in the code (a factorial and a test on the Prime); the four new helpers forward-declared with the '
      'rest (%d declarations)' % len(fwd), not any('!=' in c for c in code)
      and all(x in fwd for x in ('ne_BigMsg', 'ne_BadDist', 'ne_SgMin', 'ne_Snap')), fwd[-6:])


def code_glyphs(txt):
    out = set()
    for ln in txt.split('\n'):
        c = re.sub(r'"[^"]*"', '""', ln.split('//')[0])
        out |= set(ch for ch in c if ord(ch) > 127)
    return out


gn, go = code_glyphs(SRC), code_glyphs(OSRC)
check('G3 no new non-ASCII character in the code outside strings: %s (beta 42c: %s)' % (
    ''.join(sorted(gn)), ''.join(sorted(go))), gn <= go, sorted(gn - go))

py_of = lambda t: t[t.index('\n#PYTHON SAMPBINSPY'):t.index('\n#END', t.index('\n#PYTHON SAMPBINSPY'))]  # noqa: E731
pn = [ln.split('#')[0].rstrip() for ln in py_of(SRC).split('\n')]
po = [ln.split('#')[0].rstrip() for ln in py_of(OSRC).split('\n')] if OSRC else []
dn = [x for x in pn if x not in po]
do_ = [x for x in po if x not in pn]
check('G4 the MicroPython sampler differs from beta 42c\'s in its sums only (code, comments aside): added %s, gone %s'
      % ([x.strip() for x in dn], [x.strip() for x in do_]),
      sorted(x.strip() for x in dn) == sorted(['z = v * f', 'val = mu + sg * z', 'tot += z', 'tot2 += z * z'])
      and sorted(x.strip() for x in do_) == sorted(['val = mu + sg * v * f', 'tot += val', 'tot2 += val * val']),
      (dn, do_))

# ===================================================================== D
print('=== D. layout (text_overlap_v1: the R sessions and the ends of what is accepted, run again on both versions)')


def draw_ends(mu, sg):
    """the ends without the Explorer's sigma keys, which beta 42c cannot take at sigma = 1E-9"""
    def f(h):
        h.choose(1)
        h.answer({'sdMU': mu, 'sdSG': sg})
        h.choose(2)
        h.tap(*SOFT(4))
        h.tap(*SOFT(4))
        h.press('Zero', 'Enter')
        h.choose(3, 1)
        h.answer({'pcA': mu + sg})
        h.choose(3, 4)
        h.answer({'pcA': mu - sg, 'pcB': mu + 2 * sg})
        h.choose(4, 5)
        h.answer({'icC': 0.95})
        h.choose(7, 3)
        h.answer({'c2A': 0.05})
        h.choose(6, 6, 1)
        h.choose(8)
        h.choose(9, 3)
        h.answer({'swLO': mu - 5 * sg, 'swHI': mu + 5 * sg})
        h.choose(9, 7)
        h.choose(9, 8)
        h.choose(5, 1)
        h.answer({'zsX': mu + sg, 'zsM': mu, 'zsS': sg})
    return f


OV.RECORDS.clear()
d_err = []
for sc in [s_ for _, s_ in sessions] + [draw_ends(mu, sg) for mu, sg in
                                        ((0.0, 1E-9), (0.0, 1E10), (1E18, 1E10), (1E9, 10.0), (0.001, 1E-9))]:
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, None)
    d_err.append((en, eo))
rep = OV.report()


def firm_of(tag0):
    t = [t for t in rep if t.startswith(tag0)]
    f = rep[t[0]] if t else None
    out = set()
    if f:
        out |= set(('overlap', c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm'])
        out |= set(('straddle', x['text'], x['edge']) for x in f['straddles'] if x['firm'])
        out |= set(('overrun', x['text'], x.get('right')) for x in f['overruns'] if x['firm'])
        print('   %s: %d distinct screens of %d' % (t[0], f['screens_distinct'], f['screens_total']))
    return bool(t), out


okn, fn = firm_of(os.path.splitext(os.path.basename(PROG))[0])
oko, fo = firm_of('NormExplorer_beta42c')
check('D1 the same runs on both versions: no firm overlap, frame straddle or overrun on a beta 42d screen that beta '
      '42c does not also have (beta 42d: %d kinds, beta 42c: %d), no error on either' % (len(fn), len(fo)),
      okn and not (fn - fo) and not any(a or b for a, b in d_err), (sorted(fn - fo)[:6], d_err))


def xrow(tag0):
    """overlaps between two texts on the x-label row (y = BOT + 5 = 193)"""
    t = [t for t in rep if t.startswith(tag0)]
    return set((c['a'], c['b']) for c in rep[t[0]]['collisions'] if c['severity'] == 'overlap' and c['firm']
               and c['ay'] == 193 and c['by'] == 193) if t else set()


xn, xo = xrow(os.path.splitext(os.path.basename(PROG))[0]), xrow('NormExplorer_beta42c')
check('D2 x labels printed over each other: beta 42d none, beta 42c %d kinds (e.g. %s)' % (
    len(xo), sorted(xo)[:2]), not xn and len(xo) > 0, sorted(xn)[:4])

def yw(s):
    """a label's width as the programs estimate it: 5.5 px a character, 3 px for the point (n3_YWd, ne_YWd, st_LWd;
    "0.03" is 20 px wide on the Virtual Calculator)"""
    return 5.5 * (len(s) - 1) + 3 if '.' in s else 5.5 * len(s)


def yval(s):
    return float(s.replace('ᴇ', 'e').replace('−', '-').replace('×', '').replace(',', ''))


def close(a, b):
    return abs(a - b) <= 1E-9 * max(abs(a), abs(b), 1E-300)

# ===================================================================== Y
print('=== Y. beta 42e: density labels in the scientific form when they do not fit left of the axis')
PREV = OLD     # beta 42c: beta 42d drew its density labels exactly as beta 42c did


def ne_ylabs(h):
    """the Explorer's first screen's density labels (font 1 at x 2, above the axis at y 188)"""
    for s_ in h.screens:
        ls = [t.text for t in s_.texts if t.x == 2 and t.y < 184]
        if ls:
            return ls
    return []


def explore(sg, path):
    def sc(h):
        h.choose(1)
        h.answer({'sdMU': 0.0, 'sdSG': sg})
        h.choose(2)
    return run(sc, path)


SIGS = [10.0 ** k for k in range(-9, 11)] + [0.5, 15.0, 250.0, 2000.0, 5000.0, 20000.0, 3E-7]
sci, bad, old_wide = [], [], []
for sg in SIGS:
    hn_, _, en_ = explore(sg, PROG)
    ho_, _, eo_ = explore(sg, PREV) if PREV else (None, None, 'no beta 42c')
    ln_, lo_ = ne_ylabs(hn_), (ne_ylabs(ho_) if ho_ else [])
    ow = [x for x in lo_ if yw(x) > 34]
    if ow:
        old_wide.append((sg, ow[-1]))
    ok = not en_ and not eo_ and len(ln_) > 0 and all(yw(x) <= 34 for x in ln_) and len(ln_) == len(lo_) \
        and all(close(yval(a), yval(b)) for a, b in zip(ln_, lo_))
    if ow:
        ok = ok and all('ᴇ' in x for x in ln_)
        sci.append((sg, ln_[-1] if ln_ else ''))
    else:
        ok = ok and ln_ == lo_
    if not ok:
        bad.append((sg, ln_, lo_, en_, eo_))
check('Y1 the Explorer at N(0, sigma), %d sigmas from 1E-9 to 1E10: every density label at most 34 px wide (x 2 to '
      'the axis at 38); where beta 42c\'s and 42d\'s were wider (%d sigmas) they are the same values in the '
      'scientific form, e.g. %s; elsewhere exactly theirs' % (len(SIGS), len(sci), sci[:3]),
      PREV is not None and not bad and len(sci) > 0, bad[:3])
check('Y2 beta 42c drew labels wider than the margin at %d of those sigmas, sigma = 10000 among them (beta 42d, '
      'the same: "0.00006" over the axis and into the mu box on the Virtual Calculator), e.g. %s' % (len(old_wide), old_wide[:3]),
      any(sg == 10000.0 for sg, _ in old_wide) and len(old_wide) == len(sci), old_wide)
yb = [ln for ln in SRC.split('\n') if 'ndLbl := STRING(ndYV, 3, 1)' in ln]
check('Y3 the scientific form is STRING(x, 3, 1) without its ".0" (SampDist v2.3e\'s, seen on the Virtual '
      'Calculator), and a label is drawn only when it fits', len(yb) == 1
      and 'IF ne_YWd(ndLbl) <= 34 THEN TEXTOUT_P(ndLbl, G1, 2, ndTY-4, 1, NGRAY); END;' in SRC, yb)

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
