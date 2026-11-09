# Starter pack for the Virtual Calculator

*v16, 2026-11-09. Built by `tools/make_starter_pack_v4.py` from `programs/`; do not edit this page by hand.*

All 31 programs in one zip, ready for the free **HP Prime Virtual Calculator** on a Windows PC: no Connectivity Kit, no copying and pasting. Download **[HP_Prime_Statistics_Starter_Pack_v16.zip](https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack/HP_Prime_Statistics_Starter_Pack_v16.zip)** (one file).

*How this pack was tested on the Virtual Calculator: [docs/changes/StarterPack_v16_NOTES.md](../docs/changes/StarterPack_v16_NOTES.md).*

### What you need
- A Windows PC with the HP Prime Virtual Calculator (64-bit). It is a free download from hpcalc.org, which lists Hewlett-Packard as its author. The pack was tested on the Virtual Calculator 2.4.2 (build 2026-09-09), 64-bit.
- The zip, unzipped (right-click it, Extract All).

### Install
1. Start the Virtual Calculator once, then close it (Calculator menu, Exit). That first start makes its folder: `Documents\HP Prime\Calculators\Prime`.
2. Open the unzipped folder `Copy these into Prime` and copy everything in it into that Prime folder. The calculator must be closed while you copy: it reads its folder only when it starts.
3. Start the Virtual Calculator. Shift, then Program (the Program Catalog) lists the programs.

### Run a program
- In the Program Catalog, tap the program, then tap Run. Or type its name in Home (the list below) and press Enter. Nothing to check or compile first: every file in this pack was checked on the Virtual Calculator before it was packed.
- If a program ever says Syntax Error, or Run does nothing (a different version of the Virtual Calculator may want to compile it again): tap it, tap Edit, tap Check, tap OK, press Esc, then tap Run. Once is enough.
- CentralLimit is an app, built on Statistics 1Var: press Apps, highlight it and tap Start (touching its icon opens its spreadsheet instead). Then press View for its menu.
- BurrLab, ErrorRate, GaltonBoard, NormExplorer and StudRange carry MicroPython. They work the same way: the Virtual Calculator has the calculator's own MicroPython.

### Your own data: DataLoad
- Typing a long data set into a calculator is not feasible. The HP Prime Data Loader, a web page in this repository (its folder `data-loader`), turns columns pasted from Excel, SPSS or a CSV file into the calculator's own matrix file, `M1.hpmat`. Copy it into the Prime folder the same way (calculator closed), then run DataLoad: it puts each column, or each group's scores, into the Statistics 1Var lists D1-D9 (or Statistics 2Var C1-C9) that the other programs read.
- Open the Statistics 1Var app once (Apps) before the first load: its lists do not exist until then.
- If DataLoad says lists after the new ones hold data from before, choose clear. AnovaLab, RankLab and AgreeLab read every list that holds data as one more group (or rater).
- `Sample data (optional)` holds `M1.hpmat`: the Rossi re-arrest data (432 rows x 5 columns: week of first re-arrest, arrest 1/0, financial aid 1/0, age, prior convictions). Copy it too if you want data to try: it becomes the calculator's matrix M1 and replaces what M1 held. Then DataLoad, Scores by group, scores in column 1, groups in column 3, puts the weeks without and with financial aid in D1 and D2, ready for TTestLab.

### Good to know
- Windows asks before it replaces a file of the same name. Replacing it replaces that program on the calculator.
- On a real HP Prime (G1 or G2), send programs with the Connectivity Kit instead, a few at a time: copying files works only for the Virtual Calculator.
- Each program's source, its change notes and how it was tested are in the repository: programs/, docs/changes/ and verify/.

## What is in the pack

