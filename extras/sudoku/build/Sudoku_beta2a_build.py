#!/usr/bin/env python3
"""Sudoku_beta2a_build.py -- writes Sudoku_beta2a.txt from Sudoku_beta2a_template.txt (26 Nov 2026).

Everything a table holds is computed here, never typed (Lessons Learned 14, rule 31):
  @UNIT@ @PEER@        the 27 units and every square's 20 peers (su_engine.py)
  @BP@ @BS@            the base puzzles and their answers (base_puzzles.json, made by su_gen.py),
                       each checked again here: one answer, and it is the stored one
  @GLYO@ @GLYS@ @GLYN@ the 3 x 5 pencil-mark digits as strokes (drawn below as text, to be looked at)
  @HELPH@ @HELPT@      the help pages, wrapped at the calculator's measured font-2 glyph widths
                       (verify/round11/glyph_widths_vc.json in hp-prime-statistics)
  @GAMES0@ @SENT2V@    beta 2a: the texts of My games with no games, and of the page after the copy into
                       Statistics 2Var, wrapped the same way
  @MAXGAMES@           beta 2a: how many games My games keeps
  @HELPGAMES@          beta 2a: the number of the help page "My games", counted here
Run:  python3 Sudoku_beta2_build.py [--widths PATH] [--out FOLDER]   (prints what it checked; stops on any failure)
      The widths file is found through $TTL_TOOLS or hp-prime-statistics/tools beside or above this folder.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import su_engine as E

WIDTHS = ''
for d in (os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, '..', 'tools'), os.path.join(HERE, '..', 'hp-prime-statistics', 'tools'),
          '/home/claude/hp-prime-statistics/tools'):
    w = os.path.join(d, '..', 'verify', 'round11', 'glyph_widths_vc.json')
    if d and os.path.exists(w):
        WIDTHS = w; break
if '--widths' in sys.argv:
    WIDTHS = sys.argv[sys.argv.index('--widths') + 1]
GW = {int(k): v for k, v in json.load(open(WIDTHS)).items()}

def width(s, font):                       # font 1, 2 or 3: measured on the Virtual Calculator
    return sum(GW.get(ord(c), [9, 11, 12])[font - 1] for c in s)

def plist(xs):                            # a PPL list of numbers
    return '{' + ', '.join(str(int(x)) for x in xs) + '}'

def pstr(s):
    if '"' in s or '\\' in s:
        raise SystemExit('a string holds a quotation mark or a backslash: %r' % s)
    return '"' + s + '"'

def pslist(xs):                           # a PPL list of strings
    return '{' + ', '.join(pstr(x) for x in xs) + '}'

# ------------------------------------------------------------------ the units and peers
UNIT = E.UNIT[1:]
PEER = E.PEER[1:]
assert len(UNIT) == 243 and len(PEER) == 1620
assert sorted(UNIT) == sorted(list(range(1, 82)) * 3)

# ------------------------------------------------------------------ the base puzzles
LEVELS = ['Easy', 'Medium', 'Hard', 'Expert']
base = json.load(open(os.path.join(HERE, 'base_puzzles.json')))
per = len(base['Easy'])
BP, BS = [], []
for lv in LEVELS:
    assert len(base[lv]) == per, lv
    for b in base[lv]:
        p, s = b['p'], b['s']
        assert len(p) == 81 and len(s) == 81 and set(s) == set('123456789')
        n, first, st = E.solve_str(p, want=2)
        assert n == 1 and ''.join(map(str, first)) == s, (lv, p)
        assert all(p[i] in ('0', s[i]) for i in range(81))
        BP.append(p); BS.append(s)
print('base puzzles: %d (%d a level), each with one answer, the stored one' % (len(BP), per))

# ------------------------------------------------------------------ the pencil-mark digits
STROKES = {
    1: [(1, 0, 1, 4), (0, 1, 0, 1), (0, 4, 2, 4)],
    2: [(0, 0, 2, 0), (2, 0, 2, 2), (0, 2, 2, 2), (0, 2, 0, 4), (0, 4, 2, 4)],
    3: [(0, 0, 2, 0), (0, 2, 2, 2), (0, 4, 2, 4), (2, 0, 2, 4)],
    4: [(0, 0, 0, 2), (0, 2, 2, 2), (2, 0, 2, 4)],
    5: [(0, 0, 2, 0), (0, 0, 0, 2), (0, 2, 2, 2), (2, 2, 2, 4), (0, 4, 2, 4)],
    6: [(0, 0, 2, 0), (0, 0, 0, 4), (0, 2, 2, 2), (2, 2, 2, 4), (0, 4, 2, 4)],
    7: [(0, 0, 2, 0), (2, 0, 2, 4)],
    8: [(0, 0, 2, 0), (0, 2, 2, 2), (0, 4, 2, 4), (0, 0, 0, 4), (2, 0, 2, 4)],
    9: [(0, 0, 2, 0), (0, 0, 0, 2), (0, 2, 2, 2), (2, 0, 2, 4), (0, 4, 2, 4)],
}
GLYO, GLYS, GLYN = [], [], []
art = [[''] * 5 for _ in range(9)]
for d in range(1, 10):
    GLYS.append(len(GLYO) + 1); GLYN.append(len(STROKES[d]))
    px = set()
    for (x1, y1, x2, y2) in STROKES[d]:
        assert x1 == x2 or y1 == y2       # straight strokes only
        GLYO += [x1, y1, x2, y2]
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                px.add((x, y))
    assert all(0 <= x <= 2 and 0 <= y <= 4 for x, y in px)
    for y in range(5):
        art[d - 1][y] = ''.join('#' if (x, y) in px else '.' for x in range(3))
print('pencil-mark digits (%d strokes):' % (len(GLYO) // 4))
for y in range(5):
    print('   ' + '  '.join(art[d][y] for d in range(9)))

# ------------------------------------------------------------------ the help pages
HELP = [
 ("How to play",
  "Fill the grid so that every row, every column and every 3 x 3 box holds each of the digits "
  "1 to 9 exactly once. The black digits are the clues: they are part of the puzzle, and they "
  "cannot be changed.|"
  "Tap a square to choose it, and then tap a digit on the pad at the right (or press a digit "
  "key), and your digit appears in blue. Tapping the same digit again erases it, and so do "
  "Erase, the 0 key and Del. The arrow keys move the chosen square too."),
 ("What the colors mean",
  "The row, column and box of the chosen square are shaded blue, and so is every square that "
  "holds the same digit, which makes it easy to see where that digit can still go. A digit "
  "of yours that repeats one in its row, column or box turns red at once.|"
  "The small number on each key of the pad counts how many of that digit are still to be "
  "placed, and a key turns gray when all nine are in. The thin bar at the top fills as the "
  "grid does, and a row, column or box flashes gold when you finish it."),
 ("Notes, Undo and Check",
  "Pencil marks are small digits that remind you which digits could still go in a square. "
  "Turn Notes on (the soft key, or the Notes button), and the digits you tap become pencil "
  "marks; tap one again to take it away. When you place a digit, that digit's pencil marks "
  "leave its row, column and box. The Enter menu can also fill in every pencil mark at once, "
  "or clear them all.|"
  "Undo takes back your changes one at a time. Check turns your wrong digits red, so that you "
  "can find your mistakes without being shown the answer."),
 ("Hints",
  "Hint finds a square that can be worked out now, and tells you why. Either only one digit "
  "fits the square, because its row, column and box already hold the other eight (a naked "
  "single), or a row, column or box has only one square left where some digit can go (a "
  "hidden single). The square turns dark green, and the row, column or box light green.|"
  "Press Hint again and the digit is filled in for you. A wrong digit of yours is shown "
  "first, and when no square can be worked out in one step, Hint shows the square with the "
  "fewest choices."),
 ("Watch the solver",
  "Watch (after More) shows how a computer solves the puzzle. Before every move it looks for "
  "the tightest spot: a square where only one digit fits (green), or a row, column or box "
  "where a digit fits in only one square (magenta). When no move is forced it guesses "
  "(orange), and when a guess leads to a square where nothing fits, it takes the guess back "
  "(a red flash) and tries the next digit; this is called backtracking.|"
  "A key or a tap skips to the end. The digits keep the color of the step that put them "
  "there, and a bar chart counts the steps of each kind."),
 ("Your own puzzles",
  "Type (after More) lets you enter a puzzle from a newspaper or a book. Tap a square and "
  "then a digit for each clue, and the next square is chosen for you, so a row goes in "
  "quickly; Erase leaves a square blank. Tap Play when every clue is in, and the program "
  "checks that your puzzle has exactly one answer before you start. A very hard puzzle can "
  "take a while, and Esc stops the check.|"
  "The puzzle is then kept in matrix M9. You can also fill M9 yourself, with 0 for each "
  "blank square, and choose Use the puzzle in M9."),
 ("Keeping your game",
  "When you leave with Esc your game is kept, and the first menu offers Continue the next "
  "time you run Sudoku. Solve fills in the whole answer, Restart erases your digits, and New "
  "starts another puzzle; each of them asks first. The answer of the last puzzle you finish "
  "is kept in SU_SOLVED."),
 ("My games",
  "Every puzzle that you finish yourself is kept in My games, with its level, its number of clues, your "
  "time in minutes, and how many times you used Hint and Check. Up to @MAXGAMES@ games are kept, and Clear "
  "empties My games.|"
  "The clock runs only while the board is on the screen, so the menus, questions and help pages do not "
  "count. A game that Solve or Watch finished is not kept, because then the program did the work."),
 ("The My games plot",
  "The plot shows your minutes against the clues, one dot for each game in its level's color, and each "
  "level's median time at the right. The median is the middle time, which a few very slow games cannot "
  "pull up the way they pull up a mean.|"
  "Once three games have two different numbers of clues, the plot adds the least-squares line and r, the "
  "correlation, which tells how closely the dots follow the line."),
 ("My games in Statistics 2Var",
  "2Var copies My games into the Statistics 2Var app: the clues go to C1, the minutes to C2, the level to "
  "C3 (1 Easy, 2 Medium, 3 Hard, 4 Expert, 5 typed), the Hints to C4 and the Checks to C5. When any of "
  "those columns already holds data, Sudoku asks first.|"
  "Open the app from the Apps key. Its first analysis, S1, reads C1 and C2 unless it has been changed, so "
  "its Plot view shows your minutes against the clues, and Num, then Stats, gives r."),
 ("A class experiment",
  "A class can pool its games to ask whether fewer clues take longer. One or two players tell us little "
  "about all players, because people differ so much, so the more players, the better.|"
  "Our levels and their clues go together (an Easy puzzle has more clues than an Expert one), so a slower "
  "time may come from harder logic rather than from fewer clues. Practice makes everyone faster, too, so "
  "the order in which the levels are played should be drawn at random."),
 ("Credits",
  "Written new for the HP Prime by Roger Metcalf, with Claude (Anthropic), in November 2026; "
  "none of anyone else's code is in it. Ideas came from three Sudoku programs in the "
  "hpcalc.org library: Lennart Borjeson's (2015), chromos's (2024) and HPleak's (2023)."),
]
MAXGAMES = 200                            # beta 2a: My games keeps this many games
GAMES0 = ("Finish a puzzle yourself, and it is kept here: its level, its number of clues, your time in "
          "minutes, and how many times you used Hint and Check.|Solve and Watch do not count, because then "
          "the program did the work. Help explains the plot that you will see here.")
SENT2V = ("C1 holds the clues, C2 the minutes, C3 the level (1 Easy, 2 Medium, 3 Hard, 4 Expert, 5 typed), "
          "C4 the Hints and C5 the Checks.|Open the app from the Apps key. Its first analysis, S1, reads C1 "
          "and C2 unless it has been changed, so its Plot view shows your minutes against the clues, and Num, "
          "then Stats, gives r.")
HELP = [(h, x.replace('@MAXGAMES@', str(MAXGAMES))) for h, x in HELP]
MAXW, MAXC, MAXL = 300, 47, 13           # px at font 2 from x = 8; characters (the overlap tool's narrow
                                          # 6.5 px); lines between y = 26 and the footer at y = 226
def wrap(text):
    lines = []
    for para in text.split('|'):
        if lines:
            lines.append('')
        cur = ''
        for w in para.split():
            t = (cur + ' ' + w) if cur else w
            if width(t, 2) <= MAXW and len(t) <= MAXC:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines

HELPH, HELPT = [], []
for title, text in HELP:
    lines = wrap(text)
    if len(lines) > MAXL:
        raise SystemExit('help page %r has %d lines (at most %d)' % (title, len(lines), MAXL))
    if width(title, 2) > 270:
        raise SystemExit('help title %r is %d px wide' % (title, width(title, 2)))
    HELPH.append(title); HELPT.append(lines)
    print('help %-26s %2d lines, widest %3d px' % (title, len(lines), max(width(l, 2) for l in lines)))
HELPGAMES = [h for h, x in HELP].index('My games') + 1
G0L, S2L = wrap(GAMES0), wrap(SENT2V)
if len(G0L) > 8 or len(S2L) > 10:
    raise SystemExit('My games texts too long: %d and %d lines' % (len(G0L), len(S2L)))
print('My games, no games: %d lines; after the copy: %d lines; help page "My games" is page %d'
      % (len(G0L), len(S2L), HELPGAMES))
# the levels and their clues go together, as the help page says: every Easy puzzle has more clues than every Expert one
assert min(81 - b['p'].count('0') for b in base['Easy']) > max(81 - b['p'].count('0') for b in base['Expert'])

# ------------------------------------------------------------------ write the program
t = open(os.path.join(HERE, 'Sudoku_beta2a_template.txt'), encoding='utf-8').read()
OUTDIR = HERE if '--out' not in sys.argv else sys.argv[sys.argv.index('--out') + 1]
subs = {
    '@UNIT@': plist(UNIT), '@PEER@': plist(PEER),
    '@BP@': pslist(BP), '@BS@': pslist(BS),
    '@NBASE@': str(len(BP)), '@PERLEVEL@': str(per),
    '@GLYO@': plist(GLYO), '@GLYS@': plist(GLYS), '@GLYN@': plist(GLYN),
    '@HELPH@': pslist(HELPH),
    '@HELPT@': '{' + ', '.join(pslist(p) for p in HELPT) + '}',
    '@GAMES0@': pslist(G0L), '@SENT2V@': pslist(S2L),
    '@MAXGAMES@': str(MAXGAMES), '@HELPGAMES@': str(HELPGAMES),
}
for k, v in subs.items():
    if k not in t:
        raise SystemExit('the template has no %s' % k)
    t = t.replace(k, v)
assert '@' not in t.replace('@', '', 0) or all(k not in t for k in subs)
left = [w for w in t.split() if w.startswith('@') and w.endswith('@')]
if left:
    raise SystemExit('placeholders left: %s' % left)
out = os.path.join(OUTDIR, 'Sudoku_beta2a.txt')
open(out, 'w', encoding='utf-8', newline='\n').write(t)
print('wrote %s: %d lines, %d characters' % (out, t.count('\n'), len(t)))
