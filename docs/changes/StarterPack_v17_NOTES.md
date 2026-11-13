# Starter pack v17: notes (13 November 2026)

Built by `tools/make_starter_pack_v4.py v17 --checked DIR` from `programs/`. The pack holds 31 programs; twelve have new versions from round 12, help-page fixes that the book's pre-submission read found (AnovaLab beta 1g, BayesTree beta 8k, CICatcher beta 2j, DataLoad beta 1g, EpiStats v1.7l, FitCheck beta 1g, PowerViz v2.5s, RankLab beta 1h, RiskLab beta 1g, SampDist v2.3k, StatDist v2.7m, TTestLab beta 1j; `docs/changes/<Name>_<version>_CHANGES.md`; `verify/round12/`). The other nineteen are v16's, and their checked files are v16's. DIR was the Virtual Calculator's own folder in the cloud workspace (Wine; Lessons Learned v7zm).

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 13 November 2026

- The calculator's folder was backed up first. The twelve new files, built by the first pass of the builder (hp-prime-kit's `hpprime write`), were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed.
- Program Catalog > Edit > Check on each of the twelve: "No errors in the program" for all twelve (`verify/round12/vc_checks.txt`).
- The help pages of AnovaLab (page 4/9: "Scheffé", with CHAR(233)) and SampDist (pages 1/2 and 2/2, laid out as lists again) were opened from their menus and read: the é is drawn as an accented e, and every line is inside its page (`verify/round12/screens/`). A run leaves its values in the program's file (v6's notes), so fresh copies of AnovaLab and SampDist were copied in, Checked again with no run, and those are the files in the pack.
- RankLab beta 1h was changed once more after these Checks: the monkey found a fault in Your data > Groups (`verify/round12/README.md`, "The monkey's finding"). The fixed file was copied in while the calculator was closed and Checked: "No errors in the program" (`verify/round12/screens/RankLab_check_after_fix_r12.png`), and the pack carries that file. Nothing was run.
- The calculator was left by Calculator > Exit, so that it wrote its files back. The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31.

## The Prime Loader

`prime-loader/build_loader_v1o.py` built `PrimeLoader_v1o.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1o.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1o_output.txt`).
