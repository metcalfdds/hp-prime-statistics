# -*- coding: utf-8 -*-
"""Round 16 (15 Nov 2026): FitCheck beta 1i from beta 1h, by exact replacements (a miss stops the build).

New in beta 1i (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please"; this is the fourth):
  * DIXON'S OUTLIER TEST for a small sample (3 to 30 values): the normality pages' fifth soft key, Outlier, opens a page
    with every value as a dot on a strip, the tested value in red, its gap and its range as brackets, the ratio
    (r10, r11, r21 or r22 by n: Dixon's 1953 scheme), its p at that end, the p for either end (twice it) and a
    sentence at alpha = 0.05.
  * THE P IS COMPUTED, not read from a table.  Given the anchor a = x(j) and the largest value b = x(n), the
    m = n - j - 1 values between them are independent draws from the normal curve cut to (a, b), and "ratio > R"
    says that fewer than i of them lie above c = b - R (b - a):
        P(ratio > R) = n!/((j-1)! m!) INT INT_{a<b} F(a)^(j-1) f(a) f(b) [G^m + (i-1) m G^(m-1) (H - G)] da db,
        G = F(c) - F(a),  H = F(b) - F(a),
    by 20 x 20 Gauss-Legendre points over the region where x(j) and x(n) live (fc_DxTail).
  * A PRESET: Darwin's 15 differences (the two negative ones stand far below the rest; n = 15 takes r22, which the
    second low value does not mask, where the simple ratio r10 would see nothing).
  * A FAULT MENDED: a sample refused because every value is the same no longer replaces the loaded sample's sorted
    values first (until beta 1h "The last sample again" then met lists of two lengths: a run-time error).
  * AXIS NUMBERS MENDED (found by this round's layout check, with data in the thousands and beyond): the last number of
    the chi-square curve's and of the ECDF's axis could run past the screen's right edge; a data value wider than its
    40 pixels was cut on the Q-Q plot's y axis and on the ECDF's x axis.  A number is kept on the screen now, and an
    axis with a number too wide for its room is written in the Prime's scientific form, all of it.
  * Help: 12 pages (8 before): three on the test, and the Home variables on a page of their own.
  * Written from the formulas (Dixon 1950, 1951, 1953; McBane 2006 computes the same distribution by quadrature).  No
    other program was read for the arithmetic: the library in D:\\HP-Prime holds no program with Dixon's test
    (searched 15 Nov 2026; the TI STATCALC "Outlier test" is the 1.5 IQR fences).
Every other screen is beta 1h's, the help pages' count, the opening page's list and those axis numbers aside.
Run from the repository's root:   python3 verify/round16/make_fitcheck_1i.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap
import numpy as np
BASE = '4e8ff66'; DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r16_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/FitCheck_beta1h.txt'], check=True, capture_output=True).stdout.decode('utf-8')


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)


def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)


# the 20-point Gauss-Legendre rule on (-1, 1): nodes and weights from NumPy (never typed), 12 decimals, five to a line
gx, gw = np.polynomial.legendre.leggauss(20)
def five(v): return ',\n    '.join(', '.join('%.12f' % t for t in v[k:k + 5]) for k in range(0, 20, 5))
GX, GWT = five(gx), five(gw)

# what the verify script found for fc_DxTail (kept in one place: the header note and the section heading both say it)
ERRS = ('at every n from 3 to 30 its relative error is under 0.05 % for a p above 0.001 and under 0.2 % for a p above '
        '0.0001 (verify_FitCheck_beta1i.py: against a fine-grid reference, the closed form at n = 3, simulation and '
        'McBane\'s 2006 values)')

# ---------------- header ----------------
rep('// FITCHECK - beta 1h  (15 Nov 2026)\n', '// FITCHECK - beta 1i  (15 Nov 2026)\n')
note = ('Round 16 (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please").  DIXON\'S OUTLIER TEST '
        'for a small sample (3 to 30 values): the normality pages\' fifth soft key, Outlier, opens a page with every value '
        'as a dot on a strip, the tested value in red, its gap and its range as brackets, the ratio (r10, r11, r21 or r22 '
        'by n: Dixon\'s 1953 scheme), its p at that end, the p for either end (twice it) and a sentence at alpha = 0.05.  '
        'The p is computed (fc_DxTail: a double integral over the anchor and the largest value, 20 x 20 Gauss-Legendre '
        'points), not read from a table: ' + ERRS + '.  A new preset, Darwin\'s 15 differences (n = 15 takes r22, which the second '
        'low value does not mask).  A fault mended: a sample refused because every value is the same no longer replaces '
        'the loaded sample\'s values first (until beta 1h "The last sample again" then stopped with a run-time error).  '
        'Axis numbers mended (found by this round\'s layout check): the last number of the chi-square curve\'s and the '
        'ECDF\'s axis could run past the screen\'s right edge, and a data value wider than its 40 pixels was cut on the '
        'Q-Q plot\'s y axis and the ECDF\'s x axis; a number is now kept on the screen, and an axis with a number too '
        'wide is written in the Prime\'s scientific form (fc_AxLb, fc_AxWide).  '
        'Help has 12 pages (8 before): three on the test, and the Home variables on a page of their own; Home gets FC_R '
        'and FC_PR.  Written from the formulas; the library in D:\\HP-Prime holds no program with Dixon\'s test (searched '
        '15 Nov 2026).  Every other screen is beta 1h\'s, the help pages\' count, the opening page\'s list and those axis numbers aside.')
before('// beta 1h (15 Nov 2026): Round 15', '// beta 1i (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')
after('''//   observed count and the p-value region, on a scale of SDs.
''', '''//   beta 1i: Dixon's outlier test for a small sample (the Outlier key of the
//   normality pages): every value as a dot on a strip, the tested value in
//   red, its gap and its range as brackets, the ratio and its p.
''')
after('''//   binomial test's two-sided p).
''', '''//   beta 1i: FC_R, FC_PR (Dixon's ratio and its either-end p).
''')
after('''//   log-gamma: Lanczos (1964), g = 7, nine coefficients.
''', '''//   Dixon's outlier test (beta 1i): the ratios r10, r11, r21, r22 of Dixon
//     (1950) Ann. Math. Stat. 21:488 and (1951) Ann. Math. Stat. 22:68; which
//     ratio for which n (3-7, 8-10, 11-13, 14-30): Dixon (1953) Biometrics
//     9:74, as NIST's Dataplot and R's dixonTest apply it.  The p is a double
//     integral over the standard normal (fc_DxTail), by 20 x 20 Gauss-
//     Legendre points; McBane (2006) J. Stat. Softw. 16(3) computes the same
//     distribution by quadrature and lists the errors of the printed tables.
//     Either-end p = twice the one-end p (the rule of the two-sided tables).
''')
after('''//   Binomial fit example: illustrative numbers (made up), labelled so.
''', '''//   Darwin's maize (beta 1i): the 15 differences in height, crossed minus
//     self-fertilized, in inches (Fisher's eighths of an inch divided by 8):
//     Darwin (1876); Fisher (1935) The Design of Experiments (the pairs are
//     RankLab's Darwin preset, checked there against R's HistData ZeaMays).
''')
rep('''// File map: (line numbers of this file)
//   EXPORTs and file-level LOCALs ......................... 144-233
//   small helpers: init, waits, progress, text, wrap ...... 235-538
//   special functions: log-gamma, Phi, ln Phi, chi-square
//     upper tail (incomplete gamma) ......................... 540-652
//   the chi-square fit engine: cells, check, merging ....... 654-867
//   fits: Benford, Poisson, binomial, normal on bins ....... 869-1086
//   normality: W, A^2, D, loading a sample ................ 1088-1329
//   exact binomial test (logs) 1331-1459; Fisher's exact 2 x 2 1461-1499
//   pictures and pages: chi-square fit 1501-1978, normality
//     1980-2357, binomial test 2359-2607
//   presets 2609-2811; your own data, D1 and D2 2813-2961
//   help and the title page 2963-3058; the menu items 3060-3178
//   FitCheck(), the entry point ........................... 3180-end
''', '''// File map: (line numbers of this file; beta 1i: counted by the build)
//   EXPORTs and file-level LOCALs ......................... @M1@
//   small helpers: init, waits, progress, text, wrap ...... @M2@
//   special functions: log-gamma, Phi, ln Phi, chi-square
//     upper tail (incomplete gamma) ......................... @M3@
//   the chi-square fit engine: cells, check, merging ....... @M4@
//   fits: Benford, Poisson, binomial, normal on bins ....... @M5@
//   normality: W, A^2, D, loading a sample ................ @M6@
//   exact binomial test (logs) @M7@; Fisher's exact 2 x 2 @M8@
//   pictures and pages: chi-square fit @M9@; Dixon's outlier
//     test, its arithmetic and its page @M10@; normality
//     @M11@; binomial test @M12@
//   presets @M13@; your own data, D1 and D2 @M14@
//   help and the title page @M15@; the menu items @M16@
//   FitCheck(), the entry point ........................... @M17@
''')

# ---------------- exports and state ----------------
after('''EXPORT FC_PA, FC_D, FC_PD, FC_BP;
''', '''EXPORT FC_R, FC_PR;                  // beta 1i: Dixon's ratio and its either-end p
''')
rep('''//  6 Rossi, 7 draft, 8 illustrative binomial); fcHasF 1 once a fit
''', '''//  6 Rossi, 7 draft, 8 illustrative binomial; 9, beta 1i, Darwin's
//  differences, a normality sample only); fcHasF 1 once a fit
''')
after('''//  fcEb) and the tapped column (-1 none); fcTSrc the binomial test's
//  source line.
''', '''
// ---- beta 1i: Dixon's outlier test ----
LOCAL fcDxOK, fcDxI, fcDxJ, fcDxRL, fcDxRH, fcDxP;
LOCAL fcDxE, fcDxGX, fcDxGW, fcDxPx, fcDxLv, fcDxMx;
//  fcDxOK 1 once the test is worked out for the loaded sample; fcDxI and
//  fcDxJ say which ratio: the gap runs from the tested value to the
//  fcDxI-th value in from it, the range to the fcDxJ-th value from the far
//  end (r10: 1, 1; r11: 1, 2; r21: 2, 2; r22: 2, 3); fcDxRL, fcDxRH the
//  ratio at the low and at the high end; fcDxP the one-end p of the bigger;
//  fcDxE the end tested (1 low, 2 high); fcDxGX, fcDxGW the 20 Gauss-
//  Legendre nodes and weights; fcDxPx, fcDxLv each value's pixel and level
//  on the dot strip, fcDxMx the highest level.
''')

# ---------------- init ----------------
rep('''  fcTCol := {0};
END;
''', '''  fcTCol := {0};
  // beta 1i: Dixon's test: nothing worked out yet; and the 20-point Gauss-
  // Legendre rule on (-1, 1), nodes then weights (written by the build from
  // NumPy's leggauss(20), never typed)
  fcDxOK := 0; fcDxI := 1; fcDxJ := 1; fcDxRL := 0; fcDxRH := 0; fcDxP := 1;
  fcDxE := 2; fcDxPx := {0}; fcDxLv := {0}; fcDxMx := 0;
  fcDxGX := {@GX@};
  fcDxGW := {@GW@};
END;
''')

# ---------------- loading a sample: a refused one changes nothing; a new one clears Dixon's test ----------------
rep('''// and D.  Returns 0 (with a message) for fewer than 3 values, more than
// 5000, or no spread.
''', '''// and D.  Returns 0 (with a message) for fewer than 3 values, more than
// 5000, or no spread; beta 1i: and then nothing of the loaded sample has
// been touched.
''')
rep('''  LOCAL nsD;
  nsN := SIZE(nsV);
''', '''  LOCAL nsD, nsSv;
  nsN := SIZE(nsV);
''')
rep('''  fcX := SORT(nsV); fcNX := nsN; fcBin := 0;
''', '''  // beta 1i: a refused sample changes nothing (read into locals, check,
  // then assign).  Until beta 1h "every value the same" was found after the
  // sorted values and the mean had replaced the loaded sample's, and "The
  // last sample again" then drew a Q-Q plot from lists of two lengths: a
  // run-time error.  The spread is looked at first now; the two checks
  // further down stay as they were and can no longer be reached.
  nsSv := SORT(nsV);
  IF nsSv(nsN) <= nsSv(1) THEN MSGBOX("Every value is the same: s = 0, so there is no shape to test."); RETURN 0; END;
  fcX := nsSv; fcNX := nsN; fcBin := 0;
  fcDxOK := 0;                         // beta 1i: Dixon's test belongs to the sample it was worked out for
''')
rep('''  fcX := {}; fcZq := {};
''', '''  fcX := {}; fcZq := {};
  fcDxOK := 0;                         // beta 1i
''')

# ---------------- Dixon's test: the arithmetic and the page ----------------
before('''// ============================================================
// PICTURES AND PAGES OF THE NORMALITY TESTS
''', '''// ============================================================
// beta 1i: DIXON'S OUTLIER TEST for a small sample (fc_Dx*, fc_DrawDx)
//   Is the lowest or the highest value of a sample of 3 to 30 values too
//   far from the rest to come from the same normal population?  With the
//   values sorted, x(1) <= ... <= x(n), Dixon's ratio for the HIGHEST is
//       r(i, j-1) = (x(n) - x(n-i)) / (x(n) - x(j))    a gap over a range
//   and its mirror image for the lowest.  Which ratio, by n (Dixon 1953,
//   as NIST's Dataplot and R's dixonTest apply it):
//       n 3-7:   r10 (i = 1, j = 1)     n 8-10:  r11 (i = 1, j = 2)
//       n 11-13: r21 (i = 2, j = 2)     n 14-30: r22 (i = 2, j = 3)
//   THE P is computed, not read from a table.  Given the anchor a = x(j)
//   and the largest value b = x(n), the m = n - j - 1 values between them
//   are independent draws from the normal curve cut to (a, b), and
//   "ratio > R" says that fewer than i of them lie above c = b - R (b - a).
//   So, with f and F the standard normal density and CDF,
//     P(ratio > R) = n!/((j-1)! m!) INT INT_{a<b} F(a)^(j-1) f(a) f(b)
//                    [G^m + (i-1) m G^(m-1) (H - G)] da db,
//     G = F(c) - F(a),  H = F(b) - F(a),
//   every term positive.  fc_DxTail takes 20 x 20 Gauss-Legendre points
//   over the region where x(j) and x(n) live: each around its Blom centre
//   z((k - 3/8)/(n + 1/4)), 7 large-sample standard deviations each way,
//   with b from max(a, its lower end).  @ERRL@
//   The test takes the end with the bigger ratio, so the p it reports is
//   for EITHER end: twice the one-end p, the rule of the printed two-sided
//   tables.  Twice is an upper limit: the two ends' ratios can be large
//   together (when the middle values lie close).  It is exact for r10
//   above 0.5, where the two ratios cannot both be; at the two-sided 5 %
//   point the true chance of either end is 5.0 % for r10 and 4.6 to 4.9 %
//   for the other three ratios (simulated: the verify script's A11).
// ============================================================

// The ratio at one end of the sorted sample: drE = 1 the lowest value, 2
// the highest.  0 when the tested value has no gap to its neighbor; the
// range is never shorter than the gap, so nothing is divided by 0.
fc_DxRat(drE)
BEGIN
  LOCAL drG, drW;
  IF drE == 1 THEN
    drG := fcX(1 + fcDxI) - fcX(1);
    drW := fcX(fcNX + 1 - fcDxJ) - fcX(1);
  ELSE
    drG := fcX(fcNX) - fcX(fcNX - fcDxI);
    drW := fcX(fcNX) - fcX(fcDxJ);
  END;
  IF drG <= 0 OR drW <= 0 THEN RETURN 0; END;
  RETURN MIN(1, drG / drW);
END;

// A value of the sample as text, with as few decimals as it needs, up to
// enough for the sample's own scale: a sample that spreads over 0.0000002
// gets 10 decimals, where 4 would print every value as 0.0000.  "Needs"
// is judged against the sample's range, not against the value.
fc_DxFmt(dfV)
BEGIN
  LOCAL dfI, dfT, dfM;
  dfT := fcX(fcNX) - fcX(1);
  dfM := MIN(12, MAX(4, 3 - FLOOR(LOG(dfT))));
  FOR dfI FROM 0 TO dfM DO
    IF ABS(dfV - ROUND(dfV, dfI)) <= 0.0000001 * dfT THEN RETURN fc_Cm(fc_F(dfV, dfI)); END;
  END;
  RETURN fc_Cm(fc_F(dfV, dfM));
END;

// The ratio's name with its two small digits: r10, r11, r21 or r22.
fc_DxNm()
BEGIN
  RETURN "r" + CHAR(8320 + fcDxI) + CHAR(8319 + fcDxJ);
END;

// P(ratio > dtR) at ONE end, in a normal sample of fcNX values, for the
// ratio fcDxI, fcDxJ: the double integral of the heading, 20 x 20 points.
//   a = x(j): centre dtEa = z((j - 3/8)/(n + 1/4)), SD dtSa = root(p (1 - p)
//     / (n + 2)) / f(dtEa), a from dtEa - 7 dtSa to dtEa + 7 dtSa;
//   b = x(n): the mirror image of x(1), centre dtEb, SD dtSb, and b from
//     max(a, dtEb - 7 dtSb) to dtEb + 7 dtSb.
// The scheme gives m = n - j - 1 at least 1 (n = 3, r10), and at least 8
// where G^(m - 1) is used (r21 from n = 11), so no power is 0^0.
fc_DxTail(dtR)
BEGIN
  LOCAL dtM, dtP, dtEa, dtSa, dtEb, dtSb;
  LOCAL dtAl, dtAw, dtBl, dtBh, dtCn, dtIa;
  LOCAL dtIb, dtA, dtB, dtFa, dtLo, dtBw;
  LOCAL dtG, dtC, dtS, dtT, dtK, dtFj;
  IF dtR <= 0 THEN RETURN 1; END;
  IF dtR >= 1 THEN RETURN 0; END;
  dtM := fcNX - fcDxJ - 1;
  dtP := (fcDxJ - 0.375) / (fcNX + 0.25);
  dtEa := NORMALD_ICDF(0, 1, dtP);
  // 0.398942280401 = 1 / root(2 pi)
  dtSa := (dtP * (1 - dtP) / (fcNX + 2))^0.5 / (0.398942280401 * EXP(-dtEa * dtEa / 2));
  dtP := 0.625 / (fcNX + 0.25);
  dtEb := -NORMALD_ICDF(0, 1, dtP);
  dtSb := (dtP * (1 - dtP) / (fcNX + 2))^0.5 / (0.398942280401 * EXP(-dtEb * dtEb / 2));
  dtAl := dtEa - 7 * dtSa; dtAw := 7 * dtSa;      // a = dtAl + dtAw (1 + node)
  dtBl := dtEb - 7 * dtSb; dtBh := dtEb + 7 * dtSb;
  // n! / ((j - 1)! m!) = n (n - 1) ... (m + 1) / (j - 1)!, at most 328,860
  dtCn := 1;
  FOR dtK FROM dtM + 1 TO fcNX DO dtCn := dtCn * dtK; END;
  IF fcDxJ == 3 THEN dtCn := dtCn / 2; END;
  dtT := 0;
  FOR dtIa FROM 1 TO 20 DO
    dtA := dtAl + dtAw * (1 + fcDxGX(dtIa));
    dtFa := fc_Phi(dtA);
    dtLo := MAX(dtA, dtBl);
    IF dtLo < dtBh THEN
      dtBw := (dtBh - dtLo) / 2;
      dtS := 0;
      FOR dtIb FROM 1 TO 20 DO
        dtB := dtLo + dtBw * (1 + fcDxGX(dtIb));
        dtG := MAX(0, fc_Phi(dtB - dtR * (dtB - dtA)) - dtFa);
        dtC := dtG^dtM;
        IF fcDxI == 2 THEN dtC := dtC + dtM * dtG^(dtM - 1) * MAX(0, fc_Phi(dtB) - dtFa - dtG); END;
        dtS := dtS + fcDxGW(dtIb) * EXP(-dtB * dtB / 2) * dtC;
      END;
      // F(a)^(j - 1), written out (never 0^0)
      dtFj := 1;
      IF fcDxJ == 2 THEN dtFj := dtFa; END;
      IF fcDxJ == 3 THEN dtFj := dtFa * dtFa; END;
      dtT := dtT + fcDxGW(dtIa) * dtAw * dtFj * EXP(-dtA * dtA / 2) * dtBw * dtS;
    END;
  END;
  // 0.159154943092 = 1 / (2 pi), the two densities' constants
  RETURN MIN(1, dtCn * 0.159154943092 * dtT);
END;

// Dixon's test for the loaded sample (3 to 30 raw values): which ratio,
// the ratio at each end, the one-end p of the bigger, and where each value
// sits on the dot strip (its pixel, and its level where values share a
// place: the first free level, 5 pixels being a dot's width).
fc_DxCalc()
BEGIN
  LOCAL dcI, dcA, dcT, dcL, dcP, dcLast;
  fcDxI := 1; fcDxJ := 1;
  IF fcNX >= 8 THEN fcDxJ := 2; END;
  IF fcNX >= 11 THEN fcDxI := 2; END;
  IF fcNX >= 14 THEN fcDxJ := 3; END;
  fcDxRL := fc_DxRat(1); fcDxRH := fc_DxRat(2);
  fcDxE := 2;
  IF fcDxRL > fcDxRH THEN fcDxE := 1; END;
  fc_Busy("Dixon's ratio and its p, n = " + fc_Cm(fc_I(fcNX)));
  fcDxP := fc_DxTail(MAX(fcDxRL, fcDxRH));
  // the strip runs from pixel 24 to 296 over the sample's range (the
  // loader refuses a sample with no spread, so the range is above 0)
  dcA := fcX(1); dcT := fcX(fcNX) - fcX(1);
  fcDxPx := MAKELIST(0, dcI, 1, fcNX, 1);
  fcDxLv := MAKELIST(0, dcI, 1, fcNX, 1);
  dcLast := MAKELIST(-99, dcI, 1, fcNX, 1);
  fcDxMx := 0;
  FOR dcI FROM 1 TO fcNX DO
    dcP := 24 + IP((fcX(dcI) - dcA) / dcT * 272 + 0.5);
    dcL := 1;
    WHILE dcP - dcLast(dcL) < 5 DO dcL := dcL + 1; END;
    dcLast(dcL) := dcP;
    fcDxPx(dcI) := dcP; fcDxLv(dcI) := dcL - 1;
    fcDxMx := MAX(fcDxMx, dcL - 1);
  END;
  fcDxOK := 1;
  FC_R := MAX(fcDxRL, fcDxRH); FC_PR := MIN(1, 2 * fcDxP);
END;

// The Outlier page.  A sample in bins, or of more than 30 values, gets
// sentences instead: Dixon's test is for 3 to 30 single values.
//   y 21, 34   the ratio and its either-end p; what the picture shows
//   y 46-64    the range: its length, and a blue bracket
//   y 65-84    the gap: its length, and a red bracket
//   y 86-108   the values as dots (the tested one red), stacked where
//              they share a place; 112 the axis, 116 its numbers
//   y 131-207  six lines: the ratio written out, the p at this end, the
//              other end's ratio, the sentence at alpha = 0.05, which
//              ratio this n takes, a caution
fc_DrawDx()
BEGIN
  LOCAL ddI, ddA, ddT, ddP, ddC, ddS;
  LOCAL ddV, ddDc, ddSt, ddGp, ddRg, ddR;
  LOCAL ddP2, ddLb, ddX, ddK, ddO, ddFl;
  LOCAL ddNx, ddPo, ddPg, ddPr;
  IF fcBin == 1 OR fcNX > 30 THEN
    fc_TL0();
    fc_TL("Dixon's outlier test is for a small sample: 3 to 30 values.", fcBLUE);
    fc_TLb();
    IF fcBin == 1 THEN
      fc_TL("This sample is in bins (" + fc_Cm(fc_I(fcNX)) + " values in " + fc_Cm(fc_I(SIZE(fcBM))) + " bins), so it has no single values to test.", #000000h);
    ELSE
      fc_TL("This sample has " + fc_Cm(fc_I(fcNX)) + " values.", #000000h);
    END;
    fc_TLb();
    fc_TL("With a larger sample, look at the two ends of the Q-Q plot: a value far from the rest is a point far off the line there.", fcGRAY);
    fc_TextPage("Outlier? " + fcNTtl, 1, "");
    RETURN;
  END;
  ddR := MAX(fcDxRL, fcDxRH);
  ddP2 := MIN(1, 2 * fcDxP);
  // flagged when the p AS SHOWN (4 decimals) is below 0.05, so the number
  // and the sentence under it never disagree
  ddFl := 0;
  IF ROUND(ddP2, 4) < 0.05 THEN ddFl := 1; END;
  ddC := fcGRN;
  IF ddFl == 1 THEN ddC := fcRED; END;
  fc_Frame("Outlier? " + fcNTtl);
  TEXTOUT_P("Dixon's " + fc_DxNm() + " = " + fc_Cm(fc_F(ddR, 3)) + ",  " + fc_PStr(ddP2) + " (either end)", G1, 6, 21, 1, ddC, 308);
  TEXTOUT_P("Red dot: the value tested.  Its ratio = gap / range.", G1, 6, 34, 1, fcGRAY, 308);
  // the tested value's rank ddO, where its gap ends (ddGp) and where its
  // range ends (ddRg); their pixels
  IF fcDxE == 1 THEN
    ddO := 1; ddGp := 1 + fcDxI; ddRg := fcNX + 1 - fcDxJ;
  ELSE
    ddO := fcNX; ddGp := fcNX - fcDxI; ddRg := fcDxJ;
  END;
  ddPo := fcDxPx(ddO); ddPg := fcDxPx(ddGp); ddPr := fcDxPx(ddRg);
  // the range, blue: its length, centered over a bracket (kept on the
  // screen: a character is at most about 5 pixels wide)
  ddLb := "range " + fc_DxFmt(ABS(fcX(ddO) - fcX(ddRg)));
  ddX := MAX(6, MIN(312 - 5 * DIM(ddLb), IP((ddPo + ddPr) / 2 - 2.5 * DIM(ddLb))));
  TEXTOUT_P(ddLb, G1, ddX, 46, 1, fcBLUE, 314 - ddX);
  LINE_P(G1, MIN(ddPo, ddPr), 61, MAX(ddPo, ddPr), 61, fcBLUE);
  LINE_P(G1, ddPo, 58, ddPo, 64, fcBLUE);
  LINE_P(G1, ddPr, 58, ddPr, 64, fcBLUE);
  // the gap, red and two pixels thick
  ddLb := "gap " + fc_DxFmt(ABS(fcX(ddO) - fcX(ddGp)));
  ddX := MAX(6, MIN(312 - 5 * DIM(ddLb), IP((ddPo + ddPg) / 2 - 2.5 * DIM(ddLb))));
  TEXTOUT_P(ddLb, G1, ddX, 65, 1, fcRED, 314 - ddX);
  LINE_P(G1, MIN(ddPo, ddPg), 80, MAX(ddPo, ddPg), 80, fcRED);
  LINE_P(G1, MIN(ddPo, ddPg), 81, MAX(ddPo, ddPg), 81, fcRED);
  LINE_P(G1, ddPo, 77, ddPo, 84, fcRED);
  LINE_P(G1, ddPg, 77, ddPg, 84, fcRED);
  // dotted guides down to the three values the ratio is made of
  fc_DotV(ddPo, 86, 100, fcGRAY);
  fc_DotV(ddPg, 86, 100, fcGRAY);
  fc_DotV(ddPr, 86, 100, fcGRAY);
  // the axis and its numbers (a number that would touch the one before it,
  // or the screen's edge, is left out; the steps are counted, Lessons 3)
  LINE_P(G1, 16, 112, 304, 112, #000000h);
  ddA := fcX(1); ddT := fcX(fcNX) - fcX(1);
  ddS := fc_Nice(ddT / 4);
  ddDc := MIN(12, MAX(0, -FLOOR(LOG(ddS))));
  ddV := CEILING(ddA / ddS) * ddS;
  ddNx := -99; ddK := 0;
  WHILE ddV <= fcX(fcNX) AND ddK < 12 DO
    ddP := 24 + IP((ddV - ddA) / ddT * 272 + 0.5);
    LINE_P(G1, ddP, 112, ddP, 115, #000000h);
    ddLb := fc_Cm(STRING(ROUND(ddV, ddDc) + 0, 2, ddDc));
    ddX := ddP - IP(2.5 * DIM(ddLb));
    IF ddX > ddNx + 4 AND ddX >= 2 AND ddX + 5.5 * DIM(ddLb) <= 318 THEN
      TEXTOUT_P(ddLb, G1, ddX, 116, 1, fcGRAY, 318 - ddX);
      ddNx := ddX + 5.5 * DIM(ddLb);
    END;
    ddV := ddV + ddS;
    ddK := ddK + 1;
  END;
  // the values: blue dots, the tested one red and drawn last; values that
  // share a place stack upward (the stack is squeezed to 18 pixels)
  ddSt := 6;
  IF fcDxMx > 3 THEN ddSt := 18 / fcDxMx; END;
  FOR ddI FROM 1 TO fcNX DO
    IF ddI <> ddO THEN fc_Dot(fcDxPx(ddI), 106 - IP(fcDxLv(ddI) * ddSt + 0.5), 2, fcBLUE); END;
  END;
  fc_Dot(ddPo, 106 - IP(fcDxLv(ddO) * ddSt + 0.5), 2, fcRED);
  // line 1: the ratio written out in the sorted values
  IF fcDxE == 1 THEN
    ddLb := "Low end: (x(" + fc_I(ddGp) + ") - x(1)) / (x(" + fc_I(ddRg) + ") - x(1))";
  ELSE
    ddLb := "High end: (x(" + fc_I(ddO) + ") - x(" + fc_I(ddGp) + ")) / (x(" + fc_I(ddO) + ") - x(" + fc_I(ddRg) + "))";
  END;
  TEXTOUT_P(ddLb + " = " + fc_Cm(fc_F(ddR, 3)), G1, 6, 131, 1, #000000h, 308);
  // line 2: the p at this end, and how the either-end p comes from it
  ddLb := "This end alone: " + fc_PStr(fcDxP);
  IF 2 * fcDxP <= 1 THEN
    TEXTOUT_P(ddLb + ".  Either end: twice that, at most.", G1, 6, 144, 1, #000000h, 308);
  ELSE
    TEXTOUT_P(ddLb + ".  Either end: no more than 1.", G1, 6, 144, 1, #000000h, 308);
  END;
  // line 3: the other end's ratio (three cases: smaller as shown, smaller
  // by less than the 3 decimals show, the same)
  ddLb := "High end: ratio "; ddV := fcDxRH;
  IF fcDxE == 2 THEN ddLb := "Low end: ratio "; ddV := fcDxRL; END;
  ddLb := ddLb + fc_Cm(fc_F(ddV, 3));
  CASE
    IF ROUND(ddV, 3) < ROUND(ddR, 3) THEN TEXTOUT_P(ddLb + ", the smaller (not tested).", G1, 6, 157, 1, fcGRAY, 308); END;
    IF ddV < ddR THEN TEXTOUT_P(ddLb + ", a little smaller (not tested).", G1, 6, 157, 1, fcGRAY, 308); END;
    DEFAULT
      TEXTOUT_P(ddLb + ", the same.", G1, 6, 157, 1, fcGRAY, 308);
  END;
  // line 4: the sentence at alpha = 0.05
  ddLb := "x(" + fc_I(ddO) + ") = " + fc_DxFmt(fcX(ddO));
  IF ddFl == 1 THEN
    TEXTOUT_P(ddLb + ": flagged as an outlier at " + fcAl + " = 0.05.", G1, 6, 170, 1, fcRED, 308);
  ELSE
    TEXTOUT_P(ddLb + ": not flagged at " + fcAl + " = 0.05.", G1, 6, 170, 1, fcGRN, 308);
  END;
  // line 5: which ratio this n takes
  ddLb := "3 to 7";
  IF fcNX >= 8 THEN ddLb := "8 to 10"; END;
  IF fcNX >= 11 THEN ddLb := "11 to 13"; END;
  IF fcNX >= 14 THEN ddLb := "14 to 30"; END;
  TEXTOUT_P(fc_DxNm() + ": Dixon's ratio for n from " + ddLb + ".  Normal data assumed.", G1, 6, 183, 1, fcGRAY, 308);
  // line 6: a caution
  IF ddR >= 1 THEN
    TEXTOUT_P("A ratio of 1 here means tied values: p means little.", G1, 6, 196, 1, fcMAG, 308);
  ELSE
    TEXTOUT_P("A flagged value is one to check, not to delete.", G1, 6, 196, 1, fcMAG, 308);
  END;
END;

''')

# ---------------- axis numbers that ran off the screen or were cut (found by this round's layout check) ----------------
# beta 1h: the chi-square curve's and the ECDF's last number could run past the screen's right edge ("200" from x = 306,
# "3,000" from x = 299), and a data value too wide for its 40 pixels was CUT by the width argument on the Q-Q plot's
# y axis and on the ECDF's x axis ("1,234,570" needs 48).  Now: a number is kept on the screen; the ECDF leaves one out
# that would touch the one before; and when any number of an axis is too wide, all of them are written in the Prime's
# scientific form (Lessons Learned 6: StatDist, NormExplorer and SampDist do the same).  Decimals are held to 12.
before('''// The Q-Q points: for raw data (z(i), x(i)); for a binned sample one point
''', '''// beta 1i: a number of an axis as text.  alS = 0: fixed, alD decimals (12
// at most: STRING takes no more), with commas.  alS = 1: the Prime's
// scientific form with one decimal and without a ".0": "1.5E6", "2E6"
// (the E is the calculator's small capital).  Lessons Learned 6: when any
// number of an axis is too wide for its room, all are written one way.
fc_AxLb(alV, alD, alS)
BEGIN
  LOCAL alT, alK;
  IF alS == 0 THEN RETURN fc_Cm(STRING(ROUND(alV, MIN(12, alD)) + 0, 2, MIN(12, alD))); END;
  IF alV == 0 THEN RETURN "0"; END;
  alT := STRING(alV, 3, 1);
  alK := INSTRING(alT, ".0" + CHAR(7431));
  IF alK > 1 THEN alT := LEFT(alT, alK - 1) + MID(alT, alK + 2, DIM(alT)); END;
  RETURN alT;
END;

// 1 when a number of the axis awA .. awB (a tick every awS, awD decimals)
// is wider in fixed form than awR pixels: 6 pixels a character, 3 for a
// point or a comma (the measured widths of font 1).  The ticks are counted
// (a step can stall, Lessons Learned 3).
fc_AxWide(awA, awB, awS, awD, awR)
BEGIN
  LOCAL awV, awT, awI, awW, awK;
  awV := CEILING(awA / awS) * awS; awK := 0;
  WHILE awV <= awB AND awK < 40 DO
    awT := fc_AxLb(awV, awD, 0);
    awW := 6 * DIM(awT);
    FOR awI FROM 1 TO DIM(awT) DO
      IF MID(awT, awI, 1) == "." OR MID(awT, awI, 1) == "," THEN awW := awW - 3; END;
    END;
    IF awW > awR THEN RETURN 1; END;
    awV := awV + awS; awK := awK + 1;
  END;
  RETURN 0;
END;

''')
# the Q-Q page: the z numbers kept on the screen; the value numbers in one form that fits
rep('''  LOCAL qqX1, qqY1, qqX2, qqY2, qqZ, qqB;
  qqN := fcQN;
''', '''  LOCAL qqX1, qqY1, qqX2, qqY2, qqZ, qqB;
  LOCAL qqSc, qqLb;
  qqN := fcQN;
''')
rep('''    TEXTOUT_P(fc_Cm(STRING(ROUND(qqV, qqDc), 2, qqDc)), G1, qqP - 6, 161, 1, fcGRAY, 30);
''', '''    // beta 1i: the last number is kept on the screen
    qqLb := fc_Cm(STRING(ROUND(qqV, qqDc), 2, qqDc));
    TEXTOUT_P(qqLb, G1, MIN(qqP - 6, 319 - 6 * DIM(qqLb)), 161, 1, fcGRAY, 30);
''')
rep('''  qqV := CEILING(qqVa / qqS) * qqS;
  WHILE qqV <= qqVb DO
    qqP := 158 - IP((qqV - qqVa) / (qqVb - qqVa) * 106 + 0.5);
    LINE_P(G1, 44, qqP, 312, qqP, fcGRID);
    TEXTOUT_P(fc_Cm(STRING(ROUND(qqV, qqDc), 2, qqDc)), G1, 2, qqP - 5, 1, fcGRAY, 40);
''', '''  qqV := CEILING(qqVa / qqS) * qqS;
  // beta 1i: a value too wide for the 40 pixels left of the axis was cut;
  // now all the axis's numbers are written in scientific form then
  qqSc := fc_AxWide(qqVa, qqVb, qqS, qqDc, 40);
  WHILE qqV <= qqVb DO
    qqP := 158 - IP((qqV - qqVa) / (qqVb - qqVa) * 106 + 0.5);
    LINE_P(G1, 44, qqP, 312, qqP, fcGRID);
    TEXTOUT_P(fc_AxLb(qqV, qqDc, qqSc), G1, 2, qqP - 5, 1, fcGRAY, 40);
''')
# the ECDF page
rep('''  LOCAL ecDc, ecP, ecF, ecG, ecLast;
''', '''  LOCAL ecDc, ecP, ecF, ecG, ecLast;
  LOCAL ecSc, ecLr, ecLb, ecLx;
''')
rep('''  ecV := CEILING(fcEa / ecS) * ecS;
  WHILE ecV <= fcEb DO
    ecP := 44 + IP((ecV - fcEa) / (fcEb - fcEa) * 268 + 0.5);
    LINE_P(G1, ecP, 52, ecP, 158, fcGRID);
    TEXTOUT_P(fc_Cm(STRING(ROUND(ecV, ecDc), 2, ecDc)), G1, ecP - 8, 161, 1, fcGRAY, 40);
    ecV := ecV + ecS;
  END;
''', '''  ecV := CEILING(fcEa / ecS) * ecS;
  // beta 1i: a number is kept on the screen, is never cut, and is left
  // out when it would touch the one before it; when any is wider than 40
  // pixels all are written in scientific form
  ecSc := fc_AxWide(fcEa, fcEb, ecS, ecDc, 40);
  ecLr := -99;
  WHILE ecV <= fcEb DO
    ecP := 44 + IP((ecV - fcEa) / (fcEb - fcEa) * 268 + 0.5);
    LINE_P(G1, ecP, 52, ecP, 158, fcGRID);
    ecLb := fc_AxLb(ecV, ecDc, ecSc);
    ecLx := MIN(ecP - 8, 319 - 6 * DIM(ecLb));
    IF ecLx > ecLr + 3 THEN
      TEXTOUT_P(ecLb, G1, ecLx, 161, 1, fcGRAY, 320 - ecLx);
      ecLr := ecLx + 6 * DIM(ecLb);
    END;
    ecV := ecV + ecS;
  END;
''')
# the chi-square curve page
rep('''  LOCAL dcLx, dcLast, dcPy, dcDec, dcOff;
  fc_Frame(fcX2S + " curve, df = " ''', '''  LOCAL dcLx, dcLast, dcPy, dcDec, dcOff, dcLb;
  fc_Frame(fcX2S + " curve, df = " ''')
rep('''    TEXTOUT_P(fc_Cm(STRING(ROUND(dcV, dcDec), 2, dcDec)), G1, dcPx - 6, fcPB + 5, 1, fcGRAY, 36);
''', '''    // beta 1i: the last number is kept on the screen
    dcLb := fc_Cm(STRING(ROUND(dcV, dcDec), 2, dcDec));
    TEXTOUT_P(dcLb, G1, MIN(dcPx - 6, 319 - 6 * DIM(dcLb)), fcPB + 5, 1, fcGRAY, 36);
''')

# ---------------- the normality screens: a fourth one, and its soft key ----------------
rep('''// The normality screens: 1 Q-Q, 2 ECDF, 3 Tests; Bins opens the chi-square
// fit on bins; Menu (or Esc, Enter) goes back.
''', '''// The normality screens: 1 Q-Q, 2 ECDF, 3 Tests, 4 (beta 1i) Outlier; Bins
// opens the chi-square fit on bins; Menu (or Esc, Enter) goes back.
''')
rep('''      IF nlScr == 2 THEN fc_DrawECDF(); END;
      DEFAULT
        fc_TextPage("Normality: " + fcNTtl, nlPg,''', '''      IF nlScr == 2 THEN fc_DrawECDF(); END;
      IF nlScr == 4 THEN fc_DrawDx(); END;
      DEFAULT
        fc_TextPage("Normality: " + fcNTtl, nlPg,''')
rep('''    fc_Show({"Q-Q", "ECDF", "Tests", "Bins", "", "Menu"});
''', '''    fc_Show({"Q-Q", "ECDF", "Tests", "Bins", "Outlier", "Menu"});
''')
rep('''        IF nlSl == 4 THEN fc_NorBins(); nlGo := 0; END;
        IF nlSl == 6 THEN nlGo := 0; END;
''', '''        IF nlSl == 4 THEN fc_NorBins(); nlGo := 0; END;
        // beta 1i: Outlier.  Dixon's test is worked out once for a sample
        // (a few seconds on a G1); a sample it is not for gets sentences
        IF nlSl == 5 THEN
          nlScr := 4;
          IF fcBin == 0 AND fcNX <= 30 AND fcDxOK == 0 THEN fc_DxCalc(); END;
        END;
        IF nlSl == 6 THEN nlGo := 0; END;
''')

# ---------------- the preset ----------------
before('''// The 1970 draft lottery: the number drawn for each birth date, by month.
''', '''// beta 1i: Darwin's maize.  The 15 differences in height (inches), crossed
// minus self-fertilized: RankLab's Darwin preset holds the 15 pairs, and
// these are their differences (times 8 they are Fisher's 49, -67, 8, 16, 6,
// 23, 28, 41, 14, 29, 56, 24, 75, 60, -48).  Two are negative and stand far
// below the rest: n = 15 takes r22, which the second low value does not
// mask (the plain gap over range, r10, would be 0.134 and see nothing).
fc_PreDarwin()
BEGIN
  LOCAL pwS;
  pwS := "Darwin (1876); Fisher (1935) The Design of Experiments";
  IF fc_NormSet({6.125, -8.375, 1, 2, 0.75, 2.875, 3.5, 5.125, 1.75, 3.625, 7, 3, 9.375, 7.5, -6}, "Darwin's differences", pwS) == 1 THEN
    fcNPre := 9;
    fc_SrcPage("Darwin's maize: 15 pairs of plants, one crossed and one self-fertilized.  The 15 differences in height, crossed minus self-fertilized, in inches.", pwS,
      "Two differences are negative, far below the rest.  The Outlier key tests the lowest of them (Dixon's ratio).");
  END;
END;

''')
rep('''    "Rossi ages: normality",
    "Draft lottery 1970",
    "Binomial (illustrative)"});
''', '''    "Rossi ages: normality",
    "Darwin's differences: outlier",
    "Draft lottery 1970",
    "Binomial (illustrative)"});
''')
rep('''    IF prsI == 7 THEN fc_PreDraft(); fc_GofLoop(1); END;
    IF prsI == 8 THEN fc_PreBinIll(); fc_GofLoop(1); END;
''', '''    IF prsI == 7 THEN fc_PreDarwin(); IF fcHasN == 1 THEN fc_NorLoop(1); END; END;
    IF prsI == 8 THEN fc_PreDraft(); fc_GofLoop(1); END;
    IF prsI == 9 THEN fc_PreBinIll(); fc_GofLoop(1); END;
''')
rep('''    CHOOSE(mnI, "Normality", {"The last sample again", "Preset: Rossi ages", "Preset: crimtab heights", "My values in D1"});
  ELSE
    CHOOSE(mnI, "Normality", {"Preset: Rossi ages", "Preset: crimtab heights", "My values in D1"});
''', '''    CHOOSE(mnI, "Normality", {"The last sample again", "Preset: Rossi ages", "Preset: crimtab heights", "Preset: Darwin's differences", "My values in D1"});
  ELSE
    CHOOSE(mnI, "Normality", {"Preset: Rossi ages", "Preset: crimtab heights", "Preset: Darwin's differences", "My values in D1"});
''')
rep('''    IF mnI == 3 THEN fc_PreCrim(); fc_NorLoop(1); END;
    IF mnI == 4 THEN fc_MyD(1); END;
''', '''    IF mnI == 3 THEN fc_PreCrim(); fc_NorLoop(1); END;
    IF mnI == 4 THEN fc_PreDarwin(); IF fcHasN == 1 THEN fc_NorLoop(1); END; END;
    IF mnI == 5 THEN fc_MyD(1); END;
''')

# ---------------- help ----------------
rep('''fc_Help()
BEGIN
  fc_TL0();
''', '''fc_Help()
BEGIN
  LOCAL hpA, hpB, hpC, hpD;
  // beta 1i: the four ratio names, each with its two small digits
  hpA := "r" + CHAR(8321) + CHAR(8320); hpB := "r" + CHAR(8321) + CHAR(8321);
  hpC := "r" + CHAR(8322) + CHAR(8321); hpD := "r" + CHAR(8322) + CHAR(8322);
  fc_TL0();
''')
rep('''  And the exact binomial test for one proportion.", #000000h);
''', '''  And the exact binomial test for one proportion, and Dixon's test for one outlier in a small sample.", #000000h);
''')
rep('''  fc_TLsec("Keys, presets, Home");
  fc_TL("KEYS.  Soft keys move between the pages of a result (Bars, Table, Curve, Test; Q-Q, ECDF, Tests, Bins; Plot, Why, " + fcX2S + ").  Tap a bar, a row or a point to read it; " + fcLR + " move " +
      "the choice; " + fcUD + " turn text pages.  Esc or Enter = menu.", #000000h);
  fc_TL("Presets: the data and their sources are in the program's header.  Your own data: 'Use my data', and its last item says how to fill D1 and D2.", #000000h);
  fc_TLb();
  fc_TL("HOME, after a run: FC_X2, FC_DF, FC_P, FC_O, FC_E (the last " + fcX2S + " fit, as shown), FC_W, FC_PW, FC_A2, FC_PA, FC_D, FC_PD (-1 = p > 0.10, -2 = n < 5), FC_BP (the exact test's two-sided p).", fcGRAY);
''', '''  // beta 1i: three pages on Dixon's outlier test
  fc_TLsec("Outliers: Dixon's test");
  fc_TL("DIXON'S OUTLIER TEST (the Outlier key; 3 to 30 values).  Is the lowest or the highest value too far from the rest to come from the same normal population?  Sort the values: x(1) is the lowest, " +
      "x(n) the highest.  The ratio is a gap over a range: how far the value stands from its neighbor, as a share of the spread.  0 = no gap; 1 = it stands alone.", fcBLUE);
  fc_TL("The page draws every value as a dot, the tested one in red, with its gap (red) and its range (blue) above the dots.  It tests the end with the bigger ratio.", #000000h);
  fc_TLsec("Outliers: which ratio");
  fc_TL("The ratio changes with n (Dixon 1953).  First digit: the gap ends at the nearest value (1) or the second-nearest (2).  Second digit: how many values the range leaves off its far end.", fcBLUE);
  fc_TL("3 to 7 values: " + hpA + ".  The gap to the nearest value, over the whole range.", #000000h);
  fc_TL("8 to 10: " + hpB + ".  The range leaves off 1 value.", #000000h);
  fc_TL("11 to 13: " + hpC + ".  The gap to the second-nearest value; the range leaves off 1.", #000000h);
  fc_TL("14 to 30: " + hpD + ".  The range leaves off 2 values.", #000000h);
  fc_TL("Why: a second outlier, beside the first or at the far end, would hide the first.  The later ratios guard against that.", fcMAG);
  fc_TLsec("Outliers: the p and its limits");
  fc_TL("THE P is the chance, in a normal sample of this size, of a ratio this big or bigger at that end.  FitCheck computes it; a printed table of critical values can differ from it in the third " +
      "decimal (McBane 2006).", fcBLUE);
  fc_TL("The test takes the end with the bigger ratio, so the p it reports is for either end: twice the one-end p, as in the printed tables.  That is an upper limit.", #000000h);
  fc_TL("A small p is a reason to check the value: was it misread, mistyped, or from another population?  It is no license to delete it.", fcMAG);
  fc_TL("The p assumes normal data (see the Q-Q plot).  Values tied by rounding can make the ratio 1.", fcRED);
  fc_TLsec("Keys and presets");
  fc_TL("KEYS.  Soft keys move between the pages of a result (Bars, Table, Curve, Test; Q-Q, ECDF, Tests, Bins, Outlier; Plot, Why, " + fcX2S + ").  Tap a bar, a row or a point to read it; " + fcLR + " move " +
      "the choice; " + fcUD + " turn text pages.  Esc or Enter = menu.", #000000h);
  fc_TL("Presets: the data and their sources are in the program's header.  Your own data: 'Use my data', and its last item says how to fill D1 and D2.", #000000h);
  // beta 1i: the Home variables on a page of their own, a name or two to a line
  fc_TLsec("Home variables");
  fc_TL("HOME, after a run, holds the last results under these names.", #000000h);
  fc_TL("FC_X2, FC_DF, FC_P: the last " + fcX2S + " fit.  FC_O, FC_E: its observed and expected counts, as shown.", fcGRAY);
  fc_TL("FC_W, FC_PW: Shapiro-Wilk's W and its p.", fcGRAY);
  fc_TL("FC_A2, FC_PA: Anderson-Darling's A" + fcSq + " (uncorrected) and its p.", fcGRAY);
  fc_TL("FC_D, FC_PD: Lilliefors' D and its p (-1 = p > 0.10, -2 = n < 5).", fcGRAY);
  fc_TL("FC_BP: the exact binomial test's two-sided p.", fcGRAY);
  fc_TL("FC_R, FC_PR: Dixon's ratio and its either-end p.", fcGRAY);
''')

# ---------------- two source lines of 336 and 311 characters, split (the header's own rule is 250; the text is unchanged) ----------------
rep('''" on bins: df = k - 3.  Tests page: skewness g" + CHAR(8321) + ''', '''" on bins: df = k - 3.  " +
          "Tests page: skewness g" + CHAR(8321) + ''')
rep('''CVMTEST1, NMLPROB, BENFORD and others).  It was written new for the Prime, ''', '''CVMTEST1, NMLPROB, BENFORD and others).  " +
      "It was written new for the Prime, ''')

# ---------------- the title page ----------------
rep('  fc_Frame("FitCheck - beta 1h");\n', '  fc_Frame("FitCheck - beta 1i");\n')
rep('''  TEXTOUT_P(fcX2S + " goodness of fit, Benford's law, Poisson and", G1, 12, 72, 1, #000000h, 300);
  TEXTOUT_P("binomial fits;  normal Q-Q, Shapiro-Wilk W,", G1, 12, 85, 1, #000000h, 300);
  TEXTOUT_P("Anderson-Darling A" + fcSq + ", Lilliefors D;  the exact", G1, 12, 98, 1, #000000h, 300);
  TEXTOUT_P("binomial test (Castaneda v. Partida).", G1, 12, 111, 1, #000000h, 300);
  TEXTOUT_P("(C) 2026 Roger D. Metcalf.  Written with AI", G1, 12, 132, 1, fcGRAY, 300);
  TEXTOUT_P("assistance (Claude, Anthropic).", G1, 12, 145, 1, fcGRAY, 300);
''', '''  // beta 1i: five lines (Dixon's test is named), so they start 2 pixels
  // higher and the two lines under them sit 4 and 3 pixels lower
  TEXTOUT_P(fcX2S + " goodness of fit, Benford's law, Poisson and", G1, 12, 70, 1, #000000h, 300);
  TEXTOUT_P("binomial fits;  normal Q-Q, Shapiro-Wilk W,", G1, 12, 83, 1, #000000h, 300);
  TEXTOUT_P("Anderson-Darling A" + fcSq + ", Lilliefors D;  Dixon's", G1, 12, 96, 1, #000000h, 300);
  TEXTOUT_P("outlier test;  the exact binomial test", G1, 12, 109, 1, #000000h, 300);
  TEXTOUT_P("(Castaneda v. Partida).", G1, 12, 122, 1, #000000h, 300);
  TEXTOUT_P("(C) 2026 Roger D. Metcalf.  Written with AI", G1, 12, 136, 1, fcGRAY, 300);
  TEXTOUT_P("assistance (Claude, Anthropic).", G1, 12, 148, 1, fcGRAY, 300);
''')

# ---------------- the closing line ----------------
rep('''  IF fcHasT == 1 THEN mnS := mnS + " binomial " + fc_PStr(fcTp2) + ";"; END;
''', '''  // beta 1i: Dixon's test, when its page was opened for the loaded sample
  IF fcHasN == 1 AND fcBin == 0 AND fcDxOK == 1 THEN
    mnS := mnS + " Dixon r" + fc_I(fcDxI) + fc_I(fcDxJ - 1) + " = " + fc_Cm(fc_F(MAX(fcDxRL, fcDxRH), 3)) + ", " + fc_PStr(MIN(1, 2 * fcDxP)) + " (either end);";
  END;
  IF fcHasT == 1 THEN mnS := mnS + " binomial " + fc_PStr(fcTp2) + ";"; END;
''')

# ---------------- numbers that come from the arithmetic, not from memory ----------------
rep('@GX@', GX); rep('@GW@', GWT)
rep('@ERRL@', '''At every n from 3 to 30 the
//   relative error is under 0.05 % for a p above 0.001, and under 0.2 %
//   for a p above 0.0001 (verify_FitCheck_beta1i.py: against a 360 x 600-
//   point reference, the closed form at n = 3, 1,000,000 simulated
//   samples a case, and McBane's 2006 printed values).''')

# ---------------- the file map: counted here ----------------
def line_of(text, nth=1):
    k = -1
    for _ in range(nth):
        k = s.index(text, k + 1)
    return s.count('\n', 0, k) + 1
BAR = '// ============================================================\n'
def sec(title): return line_of(BAR + title)
starts = [('M1', line_of('EXPORT FC_X2, FC_DF, FC_P, FC_O;')), ('M2', sec('// SMALL HELPERS')), ('M3', sec('// SPECIAL FUNCTIONS')),
          ('M4', sec('// THE CHI-SQUARE FIT ENGINE')), ('M5', sec('// THE FITS: Benford')), ('M6', sec('// NORMALITY: Blom scores')),
          ('M7', sec('// THE EXACT BINOMIAL TEST, in logs')), ('M8', sec("// beta 1a (review 2): FISHER'S EXACT TEST")),
          ('M9', sec('// PICTURES AND PAGES OF A CHI-SQUARE FIT')), ('M10', sec("// beta 1i: DIXON'S OUTLIER TEST")),
          ('M11', sec('// PICTURES AND PAGES OF THE NORMALITY TESTS')), ('M12', sec('// PICTURES AND PAGES OF THE EXACT BINOMIAL TEST')),
          ('M13', sec('// PRESETS (only data/DATASETS.md')), ('M14', sec('// YOUR OWN DATA: D1 and D2')), ('M15', sec('// HELP AND THE TITLE PAGE')),
          ('M16', sec('// THE MENU ITEMS')), ('M17', sec('// FitCheck(): the menu'))]
if [b for (_, b) in starts] != sorted(b for (_, b) in starts): sys.exit('BUILD STOPPED: the sections are not in the order the file map lists them')
for k, (tag, a) in enumerate(starts):
    b = (starts[k + 1][1] - 2) if k + 1 < len(starts) else None
    rep('@%s@' % tag, '%d-%s' % (a, 'end' if b is None else b))
if re.search(r'@[A-Z0-9]+@', s): sys.exit('BUILD STOPPED: a placeholder is left: %r' % re.findall(r'@[A-Z0-9]+@', s)[:5])

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'FitCheck_beta1i.txt'), 'w', encoding='utf-8', newline='').write(s)
print('FitCheck_beta1i.txt written:', len(s.split('\n')) - 1, 'lines')
