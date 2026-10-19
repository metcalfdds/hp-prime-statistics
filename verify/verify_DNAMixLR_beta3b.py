#!/usr/bin/env python3
"""verify_DNAMixLR_beta3b.py -- DNAMixLR beta 3b (17 Oct 2026): the round-2 emulator fixes.
Built from verify_DNAMixLR_beta3a.py; every check is kept and now runs in harness v3d, which raises
"Invalid input" for INSTRING("", ...) and prints small fixed decimals the Prime's way (h.sci_strings).
New (3b), after Part G:
  R1 dmCas with the CAS failing returns "" with no error (beta 3a stops); undef / infinity refused.
  R2 dmRepl, directly: a pattern at the end, at the start, the whole text, an empty pattern, an empty
     text and more, against Python's str.replace; the formula view with Giac, and with an answer that
     ENDS in a symbol ("1/2/dmq4/dmq3") -- it opens; beta 3a stops in dmRepl.
  R3 cas='fail' end to end (menu, example, bar, locus page, formula view, Quit); beta 3a stops.
  R4 the main menu: "Results (tap a row to drop)", every line shown 30 characters or fewer.
  R5 fixed decimals: loci with LR 1.0003 and 0.549, a rare allele (p 0.0004), theta 0.01 and a typed
     0.00004; every view, the locus pages and formula views, both CAS modes: no scientific STRING in
     beta 3b; beta 3a's listed.  R6: dmF and dmThS on edge values.
  G  beta 3b against beta 3a: the ten routines that differ, each by exactly the change listed.
  S  h.sci_strings over every beta 3b harness run in the script: none.
(The beta 3a description follows; "v3b" there now means v3d.)

verify_DNAMixLR_beta3a.py -- checks for DNAMixLR beta 3a (17 Oct 2026): the CAS call form that
CASProbe beta 1b found on the emulator.  Built from verify_DNAMixLR_beta3.py: every check is kept;
Part A also reads every template's answer in the Prime's printing (it must be unchanged: the LR is
a ratio of polynomials); Part B runs in harness v3b, which models the calculator's CAS; Part G (new)
runs beta 3 itself in v3b and compares beta 3a with beta 3.  New or changed checks are marked "3a".

What beta 3 adds, and how each part is checked:

Part A  THE CAS TEMPLATES, in desktop Giac (icas, through the harness's giac_eval, which
        writes each expression to a .giac file and runs icas on it).
        * A Python copy of dmCasP / dmCasLR builds the CAS text for every preset, every
          number of alleles the preset allows and several genotype patterns, plus custom
          hypotheses (a third typed person; three unknowns).
        * Giac's factor(normal(...)) answer is parsed with SymPy and evaluated at 6 thetas
          x 6 random frequency sets; it must equal the Python engine (a line-for-line copy of
          dmProb, itself checked against brute-force enumeration in verify_DNAMixLR.py) to
          1e-10 (relative).  The theta = 0 template must equal the theta = 0 LR.
        * Lengths: which formulas fit the locus page (4 lines of 48 characters after the
          display substitutions) -- the "which presets are tractable" table for the CHANGES.
Part B  THE PROGRAM, in the run harness v3 (ppl_run_v3, cas='giac' and cas='fail').
        * The PPL's own dmCasLR text equals the Python builder's, character for character.
        * The CAS answer to the PPL's text, evaluated by SymPy, equals the PPL ENGINE's LR
          (dmRecalc -> dmLR) at several thetas and frequencies, to 1e-10.
        * dmEdge (theta at the ladder edge, PPL bisection) equals a SciPy brentq root of
          log10 LR(theta) - log10(edge) on the Python engine, to 1e-7.
        * End to end: the locus page's formula view (badge, formula lines, theta = 0 line,
          value line) with Giac and with a failing CAS (decimal badge, no error); the cache
          (no second CAS call for the same locus); no CAS call in the theta drag; the theta
          plot's orange band-edge mark and text; an exclusion (no formula asked, no edge).
        * dmProb, dmKnowns, dmTyped and dmEval are byte-for-byte beta 2's.

Run:  python3 verify_DNAMixLR_beta3a.py     (exit status 0 = every check passed)
Roger Metcalf / Claude, 16 Oct 2026.
"""
import math
import os
import random
import re
import sys

import sympy as sp
from scipy.optimize import brentq

sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3d import Harness as _HarnessV3d, giac_eval, prime_print, PPLError  # noqa: E402

ALL_H = []          # 3b: every harness made in this script, for the sci_strings audit (S)
CHAR_TIMES = chr(215)


class Harness(_HarnessV3d):
    def __init__(self, paths=None, *a, **k):
        _HarnessV3d.__init__(self, paths, *a, **k)
        self._src = paths
        ALL_H.append(self)

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(HERE, 'DNAMixLR_beta3b.txt')
B3A = os.path.join(HERE, 'DNAMixLR_beta3a.txt')
BETA3 = os.path.join(HERE, 'DNAMixLR_beta3.txt')
BASE = os.path.join(HERE, 'DNAMixLR_beta2.txt')
FAILS = []
random.seed(20261016)


NPASS = [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('   ' + detail if detail else ''))
    if ok:
        NPASS[0] += 1
    if not ok:
        FAILS.append(name)


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


# ============================================================ the Python engine
def dm_prob(x, knowns, typed, fq, th):
    """dmProb, line for line (alleles are 1-based positions; 0 = outside M)."""
    m = len(fq)
    if any(k == 0 for k in knowns):
        return 0.0
    U = [i for i in range(1, m + 1) if i not in knowns]
    if len(U) > 2 * x:
        return 0.0
    if x == 0:
        return 1.0
    nT = len(typed)
    t = [0] * (m + 1)
    for a in typed:
        if a > 0:
            t[a] += 1
    pM, tM = sum(fq), sum(t[1:])
    tot = 0.0
    for mask in range(2 ** len(U)):
        pA, tA, nS = pM, tM, 0
        for i, u in enumerate(U):
            if mask >> i & 1:
                nS += 1
                pA -= fq[u - 1]
                tA -= t[u]
        term = 1.0
        for j in range(2 * x):
            term *= ((tA + j) * th + (1 - th) * pA) / (1 + (nT + j - 1) * th)
        tot += -term if nS % 2 else term
    return max(0.0, tot)


def knowns(H, pres, gen):
    kl = []
    for w in range(3):
        if pres[w] == 1 and H[w] == 1:
            kl += [gen[2 * w], gen[2 * w + 1]]
    return kl


def typed(pres, gen):
    tl = []
    for w in range(3):
        if pres[w] == 1:
            tl += [gen[2 * w], gen[2 * w + 1]]
    return tl


