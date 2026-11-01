#!/usr/bin/env python3
"""make_tlg1_v1.py -- builds TTestLabG beta 1, the GENERAL version of TTestLab, from TTestLab beta 1b
(the advanced version), by exact replacements: every replacement must find its text exactly the number of times
expected, or the build stops.

What changes (the Chapter Plan's "General and advanced versions" and "Conventions where the textbooks differ",
31 Oct 2026):
  * its own name and tag: EXPORT TTESTLABG, routines tz_, file-level variables tz (TTestLab keeps tt), so both can
    sit on one calculator (one pool of routine names, Lessons Learned s5);
  * separate variances (Welch) is the default: the start state, the flowchart's hint, the "Pooled or separate?"
    page's last lines;
  * t critical is the exact one for the df; the printed table is a note (a df the table lacks takes the next
    smaller row; a fractional df is rounded down first), not a row the program pretends to know: the books' tables
    differ past df 30;
  * step 2 shows the hand shortcut for separate variances (df = the smaller N - 1) and its larger t crit;
  * step 5 gives a p that rounds to alpha its 4 significant digits ("p = 0.04970: just below alpha = 0.050");
  * means and SDs worked out from raw scores print to 4 significant digits (206.3, not 206.32418);
  * no lecture references (Figure 11.2, Tables 11.1-11.4, the lecture's rounding notes, its misprinted table cells);
  * examples: Darwin's 1876 Zea mays pairs (dependent), the 1970 draft lottery (separate; Selective Service), and
    two of the lecture's government-data examples kept (age at arrest, JDCC, pooled; matched jails, Census of Jails,
    dependent).  The SPSS drug-use example stays in the advanced version only.
Run:  python3 make_tlg1_v1.py SRC_TTestLab_beta1b.txt SRC_PowerViz_v2.5k.txt OUT_TTestLabG_beta1.txt
"""
import re
import sys

src_path, pv_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
S = open(src_path, encoding='utf-8').read()
PV = open(pv_path, encoding='utf-8').read()


def rep(old, new, count=1):
    global S
    n = S.count(old)
    if n != count:
        sys.exit('replacement expected %d, found %d: %r' % (count, n, old[:90]))
    S = S.replace(old, new)


def routine_span(name):
    """start and end (past its closing END;) of a routine whose head is 'LOCAL name(' or 'EXPORT name('"""
    m = re.search(r'^(LOCAL|EXPORT) ' + re.escape(name) + r'\(', S, re.M)
    if not m:
        sys.exit('routine not found: ' + name)
    e = S.find('\nEND;\n', m.start())
    return m.start(), e + len('\nEND;\n')


def replace_routine(name, new_text):
    global S
    a, b = routine_span(name)
    S = S[:a] + new_text.strip('\n') + '\n' + S[b:]


def remove_block(start_text, name):
    """remove from start_text (the comment above a routine) through the routine's END;"""
    global S
    a = S.find(start_text)
    if a < 0 or S.count(start_text) != 1:
        sys.exit('block start not found once: ' + start_text[:60])
    _, b = routine_span(name)
    if b < a:
        sys.exit('block order wrong: ' + name)
    # keep one blank line between the neighbours
    S = S[:a] + S[b:].lstrip('\n')


# ---------------------------------------------------------------- 1. the name and the tags
S = re.sub(r'\btt_', 'tz_', S)
S = re.sub(r'\btt(?=[A-Z])', 'tz', S)
rep('EXPORT TTESTLAB()', 'EXPORT TTESTLABG()')
S = S.replace('"TTestLab', '"TTestLabG')
rep('"Quit TTestLab"', '"Quit TTestLabG"')   # the one display name not at a string's start (seen on the Virtual Calculator)
if re.search(r'\btt[A-Z_]', S):
    sys.exit('an old tt name survived the rename')

