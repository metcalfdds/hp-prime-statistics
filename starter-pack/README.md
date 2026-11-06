# Starter pack for the Virtual Calculator

*v14, 2026-11-05. Built by `tools/make_starter_pack_v4.py` from `programs/`; do not edit this page by hand.*

All 30 programs in one zip, ready for the free **HP Prime Virtual Calculator** on a Windows PC: no Connectivity Kit, no copying and pasting. Download **[HP_Prime_Statistics_Starter_Pack_v14.zip](https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack/HP_Prime_Statistics_Starter_Pack_v14.zip)** (one file).

*How this pack was tested on the Virtual Calculator: [docs/changes/StarterPack_v14_NOTES.md](../docs/changes/StarterPack_v14_NOTES.md).*

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
| AgreeLab | beta 1f | 3,058 | `AgreeLab` |  | `8535f0cf59e0` |
| AnovaLab | beta 1e | 3,859 | `AnovaLab` |  | `e213819ded6a` |
| BayesTree | beta 8i | 3,438 | `BayesTree` |  | `8cbf7caaeb58` |
| BiNorm3D | beta 1e | 1,279 | `BiNorm3D` |  | `7331fb308b55` |
| BurrLab | beta 1o | 4,679 | `BurrLab` | MicroPython | `a67e824b7cdc` |
| CICatcher | beta 2h | 2,195 | `CICatcher` |  | `02902bfc2153` |
| CentralLimit | beta 3f | 2,782 | (an app) | app on Statistics 1Var | `d4083c5414cf` |
| ChiTable | beta 3k | 3,707 | `ChiTable` |  | `156aedad27bb` |
| DNAMixLR | beta 3i | 3,470 | `DNAMixLR` |  | `2b5de17f1bc2` |
| DataLoad | beta 1e | 1,084 | `DATALOAD` |  | `6025099152ad` |
| EpiStats | v1.7j | 6,271 | `EpiStats` |  | `c695200ba3a9` |
| ErrorRate | beta 1i | 2,860 | `ErrorRate` | MicroPython | `46bee1b228ed` |
| ExhibitLab | beta 1f | 2,891 | `ExhibitLab` |  | `094b6b93a042` |
| FitCheck | beta 1e | 3,343 | `FitCheck` |  | `360488bfb92d` |
| GaltonBoard | beta 3h | 2,533 | `GaltonBoard` | MicroPython | `d59b84a38892` |
| Norm3 | v2.4f | 1,120 | `Norm3` |  | `e186544cee9a` |
| NormExplorer | beta 42i | 4,223 | `NormExp` | MicroPython | `10a3ccacc5b3` |
| PowerViz | v2.5q | 4,161 | `POWERVIZ` |  | `5300739d2344` |
| RankLab | beta 1f | 3,829 | `RankLab` |  | `8dde0d82d575` |
| ResampLab | beta 1g | 3,039 | `ResampLab` |  | `ffe518dd5dc9` |
| RiskLab | beta 1e | 3,166 | `RiskLab` |  | `4a55de6dde4a` |
| SampDist | v2.3i | 1,931 | `SampDist` |  | `673e9ccff429` |
| ScatterLab | beta 2i | 2,434 | `ScatterLab` |  | `a07eb77f874f` |
| StatDist | v2.7k | 5,089 | `StatDist` |  | `2d5ee4034d6d` |
| StudRange | beta 15l | 2,735 | `StudRange` | MicroPython | `038e4d8f3654` |
| SurvLab | beta 1e | 2,738 | `SurvLab` |  | `54b8f6a74c33` |
| TTestLabG | beta 1f | 1,471 | `TTESTLABG` |  | `8c4496e259fd` |
| TTestLab | beta 1h | 1,496 | `TTESTLAB` |  | `03da2aa66b91` |
| TestChooser | beta 2f | 1,913 | `TestChooser` |  | `26a859337ebe` |
| TrendTest | beta 3l | 2,283 | `TrendTest` |  | `8d6be7847faf` |

*The checksum is the first 12 hex digits of SHA-256 over the program's source (line endings made LF, trailing blank lines dropped): the file in `programs/` it was built from. Every file in the zip was read back and matched its source before the zip was written.*

## Building it again

`python3 tools/make_starter_pack_v4.py v6 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a program changes. The tool names each file, checks the names, builds with hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)), builds the sample matrix from `data-loader/examples/rossi.csv`, reads every file back, and writes the zip and this page. With `--checked` it carries each program as the Virtual Calculator wrote it back after one Check there (the same source plus its compiled block), so students never Check; it stops if a checked file's source differs from `programs/`. Build without `--checked` first, load that pack on the Virtual Calculator, Check each changed program, close it, and copy those files into FOLDER. Move the older zip out of this folder.

*Free for educational and personal use. © 2026 Roger Metcalf.*
