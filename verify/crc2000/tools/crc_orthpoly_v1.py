# crc_orthpoly_v1.py : the tables of orthogonal polynomials (pp.285-288) against polynomials built afresh
import sys, re, math
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
from fractions import Fraction
from functools import reduce

def orth(n, deg):
    """integer-valued orthogonal polynomials xi_1..xi_deg on n equally spaced points, their D and lambda"""
    xs = [Fraction(2 * i - n - 1, 2) for i in range(1, n + 1)]
    basis = [[Fraction(1)] * n]; out = []
    for j in range(1, deg + 1):
        v = [x ** j for x in xs]
        for b in basis:
            c = sum(a * bb for a, bb in zip(v, b)) / sum(bb * bb for bb in b)
            v = [a - c * bb for a, bb in zip(v, b)]
        basis.append(v)                                    # monic polynomial of degree j at the points
        den = reduce(lambda a, b: a * b // math.gcd(a, b), [f.denominator for f in v], 1)
        iv = [int(f * den) for f in v]; g = reduce(math.gcd, [abs(a) for a in iv])
        iv = [a // g for a in iv]; lam = Fraction(den, g)
        out.append((iv, sum(a * a for a in iv), lam))
    return xs, out

T = Tally('orthogonal_polynomials', 'Orthogonal polynomials: values, D and lambda')
unread = 0; blocks_seen = []
for p in range(285, 289):
    blocks = None; rows = {}
    for ln in L(p):
        hs = [(m.start(), int(m.group(1))) for m in re.finditer(r'n\s*=\s*(\d+)\s*points', ln)]
        if hs:
            if blocks:
                for b in blocks: blocks_seen.append((p, b[1], rows.get(b[1], [])))
            blocks = [(s, n) for s, n in hs]; rows = {n: [] for s, n in hs}; continue
        if not blocks: continue
        tk = toks(ln)
        if not tk: continue
        if any(t.startswith('ξ') for a, b, t in tk):
            x1 = [a for a, b, t in tk if t == 'ξ1']
            if len(x1) == len(blocks): blocks = [(x1[i] + 4, blocks[i][1]) for i in range(len(blocks))]
            continue
        if all(n >= 6 for s_, n in blocks):
            # rows of five numbers (D and lambda rows carry a label first): cut the line into such groups in order,
            # and give each group to the block whose first column is nearest
            i = 0; grp = []
            while i < len(tk):
                lab = tk[i][2] in ('D', 'λ'); m = 6 if lab else 5
                if i + m > len(tk): grp = None; break
                grp.append(tk[i:i + m]); i += m
            if grp is None: unread += 1; continue
            for g in grp:
                bi = min(range(len(blocks)), key=lambda q: abs(blocks[q][0] - 4 - g[0][0]))
                key = (ln, bi)
                for a, b_, t in g: rows[blocks[bi][1]].append((key, a, clean(t)))
            continue
        for a, b, t in tk:
            bi = max([i for i, (s, n) in enumerate(blocks) if a >= s - 10] or [0])
            rows[blocks[bi][1]].append((ln, a, clean(t)))
    if blocks:
        for b in blocks: blocks_seen.append((p, b[1], rows.get(b[1], [])))
for p, n, toklist in blocks_seen:
    # group the tokens of this block back into lines
    lines = {}
    for ln, a, t in toklist: lines.setdefault(ln if isinstance(ln, tuple) else (ln, 0), []).append(t)
    deg = min(5, n - 1); xs, O = orth(n, deg); lam1 = O[0][2]
    for tks in lines.values():
        if tks[0] == 'D':
            for j, t in enumerate(tks[1:deg + 1]):
                if re.match(r'^-?\d+$', t): T.add(p, 'n %d' % n, 'D%d' % (j + 1), t, O[j][1])
            continue
        if tks[0] == 'λ':
            for j, t in enumerate(tks[1:deg + 1]):
                try: v = Fraction(t)
                except Exception: unread += 1; continue
                T.c['ok' if v == O[j][2] else 'DIFF'] += 1; T.pages.add(p)
                if v != O[j][2]: T.flag.append([p, 'n %d' % n, 'lambda%d' % (j + 1), t, float(O[j][2]), 'DIFF'])
            continue
        if not all(re.match(r'^-?\d+$', t) for t in tks) or len(tks) != deg: unread += 1; continue
        x = Fraction(int(tks[0])) / lam1
        if x not in xs: unread += 1; continue
        i = xs.index(x)
        for j, t in enumerate(tks):
            T.add(p, 'n %d x %s' % (n, x), 'xi%d' % (j + 1), t, O[j][0][i])
if unread: T.note('%d lines of the blocks were not read as rows' % unread)
T.note('blocks: ' + ' '.join('%d' % n for p, n, t in blocks_seen))
T.done(show=10)
