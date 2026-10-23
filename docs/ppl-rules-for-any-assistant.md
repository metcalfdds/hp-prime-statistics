# HP Prime PPL: the rules, condensed for any AI assistant

*A 2,500-word distillation of `lessons-learned` (currently v7q) for a model with a small context window. Flat rules, no history, no evidence; the long document has both. Every rule here was found on an HP Prime G1 or G2 running the 2026-09-09 firmware, or on HP's Virtual Calculator of the same build. Roger Metcalf, 2026; written with AI assistance (Anthropic Claude).*

**How to use this file with a model.** Put the whole file in the system prompt. Set the context length to at least 32,768 tokens and, for a reasoning model, the output budget to at least 16,384. Ask for one small program at a time. Run `tools/ppl_gate_v1c.py` on what comes back and paste the error lines into the next turn. The example at the end passes the gate; ask the model to imitate it.

## 1. What PPL is and is not

- PPL is the HP Prime's own language. It is **not** Python, TI-BASIC or BASIC. Blocks are `BEGIN … END;`, `IF … THEN … ELSE … END;`, `FOR i FROM a TO b DO … END;`, `WHILE … DO … END;`, `REPEAT … UNTIL …;`, `CASE IF … THEN … END; … DEFAULT … END;`. Every statement ends with `;`. Assignment is `:=`. Equality test is `==`. Not-equal is `<>`. Comments are `//` to end of line.
- A program file holds one or more routines. `EXPORT Name()` makes a routine appear in the program catalog; helpers are declared without `EXPORT`. Every routine in every program on the calculator shares one name pool, matched ignoring case, so helper names must be unique across programs: prefix them (`tbCalc`, `tbShow`).
- Reals carry 12 significant digits. There is no integer type. Lists are `{1, 2, 3}`, indexed from 1, `L(2)`. Strings are `"…"`, `DIM(s)` is the length, `+` concatenates, `MID`, `LEFT`, `RIGHT`, `INSTRING` are the tools.
- Use PPL for everything that draws or reacts to keys. Use MicroPython only for a compute-heavy engine that needs a real speed-up, and keep a pure-PPL fallback (section 8). Use the CAS only for exact or symbolic text, behind a guard (section 9).

## 2. Structure and syntax that the Prime rejects

- At most **16 arguments** on any routine or built-in call. Pack more into a list.
- `LOCAL` lines carry at most **6 names**. Split longer lists across several `LOCAL` lines.
- `LOCAL` is **only allowed at the top of a routine**, before any statement. A `LOCAL` inside `IF`, `FOR` or `CASE` is a syntax error. Declare at the top, assign later.
- A routine **cannot change its caller's variables**: parameters pass by value. State shared between routines lives in file-level variables declared with `LOCAL` after the `EXPORT` line, or in `EXPORT`ed globals.
- **Never write a `//` comment inside an open bracket**, such as inside a multi-line `CHOOSE` list or a `{ … }` list. The editor reports a syntax error at the closing bracket.
- Write exponents with a capital `E`: `1E10`, `-1E10`. Lowercase `e` is a reserved name.
- `FOR i FROM 2 TO 1 DO … END;` runs zero times, which is fine; `STEP` is a keyword, so `FOR … STEP 4` is the only place it may appear.
- Keep executable code ASCII. Symbols belong in strings and comments only. Write π as `3.14159265359`.
- Distribute programs as plain `.txt` files pasted into the HP Connectivity Kit's program editor. Never rename a `.txt` to `.hpprgm`; that format is binary.

## 3. Names

- A name must not match a **built-in command or function, ignoring case**. `csC` is a syntax error because `CSC` is the cosecant; `ans`, `ci`, `fp`, `ip`, `ln`, `re`, `im`, `sign`, `e`, `i`, `x`, `K`, `G1` to `G9` are all taken. Check every new name against the built-in list (`tools/HP_Prime_Builtin_Names.txt`).
- A parameter name is checked more strictly than a `LOCAL`: `fp` fails as a parameter even where `LOCAL fp` parses.
- Avoid bare single-letter lowercase names altogether: `x` is the CAS variable, `i` the imaginary unit, `e` the constant.
- Prefix every helper routine with a two- to four-letter tag for the program (`tbShow`, `cs_Grid`, `sr_SRCDF`; letters only, the fleet checker reads `tb` or `cs_` as the tag), and every local with a tag for its routine (`shX`, `drT`), so names never collide and greps are easy.
- Never use `K`, `X`, `A` to `Z` as loop or `MAKELIST` counters; they are Home's variables and the program overwrites them. Use a `LOCAL`.

