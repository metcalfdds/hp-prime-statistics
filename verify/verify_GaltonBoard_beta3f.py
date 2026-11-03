#!/usr/bin/env python3
"""verify_GaltonBoard_beta3f.py -- checks GaltonBoard beta 3f (2 Nov 2026), the fixes for what the monkey test and
round 4's label check found in beta 3e:
  - the two forms (rows R, chance p) take real numbers only ({name,[0]}): the monkey typed lists into them, and a list
    went on into IP() and the range test ("IP given a list", "< between a list and a number");
  - the bin panel (a tap on a bar) starts at x = 2, over the left readouts at x = 4, whose first two pixels showed
    beside its edge ("n = 0" beside "Bin 6 (6 right bounces of 8)");
  - the board holds at most 5,000 balls (Roger, 2 Nov 2026: "a reasonable limit on number of balls a student can
    collect--above the threshold just display the results", then "maybe limit to 5,000 or so?"): every drop takes at
    most what is left, a pour stops when the board is full, and a full board shows its results, both overlays on and a
    line in the footer; the MicroPython drop, "Drop 100,000", is "Fill to 5,000";
  - a peg's count, redrawn as a ball passes, stands 1 px further left and clears a box from 25 px left of the peg to
    3 px short of it, so the old number ("9") is wholly erased under the new one ("10"), and the peg is not touched.

This script runs from verify/ as it is: the program from ../programs, beta 3e from ../programs or git history (Lessons
Learned rule 18), the harness, the overlap recorder, label_fit_v1 and tools/prime_facts_v1.py from ../tools,
hp-prime-kit from $HPKIT.

R  beta 3f against beta 3e, screen for screen: the welcome, drops of 1, 10 (animated), 100 and 1000, the overlays and
   SD colours, R and p typed, the arrows, Pascal's counts and C(r,k) during an animated drop, a bar tapped, help,
   reset.  Same texts, boxes and returned summary, but for the help's two lines about the big drop.
M  the findings, one check each, each also run on beta 3e, where it fails.
G  static: only the forms, the panel, the peg counts and the limit's routines differ from beta 3e; no "!="; the header names beta 3f.
D  layout: text_overlap_v1 and label_fit_v1 over every beta 3f screen drawn.

Run:  python3 verify_GaltonBoard_beta3f.py [GaltonBoard_beta3f.txt]     (exit code 0 = all passed)
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
_cands = [c for c in (os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
                      HERE) if c]
for cand in reversed(_cands):
    if os.path.exists(os.path.join(cand, 'ppl_run_v3e.py')):
        sys.path.insert(0, cand)
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME = 'GaltonBoard_beta3f.txt'
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


OLD = older('GaltonBoard_beta3e.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()

SLOT = [27, 80, 133, 187, 240, 294]      # the soft keys' centres: Drop, x10, x100, Pour, Rows, Menu
X0, BW, HB = 12, 33, 191                 # R = 8: the bars start at x 12, 33 px a bin, the bin labels below y 191


def run(script, path=PROG):
    """the welcome screen takes a key; script queues taps, keys, menu picks and answers; Esc (idle) leaves"""
    h = Harness(path, idle_key=4, home_minus=True, cas='fail')
    h.press('Enter')
    script(h)
    try:
        res = h.execute('GaltonBoard()')
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:160])
    return h, res, err


def firm_run(script, path=PROG):
    """one run, with its own firm overlaps and cut numbers; its screens then kept with the rest for D"""
    saved = dict(OV.RECORDS)
    OV.RECORDS.clear()
    h, r, e = run(script, path)
    firm = []
    for t, f in OV.report().items():
        firm += [(c['a'][:30], c['b'][:30], c['func']) for c in f['collisions'] if c['severity'] == 'overlap'
                 and c['firm']]
        firm += [(x['text'][:30], 'off the screen', x['func']) for x in f['overruns'] if x['firm']]
    new = dict(OV.RECORDS)
    OV.RECORDS.clear()
    OV.RECORDS.update(saved)
    for k, v in new.items():
        if k in OV.RECORDS:
            OV.RECORDS[k]['screens'].update(v['screens'])
            OV.RECORDS[k]['n'] += v['n']
        else:
            OV.RECORDS[k] = v
    return h, r, e, firm


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


def g(h, k):
    return h.globals_.get(k)


def menu(h, k):
    h.press('Enter')
    h.choose(k)


def soft(h, k):
    h.tap(SLOT[k - 1], 230)


def bar(h, k):
    h.tap(X0 + k * BW + BW // 2, HB + 5)


# ===================================================================== R
print('=== R. beta 3f against beta 3e, screen for screen, with ordinary use')
print('   beta 3e: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))


def s_drops(h):
    soft(h, 1)                   # one ball, animated
    soft(h, 2)                   # x10, animated
    soft(h, 3)                   # x100, fast
    menu(h, 4)                   # 1000, fast
    menu(h, 8)                   # overlay: binomial
    menu(h, 8)                   # binomial + normal
    menu(h, 9)                   # colour bars by SDs
    bar(h, 4)                    # the middle bar's panel
    h.press('Esc')
    menu(h, 15)                  # help
    menu(h, 13)                  # reset


def s_typed(h):
    menu(h, 6)
    h.answer({'srR': 6.0})
    menu(h, 7)
    h.answer({'spP': 0.3})
    soft(h, 3)
    h.press('Right')             # p 0.35, a new board
    h.press('Up')                # R 7
    soft(h, 3)
    bar(h, 2)
    h.press('Esc')


def s_pascal(h):
    menu(h, 10)                  # Pascal: the counts
    soft(h, 2)                   # x10, animated: the counts tick up
    soft(h, 2)
    menu(h, 10)                  # Pascal: C(r, k)
    soft(h, 1)


def s_empty_bar(h):
    bar(h, 6)                    # a bar's panel with no balls yet
    h.press('Esc')
    soft(h, 1)
    bar(h, 6)
    h.press('Esc')


ORD = [('drops of 1, 10, 100 and 1000, overlays, SD colours, a bar, help, reset', s_drops),
       ('R = 6 and p = 0.3 typed, 100 balls, the arrows, a bar', s_typed),
       ("Pascal's counts during two animated x10 drops, then C(r, k)", s_pascal),
       ('a bar tapped before any ball, and after one', s_empty_bar)]
HELP_NEW = ("Menu: Pascal's triangle, SD colours, and", 'MicroPython (the board holds 5,000 balls).')
HELP_OLD = ("Menu: Pascal's triangle, SD colours, Drop", '100,000 (MicroPython; PPL fallback 5,000).')


def texts_as_old(h):
    """beta 3f's texts with the help's two new lines written back as beta 3e's (the only text R expects to differ)"""
    return [tuple(dict(zip(HELP_NEW, HELP_OLD)).get(t, t) for t in sc) for sc in texts(h)]


