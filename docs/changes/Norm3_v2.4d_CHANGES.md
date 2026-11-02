# Norm3 v2.4d: changes

*1 November 2026, night. Edited from v2.4c by a patch script (`patch_n3_24d.py`), every replacement checked to apply exactly once. 1,061 lines. v2.4c was never committed: testing it on the Virtual Calculator found the fault below, and v2.4d replaced it the same night. v2.4c's changes (`Norm3_v2.4c_CHANGES.md`) are all in v2.4d.*

## What the Virtual Calculator showed

The density labels left of the axis are drawn at x = 1 in the 24 px margin. Wider labels ran over the axis and into the plot:

| σ | v2.4c's labels | |
| --- | --- | --- |
| 1, 10, 15 | 0.1 … 0.5, 0.01 … 0.05 | fit |
| 1000 | 0.0001 … 0.0005 | over the axis (any σ above about 50 gives five characters or more) |
| 10¹⁰ | 0.00000000001 … | over the axis and into the plot |
| 10⁻⁹ | 100000000 … 500000000 | over the axis and into the plot |

v2.4b drew its labels the same way. The PC overlap check (`text_overlap_v1`) compares text with text only, so a label over a line passed it.

## What changed (line numbers are v2.4c's)

1. **Density labels that do not fit are written in units of a power of ten** (712–718): if any label would be wider than 20 px (about 5.5 px a character and 3 px for the point; "0.03" is 20 px on the Virtual Calculator), every label on the axis is written as its value over 10ⁿ (1 2 3 4 5) and "×1ᴇ-4" is printed at the top of the axis, just inside the plot. New `n3_YWd` (after `n3_NiceNum`) estimates the width; the times sign is `CHAR(215)`, so the code stays ASCII.
2. Labels that fit are drawn exactly as before.
3. The banner, the firmware lines and the help page's title say v2.4d.

## Verification

`verify_Norm3_v2.4d.py`, output `verify_Norm3_v2.4d_output.txt`: **25 PASS, 0 FAIL**, run from a repository layout with v2.4b read from git history. It is v2.4c's script (every check against v2.4b, as there; R1 now writes the scaled labels back out before comparing) and a section Y: at 29 values of σ from 10⁻⁹ to 10¹⁰, every label at most 20 px wide, and where v2.4b's were wider (σ = 1000 among them) the same values in units of the printed power; elsewhere exactly v2.4b's.

**The monkey test again** (1,002 runs, 334 from each of three starts): 1,002 OK.

## Gate

`ppl_gate_v1d.py Norm3_v2.4d.txt Norm3_v2.4c.txt`: **RESULT: PASS**. Kit lint 0 errors; ppl_check 2 E5, 1 E7, as v2.4c; full parse OK (10 functions).

## The Virtual Calculator

On the Virtual Calculator (2.4.2, Rogers-HP; Claude through computer use, 1 Nov 2026, night): Check, "No errors in the program"; the file written back after that Check alone (103,036 bytes) holds the exact source and is the starter pack's. `Norm3(0, 1000, 0)`: labels 1 … 5 under "×1ᴇ-4", clear of the axis; `Norm3(0, 1ᴇ10, 0)`: 1 … 5 under "×1ᴇ-11".
