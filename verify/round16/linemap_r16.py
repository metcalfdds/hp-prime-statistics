# linemap.py NEW OLD -- routines of NEW with their line ranges: new ones, and those whose text differs from OLD's
import re, sys, io
def routines(path):
    L = io.open(path, encoding='utf-8').read().split('\n')
    out = {}; order = []
    i = 0
    hdr = re.compile(r'^(?:EXPORT\s+)?([A-Za-z_]\w*)\s*\([^)]*\)\s*$')
    while i < len(L):
        m = hdr.match(L[i])
        if m and i + 1 < len(L) and L[i + 1].strip() == 'BEGIN':
            name = m.group(1); depth = 0; j = i + 1
            # the routine ends at the first line that is exactly "END;" at column 0 after BEGIN
            while j < len(L) and L[j] != 'END;':
                j += 1
            out[name] = (i + 1, j + 1, '\n'.join(L[i:j + 1])); order.append(name); i = j + 1
        else:
            i += 1
    return out, order
new, order = routines(sys.argv[1]); old, _ = routines(sys.argv[2])
nw = [n for n in order if n not in old]; ch = [n for n in order if n in old and old[n][2] != new[n][2]]
print('routines: %d (old %d); new %d; changed %d; gone %d' % (len(new), len(old), len(nw), len(ch), len([n for n in old if n not in new])))
print('NEW: ' + ', '.join('%s %d-%d' % (n, new[n][0], new[n][1]) for n in nw))
print('CHANGED: ' + ', '.join('%s %d-%d' % (n, new[n][0], new[n][1]) for n in ch))
