# EpiStats v1.7e — changes

*20 October 2026. Built on v1.7d. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner and every on-screen title or About line that names the version.

| Line (old) | Before | After |
| --- | --- | --- |
| 617 | `CHOOSE(choice, "EpiStats v1.7d ══════════",` | `CHOOSE(choice, "EpiStats v1.7e ══════════",` |
| 2013 | `apY := es_ALine("SE = sqrt(1/a + 1/b + 1/c + 1/d)", apY, #000000h);` | `apY := es_ALine("SE = √(1/a + 1/b + 1/c + 1/d)", apY, #000000h);` |
| 2015 | `apY := es_Line2("   = sqrt(1/" + es_Cnt(apA2) + " + 1/" + es_Cnt(apB2) + " + 1/" + es_Cnt(apC2) + " + 1/" + es_Cnt(apD2) + ")", " = " + STRING(ROUND(a` | `apY := es_Line2("   = √(1/" + es_Cnt(apA2) + " + 1/" + es_Cnt(apB2) + " + 1/" + es_Cnt(apC2) + " + 1/" + es_Cnt(apD2) + ")", " = " + STRING(ROUND(apSE` |
| 2039 | `apY := es_ALine("SE = sqrt((1-p1)/a + (1-p2)/c)", apY, #000000h);` | `apY := es_ALine("SE = √((1-p1)/a + (1-p2)/c)", apY, #000000h);` |
| 2041 | `apY := es_Line2("   = sqrt(" + STRING(ROUND(1 - apP1, 3), 2, 3) + "/" + es_Cnt(apA) + " + " + STRING(ROUND(1 - apP2, 3), 2, 3) + "/" + es_Cnt(apC) + "` | `apY := es_Line2("   = √(" + STRING(ROUND(1 - apP1, 3), 2, 3) + "/" + es_Cnt(apA) + " + " + STRING(ROUND(1 - apP2, 3), 2, 3) + "/" + es_Cnt(apC) + ")",` |
| 2073 | `apY := es_ALine("SE = sqrt(p1(1-p1)/n1 + p2(1-p2)/n2)", apY, #000000h);` | `apY := es_ALine("SE = √(p1(1-p1)/n1 + p2(1-p2)/n2)", apY, #000000h);` |
| 2075 | `apY := es_Line2("   = sqrt(" + STRING(ROUND(apP1, 3), 2, 3) + "×" + STRING(ROUND(1 - apP1, 3), 2, 3) + "/" + es_Cnt(apN1), " + " + STRING(ROUND(apP2, ` | `apY := es_Line2("   = √(" + STRING(ROUND(apP1, 3), 2, 3) + "×" + STRING(ROUND(1 - apP1, 3), 2, 3) + "/" + es_Cnt(apN1), " + " + STRING(ROUND(apP2, 3),` |
| 2368 | `rpY := es_ALine("Yule's Y (on sqrt(ad), sqrt(bc)) = " + rpS, rpY, #000000h);` | `rpY := es_ALine("Yule's Y (on √(ad), √(bc)) = " + rpS, rpY, #000000h);` |
| 2456 | `TEXTOUT_P("use the chi-square on page 3.", G1, 12, 72, 1, #000000h, 296);` | `TEXTOUT_P("use the χ² on page 3.", G1, 12, 72, 1, #000000h, 296);` |
| 5731 | `{"EpiStats v1.7d",` | `{"EpiStats v1.7e",` |
| 6018 | `hsS := "SE = sqrt(" + esSET + ") = " + STRING(ROUND(hsSE, 4), 2, 4);` | `hsS := "SE = √(" + esSET + ") = " + STRING(ROUND(hsSE, 4), 2, 4);` |
| 6026 | `hsS := "SE = sqrt(" + STRING(ROUND(hsV, 6), 2, 6) + ") = " + STRING(ROUND(hsSE, 4), 2, 4);` | `hsS := "SE = √(" + STRING(ROUND(hsV, 6), 2, 6) + ") = " + STRING(ROUND(hsSE, 4), 2, 4);` |
| 6032 | `hsLs := {"Why is SE(ln OR) = sqrt(1/a+1/b+1/c+1/d)?",` | `hsLs := {"Why is SE(ln OR) = √(1/a+1/b+1/c+1/d)?",` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version rather than given a new one. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

