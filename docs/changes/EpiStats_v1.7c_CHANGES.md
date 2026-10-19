# EpiStats v1.7c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on v1.7b; every v1.7b feature is kept, and every ordinary display is unchanged. Not yet run on hardware or on the emulator.*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). `es_FmtNum` writes `< 0.001`, or `> -0.001`, below its floor, and `es_SigTxt` writes `< 0.000001`. v1.6 had already written `es_EqTxt` for this (`"P < 0.000001"`, not `"P = < 0.000001"`), but 29 displays still put the floor after `= `. In 8 of them the label is drawn apart from its value, so the screen read `IRR = IRe / IRu =   < 0.001`. Each of these took only ordinary inputs:
- a cohort with 1 case in 100,000 exposed read `RR = Re/Ru = < 0.001`;
- 1 case in 200,000 person-time read `= < 0.01 per 1,000 person-time`;
- a stratum read `OR₁ = < 0.001  (0.00-0.00)`;
- a power of 0.5001 read `z_β = < 0.001`.

**A chi-square p that read 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. The 2 × 2 page's Pearson and Yates p, and module 3's summary p, were `1 - CHISQUARE_CDF(1, x)`. That is exactly 0 once the tail is below the CDF's last digit, which on the Prime means a chi-square above about 52. The 2 × 2 page then read `0.00000 *`, where a smaller chi-square read `< 0.00001 *`, and module 3 read `p=0.0000`.

## What changed (line numbers: v1.7b → v1.7c)

1. **Two new helpers**, after `es_EqTxt`. Each reads `LEFT(…, 1)` only inside `IF DIM(…) > 0`, and neither uses INSTRING.
   - **`es_EqLb(lbL, lbS)`** (→ 787-798) is for a label drawn apart from its value. It returns the label with its closing `" ="`, or the label alone when the value starts with `<` or `>`.
   - **`es_EqV(evS)`** (→ 800-809) is for a value line that starts `"= "`. It returns `"= " + value`, or the value alone.
2. **Through `es_EqTxt`** (label and value in one string), 17 displays:
   - module 1's reading: RR, OR, LR+ and LR− (2135, 2136, 2192 → 2187, 2188, 2245);
   - page 7's sample OR (2470 → 2524);
   - the ROC page's LR+ and LR− (3693, 3696 → 3754, 3758);
   - module 5's stratum estimates, crude and M-H, on the summary and the forest plot (4717, 4793, 4795, 4997, 5004 → 4791, 4868, 4870, 5073, 5080);
   - the sample-size pages' z_α/2, z_β and Cohen's d (5159, 5222, 5273, 5324 → 5236, 5300, 5352, 5404).
3. **Through `es_EqLb`**, 8 labels:
   - module 2 page 2's RR, OR and ERR (3148, 3155, 3169 → 3206, 3214, 3229);
   - the IR pages' IRR, IRD and ERR (4319, 4324, 4331 → 4387, 4393, 4402);
   - the PT-NNH and PT-NNT (4370, 4375 → 4442, 4448). These are reached with a rate above 10 per unit of person-time.
4. **Through `es_EqV`**, the four `= … per 1,000` lines (4298, 4303, 4308, 4327 → 4363, 4369, 4375, 4397).
5. **The chi-square p, 1 df** (2603, 2618, 3996 → 2659, 2675, 4059). It is now `2 * NORMALD_CDF(0, 1, -(x^0.5))`, the same number, P(χ²₁ > x) = 2Φ(−√x), kept to its last digit.
   - Module 3's compact `p=` line (4173 → 4237) reads `p<0.0001` below its floor, in its own compact style. It never reads `p=< 0.0001`.
6. **Header:**
   - the banner (3);
   - the tested-on line (15);
   - a "What changed in v1.7c" paragraph (→ 26-52);
   - the menu title (511 → 538) and About (5395 → 5475).
   - A comment above each changed statement says what it does.

**Before and after** (harness, end to end through the menu, as part H1 of the verify does):

