# crc_ours_v2.py REPO : our own arithmetic beside the book's tables.
#   RankLab beta 1i through the PC harness: rk_SRNull (signed ranks), rk_KdNull (Kendall), rk_SpPerm (Spearman, n <= 7),
#   rk_MWNull (Mann-Whitney critical values); hpstats.py: clopper_pearson_ci, studentized_range_crit.
# For each cell: does our value round to the printed one?  Where it does not, the checks of the book say which is right.
import sys, os, re, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from crc_lib import *
repo = sys.argv[1]; only = set(sys.argv[2:])
def want(n): return (not only) or (n in only)
out = {}
def report(name, n, agree, differ, note=''):
    out[name] = dict(cells=n, agree=agree, differ=differ, note=note)
    print('%-44s cells %5d  ours = printed %5d  ours differs %4d  %s' % (name, n, agree, differ, note)); sys.stdout.flush()
    json.dump(out, open(os.path.join(W, 'ours_v2_%s.json' % ('_'.join(sorted(only)) or 'all')), 'w'), indent=1)

if want('ranklab'):
    sys.path.insert(0, os.path.join(repo, 'tools'))
    from ppl_run_v3e import Harness
    h = Harness(os.path.join(repo, 'programs', 'RankLab_beta1i.txt'), idle_key=4, home_minus=True, cas='fail')
    G = h.globals_
    def lst(v): return [float(x) for x in v]
    # ---- signed ranks
    ns = None; n_ = ag = 0
    for ln in L(379):
        tk = [t for a, b, t in toks(ln)]
        if 'sided' in tk and 'n' in tk: ns = [int(t) for t in tk[tk.index('=') + 1:]]; continue
        if ns and tk[:2] == ['α', '='] and len(tk) >= 7:
            a1 = float(tk[2]); vals = tk[6:]
            for t, n in zip(reversed(vals), reversed(ns)):
                h.execute('rk_SRNull({%s})' % ','.join(str(i) for i in range(1, n + 1)))
                c = lst(G['rkNull']); den = float(G['rkNDen']); cum = 0; crit = -1
                for j, v in enumerate(c):
                    cum += v
                    if cum / den <= a1 * (1 + 1e-12): crit = j
                    else: break
                n_ += 1; ag += int(t) == crit
    report('RankLab rk_SRNull: signed-ranks critical', n_, ag, n_ - ag)
    # ---- Kendall
    hdr = None; n_ = ag = 0; cache = {}
    for ln in L(352):
        tkp = toks(ln); tk = [t for a, b, t in tkp]
        if tk and tk[0] == 'St' and len(tk) > 4:
            hh = [(a, b, t.replace('n=', '')) for a, b, t in tkp[1:] if t not in ('n', '=')]
            hdr = [(a, b, t) for a, b, t in hh if t.isdigit()]; continue
        if hdr and len(tk) >= 2 and tk[0].isdigit() and all(isnum(t) and '.' in t for t in tk[1:]):
            s = int(tk[0]); cells = tkp[1:]
            idx = list(range(len(cells))) if len(cells) == len(hdr) else [min(range(len(hdr)), key=lambda i: abs((hdr[i][0] + hdr[i][1]) / 2 - (a + b) / 2)) for a, b, t in cells]
            for (a, b, t), ci in zip(cells, idx):
                n = int(hdr[ci][2])
                if n not in cache:
                    h.execute('rk_KdNull(%d)' % n); cache[n] = (lst(G['rkKNl']), float(G['rkKDen']))
                c, den = cache[n]; n0 = n * (n - 1) // 2
                # entry j (from 1) is tau = -1 + 2(j-1)/n0, that is S = -n0 + 2(j-1)
                p = sum(v for j, v in enumerate(c) if -n0 + 2 * j >= s) / den
                n_ += 1; ag += verdict(t, p) == 'ok'
    report('RankLab rk_KdNull: Kendall P(S >= s)', n_, ag, n_ - ag)
    # ---- Spearman exact, n <= 7
    hdr = None; n_ = ag = 0; cache = {}; dif = []
    for p in (376, 377):
        for ln in L(p):
            tkp = toks(ln); tk = [t for a, b, t in tkp]
            if tk and tk[0].startswith('n=') or tk[:2] == ['n', '=']:
                hh = [(a, b, t.replace('n=', '')) for a, b, t in tkp if t not in ('n', '=')]
                hdr = [(a, b, t) for a, b, t in hh if t.isdigit()]; continue
            if hdr and len(tk) >= 2 and tk[0].isdigit() and all(isnum(t) and '.' in t for t in tk[1:]):
                S = int(tk[0]); cells = tkp[1:]
                idx = list(range(len(cells))) if len(cells) == len(hdr) else [min(range(len(hdr)), key=lambda i: abs((hdr[i][0] + hdr[i][1]) / 2 - (a + b) / 2)) for a, b, t in cells]
                for (a, b, t), ci in zip(cells, idx):
                    n = int(hdr[ci][2])
                    if n > 7 or n < 3: continue
                    if n not in cache:
                        seq = ','.join(str(i) for i in range(1, n + 1))
                        h.execute('rk_SpPerm({%s},{%s})' % (seq, seq))
                        cache[n] = (lst(G['rkSNl']), float(G['rkSLo']), float(G['rkSSt']), float(G['rkSDen']))
                    c, lo, st, den = cache[n]; D = n * (n * n - 1)
                    sd = [(1 - (lo + j * st)) * D / 6.0 for j in range(len(c))]         # sum of d squared for each bar
                    mid = D / 6.0
                    pr = sum(v for v, x in zip(c, sd) if (x <= S + 1e-6 if S <= mid else x >= S - 1e-6)) / den
                    n_ += 1; ok = verdict(t, pr) == 'ok'; ag += ok
                    if not ok: dif.append('n %d S %d' % (n, S))
    report('RankLab rk_SpPerm: Spearman exact tails, n 3-7', n_, ag, n_ - ag, 'differs at: ' + ', '.join(dif[:4]) + (' ...' if len(dif) > 4 else ''))
    # ---- Mann-Whitney critical values
    n_ = ag = 0; cache = {}
    for p in range(385, 389):
        level = None; ns = None
        for ln in L(p):
            m = re.search(r'α\s*=\s*(0?\.\d+)\s+level', ln)
            if m: level = float(m.group(1)); continue
            tk = [t for a, b, t in toks(ln)]
            if tk[:3] == ['m', 'n', '=']: ns = [int(t) for t in tk[3:]]; continue
            if level and ns and tk and all(t.isdigit() for t in tk) and len(tk) >= 2:
                mm = int(tk[0]); vals = tk[1:]
                if mm == 8 and len(vals) == 19 and int(vals[-1]) > 100: mm = 18      # the row the page labels 8 in the 0.10 table
                for t, n in zip(reversed(vals), reversed(ns)):
                    key = (min(mm, n), max(mm, n))
                    if key not in cache:
                        h.execute('rk_MWNull(%d,%d)' % key); cache[key] = (lst(G['rkNull']), float(G['rkNDen']))
                    c, den = cache[key]; cum = 0; crit = -1
                    for j, v in enumerate(c):
                        cum += v
                        if cum / den <= level * (1 + 1e-12): crit = j
                        else: break
                    n_ += 1; ag += int(t) == crit
    report('RankLab rk_MWNull: Mann-Whitney critical', n_, ag, n_ - ag)

