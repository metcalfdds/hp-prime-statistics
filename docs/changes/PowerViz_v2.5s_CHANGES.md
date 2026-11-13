# PowerViz v2.5s: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in PowerViz v2.5r (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 3/7: the three drags are three lines again (Round 11's re-wrap had run them into one sentence), and "the nearest of those values", which had nothing before it to point to, is "the nearest of the seven α values (0.001 to 0.2)", the values page 4 steps through.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of PowerViz v2.5s that differ from PowerViz v2.5r: line 4 (comment); lines 35-39 (comment); lines 3749-3755 (code). Routines whose code changed, with the number of lines: pv_ShowHelp 7.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 3, before (v2.5r)

```text
PowerViz help 3/7: Touch
DRAG ON THE PLOT:
sideways near H₁ = move the alternative the dashed red line = set
α by hand; when you lift your finger, α jumps to the nearest of
those values if it is within 15 % of it up or down = change n (one
step for every 12 pixels)
TAP THE READOUT:
n = type n;  μ, p, d or h = type the effect
any key or tap = next page
```

### Screen 3, after (v2.5s)

```text
PowerViz help 3/7: Touch
DRAG ON THE PLOT:
sideways near H₁ = move the alternative
the dashed red line = set α by hand; when you lift your
  finger, α jumps to the nearest of the seven α values
  (0.001 to 0.2) if it is within 15 % of it
up or down = change n (one step for every 12 pixels)
TAP THE READOUT:
n = type n;  μ, p, d or h = type the effect
any key or tap = next page
```

## Checks

- `tools/ppl_gate_v1e.py` against PowerViz v2.5r: PASS. lint_ppl 12 problems, as in PowerViz v2.5r; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 7 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 125/165 collisions 21 (firm 18) straddles 0 overruns 9 ghosts 0.
- The monkey (`tools/monkey_chunks_v1.py`, base 12, with `--lists`): 1000 of 1000 runs OK.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help page 3/7: five lines under DRAG ON THE PLOT, and TAP THE READOUT below them.
