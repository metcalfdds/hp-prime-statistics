# FDAES v3.9c — changes

*20 October 2026. Built on v3.9b. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner and every on-screen title or About line that names the version.

| Line (old) | Before | After |
| --- | --- | --- |
| 1377 | `"10" + " " + CHAR(215) + " sqrt(pi/2) = 12.5 yr"};` | `"10" + " " + CHAR(215) + " √(pi/2) = 12.5 yr"};` |
| 1826 | `"SE if independent sqrt(sum SD^2)/k,",` | `"SE if independent √(sum SD²)/k,",` |
| 1995 | `"B1 X + B2 X^2 (Table VIII intact,",` | `"B1 X + B2 X² (Table VIII intact,",` |
| 2007 | `"A = their mean; SA = (1/n) sqrt(sum",` | `"A = their mean; SA = (1/n) √(sum",` |
| 2039 | `"   is 10 " + CHAR(215) + " sqrt(pi/2) = 12.53, exact",` | `"   is 10 " + CHAR(215) + " √(pi/2) = 12.53, exact",` |
| 2100 | `"FDAES v3.9b has run on a PC test",` | `"FDAES v3.9c has run on a PC test",` |
| 2698 | `"sqrt(k). They are not: one child's",` | `"√(k). They are not: one child's",` |
| 4016 | `fdPage("FDAES v3.9b", {` | `fdPage("FDAES v3.9c", {` |
| 4874 | `"A = B0 + B1 X + B2 X^2",` | `"A = B0 + B1 X + B2 X²",` |
| 4940 | `"S_A = (1/n) sqrt(sum Sa^2 + 85n(n-1))",` | `"S_A = (1/n) √(sum Sa² + 85n(n-1))",` |
| 4941 | `"  = (1/" + STRING(SIZE(brAg), 1, 0) + ") sqrt(" + fdF2(brCb(3)) + " + " +` | `"  = (1/" + STRING(SIZE(brAg), 1, 0) + ") √(" + fdF2(brCb(3)) + " + " +` |
| 5202 | `"  SD " + fdF1(fdLamSD()) + " (by hand 10" + mlt + "sqrt(pi/2)",` | `"  SD " + fdF1(fdLamSD()) + " (by hand 10" + mlt + "√(pi/2)",` |
| 5237 | `"S_A = (1/2) sqrt(6.88^2 + 11.12^2",` | `"S_A = (1/2) √(6.88² + 11.12²",` |
| 5240 | `"(Without the 85: (1/2) sqrt(" + fdF2(brCb(3)) + ")",` | `"(Without the 85: (1/2) √(" + fdF2(brCb(3)) + ")",` |
| 5303 | `"  sqrt(" + fdF2(fdLvSD(1, 2, 6)) + "^2+" + fdF2(fdLvSD(1, 3, 7)) + "^2+" +` | `"  √(" + fdF2(fdLvSD(1, 2, 6)) + "²+" + fdF2(fdLvSD(1, 3, 7)) + "²+" +` |
| 5304 | `fdF2(fdLvSD(1, 4, 5)) + "^2)/3",` | `fdF2(fdLvSD(1, 4, 5)) + "²)/3",` |
| 5326 | `fdPage("ABOUT FDAES v3.9b", {` | `fdPage("ABOUT FDAES v3.9c", {` |
| 5533 | `"  error 10" + mlt + "sqrt(pi/2) = 12.53).",` | `"  error 10" + mlt + "√(pi/2) = 12.53).",` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version rather than given a new one. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

