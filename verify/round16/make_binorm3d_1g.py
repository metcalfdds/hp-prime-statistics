# -*- coding: utf-8 -*-
"""Round 16 (15 Nov 2026): BiNorm3D beta 1g from beta 1f, by exact replacements (a miss stops the build).

New in beta 1g (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please"; this is the sixth):
  * A THIRD VIEW, THE TARGET.  Soft key 3 now goes 3-D -> Cont -> CEP -> 3-D.  The target view shows the pattern of
    (x, y) pairs from above with the circle round the mean that holds half of them.  Its radius is the CEP, the circular
    error probable.  Beside it is the ellipse that holds half as well, and shots can be fired at the target (the Shots
    key or a tap on the plot, 50 at a time, 500 at most) and counted inside the circle.
  * THE ARITHMETIC, one routine (bnCepC).  Along the ridge the pairs have variance A = 1 + |rho| and across it
    B = 1 - |rho|.  In polar form round the mean
        P(R) = (2 / (pi root(A B))) INT_0^(pi/2) (1 - exp(-R^2 g(t))) / (2 g(t)) dt,  g(t) = cos^2 t/(2A) + sin^2 t/(2B),
    by the midpoint rule at 16 angles, and R solves P(R) = 1/2 by Newton's rule.  Written from the formula; no other
    program was read for it (the library in D:\\HP-Prime holds no program that computes a CEP: searched 15 Nov 2026).
  * Help: six pages (page 5 is new, The target and the CEP; the keys page is 6/6); the opening page names the new view.
  * Home: BN_CEP holds the CEP once the target view has been opened (0 until then); the closing line names it then.
Every other screen is beta 1f's, apart from the label of soft key 3 in the contour view ("CEP" where it said "3-D").
Run from the repository's root:   python3 verify/round16/make_binorm3d_1g.py OUTDIR
"""
import io, os, subprocess, sys, textwrap
BASE = '4e8ff66'; DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r16_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/BiNorm3D_beta1f.txt'], check=True, capture_output=True).stdout.decode('utf-8')


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)


def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)


# ---------------- header ----------------
rep('// BINORM3D - beta 1f\n', '// BINORM3D - beta 1g\n')
rep('''// The bivariate normal surface, turned with a finger:
//   correlation and regression to the mean
''', '''// The bivariate normal surface, turned with a finger:
//   correlation, regression to the mean, and the CEP circle
''')
note = ('Round 16 (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please").  A third view, the '
        'TARGET: the pattern of (x, y) pairs from above with the circle round the mean that holds half of them.  Its '
        'radius is the CEP, the circular error probable.  Soft key 3 now goes 3-D, Cont, CEP and back to 3-D.  The view '
        'also draws the ellipse that holds half, fires shots at the target (Shots, or a tap on the plot: 50 at a time, '
        '500 at most) and counts those inside the circle.  One new routine does the arithmetic, bnCepC: the share of '
        'pairs inside a circle of radius R as an integral over the angle (16 midpoints across a quarter turn), and '
        'Newton\'s rule for the R that holds half.  Written from the formula; the library in D:\\HP-Prime holds no '
        'program that computes a CEP (searched 15 Nov 2026).  Help has six pages (5 is new; the keys are 6/6).  BN_CEP '
        'holds the CEP once the view has been opened.  Every other screen is beta 1f\'s, apart from the label of soft '
        'key 3 in the contour view ("CEP" where it said "3-D").')
before('// beta 1f (9 Nov 2026):', '// beta 1g (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')

