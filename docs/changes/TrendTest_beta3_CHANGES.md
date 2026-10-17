# TrendTest beta 2 → beta 3: least squares as calculus

*16 October 2026. Built ON TOP OF `/home/claude/work/out/TrendTest_beta2.txt` (1436 lines); every beta 2 change is kept.
Output: `/home/claude/work/out/TrendTest_beta3.txt` (1888 lines, 80.3 KB, UTF-8, LF). **Not yet run on hardware**, and
**nothing about the CAS has run on a calculator**. "b2"/"b3" = beta 2 / beta 3 line numbers. `trCompute`, `trSetX`,
`trDrawProp`, `trAnimate` and the drag `trPlotTouch` are byte-for-byte beta 2 (checked by script).*

## What the program's line is, and what the page shows (read from the code and the beta 2 CHANGES)

TrendTest's magenta line is `trB = S/Sxx`, `trA0 = P − trB·x̄` (b2 463-467): the **weighted least-squares line of the
proportions p_i = a_i/n_i on the scores x_i, weights n_i**. It minimises

  SSE(a, b) = Σ n_i (p_i − a − b x_i)²

(its normal equations are N a + (Σ n x) b = A and (Σ n x) a + (Σ n x²) b = Σ x a, whose solution is S/Sxx). The same
line is ordinary least squares on all N individual 0/1 outcomes against their scores, and the Cochran-Armitage /
Mantel trend chi-square tests whether this b is 0. Page 4 shows the **weighted** SSE, because that is what the program
computes; both equivalences were checked with statsmodels (WLS with weights n, and OLS on the expanded 0/1 data).

## (a) Every change

1. **Results page 4, "Least squares as calculus"** (new `trPage4` b3 1201). Right from page 3 (or a tap on the right
   half); internally view 6, so the two plots keep views 4 and 5 and the drag code is untouched. `trPgStep` (b3 1625)
   turns pages in the order 1, 2, 3, 4; Enter on page 4 = menu (b2 1249 → b3 trView). The page, in a blue frame:
   - "The plotted line makes this SSE smallest:" / "SSE = sum n(p - a - bx)^2; p = cases/n, x = score";
   - the SSE as the CAS put it in order (up to 3 lines, magenta), e.g. snoring:
     `SSE = 2484×a^2+6796×a×b-220×a+12310×b^2-608×b` / `+63080529409/7933174634`;
   - "Smallest where both slopes are 0 (CAS diff):", `dSSE/da = 4968×a+6796×b-220 = 0`,
     `dSSE/db = 6796×a+24620×b-608 = 0` (blue, up to 2 lines each);
   - "Solved exactly (CAS solve), beside the decimals:", `b = 95339/4757909   (program 0.02003800)`,
     `a = 80277/4757909   (program 0.01687233)` — the fraction beside the program's own `trB`/`trA0` (about seven
     significant digits, `trDec`); a fraction too long for the line says how many digits it has instead;
   - "= least squares on all N people's 0/1 outcomes;" / "the trend χ² asks whether this b is 0.";
   - for scores written over a power of ten: "Exact: score 1698.5 = 16985/10; nothing rounded.";
   - the badge "exact (CAS)" or "decimal" (dodger blue, top right); footer "4/4, ⇆ or tap = page, Esc = menu".
   **Decimal version** (the CAS did not answer; a value needs more than six decimals; or the text is too long):
   the reason in red, the two normal equations symbolically and with the program's sums (`2484 a + 3398 b = 110`,
   `3398 a + 12310 b = 304`), and "Solving them (the program's decimals):" `b = 0.02003800,  a = 0.01687233`.
2. **The CAS work** (`trCxMake` b3 1088, called from `trDrawView` when view 6 is drawn, b3 1644). The SSE is written out
   for the table on screen, `n*(a/n-tra-trb*x)^2+…`, every count and score exact via `trRat` (b3 499): a whole number,
   or a whole number over a power of ten (midrank 1698.5 → `(16985/10)`), or nothing if more than six decimals are
   needed. Four calls through `trCas`: `normal(SSE)`, `normal(diff(SSE,tra))`, `normal(diff(SSE,trb))`,
   `solve([…=0,…=0],[tra,trb])`. `trCxSol` (b3 1055) reads a and b out of `[[a,b]]`, `list[[a,b]]`, `{[a,b]}` or
   `[a=…,b=…]`. An answer with a decimal point (approximate mode) counts as no answer (`trCxClean`). The CAS is asked
   only when the SSE text differs from the one it last answered (`trCxK`): Scores, Data, Restore or a drag change it;
   paging does not. "asking the CAS ..." is written on the screen first. Never during the drag or the animation.
