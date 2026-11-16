# -*- coding: utf-8 -*-
"""Round 16 (15 Nov 2026): CICatcher beta 2l from beta 2k, by exact replacements (a miss stops the build).

New in beta 2l (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please"; this is the fifth):
  * A SIXTH INTERVAL, THE TOLERANCE INTERVAL  xbar +/- k s, made to hold at least 90 % (or 95 %, or 99 %) of the whole
    population, with the confidence the slider shows.  The samples are a t run's (normal values, s from the sample); the
    line is blue when it holds at least that share of the population and red when it holds less.  The middle share of
    the population is a green band behind the lines; the panel of a picked line says how much it holds.
  * THE FACTOR k IS EXACT (not Howe's approximation, which many tables and guides give: 2.838 against 2.856 at n = 10).  With the sample
    mean d sigmas from the true mean, the interval must reach rho(d) each way, where Phi(d + rho) - Phi(d - rho) = p; it
    does when s >= sigma rho / k.  So the confidence of a factor k is
        g(k) = 1 - 2 INT_0^inf phi(t) P( chi-square(n - 1) < (n - 1) rho(t / root n)^2 / k^2 ) dt,
    by 12-point Gauss-Legendre on 0..6 (g to 1E-6, k to 3E-6: verify_CICatcher_beta2l.py), and k solves g(k) = level by
    the secant rule from Howe's value.  The catch level of a sample is g(k*) for its own k* = sigma rho(d) / s: one
    integral, no root finding, so the long-run tally follows the slider exactly, as for the other five intervals.
  * Written from the formulas (Wald & Wolfowitz 1946; Howe 1969 for the start).  No other program was read for it: the
    library in D:\\HP-Prime holds no program that computes a tolerance factor (searched 15 Nov 2026).
  * Help: seven pages (page 5, Tolerance intervals, is new).  The closing line of a tolerance run says what was counted.
    It is short enough for the five-line box in which the Program Catalog shows what a program returns ("CICatcher: 107 of
    111 held at least 95 % of the population (96.4 %) at 95 %, n = 10"): the first wording, with "tolerance intervals",
    "tol. 95 %,", the population's mu and sigma and "see CQ_COVER" in it, lost its end there (Virtual Calculator, 15 Nov
    2026).
Every screen of the other five intervals is beta 2k's; the help pages' count aside ("n/7" for "n/6").
Run from the repository's root:   python3 verify/round16/make_cicatcher_2l.py OUTDIR
"""
import io, os, subprocess, sys, textwrap
import numpy as np
BASE = '4e8ff66'; DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r16_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/CICatcher_beta2k.txt'], check=True, capture_output=True).stdout.decode('utf-8')


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)


def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)


# the 12-point Gauss-Legendre rule: its six positive nodes and their weights, from NumPy (never typed)
gx, gw = np.polynomial.legendre.leggauss(12)
GX = ', '.join('%.12f' % v for v in gx[6:]); GWT = ', '.join('%.12f' % v for v in gw[6:])

# ---------------- header ----------------
rep('// CICATCHER - beta 2k\n', '// CICATCHER - beta 2l\n')
note = ('Round 16 (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please").  A sixth interval, '
        'the TOLERANCE interval xbar +/- k s: made to hold at least 90 % (or 95 %, or 99 %) of the whole population, with '
        'the confidence the slider shows.  Its samples are a t run\'s; a line is blue when it holds at least that share '
        'of the population, red when it holds less; the middle share of the population is a green band; the panel of a '
        'picked line says how much it holds.  The factor k is exact: the confidence of a factor is an integral over the '
        'sample mean\'s position (cqTolG, 12-point Gauss-Legendre), solved for k by the secant rule from Howe\'s (1969) '
        'value (cqTolK); a sample\'s catch level is that integral at its own k (cqTolCat), so the tally follows the '
        'slider exactly.  Written from the formulas; the library in D:\\HP-Prime holds no program that computes a '
        'tolerance factor (searched 15 Nov 2026).  Help has seven pages (5 is new).  Every screen of the other five '
        'intervals is beta 2k\'s, the help pages\' count aside.')
