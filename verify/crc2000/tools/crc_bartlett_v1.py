# crc_bartlett_v1.py : critical values for Bartlett's test with equal sample sizes (pp.244-245), worked afresh.
# b = (geometric mean of the k variances) / (their arithmetic mean).  With a = (n - 1)/2, b^k is distributed as the product
# of k - 1 independent Beta(a, j/k) variables, j = 1 .. k-1 (from the moments of b; Gauss's multiplication formula).
# For k = 2 that is one Beta and the critical value is exact.  For k >= 3 the distribution of Y = -k ln b is found by
# inverting its characteristic function (Gil-Pelaez), and checked for k = 3 against a direct integral and by simulation.
import sys, re, math, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from crc_lib import *
import numpy as np
from scipy import stats, special, optimize, integrate

class Y:
    def __init__(self, k, n, mult=3000.0, per=200.0):
        self.k = k; self.a = a = (n - 1) / 2.0
        U = mult * max(a, 1.0); N = int(mult * per) // 2 * 2
        self.u = np.linspace(0, U, N + 1)[1:]; self.du = U / N
        lp = np.zeros(len(self.u), dtype=complex)
        for j in range(1, k):
            lp += special.loggamma(a - 1j * self.u) - special.loggamma(a) + special.loggamma(a + j / float(k)) - special.loggamma(a + j / float(k) - 1j * self.u)
        self.phi = np.exp(lp)
        self.mean = sum(special.digamma(a + j / float(k)) - special.digamma(a) for j in range(1, k))
        w = np.ones(N + 1); w[1:-1:2] = 4; w[2:-1:2] = 2; self.w = w * self.du / 3.0       # Simpson
    def cdf(self, y):
        g = np.imag(np.exp(-1j * self.u * y) * self.phi) / self.u
        g = np.concatenate(([self.mean - y], g))
        return 0.5 - np.sum(self.w * g) / math.pi
    def crit(self, alpha):
        ya = optimize.brentq(lambda y: self.cdf(y) - (1 - alpha), self.mean * 1e-6, self.mean * 15.0, xtol=1e-12 * self.mean)
        return math.exp(-ya / self.k)

def crit2(alpha, n): return math.sqrt(stats.beta.ppf(alpha, (n - 1) / 2.0, 0.5))

def cdf3_direct(x, n):
    """P(b^3 <= x) for k = 3 by a direct integral over the second Beta."""
    a = (n - 1) / 2.0
    c = 1.0 / special.beta(a, 2.0 / 3)
    g = lambda t: c * t ** (a - 1) * special.betainc(a, 1.0 / 3, x / t)
    part = integrate.quad(g, x, 1, weight='alg', wvar=(0, -1.0 / 3), epsabs=1e-13, epsrel=1e-12, limit=400)[0]
    return stats.beta.cdf(x, a, 2.0 / 3) + part

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'table'
    if mode == 'validate':
        for n in (3, 5, 10, 30, 100):
            for al in (0.05, 0.01):
                b = Y(3, n).crit(al)
                print('k 3 n %3d alpha %.2f: by inversion %.6f; direct integral gives P(b <= that) = %.7f' % (n, al, b, cdf3_direct(b ** 3, n)))
        # k = 2 through the same inversion against the exact Beta value (the slowest-converging case)
        for n in (5, 20):
            print('k 2 n %d: inversion %.5f exact %.5f' % (n, Y(2, n, mult=20000.0, per=60.0).crit(0.05), crit2(0.05, n)))
        rng = np.random.default_rng(7)
        for k, n, al in ((5, 5, 0.05), (10, 4, 0.01), (7, 12, 0.05)):
            b = Y(k, n).crit(al); cnt = 0; N = 0
            for _ in range(20):
                s = rng.chisquare(n - 1, size=(1_000_000, k))
                bb = np.exp(np.mean(np.log(s), axis=1)) / np.mean(s, axis=1)
                cnt += int((bb <= b).sum()); N += len(bb)
            print('k %d n %d alpha %.2f: inversion %.5f; simulated P(b <= that) = %.5f (se %.5f)' % (k, n, al, b, cnt / N, math.sqrt(al * (1 - al) / N)))
        sys.exit()
    for p, alpha in ((244, 0.05), (245, 0.01)):
        T = Tally('bartlett_%g' % alpha, "Critical values for Bartlett's test, alpha = %g" % alpha)
        ks = None; star = 0; cache = {}
        for ln in L(p):
            tk = [t for a, b, t in toks(ln)]
            if tk and tk[0] == 'n' and len(tk) >= 8 and all(t.isdigit() for t in tk[1:]): ks = [int(t) for t in tk[1:]]; continue
            if ks and len(tk) == len(ks) + 1 and tk[0].isdigit() and all(isnum(t) or t in ('∗', '*') for t in tk[1:]):
                n = int(tk[0])
                for k, t in zip(ks, tk[1:]):
                    if not isnum(t): star += 1; continue
                    tr = crit2(alpha, n) if k == 2 else Y(k, n).crit(alpha)
                    T.add(p, 'n %d' % n, 'k %d' % k, t, tr)
        if star: T.note('%d cells hold an asterisk' % star)
        T.done(show=8)