nhelp = [0]
same, diff, errs, nscr = 0, [], [], 0
for name, sc in ORD:
    hn, rn, en = run(sc, PROG)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no beta 3e')
    nscr += len(hn.screens)
    if en or eo:
        errs.append((name, en, eo))
    elif texts_as_old(hn) == texts(ho) and rn == ro and boxes(hn) == boxes(ho):
        same += 1
        nhelp[0] += sum(1 for sc in texts(hn) if HELP_NEW[1] in sc)
    else:
        diff.append((name, rn, ro, len(hn.screens), len(ho.screens)))
check('R1 %d sessions (every drop, overlays, SD colours, R and p typed, the arrows, Pascal\'s counts, bars, help, '
      'reset): %d screens, every text, box and the summary identical to beta 3e\'s but for the help\'s two lines about '
      'the big drop (on %d help screens), no error' % (len(ORD), nscr, nhelp[0]),
      OLD is not None and same == len(ORD) and nhelp[0] > 0, (diff[:2], errs[:2]))

# ===================================================================== M
print("=== M. the monkey test's findings and round 4's label check (2 Nov 2026; each check fails on beta 3e)")


def input_fields(src):
    code_ = '\n'.join(ln.split('//')[0] for ln in src.split('\n'))
    return re.findall(r'\bINPUT\((\{.*?\}\}|\{[^{}]*\})\s*,', code_)


ff, ffo = input_fields(SRC), input_fields(OSRC)
check('M1 both forms take real numbers only: %s; beta 3e: %s' % (ff, ffo),
      ff == ['{{srR,[0]}}', '{{spP,[0]}}'] and ffo == ['{srR}', '{spP}'], (ff, ffo))

pan = []
for name, sc in (('a bar before any ball', s_empty_bar), ('the middle bar after 1,111 balls', s_drops)):
    hn, rn, en, fn = firm_run(sc, PROG)
    ho, ro, eo, fo = firm_run(sc, OLD) if OLD else (None, None, None, [])
    pan.append((name, en, [f for f in fn if 'gbBinInfo' in f[2]], [f for f in fo if 'gbBinInfo' in f[2]]))
check('M2 the bin panel covers the left readouts ("n = 0", the mean, s at x = 4): no firm overlap on its screens; '
      'beta 3e: %s' % [x[3][:2] for x in pan], all(x[1] is None and not x[2] for x in pan) and any(x[3] for x in pan),
      pan)

