# StudRange beta 15a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 15; every beta 15 feature is kept, and the #PYTHON srq block is byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

StudRange beta 15 ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) on 17 October 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, section "StudRange beta 15"):

- **Item 8, "Soft keys on the plot": FAIL.** "α+ does nothing", and the same goes for α−, k−, k+, df and Menu. The cause is the one MenuTapProbe beta 1 found for BayesTree. With DRAWMENU on the screen, a tap on the soft-key strip reaches WAIT(−1) **only** as `{3, x, y}` (type 3, a click), with no press and no lift. A tap above the strip arrives as `{0, x, y}`, then `{2}`, then `{3, x, y}`. Beta 15 read soft keys from a type-0 press with y ≥ 218 (beta 15 lines 1915–1917), which never comes.
- **Item 13, Quit.** It returned "StudRange: q crit = 3.8612, p = 0.00000, HSD = …". The p reads 0.00000 when no P-value was asked for, and the q crit is the HSD run's (k = 4), not the plot's, with nothing to say so.

## What changed (line numbers: beta 15 → beta 15a)

1. **The plot's soft keys are read from type 3** (sr_PlotMode's touch handling, 15 1891–1936 → 15a 1956–2008). A type-3 event with y ≥ 218 that is not a stale click sets `pmAct := MIN(6, IP(x/53.4)+1)`, the same action codes as before (15a 1989–1991). A type 3 above the strip is still ignored. A type-0 press at y ≥ 218 still sets `pmDrag := 4`, so the drag samples after it are ignored, but **no longer acts** (15a 1996–2003): a firmware that sent both a press and a click would otherwise run the key twice.
2. **No stale click.** This is the same guard as BayesTree beta 8b, smaller here because the plot opens no WAIT(−1) views.
   - The plot's own presses above the strip, and every tap that a page held by `sr_WaitAny` reads, are written down in order (new file-level `srTLX`, `srTLY`, `srTLi`, 15a 306–310; `sr_WaitAny` appends at 1040).
   - The plot skips a click that matches the next spot, and forgets the list at the first event that does not match, at any press or move, or at a key (15a 1966–1987, 1939). The list is cleared when the plot opens (1683).
   - The case it covers is not measured: a help page closed by a tap on its footer leaving that tap's click for the plot. With the guard patched out, the harness's worst case fires k− there.
3. **The Quit summary** (StudRange(), 15 2227 → 15a 2314–2326). It names the q crit it quotes, the last one computed by Critical value or HSD: "q crit (k = 4, ν = 28) = 3.8612", or ν = ∞ for df 0. It says "p not computed" and "HSD not computed" for values this session never asked for. The HSD line had the same slip: it printed "HSD = 0.0000". New file-level `srQK`, `srQV`, `srPK`, `srHK` (15a 311–315) are set by sr_PvMode (1357), sr_CritMode (1404) and sr_HSDMode (1456), and reset when the program starts (2289). When the PPL fallback raised df 2 to 3, the summary names the df actually used (ν = 3).
4. **Header.** A "What changed in beta 15a" paragraph, the status line, and the banner and title line now say beta 15a. The #PYTHON block's own comment ("StudRange beta 15 - the MicroPython engine") is left as it is, so the block stays byte-identical.

Nothing else changed. The routines that differ from beta 15 are exactly StudRange, sr_CritMode, sr_HSDMode, sr_PlotMode, sr_PvMode and sr_WaitAny (verify 7g).

## Verification

`verify_StudRange_beta15a.py` (built from verify_StudRange.py; harness **ppl_run_v3c**). Output in `verify_StudRange_beta15a_output.txt`: **61 ok, 0 failures.**

- **Sections 1–6, kept:** the MicroPython engine against SciPy (q crit within 5.0E-6 relative), the PPL engine (within 8.1E-3), the plot cache, the H0 simulation, k = 2, and the real source in the harness. These cover the P-value with Python and with PPL, df 2 both ways, the HSD (1.3652, the same as SciPy), the yardstick, the plot with the badge, the q crit box, the plot menu without Python, the simulation, the k = 2 curve, diagnostics both ways, and help.
- **Section 7 (new):**
  - 7a: each soft key works from its type-3 click alone: α− (0.050 → 0.025), α+ (→ 0.100), k− (3 → 2), k+ (→ 4), df (the form opens; 20 rebuilds), Menu (the plot menu);
  - 7b: **beta 15 in v3c: α+ and Menu do nothing**, the emulator's FAIL reproduced;
  - 7c: a type-0 strip press does nothing, and an injected {0}, {2}, {3} strip tap steps α exactly once;
  - 7d: a tap in the plot moves q obs to the finger once; a tap on the q crit box sets q obs = q crit;
  - 7e: the plot's help page closed by a footer tap fires no soft key, both normally and in the `mouse_tail` worst case. Without the guard that worst case **does** fire k−;
  - 7f: the Quit summary:
    - nothing computed: "q crit not computed, p not computed, HSD not computed (engine: none)";
    - the emulator's run (HSD only): "q crit (k = 4, ν = 28) = 3.8612, p not computed, HSD = 1.3652". Beta 15 in the same run still prints "p = 0.00000";
    - P-value then Critical value: "q crit (k = 3, ν = 12) = 3.7729, p = 0.07000" (both SciPy);
    - the PPL fallback's df 3 and df ∞ are named;
  - 7g: the routine diff, and the #PYTHON block byte-identical.

## Gate

`python3 ppl_gate_v1a.py StudRange_beta15a.txt StudRange_beta15.txt` gives **RESULT: PASS**.
- ppl_check_v3: 1 E7, the same as beta 15.
- lint_ppl: the same 18 problems as beta 15, including the #PYTHON block's "depth went negative".
- fleet_names_v2: 0 collisions, 0 untagged.

With the unpacked hp-prime-kit, the kit lint gives the same single "unbalanced" error as beta 15 (the #PYTHON block).

## Device checklist (emulator first, then G2 and G1)

1. Paste and run.
2. Distribution plot (k 3, df 12, q obs 3.5). Tap each soft key in turn:
   - **α−**: α 0.050 → 0.025;
   - **α+**: back up;
   - **k−** and **k+**: k changes and the curve is rebuilt;
   - **df**: the form opens;
   - **Menu**: the plot menu opens.
3. Tap inside the plot: q obs jumps there once. Tap the q crit box: q obs = q crit, p = α.
4. Plot menu → Help for this plot. Close it by tapping the **bottom** line of the screen, about where α+ or k− sits. Back on the plot, nothing should change.
5. Tukey HSD (α .05, k 4, m 8, MSE 1), then Quit. You should see "StudRange: q crit (k = 4, ν = 28) = 3.8612, p not computed, HSD = 1.3652 (engine: …)".
6. After tapping a form's OK with a finger (df soft key → OK), check that the plot did not take that tap as a soft key (see Unresolved).

## Unresolved

- Whether an OS dialog (INPUT, CHOOSE) leaves a click for the next WAIT(−1) is not known; checklist step 6 shows it.
- A genuine soft-key tap at exactly (±2 px) the spot of the tap that just closed a page, as the very first touch after it, would be skipped once. A second tap works.
- The plot still redraws on every WAIT(−1) event, the lift and the click of a tap included. That is beta 15's loop, and on the calculator those events already arrived, so nothing changed.