def locus_lr(pres, hp, hd, gen, fq, th):
    ty = typed(pres, gen)
    p = dm_prob(hp[3], knowns(hp, pres, gen), ty, fq, th)
    d = dm_prob(hd[3], knowns(hd, pres, gen), ty, fq, th)
    return p, d, (-1.0 if d <= 0 else p / d)


# ============================================================ the CAS text (dmCasP)
def istr(n):
    """dmIStr: a whole number as plain digits."""
    v = int(round(abs(n)))
    return ('-' if n < 0 and v else '') + str(v)


def cas_p(x, kn, ty, m, z):
    """dmCasP, line for line."""
    if any(k == 0 for k in kn):
        return '0'
    U = [i for i in range(1, m + 1) if i not in kn]
    if len(U) > 2 * x:
        return '0'
    if x == 0:
        return '1'
    nT = len(ty)
    t = [0] * (m + 1)
    for a in ty:
        if a > 0:
            t[a] += 1
    tM = sum(t[1:])
    s = ''
    for mask in range(2 ** len(U)):
        sel = [1] * (m + 1)
        tA, nS = tM, 0
        for i, u in enumerate(U):
            if mask >> i & 1:
                nS += 1
                sel[u] = 0
                tA -= t[u]
        names = ['dmq' + istr(i) for i in range(1, m + 1) if sel[i] == 1]
        ps = '+'.join(names) if names else '0'
        if len(names) > 1:
            ps = '(' + ps + ')'
        term = ''
        for j in range(2 * x):
            if j > 0:
                term += '*'
            term += ps if z == 1 else '(' + istr(tA + j) + '*dmt+(1-dmt)*' + ps + ')'
        if nS % 2 == 1:
            s += '-' + term
        else:
            if mask > 0:
                s += '+'
            s += term
    if z == 1:
        return '(' + s + ')'
    den = '*'.join('(1+(' + istr(nT + j - 1) + ')*dmt)' for j in range(2 * x))
    return '(' + s + ')/(' + den + ')'


def cas_lr(pres, hp, hd, gen, m, z):
    """dmCasLR."""
    ty = typed(pres, gen)
    p = cas_p(hp[3], knowns(hp, pres, gen), ty, m, z)
    d = cas_p(hd[3], knowns(hd, pres, gen), ty, m, z)
    return 'factor(normal((' + p + ')/(' + d + ')))'


def giac_to_sympy(ans, m):
    syms = {'dmt': sp.Symbol('dmt')}
    for i in range(1, m + 1):
        syms['dmq%d' % i] = sp.Symbol('dmq%d' % i)
    return sp.sympify(ans.replace('^', '**'), locals=syms), syms


def show_len(ans, labels):
    """the length of the text the locus page would show (dmFxShow), and its line count"""
    s = ans
    for i, lab in enumerate(labels, 1):
        s = s.replace('dmq%d' % i, 'p' + lab)
    s = s.replace('dmt', 'th').replace('*', '×')
    return len('LR = ' + s), s


PRESETS = {
    1: ('V + S vs V + 1 unknown', [1, 1, 0], [1, 1, 0, 0], [1, 0, 0, 1]),
    2: ('S + 1 unknown vs 2 unknowns', [0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 2]),
    3: ('S alone vs 1 unknown', [0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]),
    4: ('V + S + 1 unknown vs V + 2 unknowns', [1, 1, 0], [1, 1, 0, 1], [1, 0, 0, 2]),
    5: ('custom: V + S + T vs V + T + 1 unknown', [1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1]),
    6: ('custom: S + 2 unknowns vs 3 unknowns', [0, 1, 0], [0, 1, 0, 2], [0, 0, 0, 3]),
}
# (preset, m, genotype entries {V1,V2,S1,S2,T1,T2})
CASES = [
    (1, 4, [1, 2, 3, 4, 0, 0]), (1, 3, [1, 1, 2, 3, 0, 0]), (1, 3, [1, 2, 2, 3, 0, 0]),
    (1, 2, [1, 2, 1, 2, 0, 0]), (1, 2, [1, 1, 2, 2, 0, 0]), (1, 3, [1, 2, 3, 3, 0, 0]),
    (2, 4, [0, 0, 1, 2, 0, 0]), (2, 3, [0, 0, 1, 2, 0, 0]), (2, 2, [0, 0, 1, 2, 0, 0]),
    (2, 3, [0, 0, 1, 1, 0, 0]), (2, 2, [0, 0, 1, 1, 0, 0]),
    (3, 2, [0, 0, 1, 2, 0, 0]),
    (4, 3, [1, 2, 2, 3, 0, 0]), (4, 4, [1, 2, 3, 4, 0, 0]), (4, 5, [1, 2, 3, 4, 0, 0]),
    (4, 6, [1, 2, 3, 4, 0, 0]), (4, 4, [1, 1, 2, 3, 0, 0]),
    (5, 6, [1, 2, 3, 4, 5, 6]), (5, 5, [1, 2, 3, 4, 4, 5]),
    (6, 4, [0, 0, 1, 2, 0, 0]),
]
THETAS = [0.0, 0.005, 0.01, 0.03, 0.05, 0.1]


def rand_freqs(m):
    while True:
        f = [round(random.uniform(0.01, 0.3), 3) for _ in range(m)]
        if sum(f) < 0.999:
            return f


# ============================================================ Part A
print('==== Part A: every CAS template in desktop Giac, against the Python engine ====')
TABLE = []
GIAC = {}
worst = 0.0
worst0 = 0.0
for pr, m, gen in CASES:
    name, pres, hp, hd = PRESETS[pr]
    e1 = cas_lr(pres, hp, hd, gen, m, 0)
    e0 = cas_lr(pres, hp, hd, gen, m, 1)
    a1 = giac_eval(e1)
    a0 = giac_eval(e0)
    GIAC[e1], GIAC[e0] = a1, a0
    fq0 = rand_freqs(m)
    p0, d0, lr0 = locus_lr(pres, hp, hd, gen, fq0, 0.01)
    if lr0 <= 0:
        TABLE.append((pr, m, gen, len(e1), 'LR %s: no formula asked' % ('0' if lr0 == 0 else 'undefined'), '', ''))
        continue
    ex1, syms = giac_to_sympy(a1, m)
    ex0, _ = giac_to_sympy(a0, m)
    f1 = sp.lambdify([syms['dmt']] + [syms['dmq%d' % i] for i in range(1, m + 1)], ex1, 'math')
    f0 = sp.lambdify([syms['dmq%d' % i] for i in range(1, m + 1)], ex0, 'math')
    for k in range(6):
        fq = rand_freqs(m)
        for th in THETAS:
            lr = locus_lr(pres, hp, hd, gen, fq, th)[2]
            worst = max(worst, rel(f1(th, *fq), lr))
        worst0 = max(worst0, rel(f0(*fq), locus_lr(pres, hp, hd, gen, fq, 0.0)[2]))
    labels = [str(10 + i) for i in range(m)]
    n1, s1 = show_len(a1, labels)
    n0, s0 = show_len(a0, labels)
    lines1 = math.ceil(n1 / 48)
    TABLE.append((pr, m, gen, len(e1), len(a1), 'shown (%d line%s)' % (lines1, 's' if lines1 > 1 else '')
                  if lines1 <= 4 else 'too long to show', '%d chars' % len(a0)))
