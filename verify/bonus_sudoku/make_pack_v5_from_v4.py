# Builds tools/make_starter_pack_v5.py from v4 by exact replacements (26 Nov 2026): the bonus program (Sudoku, extras/sudoku/).
# v4 is read from git (BASE, main before the bonus), and v5 is written into this repository's tools/; in a shallow
# clone, deepen it first (git fetch --deepen=50 origin main).  Run from anywhere.
import io, os, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = os.path.join(REPO, 'tools', '')
BASE = '8483e62'                     # main before the bonus (PR 34 merged)
s = subprocess.run(['git', 'show', BASE + ':tools/make_starter_pack_v4.py'], check=True, capture_output=True,
                   cwd=REPO).stdout.decode('utf-8')
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:70]); s = s.replace(old, new)
rep('"""make_starter_pack_v4.py -- builds the Virtual Calculator starter pack from programs/ (1 Nov 2026).\n',
    '"""make_starter_pack_v5.py -- builds the Virtual Calculator starter pack from programs/ (1 Nov 2026), and the bonus.\n\n'
    'v5 (26 Nov 2026): THE BONUS.  The pack also carries the programs of BONUS (below), folders of extras/ that each hold\n'
    'one <Name>_beta*.txt or <Name>_v*.txt, in a folder of their own, "Bonus (optional)/<Name>.hpprgm", beside the\n'
    'sample data: Sudoku, the book\'s just-for-fun program of Appendix G (Roger, 26 Nov 2026: "maybe add this as a\n'
    'bonus--"just for fun""; his choice of the Prime Loader\'s "More choices" for it, with the 31 Statisticles staying\n'
    'the Population).  A bonus program is built, read back and, with --checked, taken checked exactly as a program is\n'
    '(its checked file is <Name>.hpprgm in DIR beside the others), and its names join the pool that the name check\n'
    'reads, so that it can never clash with a Statisticle on the calculator; it is not in "Copy these into Prime",\n'
    'which stays the 31.  The instructions say what the folder is.\n')
rep("SAMPLE_FOLDER = 'Sample data (optional)'\n",
    "SAMPLE_FOLDER = 'Sample data (optional)'\n"
    "BONUS_FOLDER = 'Bonus (optional)'                  # v5: the bonus programs, beside the sample data\n"
    "BONUS = ['extras/sudoku']                          # v5: each folder holds one <Name>_beta*.txt or <Name>_v*.txt\n")
rep("""    progs = sorted(glob.glob(os.path.join(opt['repo'], 'programs', '*.txt')))
    if not progs:
        sys.exit('no programs in %s/programs' % opt['repo'])
""", """    progs = sorted(glob.glob(os.path.join(opt['repo'], 'programs', '*.txt')))
    if not progs:
        sys.exit('no programs in %s/programs' % opt['repo'])
    bonus = []                                          # v5: the bonus programs, one file in each BONUS folder
    for b in BONUS:
        f = [p for p in glob.glob(os.path.join(opt['repo'], b, '*.txt'))
             if re.match(r'^[A-Za-z][A-Za-z0-9]*_(beta|v)\\d[^_]*\\.txt$', os.path.basename(p))]
        if len(f) != 1:
            sys.exit('%s must hold one program file (<Name>_beta*.txt or <Name>_v*.txt); it holds %d' % (b, len(f)))
        bonus.append(f[0])
""")
rep("""    for p in progs:
        stem = os.path.basename(p)[:-4]""", """    for p in progs + bonus:
        stem = os.path.basename(p)[:-4]""")
rep("""                      'lines': src.count('\\n') + 1, 'run': main_export(src, name)})""",
    """                      'lines': src.count('\\n') + 1, 'run': main_export(src, name), 'bonus': p in bonus})""")
rep("""    for t in table:
        if t['app']:""", """    os.makedirs(os.path.join(work, BONUS_FOLDER))
    for t in table:
        if t['app']:""")
rep("""            out = os.path.join(dest, t['name'] + '.hpprgm')
            kit(opt, 'write', t['file'], '-o', out)""", """            out = os.path.join(os.path.join(work, BONUS_FOLDER) if t['bonus'] else dest, t['name'] + '.hpprgm')
            kit(opt, 'write', t['file'], '-o', out)""")
rep("""        print('%-13s %-11s %6d lines  %8d bytes  %s%s  read back: same%s' % (
            t['name'], t['ver'], t['lines'], t['bytes'], 'app' if t['app'] else 'program',""",
    """        print('%-13s %-11s %6d lines  %8d bytes  %s%s  read back: same%s' % (
            t['name'], t['ver'], t['lines'], t['bytes'], 'app' if t['app'] else 'bonus program' if t['bonus'] else 'program',""")
