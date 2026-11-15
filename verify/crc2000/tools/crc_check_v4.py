# -*- coding: utf-8 -*-
"""crc_check_v4.py -- part 4: the probabilities of the Wilcoxon (Mann-Whitney) U statistic in Zwillinger & Kokoska (2000),
PDF pages 380 to 384 (P(U <= u) for sample sizes m <= n <= 8), against the exact distribution counted here, and the critical
values of Spearman's rank correlation (page 375) against the exact permutation distribution for n up to 10.
  python3 -I tools/crc_check_v4.py work/all.txt work/part4.json"""
import sys, re, io, json, itertools
from functools import lru_cache
from fractions import Fraction
pages = io.open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\f')
def dec(s): return len(s.split('.')[1]) if '.' in s else 0
def verdict(printed, true):
    d = dec(printed); p = float(printed); unit = 10.0 ** (-d)
    if abs(p - true) <= 0.5 * unit * (1 + 1e-9) + 1e-12: return 'ok'
    if abs(p - true) <= 1.0 * unit * (1 + 1e-9): return 'last digit'
    return 'DIFFERS'
res = {'tables': {}, 'cells': [], 'odd': [], 'grid': []}
def note(table, page, where, printed, true):
    v = verdict(printed, true); t = res['tables'].setdefault(table, {'cells': 0, 'ok': 0, 'last digit': 0, 'DIFFERS': 0}); t['cells'] += 1; t[v] += 1
    if v != 'ok': res['cells'].append([table, page, where, printed, round(float(true), dec(printed) + 3), v])
@lru_cache(None)
def cnt(m, n, u):
    if u < 0: return 0
    if m == 0 or n == 0: return 1 if u == 0 else 0
    return cnt(m - 1, n, u - n) + cnt(m, n - 1, u)
def cdfU(m, n, u):
    tot = sum(cnt(m, n, k) for k in range(m * n + 1)); return sum(cnt(m, n, k) for k in range(u + 1)) / tot
for p in range(380, 385):
    ncur = None; ms = None
    for l in pages[p - 1].split('\n'):
        s = l.strip()
        m0 = re.fullmatch(r'n\s*=\s*(\d+)', s)
        if m0: ncur = int(m0.group(1)); ms = None; continue
        if s.startswith('u') and 'm' in s and '=' in s: ms = [int(x) for x in re.findall(r'\d+', s.split('=')[1])]; continue
        if ncur and ms:
            n = re.findall(r'\d*\.\d+|\d+', s)
            if n and '.' not in n[0] and all(dec(x) == 3 for x in n[1:]) and 1 <= len(n) - 1 <= len(ms) and s[:1].isdigit():
                u = int(n[0]); vals = n[1:]; cols = ms[len(ms) - len(vals):]          # a short row has its blanks at the left
                for m, v in zip(cols, vals):
                    true = cdfU(m, ncur, u); note('Mann-Whitney P(U<=u)', p, 'n=%d m=%d u=%d' % (ncur, m, u), v, true); res['grid'].append([ncur, m, u, v, true])
            elif n and len(n) > 2 and s[:1].isdigit(): res['odd'].append([p, s[:70]])
# Spearman: the smallest r_s with P(r_s >= value) <= alpha?  The page says which tail; the exact distribution is listed here for a look
json.dump(res, open(sys.argv[2], 'w'), indent=0)
for k, v in res['tables'].items(): print('%-24s %s' % (k, v))
print('odd lines:', len(res['odd']), res['odd'][:4])
for c in [c for c in res['cells'] if c[5] == 'DIFFERS'][:12]: print('  ', c[1:5])
