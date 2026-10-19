# ChiTable beta 3d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 3c; every beta 3c feature is kept. csFisher, csFishW, csCheck, csTotals, the CAS call line and every drag are untouched. Not yet run on hardware or on the emulator: this version has run on the PC harness only.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md` §2 items 8 and 20, §3 D8; details in `findings_D.md` §2) read beta 3c in full and re-derived every number (79,149 checks, no wrong formula). It found these:

- **D8, Roger's decision (19 Oct 2026): Newcombe for the risk difference.** The review put it this way: "The Wald form `RD ± 1.96·SE` (`1111-1113`) leaves [−1, 1] in 17.8% of all 2×2 tables with row totals ≤ 12 (e.g. the tea table: `+0.5000 (−0.1001, 1.1001)`; [3,1,0,4]: `(0.3257, 1.1743)`) and collapses to width 0 whenever p₁, p₂ ∈ {0,1} ([5,0,0,5]: `(1.0000, 1.0000)`)." Its recommendation was Newcombe, "because the program already teaches that the normal approximation is shaky below E = 5 and then prints an interval that says 1.17."
- **D-CT-1 · wrong number (Home export only).** "`1 − CHISQUARE_CDF` at 12 digits — `1082`, `1084`, `1103`. `CS_P` is exactly 0 on the Prime for χ² above ~52 (df 1) / ~55 (df 2)… the screen's `p < 0.0001` hides it, the `CS_P` a student types in Home does not."
- **D-CT-2 · wrong text.** "The Cochran rule is stated one way and applied another — help `3198-3200` vs pages `1737-1742`, `1784-1785`." The help says "expected counts of 5 or more (at least 80% of cells, none below 1)". The pages flag *any* cell below 5.
- **D-CT-3 · cosmetic.** "The 'was rounded to' message prints the typed value unrounded — `1656`." Typing 0.004 gives `Counts are whole numbers: 4.00ᴇ−3 was rounded to 0.`
- **D-CT-4 · cosmetic.** "Huge counts overflow the cells and the exact page — `1447`, `1874-1875`." With 1E9 counts, the counts-put-in line on the exact page is about 380 px wide in a 296-px box.
- **D-CT-5 · cosmetic.** "The Values form clamps a negative silently — `1583`." −5 becomes 0, while the cell editor says "A count cannot be negative."

**Roger's addition (19 Oct 2026, 12:48):** a DISCLAIMER line beside the terms of use in the header.

## What changed (line numbers: beta 3c → beta 3d)

1. **New `csUpper(df, x)`** (→ 1108–1132, just before csCompute). It gives the p-value, the upper tail, **without `1 − CDF`**:
   - df 1: `2 · NORMALD_CDF(0, 1, −√x)`. A χ² with 1 df is z².
   - df 2: `EXP(−x / 2)`. A χ² with 2 df is exponential with mean 2.
   - x ≤ 0 gives 1, so a G² a hair below 0 from rounding never reaches a square root of a negative number.
   - Any other df keeps `1 − CHISQUARE_CDF`, for a future r × c table.
   - The comments tell students why a lower tail keeps its digits on a 12-digit machine and `1 − CDF` does not.
2. **csCompute uses it for every p** (D-CT-1):
   - χ²: 1082 → 1196;
   - G²: 1084 → 1198;
   - Yates: 1103 → 1218.

   `CS_P` (1132 → 1263) gets its digits from it. The screen is unchanged: below 0.0001 it still says "p < 0.0001".
3. **New `csWils(k, n, z, s)`** (→ 1134–1160): one end of a Wilson score interval. It returns 0 exactly at k = 0 (lower end) and 1 exactly at k = n (upper end), so rounding can never push an end past 0 or 1. Its comments derive the interval for students.
4. **The RD interval is Newcombe's hybrid score interval** (D8; Newcombe 1998, method 10). The Wald lines 1111–1113 are replaced (→ 1226–1252):
   - the four Wilson ends (`cpL1`, `cpU1`, `cpL2`, `cpU2`);
   - `RD − √((p1 − L1)² + (U2 − p2)²)` and `RD + √((U1 − p1)² + (p2 − L2)²)`.

   A comment block says why Wald fails at small n: width 0 at p = 0 or 1, ends past ±1, and 1,388 of the 7,812 grid tables (17.8%) outside [−1, 1]. The four names joined csCompute's LOCAL line (1054 → 1166, now 6 names). The counts are the observed ones; the +0.5 rule stays with RR and OR.
