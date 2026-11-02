# StatDist v2.7h: changes

*1 November 2026, night. Edited from v2.7g by a patch script (`patch_sd27h.py`), every replacement checked to apply exactly once. 4,971 lines. v2.7g was never committed: testing it on the Virtual Calculator found the faults below, and v2.7h replaced it the same night. v2.7g's changes (`StatDist_v2.7g_CHANGES.md`) are all in v2.7h.*

## What the Virtual Calculator showed

A normal with σ = 10⁻⁷:

- **the density labels 1000000 … 4000000 showed as "100000" … "400000"**: `TEXTOUT_P`'s width limit (`stPL - 4`) cut the last character off, which made each label a wrong number;
- the x labels −0.0000003 … 0.0000003, each cut at 60 px, were printed over each other.

v2.7f drew its labels the same way. Density labels with five decimals or more were not drawn at all (any scale above about 2000).

## What changed (line numbers are v2.7g's)

1. **No label is clipped** (`st_Draw`, 3553 and 3566).
2. **An x label that would touch the one before it, or end more than 3 px past the right edge, is left out**; its tick stays, as in Norm3, CICatcher, NormExplorer and SampDist. At the usual windows every label is drawn as before ("3000" at x = 298 included).
3. **If any density label would be wider than the 35 px left of the axis, every label on the axis is written in the Prime's scientific form**, `STRING(x, 3, 1)` without its ".0": "4ᴇ6", "5ᴇ-5", as SampDist v2.3e's. A label that still does not fit is left out. Density labels with five decimals or more, which v2.7g left out, now show this way. `STRING(x, 2, d)` is asked only for d up to 12 (the Prime refuses 13), so a density near 10⁻²¹ (a normal with σ = 10²⁰) is labelled "1ᴇ-21" rather than stopping the program.
4. New `st_LWd` (before `st_Draw`): about 5.5 px a character and 3 px for the point. The help page's title says v2.7h.

## Verification

`verify_StatDist_v2.7h.py`, output `verify_StatDist_v2.7h_output.txt`: **45 PASS, 0 FAIL**, run from a repository layout with v2.7f read from git history. It is v2.7g's script (every check against v2.7f, as there: 2,349 screens over all 27 families identical) and a section Y: 17 plots at the far scales (a normal with σ from 10⁻⁹ to 10⁴⁰, the exponential at λ = 10⁻⁶ and 10⁶, the Poisson at λ = 100,000, a normal at μ = 10⁹), density labels at most 35 px wide, x labels apart and on the screen, and v2.7f's own labels wherever they fitted.

**The sweep again** (every parameter of all 27 families over 23 values from 1E−300 to 1E300, with Zoom− ten times): 0 broken in 1,794 runs (851 refused with a box, 943 drawn), the same tally as v2.7g's. **The monkey test again** (1,000 runs, `--lists`): 1,000 OK.

## Gate

`ppl_gate_v1d.py StatDist_v2.7h.txt StatDist_v2.7g.txt`: **RESULT: PASS**. Kit lint 0 errors; ppl_check clean, as v2.7g.

## The Virtual Calculator

On the Virtual Calculator (2.4.2, Rogers-HP; Claude through computer use, 1 Nov 2026, night): Check, "No errors in the program"; the file written back after that Check alone (451,002 bytes) holds the exact source and is the starter pack's. A normal with σ = 3 × 10⁻⁷: density labels "5ᴇ5" and "1ᴇ6", x labels −0.0000005, 0.0000000, 0.0000005, none over another. (An earlier form of the fix, label by label, also ran there: σ = 10⁻⁷ gave "1ᴇ6" … "4ᴇ6"; Burr XII with C = K = 100 through Zoom− twelve times; a Poisson with λ = 100,000 in under 10 seconds, P(X ≤ 100000) = 0.500841.)
