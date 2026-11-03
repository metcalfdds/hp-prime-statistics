#!/usr/bin/env python3
"""comma_check_v1.py -- the check behind round 5's verify scripts (commas in big numbers, Nov 2026).

Roger, 2 Nov 2026: "always put comma delimiters in big numbers".  Round 5 gave every program a routine that puts a
comma every three digits into the numbers it draws (tools/commas_v1.py made each version from the one before, by
rules; tools/commas_config_r5.py says which routines are which).  A verify script of round 5 calls check(...) here:

  G  static: the comma routine is the fleet's, word for word but its name; with every call of it taken out, the new
     code is the old code, routine for routine, except the routines its configuration names (exact edits) and the
     ones it adds; nothing the CAS or EXPR reads goes through it; no "!="; the code still ASCII if it was; the
     header names the new version.
  R  the monkey (tools/monkey_v1b.py: random keys, taps, menu picks, typed values, with 1000, 2500, 12345, 54321.5
     and 100000 among them) runs each seed on both versions.  R1: each run takes the old version's path -- the same
     ending, number of screens, boxes and returned summary once the commas are out.  R2 (information): every screen's
     texts are the old version's once the commas are out, but where a number with its commas no longer fits and the
     program writes it another way (an axis in units, a label left out, the scientific form): those are counted;
  M  every number of four or more digits the new version draws is grouped, unless the program writes it as text;
  Y  no number the program writes as text (a year in a citation) is drawn with a comma;
  D  no new firm overlap, straddle or overrun (text_overlap_v1) and no new number cut by its width (label_fit_v1).

As a command:  python3 comma_check_v1.py OLD.txt NEW.txt CALL HELPER [--runs N] [--seconds S] [--ver "OLD|NEW"]
"""
import os
import random
import re
import signal
import sys
import time
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
EXTRA = [1000, 2500, 12345, 54321.5, 100000]
HEAD = re.compile(r'^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z_]\w*)\(([^()]*)\)\s*(?://.*)?$')


# ------------------------------------------------------------------ static
def strip_comments(t):
    out = []
    for ln in t.split('\n'):
        q, i, res = False, 0, ''
        while i < len(ln):
            ch = ln[i]
            if ch == '"':
                q = not q
            if not q and ln[i:i + 2] == '//':
                break
            res += ch
            i += 1
        out.append(res.rstrip())
    return '\n'.join(x for x in out if x.strip())


def unwrap(t, helper):
    """every helper(X) replaced by X (string literals are left alone)"""
    pat = re.compile(r'(?<![\w.])%s\(' % re.escape(helper))
    while True:
        m = pat.search(t)
        if not m:
            return t
        i, d, q = m.end() - 1, 0, False
        for j in range(i, len(t)):
            ch = t[j]
            if ch == '"':
                q = not q
            elif not q and ch == '(':
                d += 1
            elif not q and ch == ')':
                d -= 1
                if d == 0:
                    break
        t = t[:m.start()] + t[i + 1:j] + t[j + 1:]


def routines(t):
    lines = t.split('\n')
    heads = [(i, HEAD.match(ln).group(1)) for i, ln in enumerate(lines)
             if HEAD.match(ln) and i + 1 < len(lines) and lines[i + 1].strip().upper().startswith('BEGIN')]
    out = {}
    for q, (i, nm) in enumerate(heads):
        e = heads[q + 1][0] if q + 1 < len(heads) else len(lines)
        body = lines[i:e]
        # the routine ends at its END; (comments and text between routines are not code of it)
        for z in range(len(body) - 1, -1, -1):
            if body[z].strip() == 'END;':
                body = body[:z + 1]
                break
        out[nm] = '\n'.join(body)
    return out


HELPER_BODY = None


def helper_text(src, helper):
    r = routines(src).get(helper)
    return strip_comments(r.replace(helper, 'HELPER')) if r else None


