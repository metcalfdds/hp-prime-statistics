#!/usr/bin/env python3
"""monkey_directed_v1.py -- the monkey, started ON a page it seldom finds by itself (15 Nov 2026; Round 16).

Random keys reach a page that lies four menus deep only now and then: of the first 300 sessions of AnovaLab beta 1i's
monkey test, 3 saw Dunnett's table and none saw its plot; none of CICatcher beta 2l's 300 saw a tolerance interval
(tools/monkey_reach_v1.py counts this).  "1,000 of 1,000 runs OK" then says little about that page.  A directed run
answers the program's first questions from a script, the LEAD, so that the session stands on the new page, and then
hands over to the monkey: the same random keys, taps, drags, menu picks and typed values as monkey_v1b.py, the same
lists in D1 and D2, the same verdicts (OK, CRASH, FREEZE, GUARD, STALL, HARNESS, STATE).

    python3 tools/monkey_directed_v1.py PROG CALL BASE K0 K1 OUT.jsonl --lead "LEAD" --reach "REGEX"
                                        [--lists] [--writes D,C] [--seconds 30] [--events 150] [--missed-ok]

LEAD is a Python list of steps, taken in order by kind:
    ('key', 'Enter')        a key for the program's next wait ('Esc', 'Enter', 'Left', 'Right', 'Up', 'Down', 'Plus', ...)
    ('tap', 240, 228)       a tap
    ('choose', 6)           the pick at the program's next CHOOSE (0 = Esc)
    ('input', 'ACCEPT')     the answer at the next INPUT: 'ACCEPT', 'CANCEL' or a dict {field: value}
    ('msgbox', True)        the answer at the next MSGBOX with a Cancel key
Keys and taps are queued before the monkey's own events; picks and answers are used up one by one, and the monkey
answers every dialog after them.  REGEX is a text the page shows: a run in which no screen carried it did not get
there, and counts as MISSED (a lead that no longer fits the program must not pass for a test of the page).  With
--missed-ok such a run keeps its verdict: that is for a lead through "Use my data" with the monkey's random lists
(--lists), where the program rightly refuses many of them and the page is never opened; the tally still says how many
runs stood on the page.

One JSON line a run is appended to OUT.jsonl as it ends (k, seed, verdict, detail, secs, reached = the number of
screens that matched); run again with the same OUT it skips the runs already written.  The last line printed is the
tally.  seed = BASE x 1000003 + k, as monkey_v1b's; a directed set takes a BASE of its own.
"""
import ast
import collections
import json
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
sys.argv = ['monkey_v1b.py']
import monkey_v1b as M  # noqa: E402
from ppl_run_v3e import Harness, ACCEPT, CANCEL, KEY  # noqa: E402

if len(a) < 6:
    sys.exit(__doc__)
prog, call, base, k0, k1, out = a[0], a[1], int(a[2]), int(a[3]), int(a[4]), a[5]
lists = '--lists' in a
missed_ok = '--missed-ok' in a
opt = {'--writes': '', '--seconds': '30', '--events': '150', '--lead': '[]', '--reach': ''}
i = 6
while i < len(a):
    if a[i] in ('--lists', '--missed-ok'):
        i += 1
        continue
    opt[a[i]] = a[i + 1]
    i += 2
M.WRITES.update(w.strip() for w in opt['--writes'].split(',') if w.strip())
LEAD = ast.literal_eval(opt['--lead'])
REACH = re.compile(opt['--reach']) if opt['--reach'] else None
if REACH is None:
    sys.exit('monkey_directed_v1: --reach REGEX is needed (the text that shows the lead arrived)')
LAST = [None]
Base = M.Monkey          # the plain monkey: M.Monkey itself is replaced below, so its methods are called through this name


class Directed(Base):
    """Monkey, with the first keys, taps, picks and answers taken from LEAD."""

    def __init__(self, path, rng, app_data, events):
        Harness.__init__(self, path, idle_key=4, home_minus=True, app_data=app_data,
                         seed=rng.randrange(1 << 30), stall_limit=20000)
        self.m = rng
        self.trace = []
        self.lead_choose = [s[1] for s in LEAD if s[0] == 'choose']
        self.lead_input = [s[1] for s in LEAD if s[0] == 'input']
        self.lead_msgbox = [s[1] for s in LEAD if s[0] == 'msgbox']
        for s in LEAD:
            if s[0] == 'key':
                self.press(s[1] if isinstance(s[1], int) else KEY[s[1]])
            elif s[0] == 'tap':
                self.tap(s[1], s[2])
        for _ in range(events):
            self._queue_random_event()
        LAST[0] = self

    def _choose(self, nodes, frame):
        if self.lead_choose:
            idx = self.lead_choose.pop(0)
            self.trace.append(('lead choose', idx))
            self._choices.appendleft(idx)
            return Harness._choose(self, nodes, frame)
        return Base._choose(self, nodes, frame)

    def _input(self, nodes, frame):
        if self.lead_input:
            ans = self.lead_input.pop(0)
            ans = ACCEPT if ans == 'ACCEPT' else CANCEL if ans == 'CANCEL' else ans
            self.trace.append(('lead input', 'ACCEPT' if ans is ACCEPT else 'CANCEL' if ans is CANCEL else ans))
            self._answers.appendleft(ans)
            return Harness._input(self, nodes, frame)
        return Base._input(self, nodes, frame)

    def _msgbox(self, args):
        if self.lead_msgbox:
            self._msgbox_answers.appendleft(bool(self.lead_msgbox.pop(0)))
            return Harness._msgbox(self, args)
        return Base._msgbox(self, args)


M.Monkey = Directed
done = set()
if os.path.exists(out):
    for ln in open(out):
        try:
            done.add(json.loads(ln)['k'])
        except Exception:
            pass
tally = collections.Counter()
reached_runs = 0
with open(out, 'a') as fh:
    for k in range(k0, k1):
        if k in done:
            continue
        seed = base * 1000003 + k
        r = M.one_run(prog, call, seed, int(opt['--events']), int(opt['--seconds']), lists)
        h = LAST[0]
        n = 0
        for s in h.screens:
            if REACH.search(' | '.join(t.text for t in s.texts)):
                n += 1
        v = r['verdict']
        if v == 'OK' and n == 0 and not missed_ok:
            v = 'MISSED'
        left = len(h.lead_choose) + len(h.lead_input) + len(h.lead_msgbox)
        rec = {'k': k, 'seed': seed, 'verdict': v, 'detail': r['detail'], 'secs': r['secs'], 'reached': n,
               'lead_left': left}
        fh.write(json.dumps(rec) + '\n')
        fh.flush()
        tally[v] += 1
        reached_runs += 1 if n else 0
        if v != 'OK':
            print('k = %d  seed %d  %s  %s  (screens of the page: %d; lead steps unused: %d)' % (
                k, seed, v, r['detail'][:160], n, left), flush=True)
print('%s  directed runs %d..%d: %s; the page was on the screen in %d of them' % (
    os.path.basename(prog), k0, k1 - 1, dict(tally), reached_runs), flush=True)
