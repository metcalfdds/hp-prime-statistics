# Starter pack v25: notes (23 November 2026)

Built by `tools/make_starter_pack_v4.py v25 --checked DIR` from `programs/`. The pack holds 31 programs; three have new versions from round 19 (`verify/round19/README.md`):

- StatDist v2.7p: the Formula page (CAS) asks the CAS only with parameters that keep it quick (Student's t when 2 df is a whole number, Fisher F when df1 and df2 are whole, Burr XII when C and K are whole), and otherwise says so in a gray line.
- EpiStats v1.7o: the stratified rates grid takes a person-time of 0, or from 1 to 100,000, and refuses one between 0 and 1 with a sentence that says so.
- PowerViz v2.5v: Cohen's h is right whatever unit the calculator's trigonometry is in; v2.5u showed "h = 11.54, large" for 0.20 when the current app (the *Solve* app, in the book's new bloodstain example) had its own Angle Measure set to Degrees.

The pack was first built that morning with the first two; at 12:56 it was built again, with PowerViz's checked file in place of v24's, and the two builds differ in PowerViz's file and one line of READ_ME_FIRST.txt only (compared file by file).

Every other file of the pack is v24's byte for byte (compared file by file): the other 28 programs' checked files, the app and the sample matrix. READ_ME_FIRST.txt differs only in four lines: the pack's version and date, and the versions of StatDist, EpiStats and PowerViz in its table.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 23 November 2026

The calculator is the one in the cloud workspace, HP's program under Wine (`tools/vc_cloud_v1/`). The record is `verify/round19/vc_record.txt`.

- **The Checks.** The two new files, built by the first pass of the builder, were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed. Program Catalog > Edit > Check said "No errors in the program" for EpiStats at 09:20:10 and for the final StatDist at 09:33:42 (an earlier build of StatDist was Checked at 09:19:52 and then changed; its file was not used). Nothing was run before the calculator was closed by Calculator > Exit and the two files copied out.
- **PowerViz**, built by a first pass of the builder at 12:53, was copied in while the calculator was closed; Program Catalog > Edit > Check said "No errors in the program" at 12:54:52, and nothing ran before Calculator > Exit and the copy out.
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31.
- **The runs** came afterwards, in other sessions of the calculator: StatDist's Formula page for F at 7 and 17.83 and for Burr XII at 2.5, 3.5 and 1.5 (the gray line, in 3 s or less), EpiStats' stratified rates grid refusing 0.5 as a person-time in both of its forms, and PowerViz's One Proportion test showing "h = 0.20, small" with the *Solve* app set to Degrees.

## The Prime Loader

`prime-loader/build_loader_v2o.py` built `PrimeLoader_v2o.html` from this pack: 31 of 31 files checked. `tests/test_loader_v2o.js`: see `tests/test_loader_v2o_output.txt`. The page is v2n's, word for word.

## Not done

No file of this pack has run on a G1 or a G2.
