# BurrLab beta 1p: changes (7 November 2026, evening)

Roger, on his G1, the first run of BurrLab on the hardware: "in menu item 2. Family Tree, the box on the right side of the screen is very dark gray and I can't really see what's going on in it, and the shaded part of the plot on the left is very very light." Built from beta 1o by `make_beta1p.py` (exact replacements; a miss stops the build). Nothing in the arithmetic changed.

## What changed

1. **The (C, K) map was a solid dark gray box.** Its border was drawn as `RECT_P(G2, 0, 0, 91, 91, buGRAY)`, ONE colour, and a one-colour `RECT_P` FILLS (Lessons Learned s6): it painted over the three regions after they were drawn, leaving only the four labels on top. The PC harness records shapes without painting them, and the page was never looked at on the Virtual Calculator, so the box was seen first on the G1. Four `LINE_P` draw the border now. The three region tints are deeper (#FFC8C8, #FFDFB4, #C8EBD2 in place of #FFEBEB, #FFF0DC, #E8F6EB): the pale ones vanish on the G1's screen.
2. **The tail shades were half-transparent washes.** `bu_Shade` drew its polygon with alpha 128, so the shade was half white before the screen saw it (#AACDFF at half strength is #D4E6FF; #FFEBEB at half strength is #FFF5F5). The shade is opaque now, in the tints themselves (blue on Explore, pink on How rare), and the curve is redrawn over it from the x₀ column to the right edge so the fill does not eat the inside half of its line.
3. The welcome page's title names beta 1p.

## Checks

- `tools/ppl_gate_v1e.py` (lint version 4, whose new check 13 reports exactly this kind of `RECT_P` and nothing else in the fleet): pass; hp-prime-kit lint 0 errors on the copy with the Python blanked; the lint's 27 lines are beta 1o's own (the `#END` of the Python block and the bare-number concatenations in `mlTx`).
- The PC harness ran Family, Explore, and How rare without error; `tools/page_render_v1.py` (new this round) painted the pages: beta 1o's map is the gray box Roger saw, beta 1p's shows the regions, the Lomax and Fisk lines, and the dot; the shades are solid with the curve on top.
- `tools/monkey_v1b.py --lists`, 300 runs, seed 1: 295 OK, 5 HARNESS (RANDSEED, the harness's own gap, as in beta 1o's runs), no CRASH, GUARD, FREEZE, STALL, or STATE.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 7 Nov 2026: Check said "No errors in the program"; the Family page shows the map with its three tints, the Lomax and Fisk lines, and the red dot inside a gray border; Explore's tail shade is solid light blue with the curve on top; How rare's is solid pink. Screens in `D:\HP-Prime\_vc_screens_2026-11-07\` (bl_*.png, 960 × 720).

Not yet run again on the G1: Roger will see whether the deeper tints and the opaque shades read well on its screen. The three map tints and the two shade colours are the constants `buLRED`, `buLORN`, `buLGRN`, and `buLBLU` in `bu_Init`'s colour block, one line each, if they need another step.
