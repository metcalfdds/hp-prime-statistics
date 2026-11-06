# AnovaLab beta 1e: changes (5 November 2026)

Rounds 9 and 10 of 5 November 2026, shipped together. Round 9 made beta 1d from beta 1c (`round9/make_round9.py`); it never shipped alone. Round 10 made beta 1e from it (`round10/make_round10.py`). Both builds are exact replacements; a miss stops them.

## What changed

1. **Reasonable limits on what a student types** (round 10; Roger: "cap everything at reasonable values"). The one- and two-sigma forms: s and sigma0 from 0.000001 to 1,000 (were 1E-50 to 1E50), n 2 to 10,000 (were to 1,000,000). A value outside its range is refused with a sentence that gives the range, and nothing changes; the form's hint line gives the range first. The calculator handles far larger numbers, and the tests type values up to 1E100: the limits are for speed and sense.
2. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "AnovaLab help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - AnovaLab help 1/8: What one-way ANOVA asks
   - AnovaLab help 2/8: Welch and the checks
   - AnovaLab help 3/8: Which pairs differ?
   - AnovaLab help 4/8: Two-way ANOVA
   - AnovaLab help 5/8: Randomized blocks
   - AnovaLab help 6/8: One and two variances
   - AnovaLab help 7/8: Your data, and Home
   - AnovaLab help 8/8: Credits

3. American spelling in what the screen shows: grey->gray x3.
4. The name is "Roger D. Metcalf", with the full stop (Roger, 5 Nov 2026).

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round10/gate_AnovaLab_beta1e.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- `tools/caps_probe_v1.py`, 40 runs, before and after round 10 (`docs/dev/caps-2026-11-05.md`).
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on beta 1e: 1000 runs, 120 events each, 467 s; OK 1000.

Not yet run on a G1 or a G2.
