# Sudoku beta 2a: changes, checks and device checklist

26 November 2026. Beta 2a is beta 2 with **My games**, a record of each puzzle that the player finishes, kept for the book's solving-time experiment, and with a clock that counts only the time the board is on the screen. Everything else is beta 2's, word for word (`Sudoku_beta2_CHANGES.md`, now in `_superseded`).

## Why

Roger, 26 Nov 2026, 6:29 a.m., on tying the Sudoku bonus to statistics: "Maybe say we could do an experiment to see how long it takes people so solve a puzzle compared to the number of initial clues…talk about how looking at just one or two people;s results might not give us a good idea about the population, compare a cross section with long term or other tests". Asked whether the program should record each finished puzzle so that students can run the experiment on their own data in the *Statistics 2Var* app, he chose "Yes, add the log (Recommended)", and for the book's bonus section a new Appendix G.

## What it does now

- **A finished game is kept.** When the player fills the last square of a puzzle, the game becomes one row of My games: its level (1 Easy, 2 Medium, 3 Hard, 4 Expert, 5 typed), its number of clues, the minutes on the clock (to two decimals), and how many times Hint and Check were used. The fireworks page says "Kept as game 7 of My games." A game that Solve or Watch finished is not kept, because then the program did the work. My games keeps up to 200 games; when it is full, the fireworks page says so, and Clear empties it.
- **My games, the page.** The last item of the first menu ("My games (none yet)", or "My games (12 so far)") and an item of the Enter menu open it. It plots minutes (up) against clues (across), one square dot for each game in its level's color (the colors of the board's level name), with light grid lines, ticks and numbers on both axes and the names of both axes. With at least three games and two different numbers of clues, it adds the least-squares line (gray, cut where it would leave the plot) and r. At the right are each level's color, its count of games, and its median minutes, because a few very slow games pull a mean up. With no games, the page says how a game gets there.
- **2Var** copies the games into the *Statistics 2Var* app: the clues to C1, the minutes to C2, the level to C3, the Hints to C4, the Checks to C5. When any of those columns already holds data, it asks first ("Replace C1 to C5?"). A page then says what went where, and how to see the plot and r in the app (Chapter 13 of the book: S1 reads C1 and C2 unless it has been changed; Num, then Stats, gives *r*). **Clear** empties My games after a question. **Help** opens the help at the page "My games". **Back** or Esc returns.
- **The clock** counts only the time the board is on the screen. Beta 2's clock went on running while a menu, a question or a help page was open; beta 2a's `suDrain`, which runs after every dialog and around every held page, starts the clock again from that moment. One wait counts for two minutes at most: `WAIT(-1)` gives up after about a minute, so a longer gap means the calculator was off.
- **Four help pages** are new: "My games", "The My games plot" (the median and *r* in plain words), "My games in Statistics 2Var", and "A class experiment" (Roger's points: one or two players tell us little about all players; our levels and their clues go together, so a slower time may come from harder logic rather than from fewer clues; practice makes everyone faster, so the order of the levels should be drawn at random).

## What changed, by line (in `Sudoku_beta2a.txt`)

The template is made from beta 2's by exact replacements (`make_beta2a_template.py`); the build (`Sudoku_beta2a_build.py`) wraps the new texts at the calculator's measured font-2 widths and counts the help page that the My games page opens.

| Line | What |
|---|---|
| 2, 18, 31-46 | Name, change-note file, and the "What changed" entry for beta 2a |
| 102-103 | `suGames0` and `suSent2V`, the texts of the page with no games and of the page after the copy, written by the build |
| 123 | `suGLv, suGCl, suGMn, suGHn, suGCk, suGNew`: My games, and the number of the game just kept |
| 199 | `suDrain` starts the clock again after a dialog or a held page |
| 1140-1152 | `suLogGame`: a finished game becomes one row |
| 1155-1180 | `suCelebrate` keeps the game and says where it went; the page is 12 pixels taller |
| 1353, 1379 | `suHelpFrom(page)`, and `suHelp()` as `suHelpFrom(1)` |
| 1425-1475 | `suNice` (round axis steps), `suTickTxt` (a tick's number, with commas), `suTxtW` (a number's width in font 1, from the measured widths), `suMedian` |
| 1478-1591 | `suGamesDraw`: the plot, the line and *r* from the deviations in a second pass, the counts and the medians; a clue number at the very corner is left out, because it would run into the minutes' 0 (found by `text_overlap_v1`) |
| 1598-1634 | `suTo2Var`: the copy into C1 to C5, its question, its refusal in a sentence, and its page |
| 1637-1645 | `suClearGames` |
| 1652-1684 | `suGames`: the page's loop, with the board's stale-click guard |
| 1765 | `suAction(18)`: My games |
| 1780 | The Enter menu gains "My games" |
| 1791-1801 | `suTick`: one wait counts for two minutes at most |
| 1930-1932 | The first menu's last item, "My games (...)" |
| 1958 | The line returned after a kept game: "Sudoku: solved in 12:34, game 7 of My games. The answer is in SU_SOLVED." |

**Menu items and help pages that moved, for the book's next draft.** The Enter menu: "My games" is item 12, so "Help" moves from 12 to 13 and "Exit Sudoku" from 13 to 14. The first menu: "My games" is added after "How to play (Help)", as item 8, or item 9 when a game is kept (the ninth item scrolls into view). The help pages: the four new pages are 8 to 11, and "Credits" moves from 8 to 12.

## Verification (26 Nov 2026, in a cloud session)

- **Gate** (`ppl_gate_v1e.py` against beta 2): PASS. hp-prime-kit lint 0 errors; ppl_check_v5 the same 3 E7 as beta 2 and no hard errors; lint_ppl the same 5 naming notes as beta 2 (the program's entry point is `Sudoku`, not its file name); full parse stops at `EXPORT` exactly as beta 2's does (the kit's limit); fleet names: 62 routine names, no collisions. `gate_output.txt`.
- **Verify script** (`verify_Sudoku_beta2a.py`, made from beta 2's, every one of its checks kept): 161 checks, 161 PASS, 0 FAIL. Part D16 is new: a finished game is kept with its level, clues, minutes, Hints and Checks, and the fireworks page says where; Hints and Checks are counted into the game; Solve and Watch keep nothing; a typed puzzle is level 5; My games full; the clock leaves out 30 seconds in each of two menus, and counts a ten-minute wait as two minutes; the page with 0, 1, 2, 3 (all times equal), 4 (all clues equal) and 13 games, where *r*, the line's two ends, all 13 dots and their colors, the counts and the medians are compared with Python's; 2Var with the columns empty, holding data (Yes, No, Cancel), and one game; Clear (Yes, No, Cancel); Help by soft key and by key; the stale-click guard on the page; My games from the first menu with and without a kept game, and from the Enter menu; the line returned. `verify_Sudoku_beta2a_output.txt`.
- **Random use** (`monkey_v1b.py`, 1,000 runs of 120 random keys, taps and drags; `--writes C`, because 2Var is meant to write C1 to C5): 1,000 of 1,000 runs OK, in 496 s. Then 300 directed runs (`monkey_directed_v1.py`), each started on the My games page with 13 games on it by a test-only copy of the program that adds one routine, `SuMyGamesTest()`, which fills My games and calls `suGames()` (the copy is not shipped): 300 of 300 OK, the page on the screen in all 300. And in 300 ordinary sessions (`monkey_reach_v1.py`), 108 reached My games, always with no games, because random keys never finish a puzzle. `monkey_Sudoku_beta2a_output.txt`.

## Device checklist (the Virtual Calculator first, then the G1 and the G2)

Beta 2's checklist (`Sudoku_beta2_CHANGES.md`) still stands; nothing of beta 2 has run on a calculator yet. These items are new.

1. **Check.** Paste into the program named Sudoku (replacing beta 2), then Program Catalog, Edit, Check: no message. Checking resets the file-level values, so My games starts empty.
2. **A kept game.** Finish an Easy puzzle (Hint again and again is the quick way): the fireworks page should say "Kept as game 1 of My games." Esc, Cancel: Home's line should end "game 1 of My games. The answer is in SU_SOLVED."
3. **The clock.** In a game, open the Enter menu and wait half a minute before Cancel: the clock at the top right should not have moved by half a minute. Then leave the board untouched for three minutes: the clock should move about three minutes.
4. **Off in the middle.** In a game, let the calculator turn itself off (or press Shift, then On), wait five minutes, and turn it on. Is Sudoku still running? If it is, the clock should have moved two minutes at most. If it is not, run it again and choose Continue.
5. **My games.** First menu, My games: are the dots, the gray line, the grid lines and the small numbers readable on the G1 and the G2? Are the five level colors easy to tell apart on the G1?
6. **2Var on a fresh app.** Reset the *Statistics 2Var* app (Apps, highlight it, Reset) or use a calculator where it has never been opened, then tap 2Var on My games. Lessons Learned §10 says the columns do not exist until the app has been opened once; the program then shows a sentence asking to open the app first. Which happens: the sentence, or a copy that works?
7. **2Var, then the app.** Tap 2Var (answer Yes if it asks), open *Statistics 2Var* from the Apps key: Symb should show S1 with C1 and C2; Plot should show the same dots as My games; Num, then Stats, should show the same *r* as My games.
8. **Clear, and Help.** Clear, then "No, keep them": nothing changes. Help on My games opens at the page "My games".

## Not yet known, or left for later

- **Nothing of beta 2 or beta 2a has run on a calculator.** Everything above is the PC harness and the Python copies.
- **Whether the copy works before *Statistics 2Var* has been opened** (checklist 6). Lessons Learned §10 says the columns do not exist until then, so the copy is wrapped in `IFERR`, and its refusal is a sentence; the harness cannot model the columns' absence.
- **What a running program does when the calculator turns off** (checklist 4), and so whether the two-minute limit on one wait is ever needed.
- **The first menu with a kept game has nine items**, so "My games" scrolls into view as the ninth. Beta 2's rule for the book (a new item goes after the old ones) put it last; moving it up would move "How to play (Help)".
