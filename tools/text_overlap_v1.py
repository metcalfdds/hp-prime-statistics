#!/usr/bin/env python3
"""text_overlap_v1 -- fleet-wide check for TEXTOUT_P text that lands on top of other text
(28 Oct 2026).  Generalises Part F of verify_BurrLab_beta1c.py.

It records every screen the ppl_run_v3e harness captures (a BLIT_P to G0, a wait for input
with G0 drawn on directly, a dialog, or the end of a call) and, for each screen, every text
on it: (x, y, font, width argument, text).  A screen is one captured frame; text drawn to G0
directly between captures belongs to the next capture, which is the harness's own rule.

The post-processor then reports, per program:
  * collisions: two texts on one screen whose ink boxes overlap, with 2 px vertical
    clearance (as Part F).  Box width = min(chars * px/char, width argument), px/char
    6.5 (font 1), 8 (font 2), 9.5 (font 3), 11 (font 4+); ink height 10 / 13 / 16 / 19 px.
    Font 0 or none means the current font: treated as font 2.
    Same y with non-overlapping x is fine.  A re-draw at the identical (x, y, font) is a
    refresh, not a collision: the latest text at that spot is the one checked.
  * frame straddles: text whose box crosses an edge of a plot frame (a RECT_P at least
    120 x 80 px that is an outline or a fill).
  * overruns: right edge past 320 px, top above 0, or bottom below 240.
  * ghosts (informational): a different text re-drawn at the same spot with no background
    colour and no RECT_P clear between, which leaves the old glyphs showing.
Draw order is replayed at analysis time: a RECT_P with corners erases the earlier texts wholly
inside it (at the narrower measured widths), as the device's paint does and the harness's item
list does not.  The JSON written by --run/--walk keeps every distinct screen's draw list, so
--md re-analyses without re-running.

Usage
  python3 text_overlap_v1.py --run build/BurrLab/verify_BurrLab_beta1c.py [--json out.json]
      runs the verify script with the recorder installed and reports what its harness
      objects drew (the script's own output goes to --log FILE, default /dev/null).
  python3 text_overlap_v1.py --walk BurrLab_beta1c.txt [--call "Burr3(2,3,10,8)"]
      generic walk: starts the program (the EXPORT named like the file, or --call), picks
      every CHOOSE item down to --depth (3) levels, breadth-first, up to --runs (80) runs,
      and on each page taps the six soft keys once and presses the arrow, +, - keys, with
      idle_key = 4 (Esc) when the program waits with nothing queued.
  python3 text_overlap_v1.py --json a.json b.json ... --md Report.md
      merges JSON results into a Markdown report.
Environment: HPKIT (default /home/claude/kit/hp-prime-kit-HEAD); the harness is found in
  ../ref next to this file, or on sys.path.

As a module: install() patches Harness._capture; RECORDS holds the screens; report()
returns the findings.  It can join ppl_gate as a step: run, then fail on collisions > 0.

Limits: widths are estimates (average glyph widths, not measured per glyph); the walk
cannot reach pages behind INPUT forms that need particular values, drags, or taps at
plot positions; what the walk does not reach it does not check.
"""
import argparse
import collections
import hashlib
import json
import os
import runpy
import signal
import sys
import time


class RunTimeout(Exception):
    pass


def _alarm(signum, frame):
    raise RunTimeout('run budget spent')

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
for cand in (os.path.join(HERE, '..', 'ref'), HERE):
    cand = os.path.abspath(cand)
    if os.path.exists(os.path.join(cand, 'ppl_run_v3e.py')) and cand not in sys.path:
        sys.path.insert(0, cand)

CW = {1: 6.5, 2: 8.0, 3: 9.5, 4: 11.0, 5: 12.5, 6: 14.0, 7: 16.0}      # Part F: conservative
CW_NARROW = {1: 5.5, 2: 6.5, 3: 7.5, 4: 8.5, 5: 9.5, 6: 11.0, 7: 13.0}  # the harness's measured averages
INK = {1: 10, 2: 13, 3: 16, 4: 19, 5: 22, 6: 25, 7: 29}
CLEAR = 2                      # px of vertical clearance between rows (Part F)
SCREEN_W, SCREEN_H = 320, 240
SK = [27, 80, 133, 187, 240, 294]   # soft-key centres, y = 230

