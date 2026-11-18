# Starter pack v23: notes (17 November 2026)

Built by `tools/make_starter_pack_v4.py v23 --checked DIR` from `programs/`. The pack holds 31 programs; sixteen have new versions from round 17, in which only words on the screen changed (`verify/round17/README.md`):

- AgreeLab beta 1i, AnovaLab beta 1j, CICatcher beta 2m, EpiStats v1.7m, ExhibitLab beta 1i, FitCheck beta 1j, PowerViz v2.5t, RankLab beta 1k, ResampLab beta 1j, ScatterLab beta 2m, StudRange beta 15n, TDist3D beta 1b, TTestLab beta 1l, TTestLabG beta 1i, TestChooser beta 2h and TrendTest beta 3n: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values, p-value with a small p), and an expression like n - 1 stands in parentheses of its own (df = (n - 1), (k - 1) df). Each has its change note, `docs/changes/<Name>_<version>_CHANGES.md`.

The other fifteen are v22's files.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 17 November 2026

The calculator is the one in the cloud workspace, HP's program under Wine (`tools/vc_cloud_v1/`).

- **The Checks.** The sixteen new files, built by the first pass of the builder (hp-prime-kit's `hpprime write`), were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed. Program Catalog > Edit > Check on each, from 12:33 to 12:45: "No errors in the program" sixteen times. Nothing was run. The calculator was left by Calculator > Exit, so that it wrote its files back, and the sixteen checked files were collected then (a run leaves its values in the program's file: v6's notes).
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31 (AgreeLab 286,252 bytes; AnovaLab 436,736; CICatcher 217,518; EpiStats 607,992; ExhibitLab 256,678; FitCheck 389,304; PowerViz 380,991; RankLab 475,264; ResampLab 276,868; ScatterLab 251,122; StudRange 261,091; TDist3D 113,794; TTestLab 210,617; TTestLabG 208,089; TestChooser 173,110; TrendTest 225,714). The pack is 1,665,290 bytes.
- **The runs** came afterwards, from 13:18 to 13:28, in another session of the calculator: TTestLab and ScatterLab for the book's two pictures, PowerViz and TDist3D for the three changed lines with the least room. All five lines stand whole, each ending 1 to 2 px short of where the glyph widths had put it (`verify/round17/vc_checks.txt`, section 3; `verify/round17/screens/`). The files the calculator wrote back after those runs are not in the pack.

## The Prime Loader

`prime-loader/build_loader_v1u.py` built `PrimeLoader_v1u.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1u.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1u_output.txt`). The page's catalog names the sixteen new versions (it reads each one from `programs/`), and `prime-loader/index.html` sends the browser on to the new page. The build script and the test are v1t's but for their names and the version they write.

## Not done

No file of this pack has run on a G1 or a G2.
