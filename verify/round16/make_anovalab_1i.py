# -*- coding: utf-8 -*-
"""Round 16 (15 Nov 2026): AnovaLab beta 1i from beta 1h, by exact replacements (a miss stops the build).

New in beta 1i (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please"; this is the sixth):
  * DUNNETT'S TEST: every group against one control.  One-way > Enter (the menu) > "Dunnett: all vs a control" asks
    which group is the control, says how long a G1 will need, asks before it starts, and then shows two new pages:
      page 6, the table: each group's difference from the control, its t, the family confidence interval, the
              adjusted p, a red star where p < alpha;
      page 7, the plot: the same intervals drawn, a dot and a bar a group, a dotted line at 0, red where the interval
              misses 0; a tap or Up/Down picks a group and its numbers are written under the plot.
  * THE P AND d crit ARE COMPUTED for the data's own group sizes, equal or not.  Given the control's mean and the
    pooled s, the k - 1 statistics are independent, so
        P(every |t_g| <= c) = INT f_S(s) G(c s) ds,   S = sqrt(chi-square_v / v),
        G(y) = INT phi(z) PROD_g [Phi(b_g z + y a_g) - Phi(b_g z - y a_g)] dz,  b_g = sqrt(n_g/n_c), a_g = sqrt(1 + b_g^2).
    G is tabulated once for a control (71 values, Simpson over z in [0, 6] doubled; 2 ceiling(5 sqrt(N/n_c)) intervals,
    16 at least), and the upper tail is summed as it stands: SUM w f (1 - G(c s)) / SUM w f, 64 Simpson intervals in
    u = sqrt(s) over s in 1 -/+ 8/sqrt(2 v), the density written relative to its top (no log-gamma).
  * Two-sided only; df 3 and up, as Tukey; a control with under 1/100 of all the values is refused with a sentence.
  * Set alpha keeps the p-values and asks before it computes d crit again.
  * Once the test has been computed, pages 6 and 7 stand between the F page and the Table page for Left and Right.
  * Help: 10 pages (9 before).  Page 5 is new, page 4 gets a line that points to it, pages 5 to 9 are now 6 to 10.
  * Written from the formulas (Dunnett 1955, 1964).  The HP-41C Users' Library Solutions book "Applied Statistics I",
    program STAT.08, was read (it gives each group's t against the control and leaves the comparison with Dunnett's
    printed table to the user): none of its code.
  * NUMBERS KEPT WHOLE (found by this version's layout check, with data in the thousands and beyond).  TEXTOUT_P draws
    as much of a text as its width holds, so beta 1h cut a number wider than its place: an SS of 2,467,448,033 in the
    ANOVA table's 62 pixels (data in the thousands are enough), a mean in the millions on the Checks page, a difference
    and its interval on the Pairs page, the y numbers of the three plots from 100,000 up, two lines of the variances
    page.  Every such number is measured now (av_AxW) and written shorter when it must be: fewer decimals, then the
    Prime's scientific form with up to 5 digits (av_FitN and its kin); the three plots move their left edge right by
    what the widest y number needs (av_AxSet); av_Gn writes 5 digits from 1E12 up (it wrote one: 1.5E12 read "2E12").
    A number that fitted is written as before.
With numbers that fitted, every other screen is beta 1h's, the help pages' numbers, the one-way menu's new item and the
opening page's list aside.
Run from the repository's root:   python3 verify/round16/make_anovalab_1i.py OUTDIR
"""
import io, json, os, re, subprocess, sys, textwrap
BASE = '4e8ff66'; DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r16_programs'
HERE = os.path.dirname(os.path.abspath(__file__))
GW = json.load(open(os.path.join(HERE, '..', 'round11', 'glyph_widths_vc.json')))
s = subprocess.run(['git', 'show', BASE + ':programs/AnovaLab_beta1h.txt'], check=True, capture_output=True).stdout.decode('utf-8')


def px(t, font=1): return sum((GW.get(str(ord(ch))) or [8, 9, 10])[font - 1] for ch in t)


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)


def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)


# the glyph variables of the program, as the screen shows them (for measuring a line written as a PPL expression)
GLY = {'avAl': chr(945), 'avGE': chr(8805), 'avTm': chr(215), 'avPM': chr(177), 'avRt': chr(8730), 'avSq': chr(178), 'avH0': 'H' + chr(8320),
       'avLR': chr(8592) + chr(8594), 'avUD': chr(8645), 'avMu': chr(956), 'avSg': chr(963), 'avS1': chr(8321), 'avS2': chr(8322)}


def shown(expr):
    """a PPL string expression made of "literals" and glyph variables joined by + -> the text on the screen"""
    out = ''; k = 0
    while k < len(expr):
        if expr[k] == '"':
            e = expr.index('"', k + 1); out += expr[k + 1:e]; k = e + 1
        elif expr[k] in ' +':
            k += 1
        else:
            m = re.match(r'[A-Za-z0-9_]+', expr[k:])
            if not m or m.group(0) not in GLY: sys.exit('BUILD STOPPED: cannot measure %r' % expr)
            out += GLY[m.group(0)]; k += len(m.group(0))
    return out


# what the verify script found for the engine (kept in one place: the header note, the section heading and help page 5 say it)
ERRS = ('against a fine Gauss-Legendre reference over 18 sets of group sizes (2 to 12 groups, equal and unequal, a control '
        'from 1/100 of the values up) and df 3 to 2,990, the p is within 0.05 % of its value wherever it is 0.0001 or more '
        '(a smaller one prints as "< 0.0001"), and d crit within 0.005 % for alpha 0.2 to 0.001 (verify_AnovaLab_beta1i.py)')

# ---------------- header ----------------
rep('// ANOVALAB - beta 1h  (15 Nov 2026)\n', '// ANOVALAB - beta 1i  (15 Nov 2026)\n')
rep('''//                         medians, Bartlett), post hoc pairs (Tukey-
//                         Kramer, Bonferroni, Holm, Scheffe), a dot plot
//                         with each mean and its CI (tap two groups to
//                         compare them), the F curve with the tail shaded
''', '''//                         medians, Bartlett), post hoc pairs (Tukey-
//                         Kramer, Bonferroni, Holm, Scheffe), a dot plot
//                         with each mean and its CI (tap two groups to
//                         compare them), the F curve with the tail shaded,
//                         and (from the Enter menu) Dunnett's test of every
//                         group against one control, as a table and as a
//                         plot of its intervals
''')
note = ('Round 16 (Roger, 15 Nov 2026, of six additions proposed for the programs: "Add all please").  DUNNETT\'S TEST: '
        'every group against one control.  One-way > Enter (the menu) > "Dunnett: all vs a control" asks which group is '
        'the control, says how long a G1 will need, asks before it starts, and then shows two new pages: page 6, a table '
        '(each group\'s difference from the control, its t, the family confidence interval, the adjusted p, a red star '
        'where p < alpha), and page 7, the same intervals drawn (a dot and a bar a group, a dotted line at 0, red where '
        'the interval misses 0; a tap or Up/Down picks a group, and its numbers are written under the plot).  The p and '
        'd crit are computed for the data\'s own group sizes, equal or not (section 3b: a table of the inner integral '
        'for those sizes, then Simpson\'s rule over s, the upper tail summed as it stands): ' + ERRS + '.  Two-sided only; '
        'df 3 and up, as Tukey; a control with under 1/100 of all the values is refused with a sentence.  Set alpha '
        'keeps the p-values and asks before it computes d crit again.  Once the test has been computed, pages 6 and 7 '
        'stand between the F page and the Table page for the Left and Right keys.  Help has 10 pages (9 before): page 5 is new, page 4 gets a '
        'line that points to it, and pages 5 to 9 are now 6 to 10.  The one-way menu has 12 items (Dunnett is the '
        'sixth, so items 1 to 6 are the six kinds of page), and the opening page names the test.  The group picker '
        '(av_PickG, with its fallback) moved up from section 12 to section 7, unchanged, because Dunnett\'s test picks '
        'its control with it.  Written from the formulas (Dunnett 1955, 1964); the HP-41C Users\' Library program '
        'STAT.08 was read, and none of its code is here.  NUMBERS KEPT WHOLE (found by this version\'s layout '
        'check, with data in the thousands and beyond): TEXTOUT_P draws as much of a text as its width holds, so beta '
        '1h cut a number wider than its place: an SS of 2,467,448,033 in the ANOVA table\'s 62 pixels (data in the '
        'thousands are enough), a mean in the millions on the Checks page, a difference and its interval on the Pairs '
        'page, the y numbers of the three plots from 100,000 up, and two lines of the variances page.  Every such '
        'number is measured now (av_AxW) and written shorter when it must be: fewer decimals, then the Prime\'s '
        'scientific form with up to 5 digits (av_FitN, av_FitG, av_FitGS, av_FitC, av_FitCI, av_FitT); the three plots '
        'move their left edge right by what the widest y number needs (av_AxSet, av_AxLb); and av_Gn writes 5 digits '
        'from 1E12 up (it wrote one: 1.5E12 read "2E12").  A number that fitted is written as before, so with such '
        'numbers every other screen is beta 1h\'s (verify_AnovaLab_beta1i.py runs the two side by side).  Harness '
        'only so far.')
