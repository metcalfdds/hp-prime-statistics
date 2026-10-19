#!/usr/bin/env python3
"""verify_DNAMixLR_beta3c.py -- DNAMixLR beta 3c (19 Oct 2026): B1, B2 and B4 of the fleet review of
19 Oct 2026 (findings_E).  Built from verify_DNAMixLR_beta3b.py: every check is kept and runs on beta 3c,
now in harness ppl_run_v3e (v3d's results; v3e adds only the exponent's Unicode minus with
home_minus=True, which this script does not set).  The predecessors are read from /home/claude/work/out
by absolute path (review item 22).  Part G (3b), beta 3b against beta 3a, keeps reading those two files.
New, after part R:
  V1 B1: the custom hypotheses.  A refused unknown count (5 or -1, under Hp or under Hd) changes
     nothing -- dmHp, dmHd, dmPres, the loci and the menu line stay as they were; beta 3b keeps the
     refused count.  The yes/no answers are stored as 1 or 0 (a typed 2 is "no"); beta 3b stored the 2.
     A valid custom pair still works end to end (stored, loci recomputed = the Python engine).
  V2 B2: the reason for an LR of 0, on the locus page and in its formula view: a known's allele outside M;
     too few unknowns to supply M (the review's V 12/13 + S 14/14); a true underflow (p = 1E-100).  Beta 3b gives the
     first sentence for all three.  A random sweep: the reason shown for every LR = 0 locus is the one the
     Python engine finds, and every LR equals the exact one.  "1 allele", not "1 alleles".
  V3 B4: help page 2 reads "LR 2-10 weak", and dmVerbal and dmBand put the edge at 2.
  V6 dmProb without cancellation (3c): the per-allele sum of positive terms equals the inclusion-exclusion sum
     EXACTLY in fractions (1,500 random loci); the PPL dmProb = exact fractions over every preset and custom
     pair, the CASES genotypes, ordinary and rare frequencies, theta 0-0.3, |U| up to 8, and = brute force;
     in a 12-digit model beta 3c keeps ~10 digits where beta 3b's sum is off by orders of magnitude; the two
     cases that cancelled (exact LR 6.64E-7 and 3.6E5) end to end, beta 3b's EXCLUDED / 'Hd cannot' beside
     them; the work at the limits and the harness time.  V2's sweep also checks every LR by value.
  V5 the teaching-aid notice (Roger, 19 Oct 2026, 12:48): the DISCLAIMER line in the header; on screen, in red,
     "Teaching aid; not for casework or legal use." on help page 1, the Results table, every locus page and the
     fallacy page, "Teaching aid only" in the title row of the three plots -- inside the screen and clear of
     every other text by a 6.5 / 7.6 px-per-character model, in five states; beta 3b shows neither; a tap on
     the locus plot's title still switches to the waterfall.
  V4 the review's check_DNAMixLR.py, run on beta 3c and on beta 3b: every check beta 3b failed passes,
     except the seven that wait on open decisions (the Hypotheses wording, D17; dmBig's "10.00E-3", B5,
     not in this pass), and the only checks beta 3c "fails" are the five that recorded the bugs.
  G (3c) beta 3c against beta 3b: exactly dmSetHyp, dmDrawFx, dmDrawPanel, dmHelpPage (B1, B2, B4) and, for
     the notice, dmCombLines, dmDrawFall, dmDrawLoci, dmThStatic and dmLadFrame differ, each by exactly the
     change listed; the banner and the header paragraph; at most 6 names per LOCAL.
  S (kept) covers every beta 3c run in the script, V included.

(The beta 3b description follows.)

verify_DNAMixLR_beta3b.py -- DNAMixLR beta 3b (17 Oct 2026): the round-2 emulator fixes.
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
from ppl_run_v3e import Harness as _HarnessV3d, giac_eval, prime_print, PPLError  # noqa: E402  (3c: v3e)
from ppl_run_v3e import HarnessStall  # noqa: E402

ALL_H = []          # 3b: every harness made in this script, for the sci_strings audit (S)
CHAR_TIMES = chr(215)


class Harness(_HarnessV3d):
    def __init__(self, paths=None, *a, **k):
        _HarnessV3d.__init__(self, paths, *a, **k)
        self._src = paths
        ALL_H.append(self)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/claude/work/out'          # 3c: the predecessors, by absolute path (review item 22)
PROG = os.path.join(HERE, 'DNAMixLR_beta3c.txt')
B3B = os.path.join(OUT, 'DNAMixLR_beta3b.txt')
B3A = os.path.join(OUT, 'DNAMixLR_beta3a.txt')
BETA3 = os.path.join(OUT, 'DNAMixLR_beta3.txt')
BASE = os.path.join(OUT, 'DNAMixLR_beta2.txt')
for _p in (PROG, B3B, B3A, BETA3, BASE):
    if not os.path.exists(_p):
        print('MISSING ' + _p)
        sys.exit(2)
SCR = '/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad'
os.makedirs(SCR, exist_ok=True)
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
# 3c: dmProb left this list -- its inclusion-exclusion sum cancelled (part V6), so it is rewritten and checked
# by value against exact fractions instead; the expected "byte for byte beta 2" was the bug
for nm in ('dmKnowns', 'dmTyped', 'dmEval'):
    pat = re.compile(r'^' + nm + r'\(.*?\)\nBEGIN\n.*?^END;\n', re.S | re.M)
    check('%s byte-for-byte beta 2' % nm, pat.search(src3).group(0) == pat.search(src2).group(0))
pat = re.compile(r'^dmProb\(.*?\)\nBEGIN\n.*?^END;\n', re.S | re.M)
check('3c: dmProb is NOT beta 2\'s any more (rewritten without cancellation; part V6 checks it by value)',
      pat.search(src3).group(0) != pat.search(src2).group(0))

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
print('\n==== R. 3b: the round-2 emulator findings, run on beta 3c (harness v3e) ====')
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
        check('R3: beta 3c, cas=fail, menu -> example -> bar -> locus page -> formula view -> Quit: completes, '
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
check('R4: beta 3a had the 36-character line the emulator cut; beta 3c does not (comments aside)',
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
        check('R5 %d loci, theta %s %s: beta 3c runs every view and the locus pages' % (nl, th, cas), en is None, str(en)[:80])
        check('R5 %d loci, theta %s %s: beta 3c printed no scientific STRING' % (nl, th, cas), hn.sci_strings == [], str(hn.sci_strings[:5]))
        shown = [t.text for p in hn.pages for t in p.texts]
        check('R5 %d loci, theta %s %s: no small-capital E on screen' % (nl, th, cas), not any(u'ᴇ' in s for s in shown))
        ho_, eo = res[B3A]
        for v, d, t in ho_.sci_strings:
            old_sci.setdefault(t, (v, d))
        if cas == 'giac':
            labs = sorted({t.text for t in hn.texts if t.text in ('0.0', '-0.1', '-0.2', '-0.3', '0.1', '0.2')})
            box = sorted({t.text for t in hn.texts if t.text.startswith('.000')})
            print('  R5 %d loci, theta %-7s beta 3c: 0 scientific, %d screens; beta 3a: %d scientific%s' % (
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
print('\n==== G (3b): beta 3b against beta 3a (3c: kept on those two files) ====')
_t0, _t1 = open(B3A, encoding='utf-8').read(), open(B3B, encoding='utf-8').read()
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

# ================================================================ V (3c): the fleet review of 19 Oct 2026
print('\n==== V (3c): the fleet review of 19 Oct 2026 -- B1, B2, B4 (harness v3e) ====')
from fractions import Fraction as _Fr


def _load_into(h, pres, hp, hd, loci, th=0.01):
    g = h.globals_
    g['dmPres'] = [float(v) for v in pres]; g['dmHp'] = [float(v) for v in hp]; g['dmHd'] = [float(v) for v in hd]
    g['dmLoc'] = [[[float(v) for v in l], [float(v) for v in f], [float(v) for v in gg]] for l, f, gg in loci]
    g['dmInc'] = [1.0] * len(loci); g['dmNL'] = float(len(loci)); g['dmTh'] = float(th); g['dmSel'] = 1.0
    g['dmCvOK'] = 0.0; g['dmEdOK'] = 0.0
    h.call('dmRecalc')


def _custom(path, typed_ans, hp_ans, hd_ans):
    """the worked example under preset 1, then Hypotheses > Custom with the three forms answered"""
    h = Harness(path, strict=True, cas='fail')
    h.call('dmInit')
    _load_into(h, *PRESETS[1][1:], EX_LOCI)
    before = {k: list(h.globals_[k]) if isinstance(h.globals_[k], list) else h.globals_[k]
              for k in ('dmPres', 'dmHp', 'dmHd', 'dmLR', 'dmNL')}
    h.choose(5)
    h.answer(typed_ans); h.answer(hp_ans); h.answer(hd_ans)
    h.call('dmSetHyp')
    return h, before


# ---- V1, B1: a refused unknown count changes nothing; the yes/no answers are 1 or 0
print('-- V1 (B1): the custom hypotheses --')
T_OK = {'cuV': 1, 'cuS': 1, 'cuT': 0}
REFUSED = [('Hp 5 unknowns', {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 5}, {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': 1}, 3, 5),
           ('Hp -1 unknowns', {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': -1}, {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': 1}, 3, -1),
           ('Hd 5 unknowns', {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 0}, {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': 5}, 4, 5),
           ('Hd -1 unknowns', {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 0}, {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': -1}, 4, -1),
           ('Hp 4.7 unknowns, Hd 5 (IP(4.7) = 4 is fine, 5 is not)', {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 4.7},
            {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': 5}, 4, 5)]
for nm, hpa, hda, which, val in REFUSED:
    hn, bn = _custom(PROG, T_OK, hpa, hda)
    gn = hn.globals_
    box = [m.lines[0] for m in hn.msgboxes]
    # the next recalculation (a theta change, a new locus) works with what is stored
    hn.call('dmRecalc')
    check('V1 B1: %s refused: the "0 to 4" box, and dmHp, dmHd, dmPres, dmNL and every LR (after a recalculation) '
          'exactly as before' % nm, box == ['Unknown contributors: 0 to 4 under each hypothesis.']
          and gn['dmHp'] == bn['dmHp'] and gn['dmHd'] == bn['dmHd'] and gn['dmPres'] == bn['dmPres']
          and gn['dmNL'] == bn['dmNL'] and gn['dmLR'] == bn['dmLR'] and hn.error is None,
          'dmHp %s dmHd %s LR %s' % (gn['dmHp'], gn['dmHd'], gn['dmLR']))
    ho_, bo = _custom(B3B, T_OK, hpa, hda)
    kept = (ho_.globals_['dmHp'] if which == 3 else ho_.globals_['dmHd'])[3]
    ho_.call('dmRecalc')
    check('V1 B1: ... beta 3b, the same: the box, but the refused %s is KEPT (%s(4) = %s), and the next '
          'recalculation uses it (LRs %s)' % (val, 'dmHp' if which == 3 else 'dmHd', kept,
                                              ['%.4g' % v for v in ho_.globals_['dmLR']]),
          len(ho_.msgboxes) == 1 and kept == float(val) and ho_.globals_['dmLR'] != bo['dmLR'])
# the typed persons changed in the first form, then a refused count: nothing changes, nothing is cleared
hn, bn = _custom(PROG, {'cuV': 1, 'cuS': 1, 'cuT': 1}, {'cuV': 1, 'cuS': 1, 'cuT': 1, 'cuX': 5},
                 {'hdV': 1, 'hdS': 0, 'hdT': 1, 'hdX': 1})
check('V1 B1: a third person typed AND a refused count: dmPres stays {1, 1, 0}, the 3 loci are not cleared, one box',
      hn.globals_['dmPres'] == [1.0, 1.0, 0.0] and hn.globals_['dmNL'] == 3.0 and len(hn.msgboxes) == 1
      and hn.globals_['dmHp'] == bn['dmHp'], str(hn.globals_['dmPres']))
# the review's reproduction through the menu: example, Hypotheses > Custom > Hp 5 > Hd 1, then Quit
for path in (PROG, B3B):
    hm_ = Harness(path, strict=True, cas='fail')
    hm_.choose(9, 1, 5)
    hm_.answer(T_OK, {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 5}, {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': 1})
    hm_.choose(12)
    rr = hm_.call('DNAMixLR')
    first = hm_.chooses[-1].items[0]
    if path == PROG:
        check('V1 B1: through the menu (example, Custom, Hp 5): the menu still reads "%s" and Quit returns %r'
              % (first, rr), first == 'Hypotheses:  V + S, no unknown  vs  V + 1 unknown'
              and rr.startswith('DNAMixLR: combined LR = 3981.5'))
    else:
        check('V1 B1: ... beta 3b, the same run: the menu reads "%s" (the refused count shown as the hypothesis)'
              % first, '5 unknowns' in first)
# the yes/no answers: a typed 2 is "no" (1 or 0 stored), in the typed-persons form and in Hp / Hd
hn, bn = _custom(PROG, {'cuV': 2, 'cuS': 1, 'cuT': 0}, {'cuV': 2, 'cuS': 1, 'cuT': 0, 'cuX': 1},
                 {'hdV': 1, 'hdS': 0.5, 'hdT': 0, 'hdX': 2})
ho_, bo = _custom(B3B, {'cuV': 2, 'cuS': 1, 'cuT': 0}, {'cuV': 2, 'cuS': 1, 'cuT': 0, 'cuX': 1},
                  {'hdV': 1, 'hdS': 0.5, 'hdT': 0, 'hdX': 2})
check('V1 B1: "Victim typed? = 2" is stored as 0 (dmPres = %s), Hp\'s 2 as 0 and Hd\'s 1 as 1 (dmHp %s, dmHd %s); '
      'every flag is 0 or 1' % (hn.globals_['dmPres'], hn.globals_['dmHp'], hn.globals_['dmHd']),
      hn.globals_['dmPres'] == [0.0, 1.0, 0.0] and hn.globals_['dmHp'] == [0.0, 1.0, 0.0, 1.0]
      and hn.globals_['dmHd'] == [1.0, 0.0, 0.0, 2.0])
check('V1 B1: ... beta 3b stored the 2s (dmPres %s, dmHp %s)' % (ho_.globals_['dmPres'], ho_.globals_['dmHp']),
      ho_.globals_['dmPres'] == [2.0, 1.0, 0.0] and ho_.globals_['dmHp'][0] == 2.0)
# a valid custom pair (preset 4 written by hand) is stored and every locus is recomputed = the engine
hn, bn = _custom(PROG, T_OK, {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 1}, {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': 2})
want = [locus_lr([1, 1, 0], [1, 1, 0, 1], [1, 0, 0, 2], gen, fq, 0.01)[2] for lab, fq, gen in EX_LOCI]
check('V1 B1: a valid custom pair (V + S + 1U vs V + 2U) is stored, no box, the 3 loci kept and recomputed = '
      'the Python engine (%s)' % ['%.4f' % v for v in hn.globals_['dmLR']],
      hn.globals_['dmHp'] == [1.0, 1.0, 0.0, 1.0] and hn.globals_['dmHd'] == [1.0, 0.0, 0.0, 2.0]
      and not hn.msgboxes and hn.globals_['dmNL'] == 3.0
      and all(rel(a, b) < 1e-12 for a, b in zip(hn.globals_['dmLR'], want)))
# 4 unknowns under each is the edge that is still accepted; cancelling a form changes nothing
hn, bn = _custom(PROG, T_OK, {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 4}, {'hdV': 1, 'hdS': 0, 'hdT': 0, 'hdX': 4})
check('V1 B1: 4 and 4 unknowns are accepted (dmHp %s, dmHd %s)' % (hn.globals_['dmHp'], hn.globals_['dmHd']),
      hn.globals_['dmHp'][3] == 4.0 and hn.globals_['dmHd'][3] == 4.0 and not hn.msgboxes)
from ppl_run_v3e import CANCEL as _CANCEL  # noqa: E402
hn, bn = _custom(PROG, T_OK, {'cuV': 1, 'cuS': 1, 'cuT': 0, 'cuX': 2}, _CANCEL)
check('V1 B1: the Hd form cancelled: nothing changes', hn.globals_['dmHp'] == bn['dmHp'] and hn.globals_['dmHd'] == bn['dmHd'])

# ---- V2, B2: the reason for an LR of 0
print('-- V2 (B2): the reason for an LR of 0 --')
REASON_TXT = {
    1: (['LR = 0: a known contributor under Hp has an', 'allele the mixture does not show.  Excluded.'],
        ['LR = 0 for every p and theta: a known', 'contributor under Hp has an allele the',
         'mixture does not show, so P(E|Hp) = 0.']),
    2: (['LR = 0: under Hp the contributors cannot', 'account for every allele of M.  Excluded.'],
        ['LR = 0 for every p and theta: under Hp', 'the contributors cannot account for every',
         'allele of M, so P(E|Hp) = 0.']),
    0: (['LR = 0: P(E|Hp) underflows: it is below the', "calculator's smallest number.  Counted as 0."],
        ['LR = 0 at these p and theta: P(E|Hp) is', 'below the smallest number the calculator',
         'holds (underflow), so it counts as 0.'])}
ALL_REASON_LINES = set(s for v in REASON_TXT.values() for part in v for s in part)


def _reason_py(pres, hp, gen, m):
    kn = knowns(hp, pres, gen)
    if any(k == 0 for k in kn):
        return 1
    if len([i for i in range(1, m + 1) if i not in kn]) > 2 * hp[3]:
        return 2
    return 0


def _pages(path, pres, hp, hd, loci, th, sels):
    """the locus page of each locus in sels, picture view then formula view: {sel: (pic texts, fx texts)}"""
    h = Harness(path, strict=True, cas='fail')
    h.call('dmInit')
    _load_into(h, pres, hp, hd, loci, th)
    out = {}
    for s in sels:
        res = []
        for frm in (0.0, 1.0):
            h.globals_['dmSel'] = float(s); h.globals_['dmFrm'] = frm
            h.press('Esc'); h.call('dmLocusPanel')
            res.append([t.text for t in h.pages[-1].texts])
        out[s] = res
    return h, out


def bf_brute(x, knowns_, typed_, fq, th):
    """every order of the 2x unknown alleles over the alleles of M plus 'outside M', NRC II conditionals (3c)"""
    import itertools
    m = len(fq)
    p = [1.0 - sum(fq)] + list(fq)
    if any(k == 0 for k in knowns_):
        return 0.0
    need = set(range(1, m + 1)) - set(knowns_)
    if x == 0:
        return 1.0 if not need else 0.0
    base = [0] * (m + 1)
    for a in typed_:
        base[a] += 1
    total = 0.0
    for seq in itertools.product(range(m + 1), repeat=2 * x):
        if 0 in seq or not need.issubset(seq):
            continue
        cnt, n, pr = list(base), len(typed_), 1.0
        for a in seq:
            pr *= (cnt[a] * th + (1 - th) * p[a]) / (1 + (n - 1) * th)
            cnt[a] += 1
            n += 1
        total += pr
    return total


def _exact_prob(x, kn, ty, fq, th):
    """dm_prob in exact rational arithmetic (fq, th as Fractions)"""
    m = len(fq)
    if any(k == 0 for k in kn):
        return _Fr(0)
    U = [i for i in range(1, m + 1) if i not in kn]
    if len(U) > 2 * x:
        return _Fr(0)
    if x == 0:
        return _Fr(1)
    nT = len(ty); t = [0] * (m + 1)
    for a in ty:
        if a > 0:
            t[a] += 1
    pM, tM, tot = sum(fq, _Fr(0)), sum(t[1:]), _Fr(0)
    for mask in range(2 ** len(U)):
        pA, tA, nS = pM, tM, 0
        for i, u in enumerate(U):
            if mask >> i & 1:
                nS += 1; pA -= fq[u - 1]; tA -= t[u]
        term = _Fr(1)
        for j in range(2 * x):
            term = term * ((tA + j) * th + (1 - th) * pA) / (1 + (nT + j - 1) * th)
        tot += -term if nS % 2 else term
    return tot


C_FQ = ['0.6', '0.0001', '0.0005', '0.0002', '0.0002', '0.0005', '0.0001']
V2_CASES = [
    (1, 'a known\'s allele outside M (suspect 14/out)', [1, 1, 0], [1, 1, 0, 0], [1, 0, 0, 1],
     ([12, 13, 14, 15], [0.10, 0.20, 0.15, 0.05], [1, 2, 3, 0, 0, 0]), 0.01),
    (2, 'the review\'s case: V 12/13 + S 14/14 cannot explain {12, 13, 14, 15}', [1, 1, 0], [1, 1, 0, 0],
     [1, 0, 0, 1], ([12, 13, 14, 15], [0.10, 0.20, 0.15, 0.05], [1, 2, 3, 3, 0, 0]), 0.01),
    (2, 'S + 1U cannot supply 3 more alleles', [0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 3],
     ([10, 11, 12, 13, 14], [0.1, 0.1, 0.1, 0.1, 0.1], [0, 0, 1, 1, 0, 0]), 0.0),
    (0, 'a true underflow: four alleles at p = 1E-100 that S + 2U must draw (V + T + 1U carry them), theta 0',
     [1, 1, 1], [0, 1, 0, 2], [1, 0, 1, 1], ([10, 11, 12, 13, 14], [0.6] + [1e-100] * 4, [2, 3, 1, 1, 4, 5]), 0.0),
]
for reason, nm, pres, hp, hd, locus, th in V2_CASES:
    hn, pn = _pages(PROG, pres, hp, hd, [locus], th, [1])
    ho_, po = _pages(B3B, pres, hp, hd, [locus], th, [1])
    lr_n = hn.globals_['dmLR'][0]
    pic, fx = pn[1]
    want_pic, want_fx = REASON_TXT[reason]
    ok_n = lr_n == 0 and all(s in pic for s in want_pic) and all(s in fx for s in want_fx) \
        and not any(s in pic + fx for s in ALL_REASON_LINES - set(want_pic) - set(want_fx))
    check('V2 B2: %s: LR = 0, reason %d (Python: %d): the page and the formula view say %r'
          % (nm, reason, _reason_py(pres, hp, locus[2], len(locus[0])), want_pic[0]),
          ok_n and _reason_py(pres, hp, locus[2], len(locus[0])) == reason, str([s for s in pic if 'LR = 0' in s]))
    o_pic, o_fx = po[1]
    if reason == 1:
        check('V2 B2: ... beta 3b says the same here (the one case its sentence fits)',
              REASON_TXT[1][0][0] in o_pic and REASON_TXT[1][1][0] in o_fx)
    else:
        check('V2 B2: ... beta 3b says "a known contributor under Hp has an allele the mixture does not show" here',
              REASON_TXT[1][0][0] in o_pic and REASON_TXT[1][1][1] in o_fx)
    if reason == 0:
        kn = knowns(hp, pres, locus[2]); ty = typed(pres, locus[2])
        fqF = [_Fr(6, 10)] + [_Fr(1, 10 ** 100)] * 4
        Pe = _exact_prob(hp[3], kn, ty, fqF, _Fr(0))
        check('V2 B2: ... and it IS an underflow: exact P(E|Hp) = 24E-400 > 0, below the smallest double (and the Prime '
              'holds down to 1E-499, so on the calculator this locus would not underflow), P(E|Hd) = %.4g'
              % hn.globals_['dmPd'][0], Pe == _Fr(24, 10 ** 400) and hn.globals_['dmPp'][0] == 0.0
              and hn.globals_['dmPd'][0] > 0)
# "1 allele" / "2 alleles" in the caption under the boxes
_, pn = _pages(PROG, [1, 1, 0], [1, 1, 0, 0], [1, 0, 0, 1],
               [([12, 13, 14, 15], [0.1, 0.2, 0.15, 0.05], [1, 2, 3, 3, 0, 0]),
                ([12, 13, 14, 15, 16], [0.1, 0.2, 0.15, 0.05, 0.1], [1, 2, 3, 3, 0, 0])], 0.01, [1, 2])
_, po = _pages(B3B, [1, 1, 0], [1, 1, 0, 0], [1, 0, 0, 1],
               [([12, 13, 14, 15], [0.1, 0.2, 0.15, 0.05], [1, 2, 3, 3, 0, 0])], 0.01, [1])
check('V2: the caption reads "0 unknown(s) cannot supply 1 allele: P = 0" and "... 2 alleles: P = 0" '
      '(beta 3b: "1 alleles")', '0 unknown(s) cannot supply 1 allele: P = 0' in pn[1][0]
      and '0 unknown(s) cannot supply 2 alleles: P = 0' in pn[2][0]
      and '0 unknown(s) cannot supply 1 alleles: P = 0' in po[1][0])
# a sweep: random loci under seven hypothesis pairs; every LR = 0 locus shows the reason the engine finds
SWEEP_H = [PRESETS[1][1:], PRESETS[2][1:], PRESETS[4][1:], PRESETS[5][1:], PRESETS[6][1:],
           ([1, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]), ([1, 1, 0], [0, 1, 0, 4], [1, 0, 0, 4]),
           ([1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 2])]
rnd = random.Random(20261019)
counts, bad, nl0, npg = {0: 0, 1: 0, 2: 0}, [], 0, 0
nval, n_ie0, badval = 0, 0, []
for pres, hp, hd in SWEEP_H:
    for batch in range(4):
        loci = []
        for k in range(12):
            m = rnd.choice([2, 3, 4, 5, 6, 7])
            gen = [rnd.choice([0] + list(range(1, m + 1)) * 4) if pres[w // 2] == 1 else 0 for w in range(6)]
            if hp[3] == 4 and rnd.random() < 0.6:
                # the shape that cancelled in beta 3b: S on the one common allele, the victim on rare ones,
                # the other rare alleles left for the 4 unknowns under Hp
                m = 7
                fq = [0.6] + [rnd.choice([0.0001, 0.0002, 0.0005]) for _ in range(m - 1)]
                gen = [rnd.randint(2, 7), rnd.randint(2, 7), 1, 1, 0, 0]
            else:
                fq = rand_freqs(m)
            loci.append(([10 + i for i in range(m)], fq, gen))
        th = 0.0 if hp[3] == 4 else rnd.choice([0.0, 0.01])
        h = Harness(PROG, strict=True, cas='fail')
        h.call('dmInit')
        _load_into(h, pres, hp, hd, loci, th)
        # 3c: every locus's LR against exact rational arithmetic (the inclusion-exclusion sum in fractions)
        for (lab, fq, gen), got in zip(loci, h.globals_['dmLR']):
            fqF = [_Fr(repr(v)) for v in fq]; thF = _Fr(repr(th)); ty = typed(pres, gen)
            Pe = _exact_prob(hp[3], knowns(hp, pres, gen), ty, fqF, thF)
            De = _exact_prob(hd[3], knowns(hd, pres, gen), ty, fqF, thF)
            want = -1.0 if De == 0 else float(Pe / De)
            nval += 1
            if want > 0 and dm_prob(hp[3], knowns(hp, pres, gen), ty, fq, th) <= 0:
                n_ie0 += 1
            if not (got == want or (want > 0 and got > 0 and abs(got - want) <= 1e-9 * want)):
                badval.append((pres, hp, hd, fq, gen, th, got, want))
        zs = [i + 1 for i, v in enumerate(h.globals_['dmLR']) if v == 0]
        if not zs:
            continue
        _, pg_ = _pages(PROG, pres, hp, hd, loci, th, zs)
        for s in zs:
            lab, fq, gen = loci[s - 1]
            r = _reason_py(pres, hp, gen, len(lab))
            nl0 += 1; npg += 2
            counts[r] += 1
            pic, fx = pg_[s]
            if not (all(t in pic for t in REASON_TXT[r][0]) and all(t in fx for t in REASON_TXT[r][1])):
                bad.append((s, r, [t for t in pic if 'LR = 0' in t]))
print('  V2 sweep: %d loci with LR = 0 (reason 1: %d, reason 2: %d, underflow: %d), %d pages; %d loci checked by '
      'value, %d of them positive loci that beta 3b\'s inclusion-exclusion (in doubles) made 0' % (
          nl0, counts[1], counts[2], counts[0], npg, nval, n_ie0))
check('V2 B2: a sweep of %d LR = 0 loci under 8 hypothesis pairs: every page and formula view gives the reason the '
      'Python engine finds (1: %d, 2: %d), and none is left without a rule (no underflow at these frequencies)'
      % (nl0, counts[1], counts[2]), not bad and counts[1] > 0 and counts[2] > 0 and counts[0] == 0, str(bad[:3]))
check('V2 (3c): every one of the %d loci of that sweep has the exact LR (fractions; 1E-9 relative), including the %d '
      'that beta 3b\'s cancelling sum made 0' % (nval, n_ie0), not badval and n_ie0 > 0, str(badval[:2]))


# ---- V6 (3c): dmProb without cancellation
print('-- V6 (3c): dmProb adds without subtracting --')
import time as _time


def dp_py(x, kn, ty, fq, th, R=lambda v: v, one=1.0, zero=0.0):
    """beta 3c's dmProb, line for line: the per-allele sum of positive terms.  R rounds each operation (the
    12-digit model below); with fractions it is exact."""
    m = len(fq)
    if any(k == 0 for k in kn):
        return zero
    inU = [1] * (m + 1)
    for k in kn:
        inU[k] = 0
    if sum(inU[1:]) > 2 * x:
        return zero
    if x == 0:
        return one
    N = 2 * x
    nT = len(ty)
    t = [0] * (m + 1)
    for a in ty:
        if a > 0:
            t[a] += 1
    W = [zero] * (N + 1)
    W[0] = one
    for a in range(1, m + 1):
        G = [one] * (N + 1)
        for k in range(1, N + 1):
            G[k] = R(R(G[k - 1] * R(R((t[a] + k - 1) * th) + R(R(1 - th) * fq[a - 1]))) / k)
        lo = 1 if inU[a] else 0
        V = [zero] * (N + 1)
        for s_ in range(N + 1):
            if W[s_] > 0:
                for k in range(lo, N - s_ + 1):
                    V[s_ + k] = R(V[s_ + k] + R(W[s_] * G[k]))
        W = V
    tot = W[N]
    for j in range(1, N + 1):
        tot = R(R(tot * j) / R(1 + R((nT + j - 2) * th)))
    return tot


def r12(v):
    """round to 12 significant digits: a crude model of the Prime's reals (after every operation)"""
    if v == 0 or not math.isfinite(v):
        return v
    e = math.floor(math.log10(abs(v)))
    q = 10 ** (11 - e)
    return round(v * q) / q


