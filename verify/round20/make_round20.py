# -*- coding: utf-8 -*-
"""make_round20.py -- round 20 (27 Nov 2026): DataLoad beta 1i from beta 1h, by exact replacements.

The fault (found 27 Nov 2026, while the book's Draft 119 was checked against a reviewer's question): beta 1h's dd_Column leaves
the blank cells out of each column separately.  That is right for separate groups of unequal size and wrong for paired columns
(before and after, x and y, raters): one blank in the middle of a column makes the rest of that column slide up a row, and the
lists no longer match row for row.  beta 1i, when it is about to load two or more columns, looks for a blank ABOVE a value in
any of them and then asks how the columns go together: "Pairs: keep complete rows" (only the rows with a value in every column) or "Separate
groups: drop blanks" (beta 1h's way).  Blanks at the foot of a column (groups of unequal size, the Data Loader page's padding)
ask nothing, as before.  A help page of its own explains it (help is four pages now).

Run from the repository's root:  python3 verify/round20/make_round20.py
Every replacement must find its old text exactly once, or the script stops and writes nothing."""
import io, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OLD = os.path.join(ROOT, 'programs', 'DataLoad_beta1h.txt')
NEW = os.path.join(ROOT, 'programs', 'DataLoad_beta1i.txt')
s = io.open(OLD, encoding='utf-8', newline='').read()
CRLF = '\r\n' in s
if CRLF: s = s.replace('\r\n', '\n')
n = [0]

def rep(a, b, what):
    global s
    c = s.count(a)
    if c != 1: sys.exit('make_round20: %s: the old text stands %d times, not once' % (what, c))
    s = s.replace(a, b); n[0] += 1

# ---- the header ----
rep("// DATALOAD - beta 1h\n", "// DATALOAD - beta 1i\n", 'version')
rep("// (C) 2026 Roger D. Metcalf.  Written with AI assistance (Anthropic\n//   Claude).\n",
    "// (C) 2026 Roger D. Metcalf.\n"
    "// Written with AI assistance. The concept, direction, decisions and all\n"
    "// hardware testing are Roger D. Metcalf's; the code, drafting and\n"
    "// source-checking were done with Claude (Anthropic); beta 1i with\n"
    "// Claude Opus 5.5, November 2026.\n", 'credit')
rep("// beta 1h (22 Nov 2026): Round 18:",
    "// beta 1i (27 Nov 2026): Round 20: blank cells inside paired columns.  beta 1h left the blanks out of each\n"
    "//   column separately, which is right for separate groups of unequal size and wrong for paired columns\n"
    "//   (before and after, x and y, raters): one blank in the middle of a column made the rest of that column\n"
    "//   slide up a row, so the lists no longer matched row for row (found 27 Nov 2026, when the book's Draft 119\n"
    "//   was checked against a reviewer's question).  Now, when two or more columns are to be loaded and any of\n"
    "//   them has a blank ABOVE a value, DataLoad asks how they go together: \"Pairs: keep complete rows\" keeps only the rows\n"
    "//   with a value in every column (dd_Full, dd_Pick), and \"Separate groups: drop blanks\" is beta 1h's way\n"
    "//   (dd_Column).  Blanks only at the foot of a column ask nothing, as before.  Help is four pages: page 3,\n"
    "//   \"Blank cells\", says all this; pages 2 and 4 were 2 and 3, word for word.  Scores by group is unchanged\n"
    "//   (it always kept only the rows with both cells).\n"
    "// beta 1h (22 Nov 2026): Round 18:", 'beta 1i block')
rep("// BLANK CELLS: a column shorter than the others is padded by the web\n"
    "//   page with 9.99999999999E499, the Prime's largest real (a number no\n"
    "//   data set can hold).  DataLoad leaves out any cell at 1E499 or\n"
    "//   above, so each list gets only its own values.\n",
    "// BLANK CELLS: a column shorter than the others is padded by the web\n"
    "//   page with 9.99999999999E499, the Prime's largest real (a number no\n"
    "//   data set can hold).  DataLoad leaves out any cell at 1E499 or\n"
    "//   above, so each list gets only its own values.  A blank ABOVE a\n"
    "//   value (beta 1i) is different: in paired columns it would make the\n"
    "//   rest of its column slide up a row, so DataLoad asks first whether\n"
    "//   the columns are pairs (keep the complete rows only) or separate\n"
    "//   groups (leave each blank out of its own column).\n", 'BLANK CELLS note')

