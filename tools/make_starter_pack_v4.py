#!/usr/bin/env python3
"""make_starter_pack_v4.py -- builds the Virtual Calculator starter pack from programs/ (1 Nov 2026).

v4 (1 Nov 2026): CHECKED FILES.  With --checked DIR the pack carries, for each program, the file the Virtual
Calculator itself wrote back after the program was Checked once there: the same source plus the calculator's compiled
block.  Measured on 1 Nov 2026 (Virtual Calculator 2.4.2, build 2026-09-09): a checked TTestLabG.hpprgm copied into a
calculator that had forgotten the program ran at once from Home, with no Check; the control, ResampLab as a file
without the block, gave "Syntax Error" until checked.  So a student who installs a checked pack never Checks anything.
Each checked file's source is read back and must equal programs/<file>.txt, or the build stops (a program changed
after it was checked must be checked again).  For the app, only its program file (.hpappprgm) is taken from DIR; its
descriptor and note are built from the base as before, because the calculator's own descriptor holds the app's
saved state.  Without --checked the pack is built as in v3 and the instructions keep the Check step.
v3 (31 Oct 2026, night): the instructions name the Data Loader by its folder, data-loader/, not by the page's
versioned file name, which changes.  v2 (31 Oct 2026, the data loader): the pack also carries a sample matrix, "Sample data (optional)/M1.hpmat" (the
Rossi re-arrest data, 432 x 5, from data-loader/examples/rossi.csv), so DataLoad has something to load at once; it
is written by hp-prime-kit's `matrix write` and read back value for value.  The instructions say what DataLoad and
the Data Loader page are for.  v1 built the 28-program pack of the same day.

WHAT IT MAKES
  starter-pack/HP_Prime_Statistics_Starter_Pack_<VER>.zip, holding
      READ_ME_FIRST.txt                      what to do, in plain words (CRLF, for Notepad)
      Copy these into Prime/<Name>.hpprgm    one per program, named as on Roger's calculators
      Copy these into Prime/CentralLimit.hpappdir/   the one app (built on Statistics 1Var)
      Sample data (optional)/M1.hpmat         the Rossi data as matrix M1, for DataLoad (v2)
  starter-pack/README.md                     the same instructions and the table of versions

  A student copies the files into the Virtual Calculator's own folder,
  Documents\\HP Prime\\Calculators\\Prime, while it is closed; the next time it starts they are in the
  Program Catalog.  Lessons Learned v7zb, section 16, has what was verified on 31 Oct 2026.

HOW EACH FILE IS BUILT
  - A program: hp-prime-kit's `hpprime write SRC.txt -o NAME.hpprgm` (MIT, JordiRigau/hp-prime-kit), which puts
    the source into a copy of a Connectivity Kit container.  Then `hpprime read` pulls the source back out and
    it must equal programs/<file>.txt (line endings and trailing blanks aside), or the build stops.
  - The app (a program whose header says "THIS IS AN APP"): `hpprime build NAME --ppl SRC.txt --base BASE.hpapp`.
    BASE is tools/CentralLimit_app_base_v1.hpapp, the descriptor of Roger's working CentralLimit app on the
    Virtual Calculator (a user copy of Statistics 1Var whose H1 is D1).  The kit's own bases are Python and Base
    App: None, and CentralLimit needs Statistics 1Var's columns and plots.  Its .hpappprgm is read back and
    compared the same way.
  - A program's calculator name is its file name up to _beta or _v (TTestLab_beta1a.txt -> TTestLab).  The
    build stops if two programs would get one name, or a name is a Prime built-in or a routine or exported name
    of another program (all programs on a Prime share one pool of names), ignoring case as the Prime does.

RUN
  python3 tools/make_starter_pack_v4.py VER [--kit PATH] [--repo PATH] [--out PATH] [--sample CSV] [--checked DIR]
      VER   the pack's version, e.g. v2 (every new build of the pack gets the next number)
      --kit hp-prime-kit's folder (default: $HPKIT, then /tmp/kit/hp-prime-kit-HEAD)
      --checked  a folder of files copied back from the Virtual Calculator after each program was Checked
            there (<Name>.hpprgm, <Name>.hpappdir/<Name>.hpappprgm); every program must have one, or the build stops
      --sample  the CSV for the sample matrix (default data-loader/examples/rossi.csv; a first row of names is
            dropped; "none" leaves the sample out)
  Needs Python 3 only, and the kit.  Prints one line per program and the zip's size.
"""
import datetime
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
ZIP_FOLDER = 'Copy these into Prime'
SAMPLE_FOLDER = 'Sample data (optional)'
RAW = 'https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack'
APP_MARK = 'THIS IS AN APP'
BASE_HPAPP = os.path.join(TOOLS, 'CentralLimit_app_base_v1.hpapp')
VC_TESTED = 'the Virtual Calculator 2.4.2 (build 2026-09-09), 64-bit'


