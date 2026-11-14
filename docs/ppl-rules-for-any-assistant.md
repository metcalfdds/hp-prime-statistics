# HP Prime PPL: the rules, condensed for any AI assistant

*Version 2, 14 November 2026: a distillation of the Lessons Learned (`docs/lessons-learned_v7zs.md`) for a model with a small context window: about 4,000 words of rules and a short example program. Flat rules, no history, no evidence; the long document has both. Every rule here was found on an HP Prime G1 or G2 running the 2026-09-09 firmware, or on HP's Virtual Calculator of the same build. Version 1 (5 November 2026) was made from v7q; version 2 adds what the Lessons Learned found from v7r to v7zs: number-only input fields, the limits of `STRING` and `STUDENT_CDF`, the second-pass standard deviation, the built-in apps' lists, more on touch and on the Python bridge, and an example that follows them. Roger Metcalf, 2026; written with AI assistance (Anthropic Claude).*

**How to use this file with a model.** Put the whole file in the system prompt. Set the context length to at least 32,768 tokens and, for a reasoning model, the output budget to at least 16,384. Ask for one small program at a time. Run `tools/ppl_gate_v1e.py` on what comes back and paste the error lines into the next turn. The example at the end passes the gate; ask the model to imitate it.

## 1. What PPL is and is not

- PPL is the HP Prime's own language. It is **not** Python, TI-BASIC or BASIC. Blocks are `BEGIN … END;`, `IF … THEN … ELSE … END;`, `FOR i FROM a TO b DO … END;`, `WHILE … DO … END;`, `REPEAT … UNTIL …;`, `CASE IF … THEN … END; … DEFAULT … END;`. Every statement ends with `;`. Assignment is `:=`. Equality test is `==`. Not-equal is `<>`. Comments are `//` to end of line.
- A program file holds one or more routines. `EXPORT Name()` makes a routine appear in the program catalog; helpers are declared without `EXPORT`. Every routine in every program on the calculator shares one name pool, matched ignoring case, so helper names must be unique across programs: prefix them (`tbCalc`, `tbShow`).
- Reals carry 12 significant digits, so `x := x + step` leaves x unchanged once the step is below x's last digit: a stepped loop can then run for ever. Count the steps instead, or keep the step far above x's 12th digit. There is no integer type. Lists are `{1, 2, 3}`, indexed from 1, `L(2)`. Strings are `"…"`, `DIM(s)` is the length, `+` concatenates, `MID`, `LEFT`, `RIGHT`, `INSTRING` are the tools.
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
- `EXPORT` on a helper puts it in the Program Catalog, where a student can run it by mistake. Export only the entry point and the results a student is meant to read from Home.
- Distribute programs as plain `.txt` files pasted into the HP Connectivity Kit's program editor. Never rename a `.txt` to `.hpprgm`; that format is binary.

## 3. Names

- A name must not match a **built-in command or function, ignoring case**. `csC` is a syntax error because `CSC` is the cosecant; `ans`, `ci`, `fp`, `ip`, `ln`, `re`, `im`, `sign`, `e`, `i`, `x`, `K`, `G1` to `G9` are all taken. Check every new name against the built-in list (`tools/HP_Prime_Builtin_Names.txt`).
- A parameter name is checked more strictly than a `LOCAL`: `fp` fails as a parameter even where `LOCAL fp` parses.
- Avoid bare single-letter lowercase names altogether: `x` is the CAS variable, `i` the imaginary unit, `e` the constant.
- Prefix every helper routine with a two- to four-letter tag for the program (`tbShow`, `cs_Grid`, `sr_SRCDF`; letters only, the fleet checker reads `tb` or `cs_` as the tag), and every local with a tag for its routine (`shX`, `drT`), so names never collide and greps are easy.
- Never use `K`, `X`, `A` to `Z` as loop or `MAKELIST` counters; they are Home's variables and the program overwrites them. Use a `LOCAL`.