before('// beta 2k (14 Nov 2026):', '// beta 2l (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')
after('''//   to "95 % of WHAT?": 95 % of the intervals the method makes.
''', '''//   beta 2l: the same count for a TOLERANCE interval, xbar +/- k s,
//   which is not about the mean at all: it is made to hold at least
//   90 % (or 95 %, 99 %) of the population's values.  "95 % of WHAT?"
//   has the same answer: 95 % of the intervals the method makes hold
//   that share.
''')
after('''//                              its interval, caught or missed
''', '''//   Tolerance runs (beta 2l) . a light green band, the middle 90 %
//                              (95 %, 99 %) of the population, in
//                              place of the green line; BLUE = the
//                              line holds at least that share of the
//                              population, RED = it holds less; the
//                              panel says how much it holds
''')

# ---------------- state ----------------
rep('''//  cqType 1 mean z, 2 mean t, 3 proportion Wald, 4 Wilson
''', '''//  cqType 1 mean z, 2 mean t, 3 proportion Wald, 4 Wilson,
//         5 Exact; a tolerance run (beta 2l) is cqType 2 with
//         cqTol = 1: the same samples, another interval
''')
rep('''LOCAL cqFOOT, cqGRID, cqLBLU, cqLRED, cqLORN, cqLGRY;
''', '''LOCAL cqFOOT, cqGRID, cqLBLU, cqLRED, cqLORN, cqLGRY;
LOCAL cqLGRN;

// ---- beta 2l: the tolerance interval ----
LOCAL cqTol, cqTP, cqTZ, cqTZp, cqTN, cqTW;
LOCAL cqTR;
//  cqTol 1 = this run draws TOLERANCE intervals xbar +/- k s (its
//        samples are a t run's, so cqType is 2); 0 otherwise
//  cqTP  the share of the population the interval is to hold:
//        0.90, 0.95 or 0.99
//  cqTZ  z of the middle cqTP (1.645 for 0.90): the green band is
//        mu +/- cqTZ sigma;  cqTZp  z of cqTP one-sided (1.282)
//  cqTN, cqTW  the 12 Gauss-Legendre nodes t on 0..6, and their
//        weights times the normal density at t
//  cqTR  rho at each node: how far each way, in sigmas, an interval
//        whose centre is t / root n sigmas off the mean must reach
//        to hold cqTP of the population
''')

