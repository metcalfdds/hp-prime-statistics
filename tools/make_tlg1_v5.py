#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_tlg1_v5.py -- builds TTestLabG beta 1j, the GENERAL version of TTestLab, from TTestLab beta 1m (the advanced
version), by exact replacements: every block must find its lines exactly once, or the build stops.

v5 (Round 18, 22 Nov 2026) is v4 for the next pair of versions.  Round 18 put one line at the head of each program's
start routine (the book's four Home settings, left on), so:
  1. the CODE is the advanced version's, from "// ---- shared state ----" on, renamed as before: EXPORT TTESTLABG,
     routines tz_, file-level variables tz; "beta 1k" in a comment still becomes "beta 1h" (those comments say when a
     thing came into each program; betas 1l and 1m added no comment that names a version).  The new line comes over
     with the code;
  2. then the blocks of tools/tlg1_v5_blocks.txt are applied in order: they are v4's blocks, unchanged;
  3. the HEADER is the general version's own: beta 1i's, from git, with this version's line and history note.

How the blocks came to be, and why the general version is always built from the advanced one: make_tlg1_v3.py and
make_tlg1_v4.py, which left tools/ with their versions (git keeps them: `git show 3a121b6:tools/make_tlg1_v4.py`), and
the row for this script in tools/README.md.

Run from the repository's root:   python3 tools/make_tlg1_v5.py [programs/TTestLab_beta1m.txt] [OUTDIR]
"""
import io, os, re, subprocess, sys, textwrap
BASE = '3a121b6'                       # the commit that holds TTestLabG beta 1i, whose header this version continues
ADV = sys.argv[1] if len(sys.argv) > 1 else os.path.join('programs', 'TTestLab_beta1m.txt')
OUT = sys.argv[2] if len(sys.argv) > 2 else 'programs'
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '// ---------------- shared state ----------------'
DATE = '22 Nov 2026'


def stop(msg): sys.exit('BUILD STOPPED: ' + msg)


adv = io.open(ADV, encoding='utf-8').read()
if '// TTESTLAB - beta 1m' not in adv: stop('%s is not TTestLab beta 1m' % ADV)
old = subprocess.run(['git', 'show', BASE + ':programs/TTestLabG_beta1i.txt'], check=True, capture_output=True).stdout.decode('utf-8')

# ---------------------------------------------------------------- 1. the code, renamed
code = adv[adv.index(MARK):]
code = code.replace('TTESTLAB', 'TTESTLABG').replace('TTestLab', 'TTestLabG').replace('tt_', 'tz_')
code = re.sub(r'\btt([A-Z0-9])', r'tz\1', code).replace('beta 1k', 'beta 1h')

# ---------------------------------------------------------------- 2. the blocks
blocks, cur = [], None
for ln in io.open(os.path.join(HERE, 'tlg1_v5_blocks.txt'), encoding='utf-8').read().split('\n'):
    if ln.startswith('@@'):
        cur = []; blocks.append((ln[2:].strip(), cur))
    elif cur is None or ln == '':
        continue                                                  # a note before the first block, or the file's last line
    elif ln[0] in ' -+':
        cur.append((ln[0], ln[1:]))
    else:
        stop('tlg1_v5_blocks.txt: a line that begins with %r' % ln[0])
for name, ls in blocks:
    a = ''.join(x + '\n' for m, x in ls if m in ' -'); b = ''.join(x + '\n' for m, x in ls if m in ' +')
    marks = ''.join(m for m, x in ls).strip(' ')
    if ' ' in marks: stop('block %s: an unchanged line between changed ones' % name)
    c = code.count(a)
    if c != 1: stop('block %s: %d matches (wanted 1) for %r' % (name, c, a[:90]))
    code = code.replace(a, b)

# ---------------------------------------------------------------- 3. the header: beta 1i's, with this version's block
hdr = old[:old.index(MARK)]


def rep(a, b):
    global hdr
    if hdr.count(a) != 1: stop('header: %d matches (wanted 1) for %r' % (hdr.count(a), a[:80]))
    hdr = hdr.replace(a, b)


rep('// TTESTLABG - beta 1i   (the general version of TTestLab)', '// TTESTLABG - beta 1j   (the general version of TTestLab)')
note = ('Round 18: the program sets the four Home settings that the book\'s examples assume when it starts, and leaves '
        'them set: HSeparator := 0 (Digit Grouping 123,456.789, the period as the decimal point), HFormat := 0 (Number '
        'Format Standard), HAngle := 0 (Radians) and Entry := 0 (Textbook).  Roger, 22 Nov 2026: "we keep putting the '
        'calculator in the mode we need it to be in".  With a comma as Home\'s decimal mark STRING writes a comma, and '
        'the comma routine then put commas into the decimals (the Virtual Calculator, 22 Nov 2026).  Built from TTestLab '
        'beta 1m by tools/make_tlg1_v5.py.  One line at the head of TTESTLABG(); no other statement, number, name or '
        'word on the screen changed, only the version.')
old_hist = re.search(r'^// beta 1i \([^)]*\):', hdr, re.M).group(0)
rep(old_hist, '// beta 1j (%s): ' % DATE + '\n//   '.join(textwrap.wrap(note, 100)) + '\n' + old_hist)

for bad in ('tt_', 'TTESTLAB(', 'TTestLab ', 'beta 1k'):
    if bad in code: stop('%r is still in the code' % bad)
s = hdr + code
os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, 'TTestLabG_beta1j.txt'), 'w', encoding='utf-8', newline='').write(s)
print('TTestLab beta1m -> TTestLabG beta1j: %d blocks, %d lines' % (len(blocks), s.count('\n')))