## 4. Numbers and built-ins

- `STRING(value, 2, d)` prints `d` fixed decimals. Mode 1 ignores `d`. A value below 10^(-d) in mode 2 prints in scientific form, so print a tiny p as `"p < 0.0001"` instead of letting it switch. **`d` can be at most 12**: `STRING(0.5, 2, 13)` is "Invalid input", so cap a number of decimals worked out from the data. Fixed output also holds at most 12 significant digits and turns scientific from 1E12. The safe form is `STRING(ROUND(x, d), 2, d)`. `STRING(value, 3, d)` is scientific: `STRING(0.00015, 3, 1)` is "1.5ᴇ-4".
- `STRING()` writes a minus sign as `CHAR(8722)`, not ASCII 45, and the exponent's E as `CHAR(7431)` (ᴇ). Test for the scientific form with `INSTRING(s, CHAR(7431)) > 0`, never by matching the text. Never build text for the CAS or for Python with `STRING()`.
- `ROUND(x, d)` rounds halves away from zero. `IP`, `FP`, `FLOOR`, `CEILING` exist. `x^0.5` is the square root to use in code (the √ sign is not ASCII).
- **Never compute an upper tail as `1 - CDF`**: with 12 digits the difference is exactly 0 once the tail is below about 5E-13. Normal upper tail: `NORMALD_CDF(m, s, 2*m - t)`. Chi-square with 1 df: `2*NORMALD_CDF(0, 1, -(x^0.5))`; with 2 df: `EXP(-x/2)`; with more df, the finite sum of positive terms (even df: `EXP(-x/2)` times `1 + h + h^2/2! + …` with `h = x/2`; odd df: `2*NORMALD_CDF(0,1,-(x^0.5)) + (2*x/3.14159265359)^0.5 * EXP(-x/2) * (1 + x/3 + x^2/15 + …)`). A right-tail quantile is `-NORMALD_ICDF(0, 1, alpha)`, not `NORMALD_ICDF(0, 1, 1 - alpha)`.
- Build probabilities from **positive terms**; an alternating sum loses all its digits when the answer is small.
- **Take a standard deviation from the deviations, in a second pass**: compute the mean first, then the sum of `(x - mean)^2`. The shortcut `Σx² - n·mean²` loses its digits when the mean is large next to the SD (data near 10^8 with s = 3.03 came out as 2.98). Wrap a variance in `MAX(0, …)` before the square root.
- **Work in logarithms** where a power or a product can pass 1E499, and **scale before squaring**: `(s1^2/n1 + s2^2/n2)^0.5` with s = 1E-300 squares to 0, and with 1E300 to infinity; factor out the larger s first. An exact test that multiplies binomial coefficients builds each log coefficient from the one before, `LN C(m, k+1) = LN C(m, k) + LN((m - k)/(k + 1))`: no factorial, nothing overflows.
- `CHISQUARE(df, x)` is the **density**, not a tail. `CHISQUARE_CDF`, `CHISQUARE_ICDF`, `FISHER_CDF`, `FISHER_ICDF` accept **whole-number df only**; the densities and the Student functions take any df.
- `STUDENT_CDF` loses its digits at a huge df: at t = -1.96 it is right to 8 digits at df 10^6, gives 0.023 for 0.025 at df 10^12, and 0.5 from df 10^15. Cap a typed sample size (a million keeps the df below 2×10^6).
- `BINOMIAL(n, p, k)` and `BINOMIAL_CDF(n, p, k)` take (n, p, k) in that order; HP's own manual prints it wrong. `POISSON_CDF(lambda, k)` with k < 0 is an error, not 0.
- `NORMALD_ICDF(0, 1, 1)` and an overflow return infinity, not an error, and `IFERR` does not see it. Clamp probabilities inside (0, 1) before an inverse CDF. **Division by zero is an error** that stops the program: refuse a zero before you divide by it.
- Available and reliable: `NORMALD`, `NORMALD_CDF`, `NORMALD_ICDF`, `STUDENT`, `STUDENT_CDF`, `STUDENT_ICDF`, `FISHER`, `FISHER_CDF`, `BINOMIAL`, `BINOMIAL_CDF`, `POISSON`, `POISSON_CDF`, `COMB`, `IFTE`, `MAKELIST`, `CONCAT`, `RANDOM`, `RANDINT`, `RANDSEED`, `MAX`, `MIN`, `SORT`, `MAKEMAT`, `TICKS` (milliseconds, no parentheses).
- Not available: `GEOMETRIC*` (compute `p*(1-p)^(k-1)` by hand), `LNGAMMA` outside the CAS (carry a Lanczos helper, or work in logs as above).
- `INSTRING(s, sub)` with `s = ""` is a **run-time error**. Guard every call: `IF DIM(s) > 0 THEN … END;`. `INSTRING("abc", "")` returns 1, so an empty search string loops forever in a replace routine; guard that too.
- `LEFT(s, 0)` and `RIGHT(s, 0)` return the **whole string**, not `""`. Guard a count that can be 0. `MID(s, 0, n)` is an error: MID starts at 1.
- **Not equal is `<>`.** `!=` is a factorial and a test: `3 != 0` gives 0, and `999 != 0` stops with "Numerical overflow".
- `AND` and `OR` stop evaluating once the left side decides, so `DIM(s) > 0 AND INSTRING(s, "a") > 0` is safe.
- A trailing-zero stripper must check that the string contains a `.` first; `STRING(140000000000, 2, 1)` has none.

