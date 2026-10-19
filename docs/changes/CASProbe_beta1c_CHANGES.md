# CASProbe beta 1c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 1b; every test keeps its number and its code. The two `#PYTHON` blocks are byte-identical, and the probe's own call forms (`cxCall`, `cxObj`, `cxPickForm`) are unchanged. Beta 1c itself has not run on hardware or on the emulator. Read `CASProbe_beta1a_NOTES.md` for the test list and `CASProbe_beta1b_NOTES.md` for the call form.*

## Why: what emulator round 2 showed

Beta 1b ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) on 17 Oct 2026. It reported CAS available, call form 2, 42 pass, 8 fail, 19 values and 0 errors (`Emulator_Round1_Results_2026-10-17_v1.md`). Round 2 then found, typed in Home (`BRIEF_R2FIX_v1.md` §0):

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `LEFT("abc", 0)` | `"abc"`, the whole string |
| `MID("abc", 0, 1)` | **Error: Bad argument type** |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: **scientific**, with U+1D07 for the E |

**What that means for beta 1b.** Every test runs inside IFERR, so nothing stops the whole probe. But a failed CAS call stopped its **test**:
- `cxEq`, `cxHas` and `cxVal` hand the failed call's "" to `cxShow`;
- `cxShow` passes it to `cxFlat`, which looks for a line break with `INSTRING("", CHAR(10))`;
- the test then ends with ERROR, not with the FAIL "CAS error" line it had already written, and its later calls never run.

Harness v3d shows it. With the CAS answering the call-form tests and failing every later call, beta 1b stops **21 tests** with ERROR. The same pattern sat in five more places:
- `cxSplit` (an empty `CX_PYS`, or a `;` at the very end);
- `cxPyType` (an empty field, or a quote at the end);
- T25 (`cxq+1` failing the second time);
- T39 (an empty `cxVal` answer);
- T34b (an empty field).

Two of them also hit **LEFT(s, 0) = the whole string**:
- `cxSplit` on `";a"` gave `{";a", "a"}`;
- `cxPyType` on two quotes in a row gave `'`;
- and `cxFlat` on a text that starts with a line break would never end: each pass put the whole text back.

The kit's `cxCas` has the same `INSTRING(cR, "undef")` on a possibly empty `cR` that every fleet kit had.

## What changed (line numbers: beta 1b → beta 1c)

1. **`cxCas`, the kit** (499–510 → 537–553). The undef/"rror" test runs only when `DIM(cR) > 0` (508 → 546–551). This is the round-2 fix every fleet kit got. The `STRING(CAS(cxS))` line stays as T07 tests it, "as written".
2. **`cxFlat`** (283–295 → 311–330), which every result line passes through. It looks for a line break only while text is left. It builds the result piece by piece and takes `LEFT` only past position 1. One new LOCAL, `fR`.
3. **`cxSplit`** (363–377 → 398–415), the reader of Python's `;`-separated answers.
   - It looks only while text is left, and an empty separator returns the text whole.
   - A `;` at position 1 gives an empty field. `LEFT(s, 0)` used to return the whole string there.
4. **`cxPyType`** (1715–1725 → 1810–1826). It returns at once for an empty text, or for nothing after the first quote. Two quotes in a row give "".
5. **T25** (1158 → 1201). `vA` and `vD` are tested with `DIM` first (1169, 1185 → 1212–1215, 1231–1233). An empty `vD` (the call failed) reads as "cxq still set after purge", a FAIL, not an ERROR. One new LOCAL, `vK`.
6. **T39** (1498–1499 → 1546–1550). The two remainder notes run only when `DIM(sA) > 0`.
7. **T34b** (1868 → 1969–1971). `INSTRING(pL(5), "35/128")` runs only when the field is not empty. One new LOCAL, `pK`.
8. **`cxLineCol`, the pager** (1966 → 2070–2075). An empty line is drawn in black. `CX_LOG` is a Home variable, and the pager runs outside every IFERR, so an empty line would stop the probe at its very end.
9. **New test T43** (no CAS; 1629–1671), run after T42 and before the Python tests, under a "-- T43 (added in beta 1c) --" line:
   - **T43a:** `INSTRING("", "a")` inside IFERR. PASS = an error, as on the emulator.
   - **T43b:** `STRING(0.096, 2, 1)`. PASS = exactly `"9.6" + CHAR(7431) + "-2"`. The log lists its character codes, `57 46 54 7431 45 50`.
   - **T43c:** `STRING(ROUND(0.096, 1), 2, 1)`, the fleet's cure. PASS = `"0.1"`.
   - Two new summary lines in the log: "INSTRING of an empty string: an error" (or "NO error") and "STRING(0.096, 2, 1): scientific" (or "NOT scientific").
   - New file-level LOCALs `cxIns0` and `cxSci` (192), set in `cxInit` (221), and one line in `cxRun` (2028).
