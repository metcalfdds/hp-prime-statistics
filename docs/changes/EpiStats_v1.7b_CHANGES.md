# EpiStats v1.7b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v1.7a; every v1.7a feature is kept, and the CAS call line and quote strip in `es_Cas` are byte-identical. v1.7b itself has not run on hardware or on the emulator.*

## Why: what emulator round 2 showed

Round 2 ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' own firmware) on 17 October 2026 (`BRIEF_R2FIX_v1.md` §0 and §4).

- **EpiStats v1.7a worked there.** Help F ("Where the SE comes from") showed the CAS's own answers: "exact (CAS)", `= 53/120`, SE 0.6646. The CAS never failed, so the fallback was never tested.
- **Two string rules the harness did not model, typed in Home:**

  | Typed in Home | The Prime's answer |
  |---|---|
  | `INSTRING("", "a")` | **Error: Invalid input** |
  | `LEFT("abc", 0)` | `"abc"`, the whole string |
  | `MID("abc", 0, 1)` | **Error: Bad argument type** |
  | `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: **scientific** |
  | `STRING(0.0004, 2, 3)` | `"4.000ᴇ-4"` |
  | `STRING(0.1, 2, 1)`, `STRING(0, 2, 3)` | `"0.1"`, `"0.000"` |

  So "fixed decimals turn scientific whenever 0 < |x| < 10^-d", and "INSTRING on an empty string stops the program."
- **What that means for v1.7a.** `es_Cas` sets `cR := ""` when the CAS fails, then tests `INSTRING(cR, "undef")`. On the Prime that is the error. Harness v3d shows it: with `cas='fail'`, module 3 page 6 and Help F both stop with "INSTRING: Invalid input" (`verify_EpiStats_v1.7a.py` on v3d: 4 failures, `audit_v3d/EpiStats_v1.7a.txt`). The same v3d run of the v1.6 suite found 7 scientific displays in v1.7a: an OR CI from 0.00267 printed as `2.67ᴇ-3`, the forest plot's Breslow-Day p as `3.86ᴇ-6`, and "Crude and M-H differ by `2ᴇ-1` %".

## What changed (line numbers: v1.7a → v1.7b)

1. **`es_Cas`** (760–783 → 798–825). After the quote strip, the undef/error/infinity test runs only when `DIM(cR) > 0`, in the brief's shape and with its comment (v1.7a 778 → v1.7b 816–820). The IFERR line, the quote strip and the `esCasOK` line are unchanged.
2. **The other INSTRING, LEFT and MID calls need nothing.** The `es_Cas` line is the file's only INSTRING. Each LEFT (719, 772) counts 1, and each MID starts at 2, at `DIM(cR)` ≥ 2, or at `swI` ≥ 1 (772, 773, 794, 797). There is no RIGHT.
3. **Fixed decimals are rounded first: `STRING(ROUND(x, d), 2, d)`.** The value is then 0 or at least 10^-d, so the fixed form always holds and reads 0.0 or 0.000. 86 of the file's 155 `STRING(x, 2, d)` calls are now rounded first, in these places (one more, the forest plot's Breslow-Day p, became `es_PTxt`; item 4):

   | Where | v1.7a → v1.7b | What can be small |
   |---|---|---|
   | `es_FmtPct` | 1216 → 1262 | any proportion, e.g. a risk of 1/3000 |
   | `es_FmtCI` | 1230, 1232 → 1278, 1280 | a Wilson lower bound of 0.02 %; an OR or RR CI from 0.003 |
   | `es_Sgn` | 1349–1350 → 1398–1399 | a mosaic tile's adjusted residual near 0 |
   | the count message (`es_Grid`) | 1710 → 1759 | a count typed as 0.004 |
   | `es_Arith`, the OR, RR and RD boxes | 1800–1890 → 1852–1942 | an OR of 0.0003, p1 = 1/3000, ln OR near 0, an RD of 0.0005 |
   | the mosaic panel | 1993, 1996 → 2045, 2048 | E = 0.004; a row % of 0.03 |
   | the three readings | 2142–2169 → 2194–2221 | Youden J, kappa, McNemar χ², Yule's Q and Y near 0 |
   | page 7's null mean | 2490 → 2542 | (a+b)(a+c)/N = 0.004 |
   | risk bars, OR against RR | 3270, 3284–3288 → 3322, 3336–3340 | Ru = 0.03 %; OR and RR below 0.005; "by only 0.07 %" |
   | `es_PctTxt`, PPV vs prevalence | 3387, 3410–3411, 3441, 3455 → 3449, 3472–3473, 3503, 3517 | PPV 0.05 %; sens, spec or prevalence below 0.1 % |
   | the ROC square | 3627–3636 → 3689–3698 | TPR, FPR below 0.1 %; Youden J near 0 |
   | page 6's closed-form decimal | 3761 → 3823 | an exact upper end below 0.0001 (n over 37,000) |
   | the M-H summary | 4680, 4746–4753 → 4742, 4808–4815 | "differ by 0.2 %"; M-H and Breslow-Day χ² below 0.001 |
   | forest plot weights | 4875 → 4937 | a stratum with 0.2 % of the weight |
   | Help F | 5617–5625 → 5679–5687 | SE below 0.0001, Var below 0.000001 (counts near 10^9) |

4. **Two lines read differently**, where a rounded 0 would mislead:
   - **The NNT page** (3328 → 3380–3389). With |RD| below 0.001, "1/0.000" would read as a division by 0, so the RD is shown to three significant figures with the program's own `es_SigTxt`: `NNT = 1/0.000667 = 1500.00, round up: 1500`. The line leaves out "|RD| = " then, so it stays inside the screen. At |RD| of 0.001 or more the line is as before.
   - **The forest plot's Breslow-Day p** (4951 → 5013) uses `es_PTxt`, the program's own p style, as the M-H summary does: `Breslow-Day p < 0.01: are the strata's ORs alike?`. At p of 0.01 or more it reads exactly as before (`p = 0.88`).
