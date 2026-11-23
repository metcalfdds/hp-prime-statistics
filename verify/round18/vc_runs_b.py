# -*- coding: utf-8 -*-
"""Round 18, the runs: each program is started from the Program Catalog on a calculator that SetOdd has just left in RPN
entry, with a comma as the decimal point, Fixed 2 and Degrees; its first page is captured; the program is left; and Home
Settings is read.  One line a program."""
import os, sys, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # t69.py, beside this file
import t69
v = t69.v
CAP = os.environ.get('R18_CAP', '/tmp/r18_cap/')   # where the captures go


def read_settings(tagname):
    v.key('Home'); v.settle(); v.key('Shift'); time.sleep(0.5); v.key('Home'); v.settle()
    p = CAP + tagname + '.png'; v.cap(p)
    subprocess.run(['convert', p, '-resize', '300%', p[:-4] + '_x3.png'])
    t = subprocess.run(['tesseract', p[:-4] + '_x3.png', '-', '--psm', '6'], capture_output=True, text=True).stdout
    v.key('Home'); v.settle()
    return ('Angle' in t or 'Entry' in t), {'Radians': 'Radians' in t, 'Standard': 'Standard' in t, 'period': '123,456.789' in t,
            'Textbook': 'Textbook' in t, 'Degrees': 'Degrees' in t, 'RPN': 'RPN' in t, 'comma': '123.456,789' in t, 'Fixed': 'Fixed' in t}


def run_cat(name, wait):
    v.catalog()
    ok = t69.goto(name, 45)
    if not ok:
        for _ in range(45):
            v.key('Up', hold=0.15); time.sleep(0.25)
        ok = t69.goto(name, 45)
    if ok:
        v.soft(6); time.sleep(wait); v.settle(40)
    return ok


def main(names):
  for n in names:
      if not run_cat('SetOdd', 2.5):
          print(n, 'SetOdd NOT FOUND', flush=True); continue
      v.key('Enter'); v.settle()
      page, s0 = read_settings('odd_' + n)
      odd = s0['Degrees'] and s0['RPN'] and s0['comma'] and s0['Fixed']
      if not run_cat(n, 7):
          print(n, 'NOT FOUND', flush=True); continue
      v.cap(CAP + 'first_' + n + '.png')
      alive = v.alive()
      forced = ''
      for _ in range(3):
          v.key('Esc'); time.sleep(1.2); v.settle(15)
      v.key('Enter'); time.sleep(0.8); v.settle(10)
      page, s1 = read_settings('after_' + n)
      if not page:
          forced = ' (left by On)'
          v.key('On'); time.sleep(1.5); v.key('Enter'); time.sleep(1); v.key('Esc'); time.sleep(1)
          page, s1 = read_settings('after_' + n)
      good = s1['Radians'] and s1['Standard'] and s1['period'] and s1['Textbook']
      print(time.strftime('%H:%M:%S'), '%-12s' % n, 'before: %s' % ('RPN, comma, Fixed, Degrees' if odd else 'NOT ODD ' + str([k for k, x in s0.items() if x])),
            '| alive %s | after: %s%s' % (alive, 'Radians, Standard, 123,456.789, Textbook' if good else 'NOT THE BOOK\'S ' + str([k for k, x in s1.items() if x]), forced), flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
