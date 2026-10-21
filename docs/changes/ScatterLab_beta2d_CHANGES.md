# ScatterLab beta 2d — changes

*20 October 2026. Built on beta 2c. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 1675 | `TEXTOUT_P("SSE = sum (y - a - bx)^2 over all n = " + STRING(slN, 2, 0) + " points", G1, 12, 37, 1, #000000h, 300);` | `TEXTOUT_P("SSE = sum (y - a - bx)² over all n = " + STRING(slN, 2, 0) + " points", G1, 12, 37, 1, #000000h, 300);` |
| 1704 | `TEXTOUT_P("(sum x) a + (sum x^2) b = sum x y", G1, 12, cdY + 44, 1, slBLUE, 300);` | `TEXTOUT_P("(sum x) a + (sum x²) b = sum x y", G1, 12, cdY + 44, 1, slBLUE, 300);` |
| 1767 | `slHT("r = Sxy / sqrt(Sxx Syy), where", 156, slGRAY);` | `slHT("r = Sxy / √(Sxx Syy), where", 156, slGRAY);` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. The second pass found nothing more spelled out in this program. It found something else: this program keeps its code pure ASCII, and the first pass had typed its glyphs. They are now built with `CHAR()` (the table), which puts the same characters on screen. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version.

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

| Line (first-pass beta 2d) | Before | After |
| --- | --- | --- |
| 1685 | `TEXTOUT_P("SSE = sum (y - a - bx)² over all n = " + STRING(slN, 2, 0) + " points", G1, 12, 37, 1, #000000h, 300);` | `TEXTOUT_P(("SSE = sum (y - a - bx)" + CHAR(178) + " over all n = ") + STRING(slN, 2, 0) + " points", G1, 12, 37, 1, #000000h, 300);` |
| 1714 | `TEXTOUT_P("(sum x) a + (sum x²) b = sum x y", G1, 12, cdY + 44, 1, slBLUE, 300);` | `TEXTOUT_P(("(sum x) a + (sum x" + CHAR(178) + ") b = sum x y"), G1, 12, cdY + 44, 1, slBLUE, 300);` |
| 1777 | `slHT("r = Sxy / √(Sxx Syy), where", 156, slGRAY);` | `slHT(("r = Sxy / " + CHAR(8730) + "(Sxx Syy), where"), 156, slGRAY);` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_ScatterLab_beta2c.py`: every check passes but 6, "the file is still pure ASCII" among the passes. The 6 look for the calculus page's old text ("sum x^2", "(y - a - bx)^2") or list the routines and lines that changed.
- Not yet on a calculator.
- **This program keeps its code pure ASCII** (its other display glyphs are built with `CHAR()`), so the new glyphs are built the same way, for example `("P(age " + CHAR(8805) + " 18)")`; on screen it is the same character. `ascii_fix_2026-10-20.py` did it and checked that folding the builds back gives the swept text exactly; the gate and the verify script then ran again on the rebuilt file.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the calculus page (², √), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