# ---------------------------------------------------------------- 2. the header
a = S.find('// ============================================================\n// TTESTLAB - beta 1b')
b = S.find('// ---------------- shared state ----------------')
HEADER = r'''// ============================================================
// TTESTLABG - beta 1   (the general version of TTestLab)
// ============================================================
// FREE FOR EDUCATIONAL AND PERSONAL USE.  Keep this header with
//   the file and credit the author if you pass it on.  Not for
//   sale or commercial redistribution.  Provided as is.
// DISCLAIMER: a teaching and demonstration aid. Not validated for
//   forensic, clinical or legal use; do not rely on its results for
//   legal purposes.
// (C) 2026 Roger D Metcalf.  Written with AI assistance (Anthropic
//   Claude); every formula checked against SciPy before delivery.
// Firmware: written for the HP Prime G2 and G1 on the 2026-09-09
//   firmware.  beta 1 has run in the PC harness only so far.
//
// GENERAL AND ADVANCED VERSIONS (Roger, 31 Oct 2026).  TTestLab is
//   the ADVANCED version: Roger's lecture rules, his examples and
//   SPSS output.  TTestLabG is the GENERAL version, for the intro
//   statistics companion guide, Statisticles and any intro course.
//   It is built from TTestLab beta 1b by make_tlg1_v1.py, with the
//   same arithmetic and screens (84 checks and an independent review
//   behind them), and differs in:
//   * its name and tags (tz_, tz), so both versions can sit on one
//     calculator: every program shares one pool of routine names;
//   * separate variances (Welch) as the default test: it does not
//     need equal population variances and loses little when they
//     are equal (Delacre, Lakens & Leys 2017); pooled stays a choice;
//   * t critical exact for the df (the calculator needs no printed
//     table).  A printed table is a note: a df the table lacks takes
//     the next SMALLER row it lists (a larger t crit, the safer
//     side); a fractional df is rounded down first.  The books'
//     tables differ past df 30, so no row is claimed;
//   * step 2 sets the hand shortcut for separate variances beside
//     Welch's df: df = the smaller of N1 - 1 and N2 - 1;
//   * step 5: a p that rounds to alpha at 3 decimals also prints to
//     4 significant digits ("p = 0.04970: just below alpha = 0.050");
//   * means and SDs worked out from raw scores print to 4
//     significant digits (206.3, not 206.32418);
//   * examples: Darwin's 1876 Zea mays pairs (dependent), the 1970
//     draft lottery (separate variances; Selective Service), and two
//     government-data examples from the advanced version: age at
//     arrest (JDCC, pooled) and matched jails (Census of Jails,
//     dependent).
//
// WHAT IT DOES: the t tests an intro course teaches, worked in five
//   steps, with a picture.
//   * Which t test?  Two questions as a tappable flowchart: are the
//     samples independent?  are the population variances equal?
//     (not sure: No) -> separate-variances, pooled-variances or
//     dependent-samples t.
//   * Independent samples from each group's N, mean and SD, or from
//     raw scores in D1 and D2 (Apps, Statistics 1Var; DataLoad fills
//     them from a spreadsheet).  The "Pooled or separate?" page sets
//     the two tests side by side and says when and why they differ.
//   * Dependent samples (matched pairs, before and after) from the
//     pairs in D1 and D2, or from the mean and SD of the differences.
//   * Two-tailed, or one-tailed either way.
//   * The five steps, a screen each: 1 the hypotheses (and the data),
//     2 the distribution and df, 3 the critical value and the decision
//     rule (a t curve with the rejection region shaded), 4 the standard
//     error and t obtained with the numbers put in, 5 the decision and
//     the conclusion (t obtained and the p value on the curve).
//
// HOW THE NUMBERS ARE WORKED OUT (group 1 minus group 2, as SPSS and
//   R do):
//   pooled:    sp = sqrt(((N1-1)s1^2 + (N2-1)s2^2)/(N1+N2-2))
//              SE = sp * sqrt((N1+N2)/(N1*N2)),  df = N1 + N2 - 2
//   separate:  SE = sqrt(s1^2/N1 + s2^2/N2)  (Welch; SPSS's "Equal
//              variances not assumed" row; R's t.test default)
//              df = (a+b)^2 / (a^2/(N1-1) + b^2/(N2-1)), a = s1^2/N1,
//              b = s2^2/N2  (Welch-Satterthwaite; fractional)
//   dependent: xD = x1 - x2 for each pair, sD their SD (N-1),
//              SE = sD/sqrt(Npairs),  df = Npairs - 1
//   t obtained = (mean1 - mean2)/SE, or mean(xD)/SE
//   t critical = -STUDENT_ICDF(df, alpha) one-tailed, alpha/2 two-
//              tailed (a lower tail, mirrored: never ICDF(1 - alpha))
//   p: two-tailed 2*STUDENT_CDF(df, -|t|); H1 mu1 < mu2: STUDENT_CDF(
//      df, t); H1 mu1 > mu2: STUDENT_CDF(df, -t).  Lower tails only.
//   Cohen's d: (mean1 - mean2)/sp (independent; SPSS's Cohen's d);
//      mean(xD)/sD (dependent; SPSS's paired Cohen's d).
//   Squares are taken after dividing by the larger SD (Lessons Learned
//   s11, "scale before squaring"), so no SD over- or underflows.
//
// KEYS AND TOUCH (a GETKEY + MOUSE polling loop, Lessons Learned s6):
//   soft keys 1-5 = the five steps, "Menu" = the menu
//   Left / Right = step back / on,  Enter = menu,  Esc = quit
//   the flowchart: tap Yes or No (or the soft keys), OK = go on
// After every form, menu and box the program drains keys AND waits for
// the finger to lift (tz_Drain, tz_TDrain): a form's OK sits where a
// soft key is, and a finger still on it was once read as a tap
// (PowerViz v2.5h on Roger's calculator, 31 Oct 2026).
//
// NAMES: every routine carries the tag tz_ and every file-level
// variable the tag tz (Lessons Learned s5: all programs on a Prime
// share one pool of routine names, matched ignoring case).
// ============================================================

'''
S = S[:a] + HEADER + S[b:]

