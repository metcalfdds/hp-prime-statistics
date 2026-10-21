# GaltonBoard beta 3e — changes

*20 October 2026. Built on beta 3d. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed", then "9 apps? check 20 please"). Every one of the 20 programs was checked for symbols spelled out in the text the student sees; in GaltonBoard, the Poisson-limit page and the help page now use the house glyphs. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names, the "+/-" that names the + and − keys (the house footer), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow.

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 1987 | `pwT := "as R " + CHAR(8594) + " infinity";` | `pwT := "as R " + CHAR(8594) + " " + CHAR(8734);` |
| 2177 | `gbMsg := "Pascal's numbers need R <= 9 (pegs 28 px apart)";` | `gbMsg := "Pascal's numbers need R ≤ 9 (pegs 28 px apart)";` |

**One code line:** the Poisson page's `pwT := "as R " + CHAR(8594) + " infinity"` became `... + " " + CHAR(8734)`. `pwT` is only drawn.

## Checks

- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_GaltonBoard_beta3c.py`, run on beta 3c (all OK) and on beta 3e: 4 checks fail on 3e, two that look for "as R → infinity" where the Poisson page now says "as R → ∞", and two that list the routines and menu lines that changed. Every probability passes.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the Poisson-limit page ("as R → ∞: …") and the help page ("R ≤ 9"), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
