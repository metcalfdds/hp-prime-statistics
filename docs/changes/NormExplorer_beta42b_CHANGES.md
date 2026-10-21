# NormExplorer beta 42b — changes

*20 October 2026. Built on beta 42a. One change, from the first G1 run.*

## What changed

**The standardize animation keeps its pace on a slow calculator** (menu 8, `ne_AnimStd`).

- **Found on the G1** (Roger, 20 Oct 2026): the animation "just takes too long", though it moves smoothly.
- **Why.** Each of its twenty frames drew, then waited 0.3 s. The 0.3 s was tuned on the Virtual Calculator, where a frame draws in a millisecond or two, so the run lasted about 10.8 s there: 20 × 0.3 s plus the two holds of 1.8 s and 3 s. On the G1 the drawing itself takes time, and it came on top of the wait. In the second half every frame also rebuilds the curve, because σ changes.
- **Now.** Each frame is timed with `TICKS` (milliseconds), and the program waits only for what is left of the 0.3 s: nothing at all if the frame took longer. The run lasts about the same on the Virtual Calculator, the G2 and the G1, unless a frame alone takes more than 0.3 s.
- **What it records.** The last run's length and its slowest frame are kept in two file-level variables (`neAnTot`, `neAnMs`; cleared by `ne_ResetAll`). The Diagnostics page shows them on a new line at y = 154: `animation 10.8 s, slowest frame 240 ms`, or `animation: not run yet`. The grey block below moved down 8 px (170, 183, 196) to make room. This line is how the G1's drawing speed will be read off the screen.
- **Unchanged:** the holds (1.8 s, 3 s), the captions, the window, the frames themselves, every other routine, and the `#PYTHON` block (byte-identical).
- The milliseconds are made real (`+ 0.0`) before they are printed, so they never show as a hex integer (Lessons Learned §7).

Version strings swept (rule 13): the two banners, the "tested on" paragraph, the companion-file note and the file map's line count (3758).

## Checks

- **Gate** (`ppl_gate_v1c.py NormExplorer_beta42b.txt NormExplorer_beta42a.txt`, on Rogers-HP): **PASS**. Kit lint 0 errors; ppl_check_v4 tally unchanged (5 E5, 6 W3), no hard errors; lint_ppl 69 reports against 42a's 67, the two new ones being the Diagnostics page's two new `TEXTOUT_P` calls, which draw to the screen like the page's twelve others (the linter's known "not a GROB" report); the full parse stops at `√`, as for 42a (the tool's limit); fleet_names_v2 over 31 files: 0 collisions, 0 untagged.
- **Harness** (`verify_NormExplorer_beta42b.py`, ppl_run_v3e; output beside it): **28 checks, 0 failures.**
  - Fast drawing (the harness clock): 42a lasts 10.80 s and 42b 10.82 s; 42b's twenty frame waits are each 0.299 s; the run and its slowest frame are recorded.
  - Slow drawing (every frame's blit costing D ms):

    | D per frame | 42a | 42b |
    | --- | --- | --- |
    | 100 ms | 13.0 s | 11.0 s |
    | 250 ms | 16.3 s | 11.3 s |
    | 450 ms | 20.7 s | 14.7 s |
    | 800 ms | 28.4 s | 22.4 s |

    A frame slower than 0.3 s gets no wait at all.
  - The Diagnostics line before and after a run, its position, no hex.
  - Only `ne_AnimStd`, `ne_DiagPage` and `ne_ResetAll` differ from 42a; the `#PYTHON` block is byte-identical.
- **Not yet on a calculator.**

## Device checklist (G1 first, then the G2)

1. Load beta 42b as **NormExplorer** (open the existing program in the Kit and replace its text; do not add a second copy).
2. Menu → Standardize animation with N(100, 15). Time it from the first frame to the menu's return. **Expected: about 11 s**, if a frame draws in under 0.3 s. Beta 42a on the G1 was "too long".
3. Menu → Diagnostics. **Expected:** `animation 10.8 s, slowest frame N ms` (N is the G1's drawing time for one frame: please report it). If N is over 300, the frames themselves are the limit; tell Claude and the σ half can draw fewer frames.
4. Repeat 2–3 with N(0, 4) (a σ change only) and N(50, 1) (a shift only). The shift half reuses the cached curve, so its frames should be the fast ones.
5. Diagnostics before any animation, after a fresh launch: `animation: not run yet`, with the grey lines below it not overlapping.
6. Leave the animation and use the Explorer: nothing else should look or behave differently.
