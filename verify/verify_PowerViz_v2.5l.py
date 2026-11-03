#!/usr/bin/env python3
"""verify_PowerViz_v2.5l.py -- checks PowerViz v2.5l (2 Nov 2026), the fixes for what the monkey test found in v2.5k
(1,000 random runs under tools/monkey_v1b.py: 736 OK, 264 broken; 241 a list typed into a number field, 20 a mean or
sigma of 1E300, 3 a sigma of 1E-300):
  - every form field takes a real number only ({name,[0]}): the Edit form of each test, the n forms, the effect form;
  - a mean or sigma PowerViz cannot draw is refused with a sentence and nothing changes (pv_BadMsg): above 1,000,000,
    a sigma below 0.000001 or below |mu| x 0.000001 (the plot is the means +/- 6 SE in data units; in 12 digits a
    tick step below the means' 12th digit stops the tick loop, and the readouts' decimals must stay at 12 or fewer),
    and in test 5 a sigma2 outside 0.01 to 100 times sigma1.  The Edit form checks as typed and again after its own
    clamps; the effect form checks too;
  - at the largest and smallest numbers accepted, and at a small effect, every text keeps to its place: x labels that
    would overlap or run off are left out, readouts too wide are written scientific, H0 and H1 stand side by side,
    the 0.80 label moves out of the formula label's way, the SE line gives way to the n80 text in every test, and a
    formula-page line too long is wrapped.

This script runs from verify/ as it is: the program from ../programs, v2.5k from ../programs or git history (Lessons
Learned rule 18), the harness, the overlap recorder, label_fit_v1 and tools/prime_facts_v1.py (the device facts the
harness does not model yet) from ../tools, hp-prime-kit from $HPKIT.

R  v2.5l against v2.5k, screen for screen, with ordinary numbers: each of the five tests from its first form through
   the arrows, +/-, the n cell's form, Power vs n, Power vs effect size, the sample-size formula, Would Levene notice?,
   1/2-sided, and the exit box.  Every text, box and the returned power the same.
M  the findings, one check each, each also run on v2.5k, where it fails: the typed fields; the crash inputs refused
   with a sentence and the values kept; the lines of pv_BadMsg; the check after the clamps; the effect form; the
   largest and smallest numbers accepted running every page with no error; every new box within 4 lines at 32
   characters.
G  static: only the forms, the new pv_BadMsg, pv_TxW and pv_Fit, and six layout routines differ from v2.5k; no "!="; no glyph that
   v2.5k does not already show.
D  layout: text_overlap_v1 over every v2.5l screen drawn (no firm overlap, straddle or overrun), and label_fit_v1 (no
   number cut short by TEXTOUT_P's width argument, which would show a wrong number).

Run:  python3 verify_PowerViz_v2.5l.py [PowerViz_v2.5l.txt]     (exit code 0 = all passed)
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

NAME = 'PowerViz_v2.5l.txt'
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


OLD = older('PowerViz_v2.5k.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()


def run(script, path=PROG):
    """the test menu, the first form, the live plot; script queues picks, answers, keys and taps; Esc (idle) ends"""
    h = Harness(path, idle_key=4, home_minus=True, cas='fail')
    script(h)
    try:
        res = h.execute('POWERVIZ()')
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:160])
    return h, res, err


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


def g(h, k):
    return h.globals_.get(k)


NCELL = {1: (30, 156), 2: (30, 170), 3: (30, 170), 4: (30, 156), 5: (30, 170)}   # the n row of the readout box
FORMS = {1: {'MM0': 100.0, 'MM1': 106.0, 'SG': 15.0, 'NN': 30.0, 'AL': 0.05},
         2: {'MM0': 50.0, 'MM1': 55.0, 'SG': 10.0, 'NN': 40.0, 'AL': 0.01},
         3: {'MM0': 4.8185, 'MM1': 5.3, 'SG': 1.2, 'SG2': 2.1, 'e5a': 40.0, 'e5b': 20.0, 'AL': 0.05},
         4: {'PP0': 0.5, 'PP1': 0.6, 'NN': 100.0, 'AL': 0.05},
         5: {'PP0': 0.3, 'PP1': 0.4, 'NN': 200.0, 'AL': 0.05}}
NFORM = {1: {'env': 25.0}, 2: {'env': 60.0}, 3: {'env': 30.0, 'en2': 15.0}, 4: {'env': 150.0}, 5: {'env': 80.0}}


def s_session(item, form, nform, pages=(4, 5, 6, 7, 2)):
    def f(h):
        h.choose(item)
        h.answer(form)
        for k in ('Right', 'Right', 'Up', 'Plus', 'Minus', 'Left', 'Down'):
            h.press(k)
        h.tap(*NCELL[item])
        h.answer(nform)
        for p in pages:
            h.press('Enter')
            h.choose(p)
    return f


# ===================================================================== R
print('=== R. v2.5l against v2.5k, screen for screen, with ordinary numbers')
print('   v2.5k: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))
same, diff, errs, nscr = 0, [], [], 0
for item in (1, 2, 3, 4, 5):
    sc = s_session(item, FORMS[item], NFORM[item])
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no v2.5k')
    nscr += len(hn.screens)
    if en or eo:
        errs.append((item, en, eo))
    elif texts(hn) == texts(ho) and rn == ro and boxes(hn) == boxes(ho):
        same += 1
    else:
        diff.append((item, rn, ro, boxes(hn)[:2], boxes(ho)[:2]))
check('R1 the five tests (first form, arrows, +/-, the n form, Power vs n, Power vs effect, the formula, Would Levene '
      'notice?, 1/2-sided, the exit box): %d screens, every text, box and the returned power identical to v2.5k\'s, no '
      'error' % nscr, OLD is not None and same == 5, (diff[:2], errs[:2]))

# ===================================================================== M
print("=== M. the monkey test's findings (2 Nov 2026; each check fails on v2.5k)")


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
check('M1 all %d forms take real numbers only: every field is {name,[0]} (%d fields); v2.5k\'s were bare names'
      % (len(ff), sum(len(f) for f in ff)), len(ff) == 8 and sum(len(f) for f in ff) == 29 and typed
      and not typed_old and OLD is not None, ff)

BIG = 'Means and σ can be at most 1,000,000: use bigger units (thousands, millions).'
RATIO = 'σ₂ must be from 0.01 to 100 times σ₁.'
NARROW = 'σ is too small next to the means for the calculator\'s 12 digits. Use a larger σ or means nearer 0.'
CLOSE = 'The means differ by under a billionth of σ: no n could tell them apart.'
KEEP = ' Nothing changed.'
DEF = (100.0, 105.0, 15.0)      # MM0, MM1, SG as PowerViz starts


def s_bad(item, form):
    def f(h):
        h.choose(item)
        h.answer(form)
        h.press('Enter')
        h.choose(4)
    return f


crash = [('one-sample, sigma = 1E300', 1, {'SG': 1E300}, BIG),
         ('one-sample, mu1 = 1E300', 1, {'MM1': 1E300}, BIG),
         ('two-sample, mu0 = -1E300', 2, {'MM0': -1E300}, BIG),
         ('one-sample, sigma = 1E-300', 1, {'SG': 1E-300}, NARROW),
         ('two-sample, mu0 = 1E6, sigma = 0.5', 2, {'MM0': 1E6, 'SG': 0.5}, NARROW),
         ('unequal, sigma2 = 1E-300', 3, {'SG2': 1E-300}, NARROW),
         ('unequal, sigma1 = 1E300, mu2 = 1E300', 3, {'SG': 1E300, 'MM1': 1E300}, BIG),
         ('one-sample, mu0 = 1234567890123', 1, {'MM0': 1234567890123.0}, BIG),
         ('unequal, sigma2 = 101 sigma1', 3, {'SG': 1.0, 'SG2': 101.0}, RATIO),
         ('unequal, sigma2 = 0.009 sigma1', 3, {'SG': 100.0, 'SG2': 0.9}, RATIO),
         ('two-sample, mu0 = 1E-300, mu1 = 0, sigma = 999999', 2, {'MM0': 1E-300, 'MM1': 0.0, 'SG': 999999.0}, CLOSE)]
for name, item, form, want in crash:
    hn, rn, en = run(s_bad(item, form))
    ho, ro, eo = run(s_bad(item, form), OLD) if OLD else (None, None, 'no v2.5k')
    hr, _, _ = run(s_bad(item, {}))                  # the same run with the form's OK as shown: what it keeps
    kept = all(g(hn, k) == g(hr, k) for k in ('MM0', 'MM1', 'SG', 'SG2', 'NN', 'AL', 'NN2', 'KN1'))
    check('M2 %s: "%s", the values kept (%s), the plot drawn; v2.5k: %s' % (
        name, (want + KEEP)[:40] + '...', kept, (eo or 'no box, ' + str((boxes(ho) or [''])[0])[:40]) if ho else '-'),
        en is None and boxes(hn)[:1] == [want + KEEP] and kept and OLD is not None
        and (eo is not None or not (boxes(ho)[:1] == [want + KEEP])), (en, boxes(hn)[:2], rn, eo))

h = Harness(PROG, idle_key=4, home_minus=True, cas='fail')
h.execute('pv_Init()')
line = [('pv_BadMsg(0, 0, 0.000001, 0.000001)', ''), ('pv_BadMsg(0, 0, 0.00000099, 0.00000099)', 'N'),
        ('pv_BadMsg(1000000, 1000000, 1, 1)', ''), ('pv_BadMsg(1000000, 0, 0.99, 0.99)', 'N'),
        ('pv_BadMsg(0, -1000000.01, 5, 5)', 'B'), ('pv_BadMsg(0, 0, 1000000, 1000000)', ''),
        ('pv_BadMsg(0, 0, 1000000.1, 1000)', 'B'), ('pv_BadMsg(0, 0, 1, 100)', ''), ('pv_BadMsg(0, 0, 1, 100.1)', 'R'),
        ('pv_BadMsg(0, 0, 100, 1)', ''), ('pv_BadMsg(0, 0, 100, 0.99)', 'R'), ('pv_BadMsg(5, 0, -1, 5)', ''),
        ('pv_BadMsg(1E300, 0, 1, 1)', 'B'), ('pv_BadMsg(0, 0.000000001, 1, 1)', ''),
        ('pv_BadMsg(0, 0.00000000099, 1, 1)', 'C'), ('pv_BadMsg(5, 5, 1, 1)', ''),
        ('pv_BadMsg(0, 0.0000000101, 1, 10)', ''), ('pv_BadMsg(0, 0.0000000099, 1, 10)', 'C'),
        ('pv_BadMsg(1E-300, 0, 999999, 999999)', 'C')]
got = []
for call, _ in line:
    a = h.execute(call)
    got.append('' if a == '' else ('B' if a == BIG else ('N' if a == NARROW else ('R' if a == RATIO else ('C' if a == CLOSE else a)))))
check('M3 the lines of pv_BadMsg: means and sigma up to 1,000,000 accepted, above refused; sigma 0.000001 accepted, '
      '0.00000099 refused; at |mu| = 1E6, 1 accepted and 0.99 refused; sigma2/sigma1 from 0.01 to 100; a sigma of 0 '
      'or less left to the clamp; means apart by 1E-9 of the larger sigma accepted, by less refused, equal accepted: %s' % got, got == [b for _, b in line], list(zip([c for c, _ in line], got)))

hn, rn, en = run(s_bad(3, {'SG': 1000.0, 'SG2': 0.0}))
hr, _, _ = run(s_bad(3, {}))
ho, ro, eo = run(s_bad(3, {'SG': 1000.0, 'SG2': 0.0}), OLD) if OLD else (None, None, 'no v2.5k')
bx = boxes(hn)
check('M4 test 5, sigma1 = 1000 with sigma2 = 0: the clamp\'s box ("σ₂ must be positive ... reset to 1"), then the '
      'refusal after it (sigma2 = 1 is below 0.01 sigma1), the values kept; v2.5k: the clamp only (%s)'
      % ((boxes(ho) or [''])[:1] if ho else '-'),
      en is None and len(bx) >= 2 and bx[0].startswith('σ₂ must be positive') and bx[1] == RATIO + KEEP
      and all(g(hn, k) == g(hr, k) for k in ('MM0', 'MM1', 'SG', 'SG2', 'NN', 'AL')) and OLD is not None
      and not (len(boxes(ho)) >= 2 and boxes(ho)[1] == RATIO + KEEP), (en, bx[:3], eo))


def eff(path, val, tt=1, **kv):
    hh = Harness(path, idle_key=4, home_minus=True, cas='fail')
    hh.execute('pv_Init()')
    hh.globals_.update({'TT': float(tt)})
    hh.globals_.update({k: float(v) for k, v in kv.items()})
    hh.answer({'eev': float(val)})
    try:
        r = hh.execute('pv_EditEff()')
        e = None
    except Exception as ex:
        r, e = None, '%s: %s' % (type(ex).__name__, str(ex)[:90])
    return hh, r, e


res = []
for val, tt, kv, want in ((1E300, 1, {}, BIG), (-1E60, 2, {}, BIG), (1000001.0, 1, {}, BIG), (1E8, 5, {}, BIG),
                          (3.0, 1, {'MM0': 0.0, 'SG': 0.000002}, NARROW), (106.0, 1, {}, None),
                          (-1000000.0, 2, {}, None)):
    hn, rn, en = eff(PROG, val, tt, **kv)
    ho, ro, eo = eff(OLD, val, tt, **kv) if OLD else (None, None, 'no v2.5k')
    if want:
        ok = en is None and rn == 0 and boxes(hn) == [want + ' The mean did not change.'] and g(hn, 'MM1') == 105.0 \
            and OLD is not None and not boxes(ho) and g(ho, 'MM1') == val
    else:
        ok = en is None and rn == 1 and not boxes(hn) and g(hn, 'MM1') == val
    res.append((val, tt, ok))
check('M5 the effect form (a tap on the effect cell): 1E300, -1E60, 1,000,001 and 1E8 refused (above 1,000,000), 3 '
      'at sigma = 0.000002 refused (too far from 0), each with a sentence and the mean kept; 106 and -1,000,000 taken; '
      'v2.5k took them all: %s' % res, all(r[2] for r in res), res)

CORNERS = [('mu -1E6 and 1E6, sigma 1E6', 1, {'MM0': -1E6, 'MM1': 1E6, 'SG': 1E6}),
           ('mu 0 and 0.000001, sigma 0.000001, n 5000', 1, {'MM0': 0.0, 'MM1': 0.000001, 'SG': 0.000001, 'NN': 5000.0}),
           ('mu -1E6 and -999999, sigma 1, n 5000', 2, {'MM0': -1E6, 'MM1': -999999.0, 'SG': 1.0, 'NN': 5000.0}),
           ('unequal: mu 1E6, sigmas 1 and 100, n 5000 and 5000', 3,
            {'MM0': 1E6, 'MM1': 999999.0, 'SG': 1.0, 'SG2': 100.0, 'e5a': 5000.0, 'e5b': 5000.0}),
           ('unequal: sigmas 1E6 and 1E4, n 2 and 20', 3,
            {'MM0': 0.0, 'MM1': 1.0, 'SG': 1E6, 'SG2': 1E4, 'e5a': 2.0, 'e5b': 20.0}),
           ('d = 1E6 (mu 0 and 1E6, sigma 1)', 1, {'MM0': 0.0, 'MM1': 1E6, 'SG': 1.0}),
           ('d = 1E-9 (mu 0 and 0.001, sigma 1E6)', 1, {'MM0': 0.0, 'MM1': 0.001, 'SG': 1E6}),
           ('a small effect, d = 0.025 (100 and 100.25, sigma 10)', 2, {'MM0': 100.0, 'MM1': 100.25, 'SG': 10.0}),
           ('unequal: sigma2 = 100 sigma1', 3, {'MM0': 0.0, 'MM1': 5.0, 'SG': 1.0, 'SG2': 100.0, 'e5a': 40.0,
                                                'e5b': 20.0}),
           ('two-sample, mu -1E6 and 1E6, sigma 5E5, n 2', 2, {'MM0': -1E6, 'MM1': 1E6, 'SG': 5E5, 'NN': 2.0}),
           ('mu 999999.999 and 999999, sigma 1, n 2, alpha 1E-300', 1,
            {'MM0': 999999.999, 'MM1': 999999.0, 'SG': 1.0, 'NN': 2.0, 'AL': 1E-300})]


def firm_run(sc, path):
    """one run's firm overlaps and overruns (text_overlap_v1), its screens then kept with the rest for D"""
    saved = dict((k, v) for k, v in OV.RECORDS.items())
    OV.RECORDS.clear()
    h, r, e = run(sc, path)
    out = []
    for t, f in OV.report().items():
        out += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
        out += [(x['text'][:40], 'off the screen') for x in f['overruns'] if x['firm']]
    new = dict(OV.RECORDS)
    OV.RECORDS.clear()
    OV.RECORDS.update(saved)
    for k, v in new.items():
        if k in OV.RECORDS:
            OV.RECORDS[k]['screens'].update(v['screens'])
            OV.RECORDS[k]['n'] += v['n']
        else:
            OV.RECORDS[k] = v
    return h, r, e, out


