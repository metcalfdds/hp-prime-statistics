# BayesTree beta 8e: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 8d; every beta 8d feature is kept, and every ordinary display is unchanged. Run only in the PC harness (ppl_run_v3e); not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md` section 2, items 7 and 20; `findings_E.md` section 2):

> **B1** -- WRONG NUMBER. "`BayesTree_beta8d.txt:1443-1448`: the diagnostic odds ratio is printed as infinite at low prevalence. The 'no false negatives / positives' test is `cfn < 0.5 OR cfp < 0.5` on the EXPECTED cells of the stage, which at the default N = 1000 are fractions of a person as soon as the prior is small: prior 0.001, sens 0.90 gives FN = 0.1, so the page reads 'diagnostic OR = ∞ (no false negatives/positives)' while sens = 0.900 is printed two lines above and the DOR is LR+/LR- = 18 / 0.105 = 171."

> **B2** -- "A flick sets the slider to 0.999. WaitLab recorded a flick ending `{1, 65535, y}`; the slider (3037), the PPV view (1637) and the ROC view (1773) read x from every move."

> **B3** -- "`:1151, 1156`: 'D+ = N × prior = 1000 × < 0.001'." **B5** -- "`:1454`: 'NND = undef (J ≤ 0)' also for 0 < J <= 0.0005." **B6** -- "`:1461`: 'prevalence' on the Diagnostics page with two tests is test 1's PPV." **B7** -- "`:2631`: Enter counts with non-whole counts gives a non-whole N on the tree ('N = 19.8')."

**Roger's addition (19 Oct 2026, 12:48):** the header line "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes.", and one line on its Help page.

