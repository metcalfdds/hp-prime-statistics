#!/usr/bin/env python3
"""caps_probe_v1.py -- what each INPUT field of a program accepts (Roger, 2 Nov 2026: "Maybe we need to check for
'reasonable' caps on data a student would enter").  Roger Metcalf & Claude, 2 Nov 2026, night.

The monkey (tools/monkey_v1b.py) drives the program at random, but every INPUT it meets gets ONE field typed with a
value from a ladder (0, -1, 0.5, 1,000 ... 1E100), the other fields left as the form shows them, so whatever happens
next belongs to that one value.  After each run the timeline says, for each typed value:
  R  refused: a message box that reads like a refusal ("must", "from ... to", "at most" ...) before the next form
     or menu, or the same form again;  M  a message box of another kind (a notice), the program going on;
  A  accepted: the program went on;
  C  the run crashed right after it;  F  the run froze right after it (no end within --seconds).
For each field it reports what was tried and what came of it, and the largest value accepted.

RUN  python3 tools/caps_probe_v1.py PROGRAM.txt CALL [--runs 80] [--seconds 15] [--lists] [--out fields.json]
"""
import collections
import json
import os
import random
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.environ.get('TTL_TOOLS', HERE)            # the repository's tools/, where this file lives
sys.path.insert(0, TOOLS)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
argv0 = sys.argv
sys.argv = ['monkey_v1b.py']
import monkey_v1b as M  # noqa: E402
sys.argv = argv0
import ppl_run_v3e as R  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

REFUSE = ('must', 'between', ' from ', 'at least', 'at most', 'no more than', 'too ', 'not ', 'only ', 'cannot',
          "can't", 'invalid', 'enter ', 'needs', 'need ', 'whole number', 'positive', 'less than', 'more than',
          'greater', 'smaller', 'larger', 'above', 'below', 'out of', 'range', 'up to')
LADDER = [1000000, 1000, 1E9, 0, 1E15, -1, 10000, 100000, 0.5, 1E7, 1E12, 1E100]   # the telling values first