def args():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        sys.exit(__doc__)
    opt = {'ver': a[0], 'kit': os.environ.get('HPKIT', '/tmp/kit/hp-prime-kit-HEAD'),
           'repo': os.path.dirname(TOOLS), 'out': None, 'sample': None, 'checked': None}
    i = 1
    while i < len(a):
        if a[i] in ('--kit', '--repo', '--out', '--sample', '--checked') and i + 1 < len(a):
            opt[a[i][2:]] = a[i + 1]
            i += 2
        else:
            sys.exit('unknown argument: ' + a[i])
    if not re.match(r'^v\d+[a-z]?$', opt['ver']):
        sys.exit('VER must look like v1, v2, v2a')
    opt['out'] = opt['out'] or os.path.join(opt['repo'], 'starter-pack')
    if opt['sample'] is None:
        opt['sample'] = os.path.join(opt['repo'], 'data-loader', 'examples', 'rossi.csv')
    if opt['sample'] != 'none' and not os.path.exists(opt['sample']):
        sys.exit('the sample CSV %s is missing (pass --sample none to leave it out)' % opt['sample'])
    if opt['checked'] and not os.path.isdir(opt['checked']):
        sys.exit('the checked-files folder %s is missing' % opt['checked'])
    if not os.path.exists(os.path.join(opt['kit'], 'hpprime.py')):
        sys.exit('hp-prime-kit not found at %s (pass --kit or set HPKIT)' % opt['kit'])
    return opt


def norm(s):
    """Source text for comparison: one kind of line ending, no trailing blank lines."""
    return s.replace('\r\n', '\n').replace('\r', '\n').rstrip()


