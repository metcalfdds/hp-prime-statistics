# Starter pack v29: notes (28 November 2026)

Built by `tools/make_starter_pack_v6.py v29 --kit KIT`, then again with `--checked FOLDER` (`StarterPack_v6_NOTES.md` has the two passes). SHA-256 of the zip begins `572353139c80`.

## Why

Round 21 (28 November 2026): **TTestLab beta 1n** and **TTestLabG beta 1k** (`docs/changes/TTestLab_beta1n_CHANGES.md`, `docs/changes/TTestLabG_beta1k_CHANGES.md`). Each number on steps 2 and 4 is now worked out from the numbers shown before it, so that each step checks on a calculator, because beta 1m and beta 1j showed every number rounded from the exact value and a step could miss (the draft lottery's 13,707/37.81 is 362.52, where the screen said 362.56).

## What changed

- **TTestLab.hpprgm**: beta 1n, and **TTestLabG.hpprgm**: beta 1k, each checked on the Virtual Calculator 2.4.2 in the cloud workspace on 28 November 2026 at 03:33 ("No errors in the program") and collected before either was run (`verify/round21/vc_record.txt`). The first pass's two files, the ones that were checked, are byte for byte what `hpprime write` makes of `programs/`; the builder read each checked file's source back and found it equal to `programs/TTestLab_beta1n.txt` and `programs/TTestLabG_beta1k.txt`.
- **READ_ME_FIRST.txt**: its first line names v29, and the two programs' lines in the table name beta 1n and beta 1k. Nothing else in it is different.
- **The other 33 files**: v28's, byte for byte (compared file by file after the build): the 28 other programs' checked files, the app, the bonus and the sample data are the ones v28 carried, taken from v28 as the checked folder.

## What has been tested

TTestLab beta 1n and TTestLabG beta 1k from this pack's checked files ran on the Virtual Calculator after they were collected (`verify/round21/vc_record.txt`). The Prime Loader v2s is built from this pack (`prime-loader/README.md`, "What v2s changes").
