# BurrLab beta 1l: changes

*2 Nov 2026, night. Made from beta 1j by way of beta 1k (never shipped), each by exact replacements (`make_burr_1k.py`, `make_burr_1l.py`). 4,647 lines. Beta 1k's changes are listed first; the repository goes from beta 1j to beta 1l.*

## Why

Roger tried beta 1j and then 1k on the Virtual Calculator, 2 Nov 2026:

- "ON the Burr program, in the Explore--I can move x0 WAY out to the hundred's of thousands and that really messes up the plot--do we need to put some caps on c, k, s, and x0?" Then: "I think we might want to cap S at something less than 1,000,000", and "cap at 1,000 is just right".
- "IN Burr, Explore...is there a y-axis? If so I can't see it--there is a number in the upper left of the white area of the plot just under the orange ribbon, but I dont know what that's for".
- "Also, some of the menu items run out of the box".

## What changed

**Beta 1k: x0 and S keep to the plot.**

1. **x0 stops at the plot's right edge.** Beta 1j's window stretched to 1.15 x0 and each arrow step was a fortieth of the window, so every press made the next step bigger: 400 presses took x0 to 460,000,000. The window is now the curve's own (its 0.995 quantile, at most 50 S), and x0 stops at the last step inside it. When C, K or S shrink the window, x0 comes back inside it (`bu_Window`, `bu_ExpStep`).
2. **S stops at 1,000** (it was 1,000,000), for the arrows, the drag and the Family page's S key, so the x axis runs to 50,000 at most. An S already above 1,000 (a fit to data in large units) is not pulled down by an up press; it just goes no higher. C and K keep their range, 0.2 to 50.

**Beta 1l: a y axis you can see.**

