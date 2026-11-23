# -*- coding: utf-8 -*-
"""verify_round19_v1.py -- Round 19 (23 Nov 2026): StatDist v2.7p and EpiStats v1.7o.

  B   THE BUILD (verify/round19/make_round19.py) makes each filed program byte for byte.
  T1  Only the round's lines changed: every line that differs from the old version is the build's (a replacement, the
      history note, the header, or a quoted string that holds the version).
  G   THE GATE (tools/ppl_gate_v1e.py) passes each new version against its old one (verify/round19/gates/).
  S   STATDIST'S FORMULA PAGE, driven as a student does (Advanced Continuous, the family, Probability Type 2, the form,
      Enter, "Formula page (CAS)"), with every CAS call timed:
        S1  t at df 17.83, 206.3, 30.1 and 0.83; F at df 7 and 17.83 and at 7.5 and 17.5; Burr XII at C = 2.37 and at 2.5, 3.5: no
            integral goes to the CAS, the gray line says why, and the page shows "no closed form shown" and the
            program's own values.  The old version, at df 17.83, is the comparison: its E[X^2] call does not end in
            the harness's 60 s.
        S2  t at df 24, 17.5 and 1; F at 7 and 18; Burr XII at C = 2, K = 3, S = 1 and S = 1.83: the CAS is asked as
            before, every call ends within 5 s, and the page reads as the old version's does.
        S3  Another family (Normal, Gamma, Beta, with parameters to two decimals): the page is the old version's,
            line for line.
  E   EPISTATS' STRATIFIED RATES GRID:
        E1  The four-value form (es_AskAll, esMod 7): a person-time of 1E-300, 0.5 or 0.999 in either field is
            refused with the round's sentence and the grid does not change; 0, 1 and 100,000 are taken; 100,000.5
            is refused with the cap's sentence, as before; Cancel changes nothing.  The case-control grid (esMod 5)
            still takes 0.5 and rounds it, with its own sentence.
        E2  The one-cell form (es_Grid through es_StratGrids(3)): 0.5 in a person-time cell is refused with the
            sentence and the cell keeps its value; 1 is taken.  The old version took 0.5.
        E3  The help lines of the two forms give the range and fit (at most 47 characters show).
        E4  es_MHCalc, the rate ratio, on every pair of strata of the floor sweep's grid at the floor (cases 0, 1 and
            100,000; person-times 0, 1 and 100,000) that stays inside the harness's EXP: the same E and interval as
            the formula worked in Python, to 1E-9 relative.  The 1E-300 table of round 18 is now refused at entry.
  R   The two runs of round 18's monkey that stopped, replayed with their own seeds on the new versions: both end OK.
  M   The start routines in the harness (idle key Esc): no error, and no more warnings than the old versions.
  N   tools/fleet_names_v2.py and tools/screen_text_v1.py over the 31 newest programs.

Run from the repository's root:   python3 verify/verify_round19_v1.py        (about five minutes; its output is beside it)
"""
import difflib, io, json, os, re, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.path.insert(0, os.path.join(HERE, 'round19'))
import make_round19 as M  # noqa: E402
import ppl_run_v3e as PR  # noqa: E402
from ppl_run_v3e import Harness, Key, KEY, CANCEL  # noqa: E402

OUT = []


def say(tag, name, ok, what):
    line = '%-3s %-9s %-4s %s' % (tag, name, 'OK' if ok else 'FAIL', what)
    OUT.append((ok, line)); print(line, flush=True)


PAIRS = [(n, ov, M.R18.nxt(ov)) for n, ov in M.OLD.items()]
old = {n: M.old_text(n, ov) for n, ov, nv in PAIRS}
newf = {n: os.path.join(REPO, 'programs', '%s_%s.txt' % (n, nv)) for n, ov, nv in PAIRS}
new = {n: io.open(newf[n], encoding='utf-8', newline='').read() for n in newf}
tmp = tempfile.mkdtemp(prefix='r19ver_')
oldf = {}
for n, ov, nv in PAIRS:
    oldf[n] = os.path.join(tmp, '%s_%s.txt' % (n, ov))
    io.open(oldf[n], 'w', encoding='utf-8', newline='').write(old[n])

