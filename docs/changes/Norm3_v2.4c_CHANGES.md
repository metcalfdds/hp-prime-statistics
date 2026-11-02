# Norm3 v2.4c: changes

*1 November 2026. Edited from v2.4b by hand. 1,013 lines. The `!=` the Virtual Calculator showed to be a factorial, and fixes for numbers Norm3 cannot draw (the book's vetting point 6, "bulletproof under careless and random use").*

## What was found

The monkey test's first pass found nothing in Norm3 (three starts, 400 runs each: 400, 400, 400 OK). Three things came from elsewhere:

1. **`!=` is a factorial and a test on the Prime.** Typed in Home on the Virtual Calculator, `{3!=0, 0!=0, 3<>0, 0<>0}` gave `{0, 0, 1, 0}`, and `999!=0` stopped with "Numerical overflow" (1 Nov 2026). The harness reads `!=` as "not equal", so only a static check can see it. Norm3 v2.4b had one, in `n3_fmtp` (255): "IF pv != 0 AND ABS(pv) < thr" never held on the calculator, so a tiny pdf or area printed in the Prime's scientific form instead of "< 0.0001". BayesTree beta 8e had the same line and ended with "Numerical overflow" at 0.999.
2. **Numbers Norm3 cannot draw.** Norm3 is called from Home with three numbers, so a careless call can hand it anything. In v2.4b: a list for μ, σ or x₀ went on into the arithmetic; σ = 1E300 or 10¹² stopped with STRING's "Invalid input" (the density labels would need 301 or 13 decimals; the Prime takes at most 12); μ = 1E40 with σ = 1 divided by zero; and μ = 10⁹ with σ = 0.001 drew in the harness, but its tick loop, run in 12-digit decimals, is stuck (SampDist v2.3d's same loop never ended on the Virtual Calculator).
3. **The σ keys** could take σ past those limits: σ+ from 10¹⁰ stopped with "Invalid input", and σ− at μ = 10⁹ went down to 0.1153.

## What changed (line numbers are v2.4b's)

1. **`<>`, not `!=`** (`n3_fmtp`, 255).
2. **Numbers Norm3 cannot draw are refused with a sentence, before anything is drawn** (415), on the line NormExplorer beta 42d, CICatcher beta 2e and SampDist v2.3e draw:
   - a list or other non-number: "Norm3 takes three numbers: Norm3(μ, σ, x₀)";
   - 50 digits or more: "A number you typed has more than 50 digits: too large to work with.";
   - σ above 10¹⁰: "σ can be at most 1E10: a larger σ needs density labels with more decimals than the calculator prints.";
   - σ below 0.000000001 or below |μ|/100,000,000: "σ is too small next to μ for the calculator's 12 digits. Use a larger σ or a μ nearer 0."
3. **The σ keys stay inside the same limits** (908): σ− stops at 0.0001 or at |μ|/100,000,000, whichever is larger, and never raises a smaller σ typed at the start (v2.4b's MAX(0.0001, σ/1.25) did); σ+ stops at 10¹⁰.
4. **An x label that would touch the one before it, the "x" caption or the right edge is left out** (643–644); its tick stays. At a large μ or a small σ the labels are long ("1000000010").
5. **"0 = re-centre" is shown only where the title leaves room for it** (761–769): at a large μ the title ran into it.
6. The banner, the firmware lines and the help page's title say v2.4c.

Nothing else changed.

## Verification

`verify_Norm3_v2.4c.py`, output `verify_Norm3_v2.4c_output.txt`: **23 PASS, 0 FAIL**, run from a repository layout, with v2.4b read from git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** 9 calls × 2 key sets (every key: μ, σ, x₀, re-centre; taps and the menu), 392 screens: every text and the summary identical to v2.4b's but for x labels left out, and those are exactly the ones that would touch the "x" caption or the label drawn before them (v2.4b printed them overlapping).
- **M** the refusals (nine cases, and μ = 10⁹ with σ = 0.001, whose v2.4b tick loop is run in 12-digit decimals); the ends of what is accepted draw with every key and no error; the σ keys at 10¹⁰, at μ = 10⁹, from a typed 0.00001, and at ordinary values (unchanged); every new sentence within 4 lines of 32 characters.
- **G** only `Norm3`, `n3_fmtp` and `n3_Help` differ; no `!=` (v2.4b had one); no new glyph in the code.
- **D** text_overlap_v1 over every v2.4c screen drawn: no firm overlap, straddle or overrun, the ends of what is accepted included (v2.4b on its own runs: 59).

**The monkey test again** (1,002 runs, 150 events each, 334 from each of three starts: `Norm3(0,1,1.96)`, `Norm3(100,15,130)`, `Norm3(0.5,0.0002,0.5003)`): v2.4c **1,002 OK**.

## Gate

`ppl_gate_v1d.py Norm3_v2.4c.txt Norm3_v2.4b.txt`: **RESULT: PASS**.

## The Virtual Calculator

On the Virtual Calculator (2.4.2, build 2026-09-09, Rogers-HP; Claude through computer use, 1 Nov 2026, night). Check: "No errors in the program". Called from Home with pasted arguments:

- `Norm3(0, 1ᴇ12, 0)` returned "σ can be at most 1E10: a larger σ needs density labels …"; `Norm3(1ᴇ40, 1, 1ᴇ40)` returned "σ is too small next to μ for the calculator's 12 digits …". Nothing was drawn, and nothing stopped.
- `Norm3(1ᴇ9, 10, 1ᴇ9)`, the narrowest σ accepted at μ = 10⁹, drew at once: x labels thinned (999999970, 999999990, 1000000010, 1000000030), pdf 0.0399, both areas 0.5000; σ− left σ at 10.
- `Norm3(0, 1ᴇ10, 0)` and `Norm3(0, 1ᴇ−9, 0)` drew without an error, **but their density labels ran over the axis** ("0.00000000005", "500000000"), and so did the labels at everyday values: "0.0005" at σ = 1000, and five characters or more at any σ above about 50. The PC overlap check compares text with text, so a label over a line passed it. **v2.4d** writes those labels in units of a power of ten (`Norm3_v2.4d_CHANGES.md`); v2.4c was never committed.
