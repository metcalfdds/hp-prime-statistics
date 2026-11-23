# -*- coding: utf-8 -*-
"""verify_round18_settings_v1.py -- Round 18 (22 Nov 2026): every program sets the book's four Home settings at its start.

One script for all 31 programs, because the round put the same line into each (verify/round18/README.md says why).
Each new version in programs/ is checked against the version before it, read from git (BASE).

  B   THE BUILD (verify/round18/make_round18.py) makes each filed program byte for byte.
  T1  ONLY THE ROUND'S LINES CHANGED.  Take the new version; take out the settings line at each start routine, the new
      history note, and (NormExplorer, StudRange) the new first line.  What is left differs from the old version only in
      the header's version line and in quoted strings that hold the version or its date.  Every other line is the same.
  T2  THE LINE IS WHERE A PROGRAM STARTS.  In every EXPORT routine (and CentralLimit's START and Plot hooks, by which an
      app is started) the first statement after the routine's LOCAL lines is the settings line, word for word.
  T3  THE FIRST LINE of every program is the pragma line.
  T4  THE LINE'S CODE IS ASCII, and it names the four variables the probes showed a program can assign.
  G   THE GATE (tools/ppl_gate_v1e.py) passes each new version against its old one.
  S   THE HARNESS SMOKE TEST: the start routine with the idle key Esc ends as the old version's did, with no more warnings.
  H   THE SETTINGS IN THE HARNESS: with HSeparator 4, HFormat 1, HAngle 1 and Entry 2 before the start routine is called
      (a comma, Fixed, Degrees, RPN), all four are 0 afterwards.  The harness is a PC model: it has no Home settings of
      its own and always writes a period (tools/prime_facts_v1.py, facts 5 and 6), so H shows that the line RUNS, and
      what the line DOES to a calculator is in verify/round18/vc_checks.txt.
  N   FLEET NAMES and SCREEN TEXT (tools/fleet_names_v2.py, tools/screen_text_v1.py) on the 31 programs.

Run from the repository's root, with hp-prime-kit at $HPKIT:   python3 verify/verify_round18_settings_v1.py
"""
import glob, io, os, re, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(HERE, 'round18')); sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
import make_round18 as R  # noqa: E402  (the build's own names: LINE, PRAGMA, OLD, heads, split_comment)

PAIRS = [(n, ov, R.nxt(ov)) for n, ov in R.OLD.items()] + [(R.GENERAL[0], R.GENERAL[1], R.nxt(R.GENERAL[1]))]
PAIRS.sort()
CALLS = {'PowerViz': ['POWERVIZ()'], 'TTestLab': ['TTESTLAB()'], 'TTestLabG': ['TTESTLABG()'], 'DataLoad': ['DATALOAD()'],
         'NormExplorer': ['NormExp()'], 'Norm3': ['Norm3(100,15,130)'], 'EpiStats': ['EpiStats()', 'EpiStats2x2(10,20,30,40)'],
         'CentralLimit': ['START()', 'Plot()']}
fails, lines = [], []


def say(code, name, ok, text=''):
    lines.append('%-2s %-12s %s  %s' % (code, name, 'OK  ' if ok else 'FAIL', text)); print(lines[-1], flush=True)
    if not ok:
        fails.append((code, name))


def old_text(n, ov):
    return subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (R.BASE, n, ov)], check=True, capture_output=True).stdout.decode('utf-8')


new, old = {}, {}
for n, ov, nv in PAIRS:
    new[n] = io.open(os.path.join('programs', '%s_%s.txt' % (n, nv)), encoding='utf-8').read(); old[n] = old_text(n, ov)

# ------------------------------------------------------------------ B, the build
bdir = tempfile.mkdtemp(prefix='r18build_')
rb = subprocess.run([sys.executable, os.path.join(HERE, 'round18', 'make_round18.py'), bdir], capture_output=True, text=True)
for n, ov, nv in PAIRS:
    f = os.path.join(bdir, '%s_%s.txt' % (n, nv))
    same = rb.returncode == 0 and os.path.exists(f) and io.open(f, encoding='utf-8', newline='').read() == io.open(os.path.join('programs', '%s_%s.txt' % (n, nv)), encoding='utf-8', newline='').read()
    say('B', n, same, 'verify/round18/make_round18.py makes the filed %s byte for byte' % nv)
