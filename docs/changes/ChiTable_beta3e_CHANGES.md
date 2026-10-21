# ChiTable beta 3e — changes

*20 October 2026. Built on beta 3d. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 1947 | `TEXTOUT_P("All expected counts >= 5: chi-square is fine.", G1, 12, 168, 1, csGRN, 296);` | `TEXTOUT_P("All expected counts >= 5: χ² is fine.", G1, 12, 168, 1, csGRN, 296);` |
| 1951 | `TEXTOUT_P("chi-square is shaky; Fisher (2x2) or merge cells.", G1, 12, 181, 1, csRED, 296);` | `TEXTOUT_P("χ² is shaky; Fisher (2x2) or merge cells.", G1, 12, 181, 1, csRED, 296);` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version rather than given a new one. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

| Line (first-pass beta 3e) | Before | After |
| --- | --- | --- |
| 1684 | `DEFAULT TEXTOUT_P("Top: (O-E)" + csSqS + "/E, summing to " + csX2S + ".  \|adj\| >= 2: notable.", G1, 6, 184, 1, csGRAY, 308);` | `DEFAULT TEXTOUT_P("Top: (O-E)" + csSqS + "/E, summing to " + csX2S + (".  \|adj\| " + CHAR(8805) + " 2: notable."), G1, 6, 184, 1, csGRAY, 308);` |
| 1711 | `akH := "Observed count, a whole number >= 0";` | `akH := ("Observed count, a whole number " + CHAR(8805) + " 0");` |
| 1905 | `TEXTOUT_P("Decision: " + csX2S + " < critical, p >= " + csAl, G1, 12, 117, 1, #000000h, 296);` | `TEXTOUT_P("Decision: " + csX2S + (" < critical, p " + CHAR(8805) + " ") + csAl, G1, 12, 117, 1, #000000h, 296);` |
| 1910 | `TEXTOUT_P("(V = phi = Cohen's w here, since min(r,c) = 2)", G1, 12, 168, 1, csGRAY, 296);` | `TEXTOUT_P(("(V = " + CHAR(966) + " = Cohen's w here, since min(r,c) = 2)"), G1, 12, 168, 1, csGRAY, 296);` |
| 1943 | `TEXTOUT_P("p >= " + csAl + " (" + csAStr() + "): DO NOT REJECT " + csH0 + "; " + csH1 + " not accepted.", G1, 12, 62, 1, csGRN, 296);` | `TEXTOUT_P(("p " + CHAR(8805) + " ") + csAl + " (" + csAStr() + "): DO NOT REJECT " + csH0 + "; " + csH1 + " not accepted.", G1, 12, 62, 1, csGRN, 296);` |
| 1957 | `TEXTOUT_P("All expected counts >= 5: χ² is fine.", G1, 12, 168, 1, csGRN, 296);` | `TEXTOUT_P(("All expected counts " + CHAR(8805) + " 5: " + CHAR(967) + CHAR(178) + " is fine."), G1, 12, 168, 1, csGRN, 296);` |
| 1961 | `TEXTOUT_P("χ² is shaky; Fisher (2x2) or merge cells.", G1, 12, 181, 1, csRED, 296);` | `TEXTOUT_P((CHAR(967) + CHAR(178) + " is shaky; Fisher (2x2) or merge cells."), G1, 12, 181, 1, csRED, 296);` |
| 1989 | `TEXTOUT_P("p1 = " + STRING(csO(1), 2, 0) + "/" + STRING(csRT(1), 2, 0) + " = " + STRING(ROUND(csP1, 4), 2, 4) + "   p2 = " + STRING(csO(3), 2, 0) + "/" + STRING(csRT(2), 2, 0) + " = " + STRING(ROUND(csP2, 4), 2, 4), G1, 12, 46, 1, #000000h, 296);` | `TEXTOUT_P(("p" + CHAR(8321) + " = ") + STRING(csO(1), 2, 0) + "/" + STRING(csRT(1), 2, 0) + " = " + STRING(ROUND(csP1, 4), 2, 4) + ("   p" + CHAR(8322) + " = ") + STRING(csO(3), 2, 0) + "/" + STRING(csRT(2), 2, 0) + " = " + STRING(ROUND(csP2, 4), 2, 4), G1, 12, 46, 1, #000000h, 296);` |
| 2003 | `TEXTOUT_P("Risk diff. p1 - p2 = " + csSgn(csRD, 4) + " (" + STRING(ROUND(csRDL, 4), 2, 4) + ", " + STRING(ROUND(csRDH, 4), 2, 4) + ")", G1, 12, 111, 1, csMAG, 296);` | `TEXTOUT_P(("Risk diff. p" + CHAR(8321) + " - p" + CHAR(8322) + " = ") + csSgn(csRD, 4) + " (" + STRING(ROUND(csRDL, 4), 2, 4) + ", " + STRING(ROUND(csRDH, 4), 2, 4) + ")", G1, 12, 111, 1, csMAG, 296);` |
| 2004 | `TEXTOUT_P("Relative risk p1/p2 = " + STRING(ROUND(csRR, 3), 2, 3) + " (" + STRING(ROUND(csRRL, 3), 2, 3) + ", " + STRING(ROUND(csRRH, 3), 2, 3) + ")", G1, 12, 124, 1, csMAG, 296);` | `TEXTOUT_P(("Relative risk p" + CHAR(8321) + "/p" + CHAR(8322) + " = ") + STRING(ROUND(csRR, 3), 2, 3) + " (" + STRING(ROUND(csRRL, 3), 2, 3) + ", " + STRING(ROUND(csRRH, 3), 2, 3) + ")", G1, 12, 124, 1, csMAG, 296);` |
| 2018 | `TEXTOUT_P("phi = " + csSgn(csPhi, 3) + "   (positive when a*d > b*c)", G1, 12, 167, 1, csBLUE, 296);` | `TEXTOUT_P((CHAR(966) + " = ") + csSgn(csPhi, 3) + ("   (positive when a" + CHAR(215) + "d > b" + CHAR(215) + "c)"), G1, 12, 167, 1, csBLUE, 296);` |
| 2476 | `TEXTOUT_P("blue: more than expected; red: fewer (\|adj\|>=2)", G1, 6, 190, 1, csGRAY, 308);` | `TEXTOUT_P(("blue: more than expected; red: fewer (\|adj\|" + CHAR(8805) + "2)"), G1, 6, 190, 1, csGRAY, 308);` |
| 3416 | `TEXTOUT_P("2x2 extras take column 1 as the outcome: p1, p2,", G1, 12, 86, 1, csMAG, 296);` | `TEXTOUT_P(("2x2 extras take column 1 as the outcome: p" + CHAR(8321) + ", p" + CHAR(8322) + ","), G1, 12, 86, 1, csMAG, 296);` |
| 3444 | `TEXTOUT_P("Residual plot: one bar per cell, dotted at +/-2.", G1, 12, 179, 1, csGRAY, 296);` | `TEXTOUT_P(("Residual plot: one bar per cell, dotted at " + CHAR(177) + "2."), G1, 12, 179, 1, csGRAY, 296);` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_ChiTable_beta3d.py`: 6,910 of 6,931 checks pass, every number against SciPy and statsmodels and "the file is still pure ASCII" among them. The 21 that fail look for the old wording (p1 - p2, p >= α, phi, chi-square is shaky, |adj| >= 2) or for "only these routines changed".
- Not yet on a calculator.
- **This program keeps its code pure ASCII** (its other display glyphs are built with `CHAR()`), so the new glyphs are built the same way, for example `("P(age " + CHAR(8805) + " 18)")`; on screen it is the same character. `ascii_fix_2026-10-20.py` did it and checked that folding the builds back gives the swept text exactly; the gate and the verify script then ran again on the rebuilt file.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the 2×2 extras page (p₁, p₂, φ, a×d > b×c), the decision lines (p ≥ α), the residual help (|adj| ≥ 2, ±2) and the expected-count verdict, and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