rep("""    print('%s: %d programs and %d app, %.2f MB' % (zname, sum(1 for t in table if not t['app']),
                                                  sum(1 for t in table if t['app']), os.path.getsize(zpath) / 1e6))""",
    """    print('%s: %d programs and %d app, and %d bonus program, %.2f MB' % (
        zname, sum(1 for t in table if not t['app'] and not t['bonus']), sum(1 for t in table if t['app']),
        sum(1 for t in table if t['bonus']), os.path.getsize(zpath) / 1e6))""")
# the instructions: the 31 stay "the programs"; the bonus is told apart
rep('''    app = [t for t in table if t['app']]
    py = [t['name'] for t in table if t['py']]''', '''    bon = [t for t in table if t.get('bonus')]                 # v5: the bonus programs, told apart from the 31
    table = [t for t in table if not t.get('bonus')]
    app = [t for t in table if t['app']]
    py = [t['name'] for t in table if t['py']]''')
rep("""          '*%s, %s. Built by `tools/make_starter_pack_v4.py` from `programs/`; do not edit this page by hand.*'""",
    """          '*%s, %s. Built by `tools/make_starter_pack_v5.py` from `programs/` and `extras/sudoku/`; do not edit this page by hand.*'""")
rep("""    if all(t.get('checked') for t in table):""", """    if all(t.get('checked') for t in table + bon):""")
rep("""          hd('Good to know'),""", """          ] + bonus_lines(hd, c, bon) + [
          hd('Good to know'),""")
rep("""        for t in table:
            L += ['  %-13s %-11s %s%s' % (t['name'], t['ver'], t['run'] if not t['app'] else 'Apps > ' + t['name'],
                                          '  (MicroPython)' if t['py'] else '')]""",
    """        for t in table:
            L += ['  %-13s %-11s %s%s' % (t['name'], t['ver'], t['run'] if not t['app'] else 'Apps > ' + t['name'],
                                          '  (MicroPython)' if t['py'] else '')]
        for t in bon:
            L += ['  %-13s %-11s %s  (bonus, in %s)' % (t['name'], t['ver'], t['run'], BONUS_FOLDER)]""")
rep("""                '; '.join(x for x in ('app on Statistics 1Var' if t['app'] else '',
                                      'MicroPython' if t['py'] else '') if x), t['sha'])]""",
    """                '; '.join(x for x in ('app on Statistics 1Var' if t['app'] else '',
                                      'MicroPython' if t['py'] else '') if x), t['sha'])]
        for t in bon:
            L += ['| %s | %s | %s | `%s` | bonus, in `%s` (not one of the *Statisticles*) | `%s` |' % (
                t['name'], t['ver'], format(t['lines'], ','), t['run'], BONUS_FOLDER, t['sha'])]""")
rep("""made LF, trailing blank lines dropped): the file in `programs/` it was built from.""",
    """made LF, trailing blank lines dropped): the file in `programs/` (or, for the bonus, `extras/sudoku/`) it was built from.""")
rep("""              '`python3 tools/make_starter_pack_v4.py v6 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a '""",
    """              '`python3 tools/make_starter_pack_v5.py v27 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a '""")
rep('''def dataload_lines(hd, c, sample, plain):''', '''def bonus_lines(hd, c, bon):
    """v5: what the bonus folder is."""
    if not bon:
        return []
    return [hd('Just for fun: the bonus'),
            '- The folder %s holds %s, a bonus that is not one of the 31 %s: %s. Copy it into the Prime'
            ' folder too if you want it, in the same way (calculator closed). The book tells about it in Appendix G,'
            ' "Just for fun: Sudoku, and the statistics hiding in it".' % (
                c(BONUS_FOLDER), ', '.join(c(t['name'] + '.hpprgm') for t in bon),
                'Statisticles' if c('x') == 'x' else '*Statisticles*',
                '; '.join('%s %s, a Sudoku puzzle game that keeps a record of the games you finish for a class'
                          ' experiment' % (t['name'], t['ver']) if t['name'] == 'Sudoku' else t['name'] for t in bon)),
            '']


def dataload_lines(hd, c, sample, plain):''')
rep('''  python3 tools/make_starter_pack_v4.py VER''', '''  python3 tools/make_starter_pack_v5.py VER''')
io.open(R + 'make_starter_pack_v5.py', 'w', encoding='utf-8').write(s)
print('wrote make_starter_pack_v5.py', len(s))
