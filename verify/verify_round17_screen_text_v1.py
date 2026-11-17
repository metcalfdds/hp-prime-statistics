#!/usr/bin/env python3
"""verify_round17_screen_text_v1.py -- checks Round 17 (17 Nov 2026): the screen text of sixteen programs in the book's
house form for a statistic's letter, as far as a screen can follow it: a hyphen joins the letter to its noun (F-test,
t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is
a small letter.  Only text inside quotation marks changed, and the version of each program, so the checks are of the
text, of its place on the screen, and of everything else staying put.  Made from verify_round16_wording_v1.py.

Runs from the repository alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, the old
versions from git (the commit before Round 17, make_round17.BASE).  Needs hp-prime-kit (HPKIT) for the harness.

  T1  verify/round17/make_round17.py, run again from the old versions, makes each of the 16 new files byte for byte.
  T2  each new file differs from its old one only in comment lines and, in lines of code, only INSIDE quotation marks:
      with every quoted string taken out, the code of the two versions is the same line for line.
  T3  tools/screen_text_v1.py over all 31 programs: no place against the rules (the old versions had 116, counted with
      the walks; verify/round17/screen_text_before.txt).
  T4  the help pages, dumped by the harness (verify/round11/helpdump_r11.py) from the old and the new version: with the
      round's replacements made in the old pages' text, the two are the same page for page (a line that flows may
      break at another word, so a page is compared as running text); and every new help screen laid out at the glyph
      widths GlyphProbe_v1 measured on the Virtual Calculator has nothing cut and nothing overlapping
      (verify/round11/helpcheck_r11.py's rule, 318 px less x, or the width argument).
  T5  tools/ppl_gate_v1e.py on each new version against its old one: PASS.
  T6  EVERY CHANGED TEXT IS SEEN ON A SCREEN OF THE NEW VERSION, AND FITS.  The screens come from the help pages, from
      the monkey's sessions (T7) and, for a text those do not reach, from a directed call of its page.  A drawn text is
      measured at the Virtual Calculator's glyph widths against its own limit (the screen's edge, or its width
      argument); a menu item is counted against 30 characters and a menu title against 31; a form's help line against
      the longest of the form's other help lines.  And no line that flows breaks inside an expression in parentheses
      ("... df = (k -" at the end of one line and "1)." on the next).
  T7  the monkey, 30 seeds on the old and the new version of each program (10 for StudRange, whose integrals are slow):
      the same verdict, boxes, menus, forms and closing line, and every screen the same text for text once the
      round's replacements are made in the old one (a screen whose text flows is compared as running text, and may
      have nothing cut or overlapping that the old one did not have).
  T8  tools/fleet_names_v2.py over programs/: clean.
"""
import os, sys, io, json, glob, shutil, subprocess, tempfile, importlib.util, re, random, signal, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
R17 = os.path.join(HERE, 'round17'); R11 = os.path.join(HERE, 'round11')
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
spec = importlib.util.spec_from_file_location('m17', os.path.join(R17, 'make_round17.py'))
m17 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ['x', os.devnull]; spec.loader.exec_module(m17); sys.argv = argv
res = []
ONLY = [a for a in sys.argv[1:] if re.match(r'^T\d$', a)]          # e.g. "T6 T7": only those parts (T1 always runs)
PROGS = dict((n, (e[0], e[1])) for n, e in m17.EDITS.items()); PROGS['TTestLabG'] = ('beta1h', 'beta1i')
for a in sys.argv[1:]:
    if a.startswith('--only='):                                      # e.g. --only=FitCheck,TDist3D: those programs only
        PROGS = dict((n, v) for n, v in PROGS.items() if n in a[7:].split(','))