5. **Not changed, and why** (68 calls). These cannot reach 0 < |x| < 10^-d:
   - the guarded formatters: `es_PTxt`, `es_FmtNum` and `es_SigTxt` already show a value below 10^-d as "< 0.0001";
   - counts, totals and loop indices (whole numbers, d = 0), and `es_Cnt`'s whole counts and x.5 halves;
   - axis labels, which are multiples of a 1-2-5 step with d = −FLOOR(LOG(step));
   - the mosaic's "all" bar label, drawn only when its tile is 12 px of 112, so 10 % or more;
   - "Re = …" in the OR-vs-RR line, shown only when Re ≥ 0.1;
   - the NNT itself (1 or more), and |RD| in the branch where it is 0.001 or more;
   - the "homogeneous" Breslow-Day p (0.05 or more).

   The verify script lists each one with its reason (F4).
6. **Comments.** Short notes say why at `es_FmtPct`, `es_FmtCI`, `es_Sgn`, `es_PctTxt`, the top of `es_Arith` and the NNT line. No comment sits inside an open bracket (ppl_check_v4 E12: 0).
7. **Header and version.** A "What changed in v1.7b" paragraph (line numbers v1.7a's) and a firmware paragraph that records round 1 (v1.6's 2×2 path) and round 2 (v1.7a's Help F). The banner, the title comment, the main menu's title (473 → 511, still 25 characters) and the About page (5333 → 5395) read v1.7b.

Nothing else changed. The routines that differ from v1.7a are exactly these 21: `EpiStats`, `es_Cas`, `es_FmtPct`, `es_FmtCI`, `es_Sgn`, `es_Grid`, `es_Arith`, `es_Mosaic`, `es_ReadPage`, `es_CORPage`, `es_RiskBars`, `es_NNTIcons`, `es_PctTxt`, `es_PrevDraw`, `es_ROCPage`, `es_ExactPage`, `es_RuleTxt`, `es_MHSummary`, `es_ForestDraw`, `es_Help_SE` and `es_Help_About`. Outside them only comments differ.

## Verification

`verify_EpiStats_v1.7b.py`, built from the v1.7a script, runs every harness session on **ppl_run_v3d**. Output in `verify_EpiStats_v1.7b_output.txt`: **ALL CHECKS PASSED, 163 checks, 0 failures.**

- **Kept:** A (Clopper–Pearson, mid-P and the conditional OR against statsmodels and SciPy), B, C (every CAS template in desktop Giac) and D (end to end, with `cas='giac'` and `cas='fail'`). D4 and D5 with `cas='fail'`, which stop on v1.7a in v3d, now pass. G (v1.7 against v1.7a) still passes.
- **E:** the v1.6 suite now runs on v3d through a shim. It passes, and its 27 harness runs print no scientific number (v1.7a: 7).
- **F1, `es_Cas` directly:**
  - `1/2+1/3` gives `5/6`;
  - `1/0` (the CAS says `±∞`), `0/0` and a syntax error give "" with `esCasOK` 0;
  - with the CAS failing, "" and no error; v1.7a stops with "INSTRING: Invalid input".
- **F2, every CAS page with the CAS failing:**
  - module 3 page 6 (Spec 30/30) shows `exact lower = (α/2)^(1/n) = 0.8843` and "decimal";
  - Help F shows the textbook form, `= 0.441667`, `SE = sqrt(0.441667) = 0.6646` and "decimal";
  - v1.7a stops on both, in `es_XCas > es_Cas` and `es_Help_SE > es_Cas`.
- **F3, sixteen tables that push a display below 10^-d,** covering every changed routine. For each:
  - v1.7a prints scientific in the expected routines;
  - v1.7b prints none, and the line reads as listed above;
  - the pages are the same, and every word that changed was a scientific number (or one of the two reworded phrases).

  Among them: module 1 (1, 2999, 50, 50): `OR = ad/bc = < 0.001   (0.00-0.00)`. Module 2 (1, 2999, 1, 999): `NNT = 1/0.000667 = 1500.00`. Module 3 (1, 1, 2999, 2999): `TPR = sens = 0.0 %`. Module 5: `Breslow-Day p < 0.01`. Help F with counts of 10^9: `SE = sqrt(1/250000000) = 0.0001`.
- **F4, the static sweep:** 154 `STRING(x, 2, d)` calls: 86 rounded first, and 68 bare ones, each with a listed reason.
- **F5:** the one INSTRING is inside `IF DIM(cR) > 0`; every LEFT counts 1; every MID start is listed.
- **G2:** the routine diff is as listed. `es_Cas` keeps its IFERR line and quote strip. No code line says v1.7a.
- **SCI, `h.sci_strings`:**
  - v1.7b: 0 scientific results in 34 harness runs (B, D, F), and 0 in the v1.6 suite's 27;
  - v1.7a: 66 distinct ones, in the 19 comparison runs of F.

**Harness note.** The harness computes in binary floating point, and the Prime in decimal. A value that is an exact tie, such as 0.0005 at three decimals, can round differently in the harness's `STRING` and `ROUND` (`-0.499` against `-0.500`). F3's tables avoid ties for that reason; on the Prime both forms round the same way. A rounded tiny negative prints `-0.000` in the harness (Kappa, Youden J). The Prime may print `0.000` there.

## Gate

`python3 ppl_gate_v1b.py EpiStats_v1.7b.txt EpiStats_v1.7a.txt` (in `gate_r2`) gives **RESULT: PASS**.
- ppl_check_v4: 66 E4 and 36 E9, the same as v1.7a. No hard error, E12 included.
- lint_ppl: 87 problems against v1.7a's 21. The 66 new ones all read "STRING() with 4 args, want 3", one per line that holds a `STRING(ROUND(x, d), 2, d)`. lint_ppl splits a STRING call's arguments at every comma, so the comma inside `ROUND(x, d)` counts as a fourth argument. That is the lint's limit, not an error.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 built-in matches.
- The kit zip is not in the container, so the gate skips the kit lint and the parse. `check.sh` runs both:
  - the hp-prime-kit lint: **0 errors**;
  - the full parse fails at line 377, "expected a name after EXPORT", the file-level LOCAL after the EXPORT list. v1.7a fails the same way at its line 339. That is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Paste, then Program Catalog → EpiStats → Edit → Check: no error. The menu title reads "EpiStats v1.7b".
2. **Module 1 with a table of (1, 2999, 50, 50).**
   - The Cohort tab: `OR = ad/bc = < 0.001   (0.00-0.00)` and `Risk if exposed, a/(a+b) = 0.0%`.
   - Page 5, Down: the OR box ends `= 0.00 to 0.00`.
   - No number on any page has a small ᴇ in it.
3. **Module 2 with (1, 2999, 1, 999).** Page 5 (the NNT) reads `NNT = 1/0.000667 = 1500.00, round up: 1500` inside the screen. Page 4 reads `the outcome is rare here (Ru = 0.1 %).`
4. **Module 3 with (1, 1, 2999, 2999).**
   - Page 4: `sens = 0.0 %, spec = 100.0 %`.
   - Page 5: `TPR = sens = 0.0 %`, `FPR = 1-spec = 0.0 %`, ` = 0.000/0.000 = 1.00`.
   - Write down whether the Youden line shows `0.000` or `-0.000`.
5. **Stratified (M-H), case-control,** strata (10, 2, 2, 10) and (2, 10, 10, 2): the forest plot (page 3) reads `Breslow-Day p < 0.01: are the strata's ORs alike?`.
6. **The fallback.** Not testable on the Prime unless the CAS fails, which it did not in round 2. Help F and module 3 page 6 should still show "exact (CAS)" as in round 2: `= 53/120`, `SE = sqrt(53/120) = 0.6646`.

## Unresolved (for Roger)

- **Extreme tables round to zeros.** A table with an OR below 0.005 now shows, for example, `OR = 0.00 exaggerates RR = 0.00 by 60 % here`, `ln OR = ln(0.000) = -8.006` and `= 0.000/0.000 = 1.00`. Each number is honestly rounded, but a student may read `ln(0.000)` as ln 0. The brief's rule is ROUND first. Three significant figures (`es_SigTxt`) would read better in the worked boxes, but they would change how every ordinary value prints there (`0.500` instead of `0.50`). Your call; v1.7b keeps the fixed decimals.
- **A value of 10^12 or more** also prints in scientific form with fixed decimals (`STRING(1E15, 2, 0)` = `1ᴇ15`). No display here can reach it with classroom tables: `es_FmtNum` switches to Standard above 9999, and N ≤ 2000 caps the conditional OR. This is not changed.
