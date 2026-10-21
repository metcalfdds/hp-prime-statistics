# DNAMixLR beta 3d — changes

*20 October 2026. Built on beta 3c. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed", then "9 apps? check 20 please"). Every one of the 20 programs was checked for symbols spelled out in the text the student sees; in DNAMixLR, every "theta" (and the formula's "th") now use the house glyphs. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names, the "+/-" that names the + and − keys (the house footer), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow.

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 1512 | `IF INPUT({stT}, "Coancestry coefficient", {"theta:"},` | `IF INPUT({stT}, "Coancestry coefficient", {(CHAR(952) + ":")},` |
| 1515 | `MSGBOX("theta must be at least 0 and well below 0.5; 0.01 to 0.03 is the usual range.");` | `MSGBOX((CHAR(952) + " must be at least 0 and well below 0.5; 0.01 to 0.03 is the usual range."));` |
| 1990 | `TEXTOUT_P("log10 LR against theta", G2, 24, 2, 2, dmBLUE);` | `TEXTOUT_P(("log10 LR against " + CHAR(952)), G2, 24, 2, 2, dmBLUE);` |
| 2052 | `tsS2 := "at theta " + dmF(dmEdT, 4);` | `tsS2 := ("at " + CHAR(952) + " ") + dmF(dmEdT, 4);` |
| 2054 | `tsS2 := "at theta " + dmF(dmEdT, 4) + " (off plot)";` | `tsS2 := ("at " + CHAR(952) + " ") + dmF(dmEdT, 4) + " (off plot)";` |
| 2061 | `TEXTOUT_P("up to theta 0.25", G2, dmP2R - 98, dmP2T + 12, 1, dmORNG);` | `TEXTOUT_P(("up to " + CHAR(952) + " 0.25"), G2, dmP2R - 98, dmP2T + 12, 1, dmORNG);` |
| 2073 | `TEXTOUT_P("drag or Left/Right = theta, Ent = adopt, Esc = menu", G2, 4, 206, 1, dmFOOT, 312);` | `TEXTOUT_P(("drag or Left/Right = " + CHAR(952) + ", Ent = adopt, Esc = menu"), G2, 4, 206, 1, dmFOOT, 312);` |
| 2093 | `TEXTOUT_P("theta " + dmF(tfTh, 4), G1, 4, 20, 1, dmGRN);` | `TEXTOUT_P((CHAR(952) + " ") + dmF(tfTh, 4), G1, 4, 20, 1, dmGRN);` |
| 2103 | `TEXTOUT_P("your theta " + dmThS(dmTh) + " is off the plot: drag", G1, 4, 20, 1, dmGRN);` | `TEXTOUT_P(("your " + CHAR(952) + " ") + dmThS(dmTh) + " is off the plot: drag", G1, 4, 20, 1, dmGRN);` |
| 2230 | `TEXTOUT_P("theta = " + dmThS(dmTh), G1, 12, 33, 1, dmGRAY);` | `TEXTOUT_P((CHAR(952) + " = ") + dmThS(dmTh), G1, 12, 33, 1, dmGRAY);` |
| 2493 | `TEXTOUT_P("LR as a formula in p and " + dmTHG + " (theta):", G1, 10, fxY, 1, #000000h, 230);` | `TEXTOUT_P("LR as a formula in p and " + dmTHG + ":", G1, 10, fxY, 1, #000000h, 230);` |
| 2520 | `TEXTOUT_P("LR = 0 for every p and theta: a known", G1, 10, fxY, 1, dmRED, 300);` | `TEXTOUT_P(("LR = 0 for every p and " + CHAR(952) + ": a known"), G1, 10, fxY, 1, dmRED, 300);` |
| 2525 | `TEXTOUT_P("LR = 0 for every p and theta: under Hp", G1, 10, fxY, 1, dmRED, 300);` | `TEXTOUT_P(("LR = 0 for every p and " + CHAR(952) + ": under Hp"), G1, 10, fxY, 1, dmRED, 300);` |
| 2530 | `TEXTOUT_P("LR = 0 at these p and theta: P(E\|Hp) is", G1, 10, fxY, 1, dmRED, 300);` | `TEXTOUT_P(("LR = 0 at these p and " + CHAR(952) + ": P(E\|Hp) is"), G1, 10, fxY, 1, dmRED, 300);` |
| 2537 | `TEXTOUT_P("for every p and theta, so no LR, no formula.", G1, 10, fxY + 11, 1, dmRED, 300);` | `TEXTOUT_P(("for every p and " + CHAR(952) + ", so no LR, no formula."), G1, 10, fxY + 11, 1, dmRED, 300);` |
| 2556 | `IF dmFxS == 1 THEN fxS := "With theta: " + STRING(DIM(dmFxT), 2, 0) + " characters, too long to show."; END;` | `IF dmFxS == 1 THEN fxS := ("With " + CHAR(952) + ": ") + STRING(DIM(dmFxT), 2, 0) + " characters, too long to show."; END;` |
| 2565 | `fxL := dmWrap("theta = 0: LR = " + dmFxShow(dmF0T), 48);` | `fxL := dmWrap((CHAR(952) + " = 0: LR = ") + dmFxShow(dmF0T), 48);` |
| 2572 | `TEXTOUT_P("At theta = 0: " + STRING(DIM(dmF0T), 2, 0) + " characters, too long to show.", G1, 10, fxY, 1, dmGRAY, 304);` | `TEXTOUT_P(("At " + CHAR(952) + " = 0: ") + STRING(DIM(dmF0T), 2, 0) + " characters, too long to show.", G1, 10, fxY, 1, dmGRAY, 304);` |
| 2607 | `TEXTOUT_P("theta = " + dmThS(dmTh), G1, 210, 8, 1, dmGRAY);` | `TEXTOUT_P((CHAR(952) + " = ") + dmThS(dmTh), G1, 210, 8, 1, dmGRAY);` |
| 2719 | `TEXTOUT_P("theta = 0: plain p, the product rule.  Next allele", G1, 10, dmPcY + 39, 1, dmGRAY, 300);` | `TEXTOUT_P((CHAR(952) + " = 0: plain p, the product rule.  Next allele"), G1, 10, dmPcY + 39, 1, dmGRAY, 300);` |
| 2724 | `TEXTOUT_P("plain p = " + dmF(dmFq(dpA), 3) + " becomes " + dmF(dpQ, 3) + " with theta", G1, 10, dmPcY + 61, 1, dmMAG, 300);` | `TEXTOUT_P("plain p = " + dmF(dmFq(dpA), 3) + " becomes " + dmF(dpQ, 3) + (" with " + CHAR(952)), G1, 10, dmPcY + 61, 1, dmMAG, 300);` |
| 2737 | `TEXTOUT_P("single source: LR = 1/(2pq) or 1/p^2 = 1/RMP", G1, 12, dmPcY + 83, 1, dmGRN, 300);` | `TEXTOUT_P(("single source: LR = 1/(2pq) or 1/p" + CHAR(178) + " = 1/RMP"), G1, 12, dmPcY + 83, 1, dmGRN, 300);` |
| 2739 | `TEXTOUT_P("single source: LR = 1/RMP, theta-corrected", G1, 12, dmPcY + 83, 1, dmGRN, 300);` | `TEXTOUT_P(("single source: LR = 1/RMP, " + CHAR(952) + "-corrected"), G1, 12, dmPcY + 83, 1, dmGRN, 300);` |
| 3059 | `MSGBOX("Loaded: victim + suspect vs victim + 1 unknown, 3 loci, theta = " + dmThS(dmTh) + ".  Locus 1: victim 12/13, suspect 14/15, mixture 12,13,14,15.  Now see Results and the plots.");` | `MSGBOX(("Loaded: victim + suspect vs victim + 1 unknown, 3 loci, " + CHAR(952) + " = ") + dmThS(dmTh) + ".  Locus 1: victim 12/13, suspect 14/15, mixture 12,13,14,15.  Now see Results and the plots.");` |
| 3096 | `TEXTOUT_P("0.03 conservative.  The theta plot shows how", G1, 12, 115, 1, #000000h);` | `TEXTOUT_P(("0.03 conservative.  The " + CHAR(952) + " plot shows how"), G1, 12, 115, 1, #000000h);` |
| 3097 | `TEXTOUT_P("much the LR falls as theta rises.", G1, 12, 128, 1, #000000h);` | `TEXTOUT_P(("much the LR falls as " + CHAR(952) + " rises."), G1, 12, 128, 1, #000000h);` |
| 3113 | `TEXTOUT_P("LR and the ladder follow.  Ent adopts theta.", G1, 12, 96, 1, dmGRN);` | `TEXTOUT_P(("LR and the ladder follow.  Ent adopts " + CHAR(952) + "."), G1, 12, 96, 1, dmGRN);` |
| 3127 | `TEXTOUT_P("in the allele frequencies p and theta (th),", G1, 12, 50, 1, dmMAG);` | `TEXTOUT_P(("in the allele frequencies p and " + CHAR(952) + ","), G1, 12, 50, 1, dmMAG);` |
| 3130 | `TEXTOUT_P("simplifies it.  At theta = 0 it is the product", G1, 12, 76, 1, dmBLUE);` | `TEXTOUT_P(("simplifies it.  At " + CHAR(952) + " = 0 it is the product"), G1, 12, 76, 1, dmBLUE);` |
| 3134 | `TEXTOUT_P("BAND EDGE (theta plot, orange): the theta at", G1, 12, 131, 1, dmORNG);` | `TEXTOUT_P(("BAND EDGE (" + CHAR(952) + " plot, orange): the " + CHAR(952) + " at"), G1, 12, 131, 1, dmORNG);` |
| 3136 | `TEXTOUT_P("band edge as theta rises from yours: how far", G1, 12, 157, 1, dmORNG);` | `TEXTOUT_P(("band edge as " + CHAR(952) + " rises from yours: how far"), G1, 12, 157, 1, dmORNG);` |
| 3137 | `TEXTOUT_P("theta must go before the words change.", G1, 12, 170, 1, dmORNG);` | `TEXTOUT_P((CHAR(952) + " must go before the words change."), G1, 12, 170, 1, dmORNG);` |
| 3202 | `dmTHG := "th";                                           // CHAR(952) after GfxProbe T14` | `dmTHG := CHAR(952);                                      // theta: GfxProbe T14 renders it` |
| 3314 | `"Coancestry theta = " + dmThS(dmTh),` | `("Coancestry " + CHAR(952) + " = ") + dmThS(dmTh),` |
| 3317 | `"Plot: LR against theta (drag)",` | `("Plot: LR against " + CHAR(952) + " (drag)"),` |
| 3342 | `mnS := mnS + ", theta = " + dmThS(dmTh);` | `mnS := mnS + (", " + CHAR(952) + " = ") + dmThS(dmTh);` |

**One code line:** `dmTHG`, the way θ is written in a formula, was `"th"` "until GfxProbe T14 shows that CHAR(952) renders" (beta 3c's own comment). T14 showed it does (Virtual Calculator, 17 Oct 2026), so `dmTHG := CHAR(952)`. The CAS still receives `dmt`; only the text shown is θ.

## Checks

- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_DNAMixLR_beta3c.py`: 167 of 188 checks pass. The 21 that fail look for "theta" on a page that now says θ ("LR as a formula in p and θ:", "θ = 0: LR = …"), or for "only these lines changed". Every LR passes.
- Not yet on a calculator.
- **This program keeps its code pure ASCII** (its other display glyphs are built with `CHAR()`), so the new glyphs are built the same way, for example `("P(age " + CHAR(8805) + " 18)")`; on screen it is the same character. `ascii_fix_2026-10-20.py` did it and checked that folding the builds back gives the swept text exactly; the gate and the verify script then ran again on the rebuilt file.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the θ input box, the LR-against-θ plot and its footer, the formula page ("LR as a formula in p and θ:" and the formula itself, which now writes θ where it wrote th), the summary page and the help pages, and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