big = []
for name, item, form in CORNERS:
    nf = {'env': 5000.0} if item != 3 else {'env': 5000.0, 'en2': 5000.0}
    sc = s_session(item, form, nf, pages=(4, 5, 6, 7, 2))
    hn, rn, en, fn = firm_run(sc, PROG)
    ho, ro, eo, fo = firm_run(sc, OLD) if OLD else (None, None, None, [])
    big.append((name, en, [b for b in boxes(hn) if 'Exported' not in b][:2], fn, fo))
check('M6 the corners of the ranges accepted, and a small effect, run every page (arrows, +/-, n = 5000, Power vs n, '
      'Power vs effect, the formula, Would Levene notice?, 1/2-sided) with no error and no refusal, STRING refusing 13 '
      'decimals as on the Prime: %s' % [(b[0][:28], b[1]) for b in big],
      all(b[1] is None and not b[2] for b in big), [(b[0], b[1], b[2]) for b in big])
check('M7 and on every one of those screens every text keeps to its place: no firm overlap and nothing off the screen '
      '(v2.5k on the same runs: %d, e.g. %s)' % (sum(len(b[4]) for b in big), [b[4][0] for b in big if b[4]][:3]),
      all(not b[3] for b in big) and sum(len(b[4]) for b in big) > 0, [(b[0], b[3]) for b in big if b[3]])



