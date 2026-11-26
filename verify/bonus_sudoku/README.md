# The bonus, Sudoku: starter pack v26 and the Prime Loader v2p (26 November 2026)

How the new versions were made, each from the version before by exact replacements, as a program is:

| Script | What it made |
|---|---|
| `make_pack_v5_from_v4.py` | `tools/make_starter_pack_v5.py` from v4: the folder `Bonus (optional)` and its program (`BONUS`), its name check, its checked file, and the instructions' section on it |
| `make_loader_v2p.py` | `prime-loader/build_loader_v2p.py` and `loader_template_v2p.html` from v2o: the bonus read from the pack and checked against `extras/sudoku/`, and its box under "More choices" |
| `make_test_v2p.py` | `prime-loader/tests/test_loader_v2p.js` from v2o's test: the new names, and part 14, the bonus |

The scripts were run in the cloud workspace, where they name `/home/claude/hp-prime-statistics/` as the repository; they read the files of the version before, which git keeps.

The records: `docs/changes/StarterPack_v26_NOTES.md` (the pack, its Check on the Virtual Calculator, and the comparison with v25), `prime-loader/README.md` ("What v2p adds"), `prime-loader/tests/test_loader_v2p_output.txt`, `tools/pages_a11y_v1_output.txt`, and the program's own folder, `extras/sudoku/` (its verify script and output, its random-use record, and its first run on the Virtual Calculator).
