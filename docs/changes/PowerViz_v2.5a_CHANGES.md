# PowerViz v2.5a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v2.5 (16 Oct 2026); every v2.5 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). v2.5's `pv_Cas` (`cR := STRING(CAS(pv_S));`) returned its own input, `solve(...,pvn)`. `pv_CasUse` refused it because `pvn` was still in it, so the "Where the formula comes from" page always showed the textbook form with "decimal".
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime prints a solve with braces, `{1/20}` (T18), and a square root with the root sign, `√2` (T14b, T21a).

## What changed (line numbers: v2.5 → v2.5a)

1. **`pv_Cas`** (v2.5 367–388 → v2.5a 384–411): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + pv_S + ")" + CHAR(34) + ")"));` (v2.5a line 396; the file's one-space indent kept). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0` (∞ and ±∞). The comments say why.
2. **No answer reader needed a code change.**
   - `pv_Strip` already drops braces, which is the Prime's solve form; its leading-`list` step is harmless dead code on the Prime, kept for desktop Giac.
   - `pv_CasUse` tests only for the CAS names, `,` and `.`, which print the same.
   - `pv_Disp` turns `sqrt` into the root sign. On the calculator the CAS already writes √, so that step finds nothing there and the answer is shown as it is.

   The **comments** of `pv_Strip` and `pv_Disp` now say what the emulator showed. No CAS text assigns a variable: `pvn` is solved for, and `pvza`, `pvzb`, `pvs` and the others stay symbols.
3. **Header**: version v2.5a, the firmware paragraph, a "v2.5a — what changed" note.

Nothing else changed. The verify script checks this: the only routine that differs from v2.5 is `pv_Cas`, and outside it only comments differ.

## Verification

`verify_PowerViz_v2.5a.py` (from the v2.5 script; harness **ppl_run_v3b**), output in `verify_PowerViz_v2.5a_output.txt`: **62 PASS, 0 FAIL** (v2.5's script: 55; the new checks are marked 2.5a).

- A1–A5 (unchanged): the mathematics of every template in desktop Giac, against SymPy, the PPL closed form and statsmodels (448 values over 7 alphas and 2 tails).
- A6 (2.5a): all 4 symbolic and 32 numeric templates, read as pv_Cas receives them on the calculator, arrive in braces with the root sign. Example: `{((√(-pvp^2+pvp)*pvza+√(-pvr^2+pvr)*pvzb)/pvd)^2}`. Each passes pv_CasUse and has the value of desktop Giac's answer.
- B, end to end, every test and both tails:
  - **cas='giac'**: the formula page shows "exact (CAS)", the CAS solve and the CAS line with the student's numbers. Test 3 shows `n = (5×zα+2×√6×zβ)^2`, with the Prime's root sign and no "sqrt". Every CAS text asks for `string(...)`. No CAS variable is assigned, and no CAS call takes a variable.
  - The CAS is asked only on opening the page, and only when the test or the values change (3 calls over 5 openings). Drags make 0 calls.
  - **cas='fail'**: "decimal", the textbook form, the PPL numbers, no error.
- B10 (2.5a): canned answers in the calculator's form (quoted, braces) give the exact page. A decimal answer is refused.
- B12: v2.4's verification run against v2.5a gives 64 PASS, and the only FAIL is the intended help-page count.
- G (2.5a): v2.5 itself in v3b shows the emulator's finding: the textbook form, "decimal", and a "non-literal" warning.

**Gate**: `python3 ppl_gate_v1a.py PowerViz_v2.5a.txt PowerViz_v2.5.txt`: **RESULT: PASS**.
- ppl_check_v3 gives 5 E1, 173 E7 and 14 E9, the same as v2.5; none is a hard error. They come from the `LOCAL pv_Name()` heads, which LocalHeadProbe passed on the emulator.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the v2.5 checklist)

1. One mean, defaults, then tap the n₈₀ panel (or Menu, "Sample-size formula"). You should see "exact (CAS)", `CAS, solved for n:` and `n = ((σ×zα+σ×zβ)/(μ₁−μ₀))^2`, then `n = (3×zα+3×zβ)^2`. "decimal" with the textbook form means the call form is not working on this calculator: note it and skip the CAS steps.
2. One proportion: the CAS line should carry the root sign, e.g. `n = (5×zα+2×√6×zβ)^2`. Write down exactly how the calculator prints it.
3. On the G1, time how long the page takes to open the first time, and the second time (cached, instant).
4. Afterwards, in the CAS view, `pvn` has no value.
