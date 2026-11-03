# GaltonBoard beta 3f: changes

*2 November 2026. Made from beta 3e by a script of exact replacements (17 edits). 2,470 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use") and what round 4's label check found, and a limit on the balls a board holds (Roger, 2 Nov 2026).*

## What the monkey test found

`tools/monkey_v1b.py` drives the program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms (`docs/dev/monkey-fleet-2026-11-01.md`). Beta 3e's 1,000 runs were taken in chunks written run by run (`tools/monkey_chunks_v1.py`, the same seeds as `monkey_v1b.py`), because a single 1,000-run job outlived the session's two-hour limit for a background task and, writing only at the end, left nothing (Lessons Learned v7zi). Beta 3e's first 281 runs (k = 0 to 280) gave 255 OK, 18 with no end within 30 seconds and 8 broken by a typed list; the rest were not needed once the causes were clear.

1. **A typed list.** The two forms (rows R, chance p) were plain names, which take any type, and a list went on into `IP()` and the range test.
2. **No end within 30 seconds: slow, not stuck.** The drops and pours are paced by the clock (at least 25 ms a frame, as on the calculator), so a run of 150 random events that starts several animated drops takes a while: 43 of the OK runs took over 15 seconds, the longest 29.6. Six of the 18 were run again with 300 seconds: five ended normally after 26.8 to 31.8 seconds and the sixth after 43.8, at a typed list (finding 1). None was a hang, and nothing changed for them. Beta 3f's 1,000 runs are given 120 seconds each.

Round 4's label check (`tools/monkey_labels_v1.py`: `text_overlap_v1` with the monkey driving; `docs/dev/label-check-2026-11-02.md`) found two places where text met text:

3. **The bin panel** (a tap on a bar) started at x = 6, and the left readouts ("n = 0", the mean, s) start at x = 4: their first two pixels showed beside the panel's edge, next to "Bin 6 (6 right bounces of 8)".
4. **Pascal's counts**, redrawn as a ball passes a peg, cleared a box from 24 px left of the peg to 4 px short of it, and at the narrow measure the edge of an old "9" lay outside it, under the new "10".

## What changed (line numbers are beta 3e's)

