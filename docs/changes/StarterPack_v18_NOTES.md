# Starter pack v18: notes (13 November 2026, evening)

Built by `tools/make_starter_pack_v4.py v18 --checked DIR` from `programs/`. The pack holds 31 programs; one has a new version from round 13: ChiTable beta 3m, the exact test for its 2 × 3 and 3 × 2 tables (`docs/changes/ChiTable_beta3m_CHANGES.md`; `verify/round13/`). The other thirty are v17's, and their checked files are v17's. DIR was the Virtual Calculator's own folder in the cloud workspace (Wine; Lessons Learned v7zm).

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 13 November 2026

- The calculator's folder was backed up first. ChiTable beta 3m, built by the first pass of the builder (hp-prime-kit's `hpprime write`), was copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed.
- Program Catalog > Edit > Check: "No errors in the program" (`verify/round13/vc_checks.txt`). Then it was run, to look at help page 1 and at results page 5 for each shape (`verify/round13/screens/`); that found the "MORE than expected" wording that beta 3m now fixes.
- The fixed file was copied in while the calculator was closed, Checked ("No errors in the program") and run once, to see page 5's "just as expected". A run leaves its values in the program's file (v6's notes), so a fresh copy was copied in once more, Checked with nothing run ("No errors in the program"), and that is the file in the pack.
- The calculator was left by Calculator > Exit, so that it wrote its files back. The second pass of the builder read every checked file back: the same source as `programs/`, plus the calculator's compiled block, for all 31.

## The Prime Loader

`prime-loader/build_loader_v1p.py` built `PrimeLoader_v1p.html` from this pack: 31 of 31 files checked. `tests/test_loader_v1p.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1p_output.txt`).
