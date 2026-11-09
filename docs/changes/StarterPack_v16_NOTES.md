# Starter pack v16: notes (9 November 2026)

Built by `tools/make_starter_pack_v4.py v16 --checked DIR` from `programs/`. The pack holds 31 programs, all with new versions from round 11, the help pages in plain words (`docs/changes/<Name>_<version>_CHANGES.md`; `verify/round11/`). DIR was the Virtual Calculator's own folder in the cloud workspace (Wine; Lessons Learned v7zm). Each file was copied in while the calculator was closed, Checked once, and written back when the calculator was closed with Calculator > Exit. The builder read the source back out of every checked file, and all 31 are the same as `programs/`.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 9 November 2026

- The 31 files were built by hp-prime-kit's `hpprime write` (the app by `hpprime build` on `tools/CentralLimit_app_base_v1.hpapp`). They were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed.
- Program Catalog > Edit > Check on each of the 30 programs: "No errors in the program" for all 30 (`verify/round11/vc_checks.txt`).
- RiskLab beta 1f and ResampLab beta 1h were rebuilt after their opening screens' dates were set to 9 Nov 2026, copied in again, and Checked again: no errors.
- The CentralLimit app's program is in the Program Catalog only while CentralLimit is the current app. It was started from the Application Library (Apps, the CentralLimit icon, Start); "CentralLimit (App)" then headed the catalog, and Check said "No errors in the program".
- The help pages of ChiTable, BayesTree, StudRange, BurrLab and AgreeLab were opened from their menus and read: every line inside its page (`verify/round11/screens/`). A run leaves its values in the program's file (v6's notes), so fresh copies of ChiTable, BayesTree, StudRange and BurrLab were copied in, Checked again with no run, and those are the files in the pack. AgreeLab's checked file had been collected before it was run.
- TTestLab beta 1i, TTestLabG beta 1g and StudRange beta 15m were rebuilt once more after "t crit" and "q crit" were kept whole on one line, copied in, and Checked again with no run: no errors.
- Each Check added the calculator's compiled block (the builder's "checked (+N)" column; BurrLab +60,574 bytes, EpiStats +27,204).

## The Prime Loader

`prime-loader/build_loader_v1n.py` built `PrimeLoader_v1n.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1n.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1n_output.txt`).
