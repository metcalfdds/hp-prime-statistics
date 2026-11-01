# Starter pack v4: notes (31 October 2026, night)

*The pack: `starter-pack/HP_Prime_Statistics_Starter_Pack_v4.zip`, built by `tools/make_starter_pack_v3.py v4` from the 30 programs in `programs/` as of this commit. v1 to v3 (the same day) and how a pack is loaded and tested: `StarterPack_v1_NOTES.md`, `StarterPack_v2_NOTES.md`, `StarterPack_v3_NOTES.md`.*

## What changed from v3

- **TTestLabG beta 1** (new): the general version of TTestLab (`TTestLabG_beta1_NOTES.md`). Its file in the pack, `TTestLabG.hpprgm` (105,238 bytes), is byte for byte `hpprime write` of `programs/TTestLabG_beta1.txt`. TTestLab stays in the pack beside it; the two share no routine names.
- `READ_ME_FIRST.txt` and `starter-pack/README.md`: the version line and TTestLabG's row.
- Everything else, the sample matrix included, is byte for byte v3's (compared file by file with v3's zip: one new file, one changed read-me).

## Checks

Every program read back equal to its source; the name check passed; `fleet_names_v2.py programs/*.txt`: 30 files, 2,251 routine names, 0 collisions; 1.39 MB zipped. v3's zip is in the author's `_superseded_2026-10-31` folder (it was never committed: all four packs were built the same day).

**On the Virtual Calculator.** The 29 files v4 shares with v3 are the ones v1–v3's load tests ran (v3's TTestLab differs from the file that ran in two header comment lines). `TTestLabG.hpprgm` is byte for byte the file that was copied into the Virtual Calculator, checked and run on 31 Oct 2026 (`TTestLabG_beta1_NOTES.md`). A first build of v4 carried TTestLabG's first build, whose menu still said "Quit TTestLab"; it is in the author's `_superseded_2026-10-31` folder.
