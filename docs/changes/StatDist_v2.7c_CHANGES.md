# StatDist v2.7c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v2.7b; every v2.7b feature is kept, and the CAS call line and quote strip in `st_Cas` are byte-identical. v2.7c itself has not run on hardware or on the emulator.*

## Why: what emulator round 2 showed

Round 2 ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' own firmware) on 17 October 2026 (`BRIEF_R2FIX_v1.md` §0 and §4).

- **StatDist v2.7b worked there.** F(2.5, 7.5) gave 0.800427 and χ²(2.5) gave 0.876911. The Formula page showed the CAS's exact answers, `15/11`, `405/77` and `2880/847`, with "exact (CAS)". The CAS never failed, so the fallback was never tested.
- **Two string rules the harness did not model, typed in Home:**
  - `INSTRING("", "a")` is **"Error: Invalid input"**, and `INSTRING("abc", "")` is 1;
  - `LEFT("abc", 0)` is `"abc"`, the whole string;
  - `MID("abc", 0, 1)` is **"Error: Bad argument type"**;
  - `STRING(0.096, 2, 1)` is `"9.6ᴇ-2"`: **scientific** whenever 0 < |x| < 10^-d.
- **What that means for v2.7b** (harness v3d, `audit_v3d/StatDist_v2.7b.txt`):
  - **The fallback.** `st_Cas` sets `cR := ""` when the CAS fails, then tests `INSTRING(cR, "undef")`, which is the error on the Prime. Every Formula page with `cas='fail'` stops.
  - **A second crash, with the CAS answering.** The old verify script stopped at Pareto(1, 1). Its CDF comes back as `(stqx-1)/stqx`, and `st_Repl`, which turns `stqx` into `x` for the page, loops `INSTRING` on what is left of the text. When the answer ends in the name being replaced, what is left is "", and the next INSTRING stops the program. This is the same fault as TrendTest's `trRepl` and ScatterLab's replace loop on the emulator. Part 1's 251 CAS answers include 5 such endings: `(stqx-1)/stqx`, `(stqx^stqb-1)/stqx^stqb`, `1/stqa` (an Exponential with a rate that is not a simple ratio), `2*stqb` and `5*stqb`.

## What changed (line numbers: v2.7b → v2.7c)

1. **`st_Cas`** (728–749 → 771–795). After the quote strip, the undef/error/infinity test runs only when `DIM(cR) > 0`, in the brief's shape and with its comment (747 → 789–793). The IFERR line and the quote strip are unchanged.
2. **`st_Repl`** (778–797 → 824–850), in the brief's replace-loop shape:
   - an empty pattern returns the text unchanged (`INSTRING(s, "")` is 1, so the old loop would never end);
   - the position is looked for only while text is left (784 and 793 → 837 and 846);
   - LEFT is still taken only past position 1 (`IF rpP > 1`).

   The comment now says what `LEFT(s, 0)` does: it returns the whole string, as the emulator showed.
3. **`st_fmtx`** (415–428 → 451–471). It shows a value with the fewest decimals, 0 to 3, that show it exactly. A value within 1E-10 of a whole number was printed with 0 decimals as it was, so a mean of 1E-17 left by rounding error would read `1ᴇ-17`. It now prints the rounded value: `0`, and never `-0`, since a rounded −1E-17 is set to 0. One new LOCAL, `fxR`.
4. **The other INSTRING, LEFT and MID calls need nothing.** The 12 INSTRING lines are:
   - `st_Cas` (fixed above) and `st_Repl` (2 lines, fixed above);
   - `st_IVal` (761), `st_Digits` (882) and `st_FmRes` (3512), which search the fixed text "0123456789" (or with "/-");
   - `st_FmGood` (3395–3403), whose first line returns at `DIM(fgT) == 0`;
   - `st_FmSub` (3416), whose text has already passed `st_FmGood`.

   Every LEFT counts 1, 2, `rpP - 1` under `IF rpP > 1`, or `wrB` ≥ 1. Every MID starts at 1 or more: `st_Wrap` is only called with a width of 46, so `wrI` ≥ 31. There is no RIGHT.
5. **The other 15 `STRING(x, 2, d)` calls cannot reach 0 < |x| < 10^-d:**
   - `st_fmtp` shows a value below 10^-d as "< 0.000001", and its `thr` is 10^-d itself;
   - the axis labels are multiples of a 1-2-5 step with d = −FLOOR(LOG(step)), and a −0 is set to 0;
   - the "% beyond" notes are drawn only from 0.15 % up;
   - `st_Int` prints IP(x);
   - k, a and b of a discrete family are whole;
   - the "not a simple ratio" line (3706) prints 12 decimals, so only a parameter below 1E-12 would turn scientific, and that is the one form that can show it.
