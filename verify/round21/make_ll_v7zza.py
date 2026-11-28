#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_ll_v7zza.py -- round 21 (28 Nov 2026): Lessons Learned v7zza from v7zz, by exact replacements (each old text must
stand exactly once, or the build stops).  What it adds: the "What changed in v7zza" block at the top; in section 3 a bullet
on how ROUND rounds a tie and how many digits the Virtual Calculator held; in section 13 the house rule that a worked step
checks from the numbers it shows; in section 15 the new set's line and the rows of TTestLab, TTestLabG and DataLoad (whose
beta 1i, of round 20, was not yet in the table).  Then it removes v7zz (git keeps it).

Run from the repository's root:   python3 verify/round21/make_ll_v7zza.py
"""
import io, os, sys
OLD, NEW = 'docs/lessons-learned_v7zz.md', 'docs/lessons-learned_v7zza.md'
s = io.open(OLD, encoding='utf-8', newline='').read()


def rep(a, b, what):
    global s
    c = s.count(a)
    if c != 1: sys.exit('BUILD STOPPED: %s: %d matches (wanted 1)' % (what, c))
    s = s.replace(a, b)


rep('*Roger Metcalf & Claude · v7zz · 23 November 2026, a CAS integral that does not end, the smallest person-time, and an app\'s own angle setting (v7zy ',
    '*Roger Metcalf & Claude · v7zza · 28 November 2026, a worked step that checks on a calculator, and a tie that ROUND rounds away from zero (v7zz '
    '23 November 2026, a CAS integral that does not end, the smallest person-time, and an app\'s own angle setting; v7zy ', 'the title line')

block = """**What changed in v7zza** (28 Nov 2026; round 21, `verify/round21/README.md`):

- **A step that works the arithmetic out must check on a calculator from the numbers it shows** (§13). TTestLab and TTestLabG showed every number on steps 2 and 4 as the exact value rounded to 4 significant digits, and a line worked from rounded numbers can miss in its last digit or two: the draft lottery's step 2 said df = 13,707 / 37.81 = 362.56, and 13,707/37.81 is 362.52; the age-at-arrest example's step 4 said 1.321 × 0.2345 = 0.3097, and that product is 0.30977. The book's read-through of its Draft 127 found the first (its item A10). TTestLab beta 1n and TTestLabG beta 1k work each number out from the numbers shown before it, rounded to its own digits, each result with fewer significant digits than what it is worked from, and take the fewest digits (4 to 8 for SE) at which that chain still gives the exact SE, df and t: 13,707 / 37.806 = 362.56, and 1.3209 × 0.23449 = 0.3097. Their verify scripts read every relation off the screen and work it in exact decimal arithmetic, rounded half away from zero, for every example and 1,759 random cases. Where even 8 digits do not give the exact t (7 of the 1,759, each a t of 100,000 or more), every line still checks, and step 4's t can differ from step 5's in its last decimals.
- **A number no student can see on a page must not feed a line that is on it** (§13). The first chain worked Welch's numerator, (a + b)², from the sum that step 4 shows, which step 4 rounds when it has too many digits; step 2, where the numerator stands, shows only a and b, and a student working from them got 0.00000288436 where the screen said 0.00000288437. It is worked from a and b now.
- **A worked line grows with the digits the chain needs, so lay it out for the largest numbers the forms take** (§6). The monkey found the two-proportion test's root past the screen's edge, its line holding a pooled p of 10 decimals (0.0000759837), its complement and the two n; the t and z lines now take three lines, and the pooled p and its root two each, and part D of the verify scripts draws every step with means of ±9,999.99999, two n of 1,000,000 and a pooled p below 0.0001.
- **`ROUND` rounds the decimal the calculator holds, and a tie away from zero** (§3; Virtual Calculator 2.4.2, 28 Nov 2026, `diagnostics/RoundProbe_beta1a.txt`). 162.45/10 is 16.245 and ROUND(162.45/10, 2) is 16.25; ROUND(0.125, 2) is 0.13, ROUND(2.5, 0) 3, ROUND(−2.5, 0) −3 and ROUND(16.245, −4) 16.25. The PC harness's binary floats hold 162.45/10 as 16.244999999999997, and its ROUND gave 16.24, so a one-sample step 4 with s = 162.45 and N = 100 showed SE = 16.24 there against a student's 16.25. `tools/prime_facts_v1.py` fact 8 models it.
- **The Virtual Calculator held more digits than the 12 it shows** (§3; the same probe). (1 + 1E−12) − 1 to (1 + 1E−15) − 1 gave 1E−12 to 1E−15; 123101.0078125 − 123101 gave 0.0078125; and (0.0078125 + 123101)², which STRING showed as 15153858124.5, rounded to 15153858124, so the value it held was below the half. The harness's binary arithmetic gives (1 + 1E−12) − 1 = 1.00008890058E−12, and that is not modelled. Not tried on a G1 or a G2, nor for the distribution functions, whose far tails the rest of §3 still treats as 12 digits.