before('// beta 1h (15 Nov 2026): Round 15', '// beta 1i (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')
after('//   Scheffe: Scheffe (1953) Biometrika 40:87-104.\n',
      '''//   Dunnett's test: Dunnett (1955) JASA 50:1096-1121 (the test);
//     Dunnett (1964) Biometrics 20:482-491 (the two-sided tables: this
//     program's d crit agrees with the 15 values tried, 3 to 10 groups
//     at df 10, 20 and 60, to their two decimals).
''')
before('// File map (line numbers of this file; file-level state 148-204):\n',
       '''// Dunnett's test (beta 1i) is written from the formulas in section 3b.
//   The HP-41C Users' Library Solutions book "Applied Statistics I",
//   program STAT.08, was read: after an ANOVA it gives each group's t
//   against the control, and the user compares it with Dunnett's printed
//   table (no probability is computed there).  None of its code is in
//   this program.
''')
a = s.index('// File map (line numbers of this file; file-level state 148-204):\n')
b = s.index('// ============================================================\n', a)
s = s[:a] + '''// File map (line numbers of this file; counted by the build script):
//   @M0@  file-level state
//   @M1@  1. small helpers: palette, drains, waits, formats, fit, frame, busy
//   @M2@  2. special functions: log-gamma, incomplete beta and gamma, tails, quantiles
//   @M3@  3. studentized range: StudRange PPL engine, P_k tabulated per k
//   @M3B@  3b. Dunnett's test: the table of G, the tail, d crit, the run
//   @M4@  4. presets (mock jury, draft 1970, insect sprays, judges)
//   @M5@  5. arithmetic: one-way, post hoc, Tukey, inverse, two-way Type III, blocks, variances
//   @M6@  6. curve page: F / chi-square cache and drawing
//   @M7@  7. one-way pages: Table, Checks, Pairs, Dots, F; Dunnett's table and plot
//   @M8@  8. help (10 pages), set alpha
//   @M9@  9. one-way view loop
//   @M10@  10. two-way pages and view
//   @M11@  11. randomized block pages and view
//   @M12@  12. variances pages and view
//   @M13@  13. your own data (D1-D9)
//   @M14@  14. presets menu, opening page, main menu (AnovaLab)
''' + s[b:]

# ---------------- state ----------------
after('LOCAL avSRE;\n', '''// ---- Dunnett's test (beta 1i): the setup for a control (the distinct
//      sizes of the other groups), the table of G and its key, the
//      results (avDnC = the control they are for, 0 = none; avDnD = d
//      crit, -1 not computed for this alpha, -2 "not now" or Esc) ----
LOCAL avDnB, avDnA, avDnM, avDnNz, avDnT, avDnKey;
LOCAL avDnC, avDnD, avDnP, avDnDf, avDnSE, avDnTs;
LOCAL avDnSel;
// ---- beta 1i: how an axis writes its numbers (av_AxSet), and the left
//      edge of the one-way dot plot (kept while its picture is cached) ----
LOCAL avAxF, avAxD, avAxS, avODL;
''')
after('  avSRE := 0;\n', '''  avDnB := {}; avDnA := {}; avDnM := {}; avDnNz := 0; avDnT := {}; avDnKey := "";
  avDnC := 0; avDnD := -1; avDnP := {}; avDnDf := {}; avDnSE := {}; avDnTs := {};
  avDnSel := 0;
  avAxF := 0; avAxD := 0; avAxS := 1; avODL := 36;
''')

# ---------------- section 1: numbers kept whole ----------------
HELPERS = r'''// ---- beta 1i: numbers kept whole.  TEXTOUT_P draws as much of a text
// as its width holds and drops the rest, so a number wider than its
// place lost its last digits (an SS of 2,467,448,033 in the table's 62
// pixels).  From beta 1i a number is measured first and written shorter
// when it must be: fewer decimals, then the Prime's scientific form.

// About how wide a number is in font 1: 6 pixels a character, 3 for a
// point or a comma, 5 for the Prime's minus sign (the calculator's own
// widths: GlyphProbe, 9 Nov 2026).
av_AxW(xwT)
BEGIN
  LOCAL xwW, xwI, xwC;
  xwW := 6*DIM(xwT);
  FOR xwI FROM 1 TO DIM(xwT) DO
    xwC := MID(xwT, xwI, 1);
    IF xwC == "." OR xwC == "," THEN xwW := xwW - 3; END;
    IF xwC == CHAR(8722) THEN xwW := xwW - 1; END;
  END;
  RETURN xwW;
END;

// A number for a place fnW pixels wide.  As av_Gn writes it (about 5
// digits) when that fits; a number of 10 or more, and a zero, then
// lose decimals one by one ("82,430.8" -> "82,431"; "0.0000" -> "0");
// what still does not fit, any
// number under 0.001 that is not 0 (av_Gn would print it as 0.0000)
// and any of 1E12 or more (STRING's fixed form is scientific there,
// with as many digits as decimals asked: 1 at the most here) go in
// the Prime's scientific form with 4 decimals, or as many fewer as
// the place needs ("9.7500E-8", "1.07E6", "1E6").
av_FitN(fnV, fnW)
BEGIN
  LOCAL fnS, fnD, fnA;
  fnA := ABS(fnV);
  IF (fnA >= 0.001 AND fnA < 1E12) OR fnA == 0 THEN
    fnD := 4;
    IF fnA >= 1 THEN fnD := 3; END;
    IF fnA >= 10 THEN fnD := 2; END;
    IF fnA >= 1000 THEN fnD := 1; END;
    IF fnA >= 100000 THEN fnD := 0; END;
    fnS := av_Cm(av_Fx(fnV, fnD));
    IF av_AxW(fnS) <= fnW THEN RETURN fnS; END;
    WHILE (fnA >= 10 OR fnA == 0) AND fnD > 0 DO
      fnD := fnD - 1;
      fnS := av_Cm(av_Fx(fnV, fnD));
      IF av_AxW(fnS) <= fnW THEN RETURN fnS; END;
    END;
    IF fnA == 0 THEN RETURN "0"; END;
  END;
  fnD := 4;
  WHILE fnD >= 0 DO
    fnS := STRING(fnV, 3, fnD);
    IF av_AxW(fnS) <= fnW THEN RETURN fnS; END;
    fnD := fnD - 1;
  END;
  RETURN fnS;
END;

// The same with its sign: "+2.13", "-0.567" (a 0 has none).
av_FitS(fsV, fsW)
BEGIN
  IF fsV > 0 THEN RETURN "+" + av_FitN(fsV, fsW - 6); END;
  RETURN av_FitN(fsV, fsW);
END;

// A number in a place of a page beta 1h already had: as av_Gn writes
// it whenever that fits, so the page reads as it did; else as av_FitN.
av_FitG(fgV, fgW)
BEGIN
  LOCAL fgS;
  fgS := av_Gn(fgV);
  IF av_AxW(fgS) <= fgW THEN RETURN fgS; END;
  RETURN av_FitN(fgV, fgW);
END;

// A number whose text is already made (ftS, for the value ftV): that
// text when it fits ftW pixels, else as av_FitN writes the value.
av_FitT(ftS, ftV, ftW)
BEGIN
  IF av_AxW(ftS) <= ftW THEN RETURN ftS; END;
  RETURN av_FitN(ftV, ftW);
END;

// The same for av_Sgn's signed form.
av_FitGS(fhV, fhW)
BEGIN
  LOCAL fhS;
  fhS := av_Sgn(fhV);
  IF av_AxW(fhS) <= fhW THEN RETURN fhS; END;
  RETURN av_FitS(fhV, fhW);
END;

// The same for av_Cmp's form (an F statistic in fcN characters).
av_FitC(fcV, fcN, fcW)
BEGIN
  LOCAL fcS;
  fcS := av_Cmp(fcV, fcN);
  IF av_AxW(fcS) <= fcW THEN RETURN fcS; END;
  RETURN av_FitN(fcV, fcW);
END;

// An interval "(lo, hi)" for a place fiW pixels wide: as av_Gn writes
// its two ends when that fits, else each end fitted to half the room.
av_FitCI(fiA, fiB, fiW)
BEGIN
  LOCAL fiS, fiT, fiH;
  fiS := av_Gn(fiA); fiT := av_Gn(fiB);
  IF av_AxW(fiS) + av_AxW(fiT) + 12 <= fiW THEN RETURN "(" + fiS + ", " + fiT + ")"; END;
  fiH := IP((fiW - 12)/2);
  RETURN "(" + av_FitN(fiA, fiH) + ", " + av_FitN(fiB, fiH) + ")";
END;

// A number of the axis av_AxSet prepared: with avAxD decimals and
// commas, or (avAxF = 1) in the Prime's scientific form with avAxD
// decimals, a tick at zero as "0".
av_AxLb(alV)
BEGIN
  IF avAxF == 0 THEN RETURN av_Cm(av_Fx(alV, avAxD)); END;
  IF ABS(alV) < avAxS/1000 THEN RETURN "0"; END;
  RETURN STRING(alV, 3, avAxD);
END;

// An axis whose numbers stand left of the plot (or under it).  It
// decides how they are written: with the asD decimals their step needs
// and commas, as before (avAxF = 0), unless such a number would need
// more than 80 pixels or more than 6 decimals, or is 1E12 or more:
// then all of them in scientific form (avAxF = 1) with the decimals
// that tell one tick from the next (8 at the most).  Returns the x for
// the plot's left edge: 36, as before, when every number fits the 32
// pixels left of it, and as much more as the widest number needs (in
// scientific form any tick can be the widest, so each is measured).
// asLo, asHi: the first and the last tick; asS: the step.
av_AxSet(asLo, asHi, asS, asD)
BEGIN
  LOCAL asW, asM, asV, asI;
  avAxS := asS; avAxF := 0; avAxD := asD;
  asM := MAX(ABS(asLo), ABS(asHi));
  IF asM <= 0 THEN asM := asS; END;
  asW := 999;
  IF asD <= 6 AND asM < 1E12 THEN
    asW := MAX(av_AxW(av_Cm(av_Fx(asLo, asD))), av_AxW(av_Cm(av_Fx(asHi, asD))));
  END;
  IF asW > 80 THEN
    avAxF := 1;
    avAxD := MAX(0, MIN(8, FLOOR(LOG(asM)) - FLOOR(LOG(asS))));
    asW := 0; asV := asLo; asI := 0;
    WHILE asV <= asHi + asS/1000 AND asI < 60 DO
      asW := MAX(asW, av_AxW(av_AxLb(asV)));
      asV := asV + asS; asI := asI + 1;
    END;
  END;
  RETURN MAX(36, asW + 4);
END;

'''
before('''// A p-value's digits: "< 0.0001" below what 4 decimals can show.
av_PT(ptP)
''', HELPERS)

