#!/usr/bin/env python3
"""verify_NormExplorer_beta42g.py -- checks NormExplorer beta 42g (2 Nov 2026, night; round 6: reasonable caps on what a
student types, and menu items that fit their box) against beta 42f.
Roger: "for alpha we dont need like 0.00001 or something--use real world values like 0.001, 0.01, 0.05, 0.1,
0.2 and so forth". Roger: "some of the menu items run out of the box": the box shows about 30 characters (round 2's rule; the
Virtual Calculator, 2 Nov 2026: BurrLab's box 214 px with items of 38 characters cut).
  G  static: only the critical values (ne_InvCalc), the power picture (ne_Compare2) and the data menu (ne_Histo) differ from beta 42f; the header names beta 42g; no new "!=", nothing new for the CAS.
  X  the three critical-value forms and the power picture refuse alpha 0.5 and 0.0005 and take 0.2; "x at a percentile" still takes 0.9; beta 42f took 0.5; every menu item at most 30 characters.
  R  the monkey, 30 seeds on both versions (tools/comma_check_v1.py): the same path but where a value is now refused,
     the same texts to the CAS, every big number grouped, no year grouped, no new overlap or cut number.
Run from verify/ as it is (beta 42f from ../programs, an _superseded_* folder or git history).
    python3 verify_NormExplorer_beta42g.py [NormExplorer_beta42f.txt]
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
NAME, OLDNAME = 'NormExplorer_beta42g.txt', 'NormExplorer_beta42f.txt'
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
print('=== NormExplorer beta 42g against beta 42f ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()
print('=== G. static')
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
WANT = ['ne_Compare2', 'ne_Histo', 'ne_InvCalc']
check("G1 only the critical values (ne_InvCalc), the power picture (ne_Compare2) and the data menu (ne_Histo) differ from beta 42f: %s" % diff, diff == WANT, diff)
check('G2 the header names beta 42g', '// NORM EXPLORER - beta 42g' in SRC and '// beta 42g (2 Nov 2026, night)' in SRC)
check('G3 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('CAS(') == OSRC.count('CAS(') and SRC.count('EXPR(') == OSRC.count('EXPR('))
print('=== X. alpha and the menu')

bad = []
for pick, var in ((2, 'icP'), (3, 'icP'), (4, 'icP')):
    for v, want in ((0.5, 1), (0.0005, 1), (0.2, 0), (0.001, 0)):
        h = run(PROG, 'ne_InvCalc()', [{var: v}], chooses=[pick], secs=10, first=['ne_ResetAll()'])
        got = any(t.startswith('α must be from 0.001 to 0.2') for t in msgs(h))
        if got != bool(want):
            bad.append((pick, v, msgs(h)[:2]))
for v, want in ((0.5, 1), (0.0005, 1), (0.2, 0)):
    h = run(PROG, 'ne_Compare2()', [{'c2A': v}], chooses=[3], secs=10, first=['ne_ResetAll()'])
    got = any(t.startswith('α must be from 0.001 to 0.2') for t in msgs(h))
    if got != bool(want):
        bad.append(('power', v, msgs(h)[:2]))
h = run(PROG, 'ne_InvCalc()', [{'icP': 0.9}], chooses=[1], secs=10, first=['ne_ResetAll()'])
if any('must be' in t for t in msgs(h)):
    bad.append(('percentile 0.9', msgs(h)[:1]))
check('X1 the critical values and the power picture refuse alpha 0.5 and 0.0005 and take 0.2 and 0.001; a percentile '
      'of 0.9 is still taken', not bad, bad)
o_ = run(OLD, 'ne_InvCalc()', [{'icP': 0.5}], chooses=[2], secs=10, first=['ne_ResetAll()'])
check('X2 beta 42f took alpha 0.5', not any('must be' in t or 'between' in t for t in msgs(o_)), msgs(o_)[:2])
WANT_ITEMS = ['My data: D1 (Statistics 1Var)', 'Regression residuals: C1, C2']

items = []
_src = CC.strip_comments(SRC)
for m_ in re.finditer(r'CHOOSE\s*\(', _src):
    t_ = _src[m_.end() - 1:]
    d_, q_ = 0, False
    for j_, ch in enumerate(t_):
        if ch == '"':
            q_ = not q_
        elif not q_ and ch in '([{':
            d_ += 1
        elif not q_ and ch in ')]}':
            d_ -= 1
            if d_ == 0:
                break
    items += re.findall(r'"([^"]*)"', t_[:j_ + 1])[1:]
longest = max(items, key=len)
check('XM every menu item at most 30 characters: %d items, the longest %d ("%s")' % (len(items), len(longest), longest),
      len(longest) <= 30 and all(w in items for w in WANT_ITEMS), [w for w in WANT_ITEMS if w not in items])

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
RES = CC.runs(OLD, PROG, 'NormExp()', 30, 30, 'beta 42f|beta 42g', None)
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
