# -*- coding: utf-8 -*-
"""probe_dataload_bins.py -- DataLoad's histogram of a column whose values are all the same (23 Nov 2026).

The monkey (round 18, seed 18000713) tapped a summary row whose column held one value, and dd_DrawHisto stopped at
"index 0 out of range in hc (1..0)".  With every value equal, dd_DrawHisto takes hw := MAX(1, |v|/10) as the bin width,
hs := FLOOR(v/hw)*hw as the first bin's start and hnb := FLOOR((v - hs)/hw) + 1 bins.  In binary doubles, as the PC
harness counts, |v|/10 is rounded, FLOOR(v/hw)*hw can come out a hair above v, and then hnb is 0.  In decimal, as the
Prime counts (12 digits), dividing by 10 moves the decimal point and FLOOR(v/hw)*hw is v.

Part 1 runs dd_DrawHisto in the harness on 437 such columns (three equal values each); part 2 does the same three lines
of arithmetic in Python, once in binary doubles and once in 12-digit decimals.

Run from the repository's root:   python3 verify/round18/probes/probe_dataload_bins.py
"""
import math, os, random, sys
from decimal import Decimal, getcontext
sys.path.insert(0, 'tools'); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
from ppl_run_v3e import Harness  # noqa: E402

vals = [5, -5, 0, 0.3, 11, 12.3, 13, -13, 17, 23, 29, 31, 33.3, 37, 41, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
        1e300, -1e300, 1e-300, 123456789012, 0.07, 1.1, 2.2, 3.3, 19.99, 99.9]
rnd = random.Random(1)
vals += [round(rnd.uniform(-1e4, 1e4), rnd.randint(0, 6)) for _ in range(400)]

# part 1: the program in the harness
crash = []
for v in vals:
    h = Harness('programs/DataLoad_beta1h.txt', idle_key=4, home_minus=True, app_data={'D1': [v, v, v], 'C1': []})
    try:
        h.execute('dd_Init()')
        h.execute('dd_DrawHisto(1)')
    except Exception as e:
        crash.append((v, str(e)[:60]))
print('harness: %d columns, %d stopped: %s' % (len(vals), len(crash), sorted({e for _, e in crash})))


# part 2: the three lines, in binary doubles and in 12-digit decimals
def bins_binary(v):
    hw = max(1, abs(v) / 10)
    hs = math.floor(v / hw) * hw
    return math.floor((v - hs) / hw) + 1


getcontext().prec = 12


def bins_decimal(v):
    v = +Decimal(repr(v))
    hw = max(Decimal(1), abs(v) / 10)
    hs = (v / hw).to_integral_value(rounding='ROUND_FLOOR') * hw
    return int(((v - hs) / hw).to_integral_value(rounding='ROUND_FLOOR')) + 1


b = [v for v in vals if bins_binary(v) < 1]
d = [v for v in vals if bins_decimal(v) < 1]
print('binary doubles: %d columns with no bin; 12-digit decimals: %d' % (len(b), len(d)))
print('the same columns as the harness stopped on: %s' % (sorted(b) == sorted(v for v, _ in crash)))
print('the smallest |v| with no bin in binary: %s' % (min(abs(v) for v in b) if b else None))
