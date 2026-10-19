#!/usr/bin/env python3
"""verify_ChiTable_beta3d.py -- ChiTable beta 3d (19 Oct 2026): the fleet review's fixes (D8, D-CT-1..5).
Built from verify_ChiTable_beta3c.py; every check is kept and now runs in harness ppl_run_v3e (which gives
v3d's results with home_minus off).  Changed old checks (their expected value WAS the bug, or the routine
was meant to change):
  R6   the tea table's RD line: beta 3c's Wald "(-0.1001, 1.1001)" is now Newcombe's "(-0.1355, 0.7891)";
  E    "byte-identical to beta 2": csCompute, csAskAll and csEntry are now checked to differ from beta 2
       ONLY by the 3d edits (part G3d has the exact lines); the other eleven stay byte-identical;
  G 3c the 3c-vs-3b record now reads the 3c file (out/ChiTable_beta3c.txt), not this version.
New checks (3d), part N, each run on beta 3d AND on beta 3c to show the old version failing:
  N1  D8, Newcombe: csWils against statsmodels' Wilson interval; csCompute's RD interval over EVERY 2 x 2
      table with row totals <= 12 (7,812 tables, the review's grid) against an exact Newcombe of our own
      (mpmath, 40 digits, the program's z = 1.959964): max error < 1E-9, never outside [-1, 1], never
      width 0; our Newcombe against statsmodels' confint_proportions_2indep(method='newcomb'); a 12-digit
      transcription (decimal, 12 significant digits) of csWils + the four lines; the three values of
      findings_D on page 6; beta 3c's Wald on the same grid (1,388 outside [-1, 1], 288 of width 0);
  N2  D-CT-1, csUpper: against scipy chi2.sf for df 1 and 2; CS_P, csPG, csPY for huge chi-square tables
      (beta 3c's CS_P is exactly 0) and, with the Prime's 12-digit CDFs modelled (twelve_digits(), as the
      review's check_StatDist.py), at chi2 = 60 (beta 3c 0, beta 3d 9.49E-15); every page of the four
      examples and the tea table identical to beta 3c's except the RD line and the note;
  N3  D-CT-2: the help's rule is the rule the pages apply, on a 2 x 3 with one E = 4.5 (beta 3c's help
      passed it, its page 5 called it shaky);
  N4  D-CT-3: a typed 0.004 -> "Counts are whole numbers: 0.00 was rounded to 0.", no scientific form
      (beta 3c: "4.00E-3", the review's probe P1);
  N5  D-CT-4: 1E9 refused in the cell editor and the Values form (beta 3c took it, probe P2); 9,999,999
      taken; the exact page's counts lines in words when too long (beta 3c ran past 296 px);
  N6  D-CT-5: a negative count in the Values form is refused on Run (beta 3c made it 0 silently);
  N7  page 6's note, both branches, within the line;
  G3d beta 3d against beta 3c: the routines that differ are exactly csCompute, csAskAll, csEntry,
      csPageExact, csPage2x2, csHelp and the new csUpper, csWils, each changed only in the lines listed;
      outside them only comments differ; static rules on the new code (LOCAL <= 6, no comment inside a
      bracket, no built-in name, defined before use, INSTRING sites unchanged).
  S   h.sci_strings over every beta 3d run in this script: none.
(The beta 3c description follows; "v3d" there now means v3e.)

verify_ChiTable_beta3c.py -- ChiTable beta 3c (17 Oct 2026): the round-2 emulator fixes.
Built from verify_ChiTable_beta3b.py; every check is kept and now runs in harness v3d, which raises
"Invalid input" for INSTRING("", ...) and prints small fixed decimals the Prime's way (h.sci_strings).
New checks (3c), section R at the end:
  R1 the compile fix: no // comment inside an open bracket (ppl_check_v4 E12 and a scan of our own);
     beta 3b had exactly the two in csResMenu's CHOOSE list; the list itself is unchanged.
  R2 csCas: a failed call returns "" with no error; undef, an error, an infinity are still refused;
     beta 3b's csCas stops on the failed call (INSTRING("", "undef")).
  R3 cas='fail' end to end: the tea table (pages 6 and 7, the Fisher plot), example 2 with x10 N and
     N / 10, examples 3 and 4 -- all complete with the "decimal" badge and no error; beta 3b in v3d
     stops on every one of these runs.
  R4 fixed decimals: tables chosen to give tiny values (chi2, V, E, contributions, percentages, p1/p2,
     z, RD/RR/OR bounds, residuals) and a typed alpha of 0.00005 run through every results page,
     x10 N, every plot and Quit, cas='giac' and 'fail': no scientific STRING in beta 3c; beta 3b
     printed them (listed).  Then h.sci_strings over EVERY beta 3c harness run in this script.
  R5 the helpers csSgn, csNoZero, csAStr, csXX2Txt on the edge values.
  R6 the tea table's risk difference interval, (-0.1001, 1.1001): shown as computed (an observation
     for Roger: a Wald interval can pass 1).
  G  beta 3c against beta 3b: the routines that differ, each one's change exactly as listed; the
     swept routines differ from 3b ONLY by STRING(x, 2, d) -> STRING(ROUND(x, d), 2, d).
(The beta 3b description follows; "v3c" there now means v3d.)

verify_ChiTable_beta3b.py -- ChiTable beta 3b (17 Oct 2026): two CHOOSE lines shortened (the emulator cut
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
import ppl_run_v3e as RV3E  # noqa: E402  (3d: harness v3e; the 12-digit model patches RV3E._StatFns.log)
from ppl_run_v3e import Harness as _HarnessV3e  # noqa: E402
from hpkit.interp import PPLError  # noqa: E402

ALL_H = []          # 3c: every harness made in this script, for the sci_strings audit (R4)


class Harness(_HarnessV3e):
    def __init__(self, paths=None, *a, **k):
        _HarnessV3e.__init__(self, paths, *a, **k)
        self._src = paths
        ALL_H.append(self)

SRC = '/home/claude/work/fix19/ChiTable_beta3d.txt'
B3C = '/home/claude/work/out/ChiTable_beta3c.txt'
B3B = '/home/claude/work/out/ChiTable_beta3b.txt'
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
B3C_TXT = open(B3C, encoding='utf-8').read()


def body(txt, name):
    m = re.search(r'(?m)^' + re.escape(name) + r'\([^\n]*\)\nBEGIN\n.*?^END;', txt, re.S)
    return m.group(0) if m else None


same = []
# 3d: csCompute, csAskAll and csEntry were byte-identical to beta 2 up to beta 3c; beta 3d changes them on
# purpose (Newcombe and csUpper; the count cap and the negative count; the cap and the rounded message).
# Here they must differ from beta 2, and part G3d checks that the difference is exactly the 3d lines.
for f in ('csFisher', 'csFishW', 'csCheck', 'csTotals', 'csNewTable', 'csSetAlpha',
          'csDrain', 'csWaitAny', 'csBarDrag', 'csMorph', 'csCurve'):
    b3, b2 = body(src, f), body(old, f)
    if check(b3 is not None and b3 == b2, '%s differs from beta 2' % f):
        same.append(f)
say('  byte-identical to beta 2: ' + ', '.join(same))
for f in ('csCompute', 'csAskAll', 'csEntry'):
    check(body(src, f) != body(old, f) and body(B3C_TXT, f) == body(old, f),
          '3d: %s was byte-identical to beta 2 in 3c and changes in 3d' % f)
say('  3d: csCompute, csAskAll, csEntry were byte-identical to beta 2 in beta 3c; beta 3d changes them (G3d)')


def _norm(t):
    """a routine's code: comments, blank lines and trailing blanks removed"""
    t = re.sub(r'//[^\n]*', '', t)
    return '\n'.join(l.rstrip() for l in t.split('\n') if l.strip())


def _unround(t):
    """3c's sweep undone: STRING(ROUND(x, d), 2, d) -> STRING(x, 2, d)"""
    return re.sub(r'STRING\(ROUND\((.*?), (\w+)\), 2, \2\)', r'STRING(\1, 2, \2)', t)


# 3c: three device-tested drawing routines carry the round-2 sweep and nothing else
for f in ('csCvDraw', 'csBars', 'csMosaic'):
    b3, b2 = body(src, f), body(old, f)
    check(b3 is not None and b3 != b2 and _unround(_norm(b3)) == _norm(b2),
          '3c: %s differs from beta 2 by more than STRING(ROUND(x, d), 2, d)' % f)
say('  3c: csCvDraw, csBars, csMosaic differ from beta 2 only by STRING(x, 2, d) -> STRING(ROUND(x, d), 2, d)')

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
say('\nG. beta 3b against beta 3a (kept from the 3b script)')
import re as _re
_b_old = open(B3A, encoding='utf-8').read()
_b_new = open(B3B, encoding='utf-8').read()


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


# ================================================================ R (3c): the round-2 emulator findings
say('\nR. 3c: the round-2 emulator findings (harness v3d; now v3e, run on beta 3d)')


def comment_in_bracket(path):
    """(line, bracket) for every // comment met while a ( [ or { is open -- a Syntax Error on the Prime"""
    txt = re.sub(r'(?s)#PYTHON.*?#END', lambda m: '\n' * m.group(0).count('\n'), open(path, encoding='utf-8').read())
    out, stack, ins, i, ln = [], [], False, 0, 1
    while i < len(txt):
        c = txt[i]
        if c == '\n':
            ln += 1
        if ins:
            if c == '"':
                ins = False
        elif c == '"':
            ins = True
        elif txt.startswith('//', i):
            if stack:
                out.append((ln, stack[-1][1]))
            j = txt.find('\n', i)
            i = len(txt) if j < 0 else j
            continue
        elif c in '([{':
            stack.append((c, ln))
        elif c in ')]}':
            if stack:
                stack.pop()
        i += 1
    return out


