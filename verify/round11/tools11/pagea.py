"""Round 11: help pages drawn line by line at fixed y (TEXTOUT_P, or a helper that takes x and y).

A page is read from its source lines into BLOCKS (lines that share x, colour/font and the line step, with no gap) and
each block into ITEMS (a sentence or a list entry: a line that starts a new entry begins an item).  The approved
changes are applied to the items' text; a changed item is wrapped again at the calculator's own glyph widths;
an unchanged item keeps its lines and code exactly.  Then every line gets its y again (the step inside a block,
the page's own gap between blocks), and a page that would pass the last y is split at a block (or item) boundary.
"""
import re
from hp11 import Parser, segs_to_marked, marked_to_code, wrap, W, plain, norm, VAR_RE

ITEM = re.compile(r'^\s*(\S+(, \S+)?( \S+)?) = |^\s*[A-Z][A-Za-z0-9 /-]{0,20}:|^\s*[-*•] |^\s*\(\S{1,4}\) |^\s*\d+[.)] ')


def ind(s):
    return len(re.match(r' *', plain(s)).group(0))


LOOSE = [True]


TABLE = re.compile(r'\S {3,}\S')


def cont(prev, nxt, first):
    """does line nxt carry on the item whose first line is first (prev is the line before)?"""
    p, n = plain(prev).rstrip(), plain(nxt)
    if not n.strip() or not p.strip():
        return False
    if TABLE.search(n) or TABLE.search(p):
        return False                       # a table row (columns lined up with spaces) stands alone
    if ind(nxt) > ind(first):
        return True
    if p[-1] == ',':
        return True                        # a list that goes on: "... 30°," / "ν = 3."
    if LOOSE[0]:
        # prose: a line that does not end a sentence goes on ('.)' and '."' end one too)
        return not (p[-1] in '.;:!?' or p.endswith(('.)', '.)"', '."', "?)", ".'")))
    if ITEM.match(n):
        return False
    c = n.lstrip()[0]
    if 'a' <= c <= 'z' and p[-1] not in '.;:!?':
        return True
    if p[-1] in ',(±+−-×/' or p.endswith((' and', ' or', ' the', ' a', ' of', ' to', ' in', ' is', ' =',
                                                       ' by', ' with', ' for', ' its', ' as', ' at', ' on', ' from')):
        return True
    return False


class Line:
    def __init__(self, idx, raw, m, parser):
        self.idx, self.raw = idx, raw
        gd = m.groupdict()
        self.pre, self.expr, self.y, self.post = m.group('pre'), m.group('expr'), int(m.group('y')), m.group('post')
        self.x = int(gd['x']) if gd.get('x') is not None else None
        self.segs = parser.parse(self.expr)
        self.text, self.codes = segs_to_marked(self.segs)
        self.mid = m.group('mid') if 'mid' in m.groupdict() and m.group('mid') is not None else ', '
        self.sep = gd.get('sep') or ', '

    def code(self, y=None, expr=None):
        e = self.expr if expr is None else expr
        yy = self.y if y is None else y
        if self.x is None:
            return '%s%s%s%d%s' % (self.pre, e, self.mid, yy, self.post)
        return '%s%s%s%d%s%d%s' % (self.pre, e, self.mid, self.x, self.sep, yy, self.post)