CALL = dict((n, n + '()') for n in PROGS); CALL.update({'PowerViz': 'POWERVIZ()', 'TTestLab': 'TTESTLAB()', 'TTestLabG': 'TTESTLABG()'})
S1, S2, S0 = u'₁', u'₂', u'₀'; X2 = u'χ²'; SG = u'σ'; NU = u'ν'; MIN = u'−'
# what the round changed, AS THE SCREEN SHOWS IT: (old text, new text), in the order they are to be made
MAP = {
 'AgreeLab': [('ICC intervals (F quantiles)', 'ICC intervals (F-quantiles)'), ('no F interval', 'no F-interval')],
 'AnovaLab': [('The q distribution is', 'The q-distribution is'),
              (' is true, F is near 1 and follows the', ' is true, F is near 1 and follows the F-curve'),
              ('F(k - 1, N - k) curve; p = P(F this big', 'with (k - 1) and (N - k) df; p = P(F this big'),
              ('The F test assumes', 'The F-test assumes'),
              ('usual method): k - 1 comparisons', 'usual method): (k - 1) comparisons'),
              (', df n - 1.', ', df = (n - 1).'),
              (', df n' + S1 + ' - 1 and n' + S2 + ' - 1.', ', df = (n' + S1 + ' - 1) and (n' + S2 + ' - 1).'),
              ('F curve and p', 'F-curve and p'), ('F curve of an effect', 'F-curve of an effect'),
              ('F curve (treatments)', 'F-curve (treatments)'), (': the F test and interval', ': the F-test and interval')],
 'CICatcher': [('(a t interval needs', '(a t-interval needs')],
 'EpiStats': [('M-H ' + X2 + ' (1 df): is the common OR 1?', 'M-H ' + X2 + ', 1 df: is the common OR 1?'),
              ('Breslow-Day (k-1 df):', 'Breslow-Day, (k-1) df:')],
 'ExhibitLab': [('SD (divisor n - 1), grams', 'SD, divisor (n - 1), grams'), ('t SE, t on n - 1', 't SE, t on (n - 1)')],
 'FitCheck': [('(k - 3) and ' + X2 + '(k - 1) (Chernoff', '(k-3) and ' + X2 + '(k-1) (Chernoff'), ('df = k - 1 - m', 'df = (k-1-m)'),
              ('p estimated (df = k - 2) or typed (df = k - 1).', 'p estimated, df = (k-2); typed, df = (k-1).'),
              ('df = k - 2', 'df = (k-2)'), ('df = k - 1.', 'df = (k-1).'), ('df = k - 3', 'df = (k-3)')],
 'PowerViz': [('F test of s' + S1 + u'²/s' + S2 + u'²', 'F-test of s' + S1 + u'²/s' + S2 + u'²'),
              ('puts in the z values (PPL)', 'puts in the z-values (PPL)'),
              ('z test: ' + SG + S1 + ', ' + SG + S2 + ' taken', 'z-test: ' + SG + S1 + ', ' + SG + S2 + ' taken')],
 'RankLab': [('the p tail(s)', 'the p-tail(s)')],
 'ResampLab': [('BCa and t intervals.', 'BCa and t-intervals.')],
 'ScatterLab': [('df = n - 2', 'df = (n - 2)')],
 'StudRange': [('P-value from q', 'p-value from q'), ('P-value: Studentized Range', 'p-value: Studentized Range')],
 'TDist3D': [('has one parameter, the degrees of freedom ' + NU + ' = n ' + MIN + ' 1.',
              'has one parameter: degrees of freedom, ' + NU + ' = (n ' + MIN + ' 1).'),
             ('Every t curve at once', 'Every t-curve at once')],
 'TTestLab': [('df = N' + S1 + ' + N' + S2 + ' - 2', 'df = (N' + S1 + ' + N' + S2 + ' - 2)'), ('t table, row df', 't-table, row df'),
              ('df = N - 1', 'df = (N - 1)')],
 'TTestLabG': [('df = N' + S1 + ' + N' + S2 + ' - 2', 'df = (N' + S1 + ' + N' + S2 + ' - 2)'),
               ('the smaller of N' + S1 + '-1, N' + S2 + '-1', 'the smaller of (N' + S1 + '-1), (N' + S2 + '-1)'),
               ('df = N - 1', 'df = (N - 1)')],
 'TestChooser': [("Cochran's Q test", "Cochran's Q-test"), (', k - 1 df', ', (k - 1) df'), ('ANOVA; k - 1 df.', 'ANOVA; (k - 1) df.')],
 'TrendTest': [('trend, k-2 df', 'trend, (k-2) df'), (' (k-1 df) asks only', ', (k-1) df, asks only'),
               (' (k-2 df) measures', ', (k-2) df, measures')],
}
# A CHANGED TEXT THAT NEITHER THE HELP PAGES NOR THE MONKEY'S SESSIONS SHOW is drawn by a lead of its own: the page's own
# routines, with the state its own menus would have set.  name -> [(what the lead shows, function of the harness)]


