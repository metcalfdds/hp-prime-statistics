# EpiStats v1.7j: changes (5 November 2026)

Rounds 9 and 10 of 5 November 2026, shipped together. Round 9 made v1.7i from v1.7h (`round9/make_round9.py`); it never shipped alone. Round 10 made v1.7j from it (`round10/make_round10.py`). Both builds are exact replacements; a miss stops them.

## What changed

1. **Reasonable limits on what a student types** (round 10; Roger: "cap everything at reasonable values"). A count at most 100,000 (was 9,999,999); person-time from 0.001 to 100,000 (was 1E-6 to 1E15); the sample-size forms: sigma and E above 0 and at most 1,000, the difference in means from -10,000 to 10,000, a proportion's E between 0 and 1. A value outside its range is refused with a sentence that gives the range, and nothing changes; the form's hint line gives the range first. The calculator handles far larger numbers, and the tests type values up to 1E100: the limits are for speed and sense.
2. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "EpiStats help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - EpiStats help 1/15: About EpiStats
   - EpiStats help 2/15: 2×2 table guide
   - EpiStats help 3/15: Sensitivity, specificity
   - EpiStats help 4/15: Risk and odds ratios
   - EpiStats help 5/15: Confidence intervals
   - EpiStats help 6/15: Mantel-Haenszel
   - EpiStats help 7/15: Kappa
   - EpiStats help 8/15: Variable reference
   - EpiStats help 9/15: Entry grid, soft keys
   - EpiStats help 10/15: Result pages and taps
   - EpiStats help 11/15: PPV vs prevalence, ROC
   - EpiStats help 12/15: Readings, Fisher bars
   - EpiStats help 13/15: Forest, risk bars, NNT
   - EpiStats help 14/15: Exact CIs, exact OR
   - EpiStats help 15/15: Where the SE comes from

3. The help titles are in font 2, like the rest of the fleet.
4. American spelling in what the screen shows: grey->gray x3, Grey->Gray x2.
5. The name is "Roger D. Metcalf", with the full stop (Roger, 5 Nov 2026).

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round10/gate_EpiStats_v1.7j.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- `tools/caps_probe_v1.py`, 40 runs, before and after round 10 (`docs/dev/caps-2026-11-05.md`).
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on v1.7j: 1000 runs, 120 events each, 588 s; OK 1000.

Not yet run on a G1 or a G2.
