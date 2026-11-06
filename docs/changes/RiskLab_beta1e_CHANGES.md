# RiskLab beta 1e: changes (5 November 2026)

Round 9 of 5 November 2026. Made from beta 1d by `round9/make_round9.py` (exact replacements; a miss stops the build).

## What changed

1. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "RiskLab help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - RiskLab help 1/8: Logistic regression
   - RiskLab help 2/8: Separation, collinearity
   - RiskLab help 3/8: The ROC curve and the AUC
   - RiskLab help 4/8: Cut-offs and trade-offs
   - RiskLab help 5/8: Calibration, H-L test
   - RiskLab help 6/8: Fairness definitions
   - RiskLab help 7/8: The data
   - RiskLab help 8/8: Keys, your data, Home

2. American spelling in what the screen shows: Grey->Gray x1, labelled->labeled x1.
3. The name is "Roger D. Metcalf", with the full stop (Roger, 5 Nov 2026).

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round9/gate_RiskLab_beta1e.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- The monkey test was not run again: beyond its strings, beta 1e's code is beta 1d's, which passed its 1,000 runs (round 8 or before).

Not yet run on a G1 or a G2.
