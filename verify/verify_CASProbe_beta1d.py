#!/usr/bin/env python3
"""verify_CASProbe_beta1d.py -- CASProbe beta 1d on the PC (Roger Metcalf / Claude, 17 Oct 2026).

Beta 1d = beta 1c with T43b's test corrected.  Beta 1c ran on the HP Prime Virtual Calculator 2.4.2
(build 2026-09-09, 17 Oct 2026): "pass 44, fail 9, value 19, error 0, skip 0", one FAIL more than the
45 / 8 expected.  The extra FAIL was T43b:
    T43b FAIL STRING(0.096, 2, 1) is not 9.6E-2
      = 9.6\u1d07\u22122, codes 57 46 54 7431 8722 50
The Prime prints the scientific form (7431, the small capital E), but the exponent's minus is U+2212,
Home's minus (8722), not the ASCII hyphen T43b compared against.  Beta 1d PASSes T43b when the text
holds CHAR(7431), whatever the sign, notes which minus the exponent used, and cxSci (the summary line)
follows the same test.  Harness v3e models the exponent's minus (home_minus=True, as this script runs).

Built from verify_CASProbe_beta1c.py; every check of it is kept, run in harness v3e, with the new
version's expectations.  What is new for 1d is marked "1d":
  A. every CAS template the probe sends (printed after C1, from h.cas_calls, as the Prime prints)
  B. the two #PYTHON blocks under CPython, with stub hpprime / cas modules (unchanged blocks)
  C. end to end in harness v3e (home_minus: Home's STRING(-2.5) gives U+2212, and since v3e the
     exponent of STRING(0.096, 2, 1) too, as the emulator did):
       C0 the emulator's runs: beta 1b gives the emulator's 42 / 8 / 19 / 0; (1d) beta 1c gives the
          emulator's 44 / 9 / 19 / 0 with its T43b lines exactly (harness v3d gave 45 / 8: it printed
          a hyphen there); beta 1d 45 / 8 / 19 / 0; (1d) beta 1d's log is beta 1c's line for line
          except the version line, T43b's record, the exponent-minus note, one summary line and the
          tally
       C1 cas='giac', Python in CPython with an emulator-like cas.caseval: every expectation
       C2 CAS variables persist (emulator T25) and purge clears them
       C3 cas='fail' (every CAS call fails) -- the fallback paths
       C4 Python absent; C5 the menu; C6 the T34 warning; C7 the crash marker; C8 stale keys
       C9 (1c) the CAS answers the call-form tests but fails every later call: beta 1b stops 21
          tests with ERROR (INSTRING("") in cxFlat via cxShow); beta 1d logs each as a FAIL
  D. simulated DEVICE outcomes, as before (D1, D6 and D8 are now the emulator's own behaviour);
     (1d) D11: the exponent's minus as a hyphen, no sign at all, and an ASCII E
  E. layout: every TEXTOUT_P inside 320 px; log lines <= 46 characters
  F. the text helpers on edge inputs, including (1c) an empty text, a break or a separator at the
     very start and the very end, two quotes in a row
  G. (1d) beta 1d against beta 1c: the routines that differ (CASProbe, cxBegin, cxSummary, cxT43),
     the #PYTHON blocks unchanged; and, as before, against beta 1b
  H. every scientific STRING result (h.sci_strings) of every beta 1d run: only T43b's own
     STRING(0.096, 2, 1); every INSTRING, LEFT and MID, and why it cannot meet "" or a count of 0

Nothing here is device evidence.  It reads files only, and writes verify_CASProbe_beta1d_output.txt
beside itself.  Run:  python3 verify_CASProbe_beta1d.py
"""
import os, re, sys, time, types, subprocess, tempfile, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'CASProbe_beta1d.txt')
PREV = os.path.join(HERE, 'CASProbe_beta1c.txt')         # 1d: the version the emulator ran
OLD = os.path.join(HERE, 'CASProbe_beta1b.txt')
sys.path.insert(0, HERE)
import ppl_run_v3e as R                                  # noqa: E402
from ppl_run_v3e import Harness, CasResult               # noqa: E402
try:                                                     # 1d: C0 shows what v3d printed
    import ppl_run_v3d as R3D                            # noqa: E402
except ImportError:                                      # archived: that one check is skipped
    R3D = None
interp = R.interp

C50 = '100891344545564193334812497256'
OUT = []
FAILS = []
NCHK = [0]

# 1c: every harness made in this run is kept, and every scientific STRING result recorded with
# the routine that printed it (part H)
HARNESSES = []
_h_init = Harness.__init__
_h_sh = Harness._string_home


def _init(self, path, *a, **k):
    _h_init(self, path, *a, **k)
    self.vpath = os.path.basename(path)
    self.sci_where = []
    HARNESSES.append(self)


def _sh(self, a):
    n0 = len(self.sci_strings)
    r = _h_sh(self, a)
    if len(self.sci_strings) > n0:
        self.sci_where.append((self._fstack[-1][0] if self._fstack else '?', self.sci_strings[-1][2]))
    return r


Harness.__init__ = _init
Harness._string_home = _sh


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    OUT.append(s)


def check(ok, msg):
    NCHK[0] += 1
    say(('PASS  ' if ok else 'FAIL  ') + msg)
    if not ok:
        FAILS.append(msg)


SRC_TEXT = open(SRC, encoding='utf-8').read()
BLOCKS = dict(re.findall(r'^#PYTHON (\w+)\n(.*?)^#END', SRC_TEXT, re.S | re.M))


# ------------------------------------------------------------------ shims
def session_giac(keep_state=True):
    """A desktop Giac for the Python block's cas.caseval in part B (CPython stubs only).
    Output is decoded with errors='replace'."""
    hist = []

    def ev(expr, timeout=60):
        body = ''.join(x + ';\n' for x in hist) + expr.rstrip().rstrip(';') + ';\n'
        with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
            f.write(body)
            name = f.name
        try:
            out = subprocess.run(['icas', name], capture_output=True,
                                 timeout=timeout).stdout.decode('utf-8', 'replace')
        finally:
            os.unlink(name)
        keep = [ln.rstrip() for ln in out.split('\n') if ln.strip() and not (
            ln.strip().startswith('// ') or ln.strip().startswith('Added ')
            or ln.strip().startswith('Warning'))]
        keep = keep[len(hist):]
        txt = '\n'.join(keep).strip()
        if txt.endswith(','):
            txt = txt[:-1]
        if re.match(r'\s*(\w+)\s*:=', expr) and keep_state:
            hist.append(expr)
        m = re.match(r'\s*purge\((\w+)\)', expr)
        if m:
            hist[:] = [x for x in hist if not re.match(r'\s*' + m.group(1) + r'\s*:=', x)]
        return txt
    return ev


def caseval_emulator(s):
    """Python's cas.caseval as the emulator answered (CASProbe 1a/1b T34): a str, with a
    big integer as a 12-digit decimal (run_CASProbe_beta1b_v3b.py)."""
    t = R.prime_eval(s)
    if len(t) >= 2 and t[0] == '"' and t[-1] == '"':
        t = t[1:-1]
    if re.fullmatch(r'-?\d{13,}', t):
        t = '%.12g' % float(t)
    return t


def make_python(h, cas_mode='emulator', bigint=True):
    """PYTHON(name) runs the real #PYTHON block in CPython: hpprime.eval reads/writes the harness
    globals.  cas.caseval: 'emulator' (as the emulator answered), 'giac' (desktop Giac, exact),
    'raise' (a crash), 'missing' (no cas module)."""
    def fake(a):
        name = a[0]
        block = BLOCKS[name]
        if not bigint:      # a MicroPython with 64-bit ints: both big results overflow
            block = block.replace('str(2 ** 100)', '_overflow()')
            block = block.replace('c = c * (50 + i) // i', 'c = _mul(c, 50 + i) // i')
        hp = types.ModuleType('hpprime')

        def ev(s):
            m = re.fullmatch(r'(CX_\w+):="(.*)"', s, re.S)
            if m:
                h.globals_[m.group(1)] = m.group(2)
                return m.group(2)
            if s in ('CX_CS', 'CX_PYS', 'CX_PYM'):
                return h.globals_[s]
            if s == 'TICKS':
                return float(h._ticks())
            raise RuntimeError('stub hpprime.eval cannot answer %r' % s)
        hp.eval = ev
        hp.ticks = lambda: int(time.time() * 1000)
        sys.modules['hpprime'] = hp
        if cas_mode == 'missing':
            sys.modules['cas'] = None
        else:
            cm = types.ModuleType('cas')
            if cas_mode == 'giac':
                cm.caseval = lambda s: session_giac(False)(s)
            elif cas_mode == 'emulator':
                cm.caseval = caseval_emulator
            else:
                def boom(s):
                    raise RuntimeError('simulated caseval crash')
                cm.caseval = boom
            sys.modules['cas'] = cm
        g = {'__name__': '__main__'}
        if not bigint:
            def _overflow():
                raise OverflowError('small int overflow')
            g['_overflow'] = _overflow

            def _mul(a, b):
                if abs(a * b) > 2 ** 63 - 1:
                    raise OverflowError('small int overflow')
                return a * b
            g['_mul'] = _mul
        try:
            exec(compile(block, name, 'exec'), g)
        except Exception as e:      # on the device: a traceback in the Terminal, PPL goes on
            h.warnings.append('Python %s raised %s: %s' % (name, type(e).__name__, e))
        return 0.0
    return fake


