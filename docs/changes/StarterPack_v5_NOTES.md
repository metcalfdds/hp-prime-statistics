# Starter pack v5: notes (1 November 2026)

*The pack: `starter-pack/HP_Prime_Statistics_Starter_Pack_v5.zip`, built by `tools/make_starter_pack_v4.py v5 --checked FOLDER` from the 30 programs in `programs/`. v1 to v4 (31 October): `StarterPack_v1_NOTES.md` to `StarterPack_v4_NOTES.md`.*

## What changed from v4: no Check

Every program in v5 is a **checked file**: the file the Virtual Calculator itself wrote back after the program was Checked once there. It holds the same source plus the calculator's compiled block. A student who installs v5 taps a program and Runs it, with nothing to check first. `READ_ME_FIRST.txt` and `starter-pack/README.md` now say "Run a program" in place of "The first time you run each program". They keep Check only as a fallback, in case a different version of the Virtual Calculator wants to compile again.

The programs and their sources are v4's. Only the files differ: each is larger by its compiled block, from +1,480 bytes (Norm3) to +60,222 (BurrLab). The sample matrix is byte for byte v4's.

Roger's aim is to make the Prime and the Virtual Prime very easy for uninterested college students to use with the proposed stats book. The Check step was the one that would lose them: 30 trips through Program Catalog → Edit → Check.

## The measurement (Virtual Calculator 2.4.2, build 2026-09-09, calculator `Prime`, Rogers-HP; by Claude through computer use)

The calculator's folder held all 29 programs as checked files after the 31 October runs (each larger than its pack v4 file). hp-prime-kit had measured only files without a block, which need Check (`deploy.compile-once-after-a-file-copy`); nobody had tried a file with one.

1. **Step A: make it forget.** With the calculator closed, `TTestLabG.hpprgm` (checked, 114,646 bytes) was moved out of the folder, and `ResampLab.hpprgm` was replaced by its unchecked pack v4 file (232,684 bytes), as a control. The calculator was started:
   - TTestLabG was gone from the Program Catalog;
   - `TTESTLABG` pasted into Home and entered **started TTestLab**, the advanced version. Home read the unknown name as `TTESTLAB*G`, and the run ended "Error: Bad argument type". That trap probably also explains 31 October's "the last letter was dropped" (TTestLabG_beta1_NOTES.md).

   Then the calculator was closed (Calculator menu → Exit).
2. **Step B: the checked file.** The checked `TTestLabG.hpprgm` was copied back in and the calculator started. With **no Check**, `TTESTLABG` in Home opened TTestLabG's start menu at once ("TTestLabG: t tests in 5 steps"). Example 2, Darwin's plants, ran: step 1 as on 31 October. Esc ended it with "TTestLabG: t(14) = 2.15, p = 0.050, two-tailed".
3. **The control.** `ResampLab` in Home, from its unchecked file, gave **"Error: Syntax Error"**, as an unchecked file always does.

A checked file therefore carries what the calculator needs: copied into a calculator that does not know the program, it runs at once.

## The checked files

- **Where they came from.** 29 were in the Virtual Calculator's folder from the 31 October runs, each loaded from a pack (v1 to v4) and Checked there. They were collected on 1 November, ResampLab's from the copy kept before the control.
- **TTestLab.** Its file on the calculator was the one that ran on 31 October, whose header differs from beta 1b's in two comment lines (`StarterPack_v4_NOTES.md`). So beta 1b's exact file from pack v4 was copied in, opened, Checked ("No errors in the program") and collected after Exit.
- **Checked against the source.** `make_starter_pack_v4.py --checked` reads the source out of each checked file with hp-prime-kit and requires it to equal `programs/<file>.txt` (line endings and trailing blank lines aside). All 30 did. A first run with TTestLab's old file stopped, as it should: "the checked file TTestLab.hpprgm holds a different source from TTestLab_beta1b". The tool also stops if a file carries no compiled block.
- **The app.** For CentralLimit only the program file, `CentralLimit.hpappprgm` (checked, +14,968 bytes), comes from the calculator. Its descriptor `CentralLimit.hpapp` and note are built from `tools/CentralLimit_app_base_v1.hpapp` as before. The calculator's own descriptor differs from the base at byte 93, because it holds the app's saved state, which should not be shipped to students.

## Checks

The tool's name check passed. The programs are v4's, so v4's fleet-name check stands (`fleet_names_v2.py programs/*.txt`: 30 files, 2,251 routine names, 0 collisions). Every file was read back. The pack is 1.45 MB zipped. v4's zip and README and the v3 tool are in the author's `_superseded_2026-11-01` folder.

## Also measured on 1 November (Rogers-HP, by Roger)

- **Windows' Extract All, the Prime Loader's Firefox route.**
  - A zip holding SampDist's checked file was put in Downloads. Extract All → Browse → Documents → HP Prime → Calculators → Prime showed `C:\Users\metca\Documents\HP Prime\Calculators\Prime`, with no folder named after the zip.
  - After Extract, `SampDist.hpprgm` sat in the Prime folder itself, and the calculator listed it.
  - (The no-Check run that followed is void: tapping a name in the Program Catalog opens its editor, and the next press landed on the editor's Check.)
- **The Connectivity Kit.**
  - With the Kit and the Virtual Calculator both running, dragging `Norm3.hpprgm` onto **Virtual Prime** in the Kit's Calculators list installed it, and Norm3 ran (Program Parameters: mu, sd, x₀).
  - The drag's label read "Move", but the file stayed in its folder.
  - Roger: the same drag works for the G1 and G2. A program sent by the Kit is compiled by the calculator as it arrives (hp-prime-kit, `deploy.no-manual-compile`, measured on a G2), so checked files matter only for copying into the Virtual Calculator's folder.
- **Dropping a file onto the Virtual Calculator's own window** was refused (the "no" cursor).

## Pack v5's files through the Prime Loader (1 November 2026, 08:59-09:03)

Roger opened `PrimeLoader_v1b.html` in Edge, picked chapter 7 and clicked Load. The page moved the six programs then on the calculator to `Loader backups\2026-11-01 0859` and wrote SampDist, GaltonBoard and the CentralLimit app, each byte for byte pack v5's. Claude then started the calculator: its Program Catalog listed GaltonBoard and SampDist; `GaltonBoard` and `SampDist` typed in Home ran at once (the board; the Sampling Distribution menu); CentralLimit, started from Apps, showed its welcome page and then its own Views menu. **Nothing was checked.** So the app, with its base descriptor and its checked program, works, and three more programs ran from checked files with no Check.

## Not yet

- Pack v5 as a whole on a fresh calculator, each program run by name with no Check. TTestLabG, GaltonBoard, SampDist and CentralLimit are the measured cases; the other 26 carry blocks of the same kind, written by the same calculator the same way.
- A Virtual Calculator of another version, and the Mac build. Whether a block written by 2.4.2 suits another version is not known; the instructions' fallback (Check once) covers it.
