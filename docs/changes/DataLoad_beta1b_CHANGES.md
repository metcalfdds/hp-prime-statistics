# DataLoad beta 1b: changes and device checklist (31 October 2026)

*The version in `programs/` and in the starter pack v2. beta 1 and 1a: `DataLoad_beta1_NOTES.md`, `DataLoad_beta1a_CHANGES.md`.*

## Change

- **The line DataLoad returns is cleared at the start of every run** (`ddLAST := ""` in `DATALOAD()`). beta 1a, run a second time and quit without loading, returned the first run's line ("DataLoad: M1 col 1 by col 3 → D1-D2, D3 cleared"); a file-level variable keeps its value from one run to the next. Now such a run returns "DataLoad: nothing loaded".

## Checks

- Gate `ppl_gate_v1c.py`: PASS. Kit lint 0 errors; no hard errors (E2/E3/E6/E8/E10/E11/E12); `lint_ppl` 538 checks, the 4 entry-point notes every single-EXPORT program gets; the parse stops at the first file-level `LOCAL` (the kit tool's limit).
- `fleet_names_v2.py programs/*.txt`: 29 files, 2,200 routine names, 0 collisions, 0 untagged, 0 built-in matches. `case_scan_v1.py`: nothing to report.
- `verify/verify_DataLoad_beta1b.py`: **56 PASS, 0 FAIL** (`verify_DataLoad_beta1b_output.txt`). K10 is new: a second run that loads nothing returns "DataLoad: nothing loaded". The same script run on beta 1a fails K10 with beta 1a's line, so the check sees the fault.
- `hpprime write` → `DataLoad.hpprgm`, 73,068 bytes, read back equal to the source. The starter pack v2 carries this same file (SHA-256 `a82ce1107cd064a0…`).

## The run on the Virtual Calculator (31 Oct 2026, 19:57–19:59 CDT)

beta 1a's file set aside to `…\_set_aside_2026-10-31\vc_before_dataload_beta1b`, beta 1b's copied in. Check: "No errors in the program". Scores by group, 1 by 3, with D1 and D2 holding data: "D1, D2 hold data", "Replace D1-D2", the two groups of 216. Quit: "DataLoad: M1 col 1 by col 3 → D1-D2". `DATALOAD` again, Quit at once: **"DataLoad: nothing loaded"**.

What beta 1b has run, all told, on the Virtual Calculator: both loads, on the Rossi data (432 × 5) and on a 10 × 3 matrix with text codes, a blank and a short column; the summary and the histograms; clearing and keeping leftover lists; the form; Help; and TTestLab reading the loaded D1 and D2 (beta 1 run, same loading code). Its numbers agreed with Python and SciPy throughout (`DataLoad_beta1_NOTES.md`).

## Device checklist (G1 and G2: not yet run)

1. **Getting a matrix in.** In the Connectivity Kit, drag `M1.hpmat` (from the Data Loader page or `data-loader/examples/`) onto the calculator. Does M1 arrive as 432 × 5? If not, open M1 in the Kit's matrix editor and paste the columns from a spreadsheet; note which works.
2. Open Statistics 1Var once, then send `DataLoad.hpprgm`; run `DATALOAD`. Menu title "DataLoad: M1, 432 × 5".
3. **Columns**: time it (Virtual Calculator: under 4 s for 2,160 cells). The summary: D1–D5, "M1 col 1" … "M1 col 5", n 432; text clear of the n column.
4. **Tap D4**: x̄ 24.6, s 6.113, min 17, Q1 20, med 23, Q3 27, max 44. Compare with Statistics 1Var's own Stats for D4.
5. **Scores by group**, 1 by 3: "D1-D5 hold data" with "Fill D1-D2, clear D3-D5" first. Clear: only D1, D2 remain, n 216 each. Check D3–D5 are empty in the Numeric view.
6. **TTestLab** → independent, not equal → Raw scores in D1 and D2 → two-tailed, .05: t(421.19) = −1.68, p = 0.094.
7. **AnovaLab** → Use my data (D1-D9) → one-way: exactly two groups, F(1, 430) = 2.82, p = 0.094 (SciPy's `f_oneway`; the pooled t squared). Five groups here would mean the leftover lists were read.
8. **The C lists:** menu item 5 to "Lists: C (Statistics 2Var)", open Statistics 2Var once first, Columns: C1–C5 filled (run in the PC harness only).
9. Touch: tap rows 1 and 5 of the summary; tap the histogram to go back. Finger lifts cleanly after the form's OK (no soft key or row read by mistake).
10. Quit, run again, quit at once: "DataLoad: nothing loaded".
11. Large data: a 2,000-row matrix (the page will make one from any CSV). Time Columns and Scores by group on a G1: both build lists with `CONCAT` one value at a time.
