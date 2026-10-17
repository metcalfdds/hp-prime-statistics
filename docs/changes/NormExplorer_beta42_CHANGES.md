# NormExplorer beta 42 — changes from beta 41

*16 October 2026. The touch and graphics version, built on beta 41 (every beta 41 fix kept). Not yet run on hardware.*
*"Old" line numbers refer to `NormExplorer_beta41.txt` (2255 lines); "new" to `NormExplorer_beta42.txt` (3418 lines after the follow-up in section A2).*
*Section A's "new" line numbers were taken before the A2 follow-up: add 16 for lines 165-1002 of that count, 93 for 1003-2342 and 94 from the help pages on (e.g. ne_Explorer 1003 → 1019, ne_HelpPages 2350 → 2443, ne_NormDraw 2623 → 2717).*
*Companion guide: `normexplorer-guide_beta42.md` (no earlier guide was staged, so it was written from the program).*

## Gate result (`check.sh NormExplorer_beta42.txt NormExplorer_beta41.txt`)

```
--- 1. kit lint (errors) ---            kit lint: 0 errors
--- 2. ppl_check tally (NEW) ---        5 E5   6 W3
--- 2. ppl_check tally (ORIG) ---       5 E5  19 W3
--- 2b. hard errors E2 E3 E6 E8 E10 E11 --- none
--- 3. lint_ppl ---                     1364 checks, 75 problems (beta 41: 995 checks, 109 problems)
      same categories as beta 41, none new: block depth in the #PYTHON block (758), the five
      INPUT-return lines and the seven CHOOSE-capture lines that beta 41 also lists (pending
      idiom), one STRING(NORMALD(..),2,4) false positive at 1508 (beta 41's 911), and the
      G0-drawing "not a GROB" noise, which fell from 59 to 25 because the help pages now draw on G1
--- 4. full parse (kit interpreter) --- PARSE FAIL at 643: '√'  (beta 41: same failure at 492)
--- 5. E5 non-ASCII in code ---         the same five √ (643, 2037, 2076, 2163, 2264)
```

The E5 count did not grow (no new `√`; new code uses no Unicode outside strings); W3 fell from 19 to 6 because the help pages are now composed on G1, where the width check can read the x argument. One new hard error appeared during the build and was fixed before delivery: `LOCAL exAct` matched the built-in `EXACT` (E11) and was renamed `exCmd`.

**Full parse with the harness's pre-processing.** The kit interpreter cannot read `√`, forward declarations, a file-level `LOCAL` or `#RRGGBBh`. `verify_NormExplorer.py` pre-processes exactly those four things (√( → SQRT(, forward declarations dropped, file-level LOCAL read as globals, hex to decimal) and then loads the file: **beta 41 and beta 42 both parse** (34 functions, 83 globals in beta 42), and every path below was run.

**Fleet names** (`fleet_names_v2.py` over every `.txt` in `out/`): no collision, untagged helper, mixed tag or built-in match involves NormExplorer. The seven new routines are `ne_Drain`, `ne_WaitAny`, `ne_Sweep`, `ne_BarHit`, `ne_InShade`, `ne_RTxt` and `ne_Tag`; every new identifier was also checked against `HP_Prime_Builtin_Names.txt` and the kit's name list, ignoring case.

## Verification (`verify_NormExplorer.py`, 135 checks, 0 failures)

**Part A, the new formulas against SciPy:** left-tail z* = Φ⁻¹(α) and the area below x* = α (α = .10, .05, .01); two-tailed: area outside μ ± z(1−α/2)σ = α; the power by the program's route (x* first, then the area of curve 2 past it) against the textbook 1 − Φ(z₁₋α − d) at four settings, including N(0,1) vs μ₂ = 1, α = .05 → 0.2595; one bin's p and n·p; the trapezoid S-curve against the exact CDF: 1.7×10⁻⁵ on μ ± 4σ, 3.9×10⁻⁵ on μ ± 6σ (0.01 px), 1.0×10⁻² when σ is 1/200 of the window (1.5 px); the density digit rule (0.242, 0.0266, 1.990, 0.00266, 0.000400).

**Part B, the PPL itself in the kit interpreter**, with SciPy behind NORMALD*, scripted CHOOSE / INPUT answers written into the named variables, scripted keys and touches (each tied to the routine that must be running), and every G1 drawing call recorded frame by frame:

