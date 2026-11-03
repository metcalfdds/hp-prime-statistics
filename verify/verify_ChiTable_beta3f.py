#!/usr/bin/env python3
"""verify_ChiTable_beta3f.py -- checks ChiTable beta 3f (2 Nov 2026), the fixes for what the monkey test found in
beta 3e (1,000 random runs under tools/monkey_v1b.py: 894 OK, 106 broken, every one a list typed into a count or
alpha field), and the typed alpha that Lessons Learned v7m's audit named:
  - every form field takes a real number only ({name,[0]}): the Values form (four or six counts), the one-cell form
    and the alpha form;
  - a typed alpha must be from 0.0001 to below 1.  The critical value is CHISQUARE_ICDF(df, 1 - alpha), and 1 - alpha
    is 1 in 12 digits for an alpha below about 5E-13 (in the harness's 16, below about 1E-16), which gives an
    infinite critical value with no error.  The refusal says so in a box, and alpha does not change.

This script runs from verify/ as it is: the program from ../programs, beta 3e from ../programs or git history
(Lessons Learned rule 18), the harness, the overlap recorder and tools/prime_facts_v1.py (the device facts the
harness does not model yet) from ../tools, hp-prime-kit from $HPKIT.

R  beta 3f against beta 3e, screen for screen, with ordinary counts: the three shapes typed in the Values form, a
   cell typed alone (a fraction rounded, a count too large refused), alpha set to 0.01, the four example tables and
   every page and plot.  Every text, box and the summary the same.
M  the findings, one check each, each also run on beta 3e, where it fails: the typed fields; a tiny alpha refused
   with a sentence and alpha unchanged; the edges of the alpha range; the largest and smallest alpha accepted
   drawing every page with a finite critical value; the new box within 4 lines at 32 characters; the observed
   chi-square's label on the curve page on the screen when the observed value sets the window (round 4's label
   check under random use found it past the right edge).
G  static: only csAskAll, csCvDraw, csEntry and csSetAlpha differ from beta 3e; no "!="; the code ASCII, as before.
D  layout: text_overlap_v1 and label_fit_v1 over every beta 3f screen drawn: no firm overlap, straddle or overrun,
   and no number cut short by its width argument.

Run:  python3 verify_ChiTable_beta3f.py [ChiTable_beta3f.txt]     (exit code 0 = all passed)
"""
import glob
import math
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
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME = 'ChiTable_beta3f.txt'
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


