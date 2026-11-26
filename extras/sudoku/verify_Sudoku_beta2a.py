#!/usr/bin/env python3
"""verify_Sudoku_beta2a.py -- checks Sudoku beta 2a (Sudoku_beta2a.txt) in the PC harness ppl_run_v3e.
  Made from verify_Sudoku_beta2.py (26 Nov 2026): every check of beta 2 is kept, the Enter menu's Help and
  Exit Sudoku are one place lower, and part D16 checks what beta 2a adds (My games and the clock).

  A  the file: the opening #pragma line, the Home settings as the first statement of Sudoku(), ASCII code,
     the tables the build wrote (units, peers, base puzzles) against a fresh computation
  B  the engine (suEInit, suESolve) against su_engine.py (the line-for-line Python copy) and an independent
     brute-force solver: the answer, the number of answers (capped at 2) and the five step counts, on the
     24 base puzzles, the sample and four published hard puzzles (beta 1's numbers), a puzzle with two
     answers, one with none, and clashing clues
  C  suNew: 400 new puzzles -- each answer a Sudoku grid, each clue the answer's digit, exactly one answer,
     the base puzzle's clue count, the level kept (Easy by the only-digit step alone, Medium without a
     guess, Hard and Expert with one), every base puzzle and both diagonals used
  D  the board, driven by taps and keys: a whole game played to the end (fireworks, SU_SOLVED, the line
     returned), pencil marks and every kind of Undo, the hints (wrong digit, only digit, only square in a
     row, a column and a box, fewest choices, the second press), Check, Watch (the bar chart's counts =
     the engine's), Solve, Restart, Type (auto-advance, Erase, Play: too few clues, clashing clues, two
     answers, no answer, one answer and M9, Esc during the check), M9 (good, wrong size, 2.5, 10), the
     Enter menu, Help, the arrow keys and the digit keys, WAIT(-1) giving up, the flash of a finished row,
     the stale-click guard, and Esc or Cancel at every dialog
  D16 beta 2a: a finished game goes into My games (its level, clues, minutes, Hints and Checks), and a game
     ended by Solve or Watch does not; a typed puzzle is level 5; the full log; the clock leaves out a
     dialog's time and counts one wait for two minutes at most; the My games page with 0, 1, 2 and 13 games
     (r, the least-squares line and its ends, the dots, the counts and the medians against Python); 2Var with
     the columns empty, holding data (Yes, No, Cancel), one game; Clear (Yes, No, Cancel); Help by soft key
     and by key; the stale-click guard on the page; My games from the first menu and the Enter menu; the
     line returned after a logged game
  E  the text: every screen of D through text_overlap_v1 and label_fit_v1 (no firm overlap, straddle or
     overrun), every message line at most 17 characters, CHOOSE titles (31) and items (30), MSGBOX texts
     in at most 5 lines of 30 characters, and every line returned at most 100 characters
Run:  HPKIT=<hp-prime-kit folder> python3 verify_Sudoku_beta2a.py [Sudoku_beta2a.txt]
      (su_engine.py and base_puzzles.json beside this file or in Sudoku_build/; the fleet's tools in
      $TTL_TOOLS, tools/, ../tools or hp-prime-statistics/tools)
"""
import os, sys, re, json, time, random, collections
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = next((d for d in (HERE, os.path.join(HERE, 'build'), os.path.join(HERE, 'Sudoku_build'))   # extras/sudoku/build/ in the repository
              if os.path.exists(os.path.join(d, 'su_engine.py'))), os.path.join(HERE, 'Sudoku_build'))
def _tools():
    # the fleet's tools: $TTL_TOOLS, or tools/ beside this file or one folder up, or inside hp-prime-statistics/
    for d in [os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
              os.path.join(HERE, '..', '..', 'tools'),                    # extras/sudoku/ in the repository
              os.path.join(HERE, 'hp-prime-statistics', 'tools'), '/home/claude/hp-prime-statistics/tools']:
        if d and os.path.exists(os.path.join(d, 'ppl_run_v3e.py')):
            return os.path.abspath(d)
    raise SystemExit('the fleet tools (ppl_run_v3e.py, text_overlap_v1.py) were not found: set TTL_TOOLS')
TOOLS = _tools()
WIDTHS = os.path.join(TOOLS, '..', 'verify', 'round11', 'glyph_widths_vc.json')
sys.path.insert(0, BUILD); sys.path.insert(0, TOOLS)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
import ppl_run_v3e as R
import su_engine as E
import text_overlap_v1 as T

PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'Sudoku_beta2a.txt')
SRC = open(PROG, encoding='utf-8').read()
BASE = json.load(open(os.path.join(BUILD, 'base_puzzles.json')))
LEVELS = ['Easy', 'Medium', 'Hard', 'Expert']

RESULTS = []
def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok)))
    print('%-4s %-58s %s' % ('PASS' if ok else 'FAIL', name, detail))

# ------------------------------------------------------------------ the harness, with a human's pace
class H(R.Harness):
    """WAIT(-1) hands each event over 200 ms after it was called (a person needs that long to see the
    screen and tap), except the calls numbered in `instant`, which model an event already queued."""
    def __init__(self, *a, **k):
        R.Harness.__init__(self, *a, **k)
        self.nwait, self.instant = 0, set()
        self.extra = {}          # beta 2a: wait call number -> more milliseconds (the calculator was off)
        self.dialog_ms = 0.0     # beta 2a: the time a person spends in each CHOOSE or MSGBOX
    def _wait(self, a):
        v = R.Harness._wait(self, a)
        self.nwait += 1
        if self.nwait not in self.instant:
            self.clock += 200.0
        self.clock += self.extra.get(self.nwait, 0.0)
        return v
    def _choose(self, nodes, frame):
        self.clock += self.dialog_ms
        return R.Harness._choose(self, nodes, frame)
    def _msgbox(self, a):
        self.clock += self.dialog_ms
        return R.Harness._msgbox(self, a)

SCREENS = []          # every screen of part D, for part E
MSGLINES = collections.Counter()
def harness(strict=True, seed=1):
    h = H([PROG], idle_key=4, strict=strict, seed=seed)
    h.execute('suSetup()')
    return h

def keep(h):
    """Collect the screens and message lines of a drive, then empty the harness's records."""
    for s in h.screens:
        SCREENS.append(s)
    del h.screens[:]
    m = h.globals_.get('suMsg')
    if isinstance(m, list):
        for x in m:
            MSGLINES[x] += 1

def fl(xs):
    return [float(x) for x in xs]

def digits(s):
    return [0 if c in '.0' else int(c) for c in s]

SK = [27, 80, 133, 187, 240, 294]          # soft-key centres
def sq(k):                                  # the middle of square k
    r, c = (k - 1) // 9, (k - 1) % 9
    return (2 + 24 * c + 12, 2 + 24 * r + 12)
