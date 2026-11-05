#!/usr/bin/env python3
"""verify_EpiStats_v1.7h.py -- checks EpiStats v1.7h (4 Nov 2026): the monkey test's first run on EpiStats.
On v1.7g, 1,000 monkey runs gave 838 OK, 161 HARNESS (a list typed into a number field went into the arithmetic) and
1 CRASH (a mean difference of 1E-300: its square underflows, so n divided by zero).  Checked here:
  G  every INPUT field typed {name,[0]}; the header, menu and About page name v1.7h; only the routines the change note
     names differ from v1.7g; no new "!=" and nothing new for the CAS.
  X  the sample sizes: SciPy's n for ordinary values (unchanged from v1.7g, value for value); 1E-300 and an effect too
     small for n <= 100,000,000 refused with a sentence, never a crash; more than 50 digits refused; n at least 1.
  P  es_FmtPct: below -9,999 % and above 99,999 % as words; ordinary values as before.
  D  the comma_check runs (30 seeds): no new overlap, straddle, overrun or cut number (the v1.7g script's D).
Built in the PC harness; the Virtual Calculator run is in the CHANGES file.  Run:  python3 verify_EpiStats_v1.7h.py
"""
import glob
import os
import re
import signal
import subprocess
import sys
import tempfile
import warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
for cand in reversed([c for c in (os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'), HERE) if c]):
    if os.path.exists(os.path.join(cand, 'comma_check_v1.py')):
        sys.path.insert(0, cand)
import comma_check_v1 as CC  # noqa: E402
from ppl_run_v3e import Harness, CANCEL, ACCEPT  # noqa: E402,F401
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
NAME, OLDNAME = 'EpiStats_v1.7h.txt', 'EpiStats_v1.7g.txt'
PROG = os.path.join(HERE, NAME) if os.path.exists(os.path.join(HERE, NAME)) else os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:600]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def older(name):
    if len(sys.argv) > 1:
        return sys.argv[1]
    for pth in [os.path.join(HERE, name), os.path.join(HERE, '..', 'programs', name)] + \
            sorted(glob.glob(os.path.join(HERE, '..', '_superseded_*', name)), reverse=True):
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
                return pth
    except Exception:
        pass
    return None


class _Up(Exception):
    pass


def _alarm(signum, frame):
    raise _Up()


def run(path, call, answers=(), chooses=(), keys=(), secs=20, msgbox_ok=(), first=()):
    """Run CALL on PATH with INPUT answers, CHOOSE picks and keys queued; Esc when it waits.  -> the harness, or
    the harness with .stopped = 'time' if it ran past SECS (a long computation the check does not need)."""
    h = Harness(path, idle_key=4)
    h.stopped = ''
    for a in answers:
        h.answer(a)
    for c in chooses:
        h.choose(c)
    for k in keys:
        h.press(k)
    for o in msgbox_ok:
        h._msgbox_answers.append(o)
    for f_ in first:                 # the program's own setup, before the call
        h.execute(f_)
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(secs)
    try:
        h.execute(call)
    except _Up:
        h.stopped = 'time'
    finally:
        signal.alarm(0)
    return h


def msgs(h):
    return [m.text for m in h.msgboxes]



OLD = older(OLDNAME)
print('=== EpiStats v1.7h against v1.7g ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()
from scipy.stats import norm as _N  # noqa: E402
import math  # noqa: E402
print('=== G. static')
forms = re.findall(r'INPUT\(\s*\{(.*?)\}\s*,\s*"', SRC, re.S)
untyped = [f for f in forms if re.search(r'(?:^|,)\s*[A-Za-z_]\w*\s*(?:,|$)', f)]
check('G1 all 12 forms, every field typed {name,[0]} (%d forms)' % len(forms), len(forms) == 12 and not untyped, untyped)
check('G2 the header, the menu title and the About page name v1.7h', '// EPISTATS - v1.7h' in SRC and '"EpiStats v1.7h ' in SRC
      and '{"EpiStats v1.7h",' in SRC and 'v1.7f",' not in SRC)
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
WANT = ['EpiStats', 'es_AskAll', 'es_FmtPct', 'es_Grid', 'es_GridDraw', 'es_Help_About', 'es_IR_Page2', 'es_Module_IncidenceRate',
        'es_SS_OneMean', 'es_SS_OneProportion', 'es_SS_TwoMeans', 'es_SS_TwoProportions']
check('G3 only the routines the change note names differ from v1.7g: %s' % diff, diff == WANT, diff)
check('G4 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('CAS(') == OSRC.count('CAS(') and SRC.count('EXPR(') == OSRC.count('EXPR('))
print('=== X. sample sizes')


def nshown(h):
    for s_ in h.screens:
        for t in s_.texts:
            m = re.match(r'n = ([\d,]+)$', t.text)
            if m:
                return int(m.group(1).replace(',', ''))
    return None


def z(p):
    return _N.ppf(p)


CASES = [  # routine, answers, SciPy's n
    ('es_SS_TwoMeans()', {'delta': 1, 'sigma': 2}, math.ceil(2 * 4 * (z(.975) + z(.8)) ** 2 / 1)),
    ('es_SS_TwoMeans()', {'delta': 5, 'sigma': 15, 'alpha': 0.01, 'power': 0.9}, math.ceil(2 * 225 * (z(.995) + z(.9)) ** 2 / 25)),
    ('es_SS_TwoProportions()', {'p1': 0.5, 'p2': 0.3}, math.ceil(2 * .4 * .6 * (z(.975) + z(.8)) ** 2 / .04)),
    ('es_SS_OneProportion()', {'p': 0.5, 'moe': 0.03}, math.ceil(z(.975) ** 2 * .25 / .0009)),
    ('es_SS_OneMean()', {'sigma': 10, 'moe': 2}, math.ceil((z(.975) * 10 / 2) ** 2)),
    ('es_SS_TwoMeans()', {'delta': 1, 'sigma': 1E-300}, 1),
]
bad = []
for r_, a, want in CASES:
    h = run(PROG, r_, [a], secs=10)
    ho = run(OLD, r_, [a], secs=10)
    got, old = nshown(h), (nshown(ho) if a.get('sigma') != 1E-300 else 1)
    if got != want or old != want:
        bad.append((r_, a, want, got, old, msgs(h)[:1]))
check('X1 ordinary values give SciPy\'s n, as v1.7g did; sigma 1E-300 gives n = 1, not 0', not bad, bad)
REF = [
    ('es_SS_TwoMeans()', {'delta': 1E-300, 'sigma': 100}, 'The difference is too small'),
    ('es_SS_TwoMeans()', {'delta': 0.0001, 'sigma': 1}, 'The difference is too small'),
    ('es_SS_TwoMeans()', {'delta': 1E60, 'sigma': 1}, 'more than 50 digits'),
    ('es_SS_TwoProportions()', {'p1': 0.5, 'p2': 0.50001}, 'too close'),
    ('es_SS_OneProportion()', {'p': 0.5, 'moe': 1E-300}, 'margin of error is too small'),
    ('es_SS_OneMean()', {'sigma': 10, 'moe': 1E-300}, 'margin of error is too small'),
    ('es_SS_OneMean()', {'sigma': 1E60, 'moe': 1}, 'more than 50 digits'),
]
bad = []
for r_, a, want in REF:
    try:
        h = run(PROG, r_, [a], secs=10)
        ok = any(want in t for t in msgs(h)) and nshown(h) is None
    except Exception as e:
        ok, h = False, None
        bad.append((r_, a, 'CRASH ' + type(e).__name__ + ' ' + str(e)[:80]))
        continue
    if not ok:
        bad.append((r_, a, msgs(h)[:2]))
check('X2 1E-300, effects too small for n <= 100,000,000 and numbers of more than 50 digits are refused with a sentence', not bad, bad)
try:
    run(OLD, 'es_SS_TwoMeans()', [{'delta': 1E-300, 'sigma': 100}], secs=10)
    oc = 'no crash'
except Exception as e:
    oc = type(e).__name__ + ': ' + str(e)[:60]
check('X3 v1.7g crashed on delta = 1E-300 (the monkey\'s seed 1000761): %s' % oc, 'division by zero' in oc, oc)
# n near the cap is still computed: d = sqrt(2)(za+zb)/1E4 * 1.01
d = 2 ** .5 * (z(.975) + z(.8)) / 1E4 * 1.01
h = run(PROG, 'es_SS_TwoMeans()', [{'delta': d, 'sigma': 1}], secs=10)
check('X4 an effect just above the cap is computed (n = %s, below 100,000,000)' % nshown(h), nshown(h) is not None and nshown(h) < 1E8, msgs(h)[:2])
bad = []
for a, want in (({'cexp': 5, 'u': 1E300, 'pte': 100, 'ptu': 1E-300}, 'Cases above 9,999,999'),
                ({'cexp': 5, 'u': 3, 'pte': 100, 'ptu': 1E-300}, 'Person-time must be from'),
                ({'cexp': 5, 'u': 3, 'pte': 1E20, 'ptu': 100}, 'Person-time must be from')):
    try:
        h = run(PROG, 'es_Module_IncidenceRate()', [a], secs=10)
        if not any(want in t for t in msgs(h)):
            bad.append((a, msgs(h)[:2]))
    except Exception as e:
        bad.append((a, 'CRASH ' + str(e)[:80]))
h = run(PROG, 'es_Module_IncidenceRate()', [{'cexp': 20, 'u': 10, 'pte': 1000, 'ptu': 1000}], secs=10)
if any('must be' in t or 'do not fit' in t for t in msgs(h)):
    bad.append(('ordinary values refused', msgs(h)[:2]))
check('X5 the incidence-rate form refuses 1E300 cases and a person-time of 1E-300 or 1E20 (the monkey\'s seed 1000392), and takes 20 and 10 over 1,000 and 1,000', not bad, bad)
print('=== P. percentages')
want = {-200000: '< −9,999%', -99.99: '-9999.0%', 0.5: '50.0%', 999.99: '99999.0%', 1000: '> 99,999%'}
bad = []
for x, w in want.items():
    hh = Harness(PROG, idle_key=4)
    got = hh.execute('es_FmtPct(%r)' % x)
    if str(got) != w:
        bad.append((x, w, got))
check('P1 es_FmtPct: below -9,999 %% and above 99,999 %% as words, the rest as before: %s' % bad, not bad, bad)
print('=== D. layouts (comma_check, 30 seeds)')
RES = CC.runs(OLD, PROG, 'EpiStats()', 30, 30, 'v1.7g|v1.7h', None)
d_ = [r for r in CC.report(RES, {}, (), ()) if r[0].startswith('D')]
for nm, ok, det in d_:
    check(nm, ok, det)
print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for f in FAIL:
    print('  FAILED: ' + f)
sys.exit(1 if FAIL else 0)