| Path | What was run | Result |
|---|---|---|
| Probability from x, all 4 | N(100,15), x = 110; a = 85, b = 115 | NE_P = 0.747507 / 0.252493 / 0.682689 / 0.317311 = SciPy to 1e−12; printed readouts 0.7475 / 0.2525 / 0.6827 / 0.3173; 9 sweep frames then the final view, running area rising every frame; riding tag = the area (outside: 0.1587 on each tail); footer, z-ruler row −3…3 at y = 205, nothing below y = 217 |
| Sweep skip | a key during the sweep | 1 sweep frame drawn, then the final view |
| x from probability, all 5 | N(100,15) | percentile 119.2233; right x* 124.6728; **left** z* = −1.6449, x* = 75.3272 (mode 1); **two-tailed** z* = ±1.9600, 70.6005 and 129.3995 (mode 4), each tail tagged 0.0250, P(outside) = 0.0500; central 70.6005…129.3995 |
| Z-solver, all 4 | (130,100,15), (−1.5,100,15), (130,2,15), (130,100,2) | z = 2, x = 77.5, μ = 100, σ = 15 (regression) |
| Power picture | N(0,1), μ₂ = 1, α = .05 | "power = 0.2595" on the plot and NE_P = 0.259511 (SciPy 0.259511); 68 light-green columns, all right of x* |
| Explorer: two-bound drag | between −1…1; drag b to 2; tap at −3; drag a past b to 3 | mode stays 3 throughout; a jumped (nearer bound); a and b swapped on crossing (1.985, 3.000); "area between" 0.0222 = SciPy; DRAWMENU once per frame, 11 of 11; no footer at y = 226 |
| Explorer: grabs | drag the mean line to ~1.06, lift; drag the right shoulder out ~1.0, lift | μ snapped to 1.0 (step 0.2), σ snapped to 2.0 (step 0.1); peak back at 62 % of the box (mean line 187→97); hint line names the held parameter on 6 frames; held line drawn 3 px wide |
| Explorer: soft keys | Bands, Ref ×3, Centre, Shade ×5, Hist, More, Menu (page 2) by taps at y = 228 | bands off; Ref 1→2→0→1; Shade left, right, between, outside, none; Hist with no histogram prints its note; "height 0.242 (density," shown; the CDF drawn while Ref = CDF |
| Explorer: soft-key page 2 | between −1…1; More, Bnd A, → →, Bnd B, ←, Bnd B again, →, sigma, →, Enter | a: −1 → −0.8 (step 0.1); b: 1 → 0.9; default restored, → moved μ 0 → 0.2; sigma chosen, → widened σ 1 → 1.1; mode stayed 3; page 1 labels end in More, page 2 labels drawn; "arrows move: lower bound" under the title and that bound drawn thick |
| Data: bars | 400 values in D1, tap the bar holding x̄ | "bin 17: 45 observed, 39.5 expected (n×p)": the index is the tapped bar, 45 = the count recomputed in Python, 39.5 = 400·p (SciPy 39.48); 23 filled bars; footer with "tap bar = counts" |
| Result view → Explorer | right tail at 1, tap in the plot | Explorer entered (DRAWMENU seen) with mode 2 kept |
| CDF overlay | N(0,1), left tail at 1 | "CDF(x₀) = 0.8413"; the S-curve list within 1.7×10⁻⁵ of SciPy; 26 drop-line pixels |
| The rest | animation, help, all 9 window items, a whole NormExp session | 22 animation frames; 3 help pages on G1; every window item ran; NormExp returned `NormExp: z = 1.6449, x = 124.6728, p = 0.2595` |

An off-device renderer (PIL, from the same recorded calls; scratch tool, not delivered) was used to look at ten screens and audit every text's right edge and the y ≥ 218 strip; it led to change 9's layout rule (below) and found no text off the screen.

## A. The numbered changes

