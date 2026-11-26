#!/usr/bin/env python3
"""make_beta2a_template.py -- writes Sudoku_beta2a_template.txt from Sudoku_beta2_template.txt by exact
replacements (each old text must occur exactly once, or the script stops).  26 Nov 2026.
Beta 2a adds My games, for the book's solving-time experiment, and a clock that runs only while the board
is on the screen."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
# beta 2's template: beside this script in the cloud session's layout, or in D:\HP-Prime's _superseded folder
for SRC in (os.path.join(HERE, '..', 'sudoku2', 'Sudoku_beta2_template.txt'),
            os.path.join(HERE, '..', '_superseded_2026-11-26', 'Sudoku_build_beta2', 'Sudoku_beta2_template.txt'),
            os.path.join(HERE, 'Sudoku_beta2_template.txt')):
    if os.path.exists(SRC):
        break
OUT = os.path.join(HERE, 'Sudoku_beta2a_template.txt')
t = open(SRC, encoding='utf-8').read()

def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        sys.exit('found %d times, not once: %r' % (n, old[:100]))
    t = t.replace(old, new)

# ---- the header
rep('// Sudoku beta 2  -  play Sudoku,', '// Sudoku beta 2a  -  play Sudoku,')
rep('// Sudoku_beta2_CHANGES.md).', '// Sudoku_beta2a_CHANGES.md).')
rep('''// WHAT CHANGED
// beta 2 (26 Nov 2026):''', '''// WHAT CHANGED
// beta 2a (26 Nov 2026): My games, for the book's solving-time
//   experiment (Roger: "we could do an experiment to see how long it
//   takes people to solve a puzzle compared to the number of initial
//   clues"). Each puzzle that you finish yourself becomes one game:
//   its level, its clues, your minutes, and the Hints and Checks you
//   used (suLogGame; at most @MAXGAMES@ games). My games, the last item
//   of the first menu and an item of the Enter menu, plots minutes
//   against clues, one dot a game in its level's color, with the
//   least-squares line and r (suGamesDraw), and copies the games into
//   the Statistics 2Var app, C1 to C5, asking first when those
//   columns hold data (suTo2Var). The clock now runs only while the
//   board is on the screen: a menu, a question or a help page no
//   longer counts (suDrain starts it again), and one wait counts for
//   two minutes at most (suTick). The Enter menu's Help and Exit
//   Sudoku move down one place, below My games; two help pages, on My
//   games, come before Credits.
// beta 2 (26 Nov 2026):''')

# ---- the log's file-level values
rep('LOCAL suFlash;\n', 'LOCAL suFlash;\nLOCAL suGLv, suGCl, suGMn, suGHn, suGCk, suGNew;   // My games (beta 2a)\n')
rep('''  suPow := {1, 2, 4, 8, 16, 32, 64, 128, 256};
  suReady := 1;''', '''  suPow := {1, 2, 4, 8, 16, 32, 64, 128, 256};
  // My games starts empty (beta 2a)
  suGLv := {}; suGCl := {}; suGMn := {}; suGHn := {}; suGCk := {}; suGNew := 0;
  suReady := 1;''')

# ---- the clock: a dialog or a held page is not the game's time
rep('''  REPEAT UNTIL MOUSE(1) == -1 OR TICKS - suDrT > 1000;
  suStale := 1;      // a dialog's own tap may still reach the board's WAIT(-1) (see suPlay)
END;''', '''  REPEAT UNTIL MOUSE(1) == -1 OR TICKS - suDrT > 1000;
  suStale := 1;      // a dialog's own tap may still reach the board's WAIT(-1) (see suPlay)
  suTLast := TICKS;  // beta 2a: the time spent in a dialog or a held page is not the game's
END;''')
rep('''// suTick: add the time since the last event to the game's clock
suTick()
BEGIN
  LOCAL suTkN;
  suTkN := TICKS;
  IF suGame == 1 AND suMode == 1 THEN
    IF suTkN - suTLast > 0 THEN suTEl := suTEl + (suTkN - suTLast); END;
  END;
  suTLast := suTkN;
END;''', '''// suTick: add the time since the last event to the game's clock. One
// wait counts for two minutes at most (beta 2a): WAIT(-1) gives up after
// about a minute, so a longer gap means that the calculator was off
suTick()
BEGIN
  LOCAL suTkN, suTkD;
  suTkN := TICKS;
  IF suGame == 1 AND suMode == 1 THEN
    suTkD := suTkN - suTLast;
    IF suTkD > 120000 THEN suTkD := 120000; END;
    IF suTkD > 0 THEN suTEl := suTEl + suTkD; END;
  END;
  suTLast := suTkN;
END;''')

# ---- a new game has not been logged yet
rep('''  suHints := 0; suChecks := 0; suFlash := {};
  suClearHint();
  suWatched := 0; suPanel := 0;''', '''  suHints := 0; suChecks := 0; suFlash := {}; suGNew := 0;
  suClearHint();
  suWatched := 0; suPanel := 0;''')

# ---- the finish: the game goes into My games
rep('''// suCelebrate: the puzzle is done
suCelebrate()
BEGIN
  LOCAL suCeT;
  suGame := 2;''', '''// suLogGame: a puzzle that the player finished becomes one game of My
// games (beta 2a): its level, its clues, the minutes on the clock, and
// the Hints and Checks used. Returns the game's number, or 0 when My
// games already holds @MAXGAMES@ games.
suLogGame()
BEGIN
  LOCAL suLgN;
  suLgN := SIZE(suGLv);
  IF suLgN >= @MAXGAMES@ THEN RETURN 0; END;
  suLgN := suLgN + 1;
  suGLv(suLgN) := suLevel;
  suGCl(suLgN) := suCountClues();
  suGMn(suLgN) := ROUND(suTEl / 60000, 2);
  suGHn(suLgN) := suHints;
  suGCk(suLgN) := suChecks;
  RETURN suLgN;
END;

// suCelebrate: the puzzle is done
suCelebrate()
BEGIN
  LOCAL suCeT;
  suGame := 2;
  suGNew := suLogGame();''')
rep('''  RECT_P(G1, 30, 66, 290, 160, RGB(255,69,0), RGB(255,240,220));
  TEXTOUT_P("Solved!", G1, 112, 74, 5, RGB(0,140,60));
  TEXTOUT_P("Your time: " + suTime(suTEl), G1, 46, 104, 2, RGB(0,0,0));
  TEXTOUT_P("Hints " + suNs(suHints) + "    Checks " + suNs(suChecks), G1, 46, 122, 2, RGB(0,0,0));
  TEXTOUT_P("Press a key or tap to go on.", G1, 46, 142, 1, RGB(30,144,255));''',
'''  RECT_P(G1, 30, 66, 290, 172, RGB(255,69,0), RGB(255,240,220));
  TEXTOUT_P("Solved!", G1, 112, 74, 5, RGB(0,140,60));
  TEXTOUT_P("Your time: " + suTime(suTEl), G1, 46, 104, 2, RGB(0,0,0));
  TEXTOUT_P("Hints " + suNs(suHints) + "    Checks " + suNs(suChecks), G1, 46, 122, 2, RGB(0,0,0));
  IF suGNew > 0 THEN
    TEXTOUT_P("Kept as game " + suNs(suGNew) + " of My games.", G1, 46, 142, 1, RGB(0,0,0));
  ELSE
    TEXTOUT_P("My games is full: @MAXGAMES@ games.", G1, 46, 142, 1, RGB(0,0,0));
  END;
  TEXTOUT_P("Press a key or tap to go on.", G1, 46, 156, 1, RGB(30,144,255));''')

# ---- the help pages can open at a given page
rep('''// suHelp: the help pages. A key or a tap turns the page, Left goes
// back, Esc leaves.
suHelp()
BEGIN
  LOCAL suHpP, suHpI, suHpK, suHpN, suHpT;
  suHpN := SIZE(suHelpT);
  suHpP := 1;''', '''// suHelpFrom: the help pages, from page suHfP on. A key or a tap turns
// the page, Left goes back, Esc leaves.
suHelpFrom(suHfP)
BEGIN
  LOCAL suHpP, suHpI, suHpK, suHpN, suHpT;
  suHpN := SIZE(suHelpT);
  suHpP := suHfP;''')
rep('''END;

// suBusy: 1 when a game has digits, marks or clues that would be lost''', '''END;

// suHelp: the help pages from the first
suHelp()
BEGIN
  suHelpFrom(1);
END;

// suBusy: 1 when a game has digits, marks or clues that would be lost''')

# ---- My games: the page, its plot, the copy into Statistics 2Var, Clear
GAMES = r'''// =====================================================================
// MY GAMES (beta 2a). Game i of My games is suGLv(i), the level (1 Easy
// ... 4 Expert, 5 typed); suGCl(i), its clues; suGMn(i), the minutes on
// the clock; suGHn(i) and suGCk(i), the Hints and Checks used. Kept like
// the game: file-level values stay until the program is checked or sent
// again.
// =====================================================================

// suNice: a round step for an axis suNcR long, in about four parts: 1,
// 2 or 5 times a power of ten (Heckbert's nice numbers)
suNice(suNcR)
BEGIN
  LOCAL suNcE, suNcF;
  IF suNcR <= 0 THEN RETURN 1; END;
  suNcE := FLOOR(LOG(suNcR / 4));
  suNcF := (suNcR / 4) / (10 ^ suNcE);
  IF suNcF <= 1 THEN RETURN 10 ^ suNcE; END;
  IF suNcF <= 2 THEN RETURN 2 * 10 ^ suNcE; END;
  IF suNcF <= 5 THEN RETURN 5 * 10 ^ suNcE; END;
  RETURN 10 * 10 ^ suNcE;
END;

// suTickTxt: a tick's number as text: whole when the step is whole, else
// with one decimal; commas either way (the fleet's rule)
suTickTxt(suTtV, suTtS)
BEGIN
  IF suTtS >= 1 THEN RETURN suNs(suTtV); END;
  RETURN suCm(STRING(ROUND(suTtV, 1) + 0.0, 2, 1));
END;

// suTxtW: the width of a number's text in font 1, in pixels, from the
// widths measured on the Virtual Calculator: 3 for a period or a comma,
// 6 for a digit or a minus sign
suTxtW(suTwS)
BEGIN
  LOCAL suTwI, suTwW, suTwC;
  suTwW := 0;
  FOR suTwI FROM 1 TO DIM(suTwS) DO
    suTwC := MID(suTwS, suTwI, 1);
    IF suTwC == "." OR suTwC == "," THEN suTwW := suTwW + 3; ELSE suTwW := suTwW + 6; END;
  END;
  RETURN suTwW;
END;

// suMedian: the middle value of a list of numbers (the mean of the two
// middle values when the count is even)
suMedian(suMdL)
BEGIN
  LOCAL suMdS, suMdN;
  suMdN := SIZE(suMdL);
  IF suMdN == 0 THEN RETURN 0; END;
  suMdS := SORT(suMdL);
  IF (suMdN MOD 2) == 1 THEN RETURN suMdS((suMdN + 1) / 2); END;
  RETURN (suMdS(suMdN / 2) + suMdS(suMdN / 2 + 1)) / 2;
END;

// suGamesDraw: the My games page, made in G1. The plot: minutes up the
// left (x = 40, from y = 186 up to y = 42) against clues across (to
// x = 246), one square dot a game in its level's color (the board's
// colors), and, with at least 3 games and 2 different clue counts, the
// least-squares line and r, both from the deviations from the means in
// a second pass. At the right, each level's color, its count, and its
// median minutes, because a few very slow games pull a mean up.
suGamesDraw()
BEGIN
  LOCAL suGdN, suGdI, suGdK, suGdC, suGdL, suGdM;
  LOCAL suGdX0, suGdX1, suGdYm, suGdS, suGdT, suGdV;
  LOCAL suGdP, suGdQ, suGdU, suGdMx, suGdMy, suGdB;
  LOCAL suGdQx, suGdQy, suGdQxy, suGdA, suGdXa, suGdXb;
  LOCAL suGdYa, suGdYb, suGdTx;
  suGdC := {RGB(0,140,60), RGB(30,144,255), RGB(255,69,0), RGB(200,0,200), RGB(90,90,90)};
  suGdN := SIZE(suGLv);
  DIMGROB_P(G1, 320, 240, RGB(255,255,255));
  RECT_P(G1, 0, 0, 319, 20, RGB(0,60,200), RGB(0,60,200));
  TEXTOUT_P("My games: minutes against clues", G1, 8, 3, 2, RGB(255,255,255));
  IF suGdN == 0 THEN
    TEXTOUT_P("No games yet.", G1, 8, 28, 3, RGB(0,60,200));
    FOR suGdI FROM 1 TO SIZE(suGames0) DO
      TEXTOUT_P(suGames0(suGdI), G1, 8, 54 + 16 * (suGdI - 1), 2, RGB(0,0,0));
    END;
    RETURN 0;
  END;
  // the ranges: clues from one below the fewest to one above the most
  // (at least 4 wide), minutes from 0 to a round number above the most
  suGdX0 := suGCl(1); suGdX1 := suGCl(1); suGdYm := 1;
  FOR suGdI FROM 1 TO suGdN DO
    suGdX0 := MIN(suGdX0, suGCl(suGdI)); suGdX1 := MAX(suGdX1, suGCl(suGdI));
    suGdYm := MAX(suGdYm, suGMn(suGdI));
  END;
  suGdX0 := suGdX0 - 1; suGdX1 := suGdX1 + 1;
  IF suGdX1 - suGdX0 < 4 THEN suGdX0 := suGdX0 - 1; suGdX1 := suGdX1 + 1; END;
  suGdS := suNice(suGdYm * 1.05);
  suGdT := suGdS * CEILING(suGdYm * 1.05 / suGdS);
  // the minutes: light grid lines, ticks and their numbers
  suGdV := 0;
  WHILE suGdV <= suGdT + suGdS / 1000 DO
    suGdQ := IP(186 - suGdV * 144 / suGdT + 0.5);
    IF suGdV > 0 THEN LINE_P(G1, 41, suGdQ, 246, suGdQ, RGB(225,225,225)); END;
    LINE_P(G1, 37, suGdQ, 40, suGdQ, RGB(0,0,0));
    suGdL := suTickTxt(suGdV, suGdS);
    TEXTOUT_P(suGdL, G1, 35 - suTxtW(suGdL), suGdQ - 5, 1, RGB(0,0,0));
    suGdV := suGdV + suGdS;
  END;
  // the clues: ticks and their numbers
  suGdU := suNice(suGdX1 - suGdX0);
  suGdV := CEILING(suGdX0 / suGdU) * suGdU;
  WHILE suGdV <= suGdX1 DO
    suGdP := IP(40 + (suGdV - suGdX0) * 206 / (suGdX1 - suGdX0) + 0.5);
    LINE_P(G1, suGdP, 186, suGdP, 189, RGB(0,0,0));
    suGdL := suNs(suGdV);
    // a number at the corner would run into the minutes' 0, so it is left out
    IF suGdP - IP(suTxtW(suGdL) / 2) >= 38 THEN TEXTOUT_P(suGdL, G1, suGdP - IP(suTxtW(suGdL) / 2), 190, 1, RGB(0,0,0)); END;
    suGdV := suGdV + suGdU;
  END;
  LINE_P(G1, 40, 42, 40, 186, RGB(0,0,0));
  LINE_P(G1, 40, 186, 246, 186, RGB(0,0,0));
  TEXTOUT_P("minutes", G1, 4, 23, 1, RGB(0,0,0));
  TEXTOUT_P("clues", G1, 131, 202, 1, RGB(0,0,0));
  // the least-squares line and r: the means first, then the deviations
  suGdMx := 0; suGdMy := 0;
  FOR suGdI FROM 1 TO suGdN DO
    suGdMx := suGdMx + suGCl(suGdI); suGdMy := suGdMy + suGMn(suGdI);
  END;
  suGdMx := suGdMx / suGdN; suGdMy := suGdMy / suGdN;
  suGdQx := 0; suGdQy := 0; suGdQxy := 0;
  FOR suGdI FROM 1 TO suGdN DO
    suGdQx := suGdQx + (suGCl(suGdI) - suGdMx) ^ 2;
    suGdQy := suGdQy + (suGMn(suGdI) - suGdMy) ^ 2;
    suGdQxy := suGdQxy + (suGCl(suGdI) - suGdMx) * (suGMn(suGdI) - suGdMy);
  END;
  IF suGdN >= 3 AND suGdQx > 0 THEN
    suGdB := suGdQxy / suGdQx; suGdA := suGdMy - suGdB * suGdMx;
    // the line from the left edge to the right edge, cut where it would
    // leave the plot at the top or the bottom
    suGdXa := suGdX0; suGdYa := suGdA + suGdB * suGdX0;
    suGdXb := suGdX1; suGdYb := suGdA + suGdB * suGdX1;
    IF suGdYa < 0 THEN suGdXa := (0 - suGdA) / suGdB; suGdYa := 0; END;
    IF suGdYa > suGdT THEN suGdXa := (suGdT - suGdA) / suGdB; suGdYa := suGdT; END;
    IF suGdYb < 0 THEN suGdXb := (0 - suGdA) / suGdB; suGdYb := 0; END;
    IF suGdYb > suGdT THEN suGdXb := (suGdT - suGdA) / suGdB; suGdYb := suGdT; END;
    LINE_P(G1, IP(40 + (suGdXa - suGdX0) * 206 / (suGdX1 - suGdX0) + 0.5), IP(186 - suGdYa * 144 / suGdT + 0.5), IP(40 + (suGdXb - suGdX0) * 206 / (suGdX1 - suGdX0) + 0.5), IP(186 - suGdYb * 144 / suGdT + 0.5), RGB(90,90,90));
    IF suGdQy > 0 THEN
      suGdTx := "n = " + suNs(suGdN) + "      r = " + STRING(ROUND(suGdQxy / (suGdQx * suGdQy) ^ 0.5, 2) + 0.0, 2, 2);
    ELSE
      suGdTx := "n = " + suNs(suGdN) + "; every time is the same";
    END;
  ELSE
    IF suGdN < 3 THEN
      suGdTx := "n = " + suNs(suGdN) + "; the line and r need 3 games";
    ELSE
      suGdTx := "n = " + suNs(suGdN) + ", all with " + suNs(suGCl(1)) + " clues: no line";
    END;
  END;
  TEXTOUT_P(suGdTx, G1, 60, 23, 1, RGB(0,0,0));
  // the dots, over the grid and the line
  FOR suGdI FROM 1 TO suGdN DO
    suGdP := IP(40 + (suGCl(suGdI) - suGdX0) * 206 / (suGdX1 - suGdX0) + 0.5);
    suGdQ := IP(186 - suGMn(suGdI) * 144 / suGdT + 0.5);
    RECT_P(G1, suGdP - 3, suGdQ - 3, suGdP + 3, suGdQ + 3, RGB(0,0,0), suGdC(suGLv(suGdI)));
  END;
  // the levels: color, count, and median minutes
  TEXTOUT_P("Median min", G1, 252, 110, 1, RGB(0,60,200));
  suGdU := 0;
  FOR suGdK FROM 1 TO 5 DO
    suGdM := {};
    FOR suGdI FROM 1 TO suGdN DO
      IF suGLv(suGdI) == suGdK THEN suGdM(SIZE(suGdM) + 1) := suGMn(suGdI); END;
    END;
    RECT_P(G1, 252, 42 + 13 * (suGdK - 1), 258, 48 + 13 * (suGdK - 1), RGB(0,0,0), suGdC(suGdK));
    TEXTOUT_P(suLvName(suGdK) + " " + suNs(SIZE(suGdM)), G1, 262, 40 + 13 * (suGdK - 1), 1, RGB(0,0,0));
    IF SIZE(suGdM) > 0 THEN
      suGdU := suGdU + 1;
      TEXTOUT_P(suLvName(suGdK) + " " + suCm(STRING(ROUND(suMedian(suGdM), 1) + 0.0, 2, 1)), G1, 252, 110 + 13 * suGdU, 1, RGB(0,0,0));
    END;
  END;
  RETURN suGdN;
END;

// suTo2Var: copy My games into the Statistics 2Var app: the clues to C1,
// the minutes to C2, the level to C3, the Hints to C4 and the Checks to
// C5. The columns are global (Lessons Learned 10), but a column does not
// exist until the app has been opened once, so each reach goes in IFERR.
// Asks first when any of C1 to C5 already holds data.
suTo2Var()
BEGIN
  LOCAL suTvF, suTvI, suTvN;
  suTvN := SIZE(suGLv);
  IF suTvN == 0 THEN RETURN 0; END;
  suTvF := 0;
  IFERR
    IF SIZE(C1) > 0 OR SIZE(C2) > 0 OR SIZE(C3) > 0 OR SIZE(C4) > 0 OR SIZE(C5) > 0 THEN suTvF := 1; END;
  THEN
    suTvF := 0;
  END;
  IF suTvF == 1 THEN
    IF suAsk("Replace C1 to C5?", "Yes, put my games there", "No, keep what is there") == 0 THEN RETURN 0; END;
  END;
  IFERR
    C1 := suGCl; C2 := suGMn; C3 := suGLv; C4 := suGHn; C5 := suGCk;
  THEN
    MSGBOX("Statistics 2Var could not take the games. Open the app once from the Apps key, and then try again.");
    suDrain();
    RETURN 0;
  END;
  DIMGROB_P(G1, 320, 240, RGB(255,255,255));
  RECT_P(G1, 0, 0, 319, 20, RGB(0,140,60), RGB(0,140,60));
  TEXTOUT_P("Sent to Statistics 2Var", G1, 8, 3, 2, RGB(255,255,255));
  IF suTvN == 1 THEN
    TEXTOUT_P("1 game is now in C1 to C5.", G1, 8, 28, 2, RGB(0,0,0));
  ELSE
    TEXTOUT_P(suNs(suTvN) + " games are now in C1 to C5.", G1, 8, 28, 2, RGB(0,0,0));
  END;
  FOR suTvI FROM 1 TO SIZE(suSent2V) DO
    TEXTOUT_P(suSent2V(suTvI), G1, 8, 50 + 15 * (suTvI - 1), 2, RGB(0,0,0));
  END;
  TEXTOUT_P("Press a key or tap to go on.", G1, 8, 226, 1, RGB(30,144,255));
  BLIT_P(G0, 0, 0, G1);
  suWaitAny();
  RETURN 1;
END;

// suClearGames: empty My games, after a question
suClearGames()
BEGIN
  IF SIZE(suGLv) == 0 THEN RETURN 0; END;
  IF suAsk("Clear My games?", "Yes, clear all " + suNs(SIZE(suGLv)) + " games", "No, keep them") == 1 THEN
    suGLv := {}; suGCl := {}; suGMn := {}; suGHn := {}; suGCk := {};
    RETURN 1;
  END;
  RETURN 0;
END;

// suGames: the My games page. 2Var copies the games into Statistics 2Var,
// Clear empties My games, Help opens its help page, Back or Esc leaves.
// With DRAWMENU on the screen a tap on its strip comes only as a click
// (y >= 218), and a click handed over at once after a dialog is that
// dialog's own tap (Lessons Learned 7), so it is skipped, as on the board.
suGames()
BEGIN
  LOCAL suGmE, suGmW, suGmS, suGmGo;
  suGmGo := 1;
  WHILE suGmGo == 1 DO
    suGamesDraw();
    BLIT_P(G0, 0, 0, G1);
    IF SIZE(suGLv) > 0 THEN
      DRAWMENU({"2Var", "Clear", "", "", "Help", "Back"});
    ELSE
      DRAWMENU({"", "", "", "", "Help", "Back"});
    END;
    suGmW := TICKS;
    suGmE := WAIT(-1);
    suGmW := TICKS - suGmW;
    IF TYPE(suGmE) == 6 THEN
      IF SIZE(suGmE) >= 3 THEN
        IF suGmE(1) == 3 AND suGmE(3) + 0.0 >= 218 THEN
          suGmS := MIN(6, IP((suGmE(2) + 0.0) / 53.4) + 1);
          IF suStale == 1 AND suGmW < 100 THEN suGmS := 0; END;
          suStale := 0;
          IF suGmS == 1 THEN suTo2Var(); END;
          IF suGmS == 2 THEN suClearGames(); END;
          IF suGmS == 5 THEN suHelpFrom(@HELPGAMES@); END;
          IF suGmS == 6 THEN suGmGo := 0; END;
        END;
      END;
    ELSE
      IF suGmE == 4 THEN suGmGo := 0; END;
      IF suGmE == 3 THEN suHelpFrom(@HELPGAMES@); END;
    END;
  END;
END;

// suAction: carry out one action by number'''
rep('// suAction: carry out one action by number', GAMES)
rep('''//  marks  14 Play (typing)  15 Clear (typing)  16 Back (typing)  17 Exit
// Returns 0 to go on, 2 to leave the program.''', '''//  marks  14 Play (typing)  15 Clear (typing)  16 Back (typing)  17 Exit
//  18 My games (beta 2a)
// Returns 0 to go on, 2 to leave the program.''')
rep('''  IF suAcA == 17 THEN RETURN 2; END;
  RETURN 0;
END;''', '''  IF suAcA == 17 THEN RETURN 2; END;
  IF suAcA == 18 THEN suGames(); RETURN 0; END;
  RETURN 0;
END;''')

# ---- the Enter menu: My games after Type in a puzzle
rep('''"New puzzle", "Type in a puzzle", "Help", "Exit Sudoku"});
    suDrain();
    suMnA := {3, 5, 4, 2, 12, 13, 7, 8, 10, 1, 9, 11, 17};''', '''"New puzzle", "Type in a puzzle", "My games", "Help", "Exit Sudoku"});
    suDrain();
    suMnA := {3, 5, 4, 2, 12, 13, 7, 8, 10, 1, 9, 18, 11, 17};''')

# ---- the first menu: My games as its last item
rep('''  LOCAL suMain, suItems, suActs, suGo, suOut;
  HSeparator := 0;''', '''  LOCAL suMain, suItems, suActs, suGo, suOut, suGmT;
  HSeparator := 0;''')
rep('''    suItems := CONCAT(suItems, {"New puzzle: Easy", "New puzzle: Medium", "New puzzle: Hard", "New puzzle: Expert", "Type in a puzzle", "Use the puzzle in M9", "How to play (Help)"});
    suActs := CONCAT(suActs, {1, 2, 3, 4, 5, 6, 7});''', '''    IF SIZE(suGLv) == 0 THEN suGmT := "My games (none yet)"; ELSE suGmT := "My games (" + suNs(SIZE(suGLv)) + " so far)"; END;
    suItems := CONCAT(suItems, {"New puzzle: Easy", "New puzzle: Medium", "New puzzle: Hard", "New puzzle: Expert", "Type in a puzzle", "Use the puzzle in M9", "How to play (Help)", suGmT});
    suActs := CONCAT(suActs, {1, 2, 3, 4, 5, 6, 7, 9});''')
rep('''      IF suMain == 7 THEN suHelp(); END;''', '''      IF suMain == 7 THEN suHelp(); END;
      IF suMain == 9 THEN suGames(); END;''')
rep('''      IF suMain <> 7 AND (suGame >= 1 OR suMode == 2) THEN''', '''      IF suMain <> 7 AND suMain <> 9 AND (suGame >= 1 OR suMode == 2) THEN''')
rep('''  IF suGame == 2 AND suWatched == 0 THEN RETURN "Sudoku: solved in " + suTime(suTEl) + ". The answer is in SU_SOLVED."; END;''',
'''  IF suGame == 2 AND suWatched == 0 AND suGNew > 0 THEN RETURN "Sudoku: solved in " + suTime(suTEl) + ", game " + suNs(suGNew) + " of My games. The answer is in SU_SOLVED."; END;
  IF suGame == 2 AND suWatched == 0 THEN RETURN "Sudoku: solved in " + suTime(suTEl) + ". The answer is in SU_SOLVED."; END;''')

# ---- the texts the build wraps
rep('LOCAL suHelpT := @HELPT@;', 'LOCAL suHelpT := @HELPT@;\nLOCAL suGames0 := @GAMES0@;     // My games with no games yet (beta 2a)\nLOCAL suSent2V := @SENT2V@;     // after the copy into Statistics 2Var (beta 2a)')
open(OUT, 'w', encoding='utf-8', newline='\n').write(t)
print('wrote', OUT, t.count('\n'), 'lines')
