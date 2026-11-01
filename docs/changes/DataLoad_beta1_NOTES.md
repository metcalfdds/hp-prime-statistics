# DataLoad beta 1: notes and the first Virtual Calculator run (31 October 2026)

*beta 1 never reached `programs/`: the run below found five things to fix, and beta 1a and 1b (their own CHANGES files) are what went in. These notes keep the design and the first run. The general findings are in Lessons Learned v7zc.*

## Why

Roger: "Of course one issue here is entering long data sets on a calculator by hand is just not feasible—maybe we could make some sort of 'data loader' to copy a dataset and then put it in a format to paste to the Prime folder." Then, to the plan of a web page, a calculator program and both in the starter pack: "Of course!"

## The two halves

1. **The HP Prime Data Loader** (`data-loader/DataLoader_v2.html`, a single page that works offline). Paste columns from Excel, SPSS or a CSV file, or open the file; it reads them, shows each column (numbers or text, values, blanks, range or codes), and writes the calculator's own matrix file, `M1.hpmat` (or M0–M9). Text columns become codes 1, 2, 3 … in alphabetical order, and the page shows which is which. Blank cells (empty, `NA`, `.`) are written as 9.99999999999E499, the Prime's largest real.
2. **DataLoad** (this program). It puts a matrix's columns where the fleet reads data: the Statistics 1Var lists D1–D9, or the Statistics 2Var lists C1–C9. Two ways: **Columns** (column *j* to list *j*, at most 9) and **Scores by group** (a column of scores and one of group codes, the way SPSS keeps data; each group's scores to its own list, the smallest code to D1). Cells at 1E499 or above are left out, so each list gets only its own values. Then it shows every list that holds data, a box plot each, and a histogram of any list you tap.

## The probe first (DLTest, 31 Oct 2026, 18:53 CDT)

A 30-line program copied M1's first two columns into D1 and D2 with `MAKELIST` and returned their sizes and sums. With the Rossi data (432 × 5) in M1 as a file written by hp-prime-kit, it returned `{432, 5, 19809, 114, 432, 432}` on the Virtual Calculator 2.4.2, and the Statistics 1Var Numeric view showed the columns row for row. So a matrix arriving as a file reaches a program, and the program can fill the D lists.

## The file format

`.hpmat` as hp-prime-kit (MIT, JordiRigau/hp-prime-kit) documents it: a 16-byte header (`01 00`, the type word `14 80`, rank 2, rows, columns, little-endian) and then one 8-byte number per cell, row by row. A number is twelve BCD digits, a 12-bit two's-complement exponent and a sign nibble. The calculator's own files carry the type word `14 9B`; it accepted `14 80`, and when it rewrote M1 on exit it kept `14 80` and every cell. The page's encoder reads digits from the text and rounds half up at the 13th; over 20,014 test numbers it matched the kit's encoder on all 20,011 a double can carry, and the Rossi file it writes is byte for byte the kit's (`data-loader/tests/`).

## Checks before the calculator

- Gate `ppl_gate_v1c.py`: PASS (kit lint 0 errors; no hard errors; the parse stops at the first file-level `LOCAL`, the kit tool's known limit).
- `verify_DataLoad_beta1.py`: 44 PASS, 0 FAIL (the summary numbers against Python with the Prime's quartile rule over 2,000 lists; both loads on the Rossi data value for value; blanks; replacing; the matrix menu; the pages; layout).

## The run on the Virtual Calculator (31 Oct 2026, 19:36–19:45 CDT)

Virtual Calculator 2.4.2 (build 2026-09-09), calculator `Prime`, Rogers-HP; by Claude through computer use. M1 = the page's Rossi file (432 × 5); M2 = a 10 × 3 test matrix made by the page from text: months, sex (female/male, so codes 1/2), prior, with one `NA` and a third column of 5 values.

1. Catalog → DataLoad → Edit → Check: "No errors in the program". `DATALOAD` in Home opened the menu, titled "DataLoad: M1, 432 × 5".
2. **Columns** (D1, D2 held the probe's data): the question "D1-D5 already hold data", Replace. The summary: D1–D5, "column 1" … "column 5", n 432 each, a box plot each (weeks bunched at 52, arrest and aid 0/1, age and priors skewed right).
3. **Tap D4** (age): the histogram, bins of 2 from 16 to 46; n 432, x̄ 24.6, s 6.113; min 17, Q1 20, med 23, Q3 27, max 44. Python: 24.597, 6.1134, 17, 20, 23, 27, 44.
4. **Scores by group**, scores column 1, groups column 3: D1 "col 3 = 0" n 216, D2 "col 3 = 1" n 216. D1's histogram: x̄ 44.83, s 13.52, min 1, Q1 44, med 52, Q3 52, max 52 (Python 44.833, 13.518, 1, 44, 52, 52, 52).
5. **M2, Columns**: D1 n 9 (the `NA` left out), D2 n 10 (codes 1 and 2), D3 n 5 (the ragged column), the box plots where the numbers put them.
6. **M2, Scores by group** (1 by 2): D1 "col 2 = 1" n 4 (the women's sentences without the `NA`), D2 "col 2 = 2" n 5.
7. **M1 again**, 1 by 3, then Quit: Home showed "DataLoad: M1 col 1 by col 3 → D1-D2".
8. **TTestLab read the loaded lists:** Choose the test → independent, variances not equal → "Raw scores in D1 and D2" → two-tailed, α .05. Step 1 showed D1 x̄₁ = 44.83333, s₁ = 13.51829, N₁ = 216 and D2 x̄₂ = 46.875, s₂ = 11.68653, N₂ = 216; step 4, SE 1.216 and t = −1.68; Home, "TTestLab: t(421.19) = −1.68, p = 0.094, two-tailed". SciPy's Welch test on the same weeks: t = −1.6792, df 421.195, p = 0.0939.
9. Help: three pages, all lines inside the screen.

## What the run found (fixed in beta 1a)

1. **Lists left from an earlier load.** After step 4, D3–D5 still held Rossi's columns 3–5, labelled "column 3" … "column 5". After step 5, D4 and D5 still held Rossi's columns and read "column 4", "column 5" under M2's columns, as if M2 had five. AnovaLab (one-way), RankLab (groups) and AgreeLab (raters) read **every** D list that holds data, so a two-group load followed by AnovaLab would have analysed five groups.
2. The question said "D1-D5 already hold data" when only D1 and D2 did.
3. A column that is blank throughout left its list as it was (old values, no label).
4. The Scores-by-group form cut its labels: "Scores in colu…", "Groups in col…". Its help said "analyse".
5. Help page 3 left out RankLab's groups.

## Driving the Virtual Calculator (not DataLoad's)

PC-keyboard Enter presses and quick taps on a menu item were sometimes missed: a tap highlighted the item without choosing it, and an Enter from the PC keyboard did nothing on the summary page. The calculator's own Enter key, clicked with a 0.3-s press, always worked. Lessons Learned §16 already records the same for other programs.