## 5. Input and dialogs

- `INPUT({v1, v2}, "Title", {"label 1", "label 2"}, {"help 1", "help 2"}, {default 1, default 2})`. The first argument is a list of **variable names**, which `INPUT` writes back in place. Value lists give "Invalid Input". `INPUT` returns 0 when the user cancels: test it and return.
- **Make every number field take numbers only: `{name,[0]}`.** `INPUT({{v1,[0]}, {v2,[0]}}, …)` refuses a list typed into the field ("Invalid input", and the field keeps its value). A plain name accepts any type, so a list typed where a number belongs goes into the arithmetic and stops the program or prints nonsense.
- **Never `INPUT` into a routine parameter**; it fails silently. Copy to a `LOCAL`, `INPUT` that.
- There is no blank input field: a real always shows a value. Default to 0 unless 0 is illegal for the field (a confidence level defaults to 0.95, an alpha to 0.05).
- About 14 characters of a label show before the Prime cuts it with "…", and about 47 of the help line. Keep labels short ("n:", "Mean:") and put the detail, and the field's range, in the help line.
- **Refuse a value outside its range with a sentence that gives the range, and change nothing**; never clamp it without a word. Sensible ranges for a course: a mean or a bound from -10,000 to 10,000; an SD, a df or a rate above 0 and at most 1,000; a sample size at most 10,000; a count in a table at most 100,000; alpha from 0.001 to 0.2. Data loaded into the lists are not limited.
- `CHOOSE(idx, "Title", {"item 1", "item 2", …})` is the list form and takes any number of items; the simple form stops at 14. `CHOOSE` numbers the items itself (1 to 9, then A, B, C), so do not number them in the strings. **An item shows at most about 30 characters**: the box sizes itself to about 214 pixels and cuts the rest. Set `idx := 0` before the call and test `idx` afterwards; Cancel leaves it 0. Never test `CHOOSE`'s return value for a specific number.
- `MSGBOX(text)` shows **5 lines**; the rest is lost. Longer output goes on a screen of your own. `MSGBOX(text, 1)` shows OK and Cancel and returns 1 or 0.
- A guard message should teach: say what was wrong with the value and what would be right.

## 6. Screens and graphics

