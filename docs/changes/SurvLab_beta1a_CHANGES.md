# SurvLab beta 1a: changes from beta 1 (21 Oct 2026)

These changes act on the second review, `REVIEW2_SurvLab_beta1.md`, items 1-15. `SurvLab_beta1.txt` is unchanged.

- **Verify:** `verify_SurvLab_beta1a.py` gives 5,619 checks, 0 failures. Its Part E has one or more checks per item.
- **Gate:** `ppl_gate_v1c.py SurvLab_beta1a.txt SurvLab_beta1.txt` gives PASS. The kit lint has 0 errors and ppl_check_v4 is clean. lint_ppl's 6 problems are the known file-name and EXPORT-discipline noise; all the "not a GROB" lines are gone. fleet_names reports 0 collisions.
- **Harness:** it ran under the updated `hpkit/interp.py`, which raises an error on `+` with a list operand. Nothing tripped, because SurvLab has no list arithmetic.

| # | Change |
|---|---|
| 1 | No grob is passed as a parameter any more. All 8 drawing helpers (`sv_Frame`, `sv_Grid`, `sv_XLab`, `sv_Steps`, `sv_Ticks`, `sv_Band`, `sv_DotH`, `sv_DotV`) draw on G1 by name. `sv_Frame` clears with `DIMGROB_P(G1, 320, 240, #FFFFFFh)` (ChiTable's way). The KM plot is composed in G1 and cached with `BLIT_P(G2, 0, 0, G1)` (GaltonBoard's device-run `BLIT_P(G2, 0, 0, G3)` shape); each frame starts with `BLIT_P(G1, 0, 0, G2)`. A static check confirms that every drawing call names G0, G1 or G2. |
| 2 | **Life table, end of follow-up.** The last interval is cut at the row's last observed time T and closed: [48, 52], not [52, 56). Those censored at T complete it and are not halved; a new column `svLF` holds them. On the last row the page says "Ends at 52: the 318 still followed then complete it". Help page 4 and the header state the convention: Cutler & Ederer's half-interval rule for withdrawals; the closing date treated as in Lee & Wang ch. 4 and Collett §2.1.1 (pages not checked). Rossi all, width 4: S(52) = 0.7361 = KM; it was 0.7271 at "56". With no censoring before T, the life-table S equals KM at every interval end (Rossi, and 15 random sets). The table's first column is now "from-to" (e.g. 48-52). |
| 3 | **Quantile wording.** "First time S < 1 − p" is now called statsmodels' rule, and "SAS and R average when S sits exactly on 1 − p" is added (help, header, `sv_Quant` comment). S = 0.75 is now "the 25th percentile, or first quartile, of the time to re-arrest"; "75th-percentile" is gone. Page titles read "Time by which 25% are re-arrested" / "Median: time by which 50% …", and headings "25th percentile (Q1): first time S(t) < 0.75". |
| 4 | **Speed.** Your data is capped at 500 rows (was 2,000). In the harness, 500 rows cost about 54,000 statements to draw the KM plot and 69,000 to fit; Rossi costs 6,200 and 17,200. The "working" page now appears from 150 rows. A KM plot with more than 150 steps shows "Drawing N steps ... (Esc = no band)", and Esc, polled every 25 steps, stops the band and says so. Each quantile and its CI are computed once per page draw: the Rossi page fell from 4,169 to 3,296 statements. |
| 5 | One row in C1: the MSGBOX now says "Need at least 2 rows; C1 has 1." instead of "no data". |
| 6 | "An observed grouping, not an experiment." now appears only for SurvLab's own splits (new flag `svSplit`), not when C3 holds a single code. |
| 7 | The H(t) one-curve line now reads "KM S = …; exp(-H) ≥ S, close while many at risk" instead of "close to it". This is checked on 20 random sets and on the two-events-at-3 case (S = 0, exp(−H) = 0.368). |
| 8 | Peto's HR exp((O₁ − E₁)/V), with CI exp(± 1.96/√V), is shown under the O/E ratio: Rossi 0.692, CI 0.479 to 1.000. "Peto's CI misses 1 exactly when log-rank p < 0.05" is shown and checked on every random set. The borderline line now names the O/E-ratio CI. The assumption line reads "HR assumes proportional hazards (no crossing)". New Home export `SV_HRP`. |
| 9 | Page 3 now says "(rule of thumb): suggests the gap …", and help page 3 says the early/late line is SurvLab's rule of thumb, not a test. |
| 10 | In the life-table plot, a tap off every bar clears the selection. A tap on the KM title now explains the view ("Band = 95% CI of S(t); ticks = censored times", or the H(t) form). |
| 11 | A row with no events gets "no events, so no quantile can be estimated: S(t) stays at 1" instead of "try 25%". |
| 12 | The quantile CI's upper end is open. The quantile page says "upper end not included"; help says "up to the next event time (not included); n.r. = open". |
| 13 | The header cites Allison (1995) *Survival Analysis Using the SAS System: A Practical Guide*, SAS Institute, and the R package carData. |
| 14 | At-risk counts now start at x ≥ 42, clear of "no aid". The load page's source line is "Data: …" (shorter). Shortened: the life-table footer ("tap row = info") and the page-3 line. The log-rank bar panel is 8 px shorter, so its legend no longer touches the HR line. |
| 15 | Band colours: not changed; this is left as Roger's decision (see NOTES). |