hn, rn, en, fn = firm_run(s_pascal, PROG)
ho, ro, eo, fo = firm_run(s_pascal, OLD) if OLD else (None, None, None, [])
pegs_n = sorted(set(t.text for s in hn.screens for t in s.texts if re.fullmatch(r'1[0-9]', t.text)))
check("M3 Pascal's counts during an animated drop: the old count is wholly erased under the new one (\"9\" under "
      '"10"), no firm overlap on any screen (counts up to %s); beta 3e: %s' % (pegs_n[-1:] or '-', fo[:2]),
      en is None and not fn and pegs_n and any(f[:2] == ('9', '10') for f in fo), (en, fn[:4], fo[:4]))

m = re.search(r'RECT_P\(G3, plX - (\d+), plY - 8, plX - (\d+), plY \+ 2, gbWHT, gbWHT\)', SRC)
t = re.search(r'TEXTOUT_P\(plS, G3, plX - (\d+) - 5 \* DIM\(plS\)', SRC)
lft, rgt, tx = (int(m.group(1)), int(m.group(2)), int(t.group(1))) if m and t else (None, None, None)
# the peg: x from -2 to +2 about its centre; its left neighbour, 28 px or more away (counts need pegs 28 px apart),
# ends at -26; a count of n characters at -tx - 5n is at most 5.5 n wide (the overlap check's narrow measure)
fits = m and t and rgt >= 3 and lft <= 25 and all(-tx - 5 * n >= -lft and -tx - 5 * n + 5.5 * n <= -rgt
                                                  for n in (1, 2, 3, 4))
check("M4 a peg's clearing box (x from -%s to -%s of the peg's centre) misses the peg (-2 to +2) and its left "
      'neighbour (-26 or further), and holds every count of 1 to 4 characters (drawn from -%s - 5n)' % (lft, rgt, tx),
      bool(fits), (lft, rgt, tx))

FULL = '5000 balls: the board is full (Menu, Reset)'


class _TimeUp(Exception):
    pass


def _alarm(signum, frame):
    raise _TimeUp()


def at(path, n0, call):
    """a board set up and drawn (gbInit, gbScene), n set to n0, then one drop routine called directly (no idle key: a pour runs until the
    board is full or its own count is reached)"""
    h = Harness(path, home_minus=True, cas='fail')
    h.execute('gbInit()')
    h.execute('gbScene()')                      # the board drawn, as the main loop does before any drop
    h.globals_['gbN'] = float(n0)
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(60)                            # beta 3e's pour has no end of its own here
    try:
        r = h.execute(call)
        e = None
    except _TimeUp:
        r, e = None, 'no end within 60 s'
    except Exception as ex:
        r, e = None, '%s: %s' % (type(ex).__name__, str(ex)[:80])
    finally:
        signal.alarm(0)
    return r, e, g(h, 'gbN'), g(h, 'gbMsg'), g(h, 'gbOvl')


lim = []
for n0, call, want_n, want_msg in ((4995, 'gbDropFast(100)', 5000, FULL), (5000, 'gbDropFast(100)', 5000, FULL),
                                   (4999, 'gbDropAnim()', 5000, None), (5000, 'gbDropAnim()', 5000, FULL),
                                   (4995, 'gbPour(3, 10)', 5000, FULL), (4990, 'gbPour(2, 0)', 5000, FULL),
                                   (5000, 'gbPour(2, 0)', 5000, FULL), (5000, 'gbBigDrop(5000)', 5000, FULL),
                                   (4000, 'gbDropFast(100)', 4100, None)):
    r, e, n, msg, ovl = at(PROG, n0, call)
    ok = e is None and n == want_n and (msg == want_msg if want_msg else msg != FULL) and (ovl == 2) == (want_msg is not None)
    ro, eo, no, msgo, ovlo = at(OLD, n0, call) if OLD else (None, 'no beta 3e', None, None, None)
    lim.append((n0, call, ok, n, msg if msg == FULL else '-', no if eo is None else eo))
check('M5 the board holds at most 5,000 balls (Roger, 2 Nov 2026): from n = 4,995 a drop of 100 or a x10 pour stops '
      'at 5,000, from 4,990 a pour stops itself there, a full board drops nothing, and each shows "%s" with both '
      'overlays on; below the limit nothing changes; beta 3e: n = %s' % (FULL, [x[5] for x in lim]),
      all(x[2] for x in lim) and OLD is not None
      and any(isinstance(x[5], float) and x[5] > 5000 for x in lim), lim)
r3 = []
h = Harness(PROG, home_minus=True, cas='fail')
h.execute('gbInit()')
for n0 in (0, 4999, 5000, 5001, 1E300):
    h.globals_['gbN'] = float(n0)
    r3.append(h.execute('gbRoom()'))