RECORDS = collections.OrderedDict()   # tag -> {'screens': {digest: [count, first_index, screen_dict]}, 'n': total}
_CUR_TAG = ['?']


def _font(f):
    try:
        f = int(f or 0)
    except (TypeError, ValueError):
        f = 0
    return f if f in CW else 2


def _box(t, cw=CW):
    f = _font(t['font'])
    w = len(t['text']) * cw[f]
    if t['width'] is not None:
        w = min(w, t['width'])
    return (t['x'], t['x'] + w, t['y'], t['y'] + INK[f])


def _covers(r, b):
    return r[0] <= b[0] and b[1] <= r[2] and r[1] <= b[2] and b[3] <= r[3]


def digest_screen(scr):
    """Compact dict of one harness Screen: the texts and the rectangles in draw order
    (so the paint can be replayed at analysis time), the menu flag, where it was captured."""
    items = []
    for it in scr.items:
        if it.__class__.__name__ == 'Text':
            t = it
            if not t.text.strip():
                continue
            try:
                x, y = float(t.x or 0), float(t.y or 0)
            except (TypeError, ValueError):
                continue
            w = t.width
            try:
                w = float(w) if w is not None else None
            except (TypeError, ValueError):
                w = None
            items.append({'x': x, 'y': y, 'font': _font(t.font), 'width': w, 'text': t.text,
                          'bg': t.bg is not None})
        elif it.__class__.__name__ == 'Shape' and it.cmd in ('RECT_P', 'RECT') and len(it.args) >= 4:
            try:
                x1, y1, x2, y2 = [float(v) for v in it.args[:4]]
            except (TypeError, ValueError):
                continue
            items.append({'rect': (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))})
    return {'items': items, 'menu': bool(scr.menu), 'reason': scr.reason, 'func': scr.func}


def paint(d):
    """Replay the draw order: a RECT_P with corners is a filled rectangle (the Prime fills
    with the edge colour when no fill is given), so it erases every earlier text whose ink
    box, at the narrower measured widths, lies wholly inside it.  -> (texts, frames), where
    a frame is a rectangle at least 120 x 80 px (a plot frame or a panel)."""
    texts, frames = [], []
    for it in d['items']:
        if 'rect' in it:
            r = it['rect']
            texts = [t for t in texts if not _covers(r, _box(t, CW_NARROW))]
            if r[2] - r[0] >= 120 and r[3] - r[1] >= 80:
                frames.append(r)
        else:
            texts.append(it)
    return texts, frames


def record(tag, scr):
    d = digest_screen(scr)
    key = hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()
    rec = RECORDS.setdefault(tag, {'screens': collections.OrderedDict(), 'n': 0})
    rec['n'] += 1
    e = rec['screens'].get(key)
    if e is None:
        rec['screens'][key] = [1, rec['n'], d]
    else:
        e[0] += 1


def install():
    """Patch the harness so every captured screen is recorded under the program's tag."""
    import ppl_run_v3e as R
    if getattr(R.Harness, '_overlap_hooked', False):
        return R
    orig_capture = R.Harness._capture
    orig_load = R.Harness.load_path

    def load_path(self, path):
        self._overlap_tag = os.path.basename(path)
        return orig_load(self, path)

    def _capture(self, reason):
        orig_capture(self, reason)
        record(getattr(self, '_overlap_tag', _CUR_TAG[0]), self.screens[-1])

    R.Harness.load_path = load_path
    R.Harness._capture = _capture
    R.Harness._overlap_hooked = True
    return R