# ---------------- the arithmetic: routines of its own ----------------
before('''// ------------------------------------------------------------
// THE FIVE INTERVALS
// ------------------------------------------------------------
''', '''// ------------------------------------------------------------
// beta 2l.  THE TOLERANCE INTERVAL  xbar +/- k s
//
// It is to hold at least the share p (cqTP) of a normal population
// with confidence g: in the share g of all samples of n.  Work in
// sigmas from the true mean.  A sample whose mean is d sigmas off
// needs its interval to reach rho(d) each way, where
//     Phi(d + rho) - Phi(d - rho) = p,
// and xbar +/- k s reaches that far when s >= sigma rho(d) / k.  The
// mean and s are independent, so averaging over the mean's position
// (d = t / root n, t standard normal) gives the confidence of k:
//     g(k) = 1 - 2 INT_0^inf phi(t)
//                P( chi-square(n - 1) < (n - 1) rho(t / root n)^2 / k^2 ) dt.
// This is the exact factor (Wald & Wolfowitz 1946 set the problem up
// this way).  Howe's (1969) approximation is what many tables and
// guides give, and it differs from the exact factor in the third
// digit: 2.838 against 2.856 at n = 10, p = 0.90, g = 0.95.
// The integral is done by 12-point Gauss-Legendre on
// 0..6 (the density beyond 6 is 1E-9): g to 1E-6 and k to 3E-6 for
// n = 2 to 100, p = 0.90, 0.95, 0.99 and g = 0.5 to 0.999, against
// adaptive quadrature, and a simulation of 400,000 samples
// (verify_CICatcher_beta2l.py).  Every term is a lower tail times a
// positive weight, so nothing cancels.
// ------------------------------------------------------------

// rho(d): Phi(d + r) - Phi(d - r) = cqTP for a centre trD >= 0 sigmas
// off the mean.  The root lies between d + z(p) and d + z((1 + p)/2).
// Newton's rule from the upper end, every step kept inside those
// bounds; the slope phi(d + r) + phi(d - r) is at least phi(z((1 +
// p)/2)) there, never near 0.  8 steps at most (PC harness: 1 to 6).
cqTolRho(trD)
BEGIN
  LOCAL trLo, trHi, trR, trF, trS, trI;
  trLo := trD + cqTZp; trHi := trD + cqTZ;
  trR := trHi;
  FOR trI FROM 1 TO 8 DO
    trF := NORMALD_CDF(0, 1, trD + trR) - NORMALD_CDF(0, 1, trD - trR) - cqTP;
    trS := trF / (NORMALD(0, 1, trD + trR) + NORMALD(0, 1, trD - trR));
    trR := MAX(trLo, MIN(trHi, trR - trS));
    IF ABS(trS) < 1E-11 THEN BREAK; END;
  END;
  RETURN trR;
END;

// The tables of a tolerance run, for its n and its cqTP: the two z
// values, the 12 nodes t on 0..6 with their weights times phi(t), and
// rho at t / root n.  The rule's six positive nodes and weights on
// -1..1 are NumPy's leggauss(12), written here to 12 digits; the pair
// -x and +x move to t = 3 (1 - x) and t = 3 (1 + x), weight 3 w.
cqTolSet()
BEGIN
  LOCAL tsX, tsW, tsI, tsT;
  tsX := {@GX@};
  tsW := {@GW@};
  cqTZ := NORMALD_ICDF(0, 1, (1 + cqTP) / 2);
  cqTZp := NORMALD_ICDF(0, 1, cqTP);
  cqTN := MAKELIST(0, tsI, 1, 12);
  cqTW := MAKELIST(0, tsI, 1, 12);
  cqTR := MAKELIST(0, tsI, 1, 12);
  FOR tsI FROM 1 TO 6 DO
    tsT := 3 * (1 - tsX(tsI));
    cqTN(tsI) := tsT;
    cqTW(tsI) := 3 * tsW(tsI) * NORMALD(0, 1, tsT);
    tsT := 3 * (1 + tsX(tsI));
    cqTN(tsI + 6) := tsT;
    cqTW(tsI + 6) := 3 * tsW(tsI) * NORMALD(0, 1, tsT);
  END;
  FOR tsI FROM 1 TO 12 DO
    cqTR(tsI) := cqTolRho(cqTN(tsI) / cqN^0.5);
  END;
END;

// g(k): the confidence of the factor tgK (the formula above).  The
// sum is the miss rate (1 - g)/2, built from lower tails only; g is
// used from 0.5 up, where 1 - 2 x sum keeps its digits.
cqTolG(tgK)
BEGIN
  LOCAL tgI, tgS, tgC;
  tgS := 0;
  tgC := cqDF / (tgK * tgK);
  FOR tgI FROM 1 TO 12 DO
    tgS := tgS + cqTW(tgI) * CHISQUARE_CDF(cqDF, tgC * cqTR(tgI) * cqTR(tgI));
  END;
  RETURN 1 - 2 * tgS;
END;

// k for the confidence tkG (0.5 to 0.999): g(k) = tkG.  Start from
// Howe's (1969) approximation,
//     k0 = z root( (n - 1)(1 + 1/n) / chi-square quantile(1 - g; n - 1) ),
// which is within 8 % of the answer everywhere here, and a second
// point 3 % off on the root's side; then the secant rule.  The steps
// are counted: 40 at most (the PC harness takes 3 to 6).
cqTolK(tkG)
BEGIN
  LOCAL tkA, tkB, tkFa, tkFb, tkC, tkI;
  tkA := cqTZ * (cqDF * (1 + 1 / cqN) / CHISQUARE_ICDF(cqDF, MAX(0.0005, MIN(0.5, 1 - tkG))))^0.5;
  tkFa := cqTolG(tkA) - tkG;
  IF tkFa < 0 THEN tkB := 1.03 * tkA; ELSE tkB := 0.97 * tkA; END;
  tkFb := cqTolG(tkB) - tkG;
  FOR tkI FROM 1 TO 40 DO
    IF tkFb == tkFa THEN BREAK; END;
    tkC := tkB - tkFb * (tkB - tkA) / (tkFb - tkFa);
    IF tkC <= 0 THEN tkC := tkB / 2; END;
    tkA := tkB; tkFa := tkFb;
    tkB := tkC; tkFb := cqTolG(tkB) - tkG;
    IF ABS(tkB - tkA) < 1E-9 * tkB THEN BREAK; END;
  END;
  RETURN tkB;
END;

// The catch level of one tolerance interval: the lowest level, in
// thousandths from 500 to 999, at which xbar +/- k s holds at least
// cqTP of the population; 1000 if it does not even at 99.9 %.  The
// interval holds enough when k is at least k* = sigma rho(d) / s
// (d = |xbar - mu| / sigma), and the factor of level L is at least
// k* exactly when g(k*) <= L / 1000, because g rises with k.  So the
// catch level is g(k*), rounded up: one integral, no root finding.
cqTolCat(tcE, tcS)
BEGIN
  LOCAL tcK;
  // s = 0 would need n identical values: an interval of no width
  IF tcS <= 0 THEN RETURN 1000; END;
  tcK := cqSg * cqTolRho(ABS(tcE - cqMu) / cqSg) / tcS;
  RETURN MAX(500, MIN(1000, CEILING(1000 * cqTolG(tcK))));
END;

// How much of the population lies inside thLo .. thHi, in percent
// (two lower tails of N(mu, sigma)).
cqTolHold(thLo, thHi)
BEGIN
  RETURN 100 * (NORMALD_CDF(cqMu, cqSg, thHi) - NORMALD_CDF(cqMu, cqSg, thLo));
END;

// The middle cqTP of the population, mu +/- cqTZ sigma, as a light
// green band behind the lines (tbW = 1, drawn before the grid) and
// as its two green edges (tbW = 2, drawn over the grid).
cqTolBand(tbW)
BEGIN
  LOCAL tbA, tbB;
  tbA := cqPXi(cqMu - cqTZ * cqSg);
  tbB := cqPXi(cqMu + cqTZ * cqSg);
  IF tbW == 1 THEN
    IF MIN(cqPR, tbB) > MAX(cqPL, tbA) THEN
      RECT_P(G1, MAX(cqPL, tbA), cqPT, MIN(cqPR, tbB), cqAY - 1, cqLGRN, cqLGRN);
    END;
  ELSE
    IF tbA >= cqPL AND tbA <= cqPR THEN LINE_P(G1, tbA, cqPT, tbA, cqAY - 1, cqGRN); END;
    IF tbB >= cqPL AND tbB <= cqPR THEN LINE_P(G1, tbB, cqPT, tbB, cqAY - 1, cqGRN); END;
  END;
END;

''')

