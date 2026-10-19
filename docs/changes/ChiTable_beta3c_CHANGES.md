# ChiTable beta 3c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3b; every beta 3b feature is kept, and csCompute, csFisher and the CAS call line are untouched. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed (round 2)

Beta 3b ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) on 17 October 2026, round 2:

> **ChiTable beta 3b did not compile**: "Syntax Error" in `csResMenu`, where beta 3b put two `//` comment lines INSIDE the `CHOOSE(rmI, "Results menu", { ... })` list. With those two lines removed, it compiled and every CAS page was right. **A comment inside an open bracket is a syntax error on the Prime.**

The same round found two string behaviours, typed in Home, that the PC harness had not modelled:

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: fixed decimals turn **scientific** whenever 0 < \|x\| < 10^-d |

ChiTable's CAS never failed on the emulator, so its fallback was not reached there. Harness v3d shows it: `csCas` sets `cR := ""` when the CAS fails, then tests `INSTRING(cR, "undef")`, and the program stops (`audit_v3d/ChiTable_beta3b.txt`, the `cas='fail'` tea run).

## What changed (line numbers: beta 3b → beta 3c)

1. **The compile fix** (csResMenu, 3b 1270–1290 → 3c 1341–1365). The two comment lines (3b 1277–1278) moved above the `CHOOSE`, with a line saying why. The list is the same four items in the same order; set the comments aside and the routine's code is identical to 3b's.
2. **csCas** (3b 725–745 → 3c 788–813). After the quote strip, the undef / error / infinity tests run only when `DIM(cR) > 0` (3c 809–811). The `IFERR` line and the quote strip are byte-identical.
   - **The other INSTRINGs are safe.** csIsFr (3b 761) and csFrDig (781) search the constant `"0123456789"` for one character taken by `MID(s, i, 1)` with i from 1 to DIM(s), so neither argument can be empty.
   - **LEFT and MID are safe.** Both LEFTs take 1 character: csNoZero 427, and csCas 737, which runs only when DIM ≥ 2. Every MID starts at 1 or 2. No RIGHT.
