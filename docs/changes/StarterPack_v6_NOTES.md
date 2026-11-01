# Starter pack v6: notes (1 November 2026)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v6.zip`, built by `tools/make_starter_pack_v4.py v6 --checked FOLDER` from the 30 programs in `programs/`. v5 was built earlier the same day: `StarterPack_v5_NOTES.md`.*

## What changed from v5

Two programs changed:

| Program | v5 | v6 |
| --- | --- | --- |
| TTestLab | beta 1b | **beta 1c** |
| TTestLabG | beta 1 | **beta 1a** |

Both carry the monkey test's fixes (`docs/changes/TTestLab_beta1c_CHANGES.md`, `TTestLabG_beta1a_CHANGES.md`):

- every form field takes numbers only;
- a number with more than 50 digits is refused with a sentence;
- a typed N over 1,000,000 is refused with a sentence.

Everything else in the zip is byte for byte v5's: the other 28 programs, the CentralLimit app and the sample matrix. `READ_ME_FIRST.txt` differs only in its title line and the two versions in its table.

## The two checked files (Virtual Calculator 2.4.2, Rogers-HP, by Claude through computer use)

- **How they were made.** Each was built by hp-prime-kit, copied into the calculator's folder with the calculator closed, opened in the editor and Checked ("No errors in the program"). The calculator was then closed (Calculator → Exit), and the file it wrote back was collected.
  - TTestLab: 125,393 bytes, +10,101.
  - TTestLabG: 123,725 bytes, +9,707.
- **Checked against the source.** `make_starter_pack_v4.py --checked` read the source out of each and found it equal to `programs/<file>.txt`.
- **Collected after a Check and nothing else.** A first TTestLabG file was collected after a run of its example 2, and it was 394 bytes larger: **a checked file keeps the file-level values of its last run** (Lessons Learned v7zg §3). A student would then have found that example's numbers in the forms. It was set aside, and the file was made again by copying in, Checking and closing.
- **The other 28 files** are v5's, collected on 1 November from the calculator after the 31 October runs. They may carry their last run's values. When each program next changes, its file is to be collected after a Check alone.

## Checks

The tool's name check passed. `fleet_names_v2.py` over the 30 programs found 2,259 routine names and 0 collisions. Every file was read back. The pack is 1.45 MB zipped (sha256 begins `d3ffd1430c3a`). The Prime Loader v1d is built from it, and its Chromium test gives 58 PASS (`prime-loader/tests/test_loader_v1d_output.txt`).