# ------------------------------------------------------------------ analysis
def analyse_screen(d):
    """-> (collisions, straddles, overruns, ghosts) for one screen digest.  Each finding
    carries firm=True when it survives the narrower measured glyph widths too; a finding
    that only appears at the conservative widths is marginal (a few px, estimate-sensitive)."""
    last = collections.OrderedDict()
    ghosts = []
    texts, frames = paint(d)
    for t in texts:
        k = (round(t['x']), round(t['y']), t['font'])
        prev = last.get(k)
        if prev is not None and prev['text'] != t['text'] and not t['bg']:
            ghosts.append((prev['text'], t['text'], t['x'], t['y']))
        last[k] = t
    items = [(_box(t), _box(t, CW_NARROW), t) for t in last.values()]
    coll, strad, over = [], [], []
    for i in range(len(items)):
        (ax0, ax1, ay0, ay1), (_, nax1, _, _), a = items[i]
        if ax1 > SCREEN_W + 0.5 or ay0 < 0 or ay1 > SCREEN_H:
            over.append((a['text'], a['x'], a['y'], round(ax1), nax1 > SCREEN_W + 0.5 or ay0 < 0 or ay1 > SCREEN_H))
        for j in range(i + 1, len(items)):
            (bx0, bx1, by0, by1), (_, nbx1, _, _), b = items[j]
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 + CLEAR and by0 < ay1 + CLEAR:
                firm = ax0 < nbx1 and bx0 < nax1
                coll.append((a['text'], a['x'], a['y'], a['font'], b['text'], b['x'], b['y'], b['font'], firm))
        for (fx0, fy0, fx1, fy1) in frames:
            xo = ax0 < fx1 and ax1 > fx0
            yo = ay0 < fy1 and ay1 > fy0
            which, by = [], 0
            if xo and ay0 < fy1 < ay1:
                which.append('bottom'); by = max(by, ay1 - fy1)
            if xo and ay0 < fy0 < ay1:
                which.append('top'); by = max(by, fy0 - ay0)
            if yo and ax0 < fx0 < ax1:
                which.append('left'); by = max(by, fx0 - ax0)
            if yo and ax0 < fx1 < ax1:
                which.append('right'); by = max(by, ax1 - fx1)
            if which:
                firm = not (which == ['right'] and nax1 <= fx1)
                strad.append((a['text'], a['x'], a['y'], '/'.join(which), round(by, 1), firm))
    return coll, strad, over, ghosts


def severity(ay, af, by, bf):
    """'overlap' when the ink boxes themselves overlap; 'tight' when only the 2 px clearance
    is missing (rows 11 px apart in font 1, 14 px apart in font 2)."""
    a1, b1 = ay + INK[af], by + INK[bf]
    return 'overlap' if (ay < b1 and by < a1) else 'tight'


def fix_class(c):
    at, ax, ay, af, bt, bx, by, bf = c
    if abs(ay - by) < 1:
        return 'shorten / stagger (same row)'
    if abs(ay - by) < INK[max(af, bf)] * 0.5:
        return 'move a row (rows nearly on top of each other)'
    return 'move a row (rows too close)'


def _group(store, key, item, count, first, d):
    e = store.get(key)
    if e is None:
        store[key] = e = {'n_screens': 0, 'screen': first, 'func': d['func'], 'funcs': [], 'examples': [], 'firm': False, 'n_texts': 0}
    if d['func'] not in e['funcs'] and len(e['funcs']) < 3:
        e['funcs'].append(d['func'])
        e['func'] = ', '.join(e['funcs'])
    e['n_screens'] += count
    e['firm'] = e['firm'] or item[-1]
    tx = item[:1] if len(item) < 8 else (item[0], item[4])
    if tx not in e['examples']:
        e['n_texts'] += 1
        if len(e['examples']) < 3:
            e['examples'].append(tx)
    return e


