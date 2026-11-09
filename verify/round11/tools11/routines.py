"""Find a PPL file's top-level routines: name -> (first line, last line), 1-based, by 'name(...)' then 'BEGIN' at column 0."""
import re, sys
HEAD = re.compile(r'^(EXPORT\s+|LOCAL\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*$')
def routines(path):
    L = open(path, encoding='utf-8').read().split('\n')
    starts = []
    for i, l in enumerate(L):
        m = HEAD.match(l)
        if m and i + 1 < len(L) and L[i + 1].strip().startswith('BEGIN'):
            starts.append((m.group(2), i))
    out = {}
    for k, (n, s) in enumerate(starts):
        e = (starts[k + 1][1] if k + 1 < len(starts) else len(L)) - 1
        # back up to the last END; of this routine
        while e > s and not re.match(r'^END;', L[e]): e -= 1
        out[n] = (s + 1, e + 1)
    return out, L
if __name__ == '__main__':
    r, L = routines(sys.argv[1])
    for n in sys.argv[2:]:
        a, b = r[n]; print(f'--- {n} {a}-{b}'); print('\n'.join(f'{i}: {L[i-1]}' for i in range(a, b + 1)))
