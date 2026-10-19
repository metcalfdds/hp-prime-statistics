# ScatterLab beta 2c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 2b; every beta 2b feature is kept, and the user's guide (`scatterlab-guide_beta2.md`) still applies. Every routine except slNum is byte-identical, comments included. Not yet run on hardware or on the emulator: this version has run on the PC harness only.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md` §2 item 9; `findings_D.md` §3) checked beta 2b in 590 checks. b₀, b₁, r, r², SSE and the leverage agree with `linregress` and statsmodels OLS to 1E-9 on 61 data sets, and every guard holds. It found one wrong number:

> **D-SL-1 · WRONG NUMBER (decimal page only) · slNum strips trailing zeros without a decimal point — `1617-1618`.** The Prime's fixed output holds 12 significant digits (§3: `STRING(123456789012,2,2)` = `"123456789012"`, no decimals), so for 1E11 ≤ |x| < 1E12 `slFx(x, 1)` has no "." and the zero strip eats real digits. ppl_run_v3e (which models that limit) prints, for x = 100000, 200000, 300000 (Σx² = 1.4E11): `600000 a + 14 b = 1400000` — the page's second normal equation is wrong by a factor of 10¹⁰. `slNum(1.4E11)` = `"14"`, `slNum(123456789000)` = `"123456789"`. Reached only on the decimal page (the CAS failed, a value needs over 6 decimals, or the text is too long) with crime-sized x.

The review's verdict was "ship as is after one two-line fix". `check_ScatterLab.py` failed 3 of its 590 checks, all of them this.

**Roger's addition (19 Oct 2026, 12:48):** a DISCLAIMER line beside the terms of use in the header.

## What changed (line numbers: beta 2b → beta 2c)

1. **slNum** (2b 1608–1620 → 2c 1631–1656). The trailing-zero strip (2b 1617–1618 → 2c 1649–1654) now runs only when the text holds a "." (`IF INSTRING(nmS, ".") > 0`). `IF DIM(nmS) > 0` comes first, because INSTRING on an empty string is "Invalid input" on the Prime. slFx always returns at least one character, so the DIM test is insurance.
   - **What changes on screen:** `slNum(1.4E11)` is `140000000000`, and the decimal page's line is `600000 a + 140000000000 b = 1400000`.
   - **What does not change:** every number with a decimal point (260.8 stays 260.8), every whole number below 1E9, and the six-significant-digit form from 1E12 up.
   - A comment explains the 12-digit limit for students.