def report(tag=None, records=None):
    """-> {tag: {...}} findings for every recorded program (or one).  Findings are grouped by
    layout spot (routine, positions, fonts): a page whose numbers change from screen to
    screen counts once, with up to three example texts."""
    out = {}
    for t, rec in (records or RECORDS).items():
        if tag is not None and t != tag:
            continue
        colls, strads, overs, ghosts = (collections.OrderedDict() for _ in range(4))
        for key, (count, first, d) in rec['screens'].items():
            c, s, o, g = analyse_screen(d)
            for it in c:
                e = _group(colls, (it[1], it[2], it[3], it[5], it[6], it[7]), it, count, first, d)
                e.update(ax=it[1], ay=it[2], af=it[3], bx=it[5], by=it[6], bf=it[7])
            for it in s:
                e = _group(strads, (it[1], it[2], it[3]), it, count, first, d)
                e.update(x=it[1], y=it[2], edge=it[3], by=max(e.get('by', 0), it[4]))
            for it in o:
                e = _group(overs, (it[1], it[2]), it, count, first, d)
                e.update(x=it[1], y=it[2], right=max(e.get('right', 0), it[3]))
            for it in g:
                e = ghosts.setdefault((it[2], it[3]), {'n_screens': 0, 'screen': first, 'func': d['func'],
                                                                   'x': it[2], 'y': it[3], 'examples': []})
                e['n_screens'] += count
                if len(e['examples']) < 3 and (it[0], it[1]) not in e['examples']:
                    e['examples'].append((it[0], it[1]))
        for e in colls.values():
            e['a'], e['b'] = e['examples'][0]
            e['severity'] = severity(e['ay'], e['af'], e['by'], e['bf'])
            e['fix'] = fix_class((e['a'], e['ax'], e['ay'], e['af'], e['b'], e['bx'], e['by'], e['bf']))
        for e in strads.values():
            e['text'] = e['examples'][0][0]
            e['fix'] = 'move axis labels inside the frame'
        for e in overs.values():
            e['text'] = e['examples'][0][0]
            e['fix'] = 'shorten / move left'
        out[t] = {
            'screens_total': rec['n'], 'screens_distinct': len(rec['screens']),
            'collisions': list(colls.values()), 'straddles': list(strads.values()),
            'overruns': list(overs.values()), 'ghosts': list(ghosts.values()),
        }
    return out


# ------------------------------------------------------------------ drivers
def run_script(path, log):
    """Run a verify script with the recorder installed.  Its stdout goes to `log`."""
    install()
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    old_out, old_argv = sys.stdout, sys.argv
    sys.argv = [path]
    t0 = time.time()
    err = None
    with open(log, 'w') as f:
        sys.stdout = f
        try:
            runpy.run_path(path, run_name='__main__')
        except SystemExit:
            pass
        except Exception as e:      # the script's own failure: keep what was recorded
            err = '%s: %s' % (type(e).__name__, str(e)[:200])
        finally:
            sys.stdout = old_out
            sys.argv = old_argv
    return err, time.time() - t0


def _entry(h, prog, call):
    if call:
        return call
    stem = os.path.basename(prog).split('_')[0]
    for n in h.funcs:
        if n.lower() == stem.lower():
            return n + '()'
    for n in h.funcs:
        if n.lower().startswith(stem.lower()[:6]) and not h.funcs[n][0]:
            return n + '()'
    raise SystemExit('no entry point found for %s; pass --call' % prog)


def walk(prog, call=None, depth=3, max_runs=80, per_run_s=60, data=None):
    """Breadth-first walk of the program's CHOOSE menus with the recorder installed."""
    R = install()
    tag = os.path.basename(prog)
    _CUR_TAG[0] = tag
    kw = dict(strict=False, idle_key=4, cas='fail', stall_limit=3000, max_screens=400)
    if data:
        kw['app_data'] = data
    # an app program (VIEW "label", routine()) is walked through every view routine
    probe = R.Harness(prog, **kw)
    entries = [call] if call else [n + '()' for _, n in probe.views] or [_entry(probe, prog, None)]
    plans = collections.deque((e, ()) for e in entries)
    seen = set()
    runs, errors, stalls = 0, collections.Counter(), 0
    t_start = time.time()
    entry = ', '.join(entries) if len(entries) > 1 else entries[0]
    while plans and runs < max_runs:
        entry_call, plan = plans.popleft()
        for variant in ('keys', 'softkeys'):
            h = R.Harness(prog, **kw)
            h._table['RANDSEED'] = lambda a, site: (h.rng.seed(int(a[0])), 0.0)[1]
            h.choose(*plan)
            if variant == 'keys':
                h.press('Right', 'Right', 'Up', 'Plus', 'Left', 'Down', 'Minus', 'Zero')
            else:
                for x in SK:
                    h.tap(x, 230)
                h.press('Enter')
            signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(per_run_s)
            try:
                h.execute(entry_call)
            except Exception as e:
                nm = type(e).__name__
                if 'Stall' in nm or nm == 'RunTimeout':
                    stalls += 1
                else:
                    errors[nm + ': ' + str(e)[:80]] += 1
            finally:
                signal.alarm(0)
            runs += 1
            if variant == 'keys':
                # expand: every CHOOSE met after the plan was consumed, first unseen one
                chs = [d for d in h.dialogs if isinstance(d, R.Choose)]
                if len(chs) > len(plan) and len(plan) < depth:
                    nxt = chs[len(plan)]
                    for i in range(1, len(nxt.items) + 1):
                        p = plan + (i,)
                        if (entry_call, p) not in seen:
                            seen.add((entry_call, p))
                            plans.append((entry_call, p))
            if time.time() - t_start > per_run_s * 10:
                plans.clear()
                break
    return {'runs': runs, 'stalls': stalls, 'errors': dict(errors.most_common(5)), 'budget_s': per_run_s,
            'entry': entry, 'seconds': round(time.time() - t_start, 1)}