# ---------------- section 3b: the engine ----------------
ENGINE = r'''// ============================================================
// 3b. DUNNETT'S TEST (beta 1i): every group against one control.
//    t_g = (mean_g - mean_c) / sqrt(MSW (1/n_g + 1/n_c)), for g <> c.
//    Given the control's mean and the pooled s, the k - 1 statistics
//    are independent.  With z the control's standardized mean and
//    S = s/sigma = sqrt(chi-square_v / v):
//      P(every |t_g| <= c) = INT f_S(s) G(c s) ds,
//      G(y) = INT phi(z) PROD_g [Phi(b_g z + y a_g) - Phi(b_g z - y a_g)] dz,
//      b_g = sqrt(n_g/n_c),  a_g = sqrt(1 + b_g^2).
//    - G depends on the group sizes only.  It is tabulated ONCE for a
//      control, at y = 0, 0.1, ..., 7 (71 values; G = 1 from 7 on), each
//      by Simpson's rule over z in [0, 6]: the integrand is even in z, so
//      the half is doubled.  The intervals: 2 x ceiling(5 sqrt(N/n_c)),
//      16 at least, because the product varies faster in z the smaller
//      the control is next to N (measured: that keeps G within 0.000001).
//      Groups of one size share a factor, raised to their number.  The
//      table is read by 4-point cubic interpolation, as Tukey's is.
//    - The upper tail P(max |t| > c) is summed as it stands, never as 1
//      minus a lower tail: SUM w f (1 - G(c s)) / SUM w f, 64 Simpson
//      intervals in u = sqrt(s), over s in 1 -/+ 8/sqrt(2 v) (from 0
//      when that is negative).  f is the density of S in u, written
//      relative to its top, so no log-gamma is needed, and dividing by
//      SUM w f makes the weights add to 1.
//    - d crit: the c whose tail is alpha, by the Illinois regula falsi
//      of av_SRCrit (8 to 22 tails, 12 as a rule).
//    - accuracy: @ERRL@
//    - df 3 and up, as Tukey.  A control with under 1/100 of the values
//      is refused (its table would need over 100 intervals).
//    - Esc is read at every table value and inside every tail.
// ============================================================

// The setup for control usC: the distinct sizes among the other groups
// (avDnB = b = sqrt(n/n_c), avDnA = a = sqrt(1 + b^2), avDnM = how many
// groups have that size) and the Simpson intervals avDnNz.  Returns the
// table's key, the control's size and then the others' in group order
// ("12|12,10,15,"): the same sizes give the same table.
av_DnSetup(usC)
BEGIN
  LOCAL usG, usJ, usF, usN, usK, usR;
  avDnB := {}; avDnA := {}; avDnM := {}; usN := {};
  usK := av_Fx(avRn(usC), 0) + "|";
  FOR usG FROM 1 TO avOK DO
    IF usG <> usC THEN
      usK := usK + av_Fx(avRn(usG), 0) + ",";
      usF := 0;
      FOR usJ FROM 1 TO SIZE(usN) DO
        IF usN(usJ) == avRn(usG) THEN usF := usJ; END;
      END;
      IF usF > 0 THEN
        avDnM(usF) := avDnM(usF) + 1;
      ELSE
        usR := avRn(usG)/avRn(usC);
        usN := CONCAT(usN, {avRn(usG)});
        avDnB := CONCAT(avDnB, {SQRT(usR)});
        avDnA := CONCAT(avDnA, {SQRT(1 + usR)});
        avDnM := CONCAT(avDnM, {1});
      END;
    END;
  END;
  // rounded first, so that 5 sqrt(N/n) = 10 is 10 on any machine
  avDnNz := MAX(16, 2*CEILING(ROUND(5*SQRT(avNN/avRn(usC)), 6)));
  RETURN usK;
END;

// The table of G for control ubC (avDnT, 71 values), kept under its
// key.  Returns 0 if Esc stopped it: the table it had is kept then.
//   Phi(u + w) - Phi(u - w), u = b z >= 0 and w = y a > 0, is taken from
//   lower tails only: Phi(w - u) - Phi(-u - w) when u > w (both small),
//   else 1 - Phi(-u - w) - Phi(u - w).
av_DnBuild(ubC)
BEGIN
  LOCAL ubK, ubNd, ubH, ubZ, ubW, ubT;
  LOCAL ubI, ubJ, ubG, ubY, ubS, ubP;
  LOCAL ubU, ubV, ubD;
  ubK := av_DnSetup(ubC);
  IF ubK == avDnKey THEN RETURN 1; END;
  ubNd := SIZE(avDnB);
  ubH := 6/avDnNz;
  // the nodes z = j h, and Simpson's weight x h/3 x phi(z) x 2
  ubZ := MAKELIST(0, ubI, 1, avDnNz + 1); ubW := MAKELIST(0, ubI, 1, avDnNz + 1);
  FOR ubJ FROM 0 TO avDnNz DO
    IF ubJ == 0 OR ubJ == avDnNz THEN
      ubS := 1;
    ELSE
      IF ubJ MOD 2 == 1 THEN ubS := 4; ELSE ubS := 2; END;
    END;
    ubZ(ubJ + 1) := ubJ*ubH;
    ubW(ubJ + 1) := 2*ubS*ubH/3*NORMALD(0, 1, ubJ*ubH);
  END;
  ubT := MAKELIST(0, ubI, 1, 71);
  FOR ubI FROM 2 TO 71 DO
    ubY := (ubI - 1)/10; ubS := 0;
    FOR ubJ FROM 1 TO avDnNz + 1 DO
      ubP := ubW(ubJ);
      FOR ubG FROM 1 TO ubNd DO
        ubU := avDnB(ubG)*ubZ(ubJ); ubV := ubY*avDnA(ubG);
        IF ubU > ubV THEN
          ubD := NORMALD_CDF(0, 1, ubV - ubU) - NORMALD_CDF(0, 1, -ubU - ubV);
        ELSE
          ubD := 1 - NORMALD_CDF(0, 1, -ubU - ubV) - NORMALD_CDF(0, 1, ubU - ubV);
        END;
        IF ubD <= 0 THEN
          ubP := 0;
        ELSE
          IF avDnM(ubG) == 1 THEN ubP := ubP*ubD; ELSE ubP := ubP*ubD^avDnM(ubG); END;
        END;
      END;
      ubS := ubS + ubP;
    END;
    ubT(ubI) := MIN(1, ubS);
    av_PrgTick(ubI, 71);
    IF avStop == 1 THEN RETURN 0; END;
  END;
  avDnT := ubT; avDnKey := ubK;
  RETURN 1;
END;

// G(y) read from the table by 4-point cubic (Lagrange) interpolation:
// the four grid values around y, t = y in grid steps from the first.
av_DnGI(ugY)
BEGIN
  LOCAL ugI, ugT, ugA, ugB, ugC, ugD;
  IF ugY <= 0 THEN RETURN 0; END;
  IF ugY >= 7 THEN RETURN 1; END;
  ugI := MIN(MAX(IP(ugY*10) - 1, 0), 67);
  ugT := ugY*10 - ugI;
  ugA := avDnT(ugI + 1); ugB := avDnT(ugI + 2); ugC := avDnT(ugI + 3); ugD := avDnT(ugI + 4);
  ugA := -ugA*(ugT - 1)*(ugT - 2)*(ugT - 3)/6 + ugB*ugT*(ugT - 2)*(ugT - 3)/2 - ugC*ugT*(ugT - 1)*(ugT - 3)/2 + ugD*ugT*(ugT - 1)*(ugT - 2)/6;
  RETURN MIN(1, MAX(0, ugA));
END;

// The upper tail P(max |t| > c) for v df (the table holds the sizes):
// SUM w f (1 - G(c s)) / SUM w f over ns Simpson intervals (even) in
// u = sqrt(s).  f = u s^(v-1) exp(-v s^2/2), divided by its value at
// its top s^2 = (v - 1)/v, is the density of S in u up to a constant
// that the division by SUM w f removes.  avStop = 1 (Esc) makes it
// return at once.
av_DnTail(utC, utV, utNs)
BEGIN
  LOCAL utW, utLo, utH, utE, utJ, utU;
  LOCAL utS, utF, utN, utD;
  IF avStop == 1 THEN RETURN 0; END;
  IF utC <= 0 THEN RETURN 1; END;
  utW := 8/SQRT(2*utV);
  utLo := SQRT(MAX(0, 1 - utW)); utH := (SQRT(1 + utW) - utLo)/utNs;
  utE := (utV - 1)*LN((utV - 1)/utV)/2 - (utV - 1)/2;
  utN := 0; utD := 0;
  FOR utJ FROM 0 TO utNs DO
    utU := utLo + utJ*utH; utS := utU*utU;
    IF utS > 0 THEN
      IF utJ == 0 OR utJ == utNs THEN
        utF := 1;
      ELSE
        IF utJ MOD 2 == 1 THEN utF := 4; ELSE utF := 2; END;
      END;
      utF := utF*utU*EXP((utV - 1)*LN(utS) - utV*utS*utS/2 - utE);
      utD := utD + utF;
      utN := utN + utF*(1 - av_DnGI(utC*utS));
    END;
    IF utJ MOD 8 == 0 THEN
      av_PrgTick(utJ, utNs);
      IF avStop == 1 THEN RETURN 0; END;
    END;
  END;
  RETURN utN/utD;
END;

// d crit: the c with P(max |t| > c) = alpha, by the Illinois-modified
// regula falsi of av_SRCrit on alpha - tail (8 to 22 tails, 12 as a
// rule).  Each tail is a step of the bar, which starts at ucO steps
// (the steps done before it).  Returns -2 if stopped.
av_DnCrit(ucA, ucV, ucNs, ucO)
BEGIN
  LOCAL ucQl, ucQh, ucFl, ucFh, ucQm, ucFm;
  LOCAL ucIt, ucSd, ucE;
  ucE := 0;
  ucQl := 0.6; ucFl := ucA - av_DnTail(ucQl, ucV, ucNs);
  ucE := ucE + 1; av_PrgStep(ucO + ucE, ucO + 22, "d crit: step " + av_I(ucE) + " (it takes 8 to 22)");
  ucQh := 4; ucFh := ucA - av_DnTail(ucQh, ucV, ucNs);
  ucE := ucE + 1; av_PrgStep(ucO + ucE, ucO + 22, "d crit: step " + av_I(ucE) + " (it takes 8 to 22)");
  WHILE ucFh < 0 AND ucQh < 60 AND avStop == 0 DO
    ucQh := ucQh*1.5; ucFh := ucA - av_DnTail(ucQh, ucV, ucNs);
    ucE := ucE + 1; av_PrgStep(ucO + ucE, ucO + 22, "d crit: step " + av_I(ucE) + " (it takes 8 to 22)");
  END;
  ucQm := (ucQl + ucQh)/2; ucSd := 0;
  FOR ucIt FROM 1 TO 40 DO
    IF avStop == 1 THEN BREAK; END;
    ucQm := (ucQl*ucFh - ucQh*ucFl)/(ucFh - ucFl);
    ucFm := ucA - av_DnTail(ucQm, ucV, ucNs);
    ucE := ucE + 1; av_PrgStep(ucO + ucE, ucO + 22, "d crit: step " + av_I(ucE) + " (it takes 8 to 22)");
    IF ABS(ucFm) < 1E-7 OR ABS(ucQh - ucQl) < 5E-5 THEN BREAK; END;
    IF ucFm*ucFl > 0 THEN
      ucQl := ucQm; ucFl := ucFm;
      IF ucSd == -1 THEN ucFh := ucFh/2; END;
      ucSd := -1;
    ELSE
      ucQh := ucQm; ucFh := ucFm;
      IF ucSd == 1 THEN ucFl := ucFl/2; END;
      ucSd := 1;
    END;
  END;
  IF avStop == 1 THEN RETURN -2; END;
  RETURN ucQm;
END;

// The G1 estimate shown before a Dunnett computation, for control ueC
// and ueEv tails: the table still to build (70 values x (nz + 1) nodes
// x the distinct sizes x 2 normal tails) plus 65 nodes a tail, at the 5
// to 15 ms an inner step that av_TEst uses.  In minutes from 2 minutes.
av_DnEst(ueC, ueEv)
BEGIN
  LOCAL ueU, ueK;
  ueK := av_DnSetup(ueC);
  ueU := ueEv*65*3;
  IF ueK <> avDnKey THEN ueU := ueU + 70*(avDnNz + 1)*SIZE(avDnB)*2; END;
  IF ueU*0.015 >= 120 THEN
    RETURN "about " + av_I(MAX(1, ROUND(ueU*0.005/60, 0))) + "-" + av_I(MAX(2, ROUND(ueU*0.015/60, 0))) + " min on a G1";
  END;
  RETURN "about " + av_I(MAX(1, ROUND(ueU*0.005, 0))) + "-" + av_I(MAX(2, ROUND(ueU*0.015, 0))) + " s on a G1";
END;

// The progress page of Dunnett's test, composed on G1 as av_PrgPage is:
// a title, what is happening and an estimate, an empty step bar and an
// empty inner bar (av_PrgStep and av_PrgTick fill them).
av_DnPage(upT, upE)
BEGIN
  av_Band("Working: Dunnett's test");
  av_Tx(upT, 12, 30, avBLUE);
  av_Tx("The largest |t| of several groups against one", 12, 50, #000000h);
  av_Tx("control follows a double integral, done here", 12, 63, #000000h);
  av_Tx("by Simpson's rule in PPL for these group sizes.", 12, 76, #000000h);
  av_Tx(upE, 12, 92, avMAG);
  av_Tx("Esc stops (read every few moments).", 12, 108, avRED);
  RECT_P(G1, 50, 140, 270, 152, #000000h, #FFFFFFh);
  RECT_P(G1, 50, 156, 270, 160, avGRAY, #FFFFFFh);
  BLIT_P(G0, 0, 0, G1);
END;

// Before any Dunnett computation: a one-line warning with the estimate,
// as a CHOOSE (av_TukeyAsk's way).  Returns 1 = go ahead, 0 = not now.
av_DnAsk(uqT, uqC, uqEv)
BEGIN
  LOCAL uqI;
  uqI := 0;
  CHOOSE(uqI, uqT + ": " + av_DnEst(uqC, uqEv), {"Compute it now", "Not now"});
  IF uqI == 1 THEN RETURN 1; END;
  RETURN 0;
END;

// Dunnett's test for control uaC: the table, then a p for every other
// group (a bar step each), then d crit.  The p-values are kept as soon
// as all of them are done; Esc during d crit leaves them with d crit
// marked not computed (-2).  Returns 1 when the p-values stand, 0 when
// Esc came before that (nothing is changed then).
av_DnAll(uaC)
BEGIN
  LOCAL uaG, uaM, uaP, uaD, uaS, uaT;
  LOCAL uaN, uaK;
  uaM := avOK - 1;
  av_DnPage("Dunnett: every group against " + avOSh(uaC), "Estimate: " + av_DnEst(uaC, uaM + 14) + ".");
  avStop := 0;
  TEXTOUT_P("the table for these group sizes", G0, 50, 164, 1, avGRAY, 250);
  IF av_DnBuild(uaC) == 0 THEN av_KDrain(); RETURN 0; END;
  uaD := MAKELIST(0, uaG, 1, avOK); uaS := MAKELIST(0, uaG, 1, avOK);
  uaT := MAKELIST(0, uaG, 1, avOK); uaP := MAKELIST(-1, uaG, 1, avOK);
  uaN := 0;
  FOR uaG FROM 1 TO avOK DO
    IF uaG <> uaC THEN
      uaD(uaG) := avRm(uaG) - avRm(uaC);
      uaS(uaG) := SQRT(avMSW*(1/avRn(uaG) + 1/avRn(uaC)));
      uaT(uaG) := uaD(uaG)/uaS(uaG);
      uaP(uaG) := av_DnTail(ABS(uaT(uaG)), avDf2, 64);
      IF avStop == 1 THEN av_KDrain(); RETURN 0; END;
      uaN := uaN + 1;
      av_PrgStep(uaN, uaM + 22, "group " + av_I(uaN) + " of " + av_I(uaM));
    END;
  END;
  // the p-values stand from here on, whatever happens to d crit
  avDnC := uaC; avDnDf := uaD; avDnSE := uaS; avDnTs := uaT; avDnP := uaP;
  avDnD := -2; avDnSel := 0;
  uaK := av_DnCrit(avAlpha, avDf2, 64, uaM);
  IF avStop == 0 THEN avDnD := uaK; END;
  av_KDrain();
  RETURN 1;
END;

// d crit alone, for the control the p-values are for (after Set alpha,
// or after an Esc): the table is built again only if its key differs.
av_DnCritRun()
BEGIN
  LOCAL urK;
  av_DnPage("d crit: every group against " + avOSh(avDnC) + ", " + avAl + " = " + av_AS(), "Estimate: " + av_DnEst(avDnC, 14) + ".");
  avStop := 0;
  avDnD := -2;
  IF av_DnBuild(avDnC) == 1 THEN
    urK := av_DnCrit(avAlpha, avDf2, 64, 0);
    IF avStop == 0 THEN avDnD := urK; END;
  END;
  av_KDrain();
  RETURN 0;
END;


'''
before('''// ============================================================
// 4. THE PRESETS (data/DATASETS.md only; the values were written into
''', ENGINE)

