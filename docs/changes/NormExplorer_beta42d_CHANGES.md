# NormExplorer beta 42d: changes

*1 November 2026. Edited from beta 42c by a patch script, every replacement checked to apply exactly once. 4,104 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use"), and for two numerical faults found while checking those fixes at the large and small ends.*

## What the monkey test found

`tools/monkey_v1b.py` drives the program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms, random Statistics lists in D1 and D2 (`docs/dev/monkey-fleet-2026-11-01.md`). Over 400 runs (150 events each) beta 42c gave:

| Verdict | Runs | Cause |
| --- | --- | --- |
| OK | 353 | |
| HARNESS | 30 | a list typed into a number field went on into the arithmetic (`<=`, `+`, `*`, `-`, `<` between a list and a number) |
| STALL | 9 | the Diagnostics page read keys only, and a tap there did nothing |
| CRASH | 5 | `STRING(x, 2, 13)`: at σ = 1.23 × 10¹² (and 10¹²) the density labels need 13 decimals, which the Prime refuses ("Invalid input") |
| CRASH | 3 | division by zero: μ = ±1E300 (typed in menu 1, or solved from z = −1E300), so μ ± 4σ was μ and the window had no width |

Writing z-scores of D1 into D2 (menu 6) is the program's purpose there, announced on screen, so it does not count (`--writes D`).

## What changed (line numbers are beta 42c's)

