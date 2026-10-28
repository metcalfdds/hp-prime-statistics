# FitCheck beta 1a — changes from beta 1 (21 Oct 2026)

Source: `REVIEW2_FitCheck_beta1.md`. Beta 1 is untouched (md5 ed6f95fb…). The beta 1 parts are kept in `parts_beta1/`.

- **R1:** `fc_DrawBars` no longer crashes after Unmrg. It used to read the merged groups (`fcMS`/`fcME`) for a normal fit on bins before testing `fcMrg`, which stopped the program after Bins → Unmrg → Bars. Verify R1 runs this path on crimtab, Rossi and a D1 sample, with no error and the unmerged bins page shown.
- **R2:** the draft lottery preset is now a 2 × 2 table (Jan-Jun / Jul-Dec × low 1-183 / high 184-366).
  - Pearson χ² = 14.164, df 1, p = 0.000168, checked against `chi2_contingency(correction=False)`.
  - Fisher's exact (hypergeometric, drawn without replacement) is shown two-sided: p = 0.000243, checked against `fisher_exact` and a `hypergeom` sum. The new routines are `fc_LHyp` and `fc_Fisher`, checked against `fisher_exact` on 80 random tables.
  - The old fixed-share goodness-of-fit test (χ² 7.08, p = 0.0078) stays only as a teaching point on the Test page, which explains in plain words why it understates the evidence (variance factor (366 − 183)/365 = 0.50).
  - Merge is refused on a 2 × 2 table.
  - These p-values are shown to 6 decimals (`fc_P6`) so that Pearson's p and Fisher's p can be told apart.
- **R3:** Lilliefors p is given only for n ≥ 5, the start of Dallal-Wilkinson's range as implemented. For n = 3 or 4 the page shows "p not available for n < 5" in grey, `FC_PD = -2`, and the test is left out of the verdict (`fc_LDStr`, `fc_LDCol`).
- **R4:** the Benford first-two-digits test leaves out numbers below 10, counts them (`fcBenS`), and says so on the Test page and in a MSGBOX. If nothing is left after that, a message says so.
- **R5:** Castaneda's footnote 17 now comes from `data/DATASETS.md` and is cited as "430 U.S. at 496-497 n.17". The text is a paraphrase with one short quotation ("approximately 29 standard deviations"), plus the 1 in 10^140 sentence next to the exact p (4.18 × 10^-145). The source line reads "n. 17 at 496-497".
- **R6 (Esc and progress):** loading a sample with n > 200 shows a progress count every 250 steps (`fc_Prog`), and Esc stops the load cleanly ("Stopped (Esc): no sample is loaded").
- **R6 (Q-Q redraw):** the Q-Q page still redraws all n dots per keypress. This is not changed; it is on the device checklist.
- **R7:** the device checklist gains the ln Φ far-tail test: `NORMALD_CDF(0,1,-29.115)` ≈ 1.161E-186 and `NORMALD_CDF(0,1,-37.5)` ≈ 4.6E-308.
- **R8:** the moments and the Shapiro-Wilk sums are now taken in units of the largest |x − x̄| (`fcSc`), so nothing overflows. Values near 1E150 give the same s, g₁, g₂ and W as the unscaled data.
- **R9:** every source line is now at most 229 characters (it was 566). Long strings are split with `+`.
- **R10:** INPUT labels and help strings are built in variables first (`mdLb`, `mdHp`, `tbH`), and "H0"/"p0" on screen are now glyphs.
  - lint_ppl now reports two "INPUT return discarded" lines. Both are its 40-character heuristic: each return is tested in `IF INPUT(...) == 0 THEN RETURN`.
- **R11:** wording fixes.
  - Triola's question is labelled "(p. 653, paraphrased)".
  - "keep H₀" now reads "do not reject H₀".
  - The Castaneda source page is shown on every route.
  - "Phi(…)" is no longer written out on screen.
- **R12:** style fixes.
  - Footers are comma-separated.
  - The expected-bar fill is the house light orange #FFF0DC.
  - The glyph names are now `fcUD` (⇅) and `fcLR` (⇆).
  - Header, title page ("beta 1a") and file map updated.
- **R13:** the review found no list arithmetic. Nothing to change.
