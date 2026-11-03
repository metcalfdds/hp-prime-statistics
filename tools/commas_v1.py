#!/usr/bin/env python3
"""commas_v1.py -- round 5 (Nov 2026): commas in big numbers, the same way in every program of the fleet.

Roger, 2 Nov 2026: "always put comma delimiters in big numbers".  STRING never groups digits (Virtual Calculator,
2 Nov 2026: STRING(1234567) is "1234567" even with Home's digit grouping on), so each program gets its own helper,
<pfx>Cm(text): a comma every three digits in each run of four or more digits that does not follow a decimal point.
It is idempotent ("1,000" has no run of four), leaves decimals and exponents alone, and was run on the Virtual
Calculator in CommaProbe beta 1 (12 of 12 as expected).

What the script does to a program, all by exact rules (CONFIG in commas_config_r5.py says which routines are which):
  1. the helper, defined before the first routine;
  2. every call of STRING or of a routine listed as a number formatter (cfg 'fmt') is wrapped where it is made,
     <pfx>Cm(STRING(...)), so the text is grouped before it is measured or drawn, unless it sits inside (at any depth) a call
     that reads the text rather than shows it -- EXPR, CAS, DIM, INSTRING, MID, LEFT, RIGHT, ASC, SIZE, POS, a
     CAS helper of the program, or another STRING -- or in a statement that calls the CAS or builds text that
     reaches it (within a routine that calls EXPR, CAS or the program's CAS helper: the variables in the call, and
     those they are built from); cfg 'skip' names routines left alone (text helpers, the CAS's own helpers), and
     nothing inside a formatter is wrapped (its result is, where it is called);
  3. cfg 'edits': exact replacements (help text, width measures that count a comma as narrow, and the like);
  4. the version: the title line, every string literal that names the version, and a "what changed" block.
Usage: python3 commas_v1.py NAME IN.txt OUT.txt      (NAME as in commas_config_r5.CONFIG)
Prints one line: what it wrapped.
"""
import os
import re
import sys
from commas_config_r5 import CONFIG, HISTORY, DATE

NAME, SRC, DST = sys.argv[1:4]
C = CONFIG[NAME]
text = open(SRC, encoding='utf-8').read()

HEAD = re.compile(r'^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z_]\w*)\(([^()]*)\)\s*(?://.*)?$')
READERS = {'EXPR', 'CAS', 'DIM', 'INSTRING', 'MID', 'LEFT', 'RIGHT', 'ASC', 'SIZE', 'POS', 'STRING', 'REPLACE',
           'UPPER', 'LOWER', 'NUMBER'}


def segments(t):
    """kinds per character: 'c' code, 's' inside a string literal (quotes included), 'm' comment"""
    k = ['c'] * len(t)
    i, n = 0, len(t)
    while i < n:
        ch = t[i]
        if ch == '"':
            j = i + 1
            while j < n and t[j] != '"' and t[j] != '\n':
                j += 1
            for q in range(i, min(j + 1, n)):
                k[q] = 's'
            i = j + 1
        elif ch == '/' and i + 1 < n and t[i + 1] == '/':
            j = t.find('\n', i)
            j = n if j < 0 else j
            for q in range(i, j):
                k[q] = 'm'
            i = j
        else:
            i += 1
    return k


def routines(t):
    """[(name, start offset, end offset)] by the header lines (a name(args) line followed by BEGIN)"""
    lines = t.split('\n')
    offs, o = [], 0
    for ln in lines:
        offs.append(o)
        o += len(ln) + 1
    heads = []
    for i, ln in enumerate(lines):
        m = HEAD.match(ln)
        if m and i + 1 < len(lines) and lines[i + 1].strip().upper().startswith('BEGIN'):
            heads.append((m.group(1), offs[i]))
    out = []
    for q, (nm, st) in enumerate(heads):
        en = heads[q + 1][1] if q + 1 < len(heads) else len(t)
        out.append((nm, st, en))
    return out


def match_close(t, k, i):
    """t[i] == '(' -> index of its ')' (code characters only)"""
    d = 0
    for j in range(i, len(t)):
        if k[j] != 'c':
            continue
        if t[j] in '([{':
            d += 1
        elif t[j] in ')]}':
            d -= 1
            if d == 0:
                return j
    raise ValueError('no close at %d' % i)


