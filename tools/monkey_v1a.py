#!/usr/bin/env python3
"""monkey_v1a.py -- throws random use at an HP Prime program in the PC harness (ppl_run_v3e.py) and reports every way
it broke.  Roger Metcalf & Claude, 1 Nov 2026.

WHY.  The companion book's programs "simply must work": students who don't want to be there will press anything, type
anything and cancel anything.  The verify scripts drive every path a careful student takes; this drives the paths a
careless one takes.  (The book's vetting standard, point 6.)

v1a (1 Nov 2026): the matrices M0-M9 exist in every run, as on the Prime (an unused matrix holds one zero; v1 left
them undefined, so DataLoad crashed on M1 in all 400 runs, the harness's gap, not DataLoad's); with --lists, M1
is sometimes random too (a small table, one row, one column, a column with a blank, all zeros), from its own random
stream, so every v1 seed still gives v1's run for a program that does not read the matrices; a run that leaves
M0-M9 changed counts as STATE; and --writes names the Home variables a program is MEANT to change (DataLoad
fills D1-D9 or C1-C9: --writes D,C), which then do not count as STATE.

WHAT ONE RUN DOES.  It loads the program, sometimes with random Statistics lists D1 and D2 (empty, one value, all
equal, ordinary, enormous, unequal lengths), and calls its main routine.  Then:
  - every CHOOSE gets a random answer at the moment it opens: an item, or Cancel;
  - every INPUT gets, at the moment it opens: Cancel, OK as shown, or random entries in some of its fields
    (ordinary numbers, 0, negatives, fractions, 1E300, 1E-300, a 13-digit number, and, where the field takes any type,
    sometimes a list);
  - every OK/Cancel message box gets a random answer;
  - a stream of random keys (any key code), taps (anywhere, often on the soft-key row) and drags is queued;
  - when the stream runs out, Esc is pressed whenever the program waits (idle_key), so a program that cannot be left
    with Esc shows up as a freeze.

WHAT COUNTS AS BROKEN (each run gets one verdict):
  CRASH      a calculator error (the PPL error a student would see as "Error: ...")
  GUARD      a call into the calculator with a value whose device answer has never been observed (Unverified):
             the program passed a built-in something it should have refused first
  FREEZE     the run did not finish within --seconds (a loop that never ends, or one that ignores Esc)
  STALL      the program waited for input with nothing left to give it and Esc did not end it
  STATE      the run left one of Home's variables (A-Z, L0-L9, the Statistics lists, angle) changed
  HARNESS    the harness cannot model something the program did (Unsupported): not the program's fault; listed
  OK         it ended normally
Each broken run is saved with its seed, so `--replay SEED` reruns exactly that run and prints its trace.

RUN
  python3 monkey_v1a.py PROGRAM.txt CALL [--runs 300] [--events 120] [--seed 1] [--seconds 20] [--lists]
                        [--replay SEED] [--out report.json] [--writes D,C,M1 ...]
    CALL      the program's main call as typed in Home, e.g. "TTESTLABG()"
    --lists   give the program random Statistics lists D1 and D2 in some runs
  Needs the harness ppl_run_v3e.py (beside this file, ./tools, ../tools or $TTL_TOOLS) and hp-prime-kit ($HPKIT).
"""
import collections
import copy
import json
import math
import os
import random
import signal
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
for cand in (os.environ.get('TTL_TOOLS', ''), HERE, os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools')):
    if cand and os.path.exists(os.path.join(cand, 'ppl_run_v3e.py')):
        sys.path.insert(0, cand)
        break
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
import ppl_run_v3e as R                      # noqa: E402
from ppl_run_v3e import Harness, ACCEPT, CANCEL, KEY   # noqa: E402

HOME_VARS = [c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'] + ['L%d' % i for i in range(10)] + \
            ['D%d' % i for i in range(10)] + ['C%d' % i for i in range(10)] + ['HAngle'] + \
            ['M%d' % i for i in range(10)]

NUMS_ORDINARY = [1, 2, 3, 5, 7, 10, 12, 15, 20, 25, 30, 50, 100, 0.5, 0.05, 0.01, 1.5, 2.5, 3.14159, 98.6, 206.3]
NUMS_EDGE = [0, -1, -5, -0.5, 1E300, -1E300, 1E-300, 1234567890123, 0.1 + 0.2, 1E12, 2.5E-8, 999999]


class TimeUp(Exception):
    pass


def _alarm(signum, frame):
    raise TimeUp()


class Monkey(Harness):
    """The harness, with dialogs answered at random at the moment they open."""

    def __init__(self, path, rng, app_data, events):
        Harness.__init__(self, path, idle_key=4, home_minus=True, app_data=app_data,
                         seed=rng.randrange(1 << 30), stall_limit=20000)
        self.m = rng
        self.trace = []
        for _ in range(events):
            self._queue_random_event()

    # ---- the stream of keys, taps and drags
    def _queue_random_event(self):
        r = self.m.random()
        if r < 0.40:
            code = self.m.choice([KEY['Esc'], KEY['Enter'], KEY['Left'], KEY['Right'], KEY['Up'], KEY['Down']]
                                 if self.m.random() < 0.6 else list(range(0, 51)))
            self.press(code)
        elif r < 0.85:
            if self.m.random() < 0.5:                       # the soft-key row
                x, y = self.m.randrange(0, 320), self.m.randrange(220, 240)
            else:
                x, y = self.m.randrange(0, 320), self.m.randrange(0, 240)
            self.tap(x, y, lift=self.m.random() < 0.5)
        else:
            n = self.m.randrange(2, 7)
            x, y = self.m.randrange(0, 320), self.m.randrange(0, 220)
            pts = []
            for _ in range(n):
                x = min(319, max(0, x + self.m.randrange(-60, 61)))
                y = min(239, max(0, y + self.m.randrange(-40, 41)))
                pts.append((x, y))
            self.drag(pts)

    # ---- CHOOSE: count the items as the harness does, then pick
    def _choose(self, nodes, frame):
        vals = [self.evaluate(n, frame) for n in nodes[1:]]
        items = vals[1] if len(vals) == 2 and isinstance(vals[1], list) else vals[1:]
        k = len(items)
        idx = 0 if (k == 0 or self.m.random() < 0.15) else self.m.randrange(1, k + 1)
        self.trace.append(('choose', R._std(vals[0]) if vals else '', k, idx))
        self._choices.appendleft(idx)
        return Harness._choose(self, nodes, frame)

    # ---- INPUT: read the field names (and whether a field is limited to reals), then answer
    def _input(self, nodes, frame):
        first = nodes[0] if nodes else None
        names, typed = [], []
        if first is not None:
            elems = first[1] if first[0] == 'seq' else [first]
            for el in elems:
                lim = False
                if el[0] == 'seq' and el[1] and el[1][0][0] == 'var':
                    lim = len(el[1]) > 1                      # {var, types, pos}: the types limit it
                    el = el[1][0]
                if el[0] == 'var':
                    names.append(el[1])
                    typed.append(lim)
        r = self.m.random()
        if r < 0.15 or not names:
            ans = CANCEL
        elif r < 0.30:
            ans = ACCEPT
        else:
            ans = {}
            for n, lim in zip(names, typed):
                if self.m.random() < 0.6:
                    ans[n] = self._value(lim)
        self.trace.append(('input', names, 'CANCEL' if ans is CANCEL else 'OK' if ans is ACCEPT else ans))
        self._answers.appendleft(ans)
        return Harness._input(self, nodes, frame)

    def _value(self, limited):
        r = self.m.random()
        if r < 0.55:
            v = self.m.choice(NUMS_ORDINARY)
        elif r < 0.92 or limited:
            v = self.m.choice(NUMS_EDGE)
        else:
            v = [float(self.m.choice(NUMS_ORDINARY)) for _ in range(self.m.randrange(1, 4))]
        return float(v) if not isinstance(v, list) else v

    def _msgbox(self, a):                                      # MSGBOX(text, 1): OK or Cancel
        self._msgbox_answers.appendleft(self.m.random() < 0.7)
        return Harness._msgbox(self, a)


def random_lists(rng):
    kind = rng.choice(['none', 'none', 'empty', 'one', 'equal', 'ordinary', 'ordinary', 'unequal', 'huge', 'pairs'])
    if kind == 'none':
        return None, kind
    def col(n, lo=0, hi=100):
        return [round(rng.uniform(lo, hi), rng.choice([0, 1, 2])) for _ in range(n)]
    if kind == 'empty':
        return {'D1': [], 'D2': []}, kind
    if kind == 'one':
        return {'D1': col(1), 'D2': col(1)}, kind
    if kind == 'equal':
        v = rng.choice([0.0, 5.0, 12.5])
        return {'D1': [v] * rng.randrange(2, 9), 'D2': [v] * rng.randrange(2, 9)}, kind
    if kind == 'ordinary':
        return {'D1': col(rng.randrange(2, 40)), 'D2': col(rng.randrange(2, 40))}, kind
    if kind == 'unequal':
        return {'D1': col(rng.randrange(2, 6)), 'D2': col(rng.randrange(20, 60))}, kind
    if kind == 'huge':
        return {'D1': col(rng.randrange(2, 9), -1E300, 1E300), 'D2': col(rng.randrange(2, 9), 1E-300, 2E-300)}, kind
    n = rng.randrange(2, 30)
    return {'D1': col(n), 'D2': col(n)}, kind


def _plain(v):
    """a value that compares by content (the kit's Matrix has no ==)"""
    if isinstance(v, R.interp.Matrix):
        return ('matrix', [list(r) for r in v.rows])
    return copy.deepcopy(v)


def snapshot(h):
    return dict((k, _plain(h.globals_.get(k))) for k in HOME_VARS)


def random_matrix(seed):
    """v1a: M1 for one run, from its own stream (so the lists and the events are v1's)"""
    mr = random.Random(seed * 7 + 1)
    kind = mr.choice(['zero', 'zero', 'small', 'row', 'column', 'blank', 'zeros'])
    if kind == 'zero':
        return None, kind
    r, c = {'small': (mr.randrange(2, 12), mr.randrange(2, 5)), 'row': (1, mr.randrange(2, 6)),
            'column': (mr.randrange(2, 15), 1), 'blank': (mr.randrange(3, 10), mr.randrange(2, 4)),
            'zeros': (mr.randrange(2, 6), mr.randrange(1, 4))}[kind]
    rows = [[0.0 if kind == 'zeros' else float(round(mr.uniform(0, 100), mr.choice([0, 1, 2]))) for _ in range(c)]
            for _ in range(r)]
    if kind == 'blank':
        rows[mr.randrange(r)][mr.randrange(c)] = float('inf')     # a blank cell reads as 1E499 or more
    return R.interp.Matrix(rows), kind


WRITES = set()          # v1a: Home variables the program is meant to change (--writes)


def _meant(k):
    return k in WRITES or (k[:1] in WRITES and k[1:].isdigit())


def one_run(path, call, seed, events, seconds, lists):
    rng = random.Random(seed)
    app, kind = random_lists(rng) if lists else (None, 'none')
    h = Monkey(path, rng, app, events)
    for k in range(10):                                   # v1a: the matrices exist, one zero each
        h.globals_.setdefault('M%d' % k, R.interp.Matrix([[0.0]]))
    if lists:
        m1, mkind = random_matrix(seed)
        if m1 is not None:
            h.globals_['M1'] = m1
            kind = kind + '+M1 ' + mkind
    before = snapshot(h)
    verdict, detail = 'OK', ''
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(seconds)
    t0 = time.time()
    try:
        h.execute(call)
    except TimeUp:
        verdict, detail = 'FREEZE', 'no end after %d s (in %s)' % (seconds, h._where())
    except R.Unverified as e:
        verdict, detail = 'GUARD', '%s (in %s)' % (str(e)[:200], ' > '.join(getattr(e, 'ppl_stack', [])[-3:]))
    except R.HarnessStall as e:
        verdict, detail = 'STALL', str(e)[:200]
    except R.Unsupported as e:
        verdict, detail = 'HARNESS', str(e)[:200]
    except R.HarnessScriptError as e:
        verdict, detail = 'HARNESS', 'monkey: ' + str(e)[:200]
    except RecursionError:
        verdict, detail = 'CRASH', 'recursion too deep'
    except Exception as e:
        verdict = 'CRASH'
        detail = '%s: %s (in %s)' % (type(e).__name__, str(e)[:200], ' > '.join(getattr(e, 'ppl_stack', [])[-3:]))
    finally:
        signal.alarm(0)
    if verdict == 'OK':
        after = snapshot(h)
        changed = [k for k in HOME_VARS if after[k] != before[k] and not _meant(k)]
        if changed:
            verdict, detail = 'STATE', 'changed: ' + ', '.join(changed)
    return {'seed': seed, 'verdict': verdict, 'detail': detail, 'lists': kind, 'secs': round(time.time() - t0, 2),
            'dialogs': len(h.trace), 'screens': len(h.screens), 'result': str(h.result)[:80] if verdict == 'OK' else '',
            'trace': h.trace[-12:]}


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    path, call = a[0], a[1]
    opt = {'--runs': 300, '--events': 120, '--seed': 1, '--seconds': 20, '--replay': None, '--out': None,
           '--writes': ''}
    lists = '--lists' in a
    i = 2
    while i < len(a):
        if a[i] == '--lists':
            i += 1
            continue
        opt[a[i]] = a[i + 1]
        i += 2
    runs, events, base, secs = int(opt['--runs']), int(opt['--events']), int(opt['--seed']), int(opt['--seconds'])
    WRITES.update(w.strip() for w in opt['--writes'].split(',') if w.strip())
    if opt['--replay'] is not None:
        r = one_run(path, call, int(opt['--replay']), events, secs, lists)
        print(json.dumps(r, indent=1, default=str))
        return
    tally = collections.Counter()
    bad = []
    t0 = time.time()
    for k in range(runs):
        seed = base * 1000003 + k
        r = one_run(path, call, seed, events, secs, lists)
        tally[r['verdict']] += 1
        if r['verdict'] != 'OK':
            bad.append(r)
    print('%s  %s: %d runs, %d events each, %.0f s' % (os.path.basename(path), call, runs, events, time.time() - t0))
    for v in ('OK', 'CRASH', 'GUARD', 'FREEZE', 'STALL', 'STATE', 'HARNESS'):
        if tally[v]:
            print('  %-8s %d' % (v, tally[v]))
    groups = collections.OrderedDict()
    for r in bad:
        key = (r['verdict'], r['detail'].split(' (in ')[0][:90])
        groups.setdefault(key, []).append(r)
    for (v, d), rs in groups.items():
        print('  %s x%d: %s   e.g. --replay %d' % (v, len(rs), d, rs[0]['seed']))
    if opt['--out']:
        json.dump({'tally': tally, 'bad': bad}, open(opt['--out'], 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