def harness(cas='giac', python='emulator', bigint=True, stale=False, src=None, harness_cls=None):
    """1c: the harness's own CAS model (v3d: CAS(variable) unevaluated, the EXPR form evaluated,
    the Prime's printing, CAS variables persist, a big non-string integer a real), and Home's
    U+2212 minus in STRING(-2.5) -- what the emulator did; 1d: harness v3e, whose home_minus also
    puts U+2212 before the exponent of a scientific STRING(x, 2, d), as the emulator did in beta 1c's
    T43b.  beta 1a's TYPE/EXPR and session shims were for harness v3, which had none of this.
    harness_cls=R3D.Harness runs the same set-up in harness v3d (C0 only)."""
    h = (harness_cls or Harness)(src or SRC, cas=cas, stale_keys=stale, strict=True, home_minus=True)
    h.globals_['HSeparator'] = 0.0
    h.globals_['HFormat'] = 0.0
    if python is not None:
        h._python = make_python(h, python, bigint)
    return h


def run(h, menu=1, warn='Plus', summary='Enter', pager='Esc', msgbox=False):
    h.choose(menu)
    if warn == 'Plus':
        h.press(50)
    elif warn == 'Minus':
        h.press(45)
    elif isinstance(warn, tuple):
        h.tap(*warn)
    if summary:
        h.press(KEYS[summary]) if isinstance(summary, str) else h.tap(*summary)
    if pager:
        h.press(KEYS[pager])
    res = h.call('CASProbe')
    return res


KEYS = {'Enter': 30, 'Esc': 4, 'Plus': 50, 'Minus': 45, 'Down': 12, 'Right': 8}


def log(h):
    return list(h.globals_['CX_LOG'])


def line(h, prefix):
    """The first CX_LOG line that starts with prefix (e.g. 'T05 ')."""
    for s in log(h):
        if s.startswith(prefix):
            return s
    return None


def rec(h, prefix):
    """A record line with its word-wrapped continuation joined on."""
    L = log(h)
    for i, s in enumerate(L):
        if s.startswith(prefix):
            return s + ' ' + (L[i + 1].strip() if i + 1 < len(L) else '')
    return ''


def verdict(h, tid):
    s = line(h, tid + ' ')
    return s.split()[1] if s else None


def counts(h):
    c = collections.Counter()
    for s in log(h):
        m = re.match(r'(T\d\d[a-d]?) (PASS|FAIL|VALUE|ERROR|SKIP)\b', s)
        if m:
            c[m.group(2)] += 1
    return c


def fails(h):
    return [s.split()[0] for s in log(h) if re.match(r'T\d\d[a-d]? FAIL\b', s)]


# ======================================================================= A
say('== A. every template the probe sends, as the Prime prints it (harness v3e: desktop Giac 1.9')
say('      with the Prime\'s printing) -- printed after run C1, from h.cas_calls ==')
TEMPLATES = None

# ======================================================================= B
say('')
say('== B. the #PYTHON blocks under CPython (stub hpprime, stub cas = desktop Giac) ==')
check(set(BLOCKS) == {'cxPyBig', 'cxPyCas'}, 'two blocks found: %s' % sorted(BLOCKS))
for nm, bl in BLOCKS.items():
    check(not re.search(r'^\s*#\s*END', bl, re.M), '%s: no comment line that looks like #END' % nm)
    check(not re.search(r'^(import|from) (?!hpprime)', bl, re.M),
          '%s: the only top-level import is hpprime (Lessons Learned s9)' % nm)
    check('\t' not in bl, '%s: spaces only, no tabs' % nm)


class Mini(object):
    def __init__(self):
        self.globals_ = {'CX_CS': C50, 'CX_PYS': '', 'CX_PYM': ''}
        self.warnings = []
        self.clock = 0

    def _ticks(self):
        self.clock += 1
        return self.clock


m = Mini(); make_python(m, 'giac')(['cxPyBig'])
check(m.globals_['CX_PYS'] == '1267650600228229401496703205376;%s;same' % C50,
      'cxPyBig: CX_PYS = %r' % m.globals_['CX_PYS'])
check(m.globals_['CX_PYM'] == 'T33 done', 'cxPyBig: last mark %r' % m.globals_['CX_PYM'])
m = Mini(); m.globals_['CX_CS'] = '"%s"' % C50; make_python(m, 'giac')(['cxPyBig'])
check(m.globals_['CX_PYS'].endswith(';same'), 'cxPyBig: a quoted CX_CS still reads as the same integer')
m = Mini(); m.globals_['CX_CS'] = C50[:-1] + '7'; make_python(m, 'giac')(['cxPyBig'])
check(m.globals_['CX_PYS'].endswith(';differ'), 'cxPyBig: a wrong CX_CS gives "differ"')
m = Mini(); make_python(m, 'giac', bigint=False)(['cxPyBig'])
check(m.globals_['CX_PYS'] == 'ERR small int overflow;ERR small int overflow;differ',
      'cxPyBig without big ints: %r' % m.globals_['CX_PYS'])
m = Mini(); make_python(m, 'giac')(['cxPyCas'])
f = m.globals_['CX_PYS'].split(';')
check(len(f) == 6 and f[0] == "<class 'str'>" and f[1] == C50 and f[4] == '35/128',
      'cxPyCas (desktop Giac): %r' % m.globals_['CX_PYS'])
m = Mini(); make_python(m, 'emulator')(['cxPyCas'])
f = m.globals_['CX_PYS'].split(';')
check(len(f) == 6 and f[0] == "<class 'str'>" and f[1] == '1.00891344546e+29' and f[4] == '35/128',
      '1c: cxPyCas with the emulator\'s caseval (a decimal for C(100,50), emulator T34): %r' % m.globals_['CX_PYS'])
m = Mini(); make_python(m, 'raise')(['cxPyCas'])
check(m.globals_['CX_PYS'] == '' and m.globals_['CX_PYM'] == 'T34 import ok, calling caseval',
      'cxPyCas, caseval crashing: CX_PYS empty, mark %r' % m.globals_['CX_PYM'])
m = Mini(); make_python(m, 'missing')(['cxPyCas'])
check(m.globals_['CX_PYS'].startswith('noimport;'), 'cxPyCas, no cas module: %r' % m.globals_['CX_PYS'])

# ======================================================================= C0
say('')
say('== C0. the emulator\'s runs (Run every test, + at the warning, a key, Esc), harness v3e ==')
EMU = {'PASS': 42, 'FAIL': 8, 'VALUE': 19, 'ERROR': 0}
EMU_FAIL = ['T01', 'T04', 'T05', 'T06', 'T07', 'T10', 'T32', 'T34a']
ho = harness(src=OLD)
r_old = run(ho)
co = counts(ho)
say('   beta 1b: %s; pass %d, fail %d, value %d, error %d; FAIL %s'
    % (r_old, co['PASS'], co['FAIL'], co['VALUE'], co['ERROR'], fails(ho)))
check(all(co[k] == v for k, v in EMU.items()) and fails(ho) == EMU_FAIL,
      'beta 1b in v3e gives the emulator\'s 42 pass, 8 fail, 19 values, 0 errors, FAIL %s' % EMU_FAIL)
# 1d: beta 1c as the emulator ran it (17 Oct 2026): "pass 44, fail 9, value 19, error 0, skip 0",
# the extra FAIL T43b, its codes 57 46 54 7431 8722 50, and the summary "NOT scientific"
EMU1C_FAIL = ['T01', 'T04', 'T05', 'T06', 'T07', 'T10', 'T32', 'T43b', 'T34a']
EMU1C_T43B = ['T43b FAIL STRING(0.096, 2, 1) is not 9.6E-2',
              '  = 9.6\u1d07\u22122, codes 57 46 54 7431 8722 50 ']
