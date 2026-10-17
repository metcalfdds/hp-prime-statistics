#!/usr/bin/env python3
"""verify_ChiTable_beta3b.py -- ChiTable beta 3b (17 Oct 2026): two CHOOSE lines shortened (the emulator cut
"Death penalty x defendant's rac[e]" and "N / 10: every count divided by [10]" at the box's edge).
Built from verify_ChiTable_beta3a.py; every check is kept and now runs in harness v3c.  New checks (3b):
  every CHOOSE line the program can show is at most 30 characters (the source, every list, and every
  dialog seen in the runs); the two shortened menus still do what they did (the examples load the
  same tables, N / 10 restores the counts); beta 3b against beta 3a: only csExamples and csResMenu differ.
(The beta 3a description follows; "v3b" there now means v3c.)

verify_ChiTable_beta3b.py -- checks for ChiTable beta 3a (17 Oct 2026): the CAS call form that
CASProbe beta 1b found on the emulator.  Built from verify_ChiTable_beta3.py: every check is kept and
run in harness v3b, which models the calculator's CAS (CAS of a variable unevaluated, the Prime's
printing, a CAS string as a PPL string).  Changed or new checks are marked "3a".

  A. Giac (desktop 1.9, icas): the traps the templates avoid -- a sum over a symbolic index
     (Giac tries to solve Gamma equations) against sum(seq(...)) with whole-number bounds.
  B. The CAS text THE PROGRAM BUILDS, captured from the run harness (ppl_run_v3, cas='giac')
     for representative and edge tables (ties, zero cells, the smallest table, symmetric tables,
     large N), answered by Giac, and compared with Python fractions and SciPy:
       Fisher p   == the exact-integer rule (a table counts when 10^7 w <= (10^7+1) w_obs, the
                     same 1.0000001 tolerance as csFisher, R and SciPy), as a Fraction; its float
                     == scipy.stats.fisher_exact == csFisher's own decimal (csFish);
       the runs of a the program sums == the exact-integer decision (float decision == exact);
       chi2       == N(ad-bc)^2/(r1 r2 c1 c2) == sum (O-E)^2/E as Fractions; float == SciPy's
                     chi2_contingency(correction=False) == csCompute's csX2;
       ad - bc, r1 r2 c1 c2, the ways that count and C(N, c1) as exact integers;
       the "too big" guard: csXDg (digits of C(N, c1), estimated by PPL) against len(str(comb)).
  C. 300 random 2 x 2 and 150 random 2 x 3 / 3 x 2 tables, the same comparisons.
  D. End to end in the harness, cas='giac' AND cas='fail': the lady tasting tea typed in the grid
     (Values form, Run), results pages 6 and 7, the Fisher plot; example 2 (long fractions,
     digit counts), x10 N (the "too big" path), N / 10; examples 3 and 4 (2 x 3, 3 x 2).  The
     fallback shows the decimal and the "decimal" badge, with no runtime error.
  E. The fence: the CAS only on page entry -- a call-graph check (no CAS reachable from the bar
     drag, the curve drag, the morph or any frame routine), the cache (pages turned back and
     forth ask nothing new; a bar drag asks nothing; a changed table asks once), and the device-
     tested routines byte-identical to beta 2 (csFishW moved but unchanged).

  G. 3a: beta 3 in harness v3b (its csCas returns its own text: no fraction anywhere), and beta 3a
     against beta 3 (only csCas differs).

Run:  python3 verify_ChiTable_beta3a.py      (needs SciPy and Giac's icas; reads files only)
"""
import sys, re, math, random, subprocess, tempfile, os
from fractions import Fraction as Fr
import numpy as np
from scipy import stats

sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3c import Harness  # noqa: E402

SRC = '/home/claude/work/out/ChiTable_beta3b.txt'
B3A = '/home/claude/work/out/ChiTable_beta3a.txt'
BETA3 = '/home/claude/work/out/ChiTable_beta3.txt'
OLD = '/home/claude/work/out/ChiTable_beta2.txt'
FAILS = []
NPASS = [0]


def check(cond, msg):
    if cond:
        NPASS[0] += 1
    else:
        FAILS.append(msg)
        print('FAIL ' + msg)
    return cond


def say(msg):
    print(msg)


def giac(lines):
    """Run expressions through icas; return (answers, warnings)."""
    with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
        f.write(';\n'.join(lines) + ';\n')
        name = f.name
    cp = subprocess.run(['icas', name], capture_output=True, text=True)
    out = cp.stdout + '\n' + cp.stderr          # Giac's warnings go to stderr
    os.unlink(name)
    ans, warn = [], []
    for ln in out.split('\n'):
        t = ln.strip()
        if not t or t.startswith('// ') or t.startswith('Added '):
            continue
        if t.startswith('Warning') or t.startswith('Unable'):
            warn.append(t)
            continue
        ans.append(t.rstrip(','))
    return ans, warn


# ---------------------------------------------------------------- exact arithmetic
def margins(o, nr, nc):
    R = [sum(o[r * nc:(r + 1) * nc]) for r in range(nr)]
    C = [sum(o[c::nc]) for c in range(nc)]
    return R, C, sum(o)