# R1. the compile fix
cb_new, cb_old = comment_in_bracket(SRC), comment_in_bracket(B3B)
check(cb_new == [], 'R1: beta 3d has a // comment inside an open bracket: %s' % cb_new)
check(cb_old == [(1277, 1274), (1278, 1274)], 'R1: beta 3b had the two comments in the CHOOSE list: %s' % cb_old)
say('  R1 own scan: beta 3b comments inside an open bracket at %s (the { of line %s); beta 3d: %s' % (
    [l for l, _ in cb_old], cb_old[0][1] if cb_old else '-', cb_new or 'none'))
_ck = subprocess.run([sys.executable, '-I', '/home/claude/work/ppl_check_v4.py',
                      '/home/claude/work/whitelist_empty.json,/home/claude/work/HP_Prime_Builtin_Names.txt', SRC],
                     capture_output=True, text=True).stdout
_ck0 = subprocess.run([sys.executable, '-I', '/home/claude/work/ppl_check_v4.py',
                       '/home/claude/work/whitelist_empty.json,/home/claude/work/HP_Prime_Builtin_Names.txt', B3B],
                      capture_output=True, text=True).stdout
e12n, e12o = len(re.findall(r'\bE12\b', _ck)), len(re.findall(r'\bE12\b', _ck0))
check(e12n == 0 and e12o == 2, 'R1: ppl_check_v4 E12: beta 3d %d (want 0), beta 3b %d (want 2)' % (e12n, e12o))
say('  R1 ppl_check_v4 E12: beta 3b %d, beta 3d %d' % (e12o, e12n))
# the list itself is unchanged: the same four items, the same order (comments moved above the CHOOSE)
_rm_new = [it for ln, it in choose_items(SRC) if 'counts divided by 10' in it or 'Restore the original' in it or it in ('Main menu',) or '10 N:' in it]
_rm_old = [it for ln, it in choose_items(B3B) if 'counts divided by 10' in it or 'Restore the original' in it or it in ('Main menu',) or '10 N:' in it]
check(_rm_new == _rm_old and len(_rm_new) == 4, 'R1: the Results menu items changed: %s vs %s' % (_rm_new, _rm_old))
_bn, _bo = body(src, 'csResMenu'), body(open(B3B, encoding='utf-8').read(), 'csResMenu')
check(_norm(_bn) == _norm(_bo), 'R1: csResMenu differs from beta 3b in more than its comments')
say('  R1 csResMenu: the same code as beta 3b once comments are set aside; items %s' % _rm_new)
# and a run through the Results menu still works: example 2, Menu, N / 10 refused? no -- x10 N then N / 10
hh = Harness(SRC, cas='giac', seed=11, strict=False)
hh.choose(12, 2); hh.tap(300, 230); hh.choose(2); hh.press('Enter'); hh.tap(300, 230); hh.choose(3); hh.press('Enter')
hh.tap(300, 230); hh.choose(4); hh.press('Esc'); hh.choose(14); hh.call('ChiTable')
_menus = [c for c in hh.chooses if c.title == 'Results menu']
check(hh.error is None and len(_menus) == 3 and [int(v) for v in hh.globals_['csO']] == [64, 451, 4, 155],
      'R1: the Results menu runs (x10 N, N / 10, Restore): %s %s' % (hh.error, hh.globals_['csO']))

# R2. csCas
hf = Harness(SRC, cas='fail', seed=1)
hf.call('csInit')
r = hf.call('csCas', '34/70')
check(r == '' and hf.error is None, 'R2: csCas with the CAS failing returned %r' % r)
say('  R2 csCas("34/70") with the CAS failing: %r, no error' % r)
hg = Harness(SRC, cas='giac', seed=1)
hg.call('csInit')
for q, want in (('34/70', '17/35'), ('comb(8,4)', '70'), ('1/0', ''), ('0/0', ''), ('limit(1/csj,csj,0,1)', ''),
                ('3*4-1*1', '11')):
    got = hg.call('csCas', q)
    check(got == want, 'R2: csCas(%r) = %r, want %r' % (q, got, want))
say('  R2 csCas with Giac: 34/70 -> 17/35, comb(8,4) -> 70; 1/0 (the Prime prints +-inf), 0/0 (undef), '
    'a one-sided limit to infinity -> "" (refused)')
h0 = Harness(B3B, cas='fail', seed=1)
h0.call('csInit')
try:
    h0.call('csCas', '34/70')
    check(False, 'R2: beta 3b csCas did not stop on a failed call in v3d')
except PPLError as ex:
    check('INSTRING' in str(ex), 'R2: beta 3b stopped, but not on INSTRING: %s' % ex)
    say('  R2 beta 3b csCas, the same failed call in v3d: stops -- %s' % str(ex)[:70])

# R3. cas='fail' end to end; beta 3b stops on each run
for label, fn in (('tea (pages 6, 7, Fisher plot)', 'tea'), ('example 2, x10 N, N / 10', 'ex2'), ('examples 3 and 4', 'ex34')):
    res = {}
    for path in (SRC, B3B):
        hh = Harness(path, cas='fail', seed=21, strict=False)
        if fn == 'tea':
            hh.choose(1); hh.tap(80, 230); hh.answer({'a1': 3, 'a2': 1, 'a3': 1, 'a4': 3}); hh.tap(300, 230)
            hh.press(*(['Right'] * 6)); hh.press('Esc'); hh.choose(10); hh.press('Esc'); hh.choose(14)
        elif fn == 'ex2':
            hh.choose(12, 2); hh.press(*(['Right'] * 6)); hh.tap(300, 230); hh.choose(2); hh.press('Enter')
            hh.tap(300, 230); hh.choose(3); hh.press('Enter'); hh.press('Esc'); hh.choose(14)
        else:
            hh.choose(12, 3); hh.press(*(['Right'] * 5)); hh.press('Esc')
            hh.choose(12, 4); hh.press(*(['Right'] * 5)); hh.press('Esc'); hh.choose(14)
        try:
            hh.call('ChiTable')
        except Exception:
            pass
        res[path] = hh
    hn, ho = res[SRC], res[B3B]
    exact = [p for p in hn.pages if p.func in ('csPage2x2', 'csPageExact', 'csFishDraw')]
    check(hn.error is None and exact and all(has(p, 'decimal') for p in exact if p.func != 'csPage2x2' or has(p, 'Fisher')),
          'R3 %s: beta 3d with the CAS failing: error %s, %d exact-page frames' % (label, hn.error, len(exact)))
    check(not any(has(p, 'exact (CAS)') for p in exact), 'R3 %s: an "exact (CAS)" badge with the CAS failing' % label)
    check(isinstance(ho.error, PPLError) and 'INSTRING' in str(ho.error),
          'R3 %s: beta 3b in v3d did not stop on INSTRING (%s)' % (label, ho.error))
    say('  R3 %-30s cas=fail: beta 3d completes, %d exact-page frames, all "decimal"; beta 3b stops in %s: %s' % (
        label, len(exact), getattr(ho.error, 'ppl_stack', ['?'])[-1], str(ho.error)[:40]))

# R4. fixed decimals: tables that give tiny values, every page and plot, both CAS modes
SMALL = [
    ([1000, 1001, 1000, 1000], None, 'near independence (chi2 0.0003, V 0.0003, z, RD ~ 0)'),
    ([1, 1, 1, 20000], 0.00005, 'a sparse table (E 0.0002, p2 0.00005), alpha typed 0.00005'),
    ([2, 30000, 1, 30000], None, 'rare outcome (p1, p2 under 0.0001, RR bounds)'),
    ([3, 1, 1, 3], None, 'the tea table'),
]


def small_run(path, cells, mode, alpha):
    hh = Harness(path, cas=mode, seed=31, strict=False)
    if alpha is not None:
        hh.choose(11); hh.answer({'alV': alpha})
    hh.choose(1); hh.tap(80, 230)
    hh.answer({'a1': cells[0], 'a2': cells[1], 'a3': cells[2], 'a4': cells[3]})
    hh.tap(300, 230)                                   # Run: results page 1
    hh.tap(80, 70)                                     # page 1: tap cell R1 C1 (its E)
    hh.press(*(['Right'] * 6))                         # pages 2 .. 7
    hh.tap(300, 230); hh.choose(2); hh.press('Enter')  # Menu: x10 N, the before/after page
    hh.tap(300, 230); hh.choose(3); hh.press('Enter')  # N / 10 (refused or done)
    hh.press('Esc')
    for item in (6, 7, 8, 9, 10):                      # bars, mosaic, curve, residuals, Fisher
        hh.choose(item); hh.press('Esc')
    hh.choose(5); hh.press('Esc')                      # the results again (alpha in the menu line)
    hh.choose(14)
    try:
        ret = hh.call('ChiTable')
    except Exception:
        ret = None
    return hh, ret


