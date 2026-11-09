"""Round 11: which routines each new version changes (it should be the help routines, the header and the version only)."""
import sys, os, re, difflib
sys.path.insert(0, 'tools11')
from routines import routines
for nv in open('newfiles.txt').read().split():
    n = nv.split('_')[0]
    old = [f for f in os.listdir('r/src') if f.startswith(n + '_')][0]
    ro, Lo = routines('r/src/' + old)
    rn, Ln = routines('r/programs/' + nv + '.txt')
    def where(r, i):
        for k, (a, b) in r.items():
            if a <= i + 1 <= b:
                return k
        return '(top level)'
    sm = difflib.SequenceMatcher(None, Lo, Ln, autojunk=False)
    touched = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        for j in range(j1, max(j2, j1 + 1)):
            if j < len(Ln):
                w = where(rn, j)
                if w == '(top level)' and (Ln[j].lstrip().startswith('//')):
                    w = '(comments)'
                touched[w] = touched.get(w, 0) + 1
        for i in range(i1, i2):
            w = where(ro, i)
            if w == '(top level)' and Lo[i].lstrip().startswith('//'):
                w = '(comments)'
            touched.setdefault(w, 0)
    print('%-22s %s' % (nv, ', '.join('%s:%d' % kv for kv in sorted(touched.items()))))