# ------------------------------------------------------------------ report
def to_markdown(results, out):
    """results: {tag: {'name', 'version', 'mode', 'findings', 'walk', 'err'}}"""
    L = ['# Overlap sweep -- %s' % time.strftime('%Y-%m-%d'), '',
         'Text that lands on top of other text, straddles a plot frame edge, or runs off the screen, as the '
         'ppl_run_v3e harness records it.  Widths are estimates: 6.5 / 8 / 9.5 px per character for fonts 1 / 2 / 3 '
         '(Part F of verify_BurrLab_beta1c), ink 10 / 13 / 16 px, 2 px row clearance.  A finding is **firm** when it '
         'is still there at the harness\'s narrower measured widths (5.5 / 6.5 / 7.5 px per character); otherwise it '
         'is marginal (a few px, estimate-sensitive).  "Overlap" = the ink boxes themselves overlap; "tight" = rows '
         'only inside the 2 px clearance (11 px apart in font 1, 14 px in font 2).  Findings are grouped by layout '
         'spot (positions and fonts; the routine column names where the screen was captured), so a page whose numbers '
         'change counts once.  Tool: tools/text_overlap_v1.py.', '',
         '| Program | Version | Driver | Screens (distinct / total) | Overlaps (firm) | Tight rows | Frame straddles (firm) | Overruns (firm) | Ghost redraws |',
         '|---|---|---|---|---|---|---|---|---|']
    for tag, r in results.items():
        f = r['findings']
        f['collisions'].sort(key=lambda c: (c['severity'] != 'overlap', not c['firm'], -c['n_screens']))
        ov = [c for c in f['collisions'] if c['severity'] == 'overlap']
        L.append('| %s | %s | %s | %d / %d | %d (%d) | %d | %d (%d) | %d (%d) | %d |' % (
            r['name'], r['version'], r['mode'], f['screens_distinct'], f['screens_total'],
            len(ov), sum(c['firm'] for c in ov), len(f['collisions']) - len(ov),
            len(f['straddles']), sum(x['firm'] for x in f['straddles']),
            len(f['overruns']), sum(x['firm'] for x in f['overruns']), len(f['ghosts'])))
    L.append('')
    for tag, r in results.items():
        f = r['findings']
        if not (f['collisions'] or f['straddles'] or f['overruns']):
            continue
        L.append('## %s %s' % (r['name'], r['version']))
        if r.get('walk'):
            w = r['walk']
            L.append('Generic walk: %d runs, %d stalls or budget stops, %ss; entry %s; errors: %s' % (
                w['runs'], w['stalls'], w['seconds'], w['entry'], w['errors'] or 'none'))
        if r.get('err'):
            L.append('Driver ended early with: %s' % r['err'])
        if f['collisions']:
            L.append('')
            L.append('| # | Kind | Firm | Screen | Routine | Text A (x, y, font) | Text B (x, y, font) | Screens | Fix |')
            L.append('|---|---|---|---|---|---|---|---|---|')
            for i, c in enumerate(f['collisions'][:10], 1):
                L.append('| %d | %s | %s | %d | %s | `%s` (%g, %g, f%d) | `%s` (%g, %g, f%d) | %d | %s |' % (
                    i, c['severity'], 'yes' if c['firm'] else 'no', c['screen'], c['func'],
                    c['a'].replace('|', '\\|')[:40], c['ax'], c['ay'], c['af'],
                    c['b'].replace('|', '\\|')[:40], c['bx'], c['by'], c['bf'], c['n_screens'], c['fix']))
            if len(f['collisions']) > 10:
                L.append('')
                L.append('... and %d more collision spots.' % (len(f['collisions']) - 10))
        if f['straddles']:
            L.append('')
            L.append('Frame straddles (first 10): ' + '; '.join(
                '`%s` at (%g, %g) crosses the %s edge by %g px%s [screen %d, %s]' % (
                    x['text'][:30], x['x'], x['y'], x['edge'], x['by'], '' if x['firm'] else ' (marginal)', x['screen'], x['func'])
                for x in f['straddles'][:10]))
        if f['overruns']:
            L.append('')
            L.append('Overruns (first 10): ' + '; '.join(
                '`%s` at (%g, %g) right edge %d%s [screen %d, %s]' % (
                    x['text'][:30], x['x'], x['y'], x['right'], '' if x['firm'] else ' (marginal)', x['screen'], x['func'])
                for x in f['overruns'][:10]))
        L.append('')
    with open(out, 'w') as fh:
        fh.write('\n'.join(L) + '\n')


