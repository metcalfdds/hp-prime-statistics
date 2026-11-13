#!/usr/bin/env python3
"""make_chitable_3m.py OUTDIR -- ChiTable beta 3m (13 Nov 2026) from beta 3l, by exact replacements (each must match once).
Roger, 13 Nov 2026: "Could we do an exact test for a bigger table?"  Beta 3m adds the exact test for the 2 x 3 and 3 x 2
tables (Freeman and Halton 1951: Fisher's rule with more columns), shows it on results page 5 when an expected count is below 5,
and points help page 1 to the exact tests.  Reads beta 3l from git (BASE), writes OUTDIR/ChiTable_beta3m.txt."""
import os, sys, subprocess
BASE = '0a422c4'
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
OLD = subprocess.run(['git', 'show', BASE + ':programs/ChiTable_beta3l.txt'], cwd=REPO, capture_output=True, check=True).stdout.decode('utf-8')

ROUTINE = r'''// ------------------------------------------------------------
// BETA 3M: THE EXACT TEST FOR A 2 x 3 OR 3 x 2 TABLE
// (Freeman and Halton 1951: Fisher's exact test with more columns)
//
// Fisher's idea, unchanged: keep every row total and every column
// total fixed, list every table that has those totals, and add up
// the chances of the tables that are NO MORE PROBABLE than the one
// observed.  That sum is the two-sided p.  R's fisher.test
// computes the same p.
//
// How the tables are listed.  A 3 x 2 table is first turned on its
// side (rows become columns); the p does not change.  In a 2 x 3
// table the first row (a, b, c) decides everything, because the
// second row is the column totals minus the first.  With the row
// total r1 fixed, c = r1 - a - b, so a and b alone run through the
// tables.
//
// The chance of one table is C(c1, a) C(c2, b) C(c3, c) / C(N, r1)
// (how many ways each column's count can be chosen).  The program
// never computes a factorial of a big number: it keeps the LOG of
// each binomial coefficient, built from its neighbor by one ratio,
// C(m, k+1) = C(m, k) (m - k) / (k + 1), so nothing can overflow.
// The chances are then added relative to the table of expected
// counts (the most probable table, or close to it), so the biggest
// term is about 1.
//
// Ties.  A table exactly as probable as the observed one counts, as
// in csFisher; "exactly" allows a hair of rounding (1E-7 in the log,
// the tolerance R uses).
//
// Returns the p, or -1 when there are more than 10,000 tables: too
// many to add up quickly on the calculator, and then the page says
// to merge cells.  A table that small samples make shaky has far
// fewer (a 2 x 3 table with 100 cases has about 900).
// ------------------------------------------------------------
csFishRC()
BEGIN
  LOCAL frX1, frX2, frX3, frY1, frY2, frY3;
  LOCAL frR1, frC1, frC2, frC3, frN, frI;
  LOCAL frAL, frAH, frBm, frBM, frCm, frCM;
  LOCAL frA, frB, frBL, frBH, frCnt, frL;
  LOCAL frL1, frL2, frL3, frLo, frLr, frW;
  LOCAL frTot, frSum, frRa, frRb;
  // the table as 2 x 3, first row (frX1 frX2 frX3), second (frY1 frY2 frY3)
  IF csNR == 2 THEN
    frX1 := csO(1); frX2 := csO(2); frX3 := csO(3);
    frY1 := csO(4); frY2 := csO(5); frY3 := csO(6);
  ELSE
    // 3 x 2: column 1 becomes the first row, column 2 the second
    frX1 := csO(1); frX2 := csO(3); frX3 := csO(5);
    frY1 := csO(2); frY2 := csO(4); frY3 := csO(6);
  END;
  frR1 := frX1 + frX2 + frX3;
  frC1 := frX1 + frY1; frC2 := frX2 + frY2; frC3 := frX3 + frY3;
  frN := frC1 + frC2 + frC3;
  // a runs from frAL to frAH; for each a, b runs from frBL to frBH
  // (every count in both rows at least 0)
  frAL := MAX(0, frR1 - frC2 - frC3); frAH := MIN(frC1, frR1);
  // count the tables first, and stop at 10,000
  frCnt := 0;
  FOR frA FROM frAL TO frAH DO
    frBL := MAX(0, frR1 - frA - frC3); frBH := MIN(frC2, frR1 - frA);
    frCnt := frCnt + frBH - frBL + 1;
    IF frCnt > 10000 THEN RETURN -1; END;
  END;
  // the logs of C(c1, a), C(c2, b) and C(c3, c), each up to a constant
  // that cancels: index 1 is the smallest a (b, c) that can occur
  frL1 := MAKELIST(0, frI, 1, frAH - frAL + 1);
  FOR frI FROM frAL TO frAH - 1 DO
    frL1(frI - frAL + 2) := frL1(frI - frAL + 1) + LN((frC1 - frI) / (frI + 1));
  END;
  frBm := MAX(0, frR1 - frAH - frC3); frBM := MIN(frC2, frR1 - frAL);
  frL2 := MAKELIST(0, frI, 1, frBM - frBm + 1);
  FOR frI FROM frBm TO frBM - 1 DO
    frL2(frI - frBm + 2) := frL2(frI - frBm + 1) + LN((frC2 - frI) / (frI + 1));
  END;
  frCm := MAX(0, frR1 - frAH - frC2); frCM := MIN(frC3, frR1 - frAL);
  frL3 := MAKELIST(0, frI, 1, frCM - frCm + 1);
  FOR frI FROM frCm TO frCM - 1 DO
    frL3(frI - frCm + 2) := frL3(frI - frCm + 1) + LN((frC3 - frI) / (frI + 1));
  END;
  // the observed table's log chance, and the table of expected counts
  // (rounded, kept inside the ranges) as the reference
  frLo := frL1(frX1 - frAL + 1) + frL2(frX2 - frBm + 1) + frL3(frX3 - frCm + 1);
  frRa := MIN(MAX(ROUND(frR1 * frC1 / frN, 0), frAL), frAH);
  frBL := MAX(0, frR1 - frRa - frC3); frBH := MIN(frC2, frR1 - frRa);
  frRb := MIN(MAX(ROUND(frR1 * frC2 / frN, 0), frBL), frBH);
  frLr := frL1(frRa - frAL + 1) + frL2(frRb - frBm + 1) + frL3(frR1 - frRa - frRb - frCm + 1);
  // one pass over every table: all of them for the total, and the ones
  // no more probable than the observed table for the p
  frTot := 0; frSum := 0;
  FOR frA FROM frAL TO frAH DO
    frBL := MAX(0, frR1 - frA - frC3); frBH := MIN(frC2, frR1 - frA);
    FOR frB FROM frBL TO frBH DO
      frL := frL1(frA - frAL + 1) + frL2(frB - frBm + 1) + frL3(frR1 - frA - frB - frCm + 1);
      frW := EXP(frL - frLr);
      frTot := frTot + frW;
      IF frL <= frLo + 0.0000001 THEN frSum := frSum + frW; END;
    END;
  END;
  RETURN MIN(1, frSum / frTot);
END;

// beta 3m: the exact test's p for the table on screen, worked out once
// per table (csXKeyOf, the key the CAS cache uses) and kept in csRCP.
csRCEnsure()
BEGIN
  LOCAL reK;
  reK := csXKeyOf();
  IF reK <> csRCKey THEN
    csRCKey := reK;
    csRCP := csFishRC();
  END;
END;

csPageInterp()
BEGIN'''

