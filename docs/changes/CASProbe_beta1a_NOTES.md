# CASProbe beta 1a: notes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 16 October 2026.*

**Status: NOT yet run on hardware.** Nothing about the CAS has run on our calculators yet. This probe decides how every fleet program calls the CAS (BRIEF_CAS.md's `xxCas`), so it should run before any CAS version of a fleet program is pasted.

Files, all in ``:
- `CASProbe_beta1a.txt`: the program (2,090 lines, PPL plus two `#PYTHON` blocks; tag `cx`).
- `verify_CASProbe_beta1a.py`: the PC checks (desktop Giac, CPython, run harness v3). Its output is in `verify_CASProbe_beta1a_output.txt`: **145 checks, all pass**.
- This file.

**Beta 1a supersedes beta 1.** `CASProbe_beta1.txt`, its NOTES and its verify files stay in out/ for the record (out/ keeps old versions beside new ones), but only beta 1a should be pasted. The two share every routine name, so they must never be on the calculator together.

---

## 0 · What changed in beta 1a

The coordinator asked for the tests that the CAS program builders need (ErrorRate Lab, RankLab, the regression and Fisher pages). Beta 1a adds eight tests and changes nothing else in beta 1, apart from:
- the version strings (banner, menu title, page titles, log heading, Python comments);
- the pass-flag lists, grown from 40 to 50 entries;
- three new lines in the log's summary.

**Every beta 1 test keeps its number**, because other programs' notes cite them (T16b, T25, T34). The new tests are numbered T35–T42 and **run after T32 and before the Python tests**, which stay last. A log line "-- T35-T42 (added in beta 1a) --" marks where they start.

| Test | Asks | Desktop Giac 1.9 / SciPy |
|---|---|---|
| T35a–d | one CAS text of about 1,000, 2,000, 3,000 and 6,000 characters: 1/2+1/6+1/12+… (the sum of 1/(k(k+1)), built with cxIStr), whose answer is N/(N+1). Each length is timed; the test stops at the first failure, which is the break | 143/144 (1,002 chars), 268/269 (2,002), 385/386 (3,008), 718/719 (6,005) |
| T36a | `solve([cxa+cxb=3,cxa-cxb=1],[cxa,cxb])`: the exact shape of the answer | `list[[2,1]]`, shape "prefix list, [[]], commas" |
| T36b | the least-squares normal equations through (0,2), (1,3), (2,5), (3,4), built from the data with cxIStr: `solve([4*cxa+6*cxb=14,6*cxa+14*cxb=25],[cxa,cxb])` | `list[[23/10,4/5]]` (numpy.polyfit: slope 0.8, intercept 2.3) |
| T37a | `normal((3*cxt+1)*(4*cxt+1)/(2*(cxt*cxp-cxt-cxp)))`: the shape | `(12*cxt^2+7*cxt+1)/(2*cxp*cxt-2*cxp-2*cxt)` |
| T37b | its value at t = 1, p = 3 (the PASS, since printed forms vary) | `-10` |
| T37c | `factor(6*cxt^2+7*cxt+2)` | `(2*cxt+1)*(3*cxt+2)` |
| T38a | does a product print with `*`, a dot (codes 183, 8901, 8729) or × (215)? `expand((cxt+2)*(cxp+3))` | `cxp*cxt+2*cxp+3*cxt+6`: `*` |
| T38b–d | list brackets: `seq(cxj^2,cxj,1,4)`, `solve(cxt^2=4,cxt)`, `[[1,2],[3,4]]*2` | `[1,4,9,16]`; `list[-2,2]`; `[[2,4],[6,8]]` |
| T39a | `series(1-exp(-cxt),cxt=0,3)`: the shape (ErrorRate's trawl page, with a tagged symbol) | `cxt-1/2*cxt^2+1/6*cxt^3+cxt^4*order_size(cxt)` |
| T39b | `convert(series(…),polynom)`: does it drop the remainder? | `cxt-1/2*cxt^2+1/6*cxt^3` |
| T40a | `limit(comb(cxn,2)*(cxl/cxn)^2*(1-cxl/cxn)^(cxn-2),cxn,inf)`, timed | `1/2*cxl^2*exp(-cxl)` |
| T40b | the same written as ErrorRate's falling factorial, `cxn*(cxn-1)/2*…` | `1/2*cxl^2*exp(-cxl)` |
| T40c | ErrorRate's whole k ≤ 2 sum (erlPoiTerms' exact text, with cx names) inside `factor(limit(…,cxn,inf))` | `(cxl^2+2*cxl+2)*exp(-cxl)/2` |
| T41a | how the ANSWER of an infinite limit prints: `limit(cxn^2,cxn,inf)`. T16/T16b settle the INPUT spelling, which is ErrorRate line 2463's `erlInf` | `+infinity`. With `infinity` as the input, desktop Giac answers the unsigned `infinity` and warns |
| T41b | ErrorRate's trawl limit `limit(1-(1-cxl/cxn)^cxn,cxn,inf)` | `-exp(-cxl)+1` |
| T42 | no CAS: `BINOMIAL_CDF(30, 0.2, 2)`. It confirms the (n, p, k) order (GfxProbe T20 checks only BINOMIAL's) | SciPy `binom.cdf(2,30,0.2)` = 0.0441790 |

**How each new test passes:**
- T35: the exact N/(N+1).
- T36a: the answer contains `2,1` (otherwise VALUE).
- T36b: it contains both `23/10` and `4/5`.
- T37b: it is exactly `-10`.
- T37c: it contains `2*cxt+1` and `3*cxt+2`.
- T38a: it contains `*` (otherwise VALUE, naming the sign found).
- T39b: it contains `cxt^3` and neither `order` nor `O(`.
- T40a–c: it contains `cxl^2` and `-cxl`, true of both `exp(-cxl)` and `e^(-cxl)`.
- T41b: it contains `-cxl`.
- T42: the value is within 0.000001 of 0.044179.
- The shape tests (T36, T38) are VALUEs with a "shape:" line: the text before the first bracket, the brackets in order, and commas or semicolons.

**Placement:**
- T35–T41 go through the chosen call form and are skipped with T11–T32 if no form works.
- T42 has no CAS, so it always runs.

**The three new summary lines in the log** are "long CAS text: works to N characters" (or where it fails), "an infinite limit prints: …" and "BINOMIAL_CDF order (n, p, k): yes/NO". The summary page itself is unchanged.

**New CAS symbols:** `cxa`, `cxb` and `cxl` (tagged; they never collide with a student's names).

---

## 1 · What the probe does, and the order

It follows GfxProbe beta 1's structure:
- The palette is held in file-level LOCALs, set in `cxInit`.
- The tests are numbered T01–T42 and run in the order T01–T32, T35–T42, T33, T34. Every test runs inside `IFERR`, so one failure cannot stop the rest, and the riskiest tests (Python) come last.
- Each test names itself in `CX_LAST`, the crash marker, and draws a progress page. A slow CAS call on a G1 then does not look like a hang.
- Results go one line at a time into the Home list `CX_LOG`. Lines are at most 46 characters, word-wrapped, with continuation lines indented two spaces.
- At the end come a summary page (photograph it), then the log pager. `CX_SUM` holds the one-line verdict, and the program returns `"CASProbe: " + CX_SUM`.

**The menu:** Run every test · Skip Python CAS · Skip all Python · Show last log. Items are unnumbered (the Prime numbers them itself), and Cancel returns "CASProbe: cancelled".

**What it changes:** only its own Home variables:
- `CX_LOG`, `CX_LAST`, `CX_SUM`, `CX_CS`, `CX_PYS` and `CX_PYM`.
- `HSeparator` and `HFormat` are read through `EXPR`, so an unknown name is a run-time error, not a paste-time one. They are never written.
- The CAS settings are only read (`cas_setup()` in T14, and again in T32b to see whether the run changed them).
- T25 assigns the tagged CAS variable `cxq` and purges it again, and only if `cxq` was unassigned to begin with.
- `x`, `n`, `p`, `k` and `t` are only **read** (T25c), to see whether Roger's CAS has any of them assigned now.

**CAS symbols** are all tagged: `cxn`, `cxt`, `cxp`, `cxz`, `cxq` and `cxj`, plus `cxa`, `cxb` and `cxl` in beta 1a. CAS text never contains a decimal point except T13 (on purpose) and T31b (Home's STRING of −2.5, on purpose). Integers in CAS text come from `cxIStr` (BRIEF_CAS's `xxIStr`).

**The call form is adaptive.** T04–T10 try the forms; `cxPickForm` takes the first of T07, T08 and T09 that returns all 30 digits:
- T07 is BRIEF_CAS's routine as written, with the text arriving as a parameter.
- T08 is the EXPR literal form.
- T09 is the `CAS.eval` form.

T11–T32 and T35–T41 then run through that form. If no form works from a variable, they are skipped and the summary says "CAS available: no"; T42 (no CAS) still runs.

---

## 2 · The tests: what each checks, why, and what desktop Giac 1.9 gives

The "PASS when" column is the program's own test.

### Home side (no CAS)

| Test | Checks | Why it matters | PASS when |
|---|---|---|---|
| T01 | `STRING(123456789012)`, `STRING(-2.5)`, `"" + 123456789012`, with the character codes | PyProbe saw U+FE50 group marks and a U+2212 minus in argv. If STRING does the same, `STRING(real)` can never go into CAS text. That is already the fence rule; T01 shows the reason | the text is exactly `123456789012` and `-2.5` (codes 45 50 46 53) |
| T02 | `cxIStr(123456789012)`, `(-25)`, `(0)`, `(COMB(30,15))` | the cure for T01: plain digits only | the four strings are exact, and no code is over 126 |
| T03 | reads `HSeparator` and `HFormat` (VALUE) | a comma decimal mark would break any decimal point in CAS text, and list parsing with EXPR (T24) | — |

### Call forms (each asks for C(100,50) = 100891344545564193334812497256)

| Test | Form | Source | Desktop Giac / harness |
|---|---|---|---|
| T04 | `STRING(CAS("comb(100,50)"))`, literal | kit `CAS.md` (emulator: `CAS("1/2+1/3")` = 5/6, TYPE 8); `spect.hpprgm` (`STRING(CAS("..."))` in IFERR) | 30 digits |
| T05 | the answer kept in a LOCAL: `TYPE`, `STRING(v)`, `"" + v`, and `TYPE(CAS("comb(8,4)/2^8"))` | the kit measured TYPE 8; HP's help says 14.x; HP's Commands.pdf says numerical-mode outputs "are transformed into strings" | 30 digits both ways; TYPE 8 is the harness's assumption |
| T06 | `CAS(s)`, s a LOCAL string | how programs build text. The risk is that the CAS hands the string itself back (in Giac a string evaluates to itself) | 30 digits |
| T07 | `cxCas(s)`, BRIEF_CAS's `xxCas` exactly as written (s a parameter) | if this passes, no fleet program changes | 30 digits |
| T08 | `STRING(EXPR("CAS(" + q + s + q + ")"))`, q = CHAR(34) | the literal form built at run time (HP User Guide: EXPR; kit: CAS) | 30 digits |
| T09 | `STRING(EXPR("CAS.eval(" + q + s + q + ")"))` | PyReversi (hpcalc `pyreversi.zip`, `PyReversi_Python.txt` line 246) and the ReavesX EE-CpE applet (`MENU.py` line 57) store CAS results with `CAS.eval("…")` in run-time PPL text | 30 digits (harness shim, §5) |
| T10 | `STRING(EXPR("CAS.comb(100,50)"))` | HP `Commands.pdf` (commands.zip, CAS entry): "CAS(expression) or CAS.function(...) or CAS.variable[(...)] … outputs in numerical mode are transformed into strings"; User Guide example `CAS.irem(45,7)`. Information only: the fence bans dotted calls | 30 digits (harness shim) |

The dotted forms are written inside `EXPR` on purpose. A form the firmware does not know is then a **run-time** error that IFERR catches, not a paste-time syntax error that stops the whole paste.

A failure is described by how it looked:
- "run-time error"
- "empty answer"
- "text came back unevaluated"
- "became a 12-digit real"
- "other text"

A pass whose text came back inside quotes is noted, and it changes the advice (§6).

### Fractions, strings, modes

| Test | CAS text | Desktop Giac 1.9 | PASS when |
|---|---|---|---|
| T11 | `comb(8,4)/2^8` | `35/128` | = 35/128 |
| T12 | `string(comb(8,4)/2^8)`, then TYPE, STRING and `"" +` of it | `"35/128"` (a Giac string) | TYPE 2 and `"" + it` = 35/128 (otherwise VALUE) |
| T13 | `exact(0.4857142857142857)` | `17/35` | = 17/35 |
| T14a | `1/3` | `1/3` (exact mode) | VALUE: "stays 1/3: CAS exact" or "became decimal: approx?" |
| T14b | `sqrt(2)` | `sqrt(2)` (the Prime may print √: its code is listed) | VALUE |
| T14c | `evalf(17/35)` | `0.485714285714` | contains 485714 |
| T14d | `cas_setup()` | `[0,0,0,1,0,[1e-12,1e-15],12,[2,100,0,25],0,1,0,1]` (item 1: 0 exact, 1 approx) | VALUE; kept for T32b |
| T15a | `"comb(" + cxIStr(100) + "," + cxIStr(50) + ")"` | 30 digits | = 30 digits |
| T15b | `cxIStr(123456789012) + "+1"` | `123456789013` | = 123456789013 |

### Calculus and solving (each with its own time)

| Test | CAS text | Desktop Giac 1.9 | PASS when |
|---|---|---|---|
| T16 | `limit(cxn*(1-(1/20)^(1/cxn)),cxn,inf)` (retried with `infinity` if `inf` errors) | `ln(20)` | contains `ln(20)` |
| T17 | `limit(cosh(cxt/sqrt(cxn))^cxn,cxn,inf)` | `exp(cxt^2/2)` | contains `cxt^2/2` |
| T18 | `solve((95/100)*cxp/((95/100)*cxp+(5/100)*(1-cxp))=1/2,cxp)` | `list[1/20]` (older Giac: `[1/20]` or `{1/20}`) | contains `1/20` |
| T19 | `fsolve((1-cxp)^30=5/100,cxp=0..1)` | `[0.0950338528553]` | contains `950338` |
| T20a | `diff(ln(cxp/(1-cxp)),cxp)` | `1/cxp+1/(1-cxp)` | VALUE |
| T20b | `simplify(diff(...))` | `-1/(cxp^2-cxp)` | VALUE |
| T20c | `subst(diff(...),cxp=1/4)` | `16/3` | = 16/3 (the printed forms vary, the value does not) |
| T21a | `int(exp(-cxz^2/2)/sqrt(2*pi),cxz,-inf,196/100)` | `erf(49*sqrt(2)/50)/2+1/2` | VALUE |
| T21b | `evalf(int(...))` | `0.975002104852` | contains `975002` |

1.96 is written 196/100: no decimal point in CAS text.

### Size and speed

| Test | CAS text | Desktop Giac 1.9 | PASS when |
|---|---|---|---|
| T22 | `comb(1000,500)` | 300 digits, `270288…216320` | 300 characters, head and tail right |
| T23 | `expand(normal(Q))`, Q = the Gaussian binomial [12 choose 6] in cxq written out | 333 characters, degree 36, middle term `58*cxq^18` | contains `58*cxq^18` |
| T24 | `seq(coeff(normal(Q),cxq,cxj),cxj,0,36)` (fallback `symb2poly(normal(Q),cxq)`), then the text is turned into a PPL list with `EXPR` | `[1,1,2,3,5,7,11,13,18,22,28,32,39,42,48,51,55,55,58,…,1,1]` | 37 numbers, sum 924, item 19 = 58 |

`cxToList` takes what lies between the first opening and the last closing bracket. So `poly1[…]` (what desktop `symb2poly` prints), `list[…]`, `[…]` and `{…}` all work.

### State

| Test | Checks | Desktop Giac (persistent session) |
|---|---|---|
| T25a | `cxq+1`, then `cxq:=7`, then `cxq+1`: is it 8? | `cxq+1`, `7`, **8**: variables persist |
| T25b | `purge(cxq)`, then `cxq+1` | `7`, then `cxq+1`: purge works (PASS) |
| T25c | reads `x`, `n`, `p`, `k`, `t` | each itself (none assigned) |

### Errors (riskiest CAS tests, so last among them)

| Test | CAS text | Desktop Giac 1.9 | PASS when |
|---|---|---|---|
| T26 | `comb(100,` | adds the missing `)` itself, then `comb(undef)` / `Error: Bad Argument Type` | the error is caught by IFERR (PASS); came back as text (VALUE) |
| T27 | `1/0` | `infinity` | VALUE (the Prime may print a glyph: codes listed) |
| T28 | `0/0` | `undef` | contains `undef`: the word xxCas rejects |
| T29 | `cxnosuch(3)` | `cxnosuch(3)` (no error) | VALUE: a typo passes every guard |
| T30 | `fsolve(cxp^2+1=0,cxp=0..1)` | `[]` | VALUE |
| T31a | `STRING(123456789012) + "+1"` | `123456789013` (if STRING is plain) | = 123456789013 |
| T31b | `STRING(-2.5) + "+1/2"` | `-2.0` | VALUE |
| T32 | `cxCas("0/0")`, `cxCas("comb(100,")`, `cxCas("cxnosuch(3)")` | "", "", `cxnosuch(3)` | the first two are "" |
| T32b | `cas_setup()` again | same as T14d | unchanged |

### Added in beta 1a (T35–T42; run before the Python tests)

The full table, with desktop Giac's answers and the pass rules, is in §0.

### MicroPython (last)

| Test | Block | Checks | CPython stand-in |
|---|---|---|---|
| T33a | `cxPyBig` | `str(2**100)` = 1267650600228229401496703205376 | PASS |
| T33b | `cxPyBig` | Python's own exact C(100,50), by `c = c*(50+i)//i` | PASS |
| T33c | `cxPyBig` | reads `CX_CS` (the CAS's own 30-digit text) through `hpprime.eval` and compares it with `int()` | "same" |
| T34a | `cxPyCas` | `import cas` (inside main), then `cas.caseval("comb(100,50)")`: its type, value and ms | `<class 'str'>`, 30 digits |
| T34b | `cxPyCas` | `cas.caseval("comb(8,4)/2^8")` | 35/128 |

How the Python blocks follow Lessons Learned §9:
- The only top-level import is `hpprime`; everything else is imported inside `main()` or a `try`.
- The answer goes back through `ev('CX_PYS:="…"')`, built by concatenation, with quotes and backslashes cleaned out first.
- Progress marks go into `CX_PYM`.
- The PPL side keeps the three guards:
  1. it clears `CX_PYS` and `CX_PYM` first;
  2. it validates by using the answer (it splits it and compares every field);
  3. when no answer comes, it logs "no answer" with the last mark and carries on.

`import cas` / `cas.caseval(text)` is the form on Markowski's page (`Community_Library/docs/markowski_udel/index.html`, line 362). PrimeSUD, Stoichiometry and tml.py use `from cas import get_key` in live code, so the module itself loads on devices.

**Before T34**, a warning page says, in these words: "Next test calls cas.caseval from Python; one author reported a crash. If the calculator resets, rerun CASProbe and choose 'Skip Python CAS'." It offers two buttons, Run it and Skip it; + runs, and − or Esc skips. Just before the call, `CX_LAST` is set to "T34 Python cas.caseval: if you read this after a reset, caseval crashed". At the next start the program reads `CX_LAST`. If it is not "done", the log and a 3-line MSGBOX say where the last run stopped.

---

## 3 · Gate output (final file)

`bash check.sh CASProbe_beta1a.txt CASProbe_beta1.txt`:
```
--- 1. kit lint (errors) ---
CASProbe_beta1a.txt:2091: ERROR: unbalanced: unclosed blocks: -1 ... [no fact]
1 file(s): 1 error(s), 82 warning(s)
--- 2. ppl_check_v2 tally (NEW)  ---       (none)
--- 2. ppl_check_v2 tally (ORIG) ---       (none)
--- 2b. HARD errors in NEW (E2 E3 E6 E8 E10 E11): none
--- 3. lint_ppl: 1163 checks, 71 problems
  PROBLEM line 1623: block depth went negative
  PROBLEM unbalanced blocks: final depth -1 (want 0)
  PROBLEM line 434/451: assignment ... concatenates bare 'bW'/'rV'/'rW' ...
--- 4. full parse: PARSE FAIL <ppl>:134: expected a name after EXPORT
   ORIG: CASProbe_beta1.txt PARSE FAIL <ppl>:112: expected a name after EXPORT
--- 5. 2090 lines, 74479 bytes; no non-ASCII in code
```
`python3 ppl_gate_v1.py CASProbe_beta1a.txt CASProbe_beta1.txt`:
```
2. ppl_check_v3 tally: clean            original: clean      hard errors: none
3. lint_ppl: 1163 checks, 71 problems   (the same lines as above)
5. fleet_names_v2 over 76 files: 0 untagged, 0 mixed-tag files, 0 built-in matches
RESULT: PASS
```
`ppl_gate_v1` skips the kit lint and the parse ("zip not found"), so `check.sh` ran those.

How to read the gate:
- **Kit lint: 1 error.** It is the `#END` `unbalanced` that every Python-block file shows, which the brief allows.
- **The 82 kit warnings** are the Python blocks read as PPL, plus the fleet-wide TEXTOUT_P width note.
- **The 71 lint_ppl problems** are all known noise:
  - 56 "STRING() with 1 or 2 args". This includes every `INSTRING(…)` line: the lint reads `INSTRING(` as `STRING(`, which is why the count grew with the new tests.
  - The `#END` depth.
  - 3 "concatenates bare" lines, which are string parameters.
  - EXPORT discipline and the file name.
- **The full parse fails at the file-level LOCAL after the EXPORT list**, the tool's limit. With those lines and the Python blocks masked: **PARSE OK (80 functions)**.
- **Defined before use:** all 80 routines are.
- **fleet_names:** the only `cx` collisions are between CASProbe beta 1 and beta 1a, which are versions of one program.
- **The checker caught two more built-in clashes** in the new tests: `rE` (Re, the real part) and `fP` (FP). They were renamed `rEx` and `fTerms`.

---

## 4 · Harness output (ppl_run_v3, `verify_CASProbe_beta1a.py`)

**145 checks, ALL PASS** (the 116 beta 1 checks, plus 29 for beta 1a). The full log of every run is in `verify_CASProbe_beta1a_output.txt`.

### C1: `cas='giac'`, Python run in CPython, "Run every test"

- **Returned:** `CASProbe: form 1, CAS yes, slowest 1 ms, 50 pass, 0 fail` (70 CAS calls).
- Every check that desktop Giac can pass, passes: T01 T02 T04–T13 T14c T15 T16–T19 T20c T21b T22–T24 T25b T26 T28 T31a T32 T32b T33a–c T34a–b, and in 1a T35a–d T36a–b T37b–c T38a T39b T40a–c T41b T42.
- 1a, the order: T35–T42 run after T32b and before T33a.
- 1a, the new text: "no break up to 6005 characters", the T36a shape "prefix list, [[]], commas", T41a "prints as infinity", T42 "= 0.044179", and the three summary lines.
- **The VALUEs:**
  - T03: HSeparator 0, decimal dot (preset in the harness).
  - T14a/b/d, T20a/b, T21a, T25a ("CAS variables persist"), T25c, T27, T29, T30, T31b.
- No test stopped with an error, and no CX_LOG line is over 46 characters.

The summary page, as the harness recorded it:
```
CAS available: yes                         (green, font 2)
Call form to use:
  STRING(CAS(s)), xxCas as written         (magenta)
slowest call: 1 ms                         (orange)
  in T04 CAS literal comb(100,50)          (grey, font 1)
pass 50, fail 0, value 19, error 0, skip 0 (blue, font 1)
Home STRING(real): plain ASCII
CAS variables persist: yes
Python ints: exact (2**100 ok)
caseval: str, 30 digits, 32 ms            (the PC's Giac through the stub)
```
The harness's TICKS is a virtual clock (1 ms per reading), so every "ms" here is 1. Real times come only from the device. The PC's Giac times, 30–60 ms per call, are mostly process start-up.

### The other runs

| Run | What it showed |
|---|---|
| C2, Giac as the harness ships it (fresh per call) | T25a "each CAS() call starts afresh"; everything else the same |
| C3, `cas='fail'` | T04–T10 FAIL with a reason; one T11 SKIP for T11–T32 and T35–T41. T42 still PASSes (no CAS), and the log says "long CAS text: not tested". T33 still passes, on the constant ("CX_CS is the constant: no CAS text"). T34 "no answer", last mark "T34 import ok, calling caseval". Summary: "CAS available: no", "none: the CAS gave no 30 digits", "caseval: no answer (crash?)" |
| C4, PYTHON() does nothing | T33 and T34 "Python gave no answer", last mark " none" |
| C5, the menu | "Skip Python CAS": T33 runs, T34 SKIP, no warning page. "Skip all Python": both SKIP. "Show last log": only the pager, log kept. Cancel: "CASProbe: cancelled" |
| C6, the warning | a tap on Skip it, or the − key: T34 SKIP. A tap on Run it: T34 runs. A tap on the summary and on the pager's lower half pages on ("lines 14-26") |
| C7, CX_LAST preset to the T34 marker | "previous run stopped in: T34 …" in the log, and a 3-line MSGBOX |
| C8, stale keys (the dialog's Enter left in the buffer) | no page skipped |

### Simulated device outcomes, to exercise every reporting branch

| Variant | What the probe reported |
|---|---|
| D1: CAS(variable) hands the string back | T04, T05 PASS; T06, T07 FAIL "text came back unevaluated"; T08, T09 PASS. **Form 2 chosen**, and the log gives the line `cR := STRING(EXPR("CAS(" + CHAR(34) + xxS + CHAR(34) + ")"));`. T11–T31 pass through the EXPR form. T32 FAIL, since the as-written xxCas cannot work then. `form 2, CAS yes` |
| D2: CAS answers arrive as 12-digit reals | T04–T10 FAIL "became a 12-digit real"; T11–T32 skipped |
| D3: STRING() with U+FE50 grouping and a U+2212 minus | T01 FAIL ("123﹐456﹐789﹐012", codes 65104; "−2.5", codes 8722 50 46 53). T31a FAIL. T02 and T15 still PASS. Summary "Home STRING(real): NOT plain" |
| D4: a CAS syntax error returned as text | T26 VALUE "came back as text"; T32 still PASS (the "rror" guard catches it) |
| D5: MicroPython with 64-bit ints | T33a "2**100 = ERR small int overflow", T33b FAIL, summary "Python ints: not exact". With no `cas` module: T34 "import cas failed" |
| D6: CAS answers are PPL strings (Commands.pdf) | the 30 digits are still found; "(the text came back inside quotes)". The advice becomes `cR := "" + CAS(xxS);  (T05: no quotes)`, and the summary shows `"" + CAS(s), not STRING`. T11 and the guard still pass |
| D7 (1a): CAS text over 2,500 characters fails | T35a and T35b PASS; T35c FAIL "3008 chars: CAS error"; T35d not tried. "works to 2002 characters; the FAIL is the break", and the summary line says 2002 |
| D8 (1a): an infinite limit printed as +∞ | T41a "prints as the glyph (8734)", and the summary line names it |
| D9 (1a): BINOMIAL_CDF reads (n, k, p) | if that raises: T42 FAIL "run-time error" and "BINOMIAL_CDF order (n, p, k): NO"; if it gives a wrong value: FAIL with "= 0.500000 (SciPy 0.044179)" |
| F: the text helpers on edge inputs | `cxShort` with short limits, `cxRest` past the end, `cxSplit` with a trailing `;`, `cxPyType`, `cxToList` on `poly1[…]`/`list[1/20]`/`[]`, `cxStrip`, `cxFlat`, `cxIStr`, `cxCodes`; in 1a, `cxShape` (`list[[2,1]]`, `[1,4,9,16]`, `{1;2}`, `cxt+1`, `poly1[1,1]`) and `cxMulSign` (`*`, U+00B7, U+22C5, none). Word wrap: a "(1234 ms)" moves to the next line whole; a run of digits is cut at 46 |
| E: layout | no TEXTOUT_P is estimated past x = 320 at the gate's widths (font 1 6 px, font 2 7.6, font 3 8.6) |

---

## 5 · Harness shims and limits (what the PC run does not prove)

- **TYPE of a CAS answer** is not covered by harness v3. The test script returns 8, the kit's emulator measurement, or 2 for a Giac string. T05 and T12 on the device decide.
- **`CAS.eval("…")` and `CAS.comb(…)` inside EXPR**: the kit's parser cannot read dotted names (it raises Unsupported). The script models the documented behaviour: `CAS.eval(s)` → `CAS(s)`, and `CAS.f(a)` → `CAS("f(a)")`.
- **CAS variables do not persist in the shipped harness** (a fresh `icas` for each call). The script's session shim replays assignments to model a persistent CAS; C2 shows the shipped behaviour.
- **A harness v3 bug, worth fixing in v4:** after a syntax error, desktop Giac prints raw bytes (`\x17\xff0.\xa7U`). `giac_eval`'s `subprocess.run(text=True)` then raises UnicodeDecodeError, which surfaces as `Unsupported: CAS given a string is not covered`. The test script decodes with `errors='replace'`. Desktop Giac also *repairs* `comb(100,` by adding the `)` and then reports `Error: Bad Argument Type`; the Prime's older Giac may say "Syntax Error" instead.
- **Desktop Giac's definite `int`** prints a "No checks were made for singular points…" warning line, which the harness keeps in the answer text. The probe tests with `INSTRING`, so it still passes; on the Prime the warning probably goes nowhere.
- **The Python blocks ran in CPython**, whose integers are always exact. T33 on the device is the real test. D5 shows what a 64-bit-int MicroPython would report.
- **Nothing is rendered.** Widths are estimates; the font-1 log lines are at most 46 characters.

---

## 6 · Device run instructions

1. **Install.** If beta 1 is on the calculator, delete it first: the two share routine names. Paste `CASProbe_beta1a.txt` into the Connectivity Kit editor and sync to the **G2**. Check: there should be no syntax error. Both `#PYTHON cxPyBig … #END` and `#PYTHON cxPyCas … #END` must keep their indentation. If the paste fails, the cursor's line is itself a finding: note the line.
2. **Run it on the G2** with the Terminal closed: Program Catalog → CASProbe → "Run every test".
   - A progress page names each test.
   - Most calls should be quick on the G2. If one test sits for more than about two minutes, break the program with the calculator's usual break (not tested here) and note `CX_LAST`.
3. **The warning before T34:** read it, then press + (or tap Run it).
   - If the calculator resets: after the restart, type `CX_LAST` in Home first and photograph it.
   - Then rerun CASProbe with "Skip Python CAS". The crash itself is the T34 finding.
4. **Photograph the summary page.** Then any key opens the log pager: Up/Down move a line, Left/Right or a tap move a page. Photograph every page, or later type `CX_LOG` in Home (one string per line) and `CX_SUM`.
5. **Run it again on the G1**, the same way. The G1 timings are the ones that matter: every result line ends "(… ms)", and the summary names the slowest call.
6. Send back both sets of photos (or the two `CX_LOG`s), and say whether either calculator reset.

Rough time: about 70 CAS calls, 2 Python runs and 3 taps or keys, a few minutes on each calculator. The G1 could take longer, mostly in T16–T17 and T40 (limits), T21–T24, and T35's long texts.

---

## 7 · What each outcome means for BRIEF_CAS.md's call routine

The routine's one line is `cR := STRING(CAS(xxS));` inside IFERR, followed by the `undef` / `rror` guard.

### The call form (T04–T10; the summary's "Call form to use")

| What the probe shows | Change to `xxCas` |
|---|---|
| T07 PASS, no quotes note ("STRING(CAS(s)), xxCas as written") | **None.** BRIEF_CAS stands |
| T07 PASS but "(the text came back inside quotes)", and T05 shows `"" + v` unquoted (summary `"" + CAS(s), not STRING`) | `cR := "" + CAS(xxS);` (HP's Commands.pdf says numerical-mode CAS outputs become strings, and STRING() of a string adds quotes) |
| T07 PASS with quotes, `"" + v` quoted too ("drop the quotes") | keep the line and strip one pair of surrounding quotes, as `cxStrip` does |
| T06/T07 FAIL "text came back unevaluated", T08 PASS (form 2) | `cR := STRING(EXPR("CAS(" + CHAR(34) + xxS + CHAR(34) + ")"));`. CAS text must then never contain a double quote (none of our templates does) |
| T08 FAIL, T09 PASS (form 3) | `cR := STRING(EXPR("CAS.eval(" + CHAR(34) + xxS + CHAR(34) + ")"));` |
| "became a 12-digit real" everywhere | exactness is lost on the way back. If T12 PASSes (`string(…)` arrives as a PPL string), wrap every template: `CAS("string(" + xxS + ")")` (that means a CAS beta 2 probe of that form). Otherwise the exact-fraction features cannot ship, and the decimal fallbacks are what students see |
| only T04 (the literal) passes | a program cannot build CAS text at run time; no CAS feature ships. The next probe would be `#cas` functions (not in beta 1a; see §8) |
| nothing passes, or T04 errors | CAS unavailable from PPL on this firmware; every CAS feature stays on its decimal fallback |

### The guard, the variables and the settings

- **T26 PASS** (a syntax error raises): IFERR is the guard, as written. **T26 VALUE** ("came back as text"): the `INSTRING(cR, "rror")` line is what catches it; T32 confirms whether it does.
- **T28 PASS**: the word is `undef`, as the guard expects. If the Prime prints something else for 0/0, the guard's word changes to what T28 shows.
- **T29**: a misspelt command comes back as itself with no error, so no guard can catch a typo. Fence rule 6 (test every template in desktop Giac) is the only protection.
- **T25a "persist"**: a CAS variable survives between calls, so a student's `x` leaks into any text that uses `x`. Tagged names (fence rule 5) are essential.
  - **T25b PASS**: `purge(xxq)` works, so "start the expression with a purge" becomes allowed.
  - **T25c**: lists which of x, n, p, k, t are assigned in Roger's CAS right now.
- **T32b FAIL**: the run changed `cas_setup()`. Some template is changing a setting, so programs must save and restore (ideas §2 rule 5).
- **T14a "became decimal: approx?"**: the CAS is in approximate mode, so fractions print as decimals. Either templates wrap their answer in `exact(…)`, or the badge says "decimal".

### Home text, separators and timing

- **T01 FAIL** (marks or a special minus): `STRING(real)` must never enter CAS text (already the rule); T31a shows the breakage. **T02 and T15 PASS**: `xxIStr` is the cure, as BRIEF_CAS has it.
- **T03 "decimal comma"**:
  - No decimal point can go in CAS text (already the rule). T13 shows what happens to one.
  - `cxToList`'s EXPR of "{1,1,2}" (T24) may need ";" between items, so any program reading CAS lists must check this.
- **Timing.** Fence rule 2 (event-only calls, cached text) holds whatever the numbers are.
  - Any call over about 1–2 s on the G1 needs a "Please wait" line before it.
  - If T23 and T24 are fast on the G1, RankLab's exact null distributions are feasible.

### Added in beta 1a

- **T35, long text.** A program may send one CAS text up to the last length that passed. Above it, the formula must be split into several calls (each cached), or summed in PPL. If even 1,000 characters fail, page-sized formulas (Fisher sums written out, likelihoods) must be split from the start. Each length's ms shows whether long texts are affordable on the G1.
- **T36, two-equation solve.** The "shape:" line is how a program must take the answer apart. With desktop Giac's `list[[2,1]]`, a program strips the prefix and the outer brackets: `cxToList`'s first-bracket to last-bracket rule leaves `[2,1]` inside braces, so it needs one more unwrap. Braces, semicolons, or `cxa=2` text each need a different parser, and the probe shows which. T36b shows whether exact fractions survive the normal equations (ScatterLab, TrendTest).
- **T37.** These are the forms a "where the formula comes from" page will show. Expect `normal()` to multiply out and reorder, so the display should not assume the student's factor order.
- **T38a.** `*` confirms fence rule 7 ("show * as ×") as written. A dot or × means that display substitution changes or is dropped.
- **T38b–d.** The list brackets (`[ ]` against `{ }`, and any `list` prefix) decide `cxToList`-style parsing in every program that reads CAS lists. A matrix prints `[[…],[…]]`.
- **T39.** If T39b passes, `convert(series(…),polynom)` gives a plain polynomial and ErrorRate's trawl line works as written. If the remainder survives, ErrorRate must strip `+…order_size(…)` itself, or drop `convert` and cut the text.
- **T40a–c.**
  - If they pass, ErrorRate's Poisson-limit line (erlPoiTerms, with `factor(limit(…))`) works.
  - The ms for T40c is the cost of its k ≤ 2 case; larger k is longer. If T40a passes but T40b fails, write the terms with `comb(n,k)`, and the reverse if not.
- **T41a**, how an infinite limit prints (input is T16's question):
  - `infinity` (desktop: `+infinity`) or `inf`: any program that tests an answer for infinity uses that word.
  - The glyph ∞ (8734): test for CHAR(8734).
  - ErrorRate line 2463's `erlInf` is the input spelling. It stays "inf" if T16 passed on its first call, and becomes "infinity" if only T16b passed. Desktop Giac: "inf" gives the signed `+infinity`, while "infinity" gives the unsigned `infinity` and a warning, so "inf" is preferable when both work.
- **T42 PASS.** `BINOMIAL_CDF(n, p, k)` is confirmed, and ErrorRate's bisection, StatDist and the harness are right. **FAIL**: every BINOMIAL_CDF call in the fleet needs review against GfxProbe T20's finding for BINOMIAL.

### MicroPython

- **T33a/b PASS**: MicroPython's integers are exact at any size, so Python can count exactly itself (RankLab's dynamic programme, comb). **FAIL** ("ERR …overflow"): keep exact counting in the CAS.
- **T33c PASS**: CAS text handed to Python through a PPL global is read back exactly. That is the safe route for "PPL calls the CAS, Python uses the answer" (ideas §2 rule 7).
- **T34a/b PASS**, with no reset on either calculator: `cas.caseval` works. Note its type (str or another) and its ms. Rule 7 could then allow it behind a guard; that is Roger's call. **A reset, or "no answer (crash?)"**: never use `cas.caseval`; PPL does the CAS calls and hands the text over as in T33c.

---

## 8 · Not settled by beta 1a, stated plainly

- **`#cas … #end` functions** were not tested, nor whether their names share the routine pool (ideas §6 items 2 and 7). A `#cas` block is a paste-time risk, and the fence (BRIEF_CAS rule 4) keeps them out of fleet programs. If the call-form tests all fail, they are beta 2's subject.
- **A direct dotted call in code** (`CAS.comb(100,50)` outside EXPR) was not tested: a paste-time risk. Corpus programs do it (fseries.hpprgm, Polysolver), and T10 tests the same call through EXPR.
- **HSeparator's effect on CAS output** (comma against dot in the answer text) is only inferred from T03 and T13. The probe does not change HSeparator to find out.
- **What the Prime prints** for `ln(20)`, `exp(…)`, `√`, `∞` and lists (`[…]` against `{…}`, `list[…]`, `poly1[…]`). The PASS rules are written to accept the likely variants, and every non-ASCII character is logged by code.
- **The CAS timeout and the break key** were not probed. A very slow G1 call can only be watched, not limited.
- **Whether `CX_LAST` survives a reset** is unknown. That is why the T34 instructions say to type it in Home before rerunning.
- **Beta 1a:** no length above 6,000 characters is tried. If T35d passes, the true limit is somewhere above that, and no fleet program needs more. How the Prime prints `list[…]`, `order_size` and `exp` is unknown; the pass rules accept the likely variants, and every shape is logged.
- **None of this has run on hardware.**

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
