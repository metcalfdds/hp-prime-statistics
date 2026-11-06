# ExhibitLab beta 1f: changes (5 November 2026)

Rounds 9 and 10 of 5 November 2026, shipped together. Round 9 made beta 1e from beta 1d (`round9/make_round9.py`); it never shipped alone. Round 10 made beta 1f from it (`round10/make_round10.py`). Both builds are exact replacements; a miss stops them.

## What changed

1. **Reasonable limits on what a student types** (round 10; Roger: "cap everything at reasonable values"). c (0.5 to 0.9999), the claim (0.001 to 0.999), the negatives allowed (0 to 20) and the prior's a and b (0.1 to 100) are now refused outside their ranges; before, each was moved to the nearest end with a sentence.  The weights: mean above 0 and at most 10,000 g, SD 0 to 1,000 g. A value outside its range is refused with a sentence that gives the range, and nothing changes; the form's hint line gives the range first. The calculator handles far larger numbers, and the tests type values up to 1E100: the limits are for speed and sense.
2. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "ExhibitLab help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - ExhibitLab help 1/8: What the claim means
   - ExhibitLab help 2/8: Frequentist or Bayesian?
   - ExhibitLab help 3/8: Why N hardly matters
   - ExhibitLab help 4/8: Random selection
   - ExhibitLab help 5/8: The total weight
   - ExhibitLab help 6/8: Checking against ENFSI
   - ExhibitLab help 7/8: Keys and Home
   - ExhibitLab help 8/8: Sources

3. American spelling in what the screen shows: analysed->analyzed x2, grey->gray x1.
4. The name is "Roger D. Metcalf", with the full stop (Roger, 5 Nov 2026).

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round10/gate_ExhibitLab_beta1f.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- `tools/caps_probe_v1.py`, 40 runs, before and after round 10 (`docs/dev/caps-2026-11-05.md`).
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on beta 1f: 1000 runs, 120 events each, 1029 s; OK 1000.

Not yet run on a G1 or a G2.
