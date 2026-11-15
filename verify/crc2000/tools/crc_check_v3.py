# -*- coding: utf-8 -*-
"""crc_check_v3.py -- part 3: the upper 1%, 5% and 10% points of the studentized range in Zwillinger & Kokoska (2000), PDF
pages 87 to 89, against scipy.stats.studentized_range.  The three tables are set sideways, and the text layer runs their
numbers together, so the words are taken with their positions: one row of the table is one column of words on the page.
  python3 -I tools/crc_check_v3.py pdf/crc_spstf.pdf work/part3.json"""
import sys, re, json, math, warnings
warnings.simplefilter('ignore')
import fitz
from scipy import stats
fitz.TOOLS.mupdf_display_errors(False)
d = fitz.open(sys.argv[1])
def dec(s): return len(s.split('.')[1]) if '.' in s else 0
def verdict(printed, true):
    dd = dec(printed); p = float(printed); unit = 10.0 ** (-dd)
    if abs(p - true) <= 0.5 * unit * (1 + 1e-9) + 1e-12: return 'ok'
    if abs(p - true) <= 1.0 * unit * (1 + 1e-9): return 'last digit'
    return 'DIFFERS'
res = {'tables': {}, 'cells': [], 'rows': {}}
for pn, a in ((87, 0.01), (88, 0.05), (89, 0.10)):
    p = d[pn - 1]; rows = {}
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            if tuple(round(v) for v in l['dir']) != (0, -1): continue
            for s in l['spans']:
                x = round(s['bbox'][0]); 
                for tok, y in ((s['text'], s['bbox'][3]),):
                    rows.setdefault(x, []).append((-y, tok))
    table = 'studentized range, upper %g%%' % (100 * a); t = res['tables'].setdefault(table, {'cells': 0, 'ok': 0, 'last digit': 0, 'DIFFERS': 0, 'rows': 0})
    hdr = None
    for x in sorted(rows):
        joined = ''.join(tk for _, tk in sorted(rows[x])).replace('−', '-')
        hdr = list(range(2, 21))          # the header row reads n = 2, 3, ..., 20 (its digits run together in the text layer)
        if 'ν' in joined or 'n' in joined: continue
        S = re.sub(r'\s+', '', joined)
        # the row's label and its 19 values run together in the text layer ("1203.714.20..."): every value has two decimals,
        # and the label is the one of the table's df values that leaves 19 values, the first without a leading zero and not above the second
        lab = vals = None
        nread = t['rows'] + len(res['rows'].get(table, []))          # rows come in the table's order: the first twenty are df 1 to 20
        for cand in ((str(nread + 1),) if nread < 20 else ('∞', '1000', '120', '100', '60', '40', '30', '25', '24')):
            if S.startswith(cand):
                v = re.findall(r'\d+\.\d\d', S[len(cand):])
                if len(v) == 19 and ''.join(v) == S[len(cand):] and not v[0].startswith('0') and float(v[0]) <= float(v[1]) + 1e-9:
                    lab, vals = cand, v; break
        if lab is None:
            res['rows'].setdefault(table, []).append([S[:70]]); continue
        t['rows'] += 1; df = math.inf if lab == '∞' else int(lab)
        for k, v in zip(hdr, vals):
            true = float(stats.studentized_range.isf(a, k, df)); vd = verdict(v, true); t['cells'] += 1; t[vd] += 1
            if vd != 'ok': res['cells'].append([table, pn, 'n=%d df=%s' % (k, lab), v, round(true, 3), vd])
            res.setdefault('grid', []).append([a, k, lab, v, round(true, 6)])
    t['columns'] = hdr
json.dump(res, open(sys.argv[2], 'w'), indent=0)
for k, v in res['tables'].items(): print(k, {a: b for a, b in v.items() if a != 'columns'}, 'n =', v['columns'][0], 'to', v['columns'][-1])
print('rows not read:', {k: len(v) for k, v in res['rows'].items()}, [r for v in res['rows'].values() for r in v][:4])
import collections
cc = collections.Counter((c[0][-9:], c[2].split('df=')[1]) for c in res['cells'] if c[5] == 'DIFFERS')
print('cells that differ, by table and df:', dict(cc))
big = sorted((c for c in res['cells'] if c[5] == 'DIFFERS'), key=lambda c: -abs(float(c[3]) - c[4]) / c[4])[:10]
print('largest relative differences:', [c[1:5] for c in big])
