# ScatterLab beta 2a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 2 (16 Oct 2026); every beta 2 feature is kept, and the user's guide (`scatterlab-guide_beta2.md`) still applies. Not yet run on hardware or on the emulator. The beta 2 device checklist is in `ScatterLab_beta2_NOTES.md`.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 2's `slCas` (`cR := STRING(CAS(slS));`) returned its own input. The echoed solve text still held `sla`, so `slCxSol` refused it, and the "Least squares as calculus" page always showed the decimal normal equations with "decimal". The harness reproduces this (verify, part G).
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime prints the solve of a system with braces round a vector: `{[2,1]}`, `{[23/10,4/5]}` (T36). Desktop Giac prints `list[[2,1]]`. Polynomials and fractions print alike.

## What changed (line numbers: beta 2 → beta 2a)

1. **`slCas`** (beta 2 306–327 → beta 2a 322–349): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + slS + ")" + CHAR(34) + ")"));` (2a line 334). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0`. The comments say why.
2. **No answer reader needed a code change.**
   - `slCxSol` (2a 1386) already drops braces and brackets, so the Prime's `{[a,b]}` reads as `a,b`. Its `list` removal is harmless dead code on the Prime. Its **comment** now names the Prime's form (CASProbe T36).
   - `slCxClean` reads the same everywhere.
   - No CAS text assigns a variable: `sla` and `slb` are solved for.
3. **Header**: version beta 2a, the firmware paragraph, a "What changed in beta 2a" note. The CAS-kit box and the beta 2 note name the call form.

Nothing else changed. The verify script checks this: the only routine that differs from beta 2 is `slCas`, and outside it only comments differ.

## Verification

`verify_ScatterLab_beta2a.py` (from the beta 2 script, harness **ppl_run_v3b**), output in `verify_ScatterLab_beta2a_output.txt`: **33 PASS, 0 failure(s)** (beta 2's script: 27).

- Part A (unchanged): every template for the data sets in desktop Giac. SSE, derivatives and solve equal SymPy, exact fractions and statsmodels OLS. 2a: in the Prime's printing every solve answer is `{[a,b]}` and the polynomials are unchanged.
- Part B:
  - slCxMake builds exactly the SSE text, and the PPL reads the braces as the exact fractions for every set.
  - **cas='giac'**: tapping the equation opens the page. It shows `b = 2441/2394   (program 1.019632)`, `a = 3186173/191520   (program 16.63624)`, the `x = 10.4 is 104/10` note and "exact (CAS)". 4 calls, all asking for `string(...)`, the solve answer arriving as `"{[…]}"`. No CAS variable is assigned, and no CAS call takes a variable.
  - The menu path is cached. A drag makes no CAS call, and the page afterwards fits the moved points.
  - **cas='fail'**: "decimal", the normal equations with the program's sums, no error.
- B, canned answers (2a): answers in the calculator's form (quoted, braces) give the exact page.
- G (2a): beta 2 itself in v3b shows "decimal" and no fractions.

**Gate**: `python3 ppl_gate_v1a.py ScatterLab_beta2a.txt ScatterLab_beta2.txt`: **RESULT: PASS**.
- ppl_check_v3 is clean.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 2 checklist)

1. Data, the first example (Poverty vs crime, synthetic), then tap the equation in the panel. You should see `b = 2441/2394   (program 1.019632)`, `a = 3186173/191520   (program 16.63624)` and "exact (CAS)". "The CAS did not answer" with "decimal" means the call form is not working: note it.
2. Drag a point, then open the page again: asked once more, with the new line.
3. On the G1, time "asking the CAS ..." (four calls).
4. Afterwards, in the CAS view, `sla` and `slb` have no value.