after('''//     red on the surface, its top marked above the regression line.
''', '''//   Target view (CEP; beta 1g): the pattern from above as a target.
//     The green circle round the mean holds half of all (x, y) pairs;
//     its radius R is the CEP, the circular error probable.  The blue
//     ellipse holds half as well, in less area.  Shots fires 50 random
//     pairs at the target and counts those inside the circle.
''')
after('''//     on the screen at every tilt.
''', '''//   The CEP (beta 1g; bnCepC, checked against a second integral and a
//   simulation, verify_BiNorm3D_beta1g.py): with A = 1 + |rho| the
//   variance along the ridge and B = 1 - |rho| across it,
//     P(R) = (2 / (pi (A B)^0.5)) INT_0^(pi/2) (1 - exp(-R^2 g)) / (2 g) dt,
//     g = cos^2 t / (2 A) + sin^2 t / (2 B);  the CEP is the R with
//     P(R) = 1/2.  At rho = 0 it is (2 ln 2)^0.5 = 1.1774.
//   The ellipse Q = 2 ln 2 holds half too (1 - exp(-Q/2) = 1/2).
''')
rep('''//   Soft keys: rho- rho+ (also the - and + keys) | Cont (3-D) |
//     Slice | Reset (theta 35, phi 30, rho 0.60) | Menu (also Enter)
''', '''//   Target view (beta 1g): Shots, or a tap on the plot = 50 more
//     shots; Clear removes them.
//   Soft keys: rho- rho+ (also the - and + keys) | Cont, CEP, 3-D
//     (the next view) | Slice | Reset (theta 35, phi 30, rho 0.60) |
//     Menu (also Enter).  In the target view keys 4 and 5 are Shots
//     and Clear.
''')
rep('''//   BN_RHO  the last rho
''', '''//   BN_RHO  the last rho
//   BN_CEP  the CEP for that rho, once the target view has been
//           opened in the run (0 if it never was)
''')
rep('''//   the projection; the 3-D view; the contour view and slice
//   panel; dragging; setting rho and x0; menu, timing, help;
//   init and main.
''', '''//   the projection; the 3-D view; the contour view and slice
//   panel; the target view and the CEP (beta 1g); dragging; setting
//   rho and x0; menu, timing, help; init and main.
''')

# ---------------- state ----------------
rep('EXPORT BN_RHO;\n', 'EXPORT BN_RHO, BN_CEP;\n')
rep('''//  bnView 1 = the 3-D surface, 2 = the contour view from above
''', '''//  bnView 1 = the 3-D surface, 2 = the contour view from above,
//         3 = the target view with the CEP circle (beta 1g)
''')
before('''// ---- one frame of the 3-D view (set by bnFrame and bnDraw3D) ----
''', '''// ---- beta 1g: the target view and the CEP ----
LOCAL bnCpR, bnCpD, bnCpK, bnQC, bnQS, bnTEX;
LOCAL bnTEY, bnShX, bnShY, bnShI, bnShN, bnShIn;
LOCAL bnTgt;
//  bnCpR  the CEP: the radius of the circle round the mean that
//         holds half of all (x, y) pairs (bnCepC)
//  bnCpD  1 = rho has changed since bnCpR was worked out
//  bnCpK  how many Newton steps the last bnCepC took
//  bnQC, bnQS  cos^2 t and sin^2 t at 16 angles across a quarter turn
//  bnTEX, bnTEY  the ellipse that holds half, in pixels: 61 points
//  bnShX, bnShY  the shots fired, in pixels (x = 0: off the plot);
//         bnShI 1 = that shot is inside the circle
//  bnShN  how many shots have been fired; bnShIn how many are inside
//  bnTgt  1 once the target view has been opened in this run

''')

# ---------------- the soft keys ----------------
rep('''  IF bnView == 1 THEN
    DRAWMENU({bnRS + bnMin, bnRS + "+", "Cont", "Slice", "Reset", "Menu"});
  ELSE
    DRAWMENU({bnRS + bnMin, bnRS + "+", "3-D", "Slice", "Reset", "Menu"});
  END;
''', '''  // beta 1g: key 3 names the NEXT view (3-D, Cont, CEP, 3-D ...); in
  // the target view keys 4 and 5 fire the shots and clear them
  IF bnView == 1 THEN
    DRAWMENU({bnRS + bnMin, bnRS + "+", "Cont", "Slice", "Reset", "Menu"});
  END;
  IF bnView == 2 THEN
    DRAWMENU({bnRS + bnMin, bnRS + "+", "CEP", "Slice", "Reset", "Menu"});
  END;
  IF bnView == 3 THEN
    DRAWMENU({bnRS + bnMin, bnRS + "+", "3-D", "Shots", "Clear", "Menu"});
  END;
''')