| # | Task | Old lines | New lines | What was done |
|---|---|---|---|---|
| 1 | Two-bound drag; the area rides the region | 735-753 (750 collapsed modes 3/4 to a left tail) | 1003-1301 (press 1082-1132, drag 1134-1178, lift 1180-1195); 2574-2620 (`ne_Tag`); 3235-3260 | The Explorer now tracks a finger as **press → drag → lift** (`exDown`), and the poll loop also returns while the finger is down so the lift is seen. On the press it picks what to hold from positions **recorded by the frame on screen** (`neAPX`, `neBPX`, `neMuPX`, `neSgL`, `neSgR`, -999 when not drawn): the nearest within 8 px wins, bounds first on ties. Nothing near: the **nearer bound jumps** to the finger (with one bound, x₀; with none, a left tail starts, as before). Modes 3/4 are **kept**. Dragging one bound past the other swaps them and the finger keeps holding the one it is on. A finger that leaves the box keeps dragging, pinned to the edge. **`ne_Tag`** prints the area in a small white box centred on the shaded pixel span, half-way up the tallest column of that span (the one nearest μ), font 2 (font 1 when the span is 40-59 px), nothing below 40 px; outside shading tags each tail with its own area. |
| 2 | Soft keys (two pages after A2) | 2232-2235 (Explorer footer); 312 `NPBOT := 210` | 1065 (`DRAWMENU` after every frame); 1085-1089 (slot); 1197-1282 (actions); 413 `NPBOT := 188` | `DRAWMENU({"Bands","Ref","Centre","Shade","Hist","Menu"})` right after `ne_NormDraw`'s blit; a press with y ≥ 218 is drained (`ne_Drain`) and read as slot `MIN(6, IP(x/53.4)+1)`. Keys and soft keys share one action code (`exCmd`): + Bands, − Ref, 0 Centre, Esc/Enter Menu. **Shade** cycles left → right → between → outside → none from the current x₀ (between starts at μ ∓ \|x₀ − μ\|, one σ if x₀ = μ; an off-screen x₀ comes back to μ + σ). **Hist** toggles bar-reading mode (or says there is no histogram). The Explorer footer is gone. The box bottom moved 210 → 188: ticks 188-192, x labels from 193 (was BOT+7, now BOT+5), z labels from 205; the lowest text ends at 216. |
| 3 | Grab μ and σ | — | 1109-1117 (grab), 1155-1173 (drag), 1185-1191 (snap); 2996-3052 (thick lines, shoulder squares) | μ: the press on the mean line, then μ moves by the finger's movement since the press (no jump), kept inside the window. σ: the press on a shoulder (μ ± σ, small squares drawn in the Explorer), σ = σ₀ ± movement, outward wider, floor = the σ step. The held line (mean, both shoulders, or a bound) is drawn 3 px wide and the hint line under the title names it. On lift μ and σ snap to the arrow keys' NiceNum steps; the y-scale refits on σ (during the drag and on the snap), never on μ; the x-window never moves. |
| 4 | Live result views | 659-667 | 850-882; 952-972 (`ne_BarHit`); 770-796 (`ne_Drain`, `ne_WaitAny`); 826 (ZPanel) | `ne_ShowCurve` loops on `ne_WaitAny` (the house drain-wait-drain on keys AND touch): a tap on a bar shows its panel and stays; a tap anywhere else in the plot box calls `ne_Explorer` with the shading as it is; a key, or a tap outside the box, returns. The result panel (`ne_ZPanel`) and the help pages also accept a tap. |
| 5 | Filled bars; tap a bar | 2029-2047 (three LINE_P per bar) | 2838-2901 (bars), 3262-3284 (panel) | One `RECT_P(G1, …, NGRN, fill)` per bar, after the shading and under the curves. Inside the shaded region a bar is filled deep orange (`neBARS`), so the shading still reads as one region; a bar a bound crosses is split there (up to three pieces, each coloured by whether its middle is shaded, `ne_InShade`). Each bar's box is recorded (`neHX1`, `neHX2`, `neHY1`). The read bar is outlined red; the orange-framed panel says "bin k: O observed, E expected (n×p)" and "x from … to …, p = …", with p = F(right) − F(left) under the curve drawn now. |
| 6 | Shading sweep | — | 900-947 (`ne_Sweep`); `neSweep := 1` at 1471, 1503, 1547, 1570, 1595, 1622, 1648, 1863 | After every probability panel (4 in menu 3, 5 in menu 4, the power picture): the window is fixed for the final picture, then nine frames with the bound at 1/10 … 9/10 of the way from the edge (left tail from the left edge, right tail from the right edge, outside each tail from its edge, between both bounds from μ — or from the middle of a…b when μ is outside it); the result view itself is the tenth. Between frames a 70 ms `TICKS` pause polls GETKEY and MOUSE, so any key or touch ends the sweep (`WAIT` would not listen). Footer during the sweep: "any key or tap = skip". The cached pdf means no NORMALD per column on any sweep frame. |
| 7 | CDF overlay | 784 (− toggled 0/1); 860-861, 898-901 | 1236-1241; 1342-1430 (menu 9 item 6); 2693-2711 (cache); 2955-2975 (curve, axis); 3076-3093 (drop lines); readout in 3149-3233 | `NE_CFG(2)` is three-way: 0 none, 1 N(0,1) reference, 2 the CDF. The Ref soft key and − cycle 1 → 2 → 0 → 1; menu 9 has one item for each overlay (turning one on turns the other off). The S-curve is magenta on a right-hand 0…1 axis (1 at six pixels below the box top, a tick at ½, "1" outside the box). It is built from the cached pdf by trapezoids (one NORMALD_CDF, not 273) and cached with it. Dotted drop lines (`PIXON_P` every 4th pixel) run from each bound's point on the S-curve to the right axis; the readout adds "CDF(x₀) = …" (or CDF(a), CDF(b)) from NORMALD_CDF itself. |
| 8 | z-ruler | — | 2816-2836 | A grey row at y = BOT+17: "z" at the left, then −3…3 centred at x = μ + kσ (in the window only); every other label when σ < 14 px, none below 7 px. Drawn on every plot, the animation included (where it slides and stretches with the curve). |
| 9 | Height is not probability | 2202-2213 | 3171-3191 | In the Explorer (NE_KH = 1), modes 1/2 read "area to the left = 0.8413" (or right) and then "height 0.242 (density," / "not a probability)", with 3-6 decimals so a small density is not printed as 0.000 (rule checked in Part A). Two bounds read "area between / outside". Result views keep the P(X < x₀) notation of the panel before them. **Layout rule added after the renderer showed the column sitting on the curve:** in the Explorer while something is shaded the 68-95-99.7 text block is not drawn (the bands themselves still are) and the column starts at the top of the box (y = 44); with the second curve on, the two density lines are left out (the power line takes the corner). Long lines start further left (`ne_RTxt`) so they end on screen. |
| 10 | Critical values | 1007-1086 (right tail only) | 1513-1660 | Menu 4 is: percentile; right tail; **left tail** (z* = Φ⁻¹(α), shading mode 1); **two tails** (z* = Φ⁻¹(1 − α/2), x* = μ ± z*σ, shading mode 4 so both tails shade and each is tagged α/2); central interval (**now item 5, was 3**). |
| 11 | Power picture | 2005-2013 (overlap pass) | 1810-1870 (menu 7 item 3); 2765-2797; power readout | With curve 2 on and mode 2, the overlap fill stops at x*, and past x* light green fills from curve 1 up to curve 2 wherever curve 2 is higher (read from the cached second pdf), on top of the orange α; the readout adds "power = …" = 1 − NORMALD_CDF(μ₂, σ, x*). Menu 7's new item 3 asks for α, sets x* = μ + z₁₋α σ, turns curve 2 on at the current μ₂ and shows a panel (α, x*, μ₂, d, power, β) before the curve. |
| 12 | Help pages and guide | 1744-1788 (two pages, G0, key only) | 2343-2430; header 1-165 | Three pages composed on G1, each held by `ne_WaitAny`: the modules; the Explorer's soft keys (two columns, since the font is proportional) with their key shortcuts; touch. The header's beta 42 paragraph lists all twelve, the file map has the new routines and the true line count (3324), the MAIN MENU listing and the "every calculation panel" note are updated, and the guide is named. |