10. **Version strings and header.**
    - The banner, the progress page (456 → 494), the summary page (1935 → 2039), the menu title (2037 → 2144) and the log's first line (2047 → 2154) read beta 1c.
    - A "WHAT CHANGED IN BETA 1c" paragraph, the firmware line (beta 1b's emulator result), and T43 in the test list.
    - The comments inside the two `#PYTHON` blocks still say "beta 1b", because the blocks are left byte-identical, as the brief asks.

**Not changed, and why:**
- **The other INSTRINGs** (41 calls in all) cannot meet "":
  - `cxHas`, `cxHas2`, T23, T26, T36a, T38a (`cxMulSign`) and T41a test only when `cxErr` = 0, and then the text is `STRING()` of something, never "";
  - `cxVerdict50` tests only in the ELSE of `IF fT == ""`;
  - `cxShape` has already returned "no brackets" for an empty text.
- **Every other LEFT count and MID start is 1 or more:**
  - `cxNote`: 46, `nB - 1` ≥ 24, and MID at `nB` ≥ 25;
  - `cxShort`: `sN - 3` ≥ 9, `sN - 14` ≥ 10, and MID at `sD - 8` ≥ 16;
  - T22: LEFT 6, and MID at `gD - 5`, only when `gD` ≥ 6;
  - `cxShape`: `kP - 1`, only past 1;
  - `cxStrip` and `cxRest`: starts of 2 or more.
- **The one `STRING(x, 2, d)` in beta 1b** (T42, `STRING(bV, 2, 6)`) shows 0.044179 unless BINOMIAL_CDF itself is wrong. A probe should then record what the Prime printed, scientific or not.

Nothing else changed. The routines that differ from beta 1b are exactly these 14: `CASProbe`, `cxBegin`, `cxCas`, `cxFlat`, `cxInit`, `cxLineCol`, `cxPyType`, `cxRun`, `cxSplit`, `cxSummary`, `cxT25`, `cxT34`, `cxT39` and the new `cxT43`. Outside them, only comments and the new LOCAL line differ.

## Verification

`verify_CASProbe_beta1c.py`, built from `verify_CASProbe_beta1a.py`, the newest verify script for the probe, runs in **ppl_run_v3d**. Output in `verify_CASProbe_beta1c_output.txt`: **ALL CHECKS PASS, 186 checks.**

**Why the expectations changed.** The beta 1a script was written for harness v3, before the emulator. v3 answered `CAS(variable)`, kept big integers exact and printed desktop Giac's text, so its expectations were "form 1 works". On the emulator beta 1b found otherwise, and v3d models what it found. Every beta 1a check is kept; where the emulator answered differently, the expected value is now the emulator's, and the check line says "emulator". The changed expectations:
- **The call forms:** form 2; T01, T04, T05, T06, T07, T10, T32 and T34a FAIL, which are the emulator's 8.
- **Printing:** T36a's shape is `{[]}`, and T41a's limit prints as the glyph.
- **CAS variables persist** (T25a).
- **The device variants:** D1, D6 and D8 are now the default behaviour. D2 and D4 are restated for the EXPR form.

**C0, the emulator's run:**
- **beta 1b in v3d reproduces the emulator exactly:** 42 pass, 8 fail, 19 values, 0 errors, with the same 8 FAILs;
- **beta 1c:** 45 pass, 8 fail, 19 values, 0 errors, the extra three being T43a–c;
- its log is beta 1b's line for line, except the version line, the 7-line T43 block, the two new summary lines and the tally.

**C1–C8, kept:**
- every test the emulator passed passes, along with T43a–c;
- the menu, the warning page, the crash marker and stale keys behave as before;
- every log line is 46 characters or fewer.

**C9, the new case** (the CAS answers the call-form tests, then fails every later call):
- beta 1b stops 21 tests with ERROR;
- beta 1c stops none: each later test logs "CAS error" and goes on to its next call (checked on T11, T16, T21a and T21b, T27–T30, T40a–c and T41a–b), and T25 and T39 log and go on;
- form 2 is still chosen.

**D10:** with `INSTRING("")` = 0 and `STRING(0.096, 2, 1)` = "0.1" (the rules not as the emulator showed them), T43a and T43b FAIL, and the summary says "NO error" and "NOT scientific".

**F, the helpers on edge inputs:**
- `cxFlat` on "", on a break at the start, on a lone break and on two breaks in a row;
- `cxSplit` on "", `";a"`, `";"`, `"a;;b"`, `"noimport;"` and an empty separator;
- `cxPyType` on "", `'` and `''`;
- `cxLineCol("")`.

Beta 1b, run on the same inputs, stops on 4 and gets 2 wrong. Its `cxFlat` on a leading break is not run, because it would never end.

**G:** the routine diff is as listed; the `#PYTHON` blocks and the three call-form routines are unchanged; no code line says beta 1b.

**H:**
- the only scientific `STRING` result in all 21 beta 1c harness runs is T43b's own `9.6ᴇ-2`;
- all 41 INSTRINGs are listed, each with the guard or the reason it cannot meet "";
- every LEFT count and MID start is listed.

## Gate

`python3 ppl_gate_v1b.py CASProbe_beta1c.txt CASProbe_beta1b.txt` (in `gate_r2`) gives **RESULT: PASS**.
- ppl_check_v4: clean, as beta 1b. No hard error, E12 included.
- lint_ppl: 73 problems against beta 1b's 71. Both have the depth error at the `#PYTHON` block's `#END`, the EXPORT-discipline lines for the `CX_*` results, and the bare-string concatenation notes. The 2 new ones are noise too: one more INSTRING read as a 2-argument STRING, and T43c's `STRING(ROUND(0.096, 1), 2, 1)` read as 4 arguments.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 built-in matches (`sxA`… `sxE`, `cxIns0`, `cxSci`, `fR`, `vK`, `pK` are new).
- `check.sh` runs the parts the gate skips without the kit zip:
  - the hp-prime-kit lint: **1 error**, "unbalanced", the same as beta 1b's. The kit counts a `#PYTHON` block's lines.
  - the full parse fails at line 178, "expected a name after EXPORT". Beta 1b fails the same way at its line 152. That is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Paste (replace beta 1b in the Kit; the two share every routine name), then Program Catalog → CASProbe → Edit → Check: no error.
2. Run every test. On the emulator, expect **45 pass, 8 fail, 19 values, 0 errors**: beta 1b's 42 / 8 / 19, plus T43a–c. The FAILs are T01, T04, T05, T06, T07, T10, T32 and T34a, as in beta 1b.
3. **T43 in the log:**
   - `T43a PASS INSTRING of an empty string is an error`;
   - `T43b PASS STRING(0.096, 2, 1) is scientific` with `= 9.6ᴇ-2, codes 57 46 54 7431 45 50`;
   - `T43c PASS STRING(ROUND(0.096, 1), 2, 1) = 0.1`;
   - and in the summary, "INSTRING of an empty string: an error" and "STRING(0.096, 2, 1): scientific".
4. **On the G2, then the G1:** the same three lines. **A FAIL on T43a or T43b is a finding.** It means the calculator's firmware behaves differently from the emulator's, and the fleet's guards are then insurance, not a fix. Copy the log (Edit ▸ Copy on CX_LOG).
5. On the G1, note the "slowest call" on the summary page (the open question since beta 1).
