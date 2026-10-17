# StatDist v2.7a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v2.7 (16 Oct 2026); every v2.7 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). v2.7's `st_Cas` (`cR := STRING(CAS(stS));`) returned its own input. Every Formula-page answer still said `int(` or `sum(`, so `st_FmGood` refused it, and the page showed "no closed form shown" and "decimal" throughout. The harness reproduces this (verify, part 4).
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime prints infinity as `∞`, CHAR(8734) (T41), and 1/0 as `±∞` (T27). The new kit (BRIEF_CAS_v2) refuses any answer holding ∞. That broke v2.7's one infinity reader: "no mean" and "no variance" were shown only when the CAS answered the divergent integral with an infinity.

## What changed (line numbers: v2.7 → v2.7a)

1. **`st_Cas`** (v2.7 652–672 → v2.7a 682–709): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + stS + ")" + CHAR(34) + ")"));` (v2.7a line 694). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0`. The comments say why.
2. **"No mean" / "no variance" asked as a finite question.**
   - `st_FmCont` (v2.7 3447 and 3468 → v2.7a 3490 and 3512) now asks `exp(-(<the same integral>))` instead of the integral. That is `0` exactly when the integral is +∞.
   - A finite integral v gives e^(−v), never 0. −∞ gives an infinity, which st_Cas refuses. An integral the CAS cannot do stays unevaluated.
   - `st_FmInf` (v2.7 3332–3340 → v2.7a 3372–3383) now reads that `0`. v2.7 read `"infinity"` (desktop) or the ∞ sign, which can no longer reach it.
   - The assumption suffix (`| stqb>0`) stays inside the brackets.
3. **`st_FmGood`** (v2.7 3290–3301 → v2.7a 3326–3341) also refuses the integral and summation signs (CHAR(8747) ∫, CHAR(8721) ∑, CHAR(931) Σ). **Not measured**: CASProbe saw no undone integral. This guards against the Prime writing an integral it cannot do as `∫(…)` rather than `integrate(…)`. The value check would not catch such an answer, because an undone integral still evaluates to the right number.
4. **No other reader changed.**
   - Shown answers are checked by value (`st_FmAsk` → `st_CasNum`, a whole number read by `st_IVal`).
   - `st_FmShow` only swaps names.
   - The fraction test reads digits, `/` and `-`.
   - On the Prime the formulas carry `e^(` and the root sign; they are shown as they are.
5. **Version strings**: the banner, the help page's title (`st_show_help`: "Statistical Distributions v2.7a", 2235), and a "WHAT CHANGED in v2.7a" note.

Nothing else changed. The verify script checks this: the routines that differ from v2.7 are exactly `st_Cas`, `st_FmCont`, `st_FmGood`, `st_FmInf` and `st_show_help`, and outside them only comments differ.

## Verification

`verify_StatDist_v2.7a.py` (from the v2.7 script, harness **ppl_run_v3b**; its SymPy reader now takes the Prime's printing: √, e^, ∞), output in `verify_StatDist_v2.7a_output.txt`: **RESULT: ALL PASS, 36 checks** (v2.7's script: 15; the new ones are marked 2.7a).

- Part 1: 77 parameter sets over the 27 families. **197 answers shown and correct, 16 rejected, 0 wrong; 98 of 98 exact comparisons agree.** This is the same tally v2.7 gave in harness v3a, where the CAS was answered from variables. Every "infinite" moment is now found by the probe: Cauchy, t with 1 df (mean and variance), t with 2 df (variance), F, Burr XII, and Pareto with α 1 and 1.5.
- Part 2, **cas='fail'**: all 27 families show "decimal", the program's decimals and no error.
- Part 3: the touch and key paths, the page kept, no CAS call in a frame or a drag, and the plot frames identical to v2.6's. The kit drops the quotes and refuses undef, `±∞` and `∞`.
- Part 4 (2.7a):
  - v2.7 itself in v3b shows no closed form.
  - The probe answers `0` on every divergent integral and asks nothing where the moment exists.
  - In desktop Giac, Prime printing: exp(−(+∞)) = 0 → infinite; e^(−1) → not; exp(−(−∞)) → ∞ → refused; a finite Cauchy piece → not.
  - st_FmGood refuses the three glyph forms and still takes `1/2*e^(-1)`.

**Gate**: `python3 ppl_gate_v1a.py StatDist_v2.7a.txt StatDist_v2.7.txt`: **RESULT: PASS**.
- ppl_check_v3 is clean.
- lint_ppl has no new problems. The extra INSTRING on the reject line, which the lint reads as a 2-argument STRING(), is offset by the old st_FmInf tests that were removed.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the v2.7 checklist)

1. Exponential, λ = 0.5, the Formula page. You should see `E[X] = 2` and `E[X^2] = 8` (or the CAS's form), each with `the program's value: agree` and "exact (CAS)". "no closed form shown" with "decimal" on every line means the call form is not working: note it and skip the CAS steps.
2. Cauchy, defaults, the Formula page: `from the centre up alone: infinity (CAS).` and `So there is NO mean`, then `= infinity (CAS): there is NO variance`. These come from the new exp(−(…)) question.
3. Student t, df = 2: E[X] shown, then `= infinity (CAS): there is NO variance`.
4. Any family whose page shows an answer with `∫` or `Σ` in it means the glyph refusal did not catch something: photograph it.
5. On the G1, time the Formula page for the Normal and for the Chi-square (the slowest in desktop Giac).