shutil.rmtree(bdir, ignore_errors=True)

# ------------------------------------------------------------------ T1 to T4
for n, ov, nv in PAIRS:
    ot, nt = R.tag(ov), R.tag(nv)
    L = new[n].split('\n')
    took_pragma = 0
    if n in R.NO_PRAGMA:
        took_pragma = int(L[0] == R.PRAGMA); L = L[1:]
    set_lines = [i for i, l in enumerate(L) if l.strip() == R.LINE]
    L = [l for i, l in enumerate(L) if i not in set(set_lines)]
    h0 = [i for i, l in enumerate(L) if l.startswith('// %s (%s): Round 18:' % (nt, R.DATE))]
    took_note = 0
    if len(h0) == 1:
        k = h0[0] + 1
        while L[k].startswith('//   ') and not re.match(r'^//\s*' + re.escape(ot) + r'\s*\(', L[k]):
            k += 1
        took_note = k - h0[0]; L = L[:h0[0]] + L[k:]
    O = old[n].split('\n')
    diff = [(a, b) for a, b in zip(O, L) if a != b]
    bad = []
    for a, b in diff:
        if re.match(r'^//\s*[A-Za-z0-9 ]+ - ' + re.escape(nt) + r'\b', b):
            continue                                            # the header's version line
        ca, ka = R.split_comment(a); cb, kb = R.split_comment(b)
        back = re.sub(r'"[^"\n]*"', lambda m: re.sub(r'\b22 Nov 2026', 'DATE', m.group(0).replace(nt, ot).replace(nv, ov)), cb)
        was = re.sub(r'"[^"\n]*"', lambda m: re.sub(r'\b\d{1,2} Nov 2026', 'DATE', m.group(0)), ca)
        if ka != kb or back != was:
            bad.append(b.strip()[:60])
    want_sets = len(R.heads(n, new[n].split('\n'))) - (1 if n == 'CentralLimit' else 0)
    ok = (len(O) == len(L) and not bad and len(set_lines) == want_sets and took_note >= 7
          and took_pragma == (1 if n in R.NO_PRAGMA else 0))
    say('T1', n, ok, '%s -> %s: %d settings line(s), a history note of %d lines%s; %d other line(s) differ, all by the version%s'
        % (ov, nv, len(set_lines), took_note, ', the new first line' if took_pragma else '', len(diff), ('; NOT: ' + '; '.join(bad[:3])) if bad else ''))
    # T2
    NL = new[n].split('\n'); miss = []
    for h in R.heads(n, NL):
        rn = re.search(r'(\w+)\s*\(', NL[h].replace('EXPORT', '')).group(1)
        if n == 'CentralLimit' and rn == 'CentralLimit':
            continue
        k = h + 1
        while NL[k].strip() != 'BEGIN':
            k += 1
        k += 1
        while True:
            code = R.split_comment(NL[k])[0].strip()
            if code == '':
                k += 1
            elif re.match(r'LOCAL\b', code):
                while not R.split_comment(NL[k])[0].rstrip().endswith(';'):
                    k += 1
                k += 1
            else:
                break
        if NL[k].strip() != R.LINE:
            miss.append(rn)
    say('T2', n, not miss, 'the first statement of each start routine' + ((': NOT in ' + ', '.join(miss)) if miss else ''))
    say('T3', n, bool(re.match(r'#pragma mode\(\s*separator\(\.,;\) integer\(h32\)\s*\)\n', new[n])), 'the first line is the pragma line')
code = R.split_comment(R.LINE)[0]
say('T4', 'the line', all(ord(c) < 128 for c in R.LINE) and [v for v in ('HSeparator', 'HFormat', 'HAngle', 'Entry') if v + ' := 0;' in code]
    == ['HSeparator', 'HFormat', 'HAngle', 'Entry'], code.strip())

