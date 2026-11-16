# -*- coding: utf-8 -*-
"""check_all.py NAME... -- Check each named program on the cloud Virtual Calculator (Round 16, 15 Nov 2026).

Start with the Program Catalog open (Shift, 1).  For each name: the highlight is moved to its row, Edit, the editor's
title is read and must name the program, Check, and the box must read "No errors in the program"; then OK and Esc.
One line a program goes to $VC/checks/log.txt with the time, and a capture of each box beside it.  It stops at the
first thing it does not expect.  Afterwards leave the calculator by Calculator > Exit and collect the checked files
BEFORE any program is run (a run leaves its values in the file).

    VC=/tmp/vc python3 tools/vc_cloud_v1/check_all.py AnovaLab CICatcher
    --first-open        the first program's Check box is already showing
    --first-in-editor   the first program's editor is already open
"""
import sys, time, difflib, datetime
import vcdrive as V
import os
OUT = os.path.join(os.environ.get('VC', '/tmp/vc'), 'checks') + os.sep
os.makedirs(OUT, exist_ok=True)
args = sys.argv[1:]
first_open = '--first-open' in args
in_editor = '--first-in-editor' in args
names = [a for a in args if not a.startswith('--')]


def title():
    """the title line, read several ways (white letters on blue: tesseract misses some renderings)"""
    p = V.cap(OUT + 'tmp_title.png')
    best = ''
    for crop in ((200, 20, 60, 0), (320, 20, 0, 0)):
        for neg in (True, False):
            a = ['convert', p, '-crop', '%dx%d+%d+%d' % crop, '+repage']
            if neg: a.append('-negate')
            V.sh(*(a + [OUT + 'tmp_title_n.png']))
            for psm in (7, 6, 13):
                t = V.ocr(OUT + 'tmp_title_n.png', None, psm)
                if 'Main' in t or 'Catalog' in t:
                    return t
                if len(t) > len(best): best = t
    return best


def like(text, name):
    t = V.norm(text).lower(); n = name.lower()
    best = 0
    for i in range(0, max(1, len(t) - len(n) + 1)):
        best = max(best, difflib.SequenceMatcher(None, t[i:i + len(n)], n).ratio())
    return best


def log(s):
    print(s, flush=True)
    open(OUT + 'log.txt', 'a').write(s + '\n')


def open_editor(name):
    """move the highlight to the program's row and press Edit; return the editor's title"""
    if not V.run_program(name, softkey=1):
        return 'row not found: ' + name
    time.sleep(5.0)
    return title()


for k, name in enumerate(names):
    if not (first_open and k == 0):
        if not (in_editor and k == 0):
            t = open_editor(name)
        else:
            t = title()
        if 'Main' not in t or like(t, name) < 0.75:
            log('STOP %s: the editor\'s title reads %r' % (name, t)); sys.exit(1)
        V.soft(6)                                         # Check
    t0 = time.time(); box = ''
    while time.time() - t0 < 90:
        time.sleep(2.0)
        p = V.cap(OUT + 'tmp_box.png')
        box = V.ocr(p, (216, 48, 51, 95), 6)
        if 'error' in box.lower() or 'rror' in box:
            break
    tt = title()
    p3 = V.cap(OUT + name + '_check.png', x3=True)
    now = datetime.datetime.now().strftime('%H:%M')
    log('%-10s | editor title %r | box %r | %s | %.0f s' % (name, tt, box, now, time.time() - t0))
    if 'No errors in the program' not in box:
        log('STOP %s: the box does not say "No errors in the program"' % name); sys.exit(1)
    V.soft(6); time.sleep(1.2)                            # OK closes the box
    V.key('Esc'); time.sleep(2.5)                         # the editor closes: back in the catalog
    c = V.ocr(V.cap(OUT + 'tmp_cat.png'), (320, 20, 0, 0), 7)
log('catalog after the last: %r' % title())
