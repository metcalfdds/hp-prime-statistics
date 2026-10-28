# ResampLab beta 1a — changes from beta 1 (21 Oct 2026)

One line per fix, numbered by the item in `REVIEW2_ResampLab_beta1.md`. `ResampLab_beta1.txt` is unchanged. Checks: `verify_ResampLab_beta1a.py` (Part R1–R8 and the audits added in Part A; every beta 1 check kept).

| Review item | Fix in beta 1a | Check |
| --- | --- | --- |
| 1 | `rs_Lab`: after EVERY action the keys are drained and `rs_Drain()` (the 1-s TICKS-capped finger drain) runs, so the Enter that closes a MSGBOX (Exact on MockJury/Rossi, CIs/BCa below B = 100, the 9,000 maximum) no longer opens the Actions menu | R1: stale-key mode, every soft key on both pages in all four modes, plus the Enter menu (exactly one Actions per Enter) |
| 2 | Jackknife in one pass (`rs_Jack`): mean (S − xᵢ)/(n−1); SD by the sum-of-squares downdate; median and 10% trimmed mean from the sorted list with prefix sums; progress bar + Esc above n = 300 (Esc: "BCa: jackknife stopped by Esc"). n = 1,000 starts in 0.13–0.23 s in the harness (beta 1: 19 s at 999) | R2: against leave-one-out in numpy, 8 data sets × 4 statistics and n = 1,000; Esc at n = 400 |
| 2 | BCa cap: none needed after the one-pass jackknife; the most data accepted is 1,000 values (raised from 999), all within the jackknife's budget (0.13–0.23 s in the harness, so 4–23 s on a G1 by the ×30–100 rule) | R2 timing |
| 3 | `rs_Splits` replaces `COMB(N, k)`: the count is built term by term and stops past the limit; above it, its size from a sum of logs ("about 10^600"); exact text below 10^9 | R3: nine (N, k) against `math.comb`; 1,000 v 1,000 through the menus |
| 4 | `rsBusy`: during a bulk run the redraw skips `rs_BtCI` (no sort of every value); the status says "intervals at the end"; the intervals are computed once at the end | R4: at most one `rs_BtCI` call in a 3,000-resample run with frequent redraws |
| 4 | The 60-s cap is re-checked at every 2-s redraw on the time actually used (redraws included), and a cap is a whole number of hundreds | R4: a run that slows after the first check is still capped; H11 |
| 5 | `rsEps` = 1E−9 × the pooled values' range (two groups) or × mean |d| (paired), not "+ 1"; `rs_Grid` refuses a nonzero value that rounds to 0 | R5: {1..5} v {6..10} and paired {1,3,2,4,−1} at ×1E−10, ×1, ×1E10 against itertools; MC replay |
| 6 | Darwin source: "sec. 21 (15 pairs in 4 pots)"; note "grew in the same pot" | R6: the CSV's pot column has 4 values; page text |
| 7 | `rs_PEq` ("p = 0.0476" / "p < 0.0001") and `rs_PFr` ("p = 12/252 = 0.0476", "p = 2/32,768 (p < 0.0001)", "p = 0/1,000"); used on every page, the Info page (SE written "= 0" or "< 0.0001") and the Home summary | R7: D1 = 1..15 paired; audit: no "= <" in any text or summary of any run |
| 8 | `rs_Para` stops at y 208 (never into the footer); "Meaning" paragraph shortened | audit: text-page lines ≤ 209; the review's heavy-tie Info page |
| 8 | Over-wide lines shortened: exact status line (no "(Exact, on More)"), BCa reasons, tap notes ("a..b: n (r in tail)"), CIs note, splash credit | audit at 6.5 px/char |
| 8 | INPUT help lines: "0 = fresh; a whole number repeats a run", "0.5 to 0.999 (0.95 = 95%)" (≤ 43 characters) | R8 |
| 8 | MSGBOX texts all ≤ 100 characters | audit |
| 8 (15) | Paired page: "Each shuffle flips each pair's sign at random, as if H₀ were true." | R8 |
| 8 (13) | After a bulk run a tap on a bootstrap value says "(a value in the sample)"; "picked k times" only after Once | R8 |
| 8 (14) | The one-sample bootstrap names its data ("mean of differences cross − self = …", "group A (Unattr)"); Use my data with equal lengths resamples D1 − D2, as Darwin resamples its differences | R8 |
| 9 | Counting by sums limited by its work, n × Σ|d|f ≤ 20,000 (Darwin 8,160); Esc read in its final loop too | R8 (n = 30, Σ = 1,020 refused) |
| 16 | "Fisher (1935, sec. 21) worked this test on these data" (no unverified "by hand"); the header says the TI "Resampling" activity is not in ref/ | R6/H3 text |
| 17 | Help: a seeded run repeats unless the 60-s cap cuts it on a slower calculator | — |
| 18 | Once's animation gated by `rsNd` on the paired page; CIs picture labels "pct/basic/BCa/t"; "If they differ a lot: skew or lumps"; Help's "middle N%" follows Level; menu title "ResampLab: Rossi" (short name); key legend on the permutation pages | R8 |
| 19 | NOTES state that |d| ≥ |obs| is not SciPy's default two-sided rule (2·min of one-sided) | NOTES |
| (beta 1 report) | Exact limit 2,000 splits | H9b |