# ------------------------------------------------------------------ B, the build
bd = os.path.join(tmp, 'build')
subprocess.run([sys.executable, os.path.join(HERE, 'round19', 'make_round19.py'), bd], check=True, capture_output=True)
for n, ov, nv in PAIRS:
    b = io.open(os.path.join(bd, '%s_%s.txt' % (n, nv)), encoding='utf-8', newline='').read()
    say('B', n, b == new[n], 'the build makes %s %s byte for byte (%s lines)' % (n, nv, '{:,}'.format(new[n].count('\n') + 1)))

# ------------------------------------------------------------------ T1, only the round's lines
for n, ov, nv in PAIRS:
    allowed_new = set()
    for a, b in M.REPL[n]:
        allowed_new.update(b.split('\n'))
    allowed_old = set()
    for a, b in M.REPL[n]:
        allowed_old.update(a.split('\n'))
    ol, nl = old[n].split('\n'), new[n].split('\n')
    hist = [i for i, l in enumerate(nl) if l.startswith('// %s (%s): Round 19:' % (M.R18.tag(nv), M.DATE))]
    h0 = hist[0] if hist else -1
    h1 = h0 + 1
    while h0 >= 0 and nl[h1].startswith('//   '):
        h1 += 1
    bad = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ol, nl, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        for k in range(i1, i2):
            if ol[k] not in allowed_old and M.R18.tag(ov) not in ol[k] and ov not in ol[k]:
                bad.append('-' + ol[k][:60])
        for k in range(j1, j2):
            if not (nl[k] in allowed_new or h0 <= k < h1 or M.R18.tag(nv) in nl[k] or nv in nl[k]):
                bad.append('+' + nl[k][:60])
    say('T1', n, not bad and h0 >= 0, 'every changed line is the build\'s; the history note is lines %d to %d%s'
        % (h0 + 1, h1, ('; NOT: ' + ' | '.join(bad[:4])) if bad else ''))