def w2(a, r1, r2, c1):
    return math.comb(r1, a) * math.comb(r2, c1 - a)


def fisher_exact_frac(a, b, c, d):
    """Two-sided p by the exact-integer form of csFisher's rule: a table counts when its weight
    is at most the observed weight times 1.0000001, i.e. 10^7 w <= (10^7 + 1) w_obs."""
    r1, r2, c1 = a + b, c + d, a + c
    lo, hi = max(0, c1 - r2), min(r1, c1)
    wo = w2(a, r1, r2, c1)
    inc = [x for x in range(lo, hi + 1) if 10 ** 7 * w2(x, r1, r2, c1) <= (10 ** 7 + 1) * wo]
    s = sum(w2(x, r1, r2, c1) for x in inc)
    return Fr(s, math.comb(r1 + r2, c1)), inc, s


def runs_of(seq):
    out, st = [], None
    for i, x in enumerate(seq):
        if st is None:
            st = x
        if i == len(seq) - 1 or seq[i + 1] != x + 1:
            out.append((st, x))
            st = None
    return out


def chi2_exact(o, nr, nc):
    R, C, N = margins(o, nr, nc)
    s = Fr(0)
    for r in range(nr):
        for c in range(nc):
            E = Fr(R[r] * C[c], N)
            s += (o[r * nc + c] - E) ** 2 / E
    return s


def cs_fishw_float(a, b, c, d):
    """Python mirror of csFishW (float ratios from the mode) -- the PPL decision."""
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2
    lo, hi = max(0, c1 - r2), min(r1, c1)
    m = min(max(math.floor((r1 + 1) * (c1 + 1) / (n + 2)), lo), hi)
    W = [0.0] * (hi - lo + 1)
    W[m - lo] = 1.0
    w, k = 1.0, m
    while k < hi:
        w = w * (r1 - k) * (c1 - k) / ((k + 1) * (r2 - c1 + k + 1)); W[k - lo + 1] = w; k += 1
    w, k = 1.0, m
    while k > lo:
        w = w * k * (r2 - c1 + k) / ((r1 - k + 1) * (c1 - k + 1)); W[k - lo - 1] = w; k -= 1
    t = sum(W)
    return lo, [x / t for x in W]


# ---------------------------------------------------------------- the harness
def H(cas='giac'):
    h = Harness(SRC, cas=cas, seed=1)
    h.call('csInit')
    return h


def load(h, nr, nc, o):
    h.globals_['csNR'] = float(nr)
    h.globals_['csNC'] = float(nc)
    h.globals_['csO'] = [float(x) for x in o]
    h.call('csCompute')


def ask(h, nr, nc, o):
    """Load a table, ask for every exact answer once (csXEnsure(1)), return the cache and calls."""
    load(h, nr, nc, o)
    n0 = len(h.cas_calls)
    h.call('csXEnsure', 1)
    g = h.globals_
    keys = ['csXFSt', 'csXFr', 'csXSum', 'csXX2', 'csXAd', 'csXPr', 'csXS', 'csXT', 'csXDg',
            'csFish', 'csX2', 'csCasOK']
    res = {k: g[k] for k in keys}
    res['calls'] = h.cas_calls[n0:]
    return res


RUNPAT = re.compile(r'sum\(seq\(comb\((\d+),csj\)\*comb\((\d+),(\d+)-csj\),csj,(\d+),(\d+)\)\)')