old_sci = {}
for cells, alpha, tag in SMALL:
    for mode in ('giac', 'fail'):
        hn, rn = small_run(SRC, cells, mode, alpha)
        check(hn.error is None and rn and rn.startswith('ChiTable: '), 'R4 %s %s: error %s' % (tag, mode, hn.error))
        check(hn.sci_strings == [], 'R4 %s %s: beta 3d printed scientific: %s' % (tag, mode, hn.sci_strings[:6]))
        shown = [l for p in hn.pages for l in p.lines()] + [it for c in hn.chooses for it in c.items] + [rn or '']
        check(not any(u'ᴇ' in l for l in shown), 'R4 %s %s: a small-capital E on screen' % (tag, mode))
        ho, ro = small_run(B3B, cells, mode, alpha)
        for v, d, t in ho.sci_strings:
            old_sci.setdefault(t, (v, d))
        if mode == 'giac':
            say('  R4 %-58s beta 3d: 0 scientific, %d screens; beta 3b: %d scientific%s' % (
                tag, len(hn.pages), len(ho.sci_strings), ' (stopped: ' + str(ho.error)[:30] + ')' if ho.error else ''))
        if tag.startswith('near') and mode == 'giac':
            p3 = [p for p in hn.pages if p.func == 'csPageTest'][0]
            p6 = [p for p in hn.pages if p.func == 'csPage2x2'][0]
            sc = [p for p in hn.pages if p.func == 'csScaleN'][0]
            for s in ("Cramer's V = 0.000 (negligible)", 'Contingency coefficient C = 0.000', '= 0.000'):
                check(has(p3, s), 'R4 near: page 3 lacks "%s"' % s)
            check(has(p6, 'z, two proportions = -0.016') or has(p6, 'z, two proportions = 0.016')
                  or any('z, two proportions = ' in l for l in p6.lines()), 'R4 near: page 6 z line')
            check(any(l in ('0.00', '0.000') for l in sc.lines()), 'R4 near: the x10 page shows 0.00 / 0.000')
            for l in (p3.lines()[3:9] + [l for l in p6.lines() if 'Risk' in l or 'z,' in l or 'phi' in l]
                      + [l for l in sc.lines() if l[:1].isdigit()]):
                say('      | ' + l)
        if tag.startswith('a sparse') and mode == 'giac':
            sm = [it for c in hn.chooses for it in c.items if it.startswith('Set ')]
            check(sm and sm[-1] == u'Set α (now 0.00005)', 'R4 sparse: the menu line %s' % sm[-1:])
            p3 = [p for p in hn.pages if p.func == 'csPageTest'][0]
            check(any(u'critical value at α = 0.00005: ' in l for l in p3.lines()), 'R4 sparse: page 3 alpha')
            g1 = [p for p in hn.pages if p.func == 'csGrid']
            check(any(has(p, '0.00') for p in g1), 'R4 sparse: an expected count shows as 0.00')
            say('      | ' + sm[-1] + '  /  ' + [l for l in p3.lines() if 'critical' in l][0])
say('  R4 beta 3b printed, in these runs (value, digits -> text):')
for t, (v, d) in sorted(old_sci.items(), key=lambda kv: (kv[1][1], abs(kv[1][0])))[:24]:
    say('      STRING(%.6g, 2, %d) -> %s' % (v, d, t))
check(len(old_sci) >= 10, 'R4: beta 3b printed fewer scientific strings than expected (%d)' % len(old_sci))

# R5. the helpers on edge values
hu = Harness(SRC, cas='fail', seed=1)
hu.call('csInit')
for v, d, want in ((-0.004, 2, '+0.00'), (0.004, 2, '+0.00'), (-0.006, 2, '-0.01'), (1.666, 2, '+1.67'),
                   (-3.634, 2, '-3.63'), (0.00004, 4, '+0.0000'), (-0.5, 4, '-0.5000'), (0, 3, '+0.000')):
    got = hu.call('csSgn', float(v), float(d))
    check(got == want, 'R5: csSgn(%r, %d) = %r, want %r' % (v, d, got, want))
for v, d, want in ((0.004, 2, '.00'), (0.226, 3, '.226'), (0.0004, 3, '.000'), (1.0, 3, '1.000'), (0.05, 2, '.05')):
    got = hu.call('csNoZero', float(v), float(d))
    check(got == want, 'R5: csNoZero(%r, %d) = %r, want %r' % (v, d, got, want))
for a, want in ((0.05, '0.05'), (0.037, '0.037'), (0.01, '0.01'), (0.0037, '0.0037'), (0.001, '0.001'),
                (0.0001, '0.0001'), (0.00005, '0.00005'), (0.000012, '0.00001'), (0.2, '0.20'), (5e-8, '0.00000005')):
    hu.globals_['csAlpha'] = float(a)
    got = hu.call('csAStr')
    check(got == want, 'R5: csAStr at alpha %r = %r, want %r' % (a, got, want))
hu.globals_['csXX2'] = ''
for x2, want in ((0.0004, '= 0.000'), (13.157, '= 13.157'), (0, '= 0.000')):
    hu.globals_['csX2'] = float(x2)
    got = hu.call('csXX2Txt', 44.0)
    check(got == want, 'R5: csXX2Txt with chi2 %r = %r' % (x2, got))
check(hu.sci_strings == [], 'R5: the helpers printed scientific: %s' % hu.sci_strings)
say('  R5 csSgn(-0.004, 2) = "+0.00", csNoZero(0.004, 2) = ".00", csAStr at 0.00005 = "0.00005", at 5E-8 = "0.00000005"')

# R6. the tea table's risk difference interval.  3c recorded the Wald interval (-0.1001, 1.1001) as an
# observation for Roger; he chose Newcombe (D8, 19 Oct 2026), so the expected line is CHANGED here: the
# old expected value was the finding.  Beta 3c's line is checked in N1 as the regression.
hh = Harness(SRC, cas='giac', seed=2, strict=False)
hh.choose(1); hh.tap(80, 230); hh.answer({'a1': 3, 'a2': 1, 'a3': 1, 'a4': 3}); hh.tap(300, 230)
hh.press(*(['Right'] * 5)); hh.press('Esc'); hh.choose(14); hh.call('ChiTable')
p6 = [p for p in hh.pages if p.func == 'csPage2x2'][-1]
rd = [l for l in p6.lines() if l.startswith('Risk diff.')]
check(rd == ['Risk diff. p1 - p2 = +0.5000 (-0.1355, 0.7891)'], 'R6 (3d): the tea RD line %s' % rd)
_se = math.sqrt(0.75 * 0.25 / 4 + 0.25 * 0.75 / 4)
check(abs(0.5 + 1.959963984540054 * _se - 1.1001) < 5e-5, 'R6: the Wald upper bound WAS 0.5 + 1.96 SE = 1.1001')
say('  R6 tea, page 6: "%s" -- Newcombe (3d); beta 3c showed Wald, 0.5 +/- 1.96 x %.4f = (-0.1001, 1.1001)'
    % (rd[0] if rd else '?', _se))

# ================================================================ G (3c): beta 3c against beta 3b
say('\nG. 3c: beta 3c against beta 3b (the 3c record, read from out/ChiTable_beta3c.txt)')
_t0, _t1 = open(B3B, encoding='utf-8').read(), open(B3C, encoding='utf-8').read()
_N0 = {k: _norm(v) for k, v in _bodies(_t0).items()}
_N1 = {k: _norm(v) for k, v in _bodies(_t1).items()}
_d3c = sorted(n for n in set(_N0) | set(_N1) if _N0.get(n) != _N1.get(n))
SWEEP = ['ChiTable', 'csBars', 'csCvDraw', 'csEStr', 'csGrid', 'csMosaic', 'csNoZero', 'csPage2x2',
         'csPageInterp', 'csPageTest', 'csResBars', 'csScaleN', 'csXX2Txt']
OTHER = ['csAStr', 'csCas', 'csPageExact', 'csSgn']
check(_d3c == sorted(SWEEP + OTHER), 'G 3c: routines that differ from beta 3b: %s' % _d3c)
for n in SWEEP:
    check(_unround(_N1[n]) == _N0[n] and _N1[n] != _N0[n], 'G 3c: %s is more than the ROUND sweep' % n)
check(_N1['csCas'] == _N0['csCas'].replace(
    '  IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;',
    '  IF DIM(cR) > 0 THEN\n    IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;\n  END;'),
    'G 3c: csCas differs by more than the DIM guard')
check(_N1['csCas'].count('cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + csS + ")" + CHAR(34) + ")"));') == 1,
      'G 3c: the IFERR call line is unchanged')
check(_N1['csAStr'] == _N0['csAStr'].replace('BEGIN\n', 'BEGIN\n  LOCAL asD;\n  IF csAlpha < 0.0001 THEN\n'
      '    asD := MIN(11, -FLOOR(LOG(csAlpha)));\n    RETURN STRING(ROUND(csAlpha, asD), 2, asD);\n  END;\n', 1),
      'G 3c: csAStr differs by more than its new first branch')
check(_N1['csPageExact'] == _N0['csPageExact'].replace(
    '    pxR := "= " + STRING(csFish, 2, 4);\n    IF csFish < 0.0001 THEN pxR := "(< 0.0001)"; END;',
    '    IF csFish < 0.0001 THEN pxR := "(< 0.0001)"; ELSE pxR := "= " + STRING(csFish, 2, 4); END;'),
    'G 3c: csPageExact differs by more than the pxR line')
check(_outside(_t0, _d3c) == _outside(_t1, _d3c), 'G 3c: outside those routines only comments differ')
say('  differ from beta 3b: %s' % ', '.join(_d3c))
say('    the sweep only (STRING(x, 2, d) -> STRING(ROUND(x, d), 2, d)): %s' % ', '.join(SWEEP))
say('    csCas: the DIM(cR) > 0 guard; csAStr: a first branch below 0.0001; csSgn: rounds first;')
say('    csPageExact: pxR built in one IF; csResMenu: the same code, its comment moved above the CHOOSE')

# ================================================================ N (3d): the fleet review of 19 Oct 2026
say('\nN. 3d: the fleet review of 19 Oct 2026 (D8, D-CT-1 .. D-CT-5); each test on beta 3d and on beta 3c')
import mpmath  # noqa: E402
from decimal import Decimal, getcontext  # noqa: E402
from statsmodels.stats.proportion import proportion_confint, confint_proportions_2indep  # noqa: E402
from scipy.stats import chi2 as _chi2, norm as _normal  # noqa: E402  (not _norm: that is the code normaliser)

