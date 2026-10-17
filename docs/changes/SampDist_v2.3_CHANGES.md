# SampDist v2.3 — changes from v2.2

*16 October 2026. Touch and graphics version, built on the v2.2 fix version (every v2.2 fix kept). NOT yet run on hardware.*
*"Old" line numbers refer to `SampDist_v2.2.txt` (708 lines); "new" to `SampDist_v2.3.txt` (1611 lines, UTF-8, LF).*

## A. The changes

| # | Task | Old lines | New lines | What was done |
|---|------|-----------|-----------|---------------|
| 1 | Population ghost | — | `sd_curves` 418-463; window in `sd_live` 715-737 | N(μ, σ) drawn as a faint grey (150,150,150) polyline (every 2nd column) behind x̄'s blue curve on the probability and critical-value graphs, labelled `population (σ = 15)` just above the curve at μ + 1.2σ (or at the right end when that shoulder is off the window). ONE y-scale, fitted to x̄'s curve (`ymx = 1.15·NORMALD(μ, σx̄, μ)`), so the population's peak is 1/√n of x̄'s — the harness measured 0.183 at n = 30 (1/√30 = 0.183). The x-window is fitted on entry as μ ± max(4σx̄, min(3.5σ, 16σx̄)) — the population's shoulders show at moderate n and x̄'s curve stays about a quarter of the plot wide — then FROZEN while n changes (Lessons Learned §6), so the population stays put and x̄'s curve narrows. It refits only if x̄'s curve outgrows it (2.5σx̄ > half-width), and says so. |
| 2 | Soft keys on the result graph | footers 378 | `sd_compose` 571-686; `sd_live` 689-963 | `DRAWMENU({"n−","n+","n×4","μ,σ","Tail","Menu"})` after every blit (labels built with CHAR(8722), CHAR(215), CHAR(956), CHAR(963)). n− / n+ step through 1 2 4 5 10 16 20 25 30 40 50 64 100 160 200 400 (from a typed n like 37 they go to 30 / 40); n×4 multiplies n by 4 up to 1600; μ,σ reopens the form (with α in critical mode; in probability mode the bounds form follows so the bounds can follow a new μ; invalid values are refused with a message and nothing changes); Tail cycles left → right → between → outside (critical mode: lower → upper → two-tailed, α kept); Menu returns. After each, P, the σx̄ line and the shading are recomputed. Probability mode: a new n keeps the bounds and changes P. Critical mode: a new n keeps α and moves the critical values. Footer text moved into the panel's fourth line (the strip occupies y ≥ 218); the plot box is now x 40-314, y 20-150 and the panel y 166-216. Hardware shortcuts: + / − = n+ / n−, Enter = a CHOOSE with n×4, edit, next tail, back; Esc = menu. **"More" soft-key pages (the 16 Oct convention) were considered and not applied: every screen's actions fit in six slots.** |
| 3 | Live bound | `sd_drawDist` 227-387 | `sd_compose` 571, `sd_live` 689, `sd_fix` 548 | `sd_drawDist` split into compose (`sd_compose`, draws G1, blits, DRAWMENU) and the wait/interaction loop (`sd_live`). A finger in the plot box moves the NEARER bound (chosen at the press, kept for the drag); P recomputes each frame (two NORMALD_CDF calls; the curves come from cached pixel rows — no NORMALD per column during a drag). On lift the bound snaps to a step of NiceNum(σx̄/4) (0.5 at σx̄ = 2.74); Left/Right move the active bound by the same step onto the grid; Up/Down choose the other bound in a two-bound region (the active bound is drawn 2 px wide with a red handle). Dragging one bound past the other swaps them. In critical-value mode the drag changes α (read back from the bound; two-tailed keeps the pair symmetric about μ; α kept within 0.000001-0.999999 so NORMALD_ICDF never sees 0 or 1). A redraw happens only when something changed (NormExplorer beta 41's rule). *Note:* the brief says "the probability recomputes from the cached pdf"; it is computed with NORMALD_CDF instead — exact, and the same formula as the menu path — while the drawing uses the cache. |
| 4 | Compare view | `sd_drawCmp` 392-464; `sd_drawOne` 199-220 | `sd_drawCmp` 966-1180 | Fills under the three curves, widest (largest σx̄) first, in light red / blue / green (255,235,235 / 235,242,255 / 232,246,235), then all outlines; on opening, n grows as nᶠ⁄⁸ over 8 frames so the curves start as the population and squeeze (any key or tap skips); a finger on the plot is a black vertical cursor with the three P(x̄ < x) values in the legend colours and a dot on each curve; a tap (≤ 8 px movement) within 6 px of a curve above the axis picks it — drawn 3 px thick, "n = 160:  σx̄ = 1.1859" printed top-left in its colour; a tap elsewhere clears. The finished scene is composed once into **G2** and copied into G1 per cursor frame (GaltonBoard's scene + frame idiom). Footer `drag = cursor, tap a curve = pick, any key = menu`. v2.2's σ-in-title fix kept (title now width-clipped at 308 px). `sd_drawOne` replaced by `sd_pdfList`/`sd_pyList`/`sd_poly`/`sd_fill`. |
| 5 | Watch sample means | — | `sd_watch` 1337-1494; menu 1557-1584 | New menu item 4 (Help moves to 5). Form μ, σ, n (100, 15, 30). 40 samples of n draws from N(μ, σ) via `sd_Norm` (Marsaglia polar, PPL, CentralLimit's `cltNorm` shape); each mean falls as a red dot (5 frames for the first six, 2 after) and lands magenta, stacked in 4-px columns on the axis under x̄'s curve; then a histogram of the 40 means (bars one σx̄ wide, edges at μ + kσx̄, height count/(40σx̄) so it shares the curve's density scale), a rug of the means, and the panel: mean of the 40 (vs μ), their SD with n − 1 (vs σx̄), σ vs σx̄. Above n = 100 each mean is drawn directly from N(μ, σx̄) and the screen says so. Any key or tap skips the drop. Scene in G2, landed dots added to G2. |
| 6 | y-axis labels | — | `sd_axes` 466-501 | Density ticks on the NiceNum ladder (about four, none in the top 5 %), grey labels right-aligned left of the axis. x labels are also clamped so the last one cannot run past x = 318 (the harness found "20000" ending at x ≈ 329 at extreme inputs, as in v2.2). |
| 7 | Help, footers | `sd_showHelp` 610-651 | 1497-1554 | Two drawn pages held by `sd_WaitAny` (key OR tap; capped drain), documenting the population curve, soft keys, drag, keys, the compare gestures, Watch. Footers in the house form, dodger blue: `any key or tap = next / = menu`, `any key or tap = skip`, and the result graph's key line in the panel. |
| 8 | Touch kit | — | 262-292 | `sd_Drain` (capped finger-lift drain) and `sd_WaitAny` (returns the key or −1) — ChiTable's `csDrain`/`csWaitAny` shapes. Every wait after a form or menu drains keys and touch first. |
| 9 | Header | 1-145 | 1-211 | v2.3 paragraph (every change, v2.2 line numbers), the house licence paragraph added after the existing (C)/AI lines, firmware line "v2.3 NOT yet run on hardware (nor has v2.2)", menu list, the in-file device checklist updated. |

New tagged helpers: `sd_Drain, sd_WaitAny, sd_Norm, sd_pdfList, sd_pyList, sd_poly, sd_fill, sd_quick, sd_grid, sd_curves, sd_axes, sd_prob, sd_crit, sd_fix, sd_compose, sd_live, sd_watch`. Gone: `sd_drawOne`, `sd_drawDist`. `sd_modeProb` / `sd_modeCrit` / `sd_modeCompare` keep their forms, checks and formulas; the two first now end in `sd_live(...)`. `sd_prob` / `sd_crit` hold copies of the mode 1 / mode 2 formulas (the harness checks they agree with v2.2 to 1e-12). No file-level LOCALs were added (the kit interpreter cannot parse them, and the original parsed): all live state is in `sd_live`'s LOCALs and passed as lists (`st`, `geo`).

## B. Gate (`check.sh out/SampDist_v2.3.txt out/SampDist_v2.2.txt`, final run)

```
kit lint: 0 errors
ppl_check tally NEW: 2 E4, 3 E9        ORIG (v2.2): 4 E4, 4 E9   (fell)
hard errors E2/E3/E6/E8/E10/E11: none
lint_ppl: 1260 checks, 18 problems = the 4 v2.2 noise lines (entry-point/EXPORT naming)
          + 14 "targets 'poG'/'axG'... not a GROB" (GROB passed as a parameter, the
          ChiTable csDotV idiom -- listed as known noise in the brief)
full parse: PARSE OK (25 functions)    ORIG: PARSE OK (10 functions)
1611 lines, 67547 bytes
fleet_names_v2 over the newest version of all 22 programs: 0 collisions, 0 untagged,
          0 mixed-tag, 0 built-in matches
```

## C. Harness run (`verify_SampDist_v2.3.py`, using `ppl_harness_v1.py`)

No `ppl_run_v1.py` existed, so `ppl_harness_v1.py` was written: it loads the real file into hp-prime-kit's interpreter, supplies NORMALD / NORMALD_CDF / NORMALD_ICDF from SciPy, STRING modes 1 and 2 (mode 2 rounded decimal half-up, as the Prime does), RANDOM (seeded), TICKS, and scripted GETKEY / MOUSE (keys, taps, drags), CHOOSE and INPUT answers written back into the named variables; every graphics call is recorded per frame. **317 checks, 0 failures**:

- **Numbers unchanged:** 65 cases (5 parameter sets × 4 regions, × 3 tails × 3 α) through v2.2 AND v2.3 — all six EP_SD_* identical to 1e-12 and equal to SciPy.
- Soft keys: n×4 / n+ / n− / Tail sequence (30 → 120 → 160 → 100 → 64; left → right → between → outside → left): every frame's header n and printed P match SciPy; the ladder ends (1, 37, 400, 1000) and the n×4 cap at 1600, each with its message.
- Drag: nearer bound chosen, live value, snap to 0.5 on lift, Left/Right steps, Down switches bound, crossing swaps — P = SciPy throughout.
- Critical mode: n×4 moves lo to the SciPy quantile with α kept (all three tails); a two-tailed drag stays symmetric, α read back = 2Φ(lo); a later n×4 keeps the dragged α; Tail cycle.
- μ,σ form + Enter menu; invalid σ refused with nothing changed; α edit in critical mode.
- Compare: 8 opening frames; every cursor reading equals Φ at the cursor's x for each n; a tap at the n = 160 peak picks it (σx̄ = 1.1859); fills drawn widest first for both n orders.
- Watch: the 40 means re-simulated in Python from the same RNG stream (Marsaglia) — printed mean and SD agree at 3 decimals for n = 30, 4 and 250 (direct-draw note shown); histogram bar heights sum to ≈ 40; a key skips the drop.
- Pictures: population/x̄ peak ratio 0.183 at n = 30; label text; density labels; x window identical before and after n×4 twice; help = 2 pages; all unclipped font-1 text ends by x ≈ 319 (6.2 px/char estimate).
- Cost: a live drag frame draws 436-502 primitives (right tail, n = 30) — most of it the population polyline (≈137) and the shading.

## D. DEVICE TEST CHECKLIST (in this order, G2 first, then G1)

1. **Paste.** New constructs: `DRAWMENU` with labels built from `CHAR(8722)`, `CHAR(215)`, `CHAR(956)`, `CHAR(963)`; `CHAR(8646)` / `CHAR(8645)` in strings; `FOR … STEP 2` (sd_quick); `DIMGROB_P(G2, …)` and `BLIT_P(G1, 0, 0, G2)`; GROBs passed as parameters to helpers (ChiTable's csDotV does this).
2. **Menu:** five items, Watch sample means is 4, Help is 5.
3. **Find probability**, defaults (0, 1, 30), Left tail, a = −0.5. Expect: grey population bell (peak ≈ 18 % of the blue one) with "population (σ = 1)" by its right shoulder; blue x̄ spike; density labels 0.5 … 2.0 in grey on the left; panel with P = 0.003085, z line, σ line, and the key line in dodger blue; soft keys `n− n+ n×4 μ,σ Tail Menu`. Check the soft-key labels render (the minus, ×, μ, σ glyphs).
4. **n×4** (slot 3): n = 120, the blue curve narrows to half width, the grey curve does not move sideways (it gets lower: same scale), P drops to 0.000130. **n+** → 160, **n−** → 100. Tap each slot once.
5. **Tail** four times: right, between (bounds become symmetric about μ), outside, left. Shading follows.
6. **Drag:** in "between", put a finger near the left bound and slide; the bound and P follow the finger; lift — the bound snaps to a round step. Left/Right nudge it; Down then Right moves the OTHER bound. Drag one bound past the other: they swap, nothing breaks. **On the G1 note whether the drag feels smooth** (≈ 450 primitives per frame).
7. **μ,σ** soft key: the form opens with the current values; change μ to 50, OK; the bounds form follows; OK. Window refits. Try σ = −1: "σ must be > 0; nothing changed".
8. **Enter** on the graph: the "More" CHOOSE (n × 4, Edit, Next tail type, Back to menu); each works. Esc returns to the menu.
9. **Find critical value**, two-tailed, α = 0.05: both red lines at μ ± 1.96σx̄, central region shaded, P = 0.950000. n×4: lines move in, P stays 0.95. Drag a line: both move symmetrically, P (= 1 − α) changes; lift snaps.
10. **Compare sample sizes**, defaults: 8 frames of curves squeezing from the population (caption "n growing: …"), then filled curves (pale red widest, blue, green on top). Touch and slide on the plot: a black cursor with three P values in red/blue/green. Tap the top of the green curve: it thickens and "n = 160: σx̄ = 1.1859" appears top left. Tap empty space: cleared. Any key = menu. Re-open and press a key during the opening: it skips. *If `BLIT_P(G1, 0, 0, G2)` errors, this is the first fleet program to depend on it (GaltonBoard beta 1b also does) — report the line.*
11. **Watch sample means**, defaults: dots fall one by one (slow for six, then faster), stack on the axis under the blue curve; then the histogram, the rug, and the panel lines (mean of the 40 near 100, SD near 2.74). Repeat with n = 250: the direct-draw note. Tap during the fall: it skips to the histogram.
12. **Help:** two pages, each dismissed by a key or a tap; text fits.
13. Widths at extremes: Find probability with μ = −12345.678, σ = 12345.678, n = 100000, Between −20000 … 20000 — panel lines are clipped at the panel edge, not run off; the last x label stays on screen.
14. **Home:** EP_SD_* hold the last live state (e.g. after n×4 EP_SD_SE is σ/√(4n)).
15. Carried from v2.2: `√` in "/√30" renders; ₃ in "n₃:"; CHOOSE items built with CHAR(57344).

## E. Not confirmed / left as it was

- `BLIT_P(G1, 0, 0, G2)` / `DIMGROB_P(G2,…)` are GaltonBoard's idiom and not yet run by any fleet program on hardware; used only in Compare and Watch, never on the core probability path.
- G1 frame cost during a drag is estimated, not measured.
- CHAR(8722) (minus) and CHAR(8646)/(8645) arrows are on CLAUDE.md's verified palette list but not in the brief's CHAR list; CHAR(215), 956, 963, 57344 are.
- The harness models STRING mode 2 as decimal half-up rounding of the binary value; ties that differ only in binary representation can show one digit differently from the device (none in the SampDist checks).
- The two-tailed critical value still shades the central 1 − α (v2.2 behaviour; the review's "offer both" idea was not in this brief).
- `K` remains the MAKELIST counter (GfxProbe T19 pending).
