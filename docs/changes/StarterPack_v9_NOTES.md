# Starter pack v9: notes (2 November 2026)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v9.zip`, built by `tools/make_starter_pack_v4.py v9 --checked FOLDER` from the 30 programs in `programs/`. v8: `StarterPack_v8_NOTES.md`.*

## What changed from v8

Four programs changed:

| Program | v8 | v9 |
| --- | --- | --- |
| PowerViz | v2.5k | **v2.5l** |
| ScatterLab | beta 2d | **beta 2f** |
| ChiTable | beta 3e | **beta 3f** |
| GaltonBoard | beta 3e | **beta 3f** |

All four carry the monkey test's fixes, round 4, and what round 4's label check found. Their change notes are in `docs/changes/` (`PowerViz_v2.5l_CHANGES.md`, `ScatterLab_beta2f_CHANGES.md`, `ChiTable_beta3f_CHANGES.md`, `GaltonBoard_beta3f_CHANGES.md`). In short:

- every form field takes numbers only;
- a number the program cannot draw is refused with a sentence before anything changes (PowerViz: means and σ above 1,000,000, or too close for 12 digits; ScatterLab: a point or a C1/C2 load of 50 digits, or closer than 12 digits tell apart; ChiTable: α below 0.0001);
- no axis label shows a number cut short: ScatterLab labels a long axis in units (×1ᴇ5) or from its lowest tick and fits its side panel's numbers; PowerViz fits its numbers to their cells;
- ScatterLab writes ŷ and ȳ as letters;
- GaltonBoard's board holds at most 5,000 balls, and its MicroPython drop is "Fill to 5,000".

Everything else in the zip is byte for byte v8's: the other 26 programs, the CentralLimit app and the sample matrix. `READ_ME_FIRST.txt` differs only in its title line and the four versions in its table.

## The four checked files (Virtual Calculator 2.4.2, Rogers-HP, by Claude through computer use)

- Each was built by hp-prime-kit, copied into the calculator's folder with the calculator closed, opened in the editor and Checked ("No errors in the program"), and the file the calculator wrote back was collected **after that Check and nothing else** (a checked file keeps the file-level values of its last run: `StarterPack_v6_NOTES.md`).
  - PowerViz v2.5l: 365,065 bytes, +18,281.
  - ScatterLab beta 2f: 210,818 bytes, +17,080.
  - ChiTable beta 3f: 357,598 bytes, +20,456.
  - GaltonBoard beta 3f: 224,358 bytes, +19,408.
- `make_starter_pack_v4.py --checked` read the source out of each and found it equal to `programs/<file>.txt`.
- The other 26 files are v8's.

## Checks

The tool's name check passed. `fleet_names_v2.py` over the 30 programs found 2,289 routine names and 0 collisions. Every file was read back. The pack is 1.49 MB zipped (1,485,967 bytes; sha256 begins `33f1a8322fd5`). The Prime Loader v1g is built from it, and its Chromium test gives 58 PASS, 0 FAIL (`prime-loader/tests/test_loader_v1g_output.txt`).