# ---------------------------------------------------------------- 3. state: separate by default; no table-row state
rep('LOCAL tzTY:=1;           // the test: 1 pooled, 2 separate, 3 dependent',
    'LOCAL tzTY:=2;           // the test: 1 pooled, 2 separate (the default), 3 dependent')
rep('LOCAL tzEX:=0;           // the example on screen: 0 none, 1-3 the examples',
    'LOCAL tzEX:=0;           // the example on screen: 0 none, 1-4 the examples')
rep('LOCAL tzSE:=1, tzT:=0, tzDF:=1, tzTC:=1, tzTB:=1, tzDFT:=1;\nLOCAL tzP:=1, tzD:=0, tzSP:=1, tzREJ:=0, tzREJB:=0;',
    'LOCAL tzSE:=1, tzT:=0, tzDF:=1, tzTC:=1;\nLOCAL tzP:=1, tzD:=0, tzSP:=1, tzREJ:=0;')

# ---------------------------------------------------------------- 4. comments that named the lecture's tables
rep("// The decimals a column of typed values needs: the most any of them\n// needs, so the pairs print as the lecture's Table 11.3 does, 1.30 and\n// 1.00 beside 1.25 (review 11)",
    "// The decimals a column of typed values needs: the most any of them\n// needs, so a column prints alike: 1.30 and 1.00 beside 1.25")

# ---------------------------------------------------------------- 5. a value on the data screens
rep('''LOCAL tz_Sig(sv)
BEGIN
 LOCAL sd;
 IF sv == 0 THEN RETURN "0"; END;
 sd := MIN(10, MAX(0, 3 - FLOOR(LOG(ABS(sv)))));
 RETURN STRING(ROUND(sv,sd),2,sd);
END;
''', '''LOCAL tz_Sig(sv)
BEGIN
 LOCAL sd;
 IF sv == 0 THEN RETURN "0"; END;
 sd := MIN(10, MAX(0, 3 - FLOOR(LOG(ABS(sv)))));
 RETURN STRING(ROUND(sv,sd),2,sd);
END;

// A mean or SD on the data screens: as it was typed (tz_Num) when it
// was typed; to 4 significant digits (tz_Sig) when the program worked
// it out from raw scores (D1/D2 or an example's data), so a draft
// lottery mean shows as 206.3, not 206.32418.
LOCAL tz_Val(vv)
BEGIN
 IF tzSRC == 2 THEN RETURN tz_Sig(vv); END;
 RETURN tz_Num(vv);
END;
''')
# the means: step 1 and step 4's t obt line; the SDs: step 1 and step 4's pooled and separate SE lines
for v, want in (('tzM1', 2), ('tzM2', 2), ('tzS1', 3), ('tzS2', 3)):
    n = S.count('tz_Num(%s)' % v)
    if n != want:
        sys.exit('tz_Num(%s): expected %d, found %d' % (v, want, n))
    S = S.replace('tz_Num(%s)' % v, 'tz_Val(%s)' % v)

