#!/usr/bin/env python3
"""ovlist.py out.json [--all] -- compact full listing of an overlap JSON (firm overlaps,
tight rows, straddles, overruns), grouped by routine."""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import text_overlap_v1 as T

def listing(rep, show_all=False):
    for tag, f in rep.items():
        ov = [c for c in f['collisions'] if c['severity'] == 'overlap']
        tight = [c for c in f['collisions'] if c['severity'] != 'overlap']
        print('== %s: overlaps %d (firm %d), tight %d, straddles %d (firm %d), overruns %d (firm %d)' % (
            tag, len(ov), sum(c['firm'] for c in ov), len(tight),
            len(f['straddles']), sum(x['firm'] for x in f['straddles']),
            len(f['overruns']), sum(x['firm'] for x in f['overruns'])))
        def line(c):
            return '%s%s %s | A %r (%g,%g,f%d) | B %r (%g,%g,f%d) | n=%d' % (
                'F' if c['firm'] else 'm', 'OV' if c['severity'] == 'overlap' else 'tt', c['func'],
                c['a'][:34], c['ax'], c['ay'], c['af'], c['b'][:34], c['bx'], c['by'], c['bf'], c['n_screens'])
        seen = set()
        for c in sorted(ov, key=lambda c: (c['func'], c['ay'], c['by'])):
            k = (c['func'], c['ay'], c['af'], c['by'], c['bf'], c['firm'])
            if k in seen and not show_all:
                continue
            seen.add(k)
            print('  ' + line(c))
        seen = set()
        for c in sorted(tight, key=lambda c: (c['func'], c['ay'], c['by'])):
            k = (c['func'], c['ay'], c['af'], c['by'], c['bf'])
            if k in seen and not show_all:
                continue
            seen.add(k)
            print('  ' + line(c))
        for x in f['straddles']:
            print('  %sSTR %s %r (%g,%g) %s edge by %g' % ('F' if x['firm'] else 'm', x['func'], x['text'][:30], x['x'], x['y'], x['edge'], x['by']))
        for x in f['overruns']:
            print('  %sRUN %s %r (%g,%g) right %d' % ('F' if x['firm'] else 'm', x['func'], x['text'][:30], x['x'], x['y'], x['right']))

