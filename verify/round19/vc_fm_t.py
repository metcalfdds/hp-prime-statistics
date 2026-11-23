# -*- coding: utf-8 -*-
"""vc_fm_t.py -- on the cloud Virtual Calculator: StatDist, Advanced Continuous, Student t, lower tail, df typed, x 0,
OK, Enter, "Formula page (CAS)"; captures as the page is asked for and at the times given (round 19, 23 Nov 2026).

Run with the calculator on the Program Catalog's StatDist row:  python3 vc_fm_t.py DF TAG CAPDIR [SECONDS ...]
(uses tools/vc_cloud_v1/vcdrive.py; prints the time each capture was made and its OCR)"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'vc_cloud_v1'))
import vcdrive as v  # noqa: E402

DF, TAG, CAP = sys.argv[1], sys.argv[2], sys.argv[3]
AT = [float(x) for x in sys.argv[4:]] or [5, 30, 90, 180]
v.act(v.soft, 6, wait=40); v.settle(40)                  # Run
v.pick(3); v.pick(1); v.pick(1); v.settle()               # Advanced Continuous, Student t, lower tail
for k in DF:
    v.key({'.': 'Dot'}.get(k, k), hold=0.2); time.sleep(0.4)
v.key('Enter'); time.sleep(1); v.settle()
v.cap(CAP + TAG + '_form.png')
v.act(v.soft, 6, wait=40); v.settle(40)                  # OK: the plot
v.cap(CAP + TAG + '_plot.png')
v.act(v.key, 'Enter'); v.settle()                         # Plot options
v.cap(CAP + TAG + '_options.png')
t0 = time.time()
v.key('2', hold=0.2)                                      # Formula page (CAS)
for at in AT:
    while time.time() - t0 < at:
        time.sleep(0.5)
    p = CAP + '%s_fm_%03ds.png' % (TAG, int(at))
    v.cap(p)
    print('%6.1f s  %s | %s' % (time.time() - t0, os.path.basename(p), ' '.join(v.ocr(p).split())[:150]), flush=True)
