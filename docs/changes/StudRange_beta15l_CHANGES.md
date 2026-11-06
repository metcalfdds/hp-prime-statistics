# StudRange beta 15l: changes (5 November 2026)

Rounds 9 and 10 of 5 November 2026, shipped together. Round 9 made beta 15k from beta 15j (`round9/make_round9.py`); it never shipped alone. Round 10 made beta 15l from it (`round10/make_round10.py`). Both builds are exact replacements; a miss stops them.

## What changed

1. **Reasonable limits on what a student types** (round 10; Roger: "cap everything at reasonable values"). df from 1 to 1,000 or 0 for infinity (was 100,000); an observed q from 0 to 100; the MSE at most 1,000,000 (an SD of 1,000, squared); a group mean from -10,000 to 10,000. A value outside its range is refused with a sentence that gives the range, and nothing changes; the form's hint line gives the range first. The calculator handles far larger numbers, and the tests type values up to 1E100: the limits are for speed and sense.
2. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "StudRange help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - StudRange help 1/4: About StudRange
   - StudRange help 2/4: Why q and not t
   - StudRange help 3/4: Two engines
   - StudRange help 4/4: The plot


## Checks

- `tools/ppl_gate_v1d.py`: pass (`round10/gate_StudRange_beta15l.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- `tools/caps_probe_v1.py`, 40 runs, before and after round 10 (`docs/dev/caps-2026-11-05.md`).
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on beta 15l: 1000 runs, 120 events each, 5131 s; OK 1000.

Not yet run on a G1 or a G2.
