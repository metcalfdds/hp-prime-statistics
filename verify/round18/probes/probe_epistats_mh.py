# -*- coding: utf-8 -*-
"""probe_epistats_mh.py -- EpiStats' stratified rate ratio (es_MHCalc, kind 3) with extreme person-times (23 Nov 2026).

The monkey (round 18, seed 18000612) typed a person-time of 1E-300 in a stratum, and es_MHCalc divided by zero.
Cells per stratum: cases exposed, person-time exposed, cases unexposed, person-time unexposed.  The third set is an
ordinary one, for comparison.

Run from the repository's root:   python3 verify/round18/probes/probe_epistats_mh.py
"""
import sys, os
sys.path.insert(0, 'tools')
from ppl_run_v3e import Harness
# stratum 1: 1 case in 100,000 exposed person-time, 0 cases in a tiny unexposed person-time; stratum 2 the other way round
h = Harness('programs/EpiStats_v1.7n.txt', idle_key=4, home_minus=True)
for cells in ('{1,100000,0,1E-300, 0,1E-300,1,100000}', '{1,100000,0,0.001, 0,0.001,1,100000}', '{5,1000,3,1200, 4,900,2,1100}'):
    try:
        print(cells, '->', str(h.execute('es_MHCalc(3, %s, {0,0})' % cells))[:120])
    except Exception as e:
        print(cells, '-> ERROR', str(e)[:100])
