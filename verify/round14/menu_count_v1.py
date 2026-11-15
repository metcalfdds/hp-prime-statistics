#!/usr/bin/env python3
"""menu_count_v1.py -- every CHOOSE in the fleet's programs, with the number of items it lists, counted from the
program text: arguments split at the top level (strings, parentheses and braces respected).  A list held in a
variable is reported apart.  Prints totals, and the menus over eight items with where Help, Quit and Back stand."""
import re, glob, io, os, sys


def split_top(a):
    out, cur, d, q = [], '', 0, False
    for c in a:
        if c == '"': q = not q
        if not q:
            if c in '({[': d += 1
            elif c in ')}]': d -= 1
            elif c == ',' and d == 0:
                out.append(cur); cur = ''; continue
        cur += c
    out.append(cur)
    return [x.strip() for x in out]


tot = 0; longm = []; var = []
for p in sorted(glob.glob(os.path.join(sys.argv[1] if len(sys.argv) > 1 else 'programs', '*.txt'))):
    s = io.open(p, encoding='utf-8').read(); name = os.path.basename(p)[:-4]
    for m in re.finditer(r'\bCHOOSE\s*\(', s):
        ls = s.rfind('\n', 0, m.start()) + 1
        if '//' in s[ls:m.start()]: continue                      # a CHOOSE named in a comment
        i = m.end(); d = 1; j = i; q = False
        while j < len(s) and d:
            c = s[j]
            if c == '"': q = not q
            elif not q:
                if c == '(': d += 1
                elif c == ')': d -= 1
            j += 1
        args = split_top(s[i:j-1]); line = s.count('\n', 0, m.start()) + 1
        tot += 1
        if len(args) == 3 and args[2].startswith('{'):
            items = split_top(args[2][1:-1])
        elif len(args) > 3:
            items = args[2:]
        else:
            var.append((name, line, args[-1][:30])); continue
        if len(items) > 8:
            where = []
            for k, t in enumerate(items):
                st = re.findall(r'"((?:[^"]|"")*)"', t)
                if st and re.search(r'^\s*(help|quit|back|exit)\b', st[0], re.I): where.append((k + 1, st[0].split()[0]))
            title = (re.findall(r'"((?:[^"]|"")*)"', args[1]) or ['(built)'])[0]
            longm.append((name, line, len(items), title[:30], where))
progs = sorted(set(r[0] for r in longm))
late = [r for r in longm if any(k > 8 for k, w in r[4])]
print('CHOOSE calls: %d; with the list in a variable: %d; with more than eight items: %d, in %d programs' % (tot, len(var), len(longm), len(progs)))
print('of those, Help, Quit or Back after the eighth item: %d, in %d programs' % (len(late), len(set(r[0] for r in late))))
print('Help itself after the eighth: %d, in %d programs' % (sum(1 for r in longm if any(k > 8 and w.lower() == 'help' for k, w in r[4])),
                                                           len(set(r[0] for r in longm if any(k > 8 and w.lower() == 'help' for k, w in r[4])))))
for r in longm:
    print('  %-22s %5d  %2d  %-30s  %s' % (r[0], r[1], r[2], r[3], ' '.join('%s=%d' % (w, k) for k, w in r[4])))
print('variable lists:', var)
