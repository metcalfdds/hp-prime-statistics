# Round-2 tests on the HP Prime Virtual Calculator (17 October 2026)

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). Run by Claude through computer use on Rogers-HP, 17 October 2026, 11:35–12:40 (CDT); the fix versions were retested the same afternoon, 14:30–15:30 (v2 adds that retest, below, and corrects the minus sign in fact 2).*

**The emulator:** HP Prime Virtual Calculator 2.4.2, build 2026-09-09 — the calculators' own firmware (round 1 has the details). **What was tested:** the versions that became current after round 1 (the "a" and "b" fix versions), and CentralLimit as an app. **How:** each file was opened from `FIXED_FOR_DEVICE` in Notepad, copied, pasted over the program in the Connectivity Kit and saved; run from Home by pasting its name. Every number below was checked against SciPy or exact arithmetic.

---

## Summary

| Program | Version | Result |
|---|---|---|
| BayesTree | beta 8b | **Soft keys fire; rounding fixed; CAS exact.** Two small event bugs, cosmetic items |
| StudRange | beta 15a | **Plot soft keys fire**; the same small event bug; Quit summary ignores the plot |
| GaltonBoard | beta 3b | **PASS**: solid pegs and balls; Poisson-limit CAS page exact |
| TrendTest | beta 3b | Dots solid; **CAS page 4 stops the program** ("Invalid input"); a scientific-notation readout |
| StatDist | v2.7b | **PASS**: χ² and F at df 2.5; the CAS formula page exact |
| ChiTable | beta 3b | **Does not compile** (comments inside a CHOOSE list); with them removed, every CAS page exact |
| CICatcher | beta 2a | **PASS**: the CAS end-point `1−(1/40)^(1/20) = 0.1684`, exact; one menu line cut |
| DNAMixLR | beta 3a | **PASS**: the LR formula from the CAS; one menu line still cut |
| EpiStats | v1.7a | **PASS**: Help F (the delta method) exact, `53/120` |
| ScatterLab | beta 2a | **The calculus page stops the program** ("Invalid input"), the same cause as TrendTest |
| PowerViz | v2.5a | **PASS**: "Where n comes from", exact |
| CentralLimit | beta 3a (app) | **PASS — first run as an app**: dashboard, samples, the exact curve and the MGF page |

**Five new facts about the Prime** (typed in Home to confirm; they go into Lessons Learned v7i):

| Typed in Home | Answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `INSTRING("abc", "")` / `INSTRING("abc", "z")` | 1 / 0 |
| `LEFT("abc", 0)`, `RIGHT("abc", 0)` | `"abc"` (the whole string) |
| `MID("abc", 0, 1)` | **Error: Bad argument type** |
| `MID("abc", 4)`, `MID("", 1, 1)`, `MID("abc", 2, 0)` | `""` |
| `STRING(0.096, 2, 1)`, `STRING(0.0999, 2, 1)`, `STRING(0.05, 2, 1)` | `"9.6ᴇ−2"`, `"1.0ᴇ−1"`, `"5.0ᴇ−2"` |
| `STRING(0.0004, 2, 3)`, `STRING(0.00099, 2, 3)` | `"4.000ᴇ−4"`, `"9.900ᴇ−4"` |
| `STRING(0.1, 2, 1)`, `STRING(0.001, 2, 3)`, `STRING(0, 2, 3)`, `STRING(0.00041, 2, 5)` | `"0.1"`, `"0.001"`, `"0.000"`, `"0.00041"` |
| `STRING(123456789012, 2, 2)`, `STRING(1E15, 2, 0)`, `STRING(99999.5, 2, 0)` | `"123456789012"`, `"1ᴇ15"`, `"100000"` |

