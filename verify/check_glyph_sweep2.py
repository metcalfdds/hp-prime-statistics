# Checks the second pass of the 20 Oct 2026 symbol sweep (sweep2.py).
# For each program: every changed line that is not a comment differs from
# the old line ONLY inside string literals, except the code lines listed
# in CODE_OK; no CAS-bound text changed; what is left of the spelled-out
# forms is printed so it can be read through.
import re, difflib, os
OLD = '/home/claude/all20'; NEW = '/home/claude/glyph'
G = '/home/claude/glyph/'
PAIRS = [('Burr3_v2.4b.txt', 'Burr3_v2.4c.txt'), ('CICatcher_beta2c.txt', 'CICatcher_beta2d.txt'),
 ('CentralLimit_beta3c.txt', 'CentralLimit_beta3d.txt'), ('DNAMixLR_beta3c.txt', 'DNAMixLR_beta3d.txt'),
 ('ErrorRate_beta1d.txt', 'ErrorRate_beta1e.txt'), ('GaltonBoard_beta3d.txt', 'GaltonBoard_beta3e.txt'),
 ('PowerViz_v2.5d.txt', 'PowerViz_v2.5e.txt'), ('SampDist_v2.3b.txt', 'SampDist_v2.3c.txt')] + \
 [(G + o, n) for o, n in [('BiNorm3D_beta1a.txt', 'BiNorm3D_beta1b.txt'), ('ChiTable_beta3d.txt', 'ChiTable_beta3e.txt'),
  ('EpiStats_v1.7d.txt', 'EpiStats_v1.7e.txt'), ('FDAES_v3.9b.txt', 'FDAES_v3.9c.txt'),
  ('NormExplorer_beta42b.txt', 'NormExplorer_beta42c.txt'), ('ScatterLab_beta2c.txt', 'ScatterLab_beta2d.txt'),
  ('StatDist_v2.7e.txt', 'StatDist_v2.7f.txt'), ('TestChooser_beta2a.txt', 'TestChooser_beta2b.txt'),
  ('TrendTest_beta3d.txt', 'TrendTest_beta3e.txt')]]
# Both passes of the sweep are checked here, each file against its 19 Oct
# (pre-sweep) version.  Glyphs rebuilt with CHAR() in the six programs that
# keep their source ASCII are folded back to literals before comparing.
CODE_OK = {'FDAES_v3.9c.txt': ['TEXTOUT_P(CHAR(8805), G1, odCx - 6'],'DNAMixLR_beta3d.txt': ['dmTHG := CHAR(952);'],
           'GaltonBoard_beta3e.txt': ['pwT := "as R " + CHAR(8594) + " " + CHAR(8734);'],
           'StatDist_v2.7f.txt': ['st_Repl(fwS, "+infinity", CHAR(8734))', 'st_Repl(fwS, "infinity", CHAR(8734))',
                                  'RETURN CHAR(8722) + CHAR(8734);', 'RETURN CHAR(8734);']}
CASWORDS = re.compile(r'CAS\(|Cas\(|st_FmAsk|csCas|erlCas\(|pv_Cas|EXPR\(|cxE :=|limit\(|simplify\(|solve\(')
FOLD = re.compile(r'\((?:"[^"]*"|CHAR\(\d+\))(?: \+ (?:"[^"]*"|CHAR\(\d+\)))+\)')
GLY = re.compile(r'CHAR\((57344|57345|967|178|8730|8805|8804|8800|177|215|8594|8734|952|951|956|963|961|966|964|945|960|8320|8321|8322|8722)\)')
def fold(code):
    def f(m):
        out = ''
        for p in re.findall(r'"[^"]*"|CHAR\(\d+\)', m.group(0)):
            out += p[1:-1] if p.startswith('"') else chr(int(p[5:-1]))
        return '"' + out + '"'
    return FOLD.sub(f, code)
def skel(l):
    code = l if re.search(r'"[^"]*//[^"]*"', l) else l.split('//')[0]
    code = fold(code)
    code = re.sub(r'"[^"]*"', '""', code)
    # the first pass split strings around CHAR(57344)/CHAR(57345) etc.: "a" + CHAR(n) + "b" -> ""
    code = re.sub(r'""(?: \+ (?:""|' + GLY.pattern + r'))+', '""', code)
    code = GLY.sub('""', code)
    return code.rstrip()
fails = 0; total = 0
for o, n in PAIRS:
    A = open(os.path.join(OLD, o), encoding='utf-8').read().split('\n')
    B = open(os.path.join(NEW, n), encoding='utf-8').read().split('\n')
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    nchg = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': continue
        olds = A[i1:i2]; news = B[j1:j2]
        for k, b in enumerate(news):
            if b.lstrip().startswith('//'): continue          # comment lines (the notes)
            nchg += 1
            a = olds[k] if k < len(olds) else ''
            if any(tok in b for tok in CODE_OK.get(n, [])): continue
            if skel(a) != skel(b):
                print('FAIL code outside strings changed:', n, j1 + k + 1, '\n   ', a.strip()[:120], '\n   ', b.strip()[:120]); fails += 1
            if CASWORDS.search(b):
                print('FAIL a CAS-bound line changed:', n, j1 + k + 1, b.strip()[:120]); fails += 1
        for a in olds:
            if not a.lstrip().startswith('//') and a.strip() and len(olds) > len(news):
                pass
    total += nchg
    print('%-26s %3d code lines changed, non-comment line count %d -> %d' % (n, nchg,
          sum(1 for x in A if not x.lstrip().startswith('//')), sum(1 for x in B if not x.lstrip().startswith('//'))))
print('\nTOTAL %d changed code lines, %d failures' % (total, fails))
