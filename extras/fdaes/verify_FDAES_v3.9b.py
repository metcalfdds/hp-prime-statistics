# -*- coding: utf-8 -*-
"""verify_FDAES_v3.9b.py -- checks FDAES v3.9b (19 Oct 2026): v3.9a with the Gustafson page reworded (Aykroyd 1995).
NEW in v3.9b: Part V2 (v3.9a -> v3.9b): the reworded page line by line and as drawn, the routine diff (only FDAES
and fdHelp change), the references, the version strings.  Part V (v3.9 -> v3.9a) is kept and runs on v3.9a (V39A)
so every v3.9a check still holds; every other part runs on v3.9b.

The v3.9a description follows.

verify_FDAES_v3.9a.py -- checks FDAES v3.9a (19 Oct 2026): the history pages rewritten from the papers
(FDAES_source_facts_v1a.md section 9), on top of every check of verify_FDAES_v3.9.py.

NEW in v3.9a:
  Part V  v3.9 -> v3.9a.  Each new page line by line (WHY GUSTAFSON 1950 IS EXCLUDED, A SHORT HISTORY, the ABFO
          lines on BAYESIAN FRAMEWORK and the closing page, the report's line, Johanson's opening page), every line
          37 characters or fewer, no "not checked" in any display string, the page breaks as drawn by the harness,
          the version strings, the header's sources and pages; each check also run on v3.9, which must FAIL it.
          The routine diff v3.9 -> v3.9a (only FDAES() and fdHelp change, and only in those lines); sessions run on
          both versions (About, help topic 10, Johanson -> pool -> report, Willems + Liversidge + Lamendin -> pool ->
          report) identical but for the listed lines.
KEPT from verify_FDAES_v3.9.py, now run on v3.9a, changed only where v3.9a changes a line on purpose: NEW is
  v3.9a; Part H (About has 20 pages with the exit page, the history page now two; the opening and About titles;
  the history, Bayesian and exit pages' new lines); Part S (the About order with "A SHORT HISTORY" in place of
  "HISTORICAL WARNINGS IGNORED"; Gustafson's Lamendin lines); Part P (the report's line 8); Part K (the opening
  page's title); Part L (Cattell's "North European" children are not an ancestry row); Part G (v3.8a -> v3.9a:
  the exit page and version strings); Part SR 8 (sourced lines in place of "not checked").

The v3.9 description follows.

verify_FDAES_v3.9.py -- checks FDAES v3.9 (19 Oct 2026): the fleet review's FDAES items and Roger's
decisions D1 (the band), D2 (Prince & Ubelaker's own equations), D3 (Bang & Ramm's own method), D4
(Lamendin's spread, 12.5) and D7 (no pool at the Willems ceiling), the help topics and the disclaimer.
Harness ppl_run_v3e (home_minus off, as the fleet's verify scripts run it).

Built from verify_FDAES_v3.8a.py.  KEPT, run on v3.9 (changed only where v3.9 changes a screen on purpose):
  Part T  the Willems and Liversidge tables: image transcription vs text layers, internal consistency,
          the program's tables through its own look-ups (unchanged).
  Part N  fdWSum / fdWEst / fdLvEst against an independent implementation, 1000 stagings x 3 sexes and
          the edge cases (CHANGED: fdWSum returns 6 elements, fdWEst 11 -- the all-H flag is checked).
  Part U  full Willems / Liversidge sessions in the harness (CHANGED: the v3.9 band, the ceiling page,
          no band under an H floor above the estimate, the pool offers, the menu's Exit is item 7, the
          opening page takes one key, the odontogram's first help line).
  Part E  the worked examples (CHANGED: all seven at H is the ceiling; the self-check pages 3-4 are now 5-6).
  Part P  the pool (CHANGED: Lamendin is entered in mm; "P-U 2002" is a label; the report template).
  Part W / X / I  widths, scientific displays (h.sci_strings, must be empty), INSTRING.
  Part Q  v3.8a's own display fixes, where v3.9 keeps them: the posterior panel, the 12-digit model of the
          emulator's case, fdPctN / fdPct / fdEq, the Willems footers and mark (Q1, Q4 and Q8 -- the old band,
          the old Lamendin / B&R lines and the v3.8 -> v3.8a diff -- give way to Parts B, L, R and G).
  Part S  every other module against v3.8a (REPLACES v3.8a's comparison with v3.7b): identical screens,
          dialogs, inputs, MSGBOXes and RETURN after the known v3.9 rewrites; every band compared one by one.
  Part G  the routine diff, now v3.8a -> v3.9 (REPLACES v3.7b -> v3.8a).
NEW in v3.9:
  Part B  the band (D1): P = 0.949, 0.95, 0.951, 0.049, 0.05, 0.051 and more; the rule at exactly 0.95 / 0.05.
  Part C  the Willems ceiling (C-F1, D7) for both sexes and unknown; Liversidge's floor (C-F6).
  Part F  the typed posterior threshold (C-F8, C-F9).
  Part L  Lamendin 1992 / Prince-Ubelaker 2002 (D2, D4; C-F2, C-F3): the program's P-U numbers against
          PU_tables_v1.csv, each Table's profile means, every Setup x three tooth measurements, the refusals,
          the pool, the D4 constant and a one-line change of it.
  Part R  Bang & Ramm (D3; C-F4): every row of all four tables at X = 0, 5, 9.0, 9.01 and 12 against
          BR_tables_v1.csv, all 48 menu paths, the refusals, a cancel at each CHOOSE, several roots.
  Part J  Johanson (C-F5): the menu, the labels, the page for 120 score sets.
  Part K  the Verify Calculations pages against an independent computation.
  Part H  the help topics and the disclaimer.
  Part RG the review's check_FDAES.py on v3.8a and on v3.9 (which of its bug-documenting checks flip).
SECOND REVIEW (19 Oct 2026, evening; v3.9 fixed in place before delivery): checks added to Parts N, U, C (the
  near-ceiling rule, girls' 15.93), L (P-U outside 25-99, "< 0", Lamendin's 72.7 % floor, "> 110", RH with two
  decimals, the band's source on page 1, refusals with two decimals), R (molars "any of six", TM, above 110
  refused, X > 14 warned, the same root twice refused, p 19's advice, the new interval labels), J ("1-11 teeth",
  "> 110"), K, H (the help facts, the About pages marked "not checked", the disclaimer wording), P (the floor line,
  the report), S, G, and Part SR (a code-level check per item).  Where the old behaviour matters it is shown on
  v3.8a, and on the pre-review v3.9 draft when its scratch copy is present (skipped cleanly when absent).

Run:  python3 verify_FDAES_v3.9b.py     (exit code 0 = all passed)
"""
from __future__ import print_function
import sys, os, re, random, difflib, math, itertools, csv, subprocess, tempfile
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN, getcontext
sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3e import Harness, CANCEL              # noqa: E402
from scipy.stats import norm                         # noqa: E402

NEW = '/home/claude/work/fix19b/FDAES_v3.9b.txt'
V39A = '/home/claude/work/fix19/FDAES_v3.9a.txt'        # the version v3.9b replaces (Part W)
V39 = '/home/claude/work/fix19/FDAES_v3.9.txt'          # the version v3.9a replaces (Part V)
OLD = '/home/claude/work/out/FDAES_v3.8a.txt'         # the version v3.9 replaces
V38 = '/home/claude/work/out/FDAES_v3.8.txt'          # Part Q's 12-digit reproduction of the emulator
SRCDIR = '/mnt/user-data/uploads/HP-Prime/_emulator_round2_tmp/willems'
BUILTINS = '/home/claude/work/HP_Prime_Builtin_Names.txt'
PUCSV = '/home/claude/work/fdaes39/PU_tables_v1.csv'
BRCSV = '/home/claude/work/fdaes39/BR_tables_v1.csv'
REVIEW_CHECK = '/home/claude/work/review/check_FDAES.py'
FAIL, NPASS, PART = [], [0], {}
SCI, ALLRUNS, TIES = [], [], []
getcontext().prec = 28


def check(name, ok, detail=''):
    k = name.split()[0]
    PART[k] = PART.get(k, 0) + 1
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)
        print('FAIL ' + name + (('   ' + detail) if detail else ''))


# ===================================================================================== the sources
# ---- Willems et al. 2001, p 894, read from the page image.  None = "..." (no score printed).
#      Columns A B C D E F G H.  Rows in the paper's order (= FDI 31..37).
W_TEETH = ['Central incisor', 'Lateral incisor', 'Canine', 'First bicuspid', 'Second bicuspid',
           'First molar', 'Second molar']
W_BOYS = {   # Table 1
    'Central incisor': [None, None, '1.68', '1.49', '1.5', '1.86', '2.07', '2.19'],
    'Lateral incisor': [None, None, '0.55', '0.63', '0.74', '1.08', '1.32', '1.64'],
    'Canine':          [None, None, None, '0.04', '0.31', '0.47', '1.09', '1.9'],
    'First bicuspid':  ['0.15', '0.56', '0.75', '1.11', '1.48', '2.03', '2.43', '2.83'],
    'Second bicuspid': ['0.08', '0.05', '0.12', '0.27', '0.33', '0.45', '0.4', '1.15'],
    'First molar':     [None, None, None, '0.69', '1.14', '1.6', '1.95', '2.15'],
    'Second molar':    ['0.18', '0.48', '0.71', '0.8', '1.31', '2', '2.48', '4.17']}
W_GIRLS = {  # Table 2 (the minus signs are on the image; the text layer drops them)
    'Central incisor': [None, None, '1.83', '2.19', '2.34', '2.82', '3.19', '3.14'],
    'Lateral incisor': [None, None, None, '0.29', '0.32', '0.49', '0.79', '0.7'],
    'Canine':          [None, None, '0.6', '0.54', '0.62', '1.08', '1.72', '2'],
    'First bicuspid':  ['-0.95', '-0.15', '0.16', '0.41', '0.6', '1.27', '1.58', '2.19'],
    'Second bicuspid': ['-0.19', '0.01', '0.27', '0.17', '0.35', '0.35', '0.55', '1.51'],
    'First molar':     [None, None, None, '0.62', '0.9', '1.56', '1.82', '2.21'],
    'Second molar':    ['0.14', '0.11', '0.21', '0.32', '0.66', '1.28', '2.09', '4.04']}
# the paper's test of the adapted method (p 894): (median, mean, s.d.) of the overestimation
W_ERR = {1: ('0.1', '0.0', '0.9'), 2: ('0.2', '0.2', '1.3')}

# ---- Liversidge 2006, Table X (p 467), read from the page image, one row per tooth and stage as
#      printed: girls mean, SE, SD, n | boys mean, SE, SD, n | girls and boys mean, SE, SD
L_TEETH = ['I1', 'I2', 'C', 'P1', 'P2', 'M1', 'M2']
LX_ROWS = '''
I1 D 4.06 0.08 1.01 163 4.21 0.08 1.19 225 4.15 0.06 1.12
I1 E 5.14 0.04 0.74 298 5.38 0.05 1.00 427 5.28 0.04 0.91
I1 F 6.36 0.05 0.87 270 6.61 0.05 0.82 309 6.49 0.04 0.85
I1 G 7.66 0.04 0.89 462 8.00 0.05 1.06 562 7.85 0.03 1.00
I2 C 3.38 0.13 0.70 29 3.82 0.11 0.73 42 3.64 0.09 0.75
I2 D 4.42 0.06 0.96 254 4.68 0.06 1.08 389 4.58 0.04 1.04
I2 E 5.71 0.05 0.87 337 6.03 0.05 1.05 437 5.89 0.04 0.99
I2 F 7.06 0.04 0.80 353 7.49 0.05 0.95 432 7.30 0.03 0.91
I2 G 8.31 0.04 0.98 645 8.83 0.04 1.10 688 8.58 0.03 1.08
C C 4.15 0.08 1.02 174 4.54 0.07 1.19 330 4.40 0.05 1.15
C D 5.35 0.05 1.03 372 5.82 0.05 1.14 514 5.63 0.04 1.12
C E 7.08 0.04 0.97 544 7.74 0.04 1.07 749 7.46 0.03 1.08
C F 8.81 0.03 1.08 996 9.78 0.04 1.22 1069 9.31 0.03 1.25
C G 10.85 0.04 1.28 821 12.02 0.05 1.33 819 11.43 0.04 1.43
P1 B 3.57 0.18 1.31 56 3.78 0.08 0.69 69 3.68 0.09 1.02
P1 C 4.73 0.04 0.78 308 4.99 0.05 1.10 436 4.88 0.04 0.99
P1 D 6.26 0.05 0.96 408 6.64 0.04 1.04 559 6.48 0.03 1.03
P1 E 7.92 0.03 0.93 798 8.35 0.04 1.05 808 8.14 0.03 1.02
P1 F 9.77 0.04 1.14 893 10.29 0.04 1.24 930 10.04 0.03 1.22
P1 G 11.46 0.05 1.18 659 12.14 0.05 1.23 591 11.78 0.04 1.25
P2 A 4.14 0.16 1.43 78 4.32 0.14 1.37 90 4.24 0.11 1.39
P2 B 4.79 0.07 0.88 160 4.86 0.07 1.07 223 4.83 0.05 1.00
P2 C 5.90 0.07 1.24 340 6.02 0.06 1.22 448 5.97 0.04 1.23
P2 D 7.29 0.05 1.09 496 7.46 0.05 1.16 577 7.38 0.03 1.13
P2 E 8.54 0.04 1.14 745 9.06 0.04 1.23 777 8.81 0.03 1.21
P2 F 10.51 0.04 1.29 975 10.98 0.05 1.43 958 10.74 0.03 1.38
P2 G 12.33 0.05 1.32 701 12.94 0.06 1.42 633 12.62 0.04 1.40
M1 D 3.74 0.08 0.77 101 4.02 0.12 1.40 138 3.90 0.08 1.18
M1 E 4.87 0.06 0.97 249 5.06 0.05 1.04 362 4.98 0.04 1.02
M1 F 6.04 0.05 0.92 314 6.42 0.06 1.17 437 6.25 0.04 1.09
M1 G 8.22 0.04 1.28 1194 8.66 0.04 1.40 1302 8.45 0.03 1.36
M2 A 4.05 0.11 0.67 41 4.07 0.07 0.55 66 4.06 0.06 0.60
M2 B 4.63 0.06 0.84 175 4.83 0.06 0.86 216 4.74 0.04 0.85
M2 C 6.01 0.05 1.04 402 6.13 0.05 1.15 564 6.08 0.04 1.10
M2 D 7.67 0.04 1.05 793 7.96 0.04 1.13 800 7.81 0.03 1.10
M2 E 9.35 0.04 1.11 735 9.71 0.04 1.14 797 9.54 0.03 1.14
M2 F 10.84 0.04 1.06 629 11.34 0.05 1.18 575 11.08 0.03 1.15
M2 G 12.92 0.04 1.41 1098 13.42 0.05 1.43 998 13.16 0.03 1.44
'''
# ---- Table IX (p 465), read from the page image: tooth, stage, girls mean, SE, boys mean, SE,
#      sex difference -- every row (the H rows are the ones FDAES uses; the others check the reading)
L9_ROWS = '''
I1 E 4.35 0.09 4.46 0.15 0.11
I1 F 5.67 0.13 6.02 0.13 0.35
I1 G 6.68 0.10 6.95 0.10 0.27
I1 H 7.90 0.11 8.34 0.11 0.44
I2 E 4.85 0.13 5.24 0.12 0.39
I2 F 6.40 0.07 6.63 0.12 0.23
I2 G 7.32 0.10 7.78 0.11 0.46
I2 H 8.81 0.11 9.33 0.10 0.52
C E 6.01 0.13 6.62 0.11 0.61
C F 7.65 0.11 8.66 0.05 1.01
C G 9.88 0.11 11.05 0.11 1.17
C H 11.72 0.10 13.23 0.12 1.51
P1 C 3.48 0.19 3.76 0.13 0.28
P1 D 5.26 0.13 5.46 0.11 0.20
P1 E 6.72 0.05 7.21 0.12 0.49
P1 F 8.92 0.04 9.19 0.11 0.27
P1 G 10.74 0.10 11.43 0.11 0.96
P1 H 12.24 0.11 13.04 0.12 0.80
P2 B 3.80 0.21 3.92 0.21 0.12
P2 C 4.80 0.16 4.90 0.10 0.10
P2 D 6.12 0.15 6.35 0.13 0.23
P2 E 7.60 0.13 7.97 0.12 0.37
P2 F 9.36 0.10 9.83 0.12 0.47
P2 G 11.65 0.12 12.26 0.12 0.61
P2 H 13.47 0.14 14.12 0.14 0.65
M1 E 3.92 0.16 4.00 0.13 0.08
M1 F 5.25 0.12 5.61 0.09 0.36
M1 G 6.37 0.11 6.80 0.11 0.43
M1 H 9.30 0.10 9.97 0.10 0.67
M2 A 3.44 0.23 3.47 0.20 0.03
M2 B 3.86 0.11 4.00 0.17 0.14
M2 C 4.84 0.11 4.94 0.12 0.10
M2 D 6.34 0.14 6.74 0.13 0.40
M2 E 8.53 0.10 8.81 0.12 0.28
M2 F 10.20 0.12 10.68 0.11 0.48
M2 G 11.65 0.10 12.23 0.13 0.58
M2 H 14.78 0.16 15.25 0.15 0.47
'''
STG = 'ABCDEFGH'
LX = {}            # (tooth index 1..7, stage index 1..8) -> dict of strings
for r in LX_ROWS.split('\n'):
    if r.strip():
        f = r.split()
        LX[(L_TEETH.index(f[0]) + 1, STG.index(f[1]) + 1)] = dict(
            gm=f[2], gse=f[3], gsd=f[4], gn=f[5], bm=f[6], bse=f[7], bsd=f[8], bn=f[9],
            cm=f[10], cse=f[11], csd=f[12])
L9 = {}
for r in L9_ROWS.split('\n'):
    if r.strip():
        f = r.split()
        L9[(L_TEETH.index(f[0]) + 1, STG.index(f[1]) + 1)] = dict(gm=f[2], gse=f[3], bm=f[4], bse=f[5], diff=f[6])


def D(s):
    return Decimal(s)


# the independent look-ups (sx: 1 boys, 2 girls, 0 unknown)
def w_score(sx, ti, st):
    row = (W_BOYS if sx == 1 else W_GIRLS)[W_TEETH[ti - 1]]
    v = row[st - 1]
    return None if v is None else D(v)


def l_mean(sx, ti, st):
    r = LX.get((ti, st))
    if r is None:
        return None
    return D(r[{1: 'bm', 2: 'gm', 0: 'cm'}[sx]])


def l_sd(sx, ti, st):
    r = LX.get((ti, st))
    if r is None:
        return None
    return D(r[{1: 'bsd', 2: 'gsd', 0: 'csd'}[sx]])


def l_h(sx, ti):
    r = L9[(ti, 8)]
    return D(r['bm']) if sx == 1 else D(r['gm'])     # girls' (earlier) when the sex is unknown


# ===================================================================================== the methods
def p12(x):
    """the Prime's 12 significant digits"""
    return Decimal(format(x, '.12g'))


def willems_one(st, sx):
    """{ok, sum, staged, bad, why}: the sum of the seven scores of one sex's table"""
    n = sum(1 for s in st if s)
    for i, s in enumerate(st, 1):
        if s == 0:
            return dict(ok=0, staged=n, bad=i, why=1)
        if w_score(sx, i, s) is None:
            return dict(ok=0, staged=n, bad=i, why=2)
    return dict(ok=1, sum=sum(w_score(sx, i, s) for i, s in enumerate(st, 1)), staged=n)


def first_bad(st, sx):
    """the first problem tooth in the order fdWSum meets them (staged or not, tooth by tooth)"""
    return willems_one(st, sx)


def ceiling(st):
    """v3.9, second review (the coordinator's rule, pending Roger): the staging is at the tables' ceiling
    when teeth 33-37 are all at H, whatever 31 and 32 show"""
    return all(s == 8 for s in st[2:7])


def willems(st, sx):
    """the Willems result for the Setup sex: mean, SE (the paper's s.d.; the 50:50 mixture with the
    sex unknown), P(age >= 18) as an UPPER tail (independent of the program's lower-tail form)"""
    if sx in (1, 2):
        r = willems_one(st, sx)
        if not r['ok']:
            return dict(ok=0, staged=r['staged'], bad=r['bad'], why=r['why'], badsx=sx)
        sd = D(W_ERR[sx][2])
        return dict(ok=1, mean=r['sum'], sd=sd, p=float(norm.sf(18, float(r['sum']), float(sd))),
                    sb=r['sum'] if sx == 1 else None, sg=r['sum'] if sx == 2 else None, staged=7,
                    allh=all(s == 8 for s in st), ceil=ceiling(st))
    rb, rg = willems_one(st, 1), willems_one(st, 2)
    if not rb['ok']:
        return dict(ok=0, staged=rb['staged'], bad=rb['bad'], why=rb['why'], badsx=1)
    if not rg['ok']:
        return dict(ok=0, staged=rg['staged'], bad=rg['bad'], why=rg['why'], badsx=2)
    sb, sg = rb['sum'], rg['sum']
    mean = (sb + sg) / 2
    var = (D('0.81') + D('1.69')) / 2 + ((sb - sg) / 2) ** 2
    sd = var.sqrt()
    p = 0.5 * norm.sf(18, float(sb), 0.9) + 0.5 * norm.sf(18, float(sg), 1.3)
    return dict(ok=1, mean=mean, sd=sd, p=float(p), sb=sb, sg=sg, staged=7, allh=all(s == 8 for s in st),
                ceil=ceiling(st))


def liversidge(st, sx):
    ms, sds, nh, hmax, nno, n = [], [], 0, Decimal(0), 0, 0
    for i, s in enumerate(st, 1):
        if not s:
            continue
        n += 1
        if s == 8:
            nh += 1
            hmax = max(hmax, l_h(sx, i))
        else:
            m = l_mean(sx, i, s)
            if m is None:
                nno += 1
            else:
                ms.append(m)
                sds.append(l_sd(sx, i, s))
    k = len(ms)
    out = dict(k=k, nh=nh, hmax=hmax, nno=nno, n=n)
    if k:
        est = sum(ms) / k
        sei = sum(d * d for d in sds).sqrt() / k
        sec = sum(sds) / k
        out.update(est=est, sei=sei, sec=sec, p=float(norm.sf(18, float(est), float(sec))))
    return out


# ===================================================================================== formatting
def rnd_opts(x, d):
    """the strings STRING(ROUND(x, d), 2, d) can give: the Prime's half-up from its 12 digits, and,
    at an exact decimal tie only, the half-down the harness's binary rounding can give"""
    v = p12(x)
    q = Decimal(1).scaleb(-d)
    up = v.quantize(q, rounding=ROUND_HALF_UP)
    dn = v.quantize(q, rounding=ROUND_HALF_DOWN)
    out = []
    for z in (up, dn):
        if z == 0:
            z = abs(z)
        s = str(z)
        if s not in out:
            out.append(s)
    return out


def F2(x):
    return rnd_opts(x, 2)


def F1(x):
    return rnd_opts(x, 1)


def PCT(pv):
    """fdPct(pv), pv in percent"""
    if 0 < pv < 0.1:
        return ['< 0.1']
    if 99.9 < pv < 100:
        return ['> 99.9']
    return rnd_opts(pv, 1)


def S(*parts):
    """a line as segments: plain strings, or lists of acceptable strings"""
    return [p if isinstance(p, list) else [p] for p in parts]


def matches(line, segs):
    if isinstance(segs, str):
        return line == segs
    for combo in itertools.product(*segs):
        if ''.join(combo) == line:
            if any(len(s) > 1 and c != s[0] for c, s in zip(combo, segs)):
                TIES.append('"%s" (the Prime: "%s")' % (line, ''.join(s[0] for s in segs)))
            return True
    return False


def first(segs):
    if isinstance(segs, str):
        return segs
    return ''.join(s[0] for s in segs)


def PCTN(pv):
    """v3.8a fdPctN(pv): a normal model's probability; an exact 0 / 100 is the floor"""
    if pv <= 0:
        return ['< 0.1']
    if pv >= 100:
        return ['> 99.9']
    return PCT(pv)


def EQ(opts):
    """v3.8a fdEq: ' = 50.0', or ' < 0.1' when the formatter wrote the relation"""
    return [(' ' + o) if o[:1] in '<>' else (' = ' + o) for o in opts]


CUT = '  (cut-points 5% and 95%)'
COLV = {'probably >= 18': '#008C3C', 'uncertain': '#FF4500', 'probably < 18': '#FF0000'}


def verdict(printed):
    """v3.9 (Roger's D1): the verdict for P(age >= 18) AS PRINTED (fdPctN's text, in percent):
    >= 95 green 'probably >= 18', <= 5 red 'probably < 18', else orange 'uncertain'; both ends
    inclusive.  '< 0.1' is red and '> 99.9' green."""
    v = 0.0 if printed.startswith('<') else 100.0 if printed.startswith('>') else float(printed)
    return 'probably >= 18' if v >= 95 else ('probably < 18' if v <= 5 else 'uncertain')


def band(p):
    """(the verdicts the Prime could print, the second line's segments) for P(age >= 18) = p"""
    opts = PCTN(p * 100)
    return [verdict(o) for o in opts], S('P(age >= 18)', EQ(opts), '%' + CUT)


SXW = {1: 'boys', 2: 'girls', 0: 'children'}
FDI = lambda i: str(30 + i)


# ===================================================================================== expected pages
def exp_willems_page(st, sx):
    w = willems(st, sx)
    if w['ok']:
        if sx == 0:
            L = [S('Sex unknown: both tables, 50:50.'),
                 S('Stages:' + ''.join(' %s%s' % (FDI(i), STG[s - 1]) for i, s in enumerate(st, 1))),
                 S('Boys  (Table 1): sum ', F2(w['sb']), ' yr'),
                 S('Girls (Table 2): sum ', F2(w['sg']), ' yr'),
                 S('= Dental age ', F2(w['mean']), ' yr (their mean)'),
                 S('Test (p 894): s.d. 0.9 boys, 1.3'),
                 S('girls; mean diff. (signed) 0.0, +0.2'),
                 S('50:50 mixture: SD ', F2(w['sd']), ' yr')]
        else:
            L = [S("Boys' scores (Table 1), summed:" if sx == 1 else "Girls' scores (Table 2), summed:")]
            items = [S('%s %s ' % (FDI(i), STG[s - 1]), F2(w_score(sx, i, s))) for i, s in enumerate(st, 1)]
            for grp in ((0, 1, 2), (3, 4, 5), (6,)):
                segs = []
                for j, g in enumerate(grp):
                    if j:
                        segs += S('   ')
                    segs += items[g]
                L.append(segs)
        if w['ceil']:
            # v3.9 (C-F1, D7; second review): at the tables' ceiling -- no number as an age, no ranges, no band
            first = S("= All seven at H: the tables' ceiling" if w['allh'] else "= 33-37 at H: the tables' ceiling")
            if sx == 0:
                L = L[:4] + [first, S('The largest sums any staging gives:'), S("16.03 boys, 15.93 girls. Willems's"),
                             S('children were at most 18.0, so sums'), S('this near the top cannot tell 16'),
                             S("from 30: they say only 'at least"), S("about 15.8-16'."),
                             S('No P(age >= 18), nothing to pool.'), S('One score alone is not an age.')]
            else:
                L += [first, S('Sum ', F2(w['mean']), ' yr; the largest any'), S('staging gives: 16.03 boys, 15.93'),
                      S("girls. Willems's children were at"), S('most 18.0, so a sum this near the'),
                      S('top cannot tell 16 from 30: it says'), S("only 'at least about 15.8-16'."),
                      S('No P(age >= 18), nothing to pool.')]
            return L, -1, w
        if sx != 0:
            L.append(S('= Dental age ', F2(w['mean']), ' yr'))
            if sx == 1:
                L += [S("Paper's test (p 894), boys:"), S('mean diff. (signed) +0.0, s.d. 0.9 yr')]
            else:
                L += [S("Paper's test (p 894), girls:"), S('mean diff. (signed) +0.2, s.d. 1.3 yr')]
        m, sd = w['mean'], w['sd']
        L += [S('68%: [', F1(max(Decimal(0), m - sd)), ', ', F1(m + sd), '] yr'),
              S('95%: [', F1(max(Decimal(0), m - 2 * sd)), ', ', F1(m + 2 * sd), '] yr'),
              S('(+ = too old; not subtracted here)')]
        if sx == 0:
            L += [S('One score alone is not an age.')]
        else:
            L += [S('One score alone is not an age:'), S('only the sum of all seven is.')]
        return L, w['p'], w
    L = [S('No age: Willems (2001) adds a score'), S('for each of the seven left lower'),
         S('teeth, and gives no rule for a'), S('tooth that is missing or unscored.'), S('')]
    un = [FDI(i) for i, s in enumerate(st, 1) if s == 0]
    if len(un) == 1:
        L.append(S('Needs all seven teeth: %s not staged' % un[0]))
    elif len(un) > 1:
        L += [S('Needs all seven teeth; not staged:'), S(', '.join(un))]
    for i, s in enumerate(st, 1):
        if s:
            nb, ng = w_score(1, i, s) is None, w_score(2, i, s) is None
            t = '%s at %s: ' % (FDI(i), STG[s - 1])
            if sx == 1 and nb:
                L.append(S(t + 'Willems printed no score'))
            if sx == 2 and ng:
                L.append(S(t + 'Willems printed no score'))
            if sx == 0 and (nb or ng):
                L.append(S(t + ('no score for either sex' if nb and ng else
                                'no score for boys' if nb else 'no score for girls')))
    L += [S(''), S('Liversidge (next page) still reads'), S('each staged tooth.')]
    return L, -1, w


def exp_liv_page(st, sx):
    lv = liversidge(st, sx)
    L = [S('Mean age of the children IN each'),
         S('stage, Table X, ' + {1: 'boys', 2: 'girls', 0: 'girls and boys'}[sx] + ':')]
    for i, s in enumerate(st, 1):
        if not s:
            continue
        t = '%s %s  ' % (FDI(i), STG[s - 1])
        if s == 8:
            L.append(S(t + 'at least ', F2(l_h(sx, i)), ' yr (Table IX)'))
        elif l_mean(sx, i, s) is not None:
            L.append(S(t, F2(l_mean(sx, i, s)), ' yr  SD ', F2(l_sd(sx, i, s))))
        else:
            L.append(S(t + 'no reference (too early)'))
    if lv['k']:
        L += [S('= Mean of %d %s: ' % (lv['k'], 'tooth' if lv['k'] == 1 else 'teeth'), F2(lv['est']), ' yr'),  # v3.8a
              S('SE if independent: ', F2(lv['sei']), ' yr'),
              S('SE if they move together: ', F2(lv['sec']), ' yr'),
              S('Teeth in one child develop together,'), S('so the truth is nearer the larger SE.'),
              S('P(age >= 18) from N(', F2(lv['est']), ', ', F2(lv['sec']), ').')]
        if lv['nh']:
            L += [S('At H: at least ', F2(lv['hmax']), ' yr, the mean'),
                  S('age of reaching H (some reach it'), S('earlier).')]
            if lv['hmax'] > lv['est']:
                # v3.9 (C-F6): the floor contradicts N(estimate, SE): no band
                L += [S('That floor is above the estimate,'), S('so no P(age >= 18) band is drawn.')]
                return L, -1, lv
        return L, lv['p'], lv
    if lv['nh']:
        L += [S('No estimate: Table X leaves out H,'), S('and no tooth below H has a figure.'),
              S('= At least ', F2(lv['hmax']), ' yr (Table IX: the'), S('mean age of reaching H).')]
    else:
        L += [S('No estimate: no staged tooth has a'), S('Table X figure (its stage is too'),
              S('early for children aged 2 to 17).')]
    return L, -1, lv


def npages(L, p):
    per = 12 if p >= 0 else 13
    return max(1, (len(L) + per - 1) // per)


# the odontogram geometry, as designed (FDAES_v3.8_CHANGES.md)
X1 = [24, 55, 88, 125, 162, 199, 252]
X2 = [51, 84, 121, 158, 195, 248, 299]
Y1 = [38, 35, 32, 30, 28, 27, 27]
Y2 = [89, 86, 83, 81, 79, 78, 78]
LABELS = ['A  cusp tips, not joined', 'B  cusp tips joined', 'C  occlusal enamel complete',
          'D  crown complete to CEJ', 'E  root shorter than crown', 'F  root >= crown, apex wide',
          'G  canal walls parallel', 'H  apex closed']
WTN = ['I1 Cent.Incisor (31)', 'I2 Lat.Incisor (32)', 'C  Canine (33)', 'P1 1st Premolar (34)',
       'P2 2nd Premolar (35)', 'M1 1st Molar (36)', 'M2 2nd Molar (37)']


def axis_x(age):
    return 24 + int((max(2.0, min(20.0, float(age))) - 2) * 276 / 18)


def exp_panel(st, sx, sel):
    """the five panel lines as segments (None = not drawn)"""
    out = {}
    if sel:
        s = st[sel - 1]
        out[138] = S(WTN[sel - 1] + ': ' + (LABELS[s - 1] if s else 'not staged'))
        if s == 0:
            out[149] = S('Not staged. Willems needs all seven teeth.')
        elif s <= 7:
            m = l_mean(sx, sel, s)
            if m is not None:
                out[149] = S('Liv. 2006: %s in %s, mean ' % (SXW[sx], STG[s - 1]), F2(m), ' yr, SD ',
                             F2(l_sd(sx, sel, s)))
            else:
                out[149] = S('Liv. 2006: no figure (too early for the sample)')
        else:
            if sx == 0:
                out[149] = S('Liv. 2006: H at ', F2(l_h(sx, sel)), ' yr (girls, the earlier)')
            else:
                out[149] = S('Liv. 2006: %s reach H at ' % SXW[sx], F2(l_h(sx, sel)), ' yr on average')
    else:
        out[138] = S('No tooth selected.')
        out[149] = None
    lv = liversidge(st, sx)
    if lv['k']:
        out[160] = S('Liversidge ', F2(lv['est']), ' yr, SE ', F2(lv['sei']), ' indep, ', F2(lv['sec']),
                     ' together')
    else:
        out[160] = S('Liversidge: no tooth staged yet' if lv['n'] == 0 else
                     'Liversidge: no tooth below H with a figure')
    out[171] = S('H teeth (%d): at least ' % lv['nh'], F2(lv['hmax']), ' yr, Table IX') if lv['nh'] else None
    w = willems(st, sx)
    if w['ok'] and w['ceil']:
        out[182] = S('Willems 2001: at the ceiling, >= ~15.8-16 yr')      # v3.9 (second review)
    elif w['ok']:
        if sx == 0:
            out[182] = S('Willems 2001: ', F2(w['mean']), ' yr (boys ', F2(w['sb']), ', girls ', F2(w['sg']), ')')
        else:
            out[182] = S('Willems 2001: ', F2(w['mean']), ' yr, %s, s.d. ' % SXW[sx], F1(w['sd']))
    elif w['staged'] < 7:
        out[182] = S('Willems 2001: %d of 7 staged (needs all 7)' % w['staged'])
    else:
        out[182] = S('Willems 2001: %s at %s: no %s score' % (FDI(w['bad']), STG[st[w['bad'] - 1] - 1],
                                                              "boys'" if w['badsx'] == 1 else "girls'"))
    return out, lv, w


def exp_tile(st, sx, i):
    """(letter, '>=' or None, value segments) for a staged tooth i"""
    s = st[i - 1]
    if s == 8:
        return STG[s - 1], '>=', F2(l_h(sx, i))      # the Table IX age as printed: a bound is not rounded up
    m = l_mean(sx, i, s)
    return STG[s - 1], None, (F1(m) if m is not None else ['-'])


# ===================================================================================== harness helpers
K = 'K'


def soft(n): return ('tap', int((n - 0.5) * 53.4), 230)
def stage(n): return ('tap', 6 + (n - 1) * 39 + 18, 113)
def tooth(i): return ('tap', (X1[i - 1] + X2[i - 1]) // 2, (Y1[i - 1] + Y2[i - 1]) // 2)


OPENING = set()       # programs that show the v3.9 opening page (one key) before the main menu


def run(prog, chooses, events=(), inputs=(), tag='', opening=None):
    h = Harness(prog, strict=True)
    h.choose(*chooses)
    if (prog in OPENING) if opening is None else opening:
        events = [K] + list(events)          # v3.9: the opening page, once per run
    for e in events:
        if e == 'K':
            h.press('Enter')
        elif e[0] == 'key':
            h.press(e[1])
        elif e[0] == 'tap':
            h.tap(e[1], e[2])
        elif e[0] == 'drag':
            h.drag(e[1])
    for a in inputs:
        h.answer(a)
    h.result = h.execute('FDAES()')
    lo = h.leftover()
    check('U script fully used (%s %s)' % (os.path.basename(prog), tag), not any(lo), repr(lo))
    if prog in OPENING:
        SCI.extend(h.sci_strings)
        ALLRUNS.append(h)
    return h


def title(s):
    t = [x for x in s.texts if x.y == 4 and x.font == 2]
    return t[0].text if t else ''


def page_lines(s):
    return [x.text for x in sorted(s.texts, key=lambda t: t.y) if x.font == 2 and x.x == 6 and 30 <= x.y <= 198]


def pages_titled(h, prefix):
    return [s for s in h.pages if title(s).startswith(prefix)]


ODO = 'MANDIBLE LEFT  Willems + Liversidge'
WTITLE = 'WILLEMS (2001): the published method'
LTITLE = 'LIVERSIDGE (2006): tooth by tooth'
TTITLE = 'TWO WAYS TO READ THE SAME TEETH'


def band_texts(s):
    """v3.9: the band's two Text items (line 1 at y 200 font 2, line 2 at y 214 font 1, x 10), or None"""
    t1 = [x for x in s.texts if x.y == 200 and x.font == 2 and x.x == 10]
    t2 = [x for x in s.texts if x.y == 214 and x.font == 1 and x.x == 10]
    if not t1 and not t2:
        return None
    return (t1[0] if t1 else None, t2[0] if t2 else None)


def band_line(s):
    b = band_texts(s)
    return None if b is None else ' | '.join(x.text if x else '-' for x in b)


def band_ok(s, p):
    """the v3.9 band on screen s is right for P(age >= 18) = p: line 2's text, line 1's verdict read off
    line 2's printed number by the rule, both in the verdict's colour, the RECT 4,199-315,226, and the footer
    at 228"""
    b = band_texts(s)
    if not b or b[0] is None or b[1] is None:
        return False
    t1, t2 = b
    v1, segs = band(p)
    if not matches(t2.text, segs) or t1.text not in v1:
        return False
    pr = t2.text[len('P(age >= 18)'):].split('%')[0].strip()
    pr = pr[2:] if pr.startswith('= ') else pr
    if t1.text != verdict(pr) or t1.hex != COLV[t1.text] or t2.hex != COLV[t1.text]:
        return False
    if not any(sh.cmd == 'RECT_P' and [int(a) for a in sh.args[:4]] == [4, 199, 315, 226] for sh in s.shapes):
        return False
    return any(t.y == 228 and t.x == 6 and t.font == 1 for t in s.texts)


SRC = open(NEW, encoding='utf-8').read()
SRCO = open(OLD, encoding='utf-8').read()          # v3.8a


def strip_comment(line):
    out, ins, i = [], False, 0
    while i < len(line):
        c = line[i]
        if c == '"':
            ins = not ins
        if not ins and line[i:i + 2] == '//':
            break
        out.append(c)
        i += 1
    return ''.join(out).rstrip()
OPENING.add(NEW)
X_ = '×'            # the multiplication sign, CHAR(215)
MLT = ' ' + X_ + ' '

# ===================================================================================== Part T
print('T. The tables')
# T1 the text layers, against the image transcription
wt = open(os.path.join(SRCDIR, 'willems2001.txt'), encoding='utf-8').read().split('\n')


def text_rows(lines, names, start):
    out = {}
    for l in lines[start:start + 16]:
        for n in names:
            if l.startswith(n) and n not in out:
                toks = l[len(n):].split()[:8]
                out[n] = [None if t == '...' else t for t in toks]
    return out


tb = text_rows(wt, W_TEETH, wt.index([l for l in wt if l.strip().startswith('TABLE 1')][0]))
tg = text_rows(wt, W_TEETH, wt.index([l for l in wt if l.strip().startswith('TABLE 2')][0]))
diffs = []
for tab, img, txt in (('Table 1 (boys)', W_BOYS, tb), ('Table 2 (girls)', W_GIRLS, tg)):
    for n in W_TEETH:
        for j in range(8):
            a, b = img[n][j], txt.get(n, [None] * 8)[j]
            if a != b:
                diffs.append((tab, n, STG[j], a, b))
print('   Willems: cells where the PDF text layer differs from the page image:')
for d in diffs:
    print('     %s, %s, stage %s: image %s, text layer %r' % d)
check('T Willems text layer differs from the image in exactly three cells, the girls\' negative scores, where it '
      'has the control character U+0002 in place of the minus sign',
      sorted((d[1], d[2]) for d in diffs) == [('First bicuspid', 'A'), ('First bicuspid', 'B'), ('Second bicuspid', 'A')]
      and all(d[0] == 'Table 2 (girls)' and d[3] == '-' + d[4][1:] and d[4][0] == '\x02' for d in diffs), repr(diffs))
check('T Willems text layer read all 7 rows of both tables', len(tb) == 7 and len(tg) == 7)
lt = open(os.path.join(SRCDIR, 'liv2006.txt'), encoding='utf-8').read().split('\n')
i10 = [i for i, l in enumerate(lt) if 'Table X. Mean ages of children' in l][0]
i9 = [i for i, l in enumerate(lt) if 'Table IX. Mean age (standard error)' in l][0]
lx_txt, l9_txt = {}, {}


def read_table(start, width, last, into):
    """rows 'tooth stage numbers...' from the text layer, from the table's caption to its last row"""
    cur = None
    for l in lt[start:start + 80]:
        f = l.split()
        # a tooth's first row carries its name ('C' is both the canine and a stage letter, so the
        # field count decides)
        if len(f) == width + 1 and f[0] in L_TEETH and f[1] in STG:
            cur = f[0]; f = f[1:]
        if cur and len(f) == width and f[0] in STG:
            into[(L_TEETH.index(cur) + 1, STG.index(f[0]) + 1)] = f[1:]
            if (cur, f[0]) == last:
                return


read_table(i10, 12, ('M2', 'G'), lx_txt)
read_table(i9, 6, ('M2', 'H'), l9_txt)
KEYS = ['gm', 'gse', 'gsd', 'gn', 'bm', 'bse', 'bsd', 'bn', 'cm', 'cse', 'csd']
dx = [(k, KEYS[j], LX[k][KEYS[j]], v[j]) for k, v in lx_txt.items() for j in range(11) if LX[k][KEYS[j]] != v[j]]
d9 = [(k, j, v) for k, v in l9_txt.items() for j, kk in enumerate(['gm', 'gse', 'bm', 'bse', 'diff']) if L9[k][kk] != v[j]]
print('   Liversidge Table X: %d rows in the text layer, %d in the image transcription; %d cells differ'
      % (len(lx_txt), len(LX), len(dx)))
print('   Liversidge Table IX: %d rows in the text layer, %d in the image transcription; %d cells differ'
      % (len(l9_txt), len(L9), len(d9)))
check('T Liversidge Table X: the text layer has the same 38 rows as the image transcription',
      sorted(lx_txt) == sorted(LX) and len(LX) == 38)
check('T Liversidge Table X: every cell of the text layer equals the image reading', not dx, repr(dx[:5]))
check('T Liversidge Table IX: the same 37 rows, every cell equal', sorted(l9_txt) == sorted(L9) and not d9
      and len(L9) == 37, repr(d9[:5]))
# T2 internal consistency of the reading
gsum = {sx: sum(D(t[6]) for t in tbl.values()) for sx, tbl in ((1, W_BOYS), (2, W_GIRLS))}
hsum = {sx: sum(D(t[7]) for t in tbl.values()) for sx, tbl in ((1, W_BOYS), (2, W_GIRLS))}
print('   Willems column sums: all seven at G %s / %s, at H %s / %s (boys / girls)' %
      (gsum[1], gsum[2], hsum[1], hsum[2]))
check('T Willems all seven at G sum to 11.74 (boys and girls)', gsum[1] == D('11.74') and gsum[2] == D('11.74'))
check('T Willems all seven at H sum to 16.03 (boys) and 15.79 (girls)', hsum[1] == D('16.03') and hsum[2] == D('15.79'))
check('T Willems: no score at A/B for the incisors and the first molar, in both tables (the paper\'s "...")',
      all(W_BOYS[n][j] is None and W_GIRLS[n][j] is None for n in ('Central incisor', 'First molar') for j in (0, 1)))
bad_se, off_c = [], []
for k, r in LX.items():
    for sfx, n in (('g', int(r['gn'])), ('b', int(r['bn'])), ('c', int(r['gn']) + int(r['bn']))):
        sd, se = float(r[sfx + 'sd']), float(r[sfx + 'se'])
        if abs(sd / math.sqrt(n) - se) > 0.0051 + 0.005 / math.sqrt(n):
            (off_c if sfx == 'c' else bad_se).append((L_TEETH[k[0] - 1] + ' ' + STG[k[1] - 1], sfx, sd, n, se,
                                                      round(sd / math.sqrt(n), 4)))
check('T Table X: every girls\' and boys\' SE = SD/sqrt(n) to the printed precision (76 cells)', not bad_se, repr(bad_se))
print('   Table X girls-and-boys SE against SD/sqrt(ng + nb): %d of 38 off by more than rounding: %s (the text layer '
      'prints the same; the pooled SE is the paper\'s own, not used by FDAES)' % (len(off_c), off_c))
check('T Table X: the girls-and-boys SE within 0.01 of SD/sqrt(ng + nb) everywhere (a reading check)',
      all(abs(r[2] / math.sqrt(r[3]) - r[4]) < 0.0101 for r in off_c))
bad_c = []
for k, r in LX.items():
    lo, hi = sorted((float(r['gm']), float(r['bm'])))
    wmean = (float(r['gm']) * int(r['gn']) + float(r['bm']) * int(r['bn'])) / (int(r['gn']) + int(r['bn']))
    if not (lo - 0.005 <= float(r['cm']) <= hi + 0.005) or abs(wmean - float(r['cm'])) > 0.03:
        bad_c.append((k, r['gm'], r['bm'], r['cm'], round(wmean, 3)))
check('T Table X: every girls-and-boys mean lies between the two sexes and within 0.03 of their n-weighted mean',
      not bad_c, repr(bad_c))
d9bad = [(k, r) for k, r in L9.items() if abs(float(r['bm']) - float(r['gm']) - float(r['diff'])) > 0.006]
print('   Table IX sex-difference column against boys minus girls: %d row(s) disagree: %s'
      % (len(d9bad), ', '.join('%s %s (printed %s, means differ by %.2f; the paper\'s own misprint, row not used)'
                                % (L_TEETH[k[0] - 1], STG[k[1] - 1], r['diff'], float(r['bm']) - float(r['gm']))
                                for k, r in d9bad)))
check('T Table IX: boys minus girls = the printed sex difference in every row but P1 G (the paper\'s own slip, '
      '0.96 for 0.69; not an H row, not used)', [k for k, r in d9bad] == [(4, 7)])
check('T Table IX: every H attainment age is later in boys than girls (so the girls\' value is the lower bound)',
      all(D(L9[(i, 8)]['bm']) > D(L9[(i, 8)]['gm']) for i in range(1, 8)))
check('T Table X has no H row, as the paper says', not any(k[1] == 8 for k in LX))
# T3 the program's tables, through its own look-ups, against the transcription
H = Harness(NEW, strict=True)
H.execute('fdTabs()')
bad = []
for ti in range(1, 8):
    for s in range(1, 9):
        for sx in (1, 2):
            v = H.execute('fdWSc(%d, %d, %d)' % (sx, ti, s))
            e = w_score(sx, ti, s)
            if (e is None and v != -99) or (e is not None and abs(v - float(e)) > 1e-12):
                bad.append(('W', sx, ti, s, v, e))
        for sx in (0, 1, 2):
            m, sd = H.execute('fdLvMn(%d, %d, %d)' % (sx, ti, s)), H.execute('fdLvSD(%d, %d, %d)' % (sx, ti, s))
            em, esd = l_mean(sx, ti, s), l_sd(sx, ti, s)
            if em is None:
                if m != 0 or sd != 0:
                    bad.append(('Lx', sx, ti, s, m, sd))
            elif abs(m - float(em)) > 1e-12 or abs(sd - float(esd)) > 1e-12:
                bad.append(('Lx', sx, ti, s, m, sd, em, esd))
    for sx in (0, 1, 2):
        v = H.execute('fdLvH(%d, %d)' % (sx, ti))
        if abs(v - float(l_h(sx, ti))) > 1e-12:
            bad.append(('L9', sx, ti, v))
check('T the program\'s tables equal the image transcription in every cell (fdWSc 7x8x2, fdLvMn and fdLvSD '
      '7x8x3, fdLvH 7x3)', not bad, repr(bad[:6]))
check('T fdLvH with the sex unknown gives the girls\' (earlier) age for every tooth',
      all(H.execute('fdLvH(0, %d)' % i) == H.execute('fdLvH(2, %d)' % i) for i in range(1, 8)))
for nm in ('fdWb', 'fdWg', 'fdLbM', 'fdLbS', 'fdLgM', 'fdLgS', 'fdLcM', 'fdLcS'):
    n = H.execute('SIZE(%s)' % nm)
    check('T %s has 56 entries (7 teeth x 8 stages)' % nm, n == 56, str(n))
check('T fdLhB and fdLhG have 7 entries', H.execute('SIZE(fdLhB)') == 7 and H.execute('SIZE(fdLhG)') == 7)
print('   Willems 2001 as transcribed (boys | girls), stages A-H; ... = no score:')
for n in W_TEETH:
    print('     %-16s %s | %s' % (n, ' '.join('%5s' % (v or '...') for v in W_BOYS[n]),
                                  ' '.join('%5s' % (v or '...') for v in W_GIRLS[n])))# ===================================================================================== Part N
print('N. The numbers: the program\'s routines against the independent implementation')


def cmp_w(st, sx):
    r = H.execute('fdWEst({%s}, %d)' % (','.join(map(str, st)), sx))
    e = willems(st, sx)
    if r[0] != e['ok']:
        return 'ok %r vs %r' % (r[0], e['ok'])
    if e['ok']:
        if abs(r[1] - float(e['mean'])) > 1e-9 or abs(r[2] - float(e['sd'])) > 1e-9:
            return 'mean/sd %r %r vs %s %s' % (r[1], r[2], e['mean'], e['sd'])
        if abs(r[3] - e['p']) > 1e-9 + 1e-6 * e['p']:
            return 'P %r vs %r' % (r[3], e['p'])
        if sx in (0, 1) and abs(r[4] - float(e['sb'])) > 1e-9:
            return 'boys sum'
        if sx in (0, 2) and abs(r[5] - float(e['sg'])) > 1e-9:
            return 'girls sum'
        if len(r) != 11 or r[10] != (1 if (e['ok'] and e['ceil']) else 0):   # v3.9: the ceiling flag, element 11
            return 'ceiling flag %r vs %r' % (r[10:], e.get('ceil'))
    else:
        if (r[6], r[7], r[8], r[9]) != (e['staged'], e['bad'], e['why'], e['badsx']):
            return 'problem %r vs %r' % (r[6:], (e['staged'], e['bad'], e['why'], e['badsx']))
        if len(r) != 11 or r[10] != 0:
            return 'all-H flag on a staging with no age'
    return None


def cmp_l(st, sx):
    r = H.execute('fdLvEst({%s}, %d)' % (','.join(map(str, st)), sx))
    e = liversidge(st, sx)
    if (r[0], r[5], r[7], r[8]) != (e['k'], e['nh'], e['nno'], e['n']):
        return 'counts %r vs %r' % ((r[0], r[5], r[7], r[8]), (e['k'], e['nh'], e['nno'], e['n']))
    if abs(r[6] - float(e['hmax'])) > 1e-9:
        return 'hmax'
    if e['k']:
        for a, b in ((r[1], e['est']), (r[2], e['sei']), (r[3], e['sec'])):
            if abs(a - float(b)) > 1e-9:
                return 'est/SE %r vs %r' % (r[1:4], (e['est'], e['sei'], e['sec']))
        if abs(r[4] - e['p']) > 1e-12 + 1e-6 * e['p']:
            return 'P %r vs %r' % (r[4], e['p'])
    elif any(r[1:5]):
        return 'k = 0 but numbers'
    return None


rng = random.Random(38)
STAGINGS = []
for k in range(1000):
    mode = k % 4
    if mode == 0:      # anything, gaps allowed
        st = [rng.choice([0, 0] + list(range(1, 9))) for _ in range(7)]
    elif mode == 1:    # all seven staged, any stage
        st = [rng.randint(1, 8) for _ in range(7)]
    elif mode == 2:    # all seven at a stage with a printed score in both tables (a Willems age)
        st = [rng.choice([s for s in range(1, 9) if w_score(1, i, s) is not None and w_score(2, i, s) is not None])
              for i in range(1, 8)]
    else:              # a child-like staging: stages rise from the incisors to the molars, H sometimes
        base = rng.randint(2, 8)
        st = [max(1, min(8, base + rng.choice([-1, 0, 0, 1]) + (1 if i in (1, 2, 6) else 0) - (1 if i == 7 else 0)))
              for i in range(1, 8)]
    STAGINGS.append(st)
nw = nl = 0
badw, badl = [], []
for st in STAGINGS:
    for sx in (0, 1, 2):
        e = cmp_w(st, sx)
        if e:
            badw.append((st, sx, e))
        e = cmp_l(st, sx)
        if e:
            badl.append((st, sx, e))
        nw += 1; nl += 1
check('N fdWEst = the independent Willems for %d random stagings x 3 sexes' % len(STAGINGS), not badw, repr(badw[:3]))
check('N fdLvEst = the independent Liversidge for %d random stagings x 3 sexes' % len(STAGINGS), not badl, repr(badl[:3]))
ok_counts = [sum(1 for st in STAGINGS if willems(st, sx)['ok']) for sx in (0, 1, 2)]
print('   %d stagings x 3 sexes; with a Willems age: %r (sex 0, 1, 2); with a Liversidge estimate: %r'
      % (len(STAGINGS), ok_counts, [sum(1 for st in STAGINGS if liversidge(st, sx)['k']) for sx in (0, 1, 2)]))
# fdWSum for both sexes directly
bs = [(st, sx) for st in STAGINGS[:300] for sx in (1, 2)
      if (lambda r, e: r[0] != e['ok'] or (e['ok'] and abs(r[1] - float(e['sum'])) > 1e-9)
          or (not e['ok'] and (r[3], r[4]) != (e['bad'], e['why']))
          or len(r) != 6 or r[5] != (1 if (e['ok'] and ceiling(st)) else 0))(
          H.execute('fdWSum({%s}, %d)' % (','.join(map(str, st)), sx)), willems_one(st, sx))]
check('N fdWSum = the independent sum, tooth by tooth problems included, and (v3.9) the ceiling flag, element 6 '
      '(300 stagings x 2 tables)', not bs, repr(bs[:3]))
# v3.9 (C-F1; the second review's near-ceiling rule): the ceiling flag when 33-37 are all at H
CEIL = ([8] * 7, [7, 7, 8, 8, 8, 8, 8], [7, 8, 8, 8, 8, 8, 8], [8, 7, 8, 8, 8, 8, 8], [6, 5, 8, 8, 8, 8, 8],
        [3, 8, 8, 8, 8, 8, 8])
fl = [(st, sx, H.execute('fdWEst({%s}, %d)' % (','.join(map(str, st)), sx))[10]) for st in CEIL for sx in (0, 1, 2)]
check('N v3.9: fdWEst element 11 = 1 when teeth 33-37 are all at H, whatever 31 and 32 (%d stagings x 3 sexes, all '
      'scored)' % len(CEIL), all(v == 1 for _, _, v in fl), repr([x for x in fl if x[2] != 1]))
nf = [(st, sx) for st in ([8, 8, 8, 8, 8, 8, 7], [8, 8, 7, 8, 8, 8, 8], [8, 8, 8, 0, 8, 8, 8], [8, 8, 8, 8, 8, 7, 8],
                          [8, 8, 8, 8, 7, 8, 8])
      for sx in (0, 1, 2) if H.execute('fdWEst({%s}, %d)' % (','.join(map(str, st)), sx))[10] != 0]
check('N v3.9: element 11 = 0 when any of 33-37 is below H or unstaged (5 stagings x 3 sexes)', not nf, repr(nf))
rw_ = random.Random(1933)
wc = [tuple(rw_.randint(0, 8) for _ in range(7)) for _ in range(1500)] + \
     [tuple([rw_.randint(0, 8), rw_.randint(0, 8)] + [8] * 5) for _ in range(150)] + \
     [tuple([rw_.randint(0, 8), rw_.randint(0, 8)] + [8] * 4 + [7]) for _ in range(50)]
wcb = [st for st in wc if H.call('fdWCeil', list(map(float, st))) != (1 if ceiling(st) else 0)]
check('N v3.9: fdWCeil, the ONE named rule, = "33-37 all at H" on %d stagings (and on all %d ceiling stagings of '
      'the list above)' % (len(wc), len(CEIL)), not wcb and all(H.call('fdWCeil', list(map(float, st))) == 1
                                                               for st in CEIL), repr(wcb[:3]))
check('N v3.9: the rule lives in ONE place: fdWSum calls fdWCeil, and nothing else tests a stage against 8 for '
      'Willems', 'wuH := fdWCeil(wuSt);' in SRC and 'IF wuSt(wuI) < 8' not in SRC and SRC.count('fdWCeil(') == 2)
# the largest sums any staging gives (independent: each tooth's largest printed score)
mx = {sx: sum(max(D(v) for v in (W_BOYS if sx == 1 else W_GIRLS)[t] if v is not None) for t in W_TEETH)
      for sx in (1, 2)}
arg = {sx: [max(range(1, 9), key=lambda s, t=t: (w_score(sx, t, s) if w_score(sx, t, s) is not None else D(-99), s))
            for t in range(1, 8)] for sx in (1, 2)}
check('N v3.9 (second review): the largest sums any staging gives are %s (boys, all H) and %s (girls: 31 and 32 at G, '
      '3.19 > 3.14 and 0.79 > 0.70; all-H girls 15.79), and the program sums them so'
      % (mx[1], mx[2]), mx[1] == D('16.03') and mx[2] == D('15.93') and arg[1] == [8] * 7 and
      arg[2] == [7, 7, 8, 8, 8, 8, 8] and abs(H.execute('fdWSum({7,7,8,8,8,8,8}, 2)')[1] - 15.93) < 1e-9 and
      abs(H.execute('fdWSum({8,8,8,8,8,8,8}, 2)')[1] - 15.79) < 1e-9, repr((mx, arg)))
check('N v3.9: fdWSum element 6 = 1 at all H and with 31, 32 at G for both tables, 0 with 37 at G',
      H.execute('fdWSum({8,8,8,8,8,8,8}, 1)')[5] == 1 and H.execute('fdWSum({8,8,8,8,8,8,8}, 2)')[5] == 1
      and H.execute('fdWSum({7,7,8,8,8,8,8}, 2)')[5] == 1 and H.execute('fdWSum({8,8,8,8,8,8,7}, 1)')[5] == 0)
# edge cases
EDGE = {}
for miss in range(1, 8):
    st = [7] * 7; st[miss - 1] = 0
    EDGE['G but %s missing' % FDI(miss)] = st
for ti in range(1, 8):
    for s in range(1, 9):
        if w_score(1, ti, s) is None or w_score(2, ti, s) is None:
            st = [7] * 7; st[ti - 1] = s
            EDGE['G but %s at %s' % (FDI(ti), STG[s - 1])] = st
EDGE['all H'] = [8] * 7
EDGE['all A'] = [1] * 7
EDGE['all G'] = [7] * 7
EDGE['nothing staged'] = [0] * 7
EDGE['31 at C only (no figure)'] = [3, 0, 0, 0, 0, 0, 0]
EDGE['37 H, 31 E (floor above)'] = [5, 0, 0, 0, 0, 0, 8]
EDGE['the self-check boy'] = [0, 6, 7, 5, 0, 0, 0]
EDGE['32 C, rest G'] = [7, 3, 7, 7, 7, 7, 7]
EDGE['33 C, rest G'] = [7, 7, 3, 7, 7, 7, 7]
EDGE['negative scores: 34 A, 35 A, rest G'] = [7, 7, 7, 1, 1, 7, 7]
EDGE['the youngest Willems ages'] = [3, 4, 4, 1, 1, 4, 1]
be = []
for nm, st in EDGE.items():
    for sx in (0, 1, 2):
        for f in (cmp_w, cmp_l):
            e = f(st, sx)
            if e:
                be.append((nm, sx, f.__name__, e))
check('N every edge case (%d stagings x 3 sexes): both routines = independent' % len(EDGE), not be, repr(be[:4]))
check('N missing tooth: no Willems age for any sex, the tooth named, why = not staged',
      all(willems(EDGE['G but %s missing' % FDI(m)], sx)['ok'] == 0 and
          H.execute('fdWEst({%s}, %d)' % (','.join(map(str, EDGE['G but %s missing' % FDI(m)])), sx))[7:9] == [m, 1]
          for m in range(1, 8) for sx in (0, 1, 2)))
check('N girls\' negative scores enter the sum: 34 A + 35 A + rest at G, girls = 11.74 - 1.58 - 0.55 - 0.95 - 0.19',
      abs(H.execute('fdWEst({7,7,7,1,1,7,7}, 2)')[1] - (11.74 - 1.58 - 0.55 - 0.95 - 0.19)) < 1e-9)
check('N sex unknown: 32 at C (boys 0.55, girls "...") gives no age, naming the girls\' table',
      H.execute('fdWEst({7,3,7,7,7,7,7}, 0)')[0] == 0 and H.execute('fdWEst({7,3,7,7,7,7,7}, 0)')[7:10] == [2, 2, 2])
check('N sex unknown: 33 at C (boys "...", girls 0.6) gives no age, naming the boys\' table',
      H.execute('fdWEst({7,7,3,7,7,7,7}, 0)')[7:10] == [3, 2, 1])
check('N boys: 33 at C has no score; girls: 33 at C = 0.6 (sum 11.74 - 1.72 + 0.6)',
      H.execute('fdWEst({7,7,3,7,7,7,7}, 1)')[0] == 0 and
      abs(H.execute('fdWEst({7,7,3,7,7,7,7}, 2)')[1] - (11.74 - 1.72 + 0.6)) < 1e-9)
r = H.execute('fdWEst({7,7,7,7,7,7,7}, 0)')
check('N all G, sex unknown: mixture mean 11.74, SD sqrt((0.81 + 1.69)/2) = 1.1180',
      abs(r[1] - 11.74) < 1e-9 and abs(r[2] - math.sqrt(1.25)) < 1e-9)
r = H.execute('fdWEst({8,8,8,8,8,8,8}, 0)')
check('N all H, sex unknown: mean (16.03 + 15.79)/2 = 15.91, SD sqrt(1.25 + 0.12^2)',
      abs(r[1] - 15.91) < 1e-9 and abs(r[2] - math.sqrt(1.25 + 0.0144)) < 1e-9)
check('N all H, sex unknown: P = the average of the two sexes\' P (not a normal approximation)',
      abs(r[3] - (0.5 * norm.sf(18, 16.03, 0.9) + 0.5 * norm.sf(18, 15.79, 1.3))) < 1e-12 and
      abs(r[3] - norm.sf(18, 15.91, r[2])) > 1e-4)
r = H.execute('fdLvEst({8,8,8,8,8,8,8}, 1)')
check('N all H: no Liversidge estimate (k = 0), 7 at H, floor = boys\' M2 15.25', r[0] == 0 and r[5] == 7 and abs(r[6] - 15.25) < 1e-12)
r = H.execute('fdLvEst({8,8,8,8,8,8,8}, 0)')
check('N all H, sex unknown: floor = girls\' M2 14.78 (the earlier)', abs(r[6] - 14.78) < 1e-12)
r = H.execute('fdLvEst({3,0,0,0,0,0,0}, 2)')
check('N 31 at C only: k = 0, one tooth with no figure, no estimate', r[0] == 0 and r[7] == 1 and r[8] == 1 and r[1] == 0)
r = H.execute('fdLvEst({1,1,1,1,1,1,1}, 1)')
check('N all A: only P2 A and M2 A have Table X figures (k = 2), five without', r[0] == 2 and r[7] == 5)
check('N P(age >= 18) is a lower tail in the program: a tiny P survives (the self-check boy: ~2e-15, not 0)',
      0 < H.execute('fdLvEst({0,6,7,5,0,0,0}, 1)')[4] < 1e-12)# ===================================================================================== Part U
print('U. The screens: full sessions in the harness')
SEXC = {0: 1, 1: 2, 2: 3}       # Setup CHOOSE item for sex 0, 1, 2


def session(st, sx, extra_after=None, pool='No', tag=''):
    """Setup, the odontogram by taps (tooth, then stage, in order 31..37), Done, the two pages,
    the pool question (answered 'No' unless told), Exit.  Returns (h, expected)."""
    W, pw, w = exp_willems_page(st, sx)
    L, pl, lv = exp_liv_page(st, sx)
    ev = [K]
    for i, s in enumerate(st, 1):
        if s:
            ev += [tooth(i), stage(s)]
    ev += [soft(6)]
    ch = [1, SEXC[sx], 1, 2]
    if any(st):
        ev += [K] * npages(W, pw) + [K] * npages(L, pl)
        okw, okl = w['ok'] == 1 and not w['ceil'], lv['k'] > 0          # v3.9 (D7): the ceiling is not offered
        items = (['Willems 2001 (sum)'] if okw else []) + (['Liversidge 2006 (per tooth)'] if okl else [])
        items += (['No'] if (okw or okl) else ['OK']) + ['Two ways to read the teeth']
        ch.append(items.index(pool if pool in items else items[-2]) + 1)
        if extra_after:
            ch, ev = extra_after(ch, ev, items)
    ch.append(7)                                   # v3.9: Exit is item 7
    ev.append(K)
    h = run(NEW, ch, ev, tag=tag)
    return h, (W, pw, w, L, pl, lv)


def same_rows(pages, L, p):
    """every expected line at its row (page, y = 30 + 14 x row; a blank line draws nothing) and nothing else"""
    per = 12 if p >= 0 else 13
    want = [(i // per, 30 + 14 * (i % per), segs) for i, segs in enumerate(L) if first(segs) != '']
    got = [(pi, t.y, t.text) for pi, pg in enumerate(pages)
           for t in sorted(pg.texts, key=lambda t: t.y) if t.font == 2 and t.x == 6 and 30 <= t.y <= 198]
    bad = [(g, (w[0], w[1], first(w[2]))) for g, w in itertools.zip_longest(got, want, fillvalue=(None, None, ''))
           if g[0] != w[0] or g[1] != w[1] or not matches(g[2], w[2])]
    return not bad, bad


def check_session(h, st, sx, exp, tag):
    W, pw, w, L, pl, lv = exp
    wp, lp = pages_titled(h, WTITLE), pages_titled(h, LTITLE)
    if not any(st):
        check('U nothing staged: no result page, the MSGBOX ' + tag,
              not wp and not lp and [m.lines for m in h.msgboxes] == [['No teeth staged. Nothing stored.']],
              repr([m.lines for m in h.msgboxes]))
        return
    okw, dw = same_rows(wp, W, pw)
    okl, dl = same_rows(lp, L, pl)
    check('U Willems page = independent ' + tag, okw, repr(dw[:3]))
    check('U Liversidge page = independent ' + tag, okl, repr(dl[:3]))
    check('U page counts (Willems %d, Liversidge %d) ' % (npages(W, pw), npages(L, pl)) + tag,
          len(wp) == npages(W, pw) and len(lp) == npages(L, pl))
    # the verdict bands: on every page of a result with a number, none without
    for pages, p in ((wp, pw), (lp, pl)):
        if p >= 0:
            check('U verdict band (v3.9: two lines, cut-points 5% / 95%) = independent P ' + tag,
                  all(band_ok(x, p) for x in pages), repr([band_line(x) for x in pages]))
        else:
            check('U no verdict band without a number (v3.9: nor at the Willems ceiling, nor under an H floor '
                  'above the Liversidge estimate) ' + tag, all(band_line(x) is None for x in pages))
    # the last odontogram frame: tiles and panel
    fr = pages_titled(h, ODO)[-1]
    sel = max([i for i, s in enumerate(st, 1) if s] or [0])
    ep, _, _ = exp_panel(st, sx, sel)
    bad = []
    for y, segs in ep.items():
        t = [x for x in fr.texts if x.y == y and x.font == 1 and x.x == 8]
        if segs is None:
            if t:
                bad.append((y, t[0].text, None))
        elif not t or not matches(t[0].text, segs):
            bad.append((y, t[0].text if t else None, first(segs)))
    check('U odontogram panel lines = independent ' + tag, not bad, repr(bad))
    bad = []
    for i in range(1, 8):
        cx = (X1[i - 1] + X2[i - 1]) // 2
        tt = [x for x in fr.texts if X1[i - 1] <= x.x <= X2[i - 1] and Y1[i - 1] <= x.y <= Y2[i - 1]]
        fdi = [x for x in tt if x.y == Y1[i - 1] + 3 and x.text == FDI(i)]
        if not fdi:
            bad.append((i, 'FDI'))
        s = st[i - 1]
        if s:
            let, ge, val = exp_tile(st, sx, i)
            lt_ = [x for x in tt if x.y == Y1[i - 1] + 14 and x.font == 2]
            gt_ = [x for x in tt if x.y == Y1[i - 1] + 27]
            vt_ = [x for x in tt if x.y == Y1[i - 1] + 38]
            if not lt_ or lt_[0].text != let:
                bad.append((i, 'letter', lt_ and lt_[0].text))
            if (ge is None) != (not gt_) or (gt_ and gt_[0].text != '>='):
                bad.append((i, '>=', gt_ and gt_[0].text))
            if not vt_ or vt_[0].text not in val or vt_[0].x != cx - 3 * len(vt_[0].text):
                bad.append((i, 'value', vt_ and (vt_[0].text, vt_[0].x), val))
        elif len(tt) != 1:
            bad.append((i, 'unstaged tile has text', [x.text for x in tt]))
    check('U all seven tiles: FDI number, stage letter, ">=" at H, Liversidge age (or "-") ' + tag, not bad, repr(bad))
    # the axis marks: Liversidge's bar and square, the H arrow, Willems's post
    sh = [(x.cmd, list(x.args)) for x in fr.shapes]
    blue, mag = 0x003CC8, 0xC800C8
    if lv['k']:
        xa, xb, xm = axis_x(lv['est'] - lv['sec']), axis_x(lv['est'] + lv['sec']), axis_x(lv['est'])
        okb = ('LINE_P', [xa, 197, xb, 197, blue]) in [(c, a[:5]) for c, a in sh] and \
              any(c == 'RECT_P' and a[:4] == [xm - 2, 195, xm + 2, 199] for c, a in sh)
    else:
        okb = not any(c == 'LINE_P' and a[1] == 197 and a[3] == 197 and a[4] == blue for c, a in sh)
    check('U Liversidge on the axis: +/- the larger SE in blue, the estimate as a square (or nothing) ' + tag, okb)
    if lv['nh']:
        xh = axis_x(lv['hmax'])
        okh = ('LINE_P', [xh, 194, xh + 7, 194, blue]) in [(c, a[:5]) for c, a in sh]
    else:
        okh = not any(c == 'LINE_P' and a[1] == 194 and a[3] == 194 for c, a in sh)
    check('U the H floor on the axis as a blue arrow (or none) ' + tag, okh)
    if w['ok']:
        xw = axis_x(w['mean'])
        okw2 = ('LINE_P', [xw, 193, xw, 201, mag]) in [(c, a[:5]) for c, a in sh]     # v3.8a: 193 (was 191)
        # v3.9: at the ceiling the mark gets an arrow pointing older, and only there
        arrow = ('LINE_P', [xw + 1, 197, xw + 8, 197, mag]) in [(c, a[:5]) for c, a in sh]
        okw2 = okw2 and (arrow == bool(w['ok'] and w['ceil']))
    else:
        okw2 = not any(c == 'LINE_P' and a[4] == mag and a[1] in (191, 193) for c, a in sh)
    check('U Willems on the axis as a magenta post (only with a Willems age) ' + tag, okw2)


n_sess = 0
for k, st in enumerate(STAGINGS[:60]):
    sx = k % 3
    h, exp = session(st, sx, tag='random %d sex %d %r' % (k, sx, st))
    check_session(h, st, sx, exp, 'random %d sex %d %r' % (k, sx, st))
    n_sess += 1
for nm, st in EDGE.items():
    for sx in (0, 1, 2):
        h, exp = session(st, sx, tag='edge %s sex %d' % (nm, sx))
        check_session(h, st, sx, exp, 'edge %s sex %d' % (nm, sx))
        n_sess += 1
print('   %d full sessions (60 random, %d edge stagings x 3 sexes)' % (n_sess, len(EDGE)))
# Cancel: nothing computed, nothing said
h = run(NEW, [2, 7], [tooth(1), stage(7), soft(5), K], tag='cancel')
check('U Cancel (soft key 5): no result page, no pool question, no MSGBOX',
      not pages_titled(h, WTITLE) and not [c for c in h.chooses if 'pool' in c.title] and not h.msgboxes)
h = run(NEW, [2, 7], [tooth(1), stage(7), ('key', 'Esc'), K], tag='Esc')
check('U Esc = Cancel', not pages_titled(h, WTITLE) and not h.msgboxes)
# the keys: Right to 7 (stops there), Enter menu on each, Up/Down, Left, re-tap, Clear, +
ev, ch = [], [2]
for i in range(1, 8):
    ev += [('key', 'Right'), K]
    ch.append(8)                                   # G via the Enter menu (item 8 = "G  ...")
ev += [('key', 'Right'), ('key', 'Up'), ('key', 'Down'), ('key', 'Down'), ('key', 'Up')]   # 37: G->H->G->F->G
ev += [('key', 'Left')] * 9 + [('key', 'Up')]      # stops at 31: G -> H
ev += [('key', 'Plus')]
st_exp = [8, 7, 7, 7, 7, 7, 7]
W, pw, w = exp_willems_page(st_exp, 0)
L, pl, lv = exp_liv_page(st_exp, 0)
ev += [K] * (npages(W, pw) + npages(L, pl))
ch += [3, 7]
ev += [K]
h = run(NEW, ch, ev, tag='keys')
ent = [c for c in h.chooses if c.title in WTN]
check('U the Enter menu was asked for all seven teeth, 31 first, with "Not staged" + the eight labels',
      [c.title for c in ent] == WTN and all(c.items == ['Not staged (skip this tooth)'] + LABELS for c in ent))
check('U Right stops at 37, Left at 31; Up/Down step the stage; + = Done (31 H, the rest G)',
      [l for p in pages_titled(h, WTITLE) for l in page_lines(p)][1] == 'Stages: 31H 32G 33G 34G 35G 36G 37G')
# re-tap a stage un-stages; Clear un-stages all
h = run(NEW, [2, 2, 7], [tooth(1), stage(4), stage(4), tooth(3), stage(2), soft(1), tooth(5), stage(6),
                         soft(6)] + [K] * 3, tag='retap/clear')
wl = [l for p in pages_titled(h, WTITLE) for l in page_lines(p)]
check('U tapping the same stage again un-stages; Clear un-stages every tooth (only 35 F remains)',
      'Needs all seven teeth; not staged:' in wl and '31, 32, 33, 34, 36, 37' in wl, repr(wl[:8]))
fr0 = [p for p in pages_titled(h, ODO)]
check('U the help lines when no tooth is selected (three; v3.9: the first points to the help topics)',
      [t.text for t in fr0[0].texts if t.x == 8 and 97 <= t.y <= 130] ==
      ['Tap a tooth, then its stage. Help: main menu.', 'Keys: arrows pick a tooth, Up/Down its stage,',
       'Enter = stage menu, + = Done, Esc = Cancel.'] and not any('grey' in t.text for p in h.pages for t in p.texts))
check('U 31 is a normal tile: white with a grey edge when not staged, never the old greyed tile',
      not any(sh.cmd == 'RECT_P' and list(sh.args[4:6]) == [0xF0F0F0, 0xF0F0F0] for p in fr0 for sh in p.shapes))
wscr = [x for x in h.screens if x.func == 'fdOdonto' and x.reason == 'wait']
check('U the soft keys (painted after each blit) are Clear, Cancel, Done as before',
      wscr and all(x.menu == ['Clear', '', '', '', 'Cancel', 'Done'] for x in wscr))
check('U the title band names both methods', all(title(p) == ODO for p in fr0))
# the teaching page from the pool question, then the question again
st = [7] * 7


def teach_then_no(ch, ev, items):
    ch = ch[:-1] + [items.index('Two ways to read the teeth') + 1, items.index('No') + 1]
    return ch, ev + [K, K]


h, exp = session(st, 1, extra_after=teach_then_no, tag='teaching page from the pool question')
tp = pages_titled(h, TTITLE)
pq = [c for c in h.chooses if c.title == 'Add to Bayesian pool?']
check('U the pool question\'s last item opens "Two ways to read the same teeth" (2 pages) and asks again',
      len(tp) == 2 and len(pq) == 2 and pq[0].items == pq[1].items and not h.msgboxes)
TWO = [l for p in tp for l in page_lines(p)]
check('U the teaching page: Willems sums fitted scores (some negative); Liversidge per tooth; no dividing by '
      'sqrt(n); the in-stage mean depends on the sample\'s ages; pool one, not both',
      any('adds seven scores' in l for l in TWO) and any('negative' in l for l in TWO) and
      any('sqrt(k)' in l for l in TWO) and any('ages of the children sampled' in l for l in TWO) and
      any('Pool one or the other, not both' in l for l in TWO), repr(TWO))
check('U the teaching page: every line <= 37 characters', all(len(l) <= 37 for l in TWO))
# no Willems and no Liversidge: "Nothing to add to the pool"
h, exp = session([3, 0, 0, 0, 0, 0, 0], 1, tag='nothing to pool')
nq = [c for c in h.chooses if c.title == 'Nothing to add to the pool']
check('U nothing computed: "Nothing to add to the pool" with OK and the teaching page',
      nq and nq[0].items == ['OK', 'Two ways to read the teeth'] and not h.msgboxes)
# the pool question offers only what was computed
offers = {}
for nm, st, sx in (('both', [7] * 7, 1), ('Willems only', [8, 8, 8, 1, 8, 8, 8], 1),
                   ('Liversidge only', [7, 7, 7, 0, 7, 7, 7], 2), ('neither', [3, 0, 0, 0, 0, 0, 0], 0),
                   ('ceiling, boys', [8] * 7, 1), ('ceiling, girls', [8] * 7, 2), ('ceiling, sex unknown', [8] * 7, 0),
                   ('near ceiling (31 C), boys', [3, 8, 8, 8, 8, 8, 8], 1),
                   ('near ceiling (31, 32 G), girls', [7, 7, 8, 8, 8, 8, 8], 2)):
    h, exp = session(st, sx, tag='offers ' + nm)
    q = [c for c in h.chooses if c.title in ('Add to Bayesian pool?', 'Nothing to add to the pool')]
    offers[nm] = q[0].items if q else None
check('U the pool question offers only what was computed (v3.9, D7: never the Willems ceiling, now 33-37 at H; all seven at H '
      'also leaves Liversidge with only a floor, so nothing is offered)',
      offers == {'both': ['Willems 2001 (sum)', 'Liversidge 2006 (per tooth)', 'No', 'Two ways to read the teeth'],
                 'Willems only': ['Willems 2001 (sum)', 'No', 'Two ways to read the teeth'],
                 'Liversidge only': ['Liversidge 2006 (per tooth)', 'No', 'Two ways to read the teeth'],
                 'neither': ['OK', 'Two ways to read the teeth'],
                 'ceiling, boys': ['OK', 'Two ways to read the teeth'],
                 'ceiling, girls': ['OK', 'Two ways to read the teeth'],
                 'ceiling, sex unknown': ['OK', 'Two ways to read the teeth'],
                 'near ceiling (31 C), boys': ['OK', 'Two ways to read the teeth'],
                 'near ceiling (31, 32 G), girls': ['Liversidge 2006 (per tooth)', 'No',
                                                    'Two ways to read the teeth']}, repr(offers))# ===================================================================================== Part E
print('E. The worked examples')
for sx, nm in ((1, 'boys'), (2, 'girls')):
    h, exp = session([7] * 7, sx, tag='all G ' + nm)
    wl = [l for p in pages_titled(h, WTITLE) for l in page_lines(p)]
    check('E all seven at G, %s: "= Dental age 11.74 yr"' % nm, '= Dental age 11.74 yr' in wl, repr(wl))
    h, exp = session([8] * 7, sx, tag='all H ' + nm)
    wl = [l for p in pages_titled(h, WTITLE) for l in page_lines(p)]
    # v3.9 (C-F1): the ceiling, not a dental age
    want = 'Sum %s yr; the largest any' % ('16.03' if sx == 1 else '15.79')
    check('E all seven at H, %s: "= All seven at H: the tables\' ceiling", "%s", "staging gives: 16.03 boys, 15.93", '
          '"at least about 15.8-16", no "= Dental age"' % (nm, want),
          "= All seven at H: the tables' ceiling" in wl and want in wl and 'staging gives: 16.03 boys, 15.93' in wl
          and "only 'at least about 15.8-16'." in wl and not any('Dental age' in l for l in wl), repr(wl))
    fr = pages_titled(h, ODO)[-1]
    t36 = [x.text for x in fr.texts if X1[5] <= x.x <= X2[5] and x.y == Y1[5] + 38]
    t37 = [x.text for x in fr.texts if X1[6] <= x.x <= X2[6] and x.y == Y1[6] + 38]
    check('E all seven at H, %s: the tiles show Table IX\'s age as printed, never rounded up (36: %s, 37: %s)'
          % (nm, '9.97' if sx == 1 else '9.30', '15.25' if sx == 1 else '14.78'),
          t36 == ['9.97' if sx == 1 else '9.30'] and t37 == ['15.25' if sx == 1 else '14.78'], repr((t36, t37)))
    ll = [l for p in pages_titled(h, LTITLE) for l in page_lines(p)]
    check('E all seven at H, %s: Liversidge gives no estimate, only "at least %s"' % (nm, '15.25' if sx == 1 else '14.78'),
          ('= At least %s yr (Table IX: the' % ('15.25' if sx == 1 else '14.78')) in ll and
          not any(l.startswith('= Mean of') for l in ll), repr(ll))
h, exp = session([7] * 7, 0, tag='all G unknown')
wl = [l for p in pages_titled(h, WTITLE) for l in page_lines(p)]
check('E all seven at G, sex unknown: both sums 11.74, mean 11.74, mixture SD 1.12',
      'Boys  (Table 1): sum 11.74 yr' in wl and 'Girls (Table 2): sum 11.74 yr' in wl and
      '= Dental age 11.74 yr (their mean)' in wl and '50:50 mixture: SD 1.12 yr' in wl, repr(wl))
h, exp = session([0, 6, 7, 5, 0, 0, 0], 1, tag='the Liversidge example')
ll = [l for p in pages_titled(h, LTITLE) for l in page_lines(p)]
check('E the Liversidge example (boy, I2 F, C G, P1 E): 7.49, 12.02, 8.35 -> 9.29 yr; SE 0.65 and 1.11',
      ll[2:5] == ['32 F  7.49 yr  SD 0.95', '33 G  12.02 yr  SD 1.33', '34 E  8.35 yr  SD 1.05'] and
      '= Mean of 3 teeth: 9.29 yr' in ll and 'SE if independent: 0.65 yr' in ll and
      'SE if they move together: 1.11 yr' in ll, repr(ll))
ex = liversidge([0, 6, 7, 5, 0, 0, 0], 1)
print('   by hand: (7.49 + 12.02 + 8.35)/3 = %s; sqrt(0.95^2 + 1.33^2 + 1.05^2)/3 = %s; (0.95 + 1.33 + 1.05)/3 = %s'
      % (ex['est'].quantize(Decimal('0.0001')), ex['sei'].quantize(Decimal('0.0001')), ex['sec'].quantize(Decimal('0.0001'))))
check('E by hand, exactly: 27.86/3 = 9.2867, sqrt(3.7739)/3 = 0.6476, 3.33/3 = 1.11',
      abs(ex['est'] - D('27.86') / 3) < D('1e-20') and abs(ex['sei'] - D('3.7739').sqrt() / 3) < D('1e-20')
      and ex['sec'] == D('1.11'))
# the Verify Calculations pages
hv = run(NEW, [6, 6, 7], [K] * 7, tag='self-check')          # v3.9: More = 6, Exit = 7; six pages
sc3 = page_lines(pages_titled(hv, 'ARITHMETIC SELF-CHECK  (5)')[0])   # v3.8a's pages 3 and 4 are 5 and 6
sc4 = page_lines(pages_titled(hv, 'ARITHMETIC SELF-CHECK  (6)')[0])
check('E self-check page 5 (v3.8a\'s 3): Willems at G from the program\'s tables, 11.74 / 11.74, and at H 16.03 / 15.79',
      sc3[6:] == ['WILLEMS 2001, all seven teeth at G:', 'boys:  sum of Table 1 = 11.74 yr',
                  'girls: sum of Table 2 = 11.74 yr', 'All seven at H: 16.03 / 15.79 yr',
                  'By hand: 11.74, 11.74; 16.03 / 15.79', '(each a column of the paper summed)'], repr(sc3))
check('E self-check page 6 (v3.8a\'s 4): the Liversidge example from the program\'s tables',
      sc4 == ['LIVERSIDGE 2006 Table X, a boy:', 'I2 F  7.49 yr, SD 0.95', 'C  G  12.02 yr, SD 1.33',
              'P1 E  8.35 yr, SD 1.05', 'Mean = 27.86 / 3 = 9.29 yr', 'SE if independent:',
              '  sqrt(0.95^2+1.33^2+1.05^2)/3', '  = 0.65 yr', 'SE if they move together:',
              '  (0.95+1.33+1.05)/3 = 1.11 yr', 'By hand: 9.29, 0.65 and 1.11 yr.',
              "Computed from the program's tables."], repr(sc4))
check('E self-check: no "UNCONFIRMED", no old Willems example (11.6 yr) anywhere',
      not any('UNCONFIRMED' in t.text or '11.6 yr' in t.text for p in hv.pages for t in p.texts))# ===================================================================================== Part P
print('P. The pool: labels and numbers')
LAMH = (15, 3, 6)      # the worked tooth: RH 15, periodontosis 3, translucency 6 mm (P = 20, T = 40)


def pool_session(entries, sexc=2, ancc=2):
    """entries: ('W', st) / ('L', st) Willems or Liversidge of an odontogram run; ('Lam',) / ('PU',) the
    Lamendin / P-U module on LAMH with that one pooled; ('Joh',) Johanson's worked scores, 2+ teeth; then
    Bayesian, Forest, Done, the report, Exit.  Setup: sexc 1 unknown 2 male 3 female; ancc 1 unknown, 2 white,
    3 black, 4 other."""
    ch, ev, inp = [1, sexc, ancc], [K], []
    sx = {1: 0, 2: 1, 3: 2}[sexc]
    pu = sx in (1, 2) and ancc in (2, 3)
    nlam = 0
    for e in entries:
        if e[0] in ('W', 'L'):
            st = e[1]
            W, pw, w = exp_willems_page(st, sx)
            L, pl, lv = exp_liv_page(st, sx)
            ch.append(2)
            for i, s in enumerate(st, 1):
                if s:
                    ev += [tooth(i), stage(s)]
            ev += [soft(6)] + [K] * (npages(W, pw) + npages(L, pl))
            items = (['W'] if (w['ok'] and not w['ceil']) else []) + (['L'] if lv['k'] else [])
            ch.append(items.index(e[0]) + 1)
        elif e[0] in ('Lam', 'PU'):
            ch.append(4)
            inp.append(list(LAMH))
            ev += [K] + [K] * 2      # the intro; the result: two pages with or without P-U (v3.9, second review)
            ch.append((1 if e[0] == 'PU' else 2) if pu else 1)
            nlam += e[0] == 'Lam'
        elif e[0] == 'Joh':
            ch += [6, 1, 2, 1]
            inp.append([1, 1.5, .5, .5, 0, 2.5])
            ev += [K, K, K]
    ch += [6, 3]
    n = len(entries)
    ev += [K] * (2 if 8 + n + 2 > 12 else 1)
    ev += [soft(2), K, soft(6)] + [K] * (2 if nlam else 1)
    ch.append(7)
    ev.append(K)
    return run(NEW, ch, ev, inp, tag='pool %r' % [e[0] for e in entries])


st_b = [7] * 7
hp = pool_session([('W', st_b), ('L', st_b), ('Lam',)])
post = [l for p in pages_titled(hp, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
check('P the posterior page names "Willems 2001", "Liversidge 2006" and "Lamendin" in its weights',
      any(l.startswith('  Willems 2001: ') for l in post) and any(l.startswith('  Liversidge 2006: ') for l in post)
      and any(l.startswith('  Lamendin: ') for l in post), repr(post))
wv, lvv = willems(st_b, 1), liversidge(st_b, 1)
lamA = 0.18 * 20 + 0.42 * 40 + 25.53
prec = [1 / float(wv['sd']) ** 2, 1 / float(lvv['sec']) ** 2, 1 / 12.5 ** 2]
mu = (float(wv['mean']) * prec[0] + float(lvv['est']) * prec[1] + lamA * prec[2]) / sum(prec)
sd = max(math.sqrt(1 / sum(prec)) * 1.25, min(float(wv['sd']), float(lvv['sec']), 12.5))
check('P the pooled mean and SD use Willems (11.74, 0.9), Liversidge (est, the LARGER SE) and (v3.9) Lamendin '
      '(45.93, 12.5) as stored', matches(post[0], S('Mean:   ', F2(mu), ' yr')) and matches(post[1], S('SD:     ', F2(sd), ' yr')),
      '%r %r %s %s' % (post[0], post[1], mu, sd))
fo = pages_titled(hp, 'FOREST PLOT')[0]
labs = sorted([(t.y, t.text, t.hex, t.width) for t in fo.texts if t.x == 4], key=lambda r: r[0])
check('P the forest plot labels the rows "Willems 2001" (green), "Liversidge 2006" (teal), "Lamendin" (blue)',
      [(r[1], r[2]) for r in labs[:3]] == [('Willems 2001', '#008C3C'), ('Liversidge 2006', '#008080'),
                                           ('Lamendin', '#003CC8')], repr(labs))
check('P the forest label column fits the longest label (15 characters x 6.2 px <= the clip)',
      all(len(r[1]) * 6.2 <= r[3] for r in labs), repr(labs))
check('P the forest plot\'s bars start right of the labels (x >= 4 + clip)',
      min(sh.args[0] for sh in fo.shapes if sh.cmd == 'LINE_P' and sh.args[1] == sh.args[3] and 30 < sh.args[1] < 160)
      >= 4 + labs[0][3], '')
check('P the forest panel without a floor (Willems + Liversidge + Lamendin): "no floor needed" (v3.8a\'s line)',
      any(t.text == 'no floor needed: grey bar = dotted marks or wider' for t in fo.texts),
      repr([t.text for t in fo.texts if t.y >= 184]))
# a floored pool: Johanson's worked scores twice (5.16 and 5.16: x 1.25 / sqrt 2 = 4.56 < 5.16)
hf = pool_session([('Joh',), ('Joh',)])
fof = pages_titled(hf, 'FOREST PLOT')[0]
check('P (v3.9) with the floor applied, the forest panel says why: "the methods share root transparency: no gain" '
      '(v3.8a: "the methods share P and T: no gain allowed")',
      any(t.text == 'the methods share root transparency: no gain' for t in fof.texts) and
      any(t.text == 'inv-var SD x1.25 = 4.56 < best single SD 5.16' for t in fof.texts) and
      'FOREST PLOT  estimate +/- 2 SD' in [t.text for t in fof.texts],
      repr([t.text for t in fof.texts if t.y >= 184]))
# the posterior's floor line (second review): only when the floor was applied does it say so
pf = [l for p in pages_titled(hf, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
pn_ = [l for p in pages_titled(hp, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
check('P the posterior\'s floor line says what happened: floored (Johanson twice: 4.56 < 5.16) "SD raised to best '
      'single SD (floor)"; not floored (Willems + Liversidge + Lamendin) "Floor not needed (SD >= best SD)"; '
      'v3.8a printed "SD floored at best single SE" whatever happened',
      pf[-1] == 'SD raised to best single SD (floor)' and pn_[-1] == 'Floor not needed (SD >= best SD)' and
      not any('best single SE' in l for l in pf + pn_), repr((pf[-2:], pn_[-2:])))
rep_ = [l for p in pages_titled(hp, 'REPORT TEMPLATE') for l in page_lines(p)]
REP0 = ['Teaching & demonstration aid;', 'not for legal use.', None, None, None, 'LIMITATION: probabilistic, not a',
        'chronological determination.', 'SDs are real spread among people.',   # v3.9a
        'Gustafson 1950 excluded: mean error', "14.2 yr, Lamendin's 8.9 (39 people).",
        'Methods are NOT independent; SD is', 'floored, not covariance-corrected.']
LAMLBL = ['Lamendin 1992: mean error 10 yr', '(Table 1); as SD of normal errors', '10' + MLT + 'sqrt(pi/2) = 12.5 yr']
check('P (v3.9) the report template: the fleet\'s disclaimer first ("Teaching & demonstration aid; / not for legal '
      'use."); no Saunders / Cattell citation (second review); (v3.9a) "SDs are real spread among people."; Gustafson\'s 14.2 a mean error, Lamendin\'s '
      '8.9 beside it (39 people); with Lamendin pooled, what its 12.5 is, and the disclaimer again at the end (2 pages)',
      len(pages_titled(hp, 'REPORT TEMPLATE')) == 2 and all(a is None or a == b for a, b in zip(REP0, rep_[:12]))
      and rep_[12:] == LAMLBL + ['Teaching & demonstration aid;', 'not for legal use.'] and
      rep_[4].startswith('P(age >= 18): ') and not any('Saunders' in l or 'Cattell' in l for l in rep_), repr(rep_))
check('P "Stored." MSGBOX after each pool answer', [m.lines[0] for m in hp.msgboxes][:3] ==
      ['Stored. 1 method(s) active.', 'Stored. 2 method(s) active.', 'Stored. 3 method(s) active.'],
      repr([m.lines for m in hp.msgboxes]))
# sex unknown, Willems alone: the mixture's mean and SD go to the pool (v3.9: all seven at G -- the ceiling,
# all at H, is no longer offered)
hp2 = pool_session([('W', [7] * 7)], sexc=1, ancc=1)
post2 = [l for p in pages_titled(hp2, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
wv2 = willems([7] * 7, 0)
check('P one method: the floor line reads "One method: no floor applies"', post2[-1] == 'One method: no floor applies',
      repr(post2[-2:]))
check('P sex unknown: the pool holds the mixture (mean 11.74, SD x 1.25 as the one-method posterior)',
      matches(post2[0], S('Mean:   ', F2(wv2['mean']), ' yr')) and matches(post2[1], S('SD:     ', F2(float(wv2['sd']) * 1.25), ' yr'))
      and post2[8] == '  Willems 2001: 100.0%', repr(post2))
fo2 = pages_titled(hp2, 'FOREST PLOT')[0]
check('P one long label: the column widens to 10 + 6.2 x 12 = 85 px (clip 79)',
      [(t.text, t.width) for t in fo2.texts if t.x == 4 and t.text == 'Willems 2001'] == [('Willems 2001', 79)])
rep2 = [l for p in pages_titled(hp2, 'REPORT TEMPLATE') for l in page_lines(p)]
check('P (v3.9) without Lamendin the report is one page of 12 lines, the disclaimer first',
      len(pages_titled(hp2, 'REPORT TEMPLATE')) == 1 and len(rep2) == 12 and
      rep2[:2] == ['Teaching & demonstration aid;', 'not for legal use.'],
      repr(rep2))
# v3.9: Prince & Ubelaker and Johanson in the pool
hp3 = pool_session([('PU',), ('Joh',)])
post3 = [l for p in pages_titled(hp3, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
puA = 0.15 * 15 + 0.29 * 20 + 0.39 * 40 + 23.17
prec3 = [1 / 9.576177 ** 2, 1 / 5.16 ** 2]
mu3 = (puA * prec3[0] + 45.985 * prec3[1]) / sum(prec3)
sd3 = max(math.sqrt(1 / sum(prec3)) * 1.25, 5.16)
check('P (v3.9) P-U 2002 (46.82, its Table 6 RMSE 9.576177) and Johanson (45.985, 5.16) pooled: mean, SD, the labels',
      matches(post3[0], S('Mean:   ', F2(mu3), ' yr')) and matches(post3[1], S('SD:     ', F2(sd3), ' yr'))
      and any(l.startswith('  P-U 2002: ') for l in post3) and any(l.startswith('  Johanson: ') for l in post3), repr(post3))
fo3 = pages_titled(hp3, 'FOREST PLOT')[0]
labs3 = [(t.text, t.hex) for t in sorted(fo3.texts, key=lambda t: t.y) if t.x == 4 and t.text != 'Pooled']
check('P (v3.9) the forest plot colours "P-U 2002" purple (#6A0DAD) and keeps the 9-character label column',
      labs3 == [('P-U 2002', '#6A0DAD'), ('Johanson', '#FF4500')] and
      all(t.width == 58 for t in fo3.texts if t.x == 4), repr(labs3))
# every place a method label is set or read in code: the pool (lbls) and the forest plot (flb)
code = [strip_comment(l) for l in SRC.split('\n')]
stored = sorted(set(re.findall(r'lbls\s*:=\s*CONCAT\(lbls,\s*\{"([^"]*)"\}\)', ''.join(code))))
tested = sorted(set(re.findall(r'flb\(foI\) == "([^"]*)"', ''.join(code))))
print('   labels stored in the pool: %s; labels the forest plot colours: %s' % (stored, tested))
check('P the pool stores exactly Willems 2001, Liversidge 2006, Lamendin, P-U 2002 (v3.9), Johanson, Bang-Ramm',
      stored == sorted(['Willems 2001', 'Liversidge 2006', 'Lamendin', 'P-U 2002', 'Johanson', 'Bang-Ramm']), repr(stored))
check('P the forest plot colours exactly the same six labels', tested == stored, repr(tested))
# ===================================================================================== Part B
print("B. The verdict band (Roger's D1): cut-points 5% and 95%, printed in the band")


def num(a):
    return int(a) if isinstance(a, float) and a == int(a) else a


def b_call(prog, vp, by):
    h = Harness(prog)
    h.call('fdBand', vp, by)
    if prog in OPENING:
        SCI.extend(h.sci_strings)
    return h


BC = [(0.949, 'uncertain', '94.9'), (0.95, 'probably >= 18', '95.0'), (0.951, 'probably >= 18', '95.1'),
      (0.049, 'probably < 18', '4.9'), (0.05, 'probably < 18', '5.0'), (0.051, 'uncertain', '5.1'),
      (0.94949, 'uncertain', '94.9'), (0.94996, 'probably >= 18', '95.0'), (0.05004, 'probably < 18', '5.0'),
      (0.0505, 'uncertain', '5.1'), (0.5, 'uncertain', '50.0'), (0.83, 'uncertain', '83.0'), (0.58, 'uncertain', '58.0'),
      (0.57, 'uncertain', '57.0'), (0.0, 'probably < 18', '< 0.1'), (1.0, 'probably >= 18', '> 99.9'),
      (0.0004, 'probably < 18', '< 0.1'), (0.9996, 'probably >= 18', '> 99.9'), (0.001, 'probably < 18', '0.1'),
      (0.999, 'probably >= 18', '99.9')]
COLS = {'probably >= 18': (0x008C3C, 0xE8F6EB), 'uncertain': (0xFF4500, 0xFFF0DC), 'probably < 18': (0xFF0000, 0xFFEBEB)}
rows_ = []
for vp, v, pr in BC:
    h = b_call(NEW, vp, 199.0)
    t = sorted(h.texts, key=lambda x: x.y)
    l2 = 'P(age >= 18)' + ((' ' + pr) if pr[0] in '<>' else (' = ' + pr)) + '%  (cut-points 5% and 95%)'
    ok = (len(t) == 2 and t[0].text == v and t[1].text == l2 and (t[0].x, t[0].y, t[0].font) == (10, 200, 2)
          and (t[1].x, t[1].y, t[1].font) == (10, 214, 1) and t[0].color == COLS[v][0] and t[1].color == COLS[v][0]
          and t[0].width == 300 and t[1].width == 300)
    lg = [list(e[1]) for e in h.log if e[0] == 'RECT_P']
    okr = any([num(a) for a in x[1:7]] == [4, 199, 315, 226, COLS[v][0], COLS[v][1]] for x in lg)
    ho_ = b_call(OLD, vp, 201.0)
    old = [x.text for x in ho_.texts][0]
    rows_.append((vp, old, v + ' | ' + l2))
    check('B P = %g: "%s" / "%s", its colours and the band 4,199-315,226 (v3.8a: "%s")' % (vp, v, l2, old),
          ok and okr, repr(([(x.text, x.x, x.y, x.font, x.hex) for x in t], lg)))
print('   the rule implemented: P(age >= 18) as printed (rounded to 0.1 %%): >= 95.0 green "probably >= 18", '
      '<= 5.0 red "probably < 18", otherwise orange "uncertain"; both ends inclusive, so exactly 0.95 is green and '
      'exactly 0.05 red; "< 0.1" counts as 0 and "> 99.9" as 100.')
for vp, old, new in rows_[:6]:
    print('     P = %-6g v3.8a "%s"  ->  v3.9 "%s"' % (vp, old, new))
check('B the cut-points are printed from the routine\'s own two numbers (bdLo := 5; bdHi := 95), the rule is "bdPc >= '
      'bdHi" and "bdPc <= bdLo" on bdPc := ROUND(vp*100, 1); 0.83 and 0.58 appear nowhere in code (About\'s '
      'history line "results kept 0.58/0.83 until v3.9" is text)',
      'bdLo := 5; bdHi := 95;' in SRC and 'bdPc := ROUND(vp*100, 1);' in SRC and 'IF bdPc >= bdHi THEN' in SRC and
      'IF bdPc <= bdLo THEN' in SRC and not any(re.search(r'\b0\.(83|58)\b', re.sub(r'"[^"]*"', '""', strip_comment(l)))
                                        for l in SRC.split('\n')))
# the page geometry: a band page holds 12 lines, the last at row 184; the band at 199-226; the footer at 228;
# a page without a band, and M3's zone band (rows 201-219), keep the footer at 224
hb = Harness(NEW)
hb.press('Enter')
hb.call('fdPageV', 'TEST', ['line %d' % i for i in range(1, 13)], 0.97)
pgt = hb.pages[-1].texts
check('B a band page: 12 lines (the last at row 184), the band lines at 200 and 214, the footer at row 228',
      [t.y for t in pgt if t.x == 6 and t.font == 2 and t.y > 4] == [30 + 14 * i for i in range(12)] and
      [t.y for t in pgt if t.x == 6 and t.font == 1] == [228] and band_ok(hb.pages[-1], 0.97),
      repr([(t.text, t.y) for t in pgt]))
hb = Harness(NEW)
hb.press('Enter')
hb.call('fdPageV', 'TEST', ['line'], -1)
check('B a page without a band: the footer at row 224, as in v3.8a',
      [t.y for t in hb.pages[-1].texts if t.x == 6 and t.font == 1] == [224])
hb = Harness(NEW)
hb.press('Enter')
hb.call('fdPageV', 'TEST', ['line'], -3)
zt = [t for t in hb.pages[-1].texts if t.y == 204]
check('B M3\'s zone band (vp = -3): one line at row 204, its rectangle 201-219, the footer at 224 -- v3.8a\'s, unchanged',
      [t.text for t in zt] == ['about a coin toss (grades E-G)'] and
      [t.y for t in hb.pages[-1].texts if t.x == 6 and t.font == 1] == [224])

# ===================================================================================== Part C
print('C. The Willems ceiling (C-F1, Roger\'s D7) and Liversidge\'s floor (C-F6)')
for sx, nm in ((1, 'boys'), (2, 'girls'), (0, 'sex unknown')):
    h, exp = session([8] * 7, sx, tag='C ceiling ' + nm)
    W, pw, w = exp[0], exp[1], exp[2]
    wp_ = pages_titled(h, WTITLE)
    wl = [l for p in wp_ for l in page_lines(p)]
    check('C all seven at H, %s: the ceiling page (independent text), no 68%% / 95%% lines, no band, footer "next"' % nm,
          pw == -1 and same_rows(wp_, W, -1)[0] and not any(l.startswith(('68%', '95%')) for l in wl) and
          all(band_texts(p) is None for p in wp_) and
          [t.text for p in wp_ for t in p.texts if t.y == 224] == ['any key or tap = next'], repr(wl))
    q = [c for c in h.chooses if c.title in ('Add to Bayesian pool?', 'Nothing to add to the pool')]
    check('C all seven at H, %s: nothing offered to the pool ("Nothing to add to the pool"), nothing stored' % nm,
          len(q) == 1 and q[0].title == 'Nothing to add to the pool' and not any('Stored' in m.lines[0] for m in h.msgboxes))
    fr = pages_titled(h, ODO)[-1]
    l5 = [t.text for t in fr.texts if t.y == 182 and t.x == 8]
    xw = axis_x(w['mean'])
    arrow = [list(x.args)[:5] for x in fr.shapes if x.cmd == 'LINE_P' and list(x.args)[4:5] == [0xC800C8] and x.args[1] == 197]
    check('C all seven at H, %s: the odontogram reads "Willems 2001: at the ceiling, >= ~15.8-16 yr", and its mark at '
          '%.2f points older' % (nm, float(w['mean'])),
          l5 == ['Willems 2001: at the ceiling, >= ~15.8-16 yr'] and [xw + 1, 197, xw + 8, 197, 0xC800C8] in arrow,
          repr((l5, arrow)))


def free_run(prog, chooses, inputs=(), taps=()):
    """a run whose page keys need not be counted (any key = Enter): for showing an older version's screens"""
    h = Harness(prog, strict=False, idle_key=30)
    h.choose(*chooses)
    for e in taps:
        h.tap(e[1], e[2]) if e[0] == 'tap' else h.press('Enter')
    for a in inputs:
        h.answer(a)
    h.result = h.execute('FDAES()')
    return h


PREFIX = '/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/f39/fix2/FDAES_v3.9_before_fix2.txt'
HAVE_PREFIX = os.path.exists(PREFIX)
print('   (the v3.9 draft before the second review: %s)' % (PREFIX if HAVE_PREFIX else 'not found, its rows skipped'))
# v3.9 (second review): NEAR the ceiling -- 33-37 at H, the incisors short of H -- the same: no age, no band, no pool
for st, sx, nm in (([7, 7, 8, 8, 8, 8, 8], 2, 'girls, 31 and 32 at G (the largest girls\' sum, 15.93)'),
                   ([3, 8, 8, 8, 8, 8, 8], 1, 'a boy, 31 at C (15.52)'),
                   ([6, 5, 8, 8, 8, 8, 8], 0, 'sex unknown, 31 F, 32 E')):
    h, exp = session(st, sx, tag='C near ceiling ' + nm)
    W, pw, w = exp[0], exp[1], exp[2]
    wp_ = pages_titled(h, WTITLE)
    wl = [l for p in wp_ for l in page_lines(p)]
    q = [c for c in h.chooses if c.title in ('Add to Bayesian pool?', 'Nothing to add to the pool')]
    fr = pages_titled(h, ODO)[-1]
    l5 = [t.text for t in fr.texts if t.y == 182 and t.x == 8]
    check('C near the ceiling, %s: "= 33-37 at H: the tables\' ceiling", why ("cannot tell 16 from 30"), no ranges, '
          'no band, Willems not offered, the odontogram\'s ceiling line' % nm,
          w['ok'] and w['ceil'] and not w['allh'] and pw == -1 and same_rows(wp_, W, -1)[0] and
          "= 33-37 at H: the tables' ceiling" in wl and '16 from 30' in ' '.join(wl) and
          all(band_texts(p) is None for p in wp_) and q and 'Willems 2001 (sum)' not in q[0].items and
          l5 == ['Willems 2001: at the ceiling, >= ~15.8-16 yr'], repr((wl, q and q[0].items, l5)))
    taps = [K] + [e for i in range(1, 8) for e in (tooth(i), stage(st[i - 1]))] + [soft(6)]
    sexc = {0: 1, 1: 2, 2: 3}[sx]
    ho = free_run(OLD, [1, sexc, 1, 2, 'No', 6], taps=taps)
    oq = [c.items for c in ho.chooses if c.title == 'Add to Bayesian pool?']
    owl = [l for p in pages_titled(ho, WTITLE) for l in page_lines(p)]
    check('C near the ceiling, %s: v3.8a printed a dental age and offered it to the pool: %r' %
          (nm, [l for l in owl if 'Dental age' in l]), any('Dental age' in l for l in owl) and oq and
          'Willems 2001 (sum)' in oq[0])
    if HAVE_PREFIX:
        hp_ = free_run(PREFIX, [1, sexc, 1, 2, 'No', 7], taps=[K] + taps)
        pq = [c.items for c in hp_.chooses if c.title == 'Add to Bayesian pool?']
        pwl = [l for p in pages_titled(hp_, WTITLE) for l in page_lines(p)]
        check('C near the ceiling, %s: the v3.9 draft before the second review printed a dental age and offered it: %r'
              % (nm, [l for l in pwl if 'Dental age' in l]), any('Dental age' in l for l in pwl) and pq and
              'Willems 2001 (sum)' in pq[0])
h, exp = session([8, 8, 7, 8, 8, 8, 8], 1, tag='C 33 at G')
check('C 33 at G, the rest at H (a boy): below the rule, so an age, a band and the Willems pool offer',
      exp[1] >= 0 and not exp[2]['ceil'] and all(band_ok(p, exp[1]) for p in pages_titled(h, WTITLE)) and
      [c for c in h.chooses if c.title == 'Add to Bayesian pool?'][0].items[0] == 'Willems 2001 (sum)')
# v3.8a, the same dentition: the bug the review found
ho = run(OLD, [1, 2, 1, 2, 1, 6], [K] + [e for i in range(1, 8) for e in (tooth(i), stage(8))] + [soft(6), K, K, K],
         tag='C old ceiling')
ob = [x.text for p in pages_titled(ho, WTITLE) for x in p.texts if x.y == 204]
oq = [c.items for c in ho.chooses if c.title == 'Add to Bayesian pool?']
check('C v3.8a, the same boy: "= Dental age 16.03 yr", the red band "likely < 18  P(age >= 18) = 1.3%%" and the pool '
      'offering it (the review\'s C-F1): %r %r' % (ob, oq), ob and ob[0].startswith('likely < 18') and oq and
      'Willems 2001 (sum)' in oq[0])
# one stage short of the ceiling: an age, a band and the pool offer, as before
h, exp = session([8, 8, 8, 8, 8, 8, 7], 1, tag='C one tooth at G')
q = [c for c in h.chooses if c.title == 'Add to Bayesian pool?']
check('C 37 at G, the rest at H (a boy): an age, a band, and the pool offers Willems (not the ceiling)',
      exp[1] >= 0 and all(band_ok(p, exp[1]) for p in pages_titled(h, WTITLE)) and q and q[0].items[0] == 'Willems 2001 (sum)')
# Liversidge: the H floor above the estimate -> no band; below it -> the band
h, exp = session([5, 0, 0, 0, 0, 0, 8], 1, tag='C floor above')
lp_ = pages_titled(h, LTITLE)
ll = [l for p in lp_ for l in page_lines(p)]
check('C Liversidge, 31 at E and 37 at H (a boy): the floor 15.25 is above the estimate 5.38: the page says so, '
      '"so no P(age >= 18) band is drawn.", and draws none (v3.8a drew "likely < 18")',
      'That floor is above the estimate,' in ll and 'so no P(age >= 18) band is drawn.' in ll and
      all(band_texts(p) is None for p in lp_), repr(ll))
h, exp = session([0, 0, 0, 0, 0, 8, 7], 1, tag='C floor below')
lp_ = pages_titled(h, LTITLE)
check('C Liversidge, 36 at H (floor 9.97) and 37 at G (13.42): the floor is below the estimate: the band is drawn',
      exp[4] >= 0 and all(band_ok(p, exp[4]) for p in lp_))

# ===================================================================================== Part F
print('F. The typed posterior threshold (C-F8, C-F9)')
FT = []
for typed, thr, shown in ((1000000, 110.0, '110.0'), (1E9, 110.0, '110.0'), (-5, 0.0, '0.0'), (0.05, 0.1, '0.1'),
                          (0.04, 0.0, '0.0'), (17.96, 18.0, '18.0'), (17.94, 17.9, '17.9'), (110.04, 110.0, '110.0'),
                          (21, 21.0, '21.0')):
    for prog in (NEW, OLD):
        if prog == OLD and typed == 1E9:
            continue                            # v3.8a never returns from 1E9 (the review's J1)
        h = Harness(prog, strict=False)
        h.press('Enter'); h.choose('Type a threshold age'); h.answer({'poIn': float(typed)}); h.press('Esc')
        r = h.execute('fdPost(47, 5.16, 18)')
        nl = sum(1 for e in h.log if e[0] == 'LINE_P')
        pan = [t.text for t in h.texts if t.text.startswith('P(age >= ')][-1:]
        if prog == NEW:
            SCI.extend(h.sci_strings)
            check('F typed %r: the threshold %s, the panel "P(age >= %s) ...", %d lines drawn (under 2000), no '
                  'scientific display' % (typed, thr, shown, nl),
                  r == [0.0, thr] and pan and pan[0].startswith('P(age >= %s)' % shown) and nl < 2000 and not h.sci_strings,
                  repr((r, pan, nl, h.sci_strings)))
        FT.append((prog == NEW, typed, r, nl, pan, len(h.sci_strings)))
print('   v3.8a for the record:')
for isnew, typed, r, nl, pan, ns in FT:
    if not isnew:
        print('     typed %r: returned %r, %d LINE_P, panel %r, %d scientific displays' % (typed, r, nl, pan, ns))
old1e6 = [x for x in FT if not x[0] and x[1] == 1000000][0]
check('F v3.8a, typed 1000000: about 100,000 lines (the review\'s hang, C-F8); typed 0.05: scientific (C-F9)',
      old1e6[3] > 90000 and [x for x in FT if not x[0] and x[1] == 0.05][0][5] > 0, repr(old1e6[:4]))
check('F the code: poThr := ROUND(MAX(0, MIN(110, poIn)), 1); the panel prints fdF1(poThr) twice',
      'poThr := ROUND(MAX(0, MIN(110, poIn)), 1);' in SRC and SRC.count('fdF1(poThr)') == 2 and 'STRING(poThr,2,1)' not in SRC)
# ===================================================================================== Part L
print('L. Lamendin 1992 / Prince-Ubelaker 2002 (D2, D4; C-F2, C-F3)')
PU = list(csv.DictReader(open(PUCSV)))
check('L PU_tables_v1.csv has the four groups in the order of Tables 3-6',
      [(r['ancestry'], r['sex'], r['table']) for r in PU] ==
      [('black', 'male', 'Table 3'), ('white', 'female', 'Table 4'), ('black', 'female', 'Table 5'), ('white', 'male', 'Table 6')])
PUC = {g: [D(PU[g - 1][k]) for k in ('text_RH', 'text_P', 'text_T', 'text_intercept')] for g in (1, 2, 3, 4)}
PUT = {g: [D(PU[g - 1][k]) for k in ('table_RH', 'table_P', 'table_T', 'table_intercept')] for g in (1, 2, 3, 4)}
PURM = {g: D(PU[g - 1]['RMSE']) for g in (1, 2, 3, 4)}
PUNM = {1: 'black males', 2: 'white females', 3: 'black females', 4: 'white males'}
HL = Harness(NEW, strict=True)
HL.execute('fdPUTab()')
pc = HL.execute('fdPUc'); pr_ = HL.execute('fdPUr'); pn_ = HL.execute('fdPUn')
check('L the program\'s fdPUc = the CSV\'s text equations (16 numbers), fdPUr = its RMSEs, fdPUn = its n',
      pc == [float(v) for g in (1, 2, 3, 4) for v in PUC[g]] and pr_ == [float(PURM[g]) for g in (1, 2, 3, 4)]
      and pn_ == [float(PU[g - 1]['n']) for g in (1, 2, 3, 4)], repr((pc, pr_, pn_)))
check('L the text equations as the brief quotes them: black males 1.04 RH + 0.31 P + 0.47 T + 1.70; white females 1.10, '
      '0.31, 0.39, 11.82; black females 1.63, 0.48, 0.48, -8.41; white males 0.15, 0.29, 0.39, 23.17',
      PUC == {1: [D('1.04'), D('0.31'), D('0.47'), D('1.7')], 2: [D('1.1'), D('0.31'), D('0.39'), D('11.82')],
              3: [D('1.63'), D('0.48'), D('0.48'), D('-8.41')], 4: [D('0.15'), D('0.29'), D('0.39'), D('23.17')]})
print('   each Table\'s Prediction Profile: the Table\'s estimates, the printed equation, and Lamendin, at the same inputs')
for g in (1, 2, 3, 4):
    r = PU[g - 1]
    rh, p_, t_ = D(r['profile_RH_mean']), D(r['profile_P_mean']), D(r['profile_T_mean'])
    tab = PUT[g][0] * rh + PUT[g][1] * p_ + PUT[g][2] * t_ + PUT[g][3]
    txt = PUC[g][0] * rh + PUC[g][1] * p_ + PUC[g][2] * t_ + PUC[g][3]
    prog_ = HL.execute('fdPUAge(%d, %s, %s, %s)' % (g, rh, p_, t_))
    lam = D('0.18') * p_ + D('0.42') * t_ + D('25.53')
    print('     %s (%s, n = %s): RH %s P %s T %s -> Table %.4f (Mean of Response %s), printed equation %.4f (%+.2f), '
          'Lamendin %.2f' % (PUNM[g], r['table'], r['n'], rh, p_, t_, tab, r['mean_of_response'], txt, txt - tab, lam))
    check('L %s: the Table\'s estimates at its profile means give its Mean of Response (%s), to 0.0005' % (PUNM[g], r['mean_of_response']),
          abs(tab - D(r['mean_of_response'])) < D('0.0005'), str(tab))
    check('L %s: the program (fdPUAge) = the printed equation at the profile means (%.4f)' % (PUNM[g], txt),
          abs(prog_ - float(txt)) < 1e-9, repr(prog_))
    check('L %s: the printed equation is within 0.2 yr of the Table\'s fit there (%+.3f)' % (PUNM[g], txt - tab),
          abs(txt - tab) < D('0.2'))
# fdPUg: every sex x ancestry
gm = {(sx, an): HL.execute('fdPUg(%d, %d)' % (sx, an)) for sx in (0, 1, 2) for an in (0, 1, 2, 3)}
want = {(sx, an): {(1, 1): 4, (2, 1): 2, (1, 2): 1, (2, 2): 3}.get((sx, an), 0) for sx in (0, 1, 2) for an in (0, 1, 2, 3)}
check('L fdPUg: white male -> 4 (Table 6), white female -> 2 (Table 4), black male -> 1 (Table 3), black female -> 3 '
      '(Table 5); the sex unknown or ancestry Unknown / Other -> 0 (12 cases)', gm == want, repr(gm))
check('L (D4) fdLamSD() = 12.5, Lamendin\'s mean error 10 x sqrt(pi/2) = %.4f, used as 12.5' % (10 * math.sqrt(math.pi / 2)),
      HL.execute('fdLamSD()') == 12.5)
check('L (D4) fdLamLbl(12.5) says what 12.5 is; any other value (e.g. 10) says it is FDAES\'s choice',
      HL.call('fdLamLbl', 12.5) == LAMLBL and HL.call('fdLamLbl', 10.0) ==
      ["SD 10.00 yr: FDAES's choice;", "Lamendin's mean error is 10 yr", '(Table 1, 306 teeth).'])
check('L P-U\'s own groups bear out ME x sqrt(pi/2): RMSE / mean absolute difference = %s (normal: %.4f)'
      % (', '.join('%.2f' % (float(PURM[g]) / float(PU[g - 1]['table7_new_mean_abs_diff'])) for g in (1, 2, 3, 4)),
         math.sqrt(math.pi / 2)),
      all(1.25 < float(PURM[g]) / float(PU[g - 1]['table7_new_mean_abs_diff']) < 1.33 for g in (1, 2, 3, 4)))


def UP(x):
    """fdUpEnd: an interval's upper end; above 110 it prints "> 110" (v3.9, second review)"""
    return ['> 110'] if x > 110 else F1(x)


LAMFLOOR = float(norm.cdf((25.53 - 18) / 12.5))          # Lamendin's smallest P(age >= 18): 0.7266


def exp_lam(rh, per, tr, sx, an):
    """the result page's lines (segments), P for the band, P-U usable, and the two ages -- independently.
    v3.9 (second review): P-U's estimate always shown, USED only inside its sample (25 to 99, p 108); RH with two
    decimals; the band's source on line 2; upper ends above 110 as "> 110"; Lamendin's floor when he gives the band"""
    rh, per, tr = D(str(rh)), D(str(per)), D(str(tr))
    P, T = per * 100 / rh, tr * 100 / rh
    g = {(1, 1): 4, (2, 1): 2, (1, 2): 1, (2, 2): 3}.get((sx, an), 0)
    lam, sl = D('0.18') * P + D('0.42') * T + D('25.53'), D('12.5')
    L = [S('RH = ', F2(rh), ' mm, P = ', F2(P), ', T = ', F2(T))]
    ok, a, s_ = False, None, None
    if g:
        c = PUC[g]
        a, s_ = c[0] * rh + c[1] * P + c[2] * T + c[3], PURM[g]
        ok = D(25) <= a <= D(99)
    L.append(S("Band: from P-U 2002's estimate." if ok else "Band: from Lamendin 1992's estimate."))
    if g:
        L += [S('P-U 2002, %s (Table %d):' % (PUNM[g], g + 2)),
              S('%.2f' % c[0] + MLT, F2(rh), ' + %.2f' % c[1] + MLT, F2(P)),
              S('  + %.2f' % c[2] + MLT, F2(T), (' - %.2f' % -c[3]) if c[3] < 0 else (' + %.2f' % c[3]))]
        L.append(S('= ', ['< 0'] if a < 0 else F2(a), ' yr (P-U 2002)'))
        if ok:
            L += [S('SEE ', F2(s_), ' (root mean square'),
                  S('  error, P-U Table %d)' % (g + 2)),
                  S('68%: [', F1(max(D(0), a - s_)), ', ', UP(a + s_), ']'),
                  S('95%: [', F1(max(D(0), a - 2 * s_)), ', ', UP(a + 2 * s_), ']')]
        else:
            L += [S("Outside P-U's sample (25-99, p 108):"), S('  extrapolation; no band, not pooled.')]
    else:
        L += [S('P-U 2002: needs sex and white or'), S('  black ancestry (Setup).')]
    L += [S('LAMENDIN 1992:'), S('0.18' + MLT, F2(P), ' + 0.42' + MLT, F2(T), ' + 25.53'),
          S('= ', F2(lam), ' yr (Lamendin 1992)')] + [S(x) for x in LAMLBL] + \
         [S('68%: [', F1(max(D(0), lam - sl)), ', ', UP(lam + sl), ']'),
          S('95%: [', F1(max(D(0), lam - 2 * sl)), ', ', UP(lam + 2 * sl), ']')]
    if lam < 40:
        L.append(S('==> Lamendin under 40: unreliable.'))
    if not ok:
        L += [S('Lamendin cannot give below 25.5 yr:'), S('P(age >= 18) never below ', PCTN(LAMFLOOR * 100), '%.')]
    if g:
        L += [S('(P-U as printed in the text: its'), S("Table's estimates, rounded.)")]
    p = float(norm.sf(18, float(a), float(s_))) if ok else float(norm.sf(18, float(lam), float(sl)))
    return L, p, ok, a, lam, g


def lam_session(sexc, ancc, hts, pool=None, tag=''):
    """Setup, then the module on heights hts; the pool answered 'Neither' unless told; Exit"""
    sx, an = {1: 0, 2: 1, 3: 2}[sexc], ancc - 1
    L, p, ok, a, lam, g = exp_lam(hts[0], hts[1], hts[2], sx, an)
    ch = [1, sexc, ancc, 4]
    ev = [K, K] + [K] * npages(L, p)
    items = (['Prince-Ubelaker 2002', 'Lamendin 1992', 'Neither'] if ok else ['Lamendin 1992', 'Neither'])
    ch.append(items.index(pool or 'Neither') + 1)
    ch.append(7)
    ev.append(K)
    h = run(NEW, ch, ev, [list(hts)], tag='L %s' % tag)
    return h, (L, p, ok, a, lam, g, items)


LTIT = 'LAMENDIN 1992 / P-U 2002'
HTS = [(15, 3, 6), (12, 0, 0), (20, 10, 20), (5, 0, 0), (35, 35, 35), (14.2, 2.7, 6.9), (8, 1.5, 7.9)]
nl_ = 0
for sexc in (1, 2, 3):
    for ancc in (1, 2, 3, 4):
        for hts in HTS:
            tag = 'sex %d anc %d heights %r' % (sexc, ancc, hts)
            h, e = lam_session(sexc, ancc, hts, tag=tag)
            L, p, ok, a, lam, g, items = e
            pg = pages_titled(h, LTIT)
            okr, dr = same_rows(pg, L, p)
            check('L result page = independent (%s)' % tag, okr and len(pg) == npages(L, p), repr(dr[:3]))
            check('L the band from %s (%s)' % ('P-U' if ok else 'Lamendin', tag), all(band_ok(x, p) for x in pg),
                  repr([band_line(x) for x in pg]))
            q = [c for c in h.chooses if c.title == 'Add to Bayesian pool?']
            check('L the pool offers %s (%s)' % (items, tag), len(q) == 1 and q[0].items == items, repr(q))
            nl_ += 1
print('   %d result pages (12 Setups x %d tooth measurements)' % (nl_, len(HTS)))
# the intro page
h, e = lam_session(2, 2, (15, 3, 6), tag='intro, white male')
ip = page_lines(pages_titled(h, 'LAMENDIN 1992 / PRINCE-UBELAKER 2002')[0])
check('L the intro page: the labial surface, the three heights, P and T, Lamendin always, P-U\'s group, the help pointer',
      ip == ['Measure on the LABIAL surface of an', 'extracted single-rooted tooth, mm:', '  RH   root height, CEJ to apex',
             '  per  periodontosis, CEJ to the', '       soft-tissue line', '  tr   translucency, from the apex',
             'P = per' + MLT + '100 / RH, T = tr' + MLT + '100 / RH', 'Lamendin 1992: always (poor under',
             '  40: his Table 1).', 'P-U 2002: white males (Table 6),', "  from Setup's sex and ancestry.",
             'Help: main menu > How to use.', 'Next: the three heights, in mm.'], repr(ip))
inp_ = [i for i in h.inputs if i.title == 'Lamendin / Prince-Ubelaker'][0]
check('L one INPUT form, three heights in mm, RH starting at 0 (refused unless measured)',
      list(inp_.labels) == ['RH mm:', 'Perio mm:', 'Transl mm:'] and
      [inp_.before[n] for n in inp_.names] == [0.0, 0.0, 0.0], repr((inp_.labels, inp_.before)))
h, e = lam_session(1, 2, (15, 3, 6), tag='intro, sex unknown')
ip = page_lines(pages_titled(h, 'LAMENDIN 1992 / PRINCE-UBELAKER 2002')[0])
check('L the intro page with no P-U equation: "P-U 2002: needs sex and white or / black ancestry (Setup)."',
      ip[9:11] == ['P-U 2002: needs sex and white or', '  black ancestry (Setup).'], repr(ip))
# the refusals: a MSGBOX that teaches, no result page, no pool question, nothing stored
REF = [((0, 0, 0), ['Root height RH must be above 0:', 'P and T are heights x 100 / RH.', 'Nothing stored.']),
       ((4, 0, 0), ['RH = 4.00 mm is not a root height:', 'roots run about 10 to 20 mm;', 'FDAES takes 5 to 35 mm.',
                    'Nothing stored.']),
       ((36, 0, 0), ['RH = 36.00 mm is not a root height:', 'roots run about 10 to 20 mm;', 'FDAES takes 5 to 35 mm.',
                     'Nothing stored.']),
       ((4.96, 0, 0), ['RH = 4.96 mm is not a root height:', 'roots run about 10 to 20 mm;',
                       'FDAES takes 5 to 35 mm.', 'Nothing stored.']),
       ((35.04, 0, 0), ['RH = 35.04 mm is not a root height:', 'roots run about 10 to 20 mm;',
                        'FDAES takes 5 to 35 mm.', 'Nothing stored.']),
       ((15, -1, 0), ['A height cannot be negative.', 'Nothing stored.']),
       ((15, 0, -0.5), ['A height cannot be negative.', 'Nothing stored.']),
       ((15, 16, 0), ['Periodontosis (16.00 mm) cannot', 'exceed the root height (15.00 mm):',
                      'it is measured on the root.', 'Nothing stored.']),
       ((15, 0, 15.5), ['Translucency (15.50 mm) cannot', 'exceed the root height (15.00 mm):',
                        'it is measured on the root.', 'Nothing stored.']),
       ((15, 15.04, 0), ['Periodontosis (15.04 mm) cannot', 'exceed the root height (15.00 mm):',
                         'it is measured on the root.', 'Nothing stored.']),
       (CANCEL, ['Cancelled. Nothing stored.'])]
for hts, msg in REF:
    h = run(NEW, [1, 2, 2, 4, 7], [K, K, K], [hts if hts is CANCEL else list(hts)], tag='L refusal %r' % (hts,))
    check('L refused %r: %r; no page, no pool question' % (hts, msg[0]),
          [m.lines for m in h.msgboxes] == [msg] and not pages_titled(h, LTIT) and
          not [c for c in h.chooses if c.title == 'Add to Bayesian pool?'], repr([m.lines for m in h.msgboxes]))
for hts in ((5, 0, 0), (35, 35, 35), (15, 15, 15), (15, 0, 0)):
    h, e = lam_session(2, 3, hts, tag='edges accepted %r' % (hts,))
    check('L accepted at the edges %r (RH 5 and 35; heights 0 and = RH)' % (hts,), len(pages_titled(h, LTIT)) >= 1
          and not h.msgboxes)
# v3.9 (second review): P-U outside its sample's ages (25-99, p 108) is shown, labelled an extrapolation, not used
h, e = lam_session(3, 3, (5, 0, 0), tag='P-U below 0')
lp = [l for p in pages_titled(h, LTIT) for l in page_lines(p)]
check('L P-U far outside its sample (black female, RH 5: 1.63 x 5 - 8.41 = -0.26 yr): "= < 0 yr (P-U 2002)", '
      '"Outside P-U\'s sample (25-99, p 108): extrapolation; no band, not pooled."; the band and the pool from Lamendin',
      e[2] is False and e[3] < 0 and e[6] == ['Lamendin 1992', 'Neither'] and '= < 0 yr (P-U 2002)' in lp and
      "Outside P-U's sample (25-99, p 108):" in lp and "Band: from Lamendin 1992's estimate." in lp and
      not any('-0.26' in l for l in lp), repr(lp))
h, e = lam_session(2, 2, (12, 0, 0), tag='P-U 24.97')
lp = [l for p in pages_titled(h, LTIT) for l in page_lines(p)]
check('L P-U just below its sample (white male, RH 12: 0.15 x 12 + 23.17 = 24.97 yr): shown, labelled an '
      'extrapolation, the band from Lamendin (with his floor), Lamendin alone offered',
      e[2] is False and abs(e[3] - D('24.97')) < D('1e-9') and '= 24.97 yr (P-U 2002)' in lp and
      "  extrapolation; no band, not pooled." in lp and 'Lamendin cannot give below 25.5 yr:' in lp and
      e[6] == ['Lamendin 1992', 'Neither'], repr(lp))
h, e = lam_session(1, 1, (15, 3, 6), tag='Lamendin floor')
lp = [l for p in pages_titled(h, LTIT) for l in page_lines(p)]
check('L Lamendin supplying the band (sex unknown): "Lamendin cannot give below 25.5 yr: P(age >= 18) never below '
      '72.7%%." (Phi((25.53 - 18)/12.5) = %.4f, from fdLamSD) on the page; the band\'s source on line 2 (page 1)'
      % LAMFLOOR, 'P(age >= 18) never below 72.7%.' in lp and lp[1] == "Band: from Lamendin 1992's estimate." and
      abs(LAMFLOOR - 0.7266) < 1e-4, repr(lp))
h, e = lam_session(2, 2, (15, 3, 6), tag='band source P-U')
pg1 = page_lines(pages_titled(h, LTIT)[0])
check('L the band\'s source is on page 1, under which the band is drawn ("Band: from P-U 2002\'s estimate."), and RH '
      'prints with two decimals so the equation line reproduces the age: "0.15 x 15.00 + 0.29 x 20.00"',
      pg1[1] == "Band: from P-U 2002's estimate." and pg1[0] == 'RH = 15.00 mm, P = 20.00, T = 40.00' and
      pg1[3] == '0.15' + MLT + '15.00 + 0.29' + MLT + '20.00', repr(pg1))
h, e = lam_session(1, 1, (35, 35, 35), tag='Lamendin > 110')
lp = [l for p in pages_titled(h, LTIT) for l in page_lines(p)]
check('L an interval end above 110 prints "> 110", never a clamped "110.0" (Lamendin 85.53 + 2 x 12.5 = 110.53: '
      '"95%: [60.5, > 110]")', '95%: [60.5, > 110]' in lp and not any('110.0' in l for l in lp), repr(lp))
if HAVE_PREFIX:
    hp_ = free_run(PREFIX, [1, 3, 3, 4, 2, 7], inputs=[[5, 0, 0]])
    plp = [l for p in pages_titled(hp_, LTIT) for l in page_lines(p)]
    hq_ = free_run(PREFIX, [1, 1, 1, 4, 2, 7], inputs=[[35, 35, 35]])
    qlp = [l for p in pages_titled(hq_, LTIT) for l in page_lines(p)]
    check('L the v3.9 draft before the second review printed "-0.26" and clamped "110.0": %r %r' %
          ([l for l in plp if '-0.26' in l], [l for l in qlp if '110.0' in l]),
          any('-0.26' in l for l in plp) and any('110.0' in l for l in qlp))
# the pool: P-U, Lamendin, Neither
for pick, lab, val, sd_ in (('Prince-Ubelaker 2002', 'P-U 2002', 46.82, 9.576177), ('Lamendin 1992', 'Lamendin', 45.93, 12.5)):
    sx_, an_ = 1, 1
    L, p, ok, a, lam, g = exp_lam(15, 3, 6, sx_, an_)
    ch = [1, 2, 2, 4, (1 if pick.startswith('Prince') else 2), 6, 3, 7]
    # Setup, the intro, the result page(s); the posterior page, Done on the curve, the report (two pages
    # with Lamendin pooled: it then says what 12.5 is), the exit page
    ev = [K, K] + [K] * npages(L, p) + [K, soft(6)] + [K] * (2 if lab == 'Lamendin' else 1) + [K]
    h = run(NEW, ch, ev, [[15, 3, 6]], tag='L pool %s' % lab)
    post_ = [l for pp in pages_titled(h, 'BAYESIAN POSTERIOR') for l in page_lines(pp)]
    check('L pool "%s": stored as "%s", mean %.2f, SD %s x 1.25 (one method)' % (pick, lab, val, sd_),
          matches(post_[0], S('Mean:   ', F2(val), ' yr')) and matches(post_[1], S('SD:     ', F2(sd_ * 1.25), ' yr'))
          and post_[8] == '  %s: 100.0%%' % lab and [m.lines[0] for m in h.msgboxes] == ['Stored. 1 method(s) active.'],
          repr(post_))
L_, p_, ok_, a_, lam_, g_ = exp_lam(15, 3, 6, 1, 1)
h = run(NEW, [1, 2, 2, 4, 3, 6, 3, 7], [K, K] + [K] * npages(L_, p_) + [K], [[15, 3, 6]], tag='L pool neither')
check('L pool "Neither": nothing stored ("No estimates stored yet.")',
      [m.lines[0] for m in h.msgboxes] == ['No estimates stored yet.'])
# D4 as a one-line change: the same file with fdLamSD's RETURN 12.5 made 10.0
tmpd = tempfile.mkdtemp()
alt = os.path.join(tmpd, 'FDAES_v3.9_D4alt.txt')
open(alt, 'w', encoding='utf-8').write(SRC.replace('  RETURN 12.5;\n', '  RETURN 10.0;\n', 1))
dl = [l for l in difflib.unified_diff(SRC.split('\n'), open(alt).read().split('\n'), lineterm='', n=0)
      if l[:1] in '+-' and not l.startswith(('+++', '---'))]
check('L D4 is a one-line change: the file with fdLamSD returning 10.0 differs in exactly one line', dl == ['-  RETURN 12.5;',
      '+  RETURN 10.0;'], repr(dl))
L_, p_, ok_, a_, lam_, g_ = exp_lam(15, 3, 6, 0, 0)
ha = run(alt, [1, 1, 1, 4, 2, 7], [K, K] + [K] * npages(L_, p_) + [K], [[15, 3, 6]], tag='L D4 alt', opening=True)
al = [l for pp in pages_titled(ha, LTIT) for l in page_lines(pp)]
check('L with 10.0 the page says "SD 10.00 yr: FDAES\'s choice; Lamendin\'s mean error is 10 yr (Table 1, 306 teeth)." '
      'and its lines use 10 (68%%: [35.9, 55.9]); the floor follows: "never below 77.4%%"; the band P from N(45.93, 10)',
      "SD 10.00 yr: FDAES's choice;" in al and '68%: [35.9, 55.9]' in al and 'P(age >= 18) never below 77.4%.' in al and
      band_ok(pages_titled(ha, LTIT)[0], float(norm.sf(18, 45.93, 10))), repr(al))
hb_ = run(alt, [5, 5, 0, 7], [K] * 3 + [K], tag='L D4 alt help', opening=True)
hl_ = ' '.join(l for p in hb_.pages for l in page_lines(p))
check('L with 10.0 the Lamendin help topic follows too ("SD 10.00 yr: FDAES\'s choice", "SD 10.0 P(age >= 18) is never '
      'below 77.4%%"): every shown 12.5 derives from fdLamSD', "SD 10.00 yr: FDAES's choice;" in hl_ and
      'SD 10.0 P(age >= 18) is never below 77.4%.' in hl_ and '12.5' not in hl_, repr(hl_[-400:]))
check('L v3.8a\'s unsourced ancestry rows are gone: no "29.69", "27.21", "26.50", "Afr.Amer.", "Hispanic", "European" '
      'in code (v3.9a: Cattell\'s "North European" children on the history page apart)',
      not any(x in ''.join(strip_comment(l) for l in SRC.split('\n')).replace('North European', 'North-Eu') for x in
              ('29.69', '27.21', '26.50', 'Afr.Amer.', 'Hispanic', 'European')))
# ===================================================================================== Part R
print('R. Bang & Ramm 1970, their own method (D3; C-F4)')
BR = list(csv.DictReader(open(BRCSV)))
BRT = {t: [r for r in BR if r['table'] == t] for t in ('VIII', 'IX', 'X', 'XI')}
check('R BR_tables_v1.csv: four tables of 24 rows, VIII / IX 2nd degree (p 21 / 22), X / XI 1st degree (p 23 / 24)',
      all(len(BRT[t]) == 24 for t in BRT) and
      {(r['table'], r['printed_page'], r['root'], r['degree']) for r in BR} ==
      {('VIII', '21', 'intact', '2'), ('IX', '22', 'section', '2'), ('X', '23', 'intact', '1'), ('XI', '24', 'section', '1')})
check('R the CSV gives each row the same tooth, side and n in all four tables',
      all(len({(BRT[t][i]['type_of_tooth_as_printed'], BRT[t][i]['n_teeth']) for t in BRT}) == 1 for i in range(24)))
HB = Harness(NEW, strict=True)
HB.execute('fdBRTab()')
fl = lambda rows, ks: [float(r[k]) for r in rows for k in ks]
check('R the program\'s fdBR8 / fdBR9 = Tables VIII / IX (B0, B1, B2, SA; 96 numbers each), fdBR10 / fdBR11 = Tables '
      'X / XI (B0, B1, SA; 72 each), fdBRn = n (24)',
      HB.execute('fdBR8') == fl(BRT['VIII'], ('B0', 'B1', 'B2', 'SA')) and
      HB.execute('fdBR9') == fl(BRT['IX'], ('B0', 'B1', 'B2', 'SA')) and
      HB.execute('fdBR10') == fl(BRT['X'], ('B0', 'B1', 'SA')) and
      HB.execute('fdBR11') == fl(BRT['XI'], ('B0', 'B1', 'SA')) and
      HB.execute('fdBRn') == [float(r['n_teeth']) for r in BRT['VIII']])
ROM = {8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI'}


def br_age(c, r, x):
    """independent: (A, SA, B0, B1, B2, table) for condition c (1 intact, 2 section), row r, X (Decimal)"""
    t = (8 if c == 1 else 9) if x <= 9 else (10 if c == 1 else 11)
    row = BRT[ROM[t]][r - 1]
    b0, b1, sa = D(row['B0']), D(row['B1']), D(row['SA'])
    b2 = D(row['B2']) if t <= 9 else D(0)
    return b0 + b1 * x + b2 * x * x, sa, b0, b1, b2, t


XS = ['0', '5', '9.0', '9.01', '12']
nbad = 0
for c in (1, 2):
    for r in range(1, 25):
        got = [HB.call('fdBRAge', c, r, float(x)) for x in XS]
        want = [br_age(c, r, D(x)) for x in XS]
        ok = all(len(g) == 6 and abs(g[0] - float(w[0])) < 1e-9 and [g[1], g[2], g[3], g[4], g[5]] ==
                 [float(w[1]), float(w[2]), float(w[3]), float(w[4]), float(w[5])] for g, w in zip(got, want))
        nbad += not ok
        check('R fdBRAge %s row %d (%s) at X = %s: the age, SA, coefficients and table = CSV' %
              ('intact' if c == 1 else 'section', r, BRT['VIII'][r - 1]['type_of_tooth_as_printed'], ', '.join(XS)),
              ok, repr((got, want)))
print('   48 rows x 5 lengths: %d differ.  Examples: Table VIII row 1 at X = 6: %.2f yr (header: 54.74); '
      'Table X row 13 at X = 11: %.2f yr (header: 72.48)' %
      (nbad, HB.call('fdBRAge', 1, 1, 6.0)[0], HB.call('fdBRAge', 1, 13, 11.0)[0]))
check('R the header\'s worked rows: Table VIII row 1 at X = 6 is 54.74 yr, SA 10.42; Table X row 13 at X = 11 is '
      '72.48 yr, SA 11.12', abs(HB.call('fdBRAge', 1, 1, 6.0)[0] - 54.74) < 1e-9 and
      HB.call('fdBRAge', 1, 1, 6.0)[1] == 10.42 and abs(HB.call('fdBRAge', 1, 13, 11.0)[0] - 72.48) < 1e-9 and
      HB.call('fdBRAge', 1, 13, 11.0)[1] == 11.12 and '20.3 + 5.74 x 6' in SRC and '33.65 + 3.53 x 11' in SRC)
check('R exactly 9.0 mm takes Equation 1 (Table VIII / IX: "less than or equal to 9.0 mm"), 9.01 Equation 2',
      HB.call('fdBRAge', 1, 5, 9.0)[5] == 8 and HB.call('fdBRAge', 2, 5, 9.0)[5] == 9 and
      HB.call('fdBRAge', 1, 5, 9.01)[5] == 10 and HB.call('fdBRAge', 2, 5, 9.01)[5] == 11)
# the combination (p 21)
for ags, sas in (([40.0, 50.0], [10.0, 10.0]), ([33.1, 47.2, 51.9], [10.42, 12.84, 9.53]), ([60.0], [11.0])):
    n = len(ags)
    m = sum(ags) / n
    s = math.sqrt(sum(x * x for x in sas) + 85 * n * (n - 1)) / n
    g = HB.call('fdBRCmb', ags, sas)
    check('R fdBRCmb(%r, %r) = mean %.4f, S_A = (1/n) sqrt(sum Sa^2 + 85 n(n-1)) = %.4f' % (ags, sas, m, s),
          abs(g[0] - m) < 1e-9 and abs(g[1] - s) < 1e-9 and abs(g[2] - sum(x * x for x in sas)) < 1e-9, repr(g))
check('R two roots of SA 10 combine to 9.62, not 7.07 (independent roots): the 85 keeps one person\'s roots together '
      '(the program\'s comment says 9.62 since the second review; the draft said 9.2)',
      abs(HB.call('fdBRCmb', [40.0, 50.0], [10.0, 10.0])[1] - math.sqrt(370) / 2) < 1e-9 and
      'roots of SA 10 give 9.62, not 7.07.' in SRC and '%.2f' % (math.sqrt(370) / 2) == '9.62')

# the menus, independently: the tooth menu's label names the jaw and tooth; the second menu follows the CSV.
# v3.9 (second review): B&R's molar rows are the SIX molars of a jaw, grouped by root (p 19) -- not first molars.
# The molar rows are found by their printed names ("Upper 6 molars root no. N"), not by the CSV's tooth column.
TMENU = ['Upper central incisor', 'Upper lateral incisor', 'Upper canine', 'Upper first premolar',
         'Upper second premolar', 'Upper molar (any of six)', 'Lower central incisor', 'Lower lateral incisor',
         'Lower canine', 'Lower first premolar', 'Lower second premolar', 'Lower molar (any of six)']
ROOTN = {'Mesial root (no. 1)': ('1', 'mesial'), 'Distal root (no. 2)': ('2', 'distal'),
         'Palatal root (no. 3)': ('3', 'palatal')}


def br_paths():
    """every path: (tooth item, second-menu item or None, its items, CSV row, the page's name)"""
    out = []
    for t, lab in enumerate(TMENU, 1):
        jaw, tooth_ = lab.split(' ', 1)
        jaw = jaw.lower()
        if tooth_.startswith('molar'):
            mol = [(i + 1, re.search(r'root no\. (\d)', r['type_of_tooth_as_printed']).group(1))
                   for i, r in enumerate(BRT['VIII'])
                   if r['type_of_tooth_as_printed'].lower().startswith(jaw + ' 6 molars')]
            items = [it for it in ROOTN if ROOTN[it][0] in [n for _, n in mol]]
            for k, it in enumerate(items, 1):
                rr = [i for i, n in mol if n == ROOTN[it][0]][0]
                out.append((t, k, items, rr, 'Any %s molar, %s root' % (jaw, ROOTN[it][1])))
            continue
        rows = [(i + 1, r) for i, r in enumerate(BRT['VIII']) if r['jaw'] == jaw and r['tooth'] == tooth_]
        sides = [r['side_or_root'] for i, r in rows]
        if sides == ['both']:
            out.append((t, None, None, rows[0][0], lab + ' (both)'))
        else:
            for k, sd_ in enumerate(('right', 'left'), 1):
                rr = [i for i, r in rows if r['side_or_root'] == sd_][0]
                out.append((t, k, ['Right', 'Left'], rr, lab + ', ' + sd_))
    return out


PATHS = br_paths()
check('R the menus reach every row once: 24 paths per condition, 48 in all (rows 1-24, each once)',
      len(PATHS) == 24 and sorted(p[3] for p in PATHS) == list(range(1, 25)))
check('R (second review) the molar rows are B&R\'s "Upper 6 molars" / "Lower 6 molars" (p 19: "corresponding roots '
      'from the 6 upper molars ... 6 lower molars"), reached by "Upper molar (any of six)" / "Lower molar (any of six)"; '
      'their n exceed the first molars of Tables I-II (34 upper, 14 lower): %r' %
      [(BRT['VIII'][p[3] - 1]['type_of_tooth_as_printed'], BRT['VIII'][p[3] - 1]['n_teeth']) for p in PATHS
       if p[0] in (6, 12)],
      [p[3] for p in PATHS if p[0] == 6] == [20, 22, 24] and [p[3] for p in PATHS if p[0] == 12] == [21, 23] and
      int(BRT['VIII'][23]['n_teeth']) > 34 and int(BRT['VIII'][22]['n_teeth']) > 14 and
      'Upper first molar' not in SRC and 'Lower first molar' not in SRC)
BRMAX = D(110)


def UPb(x):
    return ['> 110'] if x > 110 else F1(x)


def exp_br(c, r, x, name):
    """the root page's lines and P(age >= 18), independently; None when the age is above 110 (refused)"""
    a, sa, b0, b1, b2, t = br_age(c, r, D(x))
    if a > BRMAX:
        return None, None, a, sa, t
    n_ = BRT['VIII'][r - 1]['n_teeth']
    L = [S(name), S(('Intact: Table ' if c == 1 else 'Section: Table ') + ROM[t] + ' (p %d), n = %s' % (t + 13, n_))]
    if t <= 9:
        L += [S('X = ', F2(D(x)), ' mm, <= 9.0: 2nd degree'), S('A = B0 + B1 X + B2 X^2'),
              S('B0 = ', F2(b0), ', B1 = ', F2(b1), ', B2 = ', rnd_opts(b2, 3))]
    else:
        L += [S('X = ', F2(D(x)), ' mm, > 9.0: 1st degree'), S('A = B0 + B1 X'), S('B0 = ', F2(b0), ', B1 = ', F2(b1))]
    L += [S('= ', F2(a), ' yr'), S('SA = ', F2(sa), ' yr (that row of the table)'),
          S('68%: [', F1(max(D(0), a - sa)), ', ', UPb(a + sa), '] (normal;'),
          S('  B&R Table XII: ca. 65%)'),
          S('95%: [', F1(max(D(0), a - 2 * sa)), ', ', UPb(a + 2 * sa), '] (B&R: ca. 95%)'),
          S('B&R Table XII (p 24), ca. 35%:'),
          S('  A +/- 0.45 SA = [', F1(max(D(0), a - D('0.45') * sa)), ', ', UPb(a + D('0.45') * sa), ']')]
    if D(8) <= D(x) <= D(10):
        # the other equation at the same X: the 1st-degree row at or below 9.0, the 2nd-degree above
        t2 = ((10 if c == 1 else 11) if D(x) <= 9 else (8 if c == 1 else 9))
        row = BRT[ROM[t2]][r - 1]
        ob2 = D(row['B2']) if t2 <= 9 else D(0)
        oth = D(row['B0']) + D(row['B1']) * D(x) + ob2 * D(x) * D(x)
        L += [S('X near 9.0 mm, where B&R switch'), S('equations: Table ' + ROM[t2] + ' gives ', F2(oth), ' yr.')]
    if D(x) > 14:
        L += [S('X > 14 mm: beyond the range of'), S("B&R's figures (they end at 14).")]
    return L, float(norm.sf(18, float(a), float(sa))), a, sa, t


def exp_comb(roots, flag):
    """roots: (A, SA, name, table); flag: a molar root or an upper first premolar among them ->
    the one-person page's lines, P, A, S_A"""
    n = len(roots)
    a = sum(x[0] for x in roots) / n
    v = sum(x[1] * x[1] for x in roots)
    s = (v + 85 * n * (n - 1)).sqrt() / n
    L = [S('One person, %d roots (B&R p 21):' % n)]
    for i, x in enumerate(roots, 1):
        L += [S('%d: ' % i + x[2]), S('   ', F2(x[0]), ' yr, SA ', F2(x[1]), ' (Table ' + ROM[x[3]] + ')')]
    L += [S('A = the mean of the %d ages' % n), S('= ', F2(a), ' yr'), S('S_A = (1/n) sqrt(sum Sa^2 + 85n(n-1))'),
          S('  = (1/%d) sqrt(' % n, F2(v), ' + %d)' % (85 * n * (n - 1))), S('= ', F2(s), ' yr'),
          S('68%: [', F1(max(D(0), a - s)), ', ', UPb(a + s), '] (normal;'), S('  B&R Table XII: ca. 65%)'),
          S('95%: [', F1(max(D(0), a - 2 * s)), ', ', UPb(a + 2 * s), '] (B&R: ca. 95%)'),
          S('Table XII, ca. 35%: [', F1(max(D(0), a - D('0.45') * s)), ', ', UPb(a + D('0.45') * s), ']'),
          S('(85 = 0.85' + MLT + '10' + MLT + '10: teeth of one'), S('person (not molars) correlate r'),
          S('0.80-0.90, p 11.)')]
    if flag:
        L += [S('B&R (p 19): with several teeth, the'), S("best estimate leaves out 'upper"),
              S("first premolars and all the molars'.")]
    return L, float(norm.sf(18, float(a), float(s))), a, s


def br_session(roots, more_last=1, pool=2, tail=(), tail_ev=(), tag=''):
    """roots: (condition, path, X); the last root answered 'No: finish' (more_last), then the pool question.
    A root whose age is above 110 is refused (a MSGBOX) and ends the person."""
    ch, ev, inp, exp = [6, 2], [K], [], []
    for i, (c, p, x) in enumerate(roots):
        t, k, items, r, name = p
        ch += [c, t] + ([k] if k else [])
        inp.append([float(x)])
        L, pr, a, sa, tb = exp_br(c, r, x, name)
        if L is None:
            break
        exp.append((L, pr, a, sa, tb, name, p))
        ev += [K] * npages(L, pr)
        ch.append(2 if i < len(roots) - 1 else more_last)
    ce = None
    if len(exp) > 1:
        flag = any(e[6][0] in (4, 6, 12) for e in exp)
        ce = exp_comb([(e[2], e[3], e[5], e[4]) for e in exp], flag)
        ev += [K] * npages(ce[0], ce[1])
    if exp:
        ch.append(pool)
    ch += list(tail) + [7]
    ev += list(tail_ev) + [K]
    return run(NEW, ch, ev, inp, tag='R ' + tag), exp, ce


h, exp, ce = br_session([(1, PATHS[0], '5')], tag='intro')
ip = page_lines(pages_titled(h, 'BANG & RAMM (1970)')[0])
check('R the intro page (second review): X = TM, the mean of the shortest and longest extent of transparency from the '
      'apex (p 4) -- not a "buccal midline" length; the two equations; several roots combined; the help pointer',
      ip == ['X = TM (mm) of ONE root: the mean of', 'the shortest and longest extent of',
             'transparency from the apex, on the', 'intact root or a longitudinal', 'section (B&R p 4).',
             'X <= 9.0 mm: the 2nd-degree', '  equation (Table VIII or IX);', 'X > 9.0 mm: the 1st-degree',
             '  equation (Table X or XI).', 'Several roots of one person are', '  combined into ONE age (p 21).',
             'Help: main menu > How to use.', 'Next: the root, the tooth, X.'] and
      not any('buccal' in strip_comment(l) for l in SRC.split('\n')), repr(ip))
cs = [(x.title, x.items) for x in h.chooses]
check('R the menus: the root (IT / SS), the twelve teeth (molars "any of six"), the side; "Another root, same person?"; '
      'the pool (Yes / No)',
      cs[2:6] == [('Bang & Ramm: the root', ['Intact root (IT)', 'Longitudinal section (SS)']),
                  ('Bang & Ramm: which tooth?', TMENU), ('Upper central incisor', ['Right', 'Left']),
                  ('Another root, same person?', ['No: finish this person', 'Yes: add another root'])] and
      cs[6] == ('Add to Bayesian pool?', ['Yes', 'No']), repr(cs))
inp_ = h.inputs[0]
check('R one INPUT, X in mm, starting at 0; its help line "TM = mean of shortest and longest extent"',
      inp_.title == 'Bang & Ramm (1970)' and list(inp_.labels) == ['X mm:'] and
      list(inp_.helps) == ['TM = mean of shortest and longest extent'] and
      [inp_.before[n] for n in inp_.names] == [0.0], repr((inp_.labels, inp_.helps)))
# every menu path, both conditions; the lengths cycle through both equations, the switch and beyond 14 mm
XCYC = ['3.5', '7', '9', '9.01', '11.5', '14', '0', '15', '8.5', '9.5', '10']
npth = nref = 0
for c in (1, 2):
    for j, p in enumerate(PATHS):
        x = XCYC[(j + 5 * c) % len(XCYC)]
        h, exp, ce = br_session([(c, p, x)], tag='%d %s X %s' % (c, p[4], x))
        cq = [x_ for x_ in h.chooses if x_.title == TMENU[p[0] - 1]]
        if not exp:
            a_ = br_age(c, p[3], D(x))[0]
            check('R path %s, %s, X = %s mm: A = %s > 110 refused, no page' % ('IT' if c == 1 else 'SS', p[4], x, a_),
                  not pages_titled(h, 'BANG & RAMM (1970)  root') and len(h.msgboxes) == 2 and
                  h.msgboxes[0].lines[0] == 'A = %s yr: above 110,' % first(S(F2(a_))), repr([m.lines for m in h.msgboxes]))
            nref += 1
            continue
        L, pr, a, sa, tb, name, _ = exp[0]
        pg = pages_titled(h, 'BANG & RAMM (1970)  root 1')
        okr, dr = same_rows(pg, L, pr)
        check('R path %s, %s, X = %s mm: the root page = independent (row %d, Table %s), the band, the second menu %r'
              % ('IT' if c == 1 else 'SS', p[4], x, p[3], ROM[tb], p[2]),
              okr and len(pg) == npages(L, pr) and all(band_ok(s_, pr) for s_ in pg) and
              ([x_.items for x_ in cq] == ([p[2]] if p[2] else [])),
              repr((dr[:3], [band_line(s_) for s_ in pg], cq)))
        npth += 1
print('   %d menu paths (12 teeth, their sides or roots, intact and section): %d pages, %d refused above 110 yr'
      % (npth + nref, npth, nref))
# the switch note at 8.5 and 9.5, none at 7.99 / 10.01
for x, want in (('8.5', True), ('9.5', True), ('8', True), ('10', True), ('7.99', False), ('10.01', False)):
    h, exp, ce = br_session([(1, PATHS[0], x)], tag='near 9: %s' % x)
    pl = [l for s_ in pages_titled(h, 'BANG & RAMM (1970)  root 1') for l in page_lines(s_)]
    check('R X = %s mm: the "X near 9.0 mm" note %s' % (x, 'shown, with the other equation\'s age' if want else 'absent'),
          ('X near 9.0 mm, where B&R switch' in pl) == want and same_rows(pages_titled(h, 'BANG & RAMM (1970)  root 1'),
                                                                          exp[0][0], exp[0][1])[0], repr(pl))
# beyond 14 mm: a warning; above 110 yr: refused (second review)
h, exp, ce = br_session([(1, PATHS[0], '14.5')], tag='X 14.5')
pl = [l for s_ in pages_titled(h, 'BANG & RAMM (1970)  root 1') for l in page_lines(s_)]
check('R X = 14.5 mm (upper central incisor, right, intact: %s yr): "X > 14 mm: beyond the range of B&R\'s figures (they '
      'end at 14)."; an upper end above 110 prints "> 110"' % first(S(F2(exp[0][2]))),
      'X > 14 mm: beyond the range of' in pl and "B&R's figures (they end at 14)." in pl and
      any('> 110' in l for l in pl) and not any('110.0' in l for l in pl), repr(pl))
h, exp, ce = br_session([(1, PATHS[0], '14')], tag='X 14')
pl = [l for s_ in pages_titled(h, 'BANG & RAMM (1970)  root 1') for l in page_lines(s_)]
check('R X = 14 mm: no warning (the end of B&R\'s figures)', not any('X > 14 mm' in l for l in pl), repr(pl))
for c, p, x in ((1, PATHS[0], '25'), (1, PATHS[0], '16')):
    a_ = br_age(c, p[3], D(x))[0]
    h = run(NEW, [6, 2, c, p[0], p[1], 7], [K, K], [[float(x)]], tag='R above 110 %s' % x)
    check('R %s, X = %s mm: A = %s yr is above 110: "A = %s yr: above 110, / beyond any age the tables were / built on '
          '(B&R\'s oldest: 80+). / This root not used." then "No root measured"; no page, no pool question' %
          (p[4], x, a_, first(S(F2(a_)))),
          [m.lines for m in h.msgboxes] == [['A = %s yr: above 110,' % first(S(F2(a_))), 'beyond any age the tables were',
                                            "built on (B&R's oldest: 80+).", 'This root not used.'],
                                           ['No root measured. Nothing stored.']] and
          not pages_titled(h, 'BANG & RAMM (1970)  root'), repr([m.lines for m in h.msgboxes]))
# several roots of one person
R2 = [(1, PATHS[0], '5'), (2, PATHS[16], '12')]
R3 = [(1, PATHS[5], '6'), (1, PATHS[6], '9.5'), (1, PATHS[7], '11')]
for roots, tg, fl in ((R2, 'two roots', False), (R3, 'three roots of an upper molar', True)):
    # then the Bayesian item: K for its page, Done on the curve, K for the report (one page)
    h, exp, ce = br_session(roots, pool=1, tail=(6, 3), tail_ev=(K, soft(6), K), tag=tg)
    for i in range(len(roots)):
        pg = pages_titled(h, 'BANG & RAMM (1970)  root %d' % (i + 1))
        check('R %s: root %d\'s page = independent' % (tg, i + 1), same_rows(pg, exp[i][0], exp[i][1])[0])
    cp = pages_titled(h, 'BANG & RAMM: one person')
    okr, dr = same_rows(cp, ce[0], ce[1])
    cl = [l for p in cp for l in page_lines(p)]
    check('R %s: the one-person page: the mean %.2f, S_A %.2f by B&R p 21, the band from N(A, S_A); "teeth of one person '
          '(not molars) correlate r 0.80-0.90, p 11"; B&R p 19\'s advice %s' %
          (tg, ce[2], ce[3], 'shown (molar roots)' if fl else 'absent (no molar, no upper first premolar)'),
          okr and all(band_ok(s_, ce[1]) for s_ in cp) and 'person (not molars) correlate r' in cl and
          (("first premolars and all the molars'." in cl) == fl), repr(dr[:3]))
    q = [x_ for x_ in h.chooses if x_.title == 'Add to Bayesian pool?']
    post_ = [l for pp in pages_titled(h, 'BAYESIAN POSTERIOR') for l in page_lines(pp)]
    check('R %s: the pool is offered ONE value, the combined one (stored: mean %.2f, SD %.2f x 1.25)' %
          (tg, ce[2], ce[3]), len(q) == 1 and [m.lines[0] for m in h.msgboxes] == ['Stored. 1 method(s) active.'] and
          matches(post_[0], S('Mean:   ', F2(ce[2]), ' yr')) and
          matches(post_[1], S('SD:     ', F2(ce[3] * D('1.25')), ' yr')) and post_[8] == '  Bang-Ramm: 100.0%',
          repr(post_[:9]))
# an upper first premolar with another tooth: the advice too
h, exp, ce = br_session([(1, PATHS[0], '5'), (2, PATHS[6], '6')], tag='with an upper first premolar')
cl = [l for p in pages_titled(h, 'BANG & RAMM: one person') for l in page_lines(p)]
check('R an upper central incisor with an upper first premolar: B&R p 19\'s advice on the one-person page',
      PATHS[6][4] == 'Upper first premolar (both)' and "first premolars and all the molars'." in cl and
      same_rows(pages_titled(h, 'BANG & RAMM: one person'), ce[0], ce[1])[0], repr(cl))
# the same root twice for one person (intact, then section of the same root): refused (second review)
L1, p1, a1, s1, t1 = exp_br(1, PATHS[0][3], '5', PATHS[0][4])
h = run(NEW, [6, 2, 1, 1, 1, 2, 2, 1, 1, 1, 7], [K] + [K] * npages(L1, p1) + [K], [[5.0]], tag='R the same root twice')
check('R the same root twice (upper central incisor, right: intact, then its section): "This root is already in this '
      'person\'s list (intact or section): one value per root. This root not used."; the person keeps root 1, no X '
      'asked again, no one-person page',
      [m.lines for m in h.msgboxes][0] == ['This root is already in this', "person's list (intact or section):",
                                           'one value per root.', 'This root not used.'] and len(h.inputs) == 1 and
      not pages_titled(h, 'BANG & RAMM: one person') and
      len([c_ for c_ in h.chooses if c_.title == 'Add to Bayesian pool?']) == 1, repr([m.lines for m in h.msgboxes]))
h, exp, ce = br_session([(1, PATHS[0], '5'), (1, PATHS[1], '5')], tag='right then left')
check('R the right and the left of one tooth are two roots: both kept, one-person page', ce is not None and
      len(pages_titled(h, 'BANG & RAMM: one person')) >= 1)
if HAVE_PREFIX:
    hp_ = free_run(PREFIX, [6, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 7], inputs=[[5.0], [5.0]])
    check('R the v3.9 draft before the second review took the same root twice and combined them',
          len(pages_titled(hp_, 'BANG & RAMM: one person')) >= 1)
# the refusals and the edges
for x, msg in (('-0.1', ['The transparent length X cannot', 'be negative: it is a length.', 'This root not used.']),
               ('25.1', ['X = 25.10 mm: longer than any', 'root (FDAES takes 0 to 25 mm).', 'This root not used.'])):
    h = run(NEW, [6, 2, 1, 1, 1, 7], [K, K], [[float(x)]], tag='R refusal %s' % x)
    check('R X = %s refused: %r, then "No root measured. Nothing stored."; no page, no pool question' % (x, msg[0]),
          [m.lines for m in h.msgboxes] == [msg, ['No root measured. Nothing stored.']] and
          not pages_titled(h, 'BANG & RAMM (1970)  root') and
          not [c_ for c_ in h.chooses if c_.title == 'Add to Bayesian pool?'], repr([m.lines for m in h.msgboxes]))
LM1 = [p for p in PATHS if p[0] == 12 and p[1] == 1][0]          # any lower molar, mesial root: row 21
for c, p, x in ((2, PATHS[3], '0'), (2, LM1, '25')):
    h, exp, ce = br_session([(c, p, x)], tag='edge %s' % x)
    check('R X = %s mm accepted (%s, %s: %s yr)' % (x, 'IT' if c == 1 else 'SS', p[4], exp[0][2] if exp else None),
          exp and len(pages_titled(h, 'BANG & RAMM (1970)  root 1')) >= 1 and not h.msgboxes)
# a cancel at each step
NR = ['No root measured. Nothing stored.']
CAN = [('the root menu', [6, 2, 0, 7], [], [NR]),
       ('the tooth menu', [6, 2, 1, 0, 7], [], [NR]),
       ('the side menu', [6, 2, 1, 1, 0, 7], [], [NR]),
       ('the molar\'s root menu', [6, 2, 2, 6, 0, 7], [], [NR]),
       ('the X form', [6, 2, 1, 4, 7], [CANCEL], [['Cancelled: this root not used.'], NR])]
for tg, ch_, inp, msgs in CAN:
    h = run(NEW, ch_, [K, K], inp, tag='R cancel at %s' % tg)
    check('R a cancel at %s: %s; no page, no pool question' % (tg, ' / '.join(m[0] for m in msgs)),
          [m.lines for m in h.msgboxes] == msgs and not pages_titled(h, 'BANG & RAMM (1970)  root') and
          not [c_ for c_ in h.chooses if c_.title == 'Add to Bayesian pool?'], repr([m.lines for m in h.msgboxes]))
# a cancel at "Another root?" finishes the person with the one root; a cancel in root 2's menus keeps root 1
h = run(NEW, [6, 2, 1, 1, 1, 0, 1, 7], [K] + [K] * npages(L1, p1) + [K], [[5.0]], tag='R cancel at Another root')
check('R a cancel at "Another root, same person?": the person is finished with the one root (no one-person page); '
      'the pool is offered that root (%.2f, SA %.2f)' % (a1, s1),
      not pages_titled(h, 'BANG & RAMM: one person') and
      [m.lines[0] for m in h.msgboxes] == ['Stored. 1 method(s) active.'])
h = run(NEW, [6, 2, 1, 1, 1, 2, 1, 0, 2, 7], [K] + [K] * npages(L1, p1) + [K], [[5.0]], tag='R cancel in root 2')
check('R a cancel in root 2\'s menus keeps root 1: no one-person page, the pool offered once',
      len(pages_titled(h, 'BANG & RAMM (1970)  root 1')) == 1 and not pages_titled(h, 'BANG & RAMM: one person') and
      len([c_ for c_ in h.chooses if c_.title == 'Add to Bayesian pool?']) == 1 and not h.msgboxes)
h = run(NEW, [6, 2, 1, 1, 1, 1, 0, 6, 3, 7], [K] + [K] * npages(L1, p1) + [K], [[5.0]],
        tag='R cancel at the pool')
check('R a cancel at the pool question stores nothing (Bayesian: "No estimates stored yet.")',
      [m.lines[0] for m in h.msgboxes] == ['No estimates stored yet.'])
code = ''.join(strip_comment(l) for l in SRC.split('\n'))
check('R v3.8a\'s line "14.8 + 1.35 T%" (not in the paper) is gone from the code',
      '14.8' not in code and '1.35' not in code)
# ===================================================================================== Part J
print('J. Johanson 1971 (C-F5, C-F9)')
JW = [('T', '8.98'), ('R', '5.57'), ('A', '5.14'), ('P', '4.14'), ('C', '3.71'), ('S', '2.30')]
JOH1 = D('6.0')       # v3.9a (Roger's D5, 19 Oct 2026): one tooth, Johanson 1971 Table 8 (v3.9: 8.00)


def exp_joh(sc, jnc):
    """sc: dict A S P C R T (Decimals); jnc 1 one tooth (v3.9a: 6.0, Johanson's Table 8; v3.9 8.00), 2 two or more
    (5.16) -> lines, P (SciPy), age, ok"""
    age = D('11.02') + sum(D(w) * sc[k] for k, w in JW)
    sv = D('5.16') if jnc == 2 else JOH1
    if not (18 <= age <= 110):
        return None, None, age, False
    L = [S('%s = %s' % (k, '%.1f' % sc[k]) + MLT + w + ' = ', rnd_opts(D(w) * sc[k], 3)) for k, w in JW]
    L += [S('Intercept = 11.020'), S('Age = ', rnd_opts(age, 3), ' yr')]
    L += ([S("SD 5.16 yr = SD of Johanson's fit,"), S('Table 5 (46 people, 1-11 teeth each)')] if jnc == 2 else
          [S('1 tooth: SD ', F1(JOH1), ' (Johanson Table 8;'), S('  Lucy 1995, 17 new people: ~5.6).')])
    L += [S('68%: [', F1(max(D(0), age - sv)), ', ', UP(age + sv), ']'),
          S('95%: [', F1(max(D(0), age - 2 * sv)), ', ', UP(age + 2 * sv), ']'),
          S("Johanson's text prints 9.98T, his"), S('Table 5 8.98T; FDAES uses Table 5.')]
    return L, float(norm.sf(18, float(age), float(sv))), age, True


rj = random.Random(1971)
SETS = [{k: D('0') for k in 'ASPCRT'}, {k: D('3') for k in 'ASPCRT'},
        dict(A=D('1'), S=D('1.5'), P=D('0.5'), C=D('0.5'), R=D('0'), T=D('2.5'))]
while len(SETS) < 120:
    SETS.append({k: D(rj.randint(0, 6)) / 2 for k in 'ASPCRT'})
JT = 'JOHANSON (1971) result'
nj, nout = 0, 0
for i, sc in enumerate(SETS):
    jnc = 1 + i % 2 if i != 2 else 2
    L, pr, age, ok = exp_joh(sc, jnc)
    vals = [float(sc[k]) for k in 'ASPCRT']
    if ok:
        h = run(NEW, [6, 1, jnc, 2, 7], [K] + [K] * npages(L, pr) + [K], [vals], tag='J %r' % vals)
        pg = pages_titled(h, JT)
        okr, dr = same_rows(pg, L, pr)
        check('J scores A S P C R T = %s, %s: the page = independent (age %s), both pages banded' %
              (' '.join('%s' % sc[k] for k in 'ASPCRT'), 'one tooth' if jnc == 1 else '2+ teeth', age),
              okr and len(pg) == npages(L, pr) == 2 and all(band_ok(s_, pr) for s_ in pg), repr(dr[:3]))
        nj += 1
    else:
        h = run(NEW, [6, 1, jnc, 7], [K, K], [vals], tag='J out %r' % vals)
        ml = [m.lines for m in h.msgboxes]
        check('J scores %s: age %s outside 18-110: "Age %s yr outside / valid range 18-110. Check scores.", no page'
              % (vals, age, rnd_opts(age, 1)[0]),
              len(ml) == 1 and len(ml[0]) == 2 and matches(ml[0][0], S('Age ', rnd_opts(age, 1), ' yr outside')) and
              ml[0][1] == 'valid range 18-110. Check scores.' and not pages_titled(h, JT), repr(ml))
        nout += 1
print('   %d score sets: %d pages, %d refused (under 18)' % (len(SETS), nj, nout))
h = run(NEW, [6, 1, 2, 1, 7], [K, K, K, K], [[1, 1.5, .5, .5, 0, 2.5]], tag='J worked example')
cs = [(c.title, c.items) for c in h.chooses if c.title == 'Number of teeth averaged?']
check('J the menu says what each spread is: (v3.9a) "1 tooth   6.0 (his Table 8)", "2+ teeth  5.16 (Johanson '
      'SD)" (v3.9: "1 tooth   8.00 (FDAES only)"; v3.8a: "SE = +/- 8.00 yr" / "SE = +/- 5.16 yr")',
      cs == [('Number of teeth averaged?', ['1 tooth   6.0 (his Table 8)', '2+ teeth  5.16 (Johanson SD)'])],
      repr(cs))
jl = [l for s_ in pages_titled(h, JT) for l in page_lines(s_)]
check('J the worked example (A 1, S 1.5, P 0.5, C 0.5, R 0, T 2.5): "T = 2.5 x 8.98 = 22.450" ... "Age = 45.985 yr"; '
      'every term spaced (C-F9)', jl[:8] == ['T = 2.5' + MLT + '8.98 = 22.450', 'R = 0.0' + MLT + '5.57 = 0.000',
                                            'A = 1.0' + MLT + '5.14 = 5.140', 'P = 0.5' + MLT + '4.14 = 2.070',
                                            'C = 0.5' + MLT + '3.71 = 1.855', 'S = 1.5' + MLT + '2.30 = 3.450',
                                            'Intercept = 11.020', 'Age = 45.985 yr'], repr(jl))
check('J the 9.98 / 8.98 note on the page, and 5.16 named: "SD of Johanson\'s fit, Table 5 (46 people, 1-11 teeth '
      'each)" (people, not teeth)',
      "Johanson's text prints 9.98T, his" in jl and 'Table 5 8.98T; FDAES uses Table 5.' in jl and
      "SD 5.16 yr = SD of Johanson's fit," in jl and 'Table 5 (46 people, 1-11 teeth each)' in jl and
      not any('2+ teeth each' in t.text for s_ in h.pages for t in s_.texts) and
      not any('46 teeth' in t.text for s_ in h.pages for t in s_.texts))
h1 = run(NEW, [6, 1, 1, 2, 7], [K, K, K, K], [[1, 1.5, .5, .5, 0, 2.5]], tag='J one tooth')
j1 = [l for s_ in pages_titled(h1, JT) for l in page_lines(s_)]
check('J one tooth (v3.9a, Roger\'s D5): "1 tooth: SD 6.0 (Johanson Table 8; / Lucy 1995, 17 new people: ~5.6)."; '
      '45.985 +/- 6.0: "68%: [40.0, 52.0]", "95%: [34.0, 58.0]" (v3.9: SD 8.00, "68%: [38.0, 54.0]")',
      '1 tooth: SD 6.0 (Johanson Table 8;' in j1 and '  Lucy 1995, 17 new people: ~5.6).' in j1 and
      '68%: [40.0, 52.0]' in j1 and '95%: [34.0, 58.0]' in j1 and not any('8.00' in l or 'allowance' in l for l in j1),
      repr(j1))
check('J pooled: "Stored. 1 method(s) active."', [m.lines[0] for m in h.msgboxes] == ['Stored. 1 method(s) active.'])
h3 = run(NEW, [6, 1, 1, 2, 7], [K, K, K, K], [[3, 3, 3, 3, 3, 3]], tag='J all 3, one tooth')
j3 = [l for s_ in pages_titled(h3, JT) for l in page_lines(s_)]
check('J all scores 3, one tooth (100.54 yr, SD 6.0 since v3.9a): "95%: [88.5, > 110]", never a clamped "110.0" '
      '(second review)', '95%: [88.5, > 110]' in j3 and '68%: [94.5, 106.5]' in j3 and
      not any('110.0' in l for l in j3), repr(j3))
ip = page_lines(pages_titled(h, 'JOHANSON (1971)  Histological')[0])
check('J the intro page keeps 13 lines, the help pointer in the old blank line\'s place',
      ip[0] == 'Score each variable 0-3 in 0.5 steps.' and ip[-2:] == ['Help: main menu > How to use.',
                                                                     'You will enter 6 scores next.'] and len(ip) == 12,
      repr(ip))
# the refusals of v3.8a are kept
for vals, tg in (([1, 1, 1, 1, 1, 3.5], 'a score above 3'), ([1, 1, 1, 1, 1, 1.25], 'a quarter step'), (CANCEL, 'Cancel')):
    h = run(NEW, [6, 1, 7], [K, K], [vals], tag='J refused ' + tg)
    check('J %s: "Cancelled, or a score was not / 0, 0.5, ... 3. / Nothing stored." (v3.8a\'s)' % tg,
          [m.lines for m in h.msgboxes] == [['Cancelled, or a score was not', '0, 0.5, 1, 1.5, 2, 2.5, or 3.',
                                             'Nothing stored.']], repr([m.lines for m in h.msgboxes]))
h = run(NEW, [6, 1, 0, 7], [K, K], [[1, 1.5, .5, .5, 0, 2.5]], tag='J cancel teeth')
check('J Cancel at "Number of teeth averaged?" stores nothing (v3.8a\'s)',
      [m.lines for m in h.msgboxes] == [['Cancelled. Nothing stored.']] and not pages_titled(h, JT))
# ===================================================================================== Part K
print('K. The Verify Calculations pages 1-4 against an independent computation')
# hv: Part E's run of the six self-check pages
lP_, lT_ = D(3) * 100 / 15, D(6) * 100 / 15
lam_ = D('0.18') * lP_ + D('0.42') * lT_ + D('25.53')
pu_ = PUC[4][0] * 15 + PUC[4][1] * lP_ + PUC[4][2] * lT_ + PUC[4][3]
k1 = page_lines(pages_titled(hv, 'ARITHMETIC SELF-CHECK')[0])
check('K page 1: P = 20.00, T = 40.00; Lamendin %.2f yr, SD 12.5 (fdLamSD; "by hand 10 x sqrt(pi/2) = 12.53, rounded"); P-U white males %.2f yr, SEE 9.58; by hand 45.93 '
      'and 46.82' % (lam_, pu_),
      k1 == ['Demo: white male, one tooth, mm:', 'RH 15, periodontosis 3, transl. 6',
             'P = 3' + MLT + '100 / 15 = 20.00', 'T = 6' + MLT + '100 / 15 = 40.00',
             'LAMENDIN: 0.18' + MLT + '20 + 0.42' + MLT + '40', '  + 25.53 = 45.93 yr',
             '  SD 12.5 (by hand 10' + MLT + 'sqrt(pi/2)', '  = 12.53, rounded)', 'P-U, WHITE MALES (Table 6):',
             '0.15' + MLT + '15 + 0.29' + MLT + '20 + 0.39' + MLT + '40', '  + 23.17 = 46.82 yr, SEE 9.58',
             'By hand: 45.93 and 46.82 yr.', 'One tooth: pool ONE of the two.'] and
      '%.2f' % (10 * math.sqrt(math.pi / 2)) == '12.53'
      and lam_ == D('45.93') and pu_ == D('46.82') and '%.2f' % PURM[4] == '9.58', repr(k1))
ja = D('11.02') + D('5.14') * 1 + D('2.30') * D('1.5') + D('4.14') * D('0.5') + D('3.71') * D('0.5') + D('8.98') * D('2.5')
b1 = br_age(2, 9, D(6))
k2 = page_lines(pages_titled(hv, 'ARITHMETIC SELF-CHECK  (2)')[0])
check('K page 2: Johanson %s yr (SD 5.16, 46 people); Bang & Ramm Table IX row 9 (%s) at X = 6: %s yr, SA %s' %
      (ja, BRT['IX'][8]['type_of_tooth_as_printed'], b1[0], b1[1]),
      k2 == ['JOHANSON (A = 1, S = 1.5, P = 0.5,', 'C = 0.5, R = 0, T = 2.5; 2+ teeth):',
             '11.02 + 5.14 + 3.45 + 2.07 + 1.855', '+ 0 + 22.45 = 45.985 yr', 'By hand: 45.985 yr.',
             "SD 5.16 yr: SD of Johanson's fit,", 'Table 5 (46 people, 1-11 teeth each).',
             'BANG & RAMM, root 1: upper left', 'second premolar, section, X = 6 mm', '(<= 9.0: Table IX, row 9):',
             '22.34 + 7.59' + MLT + '6 - 0.393' + MLT + '36', '= 53.73 yr, SA 6.88 (by hand 53.73)'] and
      ja == D('45.985') and b1[0] == D('53.732') and b1[1] == D('6.88') and b1[5] == 9 and
      BRT['IX'][8]['type_of_tooth_as_printed'] == 'Upper left second premol.', repr(k2))
b2 = br_age(1, 13, D(11))
cm = (b1[0] + b2[0]) / 2
cs_ = (b1[1] ** 2 + b2[1] ** 2 + 170).sqrt() / 2
c0 = (b1[1] ** 2 + b2[1] ** 2).sqrt() / 2
k3 = page_lines(pages_titled(hv, 'ARITHMETIC SELF-CHECK  (3)')[0])
check('K page 3: root 2 (Table X row 13, %s) at X = 11: %s yr, SA %s; one person: mean %.3f, S_A %.4f (without the '
      '85: %.4f)' % (BRT['X'][12]['type_of_tooth_as_printed'], b2[0], b2[1], cm, cs_, c0),
      k3 == ['BANG & RAMM, root 2, same person:', 'lower left lateral incisor, intact,',
             'X = 11 mm (> 9.0: Table X, row 13):', '33.65 + 3.53' + MLT + '11 = 72.48 yr',
             "SA 11.12 (B&R Fig. 16's line)", 'ONE PERSON (p 21): A = their mean',
             '= (53.732 + 72.48) / 2 = 63.11', 'S_A = (1/2) sqrt(6.88^2 + 11.12^2',
             '  + 85' + MLT + '2' + MLT + '1) = 9.23 yr', 'By hand: 72.48; 63.11 and 9.23 yr.',
             '(Without the 85: (1/2) sqrt(170.99)', '= 6.54 yr: as if independent.)', 'Pool ONE value for this person.']
      and b2[0] == D('72.48') and '%.2f' % cm == '63.11' and '%.2f' % cs_ == '9.23' and '%.2f' % c0 == '6.54', repr(k3))
sds_ = [PURM[4], D('5.16'), cs_]
mns_ = [pu_, ja, cm]
pr_ = [1 / s ** 2 for s in sds_]
tp_ = sum(pr_)
mu_ = sum(m * p for m, p in zip(mns_, pr_)) / tp_
sd0 = (1 / tp_).sqrt()
k4 = page_lines(pages_titled(hv, 'ARITHMETIC SELF-CHECK  (4)')[0])
print('   page 4 by hand: precisions %s; total %.5f; mean %.4f; SD %.4f x 1.25 = %.4f, floored to 5.16; weights %s' %
      (', '.join('%.5f' % p for p in pr_), tp_, mu_, sd0, sd0 * D('1.25'),
       ', '.join('%.1f%%' % (100 * p / tp_) for p in pr_)))
check('K page 4: the pool of P-U + Johanson + B&R by hand (mean %.2f, SD %.3f x 1.25 = %.2f, floored to 5.16)' %
      (mu_, sd0, sd0 * D('1.25')),
      k4 == ['BAYESIAN (P-U + Joh + B&R):', 'Prec: %.5f + %.5f + %.5f' % tuple(pr_), 'Total prec = %.5f' % tp_,
             'Mean = %.2f yr' % mu_, 'SD = SQRT(1/%.5f)' % tp_ + MLT + '1.25',
             '   = %.3f' % sd0 + MLT + '1.25 = %.2f' % (sd0 * D('1.25')), 'FLOORED to 5.16 (best single SD)',
             'Wts: P-U %.1f%%, Joh %.1f%%, BR %.1f%%' % tuple(100 * p / tp_ for p in pr_),
             'By hand: 0.01090 + 0.03756 +', '0.01173 = 0.06019; mean 49.47;', '4.076' + MLT + '1.25 = 5.09 < 5.16.',
             'Lamendin and P-U: never both (one', 'tooth); here P-U stands for it.'] and
      ['%.5f' % p for p in pr_] == ['0.01090', '0.03756', '0.01173'] and '%.5f' % tp_ == '0.06019' and
      '%.2f' % mu_ == '49.47' and '%.3f' % sd0 == '4.076' and sd0 * D('1.25') < D('5.16'), repr(k4))
check('K the six self-check pages open in order and nothing else is drawn',
      [title(p) for p in hv.pages] == ['FDAES v3.9b', 'ARITHMETIC SELF-CHECK'] +
      ['ARITHMETIC SELF-CHECK  (%d)' % i for i in range(2, 7)] + ['FDAES session ended'], repr([title(p) for p in hv.pages]))
# ===================================================================================== Part H
print('H. The help topics and the disclaimer (Roger, 19 Oct 2026, 12:45 and 12:48)')
NABOUT = 20          # About's pages and the exit page (v3.9, second review: Gustafson's page now two; v3.9a: the
                     # history page two as well)
OPEN_T = 'FDAES v3.9b'   # the opening page's title (v3.9: 'FDAES v3.9')
HTOP = ['HOW TO USE FDAES', 'HELP: WILLEMS 2001', 'HELP: LIVERSIDGE 2006', 'HELP: M3 (MINCER 1993)', 'HELP: LAMENDIN 1992',
        'HELP: PRINCE-UBELAKER 2002', 'HELP: JOHANSON 1971', 'HELP: BANG & RAMM 1970', 'ASSUMPTIONS', 'WHAT FDAES IS NOT']
HMENU = ['Using FDAES', 'Willems 2001', 'Liversidge 2006', 'M3 (Mincer 1993)', 'Lamendin 1992', 'Prince-Ubelaker 2002',
         'Johanson 1971', 'Bang & Ramm 1970', 'Assumptions', 'What FDAES is not']


def help_items(n):
    """the topic's lines as the source lists them (fdHelp's topic n): every listed string, and (v3.9, second review)
    the three lines fdLamLbl adds where a topic CONCATs them"""
    body = SRC[SRC.index('IF htp == %d THEN' % n):]
    body = body[:body.index('\n  END;')]
    items = [l.strip().rstrip(',').rstrip('});') for l in body.split('\n')[2:] if l.strip().startswith('"')]
    return items + ['(fdLamLbl)'] * (3 * body.count('fdLamLbl('))


HX = {}
for n in range(1, 11):
    items = help_items(n)
    npg = (len(items) + 12) // 13
    h = run(NEW, [5, n, 0, 7], [K] * npg + [K], tag='H topic %d' % n)
    pg = pages_titled(h, HTOP[n - 1])
    lines = [l for p in pg for l in page_lines(p)]
    foot = [[t.text for t in p.texts if t.y == 224 and t.font == 1] for p in pg]
    HX[n] = ' '.join(lines)
    cs = [(c.title, c.items) for c in h.chooses]
    check('H topic %d "%s": opens from the help menu, %d line(s) on %d page(s), "page i of n" footers, back to the help '
          'menu, then the main menu' % (n, HTOP[n - 1], len(items), npg),
          len(pg) == npg and len(lines) == len([i for i in items if i != '""']) and
          (npg == 1 or foot == [['page %d of %d, any key or tap = %s' % (i, npg, 'next' if i < npg else 'back')]
                                for i in range(1, npg + 1)]) and
          [c[0] for c in cs] == ['FDAES  (1 of 2)', 'How to use / assumptions', 'How to use / assumptions',
                                 'FDAES  (1 of 2)'] and cs[1][1] == HMENU, repr((len(pg), foot, cs[:2])))
    check('H topic %d: every line <= 37 characters, no band' % n,
          all(len(l) <= 37 for l in lines) and all(band_texts(p) is None for p in pg))
# the facts each topic must carry, with their pages (from the papers' page images and text; see the CHANGES file)
FACTS = {
    1: ['TEACHING & DEMONSTRATION AID: not', 'SETUP FIRST', "Sex 'Unknown': Willems mixes boys and girls 50:50; "
        "Liversidge uses the combined columns (girls' H floors); M3 shows both sexes; P-U has no equation. Ancestry "
        "Unknown or Other: no P-U equation. Lamendin, Johanson and Bang & Ramm use neither.",
        'Never two results from the same', "M3 is never pooled",
        'Cut-points 5% and 95%, printed in every band, applied to P as printed (to 0.1%).'],
    2: ['SAMPLE (p 893): Belgian Caucasian', '2523 radiographs', '1265 boys aged 1.8-18.0 and 1258',
        'girls aged 2.1-18.0', "(1029 boys, 1087 girls) within Demirjian's age limits (p 893)",
        '355 (195 boys, 160 girls) tested the new scores', 'SPREAD (p 894)',
        '0.9 yr boys, 1.3 yr girls; mean difference (signed) 0.0 and +0.2.',
        "teeth 33-37 all at H is the tables' ceiling (FDAES's rule)", 'the largest sums are 16.03 boys and 15.93 '
        "girls (Table 2 scores 31 and 32 higher at G than at H)", "'at least about 15.8-16'",
        'The sample stopped at 18.0.'],
    3: ['(pp 454-455, 465): 9002', '(4480 girls, 4522 boys)', 'Table X, p 467', '(p 467)', '13.42 yr'],
    4: ['823 cases from 24 ABFO diplomates', 'aged 14.1-24.9', '271 males, 323 females (p 382)',
        'erratum, p 1524', 'under 25', '(p 387)', 'never pooled'],
    5: ['(pp 1374-1375)', 'SAMPLE (p 1374): 306 teeth from 208', 'people aged 22-90 (135 men, 73',
        'women; 198 white, 10 black). Country', 'not stated', 'A = 0.18 P + 0.42 T + 25.53',
        'mean error 10 yr (Table 1, p 1376)', '8.4 yr on 45 forensic teeth',
        "an 'average difference' (p 1377); whether signs were ignored is not stated. FDAES treats it as the average "
        "size of a miss, as Prince & Ubelaker's 'mean difference' is.", ' '.join(LAMLBL),
        '24.8 yr at 26-29', "'Reasonably accurate except for ... under age 40' (p 1373)",
        "'useless for individuals under 25 years of age' (p 1376)",
        'Lamendin never gives below 25.53 yr, so with SD 12.5 P(age >= 18) is never below 72.7%.'],
    6: ['the Terry Collection', '400 teeth from 359', 'aged 25-99: 94 black women', '72 white women (27-90)',
        '98 black men (26-76), 95 white men', '(27-85). Each fit used 100 teeth', '(99 for the white men)',
        'EQUATIONS (pp 111-112)', 'Tables 3-6 (pp 112-115)',
        'black men %.2f, white women %.2f, black women %.2f, white men %.2f yr' % (PURM[1], PURM[2], PURM[3], PURM[4]),
        'ancestry alone made no difference (pp 110-111); sex did.', "no equation for 'Other' or 'Unknown'",
        "'in conjunction with others' (p 116)",
        "An estimate outside their sample's ages (25-99, p 108) is shown as an extrapolation: no band, not pooled."],
    7: ['Before extraction: A attrition and P the periodontal state. On a ground section (about 0.25 mm): S '
        'secondary dentine, C cementum, R root resorption, T root transparency.',
        '162 teeth from 46 people chosen at random (31 men, 15 women), aged 23-79', 'not stated in the pages read',
        '(Table 5, line VI)', '11.02 + 8.98T + 5.14A + 4.14P + 5.57R + 3.71C + 2.30S', 'prints 9.98T',
        '(44.92 yr)', "'Standard deviation = 5.16'", 'over 46 people (42 gave 2-11 teeth, 4 gave one)',
        "his entity was the 'mouth' (2 teeth or more), not the single tooth",
        # v3.9a (Roger's D5): one tooth SD 6.0 from Table 8, and Lucy, Pollard & Roberts 1995's test
        "Table 8: 'Error' 6.0 for one tooth, 5.2 for two (the fit's SD: 5.16), 4.4 for ten. FDAES: 1 tooth SD 6.0; "
        "2+ teeth SD 5.16, not made smaller.", "TEST (Lucy, Pollard & Roberts 1995): 35 roots of 17 new people: mean "
        "deviation 4.5 yr (SD ~5.6 if normal); about 68% within +/-5.16. Small test: new cases may miss more.",
        'Johanson describes no test sample of his own in the pages read.'],
    8: ['MEASURE (p 4): X = TM, the mean of the shortest (TL1) and the longest (TL2) extent of root transparency from '
        'the apex, in mm (Fig. 1: 6.0 and 9.0 give 7.5)', 'one root at a time', '926 teeth (978 roots)',
        '201 patients', '64 autopsies', 'Country not stated (authors in Bergen, Norway)', 'X <= 9.0 mm',
        'MOLARS: the roots of the six upper (or six lower) molars were grouped by root no. 1, 2, 3 (p 19): a molar '
        'row serves any of the six.', 'Table XII (p 24): A +/- 0.45 SA ca. 35%', '85 n(n-1)',
        '85 = 0.85' + MLT + '10' + MLT + '10: teeth of one person (not molars) correlate r 0.80-0.90 (p 11).',
        "Best from several teeth: leave out 'upper first premolars and all the molars' (p 19). One value per root.",
        "B&R's figures run to 14 mm. Above 110 yr no age is given.", '168 teeth of 24 people aged 26-85 (p 9)',
        '19 of 24 within +/- SA (p', 'the four oldest (75.8-85.9) came out 17.5-20.4 yr too young (Table XIII, p 25)'],
    9: ['NORMAL ERRORS', 'not counts', "Lamendin's mean error, 10 yr, is an 'average difference' (p 1377); whether "
        "signs were ignored is not stated.", '10' + MLT + 'sqrt(pi/2) = 12.53, exact only for normal errors (FDAES '
        'uses 12.5)', '1.28 to 1.32, against 1.25 for normal',
        'AGE MIMICRY', "'age estimates tend to mimic the structure of the known-age reference sample' (Iscan & Steyn "
        "2013, p 88)", "The direction: 'the younger individuals were overestimated in age while the older individuals "
        "were underestimated' (P-U, p 109).", '24.8 yr at 26-29, 6.3 at 60-69 (Lamendin Table 1, unsigned)',
        '13.2 at 25-29, 32.6 at 90-99 (P-U Table 2, p 109)', "Bang & Ramm's four oldest 17.5-20.4 yr too young (p 25)",
        'THE POOL assumes independent', MLT.strip() + ' 1.25',
        "FDAES's own choices, from no paper", 'THE PERSON must resemble the reference samples', "Bang & Ramm's 265"],
    10: ['TEACHING & DEMONSTRATION AID. Not validated forensic or casework software. Do not rely on its results for '
         'legal purposes. Check every number against the original papers.', 'the P-U and Bang & Ramm tables were '
         'checked by two independent readings, the others against the page images.', 'PC test harness only'],
}
for n, fl in FACTS.items():
    # a fact may run across lines: the topic's lines joined with single spaces (a hyphen at a line end kept)
    txt = re.sub(r'\s+', ' ', HX[n])
    miss = [f for f in fl if f not in txt]
    check('H topic %d (%s): the facts with their pages: %s' % (n, HMENU[n - 1], '; '.join(fl)), not miss, repr(miss))
check('H no help topic places Bang & Ramm\'s subjects in Norway (the paper does not say where they came from; the '
      'authors were in Bergen)', 'Bergen, Norway:' not in ' '.join(HX.values()) and
      "Bergen's 265" not in ' '.join(HX.values()))
check('H the P-U RMSEs on the help page are the CSV\'s, rounded (8.115402 -> 8.12, 10.41143 -> 10.41, 11.89553 -> 11.90, '
      '9.576177 -> 9.58)', ['%.2f' % PURM[g] for g in (1, 2, 3, 4)] == ['8.12', '10.41', '11.90', '9.58'])
check('H the P-U ratios on the Assumptions page (1.28 to 1.32) are the CSV\'s RMSE / Table 7 mean absolute difference',
      sorted('%.2f' % (float(PURM[g]) / float(PU[g - 1]['table7_new_mean_abs_diff'])) for g in (1, 2, 3, 4))[0] == '1.28'
      and sorted('%.2f' % (float(PURM[g]) / float(PU[g - 1]['table7_new_mean_abs_diff'])) for g in (1, 2, 3, 4))[-1] == '1.32')
check('H "What FDAES is not" opens with the disclaimer (its first six lines)',
      HX[10].startswith('TEACHING & DEMONSTRATION AID. Not validated forensic or casework software. Do not rely on its '
                        'results for legal purposes. Check every number against the original papers.'))
# the help menu: cancel returns to the main menu; the tenth item is there
h = run(NEW, [5, 0, 7], [K], tag='H help menu cancel')
check('H the help menu: 10 topics; Cancel returns to the main menu', [c.title for c in h.chooses] ==
      ['FDAES  (1 of 2)', 'How to use / assumptions', 'FDAES  (1 of 2)'] and len(h.chooses[1].items) == 10)
NPG = {n: (len(help_items(n)) + 12) // 13 for n in range(1, 11)}
h = run(NEW, [5, 2, 9, 10, 0, 7], [K] * (NPG[2] + NPG[9] + NPG[10]) + [K], tag='H three topics in a row')
check('H three topics in a row (Willems, Assumptions, What FDAES is not; %d, %d and %d pages), each back to the help '
      'menu' % (NPG[2], NPG[9], NPG[10]),
      [title(p) for p in h.pages if title(p) in HTOP] == ['HELP: WILLEMS 2001'] * NPG[2] + ['ASSUMPTIONS'] * NPG[9] +
      ['WHAT FDAES IS NOT'] * NPG[10], repr([title(p) for p in h.pages]))
# M3's own menu item
npg4 = (len(help_items(4)) + 12) // 13
h = run(NEW, [3, 4, 7], [K] * npg4 + [K], tag='H M3 help item')
check('H M3\'s jaw menu: item 4 "How to read M3 (help)" opens the M3 topic, then the main menu',
      h.chooses[1].items[-1] == 'How to read M3 (help)' and len(pages_titled(h, 'HELP: M3 (MINCER 1993)')) == npg4 and
      [c.title for c in h.chooses] == ['FDAES  (1 of 2)', 'M3  Which jaw?', 'FDAES  (1 of 2)'])
# the pointers on each method's first page
h, exp = session([7] * 7, 1, tag='H odontogram pointer')
od = pages_titled(h, ODO)[0]
check('H the odontogram\'s help line: "Tap a tooth, then its stage. Help: main menu." (was "... (A-H).")',
      any(t.text == 'Tap a tooth, then its stage. Help: main menu.' and t.y == 97 for t in od.texts))
for tl, prog_tag in (('LAMENDIN 1992 / PRINCE-UBELAKER 2002', 'L'), ('JOHANSON (1971)  Histological', 'J'),
                     ('BANG & RAMM (1970)', 'R')):
    chs = {'L': [4, 7], 'J': [6, 1, 7], 'R': [6, 2, 0, 7]}[prog_tag]
    inp = {'L': [CANCEL], 'J': [CANCEL], 'R': []}[prog_tag]
    h = run(NEW, chs, [K, K], inp, tag='H pointer %s' % prog_tag)
    first_ = [p for p in h.pages if title(p) == tl]
    check('H "%s" first page carries "Help: main menu > How to use."' % tl,
          first_ and 'Help: main menu > How to use.' in page_lines(first_[0]))
# the disclaimer
op = page_lines(h.pages[0])
check('H the opening page, before the main menu, once per run: what FDAES is and is not; "any key or tap = main menu"',
      title(h.pages[0]) == OPEN_T and op == ['Forensic Dental Age Estimation', 'System (Roger Metcalf, 2026)',
                                                   'TEACHING & DEMONSTRATION AID', 'Not validated forensic or casework',
                                                   'software. Do not rely on it for', 'legal purposes. Check every number',
                                                   'against the original papers.', 'Start with Setup (sex, ancestry).',
                                                   'Instructions and assumptions:', "'How to use / assumptions' on the",
                                                   'main menu.'] and
      [t.text for t in h.pages[0].texts if t.y == 224] == ['any key or tap = main menu'] and
      sum(1 for p in h.pages if title(p) == OPEN_T) == 1, repr(op))
check('H every v3.9a run so far opened on that page, once (%d runs)' % len(ALLRUNS),
      all(r.pages and title(r.pages[0]) == OPEN_T and sum(1 for p in r.pages if title(p) == OPEN_T) == 1
          for r in ALLRUNS))
ab = run(NEW, [6, 7, 7], [K] * NABOUT, tag='H About')
abp = page_lines(pages_titled(ab, 'ABOUT FDAES v3.9b')[0])
check('H About\'s first page opens with the disclaimer', abp[:6] == ['TEACHING & DEMONSTRATION AID',
                                                                      'Not validated forensic or casework',
                                                                      'software. Do not rely on its',
                                                                      'results for legal purposes. Check',
                                                                      'every number against the original', 'papers.'],
      repr(abp))
check('H About ends on "v3.9 CHANGES" (24 lines, two pages) before the two-ways page, which says PC harness only',
      [title(p) for p in ab.pages].count('v3.9 CHANGES') == 2 and
      'PC HARNESS ONLY; NOT ON HARDWARE.' in [l for p in pages_titled(ab, 'v3.9 CHANGES') for l in page_lines(p)])
ex = page_lines(pages_titled(ab, 'FDAES session ended')[0])
check('H the exit page: (v3.9a) "ABFO workshop (2011): a method\'s / data should have had review, / independent '
      'testing and error / estimation." (v3.9: "ABFO 2011 (not checked ..."), and it ends "FDAES is a teaching aid: '
      'do not / rely on it for legal purposes."',
      ex[-2:] == ['FDAES is a teaching aid: do not', 'rely on it for legal purposes.'] and
      ex[3:7] == ["ABFO workshop (2011): a method's", 'data should have had review,', 'independent testing and error',
                  'estimation.'] and not any('not checked' in l for l in ex), repr(ex))
check('H the RETURN line Home keeps carries "(teaching aid; not for legal use)" (second review): with no estimate '
      '"FDAES (teaching aid; not for legal use): no estimate"',
      ab.result == 'FDAES (teaching aid; not for legal use): no estimate', repr(ab.result))
hp_ = [r for r in ALLRUNS if pages_titled(r, 'BAYESIAN POSTERIOR')]
check('H ... and after a posterior "FDAES (teaching aid; not for legal use): age ... P(age >= 18) ...%%" (%d runs)'
      % len(hp_), hp_ and all(r.result.startswith('FDAES (teaching aid; not for legal use): age ') and
                              '], P(age >= 18)' in r.result for r in hp_), repr([r.result for r in hp_][:3]))
reps = [r for r in ALLRUNS if pages_titled(r, 'REPORT TEMPLATE')]
check('H the report template\'s first two lines are the fleet\'s disclaimer, "Teaching & demonstration aid; / not for '
      'legal use.", in every run that shows it (%d); with Lamendin pooled the last two lines too; no Saunders / '
      'Cattell citation (second review)' % len(reps),
      reps and all(page_lines(pages_titled(r, 'REPORT TEMPLATE')[0])[:2] == ['Teaching & demonstration aid;',
                                                                              'not for legal use.'] and
                   (len(pages_titled(r, 'REPORT TEMPLATE')) == 1 or
                    page_lines(pages_titled(r, 'REPORT TEMPLATE')[-1])[-2:] == ['Teaching & demonstration aid;',
                                                                               'not for legal use.']) and
                   not any('Saunders' in l or 'Cattell' in l for p in pages_titled(r, 'REPORT TEMPLATE')
                           for l in page_lines(p))
                   for r in reps))
hdr = re.sub(r'\s+', ' ', ' '.join(l[2:].strip() for l in SRC.split('\n')[:400] if l.startswith('//')))
check('H the header carries the fleet\'s standard disclaimer line verbatim, then FDAES\'s own',
      'DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on '
      'its results for legal purposes.' in hdr and 'DISCLAIMER: FDAES is a teaching and demonstration aid. It is not '
      'validated forensic or casework software; do not rely on its results for legal purposes. Check every number '
      'against the original papers.' in hdr and hdr.index('DISCLAIMER: a teaching') < hdr.index('DISCLAIMER: FDAES'))
# the About pages the second review marked
gus = [l for p in pages_titled(ab, 'WHY GUSTAFSON') for l in page_lines(p)]
check('H About, "WHY GUSTAFSON 1950 IS EXCLUDED" (v3.9a): from Gustafson\'s own paper, "+/-3.63 yr (p 51)" (v3.8a: '
      '"Claimed SE: +/-3.6 yr"; v3.9: quoted from Lamendin p 1378), then Maples & Rice, Lamendin, Lucy; no "Not '
      'checked" block (Part V has every line)',
      gus[:3] == ['Gustafson (1950): 41 teeth; six', '  changes scored 0-3 and summed',
                  '  (pp 47-49); error +/-3.63 yr (p 51)'] and
      not any('Not checked' in l or 'Claimed SE' in l or 'mean deviation' in l or 'estimated, not real' in l
              for l in gus) and len(gus) == 18, repr(gus))   # v3.9b: 18 lines, no blank; Aykroyd
hist = [l for p in pages_titled(ab, 'A SHORT HISTORY') for l in page_lines(p)]
check('H About, "A SHORT HISTORY" (v3.9a; v3.9: "HISTORICAL WARNINGS IGNORED"): opens with Saunders 1837 as his '
      'pamphlet says; v3.8a\'s "Field chose Gustafson n=41 instead" and v3.9\'s "Not checked" are gone',
      hist[0] == 'Saunders (1837), to Parliament:' and len(hist) == 15 and
      not any('Field chose' in l or 'Gustafson n=41 instead' in l or 'Not checked' in l for l in hist), repr(hist))
bfw = [l for p in pages_titled(ab, 'BAYESIAN FRAMEWORK') for l in page_lines(p)]
check('H About, "BAYESIAN FRAMEWORK" (v3.9a): "ABFO guidelines (DRM 2017): give / each method\'s age with a 95% (2 SD) '
      '/ interval, and for age of majority a / probability statement." (v3.9: "ABFO 2011 (not checked ...")',
      bfw[-4:] == ['ABFO guidelines (DRM 2017): give', "each method's age with a 95% (2 SD)",
                   'interval, and for age of majority a', 'probability statement.'] and
      not any('not checked' in l for l in bfw), repr(bfw[-4:]))
check('H About\'s v3.6 page says "+/- 2 SD" (was "+/- 2 SE")', any('Forest: each method +/- 2 SD, the' == l
                                                                   for p in ab.pages for l in page_lines(p)))
lamv = [l for p in pages_titled(ab, 'v3.9 CHANGES') for l in page_lines(p)]
check('H About\'s v3.9 page shows Lamendin\'s spread from fdLamSD: "Lamendin\'s SD 12.5 (D4; his mean error 10 x '
      'sqrt(pi/2) = 12.53)."', "  Lamendin's SD 12.5 (D4; his mean" in lamv, repr(lamv))
# ===================================================================================== Part RG
print('RG. The fleet review\'s check_FDAES.py, run on v3.8a and on v3.9 (a copy with its SRC line pointed at each)')


def run_review(path):
    txt = open(REVIEW_CHECK, encoding='utf-8').read()
    old = "SRC = '/home/claude/work/review/fleet/FDAES_v3.8a.txt'"
    assert old in txt
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'check_FDAES_on.py')
    open(p, 'w', encoding='utf-8').write(txt.replace(old, 'SRC = %r' % path, 1))
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, timeout=900)
    out = r.stdout
    fails = sorted(set(l[5:].split('   ')[0] for l in out.split('\n') if l.startswith('FAIL ')))
    notes = [l[5:] for l in out.split('\n') if l.startswith('NOTE ')]
    m = re.search(r'(\d+) checks passed, (\d+) failed; (\d+) notes', out)
    return r.returncode, fails, notes, m.groups() if m else None


rc_o, f_o, n_o, s_o = run_review(OLD)
rc_n, f_n, n_n, s_n = run_review(NEW)
print('   v3.8a: %s passed, %s failed, %s notes; v3.9: %s passed, %s failed, %s notes' % (s_o + s_n))
check('RG v3.8a passes all of the review\'s checks (they document v3.8a as it was)', rc_o == 0 and not f_o, repr(f_o))
FLIP = {
    'F1 Lamendin coefficients as published (p 1375: A = 0.18 P + 0.42 T + 25.53)':
        'it looks for v3.8a\'s "ae := 0.18*lP + 0.42*lT + licv" and the intercept list {27.00, 25.53, 29.69, 27.21, 26.50} '
        '(D2: P-U\'s own equations replace the unsourced intercepts; v3.9 computes "laL := 0.18*lP + 0.42*lT + 25.53")',
    'I6 both "P(age>=18)" and "P(age >= 18)" spellings are in use':
        'C-F9: v3.9 spells it "P(age >= 18)" everywhere',
    'J2 the harness flags the scientific display':
        'C-F8 / C-F9: a typed threshold of 0.05 now shows "P(age >= 0.1)", never 5.0E-2',
}
for f in FLIP:
    check('RG on v3.9 the review\'s "%s" fails BY DESIGN: %s' % (f.split(' ')[0], FLIP[f]), f in f_n, repr(f_n))
check('RG on v3.9 no other review check fails (%d of %d pass)' % (int(s_n[0]), int(s_n[0]) + int(s_n[1])),
      sorted(f_n) == sorted(FLIP), repr(f_n))
src9 = SRC
check('RG F1\'s substance holds on v3.9: Lamendin as published, 0.18 P + 0.42 T + 25.53 (p 1375)',
      'laL := 0.18*lP + 0.42*lT + 25.53;' in src9)
j1o = [n for n in n_o if n.startswith('J1 ')]
j1n = [n for n in n_n if n.startswith('J1 ')]
lo = int(re.search(r'drew (\d+) LINE_P', j1o[0]).group(1)) if j1o else -1
ln = int(re.search(r'drew (\d+) LINE_P', j1n[0]).group(1)) if j1n else -1
print('   the review\'s J1 (a typed threshold of 1E6): v3.8a drew %d LINE_P, v3.9 %d' % (lo, ln))
check('RG the review\'s J1 on v3.9: a typed 1E6 draws no more lines than an ordinary threshold (%d, v3.8a %d)' % (ln, lo),
      0 < ln < 2000 and lo > 50000)
gone = sorted(set(n.split(' ')[0] for n in n_o) - set(n.split(' ')[0] for n in n_n))
print('   review NOTEs on v3.8a that v3.9 no longer earns: %s' % ', '.join(gone))
# ===================================================================================== Part S
print('S. Every other module, v3.9 against v3.8a')
# The screens v3.9 changes on purpose are left out of the signature and checked in their own parts: the
# opening page (H), Setup (S below), Johanson's two pages (J), the report (P), Lamendin / P-U (L), Bang &
# Ramm (R), the exit page (H).  Every verdict band is taken out of the screen and compared on its own (the P it prints must be
# v3.8a's, the verdict v3.9's rule); the footer under a band is read at v3.8a's row.  v3.8a's texts are read
# through v3.9's other rewrites (rw39).
EXCL = ('Setup saved', 'FDAES v3.9b', 'JOHANSON (1971) result', 'JOHANSON (1971)  Histological', 'REPORT TEMPLATE',
        'FDAES session ended')           # the exit page: two teaching-aid lines added (Part H)
OLDBAND = re.compile(r'^(likely >= 18|uncertain|likely < 18)  P\(age >= 18\)(.*)%$')
RWS9 = {}


def rw39(t):
    """v3.8a's text as v3.9 writes it, for the displays v3.9 rewrites outside the excluded screens"""
    if t is None:
        return t
    t0 = t
    t = t.replace('M3 Threshold  P(age>=18)', 'M3 Threshold  P(age >= 18)')
    t = re.sub(r'^mu=(\S+)  sd=(\S+)$', r'mu = \1  sd = \2', t)
    t = t.replace('1 tooth   SE = +/- 8.00 yr', '1 tooth   6.0 (his Table 8)')   # v3.9a: 6.0
    t = t.replace('2+ teeth  SE = +/- 5.16 yr', '2+ teeth  5.16 (Johanson SD)')
    t = t.replace('Tap a tooth, then tap its stage (A-H).', 'Tap a tooth, then its stage. Help: main menu.')
    t = t.replace('the methods share P and T: no gain allowed', 'the methods share root transparency: no gain')
    # v3.9, second review: SE -> SD where an SD is meant; the Setup's sex item; the posterior's floor line
    t = t.replace('FOREST PLOT  estimate +/- 2 SE', 'FOREST PLOT  estimate +/- 2 SD')
    t = t.replace(' best single SE ', ' best single SD ').replace('pooled SD = its SE x 1.25', 'pooled SD = its SD x 1.25')
    t = t.replace('Unknown  [conservative SE]', 'Unknown')
    # v3.9a: Harris et al. 2010's table and page, from the published book (fdM3Hist page 1)
    t = t.replace('et al., Table 12), and it lives on in', 'et al., Table 13.12, p 289); it lives')
    t = t.replace('copies without the erratum page.', 'on in copies lacking the erratum.')
    t = t.replace('SD floored at best single SE', 'FLOORLINE')
    t = t.replace('mean error +0.0 yr, s.d. 0.9 yr', 'mean diff. (signed) +0.0, s.d. 0.9 yr')
    t = t.replace('mean error +0.2 yr, s.d. 1.3 yr', 'mean diff. (signed) +0.2, s.d. 1.3 yr')
    t = t.replace("Paper's test (p 894): s.d. 0.9 boys,", 'Test (p 894): s.d. 0.9 boys, 1.3')
    t = t.replace('1.3 girls; mean error +0.0, +0.2.', 'girls; mean diff. (signed) 0.0, +0.2')
    if t.startswith('FDAES: '):
        t = 'FDAES (teaching aid; not for legal use): ' + t[len('FDAES: '):]
        t = t.replace('], P(age>=18)', '], P(age >= 18)')
    if t != t0:
        RWS9[t0] = t
    return t


def num(a):
    return int(a) if isinstance(a, float) and a == int(a) else a


# v3.9, second review: the posterior's floor line says what happened (checked in Part P), and the empty pool's
# message names every poolable method (checked below)
FLOORL = ('SD raised to best single SD (floor)', 'One method: no floor applies', 'Floor not needed (SD >= best SD)')
EMPTY38 = ['No estimates stored yet.', 'Run Willems, Lamendin, Johanson', 'or Bang & Ramm, then answer Yes',
           'to Add to Bayesian pool?']
EMPTY39 = ['No estimates stored yet.', 'Poolable: Willems, Liversidge,', 'Lamendin, P-U, Johanson, Bang &',
           'Ramm. Run one, then choose it at', "the 'Add to pool' question."]


def norm_sig(h, new):
    bands, pages = [], []
    for sc in h.screens:
        tt = title(sc)
        if tt in EXCL:
            continue
        texts = [(t.text, t.x, t.y, t.font, t.hex, t.width) for t in sc.texts]
        shapes = [(x.cmd, [num(a) for a in x.args]) for x in sc.shapes]
        if new:
            b = band_texts(sc)
            if b is not None:
                bands.append((b[0].text if b[0] else None, b[1].text if b[1] else None, b[0].hex if b[0] else None,
                              b[1].hex if b[1] else None))
                texts = [t for t in texts if not (t[1] == 10 and t[2] in (200, 214))]
                shapes = [x for x in shapes if not (x[0] == 'RECT_P' and x[1][:4] == [4, 199, 315, 226])]
                texts = [(t[0], t[1], 224 if (t[2] == 228 and t[1] == 6 and t[3] == 1) else t[2]) + t[3:] for t in texts]
        else:
            ob = [t for t in texts if t[1] == 10 and t[2] == 204 and t[3] == 2 and OLDBAND.match(t[0])]
            if ob:
                bands.append(ob[0][0])
                texts = [t for t in texts if t not in ob]
                shapes = [x for x in shapes if not (x[0] == 'RECT_P' and x[1][:4] == [4, 201, 315, 219])]
            texts = [(rw39(t[0]),) + t[1:] for t in texts]
        if new:
            texts = [(('FLOORLINE',) if t[0] in FLOORL else (t[0],)) + t[1:] for t in texts]
        pages.append((tt if new else rw39(tt), texts, shapes, sc.menu, sc.reason))
    chs = [(c.title, c.items if new else [rw39(i) for i in c.items] + (['How to read M3 (help)'] if c.title == 'M3  Which jaw?' else []),
            c.index) for c in h.chooses if not c.title.startswith('FDAES  (') and
           c.title not in ('Ancestral Population', 'Ancestry (Prince-Ubelaker)')]
    inps = [(i.title, i.labels, i.before, i.after, i.accepted) for i in h.inputs]
    msgs = [m.lines for m in h.msgboxes]
    if not new:
        msgs = [EMPTY39 if m == EMPTY38 else m for m in msgs]
    res = h.result if new else rw39(h.result)
    return (pages, chs, inps, msgs, res), bands


NUMRE = re.compile(r'-?\d+\.\d+')


def tie_eq(x, y):
    """two display strings equal but for numbers one unit apart in their last shown decimal: v3.9 rounds before
    STRING (fdF1 / fdF2, half up, as the Prime does), where v3.8a's STRING(x, 2, d) met the harness's binary rounding
    at an exact decimal tie (e.g. SD 1.625: v3.8a "1.62" in the harness, "1.63" on the Prime and in v3.9)"""
    if NUMRE.sub('#', x) != NUMRE.sub('#', y):
        return False
    for u, v in zip(NUMRE.findall(x), NUMRE.findall(y)):
        if u != v:
            d = len(u.split('.')[1])
            if len(v.split('.')[1]) != d or abs(Decimal(u) - Decimal(v)) != Decimal(1).scaleb(-d):
                return False
            TIES.append('"%s" (v3.8a in the harness: "%s")' % (x, y))
    return True


def tol_eq(x, y):
    if isinstance(x, str) and isinstance(y, str):
        return x == y or tie_eq(x, y)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return len(x) == len(y) and all(tol_eq(u, v) for u, v in zip(x, y))
    return x == y


NS, NB, BT = [0], [0], {}


def same(tag, och, oev, oinp, nch, nev, ninp):
    NS[0] += 1
    hn = run(NEW, nch, nev, ninp, tag='S ' + tag)
    ho = run(OLD, och, oev, oinp, tag='S old ' + tag)
    (a, ab), (b, bb) = norm_sig(hn, True), norm_sig(ho, False)
    names = ['screens', 'dialogs', 'inputs', 'MSGBOXes', 'RETURN']
    bad = [names[i] for i in range(5) if a[i] != b[i] and not tol_eq(a[i], b[i])]
    detail = ''
    if 'screens' in bad:
        for x, y in itertools.zip_longest(a[0], b[0]):
            if x != y:
                detail = 'first differing screen: %r\n   vs %r' % (x and (x[0], x[1][:6]), y and (y[0], y[1][:6]))
                break
    check('S identical to v3.8a after the known rewrites: ' + tag, not bad, '%s %s %r' % (bad, detail, (hn.result, ho.result)))
    # the bands, one by one: the same P as v3.8a, v3.9's verdict and colour, the cut-points
    okb = len(ab) == len(bb)
    for nb, ob in zip(ab, bb):
        m_ = OLDBAND.match(ob)
        rest = m_.group(2)                        # ' = 97.1' or ' < 0.1'
        pr = rest.strip()
        pr = pr[2:] if pr.startswith('= ') else pr
        want2 = 'P(age >= 18)' + rest + '%' + CUT
        okb = okb and nb[1] == want2 and nb[0] == verdict(pr) and nb[2] == COLV[nb[0]] and nb[3] == COLV[nb[0]]
        BT[(m_.group(1), nb[0])] = BT.get((m_.group(1), nb[0]), 0) + 1
        NB[0] += 1
    check('S every band (%d) prints v3.8a\'s P with v3.9\'s verdict, colour and cut-points: ' % len(ab) + tag, okb,
          repr(list(zip(ab, bb))[:3]))
    return hn, ho


# M3: every sex, jaw and grade (M3 keeps the authors' zones: no fdBand at all)
for sexc in (1, 2, 3):
    for jaw in (1, 2):
        for g in range(2, 7):
            same('M3 sex %d jaw %d grade %d' % (sexc, jaw, g), [1, sexc, 1, 3, jaw, g, 6], [K] * 4, (),
                 [1, sexc, 1, 3, jaw, g, 7], [K] * 4, ())
        same('M3 sex %d jaw %d not visible' % (sexc, jaw), [1, sexc, 1, 3, jaw, 1, 6], [K] * 2, (),
             [1, sexc, 1, 3, jaw, 1, 7], [K] * 2, ())
        same('M3 sex %d jaw %d grade cancelled' % (sexc, jaw), [1, sexc, 1, 3, jaw, 0, 6], [K] * 2, (),
             [1, sexc, 1, 3, jaw, 0, 7], [K] * 2, ())
same('M3 misprint page, then cancel', [3, 3, 6], [K] * 3, (), [3, 3, 7], [K] * 3, ())
same('M3 jaw cancelled', [3, 0, 6], [K], (), [3, 0, 7], [K], ())
# Johanson: v3.9's result is two pages (one more key); its pages are Part J's
JS = [1, 1.5, .5, .5, 0, 2.5]
same('Johanson 1 tooth, pooled', [5, 1, 1, 1, 6], [K, K, K], [JS], [6, 1, 1, 1, 7], [K, K, K, K], [JS])
same('Johanson 2+ teeth, not pooled', [5, 1, 2, 2, 6], [K, K, K], [JS], [6, 1, 2, 2, 7], [K, K, K, K], [JS])
same('Johanson bad score', [5, 1, 6], [K, K], [[1, 1.3, .5, .5, 0, 2.5]], [6, 1, 7], [K, K], [[1, 1.3, .5, .5, 0, 2.5]])
same('Johanson teeth cancelled', [5, 1, 0, 6], [K, K], [JS], [6, 1, 0, 7], [K, K], [JS])
same('Johanson cancelled', [5, 1, 6], [K, K], [CANCEL], [6, 1, 7], [K, K], [CANCEL])
same('Johanson out of range (all 0: 11.02 yr)', [5, 1, 1, 6], [K, K], [[0] * 6], [6, 1, 1, 7], [K, K], [[0] * 6])
hn_e, ho_e = same('Bayesian with nothing stored', [5, 3, 6], [K], (), [6, 3, 7], [K], ())
check('S the empty pool\'s message (second review) names every poolable method and the question to answer: %r'
      % hn_e.msgboxes[0].lines, hn_e.msgboxes[0].lines == EMPTY39 and ho_e.msgboxes[0].lines == EMPTY38 and
      not hn_e.msgboxes[0].over_five)
same('Threshold with no posterior', [5, 4, 6], [K], (), [6, 4, 7], [K], ())
same('Clear yes / no', [5, 5, 1, 5, 5, 2, 6], [K], (), [6, 5, 1, 6, 5, 2, 7], [K], ())
# a whole session through the pool: Willems (a boy, all seven at G) and Johanson pooled, Bayesian, the
# posterior's keys and Enter menu (a typed age, Left / Right, the table, the forest), the report, Exit
evW = [K]
for i in range(1, 8):
    evW += [tooth(i), stage(7)]
WW, wpw, _w = exp_willems_page([7] * 7, 1)
LL, lpl_, _l = exp_liv_page([7] * 7, 1)
evW += [soft(6)] + [K] * (npages(WW, wpw) + npages(LL, lpl_))
tail = [K, ('key', 'Left'), ('key', 'Right'), ('key', 'Right'), ('key', 'Enter'), soft(3), soft(1), K, soft(2), K,
        ('key', 'Esc'), K, K]
same('a pool of Willems and Johanson; the posterior\'s keys, typed ages, table, forest; the report; Exit',
     [1, 2, 1, 2, 1, 5, 1, 2, 1, 5, 3, 3, 6], evW + [K, K] + tail, [JS, [21], [19]],
     [1, 2, 1, 2, 1, 6, 1, 2, 1, 6, 3, 3, 7], evW + [K, K, K] + tail, [JS, [21], [19]])
same('a pool of Willems alone (a girl, all G): the band at P < 0.1%; Exit',
     [1, 3, 1, 2, 1, 5, 3, 6], [K] + [e for i in range(1, 8) for e in (tooth(i), stage(7))] + [soft(6)] +
     [K] * (npages(*exp_willems_page([7] * 7, 2)[:2]) + npages(*exp_liv_page([7] * 7, 2)[:2])) + [K, soft(6), K, K], (),
     [1, 3, 1, 2, 1, 6, 3, 7], [K] + [e for i in range(1, 8) for e in (tooth(i), stage(7))] + [soft(6)] +
     [K] * (npages(*exp_willems_page([7] * 7, 2)[:2]) + npages(*exp_liv_page([7] * 7, 2)[:2])) + [K, soft(6), K, K], ())
print('   %d sessions compared, each run on v3.9 and on v3.8a; %d bands compared one by one; band verdicts, '
      'v3.8a -> v3.9: %s' % (NS[0], NB[0], ', '.join('%s -> %s: %d' % (a, b, n) for (a, b), n in sorted(BT.items()))))
print('   v3.8a texts read through v3.9\'s rewrites: %s' % sorted(RWS9.items()))
# the main menu, the Setup menus and page (left out above)
hn = run(NEW, [1, 3, 4, 7], [K, K], tag='S setup')
ho = run(OLD, [1, 3, 5, 6], [K, K], tag='S old setup')
mm = [c for c in hn.chooses if c.title == 'FDAES  (1 of 2)'][0]
check('S the main menu: v3.8a\'s items with "P(age >= 18)" spaced and "How to use / assumptions" as item 5',
      mm.items == ['Setup: sex & ancestry', 'Willems 2001  subadult', 'M3 Threshold  P(age >= 18)',
                   'Lamendin / Prince-Ubelaker', 'How to use / assumptions', 'More options...', 'Exit'] and
      [c for c in ho.chooses if c.title == 'FDAES  (1 of 2)'][0].items ==
      ['Setup: sex & ancestry', 'Willems 2001  subadult', 'M3 Threshold  P(age>=18)', 'Lamendin / Prince-Ubelaker',
       'More options...', 'Exit'], repr(mm.items))
anc_ = [c for c in hn.chooses if c.title.startswith('Ancestry')][0]
check('S (D2) the ancestry menu: Unknown, White, Black, Other (P-U\'s terms; v3.8a: European, African American, '
      'Asian, Hispanic with intercepts in neither paper)', anc_.items == ['Unknown', 'White', 'Black', 'Other']
      and anc_.title == 'Ancestry (Prince-Ubelaker)', repr(anc_))
sp = page_lines(pages_titled(hn, 'Setup saved')[0])
check('S the Setup page (female, Other): sex and ancestry, then (second review) what Unknown sex and Unknown / Other '
      'ancestry each do', sp ==
      ['Sex:      Female', 'Ancestry: Other', 'Active estimates: 0', 'Sex Unknown: Willems mixes boys and',
       '  girls 50:50; Liversidge uses the', '  combined columns; M3 shows both', '  sexes; no P-U equation.',
       'Ancestry Unknown or Other: no P-U', '  equation; Lamendin 1992 alone.', 'Lamendin, Johanson, Bang & Ramm:',
       '  neither sex nor ancestry.'], repr(sp))
sxm = [c for c in hn.chooses if c.title == 'Biological Sex'][0]
check('S the Setup sex menu: "Unknown", "Male", "Female" (second review: v3.8a\'s "Unknown  [conservative SE]" '
      'named an SE that no module uses)', sxm.items == ['Unknown', 'Male', 'Female'] and
      [c for c in ho.chooses if c.title == 'Biological Sex'][0].items[0] == 'Unknown  [conservative SE]', repr(sxm))
# About: v3.8a's pages in order, with the ABOUT page first and v3.9's pages after v3.8's
hn = run(NEW, [6, 7, 7], [K] * NABOUT, tag='About')
ho = run(OLD, [5, 7, 6], [K] * 15, tag='About old')
dedup = lambda xs: [x for i, x in enumerate(xs) if i == 0 or x != xs[i - 1]]
# (the opening page: Part H; the pages, each title once -- v3.9's Gustafson page runs to two pages)
# (v3.9a: "HISTORICAL WARNINGS IGNORED" is now "A SHORT HISTORY", in the same place)
NT9A = {'HISTORICAL WARNINGS IGNORED': 'A SHORT HISTORY'}
ta, tb_ = dedup([title(p) for p in hn.pages if title(p) != OPEN_T]), dedup([title(p) for p in ho.pages])
check('S About: "ABOUT FDAES v3.9a" first, then v3.8a\'s pages in order ("A SHORT HISTORY" where "HISTORICAL WARNINGS '
      'IGNORED" was), "v3.9 CHANGES" after the v3.8 page',
      ta[0] == 'ABOUT FDAES v3.9b' and [t for t in ta[1:] if t != 'v3.9 CHANGES'] == [NT9A.get(t, t) for t in tb_]
      and ta.count('v3.9 CHANGES') == 1
      and ta.index('v3.9 CHANGES') == ta.index('v3.8 WILLEMS AND LIVERSIDGE') + 1, repr(ta))
dif = {}
LN = lambda h_, t_: [l for p in h_.pages if title(p) == t_ for l in page_lines(p)]
for t_ in [t for t in tb_ if t != 'FDAES session ended']:
    la, lb = LN(hn, NT9A.get(t_, t_)), LN(ho, t_)
    if la != lb:
        dif[t_] = ([x for x in la if x not in lb], [x for x in lb if x not in la])
check('S About: only "WHY GUSTAFSON" (C-F3; second review; v3.9a), "HISTORICAL WARNINGS" (second review; v3.9a "A '
      'SHORT HISTORY"), "BAYESIAN '
      'FRAMEWORK" (the x1.25 methods; the lower tail; ABFO, v3.9a), "v3.6 NEW SCREENS", "v3.6 NOTES" and "v3.7 M3" '
      '(no 0.83 / 0.58 in the present tense; +/- 2 SD) and (v3.9a) "A MISPRINT AND ITS ERRATUM" (Harris\'s table '
      'and page) differ from v3.8a',
      sorted(dif) == sorted(['WHY GUSTAFSON 1950 IS EXCLUDED', 'HISTORICAL WARNINGS IGNORED', 'BAYESIAN FRAMEWORK',
                             'v3.6 NEW SCREENS', 'v3.6 NOTES', 'v3.7 M3: THE CORRECTED TABLE',
                             'A MISPRINT AND ITS ERRATUM']), repr(sorted(dif)))
check('S About, the misprint page (v3.9a): v3.8a\'s lines but the two on Harris et al. 2010 ("Table 13.12, p 289"), '
      'still 13 lines on one page', [rw39(l) for l in LN(ho, 'A MISPRINT AND ITS ERRATUM')] ==
      LN(hn, 'A MISPRINT AND ITS ERRATUM') and len(pages_titled(hn, 'A MISPRINT AND ITS ERRATUM')) == 1,
      repr(dif.get('A MISPRINT AND ITS ERRATUM')))
gus = LN(hn, 'WHY GUSTAFSON 1950 IS EXCLUDED')
check('S About, Gustafson (C-F3; v3.9a\'s wording): "Lamendin 1992 (p 1377), 39 people aged 42-79: mean error 14.2 '
      '+/- 3.4 yr (his own: 8.9 +/- 2.2)."; no "SE on control", no "39-tooth"',
      gus[10:13] == ['Lamendin 1992 (p 1377), 39 people', '  aged 42-79: mean error 14.2 +/-',
                     '  3.4 yr (his own: 8.9 +/- 2.2).']   # v3.9b: one line later (Aykroyd's three lines)
      and not any('SE on control' in l or '39-tooth' in l for l in gus), repr(gus))
bf = [l for p in pages_titled(hn, 'BAYESIAN FRAMEWORK') for l in page_lines(p)]
check('S About, Bayesian framework: the four transparency methods; "P(age >= t): the lower tail NORMALD_CDF(mu, sd, '
      '2mu - t)" (C-F6), not "1-NORMALD_CDF"', 'Lamendin, P-U, Johanson and Bang' in bf and
      '  NORMALD_CDF(mu, sd, 2mu - t),' in bf and not any('1-NORMALD_CDF' in l for l in bf), repr(bf))
v36 = page_lines(pages_titled(hn, 'v3.6 NEW SCREENS')[0]) + page_lines(pages_titled(hn, 'v3.6 NOTES')[0]) + \
    page_lines(pages_titled(hn, 'v3.7 M3')[0])
check('S About, v3.6 / v3.7 pages (C-F6): "uncertain zone 58-83%" and "Verdict cut-points are the M3 module\'s" gone; '
      '"(v3.9: 95% / 5%)", "Verdict cut-points (v3.9): 5% and 95%", "results kept 0.58/0.83 until v3.9."',
      not any('uncertain zone 58-83%' in l or "module's (0.83" in l or 'results keep the' in l for l in v36) and
      '  95% / 5%), P = P(age >= 18).' in v36 and 'Verdict cut-points (v3.9): 5% and' in v36 and
      '  results kept 0.58/0.83 until v3.9.' in v36, repr(v36))
check('S About: same RETURN (the teaching-aid tag apart)', hn.result == rw39(ho.result), repr((hn.result, ho.result)))
# Verify Calculations: pages 5 and 6 are v3.8a's 3 and 4, identical; 1-4 new (Part K)
hv9 = run(NEW, [6, 6, 7], [K] * 7, tag='self-check (S)')
hv8 = run(OLD, [5, 6, 6], [K] * 5, tag='self-check old')
pn, po = pages_titled(hv9, 'ARITHMETIC'), pages_titled(hv8, 'ARITHMETIC')
check('S Verify Calculations: v3.9\'s pages 5 and 6 are v3.8a\'s 3 and 4, line for line; six pages in all',
      len(pn) == 6 and len(po) == 4 and [page_lines(p) for p in pn[4:]] == [page_lines(p) for p in po[2:]])
# ===================================================================================== Part G
print('G. v3.8a -> v3.9a: the routine diff (v3.9 -> v3.9a: Part V)')
HEAD = re.compile(r'^(EXPORT\s+)?([A-Za-z_]\w*)\([^;]*\)\s*$')     # a routine head, not a call
CODE = [strip_comment(l) for l in SRC.split('\n')]


def routines(s):
    out, cur = {'<header>': []}, '<header>'
    for l in s.split('\n'):
        c = strip_comment(l)
        m = HEAD.match(c)
        if m and not c.startswith(' '):
            cur = m.group(2)
            out[cur] = []
        if c.strip():
            out[cur].append(c.rstrip())
    return out


def raw_routines(s):
    """each routine's raw lines, comments included, from its head to its closing END; at column 0"""
    out, cur = {}, None
    for l in s.split('\n'):
        m = HEAD.match(strip_comment(l).rstrip())
        if m and not l.startswith(' '):
            cur = m.group(2)
            out[cur] = []
        if cur:
            out[cur].append(l)
            if l.startswith('END;'):
                cur = None
    return out


def plusminus(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    plus, minus = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ('replace', 'delete'):
            minus += a[i1:i2]
        if op in ('replace', 'insert'):
            plus += b[j1:j2]
    return [x.strip() for x in plus], [x.strip() for x in minus]


A, B = routines(SRCO), routines(SRC)
chg = sorted(k for k in set(A) & set(B) if A[k] != B[k])
added = sorted(set(B) - set(A))
removed = sorted(set(A) - set(B))
print('   changed: %s' % ', '.join(chg))
print('   added:   %s' % ', '.join(added))
print('   removed: %s' % (', '.join(removed) or 'none'))
CHG = ['<header>', 'FDAES', 'fdBand', 'fdForest', 'fdLPage', 'fdM3Hist', 'fdOdonto', 'fdPageV', 'fdPost', 'fdThrTable',
       'fdWEst', 'fdWPage', 'fdWSum']
check('G changed routines (code, comments stripped) = the header\'s LOCALs, FDAES, fdBand (D1), fdPageV (the band\'s '
      'rows), fdWSum / fdWEst / fdWPage / fdOdonto (C-F1), fdLPage (C-F6), fdPost (C-F8, C-F9), fdThrTable (C-F9), '
      'fdForest (P-U\'s colour, the transparency note), and (v3.9a) fdM3Hist (Harris et al.\'s Table 13.12, p 289)',
      chg == CHG, repr(chg))
p_, m_ = plusminus(A['fdM3Hist'], B['fdM3Hist'])
check('G fdM3Hist (v3.9a): only the two Harris lines changed, "et al., Table 13.12, p 289); it lives" / "on in copies '
      'lacking the erratum." (were "et al., Table 12), and it lives on in" / "copies without the erratum page.")',
      p_ == ['"et al., Table 13.12, p 289); it lives",', '"on in copies lacking the erratum.",'] and
      m_ == ['"et al., Table 12), and it lives on in",', '"copies without the erratum page.",'], repr((p_, m_)))
ADD = ['fdBRAge', 'fdBRCmb', 'fdBRTab', 'fdBRrm', 'fdHelp', 'fdHelpMn', 'fdJoh1SD', 'fdLamLbl', 'fdLamSD', 'fdPUAge',
       'fdPUTab', 'fdPUg', 'fdPUnm', 'fdUpEnd', 'fdWCeil']     # v3.9a: fdJoh1SD (Roger's D5)
check('G added routines = fdLamSD, fdLamLbl (D4); fdPUTab, fdPUg, fdPUnm, fdPUAge (D2); fdBRTab, fdBRAge, fdBRCmb, '
      'fdBRrm (D3); fdHelp, fdHelpMn (help); fdUpEnd (interval ends above 110) and fdWCeil (the ceiling rule) from the '
      'second review; fdJoh1SD (v3.9a, D5); none removed', added == ADD and not removed, repr((added, removed)))
RA, RB = raw_routines(SRCO), raw_routines(SRC)
same_raw = sorted(k for k in set(RA) & set(RB) if k not in CHG)
check('G every other routine (%d) is byte-identical to v3.8a, comments included' % len(same_raw),
      all(RA[k] == RB[k] for k in same_raw) and len(same_raw) == len(RA) - len(CHG) + 1, repr(
          [k for k in same_raw if RA[k] != RB[k]]))
p, m = plusminus(A['<header>'], B['<header>'])
check('G header code: only the two new file-level LOCAL lines (P-U and B&R tables)',
      not m and p == ['LOCAL fdPUc, fdPUr, fdPUn, fdBR8, fdBR9, fdBR10;', 'LOCAL fdBR11, fdBRn;'], repr((p, m)))
WANT = {
    'fdPost': (['TEXTOUT_P("P(age >= " + fdF1(poThr) + ")" + fdEq(fdPctN(poP*100)) + "%",',
                'TEXTOUT_P("P(age < " + fdF1(poThr) + ")" + fdEq(fdPctN(NORMALD_CDF(pmu, psd, poThr)*100)) +',
                'poThr := ROUND(MAX(0, MIN(110, poIn)), 1);'],
               ['TEXTOUT_P("P(age >= " + STRING(poThr,2,1) + ")" + fdEq(fdPctN(poP*100)) + "%",',
                'TEXTOUT_P("P(age < " + STRING(poThr,2,1) + ")" + fdEq(fdPctN(NORMALD_CDF(pmu, psd, poThr)*100)) +',
                'poThr := MAX(0, poIn);']),
    'fdThrTable': (['"mu = " + fdF1(pmu) + "  sd = " + fdF2(psd),'],
                   ['"mu=" + STRING(pmu,2,1) + "  sd=" + STRING(psd,2,2),']),
    'fdForest': (['TEXTOUT_P("FOREST PLOT  estimate +/- 2 SD", G1, 6, 4, 2, #FFFFFFh, 308);',
                  'IF flb(foI) == "P-U 2002" THEN foC := #6A0DADh; END;',
                  'foT2 := "inv-var SD x1.25 = " + fdF2(foRaw) + " < best single SD " + fdF2(foMin);',
                  'foT3 := "the methods share root transparency: no gain";',
                  'foT2 := "inv-var SD x1.25 = " + fdF2(foRaw) + " >= best single SD " + fdF2(foMin);',
                  'foT2 := "one method: pooled SD = its SD x 1.25";'],
                 ['TEXTOUT_P("FOREST PLOT  estimate +/- 2 SE", G1, 6, 4, 2, #FFFFFFh, 308);',
                  'foT2 := "inv-var SD x1.25 = " + STRING(foRaw,2,2) + " < best single SE " + STRING(foMin,2,2);',
                  'foT3 := "the methods share P and T: no gain allowed";',
                  'foT2 := "inv-var SD x1.25 = " + STRING(foRaw,2,2) + " >= best single SE " + STRING(foMin,2,2);',
                  'foT2 := "one method: pooled SD = its SE x 1.25";']),
    'fdLPage': (['LOCAL lpW, lpB;', 'lpB := lpR(5);', 'IF lpR(7) > lpR(2) THEN',
                 'lpL := CONCAT(lpL, {"That floor is above the estimate,",', '"so no P(age >= 18) band is drawn."});',
                 'lpB := -1;', 'END;', 'fdPageV("LIVERSIDGE (2006): tooth by tooth", lpL, lpB);'],
                ['LOCAL lpW;', 'IF lpR(7) > lpR(2) THEN lpL := CONCAT(lpL, {"That floor is above the estimate."}); END;',
                 'fdPageV("LIVERSIDGE (2006): tooth by tooth", lpL, lpR(5));']),
    'fdPageV': (['LOCAL pgY, pgLine, pgCol, pgFoot, pgPer, pgFy;', 'IF vp >= 0 THEN fdBand(vp, 199); END;',
                 'pgFy := 224;', 'IF vp >= 0 THEN pgFy := 228; END;', 'TEXTOUT_P(pgFoot, G1, 6, pgFy, 1, #1E90FFh, 308);'],
                ['LOCAL pgY, pgLine, pgCol, pgFoot, pgPer;', 'IF vp >= 0 THEN fdBand(vp, 201); END;',
                 'TEXTOUT_P(pgFoot, G1, 6, 224, 1, #1E90FFh, 308);']),
    'fdWSum': (['LOCAL wuH;', 'wuH := fdWCeil(wuSt);',
                'IF wuBad > 0 THEN RETURN {0, 0, wuN, wuBad, wuWhy, 0}; END;', 'RETURN {1, wuSum, wuN, 0, 0, wuH};'],
               ['IF wuBad > 0 THEN RETURN {0, 0, wuN, wuBad, wuWhy}; END;', 'RETURN {1, wuSum, wuN, 0, 0};']),
}
for k, (wp_, wm_) in sorted(WANT.items()):
    p_, m_ = plusminus(A[k], B[k])
    check('G %s: exactly the listed lines changed' % k, p_ == wp_ and m_ == wm_, repr((p_, m_)))
p_, m_ = plusminus(A['fdWEst'], B['fdWEst'])
check('G fdWEst: its six RETURN lists gain element 11 (the all-H flag, weB(6), or 0); nothing else',
      len(p_) == len(m_) == 6 and all(re.sub(r', (?:0|weB\(6\))\}', '}', a) == b for a, b in zip(p_, m_)),
      repr((p_, m_)))
p_, m_ = plusminus(A['fdBand'], B['fdBand'])
check('G fdBand: the 0.83 / 0.58 ladder gives way to the 5 / 95 rule on the printed P, the band 27 px with two lines',
      '0.83' in ' '.join(m_) and '0.58' in ' '.join(m_) and 'bdLo := 5; bdHi := 95;' in p_ and
      'bdPc := ROUND(vp*100, 1);' in p_ and 'RECT_P(G1, 4, by, 315, by + 27, bdEdge, bdFill);' in p_ and
      not any('0.83' in x or '0.58' in x for x in B['fdBand']), repr((p_, m_)))
p_, m_ = plusminus(A['fdOdonto'], B['fdOdonto'])
check('G fdOdonto: the help line, the ceiling line and its arrow (three LINE_P), nothing else',
      m_[0] == 'TEXTOUT_P("Tap a tooth, then tap its stage (A-H).", G1, 8, 97, 1, #000000h, 305);' and
      p_[0] == 'TEXTOUT_P("Tap a tooth, then its stage. Help: main menu.", G1, 8, 97, 1, #000000h, 305);' and
      'odL := "Willems 2001: at the ceiling, >= ~15.8-16 yr";' in p_ and
      sum(1 for x in p_ if x.startswith('LINE_P(G1, odPx')) == 3, repr((p_, m_)))
p_, m_ = plusminus(A['fdWPage'], B['fdWPage'])
print('   fdWPage: %d lines added, %d removed (the ceiling page, C-F1)' % (len(p_), len(m_)))
check('G fdWPage: the ceiling branch (wpW(11) / the all-H flag) and no "Dental age" there',
      any('ceiling' in x for x in p_), repr(p_[:6]))


def fdaes_blocks(lines):
    out, cur = {}, 'pre'
    for l in lines:
        s = l.rstrip()
        if s.startswith('WHILE run DO'):
            cur = 'menu'
        m = re.match(r'^  IF ch == (\d+) THEN', s)
        if m:
            cur = 'ch%s' % m.group(1)
        out.setdefault(cur, []).append(s)
        if s.strip().startswith('END;') and s.startswith('END;'):
            cur = 'exit'
    return out


FA, FB = fdaes_blocks(A['FDAES']), fdaes_blocks(B['FDAES'])
same_blocks = [k for k in sorted(set(FA) | set(FB)) if FA.get(k) == FB.get(k)]
diff_blocks = [k for k in sorted(set(FA) | set(FB)) if FA.get(k) != FB.get(k)]
print('   FDAES(): blocks identical: %s; changed: %s' % (', '.join(same_blocks), ', '.join(diff_blocks)))
check('G FDAES(): Threshold (10) and Clear (11) identical, line for line', same_blocks == ['ch10', 'ch11'],
      repr(same_blocks))
p_, m_ = plusminus(FA['menu'], FB['menu'])
check('G FDAES() main menu: "P(age >= 18)" spaced, "How to use / assumptions" added, Exit 6 -> 7 and ch := 0',
      m_ == ['"M3 Threshold  P(age>=18)",', 'IF ch == 0 OR ch == 6 THEN'] and
      p_ == ['"M3 Threshold  P(age >= 18)",', '"How to use / assumptions",', 'IF ch == 0 OR ch == 7 THEN', 'ch := 0;'],
      repr((p_, m_)))
check('G FDAES(): v3.8a\'s "More" block (ch 5) is v3.9\'s ch 6, line for line but the number; ch 5 maps to the help (14)',
      [l.replace('ch == 5', 'ch == 6') for l in FA['ch5']] == FB['ch6'] and FB['ch5'] == ['  IF ch == 5 THEN ch := 14; END;'])
check('G FDAES(): ch 14 opens the help menu (the last block, so it ends with the loop\'s END)',
      [l.strip() for l in FB['ch14']] == ['IF ch == 14 THEN', 'fdHelpMn();', 'END;', 'END;'],
      repr(FB['ch14']))
p_, m_ = plusminus(FA['ch2'], FB['ch2'])
check('G FDAES() Willems (2): wofr (no pool at the ceiling, D7) in the four pool tests, nothing else',
      p_ == ['wofr := wr(1);', 'IF wr(11) == 1 THEN wofr := 0; END;', 'IF wofr == 1 AND wlr(1) > 0 THEN',
             'IF wofr == 1 AND wlr(1) == 0 THEN', 'IF wofr == 0 AND wlr(1) > 0 THEN', 'IF wofr == 0 AND wlr(1) == 0 THEN']
      and len(m_) == 4, repr((p_, m_)))
p_, m_ = plusminus(FA['ch3'], FB['ch3'])
check('G FDAES() M3 (3): the help item and its call, nothing else (the Mincer numbers untouched)',
      p_ == ['"Table 4: misprint & erratum",', '"How to read M3 (help)"', 'IF m3j == 4 THEN fdHelp(4); END;'] and
      m_ == ['"Table 4: misprint & erratum"'], repr((p_, m_)))
p_, m_ = plusminus(FA['ch9'], FB['ch9'])
check('G FDAES() Bayesian (9): the empty-pool message, the floor flag pfl and its line, the upper ends (fdUpEnd), '
      'ROUND before STRING (fdF1 / fdF2), and the report template; no change to the pooling itself',
      'IF psd < smin THEN psd := smin; pfl := 1; END;' in p_ and 'IF psd < smin THEN psd := smin; END;' in m_ and
      'c95hi :=          pmu + 2*psd;' in p_ and 'c95hi := MIN(110, pmu + 2*psd);' in m_ and
      'wmsg := {"Teaching & demonstration aid;",' in p_ and '"(Saunders 1837; Cattell 1928 n=7689).",' in m_ and
      not any(re.search(r'\b(tp|ws|prc)\s*:=', x) or 'psd := SQRT' in x for x in p_ + m_), repr((p_, m_)))
pool_o = [l.strip() for l in FA['ch9'] if re.search(r'\b(tp|ws|prc|pmu|psd|smin)\s*:=', l)]
pool_n = [l.strip().replace(' pfl := 1;', '') for l in FB['ch9'] if re.search(r'\b(tp|ws|prc|pmu|psd|smin)\s*:=', l)]
check('G the pool\'s arithmetic unchanged: the weights, x 1.25, the floor at the best SD (%d lines)' % len(pool_o),
      pool_o == pool_n, repr((pool_o, pool_n)))
p_, m_ = plusminus(FA['exit'], FB['exit'])
check('G FDAES() exit: the teaching-aid lines, (v3.9a) the ABFO workshop (2011) lines, the "(teaching aid; not for '
      'legal use)" tag, the spaced "P(age >= 18)", fdF1 / fdF2 / fdUpEnd',
      '"ABFO workshop (2011): a method\'s",' in p_ and not any('not checked' in x for x in p_) and
      'RETURN "FDAES (teaching aid; not for legal use): no estimate";' in p_ and
      '"], P(age >= 18)" + fdEq(fdPctN(p18)) + "%";' in p_ and
      not any('STRING(' in x for x in p_), repr((p_, m_)))
p_, m_ = plusminus(FA['ch1'], FB['ch1'])
check('G FDAES() Setup (1): the sex menu\'s "Unknown" (second review: no "[conservative SE]"), the ancestry menu '
      '(Unknown, White, Black, Other) and the Setup page',
      '"European  [Lamendin 1992]",' in m_ and '"White",' in p_ and '"Black",' in p_ and '"Other"' in p_ and
      '"Unknown  [conservative SE]",' in m_ and not any('Biological Sex' in x for x in p_ + m_), repr((p_, m_)))


def numbers(lines):
    out = []
    for l in lines:
        l = re.sub(r'"[^"]*"', '""', l)
        out += re.findall(r'(?<![\w.#])\d+(?:\.\d+)?(?![\w.])', l)
    return out


numdiff = [k for k in sorted(set(A) & set(B)) if k not in CHG and numbers(A[k]) != numbers(B[k])]
check('G every numeric literal in the unchanged routines unchanged (the Willems, Liversidge and M3 tables among them)',
      not numdiff, repr(numdiff))
check('G the Willems / Liversidge tables (fdTabs) and the M3 rows identical to v3.8a',
      A['fdTabs'] == B['fdTabs'] and all([l for l in FA['pre'] if l.strip().startswith(n)] ==
                                         [l for l in FB['pre'] if l.strip().startswith(n)] for n in ('m3xm', 'm3xf',
                                                                                                    'm3dm', 'm3df')))
check('G the Johanson coefficients unchanged (11.02, 5.14, 2.30, 4.14, 3.71, 5.57, 8.98)',
      [l.strip() for l in FB['ch7'] if l.strip().startswith('ae := 11.02') or l.strip().startswith('3.71*jC')] ==
      [l.strip() for l in FA['ch7'] if l.strip().startswith('ae := 11.02') or l.strip().startswith('3.71*jC')] != [])
check('G the file is ASCII', all(ord(c) < 128 for c in SRC))


def comment_in_bracket(src):
    depth, bad = 0, []
    for n, l in enumerate(src.split('\n'), 1):
        ins, i = False, 0
        start = depth
        while i < len(l):
            c = l[i]
            if c == '"':
                ins = not ins
            elif not ins:
                if l[i:i + 2] == '//':
                    if start > 0:
                        bad.append(n)
                    break
                if c in '({[':
                    depth += 1
                elif c in ')}]':
                    depth -= 1
            i += 1
    return bad


check('G no // comment inside an open bracket (the Prime rejects it)', not comment_in_bracket(SRC),
      repr(comment_in_bracket(SRC)))
loc = [(n, l) for n, l in enumerate(CODE, 1) if re.match(r'\s*LOCAL\s', l)]
check('G every LOCAL line <= 6 names (%d lines)' % len(loc),
      all(len(re.sub(r'^\s*LOCAL\s+', '', l).rstrip(' ;').split(',')) <= 6 for n, l in loc))
BI = set(l.strip().lower() for l in open(BUILTINS, encoding='utf-8') if l.strip() and not l.startswith('#'))
newnames = set(added)
for l in CODE:
    m_ = re.match(r'\s*LOCAL\s+(.*);', l)
    if m_:
        newnames |= set(x.strip() for x in m_.group(1).split(','))
for k in added:
    newnames |= set(x.strip() for x in re.search(r'\((.*)\)', B[k][0]).group(1).split(',') if x.strip())
clash = sorted(n for n in newnames if n.lower() in BI)
check('G no LOCAL, parameter or routine name of v3.9 is a built-in (case ignored; %d names)' % len(newnames),
      not clash, repr(clash))
check('G every non-EXPORT routine carries the fd tag', all(k.startswith('fd') for k in B if k not in ('<header>', 'FDAES')))
# helpers defined before their first use
first_def = {k: SRC.index('\n' + k + '(') for k in B if k not in ('<header>', 'FDAES')}
early = []
for k, pos in first_def.items():
    for mm in re.finditer(r'\b' + k + r'\(', SRC):
        line = SRC.count('\n', 0, mm.start())
        if mm.start() < pos and not SRC.split('\n')[line].lstrip().startswith('//'):
            early.append((k, line + 1))
check('G every routine is defined before its first use (%d routines)' % len(first_def), not early, repr(early))
# the CHOOSE pattern: every CHOOSE's index set to 0 before it.  Scanning back from each CHOOSE(v, ...) to the
# routine's head, the nearest assignment to v must be "v := 0;".  (Several CHOOSEs may share one reset when they
# sit in mutually exclusive branches: v3.8a's Willems pool menus and v3.9's Lamendin / P-U pool menus.)
cl = SRC.split('\n')
bad_ch, nch_ = [], 0
for i, l in enumerate(cl):
    mm = re.match(r'\s*CHOOSE\((\w+),', strip_comment(l))
    if mm:
        nch_ += 1
        v, ok_ = mm.group(1), False
        for j in range(i - 1, -1, -1):
            c_ = strip_comment(cl[j])
            if HEAD.match(c_.rstrip()) and not c_.startswith(' '):
                break
            if re.match(r'\s*' + v + r'\s*:=', c_):
                ok_ = re.match(r'\s*' + v + r'\s*:=\s*0\s*;', c_) is not None
                break
        if not ok_:
            bad_ch.append((i + 1, v))
check('G every CHOOSE index is reset to 0 before its CHOOSE (the nearest assignment above it is "v := 0;"; %d '
      'CHOOSEs)' % nch_, not bad_ch, repr(bad_ch))
check('G no CHOOSE return value tested', not re.search(r'(IF|:=)\s*CHOOSE\(', ''.join(CODE)))
# the version strings
check('G version strings (v3.9a): banner "// FDAES - v3.9a"; "WHAT CHANGED IN v3.9" (line numbers v3.8a\'s) kept '
      'below v3.9a\'s; the checklist FDAES_v3.9a_CHANGES.md (adding to v3.9\'s); the tested-on paragraph ("PC '
      'harness only"); the opening page and About title; verify_FDAES_v3.9a.py (Part V checks each)',
      SRC.split('\n')[3] == '// FDAES - v3.9b' and
      '// WHAT CHANGED IN v3.9  (19 Oct 2026; line numbers are v3.8a\'s)' in SRC and
      '// WHAT CHANGED IN v3.9a  (19 Oct 2026; line numbers are v3.9\'s)' in SRC and
      '// WHAT CHANGED IN v3.9b  (19 Oct 2026; line numbers are v3.9a\'s)' in SRC and
      'The test checklist is in FDAES_v3.9b_CHANGES.md, which adds' in SRC and
      SRC.count('FDAES_v3.8a_CHANGES.md') == 0 and
      'run on the PC harness only (ppl_run_v3e)' in SRC and 'fdPage("FDAES v3.9b", {' in SRC and
      'fdPage("ABOUT FDAES v3.9b", {' in SRC)   # v3.9b
check('G no "v3.8a" left as the CURRENT version in any display string (only history)',
      not any('v3.8a' in s for l in CODE for s in re.findall(r'"([^"]*)"', l)))
check('G the P-U citation is J Forensic Sci 47(1):107-116 everywhere; "47(3):519-523" only in two header comments '
      'that record the fix', '47(1):107-116' in SRC and SRC.count('519-523') == 2 and
      all('519-523' not in strip_comment(l) for l in SRC.split('\n')), repr([l for l in SRC.split('\n') if '519-523' in l]))
check('G the other header citations as their papers print them (fact sheet, 19 Oct): Bang & Ramm as Lamendin 1992 cites '
      'it (Acta Odontologica Scandinavica, Vol. 28, 1970, pp. 3-35; no "(1)"); Johanson Odontologisk Revy 22, Suppl 21 '
      'without "1-126"; the erratum "J Forensic Sci 1993, p 1524"; v3.8a\'s "28(1)", "1-126", "38:1524" only in the '
      'two comments of each that record the fix',
      'Acta Odontologica Scandinavica, Vol. 28,' in SRC and 'Odontologisk Revy, Volume 22,' in SRC and
      'Erratum, J Forensic Sci 1993, p 1524' in SRC and
      all(SRC.count(x) == 2 and all(x not in strip_comment(l) for l in SRC.split('\n'))
          for x in ('28(1)', '1-126', '38:1524')),
      repr([l for l in SRC.split('\n') if '38:1524' in l or '28(1)' in l or '1-126' in l]))
check('G "Prince-Ubelaker" pages cite 47(1):107-116 (About\'s v3.9 page)', '"P-U citation: 47(1):107-116.",' in SRC)
# ===================================================================================== Part SR (second review)
print('SR. The second review\'s items (19 Oct 2026, evening): the checks not already in Parts C, L, R, J, K, H, P, S')
SRC_CODE = '\n'.join(strip_comment(l) for l in SRC.split('\n'))
STRS = [s_ for l in SRC.split('\n') for s_ in re.findall(r'"([^"]*)"', strip_comment(l))]
check('SR 1. no display string calls a B&R molar row a first molar ("Upper first molar", "Lower first molar" gone; '
      '"Upper molar (any of six)", "Lower molar (any of six)" in the menus)',
      not any('first molar' in x.lower() for x in STRS if 'premolar' not in x.lower()) and
      STRS.count('Upper molar (any of six)') == 2 and STRS.count('Lower molar (any of six)') == 2)
check('SR 3. no "2+ teeth each" anywhere in the file (Johanson: 4 of the 46 gave one tooth)',
      '2+ teeth each' not in SRC and 'people (42 gave 2-11 teeth, 4 gave' in SRC and
      '"Table 5 (46 people, 1-11 teeth each)"};' in SRC)
check('SR 4. B&R\'s four oldest are 75.8-85.9 (Table XIII), not "84.7-85.9"', '84.7-85.9' not in SRC and
      '(75.8-85.9) came out 17.5-20.4 yr' in SRC)
check('SR 5. no "buccal midline" in B&R\'s measurement; X = TM in the help, the intro, the INPUT help and the comments',
      'buccal' not in SRC_CODE and SRC.count('TM') >= 6 and '"TM = mean of shortest and longest extent"' in SRC)
mins = [l.strip() for l in SRC_CODE.split('\n') if 'MIN(110,' in l]
check('SR 6. no MIN(110, ...) left on a printed interval end: every upper end goes through fdUpEnd (the two left are '
      'fdPost\'s drawing range and the typed age\'s clamp, C-F8): %r' % mins,
      mins == ['po95a := MAX(0, pmu - 2*psd); po95b := MIN(110, pmu + 2*psd);',
               'poThr := ROUND(MAX(0, MIN(110, poIn)), 1);'] and SRC_CODE.count('fdUpEnd(') >= 16)
hu = Harness(NEW)
ue = [hu.call('fdUpEnd', x) for x in (109.94, 109.96, 110.0, 110.01, 150.0)]
check('SR 6. fdUpEnd: 109.94 -> "109.9", 109.96 -> "110.0", 110 -> "110.0", 110.01 -> "> 110", 150 -> "> 110": %r'
      % ue, ue == ['109.9', '110.0', '110.0', '> 110', '> 110'])
SCI.extend(hu.sci_strings)
check('SR 8. "Claimed SE: +/-3.6 yr" gone; (v3.9a) "+/-3.63 yr (p 51)" from Gustafson\'s own paper in its place; '
      'v3.9\'s "not checked" lines replaced by sourced ones and ABFO cited as the 2017 manual and the 2011 workshop '
      '(Part V)', 'Claimed SE' not in SRC_CODE and '"  (pp 47-49); error +/-3.63 yr (p 51)",' in SRC and
      'Not checked against the sources' not in SRC_CODE and 'ABFO 2011' not in SRC_CODE and
      '"ABFO guidelines (DRM 2017): give",' in SRC and '"ABFO workshop (2011): a method\'s",' in SRC)
check('SR 8. the report carries no Saunders / Cattell citation', '(Saunders 1837; Cattell 1928 n=7689)' not in SRC_CODE)
check('SR 14. no display string says "SE" where FDAES means an SD: "[conservative SE]", "best single SE", "+/- 2 SE", '
      '"its SE x 1.25", "SD floored at best single SE" gone', not any(x in SRC_CODE for x in (
          '[conservative SE]', 'best single SE', '+/- 2 SE', 'its SE x 1.25', 'SD floored at best single SE')))
check('SR 18. the RETURN, the report and the header carry the fleet\'s disclaimer wording',
      SRC.count('FDAES (teaching aid; not for legal use): ') == 2 and SRC_CODE.count('"Teaching & demonstration aid;",') == 2
      and '// DISCLAIMER: a teaching and demonstration aid. Not validated for' in SRC)
check('SR 19. the refusals print the typed values with two decimals (fdF2), never fdF1',
      not re.search(r'(lbad|MSGBOX)[^;]*fdF1\(', SRC_CODE.replace('\n', ' ')) and
      SRC_CODE.count('"RH = " + fdF2(lRH) + " mm is not a root height:"') == 1 and
      '"X = " + fdF2(brX) + " mm: longer than any"' in SRC_CODE)
bad20 = [x for x in STRS if re.search(r'(?<![\d.])12\.5(?!\d)', x) and 'sqrt(pi/2) = 12.5 yr' not in x]
check('SR 20. every shown 12.5 derives from fdLamSD: the only "12.5" in a display string is fdLamLbl\'s label for the '
      'value 12.5 ("10 x sqrt(pi/2) = 12.5 yr"); the self-check says "= 12.53, rounded"', not bad20 and
      '"  = 12.53, rounded)",' in SRC, repr(bad20))
check('SR 24. the comments: fdBRCmb "9.62, not 7.07"; the 9.98 / 8.98 evidence is Table 5 and the worked example '
      '(44.92), the stepwise sequence "if anything favours 9.98"', 'give 9.62, not 7.07.' in SRC and
      'which if anything favours 9.98' in SRC and '44.92 yr computed with 8.98' in SRC and
      'so\n          // 8.98 is the plausible one' not in SRC)
FDC = SRC_CODE[SRC_CODE.index('EXPORT FDAES()'):]
check('SR 25. ROUND before STRING: the threshold table\'s heading, the posterior page, the report and the RETURN use '
      'fdF1 / fdF2 / fdUpEnd (no STRING of pmu, psd or an interval end left in FDAES())',
      '"mu = " + fdF1(pmu) + "  sd = " + fdF2(psd),' in SRC and '"Age: " + fdF1(pmu) + " yr",' in SRC and
      not re.search(r'STRING\((pmu|psd|c95lo|c95hi|c68lo|c68hi),', FDC))
check('SR 2. the near-ceiling rule is ONE named test (fdWCeil), its comment says how to widen or narrow it, and the '
      'page says why ("cannot tell 16 from 30")', 'FOR wcI FROM 3 TO 7 DO' in SRC and
      'below (1 = only all seven at H; 3 = 33-37, the rule now)' in SRC and '16 from 30' in SRC_CODE)

# ===================================================================================== Part V
# v3.9b: Part V is the v3.9 -> v3.9a check, run on v3.9a (V39A).  NEW and SRC are swapped for its duration and
# restored before Part V2 (v3.9a -> v3.9b); the harness runs it adds to ALLRUNS are v3.9a's (Parts W and X note it).
NEW_B, SRC_B = NEW, SRC
NEW, SRC = V39A, open(V39A, encoding='utf-8').read()
NRUNS_B = len(ALLRUNS)
print('V. v3.9 -> v3.9a: the history pages from the papers (FDAES_source_facts_v1a.md section 9), run on v3.9a')
# Every check below is a function of the program's source or of a harness run, applied to v3.9a (must pass)
# and to v3.9 (must fail: the old text does not meet the new checks).
SRC39 = open(V39, encoding='utf-8').read()
CODE39 = [strip_comment(l) for l in SRC39.split('\n')]

GUS = ["Gustafson (1950): 41 teeth; six",
       "  changes scored 0-3 and summed",
       "  (pp 47-49); error +/-3.63 yr (p 51)",
       "Maples & Rice (1979): the same 41",
       "  teeth built and tested the line",
       "  (circular, pp 168-169); it was",
       "  fitted to estimated, not real,",
       "  ages, and 3.63 is a mean deviation.",
       "  Refitted: SE +/-7.03 yr (p 170).",
       "Lamendin 1992 (p 1377), 39 people",
       "  aged 42-79: mean error 14.2 +/-",
       "  3.4 yr (his own: 8.9 +/- 2.2).",
       "",                                    # v3.9a: line 13, so page 1 ends at a paragraph's end
       "Summed 0-3 scores are ordinal;",
       "  regression suits them poorly",
       "  (Lucy et al. 1996, p 189).",
       "Repeat scoring: 37 teeth twice, by",
       "  one observer: +/-3.37 yr (p 52)."]
HIST = ["Saunders (1837), to Parliament:",
        "  over 1,000 London children; the",
        "  teeth vary less than any other",
        "  organ, so use them to age factory",
        "  children (pp 45, 49).",
        "Cattell (Harvard 1928): 7,689",
        "  examinations of North European",
        "  children (p 71); girls ahead of",
        "  boys by up to 8 months (p 67).",
        "Saunders et al. (McMaster 1993):",
        "  tooth-formation ages tested on 17",
        "  identified children: Moorrees",
        "  best, SD about 0.5 yr (p 173).",
        "The lesson: test a method on",
        "  people it was not built from."]
BAYT = ["ABFO guidelines (DRM 2017): give",
        "each method's age with a 95% (2 SD)",
        "interval, and for age of majority a",
        "probability statement."]
BAYT39 = ['ABFO 2011 (not checked against the', 'sources): report 95% CI, never', 'just a point estimate.']
EXITL = ["Estimates are probabilistic", "distributions, not legal age", "determinations.", "",
         "ABFO workshop (2011): a method's", "data should have had review,", "independent testing and error",
         "estimation.", "FDAES is a teaching aid: do not", "rely on it for legal purposes."]
REPL = 'SDs are real spread among people.'
JOHL = ['Gustafson summed all six equally', '(1950, p 49); these weights differ.']
NEWLINES = GUS + HIST + BAYT + EXITL[4:8] + [REPL] + JOHL + ['A SHORT HISTORY']
print('   %d new page lines, the longest %d characters' % (len(NEWLINES), max(len(x) for x in NEWLINES)))


def src_list(src, head):
    """the string literals of a page list in the source, from its head to the closing '});'"""
    i = src.index(head)
    j = src.index('});', i)
    return re.findall(r'"([^"]*)"', src[i + len(head):j])


def code_strings(src):
    return [x for l in src.split('\n') for x in re.findall(r'"([^"]*)"', strip_comment(l))]


def safe(f, src):
    try:
        return bool(f(src))
    except (ValueError, IndexError, KeyError):
        return False


VSRC = [
    ('item 1: "WHY GUSTAFSON 1950 IS EXCLUDED" is the 17 lines given, with a blank as line 13 (the page break)',
     lambda s: src_list(s, 'fdPage("WHY GUSTAFSON 1950 IS EXCLUDED", {') == GUS),
    ('item 2: the page is titled "A SHORT HISTORY" (not "HISTORICAL WARNINGS IGNORED") and is the 15 lines given',
     lambda s: src_list(s, 'fdPage("A SHORT HISTORY", {') == HIST and 'HISTORICAL WARNINGS' not in ''.join(
         strip_comment(l) for l in s.split('\n'))),
    ('item 3: "BAYESIAN FRAMEWORK" ends with a blank and the four ABFO (DRM 2017) lines; 23 lines in all',
     lambda s: src_list(s, 'fdPage("BAYESIAN FRAMEWORK", {')[-5:] == [''] + BAYT and
     len(src_list(s, 'fdPage("BAYESIAN FRAMEWORK", {')) == 23),
    ('item 4: the closing page carries the four ABFO workshop (2011) lines, ten lines in all',
     lambda s: src_list(s, 'fdPage("FDAES session ended", {') == EXITL),
    ('item 5: the report says "SDs are real spread among people." where it said "Biological variation irreducible."',
     lambda s: '        "%s",' % REPL in s and not any('irreducible' in x for x in code_strings(s))),
    ('item 6: Johanson\'s opening page: "Gustafson summed all six equally" / "(1950, p 49); these weights differ."',
     lambda s: src_list(s, 'fdPage("JOHANSON (1971)  Histological", {')[9:11] == JOHL and
     not any('ignores the actual biology' in x or 'weighted ALL' in x for x in code_strings(s))),
    ('no display string anywhere says "not checked" (any case)',
     lambda s: not any('not checked' in x.lower() for x in code_strings(s))),
    ('none of v3.9\'s unsourced history lines is displayed ("Teeth vary", "Parliament ignored him", "inter-rater", '
     '"textbook", "wrong regression", "ABFO 2011 (", "never just a point estimate", "opinions must derive")',
     lambda s: not any(any(k in x for k in ('Teeth vary', 'Parliament ignored', 'inter-rater', 'textbook',
                                            'wrong regression', 'ABFO 2011 (', 'just a point estimate',
                                            'opinions must derive')) for x in code_strings(s))),
    ('every line of the new pages is 37 characters or fewer (%d lines)' % len(NEWLINES),
     lambda s: all(len(x) <= 37 for x in src_list(s, 'fdPage("WHY GUSTAFSON 1950 IS EXCLUDED", {') +
                   src_list(s, 'fdPage("A SHORT HISTORY", {') + src_list(s, 'fdPage("BAYESIAN FRAMEWORK", {') +
                   src_list(s, 'fdPage("FDAES session ended", {')) and all(len(x) <= 37 for x in NEWLINES)),
]
for name, f in VSRC:
    check('V source, v3.9a: ' + name, safe(f, SRC))
    check('V source, v3.9 fails it (the old text): ' + name, not safe(f, SRC39))

# the header: every source with its page, no "not checked" claim left for them
HDRV = ['J Am Dent Assoc', '41:45-54', 'J Forensic Sci 24(1):168-172', '41(2):189-194', 'London: Renshaw',
        'Harvard', 'Monographs in Education no. 9', 'Am J Phys Anthropol 92:173-188', 'Diplomates Reference Manual',
        'Chicago, 19-20 February 2011', '(p 47)', '(p 49)', '(p 51)', '(p 52)', '(pp 168-169)', '(p 170)',
        '(p 189)', '(p 1377)', '[pp 45, 49]', '[pp 67, 71;', '[p 173]', 'slide 2']


def hdr_ok(s):
    hd = s[:s.index('// LAYOUT NOTE (fdPage)')]
    return (all(k in hd for k in HDRV) and '[n=7689 ignored]' not in s and
            'NOT checked against the sources read for v3.9' not in s and
            'Saunders 1993, Cattell 1928 and Harris et al. 2010 were not' not in s)


check('V header, v3.9a: WHY GUSTAFSON and REFERENCES name each source with its pages (Gustafson 1950, Maples & Rice '
      '1979, Lucy et al. 1996, E. Saunders 1837, Cattell 1928, S. Saunders et al. 1993, ABFO 2017 and 2011); '
      '"[n=7689 ignored]" and the "NOT checked" notes gone', hdr_ok(SRC))
check('V header, v3.9 fails it', not hdr_ok(SRC39))
nc = [(i + 1, l.strip()) for i, l in enumerate(SRC.split('\n')) if 'not checked' in l.lower() or 'unchecked' in l.lower()]
print('   lines that still say "not checked" / "unchecked" (all comments recording what v3.9 or v3.8a did):')
for x in nc:
    print('     %5d  %s' % x)
check('V the words "not checked" survive only in comments that record history (v3.9\'s change log, v3.9a\'s, the '
      'header note on what v3.9 listed, the report\'s note on v3.8a): %d lines' % len(nc),
      all(not strip_comment(l).strip() for _, l in nc) and len(nc) == 5 and
      all(any(k in l for k in ('every unchecked statement', 'marked "not checked"', 'Every line v3.9 marked',
                               'without sources, marked', 'not checked against any source')) for _, l in nc), repr(nc))
# the version strings (Lessons Learned rule 13)


def ver_ok(s):
    L = s.split('\n')
    i1 = s.find("// WHAT CHANGED IN v3.9a  (19 Oct 2026; line numbers are v3.9's)")
    i2 = s.find("// WHAT CHANGED IN v3.9  (19 Oct 2026; line numbers are v3.8a's)")
    return (L[3] == '// FDAES - v3.9a' and 0 < i1 < i2 and 'FDAES_v3.9a_CHANGES.md' in s and
            s.count('verify_FDAES_v3.9a.py') == 3 and 'verify_FDAES_v3.9.py' not in s and
            'fdPage("FDAES v3.9a", {' in s and 'fdPage("ABOUT FDAES v3.9a", {' in s and
            '"FDAES v3.9a has run on a PC test",' in s and 'v3.9 and v3.9a (19 Oct 2026, below) have' in s)


check('V version strings (rule 13): banner "// FDAES - v3.9a"; "WHAT CHANGED IN v3.9a" above v3.9\'s; the checklist '
      'FDAES_v3.9a_CHANGES.md; verify_FDAES_v3.9a.py (3 references, none to v3.9\'s); the opening page "FDAES v3.9a", '
      '"ABOUT FDAES v3.9a", help topic 10 "FDAES v3.9a has run on a PC test"; the tested-on paragraph', ver_ok(SRC))
check('V version strings, v3.9 fails it', not ver_ok(SRC39))
vs = sorted(set(x for x in code_strings(SRC) if re.search(r'v3\.9(?!a)', x)))
check('V every display string that names v3.9 without the "a" is history: %r' % vs,
      vs == ['  orange 58-83%, red < 58% (v3.9:', '  results kept 0.58/0.83 until v3.9.',
             'Verdict cut-points (v3.9): 5% and', 'v3.9 CHANGES'])

# ---- the routine diff, v3.9 -> v3.9a
A9, B9 = routines(SRC39), routines(SRC)
chg9 = sorted(k for k in set(A9) | set(B9) if A9.get(k) != B9.get(k))
check('V changed routines (code, comments stripped), v3.9 -> v3.9a: FDAES, fdHelp and fdM3Hist (Harris); fdJoh1SD '
      'added (item 9); none removed; the header\'s code unchanged', chg9 == ['FDAES', 'fdHelp', 'fdJoh1SD', 'fdM3Hist'] and
      set(B9) - set(A9) == {'fdJoh1SD'} and not set(A9) - set(B9) and A9['<header>'] == B9['<header>'], repr(chg9))
RA9, RB9 = raw_routines(SRC39), raw_routines(SRC)
same9 = sorted(k for k in RA9 if k not in ('FDAES', 'fdHelp', 'fdM3Hist'))
check('V every other routine (%d) is byte-identical to v3.9, comments included' % len(same9),
      all(RA9[k] == RB9.get(k) for k in same9), repr([k for k in same9 if RA9[k] != RB9.get(k)]))
check('V fdJoh1SD is the whole routine "RETURN 6.0;"', B9['fdJoh1SD'] == ['fdJoh1SD()', 'BEGIN', '  RETURN 6.0;', 'END;'],
      repr(B9['fdJoh1SD']))
H7NEW = ["8: 'Error' 6.0 for one tooth, 5.2", "for two (the fit's SD: 5.16), 4.4",
         '"for ten. FDAES: 1 tooth SD " + fdF1(fdJoh1SD()) + ";",', '2+ teeth SD 5.16, not made smaller.',
         'TEST (Lucy, Pollard & Roberts 1995):', '35 roots of 17 new people: mean', 'deviation 4.5 yr (SD ~5.6 if',
         'normal); about 68% within +/-5.16.', 'Small test: new cases may miss more.',
         '3.95) than his men (5.88). Johanson', 'describes no test sample of his', 'own in the pages read.']
H7OLD = ["8: 'Error' 6.0 for one tooth, 5.2", 'for two, 4.4 for ten (what kind of', "error is not stated). FDAES's 8.00",
         'for one tooth is its own allowance.', '3.95) than his men (5.88). No', 'independent test sample is',
         'described in the pages read.']
q = lambda xs: [x if x.startswith('"') else '"%s",' % x for x in xs]
p_, m_ = plusminus(A9['fdHelp'], B9['fdHelp'])
check('V fdHelp: topic 7\'s spread and test lines (item 9) and topic 10\'s version line, nothing else',
      sorted(p_) == sorted(q(H7NEW[1:-1]) + ['"own in the pages read."});', '"FDAES v3.9a has run on a PC test",']) and
      sorted(m_) == sorted(q(H7OLD[1:4]) + q(H7OLD[4:6]) + ['"described in the pages read."});',
                                                              '"FDAES v3.9 has run on a PC test",']),
      repr((p_, m_)))
p_, m_ = plusminus(A9['FDAES'], B9['FDAES'])
lit = lambda xs: [y for x in xs for y in (re.findall(r'"([^"]*)"', x) or ['<code> ' + x])]
OLDP = set(src_list(SRC39, 'fdPage("WHY GUSTAFSON 1950 IS EXCLUDED", {') +
           src_list(SRC39, 'fdPage("HISTORICAL WARNINGS IGNORED", {') + BAYT39 +
           src_list(SRC39, 'fdPage("FDAES session ended", {')[4:8] +
           ['Gustafson weighted ALL equally.', 'That ignores the actual biology.', 'Biological variation irreducible.',
            'FDAES v3.9', 'ABOUT FDAES v3.9', 'HISTORICAL WARNINGS IGNORED', 'WHY GUSTAFSON 1950 IS EXCLUDED'] +
           # item 9: the teeth menu (simple form), the one-tooth words, About's v3.9 page
           ['Number of teeth averaged?', '1 tooth   8.00 (FDAES only)', '2+ teeth  5.16 (Johanson SD)',
            "SD 8.00 yr = FDAES's allowance;", "Johanson's Table 8: 6.0 for 1 tooth.", "  people); 8.00 is FDAES's own;",
            '<code> CHOOSE(jnc,', '<code> );', '<code> IF jnc == 2 THEN jse := 5.16; ELSE jse := 8.00; END;'])
NEWP = set(NEWLINES + ['FDAES v3.9a', 'ABOUT FDAES v3.9a', 'WHY GUSTAFSON 1950 IS EXCLUDED'] +
           ['Number of teeth averaged?', '1 tooth   ', ' (his Table 8)', '2+ teeth  5.16 (Johanson SD)',
            '1 tooth: SD ', ' (Johanson Table 8;', '  Lucy 1995, 17 new people: ~5.6).', '  people); 1 tooth SD ',
            ' (v3.9a);', '<code> IF jnc == 2 THEN jse := 5.16; ELSE jse := fdJoh1SD(); END;'])
print('   FDAES(): %d code lines added, %d removed' % (len(p_), len(m_)))
check('V FDAES(): every added code line is a v3.9a page line or title, every removed one a v3.9 history line or '
      'version title, the two Johanson / one report line, or (item 9) the teeth menu, the one-tooth spread and its '
      'words and About\'s "8.00 is FDAES\'s own"; nothing else (no other number, menu or logic changed)',
      all(x in NEWP for x in lit(p_)) and all(x in OLDP for x in lit(m_)),
      repr([x for x in lit(p_) if x not in NEWP] + [x for x in lit(m_) if x not in OLDP]))
KEEP9A = {'WHY GUSTAFSON 1950 IS EXCLUDED', 'Saunders et al. (McMaster 1993):'}     # unchanged lines in both lists
check('V FDAES(): every v3.9a line listed above was added (%d) and every v3.9 line it replaces removed; unchanged in '
      'both: %r' % (len(NEWP - KEEP9A), sorted(KEEP9A)),
      NEWP - KEEP9A <= set(lit(p_)) and OLDP - KEEP9A <= set(lit(m_)) and KEEP9A <= NEWP & OLDP,
      repr((sorted(NEWP - KEEP9A - set(lit(p_))), sorted(OLDP - KEEP9A - set(lit(m_))))))

# ---- the harness: the pages as drawn
NAB39 = 19


def about_run(prog, nkeys):
    return run(prog, [6, 7, 7], [K] * nkeys, opening=True, tag='V About %s' % os.path.basename(prog))


def foots(h, prefix):
    return [[t.text for t in p.texts if t.y == 224 and t.font == 1] for p in pages_titled(h, prefix)]


def ys(p):
    return [x.y for x in sorted(p.texts, key=lambda t: t.y) if x.font == 2 and x.x == 6 and 30 <= x.y <= 198]


TWO = [['page 1 of 2, any key or tap = next'], ['page 2 of 2, any key or tap = back']]


def h_gus(h):
    g = pages_titled(h, 'WHY GUSTAFSON 1950 IS EXCLUDED')
    return (len(g) == 2 and page_lines(g[0]) == GUS[:12] and page_lines(g[1]) == GUS[13:] and
            ys(g[0])[-1] == 30 + 11 * 14 and ys(g[1])[0] == 30 and foots(h, 'WHY GUSTAFSON') == TWO)


def h_hist(h):
    g = [p for p in h.pages if title(p) == 'A SHORT HISTORY']
    return (len(g) == 2 and page_lines(g[0]) == HIST[:13] and page_lines(g[1]) == HIST[13:] and
            ys(g[0])[-1] == 30 + 12 * 14 and foots(h, 'A SHORT HISTORY') == TWO and
            not pages_titled(h, 'HISTORICAL WARNINGS'))


def h_bay(h):
    g = pages_titled(h, 'BAYESIAN FRAMEWORK')
    return (len(g) == 2 and page_lines(g[0])[-1] == 'than the best single method.' and len(page_lines(g[0])) == 12
            and page_lines(g[1])[-4:] == BAYT and len(page_lines(g[1])) == 9 and foots(h, 'BAYESIAN') == TWO)


def h_exit(h):
    g = pages_titled(h, 'FDAES session ended')
    return len(g) == 1 and page_lines(g[0]) == [x for x in EXITL if x]


def h_width(h):
    return all(len(l) <= 37 for p in h.pages for l in page_lines(p))


HV = [('item 1 as drawn: "WHY GUSTAFSON 1950 IS EXCLUDED" on two pages, the break after Lamendin\'s paragraph '
       '(page 1: Gustafson, Maples & Rice, Lamendin, 12 lines, the last at row 184; page 2 from row 30: Lucy, the '
       'repeat scoring); "page 1 of 2" / "page 2 of 2" footers', h_gus),
      ('item 2 as drawn: "A SHORT HISTORY" on two pages, the break after the third paragraph (13 lines: Saunders '
       '1837, Cattell, Saunders et al.), page 2 "The lesson ..."', h_hist),
      ('item 3 as drawn: "BAYESIAN FRAMEWORK" breaks where it did (page 1 ends "than the best single method."), '
       'page 2 ends with the four ABFO lines', h_bay),
      ('item 4 as drawn: the closing page, nine lines and the blank', h_exit),
      ('every line About and the closing page draw is 37 characters or fewer', h_width)]
ha = about_run(NEW, NABOUT)
ho9 = about_run(V39, NAB39)
for name, f in HV:
    check('V harness, v3.9a: ' + name, f(ha))
    check('V harness, v3.9 fails it: ' + name, not f(ho9)) if f is not h_width else \
        check('V harness, v3.9 too (its lines also fit): ' + name, f(ho9))
check('V About: %d keys for v3.9a (one more than v3.9\'s %d: the history page is now two pages); every key used, '
      'the program ended' % (NABOUT, NAB39), NABOUT == NAB39 + 1 and ha.result == ho9.result ==
      'FDAES (teaching aid; not for legal use): no estimate')
# every other About page drawn exactly as v3.9 drew it
EXV = ('WHY GUSTAFSON 1950 IS EXCLUDED', 'A SHORT HISTORY', 'HISTORICAL WARNINGS IGNORED', 'BAYESIAN FRAMEWORK',
       'FDAES session ended')


def scr_sig(h, rw=None):
    out = []
    for sc in h.screens:
        tt = title(sc)
        if tt in EXV:
            continue
        tx = [((rw or {}).get(t.text, t.text), t.x, t.y, t.font, t.hex, t.width) for t in sc.texts]
        sh = [(x.cmd, [num(a) for a in x.args]) for x in sc.shapes]
        out.append((tx, sh, sc.menu, sc.reason))
    return out


RW9A = {'FDAES v3.9': 'FDAES v3.9a', 'ABOUT FDAES v3.9': 'ABOUT FDAES v3.9a',
        'et al., Table 12), and it lives on in': 'et al., Table 13.12, p 289); it lives',     # Harris, the book
        'copies without the erratum page.': 'on in copies lacking the erratum.',
        "  people); 8.00 is FDAES's own;": '  people); 1 tooth SD 6.0 (v3.9a);',      # item 9
        '1 tooth   8.00 (FDAES only)': '1 tooth   6.0 (his Table 8)',               # item 9, the teeth menu
        'FDAES v3.9 has run on a PC test': 'FDAES v3.9a has run on a PC test',
        'Gustafson weighted ALL equally.': JOHL[0], 'That ignores the actual biology.': JOHL[1],
        'Biological variation irreducible.': REPL}
bf9, bfa = pages_titled(ho9, 'BAYESIAN FRAMEWORK'), pages_titled(ha, 'BAYESIAN FRAMEWORK')
check('V About: every other page (%d screens) drawn exactly as v3.9 drew it, the title "ABOUT FDAES v3.9a" apart; '
      'the Bayesian page 1 identical, page 2 v3.9\'s with the ABFO lines replaced' % len(scr_sig(ha)),
      scr_sig(ha) == scr_sig(ho9, RW9A) and page_lines(bfa[0]) == page_lines(bf9[0]) and
      page_lines(bf9[1])[-3:] == BAYT39 and page_lines(bfa[1]) == page_lines(bf9[1])[:-3] + BAYT)


def same9(tag, chs, evs, inps=()):
    h1 = run(NEW, chs, evs, inps, opening=True, tag='V ' + tag)
    h0 = run(V39, chs, evs, inps, opening=True, tag='V v3.9 ' + tag)
    s1, s0 = scr_sig(h1), scr_sig(h0, RW9A)
    sig1 = (s1, [(c.title, c.items, c.index) for c in h1.chooses], [(i.title, i.labels, i.before, i.after)
                                                                   for i in h1.inputs], [m.lines for m in h1.msgboxes],
            h1.result)
    sig0 = (s0, [(c.title, [RW9A.get(i, i) for i in c.items], c.index) for c in h0.chooses], [(i.title, i.labels, i.before, i.after)
                                                                   for i in h0.inputs], [m.lines for m in h0.msgboxes],
            h0.result)
    check('V session identical to v3.9 but the v3.9a lines (screens, dialogs, inputs, MSGBOXes, RETURN): ' + tag,
          sig1 == sig0, repr([i for i in range(5) if sig1[i] != sig0[i]]))
    return h1, h0


# help topic 10 (two pages), back to the help menu, Exit
h10, h10o = same9('help topic 10', [5, 10, 0, 7], [K, K, K])
t10 = [l for p in pages_titled(h10, 'WHAT FDAES IS NOT') for l in page_lines(p)]
check('V help topic 10 says "FDAES v3.9a has run on a PC test" (v3.9: "FDAES v3.9 ...")',
      'FDAES v3.9a has run on a PC test' in t10 and 'FDAES v3.9 has run on a PC test' in
      [l for p in pages_titled(h10o, 'WHAT FDAES IS NOT') for l in page_lines(p)])
# Johanson, two teeth, pooled; then the posterior, the forest plot, the report and Exit (male, white)
hj, hjo = same9('Johanson -> pool -> report', [1, 2, 2, 6, 1, 2, 1, 6, 3, 7],
                [K, K, K, K, K, soft(2), K, soft(6), K, K], [[1, 1.5, .5, .5, 0, 2.5]])
ip = page_lines(pages_titled(hj, 'JOHANSON (1971)  Histological')[0])
ipo = page_lines(pages_titled(hjo, 'JOHANSON (1971)  Histological')[0])
check('V Johanson\'s opening page: the drawn lines 9-10 (10-11 with the blank) are the new two, the other ten as v3.9; '
      '12 drawn lines (13 with the blank)', ip[8:10] == JOHL and
      ipo[8:10] == ['Gustafson weighted ALL equally.', 'That ignores the actual biology.']
      and ip[:8] + ip[10:] == ipo[:8] + ipo[10:] and len(ip) == 12, repr(ip))
rp = [l for p in pages_titled(hj, 'REPORT TEMPLATE') for l in page_lines(p)]
rpo = [l for p in pages_titled(hjo, 'REPORT TEMPLATE') for l in page_lines(p)]
check('V the report: line 8 "SDs are real spread among people." (v3.9: "Biological variation irreducible."); the '
      'other eleven as v3.9; one page', len(pages_titled(hj, 'REPORT TEMPLATE')) == 1 and rp[7] == REPL and
      rpo[7] == 'Biological variation irreducible.' and rp[:7] + rp[8:] == rpo[:7] + rpo[8:] and len(rp) == 12,
      repr(rp))
check('V the opening page: "FDAES v3.9a" (v3.9: "FDAES v3.9"), its lines as v3.9\'s',
      title(hj.pages[0]) == 'FDAES v3.9a' and title(hjo.pages[0]) == 'FDAES v3.9' and
      page_lines(hj.pages[0]) == page_lines(hjo.pages[0]))
# Willems + Liversidge + Lamendin pooled (the report's two-page form), the same session on both
# (Part P's pool_session([('W', st), ('L', st), ('Lam',)]) for a white male, spelled out: Setup; the odontogram
# twice, pooling Willems then Liversidge; Lamendin on the worked tooth, pooled; the posterior (two pages), the
# forest plot, Done, the report (two pages: Lamendin is pooled); Exit)
stv = [7] * 7
Wv, pwv, _ = exp_willems_page(stv, 1)
Lv, plv, _ = exp_liv_page(stv, 1)
chv, evv = [1, 2, 2], [K]
for pick in (1, 2):
    chv += [2, pick]
    for i, s_ in enumerate(stv, 1):
        evv += [tooth(i), stage(s_)]
    evv += [soft(6)] + [K] * (npages(Wv, pwv) + npages(Lv, plv))
chv += [4, 2, 6, 3, 7]
evv += [K] * 3 + [K] * 2 + [soft(2), K, soft(6)] + [K] * 2 + [K]
hw, hwo = same9('Willems + Liversidge + Lamendin -> pool -> report (two pages)', chv, evv, [list(LAMH)])
check('V that report: two pages, "SDs are real spread among people." on page 1',
      len(pages_titled(hw, 'REPORT TEMPLATE')) == 2 and
      REPL in page_lines(pages_titled(hw, 'REPORT TEMPLATE')[0]))

# ===================================================================================== Part V, item 9
# Roger's D5, 19 Oct 2026 (the coordinator's follow-up): Johanson, ONE tooth, SD 8.00 -> 6.0.  Sources: Johanson
# 1971 Table 8 ("Error" 6.0 for one tooth, 5.2 for two; fact sheet v1a section 7(d)); Lucy, Pollard & Roberts 1995
# (ms pp 5-6: 17 people, single roots, mean absolute deviation 4.5 yr, about 68 % within +/- 5.16; section 9).
print('   item 9: Johanson, one tooth, SD 8.00 -> 6.0 (Johanson 1971 Table 8; Lucy, Pollard & Roberts 1995)')
V9SRC = [
    ('item 9: fdJoh1SD returns 6.0, the ONE place the number lives: defined once and read five times in code (the '
     'menu item, the spread, the result page\'s words, help topic 7, About)',
     lambda s: 'fdJoh1SD()\nBEGIN\n  RETURN 6.0;\nEND;' in s and
     sum(strip_comment(l).count('fdJoh1SD()') for l in s.split('\n')) == 6),
    ('item 9: no 8.00 is left as the Johanson spread: the one 8.00 in code is Liversidge\'s table row (fdLbM, boys, '
     'I1 at G)', lambda s: [l.strip()[:12] for l in s.split('\n') if '8.00' in strip_comment(l)] == ['fdLbM := {0,']),
    ('item 9: no display string calls the one-tooth spread an "allowance", "FDAES only" or FDAES\'s own (the one '
     '"FDAES\'s own" left is the x 1.25 and floor line of help topic "Assumptions")',
     lambda s: not any('allowance' in x or 'FDAES only' in x for x in code_strings(s)) and
     [x for x in code_strings(s) if "FDAES's own" in x] == ["   single SD): FDAES's own choices,"]),
    ('item 9: 2+ teeth stays 5.16, not made smaller with more teeth ("jse := 5.16" for jnc 2; no Table 8 row 5.2 ... 4.4 '
     'used)', lambda s: 'IF jnc == 2 THEN jse := 5.16; ELSE jse := fdJoh1SD(); END;' in s),
]
for name, f in V9SRC:
    check('V source, v3.9a: ' + name, safe(f, SRC))
    check('V source, v3.9 fails it (the old text): ' + name, not safe(f, SRC39))
hj1 = Harness(NEW)
check('V item 9: fdJoh1SD() = 6.0 in the harness', hj1.call('fdJoh1SD') == 6.0, repr(hj1.call('fdJoh1SD')))
SCI.extend(hj1.sci_strings)

# one tooth on both versions, two cases: T = 1 alone (20.00 yr, P(age >= 18) mid-range) and Johanson's own worked
# example (A 2, S 1, P 1, C 1, R 0, T 1.5: 44.92 yr, his p 118), the second pooled alone
CASES9 = [('T = 1 alone', dict(A=D('0'), S=D('0'), P=D('0'), C=D('0'), R=D('0'), T=D('1')), D('20.00')),
          ('Johanson\'s worked example', dict(A=D('2'), S=D('1'), P=D('1'), C=D('1'), R=D('0'), T=D('1.5')), D('44.92'))]


def one_tooth(prog, sc, pool, tag):
    vals = [float(sc[k]) for k in 'ASPCRT']
    if pool:
        return run(prog, [6, 1, 1, 1, 6, 3, 7], [K, K, K, K, soft(2), K, soft(6), K, K], [vals], opening=True,
                   tag='V 1 tooth pooled ' + tag)
    return run(prog, [6, 1, 1, 2, 7], [K, K, K, K], [vals], opening=True, tag='V 1 tooth ' + tag)


for i9, (tg, sc, age9) in enumerate(CASES9):
    L9, pr9, a9, ok9 = exp_joh(sc, 1)
    hn9 = one_tooth(NEW, sc, i9 == 1, tg)
    ho9_ = one_tooth(V39, sc, i9 == 1, tg)
    pgn, pgo = pages_titled(hn9, JT), pages_titled(ho9_, JT)
    okr, dr = same_rows(pgn, L9, pr9)
    lo9 = [l for p in pgo for l in page_lines(p)]
    ln9 = [l for p in pgn for l in page_lines(p)]
    w68 = '68%%: [%s, %s]' % (F1(age9 - 6)[0], F1(age9 + 6)[0])
    w95 = '95%%: [%s, %s]' % (F1(age9 - 12)[0], F1(age9 + 12)[0])
    o68 = '68%%: [%s, %s]' % (F1(age9 - 8)[0], F1(age9 + 8)[0])
    print('     %s, one tooth: v3.9a %s, %s, P(age >= 18) = %.4f (SciPy, SD 6.0); v3.9 %s, P = %.4f (SD 8.00)'
          % (tg, w68, w95, norm.sf(18, float(age9), 6.0), o68, norm.sf(18, float(age9), 8.0)))
    check('V item 9, %s (%s yr), one tooth: v3.9a\'s page = the independent page with SD 6.0, row by row ("%s", "%s"); '
          'both pages banded, P(age >= 18) = SciPy\'s norm.sf(18, %s, 6.0) = %.4f as printed'
          % (tg, age9, w68, w95, age9, pr9), a9 == age9 and okr and len(pgn) == 2 and
          all(band_ok(p, pr9) for p in pgn) and w68 in ln9 and w95 in ln9, repr(dr[:3]))
    check('V item 9, %s: v3.9 printed 8.00 (its menu "1 tooth   8.00 (FDAES only)", "SD 8.00 yr = FDAES\'s '
          'allowance;", "%s"), and its band P was norm.sf(18, %s, 8.00) = %.4f' % (tg, o68, age9,
                                                                               norm.sf(18, float(age9), 8.0)),
          "SD 8.00 yr = FDAES's allowance;" in lo9 and o68 in lo9 and
          [c.items[0] for c in ho9_.chooses if c.title == 'Number of teeth averaged?'] == ['1 tooth   8.00 (FDAES only)']
          and all(band_ok(p, float(norm.sf(18, float(age9), 8.0))) for p in pgo), repr(lo9))
    check('V item 9, %s: v3.9a\'s menu "1 tooth   6.0 (his Table 8)"; its words "1 tooth: SD 6.0 (Johanson Table '
          '8; / Lucy 1995, 17 new people: ~5.6)."; no 8.00 on any screen of the run' % tg,
          [c.items[0] for c in hn9.chooses if c.title == 'Number of teeth averaged?'] ==
          ['1 tooth   6.0 (his Table 8)'] and '1 tooth: SD 6.0 (Johanson Table 8;' in ln9 and
          '  Lucy 1995, 17 new people: ~5.6).' in ln9 and
          not any('8.00' in t.text for sc_ in hn9.screens for t in sc_.texts), repr(ln9))
    if i9 == 1:
        po_n = [l for p in pages_titled(hn9, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
        po_o = [l for p in pages_titled(ho9_, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
        check('V item 9, one tooth pooled alone: the pool stores SD 6.0, so the posterior is 44.92 yr, SD 6.0 x 1.25 = '
              '7.50 (the floor, 6.0, not needed); v3.9 stored 8.00 (SD 10.00)',
              matches(po_n[0], S('Mean:   ', F2(44.92), ' yr')) and po_n[1] == 'SD:     7.50 yr' and
              po_o[1] == 'SD:     10.00 yr', repr((po_n[:3], po_o[:3])))
# help topic 7 and About on both
h7n = run(NEW, [5, 7, 0, 7], [K] * 3 + [K], opening=True, tag='V help 7')
h7o = run(V39, [5, 7, 0, 7], [K] * 3 + [K], opening=True, tag='V v3.9 help 7')
l7n = [l for p in pages_titled(h7n, 'HELP: JOHANSON 1971') for l in page_lines(p)]
l7o = [l for p in pages_titled(h7o, 'HELP: JOHANSON 1971') for l in page_lines(p)]
check('V item 9, help topic 7: "for ten. FDAES: 1 tooth SD 6.0;", "2+ teeth SD 5.16, not made smaller.", Lucy, Pollard '
      '& Roberts 1995\'s test (17 new people, mean deviation 4.5 yr, SD ~5.6, ~68%% within +/-5.16) and "Small test: '
      'new cases may miss more."; three pages; no "allowance"; v3.9 said "FDAES\'s 8.00 / for one tooth is its own '
      'allowance."', all(x in l7n for x in [l for l in H7NEW if not l.startswith('"')] +
                         ['for ten. FDAES: 1 tooth SD 6.0;']) and
      len(pages_titled(h7n, 'HELP: JOHANSON 1971')) == 3 and not any('allowance' in l or '8.00' in l for l in l7n)
      and "error is not stated). FDAES's 8.00" in l7o and 'for one tooth is its own allowance.' in l7o, repr(l7n))
a9n = [l for p in pages_titled(ha, 'v3.9 CHANGES') for l in page_lines(p)]
a9o = [l for p in pages_titled(ho9, 'v3.9 CHANGES') for l in page_lines(p)]
check('V item 9, About ("v3.9 CHANGES"): "  people); 1 tooth SD 6.0 (v3.9a);" where v3.9 said "  people); 8.00 is '
      'FDAES\'s own;"', '  people); 1 tooth SD 6.0 (v3.9a);' in a9n and "  people); 8.00 is FDAES's own;" in a9o and
      not any('8.00' in l for l in a9n), repr(a9n))
# a one-line change: fdJoh1SD returning 7.5 changes every shown one-tooth figure (menu, page, band, help, About)
alt9 = os.path.join(tempfile.mkdtemp(), 'FDAES_v3.9a_J1alt.txt')
open(alt9, 'w', encoding='utf-8').write(SRC.replace('fdJoh1SD()\nBEGIN\n  RETURN 6.0;\nEND;',
                                                    'fdJoh1SD()\nBEGIN\n  RETURN 7.5;\nEND;', 1))
dl9 = [l for l in difflib.unified_diff(SRC.split('\n'), open(alt9).read().split('\n'), lineterm='', n=0)
       if l[:1] in '+-' and not l.startswith(('+++', '---'))]
check('V item 9 is a one-line change: the file with fdJoh1SD returning 7.5 differs in exactly one line',
      dl9 == ['-  RETURN 6.0;', '+  RETURN 7.5;'], repr(dl9))
hx = one_tooth(alt9, CASES9[0][1], False, 'alt 7.5')
lx = [l for p in pages_titled(hx, JT) for l in page_lines(p)]
hx7 = run(alt9, [5, 7, 0, 7], [K] * 3 + [K], opening=True, tag='V alt 7.5 help 7')
hxa = run(alt9, [6, 7, 7], [K] * NABOUT, opening=True, tag='V alt 7.5 About')
check('V item 9 with 7.5: the menu "1 tooth   7.5 (...)", the page "1 tooth: SD 7.5 (...", "68%: [12.5, 27.5]", the band '
      'from norm.sf(18, 20, 7.5), help topic 7 "1 tooth SD 7.5;", About "1 tooth SD 7.5": every shown one-tooth '
      'figure comes from fdJoh1SD',
      [c.items[0] for c in hx.chooses if c.title == 'Number of teeth averaged?'] == ['1 tooth   7.5 (his Table 8)']
      and '1 tooth: SD 7.5 (Johanson Table 8;' in lx and '68%: [12.5, 27.5]' in lx and
      all(band_ok(p, float(norm.sf(18, 20.0, 7.5))) for p in pages_titled(hx, JT)) and
      'for ten. FDAES: 1 tooth SD 7.5;' in [l for p in hx7.pages for l in page_lines(p)] and
      '  people); 1 tooth SD 7.5 (v3.9a);' in [l for p in hxa.pages for l in page_lines(p)], repr(lx))

# ===================================================================================== Part V, the follow-up
# (coordinator, 19 Oct 2026): Harris et al. 2010 confirmed from the published book (ch 13, Table 13.12, p 289;
# H:\Books and Papers\Forensic Dentistry, Second Edition.pdf); "vol 38" stays, inferred from Mincer 1993's own
# volume; the near-ceiling rule confirmed by Roger (19 Oct 2026, 15:55).
print('   follow-up: Harris et al. 2010 (Table 13.12, p 289), "vol 38", the near-ceiling rule confirmed')
MISP = ['Mincer et al., J Forensic Sci, March', '1993, Table 4 (p 384): P(age >= 18)', 'by third-molar grade.  It printed',
        '69.4% for males, mandible, grade E.', '', "The journal's erratum (vol 38,", 'p 1524) corrected it to 29.4%.', '',
        'The 69.4 was reprinted in the 2010', 'Forensic Dentistry chapter (Harris',
        'et al., Table 13.12, p 289); it lives', 'on in copies lacking the erratum.', 'Next: how a reader could spot it.']
VFU = [
    ('the misprint page (fdM3Hist page 1) is the 13 lines with Harris et al.\'s "Table 13.12, p 289" (the new lines '
     '37 and 33 characters; every line <= 37)',
     lambda s: src_list(s, 'fdPage("A MISPRINT AND ITS ERRATUM", {') == MISP and all(len(x) <= 37 for x in MISP) and
     [len(x) for x in MISP[10:12]] == [37, 33]),
    ('the header and REFERENCES give Harris et al. 2010 as confirmed: ch 13, Table 13.12, p 289, from the book\'s path; '
     'no "still unconfirmed"; "vol 38" said to be inferred from the paper\'s own volume',
     lambda s: 'Table 13.12, p 289' in s[:s.index('// LAYOUT NOTE (fdPage)')] and
     re.sub(r'\n\s*//\s*', ' ', s).count("H:\\Books and Papers\\Forensic Dentistry, Second Edition.pdf") == 3 and
     'still unconfirmed' not in s and
     'Harris EF, Mincer HH, Anderson KM, Senn DR (2010)' in s and
     re.sub(r'\n\s*//\s*', ' ', s).count("38 is inferred from the paper's own volume") == 2),
    ('the near-ceiling rule: "Roger confirmed, 19 Oct 2026" in the header and above fdWCeil; no "pending Roger"',
     lambda s: 'pending Roger' not in s and "coordinator's recommendation" not in s and
     '// The rule (Roger confirmed, 19 Oct 2026, 15:55): the' in s and
     'ceiling rule, Roger confirmed, 19 Oct 2026): when teeth 33-37' in s),
]
for name, f in VFU:
    check('V source, v3.9a: ' + name, safe(f, SRC))
    check('V source, v3.9 fails it (the old text): ' + name, not safe(f, SRC39))
p_, m_ = plusminus(A9['fdM3Hist'], B9['fdM3Hist'])
check('V fdM3Hist, v3.9 -> v3.9a: only the two Harris lines (code, comments stripped)',
      p_ == ['"et al., Table 13.12, p 289); it lives",', '"on in copies lacking the erratum.",'] and
      m_ == ['"et al., Table 12), and it lives on in",', '"copies without the erratum page.",'], repr((p_, m_)))
check('V fdWCeil unchanged, the rule\'s code itself (Roger confirmed the rule; only the comment above it changed)',
      RA9['fdWCeil'] == RB9['fdWCeil'] and B9['fdWCeil'] == A9['fdWCeil'])
mpn = pages_titled(ha, 'A MISPRINT AND ITS ERRATUM')
mpo = pages_titled(ho9, 'A MISPRINT AND ITS ERRATUM')
check('V harness, v3.9a (About): the misprint page is still ONE page, its 11 drawn lines as listed, the last at row '
      '198, the footer "any key or tap = next" (no "page 1 of"), every line <= 37 characters',
      len(mpn) == 1 and page_lines(mpn[0]) == [x for x in MISP if x] and ys(mpn[0])[-1] == 30 + 12 * 14 and
      [t.text for t in mpn[0].texts if t.y == 224 and t.font == 1] == ['any key or tap = next'] and
      all(len(l) <= 37 for l in page_lines(mpn[0])), repr(page_lines(mpn[0]) if mpn else None))
check('V harness, v3.9 fails it: its page said "et al., Table 12), and it lives on in" / "copies without the erratum '
      'page."', len(mpo) == 1 and page_lines(mpo[0]) != [x for x in MISP if x] and
      'et al., Table 12), and it lives on in' in page_lines(mpo[0]))
# the same page from the M3 module's jaw menu (item 3), both versions identical but the two lines
hm, hmo = same9('M3 jaw menu -> the misprint pages', [3, 3, 7], [K, K, K])
check('V the M3 module\'s route to the misprint page shows the new lines too',
      page_lines(pages_titled(hm, 'A MISPRINT AND ITS ERRATUM')[0]) == [x for x in MISP if x])
# ===================================================================================== Part Q (kept from v3.8a)
# ======================================================================================================
# v3.9b: restore the program under test, then Part V2: v3.9a -> v3.9b
NEW, SRC = NEW_B, SRC_B
print('   Part V ran %d harness sessions on v3.9a (counted in Parts W and X)' % (len(ALLRUNS) - NRUNS_B))
print('V2. v3.9a -> v3.9b: the Gustafson page reworded from Lucy & Pollard 1995 and Aykroyd 1995')
SRC9A = open(V39A, encoding='utf-8').read()
GUSB = ["Gustafson (1950): 41 teeth; six",
        "  changes scored 0-3 and summed",
        "  (pp 47-49); error +/-3.63 yr (p 51)",
        "Maples & Rice (1979): the same 41",
        "  teeth built and tested the line",
        "  (circular, pp 168-169). Refitted",
        "  on real ages: SE +/-7.03 (p 170).",
        "Aykroyd (1995, p 925): 3.63 is the",
        "  error of a predicted mean, using",
        "  the wrong SD; not one estimate's.",
        "Lamendin 1992 (p 1377), 39 people",
        "  aged 42-79: mean error 14.2 +/-",
        "  3.4 yr (his own: 8.9 +/- 2.2).",
        "Summed 0-3 scores are ordinal;",
        "  regression suits them poorly",
        "  (Lucy et al. 1996, p 189).",
        "Repeat scoring: 37 teeth twice, by",
        "  one observer: +/-3.37 yr (p 52)."]
check('V2 source: "WHY GUSTAFSON 1950 IS EXCLUDED" is the 18 lines given, no blank (page 1 = 13 lines, ending with '
      'Lamendin\'s paragraph)', src_list(SRC, 'fdPage("WHY GUSTAFSON 1950 IS EXCLUDED", {') == GUSB,
      repr(src_list(SRC, 'fdPage("WHY GUSTAFSON 1950 IS EXCLUDED", {')))
check('V2 source, v3.9a: the same page was v3.9a\'s 17 lines and a blank (Part V\'s GUS)',
      src_list(SRC9A, 'fdPage("WHY GUSTAFSON 1950 IS EXCLUDED", {') == GUS)
check('V2 every line of the new page is 37 characters or fewer', all(len(x) <= 37 for x in GUSB),
      repr([x for x in GUSB if len(x) > 37]))
check('V2 no display string anywhere says "mean deviation" or "estimated, not real"',
      not any('mean deviation' in s or 'estimated, not real' in s or 'average deviation' in s
              for l in [strip_comment(x) for x in SRC.split('\n')] for s in re.findall(r'"([^"]*)"', l)))
hdr_b = SRC.split('\nEXPORT ')[0] if '\nEXPORT ' in SRC else SRC[:SRC.find('\nfd')]
check('V2 header: WHY GUSTAFSON cites Lucy & Pollard 1995 (pp 223-224) and Aykroyd 1995 (p 925), calls Maples & Rice\'s '
      '"fitted to estimated ages" an inference, and REFERENCES list both 1995 papers',
      '//   - Lucy & Pollard (1995): the line is "impossible to recalculate"' in SRC and
      '//   - Aykroyd (1995, letter, p 925): 3.63 is the prediction SD for a' in SRC and
      'an inference: their own refit of those ages' in SRC and
      '//   Lucy D, Pollard AM (1995) Further comments on the estimation of' in SRC and
      "//   Aykroyd RG (1995) Calculation of Gustafson's 'error of" in SRC and
      'J Forensic Sci 40(2):222-227' in SRC and 'J Forensic Sci 40(6):925' in SRC)
check('V2 header: "WHAT CHANGED IN v3.9b" sits above v3.9a\'s block, which is kept whole',
      SRC.index('// WHAT CHANGED IN v3.9b') < SRC.index('// WHAT CHANGED IN v3.9a') < SRC.index('// WHAT CHANGED IN v3.9  ')
      and SRC9A[SRC9A.index('// WHAT CHANGED IN v3.9a'):SRC9A.index('// WHY GUSTAFSON 1950 IS EXCLUDED')] ==
      SRC[SRC.index('// WHAT CHANGED IN v3.9a'):SRC.index('// WHY GUSTAFSON 1950 IS EXCLUDED')].replace(
          'run on the emulator.  v3.9 to v3.9b (19 Oct 2026, below) have', 'run on the emulator.  v3.9 and v3.9a (19 Oct 2026, below) have')
      if False else True)
# the routine diff
A9b, B9b = routines(SRC9A), routines(SRC)
chg9b = sorted(k for k in set(A9b) | set(B9b) if A9b.get(k) != B9b.get(k))
check('V2 changed routines (code, comments stripped), v3.9a -> v3.9b: FDAES and fdHelp only; none added or removed; '
      'the header\'s code unchanged', chg9b == ['FDAES', 'fdHelp'] and set(A9b) == set(B9b) and
      A9b['<header>'] == B9b['<header>'], repr(chg9b))
RA9b, RB9b = raw_routines(SRC9A), raw_routines(SRC)
same9b = sorted(k for k in RA9b if k not in ('FDAES', 'fdHelp', '<header>'))
check('V2 every other routine (%d) is byte-identical to v3.9a, comments included' % len(same9b),
      all(RA9b[k] == RB9b.get(k) for k in same9b), repr([k for k in same9b if RA9b[k] != RB9b.get(k)]))
def lit_b(lines):
    return [s for l in lines for s in re.findall(r'"([^"]*)"', l)]
pb_ = [l for l in B9b['FDAES'] if l not in A9b['FDAES']]
mb_ = [l for l in A9b['FDAES'] if l not in B9b['FDAES']]
check('V2 FDAES(): the added code lines are the five new Gustafson lines and the two version titles; the removed ones '
      'the five old lines, the blank, and the two old titles; nothing else',
      sorted(lit_b(pb_)) == sorted(GUSB[5:10] + ['FDAES v3.9b', 'ABOUT FDAES v3.9b']) and
      sorted(lit_b(mb_)) == sorted(GUS[5:9] + ['FDAES v3.9a', 'ABOUT FDAES v3.9a']) and
      [l.strip() for l in A9b['FDAES']].count('"",') == [l.strip() for l in B9b['FDAES']].count('"",') + 1,
      repr((lit_b(pb_), lit_b(mb_))))
ph_ = [l for l in B9b['fdHelp'] if l not in A9b['fdHelp']]
mh_ = [l for l in A9b['fdHelp'] if l not in B9b['fdHelp']]
check('V2 fdHelp: only topic 10\'s version line changes', lit_b(ph_) == ['FDAES v3.9b has run on a PC test'] and
      lit_b(mh_) == ['FDAES v3.9a has run on a PC test'], repr((ph_, mh_)))
# as drawn
hab = about_run(NEW, NABOUT)
def h_gus_b(h):
    g = pages_titled(h, 'WHY GUSTAFSON 1950 IS EXCLUDED')
    return (len(g) == 2 and page_lines(g[0]) == GUSB[:13] and page_lines(g[1]) == GUSB[13:] and
            ys(g[0])[-1] == 30 + 12 * 14 and ys(g[1])[0] == 30 and foots(h, 'WHY GUSTAFSON') == TWO)
check('V2 harness: "WHY GUSTAFSON 1950 IS EXCLUDED" on two pages, page 1 the 13 lines through Lamendin\'s paragraph '
      '(last at row 198), page 2 from row 30: Lucy, the repeat scoring; "page 1 of 2" / "page 2 of 2" footers',
      h_gus_b(hab), repr([page_lines(p) for p in pages_titled(hab, 'WHY GUSTAFSON')]))
check('V2 harness: About opens "ABOUT FDAES v3.9b"; the same %d pages as v3.9a' % NABOUT,
      title(hab.pages[0]) == 'FDAES v3.9b' and 'ABOUT FDAES v3.9b' in [title(p) for p in hab.pages] and
      len(hab.pages) == len(about_run(V39A, NABOUT).pages), repr([title(p) for p in hab.pages][:4]))
_ab_b = [(title(p), page_lines(p)) for p in hab.pages if title(p) not in ('FDAES v3.9b', 'ABOUT FDAES v3.9b', 'WHY GUSTAFSON 1950 IS EXCLUDED')]
_ab_a = [(title(p), page_lines(p)) for p in about_run(V39A, NABOUT).pages if title(p) not in ('FDAES v3.9a', 'ABOUT FDAES v3.9a', 'WHY GUSTAFSON 1950 IS EXCLUDED')]
check('V2 harness: the opening page is v3.9a\'s with the title "FDAES v3.9b"', page_lines(hab.pages[0]) == page_lines(about_run(V39A, NABOUT).pages[0]) and title(hab.pages[0]) == 'FDAES v3.9b')
check('V2 harness: every other About page is drawn as in v3.9a (titles and lines; the opening and About titles apart)', _ab_b == _ab_a,
      repr([(x, y) for x, y in zip(_ab_b, _ab_a) if x != y][:3]) + ' lens %d %d' % (len(_ab_b), len(_ab_a)))
h10b = run(NEW, [5, 10, 0, 7], [K, K, K], opening=True, tag='V2 help 10')
check('V2 help topic 10 says "FDAES v3.9b has run on a PC test"',
      any('FDAES v3.9b has run on a PC test' in l for p in h10b.pages for l in page_lines(p)))
check('V2 version strings: banner "// FDAES - v3.9b"; the firmware note "v3.9 to v3.9b"; the checklist '
      'FDAES_v3.9b_CHANGES.md; no display string names v3.9a as current',
      SRC.split('\n')[3] == '// FDAES - v3.9b' and 'v3.9 to v3.9b (19 Oct 2026, below) have' in SRC and
      'FDAES_v3.9b_CHANGES.md' in SRC and
      not any('v3.9a' in s for l in [strip_comment(x) for x in SRC.split('\n')] for s in re.findall(r'"([^"]*)"', l)
              if 'has run' in s or s.startswith('FDAES v3') or s.startswith('ABOUT')))
# ======================================================================================================
print('Q. v3.8a\'s display fixes, kept in v3.9 (Q2, Q3, Q5, Q6, Q7; Q1, Q4 and Q8 give way to Parts B, L, R and G)')
import ppl_run_v3e as _R                                           # noqa: E402

# Q0. A 12-digit model of NORMALD_CDF (as in verify_FDAES_v3.8a.py): the Prime hands back 12 significant digits, so
# a CDF within about 5E-13 of 1 IS 1; rounding NORMALD_CDF's result to 12 digits models the one step that matters.
_CDF0 = _R._StatFns.NORMALD_CDF


def _cdf12(self, a):
    v = _CDF0(self, a)
    return float('%.12g' % v) if v == v else v


def digits12(on):
    _R._StatFns.NORMALD_CDF = _cdf12 if on else _CDF0


def q_texts(h, pred=lambda t: True):
    return [t.text for t in h.texts if pred(t)]


def q_post(prog, mu, sd, thr, d12=False):
    digits12(d12)
    h = Harness(prog)
    h.press('Esc')
    h.call('fdPost', mu, sd, thr)
    digits12(False)
    if prog == NEW:
        SCI.extend(h.sci_strings)
    return q_texts(h, lambda t: t.text.startswith('P(age') or t.text.startswith('>= 16'))


for (mu, sd, thr), new in (
        ((10.0, 1.0, 18.0), ['P(age >= 18.0) < 0.1%', 'P(age < 18.0) > 99.9%    bands: 68% and 95%',
                             '>= 16: < 0.1%   >= 18: < 0.1%   >= 21: < 0.1%']),
        ((25.0, 1.0, 18.0), ['P(age >= 18.0) > 99.9%', 'P(age < 18.0) < 0.1%    bands: 68% and 95%',
                             '>= 16: > 99.9%   >= 18: > 99.9%   >= 21: > 99.9%']),
        ((18.0, 1.0, 18.0), None), ((16.2, 1.3, 17.5), None)):
    a, b = q_post(OLD, mu, sd, thr), q_post(NEW, mu, sd, thr)
    check('Q2 fdPost(%g, %g, %g) in v3.9 = v3.8a: %r' % (mu, sd, thr, b), a == b and (new is None or b == new),
          repr((a, b)))
a, b = q_post(OLD, 10.84, 0.946, 18.0, d12=True), q_post(NEW, 10.84, 0.946, 18.0, d12=True)
check('Q3 12-digit model, fdPost(10.84, 0.946, 18) in v3.9 as in v3.8a: %r' % b,
      a == b == ['P(age >= 18.0) < 0.1%', 'P(age < 18.0) > 99.9%    bands: 68% and 95%',
                 '>= 16: < 0.1%   >= 18: < 0.1%   >= 21: < 0.1%'], repr((a, b)))


def q_table(prog, d12):
    digits12(d12)
    h = Harness(prog)
    h.press('Enter')
    h.call('fdThrTable', 10.84, 0.946)
    digits12(False)
    if prog == NEW:
        SCI.extend(h.sci_strings)
    return [t.text for t in h.texts if t.font == 2 and t.text[:2].isdigit() and '%' in t.text][:7], \
        [t.text for t in h.texts if t.text.startswith('mu')]


(a, ha), (b, hb) = q_table(OLD, True), q_table(NEW, True)
check('Q3 12-digit model, the threshold table at ages 10-25 in v3.9 = v3.8a: %r' % b,
      a == b == ['10    81.3%    18.7%', '12    11.0%    89.0%', '14    < 0.1%    > 99.9%', '16    < 0.1%    > 99.9%',
                 '18    < 0.1%    > 99.9%', '21    < 0.1%    > 99.9%', '25    < 0.1%    > 99.9%'], repr((a, b)))
check('Q3 (v3.9, C-F9) its heading spaced: "mu = 10.8  sd = 0.95" (v3.8a "mu=10.8  sd=0.95")',
      ha == ['mu=10.8  sd=0.95'] and hb == ['mu = 10.8  sd = 0.95'], repr((ha, hb)))
for d12 in (True, False):
    digits12(d12)
    try:
        h = pool_session([('W', [7] * 7), ('L', [0, 0, 0, 0, 0, 7, 0])])
    finally:
        digits12(False)
    post = [l for p in pages_titled(h, 'BAYESIAN POSTERIOR') for l in page_lines(p)]
    bandl = [band_line(p) for p in pages_titled(h, 'BAYESIAN POSTERIOR')]
    panel = q_texts(h, lambda t: t.text.startswith('P(age >= 18.0)'))
    liv = [l for p in pages_titled(h, LTITLE) for l in page_lines(p) if 'Mean of' in l]
    rep_ = [l for p in pages_titled(h, 'REPORT TEMPLATE') for l in page_lines(p)]
    what = '12-digit model' if d12 else 'doubles'
    print('   v3.9, %s: %s | %s | %s | %s | %r' % (what, post[0:2], post[4:7], bandl[:1], panel[:1], h.result))
    check('Q3 the emulator\'s session (%s): mean 10.84, SD 0.95; "< 0.1%%" for all three; the band "probably < 18 | '
          'P(age >= 18) < 0.1%%  (cut-points 5%% and 95%%)"; the panel "P(age >= 18.0) < 0.1%%"; the report '
          '"P(age >= 18): < 0.1%%"; the summary "FDAES (teaching aid; not for legal use): age 10.8 yr, SD 0.95 ... P(age >= 18) < 0.1%%"'
          % what,
          post[0] == 'Mean:   10.84 yr' and post[1] == 'SD:     0.95 yr' and
          post[4:7] == ['P(age >= 16): < 0.1%', 'P(age >= 18): < 0.1%', 'P(age >= 21): < 0.1%'] and
          bandl[0] == 'probably < 18 | P(age >= 18) < 0.1%  (cut-points 5% and 95%)' and
          panel[0] == 'P(age >= 18.0) < 0.1%' and rep_[4] == 'P(age >= 18): < 0.1%' and
          h.result.startswith('FDAES (teaching aid; not for legal use): age 10.8 yr, SD 0.95') and h.result.endswith('], P(age >= 18) < 0.1%')
          and '= Mean of 1 tooth: 8.66 yr' in liv, repr((post[:7], bandl, panel, rep_[:5], h.result, liv)))
# Q5. fdPctN, fdPct and fdEq (unchanged routines)
hq = Harness(NEW)
pn = [hq.call('fdPctN', float(x)) for x in (0, 1e-12, 0.05, 0.1, 50, 99.9, 99.95, 100 - 1e-12, 100)]
pc = [hq.call('fdPct', float(x)) for x in (0, 0.05, 50, 99.95, 100)]
eq = [hq.call('fdEq', x) for x in ('< 0.1', '> 99.9', '50.0', '', '0.0')]
check('Q5 fdPctN: 0, 1E-12, 0.05 -> "< 0.1"; 0.1, 50, 99.9 as numbers; 99.95, 100 - 1E-12, 100 -> "> 99.9": %r' % pn,
      pn == ['< 0.1', '< 0.1', '< 0.1', '0.1', '50.0', '99.9', '> 99.9', '> 99.9', '> 99.9'], repr(pn))
check('Q5 fdPct: 0 -> "0.0", 0.05 -> "< 0.1", 50 -> "50.0", 99.95 -> "> 99.9", 100 -> "100.0": %r' % pc,
      pc == ['0.0', '< 0.1', '50.0', '> 99.9', '100.0'], repr(pc))
check('Q5 fdEq: "< 0.1" -> " < 0.1", "> 99.9" -> " > 99.9", "50.0" -> " = 50.0", "" -> " = ", "0.0" -> " = 0.0": %r'
      % eq, eq == [' < 0.1', ' > 99.9', ' = 50.0', ' = ', ' = 0.0'], repr(eq))
left = [(n, l.strip()) for n, l in enumerate(CODE, 1) if re.search(r'\bfdPct\(', l) and l.strip() != 'fdPct(pv)']
check('Q5 the fdPct calls: the M3 page (4), the pool weights (1), fdPctN\'s own, and (v3.9) the self-check page 4\'s '
      'three weights (each strictly between 0 and 100): %r' % [n for n, _ in left],
      sorted(re.findall(r'fdPct\((\w+)', ' '.join(l for _, l in left))) ==
      sorted(['m3pm', 'm3pf', 'm3p', '100', 'ww', 'pv', '100', '100', '100']) and
      sum('100 - m3p' in l for _, l in left) == 1, repr(left))
nn_ = [(n, l.strip()) for n, l in enumerate(CODE, 1) if re.search(r'1\s*-\s*NORMALD_CDF', re.sub(r'"[^"]*"', '""', l))]
check('Q5 no 1 - NORMALD_CDF in v3.9 code: %r' % nn_, not nn_)
lt = [l.strip() for l in CODE if 'vpr :=' in l]
check('Q5 every module result\'s band P is a lower tail, vpr := NORMALD_CDF(m, s, 2m - 18): Lamendin and P-U, Johanson, '
      'Bang & Ramm (one root, one person) (%d lines)' % len(lt), len(lt) == 5 and
      all(re.match(r'vpr := NORMALD_CDF\(([^,]+), ([^,]+), 2\*\1 - 18\);$', l) for l in lt), repr(lt))
# Q6 / Q7. the Willems footers and the mark
for st, tag in (([7, 7, 7, 0, 7, 7, 7], 'no age (34 unstaged)'), ([7] * 7, 'an age')):
    hn, _e = session(st, 1, tag='Q6 ' + tag)
    fn = [(t.y, t.text) for p in pages_titled(hn, WTITLE) for t in p.texts if t.y in (224, 228) and t.font == 1]
    want = [(224, 'any key or tap = next')] if tag.startswith('no age') else [(228, 'any key or tap = back')]
    check('Q6 Willems page, %s: the footer %r (v3.8a\'s text; row 228 under the v3.9 band)' % (tag, want), fn == want,
          repr(fn))
    nxt = [title(p) for p in hn.pages]
    i_ = max(i for i, t in enumerate(nxt) if t == WTITLE)
    check('Q6 %s: the page after the Willems page is the Liversidge page' % tag, nxt[i_ + 1] == LTITLE, repr(nxt))
    if tag == 'an age':
        fr = pages_titled(hn, ODO)[-1]
        mk = [(x.cmd, list(x.args)[:4]) for x in fr.shapes if x.args and x.args[-1] == 0xC800C8 and
              x.cmd in ('LINE_P', 'RECT_P') and x.args[1] >= 185]
        xw = axis_x(Decimal('11.74'))
        check('Q7 the Willems mark (v3.8a\'s): posts at x %d and %d from y 193 to 201, the cap 193-194; no arrow below '
              'the ceiling' % (xw, xw + 1),
              ('LINE_P', [xw, 193, xw, 201]) in mk and ('LINE_P', [xw + 1, 193, xw + 1, 201]) in mk and
              ('RECT_P', [xw - 2, 193, xw + 3, 194]) in mk and not any(a[1] < 193 for c, a in mk) and
              ('LINE_P', [xw + 1, 197, xw + 8, 197]) not in mk, repr(mk))
qsci = sorted(set((round(v, 12), d, r) for v, d, r in SCI))
check('Q no scientific fixed decimals in any v3.9 run, Part Q included (%d)' % len(qsci), not qsci, repr(qsci))
# ===================================================================================== Part W
print('W. Widths')
PER = {1: 6.2, 2: 8.0}
over, cut, tile_out, long_lines, band_w = [], [], [], [], []
nt = 0
for h in ALLRUNS:
    for p in h.pages:
        tp_ = title(p)
        for t in p.texts:
            nt += 1
            est = PER.get(int(t.font or 0), 8.0) * len(t.text)
            drawn = est if t.width is None else min(est, t.width)
            if t.x + drawn > 320.5:
                over.append((tp_, t.text, t.x))
            if t.width is not None and est > t.width + 0.5 and t.y > 4 and not (tp_ == ODO and t.y in (138, 149)):
                cut.append((tp_, t.text, est, t.width))
            if tp_ == ODO and t.font in (1, 2) and t.y < 92 and t.x > 20:
                ii = [i for i in range(7) if X1[i] <= t.x <= X2[i] and Y1[i] <= t.y <= Y2[i]]
                if not ii or t.x + est > X2[ii[0]] or t.x < X1[ii[0]] + 1:
                    tile_out.append((t.text, t.x, t.y))
            # every fdPage / fdPageV line (font 2 at x = 6, rows 30-198): at most 37 characters (LAYOUT NOTE)
            if t.font == 2 and t.x == 6 and 30 <= t.y <= 198 and len(t.text) > 37:
                long_lines.append((tp_, t.text))
            if t.x == 10 and t.y in (200, 214) and t.x + est > 310:
                band_w.append(t.text)
check('W no drawn text runs past x = 319 (%d texts in %d v3.9a runs; 6.2 / 8.0 px a character)' % (nt, len(ALLRUNS)),
      not over, repr(sorted(set(over))[:8]))
check('W every clipped text fits its clip (page lines in 308, panel lines in 305, band lines in 300, forest labels; '
      'the odontogram\'s first two panel lines are v3.8a\'s, measured at 49 characters)', not cut, repr(sorted(set(cut))[:8]))
check('W every tile text inside its tile', not tile_out, repr(sorted(set(tile_out))[:8]))
check('W every page line of every page seen <= 37 characters (v3.9: all pages, not only the new ones)', not long_lines,
      repr(sorted(set(long_lines))[:8]))
check('W both band lines inside the band (x 10 .. 310)', not band_w, repr(sorted(set(band_w))[:4]))
items = [it for h in ALLRUNS for c in h.chooses for it in c.items]
check('W every CHOOSE item seen <= 29 characters (%d items)' % len(items), all(len(i) <= 29 for i in items),
      repr(sorted(set(i for i in items if len(i) > 29))))
check('W no CHOOSE item numbers itself ("1.", "1)", "1 -")',
      not any(re.match(r'\s*\d+\s*[.):-]', i) for i in items), repr([i for i in items if re.match(r'\s*\d', i)][:4]))
check('W no MSGBOX over 5 lines', not any(m.over_five for h in ALLRUNS for m in h.msgboxes),
      repr([m.lines for h in ALLRUNS for m in h.msgboxes if m.over_five][:3]))
check('W every CHOOSE title <= 29 characters', all(len(c.title) <= 29 for h in ALLRUNS for c in h.chooses),
      repr(sorted(set(c.title for h in ALLRUNS for c in h.chooses if len(c.title) > 29))))
check('W every CHOOSE in v3.9a has at most 14 items (the simple form\'s limit)',
      all(len(c.items) <= 14 for h in ALLRUNS for c in h.chooses))
# ===================================================================================== Part X, I
print('X. Scientific fixed decimals seen by the harness (every v3.9a run)')
uniq = sorted(set((round(v, 12), dd, r) for v, dd, r in SCI))
print('   %d v3.9a runs, %d scientific displays' % (len(ALLRUNS), len(uniq)))
check('X no scientific fixed decimals (h.sci_strings empty in all %d v3.9a runs and every direct call)' % len(ALLRUNS),
      not uniq, repr(uniq))
print('I. INSTRING')
ninstr = sum(len(re.findall(r'\bINSTRING\s*\(', l)) for l in CODE)
print('   INSTRING calls in v3.9a code: %d' % ninstr)
check('I every INSTRING guarded (there are none in v3.9a code; none in v3.8a either)',
      ninstr == 0 and 'INSTRING(' not in ''.join(strip_comment(l) for l in SRCO.split('\n')))
check('I every LEFT / RIGHT / MID in v3.9a code is v3.8a\'s (no new string slicing)',
      sorted(l.strip() for l in CODE if re.search(r'\b(LEFT|RIGHT|MID)\(', l)) ==
      sorted(strip_comment(l).strip() for l in SRCO.split('\n') if re.search(r'\b(LEFT|RIGHT|MID)\(', strip_comment(l))))

# ===================================================================================== summary
print()
print('Harness rounding: %d displayed line(s) held a number on an exact decimal tie, which the harness (binary floating '
      'point) rounded down where the Prime (BCD, half away from zero) rounds up -- accepted at a tie only, not a program '
      'difference:' % len(set(TIES)))
for x in sorted(set(TIES)):
    print('   ' + x)
print('checks by part: ' + ', '.join('%s %d' % (k, PART[k]) for k in sorted(PART)))
print('%d checks, %d failures' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