1. **Every form field takes a real number only**: all 15 forms, 26 fields, are `{name,[0]}` (1607, 1675, 1755, 1799, 1864, 1891, 1921, 1947, 1974, 2081, 2104, 2124, 2144, 2198, 2208). On the Virtual Calculator such a field refuses `{1,2}` with "Invalid input" and keeps its value (TTestLab, 1 Nov 2026).
2. **What 12 digits cannot draw is refused with a sentence, before anything changes** (new `ne_BigMsg`, `ne_BadDist`, `ne_SgMin`, after `ne_Btw`), on the lines Norm3 v2.4c, CICatcher beta 2e and SampDist v2.3e draw:
   - a number of 50 digits or more: "A number you typed has more than 50 digits: too large to work with.";
   - σ above 10¹⁰: "σ can be at most 1E10: a larger σ needs density labels with more decimals than the calculator prints.";
   - σ below 0.000000001 or below |μ|/100,000,000: "σ is too small next to μ for the calculator's 12 digits. Use a larger σ or a μ nearer 0." (SampDist v2.3d's tick loop never ended there on the Virtual Calculator.)
   - Where: menu 1 (1610); the Z-formula solver (2084–2157: the three typed numbers, then the μ and σ the solve would give the session, then the value solved for: "These values give z beyond 1E50: too large to work with.", and x, σ the same); the bounds of menu 3 (1756, 1800); μ₂ (2199: a far μ₂ only widens the window, so it needs no other limit); the custom window (1677: "This window is too narrow for the calculator's 12 digits. Make it wider."); and every data route (`ne_BinData`, `ne_TwoGroups`, `ne_ResidLoad`, `ne_ZtoD2`: a value of 50 digits or more, then the fitted mean and s, in sentences that speak of the data: "… Subtract one number from every value.").
3. **The Explorer stays inside those lines.** The σ keys and the σ drag stop at 10¹⁰ and at `ne_SgMin`; the μ drag and keys keep |μ| within 100,000,000 σ, so leaving the Explorer never gives a window too narrow to draw (a shading bound at 1E40 widened the frozen window, μ could be dragged out to 9.6E39, and with the shading off the auto window then divided by zero). Its steps are rounded to the step's own decimals (new `ne_Snap`), not to 6 (1426–1498): σ ↑ from 1E−8 rounded the new σ to 0.
4. **Diagnostics takes a tap** (2748–2750): it waits with `ne_WaitAny`, like every other page; its footer says "Any key or tap: back to the menu".
5. **x labels that would overlap are left out** (3225–3236); the tick stays. At σ = 10¹⁰ the labels are 12 characters wide and 34 px apart, and were printed over each other. At the usual windows every label is drawn, as before.
6. **s from deviations, and the samples' sums of z.** The Prime keeps 12 digits, and s = √((Σx² − n x̄²)/(n − 1)) subtracts two nearly equal numbers. `ne_BinData`, `ne_TwoGroups` and `ne_ZtoD2` now take s from the deviations x − x̄ in a second pass. The samplers (`ne_SampBins` and the MicroPython `SAMPBINSPY`) now add up the standard normal z behind each value drawn, and `ne_Histo` turns those sums into x̄ = μ + σ z̄ and s = σ s_z. Even with the harness's 16 digits, beta 42c read D1 = 100,000,001 … 100,000,010 (s = 3.03) as s = 2.98, two groups near 100,000,000 as pooled σ 1.41 and d = 1.56 (1.76 and 1.25), and a sample from N(10⁹, 10) as s = 0.00; the Python sampler's `"%.6f"` would print the sum of squares of a sample with σ = 0.0001 as 0.000002. At N(0, 1) every number is as before.
7. Header: the beta 42d block; the map; forward declarations for the four new helpers.

Not changed: at the far ends of what is accepted (|μ| or σ near 10¹⁰, σ near 10⁻⁹) a few readouts (the 68–95–99.7 block, the solver's last line, the Diagnostics session line) are long enough to run past the right edge.

## Verification

`verify_NormExplorer_beta42d.py`, output `verify_NormExplorer_beta42d_output.txt`: **48 PASS, 0 FAIL**, run from a repository layout, with beta 42c read from git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** six sessions over every menu item (the Explorer with every key, soft key and drags; 4 areas, 5 quantiles, 4 solves, compare and power, simulate, D1, C1/C2, residuals, z-scores, every window item, the animation, Help, reset): 152 screens, every text, box, menu title and result identical to beta 42c's. The Diagnostics page differs only in its footer.
- **M** one check per finding, each also run on beta 42c, where it fails: the typed fields; 26 refusals with the session unchanged and drawing going on; the lines themselves; the Explorer's σ keys at 10¹⁰, at μ = 10⁹ with Centre, at 1E−8 and 1E−9, and the μ drag at a bound of 1E40; Diagnostics and a tap; the ends of what is accepted through every menu item; the three numerical faults of (6); every new box within 4 lines of 32 characters.
- **G** only the 20 routines named differ; no `!=`; no new glyph in the code; the MicroPython sampler differs only in its four sum lines.
- **D** text_overlap_v1 over the same runs on both versions: nothing new; no x labels over each other (beta 42c: 74 kinds).

**The monkey test again** (1,000 runs, 150 events each, `--lists --writes D`): beta 42d **1,000 OK**.

## Gate

`ppl_gate_v1d.py NormExplorer_beta42d.txt NormExplorer_beta42c.txt`: **RESULT: PASS**. Kit lint 0 errors; ppl_check 5 E5, 6 W3, as beta 42c; lint_ppl's problems are beta 42c's (drawing to G0, the INPUTs whose `== 0` sits on a later line, and the file-name entry point).

## The Virtual Calculator

On the Virtual Calculator (2.4.2, build 2026-09-09, Rogers-HP; Claude through computer use, 1 Nov 2026, night). Check: "No errors in the program". The program runs from Home as `NormExp` (its entry point); `NormExplorer` is "Syntax Error" there.

- Menu 1, **σ = 1.23E12**: the box "σ can be at most 1E10: …", and the menu with N(0, 1) unchanged (beta 42c stopped with "Invalid input" here).
- Menu 1, **μ = 1E9 with σ = 1**: "σ is too small next to μ for the calculator's 12 digits. …"; with σ = 10 accepted.
- Data & histogram → Simulate a sample, **n = 1000 from N(10⁹, 10)**: x̄ = 1000000000.12, **s = 10.28** (beta 42c, in the harness: s = 0.00).
- **At σ = 10,000 the Explorer's density labels "0.00006" … ran over the axis** and into the μ box; any σ above about 2000 gives labels of seven characters. **Beta 42e** writes them in the scientific form (`NormExplorer_beta42e_CHANGES.md`); beta 42d was never committed.
- Not tried there: the Diagnostics page's tap (harness only).
