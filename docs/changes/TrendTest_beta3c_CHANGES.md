# TrendTest beta 3c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3b; every beta 3b feature is kept. trCompute, the CAS call form (trCas's IFERR line and quote strip) and the 35 routines listed under "Nothing else" are byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

TrendTest beta 3b ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) in round 2, 17 October 2026 (`BRIEF_R2FIX_v1.md` §0 and §4):

- **Results page 4, least squares as calculus: "Error: Invalid input", and the program stopped.** Typed in Home: `INSTRING("", "a")` is "Error: Invalid input"; `INSTRING("abc", "")` is 1. `trRepl` looked for its pattern again in what was left of the text. solve's answer, `{[80277/4757909,95339/4757909]}`, ends in the `}` that trRepl removes, so what was left was `""`. The CAS had answered all four calls.
- **The proportions plot printed `line 0.017 (+9.6ᴇ-2 SE)`.** Typed in Home: `STRING(0.096, 2, 1)` is `"9.6ᴇ-2"` (U+1D07 for the E). Fixed decimals turn scientific whenever 0 < |x| < 10^-d.
- **Help: Esc moved to the next help page** instead of leaving help. The footers said "Any key = page 2" and "Any key = menu".
- Not seen on the emulator, because its CAS never failed, but shown by harness v3d: when the CAS fails, `trCas` sets its answer to `""` and then tests `INSTRING(cR, "undef")`. That is the same error, so the decimal fallback page could never be reached.

## What changed (line numbers: beta 3b → beta 3c)

