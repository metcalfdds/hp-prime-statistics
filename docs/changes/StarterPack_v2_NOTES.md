# Starter pack v2: notes (31 October 2026)

*The pack: `starter-pack/HP_Prime_Statistics_Starter_Pack_v2.zip`, built by `tools/make_starter_pack_v2.py v2` from the 29 programs in `programs/` as of this commit. v1 (the same day, 28 programs) and how a pack is loaded and tested: `StarterPack_v1_NOTES.md`.*

## What changed from v1

- **DataLoad beta 1b** added: `Copy these into Prime/DataLoad.hpprgm` (73,068 bytes). It is the file that ran on the Virtual Calculator in DataLoad's third run (`DataLoad_beta1b_CHANGES.md`): same SHA-256.
- **Sample data (optional)/M1.hpmat**: the Rossi re-arrest data, 432 × 5 (week of first re-arrest, arrest 1/0, financial aid 1/0, age, prior convictions), written by hp-prime-kit's `matrix write` from `data-loader/examples/rossi.csv` and read back value for value. It is byte for byte the M1 that the Data Loader page writes and that DataLoad loaded on the Virtual Calculator. It sits in its own folder because copying it replaces the calculator's matrix M1.
- **READ_ME_FIRST.txt and starter-pack/README.md** gain "Your own data: DataLoad": what the Data Loader page is for, opening Statistics 1Var once, clearing lists left from an earlier load, and how to try the sample (Scores by group, scores in column 1, groups in column 3, then TTestLab).
- **tools/make_starter_pack_v2.py** replaces v1: it builds and checks the sample (`--sample CSV`, or `--sample none`).

## Checks

- Every program read back equal to its source; the name check passed; `fleet_names_v2.py programs/*.txt`: 29 files, 2,200 routine names, 0 collisions; `case_scan_v1.py`: nothing to report.
- **The other 28 files and CentralLimit's app folder are byte for byte the files in v1**, which loaded and passed Check on the Virtual Calculator 2.4.2 (v1's notes). Only `READ_ME_FIRST.txt` differs, and the two new files are added. So every file in v2 has been on the Virtual Calculator; v2 as one zip has not been unpacked there by someone other than us.
- 1.37 MB zipped.

## Not tested

- The `Sample data (optional)` instructions read by a student.
- As for v1: a computer that has never run the Virtual Calculator, the Mac and Linux builds, and a G1 or G2 (which use the Connectivity Kit).
