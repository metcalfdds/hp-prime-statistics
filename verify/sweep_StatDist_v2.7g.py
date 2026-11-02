#!/usr/bin/env python3
"""sweep_StatDist_v2.7g.py -- every parameter (and x) of all 27 StatDist families swept over the decades, the rest at
their defaults: the test behind StatDist v2.7g's limits (1 Nov 2026).

WHY.  The monkey test (tools/monkey_v1b.py) reaches any one of StatDist's 27 families only now and then.  This sweep
types each field of each family's form, one at a time, through 23 values from 1E-300 to 1E300 (and their negatives),
and then drives the plot the way a careless student might: Zoom- ten times, Zoom+ three times, the arrows, Up, the
refit, the Numbers page and the Formula page.  Each run gets one verdict: an error (the harness's message), FREEZE
(no end within 20 s), or none -- drawn, or refused with the program's own box.

RUN   python3 sweep_StatDist_v2.7g.py PROGRAM.txt [FAMILY_IDS]      e.g.  ... StatDist_v2.7f.txt 10,15,16
      Needs the harness ppl_run_v3e.py and tools/prime_facts_v1.py (beside this file, ../tools or $TTL_TOOLS) and
      hp-prime-kit ($HPKIT).  Prints each broken run and a summary; writes sweep_<PROGRAM>.json beside itself.
"""
import json
import os
import re
import signal
import sys
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
for cand in reversed([c for c in (os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, 'tools'),
                                  os.path.join(HERE, '..', 'tools'), HERE) if c]):
    if os.path.exists(os.path.join(cand, 'ppl_run_v3e.py')):
        sys.path.insert(0, cand)
from ppl_run_v3e import Harness  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

PROG = sys.argv[1]
SRC = open(PROG, encoding='utf-8').read()
# family id -> (main menu item, item in its sub-menu)
MENU = {1: (2, 1), 2: (2, 2), 3: (2, 3), 18: (2, 4), 4: (2, 5), 5: (2, 6), 19: (2, 7), 6: (2, 8),
        7: (3, 1), 8: (3, 2), 9: (3, 3), 24: (3, 4), 25: (3, 5), 10: (3, 6), 11: (3, 8), 20: (3, 9), 12: (3, 10),
        13: (3, 11), 21: (3, 12), 23: (3, 13), 22: (3, 14), 14: (3, 15),
        15: (4, 1), 16: (4, 2), 17: (4, 3), 26: (4, 4), 27: (4, 5)}
# each family's fields (its x form), read from its st_ask_* routine: the st_AskAB(id, ...) line names the family
fields = {}
for m in re.finditer(r'^(st_ask_\w+)\(aTl, aCur, aFull\)\n(.*?)^END;', SRC, re.M | re.S):
    body = m.group(2)
    ids = re.findall(r'st_AskAB\((\d+),', body)
    ins = [re.findall(r'\{(\w+),\[0\]\}', x) for x in re.findall(r'INPUT\(\{((?:\{\w+,\[0\]\}(?:, )?)+)\}', body)]
    if not ins:                                   # v2.7f's forms: plain names
        ins = [[y.strip() for y in x.split(',')] for x in re.findall(r'INPUT\(\{([^}]*)\}', body)]
    if ids and ins:
        fields[int(ids[0])] = max(ins, key=len)
assert len(fields) == 27, sorted(fields)
G = [1E-300, 1E-12, 1E-6, 0.0001, 0.001, 0.05, 0.1, 0.3, 3.0, 10.0, 100.0, 1000.0, 1E5, 1E6, 1E12, 1E49, 1E300,
     -1E300, -1E49, -1E12, -1000.0, -100.0, -0.3]
KEYS = ['Minus'] * 10 + ['Plus'] * 3 + ['Left', 'Right', 'Up', 'Zero', 'Enter', 'Enter', 'Enter']


class _TO(Exception):
    pass


def _alarm(*a):
    raise _TO()


signal.signal(signal.SIGALRM, _alarm)


def one(fam, fld, v):
    """the family's lower-tail form with fld = v, then the plot's keys; Enter twice opens the Numbers page and the
    Formula page (the menu answers 1 and 2)"""
    h = Harness(PROG, idle_key=4, home_minus=True, cas='fail')
    mn, ix = MENU[fam]
    h.choose(mn, ix, 1, 1, 2)
    h.answer({fld: v})
    h.press(*KEYS)
    signal.alarm(20)
    try:
        h.execute('StatDist()')
        err = None
    except _TO:
        err = 'FREEZE'
    except Exception as e:
        err = '%s: %s' % (type(e).__name__, str(e)[:140])
    finally:
        signal.alarm(0)
    return err, [' | '.join(b.lines) for b in h.msgboxes]


fams = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else sorted(fields)
out = []
for fam in fams:
    for fld in fields[fam]:
        for v in G:
            err, boxes = one(fam, fld, v)
            out.append((fam, fld, v, err, boxes[:2]))
            if err:
                print(fam, fld, v, err, flush=True)
json.dump(out, open(os.path.join(HERE, 'sweep_%s.json' % os.path.basename(PROG)), 'w'))
bad = [o for o in out if o[3]]
print('%s: %d runs over %d families; %d broken (in %d families), %d refused with a box, %d drawn'
      % (os.path.basename(PROG), len(out), len(fams), len(bad), len(set(o[0] for o in bad)),
         sum(1 for o in out if o[4] and not o[3]), sum(1 for o in out if not o[4] and not o[3])))