# ---------------- the arithmetic: new data and a new alpha forget what Dunnett's test held ----------------
rep('''  avScM := SQRT(avDf1*av_FQ(avAlpha, avDf1, avDf2));
  avQc := -1;
END;
''', '''  avScM := SQRT(avDf1*av_FQ(avAlpha, avDf1, avDf2));
  avQc := -1;
  // beta 1i: Dunnett's d crit is for one alpha too (its p-values stay)
  avDnD := -1;
END;
''')
rep('''  avPTop := 1; avPIx := 0; avSelA := 0; avSelB := 0;
  av_OCrit();
END;
''', '''  avPTop := 1; avPIx := 0; avSelA := 0; avSelB := 0;
  // beta 1i: new data, so Dunnett's results are for no group now (its
  // table stays: the same sizes would need the same one)
  avDnC := 0; avDnSel := 0;
  av_OCrit();
END;
''')
rep('''// The alpha-dependent constants of the one-way pages: t for each
// group's CI (pooled s), Bonferroni's t, Scheffe's multiplier.  Tukey's
// q crit is forgotten (it is recomputed when a page needs it).
''', '''// The alpha-dependent constants of the one-way pages: t for each
// group's CI (pooled s), Bonferroni's t, Scheffe's multiplier.  Tukey's
// q crit is forgotten (it is recomputed when a page needs it), and so
// is Dunnett's d crit.
''')

# ---------------- the group picker moves up (unchanged) ----------------
a = s.index('// The fallback group picker: one group at a time, literal menus.\nav_PickG2(p2T)\n')
b = s.index('// The alternative, by CHOOSE.  Returns 1, 2, 3 or 0.\nav_PickAlt(ptV)\n')
PICK = s[a:b]
if PICK.count('END;\n\n') != 2 or 'av_PickG(pgT)' not in PICK: sys.exit('BUILD STOPPED: the group picker is not the two routines expected')
s = s[:a] + s[b:]