6. **Header and version.**
   - A "WHAT CHANGED in v2.7c" paragraph (line numbers v2.7b's).
   - A firmware paragraph that records rounds 1 and 2.
   - The banner and the help page title (2299 → 2352) read v2.7c.

Nothing else changed. The routines that differ from v2.7b are exactly `st_Cas`, `st_Repl`, `st_fmtx` and `st_show_help`; outside them only comments differ.

## Verification

`verify_StatDist_v2.7c.py`, built from the v2.7b script, runs every check on **ppl_run_v3d**. Output in `verify_StatDist_v2.7c_output.txt`: **RESULT: ALL PASS, 100 checks.**

- **Parts 1–5, kept:**
  - Part 1, the Formula page with `cas='giac'` over 77 parameter sets: 197 answers shown and correct, 16 rejected, 0 wrong, and 98 of 98 exact comparisons. Every page line is the same as v2.7b's run. On v3d, v2.7b's own script stopped at Pareto(1, 1).
  - Part 2, `cas='fail'` for all 27 families: "decimal", no error.
  - Part 3, touch and keys (the help title now says v2.7c); Part 4, the infinity probe.
  - Part 5, fractional df: 5e still compares v2.7b with v2.7a, its own change set.
- **6a, `st_Cas` directly:** `5/6` for `1/2+1/3`. The infinity, undef and a syntax error give "". With the CAS failing it returns "" and no error; v2.7b stops.
- **6b, the Formula page through the soft keys with the CAS failing** (Pareto(1, 1), Exponential(0.5), Binomial(20, 0.5)): v2.7c shows "decimal" and "no closed form shown"; v2.7b stops in `st_Cas`.
- **6c, the replace loop with the CAS answering:**
  - Pareto(1, 1) now shows `F(x) = (x-1)/x` with "exact (CAS)"; v2.7b stops in `st_FmShow > st_Repl`;
  - all 251 of Part 1's answers go through `st_FmShow` in both versions: the 5 ending in a replaced name stopped v2.7b, and the rest read exactly as before.
- **6d, `st_Repl` on:**
  - a pattern at the end, `(x-1)/x`;
  - at the start;
  - the whole text (`stqa` → `a`);
  - an empty pattern (the text unchanged; v2.7b would loop for ever);
  - an empty text ("");
  - no match;
  - `**` → `××`;
  - a pattern inside its own replacement.

  v2.7b stops on four of them.
- **6e, `st_fmtx`:** `1E-17`, `-1E-17` and `1E-11` print `0` (v2.7b: `1ᴇ-17`, `-1ᴇ-17`, `1ᴇ-11`). 2, 1.96, 1/3, 0.0004, −2.5, 123 and 0.3 print as before.
- **6f, the static sweep:** all 16 `STRING(x, 2, d)` calls with a reason each; every INSTRING's first argument; every LEFT and MID.
- **6g:** the routine diff is as listed. `st_Cas` keeps its IFERR line and quote strip, and no code line says v2.7b.
- **6h, `h.sci_strings`:**
  - v2.7c: no scientific result in any of the 30 harness runs;
  - v2.7b, in Part 6 for comparison: `st_fmtx`'s `1ᴇ-17`, `-1ᴇ-17` and `1ᴇ-11`.

## Gate

`python3 ppl_gate_v1b.py StatDist_v2.7c.txt StatDist_v2.7b.txt` (in `gate_r2`) gives **RESULT: PASS**.
- ppl_check_v4: clean, as v2.7b. No hard error, E12 included.
- lint_ppl: 26 problems, as v2.7b. All are noise: the lint reads each `INSTRING(` as a `STRING(` call, and two lines with `MID(...)` inside give "4 args".
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged.
- `check.sh` runs the parts the gate skips without the kit zip:
  - the hp-prime-kit lint: **0 errors**;
  - the full parse fails at line 305, "expected a name after EXPORT". v2.7b fails the same way at its line 269. That is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Paste, then Program Catalog → StatDist → Edit → Check: no error. Help's title reads "Statistical Distributions v2.7c".
2. **The replace-loop crash.** Advanced Continuous → Pareto with x_m = 1 and α = 1 (Lower tail, x = 2). Open the Formula page (More, More, Formula). It should show the CDF line `F(x) = (x-1)/x` (or the calculator's equivalent) with "exact (CAS)", and **no error**. v2.7b would stop here if the Prime's answer ends in `stqx`. Note what the CAS wrote.
3. **The same for a symbolic mean.** An Exponential with rate 0.3333333333 (not a simple ratio) → Formula page. The mean line reads `1/λ`-style (`1/a`), with no error.
4. Round 2's own checks, again: F(2.5, 7.5), x = 2 → 0.800427; χ²(2.5), x = 5 → 0.876911; the Formula page answers as before.
5. **The fallback** cannot be forced on the Prime. If a Formula page ever says "decimal" and "no closed form shown", it must not stop.

## Unresolved

- None in the code. **A value of 10^12 or more** also prints scientific with fixed decimals (`STRING(1E15, 2, 0)` = `1ᴇ15`). `st_fmtp` can be handed one: a LogNormal moment with σ = 5 is about 5E21. There, scientific is the only form that can show the number, so it is left as it is.
