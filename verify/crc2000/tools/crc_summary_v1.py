# crc_summary_v1.py : gather every check of Zwillinger & Kokoska (2000) into one list of tables, with the pages each
# stands on, the cells read, the cells off by one unit in the last place and the cells wrong by more; then count wrong cells
# page by page for the error model.  Writes work/summary.json and prints the list.
import json, os, sys, collections, glob
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work')
def res(name):
    d = json.load(open(os.path.join(W, 'res_%s.json' % name)))
    return d['counts'], d['pages'], d['flag']
P = {k: json.load(open(os.path.join(W, 'part%d.json' % k))) for k in (1, 2, 3, 4)}
def part(k, names):
    n = l = w = 0; flags = []
    for nm in names:
        t = P[k]['tables'][nm]; n += t['cells']; l += t['last digit']; w += t['DIFFERS']
        flags += [[c[1], c[2], '', c[3], c[4], 'DIFF' if c[5] == 'DIFFERS' else 'last'] for c in P[k]['cells'] if c[0] == nm]
    return n, l, w, flags

T = []   # each: dict(name, pages(list), n, last, wrong, kind, note, bypage{page: wrong})
def add(name, pages, n, last, wrong, kind, note, flags=None, bypage=None, label_cells=0):
    bp = collections.Counter()
    if bypage: bp.update(bypage)
    elif flags:
        for f in flags:
            if f[5] == 'DIFF': bp[f[0]] += 1
    if wrong and not bp and len(pages) == 1: bp[pages[0]] = wrong
    assert sum(bp.values()) == wrong, (name, sum(bp.values()), wrong)
    T.append(dict(name=name, pages=list(pages), n=n, last=last, wrong=wrong, kind=kind, note=note, bypage=dict(bp), label_cells=label_cells))
def R(name, title, kind='clean', note='', pages=None, drop_diff=False):
    c, pg, fl = res(name)
    n = sum(c.values()); w = 0 if drop_diff else c['DIFF']
    add(title, pages or list(range(pg[0], pg[-1] + 1)), n, c['last'], w, kind, note, flags=None if drop_diff else fl)