# ---------------- section 7: Dunnett's pages ----------------
FOOT6 = 'avLR + " = page, " + avUD + " = a group, Ent = menu, Esc = main menu"'
FOOT7 = 'avLR + " = page, " + avUD + " or a tap = a group, Ent = menu"'
CAP6 = '"diff = its mean - the control\'s;  red * = differs at " + avAl + " = "'
LEG7 = '"red = the CI misses 0 (differs at " + avAl + " = "'
for nm, ex, lim in (('the footer of page 6', FOOT6, 312), ('the footer of page 7', FOOT7, 312), ('the caption of page 6', CAP6 + ' + "0.001"', 312),
                    ('the legend of page 7', LEG7 + ' + "0.001);  dotted line = 0"', 312),
                    ('page 6, line 3', '"CI = diff " + avPM + " d crit " + avTm + " SE;  p = P(largest |t| " + avGE + " this |t|)"', 312),
                    ('page 6, d crit missing', '"d crit not computed for " + avAl + " = 0.001 (not asked for, or Esc)."', 312),
                    ('page 7, no pick', '"Tap a row, or " + avUD + ", to read a group\'s numbers."', 312)):
    if px(shown(ex)) > lim: sys.exit('BUILD STOPPED: %s is %d pixels (%d at most)' % (nm, px(shown(ex)), lim))
PAGES = r'''// ---- beta 1i: Dunnett's test, every group against one control ----

// The group picker, moved up from section 12 in beta 1i, unchanged:
// Dunnett's test picks its control with it.
@PICK@// The group in row uwR (0 = the first row) of Dunnett's pages: the
// groups in their order, the control left out.  0 when there is none.
av_DnRowG(uwR)
BEGIN
  LOCAL uwG, uwN;
  uwN := -1;
  FOR uwG FROM 1 TO avOK DO
    IF uwG <> avDnC THEN
      uwN := uwN + 1;
      IF uwN == uwR THEN RETURN uwG; END;
    END;
  END;
  RETURN 0;
END;

// The height of a row of the plot: 40 pixels, less when the rows of
// k - 1 groups would not fit in 122 (11 groups: 11 pixels each).
av_DnPitch()
BEGIN
  RETURN MIN(40, IP(122/MAX(1, avOK - 1)));
END;

// A t statistic for a place 40 pixels wide: 3 decimals when they fit
// (up to 99.999 either way), else as av_FitN writes it.
av_DnTS(xsV)
BEGIN
  LOCAL xsS;
  xsS := av_Cm(av_Fx(xsV, 3));
  IF av_AxW(xsS) <= 40 THEN RETURN xsS; END;
  RETURN av_FitN(xsV, 40);
END;

// Up or Down on Dunnett's pages: the group before or after the picked
// one, the control skipped (from none: the first, or the last).
av_DnMove(umK)
BEGIN
  LOCAL umG;
  umG := avDnSel;
  IF umK == 12 THEN
    REPEAT umG := umG + 1; UNTIL umG > avOK OR umG <> avDnC;
    IF umG <= avOK THEN avDnSel := umG; END;
  ELSE
    IF umG == 0 THEN umG := avOK + 1; END;
    REPEAT umG := umG - 1; UNTIL umG < 1 OR umG <> avDnC;
    IF umG >= 1 THEN avDnSel := umG; END;
  END;
END;

// Menu > Dunnett.  Asks which group is the control, refuses what the
// engine cannot do with a sentence, says how long it will take and asks
// before it starts.  Returns 1 when Dunnett's pages can be shown.
av_DnRun()
BEGIN
  LOCAL unC;
  IF avDf2 < 3 THEN
    MSGBOX("Dunnett's test needs df within " + avGE + " 3 here (the PPL engine): N - k is " + av_I(avDf2) + ".");
    RETURN 0;
  END;
  unC := av_PickG("Dunnett: which is the control?");
  IF unC < 1 THEN RETURN 0; END;
  IF avNN > 100*avRn(unC) THEN
    MSGBOX("Dunnett's test here needs a control group with at least 1/100 of all the values: " + avON(unC) + " has " + av_I(avRn(unC)) + " of " + av_I(avNN) + ".");
    RETURN 0;
  END;
  IF unC == avDnC THEN
    // its p-values stand; only d crit may be missing (Set alpha, or Esc)
    IF avDnD < 0 THEN
      IF av_DnAsk("Dunnett d crit", unC, 14) == 1 THEN av_DnCritRun(); ELSE avDnD := -2; END;
    END;
    RETURN 1;
  END;
  IF av_DnAsk("Dunnett", unC, avOK - 1 + 14) == 0 THEN RETURN 0; END;
  IF av_DnAll(unC) == 0 THEN
    MSGBOX("Stopped (Esc): Dunnett's test was not computed.");
    RETURN 0;
  END;
  RETURN 1;
END;

// Page 6: Dunnett's test as a table, a row for every group but the
// control: its difference from the control, its t, the family CI and
// the adjusted p; red with a star where p < alpha.
av_ODrawDunn()
BEGIN
  LOCAL udG, udY, udR, udC, udMk, udHw;
  LOCAL udM, udS;
  av_Band("Dunnett: each group vs a control");
  udM := avOK - 1;
  av_Tx("Control: " + avON(avDnC) + "  (n = " + av_I(avRn(avDnC)) + ", mean " + av_FitN(avRm(avDnC), 72) + ")", 4, 22, avBLUE);
  IF avDnD > 0 THEN
    udS := " comparisons";
    IF udM == 1 THEN udS := " comparison"; END;
    av_Tx("d crit = " + av_Cm(av_Fx(avDnD, 3)) + "  (" + av_I(udM) + udS + ", df = " + av_I(avDf2) + ", " + avAl + " = " + av_AS() + ")", 4, 35, avBLUE);
    av_Tx("CI = diff " + avPM + " d crit " + avTm + " SE;  p = P(largest |t| " + avGE + " this |t|)", 4, 48, avGRAY);
  ELSE
    av_Tx("d crit not computed for " + avAl + " = " + av_AS() + " (not asked for, or Esc).", 4, 35, avRED);
    av_Tx("Menu > Dunnett computes it.  The p-values stand.", 4, 48, avGRAY);
  END;
  av_Tx("Group", 4, 60, avGRAY); av_Tx("diff", 44, 60, avGRAY); av_Tx("t", 96, 60, avGRAY);
  av_Tx(av_CS(1 - avAlpha) + " CI (family)", 138, 60, avGRAY); av_Tx("adj. p", 250, 60, avGRAY);
  LINE_P(G1, 3, 70, 316, 70, avGRAY);
  udR := 0;
  FOR udG FROM 1 TO avOK DO
    IF udG <> avDnC AND udR < 11 THEN
      udY := 72 + udR*11; udR := udR + 1;
      udC := #000000h; udMk := "";
      IF avDnP(udG) < avAlpha THEN udC := avRED; udMk := "*"; END;
      IF udG == avDnSel THEN RECT_P(G1, 2, udY - 1, 317, udY + 9, avLORN, avLORN); END;
      TEXTOUT_P(avOSh(udG), G1, 4, udY, 1, udC, 38);
      TEXTOUT_P(av_FitS(avDnDf(udG), 48), G1, 44, udY, 1, udC, 50);
      TEXTOUT_P(av_DnTS(avDnTs(udG)), G1, 96, udY, 1, udC, 40);
      IF avDnD > 0 THEN
        udHw := avDnD*avDnSE(udG);
        TEXTOUT_P("(" + av_FitN(avDnDf(udG) - udHw, 49) + ", " + av_FitN(avDnDf(udG) + udHw, 49) + ")", G1, 138, udY, 1, udC, 110);
      ELSE
        TEXTOUT_P("--", G1, 138, udY, 1, avGRAY, 110);
      END;
      TEXTOUT_P(av_PT(avDnP(udG)), G1, 250, udY, 1, udC, 54);
      TEXTOUT_P(udMk, G1, 308, udY, 1, udC, 10);
    END;
  END;
  av_Tx(@CAP6@ + av_AS(), 4, 195, avGRAY);
  av_Foot(@FOOT6@);
END;

// Page 7: Dunnett's intervals drawn.  A row for every group but the
// control: a black mark at its difference from the control, a bar for
// its family CI (red when the bar misses 0, blue otherwise), on one
// axis with a dotted line at 0.  The picked row is on a light band and
// its numbers are written under the plot.
av_ODrawDnPl()
BEGIN
  LOCAL ulG, ulM, ulLo, ulHi, ulHw, ulR;
  LOCAL ulY, ulP, ulX0, ulX1, ulX2, ulC;
  LOCAL ulSt, ulV, ulS, ulLx, ulW, ulD;
  LOCAL ulI, ulYa, ulSc, ulH2;
  av_Band("Dunnett plot: group minus control");
  ulM := avOK - 1; ulP := av_DnPitch(); ulH2 := IP(ulP/2);
  IF avDnD > 0 THEN
    av_Tx("Control: " + avOSh(avDnC) + ".  Bars: " + av_CS(1 - avAlpha) + " family CIs (d crit " + av_Cm(av_Fx(avDnD, 3)) + ").", 4, 22, avBLUE);
  ELSE
    av_Tx("Control: " + avOSh(avDnC) + ".  No bars: d crit is not computed.", 4, 22, avRED);
  END;
  // the scale: every interval (or mark) and 0, with a little room
  ulLo := 0; ulHi := 0;
  FOR ulG FROM 1 TO avOK DO
    IF ulG <> avDnC THEN
      ulHw := 0;
      IF avDnD > 0 THEN ulHw := avDnD*avDnSE(ulG); END;
      ulLo := MIN(ulLo, avDnDf(ulG) - ulHw); ulHi := MAX(ulHi, avDnDf(ulG) + ulHw);
    END;
  END;
  IF ulHi - ulLo <= 0 THEN ulLo := -1; ulHi := 1; END;
  ulW := (ulHi - ulLo)*0.04; ulLo := ulLo - ulW; ulHi := ulHi + ulW;
  // the plot runs from x 52 to x 308; the axis sits under the last row
  ulSc := 256/(ulHi - ulLo);
  ulYa := 36 + ulM*ulP + 2;
  ulX0 := 52 + ROUND((0 - ulLo)*ulSc, 0);
  ulR := 0;
  FOR ulG FROM 1 TO avOK DO
    IF ulG <> avDnC THEN
      ulY := 36 + ulR*ulP + ulH2; ulR := ulR + 1;
      IF ulG == avDnSel THEN RECT_P(G1, 2, ulY - ulH2, 317, ulY - ulH2 + ulP - 1, avLORN, avLORN); END;
      ulC := avBLUE;
      IF avDnP(ulG) < avAlpha THEN ulC := avRED; END;
      TEXTOUT_P(avOSh(ulG), G1, 4, ulY - 5, 1, ulC, 44);
      IF avDnD > 0 THEN
        ulHw := avDnD*avDnSE(ulG);
        ulX1 := 52 + ROUND((avDnDf(ulG) - ulHw - ulLo)*ulSc, 0);
        ulX2 := 52 + ROUND((avDnDf(ulG) + ulHw - ulLo)*ulSc, 0);
        RECT_P(G1, ulX1, ulY - 1, ulX2, ulY + 1, ulC, ulC);
        LINE_P(G1, ulX1, ulY - 3, ulX1, ulY + 3, ulC);
        LINE_P(G1, ulX2, ulY - 3, ulX2, ulY + 3, ulC);
      END;
      av_Mark(52 + ROUND((avDnDf(ulG) - ulLo)*ulSc, 0), ulY, #000000h);
      IF avDnP(ulG) < avAlpha THEN TEXTOUT_P("*", G1, 311, ulY - 5, 1, avRED, 8); END;
    END;
  END;
  // the line of no difference, dotted, down the rows
  av_DotV(ulX0, 34, ulYa, avGRAY);
  // the axis: ticks at nice steps (Heckbert), their numbers as av_AxSet
  // decides; a number that would touch the one before it is left out,
  // and none runs off the screen
  LINE_P(G1, 52, ulYa, 308, ulYa, #000000h);
  ulSt := av_Nice((ulHi - ulLo)/8);
  ulD := MAX(0, -FLOOR(LOG(ulSt)));
  ulV := CEILING(ulLo/ulSt)*ulSt;
  // how the numbers are written (the margin av_AxSet returns is for a
  // y axis: not used here)
  ulW := av_AxSet(ulV, FLOOR(ulHi/ulSt)*ulSt, ulSt, ulD);
  ulLx := -100; ulI := 0;
  WHILE ulV + ulI*ulSt <= ulHi AND ulI < 12 DO
    ulX1 := 52 + ROUND((ulV + ulI*ulSt - ulLo)*ulSc, 0);
    LINE_P(G1, ulX1, ulYa, ulX1, ulYa + 2, #000000h);
    ulS := av_AxLb(ulV + ulI*ulSt);
    ulW := av_AxW(ulS);
    ulX2 := MAX(2, MIN(317 - ulW, ulX1 - IP(ulW/2)));
    IF ulX2 > ulLx + 4 THEN
      TEXTOUT_P(ulS, G1, ulX2, ulYa + 3, 1, avGRAY, ulW + 2);
      ulLx := ulX2 + ulW;
    END;
    ulI := ulI + 1;
  END;
  IF avDnD > 0 THEN
    av_Tx(@LEG7@ + av_AS() + ");  dotted line = 0", 4, 173, avGRAY);
  ELSE
    av_Tx("red = p < " + avAl + " = " + av_AS() + " (differs);  dotted line = 0", 4, 173, avGRAY);
  END;
  IF avDnSel > 0 AND avDnSel <> avDnC THEN
    av_Tx(avOSh(avDnSel) + " - " + avOSh(avDnC) + " = " + av_FitS(avDnDf(avDnSel), 52) + ";  t = " + av_DnTS(avDnTs(avDnSel)) + ";  " + av_PE(avDnP(avDnSel)), 4, 184, #000000h);
    IF avDnD > 0 THEN
      ulHw := avDnD*avDnSE(avDnSel);
      av_Tx(av_CS(1 - avAlpha) + " family CI: " + av_FitN(avDnDf(avDnSel) - ulHw, 60) + " to " + av_FitN(avDnDf(avDnSel) + ulHw, 60) + ";  SE " + av_FitN(avDnSE(avDnSel), 52), 4, 195, #000000h);
    ELSE
      av_Tx("SE " + av_FitN(avDnSE(avDnSel), 52) + ";  no CI without d crit (Menu > Dunnett)", 4, 195, #000000h);
    END;
  ELSE
    av_Tx("Tap a row, or " + avUD + ", to read a group's numbers.", 4, 184, avGRAY);
  END;
  av_Foot(@FOOT7@);
END;

'''.replace('@PICK@', PICK).replace('@CAP6@', CAP6).replace('@FOOT6@', FOOT6).replace('@FOOT7@', FOOT7).replace('@LEG7@', LEG7)
before('// Draw the current one-way page.\nav_ODraw()\n', PAGES)
rep('''  IF avScr == 5 THEN av_ODrawF(); END;
END;
''', '''  IF avScr == 5 THEN av_ODrawF(); END;
  // beta 1i: Dunnett's table and plot
  IF avScr == 6 THEN av_ODrawDunn(); END;
  IF avScr == 7 THEN av_ODrawDnPl(); END;
END;
''')