# ---------------- the new view: arithmetic, shots, drawing ----------------
before('''// Draw whichever view is current.
bnShow()
''', r'''// ------------------------------------------------------------
// beta 1g.  THE TARGET VIEW AND THE CEP.
//
// bnCepC: the CEP (circular error probable), the radius R of the
// circle round the mean that holds half of all (x, y) pairs.
//   Along the ridge the pairs have variance A = 1 + |rho|, across it
//   B = 1 - |rho|, and the two directions are uncorrelated.  In polar
//   form round the mean the share inside radius R is
//     P(R) = (2 / (pi (A B)^0.5))
//            INT_0^(pi/2) (1 - exp(-R^2 g(t))) / (2 g(t)) dt,
//     g(t) = cos^2 t / (2 A) + sin^2 t / (2 B).
//   The integrand is smooth and periodic, so the midpoint rule at 16
//   angles gives P to 10 digits or better for every rho from -0.9
//   to 0.9 (verify_BiNorm3D_beta1g.py).  Every term is positive, and
//   R^2 g is at least 0.2, so 1 - exp(...) loses no digits.
//   R solves P(R) = 1/2 by Newton's rule, with
//     P'(R) = (2 R / (pi (A B)^0.5)) INT_0^(pi/2) exp(-R^2 g(t)) dt,
//   from R = (2 ln 2)^0.5 (A B)^0.25: its value for a round pattern
//   of the same area.  The steps are counted (30 at most; it takes
//   3 to 6).  At rho = 0, R = (2 ln 2)^0.5 = 1.1774.
// It also sets the ellipse Q = 2 ln 2, which holds half as well
// (1 - exp(-Q / 2) = 1/2), drawn as bnCache draws its two, and it
// removes the shots: they were fired at the old rho.
// ------------------------------------------------------------
bnCepC()
BEGIN
  LOCAL cpA, cpB, cpR, cpI, cpN, cpP;
  LOCAL cpD, cpE, cpG, cpC, cpS, cpK;
  LOCAL cpU, cpV;
  cpA := 1 + ABS(bnRho); cpB := 1 - ABS(bnRho);
  cpC := 1 / (16 * (cpA * cpB)^0.5);
  cpR := (2 * LN(2))^0.5 * (cpA * cpB)^0.25;
  cpN := 0;
  REPEAT
    cpP := 0; cpD := 0;
    FOR cpI FROM 1 TO 16 DO
      cpG := bnQC(cpI) / (2 * cpA) + bnQS(cpI) / (2 * cpB);
      cpE := EXP(-cpR * cpR * cpG);
      cpP := cpP + (1 - cpE) / (2 * cpG);
      cpD := cpD + cpE;
    END;
    cpP := cpC * cpP;
    cpD := cpC * cpR * cpD;
    cpS := (cpP - 0.5) / cpD;
    // never step to zero or below: halve instead
    IF cpS >= cpR THEN cpS := cpR / 2; END;
    cpR := cpR - cpS;
    cpN := cpN + 1;
  UNTIL ABS(cpS) < 1E-10 OR cpN >= 30;
  bnCpR := cpR; bnCpK := cpN; bnCpD := 0;
  BN_CEP := cpR;
  // the ellipse that holds half: Q = 2 ln 2, so k = (2 ln 2)^0.5
  cpK := (2 * LN(2))^0.5;
  cpU := (1 + bnRho)^0.5 / 2^0.5;
  cpV := (1 - bnRho)^0.5 / 2^0.5;
  FOR cpI FROM 1 TO 61 DO
    bnTEX(cpI) := IP(bnCXc + bnCU * cpK * (cpU * bnCos(cpI) + cpV * bnSin(cpI)) + 0.5);
    bnTEY(cpI) := IP(bnCYc - bnCU * cpK * (cpU * bnCos(cpI) - cpV * bnSin(cpI)) + 0.5);
  END;
  bnShN := 0; bnShIn := 0;
END;

// Fire shN more shots at the target: pairs (x, y) of N(0, 1) values
// with correlation rho, x = z1, y = rho z1 + (1 - rho^2)^0.5 z2.  The
// two normals come from Marsaglia's polar method (as CICatcher's
// samples do): no sine or cosine, so the angle setting cannot spoil
// them.  A shot is inside the circle when x^2 + y^2 <= R^2.  500
// shots at most; a shot that lands off the plot is counted, not drawn.
// Returns 1 if any were fired.
bnShots(shN)
BEGIN
  LOCAL shI, shU, shV, shW, shF, shX;
  LOCAL shY, shC, shQ, shPx, shPy;
  IF bnShN >= 500 THEN
    bnMsg := "500 shots is the most: Clear starts again";
    RETURN 0;
  END;
  shC := (1 - bnRho^2)^0.5;
  shQ := bnCpR * bnCpR;
  FOR shI FROM 1 TO shN DO
    IF bnShN < 500 THEN
      REPEAT
        shU := 2 * RANDOM - 1;
        shV := 2 * RANDOM - 1;
        shW := shU * shU + shV * shV;
      UNTIL shW > 0 AND shW < 1;
      shF := (-2 * LN(shW) / shW)^0.5;
      shX := shU * shF;
      shY := bnRho * shX + shC * shV * shF;
      bnShN := bnShN + 1;
      shPx := IP(bnCXc + bnCU * shX + 0.5);
      shPy := IP(bnCYc - bnCU * shY + 0.5);
      IF shPx <= bnCL OR shPx >= bnCR - 1 OR shPy <= bnCT OR shPy >= bnCB - 1 THEN shPx := 0; END;
      bnShX(bnShN) := shPx;
      bnShY(bnShN) := shPy;
      bnShI(bnShN) := 0;
      IF shX * shX + shY * shY <= shQ THEN
        bnShI(bnShN) := 1;
        bnShIn := bnShIn + 1;
      END;
    END;
  END;
  RETURN 1;
END;

// The target's grid, tick labels at -3 .. 3, axes and frame (the
// contour view's, drawn here for the target view).
bnTgGrid()
BEGIN
  LOCAL tgI, tgX, tgY, tgS;
  FOR tgI FROM 0 TO 6 DO
    tgX := bnCL + tgI * bnCU;
    tgY := bnCT + tgI * bnCU;
    LINE_P(G1, tgX, bnCT, tgX, bnCB, bnGRID);
    LINE_P(G1, bnCL, tgY, bnCR, tgY, bnGRID);
    tgS := bnCm(STRING(tgI - 3, 2, 0));
    TEXTOUT_P(tgS, G1, tgX - IP(3 * DIM(tgS)), bnCB + 2, 1, bnGRAY, 16);
    tgS := bnCm(STRING(3 - tgI, 2, 0));
    TEXTOUT_P(tgS, G1, 2, tgY - 5, 1, bnGRAY, 18);
  END;
  LINE_P(G1, bnCL, bnCYc, bnCR, bnCYc, bnFLR);
  LINE_P(G1, bnCXc, bnCT, bnCXc, bnCB, bnFLR);
  LINE_P(G1, bnCL, bnCT, bnCR, bnCT, bnGRAY);
  LINE_P(G1, bnCR, bnCT, bnCR, bnCB, bnGRAY);
  LINE_P(G1, bnCR, bnCB, bnCL, bnCB, bnGRAY);
  LINE_P(G1, bnCL, bnCB, bnCL, bnCT, bnGRAY);
  TEXTOUT_P("x", G1, bnCR - 8, bnCYc + 2, 1, bnGRAY, 8);
  TEXTOUT_P("y", G1, bnCXc + 4, bnCT + 1, 1, bnGRAY, 8);
END;

// THE TARGET VIEW: the pattern from above as a target.  The shots
// (green inside the circle, orange outside), the ellipse that holds
// half (blue), the CEP circle (green, two lines thick), and beside
// the plot what they are and the count.  One frame in G1, one blit.
bnDrawT()
BEGIN
  LOCAL dtI, dtR, dtS, dtC, dtX1, dtY1;
  LOCAL dtX2, dtY2, dtM;
  IF bnCpD == 1 THEN bnCepC(); END;
  DIMGROB_P(G1, 320, 240, #FFFFFFh);
  TEXTOUT_P("Target: CEP, " + bnRS + " = " + bnCm(bnF(bnRho, 2)), G1, 22, 2, 1, bnBLUE, 170);
  bnTgGrid();
  // ---- the shots: 2 x 2 dots ----
  FOR dtI FROM 1 TO bnShN DO
    IF bnShX(dtI) > 0 THEN
      dtC := bnORNG;
      IF bnShI(dtI) == 1 THEN dtC := bnGRN; END;
      RECT_P(G1, bnShX(dtI), bnShY(dtI), bnShX(dtI) + 1, bnShY(dtI) + 1, dtC);
    END;
  END;
  // ---- the ellipse that holds half, from bnCepC ----
  FOR dtI FROM 1 TO 60 DO
    LINE_P(G1, bnTEX(dtI), bnTEY(dtI), bnTEX(dtI + 1), bnTEY(dtI + 1), bnBLUE);
  END;
  // ---- the CEP circle, radius R and R + 1 px: two lines thick ----
  FOR dtM FROM 0 TO 1 DO
    dtR := bnCpR * bnCU + dtM;
    FOR dtI FROM 1 TO 60 DO
      dtX1 := IP(bnCXc + dtR * bnCos(dtI) + 0.5);
      dtY1 := IP(bnCYc - dtR * bnSin(dtI) + 0.5);
      dtX2 := IP(bnCXc + dtR * bnCos(dtI + 1) + 0.5);
      dtY2 := IP(bnCYc - dtR * bnSin(dtI + 1) + 0.5);
      LINE_P(G1, dtX1, dtY1, dtX2, dtY2, bnGRN);
    END;
  END;
  // ---- beside the plot: what the two curves are, and the count ----
  TEXTOUT_P("Green circle: holds", G1, 198, 22, 1, bnGRN, 118);
  TEXTOUT_P("half of all (x, y)", G1, 198, 34, 1, bnGRN, 118);
  TEXTOUT_P("pairs.  Its radius", G1, 198, 46, 1, bnGRN, 118);
  TEXTOUT_P("is the CEP:", G1, 198, 58, 1, bnGRN, 118);
  TEXTOUT_P("R = " + bnCm(bnF(bnCpR, 3)), G1, 198, 72, 2, bnGRN, 118);
  TEXTOUT_P("Blue ellipse: half", G1, 198, 94, 1, bnBLUE, 118);
  TEXTOUT_P("too, in less area.", G1, 198, 106, 1, bnBLUE, 118);
  IF bnShN > 0 THEN
    TEXTOUT_P("Shots: " + bnCm(STRING(bnShN, 2, 0)), G1, 198, 126, 1, #000000h, 118);
    dtS := "inside: " + bnCm(STRING(bnShIn, 2, 0)) + " (" + bnCm(STRING(ROUND(100 * bnShIn / bnShN, 0), 2, 0)) + " %)";
    TEXTOUT_P(dtS, G1, 198, 138, 1, #000000h, 118);
  ELSE
    TEXTOUT_P("No shots yet.", G1, 198, 126, 1, bnGRAY, 118);
  END;
  TEXTOUT_P("Shots, or a tap on", G1, 198, 158, 1, bnRED, 118);
  TEXTOUT_P("the plot: 50 more", G1, 198, 170, 1, bnRED, 118);
  // ---- the two lines under the plot ----
  TEXTOUT_P("CEP: the circular error probable, the 50 % circle", G1, 4, 194, 1, #000000h, 312);
  IF DIM(bnMsg) > 0 THEN
    TEXTOUT_P(bnMsg, G1, 4, 206, 1, bnRED, 312);
  ELSE
    IF ABS(bnRho) < 0.001 THEN
      TEXTOUT_P(bnRS + " = 0: a round pattern; the circle is the ellipse", G1, 4, 206, 1, bnMAG, 312);
    ELSE
      dtS := bnCm(bnF(((1 + ABS(bnRho)) / (1 - ABS(bnRho)))^0.5, 2));
      TEXTOUT_P("Pattern " + dtS + " times as long as wide.  At " + bnRS + " = 0, R = 1.177", G1, 4, 206, 1, bnGRAY, 312);
    END;
  END;
  BLIT_P(G0, 0, 0, G1);
  bnMenuBar();
END;

// A tap in the target view: on the plot it fires 50 more shots.
bnTgTap(ttX, ttY)
BEGIN
  IF ttX >= bnCL AND ttX <= bnCR AND ttY >= bnCT AND ttY <= bnCB THEN
    IF bnCpD == 1 THEN bnCepC(); END;
    bnShots(50);
  END;
  bnDrain();
  RETURN 0;
END;

// The next view: 3-D, Cont, CEP and round again.
bnNextV()
BEGIN
  bnView := bnView + 1;
  IF bnView > 3 THEN bnView := 1; END;
  IF bnView == 3 THEN bnTgt := 1; END;
END;

''')
rep('''  IF bnView == 1 THEN bnDraw3D(); ELSE bnDrawC(); END;
END;
''', '''  IF bnView == 1 THEN bnDraw3D(); END;
  IF bnView == 2 THEN bnDrawC(); END;
  IF bnView == 3 THEN bnDrawT(); END;
END;
''')

