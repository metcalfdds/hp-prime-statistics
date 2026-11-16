# -*- coding: utf-8 -*-
"""Round 16 (15 Nov 2026): RankLab beta 1j from beta 1i, by exact replacements (a miss stops the build).

New in beta 1j (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please"; the fifth and sixth):
  * PAGE'S L, the test for an ORDERED trend across the treatments of a Friedman layout (main menu item 9): L = sum j R_j
    over the treatments in the order listed; z without a continuity correction; the EXACT p by convolving the blocks'
    own null distributions, a block with ties by walking all the orders of its own midranks (the exact conditional
    distribution of Hollander, Wolfe & Chicken, section 7.2, Comment 19), when a step budget of 60,000 allows it;
    Rising / Falling on the fifth soft key; a picture of the mean ranks in order; the mean Spearman rs with the order.
  * THE RUNS TEST for the randomness of a sequence of two kinds (main menu item A): the runs counted, the exact p from
    the number of orders with that many runs (in logs, n <= 2,000), z without a continuity correction as the HP-65
    Stat Pac 2 printed it in 1975; the sequence as squares, and for numbers (cut at their median) a run chart.
  * FOUR PRESETS: ozone and airway resistance (Goldsmith & Nadel 1969, Roger's own 2021 homework data), the 1970
    draft lottery's months in order (days 1-28 as blocks), the HP-65's roulette example, the lottery's runs by day.
  * A FAULT MENDED: the Null page wrote "U1 = infinite" (or "T+ = infinite") when the statistic reached 100,000, as
    Mann-Whitney's U does with two groups of 500; the word belongs to Spearman's t of a perfect order only.
  * Help: 10 pages (7 before).
Written from the formulas; what was read is in the program's header.  Every other screen is beta 1i's.
Run from the repository's root:   python3 verify/round16/make_ranklab_1j.py OUTDIR
"""
import io, itertools, collections, json, math, os, re, subprocess, sys, textwrap
BASE = '4e8ff66'; DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r16_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/RankLab_beta1i.txt'], check=True, capture_output=True).stdout.decode('utf-8')
GW = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'round11', 'glyph_widths_vc.json')))


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)


def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)
def px(t, font=1): return sum((GW.get(str(ord(ch))) or [8, 9, 10])[font - 1] for ch in t)


# ---------------- the one-block null of Page's L, k = 3..9: counted here, never typed ----------------
def one_block(k):
    c = collections.Counter()
    for p in itertools.permutations(range(1, k + 1)):
        c[sum((j + 1) * p[j] for j in range(k))] += 1
    lo = k * (k + 1) * (k + 2) // 6; hi = k * (k + 1) * (2 * k + 1) // 6
    v = [c.get(x, 0) for x in range(lo, hi + 1)]
    assert sum(v) == math.factorial(k) and v == v[::-1] and len(v) == (k - 1) * k * (k + 1) // 6 + 1
    return v


def ppl_list(v, indent='      ', per=14):
    rows = [', '.join(str(x) for x in v[i:i + per]) for i in range(0, len(v), per)]
    return '{' + (',\n' + indent).join(rows) + '}'


LONE = ''.join('  IF loK == %d THEN\n    RETURN %s;\n  END;\n' % (k, ppl_list(one_block(k))) for k in range(3, 10))

