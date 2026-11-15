# -*- coding: utf-8 -*-
"""Round 14, part 2 (14 Nov 2026): TTestLab beta 1k from beta 1j, by exact replacements (a miss stops the build).

New in beta 1k (Roger, 14 Nov 2026: "go ahead and do the program work"; the book's Chapters 9 and 11):
  * three more tests in the same five steps: the one-sample t-test (ttTY 4: a sample's mean against mu0, from the
    mean, SD and N or from scores in D1), the one-proportion z-test (5) and the two-proportion z-test (6), from counts;
  * a z-test uses the standard normal curve: step 2 says so and checks that every count is at least 5 (the book's
    rule), step 3 gives z critical, and the curve of steps 3 and 5 is the normal curve;
  * "Choose the test" opens a short menu first (two means go on to the flowchart);
  * three more examples, all in the book: Student's sleep data (Chapter 9: t(9) = 4.06), the grand juries of
    Castaneda v. Partida (Chapters 5 and 12: z = -29.1) and the Rossi experiment (Chapter 11: z = -1.965);
  * help page 3 of 3.
The three older tests are untouched: their pages, forms and numbers are beta 1j's (the verify script compares them).
Run from the repository's root:   python3 verify/round14/make_ttestlab_1k.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap
BASE = '1001032'; DATE = '14 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r14_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/TTestLab_beta1j.txt'], check=True, capture_output=True).stdout.decode('utf-8')

def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)

def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)

# ---------------------------------------------------------------- header, history
rep('// TTESTLAB - beta 1j', '// TTESTLAB - beta 1k')
note = ('Round 14 (Roger, 14 Nov 2026: "go ahead and do the program work").  Three more tests, in the same five '
        'steps: the one-sample t-test (a sample\'s mean against mu0; from the mean, SD and N, or from scores in D1), '
        'the one-proportion z-test and the two-proportion z-test (from counts).  A z-test uses the standard normal '
        'curve: step 2 says so and checks that every count is at least 5, step 3 gives z critical, and the curve of '
        'steps 3 and 5 is the normal curve (tt_Dens).  "Choose the test" opens a short menu first, and two means go '
        'on to the flowchart (tt_Pick).  Three more examples, all from the book: Student\'s sleep data (one-sample '
        't(9) = 4.06), the grand juries of Castaneda v. Partida (one proportion, z = -29.1) and the Rossi experiment '
        '(two proportions, z = -1.965).  Help page 3 of 3.  The three older tests are as they were: their pages, '
        'forms and numbers are beta 1j\'s, but for one line of step 5: a Cohen\'s d past 999.99 in size prints as "> 999.99" '
        '(tt_DS), so that it cannot run into the label beside it.  New routines: tt_SL, tt_Dens, tt_ZCrit, tt_ZP, tt_HS, tt_DS, tt_One, tt_Whole, '
        'tt_CalcN, tt_VN, tt_Par, tt_Step1N, tt_Step2N, tt_Step3Z, tt_Step4N, tt_Step5N, tt_Fam, tt_Pick, '
        'tt_AskDataN.  Gate and PC harness when written; its CHANGES file says what ran on the Virtual Calculator.')
before('// beta 1j (13 Nov 2026):', '// beta 1k (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')

after('''//   * Dependent samples (matched pairs, before and after) from the
//     pairs in D1 and D2, or from the mean and SD of the differences.
''', '''//   * (beta 1k) One sample and proportions, in the same five steps: the
//     one-sample t-test (a sample's mean against mu0, the value H0
//     claims; from the mean, SD and N, or from scores in D1), the
//     one-proportion z-test and the two-proportion z-test (from counts).
//     The z-tests use the normal curve; step 2 checks that every count
//     is at least 5, the book's rule for the normal approximation.
''')
after('''//     separate variances: t = -4.351 on 265.924 df, as SPSS).
''', '''//     Three more since beta 1k, each worked in the book: Student's sleep
//     data (Cushny and Peebles 1905; Student 1908: one-sample t(9) =
//     4.06), the grand juries of Castaneda v. Partida, 430 U.S. 482
//     (1977) (339 of 870 against p0 = 0.791: z = -29.1) and the Rossi
//     experiment (Rossi, Berk and Lenihan 1980: re-arrested, 48 of 216
//     with aid against 66 of 216 without: z = -1.965).
''')
after('''//   Cohen's d: (mean1 - mean2)/sp (independent; SPSS's Cohen's d);
//      mean(xD)/sD (dependent; SPSS's paired Cohen's d).
''', '''//   one sample (beta 1k): SE = s/sqrt(N), t obtained = (mean - mu0)/SE,
//      df = N - 1; Cohen's d = (mean - mu0)/s
//   one proportion: p-hat = x/n, SE = sqrt(p0(1 - p0)/n) (from p0, not
//      p-hat: the test assumes H0), z obtained = (p-hat - p0)/SE
//   two proportions: pooled p = (x1 + x2)/(n1 + n2),
//      SE = sqrt(p(1 - p)(1/n1 + 1/n2)), z obtained = (p-hat1 - p-hat2)/SE
//   z critical = -NORMALD_ICDF(0, 1, alpha) one-tailed, alpha/2 two-
//      tailed; p from NORMALD_CDF(0, 1, .), lower tails only, as for t
''')

# ---------------------------------------------------------------- shared state
after('''LOCAL ttTY:=1;           // the test: 1 pooled, 2 separate, 3 dependent
''', '''//   (beta 1k) 4 one-sample t, 5 one-proportion z, 6 two-proportion z
''')
rep('// the example on screen: 0 none, 1-3 the examples', '// the example on screen: 0 none, 1-6 the examples')
after('''LOCAL ttX1:={0}, ttX2:={0}, ttXD:={0};
''', '''// one sample (beta 1k): its mean, SD and N, the mean H0 claims (mu0), and
// the scores themselves when they came from D1
LOCAL ttMO:=0, ttSO:=1, ttNO:=10, ttMU:=0, ttXO:={0};
// proportions (beta 1k): the successes and the size of sample 1 and of
// sample 2 (a one-proportion test uses sample 1 only), and p0, the
// proportion H0 claims; then the sample proportions and the pooled one
LOCAL ttKA:=5, ttNA:=10, ttKB:=5, ttNB:=10, ttP0:=0.5;
LOCAL ttPA:=0.5, ttPB:=0.5, ttPP:=0.5;
''')

# ---------------------------------------------------------------- z-tests: the curve, z critical, p, the symbols
after(''' IF ttTL < 0 THEN RETURN STUDENT_CDF(pdf,pt); END;
 RETURN STUDENT_CDF(pdf,-pt);
END;

''', r'''// ---------------- z-tests and the tests' symbols (beta 1k) ----------------
// TTestLab's first three tests are t-tests for two means.  Since beta 1k
// it also works a one-sample t-test (ttTY = 4) and two z-tests for
// proportions (5: one proportion, 6: two).  A z-test uses the standard
// normal curve, which has no df.

// The statistic's letter for the test on screen: "z" for a proportion
// test, "t" for the rest
LOCAL tt_SL()
BEGIN
 IF ttTY >= 5 THEN RETURN "z"; END;
 RETURN "t";
END;

// The height at dvx of the curve the test uses: the standard normal
// curve for a z-test, Student's t on ttDF for a t-test
LOCAL tt_Dens(dvx)
BEGIN
 IF ttTY >= 5 THEN RETURN NORMALD(0,1,dvx); END;
 RETURN STUDENT(ttDF,dvx);
END;

// z critical (its size) at alpha for the tails on screen: the point of
// the standard normal curve with a = alpha (one-tailed) or alpha/2
// (two-tailed) beyond it.  A lower-tail quantile, mirrored, as tt_Crit's
// (Lessons Learned s3: never ICDF(1 - a)).
LOCAL tt_ZCrit()
BEGIN
 RETURN -NORMALD_ICDF(0,1,IFTE(ttTL == 0,ttAL/2,ttAL));
END;

// The p value for a z, for the tails on screen (lower tails only; the
// two-tailed p is capped at 1, as tt_PVal's)
LOCAL tt_ZP(zpv)
BEGIN
 IF ttTL == 0 THEN RETURN MIN(1,2*NORMALD_CDF(0,1,-ABS(zpv))); END;
 IF ttTL < 0 THEN RETURN NORMALD_CDF(0,1,zpv); END;
 RETURN NORMALD_CDF(0,1,-zpv);
END;

// The two sides of the hypotheses in symbols, for the test on screen:
// mu1 and mu2 (two means), mu and mu0 (one mean), p and p0 (one
// proportion), p1 and p2 (two proportions)
LOCAL tt_HS()
BEGIN
 IF ttTY == 4 THEN RETURN {"μ","μ"+CHAR(8320)}; END;
 IF ttTY == 5 THEN RETURN {"p","p"+CHAR(8320)}; END;
 IF ttTY == 6 THEN RETURN {"p"+CHAR(8321),"p"+CHAR(8322)}; END;
 RETURN {"μ"+CHAR(8321),"μ"+CHAR(8322)};
END;

// Cohen's d as the pages print it after "Cohen's d": " = 1.28", or, past
// 999.99 in size, " > 999.99" or " < -999.99".  A d that large comes from
// an SD typed far too small, and its digits would run into the label
// beside it (the label monkey, 14 Nov 2026: "Cohen's d = -34,200,918,..."
// over "magenta area = p", on the older tests' step 5 as well).
LOCAL tt_DS()
BEGIN
 IF ttD >= 1000 THEN RETURN " > 999.99"; END;
 IF ttD <= -1000 THEN RETURN " < "+CHAR(8722)+"999.99"; END;
 RETURN " = "+tt_Cm(tt_Fmt(ttD,2));
END;

''')
# the older tests' step 5 prints d through it
rep(""" TEXTOUT_P("Cohen's d = "+tt_Cm(tt_Fmt(ttD,2))+tt_Cm(IFTE(ttTY == 3,""", """ TEXTOUT_P("Cohen's d"+tt_DS()+tt_Cm(IFTE(ttTY == 3,""")

# ---------------------------------------------------------------- the arithmetic of the new tests
before('''// Everything the five steps show, from the numbers on screen.  Sets
''', r'''// ---------------- one sample and proportions: the arithmetic (beta 1k) ----------------
// Mean and SD (N - 1) of the one sample's scores in ttXO: two passes, the
// mean first, then the squared distances from it (Lessons Learned s11:
// never from the sum of squares, which loses its digits)
LOCAL tt_One()
BEGIN
 LOCAL oj, oq;
 ttNO := SIZE(ttXO);
 oq := 0;
 FOR oj FROM 1 TO ttNO DO oq := oq + ttXO(oj); END;
 ttMO := oq/ttNO;
 oq := 0;
 FOR oj FROM 1 TO ttNO DO oq := oq + (ttXO(oj)-ttMO)^2; END;
 ttSO := (oq/(ttNO-1))^.5;
END;

// Is wv a whole number from wlo to whi?  (a count, or a sample size)
LOCAL tt_Whole(wv, wlo, whi)
BEGIN
 IF wv < wlo OR wv > whi THEN RETURN 0; END;
 IF FP(wv) <> 0 THEN RETURN 0; END;
 RETURN 1;
END;

// The one-sample t-test and the two z-tests: check the numbers on screen
// and work out what the five steps show.  Returns 1, or 0 with ttOK = 0
// and the reason in ttMSG when the numbers give no test.  The z-tests
// are finished here; the one-sample t goes back to tt_Calc for its t
// critical and p, as the other t-tests.
LOCAL tt_CalcN()
BEGIN
 IF ttTY == 4 THEN
  // ---- one sample: t = (mean - mu0)/(s/sqrt(N)) on N - 1 df ----
  // mu0 is always typed.  Typed numbers keep to the fleet's ranges;
  // scores from D1 were checked when the list was read.
  IF tt_Big(ttMU) THEN
   ttOK := 0; ttMSG := "A number you typed has more than 50 digits: too large to work with. Choose Edit the numbers to change it."; RETURN 0;
  END;
  IF ttSRC == 1 THEN
   IF tt_Big(ttMO) OR tt_Big(ttSO) OR tt_Big(ttNO) THEN
    ttOK := 0; ttMSG := "A number you typed has more than 50 digits: too large to work with. Choose Edit the numbers to change it."; RETURN 0;
   END;
   IF ttNO > 10000 THEN ttOK := 0; ttMSG := tt_NMsg(); RETURN 0; END;
   IF MAX(ABS(ttMO), ABS(ttMU)) > 10000 OR ttSO > 1000 THEN ttOK := 0; ttMSG := "The mean and μ"+CHAR(8320)+" must be from -10,000 to 10,000 and the SD at most 1,000. Choose Edit the numbers to change it."; RETURN 0; END;
  ELSE
   ttNO := SIZE(ttXO);
  END;
  IF ttNO < 2 THEN ttOK := 0; ttMSG := "A one-sample t-test needs N of at least 2."; RETURN 0; END;
  IF ttSRC == 2 THEN tt_One(); END;
  IF ttSO < 0 THEN ttOK := 0; ttMSG := "An SD cannot be negative."; RETURN 0; END;
  IF ttSO == 0 THEN ttOK := 0; ttMSG := "The SD is 0: every score is the same, so there is no t."; RETURN 0; END;
  ttSE := ttSO/ttNO^.5;
  ttDF := ttNO-1;
  ttT := (ttMO-ttMU)/ttSE;
  ttD := (ttMO-ttMU)/ttSO;
  ttSP := ttSO;
  RETURN 1;
 END;
 IF ttTY == 5 THEN
  // ---- one proportion: z = (p-hat - p0)/sqrt(p0(1 - p0)/n) ----
  // the SE is built from p0, not from p-hat: the test works out what
  // would happen if H0 were true
  IF tt_Whole(ttNA,1,1000000) == 0 THEN ttOK := 0; ttMSG := "n must be a whole number from 1 to 1,000,000. Choose Edit the numbers to change it."; RETURN 0; END;
  IF tt_Whole(ttKA,0,ttNA) == 0 THEN ttOK := 0; ttMSG := "x, the number of successes, must be a whole number from 0 to n. Choose Edit the numbers to change it."; RETURN 0; END;
  IF ttP0 < 0.00001 OR ttP0 > 0.99999 THEN ttOK := 0; ttMSG := "p"+CHAR(8320)+" must be from 0.00001 to 0.99999. Choose Edit the numbers to change it."; RETURN 0; END;
  ttPA := ttKA/ttNA;
  ttSE := (ttP0*(1-ttP0)/ttNA)^.5;
  ttT := (ttPA-ttP0)/ttSE;
  ttD := ttPA-ttP0;
 ELSE
  // ---- two proportions: z = (p-hat1 - p-hat2)/SE ----
  // under H0 the two samples share one proportion, so the SE is built
  // from the pooled p = (x1 + x2)/(n1 + n2)
  IF tt_Whole(ttNA,1,1000000) == 0 OR tt_Whole(ttNB,1,1000000) == 0 THEN ttOK := 0; ttMSG := "Each n must be a whole number from 1 to 1,000,000. Choose Edit the numbers to change it."; RETURN 0; END;
  IF tt_Whole(ttKA,0,ttNA) == 0 OR tt_Whole(ttKB,0,ttNB) == 0 THEN ttOK := 0; ttMSG := "Each x, a number of successes, must be a whole number from 0 to its n. Choose Edit the numbers to change it."; RETURN 0; END;
  IF ttKA+ttKB == 0 OR ttKA+ttKB == ttNA+ttNB THEN ttOK := 0; ttMSG := "Every case is a success, or none is: the two samples cannot differ, so there is no z."; RETURN 0; END;
  ttPA := ttKA/ttNA; ttPB := ttKB/ttNB;
  ttPP := (ttKA+ttKB)/(ttNA+ttNB);
  ttSE := (ttPP*(1-ttPP)*(1/ttNA+1/ttNB))^.5;
  ttT := (ttPA-ttPB)/ttSE;
  ttD := ttPA-ttPB;
 END;
 // a z-test: no df; z critical, p and the decision from the normal curve
 ttDF := 0;
 ttTC := tt_ZCrit();
 ttP := tt_ZP(ttT);
 ttREJ := tt_Beyond(ttT,ttTC);
 RETURN 1;
END;

''')
after(''' LOCAL cr, cbk;
 ttOK := 1; ttMSG := "";
''', ''' // beta 1k: the one-sample t-test and the z-tests check and work out
 // their own numbers (tt_CalcN).  The z-tests are finished there; the
 // one-sample t goes on to t critical and p below.
 IF ttTY >= 4 THEN
  IF tt_CalcN() == 0 THEN RETURN 0; END;
  IF ttTY >= 5 THEN RETURN 1; END;
 END;
 IF ttTY <= 3 THEN
''')
before(''' ttTC := tt_Crit(ttDF);
 ttDFT := tt_TabDF(ttDF);
''', ''' END;
''')

# ---------------------------------------------------------------- words
before(''' RETURN "Dependent-samples t-test";
''', ''' IF ttTY == 4 THEN RETURN "One-sample t-test"; END;
 IF ttTY == 5 THEN RETURN "One-proportion z-test"; END;
 IF ttTY == 6 THEN RETURN "Two-proportion z-test"; END;
''')
rep('''// "t(73)" or "t(72.44)"
LOCAL tt_TDf()
BEGIN
''', '''// "t(73)" or "t(72.44)"; "z" for a z-test, which has no df (beta 1k)
LOCAL tt_TDf()
BEGIN
 IF ttTY >= 5 THEN RETURN "z"; END;
''')
rep(''' DRAWMENU({"1 H","2 df","3 crit","4 t","5 end","Menu"});
''', ''' // a z-test has no df and no t: its second and fourth keys say so
 // (beta 1k)
 IF ttTY >= 5 THEN
  DRAWMENU({"1 H","2 dist","3 crit","4 z","5 end","Menu"});
 ELSE
  DRAWMENU({"1 H","2 df","3 crit","4 t","5 end","Menu"});
 END;
''')

# ---------------------------------------------------------------- the curve: t, or the normal curve for a z-test
rep('''// time (Lessons Learned s6: shade by columns, never by samples).
''', '''// time (Lessons Learned s6: shade by columns, never by samples).
// beta 1k: for a z-test the curve is the standard normal curve (tt_Dens)
// and the labels say z (tt_SL).
''')
rep(' cpk := STUDENT(ttDF,0);\n', ' cpk := tt_Dens(0);\n')
rep('  cf := STUDENT(ttDF,cx);\n', '  cf := tt_Dens(cx);\n')
rep('    TEXTOUT_P("t crit",G1,IFTE(cs < 0,ttPL+3,ttPR-38),cy0+2,1,ttRED);\n',
    '    TEXTOUT_P(tt_SL()+" crit",G1,IFTE(cs < 0,ttPL+3,ttPR-38),cy0+2,1,ttRED);\n')
rep('  cs := "t obt = "+tt_Cm(tt_Fmt(ttT,2));\n', '  cs := tt_SL()+" obt = "+tt_Cm(tt_Fmt(ttT,2));\n')

# ---------------------------------------------------------------- the pages of the new tests
before('''// ---------------- pooled or separate? ----------------
''', r'''// ---------------- one sample and proportions: the pages (beta 1k) ----------------
// Steps 1, 2, 4 and 5 of the one-sample t-test and of the two z-tests,
// and step 3 of the z-tests (the one-sample t shares tt_Step3 with the
// other t-tests).  They are laid out like the two-sample pages above.

// A mean or an SD for these pages: as it was typed, or to 4 significant
// digits when the program worked it out from the scores in D1
LOCAL tt_VN(vnv)
BEGIN
 IF ttSRC == 2 THEN RETURN tt_Cm(tt_Sig(vnv)); END;
 RETURN tt_Cm(tt_Num(vnv));
END;

// A number's text in brackets when it is negative: "1.2 - (-3)".  On the
// Prime a negative number's text begins with the true minus sign,
// CHAR(8722) (Lessons Learned s3), not the hyphen of the keyboard.
LOCAL tt_Par(prs)
BEGIN
 IF DIM(prs) > 0 THEN
  IF LEFT(prs,1) == "-" OR LEFT(prs,1) == CHAR(8722) THEN RETURN "("+prs+")"; END;
 END;
 RETURN prs;
END;

// ---- step 1: the hypotheses and the data ----
LOCAL tt_Step1N()
BEGIN
 LOCAL sh, sj, sn, sk, sw, sc;
 LOCAL sx, sy, ss;
 sh := tt_HS();
 tt_Frame("Step 1. The hypotheses");
 TEXTOUT_P(tt_TName()+", "+tt_TailS()+", "+tt_AlS(),G1,8,30,1,ttGRAY);
 // H0: the value it claims (one sample), or equal proportions (two)
 IF ttTY == 4 THEN
  TEXTOUT_P("H"+CHAR(8320)+": μ = μ"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttMU))+"   (the population mean is μ"+CHAR(8320)+")",G1,8,46,1,ttBLUE);
 END;
 IF ttTY == 5 THEN
  TEXTOUT_P("H"+CHAR(8320)+": p = p"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttP0))+"   (the population proportion is p"+CHAR(8320)+")",G1,8,46,1,ttBLUE);
 END;
 IF ttTY == 6 THEN
  TEXTOUT_P("H"+CHAR(8320)+": p"+CHAR(8321)+" = p"+CHAR(8322)+"   (the population proportions are equal)",G1,8,46,1,ttBLUE);
 END;
 // H1: either way, or the direction chosen
 ss := " ≠ ";
 IF ttTL < 0 THEN ss := " < "; END;
 IF ttTL > 0 THEN ss := " > "; END;
 ss := "H"+CHAR(8321)+": "+sh(1)+ss+sh(2);
 IF ttTL == 0 THEN
  IF ttTY == 6 THEN
   TEXTOUT_P(ss+"   (they differ, either way)",G1,8,60,1,ttMAG);
  ELSE
   TEXTOUT_P(ss+"   (it differs, either way)",G1,8,60,1,ttMAG);
  END;
 ELSE
  TEXTOUT_P(ss+"   (a predicted direction)",G1,8,60,1,ttMAG);
 END;
 IF ttTY == 4 AND ttSRC == 1 THEN
  // one sample, from its typed mean, SD and N
  RECT_P(G1,4,76,315,134,ttORNG,ttLORN);
  TEXTOUT_P("The sample:",G1,10,80,1,ttGRAY);
  TEXTOUT_P(CHAR(57344)+" = "+tt_Cm(tt_Num(ttMO))+",   s = "+tt_Cm(tt_Num(ttSO))+",   N = "+tt_Cm(tt_Num(ttNO)),G1,10,95,1,ttBLK);
  TEXTOUT_P("The mean H"+CHAR(8320)+" claims:   μ"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttMU)),G1,10,114,1,ttBLK);
  IF DIM(ttDV) > 0 THEN TEXTOUT_P("Outcome: "+ttDV,G1,8,144,1,ttGRAY); END;
 END;
 IF ttTY == 4 AND ttSRC == 2 THEN
  // one sample, from the scores in D1: the first of them in two rows,
  // as many to a row as their widest text allows
  RECT_P(G1,4,74,315,176,ttORNG,ttLORN);
  TEXTOUT_P("The sample ("+ttG1+"):  N = "+tt_Cm(STRING(ttNO,1,0))+" scores",G1,10,78,1,ttGRAY);
  // the decimals the scores shown need, and their widest text
  sk := 0;
  FOR sj FROM 1 TO MIN(ttNO,10) DO sk := MAX(sk, tt_NDec(ttXO(sj))); END;
  sw := 1;
  FOR sj FROM 1 TO MIN(ttNO,10) DO sw := MAX(sw, DIM(tt_Cm(tt_FixD(ttXO(sj),sk)))); END;
  sc := 5;
  IF sw > 8 THEN sc := 4; END;
  IF sw > 11 THEN sc := 3; END;
  IF sw > 15 THEN sc := 2; END;
  sn := MIN(ttNO,2*sc);
  FOR sj FROM 1 TO sn DO
   sx := 14 + IP(300/sc)*((sj-1) MOD sc);
   sy := 93 + 13*IP((sj-1)/sc);
   TEXTOUT_P(tt_Cm(tt_FixD(ttXO(sj),sk)),G1,sx,sy,1,ttBLK);
  END;
  IF ttNO > sn THEN TEXTOUT_P("... and "+tt_Cm(STRING(ttNO-sn,1,0))+" more",G1,14,119,1,ttGRAY); END;
  TEXTOUT_P(CHAR(57344)+" = "+tt_Cm(tt_Sig(ttMO))+",   s = "+tt_Cm(tt_Sig(ttSO)),G1,10,135,1,ttBLK);
  TEXTOUT_P("The mean H"+CHAR(8320)+" claims:   μ"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttMU)),G1,10,148,1,ttBLK);
  IF DIM(ttDV) > 0 THEN TEXTOUT_P("Outcome: "+ttDV,G1,10,162,1,ttGRAY); END;
 END;
 IF ttTY == 5 THEN
  // one proportion: x successes in n cases
  RECT_P(G1,4,76,315,146,ttORNG,ttLORN);
  TEXTOUT_P("The sample:",G1,10,80,1,ttGRAY);
  TEXTOUT_P("x = "+tt_Cm(tt_Num(ttKA))+" successes in n = "+tt_Cm(tt_Num(ttNA))+" cases",G1,10,95,1,ttBLK);
  TEXTOUT_P(CHAR(57345)+" = x/n = "+tt_Cm(tt_Sig(ttPA)),G1,10,109,1,ttBLK);
  TEXTOUT_P("The proportion H"+CHAR(8320)+" claims:   p"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttP0)),G1,10,127,1,ttBLK);
  IF DIM(ttDV) > 0 THEN TEXTOUT_P("Success: "+ttDV,G1,8,156,1,ttGRAY); END;
 END;
 IF ttTY == 6 THEN
  // two proportions: a column per sample, as the two-means page
  RECT_P(G1,4,76,315,152,ttORNG,ttLORN);
  TEXTOUT_P("Sample 1",G1,10,80,1,ttBLK);
  TEXTOUT_P("Sample 2",G1,165,80,1,ttBLK);
  TEXTOUT_P(ttG1,G1,10,93,1,ttGRAY);
  TEXTOUT_P(ttG2,G1,165,93,1,ttGRAY);
  TEXTOUT_P("x"+CHAR(8321)+" = "+tt_Cm(tt_Num(ttKA)),G1,10,108,1,ttBLK);
  TEXTOUT_P("x"+CHAR(8322)+" = "+tt_Cm(tt_Num(ttKB)),G1,165,108,1,ttBLK);
  TEXTOUT_P("n"+CHAR(8321)+" = "+tt_Cm(tt_Num(ttNA)),G1,10,122,1,ttBLK);
  TEXTOUT_P("n"+CHAR(8322)+" = "+tt_Cm(tt_Num(ttNB)),G1,165,122,1,ttBLK);
  TEXTOUT_P(CHAR(57345)+CHAR(8321)+" = "+tt_Cm(tt_Sig(ttPA)),G1,10,136,1,ttBLK);
  TEXTOUT_P(CHAR(57345)+CHAR(8322)+" = "+tt_Cm(tt_Sig(ttPB)),G1,165,136,1,ttBLK);
  IF DIM(ttDV) > 0 THEN TEXTOUT_P("Success: "+ttDV,G1,8,160,1,ttGRAY); END;
  TEXTOUT_P("x = the successes, n = the cases;  "+CHAR(57345)+" = x/n.",G1,8,176,1,ttGRAY);
  TEXTOUT_P("Sample 1 minus sample 2, all the way through.",G1,8,189,1,ttGRAY);
 END;
 tt_ShowSteps();
END;

// ---- step 2: the distribution; df, or the check of the counts ----
LOCAL tt_Step2N()
BEGIN
 LOCAL sa, sb, sok;
 IF ttTY == 4 THEN
  tt_Frame("Step 2. Distribution and df");
  TEXTOUT_P("The distribution is t: its shape depends on df.",G1,8,32,1,ttBLK);
  TEXTOUT_P("One sample:  df = N - 1",G1,8,54,1,ttBLUE);
  TEXTOUT_P("   = "+tt_Cm(tt_Num(ttNO))+" - 1 = "+tt_Cm(STRING(ttDF,1,0)),G1,8,69,1,ttBLUE);
  TEXTOUT_P("The sample mean uses up one df: the N distances",G1,8,90,1,ttGRAY);
  TEXTOUT_P("from it always add to zero.",G1,8,103,1,ttGRAY);
  TEXTOUT_P("The more df, the closer t comes to the normal",G1,8,160,1,ttGRAY);
  TEXTOUT_P("curve; few df give a wider, flatter t.",G1,8,173,1,ttGRAY);
 ELSE
  tt_Frame("Step 2. The distribution");
  TEXTOUT_P("The distribution is z, the standard normal curve.",G1,8,32,1,ttBLK);
  TEXTOUT_P("A z-test has no df: the curve never changes.",G1,8,47,1,ttBLUE);
  // the normal curve stands in for the binomial distribution, and fits
  // it well only when the counts are large enough: the book's rule
  TEXTOUT_P("The curve is an approximation.  It fits well when",G1,8,68,1,ttBLK);
  IF ttTY == 5 THEN
   sa := ttNA*ttP0; sb := ttNA*(1-ttP0);
   TEXTOUT_P("n p"+CHAR(8320)+" and n(1 - p"+CHAR(8320)+") are both at least 5:",G1,8,81,1,ttBLK);
   TEXTOUT_P("n p"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttNA))+" × "+tt_Cm(tt_Num(ttP0))+" = "+tt_Cm(tt_Sig(sa)),G1,8,98,1,ttBLUE);
   TEXTOUT_P("n(1 - p"+CHAR(8320)+") = "+tt_Cm(tt_Num(ttNA))+" × "+tt_Cm(tt_Num(1-ttP0))+" = "+tt_Cm(tt_Sig(sb)),G1,8,111,1,ttBLUE);
   sok := 0;
   IF sa >= 5 AND sb >= 5 THEN sok := 1; END;
  ELSE
   TEXTOUT_P("each sample has at least 5 successes and 5 failures:",G1,8,81,1,ttBLK);
   TEXTOUT_P("sample 1:  "+tt_Cm(tt_Num(ttKA))+" and "+tt_Cm(tt_Num(ttNA-ttKA)),G1,8,98,1,ttBLUE);
   TEXTOUT_P("sample 2:  "+tt_Cm(tt_Num(ttKB))+" and "+tt_Cm(tt_Num(ttNB-ttKB)),G1,8,111,1,ttBLUE);
   sok := 0;
   IF MIN(MIN(ttKA,ttNA-ttKA),MIN(ttKB,ttNB-ttKB)) >= 5 THEN sok := 1; END;
  END;
  IF sok THEN
   TEXTOUT_P("Yes: the normal curve fits.",G1,8,130,1,ttGRN);
  ELSE
   TEXTOUT_P("No: the curve fits poorly, so p is only rough.",G1,8,130,1,ttRED);
   IF ttTY == 5 THEN
    TEXTOUT_P("Use an exact binomial test (FitCheck).",G1,8,143,1,ttRED);
   ELSE
    TEXTOUT_P("Use Fisher's exact test (ChiTable).",G1,8,143,1,ttRED);
   END;
  END;
  TEXTOUT_P("z is what t becomes when df grows without end.",G1,8,173,1,ttGRAY);
 END;
 tt_ShowSteps();
END;

// ---- step 3 of a z-test: z critical and the rule ----
LOCAL tt_Step3Z()
BEGIN
 tt_Frame("Step 3. Critical value, decision rule");
 TEXTOUT_P(tt_AlS()+", "+tt_TailS()+";  the normal curve, so no df",G1,8,30,1,ttBLK);
 TEXTOUT_P("z crit = "+tt_CritS(ttTC),G1,8,44,1,ttRED);
 IF ttTL == 0 THEN
  TEXTOUT_P("Rule: if z obt > "+tt_Cm(tt_Fmt(ttTC,3))+" or z obt < "+tt_Cm(tt_Fmt(-ttTC,3))+",",G1,8,60,1,ttBLK);
 ELSE
  IF ttTL < 0 THEN
   TEXTOUT_P("Rule: if z obt < "+tt_Cm(tt_Fmt(-ttTC,3))+",",G1,8,60,1,ttBLK);
  ELSE
   TEXTOUT_P("Rule: if z obt > "+tt_Cm(tt_Fmt(ttTC,3))+",",G1,8,60,1,ttBLK);
  END;
 END;
 TEXTOUT_P("  reject H"+CHAR(8320)+".  Red = the rejection region (α).",G1,8,73,1,ttBLK);
 TEXTOUT_P("z crit is the same for every sample size.",G1,8,89,1,ttGRAY);
 tt_Curve(114,196,0,0);
 tt_ShowSteps();
END;

// ---- step 4: the standard error and t or z obtained ----
LOCAL tt_Step4N()
BEGIN
 IF ttTY == 4 THEN
  tt_Frame("Step 4. Standard error and t obtained");
  // the mean and SD as typed, or to 4 digits when they came from D1
  TEXTOUT_P(CHAR(57344)+" = "+tt_VN(ttMO)+",   s = "+tt_VN(ttSO)+",   N = "+tt_Cm(tt_Num(ttNO))+",   μ"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttMU)),G1,8,34,1,ttBLK);
  TEXTOUT_P("SE = s/√N = "+tt_VN(ttSO)+"/√"+tt_Cm(tt_Num(ttNO))+" = "+tt_Cm(tt_Sig(ttSE)),G1,8,58,1,ttBLUE);
  TEXTOUT_P("t obt = ("+CHAR(57344)+" - μ"+CHAR(8320)+")/SE = ("+tt_VN(ttMO)+" - "+tt_Par(tt_Cm(tt_Num(ttMU)))+")/"+tt_Cm(tt_Sig(ttSE)),G1,8,82,1,ttMAG);
  TEXTOUT_P("      = "+tt_Cm(tt_Sig(ttMO-ttMU))+"/"+tt_Cm(tt_Sig(ttSE))+" = "+tt_Cm(tt_Fmt(ttT,2)),G1,8,95,1,ttMAG);
  TEXTOUT_P("t obt counts the standard errors between the",G1,8,120,1,ttGRAY);
  TEXTOUT_P("sample mean and μ"+CHAR(8320)+".",G1,8,133,1,ttGRAY);
 END;
 IF ttTY == 5 THEN
  tt_Frame("Step 4. Standard error and z obtained");
  TEXTOUT_P(CHAR(57345)+" = x/n = "+tt_Cm(tt_Num(ttKA))+"/"+tt_Cm(tt_Num(ttNA))+" = "+tt_Cm(tt_Sig(ttPA)),G1,8,32,1,ttBLK);
  TEXTOUT_P("SE = √(p"+CHAR(8320)+"(1 - p"+CHAR(8320)+")/n)",G1,8,50,1,ttBLUE);
  TEXTOUT_P("   = √("+tt_Cm(tt_Num(ttP0))+" × "+tt_Cm(tt_Num(1-ttP0))+"/"+tt_Cm(tt_Num(ttNA))+") = "+tt_Cm(tt_Sig(ttSE)),G1,8,63,1,ttBLK);
  TEXTOUT_P("z obt = ("+CHAR(57345)+" - p"+CHAR(8320)+")/SE = ("+tt_Cm(tt_Sig(ttPA))+" - "+tt_Cm(tt_Num(ttP0))+")/"+tt_Cm(tt_Sig(ttSE)),G1,8,84,1,ttMAG);
  TEXTOUT_P("      = "+tt_Cm(tt_Sig(ttPA-ttP0))+"/"+tt_Cm(tt_Sig(ttSE))+" = "+tt_Cm(tt_Fmt(ttT,2)),G1,8,97,1,ttMAG);
  TEXTOUT_P("SE is built from p"+CHAR(8320)+", not from "+CHAR(57345)+": the test works",G1,8,120,1,ttGRAY);
  TEXTOUT_P("out what would happen if H"+CHAR(8320)+" were true.",G1,8,133,1,ttGRAY);
 END;
 IF ttTY == 6 THEN
  tt_Frame("Step 4. Standard error and z obtained");
  TEXTOUT_P(CHAR(57345)+CHAR(8321)+" = x"+CHAR(8321)+"/n"+CHAR(8321)+" = "+tt_Cm(tt_Num(ttKA))+"/"+tt_Cm(tt_Num(ttNA))+" = "+tt_Cm(tt_Sig(ttPA)),G1,8,30,1,ttBLK);
  TEXTOUT_P(CHAR(57345)+CHAR(8322)+" = x"+CHAR(8322)+"/n"+CHAR(8322)+" = "+tt_Cm(tt_Num(ttKB))+"/"+tt_Cm(tt_Num(ttNB))+" = "+tt_Cm(tt_Sig(ttPB)),G1,8,43,1,ttBLK);
  // under H0 the two samples share one proportion: pool them
  TEXTOUT_P("Pooled, because H"+CHAR(8320)+" gives both samples one p:",G1,8,58,1,ttBLUE);
  TEXTOUT_P("p = (x"+CHAR(8321)+" + x"+CHAR(8322)+")/(n"+CHAR(8321)+" + n"+CHAR(8322)+") = "+tt_Cm(tt_Num(ttKA+ttKB))+"/"+tt_Cm(tt_Num(ttNA+ttNB))+" = "+tt_Cm(tt_Sig(ttPP)),G1,8,71,1,ttBLUE);
  TEXTOUT_P("SE = √(p(1 - p)(1/n"+CHAR(8321)+" + 1/n"+CHAR(8322)+"))",G1,8,86,1,ttBLUE);
  TEXTOUT_P("   = √("+tt_Cm(tt_Sig(ttPP))+" × "+tt_Cm(tt_Sig(1-ttPP))+" × (1/"+tt_Cm(tt_Num(ttNA))+" + 1/"+tt_Cm(tt_Num(ttNB))+"))",G1,8,99,1,ttBLK);
  TEXTOUT_P("   = "+tt_Cm(tt_Sig(ttSE)),G1,8,112,1,ttBLK);
  TEXTOUT_P("z obt = ("+CHAR(57345)+CHAR(8321)+" - "+CHAR(57345)+CHAR(8322)+")/SE = ("+tt_Cm(tt_Sig(ttPA))+" - "+tt_Cm(tt_Sig(ttPB))+")/"+tt_Cm(tt_Sig(ttSE)),G1,8,129,1,ttMAG);
  TEXTOUT_P("      = "+tt_Cm(tt_Sig(ttPA-ttPB))+"/"+tt_Cm(tt_Sig(ttSE))+" = "+tt_Cm(tt_Fmt(ttT,2)),G1,8,142,1,ttMAG);
 END;
 tt_ShowSteps();
END;

// ---- step 5: the decision ----
LOCAL tt_Step5N()
BEGIN
 LOCAL sd;
 tt_Frame("Step 5. Decision and conclusion");
 IF ttREJ THEN
  TEXTOUT_P(tt_SL()+" obt = "+tt_Cm(tt_Fmt(ttT,3))+" is beyond "+tt_SL()+" crit = "+tt_CritS(ttTC)+":",G1,8,30,1,ttRED);
  TEXTOUT_P("REJECT H"+CHAR(8320)+".",G1,8,43,1,ttRED);
  // which way: the sample's side of the value H0 claims, or sample 1's
  // side of sample 2
  sd := "higher";
  IF ttT < 0 THEN sd := "lower"; END;
  IF ttTY == 4 THEN
   IF ttTL == 0 THEN
    TEXTOUT_P("The population mean differs significantly from μ"+CHAR(8320)+":",G1,8,58,1,ttBLK);
   ELSE
    TEXTOUT_P("The mean differs from μ"+CHAR(8320)+" the way H"+CHAR(8321)+" predicted:",G1,8,58,1,ttBLK);
   END;
   TEXTOUT_P("the sample mean is "+sd+" than μ"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttMU))+".",G1,8,71,1,ttBLK);
  END;
  IF ttTY == 5 THEN
   IF ttTL == 0 THEN
    TEXTOUT_P("The proportion differs significantly from p"+CHAR(8320)+":",G1,8,58,1,ttBLK);
   ELSE
    TEXTOUT_P("The proportion differs from p"+CHAR(8320)+" the way H"+CHAR(8321)+" predicted:",G1,8,58,1,ttBLK);
   END;
   TEXTOUT_P("the sample proportion is "+sd+" than p"+CHAR(8320)+" = "+tt_Cm(tt_Num(ttP0))+".",G1,8,71,1,ttBLK);
  END;
  IF ttTY == 6 THEN
   IF ttTL == 0 THEN
    TEXTOUT_P("The population proportions differ significantly:",G1,8,58,1,ttBLK);
   ELSE
    TEXTOUT_P("The proportions differ the way H"+CHAR(8321)+" predicted:",G1,8,58,1,ttBLK);
   END;
   TEXTOUT_P("sample 1 ("+ttG1+") has the "+sd+" proportion.",G1,8,71,1,ttBLK);
  END;
 ELSE
  TEXTOUT_P(tt_SL()+" obt = "+tt_Cm(tt_Fmt(ttT,3))+" is not beyond "+tt_SL()+" crit = "+tt_CritS(ttTC)+":",G1,8,30,1,ttGRN);
  TEXTOUT_P("RETAIN H"+CHAR(8320)+".",G1,8,43,1,ttGRN);
  TEXTOUT_P("No significant difference: no support for H"+CHAR(8321)+".",G1,8,58,1,ttBLK);
  // one-tailed, and the difference lies the opposite way to H1's
  IF ttTL <> 0 AND ttT*ttTL < 0 THEN
   IF ttTY == 6 THEN
    TEXTOUT_P("The samples even differ the other way from H"+CHAR(8321)+".",G1,8,71,1,ttBLK);
   ELSE
    TEXTOUT_P("The sample even differs the other way from H"+CHAR(8321)+".",G1,8,71,1,ttBLK);
   END;
  END;
 END;
 // The one-sample t: the printed table's row can decide differently from
 // the exact df.  Otherwise a p that rounds to alpha shows its 4 digits,
 // so "p = 0.050" never stands beside a decision it seems to contradict.
 IF ttTY == 4 AND ttREJ <> ttREJB THEN
  TEXTOUT_P("(Table row "+tt_Cm(STRING(ttDFT,1,0))+", "+tt_CritS(ttTB)+", decides the other way.)",G1,8,84,1,ttGRAY);
 ELSE
  IF ttAL >= 0.001 AND ROUND(ttP,3) == ROUND(ttAL,3) AND ttP <> ttAL THEN
   IF ttP < ttAL THEN
    TEXTOUT_P("(p = "+tt_Cm(tt_Sig(ttP))+": just below "+tt_AlS()+".)",G1,8,84,1,ttGRAY);
   ELSE
    TEXTOUT_P("(p = "+tt_Cm(tt_Sig(ttP))+": just above "+tt_AlS()+".)",G1,8,84,1,ttGRAY);
   END;
  END;
 END;
 TEXTOUT_P("Report "+tt_TDf()+" = "+tt_Cm(tt_Fmt(ttT,2))+", p"+tt_Rel(tt_Cm(tt_FmtP(ttP,3)))+", "+tt_TailS(),G1,8,97,1,ttMAG);
 // the size of the difference: Cohen's d for a mean, the difference
 // itself for proportions
 IF ttTY == 4 THEN
  TEXTOUT_P("Cohen's d"+tt_DS()+"  (("+CHAR(57344)+" - μ"+CHAR(8320)+")/s)",G1,8,110,1,ttMAG);
 END;
 IF ttTY == 5 THEN
  TEXTOUT_P("Difference: "+CHAR(57345)+" - p"+CHAR(8320)+" = "+tt_Cm(tt_Fmt(ttD,3)),G1,8,110,1,ttMAG);
 END;
 IF ttTY == 6 THEN
  TEXTOUT_P("Difference: "+CHAR(57345)+CHAR(8321)+" - "+CHAR(57345)+CHAR(8322)+" = "+tt_Cm(tt_Fmt(ttD,3)),G1,8,110,1,ttMAG);
 END;
 TEXTOUT_P("magenta area = p",G1,216,110,1,ttMAG);
 tt_Curve(134,196,1,1);
 tt_ShowSteps();
END;

''')

# ---------------------------------------------------------------- pooled or separate: not for the new tests
before(''' IF ttTY == 3 THEN
  MSGBOX("Pooled or separate variances is a question for INDEPENDENT samples.''', ''' // beta 1k: the one-sample t-test and the z-tests have no such choice
 IF ttTY >= 4 THEN
  MSGBOX("Pooled or separate variances is a question for a test of TWO independent means. The test on screen has no such choice.");
  tt_Settle();
  RETURN 0;
 END;
''')

# ---------------------------------------------------------------- choosing the test
before('''// ---------------- data in ----------------
''', r'''// ---------------- which test? (beta 1k) ----------------
// Which numbers a test uses: the two independent t-tests share theirs
// (family 1); every other test has numbers of its own.  A change of
// family asks for new numbers.
LOCAL tt_Fam(fty)
BEGIN
 IF fty <= 2 THEN RETURN 1; END;
 RETURN fty;
END;

// The test to run: a short menu first, and for two means the flowchart.
// Returns 1-6 (1 pooled, 2 separate, 3 dependent, 4 one-sample t, 5 one-
// proportion z, 6 two-proportion z), or 0 if the menu or the flowchart
// was left with Esc.
LOCAL tt_Pick()
BEGIN
 LOCAL pkc;
 pkc := 0;
 CHOOSE(pkc,"Which test?",{"Two means: t (flowchart)","One mean: one-sample t","One proportion: z","Two proportions: z"});
 tt_Settle();
 IF pkc == 0 THEN RETURN 0; END;
 IF pkc == 1 THEN RETURN tt_Flow(); END;
 RETURN pkc + 2;
END;

''')

# ---------------------------------------------------------------- tails: the symbols of the test on screen
rep('''LOCAL tt_AskTails()
BEGIN
 LOCAL ak, aa, al, at;
 ak := 0;
 CHOOSE(ak,"Tails",{"Two-tailed: μ₁ ≠ μ₂","One-tailed: μ₁ < μ₂","One-tailed: μ₁ > μ₂"});
''', '''LOCAL tt_AskTails()
BEGIN
 LOCAL ak, aa, al, at;
 LOCAL ah;
 ak := 0;
 // the two sides of the hypotheses, in the symbols of the test on
 // screen (beta 1k): mu1 and mu2, mu and mu0, p and p0, or p1 and p2
 ah := tt_HS();
 CHOOSE(ak,"Tails",{"Two-tailed: "+ah(1)+" ≠ "+ah(2),"One-tailed: "+ah(1)+" < "+ah(2),"One-tailed: "+ah(1)+" > "+ah(2)});
''')

# ---------------------------------------------------------------- the numbers of the new tests
before('''// The numbers for the test chosen.  Returns 1 when they are in and
''', r'''// The numbers for a one-sample t-test or a z-test (beta 1k).  Returns 1
// when they are in, 0 if cancelled.  As in tt_AskData below, nothing
// changes until a form is OK'd or a list is read: the forms fill local
// variables first.  Every field is {name,[0]}, a real number only.
LOCAL tt_AskDataN()
BEGIN
 LOCAL ds, dok, dl1, da, db, dc;
 LOCAL dd;
 IF ttTY == 4 THEN
  ds := 0;
  CHOOSE(ds,"The sample",{"Type the mean, SD, N","Raw scores in D1"});
  tt_Settle();
  IF ds == 0 THEN RETURN 0; END;
  IF ds == 1 THEN
   da := ttMO; db := ttSO; dc := ttNO; dd := ttMU;
   dok := INPUT({{da,[0]},{db,[0]},{dc,[0]},{dd,[0]}},"One sample",{"Mean:","SD:","N:","μ₀:"},
    {"The sample's mean, -10,000 to 10,000","SD (N - 1), at most 1,000","Size, 2 to 10,000","The mean H0 claims, -10,000 to 10,000"});
   tt_Settle();
   IF dok == 0 THEN RETURN 0; END;
   // a whole N, as the other forms take it
   ttMO := da; ttSO := db; ttNO := IP(dc); ttMU := dd;
   ttSRC := 1;
   ttG1 := "Group 1"; ttG2 := "Group 2";
  ELSE
   dl1 := tt_ReadD(1);
   IF SIZE(dl1) < 2 THEN
    MSGBOX("Put the sample in D1 of the Statistics 1Var app: at least 2 scores.");
    tt_Settle();
    RETURN 0;
   END;
   // a value too large to square is refused before any arithmetic
   // (tt_Big), and nothing changes
   IF tt_BigL(dl1) > 0 THEN
    MSGBOX(tt_BigLMsg(dl1,{0}));
    tt_Settle();
    RETURN 0;
   END;
   // the scores are in D1; H0's mean is still to be typed
   dd := ttMU;
   dok := INPUT({{dd,[0]}},"One sample: scores in D1",{"μ₀:"},{"The mean H0 claims for the population"});
   tt_Settle();
   IF dok == 0 THEN RETURN 0; END;
   ttXO := dl1; ttMU := dd;
   ttSRC := 2;
   ttG1 := "D1"; ttG2 := "Group 2";
  END;
 END;
 IF ttTY == 5 THEN
  da := ttKA; db := ttNA; dc := ttP0;
  dok := INPUT({{da,[0]},{db,[0]},{dc,[0]}},"One proportion",{"x:","n:","p₀:"},
   {"Successes: a whole number, 0 to n","Cases: a whole number, 1 to 1,000,000","The proportion H0 claims, 0.00001 to 0.99999"});
  tt_Settle();
  IF dok == 0 THEN RETURN 0; END;
  ttKA := da; ttNA := db; ttP0 := dc;
  ttSRC := 1;
  ttG1 := "Group 1"; ttG2 := "Group 2";
 END;
 IF ttTY == 6 THEN
  da := ttKA; db := ttNA; dc := ttKB; dd := ttNB;
  dok := INPUT({{da,[0]},{db,[0]},{dc,[0]},{dd,[0]}},"Two proportions",{"x 1:","n 1:","x 2:","n 2:"},
   {"Sample 1's successes, 0 to n 1","Sample 1's cases, 1 to 1,000,000","Sample 2's successes, 0 to n 2","Sample 2's cases, 1 to 1,000,000"});
  tt_Settle();
  IF dok == 0 THEN RETURN 0; END;
  ttKA := da; ttNA := db; ttKB := dc; ttNB := dd;
  ttSRC := 1;
  ttG1 := "Group 1"; ttG2 := "Group 2";
 END;
 // new numbers: no longer one of the examples
 ttEX := 0; ttDV := "";
 RETURN 1;
END;

''')
rep(''' LOCAL dm, dsd, dn;
 ds := 0;
 IF ttTY <> 3 THEN
''', ''' LOCAL dm, dsd, dn;
 // beta 1k: the one-sample t-test and the z-tests have forms of their own
 IF ttTY >= 4 THEN RETURN tt_AskDataN(); END;
 ds := 0;
 IF ttTY <> 3 THEN
''')

# ---------------------------------------------------------------- examples 4 to 6
after('''  ttG1 := "Male"; ttG2 := "Female";
  ttDV := "amount of drug use experience (SPSS)";
 END;
''', r''' IF ek == 4 THEN
  // Student's sleep data (Cushny and Peebles 1905; Student 1908, the
  // first worked example of the t-test; the book's Chapter 9): for each
  // of 10 patients, the hours of sleep gained with the second drug minus
  // the hours gained with the first.  One-sample t against 0, two-
  // tailed, alpha .05: t(9) = 4.06, p = .003
  ttTY := 4; ttSRC := 2; ttTL := 0; ttAL := 0.05;
  ttXO := {1.2,2.4,1.3,1.3,0,1,1.8,0.8,4.6,1.4};
  ttMU := 0;
  ttG1 := "the differences"; ttG2 := "Group 2";
  ttDV := "extra hours of sleep, Student 1908";
 END;
 IF ek == 5 THEN
  // Castaneda v. Partida, 430 U.S. 482 (1977) (the book's Chapters 5
  // and 12; FitCheck's preset): over 11 years, 339 of the 870 people
  // summoned for grand jury duty in Hidalgo County, Texas were Mexican-
  // American, in a county whose population was 79.1% Mexican-American.
  // The Court counted the shortfall in standard deviations, about 29:
  // that count is this z.  Two-tailed, alpha .05: z = -29.1
  ttTY := 5; ttSRC := 1; ttTL := 0; ttAL := 0.05;
  ttKA := 339; ttNA := 870; ttP0 := 0.791;
  ttG1 := "Group 1"; ttG2 := "Group 2";
  ttDV := "Mexican-American (Castaneda v. Partida)";
 END;
 IF ek == 6 THEN
  // the Rossi experiment (Rossi, Berk and Lenihan 1980; the book's
  // Chapter 11): 432 men released from Maryland state prisons, half of
  // them given financial aid; re-arrested within 52 weeks: 48 of the 216
  // given aid and 66 of the 216 given none.  Two-tailed, alpha .05:
  // z = -1.965, p = .049
  ttTY := 6; ttSRC := 1; ttTL := 0; ttAL := 0.05;
  ttKA := 48; ttNA := 216; ttKB := 66; ttNB := 216;
  ttG1 := "Financial aid"; ttG2 := "No aid";
  ttDV := "re-arrested within 52 weeks (Rossi)";
 END;
''')

# ---------------------------------------------------------------- help: three pages
rep(' tt_Frame("TTestLab help 1/2: Keys");\n', ' tt_Frame("TTestLab help 1/3: Keys");\n')
rep(' tt_Frame("TTestLab help 2/2: The numbers");\n', ' tt_Frame("TTestLab help 2/3: The numbers");\n')
rep(''' TEXTOUT_P("T-Test: 1 μ on the differences, with μ₀ = 0.",G1,8,190,1,ttGRAY);
 TEXTOUT_P("any key or tap = back",G1,8,222,1,ttFOOT);
 BLIT_P(G0,0,0,G1);
 tt_WaitAny();
END;
''', ''' TEXTOUT_P("T-Test: 1 μ on the differences, with μ₀ = 0.",G1,8,190,1,ttGRAY);
 TEXTOUT_P("any key or tap = next page",G1,8,222,1,ttFOOT);
 BLIT_P(G0,0,0,G1);
 tt_WaitAny();
 // page 3 (beta 1k): the one-sample t-test and the two z-tests
 tt_Frame("TTestLab help 3/3: One sample, proportions");
 TEXTOUT_P("ONE-SAMPLE t: a sample's mean against μ₀, the mean H₀ claims",G1,8,30,1,ttBLUE);
 TEXTOUT_P("t obt = ("+CHAR(57344)+" - μ₀)/(s/√N), df = N - 1.  Type the mean, SD and N,",G1,8,43,1,ttBLK);
 TEXTOUT_P("or put the scores in D1 (Apps, Statistics 1Var).",G1,8,56,1,ttBLK);
 TEXTOUT_P("ONE PROPORTION: x successes in n cases against p₀",G1,8,72,1,ttBLUE);
 TEXTOUT_P("z obt = ("+CHAR(57345)+" - p₀)/√(p₀(1 - p₀)/n), where "+CHAR(57345)+" = x/n",G1,8,85,1,ttBLK);
 TEXTOUT_P("TWO PROPORTIONS: x₁ of n₁ against x₂ of n₂",G1,8,101,1,ttBLUE);
 TEXTOUT_P("z obt = ("+CHAR(57345)+"₁ - "+CHAR(57345)+"₂)/SE; SE pools the two samples",G1,8,114,1,ttBLK);
 TEXTOUT_P("A z-test uses the normal curve, which has no df.  Step 2",G1,8,130,1,ttMAG);
 TEXTOUT_P("checks that the counts are large enough for it (at least 5).",G1,8,143,1,ttMAG);
 TEXTOUT_P("Check on the Prime: Inference app, Hyp. test, T-Test: 1 μ,",G1,8,164,1,ttGRAY);
 TEXTOUT_P("Z-Test: 1 π and Z-Test: π₁ - π₂.",G1,8,177,1,ttGRAY);
 TEXTOUT_P("any key or tap = back",G1,8,222,1,ttFOOT);
 BLIT_P(G0,0,0,G1);
 tt_WaitAny();
END;
''')

# ---------------------------------------------------------------- the menu
rep('  mt := tt_Flow();\n', '  mt := tt_Pick();\n', 2)
rep('''   // needs new numbers, and a cancelled form keeps the old test.
   mo := ttTY;
   ttTY := mt;
   IF (mt == 3) <> (mo == 3) THEN
''', '''   // needs new numbers, and a cancelled form keeps the old test.
   // beta 1k: so does a change to or from the one-sample t-test or a
   // z-test, each with numbers of its own (tt_Fam).
   mo := ttTY;
   ttTY := mt;
   IF tt_Fam(mt) <> tt_Fam(mo) THEN
''')
rep('''  CHOOSE(mt,"Examples",{"Age at arrest (pooled)","Matched jails (dependent)","Drug use by sex (separate)"});
''', '''  CHOOSE(mt,"Examples",{"Age at arrest (pooled)","Matched jails (dependent)","Drug use by sex (separate)","Student's sleep (1 sample)","Grand juries (1 proportion)","Re-arrest (2 proportions)"});
''')

# ---------------------------------------------------------------- the pages' switch
rep('''LOCAL tt_Page(pst)
BEGIN
''', '''LOCAL tt_Page(pst)
BEGIN
 // beta 1k: the one-sample t-test and the z-tests have pages of their
 // own; the one-sample t shares step 3 with the other t-tests
 IF ttTY >= 4 THEN
  IF pst == 1 THEN tt_Step1N(); END;
  IF pst == 2 THEN tt_Step2N(); END;
  IF pst == 3 THEN
   IF ttTY == 4 THEN tt_Step3(); ELSE tt_Step3Z(); END;
  END;
  IF pst == 4 THEN tt_Step4N(); END;
  IF pst == 5 THEN tt_Step5N(); END;
  RETURN 0;
 END;
''')

# ---------------------------------------------------------------- main
rep('''  CHOOSE(ms,"TTestLab: t-tests in 5 steps",{"Choose the test (flowchart)","Example: age at arrest","Example: matched jails","Example: drug use by sex","Help"});
  tt_Settle();
  IF ms == 5 THEN tt_Help(); END;
 UNTIL ms <> 5;
''', '''  CHOOSE(ms,"TTestLab: tests in 5 steps",{"Choose the test","Example: age at arrest","Example: matched jails","Example: drug use by sex","Examples: one sample, z-tests","Help"});
  tt_Settle();
  IF ms == 6 THEN tt_Help(); END;
  // beta 1k: the three newer examples have a list of their own, so that
  // every item of this menu stays on the screen (a ninth item would
  // scroll out of sight); Esc there comes back to this menu
  mx := 0;
  IF ms == 5 THEN
   CHOOSE(mx,"One sample and z-tests",{"Student's sleep (1 sample)","Grand juries (1 proportion)","Re-arrest (2 proportions)"});
   tt_Settle();
  END;
 UNTIL ms <> 6 AND (ms <> 5 OR mx > 0);
''')
after(' IF ms >= 2 AND ms <= 4 THEN tt_Example(ms-1); END;\n', ' IF ms == 5 THEN tt_Example(mx+3); END;\n')
rep('EXPORT TTESTLAB()\nBEGIN\n LOCAL ms, mt;\n', 'EXPORT TTESTLAB()\nBEGIN\n LOCAL ms, mt, mx;\n')

# every version string in a literal (as Rounds 11 and 12 did)
s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace('beta 1j', 'beta 1k').replace('beta1j', 'beta1k'), s)
os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'TTestLab_beta1k.txt'), 'w', encoding='utf-8', newline='').write(s)
print('TTestLab beta1j -> beta1k: %d lines' % s.count('\n'))
