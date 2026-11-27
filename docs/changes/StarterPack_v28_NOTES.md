# Starter pack v28: notes (27 November 2026)

Built by `tools/make_starter_pack_v6.py v28 --kit KIT`, then again with `--checked FOLDER` (`StarterPack_v6_NOTES.md` has the two passes). SHA-256 of the zip begins `d16f5b21cc3d`.

## Why

Round 20 (27 November 2026): **DataLoad beta 1i** (`docs/changes/DataLoad_beta1i_CHANGES.md`). When it loads two or more columns and a blank cell stands above a value in any of them, it asks whether the columns are pairs (keep the complete rows only, so each pair stays a pair) or separate groups (each blank left out of its own column), because beta 1h left each blank out of its own column and paired columns then slid out of step.

## What changed

- **DataLoad.hpprgm**: beta 1i, checked on the Virtual Calculator 2.4.2 in the cloud workspace on 27 November 2026 ("No errors in the program") and collected before it was run (`verify/round20/vc_record.txt`). The builder read its source back and found it equal to `programs/DataLoad_beta1i.txt`.
- **READ_ME_FIRST.txt**: its first line names v28, and DataLoad's line in the table names beta 1i. Nothing else in it is different.
- **The other 34 files**: v27's, byte for byte (compared file by file after the build): the 29 other programs' checked files, the app, the bonus and the sample data are the ones v27 carried, taken from v27 as the checked folder.

## What has been tested

DataLoad beta 1i from this pack's checked file ran on the Virtual Calculator on Student's sleep data with two blank cells: the question, Pairs (8 and 8, the 8 complete patients, row for row), Separate groups (9 and 9), Cancel, and the four help pages (`verify/round20/vc_record.txt`). The Prime Loader v2r is built from this pack (`prime-loader/README.md`, "What v2r changes").