1. **`INSTRING` on an empty string is a run-time error.** Every program's CAS fallback (`INSTRING(cR, "undef")` after a failed call) would stop the program, and so does any replace loop that searches what is left of a string once the pattern was its last character (TrendTest, ScatterLab).
2. **Fixed decimals turn scientific below 10⁻ᵈ**: `STRING(x, 2, d)` prints `9.6ᴇ−2` whenever 0 < |x| < 10⁻ᵈ (the E is U+1D07, and the exponent's minus is U+2212, CHAR(8722), not a hyphen: v1 of this report transcribed it as a hyphen; CASProbe beta 1c read the codes, below). `STRING(ROUND(x, d), 2, d)` is the safe form. Fixed output also holds 12 significant digits at most, and from 1E12 it is scientific.
3. **A `//` comment inside an open bracket is a syntax error.** ChiTable beta 3b's two comment lines inside a CHOOSE list stopped it compiling; with them removed it compiled and ran.
4. **Under `WAIT(-1)`, a tap on the bottom strip (y ≥ 218) arrives only as a type-3 click even on a screen that draws no soft keys** (BayesTree's ROC view, after the tree had drawn its DRAWMENU), so a view that closes on a type-0 press outside its plot ignores a footer tap.
5. **A tap read through `MOUSE` (a page held by `xxWaitAny`) leaves no click for the next `WAIT(-1)`.** BayesTree and StudRange expect one and skip the next real tap at the same spot.

The PC harness models 1 and 2 since **ppl_run_v3d** (and the exponent's Unicode minus since **v3e**), and the gate catches 3 since **ppl_check_v4 E12** (`ppl_gate_v1b.py`). Under v3d, every CAS program's `cas='fail'` run stops at the empty INSTRING, as the calculator would.

---

## BayesTree beta 8b

| Item | Result |
|---|---|
| First frame | PASS: prior 0.100, sens 0.90, spec 0.95 → T+ 90, T− 10, T+ 45, T− 855; PPV = **2/3**, NPV = **171/173**, "exact (CAS), tap"; "Most T+ are false if prior < 5.3 %" (1/19); the first-level numbers right of the branch lines (fixed) |
| **Soft keys** | **PASS**: Values (form), Counts, ROC, PPV, 2×2, More (pages 2 and 3), Diag, Fagan, Icons, 3 prev, Help, Test 2, Reset, Forensic, Leaves, Exact all open from a tap |
| **Rounding** | **PASS**: sens 0.835 → T+ **84**, T− **16** (the round-1 slip gave 17); at prior 0.292, 244 + 48 = 292 and 35 + 673 = 708; the 2×2 view adds up (84/16/100, 45/855/900, 129/871/1000) |
| CAS | PPV = 167/257, NPV = 570/581; prior 0.292: 12191/13961, 11210/12013; break-even 5.6 %; two tests: break-even 0.36 % = 100/27989, Exact and Bayes pages — all exact and correct |
| Views | ROC: d′ 2.619, AUC 0.968. PPV view: the break-even mark, a drag to prior 0.292 (PPV 0.873, NPV 0.933). Fagan: a drag to prior 0.041 (PPV 0.417). Icon array: TP 34, FP 48, FN 7, TN 911. Three prevalences: 0.016, 0.144, 0.650. Diagnostics: accuracy 0.916, balanced 0.893, J 0.785, NND 1.274, DOR 96.15, F1 0.854, MCC 0.796, κ 0.795. All correct |
| Stale clicks | PASS where they are real: the ROC view closed by a tap at its top right (on the tree's slider) moved nothing; a node page closed by a tap on the D− box opened nothing |
| Slider and branch drags | PASS (a drag needs several move events; one fast mouse drag with a single move changes nothing — an emulator artefact, a finger sends many) |
| Exit | "BayesTree: PPV = 0.667 = 2/3, NPV = 0.988 (prior …" |

**Bugs:**
1. **A real tap is skipped once.** Close the 2×2 view by tapping its footer at the ROC key's spot, then tap ROC at the same spot: nothing; a second tap opens ROC. `bt_WaitAny` puts its closing tap on the stale-click list, but no click from a MOUSE-read tap ever reaches `WAIT(-1)`, so the entry waits for a real tap at that spot (±2 px) and eats it. Rare with a finger, common with a mouse.
2. **The ROC, PPV and Fagan views ignore a tap on their footer** (fact 4). Their footers say "Esc = back", so nothing is lost, but "tap outside = back" stops at y 218.
3. **Text:** the Diagnostics page says "use ConTable2" (now in EpiStats); the two-test breadcrumb's arrows are covered by the next number ("0.04 –0.42 –0.92"); the two-test Exact page's second line runs off the right edge; the soft-key label "Forensic" is cut ("Forensi").

One unexplained miss: on the very first run, the first tap on Values did nothing; it did not happen again in three restarts.

## StudRange beta 15a

| Item | Result |
|---|---|
| Distribution plot (k 3, ν 12, q 3.5) | PASS: q crit 3.773, p 0.0700, "engine: MicroPython 1.9.4" |
| **Soft keys** | **PASS**: α+ (α 0.100, q crit 3.204), k+ (k 4: q crit 3.620, p 0.1151), df (ν 1230: q crit 3.244, p 0.0643), α− (q crit 3.638), Menu. All = SciPy |
| Plot menu, Help for this plot | PASS |
| **Stale click** | **The same bug as BayesTree**: close the plot's help page by tapping the footer at the α− spot, then tap α−: skipped once, then works |
| Quit summary | "StudRange: q crit not computed, p not computed, HSD not computed (engine: …)" after a session that used only the plot — the plot's values don't count |

## GaltonBoard beta 3b — PASS

Pegs and balls are **solid** (a ball caught mid-fall: a solid red disc with its pale trail). Drop → "R L L R L L R L → 3 rights → bin 3". Menu → Where Poisson comes from (CAS): the limit **32/(3·e⁴)** for k = 4 and **1024/(315·e⁴)** for k = 7, "exact (CAS)"; P(4) for R = 8, 32, 128 and Poisson = 0.2734, 0.2088, 0.1985, 0.1954 (= SciPy). *Cosmetic:* four main-menu items are cut at the box's right edge ("Overlays: none / binomial / + n…", "…distance from Rp", "Pascal's triangle: off / counts…", "Send bins to D1, D2 (Statistics…"); the exit line says "1 balls".

## TrendTest beta 3b

Examples → Snoring: results page 1 (trend χ² 72.659, Pearson 72.782, departure 0.123, as round 1); "(made up)" now fits. Proportions plot and OR plot: **solid dots** (fixed). **Results page 4 (the CAS page): "Error: Invalid input", the program stopped** (fact 1: `trRepl` on solve's `{[a,b]}`). The proportions readout says `line 0.017 (+9.6ᴇ−2 SE)` (fact 2). Help: Esc steps to the next help page instead of leaving help. A quick mouse click on a soft key is missed (a 0.3-s press works; round 1's note).

## StatDist v2.7b — PASS

χ²(df 2.5): P(X ≤ 5) = **0.876911**, P(X > 5) = 0.123089, f(5) = 0.0569. F(2.5, 7.5): P(X ≤ 2) = **0.800427**, f = 0.1402, mean 1.3636, SD 1.8440. All = SciPy (round 1 stopped with "Invalid input"). The INPUT label now reads "df:". The formula page (CAS) for F(2.5, 7.5): E[X] = **15/11**, E[X²] = **405/77**, Var = **2880/847**, each "the program's value: agree", "exact (CAS)".

## ChiTable beta 3b

**Running it gave "Error: Syntax Error".** The Program Catalog's Check stopped in `csResMenu`, where beta 3b put two `//` comment lines inside the `CHOOSE(rmI, "Results menu", { … })` list (fact 3). A test copy with those two lines removed (`_emulator_round2_tmp\ChiTable_nocomment.txt`) compiled and ran: the tea table {3, 1; 1, 3} gives page 6 "Fisher's exact test, two-sided: p = **17/35** = 0.4857, exact (CAS)" and page 7 "χ² = 8 × (3 × 3 − 1 × 1)² / (4 × 4 × 4 × 4) = 8 × 8² / 256 = 2 = 2.000 … 34 of the 70 equally likely ways, p = 34/70 = 17/35 = 0.4857", exact (CAS). *Observation for Roger:* the risk difference's Wald CI there is (−0.1001, 1.1001), outside [−1, 1].

## CICatcher beta 2a — PASS

Exact (Clopper–Pearson), p 0.10, n 20, +50: 49 of 50 caught. Tapping a line with 0 yeses: "upper = **1−(1/40)^(1/20)** = 0.1684", "exact (CAS)". *Cosmetic:* the setup item "Proportion: Exact (Clopper-Pear[son])" is cut. A quick click on the emulator's Esc key was missed; a 0.3-s press quit.

## DNAMixLR beta 3a — PASS

Worked example, locus 1, formula view: "LR = (3×th+1)×(4×th+1)/(2×(th×p15−p15−th)×(p14×th−p14−th))", θ = 0: "LR = 1/(2×p15×p14)", "your p, th = 0.010: LR = 56.793", "exact (CAS)" (the formula at p14 = 0.15, p15 = 0.05, θ = 0.01 gives 56.79). *Cosmetic:* "Results table (tap a row to dro[p])" is still cut.

## EpiStats v1.7a — PASS

Help & Information → F "Where the SE comes from": "CAS: g′(p) = 1/p+1/(1−p) = 1/(p(1−p)) (CAS: the difference is 0)", "Var = 1/12+1/5+1/8+1/30 = **53/120**", "SE = sqrt(53/120) = 0.6646", "exact (CAS)".

## ScatterLab beta 2a

Data → Poverty vs crime (SYNTHETIC): n 16, r 0.751, ŷ = 16.64 + 1.020x, SSE 422.7. **Tapping the equation (the calculus page): "Error: Invalid input", the program stopped** — the same replace-loop cause as TrendTest.

## PowerViz v2.5a — PASS

One-sample mean: power 0.572, n₈₀ = 56 (55.6). Tapping n₈₀ → "Where n comes from": "CAS, solved for n: n = ((σ×zα+σ×zβ)/(μ₁−μ₀))^2", "CAS, with σ = 15, |μ₁−μ₀| = 5: n = (3×zα+3×zβ)^2", "n = 55.64 … Round UP: n = 56; trying n: n₈₀ = 56", "exact (CAS)" (CAS 5 ms).

## CentralLimit beta 3a, as an app — PASS (first run)

**Round 1 was wrong about the install.** The program pasted into the Kit's app editor in round 1 *had* reached the calculator (the Program Catalog's "CentralLimit (App)" held beta 2, and Check said "No errors"). This time beta 3a was pasted into the same place (Application Library → double-click CentralLimit → Program tab → paste → save), and the calculator's **View** key showed the app's own Views menu (CLT dashboard, Choose population, Draw samples, Plot population, Plot sample means, Square-root law, Exact curve (uniform), Why the bell? (MGF), …). Starting the app from the Application Library shows the stock Numeric view; the View key is the way in.
- Dashboard: Uniform, N 500 (μ 5.01, σ 2.98); n+ to 16; a tap on the top panel → 200 sample means, the exact curve and N(μ, σ/√n), "σ/SD = 4.11, √n = 4".
- Exact curve (uniform), n = 16: the peak of S's density **2330931341/6810804000** = 0.342240261 against the normal 0.345494149, "exact (CAS)".
- Why the bell? (MGF): "CAS: ln M(t) = −1/12×t^4/n+1/2×t^2 + …", the curves for n = 1, 4, 16 and e^(t²/2), "exact (CAS)".
- *Cosmetic:* the population item "Geometric (whole numbers, skewe[d])" is cut.

---

## What was fixed (the round-2 fix versions)

Built on harness **ppl_run_v3d** and gated with **ppl_gate_v1b** (ppl_check_v4, E12 hard); each has its `_CHANGES.md` and device checklist:
- **ChiTable beta 3c**: the comment lines moved out of the list; the CAS fallback.
- **TrendTest beta 3c, ScatterLab beta 2b**: the replace loops and `xxCas`; small fixed decimals; TrendTest's help Esc.
- **BayesTree beta 8c, StudRange beta 15b**: a click counts as stale only if `WAIT(-1)` returned it at once (already queued, < 100 ms); BayesTree's views close on a footer tap; BayesTree's text items; StudRange's summary counts the plot.
- **GaltonBoard 3c, CICatcher 2b, DNAMixLR 3b, EpiStats 1.7b, ErrorRate 1b, PowerViz 2.5b, StatDist 2.7c, CentralLimit 3b, CASProbe 1c**: the `xxCas` fallback and every INSTRING on a possibly empty string; small fixed decimals; the cut menu lines; CASProbe adds checks of facts 1 and 2. Then **CASProbe beta 1d**: T43b passes when the text contains CHAR(7431), whatever the minus, and logs which minus the exponent used; harness **ppl_run_v3e** prints the exponent's minus as U+2212 (with `home_minus=True`) and reproduces 1c's 44 / 9 exactly; 1d gives 45 / 8 / 19 / 0 there (verify 199 checks; gate PASS). Delivered; not yet run on the emulator.

---

## Retest of the fix versions (17 Oct 2026, 14:30–15:30)

Each fix version was pasted over its predecessor through the Connectivity Kit (CentralLimit through the app editor) from `_emulator_round2_tmp\r2fix`, byte-identical to what is now in `FIXED_FOR_DEVICE`, and run from Home. The CAS never failed, so the decimal fallbacks were again not reached on the emulator (the harness runs them).

| Program | Version | Result |
|---|---|---|
| BayesTree | beta 8c | **PASS**: the first tap after a footer close now counts; the two-test breadcrumb (laid out with TEXTOUT_P's return value) sits end to end |
| TrendTest | beta 3c | **PASS**: Snoring, page 4 — the crash of round 2 — shows `b = 95339/4757909`, "exact (CAS)"; the proportions readout `line 0.017 (+0.1 SE)`; Esc in Help returns to the menu |
| ScatterLab | beta 2b | **PASS**: Poverty vs crime, tap the equation — the crash of round 2 — `b = 2441/2394 (program 1.019632)`, `a = 3186173/191520 (program 16.63624)`, "exact (CAS)" |
| StudRange | beta 15b | **PASS**: Help for this plot closed by a tap at the α− spot, then one tap on α−: α 0.050 → 0.025, q crit 4.324 (round 2 skipped that tap). Quit: `StudRange: q crit (k = 3, ν = 12, α = 0.025) = 4.324, p = 0.0700, HSD not computed (engine: Python)` |
| StatDist | v2.7c | **PASS**: Pareto(1, 1), whose CDF `(stqx-1)/stqx` stopped v2.7b in the harness: the Formula page reads `F(x) = (x−1)/x`, "at x = 2: 0.500000, the program's: agree", mean and variance "= infinity (CAS)", "exact (CAS)" |
| PowerViz | v2.5b | **PASS**: "Where n comes from", exact (CAS), n = 56; the exit box |
| ChiTable | beta 3c | **PASS: compiles and runs** (beta 3b did not). Tea table {3, 1; 1, 3}: page 6 `p = 17/35 = 0.4857`, page 7 `= 2 = 2.000`, "34 of the 70 equally likely ways", both "exact (CAS)"; the Results menu shows all four items |
| GaltonBoard | beta 3c | **PASS**: every main-menu line in full ("Overlay: none/binom/+normal", "Colour bars by SDs from Rp", "Pascal: off/counts/C(r,k)", "Bins to D1, D2 (Stats 1Var)", "Where Poisson comes from (CAS)"); one ball, then Esc: `Galton Board: 1 ball, R = 8, p = 0.50; …` |
| CICatcher | beta 2b | **PASS**: the setup menu in full ("Proportion: Exact (C-P)"); header "Exact, p = 0.10, n = 20"; +50, a 0-yes line: `upper = 1−(1/40)^(1/20) = 0.1684`, "exact (CAS)", `p̂ = 0/20 = 0.00: 0.00 to 0.17, caught` |
| DNAMixLR | beta 3b | **PASS**: "Results (tap a row to drop)" in full; the worked example's formula view for loci 1, 2 and 3, each "exact (CAS)", nothing stops. *For Roger:* the first menu line, "Hypotheses:  V + S, no unknown", is cut at the box edge, so Hd does not show (as its CHANGES predicted) |
| EpiStats | v1.7b | **PASS**: menu "EpiStats v1.7b". Module 1 (1, 2999, 50, 50): `OR = ad/bc = < 0.001 (0.00-0.00)`, `Risk if exposed, a/(a+b) = 0.0%`; the OR box ends `= 0.00 to 0.00`. Module 2 (1, 2999, 1, 999): `the outcome is rare here (Ru = 0.1 %)`, `NNT = 1/0.000667 = 1500.00, round up: 1500`. No ᴇ anywhere. *For Roger:* the OR box also reads `ln OR = ln(0.000) = −8.006` (the extreme-table item in its CHANGES) |
| ErrorRate | beta 1b | **PASS**: Why 3, exact (CAS); true rate 0.0002 → "0.0200 %"; trawl at 1 in 1 billion, N = 1: `expected chance matches N × RMP = 0.000`, and the Exact page `μ = 0.000.` *Cosmetic:* "N = 1 profiles searched"; `P(at least one chance match) = < 0.0001 %` and `P = < 0.0001 % exactly` (the "= <" form StudRange 15b dropped) |
| CentralLimit | beta 3b (app) | **PASS**: installed through the Kit's app editor; starts; "Geometric (counts, skewed)" in full; n = 16, Exact curve: `2330931341/6810804000 = 0.342240261`, "exact (CAS)" |
| CASProbe | beta 1c | **44 pass, 9 fail, 19 values, 0 errors** (the checklist expected 45 / 8). T43a PASS (`INSTRING("", "a")` is an error), T43c PASS (`STRING(ROUND(0.096, 1), 2, 1)` = `0.1`). **T43b FAILed, but the test was wrong**: the Prime printed `9.6ᴇ−2`, codes 57 46 54 7431 **8722** 50 — scientific, as fact 2 says, with the Unicode minus; T43b compared the text with an ASCII hyphen, and the summary said "NOT scientific". Fixed in beta 1d |

**New fact from the retest:** the Prime prints the exponent's minus as U+2212, as it prints a negative number's leading minus (CASProbe T01). A program that wants to know whether a STRING came out scientific must look for CHAR(7431), not compare text.

**Items for Roger** (all cosmetic or wording; nothing stops a program):
1. DNAMixLR's "Hypotheses" menu line is cut, hiding Hd (a wording choice, in its CHANGES).
2. ErrorRate's trawl: "1 profiles" and "= < 0.0001 %".
3. EpiStats' extreme tables: `ln(0.000)` in the worked OR box.
4. EpiStats page 3 prints a p-value of 0 as `0.00000 *`, where other programs say "< 0.00001".

## Still for the calculators (G1 and G2) — the emulator can't settle these

1. **G1 speed:** CASProbe on the G1 (the slowest CAS call; the emulator's was 10 ms); BayesTree's 1.5-s auto-off for CAS updates; ChiTable's drag on a G1; CentralLimit's sample drawing.
2. **A light finger tap on a soft key** in the polling programs (TrendTest, ChiTable, PowerViz, CICatcher, ScatterLab, StatDist's gallery): a quick mouse click is missed, a 0.3-s press works.
3. **Whether a MOUSE-read tap leaves a click for `WAIT(-1)` on the hardware** (BayesTree 8c and StudRange 15b now skip a click only if it was already queued; the hardware case is in their checklists).
4. **GfxProbe T15 and T16**: a held key across `WAIT(0.02)`; a second finger.
5. **Arrow keys on the skin** move two steps on the emulator; the hardware keys are the real test.
6. **G1 memory** with the whole fleet loaded.
7. **CASProbe beta 1d's T43** on the G1 and G2: an empty INSTRING, and the codes of `STRING(0.096, 2, 1)`. A different answer there is a finding: the fleet's guards would then be insurance, not a fix.
8. **AND/OR short-circuiting inside a program** (measured in Home only); nothing in the fleet depends on it.
