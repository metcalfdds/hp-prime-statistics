# TouchKit template v3: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v2. Comments only: the code is byte-identical to v2.*

## Why: what the emulator showed

BayesTree beta 7 and StudRange beta 15 read their soft keys from WAIT(−1). On the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) not one of those soft keys did anything. MenuTapProbe beta 1 showed why (`Emulator_Round1_Results_2026-10-17_v1.md`). With DRAWMENU on the screen:

| What was touched | What WAIT(−1) returned |
|---|---|
| a tap on soft key 2 | only `{3, 78, 230}`: type 3 (click), no press, no lift |
| a tap on the screen above the keys | `{0, 161, 115}`, then `{2}`, then `{3, 161, 115}` |

GfxProbe T17 added that WAIT(−1)'s values are whole numbers (`#3C:-16h`), so `STRING()` prints them in hex; arithmetic on them is fine.

The template polls GETKEY and MOUSE (its `TouchKit()` loop, v2 lines 199–203). MOUSE sees a finger on the soft-key strip like a finger anywhere else, which is ChiTable's device-verified method, so the template's soft keys work and its code needed no change. The brief asked for the note whatever the method, so that the next program written from the template, if it waits with WAIT(−1), does not repeat BayesTree's mistake.

## What changed

1. **Header, title line:** "TouchKit template v3" (line 3).
2. **"WHAT CHANGED IN v3"** (lines 34–36): one paragraph.
3. **A new comment block, "SOFT KEYS AND WAIT(-1)"** (lines 52–80), at the end of the header. It covers:
   - WAIT(−1)'s own type table (0 Down, 1 Move, 2 Up, 3 Click, 5 Stretch, 6 Rotate, 7 Long click);
   - the three sequences: a soft-key tap is only {3, x, y}; any other tap is {0}, {2}, {3}; a drag is {0}, {1} …, {2};
   - what a WAIT(−1) program must do:
     - read soft keys from type 3 with y ≥ 218, `slot := MIN(6, IP(x / 53.4) + 1)`;
     - ignore type 3 above the strip, and let a type-0 press on the strip do nothing;
     - check `SIZE(ev) >= 3` before reading x and y;
     - remember that a press closing a page still owes its {2} and {3}, which reach whatever waits next. It names BayesTree beta 8b's and StudRange beta 15a's lists, `btTLX` and `srTLX`;
   - add 0.0 before `STRING()` of a WAIT(−1) value;
   - one line of history saying why this matters.

## Verification

`verify_TouchKit_template_v3.py` is new; there was no verify script for v1 or v2. It runs in harness **ppl_run_v3c**. Output in `verify_TouchKit_template_v3_output.txt`: **12 PASS, 0 FAIL.**
- v3's code is byte-identical to v2's once comments are removed.
- The note says what the emulator measured.
- In the harness, the soft keys (read through MOUSE) work on both pages: −0.5 then Quit; More, Full, More, +0.5 then Quit.
- A drag on bar 2 sets it from the finger, the arrow keys work, Esc quits, and no harness warning is raised.

## Gate

`python3 ppl_gate_v1a.py TouchKit_template_v3.txt TouchKit_template_v2.txt` gives **RESULT: PASS**.
- ppl_check_v3: clean.
- lint_ppl: the same 4 problems as v2.
- fleet_names_v2: 0 collisions, 0 untagged.

With the unpacked hp-prime-kit, the kit lint gives 0 errors.

## Device checklist

Nothing new to try: the code is v2's. If the template is ever run, tap each soft key on both pages.

## Left as it was (stale, for the next edit)

- Step 3 of "HOW TO USE" still names `ppl_gate_v1.py`; the current gate is `ppl_gate_v1a.py`.
- "WHAT IS NOT IN IT" still lists FILLPOLY_P, TRIANGLE_P alpha and blends, the scaled BLIT_P and a LOCAL MAKELIST counter as unverified. GfxProbe beta 1 passed all four on the emulator (T01–T06, T08, T19). They have not run on a G1 or G2.
