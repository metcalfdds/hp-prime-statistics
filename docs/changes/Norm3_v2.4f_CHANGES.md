# Norm3 v2.4f: changes (5 November 2026)

Round 9 of 5 November 2026. Made from v2.4e by `round9/make_round9.py` (exact replacements; a miss stops the build).

## What changed

1. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "Norm3 help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - Norm3 help: Touch and keys

2. American spelling in what the screen shows: re-centre->re-center x2, Re-centre->Re-center x1.
3. The name is "Roger D. Metcalf", with the full stop (Roger, 5 Nov 2026).

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round9/gate_Norm3_v2.4f.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- The monkey test was not run again: beyond its strings, v2.4f's code is v2.4e's, which passed its 1,000 runs (round 8 or before).

Not yet run on a G1 or a G2.
