# BayesTree beta 8b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 8a; every beta 8a feature is kept, and the CAS call form (`bt_Cas`) is byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

BayesTree beta 7 ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) on 17 October 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, section "BayesTree beta 7"). Beta 8a has the same event code.

- **Soft keys under WAIT(-1): FAIL.** "Tapping Values or ROC does nothing (the Enter menu still works)." MenuTapProbe beta 1, written for this, recorded every WAIT(−1) result with DRAWMENU on the screen:

  | What was touched | What WAIT(−1) returned |
  |---|---|
  | a tap on soft key 2 | only `{3, 78, 230}`: type 3 (click), no type 0, no lift |
  | a tap on the screen above the keys | `{0, 161, 115}`, then `{2}`, then `{3, 161, 115}` |

  Beta 8a read a soft key from a type-0 press with y ≥ 218 (8a lines 2574–2585), which never arrives on the strip.
- **Rounding slip.** After a sens drag to 0.835, the D+ 100 branch showed T+ 84 and T− 17 (83.5 and 16.5, each rounded): 101.
- **Cosmetic.** "The first-level numbers (0.100 / 0.900) sit on top of the branch lines."

## What changed (line numbers: beta 8a → beta 8b)

1. **Soft keys are read from type 3** (main loop, 8a 2565–2660 → 8b 2709–2848). A type-3 event with y ≥ 218 is a soft key: slot `MIN(6, IP(x/53.4)+1)`, slot 6 = More, as before (8b 2806–2826). A type 3 **above** the strip still falls through to the old "gesture over" branch and does nothing new: a screen tap sends 0, 2 and 3, and acting on both would run it twice. The type-0 path at y ≥ 218 is **neutralised** (8b 2742–2748): it sets nothing, so a firmware that ever sent a press *and* a click for a strip tap would still run the key once.
2. **No stale click** (new; not in the brief, but the same double-fire in another place). The harness showed it: the PPV, ROC and Fagan views close on a type-0 press read from WAIT(−1), and that tap's `{2}` and `{3, x, y}` then reach the tree. If the tap was on the view's footer (y ≥ 218), the tree, now reading soft keys from type 3, would run the soft key under that spot (closing the PPV view by tapping its footer at x 150 opened ROC). So every tap whose click may still come is written down in order:
   - new file-level lists `btTLX`, `btTLY` and the pointer `btTLi` (8b 311–313), cleared at start (2277);
   - the three views append their closing tap (8b 1440, 1568, 1758);
   - `bt_WaitAny` appends every tap it reads (8b 638), in case a tap read through MOUSE also reaches WAIT(−1). That was not seen on the emulator, but it is not ruled out either;
   - the tree's own press (y < 218) starts the list, because its own click follows its lift (8b 2737).

   Such clicks arrive first and in order, so the tree skips a click matching the next spot (±2 px) and forgets the list at the first event that does not match, or at any press, move or key (8b 2715–2737, 2845).
3. **Every pair on the tree adds up.**
   - New `bt_RCnt` (8b 793–802): the counts. N and D+ are rounded; D− = N − D+; T+ is rounded and T− = D+ − T+; the same in the D− row. MIN keeps a child from passing its parent, which can only happen with two tests, when N is not whole.
   - New `bt_RPrb` (808–816): the same rule at three decimals for the Leaves (shares) view.
   - New `bt_fmtq` (825–831): prints such a rounded share. It keeps `bt_fmtp`'s "< 0.001" when the rounded share is 0 but the exact one is not.
   - The boxes, the first-level numbers (prior / 1 − prior) and the second-level ones (sens / 1 − sens, 1 − spec / spec) use them (8b 2551–2611).
   - The node page (two calls) and the 2×2 view get the same rounded counts (2770, 2829; the 2×2 view 2392), so a tapped box's page agrees with the box. The 2×2 view's totals also add up now: before, they read 84 + 17 = 100.
   - PPV and NPV stay exact.
4. **First-level numbers moved off the branch lines.** They were at x 84, y 70 and 142; they are now at x 98, y 78 and 136 (8b 2551–2555), right of the lines. Their tap boxes moved with them: boxes 8 and 9 are now x 92–140, y 74–92 and y 132–150 (8b 2320–2323).
5. **Header.** A beta 8b paragraph, the hardware/emulator status, and two short names: the parameter `rsL` (lint_ppl reads "rpL" as RPL from its own name table) and `fqS`.

Nothing else changed. The verify script checks that the routines differing from beta 8a are exactly `BayesTree`, `bt_FaganView`, `bt_PrevView`, `bt_RocView`, `bt_WaitAny` and the new `bt_RCnt`, `bt_RPrb`, `bt_fmtq`. Outside them only comments and the one new file-level LOCAL line differ.