hp = harness(src=PREV)
r_prev = run(hp)
cp = counts(hp)
say('   beta 1c: %s; pass %d, fail %d, value %d, error %d; FAIL %s'
    % (r_prev, cp['PASS'], cp['FAIL'], cp['VALUE'], cp['ERROR'], fails(hp)))
lp = log(hp)
ib = lp.index(EMU1C_T43B[0]) if EMU1C_T43B[0] in lp else -1
check(cp['PASS'] == 44 and cp['FAIL'] == 9 and cp['VALUE'] == 19 and cp['ERROR'] == 0
      and fails(hp) == EMU1C_FAIL and ib > 0 and lp[ib:ib + 2] == EMU1C_T43B
      and 'STRING(0.096, 2, 1): NOT scientific' in lp,
      '1d: beta 1c in v3e gives the emulator\'s beta 1c run: 44 pass, 9 fail, 19 values, 0 errors, the extra '
      'FAIL T43b with "codes 57 46 54 7431 8722 50", and "STRING(0.096, 2, 1): NOT scientific"')
if ib > 0:
    say('   ' + '\n   '.join(lp[ib:ib + 2]))
if R3D is None:
    say('   (ppl_run_v3d.py is not beside this script: the v3d comparison is skipped)')
else:
    hp3 = harness(src=PREV, harness_cls=R3D.Harness)
    run(hp3)
    c3 = counts(hp3)
    check(c3['PASS'] == 45 and c3['FAIL'] == 8 and verdict(hp3, 'T43b') == 'PASS'
          and '  = 9.6\u1d07-2, codes 57 46 54 7431 45 50 ' in log(hp3),
          '1d: in harness v3d beta 1c gave 45 pass, 8 fail, T43b PASS with codes ... 7431 45 50 -- v3d printed an '
          'ASCII hyphen in the exponent, so it could not show the emulator\'s FAIL; v3e prints U+2212 there')
h = harness()
r_new = run(h)
cn = counts(h)
say('   beta 1d: %s; pass %d, fail %d, value %d, error %d; FAIL %s'
    % (r_new, cn['PASS'], cn['FAIL'], cn['VALUE'], cn['ERROR'], fails(h)))
check(cn['PASS'] == 45 and cn['FAIL'] == 8 and cn['VALUE'] == 19 and cn['ERROR'] == 0 and fails(h) == EMU_FAIL,
      '1d: beta 1d gives beta 1b\'s emulator run plus T43a, T43b, T43c PASS: 45 pass, 8 fail, 19 values, '
      '0 errors, FAIL %s' % EMU_FAIL)
old_l = [re.sub(r'\d+ ms', 'N ms', s) for s in log(ho)]       # timings vary from run to run
prev_l = [re.sub(r'\d+ ms', 'N ms', s) for s in lp]
new_l = [re.sub(r'\d+ ms', 'N ms', s) for s in log(h)]
i43 = new_l.index('-- T43 (added in beta 1c) --')
j43 = next(i for i in range(i43 + 1, len(new_l)) if not (new_l[i].startswith('T43') or new_l[i].startswith('  ')))
two = ['INSTRING of an empty string: an error', 'STRING(0.096, 2, 1): scientific']
k2 = new_l.index(two[0])
same = (new_l[0] == 'CASProbe beta 1d, 17 Oct 2026 build' and old_l[0] == 'CASProbe beta 1b, 17 Oct 2026 build'
        and new_l[k2:k2 + 2] == two
        and new_l[1:i43] + new_l[j43:k2] + new_l[k2 + 2:-1] == old_l[1:-1]
        and old_l[-1].replace('42 pass', '45 pass') == new_l[-1])
check(same, '1c: the log is beta 1b\'s line for line (timings aside), except the version line, the T43 block '
      '(%d lines), two new summary lines and the tally' % (j43 - i43))
say('   ' + '\n   '.join(new_l[i43:j43]))
# 1d: against beta 1c, only T43b's record, its new note line, one summary line, the version line and
# the tally differ
T43B_1D = ['T43b PASS STRING(0.096, 2, 1) is scientific',
           '  = 9.6\u1d07\u22122, codes 57 46 54 7431 8722 50 ',
           '  exponent minus: CHAR(8722), Home\'s minus']
want_l = list(prev_l)
want_l[0] = 'CASProbe beta 1d, 17 Oct 2026 build'
if ib > 0:
    want_l[ib:ib + 2] = T43B_1D
want_l = [('STRING(0.096, 2, 1): scientific' if x == 'STRING(0.096, 2, 1): NOT scientific' else x) for x in want_l]
want_l[-1] = want_l[-1].replace('44 pass, 9 fail', '45 pass, 8 fail')
check(ib > 0 and new_l == want_l and prev_l[0] == 'CASProbe beta 1c, 17 Oct 2026 build',
      '1d: the log is beta 1c\'s line for line (timings aside), except the version line, T43b\'s record (FAIL -> '
      'PASS), one new note line "exponent minus: CHAR(8722), Home\'s minus", the summary line "NOT scientific" -> '
      '"scientific" and the tally (44 pass, 9 fail -> 45 pass, 8 fail)')
if new_l != want_l:
    import difflib
    for d_ in list(difflib.unified_diff(want_l, new_l, 'expected', 'beta 1d', n=0, lineterm=''))[:30]:
        say('     ' + d_)

# ======================================================================= C1
say('')
say('== C1. end to end: cas=giac, Python in CPython (emulator caseval), Run every test ==')
t0 = time.time()
res = r_new
say('RETURN:', res)
check(h.globals_['CX_LAST'] == 'done', 'CX_LAST = "done"')
say('--- CX_LOG, as the pager shows it ---')
for s in log(h):
    say('   ' + s)
expect_pass = ['T02', 'T08', 'T09', 'T11', 'T12',
               'T13', 'T14c', 'T15a', 'T15b', 'T16', 'T17', 'T18', 'T19', 'T20c', 'T21b',
               'T22', 'T23', 'T24', 'T25b', 'T26', 'T28', 'T31a', 'T32b', 'T33a', 'T33b',
               'T33c', 'T34b',
               # 1a
               'T35a', 'T35b', 'T35c', 'T35d', 'T36a', 'T36b', 'T37b', 'T37c', 'T38a', 'T39b',
               'T40a', 'T40b', 'T40c', 'T41b', 'T42',
               # 1c
               'T43a', 'T43b', 'T43c']
bad = [t for t in expect_pass if verdict(h, t) != 'PASS']
check(not bad, 'every check that the emulator passed PASSes (%d; beta 1a\'s list of 50 less the emulator\'s 8 '
      'FAILs, plus T43a-c); not: %s' % (len(expect_pass), bad))
check([L_ for L_ in log(h) if L_.startswith('T43b ')] == [T43B_1D[0]]
      and log(h)[log(h).index(T43B_1D[0]):log(h).index(T43B_1D[0]) + 3] == T43B_1D,
      '1d: T43b PASS, "= 9.6E-2, codes 57 46 54 7431 8722 50" (the E and the minus as the emulator printed them), '
      'and the note "exponent minus: CHAR(8722), Home\'s minus"')
check(verdict(h, 'T03') == 'VALUE' and 'HSeparator = 0, decimal dot' in line(h, 'T03'), line(h, 'T03'))
check(verdict(h, 'T01') == 'FAIL' and any('8722' in s for s in log(h)),
      'emulator: T01 FAIL, STRING(-2.5) begins with U+2212 (code 8722)')
for t, why in (('T04', '12-digit real'), ('T05', 'lost the exact digits'), ('T06', 'unevaluated'),
               ('T07', 'unevaluated'), ('T10', '12-digit real')):
    check(verdict(h, t) == 'FAIL' and why in rec(h, t + ' '), 'emulator: %s' % rec(h, t + ' '))
L1 = log(h)
order = [s.split()[0] for s in L1 if re.match(r'T\d\d[a-d]? ', s)]
check(order.index('T32b') < order.index('T35a') < order.index('T42') < order.index('T43a') < order.index('T33a'),
      '1a/1c: T35-T42 run after T32, T43 after T42, all before the Python tests')
