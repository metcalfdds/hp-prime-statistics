#!/usr/bin/env python3
"""verify_ScatterLab_beta2f.py -- checks ScatterLab beta 2f (2 Nov 2026), the fixes for what the monkey test found in
beta 2d (1,000 random runs under tools/monkey_v1b.py: 978 OK, 22 broken, all at "Type a point": 9 a typed list, 13 a
typed 1E300), and its axis labels:
  - the point form takes real numbers only ({name,[0]});
  - a point the plot cannot hold is refused with a sentence and not added (slPtMsg): 50 digits or more, or x or y
    values too close together for 12 digits (slTiny); loading C1 and C2 is refused the same way; the window and the
    fit treat such a spread as none;
  - axis labels are never cut by TEXTOUT_P's width (beta 2d cut "100000" to "10000" at the y axis): when a label does
    not fit, the axis is labelled in units of a power of ten ("x1E5") or from its lowest tick ("y = 1000000 +
    label");
  - the bottom y label is left out when the first x label would run into it (beta 2d drew "50" over "15");
  - the side panel's numbers fit its 86 px (slFitN, slFitT): beta 2e, the same day, had everything above, and on the
    Virtual Calculator its panel printed SSE = 18053333333 as "SSE = 1805333333", the last digit cut off; a line too
    wide is now written with its number in the scientific form ("SSE = 1.8053E10").  Beta 2e was never committed;
  - y-hat and y-bar are the font's own letters, CHAR(375) and CHAR(563), not the words (Roger, 2 Nov: a symbol gets
    a character; SymProbe beta 1 drew both in fonts 1 and 2 on the Virtual Calculator).

This script runs from verify/ as it is: the program from ../programs, beta 2d from ../programs or git history (Lessons
Learned rule 18), the harness, the overlap recorder, label_fit_v1 and tools/prime_facts_v1.py (the device facts the
harness does not model yet) from ../tools, hp-prime-kit from $HPKIT.

R  beta 2f against beta 2d, screen for screen, with ordinary data: the example, every menu item (far point, fit,
   residuals, guess, the calculus page, help, a typed point, delete), C1/C2 saved and loaded.  Same texts and boxes,
   with the two letters read back as the words they replace.
M  the findings, one check each, each also run on beta 2d, where it fails.
G  static: only the routines named below differ from beta 2d; no "!="; the code ASCII, as before.
D  layout: text_overlap_v1 and label_fit_v1 over every beta 2f screen drawn.

Run:  python3 verify_ScatterLab_beta2f.py [ScatterLab_beta2e.txt]     (exit code 0 = all passed)
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
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME = 'ScatterLab_beta2f.txt'
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


OLD = older('ScatterLab_beta2d.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()


def run(script, path=PROG, c1=None, c2=None):
    """script queues keys, menu picks and answers; Esc (idle) leaves the plot"""
    app = {'C1': [float(v) for v in c1], 'C2': [float(v) for v in c2]} if c1 is not None else None
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=app)
    script(h)
    try:
        res = h.execute('ScatterLab()')
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:160])
    return h, res, err


def isolated(script, path=PROG, c1=None, c2=None):
    """one run, with its own firm overlaps and cut numbers; its screens then kept with the rest for D"""
    saved = dict(OV.RECORDS)
    OV.RECORDS.clear()
    h, r, e = run(script, path, c1, c2)
    firm = []
    for t, f in OV.report().items():
        firm += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
        firm += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
    cut = sorted(set(x[0] for v in LF.clipped(OV.RECORDS).values() for x in v))
    new = dict(OV.RECORDS)
    OV.RECORDS.clear()
    OV.RECORDS.update(saved)
    for k, v in new.items():
        if k in OV.RECORDS:
            OV.RECORDS[k]['screens'].update(v['screens'])
            OV.RECORDS[k]['n'] += v['n']
        else:
            OV.RECORDS[k] = v
    return h, r, e, firm, cut


YW = {chr(0x177): 'y-hat', chr(0x233): 'y-bar'}


def words(x):
    """beta 2f's two letters read back as beta 2d's words, so the rest can be compared character for character"""
    if isinstance(x, str):
        for k, v in YW.items():
            x = x.replace(k, v)
        return x
    if isinstance(x, (list, tuple)):
        return type(x)(words(y) for y in x)
    return x


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


def g(h, k):
    return h.globals_.get(k)


def menu(h, k, sub=None):
    h.press('Enter')
    if sub is None:
        h.choose(k)
    else:
        h.choose(k, sub)


def typed(h, x, y):
    menu(h, 7)
    h.answer({'tpX': float(x), 'tpY': float(y)})


def s_tour(h):
    menu(h, 6, 1)               # the example
    menu(h, 3)                  # residuals on
    menu(h, 1)                  # a far-out point
    menu(h, 2)                  # fit the window
    typed(h, 30.5, 48.2)        # a typed point, outside the window: refit
    menu(h, 8)                  # delete the selected point
    menu(h, 4)                  # guess the line
    h.press('Up')
    h.press('Right')
    h.press('Down')
    h.press('Enter')            # reveal
    h.press('Esc')              # back to Add
    menu(h, 5)                  # least squares as calculus
    h.press('Enter')
    menu(h, 9)                  # help: its pages
    for _ in range(6):
        h.press('Enter')
    menu(h, 6, 3)               # save to C1, C2
    menu(h, 6, 4)               # clear
    menu(h, 6, 2)               # load C1, C2


def s_load(h):
    menu(h, 6, 2)
    menu(h, 3)
    menu(h, 1)


# ===================================================================== R
print('=== R. beta 2f against beta 2d, screen for screen, with ordinary data')
print('   beta 2d: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))
ORD = [('the example, every menu item, C1/C2 saved and loaded', s_tour, None, None),
       ('C1/C2: poverty-like numbers', s_load, [10.4, 14.9, 7.1, 18.6, 23.0, 25.0], [34.4, 43.5, 22.3, 36.1, 45.2,
                                                                                      35.3]),
       ('C1/C2: x from 0 to 9, y from 2 to 9.5', s_load, list(range(10)), [2, 3.5, 4, 5.5, 5, 7, 8.2, 8, 9.5, 9]),
       ('C1/C2: x 1 to 6, y 120 to 170', s_load, [1, 2, 3, 4, 5, 6], [120, 135, 150, 148, 170, 161])]
same, diff, errs, nscr = 0, [], [], 0
for name, sc, c1, c2 in ORD:
    hn, rn, en = run(sc, PROG, c1, c2)
    ho, ro, eo = run(sc, OLD, c1, c2) if OLD else (None, None, 'no beta 2d')
    nscr += len(hn.screens)
    if en or eo:
        errs.append((name, en, eo))
    elif words(texts(hn)) == texts(ho) and words(rn) == ro and words(boxes(hn)) == boxes(ho):
        same += 1
    else:
        diff.append((name, rn, ro, boxes(hn)[:2], boxes(ho)[:2]))
check('R1 %d sessions (the example and every menu item; three ordinary C1/C2 loads): %d screens, every text, box and '
      'the summary identical to beta 2d\'s once its two letters are read as the words, no error' % (len(ORD), nscr), OLD is not None and same == len(ORD),
      (diff[:2], errs[:2]))

# ===================================================================== M
print("=== M. the monkey test's findings, and the labels (2 Nov 2026; each check fails on beta 2d)")


def input_fields(src):
    code_ = '\n'.join(ln.split('//')[0] for ln in src.split('\n'))
    return re.findall(r'\bINPUT\((\{.*?\}\}|\{[^{}]*\})\s*,', code_)


ff, ffo = input_fields(SRC), input_fields(OSRC)
check('M1 the one form takes real numbers only: %s; beta 2d: %s' % (ff, ffo),
      ff == ['{{tpX,[0]}, {tpY,[0]}}'] and ffo == ['{tpX, tpY}'], (ff, ffo))

BIG = 'A number you typed has more than 50 digits: too large to work with.'
CLOSE = 'That point is too close to the others for the calculator\'s 12 digits.'
NOTADD = ' The point was not added.'


def s_points(pts, clear=True):
    def f(h):
        if clear:
            menu(h, 6, 4)
        for x, y in pts:
            typed(h, x, y)
        menu(h, 3)
        menu(h, 2)
    return f


cases = [('x = 1E300', [(1E300, 5.0)], [BIG + NOTADD], 0),
         ('y = -1E300', [(5.0, -1E300)], [BIG + NOTADD], 0),
         ('x = 0, 1E-300, 2E-300', [(0.0, 0.0), (1E-300, 1.0), (2E-300, 2.0)], [CLOSE + NOTADD] * 2, 1),
         ('y = 0, 1E-300, 2E-300 at x = 1, 2, 3', [(1.0, 0.0), (2.0, 1E-300), (3.0, 2E-300)], [CLOSE + NOTADD] * 2, 1),
         ('x = 1E9 and 1E9 + 1E-3', [(1E9, 1.0), (1E9 + 0.001, 2.0)], [CLOSE + NOTADD], 1)]
for name, pts, want, nkeep in cases:
    hn, rn, en = run(s_points(pts))
    ho, ro, eo = run(s_points(pts), OLD) if OLD else (None, None, 'no beta 2d')
    check('M2 typed points, %s: "%s", %d point(s) kept, no error; beta 2d: %s' % (
        name, want[0][:34] + '...', nkeep, eo or ('no box, n = %s' % g(ho, 'slN'))),
        en is None and boxes(hn) == want and g(hn, 'slN') == nkeep and OLD is not None and not boxes(ho),
        (en, boxes(hn), g(hn, 'slN'), eo))

h = Harness(PROG, idle_key=4, home_minus=True, cas='fail')
h.execute('slInit()')
line = [('slTiny(0, 0.000000001)', 0), ('slTiny(0, 0.00000000099)', 1), ('slTiny(1000000000, 1000000011)', 0),
        ('slTiny(1000000000, 1000000010)', 1), ('slTiny(5, 5)', 0), ('slTiny(-1E49, 1E49)', 0),
        ('slTiny(0, 1E-300)', 1)]
got = [h.execute(c) for c, _ in line]
check('M3 the lines of slTiny: a spread of 1E-9 is enough at 0, 9.9E-10 is not; at 1E9, 11 is enough and 10 is not (1E-8 of 1000000010 is 10.0000001); '
      'no spread is no spread: %s' % got, got == [w for _, w in line], list(zip([c for c, _ in line], got)))

LBIG = 'C1 or C2 holds a number of 50 digits or more: too large to work with. Nothing was loaded.'
LCLOSE = 'The x or y values in C1, C2 are too close together for the calculator\'s 12 digits. Nothing was loaded.'
lc = []
for name, c1, c2, want in (('y = 1E300', [1, 2, 3], [1, 1E300, 3], LBIG),
                           ('x = 0, 1E-300, 2E-300', [0, 1E-300, 2E-300], [1, 2, 3], LCLOSE),
                           ('y within 5E-10', [1, 2, 3], [7, 7 + 5E-10, 7], LCLOSE)):
    hn, rn, en = run(s_load, PROG, c1, c2)
    ho, ro, eo = run(s_load, OLD, c1, c2) if OLD else (None, None, 'no beta 2d')
    ok = en is None and boxes(hn)[:1] == [want] and OLD is not None and not boxes(ho)[:1] == [want]
    lc.append((name, ok, eo or 'loaded'))
check('M4 loading C1, C2: a number of 50 digits, x or y too close together: refused with a sentence, nothing loaded; '
      'beta 2d loaded them: %s' % lc, all(x[1] for x in lc), lc)

LAB = [('y 100,000 to 500,000', [1, 2, 3, 4, 5, 6], [100000, 250000, 180000, 420000, 390000, 500000], 'x1E5'),
       ('y 0.0011 to 0.0042', [1, 2, 3, 4, 5, 6], [0.0011, 0.0023, 0.0017, 0.0031, 0.0028, 0.0042], 'x1E-4'),
       ('y -20,000 to -5,000', [1, 2, 3, 4, 5, 6], [-20000, -15000, -17000, -9000, -6000, -5000], 'x1E3'),
       ('y 1,000,001 to 1,000,006', [1, 2, 3, 4, 5, 6], [1000001, 1000003, 1000002, 1000006, 1000005, 1000004],
        'y = 1000000 + label'),
       ('x and y from -9E49 to 9.9E49', [-9e49, 9e49, 1e49], [9.9e49, -9.9e49, 0], 'x1E49')]
norm = lambda t: t.replace('×', 'x').replace('ᴇ', 'E').replace('−', '-')  # noqa: E731
lab = []
for name, c1, c2, note in LAB:
    hn, rn, en, fn, cn = isolated(s_load, PROG, c1, c2)
    ho, ro, eo, fo, co = isolated(s_load, OLD, c1, c2) if OLD else (None, None, None, [], [])
    notes = sorted(set(norm(t.text) for s in hn.screens for t in s.texts if 'label' in t.text or '×' in t.text))
    lab.append((name, en, cn, notes, co))
check('M5 axis labels never cut: no number cut short by its width on any screen, the axis labelled in units or from '
      'its lowest tick instead (%s); beta 2d cut %d labels, e.g. %s' % (
          [x[3] for x in lab], sum(len(x[4]) for x in lab), [x[4][:2] for x in lab][:3]),
      all(x[1] is None and not x[2] and [n for n in x[3] if n == note] for x, (_, _, _, note) in zip(lab, LAB))
      and all(x[4] for x in lab[:4]), [(x[0], x[1], x[2], x[3]) for x in lab])

cor = []
for name, c1, c2 in (('x 100 to 300, y 20 to 50', [100, 150, 220, 300, 260], [20, 35, 41, 50, 28]),
                     ('x and y either side of 0', [-50, -20, 10, 30, 50], [-20, -5, 3, 12, 20]),
                     ('x 1000 to 3000, y -500 to 900', [1000, 1500, 2200, 3000], [-500, 100, 900, 300]),
                     ('x -8 to -1, y 0.1 to 0.9', [-8, -6, -5, -3, -1], [0.1, 0.35, 0.3, 0.6, 0.9])):
    hn, rn, en, fn, cn = isolated(s_load, PROG, c1, c2)
    ho, ro, eo, fo, co = isolated(s_load, OLD, c1, c2) if OLD else (None, None, None, [], [])
    cor.append((name, en, fn, fo))
check('M6 the corner: the bottom y label is left out where the first x label would run into it: no firm overlap; beta '
      '2d: %s' % [x[3][:1] for x in cor], all(x[1] is None and not x[2] and x[3] for x in cor), cor)

ext = []
for name, pts in (('+-9.9E49', [(-9.9E49, 9.9E49), (9.9E49, -9.9E49), (0.0, 0.0)]),
                  ('a spread of 1E-9 at 0', [(0.0, 0.0), (0.000000001, 2.0), (0.0000000005, 1.0)]),
                  ('a spread of 11 at 1E9', [(1E9, 1.0), (1E9 + 11.0, 2.0), (1E9 + 5.0, 0.5)]),
                  ('a y spread of 2E-8 at 1', [(1.0, 1.0), (2.0, 1.00000002), (3.0, 1.00000001)])):
    def sc(h, pts=pts):
        s_points(pts)(h)
        menu(h, 1)
        menu(h, 4)
        h.press('Up')
        h.press('Enter')
        h.press('Esc')
        menu(h, 5)
        h.press('Enter')
    hn, rn, en, fn, cn = isolated(sc)
    ext.append((name, en, boxes(hn), fn, cn, g(hn, 'slN')))
check('M7 the largest and smallest accepted (points at +-9.9E49, spreads of 1E-9 at 0 and 11 at 1E9, a y spread of '
      '2E-8 at 1; the far point makes 4): every point added, the fit, a far point, guess, the calculus page, with no error, no box, no overlap and '
      'no number cut: %s' % [(x[0], x[1], x[5]) for x in ext],
      all(x[1] is None and not x[2] and not x[3] and not x[4] and x[5] == 4.0 for x in ext), ext)

# M9: the panel (beta 2f; the Virtual Calculator, 2 Nov 2026, evening)
PAN = [('C1/C2 as on the Virtual Calculator: x 1 to 6, y 100,000 to 500,000', [1, 2, 3, 4, 5, 6],
        [100000, 250000, 180000, 420000, 390000, 500000]),
       ('x 1 to 6, y in the millions', [1, 2, 3, 4, 5, 6], [1200000, 3100000, 2500000, 5800000, 4900000, 7300000]),
       ('x in the hundred-thousands, y 1 to 9', [150000, 320000, 410000, 640000, 880000], [1, 3, 2.5, 6, 9]),
       ('x and y near -1E9', [-1E9, -9.9E8, -9.8E8, -9.7E8], [-1E9, -9.85E8, -9.9E8, -9.6E8])]
pan = []
for name, c1, c2 in PAN:
    hn, rn, en, fn, cn = isolated(s_load, PROG, c1, c2)
    ho, ro, eo, fo, co = isolated(s_load, OLD, c1, c2) if OLD else (None, None, None, [], [])
    sse = sorted(set(t.text for sc in hn.screens for t in sc.texts if t.text.startswith('SSE = ')))
    pan.append((name, en, cn, sse, co))
check('M9 the side panel\'s numbers fit its 86 px: no line cut short at a digit on any screen (label_fit_v1 looks at '
      'every line since 2 Nov, evening), the SSE in the scientific form when too long (%s); beta 2d cut %d lines '
      '(beta 2e too, on the Virtual Calculator: "SSE = 1805333333" for 18053333333)' % (
          [x[3][:1] for x in pan], sum(len(x[4]) for x in pan)),
      all(x[1] is None and not x[2] and x[3] for x in pan) and any(x[4] for x in pan), pan)

# M10: y-hat and y-bar as letters (beta 2f, Roger 2 Nov 2026)
hy, ry, ey = run(s_tour, PROG)
hw, rw, ew = run(s_tour, OLD) if OLD else (None, None, 'no beta 2d')
allt = [t.text for sc in hy.screens for t in sc.texts] + boxes(hy) + [ry or '']
allw = ([t.text for sc in hw.screens for t in sc.texts] + boxes(hw) + [rw or '']) if hw else []
nyh = sum(t.count(chr(0x177)) for t in allt)
nyb = sum(t.count(chr(0x233)) for t in allt)
nword = [t for t in allt if 'y-hat' in t or 'y-bar' in t]
nold = sum(1 for t in allw if 'y-hat' in t or 'y-bar' in t)
check('M10 y-hat and y-bar as letters: the tour shows %s %d times and %s %d times, the words never (%d texts); the summary '
      'in Home "%s"; beta 2d: the words in %d texts' % (chr(0x177), nyh, chr(0x233), nyb, len(nword), (ry or '')[:40], nold),
      ey is None and nyh > 0 and nyb > 0 and not nword and nold > 0 and chr(0x177) in (ry or ''), (ey, nword[:3]))

msgs = [BIG + NOTADD, CLOSE + NOTADD, LBIG, LCLOSE]
lines = [len(textwrap.wrap(m, 32)) for m in msgs]
check('M8 every new box within 4 lines at 32 characters a line: %s' % lines, max(lines) <= 4, lines)

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
WANT = sorted(['slSetRes', 'slAutoWin', 'slFit', 'slAxes', 'slTypePt', 'slLoadC', 'slTiny', 'slMeas', 'slLab',
               'slLabMode', 'slLabNote', 'slPtMsg', 'slFitN', 'slFitT', 'slPanel', 'slInit'])
check('G1 only these differ from beta 2d, code for code (comments aside): %s' % changed, changed == WANT,
      sorted(set(changed) ^ set(WANT)))
code = [ln.split('//')[0] for ln in SRC.split('\n')]
check('G2 no "!=" in the code (a factorial and a test on the Prime)', not any('!=' in c for c in code))
check('G3 the code is ASCII, as beta 2d\'s is (its glyphs are built with CHAR(); only comments carry others)',
      all(ord(c) < 128 for ln in code for c in ln), [ln for ln in code if any(ord(c) > 127 for c in ln)][:3])
hdr = SRC.split('\n')[3]
check('G4 the header names beta 2f: "%s"' % hdr.strip(), hdr.strip() == '// SCATTERLAB - beta 2f')

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
oko, fo = firm_of('ScatterLab_beta2d')
check('D1 no firm overlap, frame straddle or overrun on any beta 2f screen drawn (beta 2d on the same runs: %d)'
      % len(fo), okn and not fn, fn[:6])
cut = LF.clipped(OV.RECORDS)
cn = cut.get(os.path.basename(PROG), [])
check('D2 no number cut short by its width argument on any beta 2f screen (label_fit_v1; beta 2d on the same runs: %d)'
      % len(cut.get('ScatterLab_beta2d.txt', [])), not cn, cn[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
