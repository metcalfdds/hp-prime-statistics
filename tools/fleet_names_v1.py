#!/usr/bin/env python3
"""fleet_names_v1.py -- one shared pool of routine names across every HP Prime program.

The Prime keeps the routines of ALL programs in one pool, so two programs that define
a helper with the same name (NiceNum, fmtp, lngamma ...) can run each other's code.
That sent StudRange into a Burr3 screen on 10 Oct 2026 and forced a reset.

usage:  python3 fleet_names_v1.py prog1.txt prog2.txt ...      (or *.txt)

Reports, case-insensitively (the Prime ignores case when it matches names):
  COLLISION  a routine name defined in more than one file
  UNTAGGED   a non-EXPORT routine whose name does not start with a program tag
             (two to four letters or digits and an underscore, e.g. sr_NiceNum,
              or the older csName / cltName style: a lowercase tag glued to a
              capitalised name)
  BUILTIN    a routine name that matches an HP Prime built-in when case is ignored
             (needs HP_Prime_Builtin_Names.txt next to this script)
Exit status 1 when any COLLISION is found.
"""
import re, sys, os, collections

HEAD = re.compile(r'^\s*(EXPORT\s+)?(LOCAL\s+)?([A-Za-z_]\w*)\s*\(')
APP_HOOKS = {'START', 'PLOT', 'SYMB', 'NUM', 'RESET', 'INFO', 'PLOTSETUP', 'SYMBSETUP',
             'NUMSETUP', 'VIEW'}

def routines(path):
    """(name, exported) for every routine defined in a PPL file; Python blocks skipped."""
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    out = []; inpy = False
    for i, raw in enumerate(lines):
        s = raw.strip()
        if s.startswith('#PYTHON'): inpy = True
        if inpy:
            if s.startswith('#END'): inpy = False
            continue
        code = raw.split('//')[0]
        m = HEAD.match(code)
        if not m: continue
        # the header may run over several lines: join until the ')' then look for BEGIN
        seg = code; j = i
        while ')' not in seg and j + 1 < len(lines) and j - i < 6:
            j += 1; seg += ' ' + lines[j].split('//')[0]
        after = seg.split(')', 1)[1] if ')' in seg else ''
        if after.strip().startswith(';'):          # forward declaration, not a body
            continue
        nxt = lines[j + 1].split('//')[0].strip() if j + 1 < len(lines) else ''
        if 'BEGIN' in after or nxt.startswith('BEGIN'):
            out.append((m.group(3), bool(m.group(1))))
    return out

def main(paths):
    builtins = set()
    bpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'HP_Prime_Builtin_Names.txt')
    if os.path.exists(bpath):
        builtins = {l.split()[0].upper() for l in open(bpath, encoding='utf-8', errors='replace')
                    if l.strip() and not l.startswith('#')}
    where = collections.defaultdict(list)
    untagged = []; bi = []
    for p in paths:
        for name, exported in routines(p):
            where[name.upper()].append((os.path.basename(p), name))
            if name.upper() in builtins and name.upper() not in APP_HOOKS:
                bi.append((os.path.basename(p), name))
            if not exported and name.upper() not in APP_HOOKS:
                if not re.match(r'^[a-z0-9]{2,4}_\w+$', name) and not re.match(r'^[a-z]{2,4}[A-Z]\w*$', name):
                    untagged.append((os.path.basename(p), name))
    bad = 0
    for key, defs in sorted(where.items()):
        files = {f for f, _ in defs}
        if len(files) > 1:
            bad += 1
            print('COLLISION  %-20s %s' % (key, ', '.join(sorted('%s:%s' % d for d in defs))))
    for f, n in untagged: print('UNTAGGED   %-20s %s' % (n, f))
    for f, n in bi: print('BUILTIN    %-20s %s' % (n, f))
    print('%d files, %d routine names, %d collisions, %d untagged, %d built-in matches'
          % (len(paths), len(where), bad, len(untagged), len(bi)))
    return 1 if bad else 0

if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
