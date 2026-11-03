# Starter pack for the Virtual Calculator

*v9, 2026-11-02. Built by `tools/make_starter_pack_v4.py` from `programs/`; do not edit this page by hand.*

All 30 programs in one zip, ready for the free **HP Prime Virtual Calculator** on a Windows PC: no Connectivity Kit, no copying and pasting. Download **[HP_Prime_Statistics_Starter_Pack_v9.zip](https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack/HP_Prime_Statistics_Starter_Pack_v9.zip)** (one file).

*How this pack was tested on the Virtual Calculator: [docs/changes/StarterPack_v9_NOTES.md](../docs/changes/StarterPack_v9_NOTES.md).*

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
| AgreeLab | beta 1b | 2,957 | `AgreeLab` |  | `3b5c24757688` |
| AnovaLab | beta 1a | 3,772 | `AnovaLab` |  | `68c695871bb1` |
| BayesTree | beta 8f | 3,364 | `BayesTree` |  | `8b7b6ea9f1f1` |
| BiNorm3D | beta 1b | 1,214 | `BiNorm3D` |  | `742dc06b3f6b` |
| BurrLab | beta 1i | 4,381 | `BurrLab` | MicroPython | `e8989b06a5a2` |
| CICatcher | beta 2e | 2,132 | `CICatcher` |  | `c301fd817b8f` |
| CentralLimit | beta 3d | 2,725 | (an app) | app on Statistics 1Var | `9dc7d25fb7c5` |
| ChiTable | beta 3f | 3,617 | `ChiTable` |  | `2a97945e79cf` |
| DNAMixLR | beta 3e | 3,372 | `DNAMixLR` |  | `0f79501fc017` |
| DataLoad | beta 1b | 1,007 | `DATALOAD` |  | `1adf9818810b` |
| EpiStats | v1.7e | 6,094 | `EpiStats` |  | `75dcb9c26958` |
| ErrorRate | beta 1e | 2,778 | `ErrorRate` | MicroPython | `6888230189a6` |
| FitCheck | beta 1a | 3,232 | `FitCheck` |  | `4a809a3b9819` |
| GaltonBoard | beta 3f | 2,471 | `GaltonBoard` | MicroPython | `7ff40ead3d1c` |
| Norm3 | v2.4d | 1,062 | `Norm3` |  | `ad35545f4fdb` |
| NormExplorer | beta 42e | 4,144 | `NormExp` | MicroPython | `91cbdbb86af3` |
| PowerViz | v2.5l | 4,084 | `POWERVIZ` |  | `1bbee8b40ea7` |
| RankLab | beta 1b | 3,734 | `RankLab` |  | `fffcad282d48` |
| ResampLab | beta 1c | 2,936 | `ResampLab` |  | `bb571c744b47` |
| RiskLab | beta 1b | 3,102 | `RiskLab` |  | `a949b5181bfe` |
| SampDist | v2.3e | 1,850 | `SampDist` |  | `f0cf52265f6e` |
| ScatterLab | beta 2f | 2,372 | `ScatterLab` |  | `6c45e0a866e4` |
| SeizureLab | beta 1b | 2,802 | `SeizureLab` |  | `27ccda7bad26` |
| StatDist | v2.7h | 4,972 | `StatDist` |  | `25b5780a721d` |
| StudRange | beta 15f | 2,584 | `StudRange` | MicroPython | `a689bc28f64b` |
| SurvLab | beta 1b | 2,672 | `SurvLab` |  | `e62650dabde0` |
| TTestLabG | beta 1a | 1,393 | `TTESTLABG` |  | `43108258f901` |
| TTestLab | beta 1c | 1,420 | `TTESTLAB` |  | `172819074c60` |
| TestChooser | beta 2c | 1,853 | `TestChooser` |  | `5e16ec2ea20c` |
| TrendTest | beta 3g | 2,196 | `TrendTest` |  | `abbccd89a046` |

*The checksum is the first 12 hex digits of SHA-256 over the program's source (line endings made LF, trailing blank lines dropped): the file in `programs/` it was built from. Every file in the zip was read back and matched its source before the zip was written.*

## Building it again

`python3 tools/make_starter_pack_v4.py v6 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a program changes. The tool names each file, checks the names, builds with hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)), builds the sample matrix from `data-loader/examples/rossi.csv`, reads every file back, and writes the zip and this page. With `--checked` it carries each program as the Virtual Calculator wrote it back after one Check there (the same source plus its compiled block), so students never Check; it stops if a checked file's source differs from `programs/`. Build without `--checked` first, load that pack on the Virtual Calculator, Check each changed program, close it, and copy those files into FOLDER. Move the older zip out of this folder.

*Free for educational and personal use. © 2026 Roger Metcalf.*