se = []
for name, form in (('two proportions 0.97 and 0.98, n = 4990', {'PP0': 0.97, 'PP1': 0.98, 'NN': 4990.0}),
                   ('two proportions 0.97 and 0.98, n = 5000', {'PP0': 0.97, 'PP1': 0.98, 'NN': 5000.0}),
                   ('one proportion 0.98 and 0.97, n = 4990', {'PP0': 0.98, 'PP1': 0.97, 'NN': 4990.0})):
    item = 5 if name.startswith('two') else 4      # the test list: ... 4 one proportion, 5 two proportions
    hn, rn, en, fn = firm_run(s_bad(item, form), PROG)
    ho, ro, eo, fo = firm_run(s_bad(item, form), OLD) if OLD else (None, None, 'no v2.5k', [])
    lines_ = sorted(set(t.text for sc in hn.screens for t in sc.texts if t.text.startswith('SE\u2080') and t.y == 204))
    se.append((name, en, fn, lines_, fo))
check('M10 the SE line gives way to the n80 text at 5.5 px a character, decimal points included (round 4\'s label check '
      'under random use: "SE0 = sqrt(2x0.975x0.025/4990) = 0.00313" reached "n80 = 3826"): no firm overlap, the line '
      'shortened to %s; v2.5k: %s' % ([x[3][:1] for x in se], [x[4][:1] for x in se]),
      all(x[1] is None and not x[2] and x[3] for x in se) and any(x[4] for x in se), se)