# ---------------- a new rho: the CEP is stale ----------------
rep('''  IF srN <> bnRho THEN
    bnRho := srN;
    bnCache();
  END;
''', '''  IF srN <> bnRho THEN
    bnRho := srN;
    bnCache();
    bnCpD := 1;                        // beta 1g: the CEP is for the old rho
  END;
''')

# ---------------- the menu ----------------
rep('''  muS1 := "Contour view (from above)";
  IF bnView == 2 THEN muS1 := "3-D view"; END;
''', '''  // beta 1g: item 2 names the next of the three views
  muS1 := "Contour view (from above)";
  IF bnView == 2 THEN muS1 := "Target view (CEP circle)"; END;
  IF bnView == 3 THEN muS1 := "3-D view"; END;
''')
rep('''  IF muI == 2 THEN bnView := 3 - bnView; END;
''', '''  IF muI == 2 THEN bnNextV(); END;
''')

# ---------------- help: six pages ----------------
for n in (1, 2, 3, 4):
    rep('bnPage("BiNorm3D help %d/5: ' % n, 'bnPage("BiNorm3D help %d/6: ' % n)
    rep('hpK := bnPgEnd("%d/5, tap or key = next page, Esc = back");' % n, 'hpK := bnPgEnd("%d/6, tap or key = next page, Esc = back");' % n)