## Verification

`verify_BayesTree_beta8b.py` (built from the 8a script; harness **ppl_run_v3c**, which models MenuTapProbe's answers). Output in `verify_BayesTree_beta8b_output.txt`: **120 PASS, 0 FAIL.**

- **Kept:** A (every CAS template through desktop Giac = Python fractions), B (exact panel, break-even, CAS only on events, `cas='giac'` and `cas='fail'`), B16 (beta 7's verification: the same 4 intended differences as for 8a, nothing new), G (beta 8 in v3c still shows the CAS finding). B3's expected leaves now follow the new rounding rule.
- **S, soft keys:**
  - each page-1 key runs from the type-3 click alone (Values and Counts open their forms, ROC, PPV and 2×2 their views);
  - **beta 8a in v3c: Values, Counts and ROC do nothing**, the emulator's finding reproduced;
  - More steps 1 → 2 → 3 → 1; Help and Leaves work;
  - a type-0 strip press does nothing, and an injected {0}, {2}, {3} strip tap runs once;
  - a box tap and a branch-number tap each open their page once;
  - PPV, ROC and Fagan closed by a footer tap fire no soft key. With the guard patched out, the PPV case **does** open ROC; a second tap at that spot then works;
  - with `mouse_tail=True` (the unmeasured worst case), a node page and four help pages closed by footer taps fire nothing.
- **L, rounding:**
  - sens 0.835 gives T+ 84, T− 16 / T+ 45, T− 855; beta 8a shows the emulator's 84 / 17;
  - 144 one-test trees (8 priors × 6 sens/spec pairs × N 10, 37, 1000) and 12 two-test trees: every pair adds up, and every count is within one person of exact;
  - 6 trees in shares add up, and "< 0.001" is kept;
  - the FN page says "count = 16 (0.016 of N)", and the 2×2 view reads 84 + 16 = 100, 45 + 855 = 900, 129 + 871 = 1000.
- **C, layout:** neither moved number touches a branch line (sampled at 0.25 px); the old spot lay on the line; a tap on the new spots opens the prior and 1 − prior pages; no tree text passes x 318.
- **G:** the routine diff is as listed; `bt_Cas` is byte-identical to 8a.

## Gate

`python3 ppl_gate_v1a.py BayesTree_beta8b.txt BayesTree_beta8a.txt` gives **RESULT: PASS**.
- ppl_check_v3: the same tally as 8a (1 E4, 2 E5, 1 E9), no hard errors.
- lint_ppl: the same 17 problems as 8a; all are known noise.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged.

The container has no Community_Library zip, so the gate skips the kit lint. Run with the unpacked hp-prime-kit, the kit lint gives 0 errors, and the full parse stops at the root sign, as 8a's does.

## Device checklist (emulator first, then G2 and G1)

1. Paste and run. The first frame: the prior and 1 − prior numbers sit right of the two branch lines, not on them.
2. **Soft keys:** tap Values (the form opens), Cancel; tap ROC (the ROC view), Esc; tap More three times (pages 2, 3, 1); on page 2 tap Help.
3. Tap a box (one node page, not two). Tap a branch number (its page opens once, after the lift).
4. **Stale click:** open PPV with its soft key and tap the footer line at the bottom (about x 150, y 226) to go back. The tree must come back with **no** ROC view opening. Do the same in ROC (tap near x 100) and in Fagan (Enter menu, tap the footer).
5. Open a node page, then close it by tapping at the very bottom of the screen (where a soft key would be). Nothing else should open.
6. **Rounding:** Enter values 0.1 / 0.835 / 0.95 / 1000, or drag the D+ pair to sens 0.835. You should see D+ 100 → T+ 84, T− 16, and D− 900 → T+ 45, T− 855. Turn on Leaves (page 3): 0.084 + 0.016 = 0.100. Open 2×2: 84, 16, 100 in the first row.
7. After tapping **OK** on an INPUT form (Values, then OK with a finger), check that the soft-key page did not change and no view opened (see Unresolved).

## Unresolved

- Whether OS dialogs (INPUT, CHOOSE, MSGBOX) leave a click for the next WAIT(−1) is not known. If tapping a form's OK button turned the soft-key page or opened a view (checklist step 7), the dialog leaks its click. The fix would be to treat the first strip click after a dialog as stale.
- Whether a tap read through MOUSE (`bt_WaitAny` pages) also leaves its click for WAIT(−1) is not known. The list handles both cases.
- A genuine soft-key tap at exactly (±2 px) the spot of the tap that just closed a page, as the very first touch after it, would be skipped once. A second tap works.
