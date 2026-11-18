# -*- coding: utf-8 -*-
"""count_lines_r17.py [COMMIT] -- the fleet's lines, as the README's sentence gives them ("more than 95,000 lines: ... of PPL
code, ... of MicroPython (in five of them), and ... lines of comments").  Without an argument it reads programs/*.txt; with a
commit it reads that commit's programs/ from git, so the sentence can be checked against the numbers it gave before.
A line is: MicroPython (every line between #PYTHON and #END, its comments and blank lines too; the two markers themselves
are PPL); or, outside those blocks, blank, a comment (a line that begins with //) or PPL code (every other line; a line of
code with a comment after it is code).  On the commit before round 17 (39bb935) this gives 64,210, 1,156 and 26,417, which
the README rounded to 64,200, 1,160 and 26,400.
Run from the repository's root."""
import sys, glob, io, subprocess, os, re
def texts():
    if len(sys.argv) > 1:
        names = subprocess.run(['git', 'ls-tree', '--name-only', sys.argv[1], 'programs/'], capture_output=True, text=True).stdout.split()
        for n in names:
            if n.endswith('.txt'):
                yield os.path.basename(n), subprocess.run(['git', 'show', sys.argv[1] + ':' + n], capture_output=True, text=True).stdout
    else:
        for f in sorted(glob.glob('programs/*.txt')):
            yield os.path.basename(f), io.open(f, encoding='utf-8').read()
T = dict(total=0, blank=0, comment=0, python=0, ppl=0); withpy = 0; n = 0
for name, s in texts():
    n += 1; py = False; haspy = False
    lines = s.split('\n')
    if lines and lines[-1] == '': lines.pop()
    for l in lines:
        t = l.strip(); T['total'] += 1
        if re.match(r'#PYTHON\b', t): py = True; haspy = True; T['ppl'] += 1; continue
        if py and re.match(r'#END\b', t): py = False; T['ppl'] += 1; continue
        if py: T['python'] += 1
        elif not t: T['blank'] += 1
        else: T['comment' if t.startswith('//') else 'ppl'] += 1
    withpy += haspy
print('%d programs%s: %s lines; PPL code %s; MicroPython %s (in %d programs); comments %s; blank lines outside the MicroPython %s' % (
    n, ' at ' + sys.argv[1] if len(sys.argv) > 1 else '', '{:,}'.format(T['total']), '{:,}'.format(T['ppl']), '{:,}'.format(T['python']), withpy,
    '{:,}'.format(T['comment']), '{:,}'.format(T['blank'])))
