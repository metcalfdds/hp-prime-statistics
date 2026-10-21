# PowerViz v2.5e — changes

*20 October 2026. Built on v2.5d. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed", then "9 apps? check 20 please"). Every one of the 20 programs was checked for symbols spelled out in the text the student sees; in PowerViz, the sample-size formula now use the house glyphs. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names, the "+/-" that names the + and − keys (the house footer), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow.

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 2076 | `IF TT==1 THEN fs1 := {"  n = ((zα+zβ)×σ/(μ₁−μ₀))^2"}; END;` | `IF TT==1 THEN fs1 := {"  n = ((zα+zβ)×σ/(μ₁−μ₀))²"}; END;` |
| 2077 | `IF TT==2 THEN fs1 := {"  n = 2×((zα+zβ)×σ/(μ₂−μ₁))^2"}; END;` | `IF TT==2 THEN fs1 := {"  n = 2×((zα+zβ)×σ/(μ₂−μ₁))²"}; END;` |
| 2078 | `IF TT==3 THEN fs1 := pv_Wrap("  n = ((zα"+SQG+"(p₀(1−p₀)) + zβ"+SQG+"(p₁(1−p₁)))/(p₁−p₀))^2", 54); END;` | `IF TT==3 THEN fs1 := pv_Wrap("  n = ((zα"+SQG+"(p₀(1−p₀)) + zβ"+SQG+"(p₁(1−p₁)))/(p₁−p₀))²", 54); END;` |
| 2079 | `IF TT==4 THEN fs1 := pv_Wrap("  n = ((zα"+SQG+"(2"+CHAR(57345)+"(1−"+CHAR(57345)+")) + zβ"+SQG+"(p₁(1−p₁)+p₂(1−p₂)))/(p₂−p₁))^2", 54); END;` | `IF TT==4 THEN fs1 := pv_Wrap("  n = ((zα"+SQG+"(2"+CHAR(57345)+"(1−"+CHAR(57345)+")) + zβ"+SQG+"(p₁(1−p₁)+p₂(1−p₂)))/(p₂−p₁))²", 54); END;` |
| 2107 | `IF TT==1 THEN fs3 := "(("+pv_NumD(SG)+"×"+pv_FMT(fza,3)+" + "+pv_NumD(SG)+"×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")^2"; END;` | `IF TT==1 THEN fs3 := "(("+pv_NumD(SG)+"×"+pv_FMT(fza,3)+" + "+pv_NumD(SG)+"×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")²"; END;` |
| 2108 | `IF TT==2 THEN fs3 := "(("+pv_NumD(SG)+SQG+"2×"+pv_FMT(fza,3)+" + "+pv_NumD(SG)+SQG+"2×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")^2"; END;` | `IF TT==2 THEN fs3 := "(("+pv_NumD(SG)+SQG+"2×"+pv_FMT(fza,3)+" + "+pv_NumD(SG)+SQG+"2×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")²"; END;` |
| 2109 | `IF TT==3 THEN fs3 := "(("+SQG+"("+pv_NumD(PP0*(1-PP0))+")×"+pv_FMT(fza,3)+" + "+SQG+"("+pv_NumD(PP1*(1-PP1))+")×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")^2"; END;` | `IF TT==3 THEN fs3 := "(("+SQG+"("+pv_NumD(PP0*(1-PP0))+")×"+pv_FMT(fza,3)+" + "+SQG+"("+pv_NumD(PP1*(1-PP1))+")×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")²"; END;` |
| 2112 | `fs3 := "(("+SQG+"("+pv_NumD(2*fnc*(1-fnc))+")×"+pv_FMT(fza,3)+" + "+SQG+"("+pv_NumD(PP0*(1-PP0)+PP1*(1-PP1))+")×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")^2";` | `fs3 := "(("+SQG+"("+pv_NumD(2*fnc*(1-fnc))+")×"+pv_FMT(fza,3)+" + "+SQG+"("+pv_NumD(PP0*(1-PP0)+PP1*(1-PP1))+")×"+pv_FMT(fzb,3)+")/"+pv_NumD(fdl)+")²";` |

## Checks

- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_PowerViz_v2.5d.py`: 160 of 174 checks pass. The 14 that fail compare the sample-size page with its old text ("…)^2 = 55.64" is now "…)² = 55.64"), the textbook form, or the version strings. Every n and every power passes.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the sample-size page for each of the four tests, with and without the CAS (the formula ends in )²), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
