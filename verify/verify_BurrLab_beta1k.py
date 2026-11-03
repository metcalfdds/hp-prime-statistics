#!/usr/bin/env python3
"""verify_BurrLab_beta1k.py -- checks BurrLab beta 1k (2 Nov 2026, night): x0 stays on the Explore plot.

Roger, beta 1j on the Virtual Calculator: on Explore, x0 could be stepped out to the hundreds of thousands, and the
plot went with it.  beta 1j's window stretched to 1.15 x0 and each arrow step was a fortieth of the window, so every
press made the next one bigger.  beta 1k keeps the window the curve's own (the 0.995 quantile, at most 50 S) and stops
x0 at its right edge.  Roger, the same evening: "cap S at something less than 1,000,000": S now stops at 1,000
(arrows, drag and the Family page's S key), and an S already above it is not pulled down.
  G  static: only bu_Window, bu_ExpStep, bu_Explore (the drag), bu_Family (its S key), the help page and the title
     page differ from beta 1j (with comments out).
  X1 400 presses of the up arrow with x0 chosen: beta 1k's x0 stays inside the window and the window stays the
     curve's; beta 1j's runs away (the fault, shown on the old version).
  X2 x0 at the edge, then S divided by 10: x0 comes back inside the smaller window.
  X3 C, K and S keep their ranges under 600 presses each way: C and K 0.2 to 50, S 0.01 to 1,000.
  X4 an S above 1,000 (a fit in large units) is not pulled down by an up press, and comes down by a down press.
  R  the monkey, 30 seeds on both versions (tools/comma_check_v1.py): the same path, the same texts to the CAS, every
     big number grouped, no year grouped, no new overlap or cut number.
Run from verify/ as it is (beta 1j from ../programs, an _superseded_* folder or git history).
    python3 verify_BurrLab_beta1k.py [BurrLab_beta1j.txt]
"""
import glob
import os
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
from ppl_run_v3e import Harness  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME, OLDNAME = 'BurrLab_beta1k.txt', 'BurrLab_beta1j.txt'
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


OLD = older(OLDNAME)
print('=== BurrLab beta 1k against beta 1j ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()

print('=== G. static')
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
check('G1 only bu_Window, bu_ExpStep, bu_Explore, bu_Family, the help page and the title page differ from beta 1j: %s'
      % diff, diff == ['bu_ExpStep', 'bu_Explore', 'bu_Family', 'bu_Help', 'bu_Opening', 'bu_Window'], diff)
check('G2 the header names beta 1k, the title page too', '// BurrLab - beta 1k' in SRC and
      '"BurrLab beta 1k: the long right tail"' in SRC)
check('G3 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('bu_Cas(') == OSRC.count('bu_Cas('))


def steps(path, n, sel, d, shrink=False):
    h = Harness(path, idle_key=4)
    h.execute('bu_Init()')
    h.execute('bu_Window()')
    w0 = h.execute('buXmax')
    h.globals_['buSel'] = float(sel)
    for _ in range(n):
        h.execute('bu_ExpStep(%d)' % d)
        h.execute('bu_Window()')
    out = {k: h.globals_[k] for k in ('buX0', 'buXmax', 'buC', 'buK', 'buS')}
    out['w0'] = w0
    if shrink:
        h.globals_['buS'] = h.globals_['buS'] / 10
        h.execute('bu_Window()')
        out['x0_after'], out['w_after'] = h.globals_['buX0'], h.globals_['buXmax']
    return out


print('=== X. x0 on Explore')
n1, o1 = steps(PROG, 400, 4, 1, True), steps(OLD, 400, 4, 1)
check('X1 400 presses up with x0 chosen: x0 = %g inside the window %g, which is still the curve\'s (%g); beta 1j: '
      'x0 = %g, window %g' % (n1['buX0'], n1['buXmax'], n1['w0'], o1['buX0'], o1['buXmax']),
      0 < n1['buX0'] <= n1['buXmax'] and abs(n1['buXmax'] - n1['w0']) < 1e-9 and n1['buX0'] > 0.9 * n1['buXmax'] and
      o1['buX0'] > 1000 * o1['w0'])
check('X2 then S / 10: x0 = %g, inside the new window %g' % (n1['x0_after'], n1['w_after']),
      0 < n1['x0_after'] <= n1['w_after'] and n1['x0_after'] > 0.9 * n1['w_after'])
rng = []
for sel, d in ((1, 1), (1, -1), (2, 1), (2, -1), (3, 1), (3, -1)):
    r = steps(PROG, 600, sel, d)
    rng.append(r['buC'] if sel == 1 else r['buK'] if sel == 2 else r['buS'])
check('X3 C, K and S under 600 presses each way: C %g to %g, K %g to %g, S %g to %g'
      % (rng[1], rng[0], rng[3], rng[2], rng[5], rng[4]),
      abs(rng[0] - 50) < 1e-9 and abs(rng[1] - 0.2) < 1e-9 and abs(rng[2] - 50) < 1e-9 and abs(rng[3] - 0.2) < 1e-9
      and abs(rng[4] - 1000) < 1e-9 and abs(rng[5] - 0.01) < 1e-12)
h = Harness(PROG, idle_key=4)
h.execute('bu_Init()')
h.globals_['buS'], h.globals_['buSel'] = 5000.0, 3.0
h.execute('bu_ExpStep(1)')
up = h.globals_['buS']
h.execute('bu_ExpStep(-1)')
dn = h.globals_['buS']
check('X4 S = 5,000 (above the cap): up leaves it at %g, down takes it to %g' % (up, dn),
      abs(up - 5000) < 1e-9 and abs(dn - 5000 / 1.1) < 1e-6)

print('=== R. the monkey, 30 seeds on both versions')
RES = CC.runs(OLD, PROG, 'BurrLab()', 30, 30, 'beta 1j|beta 1k', None)
for nm, ok, det in CC.report(RES, {}, (), {}):
    if ok is None:
        print('INFO ' + nm)
    else:
        check(nm, ok, det)
print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
