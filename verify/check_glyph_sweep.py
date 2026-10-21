#!/usr/bin/env python3
"""check_glyph_sweep.py -- the 20 Oct 2026 symbol sweep changed only on-screen text.
For each old/new pair: (1) with every string literal and every // comment blanked, the code is
identical, except on the listed lines where a string was split around CHAR(57344)/CHAR(57345)
or a ')^0.5' became '√(...)'; (2) no string the CAS receives changed (lines that build CAS text are
compared whole); (3) the harness (ppl_run_v3e) loads the new file; (4) no display string still
spells a symbol out (X2, chi-square, chi-sq., ^2, sqrt(, xbar, x-bar, p-hat), CAS text excepted."""
import re, sys
sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3e import Harness
PAIRS = [('BiNorm3D_beta1a','BiNorm3D_beta1b'),('ChiTable_beta3d','ChiTable_beta3e'),('EpiStats_v1.7d','EpiStats_v1.7e'),
 ('ScatterLab_beta2c','ScatterLab_beta2d'),('StatDist_v2.7e','StatDist_v2.7f'),('TestChooser_beta2a','TestChooser_beta2b'),
 ('TrendTest_beta3d','TrendTest_beta3e'),('FDAES_v3.9b','FDAES_v3.9c'),('NormExplorer_beta42b','NormExplorer_beta42c')]
CASMARK = re.compile(r'csCas|cxE|fdR :=|fiM :=|st_FmAsk|simplify|xcS :=|csXX2')
SPELL = re.compile(r'(?<![A-Za-z_])(X2|X\^2|x\^2|[Cc]hi-?sq(?:uare)?\.?|[Xx]-?bar|xbar|[Pp]-hat|phat|sqrt\(|\^2(?![0-9.]))')
def strip(line):
    out, i, s = [], 0, line
    s = re.sub(r'"[^"]*"', '""', s)
    s = s.split('//')[0]
    return s.rstrip()
bad = 0
for a, b in PAIRS:
    A = open(a + '.txt', encoding='utf-8').read().split('\n')
    B = open(b + '.txt', encoding='utf-8').read().split('\n')
    ca = [strip(l) for l in A if strip(l).strip()]
    cb = [strip(l) for l in B if strip(l).strip()]
    diff = [(x, y) for x, y in zip(ca, cb) if x != y]
    allowed = all(('CHAR(5734' in y) or ('√' in y) for x, y in diff) and len(ca) == len(cb)
    cas_a = [l for l in A if CASMARK.search(l)]; cas_b = [l for l in B if CASMARK.search(l)]
    spelled = [l.strip()[:90] for l in B if not CASMARK.search(l) and any(SPELL.search(s) for s in re.findall(r'"([^"]*)"', l.split('//')[0] if '"//' not in l else l))]
    try:
        Harness(b + '.txt', home_minus=True); loads = True
    except Exception as e:
        loads = False; print('   load error:', e)
    ok = allowed and cas_a == cas_b and loads and not spelled
    bad += not ok
    print('%-24s code lines %d=%d, code diffs %d (all glyph splits: %s), CAS lines same: %s, harness loads: %s, still spelled: %d  %s'
          % (b, len(ca), len(cb), len(diff), allowed, cas_a == cas_b, loads, len(spelled), 'OK' if ok else 'FAIL'))
    for s in spelled: print('     ', s)
print('failures:', bad)
