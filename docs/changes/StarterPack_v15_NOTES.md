# Starter pack v15: notes (7 November 2026, night)

Built by `tools/make_starter_pack_v4.py v15 --checked DIR` from `programs/` (31 programs: TDist3D beta 1 joins the 30 of v14, and BurrLab is beta 1p). DIR was the Virtual Calculator's own folder in the cloud workspace (Wine; Lessons Learned v7zm), after each of the two new or changed programs had been Checked there once and the calculator closed with Calculator > Exit, which is when it writes its files back. The 29 other files are the ones v14 carried, checked the same way on 5 November.

## What was done on the Virtual Calculator 2.4.2 (build 2026-09-09), 7 November 2026

- `TDist3D.hpprgm` and `BurrLab.hpprgm`, built by hp-prime-kit's `hpprime write` from the two sources, were copied into `Documents\HP Prime\Calculators\Prime` while the calculator was closed. On the next start both were in the Program Catalog: TDist3D at the bottom (new), BurrLab in the row the old file had held (a replaced file keeps its row; the catalog's order is the calculator's own last-change record, not the file's date).
- Program Catalog > Edit > Check on each: "No errors in the program" for both.
- TDist3D was run from the catalog: the welcome page, the surface, a finger drag (θ 35° to 71°, φ 30° to 42°, the 13 × 6 grid while the finger moved and the full 25 × 11 grid after it lifted), the Curves view with ν+ twice (3, 4, 5), Menu > Frame timing (9 ms a frame at 25 × 11, 5 ms at 13 × 6, 12 ms for Curves), the four help pages, Menu > Set ν exactly = 7.5 (t crit 2.333, P(|t| > 2) 0.083, the slice redrawn), 0.3 refused with its sentence, and Esc, which showed the RETURN string.
- BurrLab beta 1p was run from the catalog: the Family page (the map with its three tints, the Lomax and Fisk lines and the red dot inside a gray border, where beta 1o showed a solid gray box), Explore (the tail shade solid light blue with the curve on top), and How rare (the shade solid pink).
- Calculator > Exit. The two checked files grew by their compiled blocks (TDist3D 98,812 to 164,382 bytes; BurrLab 404,038 to 473,223). `hpprime read` on each gave the shipped source word for word, and the pack builder's own read-back said the same for all 31.

Screens: `D:\HP-Prime\_vc_screens_2026-11-07\`.

## The Prime Loader

`prime-loader/build_loader_v1m.py` built `PrimeLoader_v1m.html` from this pack: 31 of 31 files checked; TDist3D is offered with Chapters 9 and 11. `tests/test_loader_v1m.js`: 59 PASS, 0 FAIL in Chromium (`tests/test_loader_v1m_output.txt`).
