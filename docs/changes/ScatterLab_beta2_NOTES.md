# ScatterLab beta 2 — notes (changes from beta 1)

*16 October 2026. Built ON TOP OF `/home/claude/work/out/ScatterLab_beta1.txt` (1525 lines); every beta 1 feature is
kept. Output: `/home/claude/work/out/ScatterLab_beta2.txt` (1972 lines, 75.0 KB, ASCII code, LF). **Not yet run on
hardware** (nor was beta 1), and **nothing about the CAS has run on a calculator**. "b1"/"b2" = beta 1 / beta 2 line
numbers. `slFit`, `slGuessFit`, `slDraw`, `slNear` and both drags (`slDragPt`, `slDragH`) are byte-for-byte beta 1.*

Files: `ScatterLab_beta2.txt`, `scatterlab-guide_beta2.md` (the guide), `verify_ScatterLab_beta2.py` (+ `_output.txt`),
this file. (Beta 1's NOTES describe everything else and still hold.)

## 1 · Every change

1. **Least squares as calculus, a page of its own** (new `slCxDraw` b2 1508, `slCxPage` 1570). Opened from **Menu >
   Least squares as calculus** (new item 5) or a **tap on the equation in the panel** (x ≥ 226, y 60-92, outside
   Guess mode: b2 1786). It needs a line (3 points, two different x); otherwise the note line says "Least squares needs
   3 points with different x." and no page opens. Drawn like a help page (whole screen, magenta frame), held by
   `slWaitAny` (any key or tap = back to the plot). Example data:
   - "The magenta line makes this SSE smallest:" / "SSE = sum (y - a - bx)^2 over all n = 16 points";
   - `SSE = 16×a^2+2608/5×a×b-5321/5×a+119443/25×b^2` / `-36841/2×b+373319/20` (orange, as the SSE in the panel);
   - "Smallest where both slopes are 0 (CAS diff):", `dSSE/da = 32×a+2608/5×b-5321/5 = 0`,
     `dSSE/db = 2608/5×a+238886/25×b-36841/2 = 0` (blue);
   - "Solved exactly (CAS solve), beside the decimals:", `b = 2441/2394   (program 1.019632)`,
     `a = 3186173/191520   (program 16.63624)` (magenta; the decimals are `slB1`, `slB0`);
   - "No line has a smaller SSE (try Guess), and the" / "first equation puts it through the green cross:" /
     "a = y-bar - b x̄."; "Exact: x = 10.4 is 104/10, so nothing is rounded."; the badge "exact (CAS)" / "decimal".
   **Decimal version** (the CAS did not answer; a value needs more than six decimals; too long to send): the reason in
   red, the two normal equations symbolically and with the program's sums (`16 a + 260.8 b = 532.1`,
   `260.8 a + 4777.72 b = 9210.25`), and "Solving them (the program's decimals):" `b = 1.019632,  a = 16.63624`.
2. **The CAS work** (`slCxMake` b2 1396). The SSE `(y-sla-slb*x)^2+…` is written for the points on the plot, every
   value exact via `slRat` (b2 334): a whole number, or a whole number over a power of ten (10.4 → `(104/10)`), or
   nothing when more than six decimals are needed (a typed 1/3, data from C1/C2). Four calls through `slCas`:
   `normal(SSE)`, `normal(diff(SSE,sla))`, `normal(diff(SSE,slb))`, `solve([…=0,…=0],[sla,slb])`; `slCxSol` reads
   a, b out of `[[a,b]]`, `list[[a,b]]`, `{[a,b]}` or `[a=…,b=…]`; an answer with a decimal point counts as none. The
   CAS is asked only when the SSE text differs from the one it last answered (`slCxK`): a tap, drag, delete, typed or
   loaded point changes it. "asking the CAS ..." is written on the screen first. Never during a drag.
3. **The CAS kit** (b2 291-332): `slIStr` and `slCas`, BRIEF_CAS's shapes including the later quote-strip. The
   whole-number routine's parameter is `slIv` because `slN` is the number of points. Text helpers `slRatNote`,
   `slRepl`, `slWrap` (breaks at the shallowest bracket depth; never splits a number or fraction), `slCxShow`
   (`sla` → a, `slb` → b, `*` → ×), `slCxLines`, `slCxFrac`, `slDec`, `slNum`.
4. **Menu** (b1 1287 → b2 1721): ten items, "Least squares as calculus" fifth; Data, Type, Delete, Help and Quit move
   down one (Help 9, Quit A on the Prime). No help text quoted a menu number, so nothing else had to change.
