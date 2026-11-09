"""Round 11 (9 Nov 2026): plain-language help pages.  The shared core.

- exact text widths from the calculator's own glyph widths (GlyphProbe_v1 on the Virtual Calculator, 9 Nov 2026:
  a line's width is exactly the sum of its characters' widths, fonts 1, 2 and 3);
- a small parser for PPL string expressions ("..." + CHAR(n) + glyphConst + xxCm(...)), to read a help line's text;
- greedy wrapping by pixel width;
- PPL literal emission (ASCII in quotes, every other character as CHAR(n), so a program's code stays ASCII).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
GW = {int(k): v for k, v in json.load(open(os.path.join(HERE, '..', 'glyph_widths_vc.json'))).items()}


def norm(s):
    """the proposals' spellings -> the calculator's characters"""
    return (s.replace('x̄', '').replace('p̂', ''))


VAR_RE = re.compile(r'\x10(\d+)\x11')


def W(s, font=1, varw=None):
    """width in pixels; a variable marker counts as varw[idx]"""
    tot = 0
    i = 0
    for m in VAR_RE.finditer(s):
        tot += _w(s[i:m.start()], font)
        tot += (varw or {}).get(int(m.group(1)), 30)       # a value the page computes: about five digits
        i = m.end()
    return tot + _w(s[i:], font)


def _w(s, font):
    t = 0
    for ch in s:
        if ch in '\x01\x02\x13':
            continue
        c = ord(ch)
        if c not in GW:
            raise KeyError('no measured width for %r (U+%04X)' % (ch, c))
        t += GW[c][font - 1]
    return t


# ------------------------------------------------------------------ PPL string expressions
TOK = re.compile(r'\s*(?:(?P<str>"[^"]*")|(?P<num>\d+(?:\.\d+)?)|(?P<id>[A-Za-z_][A-Za-z0-9_]*)|(?P<op>[+(),])|(?P<oth>[^\s"]))')


class Seg:
    """a piece of a line: text (known) or a variable (code kept, text unknown)"""
    def __init__(self, kind, text='', code=''):
        self.kind, self.text, self.code = kind, text, code

    def __repr__(self):
        return '%s(%r%s)' % (self.kind, self.text, ', ' + self.code if self.code else '')


def group_commas(s):
    """the fleet's comma routine (xx_Cm): a comma every three digits in a run of 4+ digits not after a point"""
    def rep(m):
        d = m.group(0)
        out = ''
        while len(d) > 3:
            out = ',' + d[-3:] + out
            d = d[:-3]
        return d + out
    return re.sub(r'(?<![\d.,])\d{4,}', rep, s)


class Parser:
    def __init__(self, consts, cmfuncs=()):
        self.consts = consts
        self.cm = set(cmfuncs)

    def parse(self, src):
        self.toks = []
        pos = 0
        while pos < len(src):
            m = TOK.match(src, pos)
            if not m or m.end() == pos:
                if src[pos:].strip() == '':
                    break
                raise ValueError('cannot parse at %r' % src[pos:pos + 30])
            pos = m.end()
            for k in ('str', 'num', 'id', 'op', 'oth'):
                if m.group(k) is not None:
                    self.toks.append((k, m.group(k)))
                    break
        self.i = 0
        segs = self.expr()
        if self.i != len(self.toks):
            raise ValueError('trailing tokens in %r' % src)
        return merge(segs)

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def take(self, v=None):
        t = self.toks[self.i]
        if v is not None and t[1] != v:
            raise ValueError('expected %s got %s' % (v, t))
        self.i += 1
        return t

    def expr(self):
        segs = self.term()
        while self.peek() == ('op', '+'):
            self.take('+')
            segs += self.term()
        return segs

    def term(self):
        k, v = self.peek()
        if k == 'str':
            self.take()
            return [Seg('t', v[1:-1])]
        if k == 'op' and v == '(':
            self.take('(')
            s = self.expr()
            self.take(')')
            return s
        if k == 'id':
            self.take()
            if self.peek() == ('op', '('):
                start = self.i
                self.take('(')
                if v == 'CHAR':
                    n = self.take()[1]
                    self.take(')')
                    return [Seg('t', chr(int(float(n))))]
                if v in self.cm:
                    inner = self.expr()
                    self.take(')')
                    if all(s.kind == 't' for s in inner):
                        return [Seg('t', group_commas(''.join(s.text for s in inner)))]
                    return [Seg('v', '', v + '(' + render(inner) + ')')]
                # any other call: keep its code as a variable
                depth = 1
                while depth:
                    kk, vv = self.take()
                    if vv == '(':
                        depth += 1
                    elif vv == ')':
                        depth -= 1
                code = v + '(' + tok_join(self.toks[start + 1:self.i - 1]) + ')'
                return [Seg('v', '', code)]
            if v in self.consts:
                return [Seg('t', self.consts[v])]
            return [Seg('v', '', v)]
        raise ValueError('unexpected %s %s' % (k, v))