rep('''  // ---- 5: keys and touch ----
  bnPage("BiNorm3D help 5/5: Keys and touch", bnORNG, bnLORN);
  bnLn("Drag sideways to turn the surface; drag down to look at it from", 32, #000000h);
  bnLn("higher up.", 45, #000000h);
  bnLn("Arrows: Left and Right turn it; Up and Down look from higher or", 58, #000000h);
  bnLn("lower; 10" + bnDg + " a press.", 71, #000000h);
  bnLn(bnRS + bnMin + " " + bnRS + "+ (or the " + bnMin + " and + keys): " + bnRS + " by 0.1.", 84, #000000h);
  bnLn("Cont: the view from above; 3-D goes back.", 97, #000000h);
  bnLn("Slice: on or off.  From above, tap or drag the plot (or Left, Right)", 110, #000000h);
  bnLn("to move " + bnX0S + ".", 123, #000000h);
  bnLn("Reset: " + bnTS + " = 35" + bnDg + ", " + bnFS + " = 30" + bnDg + ", " + bnRS + " = 0.60.", 136, #000000h);
  bnLn("Menu (Enter): set " + bnRS + " exactly, the views, the slice, reset, the grid", 153, bnGRAY);
  bnLn("while dragging, frame timing, help, quit.  Esc = quit.", 166, bnGRAY);
  bnLn("A drag draws an 11" + CHAR(215) + "11 grid, 15" + CHAR(215) + "15 on lifting.", 183, bnGRAY);
  bnLn("Home after a run: BN_RHO holds " + bnRS + ".", 200, bnGRN);
  bnPgEnd("5/5, tap or key = back to the surface");
''', '''  // ---- 5: the target and the CEP (beta 1g) ----
  bnPage("BiNorm3D help 5/6: The target and the CEP", bnGRN, bnLGRN);
  bnLn("CEP shows the pattern from above as a target.  Think of each", 32, #000000h);
  bnLn("(x, y) pair as a shot aimed at the center.", 45, #000000h);
  bnLn("The green circle holds half of all the shots.  Its radius R is the", 62, bnGRN);
  bnLn("CEP, the circular error probable: a shot is as likely to land", 75, bnGRN);
  bnLn("inside the circle as outside it.  R is in SDs of X (or of Y).", 88, bnGRN);
  bnLn(bnRS + " = 0: the pattern is round and R = 1.177.  As " + bnRS + " moves away", 105, bnMAG);
  bnLn("from 0 the pattern grows longer and narrower, and R shrinks:", 118, bnMAG);
  bnLn("@R06@ at " + bnRS + " = 0.6 and @R09@ at " + bnRS + " = 0.9.", 131, bnMAG);
  bnLn("The blue ellipse holds half of the shots too.  It has the", 148, bnBLUE);
  bnLn("pattern's own shape, so it covers less area than the circle.", 161, bnBLUE);
  bnLn("Shots, or a tap on the plot, fires 50 shots and counts those", 178, bnGRAY);
  bnLn("inside the circle: about half.  Clear removes the shots.", 191, bnGRAY);
  hpK := bnPgEnd("5/6, tap or key = next page, Esc = back");
  IF hpK == 4 THEN RETURN; END;
  // ---- 6: keys and touch ----
  bnPage("BiNorm3D help 6/6: Keys and touch", bnORNG, bnLORN);
  bnLn("Drag sideways to turn the surface; drag down to look at it from", 32, #000000h);
  bnLn("higher up.", 45, #000000h);
  bnLn("Arrows: Left and Right turn it; Up and Down look from higher or", 58, #000000h);
  bnLn("lower; 10" + bnDg + " a press.", 71, #000000h);
  bnLn(bnRS + bnMin + " " + bnRS + "+ (or the " + bnMin + " and + keys): " + bnRS + " by 0.1.", 84, #000000h);
  bnLn("Cont: the view from above; CEP: the target; 3-D: the surface.", 97, #000000h);
  bnLn("Slice: on or off.  From above, tap or drag the plot (or Left, Right)", 110, #000000h);
  bnLn("to move " + bnX0S + ".", 123, #000000h);
  bnLn("Target: Shots (or a tap) fires 50 shots; Clear removes them.", 136, #000000h);
  bnLn("Reset: " + bnTS + " = 35" + bnDg + ", " + bnFS + " = 30" + bnDg + ", " + bnRS + " = 0.60.", 149, #000000h);
  bnLn("Menu (Enter): set " + bnRS + " exactly, the views, the slice, reset, the grid", 162, bnGRAY);
  bnLn("while dragging, frame timing, help, quit.  Esc = quit.", 175, bnGRAY);
  bnLn("A drag draws an 11" + CHAR(215) + "11 grid, 15" + CHAR(215) + "15 on lifting.", 188, bnGRAY);
  bnLn("Home after a run: BN_RHO holds " + bnRS + "; BN_CEP the CEP if shown.", 201, bnGRN);
  bnPgEnd("6/6, tap or key = back to the surface");
''')
rep('''// HELP: five drawn pages.  Any key or tap turns the page; Esc
''', '''// HELP: six drawn pages.  Any key or tap turns the page; Esc
''')

