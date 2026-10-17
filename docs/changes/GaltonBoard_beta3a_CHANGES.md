# GaltonBoard beta 3a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3 (16 Oct 2026); every beta 3 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 3's `gbCas` (`cR := STRING(CAS(gbS));`) therefore returned its own input: the bar panel's exact fraction failed `gbIsFr` and fell back to the decimal, and the Poisson page never had an answer.
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08): the answer comes back as text in double quotes.
- The Prime prints exp(u) as `e^(u)` (T17: `e^(cxt^2/2)`; T40: `1/2*cxl^2*e^(-cxl)`), never `exp(`; a limit to infinity prints `∞` (U+221E).

## What changed (line numbers: beta 3 → beta 3a)

1. **`gbCas`** (beta 3 388–408 → 3a 409–436): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + gbS + ")" + CHAR(34) + ")"));` (3a line 421). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0`, so ∞ and ±∞ count as failures like undef. The comments say why.
2. **`gbPsLim`** (beta 3 537–560 → 3a 588–629): beta 3 refused any answer without `"exp"` in it (line 555). On the Prime the answer reads `…e^(-4)…`, so the Poisson limit could never have shown. Now:
   - the `"exp"` and `"inf"` text tests are gone (gbCas refuses an infinity);
   - an answer still holding `"limit"` (unevaluated) is refused as before;
   - **the answer is checked by its value**: the CAS is asked for `round(evalf(<answer>)*10^E)` (E puts about ten digits before the point), and that whole number must match PPL's `POISSON(mu, k)` to 6 significant digits. Anything else keeps the decimal and the "decimal" badge.
   The page now makes two CAS calls per new k, not one; both are cached as before (an event, never a frame).
3. **New helper `gbIVal`** (3a 564–586): reads that whole number digit by digit (no EXPR, no Home number format). Its LOCALs are on two lines, six and then one (`ivOK`), within the house limit of six a line. It is tagged `gb`, and fleet_names_v2 finds no clash.
4. **Header**: version beta 3a, the firmware paragraph, a "WHAT CHANGED in beta 3a" note. Comments that said the call form was still to be decided (the `gbInf` note, the fence box, gbCas's head) now say what CASProbe beta 1b found. T16 passed with `inf` on the emulator, so `gbInf` stays `"inf"`.

Nothing else changed. The verify script checks this: the routines that differ from beta 3 are exactly `gbCas`, `gbIVal` and `gbPsLim`, and outside them only comments differ.

## Verification

`verify_GaltonBoard_beta3a.py` (from the beta 3 script, harness **ppl_run_v3b**), output in `verify_GaltonBoard_beta3a_output.txt`: **4114 checks passed, 0 failed.**

- B: every bin for R 3–12, all k, 8 values of p: the exact fraction equals Python's `Fraction` and SciPy's `binom.pmf`, with one CAS call per new bar.
- C: the Poisson limits for 7 boards and every k are in the Prime's printing (no `exp`). Read with e = Euler's number, each equals μ^k e^(−μ)/k! exactly (SymPy) and `poisson.pmf` to 1e-12. There is one value check per limit.
  - A canned wrong limit (33/(3e⁴)) is refused by its value.
  - The right one is kept.
  - An unevaluated limit holding ∞ is refused, with no value asked.
- D, end to end:
  - **cas='giac'**: the panel shows `= 35/128 = 0.2734` with "exact (CAS)". The Poisson page at k = 3 shows `as R → infinity = 32/(3×(e^(1))^4)` and the badge. 7 CAS calls; no CAS variable assigned; no CAS call of a variable.
  - **cas='fail'**: the decimal, the "decimal" badge, "(the CAS did not answer)", no error, 4 attempts.
- D, quotes: every CAS text asks for `string(...)`, every answer arrives quoted, and no quote reaches the screen.
- E: gbCas is reached only from gbBinInfo and gbPoisson (events); no animation, drag or frame reaches it; the routines beta 3 kept byte-identical to beta 2 still are.
- G: beta 3 itself in v3b shows the emulator's finding (no fraction, no limit, a "non-literal" warning).

`(e^(1))^4` is how harness v3b writes desktop Giac's `exp(1)^4` so that the text reads back with the same meaning. The Prime may print it differently (perhaps `e^4`). The value check does not depend on the printing.

**Gate**: `python3 ppl_gate_v1a.py GaltonBoard_beta3a.txt GaltonBoard_beta3.txt`: **RESULT: PASS**.
- ppl_check_v3 is clean.
- lint_ppl has no new problems; the "final depth −1" is in beta 3 too (its #PYTHON block). The extra INSTRING on the reject line, which the lint reads as a 2-argument STRING(), is offset by the two INSTRING tests removed from gbPsLim.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.
- Run with hp-prime-kit available, the kit lint gives the same single "unbalanced" error as beta 3 (the #PYTHON block). The parse stops on the same EXPORT line as beta 3's.

## Device checklist (after the beta 3 checklist)

1. Tap bar 4 with R = 8, p = 0.50. You should see `= 35/128 = 0.2734` and "exact (CAS)". If you see "decimal", the call form is not working on this calculator: note it and stop the CAS steps.
2. Menu, "Where Poisson comes from (CAS)", then k = 3 (Right). You should see "asking the CAS …", then `as R → infinity = …` with an e^ in it and "exact (CAS)". Write down exactly how the calculator prints it.
3. On the G1, time steps 1 and 2 (each Poisson k is now two CAS calls).
4. With the CAS answers showing, open the CAS view: no new variables (gbq has no value).
