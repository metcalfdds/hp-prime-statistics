#!/usr/bin/env python3
"""verify_TestChooser_beta2a.py -- PC checks for TestChooser beta 2a (19 Oct 2026): T1 (three details pages
named the retired ConTable2 and FEP), T2 (a 31-character menu line), T3 (the two "(none)" survival cells hatched
alike) and three wordings (the log-rank test, Cochran's rule, cochran.qtest's package), from the fleet review of
19 Oct 2026 (findings_B).  Built from verify_TestChooser.py: every check is kept and runs on beta 2a (harness
ppl_run_v1, as before).  Two of its expected values WERE the bug T3 and change with it: "tcNotP equals the line-3
rule" becomes "tcNotP = the tests whose details say Not on the Prime" (test 18 says it on line 4), and "twelve
hatched tests" becomes thirteen.  The menu item is chosen by number, so T2 changes no script.  t_beta2a is new
(harness ppl_run_v3e): the review's check_TestChooser.py on beta 2 and beta 2a (its three failing checks fail on
beta 2 and pass on beta 2a), the pages as drawn, the menu, the hatching, the routine diff, the static rules.

Run:  python3 verify_TestChooser_beta2a.py      (exits 1 on any failure)

(verify_TestChooser.py's docstring follows.)

verify_TestChooser.py -- PC checks for TestChooser beta 2 (16 Oct 2026).

TestChooser computes no statistics, so there is nothing to compare with SciPy.  What is
checked instead, by running the program's own source in ppl_run_v1 (hp-prime-kit's
interpreter with scripted keys and taps):

  1. the quiz bank: every case's (scale, design) lands, through the program's own
     tcIdFor and tcFull, on the test it is meant to teach; the also-accepted cells too;
     every case uses designs 2-6 (the quiz table's five columns); lines <= 46 chars;
  2. the hatching list tcNotP is exactly the tests whose detail line 3 starts
     "Not on the Prime" (12 of them);
  3. the "Check:" lines and every new string fit their boxes (character counts);
  4. the flowchart, driven by taps and by keys: the right screens and text appear;
  5. the table: first tap selects, second tap opens; row and column lighting; the
     one-sample page; + and -; the soft keys;
  6. the quiz: a right answer (green, details), a wrong answer (red, green outline,
     reason, tap the green cell for its details), a whole round, the score page;
  7. text that would run into the soft-key strip (y >= 218) or overlap on any page.

Run:  python3 verify_TestChooser.py      (exits 1 on any failure)
"""
import sys
sys.path.insert(0, '/home/claude/work/harness')
import ppl_run_v1                     # noqa: E402
from ppl_run_v1 import KEY            # noqa: E402


class Harness(ppl_run_v1.Harness):
    """ppl_run_v1 covers RANDOM only written as a call; the fleet writes it bare
    (CentralLimit, GaltonBoard, CICatcher), as tcQNew does.  Read a bare RANDOM as
    RANDOM() -- the harness's seeded generator."""
    def evaluate(self, e, frame):
        if e[0] == 'var' and e[1] == 'RANDOM' and 'RANDOM' not in frame:
            return self._random([])
        return ppl_run_v1.Harness.evaluate(self, e, frame)

PROG = '/home/claude/work/fix19/TestChooser_beta2a.txt'   # beta 2a
FAILS = []
NOTES = []


def check(cond, msg):
    (NOTES if cond else FAILS).append(('ok   ' if cond else 'FAIL ') + msg)


def H():
    h = Harness(PROG, strict=True, seed=7)
    h.call('tcInit')
    h.reset_records()
    return h


# expected test for each case (the teaching intent), in bank order
EXPECT = ["One-way ANOVA", "Chi-square 2x2, or Fisher's exact", "Paired t test",
          "Mann-Whitney U (Wilcoxon rank-sum)", "Log-rank test (two groups)",
          "Pearson r and linear regression", "Unpaired (two-sample) t test", "McNemar's test",
          "Chi-square for an r x c table", "Kruskal-Wallis test", "Wilcoxon signed-rank test",
          "Repeated-measures ANOVA", "Friedman test", "Cochran's Q test",
          "Spearman rank correlation", "Log-rank test (several groups)",
          "Cox proportional-hazards regression", "Relative risk, odds ratio, chi-square",
          "Unpaired (two-sample) t test", "Paired t test"]