mpmath.mp.dps = 40
ZP = '1.959964'                          # the program's z (cpZ), as the decimal literal it is
ZSM = float(_normal.ppf(0.975))            # statsmodels' z, 1.959963984540054


def wilson_mp(k, n, z, s):
    """one end of the Wilson score interval, 40 digits (s = -1 lower, +1 upper)"""
    k, n, z = mpmath.mpf(k), mpmath.mpf(n), mpmath.mpf(z)
    p = k / n
    q = z * z / n
    c = (p + q / 2) / (1 + q)
    hw = z * mpmath.sqrt(p * (1 - p) / n + q / (4 * n)) / (1 + q)
    return c + s * hw


def newcombe_mp(a, n1, c, n2, z=ZP):
    """Newcombe's hybrid score interval for p1 - p2 (1998, method 10), 40 digits"""
    p1, p2 = mpmath.mpf(a) / n1, mpmath.mpf(c) / n2
    l1, u1 = wilson_mp(a, n1, z, -1), wilson_mp(a, n1, z, 1)
    l2, u2 = wilson_mp(c, n2, z, -1), wilson_mp(c, n2, z, 1)
    return (p1 - p2 - mpmath.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2),
            p1 - p2 + mpmath.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def grid_tables():
    """the review's grid (check_ChiTable.py section 7): every 2 x 2 with row totals 1..12, no zero column"""
    for n1 in range(1, 13):
        for n2 in range(1, 13):
            for a in range(0, n1 + 1):
                for c in range(0, n2 + 1):
                    b, d = n1 - a, n2 - c
                    if a + c == 0 or b + d == 0:
                        continue
                    yield [a, b, c, d]


def ct_harness(path, cas='fail', **kw):
    hh = Harness(path, cas=cas, seed=41, **kw)
    hh.call('csInit')
    return hh


def ct_load(hh, nr, nc, o):
    g = hh.globals_
    g['csNR'] = float(nr); g['csNC'] = float(nc); g['csO'] = [float(x) for x in o]
    hh.call('csCompute')
    return g