def ie12(x, kn, ty, fq, th):
    """beta 3b's inclusion-exclusion with every operation rounded to 12 digits (the review's bcd12 model)"""
    m = len(fq)
    if any(k == 0 for k in kn):
        return 0.0
    U = [i for i in range(1, m + 1) if i not in kn]
    if len(U) > 2 * x:
        return 0.0
    if x == 0:
        return 1.0
    nT = len(ty)
    t = [0] * (m + 1)
    for a in ty:
        if a > 0:
            t[a] += 1
    pM = 0.0
    for v in fq:
        pM = r12(pM + v)
    tM, tot = sum(t[1:]), 0.0
    for mask in range(2 ** len(U)):
        pA, tA, nS = pM, tM, 0
        for i, u in enumerate(U):
            if mask >> i & 1:
                nS += 1; pA = r12(pA - fq[u - 1]); tA -= t[u]
        term = 1.0
        for j in range(2 * x):
            term = r12(term * r12(r12(r12((tA + j) * th) + r12(r12(1 - th) * pA)) / r12(1 + r12((nT + j - 1) * th))))
        tot = r12(tot - term) if nS % 2 else r12(tot + term)
    return max(0.0, tot)


def ppl_prob(h, x, kn, ty, fq, th):
    h.globals_['dmFq'] = [float(v) for v in fq]
    h.globals_['dmM'] = float(len(fq))
    h.globals_['dmTh'] = float(th)
    return h.call('dmProb', float(x), [float(v) for v in kn], [float(v) for v in ty])