# ------------------------------------------------------------------ G, the gate
tmp = tempfile.mkdtemp(prefix='r18ver_'); w = os.path.join(tmp, 'w'); os.makedirs(w); olddir = os.path.join(tmp, 'old'); os.makedirs(olddir)
shutil.copytree('tools', os.path.join(w, 'tools'))
os.makedirs(os.path.join(w, 'Community_Library', 'github'))
kit = os.environ['HPKIT'].rstrip('/')
shutil.make_archive(os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit'), 'zip', os.path.dirname(kit), os.path.basename(kit))
os.makedirs(os.path.join(HERE, 'round18', 'gates'), exist_ok=True)
newf, oldf = {}, {}
for n, ov, nv in PAIRS:
    newf[n] = os.path.join(REPO, 'programs', '%s_%s.txt' % (n, nv)); oldf[n] = os.path.join(olddir, '%s_%s.txt' % (n, ov))
    io.open(oldf[n], 'w', encoding='utf-8', newline='').write(old[n])
    r = subprocess.run([sys.executable, 'ppl_gate_v1e.py', newf[n], oldf[n]], cwd=os.path.join(w, 'tools'), capture_output=True, text=True)
    io.open(os.path.join(HERE, 'round18', 'gates', '%s_%s.txt' % (n, nv)), 'w', encoding='utf-8').write(r.stdout.replace(tmp, '.').replace(REPO, '.'))
    say('G', n, 'RESULT: PASS' in r.stdout, 'the gate against %s' % ov)

# ------------------------------------------------------------------ S and H, in the harness
from ppl_run_v3e import Harness  # noqa: E402
SET = {'HSeparator': 4, 'HFormat': 1, 'HAngle': 1, 'Entry': 2}


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, alarm)


def run(f, call, preset):
    try:
        signal.alarm(180)
        h = Harness(f, idle_key=4, on_unverified='warn')
        if preset:
            h.globals_.update(SET)
        try:
            h.execute(call); err = ''
        except TO:
            err = 'timeout'
        except Exception as e:
            err = type(e).__name__ + ': ' + str(e)[:70]
        signal.alarm(0)
        return len(h.warnings), err, [h.globals_.get(k) for k in SET]
    except Exception as e:
        signal.alarm(0)
        return -1, 'load: ' + str(e)[:70], []


for n, ov, nv in PAIRS:
    for call in CALLS.get(n, [n + '()']):
        wn, en, after = run(newf[n], call, True); wo, eo, _ = run(oldf[n], call, False)
        say('S', n, en == eo and wn <= wo, '%s: warnings %d (old %d)%s' % (call, wn, wo, ('; ends ' + en) if en else ''))
        say('H', n, after == [0, 0, 0, 0], '%s: HSeparator, HFormat, HAngle, Entry from 4, 1, 1, 2 to %s' % (call, ', '.join('%g' % a if a is not None else '?' for a in after)))

# ------------------------------------------------------------------ N, names and screen text
r = subprocess.run([sys.executable, 'tools/fleet_names_v2.py'] + sorted(glob.glob('programs/*.txt')), capture_output=True, text=True)
tail = [l for l in r.stdout.strip().split('\n') if l.strip()][-1] if r.stdout.strip() else ''
say('N', 'fleet names', r.returncode == 0 and 'COLLISION' not in r.stdout, tail[:110])
r = subprocess.run([sys.executable, 'tools/screen_text_v1.py'] + sorted(glob.glob('programs/*.txt')), capture_output=True, text=True)
tail = [l for l in r.stdout.strip().split('\n') if l.strip()][-1] if r.stdout.strip() else ''
say('N', 'screen text', r.returncode == 0, tail[:110])

shutil.rmtree(tmp, ignore_errors=True)
lines.append('')
lines.append('%d checks, %d failed%s' % (len([l for l in lines if l[:1] in 'BTGSHN']), len(fails), (': ' + ', '.join('%s %s' % f for f in fails)) if fails else ''))
print(lines[-1])
io.open(os.path.join(HERE, 'verify_round18_settings_v1_output.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
sys.exit(1 if fails else 0)
