#!/usr/bin/env python3
"""fleet_names_v2.py -- one shared pool of routine names across every HP Prime program.

The Prime keeps the routines of ALL programs in one pool, so two programs that define
a helper with the same name (NiceNum, fmtp, lngamma ...) can run each other's code.
That sent StudRange into a Burr3 screen on 10 Oct 2026 and forced a reset.

usage:  python3 fleet_names_v2.py prog1.txt prog2.txt ...      (or *.txt)

Reports, case-insensitively (the Prime ignores case when it matches names):
  COLLISION  a routine name defined in more than one file
  UNTAGGED   a non-EXPORT routine whose name does not carry ITS OWN FILE's tag
  MIXEDTAG   a file whose non-EXPORT routines carry more than one tag
  BUILTIN    a routine name that matches an HP Prime built-in when case is ignored
             (needs HP_Prime_Builtin_Names.txt next to this script)
Exit status 1 when any COLLISION, UNTAGGED or MIXEDTAG is found.

v2 (16 Oct 2026): v1 accepted ANY two-to-four-character prefix as a tag, so StatDist's
ten `calc_*` stubs passed as tagged and the v7d "0 untagged" result was a false pass.
v2 works out each file's tag (the prefix most of its helpers share: `sr_`, `b3_`, or the
glued `cs`/`clt` style) and requires every helper in that file to carry it. A file is
allowed exactly one tag.  The app hooks START/Plot/Symb/Num/Reset/Info/VIEW are exempt.
"""
import re, sys, os, collections

HEAD = re.compile(r'^\s*(EXPORT\s+)?(LOCAL\s+)?([A-Za-z_]\w*)\s*\(')
APP_HOOKS = {'START', 'PLOT', 'SYMB', 'NUM', 'RESET', 'INFO', 'PLOTSETUP', 'SYMBSETUP',
             'NUMSETUP', 'VIEW'}
UNDERSCORE = re.compile(r'^([a-z0-9]{2,4})_\w+$')      # sr_NiceNum, b3_fmtp, es_FmtNum
GLUED = re.compile(r'^([a-z]{2,4})[A-Z]\w*$')           # csGrid, cltSample, gbDrain


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


def tag_of(name):
    """The tag a helper name carries, or None."""
    m = UNDERSCORE.match(name)
    if m: return m.group(1).lower() + '_'
    m = GLUED.match(name)
    if m: return m.group(1).lower()
    return None


def main(paths):
    builtins = set()
    bpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'HP_Prime_Builtin_Names.txt')
    if os.path.exists(bpath):
        builtins = {l.split()[0].upper() for l in open(bpath, encoding='utf-8', errors='replace')
                    if l.strip() and not l.startswith('#')}
    where = collections.defaultdict(list)
    untagged = []; bi = []; mixed = []
    for p in paths:
        base = os.path.basename(p)
        rs = routines(p)
        helpers = [n for n, ex in rs if not ex and n.upper() not in APP_HOOKS]
        tags = collections.Counter(t for t in (tag_of(n) for n in helpers) if t)
        filetag = tags.most_common(1)[0][0] if tags else None
        if len(tags) > 1:
            mixed.append((base, ', '.join('%s (%d)' % kv for kv in tags.most_common())))
        for name, exported in rs:
            where[name.upper()].append((base, name))
            if name.upper() in builtins and name.upper() not in APP_HOOKS:
                bi.append((base, name))
            if not exported and name.upper() not in APP_HOOKS:
                if filetag is None or tag_of(name) != filetag:
                    untagged.append((base, name, filetag or '-'))
    bad = 0
    for key, defs in sorted(where.items()):
        files = {f for f, _ in defs}
        if len(files) > 1:
            bad += 1
            print('COLLISION  %-20s %s' % (key, ', '.join(sorted('%s:%s' % d for d in defs))))
    for f, n, t in untagged: print('UNTAGGED   %-20s %-28s (file tag %s)' % (n, f, t))
    for f, t in mixed:       print('MIXEDTAG   %-20s %s' % (f, t))
    for f, n in bi:          print('BUILTIN    %-20s %s' % (n, f))
    print('%d files, %d routine names, %d collisions, %d untagged, %d mixed-tag files, %d built-in matches'
          % (len(paths), len(where), bad, len(untagged), len(mixed), len(bi)))
    return 1 if (bad or untagged or mixed) else 0


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
