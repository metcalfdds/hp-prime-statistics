# -*- coding: utf-8 -*-
"""floor_sweep_r19.py -- the smallest person-time for EpiStats' stratified rates grid (23 Nov 2026, round 19).

EpiStats' es_MHCalc works the Mantel-Haenszel rate ratio over two strata, each holding cases exposed (a), person-time
exposed (T1), cases unexposed (c) and person-time unexposed (T0):
    R = sum a T0 / T,  S = sum c T1 / T,  P = sum (a + c) T1 T0 / T^2,  T = T1 + T0,
    E = R / S,  V = P / (R S),  interval exp(ln E -+ 1.959964 sqrt V).
For each candidate floor this runs every pair of strata built from cases {0, 1, 2, 5, 100, 100,000} and person-times
{0, the floor, 1.5 x floor, 2 x floor, 5, 10, 100, 1,000, 10,000, 100,000} (those below the floor left out), in binary
doubles as the PC harness counts, and counts the tables whose R S underflows to 0 (a division by zero) and whose interval
end, |ln E| + 1.96 sqrt V, passes the harness's EXP (709.78) or the Prime's range (1E499, ln = 1,149.0; Lessons Learned
v7zy section 3).  12,960,000 tables a floor; about four minutes.

Run:   python3 verify/round19/floor_sweep_r19.py
"""
import itertools, math

LN_PRIME = 499 * math.log(10)


def mh(cells):
    R = S = P = 0.0
    for i in range(2):
        a, t1, c, t0 = cells[4 * i:4 * i + 4]
        T = t1 + t0
        if T > 0:
            R += a * t0 / T
            S += c * t1 / T
            P += (a + c) * t1 * t0 / T ** 2
    if S > 0 and R > 0:
        if R * S == 0:
            return 'underflow', None
        return 'ok', abs(math.log(R / S)) + 1.959964 * math.sqrt(max(0.0, P / (R * S)))
    return 'none', None


if __name__ == '__main__':
    C = [0, 1, 2, 5, 100, 100000]
    for F in (0.001, 0.1, 0.5, 1, 2):
        PT = [p for p in [0, F, 1.5 * F, 2 * F, 5, 10, 100, 1000, 10000, 100000] if p == 0 or p >= F]
        n = under = harness = prime = 0
        worst = 0.0
        for a1, t1, c1, t0, a2, u1, c2, u0 in itertools.product(C, PT, C, PT, C, PT, C, PT):
            st, x = mh([a1, t1, c1, t0, a2, u1, c2, u0])
            n += 1
            if st == 'underflow':
                under += 1
            if x is not None:
                worst = max(worst, x)
                harness += x > 709.78
                prime += x > LN_PRIME
        print('floor %-6g %s tables: divisions by zero %d; widest end e^%.0f; past the harness %s; past the Prime %s'
              % (F, '{:,}'.format(n), under, worst, '{:,}'.format(harness), '{:,}'.format(prime)), flush=True)
