# BurrLab beta 1h (29 Oct 2026)

Two changes from beta 1f (beta 1g, the first of them alone, was never filed):

1. **The curves are drawn by PPL again in Auto.** On the G1 and the G2, beta 1e/1f's Python curve bridge made an Explore key press take 3-4 s (Roger, 28 Oct 2026), against under 1 s for beta 1d's PPL cache (G1: c 757 d 137 w 4 ms; G2: c 868 d 117 w 2 ms). The arithmetic is faster in Python, but the ~480 values handed back through hpprime one at a time cost more than it saves. Auto and PPL only now draw the Explore, Family and Rare curves by PPL (the readout says ", PPL"); Python draws them only in "Python only" and "Both", kept for the comparison demo. **The fit still uses Python first** (Auto), where one call returns a handful of numbers. Change: `bu_Cache` (one condition, `buEng == 3 OR buEng == 4`, and Auto's label).
2. **Text only:** four messages no longer say "see the Terminal" (the Terminal cannot be opened by a key and beta 1f prints nothing); they point to `BU_PZ` in Home.

Checks: gate PASS against beta 1f; case_scan clean; `verify_BurrLab_beta1h.py` (beta 1f's script, with the curve-bridge tests run in "Python only", a new check that Auto makes no PYTHON() call on the Explore/Family path, and the readout and message texts updated): 3,466 checks, 0 failures.

Device checklist: on the G1 and G2, Explore → Up/Down should feel like beta 1d (under a second; More → Timing shows "c … d … w … ms, PPL"). Fit → BJS with Engine at Auto: the badge should name MicroPython. Engine → Both on Explore: the readout compares the two engines. Nothing should hang; if anything does, note the screen and the last key.
