# ScatterLab beta 2b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 2a; every beta 2a feature is kept, and the user's guide (`scatterlab-guide_beta2.md`) still applies. slFit, every drag, the CAS call form (slCas's IFERR line and quote strip) and the 54 routines listed under "Nothing else" are byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

ScatterLab beta 2a ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) in round 2, 17 October 2026 (`BRIEF_R2FIX_v1.md` §0 and §4):

- **Tapping the equation (the "Least squares as calculus" page) with the Poverty-vs-crime example: the program stopped with "Error: Invalid input".** This is the same crash as TrendTest's page 4, in the same kind of replace loop. Typed in Home: `INSTRING("", "a")` is "Error: Invalid input"; `INSTRING("abc", "")` is 1. `slRepl` looked for its pattern again in what was left of the text. solve's answer, `{[3186173/191520,2441/2394]}`, ends in the `}` that slRepl removes, so what was left was `""`.
- **Fixed decimals turn scientific whenever 0 < |x| < 10^-d** (Home: `STRING(0.096, 2, 1)` is `"9.6ᴇ-2"`, U+1D07 for the E). The emulator run did not reach a small value in ScatterLab. Harness v3d shows r, r² and a loaded point's coordinates doing it (part R6).
- Not seen on the emulator, because its CAS never failed, but shown by harness v3d: when the CAS fails, `slCas` sets its answer to `""` and then tests `INSTRING(cR, "undef")`. That is the same error, so the decimal fallback page could never be reached.

## What changed (line numbers: beta 2a → beta 2b)

