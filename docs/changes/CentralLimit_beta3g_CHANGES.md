# CentralLimit beta 3g: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes CentralLimit beta 3g from CentralLimit beta 3f. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 and 2 reworded: what a bar counts, why the axis is shared, the sigma/SD ratio, "the pile" and the n keys in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 3 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, cltHelp 22.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 3 screens changed; 1 kept their words.

### Before (beta 3f)

```text
CentralLimit help 1/3: Reading the dashboard
Top (blue): the population, every member.
Black line: the shape it was drawn from.
Bottom: one bar-count per sample mean x̄.
Bar colors: how far from μ, in standard
  errors (SE = σ/√n): green within 1 SE,
  orange within 2, red beyond (68-95 rule).
Both panels share ONE x-axis: means bunch up.
Green dots: the population mean μ.
Blue curve: the normal shape the CLT predicts.
σ/SD: how many times narrower the means are;
  close to √n, so every n offered is a square.
Samples are drawn WITH replacement, where
  SD(mean) = σ/√n holds exactly.
Start at n = 1 (the means ARE the population),
  then 4, 16: watch the bell form.
Any key or tap: the buttons and gestures
```

```text
CentralLimit help 2/3: Buttons, taps and keys
1 sample (or Up): watch ONE sample. Its n
  members light up red; their mean falls into
  the pile. Any key or tap skips. (Or tap the
  lower-left corner of the top panel.)
+1 (or Down): one more mean, added at once.
n− n+ (or − +): n = 1, 4, 16, 64, 100; draws.
Curve (or 0): the curves on / off.
Menu (or Enter): settings, the CAS pages, Help.
Tap the top panel: a fresh set of samples.
Drag along the top panel to pick n: the curve
  moves first, lift to draw. Left/Right: n step.
Hold a blue bar, or tap a bottom bar, for its
  range, count and share of the total.
n = 100 is item (A); big n draws fewer samples.
Esc (or Menu, Leave) leaves the dashboard.
Any key or tap: the exact curve and the MGF
```

### After (beta 3g)

```text
CentralLimit help 1/3: Reading the dashboard
Top (blue): the population, every member.
Black line: the shape it was drawn from.
Bottom: a histogram of the sample means, x̄.
Bar colors: how far from μ, in standard errors (SE = σ/√n): green
  within 1 SE, orange within 2, red beyond (68-95 rule).
Both panels share ONE x-axis, so you can see the means bunch
up more tightly than the population.
Green dots: the population mean μ.
Blue curve: the normal shape the CLT predicts.
σ/SD: how many times narrower the spread of the means is; it is
  close to √n, which is why every n offered is a square number.
Samples are drawn WITH replacement, where SD(mean) = σ/√n
  holds exactly.
Start at n = 1 (the means ARE the population), then 4, 16: watch
  the bell form.
Any key or tap: the buttons and gestures
```

```text
CentralLimit help 2/3: Buttons, taps and keys
1 sample (or Up): watch ONE sample. Its n members light up red;
  their mean is added to the histogram. Any key or tap skips. (Or
  tap the lower-left corner of the top panel.)
+1 (or Down): one more mean, added at once.
n− n+ (or − +): change n (1, 4, 16, 64, 100) and draw
new samples.
Curve (or 0): the curves on / off.
Menu (or Enter): settings, the CAS pages, Help.
Tap the top panel: a fresh set of samples.
Drag along the top panel to pick n: the curve changes as you
  drag; lift your finger to draw the samples. Left/Right: n step.
Hold a blue bar, or tap a bottom bar, for its range, count and
  share of the total.
In the menu, n = 100 is item (A); a large n draws fewer samples.
Esc (or Menu, Leave) leaves the dashboard.
Any key or tap: the exact curve and the MGF
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 3f; lint_ppl 4 problems, as in beta 3f (4); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 3 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program" (as CentralLimit (App), the app's own program).

Not yet run on a G1 or a G2.
