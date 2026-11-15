# TTestLabG beta 1h: changes (14 November 2026, night)

Round 14, part 2. The general version of TTestLab, built from **TTestLab beta 1k** by `tools/make_tlg1_v3.py` (exact replacements; a block that does not find its lines exactly once stops the build). What beta 1k adds is in `TTestLab_beta1k_CHANGES.md`; this note says what is particular to the general version, and how it is built now.

## Why

TTestLab beta 1k gained the one-sample *t*-test, the one-proportion *z*-test and the two-proportion *z*-test, for the book's Chapters 9 and 11 (Roger, 14 November 2026: "go ahead and do the program work"). The general version is the one the book's chapters use, so it gets the same three tests the same day, by the rule for general versions: the advanced program changes first, then the script builds the general one.

## What changed

| What | Where (line numbers in `TTestLabG_beta1h.txt`) |
| --- | --- |
| The three new tests, their arithmetic, pages, forms and help page 3: TTestLab beta 1k's code with `tz` for `tt` | `tz_SL` 478 to `tz_DS` 526; `tz_One` 623, `tz_Whole` 636, `tz_CalcN` 648; `tz_VN` 1146 to `tz_Step5N` 1367; `tz_Fam` 1621, `tz_Pick` 1631; `tz_AskDataN` 1706; help 1989 |
| The new examples are 5 to 7 here (this version has four older ones): Student's sleep data, the grand juries of *Castaneda v. Partida*, the Rossi experiment | `tz_Example`, 1899 |
| The start menu: "Choose the test", the four older examples, "Examples: one sample, z-tests" (item 6: the list of the three new ones) and Help: seven items, all on the screen | 2146 |
| Step 3 of the one-sample *t* is this version's own: the exact t critical first, the printed table as a note | `tz_Step3` (unchanged) |
| Step 5 of the new tests has no printed-table note: a *p* that rounds to α shows its four digits, as this version's older tests do | `tz_Step5N`, 1367 |

The older tests' pages, forms and numbers are beta 1g's, but for one line of step 5 (a Cohen's *d* past 999.99 in size prints as "> 999.99": `tz_DS`, as in TTestLab): of beta 1g's 53 routines, 14 changed, the same ones as in TTestLab, and 19 are new.

**Why the start menu has a list inside it.** The first build put the three new examples straight into the start menu: nine items here. On the Virtual Calculator the menu showed eight rows, and the ninth, Help, was cut off at the bottom of the screen (14 November 2026, 21:34). Both versions now keep the new examples in a list of their own, and both verify scripts check that no menu has more than eight items.

## How it is built: `tools/make_tlg1_v3.py`

`make_tlg1_v2.py` built beta 1a from TTestLab beta 1c. Rounds 5 to 12 then changed both programs in step, each by its round's own script, so v2's replacements no longer find their text. v3 starts again from the two current programs:

1. The code is TTestLab beta 1k's, from "shared state" on, renamed (`TTESTLABG`, `tz_`, `tz`).
2. `tools/tlg1_v3_blocks.txt` holds 53 blocks. Each gives the advanced version's lines (`-`), the general version's (`+`) and just enough unchanged lines to be found exactly once. The first 46 were made by a line diff of TTestLab beta 1j against TTestLabG beta 1g, and turn the one into the other exactly (checked when they were made). Four of them carry beta 1k's wording (the examples' count, two menus, Help's place). Seven are for beta 1k's new code: the new examples' numbers, the start menu's three lines, and step 5's note.
3. The header is the general version's own: beta 1g's, from git, with this version's block and three additions.

From here on a fix goes into TTestLab first, and this script's next version builds TTestLabG.

## Checks

- **Gate**: PASS. hp-prime-kit lint 0 errors; `lint_ppl` 4 problems, the same four as beta 1g; fleet names: 31 files, 2,410 routine names, 0 collisions.
- **`verify/verify_TTestLabG_beta1h.py`**: 63 checks, 0 failed (`verify/verify_TTestLabG_beta1h_output.txt`). The script is TTestLab's with the program's names changed (`verify/round14/make_verify_tlg_1h.py`: its files, entry point and tag, four older examples, no printed-table note). B compares 14 sessions of the older tests with beta 1g: the same screens, forms, boxes and results. The arithmetic, the book's numbers, the cancels and refusals, the help pages and the layout (313 distinct screens) are checked as for TTestLab.
- **Monkey test**: 1,000 of 1,000 runs OK (`verify/round14/mk/TTestLabG.jsonl`).
- **Label monkey** (`tools/monkey_labels_v1.py 300`): on the build before the last it found one firm overlap, "Cohen's d = −34,200,918,…" over "magenta area = p" (beta 1j has it too; `tz_DS` is the fix). On the final file: no number cut short and no firm overlap. It still lists 8 lines as running off the screen by its estimate of 6.5 px a character: seven help lines (six of them the version before's) and step 1's H₀ line. At the calculator's glyph widths all of them fit (checks H3 and D3), and the Virtual Calculator drew them whole.
- **Virtual Calculator 2.4.2** (build 2026-09-09, under Wine in the cloud workspace, 14 November 2026, 22:02): Check: "No errors in the program". The checked file went into starter pack v20 before any run. Then run from the catalog: the start menu (seven items, Help in sight), the list of new examples, the one-sample example's five steps, help page 3, and the result returned ("TTestLabG: t(9) = 4.06, p = 0.003, two-tailed"). Screens: `verify/round14/screens/TTestLabG_*.png`.

## On a G1 or a G2 (not yet run)

1. Program Catalog, TTestLabG, Edit, Check: "No errors in the program".
2. Run. The start menu shows seven items, Help the last, with no scrolling.
3. "Examples: one sample, z-tests", then Student's sleep: step 3 reads "t crit = ±2.262   (exact, for df = 9)"; step 5 reads "Report t(9) = 4.06, p = 0.003, two-tailed".
4. Then TTestLab beta 1k's list, items 4 to 11, with this program's name.

## Unresolved

- Not run on a G1 or a G2.
- The same four notes as TTestLab beta 1k's.