# ---- N1a: csWils against statsmodels' Wilson interval and our 40-digit Wilson ----
hn = ct_harness(SRC)
w_err_sm = w_err_mp = 0.0
nw = 0
for n_ in list(range(1, 31)) + [50, 100, 674, 1000, 9999999]:
    ks = range(0, n_ + 1) if n_ <= 100 else (0, 1, 2, n_ // 3, n_ // 2, n_ - 2, n_ - 1, n_)
    for k_ in ks:
        lo_sm, hi_sm = proportion_confint(k_, n_, alpha=0.05, method='wilson')
        lo_z, hi_z = hn.call('csWils', float(k_), float(n_), ZSM, -1.0), hn.call('csWils', float(k_), float(n_), ZSM, 1.0)
        lo_p, hi_p = hn.call('csWils', float(k_), float(n_), 1.959964, -1.0), hn.call('csWils', float(k_), float(n_), 1.959964, 1.0)
        w_err_sm = max(w_err_sm, abs(lo_z - lo_sm), abs(hi_z - hi_sm))
        w_err_mp = max(w_err_mp, abs(lo_p - float(wilson_mp(k_, n_, ZP, -1))) if k_ > 0 else abs(lo_p),
                       abs(hi_p - float(wilson_mp(k_, n_, ZP, 1))) if k_ < n_ else abs(hi_p - 1))
        nw += 1
        if k_ == 0:
            check(lo_p == 0.0, 'N1a: csWils(0, %d) lower end is exactly 0 (got %r)' % (n_, lo_p))
        if k_ == n_:
            check(hi_p == 1.0, 'N1a: csWils(%d, %d) upper end is exactly 1 (got %r)' % (n_, n_, hi_p))
        check(0.0 <= lo_p <= hi_p <= 1.0 and hi_p > lo_p, 'N1a: csWils(%d, %d) inside [0, 1], width > 0' % (k_, n_))
check(w_err_sm < 1e-12, 'N1a: csWils at statsmodels\' z = statsmodels proportion_confint(wilson), %d intervals, '
      'max |diff| %.2g' % (nw, w_err_sm))
check(w_err_mp < 1e-12, 'N1a: csWils at the program\'s z 1.959964 = our 40-digit Wilson, max |diff| %.2g' % w_err_mp)
say('  N1a csWils, %d intervals (n 1..30, 50, 100, 674, 1000, 9999999): vs statsmodels %.1e, vs 40 digits %.1e; '
    'k = 0 gives exactly 0, k = n exactly 1' % (nw, w_err_sm, w_err_mp))

# ---- N1b: our Newcombe against statsmodels (validates the reference) ----
sm_err = 0.0
for o in grid_tables():
    a, b, c, d = o
    lo_sm, hi_sm = confint_proportions_2indep(a, a + b, c, c + d, method='newcomb', compare='diff')
    lo_m, hi_m = newcombe_mp(a, a + b, c, c + d, z=repr(ZSM))
    sm_err = max(sm_err, abs(float(lo_m) - lo_sm), abs(float(hi_m) - hi_sm))
check(sm_err < 1e-12, 'N1b: our 40-digit Newcombe at statsmodels\' z = confint_proportions_2indep(newcomb) on the '
      'grid, max |diff| %.2g' % sm_err)
say('  N1b our Newcombe = statsmodels\' newcomb on all 7,812 grid tables to %.1e (at its z = %.12f)' % (sm_err, ZSM))

# ---- N1c: csCompute's RD interval over the whole grid, beta 3d and beta 3c ----
GRID = list(grid_tables())
EXTRA = [[9999999, 1, 1, 9999999], [9999999, 0, 0, 9999999], [1, 9999998, 0, 9999999], [5000000, 5000000, 1, 9],
         [64, 451, 4, 155], [53, 430, 15, 176], [640, 4510, 40, 1550], [1, 0, 0, 1], [0, 1, 1, 0]]
res = {}
for path in (SRC, B3C):
    hh = ct_harness(path)
    out = []
    for o in GRID + EXTRA:
        g = ct_load(hh, 2, 2, o)
        out.append((o, g['csRDL'], g['csRDH'], g['csRD']))
    res[path] = out
    check(not hh.sci_strings, 'N1c: csCompute alone printed nothing scientific (%s)' % os.path.basename(path))
new, oldr = res[SRC], res[B3C]
max_err = 0.0
worst = None
for o, lo, hi, rd in new:
    a, b, c, d = o
    lo_m, hi_m = newcombe_mp(a, a + b, c, c + d)
    e = max(abs(lo - float(lo_m)), abs(hi - float(hi_m)))
    if e > max_err:
        max_err, worst = e, o
out_new = [o for o, lo, hi, rd in new if lo < -1 or hi > 1]
w0_new = [o for o, lo, hi, rd in new if not hi > lo]
rd_in = [o for o, lo, hi, rd in new if not (lo <= rd <= hi)]
check(max_err < 1e-9, 'N1c: beta 3d RD interval = exact Newcombe (z 1.959964) on %d tables, max error %.2g (at %s)'
      % (len(new), max_err, worst))
check(not out_new, 'N1c: beta 3d never leaves [-1, 1]: %s' % out_new[:5])
check(not w0_new, 'N1c: beta 3d never has width 0: %s' % w0_new[:5])
check(not rd_in, 'N1c: beta 3d\'s interval always holds the estimate RD: %s' % rd_in[:5])
g_out = [o for o, lo, hi, rd in oldr[:len(GRID)] if lo < -1 or hi > 1]
g_w0 = [o for o, lo, hi, rd in oldr[:len(GRID)] if hi - lo == 0]
check(len(GRID) == 7812 and len(g_out) == 1388 and len(g_w0) == 288,
      'N1c: beta 3c (Wald) on the same grid: %d of %d outside [-1, 1] (17.8%%, want 1388), %d of width 0 (want 288)'
      % (len(g_out), len(GRID), len(g_w0)))
say('  N1c csCompute over the review\'s grid (%d tables) + %d big or example tables:' % (len(GRID), len(EXTRA)))
say('      beta 3d (Newcombe): max error vs 40 digits %.1e; outside [-1, 1]: %d; width 0: %d; min lower %.4f, '
    'max upper %.4f' % (max_err, len(out_new), len(w0_new), min(x[1] for x in new), max(x[2] for x in new)))
say('      beta 3c (Wald):     outside [-1, 1]: %d of %d (%.1f%%), width 0: %d; e.g. %s' % (
    len(g_out), len(GRID), 100.0 * len(g_out) / len(GRID), len(g_w0), g_out[:2]))
say('      the program\'s z 1.959964 against statsmodels\' %.9f moves an end by at most %.1e (invisible at 4 '
    'decimals)' % (ZSM, max(abs(float(newcombe_mp(*(o[0], o[0] + o[1], o[2], o[2] + o[3]))[i])
                                 - float(newcombe_mp(o[0], o[0] + o[1], o[2], o[2] + o[3], z=repr(ZSM))[i]))
                             for o in GRID[::7] for i in (0, 1))))

# ---- N1d: a 12-digit transcription of csWils and the four lines (the Prime's arithmetic, not the PPL) ----
getcontext().prec = 12
D = Decimal


def wils12(k, n, z, s):
    if k == 0 and s < 0:
        return D(0)
    if k == n and s > 0:
        return D(1)
    p = D(k) / D(n)
    q = z * z / D(n)
    cc = (p + q / 2) / (1 + q)
    hw = z * (p * (1 - p) / D(n) + q / (4 * D(n))).sqrt() / (1 + q)
    return cc + s * hw


z12 = D(ZP)
e12 = 0.0
bad12 = []
for o in GRID + EXTRA:
    a, b, c, d = o
    n1, n2 = a + b, c + d
    p1, p2 = D(a) / D(n1), D(c) / D(n2)
    l1, u1, l2, u2 = wils12(a, n1, z12, -1), wils12(a, n1, z12, 1), wils12(c, n2, z12, -1), wils12(c, n2, z12, 1)
    rd = p1 - p2
    lo = rd - ((p1 - l1) ** 2 + (u2 - p2) ** 2).sqrt()
    hi = rd + ((u1 - p1) ** 2 + (p2 - l2) ** 2).sqrt()
    lo_m, hi_m = newcombe_mp(a, n1, c, n2)
    e12 = max(e12, abs(float(lo) - float(lo_m)), abs(float(hi) - float(hi_m)))
    if lo < -1 or hi > 1 or not hi > lo:
        bad12.append(o)
getcontext().prec = 28
check(not bad12 and e12 < 1e-9, 'N1d: at 12 significant digits (decimal) the formulas never leave [-1, 1] or reach '
      'width 0, and agree with 40 digits to %.1e: %s' % (e12, bad12[:4]))
say('  N1d a 12-digit transcription (decimal, prec 12) on the same %d tables: none outside [-1, 1], none of width 0, '
    'max error %.1e' % (len(GRID) + len(EXTRA), e12))

# ---- N1e: page 6, the three tables findings_D names (and the review's probe P5 on beta 3c) ----
WANT_RD = {(3, 1, 1, 3): ('+0.5000 (-0.1355, 0.7891)', '+0.5000 (-0.1001, 1.1001)'),
           (3, 1, 0, 4): ('+0.7500 (0.0852, 0.9544)', '+0.7500 (0.3257, 1.1743)'),
           (5, 0, 0, 5): ('+1.0000 (0.3855, 1.0000)', '+1.0000 (1.0000, 1.0000)')}
for o, (w_new, w_old) in WANT_RD.items():
    got = {}
    for path in (SRC, B3C):
        hh = ct_harness(path, cas='giac')
        ct_load(hh, 2, 2, o)
        hh.globals_['csFoot'] = '6/7'
        hh.reset_records()
        hh.call('csPage2x2')
        got[path] = [t.text for t in hh.texts if t.text.startswith('Risk diff.')]
        check(not hh.sci_strings, 'N1e: page 6 of %s printed scientific' % (o,))
    check(got[SRC] == ['Risk diff. p1 - p2 = ' + w_new], 'N1e: %s page 6 (3d): %s' % (list(o), got[SRC]))
    check(got[B3C] == ['Risk diff. p1 - p2 = ' + w_old], 'N1e: %s page 6 (3c, Wald): %s' % (list(o), got[B3C]))
    say('  N1e %-13s beta 3d "%s"   beta 3c "%s"' % (list(o), got[SRC][0][21:], got[B3C][0][21:]))

# ---- N2: csUpper (D-CT-1) ----
hn = ct_harness(SRC)
up_err = 0.0
for df_ in (1, 2):
    for x_ in (1e-9, 1e-4, 0.01, 0.1, 0.5, 1, 2, 3.841459, 5.991465, 10, 20, 30, 52, 55, 60, 100, 200, 500, 1000, 1400):
        got = hn.call('csUpper', float(df_), float(x_))
        want = float(_chi2.sf(x_, df_))
        up_err = max(up_err, abs(got - want) / want)
check(up_err < 1e-9, 'N2: csUpper(df 1 and 2, chi2 1E-9 .. 1400) = scipy chi2.sf, max relative error %.2g' % up_err)
for x_ in (0.0, -1e-16, -3.0):
    check(hn.call('csUpper', 1.0, x_) == 1.0 and hn.call('csUpper', 2.0, x_) == 1.0,
          'N2: csUpper at chi2 = %r is 1 (no square root of a negative)' % x_)
got3 = hn.call('csUpper', 3.0, 7.814728)
check(abs(got3 - 0.05) < 1e-6, 'N2: csUpper(3, 7.8147) keeps 1 - CDF for a future r x c: %r' % got3)
say('  N2 csUpper against scipy chi2.sf, df 1 and 2, chi2 from 1E-9 to 1400: max relative error %.1e; '
    'chi2 <= 0 gives 1' % up_err)
# huge chi-square tables: CS_P, csPG, csPY keep their digits (double precision already loses them in 3c)
HUGE = [(2, 2, [100, 0, 0, 100], 'a 2 x 2, chi2 = 200'), (2, 2, [45, 5, 5, 45], 'a 2 x 2, chi2 = 64'),
        (2, 3, [300, 0, 10, 0, 300, 10], 'a 2 x 3, chi2 = 600'), (3, 2, [200, 1, 1, 200, 30, 30], 'a 3 x 2')]
for nr, nc, o, tag in HUGE:
    vals = {}
    for path in (SRC, B3C):
        g = ct_load(ct_harness(path), nr, nc, o)
        vals[path] = (g['CS_P'], g['csP'], g['csPG'], g['csDF'], g['csX2'], g['csG2'],
                      g['csPY'] if nr == nc == 2 else None, g['csYat'] if nr == nc == 2 else None)
    cs_p, p, pg, df_, x2, g2, py, yat = vals[SRC]
    ok = (abs(cs_p - _chi2.sf(x2, df_)) <= 1e-9 * _chi2.sf(x2, df_) and cs_p == p and cs_p > 0
          and abs(pg - _chi2.sf(g2, df_)) <= 1e-9 * _chi2.sf(g2, df_) and pg > 0)
    if py is not None:
        ok = ok and abs(py - _chi2.sf(yat, 1)) <= 1e-9 * _chi2.sf(yat, 1) and py > 0
    check(ok, 'N2: %s: beta 3d CS_P = %.4g, csPG = %.4g (scipy %.4g, %.4g)' % (
        tag, cs_p, pg, _chi2.sf(x2, df_), _chi2.sf(g2, df_)))
    old_p = vals[B3C][0]
    say('  N2 %-22s chi2 %.4g (df %d): CS_P beta 3d %.4g = scipy %.4g; beta 3c %.4g%s' % (
        tag, x2, df_, cs_p, _chi2.sf(x2, df_), old_p, '  <- 1 - CDF lost every digit' if old_p == 0 else ''))
    if x2 > 100:
        check(old_p == 0.0, 'N2: %s: beta 3c CS_P is exactly 0 (1 - CDF) even in double precision: %r' % (tag, old_p))
# the Prime's 12 digits: every statistics built-in rounded to 12 significant figures (the review's
# twelve_digits(), check_StatDist.py); arithmetic stays double
_LOG0 = RV3E._StatFns.log


def _log12(self, name, args, val):
    v = _LOG0(self, name, args, val)
    return float('%.12g' % v) if v == v else v


RV3E._StatFns.log = _log12
try:
    v12 = {}
    for path in (SRC, B3C):
        g = ct_load(ct_harness(path), 2, 2, [45, 5, 5, 45])
        v12[path] = (g['CS_P'], g['csX2'])
    # and a chi2 of exactly 60 straight through csUpper (the review's example: true p 9.5E-15)
    u60 = ct_harness(SRC).call('csUpper', 1.0, 60.0)
finally:
    RV3E._StatFns.log = _LOG0
check(v12[B3C][0] == 0.0, 'N2 (12 digits): beta 3c CS_P for chi2 = 64 is exactly 0: %r' % v12[B3C][0])
check(abs(v12[SRC][0] - _chi2.sf(64, 1)) <= 1e-10 * _chi2.sf(64, 1),
      'N2 (12 digits): beta 3d CS_P for chi2 = 64 = %r (scipy %r)' % (v12[SRC][0], _chi2.sf(64, 1)))
check(abs(u60 - 9.485737571e-15) <= 1e-10 * 9.4857e-15, 'N2 (12 digits): csUpper(1, 60) = %r (true 9.4857E-15)' % u60)
say('  N2 with 12-digit built-ins: [45,5,5,45] (chi2 = 64): CS_P beta 3c %r, beta 3d %.6g (true %.6g); csUpper(1, 60) = %.6g'
    % (v12[B3C][0], v12[SRC][0], _chi2.sf(64, 1), u60))


# every results page (and the bars plot, whose verdict line prints p) of the examples, beta 3d vs beta 3c:
# only the RD line and page 6's note may differ
def all_pages(path, nr, nc, o, cas='fail'):
    hh = ct_harness(path, cas=cas)
    ct_load(hh, nr, nc, o)
    hh.globals_['csLbl'] = 'Your data'
    hh.globals_['csLbl2'] = ''
    out = []
    for i, (fn, arg) in enumerate([('csGrid', 2), ('csGrid', 3), ('csPageTest', None), ('csGrid', 4),
                                   ('csPageInterp', None), ('csPage2x2', None), ('csPageExact', None),
                                   ('csBars', None)]):
        if fn == 'csPage2x2' and not (nr == nc == 2):
            continue
        hh.globals_['csFoot'] = '%d/7' % (i + 1)
        hh.reset_records()
        if arg is None:
            hh.call(fn)
        else:
            hh.call(fn, float(arg))
        out += [(fn, t.text) for t in hh.texts]
    return out, hh


diffs_all = []
for nr, nc, o in [(2, 2, [3, 1, 1, 3]), (2, 2, [53, 430, 15, 176]), (2, 2, [64, 451, 4, 155]),
                  (2, 3, [762, 327, 468, 484, 239, 477]), (3, 2, [762, 484, 327, 239, 468, 477]),
                  (2, 2, [100, 0, 0, 100]), (2, 3, [300, 0, 10, 0, 300, 10]), (2, 2, [1000, 1001, 1000, 1000])]:
    pn, hpn = all_pages(SRC, nr, nc, o)
    po, _hpo = all_pages(B3C, nr, nc, o)
    dn = [x for x in pn if x not in po]
    do = [x for x in po if x not in pn]
    allowed = all(t.startswith('Risk diff.') or t.startswith('(95% CIs') for _f, t in dn + do)
    check(len(pn) == len(po) and allowed and not hpn.sci_strings,
          'N2: every page of %s is beta 3c\'s but the RD line and the note: %s / %s' % (o, dn[:3], do[:3]))
    diffs_all.append((o, [t for _f, t in dn]))
say('  N2 every results page and the bars plot, 8 tables (the examples, tea, three huge or near-null ones): identical '
    'to beta 3c\'s except page 6\'s RD line and note, e.g. %s' % (diffs_all[1],))

# ---- N3: the Cochran rule (D-CT-2) ----


def help_page1(path):
    hh = ct_harness(path)
    hh.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter')
    hh.call('csHelp')
    return [t.text for t in hh.pages[0].texts], hh


hp_new, hhn = help_page1(SRC)
hp_old, _ = help_page1(B3C)
COCH = [12, 13, 5, 28, 32, 10]          # 2 x 3: R1 = 30, R2 = 70, C3 = 15 -> E13 = 4.5, every other E >= 5
EC = [30 * 40 / 100, 30 * 45 / 100, 30 * 15 / 100, 70 * 40 / 100, 70 * 45 / 100, 70 * 15 / 100]
rule_every = all(e >= 5 for e in EC)                                 # what the pages apply
rule_80 = sum(e < 5 for e in EC) <= 0.2 * len(EC) and min(EC) >= 1     # what beta 3c's help said
verdicts = {}
for path in (SRC, B3C):
    hh = ct_harness(path)
    ct_load(hh, 2, 3, COCH)
    hh.globals_['csFoot'] = '5/6'; hh.globals_['csLbl'] = 'Your data'
    hh.reset_records(); hh.call('csPageInterp')
    p5 = [t.text for t in hh.texts]
    hh.reset_records(); hh.globals_['csFoot'] = '3/6'; hh.call('csPageTest')
    p3 = [(t.text, t.hex) for t in hh.texts if t.text.startswith('Min expected')]
    verdicts[path] = ('1 of 6 expected counts are below 5:' in p5
                      and 'chi-square is shaky; Fisher (2x2) or merge cells.' in p5, p3)
help_new_every = ('Assumption: every expected count is 5 or more' in hp_new
                  and '(the pages flag any E below 5).  If not: use' in hp_new)
help_old_80 = any('least 80% of cells, none below 1' in l for l in hp_old)
check(help_new_every and not any('80%' in l for l in hp_new), 'N3: beta 3d help states the every-cell rule: %s'
      % [l for l in hp_new if 'ssumption' in l or 'flag' in l])
check(verdicts[SRC][0] and verdicts[SRC][1] == [('Min expected 4.50; cells with E < 5: 1 of 6', '#FF0000')],
      'N3: the pages flag the one E = 4.5 (page 5 "shaky", page 3 in red): %s' % (verdicts[SRC],))
check(not rule_every and rule_80, 'N3: the table separates the rules (every-cell fails, 80%% passes)')
check(help_new_every and verdicts[SRC][0] and not rule_every,
      'N3: beta 3d: help rule (every E >= 5) and the pages agree: both fail this table')
check(help_old_80 and verdicts[B3C][0] and rule_80,
      'N3: beta 3c (the finding): its help\'s 80%% rule PASSES this table while its page 5 calls it shaky')
say('  N3 2 x 3 %s, E = %s: page 5 says "1 of 6 ... below 5: chi-square is shaky" in both versions;' % (
    COCH, [round(e, 2) for e in EC]))
say('      beta 3d help: "%s / %s" (agrees); beta 3c help: the 80%% rule (passes the table: disagrees)' % (
    'Assumption: every expected count is 5 or more', '(the pages flag any E below 5).  If not: use'))


# ---- N4 .. N6: entry (the review's probes P1, P2 and D-CT-5) ----
def edit_cell(path, cells, typed, sel=1):
    hh = ct_harness(path, cas='giac', home_minus=True)
    g = hh.globals_
    g['csNR'] = 2.0; g['csNC'] = 2.0; g['csO'] = [float(x) for x in cells]; g['csSel'] = float(sel)
    hh.press('Enter')                          # Edit the selected cell
    hh.answer({'enV': typed})
    hh.press('Esc')                            # Cancel out of the grid
    hh.call('csEntry')
    return hh, [m.lines for m in hh.msgboxes], [float(x) for x in g['csO']]


# N4 (D-CT-3): a fractional count's message
for typed, want_new in ((0.004, 'Counts are whole numbers: 0.00 was rounded to 0.'),
                        (2.4, 'Counts are whole numbers: 2.40 was rounded to 2.'),
                        (7.25, 'Counts are whole numbers: 7.25 was rounded to 7.'),
                        (9999999.4, 'Counts are whole numbers: 9999999.40 was rounded to 9999999.')):
    hh, mb, o = edit_cell(SRC, [3, 1, 1, 3], typed)
    ho, mbo, oo = edit_cell(B3C, [3, 1, 1, 3], typed)
    check(mb == [[want_new]] and not hh.sci_strings and o[0] == round(typed),
          'N4: typed %r -> %s, cell %r, sci %s' % (typed, mb, o[0], hh.sci_strings))
    if typed == 0.004:
        check(mbo == [[u'Counts are whole numbers: 4.00ᴇ−3 was rounded to 0.']] and oo[0] == 0.0,
              'N4: beta 3c, the review\'s probe P1: %s' % mbo)
        say('  N4 typed 0.004: beta 3d "%s"; beta 3c "%s" (scientific)' % (mb[0][0], mbo[0][0]))

# N5 (D-CT-4): huge counts refused; 9,999,999 taken
for typed, refused in ((1e9, True), (10000000.0, True), (9999999.6, True), (9999999.0, False), (1e12, True)):
    hh, mb, o = edit_cell(SRC, [3, 1, 1, 3], typed)
    ho, mbo, oo = edit_cell(B3C, [3, 1, 1, 3], typed)
    msg = 'Counts above 9,999,999 do not fit the table: enter the data divided by 10.'
    if refused:
        check(mb == [[msg]] and o[0] == 3.0, 'N5: Edit %r refused, the cell keeps 3: %s %s' % (typed, mb, o))
        check(oo[0] == round(typed), 'N5: beta 3c took %r (got %r)' % (typed, oo[0]))
    else:
        check(mb == [] and o[0] == typed, 'N5: Edit %r taken: %s %s' % (typed, mb, o))
say('  N5 Edit: 1E9, 1E7, 9999999.6 and 1E12 refused with the message, the cell kept; 9,999,999 taken; beta 3c '
    'took every one')


def values_form(path, cells, typed, run=True):
    hh = ct_harness(path, cas='giac', home_minus=True)
    g = hh.globals_
    g['csNR'] = 2.0; g['csNC'] = 2.0; g['csO'] = [float(x) for x in cells]
    hh.press('Plus')                           # the Values form
    hh.answer({'a1': typed[0], 'a2': typed[1], 'a3': typed[2], 'a4': typed[3]})
    if run:
        hh.tap(300, 230)                       # Run
    hh.press('Esc')                            # Cancel (if Run refused or was not tapped)
    r = hh.call('csEntry')
    return hh, r, [m.lines for m in hh.msgboxes], [float(x) for x in g['csO']]


# the review's probe P2: four counts of 1E9 in the Values form, then Run
hh, r, mb, o = values_form(SRC, [0, 0, 0, 0], [1e9, 2e9, 1.5e9, 2.5e9])
ho, ro, mbo, oo = values_form(B3C, [0, 0, 0, 0], [1e9, 2e9, 1.5e9, 2.5e9])
check(mb[:1] == [['Counts above 9,999,999 do not fit the table: enter the data divided by 10.']] and o == [0, 0, 0, 0]
      and r == 0, 'N5: P2 in the Values form: refused, the table unchanged: %s %s %s' % (mb, o, r))
check(ro == 1 and oo == [1e9, 2e9, 1.5e9, 2.5e9] and mbo == [], 'N5: beta 3c (probe P2) took the 1E9 counts and ran')
hh, r, mb, o = values_form(SRC, [0, 0, 0, 0], [5, 1e9, 3, 7], run=False)
check(o == [5, 0, 3, 7] and mb == [['Counts above 9,999,999 do not fit the table: enter the data divided by 10.']],
      'N5: Values with one huge count: the others are taken, that cell keeps its count: %s %s' % (o, mb))
say('  N5 Values form: 1E9 x 4 refused (one message; beta 3c took them and ran: the review\'s probe P2); '
    '[5, 1E9, 3, 7] -> %s' % o)


# the exact page with the biggest counts the program now takes
def exact_page(path, o, cas='giac'):
    hh = ct_harness(path, cas=cas)
    ct_load(hh, 2, 2, o)
    hh.globals_['csFoot'] = '7/7'
    hh.reset_records()
    hh.call('csPageExact')
    return hh, [(t.text, t.est_width, t.width) for t in hh.texts]


_widest_old = 0.0
for o in ([9999999, 9999999, 9999999, 9999999], [9999999, 1, 2, 9999998], [1e9, 2e9, 1.5e9, 2.5e9]):
    hh, tx = exact_page(SRC, o)
    ho, txo = exact_page(B3C, o)
    clip = [t for t, ew, w in tx if w is not None and ew > w]
    check('  (your counts are too long to write out here)' in [t for t, _e, _w in tx] and not clip
          and not hh.sci_strings and not any(t.startswith('      / (') for t, _e, _w in tx),
          'N5: exact page for %s: the counts lines in words, nothing past its width: %s' % (o, clip))
    # beta 3c: a counts-put-in line longer than the page's 46-character rule; for the two biggest
    # tables past 296 px even by the harness's (narrower) estimate
    long_o = [(t, ew) for t, ew, _w in txo if (t.startswith('  = ') and '×' in t and '(' in t) or t.startswith('      / (')]
    _widest_old = max([_widest_old] + [ew for _t, ew in long_o])
    check(any(len(t) > 46 for t, _ew in long_o) and (o[1] == 1 or any(ew > 296 for _t, ew in long_o)),
          'N5: beta 3c\'s counts lines for %s: %s' % (o, [(len(t), ew) for t, ew in long_o]))
for o in ([3, 1, 1, 3], [64, 451, 4, 155], [640, 4510, 40, 1550], [99999, 88888, 77777, 66666]):
    hh, tx = exact_page(SRC, o)
    ho, txo = exact_page(B3C, o)
    check([t for t, _e, _w in tx] == [t for t, _e, _w in txo] and not any(ew > w for _t, ew, w in tx if w),
          'N5: exact page for %s (fits): identical to beta 3c' % (o,))
say('  N5 exact page: 9,999,999 x 4 and the 1E9 table say "(your counts are too long to write out here)", nothing '
    'clipped; beta 3c printed lines up to %d px (est.) in a 296-px box; tea, example 2, example 2 x 10 and 5-digit '
    'counts unchanged' % (_widest_old,))

# N6 (D-CT-5): a negative count in the Values form
hh, r, mb, o = values_form(SRC, [0, 0, 0, 0], [5, -5, 3, 7])
ho, ro, mbo, oo = values_form(B3C, [0, 0, 0, 0], [5, -5, 3, 7])
grid_neg = [t.text for t in hh.texts if t.font == 3]
check(o == [5, -5, 3, 7] and mb == [['A count cannot be negative.']] and r == 0 and hh.globals_['csHas'] != 1,
      'N6: Values -5: kept in the grid, Run refused with csCheck\'s message: %s %s %s' % (o, mb, r))
check(oo == [5, 0, 3, 7] and mbo == [] and ro == 1, 'N6: beta 3c turned -5 into 0 without a word and ran: %s %s' % (oo, mbo))
hh2, r2, mb2, o2 = values_form(SRC, [5, -5, 3, 7], [5, 6, 3, 7])
check(r2 == 1 and o2 == [5, 6, 3, 7] and mb2 == [], 'N6: corrected to 6, Run computes: %s %s' % (o2, r2))
say('  N6 Values [5, -5, 3, 7]: beta 3d keeps -5 (grid %s), Run says "A count cannot be negative."; beta 3c made it 0 '
    'silently and ran' % ([t for t in grid_neg if '5' in t][:4],))

# ---- N7: page 6's note ----
for o, want_new, want_old in (([3, 1, 1, 3], '(95% CIs; Newcombe for RD, log for RR and OR)',
                               '(95% CIs; log method for RR and OR)'),
                              ([3, 1, 0, 4], '(95% CIs; zero cell: +0.5 per cell for RR, OR)',
                               '(95% CIs; a zero cell: +0.5 added to every cell)')):
    for path, want in ((SRC, want_new), (B3C, want_old)):
        hh = ct_harness(path)
        ct_load(hh, 2, 2, o)
        hh.globals_['csFoot'] = '6/7'
        hh.reset_records(); hh.call('csPage2x2')
        notes = [t for t in hh.texts if t.text.startswith('(95% CIs')]
        check([t.text for t in notes] == [want], 'N7: %s note for %s: %s' % (os.path.basename(path), o, [t.text for t in notes]))
        if path == SRC:
            check(len(want) <= 48 and notes[0].est_width <= notes[0].width,
                  'N7: the note fits: %d characters (the page\'s longest emulator-tested line is 48), est. %.0f px of %s'
                  % (len(want), notes[0].est_width, notes[0].width))
say('  N7 page 6 note: "%s" (no zero cell), "%s" (a zero cell)' % (
    '(95% CIs; Newcombe for RD, log for RR and OR)', '(95% CIs; zero cell: +0.5 per cell for RR, OR)'))

# ---- the review's own probe script, run on both versions (check_ChiTable_harness.py, its SRC replaced) ----
_probe_src = open('/home/claude/work/review/check_ChiTable_harness.py', encoding='utf-8').read()
_probe_out = {}
for path in (SRC, B3C):
    _txt = _probe_src.replace("'/home/claude/work/review/fleet/ChiTable_beta3c.txt'", repr(path))
    cp_ = subprocess.run([sys.executable, '-c', _txt], capture_output=True, text=True, cwd='/home/claude/work/review')
    _probe_out[path] = cp_.stdout + cp_.stderr
pn_, po_ = _probe_out[SRC], _probe_out[B3C]
check('DONE' in pn_ and "MSGBOX: ['Counts are whole numbers: 0.00 was rounded to 0.']" in pn_
      and 'P1  csEntry' in pn_ and "sci_strings: [(0.004" not in pn_,
      'N (review probes) P1 on beta 3d: no scientific form')
check("MSGBOX: ['Counts are whole numbers: 4.00" in po_, 'N (review probes) P1 on beta 3c: the scientific form')
check('csN = 7000000000.0' in po_ and 'csN = 7000000000.0' not in pn_,
      'N (review probes) P2: beta 3c took the 1E9 counts; beta 3d did not')
check('Risk diff. p1 - p2 = +1.0000 (0.3855, 1.0000)' in pn_ and 'Risk diff. p1 - p2 = +0.7500 (0.0852, 0.9544)' in pn_
      and 'Risk diff. p1 - p2 = +1.0000 (1.0000, 1.0000)' in po_,
      'N (review probes) P5: Newcombe on beta 3d, Wald (width 0) on beta 3c')
check('ChiTable returned' in pn_ and 'stale skips: []' in pn_, 'N (review probes) P7: the stale-key run completes')
say('  the review\'s check_ChiTable_harness.py on beta 3d: P1 "%s"; P5 "%s"' % (
    [l.strip() for l in pn_.split('\n') if 'MSGBOX' in l][0][8:],
    [l.strip() for l in pn_.split('\n') if 'Risk diff' in l][0]))

# ================================================================ G3d: beta 3d against beta 3c
say('\nG3d. beta 3d against beta 3c')
_c3, _c4 = open(B3C, encoding='utf-8').read(), open(SRC, encoding='utf-8').read()
_M3 = {k: _norm(v) for k, v in _bodies(_c3).items()}
_M4 = {k: _norm(v) for k, v in _bodies(_c4).items()}
_d3d = sorted(n for n in set(_M3) | set(_M4) if _M3.get(n) != _M4.get(n))
WANT3D = sorted(['csCompute', 'csAskAll', 'csEntry', 'csPageExact', 'csPage2x2', 'csHelp', 'csUpper', 'csWils'])
check(_d3d == WANT3D, 'G3d: routines that differ from beta 3c: %s' % _d3d)
check(set(_M4) - set(_M3) == {'csUpper', 'csWils'} and not set(_M3) - set(_M4), 'G3d: two new routines, none removed')
check(_outside(_c3, _d3d) == _outside(_c4, _d3d), 'G3d: outside those routines only comments differ (the header)')
import difflib  # noqa: E402


def _chg(name):
    """the code lines (comments and indentation set aside) removed from and added to a routine"""
    a = [l.strip() for l in _M3[name].split('\n')]
    b = [l.strip() for l in _M4[name].split('\n')]
    rem = [l[2:] for l in difflib.ndiff(a, b) if l.startswith('- ')]
    add = [l[2:] for l in difflib.ndiff(a, b) if l.startswith('+ ')]
    return rem, add


EXP3D = {
    'csCompute': (['- LOCAL cpZ, cpHal;', '- csP := 1 - CHISQUARE_CDF(csDF, csX2);', '- csPG := 1 - CHISQUARE_CDF(csDF, csG2);',
                   '- csPY := 1 - CHISQUARE_CDF(1, csYat);',
                   '- cpSe := (csP1 * (1 - csP1) / csRT(1) + csP2 * (1 - csP2) / csRT(2))^0.5;',
                   '- csRDL := csRD - cpZ * cpSe;', '- csRDH := csRD + cpZ * cpSe;'],
                  ['+ LOCAL cpZ, cpHal, cpL1, cpU1, cpL2, cpU2;', '+ csP := csUpper(csDF, csX2);',
                   '+ csPG := csUpper(csDF, csG2);', '+ csPY := csUpper(1, csYat);',
                   '+ cpL1 := csWils(cpA, csRT(1), cpZ, -1); cpU1 := csWils(cpA, csRT(1), cpZ, 1);',
                   '+ cpL2 := csWils(cpCc, csRT(2), cpZ, -1); cpU2 := csWils(cpCc, csRT(2), cpZ, 1);',
                   '+ csRDL := csRD - ((csP1 - cpL1)^2 + (cpU2 - csP2)^2)^0.5;',
                   '+ csRDH := csRD + ((cpU1 - csP1)^2 + (csP2 - cpL2)^2)^0.5;']),
    'csAskAll': (['- LOCAL akOK, akI, akL, akH;', '- csO(akI) := MAX(0, ROUND(akL(akI), 0));'],
                 ['+ LOCAL akOK, akI, akL, akH, akBig;', '+ akBig := 0;', '+ IF ROUND(akL(akI), 0) > 9999999 THEN',
                  '+ akBig := 1;', '+ ELSE', '+ csO(akI) := ROUND(akL(akI), 0);', '+ END;', '+ IF akBig == 1 THEN',
                  '+ MSGBOX("Counts above 9,999,999 do not fit the table: enter the data divided by 10.");', '+ END;']),
    'csEntry': (['- MSGBOX("Counts are whole numbers: " + STRING(enV, 2, 2) + " was rounded to " + STRING(ROUND(enV, 0), 2, 0) + ".");'],
                ['+ IF ROUND(enV, 0) > 9999999 THEN',
                 '+ MSGBOX("Counts above 9,999,999 do not fit the table: enter the data divided by 10.");', '+ ELSE',
                 '+ MSGBOX("Counts are whole numbers: " + STRING(ROUND(enV, 2), 2, 2) + " was rounded to " + STRING(ROUND(enV, 0), 2, 0) + ".");',
                 '+ END;']),
    'csPageExact': (['- TEXTOUT_P("  = " + pxN + pxQ + "(" + pxA + pxQ + pxD + " - " + pxB + pxQ + pxC + ")" + csSqS, G1, 12, 56, 1, csBLUE, 296);',
                     '- TEXTOUT_P("      / (" + STRING(csRT(1), 2, 0) + pxQ + STRING(csRT(2), 2, 0) + pxQ + pxC1 + pxQ + STRING(csCT(2), 2, 0) + ")", G1, 12, 69, 1, csBLUE, 296);'],
                    ['+ pxS := "  = " + pxN + pxQ + "(" + pxA + pxQ + pxD + " - " + pxB + pxQ + pxC + ")" + csSqS;',
                     '+ pxR := "      / (" + STRING(csRT(1), 2, 0) + pxQ + STRING(csRT(2), 2, 0) + pxQ + pxC1 + pxQ + STRING(csCT(2), 2, 0) + ")";',
                     '+ IF DIM(pxS) > 46 OR DIM(pxR) > 46 THEN', '+ pxS := "  (your counts are too long to write out here)";',
                     '+ pxR := "";', '+ END;', '+ TEXTOUT_P(pxS, G1, 12, 56, 1, csBLUE, 296);',
                     '+ IF DIM(pxR) > 0 THEN TEXTOUT_P(pxR, G1, 12, 69, 1, csBLUE, 296); END;']),
    'csPage2x2': (['- TEXTOUT_P("(95% CIs; a zero cell: +0.5 added to every cell)", G1, 12, 150, 1, csRED, 296);',
                   '- TEXTOUT_P("(95% CIs; log method for RR and OR)", G1, 12, 150, 1, csGRAY, 296);'],
                  ['+ TEXTOUT_P("(95% CIs; zero cell: +0.5 per cell for RR, OR)", G1, 12, 150, 1, csRED, 296);',
                   '+ TEXTOUT_P("(95% CIs; Newcombe for RD, log for RR and OR)", G1, 12, 150, 1, csGRAY, 296);']),
    'csHelp': (['- TEXTOUT_P("Assumption: expected counts of 5 or more (at", G1, 12, 146, 1, csRED, 296);',
                '- TEXTOUT_P("least 80% of cells, none below 1).  If not: use", G1, 12, 159, 1, csRED, 296);'],
               ['+ TEXTOUT_P("Assumption: every expected count is 5 or more", G1, 12, 146, 1, csRED, 296);',
                '+ TEXTOUT_P("(the pages flag any E below 5).  If not: use", G1, 12, 159, 1, csRED, 296);']),
}
for name in ('csCompute', 'csAskAll', 'csEntry', 'csPageExact', 'csPage2x2', 'csHelp'):
    rem, add = _chg(name)
    want_rem = [x[2:] for x in EXP3D[name][0]]
    want_add = [x[2:] for x in EXP3D[name][1]]
    # compared as multisets: where difflib places a repeated "END;" is arbitrary
    from collections import Counter  # noqa: E402
    check(Counter(rem) == Counter(want_rem) and Counter(add) == Counter(want_add),
          'G3d: %s changed in exactly the listed lines\n   removed %s\n   added %s' % (name, rem, add))
    say('  %-12s %d code lines out, %d in (exactly as listed)' % (name, len(rem), len(add)))
# the new routines: defined once, before csCompute (PPL needs a routine before its first caller)
_pos = {n: _c4.find('\n' + n + '(') for n in ('csUpper', 'csWils', 'csCompute')}
check(0 < _pos['csUpper'] < _pos['csWils'] < _pos['csCompute'] and _c4.count('\ncsUpper(') == 1
      and _c4.count('\ncsWils(') == 1, 'G3d: csUpper and csWils are defined once, before csCompute')
# their callers: csUpper and csWils only from csCompute
_code4 = re.sub(r'//[^\n]*', '', _c4)
_callers = sorted({n for n, b in _bodies(_c4).items() for f in ('csUpper(', 'csWils(') if f in b.split('BEGIN', 1)[1]})
check(_callers == ['csCompute'], 'G3d: csUpper and csWils are called from csCompute only: %s' % _callers)
# names: no built-in, ignoring case (the Prime matches built-ins case-insensitively)
_bi = {l.strip().upper() for l in open('/home/claude/work/HP_Prime_Builtin_Names.txt', encoding='utf-8')
       if l.strip() and not l.lstrip().startswith('#')}
NEWNAMES = ['csUpper', 'upDF', 'upX', 'csWils', 'wsK', 'wsN', 'wsZ', 'wsS', 'wsP', 'wsQ', 'wsC', 'wsH',
            'cpL1', 'cpU1', 'cpL2', 'cpU2', 'akBig']
check(not [n for n in NEWNAMES if n.upper() in _bi], 'G3d: no new name is a built-in (ignoring case): %s'
      % [n for n in NEWNAMES if n.upper() in _bi])
_defs4 = re.findall(r'(?m)^(?:EXPORT\s+)?(\w+)\([^\n]*\)\s*\nBEGIN', _code4)
check(all(sum(1 for d_ in _defs4 if d_.lower() == n.lower()) == 1 for n in ('csUpper', 'csWils'))
      and len(_defs4) == len({d_.lower() for d_ in _defs4}),
      'G3d: csUpper and csWils are defined once; no two routines share a name, ignoring case (%d routines)' % len(_defs4))
# LOCAL lines: at most 6 names, at the top of a block
_loc = [l.strip() for l in _code4.split('\n') if l.strip().startswith('LOCAL ')]
_big = [l for l in _loc if len([x for x in l[6:].rstrip(';').split(',') if x.strip()]) > 6]
check(not _big, 'G3d: every LOCAL line holds 6 names or fewer: %s' % _big)
# INSTRING, LEFT, MID, RIGHT: the same calls as beta 3c (3d adds none)
_code3 = re.sub(r'//[^\n]*', '', _c3)
for f in ('INSTRING(', 'LEFT(', 'MID(', 'RIGHT('):
    check(sorted(l.strip() for l in _code3.split('\n') if f in l) == sorted(l.strip() for l in _code4.split('\n') if f in l),
          'G3d: the %s calls are beta 3c\'s' % f[:-1])
# every STRING(x, 2, d) in an added line has d = 0 or is rounded first
_added = [l for n in EXP3D for l in EXP3D[n][1]]
_bad_s = [c for l in _added for c in re.findall(r'STRING\(([^()]*(?:\([^()]*\))?[^()]*), 2, ([^)]+)\)', l)
          if c[1].strip() != '0' and not c[0].startswith('ROUND(')]
check(not _bad_s, 'G3d: every fixed-decimal STRING in the new lines is rounded first: %s' % _bad_s)
# no // comment inside an open bracket (a Syntax Error on the Prime)
check(comment_in_bracket(SRC) == [], 'G3d: no comment inside an open bracket')
check(all(ord(ch) < 128 for ch in _c4), 'G3d: the file is still pure ASCII (glyphs through CHAR())')
# the version strings
check(re.search(r'(?m)^// CHITABLE - beta 3d$', _c4) is not None and 'WHAT CHANGED in beta 3d (19 Oct 2026)' in _c4
      and 'Beta 3d is beta 3c with the fixes' in _c4 and 'beta 3' not in _code4,
      'G3d: banner, status lines and header say beta 3d; no code line names a version')

# Roger's addition (19 Oct 2026, 12:48): the DISCLAIMER beside the terms of use, a comment only
_hdr = ' '.join(l[2:].strip() for l in _c4.split('\n')[:40] if l.startswith('//'))
_terms_at = _hdr.find('FREE FOR EDUCATIONAL AND PERSONAL USE')
_disc_at = _hdr.find('DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes.')
check(_terms_at >= 0 and _disc_at > _terms_at and _disc_at - _terms_at < 400,
      'disclaimer: the exact sentence sits in the header right after the terms of use (%d, %d)' % (_terms_at, _disc_at))
_strs = re.findall(r'"([^"\n]*)"', re.sub(r'//[^\n]*', '', _c4))
check(not any('EDUCATIONAL' in x.upper() or 'warranty' in x for x in _strs),
      'disclaimer: no page states the terms of use, so no page needed the short line')
say('  csUpper and csWils: new, defined before csCompute, called only from it; 17 new names, none a built-in; '
    'LOCAL lines <= 6; INSTRING / LEFT / MID / RIGHT as in 3c; pure ASCII')

# ================================================================ the sci_strings audit, every run
say('\nS. h.sci_strings over every harness run of this script')
_mine = [h for h in ALL_H if h._src == SRC]
_sci = [(v, d, t) for h in _mine for v, d, t in h.sci_strings]
check(_sci == [], 'S: beta 3d printed scientific in %d places: %s' % (len(_sci), _sci[:8]))
say('  %d beta 3d harness runs, %d scientific STRING results (%d runs of older versions not counted)' % (
    len(_mine), len(_sci), len(ALL_H) - len(_mine)))

say('\n%d checks passed, %d failed' % (NPASS[0], len(FAILS)))
if FAILS:
    say('FAILURES:\n  ' + '\n  '.join(FAILS[:40]))
    sys.exit(1)
say('ALL OK')
