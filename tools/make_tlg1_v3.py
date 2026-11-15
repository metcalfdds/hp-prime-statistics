#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_tlg1_v3.py -- builds TTestLabG beta 1h, the GENERAL version of TTestLab, from TTestLab beta 1k (the advanced
version), by exact replacements: every block must find its lines exactly once, or the build stops.

How it works (v3, 14 Nov 2026):
  1. the CODE is the advanced version's, from "// ---- shared state ----" on, renamed: EXPORT TTESTLABG, routines tz_,
     file-level variables tz (TTestLab keeps tt), so both can sit on one calculator (one pool of routine names,
     Lessons Learned s5); "beta 1k" in a comment becomes "beta 1h";
  2. then the blocks of tools/tlg1_v3_blocks.txt are applied in order.  Each block gives the advanced version's lines
     ("-"), the general version's ("+") and just enough unchanged lines (" ") to be found exactly once.  They carry
     everything that makes this the general version: separate variances by default, t critical exact for the df with
     the printed table as a note, the hand shortcut for Welch's df, "just below alpha" for a p that rounds to alpha,
     4 significant digits for numbers worked out from raw scores, no lecture references, and its own examples
     (Darwin's plants, the 1970 draft lottery, age at arrest, matched jails; then the three new ones as 5 to 7, in
     the start menu's list "Examples: one sample, z-tests", item 6 here and 5 in the advanced version);
  3. the HEADER is the general version's own: beta 1g's, from git, with this version's block and three additions.

Why v3 is not v2 with new lines: v2 built beta 1a from TTestLab beta 1c.  Rounds 5 to 12 then changed both programs
in step (commas, ranges, help pages), each by its own round script, so v2's replacements no longer find their text.
v3's first 46 blocks were made by a line diff of TTestLab beta 1j against TTestLabG beta 1g, and reproduce the one
from the other exactly (checked when they were made); 4 of them were then given beta 1k's wording, and 7 blocks were
added for beta 1k's new code.  From here on the rule is v2's again (rule 23): a fix goes into the advanced version
first, then this script builds the general one.

Run from the repository's root:   python3 tools/make_tlg1_v3.py [programs/TTestLab_beta1k.txt] [OUTDIR]
"""
import io, os, re, subprocess, sys, textwrap
BASE = '1001032'                       # the commit that holds TTestLabG beta 1g, whose header this version continues
ADV = sys.argv[1] if len(sys.argv) > 1 else os.path.join('programs', 'TTestLab_beta1k.txt')
OUT = sys.argv[2] if len(sys.argv) > 2 else 'programs'
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '// ---------------- shared state ----------------'
DATE = '14 Nov 2026'


def stop(msg): sys.exit('BUILD STOPPED: ' + msg)


adv = io.open(ADV, encoding='utf-8').read()
if '// TTESTLAB - beta 1k' not in adv: stop('%s is not TTestLab beta 1k' % ADV)
old = subprocess.run(['git', 'show', BASE + ':programs/TTestLabG_beta1g.txt'], check=True, capture_output=True).stdout.decode('utf-8')

# ---------------------------------------------------------------- 1. the code, renamed
code = adv[adv.index(MARK):]
code = code.replace('TTESTLAB', 'TTESTLABG').replace('TTestLab', 'TTestLabG').replace('tt_', 'tz_')
code = re.sub(r'\btt([A-Z0-9])', r'tz\1', code).replace('beta 1k', 'beta 1h')

# ---------------------------------------------------------------- 2. the blocks
blocks, cur = [], None
for ln in io.open(os.path.join(HERE, 'tlg1_v3_blocks.txt'), encoding='utf-8').read().split('\n'):
    if ln.startswith('@@'):
        cur = []; blocks.append((ln[2:].strip(), cur))
    elif cur is None or ln == '':
        continue                                                  # a note before the first block, or the file's last line
    elif ln[0] in ' -+':
        cur.append((ln[0], ln[1:]))
    else:
        stop('tlg1_v3_blocks.txt: a line that begins with %r' % ln[0])
for name, ls in blocks:
    a = ''.join(x + '\n' for m, x in ls if m in ' -'); b = ''.join(x + '\n' for m, x in ls if m in ' +')
    marks = ''.join(m for m, x in ls).strip(' ')
    if ' ' in marks: stop('block %s: an unchanged line between changed ones' % name)
    c = code.count(a)
    if c != 1: stop('block %s: %d matches (wanted 1) for %r' % (name, c, a[:90]))
    code = code.replace(a, b)

# ---------------------------------------------------------------- 3. the header: beta 1g's, with this version's block
hdr = old[:old.index(MARK)]


def rep(a, b):
    global hdr
    if hdr.count(a) != 1: stop('header: %d matches (wanted 1) for %r' % (hdr.count(a), a[:80]))
    hdr = hdr.replace(a, b)


rep('// TTESTLABG - beta 1g   (the general version of TTestLab)', '// TTESTLABG - beta 1h   (the general version of TTestLab)')
note = ('Round 14 (Roger, 14 Nov 2026: "go ahead and do the program work").  Built from TTestLab beta 1k by '
        'tools/make_tlg1_v3.py.  Three more tests, in the same five steps: the one-sample t-test (a sample\'s mean '
        'against mu0; from the mean, SD and N, or from scores in D1), the one-proportion z-test and the '
        'two-proportion z-test (from counts).  A z-test uses the standard normal curve: step 2 says so and checks '
        'that every count is at least 5, step 3 gives z critical, and the curve of steps 3 and 5 is the normal curve '
        '(tz_Dens).  "Choose the test" opens a short menu first, and two means go on to the flowchart (tz_Pick).  '
        'Examples 5 to 7, all from the book: Student\'s sleep data (one-sample t(9) = 4.06), the grand juries of '
        'Castaneda v. Partida (one proportion, z = -29.1) and the Rossi experiment (two proportions, z = -1.965).  '
        'Help page 3 of 3.  The three older tests are as they were: their pages, forms and numbers are beta 1g\'s, but '
        'for one line of step 5: a Cohen\'s d past 999.99 in size prints as "> 999.99" (tz_DS).  '
        'New routines, TTestLab\'s renamed: tz_SL, tz_Dens, tz_ZCrit, tz_ZP, tz_HS, tz_DS, tz_One, tz_Whole, tz_CalcN, '
        'tz_VN, tz_Par, tz_Step1N, tz_Step2N, tz_Step3Z, tz_Step4N, tz_Step5N, tz_Fam, tz_Pick, tz_AskDataN.  Gate '
        'and PC harness when written; its CHANGES file says what ran on the Virtual Calculator.')
rep('// beta 1g (9 Nov 2026):', '// beta 1h (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n// beta 1g (9 Nov 2026):')
rep('''//     arrest (JDCC, pooled) and matched jails (Census of Jails,
//     dependent).
''', '''//     arrest (JDCC, pooled) and matched jails (Census of Jails,
//     dependent).  Three more since beta 1h, each worked in the book:
//     Student's sleep data (Cushny and Peebles 1905; Student 1908:
//     one-sample t(9) = 4.06), the grand juries of Castaneda v.
//     Partida, 430 U.S. 482 (1977) (339 of 870 against p0 = 0.791:
//     z = -29.1) and the Rossi experiment (Rossi, Berk and Lenihan
//     1980: re-arrested, 48 of 216 with aid against 66 of 216
//     without: z = -1.965).
''')
rep('''//   * Dependent samples (matched pairs, before and after) from the
//     pairs in D1 and D2, or from the mean and SD of the differences.
''', '''//   * Dependent samples (matched pairs, before and after) from the
//     pairs in D1 and D2, or from the mean and SD of the differences.
//   * (beta 1h) One sample and proportions, in the same five steps: the
//     one-sample t-test (a sample's mean against mu0, the value H0
//     claims; from the mean, SD and N, or from scores in D1), the
//     one-proportion z-test and the two-proportion z-test (from counts).
//     The z-tests use the normal curve; step 2 checks that every count
//     is at least 5, the book's rule for the normal approximation.
''')
rep('''//   Cohen's d: (mean1 - mean2)/sp (independent; SPSS's Cohen's d);
//      mean(xD)/sD (dependent; SPSS's paired Cohen's d).
''', '''//   Cohen's d: (mean1 - mean2)/sp (independent; SPSS's Cohen's d);
//      mean(xD)/sD (dependent; SPSS's paired Cohen's d).
//   one sample (beta 1h): SE = s/sqrt(N), t obtained = (mean - mu0)/SE,
//      df = N - 1; Cohen's d = (mean - mu0)/s
//   one proportion: p-hat = x/n, SE = sqrt(p0(1 - p0)/n) (from p0, not
//      p-hat: the test assumes H0), z obtained = (p-hat - p0)/SE
//   two proportions: pooled p = (x1 + x2)/(n1 + n2),
//      SE = sqrt(p(1 - p)(1/n1 + 1/n2)), z obtained = (p-hat1 - p-hat2)/SE
//   z critical = -NORMALD_ICDF(0, 1, alpha) one-tailed, alpha/2 two-
//      tailed; p from NORMALD_CDF(0, 1, .), lower tails only, as for t
''')

for bad in ('tt_', 'TTESTLAB(', 'TTestLab ', 'beta 1k'):
    if bad in code: stop('%r is still in the code' % bad)
s = hdr + code
os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'TTestLabG_beta1h.txt'), 'w', encoding='utf-8', newline='').write(s)
print('TTestLab beta1k -> TTestLabG beta1h: %d blocks, %d lines' % (len(blocks), s.count('\n')))