# ---------------- the old pages: numbers kept whole ----------------
# av_Gn from 1E12 up: STRING's fixed form is scientific there and keeps as many digits as decimals were asked, none
rep('''  IF gnA >= 100000 THEN gnD := 0; END;
  RETURN av_Cm(av_Fx(gnV, gnD));
END;
''', '''  IF gnA >= 100000 THEN gnD := 0; END;
  // beta 1i: from 1E12 up STRING's fixed form is scientific and keeps
  // one digit when no decimals are asked (1.5E12 read "2E12"): 5 digits
  IF gnA >= 1E12 THEN RETURN STRING(gnV, 3, 4); END;
  RETURN av_Cm(av_Fx(gnV, gnD));
END;
''')
# the two lines of the variances page that work the statistic out: three numbers share what the words leave
W1 = (312 - px(chr(967) + chr(178) + ' = (n - 1)s' + chr(178) + '/' + chr(963) + chr(8320) + chr(178) + ' =  ' + chr(215) + '  /  = ') - 30) // 3
W2 = (312 - px('F = s' + chr(8321) + chr(178) + '/s' + chr(8322) + chr(178) + ' =  /  = , df , ') - 60) // 3
if not (50 <= W1 <= 70 and 40 <= W2 <= 60): sys.exit('BUILD STOPPED: the variance lines leave %d and %d pixels a number' % (W1, W2))
rep('''" " + avTm + " " + av_Gn(avVS1^2) + " / " + av_Gn(avVSg0^2) + " = " + av_Cm(av_Fx(avVStat, 3)), 4, 63, avBLUE);''',
    '''" " + avTm + " " + av_FitG(avVS1^2, %d) + " / " + av_FitG(avVSg0^2, %d) + " = " + av_FitT(av_Cm(av_Fx(avVStat, 3)), avVStat, %d), 4, 63, avBLUE);''' % (W1, W1, W1))
rep('''" = " + av_Gn(avVS1^2) + " / " + av_Gn(avVS2^2) + " = " + av_Cm(av_Fx(avVStat, 4)) + ", df "''',
    '''" = " + av_FitG(avVS1^2, %d) + " / " + av_FitG(avVS2^2, %d) + " = " + av_FitT(av_Cm(av_Fx(avVStat, 4)), avVStat, %d) + ", df "''' % (W2, W2, W2))
# the three ANOVA tables: SS in 62 pixels, MS in 56, F in 40
def row(m):
    line = m.group(0)
    if '"Source"' in line: return line
    k = [0]
    def gn(mm):
        k[0] += 1
        return 'av_FitG(%s, %d)' % (mm.group(1), 62 if k[0] == 1 else 56)
    line2 = re.sub(r'av_Gn\(((?:[^()]|\([^()]*\))*)\)', gn, line)
    line2 = re.sub(r'av_Cmp\(((?:[^()]|\([^()]*\))*), 6\)', r'av_FitC(\1, 6, 40)', line2)
    if k[0] not in (1, 2): sys.exit('BUILD STOPPED: a table row with %d numbers: %r' % (k[0], line))
    return line2
