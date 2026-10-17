#!/usr/bin/env python3
"""ppl_run_v3c.py -- run an HP Prime PPL program on the PC, scripted like a student at the keys.

Built on hp-prime-kit's interpreter (hpkit.interp, JordiRigau/hp-prime-kit), which runs
the real source but answers every key, menu and form with a fixed stand-in. This adds:

  * a pre-pass so fleet files load as written: #pragma lines and #PYTHON blocks blanked,
    #RRGGBBh and #RRGGBB:24h colours to decimal, the root sign as SQRT(...), and the
    Unicode operators <= >= <> and minus to ASCII -- only in code, never in strings or
    comments; pi and e are defined as globals, so the source keeps its pi sign;
  * a parser that also reads file-level LOCAL (anywhere at the top level, after an
    EXPORT list too), forward declarations `name();` and `LOCAL name(...)` routine heads;
  * SciPy-backed statistics built-ins (NORMALD*, STUDENT*, CHISQUARE*, FISHER*,
    BINOMIAL*, POISSON*, COMB, PERM) with the argument forms of HP's help, and STRING
    with its display modes (2 = fixed decimals) instead of the kit's raw repr;
  * scripted input: one ordered queue of keys and touches (GETKEY, MOUSE, WAIT(-1),
    ISKEYDOWN) and answer queues for CHOOSE and INPUT, written back into the variables
    named in the call, as the calculator does;
  * a record of what the student would have seen: every TEXTOUT_P with its position,
    font and colour, every screen shown (each BLIT_P to G0, and G0 drawn directly when
    the program waits), every MSGBOX, CHOOSE and INPUT, the Terminal.

usage (CLI):
  python3 ppl_run_v3c.py PROG.txt [MORE.txt ...] --call "Func(args)" [options]
    --choose N|LABEL     answer the next CHOOSE (repeatable; 0 = cancel)
    --input SPEC         answer the next INPUT: "name=value,name=value", "1,2,3" (by
                         position), "ok" (accept as shown) or "cancel" (repeatable)
    --key K              queue a key: a code or Esc/Enter/Left/Right/Up/Down/Plus/Minus/Zero
    --tap X,Y            queue a tap;  --timeout  queue a WAIT(-1) time-out
    --idle-key K         when the queue is empty and the program waits, press K
    --strict             an empty CHOOSE/INPUT queue raises instead of cancel/accept
    --stale-keys         leave each dialog's OK/Cancel press in the key buffer, as on
                         the device, to find pages an undrained wait would skip
    --show screens|texts|timeline|all   (default: timeline)
    --coverage           list the built-ins the program calls that this harness lacks
    --seed N             seed for RANDOM/RANDINT (default 0)

usage (Python):
  from ppl_run_v3c import Harness, KEY, CANCEL
  h = Harness('StatDist_v2.5.txt')
  h.choose(1)                                   # Probability Type: lower tail
  h.answer({'mean': 100, 'stdev': 15, 'x_val': 130})
  h.press(KEY['Enter'])                         # leave the result page
  h.call('st_calc_normal')
  assert h.pages[-1].has('P(X <= 130.0000) = 0.977250')

See README.md beside this file for the model, what is covered, and the limits.
v1, 16 Oct 2026.  v2, 16 Oct 2026: a bare RANDOM is routed like GETKEY/MOUSE/TICKS, and a list or
matrix is COPIED on assignment, as on the calculator (v1 shared it).
v3, 16 Oct 2026: CAS("...") is answered by Giac (the engine inside the Prime's CAS; the
desktop build is 1.9, the Prime's is older, so a device probe still decides).  Every call is
logged in h.cas_calls as (expression, answer text, ms).  STRING(CAS(s)) and "text" + CAS(s)
give Giac's answer as text; a quoted Giac string comes back without its quotes.  A Giac
'Error:' raises a runtime error, so the program's IFERR runs.  Harness(path, cas='fail')
makes every CAS call fail (to test the fallback); cas={'expr': 'answer'} gives canned answers.
v3a, 16 Oct 2026: finds hp-prime-kit by itself again (HPKIT, else the Community_Library zip beside
this file or one folder up -- v1's _find_kit, lost in v2/v3), Giac output decoded with errors='replace',
POS and INSTRING covered.
v3b, 17 Oct 2026: the CAS modelled as the HP Prime Virtual Calculator answered CASProbe beta 1a/1b
(build 2026-09-09, 17 Oct 2026):
  * CAS(s) with a NON-literal argument (a variable, a parameter, a concatenation) hands the text
    back UNEVALUATED, as a PPL string -- so the old xxCas (STRING(CAS(xxS))) returns its own input;
  * CAS("literal") -- written in the source, or built at run time and read by EXPR, i.e.
    EXPR("CAS(" + CHAR(34) + s + CHAR(34) + ")") -- is evaluated by Giac; so is
    EXPR("CAS.eval(" + q + s + q + ")") and EXPR("CAS.name(args)");
  * Giac's printing is translated into the Prime's (prime_print): exp( -> e^( ; sqrt(u) -> the
    root sign before an atom, root sign + (u) otherwise; list[...] -> {...} (solve);
    +infinity -> the infinity sign, -infinity -> minus infinity, the unsigned infinity -> the
    plus-minus infinity sign (the Prime's 1/0);
  * a CAS string (string(...)) crosses into PPL as a PPL string (TYPE 2), so STRING() of it adds
    the quotes; any other answer is a CAS object (TYPE 8); a NON-string integer of more than 12
    digits crosses as a 12-digit real (1.00891344546E29);
  * a CAS variable assigned with := persists into later calls (and, on the calculator, into the
    student's CAS) until purge(name): replayed here, listed in h.cas_vars, and warned about.
  h.cas_calls holds (expression, the Prime-printed answer, ms); h.cas_desktop the raw desktop
  answers.  prime_eval(expr) is giac_eval with the Prime's printing, for verify scripts.
v3c, 17 Oct 2026: findings of the first emulator round (HP Prime Virtual Calculator 2.4.2, build
2026-09-09; Emulator_Round1_Results_2026-10-17_v1.md) are modelled, so a program the emulator showed
failing also fails here:
  * F1 (MenuTapProbe beta 1): with DRAWMENU on the screen, a tap on the soft-key strip (y >= 218)
    reaches WAIT(-1) ONLY as {3, x, y} (type 3 = click): no press, no lift.  A tap above the strip
    reaches it as {0, x, y}, then {2}, then {3, x, y}.  (wait_model='device', the default;
    wait_model='v3b' keeps v3b's {0, x, y} [then {2} with lift=True] for old scripts.)
    mouse_tail=True also leaves {2}, {3, x, y} for the next WAIT(-1) after a tap that MOUSE read --
    a worst case, NOT measured, for testing a program's guard against a stale click.
  * F3 (GfxProbe beta 1 T11/T12 and the Home checks): CHISQUARE_CDF, CHISQUARE_ICDF, FISHER_CDF and
    FISHER_ICDF with a non-integer df are a run-time error, "Invalid input" (a PPLError, which IFERR
    catches, as on the calculator); so is POISSON_CDF(mu, k) with k < 0.  CHISQUARE(df, x), STUDENT,
    STUDENT_CDF and STUDENT_ICDF take any df > 0 (they matched SciPy to 12 digits): no warning now.
  * GfxProbe T01-T06 and T08 passed on the emulator, so FILLPOLY_P (both point-list forms), the
    one-colour, blended and alpha TRIANGLE_P and the 10-argument scaled BLIT_P no longer warn; the
    3-D TRIANGLE_P mesh form (T07 drew nothing) does.  T09: ARC_P at r <= 3 used as a solid dot
    leaves diagonal holes, so a small ARC_P now gives one warning per run.
"""
from __future__ import print_function

import argparse
import collections
import itertools
import math
import os
import random
import copy
import re
import sys
import time