2. **Header:**
   - the banner;
   - the DISCLAIMER line after the terms of use (→ 16–18; Roger's addition, a comment only). No page of ScatterLab states the terms, so no page needed the short line;
   - the firmware lines: beta 2b passed the emulator retest, and beta 2c has run only in the PC harness (→ 20–29);
   - a "What changed in beta 2c (19 Oct 2026)" paragraph with the finding ID and beta 2b's line numbers (→ 33–50).

**Nothing else.** The other 65 routines are byte-identical, comments included. ScatterLab still refuses a line below 3 points (D16 is open), and there is no inference page. The file is still pure ASCII.

## Verification

`verify_ScatterLab_beta2c.py`, built from the 2b script and run in harness **ppl_run_v3e**. Output is in `verify_ScatterLab_beta2c_output.txt`: **116 PASS, 0 failures** (the 2b script had 80).

- **Kept:** every 2b check (parts A, B, G, R1–R7, R10), now run on beta 2c, with the older versions read from `out/` by absolute path (review item 22). The script now stops with a clear message if a file is missing, instead of a `FileNotFoundError` half-way.
- **Changed:** two checks.
  - **R7:** the list of INSTRING first arguments now includes `nmS`, slNum's new guarded site, and the guard list includes slNum's DIM guard. The old expected set was 2b's.
  - **G 2b:** the 2b-vs-2a record reads the 2b file.

  Beta 2b's own script, run unchanged with PROG pointed at beta 2c, fails exactly one check: R7's INSTRING list, as intended.
- **New, part D** (each test on beta 2c and on beta 2b):
  - **D1:** slNum on 14 values, including the review's.
    - Beta 2c gets all 14 right.
    - Beta 2b gets 4 wrong, every one a number of 1E11 or more ending in 0: 1.4E11 → `14`, 1.23456789E11 → `123456789`, −1.4E11 → `-14`, 1E11 → `1`. Below 1E11 (5E10 → `50000000000.0`) the "." is there, and beta 2b was right.
  - **D2:** the decimal page itself, with the CAS failing. For x = 1E5, 2E5, 3E5 it reads `600000 a + 140000000000 b = 1400000`; beta 2b printed `600000 a + 14 b = 1400000`.
  - **D3:** a property sweep of 2,698 values from 1E-7 to 1E12, both signs, with whole numbers up to 1E12 that end in zeros. The text never loses a digit beyond the shown decimals and the 12-digit limit, and has no trailing zero or point after a ".". Beta 2c: 0 wrong. Beta 2b: 236 wrong, every one 1E11 or more.
  - **D4:** the review's own `check_ScatterLab.py`, its SRC pointed at each version. Beta 2c: **590 checks, 0 failures**. Beta 2b: 590 checks, 3 failures, the three slNum ones.
  - **D5:** two points, one point and three equal x still give no line, `SL_B1` = 0 and the note "Need at least 3 points with different x.", as in beta 2b.
  - **G2c:**
    - only slNum differs from beta 2b;
    - its code lines are 2b's plus `IF DIM(nmS) > 0 THEN`, `IF INSTRING(nmS, ".") > 0 THEN` and two `END;`;
    - outside slNum only comments differ;
    - the file is pure ASCII, and every LOCAL line has 6 names or fewer;
    - the banner, status lines and paragraph say beta 2c;
    - the DISCLAIMER sentence sits right after the terms, and no page states the terms.
- **R10, `h.sci_strings` over all 49 beta 2c runs:**
  - no small number;
  - from 1E12 up only slNum's six significant digits on the decimal page (`1.40000ᴇ12`, `8.69000ᴇ12`). The Prime holds 12 digits, so scientific is its only form for these.

## Gate

`python3 ppl_gate_v1b.py ScatterLab_beta2c.txt _old/ScatterLab_beta2b.txt`, in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, the same as 2b; no hard errors, E12 included.
- lint_ppl: 30 problems (2b: 29). The new one is its known misreading of `INSTRING(` as a `STRING(` call with 2 arguments (2c line 1650), the same reading it gives the other INSTRING lines.
- Full parse: stops at the file-level `LOCAL` after the EXPORT lines (2c line 236, the same statement as 2b's 213). This is the tool's limit.
- fleet_names_v2 over 25 files: 1,292 routine names, 0 collisions, 0 untagged, 0 built-in matches.

`check.sh fix19/ScatterLab_beta2c.txt out/ScatterLab_beta2b.txt`: kit lint 0 errors; no hard errors; the parse fails on the same statement as the old file.

## Device checklist (emulator first, then G2 and G1)

1. Replace ScatterLab in the Connectivity Kit (open it and paste over it; never a second copy). Program Catalog → Edit → Check: no errors.
2. In Home, type `STRING(140000000000,2,1)`. Note whether it gives `140000000000` or `140000000000.0`; the fix is right either way.
3. **The decimal page:**
   - Data → Clear all points, then Menu → Type a point four times: (100000, 1), (200000, 2), (300000, 3) and (0, 1/3). The last point "needs over 6 decimals", so the page cannot ask the CAS, and x = 0 leaves the sums of the first three unchanged.
   - Then Menu → Least squares as calculus. The page says "decimal" and "A value needs over 6 decimals: no exact fractions.", and its equations read `4 a + 600000 b = 6.33333` and `600000 a + 140000000000 b = 1400000`. Beta 2b showed `14 b` there (harness, both versions checked).
4. The emulator's calculus page (Data → Poverty vs crime → tap the equation) still shows `b = 2441/2394` and "exact (CAS)".

## Unresolved

- **D16** (Roger): show the two-point line with a warning, or keep refusing n < 3 (kept here); and whether to add the slope-inference page (review §4 item 1, not in this pass).
- D-SL-2 ("nearly identical x" gives a slope made of rounding) was listed by the review as an improvement, not a fix-now item; it is not in this version.
