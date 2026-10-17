# DNAMixLR beta 1a → beta 2: what changed

*16 October 2026. Built ON TOP OF `DNAMixLR_beta1a.txt` (1081 lines); every beta 1a fix is kept,
including the exclusion handling. Output: `DNAMixLR_beta2.txt` (2432 lines, 100.7 KB, UTF-8, LF).
**Not yet run on hardware** (neither were beta 1 and beta 1a). "1a" = beta 1a line numbers, "b2" = beta 2 line numbers.
`dmProb`, `dmKnowns`, `dmTyped` and `dmEval` are byte-for-byte beta 1a (b2 523-627; checked by script).*

## (a) Every change

1. **Showcase: drag θ on the theta plot** (1a 868-948 → b2 `dmThX` 1344, `dmThStatic` 1356, `dmThFrame` 1442, `dmPlotTheta` 1474).
   - A finger anywhere in the plot box (`dmP2L..dmP2R` × `dmP2T..dmP2B`, ±8 px sideways, down to the tick labels) sets
     θ = 0.05·(x − dmP2L)/(dmP2R − dmP2L), snapped to 0.0025 and clamped to 0…0.05. While the finger stays down, every
     MOUSE sample that changes the snapped θ redraws: the solid green line, a green dot on the curve, the readout
     "theta 0.0125 · log10 LR 3.571 · LR 3,726" (y 20) and a red marker on the ENFSI ladder.
   - Everything comes from the **cached** 21 points (`dmPtV`) through `dmInterp` (b2 755) — `dmCombAt` is never called in
     a drag. Every θ the drag can set is a grid point, so the readout is the cached value itself; interpolation only
     matters for a typed θ off the grid.
   - The static plot is composed once into **G2** (`dmThStatic`); each frame is `BLIT_P(G1,0,0,G2)`, the moving parts,
     `BLIT_P(G0,0,0,G1)`, `DRAWMENU`.
   - Keys: Left/Right step θ by 0.0025; **Enter adopts** it (dmTh := θ, `dmRecalc`; the curve cache is kept because the
     curves do not depend on the session θ; the dotted session line moves). Esc = menu.
   - The ladder (`dmLadDraw` b2 950, `dmLadY` 939, `dmMark` 984): 13 bands from dmVerbal's edges (log10 ±0.301, ±1, ±2,
     ±3, ±4, ±6), drawn from +7 to −7 so the "extremely strong" bands show; Hp bands light blue with blue names, Hd light
     red with red names, "about equal" light orange; grey band borders. With an exclusion the curve is the other loci,
     the readout says "other loci: LR …" in red and no marker is drawn.
2. **Locus tap on plot 1** (1a 743-863 → b2 `dmDrawLoci` 1044, `dmStrip` 1002, `dmHitLocus` 1031, `dmPlotLoci` 1282).
   A tap in a column (same box constants `dmP1L..dmP1B` and the same column width as the drawing) selects the locus:
   the bar turns solid and a 3-row strip replaces legend/footer (y 184-206): alleles, P(E|Hp), P(E|Hd) (the stored
   `dmPp`/`dmPd`), LR, log10 LR, verbal, "Ent = more" (or "dropped"). Tap it again or Enter → the locus page. Left/Right
   select from the keys; a tap off the bars hides the strip. Capped `dmDrain` after every tap.
3. **Soft keys** `{"Locus","Theta","Table","Ladder","Help","Menu"}` on every page (`dmMenu` b2 443, after the blit,
   every frame; `dmSoft` b2 453 maps slot 1-5 → pages 1-5, slot 6 → menu). Pages are dispatched by `dmViews` (b2 2300):
   each page returns the next page. All footers now sit at y ≤ 207; the strip y ≥ 218 is left to DRAWMENU.
   Plot 1's box shrank (y 30-200 → 30-166) and plot 2's (44-306 × 30-196 → 40-228 × 34-166) to make room.