# ---------------- hooks in the old routines (each does nothing unless cqTol = 1) ----------------
# the critical value: k root n, so that cqLimits' t line (cqCV s / root n) is k s
rep('''  crI := crL - 499;
  IF cqCVc(crI) > 0 THEN RETURN cqCVc(crI); END;
''', '''  crI := crL - 499;
  IF cqCVc(crI) > 0 THEN RETURN cqCVc(crI); END;
  // beta 2l: a tolerance run keeps k root n here, so that the t
  // interval's half-width, cqCV s / root n (cqLimits), is k s
  IF cqTol == 1 THEN
    crV := cqTolK(crL / 1000) * cqN^0.5;
    cqCVc(crI) := crV;
    RETURN crV;
  END;
''')
rep('''  LOCAL ctQ, ctLv, ctC;
  ctLv := 0;
''', '''  LOCAL ctQ, ctLv, ctC;
  // beta 2l: a tolerance interval has a catch level of its own
  IF cqTol == 1 THEN RETURN cqTolCat(ctE, ctS); END;
  ctLv := 0;
''')
rep('''  wnW := 6.5 * wnSE;
''', '''  wnW := 6.5 * wnSE;
  // beta 2l: a tolerance interval reaches about k sigma each way, not
  // a few standard errors: its window is the mean +/- 1.625 k sigma,
  // k the factor at 95 %.  (The panel's decimals stay those of the t
  // run: they come from sigma / root n, below.)
  IF cqTol == 1 THEN wnW := 1.625 * cqSg * cqTolK(0.95); END;
''')
rep('''  cqOff := 0; cqGrow := -1;
  cqCV := cqCrit(cqL);
''', '''  cqOff := 0; cqGrow := -1;
  // beta 2l: the tables of a tolerance run, before its first factor
  IF cqTol == 1 THEN cqTolSet(); END;
  cqCV := cqCrit(cqL);
''')
rep('''cqDesc()
BEGIN
  IF cqType == 1 THEN
''', '''cqDesc()
BEGIN
  // beta 2l: a tolerance run names the share of the population
  IF cqTol == 1 THEN
    RETURN "tol. " + cqCm(STRING(100 * cqTP, 2, 0)) + " %, " + cqMuS + " = " + cqCm(cqNumS(cqMu)) + ", " + cqSgS + " = " + cqCm(cqNumS(cqSg)) + ", n = " + cqCm(STRING(cqN, 2, 0));
  END;
  IF cqType == 1 THEN
''')
rep('''  LOCAL daLX, daR;
  IF cqType >= 3 THEN
''', '''  LOCAL daLX, daR;
  // beta 2l: the middle of the population as a band, under the grid
  IF cqTol == 1 THEN cqTolBand(1); END;
  IF cqType >= 3 THEN
''')
rep('''  // the truth: two pixels wide, from the top of the stack to the axis
  daX := cqPXi(cqTruth());
  LINE_P(G1, daX, cqPT, daX, cqAY - 1, cqGRN);
  LINE_P(G1, daX + 1, cqPT, daX + 1, cqAY - 1, cqGRN);
END;
''', '''  // beta 2l: a tolerance run has no single value to catch: the two
  // edges of its band take the place of the truth line
  IF cqTol == 1 THEN
    cqTolBand(2);
    RETURN;
  END;
  // the truth: two pixels wide, from the top of the stack to the axis
  daX := cqPXi(cqTruth());
  LINE_P(G1, daX, cqPT, daX, cqAY - 1, cqGRN);
  LINE_P(G1, daX + 1, cqPT, daX + 1, cqAY - 1, cqGRN);
END;
''')
rep('''  pnTxt := pnTxt + ": " + cqCm(cqF(pnLim(1), cqVDec)) + " to " + cqCm(cqF(pnLim(2), cqVDec));
  IF pnGrw == 0 THEN
    IF cqCat(pnS) <= cqL THEN
''', '''  pnTxt := pnTxt + ": " + cqCm(cqF(pnLim(1), cqVDec)) + " to " + cqCm(cqF(pnLim(2), cqVDec));
  // beta 2l: a tolerance interval's line says how much of the
  // population it holds, with as many decimals as it takes for a red
  // line's share to read below the share it was to hold
  IF pnGrw == 0 AND cqTol == 1 THEN
    pnD := cqTolHold(pnLim(1), pnLim(2));
    pnDD := 1;
    IF cqCat(pnS) > cqL THEN
      WHILE ROUND(pnD, pnDD) >= 100 * cqTP AND pnDD < 6 DO pnDD := pnDD + 1; END;
    END;
    pnTxt := pnTxt + ", holds " + cqCm(cqF(pnD, pnDD)) + " %";
  END;
  IF pnGrw == 0 AND cqTol == 0 THEN
    IF cqCat(pnS) <= cqL THEN
''')