if want('hpstats'):
    sys.path.insert(0, os.path.join(repo, 'python'))
    import hpstats
    for conf, pr in ((0.95, range(215, 223)), (0.99, range(223, 231))):
        n_ = ag = 0
        for p in pr:
            cols = None; x = None; nline = 0
            for ln in L(p):
                tk = [t for a_, b_, t in toks(ln)]
                if not tk: continue
                if tk[0] == 'x' and len(tk) > 3: cols = tk[1:]; continue
                if cols is None: continue
                if all(isnum(t) and '.' in t for t in tk) and x is not None and nline == 1: vals = tk; kind = 1; nline = 2
                elif (isnum(tk[0]) and '.' not in tk[0]) or tk[0] == '∞':
                    x = tk[0]; vals = tk[1:]; kind = 0; nline = 1
                    if not all(isnum(t) and '.' in t for t in vals): x = None; continue
                else: continue
                if len(vals) != len(cols) or x == '∞': continue
                for j, v in enumerate(vals):
                    if cols[j] == '∞': continue
                    xi = int(x); n = xi + int(cols[j])
                    lim = hpstats.clopper_pearson_ci(xi, n, conf)[kind]
                    n_ += 1; ag += verdict(v, lim) == 'ok'
        report('hpstats clopper_pearson_ci, %d%%' % round(conf * 100), n_, ag, n_ - ag)
    g = json.load(open(os.path.join(W, 'part3.json')))['grid']
    n_ = ag = 0; right = 0
    for a, k, lab, printed, sp in g:
        df = 1e6 if lab == '∞' else int(lab)
        if df < 3: continue
        q = hpstats.studentized_range_crit(a, k, df)
        n_ += 1; ag += verdict(printed, q) == 'ok'; right += abs(q - sp) < 0.005
    report('hpstats studentized_range_crit, df 3 and up', n_, ag, n_ - ag, 'ours within 0.005 of SciPy in %d' % right)
