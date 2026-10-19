# EpiStats v1.7d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on v1.7c; every v1.7c feature is kept, and every ordinary display is unchanged. Run only in the PC harness (ppl_run_v3e); not yet run on hardware or on the emulator (v1.7c never ran on the emulator either; v1.7b did).*

## Why (fleet review, 19 Oct 2026, findings_A §1)

- **E1, a probable crash.** "Sample-size forms do not validate α or power." α = 0, power = 1, α = 2, power = 1.5 … reached `NORMALD_ICDF(0, 1, 1)`, `(0, 1, 0)` or `(0, 1, 1.5)` in all four forms; what the Prime does there (an error, or ±∞ and then `CEILING(∞)`) has never been seen.
- **E2, a wrong number.** "Module 2 treats an empty row as a risk of 0 %." Grid 0 0 5 5 printed `Risk in Exposed (Re): 0.0% (0/0)`, `RD = -50.0%`, `NNT (benefit) = 2.0` and drew the icon array; `EP_RD = -0.5`, `EP_NNT = 2`.
- **E3, a wrong number.** "Module 3 prints sensitivity 0.0 % (or specificity 0.0 %) when the column is empty." Grid 0 5 0 30 printed `Sensitivity: 0.0%`, `LR+ (positive): 0.00`, `LR- (negative): 1.167`, `FNR (β): 100.0%`, `Youden's J Index: -0.143`.
- **E4, wrong text.** "Module 1 prints RD = 0.0 % with a 'CI' of (-100.0-100.0 %) when a row is empty", under a worked box that says RD is undefined.
- **E6.** "Module 4 page 3: a long waiting time runs off the screen": `1000000.001 time units` from x 200, about 354 px.
- **E7** (findings_A: "low; fix if wanted"; added to v1.7d at the coordinator's request, 19 Oct 2026, the version unchanged because v1.7d was not yet delivered). "Module 2 page 5: `ᴇ` on the NNT line for an absurd table": grid 1 999999 1 1000000 (|RD| about 1E−12) printed `NNT = 1/< 0.000001 = 1.00ᴇ12, round up: 1ᴇ12` and `Expose 1ᴇ12 (blue)`, and page 3 `Interpretation: For every 1.00000100011E12 exposed,` (Standard format past 12 digits; the harness writes it with E). An NNT above a million says nothing a reader can use.
- **E8.** "Four remaining `1 - CHISQUARE_CDF` sites" (McNemar; the M-H χ², plain and corrected; Breslow-Day): exactly 0 above χ² ≈ 52 on the Prime, so `EP_MCN_P`, `EP_MH_P`, `EP_BD_P` read 0 where `EP_chisq_p` (v1.7c) keeps its digits.
- **E9.** "Module 4 accepts fractional cases": `2.5 cases / 1200 person-time`.
- **E10.** "Two stale references": the comment banner said v1.7b; `verify_EpiStats_v1.7c.py` named `CICatcher_beta2a.txt` and stopped with `FileNotFoundError` on a folder of current files, so its parts B2-G never ran there (review item 22).
- **E11.** "`es_Cnt` … `STRING(cnV, 2, 1)` prints `5.0ᴇ-2` for a person-time of 0.05 typed into the rates grid."
- **Roger's disclaimer** (19 Oct 2026, 12:48): a DISCLAIMER line beside the distribution terms.

## What changed (line numbers: v1.7c → v1.7d)

1. **E1** (5210-5221, 5274-5285, 5334-5339, 5386-5391 → 5438-5449, 5515-5524, 5581-5585, 5640-5644). Each form refuses α ≤ 0 or ≥ 1 with `MSGBOX("α must be between 0 and 1 (0.05 is usual).")`, and the two power forms power ≤ 0 or ≥ 1 with `MSGBOX("Power must be between 0 and 1 (0.80 is usual).")`, after the form's own checks and before any `NORMALD_ICDF`. findings_A's text, word for word.
2. **E2** (after 3042 → 3142-3151). Risk Analysis refuses a table with an empty row: `MSGBOX("A risk needs people in both rows: one row of the table is empty.")` and back to the menu, as Incidence Rates refuses zero person-time. It sits before `EP_table` is set, so a refused table changes no EP_* result. (Module 1 still analyses such a table: χ² and Fisher hold there.)
3. **E3** (3912, 4027-4028, 4076, 4116-4157 → 4060, 4178-4191, 4240, 4280-4352). `es_Module_SensSpec` sets `sOK1` (anyone with the disease) and `sOK2` (anyone without); when either is 0, LR+, LR− and Youden's J take the 999 sentinel, on the pages and in `EP_LRpos`, `EP_LRneg`, `EP_youden`. `es_SS_Page1` takes `sOK1, sOK2` (8 → 10 arguments) and prints `undef (no Disease+)` / `undef (no Disease-)` for the missing proportion and for both LRs (each needs sens AND spec: findings_A paired LR− with the Disease− column, but LR− = (1 − sens)/spec is undefined without either), and `undef` for FNR or FPR. Page 2's Youden's J reads `undef` through the sentinel; `es_SS_Page2` is unchanged.
4. **E4** (2724-2731 → 2817-2829). With a row empty, `RD := 999` and `EP_RD_CI := {0, 0}`: the cohort tab reads `RD = Re - Ru = undef`, page 5 `undef` with no CI, `EP_RD = 999`. Help > Variables (5582-5597 → 5838-5856) names the sentinel on its formerly blank line: `999 = undefined (EP_RR, EP_RD, EP_LRpos ...)`.
5. **E6** (4425-4434 → 4625-4640). Page 3's heading reads `─── Mean Waiting Times (time units) ───` and each waiting time stands alone at x 200. The heading says "Mean" for "Average" so that it fits too: 39 characters, about 306 px at ppl_check_v4's widest estimate (7.6 px); with "Average" (42) it drew a W3 warning there. The numbers keep their 2 decimals (findings_A wrote `es_FmtNum(WTe, 1)`; the suffix, not the number, was too wide).
6. **E8** (742, 4691, 4694, 4718 → 828, 4901, 4904, 4936). Each p is `2 * NORMALD_CDF(0, 1, -(x^0.5))`, P(χ²₁ > x) as a lower normal tail, kept to its last digit. All four have 1 df: Breslow-Day's K − 1 with the two strata this module takes (it is skipped when one is dropped); the comment there says what a third stratum would need (df 2: `EXP(-x/2)`; more: χ²'s own upper tail). No `1 - CHISQUARE_CDF` is left in the file. Screens are unchanged (`es_PTxt` already printed `p < 0.0001`).
7. **E7** (3091-3097, 3245-3264, before 3427 → 3200-3213, 3361-3400, 3563-3574). For |RD| below 0.000001 (an NNT above 1,000,000; RD = 0 keeps its own message):
   - page 3 reads `NNT (harm) = 1/RD   > 1,000,000` (or `NNT (benefit) = 1/|RD|`, in its side's colour, with no "=" before the relation), then `RD near 0 (|RD| < 0.000001): no meaningful NNT;` and `the two risks are practically equal`;
   - page 5 reads `NNT > 1,000,000 (RD near 0: no meaningful NNT).`, `The two risks differ by less than 0.000001, so` / `no icon array is drawn.`, and draws no cells, as it does for RD = 0;
   - `EP_NNT` holds 999: Help > Variables describes that sentinel for undefined values (`999 = undefined (EP_RR, EP_RD, EP_LRpos ...)`), and EP_NNT already held it for RD = 0. `EP_RD` keeps its value. The local NNT keeps its value too; the pages decide from RD.
   - From |RD| = 0.000001 up every page is v1.7c's: 1 199999 1 250000 (|RD| = 1.000016E−6, NNT 999,984) is the same to the character.
8. **E9** (after 4285 → 4477-4485). Fractional cases are rounded with `MSGBOX("Cases are whole numbers: the values were rounded.")`, as the grid does; person-time keeps its decimals.
9. **E10.** The comment banner (304 → 383), the menu title (538 → 617) and About (5475 → 5731) say v1.7d. The verify script reads CICatcher beta 2b from `out/`.
10. **E11** (1455-1459 → 1541-1552). `es_Cnt` prints a value between 0 and 0.1 with `es_SigTxt` (three significant figures: `0.0500`); a Haldane half and every whole count print as before.
11. **Header:** the banner (3); the DISCLAIMER line (→ 13-15); the firmware lines (→ 17-29: harness only); a "What changed in v1.7d" paragraph (→ 31-103). Comments above each changed statement say what it does and why.

**Before and after** (harness v3e, end to end; each is a check in part I of the verify):

| Case | v1.7c | v1.7d |
|---|---|---|
| Sample size, 14 forms with α or power outside (0, 1) | `NORMALD_ICDF(0, 1, 1)` etc. (the harness refuses: never seen on the Prime) | the message, no page, no `NORMALD_ICDF` |
| … α 0.999999 and power 0.000001 | | the same pages as v1.7c |
| Risk Analysis 0 0 5 5, 5 5 0 0, 0 0 0 7, 3 0 0 0, 0 0 1 1999 | `Re 0.0%`, `RD -50.0%`, `NNT 2` … | refused; EP_* untouched |
| Sens/Spec 0 5 0 30 | `Sensitivity: 0.0%`, `LR+ 0.00`, `LR- 1.167`, `FNR 100.0%`; Youden `-0.143` | `undef (no Disease+)` ×3, `FNR undef`; Youden `undef`; EP_LRpos/EP_LRneg/EP_youden 999 |
| Sens/Spec 12 0 8 0 | `Specificity: 0.0%` | `undef (no Disease-)` |
| 2×2, 0 0 0 5 (and five more) | `RD = Re - Ru = 0.0%   (-100.0-100.0%)` | `RD = Re - Ru = undef`; page 5 `undef`, no CI |
| 2×2, 10 200 0 10 (McNemar χ² 198) | `EP_MCN_P = 0` | `EP_MCN_P = 5.69E-45` |
| Stratified OR, 500 10 10 500 and 10 500 500 10 | `EP_BD_P = 0` | `EP_BD_P > 0` (= statsmodels) |
| Risk Analysis 1 999999 1 1000000 (\|RD\| ≈ 1E−12) | page 5 `NNT = 1/< 0.000001 = 1.00ᴇ12, round up: 1ᴇ12`, `Expose 1ᴇ12 (blue)`, 100 cells; page 3 `For every 1.00000100011E12 exposed`; EP_NNT 1.000001E12 | page 3 `NNT (harm) = 1/RD   > 1,000,000`, `no meaningful NNT`; page 5 `NNT > 1,000,000 (RD near 0: no meaningful NNT).`, no cells; EP_NNT 999 |
| … 1 1000000 1 999999 (benefit), 1 99999 1 100000, 1 200000 1 250000 | the same, with an NNT of 1E12, 1E10, 1,000,009 | the same |
| … 1 199999 1 250000 (\|RD\| = 1.000016E−6) | | as v1.7c, every page |
| Incidence 1 1 1000000 1000000, page 3 | `1000000 time units` off the edge | `1000000` at x 200; unit in the heading |
| Incidence 2.5 8 1200 1500 | `2.5 cases / 1200 person-time` | message; `3 cases / 1200 person-time` |
| Stratified rates, person-time 0.05 | `5.0ᴇ-2` in the grid | `0.0500` |
| Ordinary tables in every module | | identical |

## Verification

`verify_EpiStats_v1.7d.py`, built from `verify_EpiStats_v1.7c.py`; every check kept; output in `verify_EpiStats_v1.7d_output.txt`: **ALL CHECKS PASSED, 302 checks** (A 7, B 7, C 13, D 66, E 2, F 58, G 4, G2 5, H 58, I 78, REVIEW 3, SCI 1). The headings of A–H name the version that introduced each part; the file they test is v1.7d (G2 and H compare the earlier files they always compared).
- **Runs whole again** (E10): the v1.7c script stopped at part B2 on a folder of current files. v1.7d's reads its predecessors and the v1.6 suite from `out/` by absolute path and compares the shared Clopper-Pearson routines with **CICatcher beta 2b** (they are line for line the same), skipping that comparison cleanly if the file is absent.
- **Harness v3e** throughout (v3d before; the brief's harness).
- **Kept:** A–G2 and SCI as in v1.7c. Part H keeps checking the v1.7c change set (v1.7c against v1.7b), as v1.7c's G2 kept checking v1.7b's. F4's reason for `es_Cnt`'s bare `STRING(x, 2, 1)` names the 0.1 floor.
- **I (new):** each fix against v1.7c, end to end, as in the table (E7: four tables below the line and one just above it, I11); ordinary tables unchanged in modules 1, 2, 3 and 6; E8 against `chi2.sf` and statsmodels to 1.6E−13 relative (McNemar, χ² up to 968) and 2.1E−14 (the M-H p, plain and corrected, and Breslow-Day; three of them exactly 0 in v1.7c), and with the CDFs rounded to the Prime's 12 digits (v1.7c 0, v1.7d positive at χ² 58, 65, 89); the routine diff (exactly the 18 routines the fixes name differ from v1.7c, `EpiStats` and `es_Help_About` in the version string only; the other 106 byte-identical; outside them only comments); the code (the new names, versions, the disclaimer, no comment inside a bracket, LOCAL ≤ 6, INSTRING as before, no `1 - CHISQUARE_CDF`).
- **E7 against the review (I11):** the review's own E7 check (its B3 steps on 1 999999 1 1000000 and its `scan_texts` on the pages shown) **fails on v1.7c and on v1.7d before E7, and passes on v1.7d**. v1.7d before E7 is rebuilt in memory by undoing the three E7 edits; its routines hash to those of the v1.7d file as it stood before E7 (sha256 9f552f68…), and its `es_Risk_Page3` and `es_NNTIcons` are v1.7c's.
- **REVIEW (new): the review's `check_EpiStats.py`** (511 checks) on v1.7d: **508 checks, 0 failed**. The count is 508 on v1.7c too: a refused empty-row table in B3 has one check (the refusal) where it had three ("runs five pages", no scientific E on its pages, the 0/0 reading), and B5 adds one (the message): 511 − 4 + 1. On v1.7c the same script fails 36, every one a check the findings name and nothing else: E4 × 6, E2 × 2, E3 × 6, E6, E8, E9 × 3 (the review's two and the moved B5's message), E1 × 12, the two version checks (D8), and E7 × 3 (the scientific form, EP_NNT, the icon array). Expectations were moved where a fix changes what is right: D8's version string; B3's empty-row tables are refused (E2); B5's 2.5 cases are rounded (E9); C5's twelve forms are refused (E1: the check had asserted the missing guard); B3's EP_NNT and icon array for 1 999999 1 1000000 are the 999 sentinel and no cells (E7; one check for one).
- **SCI:** no scientific STRING result in any harness run of v1.7d in this script (105 runs in parts B, D, F and I), nor in the v1.6 suite's runs, nor in the review's own 109 runs of v1.7d (before E7 they printed `1.00ᴇ12` and `1ᴇ12` on the NNT page of 1 999999 1 1000000).

## Gate

`python3 ppl_gate_v1b.py EpiStats_v1.7d.txt _old/EpiStats_v1.7c.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 66 E4, 36 E9, as v1.7c; no hard errors, E12 included; no warning (the first heading, with "Average", drew W3).
- lint_ppl: 87 problems, as v1.7c (the `a` parameters, `denom`, `center` and STRING's 4 arguments: the tool's known noise).
- Full parse: stops at the file-level LOCAL after the EXPORT list (483), the same construct as v1.7c's 404: the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh` (against `out/EpiStats_v1.7c.txt`): kit lint 0 errors; the same tally; the parse fails on the same line as v1.7c's.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v1.7c (open it in the Kit). Program Catalog → Check. The menu title reads `EpiStats v1.7d`.
2. **Sample Size → Two Proportions**, α = 0: the message `α must be between 0 and 1 (0.05 is usual).`, then the menu (v1.7c went on to `NORMALD_ICDF(0,1,1)`). Power = 1: `Power must be …`. The defaults still give n = 95 per group.
3. **Risk Analysis**, grid 0 0 5 5, Run: `A risk needs people in both rows: one row of the table is empty.`
4. **Sensitivity & Specificity**, grid 0 5 0 30: page 1 `Sensitivity: undef (no Disease+)`, both LRs the same, `FNR (β): undef`; page 2 `Youden's J Index: undef`. In Home, `EP_LRpos` is 999.
5. **2×2 Table**, grid 0 0 0 5: the Cohort tab reads `RD = Re - Ru = undef`; page 5 `Risk Difference (RD): undef` with `95% CI:` blank.
6. **2×2 Table**, grid 10 200 0 10, Esc; in Home `EP_MCN_P` is about 5.69E−45, not 0.
7. **Incidence Rates** 1, 1, 1000000, 1000000: page 3's heading `─── Mean Waiting Times (time units) ───` fits on one line and `1000000` sits at the right of each label. Then 2.5, 8, 1200, 1500: the message, and page 1 reads `3 cases / 1200 person-time`.
8. **Stratified → rates**, stratum 1 cases 1, PT 0.05: the grid cell reads `0.0500`.
9. Help → Variable Reference: the line `999 = undefined (EP_RR, EP_RD, EP_LRpos ...)` fits.
10. **Risk Analysis**, grid 1 999999 1 1000000: page 3 `NNT (harm) = 1/RD   > 1,000,000` and the two grey lines within the screen; page 5 `NNT > 1,000,000 (RD near 0: no meaningful NNT).` with no cells, never `1.00ᴇ12`; in Home `EP_NNT` is 999. Then 1 199999 1 250000: page 5 `NNT = 1/0.000001 = 999984.00, round up: 999985` and the icon array, as before.

## Unresolved (for Roger)

- **D10** (fleet review §3): which two-proportion sample-size formula to name. The page names none, so nothing was relabelled; the formula is the simplified pooled one (95 for 0.5/0.3, where Fleiss gives 93).
- **E5 / D10:** "OR = undef (1.43-760.67)": show the +0.5 estimate or blank the CI. Unchanged.
- **Seen, not changed (E7's twin):** Incidence Rates page 3's person-time NNT (`PT-NNT = 1/|IRD|`, es_FmtNum, which writes `STRING(x, 1, 0)` above 9999) would show the Standard format's exponent for |IRD| below about 1E−12 (person-times near 1E12). Not in the findings; noted for the next pass.
- The review's improvements (module 4 uncertainty, one z for the file, …) are not in this pass.
