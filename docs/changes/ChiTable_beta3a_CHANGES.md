# ChiTable beta 3a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3 (16 Oct 2026); every beta 3 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 3's `csCas` (`cR := STRING(CAS(csS));`) returned its own input. `csIsFr` then refused it, so every exact line fell back to the decimal: no 17/35, no χ² fraction, no counts of ways.
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12). It keeps every digit (T22: comb(1000,500), all 300).
- Fractions and integers print as on the desktop. A negative number has an ASCII hyphen: the emulator's `{-2,2}` (T38c) and `e^(-cxl)` (T40).

## What changed (line numbers: beta 3 → beta 3a)

1. **`csCas`** (beta 3 688–709 → 3a 703–730): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + csS + ")" + CHAR(34) + ")"));` (3a line 715). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0` (∞, and the ±∞ of 1/0). The comments say why.
2. **No answer reader changed.** Every answer ChiTable reads is a whole number or a fraction: the Fisher fraction, χ², ad − bc, r₁r₂c₁c₂, the ways, C(N, c₁). `csIsFr` already accepts digits, one `/` and a leading `-`, which is how the Prime prints them. No CAS text assigns a variable (the only CAS name is the summation index `csj` inside `seq`).
3. **Header**: version beta 3a, the firmware paragraph, a "WHAT CHANGED in beta 3a" note. The fence comment and csCas's head comment now say what CASProbe beta 1b found.

Nothing else changed. The verify script checks this: the only routine that differs from beta 3 is `csCas`, and outside it only comments differ.

## Verification

`verify_ChiTable_beta3a.py` (from the beta 3 script, harness **ppl_run_v3b**), output in `verify_ChiTable_beta3a_output.txt`: **5962 checks passed, 0 failed.**

- B, C: 18 edge tables, 300 random 2 × 2 and 150 random 2 × 3 / 3 × 2 tables. Every Fisher fraction, χ² fraction, ad − bc, product, count of ways and C(N, c₁) equals Python's exact arithmetic. The floats equal SciPy and the program's own `csFish` / `csX2`. The run structure in the program's template equals the exact-integer rule.
- D, end to end, the lady tasting tea typed in the grid:
  - **cas='giac'**: page 6 shows `p = 17/35 = 0.4857` with "exact (CAS)". Page 7 shows `= 2 = 2.000` and `34 of the 70 equally likely ways`. The Fisher plot shows `red + magenta: p = 17/35`. 6 CAS calls.
  - **cas='fail'**: the decimals, the "decimal" badge, "(the CAS did not answer: the decimal only)", no error, 4 attempts.
  - Example 2: `5549501668/421789635 = 13.157`, a 140-digit Fisher fraction counted rather than cut, and the ×10 table's "too big" line, with the 956-digit C(6740, 680) never sent. Examples 3 and 4: `3668733438511/122005828000 = 30.070`.
- D, quotes: every CAS text asks for `string(...)`, every answer arrives quoted, no quote reaches a page, no CAS variable is assigned, and no CAS call takes a variable.
- E: csCas is reached only from csXFisher and csXChi, which run when a page opens (csXEnsure). A bar drag, the critical-line drag and the morph make 0 calls. The device-tested routines (csCompute, csFisher and 15 others) are byte-identical to beta 2.
- G: beta 3 itself in v3b shows the emulator's finding (csXFr and csXX2 empty, a "non-literal" warning).

**Gate**: `python3 ppl_gate_v1a.py ChiTable_beta3a.txt ChiTable_beta3.txt`: **RESULT: PASS**.
- ppl_check_v3 gives 1 W3, the same as beta 3.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 3 checklist)

1. New table, 2 × 2, Values `3 1 1 3`, Run, then page 6. You should see `p = 17/35 = 0.4857` and "exact (CAS)". "decimal" here means the call form is not working on this calculator: stop the CAS steps and note it.
2. Page 7: `= 2 = 2.000` and `p = 34/70 = 17/35 = 0.4857`.
3. Examples, victim's race, page 7: `= 5549501668/421789635 = 13.157` and `p = 0.0001 (140-digit fraction)`.
4. On the G1, time how long page 6 takes to appear the first time; turning back to it is cached and should be instant.
5. Afterwards, in the CAS view, `csj` has no value.
