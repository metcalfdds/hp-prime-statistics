# Sudoku, the bonus

**Sudoku beta 2a** (26 November 2026) is a Sudoku puzzle game for the HP Prime, written new by Roger Metcalf with Claude (Anthropic). It is a bonus, just for fun, and not one of the 31 *Statisticles*: the book tells about it, and about the statistics hiding in a Sudoku, in Appendix G, "Just for fun: Sudoku, and the statistics hiding in it", and Appendix F tells how the program works inside.

It keeps 24 puzzles, six for each of four levels, and shows each one in a new disguise every time (the digits renamed at random, the rows and columns shuffled within their bands and stacks, and half the time the grid turned over on its diagonal), so that no two games look alike. It has Hint, Check, Undo, pencil marks, Watch (the solver at work, step by step) and Solve, takes a puzzle typed in from a newspaper or from matrix M9, and keeps every puzzle that you finish yourself in **My games**, with its level, its number of clues, your time in minutes and how many times you used Hint and Check, for a class experiment on whether fewer clues take longer. My games plots your minutes against the clues, and its **2Var** key copies your games into the *Statistics 2Var* app (C1 to C5).

## Getting it onto a calculator

- **The Prime Loader** (`prime-loader/`, from v2p): under **More choices**, tick the box **Add Sudoku, just for fun**, and it goes onto the calculator with whatever else you choose; the page never takes it off a calculator.
- **The Virtual Calculator, by hand**: the starter pack (`starter-pack/`, from v26) holds it in its folder `Bonus (optional)`, checked on the Virtual Calculator; copy `Sudoku.hpprgm` into the calculator's folder with the rest.
- **HP's Connectivity Kit**: drag `Sudoku.hpprgm` from the starter pack onto the calculator's name, or paste `Sudoku_beta2a.txt` into a new program named Sudoku and Check it.

Then run it from the Program Catalog (Shift, then Program), or type `Sudoku` in Home and press Enter.

## How it was tested

- **In the PC harness** (`tools/ppl_run_v3e.py`): `verify_Sudoku_beta2a.py`, 161 checks, 161 passed (`verify_Sudoku_beta2a_output.txt`); 1,000 runs of random keys, taps and drags, all OK, then 300 runs started on the My games page with 13 games on it, all OK (`monkey_Sudoku_beta2a_output.txt`; the test-only copy that starts there is `test/Sudoku_beta2a_mygamestest.txt`, which is never sent to a calculator); the gate (`gate_output.txt`).
- **On the Virtual Calculator**, 26 November 2026: Check, a new Easy puzzle, Hint, a game finished and kept in My games, the My games plot, and the copy into *Statistics 2Var* (`vc_2026-11-26/README.md`, with the captures).
- **Not yet on a G1 or a G2.** The device checklist that is still open is in `Sudoku_beta2a_CHANGES.md` and in `vc_2026-11-26/README.md`.

## The files

| File | What it is |
|---|---|
| `Sudoku_beta2a.txt` | The program (1,961 lines of PPL) |
| `Sudoku_beta2a_CHANGES.md` | What beta 2a changed (My games, and the clock), with the line numbers, the checks and the device checklist; `Sudoku_beta2_CHANGES.md` and `Sudoku_beta1_CHANGES.md` are the versions before |
| `verify_Sudoku_beta2a.py` and its output | The verify script and what it printed; it looks for this repository's `tools/` beside it or one folder up, and needs `HPKIT` for the gate |
| `monkey_Sudoku_beta2a_output.txt`, `gate_output.txt` | Random use, and the gate |
| `build/` | How the program is made: `make_beta2a_template.py` makes the template from beta 2's by exact replacements, `Sudoku_beta2a_build.py` writes every table into it (the 27 rows, columns and boxes, each square's 20 neighbors, the 24 puzzles and their answers, the pencil-mark strokes and the help pages) and makes the program, and `su_gen.py` (with `su_engine.py`, a line-for-line copy of the program's solver) made the 24 puzzles of `base_puzzles.json` |
| `test/` | The test-only copy described above |
| `vc_2026-11-26/` | The run on the Virtual Calculator |

## Credits

Written new; none of anyone else's code is in it. The ideas came from three Sudoku programs in the hpcalc.org library, which carries their threads from the HP Forums: Lennart Börjeson's Sudoku editor/solver (2015: a square chosen by a tap, a menu strip, an undo list, the digits a square can still take; [thread 2537](https://www.hpmuseum.org/forum/thread-2537.html)), chromos's "Another sudoku solver" (2024: the two simplest steps, the naked single and the hidden single, and counting how many squares each one filled; [thread 22883](https://www.hpmuseum.org/forum/thread-22883.html)), and HPleak's "Sudoku solving program written in Python" (2023: the search drawn on the screen while it runs; [thread 20335](https://www.hpmuseum.org/forum/thread-20335.html)).
