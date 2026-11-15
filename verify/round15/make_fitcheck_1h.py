# -*- coding: utf-8 -*-
"""Round 15 (15 Nov 2026): FitCheck beta 1h from beta 1g, by exact replacements (a miss stops the build).

New in beta 1h (Roger, 15 Nov 2026, of two things another calculator's statistics programs have and ours did not: "1 and 2
would be great"; this is 2):
  * the Tests page of the normality checks gives a standard error beside the skewness g1 and beside the excess kurtosis g2:
    their exact standard errors in samples of n from a normal population,
        SE(g1) = root( 6 (n - 2) / ((n + 1)(n + 3)) ),
        SE(g2) = root( 24 n (n - 2)(n - 3) / ((n + 1)^2 (n + 3)(n + 5)) ),
    the ones SciPy's skewtest and kurtosistest use (D'Agostino, Belanger & D'Agostino 1990; Anscombe & Glynn 1983, Eq. 1).
    The one shape line becomes two, and a third says what SE is.  Help page 5 (Normality) ends with a sentence on them.
  * WORDING (the block marked CREDITS below; Roger, 14 Nov 2026: "IS there an issue with 'reworking' the TI and Triola and
    Lloyd programs?", and his paragraph of thanks in the book's Appendix F, 15 Nov): the help's Credits page and the header
    say what was done with the TI programs.  They were decoded and read to see what each one computes, and FitCheck was
    written new in PPL: none of their code is in it.  The word "reworks" is gone.  Only words change.
  * THE CLOSING SUMMARY after a sample in bins (found on the Virtual Calculator, 15 Nov 2026, running the crimtab preset to
    see the new lines): a binned sample has no W, so the line FitCheck returns to Home was "FitCheck: nothing computed"
    although its Tests page had just shown a skewness and a kurtosis.  It now names those two numbers.
Written from the formulas; no other program's code was read for the standard errors.
Run from the repository's root:   python3 verify/round15/make_fitcheck_1h.py OUTDIR
"""
import io, os, subprocess, sys, textwrap
BASE = 'a7df6e7'; DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r15_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/FitCheck_beta1g.txt'], check=True, capture_output=True).stdout.decode('utf-8')


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)


def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)


# ---- header, history ----
rep('// FITCHECK - beta 1g  (13 Nov 2026)', '// FITCHECK - beta 1h  (%s)' % DATE)
note = ('Round 15 (Roger, 15 Nov 2026: "1 and 2 would be great").  The Tests page gives a standard error beside the '
        'skewness g1 and beside the excess kurtosis g2: their exact standard errors in samples of n from a normal '
        'population, root(6(n - 2)/((n + 1)(n + 3))) and root(24 n (n - 2)(n - 3)/((n + 1)^2 (n + 3)(n + 5))), the '
        'ones SciPy\'s skewtest and kurtosistest use (D\'Agostino, Belanger & D\'Agostino 1990; Anscombe & Glynn 1983, '
        'Eq. 1), checked against 400,000 simulated normal samples at each of seven sizes (fc_ShapeSE; fcSeS, fcSeK).  '
        'The shape line is two lines now and a third says what SE is; help page 5 ends with a sentence on them.  The '
        'credits (help page 8 and the header) say what was done with the TI programs: they were read to see what each '
        'one computes, and FitCheck was written new, with none of their code (Roger, 14-15 Nov 2026).  The closing '
        'summary after a sample in bins (crimtab) names its skewness and excess kurtosis: a binned sample has no W, and '
        'the summary said "nothing computed" after the Tests page had shown both (seen on the Virtual Calculator).')
before('// beta 1g (13 Nov 2026):', '// beta 1h (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')

# ---- the opening screen names the version ----
rep('fc_Frame("FitCheck - beta 1g");', 'fc_Frame("FitCheck - beta 1h");')

# ---- state ----
after('LOCAL fcPD, fcLDi, fcSkw, fcKur, fcBin, fcBM;\n', 'LOCAL fcSeS, fcSeK;\n')
after('//  sorted index where D occurs; skewness g1 and excess kurtosis g2;\n',
      '//  (beta 1h) fcSeS and fcSeK their standard errors in normal samples;\n')

