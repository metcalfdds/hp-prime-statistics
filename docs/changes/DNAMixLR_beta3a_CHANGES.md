# DNAMixLR beta 3a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3 (16 Oct 2026); every beta 3 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 3's `dmCas` (`cR := STRING(CAS(dmS));`) returned its own input. The input has no decimal point, so the approximate-mode test passed it. The locus page's formula view would have shown the program's own unsimplified sum, e.g. `theta = 0: LR = factor(normal((1)/…`, under the badge "exact (CAS)". The harness reproduces this (verify, part G).
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12). Long text is fine: 6,005 characters in one call (T35), against dmCasMx = 3000.

## What changed (line numbers: beta 3 → beta 3a)

1. **`dmCas`** (beta 3 486–506 → beta 3a 502–529): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + dmS + ")" + CHAR(34) + ")"));` (3a line 514). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0` (∞ and ±∞). The comments say why.
2. **No answer reader changed.**
   - The LR formula is a ratio of polynomials in the p's and θ, which the Prime prints as desktop Giac does: the verify checks all 39 template answers.
   - The one test, a decimal point meaning approximate mode, reads the same everywhere.
   - `dmFxShow` only swaps names and `*`.
   - No CAS text assigns a variable (`dmq1…`, `dmt` stay symbols).
3. **Header**: version beta 3a, the firmware paragraph, a "What changed in beta 3a" note. The CAS-kit box and the beta 3 note name the call form.

Nothing else changed. The verify script checks this: the only routine that differs from beta 3 is `dmCas`, and outside it only comments differ. `dmProb`, `dmKnowns`, `dmTyped` and `dmEval` are still byte-for-byte beta 2's.

## Verification

`verify_DNAMixLR_beta3a.py` (from the beta 3 script, harness **ppl_run_v3b**), output in `verify_DNAMixLR_beta3a_output.txt`: **39 PASS, 0 failure(s)** (beta 3's script: 32).

- Part A: every template (20 cases, 6 presets) in desktop Giac, read by SymPy, equals the Python engine at 6 θ × 6 frequency sets to 1e-10. 3a: every answer prints the same on the Prime.
- Part B:
  - The PPL's dmCasLR text equals the Python builder's, and the CAS answer equals dmEval.
  - dmEdge equals brentq.
  - **cas='giac'**: the formula view shows `LR = (3×th+1)×(4×th+1)/(2×(th×p15-th-p15)×(p14×th-p14-th))`, `theta = 0: LR = 1/(2×p15×p14)`, the value line and "exact (CAS)". 2 calls; both ask for `string(...)` and arrive quoted. No quote reaches the screen. No CAS variable is assigned, and no CAS call takes a variable. The cache holds.
  - **cas='fail'**: "decimal", "The CAS did not answer: no formula here.", the value line, no error.
  - The long and the too-long formulas are counted, not cut. The θ drag makes no CAS call. The stale-key run skips no page.
- G (3a): beta 3 itself in v3b shows its own text as the formula.

**Gate**: `python3 ppl_gate_v1a.py DNAMixLR_beta3a.txt DNAMixLR_beta3.txt`: **RESULT: PASS**.
- ppl_check_v3 is clean.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 3 checklist)

1. Load the worked example, plot LR by locus, tap bar 1 twice (the locus page), then press `-` for the formula view. You should see `LR = (3×th+1)×(4×th+1)/(2×(th×p15-th-p15)×(p14×th-p14-th))` (or the calculator's equivalent), `theta = 0: LR = 1/(2×p15×p14)` and "exact (CAS)". If the lines start with `factor(normal(`, the call form is not working: note it.
2. Right and Left through the loci: "asking the CAS ..." once per new locus, then instant.
3. On the G1, time the first formula view (two CAS calls).
4. Afterwards, in the CAS view, `dmt` and `dmq1` have no value.
