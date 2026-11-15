# Starter pack v20: notes (14 November 2026, night)

Built by `tools/make_starter_pack_v4.py v20 --checked DIR` from `programs/`. The pack holds 31 programs; two have new versions from round 14, part 2: TTestLab beta 1k (the one-sample *t*-test and the one- and two-proportion *z*-tests; `docs/changes/TTestLab_beta1k_CHANGES.md`) and TTestLabG beta 1h (the general version, built from it; `docs/changes/TTestLabG_beta1h_CHANGES.md`). The other twenty-nine are v19's files.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 14 November 2026

- The calculator's folder was backed up first. The two new files, built by the first pass of the builder (hp-prime-kit's `hpprime write`), were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed.
- Program Catalog > Edit > Check on each, at 22:02: "No errors in the program" (`verify/round14/vc_checks.txt`).
- Nothing was run. The calculator was left by Calculator > Exit, so that it wrote its files back, and the two checked files were collected then (a run leaves its values in the program's file: v6's notes). Both programs were run afterwards, in another session, for their screens; that session's files are not in the pack.
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31 (TTestLab 209,289 bytes, TTestLabG 206,515).
- The pack was built three times that night. The first build's TTestLabG had nine items in its start menu, and the Virtual Calculator cut the ninth off at the bottom of the screen. The second build's programs let a huge Cohen's *d* run into the label beside it (the label monkey; beta 1j did too). After each change both programs were Checked again and packed again. Only the third build is in the repository.

## The Prime Loader

`prime-loader/build_loader_v1r.py` built `PrimeLoader_v1r.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1r.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1r_output.txt`). Chapter 9 now lists TTestLabG. The build now reads each program's version from `programs/`; v1q's table still named an older version for 14 programs (in the page's data only).

## Not done

No file of this pack has run on a G1 or a G2.
