# CICatcher beta 2d — changes

*20 October 2026. Built on beta 2c. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed", then "9 apps? check 20 please"). Every one of the 20 programs was checked for symbols spelled out in the text the student sees; in CICatcher, the formula help pages now use the house glyphs. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names, the "+/-" that names the + and − keys (the house footer), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow.

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 1796 | `"z: " + cqXb + " +/- z " + cqTms + " " + cqSgS + "/sqrt(n) uses the TRUE " + cqSgS + ",",` | `"z: " + cqXb + (" " + CHAR(177) + " z ") + cqTms + " " + cqSgS + ("/" + CHAR(8730) + "(n) uses the TRUE ") + cqSgS + ",",` |
| 1798 | `"t: " + cqXb + " +/- t " + cqTms + " s/sqrt(n) uses the sample's s.",` | `"t: " + cqXb + (" " + CHAR(177) + " t ") + cqTms + (" s/" + CHAR(8730) + "(n) uses the sample's s."),` |
| 1809 | `"Wald: " + cqPh + " +/- z " + cqTms + " sqrt(" + cqPh + "(1 - " + cqPh + ")/n), the",` | `"Wald: " + cqPh + (" " + CHAR(177) + " z ") + cqTms + (" " + CHAR(8730) + "(") + cqPh + "(1 - " + cqPh + ")/n), the",` |
| 1850 | `"0.38 +/- 1.96 " + cqTms + " sqrt(0.38 " + cqTms + " 0.62 / 100)",` | `("0.38 " + CHAR(177) + " 1.96 ") + cqTms + (" " + CHAR(8730) + "(0.38 ") + cqTms + " 0.62 / 100)",` |
| 1851 | `"= 0.38 +/- 0.095, from 28.5 % to 47.5 %.",` | `("= 0.38 " + CHAR(177) + " 0.095, from 28.5 % to 47.5 %."),` |

## Checks

- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_CICatcher_beta2c.py`: 155 of 158 checks pass. The 3 that fail look for the routine list of beta 2c (cqHelp now differs too), the banner "beta 2c", and the old help wording in beta 1's suite. Every interval and catch level passes.
- Not yet on a calculator.
- **This program keeps its code pure ASCII** (its other display glyphs are built with `CHAR()`), so the new glyphs are built the same way, for example `("P(age " + CHAR(8805) + " 18)")`; on screen it is the same character. `ascii_fix_2026-10-20.py` did it and checked that folding the builds back gives the swept text exactly; the gate and the verify script then ran again on the rebuilt file.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the help pages on the z, t and Wald intervals and the worked example (0.38 ± 1.96 …), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