# ---------------------------------------------------------------- 6. no printed-table row, no lecture cells
remove_block("// ---------------- the arithmetic ----------------\n// The row of the printed t table the lecture would read.", 'tz_TabDF')
S = S.replace("// t critical (its size) for df, at alpha,", "// ---------------- the arithmetic ----------------\n// t critical (its size) for df, at alpha,", 1)
remove_block("// The lecture's printed t table (its appendix 1) differs from the exact", 'tz_BookCell')
rep(''' LOCAL cr, cbk;
 tzOK := 1; tzMSG := "";''', ''' LOCAL cr;
 tzOK := 1; tzMSG := "";''')
rep(''' tzTC := tz_Crit(tzDF);
 tzDFT := tz_TabDF(tzDF);
 // the printed table's value, as a student would read it: the exact
 // value to 3 decimals, or the lecture's own figure in its five odd
 // cells (tz_BookCell)
 cbk := tz_BookCell();
 tzTB := IFTE(cbk > 0,cbk,ROUND(tz_Crit(tzDFT),3));
 tzP := tz_PVal(tzT,tzDF);
 tzREJ := tz_Beyond(tzT,tzTC);
 tzREJB := tz_Beyond(tzT,tzTB);''', ''' // t critical for the exact df (a printed table is only a note on
 // step 3: the books' tables differ past df 30)
 tzTC := tz_Crit(tzDF);
 tzP := tz_PVal(tzT,tzDF);
 tzREJ := tz_Beyond(tzT,tzTC);''')

# ---------------------------------------------------------------- 7. step 1: comments
rep('''  // the data, as the lecture's Table 11.1 lays them out: a column per
  // sample, its name under the heading''', '''  // the data: a column per sample, its name under the heading''')
rep('''   // the pairs, as the lecture's Table 11.3''', '''   // the pairs, a row each (the first 7)''')

# ---------------------------------------------------------------- 8. step 2: the hand shortcut for separate variances
rep(''' LOCAL sa, sb, sden;
 tz_Frame("Step 2. Distribution and df");''', ''' LOCAL sa, sb, sden, sdh;
 tz_Frame("Step 2. Distribution and df");''')
rep('''  TEXTOUT_P("A fraction is fine: SPSS prints this df in its",G1,8,118,1,tzGRAY);
  TEXTOUT_P(CHAR(34)+"Equal variances not assumed"+CHAR(34)+" row.",G1,8,131,1,tzGRAY);''',
    '''  // the hand shortcut many books give for separate variances: the
  // smaller N - 1, which gives a larger t crit than Welch's df, so it
  // errs on the safe side (the companion guide's Conventions)
  sdh := MIN(tzN1,tzN2) - 1;
  TEXTOUT_P("A fraction is fine: SPSS and R print this df.",G1,8,116,1,tzGRAY);
  TEXTOUT_P("By hand: df = the smaller of N"+CHAR(8321)+"-1, N"+CHAR(8322)+"-1 = "+STRING(sdh,1,0)+",",G1,8,131,1,tzGRAY);
  TEXTOUT_P("t crit = "+tz_CritS(tz_Crit(sdh))+": larger, so a safer test.",G1,8,144,1,tzGRAY);''')

