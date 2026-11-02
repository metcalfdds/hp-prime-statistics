# Starter pack v8: notes (1 November 2026, night)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v8.zip`, built by `tools/make_starter_pack_v4.py v8 --checked FOLDER` from the 30 programs in `programs/`. v7 was built earlier the same evening: `StarterPack_v7_NOTES.md`.*

## What changed from v7

Four programs changed:

| Program | v7 | v8 |
| --- | --- | --- |
| CICatcher | beta 2d | **beta 2e** |
| Norm3 | v2.4b | **v2.4d** |
| NormExplorer | beta 42c | **beta 42e** |
| StatDist | v2.7f | **v2.7h** |

All four carry the monkey test's fixes, round 3. Their change notes are in `docs/changes/`: `CICatcher_beta2e_CHANGES.md`; for the other three, two each (`Norm3_v2.4c_CHANGES.md` and `Norm3_v2.4d_CHANGES.md`, `NormExplorer_beta42d_CHANGES.md` and `NormExplorer_beta42e_CHANGES.md`, `StatDist_v2.7g_CHANGES.md` and `StatDist_v2.7h_CHANGES.md`), because the second letter replaced the first the same night, after the Virtual Calculator showed its density labels running over the axis. In short:

- every form field takes numbers only;
- a number the program cannot draw is refused with a sentence before anything changes: 50 digits or more, a σ above 10¹⁰, a scale too small next to its location for the calculator's 12 digits, and (StatDist) a shape parameter outside the range where its family's formulas stay finite;
- Norm3 and StatDist use `<>` where they had `!=` (a factorial and a test on the Prime);
- NormExplorer takes s from the deviations (s from Σx² − n x̄² lost its digits when the mean was large next to s), and its Diagnostics page takes a tap;
- density labels too wide for the margin no longer run over the axis: Norm3 writes them in units of a power of ten (1 2 3 4 5 under ×1ᴇ-4), NormExplorer and StatDist in the scientific form (6ᴇ-5); StatDist no longer cuts a label short ("4000000" showed as "400000") or prints x labels over each other.

Everything else in the zip is byte for byte v7's: the other 26 programs, the CentralLimit app and the sample matrix. `READ_ME_FIRST.txt` differs only in its title line and the four versions in its table.

## The four checked files (Virtual Calculator 2.4.2, Rogers-HP, by Claude through computer use)

- Each was built by hp-prime-kit, copied into the calculator's folder with the calculator closed, opened in the editor and Checked ("No errors in the program"), and the file the calculator wrote back was collected **after that Check and nothing else** (a checked file keeps the file-level values of its last run, `StarterPack_v6_NOTES.md`):
  - CICatcher beta 2e: 177,484 bytes, +14,160.
  - Norm3 v2.4d: 103,036 bytes, +1,568.
  - NormExplorer beta 42e: 381,089 bytes, +19,849.
  - StatDist v2.7h: 451,002 bytes, +19,960.
- Norm3 v2.4c, NormExplorer beta 42d and StatDist v2.7g were checked and collected the same way first; testing them there showed their density labels over the axis, and the files above replaced theirs.
- `make_starter_pack_v4.py --checked` read the source out of each and found it equal to `programs/<file>.txt`.
- The other 26 files are v7's.

## Checks

The tool's name check passed. `fleet_names_v2.py` over the 30 programs found 2,277 routine names and 0 collisions. Every file was read back. The pack is 1.47 MB zipped (1,473,829 bytes; sha256 begins `f1ae5fb157f5`). The Prime Loader v1f is built from it, and its Chromium test gives 58 PASS (`prime-loader/tests/test_loader_v1f_output.txt`).