| Program | Version | Lines | In Home, type | Notes | Source checksum |
|---|---|---|---|---|---|
| AgreeLab | beta 1g | 3,062 | `AgreeLab` |  | `b6906cd2cfb1` |
| AnovaLab | beta 1f | 3,869 | `AnovaLab` |  | `73636e53493d` |
| BayesTree | beta 8j | 3,446 | `BayesTree` |  | `762c4a0de095` |
| BiNorm3D | beta 1f | 1,282 | `BiNorm3D` |  | `e3da40166171` |
| BurrLab | beta 1q | 4,712 | `BurrLab` | MicroPython | `efaa895d783a` |
| CICatcher | beta 2i | 2,194 | `CICatcher` |  | `a4bc79d6056c` |
| CentralLimit | beta 3g | 2,788 | (an app) | app on Statistics 1Var | `502640fe6456` |
| ChiTable | beta 3l | 3,720 | `ChiTable` |  | `b86ebd200acb` |
| DNAMixLR | beta 3j | 3,471 | `DNAMixLR` |  | `349a8cc1899c` |
| DataLoad | beta 1f | 1,089 | `DATALOAD` |  | `61fd85695761` |
| EpiStats | v1.7k | 6,275 | `EpiStats` |  | `373769909c5c` |
| ErrorRate | beta 1j | 2,857 | `ErrorRate` | MicroPython | `cda5cb9c2b2d` |
| ExhibitLab | beta 1g | 2,889 | `ExhibitLab` |  | `09dc494a2d16` |
| FitCheck | beta 1f | 3,349 | `FitCheck` |  | `e43983ef6b49` |
| GaltonBoard | beta 3i | 2,533 | `GaltonBoard` | MicroPython | `d9c1bb807fcc` |
| Norm3 | v2.4g | 1,125 | `Norm3` |  | `e45ead59d4df` |
| NormExplorer | beta 42j | 4,228 | `NormExp` | MicroPython | `86d9dfd7e9d1` |
| PowerViz | v2.5r | 4,184 | `POWERVIZ` |  | `b0be46d986d1` |
| RankLab | beta 1g | 3,825 | `RankLab` |  | `0862a46f0106` |
| ResampLab | beta 1h | 3,045 | `ResampLab` |  | `3fab54ee41a1` |
| RiskLab | beta 1f | 3,160 | `RiskLab` |  | `6128c64c8133` |
| SampDist | v2.3j | 1,930 | `SampDist` |  | `38b2bb9b724e` |
| ScatterLab | beta 2j | 2,436 | `ScatterLab` |  | `8d4144c5958d` |
| StatDist | v2.7l | 5,089 | `StatDist` |  | `c34b446f83e4` |
| StudRange | beta 15m | 2,750 | `StudRange` | MicroPython | `cb1b060d6f83` |
| SurvLab | beta 1f | 2,741 | `SurvLab` |  | `9ed223b72643` |
| TDist3D | beta 1a | 1,164 | `TDist3D` |  | `f370e341f4e6` |
| TTestLabG | beta 1g | 1,478 | `TTESTLABG` |  | `ab792d637b46` |
| TTestLab | beta 1i | 1,503 | `TTESTLAB` |  | `dd90c795f2e3` |
| TestChooser | beta 2g | 1,914 | `TestChooser` |  | `e790d3eadf7d` |
| TrendTest | beta 3m | 2,289 | `TrendTest` |  | `d14cbccef5d7` |

*The checksum is the first 12 hex digits of SHA-256 over the program's source (line endings made LF, trailing blank lines dropped): the file in `programs/` it was built from. Every file in the zip was read back and matched its source before the zip was written.*

## Building it again

`python3 tools/make_starter_pack_v4.py v6 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a program changes. The tool names each file, checks the names, builds with hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)), builds the sample matrix from `data-loader/examples/rossi.csv`, reads every file back, and writes the zip and this page. With `--checked` it carries each program as the Virtual Calculator wrote it back after one Check there (the same source plus its compiled block), so students never Check; it stops if a checked file's source differs from `programs/`. Build without `--checked` first, load that pack on the Virtual Calculator, Check each changed program, close it, and copy those files into FOLDER. Move the older zip out of this folder.

*Free for educational and personal use. © 2026 Roger Metcalf.*
