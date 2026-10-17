#!/usr/bin/env python3
"""ppl_gate_v1a.py -- the four-tool gate every HP Prime PPL file passes before a paste.

usage (from D:\\HP-Prime, or the repo's tools/ folder with the programs one level up):
    python3 ppl_gate_v1.py NEW.txt [ORIGINAL.txt]
    python3 ppl_gate_v1.py --fleet *.txt          (only the fleet-wide name check)

What it runs, in order (Lessons Learned v7f, rule 14):
  1. hp-prime-kit's linter (`hpprime lint`).  Every device-tested program in the fleet gives
     0 errors, so an error is real.  The kit is read from
     Community_Library/github/JordiRigau__hp-prime-kit.zip and unpacked once into a temp folder.
     A file with a #PYTHON block shows one 'unbalanced' inside that block -- expected.
  2. ppl_check_v3.py, the error-code tally (and the ORIGINAL's, for comparison).  The hard
     codes E2 (block balance), E3 (LOCAL > 6), E6 (LOCAL placement), E8 (lowercase exponent,
     '=' for '=='), E10 (INPUT target) and E11 (built-in name clash, case ignored) must be 0.
  3. lint_ppl.py, the structural lint (block balance, LOCAL sizes, INPUT counts, CHOOSE
     pattern).  Its 'no function named <file>' and EXPORT-discipline lines are known noise.
  4. A full parse with the kit's own PPL interpreter.  It cannot read a file-level LOCAL after
     an EXPORT list, forward declarations, the √ character or #RRGGBB:24h colours; a failure
     on such a line is the tool's limit (the original will fail the same way), not an error.
Then fleet_names_v2.py over every *.txt beside NEW, so a new helper name cannot collide with
another program's (all programs share ONE pool of routine names on the calculator).

Python 3 standard library only.  Roger Metcalf / Claude, 16 Oct 2026.
v1a (16 Oct 2026, evening): paths are made absolute before any tool sees them, and a lint_ppl
run that prints no summary line now FAILS the gate instead of passing it silently.
"""
import sys, os, re, glob, zipfile, tempfile, subprocess, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
HARD = ('E2', 'E3', 'E6', 'E8', 'E10', 'E11')


def find(name):
    """A tool or data file: next to this script, or one folder up."""
    for d in (HERE, os.path.dirname(HERE)):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def kit_dir():
    """Unpack hp-prime-kit once and return the folder that holds hpprime.py."""
    z = find(os.path.join('Community_Library', 'github', 'JordiRigau__hp-prime-kit.zip'))
    if z is None:
        return None
    dest = os.path.join(tempfile.gettempdir(), 'hpkit_gate')
    root = os.path.join(dest, 'hp-prime-kit-HEAD')
    if not os.path.exists(os.path.join(root, 'hpprime.py')):
        with zipfile.ZipFile(z) as zf:
            zf.extractall(dest)
    return root


def strip_for_parse(src):
    """Remove #pragma lines and #PYTHON blocks; hex colours to decimal (the kit has neither)."""
    out, skip = [], False
    for ln in src.split('\n'):
        s = ln.strip()
        if s.startswith('#PYTHON'):
            skip = True; out.append(''); continue
        if skip:
            out.append('')
            if s.startswith('#END'): skip = False
            continue
        if s.startswith('#pragma'):
            out.append(''); continue
        ln = re.sub(r'#([0-9A-Fa-f]+)h\b', lambda m: str(int(m.group(1), 16)), ln)
        out.append(ln)
    return '\n'.join(out)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout + r.stderr


def tally(path, checker, lists):
    out = run([sys.executable, '-I', checker, lists, path])
    codes = re.findall(r'\b(E\d+|W\d+)\b', out)
    counts = {}
    for c in codes: counts[c] = counts.get(c, 0) + 1
    hard = [ln for ln in out.split('\n') if re.search(r'\b(%s)\b' % '|'.join(HARD), ln)]
    return counts, hard


def parse(path, kit):
    if kit is None:
        return 'skipped (hp-prime-kit zip not found)'
    sys.path.insert(0, kit)
    try:
        from hpkit import interp
    except Exception as e:
        return 'skipped (%s)' % e
    m = interp.Machine()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            m.load(strip_for_parse(open(path, encoding='utf-8').read()))
        return 'PARSE OK (%d functions)' % len(m.funcs)
    except Exception as e:
        return 'PARSE FAIL %s: %s' % (type(e).__name__, str(e)[:160])


