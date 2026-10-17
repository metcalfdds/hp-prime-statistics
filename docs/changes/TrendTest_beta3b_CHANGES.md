# TrendTest beta 3b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3a; every beta 3a feature is kept, and the CAS call form and trCompute are untouched. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

From the 17 October 2026 run (`Emulator_Round1_Results_2026-10-17_v1.md`):

- **TrendTest beta 2** ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) and passed: trend χ² 72.659, Pearson 72.782, departure 0.123 (all match Python). One cosmetic finding: "the Examples list cuts '(made up)' to '(made up'". CHOOSE does not wrap a line wider than its box; it cuts it (F5).
- **GfxProbe beta 1, T09: "no".** ARC_P at r = 3, 2 and 1 plus the centre pixel, drawn as a solid dot, shows a white X: concentric circles leave holes on the diagonals (F2). TrendTest's `trDot`, the dots on the proportions and odds-ratio plots, is drawn exactly that way. The emulator run did not mention the dots, but GfxProbe drew the same three circles and the pixel and saw the holes. This was found by the fleet scan (item 8 of the task) and fixed here because TrendTest was getting a new version anyway.

## What changed (line numbers: beta 3a → beta 3b)

1. **Examples** (trExamples, 3a 815–818 → 3b 838–841).
   - "Sleep hours: a U shape (made up)" (32 characters) is now "Sleep: a U shape (made up)" (26).
   - "Convictions, re-arrest (made up)" (32) is now "Prior convictions (made up)" (27).
   - The data's own labels, shown with the results, are unchanged: "ILLUSTRATIVE (made-up counts): sleep, illness" and "ILLUSTRATIVE (made up): convictions, re-arrest".
2. **Solid dots: `trDot`** (3a 379–386 → 3b 398–408). Three overlapping RECT_P bars, 7 × 3, 3 × 7 and 5 × 5, cover exactly the pixels of a disc of radius 3: the same 7 px dot in the same colour, three calls instead of four.
   - The black ring round the selected level (ARC_P r 6 and 7) and the hollow "ref" circle at OR = 1 (ARC_P r 3) are outlines on purpose and stay as they are. See "Not changed".
3. **Header.** A "beta 3b" paragraph and the status line.

Nothing else changed. The routines that differ from beta 3a are exactly `trDot` and `trExamples`; outside them only comments differ.

## Verification

`verify_TrendTest_beta3b.py` (built from the 3a script; harness **ppl_run_v3c**). Output in `verify_TrendTest_beta3b_output.txt`: **0 failures** (44 PASS lines).

- **Kept:** the least-squares calculus page (Giac solve against Python fractions, statsmodels WLS), the trend, Pearson and departure statistics, `cas='giac'` and `cas='fail'`, the stale-key run, and beta 3 in v3c still showing the CAS finding.
- **W (new):**
  - every CHOOSE line shown in the runs is at most 30 characters (51 seen) and so is every line in the source;
  - the shortened lines are the ones shown;
  - the three examples load the same data and labels as before (k 4/5/4; cases {24, 35, 21, 30}, {38, 40, 36, 44, 44}, {72, 66, 51, 88});
  - `trDot` is exactly three RECT_P covering the 37 pixels of a radius-3 disc;
  - in a run through the odds-ratio plot, the only ARC_P left is the hollow reference circle (r 3).
- **G:** the routine diff is as listed.

## Gate

`python3 ppl_gate_v1a.py TrendTest_beta3b.txt TrendTest_beta3a.txt` gives **RESULT: PASS**.
- ppl_check_v3: clean.
- lint_ppl: the same problems as 3a. Two more lines read "RECT_P targets 'dtG', not a GROB", the known noise on a grob parameter; three RECT_P replace one PIXON_P.
- fleet_names_v2: 0 collisions, 0 untagged.

With the unpacked hp-prime-kit, the kit lint gives 0 errors.

## Device checklist (emulator first, then G2 and G1)

1. Menu → Examples: "Snoring and heart disease", "Sleep: a U shape (made up)" and "Prior convictions (made up)" all show in full, with the closing parenthesis.
2. Load Snoring. On the proportions plot each dot is a solid disc with no white X. Do the same on the OR plot (the OR soft key).
3. Select a level (tap a dot). Look at the black ring round it, two ARC_P circles of r 6 and 7: if it shows pinholes on the diagonals like T09's dots, note it for the next version.

## Not changed (listed, not edited)

- The selection ring (3b 1436–1437, ARC_P r 6 and r 7) is two concentric circles, the pattern T09 found leaves diagonal gaps. It is an outline, not a solid dot, so it was left alone. The device check (step 3) decides.
- One CHOOSE line is exactly 30 characters: "Plot: proportions + trend line" (main menu, 3b line 1902). The emulator did not report it cut.