hN = Harness(PROG, strict=True, cas='fail'); hN.call('dmInit')
hO = Harness(B3B, strict=True, cas='fail'); hO.call('dmInit')
# (1) the algorithm is the inclusion-exclusion sum rearranged: equal in exact fractions
rv = random.Random(1019)
n_id = 0
id_bad = []
for trial in range(1500):
    m = rv.randint(1, 8)
    fqF = [_Fr(rv.choice([1, 2, 5, 10, 50, 100, 300, 1000, 2000]), 10000) for _ in range(m)]
    if sum(fqF) > 1:
        continue
    kn = [rv.randint(0 if rv.random() < 0.1 else 1, m) for _ in range(rv.choice([0, 2, 4, 6]))]
    ty = kn + [rv.randint(0, m) for _ in range(rv.choice([0, 2]))] or [rv.randint(1, m), rv.randint(1, m)]
    x = rv.randint(0, 4)
    th = _Fr(rv.choice([0, 1, 10, 30, 100, 300, 499]), 1000)
    n_id += 1
    if dp_py(x, kn, ty, fqF, th, one=_Fr(1), zero=_Fr(0)) != _exact_prob(x, kn, ty, fqF, th):
        id_bad.append((x, kn, ty, th))
check('V6: the per-allele sum equals the inclusion-exclusion sum EXACTLY, in fractions, in %d random loci '
      '(1-8 alleles, 0-4 unknowns, theta 0 to 0.499, knowns inside and outside M)' % n_id, not id_bad, str(id_bad[:2]))
