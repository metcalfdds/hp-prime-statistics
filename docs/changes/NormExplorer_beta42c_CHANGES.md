# NormExplorer beta 42c — changes

*20 October 2026. Built on beta 42b. Text on screen only.*

## What changed

Beta 42c carries beta 42b's change (the standardize animation keeps its 0.3 s pace on a slow calculator; the Diagnostics page shows the last run's length and slowest frame) and adds the one below. Beta 42b never reached a calculator, so its device checklist (`NormExplorer_beta42b_CHANGES.md`, items 2 to 6) is part of this one, and `verify_NormExplorer_beta42b.py` still describes the animation code, which is unchanged.

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 2543 | `MSGBOX("Wrote " + ne_Fx(zdN, 0) + " z-scores into D2.  x-bar = "` | `MSGBOX("Wrote " + ne_Fx(zdN, 0) + " z-scores into D2.  " + CHAR(57344) + " = "` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version rather than given a new one. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

| Line (first-pass beta 42c) | Before | After |
| --- | --- | --- |
| 1248 | `{"Bnd A", "Bnd B", "mu", "sigma", "Menu", "More"}};` | `{"Bnd A", "Bnd B", "μ", "σ", "Menu", "More"}};` |
| 2807 | `TEXTOUT_P("mu, sigma", G1, 20, 149, 1, NBLACK);` | `TEXTOUT_P("μ, σ", G1, 20, 149, 1, NBLACK);` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_NormExplorer_beta42b.py`: 27 of 28 checks pass, the animation's pace on fast and slow drawing among them. The 1 that fails lists the routines that changed (the Explorer, its help and the z-score message now differ too).
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the Explorer's page-2 soft keys (μ, σ) and the help line that names them, and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