def kit(opt, *cmd):
    r = subprocess.run([sys.executable, os.path.join(opt['kit'], 'hpprime.py')] + list(cmd),
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('hpprime %s failed:\n%s%s' % (' '.join(cmd), r.stdout, r.stderr))
    return r.stdout


def strip_comment(line):
    """Code part of a PPL line: drops a // comment that is not inside a string."""
    out, q = [], False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            q = not q
        if not q and line.startswith('//', i):
            break
        out.append(c)
        i += 1
    return ''.join(out)


def names_in(src):
    """Routine and EXPORT names a program puts in the calculator's shared pool (PPL part only)."""
    out, inpy = set(), False
    for ln in src.split('\n'):
        s = ln.strip()
        if s.startswith('#PYTHON'):
            inpy = True
        if inpy:
            if s.startswith('#END'):
                inpy = False
            continue
        s = strip_comment(s).strip()
        m = re.match(r'EXPORT\s+([A-Za-z_]\w*)\s*\(', s)
        if m:
            out.add(m.group(1))
            continue
        m = re.match(r'EXPORT\s+(.*)', s)
        if m:
            out.update(re.findall(r'([A-Za-z_]\w*)\s*(?::=[^,;]*)?', m.group(1).rstrip(';')))
            continue
        m = re.match(r'([A-Za-z_]\w*)\s*\([^()]*\)\s*;?\s*$', s)
        if m and not re.match(r'(IF|WHILE|FOR|CASE|RETURN|LOCAL|REPEAT|UNTIL)\b', s, re.I):
            out.add(m.group(1))
    return out


def main_export(src, name):
    ex = re.findall(r'^EXPORT\s+([A-Za-z_]\w*)\s*\(', src, re.M)
    for e in ex:
        if e.lower() == name.lower():
            return e
    return ex[0] if ex else ''


def main():
    opt = args()
    progs = sorted(glob.glob(os.path.join(opt['repo'], 'programs', '*.txt')))
    if not progs:
        sys.exit('no programs in %s/programs' % opt['repo'])
    builtins = set()
    bfile = os.path.join(TOOLS, 'HP_Prime_Builtin_Names.txt')
    if os.path.exists(bfile):
        for ln in open(bfile, encoding='utf-8', errors='replace'):
            ln = ln.strip()
            if ln and not ln.startswith('#'):
                builtins.add(ln.split()[0].lower())

    # ---- names: one per program, none clashing ----
    table, pool = [], {}
    for p in progs:
        stem = os.path.basename(p)[:-4]
        m = re.match(r'^(.+?)_(beta\d.*|v\d.*)$', stem)
        if not m:
            sys.exit('cannot read a version from %s' % stem)
        src = open(p, encoding='utf-8').read()
        name, ver = m.group(1), m.group(2).replace('beta', 'beta ').replace('_', ' ')
        table.append({'file': p, 'stem': stem, 'name': name, 'ver': ver, 'src': src,
                      'app': APP_MARK in src[:30000], 'py': bool(re.search(r'^#PYTHON', src, re.M)),
                      'lines': src.count('\n') + 1, 'run': main_export(src, name)})
        for n in names_in(src):
            pool.setdefault(n.lower(), set()).add(name)
    seen, bad = {}, []
    for t in table:
        k = t['name'].lower()
        if k in seen:
            bad.append('two programs named %s (%s, %s)' % (t['name'], seen[k], t['stem']))
        seen[k] = t['stem']
        if k in builtins:
            bad.append('%s is a Prime built-in name' % t['name'])
        others = pool.get(k, set()) - {t['name']}
        if others:
            bad.append('%s is also a routine or exported name in %s' % (t['name'], ', '.join(sorted(others))))
    if bad:
        sys.exit('name check failed:\n  ' + '\n  '.join(bad))

    # ---- build ----
    work = tempfile.mkdtemp()
    dest = os.path.join(work, ZIP_FOLDER)
    os.makedirs(dest)
    for t in table:
        if t['app']:
            if not os.path.exists(BASE_HPAPP):
                sys.exit('the app base %s is missing' % BASE_HPAPP)
            kit(opt, 'build', t['name'], '--ppl', t['file'], '--base', BASE_HPAPP, '-o', dest)
            folder = os.path.join(dest, t['name'] + '.hpappdir')
            back = os.path.join(work, t['name'] + '_back.txt')
            kit(opt, 'read', os.path.join(folder, t['name'] + '.hpappprgm'), '-o', back)
            files = sorted(os.listdir(folder))
            t['bytes'] = sum(os.path.getsize(os.path.join(folder, f)) for f in files)
            t['out'] = t['name'] + '.hpappdir (%s)' % ', '.join(files)
        else:
            out = os.path.join(dest, t['name'] + '.hpprgm')
            kit(opt, 'write', t['file'], '-o', out)
            back = os.path.join(work, t['name'] + '_back.txt')
            kit(opt, 'read', out, '-o', back)
            t['bytes'] = os.path.getsize(out)
            t['out'] = t['name'] + '.hpprgm'
        same = norm(open(back, encoding='utf-8').read()) == norm(t['src'])
        if not same:
            sys.exit('%s: the source read back from the built file differs from %s' % (t['name'], t['stem']))
        t['checked'] = False
        if opt['checked']:
            built = os.path.join(folder, t['name'] + '.hpappprgm') if t['app'] else out
            rel = (t['name'] + '.hpappdir/' + t['name'] + '.hpappprgm') if t['app'] else (t['name'] + '.hpprgm')
            chk = os.path.join(opt['checked'], *rel.split('/'))
            if not os.path.exists(chk):
                sys.exit('%s: no checked file %s in %s. Copy the built file into the Virtual Calculator, Check it '
                         'there, close it, and copy the file back.' % (t['name'], rel, opt['checked']))
            back2 = os.path.join(work, t['name'] + '_chk_back.txt')
            kit(opt, 'read', chk, '-o', back2)
            if norm(open(back2, encoding='utf-8').read()) != norm(t['src']):
                sys.exit('%s: the checked file %s holds a different source from %s. The program changed after it '
                         'was checked: check the new one on the Virtual Calculator.' % (t['name'], rel, t['stem']))
            os.remove(back2)
            t['block'] = os.path.getsize(chk) - os.path.getsize(built)
            if t['block'] <= 0:
                sys.exit('%s: %s carries no compiled block: it was not checked.' % (t['name'], rel))
            shutil.copyfile(chk, built)
            t['bytes'] = t['bytes'] + t['block']
            t['checked'] = True
        t['sha'] = hashlib.sha256(norm(t['src']).encode('utf-8')).hexdigest()[:12]
        print('%-13s %-11s %6d lines  %8d bytes  %s%s  read back: same%s' % (
            t['name'], t['ver'], t['lines'], t['bytes'], 'app' if t['app'] else 'program',
            ' + MicroPython' if t['py'] else '', ('  checked (+%d)' % t['block']) if t['checked'] else ''))

    # ---- the sample matrix (v2) ----
    sample = None
    if opt['sample'] != 'none':
        rows = [ln.strip() for ln in open(opt['sample'], encoding='utf-8') if ln.strip()]
        if rows and not re.match(r'^[-+0-9.,eE ]+$', rows[0]):
            rows = rows[1:]                                   # a first row of names
        want = [[float(x) for x in r.split(',')] for r in rows]
        bare = os.path.join(work, 'sample_noheader.csv')
        open(bare, 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
        sdir = os.path.join(work, SAMPLE_FOLDER)
        os.makedirs(sdir)
        kit(opt, 'matrix', 'write', bare, '-o', os.path.join(sdir, 'M1.hpmat'))
        back = os.path.join(work, 'sample_back.csv')
        kit(opt, 'matrix', 'read', os.path.join(sdir, 'M1.hpmat'), '-o', back)
        got = [[float(x) for x in ln.split(',')] for ln in open(back, encoding='utf-8') if ln.strip()]
        if got != want:
            sys.exit('the sample matrix read back differs from %s' % opt['sample'])
        os.remove(bare)
        os.remove(back)
        sample = {'rows': len(want), 'cols': len(want[0]), 'src': os.path.basename(opt['sample']),
                  'bytes': os.path.getsize(os.path.join(sdir, 'M1.hpmat'))}
        print('sample M1.hpmat: %d x %d from %s, %d bytes  read back: same' % (
            sample['rows'], sample['cols'], sample['src'], sample['bytes']))

    # ---- the instructions, the README and the zip ----
    today = datetime.date.today().isoformat()
    zname = 'HP_Prime_Statistics_Starter_Pack_%s.zip' % opt['ver']
    readme_txt = instructions(opt['ver'], today, table, zname, plain=True, sample=sample)
    open(os.path.join(work, 'READ_ME_FIRST.txt'), 'w', encoding='utf-8', newline='\r\n').write(readme_txt)
    os.makedirs(opt['out'], exist_ok=True)
    for old in glob.glob(os.path.join(opt['out'], 'HP_Prime_Statistics_Starter_Pack_*.zip')):
        if os.path.basename(old) != zname:
            print('note: an older pack is still in %s: %s (move it out; never two current versions)'
                  % (opt['out'], os.path.basename(old)))
    zpath = os.path.join(opt['out'], zname)
    stamp = tuple(int(x) for x in today.split('-')) + (12, 0, 0)
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, _, files in os.walk(work):
            for f in sorted(files):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, work).replace(os.sep, '/')
                if rel.endswith('_back.txt') or rel.endswith('_chk_back.txt'):
                    continue
                info = zipfile.ZipInfo(rel, date_time=stamp)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, open(full, 'rb').read())
    open(os.path.join(opt['out'], 'README.md'), 'w', encoding='utf-8').write(
        instructions(opt['ver'], today, table, zname, plain=False, sample=sample))
    shutil.rmtree(work)
    print('%s: %d programs and %d app, %.2f MB' % (zname, sum(1 for t in table if not t['app']),
                                                  sum(1 for t in table if t['app']), os.path.getsize(zpath) / 1e6))
    print('README.md written in %s' % opt['out'])