check('  no break up to 6005 characters' in L1, '1a: T35 no break up to 6005 characters')
check('  shape: {[]}, commas' in L1, '1a (emulator): T36a shape "{[]}, commas" -- the Prime prints {[2,1]}')
check(verdict(h, 'T41a') == 'VALUE' and 'the glyph (8734)' in rec(h, 'T41a '), '1a (emulator): %s' % rec(h, 'T41a '))
check('  = 0.044179 (SciPy 0.044179)' in L1, '1a: T42 shows 0.044179')
for s_ in ('long CAS text: works to 6005 characters', 'an infinite limit prints: the glyph (8734)',
           'BINOMIAL_CDF order (n, p, k): yes', 'INSTRING of an empty string: an error',
           'STRING(0.096, 2, 1): scientific'):
    check(s_ in L1, '1a/1c: summary line "%s"' % s_)
check(verdict(h, 'T25a') == 'VALUE' and 'persist' in line(h, 'T25a'), 'emulator: ' + line(h, 'T25a'))
check(h.globals_['CX_SUM'].startswith('form 2, CAS yes'), 'emulator: CX_SUM = %r' % h.globals_['CX_SUM'])
check('form 2: in xxCas use (q = CHAR(34)):' in L1 and '  the text comes in quotes: drop them' in L1,
      'emulator: the log says form 2, and drop the quotes')
check(not [s for s in L1 if ' ERROR ' in s[:9]], 'no test stopped with a run-time error')
check(all(len(s) <= 46 for s in L1), 'every CX_LOG line <= 46 characters (longest %d)'
      % max(len(s) for s in L1))
summ = [p for p in h.pages if p.func == 'cxSummary']
check(len(summ) == 1 and summ[0].has('CASProbe beta 1d: summary'), 'one summary page, titled beta 1d')
if summ:
    say('--- the summary page ---')
    for t in sorted(summ[0].texts, key=lambda t: (t.y, t.x)):
        say('   y=%3d x=%3d f%s %s  %s' % (t.y, t.x, t.font, t.hex, t.text))
warn = [p for p in h.pages if p.func == 'cxWarnPy']
check(len(warn) == 1 and warn[0].has("CASProbe and choose 'Skip Python CAS'."),
      'the warning page names the menu item exactly')
menu = h.chooses[0] if h.chooses else None
check(menu is not None and 'Skip Python CAS' in menu.items and menu.title == 'CASProbe beta 1d',
      'the menu "CASProbe beta 1d" has "Skip Python CAS": %s' % (menu.items if menu else None))
run_pg = [p_ for p_ in h.pages if p_.func == 'cxBegin']
check(run_pg and all(p_.has('CASProbe beta 1d: running') for p_ in run_pg),
      '1d: every progress page is titled "CASProbe beta 1d: running" (%d pages)' % len(run_pg))
check(not any(h.leftover()), 'no script left over: %r' % (h.leftover(),))
check(not h.cas_vars, 'emulator T25: cxq was purged again (h.cas_vars empty)')
say('--- warnings ---')
for w in sorted(set(h.warnings)):
    say('   ' + w)
TEMPLATES = list(h.cas_calls)
say('--- every CAS call: expression -> the answer as the Prime prints it (ms on the PC) ---')
for ex, ans, ms in TEMPLATES:
    a = ans.replace('\n', ' / ')
    say('   %-58s -> %s  (%.0f ms)' % (ex if len(ex) <= 58 else ex[:55] + '...',
                                      a if len(a) <= 70 else a[:60] + '... [%d chars]' % len(a), ms))
say('   %d CAS calls in all' % len(TEMPLATES))

# ======================================================================= C2
say('')
say('== C2. CAS variables persist from call to call (emulator T25), and purge clears them ==')
check(verdict(h, 'T25a') == 'VALUE' and 'persist' in line(h, 'T25a'), 'T25a: %s' % line(h, 'T25a'))
check(verdict(h, 'T25b') == 'PASS', 'T25b: %s' % line(h, 'T25b'))
check(h.globals_['CX_SUM'].startswith('form 2, CAS yes'), 'CX_SUM = %r' % h.globals_['CX_SUM'])

# ======================================================================= C3
say('')
say('== C3. cas=fail: every CAS call fails ==')
h3 = harness(cas='fail', python='raise')
res = run(h3)
say('RETURN:', res)
for t in ('T04', 'T05', 'T06', 'T07', 'T08', 'T09', 'T10'):
    check(verdict(h3, t) == 'FAIL', line(h3, t))
check(verdict(h3, 'T11') == 'SKIP' and 'T11-T32' in rec(h3, 'T11 ') and 'T35-T41' in rec(h3, 'T11 '),
      rec(h3, 'T11 '))
check(line(h3, 'T12') is None and line(h3, 'T35a') is None, 'T12-T32 and T35-T41 not run')
check(verdict(h3, 'T42') == 'PASS', '1a: T42 (no CAS) still runs: %s' % line(h3, 'T42'))
check(all(verdict(h3, t) == 'PASS' for t in ('T43a', 'T43b', 'T43c')), '1c: T43 (no CAS) still runs, a-c PASS')
check('long CAS text: not tested' in log(h3), '1a: summary "long CAS text: not tested"')
check(verdict(h3, 'T33a') == 'PASS' and '  (CX_CS is the constant: no CAS text)' in log(h3),
      'T33 runs on the constant: %s' % line(h3, 'T33a'))
check(verdict(h3, 'T34') == 'FAIL' and 'no answer' in line(h3, 'T34'), line(h3, 'T34'))
check('  last mark: T34 import ok, calling caseval' in log(h3), 'T34 names the last mark')
check(h3.globals_['CX_SUM'].startswith('form 0, CAS no'), 'CX_SUM = %r' % h3.globals_['CX_SUM'])
check(not [s for s in log(h3) if ' ERROR ' in s[:9]], 'no test stopped with a run-time error')
summ = [p for p in h3.pages if p.func == 'cxSummary'][0]
check(summ.has('CAS available: no') and summ.has('none: the CAS gave no 30 digits'),
      'summary: CAS available: no / none: the CAS gave no 30 digits')
check(summ.has('caseval: no answer (crash?)'), 'summary: caseval: no answer (crash?)')

# ======================================================================= C4
say('')
say('== C4. Python absent (PYTHON() does nothing) ==')
h4 = harness(python=None)
run(h4)
check(verdict(h4, 'T33') == 'FAIL' and 'no answer' in line(h4, 'T33'), line(h4, 'T33'))
check(verdict(h4, 'T34') == 'FAIL' and 'no answer' in line(h4, 'T34'), line(h4, 'T34'))
check('  last mark:  none' in log(h4), 'the empty mark is shown as " none"')

# ======================================================================= C5
say('')
say('== C5. the menu ==')
h5 = harness()
h5.choose(2); h5.press(30); h5.press(4)
h5.call('CASProbe')
check(verdict(h5, 'T33a') == 'PASS' and verdict(h5, 'T34') == 'SKIP', 'Skip Python CAS: %s / %s'
      % (line(h5, 'T33a'), line(h5, 'T34')))
check(not [p for p in h5.pages if p.func == 'cxWarnPy'], 'no warning page when skipped at the menu')
h5 = harness()
h5.choose(3); h5.press(30); h5.press(4)
h5.call('CASProbe')
check(verdict(h5, 'T33') == 'SKIP' and verdict(h5, 'T34') == 'SKIP', 'Skip all Python: %s / %s'
      % (line(h5, 'T33'), line(h5, 'T34')))
n_before = len(log(h5))
h5.reset_records()
h5.choose(4); h5.press(12); h5.press(8); h5.press(4)
r4 = h5.call('CASProbe')
check(r4 == 'CASProbe: %d lines in CX_LOG' % n_before and len(log(h5)) == n_before,
      'Show last log: %r, the log kept' % r4)
check([p.func for p in h5.pages] == ['cxView'] * 3, 'Show last log: only the pager (%s)'
      % [p.func for p in h5.pages])
h5.reset_records()
h5.globals_['CX_LOG'] = ['T01 PASS a line', '', 'T02 FAIL another']
h5.choose(4); h5.press(4)
try:
    r4 = h5.call('CASProbe'); e4 = None
except Exception as x:
    r4, e4 = None, x
check(e4 is None and r4 == 'CASProbe: 3 lines in CX_LOG',
      '1c: Show last log with an empty line in CX_LOG: the pager draws it (%s)' % (e4 or r4))
h5.reset_records()
h5.choose(0)
check(h5.call('CASProbe') == 'CASProbe: cancelled', 'Cancel returns "CASProbe: cancelled"')