check('Giac formula = Python engine, %d loci x 6 frequency sets x %d thetas' % (len(CASES), len(THETAS)),
      worst < 1e-10, 'worst relative difference %.2e' % worst)
check('Giac theta = 0 formula = Python engine at theta 0', worst0 < 1e-10, 'worst %.2e' % worst0)
print('\n  Which formulas the locus page can show (labels 10, 11 ...; 4 lines x 48 characters):')
print('  %-3s %-2s %-20s %-6s %-6s %-22s %s' % ('pr', 'm', 'genotypes V S T', 'in', 'out', 'theta formula', 'theta = 0'))
for row in TABLE:
    if len(row) == 7 and isinstance(row[4], int):
        pr, m, gen, li, lo, sh, z0 = row
        print('  %-3d %-2d %-20s %-6d %-6d %-22s %s' % (pr, m, gen, li, lo, sh, z0))
    else:
        pr, m, gen, li, msg, _, _ = row
        print('  %-3d %-2d %-20s %-6d %s' % (pr, m, gen, li, msg))
# the longest CAS input any PRESET can produce: every allele count and every genotype
# pattern (each entry 0 .. m) for which both hypotheses can produce the mixture
import itertools
longest = (0, None)
for pr in (1, 2, 3, 4):
    _, pres, hp, hd = PRESETS[pr]
    who = [w for w in range(3) if pres[w] == 1]
    for m in range(2, 9):
        for pat in itertools.product(range(m + 1), repeat=2 * len(who)):
            gen = [0] * 6
            for k, w in enumerate(who):
                gen[2 * w], gen[2 * w + 1] = pat[2 * k], pat[2 * k + 1]
            ty = typed(pres, gen)
            if cas_p(hp[3], knowns(hp, pres, gen), ty, m, 0) in ('0',) or \
               cas_p(hd[3], knowns(hd, pres, gen), ty, m, 0) in ('0',):
                continue
            n = len(cas_lr(pres, hp, hd, gen, m, 0))
            if n > longest[0]:
                longest = (n, (pr, m, gen))
check('the longest CAS input any preset (1-4) can produce fits dmCasMx = 3000',
      longest[0] <= 3000, '%d characters, preset %d with %d alleles %s' % ((longest[0],) + longest[1]))
c6 = [r for r in TABLE if r[0] == 6][0]
check('custom, 3 unknowns: %d characters > 3000, so the program does not send it ("too many terms")'
      % c6[3], c6[3] > 3000 and c6[5] == 'too long to show')

# the worked example's three formulas, as the program will show them
EX_LOCI = [([12, 13, 14, 15], [0.10, 0.20, 0.15, 0.05], [1, 2, 3, 4, 0, 0]),
           ([8, 9, 11], [0.30, 0.25, 0.10], [1, 1, 2, 3, 0, 0]),
           ([16, 17], [0.20, 0.30], [1, 2, 1, 2, 0, 0])]
_, pres, hp, hd = PRESETS[1]
print('\n  The worked example (preset 1), as Giac simplifies it:')
for lab, fq, gen in EX_LOCI:
    a1 = giac_eval(cas_lr(pres, hp, hd, gen, len(lab), 0))
    a0 = giac_eval(cas_lr(pres, hp, hd, gen, len(lab), 1))
    print('    locus %s: %s\n                   theta 0: %s' % (lab, show_len(a1, [str(v) for v in lab])[1],
                                                               show_len(a0, [str(v) for v in lab])[1]))

# 3a: the same answers in the Prime's printing -- a ratio of polynomials prints alike
same_print = [e for e, a in GIAC.items() if prime_print(a) != a]
check('3a: every template\'s answer (%d) prints the same on the Prime as in desktop Giac (no exp, sqrt, list, '
      'infinity)' % len(GIAC), not same_print, str(same_print[:1]))

# ============================================================ Part B
print('\n==== Part B: the PPL program in the harness (ppl_run_v3b) ====')


def load(pres, hp, hd, loci, th=0.01, cas='giac'):
    h = Harness(PROG, strict=True, cas=cas)
    h.call('dmInit')
    g = h.globals_
    g['dmPres'] = [float(v) for v in pres]
    g['dmHp'] = [float(v) for v in hp]
    g['dmHd'] = [float(v) for v in hd]
    g['dmLoc'] = [[[float(v) for v in l], [float(v) for v in f], [float(v) for v in gg]] for l, f, gg in loci]
    g['dmInc'] = [1.0] * len(loci)
    g['dmNL'] = float(len(loci))
    g['dmTh'] = th
    g['dmSel'] = 1.0
    h.call('dmRecalc')
    return h


# B1: the PPL's text = the Python builder's; the CAS answer to it = the PPL engine
same_text = True
worstB = 0.0
nB = 0
for pr, m, gen in CASES:
    name, pres, hp, hd = PRESETS[pr]
    lab = [10 + i for i in range(m)]
    fq = rand_freqs(m)
    h = load(pres, hp, hd, [(lab, fq, gen)])
    g = h.globals_
    g['dmLab'], g['dmFq'], g['dmGen'], g['dmM'] = [float(v) for v in lab], [float(v) for v in fq], \
        [float(v) for v in gen], float(m)
    t1 = h.call('dmCasLR', 0.0)
    t0 = h.call('dmCasLR', 1.0)
    same_text = same_text and t1 == cas_lr(pres, hp, hd, gen, m, 0) and t0 == cas_lr(pres, hp, hd, gen, m, 1)
    if g['dmLR'][0] <= 0:
        continue
    ex1, syms = giac_to_sympy(GIAC[t1], m)
    f1 = sp.lambdify([syms['dmt']] + [syms['dmq%d' % i] for i in range(1, m + 1)], ex1, 'math')
    for k in range(3):
        fq2 = rand_freqs(m)
        g['dmLoc'] = [[[float(v) for v in lab], [float(v) for v in fq2], [float(v) for v in gen]]]
        for th in (0.0, 0.01, 0.03, 0.05):
            g['dmTh'] = th
            h.call('dmRecalc')
            worstB = max(worstB, rel(f1(th, *fq2), g['dmLR'][0]))
            nB += 1
check('the PPL dmCasLR text = the Python builder, every case (theta and theta = 0)', same_text)
check('CAS formula (Giac, from the PPL text) = the PPL engine dmEval, %d comparisons' % nB, worstB < 1e-10,
      'worst relative difference %.2e' % worstB)