| Case | v1.7b | v1.7c |
|---|---|---|
| Module 1, 1 99999 50 50 | `RR = Re/Ru = < 0.001   (0.00-0.00)`, `OR = ad/bc = < 0.001   (0.00-0.00)` | `RR = Re/Ru < 0.001   (…)`, `OR = ad/bc < 0.001   (…)` |
| Module 1, 1 2000 2000 1 | `Sample OR = ad/bc = < 0.000001, Woolf CI …`; `LR+ = sens/(1-spec) = < 0.01,  LR- = 2000.000` | `Sample OR = ad/bc < 0.000001, …`; `LR+ = sens/(1-spec) < 0.01,  LR- = 2000.000` |
| Module 1, 9999 1 1 9999 | `…,  LR- = < 0.001` | `…,  LR- < 0.001` |
| Module 1, 80 10 10 80 (χ² 113) | `0.00000 *` (Pearson and Yates p) | `< 0.00001 *` |
| Module 2, 1 99999 50 50; 5002 4998 5000 5000 | `RR = Re / Ru =`, `OR = (a×d)/(b×c) =` then `< 0.001`; `ERR = RR - 1 =` then `< 0.001 (0.0%)` | `RR = Re / Ru`, `OR = (a×d)/(b×c)`, `ERR = RR - 1`, each then `< 0.001` |
| Module 3, 1 1000 999 10 | ROC ` = 0.001/0.990 = < 0.01`; page 3 `p=0.0000` | ` = 0.001/0.990 < 0.01`; `p<0.0001` |
| Module 4: 1, 50, 200000, 100; 10001, 10000, 1E9, 1E9; 100, 0, 1, 1 | `= < 0.01 per 1,000 person-time`, `IRR = IRe / IRu =`; `IRD = IRe - IRu =`, `= < 0.001 per 1,000 PT`, `ERR = IRR - 1 =`; `PT-NNH = 1/IRD =` (then `< 0.1`) | `< 0.01 per 1,000 person-time`, `IRR = IRe / IRu`; `IRD = IRe - IRu`, `< 0.001 per 1,000 PT`, `ERR = IRR - 1`; `PT-NNH = 1/IRD` |
| Module 5 OR, two strata 1 9999 1000 1000 | `OR₁ = < 0.001  (0.00-0.00)`, `Crude OR = < 0.001 …`, `M-H OR = < 0.001 …, both` | `OR₁ < 0.001  (…)`, `Crude OR < 0.001 …`, `M-H OR < 0.001 …, both` |
| Module 6: power 0.5001; power 0.4999; δ 0.0001; α 0.99999 | `z_β = < 0.001`; `z_β = > -0.001`; `Effect size (Cohen's d) = < 0.001`; `z_α/2 = < 0.0001` | `z_β < 0.001`; `z_β > -0.001`; `Effect size (Cohen's d) < 0.001`; `z_α/2 < 0.0001` |
| ordinary tables (10 20 30 40, 12 5 7 14, 5 5 5 5, 1 2 3 4) | every page | the same |

**Left alone (checked):**
- **The conditional MLE OR** (2139, 2471). Its smallest value at N ≤ 2000, the only N it is computed for, is 1.67E-6 (SciPy, at 1 999 999 1). That is above `es_SigTxt`'s floor of 1E-6, so the line never starts with `<`. Its CI bound can read `< 0.000001`, but that is inside the brackets, not after an "=".
- **The risk module's NNT** (3187, 3195) is `1/|RD|` with |RD| ≤ 1, so it is at least 1.
- **The forest plot's no-CI line** (4954) is shown only for a zero count, where the estimate is exactly 0 (`0.00`) or undefined.
- **McNemar, Breslow-Day and the M-H p** go through `es_PTxt`, which already writes `p < 0.0001`, 0 included.
- **Residual.** `2 NORMALD_CDF(−√x)` itself underflows to 0 for a chi-square above about 2,275 on the Prime (reals to 1E-499), or about 1,400 in the harness's doubles. In the harness, 1 2999 50 50 (χ² 1493) still reads `0.00000 *`; on the Prime it should not, since its reals reach 1E-499, but this is untested. Only a table of N in the thousands with near-total association gets there. Module 3's line reads `p<0.0001` even then; the 2 × 2 page's would read `0.00000 *`.

