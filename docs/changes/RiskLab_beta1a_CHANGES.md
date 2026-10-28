# RiskLab beta 1a - changes from beta 1 (26 Oct 2026)

From the second review (`REVIEW2_RiskLab_beta1.md`). `RiskLab_beta1.txt` is untouched. Verify:
`verify_RiskLab_beta1a.py`, 611 checks, 0 failures (beta 1's 572 carried over, a few updated on
purpose, plus Part D). Gate `ppl_gate_v1c.py RiskLab_beta1a.txt RiskLab_beta1.txt`: PASS.

| # | Review item | Change |
| --- | --- | --- |
| 1 | `rl_HL` and `RL_HL` are one name on the Prime | routine renamed `rl_HosLem` (definition and 5 calls). A case-folded scan of every routine, EXPORT and file-level LOCAL (250 names) finds 0 pairs; on beta 1 it finds only this one. No routine LOCAL folds onto a global. |
| 2 | Help page 7 misplaced the article's 44.9% / 23.5% | Help: "Their article's FPRs, 44.9% and 23.5%, count all 7,214 people (no date or charge filters). After the filters: 42.3% and 22.0%." DATASETS_RISK.md and NOTES corrected the same way; the verify recomputes 44.85 / 23.45 and 27.99 / 47.72 from all 7,214 rows (3,696 / 2,454). |
| 3 | False separation warning | Separation now comes from the fit only: no convergence in 25 steps, information singular after >= 3 steps, or a linear predictor that orders Y perfectly (new `rl_Order`). A converged fit with |eta| > 15 gets a grey note "converged (n steps); a fitted P is ~0 or ~1". The reviewer's wide-x case: no warning, numbers = statsmodels. Complete, quasi-complete and two-predictor separation are still flagged on the page. Help page 2 reworded. |
| 4 | "432 parolees" | Opening page: "Rossi's 432 men released from Maryland state prisons." |
| 5 | Zero-width AUC CI | SE = 0: "AUC = 0.500 (one score level: no interval)" / "AUC = 1.000 (SE = 0: no interval)". Red "small n or a bound cut at 0/1: the CI is rough" when a class has < 20 people or a bound is cut (with the in-sample note combined for a model's P). |
| 6 | COMPAS calibration: whose P | Title "Calibration: COMPAS (RiskLab's fit)", grey line "pred: RiskLab's logistic of Y on the score", tap: "in-sample fit to these people, not COMPAS's"; Help page 5 line added. |
| 7 | Wording | progress page mentions Rossi only for Rossi; "Y = 1: Y = 1" no longer printed; a constant x is "an x is constant or a mix of others"; footers "+/- = x10" with the × glyph; Help 6 "calibration vs equal average scores among Y=1 and among Y=0"; fairness table "PPV, FPR and FNR cannot all be equal when base rates differ (unless perfect): see Why." |
| 8 | G1 speed | unchanged estimate (about 20-60 s for Rossi with 4 predictors); timing is checklist item 8. |
| - | found while testing | huge b / SE under separation printed past their columns: table numbers now at most 7 characters (">999" from 1000, 1 decimal from 100), `rl_TF`. |

Device checklist: `RiskLab_beta1a_NOTES.md` (item 0: delete beta 1 from the calculator first).
