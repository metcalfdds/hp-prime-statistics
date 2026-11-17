# -*- coding: utf-8 -*-
"""screen_text_v1.py [--walk DIR] [--loose] [--quiet] PROGRAM.txt [...]      (Round 17, 17 Nov 2026)

THE BOOK'S TWO RULES FOR A STATISTIC'S LETTER, AS FAR AS A SCREEN CAN FOLLOW THEM.  Roger, 17 Nov 2026: "The p-value and
t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses".
A calculator's screen has no italics, so a program's text keeps the other half of each rule:

  (a) an expression like n - 1 stands in parentheses of its own:  df = (n - 1),  (k - 1) df,  df = (N1 + N2 - 2);
  (b) a hyphen joins a statistic's letter to its noun:  t-test, z-test, F-test, p-value, t-curve, t-interval, t-table,
      F-ratio, q-distribution, z-values ...   Before "critical" there is none ("t critical value", "t crit");
  (c) the p of p-value is a small letter, at the start of a line or a title too ("p-value from q"), as the book writes
      it and as ChiTable, EpiStats and AgreeLab always did.

WHAT IS READ.  Every quoted string of the program's code (comments are not read; they are for a programmer and are not on
the screen), with CHAR(n) joins closed ("df = N"+CHAR(8321)+" - 1" is one text), with the program's own symbols put in
(a name given one value in the whole program, a CHAR(n) or a text of at most three characters, such as tdMin := CHAR(8722):
"... = n " + tdMin + " 1." is read as the screen shows it) and the pieces of one line read together; inside a #PYTHON
block, strings in either kind of quote.  With --walk DIR, also every text that the generic walk of
tools/text_overlap_v1.py drew, so that a line put together from variables is seen as the screen shows it: DIR/<stem>.json,
the walk as its --json writes it, or DIR/<stem>.texts.json, the list of the distinct texts of such a walk (a walk can be
hundreds of megabytes; verify/round17/drawn_texts_r17.py writes the lists).

WHAT IS LEFT ALONE is in ALLOW below, each entry with its reason (the Prime's own names, as the Prime spells them; an
expression that is not a count of degrees of freedom).  A place that is not allowed is printed and the exit code is 1.
--loose also lists the candidates that rule (a) passes over (x-1 with no spaces, a label such as D1-9), for a reading by
eye; they do not change the exit code.

  program  line-or-"drawn"  (rule) | text
"""
import collections, io, json, os, re, sys

args = sys.argv[1:]
walk = None
loose = quiet = False
while args and args[0].startswith('--'):
    if args[0] == '--walk':
        walk = args[1]; args = args[2:]
    elif args[0] == '--loose':
        loose = True; args = args[1:]
    elif args[0] == '--quiet':
        quiet = True; args = args[1:]
    else:
        sys.exit('unknown option ' + args[0])
if not args:
    sys.exit(__doc__)

SUB = u'\u2080-\u2089'                                   # subscript digits
MINUS = u'\\-\u2212\u2013'                               # hyphen-minus, minus sign, en dash
# (a) letters (with a subscript, and joined by +), a minus, a whole number, and at most one more "- letter"
A = re.compile(u'(?<![A-Za-z0-9_.^])((?:[A-Za-z\u03bd][%s]?\\s?\\+\\s?)*[A-Za-z\u03bd][%s]?)\\s?[%s]\\s?(\\d+)'
               u'(?:\\s?[%s]\\s?[a-z](?![a-z]))?(?![A-Za-z0-9.,]*\\d)(?![A-Za-z%%%s])' % (SUB, SUB, MINUS, MINUS, SUB))
# (b) the book's own list (pagecheck/stat_terms_guard_v1.py of the book's source), without "critical"
NOUN = (r'(?:values?|tests?|testing|distributions?|statistics?|scores?|tables?|curves?|intervals?|ratios?|procedures?|'
        r'methods?|density|densities|surfaces?|quantiles?|multipliers?|tails?|max)')