class Page:
    def __init__(self, src_lines, a, b, call_re, parser, font=1, maxw=None, step=None, varw=None, ylimit=None, exclude=None):
        """src_lines: the file's lines (0-based list); a..b: the 1-based line range of the page's text calls"""
        self.font, self.varw = font, varw or {}
        self.lines = []
        self.other = []
        for i in range(a - 1, b):
            raw = src_lines[i]
            m = call_re.match(raw)
            if m and (ylimit is None or int(m.group('y')) < ylimit) and not (exclude and exclude.search(raw)):
                self.lines.append(Line(i, raw, m, parser))
            elif raw.strip() and not raw.strip().startswith('//'):
                self.other.append((i, raw))
        self.lines.sort(key=lambda l: l.y)
        self.maxw = maxw
        if step is None:                       # the page's own pitch: its most common line step
            import collections
            c = collections.Counter(b2.y - b1.y for b1, b2 in zip(self.lines, self.lines[1:]) if 0 < b2.y - b1.y <= 14)
            step = c.most_common(1)[0][0] if c else 13
        self.step = step
        # blocks
        self.blocks = []
        for l in self.lines:
            b = self.blocks[-1] if self.blocks else None
            if b and abs(l.y - b[-1].y - self.step) <= 1 and l.post == b[-1].post and l.x == b[-1].x:
                b.append(l)
            else:
                self.blocks.append([l])
        # items: [ {'lines': [Line], 'text': None or new marked text} ]
        self.items = []   # (block index, item)
        for bi, blk in enumerate(self.blocks):
            cur = None
            for l in blk:
                if cur and cont(cur['lines'][-1].text, l.text, cur['lines'][0].text):
                    cur['lines'].append(l)
                else:
                    cur = {'lines': [l], 'new': None, 'block': bi, 'codes': list(l.codes)}
                    self.items.append(cur)
                    continue
                cur['codes'] += l.codes
        self.log = []

    # -------- the text of an item, with its variables renumbered into one list
    def item_text(self, it):
        if it['new'] is not None:
            return it['new']
        out, k = '', 0
        for l in it['lines']:
            k0 = k
            t = VAR_RE.sub(lambda m: '\x10%d\x11' % (int(m.group(1)) + k0), l.text)
            k += len(l.codes)
            if not out:
                out = t
            elif re.search(r'[A-Za-z]-$', out) and re.match(r'\s*[a-z]', t):
                out = out + t.lstrip()          # a word broken at its own hyphen: re- / arrested
            else:
                out = out + '\n' + t
        return out

    def words(self, texts):
        t = ' '.join(texts)
        t = re.sub(r'([A-Za-z])-\s+([a-z])', r'\1-\2', t)
        return re.sub(r'\s+', ' ', plain(t)).strip()

    def check(self, placed):
        """every word of the changed page is on its new page(s), in order, and nothing else"""
        exp = self.words([self.item_text(it) for it in self.items])
        got = self.words([(t if isinstance(t, str) else t.text) for page in placed for it, t, y, tm in page])
        if exp != got:
            import difflib
            a, b = exp.split(' '), got.split(' ')
            d = [x for x in difflib.ndiff(a, b) if x[:1] in '+-']
            raise ValueError('the words changed in layout: %s' % d[:12])

    def reflow_all(self):
        # a sentence split across two colours (no gap between) is joined, in the first colour, in prose pages
        if LOOSE[0]:
            i = 0
            while i + 1 < len(self.items):
                a_, b_ = self.items[i], self.items[i + 1]
                ta, tb = plain(self.item_text(a_)).rstrip(), plain(self.item_text(b_)).lstrip()
                if (b_['block'] != a_['block'] and b_['lines'][0].y - a_['lines'][-1].y <= self.step + 1 and ta and tb
                        and not (ta[-1] in '.;:!?' or ta.endswith(('.)', '."'))) and re.match(r'[a-z0-9(]', tb)
                        and not TABLE.search(ta + ' ' + tb)):
                    a_['new'] = self.item_text(a_) + '\n' + VAR_RE.sub(lambda m: '\x10%d\x11' % (int(m.group(1)) + len(a_['codes'])), self.item_text(b_))
                    a_['codes'] = a_['codes'] + b_['codes']
                    a_['lines'] = a_['lines'] + b_['lines']
                    del self.items[i + 1]
                    self.log.append('joined a sentence across colours')
                    continue
                i += 1
        for it in self.items:
            if it['new'] is None and not (len(it['lines']) == 1 and TABLE.search(plain(it['lines'][0].text))):
                it['new'] = self.item_text(it)

    def apply(self, old, new):
        """replace old by new in one item, or across neighbouring items (they merge).  A number in old may stand
        for a variable the page computes (the dump showed its value): the variable is kept in new."""
        old, new = norm(old), norm(new)
        toks = old.split()
        parts, nums = [], []
        for w in toks:
            m_ = re.fullmatch(r'(\D*?)(\d[\d,]*)(\D*)', w)
            if m_ and m_.group(2):
                nums.append(m_.group(2))
                parts.append(re.escape(m_.group(1)) + '(%s|\x10\\d+\x11)' % re.escape(m_.group(2)) + re.escape(m_.group(3)))
            else:
                parts.append(re.escape(w))
        pat = re.compile(r'\s+'.join(parts))

        def fill(m):
            out = new
            for gi, num in enumerate(nums, start=1):
                got = m.group(gi)
                if got != num:
                    out = out.replace(num, got, 1)
            return out
        texts = [self.item_text(it) for it in self.items]
        for i, t in enumerate(texts):
            m = pat.search(t)
            if m:
                self.items[i]['new'] = t[:m.start()] + fill(m) + t[m.end():]
                return 'item %d' % i
        for i in range(len(self.items)):
            for j in range(i + 1, min(i + 6, len(self.items))):
                a_, b_ = self.items[j - 1], self.items[j]
                if b_['block'] != a_['block'] and b_['lines'][0].y - a_['lines'][-1].y > self.step + 1:
                    break                      # only neighbouring lines: no gap between them
                t = '\n'.join(texts[i:j + 1])
                m = pat.search(t)
                if not m:
                    continue
                if m.start() >= len(texts[i]) or m.end() <= len('\n'.join(texts[i:j])):
                    continue          # it does not start in item i and end in item j
                merged = t[:m.start()] + fill(m) + t[m.end():]
                first = self.items[i]
                codes = []
                for it in self.items[i:j + 1]:
                    codes += it['codes']
                first['new'] = merged
                first['codes'] = codes
                first['lines'] = sum((it['lines'] for it in self.items[i:j + 1]), [])
                del self.items[i + 1:j + 1]
                self.log.append('merged items %d..%d' % (i, j))
                return 'items %d-%d' % (i, j)
        raise KeyError('not found on the page: %r' % old)

    def layout(self, y0=None):
        """-> list of (block index, item, [line texts]) with every item's lines"""
        out = []
        for it in self.items:
            if it['new'] is None:
                lt = list(it['lines'])
            else:
                first = it['lines'][0]
                ind0 = ' ' * ind(first.text)
                ind1 = ' ' * ind(it['lines'][1].text) if len(it['lines']) > 1 else ind0
                avail = self.maxw - 0
                varw = self.varw
                lt = wrap(it['new'], avail, self.font, ind0, ind1, varw)
            out.append((it['block'], it, lt))
        return out

    def place(self, ymax, y_first=None):
        """y for every line; when the page would pass ymax it is split, at the item boundary (a block boundary if one
        is near) that best balances the pages. -> list of pages, each a list of (item, line, y, template Line)"""
        lay = self.layout()
        gap = {}
        for bi in range(1, len(self.blocks)):
            gap[bi] = self.blocks[bi][0].y - self.blocks[bi - 1][-1].y
        y0 = self.blocks[0][0].y if y_first is None else y_first

        def run(seq):
            page, y, prevb = [], y0, None
            for bi, it, lt in seq:
                yy = y0 if prevb is None else (y + self.step if bi == prevb else y + gap[bi])
                for k, t in enumerate(lt):
                    page.append((it, t, yy + k * self.step, it['lines'][0]))
                y, prevb = yy + (len(lt) - 1) * self.step, bi
            return page

        whole = run(lay)
        if not whole or whole[-1][2] <= ymax:
            return [whole]
        # split: try every cut between items; both parts must fit (recursively for the second)
        best = None
        for c in range(1, len(lay)):
            a, b = run(lay[:c]), run(lay[c:])
            if a[-1][2] > ymax:
                break
            rest = [b] if b[-1][2] <= ymax else None
            if rest is None:
                continue
            na, nb = len(a), len(b)
            score = abs(na - nb) - (2 if lay[c][0] != lay[c - 1][0] else 0)   # prefer a block boundary
            if best is None or score < best[0]:
                best = (score, [a, b])
        if best:
            return best[1]
        # three or more pages: fill greedily
        pages, start = [], 0
        while start < len(lay):
            c = start + 1
            while c < len(lay) and run(lay[start:c + 1])[-1][2] <= ymax:
                c += 1
            part = run(lay[start:c])
            if part[-1][2] > ymax:
                raise ValueError('one item is taller than a page: %r' % lay[start][2])
            pages.append(part)
            start = c
        return pages

    def emit(self, page):
        """code lines for one placed page"""
        out = []
        for it, t, y, tmpl in page:
            if not isinstance(t, str):
                out.append(t.code(y))      # the original line, its code kept, y changed
            else:
                expr = marked_to_code(t, it['codes'])
                out.append(tmpl.code(y, expr))
        return out

    def width_report(self, page):
        bad = []
        for it, t, y, tmpl in page:
            if not isinstance(t, str):
                continue
            w = W(t, self.font, self.varw)
            if w > self.maxw:
                bad.append((w, t))
        return bad


def if_blocks(L, a, b, var):
    """'IF var == k THEN' ... its END; inside lines a..b (1-based) -> {k: (first line, last line)}"""
    out = {}
    i = a - 1
    while i < b:
        m = re.match(r'^(\s*)IF %s == (\d+) THEN\s*$' % re.escape(var), L[i])
        if m:
            ind0 = m.group(1)
            j = i + 1
            while not re.match(r'^%sEND;' % re.escape(ind0), L[j]):
                j += 1
            out[int(m.group(2))] = (i + 1, j + 1)
            i = j
        i += 1
    return out


def text_of(page_lines):
    return [t if isinstance(t, str) else t.text for _, t, _, _ in page_lines]