def tok_text(t):
    k, v = t
    return v + (' ' if v == ',' else '')


def tok_join(toks):
    out = ''
    for k, v in toks:
        if out and (k in ('id', 'num', 'str') and (out[-1].isalnum() or out[-1] == '"')):
            out += ' '
        out += v + (' ' if v == ',' else '')
    return out


def merge(segs):
    out = []
    for s in segs:
        if out and s.kind == 't' and out[-1].kind == 't':
            out[-1] = Seg('t', out[-1].text + s.text)
        else:
            out.append(s)
    return out


REV = {}          # a program's own glyph names: text -> name (set by the build for each program)
LITERAL = [False]  # True: a glyph may stand in the string itself (programs whose code is not kept ASCII)


def set_rev(consts):
    REV.clear()
    for k, v in consts.items():
        if v and len(v) <= 3 and any(ord(c) > 126 for c in v):
            if v not in REV or len(k) < len(REV[v]):
                REV[v] = k


def lit(text):
    """a PPL expression for plain text: ASCII in quotes; a glyph by the program's own name for it when it has one,
    else (and the double quote) as CHAR(n)"""
    parts, buf = [], ''
    keys = sorted(REV, key=len, reverse=True)
    i = 0
    while i < len(text):
        hit = next((kk for kk in keys if text.startswith(kk, i) and any(ord(c) > 126 for c in text[i:i + len(kk)][:1] + kk)), None)
        if hit and any(ord(c) > 126 for c in hit) and (ord(text[i]) > 126 or text[i:i + len(hit)] == hit and ord(hit[-1]) > 126 and hit[0] == text[i]):
            if buf:
                parts.append('"' + buf + '"')
                buf = ''
            parts.append(REV[hit])
            i += len(hit)
            continue
        ch = text[i]
        c = ord(ch)
        i += 1
        if (32 <= c <= 126 or (LITERAL[0] and c > 126 and not 0xE000 <= c <= 0xF8FF and c not in (0x302, 0x304))) and ch != '"':
            buf += ch
        else:
            if buf:
                parts.append('"' + buf + '"')
                buf = ''
            parts.append('CHAR(%d)' % c)
    if buf:
        parts.append('"' + buf + '"')
    return ' + '.join(parts) if parts else '""'


def render(segs):
    """PPL code for a list of segments"""
    out = []
    for s in segs:
        out.append(lit(s.text) if s.kind == 't' else s.code)
    return ' + '.join(out) if out else '""'


def find_consts(src_text):
    """file-level glyph constants: a name assigned exactly once, from CHAR() and literals only"""
    cands = {}
    count = {}
    p = Parser({})
    code = '\n'.join(re.sub(r'^\s*//.*$', '', l) for l in src_text.split('\n'))
    for m in re.finditer(r'(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*([^;\n]+);', code):
        name, rhs = m.group(1), m.group(2)
        count[name] = count.get(name, 0) + 1
        try:
            segs = p.parse(rhs)
        except Exception:
            continue
        if segs and all(s.kind == 't' for s in segs):
            cands[name] = ''.join(s.text for s in segs)
    return {k: v for k, v in cands.items() if count.get(k) == 1}