# ---------------- init ----------------
before('''  // ---- the starting state ----
  bnView := 1; bnSlc := 0; bnDrag := 0; bnCrs := 1; bnMsg := "";
''', '''  // ---- beta 1g: cos^2 t and sin^2 t at the 16 midpoints of a
  //      quarter turn (the CEP's integral), room for the ellipse that
  //      holds half and for 500 shots ----
  bnQC := MAKELIST(0, ivI, 1, 16); bnQS := MAKELIST(0, ivI, 1, 16);
  FOR ivI FROM 1 TO 16 DO
    ivT := (ivI - 0.5) * bnPI / 32;
    bnQC(ivI) := COS(ivT * bnAU)^2;
    bnQS(ivI) := SIN(ivT * bnAU)^2;
  END;
  bnTEX := MAKELIST(0, ivI, 1, 61); bnTEY := MAKELIST(0, ivI, 1, 61);
  bnShX := MAKELIST(0, ivI, 1, 500); bnShY := MAKELIST(0, ivI, 1, 500);
  bnShI := MAKELIST(0, ivI, 1, 500);
  bnShN := 0; bnShIn := 0; bnCpR := 0; bnCpK := 0; bnCpD := 1; bnTgt := 0;
  BN_CEP := 0;
''')

# ---------------- the opening page ----------------
rep('''  TEXTOUT_P("Enter: menu, with five pages of help.", G1, 14, 167, 1, bnGRAY, 292);
''', '''  TEXTOUT_P("CEP: the pattern as a target, with the circle", G1, 14, 167, 1, bnBLUE, 292);
  TEXTOUT_P("that holds half of the shots.", G1, 14, 180, 1, bnBLUE, 292);
  TEXTOUT_P("Enter: menu, with six pages of help.", G1, 14, 197, 1, bnGRAY, 292);
''')