# ---- the arithmetic: one routine, called where g1 and g2 are set ----
before('''// Load a sample for the normality tests: sorts it, mean, SD (n - 1,
''', '''// beta 1h: the standard errors of the skewness g1 = m3/m2^1.5 and the excess
// kurtosis g2 = m4/m2^2 - 3 in samples of seN values from a NORMAL population.
// Both are exact (not large-sample approximations):
//   SE(g1) = root( 6 (n - 2) / ((n + 1)(n + 3)) )
//   SE(g2) = root( 24 n (n - 2)(n - 3) / ((n + 1)^2 (n + 3)(n + 5)) )
// (D'Agostino, Belanger & D'Agostino 1990; Anscombe & Glynn 1983, Eq. 1: the
// ones SciPy's skewtest and kurtosistest use).  For n = 3, g2 is -1.5 whatever
// the data, and its SE is 0.  In a normal sample g1 averages 0 and g2 averages
// -6/(n + 1), a little below 0.  n is at least 3 here (fc_NormSet refuses
// fewer), so nothing is divided by 0 and nothing under a root is negative.
fc_ShapeSE(seN)
BEGIN
  fcSeS := (6 * (seN - 2) / ((seN + 1) * (seN + 3)))^0.5;
  fcSeK := (24 * seN * (seN - 2) * (seN - 3) / ((seN + 1)^2 * (seN + 3) * (seN + 5)))^0.5;
END;

''')
after('''  fcSkw := (nsM3 / nsN) / (nsM2 / nsN)^1.5;
  fcKur := (nsM4 / nsN) / (nsM2 / nsN)^2 - 3;
''', '''  fc_ShapeSE(nsN);
''')
after('''  fcSkw := (sbM3 / sbN) / (sbM2 / sbN)^1.5;
  fcKur := (sbM4 / sbN) / (sbM2 / sbN)^2 - 3;
''', '''  fc_ShapeSE(sbN);
''')

# ---- the Tests page: two shape lines with their SEs, and what SE is ----
rep('''  fc_TL("Skewness g" + CHAR(8321) + " = " + fc_Cm(fc_Sgn(fcSkw, 3)) + ",  excess kurtosis g" + CHAR(8322) + " = " + fc_Cm(fc_Sgn(fcKur, 3)), #000000h);
''', '''  fc_TL("Skewness g" + CHAR(8321) + " = " + fc_Cm(fc_Sgn(fcSkw, 3)) + "  (SE " + fc_Cm(fc_F(fcSeS, 3)) + ")", #000000h);
  fc_TL("Excess kurtosis g" + CHAR(8322) + " = " + fc_Cm(fc_Sgn(fcKur, 3)) + "  (SE " + fc_Cm(fc_F(fcSeK, 3)) + ")", #000000h);
  fc_TL("SE: the standard error in normal samples.", fcGRAY);
''')

# ---- help page 5 (Normality): one sentence more, two lines of the page's fourteen ----
rep('''given for n " + fcGe + " 5 and only below 0.10.  " + fcX2S + " on bins: df = k - 3.", fcBLUE);''',
    '''given for n " + fcGe + " 5 and only below 0.10.  " + fcX2S + " on bins: df = k - 3.  Tests page: skewness g" + CHAR(8321) + " and excess kurtosis g" + CHAR(8322) + ", each with its SE if the data are normal.", fcBLUE);''')

# ---- CREDITS: what was done with the TI programs (words only) ----
rep('''// Replaces / reworks (decoded in ref/triola_ti_programs/; credit to their
//   authors -- Triola's TI-83/84 CD and the TI program libraries):
''', '''// Does on the Prime what these TI-83/84 programs do.  They were decoded and
//   read (ref/triola_ti_programs/) to see what each one computes; FitCheck was
//   then written new in PPL, and none of their code is in it.  Credit to their
//   authors -- Triola's TI-83/84 CD and the TI program libraries:
''')
rep('''  fc_TL("FitCheck reworks Triola's TI-83/84 goodness-of-fit and normality programs (X2GOF, GOFPOISS, GOFBIN, GOFNORML, X2NORM2, KOLSMIR, CVMTEST1, NMLPROB, BENFORD and others) without their bugs: the header lists them.", fcGRAY);''',
    '''  fc_TL("FitCheck does on the Prime what Triola's TI-83/84 goodness-of-fit and normality programs do (X2GOF, GOFPOISS, GOFBIN, GOFNORML, X2NORM2, KOLSMIR, CVMTEST1, NMLPROB, BENFORD and others).  It was written new for the Prime, with none of their code and without their bugs: the header lists them.", fcGRAY);''')

# ---- the closing summary after a binned sample ----
before('''  IF mnS == "FitCheck:" THEN mnS := "FitCheck: nothing computed"; END;
''', '''  // beta 1h: a sample in bins (crimtab) has no W.  Its Tests page shows a skewness
  // and an excess kurtosis, so the summary names them instead of ending as
  // "nothing computed" (which is still what a session with no fit, no sample
  // and no test returns).
  IF fcHasN == 1 AND fcBin == 1 THEN mnS := mnS + " binned sample, skewness " + fc_Cm(fc_Sgn(fcSkw, 3)) + ", excess kurtosis " + fc_Cm(fc_Sgn(fcKur, 3)) + ";"; END;
''')

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'FitCheck_beta1h.txt'), 'w', encoding='utf-8', newline='').write(s)
print('FitCheck_beta1h.txt written:', len(s.split('\n')) - 1, 'lines')