# ---------------------------------------------------------------- 9. step 3: exact t crit; the printed table as a note
replace_routine('tz_Step3', r'''
LOCAL tz_Step3()
BEGIN
 LOCAL sdf;
 tz_Frame("Step 3. Critical value, decision rule");
 sdf := IFTE(tzTY == 2,tz_Fmt(tzDF,2),STRING(tzDF,1,0));
 TEXTOUT_P(tz_AlS()+", "+tz_TailS()+", df = "+sdf,G1,8,30,1,tzBLK);
 // exact, for this df: the calculator needs no printed table
 TEXTOUT_P("t crit = "+tz_CritS(tzTC)+"   (exact, for df = "+sdf+")",G1,8,44,1,tzRED);
 IF tzTL == 0 THEN
  TEXTOUT_P("Rule: if t obt > "+tz_Fmt(tzTC,3)+" or t obt < "+tz_Fmt(-tzTC,3)+",",G1,8,60,1,tzBLK);
 ELSE
  IF tzTL < 0 THEN
   TEXTOUT_P("Rule: if t obt < "+tz_Fmt(-tzTC,3)+",",G1,8,60,1,tzBLK);
  ELSE
   TEXTOUT_P("Rule: if t obt > "+tz_Fmt(tzTC,3)+",",G1,8,60,1,tzBLK);
  END;
 END;
 IF tzTC > 12 THEN
  TEXTOUT_P("  reject H"+CHAR(8320)+".  (t crit lies beyond the plot.)",G1,8,73,1,tzBLK);
 ELSE
  TEXTOUT_P("  reject H"+CHAR(8320)+".  Red = the rejection region (α).",G1,8,73,1,tzBLK);
 END;
 // A printed t table lists only some df, and the books' tables differ
 // past 30.  The companion guide's rule: a df the table lacks takes the
 // next SMALLER row it lists, whose t crit is larger, so the test never
 // claims more than the data show; a fractional df is rounded down
 // first.  Up to df 30 every table has the row: no note.
 IF tzTY == 2 THEN
  TEXTOUT_P("Printed table?  Round df down to "+STRING(IP(tzDF),1,0)+"; if the",G1,8,87,1,tzGRAY);
  TEXTOUT_P("table lacks that row, take the next smaller.",G1,8,100,1,tzGRAY);
 ELSE
  IF tzDF > 30 THEN
   TEXTOUT_P("Printed table without row "+STRING(tzDF,1,0)+"?  Take the next",G1,8,87,1,tzGRAY);
   TEXTOUT_P("smaller row it lists (its t crit is larger).",G1,8,100,1,tzGRAY);
  END;
 END;
 tz_Curve(114,196,0,0);
 tz_ShowSteps();
END;
''')

# ---------------------------------------------------------------- 10. step 4: no lecture notes
remove_block('''// ---------------- step 4: SE and t obtained ----------------
// What the source printed, for the three examples,''', 'tz_BookNote')
S = S.replace("LOCAL tz_Step4()", "// ---------------- step 4: SE and t obtained ----------------\nLOCAL tz_Step4()", 1)
rep("   // the lecture's Table 11.4: each difference, its deviation, squared",
    "   // each difference, its deviation from the mean, and that squared")
rep('''   // the column's sum (the lecture's sigma sign is not on the verified
   // glyph list, Lessons Learned s5, so the word)''', '''   // the column's sum (the sigma sign is not on the verified glyph
   // list, Lessons Learned s5, so the word)''')
rep(''' tz_BookNote(176);
 tz_ShowSteps();''', ''' tz_ShowSteps();''')

# ---------------------------------------------------------------- 11. step 5: no table row; a p that rounds to alpha
rep(''' // the printed table's row can decide differently from the exact df
 IF tzREJ <> tzREJB THEN
  TEXTOUT_P("(Table row "+STRING(tzDFT,1,0)+", "+tz_CritS(tzTB)+", decides the other way.)",G1,8,84,1,tzGRAY);
 END;''', ''' // A p that rounds to alpha at 3 decimals ("p = 0.050" beside a
 // rejection at alpha .05 reads as a contradiction) also gets its 4
 // significant digits (Darwin's plants: p = 0.04970).
 IF tzAL >= 0.001 AND ROUND(tzP,3) == ROUND(tzAL,3) AND tzP <> tzAL THEN
  TEXTOUT_P("(p = "+tz_Sig(tzP)+": just "+IFTE(tzP < tzAL,"below","above")+" α = "+tz_Fmt(tzAL,3)+".)",G1,8,84,1,tzGRAY);
 END;''')