def _records_from_json(raw):
    recs = collections.OrderedDict()
    for tag, r in raw.items():
        recs[tag] = {'n': r['n'], 'screens': collections.OrderedDict(
            (k, [v[0], v[1], v[2]]) for k, v in r['screens'].items())}
    return recs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--run', help='a verify script to run with the recorder installed')
    ap.add_argument('--walk', help='a program to walk generically')
    ap.add_argument('--call', help='entry call for --walk, e.g. "Burr3(2,3,10,8)"')
    ap.add_argument('--depth', type=int, default=3)
    ap.add_argument('--runs', type=int, default=80)
    ap.add_argument('--budget', type=int, default=60, help='seconds per run; the walk stops after 10 x this')
    ap.add_argument('--log', default='/dev/null', help="the driver's own stdout")
    ap.add_argument('--json', nargs='*', help='write (with --run/--walk) or merge (with --md) JSON')
    ap.add_argument('--md', help='write a Markdown report from the JSON files')
    ap.add_argument('--tag', help='record under this tag only (default: every harness)')
    o = ap.parse_args()
    if o.md:
        results = collections.OrderedDict()
        rep = None
        for p in o.json or []:
            with open(p) as fh:
                blob = json.load(fh)
            if 'raw' in blob:
                rep = report(records=_records_from_json(blob['raw']))
                for tag, r in blob['results'].items():
                    r['findings'] = rep[tag]
                results.update(blob['results'])
            else:
                results.update(blob)
            del blob                           # the raw draw lists are large; one file at a time
        to_markdown(results, o.md)
        print('wrote', o.md)
        return
    results = collections.OrderedDict()
    err = walkinfo = None
    if o.run:
        err, secs = run_script(o.run, o.log)
        mode = 'verify script %s' % os.path.basename(o.run)
    elif o.walk:
        walkinfo = walk(o.walk, o.call, o.depth, o.runs, o.budget)
        mode = 'generic walk'
    else:
        ap.error('--run, --walk or --md')
    rep = report()
    for tag, f in rep.items():
        if o.tag and tag != o.tag:
            continue
        stem = tag.rsplit('.txt', 1)[0]
        name, _, ver = stem.partition('_')
        results[tag] = {'name': name, 'version': ver, 'mode': mode, 'findings': f, 'err': err, 'walk': walkinfo}
        print('%-28s screens %4d/%-5d collisions %3d (firm %3d) straddles %3d overruns %3d ghosts %3d%s' % (
            tag, f['screens_distinct'], f['screens_total'], len(f['collisions']),
            sum(c['firm'] for c in f['collisions']), len(f['straddles']),
            len(f['overruns']), len(f['ghosts']), ('  driver error: ' + err) if err else ''))
    if walkinfo:
        print('walk:', walkinfo)
    if o.json:
        raw = collections.OrderedDict((t, {'n': r['n'], 'screens': r['screens']}) for t, r in RECORDS.items()
                                      if t in results)
        with open(o.json[0], 'w') as fh:
            json.dump({'results': results, 'raw': raw}, fh)


if __name__ == '__main__':
    main()
