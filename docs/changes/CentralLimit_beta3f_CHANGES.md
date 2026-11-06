# CentralLimit beta 3f: changes (5 November 2026)

Round 9 of 5 November 2026. Made from beta 3e by `round9/make_round9.py` (exact replacements; a miss stops the build).

## What changed

1. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "CentralLimit help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - CentralLimit help 1/3: Reading the dashboard
   - CentralLimit help 2/3: Buttons, taps and keys
   - CentralLimit help 3/3: The exact curve and the MGF

2. American spelling in what the screen shows: Centre->Center x3, centred->centered x1, colours->colors x1.

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round9/gate_CentralLimit_beta3f.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: installed as an app (CentralLimit.hpappdir); Check on "CentralLimit (App)" said "No errors in the program" (round 9; round 10 did not change it).
- The monkey test: CentralLimit is an app, out of the PC harness's reach.

Not yet run on a G1 or a G2.
