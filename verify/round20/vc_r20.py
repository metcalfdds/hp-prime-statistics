# -*- coding: utf-8 -*-
"""vc_r20.py -- round 20 on the cloud Virtual Calculator (tools/vc_cloud_v1): DataLoad beta 1i, CHECKED (starter pack v28's
file), on Student's sleep data with two blanks (make_sleep_holes.js: drug 2 of patient 3 and drug 1 of patient 7 left blank).
This script holds the first steps (Statistics 1Var opened once; DataLoad from the Program Catalog; Columns; the question;
Pairs).  On 27 Nov 2026 the Program Catalog's highlighted row did not read back by OCR, so DataLoad was started with soft key 6
(Run) by hand, and the steps after Pairs (Help, Quit, the Numeric view, the second run with Separate groups and Cancel) were
driven by hand with the same vcdrive calls (act, pick, cap); vc_record.txt lists every step with its capture in vc/.
Run with the calculator on the Home screen:  python3 verify/round20/vc_r20.py STEP   (STEP = stats, run1, ...)"""
import sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'vc_cloud_v1'))
import vcdrive as V
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vc') + os.sep
step = sys.argv[1]
if step == 'stats':                       # open Statistics 1Var once, so that D1-D9 exist, then Home
    V.tap(118, 110); time.sleep(2.5); V.settle()
    V.cap(OUT + '00_stats1var.png')
    V.act(V.key, 'Home')
elif step == 'run1':                      # DataLoad, Columns: the question
    V.catalog(); time.sleep(1.5)
    V.must(V.run_program('DataLoad'), 'DataLoad run from the Program Catalog')
    time.sleep(2.5); V.settle()
    V.cap(OUT + '01_menu.png')
    V.must(V.pick(1), 'Columns')
    V.cap(OUT + '02_question.png')
elif step == 'pairs':                     # Pairs: keep complete rows
    V.must(V.pick(1), 'Pairs')
    time.sleep(2); V.settle()
    V.cap(OUT + '03_lists_pairs.png')
elif step == 'cap':
    V.cap(OUT + sys.argv[2])