# ---------------- the setup: a sixth item ----------------
rep('''  LOCAL suH1, suH2, suH3, suH4, suGo;
  suTy := 0;
''', '''  LOCAL suH1, suH2, suH3, suH4, suGo;
  LOCAL suTl, suTp;
  suTy := 0;
''')
rep('''    "Proportion: Wilson (score)",
    "Proportion: Exact (C-P)"});
  IF suTy == 0 THEN RETURN 0; END;
''', '''    "Proportion: Wilson (score)",
    "Proportion: Exact (C-P)",
    "Tolerance: " + cqXb + " " + CHAR(177) + " k s"});
  IF suTy == 0 THEN RETURN 0; END;
  // beta 2l: item 6, the tolerance interval.  Its samples are a t
  // run's, so from here on it is type 2 with suTl = 1; the share of
  // the population it is to hold is asked first.  Nothing of the old
  // run changes until the form below has been accepted.
  suTl := 0; suTp := cqTP;
  IF suTy == 6 THEN
    suTy := 0;
    CHOOSE(suTy, "Tolerance: hold how much?", {
      "90 % of the population",
      "95 % of the population",
      "99 % of the population"});
    IF suTy == 0 THEN RETURN 0; END;
    suTp := 0.9;
    IF suTy == 2 THEN suTp := 0.95; END;
    IF suTy == 3 THEN suTp := 0.99; END;
    suTl := 1; suTy := 2;
  END;
''')
rep('''  cqType := suTy;
  IF suTy <= 2 THEN
    cqMu := suTr; cqSg := suSD; cqNm := suNn;
''', '''  cqType := suTy;
  cqTol := suTl; cqTP := suTp;         // beta 2l
  IF suTy <= 2 THEN
    cqMu := suTr; cqSg := suSD; cqNm := suNn;
''')

