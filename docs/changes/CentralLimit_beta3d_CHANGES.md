# CentralLimit beta 3d — changes

*20 October 2026. Built on beta 3c. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed", then "9 apps? check 20 please"). Every one of the 20 programs was checked for symbols spelled out in the text the student sees; in CentralLimit, the "Why the bell?" pages now use the house glyphs. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names, the "+/-" that names the + and − keys (the house footer), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow.

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 2235 | `cltPgAdd("CAS: as n grows, M(t) -> " + cltShow(mgL) + ":", #C800C8h);` | `cltPgAdd("CAS: as n grows, M(t) → " + cltShow(mgL) + ":", #C800C8h);` |
| 2241 | `cltPgAdd("   16, 10000) -> e^(1/2) = " + cltF(EXP(0.5), 4) + ", N(0, 1)'s MGF.", #5A5A5Ah);` | `cltPgAdd("   16, 10000) → e^(1/2) = " + cltF(EXP(0.5), 4) + ", N(0, 1)'s MGF.", #5A5A5Ah);` |
| 2253 | `cltPgAdd("   The t^4 term shrinks like 1/n; t^2/2 is left.", #008C3Ch);` | `cltPgAdd("   The t^4 term shrinks like 1/n; t²/2 is left.", #008C3Ch);` |
| 2314 | `TEXTOUT_P("e^(t^2/2): N(0, 1)", G1, 126, mgT0 + 14, 1, #003CC8h);` | `TEXTOUT_P("e^(t²/2): N(0, 1)", G1, 126, mgT0 + 14, 1, #003CC8h);` |
| 2417 | `TEXTOUT_P("  and its limit e^(t^2/2), the bell's MGF.", G1, 8, 167, 1, #C800C8h);` | `TEXTOUT_P("  and its limit e^(t²/2), the bell's MGF.", G1, 8, 167, 1, #C800C8h);` |

## Checks

- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_CentralLimit_beta3c.py`: 151 of 156 checks pass. The 5 that fail list the routines and code lines that changed, and the version strings. Every number passes.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open Menu → Why the bell? (the CAS lines with →, the MGF plot's legend e^(t²/2)), and the help page, and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
