# ErrorRate Lab beta 1a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 1 (16 Oct 2026, round 1, current); every beta 1 feature is kept. Not yet run on hardware or on the emulator. The beta 1 device checklist is in `ErrorRate_beta1_NOTES.md`.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 1's `erlCas` (`cR := STRING(CAS(ecQ));`) returned its own input. ErrorRate only shows its CAS answers, so beta 1 would have shown its own questions as the CAS's answers, under "exact (CAS)". The harness reproduces this (verify, part G).
  - "Where the 3 comes from" would have shown `50/1000` instead of `1/20`, and `limit(p×(1-(50/1000)^(1/p)),p,inf)` instead of `ln(20)`.
  - The Engines page's live check would have read "1/2+1/3 gave 1/2+1/3".
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime writes exp(u) as `e^(u)` (T17, T40). `inf` works in a limit (T16).

## What changed (line numbers: beta 1 → beta 1a)

1. **`erlCas`** (beta 1 453–486 → beta 1a 475–514): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + ecQ + ")" + CHAR(34) + ")"));` (1a line 499). The call counter `erlCasN` and the quote drop are kept. The reject test adds `INSTRING(cR, CHAR(8734)) > 0`. The comments say why.
2. **No answer reader changed.**
   - Every answer is only shown, through `erlShow`.
   - erlShow's `exp(` → `e^(` step finds nothing on the calculator, because the Prime already writes `e^(`. It is kept for desktop Giac; its **comment** says so (1a 432–436).
   - Its turn-round of a leading `(p-1)^m` is untouched.
   - No CAS text assigns a variable; `erlq` and `erll` stay symbols.
3. **The Engines page (`erlEngPage`)**: its last two grey CAS lines said "Run CASProbe beta 1 first. If it finds a / different CAS call form, only erlCas changes." They now read "The CAS call form is the one CASProbe / beta 1b found on the emulator (erlCas)." This is a stale reference swept (Lessons Learned rule 13). Both lines are under 46 characters.
4. **Header and comments**: version beta 1a, the firmware paragraph (harness v3b, verify_ErrorRate_beta1a.py), the companion-file list, a "beta 1a" note. The erlInf comments now say T16 passed with `inf`.

Nothing else changed. The verify script checks this: the routines that differ from beta 1 are exactly `erlCas` and `erlEngPage`, outside them only comments differ, and the #PYTHON block is unchanged.

**Not changed, out of date**: `errorrate-guide_beta1.md` still says "run CASProbe beta 1 first". The guide was not part of this task.

## Verification

`verify_ErrorRate_beta1a.py` (from verify_ErrorRate.py, harness **ppl_run_v3b**; its SymPy reader takes the Prime's printing), output in `verify_ErrorRate_beta1a_output.txt`: **ALL PASS, 170 checks** (beta 1's script: 161).

- A, B, D (unchanged): the statistics through the program's own routines against SciPy and statsmodels, every quoted number, and the #PYTHON block under CPython.
- C: every CAS template, as the program builds it, now read in the Prime's printing.
  - k = 0: 25 records give α as a fraction, `1-(α)^(1/n)`, and the limit `ln(1000/am)`.
  - k = 1…6: the exact polynomial and the Poisson limit, e.g. `(μ^2+2×μ+2)×e^(-μ)/2`.
  - Also the Bayes means and the trawl's three lines.
  - erlCas: the quoted answer is unwrapped once, undef → "", and (1a) `±∞` → "".
  - erlShow on the Prime's forms (1a) gives the same display as on desktop Giac's.
- E1, **cas='giac'**:
  - "Why 3" shows `p = 1-(1/20)^(1/30)` and `ln(20)` with "exact (CAS)".
  - Bayes shows 1/62 and 1/32. The trawl Exact page shows "exact (CAS)". The Engines page shows "1/2+1/3 = 5/6".
  - Every CAS text asks for `string(...)` and every answer is quoted. No CAS variable is assigned, and no CAS call takes a variable. No "exp(" or "sqrt" appears on any page.
- E2, **cas='fail'**: the decimal fallbacks, "decimal" badges, no runtime error.
- E3 and E4: Python stopping part-way is refused, and the k > 0 session works. No CAS call during drags.
- G (1a): beta 1 itself in v3b hands back `50/1000` and `limit(...)` with erlCasOK = 1, i.e. it would show them as exact answers.

**Gate**: `python3 ppl_gate_v1a.py ErrorRate_beta1a.txt ErrorRate_beta1.txt`: **RESULT: PASS**.
- ppl_check_v3 is clean.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too. (Among them: the "final depth −1" of the #PYTHON block.)
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 1 checklist)

1. The Eng soft key (page 2) opens the Engines page. It should say `1/2+1/3 = 5/6, as it should`. "1/2+1/3 gave 1/2+1/3" means the call form is not working (the old echo): note it and skip the CAS steps.
2. Why 3, with 0 of 30 at α = 0.05: `p = 1-(1/20)^(1/30)`, the limit `ln(20)` (or the calculator's form), and "exact (CAS)".
3. n, k = 2 of 30: the CAS's polynomial line and the Poisson limit with an `e^(`. Write down how the calculator prints it.
4. On the G1, time the first opening of Why 3 (three CAS calls) and of the trawl's Exact page (three).
5. Afterwards, in the CAS view, `erlq` and `erll` have no value.