def static(old_src, new_src, helper, allowed, added, new_ver, cas_names):
    """G checks: list of (name, ok, detail)"""
    res = []
    ref = open(os.path.join(HERE, 'comma_helper_reference_v1.txt'), encoding='utf-8').read()
    h = helper_text(new_src, helper)
    res.append(('G1 the comma routine %s is the fleet\'s, word for word but its name' % helper,
                h is not None and h == strip_comments(ref), '' if h else 'missing'))
    ro, rn = routines(strip_comments(old_src)), routines(strip_comments(unwrap(new_src, helper)))
    diff = sorted(k for k in set(ro) | set(rn) if ro.get(k) != rn.get(k))
    want = sorted(set(allowed) | set(added) | {helper})
    res.append(('G2 with every %s(...) taken out, the code is the old code routine for routine, but for %s'
                % (helper, ', '.join(want)), set(diff) <= set(want), sorted(set(diff) - set(want))))
    code = strip_comments(new_src)
    bad = []
    for m in re.finditer(r'(?<![\w.])(EXPR|CAS|%s)\s*\(' % '|'.join(re.escape(c) for c in cas_names or ['_none_']), code):
        i, d, q = m.end() - 1, 0, False
        for j in range(i, len(code)):
            ch = code[j]
            if ch == '"':
                q = not q
            elif not q and ch == '(':
                d += 1
            elif not q and ch == ')':
                d -= 1
                if d == 0:
                    break
        if re.search(r'(?<![\w.])%s\(' % re.escape(helper), code[i:j]):
            bad.append(code[m.start():m.start() + 60])
    res.append(('G3 nothing the CAS or EXPR reads goes through %s' % helper, not bad, bad[:3]))
    n_old, n_new = strip_comments(old_src).count('!='), code.count('!=')
    res.append(('G4 no new "!=" in the code (a factorial and a test on the Prime; %d before, in MicroPython text where '
                'it is "not equal")' % n_old, n_new == n_old, (n_old, n_new)))
    ascii_old = all(ord(c) < 128 for c in strip_comments(old_src))
    res.append(('G5 the code is ASCII%s' % (' as before' if ascii_old else ' where it was (it was not before)'),
                (not ascii_old) or all(ord(c) < 128 for c in code), ''))
    hdr = [ln for ln in new_src.split('\n')[:40] if new_ver in ln]
    res.append(('G6 the header names %s' % new_ver, bool(hdr), ''))
    return res


