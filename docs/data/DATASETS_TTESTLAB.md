# Data sets for TTestLab (31 Oct 2026)

A companion to `DATASETS_2026-10-21.md`, under the same rule: the source shown on screen, no invented data. TTestLab's three examples are summary numbers or small tables printed in teaching material, not data files. The checks below are what could be done with them.

| Example | The numbers | Source shown on screen (step 1) | Where they come from |
| --- | --- | --- | --- |
| **Age at arrest** (pooled t, two-tailed, α .05) | Hispanic female juveniles: N 44, mean 15.89 years, s 1.45. Non-Hispanic white: N 31, mean 16.57, s 1.11 | "age at arrest (years), JDCC" | Roger's lecture note on t-tests (Table 11.1): female juveniles transferred to adult court in the Juvenile Defendants in Criminal Courts (JDCC) data |
| **Matched jails** (dependent t, one-tailed H₁ μ₁ < μ₂, α .05) | Five matched pairs of inmate-on-staff assault rates, low (x₁) and high (x₂) percentage female security staff: 1.30 and 1.00, 1.25 and .76, .86 and .99, .94 and 1.10, 2.26 and 1.85 | "assault rate, Census of Jails" | The lecture note (Table 11.3), from the Census of Jails (COJ) |
| **Drug use by sex** (separate-variances t, two-tailed, α .05) | Male: N 270, mean 4.8185, SD 3.28798. Female: N 146, mean 6.4247, SD 3.74872 | "amount of drug use experience (SPSS)" | An SPSS output Roger supplied on 31 Oct 2026 (Group Statistics and Independent Samples Test tables). Summary numbers only |

## The checks

**Age at arrest.**
- The lecture's own working is reproduced from Table 11.1 with its rounding: √1.74 × √.05 = .29, and −.68/.29 = −2.34.
- Carried at full precision, the same numbers give SE 0.3097 and t = −2.20 on 73 df (SciPy's `ttest_ind_from_stats`, pooled). TTestLab's step 4 shows both.
- The JDCC microdata were not re-analysed: the lecture note is the only source of these figures here.

**Matched jails.**
- The lecture's Table 11.3 (the pairs) and Table 11.4 (the working) agree with each other:
  - differences .30, .49, −.13, −.16, .41, summing to .91, mean .182;
  - sum of squared deviations .38 (exact 0.37508).
- The lecture's t of 1.29 is reproduced with its rounding (.38/4 = .095 taken as .10, so sD = .32 and SE .14). At full precision t = 1.33 on 4 df (SciPy's `ttest_rel`).
- The COJ microdata were not re-analysed.

**Drug use by sex.**
- From the summary numbers alone, TTestLab reproduces what SPSS printed in its "Equal variances not assumed" row: t = −4.351, df = 265.924, Std. Error Difference .36918.
- SPSS also printed Levene's F = 6.847, p = .009. A Levene F needs every score, so it cannot be recomputed here.
- No raw data are included.

**The lecture's t table (appendix 1).** It was transcribed into `verify/TTestLab_lecture_t_table_v1.py` and checked cell by cell against SciPy (verify A6).
- 193 of its 198 cells equal the exact value to 3 decimals.
- The other five are all in the one-tailed .0005 (two-tailed .001) column. Rows 2, 3, 5, 7 and 23 print 31.598, 12.941, 6.859, 5.405 and 3.767; the exact values are 31.599, 12.924, 6.869, 5.408 and 3.768.
- TTestLab shows the table's figure as the table's and, in those five cells, the exact one beside it.