def ancestors(t, k, i, lo):
    """names of the calls whose parentheses enclose position i, nearest first (back to offset lo)"""
    names, d = [], 0
    for j in range(i - 1, lo - 1, -1):
        if k[j] != 'c':
            continue
        if t[j] in ')]}':
            d += 1
        elif t[j] in '([{':
            if d == 0:
                m = re.search(r'([A-Za-z_]\w*)\s*$', t[lo:j]) if t[j] == '(' else None
                names.append(m.group(1) if m else t[j])
            else:
                d -= 1
        elif t[j] == ';' and d == 0:
            break
    return names


k = segments(text)
rts = routines(text)
fmt = set(C.get('fmt', []))
calls_cas = re.compile(r'\b(EXPR|CAS)\s*\(|\bCAS\.|\b(%s)\s*\(' % '|'.join(C.get('casfam') or ['_none_']))
skip = set(C.get('skip', []))
readers = READERS | set(C.get('casfam', [])) | set(C.get('readers', []))


def code_only(a, b):
    return ''.join(ch if kk == 'c' else ('"' if ch == '"' else ' ') for ch, kk in zip(text[a:b], k[a:b]))


# routines that call the CAS: the variables whose text reaches it (in its argument, or assigned from such, and so on).
# A routine whose own parameter reaches the CAS this way reads CAS text too (StatDist's st_FmAsk, CentralLimit's
# cltCasNum): a call of it is a CAS call, found the same way, until no more are found.
def compute_casv(cre, pos=None):
    out, reach = {}, {}
    pos = pos or {}
    for nm, st, en in rts:
        body = code_only(st, en)
        hdr_end = body.find('\n') + 1
        if not cre.search(body[hdr_end:]):
            continue
        stm = [x for x in re.split(r';', body[hdr_end:])]
        seed = set()
        for x in stm:
            for m in cre.finditer(x):
                # the call's own argument, to its closing bracket (not the rest of the statement: in
                # "ABS(EXPR(mlNum) - mlV)" only mlNum reaches EXPR)
                d_, j_ = 0, m.end() - 1
                while j_ < len(x) and x[j_] != '(':
                    j_ += 1
                e_ = j_
                for e_ in range(j_, len(x)):
                    if x[e_] == '(':
                        d_ += 1
                    elif x[e_] == ')':
                        d_ -= 1
                        if d_ == 0:
                            break
                arg_ = x[j_ + 1:e_]
                rname = m.group(2) if m.lastindex and m.lastindex >= 2 else None
                if rname in pos:
                    # a routine that reads CAS text: only the arguments its CAS text comes from
                    parts, dd, s0 = [], 0, 0
                    for q_, ch in enumerate(arg_):
                        if ch in '([{':
                            dd += 1
                        elif ch in ')]}':
                            dd -= 1
                        elif ch == ',' and dd == 0:
                            parts.append(arg_[s0:q_])
                            s0 = q_ + 1
                    parts.append(arg_[s0:])
                    arg_ = ' '.join(parts[i_] for i_ in pos[rname] if i_ < len(parts))
                seed |= set(re.findall(r'\b([A-Za-z_]\w*)\b', arg_))
        assigned = {}
        for x in stm:
            m = re.search(r'\b([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=(.*)$', x, re.S)
            if m:
                assigned.setdefault(m.group(1), []).append(m.group(2))
        cv = {v for v in seed if v in assigned}
        grew = True
        while grew:
            grew = False
            for v in list(cv):
                for rhs in assigned[v]:
                    for w in re.findall(r'\b([A-Za-z_]\w*)\b', rhs):
                        if w in assigned and w not in cv:
                            cv.add(w)
                            grew = True
        out[nm] = cv
        hm = HEAD.match(text[st:text.index('\n', st)])
        ps = [x.strip() for x in hm.group(2).split(',')] if hm and hm.group(2).strip() else []
        used = set(seed)
        for v in cv:
            for rhs in assigned[v]:
                used |= set(re.findall(r'\b([A-Za-z_]\w*)\b', rhs))
        reach[nm] = [i_ for i_, q in enumerate(ps) if q in used]
    return out, reach


READER_POS = {}


def cas_readers():
    rd = set(C.get('casfam', []))
    while True:
        cre = re.compile(r'\b(EXPR|CAS)\s*\(|\bCAS\.|\b(%s)\s*\(' % '|'.join(sorted(rd) or ['_none_']))
        _cv, reach = compute_casv(cre, READER_POS)
        new = {nm for nm, ps in reach.items() if ps and nm != C['helper']} - rd
        for nm in new:
            READER_POS[nm] = reach[nm]
        if not new:
            return rd, cre
        rd |= new