def s_snap(keys):
    def f(h):
        h.choose(2)
        h.answer({'MM0': 1E-300, 'SG': 999999.0})
        for k in keys:
            if isinstance(k, tuple):
                h.tap(*k)
            else:
                h.press(k)
        h.press('Enter')
        h.choose(4)
    return f


snap = []
for name, keys, want in (('Left', ['Left'], 1E-300), ('Left, Right, Left', ['Left', 'Right', 'Left'], 1E-300),
                         ('Left twice', ['Left', 'Left'], -50000.0)):
    hn, rn, en = run(s_snap(keys))
    ho, ro, eo = run(s_snap(keys), OLD) if OLD else (None, None, 'no v2.5k')
    snap.append((name, en, g(hn, 'MM1') == want, g(hn, 'MM1'), eo))
check('M9 the arrows (the monkey test\'s retest of this version, seed 1000164): two-sample, mu0 = 1E-300, sigma = '
      '999999, then the arrows step mu1 (15) onto 0, a difference of 1E-300: taken as equal means (mu1 = mu0), and '
      'the next step goes on to -50000, with no error; v2.5k: %s' % [x[4][:40] for x in snap],
      all(x[1] is None and x[2] for x in snap) and OLD is not None
      and all(x[4] is not None for x in snap), snap)

