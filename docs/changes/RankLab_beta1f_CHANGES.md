# RankLab beta 1f: changes (5 November 2026)

Rounds 9 and 10 of 5 November 2026, shipped together. Round 9 made beta 1e from beta 1d (`round9/make_round9.py`); it never shipped alone. Round 10 made beta 1f from it (`round10/make_round10.py`). Both builds are exact replacements; a miss stops them.

## What changed

1. **Reasonable limits on what a student types** (round 10; Roger: "cap everything at reasonable values"). The one-sample m0 from -10,000 to 10,000 (was up to 1E50). A value outside its range is refused with a sentence that gives the range, and nothing changes; the form's hint line gives the range first. The calculator handles far larger numbers, and the tests type values up to 1E100: the limits are for speed and sense.
2. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "RankLab help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - RankLab help 1/7: What it does
   - RankLab help 2/7: Keys and touch
   - RankLab help 3/7: Sign test, signed-rank
   - RankLab help 4/7: Mann-Whitney, Kruskal-Wallis
   - RankLab help 5/7: Friedman, W, correlation
   - RankLab help 6/7: Exact or normal; the p-value
   - RankLab help 7/7: Data, Home, credits

3. American spelling in what the screen shows: colours->colors x1.
4. The name is "Roger D. Metcalf", with the full stop (Roger, 5 Nov 2026).

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round10/gate_RankLab_beta1f.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- `tools/caps_probe_v1.py`, 40 runs, before and after round 10 (`docs/dev/caps-2026-11-05.md`).
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on beta 1f: 1000 runs, 120 events each, 1335 s; OK 1000.

Not yet run on a G1 or a G2.
