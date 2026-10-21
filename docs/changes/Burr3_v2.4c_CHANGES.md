# Burr3 v2.4c — changes

*20 October 2026. Built on v2.4b. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed", then "9 apps? check 20 please"). Every one of the 20 programs was checked for symbols spelled out in the text the student sees; in Burr3, the help page now use the house glyphs. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names, the "+/-" that names the + and − keys (the house footer), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow.

Version strings swept (rule 13): the banner, and the on-screen title.

| Line (old) | Before | After |
| --- | --- | --- |
| 427 | `TEXTOUT_P("Burr3 v2.4b  -  touch and keys", G1, 8, 6, 2, hpO);` | `TEXTOUT_P("Burr3 v2.4c  -  touch and keys", G1, 8, 6, 2, hpO);` |
| 430 | `TEXTOUT_P("Arrows: up or down. C, K by 0.25, S by x1.25.", G1, 8, 50, 1, hpB);` | `TEXTOUT_P("Arrows: up or down. C, K by 0.25, S by ×1.25.", G1, 8, 50, 1, hpB);` |
| 433 | `TEXTOUT_P("  (0.01 a pixel; S x1.02); a short tap sets x₀.", G1, 8, 90, 1, hpB);` | `TEXTOUT_P("  (0.01 a pixel; S ×1.02); a short tap sets x₀.", G1, 8, 90, 1, hpB);` |

## Checks

- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_Burr3_v2.4b.py`: 3 checks fail: the help page looked up by its old wording (B5), the version string on screen (D2), and the review's own check, which fails on those two (D1). Every number passes.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the touch-and-keys help page, and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
