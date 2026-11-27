# HP Prime Data Loader

Typing a long data set into a calculator is not feasible. This page turns columns from a spreadsheet into the calculator's own matrix file, and the program **DataLoad** (`programs/DataLoad_beta1i.txt`, in the starter pack) puts them into the Statistics lists the other programs read.

## Using it

1. **Open the page.** On the web it is <https://metcalfdds.github.io/hp-prime-statistics/data-loader/>. Or download `DataLoader_v7.html` (on GitHub: open the file, then "Download raw file") and open it in any current browser. It is one self-contained file: it works offline, and nothing you paste leaves your computer.
2. **Paste** columns from Excel or SPSS (or open a CSV or text file). The box starts empty. One variable per column, one case per row; a first row of names is recognized. Empty cells, `NA` and `.` become blanks.
3. **Check the columns.** Each shows whether it is numbers or text, how many values and blanks, and its range. Text columns (*male*/*female*) become codes 1, 2, 3 … in alphabetical order; the page shows which is which, so write the codes down. Anything the page did to the paste that you did not ask for is said in a line beginning "Check:". If the names or the columns came out wrong, the two controls under the table say whether the first row holds names and what separates the columns.
4. **Download M1.hpmat** (or choose M0–M9).
5. **Virtual Calculator:** follow step 4's link to the [Prime Loader](../prime-loader/README.md), which opens ready for a data file; in its step 2 click "Add a data file you were given", choose the file, close the calculator and click Load. The Loader checks the file, puts it in `Documents\HP Prime\Calculators\Prime` and puts DataLoad beside it; the programs on the calculator stay. Then start the calculator, open the Statistics 1Var app once, and run **DataLoad**: *Columns* (column 1 to D1, column 2 to D2 …) or *Scores by group* (each group's scores to its own list, the smallest code to D1). If DataLoad says lists after the new ones hold data from before, choose *clear*. (The file can also be copied into that folder by hand, with the calculator closed; the page says how.)
6. **G1 or G2:** drag the file onto the calculator in the Connectivity Kit, or paste the columns into M1 in the Kit's matrix editor. *Not yet tested.*

`examples/M1.hpmat` is the Rossi data ready to load (the starter pack carries the same file under `Sample data (optional)`). Try *Scores by group*, scores in column 1, groups in column 3, then TTestLab with "Raw scores in D1 and D2": t(421.19) = −1.68, p = 0.094.

## The review of 17 November 2026 (v4)

Roger asked for the students' helpers to be reviewed: "they must be bullet proof and as simple as possible". v3's tests passed, and each of them pasted a tidy table. Tried with what a student pastes, v3 did these things, and v4 does not:

| What a student does | v3 | v4 |
| --- | --- | --- |
| Clicks in the box and pastes | The box opened with the 432 example rows in it, so the paste went into the middle of them. | The box opens empty. "Try it with the example" fills it. |
| Has `NA` in a text column (male, female, NA) | NA became a third group with a code of its own, though the page said it became a blank. | A blank, in every kind of column. So are `N/A`, `#N/A`, `NaN`, `NULL`, `.`, `-` and `?`. |
| Has a typo in a number column (`1O`, the letter O) | A blank, without a word. | A blank, and a line names the cell: "1 cell is not a number and will be a blank: 1O". |
| Pastes `$45,000` or `45%` | The column was taken for text and coded 1, 2, 3. | Numbers, and a line says the sign was dropped (45% is read as 45, not 0.45). |
| Pastes one column of `45,000`-style numbers | Two columns, 45 and 0. | One column, and a line says how to make it two if that was meant. |
| Pastes one column of labels with spaces (*financial aid*, *no aid*) | Two columns. | One column. |
| Has *Male* and *male* in a column | Two codes. | One label, and a line says they are counted as one. |
| Has `1`, `2` and *control* in a group column | The 1s and 2s became blanks. | In a text column every cell is a label. |
| Writes decimals with a comma (`3,14`, from a European Excel) | Text, coded. | Numbers, and a line says the comma is read as a decimal comma. |
| Has names that are numbers (2019, 2020), or only text columns | The row of names was read as data (or the first label as a name), with no way to say otherwise. | A tick box: "The first row holds the column names". A table of labels only is also read better by rule. |
| Has a blank or a typo in the first row of data | The row of names could be missed. | The rule looks down the whole column. |
| Opens an .xlsx, .xls or .sav file | The box filled with rubbish. | Refused, with the way round it: copy the cells and paste them. |
| Opens a CSV saved in Windows-1252 or as "Unicode Text" | Accents were lost, or nothing was read. | Read (UTF-8, UTF-16 with its mark, else Windows-1252). |
| Copies the file into the calculator's folder by hand | The only route: a calculator left open, or a file the browser named `M1 (1).hpmat`, and nothing arrives. | Step 4 sends the student to the Prime Loader, which checks for both. The hand route is still there, with the name warning. |

The file written for a tidy table is v3's, byte for byte (the Rossi file is the test).

## What has been tested

**27 November 2026, v7: a blank cell above a value (round 20).** DataLoad beta 1i asks how the columns go together when it loads two or more columns and a blank cell stands above a value in any of them, because beta 1h left each blank out of its own column, and paired columns (a before and an after, an *x* and a *y*) then slid out of step after the blank. So the note under step 3 now says, when the paste has such a blank in any of the first 9 columns, which columns have it and what to answer: "Pairs: keep complete rows" when each row is one person or one case, so that each pair stays a pair, or "Separate groups: drop blanks" when the columns are separate groups; and the note that goes into the zip has a sixth step that says the same. A blank only at the foot of a column, one column alone, and a blank past the ninth column (which DataLoad does not take) keep v6's sentence, because DataLoad asks nothing then. Nothing the page computes or writes into the `.hpmat` file has changed (the core is still v2): `tests/test_core_v2.js` 34 PASS, 0 FAIL; `tests/page_check_v7.js` 44 PASS, 0 FAIL (v6's 37, and seven for the note, among them a student's slip, a cell left empty in the middle of a column); `tools/pages_a11y_v1.js` 32 PASS, 0 FAIL. What DataLoad beta 1i does with such a file was run in the PC harness (`verify/verify_DataLoad_beta1i.py`) and on the Virtual Calculator (`verify/round20/README.md`).

**21 November 2026, v6: accessibility only.** The page was checked against WCAG 2.1 AA with `tools/pages_a11y_v1.js` ([the record](../docs/dev/pages-accessibility-2026-11-21.md)). Three things changed, and nothing the page computes or writes: the orange and the green used for text are a shade deeper (contrast 5.5 to 1 on white, where v5's were 4.3 and 4.4 and WCAG asks 4.5); in a window 320 px wide the page no longer scrolls sideways (v5 was 379 px wide there, because its one column could not shrink and the menu "Columns are separated by" could not wrap); and the list of warnings is announced as a live region without a role that a list may not carry. On a desktop screen the page looks as it did, but for those two colors (old against new, pixel by pixel: 585 pixels differ, all of them colored text). `node tests/test_core_v2.js`: 34 PASS. `node tests/page_check_v6.js`: 37 PASS, v5's 32 and five new ones (320 px in three states, every text color on every surface, the live region). **Not done:** no screen reader has been run on the page, and v6 has not been loaded with DataLoad on a calculator; it writes the same bytes as v5, which the test compares with `examples/M1.hpmat`.

**17 November 2026, night, v5.** The Prime Loader's layout changed (its v2a: which calculator, which programs, one button), so step 4's two lines changed with it: the link now ends `?data=1`, which opens the Loader with no program chosen and a notice saying what to click, and the second line names the Loader's step 2. The same two lines changed in the note that goes into the zip. Nothing the page computes or writes changed: the core is still v2, and the file it makes is v4's byte for byte. `tests/test_core_v2.js`: 34 PASS, 0 FAIL; `tests/page_check_v5.js`: 32 PASS, 0 FAIL.

**17 November 2026, v4.** `tests/test_core_v2.js`: 34 PASS, 0 FAIL (the encoder against hp-prime-kit over 20,011 numbers, the Rossi file byte for byte, and each row of the table above). `tests/page_check_v4.js` (now v5): 32 PASS, 0 FAIL in Chromium, a real Ctrl+V among them. **On the Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 18:08 to 18:10:** the 5 × 3 file that v4 makes from `tests/vc_2026-11-17/paste.txt` (dollar signs and a thousands comma, *Male*/*male*/*Female* and an NA, an age typed `4O`) was put in the calculator's folder with DataLoad beta 1g from starter pack v23. DataLoad's title read "DataLoad: M1, 5 × 3"; *Columns* filled D1, D2 and D3 with n = 4 each; D1 showed min 45,000, max 61,250, mean 51,688 and s 7,081; D2 showed min 1, max 2, mean 1.5; D3 showed min 29, max 41, mean 35.5 and s 5.196. Those are the numbers of the paste with its three blanks left out (the captures are beside the paste). Not run on a G1 or a G2, and not yet opened in Edge on a Windows computer.

**31 October 2026, v1 to v3.** On the Virtual Calculator 2.4.2 (build 2026-09-09): the page's Rossi file (432 × 5) loaded whole; DataLoad filled D1–D5 and the two financial-aid groups; its summaries matched Python; TTestLab read the loaded lists and matched SciPy; a 10 × 3 file with text codes, an `NA` and a short column loaded as it should.

## Files

| File | What it is |
|---|---|
| `DataLoader_v7.html` | The page, built; open this one. |
| `index.html` | Written by the build: sends a browser on to the page, so the address `.../data-loader/` stays the same. |
| `page_template_v7.html` | The page's source, with slots for the encoder, the example and the Prime Loader's address. |
| `dl_core_v2.js` | The encoder: reads the table (v2: what a student's paste really looks like), describes each column, writes the `.hpmat` and the zip. Plain JavaScript, no libraries; also runs under Node for the tests. |
| `build_page_v7.py` | Puts the template, the encoder and `examples/rossi.csv` together into `DataLoader_v7.html`, and writes `index.html`. |
| `examples/rossi.csv` | The example: Rossi, Berk & Lenihan (1980), *Money, Work, and Crime*, via the R package carData; 432 men released from Maryland state prisons, followed 52 weeks. As SurvLab carries it. |
| `examples/M1.hpmat` | That example as matrix M1, the file that ran on the Virtual Calculator. |
| `tests/gen_cases_v1.py`, `tests/cases_v1.json` | 20,014 numbers as text with hp-prime-kit's encoding of each. |
| `tests/test_core_v2.js` | The page's encoder against the kit's: 20,011 compared, 0 differ (the other 3 are beyond a double: 1E499, 9.99999999999E499, 1E-499); the Rossi file byte for byte; rounding at the 13th digit; and 26 pastes a student makes. `node tests/test_core_v2.js` |
| `tests/page_check_v7.js` | Opens the page in Chromium (Playwright): the empty box, a real paste, the example downloaded and compared with `examples/M1.hpmat`, every "Check:" line, the two controls, files that are refused or read, and (v7) the note on a blank cell above a value. `node tests/page_check_v7.js` |
| `tests/make_m2_v2.js` | Rebuilds the 10 × 3 test matrix used on the calculator on 31 October. |
| `tests/vc_2026-11-17/` | The paste, the 5 × 3 file v4 made from it, and five captures of DataLoad reading it on the Virtual Calculator. |

## The format

`.hpmat` as hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)) documents it: a 16-byte header (`01 00`, type `14 80`, rank 2, rows, columns, little-endian) and one 8-byte number per cell, row by row: twelve BCD digits, a 12-bit exponent and a sign. The page reads each number from its digits and rounds half up at the 13th, so what reaches the calculator is the number as typed, to 12 digits. Blank cells are written as 9.99999999999E499, the Prime's largest real; DataLoad leaves out anything at 1E499 or above.

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). A teaching aid: not validated for forensic, clinical or legal use.*
