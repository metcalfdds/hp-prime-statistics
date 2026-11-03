# Starter pack v10: notes (2 November 2026, night)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v10.zip`, built by `tools/make_starter_pack_v4.py v10 --checked FOLDER` from the 30 programs in `programs/`. v9: `StarterPack_v9_NOTES.md`.*

## What changed from v9

All 30 programs changed, for one reason: **every number of 1,000 or more on the screen now shows its commas** (12,345.678; 1,000,000), by APA's rule: never after the decimal point, never in a year, never in text the calculator's CAS reads. AgreeLab and ResampLab also draw d̄ (a d with a bar over it), which the calculator's font does not have. How it was done and checked: `docs/dev/commas-2026-11-02.md`; each program's change note is in `docs/changes/`.

| Program | v9 | v10 |
| --- | --- | --- |
| AgreeLab | beta 1b | **beta 1c** |
| AnovaLab | beta 1a | **beta 1b** |
| BayesTree | beta 8f | **beta 8g** |
| BiNorm3D | beta 1b | **beta 1c** |
| BurrLab | beta 1i | **beta 1j** |
| CICatcher | beta 2e | **beta 2f** |
| CentralLimit | beta 3d | **beta 3e** |
| ChiTable | beta 3f | **beta 3g** |
| DNAMixLR | beta 3e | **beta 3f** |
| DataLoad | beta 1b | **beta 1c** |
| EpiStats | v1.7e | **v1.7f** |
| ErrorRate Lab | beta 1e | **beta 1f** |
| FitCheck | beta 1a | **beta 1b** |
| GaltonBoard | beta 3f | **beta 3g** |
| Norm3 | v2.4d | **v2.4e** |
| NormExplorer | beta 42e | **beta 42f** |
| PowerViz | v2.5l | **v2.5m** |
| RankLab | beta 1b | **beta 1c** |
| ResampLab | beta 1c | **beta 1d** |
| RiskLab | beta 1b | **beta 1c** |
| SampDist | v2.3e | **v2.3f** |
| ScatterLab | beta 2f | **beta 2g** |
| SeizureLab | beta 1b | **beta 1c** |
| StatDist | v2.7h | **v2.7i** |
| StudRange | beta 15f | **beta 15g** |
| SurvLab | beta 1b | **beta 1c** |
| TTestLab | beta 1c | **beta 1d** |
| TTestLabG | beta 1a | **beta 1b** |
| TestChooser | beta 2c | **beta 2d** |
| TrendTest | beta 3g | **beta 3h** |

The sample matrix is v9's, byte for byte. `READ_ME_FIRST.txt` differs only in its title line and the versions in its table.

## The 30 checked files (Virtual Calculator 2.4.2, Rogers-HP, by Claude through computer use)

All 30 were copied into the Virtual Calculator 2.4.2 (Rogers-HP, 2 November 2026, night; Claude through computer use), opened in the editor and Checked: **"No errors in the program"**, every one. The files the calculator wrote back after those Checks, and nothing else, are the ones in starter pack v10. A hand trial of GaltonBoard showed "n = 1,000" after "Drop 1,000 balls", "n = 5,000" and "4,000 balls in 88 ms" after "Fill to 5,000", and "After Galton (1873)" with its year untouched. Each change note in `docs/changes/` records its program's Check.

`make_starter_pack_v4.py --checked` read the source out of each and found it equal to `programs/<file>.txt`.

## Checks

The tool's name check passed. `fleet_names_v2.py` over the 30 programs: 2,323 routine names, 0 collisions. Every file was read back. The pack is 1,525,130 bytes (1.53 MB; sha256 begins `c281f27bdd45`). The Prime Loader v1h is built from it, and its Chromium test gives 58 PASS, 0 FAIL (`prime-loader/tests/test_loader_v1h_output.txt`).