# ---- three new routines, after dd_Column ----
rep("""  IF dd_Real(kv) THEN kl := CONCAT(kl, {kv}); END;
 END;
 RETURN kl;
END;
""", """  IF dd_Real(kv) THEN kl := CONCAT(kl, {kv}); END;
 END;
 RETURN kl;
END;

// beta 1i: is there a blank ABOVE a value in columns 1 .. hk?  Such a
// blank is not the web page's padding at the foot of a short column; it
// is a cell missing in the middle of the data.  Each column is read from
// the top: once a blank has been seen, a value below it means a hole.
// Returns {how many columns have a hole, the first such column}.
LOCAL dd_Holes(hm, hk)
BEGIN
 LOCAL hoS, hoV, hoR, hoJ, hoB, hoN;
 LOCAL hoF, hoH;
 hoS := dd_Shape(hm);
 hoV := dd_IsVec(hm);
 hoN := 0; hoF := 0;
 FOR hoJ FROM 1 TO hk DO
  hoB := 0; hoH := 0;
  FOR hoR FROM 1 TO hoS(1) DO
   IF dd_Real(dd_Cell(hm, hoR, hoJ, hoV)) THEN
    // a value: below a blank, that blank was a hole
    IF hoB THEN hoH := 1; END;
   ELSE
    hoB := 1;
   END;
  END;
  IF hoH THEN
   hoN := hoN + 1;
   IF hoF == 0 THEN hoF := hoJ; END;
  END;
 END;
 RETURN {hoN, hoF};
END;

// beta 1i: the rows in which every one of columns 1 .. fk holds a value
// (no blank).  For paired columns these are the complete pairs: a row
// with a blank anywhere is left out of EVERY list, so the lists still
// match row for row.  Returns the row numbers as a list.
LOCAL dd_Full(fm, fk)
BEGIN
 LOCAL fuS, fuR, fuJ, fuV, fuOK, fuL;
 fuS := dd_Shape(fm);
 fuV := dd_IsVec(fm);
 fuL := {};
 FOR fuR FROM 1 TO fuS(1) DO
  fuOK := 1;
  FOR fuJ FROM 1 TO fk DO
   IF fuOK THEN
    IF dd_Real(dd_Cell(fm, fuR, fuJ, fuV)) == 0 THEN fuOK := 0; END;
   END;
  END;
  IF fuOK THEN fuL := CONCAT(fuL, {fuR}); END;
 END;
 RETURN fuL;
END;

// beta 1i: column dj of the matrix, only at the rows listed in dr (the
// complete rows that dd_Full found), as a list.
LOCAL dd_Pick(dm, dj, dr)
BEGIN
 LOCAL dpL, dpI, dpV;
 dpV := dd_IsVec(dm);
 dpL := {};
 FOR dpI FROM 1 TO SIZE(dr) DO
  dpL := CONCAT(dpL, {dd_Cell(dm, dr(dpI), dj, dpV)});
 END;
 RETURN dpL;
END;

// beta 1i: blanks above values.  Ask how the columns go together.
// Pairs keep only the complete rows (dd_Full); separate groups leave
// each blank out of its own column (dd_Column, beta 1h's way).
// Returns 0 to stop (Cancel or Esc), 1 for separate groups, 2 for pairs.
LOCAL dd_AskHoles(ahH)
BEGIN
 LOCAL ahC, ahT;
 IF ahH(1) == 1 THEN
  ahT := "Column " + dd_Cm(STRING(ahH(2), 2, 0)) + " has a blank inside";
 ELSE
  ahT := dd_Cm(STRING(ahH(1), 2, 0)) + " columns have blanks inside";
 END;
 // CHOOSE's own return value is never tested (Lessons Learned): ahC is
 // set to 0 first, and only ahC is tested afterwards (0 = Esc).
 ahC := 0;
 CHOOSE(ahC, ahT, {"Pairs: keep complete rows", "Separate groups: drop blanks", "Cancel"});
 dd_Settle();
 IF ahC == 1 THEN RETURN 2; END;
 IF ahC == 2 THEN RETURN 1; END;
 RETURN 0;
END;
""", 'new routines')

# ---- dd_LoadCols ----
rep("""// 1. COLUMNS: column j to list j, j = 1 .. at most 9.  Returns the
// number of lists filled (0 = nothing done).
LOCAL dd_LoadCols()
BEGIN
 LOCAL lm, ls, lk, lj, ll, lrc;
""", """// 1. COLUMNS: column j to list j, j = 1 .. at most 9.  Returns the
// number of lists filled (0 = nothing done).  beta 1i: when two or more
// columns are to be loaded and any of them has a blank above a value,
// it asks first whether they are pairs (complete rows only) or
// separate groups (dd_AskHoles).
LOCAL dd_LoadCols()
BEGIN
 LOCAL lm, ls, lk, lj, ll, lrc;
 LOCAL lmo, lho, lfu;
""", 'dd_LoadCols locals')
rep(""" lrc := dd_Confirm(lk);
 IF lrc == 0 THEN RETURN 0; END;
 dd_Busy("Loading " + dd_Cm(STRING(ls(1), 2, 0)) + " rows ...");
 FOR lj FROM 1 TO lk DO
  ll := dd_Column(lm, lj);
""", """ // beta 1i: lmo = 1 leaves each blank out of its own column (separate
 // groups, and every load with no blank above a value); lmo = 2 keeps
 // only the complete rows (pairs).  One column has no partner to match,
 // so it is never asked about.
 lmo := 1; lfu := {};
 IF lk >= 2 THEN
  lho := dd_Holes(lm, lk);
  IF lho(1) > 0 THEN
   lmo := dd_AskHoles(lho);
   IF lmo == 0 THEN RETURN 0; END;
  END;
 END;
 IF lmo == 2 THEN
  lfu := dd_Full(lm, lk);
  IF SIZE(lfu) == 0 THEN
   MSGBOX("Every row of M" + dd_Cm(STRING(ddSRC, 2, 0)) + " has a blank in at least one of its columns, so there is no complete row, and nothing was loaded.");
   dd_Settle();
   RETURN 0;
  END;
 END;
 lrc := dd_Confirm(lk);
 IF lrc == 0 THEN RETURN 0; END;
 dd_Busy("Loading " + dd_Cm(STRING(ls(1), 2, 0)) + " rows ...");
 FOR lj FROM 1 TO lk DO
  IF lmo == 2 THEN
   ll := dd_Pick(lm, lj, lfu);
  ELSE
   ll := dd_Column(lm, lj);
  END;
""", 'dd_LoadCols: the question and the complete rows')
rep(""" ddLAST := ddLAST + " (" + dd_Cm(STRING(ls(1), 2, 0)) + " rows)" + dd_ClearRest(lrc);
""", """ IF lmo == 2 THEN
  ddLAST := ddLAST + " (" + dd_Cm(STRING(ls(1), 2, 0)) + " rows, " + dd_Cm(STRING(SIZE(lfu), 2, 0)) + " complete)" + dd_ClearRest(lrc);
 ELSE
  ddLAST := ddLAST + " (" + dd_Cm(STRING(ls(1), 2, 0)) + " rows)" + dd_ClearRest(lrc);
 END;
""", 'the summary line')