B = re.compile(u'(?<![A-Za-z0-9\u2019\'\u2011-])([ptzFUHWLQqrd])[ \u00a0](' + NOUN + r')\b')
C = re.compile(u'(?<![A-Za-z0-9])P[-\u2011]values?\\b')
B_CAP = re.compile(u'(?<![A-Za-z0-9\u2019\'\u2011-])([PTZ])[ \u00a0](' + NOUN + r')\b')      # P value, T test, Z score

# (program or '*', regular expression on the text around the place, why it is left alone)
ALLOW = [
    ('*', r'Linear t test', "the Prime's own name of its Inference method, as the Prime spells it"),
    ('Norm3', r'both P values', 'two probabilities, each written P(...) on the page: values of P, not a p-value'),
]


def find(text, tell_loose=False):
    out = []
    for m in A.finditer(text):
        a, b = m.start(), m.end()
        before, after = text[:a].rstrip(' '), text[b:].lstrip(' ')
        frag = text[a:b]
        ctx = text[max(0, a - 40):b + 26]
        if before.endswith('(') and after.startswith(')'):
            continue                                                    # in parentheses of its own
        if re.search(u'[A-Za-z0-9%s]$' % SUB, text[:a]):
            continue                                                    # the tail of a word or of a number
        if after.startswith('/'):
            continue                                                    # n - 1/2, K - 1/C: a fraction is taken away
        if re.match(u'^[A-Za-z\u03bd][%s]?[%s] \\d' % (SUB, MINUS), frag):
            continue                                                    # "T\u2212 10": a name that ends in a sign, and a count
        if (' ' not in frag and u'\u2212' not in frag and not re.search(u'(df|=|\u03bd|,|of)\\s*$', before)
                and not re.match(r'df\b', after)):
            if tell_loose:
                out.append(('a?', frag, ctx))                           # x-1, D1-9: a label, read by eye with --loose
            continue
        out.append(('a', frag, ctx))
    for m in B.finditer(text):
        out.append(('b', m.group(0), text[max(0, m.start() - 40):m.end() + 26]))
    for m in B_CAP.finditer(text):
        out.append(('b', m.group(0), text[max(0, m.start() - 40):m.end() + 26]))
    for m in C.finditer(text):
        out.append(('c', m.group(0), text[max(0, m.start() - 40):m.end() + 26]))
    return out


def allowed(stem, ctx):
    for prog, rx, why in ALLOW:
        if (prog == '*' or stem.startswith(prog + '_')) and re.search(rx, ctx):
            return why
    return None


def symbols_of(src):
    """{name: text} for every name that is given a value once in the whole program, and that value a short constant:
    CHAR(n), a text of at most three characters, or such pieces joined by +."""
    piece = r'(?:CHAR\(\d+\)|"[^"\\]{0,3}")'
    rx = re.compile(r'(?<![A-Za-z0-9_.])([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*(' + piece + r'(?:\s*\+\s*' + piece + r')*)\s*;')
    count = collections.Counter(re.findall(r'(?<![A-Za-z0-9_.])([A-Za-z_][A-Za-z0-9_]*)\s*:=', src))
    count.update(re.findall(r'(?:\u25b6|=>)\s*([A-Za-z_][A-Za-z0-9_]*)', src))            # the store arrow
    sym = {}
    for name, val in rx.findall(src):
        if count[name] != 1:
            continue
        sym[name] = ''.join(chr(int(m[5:-1])) if m.startswith('CHAR') else m[1:-1] for m in re.findall(piece, val))
    return sym


