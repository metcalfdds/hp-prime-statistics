# Sudoku beta 1: changes, checks and device checklist

*25 November 2026. Program file: `Sudoku_beta1.txt`. Verify script: `verify/verify_Sudoku_beta1.py`.*

## What it is

A Sudoku solver for the HP Prime, written in PPL. The puzzle is typed into matrix M9 (0 for a blank square) or taken from a built-in sample. The program checks the clues, solves the puzzle, and draws the grid with the clues in black and the solver's digits in blue. It lists three counts beside the grid (clues, steps, and undos), leaves the answer in `SU_SOLVED`, and returns a one-line summary to Home.

The solver is a depth-first backtracking search. Before each move it looks for the tightest spot on the board: either the empty square with the fewest legal digits, or the row, column, or box whose missing digit fits in the fewest squares. When that spot has one choice, the move is forced and no guess is made. The idea, "most constrained first," is the one behind Knuth's Algorithm X. The program was written new and uses none of anyone else's code.

It began as `SUDOKU.txt`, written in a chat outside this Project on 25 Nov 2026. That copy is superseded and should not be used. It had LOCAL lines of up to nine names, single-letter names (k, n, u), no tag on its names, `FREEZE` used as a pause, numbers without commas, and no header.

## Changes from SUDOKU.txt (the house rules, from Lessons Learned v7zx)

- Header block with author, year, AI-assistance note, terms, the DISCLAIMER line, and the firmware it was tested on (none yet) (§13).
- Every name carries the tag `su` (`suCm`, `suDrain`, `suWaitAny`, and the `su…` locals), with no single-letter names (§5). The fleet tags were read from §15, and `su` is not among them. SampDist already uses `sd_`.
- At most 6 names on a LOCAL line (§2).
- The CHOOSE index is set to 0 before the call, and the program tests the index rather than CHOOSE's return value (§2).
- Commas in big numbers come from the program's own routine (`suCm`, built on `STRING(ROUND(n,0),2,0)`, `DIM`, `MID`, and `MOD`), since `STRING` never groups digits (§6). This copy handles counts only, which are never negative, and is not the fleet's `comma_helper_reference_v1.txt`. That file is on D: and could not be reached from this session.
- No raw number is joined into a message: every number goes through `suCm`, so Home's number format cannot change the text (lint check 9).
- The result screen is drawn in G1 and blitted to the screen once (§6). It is held with `suWaitAny`, which drains keys and a touch lift capped at 1 second, waits for a key or a touch, and drains again (§7). `FREEZE` is gone.
- The program ends with `RETURN` and a summary line of at most 72 characters (§7). The answer stays in the EXPORT matrix `SU_SOLVED` (§3: `MAKEMAT` and then element assignment into an exported matrix is confirmed).
- A touch drain follows every CHOOSE, MSGBOX, and EDITMAT, as PowerViz v2.5i does (§15).
- The header's claim about guesses is now a counted number, counted in the verify script (§14 rule 32).
- House colours: the solver's digits are house blue RGB(0,60,200), the labels gray RGB(90,90,90), and the footer dodger blue RGB(30,144,255) in the canonical form ("black = clue, blue = solved, any key = exit") (§13).

## Checks run (25 Nov 2026, in a cloud session; D:\HP-Prime was not reachable)

| Check | Result |
| --- | --- |
| hp-prime-kit `hpprime lint` (cloned from GitHub, not the Community_Library zip) | 0 errors; 10 warnings, all "TEXTOUT_P without its width argument" |
| `ppl_check_v5.py` (the Project copy) | 0 errors, 0 warnings, 4 functions |
| `lint_ppl.py` v3 (the Project copy) | 179 checks; the 5 problems are the gate's known noise (entry name versus file name, EXPORT names) |
| Full parse with the kit's interpreter | PARSE OK, 4 functions |
| `verify_Sudoku_beta1.py Sudoku_beta1.txt` | 16 of 16 pass |
| Solver section, token for token, against the version the Python copy first tested | identical; only display lines differ |

**Built-in names:** `HP_Prime_Builtin_Names.txt` is on D:, so for this session the checkers read a stand-in made from hp-prime-kit's `docs/commands/names.tsv` (1,173 names, CAS names included). Run the real gate on Rogers-HP before pasting: `python3 ppl_gate_v1e.py Sudoku_beta1.txt`, which includes `fleet_names_v2.py` over the whole fleet.

**Not run:** the fleet harness (`ppl_run_v3e.py`) and the monkey test (`monkey_v1b.py`). Both are on D:. The program's PPL has not run anywhere yet; what has run is a line-for-line Python copy of its logic.

**Verify script results:** the sample puzzle matches its published answer (30 clues, 51 steps, 0 undos). Royle's 17-clue puzzle and Norvig's anti-brute-force puzzle take 64 steps each with 0 undos. Easter Monster takes 3,823 steps with 3,763 undos, and Inkala's 2012 puzzle 2,080 steps with 2,020 undos. The empty grid gives a valid grid. Conflicting clues, 2.5, 10, and an unsolvable puzzle are each refused with a sentence. On 300 random puzzles (half solvable, half random clues that are often unsolvable) the copy agrees with an independent brute-force solver every time: 0 disagree, 0 skipped. The returned line is at most 72 characters, and the longest message about 95.

## Device checklist (Virtual Calculator first, then the G1 and the G2)

1. Paste into a new program named **Sudoku** in the Connectivity Kit, then use Program Catalog → Edit → **Check**. A clean compile shows no message.
2. Run **Sudoku** from Home. The menu should show the title "Sudoku Solver" and three items, unnumbered.
3. **Solve the sample puzzle.** "Solving..." should flash, and then the grid should appear. Check:
   - the digits sit in the middle of their squares (they are drawn at +9, +5 px in font 2, and may need a pixel nudge);
   - the heavy box lines are two pixels wide;
   - the left margin reads Clues 30, Steps 51, Undo 0;
   - the footer fits on one line.
4. A key, and then a tap, should each leave the result screen. Home should show "Sudoku: solved in 51 steps, 0 undos. Answer in SU_SOLVED." Typing `SU_SOLVED` in Home should show the solved matrix.
5. **Enter a new puzzle.** Read the message, then check that the matrix editor opens on a 9 × 9 grid of zeros. **Record how the editor is left (OK, Esc, or both)** and that the solver then starts. This is the first fleet use of `EDITMAT`; the community program ACDC.txt uses `EDITMAT(M1)` the same way.
6. **Edit the puzzle in M9.** The last puzzle should open in the editor. Try a resized M9 (add a row): the program should say "M9 must have 9 rows and 9 columns."
7. Refusals: a repeated clue ("The 5 at row 1, column 2 repeats an earlier clue…"), a 2.5, and a 10. Each should give its sentence and return to Home.
8. Fewer than 17 clues (an empty grid) should give the "Only 0 clues…" message, and then one valid grid.
9. **Timing on the G1 and the G2** (reset and unplug first, §14 rule 20): run Easter Monster (enter it from the verify script's list). The step counter should update every 250 steps with commas. Record the seconds taken. The PC copy needed 3,823 steps; the calculator's time for them is unknown.
10. A finger left on the screen when the menu closes must not skip the result screen.

## Open items

- Touch entry (tap a square, then tap a digit) would replace typing 81 numbers into the matrix editor. That is the next version if wanted.
- The real gate and the monkey test, on Rogers-HP.
- Copy into `D:\HP-Prime` (the masters). This cloud session could not reach the computer.