ALT_EXPECT = {1: "Kruskal-Wallis test", 2: "Relative risk, odds ratio, chi-square",
              18: "Chi-square 2x2, or Fisher's exact"}


def t_bank():
    h = H()
    n = int(h.globals_['tcQN'])
    check(n == 20 == len(EXPECT), 'bank has 20 cases (tcQN = %d)' % n)
    cells = set()
    for i in range(1, n + 1):
        q = h.call('tcQ', i)
        s, d, alt = int(q[0]), int(q[1]), int(q[2])
        name = h.call('tcFull', h.call('tcIdFor', s, d))
        check(name == EXPECT[i - 1], 'case %2d -> (%d,%d) %s' % (i, s, d, name))
        check(2 <= d <= 6, 'case %2d design %d is in the quiz table' % (i, d))
        for line in q[3:7]:
            check(len(line) <= 46, 'case %2d line <= 46 chars: %r' % (i, line))
        if alt:
            an = h.call('tcFull', h.call('tcIdFor', alt // 10, alt % 10))
            check(an == ALT_EXPECT.get(i), 'case %2d also accepts %s' % (i, an))
            check(2 <= alt % 10 <= 6, 'case %2d alt cell in the quiz table' % i)
        else:
            check(i not in ALT_EXPECT, 'case %2d has no alt' % i)
        cells.add((s, d))
    NOTES.append('     the bank covers %d of the 18 testable cells' % len(cells))


def t_hatch_and_strings():
    h = H()
    notp = [int(v) for v in h.globals_['tcNotP']]
    # beta 2a (T3): the rule is "the details say Not on the Prime" -- test 18 says it on line 4 -- and the
    # count is thirteen; beta 2's "line 3" and "twelve" were the bug
    rule = [1 if any(l.startswith('Not on the Prime') for l in h.call('tcDetail', i)) else 0
            for i in range(1, 25)]
    check(notp == rule, 'tcNotP equals the "Not on the Prime" rule (any detail line; beta 2a, T3)')
    check(sum(notp) == 13, 'thirteen hatched tests (%d; beta 2 had twelve, T3)' % sum(notp))
    for i in range(1, 25):
        c = h.call('tcCheck', i)
        check(len(c) <= 42, 'check line %d <= 42 chars (%d)' % (i, len(c)))
    for i in range(1, 5):
        tx = h.call('tcScaleTx', i)
        check(len(tx[0]) <= 16 and all(len(x) <= 20 for x in tx[1:]), 'scale node %d fits' % i)
        check(len(h.call('tcRowSum', i)) <= 46, 'row summary %d <= 46' % i)
    for d in range(1, 7):
        check(all(len(x) <= 20 for x in h.call('tcDesTx', d)), 'design node %d fits' % d)
        check(len(h.call('tcColSum', d)) <= 46, 'column summary %d <= 46' % d)


def page_checks(h, label):
    """No text in the soft-key strip; no two texts on one page overlapping (6.5 px/char
    for font 1, 8 for font 2, 11 / 14 px rows); widths inside the screen."""
    bad = []
    for s in h.screens:
        if s.reason != 'wait':
            continue        # animation frames: a node in flight overlaps others by design
        ts = [t for t in s.texts if t.text]
        for t in ts:
            if t.y is not None and t.y + (14 if t.font == 2 else 11) > 218:
                bad.append('strip: %r y=%s' % (t.text, t.y))
            w = len(t.text) * (8 if t.font == 2 else 6.5)
            lim = t.width if t.width else 320 - t.x
            if w > lim + 2 and t.func != 'tcCellDraw':   # cell labels: beta 1b's, unchanged
                bad.append('wide (%d > %d): %r' % (w, lim, t.text))
        for i, a in enumerate(ts):
            for b in ts[i + 1:]:
                ha, hb = (14 if a.font == 2 else 11), (14 if b.font == 2 else 11)
                wa = min(len(a.text) * (8 if a.font == 2 else 6.5), a.width or 999)
                wb = min(len(b.text) * (8 if b.font == 2 else 6.5), b.width or 999)
                if (a.x, a.y) == (b.x, b.y):
                    continue        # a cell redrawn over its own copy from G2 (filled first)
                if (a.x < b.x + wb and b.x < a.x + wa and a.y < b.y + hb and b.y < a.y + ha):
                    bad.append('overlap: %r / %r' % (a.text, b.text))
    bad = sorted(set(bad))
    check(not bad, '%s: no text in the strip, too wide, or overlapping%s' %
          (label, '' if not bad else ' -- ' + '; '.join(bad[:6])))


def last_wait(h):
    return [s for s in h.screens if s.reason == 'wait'][-1]


def t_guide():
    h = H()
    h.choose(1)                                   # Guide
    h.tap(78, 125)                                # Nominal (left column, row 2)
    h.tap(78, 87)                                 # two groups, different people
    h.tap(160, 175)                               # the leaf
    h.press('Enter')                              # leave the details page
    h.press('Esc', 'Esc')                         # up to level 1, level 0
    h.press('Down', 'Right', 'Enter')             # keyboard: Survival, pick
    h.press('Right', 'Down', 'Down', 'Enter')     # association (right column, row 3)
    h.press('Enter')                              # details
    h.tap(150, 228)                               # soft key Quiz?  no: x 150 is slot 3
    h.press('Esc')                                # leave the quiz
    h.choose(5)
    r = h.call('TestChooser')
    w = [s for s in h.screens if s.reason == 'wait']
    l0 = w[0]
    check(l0.has('outcome scale?') and l0.has('Interval') and l0.has('Survival'),
          'guide level 0: root and four scales')
    check(l0.menu == ['Guide', 'Table', 'Quiz', '', 'Back', 'Quit'], 'soft keys on level 0')
    blits = h.pages
    # the 7 animation frames after the tap, then the level-1 wait frame
    up = [s for s in blits if s.func == 'tcShow']
    check(any(s.has('Q2: what is being compared?') for s in h.screens), 'level 1 drawn')
    l1 = w[1]
    check(l1.has('Nominal') and l1.has('two groups,') and l1.has('association of'),
          'level 1: breadcrumb Nominal and six designs')
    l2 = w[2]
    check(l2.has("Chi-square 2x2, or Fisher's exact") and l2.has('tap here or Ent'),
          'level 2: the leaf names chi-square / Fisher')
    det = w[3]
    check(det.has("Chi-square 2x2, or Fisher's exact") and
          det.has('Check: expected counts >= 5 in ChiTable.'), 'details page with Check line')
    check(det.has('nominal  |  2 independent groups'), 'details subtitle')
    # orange path drawn in six stages: count LINE_P in orange per frame
    frames = [s for s in h.pages if s.has('outcome') and s.has('two groups,')]
    oranges = [sum(1 for sh in s.shapes if sh.cmd == 'LINE_P' and len(sh.args) > 4
                   and int(sh.args[4]) == 0xFF4500) for s in frames]
    check(any(o > 0 for o in oranges), 'orange path lines drawn (%s)' % oranges[:10])
    check(any(s.has('Survival') and s.has('association of') for s in w), 'keyboard to Survival')
    check(any(s.has('Cox proportional-hazards regression') for s in w),
          'keyboard: survival x association = Cox')
    check(any(s.has('not on the Prime, tap or Ent') for s in w), 'hatched leaf says not on the Prime')
    check(r == 'TestChooser: Cox proportional-hazards regression', 'returns %r' % r)
    page_checks(h, 'guide')
    NOTES.append('     guide: %d screens, %d blits' % (len(h.screens), len(h.pages)))


def t_table():
    h = H()
    h.choose(2)
    h.tap(80, 60)            # first tap on (Interval, 2 groups): select
    h.tap(80, 60)            # second tap: details
    h.press('Enter')         # back
    h.tap(10, 120)           # row label Ordinal (row 3: y 110-144)
    h.tap(150, 20)           # column heading 2 (designs 2-6: x 107-159 -> design 3)
    h.tap(20, 20)            # corner key: the one-sample page
    h.press('Plus')          # light the current row
    h.press('Minus')         # light the column
    h.press('Right', 'Right', 'Right', 'Right', 'Right')   # back to design 6, page slides
    h.press('Enter')         # details of the selected cell
    h.press('Esc')
    h.tap(100, 228)          # soft key Table (stays)
    h.tap(270, 228)          # Back -> menu
    h.choose(5)
    r = h.call('TestChooser')
    w = [s for s in h.screens if s.reason == 'wait']
    check(w[0].has('2 groups') and w[0].has('< show') and
          w[0].has('= not on the Prime (R or JMP; see details)'), 'table: headings, corner, legend')
    check(w[1].has('Unpaired (two-sample) t test') and not w[1].has('What:'),
          'first tap selects and names the test (no details)')
    check(w[2].has('What:') and w[2].has('Check: Stats 1Var normal plot, each group.'),
          'second tap opens the details')
    check(w[4].has('Ordinal row: rank tests - ranks, not means'), 'row label lights the row')
    check(w[5].has('3+ independent groups: different people'), 'heading lights the column')
    check(w[6].has('1 group') and w[6].has('vs value') and w[6].has('show >'),
          'corner key shows the one-sample column')
    check(w[7].has('Interval row: means; assumes roughly normal'), '+ lights the row')
    check(w[8].has('2 independent groups: different people'), '- lights the column')
    check(w[12].has('Pearson r and linear regression') and w[12].has('assoc.')
          and not w[12].has('vs value'), 'Right past design 5 slides back to page 1')
    check(any(s.has('Pearson r and linear regression') and s.has('What:') for s in w),
          'Right x5 then Enter: Pearson details')
    g2 = h.grobs['G2']
    pix = sum(1 for it in g2.items if getattr(it, 'cmd', '') == 'PIXON_P')
    check(pix > 900, 'hatching dots in the G2 cache: %d' % pix)
    builds = sum(1 for c in h.log if c[0] == 'DIMGROB_P' and getattr(c[1][0], 'name', '') == 'G2')
    check(builds <= 3, 'G2 rebuilt only on layout changes (%d builds)' % builds)
    check(r == 'TestChooser: Pearson r and linear regression', 'returns %r' % r)
    page_checks(h, 'table')


def t_quiz():
    h = H()
    h.choose(3)
    h.reset_records()
    # find the order this seed gives, after tcQNew runs inside the quiz: script
    # answers by peeking at tcQOrd between events is impossible, so run a first pass
    # with Esc to learn the order
    h.press('Esc')
    h.choose(5)
    h.call('TestChooser')
    order = [int(v) for v in h.globals_['tcQOrd']]
    check(sorted(order) == list(range(1, 21)), 'a round is a permutation of 1..20: %s' % order)
    # second run, same seed: answer case 1 right, case 2 wrong, then the rest
    h2 = Harness(PROG, strict=True, seed=7)
    bank = {}
    h2.call('tcInit')
    for i in range(1, 21):
        q = h2.call('tcQ', i)
        bank[i] = (int(q[0]), int(q[1]), q[6])
    h2 = Harness(PROG, strict=True, seed=7)
    h2.choose(3)

    def xy(s, d):           # centre of a quiz cell (designs 2-6, rows 62 + 29 r)
        return 54 + (d - 2) * 53 + 26, 62 + (s - 1) * 29 + 14
    right = 0
    for k, c in enumerate(order):
        s, d, _ = bank[c]
        if k % 3 == 1:      # every third case answered wrong
            ws, wd = (s % 4) + 1, d
            h2.tap(*xy(ws, wd))
            if k == 1:
                h2.tap(*xy(s, d))     # tap the green cell: its details
                h2.press('Enter')     # leave the details
            else:
                h2.press('Enter')     # next
        else:
            h2.tap(*xy(s, d))
            h2.press('Enter')         # leave the details page
            right += 1
    h2.press('Esc')                   # leave the round-over page
    h2.choose(5)
    r = h2.call('TestChooser')
    w = [s for s in h2.screens if s.reason == 'wait']
    first = w[0]
    q1 = h2.call('tcQ', order[0])
    check(first.has(q1[3]) and first.has('Score = 0 of 0, case 1 of 20'),
          'quiz: case text and score line')
    green = [s for s in h2.pages if any(getattr(sh, 'cmd', '') == 'RECT_P' and len(sh.args) > 5
                                        and int(sh.args[5]) == 0x008C3C for sh in s.shapes)]
    check(len(green) > 0, 'a green cell is drawn for a right answer')
    det = w[1]
    check(det.has('What:'), 'right answer opens the details page')
    wrong = [s for s in w if s.has('tap green = its details')]
    check(len(wrong) == len([k for k in range(20) if k % 3 == 1]), 'a wrong-answer frame per wrong case (%d)' % len(wrong))
    s2, d2, reason2 = bank[order[1]]
    check(wrong[0].has(reason2), 'the reason line: %r' % reason2)
    check(any(s.has('Round over') and s.has('You picked the right test %d times out of 20.' % right)
              for s in w), 'round over: %d of 20' % right)
    check(r.startswith('TestChooser: '), 'returns %r' % r)
    page_checks(h2, 'quiz')


def t_help_and_quit():
    h = H()
    h.choose(4)
    h.press('Enter')                 # page 2
    h.tap(300, 228)                  # Quit soft key
    r = h.call('TestChooser')
    w = [s for s in h.screens if s.reason == 'wait']
    check(w[0].has('Choosing a test: two questions') and w[1].has('Touch, keys and the quiz'),
          'help: two pages')
    check(r == 'TestChooser: no test looked at', 'Quit soft key leaves: %r' % r)
    page_checks(h, 'help')


def t_soft_jumps():
    h = H()
    h.choose(1)
    h.tap(100, 228)                  # Table soft key from the guide
    h.tap(150, 228)                  # Quiz soft key from the table
    h.tap(20, 228)                   # Guide soft key from the quiz
    h.tap(270, 228)                  # Back -> menu
    h.choose(5)
    h.call('TestChooser')
    w = [s for s in h.screens if s.reason == 'wait']
    check(w[0].has('outcome scale?') and w[1].has('< show') and w[2].has('Score =')
          and w[3].has('outcome scale?'), 'soft keys jump Guide -> Table -> Quiz -> Guide -> menu')




# ------------------------------------------------------------------ beta 2a (harness ppl_run_v3e)
OLD = '/home/claude/work/out/TestChooser_beta2.txt'


def t_beta2a():
    """T1, T2, T3 and the three wordings; the review's check_TestChooser.py on beta 2 and beta 2a."""
    import re
    import io
    import types
    import difflib
    import contextlib
    sys.path.insert(0, '/home/claude/work/out')
    import ppl_run_v3e as R3
    R3_RUNS = []
    _i0 = R3.Harness.__init__

    def _i3(self, *aa, **kk):
        _i0(self, *aa, **kk)
        R3_RUNS.append(self)
    R3.Harness.__init__ = _i3

    # 1. the review's checks, loaded once per version (the script reads its program at import).  Its part C lists
    #    the menu items as written in beta 2; here they are read from each version's own CHOOSE instead, so the
    #    check (no item over 30 characters) tests the file it runs on.
    src = open('/home/claude/work/review/check_TestChooser.py', encoding='utf-8').read()
    hard = "    items = ['Guide me: the flowchart', 'Browse the table (Glantz)', 'Quiz: which test fits the case?', 'Help', 'Quit']\n"
    assert src.count(hard) == 1 and src.count("PROG = '/home/claude/work/review/fleet/TestChooser_beta2.txt'\n") == 1
    res = {}
    for path in (OLD, PROG):
        s = src.replace("PROG = '/home/claude/work/review/fleet/TestChooser_beta2.txt'\n", 'PROG = %r\n' % path)
        s = s.replace(hard, "    items = re.findall(r'\"([^\"]*)\"', re.search(r'CHOOSE\\(mnI, \"Which statistical test\\?\", \\{(.*?)\\}\\);', SRC, re.S).group(1))\n")
        m = types.ModuleType('check_TestChooser_%d' % len(res))
        m.__file__ = '/home/claude/work/review/check_TestChooser.py'
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(s, m.__file__, 'exec'), m.__dict__)
            for L in 'ABCDEF':
                getattr(m, 'part' + L)()
        res[path] = (m.NCHK[0], list(m.FAILS), buf.getvalue())
    no, fo, _ = res[OLD]
    nn, fn, logn = res[PROG]
    NOTES.append('     the review\'s check_TestChooser on beta 2: %d checks, failed %s' % (no, [f[:60] for f in fo]))
    NOTES.append('     the review\'s check_TestChooser on beta 2a: %d checks, failed %s' % (nn, fn or 'none'))
    check(len(fo) == 3 and any(f.startswith('A tcNotP') for f in fo) and any(f.startswith('B no reference') for f in fo)
          and any(f.startswith('C menu items') for f in fo),
          'beta2a: the review\'s three failing checks (A: T3 hatching, B: T1 ConTable2/FEP, C: T2 menu line) fail on beta 2')
    check(not fn and nn == no, 'beta2a: check_TestChooser on beta 2a: all %d checks pass' % nn)

    # 2. the details pages as drawn: T1 and the wordings
    want = {6: (4, 'Fleet: EpiStats > 2x2 Table; ChiTable.'),
            8: (3, 'Fleet: EpiStats > 2x2 Table > Paired.'),
            10: (3, 'Fleet: EpiStats > Risk; Inference X2.'),
            7: (2, 'Expected < 5 in <= 20% of cells; none < 1.'),
            9: (3, 'Not on the Prime.  R: RVAideMemoire pkg.'),
            16: (2, 'Most powerful if hazards are proportional.')}
    for i, (ln, txt) in sorted(want.items()):
        h = R3.Harness(PROG, strict=False, cas='fail', stall_limit=30000, idle_key=4)
        h.call('tcInit')
        h.reset_records()
        h.call('tcDetails', float(i), 1.0, 1.0)
        pg = h.pages[0]
        lines = [(t.text, t.x, t.y) for t in pg.texts]
        y = {1: 55, 2: 81, 3: 119, 4: 145, 5: 171}[ln]
        got = [t for t, x, yy in lines if yy == y]
        check(got == [txt] and all(len(t) <= 42 and x + 6.2 * len(t) <= 312 for t, x, yy in lines if x == 14),
              'beta2a: details page of test %d, line %d (y = %d) reads %r; every detail line <= 42 characters'
              % (i, ln, y, got[0] if got else None))
        if i == 8:
            l4 = [t for t, x, yy in lines if yy == 145]
            check(l4 == ['By hand, 1 df: X2 = (|b-c| - 1)^2/(b+c).'],
                  'beta2a: McNemar, "Afterwards:" reads %r -- the continuity-corrected statistic of es_McNemar' % l4)
    check(R3.Harness(PROG).call('tcDetail', 1.0)[1] == 'Normal-ish data; Welch form if SDs differ.',
          'beta2a: test 1 keeps "Welch form if SDs differ" (D12 is open)')
    code = [l.split('//')[0] for l in open(PROG, encoding='utf-8').read().split('\n') if not l.strip().startswith('//')]
    stale = [l.strip() for l in code if re.search(r'\b(ConTable2|FEP)\b', l)]
    check(not stale, 'beta2a: no code line names ConTable2 or FEP (%d)' % len(stale))
    # EpiStats really has those modules
    es = open('/home/claude/work/out/EpiStats_v1.7c.txt', encoding='utf-8').read()
    check('"2×2 Table Analysis"' in es and '"Risk Analysis (RR, OR, NNT)"' in es and 'rpT := {"Cohort", "Diagnostic", "Paired"};' in es
          and 'es_McNemar(mnB, mnC)' in es and 'es_FisherExact(a, b, c, d)' in es,
          'beta2a: EpiStats v1.7c has the "2×2 Table Analysis" module (Fisher, the Paired reading with McNemar) and '
          '"Risk Analysis (RR, OR, NNT)" -- the places the pages now name')

    # 3. T3: test 18 is hatched like test 19; the drawn table has one more hatched cell
    h = R3.Harness(PROG)
    h.call('tcInit')
    notp = [int(v) for v in h.globals_['tcNotP']]
    rule = [1 if any(l.startswith('Not on the Prime') for l in h.call('tcDetail', float(i))) else 0 for i in range(1, 25)]
    check(notp == rule and notp[17] == 1 and notp[18] == 1 and sum(notp) == 13,
          'beta2a T3: tcNotP = the tests whose details say "Not on the Prime" (13), 18 and 19 both hatched')
    dots = {}
    for path in (OLD, PROG):
        hh = R3.Harness(path, strict=False, cas='fail', stall_limit=30000, idle_key=4)
        hh.call('tcInit')
        hh.reset_records()
        hh.choose(2)
        hh.choose(5)
        try:
            hh.call('TestChooser')
        except Exception:
            pass
        dots[path] = sum(1 for c, a in hh.log if c == 'PIXON_P' and hh._grob_args(a)[0].name == 'G2')
    check(dots[PROG] > dots[OLD] > 900, 'beta2a T3: the table\'s hatching dots in G2: beta 2 %d, beta 2a %d (one more cell)'
          % (dots[OLD], dots[PROG]))

    # 4. T2: the menu
    hm = R3.Harness(PROG, strict=False, cas='fail', stall_limit=30000, idle_key=4)
    hm.choose(5)
    r = hm.call('TestChooser')
    items = hm.chooses[0].items
    check(items == ['Guide me: the flowchart', 'Browse the table (Glantz)', 'Quiz: which test fits?', 'Help', 'Quit']
          and max(len(x) for x in items) <= 30, 'beta2a T2: the menu reads %r (longest %d)' % (items, max(len(x) for x in items)))
    hq = R3.Harness(PROG, strict=False, cas='fail', stall_limit=30000, idle_key=4, seed=5)
    hq.choose('Quiz: which test fits?')
    hq.choose(5)
    hq.call('TestChooser')
    check(any(sc.has('Score =') for sc in hq.screens), 'beta2a T2: the renamed item still opens the quiz')

    # 5. the routine diff beta 2 -> beta 2a, and the static rules
    def bodies(txt):
        c = re.sub(r'//[^\n]*', '', txt)
        out = {}
        for mm in re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S):
            out[mm.group(1)] = re.sub(r'\n\s*\n', '\n', re.sub(r'[ \t]+\n', '\n', mm.group(0)))
        return out
    t0, t1 = open(OLD, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()
    B0, B1 = bodies(t0), bodies(t1)
    dif = sorted(n for n in set(B0) | set(B1) if B0.get(n) != B1.get(n))
    check(dif == ['TestChooser', 'tcDetail', 'tcInit'], 'beta2a: the routines that differ from beta 2: %s (want '
          'TestChooser (the menu), tcDetail, tcInit (tcNotP)); %d routines' % (dif, len(B1)))

    def code_lines(t):
        out = []
        for l in t.split('\n'):
            o, ins = [], False
            for j, ch in enumerate(l):
                if ch == '"':
                    ins = not ins
                if not ins and l[j:j + 2] == '//':
                    break
                o.append(ch)
            x = ''.join(o).strip()
            if x:
                out.append(x)
        return out
    k0, k1 = code_lines(t0), code_lines(t1)
    mi, pl = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
        if op in ('replace', 'delete'):
            mi += k0[i1:i2]
        if op in ('replace', 'insert'):
            pl += k1[j1:j2]
    NOTES.append('     beta 2 -> beta 2a code lines: -%d +%d' % (len(mi), len(pl)))
    check(len(mi) == len(pl) == 9 and sum(1 for l in pl if l.startswith('"')) == 8 and any('tcNotP :=' in l for l in pl),
          'beta2a: 9 code lines changed: 7 detail strings, 1 menu string, the tcNotP list')
    depth, bad = 0, []
    for n_, l in enumerate(t1.split('\n'), 1):
        ins, start = False, depth
        for j, ch in enumerate(l):
            if ch == '"':
                ins = not ins
            elif not ins:
                if l[j:j + 2] == '//':
                    if start > 0:
                        bad.append(n_)
                    break
                if ch in '({[':
                    depth += 1
                elif ch in ')}]':
                    depth -= 1
    check(not bad, 'beta2a: no // comment inside an open bracket %s' % bad[:3])
    vl = t1.split('\n')
    check(vl[3] == '// TESTCHOOSER - beta 2a' and '// beta 2a (19 Oct 2026) - what changed' in t1
          and 'only in the PC harness (ppl_run_v3e, 19 Oct 2026)' in t1
          and '// DISCLAIMER: a teaching and demonstration aid. Not validated for' in t1,
          'beta2a: the banner, the beta 2a paragraph, the status line (PC harness only) and the disclaimer')
    sci = sorted(set(x[2] for hh_ in R3_RUNS for x in hh_.sci_strings))
    check(not sci, 'beta2a: no scientific fixed decimal in the %d ppl_run_v3e runs above %s' % (len(R3_RUNS), sci[:3]))
    locs = re.findall(r'^\s*LOCAL ([^;(]*);', '\n'.join(k1), re.M)
    check(max(len(x.split(',')) for x in locs) <= 6 and not any('INSTRING(' in l for l in k1),
          'beta2a: every LOCAL line holds at most 6 names; no INSTRING')


for t in (t_bank, t_hatch_and_strings, t_guide, t_table, t_quiz, t_help_and_quit, t_soft_jumps, t_beta2a):
    try:
        t()
    except Exception as e:      # a harness stall or PPL error is a failure
        FAILS.append('FAIL %s raised %s: %s (stack %s)' % (t.__name__, type(e).__name__, e,
                                                           getattr(e, 'ppl_stack', '')))
print('\n'.join(NOTES))
print('\n'.join(FAILS))
print('%d checks passed, %d failed' % (sum(1 for n in NOTES if n.startswith('ok')), len(FAILS)))
sys.exit(1 if FAILS else 0)