msgs = [BIG + KEEP, NARROW + KEEP, RATIO + KEEP, BIG + ' The mean did not change.',
        NARROW + ' The mean did not change.', CLOSE + KEEP, CLOSE + ' The mean did not change.']
lines = [len(textwrap.wrap(m, 32)) for m in msgs]
check('M8 every new box within 4 lines at 32 characters a line: %s' % lines, max(lines) <= 4, lines)

# ===================================================================== G
print('=== G. static checks')


def bodies(txt):
    lines_ = txt.split('\n')
    heads = [i for i, ln in enumerate(lines_) if re.match(r'^(?:EXPORT\s+|LOCAL\s+)?[A-Za-z_]\w*\([^()]*\)\s*$', ln)]
    out = {}
    for k, i in enumerate(heads):
        nm = re.match(r'^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z_]\w*)', lines_[i]).group(1)
        out[nm] = '\n'.join(lines_[i:heads[k + 1] if k + 1 < len(heads) else len(lines_)])
    return out


strip_c = lambda t: '\n'.join(ln.split('//')[0].rstrip() for ln in t.split('\n') if ln.split('//')[0].strip())  # noqa
upto_end = lambda t: t[:t.index('\nEND;') + 5] if '\nEND;' in t else t  # noqa: E731
bn, bo = bodies(SRC), bodies(OSRC)
changed = sorted(k for k in set(bn) | set(bo) if strip_c(upto_end(bn.get(k, ''))) != strip_c(upto_end(bo.get(k, ''))))
WANT = ['pv_BadMsg', 'pv_DLbl', 'pv_Draw', 'pv_EditEff', 'pv_EditForm', 'pv_EditN', 'pv_Fit', 'pv_Formula', 'pv_NumD',
        'pv_PCDraw', 'pv_Panel', 'pv_SELine', 'pv_Snap0', 'pv_StepEff', 'pv_Touch', 'pv_TxW']