# B2: theta at the ladder edge
EDGES = [1e-6, 1e-4, 1e-3, 1e-2, 0.1, 0.5, 2, 10, 100, 1000, 1e4, 1e6]


def band(lr):
    return sum(1 for e in EDGES if lr >= e)


def comb(loci, pres, hp, hd, th):
    c = 1.0
    for lab, fq, gen in loci:
        lr = locus_lr(pres, hp, hd, gen, fq, th)[2]
        if lr > 0:
            c *= lr
    return c


def edge_py(loci, pres, hp, hd, th0):
    """the same bracket walk, then brentq"""
    c0 = comb(loci, pres, hp, hd, th0)
    b0 = band(c0)
    pts = [0.0025 * i for i in range(21)] + [0.06, 0.08, 0.1, 0.15, 0.2, 0.25]
    ta = th0
    for t in pts:
        if t <= th0 + 1e-7:
            continue
        v = comb(loci, pres, hp, hd, t)
        if band(v) != b0:
            tg = EDGES[b0 - 1] if band(v) < b0 else EDGES[b0]
            f = lambda q: math.log10(comb(loci, pres, hp, hd, q)) - math.log10(tg)
            return brentq(f, ta, t, xtol=1e-12), tg
        ta = t
    return -1.0, 0.0


EDGE_SETS = [
    ('worked example, theta 0.01', 1, EX_LOCI, 0.01),
    ('worked example, theta 0.03', 1, EX_LOCI, 0.03),
    ('worked example, theta 0', 1, EX_LOCI, 0.0),
    ('locus 1 alone (LR 56.8 at 0.01)', 1, EX_LOCI[:1], 0.01),
    ('rare alleles: p14 = p15 = 0.01', 1, [([12, 13, 14, 15], [0.1, 0.2, 0.01, 0.01], [1, 2, 3, 4, 0, 0])], 0.01),
    ('just above 10: p = 0.2, 0.2', 1, [([12, 13, 14, 15], [0.2, 0.2, 0.2, 0.22], [1, 2, 3, 4, 0, 0])], 0.0),
    ('preset 2, two loci', 2, [([10, 11, 12, 13], [0.1, 0.2, 0.15, 0.05], [0, 0, 1, 2, 0, 0]),
                               ([10, 11, 12], [0.1, 0.2, 0.15], [0, 0, 1, 2, 0, 0])], 0.01),
]
for nm, pr, loci, th0 in EDGE_SETS:
    _, pres, hp, hd = PRESETS[pr]
    h = load(pres, hp, hd, loci, th0)
    h.call('dmEdge')
    g = h.globals_
    tpy, vpy = edge_py(loci, pres, hp, hd, th0)
    ok = (tpy < 0 and g['dmEdT'] == -1) or (abs(g['dmEdT'] - tpy) < 1e-7 and g['dmEdV'] == vpy)
    check('band edge: %s' % nm, ok, 'program theta %.8f (LR %g), brentq %.8f (LR %g)'
          % (g['dmEdT'], g['dmEdV'], tpy, vpy))

# B3: end to end -- the locus page's formula view, Giac and a failing CAS
h = load(*PRESETS[1][1:], EX_LOCI)
h.press('Minus').press('Esc')
h.call('dmLocusPanel')
pg = h.pages[-1]
lr1 = locus_lr(*PRESETS[1][1:], EX_LOCI[0][2], EX_LOCI[0][1], 0.01)[2]
check('formula view (Giac): badge, formula, theta = 0 line, value line',
      pg.has('exact (CAS)') and pg.has(u'LR = (3×th+1)×(4×th+1)/(2×(th×p15-th-p15)×')
      and pg.has(u'(p14×th-p14-th))') and pg.has(u'theta = 0: LR = 1/(2×p15×p14)')
      and pg.has('your p, th = 0.010: LR = %.3f (the program\'s value)' % lr1),
      str([t.text for t in pg.texts if 96 <= t.y <= 180]))
check('formula view: two CAS calls (theta and theta = 0), both answered', len(h.cas_calls) == 2
      and all('Error' not in c[1] for c in h.cas_calls), '%d calls' % len(h.cas_calls))
check('3a: both texts ask for string(...), both answers arrive quoted; no CAS variable assigned, no CAS call '
      'of a variable', all(c[0].startswith('string(') and c[1].startswith('"') for c in h.cas_calls)
      and not h.cas_vars and not any('non-literal' in w for w in h.warnings))
check('3a: no quote mark reaches the formula view', not any('"' in t.text for t in pg.texts))
check('formula view footer', pg.has('tap here/- = picture, arrows = locus, Esc = menu'))
# the cache: the same locus again costs no CAS call; a tap on the footer row toggles back
h.reset_records()
h.cas_calls.clear()
h.tap(100, 205).press('Esc')
h.call('dmLocusPanel')
check('the same locus again: no new CAS call (cached)', len(h.cas_calls) == 0, '%d calls' % len(h.cas_calls))
check('a tap on the footer row switches back to the picture',
      h.pages[-1].has('tap here/- = formula, + = Hp/Hd, arrows = locus') and h.globals_['dmFrm'] == 0)
# Left/Right in the formula view: each new locus is asked once
h = load(*PRESETS[1][1:], EX_LOCI)
h.press('Minus').press('Right').press('Right').press('Left').press('Esc')
h.call('dmLocusPanel')
check('three loci visited in the formula view, then back: 2 calls per new formula',
      len(h.cas_calls) == 8, '%d calls' % len(h.cas_calls))
# a failing CAS
h = load(*PRESETS[1][1:], EX_LOCI, cas='fail')
h.press('Minus').press('Esc')
r = h.call('dmLocusPanel')
pg = h.pages[-1]
check('cas=fail: decimal badge, "did not answer", the value line, no error',
      pg.has('decimal') and pg.has('The CAS did not answer: no formula here.')
      and pg.has('your p, th = 0.010: LR = %.3f' % lr1) and not pg.has('exact (CAS)') and h.error is None,
      str([t.text for t in pg.texts if 96 <= t.y <= 180]))
# a long formula: preset 4, four alleles
_, pres, hp, hd = PRESETS[4]
h = load(pres, hp, hd, [([10, 11, 12, 13], [0.1, 0.2, 0.15, 0.05], [1, 2, 3, 4, 0, 0])])
h.press('Minus').press('Esc')
h.call('dmLocusPanel')
pg = h.pages[-1]
check('preset 4, 4 alleles: "too long to show" for theta, theta = 0 formula shown instead',
      any('characters, too long to show' in t.text for t in pg.texts) and pg.has('theta = 0: LR = (p10+p11+p12+p13)^2/'),
      str([t.text for t in pg.texts if 96 <= t.y <= 180]))