3. **The CAS kit** (b3 456-497): `trIStr` and `trCas`, BRIEF_CAS's shapes including the later quote-strip; the
   parameters are `trIv` and `trCs` because `trN` is TRN (transpose, case ignored) and `trS` is the trend sum S.
   Text helpers `trRatNote`, `trRepl`, `trWrap` (breaks at the shallowest bracket depth; never splits a number or
   fraction), `trCxShow` (`tra` → a, `trb` → b, `*` → ×), `trCxLines`, `trCxFrac`, `trDec`, `trNum` (no trailing zeros).
4. **Page counters** "1/3" … "3/3" → "1/4" … "3/4" (b3 887, 990, 1026); help page 2 gains "Results page 4: where the
   line comes from." (b3 1793); help page 3 says "Results: 4 pages" and describes page 4 (b3 1806-1809, lines below
   respaced by 3-5 px). Header: "beta 3 - what changed", SCREENS lists four pages, firmware line.
5. **State** (b3 263-264): `trCasOK trCasMx trCxK trCxSt trCxNt trCxE` / `trCxA trCxB trCxSa trCxSb`, set in `trInit`
   (`trCasMx` = 4000 characters).
6. **"More" soft-key page: not needed** — page 4 is a results page, reached like pages 2 and 3.

## Gate (final file)

```
=================== TrendTest_beta3.txt ===================  (bash check.sh NEW TrendTest_beta2.txt)
--- 1. kit lint (errors) ---               kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW / ORIG) --- (empty) / (empty)       (one E11 found on the way: LOCAL psI = Psi -> psJ)
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11)  none
--- 3. lint_ppl structural ---             1425 checks, 32 problems (beta 2: 1067, 8).  The 24 new ones are known
     false positives: STRING() "with 1 args" (the kit's STRING(CAS(trCs))), "with 2 args" / "4 args" (INSTRING(...)
     read as STRING(), the old MAX-in-STRING line), and "concatenates bare cxN / cxA / cxX / cfF" (those variables
     hold TEXT from trRat, not numbers).  Beta 2's 8 (entry point, EXPORT discipline, PIXON_P on dtG/dlG) unchanged.
--- 4. full parse ---  PARSE FAIL <ppl>:224 expected a name after EXPORT (file-level LOCAL after the EXPORT list)
                ORIG:  PARSE FAIL <ppl>:191 (same construct).  Masked: PARSE OK (50 functions; beta 2 34 + 16 new).
--- 5. ---  1888 lines, 80288 bytes; no non-ASCII in code
ppl_gate_v1.py: ppl_check_v3 clean (orig clean), hard errors none, lint as above.
fleet_names_v2 over the newest version of every program in out/ (27 files): 1233 routine names, 0 collisions,
  0 untagged, 0 mixed-tag, 0 built-in matches.
```

## Verification (`verify_TrendTest_beta3.py`, output in `verify_TrendTest_beta3_output.txt`: 0 failures)

```
Part A: the CAS templates in desktop Giac (icas), against fractions, SymPy and statsmodels
PASS snoring, as entered / 1,2,3 / midranks          SSE ok, d/da d/db ok, solve ok, WLS = OLS(0/1) = exact ok
      b = 95339/4757909, a = 80277/4757909 | b = 53492/1511327, a = -51775/3022654 | b = 109323/2069801372, ...
PASS sleep U (made up), three score sets             b = 1/120, a = 59/720 | 1/120, 83/720 | 17/729600, 540589/4377600
PASS convictions (made up), three score sets         b = 373/4380, a = 199/1095 | 373/4380, 141/1460 | 2639/7342500, ...
PASS scores with decimals 0.5, 1.25, 2.125, 4        b = 14173/119130, a = 24295/190608
PASS negative scores -2 .. 2                         b = 163/1921, a = 919/3842
PASS two levels with the same p (ties)               b = 1/20, a = 1/30
PASS a zero cell                                     b = 1/4, a = -1/4
PASS two levels                                      b = 9/50, a = -3/50
PASS six levels, large prime totals                  b = 608752/21894613, a = 1627669/21894613
PASS a score of 1/3 (more than six decimals): no CAS text at all
PASS the longest call (solve: the SSE twice) fits trCasMx = 4000   SSE text up to 167 characters
  ("SSE ok" = Giac's normal() minus SymPy's expanded weighted SSE simplifies to 0; "d/da d/db ok" likewise for the
   derivatives; "solve ok" = Giac's solution == the Fraction solution exactly; WLS = statsmodels WLS(p, [1,x],
   weights=n), OLS(0/1) = statsmodels OLS on all N individual outcomes, both within 1e-10 of the exact a, b.)
Part B: the PPL program in the harness (ppl_run_v3)
PASS trCxMake builds exactly this SSE text, 15 tables
PASS the PPL reads solve's answer: a and b = the exact fractions, every table
PASS the program's trB, trA0 = the exact fractions to 1e-12 (the decimals beside them)
PASS page 4 (Giac), snoring: badge, SSE, both derivatives, both fractions beside the decimals
PASS page 4: four CAS calls, all answered; no text below y 206 (the soft keys are at 218)
PASS page 4 twice: 4 CAS calls, not 8 (the answers are kept)
PASS Scores key on page 4 (twice, to midranks): asked again, exact midrank line, the 16985/10 note
PASS cas=fail: decimal badge, the normal equations with the program's sums, no error
PASS a drag on plot 1 (level 3 down): counts changed, NO CAS call during it   cases [24, 35, 9, 30]
PASS page 4 after the drag: the dragged table's exact line   b = 5825/365993 (program 0.01591560)
PASS Restore on page 4: the first table's line again
PASS a score of 1/3: "needs over 6 decimals", the decimal page, no CAS call
PASS stale-key run: menu, example, pages 1-4, Enter on page 4 = menu, quit; nothing skipped
```
A width sweep of page 4 (Giac and fail) and the help pages found no text past the screen edge (harness estimates).