# ---------------------------------------------------------------- 12. pooled or separate?
rep(''' TEXTOUT_P("The lecture: pooled if the population variances",G1,8,160,1,tzGRAY);
 TEXTOUT_P("are equal, separate if not (Figure 11.2).  Many",G1,8,173,1,tzGRAY);
 TEXTOUT_P("now use separate always (Delacre et al. 2017).",G1,8,186,1,tzGRAY);''',
    ''' // why separate is the default (Delacre, Lakens & Leys 2017)
 TEXTOUT_P("Pooled needs equal population variances;",G1,8,160,1,tzGRAY);
 TEXTOUT_P("separate does not, and loses little when they",G1,8,173,1,tzGRAY);
 TEXTOUT_P("are equal, so it is the default (Delacre 2017).",G1,8,186,1,tzGRAY);''')

# ---------------------------------------------------------------- 13. the flowchart
rep('// ---------------- the flowchart (Figure 11.2) ----------------',
    '// ---------------- the flowchart (two questions) ----------------')
rep(' tz_Frame("Which t test?  (Figure 11.2)");', ' tz_Frame("Which t test?");')
rep(''' // the hint for question 2
 TEXTOUT_P("Equal variances?  The problem says so, or",G1,8,182,1,tzGRAY);
 TEXTOUT_P("Levene's test (SPSS) on the raw scores.",G1,8,195,1,tzGRAY);''',
    ''' // the hint for question 2: separate is the default
 TEXTOUT_P("Not sure the variances are equal?  Answer No:",G1,8,182,1,tzGRAY);
 TEXTOUT_P("the separate t needs no such assumption.",G1,8,195,1,tzGRAY);''')

# ---------------------------------------------------------------- 14. the examples, with the draft lottery's data
m = re.search(r'LOCAL pv_Draft\(dfg\)\nBEGIN\n(.*?)\nEND;\n', PV, re.S)
if not m:
    sys.exit('pv_Draft not found in PowerViz')
draft_body = m.group(1).replace('dfg', 'tdg')
nums = [int(x) for x in re.findall(r'\d+', draft_body.split('RETURN', 1)[1])]
if sorted(int(x) for x in re.findall(r'(?<![\w.])\d+(?![\w.])', ''.join(re.findall(r'\{([^}]*)\}', draft_body)))) != list(range(1, 367)):
    sys.exit('the draft lists are not the numbers 1-366')