# ======================================================================= C6
say('')
say('== C6. the T34 warning: a tap on "Skip it", the - key, a tap on "Run it" ==')
h6 = harness()
run(h6, warn=(235, 165))
check(verdict(h6, 'T34') == 'SKIP' and 'warning' in line(h6, 'T34'), 'tap Skip it: %s' % line(h6, 'T34'))
h6 = harness()
run(h6, warn='Minus')
check(verdict(h6, 'T34') == 'SKIP', '- key: %s' % line(h6, 'T34'))
h6 = harness()
h6.choose(1); h6.tap(85, 165); h6.tap(160, 100); h6.tap(160, 200); h6.press(4)
h6.call('CASProbe')
check(verdict(h6, 'T34b') == 'PASS' and verdict(h6, 'T34a') == 'FAIL',
      'tap Run it, tap the summary, tap the pager: T34 runs (emulator: T34a FAIL, a decimal; T34b PASS)')
pv = [p for p in h6.pages if p.func == 'cxView']
check(len(pv) == 2 and pv[1].has('lines 14-26 of %d' % len(log(h6))),
      'a tap on the lower half pages on: %s' % (pv[-1].find('lines ').text if pv else None))

# ======================================================================= C7
say('')
say('== C7. the crash marker from a previous run ==')
h7 = harness()
h7.globals_['CX_LAST'] = 'T34 Python cas.caseval: if you read this after a reset, caseval crashed'
run(h7)
check(any(s.startswith('previous run stopped in: T34') for s in log(h7)), 'the log names it')
check(h7.msgboxes and 'The last run stopped inside:' in h7.msgboxes[0].lines[0]
      and not h7.msgboxes[0].over_five, 'a MSGBOX of %d lines tells Roger'
      % (len(h7.msgboxes[0].lines) if h7.msgboxes else 0))

# ======================================================================= C8
say('')
say('== C8. stale-key mode: the dialog\'s own Enter left in the key buffer ==')
h8 = harness(stale=True)
run(h8)
check(not h8.stale_skips, 'no page skipped by a left-over key: %s' % h8.stale_skips)

# ======================================================================= C9
say('')
say('== C9 (1c). the CAS answers the call-form tests, then every later call fails ==')


def partial(hh):
    real = hh._cas_eval

    def part(expr):
        if 'comb(100,50)' in expr:
            return real(expr)
        hh.cas_calls.append((expr, 'FAILED (simulated)', 0.0))
        raise R.interp.PPLError('CAS call failed (simulated)')
    hh._cas_eval = part
    return hh


ho9 = partial(harness(src=OLD))
run(ho9)
hn9 = partial(harness())
run(hn9)
eo = [s for s in log(ho9) if re.match(r'T\d\d[a-d]? ERROR', s)]
en = [s for s in log(hn9) if re.match(r'T\d\d[a-d]? ERROR', s)]
say('   beta 1b: %s; %d tests stopped, e.g. %s' % (dict(counts(ho9)), len(eo), eo[:3]))
say('   beta 1d: %s' % dict(counts(hn9)))
check(len(eo) >= 15, '1c: beta 1b stops %d tests with ERROR (cxShow -> cxFlat -> INSTRING of the failed '
      'call\'s "")' % len(eo))
check(not en and hn9.globals_['CX_SUM'].startswith('form 2, CAS yes'),
      '1c: beta 1d stops none; form 2 is still chosen')
need = ['T11', 'T16', 'T21a', 'T21b', 'T27', 'T28', 'T29', 'T30', 'T40a', 'T40b', 'T40c', 'T41a', 'T41b']
got = {t: verdict(hn9, t) for t in need}
check(all(v in ('FAIL', 'VALUE') for v in got.values()) and all('CAS error' in rec(hn9, t + ' ') for t in need),
      '1c: every later test logs its failed call ("CAS error") and goes on to its next call: %s' % got)
check(verdict(hn9, 'T39b') == 'FAIL' and verdict(hn9, 'T39a') == 'VALUE' and verdict(hn9, 'T25') == 'FAIL',
      '1c: T39 (an empty cxVal answer) and T25 (cxq+1 failing) log and go on')

# ======================================================================= D
say('')
say('== D1. device: CAS(variable) hands the string back unevaluated (the emulator; harness v3e\'s model) ==')
check(verdict(h, 'T06') == 'FAIL' and verdict(h, 'T07') == 'FAIL' and verdict(h, 'T08') == 'PASS'
      and verdict(h, 'T09') == 'PASS', 'T06, T07 FAIL; T08, T09 PASS')
check('unevaluated' in rec(h, 'T06 '), 'T06 says how it failed: %s' % rec(h, 'T06 '))
check(any(s.startswith('form 2: in xxCas use') for s in log(h)), 'form 2 chosen and logged')
check(verdict(h, 'T11') == 'PASS' and verdict(h, 'T24') == 'PASS', 'T11-T31 run through the EXPR form')
check(verdict(h, 'T32') == 'FAIL', 'T32: the as-written xxCas (form 1) guard fails here: %s' % line(h, 'T32'))
check(h.globals_['CX_SUM'].startswith('form 2, CAS yes'), 'CX_SUM = %r' % h.globals_['CX_SUM'])

say('')
say('== D2. device variant: string(...) does not help -- every 13+ digit answer is a 12-digit real ==')
hd2 = harness()
real_ev = hd2._cas_eval


def cas_d2(expr):
    r = real_ev(expr)
    if isinstance(r, str) and re.fullmatch(r'\d{13,}', r):
        return float(r)
    return r
hd2._cas_eval = cas_d2
run(hd2)
check(all(verdict(hd2, t) == 'FAIL' and '12-digit real' in rec(hd2, t + ' ') for t in ('T04', 'T08', 'T09', 'T10'))
      and all('unevaluated' in rec(hd2, t + ' ') for t in ('T06', 'T07')), rec(hd2, 'T08 '))
check(verdict(hd2, 'T11') == 'SKIP', 'no form works: T11-T32 skipped')

say('')
say('== D3. device variant: Home STRING() with U+FE50 grouping and a U+2212 minus ==')
hd3 = harness()
real_string = hd3._table['STRING']


def grouped(a, site):
    v = a[0]
    if len(a) == 1 and isinstance(v, float) and v == int(v) and abs(v) >= 1000:
        s = '{:,}'.format(int(abs(v))).replace(',', '﹐')
        return ('−' if v < 0 else '') + s
    if len(a) == 1 and isinstance(v, float) and v < 0:
        return '−' + R._std(-v)
    return real_string(a, site)
hd3._table['STRING'] = grouped
run(hd3)
check(verdict(hd3, 'T01') == 'FAIL', line(hd3, 'T01'))
check(verdict(hd3, 'T31a') == 'FAIL', 'T31a: %s' % line(hd3, 'T31a'))
check(verdict(hd3, 'T02') == 'PASS' and verdict(hd3, 'T15a') == 'PASS', 'cxIStr text still works (T02, T15)')
summ = [p for p in hd3.pages if p.func == 'cxSummary'][0]
check(summ.has('Home STRING(real): NOT plain'), 'summary: Home STRING(real): NOT plain')

say('')
say('== D4. device variant: a CAS syntax error comes back as text, not an error ==')
hd4 = harness()
real_cas = hd4._table['CAS']


def cas_d4(a, site):
    if a[0] in ('comb(100,', 'string(comb(100,)'):
        return 'Error: Syntax Error'
    return real_cas(a, site)
hd4._table['CAS'] = cas_d4
run(hd4)
check(verdict(hd4, 'T26') == 'VALUE' and 'as text' in line(hd4, 'T26'), line(hd4, 'T26'))
check(verdict(hd4, 'T32') == 'FAIL', 'T32 stays FAIL here: its form 1 hands the text back unevaluated (emulator), '
      'so the guard never sees the error text: %s' % line(hd4, 'T32'))

say('')
say('== D5. device variants on the Python side ==')
hd5 = harness(bigint=False)
run(hd5)
check(verdict(hd5, 'T33a') == 'FAIL' and '  2**100 = ERR small int overflow' in log(hd5),
      'no big ints: %s' % line(hd5, 'T33a'))
check(verdict(hd5, 'T33b') == 'FAIL', 'and comb fails too: %s' % line(hd5, 'T33b'))
summ = [p for p in hd5.pages if p.func == 'cxSummary'][0]
check(summ.has('Python ints: not exact'), 'summary: Python ints: not exact')
hd5 = harness(python='missing')
run(hd5)
check(verdict(hd5, 'T34') == 'FAIL' and 'import cas failed' in line(hd5, 'T34'), line(hd5, 'T34'))

