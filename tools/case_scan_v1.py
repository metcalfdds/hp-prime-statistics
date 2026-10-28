import re,sys,glob,collections
def names(path):
    out=[]; inpy=False
    for ln in open(path,encoding='utf-8',errors='replace'):
        s=ln.strip()
        if s.startswith('#PYTHON'): inpy=True
        if inpy:
            if s.startswith('#END'): inpy=False
            continue
        s=s.split('//')[0]
        m=re.match(r'EXPORT\s+(.*)',s)
        if m:
            body=m.group(1)
            m2=re.match(r'([A-Za-z_]\w*)\s*\(',body)
            if m2: out.append((m2.group(1),'export-fn'))
            else:
                for n in re.findall(r'([A-Za-z_]\w*)\s*(?::=[^,;]*)?',body.rstrip(';')): out.append((n,'export'))
            continue
        m=re.match(r'([A-Za-z_]\w*)\s*\([^()]*\)\s*$',s)
        if m and not re.match(r'(IF|WHILE|FOR|CASE|RETURN|LOCAL)\b',s,re.I): out.append((m.group(1),'routine'))
    return out
files=[f for f in sorted(glob.glob(sys.argv[1])) if 'Builtin' not in f]
glob_=collections.defaultdict(set)
for f in files:
    ns=names(f); d=collections.defaultdict(set)
    for n,k in ns: d[n.lower()].add(n); glob_[n.lower()].add((n,f.split('/')[-1]))
    for k,v in d.items():
        if len(v)>1: print('IN-FILE', f.split('/')[-1], sorted(v))
for k,v in glob_.items():
    sp={n for n,_ in v}; fs={f for _,f in v}
    if len(sp)>1 and len(fs)>1: print('ACROSS', sorted(v))
print('scanned',len(files),'files')