def instructions(ver, today, table, zname, plain, sample=None):
    """The student's instructions: READ_ME_FIRST.txt (plain) or starter-pack/README.md (Markdown)."""
    hd = (lambda s: s.upper()) if plain else (lambda s: '### ' + s)
    c = (lambda s: s) if plain else (lambda s: '`' + s + '`')
    app = [t for t in table if t['app']]
    py = [t['name'] for t in table if t['py']]
    L = []
    if plain:
        L += ['HP PRIME STATISTICS STARTER PACK %s (%s)' % (ver, today),
              'Roger Metcalf\'s teaching programs for the HP Prime Virtual Calculator',
              'https://github.com/metcalfdds/hp-prime-statistics', '']
    else:
        L += ['# Starter pack for the Virtual Calculator', '',
              '*%s, %s. Built by `tools/make_starter_pack_v4.py` from `programs/`; do not edit this page by hand.*'
              % (ver, today), '',
              'All %d programs in one zip, ready for the free **HP Prime Virtual Calculator** on a Windows PC: '
              'no Connectivity Kit, no copying and pasting. Download **[%s](%s/%s)** (one file).'
              % (len(table), zname, RAW, zname), '',
              '*How this pack was tested on the Virtual Calculator: '
              '[docs/changes/StarterPack_%s_NOTES.md](../docs/changes/StarterPack_%s_NOTES.md).*' % (ver, ver), '']
    L += [hd('What you need'),
          '- A Windows PC with the HP Prime Virtual Calculator (64-bit). It is a free download from hpcalc.org, which'
          ' lists Hewlett-Packard as its author. The pack was tested on %s.' % VC_TESTED,
          '- The zip, unzipped (right-click it, Extract All).', '',
          hd('Install'),
          '1. Start the Virtual Calculator once, then close it (Calculator menu, Exit). That first start makes its'
          ' folder: %s.' % c('Documents\\HP Prime\\Calculators\\Prime'),
          '2. Open the unzipped folder %s and copy everything in it into that Prime folder.' % c(ZIP_FOLDER)
          + ' The calculator must be closed while you copy: it reads its folder only when it starts.',
          '3. Start the Virtual Calculator. Shift, then Program (the Program Catalog) lists the programs.', '']
    if all(t.get('checked') for t in table):
        L += [hd('Run a program'),
              '- In the Program Catalog, tap the program, then tap Run. Or type its name in Home (the list below)'
              ' and press Enter. Nothing to check or compile first: every file in this pack was checked on the'
              ' Virtual Calculator before it was packed.',
              '- If a program ever says Syntax Error, or Run does nothing (a different version of the Virtual'
              ' Calculator may want to compile it again): tap it, tap Edit, tap Check, tap OK, press Esc, then tap'
              ' Run. Once is enough.']
    else:
        L += [hd('The first time you run each program'),
          '- In the Program Catalog, highlight the program and tap Edit (tapping its name opens it too). Tap'
          ' Check: the calculator says "No errors in the program". Tap OK, press Esc, then tap Run.',
          '- Each program needs this once. A program copied in as a file is compiled the first time Check runs;'
          ' until then Run does nothing, and typing its name in Home gives a Syntax Error. A checked program'
          ' moves to the top of the list.',
          '- After that, run it from the Program Catalog, or type its name in Home (the list below) and press'
          ' Enter.']
    if app:
        L += ['- %s is an app, built on Statistics 1Var: press Apps, highlight it and tap Start (touching its icon'
              ' opens its spreadsheet instead). Then press View for its menu.' % ', '.join(t['name'] for t in app)]
    L += ['- %s and %s carry MicroPython. They work the same way: the Virtual Calculator has the'
          ' calculator\'s own MicroPython.' % (', '.join(py[:-1]), py[-1]), '',
          ] + (dataload_lines(hd, c, sample, plain) if any(t['name'] == 'DataLoad' for t in table) else []) + [
          hd('Good to know'),
          '- Windows asks before it replaces a file of the same name. Replacing it replaces that program on the'
          ' calculator.',
          '- On a real HP Prime (G1 or G2), send programs with the Connectivity Kit instead, a few at a time:'
          ' copying files works only for the Virtual Calculator.',
          '- Each program\'s source, its change notes and how it was tested are in the repository: programs/,'
          ' docs/changes/ and verify/.', '']
    if plain:
        L += ['WHAT IS IN THE PACK', '']
        L += ['  %-13s %-11s %s' % ('Program', 'Version', 'In Home, type')]
        for t in table:
            L += ['  %-13s %-11s %s%s' % (t['name'], t['ver'], t['run'] if not t['app'] else 'Apps > ' + t['name'],
                                          '  (MicroPython)' if t['py'] else '')]
        L += ['', 'Free for educational and personal use. (C) 2026 Roger Metcalf.']
    else:
        L += ['## What is in the pack', '',
              '| Program | Version | Lines | In Home, type | Notes | Source checksum |', '|---|---|---|---|---|---|']
        for t in table:
            L += ['| %s | %s | %s | %s | %s | `%s` |' % (
                t['name'], t['ver'], format(t['lines'], ','), ('`%s`' % t['run']) if not t['app'] else '(an app)',
                '; '.join(x for x in ('app on Statistics 1Var' if t['app'] else '',
                                      'MicroPython' if t['py'] else '') if x), t['sha'])]
        L += ['', '*The checksum is the first 12 hex digits of SHA-256 over the program\'s source (line endings '
              'made LF, trailing blank lines dropped): the file in `programs/` it was built from. Every file in the '
              'zip was read back and matched its source before the zip was written.*', '',
              '## Building it again', '',
              '`python3 tools/make_starter_pack_v4.py v6 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a '
              'program changes. The tool names each file, checks the names, builds with hp-prime-kit (MIT, '
              '[JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)), builds the sample matrix '
              'from `data-loader/examples/rossi.csv`, reads every file back, and writes the zip and this page. With '
              '`--checked` it carries each program as the Virtual Calculator wrote it back after one Check there '
              '(the same source plus its compiled block), so students never Check; it stops if a checked file\'s '
              'source differs from `programs/`. Build without `--checked` first, load that pack on the Virtual '
              'Calculator, Check each changed program, close it, and copy those files into FOLDER. Move the older '
              'zip out of this folder.', '',
              '*Free for educational and personal use. © 2026 Roger Metcalf.*', '']
    return '\n'.join(L)