# ---- Chapter 4 ----
R('order_statistics', 'Expected values of normal order statistics', 'last digit', '77 of 399 cells off by one in the fourth decimal; the example on p.75 quotes 1.1630 where the table prints 1.1629')
R('order_stat_covariances', 'Variances and covariances of normal order statistics', 'label', 'the numbers are right; the heading says E[X(i)X(j)] is shown, but the entries are the covariances')
R('range_integral', 'Probability integral of the range')
n, l, w, fl = part(3, list(P[3]['tables']))
add('Studentized range, upper 1%, 5%, 10% points', [87, 88, 89], n, l, w, 'miscalculation', 'half the cells at 1% and 5% differ from the true values; Kokoska and Nevison (1989) print the right values', flags=fl)
# ---- Chapter 5 ----
n, l, w, fl = part(2, ['binomial cdf']); add('Cumulative binomial probabilities', range(96, 101), n, l, w, 'clean', '', flags=fl)
c1 = res('geometric_pmf')[0]; c2 = res('geometric_cdf')[0]
add('Geometric distribution, probability and cumulative', [102], sum(c1.values()) + sum(c2.values()), 0, 0, 'clean', 'the worked example above the table has 0.656 for 0.0656 in a sum')
R('hypergeometric', 'Hypergeometric probability and distribution functions')
add('Negative binomial probabilities', [112], 126, 1, 5, 'misprint', 'the last column carries a fifth digit, always 0, that is not a real digit: seven cells, five of them wrong as printed')
n, l, w, fl = part(2, ['Poisson cdf']); add('Cumulative Poisson probabilities', range(114, 119), n, l, w, 'clean', '', flags=fl)
# ---- Chapter 6 ----
n, l, w, fl = part(1, ['chi-square critical']); add('Chi-square critical values', range(130, 134), n, l, w, 'clean', '', flags=fl)
R('chi2_over_df', 'Chi-square over degrees of freedom', 'unknown', '500 df: 0.810 for 0.805 and 1.111 for 1.106')
n, l, w, fl = part(2, [k for k in P[2]['tables'] if k.startswith('F ')]); add('F critical values, six levels', range(141, 147), n, l, w, 'misprint', '6336 for 6366 (1%, numerator infinity, denominator 1); still printed in the 31st (2003) and 33rd (2018) editions of the CRC Standard Mathematical Tables', flags=fl)
n, l, w, fl = part(1, ['t critical'])
add("Student's t critical values", [166], n, l, w, 'label + misprint', 'the last two columns are headed 0.0025 and 0.001 but hold the values for 0.001 and 0.0005 (72 cells); 0.290 for 1.290 at 100 df; "3.69o" at 27 df', flags=fl, label_cells=72)
# ---- Chapter 7 ----
n, l, w, fl = part(1, ['normal f(z)', 'normal F(z)', 'normal 1-F(z)']); add('Normal distribution: f(z), F(z), 1 - F(z)', range(176, 185), n, l, w, 'clean', '', flags=fl)
R('normal_critical_7_1', 'Table 7.1, critical values of the normal distribution')
c, pg, fl = res('tolerance_headed_WaldWolf')
add('Tolerance factors for normal distributions', [186], 216, c['last'], c['DIFF'], 'label + approximation', 'the headings P and alpha are exchanged against the book\'s own definitions (162 of 216 cells wrong as headed; 1989 has them as gamma and 1 - alpha); the numbers are the Wald-Wolfowitz approximation (171 differ from the exact factors, by 3% at n = 2)', flags=fl, label_cells=216)
c, pg, fl = res('correlation_r'); add('Percentage points of the correlation coefficient', [193], 186, 0, 0, 'clean', 'the six cells of the first row, printed in a short form, were checked by hand')
c, pg, fl = res('circular_normal')
add('Circular normal probabilities', [194], 198, c['last'], c['DIFF'], 'label', 'every row label is one row too low: the row marked 0.2 holds the values for 0.1, and so on; with the labels moved up one row all 198 cells are exact', flags=fl, label_cells=198)
R('circular_error', 'Circular error probabilities')
# ---- Chapters 8, 9 ----
c1 = res('estimators_mean')[0]; c2 = res('estimators_range')[0]
add('Estimators of the mean and of sigma (variances, efficiencies)', [202], sum(c1.values()) + sum(c2.values()), 0, 0, 'clean', 'the best-linear-estimate part was not checked')
c, pg, fl = res('critical_9_1'); add('Table 9.1, common critical values', [206], 50, c['last'], c['DIFF'], 'misprint', 'the last row is printed with a fourth decimal that is a padding zero (1074.6790 for 1074.6794)', flags=fl)
c, pg, fl = res('t_over_root_n'); add('Table of t over root n (p.209)', [209], 36, c['last'], 36, 'label', 'the columns are headed z(alpha/2)/sqrt(n); the numbers are t(alpha/2, n-1)/sqrt(n) (8.99 at n = 2, where z gives 1.39)', bypage={209: 36}, label_cells=36)
R('median_k1k2', 'Table 9.6, k1 and k2 for the median interval', note='checked against the formula the book gives')
R('median_ci', 'Table 9.7, order statistics for the median interval')
R('poisson_limits', 'Confidence limits for a Poisson mean')
c1, p1, f1 = res('proportion_limits_95'); c2, p2, f2 = res('proportion_limits_99')
add('Confidence limits of proportions, 95% and 99%', range(215, 231), sum(c1.values()) + sum(c2.values()), c1['last'] + c2['last'], 0, 'clean', '')
# ---- Chapter 10 ----
c1, p1, f1 = res('bartlett_0.05'); c2, p2, f2 = res('bartlett_0.01')
add("Bartlett's test critical values", [244, 245], sum(c1.values()) + sum(c2.values()), c1['last'] + c2['last'], c1['DIFF'] + c2['DIFF'], 'unknown', '.1672 for .1670 (1%, n = 3, k = 3)', flags=f1 + f2)
c1, p1, f1 = res('cochran_p247_at_0.05'); c2, p2, f2 = res('cochran_p248_at_0.05'); c3, p3, f3 = res('cochran_p248_at_0.01')
add("Cochran's test critical values", [247, 248], sum(c1.values()) + sum(c2.values()), c1['last'] + c2['last'], c1['DIFF'] + c2['DIFF'], 'label + inherited',
    'the second table is headed alpha = .05 but is the 1%% table (headed rightly in 1989), so %d of its 252 cells are wrong as headed; read at the right level, %d cells of the two tables are off by 2 or 3 in the fourth decimal, as in the 1947 source' % (c2['DIFF'], c1['DIFF'] + c3['DIFF']), flags=f1 + f2, label_cells=252)
