# Starter pack v11: notes (2 November 2026, night)

*The pack is `starter-pack/HP_Prime_Statistics_Starter_Pack_v11.zip`, built by `tools/make_starter_pack_v4.py v11 --checked FOLDER` from the 30 programs in `programs/`. v10: `StarterPack_v10_NOTES.md`.*

## What changed from v10

Eleven programs changed, in round 6: **what a student types is kept to sensible ranges**, and refused with a sentence outside them, never changed without a word; **every menu item fits its box**; and BurrLab draws a y axis on every plot page. How the ranges were found and settled: `docs/dev/caps-2026-11-02.md`; each program's change note is in `docs/changes/`.

| Program | v10 | v11 | Round 6 |
| --- | --- | --- | --- |
| AgreeLab | beta 1c | **beta 1d** | eleven menu items shortened |
| BurrLab | beta 1j | **beta 1l** | x0 stops at the plot's edge, S at 1,000; a y axis on every plot; menu items shortened |
| ChiTable | beta 3g | **beta 3h** | alpha 0.001 to 0.2 (typed and dragged) |
| DNAMixLR | beta 3f | **beta 3g** | yes/no answers 1 or 0 only; allele names 1 to 99; menu items shortened |
| EpiStats | v1.7f | **v1.7g** | alpha 0.001 to 0.2; counts at most 9,999,999 |
| NormExplorer | beta 42f | **beta 42g** | alpha 0.001 to 0.2; two menu items shortened |
| PowerViz | v2.5m | **v2.5n** | alpha 0.001 to 0.2 |
| RiskLab | beta 1c | **beta 1d** | two menu items shortened |
| SampDist | v2.3f | **v2.3g** | alpha 0.001 to 0.2 (typed and dragged) |
| StudRange | beta 15g | **beta 15i** | alpha 0.001 to 0.2; k 2 to 100; df 1 to 100,000 or 0 for ∞; Tukey HSD's m 2 to 1,000 |
| TrendTest | beta 3h | **beta 3i** | a level's total at most 99,999; the results table's columns laid out again |

BurrLab beta 1k and StudRange beta 15h were builds of the same night that were never shipped: the repository goes from beta 1j to beta 1l and from beta 15g to beta 15i. The other 19 programs and the CentralLimit app are v10's, byte for byte, and so is the sample matrix. `READ_ME_FIRST.txt` differs only in its title line and the versions in its table.

## The 11 checked files (Virtual Calculator 2.4.2, Rogers-HP, by Claude through computer use)

Each of the 11 was copied into the Virtual Calculator 2.4.2 (Rogers-HP, 2 November 2026, night) with the calculator closed, opened in the editor and Checked: **"No errors in the program"**, every one. The files the calculator wrote back after those Checks, and nothing else, are the ones in starter pack v11; the other 19 are v10's checked files. Hand trials on the same calculator: BurrLab's Explore and Family pages with their y axes; StudRange's Critical value refusing a df of 1,000,000 with its sentence, and its MicroPython engine giving q crit = 3.3150 at k 3, df 10,000; TrendTest's snoring example, every confidence interval inside the results page's frame. Each change note in `docs/changes/` records its program's Check.

`make_starter_pack_v4.py --checked` read the source out of each of the 30 and found it equal to `programs/<file>.txt`.

## Checks

The tool's name check passed. `fleet_names_v2.py` over the 30 programs: 2,326 routine names, 0 collisions. Every file was read back. The pack is 1,534,529 bytes (1.53 MB; sha256 begins `adaa1ed8a150`). The Prime Loader v1i is built from it, and its Chromium test gives 58 PASS, 0 FAIL (`prime-loader/tests/test_loader_v1i_output.txt`).
