# MenuTapProbe beta 1: notes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026.*

**What it asks:** what does `WAIT(-1)` hand back for a tap on the soft-key strip that `DRAWMENU` drew?

**Why:** BayesTree beta 7's soft keys did nothing on the HP Prime Virtual Calculator. Its `WAIT(-1)` loop acts on a type-0 press with y ≥ 218.

**How to run:**
1. Run `MenuTapProbe` from the Catalog.
2. Tap a soft key, then tap the screen above the keys.
3. Press Esc.

Every event is printed on screen and kept in `MT_LOG`, as plain decimals. `WAIT(-1)`'s values are integers, which `STRING()` would print in hex.

**Result (emulator, 2.4.2, build 2026-09-09, 17 Oct 2026):**

| Touched | `WAIT(-1)` returned |
|---|---|
| soft key 2 | `{3,78,230}` and nothing else |
| the screen at (161, 115) | `{0,161,115}`, `{2}`, `{3,161,115}` |

So a strip tap is a click only: no press and no lift. This matches WaitLab's 2014 note. Lessons Learned v7h §7 has the reading pattern; BayesTree beta 8b and StudRange beta 15a use it.

**On the calculators:** run it once on the G2 and once on the G1 to confirm the same sequences.

Gate: `ppl_gate_v1a` PASS (the two lint remarks concern the probe's file name and its EXPORT log, as in the other probes).