# ------------------------------------------------------------------ the runs
def runs(old, new, call, n, seconds, ver, norm=None):
    """R, M, Y, D: a dict with the results.  norm: a text -> text map applied to both versions' texts before R compares
    them, for a change the round makes on purpose (GaltonBoard's bar labels: 1.0k became 1,093)"""
    cwd = os.getcwd()
    os.chdir(HERE)
    import text_overlap_v1 as OV
    OV.install()
    import label_fit_v1 as LF
    argv = sys.argv
    sys.argv = ['monkey_v1b.py']
    import monkey_v1b as M
    sys.argv = argv
    os.chdir(cwd)
    if 1000 not in M.NUMS_ORDINARY:
        M.NUMS_ORDINARY = list(M.NUMS_ORDINARY) + EXTRA
    vo, vn = (ver.split('|') + [''])[:2] if ver else ('', '')

    def nc(x):
        if isinstance(x, str):
            x = x.replace(',', '')
            x = x.replace(vn, vo) if vn else x
            return norm(x) if norm else x
        if isinstance(x, (list, tuple)):
            return type(x)(nc(y) for y in x)
        return x

    # C: every text the program hands the CAS or EXPR, call by call (the harness's own entry points); the two versions
    # must hand over the same texts, since the commas are for the screen only
    CASLOG = []
    if not getattr(M.R.Harness, '_cc_logged', False):
        _ce, _ex = M.R.Harness._cas_eval, M.R.Harness._expr

        def _cas_eval(self, expr, _f=_ce):
            CASLOG.append('CAS ' + str(expr))
            return _f(self, expr)

        def _expr(self, a, _f=_ex):
            CASLOG.append('EXPR ' + str(a[0] if a else ''))
            return _f(self, a)
        M.R.Harness._cas_eval, M.R.Harness._expr, M.R.Harness._cc_logged = _cas_eval, _expr, True
        M.R.Harness._cc_log = CASLOG
    CASLOG = M.R.Harness._cc_log

    def one(path, seed):
        del CASLOG[:]
        rng = random.Random(seed)
        app, kind = M.random_lists(rng)
        h = M.Monkey(path, rng, app, 150)
        for q in range(10):
            h.globals_.setdefault('M%d' % q, M.R.interp.Matrix([[0.0]]))
        m1, mk = M.random_matrix(seed)
        if m1 is not None:
            h.globals_['M1'] = m1
        verdict = 'OK'
        signal.signal(signal.SIGALRM, M._alarm)
        signal.alarm(seconds)
        try:
            h.execute(call)
        except M.TimeUp:
            verdict = 'FREEZE'
        except Exception as e:
            verdict = 'END ' + type(e).__name__
        finally:
            signal.alarm(0)
        return (verdict, [tuple(t.text for t in s.texts) for s in h.screens], [' '.join(m.lines) for m in h.msgboxes],
                str(h.result), list(CASLOG))

    src = open(new, encoding='utf-8').read()
    litlist = re.findall(r'"([^"\n]*)"', '\n'.join(ln.split('//')[0] if ln.count('"') % 2 == 0 else ln
                                                    for ln in src.split('\n')))
    lits = ' | '.join(litlist)

    def year_text(txt, m):
        """a grouped 1,500 ... 2,099 drawn in the program's own wording: some literal holds that number as text,
        and the drawn text, with this number's comma taken out, shows the literal's words beside it (3 characters
        or more on one side); a literal that is the number alone counts too.  "n = 1,980 (x10)" beside a literal
        "Lenihan (1980) via" is a count, not the year."""
        d = m.group(0).replace(',', '')
        t2 = txt[:m.start()] + d + txt[m.end():]
        for lit in litlist:
            for mm in re.finditer(r'(?<![\d.])%s(?!\d)' % d, lit):
                i = mm.start()
                left = lit[max(0, i - 5):i + 4] if i >= 3 else None
                right = lit[i:i + 9] if len(lit) - (i + 4) >= 3 else None
                if (left is None and right is None) or (left and left in t2) or (right and right in t2):
                    return True
        return False
    run4 = re.compile(r'(?<![\d.,])\d{4,}')
    r_bad, r_txt, m_bad, y_bad, verd = [], [], {}, {}, {}
    c_bad, n_cas = [], 0
    grouped = {}      # each grouped number drawn on the new version's runs: the check had numbers to look at
    OV.RECORDS.clear()
    def firm(rep, fn):
        f = rep.get(fn)
        if not f:
            return set()
        out = {('overlap', nc(c['a'][:30]), nc(c['b'][:30])) for c in f['collisions']
               if c['severity'] == 'overlap' and c['firm']}
        out |= {('straddle', nc(x['text'][:30])) for x in f['straddles'] if x['firm']}
        out |= {('overrun', nc(x['text'][:30])) for x in f['overruns'] if x['firm']}
        return out

    on, nn = os.path.basename(old), os.path.basename(new)
    ACC = {'fo': set(), 'fn': set(), 'co': set(), 'cn': set()}

    def take():
        """the overlap and cut findings of one seed's two runs, kept; then the records are dropped, so a long run
        (GaltonBoard's thousands of balls) does not fill the memory"""
        rep_ = OV.report()
        ACC['fo'] |= firm(rep_, on)
        ACC['fn'] |= firm(rep_, nn)
        cut_ = LF.clipped(OV.RECORDS)
        ACC['co'] |= {nc(x[0]) for x in cut_.get(on, [])}
        ACC['cn'] |= {nc(x[0]) for x in cut_.get(nn, [])}
        OV.RECORDS.clear()

    t0 = time.time()
    for k in range(n):
        seed = 5000 + k
        a, b = one(old, seed), one(new, seed)
        take()
        n_cas += len(b[4])
        verd[b[0]] = verd.get(b[0], 0) + 1
        if 'FREEZE' in (a[0], b[0]) and a[0] == b[0]:
            # a run stopped by the clock stops wherever the clock says: compare the screens both reached, but the last
            n_ = min(len(a[1]), len(b[1])) - 1
            n_c = min(len(a[4]), len(b[4]))
            a, b = (a[0], a[1][:n_], a[2][:0], '', a[4][:n_c]), (b[0], b[1][:n_], b[2][:0], '', b[4][:n_c])
        if a[4] != b[4] and (a[0], len(a[1])) == (b[0], len(b[1])):
            i = next((i for i in range(min(len(a[4]), len(b[4]))) if a[4][i] != b[4][i]), min(len(a[4]), len(b[4])))
            c_bad.append((seed, a[4][i][:80] if i < len(a[4]) else None, b[4][i][:80] if i < len(b[4]) else None))
        if (a[0], len(a[1]), nc(a[2]), nc(a[3])) != (b[0], len(b[1]), nc(b[2]), nc(b[3])):
            # a different path: another ending, another number of screens, another box or summary
            i = next((i for i in range(min(len(a[1]), len(b[1]))) if nc(a[1][i]) != nc(b[1][i])),
                     min(len(a[1]), len(b[1])))
            r_bad.append((seed, a[0], b[0], len(a[1]), len(b[1]), i,
                          [x for x in (a[1][i] if i < len(a[1]) else ()) if nc(x) not in
                           nc(b[1][i] if i < len(b[1]) else ())][:2],
                          [x for x in (b[1][i] if i < len(b[1]) else ()) if nc(x) not in
                           nc(a[1][i] if i < len(a[1]) else ())][:2]))
        else:
            for i in range(len(a[1])):
                if nc(a[1][i]) != nc(b[1][i]):
                    r_txt.append((seed, i, [x for x in a[1][i] if nc(x) not in nc(b[1][i])][:2],
                                  [x for x in b[1][i] if nc(x) not in nc(a[1][i])][:2]))
        for txt in [x for s in b[1] for x in s] + b[2] + [b[3]]:
            for m in run4.finditer(txt):
                if m.group(0) not in lits:
                    m_bad.setdefault(m.group(0), txt[:70])
            for m in re.finditer(r'\d,{2,}\d', txt):        # a number grouped twice ("1,,000")
                m_bad.setdefault(m.group(0), txt[:70])
            for m in re.finditer(r'(?<![\d.,])\d{1,3}(?:,\d{3})+(?![\d,])', txt):
                grouped.setdefault(m.group(0), 0)
                grouped[m.group(0)] += 1
            for m in re.finditer(r'(?<![\d.,])\d,\d{3}(?![\d,])', txt):
                d = m.group(0).replace(',', '')
                if 1500 <= int(d) <= 2099 and year_text(txt, m):
                    y_bad.setdefault(m.group(0), txt[:70])
            # a name with digits in it ("x1000", "D8S1179") never gets a comma: a letter just before a grouped run
            for m in re.finditer(r'(?<=[A-Za-z])\d{1,3}(?:,\d{3})+(?![\d,])', txt):
                y_bad.setdefault(m.group(0), txt[:70])
    fo, fn, co, cn = ACC['fo'], ACC['fn'], ACC['co'], ACC['cn']
    return {'n': n, 'secs': round(time.time() - t0), 'verdicts': verd, 'r_bad': r_bad, 'r_txt': r_txt, 'm_bad': m_bad,
            'y_bad': y_bad, 'grouped': grouped, 'c_bad': c_bad, 'n_cas': n_cas, 'd_new': sorted(fn - fo), 'c_new': sorted(cn - co), 'firm_old': len(fo),
            'firm_new': len(fn), 'cut_old': len(co), 'cut_new': len(cn)}


