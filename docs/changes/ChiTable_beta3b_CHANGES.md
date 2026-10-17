# ChiTable beta 3b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3a; every beta 3a feature is kept, and csCompute, csFisher and the CAS call form are untouched. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

ChiTable beta 2 ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) on 17 October 2026 and passed every item, with every number matching SciPy (`Emulator_Round1_Results_2026-10-17_v1.md`, section "ChiTable beta 2"). It had two cosmetic findings:

> two CHOOSE items are clipped at the right edge of the box: "Death penalty × defendant's rac[e]" in the Examples list and "N / 10: every count divided by [10]" in the Results menu. Shorten them to about 30 characters.

CHOOSE does not wrap a line wider than its box (F5): it cuts it.

## What changed (line numbers: beta 3a → beta 3b)

1. **Results menu** (csResMenu, 3a 1262 → 3b 1279). "N / 10: every count divided by 10" (33 characters) is now "N / 10: counts divided by 10" (28).
2. **Examples** (csExamples, 3a 2952–2953 → 3b 2971–2972). "Death penalty × defendant's race" (32) is now "Death penalty × defendant" (25). For the pair to still read as a pair, "Death penalty × victim's race" (29, not clipped) is now "Death penalty × victim" (22). The table's own label, shown with every results page, still names the variable: "Death penalty by defendant's race, FL 1976-87".
3. **Every other CHOOSE line** in the program was measured. With × counted as one glyph and "Set α (now …)" at its widest, none is over 28 characters.
4. **Header.** A "WHAT CHANGED in beta 3b" paragraph and the status line, which now says that beta 2 passed on the emulator.

Nothing else changed. The routines that differ from beta 3a are exactly `csExamples` and `csResMenu`; outside them only comments differ.

## Verification

`verify_ChiTable_beta3b.py` (built from the 3a script; harness **ppl_run_v3c**). Output in `verify_ChiTable_beta3b_output.txt`: **5969 checks passed, 0 failed.** Beta 3a's script had 5962; the 7 new checks are below.

- **Kept:** the exact Fisher and χ² fractions against Python and Giac, the 4,900-table arithmetic, `cas='giac'` and `cas='fail'` end to end, the CAS only on events, the routines byte-identical to beta 2 (csCompute, csFisher, …), and the layout.
- **W (new):**
  - every CHOOSE line in the source is at most 30 characters: 23 lines, the longest 28;
  - beta 3a had exactly two longer ones, the two the emulator cut;
  - every CHOOSE line shown in runs through all five examples and the Results menu is at most 30, and the new texts are the ones shown;
  - examples 1 and 2 still load {53, 430, 15, 176} and {64, 451, 4, 155};
  - ×10 N followed by "N / 10: counts divided by 10" gives the table back.
- **G:** the routine diff is as listed.

## Gate

`python3 ppl_gate_v1a.py ChiTable_beta3b.txt ChiTable_beta3a.txt` gives **RESULT: PASS**.
- ppl_check_v3: 1 W3, the same as 3a.
- lint_ppl: the same 13 problems as 3a.
- fleet_names_v2: 0 collisions, 0 untagged.

With the unpacked hp-prime-kit, the kit lint gives 0 errors.

## Device checklist (emulator first, then G2 and G1)

1. Main menu → Examples. All five lines show in full: "Death penalty × defendant", "Death penalty × victim", "Gender × party ID (2 × 3)", "Party ID × gender (3 × 2)", "Simpson (examples 1 + 2)".
2. Example 2, then the Menu soft key. The Results menu shows "N / 10: counts divided by 10" in full. ×10 N, then N / 10, gives 674 back, as before.