class Probe(M.Monkey):
    def __init__(self, path, rng, app, events, plan):
        M.Monkey.__init__(self, path, rng, app, events)
        self.plan = plan            # (field index cursor, ladder cursor) per form title, shared across runs
        self.probes = []            # (timeline index, title, name, value)

    def _input(self, nodes, frame):
        first = nodes[0] if nodes else None
        names = []
        if first is not None:
            elems = first[1] if first[0] == 'seq' else [first]
            for el in elems:
                if el[0] == 'seq' and el[1] and el[1][0][0] == 'var':
                    el = el[1][0]
                if el[0] == 'var':
                    names.append(el[1])
        where = self._where()
        if names and self.m.random() < 0.85:
            key = (where, tuple(names))
            k = self.plan[key]
            self.plan[key] += 1
            name = names[k % len(names)]
            val = LADDER[(k // len(names)) % len(LADDER)]
            self.probes.append((len(self.timeline), where, name, float(val)))
            self._answers.appendleft({name: float(val)})
        else:
            self._answers.appendleft(M.CANCEL if self.m.random() < 0.5 else M.ACCEPT)
        return R.Harness._input(self, nodes, frame)


def one_run(path, call, seed, events, seconds, lists, plan):
    rng = random.Random(seed)
    app, _ = M.random_lists(rng) if lists else (None, 'none')
    h = Probe(path, rng, app, events, plan)
    for k in range(10):
        h.globals_.setdefault('M%d' % k, R.interp.Matrix([[0.0]]))
    verdict = 'OK'
    signal.signal(signal.SIGALRM, M._alarm)
    signal.alarm(seconds)
    try:
        h.execute(call)
    except M.TimeUp:
        verdict = 'F'
    except (R.HarnessStall, R.Unsupported, R.HarnessScriptError):
        verdict = 'H'
    except Exception:
        verdict = 'C'
    finally:
        signal.alarm(0)
    out = []
    tl = h.timeline
    for n, (i, where, name, val) in enumerate(h.probes):
        rec = tl[i][1] if i < len(tl) and tl[i][0] == 'input' else None
        if rec is None or not rec.accepted:
            continue
        nxt = None
        for ev in tl[i + 1:]:
            if ev[0] in ('msgbox', 'input', 'choose'):
                nxt = ev
                break
            if ev[0] == 'event':            # a key or tap taken: the program went on with the value
                break
        last = n == len(h.probes) - 1
        if nxt is None:
            res = verdict if (last and verdict in ('C', 'F')) else 'A'
        elif nxt[0] == 'msgbox':
            t_ = R._std(nxt[1].text).lower() if hasattr(nxt[1], 'text') else ''
            res = 'R' if any(w in t_ for w in REFUSE) else 'M'
        elif nxt[0] == 'input' and nxt[1].title == rec.title and list(nxt[1].names) == list(rec.names):
            res = 'R'
        else:
            res = 'A'
        lbl = ''
        try:
            j = list(rec.names).index(name)
            lbl = R._std(rec.labels[j]) if isinstance(rec.labels, list) and j < len(rec.labels) else ''
            hp = R._std(rec.helps[j]) if isinstance(rec.helps, list) and j < len(rec.helps) else ''
        except Exception:
            hp = ''
        msg = R._std(nxt[1].text)[:80] if nxt is not None and nxt[0] == 'msgbox' and hasattr(nxt[1], 'text') else ''
        out.append({'where': where, 'title': rec.title[:60], 'name': name, 'label': lbl[:30], 'help': hp[:80],
                    'value': val, 'res': res, 'msg': msg})
    return out


def main():
    a = sys.argv[1:]
    path, call = a[0], a[1]
    opt = {'--runs': 80, '--seconds': 15, '--out': None, '--seed': 5}
    lists = '--lists' in a
    i = 2
    while i < len(a):
        if a[i] == '--lists':
            i += 1
            continue
        opt[a[i]] = a[i + 1]
        i += 2
    plan = collections.Counter()
    fields = collections.OrderedDict()
    t0 = time.time()
    for k in range(int(opt['--runs'])):
        for r in one_run(path, call, int(opt['--seed']) * 1000003 + k, 60, int(opt['--seconds']), lists, plan):
            key = (r['title'], r['name'])
            f = fields.setdefault(key, {'where': r['where'], 'label': r['label'], 'help': r['help'], 'tries': {},
                                        'msgs': set()})
            f['tries'].setdefault(r['value'], collections.Counter())[r['res']] += 1
            if r['msg']:
                f['msgs'].add(r['msg'])
                f.setdefault('vmsg', {}).setdefault(repr(r['value']), r['res'] + ': ' + r['msg'])
    rows = []
    for (title, name), f in fields.items():
        acc = [v for v, c in f['tries'].items() if (c['A'] or c['M']) and not c['R']]
        rows.append({'title': title, 'name': name, 'where': f['where'], 'label': f['label'], 'help': f['help'],
                     'max_ok': max(acc) if acc else None,
                     'tries': {repr(v): dict(c) for v, c in sorted(f['tries'].items())},
                     'msgs': sorted(f['msgs'])[:3], 'vmsg': f.get('vmsg', {})})
    name = os.path.basename(path)
    print('%s: %d runs, %.0f s, %d fields reached' % (name, int(opt['--runs']), time.time() - t0, len(rows)))
    for r in rows:
        bad = [v for v, c in r['tries'].items() if c.get('C') or c.get('F')]
        print('  %-24s %-8s max accepted %-8s %s%s' % (r['title'][:24], r['name'], r['max_ok'],
                                                      ' '.join('%s:%s' % (v, ''.join(sorted(c))) for v, c in
                                                               r['tries'].items()),
                                                      ('  CRASH/FREEZE at ' + ','.join(bad)) if bad else ''))
    if opt['--out']:
        json.dump(rows, open(opt['--out'], 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