def lead_agree(Y):
    def f(h):                                   # the ICC page of "Use my data", with a table of ratings in D1, D2 ...
        cols = list(zip(*Y))
        h.globals_.update({'D%d' % (j + 1): [float(x) for x in cols[j]] for j in range(len(cols))})
        h.press('Enter'); h.choose('Use my data'); h.choose('Continuous: D1-D9'); h.choose('Quit')
        h.execute('AgreeLab()')
    return f


def lead_anova(h):
    h.execute('AnovaLab()')
    h.execute('av_PrgPage("Tukey q crit", "about 12 s on a G1")'); h.execute('BLIT_P(G0, G1)')
    h.globals_.update({'avVMode': 2, 'avVAlt': 1, 'avVS1': 2.0, 'avVN1': 10.0, 'avVS2': 1.5, 'avVN2': 12.0, 'avVCL': 0.95, 'avVHas': 1,
                       'avVLbl': 'Typed (illustrative numbers)'})
    h.execute('av_VCompute()'); h.execute('av_VDrawRes()'); h.execute('BLIT_P(G0, G1)')


def lead_fit(h):
    h.execute('FitCheck()')
    h.execute('fc_PreRossi()')                  # raw values, so the Bins key gives the note on raw values in bins
    h.tap(186, 228); h.tap(160, 120); h.tap(160, 120)        # the Test page, and its next pages
    h.execute('fc_MNBin()')


def lead_power(h):
    h.execute('POWERVIZ()')
    h.globals_['TT'] = 5                        # two means, unequal sigma and n: the test the Levene page belongs to
    h.press('Enter'); h.press('Enter'); h.press('Enter')
    h.execute('pv_LvPage()')


def lead_resamp(h):
    h.press('Enter'); h.choose(5); h.choose('BJS: months served'); h.choose(3); h.choose(9)
    h.execute('ResampLab()')


def lead_ttest(prefix, call):
    def f(h):
        h.execute(call)
        for ty in (1, 2):                       # pooled, then separate variances
            h.globals_[prefix + 'TY'] = ty
            h.execute(prefix + '_Step2()')
    return f


def lead_chooser(h):
    h.execute('TestChooser()')
    for a in ('tcDetails(9, 2, 5)', 'tcDetails(12, 3, 3)', 'tcDetails(14, 3, 5)', 'tcDetails(17, 4, 3)'):
        h.execute(a)


DIRECT = {
 'AgreeLab': [('the ICC page, raters in perfect agreement', lead_agree([[3, 3, 3], [5, 5, 5], [9, 9, 9]])),
              ('the ICC page, targets all alike', lead_agree([[1, 2], [2, 1], [1, 2], [2, 1]]))],
 'AnovaLab': [("the waiting page of Tukey's studentized range, and the two-variance result", lead_anova)],
 'FitCheck': [('a normal fit to raw values in bins (the Rossi preset), the Test page', lead_fit)],
 'PowerViz': [("Would Levene's test notice?, both pages", lead_power)],
 'ResampLab': [('the preset BJS: months served', lead_resamp)],
 'TTestLab': [('step 2 with pooled and with separate variances', lead_ttest('tt', 'TTESTLAB()'))],
 'TTestLabG': [('step 2 with pooled and with separate variances', lead_ttest('tz', 'TTESTLABG()'))],
 'TestChooser': [('the details of tests 9, 12, 14 and 17', lead_chooser)],
}


def rec(tag, ok, msg):
    res.append(ok)
    print('%-4s %s  %s' % (tag, 'PASS' if ok else 'FAIL', msg), flush=True)


def want(t):
    return not ONLY or t in ONLY


def remap(name, t):
    for a, b in MAP[name]:
        t = t.replace(a, b)
    return t


def vmap(name):
    ov, nv = PROGS[name]
    return [(m17.tag(ov), m17.tag(nv)), (ov, nv)]