3. **Every plot has a y axis drawn by one routine, `bu_YAxis`:** a dark line up the left edge and along the bottom; two to four ticks at a 1-2-5 step, each with a pale grid line across and its number left of the axis; "0" at the bottom; and the axis's name in the row above the plot. The pages: Explore (pdf view), Family, How rare is this? ("pdf"), Histogram ("density", or "density per log10 unit"), Q-Q ("data quantile"), Hazard ("hazard h(x)"), The mean that never settles ("running mean"). Before, the y axis was the box's left edge in the grid's pale grey, and its only numbers were "0" and the top of the axis, written above the box with no tick and no name: the number Roger asked about.
4. **Numbers that would not fit are written in units, never cut.** A y number is sized before it is drawn (about 5.5 px a character, 3 px for the point; Lessons Learned). It must start 2 px or more from the screen's edge and end 2 px short of its tick, so it can be at most 28 px wide. On the Virtual Calculator, beta 1l's first build drew "0.0008" (at S = 1,000) from x = 0, and the screen's edge took half its first 0. When any number of an axis would be wider, or would come out scientific (`STRING(x, 2, 0)` is scientific from 1E12: 1.5E13 would read "2E13"), the whole axis counts in units of a power of ten, named after it, as a textbook writes "in thousands": at S = 1,000 Explore reads **"pdf (×0.0001)"** over 2, 4, 6, 8.
5. **The log axes** (Q-Q on log scales, Survival) put their powers of ten by the same rule (`bu_LogY`). The Survival page names its axis "survival P(X > x) (log)"; both get the dark axis lines.
6. **An x-axis label that would touch the one before it is left out, its tick kept** (`bu_TickLbl`, `bu_XAxis` and Explore's own row in `bu_ExFrame`). On the Family page's narrow plot at S = 1,000 the Virtual Calculator showed "1,0002,0003,000": beta 1j's commas made each label wider than the step. Explore at C = 0.2, K = 20, S = 0.01 drew "0.000020" over "0.000025".
7. **Explore's grey status row keeps its numbers whole.** At C = 0.2, K = 20, S = 0.01 it was wider than the screen and "SD < 0.0001" was cut off; now the note "(C ≤ 1)" goes first, then the SD if need be, never a number cut in two.
8. **Menu items of at most 30 characters** (the box shows about 30; the fleet's rule since round 2, TestChooser 2a and PowerViz 2.5g). Ten items of 31 to 40 characters ran out of the box. They now read: main menu "Family: Lomax, Fisk, Weibull", "The mean that never settles", "How rare is this? (1 in N)"; Fit "BJS homicide: months served", "Rossi: weeks to re-arrest", "Danish fire: 300 losses", "Danish fire: 2,156 in bins"; Fit engine "Auto: Python, else PPL", "Python only (errors show)", "Both: time and compare". The Virtual Calculator showed every item whole, the box sized to the longest.
9. Gone, since the axis's name says it: Explore's "pdf" at the foot of the plot, the Histogram's name at its top right, the Hazard page's "h max". Header: the beta 1k and 1l blocks; the version named on the screen.

Routines changed: `bu_Window`, `bu_ExpStep`, `bu_Explore`, `bu_Family`, `bu_Help` (1k); `BurrLab`, `bu_DrawFam`, `bu_DrawRare`, `bu_ExBase`, `bu_ExFrame`, `bu_FitMenu`, `bu_HazPage`, `bu_Hist`, `bu_QQ`, `bu_SimFrame`, `bu_Surv`, `bu_TickLbl`, `bu_XAxis` (1l); `bu_Opening` (both). Added: `bu_LWd`, `bu_LogY`, `bu_YAxis`.

## Verification

`verify_BurrLab_beta1k.py` (against beta 1j): **12 PASS, 0 FAIL**. X1: 400 presses up with x0 chosen leave x0 = 56 inside the window 57.6 (beta 1j: 460,000,000); X2: S / 10 brings x0 back inside; X3: C and K 0.2 to 50, S 0.01 to 1,000 under 600 presses each way; X4: S = 5,000 stays under an up press; R, M, C, Y, D as below.

`verify_BurrLab_beta1l.py` (against beta 1k), output `verify_BurrLab_beta1l_output.txt`: **21 PASS, 0 FAIL**.

- **G** static: only the routines above differ; `bu_YAxis` comes before its seven callers and after what it calls (BurrLab declares nothing ahead); its numbers are drawn only when at most 28 px wide, with a width argument of 36 (never cut); fixed decimals only up to 12; every call of `bu_TickLbl` keeps where its row's last label ends; every menu item at most 30 characters.
- **Y1** `bu_YAxis` alone at 400 axis tops from 1E-12 to 1E14: every number (times its unit) is its tick's value, level with it, at most 28 px, 2 px or more from the edge, grouped with commas, never scientific; in units, whole numbers with the unit in the name. 107 axes in plain numbers, 293 in units; two to four ticks above 0; 38 numbers left out, all within 4 px of the top (they would meet the name).
- **Y2** Explore at C and K in {0.2, 0.5, 1, 2, 5, 20, 50} and S in {0.01, 1, 10, 1000}, both views (392 screens): the pdf view names its axis and writes its numbers; the CDF view writes nothing left of the axis; nothing over anything, nothing cut.
- **Y3** the other pages on the three presets: each names its axis and writes its numbers; nothing over anything, nothing cut.
- **Y4** `bu_XAxis` at 600 ranges on the narrow and the wide plot: no label within 3 px of the one before it; Family at S = 1,000 and Explore at C = 0.2, K = 20, S = 0.01 as above.
- **R, M, C, Y, D** (`tools/comma_check_v1.py`, 30 seeds of the monkey on both versions): every run takes beta 1k's path; every number of four or more digits drawn is grouped; every text handed to the CAS is beta 1k's, call for call; no year grouped; no new overlap, straddle or overrun, no number cut.
- Overlap rule: `tools/text_overlap_v1` calls a finding firm "when it survives the narrower measured glyph widths too" but judges only right-edge straddles at those widths. The script judges a left-edge straddle at them as well (`label_fit_v1.measure`), and says so: the y numbers end 2 px short of their ticks at the measured widths, and the Virtual Calculator showed the gap.

## Gate

`ppl_gate_v1d.py BurrLab_beta1l.txt BurrLab_beta1k.txt`: PASS. The kit's linter finds 0 errors; `ppl_check_v5` is clean; `lint_ppl`'s 27 items and the kit parser's "expected a name after EXPORT" are beta 1j's and 1k's too (the `#PYTHON` block). `fleet_names_v2.py` over the 30: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Virtual Calculator 2.4.2 (Rogers-HP, 2 Nov 2026, night; Claude through computer use). Each build was copied into the calculator's folder with the calculator closed, opened in the editor and Checked: **"No errors in the program"**. The file it wrote back after the Check alone is the one in the starter pack.

- Beta 1k: S stopped at exactly 1,000 after 60 up presses; x0 stopped at 5,600 at the plot's right edge (P(X > x0) = 0.0054).
- Beta 1l: Explore's axis read "pdf" over 0.02 ... 0.08 at the start; at S = 1,000, the first build's "0.0008" lost half its first 0 to the screen's edge (hence item 4), and the final build read "pdf (×0.0001)" over 2, 4, 6, 8. Family at S = 1,000 showed its y axis; its x labels ran together on the build before item 6 was made. The main and Fit menus showed every item whole.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Explore: a dark y axis with "pdf" above it and numbers 0.02 ... 0.08 beside its ticks.
- [ ] Explore, S up to 1,000 (it stops there): the axis reads "pdf (×0.0001)" over 2, 4, 6, 8; x0 up: it stops at the plot's right edge.
- [ ] Family at S = 1,000: the x labels 0, 1,000, 3,000, 5,000 apart, none run together.
- [ ] Fit my data, a preset, then the Survival page: "survival P(X > x) (log)" above the axis, its powers of ten beside it.
- [ ] Every menu item whole inside its box (main menu, Fit, Fit engine).