Also changed, in support of the above:

- **The main and second pdf lists are cached across frames** (old 1932-1949 → new 2658-2691, state at 499-508). Keys `{μ, σ, xmin, xmax}`; rebuilt only when one changes, so a drag of x₀ or a sweep frame evaluates no NORMALD per column. `ne_ResetAll` starts the keys as lists `{0,0,0,0}` so `nePdfK(1)` is never an index into a number.
- **File-level state** for the touch records, the caches, the hint line and eight house colours (499-537), all initialised in `ne_ResetAll` (2448-2490).
- **The standardize animation's second caption** moved from y = 200 to 172 (old 1654 → new 2256): the box now ends at 188, so 200 would sit on the axis labels.
- **Footers in the house form and colour** (dodger blue, `=` with spaces): "tap plot = explore, any key = menu", "tap bar = counts, tap plot = explore, any key = menu", "any key or tap = skip", "any key or tap = next page".
- Menu 7's label in the main menu: "Compare curves (d, power)". Menu 9 has nine items: Show current window is now 7, Diagnostics 8, Reset 9.

## A2. Follow-up (16 Oct 2026, Roger): the "More" soft-key pages

Roger's house convention (BRIEF_TOUCH, "Soft-key pages"): slot 6 is **More** on every page and turns the page. Applied in the Explorer, it closes the open item "the bounds have no arrow-key equivalent".

