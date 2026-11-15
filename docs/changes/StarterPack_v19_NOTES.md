# Starter pack v19: notes (14 November 2026, evening)

Built by `tools/make_starter_pack_v4.py v19 --checked DIR` from `programs/`. The pack holds 31 programs; two have new versions from round 14: ScatterLab beta 2k (a page that tests the slope, two 95% bands, Anscombe's quartet; `docs/changes/ScatterLab_beta2k_CHANGES.md`) and CICatcher beta 2k (a wording fix on help pages 2 and 6; `docs/changes/CICatcher_beta2k_CHANGES.md`). The other twenty-nine are v18's checked files, unchanged.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 14 November 2026

- The calculator's folder was backed up first. The two new files, built by the first pass of the builder (hp-prime-kit's `hpprime write`), were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed.
- Program Catalog > Edit > Check on each: "No errors in the program" (`verify/round14/vc_checks.txt`).
- Nothing was run. The calculator was left by Calculator > Exit, so that it wrote its files back, and the two checked files were collected then (a run leaves its values in the program's file: v6's notes). ScatterLab was run afterwards, in a second session, for its screens; that session's files are not in the pack.
- The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31 (CICatcher 187,454 bytes, ScatterLab 244,624).

## The Prime Loader

`prime-loader/build_loader_v1q.py` built `PrimeLoader_v1q.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1q.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1q_output.txt`).

## Not done

No file of this pack has run on a G1 or a G2.