def dataload_lines(hd, c, sample, plain):
    """What DataLoad is for, and the optional sample matrix (v2)."""
    L = [hd('Your own data: DataLoad'),
         '- Typing a long data set into a calculator is not feasible. The HP Prime Data Loader, a web page in this'
         ' repository (its folder %s), turns columns pasted from Excel, SPSS or a CSV file into the calculator\'s own'
         ' matrix file, %s. Copy it into the Prime folder the same way (calculator closed), then run DataLoad: it'
         ' puts each column, or each group\'s scores, into the Statistics 1Var lists D1-D9 (or Statistics 2Var'
         ' C1-C9) that the other programs read.' % (c('data-loader'), c('M1.hpmat')),
         '- Open the Statistics 1Var app once (Apps) before the first load: its lists do not exist until then.',
         '- If DataLoad says lists after the new ones hold data from before, choose clear. AnovaLab, RankLab and'
         ' AgreeLab read every list that holds data as one more group (or rater).']
    if sample:
        L += ['- %s holds %s: the Rossi re-arrest data (%d rows x %d columns: week of first re-arrest, arrest 1/0,'
              ' financial aid 1/0, age, prior convictions). Copy it too if you want data to try: it becomes the'
              ' calculator\'s matrix M1 and replaces what M1 held. Then DataLoad, Scores by group, scores in'
              ' column 1, groups in column 3, puts the weeks without and with financial aid in D1 and D2, ready'
              ' for TTestLab.' % (c(SAMPLE_FOLDER), c('M1.hpmat'), sample['rows'], sample['cols'])]
    return L + ['']


if __name__ == '__main__':
    main()
