# GaltonBoard beta 3h: changes (5 November 2026)

Round 9 of 5 November 2026. Made from beta 3g by `round9/make_round9.py` (exact replacements; a miss stops the build).

## What changed

1. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "GaltonBoard help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - GaltonBoard help 1/3: Reading the Galton board
   - GaltonBoard help 2/3: Keys and touch
   - GaltonBoard help 3/3: Exact answers (CAS)

2. American spelling in what the screen shows: grey->gray x1, colours->colors x1, Colour->Color x1.

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round9/gate_GaltonBoard_beta3h.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- The monkey test was not run again: beyond its strings, beta 3h's code is beta 3g's, which passed its 1,000 runs (round 8 or before).

Not yet run on a G1 or a G2.
