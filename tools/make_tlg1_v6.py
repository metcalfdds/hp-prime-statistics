#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_tlg1_v6.py -- builds TTestLabG beta 1k, the GENERAL version of TTestLab, from TTestLab beta 1n (the advanced
version), by exact replacements: every block must find its lines exactly once, or the build stops.

v6 (Round 21, 28 Nov 2026) is v5 for the next pair of versions.  Round 21 made every step that works the arithmetic out
check from the numbers it shows (the book's read-through of its Draft 127, item A10), so:
  1. the CODE is the advanced version's, from "// ---- shared state ----" on, renamed as before: EXPORT TTESTLABG,
     routines tz_, file-level variables tz; "beta 1k" (the advanced version that brought the one-sample tests) still
     becomes "beta 1h", and then the advanced "beta 1n" and "beta 1m", which round 21's comments name, become this
     version's own "beta 1k" and "beta 1j";
  2. then the blocks of tools/tlg1_v6_blocks.txt are applied in order: v5's, with blocks 15, 16 and 42 in round 21's
     lines and blocks 27 to 29 gone (their notes say why);
  3. the HEADER is the general version's own: beta 1j's, from git, with this version's line and history note.

How the blocks came to be, and why the general version is always built from the advanced one: make_tlg1_v3.py to
make_tlg1_v5.py, which left tools/ with their versions (git keeps them), and the row for this script in tools/README.md.

Run from the repository's root:   python3 tools/make_tlg1_v6.py [programs/TTestLab_beta1n.txt] [OUTDIR]
"""
import io, os, re, subprocess, sys, textwrap
BASE = '44652dd'                       # the commit that holds TTestLabG beta 1j, whose header this version continues
ADV = sys.argv[1] if len(sys.argv) > 1 else os.path.join('programs', 'TTestLab_beta1n.txt')
OUT = sys.argv[2] if len(sys.argv) > 2 else 'programs'
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '// ---------------- shared state ----------------'
DATE = '28 Nov 2026'


def stop(msg): sys.exit('BUILD STOPPED: ' + msg)


adv = io.open(ADV, encoding='utf-8').read()
if '// TTESTLAB - beta 1n' not in adv: stop('%s is not TTestLab beta 1n' % ADV)
old = subprocess.run(['git', 'show', BASE + ':programs/TTestLabG_beta1j.txt'], check=True, capture_output=True).stdout.decode('utf-8')

# ---------------------------------------------------------------- 1. the code, renamed
code = adv[adv.index(MARK):]
code = code.replace('TTESTLAB', 'TTESTLABG').replace('TTestLab', 'TTestLabG').replace('tt_', 'tz_')
code = re.sub(r'\btt([A-Z0-9])', r'tz\1', code).replace('beta 1k', 'beta 1h')
code = code.replace('beta 1n', 'beta 1k').replace('beta 1m', 'beta 1j')

# ---------------------------------------------------------------- 2. the blocks
blocks, cur = [], None
for ln in io.open(os.path.join(HERE, 'tlg1_v6_blocks.txt'), encoding='utf-8').read().split('\n'):
    if ln.startswith('@@'):
        cur = []; blocks.append((ln[2:].strip(), cur))
    elif cur is None or ln == '':
        continue                                                  # a note before the first block, or the file's last line
    elif ln[0] in ' -+':
        cur.append((ln[0], ln[1:]))
    else:
        stop('tlg1_v6_blocks.txt: a line that begins with %r' % ln[0])
for name, ls in blocks:
    a = ''.join(x + '\n' for m, x in ls if m in ' -'); b = ''.join(x + '\n' for m, x in ls if m in ' +')
    marks = ''.join(m for m, x in ls).strip(' ')
    if ' ' in marks: stop('block %s: an unchanged line between changed ones' % name)
    c = code.count(a)
    if c != 1: stop('block %s: %d matches (wanted 1) for %r' % (name, c, a[:90]))
    code = code.replace(a, b)

# ---------------------------------------------------------------- 3. the header: beta 1j's, with this version's block
hdr = old[:old.index(MARK)]


def rep(a, b):
    global hdr
    if hdr.count(a) != 1: stop('header: %d matches (wanted 1) for %r' % (hdr.count(a), a[:80]))
    hdr = hdr.replace(a, b)


rep('// TTESTLABG - beta 1j   (the general version of TTestLab)', '// TTESTLABG - beta 1k   (the general version of TTestLab)')
note = ('Round 21: every step that works the arithmetic out checks on a calculator from the numbers it shows (the '
        'book\'s read-through of its Draft 127, item A10; Roger, 28 Nov 2026: "You\'re right about all these things--'
        'please go ahead and fix them").  beta 1j showed each number on steps 2 and 4 to 4 significant digits, rounded from '
        'the exact value, so a step could miss: the draft lottery showed df = 13,707 / 37.81 = 362.56, and 13,707/37.81 is '
        '362.52.  Now each number on those steps is worked out from the numbers shown before it, as a student with a '
        'calculator would work it, rounded to the digits it is shown with, and each result has fewer digits than what it '
        'is worked from; tz_Work takes the smallest k, 4 to 8 significant digits for SE, at which that chain gives the '
        'program\'s own SE, df and t or z, so the answers are still the exact ones.  Step 2 of the separate-variances test '
        'writes a and b from s on lines of their own; on step 4 the t and z lines take three lines, and the two-proportion '
        'test\'s root two, so the largest numbers the forms take still fit; a number that needs more than 11 decimals, or '
        'is 1E12 or more, is shown in the scientific '
        'form (beta 1j showed it as 0.0000000000); help page 2 says what steps 2 and 4 do.  Built from TTestLab beta 1n by '
        'tools/make_tlg1_v6.py; no other routine, number or word changed.')
old_hist = re.search(r'^// beta 1j \([^)]*\):', hdr, re.M).group(0)
rep(old_hist, '// beta 1k (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n' + old_hist)

for bad in ('tt_', 'TTESTLAB(', 'TTestLab ', 'beta 1n', 'beta 1m', 'beta 1l'):
    if bad in code: stop('%r is still in the code' % bad)
s = hdr + code
os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'TTestLabG_beta1k.txt'), 'w', encoding='utf-8', newline='').write(s)
print('TTestLab beta1n -> TTestLabG beta1k: %d blocks, %d lines' % (len(blocks), s.count('\n')))