5. **Page 6's note** (csPage2x2 1830–1834 → 1996–2007):
   - without a zero cell: `(95% CIs; Newcombe for RD, log for RR and OR)`. Roger's wording, "(95% CIs; Newcombe for RD, log method for RR and OR)", is 52 characters. The page's other lines are at most 48, the longest seen whole on the emulator, so "method" goes.
   - with a zero cell (red): `(95% CIs; zero cell: +0.5 per cell for RR, OR)`. Beta 3c's "+0.5 added to every cell" read as if it applied to RD too; it never did, under Wald or Newcombe.
6. **Help page 1, the assumption** (D-CT-2, csHelp 3198–3199 → 3390–3391). It now states the rule the pages apply: `Assumption: every expected count is 5 or more` / `(the pages flag any E below 5).  If not: use`. This is the honest minimum. Which rule to teach is still Roger's decision; see Unresolved.
7. **csEntry, the cell editor** (1651–1661 → 1806–1827):
   - a count above 9,999,999 (after rounding) is refused with `Counts above 9,999,999 do not fit the table: enter the data divided by 10.`, and the cell keeps its count (D-CT-4);
   - the "was rounded to" message rounds the typed value first, `STRING(ROUND(enV, 2), 2, 2)`: `Counts are whole numbers: 0.00 was rounded to 0.` (D-CT-3).
8. **csAskAll, the Values form** (1558, 1581–1585 → 1697, 1720–1740):
   - a count above 9,999,999 keeps its cell's old count, and one message says why (D-CT-4; new LOCAL `akBig`, 5 names);
   - the `MAX(0, …)` is gone (D-CT-5): a negative count stays in the grid, and Run refuses it with csCheck's "A count cannot be negative.", as for the cell editor and a bar drag.