CAS_READERS, calls_cas = cas_readers()
CASV = compute_casv(calls_cas, READER_POS)[0]
GCASV = set()
print('cas readers: %s' % sorted(CAS_READERS - set(C.get('casfam', []))))


# routines whose text reaches the CAS: called in a statement that calls it, or in building a variable that reaches
# it, and every routine those call (bu_Frac's "2731/1000" in BurrLab's moment text; grouped, it was "2,731/1,000",
# the CAS refused it and the page fell back to decimals).  They are left alone, as 'skip' routines are, and where
# their text is drawn, the draw site groups it.
def casfeed():
    names = {r[0] for r in rts}
    # a routine that reads CAS text (cas_readers) takes it in; what it calls does not build the caller's text
    rd = set(CAS_READERS) | set(C.get('casfam', []))
    callre = re.compile(r'(?<![\w.])([A-Za-z_]\w*)\s*\(')
    feed = set()
    for nm, st, en in rts:
        if nm not in CASV:
            continue
        body = code_only(st, en)
        hdr_end = body.find('\n') + 1
        for x in re.split(r';', body[hdr_end:]):
            m = re.search(r'\b([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=', x)
            if calls_cas.search(x) or (m and m.group(1) in CASV[nm]):
                _add = {w for w in callre.findall(x) if w in names and w not in rd}
                if os.environ.get('COMMAS_DEBUG') and _add - feed:
                    print('DEBUG feed', nm, sorted(_add - feed), ' '.join(x.split())[:120])
                feed |= _add
    grew = True
    while grew:
        grew = False
        for nm, st, en in rts:
            if nm in feed:
                for w in callre.findall(code_only(st, en)[1:]):
                    if w in names and w not in feed and w != nm and w not in rd:
                        if os.environ.get('COMMAS_DEBUG'):
                            print('DEBUG feed via', nm, w)
                        feed.add(w)
                        grew = True
    return feed - set(C.get('casfam', [])) - {C['helper']} - set(C.get('feed_no', []))


CASFEED = casfeed()
skip |= CASFEED


KEYRE = re.compile(r'(Key|Ky)(?![a-z])|^ky[A-Z]')


def global_casv():
    out = set()
    for nm, st, en in rts:
        if nm not in CASV:
            continue
        body = code_only(st, en)
        loc = set()
        for m in re.finditer(r'\bLOCAL\s+([^;]*);', body):
            loc |= {w.strip().split(':=')[0].strip() for w in m.group(1).split(',')}
        hm = HEAD.match(text[st:text.index('\n', st)])
        loc |= {x.strip() for x in hm.group(2).split(',')} if hm and hm.group(2).strip() else set()
        out |= {v for v in CASV[nm] if v not in loc}
    # and the globals a routine that builds CAS text puts into it (StatDist's stFmXR, in st_FmSub's "subst(...)")
    for nm, st, en in rts:
        if nm not in CASFEED:
            continue
        body = code_only(st, en)
        loc = set()
        for m in re.finditer(r'\bLOCAL\s+([^;]*);', body):
            loc |= {w.strip().split(':=')[0].strip() for w in m.group(1).split(',')}
        hm = HEAD.match(text[st:text.index('\n', st)])
        loc |= {x.strip() for x in hm.group(2).split(',')} if hm and hm.group(2).strip() else set()
        out |= {w for w in re.findall(r'(?<![\w.])([A-Za-z_]\w*)(?!\s*\()', body[body.find('\n'):])
                if w not in loc and w in ASSIGN_ANY}
    return out


def gcas_statement(nm, st, p):
    """1 if the statement holding offset p assigns a global variable whose text reaches the CAS somewhere"""
    a = max(text.rfind(';', st, p) + 1, text.index('\n', st) + 1)   # within the routine, after its header
    b = text.find(';', p)
    x = code_only(a, b if b > 0 else len(text))
    m = re.search(r'\b([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=', x)
    return 1 if m and m.group(1) in GCASV else 0


ASSIGN_ANY = set(re.findall(r'\b([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=', code_only(0, len(text))))
GCASV = global_casv()
print('global CAS variables: %s' % sorted(GCASV)[:12])


