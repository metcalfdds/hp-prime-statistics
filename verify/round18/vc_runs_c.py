# -*- coding: utf-8 -*-
"""Round 18, the directed runs: the programs the plain run could not start (a chooser or a form comes first), the app,
and two runs whose pages are kept (StatDist's result page; Norm3 by the book's typed line with a comma as the decimal mark)."""
import os, sys, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # t69.py, beside this file
import t69, vc_runs_b as B
v = t69.v
CAP = B.CAP


def odd(tagname):
    B.run_cat('SetOdd', 2.5); v.key('Enter'); v.settle()
    page, s0 = B.read_settings('odd_' + tagname)
    return s0['Degrees'] and s0['RPN'] and s0['comma'] and s0['Fixed']


def after(tagname):
    page, s1 = B.read_settings('after_' + tagname)
    return page and s1['Radians'] and s1['Standard'] and s1['period'] and s1['Textbook'], s1


def leave():
    for _ in range(3):
        v.key('Esc'); time.sleep(1.2); v.settle(15)
    v.key('Enter'); time.sleep(0.8); v.settle(10)


which = sys.argv[1]
if which == 'EpiStats':
    o = odd('EpiStats'); B.run_cat('EpiStats', 3); v.cap(CAP + 'chooser_EpiStats.png')
    v.key('Enter'); time.sleep(6); v.settle(40); v.cap(CAP + 'first_EpiStats.png'); leave(); g, s = after('EpiStats')
    print('EpiStats before odd', o, '| alive', v.alive(), '| after the book\'s', g, [k for k, x in s.items() if x], flush=True)
if which == 'Norm3':
    o = odd('Norm3'); B.run_cat('Norm3', 3); v.cap(CAP + 'form_Norm3.png')
    t69.typ('100'); v.key('Enter'); v.settle(); t69.typ('15'); v.key('Enter'); v.settle(); t69.typ('130'); v.key('Enter'); v.settle()
    v.cap(CAP + 'form_Norm3_filled.png'); v.soft(6); time.sleep(5); v.settle(40); v.cap(CAP + 'first_Norm3.png'); leave(); g, s = after('Norm3')
    print('Norm3 before odd', o, '| alive', v.alive(), '| after the book\'s', g, [k for k, x in s.items() if x], flush=True)
if which == 'StatDist':
    o = odd('StatDistB'); B.run_cat('StatDist', 6)
    v.pick(2); v.settle(30); v.pick(1); time.sleep(1.5); v.settle(30); v.pick(1); time.sleep(1.5); v.settle(30)
    t69.typ('1234.5'); v.key('Enter'); v.settle(); t69.typ('2.5'); v.key('Enter'); v.settle(); t69.typ('1236.25'); v.key('Enter'); v.settle()
    v.cap(CAP + 'form_StatDist.png'); v.soft(6); time.sleep(3); v.settle(40); v.cap(CAP + 'result_StatDist.png')
    v.key('Esc'); time.sleep(1.5); v.settle(20); v.pick(6); v.settle(); v.key('Enter'); v.settle(); g, s = after('StatDistB')
    print('StatDist before odd', o, '| alive', v.alive(), '| after the book\'s', g, [k for k, x in s.items() if x], flush=True)
if which == 'Norm3typed':
    v.soft(6); v.settle(); v.key('Esc'); v.settle(); v.key('Esc'); v.settle()
    B.run_cat('SetBook', 2.5); v.key('Enter'); v.settle()
    t69.CAP = CAP; t69.group('comma')
    t69.typ('Norm3(100,15,130)'); v.settle(); v.cap(CAP + 'typed_Norm3_line.png')
    v.key('Enter'); time.sleep(4); v.settle(40); v.cap(CAP + 'typed_Norm3_page.png'); v.soft(6); time.sleep(1.5); v.settle(20); g, s = after('Norm3typed')
    print('Norm3 typed with a comma | alive', v.alive(), '| after the book\'s', g, [k for k, x in s.items() if x], flush=True)