1. **slRepl** (2a 385–398 → 2b 446–466) is now the brief's replace loop, line for line. It looks for the pattern only while text is left; an empty pattern hands the text back unchanged.
2. **slCas** (2a 347 → 2b 404–408) has the kit's guard: the undef / rror / ∞ tests run only when `DIM(cR) > 0`. The IFERR line and the quote strip are byte-identical.
3. **slCxClean** (2a 1375–1379 → 2b 1448–1455) hands `""` back without calling INSTRING.
4. **slCxSol** (2a 1386–1408 → 2b 1462–1489) gets two guards:
   - it returns when nothing is left once the brackets are gone (solve's `{}` or `[]`);
   - after the `a=` cut, an empty half (`sla=` with nothing after it) means no answer.
5. **A new helper, slFx(x, d)** (2b 310–323): `STRING(ROUND(x, d), 2, d)`. Rounding first makes the value either 0 or at least 10^-d, so the fixed form always holds. A value that rounds to 0 prints `0.000`, never `-0.000`.
6. **The sweep: 11 of beta 2a's 17 fixed-decimal displays with d > 0 now go through slFx:**
   - **r and r² on the panel**, in both the plain and the Guess / Reveal panels (762, 763, 782, 783 → 833, 834, 853, 854). r = 0.0003 printed `2.987ᴇ-4`, and r² `8.924ᴇ-8`; both now print `0.000`;
   - **the selected point's x and y** in the note line (845 → 918). The decimals follow the snap grid, so a loaded value finer than the grid (0.004 on a step of 10) printed `4ᴇ-3`; it now prints `0`. By the same rule, `STRING(x, 2, 0)` is scientific for any 0 < |x| < 1;
   - **the axis labels** (707, 722 → 777, 792). Labels are whole multiples of the step, so on the Prime a tick at 0 should be exactly 0. Rounding to the label's own decimals makes that certain whatever the arithmetic leaves in the last digit (insurance; not seen in the harness either);
   - **slDec** (1488–1492 → 1569–1578): a value that rounds to 0 at its decimals prints `0`, as an exact 0 already did;
   - **slNum** (1516–1525 → 1602–1620): a sum below 1E-6 prints `0`. Points at x = −2/3, 1/3, 1/3 leave −1E-12 on the Prime, and beta 2a printed it in scientific form, after which the trailing-zero strip could cut an exponent's last 0. From 1E12 up, the Prime is scientific whatever the decimals: slNum now keeps six significant digits there (`8.69000ᴇ12` for Σx² of populations of a million) and skips the strip;
   - **r in the summary returned to Home** (1992 → 2087).
7. **Header**: banner beta 2b, the round-2 status lines (beta 1 passed round 1; beta 2a stopped in round 2), a "beta 2b" paragraph. No other version string appears in the program's displays.

**Nothing else.** The routines that differ from beta 2a are exactly:
- the changed ones: ScatterLab (the summary), slAxes, slCas, slCxClean, slCxSol, slDec, slNotes, slNum, slPanel, slRepl;
- the new slFx.

The other 54 routines are byte-identical, comments included (verify, part G). The file is still pure ASCII.

### The INSTRING, LEFT and MID review (2a)

- **INSTRING, 14 lines in beta 2a:**
  - **Guarded:**
    - slCas 347;
    - slRepl 390, 395;
    - slCxClean 1377;
    - slCxSol 1395–1396 (soS);
    - slCxSol 1407 (the halves after the `=` cut).
  - **Safe as they are:**
    - slRatNote 380: slCxMake calls it only when slRat's text holds a `/`;
    - slCxSol 1400, 1404, 1405: `2 ≤ soK < DIM(soS)` leaves both halves at least one character long before the `=` cut;
    - slCxMake 1432, 1433: it has already returned if cxX or cxY is empty;
    - slCxFrac 1505: the literal `"0123456789"`.
- **LEFT and MID, 6 and 15 calls; none needed a change.** They are the same shapes as TrendTest's:
  - every computed LEFT count is at least 1 (`rpI > 1`, `soK ≥ 2`, slWrap's break ≥ 24 at width 49, slNum's strip only while `DIM > 1`);
  - every computed MID start is at least 1.
- **RIGHT:** none.

### The fixed-decimal review (2b)

Beta 2a has 31 `STRING(x, 2, d)` calls:
- 14 have d = 0, and all of them print whole numbers: n, counts, page numbers, and nmV inside its `FP = 0` branch.
- 11 of the 17 with d > 0 now use slFx (item 6).
- 6 stay as they are, because they cannot reach 0 < |x| < 10^-d:
  - **slSig**, two sites: it prints `0.00` below 0.00001 and at most 5 decimals above, so |x| ≥ 10^-5 whenever it uses d = 5. It covers the coefficients, SSE, the means, the residual, the Guess line and the summary's line and SSE;
  - **slRatNote**: trRat's rule, |x| ≥ 10^-d;
  - **slAxes's width estimate** (two calls): slXlo and slXhi are 0 or whole multiples of the step;
  - **the leverage h**: at least 1/n ≥ 0.025.

## Verification

`verify_ScatterLab_beta2b.py` (built from the 2a script, harness **ppl_run_v3d**). Output in `verify_ScatterLab_beta2b_output.txt`: **80 PASS, 0 failures** (2a: 33).

- **Kept:** every 2a check, now in v3d: part A (every CAS template in desktop Giac against fractions, SymPy, statsmodels and polyfit), part B (the panel tap and the menu path with `cas='giac'` and `cas='fail'`, the cache, the drag, canned answers, two points, a 1/3 point, the stale-key run) and part G (2a against 2, beta 2 in v3d).
- **R1, slRepl directly:** 9 cases, all right. They include a pattern at the end, at the start, the whole text, an empty pattern, an empty text and only the pattern. Beta 2a in v3d stops with the INSTRING error whenever the text runs out.
- **R2:** slCas with the CAS failing returns `""` with no error (2a stops). slCxClean("") is `""`. slCxSol reads 10 answers right, empty ones included.
- **R3, the emulator's crash:** Data → Poverty vs crime → tap the equation opens the page with "exact (CAS)", `b = 2441/2394   (program 1.019632)` and `a = 3186173/191520   (program 16.63624)`. The same holds through Menu → Least squares as calculus, and Quit returns the summary. **Beta 2a, the same two runs:** the CAS answers all 4 calls, then the INSTRING error.
- **R4:** `cas='fail'`, both paths, gives the decimal page with no error; beta 2a stops.
- **R5:** canned answers (solve `{}`, `{[sla=,slb=1/2]}`, every answer `""`) give the decimal page with no error.
- **R6, seven data sets loaded from C1/C2:**
  - the sets: the example, r near 0, a value finer than the grid, x = −2/3, 1/3, 1/3, x = −2/3, −1/3, 1/3, 2/3, an axis crossing 0 in steps of 0.1, and populations of a million;
  - each run: every point's note, Resid, the page (CAS and `cas='fail'`), Guess and Reveal, Fit, a far-out point and Quit;
  - beta 2b: no error and no small number in scientific form;
  - beta 2a printed `2.987ᴇ-4` and `1.276ᴇ-4` (r), `8.924ᴇ-8` and `1.627ᴇ-8` (r²), `4ᴇ-3` and `3.0ᴇ-3` (a point's x and y), and `-1.110223ᴇ-16` (Σx on the decimal page);
  - the loaded point (0.004, 0.003) now reads `Pt 1 (0, 0.0): resid +0.08828, h = 0.42`.
- **R7, static:** the 7 remaining `STRING(x, 2, d > 0)` are exactly the justified sites above (6, plus slFx's own). Every d = 0 site prints a whole number. The INSTRING first arguments and their guards are as listed above.
- **G:** the routine diff is as listed. slCas equals 2a's apart from the guard, and slRepl is the brief's loop.
- **R10, h.sci_strings over all 42 beta 2b runs:**
  - small numbers: none;
  - from 1E12 up: one, `8.69000ᴇ12` (slNum, Σx² of the populations on the decimal page, `cas='fail'`). The Prime holds 12 digits, so scientific is its only form for it. Six significant digits are kept.

## Gate

- `python3 ppl_gate_v1b.py ScatterLab_beta2b.txt ScatterLab_beta2a.txt` (in `gate_r2`): **RESULT: PASS**.
  - ppl_check_v4: clean, no hard errors (E12 included).
  - lint_ppl: 1283 checks, 29 problems, the same 29 as beta 2a's.
  - fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 built-in matches.
- `check.sh`:
  - kit lint: **0 errors**;
  - full parse: stops at 2b line 213, the file-level `LOCAL` after the EXPORT lines. That is the same line as beta 2a's 171 and the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Replace ScatterLab in the Connectivity Kit (open it, paste over it; never a second copy). Program Catalog → Edit → Check: no errors.
2. **The emulator's crash:** Data → Poverty vs crime (SYNTHETIC), then tap the equation in the panel. The page shows `b = 2441/2394   (program 1.019632)`, `a = 3186173/191520   (program 16.63624)` and "exact (CAS)", with the SSE and both derivatives above. No "Invalid input". Any key goes back to the plot.
3. Menu → Least squares as calculus: the same page, without "asking the CAS ..." (the answers are kept).
4. **r near 0** (optional): Data → Clear all points, then Menu → Type a point six times: (1, 5), (2, 1), (3, 3), (4, 3), (5, 1), (6, 5.002). The panel reads `r = 0.000` and `r² = 0.000`, not ᴇ. Quit returns `… r = 0.0003, SSE = 16.01`.
5. After the run, in the CAS view, `sla` and `slb` have no value.
6. **G1:** time "asking the CAS ..." (four calls).

## Unresolved

- Whether the Prime's ROUND keeps a sign on a value that rounds to 0 is not known. slFx prints such a value as `0.000` either way.
- The axis-label change is insurance. On the Prime, `lo + n × step` should be exact, and the harness did not show a remainder either. It costs one ROUND per label.