# ---- help: four pages ----
rep(' dd_Frame("DataLoad help 1/3: What it does");', ' dd_Frame("DataLoad help 1/4: What it does");', 'help 1')
rep(' TEXTOUT_P("Blank cells (9.99999999999E499) are left out.", G1, 8, 136, 1, ddBLK);',
    ' TEXTOUT_P("Blank cells (9.99999999999E499) are left out: see page 3.", G1, 8, 136, 1, ddBLK);', 'help 1 blank line')
rep(' dd_Frame("DataLoad help 2/3: Getting data in");', ' dd_Frame("DataLoad help 2/4: Getting data in");', 'help 2')
rep(""" TEXTOUT_P("Open Statistics 1Var once before the first load.", G1, 8, 188, 1, ddRED);
 TEXTOUT_P("any key or tap = next page", G1, 8, 222, 1, ddFOOT);
 BLIT_P(G0, 0, 0, G1);
 dd_WaitAny();
 dd_Frame("DataLoad help 3/3: Then run");
""", """ TEXTOUT_P("Open Statistics 1Var once before the first load.", G1, 8, 188, 1, ddRED);
 TEXTOUT_P("any key or tap = next page", G1, 8, 222, 1, ddFOOT);
 BLIT_P(G0, 0, 0, G1);
 dd_WaitAny();
 // beta 1i: the page on blank cells (Round 20)
 dd_Frame("DataLoad help 3/4: Blank cells");
 TEXTOUT_P("The Data Loader page writes an empty cell (or NA, N/A,", G1, 8, 30, 1, ddBLK);
 TEXTOUT_P("a dot) as 9.99999999999E499, the Prime's largest number,", G1, 8, 43, 1, ddBLK);
 TEXTOUT_P("which no data set can hold, and DataLoad leaves it out.", G1, 8, 56, 1, ddBLK);
 TEXTOUT_P("AT THE FOOT OF A COLUMN (groups of unequal sizes):", G1, 8, 74, 1, ddCOL(1));
 TEXTOUT_P("the column simply ends there, so its list is shorter.", G1, 8, 87, 1, ddBLK);
 TEXTOUT_P("ABOVE A VALUE, with two or more columns to load:", G1, 8, 105, 1, ddCOL(2));
 TEXTOUT_P("DataLoad asks first how the columns go together.", G1, 8, 118, 1, ddBLK);
 TEXTOUT_P("PAIRS (before and after, x and y, raters): only the", G1, 8, 136, 1, ddCOL(3));
 TEXTOUT_P("rows with a value in every column are kept, so each", G1, 8, 149, 1, ddBLK);
 TEXTOUT_P("pair stays a pair and the lists match row for row.", G1, 8, 162, 1, ddBLK);
 TEXTOUT_P("SEPARATE GROUPS: each column keeps all of its own", G1, 8, 180, 1, ddCOL(4));
 TEXTOUT_P("values, and its blanks are simply left out.", G1, 8, 193, 1, ddBLK);
 TEXTOUT_P("any key or tap = next page", G1, 8, 222, 1, ddFOOT);
 BLIT_P(G0, 0, 0, G1);
 dd_WaitAny();
 dd_Frame("DataLoad help 4/4: Then run");
""", 'help 3 and 4')

out = s.replace('\n', '\r\n') if CRLF else s
io.open(NEW, 'w', encoding='utf-8', newline='').write(out)
print('make_round20: %d replacements; wrote %s (%d lines)' % (n[0], os.path.relpath(NEW, ROOT), s.count('\n')))