tmp = tempfile.mkdtemp(prefix='r17v_')
olddir = os.path.join(tmp, 'old'); os.makedirs(olddir)
OLD, NEW = {}, {}
for name, (ov, nv) in PROGS.items():
    OLD[name] = os.path.join(olddir, '%s_%s.txt' % (name, ov)); NEW[name] = os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv))
    io.open(OLD[name], 'w', encoding='utf-8', newline='').write(m17.old_text(name, ov))
# ---------------------------------------------------------------------------------------------------------------- T1
out = os.path.join(tmp, 'built'); os.makedirs(out)
r = subprocess.run([sys.executable, os.path.join(R17, 'make_round17.py'), out], capture_output=True, text=True)
for name, (ov, nv) in PROGS.items():
    f = '%s_%s.txt' % (name, nv)
    a = open(os.path.join(out, f), 'rb').read() if os.path.exists(os.path.join(out, f)) else b''
    rec('T1', a == open(NEW[name], 'rb').read() and len(a) > 0, '%s: the build makes programs/%s byte for byte' % (name, f))
# ---------------------------------------------------------------------------------------------------------------- T2
STRING = re.compile(r'"(?:[^"\\]|\\.)*"')
if want('T2'):
    for name, (ov, nv) in PROGS.items():
        old = io.open(OLD[name], encoding='utf-8').read().split('\n'); new = io.open(NEW[name], encoding='utf-8').read().split('\n')
        co = [m17.split_comment(l)[0].rstrip() for l in old if not l.lstrip().startswith('//')]
        cn = [m17.split_comment(l)[0].rstrip() for l in new if not l.lstrip().startswith('//')]
        differ = [(a, b) for a, b in zip(co, cn) if a != b]
        bare = [(a, b) for a, b in differ if STRING.sub('""', a) != STRING.sub('""', b)]
        ko = [m17.split_comment(l)[1] for l in old if not l.lstrip().startswith('//')]
        kn = [m17.split_comment(l)[1] for l in new if not l.lstrip().startswith('//')]
        rec('T2', len(co) == len(cn) and not bare and ko == kn and len(differ) > 0,
            '%s: %d lines of code; %d differ, each only inside quotation marks; the comments at the ends of lines are the same'
            % (name, len(cn), len(differ)) + ('' if not bare else ': ' + ' | '.join(b.strip()[:60] for a, b in bare[:3])))
# ---------------------------------------------------------------------------------------------------------------- T3
if want('T3'):
    allp = sorted(glob.glob(os.path.join('programs', '*.txt')))
    r = subprocess.run([sys.executable, 'tools/screen_text_v1.py'] + allp, capture_output=True, text=True)
    last = (r.stdout.strip().split('\n') or [''])[-1]
    rec('T3', r.returncode == 0 and len(allp) == 31, 'tools/screen_text_v1.py: ' + last[:150])
    for name, (ov, nv) in PROGS.items():
        t = io.open(NEW[name], encoding='utf-8').read(); o = io.open(OLD[name], encoding='utf-8').read()
        pairs = m17.EDITS[name][2] if name in m17.EDITS else []
        gone = [a for a, b, n in pairs if any(a in m17.split_comment(l)[0] for l in t.split('\n'))]
        here = [b for a, b, n in pairs if sum(m17.split_comment(l)[0].count(b) for l in t.split('\n')) < n]
        rec('T3', not gone and not here, '%s: %d old wordings gone from the code, each new one there the number of times named'
            % (name, len(pairs)) if name in m17.EDITS else '%s: built from TTestLab beta 1l (T1)' % name)