DRAFT = '''// The 1970 draft lottery (Selective Service System, drawn 1 Dec 1969):
// the number drawn for each birth date, in date order, Jan 1 to Dec 31
// (366 dates, Feb 29 included); 1 means called first.  Group 1 = born
// Jan-Jun (182 dates), group 2 = born Jul-Dec (184).  PowerViz's list
// (pv_Draft; AnovaLab's, after Fienberg 1971, Science 171:255), checked
// number for number by verify_PowerViz_v2.5h and again by this
// program's verify script.
LOCAL tz_Draft(tdg)
BEGIN
''' + draft_body + '''
END;

'''
rep('// ---------------- examples ----------------\n', '// ---------------- examples ----------------\n' + DRAFT)
replace_routine('tz_Example', r'''
LOCAL tz_Example(ek)
BEGIN
 LOCAL er1, er2;
 tzEX := ek;
 IF ek == 1 THEN
  // Darwin (1876), The Effects of Cross and Self Fertilisation in the
  // Vegetable Kingdom: 15 pairs of Zea mays, one plant of each pair
  // crossed and one self-fertilised, grown in the same pots; heights
  // in inches (RankLab's copy, rk_LdDarwin; 8 x the differences are
  // Fisher's 1935 figures 49, -67, 8, 16, 6, 23, 28, 41, 14, 29, 56,
  // 24, 75, 60, -48).  Dependent samples, two-tailed, alpha .05:
  // t(14) = 2.148, p = 0.0497 (SciPy).
  tzTY := 3; tzSRC := 2; tzTL := 0; tzAL := 0.05;
  tzX1 := {23.5,12,21,22,19.125,21.5,22.125,20.375,18.25,21.625,23.25,21,22.125,23,12};
  tzX2 := {17.375,20.375,20,20,18.375,18.625,18.625,15.25,16.5,18,16.25,18,12.75,15.5,18};
  tzG1 := "Crossed"; tzG2 := "Self";
  tzDV := "plant height (inches), Darwin 1876";
 END;
 IF ek == 2 THEN
  // The 1970 draft lottery (tz_Draft): were the numbers drawn at
  // random?  Births Jan-Jun against Jul-Dec; separate variances, two-
  // tailed, alpha .05: t(362.56) = 4.196 (SciPy).  The capsules for
  // the later months were put in last and not mixed well enough
  // (Fienberg 1971).
  tzTY := 2; tzSRC := 2; tzTL := 0; tzAL := 0.05;
  er1 := tz_MSN(tz_Draft(1)); er2 := tz_MSN(tz_Draft(2));
  tzM1 := er1(1); tzS1 := er1(2); tzN1 := er1(3);
  tzM2 := er2(1); tzS2 := er2(2); tzN2 := er2(3);
  tzG1 := "Born Jan-Jun"; tzG2 := "Born Jul-Dec";
  tzDV := "draft number (Selective Service, 1970)";
 END;
 IF ek == 3 THEN
  // transferred female juveniles' mean age at arrest (JDCC data, from
  // Roger's lecture note), Hispanic (sample 1) and non-Hispanic white
  // (2); pooled variances, two-tailed, alpha .05
  tzTY := 1; tzSRC := 1; tzTL := 0; tzAL := 0.05;
  tzM1 := 15.89; tzS1 := 1.45; tzN1 := 44;
  tzM2 := 16.57; tzS2 := 1.11; tzN2 := 31;
  tzG1 := "Hispanic"; tzG2 := "Non-Hispanic white";
  tzDV := "age at arrest (years), JDCC";
 END;
 IF ek == 4 THEN
  // inmate-on-staff assault rates in five matched pairs of jails
  // (Census of Jails, from Roger's lecture note), low (x1) and high (x2)
  // percentage female security staff; dependent samples, one-tailed
  // H1 mu1 < mu2, alpha .05
  tzTY := 3; tzSRC := 2; tzTL := -1; tzAL := 0.05;
  tzX1 := {1.30,1.25,0.86,0.94,2.26};
  tzX2 := {1.00,0.76,0.99,1.10,1.85};
  tzG1 := "Low % female"; tzG2 := "High % female";
  tzDV := "assault rate, Census of Jails";
 END;
END;
''')

# ---------------------------------------------------------------- 15. help
replace_routine('tz_Help', r'''
LOCAL tz_Help()
BEGIN
 tz_Frame("TTestLabG help 1/2: keys");
 TEXTOUT_P("SOFT KEYS:  1 H, 2 df, 3 crit, 4 t, 5 end = the",G1,8,30,1,tzBLUE);
 TEXTOUT_P("five steps;  Menu = the menu",G1,8,43,1,tzBLUE);
 TEXTOUT_P("Left / Right = a step back / on",G1,8,59,1,tzBLK);
 TEXTOUT_P("Enter = menu,  Esc = quit",G1,8,72,1,tzBLK);
 TEXTOUT_P("MENU: edit the numbers, tails and α, pooled or",G1,8,88,1,tzBLUE);
 TEXTOUT_P("separate side by side, choose the test, examples",G1,8,101,1,tzBLUE);
 TEXTOUT_P("The flowchart: tap Yes or No; OK = go on",G1,8,117,1,tzBLK);
 TEXTOUT_P("Your own scores: Apps, Statistics 1Var, Num:",G1,8,133,1,tzBLK);
 TEXTOUT_P("sample 1 (or x"+CHAR(8321)+") in D1, sample 2 (or x"+CHAR(8322)+") in D2",G1,8,146,1,tzBLK);
 TEXTOUT_P("A long data set: DataLoad fills D1 and D2.",G1,8,159,1,tzBLK);
 TEXTOUT_P("Teaching aid; not for clinical or legal use.",G1,8,177,1,tzRED);
 TEXTOUT_P("any key or tap = next page",G1,8,222,1,tzFOOT);
 BLIT_P(G0,0,0,G1);
 tz_WaitAny();
 tz_Frame("TTestLabG help 2/2: the numbers");
 TEXTOUT_P("t crit: exact for your df; no table is needed.",G1,8,30,1,tzBLK);
 TEXTOUT_P("A printed table: a df it lacks, the next smaller",G1,8,43,1,tzBLK);
 TEXTOUT_P("row; a fractional df, rounded down first.",G1,8,56,1,tzBLK);
 TEXTOUT_P("Step 4 keeps 4 significant digits on the way.",G1,8,72,1,tzBLK);
 TEXTOUT_P("Separate variances (the default): Welch's SE",G1,8,88,1,tzBLUE);
 TEXTOUT_P("and df, as SPSS and R print them",G1,8,101,1,tzBLUE);
 TEXTOUT_P("Group 1 minus group 2, as SPSS and R do",G1,8,117,1,tzBLK);
 TEXTOUT_P("p, two-tailed, is SPSS's "+CHAR(34)+"Sig. (2-tailed)"+CHAR(34),G1,8,133,1,tzMAG);
 TEXTOUT_P("Cohen's d: pooled s (independent); sD (pairs)",G1,8,146,1,tzMAG);
 // the Prime's own Inference app gives the same t (Tech Corner 24;
 // TestChooser points students there): a check on TTestLabG
 TEXTOUT_P("Check on the Prime: Inference app, Hyp. test,",G1,8,164,1,tzGRAY);
 TEXTOUT_P("T-Test: μ"+CHAR(8321)+"-μ"+CHAR(8322)+" (Pooled checked = pooled).  Pairs:",G1,8,177,1,tzGRAY);
 TEXTOUT_P("T-Test: 1 μ on the differences, with μ"+CHAR(8320)+" = 0.",G1,8,190,1,tzGRAY);
 TEXTOUT_P("any key or tap = back",G1,8,222,1,tzFOOT);
 BLIT_P(G0,0,0,G1);
 tz_WaitAny();
END;
''')

