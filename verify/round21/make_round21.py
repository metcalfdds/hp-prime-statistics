#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_round21.py -- round 21 (28 Nov 2026): TTestLab beta 1n from beta 1m, by exact replacements; each old text must be
found exactly once, or the build stops.  The new routines and steps are in the r21_*.txt files beside this script.

Why: the book's read-through of its Draft 127 (item A10, which Roger accepted on 28 Nov 2026, 01:31: "You're right about
all these things--please go ahead and fix them") found that the steps that work the arithmetic out do not always check on a
calculator from the numbers they show: TTestLabG's draft lottery shows df = 13,707 / 37.81 = 362.56, and 13,707/37.81 is
362.52; 106.1^2/182 is 61.85, where its step 4 shows 61.90.  Every number was the exact value rounded to 4 significant
digits, and a step worked from rounded numbers can miss in the last digit or two.  beta 1n works each number on steps 2 and
4 out from the numbers shown before it, as a student with a calculator would, rounded to the digits it is shown with, each
result with fewer digits than what it is worked from, and takes the smallest number of digits (k, 4 to 8, for SE) at which
that chain still gives the program's own SE, df and t or z.  TTestLabG beta 1k is built from beta 1n by
tools/make_tlg1_v6.py.

Run from the repository's root:   python3 verify/round21/make_round21.py
"""
import io, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = '44652dd'                     # the commit that holds TTestLab beta 1m (git keeps it; programs/ no longer does)
NEW = os.path.join('programs', 'TTestLab_beta1n.txt')
s = subprocess.run(['git', 'show', BASE + ':programs/TTestLab_beta1m.txt'], check=True, capture_output=True).stdout.decode('utf-8')
rd = lambda n: io.open(os.path.join(HERE, n), encoding='utf-8').read()


def rep(a, b, what):
    global s
    c = s.count(a)
    if c != 1: sys.exit('BUILD STOPPED: %s: %d matches (wanted 1)' % (what, c))
    s = s.replace(a, b)


def between(a, b):
    i = s.index(a); j = s.index(b, i)
    return s[i:j]


# 1. the header: the version, and this version's line at the head of the history
rep('// TTESTLAB - beta 1m\n', '// TTESTLAB - beta 1n\n', 'title')
note = """// beta 1n (28 Nov 2026): Round 21: every step that works the arithmetic out checks on a calculator from the numbers it
//   shows (the book's read-through of its Draft 127, item A10; Roger, 28 Nov 2026: "You're right about all these
//   things--please go ahead and fix them").  beta 1m showed each number on steps 2 and 4 to 4 significant digits,
//   rounded from the exact value, so a step could miss: TTestLabG's draft lottery showed df = 13,707 / 37.81 =
//   362.56, and 13,707/37.81 is 362.52.  Now each number on those steps is worked out from the numbers shown before
//   it, as a student with a calculator would work it, rounded to the digits it is shown with, and each result has
//   fewer digits than what it is worked from; tt_Work takes the smallest k, 4 to 8 significant digits for SE, at
//   which that chain gives the program's own SE, df and t or z, so the answers are still the exact ones.  A number
//   that is exact (typed, a mean that ends, a difference of two numbers shown) is shown whole.  Step 2 of the
//   separate-variances test now writes a and b from s on lines of their own; on step 4 the t and z lines take
//   three lines, and the two-proportion test's root two, so the largest numbers the forms take still fit.  A number
//   that needs more than 11 decimals, or is 1E12 or more, is shown in the scientific form with its significant
//   digits (beta 1m showed it as 0.0000000000).  New: tt_DcK, tt_TrD, tt_WkD, tt_RdC, tt_RdK, tt_ExC, tt_Txt,
//   tt_TyD, tt_WV, tt_Dev, tt_WkAt,
//   tt_Work; changed: tt_Step2 (test 2), tt_Step4, tt_Step4N, help page 2's two lines on step 4 (tt_Help), and the
//   age-at-arrest note of tt_BookNote (it names the root as step 4 now shows it, 0.0549853).  No other routine,
//   number or word changed.
"""
rep('// beta 1m (22 Nov 2026):', note + '// beta 1m (22 Nov 2026):', 'history')

# 2. the new routines, after tt_Sig
sig = ('LOCAL tt_Sig(sv)\nBEGIN\n LOCAL sd;\n IF sv == 0 THEN RETURN "0"; END;\n sd := MIN(10, MAX(0, 3 - FLOOR(LOG(ABS(sv)))));\n'
       ' RETURN STRING(ROUND(sv,sd),2,sd);\nEND;\n')
rep(sig, sig + rd('r21_helpers.txt'), 'the chain after tt_Sig')

# 3. step 2, the separate-variances test
rep(' LOCAL sa, sb, sden;\n tt_Frame("Step 2. Distribution and df");\n', ' LOCAL sw;\n tt_Frame("Step 2. Distribution and df");\n',
    'step 2 locals')
old2 = between(' IF ttTY == 2 THEN\n  sa := ttS1^2/ttN1; sb := ttS2^2/ttN2;\n  sden := ', ' IF ttTY == 3 THEN\n  TEXTOUT_P("Dependent samples:')
rep(old2, rd('r21_step2_new.txt'), 'step 2, test 2')

# 4. step 4, and step 4 of the one-sample tests
rep(between('LOCAL tt_Step4()\n', '// ---------------- step 5: the decision ----------------'), rd('r21_step4_new.txt') + '\n', 'step 4')
rep(between('LOCAL tt_Step4N()\n', '// ---- step 5: the decision ----'), rd('r21_step4n_new.txt'), 'step 4N')

# 5. help page 2 says what step 4 does now (beta 1m: "Step 4 keeps 4 significant digits at each step; rounding sooner / can
#    change t obt (see example 1)")
rep(' TEXTOUT_P("Step 4 keeps 4 significant digits at each step; rounding sooner",G1,8,59,1,ttBLK);\n'
    ' TEXTOUT_P("can change t obt (see example 1)",G1,8,72,1,ttBLK);\n',
    ' TEXTOUT_P("Steps 2 and 4 work each number from those shown above it, so",G1,8,59,1,ttBLK);\n'
    ' TEXTOUT_P("each step checks; rounding sooner can change t obt (example 1)",G1,8,72,1,ttBLK);\n', 'help page 2')

# 6. the age-at-arrest note names the root as step 4 shows it
rep('TEXTOUT_P("The lecture rounds √0.05499 to √.05, SE to .29,",G1,8,bny,1,ttGRAY);',
    'TEXTOUT_P("The lecture rounds √0.0549853 to √.05, SE to .29,",G1,8,bny,1,ttGRAY);', 'book note')

io.open(NEW, 'w', encoding='utf-8', newline='').write(s)
print('TTestLab beta 1m -> beta 1n: %d lines' % s.count('\n'))