1. **trRepl** (3b 571–584 → 3c 645–665) is now the brief's replace loop, line for line. It looks for the pattern only while text is left (`rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;`, before the loop and at its end). An empty pattern hands the text back unchanged; `INSTRING(s, "")` = 1 would otherwise loop for ever.
2. **trCas** (3b 533 → 3c 603–607) has the kit's guard: the undef / rror / ∞ tests run only when `DIM(cR) > 0`. The IFERR line and the quote strip are byte-identical.
3. **trCxClean** (3b 1090–1094 → 3c 1172–1179) hands `""` back without calling INSTRING.
4. **trCxSol** (3b 1101–1123 → 3c 1186–1213) gets two guards:
   - it returns when nothing is left once the brackets are gone (3c 1197; solve's `{}` or `[]`);
   - after the `a=` cut, an empty half (`tra=` with nothing after it) means no answer (3c 1210).
5. **A new helper, trFx(x, d)** (3c 402–414): `STRING(ROUND(x, d), 2, d)`. Rounding first makes the value either 0 or at least 10^-d, so the fixed form always holds. A value that rounds to 0 prints `0.000`, never `-0.000`.
6. **The sweep: 26 of beta 3b's 39 fixed-decimal displays with d > 0 now go through trFx:**
   - **the plot readout**, 1453 → 1560: p, the line's value and the residual. Snoring level 1 now reads `(+0.1 SE)`;
   - **the plot's footer statistics**: trend, the animated trend, Pearson and departure (1458–1464 → 1565–1571);
   - **page 1** (915–930 → 997–1012): fit, p, both CI ends, the three χ² statistics and the WLS line;
   - **page 2**: the panel statistic (1008 → 1090) and the Pearson lines (1027, 1031 → 1109, 1113);
   - **trDec** (1224–1228 → 1314–1323): a value that rounds to 0 at its decimals prints `0`, as an exact 0 already did;
   - **trNum** (1233–1242 → 1325–1347): a sum below 1E-6 prints `0`. Beta 3b printed it in scientific form, and its trailing-zero strip could then cut an exponent's last 0 (`1.0ᴇ-10` → `1.0ᴇ-1`). From 1E12 up, the Prime is scientific whatever the decimals: trNum now keeps six significant digits there (`7.00018ᴇ13`, not `7.0ᴇ13`) and skips the strip;
   - **the summary returned to Home** (1928 → 2036).
7. **Two displays where rounding would hide the value:**
   - **trXStr** (381–388 → 444–454): a score below 0.01 (a dose of 0.005) gets three decimals, rounded first; two decimals printed `5.00ᴇ-3`.
   - **trOrStr** (373–379 → 433–442): an odds ratio below 0.001 reads `< 0.001`, as trPStr does for p. A level with no cases against a level 1 with all cases (50/50 against 0/50, typed or dragged) gives OR 0.0001, which beta 3b printed as `9.803ᴇ-5`. `0.000` would read as "no odds at all", which is wrong here.
8. **Help: Esc leaves from any page.**
   - **trWaitAny** (430–444 → 496–514) returns the key code (−1 for a tap).
   - **trHelp** returns to the menu when that key is Esc (4): 3c 1929 and 1950.
   - **The footers** (1819, 1840, 1861 → 1926, 1948, 1969) now read `any key = page 2, Esc = menu`, `any key = page 3, Esc = menu` and `any key = menu`, in the canonical form (LL §13).
9. **Header**: banner beta 3c, the round-2 status lines, a "beta 3c" paragraph. No other version string appears in the program's displays.

**Nothing else.** The routines that differ from beta 3b are exactly:
- the changed ones: TrendTest (the summary), trCas, trChiPanel, trCxClean, trCxSol, trDec, trDrawProp, trHelp, trNum, trOrStr, trPage1, trPageChi, trRepl, trWaitAny, trXStr;
- the new trFx.

The other 35 routines are byte-identical, comments included (verify, part G).

### The INSTRING, LEFT and MID review (2a)

- **INSTRING, 13 lines in beta 3b:**
  - **Guarded:**
    - trCas 533;
    - trRepl 576, 581;
    - trCxClean 1092;
    - trCxSol 1110–1111 (soS);
    - trCxSol 1122 (the halves after the `=` cut).
  - **Safe as they are:**
    - trRatNote 566: trCxMake calls it only when trRat's text holds a `/`;
    - trCxSol 1115, 1119, 1120: `soK < DIM(soS)` and `soK ≥ 2` leave both halves at least one character long before the `=` cut;
    - trCxMake 1148: it has already returned if `DIM(cxX) == 0`;
    - trCxFrac 1214: the literal `"0123456789"`.
- **LEFT and MID, 6 and 15 calls; none needed a change:**
  - **counts:**
    - every computed LEFT count is at least 1 (`rpI > 1`, `soK ≥ 2`, trWrap's break ≥ 24 at width 49);
    - trNum's `DIM - 1` runs only while `DIM > 1`, or on text that ends in "." and so is at least 2 long.
  - **MID starts:**
    - every computed start is at least 1: `rpI + rpK`, `soK + 1`, `INSTRING(..) + 1`, `wpI ± 1` (only when `wpI > 1`), `rnP + 1`, `DIM(cR)` (`DIM ≥ 2`);
    - a count of 0 or a start past the end gives `""`, which is what each call wants.
- **RIGHT:** none.

### The fixed-decimal review (2b)

Beta 3b has 61 `STRING(x, 2, d)` calls:
- 22 have d = 0, and all of them print whole numbers: counts, levels, df, lengths, and xsV and nmV inside their `FP = 0` branches.
- 26 of the 39 with d > 0 now use trFx (item 6).
- 13 stay as they are, because they cannot reach 0 < |x| < 10^-d:
  - trPStr: p ≥ 0.0001; below that it says "< 0.0001";
  - trOrStr: three sites, OR ≥ 100, ≥ 10 and ≥ 0.001;
  - trXStr: two sites, a half (|x| ≥ 0.5) and |x| ≥ 0.01;
  - trRatNote: trRat chose the fewest decimals d for which x·10^d is whole, so |x| ≥ 10^-d;
  - the chi-square, proportion and OR tick labels: 0, a whole number of steps, or 1, 2 or 5 × 10^doD;
  - the two 5% cut-offs, ≥ 3.84;
  - the animation fraction k/15: 0 or ≥ 0.067.

## Verification

`verify_TrendTest_beta3c.py` (built from the 3b script, harness **ppl_run_v3d**). Output in `verify_TrendTest_beta3c_output.txt`: **98 PASS, 0 failures** (3b: 44).

- **Kept:** every 3b check, now in v3d. That covers part A (every CAS template in desktop Giac against fractions, SymPy and statsmodels), part B (page 4 with `cas='giac'` and `cas='fail'`, the cache, the drag, a 1/3 score, the stale-key run), part W (CHOOSE widths, solid dots) and part G (3b against 3a, beta 3 in v3d).
- **R1, trRepl directly:** 9 cases, all right. They include a pattern at the end, at the start, the whole text, an empty pattern, an empty text and only the pattern. Beta 3b in v3d stops with the INSTRING error whenever the text runs out.
- **R2:** `trCas` with the CAS failing returns `""` with no error (3b stops). trCxClean("") is `""`. trCxSol reads 10 answers right, empty ones included.
- **R3, the emulator's crash:** Examples → Snoring → Right ×3 opens page 4 with "exact (CAS)", `b = 95339/4757909` and `a = 80277/4757909`, and Quit returns the summary. **Beta 3b, the same run:** the CAS answers all 4 calls, then the INSTRING error.
- **R4:** `cas='fail'` gives the decimal page with no error; beta 3b stops.
- **R5:** canned answers (solve `{}`, `{[tra=,trb=1/2]}`, every answer `""`) give the decimal page with no error.
- **R6:** the plot readout for snoring level 1 is `L1: x = 0, 24/1379 = 0.017, line 0.017 (+0.1 SE)`. Beta 3b gives `(+9.6ᴇ-2 SE)`, the emulator's line character for character.
- **R7, Help:** Esc on page 1 → menu; a key then Esc → menu; three keys → pages 1, 2, 3 → menu. The footers are as above. Beta 3b turned the page on Esc.
- **R8, seven tables:** snoring, small doses, a dragged extreme, a rare outcome (1 to 3 of 20,000), an almost flat table, midranks on a million people, and scores −2/3, 1/3, 4/3. Each is run through pages 1–4 (CAS and `cas='fail'`), both plots at every level, Scores ×2 and Quit (94–98 frames per table, both runs together): no error and no small number in scientific form. On pages 1–3 and the plots, beta 3b printed 51 different scientific forms across them, e.g. `1.00ᴇ-3` (a score), `9.803ᴇ-5` (an OR), `5.0000ᴇ-5` (a p), `7.39ᴇ-3` (Pearson), `4.285714ᴇ-9` (the slope).
- **R9, static:** the 14 remaining `STRING(x, 2, d > 0)` are exactly the justified sites above (13, plus trFx's own). Every d = 0 site prints a whole number. The INSTRING first arguments and their guards are as listed above.
- **G:** the routine diff is as listed. trCas equals 3b's apart from the guard, and trRepl is the brief's loop.
- **R10, h.sci_strings over all 55 beta 3c runs:**
  - small numbers: none;
  - from 1E12 up: two, `7.00018ᴇ13` and `3.20000ᴇ17`, both trNum's sums of n x² on the decimal page (midranks, `cas='fail'`). The Prime holds 12 digits, so scientific is its only form for them. Six significant digits are kept.

## Gate

- `python3 ppl_gate_v1b.py TrendTest_beta3c.txt TrendTest_beta3b.txt` (in `gate_r2`): **RESULT: PASS**.
  - ppl_check_v4: clean, no hard errors (E12 included).
  - lint_ppl: 1450 checks, 34 problems, the same 34 as beta 3b's (the INSTRING-read-as-STRING, bare-concatenation and grob-parameter noise).
  - fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 built-in matches.
- `check.sh`:
  - kit lint: **0 errors**;
  - full parse: stops at 3c line 307, the file-level `LOCAL` after the EXPORT list. That is the same line as beta 3b's 262 and the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Replace TrendTest in the Connectivity Kit (open it, paste over it; never a second copy). Program Catalog → Edit → Check: no errors.
2. **Page 4:** Examples → Snoring and heart disease → Right three times. Results page 4 shows "exact (CAS)", the SSE, `dSSE/da = 4968×a+6796×b-220 = 0`, `b = 95339/4757909   (program 0.02003800)` and `a = 80277/4757909   (program 0.01687233)`. No "Invalid input".
3. **Plot readout:** tap Prop. When the animation ends, the footer reads `L1: x = 0, 24/1379 = 0.017, line 0.017 (+0.1 SE)`. Step through the levels with ⇆: no ᴇ anywhere. Do the same on pages 1–3 and the OR plot.
4. **Help:** Menu → Help, then Esc: back to the menu. Help, any key (page 2), then Esc: back to the menu. The footers read "any key = page 2, Esc = menu".
5. **Small numbers** (optional): Enter data, 3 levels, scores 1 2 3, cases 50 0 0, totals 50 50 50. Page 3 shows `< 0.001` and `(< 0.001 - 0.005)` for levels 2 and 3. Page 1 shows `0/50` with `0.0000` and `(0.000-0.071)`.
6. Quit: `TrendTest: X2 trend = … (1 df), p …` returns to Home.
7. **G1:** time "asking the CAS ..." on page 4 (four calls).

## Unresolved

- Whether the Prime's ROUND keeps a sign on a value that rounds to 0 (`ROUND(-0.00001, 3)`) is not known. trFx prints such a value as `0.000` either way. A display that strips zeros by hand (trNum) returns "0" first.
- `trRatNote` and its trRat tolerance were left alone. A score typed with 8 or more decimals, within 1E-6 of a shorter one (0.09999999), would be written as 1/10 and shown as such. That has been so since beta 3; it is not a display-format issue.