| Line (first-pass v3.9c) | Before | After |
| --- | --- | --- |
| 1176 | `bdTxt := "probably >= 18"; bdEdge := #008C3Ch; bdFill := #E8F6EBh;` | `bdTxt := ("probably " + CHAR(8805) + " 18"); bdEdge := #008C3Ch; bdFill := #E8F6EBh;` |
| 1186 | `TEXTOUT_P("P(age >= 18)" + fdEq(fdPctN(vp*100)) + "%  (cut-points " +` | `TEXTOUT_P(("P(age " + CHAR(8805) + " 18)") + fdEq(fdPctN(vp*100)) + "%  (cut-points " +` |
| 1222 | `znTxt := "reasonably confident >= 18 (grade H)";` | `znTxt := ("reasonably confident " + CHAR(8805) + " 18 (grade H)");` |
| 1387 | `"10" + " " + CHAR(215) + " √(pi/2) = 12.5 yr"};` | `"10" + " " + CHAR(215) + (" " + CHAR(8730) + "(" + CHAR(960) + "/2) = 12.5 yr")};` |
| 1779 | `"5  THE VERDICT BAND: P(age >= 18)",` | `("5  THE VERDICT BAND: P(age " + CHAR(8805) + " 18)"),` |
| 1780 | `"   >= 95% green 'probably >= 18';",` | `("   " + CHAR(8805) + " 95% green 'probably " + CHAR(8805) + " 18';"),` |
| 1781 | `"   <= 5% red 'probably < 18'; else",` | `("   " + CHAR(8804) + " 5% red 'probably < 18'; else"),` |
| 1816 | `"least about 15.8-16': no P(age >=",` | `("least about 15.8-16': no P(age " + CHAR(8805)),` |
| 1836 | `"SE if independent √(sum SD²)/k,",` | `("SE if independent " + CHAR(8730) + "(sum SD" + CHAR(178) + ")/k,"),` |
| 1907 | `"SD " + fdF1(fdLamSD()) + " P(age >= 18) is never",` | `"SD " + fdF1(fdLamSD()) + (" P(age " + CHAR(8805) + " 18) is never"),` |
| 1980 | `"normal); about 68% within +/-5.16.",` | `("normal); about 68% within " + CHAR(177) + "5.16."),` |
| 2004 | `"EQUATIONS (p 20): X <= 9.0 mm: B0 +",` | `("EQUATIONS (p 20): X " + CHAR(8804) + " 9.0 mm: B0 +"),` |
| 2005 | `"B1 X + B2 X² (Table VIII intact,",` | `("B1 X + B2 X" + CHAR(178) + " (Table VIII intact,"),` |
| 2014 | `"(p 24): A +/- 0.45 SA ca. 35%,",` | `("(p 24): A " + CHAR(177) + " 0.45 SA ca. 35%,"),` |
| 2015 | `"+/- SA ca. 65%, +/- 2 SA ca. 95%.",` | `(CHAR(177) + " SA ca. 65%, " + CHAR(177) + " 2 SA ca. 95%."),` |
| 2017 | `"A = their mean; SA = (1/n) √(sum",` | `("A = their mean; SA = (1/n) " + CHAR(8730) + "(sum"),` |
| 2018 | `"Sa^2 + 85 n(n-1)); 85 = 0.85 " + CHAR(215) + " 10 " + CHAR(215),` | `("Sa" + CHAR(178) + " + 85 n(n-1)); 85 = 0.85 ") + CHAR(215) + " 10 " + CHAR(215),` |
| 2028 | `"(p 9): 19 of 24 within +/- SA (p",` | `("(p 9): 19 of 24 within " + CHAR(177) + " SA (p"),` |
| 2036 | `"1  NORMAL ERRORS. Every mean +/- SD,",` | `("1  NORMAL ERRORS. Every mean " + CHAR(177) + " SD,"),` |
| 2038 | `"   P(age >= 18) treat a method's",` | `("   P(age " + CHAR(8805) + " 18) treat a method's"),` |
| 2049 | `"   is 10 " + CHAR(215) + " √(pi/2) = 12.53, exact",` | `"   is 10 " + CHAR(215) + (" " + CHAR(8730) + "(" + CHAR(960) + "/2) = 12.53, exact"),` |
| 2073 | `"   P(age >= 18) is a statement under",` | `("   P(age " + CHAR(8805) + " 18) is a statement under"),` |
| 2523 | `"No P(age >= 18), nothing to pool.",` | `("No P(age " + CHAR(8805) + " 18), nothing to pool."),` |
| 2533 | `"No P(age >= 18), nothing to pool."});` | `("No P(age " + CHAR(8805) + " 18), nothing to pool.")});` |
| 2656 | `"P(age >= 18) from N(" + fdF2(lpR(2)) + ", " + fdF2(lpR(4)) + ")."});` | `("P(age " + CHAR(8805) + " 18) from N(") + fdF2(lpR(2)) + ", " + fdF2(lpR(4)) + ")."});` |
| 2668 | `"so no P(age >= 18) band is drawn."});` | `("so no P(age " + CHAR(8805) + " 18) band is drawn.")});` |
| 2708 | `"√(k). They are not: one child's",` | `(CHAR(8730) + "(k). They are not: one child's"),` |
| 2896 | `"E  root shorter than crown", "F  root >= crown, apex wide",` | `"E  root shorter than crown", ("F  root " + CHAR(8805) + " crown, apex wide"),` |
| 2935 | `TEXTOUT_P(">=", G1, odCx - 6, odY1(odI) + 27, 1, odTx);` | `TEXTOUT_P(CHAR(8805), G1, odCx - 6, odY1(odI) + 27, 1, odTx);` |
| 3025 | `odL := "Willems 2001: at the ceiling, >= ~15.8-16 yr";` | `odL := ("Willems 2001: at the ceiling, " + CHAR(8805) + " ~15.8-16 yr");` |
| 3161 | `"F  root >= crown, apex wide",` | `("F  root " + CHAR(8805) + " crown, apex wide"),` |
| 3191 | `"mu = " + fdF1(pmu) + "  sd = " + fdF2(psd),` | `(CHAR(956) + " = ") + fdF1(pmu) + "  sd = " + fdF2(psd),` |
| 3193 | `"Age  P(>=age)  P(<age)",` | `("Age  P(" + CHAR(8805) + "age)  P(<age)"),` |
| 3333 | `TEXTOUT_P("P(age >= " + fdF1(poThr) + ")" + fdEq(fdPctN(poP*100)) + "%",` | `TEXTOUT_P(("P(age " + CHAR(8805) + " ") + fdF1(poThr) + ")" + fdEq(fdPctN(poP*100)) + "%",` |
| 3337 | `TEXTOUT_P(">= 16: " + fdPctN(NORMALD_CDF(pmu, psd, 2*pmu - 16)*100) +` | `TEXTOUT_P((CHAR(8805) + " 16: ") + fdPctN(NORMALD_CDF(pmu, psd, 2*pmu - 16)*100) +` |
| 3338 | `"%   >= 18: " + fdPctN(NORMALD_CDF(pmu, psd, 2*pmu - 18)*100) +` | `("%   " + CHAR(8805) + " 18: ") + fdPctN(NORMALD_CDF(pmu, psd, 2*pmu - 18)*100) +` |
| 3339 | `"%   >= 21: " + fdPctN(NORMALD_CDF(pmu, psd, 2*pmu - 21)*100) + "%",` | `("%   " + CHAR(8805) + " 21: ") + fdPctN(NORMALD_CDF(pmu, psd, 2*pmu - 21)*100) + "%",` |
| 3504 | `TEXTOUT_P("FOREST PLOT  estimate +/- 2 SD", G1, 6, 4, 2, #FFFFFFh, 308);` | `TEXTOUT_P(("FOREST PLOT  estimate " + CHAR(177) + " 2 SD"), G1, 6, 4, 2, #FFFFFFh, 308);` |
| 3582 | `foT2 := "inv-var SD x1.25 = " + fdF2(foRaw) + " < best single SD " + fdF2(foMin);` | `foT2 := ("inv-var SD " + CHAR(215) + "1.25 = ") + fdF2(foRaw) + " < best single SD " + fdF2(foMin);` |
| 3586 | `foT2 := "inv-var SD x1.25 = " + fdF2(foRaw) + " >= best single SD " + fdF2(foMin);` | `foT2 := ("inv-var SD " + CHAR(215) + "1.25 = ") + fdF2(foRaw) + (" " + CHAR(8805) + " best single SD ") + fdF2(foMin);` |
| 3644 | `mbL := "M3  P(age >= 18): " + mbJn;              // mbJn is a word` | `mbL := "M3  P(age " + CHAR(8805) + " 18): " + mbJn;              // mbJn is a word` |
| 3755 | `"1993, Table 4 (p 384): P(age >= 18)",` | `("1993, Table 4 (p 384): P(age " + CHAR(8805) + " 18)"),` |
| 4056 | `"M3 Threshold  P(age >= 18)",` | `("M3 Threshold  P(age " + CHAR(8805) + " 18)"),` |
| 4291 | `"F  root >= crown, apex wide",` | `("F  root " + CHAR(8805) + " crown, apex wide"),` |
| 4312 | `"P(age >= 18), males   = " + fdPct(m3pm(m3c - 1)) + "%",` | `("P(age " + CHAR(8805) + " 18), males   = ") + fdPct(m3pm(m3c - 1)) + "%",` |
| 4313 | `"P(age >= 18), females = " + fdPct(m3pf(m3c - 1)) + "%",` | `("P(age " + CHAR(8805) + " 18), females = ") + fdPct(m3pf(m3c - 1)) + "%",` |
| 4319 | `"P(age >= 18) = " + fdPct(m3p) + "%",` | `("P(age " + CHAR(8805) + " 18) = ") + fdPct(m3p) + "%",` |
| 4336 | `m3L := CONCAT(m3L, {"==> Reasonably confident >= 18.",` | `m3L := CONCAT(m3L, {("==> Reasonably confident " + CHAR(8805) + " 18."),` |
| 4516 | `"P(age >= 18) never below " +` | `("P(age " + CHAR(8805) + " 18) never below ") +` |
| 4575 | `"T * 8.98  Root Transparency [BEST]",` | `("T " + CHAR(215) + " 8.98  Root Transparency [BEST]"),` |
| 4576 | `"R * 5.57  Root Resorption",` | `("R " + CHAR(215) + " 5.57  Root Resorption"),` |
| 4577 | `"A * 5.14  Attrition",` | `("A " + CHAR(215) + " 5.14  Attrition"),` |
| 4578 | `"P * 4.14  Periodontosis",` | `("P " + CHAR(215) + " 4.14  Periodontosis"),` |
| 4579 | `"C * 3.71  Cementum Apposition",` | `("C " + CHAR(215) + " 3.71  Cementum Apposition"),` |
| 4580 | `"S * 2.30  Secondary Dentin [LEAST]",` | `("S " + CHAR(215) + " 2.30  Secondary Dentin [LEAST]"),` |
| 4768 | `"X <= 9.0 mm: the 2nd-degree",` | `("X " + CHAR(8804) + " 9.0 mm: the 2nd-degree"),` |
| 4883 | `brL := CONCAT(brL, {"X = " + fdF2(brX) + " mm, <= 9.0: 2nd degree",` | `brL := CONCAT(brL, {"X = " + fdF2(brX) + (" mm, " + CHAR(8804) + " 9.0: 2nd degree"),` |
| 4884 | `"A = B0 + B1 X + B2 X²",` | `("A = B0 + B1 X + B2 X" + CHAR(178)),` |
| 4902 | `"  A +/- 0.45 SA = [" + fdF1(MAX(0, brV(1) - 0.45*brV(2))) + ", " +` | `("  A " + CHAR(177) + " 0.45 SA = [") + fdF1(MAX(0, brV(1) - 0.45*brV(2))) + ", " +` |
| 4950 | `"S_A = (1/n) √(sum Sa² + 85n(n-1))",` | `("S_A = (1/n) " + CHAR(8730) + "(sum Sa" + CHAR(178) + " + 85n(n-1))"),` |
| 4951 | `"  = (1/" + STRING(SIZE(brAg), 1, 0) + ") √(" + fdF2(brCb(3)) + " + " +` | `"  = (1/" + STRING(SIZE(brAg), 1, 0) + (") " + CHAR(8730) + "(") + fdF2(brCb(3)) + " + " +` |
| 5070 | `"P(age >= 16): " + fdPctN(p16) + "%",` | `("P(age " + CHAR(8805) + " 16): ") + fdPctN(p16) + "%",` |
| 5071 | `"P(age >= 18): " + fdPctN(p18) + "%",` | `("P(age " + CHAR(8805) + " 18): ") + fdPctN(p18) + "%",` |
| 5072 | `"P(age >= 21): " + fdPctN(p21) + "%",` | `("P(age " + CHAR(8805) + " 21): ") + fdPctN(p21) + "%",` |
| 5088 | `wmsg := CONCAT(wmsg, {"Floor not needed (SD >= best SD)"});` | `wmsg := CONCAT(wmsg, {("Floor not needed (SD " + CHAR(8805) + " best SD)")});` |
| 5125 | `"P(age >= 18): " + fdPctN(p18) + "%",` | `("P(age " + CHAR(8805) + " 18): ") + fdPctN(p18) + "%",` |
| 5212 | `"  SD " + fdF1(fdLamSD()) + " (by hand 10" + mlt + "√(pi/2)",` | `"  SD " + fdF1(fdLamSD()) + " (by hand 10" + mlt + (CHAR(8730) + "(" + CHAR(960) + "/2)"),` |
| 5233 | `"(<= 9.0: Table IX, row 9):",` | `("(" + CHAR(8804) + " 9.0: Table IX, row 9):"),` |
| 5247 | `"S_A = (1/2) √(6.88² + 11.12²",` | `("S_A = (1/2) " + CHAR(8730) + "(6.88" + CHAR(178) + " + 11.12" + CHAR(178)),` |
| 5250 | `"(Without the 85: (1/2) √(" + fdF2(brCb(3)) + ")",` | `("(Without the 85: (1/2) " + CHAR(8730) + "(") + fdF2(brCb(3)) + ")",` |
| 5288 | `"M3 Table 4 (erratum), P(>=18) %:",` | `("M3 Table 4 (erratum), P(" + CHAR(8805) + "18) %:"),` |
| 5313 | `"  √(" + fdF2(fdLvSD(1, 2, 6)) + "²+" + fdF2(fdLvSD(1, 3, 7)) + "²+" +` | `("  " + CHAR(8730) + "(") + fdF2(fdLvSD(1, 2, 6)) + (CHAR(178) + "+") + fdF2(fdLvSD(1, 3, 7)) + (CHAR(178) + "+") +` |
| 5314 | `fdF2(fdLvSD(1, 4, 5)) + "²)/3",` | `fdF2(fdLvSD(1, 4, 5)) + (CHAR(178) + ")/3"),` |
| 5365 | `"  (pp 47-49); error +/-3.63 yr (p 51)",` | `("  (pp 47-49); error " + CHAR(177) + "3.63 yr (p 51)"),` |
| 5369 | `"  on real ages: SE +/-7.03 (p 170).",` | `("  on real ages: SE " + CHAR(177) + "7.03 (p 170)."),` |
| 5374 | `"  aged 42-79: mean error 14.2 +/-",` | `("  aged 42-79: mean error 14.2 " + CHAR(177)),` |
| 5375 | `"  3.4 yr (his own: 8.9 +/- 2.2).",` | `("  3.4 yr (his own: 8.9 " + CHAR(177) + " 2.2)."),` |
| 5380 | `"  one observer: +/-3.37 yr (p 52)."});` | `("  one observer: " + CHAR(177) + "3.37 yr (p 52).")});` |
| 5421 | `"w_i = 1/sigma_i^2",` | `("w_i = 1/" + CHAR(963) + "_i" + CHAR(178)),` |
| 5422 | `"mu = SUM(mu_i*w_i) / SUM(w_i)",` | `(CHAR(956) + " = SUM(" + CHAR(956) + "_i" + CHAR(215) + "w_i) / SUM(w_i)"),` |
| 5423 | `"SD = SQRT(1/SUM(w_i)) * 1.25",` | `("SD = " + CHAR(8730) + "(1/SUM(w_i)) " + CHAR(215) + " 1.25"),` |
| 5434 | `"P(age >= t): the lower tail",` | `("P(age " + CHAR(8805) + " t): the lower tail"),` |
| 5435 | `"  NORMALD_CDF(mu, sd, 2mu - t),",` | `("  NORMALD_CDF(" + CHAR(956) + ", sd, 2" + CHAR(956) + " " + CHAR(8722) + " t),"),` |
| 5436 | `"  the same as 1 - NORMALD_CDF(mu,",` | `("  the same as 1 - NORMALD_CDF(" + CHAR(956) + ","),` |
| 5445 | `"Willems stage index +5 -> +6.",` | `("Willems stage index +5 " + CHAR(8594) + " +6."),` |
| 5477 | `"  P(age >= t) follows, snaps 0.5 yr.",` | `("  P(age " + CHAR(8805) + " t) follows, snaps 0.5 yr."),` |
| 5479 | `"Forest: each method +/- 2 SD, the",` | `("Forest: each method " + CHAR(177) + " 2 SD, the"),` |
| 5483 | `"Verdict band: green P >= 83%,",` | `("Verdict band: green P " + CHAR(8805) + " 83%,"),` |
| 5485 | `"  95% / 5%), P = P(age >= 18)."});` | `("  95% / 5%), P = P(age " + CHAR(8805) + " 18).")});` |
| 5508 | `"  H reasonably confident >= 18",` | `("  H reasonably confident " + CHAR(8805) + " 18"),` |
| 5543 | `"  error 10" + mlt + "√(pi/2) = 12.53).",` | `"  error 10" + mlt + (CHAR(8730) + "(" + CHAR(960) + "/2) = 12.53)."),` |
| 5604 | `"], P(age >= 18)" + fdEq(fdPctN(p18)) + "%";` | `("], P(age " + CHAR(8805) + " 18)") + fdEq(fdPctN(p18)) + "%";` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports one problem more than v3.9b (4 to 5): line 3652, "assignment to mbL concatenates bare mbJn", a false positive, since mbJn is the word "mandible" or "maxilla" and the linter does not follow a chain through `CHAR()` (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_FDAES_v3.9b.py`, run on v3.9c with the drawn text mapped back to the words it replaced (`shim3_run.py`; the script reads a copy with the `CHAR()` builds folded back into literals, the harness runs the real file): 3,139 of 3,212 checks pass, every age, SD, probability, band and pool among them. The 73 that fail are of three kinds: 49 compare menus, dialogs or the Home summary, which the mapping does not reach ("M3 Threshold  P(age ≥ 18)", "P(age ≥ 18) < 0.1%"); 19 read the source itself (the routines and lines that changed, the version strings, "the file is ASCII" on the folded copy); 5 look for an old phrase ("10 x sqrt(pi/2)") or rerun the review's text checks. Unmapped, the same script fails 866 checks, every one on a changed character.
- Not yet on a calculator.
- **This program keeps its code pure ASCII** (its other display glyphs are built with `CHAR()`), so the new glyphs are built the same way, for example `("P(age " + CHAR(8805) + " 18)")`; on screen it is the same character. `ascii_fix_2026-10-20.py` did it and checked that folding the builds back gives the swept text exactly; the gate and the verify script then ran again on the rebuilt file.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open every P(age ≥ 18) line, the verdict-band help, the history pages (±), the inverse-variance page (×1.25, μ, σ), the Lamendin SD page (√(π/2)) and the Bayesian framework page, and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
3. **New glyphs: π.** These have not been seen on the calculator's screen in a program before. If any shows as a box, tell Claude: the word goes back in, nothing else changes.