# ---------------- help: seven pages ----------------
for n in (1, 2, 3, 4):
    rep('hpK := cqPage("CICatcher help %d/6: ' % n, 'hpK := cqPage("CICatcher help %d/7: ' % n)
rep('hpK := cqPage("CICatcher help 5/6: A criminal-justice example", {', '''// beta 2l: the tolerance interval (k at n = 10, 95 %, 90 % of the
  // population is checked in verify_CICatcher_beta2l.py)
  hpK := cqPage("CICatcher help 5/7: Tolerance intervals", {"A confidence interval is about a mean.  A tolerance interval is",
    "about single values: " + cqXb + " " + CHAR(177) + " k s is made to hold at least 90 % (or",
    "95 %, or 99 %) of the whole population.",
    "",
    "The green band is the middle 90 % of the population.  A blue",
    "line holds at least 90 % of the population; a red line holds less.",
    "Tap a line: the panel says how much of the population it holds.",
    "",
    "The level is the share of samples whose line holds its 90 %:",
    "the 'all' rate at the top settles near it.",
    "k is larger than z = 1.645 because " + cqXb + " and s are estimates: at",
    "n = 10 and 95 %, k = @K10@.  k is worked out exactly here;",
    "printed tables often give an approximation that differs in the",
    "third digit."},
    {hpN, hpN, hpN, hpN, hpY, hpB, hpB, hpN, hpM, hpM, hpN, hpN, hpG, hpG}, hpF);
  IF hpK == 4 THEN RETURN; END;

  hpK := cqPage("CICatcher help 6/7: A criminal-justice example", {''')
rep('hpK := cqPage("CICatcher help 6/6: Keys and touch", {', 'hpK := cqPage("CICatcher help 7/7: Keys and touch", {')
rep('''// Six pages (beta 2; five in beta 1); any key or tap turns the page,
// Esc leaves.
''', '''// Seven pages (beta 2l; six in beta 2, five in beta 1); any key or
// tap turns the page, Esc leaves.
''')