1. **Both forms take a real number only**: `{{srR,[0]}}` (`gbSetRows`, 1656) and `{{spP,[0]}}` (`gbSetP`, 1677). On the Virtual Calculator such a field refuses `{1,2}` with "Invalid input" and keeps its value (TTestLab, 1 Nov 2026). The ranges (R from 3 to 12, p from 0.05 to 0.95) already refused anything else with a sentence.
2. **The bin panel** is drawn from x = 2 to 317 (was 6 to 313; `gbBinInfo`, 1794), over the readouts.
3. **A peg's count** stands 1 px further left and clears from 25 px left of the peg to 3 px short of it (was 24 to 4; `gbPegLbl`, 843–844). The peg reaches 2 px either side of its centre and its left neighbour is 28 px or more away (the counts show only then), so neither is touched; every count of 1 to 4 characters lies inside the box at the overlap check's narrow measure.
4. **The board holds at most 5,000 balls** (Roger, 2 Nov 2026: "put a reasonable limit on number of balls a student can collect--above the threshold just display the results", then "maybe limit to 5,000 or so?"). 5,000 is already the cap of the PPL fallback; past it the bars change little a student can see; the wait stays short (Roger's G1 timing, 20 Oct: the ×100 key in about half a second, so 5,000 balls by PPL about 25 s); and a pour left running (the 0 key or Pour) no longer runs for ever.
   - New `gbRoom` (the balls left, 5,000 − n, never below 0) and `gbFull` (both overlays on, binomial and normal against the bars, and the footer line "5000 balls: the board is full (Menu, Reset)" in red), above `gbDropAnim`.
   - Every drop takes at most what is left: one ball (`gbDropAnim`), ×10 and the pours (`gbPour`: no new ball once those landed and in the air fill the board; the balls in the air finish their fall), 100 and 1000 (`gbDropFast`), and the MicroPython drop (`gbBigDrop`).
   - Menu item 5, "Drop 100,000 (MicroPython)", is now "Fill to 5,000 (MicroPython)" (`gbMenu`, 2203): it fills whatever room is left, still in MicroPython, and keeps its own line ("engine: MicroPython, 5000 balls in … ms") with ": board full" added, since the engine and the time are its point. The help's two lines about it now read "Menu: Pascal's triangle, SD colours, and / MicroPython (the board holds 5,000 balls)." (`gbHelp`).
   - On a full board each drop drops nothing and shows the results. Reset the counts (Menu), or a new R or p, starts a new board.
5. Header: the beta 3f block.

Nothing else changed.

## Verification

`verify_GaltonBoard_beta3f.py`, output `verify_GaltonBoard_beta3f_output.txt`: **15 PASS, 0 FAIL**, run from a repository layout, with beta 3e read from `programs/` or git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** 4 sessions (drops of 1, 10, 100 and 1000; the overlays and SD colours; R and p typed; the arrows; Pascal's counts during two animated drops, then C(r, k); bars tapped with and without balls; help; reset): 280 screens, every text, box and the returned summary identical to beta 3e's but for the help's two lines about the big drop.
- **M** each also run on beta 3e, where it fails: the two typed fields; the bin panel with no balls and after 1,111, no firm overlap on its screens (beta 3e: "n = 0" beside "Bin 6 …", "n = 1111" beside "Bin 4 …"); Pascal's counts up to 19 during an animated drop, no firm overlap (beta 3e: "9" under "10"); the clearing box's geometry (it misses the peg and its neighbour, and holds every count of 1 to 4 characters); the limit, each drop called at the edge (from 4,995 a drop of 100 or a ×10 pour stops at 5,000; from 4,990 a pour stops itself there; a full board drops nothing; each shows the full board's line with both overlays on; below the limit nothing changes; beta 3e went on to 5,095, 5,100 and 10,000, and its pour never stopped); the lines of `gbRoom`; the menu item; the footer line's width.
- **G** only `gbBigDrop`, `gbBinInfo`, `gbDropAnim`, `gbDropFast`, `gbHelp`, `gbMenu`, `gbPegLbl`, `gbPour`, `gbSetP`, `gbSetRows` and the new `gbFull` and `gbRoom` differ; no `!=`; no character in the code that beta 3e's does not already have.
- **D** over every screen drawn (325 distinct): no firm overlap, straddle or overrun (beta 3e on the same runs: 10), and no number cut by its width argument.

**The monkey test again** (1,000 runs, 150 events each, D1 and D2 announced as written): beta 3f **1,000 OK** (beta 3e: 255 of its first 281), with 120 seconds a run (`tools/monkey_chunks_v1.py`, the same seeds as `monkey_v1b.py`): 48 runs took more than 30 seconds and the longest 82, every one ending normally.

## Gate

`ppl_gate_v1d.py GaltonBoard_beta3f.txt GaltonBoard_beta3e.txt`: **RESULT: PASS** (hard errors: none).

## The Virtual Calculator

Virtual Calculator 2.4.2 on Rogers-HP, 2 November 2026, by Claude through computer use. **Check: "No errors in the program."** The checked file in starter pack v9 was collected after that Check and nothing else. Then the program was run and tried by hand: Menu, "Fill to 5,000 (MicroPython)": "engine: MicroPython, 5000 balls in 2 ms: board full", n = 5000, x̄ = 3.98, s = 1.41, the binomial and normal overlays on; then Drop: "5000 balls: the board is full (Menu, Reset)" in red, and no ball dropped. The summary returned "Galton Board: 5000 balls, R = 8, p = 0.50; …".

## Next (Roger, 2 Nov 2026)

Kept as one limit for every drop. Two limits (PPL to 5,000, MicroPython to 100,000) were weighed and left: at 8 rows the bars are 57 px tall, and the random wobble of the tallest bar is about 1 px at 5,000 balls and a third of a pixel at 100,000, so a student would see no difference, and MicroPython has not yet run on a G1 or G2. An idea for after that test: a "small board against big board" page in MicroPython, 5,000 balls against 100,000, showing the largest gap between each bin's observed share and P(k) (about 0.006 against 0.0014: 20 times the balls, √20 ≈ 4.5 times less error), the law of large numbers with numbers to it.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Menu, Rows of pegs: type `{1,2}`: "Invalid input", R kept.
- [ ] Tap a bar before any ball: the panel covers the "n = 0" readout completely.
- [ ] Menu, Pascal: counts; ×10 twice: each peg's count changes cleanly (no remains of the old number).
- [ ] Menu, Fill to 5,000 (MicroPython): how long it takes on the G1 and G2, and the footer line "engine: MicroPython, 5000 balls in … ms: board full"; both overlays on.
- [ ] Then +, −, 0 and Pour: nothing dropped, the footer "5000 balls: the board is full (Menu, Reset)" in red.
- [ ] Menu, Reset the counts: a new board, the drops work again.
