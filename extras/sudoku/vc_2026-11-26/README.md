# Sudoku beta 2a on the Virtual Calculator, 26 November 2026

The first run of Sudoku on a calculator: HP's Virtual Calculator 2.4.2 (build 2026-09-09), 64-bit, under Wine in a cloud workspace (`tools/vc_cloud_v1/`), driven with `tools/vc_cloud_v1/vcdrive.py`. The times are the calculator's clock (UTC−6). The captures are the calculator's 320 × 240 screen, three times enlarged except for the first two.

| Step | What was done | What the calculator showed | Capture |
|---|---|---|---|
| Check | The unchecked `Sudoku.hpprgm` of starter pack v26's first pass was copied into the calculator's folder; Program Catalog, Edit, Check (`tools/vc_cloud_v1/check_all.py Sudoku`) | "No errors in the program" (09:48, 2 s; `check_log_line.txt`). The calculator was left by Calculator > Exit, and the file it wrote back (244,804 bytes: the source and its compiled block of 48,948 bytes) is the checked file in the pack. | `00_check.png` |
| Start | The calculator started again; Sudoku was run from the Program Catalog | The first menu, all eight items in sight, the last "My games (none yet)" | `01_first_menu.png` |
| A new Easy puzzle | Item 1 | The board, the pad with the count of each digit still to place, Erase and Notes, the soft keys New, Notes, Hint, Undo, Check and More; the clock at 0:00 | `02_easy_board.png` |
| Hint | Soft key 3 | "Hint: only a 4 fits the green square, because its row, column and box hold the other 8 digits. Press Hint again to fill it in." The 4 is right: the square's column already holds 1, 2, 3, 5, 6, 7, 8 and 9. | `03_hint.png` |
| Hint again | Soft key 3 | The 4 filled in | `04_hint_filled.png` |
| Esc, Continue | Esc, then item 1 | The first menu offered "Continue (Easy, 0:21)", and the game went on where it was | |
| Finished with Hint | 84 more presses of Hint | "Solved! Your time: 2:34. Hints 43, Checks 0. Kept as game 1 of My games." | `07_finished.png` |
| My games | A key, Esc, then item 8, "My games (1 so far)" | One green dot at 38 clues and 2.6 minutes, the axes, "n = 1; the line and r need 3 games", the counts by level and the median, 2.6 | `08_my_games_1.png` |
| 2Var | Soft key 1 | "Sent to Statistics 2Var. 1 game is now in C1 to C5." and the sentences on which column holds what | `09_2var.png` |
| Leave | A key, Back, Esc | The Program Catalog's box with the line Sudoku returned: "Sudoku: solved in 2:34, game 1 of My games. The answer is in SU_SOLVED." | `10_after_exit.png` |

The calculator was then left by Calculator > Exit (its own Sudoku file now holds this run's values, so it is not the checked file).

**Not done here, and still open** (the device checklist of `Sudoku_beta2a_CHANGES.md`): the clock's pauses timed against a watch (item 3); the calculator turned off in the middle of a game (item 4); the level colors on a G1 (item 5); 2Var on a *Statistics 2Var* app that has never been opened (item 6; whether this calculator's app had been opened before is not known); the dots and *r* in the app itself (item 7); Clear and Help on My games (item 8); and everything on a G1 and a G2.
