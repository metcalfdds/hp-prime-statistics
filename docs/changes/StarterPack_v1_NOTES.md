# Starter pack v1: notes and the Virtual Calculator test (31 October 2026)

*Added the same night: v1's zip and `tools/make_starter_pack_v1.py` were replaced by v2 (`StarterPack_v2_NOTES.md`) before they were committed, so neither is in this repository's history; the tool is in the author's `_superseded_2026-10-31` folder. Every program file in v2 is byte for byte the v1 file tested below.*

*The pack: `starter-pack/HP_Prime_Statistics_Starter_Pack_v1.zip`, built by `tools/make_starter_pack_v1.py v1` from the 28 programs in `programs/` as of this commit. The why and the general findings are in Lessons Learned v7zb (`docs/lessons-learned_v7zb.md`, its "What changed" block and §16).*

## Why

Roger: "I like the idea of students getting the Virtual Calculator to use--but I don't think many will want to deal with the connectivity kit and so forth--I wish we could just load up a version of the Virtual Prime with the programs already loaded". The Virtual Calculator keeps its programs as files in its own folder (`Documents\HP Prime\Calculators\Prime`) and reads that folder when it starts. So a student who copies files into it, while it is closed, has the programs the next time it opens. The pack is those files, in one zip, with plain instructions.

## What is in it

- `Copy these into Prime/`: 27 `.hpprgm` files and `CentralLimit.hpappdir`. Each file is named as the program is on Roger's calculators: the source file's name up to `_beta` or `_v`.
- `READ_ME_FIRST.txt`: the instructions and the list of versions, in plain text for Notepad.
- `starter-pack/README.md`: the same instructions and a table of versions, line counts and source checksums. The tool writes it.

## How it is built

- **Programs:** hp-prime-kit's `hpprime write SRC.txt -o NAME.hpprgm` (MIT, JordiRigau/hp-prime-kit) puts the source into a copy of a Connectivity Kit container.
- **CentralLimit:** `hpprime build CentralLimit --ppl CentralLimit_beta3d.txt --base tools/CentralLimit_app_base_v1.hpapp`. The base is the 1,350-byte descriptor of Roger's working CentralLimit app on the Virtual Calculator: a user copy of Statistics 1Var whose H1 is D1. It carries no text except "D1". Its note file is the kit's empty one, the same two bytes as Roger's.
- **Read-back:** `hpprime read` pulls the source back out of every built file, and the build stops unless it equals the `.txt` (line endings and trailing blank lines aside). All 28 matched. `hpprime build --check` on the app folder: 0 differences.
- **Names:** before building, the tool stops if two programs would get one name, if a name is a Prime built-in, or if it is a routine or EXPORT name in another program, ignoring case. None did. `tools/fleet_names_v2.py programs/*.txt`: 28 files, 2,159 routine names, 0 collisions. `tools/case_scan_v1.py 'programs/*.txt'`: nothing to report. The five `#PYTHON` blocks have five different names (`bul`, `erlPySim`, `gbPyDrop`, `SAMPBINSPY`, `srq`).
- **Size:** 1.35 MB zipped; the files inside total about 7 MB.

## The test on the Virtual Calculator (31 October 2026, Rogers-HP, by Claude through computer use)

Virtual Calculator 2.4.2, 64-bit, build 2026-09-09, calculator `Prime`.

1. The calculator was closed (Calculator menu → Exit). The program files already in its folder (BurrLab, NormExplorer, PowerViz, TTestLab, TestChooser and the CentralLimit app) were moved aside to `Documents\HP Prime\_set_aside_2026-10-31\vc_before_starter_pack_v1`. Nothing was deleted.
2. The zip's `Copy these into Prime` folder was extracted into `Documents\HP Prime\Calculators\Prime`: 30 files.
3. **Started the calculator.** The Program Catalog listed all 28: CentralLimit (App) first, then the 27 programs.
4. **Before Check**, using ChiTable:
   - typing `ChiTable` in Home gave "Error: Syntax Error";
   - the catalog's Run did nothing (pressed twice, about 0.3 s each).
5. **Check:** Edit → Check gave "No errors in the program" for every one of the 28, the app included. Each editor's title named the program.
   - Checked programs moved to the top of the catalog, under the app, and their sizes grew by the compiled block (ChiTable 325 KB → 345 KB, BurrLab 360 KB → 419 KB).
6. **After Check:** Run opened ChiTable's menu ("χ² for a two-way table"). Esc left it with "ChiTable: no table". `ChiTable` typed in Home ran it too.
7. **CentralLimit:** it was in the Application Library. Apps → Start showed its welcome page. View then showed its own Views menu (CLT dashboard, Choose population, Draw samples, …).
8. **Earlier the same evening**, the same build of two of these files ran in full:
   - TTestLab: the start menu, then the age-at-arrest example to step 5. It exited with "TTestLab: t(73) = −2.20, p = 0.031, two-tailed".
   - BurrLab: the fit on the BJS months-served preset ran in MicroPython ("engine: MicroPython 1.9.4, 0.0 s"; C = 10.84, SE 3.596; K = 0.8981; S = 150.1; ln L = −191.14; AIC 388.27).

**Not tested:**
- Running every program past its first screen. A program's own checklist in `docs/changes/` is still the device test.
- A computer that has never run the Virtual Calculator. The folder is said to be made at first start (hp-prime-kit, `docs/topics/deploy.md`); the instructions ask for one start and exit first.
- The Mac and Linux builds of the Virtual Calculator, and a G1 or G2: on a real calculator the Connectivity Kit is still the way.
- The `READ_ME_FIRST.txt` steps by someone other than us.

## Observed once, not yet repeated

On the Virtual Calculator, right after an example was chosen from TTestLab's start menu, the first tap on a soft key was ignored; the second worked. Recorded for TTestLab's device checklist.

## Unresolved

- Whether `hpcalc.org` remains the place to send students for the Virtual Calculator. HP's own download page was not found in this session. hpcalc.org lists the 64-bit Virtual Calculator 2.4.2 (2026-09-09) with Hewlett-Packard as author.
- Whether to also attach the zip to a GitHub release, so that the link never changes. For now the link names the version, and each new pack gets the next number.