def key_statement(nm, st, p):
    """1 if the statement holding offset p builds a key (a cache key: "kyS", "cfKey", "xbKy"), or sits in a routine
    that makes one ("gbPsKey"): a key never gets commas, since "1,234,567" in a key joined by commas could be
    (1, 234567) or (1234, 567)"""
    if nm in C.get('key_funcs', []):
        return 1
    a = max(text.rfind(';', st, p) + 1, text.index('\n', st) + 1)   # within the routine, after its header
    b = text.find(';', p)
    x = code_only(a, b if b > 0 else len(text))
    m = re.search(r'\b([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=', x)
    return 1 if m and (KEYRE.search(m.group(1)) or m.group(1) in C.get('key_vars', [])) else 0


def cas_statement(nm, st, p):
    """1 if the statement holding offset p calls the CAS or builds text that reaches it"""
    a = max(text.rfind(';', st, p) + 1, text.index('\n', st) + 1)   # within the routine, after its header
    b = text.find(';', p)
    x = code_only(a, b if b > 0 else len(text))
    if calls_cas.search(x):
        return 1
    m = re.search(r'\b([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=', x)
    return 1 if m and m.group(1) in CASV[nm] else 0

# ---- pass 0: numbers written into the program's own text ("Drop 1000 balls", "at most 5000 values") get their
# commas, in the string literal itself.  Never a year: a run of four digits from 1500 to 2099 is left alone unless
# cfg 'lit_yes' names its context ("N > 2000"); cfg 'lit_no' names other runs to leave alone (an NCJ number, a page);
# nor text the CAS or EXPR reads, a reader's argument ("0123456789" in INSTRING), or a skipped routine's text.
def group_digits(d):
    q = len(d) % 3 or 3
    return d[:q] + ''.join(',' + d[i:i + 3] for i in range(q, len(d), 3))


lit_edits = []
LY, LN = C.get('lit_yes', []), C.get('lit_no', []) + ['0123456789', 'NCJ-', 'CRCJ ', ':1456']
for nm, st, en in rts:
    if nm in skip or nm in fmt:
        continue
    for m in re.finditer(r'"[^"\n]*"', text[st:en]):
        a, b = st + m.start(), st + m.end()
        if k[a] != 's' or (a > 0 and k[a - 1] == 's'):
            continue
        lit = text[a:b]
        if not re.search(r'(?<![\d.,])\d{4,}(?!\d)', lit):
            continue
        anc = ancestors(text, k, a, st)
        if any(x in READERS | set(C.get('casfam', [])) for x in anc):
            continue
        if (nm in CASV and cas_statement(nm, st, a)) or key_statement(nm, st, a) or gcas_statement(nm, st, a):
            continue

        def sub(mm, lit=lit):
            d = mm.group(0)
            ctx = lit[max(0, mm.start() - 20):mm.end() + 20]
            if any(x in ctx for x in LN):
                return d
            if len(d) == 4 and 1500 <= int(d) <= 2099 and not any(x in ctx for x in LY):
                return d
            return group_digits(d)
        new = re.sub(r'(?<![\d.,])\d{4,}(?!\d)', sub, lit)
        if new != lit:
            lit_edits.append((a, b, new))
for a, b, new in reversed(lit_edits):
    text = text[:a] + new + text[b:]
# cfg edits: exact, each must match once
for old, new in (C.get('edits', []) if not __import__('os').environ.get('NOEDITS') else []):
    c = text.count(old)
    assert c == 1, (NAME, 'edit matches %d times' % c, old[:80])
    text = text.replace(old, new)
n_lit = len(lit_edits)
if True:
    # the text changed: everything above is worked out again on it
    k = segments(text)
    rts = routines(text)
    CAS_READERS, calls_cas = cas_readers()
    CASV = compute_casv(calls_cas, READER_POS)[0]
    CASFEED = casfeed()
    skip |= CASFEED
    ASSIGN_ANY = set(re.findall(r'\b([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=', code_only(0, len(text))))
    GCASV = global_casv()
print('global CAS variables: %s' % sorted(GCASV)[:12])
print('casfeed: %s' % sorted(CASFEED))
print('literals given commas: %d %s' % (n_lit, [t[2][:50] for t in lit_edits][:int(C.get('show_lits', 0))]))

edits = []                                   # (start, end, replacement)
n_ret = n_str = 0
n_cas = [0]