# ------------------------------------------------------------------ G, the gate
w = os.path.join(tmp, 'w'); os.makedirs(w)
shutil.copytree('tools', os.path.join(w, 'tools'))
os.makedirs(os.path.join(w, 'Community_Library', 'github'))
kit = os.environ['HPKIT'].rstrip('/')
shutil.make_archive(os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit'), 'zip', os.path.dirname(kit), os.path.basename(kit))
os.makedirs(os.path.join(HERE, 'round19', 'gates'), exist_ok=True)
for n, ov, nv in PAIRS:
    r = subprocess.run([sys.executable, 'ppl_gate_v1e.py', newf[n], oldf[n]], cwd=os.path.join(w, 'tools'), capture_output=True, text=True)
    io.open(os.path.join(HERE, 'round19', 'gates', '%s_%s.txt' % (n, nv)), 'w', encoding='utf-8').write(
        r.stdout.replace(tmp, '.').replace(REPO, '.'))
    say('G', n, 'RESULT: PASS' in r.stdout, 'the gate against %s' % ov)

# ------------------------------------------------------------------ S, StatDist's formula page
CALLS = []
_orig = PR.giac_eval


def _timed(expr, timeout=60):
    t = time.time()
    try:
        return _orig(expr, timeout)
    finally:
        CALLS.append((expr, time.time() - t))


PR.giac_eval = _timed


def fm(prog, fam, ans):
    del CALLS[:]
    h = Harness(prog, idle_key=4, home_minus=True)
    h.choose('Advanced Continuous', fam, 2, 'Formula page (CAS)')
    h.answer(ans)
    h.event(Key(KEY['Enter']))
    err = ''
    try:
        h.execute('StatDist()')
    except Exception as e:
        err = type(e).__name__ + ': ' + str(e)[:80]
    ints = [(e, s) for e, s in CALLS if 'int(' in e]
    return list(h.globals_.get('stFmL') or []), ints, max([s for _, s in CALLS] or [0]), err


NOTE = 'The CAS is asked here only when'
SD = 'StatDist'
GUARD = [('Student t', {'df': 17.83, 'x_val': 1}), ('Student t', {'df': 206.3, 'x_val': 1}),
         ('Student t', {'df': 30.1, 'x_val': 1}), ('Student t', {'df': 0.83, 'x_val': 1}),
         ('Fisher F', {'df1': 7, 'df2': 17.83, 'x_val': 1}), ('Fisher F', {'df1': 7.5, 'df2': 17.5, 'x_val': 1}),
         ('Burr Type XII', {'stC': 2.37, 'stK': 3, 'stS': 1, 'x_val': 1}), ('Burr Type XII', {'stC': 2.5, 'stK': 3.5, 'stS': 1.5, 'x_val': 1})]
for fam, ans in GUARD:
    L, ints, mx, err = fm(newf[SD], fam, ans)
    txt = '\n'.join(L)
    ok = not err and not ints and NOTE in txt and 'no closed form shown' in txt
    say('S1', SD, ok, '%s %s: %d integral(s) asked, the note %s, "no closed form shown" %s%s'
        % (fam, json.dumps(ans).replace('"', ''), len(ints), 'shown' if NOTE in txt else 'MISSING',
           'shown' if 'no closed form shown' in txt else 'MISSING', (', ' + err) if err else ''))
L, ints, mx, err = fm(oldf[SD], 'Student t', {'df': 17.83, 'x_val': 1})
say('S1', SD, 'TimeoutExpired' in err, 'the old version at df 17.83, for comparison: %s'
    % (err or 'it ended (%d integrals, longest %.1f s)' % (len(ints), mx)))

ASKED = [('Student t', {'df': 24, 'x_val': 1}), ('Student t', {'df': 17.5, 'x_val': 1}), ('Student t', {'df': 1, 'x_val': 1}),
         ('Fisher F', {'df1': 7, 'df2': 18, 'x_val': 1}), ('Burr Type XII', {'stC': 2, 'stK': 3, 'stS': 1, 'x_val': 1}),
         ('Burr Type XII', {'stC': 2, 'stK': 3, 'stS': 1.83, 'x_val': 1})]
OTHER = [('Common Continuous', 'Normal', {'mu': 0.37, 'sg': 1.83, 'x_val': 1}),
         ('Advanced Continuous', 'Gamma', {'gaK': 2.37, 'gaT': 1.83, 'x_val': 1}),
         ('Advanced Continuous', 'Beta', {'btA': 2.37, 'btB': 3.37, 'x_val': 0.5})]
for fam, ans in ASKED:
    Ln, intn, mxn, errn = fm(newf[SD], fam, ans)
    Lo, into, mxo, erro = fm(oldf[SD], fam, ans)
    ok = not errn and Ln == Lo and len(intn) == len(into) and len(intn) > 0 and mxn < 5 and NOTE not in '\n'.join(Ln)
    say('S2', SD, ok, '%s %s: %d integral(s) asked, the longest call %.1f s; the page is the old version\'s line for line: %s'
        % (fam, json.dumps(ans).replace('"', ''), len(intn), mxn, 'yes' if Ln == Lo else 'NO'))


def fm_other(prog, menu, fam, ans):
    """Normal, Gamma, Beta: their forms' fields are read from the program, two decimals typed into each"""
    del CALLS[:]
    h = Harness(prog, idle_key=4, home_minus=True)
    h.choose(menu, fam, 2, 'Formula page (CAS)')
    h.answer(ans if ans else PR.ACCEPT)
    h.event(Key(KEY['Enter']))
    err = ''
    try:
        h.execute('StatDist()')
    except Exception as e:
        err = type(e).__name__ + ': ' + str(e)[:80]
    return list(h.globals_.get('stFmL') or []), [e for e, s in CALLS if 'int(' in e], err


for menu, fam, ans in OTHER:
    Ln, intn, errn = fm_other(newf[SD], menu, fam, ans)
    Lo, into, erro = fm_other(oldf[SD], menu, fam, ans)
    say('S3', SD, not errn and Ln == Lo and len(intn) == len(into) > 0,
        '%s (%s): %d integral(s) asked; the page is the old version\'s line for line: %s%s'
        % (fam, 'its form as it opens' if not ans else json.dumps(ans).replace('"', ''), len(intn), 'yes' if Ln == Lo else 'NO',
           (', ' + errn) if errn else ''))
PR.giac_eval = _orig

# ------------------------------------------------------------------ E, EpiStats' stratified rates grid
ES = 'EpiStats'
SENT = M.PT_MSG


def askall(prog, mod, vals):
    h = Harness(prog, idle_key=4, home_minus=True)
    h.execute('es_Init()')
    h.globals_.update({'esMod': mod, 'esStr': 1})
    h.globals_['esCel'] = [7.0, 700.0, 3.0, 900.0]
    h.answer(vals)
    r = h.execute('es_AskAll()')
    return r, list(h.globals_['esCel']), [m.text for m in h.msgboxes]


for C_, D_, take in ((100000, 1E-300, 0), (0.5, 100, 0), (100, 0.999, 0), (1, 100000, 1), (0, 0, 1), (1, 1, 1)):
    r, cel, mb = askall(newf[ES], 7, {'avA': 2, 'avB': 1, 'avC': C_, 'avD': D_})
    if take:
        ok = r == 1 and cel == [2, C_, 1, D_] and not mb
    else:
        ok = r == 0 and cel == [7, 700, 3, 900] and mb == [SENT]
    say('E1', ES, ok, 'person-times %s and %s: %s' % (C_, D_, ('taken, the grid holds %s' % cel) if r == 1 else
        ('refused (%s), the grid unchanged' % ('the round\'s sentence' if mb == [SENT] else mb))))
r, cel, mb = askall(newf[ES], 7, {'avA': 2, 'avB': 1, 'avC': 100000.5, 'avD': 5})
say('E1', ES, r == 0 and cel == [7, 700, 3, 900] and mb and 'at most 100,000' in mb[0], 'person-time 100,000.5: refused with the cap\'s sentence, as before')
r, cel, mb = askall(newf[ES], 7, CANCEL)
say('E1', ES, r == 0 and cel == [7, 700, 3, 900] and not mb, 'Cancel on the form: nothing changes')
r, cel, mb = askall(newf[ES], 5, {'avA': 2, 'avB': 1, 'avC': 3, 'avD': 0.5})
r0, cel0, mb0 = askall(oldf[ES], 5, {'avA': 2, 'avB': 1, 'avC': 3, 'avD': 0.5})
say('E1', ES, (r, cel, mb) == (r0, cel0, mb0) and SENT not in mb, 'the case-control grid with 0.5: as the old version (%s, %s)' % (cel, mb))


def grid(prog, edits):
    h = Harness(prog, idle_key=4, home_minus=True)
    h.execute('es_Init()')
    h.event(Key(KEY['Right']))
    for v in edits:
        h.event(Key(KEY['Enter'])); h.answer({'gdV': v})
    h.event(Key(KEY['Esc']))
    h.execute('es_StratGrids(3)')
    return list(h.globals_['esMS'])[17], [m.text for m in h.msgboxes]


v_new, mb_new = grid(newf[ES], [0.5])
v_old, mb_old = grid(oldf[ES], [0.5])
say('E2', ES, v_new == 0 and mb_new == [SENT], 'one cell, 0.5 typed as person-time: refused, the cell keeps 0 (the old version took it: %s)' % v_old)
v_new, mb_new = grid(newf[ES], [0.5, 1])
say('E2', ES, v_new == 1 and mb_new == [SENT], 'then 1: taken, the cell holds %s' % v_new)

hl = re.findall(r'"(Person-time (?:un)?exposed, 0 or 1 to 100,000)"', new[ES])
hl2 = re.findall(r'" person-time, 0 or 1 to 100,000"', new[ES])
longest = max(len(x) for x in hl) if hl else 0
say('E3', ES, len(hl) == 2 and len(hl2) == 1 and longest <= 47 and len('Exposed- person-time, 0 or 1 to 100,000') <= 47,
    'the help lines give the range: %d in the four-value form (the longest %d characters), 1 in the one-cell form (%d with its row)'
    % (len(hl), longest, len('Exposed- person-time, 0 or 1 to 100,000')))

sys.path.insert(0, os.path.join(HERE, 'round19'))
import floor_sweep_r19 as FS  # noqa: E402
import itertools  # noqa: E402
h = Harness(newf[ES], idle_key=4, home_minus=True)
h.execute('es_Init()'); h.globals_['esMod'] = 7
Cs, Ps = [0, 1, 100000], [0, 1, 100000]
n = agree = skipped = 0
worst = 0.0
for t in itertools.product(Cs, Ps, Cs, Ps, Cs, Ps, Cs, Ps):
    st, x = FS.mh(list(t))
    if st != 'ok':
        continue
    if x > 709.0:
        skipped += 1
        continue
    R = S = 0.0
    for i in range(2):
        a, t1, c, t0 = t[4 * i:4 * i + 4]
        if t1 + t0 > 0:
            R += a * t0 / (t1 + t0); S += c * t1 / (t1 + t0)
    E = R / S
    out = h.execute('es_MHCalc(3, {%s}, {0,0})' % ','.join(repr(float(v)) for v in t))
    n += 1
    import math
    lo, hi = math.exp(math.log(E) - (x - abs(math.log(E)))), math.exp(math.log(E) + (x - abs(math.log(E))))
    if all(abs(p - q) <= 1E-9 * max(abs(q), 1E-300) for p, q in zip(out[:3], (E, lo, hi))):
        agree += 1
    worst = max(worst, x)
say('E4', ES, n > 0 and agree == n, 'es_MHCalc on %s tables at the floor: E and the interval as worked in Python, %s of %s; %d tables with an end past the '
    'harness\'s EXP (e^709) left out, which the Prime holds (floor_sweep_r19.py: none past 1E499)' % ('{:,}'.format(n), '{:,}'.format(agree), '{:,}'.format(n), skipped))

# ------------------------------------------------------------------ R, round 18's two stopped runs, replayed
for n, seed, opts in (('StatDist', 18000984, ['--lists', '--seconds', '240']), ('EpiStats', 18000612, ['--lists', '--seconds', '30'])):
    call = 'EpiStats()' if n == 'EpiStats' else 'StatDist()'
    o = subprocess.run([sys.executable, 'tools/monkey_v1b.py', newf[n], call, '--replay', str(seed), '--events', '150'] + opts,
                       capture_output=True, text=True).stdout
    try:
        d = json.loads(o[o.index('{'):])
        v, det = d['verdict'], d['detail']
    except Exception:
        v, det = '?', o[-100:]
    say('R', n, v == 'OK', 'round 18\'s seed %d, replayed: %s %s' % (seed, v, det[:80]))

# ------------------------------------------------------------------ M, the start routines
for n, calls in (('StatDist', ['StatDist()']), ('EpiStats', ['EpiStats()', 'EpiStats2x2(10,20,30,40)'])):
    for call in calls:
        res = []
        for f in (newf[n], oldf[n]):
            try:
                hh = Harness(f, idle_key=4, on_unverified='warn'); hh.execute(call); res.append((len(hh.warnings), ''))
            except Exception as e:
                res.append((-1, type(e).__name__ + ': ' + str(e)[:60]))
        say('M', n, res[0][1] == '' and res[0][0] <= res[1][0], '%s: %d warnings (the old version %d)%s' % (call, res[0][0], res[1][0], res[0][1]))

# ------------------------------------------------------------------ N, the fleet's names and the screen text
newest = sorted(os.path.join('programs', f) for f in os.listdir('programs') if f.endswith('.txt'))
r = subprocess.run([sys.executable, 'tools/fleet_names_v2.py'] + newest, capture_output=True, text=True)
tail = (r.stdout.strip().split('\n') or [''])[-1]
say('N', 'fleet', r.returncode == 0 and ' 0 collisions' in tail, 'fleet_names_v2 over %d programs: %s' % (len(newest), tail[:90]))
r = subprocess.run([sys.executable, 'tools/screen_text_v1.py'] + newest, capture_output=True, text=True)
tail = (r.stdout.strip().split('\n') or [''])[-1]
say('N', 'fleet', r.returncode == 0 and 'against the rules: 0 ' in tail, 'screen_text_v1 over %d programs: %s' % (len(newest), tail[:90]))

fails = [l for ok, l in OUT if not ok]
print('%d checks, %d failed' % (len(OUT), len(fails)))
