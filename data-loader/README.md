# HP Prime Data Loader

Typing a long data set into a calculator is not feasible. This page turns columns from a spreadsheet into the calculator's own matrix file, and the program **DataLoad** (`programs/DataLoad_beta1b.txt`, in the starter pack) puts them into the Statistics lists the other programs read.

## Using it

1. **Open the page.** Download `DataLoader_v3.html` (on GitHub: open the file, then "Download raw file") and open it in any current browser. It is one self-contained file: it works offline, and nothing you paste leaves your computer.
2. **Paste** columns from Excel, SPSS or a CSV file (or open the file). One variable per column, one case per row; a first row of names is recognized. Empty cells, `NA` and `.` become blanks.
3. **Check the columns.** Each shows whether it is numbers or text, how many values and blanks, and its range. Text columns (*male*/*female*) become codes 1, 2, 3 … in alphabetical order; the page shows which is which, so write the codes down.
4. **Download M1.hpmat** (or choose M0–M9).
5. **Virtual Calculator:** close it (Calculator menu, Exit), copy the file into `Documents\HP Prime\Calculators\Prime`, start it, open the Statistics 1Var app once, and run **DataLoad**: *Columns* (column 1 to D1, column 2 to D2 …) or *Scores by group* (each group's scores to its own list, the smallest code to D1). If DataLoad says lists after the new ones hold data from before, choose *clear*: AnovaLab, RankLab and AgreeLab read every list that holds data.
6. **G1 or G2:** drag the file onto the calculator in the Connectivity Kit, or paste the columns into M1 in the Kit's matrix editor. *Not yet tested.*

`examples/M1.hpmat` is the Rossi data ready to copy (the starter pack carries the same file under `Sample data (optional)`). Try *Scores by group*, scores in column 1, groups in column 3, then TTestLab with "Raw scores in D1 and D2": t(421.19) = −1.68, p = 0.094.

## What has been tested (31 October 2026)

On the Virtual Calculator 2.4.2 (build 2026-09-09): the page's Rossi file (432 × 5) loaded whole; DataLoad filled D1–D5 and the two financial-aid groups; its summaries matched Python; TTestLab read the loaded lists and matched SciPy; a 10 × 3 file with text codes, an `NA` and a short column loaded as it should. Records: `docs/changes/DataLoad_beta1_NOTES.md`, `DataLoad_beta1a_CHANGES.md`, `DataLoad_beta1b_CHANGES.md`.

## Files

| File | What it is |
|---|---|
| `DataLoader_v3.html` | The page, built; open this one. |
| `page_template_v3.html` | The page's source, with two slots for the encoder and the example. |
| `dl_core_v1.js` | The encoder: reads the table, describes each column, writes the `.hpmat` and the zip. Plain JavaScript, no libraries; also runs under Node for the tests. |
| `build_page_v3.py` | Puts the template, the encoder and `examples/rossi.csv` together into `DataLoader_v3.html`. |
| `examples/rossi.csv` | The example: Rossi, Berk & Lenihan (1980), *Money, Work, and Crime*, via the R package carData; 432 men released from Maryland state prisons, followed 52 weeks. As SurvLab carries it. |
| `examples/M1.hpmat` | That example as matrix M1, the file that ran on the Virtual Calculator. |
| `tests/gen_cases_v1.py`, `tests/cases_v1.json` | 20,014 numbers as text with hp-prime-kit's encoding of each. |
| `tests/test_core_v1.js` | The page's encoder against the kit's: 20,011 compared, 0 differ (the other 3 are beyond a double: 1E499, 9.99999999999E499, 1E-499); the Rossi file byte for byte; blanks, text codes, rounding at the 13th digit. `node tests/test_core_v1.js` |
| `tests/page_check_v3.js` | Opens the page in Chromium (Playwright), downloads M1.hpmat and compares it with `examples/M1.hpmat`; pastes a text-coded table. `node tests/page_check_v3.js` |
| `tests/make_m2_v1.js` | Rebuilds the 10 × 3 test matrix used on the calculator. |

## The format

`.hpmat` as hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)) documents it: a 16-byte header (`01 00`, type `14 80`, rank 2, rows, columns, little-endian) and one 8-byte number per cell, row by row: twelve BCD digits, a 12-bit exponent and a sign. The page reads each number from its digits and rounds half up at the 13th, so what reaches the calculator is the number as typed, to 12 digits. Blank cells are written as 9.99999999999E499, the Prime's largest real; DataLoad leaves out anything at 1E499 or above.

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). A teaching aid: not validated for forensic, clinical or legal use.*
