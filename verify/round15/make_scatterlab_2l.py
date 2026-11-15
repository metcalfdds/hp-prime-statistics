# -*- coding: utf-8 -*-
"""Round 15 (15 Nov 2026): ScatterLab beta 2l from beta 2k, by exact replacements (a miss stops the build).

New in beta 2l (Roger, 15 Nov 2026, of two things another calculator's statistics programs have and ours did not: "1 and 2
would be great"; this is 1):
  * the page Menu > Inference for the slope ends with a 95% confidence interval for rho, the population's correlation, by
    Fisher's z: z = 0.5 ln((1 + r)/(1 - r)), z -/+ 1.959964/root(n - 3), back through tanh.  It needs 4 points, and it is
    left out, with a sentence, for 3 points or when r is 1 or -1 in the Prime's 12 digits.  The line above it shows r.
  * help page 1 (What r measures) ends with a line that says where the interval is.
Written from the formula (any intermediate text gives it); no other program's code was read for it.
Run from the repository's root:   python3 verify/round15/make_scatterlab_2l.py OUTDIR
"""
import io, os, subprocess, sys, textwrap
BASE = 'a7df6e7'; DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r15_programs'
s = subprocess.run(['git', 'show', BASE + ':programs/ScatterLab_beta2k.txt'], check=True, capture_output=True).stdout.decode('utf-8')


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit('BUILD STOPPED: %d matches (wanted %d) for %r' % (c, n, a[:90]))
    s = s.replace(a, b)


def after(a, b):  rep(a, a + b)
def before(a, b): rep(a, b + a)


# ---- header, history ----
rep('// SCATTERLAB - beta 2k', '// SCATTERLAB - beta 2l')
note = ('Round 15 (Roger, 15 Nov 2026: "1 and 2 would be great").  New: the page Menu > Inference for the slope ends with a '
        '95% confidence interval for rho, the population\'s correlation, by Fisher\'s z: z = 0.5 ln((1 + r)/(1 - r)) is close '
        'to normal with standard error 1/root(n - 3), so z -/+ 1.959964/root(n - 3) is carried back to r through tanh '
        '(slInf: slRok, slRlo, slRhi).  It needs 4 points; with 3, or when r is 1 or -1 in 12 digits, the page says so '
        'instead.  The line above it now shows r.  Help page 1 ends with a line that says where the interval is.  The '
        'page\'s last three lines sit at y 175, 188 and 204 (they were two, at 181 and 194).  Nothing else is changed.')
before('// beta 2k (14 Nov 2026):', '// beta 2l (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n')
after('//   r = Sxy / sqrt(Sxx Syy),  r-squared = r^2\n',
      '//   95% interval for rho (beta 2l; slInf):  z = 0.5 ln((1 + r)/(1 - r)),\n'
      '//            z -/+ 1.959964 / sqrt(n - 3),  back through tanh\n')

# ---- state ----
after('LOCAL slTc, slTcD, slCiL, slCiH;\n', 'LOCAL slRok, slRlo, slRhi;\n')
after('//  slCiH the slope\'s 95% interval\n',
      '//  beta 2l: slRok 1 when rho has an interval (a test, 4 points or more,\n'
      '//  |r| below 1 in 12 digits);  slRlo, slRhi its 95% limits (Fisher\'s z)\n')

# ---- the arithmetic ----
rep('''  LOCAL ifD;
  slIok := 0; slSe := 0; slSeB := 0; slTv := 0; slPv := 1;
  slCiL := 0; slCiH := 0;
''', '''  LOCAL ifD, ifZ, ifH, ifE;
  slIok := 0; slSe := 0; slSeB := 0; slTv := 0; slPv := 1;
  slCiL := 0; slCiH := 0;
  slRok := 0; slRlo := 0; slRhi := 0;
''')
rep('''      slCiL := slB1 - slTc * slSeB;
      slCiH := slB1 + slTc * slSeB;
    END;
  END;
  SL_SEB := slSeB; SL_T := slTv; SL_P := slPv;
''', '''      slCiL := slB1 - slTc * slSeB;
      slCiH := slB1 + slTc * slSeB;
    END;
  END;
  // beta 2l: the 95% interval for rho by Fisher's z.  z = 0.5 ln((1 + r)/(1 - r))
  // is close to normal with standard error 1/root(n - 3), so the limits are
  // z -/+ 1.959964/root(n - 3), carried back to r by tanh(z) = (e^2z - 1)/(e^2z + 1).
  // It needs a test (slIok: the points are not all on the line), 4 points
  // (n - 3 is under the root) and |r| below 1 in the Prime's 12 digits
  // (1 - r is divided by).  |z| is then at most about 16, so e^2z is safe.
  IF slIok == 1 AND slRdef == 1 AND slN >= 4 AND ABS(slR) < 1 THEN
    ifZ := 0.5 * LN((1 + slR) / (1 - slR));
    ifH := 1.95996398454 / (slN - 3)^0.5;
    ifE := EXP(2 * (ifZ - ifH));
    slRlo := (ifE - 1) / (ifE + 1);
    ifE := EXP(2 * (ifZ + ifH));
    slRhi := (ifE - 1) / (ifE + 1);
    slRok := 1;
  END;
  SL_SEB := slSeB; SL_T := slTv; SL_P := slPv;
''')

# ---- the page ----
rep('''    slHT("s is the typical miss of a point from the line.", 181, slGRAY);
    slHT("The test of " + CHAR(961) + " = 0 gives the same t and p.", 194, slGRAY);
''', '''    slHT("s is the typical miss of a point from the line.", 175, slGRAY);
    ipS := "The test of " + CHAR(961) + " = 0 gives the same t and p.";
    slHT(slIL("r = " + slFx(slR, 3) + ".  " + ipS, ipS), 188, slGRAY);
    // beta 2l: the 95% interval for rho (slInf), or the reason there is none
    IF slRok == 1 THEN
      ipS := "95% interval for " + CHAR(961) + ": " + slFx(slRlo, 3) + " to " + slFx(slRhi, 3);
      slHT(slIL(ipS + " (Fisher's z)", ipS), 204, #000000h);
    ELSE
      IF slN < 4 THEN
        slHT("An interval for " + CHAR(961) + " needs at least 4 points.", 204, slGRAY);
      ELSE
        slHT("r is 1 or -1 to 12 digits, so " + CHAR(961) + " has no interval.", 204, slGRAY);
      END;
    END;
''')

# ---- help page 1: where the interval is ----
after('''    slHT("Sxy = sum (x - " + slXBAR + ")(y - " + slYBAR + ").", 182, slGRAY);
''', '''    slHT("Menu > Inference: a 95% interval for the population's r (" + CHAR(961) + ").", 198, slBLUE);
''')

os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'ScatterLab_beta2l.txt'), 'w', encoding='utf-8', newline='').write(s)
print('ScatterLab_beta2l.txt written:', len(s.split('\n')) - 1, 'lines')