OLD = older('ChiTable_beta3e.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()


def run(script, path=PROG):
    """the main menu; script queues menu picks, form answers, keys and taps; Esc (idle) leaves each view"""
    h = Harness(path, idle_key=4, home_minus=True, cas='fail')
    script(h)
    try:
        res = h.execute('ChiTable()')
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


VALUES, RUN = (80, 230), (300, 230)          # the entry grid's Values and Run soft keys
QUIT = 14


def s_values(shape, counts, then=()):
    """a new table of a shape (1: 2x2, 2: 2x3, 3: 3x2), every count in the Values form, Run; then menu picks"""
    def f(h):
        h.choose(shape)
        h.tap(*VALUES)
        h.answer(dict(('a%d' % (i + 1), float(c)) for i, c in enumerate(counts)))
        h.tap(*RUN)
        for k in then:
            h.choose(k)
        h.choose(QUIT)
    return f


def s_cell(shape, counts, cell_val):
    """the Values form, then Enter (edit cell 1) with one value typed, then Run"""
    def f(h):
        h.choose(shape)
        h.tap(*VALUES)
        h.answer(dict(('a%d' % (i + 1), float(c)) for i, c in enumerate(counts)))
        h.press('Enter')
        h.answer({'enV': float(cell_val)})
        h.tap(*RUN)
        h.choose(5)
        h.choose(QUIT)
    return f


def s_alpha(al, example=1, pages=(5, 6, 7, 8, 9, 10)):
    """Set alpha, then an example table, then each page and plot"""
    def f(h):
        h.choose(11)
        h.answer({'alV': float(al)})
        h.choose(12, example)
        for k in pages:
            h.choose(k)
        h.choose(QUIT)
    return f


ALL_PAGES = (5, 6, 7, 8, 9, 10)

# ===================================================================== R
print('=== R. beta 3f against beta 3e, screen for screen, with ordinary counts')
print('   beta 3e: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))
cases = [('2x2 typed, every page', s_values(1, (12, 5, 9, 14), ALL_PAGES)),
         ('2x3 typed, results and curve', s_values(2, (20, 30, 25, 10, 15, 40), (5, 8))),
         ('3x2 typed, a count of 1E8 refused', s_values(3, (5, 1E8, 7, 9, 4, 6), (5,))),
         ('2x2, cell 1 typed as 2.5', s_cell(1, (3, 1, 1, 3), 2.5)),
         ('2x3, cell 1 typed as -4 (Run refuses it)', s_cell(2, (3, 1, 1, 3, 2, 2), -4)),
         ('alpha 0.01, example 1, every page', s_alpha(0.01, 1)),
         ('alpha 0.10, example 3, every page', s_alpha(0.10, 3)),
         ('example 2, every page', s_alpha(0.05, 2)),
         ('example 4, every page', s_alpha(0.05, 4)),
         ('example 5 (Simpson), every page', s_alpha(0.05, 5))]
same, diff, errs, nscr = 0, [], [], 0
for name, sc in cases:
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no beta 3e')
    nscr += len(hn.screens)
    if en or eo:
        errs.append((name, en, eo))
    elif texts(hn) == texts(ho) and rn == ro and boxes(hn) == boxes(ho):
        same += 1
    else:
        diff.append((name, rn, ro, boxes(hn)[:2], boxes(ho)[:2]))
check('R1 %d sessions (the three shapes typed, a cell typed alone, alpha 0.01 and 0.10, the five examples, every '
      'page and plot): %d screens, every text, box and the summary identical to beta 3e\'s, no error'
      % (len(cases), nscr), OLD is not None and same == len(cases), (diff[:2], errs[:2]))

# ===================================================================== M
print("=== M. the monkey test's findings (2 Nov 2026; each check fails on beta 3e)")


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
check('M1 all %d forms take real numbers only: every field is {name,[0]} (%d fields); beta 3e\'s were bare names'
      % (len(ff), sum(len(f) for f in ff)), len(ff) == 5 and sum(len(f) for f in ff) == 18 and typed
      and not typed_old and OLD is not None, ff)

ALBOX = 'α must be from 0.0001 to below 1 (0.05 is usual, 0.01 is strict). It did not change.'


def s_tiny(al):
    def f(h):
        h.choose(11)
        h.answer({'alV': float(al)})
        h.choose(12, 1)
        h.choose(8)                       # the chi-square curve and its critical value
        h.choose(QUIT)
    return f


for al in (1E-17, 1E-300):
    hn, rn, en = run(s_tiny(al))
    ho, ro, eo = run(s_tiny(al), OLD) if OLD else (None, None, 'no beta 3e')
    crit_n, crit_o = g(hn, 'csCrit'), (g(ho, 'csCrit') if ho else None)
    check('M2 alpha = %g typed: "%s", alpha stays 0.05 and the critical value is finite (%.4f); beta 3e: no box, '
          'alpha %s, critical value %s%s' % (al, ALBOX[:30] + '...', crit_n if crit_n is not None else float('nan'),
                                              g(ho, 'csAlpha') if ho else '-', crit_o, (', ' + eo) if eo else ''),
          en is None and boxes(hn) == [ALBOX] and g(hn, 'csAlpha') == 0.05 and crit_n is not None
          and math.isfinite(crit_n) and OLD is not None and not boxes(ho)
          and (eo is not None or (crit_o is not None and not math.isfinite(crit_o))),
          (en, boxes(hn), g(hn, 'csAlpha'), crit_n, eo, crit_o))

edge = []
for al, ok in ((0.0001, 1), (0.00009999, 0), (0.9999, 1), (1.0, 0), (0.0, 0), (-0.05, 0)):
    hn, rn, en = run(lambda h, al=al: (h.choose(11), h.answer({'alV': float(al)}), h.choose(QUIT)))
    got = (en is None and not boxes(hn) and g(hn, 'csAlpha') == al) if ok else \
        (en is None and boxes(hn) == [ALBOX] and g(hn, 'csAlpha') == 0.05)
    edge.append((al, ok, got))
check('M3 the alpha range: 0.0001 and 0.9999 accepted; 0.00009999, 1, 0 and -0.05 refused with the box, alpha '
      'unchanged: %s' % [(a, 'ok' if o else 'refused') for a, o, _ in edge], all(x[2] for x in edge), edge)

big = []
for al in (0.0001, 0.9999):
    for ex in (1, 3, 4):
        hn, rn, en = run(s_alpha(al, ex, ALL_PAGES))
        cr = g(hn, 'csCrit')
        big.append((al, ex, en, boxes(hn), cr))
FISHER_ONLY = "Fisher's exact distribution is drawn for a 2 × 2 table only."
check('M4 the largest and smallest alpha accepted, on three example tables, every page and plot: no error, a finite '
      'critical value, and no box but the Fisher plot\'s own note on the 2 x 3 and 3 x 2 tables: %s'
      % [(b[0], b[1], round(b[4], 4) if b[4] is not None else None) for b in big],
      all(b[2] is None and b[3] == ([] if b[1] == 1 else [FISHER_ONLY]) and b[4] is not None and math.isfinite(b[4])
          for b in big), big)

lines = [len(textwrap.wrap(m, 32)) for m in (ALBOX,)]
check('M5 the new box within 4 lines at 32 characters a line: %s' % lines, max(lines) <= 4, lines)


def x2_labels(h):
    """the observed chi-square's label on the curve page: (text, x, its right end at 5.5 px a character)"""
    return sorted(set((t.text, t.x, t.x + 5.5 * len(t.text)) for sc in h.screens for t in sc.texts
                      if t.text.startswith('\u03c7\u00b2 = ') and t.y == 40))


lab = []
for counts in ((50, 5, 5, 50), (30, 10, 10, 30), (40, 2, 3, 41)):
    hn, rn, en = run(s_values(1, counts, (8,)))
    ho, ro, eo = run(s_values(1, counts, (8,)), OLD) if OLD else (None, None, 'no beta 3e')
    ln, lo = x2_labels(hn), (x2_labels(ho) if ho else [])
    lab.append((counts, en, ln, lo))
check('M6 the observed chi-square\'s label on the curve page stays on the screen when the observed value sets the '
      'window (it goes left of its line near the right edge, as crit\'s does): %s; beta 3e kept it right of the '
      'line, past x = 320 at 40, 2, 3, 41: %s' % (
          [x[2] for x in lab], [x[3] for x in lab]),
      all(x[1] is None and x[2] and all(r <= 318 for _, _, r in x[2]) for x in lab)
      and any(r > 320 for x in lab for _, _, r in x[3]), lab)

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


strip_c = lambda t: '\n'.join(ln.split('//')[0].rstrip() for ln in t.split('\n'))  # noqa: E731
upto_end = lambda t: t[:t.index('\nEND;') + 5] if '\nEND;' in t else t  # noqa: E731
bn, bo = bodies(SRC), bodies(OSRC)
changed = sorted(k for k in set(bn) | set(bo) if strip_c(upto_end(bn.get(k, ''))) != strip_c(upto_end(bo.get(k, ''))))
check('G1 only csAskAll, csCvDraw, csEntry and csSetAlpha differ from beta 3e, code for code (comments aside): %s'
      % changed, changed == ['csAskAll', 'csCvDraw', 'csEntry', 'csSetAlpha'], changed)
code = [ln.split('//')[0] for ln in SRC.split('\n')]
check('G2 no "!=" in the code (a factorial and a test on the Prime)', not any('!=' in c for c in code))
check('G3 the code is ASCII, as beta 3e\'s is (its glyphs are built with CHAR(); only comments carry others)',
      all(ord(c) < 128 for ln in code for c in ln), [ln for ln in code if any(ord(c) > 127 for c in ln)][:3])
hdr = SRC.split('\n')[3]
check('G4 the header names beta 3f: "%s"' % hdr.strip(), hdr.strip() == '// CHITABLE - beta 3f')

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
oko, fo = firm_of('ChiTable_beta3e')
check('D1 no firm overlap, frame straddle or overrun on any beta 3f screen drawn, alpha 0.0001 and 0.9999 included '
      '(beta 3e on the same runs: %d)' % len(fo), okn and not fn, fn[:6])
cut = LF.clipped(OV.RECORDS)
cn = cut.get(os.path.basename(PROG), [])
check('D2 no number cut short by its width argument on any beta 3f screen (label_fit_v1; beta 3e on the same runs: %d)'
      % len(cut.get('ChiTable_beta3e.txt', [])), not cn, cn[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