3. **Fixed decimals** (the sweep; 176 `STRING(…, 2, …)` calls read). Every display that real inputs can push below 10^-d now rounds first, `STRING(ROUND(x, d), 2, d)`. Near independence, sparse tables, rare outcomes or ×10 N reach all of these:
   - csEStr 1147 → 1217 (E);
   - csScaleN 1234–1241 → 1305–1312 (χ² and V, before and after);
   - csGrid 1376–1430 → 1454–1508 (E, the row / column / N %, contributions, row and column sums of contributions, χ²);
   - csPageTest 1641–1657 → 1721–1737 (χ², critical value, V, C, G², min E);
   - csPageInterp 1679–1694 → 1761–1776 (χ², V, E);
   - csPage2x2 1728–1744 → 1813–1829 (p1, p2, z, χ², Yates, the RD, RR and OR bounds);
   - csBars 2016–2025 → 2104–2113 (E, (O−E)²/E, χ²);
   - csMosaic 2193 → 2281 (row %);
   - csResBars 2316 → 2404 (E);
   - csCvDraw 2557–2564 → 2646–2653 (crit, χ²);
   - csXX2Txt 965–974 → 1033–1044 (χ²);
   - the Quit line, ChiTable 3281 → 3370 (χ², V).

   The helpers round inside, so every caller is covered:
   - **csSgn** (455–459 → 516–522), for the residuals, RD and phi. "+ 0" turns a rounded −0 into 0, so −0.004 reads "+0.00".
   - **csNoZero** (423–429 → 472–478), for APA's V: 0.004 gives ".00".
   - **csAStr** (444–452 → 493–510). Only a *typed* α can be below 0.0001; the drag stops there. Such an α gets the decimals it needs: 0.00005 shows as "0.00005", 5E-8 as "0.00000005" (at most 11).
   - **csPageExact** (3b 1811–1812 → 3c 1898). A Fisher p below 0.0001 is no longer put through `STRING(…, 2, 4)` before "(< 0.0001)" replaces it.

   **Left as they were, and why:**
   - p-values keep "p < 0.0001" (csPStr, csXPText, the Fisher plot's "P < 0.0001").
   - Counts (d = 0) are whole numbers.
   - The bars, curve and Fisher axes count up from 0.
   - The residual axis spans at least −3..3 in whole steps (rbMx starts at 3).
   - The Simpson bars come from the fixed example tables.
   - csEntry's "Counts are whole numbers: … was rounded to …" shows the count as the student typed it. Rounding would print "0.00" for a typed 0.004 and hide it, and csEntry is device-tested, so it is unchanged.
4. **Header.** "beta 3c" in the banner. A "WHAT CHANGED in beta 3c" paragraph quotes the finding, with beta 3b's line numbers. The status lines now say what rounds 1 and 2 showed.

Nothing else changed. The verify script checks that the routines that differ from 3b are exactly ChiTable, csAStr, csBars, csCas, csCvDraw, csEStr, csGrid, csMosaic, csNoZero, csPage2x2, csPageExact, csPageInterp, csPageTest, csResBars, csScaleN, csSgn and csXX2Txt. It also checks that thirteen of them differ **only** by the ROUND wrapping, and that csResMenu differs only in comments.

## Verification

`verify_ChiTable_beta3c.py`, built from the 3b script and run in harness **ppl_run_v3d**. Output in `verify_ChiTable_beta3c_output.txt`: **6074 checks passed, 0 failed.** The 3b script had 5969.

- **Kept:**
  - the Giac traps;
  - 18 edge tables and 450 random tables against Python fractions and SciPy;
  - the tea, example 2 and example 3/4 runs, end to end with `cas='giac'` and `cas='fail'`;
  - the fence and the cache;
  - the CHOOSE widths;
  - the routines byte-identical to beta 2. csCvDraw, csBars and csMosaic now differ from beta 2 only by the ROUND wrapping; the other 14 are byte-identical.
- **R1, the compile fix:**
  - ppl_check_v4 E12: beta 3b 2, beta 3c 0;
  - a scan of our own finds beta 3b's comments at 1277 and 1278 (inside the `{` of 1274) and none in 3c;
  - the Results menu still runs ×10 N, N / 10 and Restore.
- **R2, csCas:**
  - a failed call returns "" with no error;
  - with Giac, 34/70 gives 17/35, and 1/0, 0/0 and an infinite limit give "";
  - beta 3b's csCas stops on the failed call (INSTRING).
- **R3, `cas='fail'` end to end** (tea pages 6, 7 and the Fisher plot; example 2 with ×10 N and N / 10; examples 3 and 4): beta 3c completes, every exact page "decimal". **Beta 3b in v3d stops in csCas on all three runs.**
- **R4, fixed decimals.** Four tables and a typed α of 0.00005 run through all 7 pages, ×10 N, N / 10, every plot and Quit, in both CAS modes. The tables: near independence {1000, 1001, 1000, 1000}, sparse {1, 1, 1, 20000}, rare {2, 30000, 1, 30000}, and tea.
  - **Beta 3c: 0 scientific strings.** It shows "Cramer's V = 0.000 (negligible)", "χ² … = 0.000", "phi = +0.000", "Set α (now 0.00005)" and "critical value at α = 0.00005: 16.448".
  - Beta 3b printed 31, 30, 15 and 1 in the same runs: "6.24ᴇ-5", "2.498ᴇ-4", "5.0ᴇ-3" (a 0.005 % share), and "1.2076ᴇ-36" (the Fisher p formatted before "(< 0.0001)" replaced it).
- **R5, the helpers on edge values:** csSgn (8), csNoZero (5), csAStr (10), csXX2Txt (3).
- **S, h.sci_strings over every beta 3c run in the script:** 34 runs, **0 scientific strings**.
- **G:** the routine diff is as listed.

## Gate

In `gate_r2`, `python3 ppl_gate_v1b.py ChiTable_beta3c.txt ChiTable_beta3b.txt` gives **RESULT: PASS**.
- **ppl_check_v4:** 1 W3, the same as 3b; the original's 2 E12 are gone.
- **lint_ppl:** 51 problems (3b: 13). The 38 new ones are all "STRING() with 4 args". lint_ppl splits a STRING call at every comma, so it reads `STRING(ROUND(x, d), 2, d)` as four arguments. It is the tool's limit, the same reading it already gave 3b's `STRING(ROUND(enV, 0), 2, 0)`.
- **fleet_names_v2:** 0 collisions, 0 untagged.

`check.sh`:
- kit lint: 0 errors;
- the full parse stops at the file-level `EXPORT` list, as 3b's does (the tool's limit).

## Device checklist (emulator first, then G2 and G1)

1. **Paste, then Check:** Program Catalog (Shift 1) → ChiTable → Edit → Check. "No errors in the program". This is the step that failed in round 2.
2. **The tea table:** New table 2 × 2 → Values: 3, 1, 1, 3 → Run → Right to page 6. You should see "p = 17/35 = 0.4857" with "exact (CAS)", and the risk difference line "+0.5000 (-0.1001, 1.1001)" (see Unresolved). On page 7: "34 of the 70 equally likely ways", "p = 34/70 = 17/35 = 0.4857", "= 2 = 2.000", "exact (CAS)".
3. **The Results menu:** on any results page tap Menu. All four items show. ×10 N, then N / 10, then Restore all work.
4. **Small values:** New table 2 × 2 → Values 1000, 1001, 1000, 1000 → Run. Page 3 reads "= 0.000", "Cramer's V = 0.000 (negligible)", "C = 0.000"; page 6 reads "phi = +0.000". No number shows a small-capital ᴇ anywhere: the pages, the residuals plot, the ×10 N page, Quit.
5. **A typed α:** main menu → Set α → 0.00005. The menu line reads "Set α (now 0.00005)", and page 3 reads "critical value at α = 0.00005: …".

## Unresolved

- **For Roger: the risk-difference interval can leave [−1, 1].** The tea table's page 6 shows a Wald 95 % CI for RD of (−0.1001, 1.1001); a difference of two proportions cannot pass 1. The Wald interval, p1 − p2 ± 1.96 SE, does this at small n. It is computed as the header documents, so it is not changed here. Options: clip the display to [−1, 1] and say so; switch to Newcombe's hybrid score interval (method 10); or add a note at small n. Your call.
- The fallback (the "decimal" badge) has never been seen on the emulator, because its CAS never failed. The harness shows that it completes.