- The screen is 320 × 240, origin top left, y increasing **downward**. Fonts: `TEXTOUT_P(text, G, x, y, font, colour)` with font 1 (small), 2 (medium), 3 (large); it returns the x just past the text. Colours are `RGB(r, g, b)`; write `#FFFFFFh`-style literals only in strings or not at all.
- **Compose off screen, blit once.** `DIMGROB_P(G1, 320, 240, RGB(255,255,255));` then draw every element to `G1`, then `BLIT_P(G0, 0, 0, G1);`. Drawing straight to `G0` tears. A whole-screen blit takes about 1 ms on a G2 and 5 ms on a G1.
- `RECT_P(G, x1, y1, x2, y2, edge, fill)`, `LINE_P(G, x1, y1, x2, y2, colour)`, `PIXON_P(G, x, y, colour)`, `ARC_P(G, x, y, r, colour)`. **A `RECT_P` with one colour fills the rectangle**; for an outline, give two colours or draw four `LINE_P`. No dotted lines: draw them with `PIXON_P` in a `STEP 4` loop. Concentric `ARC_P` rings do not make a solid disc; use `FILLPOLY_P` or small filled `RECT_P` bars.
- `FILLPOLY_P(G, {{x1,y1}, {x2,y2}, …}, colour, alpha)` fills a polygon, translucent with alpha 0 to 255; a one-colour `TRIANGLE_P` also works on both calculators.
- Soft keys: `DRAWMENU({"Edit", "Run", "", "", "", "Quit"})` after the blit; it paints the bottom strip itself, so repeat it after every blit. The six slots are 53 pixels wide; a tap at x lands in slot `MIN(6, IP(x/53.4) + 1)`.
- Shade a region by iterating **pixel columns**, not sample points, or gaps appear. Cache a curve's heights once per frame if two passes need them, and compute a slow curve at every second or third column and join the points with lines.
- Axis ticks: step 1, 2 or 5 times a power of ten; first tick `CEILING(xmin/stp)*stp`. Fit both axes before drawing a reference curve.
- **Measure text by its glyphs, not by counting characters.** Use the x that `TEXTOUT_P` returns: draw a line once off screen (to `G1` or a small `DIMGROB_P` grob) and read where it ends. The widths of 132 characters in fonts 1 to 3, measured that way, are in `verify/round11/glyph_widths_vc.json`. Keep text lines 14 pixels apart at font 2, and keep a statistic's name ("t crit") on one line.

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
- `WAIT(-1)` touch lists are `{type, x, y}` with type 0 press, 1 drag, 2 lift (may be `{2}` alone, so check `SIZE` before reading x and y), 3 click, 7 long press. Compare `TYPE(kk) == 6` to tell a list from a key code. The numbers are integers, which `STRING()` prints in hexadecimal: add `0.0` before printing one.
- **`MOUSE` numbers its events differently**: its fifth element is 0 new, 1 completed, 2 drag, 3 stretch, 4 rotate, 5 long click. Say in a comment which table a handler reads.
- **Soft keys under `WAIT(-1)` arrive only as a click**, `{3, x, y}` with y ≥ 218: no press and no lift. Once a program has drawn a `DRAWMENU`, a tap on that strip arrives this way for the rest of the run, even on a screen that shows no soft keys.
- A `GETKEY` drain does not drain touch, and `WAIT(-1)` returns -1 by itself after about a minute with no event. Hold a page with one helper that drains keys and touch, waits for either, and drains again.
- The footer must say only what the keys really do on that screen. End a program with `RETURN`, not `PRINT`, unless there is Terminal output to scroll; returning a short summary string leaves it in Home's history.

## 8. MicroPython inside a program