say('')
say('== D6. CAS answers are PPL strings, so STRING() adds quotes (the emulator, T12; harness v3e) ==')
check(all(verdict(h, t) == 'PASS' for t in ('T08', 'T09')), 'the 30 digits are found inside the quotes')
check('  (the text came back inside quotes)' in log(h), 'and the log says the text was quoted')
summ = [p for p in h.pages if p.func == 'cxSummary'][0]
check(summ.has('EXPR("CAS("+q+s+q+")"), drop quotes'), 'the summary shows the form 2 line with ", drop quotes"')
check(verdict(h, 'T11') == 'PASS' and verdict(h, 'T12') == 'PASS', 'T11 (35/128) and T12 pass on quoted text')

say('')
say('== D7 (1a). device variant: CAS text over 2,500 characters fails ==')
hd7 = harness()
real_cas = hd7._table['CAS']


def cas_d7(a, site):
    if len(a[0]) > 2500:
        raise R.interp.PPLError('simulated: text too long')
    return real_cas(a, site)
hd7._table['CAS'] = cas_d7
run(hd7)
check(verdict(hd7, 'T35a') == 'PASS' and verdict(hd7, 'T35b') == 'PASS', 'T35a, T35b pass')
check(verdict(hd7, 'T35c') == 'FAIL' and 'CAS error' in rec(hd7, 'T35c '), rec(hd7, 'T35c '))
check(line(hd7, 'T35d') is None, 'T35d not tried after the break')
check(any(s.startswith('  works to 2002') for s in log(hd7)), 'the log names the last length that worked')
check('long CAS text: works to 2002 characters' in log(hd7), 'and the summary line says 2002')

say('')
say('== D8 (1a). an infinite limit prints as the glyph (the emulator; harness v3e) ==')
check('the glyph (8734)' in rec(h, 'T41a '), rec(h, 'T41a '))
check('an infinite limit prints: the glyph (8734)' in log(h), 'the summary line names the glyph')

say('')
say('== D9 (1a). device variant: BINOMIAL_CDF reads (n, k, p) ==')
hd9 = harness()
hd9._table['BINOMIAL_CDF'] = lambda a, site: (_ for _ in ()).throw(R.interp.PPLError('simulated: p = 2'))
run(hd9)
check(verdict(hd9, 'T42') == 'FAIL' and 'run-time error' in rec(hd9, 'T42 '), rec(hd9, 'T42 '))
check('BINOMIAL_CDF order (n, p, k): NO' in log(hd9), 'the summary line says NO')
hd9 = harness()
hd9._table['BINOMIAL_CDF'] = lambda a, site: 0.5
run(hd9)
check(verdict(hd9, 'T42') == 'FAIL' and '  = 0.500000 (SciPy 0.044179)' in log(hd9), 'a wrong value: %s' % line(hd9, 'T42'))

say('')
say('== D10 (1c). device variants for T43: the rules not as the emulator showed them ==')
hd10 = harness()
hd10._instring = lambda a: (0.0 if a[0] == '' else float(a[0].find(a[1]) + 1))
real_s = hd10._table['STRING']
hd10._table['STRING'] = lambda a, site: ('0.1' if len(a) == 3 and a[0] == 0.096 else real_s(a, site))
run(hd10)
check(verdict(hd10, 'T43a') == 'FAIL' and 'gave 0' in rec(hd10, 'T43a ') and verdict(hd10, 'T43b') == 'FAIL'
      and 'INSTRING of an empty string: NO error' in log(hd10) and 'STRING(0.096, 2, 1): NOT scientific' in log(hd10),
      '1c: INSTRING("") = 0 and STRING(0.096, 2, 1) = 0.1 give T43a, T43b FAIL and "NO" / "NOT" summary lines')
check(rec(hd10, 'T43b ') == 'T43b FAIL STRING(0.096, 2, 1) is not scientific'
      and '  = 0.1, codes 48 46 49 ' in log(hd10) and not any('exponent minus' in x for x in log(hd10)),
      '1d: the FAIL line reads "%s", the codes line follows, and no exponent-minus note (no exponent)'
      % rec(hd10, 'T43b '))

say('')
say('== D11 (1d). device variants for T43b: the exponent\'s minus a hyphen, no sign, an ASCII E ==')
D11 = [('9.6\u1d07-2', 'PASS', '  exponent minus: ASCII 45, a hyphen', 'scientific',
        'a hyphen (what harness v3d printed, and what beta 1c expected)'),
       ('9.6\u1d072', 'PASS', '  exponent minus: none', 'scientific',
        'no sign at all (not seen; the "none" branch)'),
       ('9.6E-2', 'FAIL', None, 'NOT scientific', 'an ASCII E (not the Prime\'s E: not scientific by T43b\'s test)')]
for txt_, v_, note_, sum_, why_ in D11:
    hd11 = harness()
    real_s11 = hd11._table['STRING']
    hd11._table['STRING'] = (lambda rs, t: (lambda a, site: (t if len(a) == 3 and a[0] == 0.096 else rs(a, site))))(
        real_s11, txt_)
    run(hd11)
    l11 = log(hd11)
    notes = [x for x in l11 if x.startswith('  exponent minus')]
    c11 = counts(hd11)
    want_c = (45, 8) if v_ == 'PASS' else (44, 9)
    check(verdict(hd11, 'T43b') == v_ and notes == ([note_] if note_ else [])
          and ('STRING(0.096, 2, 1): ' + sum_) in l11 and (c11['PASS'], c11['FAIL']) == want_c
          and c11['ERROR'] == 0,
          '1d: STRING(0.096, 2, 1) = %r, %s: T43b %s, %s, summary "%s", %d pass, %d fail'
          % (txt_, why_, v_, ('note "%s"' % note_.strip()) if note_ else 'no note', sum_, want_c[0], want_c[1]))

# ======================================================================= E
say('')
say('== E. layout: every text inside the screen (gate widths: f1 6, f2 7.6, f3 8.6 px) ==')
PX = {1: 6.0, 2: 7.6, 3: 8.6}
worst = []
for hh in (h,):
    for t in hh.texts:
        w = len(t.text) * PX.get(int(t.font or 1), 6.0)
        if t.x + w > 320:
            worst.append((t.x + w, t.func, t.text))
check(not worst, 'no TEXTOUT_P estimated past x = 320 (%d over)' % len(worst))
for w in sorted(worst, reverse=True)[:8]:
    say('   %.0f px  %s  %r' % w)

# ======================================================================= F
say('')
say('== F. the text helpers on edge inputs the full run does not reach ==')
hf = harness()
hf.call('cxInit')
F_CASES = [
    ('cxShort', ('abcdefghijklmnopqrstuvwxyz', 12.0), 'abcdefghi...'),
    ('cxShort', ('abc', 12.0), 'abc'),
    ('cxShort', ('x' * 60 + 'TAIL56789', 40.0), 'x' * 26 + ' ... ' + 'TAIL56789'),
    ('cxRest', ('abc', 4.0), ''),
    ('cxRest', ('abc', 2.0), 'bc'),
    ('cxSplit', ('noimport;', ';'), ['noimport', '']),
    ('cxSplit', ('a;b;c', ';'), ['a', 'b', 'c']),
    ('cxSplit', ('', ';'), ['']),
    ('cxPyType', ("<class 'str'>",), 'str'),
    ('cxPyType', ("odd'",), ''),
    ('cxPyType', ('plain',), 'plain'),
    ('cxToList', ('poly1[1,1,2]',), [1.0, 1.0, 2.0]),
    ('cxToList', ('list[1/20]',), [0.05]),
    ('cxToList', ('[]',), []),
    ('cxToList', ('no list',), []),
    ('cxStrip', ('"35/128"',), '35/128'),
    ('cxStrip', ('"',), '"'),
    ('cxFlat', ('a' + chr(10),), 'a / '),
    ('cxIStr', (-25.0,), '-25'),
    ('cxIStr', (0.0,), '0'),
    ('cxIStr', (123456789012.0,), '123456789012'),
    ('cxCodes', ('a−b﹐',), ' 8722 65104'),
    ('cxAllCodes', ('',), '(empty)'),
    # 1a
    ('cxShape', ('list[[2,1]]',), 'prefix list, [[]], commas'),
    ('cxShape', ('[1,4,9,16]',), '[], commas'),
    ('cxShape', ('{1;2}',), '{}, semicolons'),
    ('cxShape', ('cxt+1',), 'no brackets'),
    ('cxShape', ('poly1[1,1]',), 'prefix poly1, [], commas'),
    ('cxShape', ('',), 'no brackets'),
    ('cxMulSign', ('cxp*cxt+6',), '*'),
    ('cxMulSign', ('cxp·cxt',), 'middle dot (183)'),
    ('cxMulSign', ('cxp⋅cxt',), 'dot operator (8901)'),
    ('cxMulSign', ('cxp cxt',), 'none found'),
    # 1c: the round-2 rules -- an empty text, a break or separator at the start or the end
    ('cxFlat', ('',), ''),
    ('cxFlat', (chr(10) + 'a',), ' / a'),
    ('cxFlat', (chr(10),), ' / '),
    ('cxFlat', ('a' + chr(10) + chr(10) + 'b',), 'a /  / b'),
    ('cxFlat', ('plain',), 'plain'),
    ('cxSplit', (';a', ';'), ['', 'a']),
    ('cxSplit', (';', ';'), ['', '']),
    ('cxSplit', ('a;;b', ';'), ['a', '', 'b']),
    ('cxSplit', ('a;b', ''), ['a;b']),
    ('cxPyType', ('',), ''),
    ('cxPyType', ("'",), ''),
    ('cxPyType', ("''",), ''),
    ('cxPyType', ("a'b'c",), 'b'),
]
for fn, args, want in F_CASES:
    got = hf.call(fn, *args)
    if isinstance(want, list) and want and isinstance(want[0], float):
        ok = isinstance(got, list) and len(got) == len(want) and all(abs(a - b) < 1e-12 for a, b in zip(got, want))
    else:
        ok = got == want
    check(ok, '%s%r -> %r' % (fn, args, got))
