# NormExplorer beta 42e: changes

*1 November 2026, night. Edited from beta 42d by a patch script (`patch_ne42e.py`), every replacement checked to apply exactly once. 4,143 lines. Beta 42d was never committed: testing it on the Virtual Calculator found the fault below, and beta 42e replaced it the same night. Beta 42d's changes (`NormExplorer_beta42d_CHANGES.md`) are all in beta 42e.*

## What the Virtual Calculator showed

At σ = 10,000 the Explorer's density labels "0.00002", "0.00004", "0.00006" ran over the axis and the top one into the μ box. The margin left of the axis is 38 px and the labels start at x = 2; any σ above about 2000 gives labels of seven characters, and a σ below about 0.0000001 integers of seven digits. Beta 42c drew its labels the same way. The PC overlap check compares text with text only.

## What changed (line numbers are beta 42d's)

1. **If any density label would be wider than 34 px, every label on the axis is written in the Prime's scientific form** (`ne_NormDraw`'s y grid, 3463–3471): `STRING(x, 3, 1)` without its ".0", "6ᴇ-5" for 0.00006, "4ᴇ6" for 4000000, as SampDist v2.3e's labels (seen on the Virtual Calculator in round 2). A label that still does not fit is left out; its grid line stays. New `ne_YWd` (after `ne_Fx`) estimates the width: about 5.5 px a character and 3 px for the point.
2. Labels that fit are drawn exactly as before.
3. The banners and the firmware lines say beta 42e.

## Verification

`verify_NormExplorer_beta42e.py`, output `verify_NormExplorer_beta42e_output.txt`: **51 PASS, 0 FAIL**, run from a repository layout with beta 42c read from git history. It is beta 42d's script (every check against beta 42c, as there) and a section Y: the Explorer at 27 values of σ from 10⁻⁹ to 10¹⁰, every label at most 34 px wide; where beta 42c's were wider (σ = 10,000 among them) the same values in the scientific form; elsewhere exactly beta 42c's.

**The monkey test again** (1,000 runs, `--lists --writes D`): 1,000 OK.

## Gate

`ppl_gate_v1d.py NormExplorer_beta42e.txt NormExplorer_beta42d.txt`: **RESULT: PASS**. Kit lint 0 errors (the MicroPython lines blanked); ppl_check 5 E5, 6 W3, as beta 42d; lint_ppl's problems are beta 42d's.

## The Virtual Calculator

On the Virtual Calculator (2.4.2, Rogers-HP; Claude through computer use, 1 Nov 2026, night): Check, "No errors in the program"; the file written back after that Check alone (381,089 bytes) holds the exact source and is the starter pack's. The Explorer at N(0, 10000) (on the first form of the fix, label by label, which gave the same labels here): "6ᴇ-5", "4ᴇ-5", "2ᴇ-5", clear of the axis.
