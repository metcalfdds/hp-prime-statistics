# -*- coding: utf-8 -*-
"""Round 18, the Checks: Program Catalog > Edit > Check on each of the 30 programs of the first-pass pack, on the cloud
Virtual Calculator; one line a program, with what the Check's box read (OCR) and a capture."""
import os, sys, time, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # t69.py, beside this file
import t69
v = t69.v
t69.CAP = os.environ.get('R18_CAP', '/tmp/r18_cap/')   # where the captures go
names = sys.argv[1:]
for n in names:
    v.catalog()
    ok = t69.goto(n, 40)
    if not ok:
        for _ in range(40):
            v.key('Up', hold=0.15); time.sleep(0.25)
        ok = t69.goto(n, 45)
    if not ok:
        print(time.strftime('%H:%M:%S'), n, 'NOT FOUND', flush=True); continue
    v.soft(1); time.sleep(2.0); v.settle()
    v.soft(6); time.sleep(3.0); v.settle(40)
    p = t69.CAP + 'check_' + n + '.png'; v.cap(p)
    import subprocess
    subprocess.run(['convert', p, '-crop', '225x56+52+94', '+repage', '-resize', '300%', p[:-4] + '_box.png'])
    txt = ' '.join(subprocess.run(['tesseract', p[:-4] + '_box.png', '-', '--psm', '6'], capture_output=True, text=True).stdout.split())
    print(time.strftime('%H:%M:%S'), n, '|', txt[-60:], flush=True)
    v.soft(6); v.settle(); v.key('Esc'); time.sleep(1); v.settle()
