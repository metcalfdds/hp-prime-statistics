# Starter pack v24: notes (22 November 2026)

Built by `tools/make_starter_pack_v4.py v24 --checked DIR` from `programs/`. The pack holds 31 programs, and all 31 have new versions from round 18, in which each program got one line that sets the book's four Home settings when it starts (`verify/round18/README.md`):

- AgreeLab beta 1j, AnovaLab beta 1k, BayesTree beta 8l, BiNorm3D beta 1h, BurrLab beta 1s, CICatcher beta 2n, CentralLimit beta 3h, ChiTable beta 3n, DNAMixLR beta 3k, DataLoad beta 1h, EpiStats v1.7n, ErrorRate beta 1k, ExhibitLab beta 1j, FitCheck beta 1k, GaltonBoard beta 3j, Norm3 v2.4h, NormExplorer beta 42k, PowerViz v2.5u, RankLab beta 1l, ResampLab beta 1k, RiskLab beta 1i, SampDist v2.3l, ScatterLab beta 2n, StatDist v2.7o, StudRange beta 15o, SurvLab beta 1h, TDist3D beta 1c, TTestLab beta 1m, TTestLabG beta 1j, TestChooser beta 2i and TrendTest beta 3o.

No file of v23 is carried over. The sample matrix is the same.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 22 November 2026

The calculator is the one in the cloud workspace, HP's program under Wine (`tools/vc_cloud_v1/`). The record is `verify/round18/vc_checks.txt`.

- **The Checks.** The 31 new files, built by the first pass of the builder (hp-prime-kit's `hpprime write`), were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed. Program Catalog > Edit > Check on each, from 17:36 to 18:05: "No errors in the program" 31 times, and nothing was run. CentralLimit's program is in the catalog only while CentralLimit is the current app: it was started from the Application Library, where an app whose program has not been checked opens in its Numeric view and its `START` does not run. The calculator was left by its Exit, and the files were collected.
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31.
- **The runs** came afterwards, from 18:07 to 18:59, in another session of the calculator: each of the 31 started with the calculator just left in RPN entry, with a comma as the decimal point, Fixed 2 and Degrees. Each showed its own first page, and Home Settings afterwards read Radians, Standard, 123,456.789 and Textbook. The pack's files are the ones collected before these runs, so none carries a run's values.

## The Prime Loader

`prime-loader/build_loader_v2n.py` built `PrimeLoader_v2n.html` from this pack: 31 of 31 files checked. `tests/test_loader_v2n.js`: 161 PASS, 0 FAIL in Chromium (`tests/test_loader_v2n_output.txt`). The page's catalog names the 31 new versions (it reads each one from `programs/`), and no group is over 1,300,000 characters: the largest is 1,208,700.

## Not done

No file of this pack has run on a G1 or a G2.