## 4. Numbers and built-ins

- `STRING(value, 2, d)` prints `d` fixed decimals. Mode 1 ignores `d`. A value below 10^(-d) in mode 2 prints in scientific form, so print a tiny p as `"p < 0.0001"` instead of letting it switch.
- `ROUND(x, d)` rounds halves away from zero. `IP`, `FP`, `FLOOR`, `CEILING` exist. `x^0.5` is the square root to use in code (the √ sign is not ASCII).
- **Never compute an upper tail as `1 - CDF`**: with 12 digits the difference is exactly 0 once the tail is below about 5E-13. Normal upper tail: `NORMALD_CDF(m, s, 2*m - t)`. Chi-square with 1 df: `2*NORMALD_CDF(0, 1, -(x^0.5))`; with 2 df: `EXP(-x/2)`; with more df, the finite sum of positive terms (even df: `EXP(-x/2)` times `1 + h + h^2/2! + …` with `h = x/2`; odd df: `2*NORMALD_CDF(0,1,-(x^0.5)) + (2*x/3.14159265359)^0.5 * EXP(-x/2) * (1 + x/3 + x^2/15 + …)`). A right-tail quantile is `-NORMALD_ICDF(0, 1, alpha)`, not `NORMALD_ICDF(0, 1, 1 - alpha)`.
- Build probabilities from **positive terms**; an alternating sum loses all its digits when the answer is small.
- `CHISQUARE(df, x)` is the **density**, not a tail. `CHISQUARE_CDF`, `CHISQUARE_ICDF`, `FISHER_CDF`, `FISHER_ICDF` accept **whole-number df only**.
- `BINOMIAL(n, p, k)` and `BINOMIAL_CDF(n, p, k)` take (n, p, k) in that order; HP's own manual prints it wrong. `POISSON_CDF(lambda, k)` with k < 0 is an error, not 0.
- `NORMALD_ICDF(0, 1, 1)` and an overflow return infinity, not an error, and `IFERR` does not see it. Clamp probabilities inside (0, 1) before an inverse CDF.
- Available and reliable: `NORMALD`, `NORMALD_CDF`, `NORMALD_ICDF`, `STUDENT`, `STUDENT_CDF`, `STUDENT_ICDF`, `FISHER`, `FISHER_CDF`, `BINOMIAL`, `BINOMIAL_CDF`, `POISSON`, `POISSON_CDF`, `COMB`, `IFTE`, `MAKELIST`, `CONCAT`, `RANDOM`, `RANDINT`, `MAX`, `MIN`, `SORT`, `MAKEMAT`, `TICKS` (milliseconds, no parentheses).
- Not available: `GEOMETRIC*` (compute `p*(1-p)^(k-1)` by hand), `LNGAMMA` outside the CAS (carry a Lanczos helper).
- `INSTRING(s, sub)` with `s = ""` is a **run-time error**. Guard every call: `IF DIM(s) > 0 THEN … END;`. `INSTRING("abc", "")` returns 1, so an empty search string loops forever in a replace routine; guard that too.
- `LEFT(s, 0)` and `RIGHT(s, 0)` return the **whole string**, not `""`. Guard a count that can be 0.
- `AND` and `OR` stop evaluating once the left side decides, so `DIM(s) > 0 AND INSTRING(s, "a") > 0` is safe.
- A trailing-zero stripper must check that the string contains a `.` first; `STRING(140000000000, 2, 1)` has none.

## 5. Input and dialogs

- `INPUT({v1, v2}, "Title", {"label 1", "label 2"}, {"help 1", "help 2"}, {default 1, default 2})`. The first argument is a list of **variable names**, which `INPUT` writes back in place. Value lists give "Invalid Input". `INPUT` returns 0 when the user cancels: test it and return.
- **Never `INPUT` into a routine parameter**; it fails silently. Copy to a `LOCAL`, `INPUT` that.
- There is no blank input field: a real always shows a value. Default to 0 unless 0 is illegal for the field (a confidence level defaults to 0.95, an alpha to 0.05).
- `CHOOSE(idx, "Title", {"item 1", "item 2", …})` is the list form and takes any number of items; the simple form stops at 14. `CHOOSE` numbers the items itself (1 to 9, then A, B, C), so do not number them in the strings. Set `idx := 0` before the call and test `idx` afterwards; Cancel leaves it 0. Never test `CHOOSE`'s return value for a specific number.
- `MSGBOX(text)` shows **5 lines**; the rest is lost. Longer output goes on a screen of your own. `MSGBOX(text, 1)` shows OK and Cancel and returns 1 or 0.
- A guard message should teach: say what was wrong with the value and what would be right.

