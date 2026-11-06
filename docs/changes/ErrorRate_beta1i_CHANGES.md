# ErrorRate beta 1i: changes (5 November 2026)

Round 9 of 5 November 2026. Made from beta 1h by `round9/make_round9.py` (exact replacements; a miss stops the build).

## What changed

1. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "ErrorRate help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - ErrorRate help 1/9: Zero errors, not zero rate
   - ErrorRate help 2/9: Reading the main plot
   - ErrorRate help 3/9: The rule of three
   - ErrorRate help 4/9: Confidence or credibility?
   - ErrorRate help 5/9: Absence of evidence
   - ErrorRate help 6/9: Database trawls
   - ErrorRate help 7/9: Honest caveats
   - ErrorRate help 8/9: Keys and touch
   - ErrorRate help 9/9: Three engines

2. A help title gets the full 296 px (220 only beside a badge).
3. American spelling in what the screen shows: programmes->programs x3.

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round9/gate_ErrorRate_beta1i.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on beta 1i: 1000 runs, 120 events each, 1297 s; OK 1000.

Not yet run on a G1 or a G2.