# ---------------------------------------------------------------- 16. the menu's examples; the start menu
rep('''  CHOOSE(mt,"Examples",{"Age at arrest (pooled)","Matched jails (dependent)","Drug use by sex (separate)"});''',
    '''  CHOOSE(mt,"Examples",{"Darwin's plants (pairs)","Draft lottery (separate)","Age at arrest (pooled)","Matched jails (pairs)"});''')
rep('''  CHOOSE(ms,"TTestLabG: t tests in 5 steps",{"Choose the test (Figure 11.2)","Example: age at arrest","Example: matched jails","Example: drug use by sex","Help"});
  tz_Settle();
  IF ms == 5 THEN tz_Help(); END;
 UNTIL ms <> 5;''', '''  CHOOSE(ms,"TTestLabG: t tests in 5 steps",{"Choose the test (flowchart)","Example: Darwin's plants","Example: draft lottery","Example: age at arrest","Example: matched jails","Help"});
  tz_Settle();
  IF ms == 6 THEN tz_Help(); END;
 UNTIL ms <> 6;''')
rep(''' IF ms >= 2 AND ms <= 4 THEN tz_Example(ms-1); END;''', ''' IF ms >= 2 AND ms <= 5 THEN tz_Example(ms-1); END;''')

# ---------------------------------------------------------------- 17a. no string names the advanced version
for ln, line in enumerate(S.split('\n'), 1):
    if not line.lstrip().startswith('//') and re.search(r'"[^"]*TTestLab(?!G)[^"]*"', line):
        sys.exit('a string still names TTestLab, line %d: %s' % (ln, line.strip()[:100]))

# ---------------------------------------------------------------- 17. nothing of the lecture left on screen
for bad in ('lecture', 'Figure 11', 'Table 11', 'tz_TabDF', 'tz_BookCell', 'tz_BookNote', 'tzTB', 'tzDFT', 'tzREJB',
            'drug use'):
    for ln, line in enumerate(S.split('\n'), 1):
        code = line.split('//', 1)[0] if '"' not in line else line
        if bad in code and not line.lstrip().startswith('//'):
            # "Roger's lecture note" appears only in comments
            sys.exit('left in code, line %d: %s' % (ln, line.strip()[:100]))

open(out_path, 'w', encoding='utf-8').write(S)
print('wrote', out_path, S.count('\n'), 'lines')