4. **Waterfall** (toggle on plot 1: `+` or a tap on the title). Floating bars from cum(i−1) to cum(i) in log10 LR, blue
   (light-blue fill) when LR > 1, red (light-red) when LR < 1, thin grey links, signed labels (+1.75 …), and an "all"
   column from 0 to the total in a magenta frame. Running totals from `dmCum` (b2 686; status per locus: counted /
   dropped / no LR / EXCLUDED / after the exclusion). An excluded locus is a red column with "EXCLUDED" written to the
   right over the (empty) later columns; the total stops there and the "all" column says "excl.".
   **Also in bars view, the magenta running-total line now stops at an exclusion** (beta 1a ran it on over the other
   loci; the bottom line already said EXCLUDED).
5. **Allele-set picture on the locus page** (1a `dmLocusPanel` 511-554 → b2 `dmPicture` 1713, `dmUSet` 1679,
   `dmCarries` 1695, `dmDrawPanel` 1771, `dmLocusPanel` 1882). One box per allele of M with its p (".150"): filled green
   (victim), magenta (suspect), orange (third), split when two knowns carry it — **only for persons who are contributors
   under the hypothesis shown**; outlined double red when no contributing known carries it (`dmUSet` builds U exactly as
   dmProb does). A typed non-contributor leaves a small dot of their colour (they still condition θ). A known
   contributor with an allele outside M adds a red "out" box. The line under the boxes says what the unknowns must do:
   "1 unknown must supply 14, 15: P = 0.018" / "the knowns explain M exactly: P(E|Hp) = 1" / "… cannot supply … P = 0".
   Tap the picture band or press `+` to switch Hp ↔ Hd; Left/Right move between loci; Enter/Esc = menu.
6. **Drop a locus from the Results table** (1a 695-737 → b2 `dmDrawTable` 1577, `dmToggle` 1619, `dmResults` 1626).
   New `dmInc` (one 0/1 flag per locus). `dmRecalc` (b2 630) multiplies and looks for an exclusion only over included
   loci and counts `dmNDrop`; `dmCombAt` (b2 664) skips dropped loci. **Neither changes any locus's LR, P(E|Hp) or
   P(E|Hd)** (checked). Tap a row (hit test uses `dmTbY`/`dmTbH`, set while drawing) or Up/Down + Enter: the row greys
   and says "dropped"; the combined line reads "Combined (2 of 3 loci): LR 208.6, log10 2.319". Dropping the excluded
   locus removes the exclusion ("as if not typed"). The row pitch drops from 11 to 10 px at 12 loci. Flags are set in
   `dmEnterLocus`, `dmExample`, cleared in `dmClearLoci`. Menu title, plot 1, the fallacy page and the RETURN line show
   "(k dropped)". DM_LR follows the what-if product (header HOME EXPORTS says so).
7. **θ plot: usual-range band and the halved-frequency curve.** Light-green `RECT_P` band from θ 0.01 to 0.03 (replaces
   beta 1a's dotted red lines). `dmCurves` (b2 721) computes both curves once (42 `dmCombAt` passes), the second on a
   temporary copy of `dmLoc` with every frequency halved (built with FOR loops), then restores `dmLoc`; cached in
   `dmPtV`/`dmPtH` with `dmCvOK` (cleared by `dmRecalc`, kept across a θ-only change). The y range covers both. Legend:
   "0 to 0.03: LR × 0.466 (your p), × 0.142 (halved)" — θ bites harder when p is small. (This line replaces beta 1a's
   "LR: 0 … 0.01 … 0.03 …" line; the readout now gives the LR at any θ.) The theta plot's `MAKELIST(…K…)` is gone.
8. **Prosecutor's fallacy page** (new menu item 8; `dmDrawFall` b2 2045, `dmFallacy` 2119). Tap a rung (or Up/Down):
   the suspect and N = 1, 10 … 10,000,000 **other** people equally able to have left the stain, i.e. prior odds 1 : N.
   Three stacked bars on one log10-odds axis with the even-odds line: prior odds (grey), × LR (dodger blue, starting
   where the prior ends), = posterior odds (magenta); then P(Hp | E) in large magenta with a 0-1 strip; then
   "LR 5,333 × prior 1:100,000 → posterior 0.0506", "Fallacy: P(Hd|E) = 1/LR = 1.88E-4; truly 0.9494", and in red
   "The LR is NOT the probability that the / suspect contributed." With an exclusion: "posterior is 0 whatever the
   prior". The sentence is also on the locus page (under the verbal) and under the Results table's verbal (`dmCombLines`
   b2 1546). Default rung 6 (1:100,000).