def _find_kit():
    """HPKIT if set; else hp-prime-kit unpacked from a Community_Library zip next to this file
    or one folder up (D:\\HP-Prime's layout; ppl_gate_v1a.py unpacks it to the same temp
    folder); else the cloud workspace path."""
    if os.environ.get('HPKIT'):
        return os.environ['HPKIT']
    import tempfile, zipfile
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (here, os.path.dirname(here), os.path.dirname(os.path.dirname(here))):
        z = os.path.join(d, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit.zip')
        if os.path.exists(z):
            dest = os.path.join(tempfile.gettempdir(), 'hpkit_gate')
            root = os.path.join(dest, 'hp-prime-kit-HEAD')
            if not os.path.exists(os.path.join(root, 'hpkit')):
                with zipfile.ZipFile(z) as zf:
                    zf.extractall(dest)
            return root
    return '/home/claude/kit/hp-prime-kit-HEAD'


KIT = _find_kit()
if KIT not in sys.path:
    sys.path.insert(0, KIT)
try:
    from hpkit import interp                              # noqa: E402
except ImportError:
    raise SystemExit('ppl_run_v3c: hp-prime-kit not found. Set HPKIT to the folder that holds hpkit/ '
                     '(github.com/JordiRigau/hp-prime-kit), or keep Community_Library/github/'
                     'JordiRigau__hp-prime-kit.zip within two folders above this file.')
from hpkit.interp import PPLError, Unsupported            # noqa: E402

__all__ = ['Harness', 'KEY', 'CANCEL', 'ACCEPT', 'Key', 'Tap', 'Drag', 'Timeout',
           'HarnessStall', 'HarnessScriptError', 'Unverified', 'PPLError',
           'Unsupported', 'preprocess', 'giac_eval', 'prime_eval', 'prime_print', 'CasResult']

# The GETKEY codes that are device-verified (Lessons Learned s6). Others may be queued
# as numbers; the program only compares them.
KEY = {'Esc': 4, 'Left': 7, 'Right': 8, 'Up': 2, 'Down': 12, 'Enter': 30,
       'Plus': 50, 'Minus': 45, 'Zero': 42}

PRIME_MAX = 9.99999999999e499       # the Prime's real range; a double stops at 1.8e308


class HarnessStall(Exception):
    """The program waits for input that the script does not supply."""


class HarnessScriptError(Exception):
    """The script does not fit what the program asked (a CHOOSE label that is not on
    the menu, an INPUT answer naming a field the form does not have ...)."""


class Unverified(Unsupported):
    """A call whose answer on the device has never been observed (POISSON_CDF with a
    negative k, a negative sigma ...). The harness will not invent one."""


class _Cancel(object):
    def __repr__(self):
        return 'CANCEL'


class _Accept(object):
    def __repr__(self):
        return 'ACCEPT'


CANCEL = _Cancel()      # an INPUT answer: press Cancel on the form
ACCEPT = _Accept()      # an INPUT answer: press OK with the form as shown


# ================================================================ input events
class Key(object):
    """A key press. `hold` = how many further passes of the loop that received it
    ISKEYDOWN keeps reporting it down (0: only the pass it arrived in)."""

    def __init__(self, code, hold=0, anytime=False):
        self.code, self.hold, self.idle = int(code), int(hold), False
        self.anytime = bool(anytime)

    def accepts(self, kind, code=None):
        return kind == 'key' or (kind == 'down' and code == self.code)

    def __repr__(self):
        return 'Key(%d%s)' % (self.code, ', idle' if self.idle else '')


class Tap(object):
    """A finger down at (x, y) and up again. MOUSE sees one reading
    {x, y, x, y, 0} (type 0 = new), then `hold` more readings of the same point with
    type 2, then no finger. WAIT(-1) sees {0, x, y}; with lift=True the next WAIT(-1)
    sees the one-element lift list {2} (WaitLab's observation, not device-verified
    by us)."""

    def __init__(self, x, y, lift=False, hold=0, anytime=False):
        self.x, self.y, self.lift, self.hold = float(x), float(y), bool(lift), int(hold)
        self.anytime = bool(anytime)

    def accepts(self, kind, code=None):
        return kind == 'mouse'

    def readings(self):
        first = [self.x, self.y, self.x, self.y, 0.0]
        return [first] + [[self.x, self.y, self.x, self.y, 2.0] for _ in range(self.hold)]

    def __repr__(self):
        return 'Tap(%g, %g)' % (self.x, self.y)


class Drag(object):
    """A finger put down at points[0] and moved through the rest. MOUSE sees the first
    reading with type 0 and one later reading per MOUSE call, type 2 (HP's MOUSE
    table); WAIT(-1) sees {0,x,y}, then {1,x,y} per point (types 0 and 1 are device-
    verified), then {2} when lift=True."""

    def __init__(self, points, lift=True, anytime=False):
        self.points = [(float(x), float(y)) for x, y in points]
        if not self.points:
            raise ValueError('a Drag needs at least one point')
        self.lift, self.anytime = bool(lift), bool(anytime)

    def accepts(self, kind, code=None):
        return kind == 'mouse'

    def readings(self):
        x0, y0 = self.points[0]
        return ([[x0, y0, x0, y0, 0.0]] +
                [[x, y, x0, y0, 2.0] for x, y in self.points[1:]])

    def __repr__(self):
        return 'Drag(%d points from %g,%g)' % ((len(self.points),) + self.points[0])


class Timeout(object):
    """WAIT(-1) giving up with no event (about 60 s on the device): it answers -1."""

    def accepts(self, kind, code=None):
        return False

    def __repr__(self):
        return 'Timeout()'


# ============================================================ what was drawn
class Grob(object):
    """G0..G9. G0 is the screen."""

    def __init__(self, name):
        self.name, self.items, self.menu = name, [], None
        self.w, self.h, self.bg = 320, 240, 0xFFFFFF

    def __repr__(self):
        return self.name


# rough average glyph widths (px per character) by font size; a measured point:
# "abc" in font 2 is 19 px (hp-prime-kit, emulator). Estimates only.
_CHAR_W = {0: 6.5, 1: 5.5, 2: 6.5, 3: 7.5, 4: 8.5, 5: 9.5, 6: 11.0, 7: 13.0}


class Text(object):
    def __init__(self, text, x, y, font, color, width, bg, grob, func):
        self.text, self.x, self.y = text, x, y
        self.font, self.color, self.width, self.bg = font, color, width, bg
        self.grob, self.func = grob, func

    @property
    def hex(self):
        return '#%06X' % int(self.color) if self.color is not None else None

    @property
    def est_width(self):
        return len(self.text) * _CHAR_W.get(int(self.font or 0), 6.5)

    @property
    def clipped(self):
        """True when the text is probably wider than its width argument (an estimate
        from average glyph widths -- treat as a hint, not a measurement)."""
        return self.width is not None and self.est_width > self.width

    def __repr__(self):
        return 'Text(%r @%g,%g f%s %s)' % (self.text, self.x, self.y, self.font, self.hex)


class Shape(object):
    def __init__(self, cmd, args, grob):
        self.cmd, self.args, self.grob = cmd, args, grob

    def __repr__(self):
        return '%s%r' % (self.cmd, tuple(self.args))


class Screen(object):
    """What G0 held when it was captured: at every BLIT_P to G0 (reason 'blit'), and
    when the program started waiting for input or opened a dialog after drawing on G0
    directly ('wait', 'dialog'), or at the end of the call ('end')."""

    def __init__(self, items, menu, reason, func, index):
        self.items, self.menu, self.reason, self.func, self.index = items, menu, reason, func, index

    @property
    def texts(self):
        return [i for i in self.items if isinstance(i, Text)]

    @property
    def shapes(self):
        return [i for i in self.items if isinstance(i, Shape)]

    def lines(self):
        """The text strings, top to bottom, then left to right."""
        return [t.text for t in sorted(self.texts, key=lambda t: (t.y, t.x))]

    def find(self, sub):
        for t in self.texts:
            if sub in t.text:
                return t
        return None

    def has(self, sub):
        return self.find(sub) is not None

    def text_at(self, y, tol=0):
        return [t for t in self.texts if abs(t.y - y) <= tol]

    def __repr__(self):
        return 'Screen#%d(%s, %s, %d texts%s)' % (
            self.index, self.reason, self.func, len(self.texts),
            ', menu' if self.menu else '')


class MsgBox(object):
    def __init__(self, text, func):
        self.text, self.func = text, func
        self.lines = text.split('\n')

    @property
    def over_five(self):
        """MSGBOX shows about five lines (Lessons Learned s3)."""
        return len(self.lines) > 5

    def __repr__(self):
        return 'MsgBox(%d lines: %r)' % (len(self.lines), self.text[:60])


class Choose(object):
    def __init__(self, title, items, index, func):
        self.title, self.items, self.index, self.func = title, items, index, func

    @property
    def label(self):
        return self.items[self.index - 1] if self.index >= 1 else None

    def __repr__(self):
        return 'Choose(%r -> %d %r)' % (self.title, self.index, self.label)


class Input(object):
    def __init__(self, title, names, labels, helps, before, after, accepted, func):
        self.title, self.names, self.labels, self.helps = title, names, labels, helps
        self.before, self.after, self.accepted, self.func = before, after, accepted, func

    def __repr__(self):
        return 'Input(%r %s -> %s)' % (self.title, self.after,
                                       'OK' if self.accepted else 'Cancel')


class _Loop(object):
    __slots__ = ('id', 'iter', 'waiting', 'blocked', 'func', 'stale_iter')

    def __init__(self, lid, func):
        self.id, self.iter, self.waiting, self.blocked, self.func = lid, 0, 0, 0, func
        self.stale_iter = None


# ================================================================== pre-pass
_HEX = re.compile(r'#([0-9A-Fa-f]+)(?::\d+)?h\b')
_ASCII_OPS = {u'\u2264': '<=', u'\u2265': '>=', u'\u2260': '<>', u'\u2212': '-'}
_ROOT = u'\u221a'      # the root sign


def _code_transform(seg, notes):
    """Rewrite one stretch of code (no strings, no comments in it)."""
    def hexrep(m):
        notes['hex colours'] += 1
        return str(int(m.group(1), 16))
    seg = _HEX.sub(hexrep, seg)
    for u, a in _ASCII_OPS.items():
        if u in seg:
            notes['%s -> %s' % (u, a)] += seg.count(u)
            seg = seg.replace(u, a)
    if _ROOT in seg:
        out, i = [], 0
        while i < len(seg):
            c = seg[i]
            if c != _ROOT:
                out.append(c)
                i += 1
                continue
            notes['root sign -> SQRT'] += 1
            j = i + 1
            while j < len(seg) and seg[j] in ' \t':
                j += 1
            if j < len(seg) and seg[j] == '(':
                out.append('SQRT')                   # the parenthesis stays
                i = j
                continue
            m = re.match(r'[^\W\d]\w*|\d*\.?\d+(?:[eE][+-]?\d+)?', seg[j:])
            if not m:
                raise PPLError('a root sign not followed by ( or a name or number')
            out.append('SQRT(' + m.group(0) + ')')
            i = j + len(m.group(0))
        seg = ''.join(out)
    return seg


def preprocess(text):
    """-> (text the kit can read, {what was changed: count}). Line numbers are kept:
    blanked lines stay as empty lines."""
    notes = collections.Counter()
    lines, inpy = [], False
    for ln in text.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        s = ln.strip()
        if s.startswith('#PYTHON'):
            inpy = True
            notes['#PYTHON blocks'] += 1
        if inpy:
            if s.startswith('#END'):
                inpy = False
            lines.append('')
            continue
        if s.startswith('#pragma'):
            notes['#pragma lines'] += 1
            lines.append('')
            continue
        lines.append(ln)
    text = '\n'.join(lines)
    if text.startswith(u'\ufeff'):
        text = text[1:]
    # walk code / "string" / // comment / /* comment */, transform only the code
    out, seg, i, n = [], [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = text.find('"', i + 1)
            j = n - 1 if j < 0 else j
            out.append(_code_transform(''.join(seg), notes)); seg = []
            out.append(text[i:j + 1]); i = j + 1
            continue
        if text.startswith('//', i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            out.append(_code_transform(''.join(seg), notes)); seg = []
            out.append(text[i:j]); i = j
            continue
        if text.startswith('/*', i):
            j = text.find('*/', i + 2)
            j = n if j < 0 else j + 2
            out.append(_code_transform(''.join(seg), notes)); seg = []
            out.append(text[i:j]); i = j
            continue
        seg.append(c)
        i += 1
    out.append(_code_transform(''.join(seg), notes))
    return ''.join(out), dict(notes)


class _Parser(interp.Parser):
    """The kit's parser, plus four top-level forms the fleet uses: file-level LOCAL
    (before or after EXPORT lines), forward declarations `name(a, b);`, routine heads
    written `LOCAL name(...)` (PowerViz), and an app program's View-menu entries
    `VIEW "label", name()` (CentralLimit)."""

    def program(self):
        funcs, globs = {}, []
        self.forward, self.file_locals, self.views = [], [], []
        while not self.at('EOF'):
            self.semicolon()
            if self.at('EOF'):
                break
            if (self.at('ID') and self.peek().val.upper() == 'VIEW'
                    and self.peek(1).kind == 'STR'):           # VIEW "label", name()
                self.take('ID')
                label = self.take('STR').val
                self.take('OP', ',')
                name = self.take('ID').val
                funcs[name] = (self.param_list(), self.block())
                self.views.append((label, name))
                continue
            exported = self.accept('KW', 'EXPORT')
            is_local = self.accept('KW', 'LOCAL')
            if not self.at('ID'):
                self._error('expected a name at the top level')
            name = self.take('ID').val
            if self.at('OP', '('):
                params = self.param_list()
                if self.at('OP', ';'):                 # a forward declaration
                    self.forward.append(name)
                    self.semicolon()
                    continue
                funcs[name] = (params, self.block())
                continue
            line, valued = self.peek().line, 0
            while True:
                init = None
                if self.accept('OP', ':='):
                    init = self.expr()
                    valued += 1
                globs.append((name, init))
                if is_local:
                    self.file_locals.append(name)
                if not self.accept('OP', ','):
                    break
                name = self.take('ID').val
            if exported and valued >= 7:
                raise PPLError('%s:%d: %d variables with initial values in one EXPORT: '
                               'seven do not compile on the calculator'
                               % (self.filename, line, valued))
            self.semicolon()
        return funcs, globs


# ===================================================================== text
def _std(v):
    """A number as Home's Standard format would write it: up to 12 significant digits
    (the Prime's precision), trailing zeros dropped, E for the exponent. An
    approximation of the device's layout -- the switch-over points to E notation and the
    minus glyph are not measured."""
    if isinstance(v, bool):
        v = float(v)
    if isinstance(v, float):
        if v != v or v in (float('inf'), float('-inf')):
            raise Unsupported('a non-finite number (%r) has no Prime display form' % v)
        if v == 0:
            return '0'
        s = '%.12g' % v
        if 'e' in s:
            mant, ex = s.split('e')
            s = mant + 'E' + str(int(ex))
        return s
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return '{' + ','.join(_std(x) for x in v) + '}'
    if isinstance(v, interp.Matrix):
        return '[' + ','.join('[' + ','.join(_std(x) for x in r) + ']' for r in v.rows) + ']'
    if isinstance(v, Grob):
        return v.name
    if isinstance(v, CasResult):
        return v.text
    return str(v)


class CasResult(object):
    """What CAS("...") hands back in the harness when the answer is not a string: a CAS
    object (TYPE 8), printed as the Prime prints it (v3b: prime_print).  A CAS string
    is handed back as a PPL string instead (v3b), so is_str is normally False here."""
    def __init__(self, raw):
        self.raw = raw
        self.is_str = len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"'
        self.text = raw[1:-1] if self.is_str else raw

    def __repr__(self):
        return 'CasResult(%r)' % self.raw


_GIAC = None


def giac_eval(expr, timeout=60):
    """Evaluate one CAS expression with the desktop Giac (icas); return its printed answer."""
    import subprocess, tempfile, shutil
    global _GIAC
    if _GIAC is None:
        _GIAC = shutil.which('icas') or ''
    if not _GIAC:
        raise Unsupported('CAS(...) needs Giac (apt-get install xcas, which provides icas)')
    with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
        f.write(expr.rstrip().rstrip(';') + ';\n')
        name = f.name
    try:
        pr = subprocess.run([_GIAC, name], capture_output=True, timeout=timeout)
        out = pr.stdout.decode('utf-8', errors='replace')
        err = pr.stderr.decode('utf-8', errors='replace')
    finally:
        os.unlink(name)
    # v3b: a syntax error is a run-time error on the Prime (CASProbe beta 1b T26, IFERR catches
    # it); desktop Giac reports it on stderr and answers "undef" (string(...)) or nothing.
    for ln in err.split('\n'):
        if 'syntax error' in ln:
            return 'Error: ' + ln.strip()[:120]
    keep = []
    for ln in out.split('\n'):
        t = ln.strip()
        if not t or t.startswith('// ') or t.startswith('Added ') or t.startswith('Warning'):
            continue
        keep.append(ln.rstrip())
    txt = '\n'.join(keep).strip()
    if txt.endswith(','):
        txt = txt[:-1]
    return txt


# v3b: how the Prime prints a CAS answer, measured on the Virtual Calculator (CASProbe beta 1b,
# build 2026-09-09, 17 Oct 2026), against desktop Giac 1.9:
#   exp(cxt^2/2)            -> e^(cxt^2/2)                (also inside string(...) answers)
#   exp(1)^4                -> (e^(1))^4  (not measured: kept re-readable, as ^ groups right)
#   sqrt(2), sqrt(u+1)      -> the root sign: \u221a2, \u221a(u+1)
#   list[1/20], list[[2,1]] -> {1/20}, {[2,1]}           (solve)
#   +infinity / -infinity   -> \u221e / -\u221e           (limit)
#   infinity (unsigned)     -> \u00b1\u221e                (1/0)
# Everything else measured prints alike (seq and matrices in [], products with *, undef,
# evalf to 12 significant digits, an unknown function handed back unevaluated).
SQRT_SIGN = u'\u221a'
INF_SIGN = u'\u221e'
_PP_FUNC = re.compile(r'(?<![A-Za-z0-9_])(sqrt|exp|list)([(\[])')
_PP_ATOM = re.compile(r'[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?')
_PP_INF = re.compile(r'([+-]?)(?<![A-Za-z0-9_])infinity(?![A-Za-z0-9_])')


def _pp_close(s, i, op, cl):
    """Index of the bracket that closes the one at s[i] (same kind only), or -1."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == op:
            depth += 1
        elif s[j] == cl:
            depth -= 1
            if depth == 0:
                return j
    return -1


def _pp_funcs(s):
    out, i = [], 0
    while i < len(s):
        m = _PP_FUNC.search(s, i)
        if not m:
            out.append(s[i:])
            break
        name, br = m.group(1), m.group(2)
        if (name == 'list') != (br == '['):          # exp[ / sqrt[ / list( : not ours
            out.append(s[i:m.end()])
            i = m.end()
            continue
        out.append(s[i:m.start()])
        j = _pp_close(s, m.end() - 1, br, ')' if br == '(' else ']')
        if j < 0:                                     # unbalanced: leave the rest alone
            out.append(s[m.start():])
            break
        inner = _pp_funcs(s[m.end():j])
        powered = s[j + 1:j + 2] == '^'               # exp(1)^4: keep the meaning (e^(1))^4,
        if name == 'exp':                             # since ^ groups to the right
            t = 'e^(' + inner + ')'
            out.append('(' + t + ')' if powered else t)
        elif name == 'sqrt':
            t = SQRT_SIGN + (inner if _PP_ATOM.fullmatch(inner) else '(' + inner + ')')
            out.append('(' + t + ')' if powered else t)
        else:
            out.append('{' + inner + '}')
        i = j + 1
    return ''.join(out)


def _pp_inf(m):
    sign, pre = m.group(1), m.string[:m.start()]
    binary = bool(pre) and (pre[-1].isalnum() or pre[-1] in ')]}_')
    if sign == '+':
        return ('+' if binary else '') + INF_SIGN
    if sign == '-':
        return '-' + INF_SIGN
    return u'\u00b1' + INF_SIGN


def prime_print(txt):
    """Desktop Giac's printed answer -> the text the Prime prints for the same answer (v3b)."""
    return _PP_INF.sub(_pp_inf, _pp_funcs(txt))


def prime_eval(expr, timeout=60):
    """giac_eval with the Prime's printing: what a CAS template gives on the calculator, as far
    as the emulator measurements go (v3b).  A string answer keeps its quotes."""
    return prime_print(giac_eval(expr, timeout))


def _string(args):
    """STRING(v [, mode [, digits]]). Mode 1 Standard ignores digits; 2 Fixed; 3
    Scientific (Lessons Learned s3). A string comes back quoted (kit, measured)."""
    v = args[0]
    if isinstance(v, CasResult):
        return v.text
    if isinstance(v, str):
        return '"%s"' % v
    if len(args) == 1 or int(args[1]) == 1:
        return _std(v)
    mode = int(args[1])
    d = int(args[2]) if len(args) > 2 else 4
    if not isinstance(v, float):
        raise Unsupported('STRING of %s with a display mode is not covered' % interp._kind(v))
    if mode == 2:
        s = '%.*f' % (d, v)
        return s
    if mode == 3:
        s = '%.*E' % (d, v)
        mant, ex = s.split('E')
        return mant + 'E' + str(int(ex))
    raise Unsupported('STRING display mode %d is not covered (1, 2, 3 are)' % mode)


# ============================================================ statistics
_ST = None


def _stats():
    global _ST
    if _ST is None:
        try:
            from scipy import stats as st
        except ImportError:
            raise Unsupported('the statistics built-ins need SciPy (pip install scipy)')
        _ST = st
    return _ST


def _isint(v):
    return isinstance(v, float) and v == math.floor(v)


class _StatFns(object):
    """HP's argument orders (HP Prime User Guide, Probability functions)."""

    def __init__(self, h):
        self.h = h

    def unver(self, fn, why):
        msg = '%s: %s -- the device has not been seen to answer this' % (fn, why)
        if self.h.on_unverified == 'raise':
            raise Unverified(msg)
        self.h.warnings.append(msg)

    def pos(self, fn, what, v):
        if not v > 0:
            self.unver(fn, '%s = %s, not > 0' % (what, _std(v)))

    def df(self, fn, v):
        """v3c: a df that the calculator takes whatever it is (STUDENT, STUDENT_CDF, STUDENT_ICDF and the
        CHISQUARE density matched SciPy at df 2.5 on the emulator, 17 Oct 2026): only df > 0 is checked."""
        self.pos(fn, 'df', v)

    def df_whole(self, fn, v):
        """v3c: CHISQUARE_CDF, CHISQUARE_ICDF, FISHER_CDF and FISHER_ICDF refuse a non-integer df with
        "Invalid input" (GfxProbe beta 1 T11 and the Home checks, emulator 17 Oct 2026): a run-time
        error, which IFERR catches -- otherwise the program stops there, as StatDist v2.6 did."""
        self.pos(fn, 'df', v)
        if not _isint(v):
            raise PPLError('%s: Invalid input (df = %s is not a whole number; the calculator\'s '
                           'chi-square and F CDF and ICDF take whole-number df only -- GfxProbe T11)'
                           % (fn, _std(v)))

    def df_unmeasured(self, fn, v):
        """v3c: the F density with a non-integer df was not among the emulator's checks."""
        self.pos(fn, 'df', v)
        if not _isint(v):
            self.h.warnings.append('%s: non-integer df %s (accepted here; the F density with a '
                                   'fractional df was not measured on the emulator)' % (fn, _std(v)))

    def k(self, fn, v):
        if not _isint(v) or v < 0:
            self.unver(fn, 'k = %s is not a whole number >= 0' % _std(v))

    def prob(self, fn, v, open_=False):
        if not (0 <= v <= 1) or (open_ and v in (0.0, 1.0)):
            self.unver(fn, 'p = %s outside %s' % (_std(v), '(0,1)' if open_ else '[0,1]'))

    def log(self, name, args, val):
        self.h.stat_calls.append((name, tuple(args), val))
        val = float(val)
        if val != val:
            raise Unverified('%s%s has no value here (SciPy answers nan)'
                             % (name, '(' + ', '.join(_std(a) for a in args) + ')'))
        return val

    # ---- normal
    def NORMALD(self, a):
        st = _stats()
        if len(a) == 1:
            mu, sg, x = 0.0, 1.0, a[0]
        elif len(a) == 3:
            mu, sg, x = a
        else:
            raise Unsupported('NORMALD takes (x) or (mu, sigma, x)')
        self.pos('NORMALD', 'sigma', sg)
        return self.log('NORMALD', a, st.norm.pdf(x, mu, sg))

    def NORMALD_CDF(self, a):
        st = _stats()
        if len(a) == 1:
            mu, sg, x1, x2 = 0.0, 1.0, None, a[0]
        elif len(a) == 2:
            mu, sg, x1, x2 = 0.0, 1.0, a[0], a[1]
        elif len(a) == 3:
            mu, sg, x1, x2 = a[0], a[1], None, a[2]
        elif len(a) == 4:
            mu, sg, x1, x2 = a
        else:
            raise Unsupported('NORMALD_CDF takes 1 to 4 arguments')
        self.pos('NORMALD_CDF', 'sigma', sg)
        v = st.norm.cdf(x2, mu, sg) - (st.norm.cdf(x1, mu, sg) if x1 is not None else 0.0)
        return self.log('NORMALD_CDF', a, v)

    def NORMALD_ICDF(self, a):
        st = _stats()
        if len(a) == 1:
            mu, sg, p = 0.0, 1.0, a[0]
        elif len(a) == 3:
            mu, sg, p = a
        else:
            raise Unsupported('NORMALD_ICDF takes (p) or (mu, sigma, p)')
        self.pos('NORMALD_ICDF', 'sigma', sg)
        self.prob('NORMALD_ICDF', p, open_=True)
        return self.log('NORMALD_ICDF', a, st.norm.ppf(p, mu, sg))

    # ---- t, chi-square, F
    def STUDENT(self, a):
        self.df('STUDENT', a[0])
        return self.log('STUDENT', a, _stats().t.pdf(a[1], a[0]))

    def STUDENT_CDF(self, a):
        st = _stats()
        self.df('STUDENT_CDF', a[0])
        if len(a) == 2:
            v = st.t.cdf(a[1], a[0])
        elif len(a) == 3:
            v = st.t.cdf(a[2], a[0]) - st.t.cdf(a[1], a[0])
        else:
            raise Unsupported('STUDENT_CDF takes (n, x) or (n, x1, x2)')
        return self.log('STUDENT_CDF', a, v)

    def STUDENT_ICDF(self, a):
        self.df('STUDENT_ICDF', a[0])
        self.prob('STUDENT_ICDF', a[1], open_=True)
        return self.log('STUDENT_ICDF', a, _stats().t.ppf(a[1], a[0]))

    def CHISQUARE(self, a):
        self.df('CHISQUARE', a[0])
        return self.log('CHISQUARE', a, _stats().chi2.pdf(a[1], a[0]))

    def CHISQUARE_CDF(self, a):
        st = _stats()
        self.df_whole('CHISQUARE_CDF', a[0])
        if len(a) == 2:
            v = st.chi2.cdf(a[1], a[0])
        elif len(a) == 3:
            v = st.chi2.cdf(a[2], a[0]) - st.chi2.cdf(a[1], a[0])
        else:
            raise Unsupported('CHISQUARE_CDF takes (n, x) or (n, x1, x2)')
        return self.log('CHISQUARE_CDF', a, v)

    def CHISQUARE_ICDF(self, a):
        self.df_whole('CHISQUARE_ICDF', a[0])
        self.prob('CHISQUARE_ICDF', a[1], open_=True)
        return self.log('CHISQUARE_ICDF', a, _stats().chi2.ppf(a[1], a[0]))

    def FISHER(self, a):
        self.df_unmeasured('FISHER', a[0]); self.df_unmeasured('FISHER', a[1])
        return self.log('FISHER', a, _stats().f.pdf(a[2], a[0], a[1]))

    def FISHER_CDF(self, a):
        st = _stats()
        self.df_whole('FISHER_CDF', a[0]); self.df_whole('FISHER_CDF', a[1])
        if len(a) == 3:
            v = st.f.cdf(a[2], a[0], a[1])
        elif len(a) == 4:
            v = st.f.cdf(a[3], a[0], a[1]) - st.f.cdf(a[2], a[0], a[1])
        else:
            raise Unsupported('FISHER_CDF takes (n, d, x) or (n, d, x1, x2)')
        return self.log('FISHER_CDF', a, v)

    def FISHER_ICDF(self, a):
        self.df_whole('FISHER_ICDF', a[0]); self.df_whole('FISHER_ICDF', a[1])
        self.prob('FISHER_ICDF', a[2], open_=True)
        return self.log('FISHER_ICDF', a, _stats().f.ppf(a[2], a[0], a[1]))

    # ---- binomial, Poisson (the 4- and 3-argument CDFs are inclusive ranges)
    def _binom_np(self, fn, n, p):
        if not _isint(n) or n < 0:
            self.unver(fn, 'n = %s is not a whole number >= 0' % _std(n))
        self.prob(fn, p)

    def BINOMIAL(self, a):
        n, p, k = a
        self._binom_np('BINOMIAL', n, p); self.k('BINOMIAL', k)
        return self.log('BINOMIAL', a, _stats().binom.pmf(k, n, p))

    def BINOMIAL_CDF(self, a):
        st = _stats()
        n, p = a[0], a[1]
        self._binom_np('BINOMIAL_CDF', n, p)
        if len(a) == 3:
            self.k('BINOMIAL_CDF', a[2])
            v = st.binom.cdf(a[2], n, p)
        elif len(a) == 4:
            self.k('BINOMIAL_CDF', a[2]); self.k('BINOMIAL_CDF', a[3])
            v = st.binom.cdf(a[3], n, p) - (st.binom.cdf(a[2] - 1, n, p) if a[2] >= 1 else 0.0)
        else:
            raise Unsupported('BINOMIAL_CDF takes (n, p, k) or (n, p, k1, k2)')
        return self.log('BINOMIAL_CDF', a, v)

    def BINOMIAL_ICDF(self, a):
        n, p, q = a
        self._binom_np('BINOMIAL_ICDF', n, p); self.prob('BINOMIAL_ICDF', q)
        return self.log('BINOMIAL_ICDF', a, _stats().binom.ppf(q, n, p))

    def POISSON(self, a):
        mu, k = a
        self.pos('POISSON', 'mu', mu); self.k('POISSON', k)
        return self.log('POISSON', a, _stats().poisson.pmf(k, mu))

    def POISSON_CDF(self, a):
        st = _stats()
        mu = a[0]
        self.pos('POISSON_CDF', 'mu', mu)
        if len(a) == 2:
            # v3c: POISSON_CDF(2, -1) and POISSON_CDF(2, -0.5) are "Invalid input" on the
            # emulator (GfxProbe T12 and the Home checks, 17 Oct 2026): a run-time error
            if a[1] < 0:
                raise PPLError('POISSON_CDF: Invalid input (k = %s < 0 -- GfxProbe T12)' % _std(a[1]))
            self.k('POISSON_CDF', a[1])
            v = st.poisson.cdf(a[1], mu)
        elif len(a) == 3:
            self.k('POISSON_CDF', a[1]); self.k('POISSON_CDF', a[2])
            v = st.poisson.cdf(a[2], mu) - (st.poisson.cdf(a[1] - 1, mu) if a[1] >= 1 else 0.0)
        else:
            raise Unsupported('POISSON_CDF takes (mu, k) or (mu, k1, k2)')
        return self.log('POISSON_CDF', a, v)

    def POISSON_ICDF(self, a):
        mu, p = a
        self.pos('POISSON_ICDF', 'mu', mu); self.prob('POISSON_ICDF', p)
        return self.log('POISSON_ICDF', a, _stats().poisson.ppf(p, mu))

    # ---- counting: exact integers, then the Prime's range
    def _count(self, fn, a, f):
        n, k = a
        if not (_isint(n) and _isint(k)) or n < 0 or k < 0:
            self.unver(fn, '(%s, %s) not whole numbers >= 0' % (_std(n), _std(k)))
        v = f(int(n), int(k)) if k <= n else 0
        if v > PRIME_MAX:
            raise PPLError('%s(%s, %s) overflows the Prime\'s real range (about 1E500)'
                           % (fn, _std(n), _std(k)))
        if v > sys.float_info.max:
            raise Unsupported('%s(%s, %s) fits the Prime (< 1E500) but not a double '
                              '(< 1.8E308)' % (fn, _std(n), _std(k)))
        return self.log(fn, a, float(v))

    def COMB(self, a):
        return self._count('COMB', a, math.comb)

    def PERM(self, a):
        return self._count('PERM', a, math.perm)


# ================================================================== harness
class Harness(interp.Machine):
    """One loaded program (or several files, loaded into one pool like the device's)
    with scripted input and a record of the output. See the module docstring."""

    def __init__(self, paths=None, idle_key=None, strict=False, stall_limit=10000,
                 seed=0, on_unverified='raise', max_screens=5000, anim_patience=2000,
                 angle='rad', app_data=None, stale_keys=False, text=None, cas='giac',
                 home_minus=False, wait_model='device', mouse_tail=False):
        interp.Machine.__init__(self)
        # v3c: how a scripted tap reaches WAIT(-1).  'device' = the emulator's answer to
        # MenuTapProbe beta 1 (17 Oct 2026): with DRAWMENU on the screen a tap at y >= 218 is
        # ONLY {3, x, y}; a tap above it is {0, x, y}, {2}, {3, x, y}.  'v3b' = the old model.
        if wait_model not in ('device', 'v3b'):
            raise ValueError("wait_model is 'device' or 'v3b'")
        self.wait_model = wait_model
        # v3c: True = a tap read by MOUSE also leaves its {2}, {3, x, y} for the next WAIT(-1)
        # (NOT measured; a worst case for testing a program's stale-click guard)
        self.mouse_tail = mouse_tail
        self._arc_warned = False
        self._strip_warned = False
        # v3b: Home's STRING() of a negative real starts with U+2212, not a hyphen (CASProbe
        # beta 1a T01, emulator 17 Oct 2026).  Off by default: fleet verify scripts read
        # screen text with hyphens.  "text" + number is not measured and is left alone.
        self.home_minus = home_minus
        self.cas_mode = cas               # 'giac', 'fail', or a dict of canned answers (v3)
        self.cas_calls = []               # (expression, Prime-printed answer, ms)
        self.cas_desktop = []             # v3b: (expression, desktop Giac's raw answer)
        self.cas_vars = collections.OrderedDict()   # v3b: CAS variables assigned, not purged
        self._cas_hist = []               # v3b: CAS texts with := replayed before each call
        self._cas_warned = set()
        self.idle_key = idle_key
        self.anim_patience = anim_patience
        self.stale_keys = stale_keys      # model the dialog's OK/Cancel press left in the buffer
        self._stale = None
        self._draws = 0                  # drawing calls so far (a wait loop draws nothing)
        self.strict = strict
        self.stall_limit = stall_limit
        self.on_unverified = on_unverified
        self.max_screens = max_screens
        self.rng = random.Random(seed)
        self.clock = 0.0
        self.files, self.notes, self.forward, self.file_locals = [], {}, [], []
        self.views = []
        self.grobs = dict(('G%d' % i, Grob('G%d' % i)) for i in range(10))
        for g, obj in self.grobs.items():
            self.globals_[g] = obj
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':          # Home's real variables
            self.globals_[c] = 0.0
        self.globals_[u'\u03c0'] = math.pi              # pi
        self.globals_['e'] = math.e
        # Home's angle setting: 0 radians (kit, measured), 1 degrees, 2 grads
        self.globals_['HAngle'] = {'rad': 0.0, 'deg': 1.0, 'grad': 2.0}[angle]
        for k, v in (app_data or {}).items():          # D1..D9 / C0..C9 columns
            self.globals_[k] = [float(x) for x in v]
        # scripted input
        self._queue = collections.deque()
        self._choices = collections.deque()
        self._answers = collections.deque()
        self._msgbox_answers = collections.deque()
        self._pending_wait = []          # the rest of a Drag / a lift, for WAIT(-1)
        self._finger = None              # MOUSE readings still to come while a finger is down
        self._down = None                # (code, loop id, last pass) for ISKEYDOWN
        self._empty = {}                 # poll site -> (loop id, pass) of its last empty answer
        self._loops = []
        self._loop_ids = itertools.count(1)
        self._fstack = []                # (function name, its parameter names)
        self._stat = _StatFns(self)
        self._table = self._build_table()
        self.reset_records()
        if paths:
            for p in ([paths] if isinstance(paths, str) else paths):
                self.load_path(p)
        if text is not None:
            self.load_text(text, '<text>')

    # ------------------------------------------------------------ records
    def reset_records(self):
        """Forget what was drawn and shown (globals and queues are kept)."""
        self.screens, self.texts, self.msgboxes, self.dialogs = [], [], [], []
        self.terminal, self.timeline, self.warnings, self.stat_calls = [], [], [], []
        self.log, self.dropped_screens, self.stale_skips = [], 0, []
        self._g0_dirty = False
        self.result, self.error = None, None

    @property
    def pages(self):
        """The screens shown by a BLIT_P to G0 -- one per composed page."""
        return [s for s in self.screens if s.reason == 'blit']

    @property
    def chooses(self):
        return [d for d in self.dialogs if isinstance(d, Choose)]

    @property
    def inputs(self):
        return [d for d in self.dialogs if isinstance(d, Input)]

    def leftover(self):
        """Scripted input the run did not use: (events, choose answers, input answers)."""
        return list(self._queue), list(self._choices), list(self._answers)

    # ------------------------------------------------------------ loading
    def load_text(self, text, filename='<ppl>'):
        src, notes = preprocess(text)
        p = _Parser(interp.lex(src), filename)
        funcs, globs = p.program()
        self.funcs.update(funcs)
        self.forward += p.forward
        self.file_locals += p.file_locals
        self.views += p.views
        self.notes[filename] = notes
        for name, init in globs:
            self.globals_[name] = self.evaluate(init, {}) if init is not None else 0.0
        missing = [f for f in p.forward if f not in self.funcs]
        if missing:
            self.warnings.append('%s: forward-declared but never defined: %s'
                                 % (filename, ', '.join(missing)))
        return self

    def load_path(self, path):
        with open(path, encoding='utf-8-sig') as fh:
            self.load_text(fh.read(), os.path.basename(path))
        self.files.append(path)
        return self

    # ------------------------------------------------------------ scripting
    def press(self, *codes, **kw):
        """Queue key presses (codes or names from KEY). hold=n: see Key."""
        for c in codes:
            self._queue.append(Key(KEY[c] if isinstance(c, str) else c, kw.get('hold', 0),
                                   kw.get('anytime', False)))
        return self

    def tap(self, x, y, lift=False, hold=0, anytime=False):
        self._queue.append(Tap(x, y, lift, hold, anytime))
        return self

    def drag(self, points, lift=True, anytime=False):
        self._queue.append(Drag(points, lift, anytime))
        return self

    def timeout(self):
        self._queue.append(Timeout())
        return self

    def event(self, *evs):
        self._queue.extend(evs)
        return self

    def choose(self, *answers):
        """Queue CHOOSE answers: an index (0 = cancel) or an item's label."""
        self._choices.extend(answers)
        return self

    def answer(self, *answers):
        """Queue INPUT answers: {name: value}, a list by position (None = leave the
        field), ACCEPT, or CANCEL."""
        self._answers.extend(answers)
        return self

    def msgbox_answer(self, *oks):
        """Only for MSGBOX(text, 1) (OK/Cancel boxes): True = OK."""
        self._msgbox_answers.extend(oks)
        return self

    # ------------------------------------------------------------ running
    def call(self, name, *args):
        args = tuple(float(a) if isinstance(a, int) and not isinstance(a, bool) else a
                     for a in args)
        params = set(self.funcs[name][0]) if name in self.funcs else set()
        top = not self._fstack
        self._fstack.append((name, params))
        try:
            r = interp.Machine.call(self, name, *args)
            if top:
                self._capture_if_dirty('end')
                self.result = r
            return r
        except Exception as e:
            if not hasattr(e, 'ppl_stack'):
                e.ppl_stack = [f for f, _ in self._fstack]
            if top:
                self.error = e
                self._capture_if_dirty('end')
            raise
        finally:
            self._fstack.pop()

    def execute(self, expr):
        """Evaluate a call written as PPL text, e.g. 'POWERVIZ()' or 'Norm3(0,1,1.96)'."""
        p = interp.Parser(interp.lex(preprocess(expr)[0]), '<call>')
        tree = p.expr()
        if not p.at('EOF'):
            raise Unsupported('%r after the expression' % p.peek().val)
        if tree[0] == 'call' and tree[1][0] == 'var' and tree[1][1] in self.funcs:
            return self.call(tree[1][1], *[self.evaluate(a, {}) for a in tree[2]])
        if tree[0] == 'var' and tree[1] in self.funcs:
            return self.call(tree[1])
        return self.evaluate(tree, {})

    def _where(self):
        return self._fstack[-1][0] if self._fstack else '<top>'

    # ------------------------------------------------------------ loops
    def _stmt(self, s, frame):
        kind = s[0]
        if kind not in ('repeat', 'while', 'for'):
            return interp.Machine._stmt(self, s, frame)
        loop = _Loop(next(self._loop_ids), self._where())
        self._loops.append(loop)
        try:
            return getattr(self, '_loop_' + kind)(s, frame, loop)
        finally:
            self._loops.pop()
            if loop.stale_iter is not None and loop.stale_iter == loop.iter:
                # the loop ended in the pass that read the dialog's left-over key:
                # a wait that was satisfied by it -- the page was skipped
                self._stale_skip('a wait loop in %s ended on the key left over from the '
                                 'last dialog: the page it held was skipped' % loop.func)

    def _pass(self, loop, word):
        loop.iter += 1
        if loop.iter > interp.LOOP_LIMIT:
            raise Unsupported(interp._endless(word))

    def _loop_repeat(self, s, frame, loop):
        last = None
        while True:
            self._pass(loop, 'REPEAT')
            try:
                v = self.run(s[1], frame)
                if v is not None:
                    last = v
            except interp._Break as b:
                if b.levels > 1:
                    raise interp._Break(b.levels - 1)
                break
            except interp._Continue:
                pass
            if interp._truth(self.evaluate(s[2], frame)):
                break
        return last

    def _loop_while(self, s, frame, loop):
        last = None
        while True:
            self._pass(loop, 'WHILE')
            if not interp._truth(self.evaluate(s[1], frame)):
                break
            try:
                v = self.run(s[2], frame)
                if v is not None:
                    last = v
            except interp._Break as b:
                if b.levels > 1:
                    raise interp._Break(b.levels - 1)
                break
            except interp._Continue:
                continue
        return last

    def _loop_for(self, s, frame, loop):
        _, var, init, enders, step, direction, body = s
        i = self.evaluate(init, frame)
        limit = self.evaluate(enders, frame)
        inc = self.evaluate(step, frame) if step is not None else 1.0
        inc = abs(inc) * direction
        last = None
        while (inc > 0 and i <= limit) or (inc < 0 and i >= limit):
            self._pass(loop, 'FOR')
            frame[var] = i
            try:
                v = self.run(body, frame)
                if v is not None:
                    last = v
            except interp._Break as b:
                if b.levels > 1:
                    raise interp._Break(b.levels - 1)
                break
            except interp._Continue:
                pass
            i = frame[var] + inc
        return last

    # ------------------------------------------------------------ dispatch
    def evaluate(self, e, frame):
        if e[0] == 'var':
            name = e[1]
            if name not in frame and name not in self.globals_ and name not in self.funcs:
                up = name.upper()
                if up == 'GETKEY':
                    return self._getkey(id(e))
                if up == 'MOUSE':
                    return self._mouse(id(e), None)
                if up == 'TICKS':
                    return self._ticks()
                if up == 'RANDOM':                       # v2: bare RANDOM, as the fleet writes it
                    return self._random([])
                if re.fullmatch(r'[CD][0-9]', name):
                    raise PPLError('%s does not exist until its Statistics app has been '
                                   'opened (preset it with app_data={%r: [...]})' % (name, name))
        return interp.Machine.evaluate(self, e, frame)

    def _assign(self, target, value, frame):
        # v2: the Prime COPIES a list or matrix on assignment (a := b; a(1) := 9 leaves b
        # alone); the kit's interpreter shared the Python list, so v1 could hide or invent
        # aliasing bugs.  Copy here so the harness behaves like the calculator.
        if isinstance(value, list):
            value = copy.deepcopy(value)
        return interp.Machine._assign(self, target, value, frame)

    def _call_node(self, e, frame):
        base, arg_nodes = e[1], e[2]
        if base[0] == 'var':
            name = base[1]
            if name not in frame and name not in self.globals_ and name not in self.funcs:
                up = name.upper()
                if up == 'INPUT':
                    return self._input(arg_nodes, frame)
                if up == 'CHOOSE':
                    return self._choose(arg_nodes, frame)
                if up == 'CAS':                          # v3b: literal or not decides
                    return self._cas_node(arg_nodes, frame, id(e))
                if up == 'PYTHON':                       # PYTHON(blockname, args...)
                    first = (arg_nodes[0][1] if arg_nodes and arg_nodes[0][0] == 'var'
                             else self.evaluate(arg_nodes[0], frame))
                    return self._python([first] + [self.evaluate(a, frame)
                                                    for a in arg_nodes[1:]])
                fn = self._table.get(up)
                if fn is not None:
                    args = [self.evaluate(a, frame) for a in arg_nodes]
                    try:
                        return fn(args, id(e))
                    except Unverified as x:              # name the call, arguments and all
                        call = '%s(%s)' % (up, ', '.join(_std(v) for v in args))
                        msg = str(x)
                        if msg.startswith(call):
                            raise
                        if msg.startswith(up + ': '):
                            msg = msg[len(up) + 2:]
                        raise Unverified('%s: %s' % (call, msg))
                    except interp.PYTHON_FAILURES as x:
                        raise Unsupported('%s given %s is not covered (%s)' % (
                            up, ', '.join(interp._kind(a) for a in args) or 'nothing', x))
        return interp.Machine._call_node(self, e, frame)

    def _arith(self, op, a, b):
        if op == '+' and (isinstance(a, str) or isinstance(b, str)):
            return _std(a) + _std(b)          # Home's Standard format, not Python's repr
        return interp.Machine._arith(self, op, a, b)

    def _build_table(self):
        st = self._stat
        t = {}
        for n in ('NORMALD', 'NORMALD_CDF', 'NORMALD_ICDF', 'STUDENT', 'STUDENT_CDF',
                  'STUDENT_ICDF', 'CHISQUARE', 'CHISQUARE_CDF', 'CHISQUARE_ICDF',
                  'FISHER', 'FISHER_CDF', 'FISHER_ICDF', 'BINOMIAL', 'BINOMIAL_CDF',
                  'BINOMIAL_ICDF', 'POISSON', 'POISSON_CDF', 'POISSON_ICDF', 'COMB', 'PERM'):
            t[n] = (lambda f: lambda a, site: f(a))(getattr(st, n))
        t.update({
            'STRING': lambda a, site: self._string_home(a),
            'CAS': lambda a, site: self._cas(a),
            'EXPR': lambda a, site: self._expr(a),
            'POS': lambda a, site: float((_string([a[0]]) if not isinstance(a[0], str) else a[0]).find(
                a[1] if isinstance(a[1], str) else _string([a[1]])) + 1),
            'INSTRING': lambda a, site: float(a[0].find(a[1]) + 1),
            'CHAR': lambda a, site: (''.join(chr(int(c)) for c in a[0])
                                     if isinstance(a[0], list) else chr(int(a[0]))),
            'ASC': lambda a, site: [float(ord(c)) for c in a[0]],
            'TYPE': lambda a, site: self._type(a[0]),
            'TRUNCATE': lambda a, site: float(math.trunc(a[0] * 10 ** int(a[1])) / 10 ** int(a[1])),
            'RANDOM': lambda a, site: self._random(a),
            'RANDINT': lambda a, site: self._randint(a),
            'GETKEY': lambda a, site: self._getkey(site),
            'MOUSE': lambda a, site: self._mouse(site, a[0] if a else None),
            'ISKEYDOWN': lambda a, site: self._iskeydown(site, int(a[0])),
            'WAIT': lambda a, site: self._wait(a),
            'TICKS': lambda a, site: self._ticks(),
            'MSGBOX': lambda a, site: self._msgbox(a),
            'PRINT': lambda a, site: self._print(a),
            'TEXTOUT_P': lambda a, site: self._textout(a, 'TEXTOUT_P'),
            'TEXTOUT': lambda a, site: self._textout(a, 'TEXTOUT'),
            'DIMGROB_P': lambda a, site: self._dimgrob(a),
            'BLIT_P': lambda a, site: self._blit(a),
            'RECT_P': lambda a, site: self._rect(a, 'RECT_P'),
            'RECT': lambda a, site: self._rect(a, 'RECT'),
            'DRAWMENU': lambda a, site: self._drawmenu(a),
            'GROBW_P': lambda a, site: float(a[0].w),
            'GROBH_P': lambda a, site: float(a[0].h),
            'GETPIX_P': lambda a, site: float(self._grob_args(a)[0].bg or 0),
            'SUB': lambda a, site: self._sub(a),
            'ALOG': lambda a, site: 10.0 ** a[0],
            'MEAN': lambda a, site: self._mean(a),
            'SIN': lambda a, site: math.sin(self._to_rad(a[0])),
            'COS': lambda a, site: math.cos(self._to_rad(a[0])),
            'TAN': lambda a, site: math.tan(self._to_rad(a[0])),
            'ASIN': lambda a, site: self._from_rad(math.asin(a[0])),
            'ACOS': lambda a, site: self._from_rad(math.acos(a[0])),
            'ATAN': lambda a, site: self._from_rad(math.atan(a[0])),
        })
        for n in ('LINE_P', 'LINE', 'PIXON_P', 'PIXON', 'ARC', 'INVERT_P',
                  'SUBGROB_P', 'FREEZE', 'STARTAPP', 'STARTVIEW', 'CHECK', 'UNCHECK'):
            t[n] = (lambda nm: lambda a, site: self._shape(nm, a))(n)
        # v3c: FILLPOLY_P (both forms) and the 2-D TRIANGLE_P (one colour, blended, alpha) passed
        # GfxProbe T01-T06 on the emulator; only the 3-D mesh form (a matrix argument, T07: drew
        # nothing) still warns.  ARC_P warns once per run at r <= 3 (T09: holes in a solid dot).
        t['FILLPOLY_P'] = lambda a, site: self._shape('FILLPOLY_P', a)
        t['TRIANGLE_P'] = lambda a, site: self._shape(
            'TRIANGLE_P', a, warn=any(isinstance(v, interp.Matrix) for v in a))
        t['ARC_P'] = lambda a, site: self._arc(a)
        return t

    # ------------------------------------------------------------ small built-ins
    def _type(self, v):
        if isinstance(v, float):
            return 0.0
        if isinstance(v, str):
            return 2.0
        if isinstance(v, interp.Matrix):
            return 4.0
        if isinstance(v, list):
            return 6.0
        if isinstance(v, CasResult):     # v3b: a CAS object (the kit measured TYPE 8; CASProbe T05)
            return 8.0
        raise Unsupported('TYPE of %r is not covered' % (v,))

    def _angle_unit(self):
        return {0.0: 1.0, 1.0: math.pi / 180, 2.0: math.pi / 200}.get(
            self.globals_.get('HAngle', 0.0), 1.0)

    def _to_rad(self, v):
        return v * self._angle_unit()

    def _from_rad(self, v):
        return v / self._angle_unit()

    def _sub(self, a):
        obj, i, j = a[0], int(a[1]), int(a[2])
        if not isinstance(obj, (list, str)):
            raise Unsupported('SUB of %s is not covered' % interp._kind(obj))
        if i < 1 or j > len(obj) or i > j + 1:
            raise Unverified('SUB(%s, %d, %d) on %d items: an out-of-range SUB has not been '
                             'observed' % (interp._kind(obj), i, j, len(obj)))
        return obj[i - 1:j]

    def _mean(self, a):
        v = a[0]
        if len(a) != 1 or not isinstance(v, list) or not v:
            raise Unsupported('mean of anything but one non-empty list is not covered')
        return float(sum(v)) / len(v)

    def _cas(self, a):
        """CAS(...) reached through the table: a literal text (the parser's path for
        CAS("...") and EXPR's), evaluated."""
        if len(a) != 1 or not isinstance(a[0], str):
            raise Unsupported('the harness covers CAS("expression text") only')
        return self._cas_eval(a[0])

    def _string_home(self, a):
        r = _string(a)
        if (self.home_minus and a and isinstance(a[0], float) and a[0] < 0
                and isinstance(r, str) and r.startswith('-')):
            r = u'\u2212' + r[1:]
        return r

    def _cas_node(self, arg_nodes, frame, site):
        """v3b: CAS(x) as the emulator answered it (CASProbe beta 1a T04/T06/T07, 17 Oct 2026).
        A literal string is evaluated; anything else -- a variable, a parameter, a
        concatenation -- is handed back unevaluated: the PPL string itself."""
        if len(arg_nodes) != 1:
            raise Unsupported('the harness covers CAS with one argument only')
        node = arg_nodes[0]
        if node[0] == 'str':
            return self._table['CAS']([node[1]], site)
        v = self.evaluate(node, frame)
        if isinstance(v, str):
            self.cas_calls.append((v, '(unevaluated: CAS of a non-literal)', 0.0))
            self.cas_desktop.append((v, '(not sent)'))
            if 'nonliteral' not in self._cas_warned:
                self._cas_warned.add('nonliteral')
                self.warnings.append('CAS(%s) has a non-literal argument: on the calculator the '
                                     'text comes back UNEVALUATED (CASProbe beta 1a T06/T07). Use '
                                     'EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")")'
                                     % ('a variable' if node[0] == 'var' else 'an expression'))
            return v
        raise Unsupported('CAS of a %s (not text) is not covered' % interp._kind(v))

    def _expr(self, a):
        """v3b: EXPR, with the dotted CAS forms the kit's parser cannot read:
        CAS.eval("...") and CAS.name(args) are the CAS evaluating the text."""
        t = a[0] if a else None
        if isinstance(t, str):
            m = re.fullmatch(r'\s*CAS\.eval\s*\(\s*"([^"]*)"\s*\)\s*', t)
            if m:
                return self._table['CAS']([m.group(1)], None)
            m = re.fullmatch(r'\s*CAS\.([A-Za-z_]\w*)\s*\(([^"]*)\)\s*', t, re.S)
            if m:
                return self._table['CAS']([m.group(1) + '(' + m.group(2) + ')'], None)
        return interp._b_expr(self, a)

    _CAS_SENT = '__ppl_run_v3c_history__'

    def _cas_eval(self, expr):
        """Evaluate one CAS text and hand back what PPL receives (v3b):
        a PPL string for a CAS string, a real for a non-string integer over 12 digits,
        else a CasResult (TYPE 8) printed as the Prime prints it."""
        t0 = time.time()
        expr = expr.replace(u'\u2212', '-')      # the CAS reads Home's minus (CASProbe T31b)
        if self.cas_mode == 'fail':
            self.cas_calls.append((expr, 'FAILED (cas=fail)', 0.0))
            self.cas_desktop.append((expr, 'FAILED (cas=fail)'))
            raise PPLError('CAS call failed (harness cas=fail)')
        if isinstance(self.cas_mode, dict):
            if expr not in self.cas_mode:
                raise HarnessScriptError('no canned CAS answer for %r' % expr)
            raw = self.cas_mode[expr]
        elif self._cas_hist:
            body = ';\n'.join(self._cas_hist) + ';\n"' + self._CAS_SENT + '";\n' + expr
            out = giac_eval(body)
            k = out.rfind('"' + self._CAS_SENT + '"')
            raw = out if k < 0 else re.sub(r'^\s*,?\s*', '', out[k + len(self._CAS_SENT) + 2:])
        else:
            raw = giac_eval(expr)
        ms = (time.time() - t0) * 1000.0
        self.cas_desktop.append((expr, raw))
        if 'Error:' in raw or raw == '':
            self.cas_calls.append((expr, raw, ms))
            raise PPLError('CAS error: %s' % raw.replace('\n', ' ')[:160])
        txt = prime_print(raw)
        self.cas_calls.append((expr, txt, ms))
        self._cas_track(expr)
        if len(txt) >= 2 and txt[0] == '"' and txt[-1] == '"':
            return txt[1:-1]                       # a PPL string (TYPE 2)
        if re.fullmatch(r'-?\d{13,}', txt):        # a big integer, not a string: a real
            v = float(txt)
            if v in (float('inf'), float('-inf')):
                raise Unsupported('a %d-digit CAS integer as a real is past a double '
                                  '(the Prime reaches 1E500)' % len(txt.lstrip('-')))
            return v
        return CasResult(txt)

    def _cas_track(self, expr):
        """v3b: CAS variables persist (CASProbe beta 1b T25): remember := texts, forget on purge."""
        for nm in re.findall(r'purge\(\s*([A-Za-z_]\w*)\s*\)', expr):
            self.cas_vars.pop(nm, None)
            self._cas_hist = [x for x in self._cas_hist
                              if nm not in re.findall(r'([A-Za-z_]\w*)\s*:=', x)]
        names = re.findall(r'([A-Za-z_]\w*)\s*:=', expr)
        if names:
            if self.cas_mode == 'giac':
                self._cas_hist.append(expr)
            for nm in names:
                self.cas_vars[nm] = expr
                if nm not in self._cas_warned:
                    self._cas_warned.add(nm)
                    self.warnings.append('CAS text assigns %s: it persists into later calls and '
                                         'into the student\'s CAS until purge(%s) (CASProbe T25)'
                                         % (nm, nm))

    def _random(self, a):
        if not a:
            return self.rng.random()
        if len(a) == 2:
            return a[0] + (a[1] - a[0]) * self.rng.random()
        raise Unsupported('RANDOM with %d arguments is not covered' % len(a))

    def _randint(self, a):
        if len(a) == 2:
            return float(self.rng.randint(int(a[0]), int(a[1])))
        raise Unsupported('RANDINT with %d arguments is not covered' % len(a))

    def _ticks(self):
        self.clock += 1.0                    # one millisecond per reading
        return self.clock

    def _print(self, a):
        if not a:
            self.terminal = []
        else:
            self.terminal.append(_std(a[0]))
        self.log.append(('PRINT', a))
        return 0.0

    def _python(self, a):
        self.log.append(('PYTHON', a))
        self.timeline.append(('python', a, self._where()))
        self.warnings.append('PYTHON(%s) did nothing here, as on the device when the Python '
                             'side fails: the PPL fallback runs' % ', '.join(_std(x) for x in a))
        return 0.0

    # ------------------------------------------------------------ drawing
    def _grob_args(self, a):
        if a and isinstance(a[0], Grob):
            return a[0], list(a[1:])
        return self.grobs['G0'], list(a)

    def _touch(self, g):
        self._draws += 1
        if g.name == 'G0':
            self._g0_dirty = True

    def _textout(self, a, cmd):
        text = a[0]
        if len(a) > 1 and isinstance(a[1], Grob):
            g, rest = a[1], list(a[2:])
        else:
            g, rest = self.grobs['G0'], list(a[1:])
        rest += [None] * (6 - len(rest))
        x, y, font, color, width, bg = rest[:6]
        s = text if isinstance(text, str) else _std(text)
        t = Text(s, x, y, font, color, width, bg, g.name, self._where())
        g.items.append(t)
        self.texts.append(t)
        self._touch(g)
        self.log.append((cmd, a))
        return float(x or 0) + t.est_width

    def _dimgrob(self, a):
        g = a[0]
        if not isinstance(g, Grob):
            raise Unsupported('DIMGROB_P on %r' % (g,))
        g.items, g.menu = [], None
        g.w, g.h = a[1], a[2]
        g.bg = a[3] if len(a) > 3 and isinstance(a[3], float) else 0xFFFFFF
        self._touch(g)
        self.log.append(('DIMGROB_P', a))
        return 0.0

    def _rect(self, a, cmd):
        g, rest = self._grob_args(a)
        if len(rest) <= 1:                        # RECT_P([G] [, colour]): clear
            g.items, g.menu = [], None
            g.bg = rest[0] if rest else 0xFFFFFF
        else:
            g.items.append(Shape(cmd, rest, g.name))
        self._touch(g)
        self.log.append((cmd, a))
        return 0.0

    def _shape(self, cmd, a, warn=False):
        g, rest = self._grob_args(a)
        g.items.append(Shape(cmd, rest, g.name))
        self._touch(g)
        self.log.append((cmd, a))
        if warn:
            self.warnings.append('%s in its 3-D mesh form drew nothing on the emulator (GfxProbe T07)'
                                 % cmd)
        return 0.0

    def _arc(self, a):
        """v3c: ARC_P, recorded like any shape.  GfxProbe T09 (emulator, 17 Oct 2026): ARC_P at
        r = 3, 2, 1 plus the centre pixel, meant as a solid dot, shows a white X -- concentric
        circles leave holes on the diagonals.  One warning per run for a radius of 3 or less."""
        g, rest = self._grob_args(a)
        if (not self._arc_warned and len(rest) >= 3 and isinstance(rest[2], float)
                and rest[2] <= 3):
            self._arc_warned = True
            self.warnings.append('ARC_P with r = %s: a small circle drawn as a solid dot leaves '
                                 'diagonal holes (GfxProbe T09); fill it with RECT_P or FILLPOLY_P'
                                 % _std(rest[2]))
        return self._shape('ARC_P', a)

    def _blit(self, a):
        gi = [i for i, v in enumerate(a) if isinstance(v, Grob)]
        if not gi:
            raise Unsupported('BLIT_P without a graphic')
        if len(gi) == 1:
            trg, src, si = self.grobs['G0'], a[gi[0]], gi[0]
        else:
            trg, src, si = a[gi[0]], a[gi[1]], gi[1]
        offs = [v for v in a[(gi[0] + 1 if len(gi) > 1 else 0):si] if isinstance(v, float)]
        # v3c: the 10-argument scaled form passed GfxProbe T08 on the emulator (exactly 2x): no warning
        dx, dy = (offs + [0.0, 0.0])[:2]
        if dx == 0 and dy == 0:
            trg.items = list(src.items)
            trg.menu = None
        else:
            for it in src.items:
                if isinstance(it, Text):
                    trg.items.append(Text(it.text, it.x + dx, it.y + dy, it.font, it.color,
                                          it.width, it.bg, trg.name, it.func))
                else:
                    trg.items.append(Shape(it.cmd, it.args, trg.name))
        self.log.append(('BLIT_P', a))
        self._draws += 1
        if trg.name == 'G0':
            self._capture('blit')
        return 0.0

    def _drawmenu(self, a):
        labels = a[0] if len(a) == 1 and isinstance(a[0], list) else a
        self.grobs['G0'].menu = [_std(x) for x in labels]
        self._g0_dirty = True
        self._draws += 1
        self.log.append(('DRAWMENU', a))
        return 0.0

    def _capture(self, reason):
        g0 = self.grobs['G0']
        s = Screen(list(g0.items), list(g0.menu) if g0.menu else None, reason,
                   self._where(), len(self.screens) + self.dropped_screens + 1)
        self.screens.append(s)
        if len(self.screens) > self.max_screens:
            self.screens.pop(0)
            self.dropped_screens += 1
        self.timeline.append(('screen', s))
        self._g0_dirty = False

    def _capture_if_dirty(self, reason):
        if self._g0_dirty:
            self._capture(reason)

    # ------------------------------------------------------------ dialogs
    def _msgbox(self, a):
        self._capture_if_dirty('dialog')
        text = a[0] if isinstance(a[0], str) else _std(a[0])
        m = MsgBox(text, self._where())
        self.msgboxes.append(m)
        self.timeline.append(('msgbox', m))
        self.log.append(('MSGBOX', a))
        ok = True
        if len(a) > 1 and interp._truth(a[1]):
            ok = self._msgbox_answers.popleft() if self._msgbox_answers else True
        self._dialog_closed(ok)
        return 1.0 if ok else 0.0

    def _choose(self, nodes, frame):
        self._capture_if_dirty('dialog')
        if not nodes or nodes[0][0] != 'var':
            raise PPLError("CHOOSE's first argument must be a variable name")
        var = nodes[0][1]
        vals = [self.evaluate(n, frame) for n in nodes[1:]]
        title = _std(vals[0]) if vals else ''
        items = vals[1] if len(vals) == 2 and isinstance(vals[1], list) else vals[1:]
        items = [_std(i) if not isinstance(i, list) else _std(i[0]) for i in items]
        if self._choices:
            ans = self._choices.popleft()
        elif self.strict:
            raise HarnessStall('CHOOSE %r (in %s) and no answer queued; items: %s'
                               % (title, self._where(), items))
        else:
            ans = 0
        if isinstance(ans, str):
            hits = [k + 1 for k, it in enumerate(items) if it == ans]
            if not hits:
                hits = [k + 1 for k, it in enumerate(items) if ans.lower() in it.lower()]
            if len(hits) != 1:
                raise HarnessScriptError('CHOOSE %r: %r matches %d of %s'
                                         % (title, ans, len(hits), items))
            idx = hits[0]
        else:
            idx = int(ans)
        if not 0 <= idx <= len(items):
            raise HarnessScriptError('CHOOSE %r has %d items; answer %d'
                                     % (title, len(items), idx))
        if idx > 0:
            self._assign(('var', var), float(idx), frame)
        c = Choose(title, items, idx, self._where())
        self.dialogs.append(c)
        self.timeline.append(('choose', c))
        self._dialog_closed(idx > 0)
        return 1.0 if idx > 0 else 0.0

    def _input(self, nodes, frame):
        self._capture_if_dirty('dialog')
        if not nodes:
            raise PPLError('INPUT needs a variable')
        first = nodes[0]
        elems = first[1] if first[0] == 'seq' else [first]
        names = []
        for el in elems:
            if el[0] == 'seq' and el[1] and el[1][0][0] == 'var':
                el = el[1][0]                          # {var, types, position}
            if el[0] != 'var':
                raise PPLError("INPUT's first argument must be a list of variable NAMES "
                               "(the device says Invalid Input)")
            names.append(el[1])
        vals = [self.evaluate(n, frame) for n in nodes[1:]]
        title = _std(vals[0]) if vals else ''
        labels = vals[1] if len(vals) > 1 else None
        helps = vals[2] if len(vals) > 2 else None
        before = dict((n, frame.get(n, self.globals_.get(n))) for n in names)
        if self._answers:
            ans = self._answers.popleft()
        elif self.strict:
            raise HarnessStall('INPUT %r (in %s) and no answer queued; fields: %s'
                               % (title, self._where(), names))
        else:
            ans = ACCEPT
        accepted = ans is not CANCEL
        params = self._fstack[-1][1] if self._fstack else set()
        if accepted and ans is not ACCEPT:
            if isinstance(ans, dict):
                pairs = []
                for k, v in ans.items():
                    hit = [n for n in names if n == k] or [n for n in names if n.lower() == k.lower()]
                    if not hit:
                        raise HarnessScriptError('INPUT %r has fields %s; the answer names %r'
                                                 % (title, names, k))
                    pairs.append((hit[0], v))
            else:
                ans = list(ans)
                if len(ans) > len(names):
                    raise HarnessScriptError('INPUT %r has %d fields; %d values given'
                                             % (title, len(names), len(ans)))
                pairs = [(n, v) for n, v in zip(names, ans) if v is not None]
            for n, v in pairs:
                v = float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else v
                if n in params:
                    self.warnings.append('INPUT into the parameter %r of %s: on the device '
                                         'the value is not written back' % (n, self._where()))
                    continue
                self._assign(('var', n), v, frame)
        after = dict((n, frame.get(n, self.globals_.get(n))) for n in names)
        rec = Input(title, names, labels, helps, before, after, accepted, self._where())
        self.dialogs.append(rec)
        self.timeline.append(('input', rec))
        self._dialog_closed(accepted)
        return 1.0 if accepted else 0.0

    # ------------------------------------------------------------ keys and touch
    def _poll(self, site, kind, code=None):
        """A non-blocking read (GETKEY, MOUSE, ISKEYDOWN) at one call site. A queued
        event is handed over only when the program is WAITING: this same site, in the
        same running loop, already answered 'nothing' on an earlier pass, and nothing
        has been drawn since. A drain loop leaves after its first 'nothing', so it can
        never eat a scripted event (on the device the key is pressed after the drain);
        an animation that polls for Esc draws on every pass, so it is not handed the key
        meant for the page after it -- unless the event says anytime=True, or the
        animation has run anim_patience passes with the event waiting."""
        if self._finger is not None and kind != 'mouse':
            return None
        loop = self._loops[-1] if self._loops else None
        if kind == 'key' and self._stale is not None:
            ev, self._stale = self._stale, None
            self._capture_if_dirty('skipped?')
            self.timeline.append(('event', 'left-over %r from the dialog' % ev, self._where()))
            if loop is not None:
                loop.stale_iter = loop.iter
            return ev
        prev = self._empty.get(site)
        if loop is not None and prev is not None and prev[0] == loop.id and prev[1] < loop.iter:
            idle_now = prev[2] == self._draws
            ev = self._queue[0] if self._queue else None
            if ev is None and kind == 'key' and self.idle_key is not None and idle_now:
                ev = Key(self.idle_key)
                ev.idle = True
                self._queue.appendleft(ev)
            if ev is not None and ev.accepts(kind, code):
                if idle_now or getattr(ev, 'anytime', False) or loop.blocked >= self.anim_patience:
                    self._queue.popleft()
                    self._empty.clear()
                    self._deliver(ev, loop)
                    return ev
                loop.blocked += 1
            elif idle_now:
                loop.waiting += 1
                if loop.waiting > self.stall_limit:
                    raise HarnessStall(self._stall_text(kind, ev))
        if loop is not None:
            self._empty[site] = (loop.id, loop.iter, self._draws)
        return None

    def _stale_skip(self, msg):
        self.stale_skips.append(msg)
        self.timeline.append(('skip', msg))

    def _dialog_closed(self, ok):
        if self.stale_keys:
            self._stale = Key(KEY['Enter'] if ok else KEY['Esc'])

    def _stall_text(self, kind, ev):
        what = {'key': 'GETKEY', 'mouse': 'MOUSE', 'down': 'ISKEYDOWN'}[kind]
        if ev is None:
            return ('%s is waiting (polled by %s) and the event queue is empty -- queue a '
                    'key or tap, or pass idle_key' % (self._where(), what))
        return ('%s is waiting (polled by %s) but the next queued event is %r, which that '
                'loop does not read' % (self._where(), what, ev))

    def _deliver(self, ev, loop):
        self._capture_if_dirty('wait')
        self.timeline.append(('event', ev, self._where()))
        if isinstance(ev, Key):
            self._down = (ev.code, loop.id, loop.iter + ev.hold) if loop else None
        elif isinstance(ev, (Tap, Drag)):
            self._finger = ev.readings()
            # v3c, mouse_tail=True (NOT measured): the tap's click also waits for the next WAIT(-1)
            if self.mouse_tail and isinstance(ev, Tap) and self.wait_model == 'device':
                self._pending_wait += self._tap_tail(ev)

    def _menu_shown(self):
        """v3c: is a DRAWMENU strip on the screen?  DRAWMENU sets it; a BLIT_P to G0, a DIMGROB_P
        of G0 or a clear of G0 paints over it."""
        return bool(self.grobs['G0'].menu)

    def _tap_tail(self, ev):
        """v3c: what WAIT(-1) still has to hand out after a tap's first event (MenuTapProbe beta 1):
        nothing more for a soft-key tap (it was the click itself), else the lift and the click."""
        if ev.y >= 218 and self._menu_shown():
            return [[3.0, ev.x, ev.y]]
        return [[2.0], [3.0, ev.x, ev.y]]

    def _getkey(self, site):
        ev = self._poll(site, 'key')
        return float(ev.code) if ev is not None else -1.0

    def _iskeydown(self, site, code):
        loop = self._loops[-1] if self._loops else None
        d = self._down
        if d and d[0] == code and loop is not None and d[1] == loop.id and loop.iter <= d[2]:
            return 1.0
        return 1.0 if self._poll(site, 'down', code) is not None else 0.0

    def _mouse(self, site, idx):
        if self._finger is None:
            self._poll(site, 'mouse')
        reading = None
        if self._finger is not None:
            if self._finger:
                reading = self._finger.pop(0)
            else:
                self._finger = None                     # the finger lifts
        if idx is None:
            return [list(reading) if reading else [], []]
        if int(idx) == 2:
            self.warnings.append('MOUSE(2), a second finger, is not device-verified yet')
            return -1.0
        if int(idx) != 1:
            raise Unsupported('MOUSE(%s)' % _std(idx))
        return list(reading) if reading else -1.0

    def _wait(self, a):
        n = a[0] if a else None
        if n is None or n == 0:
            raise Unsupported('WAIT() / WAIT(0): not established here; use WAIT(-1) or GETKEY')
        if n > 0:
            self.clock += n * 1000.0
            self.log.append(('WAIT', a))
            return 0.0
        self._capture_if_dirty('wait')
        if self._stale is not None:
            ev, self._stale = self._stale, None
            self._stale_skip('WAIT(-1) in %s answered the key left over from the last '
                             'dialog: the page it held was skipped' % self._where())
            return float(ev.code)
        if self._pending_wait:
            v = self._pending_wait.pop(0)
            self.timeline.append(('event', 'WAIT(-1) touch list %s' % _std(v),
                                  self._where() + ' WAIT(-1)'))
            return v
        if not self._queue:
            if self.idle_key is None:
                raise HarnessStall('WAIT(-1) in %s with an empty event queue (on the device '
                                   'it times out after about 60 s and answers -1: queue '
                                   'Timeout() for that)' % self._where())
            ev = Key(self.idle_key)
            ev.idle = True
        else:
            ev = self._queue.popleft()
        self._empty.clear()
        self.timeline.append(('event', ev, self._where() + ' WAIT(-1)'))
        if isinstance(ev, Key):
            return float(ev.code)
        if isinstance(ev, Timeout):
            return -1.0
        if isinstance(ev, Tap):
            if self.wait_model == 'device':
                # v3c (MenuTapProbe beta 1, emulator 17 Oct 2026): a tap ALWAYS lifts.  On the
                # soft-key strip with DRAWMENU shown it is only {3, x, y}; anywhere else it is
                # {0, x, y}, then {2}, then {3, x, y}.  (`lift` and `hold` do not change this; a
                # finger that stays down is Drag([(x, y)], lift=False).)
                if ev.y >= 218 and self._menu_shown():
                    return [3.0, ev.x, ev.y]
                if ev.y >= 218 and not self._strip_warned:
                    self._strip_warned = True
                    self.warnings.append('a tap at y >= 218 with no DRAWMENU on the screen: modelled '
                                         'as {0}, {2}, {3} like any tap -- not measured')
                self._pending_wait += [[2.0], [3.0, ev.x, ev.y]]
                return [0.0, ev.x, ev.y]
            if ev.lift:
                self._pending_wait.append([2.0])
            return [0.0, ev.x, ev.y]
        pts = ev.points
        self._pending_wait += [[1.0, x, y] for x, y in pts[1:]]
        if ev.lift:
            self._pending_wait.append([2.0])
        return [0.0, pts[0][0], pts[0][1]]


# ================================================================== coverage
_LAZY = {'IFTE', 'MAKELIST', 'MAKEMAT', 'INPUT', 'CHOOSE', 'PYTHON'}


def coverage(h):
    """-> {name: 'covered' | 'NOT COVERED'} for every name the loaded code calls or
    reads that is neither defined in the program nor a local."""
    seen = collections.OrderedDict()

    def walk(node, local):
        if isinstance(node, tuple):
            if not node:
                return
            if node[0] == 'call' and len(node) == 3 and node[1][0] == 'var':
                if node[1][1] not in local:          # L(i) on a local list is not a call
                    seen.setdefault(node[1][1], None)
                args = node[2]
                if node[1][1].upper() == 'PYTHON' and args and args[0][0] == 'var':
                    args = args[1:]                  # PYTHON(blockname, ...)
                for a in args:
                    walk(a, local)
                return
            if node[0] == 'var' and len(node) == 2 and isinstance(node[1], str):
                if node[1] not in local:
                    seen.setdefault(node[1], None)
                return
            for x in node[1:]:
                walk(x, local)
        elif isinstance(node, list):
            for x in node:
                walk(x, local)

    def locals_of(params, body):
        loc = set(params)

        def grab(n):
            if isinstance(n, tuple) and n:
                if n[0] == 'local':
                    loc.update(nm for nm, _ in n[1])
                if n[0] == 'for':
                    loc.add(n[1])
                if n[0] == 'call' and n[1] == ('var', 'MAKELIST') and len(n[2]) > 1 \
                        and n[2][1][0] == 'var':
                    loc.add(n[2][1][1])
                for x in n[1:]:
                    grab(x)
            elif isinstance(n, list):
                for x in n:
                    grab(x)
        grab(body)
        return loc

    for name, (params, body) in h.funcs.items():
        walk(body, locals_of(params, body))
    out = collections.OrderedDict()
    for name in seen:
        if name in h.funcs or name in h.globals_:
            continue
        up = name.upper()
        ok = (up in h._table or up in interp.BUILTINS or up in _LAZY or
              up in ('GETKEY', 'MOUSE', 'TICKS', 'RANDOM', 'CAS'))
        if re.fullmatch(r'[CD][0-9]', name):
            out[name] = 'app data (preset with app_data=)'
            continue
        out[name] = 'covered' if ok else 'NOT COVERED'
    return out


# ======================================================================= CLI
def _parse_input_spec(spec):
    s = spec.strip()
    if s.lower() == 'cancel':
        return CANCEL
    if s.lower() in ('ok', 'accept'):
        return ACCEPT

    def val(v):
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            return v[1:-1]
        return float(v)
    parts = [p for p in s.split(',')]
    if all('=' in p for p in parts):
        return dict((p.split('=', 1)[0].strip(), val(p.split('=', 1)[1])) for p in parts)
    return [None if p.strip() == '' else val(p) for p in parts]


def _parse_key(k):
    if k in KEY:
        return KEY[k]
    return int(k)


def _print_screen(s):
    print('  SCREEN %d (%s, in %s)%s' % (s.index, s.reason, s.func,
                                          '  menu: %s' % s.menu if s.menu else ''))
    for t in sorted(s.texts, key=lambda t: (t.y, t.x)):
        print('     y=%3s x=%3s f%s %-8s %s%s' % (_std(t.y), _std(t.x), _std(t.font or 0),
                                                t.hex or '', t.text,
                                                '   [may clip]' if t.clipped else ''))


def _print_timeline(h):
    for item in h.timeline:
        kind = item[0]
        if kind == 'screen':
            _print_screen(item[1])
        elif kind == 'msgbox':
            m = item[1]
            print('  MSGBOX (%d lines%s, in %s): %s' % (
                len(m.lines), ', MORE THAN 5' if m.over_five else '', m.func,
                ' | '.join(m.lines)))
        elif kind == 'choose':
            c = item[1]
            print('  CHOOSE %r (in %s) -> %d %s' % (c.title, c.func, c.index,
                                                    repr(c.label) if c.label else '(cancel)'))
        elif kind == 'input':
            i = item[1]
            print('  INPUT %r (in %s) -> %s %s' % (
                i.title, i.func, 'OK' if i.accepted else 'Cancel',
                ', '.join('%s=%s' % (k, _std(v)) for k, v in i.after.items())))
        elif kind == 'event':
            print('  %r taken (in %s)' % (item[1], item[2]))
        elif kind == 'skip':
            print('  PAGE SKIPPED: ' + item[1])
        elif kind == 'python':
            print('  PYTHON%r ignored (in %s)' % (tuple(item[1]), item[2]))


def main(argv=None):
    ap = argparse.ArgumentParser(description='Run an HP Prime PPL program on the PC, '
                                             'scripted. See README.md.')
    ap.add_argument('files', nargs='+')
    ap.add_argument('--call', action='append', default=[])
    ap.add_argument('--choose', action='append', default=[])
    ap.add_argument('--input', action='append', default=[])
    ap.add_argument('--key', action='append', default=[])
    ap.add_argument('--tap', action='append', default=[])
    ap.add_argument('--timeout', action='store_true')
    ap.add_argument('--idle-key', default=None)
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--stale-keys', action='store_true')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--show', default='timeline', choices=['timeline', 'screens', 'texts', 'all'])
    ap.add_argument('--coverage', action='store_true')
    o = ap.parse_args(argv)

    h = Harness(idle_key=_parse_key(o.idle_key) if o.idle_key else None,
                strict=o.strict, seed=o.seed, stale_keys=o.stale_keys)
    for f in o.files:
        try:
            h.load_path(f)
        except (PPLError, Unsupported) as e:
            print('%s: LOAD ERROR: %s' % (os.path.basename(f), e))
            return 1
        notes = h.notes.get(os.path.basename(f)) or {}
        print('loaded %s%s' % (os.path.basename(f), ('  (pre-pass: %s)' % ', '.join(
            '%s %d' % kv for kv in sorted(notes.items()))) if notes else ''))
    print('  %d functions, %d file-level LOCALs, %d forward declarations'
          % (len(h.funcs), len(h.file_locals), len(h.forward)))
    if o.coverage:
        cov = coverage(h)
        bad = [n for n, s in cov.items() if s == 'NOT COVERED']
        app = [n for n, s in cov.items() if s.startswith('app data')]
        if app:
            print('  app data columns read: %s (preset with app_data=, else reading '
                  'them is a runtime error, as before the app is opened)' % ', '.join(app))
        print('  built-ins and outside names used: %d; not covered: %s'
              % (len(cov), ', '.join(bad) if bad else 'none'))
    for c in o.choose:
        h.choose(int(c) if re.fullmatch(r'-?\d+', c) else c)
    for s in o.input:
        h.answer(_parse_input_spec(s))
    for k in o.key:
        h.press(_parse_key(k))
    for t in o.tap:
        x, y = t.split(',')
        h.tap(float(x), float(y))
    if o.timeout:
        h.timeout()
    rc = 0
    for expr in o.call:
        try:
            r = h.execute(expr)
            print('%s -> %s' % (expr, interp._format(r)))
        except (PPLError, Unsupported, HarnessStall, HarnessScriptError) as e:
            stack = ' > '.join(getattr(e, 'ppl_stack', []) or [])
            kind = ('RUNTIME ERROR (the device would open the Program Editor)'
                    if isinstance(e, PPLError) else type(e).__name__)
            print('%s -> %s%s: %s' % (expr, kind, (' in ' + stack) if stack else '', e))
            rc = 1
        if o.show in ('timeline', 'all'):
            _print_timeline(h)
        if o.show == 'screens':
            for s in h.screens:
                _print_screen(s)
        if o.show in ('texts', 'all'):
            for t in h.texts:
                print('  TEXT %r' % t)
        if h.terminal:
            print('  TERMINAL: ' + ' | '.join(h.terminal))
        for w in h.warnings:
            print('  WARNING: ' + w)
        ev, ch, an = h.leftover()
        if ev or ch or an:
            print('  UNUSED script: events %s, choose %s, input %s' % (ev, ch, an))
        h.reset_records()
    return rc


if __name__ == '__main__':
    sys.exit(main())
