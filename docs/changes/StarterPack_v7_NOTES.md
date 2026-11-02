# Starter pack v7: notes (1 November 2026, evening)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v7.zip`, built by `tools/make_starter_pack_v4.py v7 --checked FOLDER` from the 30 programs in `programs/`. v6 was built earlier the same day: `StarterPack_v6_NOTES.md`.*

## What changed from v6

Two programs changed:

| Program | v6 | v7 |
| --- | --- | --- |
| SampDist | v2.3d | **v2.3e** |
| BayesTree | beta 8e | **beta 8f** |

Both carry the monkey test's fixes and what testing them on the Virtual Calculator found (`docs/changes/SampDist_v2.3e_CHANGES.md`, `BayesTree_beta8f_CHANGES.md`):

- every form field takes numbers only;
- numbers the program cannot draw or use are refused with a sentence (SampDist: more than 50 digits, σ above 10¹⁰, σ/√n too small for 12 digits; BayesTree: a proportion outside 0 to 1, N outside 10 to 1,000,000, a negative count);
- SampDist no longer stalls at μ = 10⁹, σ = 0.001 or stops at σ = 10¹²; BayesTree no longer divides by zero on a node's page with two tests and a small N, and no longer stops with "Numerical overflow" at a prior, sens and spec of 0.999.

Everything else in the zip is byte for byte v6's: the other 28 programs, the CentralLimit app and the sample matrix. `READ_ME_FIRST.txt` differs only in its title line and the two versions in its table.

## The two checked files (Virtual Calculator 2.4.2, Rogers-HP, by Claude through computer use)

- Each was built by hp-prime-kit, copied into the calculator's folder with the calculator closed, opened in the editor and Checked ("No errors in the program"). The calculator was then closed (Calculator → Exit), and the file it wrote back was collected: **after a Check and nothing else** (a checked file keeps the file-level values of its last run, `StarterPack_v6_NOTES.md`).
  - SampDist: 163,692 bytes, +3,240.
  - BayesTree: 326,700 bytes, +8,926.
- `make_starter_pack_v4.py --checked` read the source out of each and found it equal to `programs/<file>.txt`.
- The other 28 files are v6's. Twenty-six of them are v5's, collected on 1 November after the 31 October runs, and may carry their last run's values; when each program next changes, its file is to be collected after a Check alone.

## Checks

The tool's name check passed. `fleet_names_v2.py` over the 30 programs found 2,264 routine names and 0 collisions. Every file was read back. The pack is 1.46 MB zipped (sha256 begins `398733e8dd87`). The Prime Loader v1e is built from it, and its Chromium test gives 58 PASS (`prime-loader/tests/test_loader_v1e_output.txt`).
