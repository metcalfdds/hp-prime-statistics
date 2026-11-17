# Starter pack for the Virtual Calculator

*v23, 2026-11-17. Built by `tools/make_starter_pack_v4.py` from `programs/`; do not edit this page by hand.*

All 31 programs in one zip, ready for the free **HP Prime Virtual Calculator** on a Windows PC: no Connectivity Kit, no copying and pasting. Download **[HP_Prime_Statistics_Starter_Pack_v23.zip](https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack/HP_Prime_Statistics_Starter_Pack_v23.zip)** (one file).

*How this pack was tested on the Virtual Calculator: [docs/changes/StarterPack_v23_NOTES.md](../docs/changes/StarterPack_v23_NOTES.md).*

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
| AgreeLab | beta 1i | 3,074 | `AgreeLab` |  | `d1b50dbe1c7e` |
| AnovaLab | beta 1j | 4,749 | `AnovaLab` |  | `f64528c670d4` |
| BayesTree | beta 8k | 3,451 | `BayesTree` |  | `707756c05296` |
| BiNorm3D | beta 1g | 1,611 | `BiNorm3D` |  | `480bd7ed7177` |
| BurrLab | beta 1r | 4,721 | `BurrLab` | MicroPython | `0b23152be32c` |
| CICatcher | beta 2m | 2,489 | `CICatcher` |  | `bf6341bfa91a` |
| CentralLimit | beta 3g | 2,788 | (an app) | app on Statistics 1Var | `502640fe6456` |
| ChiTable | beta 3m | 3,863 | `ChiTable` |  | `46f1745b9ede` |
| DNAMixLR | beta 3j | 3,471 | `DNAMixLR` |  | `349a8cc1899c` |
| DataLoad | beta 1g | 1,094 | `DATALOAD` |  | `e211874d3a5e` |
| EpiStats | v1.7m | 6,285 | `EpiStats` |  | `28b1210aa38a` |
| ErrorRate | beta 1j | 2,857 | `ErrorRate` | MicroPython | `cda5cb9c2b2d` |
| ExhibitLab | beta 1i | 2,903 | `ExhibitLab` |  | `bbe79a6f998e` |
| FitCheck | beta 1j | 3,906 | `FitCheck` |  | `18bf2c2bc170` |
| GaltonBoard | beta 3i | 2,533 | `GaltonBoard` | MicroPython | `d9c1bb807fcc` |
| Norm3 | v2.4g | 1,125 | `Norm3` |  | `e45ead59d4df` |
| NormExplorer | beta 42j | 4,228 | `NormExp` | MicroPython | `86d9dfd7e9d1` |
| PowerViz | v2.5t | 4,196 | `POWERVIZ` |  | `d303ff80879e` |
| RankLab | beta 1k | 5,100 | `RankLab` |  | `892f35917605` |
| ResampLab | beta 1j | 3,060 | `ResampLab` |  | `cf3c85853b1b` |
| RiskLab | beta 1h | 3,169 | `RiskLab` |  | `f9a89623c5a8` |
| SampDist | v2.3k | 1,939 | `SampDist` |  | `2d44782aea01` |
| ScatterLab | beta 2m | 2,735 | `ScatterLab` |  | `cb8d938d95d0` |
| StatDist | v2.7n | 5,104 | `StatDist` |  | `20cbff4e1145` |
| StudRange | beta 15n | 2,757 | `StudRange` | MicroPython | `d9c08bcfdfd2` |
| SurvLab | beta 1g | 2,748 | `SurvLab` |  | `2d3c24497ee9` |
| TDist3D | beta 1b | 1,172 | `TDist3D` |  | `a903df8856aa` |
| TTestLabG | beta 1i | 2,188 | `TTESTLABG` |  | `c5565f10b084` |
| TTestLab | beta 1l | 2,221 | `TTESTLAB` |  | `a3df8bcb2c09` |
| TestChooser | beta 2h | 1,921 | `TestChooser` |  | `1d915ec15104` |
| TrendTest | beta 3n | 2,296 | `TrendTest` |  | `1414217194ee` |

*The checksum is the first 12 hex digits of SHA-256 over the program's source (line endings made LF, trailing blank lines dropped): the file in `programs/` it was built from. Every file in the zip was read back and matched its source before the zip was written.*

## Building it again

`python3 tools/make_starter_pack_v4.py v6 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a program changes. The tool names each file, checks the names, builds with hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)), builds the sample matrix from `data-loader/examples/rossi.csv`, reads every file back, and writes the zip and this page. With `--checked` it carries each program as the Virtual Calculator wrote it back after one Check there (the same source plus its compiled block), so students never Check; it stops if a checked file's source differs from `programs/`. Build without `--checked` first, load that pack on the Virtual Calculator, Check each changed program, close it, and copy those files into FOLDER. Move the older zip out of this folder.

*Free for educational and personal use. © 2026 Roger Metcalf.*