# beta 1b on the same 1c edge inputs: stops, or loops (not run)
ho_f = harness(src=OLD)
ho_f.call('cxInit')
olds = []
for fn, args in (('cxFlat', ('',)), ('cxSplit', ('', ';')), ('cxSplit', ('noimport;', ';')), ('cxPyType', ("'",)),
                 ('cxSplit', (';a', ';')), ('cxPyType', ("''",))):
    try:
        olds.append('%s%r -> %r' % (fn, args, ho_f.call(fn, *args)))
    except Exception as x:
        olds.append('%s%r stops: %s' % (fn, args, str(x)[:28]))
say('   beta 1b, for comparison: ' + '; '.join(olds) + "; cxFlat(chr(10) + 'a') not run: LEFT(s, 0) is the "
    "whole string, so beta 1b's loop never ends")
check(sum('stops' in s for s in olds) == 4 and "cxSplit(';a', ';') -> [';a', 'a']" in olds
      and "cxPyType(\"''\",) -> \"'\"" in olds,
      '1c: beta 1b stops on 4 of them (INSTRING of "") and gets two wrong (LEFT(s, 0) = the whole string)')
# the word wrap: a time is never split, digits are cut at 46, nothing exceeds 46
hf.globals_['CX_LOG'] = []
hf.call('cxNote', 'T08 PASS EXPR CAS(q s q) form: 30 digits (1234 ms)')
hf.call('cxNote', 'D' * 100)
hf.call('cxNote', 'T09 PASS EXPR CAS.eval(q s q) form: 30 digits (1 ms)')
L = list(hf.globals_['CX_LOG'])
say('   ' + ' | '.join(L))
check(L[0] == 'T08 PASS EXPR CAS(q s q) form: 30 digits' and L[1] == '  (1234 ms)',
      'a time moves to the next line whole')
check(L[2] == 'D' * 46 and L[3] == '  ' + 'D' * 44 and L[4] == '  ' + 'D' * 10, 'digits are cut at 46')
check(all(len(s) <= 46 for s in L), 'no line over 46')
# cxLineCol on an empty line (the pager)
check(hf.call('cxLineCol', '') == 0 and hf.call('cxLineCol', 'T01 PASS x') == hf.globals_['cxGRN'],
      '1c: cxLineCol("") is black, no error; a PASS line is green')

# ======================================================================= G
say('')
say('== G (1d). beta 1d against beta 1c (the version the emulator ran), and against beta 1b as before ==')
t0_, tp_, t1_ = open(OLD, encoding='utf-8').read(), open(PREV, encoding='utf-8').read(), SRC_TEXT


def _bodies(txt):
    c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', txt)
    c = re.sub(r'//[^\n]*', '', c)
    out = {}
    for m_ in re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
        out[m_.group(1)] = re.sub(r'\n\s*\n', '\n', re.sub(r'[ \t]+\n', '\n', m_.group(0)))
    return out


def _outside(t, names):
    c = re.sub(r'(?ms)^#PYTHON.*?^#END', '', re.sub(r'//[^\n]*', '', t))
    c = re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return re.sub(r'\s+', ' ', c)


# 1d: against beta 1c
B0, BP, B1 = _bodies(t0_), _bodies(tp_), _bodies(t1_)
diff_p = sorted(n for n in set(BP) | set(B1) if BP.get(n) != B1.get(n))
want_p = sorted(['CASProbe', 'cxBegin', 'cxSummary', 'cxT43'])
say('   routines that differ from beta 1c: %s' % diff_p)
check(diff_p == want_p, '1d: the routines that differ from beta 1c are exactly %s' % ', '.join(want_p))
check(all(BP[n].replace('CASProbe beta 1c', 'CASProbe beta 1d') == B1[n] for n in ('CASProbe', 'cxBegin', 'cxSummary')),
      '1d: in CASProbe, cxBegin and cxSummary the only change is the version string "CASProbe beta 1c" -> '
      '"CASProbe beta 1d" (menu title, log line, progress and summary titles); "-- T43 (added in beta 1c) --" stays')
import difflib
dl = [d_ for d_ in difflib.unified_diff(BP['cxT43'].split('\n'), B1['cxT43'].split('\n'), 'beta 1c', 'beta 1d',
                                         n=0, lineterm='') if d_[:1] in '+-' and d_[:3] not in ('---', '+++')]
say('   cxT43, code lines (comments left out), beta 1c -> beta 1d:')
for d_ in dl:
    say('     ' + d_)
want_dl = ['-  LOCAL sxA, sxB, sxC, sxE;',
           '-  IF sxB == "9.6" + CHAR(7431) + "-2" THEN cxSci := 1; END;',
           '-    cxRec("T43b", "FAIL", "STRING(0.096, 2, 1) is not 9.6E-2", -1);',
           '+  LOCAL sxA, sxB, sxC, sxE, sxM;',
           '+  IF DIM(sxB) > 0 THEN',
           '+    IF INSTRING(sxB, CHAR(7431)) > 0 THEN cxSci := 1; END;',
           '+  END;',
           '+    cxRec("T43b", "FAIL", "STRING(0.096, 2, 1) is not scientific", -1);',
           '+  IF cxSci == 1 THEN',
           '+    sxM := "none";',
           '+    IF INSTRING(sxB, CHAR(7431) + "-") > 0 THEN sxM := "ASCII 45, a hyphen"; END;',
           '+    IF INSTRING(sxB, CHAR(7431) + CHAR(8722)) > 0 THEN sxM := "CHAR(8722), Home\'s minus"; END;',
           '+    cxNote("  exponent minus: " + sxM);',
           '+  END;']
check(sorted(dl) == sorted(want_dl),
      '1d: in cxT43 only T43b changed: one LOCAL (sxM), the test (CHAR(7431) anywhere, DIM first), the FAIL '
      'text, and the exponent-minus note')
op_, o1p = _outside(tp_, diff_p), _outside(t1_, diff_p)
check(op_ == o1p, '1d: outside those four routines only comments differ (no new file-level LOCAL)')
check(re.findall(r'(?ms)^#PYTHON.*?^#END', tp_) == re.findall(r'(?ms)^#PYTHON.*?^#END', t1_)
      and re.findall(r'(?ms)^#PYTHON.*?^#END', t0_) == re.findall(r'(?ms)^#PYTHON.*?^#END', t1_),
      '1d: the two #PYTHON blocks are byte-identical to beta 1c\'s and beta 1b\'s')
check(all(BP[n] == B1[n] and B0[n] == B1[n] for n in ('cxCall', 'cxObj', 'cxPickForm')),
      '1c/1d: cxCall, cxObj and cxPickForm (the probe\'s own call forms) are unchanged')
# as before: against beta 1b
diff = sorted(n for n in set(B0) | set(B1) if B0.get(n) != B1.get(n))
want = sorted(['CASProbe', 'cxBegin', 'cxCas', 'cxFlat', 'cxInit', 'cxLineCol', 'cxPyType', 'cxRun', 'cxSplit',
               'cxSummary', 'cxT25', 'cxT34', 'cxT39', 'cxT43'])