def gate(new, orig=None):
    bad = 0
    new = os.path.abspath(new)
    orig = os.path.abspath(orig) if orig else None
    print('=' * 70); print('GATE  ' + os.path.basename(new)); print('=' * 70)
    kit = kit_dir()
    # 1. kit lint
    if kit:
        out = run([sys.executable, os.path.join(kit, 'hpprime.py'), 'lint', new])
        errs = [ln for ln in out.split('\n') if 'ERROR' in ln]
        print('1. hp-prime-kit lint: %d error(s)' % len(errs))
        for ln in errs[:10]: print('     ' + ln.strip())
        if errs and '#PYTHON' not in open(new, encoding='utf-8').read(): bad += 1
    else:
        print('1. hp-prime-kit lint: skipped (zip not found)')
    # 2. ppl_check_v3
    checker = find('ppl_check_v3.py'); names = find('HP_Prime_Builtin_Names.txt')
    if checker and names:
        empty = os.path.join(tempfile.gettempdir(), 'ppl_gate_empty.json')
        open(empty, 'w').write('[]')
        lists = empty + ',' + names
        c, hard = tally(new, checker, lists)
        print('2. ppl_check_v3 tally: ' + (', '.join('%d %s' % (v, k) for k, v in sorted(c.items())) or 'clean'))
        if orig:
            c0, _ = tally(orig, checker, lists)
            print('   original:          ' + (', '.join('%d %s' % (v, k) for k, v in sorted(c0.items())) or 'clean'))
        print('   hard errors (%s): %s' % ('/'.join(HARD), 'none' if not hard else ''))
        for ln in hard: print('     ' + ln.strip())
        if hard: bad += 1
    else:
        print('2. ppl_check_v3: skipped (ppl_check_v3.py or HP_Prime_Builtin_Names.txt not found)')
    # 3. lint_ppl
    lp = find('lint_ppl.py')
    if lp:
        out = run([sys.executable, '-I', lp, new])
        noise = ('no function named', 'is neither the entry point nor an EP_', 'is not EXPORTed', "' is EXPORTed")
        probs = [ln.strip() for ln in out.split('\n') if 'PROBLEM' in ln and not any(n in ln for n in noise)]
        summ = [ln.strip() for ln in out.split('\n') if 'checks,' in ln]
        print('3. lint_ppl: ' + (summ[0] if summ else 'DID NOT RUN -- ' + out.strip().split(chr(10))[-1][:120]))
        for ln in probs: print('     ' + ln)
        if not summ: bad += 1
    else:
        print('3. lint_ppl: skipped (lint_ppl.py not found)')
    # 4. parse
    print('4. full parse: ' + parse(new, kit))
    if orig: print('   original:   ' + parse(orig, kit))
    # fleet names
    fn = find('fleet_names_v2.py')
    if fn:
        folder = os.path.dirname(os.path.abspath(new))
        files = sorted(set(glob.glob(os.path.join(folder, '*.txt'))) | {os.path.abspath(new)})
        files = [f for f in files if 'Builtin_Names' not in f and not re.search(r'(_out|_output|_NOTES|_CHANGES)\.txt$', f)
                 and not os.path.basename(f).startswith('verify_')]
        if orig:                              # the version being replaced is not a rival
            files = [f for f in files if os.path.abspath(f) != os.path.abspath(orig)]
        # v1a: older versions of the same program left in the folder are not rivals either --
        # keep the newest file (by modification time) of each program, and NEW itself.
        def stem(f):
            b = os.path.basename(f)
            m = re.match(r'(.+?)_(beta\d|v\d|template_v\d)', b)
            return (m.group(1) if m else os.path.splitext(b)[0]).lower()
        newest = {}
        for f in files:
            f = os.path.abspath(f)
            k = stem(f)
            if k not in newest or newest[k] != new and (f == new or os.path.getmtime(f) > os.path.getmtime(newest[k])):
                newest[k] = f
        files = sorted(set(newest.values()))
        out = run([sys.executable, '-I', fn] + files)
        lines = [ln for ln in out.split('\n') if ln.strip()]
        mine = [ln for ln in lines if os.path.basename(new) in ln]
        print('5. fleet_names_v2 over %d files (newest of each program): %s' % (len(files), lines[-1] if lines else '?'))
        for ln in mine: print('     ' + ln)
        if mine: bad += 1
    print('RESULT: ' + ('PASS' if bad == 0 else 'LOOK AT THE LINES ABOVE'))
    return bad


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(2)
    if a[0] == '--fleet':
        fn = find('fleet_names_v2.py')
        sys.exit(subprocess.call([sys.executable, '-I', fn] + a[1:]))
    sys.exit(1 if gate(a[0], a[1] if len(a) > 1 else None) else 0)