9. **NRC II formula on the locus page**: for the next allele drawn (the first allele the unknowns must supply under Hd,
   else under Hp, else allele 1), with n = every typed allele (as dmProb counts them) and nₐ of them that allele:
   "Next allele 14: n = 4 seen, 1 of them 14 (NRC II):", "(1×0.010 + 0.990×0.150) / (1 + 3×0.010) = 0.1539",
   "plain p = 0.150 becomes 0.154 with theta". At θ = 0 it says the plain p stands. (The brief's "0.150 becomes 0.157"
   is n = 2; with victim and suspect both typed, n = 4 is what the engine uses, so the page shows 0.154.)
10. **Preset 3 note** on the locus page (detected from dmPres/dmHp/dmHd, so a custom single-source set gets it too):
    at θ = 0 "single source: LR = 1/(2pq) or 1/p^2 = 1/RMP"; at θ > 0 "single source: LR = 1/RMP, theta-corrected"
    (because 1/(2pq) is then not the LR shown; checked equal to NRC II's θ-corrected match probability).
11. **Animated ladder** (new menu item 7 and soft key; `dmLadFrame` b2 1921, `dmLadView` 1995, `dmPause` 428). Full-size
    ladder with integer ticks −6…6, full band names, a list of loci (log10, total) at the right; the marker steps from
    LR 1 up locus by locus with magenta ticks at each total passed, pausing 400 ms per step by a **TICKS loop** that
    also polls GETKEY and MOUSE — any key or tap skips to the end. An exclusion stops the climb in red. Tap/Enter
    replays, Esc = menu.
12. **Help** (1a 971-1010 → b2 `dmHelpPage` 2179, `dmHelp` 2236): composed in G1, three pages (page 3 new: soft keys and
    every gesture with its key equivalent, the colours, the prosecutor's-fallacy pointer); tap/Enter/Right = next,
    Left = back, Esc = menu. **Footers** in the house form, dodger blue. **RETURN** kept, same wording as beta 1a, with
    "(k dropped)" when relevant and θ via `dmThS`.
13. **Housekeeping.** Locus page, Results and Help now compose in G1 (review sweep 4). `dmWaitKey` (ignored touch)
    removed; every page polls GETKEY and MOUSE (`dmPoll` b2 409) with the capped `dmDrain` (b2 397). `dmThS` (b2 347)
    shows θ with 4 decimals when needed (an adopted 0.0125 is not shown as 0.013). New helpers `dmCom` (thousands
    separators), `dmLRS`, `dmPStr` (probability with its complement computed separately: "1 - 1.87E-4"). Menu has 12
    items, unnumbered (Prime shows 1-9, A Clear, B Help, C Quit; Quit = `mnI == 12`). `dmEnterLocus` moved after
    `dmViews` so no new forward declaration is needed. Palette constants `dmLBLU`, `dmSHAD`, `dmLRED`, `dmLGRN` added;
    geometry constants in `dmInit`. Header: "What changed in beta 2", the LR-is-not-a-probability paragraph, a file map.
14. **"More" soft-key convention (Roger, 16 Oct): considered, not applied.** This program's six labels fit exactly
    (Locus, Theta, Table, Ladder, Help, Menu) and every feature has a key route (θ: Left/Right + Enter; waterfall and
    Hp/Hd: `+`; drop: Up/Down + Enter; prior: Up/Down; Prosecutor's fallacy: Menu soft key → item 8). So slot 6 stays
    "Menu" as the brief specified; the help pages therefore describe no More key. If Roger wants the fallacy page or
    "Adopt θ" on a soft key, a second page `{"Fallacy","Wfall","Adopt","Hp/Hd","Menu","More"}` is the natural form.

## Gate (bash check.sh, final file)

```
=================== DNAMixLR_beta2.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
(empty)
--- 2. ppl_check_v2 tally (ORIG) ---
(empty)
--- 2b. ppl_check_v2 HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
(no new problems: 1690 checks, 7 problems = beta 1a's five entry-point/EXPORT noise lines + two
 "RECT_P/TEXTOUT_P targets 'lgG', not a GROB" -- the known grob-parameter noise, dmLadDraw 965/977)
--- 4. full parse (kit interpreter) ---
DNAMixLR_beta2.txt     PARSE FAIL <ppl>:202: expected KW, found OP ';'   (the forward declaration)
   ORIG: DNAMixLR_beta1a.txt  PARSE FAIL <ppl>:117: same construct
--- 5. ---
2432 lines, 100682 bytes; no non-ASCII in code
```
- With the forward declaration, EXPORT list and file-level LOCALs commented out: **PARSE OK (60 functions)**.
- `fleet_names_v2.py` over every program in out/: no DNAMixLR name collides with any other program, 0 untagged,
  0 built-in matches (the collisions it lists are other programs' old/new version pairs). One E11 found on the way
  (`dfC` = DFC) was renamed `dfBc`.

## Verification (`verify_DNAMixLR.py`, 35 checks, 0 failures)

Part A re-implements `dmProb` in Python and checks it against brute-force enumeration of every allele sequence under
the θ urn (300 random cases, max |diff| 6.1E-16). Part B runs the real source in `ppl_run_v1`:
```
PASS example theta 0: 66.67, 20, 4, combined 5333.3
PASS example theta 0.01: 56.79, 19.08, 3.674, combined 3981.5
     waterfall running totals (theta 0.01): 1.7543, 3.0349, 3.6001     (program dmCuV identical)
     drop locus 2: product 208.6482 (log10 2.3194)                     (program dmComb identical, dmLR unchanged)
     theta 0 -> 0.03: LR x 0.4656 (your p), x 0.1415 (p halved)        (program legend 0.466 / 0.142)
     fallacy: LR 5333.3 x 1:100000 -> odds 0.05333 = 1:18.750 -> P = 0.05063
     NRC II next allele 14: 0.153883                                   (page: "= 0.1539", "0.150 becomes 0.154")
PASS preset 3 LR = 1/RMP (NRC II theta-corrected), het and hom, theta 0/0.01/0.03
PASS theta curve and halved curve, 21 points each = Python; frequencies restored after the halved pass
PASS drag (Drag through 11 x positions): one frame per new theta, readout = cached curve
PASS Enter adopts the dragged theta 0.0125; combined 3726.03 = Python; readout "LR 3,726"
PASS locus tap: strip 'Locus 2: 8, 9, 11', 'P(E|Hp) = 1.000', 'P(E|Hd) = 0.052', 'LR = 19.083, log10 = 1.281',
     'moderate support for Hp'; second tap -> locus page
PASS waterfall page: +1.75, +1.28, +0.57, total 3.60; exclusion at locus 2: EXCLUDED, totals stop (status 1,3,4,4)
PASS dropping the excluded locus: no exclusion, product of the other three
PASS fallacy page: 'LR 5,333 × prior 1:100,000 → posterior 0.0506', 'P(Hp | E) = 0.0506', '= posterior odds 1 : 18.750';
     at 1:1 'P(Hp | E) = 1 - 1.87E-4'
PASS ladder: frames 'before any locus', 'after locus 1', 'after locus 2', final 'after locus 3'; a key skips
PASS RETURN 'DNAMixLR: combined LR = 3981.5, log10 = 3.600, 3 loci, theta = 0.010' (as beta 1a)
```
Also run: stale-key mode (each dialog's OK left in the buffer) through menu → worked example → Enter a locus (an
exclusion) → locus page: no skipped page, RETURN "DNAMixLR: EXCLUDED at locus 4 (LR = 0), 4 loci, theta = 0.010".
A 12-locus layout sweep of every page found no text past x 316 at 6 px/char except two lines, both fixed.

## (b) DEVICE TEST CHECKLIST (least → most risky)

1. **Paste and compile.** 60 routines, new file-level LOCAL lines at b2 233-269. If the paste stops, note the cursor line.
2. **Menu.** 12 items: 1-9, A Clear all loci, B Help, C Quit. Quit with no loci: "DNAMixLR: no loci".
3. **Worked example → Results table (item 4).** 56.79 / 19.08 / 3.674; "Combined LR = 3981.5   log10 = 3.600"; green
   "strong support for Hp"; red "The LR is NOT the probability that the / suspect contributed."; first row framed red;
   soft keys under it read Locus Theta Table Ladder Help Menu. Nothing overlaps the soft keys.
4. **Soft keys.** From the table tap each: Locus → bar plot; Theta → theta plot; Ladder → animation; Help → help p1;
   Menu → the CHOOSE menu. Esc from every page → menu.
5. **Drop a locus.** On the table tap row 2: it greys, "dropped"; "Combined (2 of 3 loci): LR 208.6, log10 2.319";
   verbal "moderately strong support for Hp". Tap again: restored (3981.5). Up/Down + Enter do the same. Menu title
   shows "(1 dropped)" while one is dropped.
6. **Locus plot, tap a bar.** Tap bar 2: it turns solid blue; strip "Locus 2: 8, 9, 11", "P(E|Hp) = 1.000",
   "LR = 19.083, log10 = 1.281", "P(E|Hd) = 0.052", "moderate support for Hp", "Ent = more". Left/Right move it. Tap
   bar 2 again → the locus page. Tap off the bars → strip gone.
7. **Waterfall.** On the locus plot press `+` (or tap the title): three blue floating bars +1.75, +1.28, +0.57, grey
   links, magenta-framed "all" bar labelled 3.60. `+` again → bars.
8. **Locus page picture.** From locus 1: boxes 12 13 (green), 14 15 (magenta), all grey borders; "the knowns explain M
   exactly: P(E|Hp) = 1". Tap the boxes (or `+`): caption "Hd: V + 1 unknown"; 14 and 15 lose their fill, gain a double
   red outline and a small magenta dot; "1 unknown must supply 14, 15: P = 0.018". Formula lines:
   "(1×0.010 + 0.990×0.150) / (1 + 3×0.010) = 0.1539", "plain p = 0.150 becomes 0.154 with theta". Check the × glyph.
9. **Prosecutor's fallacy (item 8).** Set θ = 0 (item 3) first. Rung 100,000 highlighted; "prior odds 1 : 100,000",
   "× LR 5,333", "= posterior odds 1 : 18.750", "P(Hp | E) = 0.0506", the → glyph in "LR 5,333 × prior 1:100,000 →
   posterior 0.0506". Tap rung "1": P(Hp | E) = 1 - 1.87E-4 (BCD may print 1.88E-4). Up/Down move the rung.
10. **Ladder (item 7).** Marker climbs 0 → 1.75 → 3.03 → 3.60 at about 0.4 s a step (time it: TICKS pace on G1 vs G2),
    magenta ticks left behind, ends in "strong" with "after locus 3: LR = 3981.5 (log10 3.600)". A key mid-climb skips
    to the end. Band names readable, the two "weak" labels not touching "moderate" (11 px band pitch — **watch here**).
11. **Theta plot, static (item 6).** Light-green band 0.01-0.03; blue curve with 21 dots under a magenta (halved) curve;
    dotted green session line at 0.010; ladder at the right with short names; legend "0 to 0.03: LR × 0.466 (your p),
    × 0.142 (halved)"; readout "theta 0.0100 · log10 LR 3.600 · LR 3,982" and a red marker in "strong". 42 passes run on
    entry — note how long the first draw takes on the G1.
12. **Theta drag (the showcase; G2 copy per frame).** Put a finger on the plot and slide left to right: the green line
    follows in 0.0025 steps, readout from "theta 0.0000 … LR 5,333" to "theta 0.0500 … LR 1,716", marker slides down
    inside "strong". Does it keep up on the G1? Is `BLIT_P(G1,0,0,G2)` clean (no stale line left behind)? Lift at
    0.0125 and press Enter: the dotted line moves there, the menu shows "Coancestry theta = 0.0125", Results shows
    3726.0. Left/Right without touching do the same.
13. **Exclusion.** Load the example, Enter a locus: 2 alleles 16/17, p 0.2/0.3, Victim 1/2, Suspect 1/0. Locus page:
    red exclusion lines and a red "out" box under Hp. Waterfall: red column at 4 with "EXCLUDED", "all" says "excl.".
    Theta plot: readout "other loci: LR …" in red, no ladder marker. Ladder: stops in red at locus 4. Fallacy page:
    "posterior is 0 whatever the prior". Drop locus 4 on the table: the exclusion disappears, 3981.5 is back.
14. **Twelve loci** (as in the beta 1a checklist item 7): table rows at 10 px pitch all above the rule, combined lines
    above the soft keys; plot 1 labels on two rows; waterfall 13 columns 20 px wide.
15. **Preset 3.** Hypotheses → "Suspect alone vs 1 unknown"; one locus 2 alleles p 0.2/0.3, suspect 1/2. θ 0.010:
    locus page "single source: LR = 1/RMP, theta-corrected" and LR 8.067; θ = 0: "single source: LR = 1/(2pq) or 1/p^2
    = 1/RMP" and LR 8.333.

## (c) Not confirmed, left as it was

- **Font-1 widths and heights** are estimates (5.5-6 px per character, ~10 px per line); the tightest spots are the
  short ladder labels (11.4 px band pitch on the theta plot), the locus page's formula line (clipped at 304 px) and the
  waterfall's "EXCLUDED" word running over later columns.
- **`BLIT_P(G1,0,0,G2)`** (G2 as a scene buffer) is used by GaltonBoard beta 1b and SampDist v2.3, neither yet run on
  hardware; `DRAWMENU` is device-verified, but repainting it on every drag sample has not been timed.
- **The drag loop** (`REPEAT … MOUSE … UNTIL SIZE(MOUSE(1)) == 0`) is the TouchKit/brief shape, not yet run on a device.
- **`TEXTOUT_P` and `RECT_P` into a grob passed as a parameter** (`dmLadDraw(G2 …)` / `(G1 …)`): the fleet does this with
  PIXON_P (ChiTable `csDotV`, device-run); with TEXTOUT_P it is unrun.
- **`CHAR(8594)` (→)** renders per Lessons Learned §13 (the arrow pair); `CHAR(215)` is verified.
- **MAKELIST in dmProb keeps Home's K** (dmProb must not change; GfxProbe T19 still pending).
- **The NRC II citations** in the header and help ("recommendation 4.2", "NRC II (1996) 4.2") are beta 1's, not
  re-checked here; the new text cites no equation numbers.
- **A locus with LR = −1** (Hd impossible) is still skipped silently in the product, as in beta 1/1a; the waterfall
  and ladder now label it "no LR".
- **DM_LR with dropped loci** follows the what-if product; if Roger prefers DM_LR to stay the full product, it is one
  line in `dmRecalc`.
