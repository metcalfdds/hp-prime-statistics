# -*- coding: utf-8 -*-
"""t69.py -- small steps for the comma test of 22 Nov 2026 (the cloud Virtual Calculator; tools/vc_cloud_v1/vcdrive.py).
What is asked: with Home's Digit Grouping set to 123.456,789 (a comma as the decimal point), do our Statisticles start and
show their numbers rightly?  Each step saves a capture in cap/ and prints its name; nothing is concluded here."""
import os, sys, time, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'vc_cloud_v1'))
import vcdrive as v
CAP = os.environ.get('R18_CAP', '/tmp/r18_cap/')   # where the captures go


def typ(s, delay=120):
    """type on the PC keyboard (the calculator takes it as its own keys)"""
    subprocess.run(['xdotool', 'type', '--delay', str(delay), s]); time.sleep(0.5)


def shot(name, x3=True):
    v.cap(CAP + name + '.png', x3=x3); print('captured', name); return CAP + name + '.png'


def group(style):
    """Home Settings > Digit Grouping: 'dot' = 123,456.789 (row 1), 'comma' = 123.456,789 (row 5); then back to Home.
    Starts from Home, and stops unless the page's title reads Home Settings (22 Nov: called from the Program Catalog, its
    tap opened a program's editor and the setting was never changed)."""
    y = {'dot': 33, 'comma': 117}[style]
    v.key('Home'); v.settle()
    v.key('Shift'); time.sleep(0.5); v.key('Home'); v.settle()
    t = v.title_text()
    if 'ings' not in t and 'Home' not in t:   # the title's reading is noisy ('Seetttings')
        shot('settings_FAILED', x3=False); raise SystemExit('not on Home Settings: %r' % t)
    v.tap(200, 86); v.settle()            # the Digit Grouping field
    v.soft(2); v.settle()                 # Choose
    v.tap(193, y); v.settle()
    shot('settings_' + style, x3=False)
    v.key('Home'); v.settle()


def home_line(text, name, wait=3.0, settle=30):
    """type a line in Home, Enter, wait, capture"""
    typ(text); v.settle()
    v.key('Enter'); time.sleep(wait); v.settle(settle)
    return shot(name)


def alive():
    return v.alive()


def goto(name, maxsteps=45):
    """in the Program Catalog: Down until the highlighted row reads exactly `name`; True when it does"""
    for _ in range(maxsteps):
        rows, hi = v.catalog_state()
        if hi is not None:
            at = [t for t, y in rows if abs(y - hi) < 8]
            if at and (at[0].strip() == name or _nm(at[0]) == _nm(name)):
                return True
        v.key('Down', hold=0.2); time.sleep(0.7)
    return False


def run(name, wait=6, settle=40):
    """open the catalog, go to the program, press Run; capture"""
    v.catalog()
    ok = goto(name)
    print('at', name, ok)
    if not ok:
        return False
    v.soft(6); time.sleep(wait); v.settle(settle)
    print('alive', v.alive())
    return True


def check(name):
    """Program Catalog > the program > Edit > Check > OK > Esc; a capture of the Check's box is saved"""
    v.catalog()
    if not goto(name):
        print('not found', name); return False
    v.soft(1); time.sleep(1.5); v.settle()
    v.soft(6); time.sleep(2); v.settle()
    shot('check_' + name, x3=False)
    v.soft(6); v.settle()
    v.key('Esc'); time.sleep(1); v.settle()
    return True


def _nm(t):
    """a row's name as the reading may spell it: I, l and 1 are one letter to the reader, and so are O and 0"""
    return t.strip().lower().replace('l', 'i').replace('1', 'i').replace('0', 'o').replace(' ', '')