# ---------------------------------------------------------------------------------------------------------------- the harness
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.path.insert(0, os.path.join(R11, 'tools11')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness, PPLError, HarnessStall, HarnessScriptError  # noqa: E402
HERR = (PPLError, HarnessStall, HarnessScriptError)          # what a program's run may end with; anything else stops this script
import hp11  # noqa: E402     (the glyph widths GlyphProbe_v1 measured on the Virtual Calculator)
exec(open(os.path.join(R11, 'helpdump_r11.py')).read().split('out = {}')[0].split('from ppl_run_v3e import Harness, KEY')[1])  # ROUT: each program's help routines
HGT = {1: 10, 2: 12, 3: 14, 0: 12}
BROKEN = re.compile(u'\\([A-Za-z\u03bd][\u2080-\u2089]?(?:\\s?[-\u2212+]\\s?[A-Za-z0-9\u2080-\u2089]*)*\\s*$')      # "(k -", "(N1 + N2", "(n"


def gw(t, f):
    f = int(f or 2)
    return sum(hp11.GW[ord(ch)][f - 1] if ord(ch) in hp11.GW and 1 <= f <= 3 else 8 for ch in t)


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


def help_run(path, name):
    """the help pages of one program: (pages as lists of lines, screens as lists of Text, problems of the run)"""
    pages, screens, probs = [], [], []
    for rt in ROUT[name]:
        signal.signal(signal.SIGALRM, alarm); signal.alarm(120)
        try:
            h = Harness(path, idle_key=4, on_unverified='warn')
            try:
                h.execute(CALL[name])
            except HERR:
                pass
            h.screens[:] = []
            for i in range(60):
                h.press(30)
            try:
                if name in ('AgreeLab', 'AnovaLab'):
                    for k in range(1, 12):
                        try:
                            h.execute('%s(%d)' % (rt, k))
                        except HERR:
                            break
                else:
                    h.call(rt)
            except HERR as e:
                probs.append('call %s: %s' % (rt, str(e)[:80]))
        except TO:
            probs.append('%s timed out' % rt)
            continue
        finally:
            signal.alarm(0)
        seen = set()
        for s in h.screens:
            ls = [l for l in s.lines() if l.strip()]
            key = '\n'.join(ls)
            if ls and key not in seen:
                seen.add(key); pages.append(ls); screens.append([t for t in s.texts if t.text and t.text.strip()])
    return pages, screens, probs


def first_diff(a, b):
    """where two lists of page texts first part: (page, the old text there, the new text there)"""
    for k, (x, y) in enumerate(zip(a, b)):
        if x != y:
            i = next((j for j, (c, d) in enumerate(zip(x, y)) if c != d), min(len(x), len(y)))
            return k + 1, x[max(0, i - 40):i + 40], y[max(0, i - 40):i + 40]
    return None


def runtext(lines):
    return re.sub(r'\s+', ' ', ' '.join(lines)).strip()


def layout(T):
    """helpcheck_r11's rule on one screen's texts: what is cut, and what overlaps"""
    out = []
    for t in T:
        lim = 318 - t.x
        if t.width:
            lim = min(lim, t.width)
        if gw(t.text, t.font) > lim:
            out.append('CUT %d > %d px: %r' % (gw(t.text, t.font), lim, t.text[:60]))
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            a, b = T[i], T[j]
            ay0, ay1 = a.y, a.y + HGT.get(int(a.font or 0), 12); by0, by1 = b.y, b.y + HGT.get(int(b.font or 0), 12)
            if ay0 < by1 - 1 and by0 < ay1 - 1:
                ax0, ax1 = a.x, a.x + min(gw(a.text, a.font), a.width or 999); bx0, bx1 = b.x, b.x + min(gw(b.text, b.font), b.width or 999)
                if ax0 < bx1 and bx0 < ax1:
                    out.append('OVERLAP %r (y %d) / %r (y %d)' % (a.text[:30], a.y, b.text[:30], b.y))
    return out


# everything the new versions showed, for T6: name -> list of (kind, text, x, font, width argument, where); RUNNING has
# each screen as running text (a sentence that flows may lie on two lines); OLDTEXT every text the old versions drew
SHOWN = dict((n, []) for n in PROGS); RUNNING = dict((n, []) for n in PROGS); OLDTEXT = dict((n, set()) for n in PROGS)


def note_screen(name, T, where):
    for t in T:
        SHOWN[name].append(('text', t.text, t.x, t.font, t.width, where))
    RUNNING[name].append((where, runtext([t.text for t in T])))


def note_old(name, T):
    for t in T:
        OLDTEXT[name].add(remap(name, t.text))


def note_dialogs(name, h, where):
    for m in h.msgboxes:
        SHOWN[name].append(('msgbox', m.text, None, None, None, where))
    for d in h.dialogs:
        if hasattr(d, 'items'):
            SHOWN[name].append(('menu title', str(d.title), None, None, None, where))
            for it in d.items:
                SHOWN[name].append(('menu item', str(it), None, None, None, where))
        else:
            SHOWN[name].append(('form title', str(d.title), None, None, None, where))
            for it in (d.labels or []):
                SHOWN[name].append(('form label', str(it), None, None, None, where))
            hl = [str(x) for x in (d.helps or [])]
            for it in hl:
                SHOWN[name].append(('form help', it, max([len(x) for x in hl if x != it] or [0]), None, None, where))


# ---------------------------------------------------------------------------------------------------------------- T4
if want('T4') or want('T6'):
    for name in PROGS:
        po, so, eo = help_run(OLD[name], name); pn, sn, en = help_run(NEW[name], name)
        for T in sn:
            note_screen(name, T, 'help')
        for T in so:
            note_old(name, T)
        if not want('T4'):
            continue
        a = [remap(name, runtext(p)) for p in po]; b = [runtext(p) for p in pn]
        for x, y in vmap(name):
            a = [t.replace(x, y) for t in a]
        ch = [k + 1 for k, (x, y) in enumerate(zip(po, pn)) if x != y]
        lay = [(k + 1, p) for k, T in enumerate(sn) for p in layout(T)]
        layo = [(k + 1, p) for k, T in enumerate(so) for p in layout(T)]
        new_lay = [p for p in lay if p not in layo]
        rec('T4', a == b and len(pn) > 0 and not en and len(pn) == len(po) and not new_lay,
            '%s: %d help screens; %s; with the round\'s replacements the old pages read as the new ones; nothing cut, nothing overlapping%s'
            % (name, len(pn), ('changed: ' + ', '.join(map(str, ch))) if ch else 'none changed',
               ('' if not layo else ' that the old version did not have (%d reports in both)' % len(layo))
               + ('' if not new_lay else ' -- NEW: ' + str(new_lay[:3])[:300]) + ('' if not en else ' -- run: ' + str(en)[:200])
               + ('' if a == b else ' -- TEXT DIFFERS on pages ' + str([k + 1 for k, (x, y) in enumerate(zip(a, b)) if x != y][:8]) + ': ' + str(first_diff(a, b)))))
# ---------------------------------------------------------------------------------------------------------------- T5
if want('T5'):
    w = os.path.join(tmp, 'w'); os.makedirs(w)
    shutil.copytree('tools', os.path.join(w, 'tools'))
    os.makedirs(os.path.join(w, 'Community_Library', 'github'))
    base = os.path.dirname(os.environ['HPKIT'].rstrip('/'))
    shutil.make_archive(os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit'), 'zip', base,
                        os.path.basename(os.environ['HPKIT'].rstrip('/')))
    for name in PROGS:
        r = subprocess.run([sys.executable, 'ppl_gate_v1e.py', NEW[name], OLD[name]], cwd=os.path.join(w, 'tools'), capture_output=True, text=True)
        rec('T5', 'RESULT: PASS' in r.stdout, '%s: the gate' % name)
# ---------------------------------------------------------------------------------------------------------------- T7
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
sys.argv = ['monkey_v1b.py']
import monkey_v1b as MK  # noqa: E402
sys.argv = argv


def one(path, call, seed, name, new):
    rng = random.Random(seed)
    app, kind = MK.random_lists(rng)
    hh = MK.Monkey(path, rng, app, 150)
    for q in range(10):
        hh.globals_.setdefault('M%d' % q, MK.R.interp.Matrix([[0.0]]))
    m1, mk = MK.random_matrix(seed)
    if m1 is not None:
        hh.globals_['M1'] = m1
    verdict = 'OK'
    signal.signal(signal.SIGALRM, MK._alarm); signal.alarm(60)
    try:
        hh.execute(call)
    except MK.TimeUp:
        verdict = 'FREEZE'
    except Exception as e:
        verdict = 'END ' + type(e).__name__
    finally:
        signal.alarm(0)

    def f(t):
        t = str(t)
        if not new:
            t = remap(name, t)
            for a, b in vmap(name):
                t = t.replace(a, b)
            if m17.tag(PROGS[name][1]) in t:                 # a version on the screen with its date: the new date
                t = re.sub(r'\b\d{1,2} Nov 2026', m17.DATE, t)
        return t
    scr = [tuple(f(t.text) for t in s.texts) for s in hh.screens]
    dia = [(f(d.title), tuple(f(x) for x in d.items)) if hasattr(d, 'items') else
           (f(d.title), tuple(f(x) for x in (d.labels or [])), tuple(f(x) for x in (d.helps or []))) for d in hh.dialogs]
    if new:
        for k, s in enumerate(hh.screens):
            note_screen(name, [t for t in s.texts if t.text and t.text.strip()], 'monkey seed %d' % seed)
        note_dialogs(name, hh, 'monkey seed %d' % seed)
    else:
        for s in hh.screens:
            note_old(name, [t for t in s.texts if t.text and t.text.strip()])
    raw = [[t for t in s.texts if t.text and t.text.strip()] for s in hh.screens]
    return verdict, scr, [f(m.text) for m in hh.msgboxes], dia, f(hh.result), raw


if want('T7') or want('T6'):
    for name in PROGS:
        seeds = range(1700, 1710) if name == 'StudRange' else range(1700, 1730)
        diffs = []; nscr = 0; verd = {}; nd = 0; flowed = 0
        for sd in seeds:
            a = one(OLD[name], CALL[name], sd, name, False); b = one(NEW[name], CALL[name], sd, name, True)
            nscr += len(b[1]); nd += len(b[3]) + len(b[2]); verd[b[0]] = verd.get(b[0], 0) + 1
            if a[:5] == b[:5]:
                continue
            k = None
            if a[0] == b[0] and a[2:5] == b[2:5] and len(a[1]) == len(b[1]):
                # a text that flows may break at another word: such a screen is compared as running text (the old
                # one's with the round's replacements made), and it may have nothing cut or overlapping that the
                # old screen did not have
                for j, (x, y) in enumerate(zip(a[1], b[1])):
                    if x == y:
                        continue
                    xo = runtext([t.text for t in a[5][j]])
                    for u, v in vmap(name):
                        xo = xo.replace(u, v)
                    lo = layout(a[5][j])
                    if remap(name, xo) == runtext([t.text for t in b[5][j]]) and not [q for q in layout(b[5][j]) if q not in lo]:
                        flowed += 1
                    else:
                        k = j
                        break
                if k is None:
                    continue
            else:
                k = next((i for i, (x, y) in enumerate(zip(a[1], b[1])) if x != y), None)
            diffs.append((sd, a[0], b[0], a[2] == b[2], a[3] == b[3], a[4] == b[4], len(a[1]), len(b[1]), k,
                          [(x, y) for x, y in zip(a[1][k], b[1][k]) if x != y][:2] if k is not None and k < min(len(a[1]), len(b[1])) else None))
        if want('T7'):
            rec('T7', not diffs and nscr > 60, '%s: %d seeds, %d screens and %d boxes, menus and forms the same text for text%s (%s)%s'
                % (name, len(seeds), nscr, nd, '' if not flowed else ' (%d of the screens as running text: a line that flows broke at another word)' % flowed,
                   ', '.join('%s %d' % kv for kv in sorted(verd.items())), '' if not diffs else ': ' + str(diffs[:2])[:600]))
# ---------------------------------------------------------------------------------------------------------------- T6
if want('T6'):
    FIRST = {'the help pages': 0, "the monkey's sessions": 0, 'a directed lead': 0}
    for name in PROGS:
        for what, lead in DIRECT.get(name, []):
            for path, isnew in ((NEW[name], True), (OLD[name], False)):
                signal.signal(signal.SIGALRM, alarm); signal.alarm(300)
                try:
                    h = Harness(path, idle_key=4, on_unverified='warn')
                    try:
                        lead(h)
                    except HERR as e:
                        if isnew:
                            SHOWN[name].append(('error', '%s: %s %s' % (what, type(e).__name__, str(e)[:120]), None, None, None, 'directed'))
                    for s in h.screens:
                        T = [t for t in s.texts if t.text and t.text.strip()]
                        if isnew:
                            note_screen(name, T, 'directed: ' + what)
                        else:
                            note_old(name, T)
                    if isnew:
                        note_dialogs(name, h, 'directed: ' + what)
                except TO:
                    if isnew:
                        SHOWN[name].append(('error', 'timed out: ' + what, None, None, None, 'directed'))
                finally:
                    signal.alarm(0)
        errs = [s[1] for s in SHOWN[name] if s[0] == 'error']
        for old_t, new_t in MAP[name]:
            hits = [s for s in SHOWN[name] if new_t in s[1] and s[0] != 'error']
            flows = [w for w, r in RUNNING[name] if new_t in r] if not hits else []
            flow = len(flows)
            stale = [s for s in SHOWN[name] if old_t in s[1] and new_t not in s[1] and s[0] != 'error']
            bad, tight, kinds = [], None, {}
            for kind, text, x, font, width, where in hits:
                kinds[kind] = kinds.get(kind, 0) + 1
                if kind == 'text':
                    lim = 318 - x
                    if width:
                        lim = min(lim, width)
                    ww = gw(text, font)
                    if ww > lim:
                        bad.append('%d > %d px %r' % (ww, lim, text[:50]))
                    if tight is None or lim - ww < tight[0]:
                        tight = (lim - ww, ww, lim)
                elif kind == 'menu item' and len(text) > 30:
                    bad.append('menu item of %d characters %r' % (len(text), text))
                elif kind == 'menu title' and len(text) > 31:
                    bad.append('menu title of %d characters %r' % (len(text), text))
                elif kind == 'form help' and len(text) > x:
                    bad.append('help line of %d characters, the longest of the form\'s others is %d: %r' % (len(text), x, text))
            src = set(w.split(':')[0].split(' seed')[0] for w in [h_[5] for h_ in hits] + flows)
            if src:
                FIRST['the help pages' if 'help' in src else "the monkey's sessions" if 'monkey' in src else 'a directed lead'] += 1
            seen = ', '.join('%s %d' % kv for kv in sorted(kinds.items())) if hits else ('over two lines of a text that flows, %d' % flow if flow else 'NOT SEEN')
            rec('T6', (len(hits) > 0 or flow > 0) and not bad and not stale and not errs,
                '%s: "%s" shown %d times (%s)%s%s%s' % (name, new_t[:44], len(hits) or flow, seen,
                                                     '' if tight is None else '; the tightest: %d px of %d, %d to spare' % (tight[1], tight[2], tight[0]),
                                                     '' if not bad else ' -- DOES NOT FIT: ' + '; '.join(bad[:3]),
                                                     ('' if not stale else ' -- THE OLD WORDING IS STILL SHOWN: %r' % stale[0][1][:60])
                                                     + ('' if not errs else ' -- ' + errs[0])))
        # every screen the directed leads, the help pages and the monkey showed: nothing cut and nothing overlapping at
        # the calculator's glyph widths is checked for the changed texts above; here, a line that flows must not
        # break inside an expression ("... df = (k -" at the end of a line, "1)." on the next), unless the old
        # version's own text already broke there (a formula in a help page that this round did not touch)
        broken = sorted(set(s[1] for s in SHOWN[name] if s[0] == 'text' and BROKEN.search(s[1])))
        was = [b for b in broken if b in OLDTEXT[name]]; now = [b for b in broken if b not in OLDTEXT[name]]
        rec('T6', not now, '%s: of %d texts shown, none ends inside an expression in parentheses that the old version did not end there too%s%s'
            % (name, len(SHOWN[name]), '' if not was else ' (%d old ones: %s)' % (len(was), ' | '.join(b[-28:] for b in was[:3])),
               '' if not now else ' -- NEW: ' + ' | '.join(b[-40:] for b in now[:4])))
    print('T6   of the %d changed wordings, %s' % (sum(len(v) for k, v in MAP.items() if k in PROGS),
                                               '; '.join('%d were shown by %s' % (v, k) if i == 0 else '%d more only by %s' % (v, k)
                                                         for i, (k, v) in enumerate(FIRST.items()))), flush=True)
# ---------------------------------------------------------------------------------------------------------------- T8
if want('T8'):
    r = subprocess.run([sys.executable, 'tools/fleet_names_v2.py'] + sorted(glob.glob('programs/*.txt')), capture_output=True, text=True)
    fl = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    badn = [l for l in fl if any(k in l for k in ('COLLISION', 'UNTAGGED', 'MIXEDTAG', 'BUILTIN'))]
    rec('T8', not badn and len(fl) > 0, 'tools/fleet_names_v2.py over %d programs: %s' % (len(glob.glob('programs/*.txt')), 'clean' if not badn else '%d findings' % len(badn)))
shutil.rmtree(tmp, ignore_errors=True)
print('\n%d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