- The interpreter is **MicroPython 1.9.4**, tracking CPython 3.4. No f-strings, no `random` module (use `urandom`), no `time` (use `eval('ticks()')`), no `os`, no `fsum`, `isclose`, `factorial`, `comb`. `math` has `erf`, `erfc`, `lgamma`, `gamma`.
- Embed it as `#PYTHON name … #END` in the program file, called by a PPL wrapper `PYTHON(name)`. Pass only small integers or short text as arguments: they arrive in `sys.argv` as display-formatted strings (`'−2.5'` with a Unicode minus, `'1ᴇ20'`), which `float()` rejects. Read real numbers and lists from PPL globals with `hpprime.eval("name")`; write back with `hpprime.eval('NAME:=' + "%.6f" % x)`. Never use `repr()` on a float crossing the bridge.
- **`hpprime.eval` sees only `EXPORT`ed names.** A file-level `LOCAL` read from Python comes back as its own name, as text, so `float()` raises. Put the values Python reads in exported globals.
- **Hand back a few numbers, not hundreds.** A crossing is cheap once but adds up: a curve of 480 values written back one at a time made every key press take 3 to 4 seconds, where the same curve in PPL took under 1. Python pays for a fit or a simulation that returns a handful of results; anything per pixel stays in PPL.
- **A Python exception does not raise a PPL error.** `IFERR` around `PYTHON(…)` catches nothing; the program carries on with whatever the output variable held. So: clear the output variable before the call, validate by using the result inside `IFERR` afterwards, and always carry a pure-PPL fallback. Report on screen which engine answered.
- A top-level `import` of a missing module, a quote inside a string concatenated into `eval`, or a PPL list containing a string handed raw to Python, each close the app with no message.
- `matplotl` is unusable for charts; draw with PPL `_P` commands or `hpprime`'s `line`, `fillrect`, `pixon`.

## 9. The CAS, behind a guard

- `CAS(s)` with `s` a string variable hands the text back **unevaluated**. Call it through one routine instead: `IFERR r := STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")")); THEN r := ""; END;`. Strip the surrounding quotes. Treat an answer containing `undef`, `rror` or the ∞ character as a failure and fall back to the PPL number. Test the answer only when `DIM(r) > 0`.
- Build CAS text from **integers only**: write 0.95 as `95/100`. Home's `STRING(-2.5)` carries a Unicode minus the CAS may not read.
- The Prime prints CAS answers its own way: `e^(…)`, `√2`, `{1/20}`, never `exp(`, `sqrt(` or `list[`. Check an answer by its **value** against the program's own number, never by its text, and show a badge, "exact (CAS)" or "decimal".
- CAS variables persist for the student. Use tagged names (`ctq`), never `x`, `n`, `p`, `k`, `t`, and never assign them.
- Call the CAS on events (a page opens, a value changes), never on every frame, and cache the text. Numbers for arithmetic come from PPL; the CAS supplies display text.

## 10. The built-in apps, and what a program keeps

- **The Statistics lists are reachable**: `D1` to `D9` (Statistics 1Var) and `C1` to `C9` (Statistics 2Var) can be read and written from a program. Wrap the first read in `IFERR`: a list does not exist until its app has been opened once. `D2 := {}` empties a list, and a program that reads every list that holds data must clear the ones left from an earlier load. `STARTAPP("Statistics 1Var")` opens the app with the data in place.
- **App settings are not reachable.** `H1Type` and `SetSample` in a standalone program are a syntax error at paste time, which `IFERR` cannot catch. Tell the student the setting instead, or write the program as an app.
- The matrices `M0` to `M9` can be read as `M1(r, c)`, with `SIZE(M1)` giving `{rows, columns}`; a program can spread a matrix's columns into the lists.
- **File-level variables keep their values between runs**, until the program is checked or sent again, and they travel inside a checked file. That is useful for remembering a student's last choices and wrong for anything that describes the current run: reset that at the start of the main routine.

## 11. Style

