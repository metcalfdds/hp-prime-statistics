# TrendTest beta 3e — changes

*20 October 2026. Built on beta 3d. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 1046 | `TEXTOUT_P("Chi-square test for linear trend", G1, 10, 6, 2, trBLUE);` | `TEXTOUT_P("χ² test for linear trend", G1, 10, 6, 2, trBLUE);` |
| 1225 | `TEXTOUT_P("      * [ N sum(x^2 n) - (sum x n)^2 ]", G1, 10, 164, 1, #000000h);` | `TEXTOUT_P("      * [ N sum(x² n) - (sum x n)² ]", G1, 10, 164, 1, #000000h);` |
| 1439 | `TEXTOUT_P("SSE = sum n(p - a - bx)^2; p = cases/n, x = score", G1, 10, 35, 1, #000000h, 302);` | `TEXTOUT_P("SSE = sum n(p - a - bx)²; p = cases/n, x = score", G1, 10, 35, 1, #000000h, 302);` |
| 1468 | `TEXTOUT_P("(sum n x) a + (sum n x^2) b = sum x a", G1, 10, p4Y + 33, 1, trBLUE, 302);` | `TEXTOUT_P("(sum n x) a + (sum n x²) b = sum x a", G1, 10, p4Y + 33, 1, trBLUE, 302);` |
| 1987 | `TEXTOUT_P("Chi-square for trend: the idea", G1, 12, 8, 2, trBLUE);` | `TEXTOUT_P("χ² for trend: the idea", G1, 12, 8, 2, trBLUE);` |
| 1989 | `TEXTOUT_P("grade).  Pearson's chi-square (k-1 df) asks", G1, 12, 45, 1, #000000h);` | `TEXTOUT_P("grade).  Pearson's χ² (k-1 df) asks", G1, 12, 45, 1, #000000h);` |
| 2021 | `TEXTOUT_P("(1/N + (x - xbar)^2 / sum n(x - xbar)^2).", G1, 12, 193, 1, trGRAY);` | `TEXTOUT_P("(1/N + (x - " + CHAR(57344) + ")² / sum n(x - " + CHAR(57344) + ")²).", G1, 12, 193, 1, trGRAY);` |
| 2093 | `CHOOSE(mnI, "Chi-square for linear trend", {` | `CHOOSE(mnI, "χ² for linear trend", {` |
| 2122 | `mnS := "TrendTest: X2 trend = " + trFx(trX2T, 4) + " (1 df), " + trPStr(trPT) + "; Pearson X2 = " + trFx(trX2P, 4) + " (" + STRING(trK - 1, 2, 0) + " ` | `mnS := "TrendTest: χ² trend = " + trFx(trX2T, 4) + " (1 df), " + trPStr(trPT) + "; Pearson χ² = " + trFx(trX2P, 4) + " (" + STRING(trK - 1, 2, 0) + " ` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version rather than given a new one. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

| Line (first-pass beta 3e) | Before | After |
| --- | --- | --- |
| 1232 | `TEXTOUT_P(trChi + " trend = S^2 / V  (1 df),  where", G1, 10, 128, 1, #000000h);` | `TEXTOUT_P(trChi + " trend = S² / V  (1 df),  where", G1, 10, 128, 1, #000000h);` |
| 1234 | `TEXTOUT_P("V = A (N-A) / (N^2 (N-1))", G1, 10, 152, 1, #000000h);` | `TEXTOUT_P("V = A (N-A) / (N² (N-1))", G1, 10, 152, 1, #000000h);` |
| 2023 | `TEXTOUT_P("grey within 1 SE of it (SE^2 = P(1-P)/n).", G1, 12, 80, 1, trBLUE);` | `TEXTOUT_P("grey within 1 SE of it (SE² = P(1-P)/n).", G1, 12, 80, 1, trBLUE);` |
| 2030 | `TEXTOUT_P("Band: fit +/- 1.96 SE, SE^2 = P(1-P) times", G1, 12, 180, 1, trGRAY);` | `TEXTOUT_P("Band: fit ± 1.96 SE, SE² = P(1-P) times", G1, 12, 180, 1, trGRAY);` |
| 2056 | `TEXTOUT_P("Mantel's (1963) (N-1) r^2, as this page does;", G1, 12, 159, 1, trGRAY);` | `TEXTOUT_P("Mantel's (1963) (N-1) r², as this page does;", G1, 12, 159, 1, trGRAY);` |
| 2058 | `TEXTOUT_P("print Armitage's (1955) N r^2: 72.688 for", G1, 12, 185, 1, trGRAY);` | `TEXTOUT_P("print Armitage's (1955) N r²: 72.688 for", G1, 12, 185, 1, trGRAY);` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_TrendTest_beta3d.py`: 111 of 134 checks pass. The 23 that fail look for the old wording: the help titles ("Chi-square for trend"), the Home summary ("TrendTest: X2 trend"), the menu line; the script drives the menus by their text, so a renamed title also stops its later steps. Every number passes.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the formula page (S², N²), the fit-band help (± 1.96 SE, SE²) and the Mantel/Armitage note (r²), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