def returns_text():
    """the routines whose RETURN is text: a string, STRING, CHAR, or another such routine's result"""
    out = set(fmt)
    grew = True
    while grew:
        grew = False
        cre = re.compile(r'(?<![\w.])(%s)\s*\(' % '|'.join(re.escape(x) for x in sorted(out | {'STRING', 'CHAR', 'LEFT', 'MID', 'RIGHT'})))
        for nm, st, en in rts:
            if nm in out:
                continue
            for m in re.finditer(r'\bRETURN\b', text[st:en]):
                p = st + m.start()
                if k[p] != 'c':
                    continue
                r_ = text[p + 6:text.find(';', p)]
                if '"' in r_ or cre.search(r_):
                    out.add(nm)
                    grew = True
                    break
    return out


# a routine that writes CAS text is grouped where its text is used for the screen instead (outside the CAS's
# statements): its integer and fraction text ("2731/1000") reaches the screen with its commas
WRAPFEED = sorted((CASFEED & returns_text()) - {C['helper']} - set(C.get('casfam', [])))
print('wrapped where used, outside the CAS: %s' % WRAPFEED)
wrapn = ['STRING'] + sorted(fmt | set(WRAPFEED))
WRAP = re.compile(r'(?<![\w.])(%s)\s*\(' % '|'.join(wrapn))
rd = readers | set(wrapn)
fmt_in_cas = []
for nm, st, en in rts:
    if nm in fmt or nm in skip or nm == C['helper']:
        continue                              # a formatter's own text is wrapped where it is called
    for m in WRAP.finditer(text, st, en):
        p = m.start()
        if k[p] != 'c':
            continue
        anc = ancestors(text, k, p, st)
        if any(a in rd or a == C['helper'] for a in anc):
            continue
        if (nm in CASV and cas_statement(nm, st, p)) or key_statement(nm, st, p) or gcas_statement(nm, st, p):
            n_cas[0] += 1
            if m.group(1) != 'STRING':
                fmt_in_cas.append((nm, m.group(1)))
            continue
        op = text.index('(', p)
        cl = match_close(text, k, op)
        edits.append((p, cl + 1, C['helper'] + '(' + text[p:cl + 1] + ')'))
        if m.group(1) == 'STRING':
            n_str += 1
        else:
            n_ret += 1

# draw sites: the text argument of TEXTOUT_P, MSGBOX and the program's own text routines, operand by operand.  A
# string literal is never wrapped (a year in a citation stays "1971"); nor is CHAR(..), a number, a call already
# wrapped above, or an operand holding one.  Anything else -- a variable, a list item, another routine's text -- is.
def params(st):
    m = HEAD.match(text[st:text.index('\n', st)])
    return [x.strip() for x in m.group(2).split(',')] if m and m.group(2).strip() else []


def first_arg(op):
    """op: index of '(' -> (start, end) of the first argument"""
    d = 0
    for j in range(op, len(text)):
        if k[j] != 'c':
            continue
        if text[j] in '([{':
            d += 1
        elif text[j] in ')]}':
            d -= 1
            if d == 0:
                return op + 1, j
        elif text[j] == ',' and d == 1:
            return op + 1, j
    raise ValueError('no argument end')


def operands(a, b):
    """top-level '+' operands of text[a:b] as (start, end), stripped"""
    out, d, s0 = [], 0, a
    for j in range(a, b):
        if k[j] != 'c':
            continue
        if text[j] in '([{':
            d += 1
        elif text[j] in ')]}':
            d -= 1
        elif text[j] == '+' and d == 0:
            out.append((s0, j))
            s0 = j + 1
    out.append((s0, b))
    res = []
    for x, y in out:
        while x < y and text[x] in ' \t\n':
            x += 1
        while y > x and text[y - 1] in ' \t\n':
            y -= 1
        if x < y:
            res.append((x, y))
    return res


