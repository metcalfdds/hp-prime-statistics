#!/usr/bin/env python3
"""verify_ChiTable_beta3h.py -- checks ChiTable beta 3h (2 Nov 2026, night; round 6: reasonable caps on what a
student types, and menu items that fit their box) against beta 3g.
Roger: "for alpha we dont need like 0.00001 or something--use real world values like 0.001, 0.01, 0.05, 0.1,
0.2 and so forth". Beta 3g took a typed alpha from 0.0001 to just below 1 and dragged it from 0.0001 to 0.5.
  G  static: only Set alpha (csSetAlpha), the curve page's drag (csCurve) and the two count forms' message (csAskAll, csEntry) differ from beta 3g; the header names beta 3h; no new "!=", nothing new for the CAS.
  X  Set alpha refuses 0.0005, 0.25 and 0.5 with a sentence and keeps alpha; takes 0.001 and 0.2; beta 3g took 0.5; the drag keeps to 0.001 ... 0.2.
  R  the monkey, 30 seeds on both versions (tools/comma_check_v1.py): the same path but where a value is now refused,
     the same texts to the CAS, every big number grouped, no year grouped, no new overlap or cut number.
Run from verify/ as it is (beta 3g from ../programs, an _superseded_* folder or git history).
    python3 verify_ChiTable_beta3h.py [ChiTable_beta3g.txt]
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
NAME, OLDNAME = 'ChiTable_beta3h.txt', 'ChiTable_beta3g.txt'
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
print('=== ChiTable beta 3h against beta 3g ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()
print('=== G. static')
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
WANT = ['csAskAll', 'csCurve', 'csEntry', 'csSetAlpha']
check("G1 only Set alpha (csSetAlpha), the curve page's drag (csCurve) and the two count forms' message (csAskAll, csEntry) differ from beta 3g: %s" % diff, diff == WANT, diff)
check('G2 the header names beta 3h', '// CHITABLE - beta 3h' in SRC and '// beta 3h (2 Nov 2026, night)' in SRC)
check('G3 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('CAS(') == OSRC.count('CAS(') and SRC.count('EXPR(') == OSRC.count('EXPR('))
print('=== X. alpha')

bad, took = [], []
for v, want in ((0.0005, 0), (0.25, 0), (0.5, 0), (0.001, 1), (0.2, 1)):
    h = Harness(PROG, idle_key=4)
    h.globals_['csAlpha'], h.globals_['csAl'], h.globals_['csHas'] = 0.05, 'α', 0.0
    h.answer({'alV': v})
    h.execute('csSetAlpha()')
    m = msgs(h)
    if want == 0 and not (m and m[0].startswith('α must be from 0.001 to 0.2') and h.globals_['csAlpha'] == 0.05):
        bad.append((v, m[:1], h.globals_['csAlpha']))
    if want == 1 and (m or h.globals_['csAlpha'] != v):
        bad.append((v, m[:1], h.globals_['csAlpha']))
check('X1 Set alpha refuses 0.0005, 0.25, 0.5 (alpha stays 0.05) and takes 0.001 and 0.2', not bad, bad)
h = Harness(OLD, idle_key=4)
h.globals_['csAlpha'], h.globals_['csAl'], h.globals_['csHas'] = 0.05, 'α', 0.0
h.answer({'alV': 0.5})
h.execute('csSetAlpha()')
check('X2 beta 3g took 0.5', not msgs(h) and h.globals_['csAlpha'] == 0.5, msgs(h))
cc = rn['csCurve']
check('X3 the drag keeps alpha to 0.001 ... 0.2, the line put back at the matching quantile',
      'IF cvA > 0.2 THEN cvA := 0.2; cvXv := CHISQUARE_ICDF(csDF, 0.8); END;' in cc and
      'IF cvA < 0.001 THEN cvA := 0.001; cvXv := CHISQUARE_ICDF(csDF, 0.999); END;' in cc and '0.0001' not in cc)
check('X4 a count above 9,999,999 no longer suggests dividing the data by 10 (that changes chi-square and p)',
      SRC.count('MSGBOX("Counts above 9,999,999 do not fit the table.");') == 2 and 'enter the data divided by 10."' not in
      CC.strip_comments(SRC))

print('=== R. the monkey, 30 seeds on both versions')
# Each run's message boxes, in the order comma_check makes the runs (seed 5000 + k: the old version, then the new).
# A seed whose path differs is accepted only
#   (a) when the new version showed one of this round's refusal sentences, which the old version did not (a value it
#       took is now refused, and that is the change), and the new run then ended well, as the old one did, or at the
#       harness's own edge ("END Unsupported": something the PC model of the calculator does not cover, its words
#       printed below), or
#   (b) when the two runs are the same but for a message this round rewrites on purpose (CHANGED: the old words and
#       the new), with the same ending, number of screens and result.
_argv = sys.argv
sys.argv = ['monkey_v1b.py']
import monkey_v1b as M  # noqa: E402
sys.argv = _argv
REC, INST, UNS = [], [], {}
REFUSE = ['α must be from 0.001 to 0.2']
CHANGED = {'Counts above 9,999,999 do not fit the table: enter the data divided by 10.': 'Counts above 9,999,999 do not fit the table.'}


_Base = M.Monkey


class _Rec(_Base):
    """the monkey, noting each message box of its run (one list per run, in the order the runs are made)"""

    def __init__(self, *a, **k):
        REC.append([])
        INST.append(self)
        self._rec = REC[-1]
        _Base.__init__(self, *a, **k)

    def _msgbox(self, a):
        r = _Base._msgbox(self, a)
        self._rec.append(self.msgboxes[-1].text if self.msgboxes else '')
        return r


_U = M.R.interp.Unsupported
_U_init = _U.__init__


def _u_init(self, *a, **k):
    UNS.setdefault(len(REC) - 1, str(a[0])[:90] if a else '')   # the run under way: what the harness does not cover
    _U_init(self, *a, **k)


_U.__init__ = _u_init
M.Monkey = _Rec
RES = CC.runs(OLD, PROG, 'ChiTable()', 30, 30, 'beta 3g|beta 3h', None)
EXPL, EXPL_A, EXPL_B, EDGE = set(), [], [], []
for x in RES['r_bad']:
    k_ = x[0] - 5000
    o_, n_ = REC[2 * k_], REC[2 * k_ + 1]
    # (a) this round's refusal, then a good ending (x: seed, old ending, new ending, old screens, new screens, ...)
    if (any(t not in o_ and any(t.startswith(r) for r in REFUSE) for t in n_) and
            (x[2] in ('OK', 'FREEZE', 'END Unsupported') or x[2] == x[1])):
        EXPL.add(x[0])
        EXPL_A.append(x[0])
        if x[2] == 'END Unsupported' and x[2] != x[1]:
            EDGE.append((x[0], UNS.get(2 * k_ + 1, '?')))
    # (b) a message rewritten on purpose, and nothing else different
    elif (CHANGED and x[1] == x[2] and x[3] == x[4] and [CHANGED.get(t, t) for t in o_] == n_ and
          str(INST[2 * k_].result).replace(',', '') == str(INST[2 * k_ + 1].result).replace(',', '')):
        EXPL.add(x[0])
        EXPL_B.append(x[0])
print('   R1: %d seed(s) take another path; %d of them because the new version refused a value with this round\'s '
      'sentence (%s), %d because a message is rewritten on purpose (%s)'
      % (len(RES['r_bad']), len(EXPL_A), sorted(EXPL_A), len(EXPL_B), sorted(EXPL_B)))
for e_ in EDGE:
    print('   R1: seed %d, after the refusal, reached the harness\'s edge: %s' % e_)
_good = sum(v for k_, v in RES['verdicts'].items() if k_ in ('OK', 'FREEZE'))
check('R0 the runs ran: %d of %d new-version runs ended OK or by the clock (%s)' % (_good, RES['n'], RES['verdicts']),
      _good >= 2 * RES['n'] // 3)
for nm, ok, det in CC.report(RES, {}, (), EXPL):
    if ok is None:
        print('INFO ' + nm)
    else:
        check(nm, ok, det)
print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
