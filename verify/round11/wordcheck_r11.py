"""Round 11: the words of every program's help, old dump with the approved changes applied, against the new dump.
Titles, page counts, footers and the version are left out; everything else must match word for word."""
import json, re, sys
sys.path.insert(0, 'tools11')
import props
from hp11 import norm
OLD = json.load(open('helppages_before_r11.json', encoding='utf-8'))   # the dump before Round 11 (../helppages.json is Round 11's now)
NEW = json.load(open('helppages_r11.json', encoding='utf-8'))
G = {'': 'x̄', '': 'p̂'}
NAV = re.compile(r'(next page|= next|any key|Any key|Esc = (back|done|leave|quit|menu)|= back$|= menu$|^Page \d+/\d+|Right/tap|tap or Ent|tap or key|^\d+/\d+, tap)', re.I)


def text(pages, prog):
    out = []
    for p in pages:
        if not p or p[0].startswith('['):
            continue
        p = list(p)
        while p and (NAV.search(p[-1]) and len(p[-1]) < 70):
            p.pop()                              # the footer
        for i, l in enumerate(p):
            if i == 0 and ' help' in l:
                continue
            for a, b in G.items():
                l = l.replace(a, b)
            out.append(l)
    t = ' '.join(out)
    t = re.sub(r'([A-Za-z])-\s+([a-z])', r'\1-\2', t)
    t = re.sub(r'\bv?\d+\.\d+[a-z]\b|\bbeta \d+[a-z]?\b', 'VER', t)
    return re.sub(r'\s+', ' ', t).strip()


bad = 0
for prog in NEW:
    old = text(OLD[prog], prog)
    for pg, lst in props.for_prog(prog).items():
        for o, n in lst:
            o2 = re.sub(r'\s+', ' ', o.replace('\n', ' ')).strip()
            if o2.startswith(prog + ' help'):
                continue
            if 'bias =' in o2 and prog == 'AgreeLab':
                o2, n = 'bias = d ;', 'bias = d , the mean difference;'
            pat = re.compile(r'\s*'.join(re.escape(c) for c in o2.replace(' ', '')))
            m = pat.search(old)
            if not m:
                print(prog, 'OLD NOT FOUND:', o2[:70]); bad += 1
                continue
            old = old[:m.start()] + n + old[m.end():]
    new = text(NEW[prog], prog)
    a, b = re.sub(r'\s+', '', old), re.sub(r'\s+', '', new)
    if a != b:
        import difflib
        sm = difflib.SequenceMatcher(None, old.split(' '), new.split(' '))
        diffs = [(op, ' '.join(old.split(' ')[i1:i2]), ' '.join(new.split(' ')[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
        print(prog, 'DIFFERS:', diffs[:6]); bad += 1
    else:
        print(prog, 'ok')
print('programs with differences:', bad)
