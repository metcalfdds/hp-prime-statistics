# crc_spearman_mc.py N_MILLIONS n SEED : Monte Carlo counts of S = sum d^2 at the book's critical values for n (p.375)
# writes work/spmc_<n>_<seed>.json : for each printed value, how many of the N permutations had S <= S_c and S <= S_c - 2
import sys, json, numpy as np, os
NM = int(sys.argv[1]); n = int(sys.argv[2]); seed = int(sys.argv[3])
printed = {20: ['0.2977', '0.3789', '0.5203', '0.6586'], 30: ['0.2400', '0.3059', '0.4251', '0.5479']}[n]
D = n * (n * n - 1)
Sc = [int(round((1 - float(t)) * D / 6.0)) for t in printed]
rng = np.random.default_rng(seed)
base = np.tile(np.arange(n, dtype=np.int16), (500000, 1)); idx = np.arange(n, dtype=np.int16)
thr = sorted(set([s + d for s in Sc for d in (-4, -2, 0, 2, 4)]))
cnt = {t: 0 for t in thr}; N = 0
for it in range(NM * 2):
    p = rng.permuted(base, axis=1)
    S = ((p - idx).astype(np.int32) ** 2).sum(axis=1)
    for t in thr: cnt[t] += int((S <= t).sum())
    N += len(S)
    if it % 100 == 99: json.dump({'n': n, 'N': N, 'Sc': Sc, 'printed': printed, 'cnt': cnt}, open('work/spmc_%d_%d.json' % (n, seed), 'w'))
json.dump({'n': n, 'N': N, 'Sc': Sc, 'printed': printed, 'cnt': cnt}, open('work/spmc_%d_%d.json' % (n, seed), 'w'))
print('done', n, N)
