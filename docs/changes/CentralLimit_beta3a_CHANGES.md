# CentralLimit beta 3a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3 (16 Oct 2026); every beta 3 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 3's `cltCas` (`cR := STRING(CAS(cltS));`) returned its own input.
  - The program checks every answer by value, re-feeding it to the CAS as `round(evalf(...)*10^E)` and comparing with its own number. Those checks refused everything, since an echoed `expand(sum(...))` still says "sum" and an echoed `round(...)` holds no number.
  - So the exact-curve page always said "no closed form shown" and the MGF page always showed the decimal M(1) line. The harness reproduces this (verify, part 4).
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12), and a 297-digit peak fraction crosses whole (T22).
- The Prime prints the MGF limit as `e^(cxt^2/2)` (T17), not `exp(...)`.

## What changed (line numbers: beta 3 → beta 3a)

1. **`cltCas`** (beta 3 584–603 → beta 3a 603–630): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + cltS + ")" + CHAR(34) + ")"));` (3a line 615). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0` (∞ and ±∞). The comments say why.
2. **No answer reader changed.** The answers are checked **by value**, not by their text (cltCasNum with cltIVal). The text tests only look for an unevaluated `sum`, `limit`, `series` or `order`, which print the same everywhere. Re-feeding an answer in the Prime's printing works (`subst(e^(cltqt^2/2),cltqt,1)`; verify part 2). No CAS text assigns a variable. Two comments (the header's beta 3 list and cltMgf's head) now say the limit reads `e^(t^2/2)`.
3. **Header**: version beta 3a, the firmware paragraph, a "beta 3a" note.

Nothing else changed. The verify script checks this: the only routine that differs from beta 3 is `cltCas`, and outside it only comments differ.

## Verification

`verify_CentralLimit_beta3a.py` (from the beta 3 script, harness **ppl_run_v3b**), output in `verify_CentralLimit_beta3a_output.txt`: **RESULT: ALL PASS, 77 checks** (beta 3's script: 71; the new ones are marked 3a).

- Part 1 (unchanged): the program's 12-digit Irwin–Hall sum, the symmetry, the rescaling.
- Part 2: every template in desktop Giac against SymPy and fractions: 92 polynomial pieces, 19 exact peaks, the check numbers, the MGF limit and series. 3a: the limit in the Prime's printing is `e^(cltqt^2/2)`, exactly what CASProbe T17 saw, and re-fed as the program re-feeds it, it gives round(e^½ × 10⁹).
- Part 3, end to end:
  - **cas='giac'**: the exact-curve page for n = 1 … 100 shows "exact (CAS)" and the exact peak (n = 9: `259723/573440`; above 40 characters, "fraction of N digits"). The MGF page shows `CAS: as n grows, M(t) -> e^(t^2/2):` (no `exp(`), the series `-1/12×t^4/n+1/2×t^2`, and the badge. Every CAS text asks for `string(...)`. No CAS variable is assigned, and no CAS call takes a variable.
  - **cas='fail'**: "decimal", "no closed form shown", the M(1) line, no error.
  - No CAS call while sampling, drawing, in a drag preview or in the one-sample animation.
- Part 4 (3a): beta 3 itself in v3b shows the emulator's finding.

**Gate**: `python3 ppl_gate_v1a.py CentralLimit_beta3a.txt CentralLimit_beta3.txt`: **RESULT: PASS**.
- ppl_check_v3 gives 9 E1 and 23 E7, the same as beta 3 (the app's Statistics-app names); none is a hard error.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 3 checklist)

1. A uniform population, n = 9, then menu "Exact curve (uniform)". You should see two polynomial pieces and `exact: 259723/573440 = 0.452920968` with "exact (CAS)". "no closed form shown" with "decimal" means the call form is not working: note it.
2. Menu "Why the bell? (MGF)": `CAS: as n grows, M(t) -> e^(t^2/2):` and `CAS: ln M(t) = … + ...` with "exact (CAS)". Write down exactly how the calculator prints both.
3. On the G1, time the "Asking the CAS" pause on both pages, at n = 4 (10 calls) and n = 9 (6 calls). Both pages are kept, so a second opening should be instant.
4. Afterwards, in the CAS view, `cltqs`, `cltqt`, `cltqn` and `cltqu` have no value.