def pad(d):
    return (222 + 33 * ((d - 1) % 3) + 15, 18 + 23 * ((d - 1) // 3) + 10)
ERASE, NOTES = (242, 96), (291, 96)

def setgame(h, clue, sol, level=1.0):
    g = h.globals_
    g['suClue'] = fl(clue); g['suSol'] = fl(sol); g['suLevel'] = float(level)
    h.execute('suResetPlay()')
    g['suMsg'] = []; g['suMsgC'] = 0.0; g['suStale'] = 0.0

def play(h, events):
    """Queue taps ('t', x, y), keys ('k', code[, anytime]) and CHOOSE answers ('c', n), then run suPlay."""
    for e in events:
        if e[0] == 't': h.tap(e[1], e[2])
        elif e[0] == 'k': h.press(e[1], anytime=(len(e) > 2 and e[2]))
        elif e[0] == 'c': h.choose(e[1])
    r = h.execute('suPlay()')
    keep(h)
    return r

def G(h, name):
    v = h.globals_[name]
    return [int(x) if isinstance(x, float) else x for x in v] if isinstance(v, list) else v

def tapsq(k): x, y = sq(k); return ('t', x, y)
def tappad(d): x, y = pad(d); return ('t', x, y)
def soft(s): return ('t', SK[s - 1], 230)

# ------------------------------------------------------------------ an independent solver
def brute(clue, cap=2):
    """Count answers (up to cap) by plain backtracking over bit masks; returns (count, first answer)."""
    g = list(clue); rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9
    for i, d in enumerate(g):
        if d:
            r, c, b = i // 9, i % 9, (i // 27) * 3 + (i % 9) // 3
            bit = 1 << d
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return -1, None
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
    found = []
    def rec():
        best, bi = None, -1
        for i in range(81):
            if g[i] == 0:
                r, c, b = i // 9, i % 9, (i // 27) * 3 + (i % 9) // 3
                free = [d for d in range(1, 10) if not ((rows[r] | cols[c] | boxes[b]) >> d) & 1]
                if best is None or len(free) < len(best):
                    best, bi = free, i
                    if len(free) <= 1: break
        if bi < 0:
            found.append(list(g)); return len(found) >= cap
        r, c, b = bi // 9, bi % 9, (bi // 27) * 3 + (bi % 9) // 3
        for d in best:
            bit = 1 << d
            g[bi] = d; rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            if rec(): return True
            g[bi] = 0; rows[r] &= ~bit; cols[c] &= ~bit; boxes[b] &= ~bit
        return False
    rec()
    return len(found), (found[0] if found else None)

def is_grid(s):
    for u in range(27):
        cells = [E.UNIT[u * 9 + n] for n in range(1, 10)]
        if sorted(s[k - 1] for k in cells) != list(range(1, 10)):
            return False
    return True

# ================================================================== A
print('== A  the file')
lines = SRC.split('\n')
check('A1 the first line is the fleet pragma', lines[0] == '#pragma mode( separator(.,;) integer(h32) )')
m = re.search(r'EXPORT Sudoku\(\)\nBEGIN\n((?:  LOCAL [^\n]*\n)*)  ([^\n]*)', SRC)
check('A2 Home settings first in Sudoku()', m and m.group(2).startswith('HSeparator := 0; HFormat := 0; HAngle := 0; Entry := 0;'))
def code_part(line):                       # the line without strings and // comments
    out, q = '', False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"': q = not q
        elif not q and line[i:i + 2] == '//': break
        elif not q: out += ch
        i += 1
    return out
bad = [i + 1 for i, l in enumerate(lines) if any(ord(ch) > 126 for ch in code_part(l))]
check('A3 executable code is ASCII', not bad, bad[:5])
def ppl_list(name):
    mm = re.search(r'LOCAL %s := (\{[^\n]*\});' % name, SRC)
    return json.loads(mm.group(1).replace('{', '[').replace('}', ']'))
check('A4 suUnit = the 27 units', ppl_list('suUnit') == E.UNIT[1:])
check('A5 suPeer = the 20 peers of each square', ppl_list('suPeer') == E.PEER[1:])
bp, bs = ppl_list('suBP'), ppl_list('suBS')
want_bp = [b['p'] for lv in LEVELS for b in BASE[lv]]
want_bs = [b['s'] for lv in LEVELS for b in BASE[lv]]
check('A6 suBP and suBS = the 24 base puzzles, by level', bp == want_bp and bs == want_bs, '%d puzzles' % len(bp))
check('A7 no != in the code (on the Prime it is a factorial)', not any('!=' in code_part(l) for l in lines))
check('A8 no string holds a quotation mark', '\\"' not in SRC)

# ================================================================== B
print('== B  the engine')
SAMPLE = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
SAMPLE_ANS = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
HARD = {
    "17 clues (Royle)": "000000010400000000020000000000050407008000300001090000300400200050100000000806000",
    "anti-brute-force (Norvig)": "..............3.85..1.2.......5.7.....4...1...9.......5......73..2.1........4...9",
    "Easter Monster": "1.......2.9.4...5...6...7...5.9.3.......7.......85..4.7.....6...3...9.8...2.....1",
    "Inkala 2012": "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..",
}
BETA1 = {"Easter Monster": (3823, 3763), "Inkala 2012": (2080, 2020),
         "17 clues (Royle)": (64, 0), "anti-brute-force (Norvig)": (64, 0)}
# two answers: blank sample clues one at a time until a second answer appears
two = digits(SAMPLE)
for k in range(81):
    if two[k]:
        keep_d, two[k] = two[k], 0
        if brute(two)[0] >= 2: break
nosol = digits(SAMPLE); nosol[2] = 1 if SAMPLE_ANS[2] != '1' else 2       # a wrong digit, no clash
assert brute(nosol)[0] == 0
clash = digits(SAMPLE); clash[1] = 5                                      # two 5s in row 1
CASES = [('base %s %d' % (lv, i + 1), digits(b['p'])) for lv in LEVELS for i, b in enumerate(BASE[lv])]
CASES += [('sample', digits(SAMPLE))] + [(n, digits(s)) for n, s in HARD.items()]
CASES += [('two answers', two), ('no answer', nosol), ('clashing clues', clash)]

hB = harness()
def ppl_solve(clue, want):
    g = hB.globals_
    g['suEV'] = fl(clue)
    r = hB.execute('suEInit()')
    if r > 0:
        return ('clash', int(r))
    n = hB.execute('suESolve(%d, 0)' % want)
    first = [int(x) for x in g['suSol1']] if g['suSol1'] else None
    st = tuple(int(g[x]) for x in ('suSN', 'suSH', 'suSG', 'suSU', 'suSS'))
    del hB.screens[:]
    return (int(n), first, st)
def py_solve(clue, want):
    e = E.Engine(clue)
    if e.bad:
        return ('clash', e.bad)
    n, first, st = e.solve(want)
    return (n, first, (st['naked'], st['hidden'], st['guesses'], st['undos'], st['steps']))

t0 = time.time(); agree = 0; worst = ''
for name, clue in CASES:
    for want in (1, 2):
        a, b = ppl_solve(clue, want), py_solve(clue, want)
        if a == b: agree += 1
        else: worst = '%s want %d: PPL %s, Python %s' % (name, want, str(a)[:80], str(b)[:80])
check('B1 PPL engine = Python copy (answer, count, 5 counts)', agree == 2 * len(CASES),
      '%d of %d runs, %.0f s %s' % (agree, 2 * len(CASES), time.time() - t0, worst))
ok_b = 0
for name, clue in CASES:
    n_py = py_solve(clue, 2)
    n_br = brute(clue)
    if n_py[0] == 'clash':
        ok_b += (n_br[0] == -1)
    else:
        ok_b += (n_py[0] == n_br[0] and (n_br[0] == 0 or n_py[1] == n_br[1] or n_br[0] == 2))
check('B2 answer counts = an independent brute-force solver', ok_b == len(CASES), '%d of %d' % (ok_b, len(CASES)))
r = ppl_solve(digits(SAMPLE), 1); r2 = ppl_solve(digits(SAMPLE), 2)
check('B3 sample: one answer, the published one, 51 steps, 0 undos (beta 1)',
      r2[0] == 1 and ''.join(map(str, r[1])) == SAMPLE_ANS and r[2][4] == 51 and r[2][3] == 0, r[2])
for name, (steps, undos) in BETA1.items():
    r = ppl_solve(digits(HARD[name]), 1)
    check('B4 %s: %s steps, %s undos as in beta 1' % (name, steps, undos), r[2][4] == steps and r[2][3] == undos, r[2])
r = ppl_solve(two, 2); check('B5 a puzzle with two answers: 2', r[0] == 2, '%d clues' % sum(1 for d in two if d))
r = ppl_solve(nosol, 2); check('B6 a puzzle with no answer: 0', r[0] == 0)
r = ppl_solve(clash, 2); check('B7 clashing clues: the square of the second 5', r == ('clash', 2), r)
# the counts kept up to date (suEPut / suETake) equal counts made afresh, along a whole search
g = hB.globals_
g['suEV'] = fl(digits(HARD['Inkala 2012'])); hB.execute('suEInit()')
rnd = random.Random(7); fresh_ok = 0; trials = 0
for step in range(300):
    ev = [int(x) for x in g['suEV']]
    empties = [k for k in range(1, 82) if ev[k - 1] == 0]
    filled = [k for k in range(1, 82) if ev[k - 1] and k not in set(i + 1 for i, d in enumerate(digits(HARD['Inkala 2012'])) if d)]
    if filled and rnd.random() < 0.4:
        k = rnd.choice(filled); hB.execute('suETake(%d, %d)' % (k, ev[k - 1]))
    else:
        cands = [(k, d) for k in empties for d in range(1, 10)
                 if all(g['suEH'][(u - 1) * 9 + d - 1] == 0 for u in (E.ROW[k], 9 + E.COL[k], 18 + E.BOX[k]))]
        if not cands: continue
        k, d = rnd.choice(cands); hB.execute('suEPut(%d, %d)' % (k, d))
    e = E.Engine([int(x) for x in g['suEV']])
    trials += 1
    fresh_ok += ([int(x) for x in g['suEH']] == e.H[1:] and [int(x) for x in g['suEC']] == [e.C[k] if e.V[k] == 0 else int(g['suEC'][k - 1]) for k in range(1, 82)]
                 and all(int(g['suEP'][i]) == e.P[i + 1] for i in range(243) if e.H[i + 1] == 0))
check('B8 counts kept by suEPut/suETake = counts made afresh', fresh_ok == trials, '%d random moves' % trials)
del hB

# ================================================================== C
print('== C  new puzzles')
hC = harness(seed=11)
used = collections.Counter(); trans = collections.Counter(); badC = []
def solve_class(clue):
    n, first, st = E.Engine(clue).solve(1)
    return st
for i in range(400):
    lv = 1 + i % 4
    hC.execute('suNew(%d)' % lv)
    clue, sol = G(hC, 'suClue'), G(hC, 'suSol')
    n_ok = is_grid(sol) and all(c in (0, s) for c, s in zip(clue, sol))
    nb, first = brute(clue)
    n_ok = n_ok and nb == 1 and first == sol
    nclue = sum(1 for c in clue if c)
    # which base puzzle: the one whose clue count and step profile match
    st = solve_class(clue)
    lvname = LEVELS[lv - 1]
    if lvname == 'Easy': lvl_ok = st['guesses'] == 0 and st['hidden'] == 0
    elif lvname == 'Medium': lvl_ok = st['guesses'] == 0 and st['hidden'] > 0
    else: lvl_ok = st['guesses'] > 0
    counts = sorted(b['clues'] for b in BASE[lvname])
    if not (n_ok and lvl_ok and nclue in counts):
        badC.append((i, lvname, n_ok, lvl_ok, nclue))
    # which base puzzle, by its sorted clue-digit pattern (digit renaming, line moves and the diagonal
    # keep the multiset of row/column clue counts)
    rc = tuple(sorted(sum(1 for c in range(9) if clue[r * 9 + c]) for r in range(9)))
    used[(lvname, nclue, rc)] += 1
    del hC.screens[:]
check('C1 400 new puzzles: a grid, its clues, one answer, the level kept', not badC, badC[:3])
pats = collections.Counter(k[0] for k in used)
check('C2 every level shows several different base puzzles', all(pats[lv] >= 4 for lv in LEVELS), dict(pats))
# the diagonal: seen both ways (the first row's clue count equals the base's first row or first column)
diag = collections.Counter()
for seed in range(60):
    h2 = harness(seed=1000 + seed)
    h2.execute('suNew(1)')
    clue = G(h2, 'suClue')
    # undo the digit renaming and compare with the base puzzles directly and turned over
    found = None
    for bi, b in enumerate(BASE['Easy']):
        p = digits(b['p'])
        for turn in (0, 1):
            q = [p[(c % 9) * 9 + c // 9] if turn else p[c] for c in range(81)]
            if sorted(sum(1 for c in range(9) if q[r * 9 + c]) for r in range(9)) == sorted(sum(1 for c in range(9) if clue[r * 9 + c]) for r in range(9)) \
               and sorted(sum(1 for r in range(9) if q[r * 9 + c]) for c in range(9)) == sorted(sum(1 for r in range(9) if clue[r * 9 + c]) for c in range(9)):
                found = (bi, turn)
    trans[found is not None] += 1
    if found: diag[found[1]] += 1
check('C3 each new Easy puzzle traced back to a base puzzle', trans[True] == 60, dict(trans))
check('C4 the grid is turned over on its diagonal in some games and not in others', diag[0] > 0 and diag[1] > 0, dict(diag))
del hC

# ================================================================== D
print('== D  the board')
EASY = digits(BASE['Easy'][0]['p']); EASY_S = digits(BASE['Easy'][0]['s'])
empties = [k for k in range(1, 82) if EASY[k - 1] == 0]

# D1 a whole game, played to the end by taps
h = harness()
setgame(h, EASY, EASY_S)
ev = []
for k in empties:
    ev += [tapsq(k), tappad(EASY_S[k - 1])]
ev += [('k', 30)]                          # a key to leave the fireworks page
r = play(h, ev)
g = h.globals_
check('D1 a whole Easy game by taps: solved', g['suGame'] == 2.0 and G(h, 'suUsr') == [0 if c else s for c, s in zip(EASY, EASY_S)])
M = g.get('SU_SOLVED')
check('D1 SU_SOLVED holds the answer', M is not None and [int(v) for row in M.rows for v in row] == EASY_S)
txt = [t.text for s in SCREENS[-40:] for t in s.items if t.__class__.__name__ == 'Text']
check('D1 the fireworks page and its lines were shown', 'Solved!' in txt and any(x.startswith('Your time: ') for x in txt)
      and 'Press a key or tap to go on.' in txt)
# the line Sudoku() returns after a solved game
h = harness(); setgame(h, EASY, EASY_S)
h.choose(0)                               # the first menu: Cancel
g = h.globals_
g['suUsr'] = fl([0 if c else s for c, s in zip(EASY, EASY_S)]); g['suGame'] = 2.0; g['suTEl'] = 754000.0
ret = h.execute('Sudoku()')
check('D1 the line returned after a solved game', ret == 'Sudoku: solved in 12:34. The answer is in SU_SOLVED.', ret)
RETURNS = [ret]

# D2 the flash of a finished row: the last square of row 1
h = harness(); setgame(h, EASY, EASY_S)
row1 = [k for k in empties if k <= 9]
g = h.globals_
u = [0] * 81
for k in row1[:-1]: u[k - 1] = EASY_S[k - 1]
g['suUsr'] = fl(u)
play(h, [tapsq(row1[-1]), tappad(EASY_S[row1[-1] - 1])])
# a finished row is drawn with the gold RGB(255,215,0) once, then without it
def has_color(scr, rgb):
    want = float((rgb[0] << 16) | (rgb[1] << 8) | rgb[2])
    for it in scr.items:
        if it.__class__.__name__ == 'Shape' and it.cmd == 'RECT_P':
            if any(isinstance(a, float) and a == want for a in it.args[-2:]):
                return True
    return False
golds = [has_color(s, (255, 215, 0)) for s in SCREENS[-8:]]
check('D2 a finished row flashes gold, then the flash goes', any(golds) and not golds[-1] and h.globals_['suFlash'] == [], golds)

# D3 pencil marks, the peers' marks cleared by a digit, and every kind of Undo
h = harness(); setgame(h, EASY, EASY_S)
k0 = empties[0]
peer_empty = [p for p in E.PEER[(k0 - 1) * 20 + 1:(k0 - 1) * 20 + 21] if EASY[p - 1] == 0]
d0 = EASY_S[k0 - 1]
ev = [soft(2)]                             # Notes on
ev += [tapsq(peer_empty[0]), tappad(d0), tappad(9 if d0 != 9 else 8)]
ev += [tapsq(peer_empty[1]), tappad(d0)]
ev += [soft(2)]                            # Notes off
ev += [tapsq(k0), tappad(d0)]              # the digit: the peers' marks of d0 go
play(h, ev)
notes = G(h, 'suNote')
check('D3 a digit clears its peers\' marks of that digit', notes[peer_empty[0] - 1] == (1 << ((9 if d0 != 9 else 8) - 1))
      and notes[peer_empty[1] - 1] == 0 and G(h, 'suUsr')[k0 - 1] == d0, notes[peer_empty[0] - 1])
play(h, [soft(4)])                         # Undo: the digit goes, the marks come back
notes = G(h, 'suNote')
check('D3 Undo puts the digit\'s cleared marks back', G(h, 'suUsr')[k0 - 1] == 0 and notes[peer_empty[1] - 1] == (1 << (d0 - 1))
      and notes[peer_empty[0] - 1] == (1 << (d0 - 1)) | (1 << ((9 if d0 != 9 else 8) - 1)))
play(h, [soft(4)])                         # Undo a mark toggle
check('D3 Undo takes back a pencil mark', G(h, 'suNote')[peer_empty[1] - 1] == 0)
play(h, [tapsq(peer_empty[0]), ('t',) + ERASE])     # Erase the square's marks
check('D3 Erase clears a square\'s marks', G(h, 'suNote')[peer_empty[0] - 1] == 0)
play(h, [soft(4)])
check('D3 Undo puts a square\'s erased marks back', G(h, 'suNote')[peer_empty[0] - 1] != 0)
before = G(h, 'suNote')
play(h, [('k', 30), ('c', 5)])             # Enter menu: Fill in all pencil marks
filled = G(h, 'suNote')
e = E.Engine(EASY)
want_fill = [0 if EASY[k - 1] else sum(1 << (d - 1) for d in range(1, 10) if e.cand(k, d)) for k in range(1, 82)]
check('D3 Fill in all pencil marks = every digit that fits', filled == want_fill)
play(h, [soft(4)])
check('D3 one Undo puts the old marks back', G(h, 'suNote') == before)
play(h, [('k', 30), ('c', 6)])             # Clear all pencil marks
check('D3 Clear all pencil marks', G(h, 'suNote') == [0] * 81)
play(h, [soft(4)])
check('D3 one Undo puts them back', G(h, 'suNote') == before)
UL = h.globals_['suUL']
play(h, [soft(4)] * 12)
check('D3 Undo with nothing left says so', h.globals_['suUL'] == 0 and G(h, 'suMsg') == ['There is nothing', 'left to undo.'])

# D4 hints
h = harness(); setgame(h, EASY, EASY_S)
wrongk = empties[3]; wd = EASY_S[wrongk - 1] % 9 + 1
play(h, [tapsq(wrongk), tappad(wd), soft(3)])
check('D4 Hint shows a wrong digit first', h.globals_['suSel'] == wrongk and h.globals_['suWrongOn'] == 1.0
      and G(h, 'suMsg')[0] == 'Hint: the red %d' % wd)
play(h, [soft(4), soft(3)])                # Undo the wrong digit, then Hint: an only-digit square on an Easy board
e = E.Engine([c for c in EASY]); kind, which, need, fewest = e.best()
check('D4 Hint on an Easy board: the only digit of the tightest square', h.globals_['suHintKind'] == 1.0 and
      h.globals_['suHintK'] == which and h.globals_['suHintD'] == EASY_S[which - 1] and G(h, 'suMsg')[0].startswith('Hint: only a '))
play(h, [soft(3)])
check('D4 Hint again fills it in', G(h, 'suUsr')[which - 1] == EASY_S[which - 1] and G(h, 'suMsg')[0].startswith('The '))
# hidden singles in a row, a column and a box, found by searching positions where the engine's
# tightest spot is kind 2 with one place
def find_hidden(unit_kind):
    """A position (clues and right digits) whose tightest spot is the only square for a digit in a row (0), a
    column (1) or a box (2): walked along the solver's own path through each base puzzle, as given and
    turned over on its diagonal (a row's single then becomes a column's)."""
    for lv in LEVELS:
        for b in BASE[lv]:
            for turn in (0, 1):
                p, s = digits(b['p']), digits(b['s'])
                if turn:
                    p = [p[(k % 9) * 9 + k // 9] for k in range(81)]; s = [s[(k % 9) * 9 + k // 9] for k in range(81)]
                log = []; E.Engine(p).solve(1, log)
                q = list(p)
                for how, k, d in log:
                    if how == 'undo' or s[k - 1] != d: continue
                    kd, w, n, f = E.Engine(q).best()
                    if kd == 2 and f == 1 and ((unit_kind == 0 and w <= 9) or (unit_kind == 1 and 9 < w <= 18) or (unit_kind == 2 and w > 18)):
                        return p, s, list(q)
                    q[k - 1] = d
    return None
for uk, label in ((0, 'row'), (1, 'column'), (2, 'box')):
    found = find_hidden(uk)
    if not found:
        check('D4 a hidden single in a %s' % label, False, 'no position found'); continue
    p, s, q = found
    h = harness(); setgame(h, p, s)
    h.globals_['suUsr'] = fl([q[i] if p[i] == 0 else 0 for i in range(81)])
    play(h, [soft(3)])
    e = E.Engine(q); kd, w, n, f = e.best()
    msg = G(h, 'suMsg')
    check('D4 a hidden single in a %s: the square, the digit, the words' % label,
          h.globals_['suHintKind'] == 2.0 and h.globals_['suHintU'] == w and h.globals_['suHintD'] == n
          and s[int(h.globals_['suHintK']) - 1] == n and msg[-2:] == ['Press Hint again', 'to fill it in.'], msg[:2])
# fewest choices: a position with no single (Expert base, before any move, if its tightest spot has 2+)
b = BASE['Expert'][0]
p, s = digits(b['p']), digits(b['s'])
log = []; E.Engine(p).solve(1, log)
q = list(p)
for how, k, d in log:                      # the forced moves before the first guess
    if how == 'guess': break
    q[k - 1] = d
h = harness(); setgame(h, p, s)
h.globals_['suUsr'] = fl([q[i] if p[i] == 0 else 0 for i in range(81)])
play(h, [soft(3)])
e = E.Engine(q); fewest = min(e.C[k] for k in range(1, 82) if e.V[k] == 0)
check('D4 no single: Hint shows the square with the fewest choices', h.globals_['suHintKind'] == 1.0 and
      G(h, 'suMsg')[0] == 'No square can be' and G(h, 'suMsg')[4] == 'has just %d' % fewest)
play(h, [soft(3)])
k = int(h.globals_['suSel'])
check('D4 ...and Hint again fills in its answer', G(h, 'suUsr')[k - 1] == s[k - 1])
# a moved selection ends the hint
h = harness(); setgame(h, EASY, EASY_S)
play(h, [soft(3), ('k', 8)])
check('D4 moving the square ends the hint', h.globals_['suHintArm'] == 0.0)

# D5 Check
h = harness(); setgame(h, EASY, EASY_S)
play(h, [soft(5)])
check('D5 Check with no digits placed', G(h, 'suMsg')[0] == 'Check: you have')
play(h, [tapsq(empties[0]), tappad(EASY_S[empties[0] - 1]), soft(5)])
check('D5 Check, all right', G(h, 'suMsg')[0] == 'Check: all of' and h.globals_['suWrongOn'] == 0.0)
w1 = EASY_S[empties[1] - 1] % 9 + 1
play(h, [tapsq(empties[1]), tappad(w1), soft(5)])
check('D5 Check, 1 wrong', G(h, 'suMsg')[0] == 'Check: 1 of your' and h.globals_['suWrongOn'] == 1.0)
w2 = EASY_S[empties[2] - 1] % 9 + 1
play(h, [tapsq(empties[2]), tappad(w2), soft(5)])
check('D5 Check, 2 wrong', G(h, 'suMsg')[0] == 'Check: 2 of your' and h.globals_['suChecks'] == 4.0)
# a clue square, and no square chosen
play(h, [tapsq([k for k in range(1, 82) if EASY[k - 1]][0]), tappad(5)])
check('D5 a clue cannot be changed', G(h, 'suMsg')[0] == 'That black digit')
h.globals_['suSel'] = 0.0
play(h, [tappad(5)])
check('D5 a digit with no square chosen', G(h, 'suMsg')[0] == 'Tap a square')

# D6 Watch: the bar chart's counts are the engine's
for lv in ('Easy', 'Expert'):
    p, s = digits(BASE[lv][1]['p']), digits(BASE[lv][1]['s'])
    h = harness(); setgame(h, p, s)
    play(h, [soft(6), soft(1), ('c', 1)])       # More, Watch, "Watch (ends this game)"
    n, first, st = E.Engine(p).solve(1)
    g = h.globals_
    counts = tuple(int(g[x]) for x in ('suSN', 'suSH', 'suSG', 'suSU', 'suSS'))
    check('D6 Watch %s: the counts = the engine\'s, the answer in, the chart shown' % lv,
          counts == (st['naked'], st['hidden'], st['guesses'], st['undos'], st['steps']) and g['suPanel'] == 1.0
          and G(h, 'suUsr') == [0 if c else v for c, v in zip(p, s)] and g['suGame'] == 2.0, counts)
txts = [t.text for t in SCREENS[-1].items if t.__class__.__name__ == 'Text']
check('D6 the chart\'s labels', any(x.startswith('Only digit ') for x in txts) and any(x.startswith('All steps ') for x in txts))
h = harness(); setgame(h, EASY, EASY_S)
play(h, [soft(6), soft(1), ('c', 2)])           # "Keep playing"
check('D6 Watch, Keep playing: nothing changes', h.globals_['suGame'] == 1.0 and h.globals_['suPanel'] == 0.0)
play(h, [soft(1), ('c', 0)])                     # Cancel (page 2 stays)
check('D6 Watch, Cancel: nothing changes', h.globals_['suGame'] == 1.0)
# Watch skipped by a key, and stopped with Esc (Easter Monster: long enough to stop)
p = digits(HARD['Easter Monster'])
h = harness(); setgame(h, p, E.Engine(p).solve(1)[1])
h.globals_['suPage'] = 2.0
h.tap(SK[0], 230); h.choose(1); h.press(30, anytime=True); h.press(4, anytime=True)
h.execute('suPlay()'); keep(h)
g = h.globals_
check('D6 Watch: a key stops the painting, Esc then stops the search', g['suAbort'] == 1.0 and g['suGame'] == 2.0
      and G(h, 'suMsg')[0] == 'Watch stopped' and G(h, 'suUsr') == [0 if c else v for c, v in zip(p, G(h, 'suSol'))], int(g['suSS']))

# D7 Solve and Restart
h = harness(); setgame(h, EASY, EASY_S)
play(h, [tapsq(empties[0]), tappad(EASY_S[empties[0] - 1]), soft(6), soft(2), ('c', 2)])
check('D7 Solve, Keep playing: nothing changes', h.globals_['suGame'] == 1.0)
play(h, [soft(2), ('c', 1)])
check('D7 Solve: the answer is filled in', h.globals_['suGame'] == 2.0 and G(h, 'suUsr') == [0 if c else v for c, v in zip(EASY, EASY_S)])
h = harness(); setgame(h, EASY, EASY_S)
play(h, [tapsq(empties[0]), tappad(EASY_S[empties[0] - 1]), soft(6), soft(4), ('c', 2)])
check('D7 Restart, Keep playing: the digit stays', G(h, 'suUsr')[empties[0] - 1] == EASY_S[empties[0] - 1])
play(h, [soft(4), ('c', 0)])
check('D7 Restart, Cancel: the digit stays', G(h, 'suUsr')[empties[0] - 1] == EASY_S[empties[0] - 1])
play(h, [soft(4), ('c', 1)])
check('D7 Restart: the board is back to the clues', G(h, 'suUsr') == [0] * 81 and G(h, 'suMsg')[0] == 'Back to the start')

# D8 typing a puzzle
def type_events(clue):
    ev = []
    for k in range(1, 82):
        ev.append(tappad(clue[k - 1]) if clue[k - 1] else ('t',) + ERASE)
    return ev
h = harness(); setgame(h, EASY, EASY_S)
h.globals_['suUL'] = 0.0
play(h, [soft(6), soft(3)])                      # More, Type (no digits yet: no question)
check('D8 Type: typing mode, square 1 chosen', h.globals_['suMode'] == 2.0 and h.globals_['suSel'] == 1.0)
SAMPLE_D = digits(SAMPLE)
play(h, type_events(SAMPLE_D))
check('D8 typed by taps with auto-advance and Erase: the clues', G(h, 'suClue') == SAMPLE_D, int(h.globals_['suSel']))
h.globals_['M9'] = R.interp.Matrix([[0.0] * 9 for _ in range(9)]) if hasattr(R, 'interp') else None
play(h, [soft(1)])                               # Play
g = h.globals_
M9 = g.get('M9')
check('D8 Play: one answer, the game starts, the puzzle kept in M9', g['suMode'] == 1.0 and g['suGame'] == 1.0 and g['suLevel'] == 5.0
      and G(h, 'suSol') == digits(SAMPLE_ANS) and [int(v) for row in M9.rows for v in row] == SAMPLE_D and G(h, 'suMsg')[0] == 'Your puzzle has')
# refusals: too few, clash, two answers, no answer
def typed(clue):
    h = harness(); g = h.globals_
    g['suClue'] = fl(clue); h.execute('suStartTyping0()')
    g['M9'] = R.interp.Matrix([[0.0] * 9 for _ in range(9)])
    return h
few = digits(SAMPLE); few = [d if i < 40 and d else 0 for i, d in enumerate(few)]
few = [d for d in few]; nfew = sum(1 for d in few if d)
h = typed([d if i < 25 else 0 for i, d in enumerate(digits(SAMPLE))])
nc = sum(1 for d in G(h, 'suClue') if d)
play(h, [soft(1)])
check('D8 Play with %d clues: refused with a sentence' % nc, h.msgboxes and h.msgboxes[-1].text.startswith('Only %d clues are in.' % nc) and h.globals_['suMode'] == 2.0)
MSGS = [m.text for m in h.msgboxes]
h = typed(clash); play(h, [soft(1)])
MSGS += [m.text for m in h.msgboxes]
check('D8 clashing clues: refused, the square chosen', h.msgboxes and h.msgboxes[-1].text.startswith('The 5 in row 1, column 2 repeats') and h.globals_['suSel'] == 2.0)
h = typed(two); play(h, [soft(1)])
MSGS += [m.text for m in h.msgboxes]
check('D8 two answers: refused', h.msgboxes and 'more than one answer' in h.msgboxes[-1].text and h.globals_['suMode'] == 2.0)
h = typed(nosol); play(h, [soft(1)])
MSGS += [m.text for m in h.msgboxes]
check('D8 no answer: refused', h.msgboxes and 'have no answer' in h.msgboxes[-1].text and h.globals_['suMode'] == 2.0)
# Esc during the check. LATE has one answer, found at step 218, but the search that shows there is no
# second one takes 2,558 steps (found by a seeded search over shuffled hard puzzles, 26 Nov 2026); the
# Esc reaches the check at step 250 or 500, after the first answer. Easter Monster's first answer
# comes at step 3,823, so its Esc comes before any answer.
LATE = digits('003004000200900000060010070009300000070050008400002000000060010080000065000000907')
n1, f1, s1 = E.Engine(LATE).solve(1); n2, f2, s2 = E.Engine(LATE).solve(2)
assert n2 == 1 and s1['steps'] < 250 and s2['steps'] > 500
for puzzle, ans, label in ((LATE, 2, 'an answer found, then Back to the clues'), (LATE, 1, 'an answer found, then Play (not checked)'),
                           (digits(HARD['Easter Monster']), None, 'no answer found yet')):
    h = typed(puzzle)
    h.tap(SK[0], 230); h.press(4, anytime=True)
    if ans: h.choose(ans)
    h.execute('suPlay()'); keep(h)
    g = h.globals_
    asked = any(c.title == 'Play without the check?' for c in h.chooses)
    if ans == 1:
        check('D8 Esc during the check: %s' % label, asked and g['suMode'] == 1.0 and G(h, 'suMsg')[0] == 'Not checked for a'
              and G(h, 'suSol') == f1)
    else:
        check('D8 Esc during the check: %s' % label, asked == (ans is not None) and g['suMode'] == 2.0
              and G(h, 'suMsg')[0] == 'The check was')
# Clear (with its question), Undo while typing, Back
h = typed(SAMPLE_D)
play(h, [soft(2), ('c', 2)])
check('D8 Clear, Keep the clues', G(h, 'suClue') == SAMPLE_D)
play(h, [soft(2), ('c', 1)])
check('D8 Clear the board', G(h, 'suClue') == [0] * 81)
play(h, [tapsq(5), tappad(7), soft(4)])
check('D8 Undo while typing', G(h, 'suClue') == [0] * 81 and h.globals_['suSel'] == 5.0)
play(h, [tapsq(5), tappad(7), soft(6), ('c', 0)])
check('D8 Back, then Cancel: still typing', h.globals_['suMode'] == 2.0)
play(h, [soft(6), ('c', 1), ('c', 2)])           # Back, Easy, "No, keep this one"
check('D8 Back, Easy, No: still typing', h.globals_['suMode'] == 2.0 and G(h, 'suClue')[4] == 7)
play(h, [soft(6), ('c', 1), ('c', 1)])           # Back, Easy, Yes
check('D8 Back, Easy, Yes: a new Easy game', h.globals_['suMode'] == 1.0 and h.globals_['suLevel'] == 1.0)

# D9 M9
def m9(rows):
    return R.interp.Matrix([[float(v) for v in r] for r in rows])
h = harness(); h.globals_['M9'] = m9([SAMPLE_D[r * 9:r * 9 + 9] for r in range(9)])
h.choose(6, 0); h.execute('Sudoku()'); keep(h)
check('D9 Use the puzzle in M9: the game starts', h.globals_['suMode'] == 1.0 and h.globals_['suLevel'] == 5.0 and G(h, 'suClue') == SAMPLE_D)
for label, rows, start in (('8 x 9', [SAMPLE_D[r * 9:r * 9 + 9] for r in range(8)], 'M9 must hold 9 rows'),
                           ('2.5', [[2.5] + SAMPLE_D[1:9]] + [SAMPLE_D[r * 9:r * 9 + 9] for r in range(1, 9)], 'Row 1, column 1 of M9'),
                           ('10', [[10] + SAMPLE_D[1:9]] + [SAMPLE_D[r * 9:r * 9 + 9] for r in range(1, 9)], 'Row 1, column 1 of M9')):
    h = harness(); h.globals_['M9'] = m9(rows)
    h.choose(6, 0); h.execute('Sudoku()'); keep(h)
    MSGS += [m.text for m in h.msgboxes]
    check('D9 M9 %s: refused with a sentence' % label, h.msgboxes and h.msgboxes[0].text.startswith(start), h.msgboxes[0].text[:40] if h.msgboxes else '')

# D10 the first menu: Cancel, Help, Esc from the board and Continue, the returned lines
h = harness()
h.choose(0); ret = h.execute('Sudoku()'); RETURNS.append(ret)
check('D10 Cancel at the first menu', ret == 'Sudoku: thanks for playing.', ret)
h = harness(seed=5)
h.choose(1)                                      # Easy
h.tap(*sq(1)); h.press(4)                        # a tap, then Esc: back to the first menu
h.choose(0)                                      # Cancel: leave
ret = h.execute('Sudoku()'); keep(h); RETURNS.append(ret)
check('D10 Esc keeps the game', ret.startswith('Sudoku: your game is kept') and h.globals_['suGame'] == 1.0, ret)
tel = h.globals_['suTEl']
h.choose(1); h.press(4); h.choose(0)             # Continue, Esc, Cancel
ret = h.execute('Sudoku()'); keep(h)
items = h.chooses[-2].items if len(h.chooses) >= 2 else []
check('D10 Continue is offered first, with the level and the time', items and items[0].startswith('Continue (Easy, '), items[:1])
check('D10 the clock goes on after Continue', h.globals_['suTEl'] >= tel)
h = harness(); h.choose(5); h.press(4); h.choose(0)
ret = h.execute('Sudoku()'); keep(h); RETURNS.append(ret)
check('D10 leaving while typing', ret.startswith('Sudoku: the clues you typed are kept'), ret)
h.choose(1); h.press(4); h.choose(0)
h.execute('Sudoku()'); keep(h)
check('D10 Continue typing is offered', h.chooses[-2].items[0].startswith('Continue typing ('), h.chooses[-2].items[0])

# D11 Help: every page, back, Esc
h = harness()
nh = len(ppl_list('suHelpH'))
for i in range(nh + 2):
    h.press(8)
h.choose(7); h.choose(0)
h.execute('Sudoku()'); keep(h)
heads = [t.text for s in SCREENS for t in s.items if t.__class__.__name__ == 'Text' and t.y == 3 and t.font == 2.0]
check('D11 Help: every page shown in turn', all(x in heads for x in ppl_list('suHelpH')), '%d pages' % nh)
h = harness(); setgame(h, EASY, EASY_S)
h.globals_['suPage'] = 2.0
play(h, [soft(5), ('k', 8), ('k', 7), ('k', 4)])
check('D11 Help from the board: Next, Left back, Esc', h.globals_['suMode'] == 1.0)

# D12 the Enter menu: every item, and Cancel
h = harness(); setgame(h, EASY, EASY_S)
play(h, [('k', 30), ('c', 0)])
check('D12 the Enter menu, Cancel', h.globals_['suGame'] == 1.0)
play(h, [('k', 30), ('c', 4)])
check('D12 Notes on or off', h.globals_['suNoteOn'] == 1.0)
play(h, [('k', 30), ('c', 1), ('k', 30), ('c', 2), ('k', 30), ('c', 3)])
check('D12 Hint, Check my digits, Undo', h.globals_['suHints'] == 1.0 and h.globals_['suChecks'] == 1.0)
play(h, [('k', 30), ('c', 12), ('k', 4)])
check('D12 My games (beta 2a): the page, and Esc back to the board', h.globals_['suGame'] == 1.0
      and any(t.text == 'My games: minutes against clues' for s in h.screens + SCREENS[-6:] for t in s.items if t.__class__.__name__ == 'Text'))
play(h, [('k', 30), ('c', 13), ('k', 4)])
check('D12 Help', True)
play(h, [('k', 30), ('c', 10), ('c', 0)])
check('D12 New puzzle, Cancel', h.globals_['suGame'] == 1.0)
r = play(h, [('k', 30), ('c', 14)])
check('D12 Exit Sudoku: suPlay answers 2', r == 2.0, r)
h = typed(SAMPLE_D)
r = play(h, [('k', 30), ('c', 6)])
check('D12 typing menu: Exit Sudoku', r == 2.0)
h = typed(SAMPLE_D)
play(h, [('k', 30), ('c', 0), ('k', 30), ('c', 4), ('k', 4)])
check('D12 typing menu: Cancel, Help', h.globals_['suMode'] == 2.0)

# D13 keys: arrows at the edges, digits, 0 and Del, WAIT(-1) giving up
h = harness(); setgame(h, EASY, EASY_S)
h.globals_['suSel'] = 1.0
play(h, [('k', 2), ('k', 7)])
check('D13 Up and Left at square 1 stay', h.globals_['suSel'] == 1.0)
h.globals_['suSel'] = 81.0
play(h, [('k', 12), ('k', 8)])
check('D13 Down and Right at square 81 stay', h.globals_['suSel'] == 81.0)
h.globals_['suSel'] = 0.0
play(h, [('k', 12)])
check('D13 an arrow with no square chosen picks the middle', h.globals_['suSel'] == 41.0)
k = empties[5]
h.globals_['suSel'] = float(k)
keymap = {1: 42, 2: 43, 3: 44, 4: 37, 5: 38, 6: 39, 7: 32, 8: 33, 9: 34}
play(h, [('k', keymap[EASY_S[k - 1]])])
check('D13 a digit key places its digit', G(h, 'suUsr')[k - 1] == EASY_S[k - 1])
play(h, [('k', 47)])
check('D13 the 0 key erases', G(h, 'suUsr')[k - 1] == 0)
play(h, [('k', keymap[EASY_S[k - 1]]), ('k', 19)])
check('D13 Del erases', G(h, 'suUsr')[k - 1] == 0)
h._queue.append(R.Timeout())
before = (G(h, 'suUsr'), h.globals_['suSel'])
play(h, [])
check('D13 WAIT(-1) giving up (-1): a redraw, nothing else', (G(h, 'suUsr'), h.globals_['suSel']) == before)

# D14 the stale-click guard: a soft-key click handed over at once after a dialog is skipped
h = harness(); setgame(h, EASY, EASY_S)
h.instant = {2}                                  # WAIT calls: 1 the click on New, 2 the queued click
play(h, [soft(1), ('c', 0), soft(6)])
check('D14 a click queued behind a dialog is skipped', h.globals_['suPage'] == 1.0)
h = harness(); setgame(h, EASY, EASY_S)
play(h, [soft(1), ('c', 0), soft(6)])
check('D14 the same click 200 ms later is the student\'s', h.globals_['suPage'] == 2.0)

# D15 New puzzle with a game in progress: the question, both answers, Esc
h = harness(); setgame(h, EASY, EASY_S)
play(h, [tapsq(empties[0]), tappad(EASY_S[empties[0] - 1]), soft(1), ('c', 2), ('c', 2)])
check('D15 New, Medium, No: the game stays', h.globals_['suLevel'] == 1.0 and G(h, 'suUsr')[empties[0] - 1] != 0)
play(h, [soft(1), ('c', 2), ('c', 0)])
check('D15 New, Medium, Cancel: the game stays', h.globals_['suLevel'] == 1.0)
play(h, [soft(1), ('c', 2), ('c', 1)])
check('D15 New, Medium, Yes: a Medium game', h.globals_['suLevel'] == 2.0 and G(h, 'suUsr') == [0] * 81)
play(h, [soft(6), soft(3)])                      # Type with no digits yet: no question
check('D15 Type on a fresh game: no question', h.globals_['suMode'] == 2.0)
h = harness(); setgame(h, EASY, EASY_S)
play(h, [tapsq(empties[0]), tappad(EASY_S[empties[0] - 1]), soft(6), soft(3), ('c', 2)])
check('D15 Type, No: the game stays', h.globals_['suMode'] == 1.0)
# Notes button on the panel, and notes refused in a filled square
h = harness(); setgame(h, EASY, EASY_S)
play(h, [('t',) + NOTES])
check('D15 the Notes button turns Notes on', h.globals_['suNoteOn'] == 1.0)
h.globals_['suNoteOn'] = 0.0
play(h, [tapsq(empties[0]), tappad(EASY_S[empties[0] - 1]), ('t',) + NOTES, tappad(3)])
check('D15 a pencil mark in a filled square is refused', G(h, 'suMsg')[0] == 'Pencil marks go')
# a finished game: the pad says so
h = harness(); setgame(h, EASY, EASY_S); h.globals_['suGame'] = 2.0
play(h, [tapsq(empties[0]), tappad(1)])
check('D15 a digit on a finished board', G(h, 'suMsg')[0] == 'This puzzle is')

# ================================================================== D16 (beta 2a) My games and the clock
print('== D16  My games and the clock (beta 2a)')
def texts(screens):
    return [t.text for s in screens for t in s.items if t.__class__.__name__ == 'Text']
def set_log(h, lv, cl, mn, hn=None, ck=None):
    g = h.globals_; n = len(lv)
    g['suGLv'] = fl(lv); g['suGCl'] = fl(cl); g['suGMn'] = [float(x) for x in mn]
    g['suGHn'] = fl(hn if hn is not None else [0] * n); g['suGCk'] = fl(ck if ck is not None else [0] * n)
def finish_events():
    ev = []
    for k in empties:
        ev += [tapsq(k), tappad(EASY_S[k - 1])]
    return ev + [('k', 30)]                  # a key leaves the fireworks page
NCLUE = sum(1 for c in EASY if c)
# a finished game
h = harness(); setgame(h, EASY, EASY_S); h.globals_['suHints'] = 0.0
play(h, finish_events())
g = h.globals_
mins = g['suGMn'][0] if g['suGMn'] else None
check('D16 a finished game is kept: level, clues, minutes, Hints, Checks', G(h, 'suGLv') == [1] and G(h, 'suGCl') == [NCLUE]
      and mins is not None and abs(mins - g['suTEl'] / 60000.0) <= 0.005 and abs(mins * 100 - round(mins * 100)) < 1e-9
      and G(h, 'suGHn') == [0] and G(h, 'suGCk') == [0] and g['suGNew'] == 1.0, (G(h, 'suGLv'), G(h, 'suGCl'), mins, g['suTEl']))
check('D16 the fireworks page says where the game went', 'Kept as game 1 of My games.' in texts(SCREENS[-40:]))
# a game with a Hint and a Check
h = harness(); setgame(h, EASY, EASY_S)
play(h, [soft(3), soft(5)] + finish_events())
check('D16 Hints and Checks are counted into the game', G(h, 'suGHn') == [1] and G(h, 'suGCk') == [1], (G(h, 'suGHn'), G(h, 'suGCk')))
# Solve and Watch end a game without keeping it
h = harness(); setgame(h, EASY, EASY_S)
play(h, [soft(6), soft(2), ('c', 1)])
check('D16 Solve: the game is not kept', G(h, 'suGLv') == [] and h.globals_['suGame'] == 2.0)
h = harness(); setgame(h, EASY, EASY_S)
play(h, [soft(6), soft(1), ('c', 1)])          # Watch, then the harness's idle Esc
check('D16 Watch: the game is not kept', G(h, 'suGLv') == [] and h.globals_['suWatched'] == 1.0)
# a typed puzzle, finished: level 5
h = typed(SAMPLE_D); play(h, [soft(1)])
g = h.globals_; sol = G(h, 'suSol')
ev = []
for k in range(1, 82):
    if SAMPLE_D[k - 1] == 0: ev += [tapsq(k), tappad(sol[k - 1])]
play(h, ev + [('k', 30)])
check('D16 a typed puzzle, finished: level 5 (typed)', G(h, 'suGLv') == [5] and G(h, 'suGCl') == [sum(1 for d in SAMPLE_D if d)], G(h, 'suGLv'))
# My games full: the game is not kept, and the page says so
h = harness(); setgame(h, EASY, EASY_S)
set_log(h, [1] * 200, [38] * 200, [5.0] * 200)
play(h, finish_events())
check('D16 My games full (200): the game is not kept, and the page says so', len(h.globals_['suGLv']) == 200 and h.globals_['suGNew'] == 0.0
      and 'My games is full: 200 games.' in texts(SCREENS[-40:]))
# the clock: half a minute in each menu does not count
h = harness(); setgame(h, EASY, EASY_S)
h.dialog_ms = 30000.0
t0 = h.globals_['suTEl']
play(h, [('k', 30), ('c', 0), ('k', 30), ('c', 4), ('k', 4)])      # Enter, Cancel; Enter, Notes; Esc
inc = h.globals_['suTEl'] - t0
check('D16 the clock leaves out the time spent in two menus (30 s each)', 0 < inc < 2000, inc)
# the clock: one wait of ten minutes (the calculator was off) counts for two
h = harness(); setgame(h, EASY, EASY_S)
h.extra = {2: 600000.0}
t0 = h.globals_['suTEl']
play(h, [tapsq(empties[0]), ('k', 4)])
inc = h.globals_['suTEl'] - t0
check('D16 one wait counts for two minutes at most', 120000.0 <= inc < 121000.0, inc)
# the page with no games, by the first menu; Back and Esc; Help by soft key and by key
h = harness()
h.choose(8); h.tap(SK[5], 230); h.choose(0)                 # My games, Back, Cancel
ret = h.execute('Sudoku()'); keep(h)
items = h.chooses[0].items
check('D16 the first menu ends with My games (none yet), and Back returns to it', items[-1] == 'My games (none yet)'
      and len(h.chooses) == 2 and ret == 'Sudoku: thanks for playing.', items[-1])
check('D16 no games: the page says so', 'No games yet.' in texts(h.screens + SCREENS[-4:]))
h = harness()
h.tap(SK[4], 230); h.press(4); h.press(3); h.press(4); h.press(4)   # Help (soft), Esc; Help (key), Esc; Esc
h.execute('suGames()'); keep(h)
heads = [t.text for s in SCREENS[-12:] for t in s.items if t.__class__.__name__ == 'Text' and t.y == 3 and t.font == 2.0]
check('D16 Help from the page opens at the page "My games", by soft key and by key', heads.count('My games') == 2, heads)
# thirteen games: the plot against Python
LV = [1, 3, 4, 2, 4, 1, 2, 4, 4, 2, 3, 4, 5]
CL = [38, 27, 26, 30, 25, 37, 29, 26, 25, 30, 28, 26, 31]
MN = [11.12, 18.4, 21.75, 14.5, 23.0, 10.95, 13.33, 20.2, 22.9, 15.05, 17.8, 26.4, 14.5]
HN = [0, 1, 2, 0, 3, 0, 1, 2, 4, 0, 1, 2, 0]; CK = [0, 0, 1, 1, 2, 0, 0, 1, 1, 0, 0, 3, 1]
h = harness(); set_log(h, LV, CL, MN, HN, CK)
h.press(4); h.execute('suGames()')
scr = h.screens[-1]; keep(h)
n = len(LV); mx = sum(CL) / n; my = sum(MN) / n
qx = sum((x - mx) ** 2 for x in CL); qy = sum((y - my) ** 2 for y in MN); qxy = sum((x - mx) * (y - my) for x, y in zip(CL, MN))
r = qxy / (qx * qy) ** 0.5; b = qxy / qx; a = my - b * mx
tx = [t.text for t in scr.items if t.__class__.__name__ == 'Text']
check('D16 13 games: n and r as Python computes them', ('n = 13      r = %.2f' % r) in tx, [t for t in tx if t.startswith('n =')])
# the axes as the program draws them: clues 24 to 39, minutes 0 to a round number
import math
def nice(rg):
    e = math.floor(math.log10(rg / 4)); f = (rg / 4) / 10 ** e
    return (1 if f <= 1 else 2 if f <= 2 else 5 if f <= 5 else 10) * 10 ** e
x0, x1 = min(CL) - 1, max(CL) + 1
ym = max(1, max(MN)); st = nice(ym * 1.05); top = st * math.ceil(ym * 1.05 / st)
def px(x): return int(40 + (x - x0) * 206 / (x1 - x0) + 0.5)
def py(y): return int(186 - y * 144 / top + 0.5)
xa, ya, xb, yb = x0, a + b * x0, x1, a + b * x1
if ya < 0: xa, ya = -a / b, 0
if ya > top: xa, ya = (top - a) / b, top
if yb < 0: xb, yb = -a / b, 0
if yb > top: xb, yb = (top - a) / b, top
gray = float((90 << 16) | (90 << 8) | 90)
lines = [[v for v in s.args if isinstance(v, float)] for s in scr.items if s.__class__.__name__ == 'Shape' and s.cmd == 'LINE_P']
ls = [l for l in lines if len(l) >= 5 and l[4] == gray]
want = [px(xa), py(ya), px(xb), py(yb)]
check('D16 the least-squares line, cut at the plot\'s top or bottom, ends where Python puts it', len(ls) == 1 and all(abs(p - q) <= 1 for p, q in zip(ls[0][:4], want)),
      (ls[0][:4] if ls else None, want))
cols = {1: (0, 140, 60), 2: (30, 144, 255), 3: (255, 69, 0), 4: (200, 0, 200), 5: (90, 90, 90)}
def c(rgb): return float((rgb[0] << 16) | (rgb[1] << 8) | rgb[2])
rects = [[v for v in s.args if isinstance(v, float)] for s in scr.items if s.__class__.__name__ == 'Shape' and s.cmd == 'RECT_P']
dots = [rt for rt in rects if len(rt) >= 6 and rt[2] - rt[0] == 6 and rt[3] - rt[1] == 6 and rt[0] != 252]   # not the legend's squares
want_dots = sorted((px(x), py(y), c(cols[l])) for x, y, l in zip(CL, MN, LV))
got_dots = sorted((int(rt[0] + 3), int(rt[1] + 3), rt[5]) for rt in dots)
check('D16 13 dots, each at its game and in its level\'s color', got_dots == want_dots, (len(got_dots), got_dots[:2], want_dots[:2]))
def med(v):
    v = sorted(v); k = len(v)
    return v[k // 2] if k % 2 else (v[k // 2 - 1] + v[k // 2]) / 2
names = ['Easy', 'Medium', 'Hard', 'Expert', 'Typed']
from decimal import Decimal, ROUND_HALF_UP
def r1(x): return str(Decimal(repr(x)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
want_leg = ['%s %d' % (names[k - 1], LV.count(k)) for k in range(1, 6)]
want_med = ['%s %s' % (names[k - 1], r1(med([m for m, l in zip(MN, LV) if l == k]))) for k in range(1, 6) if k in LV]
check('D16 the counts of each level', all(w in tx for w in want_leg), [w for w in want_leg if w not in tx])
check('D16 the median minutes of each level', all(w in tx for w in want_med), [w for w in want_med if w not in tx])
# one, two and three games, and four games with the same clues
for k, wantx in ((1, 'n = 1; the line and r need 3 games'), (2, 'n = 2; the line and r need 3 games')):
    h = harness(); set_log(h, LV[:k], CL[:k], MN[:k]); h.press(4); h.execute('suGames()')
    check('D16 %d game%s: no line, and the page says why' % (k, '' if k == 1 else 's'), wantx in texts(h.screens[-1:]), texts(h.screens[-1:])[:4]); keep(h)
h = harness(); set_log(h, [1] * 4, [38] * 4, [4.0, 5.5, 6.0, 9.25]); h.press(4); h.execute('suGames()')
check('D16 four games with the same clues: no line', 'n = 4, all with 38 clues: no line' in texts(h.screens[-1:])); keep(h)
h = harness(); set_log(h, [1, 2, 4], [38, 30, 26], [5.0, 5.0, 5.0]); h.press(4); h.execute('suGames()')
check('D16 three games, every time the same: a flat line and no r', 'n = 3; every time is the same' in texts(h.screens[-1:])); keep(h)
# 2Var: the columns empty -- no question, the games go in
h = harness(); set_log(h, LV, CL, MN, HN, CK)
for col in ('C1', 'C2', 'C3', 'C4', 'C5'): h.globals_[col] = []
h.tap(SK[0], 230); h.press(30); h.press(4)
h.execute('suGames()'); keep(h)
g = h.globals_
check('D16 2Var, the columns empty: no question, and C1 to C5 hold the games', len(h.chooses) == 0 and G(h, 'C1') == CL
      and g['C2'] == [float(x) for x in MN] and G(h, 'C3') == LV and G(h, 'C4') == HN and G(h, 'C5') == CK)
check('D16 2Var: the page after the copy says what went where', '13 games are now in C1 to C5.' in texts(SCREENS[-6:]))
# 2Var: the columns hold data -- No, Cancel, Yes
for ans, label in ((2, 'No'), (0, 'Cancel')):
    h = harness(); set_log(h, LV, CL, MN, HN, CK)
    h.globals_['C1'] = [7.0, 8.0]
    for col in ('C2', 'C3', 'C4', 'C5'): h.globals_[col] = []
    h.tap(SK[0], 230); h.choose(ans); h.press(4)
    h.execute('suGames()'); keep(h)
    check('D16 2Var over data, %s: the question, and C1 is kept' % label, h.chooses and h.chooses[-1].title == 'Replace C1 to C5?'
          and G(h, 'C1') == [7, 8])
h = harness(); set_log(h, LV, CL, MN, HN, CK)
h.globals_['C1'] = [7.0, 8.0]
for col in ('C2', 'C3', 'C4', 'C5'): h.globals_[col] = []
h.tap(SK[0], 230); h.choose(1); h.press(30); h.press(4)
h.execute('suGames()'); keep(h)
check('D16 2Var over data, Yes: the games replace the columns', G(h, 'C1') == CL and G(h, 'C3') == LV)
h = harness(); set_log(h, LV[:1], CL[:1], MN[:1])
for col in ('C1', 'C2', 'C3', 'C4', 'C5'): h.globals_[col] = []
h.tap(SK[0], 230); h.press(30); h.press(4)
h.execute('suGames()'); keep(h)
check('D16 2Var with one game: "1 game is now in C1 to C5."', '1 game is now in C1 to C5.' in texts(SCREENS[-6:]))
# Clear: No, Cancel, Yes
for ans, label in ((2, 'No'), (0, 'Cancel')):
    h = harness(); set_log(h, LV, CL, MN)
    h.tap(SK[1], 230); h.choose(ans); h.press(4)
    h.execute('suGames()'); keep(h)
    check('D16 Clear, %s: the games are kept' % label, len(h.globals_['suGLv']) == 13 and h.chooses[-1].title == 'Clear My games?'
          and h.chooses[-1].items[0] == 'Yes, clear all 13 games')
h = harness(); set_log(h, LV, CL, MN)
h.tap(SK[1], 230); h.choose(1); h.press(4)
h.execute('suGames()'); keep(h)
check('D16 Clear, Yes: My games is empty, and the page says so', G(h, 'suGLv') == [] and G(h, 'suGMn') == [] and 'No games yet.' in texts(SCREENS[-3:]))
# the stale-click guard: a 2Var click handed over at once after the Clear question is that question's own tap
h = harness(); set_log(h, LV, CL, MN)
for col in ('C1', 'C2', 'C3', 'C4', 'C5'): h.globals_[col] = []
h.instant = {2}
h.tap(SK[1], 230); h.choose(2); h.tap(SK[0], 230); h.press(4)
h.execute('suGames()'); keep(h)
check('D16 the stale-click guard on My games: a click handed over at once after a dialog is skipped', G(h, 'C1') == [])
# My games from the first menu with a game kept: the 9th item, and the count
h = harness(seed=5)
set_log(h, LV[:2], CL[:2], MN[:2])
h.choose(1); h.press(4)                          # Easy, Esc: the game is kept
h.choose(9); h.press(4); h.choose(0)             # My games, Esc, Cancel
h.execute('Sudoku()'); keep(h)
it2 = h.chooses[1].items
check('D16 with a game kept, My games is the 9th item, with its count', len(it2) == 9 and it2[0].startswith('Continue (') and it2[8] == 'My games (2 so far)', it2[-1:])
# the line returned after a logged game
h = harness(); setgame(h, EASY, EASY_S)
h.choose(0)
g = h.globals_
g['suUsr'] = fl([0 if c else s for c, s in zip(EASY, EASY_S)]); g['suGame'] = 2.0; g['suTEl'] = 754000.0; g['suGNew'] = 7.0
ret = h.execute('Sudoku()')
check('D16 the line returned after a logged game', ret == 'Sudoku: solved in 12:34, game 7 of My games. The answer is in SU_SOLVED.', ret)
RETURNS.append(ret)

# ================================================================== E
print('== E  the text')
T.RECORDS.clear()
digests = [T.digest_screen(s) for s in SCREENS]
firm = collections.Counter(); marg = collections.Counter(); examples = []
seen = set()
for d in digests:
    key = json.dumps(d['items'], sort_keys=True)[:4000]
    if key in seen: continue
    seen.add(key)
    coll, strad, over, ghosts = T.analyse_screen(d)
    for c in coll:
        if T.severity(c[2], c[3], c[6], c[7]) == 'overlap':
            (firm if c[8] else marg)['overlap'] += 1
            if c[8] and len(examples) < 4: examples.append(('overlap', c[:8], d['func']))
    for x in strad:
        (firm if x[5] else marg)['straddle'] += 1
        if x[5] and len(examples) < 8: examples.append(('straddle', x, d['func']))
    for x in over:
        (firm if x[4] else marg)['overrun'] += 1
        if x[4] and len(examples) < 8: examples.append(('overrun', x, d['func']))
check('E1 text_overlap: no firm overlap, straddle or overrun', not firm, '%d distinct screens; firm %s; marginal %s %s'
      % (len(seen), dict(firm), dict(marg), examples[:4]))
# every message line, from the source (literals) and as shown (part D)
lits = []
for mm in re.finditer(r'suMsgSet\(\{(.*?)\}, ', SRC):
    for s in re.findall(r'"([^"]*)"', mm.group(1)):
        lits.append(s)
long_lit = [s for s in lits if len(s) > 17]
shown_long = [s for s in MSGLINES if len(s) > 17]
check('E2 every message line at most 17 characters', not long_lit and not shown_long, (long_lit + shown_long)[:4])
def items_of(lst):                         # the top-level items of a PPL list's text
    out, depth, q, cur = [], 0, False, ''
    for ch in lst:
        if ch == '"': q = not q
        if not q and ch in '([{': depth += 1
        if not q and ch in ')]}': depth -= 1
        if ch == ',' and depth == 0 and not q: out.append(cur); cur = ''
        else: cur += ch
    return out + [cur]
nlines = [len(items_of(mm.group(1))) for mm in re.finditer(r'suMsgSet\(\{(.*?)\}, ', SRC)]
check('E3 every message at most 9 lines', max(nlines) <= 9, max(nlines))
GW = {int(k): v for k, v in json.load(open(WIDTHS)).items()}
def w1(s): return sum(GW.get(ord(c), [9, 11, 12])[0] for c in s)
widest = max(list(MSGLINES) + lits, key=w1)
check('E8 every message line at most 96 px at the measured font-1 widths (x 222 to 318)', w1(widest) <= 96,
      '%d px: %r' % (w1(widest), widest))
# CHOOSE titles and items, from the source
bad = []
for mm in re.finditer(r'CHOOSE\(\w+, "([^"]*)", \{(.*?)\}\);', SRC):
    title, items = mm.group(1), re.findall(r'"([^"]*)"', mm.group(2))
    if len(title) > 31 or any(len(i) > 30 for i in items): bad.append((title, items))
for mm in re.finditer(r'suAsk\("([^"]*)", "([^"]*)", "([^"]*)"\)', SRC):
    if len(mm.group(1)) > 31 or len(mm.group(2)) > 30 or len(mm.group(3)) > 30: bad.append(mm.groups())
lit_items = [c.items for c in []]
check('E4 CHOOSE titles at most 31 characters, items at most 30', not bad, bad[:3])
check('E4 beta 2a: the longest Clear item and My games item fit', len('Yes, clear all 200 games') <= 30 and len('My games (200 so far)') <= 30
      and len('Replace C1 to C5?') <= 31 and len('Clear My games?') <= 31)
cont = 'Continue (Medium, 23:59:59)'
check('E4 the longest Continue item fits', len(cont) <= 30 and len('Continue typing (81 clues)') <= 30)
def wrap30(text):
    out, cur = [], ''
    for w in text.split():
        if len(cur) + len(w) + (1 if cur else 0) <= 30: cur = (cur + ' ' + w) if cur else w
        else: out.append(cur); cur = w
    return out + [cur]
MSGS += re.findall(r'MSGBOX\("([^"]*)"\)', SRC)      # beta 2a: every literal MSGBOX too (2Var's refusal cannot be met in the harness)
worst = max(MSGS, key=lambda m: len(wrap30(m)))
check('E5 every MSGBOX in at most 5 lines of 30 characters', all(len(wrap30(m)) <= 5 for m in MSGS), '%d boxes; longest %d lines' % (len(MSGS), len(wrap30(worst))))
rets = re.findall(r'RETURN "(Sudoku:[^"]*)"', SRC)
longest = max(rets + ['Sudoku: solved in 23:59:59. The answer is in SU_SOLVED.',
                      'Sudoku: solved in 23:59:59, game 200 of My games. The answer is in SU_SOLVED.'], key=len)
check('E6 every returned line at most 100 characters', len(longest) <= 100, '%d: %s' % (len(longest), longest))
# the panel: the pad's small counts and the level line inside their boxes (label_fit's narrow widths)
check('E7 the help pages hold at most 13 lines', all(len(p) <= 13 for p in ppl_list('suHelpT')))

n_fail = sum(1 for _, ok in RESULTS if not ok)
print('\n%d checks, %d PASS, %d FAIL' % (len(RESULTS), len(RESULTS) - n_fail, n_fail))
sys.exit(1 if n_fail else 0)
