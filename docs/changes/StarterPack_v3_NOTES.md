# Starter pack v3: notes (31 October 2026, night)

*The pack: `starter-pack/HP_Prime_Statistics_Starter_Pack_v3.zip`, built by `tools/make_starter_pack_v3.py v3` from the 29 programs in `programs/` as of this commit. v1 and v2 (the same day) and how a pack is loaded and tested: `StarterPack_v1_NOTES.md`, `StarterPack_v2_NOTES.md`.*

## What changed from v2

- **TTestLab beta 1b** replaces beta 1a (`TTestLab_beta1b_CHANGES.md`: the independent review's eleven findings fixed). Its file in the pack (105,730 bytes) is byte for byte `hpprime write` of `programs/TTestLab_beta1b.txt`; the file that ran on the Virtual Calculator that night differs from it in two header comment lines only (the firmware note, written after the run).
- `READ_ME_FIRST.txt` and `starter-pack/README.md`: TTestLab's version line.
- `tools/make_starter_pack_v3.py` replaces v2: the instructions name the Data Loader by its folder, `data-loader/`, not by the page's versioned file name.
- Everything else, the sample matrix included, is byte for byte v2's.

## Checks

Every program read back equal to its source; the name check passed; `fleet_names_v2.py programs/*.txt`: 29 files, 2,203 routine names, 0 collisions; 1.37 MB zipped. v2's zip and tool, and a first build of v3 made with the v2 tool (its read-me named the page by its old file name), are in the author's `_superseded_2026-10-31` folder (neither v1 nor v2 was committed: all three packs were built the same day).
