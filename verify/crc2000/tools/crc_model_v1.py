# crc_model_v1.py : a model for the errors found in the tables of Zwillinger & Kokoska (2000).
# Two counts for each of the table pages checked:
#   slips   separate faults of one cell, one label or one heading (a misprint, a wrong label, a duplicated or exchanged entry)
#   wrong   numbers that are wrong as printed (the label taken at its word), by more than one unit in the last place
# For each: the Poisson fit (Student 1907 counted yeast cells this way), the index of dispersion, the negative binomial fit
# (Greenwood & Yule 1920; Student 1919 on why counts stray from Poisson's law), and 95% intervals for the mean per page.
import json, os, math, sys, collections
import numpy as np
from scipy import stats, optimize
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work')
S = json.load(open(os.path.join(W, 'summary.json')))
pages = sorted(int(p) for p in S['bypage'])
wrong = np.array([S['bypage'][str(p)] if str(p) in S['bypage'] else S['bypage'][p] for p in pages], dtype=float)
# separate slips inside tables, by page (each listed in the report)
slip_pages = {77: 1, 112: 1, 134: 2, 144: 1, 166: 3, 186: 1, 194: 1, 206: 1, 209: 1, 245: 1, 248: 1, 249: 2, 251: 1, 357: 7, 375: 2, 376: 1, 385: 1}
assert all(p in pages for p in slip_pages), [p for p in slip_pages if p not in pages]
slips = np.array([slip_pages.get(p, 0) for p in pages], dtype=float)
out = {}
def garwood(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.chi2.ppf(a / 2, 2 * k) / 2
    hi = stats.chi2.ppf(1 - a / 2, 2 * k + 2) / 2
    return lo / n, hi / n
def wilson(k, n, a=0.05):
    z = stats.norm.isf(a / 2); p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h
def nbfit(x):
    m = x.mean()
    def nll(lr):
        r = math.exp(lr); p = r / (r + m)
        return -np.sum(stats.nbinom.logpmf(x, r, p))
    o = optimize.minimize_scalar(nll, bounds=(-12, 8), method='bounded')
    return math.exp(o.x), -o.fun
def nb_profile_ci(x, a=0.05):
    """profile-likelihood interval for the mean of a negative binomial"""
    def best(m):
        def nll(lr):
            r = math.exp(lr); p = r / (r + m)
            return -np.sum(stats.nbinom.logpmf(x, r, p))
        return -optimize.minimize_scalar(nll, bounds=(-12, 8), method='bounded').fun
    m0 = x.mean(); l0 = best(m0); cut = l0 - stats.chi2.ppf(1 - a, 1) / 2
    lo = optimize.brentq(lambda m: best(m) - cut, m0 * 1e-3, m0)
    hi = optimize.brentq(lambda m: best(m) - cut, m0, m0 * 200)
    return lo, hi
rng = np.random.default_rng(15112026)
def describe(name, x):
    n = len(x); k = int(x.sum()); m = x.mean(); v = x.var(ddof=1); idx = v / m
    d = dict(pages=n, total=k, mean=m, variance=v, index_of_dispersion=idx,
             dispersion_chi2=(n - 1) * idx, dispersion_p=float(stats.chi2.sf((n - 1) * idx, n - 1)),
             pages_with_none=int((x == 0).sum()), poisson_expected_none=n * math.exp(-m),
             poisson_ci=garwood(k, n))
    r, ll = nbfit(x); d['nb_size'] = r; d['nb_expected_none'] = n * float(stats.nbinom.pmf(0, r, r / (r + m)))
    d['nb_ci'] = nb_profile_ci(x)
    bs = np.array([rng.choice(x, size=n, replace=True).mean() for _ in range(20000)])
    d['bootstrap_ci'] = (float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)))
    llp = float(np.sum(stats.poisson.logpmf(x, m))); d['loglik_poisson'] = llp; d['loglik_nb'] = ll
    # observed and expected numbers of pages with 0, 1, 2, 3 or more
    obs = [int((x == j).sum()) for j in range(3)] + [int((x >= 3).sum())]
    ep = [n * float(stats.poisson.pmf(j, m)) for j in range(3)]; ep.append(n - sum(ep))
    en = [n * float(stats.nbinom.pmf(j, r, r / (r + m))) for j in range(3)]; en.append(n - sum(en))
    d['observed_0_1_2_3plus'] = obs; d['poisson_expected'] = ep; d['nb_expected'] = en
    out[name] = d
    print('== %s: %d on %d pages; mean %.3f a page; variance %.3f; index of dispersion %.2f (chi-square %.0f on %d df, p %.2g)' % (name, k, n, m, v, idx, (n - 1) * idx, n - 1, d['dispersion_p']))
    print('   pages with 0, 1, 2, 3+: observed %s | Poisson %s | negative binomial (size %.3f) %s' % (obs, ['%.1f' % e for e in ep], r, ['%.1f' % e for e in en]))
    print('   95%% interval for the mean a page: Poisson (exact) %.3f to %.3f | negative binomial (profile) %.3f to %.3f | bootstrap over pages %.3f to %.3f' % (*d['poisson_ci'], *d['nb_ci'], *d['bootstrap_ci']))
    print('   log-likelihood: Poisson %.1f, negative binomial %.1f' % (llp, ll))