# ---------------- main ----------------
rep('''    // mnAct: 1 rho down, 2 rho up, 3 Cont / 3-D, 4 Slice, 5 Reset,
    // 6 Menu; 0 nothing
''', '''    // mnAct: 1 rho down, 2 rho up, 3 the next view, 4 Slice (Shots in
    // the target view), 5 Reset (Clear there), 6 Menu; 0 nothing
''')
rep('''        IF bnView == 1 THEN bnDrag3D(mnX, mnY); ELSE bnDragC(mnX, mnY); END;
''', '''        IF bnView == 1 THEN bnDrag3D(mnX, mnY); END;
        IF bnView == 2 THEN bnDragC(mnX, mnY); END;
        IF bnView == 3 THEN bnTgTap(mnX, mnY); END;
''')
rep('''      ELSE
        // from above, Left and Right move the slice
        IF mnK == 7 THEN bnSlc := 1; bnSetX0(bnX0 - 0.25); END;
        IF mnK == 8 THEN bnSlc := 1; bnSetX0(bnX0 + 0.25); END;
      END;
''', '''      END;
      IF bnView == 2 THEN
        // from above, Left and Right move the slice
        IF mnK == 7 THEN bnSlc := 1; bnSetX0(bnX0 - 0.25); END;
        IF mnK == 8 THEN bnSlc := 1; bnSetX0(bnX0 + 0.25); END;
      END;
''')
rep('''    IF mnAct == 3 THEN bnView := 3 - bnView; END;
    IF mnAct == 4 THEN bnSlc := 1 - bnSlc; END;
    IF mnAct == 5 THEN bnReset(); END;
''', '''    IF mnAct == 3 THEN bnNextV(); END;
    // beta 1g: in the target view key 4 fires 50 shots and key 5 clears
    // them; in the other two views they are Slice and Reset, as before
    IF mnAct == 4 THEN
      IF bnView == 3 THEN
        IF bnCpD == 1 THEN bnCepC(); END;
        bnShots(50);
      ELSE
        bnSlc := 1 - bnSlc;
      END;
    END;
    IF mnAct == 5 THEN
      IF bnView == 3 THEN
        bnShN := 0; bnShIn := 0;
      ELSE
        bnReset();
      END;
    END;
''')
rep('''  RETURN "BiNorm3D: " + bnRS + " = " + bnCm(bnF(bnRho, 2)) + ", E[Y | X = x] = " + bnCm(bnF(bnRho, 2)) + " x; " + bnRS + " in BN_RHO";
''', '''  // beta 1g: a run that opened the target view also names the CEP
  IF bnTgt == 1 THEN
    IF bnCpD == 1 THEN bnCepC(); END;
    RETURN "BiNorm3D: " + bnRS + " = " + bnCm(bnF(bnRho, 2)) + ", E[Y | X = x] = " + bnCm(bnF(bnRho, 2)) + " x, CEP = " + bnCm(bnF(bnCpR, 3)) + "; " + bnRS + " in BN_RHO, the CEP in BN_CEP";
  END;
  RETURN "BiNorm3D: " + bnRS + " = " + bnCm(bnF(bnRho, 2)) + ", E[Y | X = x] = " + bnCm(bnF(bnRho, 2)) + " x; " + bnRS + " in BN_RHO";
''')

# ---------------- the two numbers in the help text come from the reference, not from memory ----------------
import math
def cep(rho, M=4000):
    A, B = 1 + abs(rho), 1 - abs(rho)
    g = [math.cos((i + 0.5)*math.pi/2/M)**2/(2*A) + math.sin((i + 0.5)*math.pi/2/M)**2/(2*B) for i in range(M)]
    R = math.sqrt(2*math.log(2))*(A*B)**0.25
    for _ in range(60):
        P = sum((1 - math.exp(-R*R*x))/(2*x) for x in g)/(M*math.sqrt(A*B))
        D = R*sum(math.exp(-R*R*x) for x in g)/(M*math.sqrt(A*B))
        R -= (P - 0.5)/D
    return R
rep('@R06@', '%.3f' % cep(0.6)); rep('@R09@', '%.3f' % cep(0.9))

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'BiNorm3D_beta1g.txt'), 'w', encoding='utf-8', newline='').write(s)
print('BiNorm3D_beta1g.txt written:', len(s.split('\n')) - 1, 'lines;  CEP(0.6) = %.4f, CEP(0.9) = %.4f, CEP(0) = %.4f' % (cep(0.6), cep(0.9), cep(0)))