check('M6 the lines of gbRoom: room for %s balls at n = 0, 4,999, 5,000, 5,001 and 1E300' % r3,
      r3 == [5000.0, 1.0, 0.0, 0.0, 0.0], r3)
menu_ok = ('"Fill to 5,000 (MicroPython)",' in SRC and 'IF mnI == 5 THEN gbBigDrop(5000); END;' in SRC
           and '"Drop 100,000 (MicroPython)"' not in SRC and '"Drop 100,000 (MicroPython)"' in OSRC)
check('M8 the menu\'s MicroPython item reads "Fill to 5,000 (MicroPython)" and drops at most 5,000', menu_ok)
msg_w = 5.5 * len(FULL)
check('M7 the full board\'s line fits the footer: %d characters, %.0f px at 5.5 px a character (the footer takes 312)'
      % (len(FULL), msg_w), msg_w <= 312)

# ===================================================================== G
print('=== G. static checks')


def bodies(txt):
    lines_ = txt.split('\n')
    heads = [i for i, ln in enumerate(lines_) if re.match(r'^(?:EXPORT\s+)?[A-Za-z_]\w*\([^()]*\)\s*$', ln)]
    out = {}
    for k, i in enumerate(heads):
        nm = re.match(r'^(?:EXPORT\s+)?([A-Za-z_]\w*)', lines_[i]).group(1)
        out[nm] = '\n'.join(lines_[i:heads[k + 1] if k + 1 < len(heads) else len(lines_)])
    return out


strip_c = lambda t: '\n'.join(ln.split('//')[0].rstrip() for ln in t.split('\n') if ln.split('//')[0].strip())  # noqa
upto_end = lambda t: t[:t.index('\nEND;') + 5] if '\nEND;' in t else t  # noqa: E731
bn, bo = bodies(SRC), bodies(OSRC)
changed = sorted(k for k in set(bn) | set(bo) if strip_c(upto_end(bn.get(k, ''))) != strip_c(upto_end(bo.get(k, ''))))
WANT = ['gbBigDrop', 'gbBinInfo', 'gbDropAnim', 'gbDropFast', 'gbFull', 'gbHelp', 'gbMenu', 'gbPegLbl', 'gbPour',
        'gbRoom', 'gbSetP', 'gbSetRows']
check('G1 only these differ from beta 3e, code for code (comments aside): the forms, the panel, the peg counts, and the '
      'limit (the new gbRoom and gbFull, the four drops, the menu item and the help\'s two lines): %s' % changed,
      changed == WANT,
      sorted(set(changed) ^ set(WANT)))
code = [ln.split('//')[0] for ln in SRC.split('\n')]
check('G2 no "!=" in the code (a factorial and a test on the Prime)', not any('!=' in c for c in code))
nonascii = sorted(set(c for ln in code for c in ln if ord(c) > 127))
onon = sorted(set(c for ln in OSRC.split('\n') for c in ln.split('//')[0] if ord(c) > 127))
check('G3 no character in the code that beta 3e\'s code does not already have: %s' % nonascii, nonascii == onon,
      (nonascii, onon))
hdr = SRC.split('\n')[3]
check('G4 the header names beta 3f: "%s"' % hdr.strip(), hdr.strip() == '// GALTONBOARD - beta 3f')

# ===================================================================== D
print('=== D. layout (text_overlap_v1 and label_fit_v1 over every screen above)')
rep = OV.report()


def firm_of(tag0):
    t = [t for t in rep if t.startswith(tag0)]
    f = rep[t[0]] if t else None
    out = []
    if f:
        out += [('overlap', c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
        out += [('straddle', x['text'], x['edge']) for x in f['straddles'] if x['firm']]
        out += [('overrun', x['text'], x.get('right')) for x in f['overruns'] if x['firm']]
        print('   %s: %d distinct screens of %d' % (t[0], f['screens_distinct'], f['screens_total']))
    return bool(t), out


okn, fn = firm_of(os.path.splitext(os.path.basename(PROG))[0])
oko, fo = firm_of('GaltonBoard_beta3e')
check('D1 no firm overlap, frame straddle or overrun on any beta 3f screen drawn (beta 3e on the same runs: %d)'
      % len(fo), okn and not fn, fn[:6])
cut = LF.clipped(OV.RECORDS)
cn = cut.get(os.path.basename(PROG), [])
check('D2 no number cut short by its width argument on any beta 3f screen (label_fit_v1; beta 3e on the same runs: %d)'
      % len(cut.get('GaltonBoard_beta3e.txt', [])), not cn, cn[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