## 6. Screens and graphics

- The screen is 320 × 240, origin top left, y increasing **downward**. Fonts: `TEXTOUT_P(text, G, x, y, font, colour)` with font 1 (small), 2 (medium), 3 (large); it returns the x just past the text. Colours are `RGB(r, g, b)`; write `#FFFFFFh`-style literals only in strings or not at all.
- **Compose off screen, blit once.** `DIMGROB_P(G1, 320, 240, RGB(255,255,255));` then draw every element to `G1`, then `BLIT_P(G0, 0, 0, G1);`. Drawing straight to `G0` tears.
- `RECT_P(G, x1, y1, x2, y2, edge, fill)`, `LINE_P(G, x1, y1, x2, y2, colour)`, `PIXON_P(G, x, y, colour)`, `ARC_P(G, x, y, r, colour)`. No dotted lines: draw them with `PIXON_P` in a `STEP 4` loop. Concentric `ARC_P` rings do not make a solid disc; use `FILLPOLY_P` or a small filled `RECT_P`.
- Soft keys: `DRAWMENU({"Edit", "Run", "", "", "", "Quit"})` after the blit; it paints the bottom strip itself. The six slots are 53 pixels wide; a tap at x lands in slot `IP(x/53.4) + 1`.
- Shade a region by iterating **pixel columns**, not sample points, or gaps appear. Cache a curve's heights once per frame if two passes need them.
- Axis ticks: step 1, 2 or 5 times a power of ten; first tick `CEILING(xmin/stp)*stp`. Fit both axes before drawing a reference curve.
- Keep every text line 14 pixels apart at font 2; check that nothing overlaps at the right edge (about 7.5 pixels per character at font 2 on average).

## 7. Waiting for a key or a touch

- `GETKEY` returns -1 when no key is down. Reliable codes: Esc 4, Up 2, Down 12, Left 7, Right 8, Enter 30, Plus 50, Minus 45, 0 42. Route anything else through a `CHOOSE` menu.
- `UNTIL k == -1` drains; `UNTIL k > -1` waits. They look alike and do opposite things.
- **Drain, wait, drain**, because the key that closed an `INPUT` or `CHOOSE` is still in the buffer and would skip the screen you just drew:
  ```
  REPEAT k := GETKEY; UNTIL k == -1;    // drain the stale key
  REPEAT k := GETKEY; UNTIL k > -1;     // wait for a real one
  REPEAT k := GETKEY; UNTIL k == -1;    // drain it
  ```
- `FREEZE` is not a pause; it only holds the screen when the program ends. `WAIT(n)` waits n seconds; `WAIT(-1)` blocks until a key or a touch and returns a key code or a list.
- Touch with `MOUSE`: `m := MOUSE; IF SIZE(m(1)) > 0 THEN x := m(1,1); y := m(1,2); END;`. Poll keys and touch in one loop: `REPEAT k := GETKEY; m := MOUSE; UNTIL k > -1 OR SIZE(m(1)) > 0;`. After handling a touch, wait for the finger to lift with a time limit: `t := TICKS; REPEAT UNTIL MOUSE(1) == -1 OR TICKS - t > 1000;`.
- `WAIT(-1)` touch lists are `{type, x, y}` with type 0 press, 1 drag, 2 lift (may be `{2}` alone, so check `SIZE` before reading x and y), 3 click (a soft-key tap arrives only as type 3). Compare `TYPE(kk) == 6` to tell a list from a key code.
- The footer must say only what the keys really do on that screen. End a program with `RETURN`, not `PRINT`, unless there is Terminal output to scroll.

## 8. MicroPython inside a program

