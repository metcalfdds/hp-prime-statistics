#!/usr/bin/env python3
"""verify_CICatcher_beta2e.py -- checks CICatcher beta 2e (1 Nov 2026), the fixes for what the monkey test found in
beta 2d (1,000 random runs under tools/monkey_v1b.py: 5 divisions by zero, 288 typed lists):
  - a typed sigma of 1E-300 (or a mu of 1E300) left the window mu +/- 6.5 sigma/sqrt(n) with zero width in 12 digits,
    and cqWindow divided by it.  The setup form now refuses a mu or sigma with more than 50 digits and a
    sigma/sqrt(n) below 1E-9 or below |mu| x 1E-8 (cqBadMsg), with a sentence, and the form comes back; the n form
    refuses an n that would make sigma/sqrt(n) that small;
  - every form field takes a real number only ({name,[0]});
  - an axis label that would touch the one before it is left out (long labels at a large mu).

This is a new script in the repository's present layout.  It runs from verify/ as it is: the program from
../programs, beta 2d from ../programs or git history (Lessons Learned rule 18), the harness, the overlap recorder and
tools/prime_facts_v1.py (the device facts the harness does not model yet) from ../tools, hp-prime-kit from $HPKIT.

R  beta 2e against beta 2d, screen for screen, over every interval type with ordinary numbers: setup, +10 three
   times, +1, the level up and down, a line picked, the n form, Help, Reset, the summary.  Every text the same.
M  the monkey test's findings, one check each, each also run on beta 2d, where it fails: the typed fields; the crash
   inputs refused with a sentence and the form back; the line; the n form; the largest and smallest numbers accepted
   drawing with no error; every new box within 4 lines at 32 characters.
G  static: only cqAskN, cqSetup, cqDrawAxis and the new cqBadMsg differ from beta 2d; every routine tagged cq; no "!=";
   the code ASCII, as before.
D  layout: text_overlap_v1 over every beta 2e screen drawn: no firm overlap, straddle or overrun.

Run:  python3 verify_CICatcher_beta2e.py [CICatcher_beta2e.txt]     (exit code 0 = all passed)
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
from ppl_run_v3e import Harness, CANCEL  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME = 'CICatcher_beta2e.txt'
PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, NAME)
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if (detail != '' and not ok) else ''))
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


OLD = older('CICatcher_beta2d.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()


def run(script, path=PROG):
    """the welcome page (any key), the setup, the loop: script queues answers and keys; Esc (idle) leaves the loop"""
    h = Harness(path, idle_key=4, home_minus=True, cas='fail')
    script(h)
    try:
        res = h.execute('CICatcher()')
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:150])
    return h, res, err


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


def g(h, k):
    return h.globals_.get(k)


MEAN = lambda mu, sg, n, lv: {'suTr': mu, 'suSD': sg, 'suNn': n, 'suLv': lv}  # noqa: E731
PROP = lambda p, n, lv: {'suTr': p, 'suNn': n, 'suLv': lv}  # noqa: E731
SOFT = lambda k: (int((k - 0.5) * 53.4), 230)  # noqa: E731   soft key k (1..6): +1, +10, +50, level, n, Menu


def s_session(typ, form):
    def f(h):
        h.press('Enter')                                  # the welcome page
        h.choose(typ)
        h.answer(form)
        for _ in range(3):
            h.press('Plus')                               # +10
        h.press('Up')
        h.press('Up')
        h.press('Down')
        h.press('Left')                                   # pick the newest line
        h.press('Right')
        h.tap(*SOFT(3))                                   # +50
        h.tap(*SOFT(5))                                   # the n form
        h.answer({'nkN': 30.0 if typ <= 2 else 40.0})
        h.press('Enter')                                  # the menu
        h.choose(3)                                       # Help: four pages, Esc ends
        h.press('Enter')
        h.press('Enter')
        h.press('Enter')
        h.press('Enter')
        h.press('Enter')                                  # the menu again
        h.choose(2)                                       # Reset the counts
        h.press('Plus')
    return f


# ===================================================================== R
print('=== R. beta 2e against beta 2d, screen for screen, with ordinary numbers')
print('   beta 2d: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))
cases = [(1, MEAN(100.0, 15.0, 20.0, 0.95)), (1, MEAN(-3.5, 0.2, 5.0, 0.9)), (2, MEAN(50.0, 10.0, 8.0, 0.99)),
         (2, MEAN(0.0, 1.0, 2.0, 95.0)), (3, PROP(0.3, 40.0, 0.95)), (4, PROP(0.1, 20.0, 0.9)),
         (5, PROP(0.5, 25.0, 0.95)), (5, PROP(0.02, 100.0, 0.999))]
same, diff, errs, nscr = 0, [], [], 0
for typ, form in cases:
    hn, rn, en = run(s_session(typ, form))
    ho, ro, eo = run(s_session(typ, form), OLD) if OLD else (None, None, 'no beta 2d')
    nscr += len(hn.screens)
    if en or eo:
        errs.append((typ, form, en, eo))
    elif texts(hn) == texts(ho) and rn == ro and boxes(hn) == boxes(ho):
        same += 1
    else:
        diff.append((typ, form, rn, ro))
check('R1 %d sessions (all five interval types; +10, +1, +50, the level, a line picked, the n form, Help, Reset): '
      '%d screens, every text and the summary identical to beta 2d\'s, no error' % (len(cases), nscr),
      OLD is not None and same == len(cases), (diff[:2], errs[:2]))

# ===================================================================== M
print("=== M. the monkey test's findings (1 Nov 2026; each check fails on beta 2d)")


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
check('M1 all %d forms take real numbers only: every field is {name,[0]} (%d fields); beta 2d\'s were bare names'
      % (len(ff), sum(len(f) for f in ff)), len(ff) == 3 and sum(len(f) for f in ff) == 8 and typed and not typed_old
      and OLD is not None, ff)

NARROW = ('σ/√n is too small next to μ for the calculator\'s 12 digits. Use a larger σ, a smaller n or a μ nearer 0.')
BIG = 'A number you typed has more than 50 digits: too large to work with.'


def s_form(typ, form, then=None):
    """the setup form with a refused value: the box, the form again; then Cancel (or a good answer)"""
    def f(h):
        h.press('Enter')
        h.choose(typ)
        h.answer(form)
        if then is None:
            h.answer(CANCEL)
        else:
            h.answer(then)
            h.press('Plus')
    return f


crash = [('z, sigma = 1E-300', 1, MEAN(0.0, 1E-300, 20.0, 0.95), NARROW),
         ('t, sigma = 1E-300', 2, MEAN(5.0, 1E-300, 10.0, 0.95), NARROW),
         ('z, mu = 1E300', 1, MEAN(1E300, 15.0, 20.0, 0.95), BIG),
         ('t, mu = -1E300', 2, MEAN(-1E300, 15.0, 20.0, 0.95), BIG),
         ('z, sigma = 1E300', 1, MEAN(0.0, 1E300, 20.0, 0.95), BIG),
         ('z, mu = 1E40, sigma = 1', 1, MEAN(1E40, 1.0, 20.0, 0.95), NARROW)]
for name, typ, form, want in crash:
    hn, rn, en = run(s_form(typ, form))
    ho, ro, eo = run(s_form(typ, form), OLD) if OLD else (None, None, 'no beta 2d')
    check('M2 %s: "%s", the form back (Cancel then: "%s"); beta 2d: no box, %s' % (
        name, want[:36] + '...', rn, eo or ro), en is None and boxes(hn) == [want]
        and rn == 'CICatcher: no interval chosen' and OLD is not None and not boxes(ho), (en, boxes(hn), rn, eo))
# after a refusal the student types a good value and goes on
hn, rn, en = run(s_form(1, MEAN(0.0, 1E-300, 20.0, 0.95), MEAN(0.0, 2.0, 20.0, 0.95)))
check('M2 after the box, sigma = 2 typed into the form that came back: the run goes on (%s)' % (rn or '')[:60],
      en is None and boxes(hn) == [NARROW] and (rn or '').startswith('CICatcher: ') and 'of 10' in (rn or ''),
      (en, boxes(hn), rn))

h = Harness(PROG, idle_key=4, home_minus=True, cas='fail')
h.execute('cqInit()')
line = [(h.execute('cqBadMsg(0, 0.000000001*SQRT(4), 4)'), ''), (h.execute('cqBadMsg(0, 0.00000000099*SQRT(4), 4)'), 'N'),
        (h.execute('cqBadMsg(1E9, 10*SQRT(9), 9)'), ''), (h.execute('cqBadMsg(-1E9, 9.99*SQRT(9), 9)'), 'N'),
        (h.execute('cqBadMsg(9.99E49, 9.99E49, 2)'), ''), (h.execute('cqBadMsg(-1E50, 1, 2)'), 'B'),
        (h.execute('cqBadMsg(0, 1E50, 2)'), 'B')]
got = ['' if a == '' else ('B' if a == BIG else ('N' if a == NARROW else a)) for a, _ in line]
check('M3 the lines: sigma/sqrt(n) of 1E-9 accepted, 9.9E-10 refused; at mu = +-1E9, 10 accepted and 9.99 refused; '
      '9.99E49 accepted, 1E50 refused: %s' % got, got == [b for _, b in line], (got, [b for _, b in line]))


def s_nform(nn):
    def f(h):
        h.press('Enter')
        h.choose(1)
        h.answer(MEAN(1E9, 50.0, 2.0, 0.95))                # sigma/sqrt(2) = 35.4: accepted
        h.tap(*SOFT(5))
        h.answer({'nkN': nn})                               # n = 100: sigma/sqrt(n) = 5 < 10
        h.press('Plus')
    return f


hn, rn, en = run(s_nform(100.0))
ho, ro, eo = run(s_nform(100.0), OLD) if OLD else (None, None, 'no beta 2d')
check('M4 the n form at mu = 1E9, sigma = 50: n = 100 (sigma/sqrt(n) = 5) refused, "... n did not change.", n stays 2; '
      'beta 2d took it (%s)' % ((ro or '')[-30:] if ho else '-'),
      en is None and boxes(hn) == [NARROW + ' n did not change.'] and 'n = 2' in (rn or '') and OLD is not None
      and not boxes(ho) and 'n = 100' in (ro or ''), (en, boxes(hn), rn, ro))
hn, rn, en = run(s_nform(4.0))
check('M4 the same form with n = 4 (sigma/sqrt(n) = 25): accepted, no box (%s)' % (rn or '')[-40:],
      en is None and not boxes(hn) and 'n = 4' in (rn or ''), (en, boxes(hn), rn))

big = []
for name, typ, form in (('z, mu = 9.9E49, sigma = 9.9E49, n = 2', 1, MEAN(9.9E49, 9.9E49, 2.0, 0.95)),
                        ('t, mu = -9.9E49, sigma = 9.9E49, n = 100', 2, MEAN(-9.9E49, 9.9E49, 100.0, 0.999)),
                        ('z, mu = 0, sigma/sqrt(n) = 1E-9', 1, MEAN(0.0, 1E-9 * 2 ** 0.5, 2.0, 0.95)),
                        ('t, mu = 1E9, sigma/sqrt(n) = 10', 2, MEAN(1E9, 100.0, 100.0, 0.95)),
                        ('t, mu = 0.001, sigma = 1E-8, n = 100', 2, MEAN(0.001, 1E-8, 100.0, 0.5))):
    hn, rn, en = run(lambda h, typ=typ, form=form: (h.press('Enter'), h.choose(typ), h.answer(form),
                                                    h.press('Plus'), h.press('Plus'), h.tap(*SOFT(3))))
    big.append((name, en, boxes(hn), (rn or '')[:50]))
check('M5 the largest and smallest numbers accepted run (setup, +10 twice, +50) with no error and no box, with '
      'STRING refusing 13 decimals as on the Prime: %s' % [(b[0], b[1]) for b in big],
      all(b[1] is None and not b[2] and b[3].startswith('CICatcher: ') for b in big), big)

msgs = [NARROW, BIG, NARROW + ' n did not change.']
lines = [len(textwrap.wrap(m, 32)) for m in msgs]
check('M6 every new box within 4 lines at 32 characters a line: %s' % lines, max(lines) <= 4, lines)

# ===================================================================== G
print('=== G. static checks')


def bodies(txt):
    lines_ = txt.split('\n')
    heads = [i for i, ln in enumerate(lines_) if re.match(r'^(EXPORT\s+)?[A-Za-z_]\w*\([^()]*\)\s*$', ln)]
    out = {}
    for k, i in enumerate(heads):
        nm = re.match(r'^(?:EXPORT\s+)?([A-Za-z_]\w*)', lines_[i]).group(1)
        out[nm] = '\n'.join(lines_[i:heads[k + 1] if k + 1 < len(heads) else len(lines_)])
    return out


upto_end = lambda t: t[:t.index('\nEND;') + 5] if '\nEND;' in t else t  # noqa: E731
bn, bo = bodies(SRC), bodies(OSRC)
changed = sorted(k for k in set(bn) | set(bo) if upto_end(bn.get(k, '')) != upto_end(bo.get(k, '')))
check('G1 only cqAskN, cqSetup, cqDrawAxis and the new cqBadMsg differ from beta 2d, code for code: %s' % changed,
      changed == ['cqAskN', 'cqBadMsg', 'cqDrawAxis', 'cqSetup'], changed)
code = [ln.split('//')[0] for ln in SRC.split('\n')]
routines = re.findall(r'^([A-Za-z_]\w*)\([^()]*\)\s*$', SRC, re.M)
check('G2 %d routines, every one tagged cq; at most six names on a LOCAL line; no "!=" (a factorial and a test on the '
      'Prime)' % len(routines), all(r.startswith('cq') for r in routines) and not any('!=' in c for c in code)
      and not [ln for ln in code if re.match(r'\s*LOCAL\b', ln) and len(ln.split('LOCAL', 1)[1].split(',')) > 6],
      [r for r in routines if not r.startswith('cq')])
check('G3 the code is ASCII, as beta 2d\'s is (its glyphs are built with CHAR(); only comments carry others)',
      all(ord(c) < 128 for ln in code for c in ln), [ln for ln in code if any(ord(c) > 127 for c in ln)][:3])

# ===================================================================== D
print('=== D. layout (text_overlap_v1 over every screen above)')
hn, rn, en = run(lambda h: (h.press('Enter'), h.choose(1), h.answer(MEAN(1E9, 100.0, 4.0, 0.95)), h.press('Plus')))
ho, ro, eo = run(lambda h: (h.press('Enter'), h.choose(1), h.answer(MEAN(1E9, 100.0, 4.0, 0.95)), h.press('Plus')),
                 OLD) if OLD else (None, None, None)
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
oko, fo = firm_of('CICatcher_beta2d')
check('D1 no firm overlap, frame straddle or overrun on any beta 2e screen drawn, mu = 1E9 included (beta 2d on the '
      'same runs: %d, %s)' % (len(fo), sorted(set(str(x[1]) for x in fo))[:3]), okn and not fn, fn[:6])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
