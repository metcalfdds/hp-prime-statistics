# Starter pack for the Virtual Calculator

*v28, 2026-11-27. Built by `tools/make_starter_pack_v6.py` from `programs/` and `extras/sudoku/`; do not edit this page by hand.*

All 31 programs in one zip, ready for the free **HP Prime Virtual Calculator** on a Windows PC: no Connectivity Kit, no copying and pasting. Download **[HP_Prime_Statistics_Starter_Pack_v28.zip](https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack/HP_Prime_Statistics_Starter_Pack_v28.zip)** (one file).

*How this pack was tested on the Virtual Calculator: [docs/changes/StarterPack_v28_NOTES.md](../docs/changes/StarterPack_v28_NOTES.md).*

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

### Just for fun: the bonus
- The folder `Bonus (optional)` holds `Sudoku.hpprgm`, a bonus that is not one of the 31 *Statisticles*: Sudoku beta 2a, a Sudoku puzzle game that keeps a record of the games you finish for a class experiment. Copy it into the Prime folder too if you want it, in the same way (calculator closed).

### Good to know
- Windows asks before it replaces a file of the same name. Replacing it replaces that program on the calculator.
- On a real HP Prime (G1 or G2), send programs with the Connectivity Kit instead, a few at a time: copying files works only for the Virtual Calculator.
- Each program's source, its change notes and how it was tested are in the repository: programs/, docs/changes/ and verify/.

## What is in the pack

| Program | Version | Lines | In Home, type | Notes | Source checksum |
|---|---|---|---|---|---|
| AgreeLab | beta 1j | 3,082 | `AgreeLab` |  | `4885a4b6f4b9` |
| AnovaLab | beta 1k | 4,757 | `AnovaLab` |  | `93047636d994` |
| BayesTree | beta 8l | 3,459 | `BayesTree` |  | `662b2f03ad52` |
| BiNorm3D | beta 1h | 1,619 | `BiNorm3D` |  | `a5db3c5011b0` |
| BurrLab | beta 1s | 4,729 | `BurrLab` | MicroPython | `24554d605623` |
| CICatcher | beta 2n | 2,497 | `CICatcher` |  | `c610ccd89b15` |
| CentralLimit | beta 3h | 2,797 | (an app) | app on Statistics 1Var | `24949ed87538` |
| ChiTable | beta 3n | 3,871 | `ChiTable` |  | `946dce50fc6b` |
| DNAMixLR | beta 3k | 3,479 | `DNAMixLR` |  | `ed9460f9c0a1` |
| DataLoad | beta 1i | 1,255 | `DATALOAD` |  | `6f83fb5d4970` |
| EpiStats | v1.7o | 6,313 | `EpiStats` |  | `2be69e1b6486` |
| ErrorRate | beta 1k | 2,865 | `ErrorRate` | MicroPython | `53037de83357` |
| ExhibitLab | beta 1j | 2,911 | `ExhibitLab` |  | `6471fb20f894` |
| FitCheck | beta 1k | 3,914 | `FitCheck` |  | `855820754fe0` |
| GaltonBoard | beta 3j | 2,541 | `GaltonBoard` | MicroPython | `7173586c8ea5` |
| Norm3 | v2.4h | 1,133 | `Norm3` |  | `0a644261e6c6` |
| NormExplorer | beta 42k | 4,239 | `NormExp` | MicroPython | `48a4573263bf` |
| PowerViz | v2.5v | 4,219 | `POWERVIZ` |  | `d1ceb40f1d2d` |
| RankLab | beta 1l | 5,108 | `RankLab` |  | `cd906c514ab4` |
| ResampLab | beta 1k | 3,068 | `ResampLab` |  | `5074256911d9` |
| RiskLab | beta 1i | 3,177 | `RiskLab` |  | `448d57749b73` |
| SampDist | v2.3l | 1,947 | `SampDist` |  | `9f69769a3b6d` |
| ScatterLab | beta 2n | 2,743 | `ScatterLab` |  | `e50845657e92` |
| StatDist | v2.7p | 5,146 | `StatDist` |  | `cd58c256c25f` |
| StudRange | beta 15o | 2,768 | `StudRange` | MicroPython | `be030e8fa547` |
| SurvLab | beta 1h | 2,756 | `SurvLab` |  | `65170376689c` |
| TDist3D | beta 1c | 1,180 | `TDist3D` |  | `29c46c2c9f7b` |
| TTestLabG | beta 1j | 2,197 | `TTESTLABG` |  | `5ad8d9440a4c` |
| TTestLab | beta 1m | 2,229 | `TTESTLAB` |  | `734cf93a6dbd` |
| TestChooser | beta 2i | 1,929 | `TestChooser` |  | `6fc473d7b3c8` |
| TrendTest | beta 3o | 2,304 | `TrendTest` |  | `afeff2d82379` |
| Sudoku | beta 2a | 1,962 | `Sudoku` | bonus, in `Bonus (optional)` (not one of the *Statisticles*) | `33b00ac430c8` |

*The checksum is the first 12 hex digits of SHA-256 over the program's source (line endings made LF, trailing blank lines dropped): the file in `programs/` (or, for the bonus, `extras/sudoku/`) it was built from. Every file in the zip was read back and matched its source before the zip was written.*

## Building it again

`python3 tools/make_starter_pack_v6.py v28 --kit PATH_TO_hp-prime-kit --checked FOLDER` after a program changes. The tool names each file, checks the names, builds with hp-prime-kit (MIT, [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)), builds the sample matrix from `data-loader/examples/rossi.csv`, reads every file back, and writes the zip and this page. With `--checked` it carries each program as the Virtual Calculator wrote it back after one Check there (the same source plus its compiled block), so students never Check; it stops if a checked file's source differs from `programs/`. Build without `--checked` first, load that pack on the Virtual Calculator, Check each changed program, close it, and copy those files into FOLDER. Move the older zip out of this folder.

*Free for educational and personal use. © 2026 Roger Metcalf.*