- The interpreter is **MicroPython 1.9.4**, tracking CPython 3.4. No f-strings, no `random` module (use `urandom`), no `time` (use `eval('ticks()')`), no `os`, no `fsum`, `isclose`, `factorial`, `comb`. `math` has `erf`, `erfc`, `lgamma`, `gamma`.
- Embed it as `#PYTHON name … #END` in the program file, called by a PPL wrapper `PYTHON(name)`. Pass only small integers or short text as arguments: they arrive in `sys.argv` as display-formatted strings (`'−2.5'` with a Unicode minus, `'1ᴇ20'`), which `float()` rejects. Read real numbers and lists from PPL globals with `hpprime.eval("name")`; write back with `hpprime.eval('NAME:=' + "%.6f" % x)`. Never use `repr()` on a float crossing the bridge.
- **A Python exception does not raise a PPL error.** `IFERR` around `PYTHON(…)` catches nothing; the program carries on with whatever the output variable held. So: clear the output variable before the call, validate by using the result inside `IFERR` afterwards, and always carry a pure-PPL fallback. Report on screen which engine answered.
- A top-level `import` of a missing module, a quote inside a string concatenated into `eval`, or a PPL list containing a string handed raw to Python, each close the app with no message.
- `matplotl` is unusable for charts; draw with PPL `_P` commands or `hpprime`'s `line`, `fillrect`, `pixon`.

## 9. The CAS, behind a guard

- Call it through one routine: `IFERR r := STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")")); THEN r := ""; END;`. Strip the surrounding quotes. Treat an answer containing `undef`, `rror` or the ∞ character as a failure and fall back to the PPL number. Test the answer only when `DIM(r) > 0`.
- Build CAS text from **integers only**: write 0.95 as `95/100`. Home's `STRING(-2.5)` carries a Unicode minus the CAS may not read.
- CAS variables persist for the student. Use tagged names (`ctq`), never `x`, `n`, `p`, `k`, `t`, and never assign them.
- Call the CAS on events (a page opens, a value changes), never on every frame, and cache the text. Numbers for arithmetic come from PPL; the CAS supplies display text.

## 10. Style

- On screen, write the symbol, not its name: χ² is `CHAR(967) + CHAR(178)`, √ `CHAR(8730)`, ≥ ≤ ≠ `CHAR(8805)`, `CHAR(8804)`, `CHAR(8800)`, ± `CHAR(177)`, × `CHAR(215)`, → `CHAR(8594)`, ∞ `CHAR(8734)`, μ σ θ ρ λ `CHAR(956)`, `CHAR(963)`, `CHAR(952)`, `CHAR(961)`, `CHAR(955)`, subscript ₀ ₁ ₂ `CHAR(8320)` to `CHAR(8322)`, x̄ `CHAR(57344)`, p̂ `CHAR(57345)`.
- Spaces round `=`: `"p = 0.0432"`. A tiny p prints as `"p < 0.0001"`, never `"p = < 0.0001"` and never `"p = 0"`.
- Every program starts with a comment header: name and version, one line on what it does, the author, the licence line, and what has and has not been tested on a calculator.
- Version by letter (`beta 3e` to `beta 3f`); never change a file silently.

## 11. Before delivering a program

1. Every new name checked against keywords and built-ins, ignoring case; every helper carries the program's letter tag.
2. Every `LOCAL` at the top of its routine, 6 names a line.
3. No comment inside a bracket; no lowercase `e` exponent; code ASCII.
4. Every `INSTRING` guarded; every `INPUT` target a variable; every `CHOOSE` index reset to 0 first.
5. No `1 - CDF`; probabilities clamped before an inverse CDF.
6. Draw to `G1`, blit once; drain, wait, drain.
7. The formulas checked against SciPy or a textbook example before the program is pasted.
8. `python3 ppl_gate_v1c.py Program.txt` passes.

## 12. A complete example that passes the gate

A 2 × 2 table analyzer: one `INPUT` form, the chi-square with and without Yates's correction, the odds ratio with its 95% interval, a result screen, and a clean exit.