def check_2x2(h, o, tag, verbose=False):
    a, b, c, d = o
    r = ask(h, 2, 2, o)
    R, C, N = margins(o, 2, 2)
    fx, inc, s = fisher_exact_frac(a, b, c, d)
    sp = stats.fisher_exact([[a, b], [c, d]], alternative='two-sided')[1]
    ok = True
    # the PPL decision (float, csFishW + 1.0000001) == the exact-integer decision
    lo, W = cs_fishw_float(a, b, c, d)
    wobs = W[a - lo]
    fl_inc = [lo + i for i, x in enumerate(W) if x <= wobs * 1.0000001]
    ok &= check(fl_inc == inc, '%s: float decision %s != exact %s' % (tag, fl_inc, inc))
    dg_true = len(str(math.comb(N, C[0])))
    ok &= check(abs(r['csXDg'] - dg_true) <= 1, '%s: digits estimate %s vs %d' % (tag, r['csXDg'], dg_true))
    if r['csXDg'] > 100:
        ok &= check(r['csXFSt'] == 3, '%s: state %s, want 3 (too big)' % (tag, r['csXFSt']))
        ok &= check(not any('comb(%d,' % N in x[0] for x in r['calls']), '%s: a too-big table was sent to the CAS' % tag)
    else:
        ok &= check(r['csXFSt'] == 1, '%s: Fisher state %s, want 1' % (tag, r['csXFSt']))
        ok &= check(r['csXFr'] == str(fx), '%s: Fisher %s != %s' % (tag, r['csXFr'], fx))
        # the runs in the program's own template == the exact runs
        tmpl = [x[0] for x in r['calls'] if x[0].startswith('string((sum(seq(')][0]   # 3a: string(...)
        got = [(int(m.group(4)), int(m.group(5))) for m in RUNPAT.finditer(tmpl)]
        ok &= check(got == runs_of(inc), '%s: template runs %s != %s' % (tag, got, runs_of(inc)))
        ok &= check(all(int(m.group(1)) == R[0] and int(m.group(2)) == R[1] and int(m.group(3)) == C[0]
                        for m in RUNPAT.finditer(tmpl)), '%s: template margins' % tag)
        ok &= check(len(got) <= 2, '%s: more than two runs (%d)' % (tag, len(got)))
        ok &= check(r['csXS'] == str(s), '%s: ways %s != %s' % (tag, r['csXS'], s))
        ok &= check(r['csXT'] == str(math.comb(N, C[0])), '%s: C(N,c1) %s' % (tag, r['csXT']))
        ok &= check(abs(float(fx) - sp) <= 1e-9 * max(sp, 1e-300) + 1e-15, '%s: Fisher float %r vs scipy %r' % (tag, float(fx), sp))
    ok &= check(abs(r['csFish'] - sp) <= 1e-9 * max(sp, 1e-12), '%s: csFish %r vs scipy %r' % (tag, r['csFish'], sp))
    # chi2, exactly
    x2 = Fr(N * (a * d - b * c) ** 2, R[0] * R[1] * C[0] * C[1])
    ok &= check(x2 == chi2_exact(o, 2, 2), '%s: shortcut != sum form' % tag)
    ok &= check(r['csXX2'] == str(x2), '%s: chi2 %s != %s' % (tag, r['csXX2'], x2))
    ok &= check(r['csXAd'] == str(a * d - b * c), '%s: ad-bc %s' % (tag, r['csXAd']))
    ok &= check(r['csXPr'] == str(R[0] * R[1] * C[0] * C[1]), '%s: product %s' % (tag, r['csXPr']))
    spx = stats.chi2_contingency(np.array([[a, b], [c, d]]), correction=False)[0]
    ok &= check(abs(float(x2) - spx) <= 1e-9 * max(spx, 1) and abs(r['csX2'] - spx) <= 1e-9 * max(spx, 1),
                '%s: chi2 float %r / csX2 %r vs scipy %r' % (tag, float(x2), r['csX2'], spx))
    if verbose:
        say('  %-24s Fisher %-28s (scipy %.6g)  chi2 %s = %.4f   runs %s   calls %d   digits %d' % (
            tag, (r['csXFr'] if r['csXFSt'] == 1 else 'state %d' % r['csXFSt'])[:28], sp, str(x2)[:24],
            float(x2), runs_of(inc), len(r['calls']), dg_true))
    return r


def check_rxc(h, nr, nc, o, tag, verbose=False):
    r = ask(h, nr, nc, o)
    ex = chi2_exact(o, nr, nc)
    spx = stats.chi2_contingency(np.array(o).reshape(nr, nc), correction=False)[0]
    check(r['csXX2'] == str(ex), '%s: chi2 %s != %s' % (tag, r['csXX2'], ex))
    check(abs(float(ex) - spx) <= 1e-9 * max(spx, 1), '%s: chi2 float vs scipy' % tag)
    check(abs(r['csX2'] - spx) <= 1e-9 * max(spx, 1), '%s: csX2 vs scipy' % tag)
    check(r['csXFSt'] == 4, '%s: Fisher state %s, want 4 (not a 2x2)' % (tag, r['csXFSt']))
    check(len(r['calls']) == 1, '%s: %d CAS calls, want 1' % (tag, len(r['calls'])))
    if verbose:
        say('  %-24s chi2 %s = %.4f (scipy %.4f), template %d chars' % (tag, ex, float(ex), spx, len(r['calls'][0][0])))
    return r


# ================================================================ A. Giac's traps
say('A. Giac 1.9 (desktop icas): the templates avoid the symbolic-sum trap')
ans, warn = giac(['sum(comb(4,csj)*comb(4,4-csj),csj,0,1)+sum(comb(4,csj)*comb(4,4-csj),csj,3,4)'])
check(ans == ['34'] and len(warn) > 0, 'plain sum: expected 34 with Gamma warnings, got %s %s' % (ans, warn))
say('  sum(comb(..),csj,0,1)+...      -> %s, with %d warning lines: "%s"' % (ans, len(warn), warn[0] if warn else ''))
ans, warn = giac(['sum(seq(comb(4,csj)*comb(4,4-csj),csj,0,1))+sum(seq(comb(4,csj)*comb(4,4-csj),csj,3,4))'])
check(ans == ['34'] and not warn, 'seq form: expected 34 and no warnings, got %s %s' % (ans, warn))
say('  sum(seq(comb(..),csj,0,1))+... -> %s, %d warnings  (the form the program uses)' % (ans, len(warn)))
ans, warn = giac(['674*(64*155-451*4)^2/(515*159*68*606)', 'comb(8,4)', '(762-1557*1246/2757)^2/(1557*1246/2757)'])
say('  N(ad-bc)^2/(r1 r2 c1 c2), ex. 2  -> %s;  comb(8,4) -> %s;  one r x c term -> %s' % tuple(ans))
check(ans[0] == '5549501668/421789635', 'ex 2 chi2 fraction')

