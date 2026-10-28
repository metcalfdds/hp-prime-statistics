# RankLab beta 1a — changes from beta 1 (21 Oct 2026)

Every finding of the independent second review (`REVIEW2_RankLab_beta1.md`) is applied, one line each, numbered as in the review. `RankLab_beta1.txt` itself is unchanged.

1. **Small-n correlation p (review 1).**
   - Spearman's p is now exact for n ≤ 7. `rk_SpPerm` walks all n! orders of y with Heap's algorithm and updates the statistic once per swap, in whole numbers; ties are allowed.
   - Above n = 7, a perfect order without ties gets the exact 1/n!. Otherwise the t approximation is used, with a red caution line below n = 10. A perfect order with ties above n = 7 gets no Spearman p, and the verdict uses Kendall's.
   - Kendall's p is now exact without ties for n ≤ 30. `rk_KdNull` counts inversions with the same top-down / bottom-up shape as `rk_MWNull`. With ties it falls back to z and says so.
   - The Null page draws both exact nulls as bars on the rs or tau-b scale (`rk_CorNull`, `rk_IsBars`, `rkNObs`/`rkNMu`).
   - The verify script checks every exact p against brute-force enumeration in Python and against `scipy.stats.permutation_test` / `kendalltau(method='exact')`. SciPy's asymptotic p is no longer the reference for these.
2. **Quit summary mislabel (review 2).**
   - The summary is now written by `rk_Pick` after each run that worked (`rkSumS`), and Quit returns that string.
   - `rk_Open` puts back the last test, tail and mode when a test is refused or the group pick is cancelled.
   - Every refusal path followed by Quit was tested.
3. **USJudgeRatings design (review 3).**
   - New preset "US judges: 3 criteria": the 43 judges are the blocks and integrity / oral rulings / written rulings are the treatments, a real Friedman test (Q = 69.547, p ≈ 8E−16).
   - Beta 1's 11-criteria design is kept as "US judges: halo (W only)". It shows W as a description with no p, and the Result and Null pages say why: the criteria are not independent raters, since the same lawyers rated every criterion. `RK_P` = −1 there.
   - The help pages and header are reworded to match. Help page 7 notes that the MockJury test ignores the Crime factor.
4. **Esc (review 4).**
   - `rk_Prog` takes a third argument, the "Esc = stop …" text, and prints it only when the loop that called it reads Esc (`rk_Esc`, which drains the keys).
   - Esc is now read in: ranking and ordering (every 50 values), Friedman blocks, KW group summaries, the Kendall merge passes, the Kendall and MW exact counts, the signed-rank count, the Spearman orders and both Hodges-Lehmann loops.
   - If Esc stops a ranking, a message says so, no test opens and the summary is unchanged. If Esc stops an exact count, the approximation stays.
5. **Chi-square cautions and the one-block refusal (review 5).**
   - Kruskal-Wallis shows a red caution when any group has n < 5.
   - Friedman shows a red caution when b < 10, and refuses b < 2.
6. **CHAR(179) (review 6).** The text now reads "sum(t^3 - t)". The verify script checks that every `CHAR()` in the source is in the verified glyph set.
7. **Mean Spearman between blocks (review 7).**
   - `rk_FrRbar` computes it pair by pair as Pearson's r of the within-block midranks, so it is right with ties.
   - When a block ties every treatment the page says "none (a block is all tied)".
8. **Width overruns (review 8).**
   - Every flagged line is shortened: the U SD line, "Exact p: none with ties: normal used", the correlation n line, the W line, the verdict note, the KW k line, the help footer, and Dunn names cut to 7 characters.
   - The verify script now checks each font-1 line against its own TEXTOUT_P width at 6.5 px a character.
9. **Small items (review 9).**
   - "1 group" instead of "1 groups" (`rk_Grp`).
   - The normal line says "(cont. corr.)" in place of "(ties, cc)".
   - The one-sample INPUT shows m₀ and H₀ (CHAR(8320), label and help from string variables), and so does its source line.
   - The Hodges-Lehmann lines say what they estimate ("HL estimate of the median d", "of the shift X - Y").
   - Friedman's H₀ now reads "in each block all orders equally likely".
   - No magenta among the group colours or the d < 0 dots; magenta is kept for the p tail. Curve tails are shaded in the house blue (`rkLMAG` is removed).
   - A sign test with too many bars says so on its Null page. "(two-sided, ties)" appears only when there are ties.
- **Device checklist:** added Mann-Whitney on two draft months (the CHOOSE `{cgN(1), cgN(2), …}` form with 12 items).
