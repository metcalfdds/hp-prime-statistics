# -*- coding: utf-8 -*-
"""vc_fm.py -- on the cloud Virtual Calculator: StatDist's Formula page (CAS) for one family, timed (round 19, 23 Nov 2026).

From the Program Catalog's StatDist row: Run, Advanced Continuous, the family (its item number), lower tail, the values
typed into the form's first fields (the x value left at its 0), OK, Enter, "Formula page (CAS)".  The time is counted
from the key that asks for the page until "Asking the CAS" has gone from the screen (read every 2 s, at most LIMIT
seconds); the page is then captured and read.  The calculator cannot be stopped while its CAS works (two presses of On
did nothing, 23 Nov 2026), so a run that reaches LIMIT leaves it busy.

Run with the calculator on the Program Catalog's StatDist row:
    python3 vc_fm.py ITEM TAG CAPDIR VALUE [VALUE ...]        (ITEM: 1 Student t, 3 Fisher F, 6 Burr Type XII)"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'vc_cloud_v1'))
import vcdrive as v  # noqa: E402

ITEM, TAG, CAP, VALS = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4:]
LIMIT = float(os.environ.get('VC_LIMIT', '300'))
v.act(v.soft, 6, wait=40); v.settle(40)                  # Run
v.pick(3); v.pick(ITEM); v.pick(1); v.settle()            # Advanced Continuous, the family, lower tail
for val in VALS:
    for k in val:
        v.key({'.': 'Dot'}.get(k, k), hold=0.2); time.sleep(0.4)
    v.key('Enter'); time.sleep(1); v.settle()
v.cap(CAP + TAG + '_form.png')
v.act(v.soft, 6, wait=40); v.settle(40)                  # OK: the plot
v.act(v.key, 'Enter'); v.settle()                         # Plot options
t0 = time.time()
v.key('2', hold=0.2)                                      # Formula page (CAS)
time.sleep(1.0)
asking = True
while time.time() - t0 < LIMIT:
    v.cap(CAP + 'poll.png')
    if 'Asking the CAS' not in ' '.join(v.ocr(CAP + 'poll.png').split()):
        asking = False
        break
    time.sleep(2.0)
last = time.time() - t0 + t0
now = time.time()
v.settle()
p = CAP + TAG + '_fm.png'
v.cap(p)
print('%-10s %s: %s | %s' % (TAG, ' '.join(VALS), ('still "Asking the CAS" at %d s' % LIMIT) if asking else
      ('the page in %.0f s or less (polled every 2 s)' % (last - t0 + 0.0)), ' '.join(v.ocr(p).split())[:200]), flush=True)
v.key('Esc'); time.sleep(1); v.settle()                   # back to the plot
