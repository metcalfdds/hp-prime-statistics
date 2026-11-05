# Starter pack for the Virtual Calculator

*v13, 2026-11-04. Built by `tools/make_starter_pack_v4.py` from `programs/`; do not edit this page by hand.*

All 30 programs in one zip, ready for the free **HP Prime Virtual Calculator** on a Windows PC: no Connectivity Kit, no copying and pasting. Download **[HP_Prime_Statistics_Starter_Pack_v13.zip](https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack/HP_Prime_Statistics_Starter_Pack_v13.zip)** (one file).

*How this pack was tested on the Virtual Calculator: [docs/changes/StarterPack_v13_NOTES.md](../docs/changes/StarterPack_v13_NOTES.md).*

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
| AgreeLab | beta 1e | 3,054 | `AgreeLab` |  | `762324720f7f` |
| AnovaLab | beta 1c | 3,851 | `AnovaLab` |  | `526ecd6d7e9b` |
| BayesTree | beta 8g | 3,430 | `BayesTree` |  | `eb4e57e7a423` |
| BiNorm3D | beta 1d | 1,276 | `BiNorm3D` |  | `ac18c43bdf6b` |
| BurrLab | beta 1m | 4,661 | `BurrLab` | MicroPython | `8c0c97fd86a4` |
| CICatcher | beta 2f | 2,186 | `CICatcher` |  | `92b65551a6ce` |
| CentralLimit | beta 3e | 2,779 | (an app) | app on Statistics 1Var | `5137af22da17` |
| ChiTable | beta 3i | 3,701 | `ChiTable` |  | `23ed396eb6d1` |
| DNAMixLR | beta 3h | 3,467 | `DNAMixLR` |  | `fdfd5be1a9eb` |
| DataLoad | beta 1d | 1,081 | `DATALOAD` |  | `d0db5c90c537` |
| EpiStats | v1.7h | 6,262 | `EpiStats` |  | `23b8189e4495` |
| ErrorRate | beta 1h | 2,857 | `ErrorRate` | MicroPython | `e9aac2a025a9` |
| ExhibitLab | beta 1d | 2,879 | `ExhibitLab` |  | `24bd68d66af6` |
| FitCheck | beta 1c | 3,317 | `FitCheck` |  | `037a525ddae2` |
| GaltonBoard | beta 3g | 2,530 | `GaltonBoard` | MicroPython | `468cb5c3c78c` |
| Norm3 | v2.4e | 1,116 | `Norm3` |  | `8acf4a420f14` |
| NormExplorer | beta 42g | 4,212 | `NormExp` | MicroPython | `0acc8e78f677` |
| PowerViz | v2.5o | 4,149 | `POWERVIZ` |  | `ce32c3cf2816` |
| RankLab | beta 1d | 3,822 | `RankLab` |  | `dafcaee35c80` |
| ResampLab | beta 1e | 3,033 | `ResampLab` |  | `6bcd6a6bc195` |
| RiskLab | beta 1d | 3,162 | `RiskLab` |  | `99611f5d6546` |
| SampDist | v2.3g | 1,920 | `SampDist` |  | `c051c5daa19a` |
| ScatterLab | beta 2g | 2,428 | `ScatterLab` |  | `f9c51a33d276` |
| StatDist | v2.7i | 5,029 | `StatDist` |  | `32f4b589d665` |
| StudRange | beta 15j | 2,723 | `StudRange` | MicroPython | `b07f5d07fcbe` |
| SurvLab | beta 1d | 2,734 | `SurvLab` |  | `32faafc0dcc0` |
| TTestLabG | beta 1d | 1,461 | `TTESTLABG` |  | `6cf5e89b16fc` |
| TTestLab | beta 1f | 1,486 | `TTESTLAB` |  | `b98a2c5f6c29` |
| TestChooser | beta 2e | 1,910 | `TestChooser` |  | `7c7442b8f677` |
| TrendTest | beta 3j | 2,275 | `TrendTest` |  | `a20b64385223` |

*The checksum is the first 12 hex digits of SHA-256 over the program's source (line endings made LF, trailing blank lines dropped): the file in `programs/` it was built from. Every file in the zip was read back and matched its source before the zip was written.*

## Building it again

`python3 tools/make_starter_pack_v4.py v6 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a program changes. The tool names each file, checks the names, builds with hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)), builds the sample matrix from `data-loader/examples/rossi.csv`, reads every file back, and writes the zip and this page. With `--checked` it carries each program as the Virtual Calculator wrote it back after one Check there (the same source plus its compiled block), so students never Check; it stops if a checked file's source differs from `programs/`. Build without `--checked` first, load that pack on the Virtual Calculator, Check each changed program, close it, and copy those files into FOLDER. Move the older zip out of this folder.

*Free for educational and personal use. © 2026 Roger Metcalf.*