n_rows = len(re.findall(r'(?m)^ .*av_Row\([^\n]*$', s))
s = re.sub(r'(?m)^ .*av_Row\([^\n]*$', row, s)
# 13 rows (3 of them headings); 17 SS and MS cells, 4 F cells, the two routines' own headings and the 4 av_FitG of the variance lines
if n_rows != 13 or s.count('av_FitG(') != 17 + 1 + 4 or s.count('av_FitC(') != 4 + 1: sys.exit('BUILD STOPPED: the table rows (%d rows, %d av_FitG, %d av_FitC)' % (n_rows, s.count('av_FitG('), s.count('av_FitC(')))
# the Checks page: the mean, s and median of each group
rep('''      av_Tx(av_Gn(avRm(ocG)), 140, ocY, #000000h);
      av_Tx(av_Gn(SQRT(avRv(ocG))), 200, ocY, #000000h);
      av_Tx(av_Gn(avRmd(ocG)), 256, ocY, #000000h);
''', '''      // beta 1i: each number in the room up to the next column
      av_Tx(av_FitG(avRm(ocG), 56), 140, ocY, #000000h);
      av_Tx(av_FitG(SQRT(avRv(ocG)), 52), 200, ocY, #000000h);
      av_Tx(av_FitG(avRmd(ocG), 60), 256, ocY, #000000h);
''')
rep('''      TEXTOUT_P(av_Gn(avRm(ocG)), G1, ocX + 64, ocY, 1, #000000h, 44);
      TEXTOUT_P(av_Gn(SQRT(avRv(ocG))), G1, ocX + 110, ocY, 1, #000000h, 44);
''', '''      TEXTOUT_P(av_FitG(avRm(ocG), 44), G1, ocX + 64, ocY, 1, #000000h, 44);
      TEXTOUT_P(av_FitG(SQRT(avRv(ocG)), 44), G1, ocX + 110, ocY, 1, #000000h, 44);
''')
# the Pairs page: the difference and its interval
rep('''    TEXTOUT_P(av_Sgn(avPD(dpR)), G1, 84, dpY, 1, dpC, 46);
''', '''    TEXTOUT_P(av_FitGS(avPD(dpR), 46), G1, 84, dpY, 1, dpC, 46);
''')
rep('''      TEXTOUT_P("(" + av_Gn(avPD(dpR) - dpHw) + ", " + av_Gn(avPD(dpR) + dpHw) + ")", G1, 132, dpY, 1, dpC, 106);
''', '''      TEXTOUT_P(av_FitCI(avPD(dpR) - dpHw, avPD(dpR) + dpHw, 106), G1, 132, dpY, 1, dpC, 106);
''')
# the Dots page: its left edge moves right when a y number needs more than 32 pixels; the pair's line
rep('''  LOCAL ddM, ddH, ddT, ddR, ddX2, ddPr;
  ddW := (avDR - avDL)/avOK;
''', '''  LOCAL ddM, ddH, ddT, ddR, ddX2, ddPr;
  // beta 1i: the left edge is this plot's own (avODL), found when the
  // picture is drawn and kept with it
  avDL := avODL;
  ddW := (avDR - avDL)/avOK;
''')
rep('''    ddDc := MAX(0, -FLOOR(LOG(ddS)));
    // ---- grid and y ticks ----
''', '''    ddDc := MAX(0, -FLOOR(LOG(ddS)));
    // beta 1i: how the y numbers are written, and the room they need
    avODL := av_AxSet(ddLo, ddHi, ddS, ddDc);
    avDL := avODL;
    ddW := (avDR - avDL)/avOK;
    // ---- grid and y ticks ----
''')
rep('''      TEXTOUT_P(av_Cm(av_Fx(ddV, ddDc)), G1, 2, ddY - 5, 1, avGRAY, 32);
''', '''      TEXTOUT_P(av_AxLb(ddV), G1, 2, ddY - 5, 1, avGRAY, avDL - 4);
''')
rep('''      av_Tx(avOSh(avPI(ddPr)) + " - " + avOSh(avPJ(ddPr)) + ": diff " + av_Sgn(avPD(ddPr)) + ", CI (" + av_Gn(avPD(ddPr) - ddH) + ", " + av_Gn(avPD(ddPr) + ddH) + ")", 4, 184, ddC);
    ELSE
      av_Tx(avOSh(avPI(ddPr)) + " - " + avOSh(avPJ(ddPr)) + ": diff " + av_Sgn(avPD(ddPr)) + " (no CI yet)", 4, 184, ddC);
''', '''      // beta 1i: 58 pixels a number, which the line holds beside two names
      av_Tx(avOSh(avPI(ddPr)) + " - " + avOSh(avPJ(ddPr)) + ": diff " + av_FitGS(avPD(ddPr), 58) + ", CI (" + av_FitG(avPD(ddPr) - ddH, 58) + ", " + av_FitG(avPD(ddPr) + ddH, 58) + ")", 4, 184, ddC);
    ELSE
      av_Tx(avOSh(avPI(ddPr)) + " - " + avOSh(avPJ(ddPr)) + ": diff " + av_FitGS(avPD(ddPr), 58) + " (no CI yet)", 4, 184, ddC);
''')
# the interaction plot and the profile plot: the same for their y numbers
rep('''  tpDc := MAX(0, -FLOOR(LOG(tpR(3))));
  tpV := tpR(1);
''', '''  tpDc := MAX(0, -FLOOR(LOG(tpR(3))));
  // beta 1i: how the y numbers are written, and the room they need
  avDL := av_AxSet(tpR(1), tpR(2), tpR(3), tpDc);
  tpV := tpR(1);
''')
rep('''    TEXTOUT_P(av_Cm(av_Fx(tpV, tpDc)), G1, 2, tpY - 5, 1, avGRAY, 32);
''', '''    TEXTOUT_P(av_AxLb(tpV), G1, 2, tpY - 5, 1, avGRAY, avDL - 4);
''')
rep('''  bpDc := MAX(0, -FLOOR(LOG(bpS)));
  bpW := (avDR - avDL)/avBKt;
''', '''  bpDc := MAX(0, -FLOOR(LOG(bpS)));
  // beta 1i: how the y numbers are written, and the room they need
  avDL := av_AxSet(bpLo, bpHi, bpS, bpDc);
  bpW := (avDR - avDL)/avBKt;
''')
rep('''    TEXTOUT_P(av_Cm(av_Fx(bpV, bpDc)), G1, 2, bpY - 5, 1, avGRAY, 32);
''', '''    TEXTOUT_P(av_AxLb(bpV), G1, 2, bpY - 5, 1, avGRAY, avDL - 4);
''')

# ---------------- help: 10 pages ----------------
a = s.index('av_HelpPage(hpN)\nBEGIN\n'); b = s.index('// The help pages from page hsN on.\n')
H = s[a:b]
for old, new in ((9, 10), (8, 9), (7, 8), (6, 7), (5, 6)):
    for x, y in (('  IF hpN == %d THEN\n' % old, '  IF hpN == %d THEN\n' % new), ('"AnovaLab help %d/9: ' % old, '"AnovaLab help %d/10: ' % new)):
        if H.count(x) != 1: sys.exit('BUILD STOPPED: help page %d, %r' % (old, x))
        H = H.replace(x, y)
for k in (4, 3, 2, 1):
    x = '"AnovaLab help %d/9: ' % k
    if H.count(x) != 1: sys.exit('BUILD STOPPED: help page %d header' % k)
    H = H.replace(x, '"AnovaLab help %d/10: ' % k)
# page 4: a line that points to the new page
x = '''    av_Tx("2-12, df 3-1,000, " + avAl + " .1-.001).", 10, 114, avGRAY);
  END;
'''
P4 = '"One group is the control?  Dunnett\'s test: the next page."'
if px(shown(P4)) > 296: sys.exit('BUILD STOPPED: help page 4, the new line is %d pixels' % px(shown(P4)))
if H.count(x) != 1: sys.exit('BUILD STOPPED: help page 4, the last line')
H = H.replace(x, '''    av_Tx("2-12, df 3-1,000, " + avAl + " .1-.001).", 10, 114, avGRAY);
    // beta 1i
    av_Tx(%s, 10, 130, #000000h);
  END;
''' % P4)
# page 5: Dunnett's test (13 lines; a new paragraph 16 pixels down, a new line 13)
HELP5 = [('"Dunnett\'s test compares every group with ONE control"', '#000000h', 0),
         ('"group (a placebo, the usual method): k - 1 comparisons,"', '#000000h', 0),
         ('"not all the pairs.  With fewer comparisons, it finds a"', '#000000h', 0),
         ('"real difference more often than Tukey\'s test does."', '#000000h', 0),
         ('"t = (group mean - control mean)/SE, SE from MS within"', 'avBLUE', 1),
         ('"and both n.  A group differs when |t| > d crit, and d crit"', 'avBLUE', 0),
         ('"keeps the chance of ANY false alarm in the family at " + avAl + "."', 'avBLUE', 0),
         ('"Adjusted p: the chance that the LARGEST |t| of the"', 'avMAG', 1),
         ('"family is this big when no group differs from the control."', 'avMAG', 0),
         ('"Enter > Dunnett: pick the control.  It asks before it runs"', '#000000h', 1),
         ('"(slow on a G1).  Two pages: the table, then the CIs drawn."', '#000000h', 0),
         ('"Two-sided; unequal n allowed.  Choose the control before"', 'avGRAY', 1),
         ('"you see the data.  Dunnett (1955); p within 0.05 %."', 'avGRAY', 0)]
if len(HELP5) > 13: sys.exit('BUILD STOPPED: help page 5 has %d lines' % len(HELP5))
T5 = "AnovaLab help 5/10: Dunnett's test"
if px(T5, 2) > 300: sys.exit('BUILD STOPPED: help page 5, the title is %d pixels' % px(T5, 2))
y = 30; body = ''
for k, (ex, col, par) in enumerate(HELP5):
    if k: y += 16 if par else 13
    if px(shown(ex)) > 296: sys.exit('BUILD STOPPED: help page 5, a line of %d pixels (296 at most): %s' % (px(shown(ex)), ex))
    body += '    av_Tx(%s, 10, %d, %s);\n' % (ex, y, col)
if y > 198: sys.exit('BUILD STOPPED: help page 5 ends at y %d' % y)
x = '  IF hpN == 6 THEN\n    TEXTOUT_P("AnovaLab help 6/10: Two-way ANOVA"'
if H.count(x) != 1: sys.exit('BUILD STOPPED: help page 6 (the old 5) not found')
H = H.replace(x, '''  // beta 1i: Dunnett's test (the old pages 5 to 9 are 6 to 10)
  IF hpN == 5 THEN
    TEXTOUT_P("%s", G1, 10, 7, 2, avBLUE, 300);
%s  END;
''' % (T5, body) + x)
s = s[:a] + H + s[b:]
rep('''  hsP := MAX(1, MIN(9, hsN));
  WHILE hsP >= 1 AND hsP <= 9 DO
''', '''  hsP := MAX(1, MIN(10, hsN));
  WHILE hsP >= 1 AND hsP <= 10 DO
''')
rep('    IF vvA == 9 THEN av_Help(7); END;\n', '    IF vvA == 9 THEN av_Help(8); END;\n')
rep('    IF bvA == 9 THEN av_Help(6); END;\n', '    IF bvA == 9 THEN av_Help(7); END;\n')
rep('    IF tvA == 9 THEN av_Help(5); END;\n', '    IF tvA == 9 THEN av_Help(6); END;\n')