# the general case: custom, 3 unknowns -- too long to send, said so, no CAS call for it
_, pres, hp, hd = PRESETS[6]
h = load(pres, hp, hd, [([10, 11, 12, 13], [0.1, 0.2, 0.15, 0.05], [0, 0, 1, 2, 0, 0])])
h.press('Minus').press('Esc')
h.call('dmLocusPanel')
pg = h.pages[-1]
check('custom, 3 unknowns: "Too many terms to send to the CAS here.", only the theta = 0 call',
      pg.has('Too many terms to send to the CAS here.') and len(h.cas_calls) == 1
      and h.globals_['dmFxS'] == 3, str([t.text for t in pg.texts if 96 <= t.y <= 180]))
# an exclusion: no formula asked
_, pres, hp, hd = PRESETS[1]
h = load(pres, hp, hd, [([16, 17], [0.2, 0.3], [1, 2, 1, 0, 0, 0])])
h.press('Minus').press('Esc')
h.call('dmLocusPanel')
check('exclusion: LR = 0 explained, no CAS call', h.pages[-1].has('LR = 0 for every p and theta: a known')
      and len(h.cas_calls) == 0)
h.call('dmEdge')
check('exclusion: no band edge to look for (dmEdT = -2)', h.globals_['dmEdT'] == -2)

# B4: the theta plot -- the orange mark, and no CAS call during the drag
h = load(*PRESETS[1][1:], EX_LOCI)
xs = [40 + i * 188 / 20 for i in range(0, 21, 4)]
h.drag([(x, 100) for x in xs]).press('Esc')
h.call('dmPlotTheta')
g = h.globals_
txt = [t.text for t in h.texts if t.grob == 'G2']
tpy, vpy = edge_py(EX_LOCI, *PRESETS[1][1:], 0.01)
check('theta plot: "band edge LR 1,000 / at theta %.4f (off plot)"' % tpy,
      'band edge LR 1,000' in txt and ('at theta %.4f (off plot)' % tpy) in txt, str([t for t in txt if 'edge' in t or 'at theta' in t]))
check('theta drag: no CAS call at all', len(h.cas_calls) == 0)
# an edge inside the plot: the rare-allele locus (LR 5,000 at theta 0.01)
loci = [([12, 13, 14, 15], [0.1, 0.2, 0.01, 0.01], [1, 2, 3, 4, 0, 0])]
h = load(*PRESETS[1][1:], loci, th=0.01)
h.press('Esc')
h.call('dmPlotTheta')
g = h.globals_
txt = [t.text for t in h.texts if t.grob == 'G2']
tpy, vpy = edge_py(loci, *PRESETS[1][1:], 0.01)
dots = [c for c in h.log if c[0] == 'RECT_P' and c[1][0].name == 'G2' and len(c[1]) >= 7
        and c[1][5] == g['dmORNG'] and c[1][6] == g['dmORNG']]
xe = 40 + int(tpy / 0.05 * 188)
check('an edge inside the plot (theta %.4f): text, and the orange dot at x %d' % (tpy, xe),
      ('at theta %.4f' % tpy) in txt and 'band edge LR 1,000' in txt and 0 < tpy <= 0.05
      and len(dots) == 1 and dots[0][1][1] == xe - 2,
      str([t for t in txt if 'edge' in t or 'at theta' in t]) + ' dots %d' % len(dots))

# B5: the stale-key run through the menu (each dialog's OK left in the buffer)
h = Harness(PROG, strict=False, stale_keys=True, idle_key=4)
h.choose(9)                                       # Load the worked example
h.choose(5)                                       # Plot: LR by locus
h.tap(44 + 40, 100).tap(44 + 40, 100)             # select bar 1, again -> locus page
h.press('Minus').press('Esc')
h.choose(12)                                      # Quit
r = h.call('DNAMixLR')
check('stale-key run: menu -> example -> bar -> locus page -> formula -> quit, no skipped page',
      not h.stale_skips and isinstance(r, str) and r.startswith('DNAMixLR: combined LR = 3981.5'),
      'result %r, skips %r' % (r, h.stale_skips))

# B6: the protected core
src3, src2 = open(PROG, encoding='utf-8').read(), open(BASE, encoding='utf-8').read()
for nm in ('dmProb', 'dmKnowns', 'dmTyped', 'dmEval'):
    pat = re.compile(r'^' + nm + r'\(.*?\)\nBEGIN\n.*?^END;\n', re.S | re.M)
    check('%s byte-for-byte beta 2' % nm, pat.search(src3).group(0) == pat.search(src2).group(0))

# G (3a): beta 3 in v3b -- the emulator's finding: its dmCas hands back its own text, which the
# formula view would show as if the CAS had written it (no decimal point, so it passes)
h = Harness(BETA3, strict=True, cas='giac')
h.call('dmInit')
g = h.globals_
g['dmPres'] = [float(v) for v in PRESETS[1][1]]; g['dmHp'] = [float(v) for v in PRESETS[1][2]]
g['dmHd'] = [float(v) for v in PRESETS[1][3]]
g['dmLoc'] = [[[float(v) for v in l], [float(v) for v in f], [float(v) for v in gg]] for l, f, gg in EX_LOCI]
g['dmInc'] = [1.0] * len(EX_LOCI); g['dmNL'] = float(len(EX_LOCI)); g['dmTh'] = 0.01; g['dmSel'] = 1.0
h.call('dmRecalc')
h.press('Minus').press('Esc')
h.call('dmLocusPanel')
pg = h.pages[-1]
check('3a: beta 3 in v3b shows its own CAS text as the formula ("factor(normal(..." under "exact (CAS)")',
      pg.has('exact (CAS)') and any('factor(normal(' in t.text for t in pg.texts)
      and any('non-literal' in w for w in h.warnings), str([t.text for t in pg.texts if 96 <= t.y <= 130]))
say = print
_saved_check = check


def _check2(cond, msg):
    _saved_check(msg, cond)


check = _check2

# ================================================================ G (round 2a)
say('\nG. beta 3a: beta 3 in harness v3d, and beta 3a against beta 3 (kept from the 3a script)')
import re as _re
_b_old = open(BETA3, encoding='utf-8').read()
_b_new = open(B3A, encoding='utf-8').read()


def _bodies(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = _re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


_B0, _B1 = _bodies(_b_old), _bodies(_b_new)
_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))
check(_diff == ['dmCas'], 'beta 3a: routines that differ from beta 3: %s (want dmCas)' % _diff)


def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


check(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 3a: outside those routines only comments differ')
_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)
_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)
check(_py0 == _py1, 'beta 3a: the #PYTHON blocks are unchanged')
say('  routines that differ from beta 3: %s; everything else differs only in comments' % ', '.join(_diff))

