# ChiTable beta 3k: changes (5 November 2026)

Rounds 9 and 10 of 5 November 2026, shipped together. Round 9 made beta 3j from beta 3i (`round9/make_round9.py`); it never shipped alone. Round 10 made beta 3k from it (`round10/make_round10.py`). Both builds are exact replacements; a miss stops them.

## What changed

1. **Reasonable limits on what a student types** (round 10; Roger: "cap everything at reasonable values"). A count at most 100,000 (was 9,999,999), typed or by x10 N. A value outside its range is refused with a sentence that gives the range, and nothing changes; the form's hint line gives the range first. The calculator handles far larger numbers, and the tests type values up to 1E100: the limits are for speed and sense.
2. **One header on every help page** (round 9; Roger, 4 Nov 2026: one style everywhere), "ChiTable help n/N: <Topic>". As the PC harness draws them from the shipped file:

   - ChiTable help 1/5: χ² for a two-way table
   - ChiTable help 2/5: Conventions, plots, Home
   - ChiTable help 3/5: Touch, soft keys and plots
   - ChiTable help 4/5: Why df = (r - 1)(c - 1)
   - ChiTable help 5/5: Exact answers (CAS)

3. D117: page 3 is "Touch, soft keys and plots" ("new" dropped).
4. American spelling in what the screen shows: colour->color x1, grey->gray x3.

## Checks

- `tools/ppl_gate_v1d.py`: pass (`round10/gate_ChiTable_beta3k.txt`).
- The help titles were measured on the Virtual Calculator before round 9 was built (`round9/TitleProbe_v1.txt`): the widest, in font 2, is 272 pixels of the 296 the pages allow.
- `tools/caps_probe_v1.py`, 40 runs, before and after round 10 (`docs/dev/caps-2026-11-05.md`).
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 5 Nov 2026: Check said "No errors in the program", and the checked file it wrote back holds the shipped source word for word.
- `tools/monkey_v1b.py --lists`, 1,000 runs of random keys, taps, menu picks and typed values on beta 3k: 1000 runs, 120 events each, 229 s; OK 1000.

Not yet run on a G1 or a G2.