def strings_of(src):
    """(line number, [texts]) for each line of code that holds a string; PPL outside #PYTHON blocks, Python inside."""
    py = False
    sym = symbols_of(src)
    names = sorted(sym, key=len, reverse=True)
    symrx = re.compile(r'(?<![A-Za-z0-9_."])(' + '|'.join(re.escape(n) for n in names) + r')(?![A-Za-z0-9_("])') if names else None
    for n, line in enumerate(src.split('\n'), 1):
        s = line.strip()
        if s.upper().startswith('#PYTHON'):
            py = True; continue
        if py and s.upper().startswith('#END'):
            py = False; continue
        pieces = []
        if py:
            i = 0
            while i < len(line):
                ch = line[i]
                if ch == '#':
                    break
                if ch in '"\'':
                    j = i + 1
                    while j < len(line) and line[j] != ch:
                        j += 2 if line[j] == '\\' else 1
                    pieces.append(line[i + 1:j]); i = j + 1
                else:
                    i += 1
        else:
            out = []; q = False; i = 0
            while i < len(line):
                ch = line[i]
                if ch == '"':
                    q = not q
                if not q and line[i:i + 2] == '//':
                    break
                out.append(ch); i += 1
            code = ''.join(out)
            if '"' not in code:
                continue
            if symrx and not re.search(r':=\s*(?:CHAR\(\d+\)|"[^"]{0,3}")', code):
                # a symbol outside the quotes becomes its text, so that the joins below close over it
                parts = re.split(r'("(?:[^"\\]|\\.)*")', code)
                code = ''.join(p if i % 2 else symrx.sub(lambda m: '"' + sym[m.group(1)] + '"', p) for i, p in enumerate(parts))
                code = re.sub(r'"\s*\+\s*"', '', code)
            code = re.sub(r'"\s*\+\s*CHAR\((\d+)\)\s*\+\s*"', lambda m: chr(int(m.group(1))), code)
            code = re.sub(r'CHAR\((\d+)\)\s*\+\s*"', lambda m: '"' + chr(int(m.group(1))), code)
            code = re.sub(r'"\s*\+\s*CHAR\((\d+)\)', lambda m: chr(int(m.group(1))) + '"', code)
            pieces = re.findall(r'"((?:[^"\\]|\\.)*)"', code)
        if pieces:
            yield n, sorted(set(pieces + [''.join(pieces)]))


rows = []; left = []; maybe = []
nstr = collections.Counter(); ndrawn = collections.Counter()
for path in args:
    stem = os.path.basename(path)[:-4]; seen = set()
    for n, texts in strings_of(io.open(path, encoding='utf-8').read()):
        nstr[stem] += len(texts) - 1 if len(texts) > 1 else 1
        for text in texts:
            for kind, frag, ctx in find(text, loose):
                key = (kind, frag, ctx[:30])
                if key in seen:
                    continue
                seen.add(key)
                why = allowed(stem, ctx)
                (maybe if kind == 'a?' else left if why else rows).append((stem, '%5d' % n, kind, ctx, why))
    if walk:
        p = os.path.join(walk, stem + '.json'); pt = os.path.join(walk, stem + '.texts.json'); texts = set()
        if os.path.exists(p):                                  # the walk itself
            d = json.load(open(p))
            for raw in d['raw'].values():
                for scr in raw['screens'].values():
                    for it in scr[2]['items']:
                        if 'text' in it:
                            texts.add(str(it['text']))
        elif os.path.exists(pt):                               # the list of its distinct texts
            texts = set(json.load(io.open(pt, encoding='utf-8')))
        else:
            sys.exit('no walk for %s in %s' % (stem, walk))
        ndrawn[stem] = len(texts)
        for text in sorted(texts):
            for kind, frag, ctx in find(text, loose):
                key = ('drawn', kind, frag, ctx[:30])
                if key in seen:
                    continue
                seen.add(key)
                why = allowed(stem, ctx)
                (maybe if kind == 'a?' else left if why else rows).append((stem, 'drawn', kind, ctx, why))

if not quiet:
    for r in rows:
        print('%-22s %s (%s) | %s' % (r[0][:22], r[1], r[2], r[3]))
    for r in left:
        print('%-22s %s (%s) | %s   [left alone: %s]' % (r[0][:22], r[1], r[2], r[3], r[4]))
    for r in maybe:
        print('%-22s %s (%s) | %s' % (r[0][:22], r[1], r[2], r[3]))
per = collections.Counter(r[0] for r in rows)
print('%d programs, %d strings read%s; places against the rules: %d in %d programs%s; left alone: %d%s' % (
    len(args), sum(nstr.values()), ', %d drawn texts' % sum(ndrawn.values()) if walk else '', len(rows), len(per),
    (' ' + str(dict(per))) if per else '', len(left), ('; passed over by rule (a), listed for the eye: %d' % len(maybe)) if loose else ''))
sys.exit(1 if rows else 0)