## Verification

`verify_EpiStats_v1.7c.py` was built from the v1.7b script, and every check is kept. It runs on v1.7c in harness ppl_run_v3d, as before. Output is in `verify_EpiStats_v1.7c_output.txt`: **ALL CHECKS PASSED: 221 checks, 0 failures** (v1.7b's script: 163).
- **Kept checks on v1.7c.** Run unchanged on v1.7c, the v1.7b script fails only these four checks:
  - F3's run 1, which expected `OR = ad/bc = < 0.001`;
  - F3's word comparison on 1 1 1 997, where the p was 0;
  - G2's routine list and G2's version line.

  In the new script:
  - F3's run 1 expects `OR = ad/bc < 0.001`;
  - F3 reads v1.7a's text the v1.7c way (`= <` → `<`, `0.00000 *` → `< 0.00001 *`, `p=0.0000` → `p<0.0001`);
  - G2 keeps comparing the v1.7b and v1.7a files.
- **H (new):**
  - **H1.** Every row of the table, end to end, v1.7c against v1.7b. On each page every other text is v1.7b's, or v1.7b's without `= <`.
  - **H2.**
    - `2 NORMALD_CDF(0, 1, −√x)` equals `chi2.sf(x, 1)` to 1E-12 relative, for x from 0 to 1000.
    - The 2 × 2 page's two p-values for χ² of 20 to 109 never read `0.00000`, in doubles and in the Prime's 12 digits (CHISQUARE_CDF and NORMALD_CDF rounded to 12 significant digits); from χ² 36 up they read `< 0.00001 *`. v1.7b read `0.00000 *` at χ² 71 and 109.
    - Five ordinary tables are unchanged on every page.
  - **H3.** 54 tables through modules 1, 2 and 3 (162 runs): v1.7c is v1.7b without `= <`, with the p-value and label forms above, and nothing else. 102 runs are identical and 60 differ only so (8 distinct lines, `p=< 0.0001` → `p<0.0001` among them).
  - **H4.** `es_EqLb`, `es_EqV` and `es_EqTxt`, including `""`.
  - **H5.** The code:
    - The added code is the two helpers, the 29 display sites and the p form, the 3 p lines and the version strings.
    - Each changed display line, written back without the helpers, is v1.7b's line.
    - The new names (`es_EqLb`, `es_EqV`, `lbL`, `lbS`, `evS`) are not built-ins, ignoring case.
    - The banner, the menu title and About say v1.7c.
    - No comment sits inside an open bracket.
    - INSTRING is as in v1.7b. Every LOCAL line holds 6 names or fewer.
  - **H6.** The sites left alone, as above.
- **SCI (kept).** No scientific STRING result in any harness run of v1.7c.

## Gate

`python3 ppl_gate_v1b.py EpiStats_v1.7c.txt EpiStats_v1.7b.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 66 E4, 36 E9, as v1.7b. There are no hard errors, E12 included.
- lint_ppl: 87 problems, as v1.7b.
- Full parse: it stops at the EXPORT list, as v1.7b does.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v1.7b (open it in the Kit). Then Program Catalog → Check. The menu title reads `EpiStats v1.7c`.
2. **2×2 Table Analysis, a b c d = 80 10 10 80:**
   - the χ² page's two p-values read `< 0.00001 *`, never `0.00000`;
   - the reading page reads `RR = Re/Ru = 8.000 …`, with its `=`, since the value is ordinary.
   - Then 1 99999 50 50: `RR = Re/Ru < 0.001`.
3. **Incidence Rates, 1, 50, 200000, 100:** page 1 reads `< 0.01 per 1,000 person-time`, and page 2's label reads `IRR = IRe / IRu`, with no trailing `=`, before `< 0.001`.