```
// ============================================================
// TBL2X2 - version 1
// Chi-square and odds ratio for a 2 x 2 table (a b / c d)
// ============================================================
// Author: Roger Metcalf, 2026. Written with AI assistance (Anthropic
//   Claude). Free for educational and personal use; no warranty.
// Tested in the PC harness (ppl_run_v3e); not yet on a calculator.

EXPORT TBL2X2()
BEGIN
  LOCAL tbA, tbB, tbC, tbD, tbOK, tbR1;
  LOCAL tbR2, tbC1, tbC2, tbN, tbX2, tbYt;
  tbA := 10; tbB := 20; tbC := 30; tbD := 15;
  tbOK := INPUT({tbA, tbB, tbC, tbD}, "2 x 2 table",
                {"a", "b", "c", "d"},
                {"row 1, column 1", "row 1, column 2", "row 2, column 1", "row 2, column 2"},
                {10, 20, 30, 15});
  IF tbOK == 0 THEN RETURN; END;                       // Cancel
  IF MIN(tbA, tbB, tbC, tbD) < 0 THEN
    MSGBOX("Counts cannot be negative."); RETURN;
  END;
  tbR1 := tbA + tbB; tbR2 := tbC + tbD;
  tbC1 := tbA + tbC; tbC2 := tbB + tbD;
  tbN := tbR1 + tbR2;
  IF MIN(tbR1, tbR2, tbC1, tbC2) == 0 THEN
    MSGBOX("A row or column total is 0: the chi-square is undefined."); RETURN;
  END;
  // Pearson chi-square and Yates's correction, 1 df
  tbX2 := tbN * (tbA * tbD - tbB * tbC)^2 / (tbR1 * tbR2 * tbC1 * tbC2);
  tbYt := tbN * MAX(0, ABS(tbA * tbD - tbB * tbC) - tbN / 2)^2 / (tbR1 * tbR2 * tbC1 * tbC2);
  tbShow(tbA, tbB, tbC, tbD, tbX2, tbYt);
END;

// the upper tail of chi-square with 1 df, as a lower normal tail:
// it keeps its digits where 1 - CHISQUARE_CDF would be exactly 0
tbPVal(pvX)
BEGIN
  RETURN 2 * NORMALD_CDF(0, 1, -(pvX^0.5));
END;

// p as text: four decimals, or "< 0.0001"
tbPStr(psP)
BEGIN
  IF psP < 0.0001 THEN RETURN "p < 0.0001"; END;
  RETURN "p = " + STRING(psP, 2, 4);
END;

tbShow(shA, shB, shC, shD, shX2, shYt)
BEGIN
  LOCAL shOR, shSE, shLo, shHi, shY, shK;
  LOCAL shH;
  // odds ratio with Woolf's interval; 0.5 added to every cell if one is 0
  shH := 0;
  IF MIN(shA, shB, shC, shD) == 0 THEN shH := 0.5; END;
  shOR := (shA + shH) * (shD + shH) / ((shB + shH) * (shC + shH));
  shSE := (1 / (shA + shH) + 1 / (shB + shH) + 1 / (shC + shH) + 1 / (shD + shH))^0.5;
  shLo := shOR * EXP(-1.959964 * shSE);
  shHi := shOR * EXP(1.959964 * shSE);
  DIMGROB_P(G1, 320, 240, RGB(255, 255, 255));
  TEXTOUT_P("2 x 2 table", G1, 10, 6, 3, RGB(0, 0, 160));
  shY := 34;
  TEXTOUT_P("a = " + STRING(shA, 2, 0) + "   b = " + STRING(shB, 2, 0), G1, 10, shY, 2, RGB(0, 0, 0)); shY := shY + 16;
  TEXTOUT_P("c = " + STRING(shC, 2, 0) + "   d = " + STRING(shD, 2, 0), G1, 10, shY, 2, RGB(0, 0, 0)); shY := shY + 24;
  TEXTOUT_P(CHAR(967) + CHAR(178) + " = " + STRING(shX2, 2, 3) + " (1 df),  " + tbPStr(tbPVal(shX2)), G1, 10, shY, 2, RGB(0, 0, 0)); shY := shY + 16;
  TEXTOUT_P("Yates " + CHAR(967) + CHAR(178) + " = " + STRING(shYt, 2, 3) + ",  " + tbPStr(tbPVal(shYt)), G1, 10, shY, 2, RGB(0, 0, 0)); shY := shY + 24;
  TEXTOUT_P("Odds ratio = " + STRING(shOR, 2, 3), G1, 10, shY, 2, RGB(0, 0, 0)); shY := shY + 16;
  TEXTOUT_P("95% CI " + STRING(shLo, 2, 3) + " to " + STRING(shHi, 2, 3), G1, 10, shY, 2, RGB(0, 0, 0)); shY := shY + 16;
  IF shH > 0 THEN
    TEXTOUT_P("(0.5 added to every cell: a cell was 0)", G1, 10, shY, 1, RGB(120, 120, 120));
  END;
  TEXTOUT_P("Any key: quit", G1, 10, 222, 1, RGB(120, 120, 120));
  BLIT_P(G0, 0, 0, G1);
  REPEAT shK := GETKEY; UNTIL shK == -1;             // drain the key that closed INPUT
  REPEAT shK := GETKEY; UNTIL shK > -1;              // wait
  REPEAT shK := GETKEY; UNTIL shK == -1;             // drain it
END;
```