R('variance_R', 'Values of R for the variance test', 'unknown', '150 df, beta = 0.5: 1.297 for 1.294 and 1.206 for 1.203')
cs = [res('dixon_' + k) for k in ('r10', 'r11', 'r20')]
add("Dixon's ratios r10, r11, r20", [251], sum(sum(c[0].values()) for c in cs), sum(c[0]['last'] for c in cs), sum(c[0]['DIFF'] for c in cs), 'inherited + misprint', 'Dixon\'s 1951 tables are known to hold errors (McBane 2006); .745 for .765 (r10, n = 4, 5%) is not among those and looks like a misprint', flags=sum((c[2] for c in cs), []))
# 2 x 2: the b's and the probabilities
fin = json.load(open(os.path.join(W, 'finney_cells.json')))
from math import isclose
bp = collections.Counter(); wrong_b = wrong_p = last_p = 0
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from crc_lib import verdict
for p, A, B, a, lev, e, b, bt, tail, pmf in fin:
    if b != bt: wrong_b += 1; bp[p] += 1; continue
    v = verdict('0.' + e.split('.')[1], tail)
    if v == 'DIFF': wrong_p += 1; bp[p] += 1
    elif v == 'last': last_p += 1
add('2 x 2 contingency tables (critical b and its probability)', range(254, 268), 6144, last_p, wrong_b + wrong_p, 'miscalculation',
    'the probability printed is that of the single table, not the one-tail probability the text describes: %d critical values are one too large, %d probabilities are wrong by more than a unit in the third decimal and %d by one unit; the example on p.253 quotes 1.035 where the table prints 1.034' % (wrong_b, wrong_p, last_p), bypage=bp)
R('orthogonal_polynomials', 'Orthogonal polynomials', note='the blocks for 3, 4 and 5 points were not read')
# ---- Chapter 12 ----
cs = [res('duncan_' + k) for k in ('0.05', '0.01', '0.001')]
add("Duncan's multiple range test", [294, 295, 296], sum(sum(c[0].values()) for c in cs), sum(c[0]['last'] for c in cs), sum(c[0]['DIFF'] for c in cs), 'last digit', '300 of 1,713 cells off by one in the last place', flags=sum((c[2] for c in cs), []))
c1, p1, f1 = res('dunnett_two-sided_0.05'); c1b, p1b, f1b = res('dunnett_two-sided_0.05_rows10to24'); c2, p2, f2 = res('dunnett_two-sided_0.01')
add("Dunnett's two-sided critical values, 5% and 1%", [297, 298], sum(c1.values()) + sum(c1b.values()) + sum(c2.values()), c1['last'] + c1b['last'] + c2['last'], c1['DIFF'] + c1b['DIFF'] + c2['DIFF'], 'inherited',
    'the 1955 values, too large for three or more treatments (3.39 for 3.29 at 5 df, k = 3); Dunnett gave new two-sided tables in 1964', flags=f1 + f1b + f2)
