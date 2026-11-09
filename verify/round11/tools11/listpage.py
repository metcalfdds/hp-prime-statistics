"""Round 11: help pages given to a page routine as a LIST of lines (and often a parallel list of colours).

The list is read into Page's lines with a made-up y (one step a line, an empty string as a gap), so blocks, items,
the approved changes, the wrapping and the splitting are Page's own.  The new page is a list again: a gap becomes
an empty string, and the colours follow their lines."""
import re
from hp11 import segs_to_marked, marked_to_code, plain, W
import pagea
from pagea import Page, Line

STEP = 10


class _M:
    """a regex match stand-in for Line()"""
    def __init__(self, d):
        self.d = d

    def group(self, k):
        return self.d.get(k)

    def groupdict(self):
        return dict(self.d)


def split_top(body):
    """the top-level, comma-separated elements of a list literal's inside"""
    out, depth, cur, instr = [], 0, '', False
    for ch in body:
        if ch == '"':
            instr = not instr
        if not instr:
            if ch in '({[':
                depth += 1
            elif ch in ')}]':
                depth -= 1
            elif ch == ',' and depth == 0:
                out.append(cur)
                cur = ''
                continue
        cur += ch
    if cur.strip():
        out.append(cur)
    return [e.strip() for e in out]


def find_list(s, start):
    """the list literal that opens at or after position start: (index of '{', index after '}')"""
    i = s.index('{', start)
    depth, j, instr = 0, i, False
    while True:
        ch = s[j]
        if ch == '"':
            instr = not instr
        elif not instr:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i, j + 1
        j += 1


class ListPage(Page):
    def __init__(self, exprs, colors, parser, font=1, maxw=300, marker=None):
        self.font, self.varw, self.maxw, self.step = font, {}, maxw, STEP
        self.lines, self.other, self.log = [], [], []
        self.marker = marker
        y = 0
        for k, e in enumerate(exprs):
            if e.strip() == '""':
                y += STEP
                continue
            col = colors[k] if colors else 'none'
            d = {'pre': '', 'expr': e, 'x': '0', 'y': str(y), 'post': col, 'mid': ''}
            l = Line(k, e, _M(d), parser)
            if marker and l.text.startswith(marker):
                l.text = l.text[len(marker):]
                l.post = 'MARK'
                l.marked = True
            else:
                l.marked = False
            self.lines.append(l)
            y += STEP
        self.blocks = []
        for l in self.lines:
            b = self.blocks[-1] if self.blocks else None
            if b and l.y - b[-1].y == STEP and l.post == b[-1].post:
                b.append(l)
            else:
                self.blocks.append([l])
        self.items = []
        for bi, blk in enumerate(self.blocks):
            cur = None
            for l in blk:
                if cur and pagea.cont(cur['lines'][-1].text, l.text, cur['lines'][0].text):
                    cur['lines'].append(l)
                    cur['codes'] += l.codes
                else:
                    cur = {'lines': [l], 'new': None, 'block': bi, 'codes': list(l.codes)}
                    self.items.append(cur)

    def pages(self, cap):
        """-> list of pages; each a list of (expr, colour) with ('""', None) for a gap"""
        placed = self.place(ymax=(cap - 1) * STEP, y_first=0)
        out = []
        for page in placed:
            rows, last = [], None
            for it, t, y, tmpl in page:
                idx = y // STEP
                while len(rows) < idx:
                    rows.append(('""', None))
                if isinstance(t, str):
                    txt = (self.marker if tmpl.marked else '') + t
                    expr = marked_to_code(txt, it['codes'])
                else:
                    expr = t.expr
                rows.append((expr, tmpl.post))
            out.append(rows)
        return out

    def too_wide(self, page_rows):
        return []