| Line (first-pass v1.7e) | Before | After |
| --- | --- | --- |
| 1312 | `IF esCO(4) == 2 THEN RETURN "infinite  (" + es_SigTxt(esCO(2)) + "-infinity)"; END;` | `IF esCO(4) == 2 THEN RETURN "infinite  (" + es_SigTxt(esCO(2)) + "-∞)"; END;` |
| 2049 | `apY := es_ALine("SE = √((1-p1)/a + (1-p2)/c)", apY, #000000h);` | `apY := es_ALine("SE = √((1-p₁)/a + (1-p₂)/c)", apY, #000000h);` |
| 2063 | `apY := es_ALine("RR = p1 / 0 is undefined (and has no CI).", apY, esRED);` | `apY := es_ALine("RR = p₁ / 0 is undefined (and has no CI).", apY, esRED);` |
| 2083 | `apY := es_ALine("SE = √(p1(1-p1)/n1 + p2(1-p2)/n2)", apY, #000000h);` | `apY := es_ALine("SE = √(p₁(1-p₁)/n₁ + p₂(1-p₂)/n₂)", apY, #000000h);` |
| 2215 | `TEXTOUT_P("when \|adjusted residual\| >= 2; grey = neither", G1, 10, 203, 1, esGRAY, 302);` | `TEXTOUT_P("when \|adjusted residual\| ≥ 2; grey = neither", G1, 10, 203, 1, esGRAY, 302);` |
| 2521 | `TEXTOUT_P("magenta = P <= yours; they sum to " + es_EqTxt("p", es_FmtNum(esQPv, 6)), G1, 6, 182, 1, esMAG, 308);` | `TEXTOUT_P("magenta = P ≤ yours; they sum to " + es_EqTxt("p", es_FmtNum(esQPv, 6)), G1, 6, 182, 1, esMAG, 308);` |
| 3010 | `TEXTOUT_P("─── Chi-Square Tests (df=1) ───", G1, 10, y, 2, RGB(0,60,200));` | `TEXTOUT_P("─── χ² Tests (df=1) ───", G1, 10, y, 2, RGB(0,60,200));` |
| 4033 | `TEXTOUT_P("coverage >= 95 %", G1, 164, 194, 1, esORNG, 150);` | `TEXTOUT_P("coverage ≥ 95 %", G1, 164, 194, 1, esORNG, 150);` |
| 4432 | `TEXTOUT_P("─── Chi-Square & Fisher's ───", G1, 10, y, 2, RGB(0,60,200));` | `TEXTOUT_P("─── χ² & Fisher's ───", G1, 10, y, 2, RGB(0,60,200));` |
| 5898 | `"expected, red = fewer (\|adj. residual\| >= 2).",` | `"expected, red = fewer (\|adj. residual\| ≥ 2).",` |
| 6070 | `"From Home: EpiStats2x2(a,b,c,d) -> Fisher p."});` | `"From Home: EpiStats2x2(a,b,c,d) → Fisher p."});` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_EpiStats_v1.7d.py`: 271 of 302 checks pass. The 31 that fail look for the old wording ("Chi-Square", "sqrt(", ">="), or compare pages word by word with v1.7a to v1.7c, or list the routines that changed. Every number passes.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the χ² headings of the 2×2 tests, the residual notes (≥ 2), the exact-test note (P ≤ yours), the formula pages (p₁, n₁ …), an infinite odds ratio's CI ("(x-∞)") and the Home note (→), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