# ================================================================ B. representative and edge tables
say('\nB. the program\'s own CAS text (harness, cas=giac) against fractions and SciPy')
h = H('giac')
EDGE = [
    ([3, 1, 1, 3], 'lady tasting tea'),
    ([1, 3, 3, 1], 'tea, other tail'),
    ([4, 0, 0, 4], 'tea, all correct'),
    ([2, 2, 2, 2], 'p = 1 (the mode)'),
    ([1, 0, 0, 1], 'smallest, a tie'),
    ([5, 0, 3, 7], 'zero cell'),
    ([0, 5, 7, 3], 'zero cell, a = 0'),
    ([6, 2, 2, 6], 'symmetric ties'),
    ([10, 0, 0, 10], 'extreme'),
    ([0, 10, 10, 0], 'extreme, a = 0'),
    ([1, 9, 9, 1], 'near extreme'),
    ([12, 5, 9, 7], 'ordinary'),
    ([2, 7, 8, 2], 'ordinary 2'),
    ([53, 430, 15, 176], 'example 1'),
    ([64, 451, 4, 155], 'example 2'),
    ([30, 10, 10, 30], 'tea x 10'),
    ([5, 995, 3, 997], 'large N, few cases'),
    ([640, 4510, 40, 1550], 'example 2 x 10'),
]
for o, tag in EDGE:
    check_2x2(h, o, tag, verbose=True)
r = ask(h, 2, 2, [3, 1, 1, 3])
check(r['csXFr'] == '17/35', 'the brief\'s example: tea is 17/35')
say('  tea: csXPText(33) = "%s"' % h.call('csXPText', 33))
check(h.call('csXPText', 33) == 'p = 17/35 = 0.4857', 'tea display string')
ask(h, 2, 2, [64, 451, 4, 155])
t = h.call('csXPText', 33)
fx, _, _ = fisher_exact_frac(64, 451, 4, 155)
nd = len(str(fx.numerator)) + len(str(fx.denominator))
say('  example 2: csXPText(33) = "%s"  (the fraction has %d + %d = %d digits)' % (
    t, len(str(fx.numerator)), len(str(fx.denominator)), nd))
check(t == 'p = 0.0001 (%d-digit fraction)' % nd, 'example 2 digit count')
t = h.call('csXX2Txt', 44)
check(t == '= 5549501668/421789635 = 13.157', 'example 2 chi2 line: %s' % t)
say('  example 2: csXX2Txt(44) = "%s"' % t)

say('  r x c:')
check_rxc(h, 2, 3, [762, 327, 468, 484, 239, 477], 'example 3 (2 x 3)', verbose=True)
check_rxc(h, 3, 2, [762, 484, 327, 239, 468, 477], 'example 4 (3 x 2)', verbose=True)
check_rxc(h, 2, 3, [1, 2, 3, 4, 5, 6], 'small 2 x 3', verbose=True)
check_rxc(h, 3, 2, [10, 0, 5, 7, 0, 3], 'zero cells 3 x 2', verbose=True)
check_rxc(h, 2, 3, [7620, 3270, 4680, 4840, 2390, 4770], 'example 3 x 10', verbose=True)
check(ask(h, 2, 3, [762, 327, 468, 484, 239, 477])['csXX2'] == ask(h, 3, 2, [762, 484, 327, 239, 468, 477])['csXX2'],
      'a transposed table gives the same exact chi2')

# ================================================================ C. random tables
say('\nC. random tables')
rng = random.Random(20261016)
n2 = 0
while n2 < 300:
    o = [rng.randint(0, 40) for _ in range(4)]
    if rng.random() < 0.25:
        o[rng.randrange(4)] = 0
    R, C, N = margins(o, 2, 2)
    if min(R + C) == 0:
        continue
    check_2x2(h, o, 'random %s' % o)
    n2 += 1
nrc = 0
while nrc < 150:
    nr, nc = rng.choice([(2, 3), (3, 2)])
    o = [rng.randint(0, 60) for _ in range(6)]
    R, C, N = margins(o, nr, nc)
    if min(R + C) == 0:
        continue
    check_rxc(h, nr, nc, o, 'random %dx%d %s' % (nr, nc, o))
    nrc += 1
say('  300 random 2 x 2 and 150 random 2 x 3 / 3 x 2 tables done (failures, if any, listed above)')

# ================================================================ D. end to end
say('\nD. end to end in the harness')


def pages(hh, func):
    return [p for p in hh.pages if p.func == func]


def has(p, s):
    return any(s in l for l in p.lines())


def tea_run(mode):
    hh = Harness(SRC, cas=mode, seed=2, strict=False)
    hh.choose(1)                                   # New table: 2 x 2
    hh.tap(80, 230)                                # Values soft key
    hh.answer({'a1': 3, 'a2': 1, 'a3': 1, 'a4': 3})
    hh.tap(300, 230)                               # Run
    hh.press(*(['Right'] * 6))                     # to page 7 (Right stops at the last)
    hh.press('Esc')                                # results -> main menu
    hh.choose(10)                                  # Plot: Fisher exact (2 x 2)
    hh.press('Esc')
    hh.choose(14)                                  # Quit
    ret = hh.call('ChiTable')
    return hh, ret