| Page | Slot 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 (on entry) | Bands | Ref | Centre | Shade | Hist | More |
| 2 | Bnd A | Bnd B | mu | sigma | Menu | More |

- **Menu moved to page 2, slot 5.** Esc and Enter still open the menu from either page; + − 0 are still Bands, Ref, Centre.
- **Page 2 chooses what ← → move** (`exArw`, new local): Bnd A = the lower bound (x₀ with one bound), Bnd B = the upper bound, mu, sigma (← narrower, → wider). Bounds step to the next multiple of NiceNum(σ/10), as μ and σ already did; stepping one bound past the other swaps them and the arrows carry on with the one they now hold. ↑ ↓ always change σ. Tapping the chosen key again returns to the **default, which is beta 42's behaviour unchanged**: ← → μ, ↑ ↓ σ.
- **The chosen handle is drawn thick** (the same thick drawing a finger's grab uses, `neGrab`) and the line under the title says "arrows move: lower bound" (upper bound, μ, σ (← narrower, → wider)). A finger's drag hint and the Hist hint take that line while they apply.
- Bnd A with no shading starts a left tail at x₀ (brought on screen if needed, as Shade does). Bnd B needs two bounds: chosen with one bound or none it says "Bnd B needs two bounds: Shade to between or outside"; if Shade later leaves one bound, the target falls back to Bnd A.
- Code: ne_Explorer 1019-1394 (header comment 978-1017; pages and target 1054-1063; hint and thick handle 1074-1095; `DRAWMENU(exSK(exPage))` 1101; slot → action 1126-1137; arrows 1252-1283; More and page-2 actions 1353-1375). Help page 2 (2470-2499) now lists both pages; the header's change (2) and MAIN MENU listing say so.
- Checked: gate unchanged (above); 9 new harness checks (the page-2 row of the table); the help page re-rendered (the page-2 rows use a wider second column, x = 80).

## B. DEVICE TEST CHECKLIST — least risky first

1. **Paste.** If the editor stops, note the line and the cursor: 497-537 (the file-level LOCAL lines — beta 41's one line, 393 there, plus the new ones; none has been pasted yet; if they fail, make each `LOCAL` an `EXPORT`, nothing else changes), 2623 (the 12-parameter head), 1065 (DRAWMENU), 3024 (`FOR … STEP 2` from −1).
2. **Help (menu A).** Three pages; a key or a tap turns each. Page 2 lists six soft keys in two neat columns; page 3 the gestures. Text inside the panel on both calculators (the G1's font is the narrower test).
3. **Menu 3 → P(X < x) on N(0,1), x = 1.** Panel (a tap now continues as well as a key) → the orange region grows in from the left edge over about a second, the readout and a boxed **0.8413** riding along → final view with "tap plot = explore, any key = menu" in blue. Check: the two label rows under the axis (x: −4…4; z: −3…3 in grey, with "z" at the far left) both end above the bottom strip. Press Enter: back to the menu. Repeat and press a key during the sweep: it jumps to the end.
4. **Menu 4, all five items** on N(100,15): percentile .90 → 119.22; right α .05 → 124.67; **left α .05 → z* = −1.6449, x* = 75.33**, left tail shaded; **two tails α .05 → ±1.9600, 70.60 and 129.40**, both tails shaded, each boxed 0.0250; central .95 is now item 5.
5. **Menu 9: the overlays.** Item 6 "CDF overlay (S-curve)": magenta S-curve, a magenta right edge with "1" at the top, dotted line from x₀ to it, "CDF(x₀) = …" in the corner. Item 5 again → the N(0,1) curve returns and the CDF goes. Items 7, 8, 9 are Show window, Diagnostics, Reset.
6. **A result view is live.** From step 3's view, tap inside the plot: the Explorer opens with the left tail still shaded and the soft-key strip along the bottom (no grey footer). Esc returns to the menu.
7. **Explorer soft keys** (menu 2): page 1 is Bands, Ref, Centre, Shade, Hist, **More**. Tap each — Bands (bands off/on), Ref (reference → CDF → none), Centre, Shade five times (left, right, between, outside, none — between starts symmetric about μ), Hist with no histogram (a grey note under the title). Tap **More**: page 2 is Bnd A, Bnd B, mu, sigma, Menu, More. With between shading: Bnd A, then ← →: the lower bound steps (thick red line, "arrows move: lower bound"); Bnd B likewise; sigma then ← →: σ narrower / wider; tap the chosen key again: ← → move μ as before. More returns to page 1; Menu (page 2) exits, and so do Esc and Enter from either page. The hardware keys + − 0 and ↑ ↓ still work. **Watch whether the labels survive every redraw and whether a tap on the strip ever fires twice** (it should not: the handler drains the finger first).
8. **Height vs area.** In the Explorer, tap at x = 1 on N(0,1): "area to the left = 0.8413", "height 0.242 (density," "not a probability)" at the top right (no 68-95-99.7 block while shaded). Menu 1 → σ = 0.2, explore, tap at μ: height 1.995 — bigger than 1, which is the point.
9. **Drag x₀** slowly across the plot: the boxed number travels with the shaded area (it disappears when the region is narrower than 40 px) and the corner readout follows. Note how smooth it is on the G1 (the curve is no longer recomputed per frame during this drag).
10. **Two bounds.** Menu 3 → between −1 and 1 → tap the plot → Explorer. Drag b to the right: the mode stays "between". Tap empty plot left of a: a jumps there. Drag a to the right past b: they swap and the finger carries on with the other one.
11. **Grab μ:** press on the dark mean line and drag sideways: the line thickens, the hint says "Dragging μ", the bell slides, the window does not move; lift: μ snaps to a round value (the arrow step). **Grab σ:** press a small square on the curve (μ ± σ) and drag outward: σ grows, the peak stays at the same height on screen while the y labels change; lift: σ snaps.
12. **Data and bars.** Put about 100 values in D1 (Statistics 1Var), menu 6 → "My data from D1": filled pale-green bars under the curve. Tap a bar: red outline and "bin k: O observed, E expected (n×p)". Tap another; tap empty plot → Explorer; press **Hist** and slide a finger along the bars; Hist again to go back to dragging x₀. With shading on, bars inside the shaded region are deep orange and split at the red line.
13. **Power picture.** Menu 7 → "Power picture: right-tail α" → α .05 (μ₂ is the item-1 value, μ + σ by default) → panel (power 0.2595 on N(0,1) with μ₂ = 1) → orange α past x*, light green above it under curve 2, "power = 0.2595". Tap the plot → drag x* left and right: α and power trade off live.
14. **Animation (menu 8).** Unchanged except the second caption now sits inside the box (y = 172) and the z-ruler stretches with the curve.
15. **Riskiest last — the drag loop's timing on the G1.** During a μ or σ drag each reading redraws a full frame (273 NORMALD for the new curve). If it feels sluggish, report frames per second; the bound drags and the sweep should be noticeably faster than beta 41 because they no longer evaluate the pdf.

## C. Not confirmed here, left as stated

- **Bounds and the keyboard** — resolved by A2: page 2 of the soft keys chooses what ← → move. Choosing still needs a tap (soft keys never produce key codes); once chosen, the bounds move from the keyboard alone.
- **A key pressed while a finger is on the screen is ignored** (the touch branch clears `exK`, as beta 41 did). Harmless, but Esc during a drag needs a second press.
- **`DIM` on a string** (ne_RTxt, ne_Tag, the z-ruler) is on the confirmed list; the older code's `SIZE(string)` (x-axis labels) was left alone.
- **The "1" of the CDF axis** is drawn at x = 313, in the 9-px margin right of the box; on a font slightly wider than 6 px it could clip at the screen edge.
- **Font metrics.** The layout was audited with a 6 px/char (font 1) and 7.6 px/char (font 2) model and an off-device render; the Prime's own fonts may need a pixel nudge (the riding box is sized from the string length).
- Pending from beta 41 and still not changed: the seven CHOOSE calls that keep the return value, the five `√`, `K` as the MAKELIST counter (now in four more MAKELIST calls, same form), the program's own hex palette for the old elements, the Diagnostics page's key-only hold.
