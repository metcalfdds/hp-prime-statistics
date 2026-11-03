#!/usr/bin/env python3
"""verify_EpiStats_v1.7g.py -- checks EpiStats v1.7g (2 Nov 2026, night; round 6: reasonable caps on what a
student types, and menu items that fit their box) against v1.7f.
Roger: "for alpha we dont need like 0.00001 or something--use real world values like 0.001, 0.01, 0.05, 0.1,
0.2 and so forth". A caps probe gave a cell 1E100, and on the results page's small table a total of 100,000 or
more was cut short ("110,000" in 32 px).
  G  static: only the four sample-size forms, the four-value form (es_AskAll), the one-cell form (es_Grid), the results page (es_ReadPage) and the menu's title (EpiStats) differ from v1.7f; the header names v1.7g; no new "!=", nothing new for the CAS.
  X  the sample-size forms refuse alpha 0.3 and 0.0005 and take 0.2; the four-value form refuses 10,000,000 and takes 9,999,999; the one-cell form likewise; the results page leaves out a total of 110,000 and cuts nothing; v1.7f took alpha 0.3 and a cell of 1E100.
  R  the monkey, 30 seeds on both versions (tools/comma_check_v1.py): the same path but where a value is now refused,
     the same texts to the CAS, every big number grouped, no year grouped, no new overlap or cut number.
Run from verify/ as it is (v1.7f from ../programs, an _superseded_* folder or git history).
    python3 verify_EpiStats_v1.7g.py [EpiStats_v1.7f.txt]
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
NAME, OLDNAME = 'EpiStats_v1.7g.txt', 'EpiStats_v1.7f.txt'
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
print('=== EpiStats v1.7g against v1.7f ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()
print('=== G. static')
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
WANT = ['EpiStats', 'es_AskAll', 'es_Grid', 'es_ReadPage', 'es_SS_OneMean', 'es_SS_OneProportion', 'es_SS_TwoMeans', 'es_SS_TwoProportions']
check("G1 only the four sample-size forms, the four-value form (es_AskAll), the one-cell form (es_Grid), the results page (es_ReadPage) and the menu's title (EpiStats) differ from v1.7f: %s" % diff, diff == WANT, diff)
check('G2 the header names v1.7g', '// EPISTATS - v1.7g' in SRC and '"EpiStats v1.7g ' in SRC)
check('G3 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('CAS(') == OSRC.count('CAS(') and SRC.count('EXPR(') == OSRC.count('EXPR('))
print('=== X. alpha and counts')

import label_fit_v1 as LF  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
bad = []
for r_ in ('es_SS_OneMean()', 'es_SS_OneProportion()', 'es_SS_TwoMeans()', 'es_SS_TwoProportions()'):
    for v, want in ((0.3, 1), (0.0005, 1), (0.2, 0), (0.001, 0)):
        h = run(PROG, r_, [{'alpha': v}], secs=10)
        got = any(t.startswith('α must be from 0.001 to 0.2') for t in msgs(h))
        if got != bool(want):
            bad.append((r_, v, msgs(h)[:2]))
check('X1 the four sample-size forms refuse alpha 0.3 and 0.0005 and take 0.2 and 0.001', not bad, bad)
o_ = run(OLD, 'es_SS_TwoMeans()', [{'alpha': 0.3}], secs=10)
check('X2 v1.7f took alpha 0.3', not any('must be' in t for t in msgs(o_)), msgs(o_)[:2])
bad = []
for big, want in ((10000000, 1), (1E100, 1), (9999999, 0)):
    h = Harness(PROG, idle_key=4)
    h.choose(1)
    h.tap(80, 230)
    h.answer({'avA': big, 'avB': 5, 'avC': 7, 'avD': 9})
    try:
        h.execute('EpiStats()')
    except Exception as e:
        bad.append((big, 'ended', str(e)[:60]))
    got = any(t.startswith('Values above 9,999,999 do not fit the table') for t in msgs(h))
    if got != bool(want):
        bad.append((big, msgs(h)[:2]))
check('X3 the four-value form refuses 10,000,000 and 1E100 with a sentence and takes 9,999,999', not bad, bad)
h = Harness(PROG, idle_key=4)
h.choose(1)
h.tap(80, 230)
h.answer({'avA': 60000, 'avB': 50000, 'avC': 70000, 'avD': 40000})
h.execute('EpiStats()')
cuts, tot = [], []
for s_ in h.screens:
    cuts += [t.text for t in s_.texts if t.width is not None and LF.hidden_tail(t.text, OV._font(t.font), float(t.width))]
    tot += [t.text for t in s_.texts if float(t.x) == 284 and t.text != 'total']
h2 = Harness(OLD, idle_key=4)
h2.choose(1)
h2.tap(80, 230)
h2.answer({'avA': 60000, 'avB': 50000, 'avC': 70000, 'avD': 40000})
h2.execute('EpiStats()')
ocuts = []
for s_ in h2.screens:
    ocuts += [t.text for t in s_.texts if t.width is not None and LF.hidden_tail(t.text, OV._font(t.font), float(t.width))]
check('X4 rows of 110,000: v1.7g cuts nothing and leaves the two totals out of the small table (v1.7f cut %s)'
      % sorted(set(ocuts)), not cuts and not tot and '110,000' in ocuts, (cuts, tot))
g = rn['es_Grid']
check('X5 the one-cell form refuses above 9,999,999 and says so in its help line',
      'IF gdV > 9999999 THEN' in g and '0 to 9,999,999' in g)

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
REFUSE = ['α must be from 0.001 to 0.2', 'Values above 9,999,999 do not fit the table']
CHANGED = {}


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
RES = CC.runs(OLD, PROG, 'EpiStats()', 30, 30, 'v1.7f|v1.7g', None)
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
