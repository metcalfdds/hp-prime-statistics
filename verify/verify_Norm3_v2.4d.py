#!/usr/bin/env python3
"""verify_Norm3_v2.4d.py -- checks Norm3 v2.4d (1 Nov 2026, night): v2.4c's checks (against v2.4b, as there) and
section Y, the density labels that ran over the axis on the Virtual Calculator (against v2.4b, whose labels
v2.4c kept).  v2.4c's were
about the monkey test's round and what the Virtual Calculator
showed.
  - n3_fmtp's "pv != 0" is "pv <> 0": on the Prime "!=" is a factorial and a test ({3!=0, 0!=0} = {0, 0}; 999!=0
    "Numerical overflow"; the Virtual Calculator, 1 Nov 2026), so the "< 0.0001" floor never ran there.  The harness
    reads "!=" as "not equal" and cannot show this; G2 checks the code instead.
  - what Norm3 cannot draw is refused with a sentence before anything is drawn: a non-number argument, a number with
    more than 50 digits, a sigma above 1E10 (density labels past STRING's 12 decimals), a sigma below 1E-9 or below
    |mu| x 1E-8 (too few 12-digit numbers in the window);
  - the sigma keys keep sigma inside those limits, and sigma- never raises a small typed sigma.

A new script in the repository's present layout: the program from ../programs, v2.4b from ../programs or git history
(Lessons Learned rule 18), the harness, the overlap recorder and tools/prime_facts_v1.py from ../tools.

R  v2.4d against v2.4b, screen for screen, with ordinary arguments and every key: identical.
M  the findings, one check each, each also run on v2.4b, where it fails.
G  static: only Norm3, n3_fmtp and n3_Help (its title) differ from v2.4b; no "!=" in the code.
D  layout: text_overlap_v1 over every v2.4d screen drawn: no firm overlap, straddle or overrun (v2.4b's x labels
   ran into each other at a large mu or a small sigma).

Run:  python3 verify_Norm3_v2.4d.py [Norm3_v2.4d.txt]     (exit code 0 = all passed)
"""
import glob
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import warnings
from decimal import Decimal, Context, ROUND_HALF_UP

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
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME = 'Norm3_v2.4d.txt'
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


OLD = older('Norm3_v2.4b.txt')
OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
OV.install()


def run(call, keys=(), path=PROG):
    """Norm3 called from Home with its three arguments; keys are queued; Esc (idle) quits"""
    h = Harness(path, idle_key=4, home_minus=True, cas='fail')
    for k in keys:
        if isinstance(k, tuple):
            h.tap(*k)
        else:
            h.press(k)
    try:
        res = h.execute(call)
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:150])
    return h, res, err


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


def split_xlab(h):
    """each screen's texts without the x tick labels (font 1 at y 194, the row under the axis), and those labels"""
    rest, lab = [], []
    for s_ in h.screens:
        r, l_ = [], []
        for t in s_.texts:
            (l_ if (t.y == 194 and t.text not in ('x',)) else r).append((t.text, t.x, t.y))
        rest.append(r)
        lab.append(l_)
    return rest, lab


def ynorm(row):
    """v2.4d: a screen's texts with the density labels written in units of a power of ten turned back into
    v2.4b's form (the value at the step's decimals), and the power's note left out.  A screen record can hold
    several drawings (an animation); each drawing's labels run up the axis (y falling), and its note follows
    them"""
    import math
    frames, cur, last_y = [], None, None
    for i, t in enumerate(row):
        if t[1] == 1:
            if cur is None or t[2] > last_y:
                cur = {'idx': [], 'k': None}
                frames.append(cur)
            cur['idx'].append(i)
            last_y = t[2]
        elif t[0].startswith('×') and cur is not None:
            cur['k'] = float(t[0].replace('×', '').replace('ᴇ', 'e').replace('−', '-'))
    out = list(row)
    for f in frames:
        if f['k'] is None:
            continue
        ms = [float(row[i][0]) for i in f['idx']]
        step = (ms[1] - ms[0] if len(ms) > 1 else ms[0]) * f['k']
        d = max(0, -int(math.floor(math.log10(step) + 1E-9)))
        for i in f['idx']:
            out[i] = ('%.*f' % (d, float(row[i][0]) * f['k']), row[i][1], row[i][2])
    return [t for t in out if not t[0].startswith('×')]


