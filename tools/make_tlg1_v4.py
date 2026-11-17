#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_tlg1_v4.py -- builds TTestLabG beta 1i, the GENERAL version of TTestLab, from TTestLab beta 1l (the advanced
version), by exact replacements: every block must find its lines exactly once, or the build stops.

v4 (Round 17, 17 Nov 2026) is v3 for the next pair of versions.  Round 17 changed words on the screen only (the book's
two rules for a statistic's letter: "df = (N - 1)", "t-table"), so:
  1. the CODE is the advanced version's, from "// ---- shared state ----" on, renamed as before: EXPORT TTESTLABG,
     routines tz_, file-level variables tz; "beta 1k" in a comment still becomes "beta 1h" (those comments say when a
     thing came into each program, and beta 1l added no comment to the code);
  2. then the blocks of tools/tlg1_v4_blocks.txt are applied in order: v3's blocks, two lines of which carry this
     round's words (the file's note says which).  The lines the two programs share ("Pooled variances:  df = (N1 + N2
     - 2)", "One sample:  df = (N - 1)", help 3 of 3) come over from the advanced version with the code;
  3. the HEADER is the general version's own: beta 1h's, from git, with this version's line and history note.

How the blocks came to be, and why the general version is always built from the advanced one: make_tlg1_v3.py, which
left tools/ with this version (git keeps it: `git show 39bb935:tools/make_tlg1_v3.py`), and the row for this script in
tools/README.md.

Run from the repository's root:   python3 tools/make_tlg1_v4.py [programs/TTestLab_beta1l.txt] [OUTDIR]
"""
import io, os, re, subprocess, sys, textwrap
BASE = '39bb935'                       # the commit that holds TTestLabG beta 1h, whose header this version continues
ADV = sys.argv[1] if len(sys.argv) > 1 else os.path.join('programs', 'TTestLab_beta1l.txt')
OUT = sys.argv[2] if len(sys.argv) > 2 else 'programs'
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '// ---------------- shared state ----------------'
DATE = '17 Nov 2026'


def stop(msg): sys.exit('BUILD STOPPED: ' + msg)


adv = io.open(ADV, encoding='utf-8').read()
if '// TTESTLAB - beta 1l' not in adv: stop('%s is not TTestLab beta 1l' % ADV)
old = subprocess.run(['git', 'show', BASE + ':programs/TTestLabG_beta1h.txt'], check=True, capture_output=True).stdout.decode('utf-8')

# ---------------------------------------------------------------- 1. the code, renamed
code = adv[adv.index(MARK):]
code = code.replace('TTESTLAB', 'TTESTLABG').replace('TTestLab', 'TTestLabG').replace('tt_', 'tz_')
code = re.sub(r'\btt([A-Z0-9])', r'tz\1', code).replace('beta 1k', 'beta 1h')

# ---------------------------------------------------------------- 2. the blocks
blocks, cur = [], None
for ln in io.open(os.path.join(HERE, 'tlg1_v4_blocks.txt'), encoding='utf-8').read().split('\n'):
    if ln.startswith('@@'):
        cur = []; blocks.append((ln[2:].strip(), cur))
    elif cur is None or ln == '':
        continue                                                  # a note before the first block, or the file's last line
    elif ln[0] in ' -+':
        cur.append((ln[0], ln[1:]))
    else:
        stop('tlg1_v4_blocks.txt: a line that begins with %r' % ln[0])
for name, ls in blocks:
    a = ''.join(x + '\n' for m, x in ls if m in ' -'); b = ''.join(x + '\n' for m, x in ls if m in ' +')
    marks = ''.join(m for m, x in ls).strip(' ')
    if ' ' in marks: stop('block %s: an unchanged line between changed ones' % name)
    c = code.count(a)
    if c != 1: stop('block %s: %d matches (wanted 1) for %r' % (name, c, a[:90]))
    code = code.replace(a, b)

# ---------------------------------------------------------------- 3. the header: beta 1h's, with this version's block
hdr = old[:old.index(MARK)]


def rep(a, b):
    global hdr
    if hdr.count(a) != 1: stop('header: %d matches (wanted 1) for %r' % (hdr.count(a), a[:80]))
    hdr = hdr.replace(a, b)


rep('// TTESTLABG - beta 1h   (the general version of TTestLab)', '// TTESTLABG - beta 1i   (the general version of TTestLab)')
note = ('Round 17: the screen text follows the book\'s two rules for a statistic\'s letter as far as a screen can '
        '(Roger, 17 Nov 2026: "The p-value and t-test, t-distribution etc should be hyphenated and italicized"; '
        '"make sure expressions like n-1 are in parentheses").  Built from TTestLab beta 1l by tools/make_tlg1_v4.py.  '
        'Step 2 writes "Pooled variances:  df = (N1 + N2 - 2)", "One sample:  df = (N - 1)" and, for separate '
        'variances, "By hand: df = the smaller of (N1-1), (N2-1) = ..."; help 3 of 3 says "df = (N - 1)" (they said '
        '"df = N1 + N2 - 2", "df = N - 1", "the smaller of N1-1, N2-1").  Only text inside quotation marks changed, '
        'and the version: no statement, number or name.  tools/screen_text_v1.py is the check.')
rep('// beta 1h (14 Nov 2026):', '// beta 1i (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n// beta 1h (14 Nov 2026):')

for bad in ('tt_', 'TTESTLAB(', 'TTestLab ', 'beta 1k'):
    if bad in code: stop('%r is still in the code' % bad)
s = hdr + code
os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'TTestLabG_beta1i.txt'), 'w', encoding='utf-8', newline='').write(s)
print('TTestLab beta1l -> TTestLabG beta1i: %d blocks, %d lines' % (len(blocks), s.count('\n')))
