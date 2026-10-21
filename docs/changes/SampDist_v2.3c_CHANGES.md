# SampDist v2.3c — changes

*20 October 2026. Built on v2.3b. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed", then "9 apps? check 20 please"). Every one of the 20 programs was checked for symbols spelled out in the text the student sees; in SampDist, the sample-size prompts now use the house glyphs. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names, the "+/-" that names the + and − keys (the house footer), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow.

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 956 | `"Sample size, whole number >= 1", "Tail area, e.g. 0.05"});` | `"Sample size, whole number ≥ 1", "Tail area, e.g. 0.05"});` |
| 961 | `"Sample size, whole number >= 1"});` | `"Sample size, whole number ≥ 1"});` |
| 968 | `IF nn2 < 1 THEN MSGBOX("n must be >= 1; nothing changed"); END;` | `IF nn2 < 1 THEN MSGBOX("n must be ≥ 1; nothing changed"); END;` |
| 1256 | `"Sample size, whole number >= 1"});` | `"Sample size, whole number ≥ 1"});` |
| 1259 | `IF nn < 1 THEN MSGBOX("n must be >= 1"); RETURN; END;` | `IF nn < 1 THEN MSGBOX("n must be ≥ 1"); RETURN; END;` |
| 1322 | `"Sample size, whole number >= 1", "Tail area, e.g. 0.05"});` | `"Sample size, whole number ≥ 1", "Tail area, e.g. 0.05"});` |
| 1325 | `IF nn < 1 THEN MSGBOX("n must be >= 1"); RETURN; END;` | `IF nn < 1 THEN MSGBOX("n must be ≥ 1"); RETURN; END;` |
| 1377 | `MSGBOX("every n must be >= 1"); RETURN;` | `MSGBOX("every n must be ≥ 1"); RETURN;` |
| 1419 | `"Draws per sample, whole number >= 1"});` | `"Draws per sample, whole number ≥ 1"});` |
| 1422 | `IF nn < 1 THEN MSGBOX("n must be >= 1"); RETURN; END;` | `IF nn < 1 THEN MSGBOX("n must be ≥ 1"); RETURN; END;` |

## Checks

- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_SampDist_v2.3b.py`: 351 of 354 checks pass. The 3 that fail say "only sd_fix changed", "exactly the two code lines of S1 and S2 changed" and the version strings.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open every sample-size input box and its error message ("whole number ≥ 1", "n must be ≥ 1"), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