EDITS = [
 ('// CHITABLE - beta 3l\n', '// CHITABLE - beta 3m\n'),
 ('// beta 3l (9 Nov 2026): Round 11:',
  '// beta 3m (13 Nov 2026): the exact test for the 2 x 3 and 3 x 2 tables (Roger, 13 Nov 2026: "Could we do an exact test for\n'
  '//   a bigger table?").  csFishRC adds the chance of every table with the same row and column totals that is no more\n'
  '//   probable than the one observed (Freeman and Halton 1951: Fisher\'s rule with more columns; R\'s fisher.test gives\n'
  '//   the same p).  Results page 5 shows it when an expected count is below 5; with more than 10,000 such tables the\n'
  '//   page says to merge cells instead.  Page 5\'s line for a 2 x 2 table now sends the student to Fisher\'s test on\n'
  '//   page 6, and help page 1 names both exact tests.  And page 5 calls a count equal to its expected count at the two\n'
  '//   decimals shown (a table with no association at all) "just as expected", not "MORE than expected" (found on the\n'
  '//   Virtual Calculator, 13 Nov 2026).\n'
  '// beta 3l (9 Nov 2026): Round 11:'),
 ('LOCAL csXX2, csXAd, csXPr, csXS, csXT, csXDg;\n',
  'LOCAL csXX2, csXAd, csXPr, csXS, csXT, csXDg;\n'
  '// beta 3m: the exact test of a 2 x 3 or 3 x 2 table (csFishRC), and the table it belongs to\n'
  'LOCAL csRCKey, csRCP;\n'),
 ('csPageInterp()\nBEGIN', ROUTINE),
 ('    TEXTOUT_P(csCm((CHAR(967) + CHAR(178) + " is shaky; Fisher (2x2) or merge cells.")), G1, 12, 181, 1, csRED, 296);\n',
  '    // beta 3m: an exact test for every shape ChiTable takes\n'
  '    IF csNR == 2 AND csNC == 2 THEN\n'
  '      TEXTOUT_P(csCm((CHAR(967) + CHAR(178) + " is shaky; see Fisher\'s exact test, page 6.")), G1, 12, 181, 1, csRED, 296);\n'
  '    ELSE\n'
  '      csRCEnsure();\n'
  '      IF csRCP >= 0 THEN\n'
  '        TEXTOUT_P(csCm((CHAR(967) + CHAR(178) + " is shaky; exact test (Freeman-Halton): " + csPStr(csRCP))), G1, 12, 181, 1, csRED, 296);\n'
  '      ELSE\n'
  '        TEXTOUT_P(csCm((CHAR(967) + CHAR(178) + " is shaky; too many tables to count: merge cells.")), G1, 12, 181, 1, csRED, 296);\n'
  '      END;\n'
  '    END;\n'),
 ('  TEXTOUT_P("any E below 5).  If not: use Fisher\'s exact (2x2) or merge sparse", G1, 12, 159, 1, csRED, 296);\n'
  '  TEXTOUT_P("categories.", G1, 12, 172, 1, csRED, 296);\n',
  '  TEXTOUT_P("any E below 5).  If not, use the exact test (page 6 for a 2x2,", G1, 12, 159, 1, csRED, 296);\n'
  '  TEXTOUT_P("page 5 for 2x3 and 3x2) or merge sparse categories.", G1, 12, 172, 1, csRED, 296);\n'),
 ('  csCasOK := 0; csXKey := ""; csXFSt := 0; csXCSt := 0;',
  '  csCasOK := 0; csXKey := ""; csXFSt := 0; csXCSt := 0;\n  csRCKey := ""; csRCP := -2;'),
 ('  IF csO(csBig) >= csE(csBig) THEN\n    piS := "O = " + csCm(STRING(csO(csBig), 2, 0)) + ", E = " + csCm(STRING(ROUND(csE(csBig), 2), 2, 2)) + ": MORE than expected";\n  ELSE\n    piS := "O = " + csCm(STRING(csO(csBig), 2, 0)) + ", E = " + csCm(STRING(ROUND(csE(csBig), 2), 2, 2)) + ": FEWER than expected";\n  END;\n',
  '  // beta 3m: a count equal to its expected count, at the two decimals\n  // shown (a table with no association at all), was "MORE than\n  // expected"; it is "just as expected" now\n  IF csO(csBig) == ROUND(csE(csBig), 2) THEN\n    piS := "O = " + csCm(STRING(csO(csBig), 2, 0)) + ", E = " + csCm(STRING(ROUND(csE(csBig), 2), 2, 2)) + ": just as expected";\n  ELSE\n    IF csO(csBig) >= csE(csBig) THEN\n      piS := "O = " + csCm(STRING(csO(csBig), 2, 0)) + ", E = " + csCm(STRING(ROUND(csE(csBig), 2), 2, 2)) + ": MORE than expected";\n    ELSE\n      piS := "O = " + csCm(STRING(csO(csBig), 2, 0)) + ", E = " + csCm(STRING(ROUND(csE(csBig), 2), 2, 2)) + ": FEWER than expected";\n    END;\n  END;\n'),
]
def build():
    t = OLD
    for a, b in EDITS:
        assert t.count(a) == 1, ('not exactly once', t.count(a), a[:70])
        t = t.replace(a, b)
    return t
if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'programs')
    os.makedirs(out, exist_ok=True)
    t = build()
    open(os.path.join(out, 'ChiTable_beta3m.txt'), 'w', encoding='utf-8', newline='').write(t)
    print('ChiTable_beta3m.txt', len(t.split('\n')), 'lines')