# variables that only ever hold the program's own wording: every assignment to them, anywhere, is made of string
# literals, CHAR(..) and other such variables (a help sentence, a data set's citation).  They carry no computed
# number -- a computed number reaches a text through STRING or a formatter, wrapped where it is called -- so a draw
# site leaves them alone, and a year in their wording keeps no comma ("Fleiss 1971").
ASSIGN = {}
_code_s = ''.join(ch if kk != 'm' else ' ' for ch, kk in zip(text, k))
for m in re.finditer(r'(?<![\w.])([A-Za-z_]\w*)\s*(?:\([^()]*\))?\s*:=', _code_s):
    if k[m.start()] != 'c':
        continue
    e = m.end()
    d = 0
    j = e
    while j < len(text):
        if k[j] == 'c':
            if text[j] in '([{':
                d += 1
            elif text[j] in ')]}':
                d -= 1
                if d < 0:
                    break
            elif text[j] == ';' and d == 0:
                break
        j += 1
    ASSIGN.setdefault(m.group(1), []).append(text[e:j])


# a routine's parameters are assigned at its calls: each argument is one more assignment of its parameter
_heads = {}
for _nm, _st, _en in rts:
    _m = HEAD.match(text[_st:text.index('\n', _st)])
    if _m and _m.group(2).strip():
        _heads[_nm] = [x.strip() for x in _m.group(2).split(',')]
if _heads:
    for _m in re.finditer(r'(?<![\w.])(%s)\s*\(' % '|'.join(re.escape(x) for x in _heads), text):
        _p = _m.start()
        if k[_p] != 'c' or HEAD.match(text[text.rfind('\n', 0, _p) + 1:text.find('\n', _p)]):
            continue
        _op = text.index('(', _p)
        _cl = match_close(text, k, _op)
        _args, _d, _s0 = [], 0, _op + 1
        for _j in range(_op + 1, _cl):
            if k[_j] != 'c':
                continue
            if text[_j] in '([{':
                _d += 1
            elif text[_j] in ')]}':
                _d -= 1
            elif text[_j] == ',' and _d == 0:
                _args.append(text[_s0:_j])
                _s0 = _j + 1
        _args.append(text[_s0:_cl])
        for _pn, _a in zip(_heads[_m.group(1)], _args):
            ASSIGN.setdefault(_pn, []).append(_a)


def _litform(rhs):
    x = re.sub(r'"[^"\n]*"', ' S ', rhs)
    x = re.sub(r'\bCHAR\(\s*\d+\s*\)', ' S ', x)
    return x


LITVARS = set(ASSIGN)
changed = True
while changed:
    changed = False
    for v in list(LITVARS):
        for rhs in ASSIGN[v]:
            toks = re.findall(r'[A-Za-z_]\w*|[^\sA-Za-z_]', _litform(rhs))
            if not toks or any(t not in ('S', '+', '{', '}', ',') and t not in LITVARS for t in toks):
                LITVARS.discard(v)
                changed = True
                break
LITVARS -= set(C.get('wrap_vars', []))

# ---- what may carry a number without its commas: text from the CAS, from EXPR, from the routines left alone (the
# CAS's helpers, integer-text and ratio routines, fit routines), and whatever is built from such text.  Every STRING
# and formatter call is grouped where it is made, so a text built from those and the program's own wording needs
# nothing more at the screen -- and a year in that wording keeps no comma.  These "tainted" texts are what a draw
# site wraps.
TSRC = set(skip) | set(C.get('casfam', [])) | {'EXPR', 'CAS'} | set(C.get('taint', [])) | \
    {nm for nm, _a, _b in rts if re.search(r'(IStr|Rat|RatS|IVal)$', nm)}
_callre = lambda names: re.compile(r'(?<![\w.])(%s)\s*\(' % '|'.join(re.escape(x) for x in names)) if names else None
TVARS, TFUNCS = set(), set(TSRC)
grew = True
while grew:
    grew = False
    cre = _callre(TFUNCS)
    for v, rhss in ASSIGN.items():
        if v in TVARS:
            continue
        for rhs in rhss:
            code_rhs = re.sub(r'"[^"\n]*"', '""', rhs)
            if (cre and cre.search(code_rhs)) or any(re.search(r'(?<![\w.])%s(?![\w])' % re.escape(t), code_rhs)
                                                     for t in TVARS):
                TVARS.add(v)
                grew = True
                break
    for _nm, _st, _en in rts:
        if _nm in TFUNCS:
            continue
        for _m in re.finditer(r'\bRETURN\b', text[_st:_en]):
            _p = _st + _m.start()
            if k[_p] != 'c':
                continue
            r_ = re.sub(r'"[^"\n]*"', '""', text[_p + 6:text.find(';', _p)])
            if (cre and cre.search(r_)) or any(re.search(r'(?<![\w.])%s(?![\w])' % re.escape(t), r_) for t in TVARS):
                TFUNCS.add(_nm)
                grew = True
                break