describe('slips', slips)
describe('wrong numbers', wrong)
# proportions
T = S['tables']; nt = len(T)
faulty = sum(1 for t in T if t['wrong'] or t['label_cells'] or t['name'].startswith('Variances and cov'))
pw = int((wrong > 0).sum())
print('tables with a wrong number or a wrong label: %d of %d = %.1f%% (Wilson 95%% %.1f%% to %.1f%%)' % (faulty, nt, 100 * faulty / nt, *(100 * v for v in wilson(faulty, nt))))
print('pages with at least one wrong number: %d of %d = %.1f%% (Wilson 95%% %.1f%% to %.1f%%)' % (pw, len(pages), 100 * pw / len(pages), *(100 * v for v in wilson(pw, len(pages)))))
cells = np.array([t['n'] for t in T], dtype=float); wr = np.array([t['wrong'] for t in T], dtype=float); la = np.array([t['last'] for t in T], dtype=float)
print('cells %d; wrong %d = %.2f%%; off by one in the last place %d = %.2f%%' % (cells.sum(), wr.sum(), 100 * wr.sum() / cells.sum(), la.sum(), 100 * la.sum() / cells.sum()))
bs = []
for _ in range(20000):
    i = rng.integers(0, nt, nt); bs.append(wr[i].sum() / cells[i].sum())
print('   95%% interval for the share of wrong cells, resampling whole tables: %.2f%% to %.2f%%' % (100 * np.quantile(bs, 0.025), 100 * np.quantile(bs, 0.975)))
order = np.argsort(-wr); top = order[:6]
print('   the six worst tables hold %d of the %d wrong cells (%.1f%%): %s' % (wr[top].sum(), wr.sum(), 100 * wr[top].sum() / wr.sum(), '; '.join('%s %d' % (T[i]['name'][:28], wr[i]) for i in top)))
rest = [i for i in range(nt) if i not in set(top)]
print('   in the other %d tables: %d wrong in %d cells = %.3f%%' % (len(rest), wr[rest].sum(), cells[rest].sum(), 100 * wr[rest].sum() / cells[rest].sum()))
out['proportions'] = dict(tables=nt, faulty_tables=faulty, pages=len(pages), pages_with_wrong=pw, cells=float(cells.sum()), wrong=float(wr.sum()), last=float(la.sum()),
                          share_ci=(float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))), top6=float(wr[top].sum()), rest_wrong=float(wr[rest].sum()), rest_cells=float(cells[rest].sum()))
json.dump(out, open(os.path.join(W, 'model.json'), 'w'), indent=1)
