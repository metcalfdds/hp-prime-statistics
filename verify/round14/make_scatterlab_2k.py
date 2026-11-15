# -*- coding: utf-8 -*-
"""Round 14 (14 Nov 2026): ScatterLab beta 2k from beta 2j, by exact replacements (a miss stops the build).

New in beta 2k (Roger, 14 Nov 2026: "go ahead and do the program work"; "we're featuring the Prime"; "feature Anscombe"):
  * Menu > Inference for the slope: a page with s, SE(b1), t on n - 2 df, the two-tailed p, the 95% interval for the slope
    and the decision at alpha = 0.05, each with its arithmetic (the book's Chapter 13, "Inference for the slope");
  * Menu > Bands: the 95% band for the mean of y at each x (solid) and the wider one for one new case (dotted);
  * Data > Anscombe's quartet, sets 1 to 4, all drawn in one window (x 2 to 20, y 2 to 14);
  * Home: SL_SEB, SL_T, SL_P beside the six older results;  help page 7 of 7.
Run from the repository's root:   python3 verify/round14/make_scatterlab_2k.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap
BASE = '26912a9'; DATE = '14 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r14_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/ScatterLab_beta2j.txt'], check=True, capture_output=True).stdout.decode('utf-8')

def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)

def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)

# ---- header, history ----
rep('// SCATTERLAB - beta 2j', '// SCATTERLAB - beta 2k')
note = ('Round 14 (Roger, 14 Nov 2026: "go ahead and do the program work").  New: Menu > Inference for the slope, a page '
        'with s = root(SSE/(n - 2)), SE(b1) = s/root(Sxx), t = b1/SE(b1) on n - 2 df, the two-tailed p, the 95% interval '
        'for the slope and the decision at alpha = 0.05 (slInf, slInfPage); Menu > Bands, the 95% band for the mean of y '
        '(solid) and the wider one for one new case (dotted), a pixel column at a time (slBands); Data > Anscombe\'s '
        'quartet, sets 1 to 4, all in one window (slAnsc; Anscombe 1973; the values checked against R\'s anscombe); Home '
        'gets SL_SEB, SL_T and SL_P; help page 7 of 7.  The menu has twelve items now (Quit shows as C).  Every older '
        'routine is as it was but for the lines these need: slFit calls slInf, slDraw calls slBands, the two menus, '
        'slInit, the help\'s titles and its last page.')
before('// beta 2j (9 Nov 2026):', '// beta 2k (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')
after('//   SL_R2  r-squared             SL_SSE sum of squared residuals\n',
      '//   SL_SEB the slope\'s standard error (beta 2k)\n//   SL_T   its t, on n - 2 df        SL_P   the two-tailed p\n')
after('EXPORT SL_R, SL_R2, SL_SSE;\n', 'EXPORT SL_SEB, SL_T, SL_P;\n')

# ---- state ----
after('//  slOK 1 when a line exists; slRdef 1 when r exists too\n', '''
// ---- beta 2k: inference for the slope, and the two bands (set in slInf) ----
LOCAL slBand, slIok, slSe, slSeB, slTv, slPv;
LOCAL slTc, slTcD, slCiL, slCiH;
//  slBand 1 = the two 95% bands are drawn;  slIok 1 when the slope has a
//  test (a line, and at least one point off it);  slSe the residuals'
//  standard deviation, root(SSE / (n - 2));  slSeB the slope's standard
//  error;  slTv its t;  slPv the two-tailed p;  slTc the t critical value
//  for 95% on slTcD df (kept from fit to fit: a drag refits every frame,
//  and the df changes only when a point is added or deleted);  slCiL,
//  slCiH the slope's 95% interval
''')

# ---- the arithmetic: slInf, before slGuessFit (so slFit can call it) ----
before('// The student\'s line in Guess mode: through the two handles.\n', '''// beta 2k: the slope's test and interval, from the fit's own sums:
//   s = root(SSE / (n - 2)),  SE(b1) = s / root(Sxx),  t = b1 / SE(b1) on
//   n - 2 df,  p two-tailed as twice the LOWER tail at -|t| (never 1 - CDF,
//   Lessons Learned s3),  and b1 +/- t crit x SE(b1), where t crit =
//   -STUDENT_ICDF(n - 2, 0.025).
// There is no test when there is no line, or when every point is on it
// (s = 0: t would divide by zero).  Called at the end of every slFit.
slInf()
BEGIN
  LOCAL ifD;
  slIok := 0; slSe := 0; slSeB := 0; slTv := 0; slPv := 1;
  slCiL := 0; slCiH := 0;
  IF slOK == 1 AND slN >= 3 THEN
    ifD := slN - 2;
    slSe := (MAX(0, slSSE) / ifD)^0.5;
    slSeB := slSe / slSxx^0.5;
    IF slSeB > 0 THEN
      slIok := 1;
      slTv := slB1 / slSeB;
      slPv := MIN(1, 2 * STUDENT_CDF(ifD, -ABS(slTv)));
      IF ifD <> slTcD THEN
        slTc := -STUDENT_ICDF(ifD, 0.025);
        slTcD := ifD;
      END;
      slCiL := slB1 - slTc * slSeB;
      slCiH := slB1 + slTc * slSeB;
    END;
  END;
  SL_SEB := slSeB; SL_T := slTv; SL_P := slPv;
END;

''')
rep('''  SL_R := slR; SL_R2 := slR2; SL_SSE := slSSE;
END;
''', '''  SL_R := slR; SL_R2 := slR2; SL_SSE := slSSE;
  slInf();                                       // beta 2k: the slope's test, kept up to date
END;
''')

# ---- drawing: the bands ----
before('// One whole frame, composed in G1 and shown with ONE blit, then\n', '''// beta 2k: the two 95% bands around the least-squares line, a pixel column
// at a time (Lessons Learned s6: iterate pixels, solve for x):
//   inner, solid blue: where the MEAN of y lies at x,
//          y-hat +/- t crit s root(1/n + (x - x-bar)^2 / Sxx);
//   outer, dotted orange (two columns in every four): where ONE new case
//          falls,  y-hat +/- t crit s root(1 + 1/n + (x - x-bar)^2 / Sxx).
// A row outside the plot box is left out (slPy would pin it to the edge
// and draw a false line along the frame).
slBandPt(bpP, bpV, bpC)
BEGIN
  LOCAL bpR;
  bpR := slPB - (bpV - slYlo) / (slYhi - slYlo) * (slPB - slPT);
  IF bpR >= slPT AND bpR <= slPB THEN PIXON_P(G1, bpP, IP(bpR + 0.5), bpC); END;
END;

slBands()
BEGIN
  LOCAL bdP, bdX, bdY, bdG, bdM, bdW;
  FOR bdP FROM slPL TO slPR DO
    bdX := slDx(bdP);
    bdY := slB0 + slB1 * bdX;
    bdG := 1 / slN + (bdX - slXb)^2 / slSxx;
    bdM := slTc * slSe * bdG^0.5;
    bdW := slTc * slSe * (1 + bdG)^0.5;
    slBandPt(bdP, bdY + bdM, slBLUE);
    slBandPt(bdP, bdY - bdM, slBLUE);
    IF bdP MOD 4 < 2 THEN
      slBandPt(bdP, bdY + bdW, slORNG);
      slBandPt(bdP, bdY - bdW, slORNG);
    END;
  END;
END;

''')
after('''  IF slOK == 1 AND (slMode <> 3 OR slShow == 1) THEN
    slLineW(slB0, slB1, slMAG);
  END;
''', '''  // ---- beta 2k: the two 95% bands, when they are switched on ----
  IF slBand == 1 AND slIok == 1 AND (slMode <> 3 OR slShow == 1) THEN slBands(); END;
''')

# ---- data: Anscombe's quartet ----
before('// The Data chooser (soft key Data, or Enter > Data).\n', '''// beta 2k: Anscombe's quartet (Anscombe 1973, The American Statistician
// 27, 17-21): four sets of 11 points with the same means, the same r
// (0.816) and the same least-squares line (y-hat = 3.00 + 0.500 x), and
// four different pictures.  All four are drawn in ONE window, x 2 to 20
// and y 2 to 14, so the plots can be compared.  The values are those of
// R's data set anscombe.
slAnsc(anK)
BEGIN
  LOCAL anA, anB, anI;
  anA := {10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5};
  anB := {8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68};
  IF anK == 2 THEN anB := {9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74}; END;
  IF anK == 3 THEN anB := {7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73}; END;
  IF anK == 4 THEN
    anA := {8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8};
    anB := {6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89};
  END;
  FOR anI FROM 1 TO 11 DO
    slX(anI) := anA(anI);
    slY(anI) := anB(anI);
  END;
  slN := 11; slSel := 0; slLev := 0;
  slMode := 1; slShow := 1;
  slLbl := "Anscombe (1973), set " + slCm(STRING(anK, 2, 0)) + " of 4";
  slLblC := slORNG;
  slXlo := 2; slXhi := 20; slYlo := 2; slYhi := 14;
  slXs := 2; slYs := 2;
  slSetRes();
  slFit();
  slMsg1 := "All four sets have the same r and the same line.";
  slMsg2 := "Look at the plot: what does this set show?";
  slMc1 := slORNG; slMc2 := slORNG;
END;

''')
rep('''  CHOOSE(daI, "Data", {
    "Poverty vs crime (SYNTHETIC)",
    "Load from C1, C2",
    "Save to C1, C2",
    "Clear all points"});
  IF daI == 1 THEN slExample(); END;
  IF daI == 2 THEN slLoadC(); END;
  IF daI == 3 THEN slSaveC(); END;
  IF daI == 4 THEN slClear(); END;
''', '''  CHOOSE(daI, "Data", {
    "Poverty vs crime (SYNTHETIC)",
    "Anscombe's quartet, set 1",
    "Anscombe's quartet, set 2",
    "Anscombe's quartet, set 3",
    "Anscombe's quartet, set 4",
    "Load from C1, C2",
    "Save to C1, C2",
    "Clear all points"});
  IF daI == 1 THEN slExample(); END;
  IF daI >= 2 AND daI <= 5 THEN slAnsc(daI - 1); END;   // beta 2k
  IF daI == 6 THEN slLoadC(); END;
  IF daI == 7 THEN slSaveC(); END;
  IF daI == 8 THEN slClear(); END;
''')

# ---- the inference page, after slHT ----
after('''  TEXTOUT_P(htS, G1, 12, htY, 1, htC, 296);
END;

''', '''// beta 2k: the first text when it fits a help line (294 px by slMeas),
// else the second, shorter one: a line is never cut.
slIL(ilA, ilB)
BEGIN
  IF slMeas(ilA) <= 294 THEN RETURN ilA; END;
  RETURN ilB;
END;

// beta 2k: a number for the inference page: four significant digits, with
// its commas, when that is at most 70 px wide and not already scientific;
// else the scientific form (slFitN: never a cut number).  A value below
// 0.0001 is written scientific too: slSig would print it as 0.00.
slIn(nvV)
BEGIN
  IF nvV <> 0 AND ABS(nvV) < 0.0001 THEN RETURN STRING(nvV, 3, 3); END;
  RETURN slFitN("", nvV, "", 72);
END;

// beta 2k: a p-value as text: "< 0.001" below 0.001 (never "0.000"), else
// "= " and three decimals.
slPS(psV)
BEGIN
  IF psV < 0.001 THEN RETURN "< 0.001"; END;
  RETURN "= " + slFx(psV, 3);
END;

// beta 2k: the page "Inference for the slope" (Menu).  Composed like a help
// page: the whole screen, no soft keys; any key or tap goes back to the
// plot.  Every line shows its own arithmetic when that fits the line.
slInfPage()
BEGIN
  LOCAL ipK, ipS, ipD, ipB, ipG, ipR;
  IF slOK == 0 THEN
    slMsg1 := "A slope needs 3 points with different x.";
    slMc1 := slRED;
    RETURN;
  END;
  slInf();
  ipD := slCm(STRING(slN - 2, 2, 0));
  ipB := "b" + slSUB1;
  ipG := CHAR(946) + slSUB1;
  ipR := CHAR(8730);
  DIMGROB_P(G1, 320, 240, #FFFFFFh);
  RECT_P(G1, 4, 4, 315, 235, slMAG, slLBLU);
  TEXTOUT_P("Inference for the slope", G1, 12, 8, 2, slMAG, 296);
  ipS := slYHAT + " = " + slIn(slB0);
  IF slB1 >= 0 THEN
    ipS := ipS + " + " + slIn(slB1) + " x";
  ELSE
    ipS := ipS + " - " + slIn(ABS(slB1)) + " x";
  END;
  slHT(slIL(ipS + ",  n = " + slCm(STRING(slN, 2, 0)) + ",  df = n - 2 = " + ipD, ipS), 30, #000000h);
  slHT("H" + slSUB0 + ": " + ipG + " = 0 (no straight-line relation);  H" + slSUB1 + ": " + ipG + " " + CHAR(8800) + " 0", 43, slGRAY);
  IF slIok == 0 THEN
    slHT("Every point is on the line, so the residuals have", 62, slRED);
    slHT("no spread (s = 0) and the slope has no t-test.", 75, slRED);
  ELSE
    slHT(slIL("s = " + ipR + "(SSE/(n - 2)) = " + ipR + "(" + slIn(slSSE) + "/" + ipD + ") = " + slIn(slSe), "s = " + slIn(slSe)), 62, #000000h);
    slHT(slIL("SE(" + ipB + ") = s/" + ipR + "(Sxx) = " + slIn(slSe) + "/" + ipR + "(" + slIn(slSxx) + ") = " + slIn(slSeB), "SE(" + ipB + ") = " + slIn(slSeB)), 75, #000000h);
    slHT(slIL("t = " + ipB + "/SE(" + ipB + ") = " + slIn(slB1) + "/" + slIn(slSeB) + " = " + slIn(slTv), "t = " + slIn(slTv)), 91, slMAG);
    slHT("p " + slPS(slPv) + " (two-tailed, df = " + ipD + ")", 104, slMAG);
    slHT(slIL("95% interval for " + ipG + ": " + slIn(slCiL) + " to " + slIn(slCiH), slIn(slCiL) + " to " + slIn(slCiH)), 120, #000000h);
    slHT("(" + ipB + " " + CHAR(177) + " t crit " + CHAR(215) + " SE(" + ipB + "), with t crit = " + slFx(slTc, 3) + ")", 133, slGRAY);
    IF slPv < 0.05 THEN
      slHT("p < " + CHAR(945) + " = 0.05: reject H" + slSUB0 + ".  The interval leaves 0 out.", 149, slRED);
    ELSE
      slHT("p " + CHAR(8805) + " " + CHAR(945) + " = 0.05: do not reject H" + slSUB0 + ".  The interval holds 0.", 149, slBLUE);
    END;
    // a p that rounds to alpha at three decimals gets its 4 significant
    // digits beside the decision (Lessons Learned s13)
    IF slPv >= 0.0495 AND slPv < 0.0505 THEN
      IF slPv < 0.05 THEN
        slHT("(p = " + slFx(slPv, 5) + ": just below " + CHAR(945) + " = 0.050.)", 162, slGRAY);
      ELSE
        slHT("(p = " + slFx(slPv, 5) + ": just above " + CHAR(945) + " = 0.050.)", 162, slGRAY);
      END;
    END;
    slHT("s is the typical miss of a point from the line.", 181, slGRAY);
    slHT("The test of " + CHAR(961) + " = 0 gives the same t and p.", 194, slGRAY);
  END;
  TEXTOUT_P("any key or tap = back to the plot", G1, 12, 218, 1, slFOOT, 296);
  BLIT_P(G0, 0, 0, G1);
  ipK := slWaitAny();
END;

''')

# ---- help: seven pages ----
rep('// HELP: six drawn pages (a MSGBOX shows only about five lines)', '// HELP: seven drawn pages (a MSGBOX shows only about five lines)')
for i, t in enumerate(['What r measures', None, 'Residuals, least squares', 'Leverage', 'Correlation, not causation', 'Touch, keys, 2Var'], 1):
    if t: rep('"ScatterLab help %d/6: %s"' % (i, t), '"ScatterLab help %d/7: %s"' % (i, t))
rep('"ScatterLab help 2/6: " + "r"', '"ScatterLab help 2/7: " + "r"')
rep('''    slHT("Home after Quit: SL_N, SL_B0, SL_B1,", 169, slGRAY);
    slHT("SL_R, SL_R2, SL_SSE (kept up to date).", 182, slGRAY);
    slHT("Tap the equation: least squares as calculus.", 198, slMAG);
  END;
''', '''    slHT("Home after Quit: SL_N, SL_B0, SL_B1, SL_R,", 169, slGRAY);
    slHT("SL_R2, SL_SSE, SL_SEB, SL_T, SL_P (kept up to date).", 182, slGRAY);
    slHT("Tap the equation: least squares as calculus.", 198, slMAG);
  END;
  IF hgP == 7 THEN
    TEXTOUT_P("ScatterLab help 7/7: Testing the slope", G1, 12, 8, 2, slBLUE, 296);
    slHT("The points are a sample.  Would another sample", 30, #000000h);
    slHT("give a slope this far from 0?  Menu > Inference", 43, #000000h);
    slHT("for the slope answers with a t-test:", 56, #000000h);
    slHT("  s = " + CHAR(8730) + "(SSE / (n - 2)), the typical miss", 72, slMAG);
    slHT("  SE(b" + slSUB1 + ") = s / " + CHAR(8730) + "(Sxx),   t = b" + slSUB1 + " / SE(b" + slSUB1 + ")", 85, slMAG);
    slHT("  df = n - 2;  H" + slSUB0 + ": " + CHAR(946) + slSUB1 + " = 0;  p is two-tailed", 98, slMAG);
    slHT("The 95% interval is b" + slSUB1 + " " + CHAR(177) + " t crit " + CHAR(215) + " SE(b" + slSUB1 + ").", 114, #000000h);
    slHT("Menu > Bands draws two 95% bands around the line:", 130, slORNG);
    slHT("  inner, solid: where the MEAN of y lies at each x", 143, slORNG);
    slHT("  outer, dotted: where ONE new case would fall", 156, slORNG);
    slHT("Data > Anscombe's quartet: four sets of points", 172, slGRN);
    slHT("with the same r and the same line, and four very", 185, slGRN);
    slHT("different plots.  Always look at the plot.", 198, slGRN);
  END;
''')
rep('  hpN := 6; hpP := 1;', '  hpN := 7; hpP := 1;')

# ---- the menu ----
rep('''    "Least squares as calculus",
    "Data: example, C1/C2, clear",
    "Type a point (x, y)",''', '''    "Least squares as calculus",
    "Inference for the slope",
    "Bands: mean and new case",
    "Data: examples, C1/C2, clear",
    "Type a point (x, y)",''')
rep('''  IF muI == 5 THEN slCxPage(); END;              // beta 2: the CAS page
  IF muI == 6 THEN slData(); END;
  IF muI == 7 THEN slTypePt(); END;
  IF muI == 8 THEN
''', '''  IF muI == 5 THEN slCxPage(); END;              // beta 2: the CAS page
  IF muI == 6 THEN slInfPage(); END;             // beta 2k: the slope's test
  IF muI == 7 THEN                               // beta 2k: the two bands on / off
    IF slOK == 0 THEN
      slMsg1 := "Bands need a line: 3 points with different x.";
      slMc1 := slRED;
    ELSE
      IF slIok == 0 THEN
        slMsg1 := "Every point is on the line: no bands to draw.";
        slMc1 := slRED;
      ELSE
        slBand := 1 - slBand;
        IF slBand == 1 THEN
          slMsg1 := "Solid blue: where the MEAN of y lies (95%).";
          slMsg2 := "Dotted orange: where ONE new case falls (95%).";
          slMc1 := slBLUE; slMc2 := slORNG;
        END;
      END;
    END;
  END;
  IF muI == 8 THEN slData(); END;
  IF muI == 9 THEN slTypePt(); END;
  IF muI == 10 THEN
''')
rep('''  IF muI == 9 THEN slHelp(); END;
  IF muI == 10 THEN RETURN 0; END;               // Quit (the Prime shows it as A)
''', '''  IF muI == 11 THEN slHelp(); END;
  IF muI == 12 THEN RETURN 0; END;               // Quit (the Prime shows it as C)
''')

# ---- start-up ----
after('''  slCasOK := 0; slCasMx := 4000; slCxK := ""; slCxSt := 0; slCxNt := "";
  slCxE := ""; slCxA := ""; slCxB := ""; slCxSa := ""; slCxSb := "";
''', '''  // beta 2k: the bands are off, and no t critical value is kept yet
  slBand := 0; slTc := 0; slTcD := 0;
''')

# every version string in a literal (as Rounds 11 and 12 did)
s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace('beta 2j', 'beta 2k').replace('beta2j', 'beta2k'), s)
os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'ScatterLab_beta2k.txt'), 'w', encoding='utf-8', newline='').write(s)
print('ScatterLab beta2j -> beta2k: %d lines' % s.count('\n'))