check = _saved_check

# ================================================================ R (3b): the round-2 emulator findings
print('\n==== R. 3b: the round-2 emulator findings (harness v3d) ====')
NPASS0 = [0]


def _norm(t):
    t = re.sub(r'//[^\n]*', '', t)
    return '\n'.join(l.rstrip() for l in t.split('\n') if l.strip())


# R1. dmCas with the CAS failing; beta 3a stops
hf = Harness(PROG, strict=True, cas='fail'); hf.call('dmInit')
r = hf.call('dmCas', 'factor(normal(1/(2*dmq1*dmq2)))')
check('R1: dmCas with the CAS failing returns "" with no error', r == '' and hf.error is None, repr(r))
hg = Harness(PROG, strict=True, cas='giac'); hg.call('dmInit')
for q, want in (('factor(normal(1/(2*dmq1*dmq2)))', prime_print(giac_eval('factor(normal(1/(2*dmq1*dmq2)))'))),
                ('1/0', ''), ('0/0', ''), ('limit(1/dmt,dmt,0,1)', '')):
    got = hg.call('dmCas', q)
    check('R1: dmCas(%r) with Giac = %r' % (q, want), got == want, repr(got))
h0 = Harness(B3A, strict=True, cas='fail'); h0.call('dmInit')
try:
    h0.call('dmCas', 'factor(normal(1/(2*dmq1*dmq2)))')
    check('R1: beta 3a dmCas stops on a failed call in v3d', False)
except PPLError as ex:
    check('R1: beta 3a dmCas, the same failed call in v3d, stops on INSTRING', 'INSTRING' in str(ex), str(ex)[:60])

# R2. dmRepl directly: the pattern at the end, at the start, the whole text, empty pattern, empty text
hr = Harness(PROG, strict=True, cas='fail'); hr.call('dmInit')
CASESR = [('1/2/dmq4/dmq3', 'dmq3', 'p14'), ('dmq3*dmt+1', 'dmq3', 'p14'), ('dmq3', 'dmq3', 'p14'),
          ('abc', '', 'X'), ('', 'dmq3', 'p14'), ('(3*dmt+1)*(4*dmt+1)', 'dmt', 'th'), ('a*b*c*', '*', CHAR_TIMES),
          ('dmtdmt', 'dmt', 'th'), ('xyz', 'dmq3', 'p14'), ('ab', 'abc', 'Z'), ('aaa', 'aa', 'b')]
for t_, o_, n_ in CASESR:
    got = hr.call('dmRepl', t_, o_, n_)
    want = t_ if o_ == '' else t_.replace(o_, n_)
    check('R2: dmRepl(%r, %r, %r) = %r' % (t_, o_, n_, want), got == want and hr.error is None, repr(got))
ho = Harness(B3A, strict=True, cas='fail'); ho.call('dmInit')
try:
    ho.call('dmRepl', '1/2/dmq4/dmq3', 'dmq3', 'p14')
    check('R2: beta 3a dmRepl with the pattern at the end stops in v3d', False)
except PPLError as ex:
    check('R2: beta 3a dmRepl with the pattern at the END stops in v3d (INSTRING("", ...))', 'INSTRING' in str(ex), str(ex)[:60])
# the locus page with the CAS answering (giac), and with an answer that ENDS in a symbol (canned):
# the formula view opens; beta 3a stops on the second
_, pres, hp, hd = PRESETS[1]
hx = load(pres, hp, hd, EX_LOCI)
g = hx.globals_
g['dmLab'], g['dmFq'], g['dmGen'], g['dmM'] = ([float(v) for v in EX_LOCI[0][0]], [float(v) for v in EX_LOCI[0][1]],
                                               [float(v) for v in EX_LOCI[0][2]], 4.0)
T1, T0 = hx.call('dmCasLR', 0.0), hx.call('dmCasLR', 1.0)
canned = {'string(' + T1 + ')': '"' + giac_eval(T1) + '"', 'string(' + T0 + ')': '"1/2/dmq4/dmq3"'}
for path in (PROG, B3A):
    hc = Harness(path, strict=True, cas=canned)
    hc.call('dmInit')
    gc = hc.globals_
    gc['dmPres'] = [float(v) for v in pres]; gc['dmHp'] = [float(v) for v in hp]; gc['dmHd'] = [float(v) for v in hd]
    gc['dmLoc'] = [[[float(v) for v in l], [float(v) for v in f], [float(v) for v in gg]] for l, f, gg in EX_LOCI]
    gc['dmInc'] = [1.0] * 3; gc['dmNL'] = 3.0; gc['dmTh'] = 0.01; gc['dmSel'] = 1.0
    hc.call('dmRecalc')
    hc.press('Minus').press('Esc')
    try:
        hc.call('dmLocusPanel')
        err = None
    except PPLError as ex:
        err = ex
    if path == PROG:
        pg = hc.pages[-1]
        check('R2: the formula view with a theta = 0 answer ending in a symbol ("1/2/dmq4/dmq3") opens: '
              '"theta = 0: LR = 1/2/p15/p14", "exact (CAS)"', err is None and pg.has('theta = 0: LR = 1/2/p15/p14')
              and pg.has('exact (CAS)'), str([t.text for t in pg.texts if 96 <= t.y <= 140]))
    else:
        check('R2: beta 3a, the same formula view, stops in dmRepl (INSTRING("", ...))',
              err is not None and 'INSTRING' in str(err), str(err)[:60])
print('  R2 dmRepl: %d cases = Python str.replace (empty pattern: the text unchanged); a formula ending in a symbol'
      ' opens the formula view (beta 3a stops)' % len(CASESR))

# R3. cas='fail' end to end: the stale-key menu run (example, bar, locus page, formula view, quit), and
# the formula view; beta 3a in v3d stops in both
for path in (PROG, B3A):
    hh = Harness(path, strict=False, stale_keys=True, idle_key=4, cas='fail')
    hh.choose(9); hh.choose(5); hh.tap(44 + 40, 100).tap(44 + 40, 100); hh.press('Minus').press('Esc'); hh.choose(12)
    try:
        rr = hh.call('DNAMixLR')
    except PPLError:
        rr = None
    if path == PROG:
        fv = [p for p in hh.pages if p.has('The CAS did not answer: no formula here.')]
        check('R3: beta 3b, cas=fail, menu -> example -> bar -> locus page -> formula view -> Quit: completes, '
              '"decimal" and "did not answer"', hh.error is None and isinstance(rr, str)
              and rr.startswith('DNAMixLR: combined LR = 3981.5') and fv and fv[-1].has('decimal'), repr(rr))
    else:
        check('R3: beta 3a, the same run in v3d, stops on INSTRING', isinstance(hh.error, PPLError)
              and 'INSTRING' in str(hh.error), str(hh.error)[:60])