## (b) DEVICE TEST CHECKLIST (least → most risky)

1. **Run CASProbe beta 1 first**, on the G2 and the G1. If it reports a call form other than `STRING(CAS(s))` (T07),
   change the IFERR line in `trCas` (b3 479) and nothing else. Note T14 (exact mode needed, else page 4 is "decimal"),
   T18 (solve), T20 (diff), T26 (IFERR catches a CAS syntax error).
2. **Paste and compile.** New names: `trIStr trCas trRat trRatNote trRepl trWrap trCxClean trCxSol trCxMake trCxShow
   trCxLines trCxFrac trDec trNum trPage4 trPgStep`.
3. **Everything beta 2 did** (its checklist 2-15) should be unchanged — the drag especially (`trPlotTouch` is byte for
   byte beta 2).
4. **Paging.** Examples → snoring. Pages read 1/4, 2/4, 3/4; Right (or a tap on the right half) from 3/4 → 4/4; Left
   from 4/4 → 3/4; Enter on 4/4 → the menu. Help pages 2 and 3 mention page 4 and fit their frames.
5. **Page 4, the CAS steps (snoring, scores as entered).** "asking the CAS ..." appears briefly — **time it on the G1**
   (four calls). Then **exact (CAS)** at the top right, and:
   `SSE = 2484×a^2+6796×a×b-220×a+12310×b^2-608×b` / `+63080529409/7933174634` (the Prime's Giac may order the terms
   differently); `dSSE/da = 4968×a+6796×b-220 = 0`; `dSSE/db = 6796×a+24620×b-608 = 0`;
   `b = 95339/4757909   (program 0.02003800)`; `a = 80277/4757909   (program 0.01687233)`. Nothing under the soft keys.
6. **Page turns cost nothing.** Left, then Right back to 4/4: no "asking the CAS" the second time.
7. **Scores key on page 4** (`+` twice → midranks): asked again; `b = 109323/2069801372   (program 0.0000528181)`,
   `a = -33598615/1574215128   (program -0.02134309)`, and "Exact: score 1698.5 = 16985/10; nothing rounded."
   (On the Prime the 1698.5 may print with the Home decimal mark; the CAS text uses no decimal point at all.)
8. **Convictions example** (scores as entered): `b = 373/4380`, `a = 199/1095`.
9. **After a drag.** Prop → drag level 3 down, Menu → Results → page 4: a new line (asked again) matching the dragged
   counts; Restore (`0`) on page 4 → snoring's fractions again.
10. **CAS in approximate mode** (CAS settings, uncheck Exact), page 4 again after changing the scores: "decimal", the
    normal equations `2484 a + 3398 b = 110` / `3398 a + 12310 b = 304`, "b = 0.02003800,  a = 0.01687233", no error.
    Restore Exact.
11. **Home number format Fixed 2**: page 4 must be unchanged (all CAS text is built by `trIStr`). Restore Standard.

## (c) Not confirmed, left as it was

- **Nothing about the CAS has run on a Prime.** `normal`, `diff`, a two-equation `solve` with list arguments and the
  answer's printed form are desktop Giac 1.9's. CASProbe tests a one-equation `solve` (T18) and `diff` (T20), not
  `normal` nor `solve([e1,e2],[a,b])`. `trCxSol` accepts `[[a,b]]`, `list[[a,b]]`, `{[a,b]}` and `[a=…,b=…]`, with
  `,` or `;` between them; any other shape falls back to "decimal".
- **List separators under a comma decimal mark (HSeparator)**: exact answers contain no decimal point, but if the Prime
  writes the solution list with `;` that is handled; anything else falls back.
- **Speed on a G1** of four calls (desktop: 30-40 ms each).
- **Font-1 widths** are estimates (49 characters a line); the longest page-4 lines are 48-49 characters.
- The equivalence "= least squares on all N people's 0/1 outcomes" was verified (statsmodels OLS on the expanded data,
  15 tables); it is stated on the page without derivation.
- Everything in beta 2's "not confirmed" list still stands (drag frame rate, MOUSE sampling, DRAWMENU repaint per drag
  frame, MAKELIST's Home K in `trEnter`, the STRING lint false positive, widths, made-up examples).
