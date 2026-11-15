# Starter pack v21: notes (15 November 2026)

Built by `tools/make_starter_pack_v4.py v21 --checked DIR` from `programs/`. The pack holds 31 programs; seven have new versions from round 15:

- ScatterLab beta 2l: a 95% confidence interval for ρ on the Inference page (`docs/changes/ScatterLab_beta2l_CHANGES.md`);
- FitCheck beta 1h: a standard error beside the skewness and the kurtosis, the credits in new words, and a closing summary for a sample in bins (`docs/changes/FitCheck_beta1h_CHANGES.md`);
- RankLab beta 1i, AnovaLab beta 1h and ResampLab beta 1i: the credits on their last help page in new words;
- ExhibitLab beta 1h and SurvLab beta 1g: the same in the comments at the top of the file; nothing the calculator runs is different.

The other twenty-four are v20's files.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 15 November 2026

- The calculator's folder was backed up first. The seven new files, built by the first pass of the builder (hp-prime-kit's `hpprime write`), were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed.
- Program Catalog > Edit > Check on each, from 01:27 to 01:36: "No errors in the program" seven times (`verify/round15/vc_checks.txt`).
- Nothing was run. The calculator was left by Calculator > Exit, so that it wrote its files back, and the seven checked files were collected then (a run leaves its values in the program's file: v6's notes).
- The programs were run afterwards, in another session, for their screens (`verify/round15/screens/`). That run showed FitCheck's closing summary "nothing computed" after a sample in bins, and FitCheck was changed. Its new file went the same way again: built by the first pass, copied in while the calculator was closed, Checked (02:07, "No errors in the program"), collected after Calculator > Exit without a run, and only then run, in a third session.
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31 (ScatterLab 250,032 bytes; FitCheck 329,180; RankLab 350,022; AnovaLab 354,124; ResampLab 275,770; ExhibitLab 255,416; SurvLab 249,450).
- The pack was built twice that night, before and after FitCheck's change. Only the second build is in the repository.

## The Prime Loader

`prime-loader/build_loader_v1s.py` built `PrimeLoader_v1s.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1s.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1s_output.txt`). The page's catalog names the seven new versions (it reads each one from `programs/`).

## Not done

No file of this pack has run on a G1 or a G2.