say('   routines that differ from beta 1b: %s' % diff)
check(diff == want, '1c/1d: the routines that differ from beta 1b are still exactly beta 1c\'s 14: %s' % ', '.join(want))
o0, o1 = _outside(t0_, diff), _outside(t1_, diff)
check(o1.replace(' LOCAL cxIns0, cxSci;', '') == o0,
      '1c/1d: outside them only comments differ from beta 1b, and one new file-level LOCAL line (cxIns0, cxSci)')


def _nocomment(l):
    q = False
    for j, ch in enumerate(l):
        if ch == '"':
            q = not q
        elif not q and l[j:j + 2] == '//':
            return l[:j]
    return l


code_lines = [_nocomment(ln) for ln in re.sub(r'(?ms)^#PYTHON.*?^#END', '', t1_).split('\n')]
v1b = [ln for ln in code_lines if 'beta 1b' in ln]
v1c = [ln.strip() for ln in code_lines if 'beta 1c' in ln]
check(not v1b and v1c == ['cxNote("-- T43 (added in beta 1c) --");']
      and t1_.count('"CASProbe beta 1d"') == 1 and 'CASProbe beta 1d: summary' in t1_
      and 'CASProbe beta 1d: running' in t1_ and 'CASProbe beta 1d, 17 Oct 2026 build' in t1_
      and t1_.split('\n')[2].startswith('//  CASProbe beta 1d  --'),
      '1d: every on-screen and log version string, and the banner, reads beta 1d; the only code line that says '
      'beta 1c is the log marker "-- T43 (added in beta 1c) --" (history, as "added in beta 1a"); the #PYTHON '
      'comments keep beta 1b')

# ======================================================================= H
say('')
say('== H (1c/1d). the scientific STRING results, and every INSTRING, LEFT, MID ==')
new_h = [x for x in HARNESSES if x.vpath == os.path.basename(SRC)]
new_s = sorted(set((r, t) for x in new_h for r, t in x.sci_where))
say('   beta 1d: %d harness runs, scientific STRING results: %s' % (len(new_h), new_s))
check(new_s == [('cxT43', '9.6\u1d07-2')],
      '1d: the only scientific STRING result in every beta 1d run is T43b\'s own STRING(0.096, 2, 1) = 9.6E-2 '
      '(h.sci_strings keeps the hyphen form in v3e; the program got U+2212 there, C0/C1)')


def _code(t):
    out = []
    for l in t.split('\n'):
        q = False
        cut = len(l)
        for j, ch in enumerate(l):
            if ch == '"':
                q = not q
            elif not q and l[j:j + 2] == '//':
                cut = j
                break
        out.append(l[:cut])
    return out


def _calls(name, code):
    out = []
    for m_ in re.finditer(r'(?<![A-Za-z_])' + name + r'\(', code):
        if code[:m_.start()].count('"') % 2:
            continue
        j = m_.end(); d = 1; cur = ''; parts = []; q = False
        while j < len(code) and d > 0:
            c = code[j]
            if c == '"':
                q = not q
            if not q:
                if c in '([{': d += 1
                elif c in ')]}': d -= 1
            if d == 0:
                break
            if c == ',' and d == 1 and not q:
                parts.append(cur.strip()); cur = ''
            else:
                cur += c
            j += 1
        parts.append(cur.strip())
        out.append(parts)
    return out


code = _code(re.sub(r'(?ms)^#PYTHON.*?^#END', lambda m_: '\n' * m_.group(0).count('\n'), t1_))
s2 = [(i + 1, a) for i, ln in enumerate(code) for a in _calls('STRING', ln) if len(a) == 3 and a[1] == '2']
say('   STRING(x, 2, d) in beta 1d: %s' % s2)
check([a[0] for _, a in s2] == ['bV', '0.096', 'ROUND(0.096, 1)'],
      '1c: three fixed-decimal STRINGs: T42\'s value (0.044179 unless BINOMIAL_CDF is itself wrong, and then '
      'the scientific form is the honest record), and T43\'s two, on purpose')
ins = [(i + 1, a) for i, ln in enumerate(code) for a in _calls('INSTRING', ln)]
firsts = collections.Counter(a[0] for _, a in ins)
say('   INSTRING first arguments (%d calls): %s' % (len(ins), dict(firsts)))
SAFE_INS = {
    'cR': 'cxCas: inside IF DIM(cR) > 0 (1c)',
    'fT': 'cxFlat: only when DIM(fT) > 0 (1c)',
    'pT': 'cxSplit: only when DIM(pT) > 0 (1c)',
    'hR': 'cxHas: only when cxErr = 0, and then the answer is STRING() of something, never ""',
    'fT ': '',
    'qA': 'T23, T36a: only when cxErr = 0 (STRING() of the answer)',
    'vA': 'T25: only when DIM(vA) > 0 (1c)',
    'vD': 'T25: only when DIM(vD) > 0 (1c)',
    'rA': 'T26: only when cxErr = 0',
    'kS': 'cxShape: an empty text has no bracket and has returned "no brackets" before',
    'mS': 'cxMulSign: T38a calls it only when cxErr = 0',
    'jR': 'cxHas2: only when cxErr = 0',
    'sA': 'T39: inside IF DIM(sA) > 0 (1c), and T39b only when cxErr = 0',
    'iA': 'T41a: only when cxErr = 0',
    'yS': 'cxPyType: after IF DIM(yS) == 0 THEN RETURN (1c)',
    'yR': 'cxPyType: after IF DIM(yR) == 0 THEN RETURN (1c)',
    'pL(5)': 'T34b: only when DIM(pL(5)) > 0 (1c)',
    'lS': 'cxLineCol: after IF DIM(lS) == 0 THEN RETURN (1c)',
    '""': 'T43a: on purpose, inside IFERR',
    'sxB': 'T43b: STRING() of 0.096, never ""; inside IF DIM(sxB) > 0, then only when cxSci = 1 (1d)',
}
SAFE_INS.pop('fT ')
# cxVerdict50's fT: tested only in the ELSE of IF fT == ""
check(set(firsts) <= set(SAFE_INS) | {'fT'} and len(ins) == 44 and firsts['sxB'] == 3,
      '1c/1d: every INSTRING\'s first argument is guarded or cannot be "" (%d calls, beta 1c\'s 41 and T43b\'s 3; '
      'unlisted: %s)'
      % (len(ins), sorted(set(firsts) - set(SAFE_INS) - {'fT'}) or 'none'))
for k_, why in sorted(SAFE_INS.items()):
    say('     %-6s %s' % (k_, why))
say('     fT     cxFlat (guarded, 1c) and cxVerdict50 (only in the ELSE of IF fT == "")')
lm = [(nm, a) for ln in code for nm in ('LEFT', 'MID', 'RIGHT') for a in _calls(nm, ln)]
lefts = [a[1] for nm, a in lm if nm == 'LEFT']
mids = [a[1] for nm, a in lm if nm == 'MID']
say('   LEFT counts: %s' % lefts)
say('   MID starts: %s' % mids)
check(not any(nm == 'RIGHT' for nm, a in lm)
      and set(lefts) <= {'nL', 'nB - 1', 'fPos - 1', 'sN - 3', 'sN - 14', '1', 'pP - 1', '6', 'kP - 1', 'yA - 1'},
      '1c: every LEFT count is 1 or more: nL = 46; nB - 1 >= 24; fPos - 1, pP - 1, kP - 1 and yA - 1 only past 1; '
      'sN - 3 >= 9; sN - 14 >= 10; 6 when DIM >= 6')
check(set(mids) <= {'rK', 'nB', 'nB + 1', 'sD - 8', 'tD', '2', 'tI', 'tA + 1', 'gD - 5', 'kI'},
      '1c: every MID start is 1 or more: rK > 1 from every caller; nB >= 25; sD - 8 >= 16; gD - 5 >= 1 '
      '(gD >= 6); tA + 1, tI, kI >= 1')

# ======================================================================= the end
say('')
say('%d check(s) failed of %d' % (len(FAILS), NCHK[0]) if FAILS else 'ALL CHECKS PASS: %d checks' % NCHK[0])
for f_ in FAILS:
    say('   FAILED: ' + f_)
open(os.path.join(HERE, 'verify_CASProbe_beta1d_output.txt'), 'w').write('\n'.join(OUT) + '\n')
sys.exit(1 if FAILS else 0)