# ------------------------------------------------------------------ wrapping
OPS = set(['+', '-', '\u2212', '=', '\u00d7', '\u00b1', '/', '|', '<', '>', '\u2264', '\u2265', '\u2260', '\u2192', '*', '^', '&'])
NUMW = re.compile(r'^[\(]?-?\d+([.,]\d+)*[%]?$')
NB = '\x13'          # a space that does not break
# a statistic's name stays whole: a one-letter symbol (t, q, z, F, χ² ...) and the crit, obt or obs after it are not split
# at the end of a line (Round 11, 9 Nov 2026: TTestLab's page 1 had "3 crit (t" / "crit)").  Only these words: a letter
# that ends a phrase ("top-left count a", "or I") must stay where it is, so a general one-letter rule is wrong.
CRIT = re.compile(r'^(crit|obt|obs)\b')
ONE = re.compile('^[(\\[]?[A-Za-z\u0370-\u03ff\ue000\ue001][\u2080-\u2089\u00b2\u0304]?$')


def bind_ops(t, maxw, font, varw):
    """join an operator standing alone ("A + B", "d = x") to the words on both sides, so a formula is not broken
    at its operator; a run that would not fit on a line is left breakable"""
    parts = re.split(r'( +)', t)
    words, seps = parts[0::2], parts[1::2]
    out = [words[0]]
    for k in range(1, len(words)):
        sep = seps[k - 1]
        if (words[k] in OPS or words[k - 1] in OPS or (NUMW.match(words[k - 1]) and re.match(r'^[A-Za-z]{1,2}[:;,.)]*$', words[k]))
                or (ONE.match(words[k - 1]) and CRIT.match(words[k]))):
            cand = out[-1] + NB * len(sep) + words[k]
            if W(cand.replace(NB, ' '), font, varw) <= maxw * 0.6:
                out[-1] = cand
                continue
        out.append(sep)
        out.append(words[k])
    # rebuild with the separators kept
    res = out[0]
    for k in range(1, len(out), 2):
        res += out[k] + out[k + 1]
    return res


def wrap(text, maxw, font=1, ind0='', ind1='', varw=None):
    """greedy wrap by pixels; keeps the spaces between words as written (two after a full stop)"""
    t = re.sub(r'[ \t]*\n[ \t]*', ' ', text).strip(' ')
    t = bind_ops(t, maxw, font, varw)
    parts = re.split(r'( +)', t)
    lines, cur = [], ind0
    for k in range(0, len(parts), 2):
        w = parts[k]
        sp = parts[k - 1] if k else ''
        if cur.strip() and W((cur + sp + w).replace(NB, ' '), font, varw) > maxw:
            lines.append(cur)
            cur = ind1 + w
        else:
            cur = cur + (sp if cur.strip() else '') + w
    lines.append(cur)
    # no orphan: a last line of one short word takes a word from the line above, if it still fits
    if len(lines) >= 2 and W(lines[-1].replace(NB, ' ').strip(), font, varw) < 45:
        pw = re.split(r'( +)', lines[-2].rstrip())
        if len(pw) >= 5:
            moved = pw[-1]
            cand = (ind1 if len(lines) > 2 or True else ind0) + moved + pw[-2][:2] + lines[-1].lstrip()
            cand = ind1 + moved + ' ' + lines[-1].lstrip()
            if W(cand.replace(NB, ' '), font, varw) <= maxw:
                lines[-2] = ''.join(pw[:-2])
                lines[-1] = cand
    lines = [l.replace(NB, ' ') for l in lines]
    for l in lines:
        if W(l, font, varw) > maxw:
            raise ValueError('a word longer than the line: %r (%d > %d)' % (l, W(l, font, varw), maxw))
    return lines


def segs_to_marked(segs):
    """segments -> text with \\x10i\\x11 markers for variables, and the list of variable codes"""
    txt, codes = '', []
    for s in segs:
        if s.kind == 't':
            txt += s.text
        else:
            txt += '\x10%d\x11' % len(codes)
            codes.append(s.code)
    return txt, codes


def marked_to_code(txt, codes):
    out, i = [], 0
    for m in VAR_RE.finditer(txt):
        if txt[i:m.start()]:
            out.append(lit(txt[i:m.start()]))
        out.append(codes[int(m.group(1))])
        i = m.end()
    if txt[i:]:
        out.append(lit(txt[i:]))
    return ' + '.join(out) if out else '""'


def plain(txt):
    return VAR_RE.sub('', txt)
