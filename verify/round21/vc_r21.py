# -*- coding: utf-8 -*-
"""vc_r21.py -- round 21 on the cloud Virtual Calculator (tools/vc_cloud_v1): TTestLab beta 1n and TTestLabG beta 1k, CHECKED
(starter pack v29's files, collected before this run), on the book's two examples and the two-proportion test at the ends of
its form.  One step a call, from the Program Catalog; vc_record.txt lists every step with its capture in vc/.

Run with the calculator on the Program Catalog:   python3 verify/round21/vc_r21.py STEP
  tlg      TTestLabG: Example: draft lottery; steps 2 and 4 (Figure 11.2) at three times; help page 2; Quit
  tl       TTestLab: Example: age at arrest; step 4 (Figure 11.4) at three times; help page 2
  tl2p     (after tl, at TTestLab's steps) Menu, Choose the test, Two proportions: z; 1 of 999,999 and 151 of 1,000,000;
           two-tailed, 0.05; step 4 at three times; Quit
  cap NAME a capture of the screen as it stands"""
import sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'vc_cloud_v1'))
import vcdrive as V
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vc') + os.sep


def to_row(name):
    """the Program Catalog's highlight to the row whose name is exactly `name`"""
    for _ in range(16):
        rows, hi = V.catalog_state()
        want = [y for t, y in rows if t.strip() == name]
        if not want:
            V.key('Down', hold=0.2); time.sleep(0.8); continue
        d = want[0] - hi
        if abs(d) < 8: return True
        V.key('Down' if d > 0 else 'Up', hold=0.2); time.sleep(0.8)
    return False


def run(name):
    V.must(to_row(name), name + ' highlighted in the Program Catalog')
    V.must(V.act(V.soft, 6), name + ' run')
    time.sleep(2); V.settle()


def step(n, path, x3=True):
    V.must(V.act(V.soft, n), 'soft key %d' % n)
    time.sleep(1.5); V.settle()
    V.cap(OUT + path, x3=x3)


def help2(prefix):
    V.must(V.act(V.soft, 6), 'Menu')
    V.cap(OUT + prefix + '_menu.png')
    V.must(V.pick(6), 'Help')
    V.cap(OUT + prefix + '_help1.png')
    V.must(V.act(V.tap, 160, 120), 'help page 2')
    V.cap(OUT + prefix + '_help2.png', x3=True)
    V.must(V.act(V.tap, 160, 120), 'help page 3')
    V.cap(OUT + prefix + '_help3.png')
    V.must(V.act(V.tap, 160, 120), 'back from help')
    V.cap(OUT + prefix + '_after_help.png')


s = sys.argv[1]
if s == 'tlg':
    run('TTestLabG')
    V.cap(OUT + '10_tlg_start_menu.png')
    V.must(V.pick(3), 'Example: draft lottery')
    time.sleep(2); V.settle()
    V.cap(OUT + '11_tlg_lottery_step1.png')
    step(2, '12_tlg_lottery_step2_x3.png')
    step(4, '13_tlg_lottery_step4_x3.png')
    help2('14_tlg')
elif s == 'tl':
    run('TTestLab')
    V.cap(OUT + '20_tl_start_menu.png')
    V.must(V.pick(2), 'Example: age at arrest')
    time.sleep(2); V.settle()
    V.cap(OUT + '21_tl_age_step1.png')
    step(4, '22_tl_age_step4_x3.png')
    help2('23_tl')
elif s == 'tl2p':
    V.must(V.pick(4), 'Choose the test')
    V.cap(OUT + '30_tl_which_test.png')
    V.must(V.pick(4), 'Two proportions: z')
    time.sleep(1); V.settle()
    V.cap(OUT + '31_tl_form.png')
    for field, digits in enumerate(('1', '999999', '151', '1000000')):
        for d in digits:
            V.must(V.act(V.key, d), 'digit %s of field %d' % (d, field + 1))
        V.must(V.act(V.key, 'Enter'), 'Enter, field %d' % (field + 1))
    V.cap(OUT + '32_tl_form_filled.png')
elif s == 'cap':
    V.cap(OUT + sys.argv[2], x3=len(sys.argv) > 3)
