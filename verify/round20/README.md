# Round 20: blank cells inside paired columns (27 November 2026)

DataLoad beta 1i, the Data Loader page v7, starter pack v28 and the Prime Loader v2r. Roger, 27 Nov 2026, 13:03: "continue on please" (the next job after the book's Draft 121), and 13:43, to the plan and its cost: "Good—go!".

## What was wrong

On 27 November 2026, while the book's Draft 119 was being checked against a reviewer's question, we found that DataLoad beta 1h leaves the blank cells out of each column separately (`dd_Column`). That is right for separate groups of unequal size, and wrong for paired columns (a before and an after for each person, the *x* and the *y* of a scatterplot, the scores of several raters): one blank in the middle of a column made the rest of that column slide up a row, so the lists no longer matched row for row, and nothing said so.

## What changed

- **DataLoad beta 1i** (`make_round20.py`, exact replacements from beta 1h; `../../docs/changes/DataLoad_beta1i_CHANGES.md` has the line numbers). When it loads two or more columns and a blank cell stands above a value in any of them, it asks, in a box titled "Column 2 has a blank inside" (or "2 columns have blanks inside"): **Pairs: keep complete rows** (only the rows with a value in every loaded column, in every list), **Separate groups: drop blanks** (beta 1h's way) or **Cancel**. Blanks only at the foot of a column, one column alone, and a blank only past the ninth column ask nothing. A Pairs load returns "DataLoad: M1 -> D1-D2 (10 rows, 8 complete)". Help is four pages; page 3, "Blank cells", says all this.
- **The Data Loader page v7** (`../../data-loader/README.md`): the note under step 3 names the columns that have a blank above a value and the two answers, and the zip's note has a sixth step with them. Nothing it writes into the `.hpmat` file changed.
- **Starter pack v28** (`../../docs/changes/StarterPack_v28_NOTES.md`): v27 but for DataLoad's checked file and two lines of READ_ME_FIRST.txt.
- **The Prime Loader v2r** (`../../prime-loader/README.md`): v2q's page, word for word, built from pack v28, with the Data Loader's v7 link; its test and the cable core's test count the new characters and reports (DataLoad is 6,561 characters longer).

## The files here

| File | What it is |
| --- | --- |
| `make_round20.py` | Builds `programs/DataLoad_beta1i.txt` from beta 1h by exact replacements. |
| `make_v2r.py` | Makes the Prime Loader's v2r build, template and test from v2q's by exact replacements. |
| `make_sleep_holes.js` | Writes M1.hpmat of Student's sleep data with two blank cells, by the Data Loader's own core, for the Virtual Calculator run. |
| `monkey_r20.py`, `monkey_r20.txt` | The monkey's runs with an M1 that always has blank cells: 1,000 OK, and the question put in 146 of them. |
| `vc_r20.py`, `vc_record.txt`, `vc/` | The Virtual Calculator: the Check, then the run, step by step, and its captures. |
| `gates/` | The gate's output against beta 1h. |
| `pages_a11y_r20_output.txt` | `tools/pages_a11y_v1.js` on the two pages (the Data Loader's v7): 32 PASS, 0 FAIL. |

## What passed

- `../verify_DataLoad_beta1i.py`: 37 PASS, 0 FAIL. The gate: PASS (kit lint 0 errors, no hard error, the fleet's names clean). `tools/screen_text_v1.py`: nothing against the rules.
- The monkey: 1,000 of 1,000 OK (`../monkey_DataLoad_beta1i_output.txt`), and this round's monkey with blanks always in M1, 1,000 of 1,000 OK.
- `data-loader/tests/test_core_v2.js` 34 PASS; `data-loader/tests/page_check_v7.js` 44 PASS; `tools/pages_a11y_v1.js` 32 PASS; `prime-loader/usb/tests/test_usb_core_v3d.js` 95 PASS; `prime-loader/tests/test_loader_v2r.js` 173 PASS, 0 FAIL.
- The Virtual Calculator 2.4.2 in the cloud workspace: the Check ("No errors in the program"); the question on the calculator's own screen, every word in sight; Pairs giving the 8 complete patients in D1 and D2, row for row; Separate groups 9 and 9; Cancel leaving the lists alone; the four help pages inside the screen (`vc_record.txt`).

Not run: a G1 or a G2 (the change note's device checklist).