for mode in ('giac', 'fail'):
    hh, ret = tea_run(mode)
    p6, p7, pf = pages(hh, 'csPage2x2'), pages(hh, 'csPageExact'), pages(hh, 'csFishDraw')
    ok = check(p6 and p7 and pf, '%s: tea pages missing (%d %d %d)' % (mode, len(p6), len(p7), len(pf)))
    if not ok:
        continue
    p6, p7, pf = p6[-1], p7[-1], pf[-1]
    say('  [%s] tea typed in the grid, Run, pages 6 and 7, the Fisher plot; Quit returned "%s"' % (mode, ret))
    check(hh.error is None, '%s: runtime error %s' % (mode, hh.error))
    check(ret.startswith('ChiTable: '), '%s: summary line' % mode)
    if mode == 'giac':
        for s in ('p = 17/35 = 0.4857', 'exact (CAS)'):
            check(has(p6, s), 'giac page 6 lacks "%s"' % s)
        for s in ('= 8 × (3 × 3 - 1 × 1)²', '= 8 × 8² / 256', '= 2 = 2.000', 'C(4, a) × C(4, 4 - a) / C(8, 4)',
                  '34 of the 70 equally likely ways', 'p = 34/70 = 17/35 = 0.4857', '7/7'):
            check(has(p7, s), 'giac page 7 lacks "%s"' % s)
        check(has(pf, 'red + magenta: p = 17/35 = 0.4857') and has(pf, 'exact (CAS)'), 'giac Fisher plot line')
        check(len(hh.cas_calls) == 6, 'giac: %d CAS calls for the tea session, want 6 (1 + 5, the plot cached)' % len(hh.cas_calls))
    else:
        for s in ('p = 0.4857', 'decimal'):
            check(has(p6, s), 'fail page 6 lacks "%s"' % s)
        check(not has(p6, '17/35'), 'fail page 6 shows a fraction')
        for s in ('= 2.000', '(the CAS did not answer: the decimal only)', 'decimal'):
            check(has(p7, s), 'fail page 7 lacks "%s"' % s)
        check(has(pf, 'red + magenta: p = 0.4857') and has(pf, 'decimal'), 'fail Fisher plot line')
        check(len(hh.cas_calls) == 4, 'fail: %d CAS attempts, want 4 (one per table, then cached)' % len(hh.cas_calls))
    for l in p7.lines():
        say('      p7| ' + l)
    say('      p6| ' + ' / '.join(l for l in p6.lines() if 'Fisher' in l or l.startswith('p ') or l in ('exact (CAS)', 'decimal')))
    say('      fp| ' + ' / '.join(l for l in pf.lines() if 'magenta' in l or l in ('exact (CAS)', 'decimal') or 'margins' in l))
    say('      CAS calls: %d' % len(hh.cas_calls))

# 3a: every answer ARRIVES IN QUOTES now -- the CAS is asked for string(...), the answer is a PPL
# string and STRING() of it adds a pair of quotes (CASProbe beta 1b T12) -- and csCas drops them.
# (beta 3's test added a second pair by hand; in v3b the quotes are the normal path.)
hq, retq = tea_run('giac')
check(hq.error is None, 'quoted answers: runtime error %s' % hq.error)
check(all(c[0].startswith('string(') and c[1].startswith('"') for c in hq.cas_calls),
      '3a: every CAS text asks for string(...), every answer is quoted')
check(not hq.cas_vars and not any('non-literal' in w for w in hq.warnings),
      '3a: no CAS variable assigned, no CAS call of a variable')
check(not any('"' in l for p in hq.pages for l in p.lines() if p.func in ('csPage2x2', 'csPageExact', 'csFishDraw')),
      '3a: no quote mark reaches the exact pages')
pq6, pq7 = pages(hq, 'csPage2x2')[-1], pages(hq, 'csPageExact')[-1]
check(has(pq6, 'p = 17/35 = 0.4857') and has(pq6, 'exact (CAS)'), 'quoted answers: page 6 shows 17/35 (quotes dropped)')
check(has(pq7, 'p = 34/70 = 17/35 = 0.4857') and has(pq7, '= 2 = 2.000'), 'quoted answers: page 7')
say('  [quoted] every answer arrived as \'"..."\' (e.g. %s): csCas dropped the quotes; page 6 "%s"' % (
    hq.cas_calls[0][1], [l for l in pq6.lines() if l.startswith('p = ')][0]))

