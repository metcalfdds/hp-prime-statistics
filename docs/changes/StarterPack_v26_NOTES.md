# Starter pack v26: notes (26 November 2026)

Built by `tools/make_starter_pack_v5.py v26 --checked DIR` from `programs/` and `extras/sudoku/`. The pack holds the same 31 programs as v25, and one thing more: **the bonus**, Sudoku beta 2a, in a folder of its own, `Bonus (optional)/Sudoku.hpprgm`, beside the sample data.

## Why

Roger, 26 November 2026, on the Sudoku program: "maybe add this as a bonus—"just for fun"". Asked how students should get it, he chose the Prime Loader's "More choices", with the 31 *Statisticles* staying the Population. The book tells about Sudoku in its Appendix G, "Just for fun: Sudoku, and the statistics hiding in it", and Appendix F says how it works inside. So the pack carries Sudoku apart from the 31: not in `Copy these into Prime`, which stays the 31, but in `Bonus (optional)`, and READ_ME_FIRST.txt has a short section, "Just for fun: the bonus", that says what it is and that it is copied in the same way if wanted.

## What changed in the builder (`tools/make_starter_pack_v5.py`, from v4)

- `BONUS = ['extras/sudoku']`: each folder holds one program file, `<Name>_beta*.txt` or `<Name>_v*.txt` (the verify script's output and the like do not count). A bonus program is built, read back and compared with its source, and with `--checked` taken checked, exactly as a program is; its checked file is `<Name>.hpprgm` in the checked folder beside the others.
- Its names join the pool that the name check reads, so a bonus program can never clash with a *Statisticle* on the calculator (all programs on a Prime share one pool of names). Sudoku's 62 routine names clash with none.
- The instructions keep the 31 as "the programs" and tell the bonus apart; the README's table has a row for it, marked "bonus".

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 26 November 2026

The calculator is the one in the cloud workspace, HP's program under Wine (`tools/vc_cloud_v1/`).

- **The Check.** The first pass of the builder made the unchecked `Sudoku.hpprgm` (195,856 bytes). It was copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed; Program Catalog > Edit > Check said "No errors in the program" at 09:48 (`tools/vc_cloud_v1/check_all.py`), and nothing ran before Calculator > Exit. The file the calculator wrote back, 244,804 bytes (the source and a compiled block of 48,948 bytes), is the checked file.
- The checked folder was v25's 31 checked files, taken from v25's `Copy these into Prime`, and Sudoku's. The second pass of the builder read every checked file back: the same source as `programs/` (and, for Sudoku, `extras/sudoku/`), plus the calculator's compiled block, for all 32.
- **A run**, afterwards, in another session of the calculator: a new Easy puzzle, Hint, the game finished with Hint and kept as game 1 of My games, the My games plot, and the copy into *Statistics 2Var* (`extras/sudoku/vc_2026-11-26/README.md`, with the captures).

## Compared with v25

Every file that v25 has is in v26 byte for byte (34 files, compared file by file), but READ_ME_FIRST.txt, which differs in the pack's version and date, the section on the bonus, and one row of its table. The one new file is `Bonus (optional)/Sudoku.hpprgm`.

## The Prime Loader

`prime-loader/build_loader_v2p.py` built `PrimeLoader_v2p.html` from this pack: 31 of 31 files checked, and the bonus checked. `tests/test_loader_v2p.js`: **173 PASS, 0 FAIL** in Chromium, v2o's 161 checks and 12 for the bonus (`tests/test_loader_v2p_output.txt`). The page is v2o's with the bonus's box under "More choices" (the template's first comment and `prime-loader/README.md` say what changed).

## Not done

No file of this pack has run on a G1 or a G2, Sudoku included.
