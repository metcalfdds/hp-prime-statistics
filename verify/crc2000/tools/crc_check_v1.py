# -*- coding: utf-8 -*-
"""crc_check_v1.py -- compares tables of Zwillinger & Kokoska, "CRC Standard Probability and Statistics Tables and Formulae"
(Chapman & Hall/CRC, 2000; the author's PDF, E:\\My Book Scans) with SciPy.  Part 1: the standard normal table, the critical
values of t and of chi-square, and the cumulative Poisson table.  Page numbers are the PDF's.
A cell "differs" when the printed value is not the true value rounded to the printed number of decimals (a difference of one
unit in the last place is listed apart as "last digit").  Every cell that differs is written to OUT with its page, so that
it can be looked at on the page before it is called an error of the book: the text layer can misplace a digit too.
  python3 -I tools/crc_check_v1.py work/all.txt work/part1.json"""
import sys, re, io, json
from decimal import Decimal, ROUND_HALF_EVEN
from scipy import stats
pages = io.open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\f')
NUM = r'[−-]?\d*\.\d+|[−-]?\d+'
def nums(l): return [x.replace('−', '-') for x in re.findall(NUM, l)]
def dec(s): return len(s.split('.')[1]) if '.' in s else 0
def verdict(printed, true):
    d = dec(printed); p = float(printed); unit = 10.0 ** (-d)
    if abs(p - true) <= 0.5 * unit * (1 + 1e-9) + 1e-12: return 'ok'
    if abs(p - true) <= 1.0 * unit * (1 + 1e-9): return 'last digit'
    return 'DIFFERS'
res = {'tables': {}, 'cells': []}
def note(table, page, where, printed, true):
    v = verdict(printed, true); t = res['tables'].setdefault(table, {'cells': 0, 'ok': 0, 'last digit': 0, 'DIFFERS': 0}); t['cells'] += 1; t[v] += 1
    if v != 'ok': res['cells'].append([table, page, where, printed, round(true, dec(printed) + 3), v])
# A. the standard normal table: z, f(z), F(z), 1 - F(z), two blocks to the line
for p in range(176, 185):
    for l in pages[p - 1].split('\n'):
        n = nums(l)
        if len(n) in (4, 8) and all('.' in x for x in n):
            for k in range(0, len(n), 4):
                z, f, F, S = n[k:k + 4]; zz = float(z)
                if abs(zz) > 4.001 or dec(z) != 2: continue
                note('normal f(z)', p, 'z=' + z, f, stats.norm.pdf(zz)); note('normal F(z)', p, 'z=' + z, F, stats.norm.cdf(zz)); note('normal 1-F(z)', p, 'z=' + z, S, stats.norm.sf(zz))
# B. critical values of t (upper-tail alpha in the header)
hdr = None
for l in pages[166 - 1].split('\n'):
    if 'α =' in l: hdr = [float(x) for x in nums(l.split('α =')[1])]
    elif hdr:
        n = nums(l)
        if len(n) == len(hdr) + 1 and '.' not in n[0]:
            for a, x in zip(hdr, n[1:]): note('t critical', 166, 'df=%s alpha=%g' % (n[0], a), x, stats.t.isf(a, int(n[0])))
        elif l.strip().startswith('∞') and len(n) == len(hdr):
            for a, x in zip(hdr, n): note('t critical', 166, 'df=inf alpha=%g' % a, x, stats.norm.isf(a))
# C. critical values of chi-square (upper-tail alpha in the header)
for p in range(130, 134):
    hdr = None
    for l in pages[p - 1].split('\n'):
        s = l.strip()
        if s.startswith('ν') and '.' in s: hdr = [float(x) for x in nums(s)]
        elif hdr:
            n = nums(l)
            if len(n) == len(hdr) + 1 and '.' not in n[0] and all('.' in x for x in n[1:]):
                for a, x in zip(hdr, n[1:]): note('chi-square critical', p, 'df=%s alpha=%g' % (n[0], a), x, stats.chi2.isf(a, int(n[0])))
            elif n and '.' not in n[0]: res.setdefault('skipped', []).append(['chi-square critical', p, s[:60]])
# E. cumulative Poisson
for p in range(114, 119):
    for l in pages[p - 1].split('\n'):
        n = nums(l)
        if len(n) >= 2 and '.' in n[0] and all(dec(x) == 3 for x in n[1:]) and l.strip()[:1].isdigit():
            lam = float(n[0]); xs = None
            res.setdefault('poisson_rows', []).append([p, l.rstrip()[:130]])
json.dump(res, open(sys.argv[2], 'w'), indent=0)
for k, v in res['tables'].items(): print('%-22s %s' % (k, v))
print('cells that differ:', sum(1 for c in res['cells'] if c[5] == 'DIFFERS'), '| last digit:', sum(1 for c in res['cells'] if c[5] == 'last digit'), '| rows skipped:', len(res.get('skipped', [])))
for c in res['cells']:
    if c[5] == 'DIFFERS': print('  ', c)
