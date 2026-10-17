# EpiStats v1.7a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v1.7 (16 Oct 2026); every v1.7 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). v1.7's `es_Cas` (`cR := STRING(CAS(esS));`) returned its own input, and nothing downstream could tell. EpiStats shows CAS answers as text, and the input was usually a plausible-looking formula:
  - **module 3, page 6**: the closed form for 0 or n read `(1/40)^(1/30)` with "exact (CAS)". That is right by luck, because the input *is* the closed form. For n = 1 it would have read `1-(1/40)^(1/1)` instead of `39/40`.
  - **Help F**: it would have shown `CAS: g'(p) = diff(ln(p/(1-p)),p)` (the question, not the derivative) and `= 1/12+1/5+1/8+1/30` (the sum, not the fraction 53/120), both under the badge "exact (CAS)". The harness reproduces this (verify, part G).
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime writes a square root with the root sign (T14b), so the n = 2 closed form reads `1-√(1/40)`.

## What changed (line numbers: v1.7 → v1.7a)

1. **`es_Cas`** (v1.7 735–760 → v1.7a 752–782): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + esS + ")" + CHAR(34) + ")"));` (v1.7a line 764). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0` (∞ and ±∞). v1.7's added badge line (`esCasOK`) is kept. The comments say why.
2. **No answer reader changed.**
   - Every answer is shown as the CAS writes it (`es_CasShow`: esq → p, * → ×).
   - The one test on an answer, `esDvC == "0"`, reads a `0`, which prints alike everywhere.
   - No CAS text assigns a variable; `esq` is only differentiated.
   - es_XCas's comment now gives the n = 2 form in the Prime's printing.
3. **Version strings and header**:
   - the banner and the in-file title comment (v1.7 239 → v1.7a 239);
   - **on screen**, the main menu's CHOOSE title (`EpiStats v1.7a ══════════`, still 25 characters; in `EpiStats()`, v1.7 454 → v1.7a 473);
   - the About page (`es_Help_About`, v1.7 5309 → v1.7a 5333);
   - the firmware paragraph and a "What changed in v1.7a" note.

   The CAS-kit box now names the call form.

Nothing else changed. The verify script checks this: the routines that differ from v1.7 are exactly `es_Cas`, `EpiStats` (the menu title) and `es_Help_About` (the version line), and outside them only comments differ.

## Verification

`verify_EpiStats_v1.7a.py` (from the v1.7 script, harness **ppl_run_v3b**), output in `verify_EpiStats_v1.7a_output.txt`: **ALL CHECKS PASSED, 98 checks** (v1.7's script: 91; the new ones are marked 1.7a).

- A, B (unchanged): Clopper–Pearson over 11,670 intervals, mid-P, and the conditional OR against SciPy, through the program's own routines. es_CPB, es_CPInt and es_BinCheck are line for line the same as CICatcher beta 2a's.
- C: every CAS template in desktop Giac, against Python fractions.
  - The derivative, its check `0`, the Help F fractions, and 130 closed forms for k = 0 and k = n.
  - 1.7a: in the Prime's printing the n = 2 forms read `1-√(1/40)` and `√(1/40)`. No answer contains "sqrt", and none is longer than desktop Giac's, so the 22-character limit on page 6 still holds.
- D, end to end:
  - **cas='giac'**: module 3 page 6 shows `exact lower = (1/40)^(1/30)` with "exact (CAS)". The CAS is asked once per row, on the tap, as `string(...)`. Help F shows `CAS: g'(p) = 1/p+1/(1-p)`, "(CAS: the difference is 0)", `= 53/120`, `SE = sqrt(53/120) = 0.6646` and the badge. 4 calls in the run. No CAS variable is assigned, and no CAS call takes a variable.
  - **cas='fail'**: the textbook forms, the decimals, "decimal", no error.
  - The CAS appears on one code line, in es_Cas, in the EXPR form.
- E: v1.6's suite (verify_EpiStats.py) passes on v1.7a.
- G (1.7a): v1.7 itself in v3b shows the bug above on Help F.

**Gate**: `python3 ppl_gate_v1a.py EpiStats_v1.7a.txt EpiStats_v1.7.txt`: **RESULT: PASS**.
- ppl_check_v3 matches v1.7, with no hard errors.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too. (Among them: "parameter 'a' collides with a builtin name".)
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the v1.7 checklist)

1. Help, F ("Where the SE comes from"). You should see `CAS: g'(p) = 1/p+1/(1-p)` (or the calculator's equivalent), "(CAS: the difference is 0)", and with the example table `= 53/120` and "exact (CAS)". If the line still reads `diff(...)`, the call form is not working: note it and skip the CAS steps.
2. Module 3 with a specificity of 30/30, page 6, tap the Spec row: `exact lower = (1/40)^(1/30) = …` and "exact (CAS)".
3. A table with n = 2 in a row and a count of 0 or 2: the closed form reads `1-√(1/40)` or `√(1/40)`, or however the calculator simplifies it. Write it down.
4. On the G1, time the first opening of Help F (two CAS calls) and of page 6 (one).
5. Afterwards, in the CAS view, `esq` has no value.