# the largest number of blocks whose exact null is counted when no block has ties: the program's own rule, done here in
# whole numbers so that the header and the help page say what the program does (the verify script runs it in the harness)
BUDGET = 60000
def cost(b, k, tied=0, alltied=0):
    w = (k - 1) * k * (k + 1) // 6
    if tied > 0: w *= 2
    w += 1
    return w * ((w - 1) * b * (b - 1) // 2 + b) + (tied - alltied) * math.factorial(k) * 8
LIM = {k: max(b for b in range(2, 400) if cost(b, k) <= BUDGET) for k in range(3, 10)}
LIMT = {k: max([b for b in range(2, 400) if cost(b, k, 1) <= BUDGET] or [0]) for k in range(3, 10)}   # one block with ties

# ---------------- header ----------------
rep('// RANKLAB - beta 1i  (15 Nov 2026)\n', '// RANKLAB - beta 1j  (15 Nov 2026)\n')
rep('''//     Load a preset                - five real data sets, 7 presets
//     Use my data (D1..D9)         - the Statistics 1Var columns
//     Help, Quit
''', '''//     Load a preset                - seven real data sets, 11 presets
//     Use my data (D1..D9)         - the Statistics 1Var columns
//     Page's L (ordered trend)     - blocks x treatments in an order:
//                                    exact p for a small table (ties
//                                    as they are), else normal
//     Runs test (randomness)       - the order of two kinds of values:
//                                    exact p (n <= 2,000) and normal
//     Help, Quit
''')
rep('''//   approximation), a picture (the rank strip, group boxes, the
//   Friedman rank grid or the rank scatter) and the null distribution
''', '''//   approximation), a picture (the rank strip, group boxes, the
//   Friedman rank grid, the rank scatter, Page's mean ranks in order,
//   the sequence as squares or its run chart) and the null distribution
''')
rep('''//   toggle), Tails, More (Help, Dunn or Data, Menu).  Keys: Up / Down
''', '''//   toggle), Tails (Rising / Falling for Page's L), More (Help; Dunn,
//   Data or Chart; Menu).  Keys: Up / Down
''')
rep('''//   epsilon-squared (Kruskal-Wallis) or W (Friedman).  For rank
''', '''//   epsilon-squared (Kruskal-Wallis), W (Friedman), the mean Spearman
//   rs between each block's ranks and the order (Page's L) or the runs
//   counted over the runs expected (runs test).  For rank
''')
note = ('Round 16 (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please").  Two tests more, '
        'each with its own routines beside the old ones.  PAGE\'S L (main menu item 9; rk_DoPage, rk_LNull, rk_LBlock, '
        'rk_LOne, rk_PgTrend): the Friedman layout with the treatments in an order chosen beforehand; L = sum j R_j; '
        'z without a continuity correction; the exact p by convolving the blocks\' own null distributions when a budget of '
        '60,000 steps allows it (no ties: up to %s blocks for k = 3, 4, ..., 9 treatments), a block with ties by walking '
        'every order of its own midranks, so the exact p is the conditional one (Hollander, Wolfe & Chicken, section '
        '7.2, Comment 19); R\'s PageTest and SciPy\'s method = "exact" give the untied null whatever the data, and with '
        'ties their normal approximation keeps the untied variance (7.13), which Comment 21 calls conservative: here the '
        'variance is the exact conditional one.  Rising / Falling on the fifth soft key.  THE RUNS TEST (main menu item '
        'A; rk_DoRuns, rk_RuNull, rk_RuFrom, rk_PgRuns): the runs of a sequence of two kinds are counted; the exact p '
        'from the number of orders with that many runs, in logs (n <= 2,000); z without a continuity correction; numbers '
        'are cut at their median and a value equal to it is dropped; the picture is one square a value, or for numbers a '
        'run chart.  Four presets (ozone and airway resistance; the 1970 draft lottery\'s months in order and its runs by '
        'day; the HP-65 Stat Pac 2\'s roulette example); two more kinds of "Use my data".  A FAULT MENDED: the Null page '
        'wrote "infinite" for any statistic of 100,000 or more (Mann-Whitney\'s U with two groups of 500); the word is '
        'for Spearman\'s t of a perfect order only, and Left / Right now starts at the statistic there too.  The Null '
        'page\'s last axis number is kept on the screen (it ran off it for a statistic in the hundred thousands).  Your data: a table '
        'of more than 10,000 values is refused with a sentence (one list holds it).  Help has 10 pages (7 before).  Every old menu item keeps its '
        'number.  PC harness only so far.' % ', '.join(str(LIM[k]) for k in range(3, 10)))
before('// beta 1i (15 Nov 2026): Round 15', '// beta 1j (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')
before('''//   Chi-square upper tails for whole df as sums of positive terms
''', '''//   Page's L (beta 1j): Page (1963) JASA 58:216, "Ordered hypotheses for
//     multiple treatments: a significance test for linear ranks"; as
//     Hollander, Wolfe & Chicken (2014) give it, section 7.2: L (7.10),
//     its mean b k (k+1)^2/4 (7.12) and untied variance
//     b k^2 (k+1)(k^2-1)/144 (7.13), z without a continuity correction
//     (7.14); the exact conditional distribution with ties (Comment
//     19); the mean Spearman rs with the order (Comment 22).  With
//     ties the variance here is the exact conditional one, the sum
//     over the blocks of k (k+1) (k (k^2-1) - sum(t^3 - t))/144 (the
//     variance of a linear rank statistic over the orders of one
//     block), which their Comment 21 calls the more proper one.
//     Odeh (1977) Commun. Stat. Simul. Comput. 6:49 tabled the exact
//     distribution; SciPy's page_trend_test (its exact p is not
//     adjusted for ties) is the check in the verify script.
//   Runs test (beta 1j): the number of orders with a given number of
//     runs: Stevens (1939) Ann. Eugenics 9:10; Wald & Wolfowitz (1940)
//     Ann. Math. Stat. 11:147; tables: Swed & Eisenhart (1943) Ann.
//     Math. Stat. 14:66.  Mean 2 n1 n2/n + 1, variance
//     2 n1 n2 (2 n1 n2 - n)/(n^2 (n - 1)).  Numbers are cut at their
//     median and a value equal to it is dropped, as R's randtests
//     runs.test does.  z without a continuity correction, as the HP-65
//     Stat Pac 2 (1975) prints it.
''')
before('''// Does on the Prime what these TI-83/84 programs do.  They were read to
''', '''//   Ozone (beta 1j): the change in airway resistance (cm H2O/l/s) of
//     four men after an hour at 0.1, 0.6 and 1.0 ppm of ozone -
//     Goldsmith & Nadel (1969) J. Air Pollution Control Assoc. 19:329,
//     the subset in Hollander, Wolfe & Chicken (2014) Table 7.2.
//   Roulette (beta 1j): 25 spins, red or black (0 and 00 left out),
//     R R R R B R R R B B B B B R R B B B R R B B R R R - the example
//     of "The Run Test for Randomness", HP-65 Stat Pac 2 (Hewlett-
//     Packard, 1975), Stat 2-22A, p. 86, kept in the HP-67/HP-97
//     Users' Library Solutions book "Test Statistics", p. 29.
''')
before('''// File map: see the FILE MAP block just below the Home exports.
''', '''// The runs test (beta 1j) does what Hewlett-Packard's "Run Test for
//   Randomness" did on the HP-65 (Stat Pac 2, 1975, Stat 2-22A) and,
//   translated, on the HP-67/HP-97 (Users' Library Solutions: Test
//   Statistics) and the HP-41C (RUNTEST).  Those take the two counts and
//   the number of runs, keyed in, and return the mean, the standard
//   deviation and z (for small samples they send the user to
//   printed tables).  RankLab counts the runs from the sequence itself and adds
//   the exact p and the pictures.  Their pages were read to see what the
//   programs compute; this one is written new in PPL from the formulas,
//   and none of their code is in it.  Page's L is written from
//   the formulas above; no other program was read for it (the library in
//   D:\\HP-Prime holds no program with Page's L or, beyond those HP
//   keystroke programs, a runs test; searched 15 Nov 2026).
''')

# ---------------- the state ----------------
rep('''//  rkTest 1 sign, 2 signed-rank, 3 Mann-Whitney, 4 Kruskal-Wallis,
//  5 Friedman, 6 rank correlation.  rkTail 0 two-sided, 1 lower,
//  2 upper.  rkMode 1 = exact (when there is one), 0 = normal.
''', '''//  rkTest 1 sign, 2 signed-rank, 3 Mann-Whitney, 4 Kruskal-Wallis,
//  5 Friedman, 6 rank correlation, 7 Page's L, 8 the runs test (7 and
//  8: beta 1j).  rkTail 0 two-sided, 1 lower, 2 upper (Page's L: 2 =
//  rising, 1 = falling, never 0).  rkMode 1 = exact (when there is
//  one), 0 = normal.
''')
after('''//  rkDone = 1 once a test has run (for the Quit summary).
''', '''
// ---- beta 1j: Page's L and the runs test ----
LOCAL rkLDir, rkLSel, rkLNt, rkUSq, rkUVal, rkUN1;
LOCAL rkUN2, rkUNmA, rkUNmB, rkUCl, rkUSrc, rkULab;
LOCAL rkUHas, rkUCut, rkUDrop, rkURun, rkUSt, rkUSel;
LOCAL rkUCh, rkULong, rkULk, rkULs, rkUC, rkUPer;
LOCAL rkUY0;
//  Page's L (rkTest 7) works on the Friedman data (rkFM, rkFB, rkFK,
//  the names, rkFR, rkFRS).  rkLDir: the direction a data set is tested
//  in when Page's L opens on it (2 = rising, the upper tail of L; 1 =
//  falling).  rkLSel: the treatment picked on its picture.  rkLNt: how
//  many blocks have ties.
//  The runs test (rkTest 8).  rkUSq: the sequence, 1 or 2 for each
//  place, in order.  rkUVal: the numbers behind it ({} when the two
//  kinds were given as they are).  rkUN1, rkUN2: how many of each
//  kind; rkUNmA, rkUNmB their names; rkUCl their two colors.  rkUCut:
//  the median the numbers were cut at; rkUDrop: how many values equal
//  to it were dropped.  rkURun: the run each place belongs to; rkUSt:
//  the place each run starts at (rk_RuEnd gives where it ends).
//  rkUSel: the place picked.  rkUCh = 1: the picture is the run chart,
//  0: the squares.  rkULong, rkULk, rkULs: the longest run's length,
//  its kind and its first place.  rkUC, rkUPer, rkUY0: the squares'
//  pitch, how many go in a row, and the top of the first row.
''')
after('''  rkSpK := 0; rkKdK := 0; rkPSp := -1; rkPKd := -1;
''', '''  // beta 1j: Page's L and the runs test
  rkLDir := 2; rkLSel := 1; rkLNt := 0;
  rkUHas := 0; rkUSq := {}; rkUVal := {}; rkUN1 := 0; rkUN2 := 0;
  rkUNmA := ""; rkUNmB := ""; rkUCl := {rkBLUE, #E07800h};
  rkUSrc := ""; rkULab := ""; rkUCut := 0; rkUDrop := 0;
  rkURun := {}; rkUSt := {}; rkUSel := 1; rkUCh := 0;
  rkULong := 0; rkULk := 1; rkULs := 1;
  rkUC := 12; rkUPer := 25; rkUY0 := 50;
''')
rep('''  IF rkTest == 4 OR rkTest == 5 THEN RETURN "upper tail"; END;
  IF rkTail == 1 THEN RETURN "lower tail"; END;
''', '''  IF rkTest == 4 OR rkTest == 5 THEN RETURN "upper tail"; END;
  // beta 1j: Page's L is read in a direction (the upper tail of L = rising)
  IF rkTest == 7 THEN RETURN IFTE(rkTail == 1, "falling", "rising"); END;
  IF rkTail == 1 THEN RETURN "lower tail"; END;
''')

# ---------------- the arithmetic of the two tests ----------------
before('''// rk_Pick: the p-values for the tail chosen, and the Home exports.
''', r'''// ---------------- 7. PAGE'S L (beta 1j) ----------------
// Page (1963): the Friedman layout (blocks x treatments, ranks within
// each block), but H1 says more than "they differ": the treatments
// RISE in the order they are listed.  L = sum_j j R_j, where R_j is
// treatment j's rank sum, so a block whose ranks follow the order adds
// the most.  Under H0 every order of a block's ranks is equally likely
// (Hollander, Wolfe & Chicken 2014, section 7.2):
//   mean      b k (k+1)^2 / 4                                   (7.12)
//   variance  the sum over the blocks of
//             k (k+1) (k (k^2 - 1) - T_i) / 144,
//             T_i = that block's sum(t^3 - t)
//             (no ties: b k^2 (k+1)(k^2 - 1)/144, their 7.13)
//   z = (L - mean)/SD, with NO continuity correction             (7.14)
// The variance of sum_j a_j r_s(j) over the k! orders s of one block is
// sum(a - abar)^2 sum(r - rbar)^2/(k - 1); with a_j = j and the block's
// midranks r that is the line above: the exact conditional variance,
// which their Comment 21 calls the more proper one with ties (7.13
// left as it is, as SciPy leaves it, is larger, so its z is smaller).
// "Falling" is the same test read in the lower tail of L.
// The effect shown is their Comment 22: the mean, over the blocks, of
// Spearman's rs between a block's ranks and the order 1..k (a block
// that ties everything has no rs and is left out of that mean).

// rk_LOne: how many of the k! orders of the ranks 1..k give each value
// of sum j x (rank in place j), from the smallest, k(k+1)(k+2)/6, in
// steps of 1, for k = 3 to 9 ({} for any other k).  The lists were
// counted by the build script from every order (make_ranklab_1j.py),
// not typed; each is the same read from either end, and adds up to k!.
rk_LOne(loK)
BEGIN
@LONE@  RETURN {};
END;

// rk_LBlock: the null distribution of one block's sum when the block has
// ties: every one of the k! orders of its OWN midranks is equally
// likely, so they are all walked, by Heap's algorithm (one swap an
// order, as rk_SpPerm walks Spearman's).  lbA: the block's midranks
// DOUBLED (whole numbers), so the sum is on the doubled scale; a swap
// of places p and q moves it by (p - q)(v(q) - v(p)).  Returns lbW
// probabilities (count / k!) for the sums lbLo, lbLo + 1, ...
rk_LBlock(lbA, lbLo, lbW)
BEGIN
  LOCAL lbK, lbH, lbT, lbV, lbC, lbI;
  LOCAL lbP, lbQ, lbD, lbF;
  lbK := SIZE(lbA);
  lbH := rk_Zeros(lbW);
  lbT := 0; lbF := 1;
  FOR lbI FROM 1 TO lbK DO
    lbT := lbT + lbI * lbA(lbI);
    lbF := lbF * lbI;
  END;
  lbV := lbA;
  lbH(lbT - lbLo + 1) := 1;
  lbC := rk_Zeros(lbK);
  lbI := 1;                                   // Heap's index, counted from 0
  WHILE lbI < lbK DO
    IF lbC(lbI + 1) < lbI THEN
      lbP := 0;
      IF FP(lbI / 2) <> 0 THEN lbP := lbC(lbI + 1); END;
      lbQ := lbI;
      lbT := lbT + (lbP - lbQ) * (lbV(lbQ + 1) - lbV(lbP + 1));
      lbD := lbV(lbP + 1); lbV(lbP + 1) := lbV(lbQ + 1); lbV(lbQ + 1) := lbD;
      lbH(lbT - lbLo + 1) := lbH(lbT - lbLo + 1) + 1;
      lbC(lbI + 1) := lbC(lbI + 1) + 1;
      lbI := 1;
    ELSE
      lbC(lbI + 1) := 0;
      lbI := lbI + 1;
    END;
  END;
  FOR lbI FROM 1 TO lbW DO lbH(lbI) := lbH(lbI) / lbF; END;
  RETURN lbH;
END;

// rk_LNull: the exact null distribution of L.  The blocks are
// independent, so L's distribution is the blocks' distributions
// convolved one after another: a block without ties takes the counted
// list (rk_LOne), a block with ties its own orders (rk_LBlock), a block
// that ties everything adds a constant (its sum is the same in every
// order).  With a tie anywhere the scale is doubled, because L then
// moves in halves.  PROBABILITIES are kept, not counts: (k!)^b passes
// 12 digits at once, while every probability here is a sum of products
// of positive numbers, so a small tail keeps its digits.  lnT: each
// block's sum(t^3 - t).  lnCost: the steps rk_DoPage estimated (a bar is
// shown for a long count; Esc stops it).  Returns 1 with the null in
// rkNull (first value rkNLo, step rkNSt, rkNDen = 1), or 0 after Esc.
rk_LNull(lnT, lnCost)
BEGIN
  LOCAL lnB, lnK, lnSc, lnLo, lnW, lnOne;
  LOCAL lnD, lnI, lnJ, lnBk, lnNew, lnCur;
  LOCAL lnA, lnS, lnV, lnAll, lnM, lnP;
  lnB := rkFB; lnK := rkFK;
  lnSc := 1;
  FOR lnI FROM 1 TO lnB DO
    IF lnT(lnI) > 0 THEN lnSc := 2; END;
  END;
  // one block: its smallest sum and how many values it can take, on the scale
  lnLo := lnSc * lnK * (lnK + 1) * (lnK + 2) / 6;
  lnW := lnSc * (lnK - 1) * lnK * (lnK + 1) / 6 + 1;
  lnM := 1;
  FOR lnI FROM 2 TO lnK DO lnM := lnM * lnI; END;
  // the block without ties, as probabilities on the scale
  lnS := rk_LOne(lnK);
  lnOne := rk_Zeros(lnW);
  FOR lnI FROM 1 TO SIZE(lnS) DO lnOne((lnI - 1) * lnSc + 1) := lnS(lnI) / lnM; END;
  // where an all-tied block's constant sits: every rank is (k+1)/2, so
  // its sum is k (k+1)^2/4, the mean
  lnAll := lnSc * lnK * (lnK + 1)^2 / 4 - lnLo + 1;
  lnD := {1}; lnCur := 1;                     // no block yet: the sum is 0, for sure
  FOR lnBk FROM 1 TO lnB DO
    IF lnCost > 4000 THEN
      rk_Prog(lnBk / lnB, "Exact null of L: block " + rk_Cm(STRING(lnBk, 2, 0)) + " of " + rk_Cm(STRING(lnB, 2, 0)), "Esc = stop (the normal approximation stays)");
      IF rk_Esc() == 1 THEN rkExWhy := "stopped by Esc (normal used)"; RETURN 0; END;
    END;
    IF lnT(lnBk) == 0 THEN
      lnA := lnOne;
    ELSE
      IF lnT(lnBk) == lnK^3 - lnK THEN
        lnA := rk_Zeros(lnW); lnA(lnAll) := 1;
      ELSE
        lnV := rk_Zeros(lnK);
        FOR lnJ FROM 1 TO lnK DO lnV(lnJ) := ROUND(2 * rkFR((lnBk - 1) * lnK + lnJ), 0); END;
        lnA := rk_LBlock(lnV, lnLo, lnW);
      END;
    END;
    // the sums so far (lnD) plus this block's sum (lnA)
    lnNew := rk_Zeros(lnCur + lnW - 1);
    FOR lnJ FROM 1 TO lnW DO
      lnP := lnA(lnJ);
      IF lnP > 0 THEN
        FOR lnI FROM 1 TO lnCur DO
          lnNew(lnI + lnJ - 1) := lnNew(lnI + lnJ - 1) + lnD(lnI) * lnP;
        END;
      END;
    END;
    lnD := lnNew; lnCur := lnCur + lnW - 1;
  END;
  rkNull := lnD; rkNLo := lnB * lnLo / lnSc; rkNSt := 1 / lnSc; rkNDen := 1;
  RETURN 1;
END;

// rk_DoPage: Page's L on the Friedman data.  Everything is worked out
// in locals first, so a refused table changes nothing.
rk_DoPage()
BEGIN
  LOCAL dpB, dpK, dpI, dpJ, dpRow, dpRr;
  LOCAL dpT, dpTs, dpFR, dpRS, dpLi, dpL;
  LOCAL dpVar, dpNt, dpAll, dpW, dpF, dpCost;
  LOCAL dpSr, dpNr, dpD;
  dpB := rkFB; dpK := rkFK;
  IF rkFNoP == 1 THEN
    MSGBOX("The halo preset is a description only (its criteria are not independent raters), so it gets no test.  Load another data set for Page's L.");
    RETURN 0;
  END;
  IF dpK < 3 OR dpB < 2 THEN
    MSGBOX("Page's L needs at least 3 treatments (columns, in the order expected) and 2 blocks (rows).");
    RETURN 0;
  END;
  dpRS := rk_Zeros(dpK); dpFR := rk_Zeros(dpB * dpK);
  dpT := rk_Zeros(dpB); dpLi := rk_Zeros(dpB);
  dpTs := 0; dpNt := 0; dpAll := 0;
  FOR dpI FROM 1 TO dpB DO
    dpRow := rk_Zeros(dpK);
    FOR dpJ FROM 1 TO dpK DO dpRow(dpJ) := rkFM((dpI - 1) * dpK + dpJ); END;
    IF dpB * dpK > 150 AND FP(dpI / 5) == 0 THEN
      rk_Prog(dpI / dpB, "Ranking block " + rk_Cm(STRING(dpI, 2, 0)) + " of " + rk_Cm(STRING(dpB, 2, 0)), "Esc = stop (back to the menu)");
      IF rk_Esc() == 1 THEN rkStop := 1; RETURN 0; END;
    END;
    dpRr := rk_Midrank(dpRow);
    dpT(dpI) := rkTieS; dpTs := dpTs + rkTieS;
    IF rkTieS > 0 THEN dpNt := dpNt + 1; END;
    IF rkTieS == dpK^3 - dpK THEN dpAll := dpAll + 1; END;
    FOR dpJ FROM 1 TO dpK DO
      dpFR((dpI - 1) * dpK + dpJ) := dpRr(dpJ);
      dpRS(dpJ) := dpRS(dpJ) + dpRr(dpJ);
      dpLi(dpI) := dpLi(dpI) + dpJ * dpRr(dpJ);       // this block's share of L
    END;
  END;
  IF dpAll == dpB THEN
    MSGBOX("Every block ties all its treatments: there is no ranking to test.");
    RETURN 0;
  END;
  // nothing refused: the results
  rkFR := dpFR; rkFRS := dpRS;
  dpL := 0;
  FOR dpJ FROM 1 TO dpK DO dpL := dpL + dpJ * dpRS(dpJ); END;
  rkSt := dpL; rkSt2 := 0;
  rkMu := dpB * dpK * (dpK + 1)^2 / 4;
  dpVar := 0;
  FOR dpI FROM 1 TO dpB DO
    dpVar := dpVar + dpK * (dpK + 1) * (dpK * (dpK^2 - 1) - dpT(dpI)) / 144;
  END;
  rkSd := MAX(0, dpVar)^0.5;
  // no continuity correction: one z, whichever the direction
  rkZ2 := (dpL - rkMu) / rkSd; rkZL := rkZ2; rkZU := rkZ2;
  rkN := dpB; rkDf := dpK - 1; rkTieS := dpTs; rkLNt := dpNt;
  rkZero := 0; rkHLok := 0; rkHLv := 0; rkHLWhy := "";
  // the effect: the mean Spearman rs between each block's ranks and the
  // order.  A block's rs = (its share of L - k (k+1)^2/4) / sqrt(Sxx Syy),
  // Sxx = k (k^2-1)/12 for the places, Syy = (k (k^2-1) - T_i)/12
  dpSr := 0; dpNr := 0;
  FOR dpI FROM 1 TO dpB DO
    dpD := dpK * (dpK^2 - 1) - dpT(dpI);
    IF dpD > 0 THEN
      dpSr := dpSr + (dpLi(dpI) - dpK * (dpK + 1)^2 / 4) / ((dpK * (dpK^2 - 1) / 12) * (dpD / 12))^0.5;
      dpNr := dpNr + 1;
    END;
  END;
  rkEff := dpSr / dpNr; rkEff2 := dpNr;
  RK_RANKS := rkFR;
  rkLSel := 1;
  // the exact null, when the table is small enough to count
  rkEx := 0; rkNOK := 0; rkPeL := -1; rkPeU := -1;
  rkNObs := rkSt; rkNMu := rkMu;
  IF dpK > 9 THEN
    rkExWhy := "none for more than 9 treatments (normal)";
  ELSE
    // how many values one block's sum can take (twice as fine with ties)
    dpW := (dpK - 1) * dpK * (dpK + 1) / 6;
    IF dpNt > 0 THEN dpW := 2 * dpW; END;
    dpW := dpW + 1;
    dpF := 1;
    FOR dpJ FROM 2 TO dpK DO dpF := dpF * dpJ; END;
    // the steps the count would take: the convolution, block after
    // block, and every order of each block with ties (8 steps an order)
    dpCost := dpW * ((dpW - 1) * dpB * (dpB - 1) / 2 + dpB) + (dpNt - dpAll) * dpF * 8;
    IF dpCost > @BUDGET@ THEN
      rkExWhy := "none for a table this large (normal)";
    ELSE
      IF rk_LNull(dpT, dpCost) == 1 THEN
        rkPeL := rk_NSum(rkSt, 1);
        rkPeU := rk_NSum(rkSt, 0);
        rkEx := 1; rkNOK := 1; rkExWhy := "";
        rk_NullWin();
      END;
    END;
  END;
  RETURN 1;
END;

// ---------------- 8. THE RUNS TEST (beta 1j) ----------------
// A sequence of two kinds of values, n1 of one and n2 of the other, in
// the order they happened.  A RUN is a stretch of the same kind, and
// "runs" counts them: R R R R B R R R has 3.  Under H0 every one of the
// C(n, n1) orders is equally likely (Stevens 1939; Wald & Wolfowitz
// 1940; tables by Swed & Eisenhart 1943), and the number of orders is
//   runs = 2k:      2 C(n1-1, k-1) C(n2-1, k-1)
//   runs = 2k + 1:  C(n1-1, k) C(n2-1, k-1) + C(n1-1, k-1) C(n2-1, k),
//                   which is the 2k count times (n - 2k)/(2k).
//   mean 2 n1 n2/n + 1,  variance 2 n1 n2 (2 n1 n2 - n)/(n^2 (n - 1)).
// Too FEW runs (the lower tail): like values cluster, as with a drift
// or a trend.  Too MANY (the upper tail): the kinds alternate more than
// chance would.  Two-sided = twice the smaller tail, at most 1 (the
// null is not symmetric unless n1 = n2).  z = (runs - mean)/SD with NO
// continuity correction, as the HP-65 Stat Pac 2 (1975) and the
// textbooks print it.

// rk_RuNull: the exact null of the number of runs.  The counts pass
// 1E499 long before n = 2,000, so each is built in LOGS from its
// neighbor (from 2k to 2k + 2 the count is multiplied by
// (n1 - k)(n2 - k)/k^2) and kept relative to the biggest; rkNDen is
// their sum, so every tail is a sum of positive terms over that sum.
// Entry j of rkNull is for runs = j + 1 (the fewest is 2).  Returns 1,
// or 0 after Esc.
rk_RuNull(ruA, ruB)
BEGIN
  LOCAL ruN, ruKm, ruSz, ruLg, ruE, ruMx;
  LOCAL ruK, ruI, ruS, ruV;
  ruN := ruA + ruB;
  ruKm := MIN(ruA, ruB);
  // the most runs: 2 min(n1, n2) + 1, or one fewer when n1 = n2
  ruSz := 2 * ruKm;
  IF ruA == ruB THEN ruSz := ruSz - 1; END;
  ruLg := rk_Zeros(ruSz);
  ruE := LN(2); ruMx := ruE;                  // runs = 2: two orders
  FOR ruK FROM 1 TO ruKm DO
    IF ruKm > 300 AND FP(ruK / 100) == 0 THEN
      rk_Prog(ruK / ruKm, "Exact null of the runs ...", "Esc = stop (the normal approximation stays)");
      IF rk_Esc() == 1 THEN rkExWhy := "stopped by Esc (normal used)"; RETURN 0; END;
    END;
    // runs = 2k
    IF ruK > 1 THEN ruE := ruE + LN((ruA - ruK + 1) * (ruB - ruK + 1) / (ruK - 1)^2); END;
    ruLg(2 * ruK - 1) := ruE;
    ruMx := MAX(ruMx, ruE);
    // runs = 2k + 1
    IF 2 * ruK <= ruSz THEN
      ruV := ruE + LN((ruN - 2 * ruK) / (2 * ruK));
      ruLg(2 * ruK) := ruV;
      ruMx := MAX(ruMx, ruV);
    END;
  END;
  ruS := 0;
  FOR ruI FROM 1 TO ruSz DO
    ruV := ruLg(ruI) - ruMx;
    IF ruV < -1000 THEN ruLg(ruI) := 0; ELSE ruLg(ruI) := EXP(ruV); END;
    ruS := ruS + ruLg(ruI);
  END;
  rkNull := ruLg; rkNLo := 2; rkNSt := 1; rkNDen := ruS;
  RETURN 1;
END;

// rk_RuEnd: the last place of run r: the place before the next run's
// first, or the sequence's last place for the last run.  (A list of
// the runs' ends would need one entry more than the sequence has
// values, and a list holds 10,000.)
rk_RuEnd(reR)
BEGIN
  IF reR >= rkSt THEN RETURN rkN; END;
  RETURN rkUSt(reR + 1) - 1;
END;

// rk_DoRuns: count the runs of rkUSq and test them.
rk_DoRuns()
BEGIN
  LOCAL duN, duI, duA, duB, duR, duVar;
  LOCAL duRun, duSt, duG, duLen, duBest, duBk;
  LOCAL duBs;
  duN := SIZE(rkUSq);
  duA := 0; duB := 0; duR := 0;
  duRun := rk_Zeros(duN); duSt := rk_Zeros(duN);
  duG := 0; duLen := 0; duBest := 0; duBk := 1; duBs := 1;
  FOR duI FROM 1 TO duN DO
    IF rkUSq(duI) == 1 THEN duA := duA + 1; ELSE duB := duB + 1; END;
    IF rkUSq(duI) <> duG THEN
      // a new run starts here
      duR := duR + 1; duSt(duR) := duI; duG := rkUSq(duI); duLen := 0;
    END;
    duLen := duLen + 1;
    duRun(duI) := duR;
    IF duLen > duBest THEN duBest := duLen; duBk := duG; duBs := duSt(duR); END;
  END;
  IF duN < 3 OR duA == 0 OR duB == 0 THEN
    MSGBOX("The runs test needs at least 3 values, of two kinds.");
    RETURN 0;
  END;
  rkUN1 := duA; rkUN2 := duB; rkURun := duRun; rkUSt := duSt;
  rkULong := duBest; rkULk := duBk; rkULs := duBs;
  rkN := duN; rkSt := duR; rkSt2 := 0;
  rkMu := 2 * duA * duB / duN + 1;
  duVar := 2 * duA * duB * (2 * duA * duB - duN) / (duN^2 * (duN - 1));
  rkSd := MAX(0, duVar)^0.5;
  // no continuity correction: one z for every tail
  rkZ2 := (duR - rkMu) / rkSd; rkZL := rkZ2; rkZU := rkZ2;
  // the runs counted over the runs expected: below 1 = fewer than chance
  rkEff := duR / rkMu; rkEff2 := 0;
  rkZero := 0; rkHLok := 0; rkHLv := 0; rkHLWhy := "";
  rkTieN := 0; rkTieS := 0; rkTieMx := 1;
  RK_RANKS := {0};
  rkUSel := 1;
  // the exact null, up to 2,000 values
  rkEx := 0; rkNOK := 0; rkPeL := -1; rkPeU := -1;
  rkNObs := rkSt; rkNMu := rkMu;
  IF duN > 2000 THEN
    rkExWhy := "none for n > 2,000 (normal)";
  ELSE
    IF rk_RuNull(duA, duB) == 1 THEN
      rkPeL := rk_NSum(rkSt, 1);
      rkPeU := rk_NSum(rkSt, 0);
      rkEx := 1; rkNOK := 1; rkExWhy := "";
      rk_NullWin();
    END;
  END;
  RETURN 1;
END;

// rk_RuFrom: make the two-kind sequence from a list of numbers in their
// order.  Two different values in the list: they are the two kinds, as
// they are (the larger one is kind 1).  More than two: the numbers are
// cut at their median, above = kind 1, below = kind 2, and a value
// equal to the median is dropped (the usual rule; R's randtests
// runs.test does the same).  Everything is built in locals, and the
// loaded sequence changes only when the new one can be tested (a
// refused read changes nothing).  Returns 1 when loaded, 0 when refused
// (a sentence has said why).
rk_RuFrom(rfV, rfSrc, rfLab)
BEGIN
  LOCAL rfN, rfS, rfI, rfD, rfMed, rfSq;
  LOCAL rfKp, rfHi, rfLo, rfA, rfB, rfJ;
  rfN := SIZE(rfV);
  IF rfN < 3 THEN
    MSGBOX("The runs test needs at least 3 values, in the order they happened.");
    RETURN 0;
  END;
  rfS := SORT(rfV);
  rfLo := rfS(1); rfHi := rfS(rfN);
  IF rfHi == rfLo THEN
    MSGBOX("Every value is the same: there are no runs to count.");
    RETURN 0;
  END;
  // two different values, or more?  (stop at the first third value)
  rfD := 2; rfI := 1;
  WHILE rfD == 2 AND rfI <= rfN DO
    IF rfS(rfI) <> rfLo AND rfS(rfI) <> rfHi THEN rfD := 3; END;
    rfI := rfI + 1;
  END;
  IF rfD == 2 THEN
    rfSq := rk_Zeros(rfN);
    FOR rfI FROM 1 TO rfN DO
      IF rfV(rfI) == rfHi THEN rfSq(rfI) := 1; ELSE rfSq(rfI) := 2; END;
    END;
    rkUSq := rfSq; rkUVal := {}; rkUCut := 0; rkUDrop := 0;
    rkUNmA := rk_Cm(rk_Num(rfHi)); rkUNmB := rk_Cm(rk_Num(rfLo));
  ELSE
    rfMed := rk_Med(rfS);
    rfA := 0; rfB := 0;
    FOR rfI FROM 1 TO rfN DO
      IF rfV(rfI) > rfMed THEN rfA := rfA + 1; END;
      IF rfV(rfI) < rfMed THEN rfB := rfB + 1; END;
    END;
    IF rfA == 0 OR rfB == 0 OR rfA + rfB < 3 THEN
      MSGBOX("With the values equal to the median (" + rk_Cm(rk_Num(rfMed)) + ") dropped, too few are left on its two sides for a runs test.");
      RETURN 0;
    END;
    rfSq := rk_Zeros(rfA + rfB); rfKp := rk_Zeros(rfA + rfB); rfJ := 0;
    FOR rfI FROM 1 TO rfN DO
      IF rfV(rfI) <> rfMed THEN
        rfJ := rfJ + 1;
        rfKp(rfJ) := rfV(rfI);
        IF rfV(rfI) > rfMed THEN rfSq(rfJ) := 1; ELSE rfSq(rfJ) := 2; END;
      END;
    END;
    rkUSq := rfSq; rkUVal := rfKp; rkUCut := rfMed; rkUDrop := rfN - rfA - rfB;
    rkUNmA := "above"; rkUNmB := "below";
  END;
  rkUCl := {rkBLUE, #E07800h};
  rkUSrc := rfSrc; rkULab := rfLab; rkUHas := 1;
  // numbers: the run chart first, when it can be drawn (400 values)
  rkUCh := 0;
  IF SIZE(rkUVal) > 0 AND SIZE(rkUVal) <= 400 THEN rkUCh := 1; END;
  RETURN 1;
END;

''')
rep('@LONE@', LONE); rep('@BUDGET@', str(BUDGET))

# rk_Pick, rk_PMain: tests 7 and 8 have an exact p beside a normal one, as tests 1 to 3 do
rep('''rk_Pick()
BEGIN
  IF rkTest <= 3 THEN
    rkZ := rkZ2;
''', '''rk_Pick()
BEGIN
  // beta 1j: Page's L (7) and the runs test (8) take the same road as
  // tests 1 to 3 (their three z are one z: no continuity correction)
  IF rkTest <= 3 OR rkTest >= 7 THEN
    rkZ := rkZ2;
''')
rep('''  IF rkTest <= 3 AND rkEx == 1 AND rkMode == 1 THEN RETURN rkPe; END;
  IF rkTest == 6 THEN
    // Spearman's p when it has one, else Kendall's
''', '''  IF (rkTest <= 3 OR rkTest >= 7) AND rkEx == 1 AND rkMode == 1 THEN RETURN rkPe; END;
  IF rkTest == 6 THEN
    // Spearman's p when it has one, else Kendall's
''')
rep('''  IF rkTest == 6 THEN cmN := 2 * SIZE(rkCX); END;
  rkStop := 0;
''', '''  IF rkTest == 6 THEN cmN := 2 * SIZE(rkCX); END;
  IF rkTest == 7 THEN cmN := SIZE(rkFM); END;
  rkStop := 0;
''')
rep('''    IF rkTest == 6 THEN cmOK := rk_DoCorr(); END;
  END;
''', '''    IF rkTest == 6 THEN cmOK := rk_DoCorr(); END;
    IF rkTest == 7 THEN cmOK := rk_DoPage(); END;
    IF rkTest == 8 THEN cmOK := rk_DoRuns(); END;
  END;
''')

# ---------------- the presets ----------------
rep('''  rkFSrc := "New Haven Register 14 Jan 1977 (R datasets)";
  rkFHas := 1; rkFNoP := 1;
END;
''', '''  rkFSrc := "New Haven Register 14 Jan 1977 (R datasets)";
  rkFHas := 1; rkFNoP := 1; rkLDir := 2;
END;
''')
rep('''  rkFSrc := "New Haven Register 14 Jan 1977 (R datasets)";
  rkFHas := 1; rkFNoP := 0;
END;
''', '''  rkFSrc := "New Haven Register 14 Jan 1977 (R datasets)";
  rkFHas := 1; rkFNoP := 0; rkLDir := 2;
END;
''')
before('''// rk_Preset: the preset menu.  Loads one data set and returns the test
''', r'''// rk_LdOzone (beta 1j): the change in airway resistance (cm H2O/l/s,
// after minus before) of four men after an hour at each of three levels
// of ozone: Goldsmith & Nadel (1969), the subset in Hollander, Wolfe &
// Chicken (2014) Table 7.2.  Rows = the men (blocks), columns = the
// levels in rising order, so Page's L asks whether the resistance
// rises with the dose.
rk_LdOzone()
BEGIN
  rkFM := {
    -0.08, 0.01, 0.06,
    0.21, 0.17, 0.19,
    0.5, -0.11, 0.34,
    0.14, 0.07, 0.14};
  rkFB := 4; rkFK := 3;
  rkFTn := {"0.1 ppm", "0.6 ppm", "1.0 ppm"};
  rkFBn := {"Subj 1", "Subj 2", "Subj 3", "Subj 4"};
  rkFLab := "change in airway resistance after ozone";
  rkFSrc := "Goldsmith & Nadel 1969 (Hollander et al. 2014)";
  rkFHas := 1; rkFNoP := 0; rkLDir := 2;
END;

// rk_LdDraftM (beta 1j): the 1970 draft lottery as blocks x treatments:
// the days 1 to 28 of the month are the blocks (every month has them)
// and the twelve months, January to December, the treatments in order.
// Within one day-of-the-month the twelve numbers are ranked.  A fair
// drawing makes every order equally likely in each block, and blocks
// of different dates are independent, so Page's L is exact here.  The
// direction is "falling": the later months drew the lower numbers.
rk_LdDraftM()
BEGIN
  LOCAL dmN, dmC, dmD, dmM;
  dmN := rk_DraftNo();
  // the days before each month's first (February had 29 in the lottery)
  dmC := {0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335};
  rkFM := rk_Zeros(28 * 12);
  rkFBn := {};
  FOR dmD FROM 1 TO 28 DO
    FOR dmM FROM 1 TO 12 DO
      rkFM((dmD - 1) * 12 + dmM) := dmN(dmC(dmM) + dmD);
    END;
    rkFBn := CONCAT(rkFBn, {"day " + STRING(dmD, 2, 0)});
  END;
  rkFB := 28; rkFK := 12;
  rkFTn := {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
  rkFLab := "draft number: days 1-28 (blocks), 12 months";
  rkFSrc := "Fienberg 1971 Science 171:255; Starr 1997 JSE";
  rkFHas := 1; rkFNoP := 0; rkLDir := 1;
END;

// rk_LdRoul (beta 1j): 25 spins of a roulette wheel, red (R) or black
// (B), 0 and 00 left out: R R R R B R R R B B B B B R R B B B R R B B
// R R R, the example of "The Run Test for Randomness" in the HP-65 Stat
// Pac 2 (1975).  14 red, 11 black, 9 runs: that book gets the mean
// 13.32, the standard deviation 2.41 and z = -1.79.
rk_LdRoul()
BEGIN
  rkUSq := {1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1};
  rkUVal := {}; rkUCut := 0; rkUDrop := 0;
  rkUNmA := "R"; rkUNmB := "B";
  rkUCl := {rkRED, #000000h};
  rkULab := "roulette: red (R) or black (B), 25 spins";
  rkUSrc := "HP-65 Stat Pac 2 (1975), the run test's example";
  rkUHas := 1; rkUCh := 0;
END;

// rk_LdDraftR (beta 1j): the 1970 draft numbers in birth-date order,
// each above or below their median, 183.5.  Returns 1 when loaded.
rk_LdDraftR()
BEGIN
  RETURN rk_RuFrom(rk_DraftNo(), "Fienberg 1971 Science 171:255; Starr 1997 JSE", "draft number by birth date, Jan 1 to Dec 31");
END;

''')
rep('''  CHOOSE(prI, "Load a preset", {"Rossi: prior convictions", "Draft 1970: number by month", "Draft 1970: day vs number", "Darwin: Zea mays pairs", "US judges: 3 criteria", "Mock jury: years by looks", "US judges: halo (W only)"});
''', '''  // beta 1j: four presets more, after the old seven (which keep their numbers)
  CHOOSE(prI, "Load a preset", {"Rossi: prior convictions", "Draft 1970: number by month", "Draft 1970: day vs number",
    "Darwin: Zea mays pairs", "US judges: 3 criteria", "Mock jury: years by looks", "US judges: halo (W only)",
    "Ozone: airway resistance", "Draft 1970: months in order", "Roulette: red and black", "Draft 1970: runs by day"});
''')
rep('''  IF prI == 7 THEN rk_LdHalo(); RETURN 5; END;
  RETURN 0;
''', '''  IF prI == 7 THEN rk_LdHalo(); RETURN 5; END;
  IF prI == 8 THEN rk_LdOzone(); RETURN 7; END;
  IF prI == 9 THEN rk_LdDraftM(); RETURN 7; END;
  IF prI == 10 THEN rk_LdRoul(); RETURN 8; END;
  IF prI == 11 THEN
    IF rk_LdDraftR() == 1 THEN RETURN 8; END;
  END;
  RETURN 0;
''')

# ---------------- your own data ----------------
rep('''  LOCAL myI, myK, myL, myA, myB, myM;
  LOCAL myC, myN, myOK;
  myI := 0;
  CHOOSE(myI, "Your data (Statistics 1Var)", {"Groups: D1, D2, D3 ...", "Paired: D1 - D2", "One sample: D1 vs median", "Correlation: D1 (x), D2 (y)", "Friedman: rows = blocks"});
  IF myI == 0 THEN RETURN 0; END;
''', '''  LOCAL myI, myK, myL, myA, myB, myM;
  LOCAL myC, myN, myOK, myW;
  myI := 0;
  CHOOSE(myI, "Your data (Statistics 1Var)", {"Groups: D1, D2, D3 ...", "Paired: D1 - D2", "One sample: D1 vs median", "Correlation: D1 (x), D2 (y)", "Friedman: rows = blocks", "Page's L: rows = blocks", "Runs: D1 in order"});
  IF myI == 0 THEN RETURN 0; END;
  // beta 1j: the choice is kept in myW (the Friedman loop below counts with myI)
  myW := myI;
  IF myI == 7 THEN
    // the runs test: D1 in the order the values happened
    myA := rk_ReadD(1);
    IF SIZE(myA) == 0 THEN
      MSGBOX("Put the sequence in D1 of the Statistics 1Var app first, in the order it happened.");
      RETURN 0;
    END;
    IF rk_RuFrom(myA, "your data: D1, in its order", "D1 in order") == 1 THEN RETURN 8; END;
    RETURN 0;
  END;
''')
rep('''  // Friedman: D1 .. Dk side by side, one row per block
  myK := 0; myN := -1; myOK := 1;
''', '''  // Friedman (and, beta 1j, Page's L): D1 .. Dk side by side, one row per block
  myK := 0; myN := -1; myOK := 1;
''')
rep('''  rkFB := myN; rkFK := myK;
  rkFM := rk_Zeros(myN * myK);
''', '''  // beta 1j: the whole table goes into one list, and a list holds 10,000
  // values (until beta 1i a larger table was not refused)
  IF myN * myK > 10000 THEN
    MSGBOX("Friedman and Page's L take a table of 10,000 values at the most (rows " + rkTX + " columns); this one has " + rk_Cm(STRING(myN * myK, 2, 0)) + ".");
    RETURN 0;
  END;
  rkFB := myN; rkFK := myK;
  rkFM := rk_Zeros(myN * myK);
''')
rep('''  rkFSrc := "your data: Statistics 1Var columns"; rkFHas := 1; rkFNoP := 0;
  RETURN 5;
END;
''', '''  rkFSrc := "your data: Statistics 1Var columns"; rkFHas := 1; rkFNoP := 0;
  rkLDir := 2;
  // beta 1j: the same table opens under Page's L when that was the choice
  IF myW == 6 THEN RETURN 7; END;
  RETURN 5;
END;
''')
rep('''  IF enT == 6 AND rkCHas == 0 THEN
    rk_LdDraftC();
    MSGBOX("No pairs yet: the 1970 draft lottery, day vs number, loaded. (Load a preset or Use my data to change it.)");
  END;
  RETURN 1;
''', '''  IF enT == 6 AND rkCHas == 0 THEN
    rk_LdDraftC();
    MSGBOX("No pairs yet: the 1970 draft lottery, day vs number, loaded. (Load a preset or Use my data to change it.)");
  END;
  // beta 1j
  IF enT == 7 AND rkFHas == 0 THEN
    rk_LdOzone();
    MSGBOX("No blocks yet: the ozone data loaded. (Load a preset or Use my data to change it.)");
  END;
  IF enT == 8 AND rkUHas == 0 THEN
    rk_LdRoul();
    MSGBOX("No sequence yet: the roulette example loaded. (Load a preset or Use my data to change it.)");
  END;
  RETURN 1;
''')

# ---------------- names ----------------
rep('''  IF rkTest == 5 THEN RETURN "Friedman and Kendall's W"; END;
  RETURN "Rank correlation";
END;
''', '''  IF rkTest == 5 THEN RETURN "Friedman and Kendall's W"; END;
  IF rkTest == 7 THEN RETURN "Page's L"; END;
  IF rkTest == 8 THEN RETURN "Runs test"; END;
  RETURN "Rank correlation";
END;
''')
rep('''  IF rkTest == 5 THEN RETURN "Friedman"; END;
  RETURN "Rank correlation";
END;
''', '''  IF rkTest == 5 THEN RETURN "Friedman"; END;
  IF rkTest == 7 THEN RETURN "Page's L"; END;
  IF rkTest == 8 THEN RETURN "Runs test"; END;
  RETURN "Rank correlation";
END;
''')
rep('''  IF rkTest == 5 THEN RETURN "Q"; END;
  IF rkCWh == 1 THEN RETURN "t"; END;
''', '''  IF rkTest == 5 THEN RETURN "Q"; END;
  IF rkTest == 7 THEN RETURN "L"; END;
  IF rkTest == 8 THEN RETURN "runs"; END;
  IF rkCWh == 1 THEN RETURN "t"; END;
''')
rep('''  IF rkTest == 5 THEN RETURN rkFSrc; END;
  RETURN rkCSrc;
''', '''  IF rkTest == 5 OR rkTest == 7 THEN RETURN rkFSrc; END;
  IF rkTest == 8 THEN RETURN rkUSrc; END;
  RETURN rkCSrc;
''')

# ---------------- the result page ----------------
before('''  rk_Foot(rkUD + " = page, Ent = menu, 0 = help, Esc = back");
END;


// ============================================================
// THE RANK STRIP (sign test, signed-rank, Mann-Whitney)
''', r'''  // beta 1j: Page's L
  IF rkTest == 7 THEN
    rk_Ln(1, rkFLab, #000000h);
    rk_Ln(2, "b = " + rk_Cm(STRING(rkFB, 2, 0)) + " blocks, k = " + rk_Cm(STRING(rkFK, 2, 0)) + " treatments in the order listed", #000000h);
    rk_Ln(3, rk_LOrd(), #000000h);
    rk_Ln(4, "L = " + rk_Cm(rk_Num(rkSt)) + "  (mean " + rk_Cm(rk_Num(rkMu)) + ", SD " + rk_Cm(rk_Fx(rkSd, 2)) + IFTE(rkLNt > 0, "; ties in " + rk_Cm(STRING(rkLNt, 2, 0)) + IFTE(rkLNt == 1, " block", " blocks"), "") + ")", #000000h);
    rk_ExLine(5);
    rk_Ln(6, "Normal: z = " + rk_Cm(rk_Sg(rkZ, 3)) + ", " + rk_PT(rkPn) + " (no cont. corr.)", rkBLUE);
    rk_Ln(7, "Mean Spearman rs with the order = " + rk_Cm(rk_Sg(rkEff, 3)), #000000h);
    // the mean ranks in the order listed, values only (their names are
    // on the Order line): every one of them, on two lines at the most
    psM := "Mean ranks, in order: "; psN := 0;
    FOR psJ FROM 1 TO rkFK DO
      psT := rk_Cm(rk_Fx(rkFRS(psJ) / rkFB, 1));
      IF psJ < rkFK THEN psT := psT + ", "; END;
      IF DIM(psM) + DIM(psT) > 46 THEN
        IF psN < 2 THEN rk_Ln(8 + psN, psM, #000000h); END;
        psN := psN + 1;
        psM := "  ";
      END;
      psM := psM + psT;
    END;
    IF psN < 2 THEN rk_Ln(8 + psN, psM, #000000h); END;
    rk_Ln(10, rkH0 + ": no trend.  H" + CHAR(8321) + ": the ranks " + IFTE(rkTail == 1, "fall", "rise") + " in that order.", rkBLUE);
    rk_Verd(11, rk_PMain());
    rk_Ln(12, "Choose the order and the direction before the", rkGRAY);
    rk_Ln(13, "data are seen.  The blocks must be independent.", rkGRAY);
  END;
  // beta 1j: the runs test
  IF rkTest == 8 THEN
    rk_Ln(1, rkULab, #000000h);
    IF SIZE(rkUVal) > 0 THEN
      rk_Ln(2, "Median " + rk_Cm(rk_Num(rkUCut)) + ": above or below (equal: dropped)", #000000h);
      rk_Ln(3, "n = " + rk_Cm(STRING(rkN, 2, 0)) + ": " + rk_Cm(STRING(rkUN1, 2, 0)) + " above, " + rk_Cm(STRING(rkUN2, 2, 0)) + " below" + IFTE(rkUDrop > 0, " (dropped: " + rk_Cm(STRING(rkUDrop, 2, 0)) + ")", ""), #000000h);
    ELSE
      rk_Ln(2, "Two kinds of values, in the order they came", #000000h);
      rk_Ln(3, "n = " + rk_Cm(STRING(rkN, 2, 0)) + ": " + rk_Cm(STRING(rkUN1, 2, 0)) + " of " + rk_Trunc(rkUNmA, 10) + ", " + rk_Cm(STRING(rkUN2, 2, 0)) + " of " + rk_Trunc(rkUNmB, 10), #000000h);
    END;
    rk_Ln(4, "runs = " + rk_Cm(STRING(rkSt, 2, 0)) + "  (mean " + rk_Cm(rk_Fx(rkMu, 2)) + ", SD " + rk_Cm(rk_Fx(rkSd, 2)) + " under " + rkH0 + ")", #000000h);
    rk_ExLine(5);
    rk_Ln(6, "Normal: z = " + rk_Cm(rk_Sg(rkZ, 3)) + ", " + rk_PT(rkPn) + " (no cont. corr.)", rkBLUE);
    // the runs counted over the runs expected: three cases at the decimals shown
    psT := ROUND(rkEff, 2);
    IF psT < 1 THEN rk_Ln(7, "Runs / mean = " + rk_Cm(rk_Fx(rkEff, 2)) + " (below 1: like values cluster)", #000000h); END;
    IF psT > 1 THEN rk_Ln(7, "Runs / mean = " + rk_Cm(rk_Fx(rkEff, 2)) + " (above 1: the kinds alternate)", #000000h); END;
    IF psT == 1 THEN rk_Ln(7, "Runs / mean = 1.00 (as many runs as chance gives)", #000000h); END;
    IF rkULong == 1 THEN
      rk_Ln(8, "Longest run: 1 (no two neighbors are the same kind)", #000000h);
    ELSE
      rk_Ln(8, "Longest run: " + rk_Cm(STRING(rkULong, 2, 0)) + " of " + rk_Trunc(IFTE(rkULk == 1, rkUNmA, rkUNmB), 10) + ", places " + rk_Cm(STRING(rkULs, 2, 0)) + " to " + rk_Cm(STRING(rkULs + rkULong - 1, 2, 0)), #000000h);
    END;
    rk_Ln(9, rkH0 + ": the order is random  (" + rk_TailW() + ")", rkBLUE);
    rk_Verd(10, rk_PMain());
    rk_Ln(11, "Lower tail = too few runs (clusters, a drift);", rkGRAY);
    rk_Ln(12, "upper tail = too many (the kinds alternate).", rkGRAY);
    rk_Ln(13, "Exact p: every order of the two kinds (n " + rkLE + " 2,000).", rkGRAY);
  END;
''')

# ---------------- the two pictures ----------------
before('''// ============================================================
// THE NULL DISTRIBUTION
// ============================================================
''', r'''// ============================================================
// beta 1j: PAGE'S L (the mean ranks in order); THE RUNS TEST (the
// sequence as squares, or its run chart)
// ============================================================

// rk_LOrd: the order the treatments are tested in, as one line:
// "Order: 0.1 ppm -> 0.6 ppm -> 1.0 ppm" (the first two and the last
// when the whole list is too long for the line).
rk_LOrd()
BEGIN
  LOCAL lqS, lqJ, lqA;
  lqA := " " + CHAR(8594) + " ";
  lqS := "Order: " + rk_Trunc(rkFTn(1), 10);
  FOR lqJ FROM 2 TO rkFK DO lqS := lqS + lqA + rk_Trunc(rkFTn(lqJ), 10); END;
  IF DIM(lqS) <= 44 THEN RETURN lqS; END;
  RETURN "Order: " + rk_Trunc(rkFTn(1), 10) + lqA + rk_Trunc(rkFTn(2), 10) + lqA + "..." + lqA + rk_Trunc(rkFTn(rkFK), 10);
END;

// rk_PgTrend: Page's L, the picture.  The treatments left to right in
// the order listed; each one's mean rank as a dot; the dotted green
// line is the mean rank every treatment has under H0, (k + 1)/2.  Under
// each name is the weight its rank sum carries in L (its place in the
// order).  Tap a treatment (or Left / Right) to read its numbers.
rk_PgTrend()
BEGIN
  LOCAL tdK, tdB, tdJ, tdCw, tdLo, tdHi;
  LOCAL tdT, tdV, tdY, tdX, tdM, tdS;
  LOCAL tdC, tdH0;
  tdK := rkFK; tdB := rkFB;
  rk_Frame("Page's L: mean ranks in the order listed");
  TEXTOUT_P("dot = mean rank;  " + rkTX + "1, " + rkTX + "2 ... = weight in L;  dotted: " + rkH0, G1, 6, 22, 1, rkGRAY, 310);
  // the scale: whole ranks that take in every mean rank and the H0 level
  tdH0 := (tdK + 1) / 2;
  tdLo := tdH0; tdHi := tdH0;
  FOR tdJ FROM 1 TO tdK DO
    tdM := rkFRS(tdJ) / tdB;
    tdLo := MIN(tdLo, tdM); tdHi := MAX(tdHi, tdM);
  END;
  tdLo := FLOOR(tdLo); tdHi := CEILING(tdHi);
  IF tdHi == tdLo THEN tdLo := tdLo - 1; tdHi := tdHi + 1; END;
  RECT_P(G1, 34, 38, 308, 128, rkGRID, #FFFFFFh);
  tdT := rk_Nice((tdHi - tdLo) / 4);
  tdV := CEILING(tdLo / tdT) * tdT;
  WHILE tdV <= tdHi DO
    tdY := 124 - IP((tdV - tdLo) / (tdHi - tdLo) * 82);
    LINE_P(G1, 34, tdY, 308, tdY, rkGRID);
    TEXTOUT_P(rk_Num(tdV), G1, 2, tdY - 5, 1, rkGRAY, 30);
    tdV := tdV + tdT;
  END;
  // the H0 level
  tdY := 124 - IP((tdH0 - tdLo) / (tdHi - tdLo) * 82);
  FOR tdX FROM 34 TO 308 STEP 3 DO PIXON_P(G1, tdX, tdY, rkGRN); END;
  // where each treatment's dot sits (kept for the taps)
  tdCw := 274 / tdK;
  rkHX := rk_Zeros(tdK); rkHY := rk_Zeros(tdK);
  FOR tdJ FROM 1 TO tdK DO
    rkHX(tdJ) := 34 + IP((tdJ - 0.5) * tdCw);
    rkHY(tdJ) := 124 - IP((rkFRS(tdJ) / tdB - tdLo) / (tdHi - tdLo) * 82);
  END;
  // the line from dot to dot first, then the dots on top of it
  FOR tdJ FROM 2 TO tdK DO
    LINE_P(G1, rkHX(tdJ - 1), rkHY(tdJ - 1), rkHX(tdJ), rkHY(tdJ), rkGRAY);
  END;
  FOR tdJ FROM 1 TO tdK DO
    tdC := rk_GCol(tdJ);
    RECT_P(G1, rkHX(tdJ) - 3, rkHY(tdJ) - 3, rkHX(tdJ) + 3, rkHY(tdJ) + 3, tdC, tdC);
    tdS := rk_Trunc(rkFTn(tdJ), MAX(1, IP((tdCw - 2) / 6.5)));
    TEXTOUT_P(tdS, G1, rkHX(tdJ) - 3 * DIM(tdS), 131, 1, tdC, IP(tdCw) + 4);
    tdS := rkTX + STRING(tdJ, 2, 0);
    TEXTOUT_P(tdS, G1, rkHX(tdJ) - 3 * DIM(tdS), 143, 1, rkGRAY, 40);
  END;
  // the picked treatment
  tdJ := rkLSel;
  rk_Box(rkHX(tdJ) - 5, rkHY(tdJ) - 5, rkHX(tdJ) + 5, rkHY(tdJ) + 5, rkRED);
  RECT_P(G1, 0, 165, 319, 202, rkORNG, rkLORN);
  TEXTOUT_P(rk_Trunc(rkFTn(tdJ), 14) + ": rank sum " + rk_Cm(rk_Num(rkFRS(tdJ))) + ", mean rank " + rk_Cm(rk_Fx(rkFRS(tdJ) / tdB, 2)) + " (" + rkH0 + " " + rk_Num(tdH0) + ")", G1, 6, 167, 1, rk_GCol(tdJ), 308);
  TEXTOUT_P("place " + STRING(tdJ, 2, 0) + " in the order: adds " + STRING(tdJ, 2, 0) + " " + rkTX + " " + rk_Cm(rk_Num(rkFRS(tdJ))) + " = " + rk_Cm(rk_Num(tdJ * rkFRS(tdJ))) + " to L", G1, 6, 179, 1, #000000h, 308);
  TEXTOUT_P("L = " + rk_Cm(rk_Num(rkSt)) + " (mean " + rk_Cm(rk_Num(rkMu)) + "): " + IFTE(rkEx == 1 AND rkMode == 1, "exact ", "normal ") + rk_PT(rk_PMain()) + ", " + rk_TailW(), G1, 6, 191, 1, rkBLUE, 308);
  rk_Foot("tap a point, " + rkLR + " = pick, " + rkUD + " = page, Esc = back");
END;

// rk_RuGeo: the squares' size for the sequence: the pitch (rkUC), how
// many go in a row (rkUPer) and where the first row starts (rkUY0), so
// that every value up to the 2,000th has a square of its own.
rk_RuGeo()
BEGIN
  LOCAL rgN, rgR;
  rgN := MIN(2000, SIZE(rkUSq));
  rkUC := 3;
  IF rgN <= 1275 THEN rkUC := 4; END;
  IF rgN <= 840 THEN rkUC := 5; END;
  IF rgN <= 650 THEN rkUC := 6; END;
  IF rgN <= 370 THEN rkUC := 8; END;
  IF rgN <= 175 THEN rkUC := 12; END;
  rkUPer := IP(300 / rkUC);
  // the rows, centered between the header and the panel
  rgR := CEILING(rgN / rkUPer);
  rkUY0 := 48 + IP((106 - rgR * (rkUC + 2)) / 2);
END;

// rk_AxS: one number of an axis as text.  xsS = 0: as it is, with
// commas.  xsS = 1: the Prime's scientific form with one decimal and
// without a ".0" ("1.5E6", "2E6"; the E is the calculator's small
// capital), for an axis whose numbers are too wide for their room.
rk_AxS(xsV, xsS)
BEGIN
  LOCAL xsT, xsK;
  IF xsS == 0 THEN RETURN rk_Cm(rk_Num(xsV)); END;
  IF xsV == 0 THEN RETURN "0"; END;
  xsT := STRING(xsV, 3, 1);
  xsK := INSTRING(xsT, ".0" + CHAR(7431));
  IF xsK > 1 THEN xsT := LEFT(xsT, xsK - 1) + MID(xsT, xsK + 2, DIM(xsT) - xsK - 1); END;
  RETURN xsT;
END;

// rk_AxW: about how wide a number is in font 1: 6 pixels a character,
// 3 for a point or a comma.
rk_AxW(xwT)
BEGIN
  LOCAL xwW, xwI;
  xwW := 6 * DIM(xwT);
  FOR xwI FROM 1 TO DIM(xwT) DO
    IF MID(xwT, xwI, 1) == "." OR MID(xwT, xwI, 1) == "," THEN xwW := xwW - 3; END;
  END;
  RETURN xwW;
END;

// rk_RuCells: the sequence as squares, one a value, left to right and
// row after row, in the two kinds' colors.  Big squares (few values) are
// drawn one by one; small ones run by run (one bar for the piece of a
// run on a row), which is the same picture in fewer strokes.  The
// picked place's run is outlined in green and its own square is ringed;
// two green ticks at the edges point to its column and its row.  When
// the squares fit in one row, each run's length is written under it.
rk_RuCells()
BEGIN
  LOCAL rcN, rcI, rcR, rcA, rcB, rcRow;
  LOCAL rcX1, rcX2, rcY, rcC, rcE, rcP;
  LOCAL rcS;
  rk_RuGeo();
  rcN := MIN(2000, SIZE(rkUSq));
  rcP := rkUC + 2;                            // from one row to the next
  IF rkUC >= 8 THEN
    FOR rcI FROM 1 TO rcN DO
      rcRow := IP((rcI - 1) / rkUPer);
      rcX1 := 10 + (rcI - 1 - rcRow * rkUPer) * rkUC;
      rcY := rkUY0 + rcRow * rcP;
      rcC := rkUCl(rkUSq(rcI));
      RECT_P(G1, rcX1, rcY, rcX1 + rkUC - 2, rcY + rkUC - 2, rcC, rcC);
    END;
  ELSE
    rcR := 1;
    WHILE rcR <= rkSt AND rkUSt(rcR) <= rcN DO
      rcA := rkUSt(rcR); rcB := MIN(rcN, rk_RuEnd(rcR));
      rcC := rkUCl(rkUSq(rcA));
      WHILE rcA <= rcB DO
        rcRow := IP((rcA - 1) / rkUPer);
        rcE := MIN(rcB, (rcRow + 1) * rkUPer);          // the last place of this piece
        rcX1 := 10 + (rcA - 1 - rcRow * rkUPer) * rkUC;
        rcX2 := 10 + (rcE - 1 - rcRow * rkUPer) * rkUC + rkUC - 2;
        rcY := rkUY0 + rcRow * rcP;
        RECT_P(G1, rcX1, rcY, rcX2, rcY + rkUC - 2, rcC, rcC);
        rcA := rcE + 1;
      END;
      rcR := rcR + 1;
    END;
  END;
  // one row only (25 values at the most): each run's length under it
  IF rcN <= rkUPer THEN
    rcY := rkUY0 + rkUC + 3;
    FOR rcR FROM 1 TO rkSt DO
      rcA := rkUSt(rcR); rcB := rk_RuEnd(rcR);
      rcX1 := 10 + (rcA - 1) * rkUC + IP(((rcB - rcA + 1) * rkUC - 1) / 2);
      rcS := STRING(rcB - rcA + 1, 2, 0);
      TEXTOUT_P(rcS, G1, rcX1 - 3 * DIM(rcS), rcY, 1, rkGRAY, 40);
    END;
  END;
  // the picked place
  rcI := rkUSel;
  IF rcI >= 1 AND rcI <= rcN THEN
    rcR := rkURun(rcI);
    rcA := rkUSt(rcR); rcB := MIN(rcN, rk_RuEnd(rcR));
    WHILE rcA <= rcB DO
      rcRow := IP((rcA - 1) / rkUPer);
      rcE := MIN(rcB, (rcRow + 1) * rkUPer);
      rcX1 := 10 + (rcA - 1 - rcRow * rkUPer) * rkUC;
      rcX2 := 10 + (rcE - 1 - rcRow * rkUPer) * rkUC + rkUC - 2;
      rcY := rkUY0 + rcRow * rcP;
      rk_Box(rcX1 - 1, rcY - 1, rcX2 + 1, rcY + rkUC - 1, rkGRN);
      rcA := rcE + 1;
    END;
    rcRow := IP((rcI - 1) / rkUPer);
    rcX1 := 10 + (rcI - 1 - rcRow * rkUPer) * rkUC;
    rcY := rkUY0 + rcRow * rcP;
    IF rkUC >= 8 THEN
      RECT_P(G1, rcX1 + 2, rcY + 2, rcX1 + rkUC - 4, rcY + rkUC - 4, #FFFFFFh, #FFFFFFh);
    END;
    LINE_P(G1, rcX1 + IP((rkUC - 2) / 2), rkUY0 - 6, rcX1 + IP((rkUC - 2) / 2), rkUY0 - 3, rkGRN);
    LINE_P(G1, 3, rcY + IP((rkUC - 2) / 2), 7, rcY + IP((rkUC - 2) / 2), rkGRN);
  END;
END;

// rk_RuChart: the run chart of a sequence that came from numbers (up to
// 400 of them): the values in their order, joined by a line, each dot in
// the color of its side of the median; the median is the dotted line.  A
// run is a stretch of the line that stays on one side of it.
rk_RuChart()
BEGIN
  LOCAL rhN, rhLo, rhHi, rhI, rhT, rhV;
  LOCAL rhS, rhSc, rhK, rhPx, rhPy, rhC;
  LOCAL rhD, rhY;
  rhN := SIZE(rkUVal);
  rhS := SORT(rkUVal); rhLo := rhS(1); rhHi := rhS(rhN);
  IF rhHi == rhLo THEN rhLo := rhLo - 1; rhHi := rhHi + 1; END;
  rhT := (rhHi - rhLo) * 0.05; rhLo := rhLo - rhT; rhHi := rhHi + rhT;
  RECT_P(G1, 44, 46, 308, 146, rkGRID, #FFFFFFh);
  // the y axis: its numbers as they are when every one fits its room
  // (38 pixels), else all of them in the scientific form
  rhT := rk_Nice((rhHi - rhLo) / 5);
  rhSc := 0; rhV := CEILING(rhLo / rhT) * rhT; rhK := 0;
  WHILE rhV <= rhHi AND rhK < 40 DO
    IF rk_AxW(rk_AxS(rhV, 0)) > 38 THEN rhSc := 1; END;
    rhV := rhV + rhT; rhK := rhK + 1;
  END;
  rhV := CEILING(rhLo / rhT) * rhT; rhK := 0;
  WHILE rhV <= rhHi AND rhK < 40 DO
    rhPy := 146 - IP((rhV - rhLo) / (rhHi - rhLo) * 100);
    LINE_P(G1, 44, rhPy, 308, rhPy, rkGRID);
    TEXTOUT_P(rk_AxS(rhV, rhSc), G1, 2, rhPy - 5, 1, rkGRAY, 42);
    rhV := rhV + rhT; rhK := rhK + 1;
  END;
  // the x axis: the place in the order
  rhT := MAX(1, rk_Nice((rhN - 1) / 5));
  rhV := rhT;
  WHILE rhV <= rhN DO
    rhPx := 46 + IP((rhV - 1) / (rhN - 1) * 260);
    LINE_P(G1, rhPx, 146, rhPx, 149, #000000h);
    rhS := rk_Cm(STRING(rhV, 2, 0));
    TEXTOUT_P(rhS, G1, MIN(rhPx - 3 * DIM(rhS), 319 - 6 * DIM(rhS)), 150, 1, rkGRAY, 40);
    rhV := rhV + rhT;
  END;
  // the median
  rhPy := 146 - IP((rkUCut - rhLo) / (rhHi - rhLo) * 100);
  FOR rhI FROM 44 TO 308 STEP 3 DO PIXON_P(G1, rhI, rhPy, #000000h); END;
  // where each value sits (kept for the picked one), the line, the dots
  rkHX := rk_Zeros(rhN); rkHY := rk_Zeros(rhN);
  FOR rhI FROM 1 TO rhN DO
    rkHX(rhI) := 46 + IP((rhI - 1) / (rhN - 1) * 260);
    rkHY(rhI) := 146 - IP((rkUVal(rhI) - rhLo) / (rhHi - rhLo) * 100);
  END;
  FOR rhI FROM 2 TO rhN DO
    LINE_P(G1, rkHX(rhI - 1), rkHY(rhI - 1), rkHX(rhI), rkHY(rhI), #B4B4B4h);
  END;
  rhD := 0;
  IF rhN <= 150 THEN rhD := 1; END;
  IF rhN <= 60 THEN rhD := 2; END;
  FOR rhI FROM 1 TO rhN DO
    rhC := rkUCl(rkUSq(rhI));
    RECT_P(G1, rkHX(rhI) - rhD, rkHY(rhI) - rhD, rkHX(rhI) + MAX(1, rhD), rkHY(rhI) + MAX(1, rhD), rhC, rhC);
  END;
  // the picked value: a dotted green line down the plot, a green box
  rhI := MAX(1, MIN(rhN, rkUSel));
  FOR rhY FROM 46 TO 146 STEP 3 DO PIXON_P(G1, rkHX(rhI), rhY, rkGRN); END;
  rk_Box(rkHX(rhI) - 4, rkHY(rhI) - 4, rkHX(rhI) + 4, rkHY(rhI) + 4, rkGRN);
END;

// rk_PgRuns: the runs test, the picture: the legend, then the squares
// or the run chart, then the picked place in words.
rk_PgRuns()
BEGIN
  LOCAL puX, puI, puR, puA, puB, puG;
  LOCAL puS;
  rk_Frame("Runs test: the sequence, in order");
  // the legend: the two kinds, how many of each, and the runs
  puX := 6;
  RECT_P(G1, puX, 23, puX + 6, 29, rkUCl(1), rkUCl(1));
  puX := TEXTOUT_P(rk_Trunc(rkUNmA, 10) + " (" + rk_Cm(STRING(rkUN1, 2, 0)) + ")", G1, puX + 9, 21, 1, rkUCl(1), 120) + 8;
  RECT_P(G1, puX, 23, puX + 6, 29, rkUCl(2), rkUCl(2));
  puX := TEXTOUT_P(rk_Trunc(rkUNmB, 10) + " (" + rk_Cm(STRING(rkUN2, 2, 0)) + ")", G1, puX + 9, 21, 1, rkUCl(2), 120) + 10;
  TEXTOUT_P(rk_Cm(STRING(rkSt, 2, 0)) + " runs", G1, puX, 21, 1, #000000h, 90);
  IF rkUCh == 1 THEN
    TEXTOUT_P("the values in order; dotted = their median", G1, 6, 33, 1, rkGRAY, 300);
    rk_RuChart();
  ELSE
    IF rkN > 2000 THEN
      TEXTOUT_P("the first 2,000 of " + rk_Cm(STRING(rkN, 2, 0)) + " values, in order", G1, 6, 33, 1, rkGRAY, 300);
    ELSE
      IF rkN <= 25 THEN
        TEXTOUT_P("one square a value; under each run, its length", G1, 6, 33, 1, rkGRAY, 300);
      ELSE
        TEXTOUT_P("one square a value, in order; a run = one color", G1, 6, 33, 1, rkGRAY, 300);
      END;
    END;
    rk_RuCells();
  END;
  // the picked place, its run, and the test in one line
  puI := rkUSel; puG := rkUSq(puI); puR := rkURun(puI);
  puA := rkUSt(puR); puB := rk_RuEnd(puR);
  RECT_P(G1, 0, 165, 319, 202, rkORNG, rkLORN);
  puS := "Place " + rk_Cm(STRING(puI, 2, 0)) + " of " + rk_Cm(STRING(rkN, 2, 0)) + ": ";
  IF SIZE(rkUVal) > 0 THEN puS := puS + rk_Cm(rk_Num(rkUVal(puI))) + ", "; END;
  TEXTOUT_P(puS + rk_Trunc(IFTE(puG == 1, rkUNmA, rkUNmB), 10), G1, 6, 167, 1, rkUCl(puG), 308);
  IF puB > puA THEN
    puS := "run " + rk_Cm(STRING(puR, 2, 0)) + " of " + rk_Cm(STRING(rkSt, 2, 0)) + ": places " + rk_Cm(STRING(puA, 2, 0)) + " to " + rk_Cm(STRING(puB, 2, 0)) + ", " + rk_Cm(STRING(puB - puA + 1, 2, 0)) + " long";
  ELSE
    puS := "run " + rk_Cm(STRING(puR, 2, 0)) + " of " + rk_Cm(STRING(rkSt, 2, 0)) + ": this place alone";
  END;
  TEXTOUT_P(puS, G1, 6, 179, 1, #000000h, 308);
  TEXTOUT_P("runs = " + rk_Cm(STRING(rkSt, 2, 0)) + ", mean " + rk_Cm(rk_Fx(rkMu, 2)) + ": " + IFTE(rkEx == 1 AND rkMode == 1, "exact ", "normal ") + rk_PT(rk_PMain()) + ", " + rk_TailW(), G1, 6, 191, 1, rkBLUE, 308);
  IF rkUCh == 1 THEN
    rk_Foot("tap the chart, " + rkLR + " = pick, " + rkUD + " = page, Esc = back");
  ELSE
    rk_Foot("tap a square, " + rkLR + " = pick, " + rkUD + " = page, Esc = back");
  END;
END;


''')

# ---------------- the null distribution page ----------------
rep('''  IF rkTest <= 3 AND rkMode == 1 THEN RETURN 1; END;
  IF rkTest == 6 THEN RETURN 1; END;
  RETURN 0;
''', '''  IF rkTest <= 3 AND rkMode == 1 THEN RETURN 1; END;
  IF rkTest == 6 THEN RETURN 1; END;
  IF rkTest >= 7 AND rkMode == 1 THEN RETURN 1; END;
  RETURN 0;
''')
rep('''  IF rkTail == 2 THEN RETURN IFTE(itV >= rkNObs - 1E-9, 1, 0); END;
  itM := 2 * rkNMu - rkNObs;
''', '''  IF rkTail == 2 THEN RETURN IFTE(itV >= rkNObs - 1E-9, 1, 0); END;
  // beta 1j: the runs' null is not symmetric (unless n1 = n2), so its
  // two-sided p is twice the SMALLER tail and only that tail is marked
  IF rkTest == 8 THEN
    IF rkPeL <= rkPeU THEN RETURN IFTE(itV <= rkNObs + 1E-9, 1, 0); END;
    RETURN IFTE(itV >= rkNObs - 1E-9, 1, 0);
  END;
  itM := 2 * rkNMu - rkNObs;
''')
rep('''// rk_CvKind: which curve the Null page draws: 1 normal (mean rkMu, SD
// rkSd, the statistic's own scale), 2 chi-square (df rkDf), 3 Student
// t (df rkDf, Spearman), 4 standard normal (Kendall's z).
rk_CvKind()
BEGIN
  IF rkTest <= 3 THEN RETURN 1; END;
''', '''// rk_CvKind: which curve the Null page draws: 1 normal (mean rkMu, SD
// rkSd, the statistic's own scale), 2 chi-square (df rkDf), 3 Student
// t (df rkDf, Spearman), 4 standard normal (Kendall's z), 5 (beta 1j:
// Page's L, the runs test) normal as 1 but with no continuity
// correction, so the p region is cut at the statistic itself.
rk_CvKind()
BEGIN
  IF rkTest >= 7 THEN RETURN 5; END;
  IF rkTest <= 3 THEN RETURN 1; END;
''')
rep('''  IF rkTest <= 5 THEN RETURN rkSt; END;
  IF rkCWh == 2 THEN RETURN rkKz; END;
''', '''  IF rkTest <= 5 OR rkTest >= 7 THEN RETURN rkSt; END;
  IF rkCWh == 2 THEN RETURN rkKz; END;
''')
rep('''  IF dsK == 1 THEN RETURN NORMALD(rkMu, rkSd, dsX); END;
''', '''  IF dsK == 1 OR dsK == 5 THEN RETURN NORMALD(rkMu, rkSd, dsX); END;
''')
rep('''  IF cuK == 1 THEN RETURN NORMALD_CDF(0, 1, (rkMu - cuV) / rkSd); END;
''', '''  IF cuK == 1 OR cuK == 5 THEN RETURN NORMALD_CDF(0, 1, (rkMu - cuV) / rkSd); END;
''')
rep('''  IF rkTail == 1 THEN RETURN IFTE(chX <= chO, 1, 0); END;
  IF rkTail == 2 THEN RETURN IFTE(chX >= chO, 1, 0); END;
  RETURN IFTE(ABS(chX) >= ABS(chO), 1, 0);
''', '''  IF rkTail == 1 THEN RETURN IFTE(chX <= chO, 1, 0); END;
  IF rkTail == 2 THEN RETURN IFTE(chX >= chO, 1, 0); END;
  // beta 1j: kind 5 is centered on its mean, not on 0
  IF chK == 5 THEN RETURN IFTE(ABS(chX - rkMu) >= ABS(chO - rkMu), 1, 0); END;
  RETURN IFTE(ABS(chX) >= ABS(chO), 1, 0);
''')
rep('''  IF cfK == 1 THEN
    rkCvA := rkMu - 4 * rkSd; rkCvB := rkMu + 4 * rkSd;
''', '''  IF cfK == 1 OR cfK == 5 THEN
    rkCvA := rkMu - 4 * rkSd; rkCvB := rkMu + 4 * rkSd;
''')
rep('''  IF cfK >= 3 THEN
    cfL := MAX(4, 1.15 * ABS(cfO));
''', '''  IF cfK == 3 OR cfK == 4 THEN
    cfL := MAX(4, 1.15 * ABS(cfO));
''')
rep('''    IF rkTest == 3 THEN
      nlS := "Exact null of U" + CHAR(8321) + ": all C(" + rk_Cm(STRING(rkN, 2, 0)) + ", " + rk_Cm(STRING(MIN(rkKn(1), rkKn(2)), 2, 0)) + ") splits";
    END;
''', '''    IF rkTest == 3 THEN
      nlS := "Exact null of U" + CHAR(8321) + ": all C(" + rk_Cm(STRING(rkN, 2, 0)) + ", " + rk_Cm(STRING(MIN(rkKn(1), rkKn(2)), 2, 0)) + ") splits";
    END;
    // beta 1j
    IF rkTest == 7 THEN
      nlS := "Exact null of L: every order in each of the " + rk_Cm(STRING(rkFB, 2, 0)) + " blocks";
    END;
    IF rkTest == 8 THEN
      nlS := "Exact null of the runs: all C(" + rk_Cm(STRING(rkN, 2, 0)) + ", " + rk_Cm(STRING(MIN(rkUN1, rkUN2), 2, 0)) + ") orders";
    END;
''')
rep('''    IF nlK == 4 THEN nlS := "Standard normal (null of Kendall's z)"; END;
  END;
''', '''    IF nlK == 4 THEN nlS := "Standard normal (null of Kendall's z)"; END;
    IF nlK == 5 THEN nlS := "Normal approx. of " + rk_SNm() + ": mean " + rk_Cm(rk_Num(ROUND(rkMu, 2))) + ", SD " + rk_Cm(rk_Fx(rkSd, 2)); END;
  END;
''')
# the last axis number is kept on the screen (a number is never cut by its width argument)
rep('''  LOCAL nlY, nlMx, nlBw, nlCol, nlK;
  LOCAL nlO, nlPx, nlS, nlT, nlCm, nlCt;
''', '''  LOCAL nlY, nlMx, nlBw, nlCol, nlK, nlLx;
  LOCAL nlO, nlPx, nlS, nlT, nlCm, nlCt;
''')
rep('''  nlT := rk_Nice((nlB - nlA) / 6);
  nlV := CEILING(nlA / nlT) * nlT;
  WHILE nlV <= nlB DO
''', '''  nlT := rk_Nice((nlB - nlA) / 6);
  nlV := CEILING(nlA / nlT) * nlT;
  nlLx := -100;                               // where the last number written ends
  WHILE nlV <= nlB DO
''')
rep('''    TEXTOUT_P(rk_Cm(rk_Num(nlV)), G1, nlPx - 8, rkPB + 4, 1, rkGRAY, 40);
    nlV := nlV + nlT;
''', '''    // beta 1j: a number that would run past the screen's right edge is
    // moved left to end on it (6 pixels a character at the most), and
    // left out when it would then touch the number before it; the tick
    // stays.  Until beta 1i it ran off the screen ("250,000" from x = 297).
    nlS := rk_Cm(rk_Num(nlV));
    nlX1 := MIN(nlPx - 8, 319 - 6 * DIM(nlS));
    IF nlX1 >= nlLx + 4 THEN
      TEXTOUT_P(nlS, G1, nlX1, rkPB + 4, 1, rkGRAY, MAX(40, 6 * DIM(nlS)));
      nlLx := nlX1 + 6 * DIM(nlS);
    END;
    nlV := nlV + nlT;
''')
rep('''  IF nlBars == 1 OR rk_CvKind() == 1 THEN
    nlPx := rkPL + IP((IFTE(nlBars == 1, rkNMu, rkMu) - nlA) / (nlB - nlA) * nlW);
''', '''  IF nlBars == 1 OR rk_CvKind() == 1 OR rk_CvKind() == 5 THEN
    nlPx := rkPL + IP((IFTE(nlBars == 1, rkNMu, rkMu) - nlA) / (nlB - nlA) * nlW);
''')
# the mended fault: "infinite" is for Spearman's t of a perfect order (rk_CvObs's 1E6), not for a big statistic
rep('''  nlS := rk_NNm() + " = " + IFTE(ABS(nlO) >= 1E5, "infinite", rk_Cm(rk_Num(ROUND(nlO, 3))));
''', '''  // beta 1j: "infinite" is for Spearman's t of a perfect order only
  // (rk_CvObs hands back 1E6 there); until beta 1i any statistic of
  // 100,000 or more read "infinite" (U with two groups of 500)
  nlS := rk_NNm() + " = " + IFTE(rkTest == 6 AND ABS(nlO) >= 1E5, "infinite", rk_Cm(rk_Num(ROUND(nlO, 3))));
''')
rep('''  TEXTOUT_P(nlS, G1, MAX(rkPL + 2, MIN(rkPR - 7 * DIM(nlS) - 2, nlPx + 3)), rkPT + 2, 1, rkRED, 120);
''', '''  IF rkTest >= 7 AND nlO < IFTE(nlBars == 1, rkNMu, rkMu) THEN
    // beta 1j (tests 7 and 8): a statistic below the mean is named on the
    // left of its line, away from the hump of the distribution
    TEXTOUT_P(nlS, G1, MAX(rkPL + 2, nlPx - 3 - 6 * DIM(nlS)), rkPT + 2, 1, rkRED, 6 * DIM(nlS) + 12);
  ELSE
    TEXTOUT_P(nlS, G1, MAX(rkPL + 2, MIN(rkPR - 7 * DIM(nlS) - 2, nlPx + 3)), rkPT + 2, 1, rkRED, 120);
  END;
''')
rep('''    IF rkTest <= 3 THEN
      nlS := rk_SNm() + " = " + rk_Cm(rk_Num(rkSt)) + ": normal " + rk_PT(rkPn) + ", " + rk_TailW();
    ELSE
''', '''    IF rkTest <= 3 OR rkTest >= 7 THEN
      nlS := rk_SNm() + " = " + rk_Cm(rk_Num(rkSt)) + ": normal " + rk_PT(rkPn) + ", " + rk_TailW();
    ELSE
''')
rep('''    IF rkTest == 6 THEN nlS := "magenta = the p tail(s); bars = orders of y"; END;
  ELSE
''', '''    IF rkTest == 6 THEN nlS := "magenta = the p tail(s); bars = orders of y"; END;
    // beta 1j: the runs' two-sided p is twice the smaller tail
    IF rkTest == 8 AND rkTail == 0 THEN nlS := "magenta = the smaller tail; two-sided p = twice it"; END;
  ELSE
''')

# ---------------- the view ----------------
rep('''  IF rkTest <= 3 THEN RETURN IFTE(rkMode == 1 AND rkEx == 1, "Exact", "Normal"); END;
  IF rkTest == 4 THEN RETURN IFTE(rkKRk == 1, "Ranks", "Values"); END;
''', '''  IF rkTest <= 3 OR rkTest >= 7 THEN RETURN IFTE(rkMode == 1 AND rkEx == 1, "Exact", "Normal"); END;
  IF rkTest == 4 THEN RETURN IFTE(rkKRk == 1, "Ranks", "Values"); END;
''')
rep('''  IF rkTest == 4 OR rkTest == 5 THEN RETURN "Upper"; END;
  IF rkTail == 1 THEN RETURN "Lower"; END;
''', '''  IF rkTest == 4 OR rkTest == 5 THEN RETURN "Upper"; END;
  // beta 1j: Page's L has a direction
  IF rkTest == 7 THEN RETURN IFTE(rkTail == 1, "Falling", "Rising"); END;
  IF rkTail == 1 THEN RETURN "Lower"; END;
''')
rep('''      IF rkTest == 6 THEN rk_PgScat(); END;
    END;
''', '''      IF rkTest == 6 THEN rk_PgScat(); END;
      IF rkTest == 7 THEN rk_PgTrend(); END;
      IF rkTest == 8 THEN rk_PgRuns(); END;
    END;
''')
rep('''    IF rkTest == 6 THEN dwA := IFTE(rkCDat == 1, "Data", "Ranks"); END;
    DRAWMENU({"Help", dwA, "", "", "Menu", "More"});
''', '''    IF rkTest == 6 THEN dwA := IFTE(rkCDat == 1, "Data", "Ranks"); END;
    // beta 1j: a sequence of numbers has two pictures (the key says which is on)
    IF rkTest == 8 AND SIZE(rkUVal) > 0 THEN dwA := IFTE(rkUCh == 1, "Chart", "Cells"); END;
    DRAWMENU({"Help", dwA, "", "", "Menu", "More"});
''')
rep('''    IF rkTest == 6 THEN rkCSel := MAX(1, MIN(rkN, rkCSel + pkD)); END;
    RETURN 0;
''', '''    IF rkTest == 6 THEN rkCSel := MAX(1, MIN(rkN, rkCSel + pkD)); END;
    IF rkTest == 7 THEN rkLSel := MAX(1, MIN(rkFK, rkLSel + pkD)); END;
    IF rkTest == 8 THEN rkUSel := MAX(1, MIN(rkN, rkUSel + pkD)); END;
    RETURN 0;
''')
rep('''      pkN := rk_CvObs();
      IF ABS(pkN) >= 1E5 THEN pkN := rkCvB; END;
''', '''      pkN := rk_CvObs();
      // beta 1j: only Spearman's t of a perfect order is "infinite"
      IF rkTest == 6 AND ABS(pkN) >= 1E5 THEN pkN := rkCvB; END;
''')
before('''  IF rkPg == 4 THEN
    IF tpY >= 108 AND tpY < 108 + 6 * 13 THEN
''', '''  // beta 1j: Page's L: the treatment whose column was tapped
  IF rkPg == 2 AND rkTest == 7 THEN
    IF tpX >= 34 AND tpX <= 308 AND tpY >= 20 AND tpY <= 158 THEN
      rkLSel := MAX(1, MIN(rkFK, IP((tpX - 34) / (274 / rkFK)) + 1));
    END;
    RETURN 0;
  END;
  // beta 1j: the runs test: the value nearest the finger on the chart,
  // or the square under it
  IF rkPg == 2 AND rkTest == 8 THEN
    IF rkUCh == 1 THEN
      IF tpX >= 40 AND tpX <= 312 AND tpY >= 40 AND tpY <= 160 THEN
        rkUSel := MAX(1, MIN(rkN, ROUND((tpX - 46) / 260 * (rkN - 1), 0) + 1));
      END;
    ELSE
      rk_RuGeo();
      tpC := IP((tpX - 10) / rkUC);
      tpR := IP((tpY - rkUY0) / (rkUC + 2));
      IF tpX >= 10 AND tpY >= rkUY0 AND tpC < rkUPer THEN
        tpI := tpR * rkUPer + tpC + 1;
        IF tpI >= 1 AND tpI <= MIN(2000, rkN) THEN rkUSel := tpI; END;
      END;
    END;
    RETURN 0;
  END;
''')
rep('''  IF acA == 4 THEN
    IF rkTest <= 3 THEN
      IF rkEx == 0 THEN
''', '''  IF acA == 4 THEN
    IF rkTest <= 3 OR rkTest >= 7 THEN
      IF rkEx == 0 THEN
''')
rep('''  IF acA == 5 THEN
    IF rkTest == 4 OR rkTest == 5 THEN
''', '''  // beta 1j: Page's L switches between its two directions
  IF acA == 5 AND rkTest == 7 THEN
    rkTail := 3 - rkTail;
    rk_Pick();
  END;
  IF acA == 5 AND rkTest <> 7 THEN
    IF rkTest == 4 OR rkTest == 5 THEN
''')
rep('''    IF rkTest == 6 THEN rkCDat := 1 - rkCDat; rkPg := 2; END;
  END;
  IF acA == 14 THEN RETURN rk_Act(rk_Menu()); END;
''', '''    IF rkTest == 6 THEN rkCDat := 1 - rkCDat; rkPg := 2; END;
    // beta 1j: the runs test of a sequence of numbers: squares or chart
    IF rkTest == 8 AND SIZE(rkUVal) > 0 THEN
      IF rkUCh == 0 AND rkN > 400 THEN
        MSGBOX("The chart is drawn for up to 400 values (here n = " + rk_Cm(STRING(rkN, 2, 0)) + "): the squares show every one.");
      ELSE
        rkUCh := 1 - rkUCh; rkPg := 2;
      END;
    END;
  END;
  IF acA == 14 THEN RETURN rk_Act(rk_Menu()); END;
''')
rep('''  LOCAL muI, muL;
  muI := 0;
  IF rkTest <= 3 THEN muL := "Exact / normal (now " + IFTE(rkMode == 1 AND rkEx == 1, "exact", "normal") + ")"; END;
''', '''  LOCAL muI, muL, muT;
  muI := 0;
  // beta 1j: Page's L and the runs test switch exact / normal as tests 1 to
  // 3 do; Page's fifth item is its direction
  muT := "Tails (now " + rk_TailW() + ")";
  IF rkTest == 7 THEN muT := "Direction (now " + rk_TailW() + ")"; END;
  IF rkTest <= 3 OR rkTest >= 7 THEN muL := "Exact / normal (now " + IFTE(rkMode == 1 AND rkEx == 1, "exact", "normal") + ")"; END;
''')
rep('''  IF rkTest == 4 OR rkTest == 6 THEN
    CHOOSE(muI, rk_TName(), {"Result page", "Picture page", "Null distribution", muL, "Tails (now " + rk_TailW() + ")", IFTE(rkTest == 4, "Dunn pairs", "Scatter: data or ranks"), "Help", "Back to the main menu"});
''', '''  IF rkTest == 4 OR rkTest == 6 OR (rkTest == 8 AND SIZE(rkUVal) > 0) THEN
    CHOOSE(muI, rk_TName(), {"Result page", "Picture page", "Null distribution", muL, muT, IFTE(rkTest == 4, "Dunn pairs", IFTE(rkTest == 6, "Scatter: data or ranks", "Picture: squares or chart")), "Help", "Back to the main menu"});
''')
rep('''  CHOOSE(muI, rk_TName(), {"Result page", "Picture page", "Null distribution", muL, "Tails (now " + rk_TailW() + ")", "Help", "Back to the main menu"});
''', '''  CHOOSE(muI, rk_TName(), {"Result page", "Picture page", "Null distribution", muL, muT, "Help", "Back to the main menu"});
''')
rep('''  rkTail := 0; rkMode := 1;
  IF opT == 3 THEN
''', '''  rkTail := 0; rkMode := 1;
  // beta 1j: Page's L opens in the direction its data set names
  IF opT == 7 THEN rkTail := rkLDir; END;
  IF opT == 3 THEN
''')

# ---------------- help: 10 pages (7 before) ----------------
rep('''// rk_HPage: one help page of up to 13 lines (font 1, 46 characters);
// returns the key that closed it.
''', '''// rk_HPage: one help page of up to 13 lines (font 1, 296 pixels);
// returns the key that closed it.
''')
rep('''  TEXTOUT_P("Page " + rk_Cm(STRING(hpN, 2, 0)) + "/7: key = next, " + CHAR(8592) + " = back, Esc = leave", G1, 10, 220, 1, rkFOOT, 300);
''', '''  TEXTOUT_P("Page " + rk_Cm(STRING(hpN, 2, 0)) + "/10: key = next, " + CHAR(8592) + " = back, Esc = leave", G1, 10, 220, 1, rkFOOT, 300);
''')
rep('''// rk_Help: seven pages; Left goes back a page, Esc leaves.
''', '''// rk_Help: ten pages (beta 1j; seven before); Left goes back a page,
// Esc leaves.
''')
rep('''  WHILE hlP >= 1 AND hlP <= 7 DO
''', '''  WHILE hlP >= 1 AND hlP <= 10 DO
''')
for n, t in ((1, 'What it does'), (2, 'Keys and touch'), (3, 'Sign test, signed-rank'), (4, 'Mann-Whitney, Kruskal-Wallis'), (5, 'Friedman, W, correlation')):
    rep('      hlT := "RankLab help %d/7: %s";\n' % (n, t), '      hlT := "RankLab help %d/10: %s";\n' % (n, t))
# page 2: the Tails key of Page's L
rep('''        "- = Tails: two-sided, lower, upper",
''', '''        "- = Tails: two-sided, lower, upper (Page's L: rising, falling)",
''')
# old page 6 becomes 8, old page 7 is split into 9 (data, Home) and 10 (credits); pages 6 and 7 are new
HELP6 = ['Friedman asks whether the treatments differ at all.  PAGE\'S L',
         'asks more: do they rise in the ORDER LISTED (column 1, 2, 3 ...)?',
         'Rank within each block (row), as Friedman does.  Then',
         '*L = 1 @X@ R@1@ + 2 @X@ R@2@ + ... + k @X@ Rk     (R = a column\'s rank sum)',
         'A block whose ranks follow the order adds the most to L.',
         'The 5th soft key (or -) switches Rising and Falling.  Choose the',
         'order and the direction BEFORE you see the data.',
         '*EXACT p: under @H0@ every order of a block\'s ranks is equally',
         '*likely.  RankLab counts them all for a small table (3 columns:',
         '*up to %d blocks; 5: %d; 9: %d; fewer with ties), ties as they are.' % (LIM[3], LIM[5], LIM[9]),
         'NORMAL: z = (L - mean)/SD, with no continuity correction.',
         'Plot: each column\'s mean rank, in order.  Friedman opens the',
         'same data (menu item 5) and shows the ranks in each block.']
HELP7 = ['THE RUNS TEST asks whether the ORDER of a sequence is',
         'random.  It is not a rank test: it only counts.  A RUN is a',
         'stretch of the same kind:  R R R R B R R R  has 3 runs.',
         'Two kinds (red or black, pass or fail) are used as they are.',
         'Numbers are cut at their median into above and below; a value',
         'equal to the median is dropped.',
         '*TOO FEW runs: like values cluster (a drift, a trend, streaks).',
         '*TOO MANY runs: the two kinds alternate more than chance does.',
         'Tails: lower = too few, upper = too many, two-sided = either.',
         'EXACT p: every order of the two kinds is equally likely under',
         '@H0@; RankLab counts the orders (n @LE@ 2,000).',
         'NORMAL: z = (runs - mean)/SD, mean = 2 n@1@ n@2@/n + 1.',
         'Plot: a square for each value; numbers also as a chart (More).']
HELP9 = ['Presets (source on every page): Rossi',
         'recidivism, the 1970 draft lottery, Darwin\'s',
         'Zea mays, judges\' ratings, a mock jury (KW',
         'uses attractiveness only; Crime is ignored),',
         'ozone and airway resistance, a roulette wheel.',
         'Your data: Statistics 1Var D1..D9; groups =',
         'columns; paired D1 - D2; one sample D1 vs m@0@;',
         'correlation D1, D2; Friedman and Page\'s L:',
         'rows = blocks; runs: D1 in the order it happened.',
         '*Home: RK_STAT, RK_P (exact when there is',
         '*one), RK_PN, RK_EFF, RK_HL, RK_RANKS.']
HELP10 = ['Does what Michael Lloyd\'s TI-83/84 programs',
          'for Triola do (SRTEST, RSTEST, KWTEST, SRCORR,',
          'ZZRANK), without their tie, zero, rs errors.',
          'Written new for the Prime: none of their code.',
          'The runs test does what Hewlett-Packard\'s Run Test',
          'for Randomness did on the HP-65 (Stat Pac 2, 1975)',
          'and the HP-67/97.  Those took the two counts and the',
          'number of runs, keyed in, and gave the mean, the SD',
          'and z.  RankLab counts the runs itself and adds the',
          'exact p.  The roulette example is theirs.  Written',
          'new: none of their code.',
          'Page\'s L is written from its formulas (Page 1963).']


def ppl_str(line):
    """one help line as a PPL string expression; the glyphs are built from the program's own variables"""
    out = '"' + line + '"'
    for tag, expr in (('@X@', 'rkTX'), ('@H0@', 'rkH0'), ('@LE@', 'rkLE'), ('@1@', 'CHAR(8321)'), ('@2@', 'CHAR(8322)'), ('@0@', 'CHAR(8320)')):
        out = out.replace(tag, '" + ' + expr + ' + "')
    return out.replace(' + ""', '').replace('"" + ', '')


def shown(line):
    """the line as the screen shows it (for measuring): the tags as their glyphs, the leading * taken off"""
    for tag, ch in (('@X@', chr(215)), ('@H0@', 'H' + chr(8320)), ('@LE@', chr(8804)), ('@1@', chr(8321)), ('@2@', chr(8322)), ('@0@', chr(8320))):
        line = line.replace(tag, ch)
    return line[1:] if line.startswith('*') else line


def page(n, title, lines):
    if len(lines) > 13: sys.exit('BUILD STOPPED: help page %d has %d lines (13 at most)' % (n, len(lines)))
    for ln in lines:
        if px(shown(ln)) > 296: sys.exit('BUILD STOPPED: help page %d, a line of %d pixels (296 at most): %r' % (n, px(shown(ln)), ln))
    if px('RankLab help %d/10: %s' % (n, title), 2) > 296: sys.exit('BUILD STOPPED: help title %d too wide' % n)
    return ('    IF hlP == %d THEN\n      hlT := "RankLab help %d/10: %s";\n      hlL := {\n        ' % (n, n, title)
            + ',\n        '.join(ppl_str(ln) for ln in lines) + '};\n    END;\n')


a = s.index('    IF hlP == 6 THEN\n      hlT := "RankLab help 6/7: Exact or normal; the p-value";')
b = s.index('    hlK := rk_HPage(hlT, hlL, hlP);')
old67 = s[a:b]
if old67.count('IF hlP == 6 THEN') != 1 or old67.count('IF hlP == 7 THEN') != 1: sys.exit('BUILD STOPPED: help pages 6 and 7 not found as expected')
old6 = old67[:old67.index('    IF hlP == 7 THEN')]
new8 = old6.replace('IF hlP == 6 THEN', 'IF hlP == 8 THEN').replace('RankLab help 6/7: Exact or normal; the p-value', 'RankLab help 8/10: Exact or normal; the p-value')
x = '''        "and, with ties, the tie-corrected variance.",
'''
if new8.count(x) != 1: sys.exit('BUILD STOPPED: help page 6, the variance line')
new8 = new8.replace(x, x + '''        "(Page's L and the runs test: z without that correction.)",
''')
x = '''        "Friedman: upper only."};
'''
if new8.count(x) != 1: sys.exit('BUILD STOPPED: help page 6, the last line')
new8 = new8.replace(x, '''        "Friedman: upper only.  Page's L: rising or falling."};
''')
s = (s[:a] + '    // beta 1j: pages 6 and 7 are new; the old page 6 is page 8; the old page 7 is pages 9 and 10\n'
     + page(6, "Page's L, an ordered trend", HELP6) + page(7, 'The runs test', HELP7) + new8
     + page(9, 'Data and Home', HELP9) + page(10, 'Credits', HELP10) + s[b:])
for ln in ('(Page\'s L and the runs test: z without that correction.)', 'Friedman: upper only.  Page\'s L: rising or falling.',
           '- = Tails: two-sided, lower, upper (Page\'s L: rising, falling)'):
    if px(ln) > 296: sys.exit('BUILD STOPPED: a changed help line of %d pixels: %r' % (px(ln), ln))

# ---------------- the welcome page ----------------
rep('''  TEXTOUT_P("RankLab - rank tests, beta 1i", G1, 8, 4, 3, #FFFFFFh, 304);
  TEXTOUT_P("Sign, Wilcoxon signed-rank, Mann-Whitney,", G1, 10, 32, 1, rkBLUE, 300);
  TEXTOUT_P("Kruskal-Wallis, Dunn, Friedman, Kendall's W,", G1, 10, 45, 1, rkBLUE, 300);
  TEXTOUT_P("Spearman and Kendall rank correlation.", G1, 10, 58, 1, rkBLUE, 300);
''', '''  TEXTOUT_P("RankLab - rank tests, beta 1j", G1, 8, 4, 3, #FFFFFFh, 304);
  TEXTOUT_P("Sign, Wilcoxon signed-rank, Mann-Whitney,", G1, 10, 32, 1, rkBLUE, 300);
  TEXTOUT_P("Kruskal-Wallis, Dunn, Friedman, Kendall's W,", G1, 10, 45, 1, rkBLUE, 300);
  // beta 1j: the third line names the two new tests
  TEXTOUT_P("Page's L, Spearman, Kendall, the runs test.", G1, 10, 58, 1, rkBLUE, 300);
''')

# ---------------- the closing line ----------------
rep('''  IF rkTest <= 3 THEN
    suS := suS + rk_Cm(rk_Num(rkSt)) + ", " + IFTE(rkEx == 1 AND rkMode == 1, "exact ", "normal ");
  ELSE
''', '''  // beta 1j: Page's L names its blocks and treatments; the runs test
  // reads as tests 1 to 3 do
  IF rkTest == 7 THEN
    RETURN "RankLab: Page's L, b = " + rk_Cm(STRING(rkFB, 2, 0)) + ", k = " + rk_Cm(STRING(rkFK, 2, 0)) + ", L = " + rk_Cm(rk_Num(rkSt)) + ", " + IFTE(rkEx == 1 AND rkMode == 1, "exact ", "normal ") + rk_PT(suP) + " (" + rk_TailW() + ")";
  END;
  IF rkTest <= 3 OR rkTest == 8 THEN
    suS := suS + rk_Cm(rk_Num(rkSt)) + ", " + IFTE(rkEx == 1 AND rkMode == 1, "exact ", "normal ");
  ELSE
''')

# ---------------- the main menu: the old items keep their numbers ----------------
rep('''    CHOOSE(mnI, "RankLab: rank-based tests", {"Sign test (1 sample/paired)", "Wilcoxon signed-rank", "Mann-Whitney (rank-sum)", "Kruskal-Wallis + Dunn", "Friedman + Kendall's W", "Rank correlation (rs, tau-b)", "Load a preset", "Use my data (D1..D9)", "Help", "Quit"});
    IF mnI == 0 OR mnI == 10 THEN mnRun := 0; END;
''', '''    // beta 1j: items 9 and 10 (the menu shows 10 as A) are the two new
    // tests; items 1 to 8 keep their numbers, Help and Quit follow
    CHOOSE(mnI, "RankLab: rank-based tests", {"Sign test (1 sample/paired)", "Wilcoxon signed-rank", "Mann-Whitney (rank-sum)",
      "Kruskal-Wallis + Dunn", "Friedman + Kendall's W", "Rank correlation (rs, tau-b)", "Load a preset", "Use my data (D1..D9)",
      "Page's L (ordered trend)", "Runs test (randomness)", "Help", "Quit"});
    IF mnI == 0 OR mnI == 12 THEN mnRun := 0; END;
''')
rep('''    IF mnI == 9 THEN rk_Help(); END;
  END;
''', '''    IF mnI == 9 THEN rk_Open(7); END;
    IF mnI == 10 THEN rk_Open(8); END;
    IF mnI == 11 THEN rk_Help(); END;
  END;
''')

# ---------------- the file map: counted here ----------------
a = s.index('// ============================================================\n// FILE MAP (line numbers of beta 1b)')
b = s.index('// ---- Home exports (set after every computation) ----')
s = s[:a] + '''// ============================================================
// FILE MAP (line numbers of this file; beta 1j: counted by the build)
//   @M1@   Home exports and the file-level state
//   @M2@   SMALL HELPERS
//                  rk_Cm, rk_Init, rk_Drain, rk_WaitAny, rk_Nice, rk_Fx, rk_Sg,
//                  rk_Num, rk_PT, rk_TailW, rk_GCol, rk_Trunc, rk_Zeros, rk_Prog,
//                  rk_Esc, rk_Grp
//   @M3@   RANKS
//                  rk_Midrank, rk_Order, rk_Med, rk_Q7
//   @M4@   TAIL PROBABILITIES
//                  rk_PZ, rk_CCZ, rk_ChiUp, rk_TUp
//   @M5@   THE TESTS
//                  rk_Diffs, rk_Fill, rk_Walsh, rk_Shift, rk_NullWin, rk_NSum,
//                  rk_DoSign, rk_SRNull, rk_DoSR, rk_MWNull, rk_DoMW, rk_DoKW,
//                  rk_DoFr, rk_FrRbar, rk_TieSums, rk_Kendall, rk_SpPerm,
//                  rk_KdNull, rk_DoCorr, rk_CorrP, rk_CorNull; beta 1j: rk_LOne,
//                  rk_LBlock, rk_LNull, rk_DoPage, rk_RuNull, rk_RuEnd,
//                  rk_DoRuns, rk_RuFrom; rk_Pick, rk_Compute
//   @M6@   THE PRESETS
//                  rk_DraftNo, rk_LdRossi, rk_LdDraftG, rk_LdDraftC, rk_LdDarwin,
//                  rk_LdHalo, rk_LdJudges, rk_LdJury; beta 1j: rk_LdOzone,
//                  rk_LdDraftM, rk_LdRoul, rk_LdDraftR; rk_Preset, rk_ReadD,
//                  rk_MyData, rk_ChooseG, rk_PickTwo, rk_Ensure
//   @M7@   DRAWING: frames, text, the result page
//                  rk_Frame, rk_Box, rk_Ln, rk_Foot, rk_TName, rk_TSh, rk_SNm,
//                  rk_Src, rk_TieTx, rk_PMain, rk_CKind, rk_Verd, rk_ExLine,
//                  rk_MeanR, rk_PgRes
//   @M8@   THE RANK STRIP
//                  rk_PgStrip, rk_StripInfo
//   @M9@   KRUSKAL-WALLIS: GROUP BOXES, DUNN PAIRS
//                  rk_PgBox, rk_PgDunn
//   @M10@   FRIEDMAN: THE RANK GRID
//                  rk_PgGrid
//   @M11@   RANK CORRELATION: THE SCATTER
//                  rk_PgScat
//   @M12@   beta 1j: PAGE'S L, THE RUNS TEST: THEIR PICTURES
//                  rk_LOrd, rk_PgTrend, rk_RuGeo, rk_AxS, rk_AxW, rk_RuCells,
//                  rk_RuChart, rk_PgRuns
//   @M13@   THE NULL DISTRIBUTION
//                  rk_IsBars, rk_NNm, rk_InTail, rk_CvKind, rk_CvObs, rk_Dens,
//                  rk_CvUp, rk_CvShade, rk_CvFit, rk_PgNull
//   @M14@   THE VIEW: pages, soft keys, keys and taps
//                  rk_NPg, rk_K4, rk_K5, rk_Draw, rk_Pick1, rk_Tap, rk_Act,
//                  rk_Menu, rk_View, rk_Open
//   @M15@   HELP, THE WELCOME PAGE, THE ENTRY POINT
//                  rk_HPage, rk_Help, rk_Welcome, rk_Summary, RankLab
// ============================================================

''' + s[b:]


def line_of(text):
    if s.count(text) != 1: sys.exit('BUILD STOPPED: %d matches for the file map anchor %r' % (s.count(text), text[:60]))
    return s.count('\n', 0, s.index(text)) + 1


BAR = '// ============================================================\n'
starts = [('M1', line_of('// ---- Home exports (set after every computation) ----')), ('M2', line_of(BAR + '// SMALL HELPERS')),
          ('M3', line_of(BAR + '// RANKS')), ('M4', line_of(BAR + '// TAIL PROBABILITIES')), ('M5', line_of(BAR + '// THE TESTS')),
          ('M6', line_of(BAR + '// THE PRESETS')), ('M7', line_of(BAR + '// DRAWING: frames')), ('M8', line_of(BAR + '// THE RANK STRIP')),
          ('M9', line_of(BAR + '// KRUSKAL-WALLIS: GROUP BOXES')), ('M10', line_of(BAR + '// FRIEDMAN: THE RANK GRID')),
          ('M11', line_of(BAR + '// RANK CORRELATION: THE SCATTER')), ('M12', line_of(BAR + "// beta 1j: PAGE'S L (the mean ranks in order)")),
          ('M13', line_of(BAR + '// THE NULL DISTRIBUTION')), ('M14', line_of(BAR + '// THE VIEW: pages')), ('M15', line_of(BAR + '// HELP, THE WELCOME PAGE'))]
if [v for (_, v) in starts] != sorted(v for (_, v) in starts): sys.exit('BUILD STOPPED: the sections are not in the order the file map lists them')
total = len(s.split('\n')) - 1
for k, (tag, a0) in enumerate(starts):
    b0 = (starts[k + 1][1] - 2) if k + 1 < len(starts) else total
    rep('@%s@' % tag, '%4d-%-4d' % (a0, b0))
if re.search(r'@[A-Z0-9]+@', s): sys.exit('BUILD STOPPED: a placeholder is left: %r' % re.findall(r'@[A-Z0-9]+@', s)[:5])
bad = [ln for ln in s.split('\n') if len(ln) > 330]
if bad: sys.exit('BUILD STOPPED: a line of more than 330 characters: %r' % bad[0][:80])

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'RankLab_beta1j.txt'), 'w', encoding='utf-8', newline='').write(s)
print('RankLab_beta1j.txt written:', total, 'lines;  exact Page limits without ties, k = 3..9:', [LIM[k] for k in range(3, 10)],
      ' with one tied block:', [LIMT[k] for k in range(3, 10)])