"""
rep('**What changed in v7zz** (23 Nov 2026; round 19, `verify/round19/README.md`):', block + '**What changed in v7zz** (23 Nov 2026; round 19, `verify/round19/README.md`):',
    'the new block')

sec3 = ("- **`ROUND` rounds the decimal it holds, and a tie away from zero; + and − keep more digits than the 12 shown** (Virtual "
        "Calculator 2.4.2, 28 Nov 2026; v7zza; `diagnostics/RoundProbe_beta1a.txt`). ROUND(162.45/10, 2) = 16.25, ROUND(0.125, 2) = "
        "0.13, ROUND(−2.5, 0) = −3, ROUND(16.245, −4) = 16.25; (1 + 1E−15) − 1 = 1E−15. The PC harness models the first "
        "(`tools/prime_facts_v1.py` fact 8: its binary floats had put 162.45/10 just below the tie), not the second. Not tried on "
        "a G1 or a G2.\n")
rep('- **Alternating sums cancel; build probabilities from positive terms** (DNAMixLR beta 3c, 19 Oct 2026).',
    sec3 + '- **Alternating sums cancel; build probabilities from positive terms** (DNAMixLR beta 3c, 19 Oct 2026).', 'section 3')

rep('**Means and SDs worked out from raw scores print to 4 significant digits; typed values print as typed** (v7ze).',
    '**Means and SDs worked out from raw scores print to 4 significant digits; typed values print as typed** (v7ze). On a step '
    'that works with them they carry the digits the next line needs: TTestLabG\'s draft lottery shows 206.3 on step 1 and '
    '206.3242 on step 4 (v7zza).\n\n'
    '**A step that works the arithmetic out checks on a calculator from the numbers it shows** (v7zza; round 21). Each number is '
    'worked out from the numbers shown before it, as a student with a calculator works it, and rounded half away from zero to '
    'the digits it is shown with; each result has fewer significant digits than what it is worked from; a number that is exact '
    '(typed, a mean that ends, the sum or difference of two numbers shown) is shown whole; and the fewest digits are taken at '
    'which the chain still gives the exact answers. No line is fed by a number that is not on its page. The verify script reads '
    'every relation off the screen and works it in exact decimal arithmetic (TTestLab beta 1n\'s, part C).', 'section 13')

rep('**One current set, 23 November 2026** (round 19: StatDist v2.7p and EpiStats v1.7o; round 18, 22 November, gave all 31 a new letter). Before that, ',
    '**One current set, 28 November 2026** (round 21: TTestLab beta 1n and TTestLabG beta 1k; round 20, 27 November: DataLoad '
    'beta 1i). Before that, **one current set, 23 November 2026** (round 19: StatDist v2.7p and EpiStats v1.7o; round 18, 22 '
    'November, gave all 31 a new letter). Before that, ', 'section 15, the set')

rep('| **TTestLab** | beta 1m | **22 Nov (round 18):**',
    '| **TTestLab** | beta 1n | **28 Nov (round 21):** every number on steps 2 and 4 is worked out from the numbers shown before '
    'it, so each step checks on a calculator (12 new routines, `tt_DcK` to `tt_Work`); the t and z lines take three lines. '
    'Virtual Calculator: Check clean; the age-at-arrest example\'s step 4 run and read. **22 Nov (round 18):**', 'the TTestLab row')
rep('| **TTestLabG** | beta 1j | **22 Nov (round 18):**',
    '| **TTestLabG** | beta 1k | **28 Nov (round 21):** TTestLab beta 1n\'s steps 2 and 4, built from it by `tools/make_tlg1_v6.py`. '
    'Virtual Calculator: Check clean; the draft lottery\'s steps 2 and 4 run and read. **22 Nov (round 18):**', 'the TTestLabG row')
rep('| **DataLoad** | beta 1h | **22 Nov (round 18):**',
    '| **DataLoad** | beta 1i | **27 Nov (round 20):** when it loads two or more columns and a blank cell stands above a value in '
    'any of them, it asks whether the columns are pairs (complete rows only) or separate groups (`verify/round20/README.md`). '
    '**22 Nov (round 18):**', 'the DataLoad row')

io.open(NEW, 'w', encoding='utf-8', newline='').write(s)
os.remove(OLD)
print('Lessons Learned v7zz -> v7zza: %d lines' % s.count('\n'))
