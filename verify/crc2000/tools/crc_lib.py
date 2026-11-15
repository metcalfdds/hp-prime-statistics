# crc_lib.py : shared pieces for checking the tables of
#   Zwillinger & Kokoska, CRC Standard Probability and Statistics Tables and Formulae (2000)
# against values worked out afresh.  The text layer of the PDF (pdftotext -layout) is in work/all.txt,
# one page per form feed; page numbers here are PDF page numbers.
#
# Verdict for one printed cell:
#   ok    printed = the true value rounded to the decimals printed
#   last  off by one unit in the last place printed
#   DIFF  off by more than that
import io, re, json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, '..', 'work')
pages = io.open(os.path.join(W, 'all.txt'), encoding='utf-8', errors='replace').read().split('\f')

def L(p):
    return pages[p - 1].split('\n')

TOK = re.compile(r'\S+')
def toks(line):
    return [(m.start(), m.end(), m.group()) for m in TOK.finditer(line)]

def clean(s):
    return s.replace('−', '-').replace('–', '-').replace('—', '-')

NUM = re.compile(r'^-?(\d+\.?\d*|\.\d+)$')
def isnum(s):
    return bool(NUM.match(clean(s)))

def dec(s):
    s = clean(s)
    return len(s.split('.')[1]) if '.' in s else 0

def verdict(s, true):
    s = clean(s)
    d = dec(s); v = float(s); u = 10.0 ** -d; diff = abs(v - true)
    if diff <= 0.5 * u * (1 + 1e-7) + 1e-13: return 'ok'
    if diff <= 1.5 * u * (1 + 1e-7) + 1e-13: return 'last'
    return 'DIFF'

class Tally:
    def __init__(self, name, title):
        self.name = name; self.title = title
        self.c = {'ok': 0, 'last': 0, 'DIFF': 0}; self.flag = []; self.notes = []; self.pages = set()
    def add(self, page, row, col, printed, true):
        v = verdict(printed, true); self.c[v] += 1; self.pages.add(page)
        if v != 'ok': self.flag.append([page, str(row), str(col), printed, float(true), v])
        return v
    def note(self, s): self.notes.append(s)
    def done(self, show=6):
        n = sum(self.c.values())
        pg = sorted(self.pages)
        print('%-22s pp.%s-%s cells %5d  ok %5d  last %4d  DIFF %4d' % (
            self.name, pg[0] if pg else '?', pg[-1] if pg else '?', n, self.c['ok'], self.c['last'], self.c['DIFF']))
        d = [f for f in self.flag if f[5] == 'DIFF']
        for f in d[:show]:
            print('     DIFF p%d row %s col %s printed %s true %.7g' % (f[0], f[1], f[2], f[3], f[4]))
        if len(d) > show: print('     ... and %d more DIFF' % (len(d) - show))
        for s in self.notes[:4]: print('     note: ' + s[:150])
        json.dump({'name': self.name, 'title': self.title, 'pages': pg, 'counts': self.c, 'flag': self.flag,
                   'notes': self.notes}, open(os.path.join(W, 'res_%s.json' % self.name), 'w'), indent=0)

def centers(tk):
    return [(a + b) / 2.0 for a, b, t in tk]

def assign(tk, cols):
    """Map tokens to column indexes by nearest centre (cols = list of centres).  Returns list of (colindex, text)."""
    out = []
    for a, b, t in tk:
        c = (a + b) / 2.0
        j = min(range(len(cols)), key=lambda i: abs(cols[i] - c))
        out.append((j, t))
    return out

def colcenters(rows, ncol):
    """Mean centre of each column over the rows that have every column."""
    full = [r for r in rows if len(r) == ncol]
    if not full: return None
    return [sum((r[i][0] + r[i][1]) / 2.0 for r in full) / len(full) for i in range(ncol)]
