# DataLoad beta 1i: changes (27 November 2026)

Round 20 of 27 November 2026: blank cells inside paired columns. *Roger D. Metcalf, DDS, JD, DFSc, 2026. Written with AI assistance: the questions, the direction and the decisions are the author's; the reading of the sources, the drafting and the checking were done with Claude Opus 5.5 (Anthropic) in November 2026.*

## Why

On 27 November 2026, while the book's Draft 119 was being checked against a reviewer's question, we found that DataLoad beta 1h leaves the blank cells out of each column separately (`dd_Column`). That is exactly right when the columns are separate groups of different sizes, because each group then keeps all of its own values. But when each row is one person or one case, as in paired data (a before and an after for each person, the *x* and the *y* of a scatterplot, or the scores of several raters), one blank cell in the middle of a column made the rest of that column slide up by one row, and from there on the lists no longer matched row for row, without a word to the student. The book's Draft 119 warned about it (Appendix B, "A caution about blank cells in paired data") and told the student to delete such rows before pasting; Roger asked us to go on and fix it ("continue on please", 27 Nov 2026, 13:03).

## What changed (`verify/round20/make_round20.py`, exact replacements from beta 1h)

1. **The question** (lines 712 to 769, `dd_LoadCols`). Before it loads two or more columns, DataLoad looks for a blank cell that stands ABOVE a value in any of them (a blank at the foot of a column is the Data Loader page's padding for a shorter column, and asks nothing, as before). When it finds one, it asks, in a CHOOSE box whose title names the column ("Column 2 has a blank inside", or "2 columns have blanks inside"):
   1. **Pairs: keep complete rows**: only the rows with a value in every column that is loaded are kept, in every list, so each pair stays a pair and the lists match row for row;
   2. **Separate groups: drop blanks**: beta 1h's way, each blank left out of its own column;
   3. **Cancel** (or Esc): nothing is loaded and nothing is changed.

   This comes before the question about lists that already hold data. With Pairs, if no row is complete, a box says so ("Every row of M1 has a blank in at least one of its columns, so there is no complete row, and nothing was loaded.") and nothing is written. One column alone is never asked about, because it has no partner to match, and a blank only in a column past the ninth (which DataLoad does not load) asks nothing.
2. **Four new routines** (lines 424 to 504): `dd_Holes` (which columns have a blank above a value), `dd_Full` (the rows in which every loaded column holds a value), `dd_Pick` (a column at those rows only) and `dd_AskHoles` (the question). `dd_Column` and `dd_LoadGroups` are beta 1h's, word for word (Scores by group always kept only the rows in which both cells hold a value).
3. **The line DataLoad returns** after a Pairs load names the complete rows: "DataLoad: M1 → D1-D2 (10 rows, 8 complete)". After any other load it is beta 1h's line.
4. **Help is four pages** (`dd_Help`, lines 1,134 to 1,202). Page 3, "Blank cells", is new: what the Data Loader page writes for an empty cell, what a blank at the foot of a column does, and what DataLoad asks when a blank stands above a value, with what each answer does. Page 1's line on blanks now reads "Blank cells (9.99999999999E499) are left out: see page 3." Pages 2 and 4 are beta 1h's pages 2 and 3, word for word, but for their titles.
5. **The header** (lines 4 to 33 and 123 to 130): the version, the "beta 1i" note, the note on blank cells, and the credit in the house's long form.

## The Data Loader page, v7

The page said "N blank cells will be marked 9.99999999999E499; DataLoad leaves them out, so each list gets only its own values", which is no longer the whole story. When the paste has a blank above a value in any of its first 9 columns and there are two or more columns, the note under step 3 now names those columns and the two answers, and says that Scores by group always keeps only the rows in which both cells hold a value; the note that goes into the zip has a sixth step with the same answers. Nothing the page writes into the `.hpmat` file has changed (`data-loader/README.md`, "What has been tested").

## For the book (Draft 122)

- The programs table in How to use this book: DataLoad **beta 1i**.
- Appendix B, "A caution about blank cells in paired data": DataLoad now asks, so the paragraph can say what to answer instead of asking the student to delete rows by hand: "Pairs: keep complete rows" for paired data, "Separate groups: drop blanks" for separate groups.
- Chapter 1's sentence ("leaves out the blank cells of each column") can add that DataLoad asks first when a blank sits in the middle of the columns.
- No menu item moved: DataLoad's main menu is beta 1h's, item for item.

## Checks

- `verify/verify_DataLoad_beta1i.py`: **37 PASS, 0 FAIL** (its output is beside it). N: who is asked and who is not; the title and items, and that every title it can have is 31 characters or fewer and every item 30 or fewer; Pairs, Separate groups, Cancel and Esc; the Rossi data with six blanks punched in (426 rows back, each a whole row of the original, in file order); no complete row; the C lists; lists that hold data, cleared and kept; the longest line the program can return, laid out as the Program Catalog's box shows it. P: the four help pages, page 3's words, pages 1, 2 and 4 word for word beta 1h's but for the titles and page 1's line. S: beta 1h's routines word for word but `dd_LoadCols` and `dd_Help`; tags, LOCAL sizes, CHOOSE set to 0 first, no `!=`, ASCII code. R: the beta 1b script on beta 1i, every check passing but G6 (it reads beta 1h's three help titles) and L1 (it reads its own file name's layout records). L: no new firm overlap, straddle or overrun, and every new help line fits by the Virtual Calculator's measured glyph widths (281 px at the widest, of 320).
- `tools/ppl_gate_v1e.py` against beta 1h (`verify/round20/gates/gate_DataLoad_beta1i.txt`): **PASS**. Kit lint 0 errors; no hard error; the PARSE FAIL at the file-level LOCAL after EXPORT is the kit's limit, as for beta 1h; `fleet_names_v2.py` over the 31 newest files: 0 collisions, 0 untagged.
- `tools/screen_text_v1.py`: no place against the rules.
- The monkey test (`tools/monkey_chunks_v1.py`, base 1, `--lists --writes D,C`): **1,000 of 1,000 runs OK**. And the round's own monkey (`verify/round20/monkey_r20.py`), the same runs with an M1 that always has blank cells (pairs with blanks in the middle, 12 columns, no complete row, blanks only at the foot, one column, a single row): **1,000 of 1,000 OK**, and the question was put in 146 of them (`verify/round20/monkey_r20.txt`).
- **HP Prime Virtual Calculator 2.4.2** (build 2026-09-09), in the cloud workspace, 27 Nov 2026 (`verify/round20/vc_record.txt`, captures in `verify/round20/vc/`): Program Catalog > Edit > Check: "No errors in the program". Then, with Student's sleep data and two cells blank, made by the Data Loader's own core (`verify/round20/make_sleep_holes.js`): Columns put the question "2 columns have blanks inside" with its three items, every word in sight; Pairs gave D1 and D2 of 8 values each, the 8 complete patients, row for row, as the Statistics 1Var Numeric view showed; the box read "DataLoad: M1 → D1-D2 (10 rows, 8 complete)". Separate groups then gave 9 and 9, after "D1, D2 hold data", "Replace D1-D2"; Cancel at the question went back to the menu and left the lists as they were. The four help pages were drawn, every line inside the screen.

## Device checklist (G1 or G2: not yet run)

- [ ] Run DataLoad on Student's sleep data with two blanks (`verify/round20/make_sleep_holes.js` writes the file): Columns, Pairs: D1 and D2 hold 8 values each, the same 8 patients.
- [ ] Separate groups: 9 and 9. Cancel and Esc at the question: nothing changes.
- [ ] Help page 3: every line inside the screen.
- [ ] A matrix of 1,000 or more rows with blanks: how long the question takes to come, on a G1 (DataLoad reads every cell once more to look for blanks).

## Unresolved

- Nothing known. How long the extra reading takes on a G1 with a large matrix is not measured.