check('G1 only these differ from v2.5k, code for code (comments aside): the forms (pv_EditForm, pv_EditN, '
      'pv_EditEff), the new pv_BadMsg, pv_Snap0 (with its two calls, pv_StepEff and pv_Touch), pv_TxW and pv_Fit, and the layouts (pv_Draw, pv_Panel, pv_DLbl, pv_SELine, '
      'pv_PCDraw, pv_Formula, pv_NumD): %s' % changed, changed == WANT, sorted(set(changed) ^ set(WANT)))


def late_calls(txt):
    lines_ = txt.split('\n')
    heads, cur, out = {}, None, []
    for i, ln in enumerate(lines_):
        m = re.match(r'^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z_]\w*)\(([^()]*)\)\s*$', ln)
        if m:
            heads.setdefault(m.group(1), i)
    for i, ln in enumerate(lines_):
        m = re.match(r'^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z_]\w*)\(([^()]*)\)\s*$', ln)
        if m:
            cur = m.group(1)
            continue
        for c in re.findall(r'\b([A-Za-z_]\w*)\(', re.sub(r'"[^"]*"', '""', ln.split('//')[0])):
            if c in heads and heads[c] > i and c != cur:
                out.append((c, cur))
    return sorted(set(out))


check('G5 every new routine is defined above its first call (the one call to a routine further down is v2.5k\'s own: '
      '%s)' % late_calls(SRC), late_calls(SRC) == late_calls(OSRC), late_calls(SRC))
code = [ln.split('//')[0] for ln in SRC.split('\n')]
check('G2 no "!=" in the code (a factorial and a test on the Prime)', not any('!=' in c for c in code))
gl_n = set(c for ln in code for c in ln if ord(c) > 127)
gl_o = set(c for ln in OSRC.split('\n') for c in ln.split('//')[0] if ord(c) > 127)
check('G3 no glyph on screen that v2.5k does not already show (Lessons Learned v7v: diff the non-ASCII set): new %s'
      % sorted(gl_n - gl_o), not (gl_n - gl_o), sorted(gl_n - gl_o))
hdr = SRC.split('\n')[3]
check('G4 the header names v2.5l: "%s"' % hdr.strip(), hdr.strip() == '// POWERVIZ - v2.5l')

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
oko, fo = firm_of('PowerViz_v2.5k')
check('D1 no firm overlap, frame straddle or overrun on any v2.5l screen drawn, the extremes included (v2.5k on the '
      'same runs: %d)' % len(fo), okn and not fn, fn[:6])
cut = LF.clipped(OV.RECORDS)
cn = cut.get(os.path.basename(PROG), [])
check('D2 no number cut short by its width argument on any v2.5l screen (label_fit_v1; v2.5k on the same runs: %d)'
      % len(cut.get('PowerViz_v2.5k.txt', [])), not cn, cn[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
