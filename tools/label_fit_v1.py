#!/usr/bin/env python3
"""label_fit_v1 -- a number cut short by TEXTOUT_P's width argument (2 Nov 2026; the same evening, any text whose
cut-off part holds a digit, after the Virtual Calculator showed ScatterLab's "SSE = 18053333333" as "SSE = 1805333333").

Why.  TEXTOUT_P(text, G, x, y, font, colour, width) draws at most `width` pixels of the text and drops the rest.
For prose that is untidy; for a number it is a wrong number: StatDist v2.7g printed "4000000" as "400000" on the
Virtual Calculator (1 Nov 2026, Lessons Learned v7zi section 6, "never clip a number").  text_overlap_v1 measures a
text as min(its width, the width argument), so it can never see this.  This tool can: for every text the harness
recorded that reads as a number (digits, a point, a sign, the calculator's small capital E), it measures the text at
the NARROW glyph widths (5.5 / 6.5 / 7.5 px a character for fonts 1 / 2 / 3+, 3 px for a decimal point; font 1 is
about 5.5 px a character on the Virtual Calculator, and "0.03" is 20 px) and reports it when even that is wider than
its width argument: the calculator would cut it.

As a module (inside a verify script, after text_overlap_v1.install() and the runs):
    import label_fit_v1 as LF
    cut = LF.clipped(OV.RECORDS)          # {tag: [(text, x, y, font, width, measured), ...]}
From the command line, on the JSON text_overlap_v1 --run/--walk writes:
    python3 label_fit_v1.py walk.json
"""
import json
import re
import sys

NARROW = {1: 5.5, 2: 6.5, 3: 7.5}
POINT = 3.0
NUM = re.compile(r'^[\s\-−+]?[0-9][0-9.,]*(ᴇ[\-−+]?[0-9]+)?%?$')


def measure(text, font):
    cw = NARROW.get(font, 7.5 if (font or 0) > 3 else NARROW[2])
    return sum(POINT if ch == '.' else cw for ch in text)


def is_number(text):
    return bool(NUM.match(text.strip()))


def _items(records):
    for tag, rec in records.items():
        screens = rec['screens'].values() if isinstance(rec.get('screens'), dict) else rec.get('screens', [])
        for e in screens:
            d = e[2] if isinstance(e, (list, tuple)) else e
            for it in d.get('items', []):
                if 'text' in it:
                    yield tag, it


def hidden_tail(text, font, width, slack=1.0):
    """the part of text past its width argument, measured at the narrow widths ('' when it all fits)"""
    cw = NARROW.get(font, 7.5 if (font or 0) > 3 else NARROW[2])
    run = 0.0
    for i, ch in enumerate(text):
        run += POINT if ch == '.' else cw
        if run > width + slack:
            return text[i:]
    return ''


def clipped(records, slack=1.0):
    """{tag: sorted list of (text, x, y, font, width, measured)} for every text whose width argument cuts off a
    digit: a number cut short ("100000" shown as "10000"), and, since 2 Nov 2026 evening, a number at the end of a
    line of text ("SSE = 18053333333" shown as "SSE = 1805333333" on the Virtual Calculator, ScatterLab beta 2e)"""
    out = {}
    for tag, it in _items(records):
        t, w = it['text'], it.get('width')
        if w is None:
            continue
        tail = hidden_tail(t.rstrip(), it.get('font'), w, slack)
        if is_number(t) and tail or re.search(r'[0-9]', tail):
            m = measure(t.strip(), it.get('font'))
            out.setdefault(tag, set()).add((t, it['x'], it['y'], it.get('font'), w, round(m, 1)))
    return dict((k, sorted(v)) for k, v in out.items())


def main():
    for p in sys.argv[1:]:
        raw = json.load(open(p, encoding='utf-8'))
        recs = raw.get('raw', raw.get('records', raw))     # text_overlap_v1 --json writes {'results', 'raw'}
        res = clipped(recs)
        if not res:
            print('%s: no number cut by its width argument' % p)
        for tag, lst in res.items():
            print('%s: %d numbers cut' % (tag, len(lst)))
            for x in lst[:20]:
                print('   %r at (%g, %g), font %s, width %g, measured %g' % x)


if __name__ == '__main__':
    main()