# (2) the PPL dmProb (harness) against exact fractions: every preset and custom pair of this script, the CASES
# genotypes, the review's seventh pair, a random sweep, |U| up to 8 with 4 unknowns, and the rare-allele loci
PAIRS = [v[1:] for k, v in sorted(PRESETS.items())] + [([1, 1, 0], [1, 1, 0, 2], [1, 0, 0, 3]),
                                                       ([1, 1, 0], [0, 1, 0, 4], [1, 0, 0, 4]),
                                                       ([1, 1, 0], [1, 1, 0, 3], [1, 0, 0, 4])]
cases6 = []
for pr, m, gen in CASES:
    cases6.append((PRESETS[pr][1:], m, gen))
for pair in PAIRS:
    for m in (2, 4, 6, 8):
        for k in range(3):
            pres_ = pair[0]
            gen = [rv.choice([0] + list(range(1, m + 1)) * 4) if pres_[w // 2] == 1 else 0 for w in range(6)]
            cases6.append((pair, m, gen))
nP, worst6, bad6, maxU = 0, 0.0, [], 0
for (pres_, hp_, hd_), m, gen in cases6:
    for fqmode in ('ordinary', 'rare'):
        if fqmode == 'ordinary':
            fqF = [_Fr(rv.choice([100, 300, 500, 1000, 1500]), 10000) for _ in range(m)]
        else:
            fqF = [_Fr(6, 10)] + [_Fr(rv.choice([1, 2, 5]), 10000) for _ in range(m - 1)]
        if sum(fqF) > 1:
            continue
        for th in (_Fr(0), _Fr(1, 100), _Fr(3, 100), _Fr(3, 10)):
            ty = typed(pres_, gen)
            for H in (hp_, hd_):
                kn = knowns(H, pres_, gen)
                ex = _exact_prob(H[3], kn, ty, fqF, th)
                got = ppl_prob(hN, H[3], kn, ty, fqF, th)
                nP += 1
                maxU = max(maxU, len([i for i in range(1, m + 1) if i not in kn]) if H[3] else 0)
                if ex == 0:
                    if got != 0:
                        bad6.append(('zero', m, gen, H, th, got))
                else:
                    e = abs(got - float(ex)) / float(ex)
                    worst6 = max(worst6, e)
                    if e > 1e-12:
                        bad6.append((m, gen, H, float(th), got, float(ex)))
# |U| = 8 with 4 unknowns (no knowns: 8 alleles, all from the unknowns), the program's largest case
for th in (_Fr(0), _Fr(1, 100), _Fr(499, 1000)):
    fqF = [_Fr(1, 10)] * 8
    ex = _exact_prob(4, [], [1, 2], fqF, th)
    got = ppl_prob(hN, 4, [], [1, 2], fqF, th)
    nP += 1
    maxU = max(maxU, 8)
    worst6 = max(worst6, abs(got - float(ex)) / float(ex))
check('V6: the PPL dmProb (harness) = exact fractions in %d evaluations -- %d preset/custom pairs, every CASES '
      'genotype, ordinary and rare frequencies, theta 0 to 0.3, |U| up to %d: worst relative difference %.1e'
      % (nP, len(PAIRS), maxU, worst6), not bad6 and worst6 < 1e-12 and maxU == 8, str(bad6[:2]))
# brute force (every order of draws), small cases, theta included
nb, worstb = 0, 0.0
for trial in range(60):
    m = rv.randint(1, 4)
    fq = [rv.choice([0.01, 0.05, 0.1, 0.2]) for _ in range(m)]
    if sum(fq) >= 1:
        continue
    kn = [rv.randint(1, m) for _ in range(rv.choice([0, 2]))]
    ty = kn + [rv.randint(0, m), rv.randint(0, m)]
    x = rv.randint(1, 2)
    th = rv.choice([0.0, 0.01, 0.1])
    ref = bf_brute(x, kn, ty, fq, th)
    got = ppl_prob(hN, x, kn, ty, fq, th)
    nb += 1
    worstb = max(worstb, abs(got - ref) / max(ref, 1e-300) if ref > 0 else abs(got))
check('V6: the PPL dmProb = brute-force enumeration of every order of draws (%d cases): worst %.1e' % (nb, worstb),
      worstb < 1e-12)
# (3) the 12-digit model: beta 3c's sum keeps about 10 digits; beta 3b's cancelled
w12n, w12o, n12 = 0.0, 0.0, 0
for (pres_, hp_, hd_), m, gen in cases6[::2]:
    fq = [0.6] + [rv.choice([0.0001, 0.0002, 0.0005]) for _ in range(m - 1)]
    fqF = [_Fr(repr(v)) for v in fq]
    ty = typed(pres_, gen)
    for H in (hp_, hd_):
        kn = knowns(H, pres_, gen)
        ex = _exact_prob(H[3], kn, ty, fqF, _Fr(0))
        if ex <= 0:
            continue
        n12 += 1
        w12n = max(w12n, abs(dp_py(H[3], kn, ty, fq, 0.0, R=r12) - float(ex)) / float(ex))
        w12o = max(w12o, abs(ie12(H[3], kn, ty, fq, 0.0) - float(ex)) / float(ex))
print('     12-digit model, %d rare-allele probabilities: beta 3c worst relative error %.1e, beta 3b %.1e' % (n12, w12n, w12o))
check('V6: in a 12-significant-digit model of the Prime (every operation rounded), beta 3c\'s sum stays within 1E-9 '
      'of the exact value on %d rare-allele probabilities (worst %.1e); beta 3b\'s cancelling sum is off by up to '
      '%.1e (relative)' % (n12, w12n, w12o), w12n < 1e-9 and w12o > 0.5)
# (4) the two cases that cancelled, end to end: the LR, the locus page; beta 3b's wrong conclusions
CANCEL = [('S 1/1 + 4U vs V 5/7 + 4U', [1, 1, 0], [0, 1, 0, 4], [1, 0, 0, 4], [5, 7, 1, 1, 0, 0]),
          ('V 1/1 + S 2/3 + 3U vs V + 4U', [1, 1, 0], [1, 1, 0, 3], [1, 0, 0, 4], [1, 1, 2, 3, 0, 0])]
CFQ = ['0.6', '0.0001', '0.0005', '0.0002', '0.0002', '0.0005', '0.0001']
for nm, pres_, hp_, hd_, gen in CANCEL:
    fqF = [_Fr(v) for v in CFQ]
    ty = typed(pres_, gen)
    Pe = _exact_prob(hp_[3], knowns(hp_, pres_, gen), ty, fqF, _Fr(0))
    De = _exact_prob(hd_[3], knowns(hd_, pres_, gen), ty, fqF, _Fr(0))
    lre = float(Pe / De)
    locus = ([10, 11, 12, 13, 14, 15, 16], [float(v) for v in CFQ], gen)
    hn6, pn6 = _pages(PROG, pres_, hp_, hd_, [locus], 0.0, [1])
    ho6, po6 = _pages(B3B, pres_, hp_, hd_, [locus], 0.0, [1])
    lrn, lro = hn6.globals_['dmLR'][0], ho6.globals_['dmLR'][0]
    pic_n = pn6[1][0]
    shown = [t for t in pic_n if t.startswith('LR = ')]
    check('V6: %s, theta 0: exact LR %.6g; beta 3c %.6g (relative %.0e), the page shows %s and no "LR = 0"'
          % (nm, lre, lrn, abs(lrn - lre) / lre, shown), lrn > 0 and abs(lrn - lre) <= 1e-9 * lre
          and shown == ['LR = ' + hn6.call('dmBig', lrn)] and not any('LR = 0' in t for t in pic_n + pn6[1][1]))
    old_txt = [t for t in po6[1][0] if t.startswith('LR = 0') or t.startswith('Hd cannot')]
    check('V6: ... beta 3b: LR %s and the page says %s' % (lro, old_txt),
          (lro == 0 and old_txt == ['LR = 0: a known contributor under Hp has an'])
          or (lro == -1 and old_txt == ['Hd cannot produce this mixture (P = 0),']))
# (5) the work: operation counts at the limits, and the harness time
hN.globals_['dmFq'] = [0.1] * 8; hN.globals_['dmM'] = 8.0; hN.globals_['dmTh'] = 0.01
hO.globals_['dmFq'] = [0.1] * 8; hO.globals_['dmM'] = 8.0; hO.globals_['dmTh'] = 0.01
tn_ = _time.time()
for i in range(10):
    vn = hN.call('dmProb', 4.0, [], [1.0, 2.0])
tn_ = (_time.time() - tn_) / 10
to_ = _time.time()
for i in range(3):
    vo = hO.call('dmProb', 4.0, [], [1.0, 2.0])
to_ = (_time.time() - to_) / 3
ops_new = 8 * 8 + 8 * (9 * 10 // 2) + 8
ops_old = 2 ** 8 * (8 + 8)
print('     the largest case (8 alleles, 4 unknowns, |U| = 8): about %d multiply-adds in beta 3c, %d in beta 3b; '
      'harness %.1f ms vs %.1f ms per call (PC); the same value, %.10g / %.10g' % (ops_new, ops_old, tn_ * 1000,
                                                                              to_ * 1000, vn, vo))
check('V6: the largest case costs about %d operations (beta 3b: %d) and runs %.0f times faster in the harness, '
      'with the same value' % (ops_new, ops_old, to_ / tn_), tn_ < to_ and abs(vn - vo) <= 1e-12 * vo)

# ---- V3, B4: the ENFSI scale in help
print('-- V3 (B4): the ENFSI scale in help --')
hv = Harness(PROG, strict=True, cas='fail'); hv.call('dmInit'); hv.call('dmHelpPage', 2.0)
hvo = Harness(B3B, strict=True, cas='fail'); hvo.call('dmInit'); hvo.call('dmHelpPage', 2.0)
tn_, to_ = [t.text for t in hv.texts], [t.text for t in hvo.texts]
check('V3 B4: help page 2 reads "ENFSI scale: LR 2-10 weak, 10-100 moderate," (beta 3b: "LR 1-10 weak")',
      'ENFSI scale: LR 2-10 weak, 10-100 moderate,' in tn_ and 'ENFSI scale: LR 1-10 weak, 10-100 moderate,' in to_
      and [s.replace('LR 1-10', 'LR 2-10') for s in to_] == tn_)
vb = [(v, hv.call('dmVerbal', v), hv.call('dmBand', v)) for v in (1.0, 1.99, 2.0, 9.99, 10.0)]
for v, s, b in vb:
    print('     dmVerbal(%g) = %r, dmBand = %d' % (v, s, b))
check('V3 B4: the program\'s own scale puts the lower edge of "weak" at 2, as the help now says: dmVerbal 1 and '
      '1.99 "about equal", 2 and 9.99 "weak support for Hp", 10 "moderate"; dmBand steps at 2 and at 10',
      vb[0][1] == vb[1][1] == 'about equal support for Hp and Hd' and vb[2][1] == vb[3][1] == 'weak support for Hp'
      and vb[4][1] == 'moderate support for Hp' and vb[0][2] == vb[1][2] and vb[2][2] == vb[1][2] + 1
      and vb[3][2] == vb[2][2] and vb[4][2] == vb[3][2] + 1)

# ---- V4: the review's own check script, on beta 3c and on beta 3b
print('-- V4: the review\'s check_DNAMixLR.py (19 Oct 2026) on beta 3c and on beta 3b --')
REVIEW = '/home/claude/work/review/check_DNAMixLR.py'
REV_PROG = '/home/claude/work/review/fleet/DNAMixLR_beta3b.txt'


def _review_run(path, tag):
    src_ = open(REVIEW, encoding='utf-8').read()
    assert REV_PROG in src_
    tmp = os.path.join(SCR, 'check_DNAMixLR_on_%s.py' % tag)
    open(tmp, 'w', encoding='utf-8').write(src_.replace(REV_PROG, path))
    res_ = subprocess.run([sys.executable, tmp], capture_output=True, text=True, cwd=SCR)
    return [(ln[:4], ln[5:]) for ln in res_.stdout.split('\n') if ln.startswith('PASS ') or ln.startswith('FAIL ')]


import subprocess  # noqa: E402
rv_new, rv_old = _review_run(PROG, '3c'), _review_run(B3B, '3b')
check('V4: the review script ran %d checks on each version' % len(rv_new),
      len(rv_new) == len(rv_old) and len(rv_new) > 100
      and all(a[1][:20] == b[1][:20] for a, b in zip(rv_new, rv_old)))
# open decisions: the Hypotheses wording (D17, the G lines) and dmBig's "10.00E-3" (B5, not in this pass)
OPEN = ('G: Hypotheses sub-menu line', 'G: main menu line', 'H: dmBig(0.009999) prints a mantissa below 10')
# the checks that RECORDED a bug (they pass while the bug is there): each fixed now
RECORDED = ('E: a refused -1 unknowns is kept too', 'E: custom "Victim typed? = 2" is NOT validated',
            'F: the locus page (picture view) says "a known contributor', 'F: the caption also says "1 alleles"',
            'F: the formula view says the same wrong sentence')
old_fail = [b[1] for a, b in zip(rv_new, rv_old) if b[0] == 'FAIL']
fixed = [b[1] for a, b in zip(rv_new, rv_old) if b[0] == 'FAIL' and a[0] == 'PASS']
still = [a[1] for a, b in zip(rv_new, rv_old) if b[0] == 'FAIL' and a[0] == 'FAIL']
flipped = [a[1] for a, b in zip(rv_new, rv_old) if b[0] == 'PASS' and a[0] == 'FAIL']
print('     beta 3b: %d PASS, %d FAIL; beta 3c: %d PASS, %d FAIL' % (
    sum(1 for b in rv_old if b[0] == 'PASS'), len(old_fail), sum(1 for a in rv_new if a[0] == 'PASS'),
    sum(1 for a in rv_new if a[0] == 'FAIL')))
for s in fixed:
    print('     fixed:  ' + s[:110])
for s in still:
    print('     open:   ' + s[:110])
for s in flipped:
    print('     recorded bug, now gone: ' + s[:100])
check('V4: every check beta 3b failed passes on beta 3c (%d), except the %d that wait on open decisions '
      '(D17 wording, B5)' % (len(fixed), len(still)),
      len(fixed) >= 1 and all(any(s.startswith(o) for o in OPEN) for s in still) and len(still) == 7)
check('V4: the checks that recorded the bugs (pass while the bug is there) now fail, and only those (%d)' % len(flipped),
      len(flipped) == len(RECORDED) and all(any(s.startswith(r) for r in RECORDED) for s in flipped))
check('V4: the B1 regression check of the review ("dmHp is left at the refused value") fails on beta 3b and passes '
      'on beta 3c', any(s.startswith('E: ... but dmHp is left at the refused value') for s in fixed))

# ---- V5: the teaching-aid notice (Roger, 19 Oct 2026, 12:48)
print('-- V5: the teaching-aid notice on screen --')
NOTE_FULL = 'Teaching aid; not for casework or legal use.'
NOTE_SHORT = 'Teaching aid only'
DISCL_L = ('// DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; '
           'do not rely on its results for legal purposes.')
check('V5: the header carries the DISCLAIMER line beside the distribution terms',
      DISCL_L in open(PROG, encoding='utf-8').read().split('\n')[:30])
W1, W2 = 6.5, 7.6          # px per character, fonts 1 and 2: a generous model (the harness assumes 5.5 and 6.5)
EXCL_LOCI = [EX_LOCI[0], ([8, 9, 11], [0.3, 0.25, 0.1], [1, 1, 2, 0, 0, 0]), EX_LOCI[2]]
HDX_LOCI = [EX_LOCI[0], ([8, 9, 11], [0.3, 0.25, 0.1], [0, 0, 1, 2, 0, 0])]   # locus 2: V's alleles not in M: no LR
V5_STATES = [('the worked example', EX_LOCI), ('12 loci', EX_LOCI * 4), ('an exclusion at locus 2', EXCL_LOCI),
             ('12 loci with exclusions', EXCL_LOCI * 4), ('Hd impossible at locus 2', HDX_LOCI)]
PAGE_NOTE = {1: NOTE_SHORT, 2: NOTE_SHORT, 4: NOTE_SHORT, 3: NOTE_FULL, 8: NOTE_FULL, 7: NOTE_FULL}
bad5, n5, seen5 = [], 0, set()
for nm, loci in V5_STATES:
    for v in (1, 2, 3, 4, 8, 7):
        sels = sorted(set([1, 2, len(loci)])) if v == 7 else [1]
        for sel in sels:
            for frm in ((0.0, 1.0) if v == 7 else (0.0,)):
                for path in (PROG, B3B):
                    hh = Harness(path, strict=False, idle_key=4, cas='fail')
                    hh.call('dmInit')
                    _load_into(hh, *PRESETS[1][1:], loci)
                    hh.globals_['dmSel'] = float(sel); hh.globals_['dmFrm'] = frm
                    hh.press('Esc')
                    try:
                        hh.call('dmViews', float(v))
                    except HarnessStall:
                        pass
                    pg = hh.pages[-1]
                    nt = [t for t in pg.texts if t.text in (NOTE_FULL, NOTE_SHORT)]
                    if path == B3B:
                        if nt:
                            bad5.append((nm, v, sel, 'beta 3b has it'))
                        continue
                    n5 += 1
                    want = PAGE_NOTE[v]
                    if len(nt) != 1 or nt[0].text != want or nt[0].hex != '#FF0000':
                        bad5.append((nm, v, sel, frm, [t.text for t in nt]))
                        continue
                    t0 = nt[0]
                    seen5.add((v, t0.text, t0.y))
                    x_end = t0.x + W1 * len(t0.text)
                    clash = []
                    for t in pg.texts:
                        if t is t0:
                            continue
                        w = (W2 if t.font == 2 else W1) * len(t.text)
                        h_t = 14 if t.font == 2 else 10
                        v_over = t.y < t0.y + 10 and t0.y < t.y + h_t
                        h_over = t.x < x_end and t0.x < t.x + w
                        if v_over and h_over:
                            clash.append((t.y, t.x, t.text[:30]))
                    if x_end > 316 or t0.y + 10 > 218 or clash:
                        bad5.append((nm, v, sel, frm, t0.y, x_end, clash[:2]))
print('     notices seen (page, text, y): %s' % sorted(seen5))
check('V5: every LR page shows the notice in red -- "%s" on the Results table, every locus page (picture and formula '
      'view; LR > 0, = 0 and "no LR") and the fallacy page; "%s" in the title row of the three plots -- inside the '
      'screen and clear of every other text by a %.1f / %.1f px-per-character model; %d screens, 5 states; beta 3b '
      'shows neither' % (NOTE_FULL, NOTE_SHORT, W1, W2, n5), not bad5 and n5 > 30, str(bad5[:3]))
# help page 1 (the program opens on its menu: help page 1 is its About page)
hh = Harness(PROG, strict=True, cas='fail'); hh.call('dmInit'); hh.call('dmHelpPage', 1.0)
ho = Harness(B3B, strict=True, cas='fail'); ho.call('dmInit'); ho.call('dmHelpPage', 1.0)
tl = sorted((t.y, t.text) for t in hh.texts if t.font == 1)
nt = [t for t in hh.texts if t.text == NOTE_FULL]
check('V5: help page 1 shows the notice in red at y 193, between the last line (y %d) and the footer (y 204), every '
      'other line as in beta 3b (moved up at most 6 px)' % max(y for y, s in tl if y < 193),
      len(nt) == 1 and nt[0].y == 193 and nt[0].hex == '#FF0000' and 12 + W1 * len(NOTE_FULL) <= 316
      and [s for y, s in tl if s != NOTE_FULL] == [s for y, s in sorted((t.y, t.text) for t in ho.texts if t.font == 1)]
      and all(0 <= a.y - b.y <= 6 for a, b in zip(sorted([t for t in ho.texts], key=lambda t: t.y),
                                                     sorted([t for t in hh.texts if t.text != NOTE_FULL], key=lambda t: t.y)))
      and max(y for y, s in tl if y < 193) <= 193 - 11 and 193 + 11 <= 204)
# the titles moved: a tap on the title still switches the locus plot to the waterfall (y < 22, any x)
for xt in (30, 120, 250):
    hh = Harness(PROG, strict=False, idle_key=4, cas='fail'); hh.call('dmInit'); _load_into(hh, *PRESETS[1][1:], EX_LOCI)
    hh.tap(xt, 10).press('Esc')
    hh.call('dmViews', 1.0)
    check('V5: a tap on the locus plot\'s title row at x %d still switches to the waterfall' % xt,
          hh.globals_['dmWF'] == 1.0 and any(p.has('Waterfall: log10 LRs add') for p in hh.pages))

# ================================================================ G (3c): beta 3c against beta 3b
print('\n==== G (3c): beta 3c against beta 3b ====')
_u0, _u1 = open(B3B, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()
M0, M1 = _bodies2(_u0), _bodies2(_u1)
d3c = sorted(n for n in set(M0) | set(M1) if M0.get(n) != M1.get(n))
WANT3C = ['dmCombLines', 'dmDrawFall', 'dmDrawFx', 'dmDrawLoci', 'dmDrawPanel', 'dmHelpPage', 'dmLadFrame',
          'dmProb', 'dmSetHyp', 'dmThStatic']
check('G (3c): the routines that differ from beta 3b are exactly %s (B1, B2, B4, dmProb and the notice)' % WANT3C,
      d3c == WANT3C, str(d3c))
# the notice (Roger, 19 Oct 2026): every change it makes, routine by routine
NOTE_L = 'Teaching aid; not for casework or legal use.'
_hp1_old = '\n'.join('    TEXTOUT_P(%s, G1, 12, %d, 1, %s);' % (t, y, c) for t, y, c in (
    ('"Example: mixture 12,13,14,15; victim 12/13."', 105, 'dmGRN'),
    ('"Hd (victim + 1 unknown): the unknown must be"', 118, 'dmGRN'),
    ('"14/15, P = 2 p14 p15.  Hp (victim + suspect"', 131, 'dmGRN'),
    ('"14/15): P = 1.  LR = 1 / (2 p14 p15)."', 144, 'dmGRN'),
    ('"Genotype entries are POSITIONS in your allele"', 160, '#000000h'),
    ('"list (1 = the first allele); 0 means an"', 173, '#000000h'),
    ('"allele the mixture does not show."', 186, '#000000h')))
_hp1_new = _hp1_old
for _a, _b in ((105, 102), (118, 115), (131, 128), (144, 141), (160, 154), (173, 167), (186, 180)):
    _hp1_new = _hp1_new.replace(', 12, %d, 1,' % _a, ', 12, %d, 1,' % _b)
_hp1_new += '\n    TEXTOUT_P("%s", G1, 12, 193, 1, dmRED);' % NOTE_L
check('G (3c): dmHelpPage: the B4 help line, on page 1 the notice at y 193 with the lines above it moved up '
      '3 and 6 px, and page 4\'s "same model"; nothing else', _hp1_old in M0['dmHelpPage'] and M1['dmHelpPage'] ==
      M0['dmHelpPage'].replace('"ENFSI scale: LR 1-10 weak, 10-100 moderate,"',
                               '"ENFSI scale: LR 2-10 weak, 10-100 moderate,"').replace(_hp1_old, _hp1_new).replace(
          '"from the same sum the program adds up, and"', '"from the same model the program uses, and"'))
_CAU_OLD = ('TEXTOUT_P("The LR is NOT the probability that the", G1, %s, %s, 1, dmRED);\n'
            '%sTEXTOUT_P("suspect contributed.", G1, %s, %s, 1, dmRED);')
_CAU_NEW = ('TEXTOUT_P("The LR is NOT P(the suspect contributed).", G1, %s, %s, 1, dmRED);\n'
            '%sTEXTOUT_P("' + NOTE_L + '", G1, %s, %s, 1, dmRED);')
_cb_o1 = _CAU_OLD % ('12', 'cbY + 22', '    ', '12', 'cbY + 33')
_cb_n1 = _CAU_NEW % ('12', 'cbY + 22', '    ', '12', 'cbY + 33')
_cb_o2 = ('      TEXTOUT_P("exclusion - not rescued without a dropout model", G1, 12, cbY + 11, 1, dmRED);\n'
          '      RETURN 2;')
_cb_n2 = ('      TEXTOUT_P("exclusion - not rescued without a dropout model", G1, 12, cbY + 11, 1, dmRED);\n'
          '      TEXTOUT_P("' + NOTE_L + '", G1, 12, cbY + 22, 1, dmRED);\n      RETURN 3;')
check('G (3c): dmCombLines: the caution in one line and the notice under it; the notice after an exclusion too',
      _cb_o1 in M0['dmCombLines'] and _cb_o2 in M0['dmCombLines']
      and M1['dmCombLines'] == M0['dmCombLines'].replace(_cb_o1, _cb_n1).replace(_cb_o2, _cb_n2))
_fa_o = _CAU_OLD % ('4', '186', '  ', '4', '196')
_fa_n = _CAU_NEW % ('4', '186', '  ', '4', '196')
check('G (3c): dmDrawFall: the caution in one line and the notice on the line it freed; nothing else',
      _fa_o in M0['dmDrawFall'] and M1['dmDrawFall'] == M0['dmDrawFall'].replace(_fa_o, _fa_n))
_dl_o = ('    TEXTOUT_P("log10 LR by locus", G1, 100, 2, 2, dmBLUE);\n  ELSE\n'
         '    TEXTOUT_P("Waterfall: log10 LRs add", G1, 70, 2, 2, dmBLUE);\n  END;')
_dl_n = ('    TEXTOUT_P("log10 LR by locus", G1, 60, 2, 2, dmBLUE);\n  ELSE\n'
         '    TEXTOUT_P("Waterfall: log10 LRs add", G1, 8, 2, 2, dmBLUE);\n  END;\n'
         '  TEXTOUT_P("Teaching aid only", G1, 202, 6, 1, dmRED);')
check('G (3c): dmDrawLoci: the two titles moved left, the short notice in the title row; nothing else',
      _dl_o in M0['dmDrawLoci'] and M1['dmDrawLoci'] == M0['dmDrawLoci'].replace(_dl_o, _dl_n))
_ts_o = '  TEXTOUT_P("log10 LR against theta", G2, 30, 2, 2, dmBLUE);'
_ts_n = ('  TEXTOUT_P("log10 LR against theta", G2, 24, 2, 2, dmBLUE);\n'
         '  TEXTOUT_P("Teaching aid only", G2, 202, 6, 1, dmRED);')
check('G (3c): dmThStatic: the title moved left, the short notice in the title row; nothing else',
      _ts_o in M0['dmThStatic'] and M1['dmThStatic'] == M0['dmThStatic'].replace(_ts_o, _ts_n))
_lf_o = '  TEXTOUT_P("ENFSI ladder, locus by locus", G1, 20, 2, 2, dmBLUE);'
_lf_n = ('  TEXTOUT_P("ENFSI ladder by locus", G1, 20, 2, 2, dmBLUE);\n'
         '  TEXTOUT_P("Teaching aid only", G1, 202, 6, 1, dmRED);')
check('G (3c): dmLadFrame: the shorter title and the short notice in the title row; nothing else',
      _lf_o in M0['dmLadFrame'] and M1['dmLadFrame'] == M0['dmLadFrame'].replace(_lf_o, _lf_n))
_sh_old_a = '      shPres := {IP(cuV), IP(cuS), IP(cuT)};'
_sh_new_a = '      shPres := {IFTE(IP(cuV) == 1, 1, 0), IFTE(IP(cuS) == 1, 1, 0), IFTE(IP(cuT) == 1, 1, 0)};'
_sh_old_b = '''      dmHp := {IP(cuV), IP(cuS), IP(cuT), IP(cuX)};
      dmHd := {IP(hdV), IP(hdS), IP(hdT), IP(hdX)};
      IF dmHp(4) < 0 OR dmHp(4) > 4 OR dmHd(4) < 0 OR dmHd(4) > 4 THEN
        MSGBOX("Unknown contributors: 0 to 4 under each hypothesis.");
        RETURN;
      END;'''
_sh_new_b = '''      IF IP(cuX) < 0 OR IP(cuX) > 4 OR IP(hdX) < 0 OR IP(hdX) > 4 THEN
        MSGBOX("Unknown contributors: 0 to 4 under each hypothesis.");
        RETURN;
      END;
      dmHp := {IFTE(IP(cuV) == 1, 1, 0), IFTE(IP(cuS) == 1, 1, 0), IFTE(IP(cuT) == 1, 1, 0), IP(cuX)};
      dmHd := {IFTE(IP(hdV) == 1, 1, 0), IFTE(IP(hdS) == 1, 1, 0), IFTE(IP(hdT) == 1, 1, 0), IP(hdX)};'''
check('G (3c): dmSetHyp: the counts tested before anything is stored, the flags forced to 1 / 0, nothing else',
      M1['dmSetHyp'] == M0['dmSetHyp'].replace(_sh_old_a, _sh_new_a).replace(_sh_old_b, _sh_new_b)
      and _sh_old_b in M0['dmSetHyp'])
_dp_old = '''      TEXTOUT_P("LR = 0: a known contributor under Hp has an", G1, 10, 47, 1, dmRED);
      TEXTOUT_P("allele the mixture does not show.  Excluded.", G1, 10, 58, 1, dmRED);'''
_dp_new = '''      dpU := dmKnowns(dmHp); dpX := 0;
      FOR dpJ FROM 1 TO SIZE(dpU) DO
        IF dpU(dpJ) == 0 THEN dpX := 1; END;
      END;
      IF dpX == 0 THEN
        IF SIZE(dmUSet(dpU)) > 2 * dmHp(4) THEN dpX := 2; END;
      END;
      IF dpX == 1 THEN
        TEXTOUT_P("LR = 0: a known contributor under Hp has an", G1, 10, 47, 1, dmRED);
        TEXTOUT_P("allele the mixture does not show.  Excluded.", G1, 10, 58, 1, dmRED);
      END;
      IF dpX == 2 THEN
        TEXTOUT_P("LR = 0: under Hp the contributors cannot", G1, 10, 47, 1, dmRED);
        TEXTOUT_P("account for every allele of M.  Excluded.", G1, 10, 58, 1, dmRED);
      END;
      IF dpX == 0 THEN
        TEXTOUT_P("LR = 0: P(E|Hp) underflows: it is below the", G1, 10, 47, 1, dmRED);
        TEXTOUT_P("calculator's smallest number.  Counted as 0.", G1, 10, 58, 1, dmRED);
      END;'''
_al_old = '+ STRING(dpR(1), 2, 0) + " alleles: P = 0"'
_al_new = '+ STRING(dpR(1), 2, 0) + " allele" + IFTE(dpR(1) == 1, "", "s") + ": P = 0"'
_pn_o = ('      TEXTOUT_P("The LR is NOT the probability that the", G1, 10, 73, 1, dmRED);\n'
         '      TEXTOUT_P("suspect contributed.", G1, 10, 84, 1, dmRED);\n  END;')
_pn_n = ('      TEXTOUT_P("The LR is NOT P(the suspect contributed).", G1, 10, 73, 1, dmRED);\n  END;\n'
         '  TEXTOUT_P("' + NOTE_L + '", G1, 10, 84, 1, dmRED);')
check('G (3c): dmDrawPanel: the LR = 0 lines become the three-way test, "allele(s)", and the caution in one line '
      'with the notice at y 84 for every LR; nothing else',
      M1['dmDrawPanel'] == M0['dmDrawPanel'].replace(_dp_old, _dp_new).replace(_al_old, _al_new).replace(_pn_o, _pn_n)
      and _dp_old in M0['dmDrawPanel'] and _al_old in M0['dmDrawPanel'] and _pn_o in M0['dmDrawPanel'])
_fx_old = '''      TEXTOUT_P("LR = 0 for every p and theta: a known", G1, 10, fxY, 1, dmRED, 300);
      TEXTOUT_P("contributor under Hp has an allele the", G1, 10, fxY + 11, 1, dmRED, 300);
      TEXTOUT_P("mixture does not show, so P(E|Hp) = 0.", G1, 10, fxY + 22, 1, dmRED, 300);'''
_fx_new = '''      fxL := dmKnowns(dmHp); fxOn := 0;
      FOR fxJ FROM 1 TO SIZE(fxL) DO
        IF fxL(fxJ) == 0 THEN fxOn := 1; END;
      END;
      IF fxOn == 0 THEN
        IF SIZE(dmUSet(fxL)) > 2 * dmHp(4) THEN fxOn := 2; END;
      END;
      IF fxOn == 1 THEN
        TEXTOUT_P("LR = 0 for every p and theta: a known", G1, 10, fxY, 1, dmRED, 300);
        TEXTOUT_P("contributor under Hp has an allele the", G1, 10, fxY + 11, 1, dmRED, 300);
        TEXTOUT_P("mixture does not show, so P(E|Hp) = 0.", G1, 10, fxY + 22, 1, dmRED, 300);
      END;
      IF fxOn == 2 THEN
        TEXTOUT_P("LR = 0 for every p and theta: under Hp", G1, 10, fxY, 1, dmRED, 300);
        TEXTOUT_P("the contributors cannot account for every", G1, 10, fxY + 11, 1, dmRED, 300);
        TEXTOUT_P("allele of M, so P(E|Hp) = 0.", G1, 10, fxY + 22, 1, dmRED, 300);
      END;
      IF fxOn == 0 THEN
        TEXTOUT_P("LR = 0 at these p and theta: P(E|Hp) is", G1, 10, fxY, 1, dmRED, 300);
        TEXTOUT_P("below the smallest number the calculator", G1, 10, fxY + 11, 1, dmRED, 300);
        TEXTOUT_P("holds (underflow), so it counts as 0.", G1, 10, fxY + 22, 1, dmRED, 300);
      END;'''
check('G (3c): dmDrawFx: the LR = 0 lines become the three-way test; nothing else',
      M1['dmDrawFx'] == M0['dmDrawFx'].replace(_fx_old, _fx_new) and _fx_old in M0['dmDrawFx'])
check('G (3c): outside those routines only comments differ', _outside2(_u0, d3c) == _outside2(_u1, d3c))
_pb = M1['dmProb']
check('G (3c): dmProb: no subtraction of a term (no "pbTot :=  pbTot -"), no MAX(0, ...), no 2^ mask loop, no Home '
      'K as a counter; every FOR whose finish can fall below its start is guarded',
      'pbTot - ' not in _pb and 'MAX(0' not in _pb and '2^' not in _pb and ', K,' not in _pb
      and 'IF pbW(pbS + 1) > 0 AND pbLo <= pbN - pbS THEN' in _pb and _pb.count('IF SIZE(pbKn) > 0 THEN') == 2)
for nm in ('dmKnowns', 'dmTyped', 'dmEval', 'dmUSet', 'dmCasP'):
    check('G (3c): %s byte for byte beta 3b\'s' % nm, M0[nm] == M1[nm] and
          re.search(r'(?ms)^' + nm + r'\(.*?^END;', _u0).group(0) == re.search(r'(?ms)^' + nm + r'\(.*?^END;', _u1).group(0))
_l1 = _u1.split('\n')
check('G (3c): the banner reads "DNAMIXLR - beta 3c", the tested-on lines name 3c, and a "beta 3c" paragraph is there',
      _l1[3] == '// DNAMIXLR - beta 3c' and '(1 to 3c) has been run on hardware' in _u1
      and '// What changed in beta 3c (19 Oct 2026)' in _u1)
_code1 = [l for l in re.sub(r'//[^\n]*', '', _u1).split('\n') if l.strip()]
check('G (3c): no code line names a beta (version strings live in comments only)',
      not [l for l in _code1 if re.search(r'beta ?3', l)])
_lens = [len(re.findall(r',', m_)) + 1 for m_ in re.findall(r'(?m)^\s*LOCAL ([^;(]*);', '\n'.join(_code1))]
check('G (3c): every LOCAL line holds at most 6 names (max %d)' % max(_lens), max(_lens) <= 6)
_dep, _badc = 0, []
for n_, l_ in enumerate(_l1, 1):
    _ins = False
    for i_, ch in enumerate(l_):
        if ch == '"':
            _ins = not _ins
        elif not _ins:
            if l_[i_:i_ + 2] == '//':
                if _dep:
                    _badc.append(n_)
                break
            _dep += (ch in '({[') - (ch in ')}]')
check('G (3c): no // comment inside an open bracket', not _badc, str(_badc[:5]))
check('G (3c): INSTRING appears exactly as often as in beta 3b (no new search of a string)',
      re.sub(r'//[^\n]*', '', _u1).count('INSTRING(') == re.sub(r'//[^\n]*', '', _u0).count('INSTRING('))
print('  differ from beta 3b: %s, each exactly as listed' % ', '.join(d3c))

# ================================================================ S
print('\n==== S: h.sci_strings over every beta 3c harness run of this script ====')
_mine = [h_ for h_ in ALL_H if h_._src == PROG]
_sci = [(v, d, t) for h_ in _mine for v, d, t in h_.sci_strings]
check('S: %d beta 3c harness runs, %d scientific STRING results (%d runs of older versions not counted)'
      % (len(_mine), len(_sci), len(ALL_H) - len(_mine)), _sci == [], str(_sci[:8]))

print('\n%d PASS, %d failure(s)' % (NPASS[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
