#!/usr/bin/env python3
"""verify_TrendTest_beta3i.py -- checks TrendTest beta 3i (2 Nov 2026, night; round 6: reasonable caps on what a
student types, and menu items that fit their box) against beta 3h.
A caps probe gave a level a total of 1E12 ("1E12" on the screen), and beta 3h's results table cut numbers
short from about 5,000 a level ("1,250/5,000" in a 52 px column; "19,999.0" in 40).
  G  static: only data entry (trEnter) and the results table (trPage1) differ from beta 3h; the header names beta 3i; no new "!=", nothing new for the CAS.
  X  six levels of 5,000 and of 99,999: nothing on any screen cut, as entered and as midranks (beta 3h cut 5,000's); a total of 100,000 refused with a sentence, 99,999 taken.
  R  the monkey, 30 seeds on both versions (tools/comma_check_v1.py): the same path but where a value is now refused,
     the same texts to the CAS, every big number grouped, no year grouped, no new overlap or cut number.
Run from verify/ as it is (beta 3h from ../programs, an _superseded_* folder or git history).
    python3 verify_TrendTest_beta3i.py [TrendTest_beta3h.txt]
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
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
# Overlap rule (as BurrLab beta 1l's verify): tools/text_overlap_v1 calls a straddle firm when it survives its narrower
# widths, 5.5 px for every character; here it is judged at the measured widths instead (tools/label_fit_v1.measure:
# 5.5 px a character in font 1, 3 px a decimal point; Lessons Learned).  The results table's CI column, laid out again in beta 3i, ends at about x = 313.5 at those widths, inside the frame (x = 315); the Virtual Calculator showed the snoring example's "(0.012-0.026)" ending inside it (2 Nov 2026, night).  Every CI has the same 13 characters.
_ANALYSE = OV.analyse_screen


def _analyse_measured(d):
    coll, strad, over, ghosts = _ANALYSE(d)
    info = {(it['text'], it['x'], it['y']): it for it in d['items'] if 'text' in it}
    out = []
    for (txt, x, y, which, by, firm) in strad:
        it = info.get((txt, x, y), {})
        f = OV._font(it.get('font', 1))
        w = len(txt) * OV.CW[f]
        if it.get('width') is not None:
            w = min(w, it['width'])
        mw = LF.measure(txt, it.get('font', 1))
        if firm and which == 'right':
            firm = x + mw > x + w - by          # the frame's right edge is at x + w - by
        elif firm and which == 'left':
            firm = x + mw > x + by
        out.append((txt, x, y, which, by, firm))
    return coll, out, over, ghosts


OV.analyse_screen = _analyse_measured
NAME, OLDNAME = 'TrendTest_beta3i.txt', 'TrendTest_beta3h.txt'
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
print('=== TrendTest beta 3i against beta 3h ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()
print('=== G. static')
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
WANT = ['trEnter', 'trPage1']
check("G1 only data entry (trEnter) and the results table (trPage1) differ from beta 3h: %s" % diff, diff == WANT, diff)
check('G2 the header names beta 3i', '// TRENDTEST - beta 3i' in SRC and '// beta 3i (2 Nov 2026, night)' in SRC)
check('G3 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('CAS(') == OSRC.count('CAS(') and SRC.count('EXPR(') == OSRC.count('EXPR('))
print('=== X. the results table')

import label_fit_v1 as LF  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402


def table(path, tot, lv=6, mid=False):
    h = Harness(path, idle_key=4)
    h.answer({'a%d' % i: i - 1 for i in range(1, lv + 1)}, {'a%d' % i: (tot * i) // (lv + 2) for i in range(1, lv + 1)},
             {'a%d' % i: tot for i in range(1, lv + 1)})
    h.choose(lv - 1)
    h.execute('trEnter()')
    if mid:
        h.globals_['trScM'] = 2.0
        h.execute('trSetX()')
        h.execute('trCompute()')
    h.execute('trPage1()')
    g1 = h.grobs['G1']
    cut = [t.text for t in g1.items if t.__class__.__name__ == 'Text' and t.width is not None and
           LF.hidden_tail(t.text, OV._font(t.font), float(t.width))]
    over = [t.text for t in g1.items if t.__class__.__name__ == 'Text' and float(t.x) + LF.measure(t.text, 1) > 318]
    return h, cut, over


bad = []
for tot, mid in ((5000, False), (99999, False), (99999, True), (12345, True)):
    h, cut, over = table(PROG, tot, 6, mid)
    if cut or over or msgs(h):
        bad.append((tot, mid, cut[:3], over[:2], msgs(h)[:1]))
check('X1 six levels of 5,000, 12,345 and 99,999, as entered and as midranks: nothing in the results table cut or past '
      'the screen', not bad, bad)
h, cut, over = table(OLD, 5000, 6, False)
check('X2 beta 3h cut 5,000\'s table: %s' % cut[:2], len(cut) > 0, cut)
h, cut, over = table(PROG, 100000, 3, False)
h2, cut2, over2 = table(PROG, 99999, 3, False)
check('X3 a total of 100,000 is refused with a sentence; 99,999 is taken',
      msgs(h)[:1] == ["A level's total can be at most 99,999: the results table shows its numbers whole up to there."]
      and not msgs(h2), (msgs(h)[:1], msgs(h2)[:1]))

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
REFUSE = ["A level's total can be at most 99,999"]
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
RES = CC.runs(OLD, PROG, 'TrendTest()', 30, 30, 'beta 3h|beta 3i', None)
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