c1, p1, f1 = res('dunnett_one-sided_0.05'); c2, p2, f2 = res('dunnett_one-sided_0.01')
add("Dunnett's one-sided critical values, 5% and 1%", [298, 299], sum(c1.values()) + sum(c2.values()), c1['last'] + c2['last'], 0, 'clean', '')
# ---- Chapter 14 ----
R('kendall_S', "Kendall's rank correlation, distribution of S")
R('ks_one_sample_1sided', 'Kolmogorov-Smirnov one-sample critical values')
c, pg, fl = res('ks_two_sample_le')
add('Kolmogorov-Smirnov two-sample critical values', [357], 150, 0, 8, 'unknown + misprint', '8 of 150 cells wrong (the two values for 12 and 12 stand in each other\'s places; 5 and 5 has asterisks where 25/25 belongs); 36/35 for 36/36', flags=fl)
R('kruskal_wallis', 'Kruskal-Wallis exact probability levels')
c1 = res('runs')[0]; c2 = res('runs_m_equals_n')[0]; c3 = res('runs_m_equals_n_moments')[0]
add('Distribution of the total number of runs', range(362, 372), sum(c1.values()) + sum(c2.values()) + sum(c3.values()), 0, 0, 'clean', '')
c, pg, fl = res('sign_test'); add('Critical values for the sign test', [373], 178 + 22, 0, 22, 'misprint', '22 cells print 0 where no value satisfies the rule the page gives (n = 1 at every level, for instance)', bypage={373: 22})
c, pg, fl = res('spearman_critical')
add("Spearman's rank correlation, critical values", [375], 56, 0, 2, 'unknown', 'n = 12 and 13 at 0.001 are one step off the rule the other 42 exact cells follow; n = 20 agrees by simulation; two of the four cells for n = 30 are too close to call', flags=fl)
R('spearman_exact', "Spearman's rank correlation, exact tail probabilities", 'misprint', 'in the n = 6 column 0.5000 stands three times instead of twice and the rest of the column is one row low (18 cells), ending with a probability for S = 72, which cannot occur')
R('signed_rank_critical', 'Wilcoxon signed-ranks critical values')
add('Mann-Whitney U, probabilities', range(380, 385), 385, 0, 0, 'clean', '12 cells on p.381, where two blocks stand side by side, were not read')
cs = [res('mw_critical_%s_one-sided' % k) for k in ('0.1', '0.05', '0.025', '0.01', '0.005', '0.001', '0.0005')]
add('Mann-Whitney U, critical values at seven levels', range(385, 389), sum(sum(c[0].values()) for c in cs), 0, 0, 'label', 'in the 0.10 table the row for 18 is labelled 8 (its 19 numbers are right)', label_cells=19)
# ---- Chapter 15, 17, 18 ----
R('control_chart', 'Factors for control chart lines', 'inherited', 'D1 and D2 at n = 12, 14, 15 are off by 2 to 4 in the third decimal (they follow from d3 kept to three places)')
R('permutations', 'Permutations'); R('combinations', 'Combinations')
c1 = res('bessel_JY')[0]; c2 = res('bessel_IK')[0]; add('Bessel functions J, Y, I, K', [513, 515], sum(c1.values()) + sum(c2.values()), c1['last'] + c2['last'], 0, 'clean', '')
R('beta_function', 'Beta function'); R('factorials', 'Factorials, double factorials and their logarithms'); R('gamma_function', 'Gamma function')
R('partitions', 'Partitions')
c, pg, fl = res('stirling_first'); add('Stirling numbers of the first kind', [529], c['ok'], 0, 0, 'clean', '')
R('stirling_second', 'Stirling numbers of the second kind')
c, pg, fl = res('sums_of_powers'); add('Sums of powers of integers', [531], c['ok'], 0, 0, 'clean', '')

tot = dict(tables=len(T), cells=sum(t['n'] for t in T), last=sum(t['last'] for t in T), wrong=sum(t['wrong'] for t in T),
           pages=len(set(p for t in T for p in t['pages'])))
bypage = collections.Counter(); cells_by_page = collections.Counter()
for t in T:
    for p, w in t['bypage'].items(): bypage[int(p)] += w
allpages = sorted(set(p for t in T for p in t['pages']))
json.dump(dict(tables=T, totals=tot, bypage={p: bypage.get(p, 0) for p in allpages}), open(os.path.join(W, 'summary.json'), 'w'), indent=1)
if __name__ == '__main__':
    print('%-58s %-9s %6s %5s %6s  %s' % ('table', 'pages', 'cells', 'last', 'wrong', 'kind'))
    for t in T:
        pg = t['pages']; ps = '%d' % pg[0] if len(pg) == 1 else '%d-%d' % (pg[0], pg[-1])
        print('%-58s %-9s %6d %5d %6d  %s' % (t['name'][:58], ps, t['n'], t['last'], t['wrong'], t['kind']))
    print(tot)
    print('tables with wrong cells or a label fault:', sum(1 for t in T if t['wrong'] or t['label_cells']), 'of', len(T))
    print('pages with at least one wrong cell:', sum(1 for p in allpages if bypage.get(p, 0) > 0), 'of', len(allpages))