9. **The exact page, the counts put in** (csPageExact 1873–1875 → 2046–2061; D-CT-4). The two lines are built first and measured. If either is longer than 46 characters (the test the page's other lines already use), line 1 reads `  (your counts are too long to write out here)` and line 2 is left out. The CAS's whole numbers and the fraction follow as before. findings_D proposed `"  = N(ad - bc)² with the counts above"` for line 1 only. Line 2 overflows too, and there are no counts "above" on that page, so this version uses words that say what happened.
10. **Header:**
    - the banner;
    - the DISCLAIMER line after the terms of use (→ 15–17; Roger's addition, a comment only). No page of ChiTable states the terms, so no page needed the short line;
    - the tested-on lines: 3c passed the emulator retest, and 3d has run only in the PC harness (→ 25–38);
    - a "WHAT CHANGED in beta 3d (19 Oct 2026)" paragraph with the finding IDs and beta 3c's line numbers (→ 42–90);
    - the arithmetic notes (316, 327 → 371–374, 384–387).

**Nothing else.** The routines that differ from beta 3c are exactly csCompute, csAskAll, csEntry, csPageExact, csPage2x2 and csHelp, plus the new csUpper and csWils. Each differs in exactly the code lines listed above (verify, part G3d). The file is still pure ASCII.

## Verification

`verify_ChiTable_beta3d.py`, built from the 3c script and run in harness **ppl_run_v3e**. Output is in `verify_ChiTable_beta3d_output.txt`: **6,931 checks passed, 0 failed** (the 3c script had 6,074).

- **Kept:** every 3c check (parts A–E, G, W, R), now run on beta 3d. Three were changed, because their expected value was the finding or the routine was meant to change:
  - **R6:** the tea table's RD line is now `+0.5000 (-0.1355, 0.7891)`, not Wald's `(-0.1001, 1.1001)`;
  - **E:** csCompute, csAskAll and csEntry are no longer "byte-identical to beta 2". The check now says they were in 3c and change in 3d, and G3d pins the change. The other eleven are still byte-identical;
  - **G 3c:** the 3c-vs-3b record reads the 3c file.

  Beta 3c's own script, run unchanged with SRC pointed at beta 3d, fails only on these intended changes (see the note after this list).
- **N1, Newcombe** (each run on 3d and on 3c):
  - **csWils** on 671 intervals (n = 1–30, 50, 100, 674, 1000, 9,999,999): it equals statsmodels' Wilson interval to 3E-16, and a 40-digit Wilson at the program's z to 2E-16;
  - **our 40-digit Newcombe** equals statsmodels `confint_proportions_2indep(method='newcomb')` on all 7,812 grid tables, to 4E-16;
  - **csCompute's interval over the review's grid** (every 2 × 2 with row totals ≤ 12, 7,812 tables) and 9 big tables (up to 9,999,999 per cell):
    - the maximum error against the exact Newcombe at z = 1.959964 is **2.6E-16**;
    - it is never outside [−1, 1] and never of width 0;
    - it always holds RD;
    - **beta 3c** on the same grid: 1,388 outside [−1, 1] (17.8%) and 288 of width 0.
  - **The z constant.** The program's z = 1.959964, against statsmodels' 1.959963985, moves an end by at most 5.5E-9, which does not show at 4 decimals.
  - **A 12-digit transcription** (Python decimal, 12 significant digits, of csWils and the four lines) on the same 7,821 tables: none outside [−1, 1], none of width 0, max error 6.5E-12.
  - **Page 6** shows findings_D's three values: tea `(-0.1355, 0.7891)`, [3,1,0,4] `(0.0852, 0.9544)`, [5,0,0,5] `(0.3855, 1.0000)`. Beta 3c shows `(-0.1001, 1.1001)`, `(0.3257, 1.1743)` and `(1.0000, 1.0000)`.
- **N2, csUpper:**
  - against scipy `chi2.sf` (df 1 and 2, χ² from 1E-9 to 1400): max relative error 2E-13. χ² ≤ 0 gives 1;
  - huge tables (χ² = 200, a 2 × 3 with χ² = 600, a 3 × 2 with χ² = 394): `CS_P`, csPG and csPY equal scipy to 1E-9. **Beta 3c's `CS_P` is exactly 0**, even in double precision;
  - with the Prime's 12-digit built-ins modelled (the review's `twelve_digits()`): [45,5,5,45] (χ² = 64) gives `CS_P` 0 on beta 3c and 1.24419E-15 on beta 3d, which is right. `csUpper(1, 60)` = 9.48574E-15;
  - every results page and the bars plot for 8 tables (the four examples, tea, three huge or near-null tables) is identical to beta 3c's, except page 6's RD line and note.
- **N3, the assumption.** Take a 2 × 3 with one E = 4.5 (1 of 6 below 5, none below 1). Page 5 says "chi-square is shaky" and page 3 is red, in both versions. Beta 3d's help states the every-cell rule, which agrees. Beta 3c's help stated the 80% rule, which passes this table: that was the inconsistency.
- **N4, the rounded message.** Typed 0.004 gives `0.00 was rounded to 0.` (beta 3c: `4.00ᴇ−3`, scientific). Typed 2.4, 7.25 and 9999999.4 give the right messages.
- **N5, huge counts:**
  - the editor refuses 1E9, 1E7, 9999999.6 and 1E12 and keeps the cell; it takes 9,999,999. Beta 3c took every one;
  - the Values form refuses 1E9 × 4 (the review's probe P2; beta 3c took them and ran). For [5, 1E9, 3, 7] the form keeps that one cell's count;
  - the exact page for 9,999,999 × 4, [9999999, 1, 2, 9999998] and the 1E9 table uses words, and nothing exceeds its width. Beta 3c's lines ran past the 46-character rule, and past 296 px (est.) for two of them;
  - tea, example 2, example 2 × 10 and 5-digit counts are unchanged.
- **N6, a negative in the Values form:** −5 stays in the grid and Run says "A count cannot be negative."; corrected, Run computes. Beta 3c made it 0 silently.
- **N7, the note:** both branches; ≤ 48 characters; inside the 296-px width.
- **The review's own probe script.** `check_ChiTable_harness.py` was run on both versions with its SRC replaced:
  - P1 shows no scientific form on beta 3d;
  - P2 shows beta 3d refusing the 1E9 counts;
  - P5 gives Newcombe on beta 3d and Wald's width 0 on beta 3c;
  - P7, the stale-key run, completes.

  `check_ChiTable.py` itself had no failing check: it is a Python transcription of beta 3c. Its §6, §7 and §9 findings are N1 and N2 above.
- **G3d, static checks:**
  - csUpper and csWils are defined once, before csCompute, and called only from it;
  - none of the 17 new names is a built-in, ignoring case;
  - every LOCAL line has 6 names or fewer;
  - the INSTRING, LEFT, MID and RIGHT calls are beta 3c's;
  - every new fixed-decimal STRING rounds first;
  - no comment sits inside an open bracket;
  - the DISCLAIMER sentence sits right after the terms of use, and no page states the terms.
- **S, `h.sci_strings`:** **0** over all 78 beta 3d harness runs in the script.

**Beta 3c's script run unchanged on beta 3d** (only its SRC replaced; harness v3d): **6,067 passed, 7 failed**. The 7 are the intended changes and nothing else:
- R6's Wald line;
- csCompute, csAskAll and csEntry "differ from beta 2" (3 checks);
- the G 3c routine list, csPage2x2 and csPageExact, all three because that section compared the file under test with beta 3b.

## Gate

`python3 ppl_gate_v1b.py ChiTable_beta3d.txt _old/ChiTable_beta3c.txt`, in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 1 W3, the same as 3c (page 3's table line, unchanged). No hard errors, E12 included.
- lint_ppl: 52 problems (3c: 51). The new one is its known miscount of `STRING(ROUND(enV, 2), 2, 2)` as four arguments.
- Full parse: stops at the file-level `LOCAL` after the EXPORT list (3d line 416, the same statement as 3c's 357). This is the tool's limit.
- fleet_names_v2 over 25 files: 1,292 routine names, 0 collisions, 0 untagged, 0 built-in matches.

`check.sh fix19/ChiTable_beta3d.txt out/ChiTable_beta3c.txt`: kit lint 0 errors; no hard errors; the parse fails on the same statement as the old file.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 3c (open it in the Kit; never a second copy). Program Catalog → ChiTable → Edit → Check: no errors.
2. **Newcombe:** New table 2 × 2 → Values 3, 1, 1, 3 → Run → page 6.
   - It reads `Risk diff. p1 - p2 = +0.5000 (-0.1355, 0.7891)` and `(95% CIs; Newcombe for RD, log for RR and OR)`. Both lines are whole.
   - Then Values 5, 0, 0, 5: `+1.0000 (0.3855, 1.0000)` and the red `(95% CIs; zero cell: +0.5 per cell for RR, OR)`.
3. **CS_P:** Values 100, 0, 0, 100 → Run → Esc → Quit. In Home, `CS_P` gives about **2.09E-45**, not 0. Also type `NORMALD_CDF(0,1,-10)`, which should give 7.62E-24.
4. **Help, page 1:** the red lines read "Assumption: every expected count is 5 or more" and "(the pages flag any E below 5).  If not: use".
5. **Entry:**
   - Edit a cell and type 0.004: `Counts are whole numbers: 0.00 was rounded to 0.` (no small-capital E);
   - type 1000000000: `Counts above 9,999,999 …`, and the cell keeps its count;
   - Values with −5 in one cell, then Run: "A count cannot be negative.", and the grid stays.
6. **The exact page with big counts:** Values 9999999 four times → Run → page 7. It reads "(your counts are too long to write out here)", and no line runs off the right edge.

## Unresolved

- **D-CT-2 / D8, which expected-count rule to teach** (Roger): "every expected count ≥ 5" (what the pages apply, and now what the help says) or Cochran's "at least 80% of cells ≥ 5, none below 1". Either is one line on page 5 and two on help page 1.
- **The note's wording:** "log for RR and OR" stands in for "log method for RR and OR" (52 characters). If the full wording fits on the device, it can come back.
- **Typed counts can make N 8 digits.** The new cap is per count, as findings_D proposed; ×10 N still caps N at 9,999,999. With four or six counts near 9,999,999, N has 8 digits, and the grid's `N = ` cell (font 2, 72 px) may clip it. Not seen on a device.
- The CAS fallback ("decimal" badge) has still never been needed on the emulator; the harness shows that it completes.
- **The user's guide is now stale in one line.** `chitable-guide_beta3.md` line 240 still says "p = 1 − CHISQUARE_CDF(df, X²)" and "RD with a Wald interval". It was not part of this pass, so it is not changed here; the next guide version should say csUpper's closed forms and Newcombe.