- On screen, write the symbol, not its name: χ² is `CHAR(967) + CHAR(178)`, √ `CHAR(8730)`, ≥ ≤ ≠ `CHAR(8805)`, `CHAR(8804)`, `CHAR(8800)`, ± `CHAR(177)`, × `CHAR(215)`, → `CHAR(8594)`, ∞ `CHAR(8734)`, μ σ θ ρ λ `CHAR(956)`, `CHAR(963)`, `CHAR(952)`, `CHAR(961)`, `CHAR(955)`, subscript ₀ ₁ ₂ `CHAR(8320)` to `CHAR(8322)`, x̄ `CHAR(57344)`, p̂ `CHAR(57345)`, ŷ `CHAR(375)`, ȳ `CHAR(563)`. A combining bar over a letter does not stack; use these single characters.
- Spaces round `=`: `"p = 0.0432"`. A tiny p prints as `"p < 0.0001"`, never `"p = < 0.0001"` and never `"p = 0"`.
- Every number of 1,000 or more on screen carries its commas (12,345.678; 1,000,000). `STRING` never adds them, so add them with a small routine of your own where the number becomes text; never in text the CAS or `EXPR` reads, and never in a year.
- Every program starts with a comment header: name and version, one line on what it does, the author, the licence line, and what has and has not been tested on a calculator.
- Version by letter (`beta 3e` to `beta 3f`); never change a file silently.

## 12. Before delivering a program

1. Every new name checked against keywords and built-ins, ignoring case; every helper carries the program's letter tag.
2. Every `LOCAL` at the top of its routine, 6 names a line.
3. No comment inside a bracket; no lowercase `e` exponent; code ASCII; `<>`, never `!=`.
4. Every `INSTRING` guarded; every `INPUT` target a variable, every number field `{name,[0]}`, every typed value checked against its range with a sentence; every `CHOOSE` index reset to 0 first.
5. No `1 - CDF`; probabilities clamped before an inverse CDF; no division by a value that can be 0; standard deviations from a second pass.
6. Draw to `G1`, blit once; drain, wait, drain.
7. The formulas checked against SciPy or a textbook example before the program is pasted, with a reference that gives the same answer twice (one that changes is a simulation).
8. `python3 ppl_gate_v1e.py Program.txt` passes. If you can, run the monkey test too (`tools/monkey_v1b.py`): random keys, taps and odd typed values, a thousand times.

## 13. A complete example that passes the gate

A 2 × 2 table analyzer: one `INPUT` form with number-only fields and a range check, the chi-square with and without Yates's correction, the odds ratio with its 95% interval, a result screen, and a clean exit. It passes `tools/ppl_gate_v1e.py` and runs in the PC harness (`tools/ppl_run_v3e.py`) with the default table, a Cancel, a count over 100,000, and a row of zeros.

```
// ============================================================
// TBL2X2 - version 2
// Chi-square and odds ratio for a 2 x 2 table (a b / c d)
// ============================================================
// Author: Roger Metcalf, 2026. Written with AI assistance (Anthropic
//   Claude). Free for educational and personal use; no warranty.
// Checked by ppl_gate_v1e and run in the PC harness (ppl_run_v3e);
//   not yet on a calculator.

EXPORT TBL2X2()
BEGIN
  LOCAL tbA, tbB, tbC, tbD, tbOK, tbR1;
  LOCAL tbR2, tbC1, tbC2, tbN, tbX2, tbYt;
  tbA := 10; tbB := 20; tbC := 30; tbD := 15;
  tbOK := INPUT({{tbA,[0]}, {tbB,[0]}, {tbC,[0]}, {tbD,[0]}}, "2 x 2 table",
                {"a", "b", "c", "d"},
                {"Row 1, column 1: 0 to 100,000", "Row 1, column 2: 0 to 100,000",
                 "Row 2, column 1: 0 to 100,000", "Row 2, column 2: 0 to 100,000"},
                {10, 20, 30, 15});
  IF tbOK == 0 THEN RETURN; END;                       // Cancel
  IF MIN(tbA, tbB, tbC, tbD) < 0 OR MAX(tbA, tbB, tbC, tbD) > 100000 THEN
    MSGBOX("Each count must be from 0 to 100,000."); RETURN;     // refuse, and say the range
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