Not in this pass: **B4** ("NPV = 1.000" for 0.99989, Roger's decision).

## What changed (line numbers: beta 8d → beta 8e)

1. **B1, the diagnostic odds ratio** (`bt_DiagView`, 1436-1448 → 1494-1525). It is worked out from the **rates**, `dor := (se*sp)/((1-se)*(1-sp))` (= LR+/LR− = TP·TN/(FN·FP); written as one fraction so nothing is divided by sp), where se and sp are the cells' rates -- the stage's sens and spec, which every input path clamps to 0.001 or 0.01 … 0.999, so the DOR is finite. It is "∞ (sens or spec = 1)" only if sens or spec is exactly 1, which no path reaches (a guard for direct calls). A DOR of 1000 or more prints as a whole number (`bt_fmtc`: 998001 at 0.999 / 0.999; 18981 after Enter counts with FN = 0), smaller ones with 3 decimals as before. When sens or spec is at its 0.999 cap the note reads "(sens or spec at its 0.999 cap)" (it may stand for a typed "no false negatives"), otherwise "(LR+/LR−)" as before.
2. **B2, a flick** (the slider and the branch drags in `BayesTree()` 3034-3056 → 3136-3165; the PPV view 1635 → 1719-1722; the ROC view 1770 → 1857-1860). A move is used only when its point is on the screen, `x >= 0 AND x <= 320 AND y >= 0 AND y <= 240`; a flick's last move (x = 65535) is skipped and the drag keeps the value of the move before it. The main loop's move block is re-indented inside the guard, otherwise unchanged.
3. **B3, "D+ = N × prior"** (`bt_NodeInfo`, 1151 and 1156 → 1208 and 1214; new LOCALs `niPS`, `niDg` at 1159; worked out once at 1160-1178). The prior there is a factor, so it is printed as a number: 3 decimals from 0.001 up (unchanged), below that as many decimals as reach its first digit, at least 4: "1000 × 0.0001" (the smallest prior the program takes), "990 × 0.000001" for a second test's stage prior. `STRING(ROUND(p, d), 2, d)`, so never scientific.
4. **B5, NND** (1454 → 1529-1536): "undef (J ≤ 0)" only when J ≤ 0; for 0 < J ≤ 0.0005 "undef (J near 0)". (findings_E proposed "J ≈ 0"; the approximately-equal sign has not been seen on our calculators -- GfxProbe T14 tested ≤, ≥, ≠ but not ≈ -- so it is written in words.)
5. **B6, the prevalence with two tests** (1461 → 1543-1545): "prevalence = 0.667  (test 1's PPV)" when `btNS > 1`; nothing added with one test.
6. **B7, Enter counts** (2622-2627 → 2717-2729). Typed counts are cut to whole people (`MAX(0, IP(x))`), so N on the tree is a whole number ("N = 918" for 10.8 / 9.2 / 45.5 / 854.9; beta 8d "N = 920.4"). **The form now opens with the whole counts the tree shows** (`bt_RCnt`), not the expected counts (0.9 / 0.1 / 49.95 / 949.05 at prior 0.001), so OK on the form never offers a fraction that IP would then cut -- at prior 0.001 IP alone would have turned the prefilled 0.9 and 0.1 into 0 and 0 and refused the form. (It also fixes the first-menu prefill, which beta 8d showed as 0 / 0 / 0 / 0.) OK on the prefilled form at the defaults keeps prior 0.1, sens 0.9, spec 0.95; at prior 0.001 it gives the tree's 1 / 0 / 50 / 949, i.e. sens 0.999 (see Unresolved).
7. **The notice (Roger, 19 Oct 2026).** The DISCLAIMER line in the header (→ 9), verbatim, after the distribution terms; and "Teaching aid; not for casework or legal use." in red on help page 3, "reading it forensically", its 13th line (y 197; the page has 11 lines, so line 12 is a gap) (`bt_HelpView`, 2446-2448 → 2536-2543).
8. **Header:** the banner "beta 8e"; the tested-on lines (8c passed the retest on the emulator; 8d and 8e have not run there; 8e only in the harness); a "beta 8e" paragraph (26-62) in beta 8d's line numbers.

Nothing else changed. The routines that differ from beta 8d are exactly `BayesTree`, `bt_DiagView`, `bt_HelpView`, `bt_NodeInfo`, `bt_PrevView` and `bt_RocView`, each by exactly the change above (verify part G (8e)); outside them only comments differ.

**Before and after** (harness ppl_run_v3e):

| Where (how) | beta 8d | beta 8e |
|---|---|---|
| Diagnostics: defaults, − ×6 (prior 0.001), More, Diag | `diagnostic OR = ∞   (no false negatives/positives)` | `diagnostic OR = 171.000   (LR+/LR−)` |
| Diagnostics after Enter counts 90 / 0 / 45 / 855 | `diagnostic OR = ∞   (no false negatives/positives)` | `diagnostic OR = 18981   (sens or spec at its 0.999 cap)` |
| Slider drag ending in a flick (x = 65535) | prior 0.999 | prior of the last on-screen move (0.69) |
| PPV view / ROC view, the same flick | prior 0.999 / spec 0.01 | 0.32 / 0.68 (the last on-screen move) |
| Sens pair dragged, last move at y = 65535 | sens 0.01 | 0.95 |
| D+ node page at prior 0.0001 | `D+ = N × prior = 1000 × < 0.001` | `D+ = N × prior = 1000 × 0.0001` |
| Two tests from prior 0.0001 (stage prior 1.0E-6) | `D+ = N × prior = 990 × < 0.001` | `D+ = N × prior = 990 × 0.000001` |
| Diagnostics, J = 0.0004 | `NND = undef (J ≤ 0)   (1/J)` | `NND = undef (J near 0)   (1/J)` |
| Diagnostics, two tests | `prevalence = 0.667` | `prevalence = 0.667  (test 1's PPV)` |
| Enter counts 10.8 / 9.2 / 45.5 / 854.9 | `N = 920.4` | `N = 918` |
| Help page 3 | -- | `Teaching aid; not for casework or legal use.` (red) |
| Defaults: tree, panel, summary | `PPV = 2/3`, `NPV = 171/173` … | the same |

## Verification

`verify_BayesTree_beta8e.py`, built from the beta 8d script, every check kept, harness **ppl_run_v3e**. Parts A, B, S, L, C, R and R8 run on beta 8e; part G (8c) keeps reading beta 8c and 8b, and part T (8d), which checks the 8c → 8d step, keeps reading beta 8d and 8c (part U carries it to 8e). Output in `verify_BayesTree_beta8e_output.txt`: **285 PASS, 0 FAIL** (the 8d script: 235; new: 35 checks in part U, 15 in G (8e)). Run time 31 minutes.

- **One change to the script's plumbing:** the record of every harness kept for R8 now holds only each harness's file list and its `sci_strings` list (the same objects), not the harness. The first full run kept all of them alive and was killed for memory (exit 137) at the start of part T2, as findings_E reports for an earlier re-run of the 8d script; no check changed.
- **B16 (kept):** beta 7's verify run against beta 8e: the same 5 intended differences as against beta 8d, nothing else.
- **U1, B1:** the review's case (171.000; beta 8d ∞), from the keys; a sweep of 320 states (prior 0.0001 … 0.999, N 10 and 1000, sens and spec 0.01 … 0.999): every DOR line = (sens·spec)/((1−sens)(1−spec)) at the shown precision and = TP·TN/(FN·FP), the cap note exactly when sens or spec is 0.999, never ∞, no other line changed (beta 8d printed ∞ in 215 of them; the cap note shows in 128); Enter counts with FN = 0 (18981, cap note; beta 8d ∞); the guard by direct calls (sens or spec = 1 → ∞; 0 → 0.000; no error).
- **U2, B2:** a drag and the same drag ending in a flick give the same value on the slider, the PPV view, the ROC view and the sens pair (x = 65535, and y = 65535); beta 8d jumps to 0.999 / 0.01.
- **U3, B3:** node pages D+ and "source" at 10 priors (0.0001 … 0.999 and 1.0E-6): the number as specified, never "× <", every other line unchanged; from the tree at prior 0.0001 and with two tests; beta 8d "× < 0.001".
- **U4, B5:** NND at J = 0.0004, 0, −0.1, 0.0006, 0.85.
- **U5, B6:** two tests and back to one, through the menu.
- **U6, B7:** typed fractions; the prefill (90 / 10 / 45 / 855 at the defaults, 1 / 0 / 50 / 949 at prior 0.001); OK at the defaults changes nothing.
- **U7:** the T2 sweep, beta 8e against beta 8d: 160 states × (the tree, the summary, five views, 13 node pages): 54 identical; in the other 106 every differing line is a DOR line (100, checked by value), an NND line (10; "J near 0" exactly when 0 < J ≤ 0.0005) or an "N × prior" line (32, checked by value).
- **U9, the notice:** help page 3 shows the line in red at y 197, inside x 316 by a 6.5 px-per-character model, 28 px below the last line and above the footer; pages 1-2 do not; beta 8d has none; the DISCLAIMER header line.
- **U8, the review's own `check_BayesTree.py`** on beta 8e and 8d: 8d 136 PASS / 7 FAIL, 8e 141 / 2. The 6 checks 8d failed for B1 (2), B2 (3) and B3 pass; the one still failing is B4's "NPV = 1.000" (Roger's decision); the one that now "fails" recorded the old NND text ("J ≤ 0" for J = 0.0004), which B5 changed on purpose.
- **G (8e):** the routine diff above, each routine by exactly its change; banner and header; no code line names a beta; LOCAL lines ≤ 6 names; `niPS` and `niDg` are not built-ins ignoring case; no comment inside a bracket; INSTRING count unchanged; no new character in code.
- **R8 (kept):** no `STRING(x, 2, d)` of beta 8e printed in scientific form in any of its 407 harness runs.

## Gate

In `gate_f19` (beta 8d moved to `_old/`): `python3 ppl_gate_v1b.py BayesTree_beta8e.txt _old/BayesTree_beta8d.txt` → **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 1 E4, 2 E5, 1 E9, the same as beta 8d; no hard errors, E12 included.
- lint_ppl: 20 problems, as 8d (one "STRING() with 4 args" is new -- the ROUND form in `niPS`, split at its commas -- and 8d's "INPUT return discarded" is gone).
- Full parse: stops at `√` (1525; 8d at 1450), the tool's limit.
- fleet_names_v2 over the newest 25 files: 0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches.

`check.sh NEW OLD`: kit lint 0 errors; the ppl_check tally equals 8d's; parse fails on the same statement.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 8d (open it in the Kit); Program Catalog → Check.
2. **B1:** Close the menu, press − six times (prior 0.001), More, Diag: "diagnostic OR = 171.000   (LR+/LR−)". Then Enter counts 90 / 0 / 45 / 855 → Diagnostics: "diagnostic OR = 18981   (sens or spec at its 0.999 cap)", the line whole.
3. **B2 (calculator, a real finger):** flick the slider knob to the right and off the screen; the prior should stay near where the finger left the track, not jump to 0.999. The same in the PPV view and the ROC view. (The emulator's mouse cannot flick; record what the hardware sends.)
4. **B3:** Enter values: prior 0.0001 → tap the D+ box: "D+ = N × prior = 1000 × 0.0001".
5. **B5, B6:** Enter values prior 0.2, sens 0.5, spec 0.5004 → Diagnostics: "NND = undef (J near 0)". Second test 0.9 / 0.95 from the defaults → Diagnostics: "prevalence = 0.667  (test 1's PPV)".
6. **B7:** Enter counts: the form shows 90 / 10 / 45 / 855; type 10.8, 9.2, 45.5, 854.9 → the root reads "N = 918".
7. **The notice:** Help → page 3: the red line "Teaching aid; not for casework or legal use." whole, below the text, above the footer.

## Unresolved

- **B4 (Roger):** "NPV = 1.000" for an NPV of 0.99989 (prior 0.001), or "> 0.999"; the review's check still fails on it.
- **B1 wording (Roger):** the note "(sens or spec at its 0.999 cap)" is findings_E's; whether to say it so, and how to word "no false negatives" typed as counts.
- **B7 (Roger):** OK on the Enter-counts form now takes the tree's whole counts as data, so at a small prior (0.001: 1 / 0 / 50 / 949) it sets sens to 0.999 where beta 8d's fractional prefill gave back sens 0.9. That follows from counts being whole people; a form that keeps the old values unless one is typed would need a decision.
- **B5:** "undef (J near 0)" uses words where findings_E wrote "≈" (an unverified glyph); for 0 < J ≤ 0.0005 the NND is defined (above 2000) -- the program still declines to print it, as before.
- **B2:** the flick's event shape on the 2026-09-09 firmware is WaitLab's 2014 record; a move with x or y off the screen is ignored whatever its cause.
- **The notice:** one line, on help page 3 (the forensic page); BayesTree has no About page. Pages 1 and 4 are full.
