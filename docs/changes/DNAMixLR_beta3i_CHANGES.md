# DNAMixLR beta 3i: changes (5 November 2026)

Round 9 of 5 November 2026. Made from beta 3h by `round9/make_round9.py` (exact replacements; a miss stops the build).

## What changed

1. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "DNAMixLR help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - DNAMixLR help 1/4: Alleles and hypotheses
   - DNAMixLR help 2/4: Theta (coancestry)
   - DNAMixLR help 3/4: Keys and touch
   - DNAMixLR help 4/4: The LR as a formula

2. American spelling in what the screen shows: grey->gray x1.

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round9/gate_DNAMixLR_beta3i.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on beta 3i: 1000 runs, 120 events each, 192 s; OK 1000.

Not yet run on a G1 or a G2.