def tainted(seg):
    head = re.match(r'[A-Za-z_]\w*', seg)
    if not head:
        return True                       # an expression of some other shape: wrap it
    h_ = head.group(0)
    if re.fullmatch(r'[A-Za-z_]\w*', seg):
        return h_ in TVARS or h_ not in ASSIGN
    if re.fullmatch(r'[A-Za-z_]\w*\s*\(.*\)', seg, re.S):
        return h_ in TFUNCS or h_ in TVARS or (h_ not in ASSIGN and h_ not in {r[0] for r in rts}) or \
            bool(re.search(r'(?<![\w.])(%s)\s*\(' % '|'.join(re.escape(x) for x in TFUNCS), seg))
    return True
# routines whose every RETURN is such wording (a line "Data: " + a citation)
LITFUNCS = set()
for _nm, _st, _en in rts:
    _rets = []
    for _m in re.finditer(r'\bRETURN\b', text[_st:_en]):
        _p = _st + _m.start()
        if k[_p] != 'c':
            continue
        _e = text.find(';', _p)
        _rets.append(text[_p + 6:_e])
    if _rets and all(re.findall(r'[A-Za-z_]\w*|[^\sA-Za-z_]', _litform(r)) and
                     all(t in ('S', '+', '{', '}', ',') or t in LITVARS
                         for t in re.findall(r'[A-Za-z_]\w*|[^\sA-Za-z_]', _litform(r))) for r in _rets):
        LITFUNCS.add(_nm)

draw = {'TEXTOUT_P', 'MSGBOX'} | set(C.get('draw', []))
if os.environ.get('COMMAS_DEBUG'):
    for _nm, _st, _en in rts:
        _ps = params(_st)
        if _ps and 'TEXTOUT_P' in code_only(_st, _en) and _ps[0] in TVARS:
            print('DEBUG tainted first parameter of a drawing routine:', _nm, _ps[0])
grew = True
while grew:
    grew = False
    for nm, st, en in rts:
        ps = params(st)
        if nm in draw or not ps:
            continue
        body = code_only(st, en)
        if re.search(r'\b(%s)\s*\(\s*%s\s*[,)+]' % ('|'.join(sorted(draw)), re.escape(ps[0])), body[body.find('\n'):]):
            draw.add(nm)
            grew = True
DRAW = re.compile(r'(?<![\w.])(%s)\s*\(' % '|'.join(sorted(draw)))
spans = [(a, b) for a, b, _ in edits]
n_draw = 0
lit_runs = []
for nm, st, en in rts:
    if nm in fmt or nm in skip or nm == C['helper'] or nm in draw - {'TEXTOUT_P', 'MSGBOX'}:
        continue
    for m in DRAW.finditer(text, st, en):
        p = m.start()
        if k[p] != 'c':
            continue
        if (nm in CASV and cas_statement(nm, st, p)) or key_statement(nm, st, p) or gcas_statement(nm, st, p):
            continue
        a, b = first_arg(text.index('(', p))
        for x, y in operands(a, b):
            seg = text[x:y]
            if all(kk == 's' for kk in k[x:y]) or re.fullmatch(r'-?[\d.]+', seg) or re.fullmatch(r'CHAR\(\s*\d+\s*\)', seg) \
                    or seg.startswith(C['helper'] + '(') or any(ea >= x and eb <= y for ea, eb in spans) \
                    or seg in C.get('nowrap', []) or not tainted(seg):
                if all(kk == 's' for kk in k[x:y]) and re.search(r'(?<![\d.])\d{4,}', seg):
                    lit_runs.append((nm, seg[:60]))
                continue
            edits.append((x, y, C['helper'] + '(' + seg + ')'))
            n_draw += 1
print('draw routines: %s; literal 4-digit runs at draw sites: %d' % (sorted(draw - {'TEXTOUT_P', 'MSGBOX'}), len(lit_runs)))
for x in lit_runs[:int(C.get('show_lits', 0))]:
    print('   lit', x)

# nested calls: the outermost is wrapped only (the inner ones were skipped above: each wrapped name is a reader)
edits.sort()
for a, b in zip(edits, edits[1:]):
    assert a[1] <= b[0], ('overlapping edits', text[a[0]:a[1]][:60], text[b[0]:b[1]][:60])
