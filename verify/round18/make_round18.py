# -*- coding: utf-8 -*-
"""Round 18 (22 Nov 2026): every program sets the book's four Home settings when it starts, and leaves them set.

WHY.  On 22 Nov 2026 the Virtual Calculator was set to a comma as its decimal point (Home Settings, Digit Grouping
123.456,789), as a reader in Europe may have it.  STRING then writes a comma, inside a running program too, and every
program's comma routine took the decimals for a whole number: Norm3 showed 0.9772 as 0,9,772.  The two programs with no
`#pragma mode` line, NormExplorer and StudRange, stopped the calculator at Run (docs/dev/comma-decimal-mark-2026-11-22.md).
Three probes then showed that a program can assign Home's settings and that they stay set (diagnostics/SetProbe_beta1.txt,
SetOdd_beta1.txt, SetBook_beta1.txt).  Roger, the same day, asked whether each program should put the reader's own
settings back at its end or leave the book's on: "I agree that we should leave the calculator the way Statisticles sets
it--and that also helps avoid any potential mis-settings in subsequent Statisticles--we keep putting the calculator in
the mode we need it to be in".

WHAT.  One line, LINE below, at the head of every routine a person can start a program by: 31 of the 32 EXPORT routines
(EpiStats has two; CentralLimit's is empty, because an app is started by its hooks) and CentralLimit's START and Plot
hooks: 33 lines in the 31 programs.  It stands after the
routine's LOCAL lines, so that every LOCAL is still at the head.  NormExplorer and StudRange also get PRAGMA as their first
line, word for word the first line of 28 of the other 29 (StatDist's has no spaces inside its outer parentheses).  Then Round 11's bump: the header line, a history note, and the
version wherever a quoted string holds it.  Nothing else: no other statement, number, name or word on the screen.

Thirty programs are built here, each from the version before (read from git, BASE).  The thirty-first, TTestLabG, is
built from the new TTestLab by tools/make_tlg1_v5.py (the general version is always built from the advanced one), which
this script runs last.

Run from the repository's root:    python3 verify/round18/make_round18.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap

BASE = '3a121b6'                     # main before Round 18
DATE = '22 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r18_programs'
PRAGMA = '#pragma mode( separator(.,;) integer(h32) )'
LINE = 'HSeparator := 0; HFormat := 0; HAngle := 0; Entry := 0;   // Round 18: the book\'s four Home settings, left on'
HOOKS = {'CentralLimit': ('START', 'Plot')}          # an app is started by its hooks; its EXPORT routine is empty
NO_PRAGMA = ('NormExplorer', 'StudRange')
NO_HEADER = ('SampDist',)                  # its header has no line that names the version; its history notes do
# name: old version (the new one is the next letter)
OLD = {'AgreeLab': 'beta1i', 'AnovaLab': 'beta1j', 'BayesTree': 'beta8k', 'BiNorm3D': 'beta1g', 'BurrLab': 'beta1r',
       'CICatcher': 'beta2m', 'CentralLimit': 'beta3g', 'ChiTable': 'beta3m', 'DNAMixLR': 'beta3j', 'DataLoad': 'beta1g',
       'EpiStats': 'v1.7m', 'ErrorRate': 'beta1j', 'ExhibitLab': 'beta1i', 'FitCheck': 'beta1j', 'GaltonBoard': 'beta3i',
       'Norm3': 'v2.4g', 'NormExplorer': 'beta42j', 'PowerViz': 'v2.5t', 'RankLab': 'beta1k', 'ResampLab': 'beta1j',
       'RiskLab': 'beta1h', 'SampDist': 'v2.3k', 'ScatterLab': 'beta2m', 'StatDist': 'v2.7n', 'StudRange': 'beta15n',
       'SurvLab': 'beta1g', 'TDist3D': 'beta1b', 'TTestLab': 'beta1l', 'TestChooser': 'beta2h', 'TrendTest': 'beta3n'}
GENERAL = ('TTestLabG', 'beta1i')    # built last, by tools/make_tlg1_v5.py


def nxt(v):
    if v[-1] == 'z' or not v[-1].isalpha():
        die('no next letter after ' + v)
    return v[:-1] + chr(ord(v[-1]) + 1)


def tag(v):
    return v.replace('beta', 'beta ')


def die(msg):
    sys.exit('BUILD STOPPED: ' + msg)


def split_comment(line):
    """(code, comment): the line cut at the first // that is outside a quoted string"""
    q = False
    for i, ch in enumerate(line):
        if ch == '"':
            q = not q
        elif not q and line[i:i + 2] == '//':
            return line[:i], line[i:]
    return line, ''


def heads(name, L):
    """the line numbers (from 0) of the heads of the routines a person starts the program by"""
    hs = [i for i, l in enumerate(L) if re.match(r'^\s*EXPORT\s+\w+\s*\(', l)]
    for h in HOOKS.get(name, ()):
        at = [i for i, l in enumerate(L) if re.match(r'^\s*%s\s*\(\s*\)\s*$' % h, l)]
        if len(at) != 1:
            die('%s: %d heads for the hook %s' % (name, len(at), h))
        hs += at
    return sorted(hs)


