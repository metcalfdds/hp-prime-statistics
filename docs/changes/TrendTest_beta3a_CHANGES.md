# TrendTest beta 3a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3 (16 Oct 2026); every beta 3 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 3's `trCas` (`cR := STRING(CAS(trCs));`) returned its own input. The echoed solve text still held `tra`, so `trCxSol` refused it, and page 4, "Least squares as calculus", always showed the decimal normal equations with "decimal". The harness reproduces this (verify, part G).
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime prints the solve of a system with braces round a vector: `{[2,1]}`, `{[23/10,4/5]}` (T36). Desktop Giac prints `list[[2,1]]`. Polynomials and fractions print alike.

## What changed (line numbers: beta 3 → beta 3a)

1. **`trCas`** (beta 3 471–492 → beta 3a 487–514): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + trCs + ")" + CHAR(34) + ")"));` (3a line 499). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0`. The comments say why.
2. **No answer reader needed a code change.**
   - `trCxSol` (3a 1078) already drops braces and brackets, so the Prime's `{[a,b]}` reads as `a,b`. Its `list` removal is harmless dead code on the Prime, kept for desktop Giac. Its **comment** now names the Prime's form (CASProbe T36).
   - `trCxClean` (a decimal point means approximate mode) reads the same everywhere.
   - No CAS text assigns a variable: `tra` and `trb` are solved for.
3. **Header**: version beta 3a, the firmware paragraph, a "beta 3a" note. The CAS-kit box and the beta 3 note name the call form.

Nothing else changed. The verify script checks this: the only routine that differs from beta 3 is `trCas`, and outside it only comments differ.

## Verification

`verify_TrendTest_beta3a.py` (from the beta 3 script, harness **ppl_run_v3b**), output in `verify_TrendTest_beta3a_output.txt`: **37 PASS, 0 failure(s)** (beta 3's script: 31).

- Part A (unchanged): every template for 15 tables (three examples × three score modes, decimals, negatives, ties, a zero cell, two levels, large primes) in desktop Giac. The SSE, both derivatives and the solve equal SymPy and exact fractions, and WLS = OLS(0/1) = exact (statsmodels). 3a: in the Prime's printing every solve answer is `{[a,b]}` and the polynomials are unchanged.
- Part B:
  - trCxMake builds exactly the SSE text, and the PPL reads the solve's answer in braces as the exact fractions for every table.
  - **cas='giac'**, snoring page 4: `b = 95339/4757909   (program 0.02003800)`, `a = 80277/4757909`, "exact (CAS)". 4 calls, all asking for `string(...)`, the solve answer arriving as `"{[…]}"`. No CAS variable is assigned, and no CAS call takes a variable. The answers are cached.
  - The Scores key re-asks (midranks, the 16985/10 note). A drag makes no CAS call. Restore works. A 1/3 score sends nothing. The stale-key run skips no page.
  - **cas='fail'**: "decimal", the normal equations with the program's sums, no error.
- G (3a): beta 3 itself in v3b shows "decimal" and no fractions.

**Gate**: `python3 ppl_gate_v1a.py TrendTest_beta3a.txt TrendTest_beta3.txt`: **RESULT: PASS**.
- ppl_check_v3 is clean.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 3 checklist)

1. Examples, snoring, Right three times (page 4). You should see the SSE as a polynomial in a and b, both derivatives `= 0`, `b = 95339/4757909   (program 0.02003800)`, `a = 80277/4757909   (program 0.01687233)` and "exact (CAS)". "The CAS did not answer" with "decimal" means the call form is not working: note it.
2. `+` twice on page 4 (midranks): asked again; the note `Exact: score 1698.5 = 16985/10`.
3. On the G1, time "asking the CAS ..." on page 4 (four calls, the SSE sent four times).
4. Afterwards, in the CAS view, `tra` and `trb` have no value.