5. **Help** page 3 ends "Menu > Least squares as calculus: the derivation." (y 201); page 6 ends "Tap the equation:
   least squares as calculus." (y 198).
6. **State** (b2 206-207): `slCasOK slCasMx slCxK slCxSt slCxNt slCxE` / `slCxA slCxB slCxSa slCxSb`, set in `slInit`
   (`slCasMx` = 4000 characters). Header: "What changed in beta 2", firmware line.
7. **"More" soft-key page: not needed.** The six soft keys are unchanged; the page has a menu item (keys) and a tap
   target (touch).

## 2 · Decisions you may want to change

1. **Fractions, not scaled integers.** Each decimal goes to the CAS as an exact ratio (10.4 = 104/10), so a and b come
   out in the data's own units and nothing has to be "unscaled"; the page's last line says how one value was written.
   The alternative (multiply x and y by 10^d, solve, divide back) gives integer coefficients but adds a step to explain.
2. **Six decimals at most.** A value needing more (1/3) gives the decimal page; raising the limit lengthens the CAS text.
3. **The panel tap** works only outside Guess mode (in Guess the panel shows the student's own line).
4. **The page has no soft keys**, like the help pages: it is something to read, and any key returns.

## 3 · Gate (final file)

```
=================== ScatterLab_beta2.txt ===================  (bash check.sh NEW ScatterLab_beta1.txt)
--- 1. kit lint (errors) ---               kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW / ORIG) --- (empty) / (empty)
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11)  none
--- 3. lint_ppl structural ---             1262 checks, 29 problems (beta 1: 910, 6).  The 23 new ones are known
     false positives: STRING() "with 1 args" (the kit's STRING(CAS(slS))), "with 2 / 4 args" (INSTRING(...) read as
     STRING()), and "concatenates bare cxX / cxY / cfF" (those variables hold TEXT from slRat).  Beta 1's 6 unchanged.
--- 4. full parse ---  PARSE FAIL <ppl>:152 expected a name after EXPORT (file-level LOCAL after the EXPORT lists)
                ORIG:  PARSE FAIL <ppl>:124 (same construct).  Masked: PARSE OK (64 functions; beta 1 48 + 16 new).
--- 5. ---  1972 lines, 74952 bytes; no non-ASCII in code
ppl_gate_v1.py NEW ORIG: RESULT: PASS (ppl_check_v3 clean, lint as above; its kit steps skip here).
fleet_names_v2 over the newest version of every program in out/ (27 files): 1233 routine names, 0 collisions,
  0 untagged, 0 mixed-tag, 0 built-in matches.
```

## 4 · Verification (`python3 verify_ScatterLab_beta2.py` — 0 failures; output in `verify_ScatterLab_beta2_output.txt`)

```
Part A: the CAS templates in desktop Giac (icas), against fractions, SymPy and statsmodels
PASS SYNTHETIC example (16 points, 1 decimal)   SSE ok, d/da d/db ok, solve ok, OLS = polyfit = exact ok   b = 2441/2394, a = 3186173/191520
PASS integers, tied x                           ... b = 73/52, a = 14/13
PASS two decimals                               ... b = 165503/209298, a = 17541923/3488300
PASS negative values                            ... b = 26353/11890, a = -3283/11890
PASS years against crime-sized counts           ... b = 6701/650, a = -5243866/325
PASS n = 3                                      ... b = 12/7, a = 0
PASS forty points, one decimal                  ... b = 9683220/11837191, a = -72190339/118371910
PASS a perfect line y = 2x + 1 (SSE 0)          ... b = 2, a = 1
PASS flat: every y equal                        ... b = 0, a = 5
PASS three decimals                             ... b = 9661/6625, a = 5446/6625
PASS mixed precision                            ... b = -541/444, a = 14045/1184
PASS a point at y = 1/3 (more than six decimals): no CAS text at all
PASS the longest call (solve: the SSE twice) fits slCasMx = 4000   SSE text up to 1104 characters (forty points)
  ("SSE ok" = Giac's normal() minus SymPy's expanded SSE simplifies to 0; likewise both derivatives; "solve ok" =
   Giac's solution == the Fraction solution exactly; statsmodels OLS and numpy polyfit within 1e-10 of it.)
Part B: the PPL program in the harness (ppl_run_v3)
PASS slCxMake builds exactly this SSE text, 11 data sets
PASS the PPL reads solve's answer: a and b = the exact fractions, every set
PASS the program's slB1, slB0 = the exact fractions to 1e-12
PASS panel tap -> the page (Giac): badge, SSE, derivatives, fractions beside the decimals, the note
PASS the page: four CAS calls, all answered; the run ends normally
PASS cas=fail: decimal badge, the normal equations with the program's sums, no error
PASS Menu > Least squares as calculus, twice: 4 CAS calls, not 8
PASS the menu has ten items, the new one fifth
PASS a drag of point 1 (down 30 px): it moved; 8 CAS calls in all = 4 per page, none in the drag
PASS the page after the drag: the moved points' exact line   b = 57655/52668 (program 1.094687)
PASS slCas drops one surrounding pair of quotes: the quoted answers still give the exact page
PASS two points: no page, the note says why, no CAS call
PASS a point at y = 1/3: "needs over 6 decimals", the decimal page, no CAS call
PASS stale-key run: menu, Data, example, the page, quit (item A); nothing skipped
```
A width sweep of the page (Giac and fail) and the help pages found no text past the screen edge (harness estimates).

## 5 · Device test checklist — least risky first

1. **Run CASProbe beta 1 first**, on the G2 and the G1. If it reports a call form other than `STRING(CAS(s))` (T07),
   change the IFERR line in `slCas` (b2 314) and nothing else. Note T14 (exact mode, else the page is "decimal"), T18
   (solve), T20 (diff), T26 (IFERR catches a CAS syntax error).
2. **Paste and compile**; run `ScatterLab()`. Everything in beta 1's checklist (1-15) should be unchanged — the drag
   especially (`slDragPt` is byte for byte beta 1).
3. **Menu**: ten items, "Least squares as calculus" fifth, Help 9, Quit shown as A. With fewer than 3 points, item 5
   closes the menu and the note reads "Least squares needs 3 points with different x."
4. **Help pages 3 and 6**: the new last lines fit above the footer.
5. **The page, the CAS steps.** Data → Poverty vs crime; tap the equation in the panel (y-hat = 16.64 / + 1.020 x).
   "asking the CAS ..." briefly — **time it on the G1** (four calls, 16 points). Then **exact (CAS)** and the lines in
   §1 item 1 above: `SSE = 16×a^2+2608/5×a×b-5321/5×a+119443/25×b^2` / `-36841/2×b+373319/20` (term order may differ
   on the Prime), `dSSE/da = 32×a+2608/5×b-5321/5 = 0`, `dSSE/db = 2608/5×a+238886/25×b-36841/2 = 0`,
   `b = 2441/2394   (program 1.019632)`, `a = 3186173/191520   (program 16.63624)`, "Exact: x = 10.4 is 104/10 …".
   Any key back to the plot.
6. **Cached.** Open the page again (Menu item 5): no "asking the CAS".
7. **After a drag.** Drag a point, open the page: asked again, a new pair of fractions, and its decimals match the
   panel's y-hat line.
8. **Forty points** (tap them in, or load C1/C2): the page still opens (SSE text about 1,100 characters, sent twice in
   the solve call) — watch the time on the G1.
9. **A 1/3 point**: Menu → Type a point, y = 1/3 → the page shows "A value needs over 6 decimals" and the decimal
   normal equations, no CAS call.
10. **CAS in approximate mode** (uncheck Exact in the CAS settings), page again after moving a point: "decimal", the
    normal equations with the sums, no error. Restore Exact.
11. **Home number format Fixed 2**: the page must be unchanged (all CAS text is built by `slIStr`). Restore Standard.

## 6 · Not confirmed — stated plainly

- **Nothing about the CAS has run on a Prime.** `normal`, `diff`, the two-equation `solve` and the answer's printed form
  are desktop Giac 1.9's; CASProbe tests a one-equation `solve` and `diff`, not `normal` or `solve([e1,e2],[a,b])`, nor
  2-3 KB inputs (forty points). If long inputs fail, lower `slCasMx` in `slInit`.
- **List separators under a comma decimal mark**: `,` and `;` are handled; any other solve shape gives "decimal".
- **Speed on a G1** (desktop: 30-45 ms per call).
- **Text widths** are estimates (49 characters a line); the page's longest lines are 48-49 characters.
- Everything in beta 1's §6 still stands (drag frame rate, C1/C2 writes and the IFERR path, DRAWMENU per drag sample,
  widths, the 2Var wording).
