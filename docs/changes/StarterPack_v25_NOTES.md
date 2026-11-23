# Starter pack v25: notes (23 November 2026)

Built by `tools/make_starter_pack_v4.py v25 --checked DIR` from `programs/`. The pack holds 31 programs; two have new versions from round 19 (`verify/round19/README.md`):

- StatDist v2.7p: the Formula page (CAS) asks the CAS only with parameters that keep it quick (Student's t when 2 df is a whole number, Fisher F when df1 and df2 are whole, Burr XII when C and K are whole), and otherwise says so in a gray line.
- EpiStats v1.7o: the stratified rates grid takes a person-time of 0, or from 1 to 100,000, and refuses one between 0 and 1 with a sentence that says so.

Every other file of the pack is v24's byte for byte (compared file by file): the other 29 programs' checked files, the app and the sample matrix. READ_ME_FIRST.txt differs only in three lines: the pack's version and date, and the versions of StatDist and EpiStats in its table.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 23 November 2026

The calculator is the one in the cloud workspace, HP's program under Wine (`tools/vc_cloud_v1/`). The record is `verify/round19/vc_record.txt`.

- **The Checks.** The two new files, built by the first pass of the builder, were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed. Program Catalog > Edit > Check said "No errors in the program" for EpiStats at 09:20:10 and for the final StatDist at 09:33:42 (an earlier build of StatDist was Checked at 09:19:52 and then changed; its file was not used). Nothing was run before the calculator was closed by Calculator > Exit and the two files copied out.
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31.
- **The runs** came afterwards, in another session of the calculator: StatDist's Formula page for F at 7 and 17.83 and for Burr XII at 2.5, 3.5 and 1.5 (the gray line, in 3 s or less), and EpiStats' stratified rates grid refusing 0.5 as a person-time in both of its forms.

## The Prime Loader

`prime-loader/build_loader_v2o.py` built `PrimeLoader_v2o.html` from this pack: 31 of 31 files checked. `tests/test_loader_v2o.js`: see `tests/test_loader_v2o_output.txt`. The page is v2n's, word for word.

## Not done

No file of this pack has run on a G1 or a G2.
