# Starter pack v13: notes (4 November 2026, night)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v13.zip` (1.55 MB), built by `tools/make_starter_pack_v4.py v13 --checked FOLDER` from the 30 programs in `programs/`. v12: `StarterPack_v12_NOTES.md`.*

## What changed from v12

Eighteen programs changed, in round 8:

| Program | v12 | v13 | Round 8 |
| --- | --- | --- | --- |
| AgreeLab | beta 1d | **beta 1e** | the monkey test, 1,000 of 1,000: typed fields; a D list of more than 50 digits left out, with a sentence |
| AnovaLab | beta 1b | **beta 1c** | the same, and s and σ₀ from 1E−50 to 1E50; "t-test" |
| BiNorm3D | beta 1c | **beta 1d** | the monkey test: its field typed |
| BurrLab | beta 1l | **beta 1m** | the monkey test: typed fields; D1 of more than 50 digits refused |
| DNAMixLR | beta 3g | **beta 3h** | the monkey test: the fields of its 15 forms typed |
| DataLoad | beta 1c | **beta 1d** | the monkey test: its field typed; an SD that cannot overflow |
| ErrorRate | beta 1g | **beta 1h** | the monkey test: typed fields |
| FitCheck | beta 1b | **beta 1c** | the monkey test: typed fields; D1 or D2 of more than 50 digits left out; "t-test" |
| RankLab | beta 1c | **beta 1d** | the monkey test: its field typed; a D list of more than 50 digits left out; m₀ beyond 1E50 refused; a scientific number keeps its exponent |
| ResampLab | beta 1d | **beta 1e** | the monkey test: its field typed; D1 or D2 of more than 50 digits refused |
| ExhibitLab (was SeizureLab) | SeizureLab beta 1c | **ExhibitLab beta 1d** | the new name; the monkey test: typed fields; weights of more than 50 digits refused |
| StudRange | beta 15i | **beta 15j** | the monkey test: the fields of its 13 forms typed; "t-test" |
| SurvLab | beta 1c | **beta 1d** | the monkey test: its field typed |
| TrendTest | beta 3i | **beta 3j** | the monkey test: typed fields |
| PowerViz | v2.5n | **v2.5o** | "t-test" on every screen |
| TTestLab | beta 1e | **beta 1f** | "t-test" on every screen |
| TTestLabG | beta 1c | **beta 1d** | "t-test" on every screen |
| TestChooser | beta 2d | **beta 2e** | "t-test" on every screen |

**Renamed:** SeizureLab is now ExhibitLab (Roger, 4 Nov 2026: "seizure" reads as a medical word to many students). Its Home results are EX_N, EX_NMIN, EX_P, EX_LB, EX_PB, EX_TOT and EX_TLB, for SZ_... before. Copying this pack into a calculator that has SeizureLab leaves both: delete SeizureLab from the Program Catalog. The Prime Loader clears the old programs itself.

The other 12 programs and the CentralLimit app are v12's checked files, byte for byte, and so is the sample matrix. Each program's note is `docs/changes/<Name>_<version>_CHANGES.md`; `verify/verify_round8_v2.py` checks all 18 (63 PASS, 0 FAIL).

## The 18 checked files

Each was copied into the Virtual Calculator 2.4.2 running in the cloud workspace under Wine (Lessons Learned v7zn, §16), opened in the editor, and Checked: "No errors in the program". The files the calculator wrote back on Exit are the ones in the pack; `make_starter_pack_v4.py --checked` read the source out of each of the 30 and found it equal to `programs/<file>.txt`. The Prime Loader v1k is built from this pack (58 PASS, 0 FAIL in Chromium). Not yet run on a G1 or a G2.