# R4. the menu fits its box
def _choose_lines(h):
    return [it for c in h.chooses for it in c.items]


hm = Harness(PROG, strict=False, idle_key=4, cas='fail')
hm.choose(9); hm.choose(4); hm.press('Esc'); hm.choose(12)
rm = hm.call('DNAMixLR')
lines = _choose_lines(hm)
check('R4: the menu shows "Results (tap a row to drop)" (27 characters) and item 4 still opens the Results table',
      'Results (tap a row to drop)' in lines and any(p.has('Likelihood ratios by locus') for p in hm.pages)
      and hm.error is None)
over = sorted({t for t in lines if len(t) > 30})
# the first line is built from the hypotheses ("Hypotheses:  V + S, no unknown  vs  V + 1 unknown", 49
# characters) -- not reported cut on the emulator in rounds 1 and 2; listed under Unresolved, not changed
check('R4: every fixed CHOOSE line is 30 characters or fewer (the hypotheses line, built from the '
      'hypotheses, excepted: see Unresolved)', all(t.startswith('Hypotheses:') for t in over), str(over))
srcn = re.sub(r'//[^\n]*', '', open(PROG, encoding='utf-8').read())
srco = re.sub(r'//[^\n]*', '', open(B3A, encoding='utf-8').read())
check('R4: beta 3a had the 36-character line the emulator cut; beta 3b does not (comments aside)',
      '"Results table (tap a row to drop it)"' in srco and '"Results table (tap a row to drop it)"' not in srcn
      and '"Results (tap a row to drop)"' in srcn)
print('  R4 the main menu: %d lines shown, the longest %d ("%s")' % (len(set(lines)), max(len(t) for t in lines),
                                                                  max(lines, key=len)))

# R5. fixed decimals: loci that give an LR of 1.0003 (log10 0.0001) and 0.549, a rare allele (p 0.0004),
# a typed theta of 0.00004; every view, the locus page and its formula view, both CAS modes
LOCI_SMALL = [([10, 11, 12, 13], [0.05, 0.3, 0.05, 0.05], [1, 1, 2, 2, 0, 0]),      # LR 1.0003 (preset 4)
              ([10, 11, 12, 13], [0.05, 0.3, 0.3, 0.05], [1, 2, 1, 2, 0, 0]),       # LR 0.549
              ([20, 21, 22], [0.0004, 0.3, 0.2], [1, 2, 2, 3, 0, 0])]               # a rare allele
# (two loci alone: log10 LR from -0.26 to 0.0001, so the axis runs -0.3, -0.2, -0.1 and a tick that is
#  2.8E-17 in PC arithmetic, not 0; all three: -0.4 .. 0.6 in steps of 0.2)
_, pres4, hp4, hd4 = PRESETS[4]
lr_a = locus_lr(pres4, hp4, hd4, LOCI_SMALL[0][2], LOCI_SMALL[0][1], 0.01)[2]
lr_b = locus_lr(pres4, hp4, hd4, LOCI_SMALL[1][2], LOCI_SMALL[1][1], 0.01)[2]
print('  R5 the loci: LR %.6f (log10 %.6f), %.4f (log10 %.4f), and an allele at p = 0.0004' % (
    lr_a, math.log10(lr_a), lr_b, math.log10(lr_b)))
old_sci = {}
for th, nl in ((0.01, 2), (0.01, 3), (0.00004, 3)):
    for cas in ('giac', 'fail'):
        res = {}
        for path in (PROG, B3A):
            hh = Harness(path, strict=False, idle_key=4, cas=cas)
            hh.call('dmInit')
            gg = hh.globals_
            gg['dmPres'] = [float(v) for v in pres4]; gg['dmHp'] = [float(v) for v in hp4]; gg['dmHd'] = [float(v) for v in hd4]
            gg['dmLoc'] = [[[float(v) for v in l], [float(v) for v in f], [float(v) for v in g_]] for l, f, g_ in LOCI_SMALL[:nl]]
            gg['dmInc'] = [1.0] * nl; gg['dmNL'] = float(nl); gg['dmTh'] = th; gg['dmSel'] = 1.0
            hh.call('dmRecalc')
            err = None
            try:
                for v in (3, 1, 2, 4, 8, 5):
                    hh.press('Esc'); hh.call('dmViews', float(v))
                for sel in range(1, nl + 1):
                    gg['dmSel'] = float(sel)
                    hh.press('Esc'); hh.call('dmLocusPanel')
                    hh.press('Minus').press('Esc'); hh.call('dmLocusPanel')
                    gg['dmFrm'] = 0.0
                ttl = hh.call('dmThS', th)
            except Exception as ex:
                err = ex
            res[path] = (hh, err)
        hn, en = res[PROG]
        check('R5 %d loci, theta %s %s: beta 3b runs every view and the locus pages' % (nl, th, cas), en is None, str(en)[:80])
        check('R5 %d loci, theta %s %s: beta 3b printed no scientific STRING' % (nl, th, cas), hn.sci_strings == [], str(hn.sci_strings[:5]))
        shown = [t.text for p in hn.pages for t in p.texts]
        check('R5 %d loci, theta %s %s: no small-capital E on screen' % (nl, th, cas), not any(u'ᴇ' in s for s in shown))
        ho_, eo = res[B3A]
        for v, d, t in ho_.sci_strings:
            old_sci.setdefault(t, (v, d))
        if cas == 'giac':
            labs = sorted({t.text for t in hn.texts if t.text in ('0.0', '-0.1', '-0.2', '-0.3', '0.1', '0.2')})
            box = sorted({t.text for t in hn.texts if t.text.startswith('.000')})
            print('  R5 %d loci, theta %-7s beta 3b: 0 scientific, %d screens; beta 3a: %d scientific%s' % (
                nl, th, len(hn.pages), len(ho_.sci_strings), ' (stopped: %s)' % str(eo)[:40] if eo else ''))
            if nl == 2:
                old_labs = sorted({t.text for t in ho_.texts if '-17' in t.text})
                check('R5: two loci: the LR-by-locus axis reads -0.3, -0.2, -0.1, 0.0 (beta 3a: %s)' % old_labs,
                      {'-0.3', '-0.2', '-0.1', '0.0'} <= set(labs) and bool(old_labs), str(labs))
                print('      axis labels %s; beta 3a drew %s' % (labs, old_labs))
            elif th == 0.01:
                check('R5: the rare allele\'s box reads ".0004"', '.0004' in box, str(box))
                l3 = [t.text for t in hn.texts if t.text.startswith('log10 LR = ')]
                check('R5: the LR-1.0003 locus: "log10 LR = 0.000"', 'log10 LR = 0.000' in l3, str(l3[:3]))
                print('      axis labels %s; allele box %s; locus page %s' % (labs, box, sorted(set(l3))[:3]))
            else:
                tl = [t.text for t in hn.texts if 'theta = 0.000040' in t.text]
                check('R5: a typed theta of 0.00004 reads "theta = 0.000040"', bool(tl), str(tl[:2]))