def g(h, k):
    return h.globals_.get(k)


# ===================================================================== R
print('=== R. v2.4d against v2.4b, screen for screen, ordinary arguments and every key')
print('   v2.4b: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))
KEYS = ['Left', 'Right', 'Right', 'Down', 'Up', 'Up', 'Minus', 'Plus', 'Plus', 'Zero', 'Down', 'Down']
calls = ['Norm3(0,1,1.96)', 'Norm3(100,15,130)', 'Norm3(-2.5,0.4,-3)', 'Norm3(500,100,350)', 'Norm3(0,1,0.004)',
         'Norm3(0,1,-6)', 'Norm3(0.5,0.0002,0.5003)', 'Norm3(100,-15,130)', 'Norm3(0,0,1)']
same, diff, errs, nscr, dropped, model_ok = 0, [], [], 0, [], []


def thin(row):
    """v2.4c's rule applied to v2.4b's label row: walking left to right, a label is drawn only if it starts at
    least 4 px past the right end of the last one drawn (or of the "x" caption, which ends at x 11) and ends by
    x 319; 6 px a character.  A new axis drawing (x going back to the left) starts the walk again."""
    out, right, last_x = [], 11, None
    for t in row:
        if last_x is not None and t[1] <= last_x:
            right = 11
        last_x = t[1]
        if t[1] >= right + 4 and t[1] + 6 * len(t[0]) <= 319:
            out.append(t)
            right = t[1] + 6 * len(t[0])
    return out


for c in calls:
    for keys in (KEYS, [(150, 100), (60, 120), 'Enter']):
        hn, rn, en = run(c, keys)
        ho, ro, eo = run(c, keys, OLD) if OLD else (None, None, 'no v2.4b')
        nscr += len(hn.screens)
        if en or eo:
            errs.append((c, en, eo))
            continue
        rn_, ln_ = split_xlab(hn)
        rn_ = [ynorm(r) for r in rn_]   # v2.4d: density labels written out
        ro_, lo_ = split_xlab(ho)
        sub = all(set(a) <= set(b) for a, b in zip(ln_, lo_))
        dropped += sorted(set(x for a, b in zip(ln_, lo_) for x in set(b) - set(a)))
        model_ok.append(all(thin(b) == a for a, b in zip(ln_, lo_)) and len(ln_) == len(lo_))
        if rn_ == ro_ and rn == ro and sub and len(ln_) == len(lo_):
            same += 1
        else:
            diff.append((c, rn, ro))
check('R1 %d calls x 2 key sets (every key: mu, sigma, x0, re-centre; taps and the menu): %d screens, every text and '
      'the summary identical to v2.4b\'s but for x labels left out (and, v2.4d, density labels in units of a power '
      'of ten, written out for the comparison), no error' % (len(calls), nscr),
      OLD is not None and same == 2 * len(calls), (diff[:2], errs[:2]))
check('R2 the x labels left out in those ordinary runs are exactly the ones that would touch the "x" caption or '
      'the label drawn before them (v2.4b printed them overlapping); %d left out, e.g. %s'
      % (len(set(d[:2] for d in dropped)), sorted(set(d[:2] for d in dropped))[:4]),
      len(model_ok) == 2 * len(calls) and all(model_ok), (model_ok, sorted(set(dropped))[:6]))

# ===================================================================== M
print('=== M. the findings (1 Nov 2026; each check fails on v2.4b)')
TYPES = 'Norm3 takes three numbers: Norm3(μ, σ, x₀)'
BIG = 'A number you typed has more than 50 digits: too large to work with.'
WIDE = 'σ can be at most 1E10: a larger σ needs density labels with more decimals than the calculator prints.'
NARROW = 'σ is too small next to μ for the calculator\'s 12 digits. Use a larger σ or a μ nearer 0.'
cases = [('Norm3({1,2},1,0)', TYPES), ('Norm3(0,{1},0)', TYPES), ('Norm3(0,1,{0,1})', TYPES),
         ('Norm3(1E300,1,0)', BIG), ('Norm3(0,1E300,0)', BIG), ('Norm3(0,1,-1E60)', BIG),
         ('Norm3(0,1E12,0)', WIDE), ('Norm3(0,1E-300,0)', NARROW), ('Norm3(1E40,1,1E40)', NARROW)]
for c, want in cases:
    hn, rn, en = run(c)
    ho, ro, eo = run(c, (), OLD) if OLD else (None, None, 'no v2.4b')
    check('M1 %s: "%s", nothing drawn; v2.4b: %s' % (c, want[:40] + '...', eo or (ro or '')[:40]),
          en is None and rn == want and not hn.screens and OLD is not None and (eo is not None or ro != want),
          (en, rn, eo, ro))


def tick_loop_12(mu, sd):
    """v2.4b's x tick loop in 12-digit decimals: does xv := xv + stp stop moving?"""
    c = Context(prec=12, rounding=ROUND_HALF_UP)
    mu, sd = Decimal(mu), Decimal(sd)
    xmin, xmax = c.subtract(mu, c.multiply(4, sd)), c.add(mu, c.multiply(4, sd))
    raw = float(xmax - xmin) / 6
    import math
    e = math.floor(math.log10(raw))
    f = raw / 10 ** e
    stp = Decimal(str((1 if f < 1.5 else 2 if f < 3 else 5 if f < 7 else 10) * 10 ** e))
    xv = c.multiply(c.divide(xmin, stp).to_integral_value(rounding='ROUND_CEILING'), stp)
    for k in range(200):
        if xv > c.add(xmax, c.divide(stp, 1000)):
            return 'ends'
        nxt = c.add(xv, stp)
        if nxt == xv:
            return 'stuck'
        xv = nxt
    return 'still going'


hn, rn, en = run('Norm3(1E9,0.001,1E9)')
ho, ro, eo = run('Norm3(1E9,0.001,1E9)', (), OLD) if OLD else (None, None, 'no v2.4b')
check('M1 Norm3(1E9,0.001,1E9): "%s"; v2.4b drew in the harness (16 digits), and its tick loop in 12 digits is %s '
      '(SampDist v2.3d\'s same loop never ended on the Virtual Calculator)' % (NARROW[:30] + '...',
                                                                             tick_loop_12('1E9', '0.001')),
      en is None and rn == NARROW and OLD is not None and eo is None and ro != NARROW
      and tick_loop_12('1E9', '0.001') == 'stuck', (en, rn, eo))

acc = []
for c, keys in (('Norm3(0,0.000000001,0)', KEYS), ('Norm3(1E9,10,1E9)', KEYS), ('Norm3(0,1E10,0)', KEYS),
                ('Norm3(9.9E17,1E10,9.9E17)', KEYS), ('Norm3(0,1,9.9E49)', ['Plus', 'Zero'])):
    hn, rn, en = run(c, keys)
    acc.append((c, en, (rn or '')[:30]))
for c in ('Norm3(1E9,10,1E9)', 'Norm3(0,0.000000001,0)', 'Norm3(0,1E10,0)'):
    run(c, KEYS, OLD) if OLD else None
check('M2 the ends of what is accepted draw, with every key, and no error (STRING refusing 13 decimals as on the '
      'Prime): %s' % [(a[0], a[1]) for a in acc], all(a[1] is None and a[2].startswith('Norm3: N(') for a in acc), acc)

UP12 = ['Up'] * 20
hn, rn, en = run('Norm3(0,1E10,0)', UP12)
ho, ro, eo = run('Norm3(0,1E10,0)', UP12, OLD) if OLD else (None, None, 'no v2.4b')
check('M3 sigma+ twenty times from 1E10: sigma stays 1E10 (%s), no error; v2.4b: %s' % (g(hn, 'EP_NORM_SD'), eo),
      en is None and g(hn, 'EP_NORM_SD') == 1E10 and OLD is not None and eo is not None and 'Invalid input' in eo,
      (en, g(hn, 'EP_NORM_SD'), eo))
DOWN20 = ['Down'] * 20
hn, rn, en = run('Norm3(1E9,10,1E9)', DOWN20)
ho, ro, eo = run('Norm3(1E9,10,1E9)', DOWN20, OLD) if OLD else (None, None, 'no v2.4b')
check('M3 sigma- twenty times at mu = 1E9, sigma = 10: sigma stays 10 (|mu|/100,000,000); v2.4b went to %.4g' % (
    g(ho, 'EP_NORM_SD') if ho and not eo else -1), en is None and g(hn, 'EP_NORM_SD') == 10.0 and OLD is not None
      and (eo is not None or g(ho, 'EP_NORM_SD') < 1), (en, g(hn, 'EP_NORM_SD'), eo))
hn, rn, en = run('Norm3(0,0.00001,0)', ['Down'])
ho, ro, eo = run('Norm3(0,0.00001,0)', ['Down'], OLD) if OLD else (None, None, 'no v2.4b')
check('M3 sigma- once from a typed 0.00001: sigma stays 0.00001 (%s); v2.4b raised it to %s' % (
    g(hn, 'EP_NORM_SD'), g(ho, 'EP_NORM_SD') if ho else '-'),
      en is None and g(hn, 'EP_NORM_SD') == 0.00001 and OLD is not None and g(ho, 'EP_NORM_SD') == 0.0001,
      (en, g(hn, 'EP_NORM_SD'), g(ho, 'EP_NORM_SD') if ho else None))
hn, rn, en = run('Norm3(0,1,0)', ['Down'] * 3 + ['Up'] * 2)
ho, ro, eo = run('Norm3(0,1,0)', ['Down'] * 3 + ['Up'] * 2, OLD) if OLD else (None, None, 'no v2.4b')
check('M3 ordinary sigma keys unchanged: Norm3(0,1,0), sigma- three times and sigma+ twice: sigma %.6g, as v2.4b\'s' % (
    g(hn, 'EP_NORM_SD') or -1), en is None and OLD is not None and abs(g(hn, 'EP_NORM_SD') - 0.8) < 1e-12
      and g(ho, 'EP_NORM_SD') == g(hn, 'EP_NORM_SD'), (g(hn, 'EP_NORM_SD'), g(ho, 'EP_NORM_SD') if ho else None))

lines = [len(textwrap.wrap(m, 32)) for m in (TYPES, BIG, WIDE, NARROW)]
check('M4 every new sentence within 4 lines at 32 characters (they return to Home, where a line holds more): %s'
      % lines, max(lines) <= 4, lines)

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
check('G1 only Norm3, n3_fmtp, n3_Help and (v2.4d) the new n3_YWd differ from v2.4b, code for code: %s' % changed,
      changed == ['Norm3', 'n3_Help', 'n3_YWd', 'n3_fmtp'], changed)
code = [ln.split('//')[0] for ln in SRC.split('\n')]
ne_o = [ln.split('//')[0].strip() for ln in OSRC.split('\n') if '!=' in ln.split('//')[0]]
check('G2 no "!=" in the code (on the Prime a factorial and a test); v2.4b had %d: %s' % (len(ne_o), ne_o[:1]),
      not any('!=' in c for c in code) and len(ne_o) == 1, [c for c in code if '!=' in c])
fp = [ln.strip() for ln in upto_end(bn.get('n3_fmtp', '')).split('\n') if ln.strip() and not ln.strip().startswith('//')]
fpo = [ln.strip() for ln in upto_end(bo.get('n3_fmtp', '')).split('\n') if ln.strip() and not ln.strip().startswith('//')]
check('G2 n3_fmtp differs from v2.4b in its one line, "pv != 0" written "pv <> 0"',
      [a for a in fp if a not in fpo] == ['IF pv <> 0 AND ABS(pv) < thr THEN']
      and [a for a in fpo if a not in fp] == ['IF pv != 0 AND ABS(pv) < thr THEN'], (fp, fpo))
nu = sorted(set(c for ln in code for c in ln if ord(c) > 127))
nuo = sorted(set(c for ln in OSRC.split('\n') for c in ln.split('//')[0] if ord(c) > 127))
check('G3 no new non-ASCII character in the code outside strings (the house rule): code glyphs %s, v2.4b\'s %s' % (
    ''.join(nu), ''.join(nuo)), set(nu) <= set(nuo) | set('μσ'), (nu, nuo))

# ===================================================================== D
print('=== D. layout (text_overlap_v1 over every screen above)')
rep = OV.report()
tag = [t for t in rep if t.startswith(os.path.splitext(os.path.basename(PROG))[0])]
f = rep[tag[0]] if tag else None
firm = []
if f:
    firm += [('overlap', c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [('straddle', x['text'], x['edge']) for x in f['straddles'] if x['firm']]
    firm += [('overrun', x['text'], x.get('right')) for x in f['overruns'] if x['firm']]
    print('   screens: %d distinct of %d' % (f['screens_distinct'], f['screens_total']))
tago = [t for t in rep if t.startswith('Norm3_v2.4b')]
fo = rep[tago[0]] if tago else None
firm_o = [('overlap', c['a'], c['b']) for c in fo['collisions'] if c['severity'] == 'overlap' and c['firm']] if fo else []
check('D1 no firm overlap, straddle or overrun on any v2.4d screen drawn, the ends of what is accepted included '
      '(v2.4b, on its own runs: %d, %s)' % (len(firm_o), sorted(set(str(x[1]) for x in firm_o))[:3]),
      bool(tag) and not firm, firm[:6])

def yw(s):
    """a label's width as the programs estimate it: 5.5 px a character, 3 px for the point (n3_YWd, ne_YWd, st_LWd;
    "0.03" is 20 px wide on the Virtual Calculator)"""
    return 5.5 * (len(s) - 1) + 3 if '.' in s else 5.5 * len(s)


def yval(s):
    return float(s.replace('ᴇ', 'e').replace('−', '-').replace('×', '').replace(',', ''))


def close(a, b):
    return abs(a - b) <= 1E-9 * max(abs(a), abs(b), 1E-300)

# ===================================================================== Y
print('=== Y. v2.4d: density labels written in units of a power of ten when they do not fit left of the axis')
PREV = OLD     # v2.4b: v2.4c drew its density labels exactly as v2.4b did


def ylabs(h):
    """the last screen's density labels (font 1 at x 1) and the power-of-ten note at the top of the axis"""
    scr = [s_ for s_ in h.screens if any(t.x == 1 for t in s_.texts)]
    if not scr:
        return [], None
    labs = [t.text for t in scr[-1].texts if t.x == 1]
    note = [t.text for t in scr[-1].texts if t.text.startswith('×')]
    return labs, (note[0] if note else None)


SIGS = [10.0 ** k for k in range(-9, 11)] + [0.0002, 0.003, 0.5, 15.0, 50.0, 100.0, 250.0, 500.0, 2000.0]
wide_n, scaled, bad, old_wide = 0, [], [], []
for sg in SIGS:
    hn_, _, en_ = run('Norm3(0,%r,0)' % sg)
    ho_, _, eo_ = run('Norm3(0,%r,0)' % sg, path=PREV) if PREV else (None, None, 'no v2.4b')
    ln_, nt = ylabs(hn_)
    lo_, _ = ylabs(ho_) if ho_ else ([], None)
    ow = [x for x in lo_ if yw(x) > 20]
    if ow:
        old_wide.append((sg, ow[-1]))
    ok = not en_ and not eo_ and all(yw(x) <= 20 for x in ln_) and len(ln_) == len(lo_)
    if nt:
        k = yval(nt)
        ok = ok and bool(ow) and all(close(yval(a) * k, yval(b)) for a, b in zip(ln_, lo_))
        scaled.append((sg, nt, ln_[-1] if ln_ else ''))
    else:
        ok = ok and not ow and ln_ == lo_
    if not ok:
        bad.append((sg, ln_, nt, lo_, en_, eo_))
check('Y1 Norm3(0, sigma, 0) at %d sigmas from 1E-9 to 1E10: every density label at most 20 px wide (the 24 px left '
      'of the axis); where v2.4b and v2.4c had a wider one (%d sigmas) the labels are their values in units of the '
      'power printed at the top of the axis, e.g. %s; elsewhere exactly theirs' % (len(SIGS), len(scaled), scaled[:3]),
      PREV is not None and not bad and len(scaled) > 0, bad[:3])
check('Y2 v2.4b drew labels wider than the margin at %d of those sigmas, sigma = 1000 among them (v2.4c, the '
      'same: "0.0005" over the axis on the Virtual Calculator), e.g. %s' % (len(old_wide), old_wide[:3]),
      any(sg == 1000.0 for sg, _ in old_wide) and len(old_wide) == len(scaled), old_wide)

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