def insert_line(name, s):
    """LINE after the LOCAL lines at the head of each start routine; returns the text and the routines' names"""
    L = s.split('\n')
    done = []
    for h in reversed(heads(name, L)):
        rname = re.search(r'(\w+)\s*\(', L[h].replace('EXPORT', '')).group(1)
        j = h + 1
        while L[j].strip() == '':
            j += 1
        if L[j].strip() != 'BEGIN':
            die('%s: no BEGIN under %s' % (name, L[h].strip()))
        ins, k = j + 1, j + 1
        while True:
            code = split_comment(L[k])[0].strip()
            if code == '':
                k += 1                                  # a blank line or a comment: look past it
            elif re.match(r'LOCAL\b', code):
                while not split_comment(L[k])[0].rstrip().endswith(';'):
                    k += 1                              # a LOCAL statement that runs over several lines
                k += 1
                ins = k
            else:
                break
        nxt_code = L[k]
        indent = re.match(r'\s*', nxt_code).group(0) if nxt_code.strip() != 'END;' else re.match(r'\s*', nxt_code).group(0) + '  '
        if name == 'CentralLimit' and rname == 'CentralLimit':
            continue                                    # the app's EXPORT routine is empty and never runs a page
        L.insert(ins, indent + LINE)
        done.append(rname)
    if not done:
        die(name + ': no start routine')
    return '\n'.join(L), list(reversed(done))


def bump(name, s, ov, nv, note):
    """Round 11's bump: the header line, a history note before the old version's, and every version string in a literal."""
    ot, nt = tag(ov), tag(nv)
    L = s.split('\n')
    hv = None
    for i, l in enumerate(L[:40]):
        if re.match(r'^//\s*[A-Za-z0-9 ]+ - ' + re.escape(ot) + r'\b', l):
            hv = i
            break
    if hv is None and name not in NO_HEADER:
        die(name + ': no header line for ' + ot)
    if hv is not None:
        L[hv] = L[hv].replace(ot, nt)
        L[hv] = re.sub(r'\((\d+ Nov 2026[^)]*)\)', '(%s)' % DATE, L[hv], count=1)
    hist = [i for i, l in enumerate(L) if re.match(r'^//\s*' + re.escape(ot) + r'\s*\(', l)]
    if not hist:
        die(name + ': no history line for ' + ot)
    L.insert(hist[0], '// %s (%s): ' % (nt, DATE) + '\n//   '.join(textwrap.wrap(note, 100)))
    s = '\n'.join(L)
    s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace(ot, nt).replace(ov, nv), s)
    # a version on screen with its date: the new date (Round 11's bump did the same)
    s = re.sub(r'"[^"\n]*%s[^"\n]*"' % re.escape(nt), lambda m: re.sub(r'\b\d{1,2} Nov 2026', DATE, m.group(0)), s)
    return s


def note_for(name, routines):
    where = ' and '.join(r + '()' for r in routines)
    t = ('Round 18: the program sets the four Home settings that the book\'s examples assume when it starts, and leaves '
         'them set: HSeparator := 0 (Digit Grouping 123,456.789, the period as the decimal point), HFormat := 0 (Number '
         'Format Standard), HAngle := 0 (Radians) and Entry := 0 (Textbook).  Roger, 22 Nov 2026: "we keep putting the '
         'calculator in the mode we need it to be in".  With a comma as Home\'s decimal mark STRING writes a comma, and '
         'the comma routine then put commas into the decimals (the Virtual Calculator, 22 Nov 2026).  ')
    if name in NO_PRAGMA:
        t += ('The first line, #pragma mode( separator(.,;) integer(h32) ), is new as well: the other 29 programs have it, '
              'and without it this program stopped the Virtual Calculator at Run when Home\'s decimal mark was a comma.  ')
    t += ('One line at the head of %s; no other statement, number, name or word on the screen changed, only the '
          'version.' % where)
    return t


def old_text(name, ov):
    return subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (BASE, name, ov)], check=True,
                          capture_output=True).stdout.decode('utf-8')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, ov in OLD.items():
        nv = nxt(ov)
        s = old_text(name, ov)
        s, routines = insert_line(name, s)
        if name in NO_PRAGMA:
            if s.startswith('#pragma'):
                die(name + ' has a pragma line already')
            s = PRAGMA + '\n' + s
        elif not re.match(r'#pragma mode\(\s*separator\(\.,;\) integer\(h32\)\s*\)\n', s):
            die(name + ': the first line is not the pragma line')
        s = bump(name, s, ov, nv, note_for(name, routines))
        io.open(os.path.join(OUT, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8', newline='').write(s)
        print('%-12s %s -> %s  %s%s' % (name, ov, nv, ', '.join(routines), '  + pragma' if name in NO_PRAGMA else ''))
    here = os.path.dirname(os.path.abspath(__file__))
    adv = os.path.join(OUT, 'TTestLab_%s.txt' % nxt(OLD['TTestLab']))
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.dirname(here)), 'tools', 'make_tlg1_v5.py'),
                        adv, OUT], capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode:
        die('tools/make_tlg1_v5.py: ' + (r.stderr or r.stdout).strip()[-300:])
