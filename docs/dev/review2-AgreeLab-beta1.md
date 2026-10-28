# Second review: AgreeLab beta 1 (26 Oct 2026)

Independent reviewer; I did not write the program. I read the brief (v2) and Lessons Learned v7r in full, and only the parts of the program listed under "Checked" below.
My scripts are in `/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/rev2_agree/`:

- `chk.py`: the formulas, through the harness routines, 778 checks;
- `ui.py`, `ui2.py`, `ui3.py`: pages in the harness.

The references are my own, not the builder's `ag_ref.py`:

- delta-method SEs by numerical gradient, both non-null and at independence;
- statsmodels `cohens_kappa` and `fleiss_kappa`;
- per-category Fleiss kappa as Fleiss' kappa of the collapsed j / not-j table;
- pingouin `intraclass_corr`;
- the McGraw & Wong formulas in SciPy;
- `linregress`;
- a non-central-t exact LoA interval and a coverage simulation.

The gate passes (re-read its output). The verify script reports 5734 checks and 0 failures.

## Findings, most serious first

### 1. A 1-pixel drift across a tile edge moves a count (CONFIRMED, harness)
**Lines:** 1686-1689 (`ag_TTap`) and 241-250 (`ag_Poll`).

**What is wrong:** a "drag" is any press whose last finger point lies in a different tile (`ttB <> ttA`). There is no distance threshold, and the tiles touch with no gap. At k = 6 a tile is 21 px wide.

**Failure scenario:** on the MS Winnipeg preset, a press at (52, 50) with its lift at (53, 50) printed "1 moved A1,B1 to A1,B2: kappa 0.208 → 0.198". A real finger tap near an edge does this silently. It also fires in place of the intended "tap the selected tile again to type".

**Fix:** count it as a move only when the press and the lift are at least about `MAX(8, agCZ/2)` px apart (`ABS(dx) + ABS(dy)`) AND in different tiles. Otherwise treat it as a tap on the press tile.

### 2. An edited preset keeps its published source label (CONFIRMED)
**Lines:** 1386, 1398, 1605-1660, 1847.

**What is wrong:** `ag_TMove`, `ag_TAdd`, `ag_TType`, `ag_TDiag` change `agT` but leave `agTTtl`, `agTSrc` and `agTIll` alone. After finding 1's move:

- the Kappa page still reads "Data: Landis & Koch 1977 (Westlund & Kurland)";
- the title still reads "MS: 149 Winnipeg patients";
- the Home summary is "Cohen's kappa = 0.198 (MS: 149 Winnipeg patients)". The published table gives 0.208.

This is an on-screen claim that the sources do not back.

**Fix:** on the first edit of a sourced table:

- set `agTSrc := "edited from " + agTSrc + ": not the published data"`;
- add " (edited)" to the title.

Do the same for Fleiss and continuous data, if they can ever be edited.

### 3. ICCs refused for perfect agreement and for a constant offset (CONFIRMED)
**Lines:** 854-855.

**What is wrong:**

- When MSE = 0 the page says "no residual spread (error MS = 0): ICCs undefined". With perfect agreement every ICC is 1.
- With a constant offset, {1,6},{2,7},{3,8},{4,9}, the ICCs are defined: ICC(3,1) = 1, ICC(2,1) = 0.118, ICC(1,1) = -0.579. That is exactly the consistency-versus-agreement lesson that line 2175 teaches.
- Line 854 (MSR = 0) also says "undefined". The single-rating forms equal -1/(k-1) there; only the average-measure forms divide by MSR.

**Fix:**

- MSE = 0 and MSR > 0: compute the point estimates and show "no F interval (error MS = 0)" for ICC(3) and ICC(1) where F is infinite.
- MSR = 0: reword the message to say that the average-measure forms are undefined.

### 4. ICC(2,k) with a zero or negative denominator prints `4.804ᴇ15` (CONFIRMED)
**Lines:** 860, 2136, 2147.

**What is wrong:** for {1,2,1},{2,1,2},{1,2,1},{2,1,2}, MSR + (MSC - MSE)/n = 0. The page shows "ICC(2,k) 4.804ᴇ15" (`h.sci_strings`), and `ag_Mark` is called at x ≈ 1E15.

On the device, a RECT_P that far off screen is untested (PLAUSIBLE: an error, or nothing drawn).

**Fix:** if `icMR + (icMC - icME)/icN <= 1E-10*icST`, mark ICC(2,k) undefined ("--") and draw no mark. Also guard the `ag_Mark` x against values outside [agXlo, 1].

### 5. Bland-Altman limit CIs: an unlabelled approximation (CONFIRMED)
**Lines:** 944, 2338-2340, 1180-1181.

**What is wrong:** SE = s·√(1/n + 1.96²/(2(n−1))) is Bland & Altman's approximation, and it is shown as plain "95% CI". In my simulation (40,000 runs) the actual coverage was:

| n | Coverage | Misses on the side where the true limit lies above the interval |
| --- | --- | --- |
| 3-5 | 0.92 | 8% |
| 17 | 0.94 | 6% |

The nominal share of misses on that side is 2.5%.

For the PEF preset's upper limit:

- approximate: 39.1 to 108.6;
- exact (non-central t, Carkeet 2015): 48.9 to 119.9.

The program accepts n = 3.

**Fix:** label it "approx. 95% CI (B & A 1999)". Add a "rough for small n" note, as the kappa help already does. Optionally give the exact interval.

### 6. Kappa CI and p at the edges (CONFIRMED)
**Lines:** 710-716; pages 2 and 3.

**What is wrong:**

- N = 2 with perfect agreement prints "95% CI 1.000 to 1.000 (SE 0.000)" and "p = 0.0786". Any table with kappa = 1 gets SE = 0.
- The 0/12/9/0 table prints the CI as "-1.192 to -0.728", which goes below -1, and its p as "1.0000".

**Fix:**

- Clamp the CI to [-1, 1].
- When SE = 0 or N < about 30, say "large-sample interval: not meaningful here".
- Print "p > 0.9999".

### 7. The polling loop does not drain a finger (PLAUSIBLE)
**Lines:** 235 (`ag_Poll`), after the CHOOSE in `ag_TMenu` (1747) and the matching menus.

**What is wrong:** `ag_Poll` drains keys only. If a CHOOSE item is tapped and the finger is still down when the view redraws, the next MOUSE poll reads it as a tile tap, or as a move (finding 1).

**Fix:** call `ag_Drain()` at the top of `ag_Poll`, or after each menu CHOOSE.

### 8. Low-priority wording
- **Line 2341:** "(B & A 1986 used 2s: -79.65 to 75.41)". The paper prints -79.7 to 75.5, from rounded values. Say "the paper prints -79.7 to 75.5 from the rounded bias and s".
- **Line 1389:** the tile footer reads "+/- = n". It changes the selected tile's count, so write "+/- = count".

## Checked and correct
- **Cohen's kappa:**
  - po, pe, kappa;
  - the non-null SE of Fleiss, Cohen & Everitt (1969), used for the CI;
  - the H0 SE, used for z and the one-sided p, labelled one-sided with H₁ = kappa > 0;
  - kappa max (Cohen 1960) and PABAK.

  All match the delta method and statsmodels to about 1E-7, on the presets, 12 random tables, a zero-margin table, negative kappa, perfect 2×2 and 3×3, and N = 2. pe = 1 and the empty table are handled with messages, with no error.
- **Weighted kappa, linear and quadratic:** kappa, the non-null SE and the H0 SE all match.
- **Fleiss' kappa:**
  - the Fleiss 1971 preset gives 0.430245 and z = 17.65183, as R irr reports;
  - each per-category kappa equals the kappa of its collapsed j / not-j table;
  - the per-category SE0 is √(2/(Nm(m−1)));
  - an undefined category shows text, not 99.
- **ICC:**
  - all six forms match pingouin and my own ANOVA;
  - the F CIs for ICC(1) and ICC(3) and the Satterthwaite CIs for ICC(2,1) and ICC(2,k) (McGraw & Wong) match to 1E-6, including the fractional-df Newton quantile, on Shrout & Fleiss (.17 .29 .71 .44 .62 .91, ICC(1,1) CI -0.133 to 0.723), PEF and 10 random sets;
  - the F tests of ICC = 0 match;
  - the -∞ bound of ICC(2,k) is correct.
- **Bland-Altman:**
  - the bias, s, the limits, the t quantile and the proportional-bias regression (slope, two-sided p) match;
  - s = 0 shows no p and no error;
  - n < 3 is refused.
- **Device rules:** I found no case-only clashes in the file. The following are as the rules require:
  - lower-tail forms (`NORMALD_CDF(0,1,-z)`, `-STUDENT_ICDF`, the F mirror);
  - the ICDF clamp;
  - no FISHER call at a fractional df;
  - `ag_Fx` rounds before STRING;
  - the drains in `ag_Msg` and `ag_WaitAny`;
  - the capped finger drain;
  - CHOOSE indices start at 0;
  - INPUT on LOCALs;
  - IFERR on the D1-D9 reads;
  - MSGBOX texts are 5 lines or fewer at 38 characters.

  Lint's line-1319 note is a false positive (`agK` sits inside numeric arguments).
- **Data:**
  - MS Winnipeg and New Orleans match the Rdatasets CSV and `msdiag.sas` (rows are the New Orleans neurologist);
  - the PEF readings match Table 1 of `ba.txt`;
  - the Shrout & Fleiss data match `ICC.Rd`;
  - the Fleiss preset is identical to statsmodels' copy;
  - the paradox tables are labelled illustrative;
  - Landis & Koch appears only as "their convention, not a test".