# ---------------- the one-way view ----------------
rep('''  IF oaK == 7 THEN
    IF avScr == 1 THEN RETURN 5; END;
    RETURN avScr - 1;
  END;
  IF oaK == 8 THEN
    IF avScr == 5 THEN RETURN 1; END;
    RETURN avScr + 1;
  END;
  RETURN 0;
END;
''', '''  // beta 1i: Dunnett's pages, 6 and 7, are in the round once the test
  // has been computed (their actions are 16 and 17: 6 and 7 are taken)
  IF avScr >= 6 AND (oaK == 2 OR oaK == 12) THEN
    av_DnMove(oaK);
    RETURN 0;
  END;
  IF oaK == 7 THEN
    IF avScr == 1 THEN
      IF avDnC > 0 THEN RETURN 17; END;
      RETURN 5;
    END;
    IF avScr == 7 THEN RETURN 16; END;
    RETURN avScr - 1;
  END;
  IF oaK == 8 THEN
    IF avScr == 7 THEN RETURN 1; END;
    IF avScr == 6 THEN RETURN 17; END;
    IF avScr == 5 THEN
      IF avDnC > 0 THEN RETURN 16; END;
      RETURN 1;
    END;
    RETURN avScr + 1;
  END;
  RETURN 0;
END;
''')
rep('''      IF avSelA == 0 OR avSelB > 0 THEN
        avSelA := otG; avSelB := 0; avPIx := 0;
      ELSE
        IF otG <> avSelA THEN avSelB := otG; avPIx := av_PairOf(avSelA, otG); END;
      END;
    END;
    RETURN 0;
  END;
  RETURN 0;
END;
''', '''      IF avSelA == 0 OR avSelB > 0 THEN
        avSelA := otG; avSelB := 0; avPIx := 0;
      ELSE
        IF otG <> avSelA THEN avSelB := otG; avPIx := av_PairOf(avSelA, otG); END;
      END;
    END;
    RETURN 0;
  END;
  // beta 1i: a tap on a row of Dunnett's table or plot picks its group
  IF avScr == 6 THEN
    IF avTapY >= 71 AND avTapY < 71 + 11*(avOK - 1) THEN
      otG := av_DnRowG(IP((avTapY - 71)/11));
      IF otG > 0 THEN avDnSel := otG; END;
    END;
    RETURN 0;
  END;
  IF avScr == 7 THEN
    otW := av_DnPitch();
    IF avTapY >= 36 AND avTapY < 36 + otW*(avOK - 1) THEN
      otG := av_DnRowG(IP((avTapY - 36)/otW));
      IF otG > 0 THEN avDnSel := otG; END;
    END;
    RETURN 0;
  END;
  RETURN 0;
END;
''')
rep('''    "F curve and p",
    "Next method (now " + av_MName() + ")",
    "Tukey p for every pair",
    "Tukey p for this pair",
    "Set " + avAl + " (now " + av_AS() + ")",
    "Help",
    "Back to the main menu"});
  IF omI >= 1 AND omI <= 5 THEN RETURN omI; END;
  IF omI == 6 THEN RETURN 7; END;
  IF omI == 7 THEN RETURN 8; END;
  IF omI == 8 THEN RETURN 14; END;
  IF omI == 9 THEN RETURN 13; END;
  IF omI == 10 THEN RETURN 9; END;
  IF omI == 11 THEN RETURN 11; END;
  RETURN 0;
END;
''', '''    "F curve and p",
    "Dunnett: all vs a control",
    "Next method (now " + av_MName() + ")",
    "Tukey p for every pair",
    "Tukey p for this pair",
    "Set " + avAl + " (now " + av_AS() + ")",
    "Help",
    "Back to the main menu"});
  IF omI >= 1 AND omI <= 5 THEN RETURN omI; END;
  // beta 1i: item 6 is Dunnett's test, so the items after it are one down
  IF omI == 6 THEN RETURN 15; END;
  IF omI == 7 THEN RETURN 7; END;
  IF omI == 8 THEN RETURN 8; END;
  IF omI == 9 THEN RETURN 14; END;
  IF omI == 10 THEN RETURN 13; END;
  IF omI == 11 THEN RETURN 9; END;
  IF omI == 12 THEN RETURN 11; END;
  RETURN 0;
END;
''')
rep('''// "More" key: slot 6 on every page).  Actions: 1-5 the pages, 7 next
// method, 8 Tukey p, 9 help, 10 menu, 11 back, 12 previous method,
// 13 set alpha, 14 Tukey p for the selected pair.
''', '''// "More" key: slot 6 on every page).  Actions: 1-5 the pages, 7 next
// method, 8 Tukey p, 9 help, 10 menu, 11 back, 12 previous method,
// 13 set alpha, 14 Tukey p for the selected pair; beta 1i: 15 Dunnett's
// test (the menu's item), 16 and 17 its two pages (the arrows).
''')
rep('''        IF av_TukeyAsk("Tukey q crit", 14) == 1 THEN av_TukeyCrit(); ELSE avQc := -2; END;
      END;
    END;
    av_ODraw();
''', '''        IF av_TukeyAsk("Tukey q crit", 14) == 1 THEN av_TukeyCrit(); ELSE avQc := -2; END;
      END;
    END;
    // beta 1i: Dunnett's pages need results (none after new data), and
    // d crit is asked for again after Set alpha, never started unasked
    IF avScr >= 6 AND avDnC == 0 THEN avScr := 1; END;
    IF avScr >= 6 AND avDnD == -1 THEN
      IF av_DnAsk("Dunnett d crit", avDnC, 14) == 1 THEN av_DnCritRun(); ELSE avDnD := -2; END;
    END;
    av_ODraw();
''')
rep('''    IF ovA == 9 THEN
      IF avScr == 3 OR avScr == 4 THEN av_Help(3); ELSE av_Help(1); END;
    END;
''', '''    IF ovA == 9 THEN
      IF avScr >= 6 THEN
        av_Help(5);
      ELSE
        IF avScr == 3 OR avScr == 4 THEN av_Help(3); ELSE av_Help(1); END;
      END;
    END;
    // beta 1i: Dunnett's test from the menu, and its pages by the arrows
    IF ovA == 15 THEN
      IF av_DnRun() == 1 THEN avScr := 6; END;
    END;
    IF ovA == 16 OR ovA == 17 THEN avScr := ovA - 10; END;
''')

# ---------------- the opening page ----------------
rep('  av_Band("AnovaLab - beta 1h");\n', '  av_Band("AnovaLab - beta 1i");\n')
L2 = '"one-way ANOVA (Welch, checks, post hoc, Dunnett),"'
if px(shown(L2)) > 306: sys.exit('BUILD STOPPED: the opening page, line 2 is %d pixels' % px(shown(L2)))
rep('  av_Tx("one-way ANOVA (Welch, checks, post hoc pairs),", 10, 40, avBLUE);\n', '  av_Tx(%s, 10, 40, avBLUE);\n' % L2)

# ---------------- numbers that come from the checks ----------------
rep('@ERRL@', '''against a fine Gauss-Legendre reference over 18 sets
//      of group sizes (2 to 12 groups, equal and unequal, a control from
//      1/100 of the values up) and df 3 to 2,990, the p is within 0.05 %
//      of its value wherever it is 0.0001 or more (a smaller one prints
//      as "< 0.0001"), and d crit within 0.005 % for alpha 0.2 to 0.001
//      (verify_AnovaLab_beta1i.py; a Python replica of this engine,
//      checked against the PPL in the harness)''')

# ---------------- the file map: counted here ----------------
def line_of(text, nth=1):
    k = -1
    for _ in range(nth):
        k = s.index(text, k + 1)
    return s.count('\n', 0, k) + 1
BAR = '// ============================================================\n'
def sec(title): return line_of(BAR + title)
starts = [('M0', line_of('// ---- palette (set in av_Init) ----')), ('M1', sec('// 1. SMALL HELPERS')), ('M2', sec('// 2. SPECIAL FUNCTIONS')),
          ('M3', sec('// 3. THE STUDENTIZED RANGE')), ('M3B', sec("// 3b. DUNNETT'S TEST")), ('M4', sec('// 4. THE PRESETS')),
          ('M5', sec('// 5. THE ARITHMETIC')), ('M6', sec('// 6. THE CURVE PAGE')), ('M7', sec('// 7. ONE-WAY: the pages')),
          ('M8', sec('// 8. HELP')), ('M9', sec('// 9. ONE-WAY: the view')), ('M10', sec('// 10. TWO-WAY')),
          ('M11', sec('// 11. RANDOMIZED BLOCKS')), ('M12', sec('// 12. VARIANCES')), ('M13', sec('// 13. YOUR OWN DATA')),
          ('M14', sec('// 14. PRESETS, THE OPENING PAGE'))]
if [b for (_, b) in starts] != sorted(b for (_, b) in starts): sys.exit('BUILD STOPPED: the sections are not in the order the file map lists them')
for k, (tag, a) in enumerate(starts):
    b = (starts[k + 1][1] - 1) if k + 1 < len(starts) else None
    rep('@%s@' % tag, '%4d-%s' % (a, 'end ' if b is None else '%-4d' % b))
if re.search(r'@[A-Z0-9]+@', s): sys.exit('BUILD STOPPED: a placeholder is left: %r' % re.findall(r'@[A-Z0-9]+@', s)[:5])
long = [(i + 1, len(l)) for i, l in enumerate(s.split('\n')) if len(l) > 330]
if long: sys.exit('BUILD STOPPED: a line of more than 330 characters: %r' % long[:3])

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'AnovaLab_beta1i.txt'), 'w', encoding='utf-8', newline='').write(s)
print('AnovaLab_beta1i.txt written:', len(s.split('\n')) - 1, 'lines')