out = text
for st, en, rep in reversed(edits):
    out = out[:st] + rep + out[en:]

# the helper, before the first routine
HELPER = '''// ---- {h}: commas in big numbers (round 5, {date}) ----
// Roger, 2 Nov 2026: "always put comma delimiters in big numbers".  STRING never
// groups digits, whatever Home's setting, so this inserts a comma every three
// digits in each run of four or more digits that does not follow a decimal
// point: "1234567.25" -> "1,234,567.25", "-98765" -> "-98,765"; "0.00012345",
// "1.8E10" and "1,000" stay as they are.  Only text for the screen comes here,
// never text the CAS or EXPR reads ("1,000" there is two numbers).
// Run on the Virtual Calculator: CommaProbe beta 1, 12 of 12 (2 Nov 2026).
{h}(cmS)
BEGIN
  LOCAL cmO, cmI, cmJ, cmN, cmR, cmK;
  cmN := DIM(cmS);
  IF cmN < 4 THEN RETURN cmS; END;
  cmO := ""; cmI := 1;
  WHILE cmI <= cmN DO
    IF INSTRING("0123456789", MID(cmS, cmI, 1)) > 0 THEN
      // a run of digits from cmI to cmJ
      cmJ := cmI;
      WHILE cmJ < cmN AND INSTRING("0123456789", MID(cmS, cmJ + 1, 1)) > 0 DO cmJ := cmJ + 1; END;
      cmR := MID(cmS, cmI, cmJ - cmI + 1);
      IF DIM(cmR) >= 4 AND (cmI == 1 OR MID(cmS, MAX(1, cmI - 1), 1) <> ".") THEN
        // the first group takes 1 to 3 digits, then a comma before every three
        cmK := DIM(cmR) MOD 3;
        IF cmK == 0 THEN cmK := 3; END;
        cmO := cmO + LEFT(cmR, cmK);
        WHILE cmK < DIM(cmR) DO
          cmO := cmO + "," + MID(cmR, cmK + 1, 3);
          cmK := cmK + 3;
        END;
      ELSE
        cmO := cmO + cmR;
      END;
      cmI := cmJ + 1;
    ELSE
      cmO := cmO + MID(cmS, cmI, 1);
      cmI := cmI + 1;
    END;
  END;
  RETURN cmO;
END;

'''.format(h=C['helper'], date=DATE)
first = routines(out)[0][1]
out = out[:first] + HELPER + out[first:]

# the version
OLD, NEW = C['old'], C['new']
lines = out.split('\n')
for i, ln in enumerate(lines[:40] if C.get('title', 1) else []):
    if ln.startswith('//') and re.search(r'\b%s\b' % re.escape(OLD), ln):
        lines[i] = re.sub(r'\b%s\b' % re.escape(OLD), NEW, ln, count=1)
        if C.get('title_date'):
            lines[i] = lines[i].replace(C['title_date'][0], C['title_date'][1])
        break
else:
    if C.get('title', 1):
        raise SystemExit('no title line names %s' % OLD)
out = '\n'.join(lines)
kk = segments(out)
lit = []
for m in re.finditer(r'"[^"\n]*"', out):
    if kk[m.start()] == 's' and re.search(r'\b%s\b' % re.escape(OLD), m.group(0)) and m.group(0) not in C.get('keep_lits', []):
        lit.append(m)
for m in reversed(lit):
    out = out[:m.start()] + re.sub(r'\b%s\b' % re.escape(OLD), NEW, m.group(0)) + out[m.end():]
anchor = text.split('\n')[C['anchor'] - 1] + '\n'
assert anchor.startswith('//'), (NAME, 'anchor is not a comment line', anchor)
assert out.count(anchor) == 1, (NAME, 'anchor', out.count(anchor), anchor[:60])
block = HISTORY(NAME, C, n_ret, n_str)
out = out.replace(anchor, block + anchor)
open(DST, 'w', encoding='utf-8').write(out)
print('%s %s -> %s: %d formatter calls, %d STRING calls and %d drawn texts wrapped, %d kept for the CAS%s, %d routines '
      'skipped, %d edits, %d version strings' % (NAME, OLD, NEW, n_ret, n_str, n_draw, n_cas[0],
                              (' (formatters there: %s)' % sorted(set(fmt_in_cas))) if fmt_in_cas else '', len(skip),
                              len(C.get('edits', [])), len(lit)))
