#!/usr/bin/env python3
"""verify_TestChooser.py -- PC checks for TestChooser beta 2 (16 Oct 2026).

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

PROG = '/home/claude/work/out/TestChooser_beta2.txt'
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
    rule = [1 if h.call('tcDetail', i)[2].startswith('Not on the Prime') else 0
            for i in range(1, 25)]
    check(notp == rule, 'tcNotP equals the line-3 rule')
    check(sum(notp) == 12, 'twelve hatched tests (%d)' % sum(notp))
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


for t in (t_bank, t_hatch_and_strings, t_guide, t_table, t_quiz, t_help_and_quit, t_soft_jumps):
    try:
        t()
    except Exception as e:      # a harness stall or PPL error is a failure
        FAILS.append('FAIL %s raised %s: %s (stack %s)' % (t.__name__, type(e).__name__, e,
                                                           getattr(e, 'ppl_stack', '')))
print('\n'.join(NOTES))
print('\n'.join(FAILS))
print('%d checks passed, %d failed' % (sum(1 for n in NOTES if n.startswith('ok')), len(FAILS)))
sys.exit(1 if FAILS else 0)