def report(res, exempt_m=(), exempt_y=(), exempt_r=()):
    """(name, ok, detail) lines for R, M, Y, D, and an INFO line (ok None) for R2; exempt_*: digit runs, or seeds,
    the verify script accepts, each with its reason in the script"""
    m_left = {k: v for k, v in res['m_bad'].items() if k not in exempt_m}
    y_left = {k: v for k, v in res['y_bad'].items() if k not in exempt_y}
    r_left = [x for x in res['r_bad'] if x[0] not in exempt_r]
    nsc = len(res['r_txt'])
    return [
        ('R1 %d seeds (%s): each run takes the old version\'s path: the same ending, number of screens, boxes and '
         'summary once the commas are out (%d accepted as the script says)'
         % (res['n'], res['verdicts'], len(res['r_bad']) - len(r_left)), not r_left, r_left[:3]),
        ('R2 every screen\'s texts the old version\'s once the commas are out, but %d screen(s): where a number with '
         'its commas no longer fit and the program wrote it another way, or where this version changes a text on '
         'purpose (its change note says which); the first: %s' % (nsc, res['r_txt'][:3]), None, ''),
        ('M  every number of four or more digits drawn is grouped: %d different grouped numbers drawn%s; %d drawn '
         'without their commas or with them twice, %d of them accepted as the script says'
         % (len(res.get('grouped', {})), (' (' + ', '.join(sorted(res.get('grouped', {}), key=lambda g: -res['grouped'][g])[:4])
                                         + ' …)') if res.get('grouped') else '',
            len(res['m_bad']), len(res['m_bad']) - len(m_left)), not m_left, list(m_left.items())[:4]),
        ('C  every text handed to the CAS or EXPR is the old version\'s, call for call (%d calls on the new version\'s '
         'runs; a run that took another path is R1\'s)' % res.get('n_cas', 0), not res.get('c_bad'), res.get('c_bad', [])[:3]),
        ('Y  no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")', not y_left, list(y_left.items())[:4]),
        ('D  no new firm overlap, straddle or overrun (old %d, new %d) and no new number cut (old %d, new %d)'
         % (res['firm_old'], res['firm_new'], res['cut_old'], res['cut_new']),
         not res['d_new'] and not res['c_new'], (res['d_new'][:3], res['c_new'][:3]))]


if __name__ == '__main__':
    a = sys.argv[1:]

    def opt(name, dflt):
        if name in a:
            i = a.index(name)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return dflt
    nruns, secs, ver = int(opt('--runs', '30')), int(opt('--seconds', '30')), opt('--ver', '')
    old, new, call, helper = a[:4]
    res = runs(old, new, call, nruns, secs, ver)
    bad = 0
    for nm, ok, det in report(res):
        print(('INFO ' if ok is None else 'PASS ' if ok else 'FAIL ') + nm + ('' if ok in (True, None) else '   ' + str(det)[:400]))
        bad += ok is False
    sys.exit(1 if bad else 0)
