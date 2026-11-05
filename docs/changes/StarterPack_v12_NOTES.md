# Starter pack v12: notes (4 November 2026)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v12.zip`, built by `tools/make_starter_pack_v4.py v12 --checked FOLDER` from the 30 programs in `programs/`. v11: `StarterPack_v11_NOTES.md`.*

## What changed from v11

Five programs changed, in round 7:

| Program | v11 | v12 | Round 7 |
| --- | --- | --- | --- |
| ChiTable | beta 3h | **beta 3i** | the party table labeled GSS 2000, not 1991 |
| EpiStats | v1.7g | **v1.7h** | its first monkey test: typed fields; sample sizes and rates that cannot underflow or overflow; percentages and totals that fit |
| ErrorRate | beta 1f | **beta 1g** | its help no longer says it has never run on a calculator |
| TTestLab | beta 1d | **beta 1e** | the flowchart's go-ahead key reads Run, not OK |
| TTestLabG | beta 1b | **beta 1c** | the same |

The other 25 programs and the CentralLimit app are v11's checked files, byte for byte, and so is the sample matrix.

## The 5 checked files

Each was copied into the Virtual Calculator 2.4.2 running in the cloud workspace under Wine (Lessons Learned v7zm, §16), opened in the editor, and Checked: "No errors in the program". The files the calculator wrote back on Exit are the ones in the pack; `make_starter_pack_v4.py --checked` read the source out of each of the 30 and found it equal to `programs/<file>.txt`. The Prime Loader v1j is built from this pack (58 PASS, 0 FAIL in Chromium).
