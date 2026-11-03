#!/usr/bin/env python3
"""verify_StudRange_beta15i.py -- checks StudRange beta 15i (2 Nov 2026, night; round 6: reasonable caps on what a
student types, and menu items that fit their box) against beta 15g.
Roger: "for alpha we dont need like 0.00001 or something--use real world values like 0.001, 0.01, 0.05, 0.1,
0.2 and so forth".  Beta 15g clamped a typed alpha to 0.0001 ... 0.5 without a word (5 typed for 5 %% became 0.5), and
k had no upper limit in three forms (a caps probe gave it 1E9).  Nor had df: on the PPL engine df 1E12 gave q crit
3.6232 for k 4, alpha .05 (3.6332 is right) and 1E300 stopped the program; Tukey HSD's m had no cap (its automatic df is
k(m - 1)).  Beta 15h, a first build with the alpha and k caps only, was never shipped.
  G  static: only the four forms that take alpha, k, df or m (sr_PvMode, sr_CritMode, sr_HSDMode, sr_PlotMode) differ from beta 15g; the header names beta 15i; no new "!=", nothing new for the CAS.
  X  each form refuses alpha outside 0.001 ... 0.2, k outside 2 ... 100 (plot: 2 ... 20), df outside 1 ... 100,000
     (0 = infinity) and Tukey HSD's m outside 2 ... 1,000 with a sentence, and computes nothing; the edges are taken;
     beta 15g took (and clamped) the same values; q crit at df 100,000 is the infinity value to four decimals.
  R  the monkey, 30 seeds on both versions (tools/comma_check_v1.py): the same path but where a value is now refused,
     the same texts to the CAS, every big number grouped, no year grouped, no new overlap or cut number.
Run from verify/ as it is (beta 15g from ../programs, an _superseded_* folder or git history).
    python3 verify_StudRange_beta15i.py [StudRange_beta15g.txt]
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
NAME, OLDNAME = 'StudRange_beta15i.txt', 'StudRange_beta15g.txt'
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
print('=== StudRange beta 15i against beta 15g ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()
print('=== G. static')
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
WANT = ['sr_CritMode', 'sr_HSDMode', 'sr_PlotMode', 'sr_PvMode']
check("G1 only the four forms that take alpha, k, df or m (sr_PvMode, sr_CritMode, sr_HSDMode, sr_PlotMode) differ from beta 15g: %s" % diff, diff == WANT, diff)
check('G2 the header names beta 15i', '// STUDRANGE - beta 15i' in SRC and '// beta 15i (2 Nov 2026, night)' in SRC)
check('G3 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('CAS(') == OSRC.count('CAS(') and SRC.count('EXPR(') == OSRC.count('EXPR('))
print('=== X. alpha, k, df and m')

AM = 'α must be from 0.001 to 0.2 (0.05 is usual).'
KM = 'k must be a whole number from 2 to 100.'
KM20 = 'k must be a whole number from 2 to 20.'
DFM = 'df must be from 1 to 100,000, or 0 for ∞.'
DFH = 'df must be from 1 to 100,000, or 0 for auto: k(m-1).'
MM = 'm must be a whole number from 2 to 1,000.'
cases = [  # (routine, answer, the refusal wanted or '' for none)
    ('sr_CritMode()', {'ta': 5}, AM), ('sr_CritMode()', {'ta': 0.5}, AM), ('sr_CritMode()', {'ta': 0.0001}, AM),
    ('sr_CritMode()', {'ta': 0.05, 'tk': 101}, KM), ('sr_CritMode()', {'ta': 0.05, 'tk': 3.5}, KM),
    ('sr_CritMode()', {'ta': 0.05, 'tk': 1E9}, KM),
    ('sr_CritMode()', {'ta': 0.05, 'tk': 4, 'tv': 1E12}, DFM), ('sr_CritMode()', {'ta': 0.05, 'tk': 4, 'tv': -5}, DFM),
    ('sr_HSDMode()', {'ta': 0.25}, AM), ('sr_HSDMode()', {'ta': 0.05, 'tk': 1E6}, KM),
    ('sr_HSDMode()', {'ta': 0.05, 'tk': 4, 'tm': 1001}, MM), ('sr_HSDMode()', {'ta': 0.05, 'tk': 4, 'tm': 1}, MM),
    ('sr_HSDMode()', {'ta': 0.05, 'tk': 4, 'tm': 2.5}, MM), ('sr_HSDMode()', {'ta': 0.05, 'tk': 4, 'tvo': 1E12}, DFH),
    ('sr_PvMode()', {'tk': 1000}, KM), ('sr_PvMode()', {'tk': 1}, KM),
    ('sr_PvMode()', {'tk': 4, 'tv': 100001}, DFM), ('sr_PvMode()', {'tk': 4, 'tv': 0.5}, DFM),
    ('sr_PlotMode()', {'tk': 25}, KM20), ('sr_PlotMode()', {'tk': 2.5}, KM20),
    ('sr_PlotMode()', {'tk': 4, 'tv': 1E12}, DFM), ('sr_PlotMode()', {'tk': 4, 'tv': -1}, DFM),
]
bad = []
for call, ans, want in cases:
    h = run(PROG, call, [ans], secs=20)
    m = msgs(h)
    if m[:1] != [want] or any('Solving' in t.text or 'Computing' in t.text for t in h.texts):
        bad.append((call, ans, m[:2], h.stopped))
check('X1 %d typed values out of range are refused with a sentence and nothing is computed' % len(cases), not bad, bad)
ok_ = []
for call, ans in [('sr_CritMode()', {'ta': 0.001, 'tk': 100}), ('sr_CritMode()', {'ta': 0.2, 'tk': 2}),
                  ('sr_CritMode()', {'ta': 0.05, 'tk': 4, 'tv': 100000}), ('sr_CritMode()', {'ta': 0.05, 'tk': 4, 'tv': 1}),
                  ('sr_HSDMode()', {'ta': 0.2, 'tk': 100}), ('sr_HSDMode()', {'ta': 0.05, 'tk': 4, 'tm': 1000}),
                  ('sr_HSDMode()', {'ta': 0.05, 'tk': 4, 'tm': 2, 'tvo': 100000}),
                  ('sr_PvMode()', {'tk': 100}), ('sr_PvMode()', {'tk': 4, 'tv': 0}),
                  ('sr_PlotMode()', {'tk': 20}), ('sr_PlotMode()', {'tk': 4, 'tv': 100000})]:
    h = run(PROG, call, [ans], secs=8)
    m = msgs(h)
    if any(t in m for t in (AM, KM, KM20, DFM, DFH, MM)):
        ok_.append((call, ans, m[:2]))
check('X2 the edges (alpha 0.001 and 0.2, k 2 and 100, df 1, 100,000 and 0, m 2 and 1,000, the plot\'s k 20 and df '
      '100,000) are taken', not ok_, ok_)
oldtook = []
for call, ans in [('sr_CritMode()', {'ta': 5}), ('sr_CritMode()', {'ta': 0.05, 'tk': 1E9}), ('sr_PlotMode()', {'tk': 25}),
                  ('sr_CritMode()', {'ta': 0.05, 'tk': 4, 'tv': 1E12}), ('sr_HSDMode()', {'ta': 0.05, 'tk': 4, 'tm': 1001})]:
    h = run(OLD, call, [ans], secs=5)
    oldtook.append(not any('must be' in t for t in msgs(h)))
check('X3 beta 15g took those values without a word (alpha 5, k 1E9, the plot\'s k 25, df 1E12, m 1,001)', all(oldtook),
      oldtook)
pl = rn['sr_PlotMode']
check('X4 the plot: a typed alpha outside 0.001 ... 0.2 is refused, the drag stops at 0.2, a typed k outside 2 ... 20 '
      'is refused; the help lines say the ranges',
      'MIN(0.2,1-(py2-pmMY)/(py2-py1))' in pl and 'IF pmTv<0.001 OR pmTv>0.2 THEN' in pl and
      'IF pmTv<2 OR pmTv>20 OR FP(pmTv)<>0 THEN' in pl and 'MIN(0.5' not in pl and
      SRC.count('From 0.001 to 0.2; 0.05 is usual') == 3)
check('X5 the plot\'s df key refuses df outside 1 ... 100,000 (0 = infinity) and its H0 simulation m outside 2 ... 30, '
      'with a sentence (both were clamped without a word); every df help line says the range',
      'IF pmTv<0 OR (pmTv>0 AND pmTv<1) OR pmTv>100000 THEN' in pl and 'IF pmTv<2 OR pmTv>30 OR FP(pmTv)<>0 THEN' in pl
      and 'MAX(2,MIN(30,IP(pmTv)))' not in pl and 'tv:=IP(MAX(0,pmTv))' not in pl and
      SRC.count('"df error, 1 to 100,000 (0 = ∞; PPL: 3+)"') == 4 and
      SRC.count('"df error, 1 to 100,000 (0 = auto: k(m-1))"') == 1)


def qcrit(path, tv):
    h = run(path, 'sr_CritMode()', [{'ta': 0.05, 'tk': 4, 'tv': tv}], secs=60)
    t = [x.text for x in h.texts if x.text.startswith('q crit = ')]
    return t[-1] if t else None


q5, q0, qold = qcrit(PROG, 100000), qcrit(PROG, 0), qcrit(OLD, 1E12)
check('X6 q crit (k 4, alpha .05, the PPL engine) at df 100,000 is the infinity value to four decimals (%s, %s); '
      'beta 15g at df 1E12 gave %s' % (q5, q0, qold), q5 is not None and q5 == q0 and qold is not None and qold != q0)

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
REFUSE = ['α must be from 0.001 to 0.2', 'k must be a whole number from 2 to', 'df must be from 1 to 100,000', 'm must be a whole number from 2 to']
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
RES = CC.runs(OLD, PROG, 'StudRange()', 30, 90, 'beta 15g|beta 15i', None)
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