# ---------------- init ----------------
rep('''  cqLRED := #FFEBEBh; cqLORN := #FFF0DCh; cqLGRY := #E6E6E6h;
''', '''  cqLRED := #FFEBEBh; cqLORN := #FFF0DCh; cqLGRY := #E6E6E6h;
  cqLGRN := #D2EFD9h;                       // beta 2l: the tolerance band
''')
rep('''  cqType := 1;
  cqMu := 100; cqSg := 15; cqNm := 10;
''', '''  cqType := 1;
  cqTol := 0; cqTP := 0.9;                  // beta 2l: no tolerance run yet
  cqMu := 100; cqSg := 15; cqNm := 10;
''')

# ---------------- the closing line ----------------
rep('''  RETURN "CICatcher: " + cqCm(STRING(cqHit, 2, 0)) + " of " + cqCm(STRING(cqTot, 2, 0)) + " caught the truth (" + cqCm(cqPct(cqHit, cqTot)) + " %) at " + cqCm(cqLvS(cqL)) + " %, " + cqDesc() + "; see CQ_COVER";
''', '''  // beta 2l: a tolerance run says what its intervals were counted for.
  // The line is kept short: run from the Program Catalog, the calculator
  // shows what a program returns in a box of five lines of about 26
  // characters, and a longer sentence lost its end there (Virtual
  // Calculator, 15 Nov 2026).  So it gives n and leaves out mu and sigma,
  // which a tolerance interval's catch rate does not depend on, and the
  // pointer to CQ_COVER (help page 7 names the Home variables): with them
  // a run of 1,000 intervals or more still lost its last words.
  IF cqTol == 1 THEN
    RETURN "CICatcher: " + cqCm(STRING(cqHit, 2, 0)) + " of " + cqCm(STRING(cqTot, 2, 0)) + " held at least " + cqCm(STRING(100 * cqTP, 2, 0)) + " % of the population (" + cqCm(cqPct(cqHit, cqTot)) + " %) at " + cqCm(cqLvS(cqL)) + " %, n = " + cqCm(STRING(cqN, 2, 0));
  END;
  RETURN "CICatcher: " + cqCm(STRING(cqHit, 2, 0)) + " of " + cqCm(STRING(cqTot, 2, 0)) + " caught the truth (" + cqCm(cqPct(cqHit, cqTot)) + " %) at " + cqCm(cqLvS(cqL)) + " %, " + cqDesc() + "; see CQ_COVER";
''')

# ---------------- numbers that come from the arithmetic, not from memory ----------------
from scipy import stats
def rho_v(x, p):
    ax = np.abs(x); lo = ax + stats.norm.ppf(p); hi = ax + stats.norm.ppf((1 + p)/2); r = hi.copy()
    for _ in range(60):
        f = stats.norm.cdf(ax + r) - stats.norm.cdf(ax - r) - p
        r = np.minimum(hi, np.maximum(lo, r - f/(stats.norm.pdf(ax + r) + stats.norm.pdf(ax - r))))
    return r
def k_exact(n, p, g, N=400, T=10.0):
    x, w = np.polynomial.legendre.leggauss(N); t = T/2*(x + 1); wf = T/2*w*stats.norm.pdf(t); rh = rho_v(t/np.sqrt(n), p)
    from scipy.optimize import brentq
    return brentq(lambda k: 1 - 2*float((wf*stats.chi2.cdf((n - 1)*rh*rh/(k*k), n - 1)).sum()) - g, 0.1, 5000, xtol=1e-13)
K10 = k_exact(10, 0.90, 0.95)
rep('@K10@', '%.3f' % K10)
rep('@GX@', GX); rep('@GW@', GWT)

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'CICatcher_beta2l.txt'), 'w', encoding='utf-8', newline='').write(s)
print('CICatcher_beta2l.txt written:', len(s.split('\n')) - 1, 'lines;  k(10, 0.90, 0.95) = %.6f' % K10)
