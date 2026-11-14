# ChiTable beta 3m: changes (13 November 2026)

Round 13 of 13 November 2026: the exact test for ChiTable's 2 × 3 and 3 × 2 tables. Roger, 13 November 2026, about the rule that every expected count be 5 or more: "If chi square cell counts are less than 5 what do we tell the student to do?  We have Fishers exact in there right?", then "Could we do an exact test for a bigger table?" Tables bigger than ChiTable's are not for this project ("I'm not sure we gain much by adding bigger tables. What about, layer on and not for this project, doing larger tables in python or Maple?"); for the 2 × 3 and 3 × 2 tables: "Go!". The build is `verify/round13/make_chitable_3m.py`: each change is an exact replacement in ChiTable beta 3l (a miss stops it).

## What changed

1. **The exact test for a 2 × 3 or 3 × 2 table** (`csFishRC`, `csRCEnsure`). Fisher's rule with more columns (Freeman and Halton 1951): keep every row total and every column total, list every table that has those totals, and add up the chances of the tables no more probable than the one observed; that sum is the two-sided p, the one R's `fisher.test` gives. A 3 × 2 table is first turned on its side (the p does not change); in a 2 × 3 table the first row's a and b decide the rest. The chance of a table is C(c1, a) C(c2, b) C(c3, c) / C(N, r1), kept as logarithms built one from the next by C(m, k+1) = C(m, k)(m − k)/(k + 1), so no factorial is ever computed and nothing overflows in 12 digits (and no `LNGAMMA`, which the Prime has only in its CAS). The chances are added relative to the table of expected counts, so the largest term is about 1. A table exactly as probable as the observed one counts, within 1E−7 in the log, R's tolerance. More than 10,000 tables are not counted: then there is no p, and the page says to merge cells. The p is kept for the table it belongs to (`csRCKey`, the key the exact page already uses), so turning the pages does not count again.

   Results page 5, when an expected count is below 5, said "χ² is shaky; Fisher (2x2) or merge cells." for every shape. It now says, under "n of m expected counts are below 5:":
   - a 2 × 3 or 3 × 2 table: "χ² is shaky; exact test (Freeman-Halton): p = 0.2308" (the table 3 1 4 / 1 5 2);
   - more than 10,000 tables: "χ² is shaky; too many tables to count: merge cells.";
   - a 2 × 2 table: "χ² is shaky; see Fisher's exact test, page 6." (page 6 has given Fisher's test since beta 3).

2. **Help page 1** names both exact tests (below).

3. **Page 5's "Largest surprise"** called a count equal to its expected count "MORE than expected" (the test was O ≥ E). A count equal to its E at the two decimals shown, which happens in a table with no association at all, is now "just as expected"; every other line is beta 3l's, word for word (the verify script's X5). Found on the Virtual Calculator while page 5's new line was being looked at: the table 1250 1250 2 / 1250 1250 2 showed "O = 1,250, E = 1,250.00: MORE than expected".

4. **Nothing else changed**, apart from the header and the history note.

Lines of ChiTable beta 3m that differ from ChiTable beta 3l: line 4 (comment); lines 42-49 (comment, the history note); lines 576-577 (code: the file-level `csRCKey, csRCP` and their comment); lines 2057-2171 (code: the comment block, `csFishRC` at line 2092 and `csRCEnsure` at line 2162, placed before `csPageInterp`); lines 2196-2200 and 2202-2206 (code: `csPageInterp`, "just as expected"); lines 2215-2225 (code: `csPageInterp`, page 5's line); lines 3680-3681 (code: `csHelp`, help page 1); line 3800 (code: `csInit`, `csRCKey := ""; csRCP := -2;`).

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only screen 1 changed.

### Screen 1, before (beta 3l)

```text
ChiTable help 1/6: χ² for a two-way table
Pick a table shape, then tap each cell and type its OBSERVED
count.  Run computes everything.
Expected count E = row total x col total / N:
what the cell would hold if the two variables were independent.
χ² adds (O - E)² / E over the cells: a big χ² means the counts are
far from what independence predicts.
df = (rows - 1)(cols - 1).  p is the right tail of the χ² curve, drawn
by the curve plot.
Assumption: every expected count is 5 or more (the pages flag
any E below 5).  If not: use Fisher's exact (2x2) or merge sparse
categories.
Pages: O and E, percentages, the test, the cell contributions,
meaning, 2x2, exact answers.
Any key = page 2
```

### Screen 1, after (beta 3m)

```text
ChiTable help 1/6: χ² for a two-way table
Pick a table shape, then tap each cell and type its OBSERVED
count.  Run computes everything.
Expected count E = row total x col total / N:
what the cell would hold if the two variables were independent.
χ² adds (O - E)² / E over the cells: a big χ² means the counts are
far from what independence predicts.
df = (rows - 1)(cols - 1).  p is the right tail of the χ² curve, drawn
by the curve plot.
Assumption: every expected count is 5 or more (the pages flag
any E below 5).  If not, use the exact test (page 6 for a 2x2,
page 5 for 2x3 and 3x2) or merge sparse categories.
Pages: O and E, percentages, the test, the cell contributions,
meaning, 2x2, exact answers.
Any key = page 2
```

## Checks

- `verify/verify_ChiTable_beta3m.py`: 17 of 17 PASS (`verify/verify_ChiTable_beta3m_output.txt`). T1, T2: the build makes the file byte for byte, and every changed line belongs to a replacement. X1: `csFishRC` on 669 tables (300 random 2 × 3, 300 random 3 × 2, 60 larger, ties, empty rows and columns) against a brute-force count in Python's exact integers, largest difference 2.9E−15; on the 651 with no empty row or column against R 4.3.3's `fisher.test`, largest difference 1.5E−12. X2: 10,981 tables returns −1; 4,921 are counted. X3: page 5's line for each case above, and beta 3l's line when every E is 5 or more. X4: help page 1; ASCII; no `!=`; no `LOCAL` line with more than 6 names. X5: "just as expected" for a table with no association at all; on 194 random tables, 193 lines are beta 3l's word for word and 1 is "just as expected" where O = E.
- SciPy was not a reference: SciPy 1.18.1's `fisher_exact` takes an R × C table but answers it by simulation, a different number on each call (four calls on 3 1 4 / 1 5 2 gave 0.2336, 0.2356, 0.2406 and 0.2335; R and ChiTable give 0.2307692).
- `tools/ppl_gate_v1e.py` against ChiTable beta 3l: PASS. hp-prime-kit lint 0 errors; `ppl_check_v5` 27 W3, as beta 3l; no hard errors; the full parse stops at the forward declarations, the kit's own limit, as in beta 3l. `fleet_names_v2` over the 31 newest files: no collisions (`verify/round13/checks_r13.py`).
- Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured: 6 screens, no reports. The help dumps: screen 1 is the only one that changed, and only as above.
- `tools/label_fit_v1.py` on the walk reports one new line, help page 1's "any E below 5).  If not, use the exact test (page 6 for a 2x2,", 338.5 px at its flat 5.5 px a character against the width 296. At the glyph widths measured on the Virtual Calculator it is 266 px (beta 3l's line there was 289 px), and the Virtual Calculator draws it whole (`verify/round13/screens/ChiTable_help1_r13.png`). Its other line, help's "Curve: drag the red dotted line ..." (286 px measured), is beta 3l's. On the verify script's own run: no number cut by its width argument.
- `tools/comma_check_v1.py` against beta 3l, 100 seeds (`verify/round13/comma_check_r13.txt`): R1 every run takes beta 3l's path; M every number of four or more digits drawn has its commas; C every text handed to the CAS is beta 3l's; Y no year drawn with a comma. Its D reports label_fit's line above and nothing else.
- The harness smoke test (main routine, idle key Esc): OK, warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: the same report as beta 3l (apart from its timing): screens 12/900, collisions 0 (firm 0), straddles 0, overruns 0, ghosts 0. `--run` on the verify script: 198 of 200 screens, collisions 0, straddles 0, overruns 0, ghosts 0.
- The monkey (`tools/monkey_chunks_v1.py`, base 13, with `--lists`) on the final file: 1000 of 1000 runs OK (`verify/round13/mk/ChiTable.jsonl`).
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026 (`verify/round13/vc_checks.txt`): Check said "No errors in the program". Run: help page 1 inside its page; 3 1 4 / 1 5 2 and its 3 × 2 turn, 3 1 / 1 5 / 4 2, both "exact test (Freeman-Halton): p = 0.2308"; 1250 1250 2 / 1250 1250 2, "too many tables to count: merge cells." and "just as expected"; the 2 × 2 table 3 1 / 1 3, page 5 points to page 6, and page 6 gives "p = 17/35 = 0.4857", exact (CAS). The pack carries a fresh copy, Checked with nothing run.

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at:

- Help page 1: the two new lines inside the page.
- New table: 2 × 3, Values 3 1 4 / 1 5 2, Run, Right four times: page 5 says "exact test (Freeman-Halton): p = 0.2308". New table: 3 × 2, 3 1 / 1 5 / 4 2: the same p.
- **The time it takes.** New table: 2 × 3, 950 900 1 / 900 950 3 (9,248 tables, near the 10,000 limit): how long does page 5 take to appear the first time, on a G1 and on a G2? Its p is 0.1996 (R: 0.1995689827). Turning back to page 5 afterwards should be at once (the p is kept).
- 1250 1250 2 / 1250 1250 2: "too many tables to count: merge cells.", and "O = 1,250, E = 1,250.00: just as expected".
- A 2 × 2 table, 3 1 / 1 3: page 5 points to page 6; page 6 gives p = 17/35 = 0.4857.

## Unresolved

- How long 9,000 to 10,000 tables take on a G1 is not known. If page 5 is slow there (more than a few seconds), the limit can come down: a table that small counts make shaky has far fewer tables (a 2 × 3 table of 100 cases has about 900).
- ChiTable takes 2 × 2, 2 × 3 and 3 × 2 tables only. Larger tables, if ever, belong in Python or Maple, not in this project (Roger, 13 Nov 2026).