print('  R5 beta 3a printed, in these runs:')
for t, (v, d) in sorted(old_sci.items(), key=lambda kv: (kv[1][1], abs(kv[1][0])))[:14]:
    print('      STRING(%.6g, 2, %d) -> %s' % (v, d, t))
check('R5: beta 3a printed scientific strings in these runs (%d)' % len(old_sci), len(old_sci) >= 3)

# R6. dmF and dmThS on edge values
hu = Harness(PROG, strict=True, cas='fail'); hu.call('dmInit')
for v, d, want in ((0.0001287, 3, '0.000'), (-0.00115, 3, '-0.001'), (2.7755575615628914e-17, 1, '0.0'),
                   (-2.7755575615628914e-17, 1, '0.0'), (3.6, 3, '3.600'), (0.0004, 4, '0.0004'), (95.4, 1, '95.4')):
    got = hu.call('dmF', float(v), float(d))
    check('R6: dmF(%r, %d) = %r' % (v, d, want), got == want, repr(got))
for v, want in ((0.01, '0.010'), (0.0125, '0.0125'), (0.0, '0.000'), (0.00004, '0.000040'), (0.000015, '0.000015'),
                (0.03, '0.030'), (0.0001, '0.0001'), (0.00012, '0.0001')):
    got = hu.call('dmThS', float(v))
    check('R6: dmThS(%r) = %r' % (v, want), got == want, repr(got))
check('R6: the helpers printed no scientific STRING', hu.sci_strings == [], str(hu.sci_strings))

# ================================================================ G (3b): beta 3b against beta 3a
print('\n==== G (3b): beta 3b against beta 3a ====')
_t0, _t1 = open(B3A, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()
def _bodies2(txt):
    c = re.sub(r'//[^\n]*', '', txt)
    return {m.group(1): _norm(m.group(0)) for m in re.finditer(
        r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S)}
N0, N1 = _bodies2(_t0), _bodies2(_t1)
d3b = sorted(n for n in set(N0) | set(N1) if N0.get(n) != N1.get(n))
WANT = ['DNAMixLR', 'dmCas', 'dmDrawFx', 'dmDrawLoci', 'dmF', 'dmFxMake', 'dmPicture', 'dmRepl', 'dmThS', 'dmThStatic']
check('G: the routines that differ from beta 3a are exactly %s' % WANT, d3b == WANT, str(d3b))
gl = '  IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;'
check('G: dmCas is the DIM guard only', N1['dmCas'] == N0['dmCas'].replace(gl, '  IF DIM(cR) > 0 THEN\n  ' + gl + '\n  END;'))
check('G: dmF rounds (+ 0), nothing else', N1['dmF'] == N0['dmF'].replace('STRING(fv, 2, fd)', 'STRING(ROUND(fv, fd) + 0, 2, fd)'))
check('G: dmDrawLoci: one label line through dmF', N1['dmDrawLoci'] == N0['dmDrawLoci'].replace(
    'plS := STRING(plV, 2, plDec);', 'plS := dmF(plV, plDec);'))
check('G: dmThStatic: one label line through dmF', N1['dmThStatic'] == N0['dmThStatic'].replace(
    'tsS := STRING(tsV, 2, tsDec);', 'tsS := dmF(tsV, tsDec);'))
check('G: dmPicture: the one ".0004" line', N1['dmPicture'] == N0['dmPicture'].replace(
    '    IF LEFT(apPs, 1) == "0" THEN', '    IF dmFq(apJ) < 0.0005 THEN apPs := dmF(dmFq(apJ), 4); END;\n    IF LEFT(apPs, 1) == "0" THEN'))
fl = '      IF INSTRING(fmR, ".") > 0 THEN fmR := ""; END;'
check('G: dmFxMake: the two DIM guards only', N1['dmFxMake'] == N0['dmFxMake'].replace(
    fl, '      IF DIM(fmR) > 0 THEN\n  ' + fl + '\n      END;'))
check('G: dmDrawFx: the note\'s IF split, nothing else', N1['dmDrawFx'] == N0['dmDrawFx'].replace(
    '      IF fxOn == 1 AND fxY <= 162 AND INSTRING(dmFxT, "*dmt-") > 0 THEN\n        TEXTOUT_P(',
    '      IF fxOn == 1 AND fxY <= 162 AND DIM(dmFxT) > 0 THEN\n        IF INSTRING(dmFxT, "*dmt-") > 0 THEN\n          TEXTOUT_P(').replace(
    'signs pair off", G1, 10, fxY, 1, dmGRAY, 304);\n      END;', 'signs pair off", G1, 10, fxY, 1, dmGRAY, 304);\n        END;\n      END;'))
check('G: DNAMixLR: the one menu line', N1['DNAMixLR'] == N0['DNAMixLR'].replace(
    '"Results table (tap a row to drop it)"', '"Results (tap a row to drop)"'))
check('G: dmRepl is the round-2 brief\'s loop', N1['dmRepl'] == _norm('''dmRepl(rpT, rpO, rpN)
BEGIN
  LOCAL rpR, rpS, rpI, rpK;
  IF DIM(rpO) == 0 THEN RETURN rpT; END;
  rpR := ""; rpS := rpT; rpK := DIM(rpO);
  rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;
  WHILE rpI > 0 DO
    IF rpI > 1 THEN rpR := rpR + LEFT(rpS, rpI - 1); END;
    rpR := rpR + rpN;
    IF rpI + rpK > DIM(rpS) THEN rpS := ""; ELSE rpS := MID(rpS, rpI + rpK); END;
    rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;
  END;
  RETURN rpR + rpS;
END;'''))
def _outside2(t, names):
    c = re.sub(r'//[^\n]*', '', t)
    c = re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return re.sub(r'\s+', ' ', c)
check('G: outside those routines only comments differ', _outside2(_t0, d3b) == _outside2(_t1, d3b))
print('  differ from beta 3a: %s, each exactly as listed' % ', '.join(d3b))

# ================================================================ S
print('\n==== S: h.sci_strings over every beta 3b harness run of this script ====')
_mine = [h_ for h_ in ALL_H if h_._src == PROG]
_sci = [(v, d, t) for h_ in _mine for v, d, t in h_.sci_strings]
check('S: %d beta 3b harness runs, %d scientific STRING results (%d runs of older versions not counted)'
      % (len(_mine), len(_sci), len(ALL_H) - len(_mine)), _sci == [], str(_sci[:8]))

print('\n%d PASS, %d failure(s)' % (NPASS[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
