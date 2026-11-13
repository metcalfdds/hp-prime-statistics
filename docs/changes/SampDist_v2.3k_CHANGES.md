# SampDist v2.3k: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in SampDist v2.3j (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help pages 1/2 and 2/2 are lists again: Round 11's re-wrap had put "Watch sample means", "Soft keys", "Touch" and "Compare sample sizes" on one line with their first item, and run the soft keys together.  Each label is on a line of its own, in blue, with its items indented below it in black, as page 1's other three items are; Menu says what it does.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of SampDist v2.3k that differ from SampDist v2.3j: lines 35-39 (comment); lines 1852-1854 (code); lines 1867-1877 (code). Routines whose code changed, with the number of lines: sd_showHelp 14.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 1, before (v2.3j)

```text
SampDist help 1/2: The sampling distribution
The sample mean  of n draws from a Normal(μ, σ) population is
itself Normal, centered on μ with standard error
σ = σ / √n.
Find probability
   Choose left, right, between or outside, then enter the bounds.
Find critical value
   Enter α; get the  cutting off that tail.
Compare sample sizes
   Three curves on the same axes: four times the n gives half the
   standard error.
Watch sample means 40 simulated means fall onto the axis, then
   become a histogram under the curve.
Results are kept in Home as EP_SD_ names.
any key or tap = next
```

### Screen 1, after (v2.3k)

```text
SampDist help 1/2: The sampling distribution
The sample mean  of n draws from a Normal(μ, σ) population is
itself Normal, centered on μ with standard error
σ = σ / √n.
Find probability
   Choose left, right, between or outside, then enter the bounds.
Find critical value
   Enter α; get the  cutting off that tail.
Compare sample sizes
   Three curves on the same axes: four times the n gives half the
   standard error.
Watch sample means
   40 simulated means fall onto the axis, then become a
   histogram under the curve.
Results are kept in Home as EP_SD_ names.
any key or tap = next
```

### Screen 2, before (v2.3j)

```text
SampDist help 2/2: The result graph
   gray = the population N(μ, σ); blue = , on ONE scale: at n = 30
   the population curve's peak is only 18% as high as the
    curve's.
Soft keys n− n+  step n through 1, 2, 4 ... 400 n×4  quadruples n:
   σ halves μ,σ  edit;  Tail  the next kind of region (left, right,
   between, outside);  Menu
Touch drag in the plot: the nearer bound moves ⇆ nudge it, ⇅
   the other bound, +/- = n, Ent = more, Esc = menu
Compare sample sizes drag = a cursor with P( < x) for each n;
   tap a curve to pick it.
Critical values: changing n moves them; α stays the same.
any key or tap = menu
```

### Screen 2, after (v2.3k)

```text
SampDist help 2/2: The result graph
   gray = the population N(μ, σ); blue = , on ONE scale: at n = 30
   the population curve's peak is only 18% as high as the
    curve's.
Soft keys
   n− n+  step n through 1, 2, 4 ... 400
   n×4  quadruples n: σ halves
   μ,σ  edit;  Tail  the next kind of region (left, right,
   between, outside);  Menu  back to the menu
Touch
   drag in the plot: the nearer bound moves
   ⇆ nudge it, ⇅ the other bound, +/- = n, Ent = more, Esc = menu
Compare sample sizes
   drag = a cursor with P( < x) for each n; tap a curve to pick it.
Critical values: changing n moves them; α stays the same.
any key or tap = menu
```

## Checks

- `tools/ppl_gate_v1e.py` against SampDist v2.3j: PASS. lint_ppl 18 problems, as in SampDist v2.3j; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 2 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: new: screens 348/2935 collisions 27 (firm 25) straddles 16 overruns 16 ghosts 0 | old: screens 348/2935 collisions 23 (firm 21) straddles 18 overruns 18 ghosts 0.
- The monkey (`tools/monkey_chunks_v1.py`, base 12, with `--lists`): 1000 of 1000 runs OK.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help pages 1/2 and 2/2: each label alone on its line in blue, its items indented in black; nothing reaches the footer.
