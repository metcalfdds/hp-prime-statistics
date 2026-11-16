# Starter pack v22: notes (15 November 2026)

Built by `tools/make_starter_pack_v4.py v22 --checked DIR` from `programs/`. The pack holds 31 programs; nine have new versions from round 16:

- AnovaLab beta 1i: Dunnett's test, every group against one control, with a table and a plot; numbers no longer cut by their places (`docs/changes/AnovaLab_beta1i_CHANGES.md`);
- RankLab beta 1j: Page's *L* for an ordered trend, and a runs test for randomness (`docs/changes/RankLab_beta1j_CHANGES.md`);
- FitCheck beta 1i: Dixon's outlier test for a small sample (`docs/changes/FitCheck_beta1i_CHANGES.md`);
- CICatcher beta 2l: tolerance intervals, with the exact factor (`docs/changes/CICatcher_beta2l_CHANGES.md`);
- BiNorm3D beta 1g: a target view with the circular error probable (`docs/changes/BiNorm3D_beta1g_CHANGES.md`);
- StatDist v2.7n, AgreeLab beta 1h, RiskLab beta 1h and BurrLab beta 1r: their headers say, in plain verbs, what was done with the programs they stand beside; nothing the calculator runs is different but the version three of them show.

The other twenty-two are v21's files.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 15 November 2026

The calculator is the one in the cloud workspace, HP's program under Wine (`tools/vc_cloud_v1/`). It was stood up again that evening, because a restart of the workspace had removed the earlier one.

- **First round of Checks.** The nine new files, built by the first pass of the builder (hp-prime-kit's `hpprime write`), were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed. Program Catalog > Edit > Check on each, from 21:35 to 21:39: "No errors in the program" nine times. Nothing was run. The calculator was left by Calculator > Exit, so that it wrote its files back, and the nine checked files were collected then (a run leaves its values in the program's file: v6's notes).
- **The runs** came afterwards, in other sessions, for the programs' screens (`verify/round16/screens/`). They found two faults, a menu title cut at 31 characters in AnovaLab and a closing line too long for its box in CICatcher (`verify/round16/vc_checks.txt`, section 3). Both programs were changed.
- **Second round.** The two new files went the same way: built by the first pass, copied in while the calculator was closed, Checked (22:27, "No errors in the program" twice), collected after Calculator > Exit without a run, and only then run.
- **Third round.** While the change notes were written, five sentences in the comments of BiNorm3D, CICatcher and RankLab were corrected. A checked file holds its whole source, comments included, so the three were Checked once more (23:26, "No errors in the program" three times) and collected after Calculator > Exit without a run. Not one line the calculator runs differs from the files that were run.
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31 (AnovaLab 434,672 bytes; RankLab 474,154; FitCheck 386,642; CICatcher 216,400; BiNorm3D 157,704; StatDist 471,872; AgreeLab 285,014; RiskLab 286,504; BurrLab 467,948).
- The pack was built three times that night, once after each round. Only the last build is in the repository.

## The Prime Loader

`prime-loader/build_loader_v1t.py` built `PrimeLoader_v1t.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1t.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1t_output.txt`). The page's catalog names the nine new versions (it reads each one from `programs/`).

One line of the test differs from v1s's, and the page does not. The Chromium of the cloud workspace (Chrome for Testing 153.0.8010.12, Playwright 1.63) ends with SIGTRAP when a folder handle is read back from IndexedDB, which is how the page remembers the calculator's folder between visits. The test now stores the handle's name in its place, by a few lines run before the page's own script, and says so at its top; `tests/idb_handle_probe_v1.js` shows the crash by itself, with no page of ours. Whether Chrome or Edge on a person's computer, with a folder picked from the disk, does the same is not known. To find out: load a chapter with the page, close the tab, open the page in a new tab, and load another chapter. If the page offers the folder again, it remembered.

## Not done

No file of this pack has run on a G1 or a G2.