# example 2: long fractions; then x10 N (too big), N / 10, the bars drag, the cache
for mode in ('giac', 'fail'):
    hh = Harness(SRC, cas=mode, seed=3, strict=False)
    hh.choose(12, 2)                               # Examples -> victim's race
    hh.press(*(['Right'] * 6))                     # page 7
    hh.press('Left', 'Right', 'Left', 'Right')     # back and forth: no new CAS calls
    hh.tap(300, 230)                               # Menu soft key -> Results menu
    hh.choose(2)                                   # x10 N
    hh.press('Enter')                              # leave the before/after page
    hh.tap(300, 230); hh.choose(3)                 # N / 10: the table is back
    hh.press('Enter')                              # leave the before/after page
    hh.press('Esc')                                # results -> menu (Examples returns)
    hh.choose(14)
    ret = hh.call('ChiTable')
    check(hh.error is None, '%s ex2: runtime error %s' % (mode, hh.error))
    p7s = pages(hh, 'csPageExact')
    p6s = pages(hh, 'csPage2x2')
    say('  [%s] example 2: %d frames of page 7, %d of page 6; %d CAS calls' % (mode, len(p7s), len(p6s), len(hh.cas_calls)))
    calls = [c[0] for c in hh.cas_calls]
    if mode == 'giac':
        first = p7s[0]
        for s in ('= 5549501668/421789635 = 13.157', 'their ways, over all C(674, 68) ways:', '-digit fraction)'):
            check(has(first, s), 'giac ex 2 page 7 lacks "%s"' % s)
        big = [p for p in p7s if has(p, 'C(6740, 680) has about')]
        check(len(big) > 0, 'giac x10: page 7 lacks the too-big line')
        if big:
            say('      x10 N: ' + [l for l in big[0].lines() if 'about' in l][0].strip())
            check(has(big[0], '= 131.571') or has(big[0], '131.57'), 'x10 chi2 decimal shown')
        check(not any('comb(6740,680)' in c for c in calls), 'x10: the too-big Fisher fraction was sent to the CAS')
        # calls: ex 2 page 6 (1, the Fisher fraction) + page 7 (5) ; x10 (3: ad, product, chi2) ; back
        # to ex 2 (the key is new again: 1 + 5)
        check(len(calls) == 6 + 3 + 6, 'giac ex2: %d CAS calls, want 15' % len(calls))
        for l in first.lines():
            say('      p7| ' + l)
    else:
        check(all(has(p, 'decimal') for p in p7s), 'fail ex 2: every page 7 frame has the decimal badge')
    hh2 = None

# examples 3 and 4: the r x c exact page is page 6
for mode in ('giac', 'fail'):
    hh = Harness(SRC, cas=mode, seed=4, strict=False)
    hh.choose(12, 3)
    hh.press(*(['Right'] * 5))
    hh.press('Esc')
    hh.choose(12, 4)
    hh.press(*(['Right'] * 5))
    hh.press('Esc')
    hh.choose(14)
    hh.call('ChiTable')
    check(hh.error is None, '%s ex3/4: runtime error %s' % (mode, hh.error))
    pe = pages(hh, 'csPageExact')
    check(len(pe) >= 2 and all(has(p, '6/6') for p in pe), '%s: the r x c exact page is 6/6' % mode)
    if mode == 'giac':
        for p in pe:
            check(has(p, '= 3668733438511/122005828000 = 30.070'), 'giac ex 3/4 fraction line')
        check(has(pe[0], 'first cell: (762 - 1557 × 1246 / 2757)²') and has(pe[0], ', and 5 more'), 'ex 3 first cell')
        for l in pe[0].lines():
            say('      ex3| ' + l)
    else:
        check(all(has(p, '= 30.070') and has(p, 'decimal') for p in pe), 'fail ex 3/4: decimal + badge')
    say('  [%s] examples 3 and 4: %d exact-page frames, %d CAS calls' % (mode, len(pe), len(hh.cas_calls)))

# ================================================================ E. the fence
say('\nE. the fence')
src = open(SRC, encoding='utf-8').read()
code = re.sub(r'//[^\n]*', '', src)
code = re.sub(r'"[^"\n]*"', '""', code)
defs = [(m.group(1), m.start()) for m in re.finditer(r'(?m)^(?:EXPORT\s+)?([A-Za-z]\w*)\(([^()]*)\)\s*\nBEGIN', code)]
bodies = {}
for i, (n, s) in enumerate(defs):
    e = defs[i + 1][1] if i + 1 < len(defs) else len(code)
    bodies[n] = code[s:e]
names = set(bodies)
graph = {n: {m for m in re.findall(r'\b([A-Za-z]\w*)\s*\(', b[b.index('BEGIN'):]) if m in names and m != n}
         for n, b in bodies.items()}


def reach(n, seen=None):
    seen = set() if seen is None else seen
    for m in graph.get(n, ()):
        if m not in seen:
            seen.add(m)
            reach(m, seen)
    return seen


callers = sorted(n for n in names if 'csCas' in graph[n])
check(callers == ['csXChi', 'csXFisher'], 'only csXFisher and csXChi call csCas: %s' % callers)
ens = sorted(n for n in names if 'csXEnsure' in graph[n])
check(ens == ['csFishPlot', 'csPage2x2', 'csPageExact'], 'csXEnsure called from %s' % ens)
check(code.count('CAS(') == 0 and src.count('cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + csS + ")" + CHAR(34) + ")"));') == 1,
      '3a: exactly one CAS call site, the EXPR form in csCas, and no CAS( on a variable')
check(':=' not in ''.join(re.findall(r'csCas\(([^;]*)\);', code)), '3a: no CAS text assigns a CAS variable')
for f in ('csBarDrag', 'csMorph', 'csCurve', 'csCvDraw', 'csCvFit', 'csBars', 'csMosaic', 'csResBars',
          'csFishDraw', 'csPlotLoop', 'csGrid', 'csEntry', 'csScaleN', 'csResMenu', 'csCompute', 'csFisher'):
    check('csCas' not in reach(f), '%s can reach csCas' % f)
