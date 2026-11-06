# AgreeLab beta 1f: changes (5 November 2026)

Round 9 of 5 November 2026. Made from beta 1e by `round9/make_round9.py` (exact replacements; a miss stops the build).

## What changed

1. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "AgreeLab help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - AgreeLab help 1/9: Agreement beyond chance
   - AgreeLab help 2/9: SE, CI and the test
   - AgreeLab help 3/9: Kappa max and the paradox
   - AgreeLab help 4/9: Weighted kappa
   - AgreeLab help 5/9: Many raters, Fleiss' kappa
   - AgreeLab help 6/9: Which ICC?
   - AgreeLab help 7/9: Bland-Altman
   - AgreeLab help 8/9: Benchmarks are conventions
   - AgreeLab help 9/9: Agreement and forensic work

2. American spelling in what the screen shows: grey->gray x2.
3. The name is "Roger D. Metcalf", with the full stop (Roger, 5 Nov 2026).

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round9/gate_AgreeLab_beta1f.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- The monkey test was not run again: beyond its strings, beta 1f's code is beta 1e's, which passed its 1,000 runs (round 8 or before).

Not yet run on a G1 or a G2.