say('  csCas is called by %s only; csXEnsure by %s; no drag, animation or frame routine reaches it' % (callers, ens))

# the cache, measured: a bar drag asks nothing; the same table asks nothing; a new table asks once
hh = Harness(SRC, cas='giac', seed=5, strict=False)
hh.call('csInit')
# a small table, so the dragged table is small too (C(N, c1) under 100 digits: the CAS is asked)
load(hh, 2, 2, [12, 5, 9, 7])
hh.globals_['csKeep'] = [12.0, 5.0, 9.0, 7.0]
hh.globals_['csFoot'] = '6/7'
hh.call('csPage2x2'); n1 = len(hh.cas_calls)
hh.call('csPage2x2')
n2 = len(hh.cas_calls)
check(n1 == 1 and n2 == 1, 'page 6 twice on one table: %d then %d calls (want 1, 1)' % (n1, n2))
# the bars plot as a student meets it: press the solid bar of R1 C1, drag it up, lift, Esc
hh.drag([(55, 160), (55, 140), (55, 120), (55, 100)])
hh.press('Esc')
hh.call('csPlotLoop', 1)
n3 = len(hh.cas_calls)
check(n3 == n2, 'the bar drag made %d CAS calls' % (n3 - n2))
check(hh.globals_['csO'][0] != 12.0, 'the drag changed the count (%s)' % hh.globals_['csO'][0])
hh.call('csPage2x2'); n4 = len(hh.cas_calls)
check(n4 == n3 + 1, 'page 6 after the drag: %d new calls (want 1)' % (n4 - n3))
say('  page 6 twice: %d call; a bar drag (count 12 -> %d): 0 calls; page 6 after it: %d call' % (
    n1, int(hh.globals_['csO'][0]), n4 - n3))
# the morph and the curve drag, run for real: no calls
hh.call('csInit'); load(hh, 2, 2, [53, 430, 15, 176])
n5 = len(hh.cas_calls)
hh.press('Enter'); hh.call('csMorph')
n6 = len(hh.cas_calls)
check(n6 == n5, 'the morph made %d CAS calls' % (n6 - n5))
# the curve: drag the red critical line (x 168 at alpha 0.05, df 1) to the left, lift, Esc
hh.drag([(168, 100), (150, 100), (130, 100), (110, 100)])
hh.press('Esc')
hh.call('csCurve')
n7 = len(hh.cas_calls)
check(n7 == n6, 'the curve drag made %d CAS calls' % (n7 - n6))
check(abs(hh.globals_['csAlpha'] - 0.05) > 0.001, 'the curve drag moved alpha (%s)' % hh.globals_['csAlpha'])
say('  the morph (10 frames) and a drag of the critical line (alpha 0.05 -> %s): 0 CAS calls' % hh.globals_['csAlpha'])

# untouched routines: byte-identical to beta 2
old = open(OLD, encoding='utf-8').read()


def body(txt, name):
    m = re.search(r'(?m)^' + re.escape(name) + r'\([^\n]*\)\nBEGIN\n.*?^END;', txt, re.S)
    return m.group(0) if m else None


same = []
for f in ('csCompute', 'csFisher', 'csFishW', 'csCheck', 'csTotals', 'csAskAll', 'csNewTable', 'csSetAlpha',
          'csDrain', 'csWaitAny', 'csBarDrag', 'csMorph', 'csCurve', 'csCvDraw', 'csBars', 'csMosaic', 'csEntry'):
    b3, b2 = body(src, f), body(old, f)
    if check(b3 is not None and b3 == b2, '%s differs from beta 2' % f):
        same.append(f)
say('  byte-identical to beta 2: ' + ', '.join(same))

# 3a: beta 3 in v3b -- the emulator's finding: the text comes back unevaluated, no fraction
h3 = Harness(BETA3, cas='giac', seed=1)
h3.call('csInit')
load(h3, 2, 2, [3, 1, 1, 3])
h3.call('csXEnsure', 1)
check(h3.globals_['csXFr'] == '' and h3.globals_['csXX2'] == '' and any('non-literal' in w for w in h3.warnings),
      '3a: beta 3 in v3b shows no fraction (csXFr %r, csXX2 %r)' % (h3.globals_['csXFr'], h3.globals_['csXX2']))
say('  3a: beta 3 in v3b: csXFr = %r, csXX2 = %r -- its csCas handed back its own text' % (
    h3.globals_['csXFr'], h3.globals_['csXX2']))

# ================================================================ G (round 2a)
say('\nG. beta 3b against beta 3a')
import re as _re
_b_old = open(B3A, encoding='utf-8').read()
_b_new = open(SRC, encoding='utf-8').read()


def _bodies(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = _re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


_B0, _B1 = _bodies(_b_old), _bodies(_b_new)
_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))
check(_diff == ['csExamples', 'csResMenu'], 'beta 3b: routines that differ from beta 3a: %s (want csExamples, csResMenu)' % _diff)


def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


check(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 3b: outside those routines only comments differ')
_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)
_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)
check(_py0 == _py1, 'beta 3b: the #PYTHON blocks are unchanged')
say('  routines that differ from beta 3a: %s; everything else differs only in comments' % ', '.join(_diff))


# ================================================================ W (3b): CHOOSE widths
say('\nW. 3b: every CHOOSE line fits its box (the emulator cut two lines at about 31 characters)')


def _split_top(t, sep):
    """split t at sep characters that are outside strings and brackets"""
    parts, depth, ins, cur = [], 0, False, ''
    for c in t:
        if c == '"':
            ins = not ins
        elif not ins and c in '({[':
            depth += 1
        elif not ins and c in ')}]':
            depth -= 1
        if c == sep and not ins and depth == 0:
            parts.append(cur); cur = ''
            continue
        cur += c
    parts.append(cur)
    return [x.strip() for x in parts]


def _render(expr):
    """a CHOOSE item as the student sees it: literals joined, csTimes (CHAR(215)) or any other variable
    as one glyph, a call such as csAStr() as 5 characters (its widest answer, 0.001)"""
    out = ''
    for q in _split_top(expr, '+'):
        if q.startswith('"') and q.endswith('"'):
            out += q[1:-1]
        elif re.fullmatch(r'\w+\([^()]*\)', q):
            out += '#####'
        elif q == 'csTimes':
            out += '\u00d7'
        elif q:
            out += '*'
    return out


def choose_items(path):
    src = re.sub(r'//[^\n]*', '', open(path, encoding='utf-8').read())
    out = []
    for m in re.finditer(r'\bCHOOSE\(', src):
        i = m.end(); depth = 1; ins = False
        while depth:
            c = src[i]
            if c == '"':
                ins = not ins
            elif not ins and c in '({[':
                depth += 1
            elif not ins and c in ')}]':
                depth -= 1
            i += 1
        args = _split_top(src[m.end():i - 1], ',')
        items = args[2:]
        if len(items) == 1 and items[0].startswith('{'):
            items = _split_top(items[0][1:-1], ',')
        for it in items:
            out.append((src.count('\n', 0, m.start()) + 1, _render(it)))
    return out


new_items, old_items = choose_items(SRC), choose_items(B3A)
too_long = [(ln, t, len(t)) for ln, t in new_items if len(t) > 30]
check(not too_long, '3b: no CHOOSE line longer than 30 characters (%d lines; longest %d): %s'
      % (len(new_items), max(len(t) for _, t in new_items), too_long))
old_long = sorted({t for _, t in old_items if len(t) > 30})
check(old_long == ['Death penalty × defendant\'s race', 'N / 10: every count divided by 10'],
      '3b: beta 3a had exactly the two lines the emulator cut: %s' % old_long)
say('  %d CHOOSE lines, the longest %d characters; beta 3a\'s two long ones: %s' % (
    len(new_items), max(len(t) for _, t in new_items), old_long))
# in a run: every dialog the student sees
seen = []
for ex in (1, 2, 3, 4, 5):
    hh = Harness(SRC, cas='fail', seed=5, strict=False, idle_key=4)
    hh.choose(12, ex)
    hh.press(*(['Esc'] * 3))
    hh.choose(14)
    hh.call('ChiTable')
    seen += [it for c in hh.chooses for it in c.items]
hh = Harness(SRC, cas='fail', seed=5, strict=False)
hh.choose(12, 2); hh.tap(300, 230); hh.choose(3); hh.press('Enter'); hh.press('Esc'); hh.choose(14)
hh.call('ChiTable')
seen += [it for c in hh.chooses for it in c.items]
check(all(len(t) <= 30 for t in seen), '3b: every CHOOSE line shown in the runs is 30 characters or fewer (%d seen)' % len(seen))
check({'Death penalty × defendant', 'Death penalty × victim', 'N / 10: counts divided by 10'} <= set(seen),
      '3b: the shortened lines are the ones shown')
# the shortened menus still do their jobs
for ex, cells in ((1, [53, 430, 15, 176]), (2, [64, 451, 4, 155])):
    hh = Harness(SRC, cas='fail', seed=5, strict=False, idle_key=4)
    hh.choose(12, ex); hh.press(*(['Esc'] * 3)); hh.choose(14); hh.call('ChiTable')
    check([int(v) for v in hh.globals_['csO']] == cells, '3b: example %d still loads %s (got %s)' % (ex, cells, hh.globals_['csO']))
hh = Harness(SRC, cas='fail', seed=5, strict=False)
hh.choose(12, 2); hh.tap(300, 230); hh.choose(2); hh.press('Enter'); hh.tap(300, 230); hh.choose(3); hh.press('Enter')
hh.press('Esc'); hh.choose(14); hh.call('ChiTable')
check([int(v) for v in hh.globals_['csO']] == [64, 451, 4, 155], '3b: x10 N then "N / 10: counts divided by 10" gives the table back')

say('\n%d checks passed, %d failed' % (NPASS[0], len(FAILS)))
if FAILS:
    say('FAILURES:\n  ' + '\n  '.join(FAILS[:40]))
    sys.exit(1)
say('ALL OK')
